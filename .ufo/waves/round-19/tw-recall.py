#!/usr/bin/env python3
"""Round-19 C3 counter: tripwire recall on the frozen real-incident lines.

Usage: tw-recall.py REV  -> one JSON object on stdout; exit 0 printed, 2 could-not-evaluate.

Fixed denominator (pinned at pre-registration, never re-derived from REV):
the (file, line) pairs named in the round-18 frozen baseline
`.ufo/waves/round-18/frozen/expected.json` at commit 9c54c56 — every
`expected_findings` line plus every `known_misses` line. Inputs are read from
that same commit and their sha256 must equal the pinned digests.

Numerator: incident lines on which `git show REV:tools/mado-tripwire.py`
(written to a temp dir, run with `python3 -I --scan`, cwd = temp snapshot)
reports at least one finding (any class, unpermitted or not).
score = 10 * detected / incident_lines.

Reads committed bytes only (`git show`); writes only a temp dir it removes.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile

LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PIN_REV = "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d"
FROZEN = ".ufo/waves/round-18/frozen"


def show(rev, path):
    p = subprocess.run(["git", "-C", LANE, "show", f"{rev}:{path}"], capture_output=True)
    if p.returncode != 0:
        raise SystemExit(f"could_not_evaluate: git show {rev}:{path} rc={p.returncode}")
    return p.stdout


def main():
    if len(sys.argv) != 2:
        print("usage: tw-recall.py REV", file=sys.stderr)
        return 2
    rev = sys.argv[1]
    p = subprocess.run(["git", "-C", LANE, "rev-parse", "--verify", rev + "^{commit}"],
                       capture_output=True, text=True)
    if p.returncode != 0:
        print(f"could_not_evaluate: rev {rev}", file=sys.stderr)
        return 2
    commit = p.stdout.strip()
    exp = json.loads(show(PIN_REV, f"{FROZEN}/expected.json"))
    incident = sorted({(f["file"], f["line"]) for f in exp["expected_findings"]}
                      | {(m["file"], m["line"]) for m in exp.get("known_misses", [])})
    tool = show(rev, "tools/mado-tripwire.py")
    with tempfile.TemporaryDirectory(prefix="mado-r19-recall-") as td:
        os.makedirs(os.path.join(td, "inputs"))
        paths = []
        for inp in exp["inputs"]:
            b = show(PIN_REV, f"{FROZEN}/{inp['path']}")
            if hashlib.sha256(b).hexdigest() != inp["sha256"]:
                print(f"could_not_evaluate: digest {inp['path']}", file=sys.stderr)
                return 2
            with open(os.path.join(td, inp["path"]), "wb") as fh:
                fh.write(b)
            paths.append(inp["path"])
        with open(os.path.join(td, "tool.py"), "wb") as fh:
            fh.write(tool)
        r = subprocess.run([sys.executable, "-I", "tool.py", "--scan", *paths],
                           cwd=td, capture_output=True, text=True)
        lines = r.stdout.splitlines()
        if r.returncode not in (0, 1) or len(lines) < 2:
            print(f"could_not_evaluate: scan rc={r.returncode}", file=sys.stderr)
            return 2
        verdict = json.loads(lines[1])
    hit = {(f["file"], f["line"]) for f in verdict.get("findings", [])}
    rows = [{"file": f, "line": n, "detected": (f, n) in hit} for f, n in incident]
    det = sum(r["detected"] for r in rows)
    print(json.dumps({
        "schema": "mado-tw-recall-r19-v1",
        "rev": rev,
        "commit": commit,
        "tool_sha256": hashlib.sha256(tool).hexdigest(),
        "pin_rev": PIN_REV,
        "incident_lines": len(rows),
        "detected": det,
        "score": round(10 * det / len(rows), 4),
        "rows": rows,
    }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
