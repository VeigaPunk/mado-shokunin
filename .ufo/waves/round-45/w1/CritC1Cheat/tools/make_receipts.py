#!/usr/bin/env python3
"""Regenerate every CritC1Cheat receipt into the seat directory (so no receipt is hand-typed)."""
import difflib
import os
import shutil
import subprocess
import sys
import tempfile

S = os.path.dirname(os.path.abspath(__file__))
SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/w1/CritC1Cheat"
REC = os.path.join(SEAT, "receipts")
TOOLS = os.path.join(SEAT, "tools")
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality/counters/c1-r45-monitors.py")
BASE = "0c89478af821a6424c9ac922eafe02e39630cf4f"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}

sys.path.insert(0, S)
import gen_plus  # noqa: E402
import harness  # noqa: E402


def w(name, text):
    with open(os.path.join(REC, name), "w") as f:
        f.write(text)
    print("wrote receipts/%s (%d bytes)" % (name, len(text)))


def main():
    os.makedirs(REC, exist_ok=True)
    os.makedirs(TOOLS, exist_ok=True)
    work = tempfile.mkdtemp(dir=S, prefix="receipts-")

    # 0. diffs between the reference and each cheat
    ref = open(os.path.join(S, "ref.py")).read().splitlines(True)
    cheats = sorted(c for c in os.listdir(S) if c.startswith("cheat-") and c.endswith(".py"))
    out = []
    for c in cheats:
        d = difflib.unified_diff(ref, open(os.path.join(S, c)).read().splitlines(True),
                                 "ref.py", c, n=1)
        out.append("".join(d))
    w("diffs.txt", "".join(out))

    # 1. the reference on the frozen counter, two seeds
    d = harness.build(work, "REF", open(os.path.join(S, "ref.py")).read())
    lines = ["$ python3 -I %s --repo <clone of %s> --rev HEAD --work <scratch> --seed <n>" % (COUNTER, BASE)]
    for seed in (45, 7):
        rc, o = harness.score(d, work, seed)
        lines.append("REF seed=%d rc=%d" % (seed, rc))
        lines.append(o.strip().split("\n")[-1])
    w("score-ref.txt", "\n".join(lines) + "\n")

    # 2. every cheat on the frozen counter (default seed)
    lines = ["tool | rc | last line of the frozen counter (default seed 45)"]
    for c in cheats:
        d = harness.build(work, c[:-3], open(os.path.join(S, c)).read())
        rc, o = harness.score(d, work)
        lines.append("%-32s rc=%d %s" % (c, rc, o.strip().split("\n")[-1]))
    w("score-cheats.txt", "\n".join(lines) + "\n")

    # 3. differential probes
    p = subprocess.run([sys.executable, os.path.join(S, "probe.py")], capture_output=True, text=True)
    w("probes.txt", p.stdout)

    # 4. the diagnostic counter (frozen + 12 proposed fixtures) against REF and every cheat
    n = gen_plus.build_plus()
    lines = ["# diagnostic copy: frozen counter + %d proposed fixtures (%s)" % (n, gen_plus.PLUS),
             "# frozen fixtures: 49; the copy is scratch-only and is not installed"]
    tools = [("REF", "ref.py")] + [(c[:-3], c) for c in cheats]
    for name, path in tools:
        d = gen_plus.repo_for(open(os.path.join(S, path)).read(), name, work)
        rc, last, fails = gen_plus.score(gen_plus.PLUS, d, work)
        lines.append("%-32s rc=%d %s" % (name, rc, last))
        if fails:
            lines.append("%-32s FAILED: %s" % ("", ",".join(fails)))
    d = gen_plus.repo_for(open(os.path.join(S, "ref.py")).read(), "REF7", work)
    rc, last, fails = gen_plus.score(gen_plus.PLUS, d, work, 7)
    lines.append("%-32s rc=%d %s" % ("REF seed=7", rc, last))
    plus = open(gen_plus.PLUS).read()
    lines.append("")
    lines.append("# the 12 proposed fixture entries inserted before the frozen list's closing bracket:")
    start = plus.index('    ("setup-usage"')
    end = plus.index("\n]", start)
    lines.append(plus[start:end])
    w("plus-fixtures.txt", "\n".join(lines) + "\n")

    # 5. metamorphic environment check (proposal R1): same input, fixture env vs a real-looking env
    p = subprocess.run([sys.executable, os.path.join(S, "envcheck.py")], capture_output=True, text=True)
    w("env-metamorphic.txt", p.stdout + p.stderr)

    # 6. quote verification
    p = subprocess.run([sys.executable, os.path.join(S, "verify_quotes.py")], capture_output=True, text=True)
    w("quotes.txt", p.stdout + p.stderr)

    # 7. keep the tools and drivers with the receipts (they are this seat's own writes)
    for c in cheats + ["ref.py", "harness.py", "probe.py", "mkcheats.py", "gen_plus.py",
                       "envcheck.py", "verify_quotes.py", "buildA.py"]:
        shutil.copy2(os.path.join(S, c), os.path.join(TOOLS, c))
    print("copied %d files into tools/" % (len(cheats) + 8))
    return 0


if __name__ == "__main__":
    sys.exit(main())
