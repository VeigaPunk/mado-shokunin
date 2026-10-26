#!/usr/bin/env python3
"""state-matrix.py — the landed tool over the state dumps and the live projection.

Records, for each fixture: verdict, the summary tokens that carry the state, and the
process exit code. Exit codes are captured from the child process, not from a shell tail.

usage: python3 state-matrix.py --tool TOOL --rules RULES [--dumps DIR] [--live FILE]
"""
import argparse, glob, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    ap.add_argument("--rules", required=True)
    ap.add_argument("--dumps", default=os.path.join(HERE, "state-dumps"))
    ap.add_argument("--live", default=os.path.join(HERE, "live-clients-projected.json"))
    ap.add_argument("--out", default=os.path.join(HERE, "state-matrix.txt"))
    a = ap.parse_args()
    rows = [("fixture", "rc", "verdict", "state tokens", "stderr")]
    files = sorted(glob.glob(os.path.join(a.dumps, "*.json")))
    for f in files + [a.live]:
        p = subprocess.run([sys.executable, "-I", a.tool, "--clients", f, "--rules", a.rules],
                           capture_output=True, timeout=60)
        last = p.stdout.decode().rstrip().splitlines()[-1]
        summary = last.split("MADO_GEOMETRY: ", 1)[-1]
        tok = summary.split()
        verdict = [t for t in tok if t.startswith("verdict=")][0].split("=", 1)[1]
        state = " ".join(t for t in tok if t.startswith(("maximized=", "fullscreen=",
                                                         "agree=", "differ=", "tiled=", "badsize=")))
        rows.append((os.path.basename(f).removesuffix(".json"), str(p.returncode), verdict, state,
                     repr(p.stderr.decode())))
    w = [max(len(r[i]) for r in rows) for i in range(5)]
    lines = ["  ".join(r[i].ljust(w[i]) for i in range(5)).rstrip() for r in rows]
    open(a.out, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
