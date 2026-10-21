#!/usr/bin/env python3
"""Round-20 attempt-2 guard counter over the wave-2 adversarial fixtures.

Usage: a2-guards.py REV --fixtures-rev PIN

Reads `REV:tools/mado-tripwire.py` and the fixture bytes at PIN (`git show`
only), scans every fixture one file per process (`python3 -I --scan`, cwd =
temp) and prints one JSON object. Fixtures are data; nothing in them runs.

Metrics (populations frozen at PIN, each listed by file):
  recall_lost   files in the recall sets where 9c54c56 or 1f7f995 reports a
                row and REV reports none (declared exclusions listed apart)
  crash_flip    AdvCrash files where REV exits 2 and 1f7f995 does not
  pure_rows     the 24 AdvPureShapes fixtures AdvPureShapes named as pure
                data that still produce a row at REV
  vcs_fn/vcs_fp AdvVcsForms manifest truth vs REV (`write` missed / a
                measured non-write flagged); boundary cases are not scored
  a2_mismatch   a2/fixtures manifest truth (finding|write|clean) vs REV
  dup_rows      tool calls carrying both an observed and a lead row for the
                same (class, rule)
  slowest       the slowest REV scan (seconds) and its file
"""
import concurrent.futures
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time

LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
W2 = ".ufo/waves/round-20/w2/"
A2 = ".ufo/waves/round-20/a2/fixtures/"
BASES = {"pre_harm": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
         "harmed": "1f7f995caa25627db804e996cccd87fe38a3a1b6"}
RECALL_DIRS = (W2 + "AdvRecallShapes/fixtures/", W2 + "AdvDepth/silent-only/")
RECALL_PREFIX = ((W2 + "AdvLeadMarks/", "miss-"),)
RECALL_EXCLUDED = {  # declared by the seat that wrote them, before any repair
    W2 + "AdvRecallShapes/fixtures/gap04-lambda-argv-lead.jsonl": "old false positive (AdvRecallShapes)",
    W2 + "AdvRecallShapes/fixtures/ar49-signal-handler-lambda.jsonl": "signal-contingent (AdvRecallShapes)",
}
CRASH_DIRS = (W2 + "AdvCrash/fixtures/", W2 + "AdvCrash/fixtures2/")
PURE_IDS = ("ap01", "ap02b", "ap03", "ap04", "ap05", "ap06", "ap07", "ap08",
            "ap09", "ap10", "ap11", "ap14", "ap15", "ap16", "ap17", "ap18",
            "ap19", "ap20", "ap21", "ap23", "ap24", "ap25", "ap26", "ap27")
VCS_DIR = W2 + "AdvVcsForms/fixtures/"
TIMEOUT = 120


def git(*args, text=False):
    proc = subprocess.run(["git", "-C", LANE] + list(args), capture_output=True, text=text)
    if proc.returncode != 0:
        sys.exit("a2-guards: git %s failed: %s" % (" ".join(args), proc.stderr))
    return proc.stdout


def listing(pin, prefix):
    out = git("ls-tree", "-r", "--name-only", pin, "--", prefix, text=True)
    return sorted(p for p in out.splitlines() if p.endswith(".jsonl"))


