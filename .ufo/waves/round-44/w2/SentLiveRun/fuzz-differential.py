#!/usr/bin/env python3
"""fuzz-differential.py — round-43 tool vs the landed tool on the non-state path.

Generates random dumps whose `fullscreen` value is never a JSON integer 1 or 2 (absent,
0, bool, float, string, 3, -1), so the landed tool must take the round-43 path, and runs
both tools: stdout, stderr and exit code must be byte-identical for every case.

usage: python3 fuzz-differential.py --r43 R43.py --tool TOOL --rules RULES [--cases N]
"""
import argparse, hashlib, json, os, random, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--r43", required=True)
    ap.add_argument("--tool", required=True)
    ap.add_argument("--rules", required=True)
    ap.add_argument("--cases", type=int, default=400)
    ap.add_argument("--seed", type=int, default=44)
    a = ap.parse_args()
    rnd = random.Random(a.seed)
    tmp = os.path.join(HERE, ".fuzz-case.json")
    bad = []
    for i in range(a.cases):
        cs = []
        for _ in range(rnd.randint(0, 3)):
            c = {"mapped": rnd.choice([True, True, False]),
                 "floating": rnd.choice([True, False]),
                 "fullscreen": rnd.choice([0, 0, 0, None, True, 2.0, "2", 3, -1]),
                 "size": rnd.choice([[420, 500], [421, 500], [1720, 1414], None, [420],
                                     [420, 500, 1], ["420", 500], True]),
                 "class": rnd.choice(["org.omarchy.gkeep", "other", "org.omarchy.gkeep\x01", ""])}
            if c["fullscreen"] is None:
                del c["fullscreen"]
            cs.append(c)
        open(tmp, "w").write(json.dumps(cs))

        def run(tool):
            p = subprocess.run([sys.executable, "-I", tool, "--clients", tmp, "--rules", a.rules],
                               capture_output=True, timeout=60)
            return p.stdout, p.stderr, p.returncode
        x, y = run(a.r43), run(a.tool)
        if x != y:
            bad.append((i, cs, [b.decode() for b in x[:2]] + [x[2]],
                        [b.decode() for b in y[:2]] + [y[2]]))
    os.unlink(tmp)
    lines = ["round-43 vs landed differential: cases=%d seed=%d mismatches=%d"
             % (a.cases, a.seed, len(bad)),
             "r43 sha256=%s" % hashlib.sha256(open(a.r43, "rb").read()).hexdigest(),
             "landed sha256=%s" % hashlib.sha256(open(a.tool, "rb").read()).hexdigest(),
             "result: %s" % ("NON-STATE PATH BYTE-IDENTICAL (stdout, stderr, exit)"
                             if not bad else "MISMATCH")]
    if bad:
        lines.append(json.dumps(bad[0])[:1500])
    open(os.path.join(HERE, "differential.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
