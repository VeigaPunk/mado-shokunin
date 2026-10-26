#!/usr/bin/env python3
"""Differential driver: host hyprlang 0.6.8 (oracle.cpp) vs the C1 reference model (l1-draft/mado-devices.py).

Generates the corpus (gen.py), runs the C++ oracle once over a manifest, models the same configs with the
reference in-process (`parse_config` / `expected_names`), and compares per device name:
the five XKB names, kb_file, the pointer scroll factor (as printed with two decimals), block presence and the
special-category key order. Every mismatch on a case the reference does not itself mark `unsupported` is a
contract bug and is minimised by line deletion before being written to results.json.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/l1-draft/mado-devices.py"
NAMES = ("layout", "variant", "options", "model", "rules")


def load_ref():
    spec = importlib.util.spec_from_file_location("refdev", REF)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_case(root, case):
    d = os.path.join(root, case["id"])
    os.makedirs(d, exist_ok=True)
    paths = []
    for i, text in enumerate(case["files"]):
        p = os.path.join(d, "f%d.conf" % i)
        with open(p, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        paths.append(p)
    return paths


def run_oracle(root, oracle, cases):
    manifest = os.path.join(root, "manifest.txt")
    with open(manifest, "w", encoding="utf-8") as fh:
        for case in cases:
            paths = write_case(root, case)
            fh.write("CASE %s %d %d\n" % (case["id"], len(paths), len(case["names"])))
            for p in paths:
                fh.write(p + "\n")
            for n in case["names"]:
                fh.write(n + "\n")
    out = subprocess.run([oracle, "--manifest", manifest], capture_output=True, text=True, check=True).stdout
    res, cur = {}, None
    for line in out.splitlines():
        if line.startswith("BEGIN "):
            cur = line[6:]
            res[cur] = {"names": {}, "categories": None, "errors": 0}
        elif line.startswith("END "):
            cur = None
        elif cur is not None:
            obj = json.loads(line)
            if "categories" in obj:
                res[cur]["categories"] = obj["categories"]
                res[cur]["errors"] = obj["errors"]
            else:
                res[cur]["names"][obj["name"]] = obj
    return res


def ref_model(ref, case):
    st = ref.State()
    for text in case["files"]:
        ref.parse_config(text, st)
    out = {}
    for name in case["names"]:
        exp5, kbf = ref.expected_names(st, name)
        blk = st.devices.get(name, {})
        sf = min(max(blk["scroll_factor"], 0.0), 100.0) if "scroll_factor" in blk else -1.0
        out[name] = {"names": exp5, "kb_file": kbf, "sf": sf, "block": name in st.devices}
    return {"unsupported": st.unsupported, "blocks": list(st.devices.keys()), "names": out}


def compare(refm, orc):
    diffs = []
    if refm["blocks"] != orc["categories"]:
        diffs.append(("categories", None, refm["blocks"], orc["categories"]))
    for name, r in refm["names"].items():
        o = orc["names"].get(name)
        if o is None:
            diffs.append(("missing", name, r, o))
            continue
        got = (o["layout"], o["variant"], o["options"], o["model"], o["rules"])
        if tuple(r["names"]) != got:
            diffs.append(("names", name, list(r["names"]), list(got)))
        if r["kb_file"] != o["kb_file"]:
            diffs.append(("kb_file", name, r["kb_file"], o["kb_file"]))
        if ("%.2f" % r["sf"]) != o["sf"]:
            diffs.append(("scroll", name, "%.2f" % r["sf"], o["sf"]))
        if bool(r["block"]) != bool(o["block"]):
            diffs.append(("block", name, r["block"], o["block"]))
    return diffs


def compare_one(ref, oracle, root, case):
    orc = run_oracle(root, oracle, [case])[case["id"]]
    refm = ref_model(ref, case)
    if refm["unsupported"]:
        return refm, orc, None
    return refm, orc, compare(refm, orc)


def classify(case, diffs):
    return "+".join(sorted({d[0] for d in diffs}))


def minimize(ref, oracle, root, case, kind, rounds=10):
    """Greedy line/file deletion while the same divergence class survives."""
    cur = {"id": case["id"], "files": list(case["files"]), "names": list(case["names"])}
    changed = True
    while changed and rounds > 0:
        rounds -= 1
        changed = False
        cands = []
        for fi, text in enumerate(cur["files"]):
            for li in range(len(text.split("\n"))):
                c = {"id": cur["id"], "files": list(cur["files"]), "names": list(cur["names"])}
                lines = c["files"][fi].split("\n")
                del lines[li]
                c["files"][fi] = "\n".join(lines)
                if all(not t.strip() for t in c["files"]):
                    continue
                cands.append(("line", fi, li, c))
        for fi in range(len(cur["files"])):
            if len(cur["files"]) > 1:
                c = {"id": cur["id"], "files": [t for i, t in enumerate(cur["files"]) if i != fi],
                     "names": list(cur["names"])}
                cands.append(("file", fi, 0, c))
        if not cands:
            break
        sub = os.path.join(root, "min", "%s_%d" % (cur["id"], len(cands)))
        os.makedirs(sub, exist_ok=True)
        batch = []
        for i, (what, fi, li, c) in enumerate(cands):
            c = dict(c)
            c["id"] = "%s_m%d" % (cur["id"], i)
            batch.append(c)
        out = run_oracle(sub, oracle, batch)
        for i, (what, fi, li, c) in enumerate(cands):
            refm = ref_model(ref, batch[i])
            if refm["unsupported"]:
                continue
            diffs = compare(refm, out[batch[i]["id"]])
            if diffs and classify(batch[i], diffs) == kind:
                cur = {"id": case["id"], "files": c["files"], "names": c["names"]}
                changed = True
                break
    return cur


def main():
    root = sys.argv[1]
    oracle = sys.argv[2]
    n_clean = int(sys.argv[3]) if len(sys.argv) > 3 else 3200
    n_raw = int(sys.argv[4]) if len(sys.argv) > 4 else 400
    seed = int(sys.argv[5]) if len(sys.argv) > 5 else 46

    import gen

    ref = load_ref()
    cases = gen.generate(seed=seed, n_clean=n_clean, n_raw=n_raw)
    work = os.path.join(root, "corpus")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work, exist_ok=True)
    out = run_oracle(work, oracle, cases)

    total_lines = 0
    uns_total = 0
    compared = 0
    skipped = 0
    diverged = {}
    clean_lines = clean_uns = 0
    per_tag = {}
    for case in cases:
        refm = ref_model(ref, case)
        nonempty = sum(1 for t in case["files"] for line in t.split("\n") if line.strip())
        total_lines += nonempty
        uns_total += refm["unsupported"]
        if case["tag"] is None:
            clean_lines += nonempty
            clean_uns += refm["unsupported"]
        else:
            d = per_tag.setdefault(case["tag"], {"cases": 0, "lines": 0, "unsupported": 0, "declined": 0})
            d["cases"] += 1
            d["lines"] += nonempty
            d["unsupported"] += refm["unsupported"]
            d["declined"] += 1 if refm["unsupported"] else 0
        orc = out[case["id"]]
        if refm["unsupported"]:
            skipped += 1
            continue
        compared += 1
        diffs = compare(refm, orc)
        if diffs:
            text = "\n".join(case["files"])
            trig = []
            if re.search(r"^\s*\w+\s*=\s*$", text, re.M):
                trig.append("empty-name-line")
            if re.search(r"^device\[[^\]]*\]:", text, re.M):
                trig.append("bracket-line")
            if re.search(r"^device:name", text, re.M):
                trig.append("selector-line")
            if re.search(r"^\s*(unknown_key|nope)\s*=", text, re.M):
                trig.append("unregistered-key")
            if re.search(r"scroll_factor\s*=\s*[0-9.]+e-", text, re.M):
                trig.append("tiny-float")
            key = classify(case, diffs)
            diverged.setdefault(key, []).append({"id": case["id"], "tag": case["tag"], "diff": [list(d) for d in diffs],
                                                 "files": case["files"], "triggers": trig})
    minimal = {}
    if os.environ.get("MADO_MIN") == "1":
        for kind, items in diverged.items():
            minimal[kind] = []
            for item in items[:2]:
                case = {"id": item["id"], "files": item["files"], "names": [d[1] for d in item["diff"] if d[1]]}
                m = minimize(ref, oracle, root, case, kind, rounds=10)
                refm = ref_model(ref, m)
                sub = os.path.join(root, "final", item["id"])
                os.makedirs(sub, exist_ok=True)
                o = run_oracle(sub, oracle, [m])[m["id"]]
                minimal[kind].append({"id": item["id"], "files": m["files"], "names": m["names"],
                                      "unsupported": refm["unsupported"], "diffs": compare(refm, o)[:6]})

    summary = {
        "cases": len(cases),
        "compared": compared,
        "declined_by_reference": skipped,
        "config_lines": total_lines,
        "unsupported_increments": uns_total,
        "unsupported_share": (uns_total / total_lines) if total_lines else 0.0,
        "clean_lines": clean_lines,
        "clean_unsupported_increments": clean_uns,
        "divergence_cases": {k: len(v) for k, v in diverged.items()},
        "divergence_detail": {k: v[:6] for k, v in diverged.items()},
        "minimal": minimal,
        "per_tag": per_tag,
    }
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in summary.items() if k not in ("minimal", "divergence_detail")}, indent=1))
    for kind, items in minimal.items():
        print("== %s: %d minimal cases" % (kind, len(items)))
        for it in items:
            print("  ", it["id"], it["files"], "unsupported=%d" % it["unsupported"])
            print("   diffs:", it["diffs"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
