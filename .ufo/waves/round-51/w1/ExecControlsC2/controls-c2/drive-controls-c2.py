#!/usr/bin/env python3
"""Build and score the PRED-C2-r51 negative control fixtures.

Each control is a throwaway git commit in a sandbox clone of the lane: round base
`6ca8c559a4a3d6d361101592116eea2bc7452437` plus one overlay. A control is only ever a fixture
commit inside `--work`; the lane itself is cloned `--shared` and never mutated.

  ctl-a  r50 entry bytes at the C2 entry path (+ scaffold rows/pins/README row)
  ctl-b  r49 candidate bytes at the C2 entry path (+ same scaffold)
  ctl-c  authored fixture entry, held citations whose pinned tokens are ABSENT from the cited lines
  ctl-d  authored fixture entry, rows cited but NO pin files in the tree
  ctl-e  bare round base (entry absent) - the predicate's own base clause

Scoring:
  * `--counter PATH` (or the lane default `quality/counters/c2-r51-dispatch-entry.py` when it
    exists) is invoked as `python3 -I PATH --repo <fixture> --rev <fixture-rev>`; the exit code and
    final line are recorded.
  * `probe-clauses.py` always runs and records the measured clause vector (a-d).
  * `expected.json` states the required vector and verdict per control; a mismatch fails the run.

Scratch: `--work` is the only writable tree; it is removed on success unless `--keep` is passed.
TMPDIR is exported to `--work` for the counter.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROBE = os.path.join(HERE, "probe-clauses.py")
ENTRY = "corpus/knowledge/hyprland-dispatcher-dispatch-r51.md"
LANE_COUNTER = "quality/counters/c2-r51-dispatch-entry.py"

APPEND_MODES = {
    "SOURCES.md.frag": (r"^\| S\d{3,} \|", "corpus/SOURCES.md"),
    "README.md.frag": (r"^\| `knowledge/", "corpus/README.md"),
}


def run(cmd, cwd=None, env=None, check=True):
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SystemExit("command failed (%d): %s\n%s\n%s"
                         % (p.returncode, " ".join(cmd), p.stdout, p.stderr))
    return p


def git(fx, *args, check=True):
    return run(["git", "-C", fx] + list(args), check=check)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def insert_after_last_match(path, pattern, frag_path):
    lines = open(path, encoding="utf-8").read().splitlines(keepends=True)
    frag = open(frag_path, encoding="utf-8").read()
    if frag and not frag.endswith("\n"):
        frag += "\n"
    rx = re.compile(pattern)
    last = None
    for i, line in enumerate(lines):
        if rx.match(line):
            last = i
    if last is None:
        raise SystemExit("no insertion anchor %r in %s" % (pattern, path))
    lines[last + 1:last + 1] = [frag]
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return last + 2  # 1-based line of the first inserted line


def copy_tree(src, dst):
    if not os.path.isdir(src):
        return []
    added = []
    for root, _dirs, files in os.walk(src):
        rel = os.path.relpath(root, src)
        target_dir = dst if rel == "." else os.path.join(dst, rel)
        os.makedirs(target_dir, exist_ok=True)
        for name in sorted(files):
            s = os.path.join(root, name)
            t = os.path.join(target_dir, name)
            shutil.copy2(s, t)
            added.append(os.path.relpath(t, dst))
    return added


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="/home/vgpnk/Projects/shokunin/mado-shokunin")
    ap.add_argument("--base", default="6ca8c559a4a3d6d361101592116eea2bc7452437")
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True, help="receipt directory (seat-owned)")
    ap.add_argument("--fixtures", default=os.path.join(HERE, "fixtures"))
    ap.add_argument("--counter", default=None)
    ap.add_argument("--keep", action="store_true")
    args = ap.parse_args()

    repo = os.path.abspath(args.repo)
    work = os.path.abspath(args.work)
    out = os.path.abspath(args.out)
    fixtures = os.path.abspath(args.fixtures)
    os.makedirs(work, exist_ok=True)
    os.makedirs(out, exist_ok=True)
    config = json.load(open(os.path.join(fixtures, "controls.json")))
    expected = json.load(open(os.path.join(HERE, "expected.json")))

    env = dict(os.environ, TMPDIR=work)

    counter = args.counter
    if counter and not os.path.isfile(counter):
        raise SystemExit("--counter not found: %s" % counter)
    if not counter:
        lane_counter = os.path.join(repo, LANE_COUNTER)
        counter = lane_counter if os.path.isfile(lane_counter) else None

    fx = os.path.join(work, "fx")
    if os.path.exists(fx):
        shutil.rmtree(fx)
    run(["git", "clone", "-q", "--shared", repo, fx], env=env)
    toplevel = git(fx, "rev-parse", "--show-toplevel").stdout.strip()
    if toplevel != fx:
        raise SystemExit("TOPLEVEL-MISMATCH: %r != %r" % (toplevel, fx))
    git(fx, "checkout", "-q", "--detach", args.base)

    summary = []
    failures = []
    build_lines = ["# controls-c2 build receipt", "base=%s" % args.base,
                   "lane=%s" % repo, "work=%s" % work,
                   "counter=%s" % (counter or "ABSENT")]
    if counter:
        build_lines.append("counter_sha256=%s bytes=%d" % (sha256(counter),
                                                           os.path.getsize(counter)))
    build_lines.append("")

    for name in config["controls"]:
        spec = config["controls"][name]
        git(fx, "reset", "-q", "--hard", args.base)
        git(fx, "clean", "-fdxq")
        overlay = []
        inserts = []

        if not spec.get("base_only"):
            if spec.get("scaffold"):
                overlay += copy_tree(os.path.join(fixtures, "scaffold", "files"), fx)
                fetch_dir = os.path.join(fx, ".ufo/waves/round-51/fetch")
                if spec.get("pins", True) is False:
                    for rel in list(overlay):
                        if rel.startswith(".ufo/waves/round-51/fetch/"):
                            os.remove(os.path.join(fx, rel))
                            overlay.remove(rel)
                    if os.path.isdir(fetch_dir) and not os.listdir(fetch_dir):
                        os.rmdir(fetch_dir)
                    overlay_note = "pins=absent"
                else:
                    overlay_note = "pins=present"
                for frag_name, (pattern, target) in sorted(APPEND_MODES.items()):
                    frag = os.path.join(fixtures, "scaffold", "append", frag_name)
                    line = insert_after_last_match(os.path.join(fx, target), pattern, frag)
                    inserts.append("%s after-line=%d" % (target, line))
                    overlay.append(target)
            if spec.get("entry_from"):
                src = git(fx, "show", "%s:%s" % (args.base, spec["entry_from"])).stdout
                dest = os.path.join(fx, ENTRY)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "w", encoding="utf-8") as f:
                    f.write(src)
                overlay.append(ENTRY)
            if spec.get("reblock"):
                src = open(os.path.join(fixtures, "scaffold", "append",
                                        "entry-reblock.frag"), encoding="utf-8").read()
                block = src.rstrip("\n").splitlines()
                path = os.path.join(fx, ENTRY)
                kept, inserted = [], False
                for line in open(path, encoding="utf-8").read().splitlines():
                    if line.startswith(("source: ", "held: ", "held (")):
                        if not inserted:
                            kept.extend(block)
                            inserted = True
                        continue
                    kept.append(line)
                if not inserted:
                    kept.extend(block)
                kept.extend(open(os.path.join(fixtures, "scaffold", "append",
                                              "entry-reblock-manifest.frag"),
                                 encoding="utf-8").read().rstrip("\n").splitlines())
                with open(path, "w", encoding="utf-8") as f:
                    f.write("\n".join(kept) + "\n")
                inserts.append("entry-reblock.frag + entry-reblock-manifest.frag -> %s" % ENTRY)
            if spec.get("overlay"):
                overlay += copy_tree(os.path.join(fixtures, spec["overlay"], "files"), fx)

            git(fx, "add", "-A")
            git(fx, "-c", "user.name=control-fixture",
                "-c", "user.email=fixture@invalid", "commit", "-q",
                "-m", "control %s" % name)
            rev = git(fx, "rev-parse", "HEAD").stdout.strip()
        else:
            rev = git(fx, "rev-parse", "HEAD").stdout.strip()
            overlay_note = "base-only"

        lines = ["== %s rev=%s %s" % (name, rev, overlay_note)]
        for rel in sorted(set(overlay)):
            p = os.path.join(fx, rel)
            if os.path.isfile(p):
                lines.append("overlay %s %s" % (sha256(p), rel))
        for ins in inserts:
            lines.append("insert %s" % ins)

        if counter:
            cp = run([sys.executable, "-I", counter, "--repo", fx, "--rev", rev],
                     cwd=repo, env=env, check=False)
            clines = [l for l in cp.stdout.splitlines() if l.strip()]
            final = clines[-1] if clines else "(no output)"
            lines.append("counter rc=%d" % cp.returncode)
            lines += ["counter " + l for l in clines]
            if cp.stderr.strip():
                lines.append("counter stderr: %s" % cp.stderr.strip().splitlines()[-1])
            counter_verdict = "TARGET_MISSED" if "verdict=TARGET_MISSED" in final else (
                "TARGET_MET" if "verdict=TARGET_MET" in final else "UNKNOWN")
            counter_rc = cp.returncode
        else:
            lines.append("counter ABSENT (path=%s) - spec recorded only" % LANE_COUNTER)
            counter_verdict, counter_rc = "ABSENT", None

        pp = run([sys.executable, "-I", PROBE, "--repo", fx, "--rev", rev,
                  "--base", args.base, "--json"], env=env, check=False)
        plines = [l for l in pp.stdout.splitlines() if l.strip()]
        lines += ["probe " + l for l in plines]
        probefinal = next((l for l in plines if l.startswith("PROBE_C2_R51: ")), "")
        m = re.search(r"clauses_met=(\d) admitted=(\d)/1 verdict=(\w+)", probefinal)
        measured = {
            "clauses_met": int(m.group(1)) if m else None,
            "admitted": int(m.group(2)) if m else None,
            "verdict": m.group(3) if m else "UNKNOWN",
            "clauses": None,
            "max_overlap": None,
        }
        for l in plines:
            if l.startswith("PROBE_C2_R51-JSON: "):
                blob = json.loads(l.split(": ", 1)[1])
                measured["clauses"] = blob["clauses"]
                measured["max_overlap"] = blob["detail"]["c"]["max_overlap"]
        lines.append("probe rc=%d" % pp.returncode)

        exp = expected["controls"][name]
        for clause in "abcd":
            if measured["clauses"][clause] != exp["clauses"][clause]:
                failures.append("%s clause %s expected=%s measured=%s"
                                % (name, clause, exp["clauses"][clause], measured["clauses"][clause]))
        if measured["verdict"] != exp["verdict"]:
            failures.append("%s verdict expected=%s measured=%s"
                            % (name, exp["verdict"], measured["verdict"]))
        if pp.returncode != exp["probe_rc"]:
            failures.append("%s probe_rc expected=%d measured=%d"
                            % (name, exp["probe_rc"], pp.returncode))
        if counter and counter_verdict != exp["counter_verdict"]:
            failures.append("%s counter_verdict expected=%s measured=%s"
                            % (name, exp["counter_verdict"], counter_verdict))
        if counter and counter_rc != exp["counter_rc"]:
            failures.append("%s counter_rc expected=%d measured=%d"
                            % (name, exp["counter_rc"], counter_rc))

        with open(os.path.join(out, "%s.txt" % name), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        summary.append((name, rev, measured, counter_verdict, counter_rc))

    slines = ["# controls-c2 summary", "base=%s" % args.base,
              "counter=%s" % (counter or "ABSENT")]
    if counter:
        slines.append("counter_sha256=%s bytes=%d" % (sha256(counter),
                                                      os.path.getsize(counter)))
    slines.append("")
    for name, rev, measured, cverdict, crc in summary:
        cv = measured["clauses"] or {}
        vec = "".join("1" if cv.get(c) else "0" for c in "abcd")
        slines.append("%-6s clauses=%s met=%s max_overlap=%.4f verdict=%s probe_rc=%d counter=%s/%s rev=%s"
                      % (name, vec, measured["clauses_met"],
                         measured["max_overlap"] or 0.0, measured["verdict"],
                         0 if measured["admitted"] else 1, cverdict,
                         "-" if crc is None else crc, rev))
    slines.append("")
    slines.append("controls=%d matched=%d mismatched=%d verdict=%s"
                  % (len(summary), len(summary) - len(set(f.split()[0] for f in failures)),
                     len(set(f.split()[0] for f in failures)),
                     "OK" if not failures else "FAIL"))
    for f in failures:
        slines.append("MISMATCH: " + f)
    with open(os.path.join(out, "summary.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(slines) + "\n")
    with open(os.path.join(out, "build.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(build_lines) + "\n")

    print("\n".join(slines))
    git(fx, "checkout", "-q", "--detach", args.base, check=False)
    if not args.keep:
        shutil.rmtree(work, ignore_errors=True)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
