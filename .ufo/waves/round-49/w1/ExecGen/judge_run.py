#!/usr/bin/env python3
"""judge_run.py -- run generated (RMLVO, keysym) cases against the pinned judge.

Seat-local harness for mado round 49 C1 clause g (not part of the lane's
committed instruments; the generator it exercises is ``gen.py``).

Per case: compile the keymap with the pinned ``xkbcli-compile-keymap`` in a
clean environment (HOME/XDG_* inside scratch), run the pinned
``xkbcli-how-to-type`` on it, and compare against the naive baseline
(first match only, no modifiers).

Determinism: the same seed must reproduce both the case list and every judge
stdout byte for byte.  Run with ``--runs 3`` (default) and the harness fails if
the three passes disagree.

Usage:
    python3 judge_run.py --work /fast/scratch/hyaku/mado-r49/ExecGen/work \
        --seed 4901 --n 400 --runs 3
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gen  # noqa: E402

ALLOWED_WORK_ROOTS = ("/fast/scratch/hyaku/mado-r49/",)


def check_work(path):
    real = os.path.realpath(path)
    if real == "/tmp" or real.startswith("/tmp/") or real.startswith("/var/tmp/"):
        raise SystemExit("judge_run.py: refusing a /tmp work dir (%s)" % path)
    if not any(real.startswith(root) for root in ALLOWED_WORK_ROOTS):
        raise SystemExit("judge_run.py: work dir must live under %s, got %s"
                         % (" or ".join(ALLOWED_WORK_ROOTS), path))
    os.makedirs(real, exist_ok=True)
    return real


def judge_env(work):
    home = os.path.join(work, "home")
    for sub in ("", ".cache", ".config", ".local/share", ".local/state"):
        os.makedirs(os.path.join(home, sub), exist_ok=True)
    return {
        "PATH": "/usr/bin",
        "HOME": home,
        "XDG_CACHE_HOME": os.path.join(home, ".cache"),
        "XDG_CONFIG_HOME": os.path.join(home, ".config"),
        "XDG_DATA_HOME": os.path.join(home, ".local/share"),
        "XDG_STATE_HOME": os.path.join(home, ".local/state"),
    }


def run_judge(case, keymap_path, env):
    proc = subprocess.run(
        gen.how_to_type_argv(case, keymap_path),
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env=env, timeout=120,
    )
    return proc.returncode, proc.stdout, proc.stderr


def one_run(seed, n, work, env, keysyms, keep_keymaps=False, weighting="difficulty",
            contrast=None):
    keymap_dir = os.path.join(work, "keymaps-%d" % seed)
    os.makedirs(keymap_dir, exist_ok=True)
    records = []
    for case, text in gen.iter_cases(seed, n, compile_fn=gen._compile_keymap,
                                     weighting=weighting):
        path = os.path.join(keymap_dir, "c%04d.xkb" % case["index"])
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        view = gen.parse_keymap(text)
        rc, out, err = run_judge(case, path, env)
        naive = gen.naive_stdout(view, keysyms, case["keysym_value"])
        if contrast is not None and len(contrast["items"]) < contrast["limit"] \
                and not (rc == 0 and naive.encode() == out):
            contrast["items"].append({
                "case": case,
                "judge_stdout": out.decode("utf-8", "replace"),
                "judge_rc": rc,
                "naive_stdout": naive,
                "naive_rc": 0,
            })
        rows = gen.parse_judge_rows(out.decode("utf-8", "replace"))
        records.append({
            "index": case["index"],
            "case_sha": hashlib.sha256(
                json.dumps(case, sort_keys=True).encode()).hexdigest(),
            "keymap_sha": view.sha256,
            "present_pool_size": case.get("present_pool_size"),
            "judge_rc": rc,
            "judge_out_sha": hashlib.sha256(out).hexdigest(),
            "judge_stdout_bytes": len(out),
            "judge_rows": len(rows),
            "judge_stderr_bytes": len(err),
            "naive_match": (rc == 0 and naive.encode() == out),
            "keysym_draw": case["keysym_draw"],
            "keysym_form": case["keysym_form"],
            "in_keymap": case["keysym_draw"].startswith("present"),
            "multi_layout": case["multi_layout"],
            "keysym_arg": case["keysym_arg"],
            "layout": case["layout"],
            "variant": case["variant"],
            "model": case["model"],
            "options": case["options"],
        })
        if not keep_keymaps:
            os.unlink(path)
    return records


def summarise(records):
    total = len(records)
    naive_ok = sum(1 for r in records if r["naive_match"])
    zero_rows = sum(1 for r in records if r["judge_rows"] == 0)
    rc0 = sum(1 for r in records if r["judge_rc"] == 0)
    single_plain = sum(1 for r in records
                       if r["judge_rc"] == 0 and r["judge_rows"] == 1)
    multi_row = sum(1 for r in records if r["judge_rows"] > 1)
    by_draw = {}
    for r in records:
        d = by_draw.setdefault(r["keysym_draw"], {"n": 0, "naive_ok": 0})
        d["n"] += 1
        d["naive_ok"] += 1 if r["naive_match"] else 0
    by_form = {}
    for r in records:
        d = by_form.setdefault(r["keysym_form"], {"n": 0, "naive_ok": 0})
        d["n"] += 1
        d["naive_ok"] += 1 if r["naive_match"] else 0
    return {
        "cases": total,
        "judge_rc0": rc0,
        "judge_rc_nonzero": total - rc0,
        "judge_zero_rows": zero_rows,
        "judge_single_row_rc0": single_plain,
        "judge_multi_row": multi_row,
        "naive_match": naive_ok,
        "naive_match_pct": round(100.0 * naive_ok / total, 1) if total else 0.0,
        "by_draw": by_draw,
        "by_form": by_form,
    }


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--seed", type=int, default=4901)
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--keep-keymaps", action="store_true")
    ap.add_argument("--weighting", choices=("difficulty", "plain"),
                    default="difficulty")
    ap.add_argument("--json-out", default=None)
    ap.add_argument("--tsv-out", default=None)
    ap.add_argument("--contrast-out", default=None)
    ap.add_argument("--contrast-n", type=int, default=3)
    args = ap.parse_args(argv)

    work = check_work(args.work)
    env = judge_env(work)
    if gen.sha256_file(gen.JUDGE_PATH) != gen.JUDGE_SHA256:
        raise SystemExit("judge_run.py: judge digest mismatch")
    if gen.sha256_file(gen.COMPILE_PATH) != gen.COMPILE_SHA256:
        raise SystemExit("judge_run.py: compile-keymap digest mismatch")
    keysyms = gen.load_keysyms()

    contrast = {"limit": args.contrast_n, "items": []} if args.contrast_out else None
    passes = []
    for run in range(args.runs):
        records = one_run(args.seed, args.n, work, env, keysyms, args.keep_keymaps,
                          weighting=args.weighting,
                          contrast=contrast if run == 0 else None)
        summary = summarise(records)
        digest = hashlib.sha256(
            "\n".join("%s %s %d" % (r["case_sha"], r["judge_out_sha"], r["judge_rc"])
                      for r in records).encode()).hexdigest()
        passes.append({"run": run + 1, "records": records,
                       "summary": summary, "digest": digest})
        print("run %d: weighting=%s cases=%d naive=%d/%d (%.1f%%) digest=%s"
              % (run + 1, args.weighting, summary["cases"], summary["naive_match"],
                 summary["cases"], summary["naive_match_pct"], digest[:16]))
        s = summary
        print("        rc0=%d rc_nonzero=%d zero_rows=%d single_row=%d multi_row=%d"
              % (s["judge_rc0"], s["judge_rc_nonzero"], s["judge_zero_rows"],
                 s["judge_single_row_rc0"], s["judge_multi_row"]))
        for name in sorted(s["by_draw"]):
            d = s["by_draw"][name]
            print("        draw=%-18s n=%-4d naive_ok=%d" % (name, d["n"], d["naive_ok"]))
        for name in sorted(s["by_form"]):
            d = s["by_form"][name]
            print("        form=%-8s n=%-4d naive_ok=%d" % (name, d["n"], d["naive_ok"]))

    digests = {p["digest"] for p in passes}
    print("determinism: %d distinct pass digests -> %s"
          % (len(digests), "STABLE" if len(digests) == 1 else "UNSTABLE"))
    if len(digests) != 1:
        return 1
    if args.contrast_out and contrast:
        with open(args.contrast_out, "w", encoding="utf-8") as fh:
            fh.write("# seed=%d n=%d weighting=%s\n" % (args.seed, args.n, args.weighting))
            fh.write("# first %d cases the naive reader gets wrong\n"
                     % len(contrast["items"]))
            for i, item in enumerate(contrast["items"], start=1):
                fh.write("\n## contrast %d\n" % i)
                fh.write("case %s\n" % json.dumps(item["case"], sort_keys=True))
                fh.write("--- judge stdout (rc=%d, %d bytes) ---\n"
                         % (item["judge_rc"], len(item["judge_stdout"])))
                fh.write(item["judge_stdout"])
                fh.write("--- naive stdout (rc=%d, %d bytes) ---\n"
                         % (item["naive_rc"], len(item["naive_stdout"])))
                fh.write(item["naive_stdout"])
                jl = item["judge_stdout"].splitlines()
                nl = item["naive_stdout"].splitlines()
                first = None
                for k in range(max(len(jl), len(nl))):
                    a = jl[k] if k < len(jl) else "<eof>"
                    b = nl[k] if k < len(nl) else "<eof>"
                    if a != b:
                        first = (k + 1, a, b)
                        break
                if first:
                    fh.write("--- first differing line %d ---\n" % first[0])
                    fh.write("judge: %s\n" % first[1])
                    fh.write("naive: %s\n" % first[2])
    if args.tsv_out:
        fields = ("index", "layout", "variant", "model", "options", "keysym_arg",
                  "keysym_draw", "keysym_form", "present_pool_size", "judge_rc",
                  "judge_rows", "naive_match", "judge_out_sha", "case_sha",
                  "keymap_sha")
        with open(args.tsv_out, "w", encoding="utf-8") as fh:
            fh.write("\t".join(fields) + "\n")
            for r in passes[0]["records"]:
                row = []
                for f in fields:
                    v = r[f]
                    if isinstance(v, list):
                        v = ",".join(v)
                    row.append(str(v))
                fh.write("\t".join(row) + "\n")
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump({"seed": args.seed, "n": args.n, "weighting": args.weighting,
                       "passes": passes}, fh,
                      indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