def scan(tool, path, tmp):
    start = time.monotonic()
    try:
        proc = subprocess.run([sys.executable, "-I", tool, "--scan", path], cwd=tmp,
                              capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return {"exit": None, "rows": [], "seconds": TIMEOUT, "timeout": True}
    seconds = round(time.monotonic() - start, 3)
    rows = []
    lines = proc.stdout.splitlines()
    if len(lines) >= 2:
        try:
            payload = json.loads(lines[1])
            rows = [(f.get("line"), f.get("tool_call_id"), f["class"], f["rule"],
                     f.get("evidence", "observed")) for f in payload.get("findings", [])]
        except ValueError:
            pass
    return {"exit": proc.returncode, "rows": rows, "seconds": seconds, "timeout": False}


def main(argv):
    if len(argv) != 3 or argv[1] != "--fixtures-rev":
        sys.exit("usage: a2-guards.py REV --fixtures-rev PIN")
    rev = git("rev-parse", "--verify", argv[0] + "^{commit}", text=True).strip()
    pin = git("rev-parse", "--verify", argv[2] + "^{commit}", text=True).strip()
    tmp = tempfile.mkdtemp(prefix="a2-guards-")
    tools = {}
    for label, r in [("rev", rev)] + list(BASES.items()):
        data = git("show", "%s:tools/mado-tripwire.py" % r)
        path = os.path.join(tmp, "tw-%s.py" % label)
        open(path, "wb").write(data)
        tools[label] = (path, hashlib.sha256(data).hexdigest())

    recall = [p for d in RECALL_DIRS for p in listing(pin, d)]
    recall += [p for d, pre in RECALL_PREFIX for p in listing(pin, d)
               if os.path.basename(p).startswith(pre)]
    crash = [p for d in CRASH_DIRS for p in listing(pin, d)]
    pure = [p for p in listing(pin, W2 + "AdvPureShapes/fixtures/")
            if os.path.basename(p).split("-")[1] in PURE_IDS]
    vcs = listing(pin, VCS_DIR)
    a2 = listing(pin, A2)
    files = sorted(set(recall + crash + pure + vcs + a2))
    local = {}
    for p in files:
        dest = os.path.join(tmp, "fx", p)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "wb").write(git("show", "%s:%s" % (pin, p)))
        local[p] = dest

    jobs = [("rev", p) for p in files]
    jobs += [(b, p) for b in BASES for p in recall]
    jobs += [("harmed", p) for p in crash]
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futs = {pool.submit(scan, tools[label][0], local[p], tmp): (label, p)
                for label, p in jobs}
        for fut in concurrent.futures.as_completed(futs):
            results[futs[fut]] = fut.result()

    def rows(label, p):
        return results[(label, p)]["rows"]

    lost, excluded = [], []
    for p in recall:
        if any(rows(b, p) for b in BASES) and not rows("rev", p):
            (excluded if p in RECALL_EXCLUDED else lost).append(p)
    crash_flip = [p for p in crash if results[("rev", p)]["exit"] == 2
                  and results[("harmed", p)]["exit"] != 2]
    rev_exit2 = [p for p in crash if results[("rev", p)]["exit"] == 2]
    pure_rows = [p for p in pure if rows("rev", p)]

    def truths(prefix):
        raw = git("show", "%s:%smanifest.json" % (pin, prefix), text=True)
        return {c["case"]: c["truth"] for c in json.loads(raw)}

    vcs_truth = truths(VCS_DIR)
    vcs_fn, vcs_fp = [], []
    for p in vcs:
        truth = vcs_truth.get(os.path.basename(p)[:-6])
        write = any(r[2] == "vcs_write" for r in rows("rev", p))
        if truth == "write" and not write:
            vcs_fn.append(p)
        elif truth == "nowrite" and write:
            vcs_fp.append(p)
    a2_truth = truths(A2)
    a2_mismatch = []
    for p in a2:
        truth = a2_truth.get(os.path.basename(p)[:-6])
        got = rows("rev", p)
        ok = (bool(got) if truth == "finding" else
              any(r[2] == "vcs_write" for r in got) if truth == "write" else
              not got if truth == "clean" else False)
        if not ok or results[("rev", p)]["exit"] not in (0, 1):
            a2_mismatch.append(p)
    dup = []
    for p in files:
        seen = {}
        for line, call, cls, rule, ev in rows("rev", p):
            seen.setdefault((line, call, cls, rule), set()).add(ev)
        dup += ["%s:%s" % (p, k[0]) for k, evs in seen.items() if len(evs) > 1]
    slow_p = max(files, key=lambda p: results[("rev", p)]["seconds"])
    out = {
        "schema": "mado-r20-a2-guards-v1", "rev": rev, "fixtures_rev": pin,
        "tool_sha256": {k: v[1] for k, v in tools.items()},
        "populations": {"recall": len(recall), "crash": len(crash), "pure": len(pure),
                        "vcs": len(vcs), "a2": len(a2)},
        "recall_lost": len(lost), "recall_lost_files": lost,
        "recall_excluded": {p: RECALL_EXCLUDED[p] for p in excluded},
        "crash_flip": len(crash_flip), "crash_flip_files": crash_flip,
        "rev_exit2": len(rev_exit2),
        "pure_rows": len(pure_rows), "pure_rows_files": pure_rows,
        "vcs_fn": len(vcs_fn), "vcs_fn_files": vcs_fn,
        "vcs_fp": len(vcs_fp), "vcs_fp_files": vcs_fp,
        "a2_mismatch": len(a2_mismatch), "a2_mismatch_files": a2_mismatch,
        "dup_rows": len(dup), "dup_row_sites": dup,
        "timeouts": sorted(p for (label, p), r in results.items() if r["timeout"] and label == "rev"),
        "a2_seconds": {os.path.basename(p): results[("rev", p)]["seconds"] for p in a2},
        "slowest": {"file": slow_p, "seconds": results[("rev", slow_p)]["seconds"]},
    }
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
