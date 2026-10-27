#!/usr/bin/env python3
"""Score one substituted ledger row with the r52 C1 counter. Scratch-only."""
import subprocess, sys, os, json

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "85d57a818c3707397e21c840b6498b105ba798aa"
COUNTER = LANE + "/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py"
S = "/fast/scratch/hyaku/mado-r52/Attack06"

base = subprocess.run(["git", "-C", LANE, "show", REV + ":quality/tool-ledger.md"],
                      capture_output=True, check=True).stdout.decode()

def run(name, path, row):
    lines = base.splitlines()
    hit = [i for i, l in enumerate(lines) if l.startswith("| `%s`" % path)]
    assert len(hit) == 1, (path, hit)
    lines[hit[0]] = row
    lp = os.path.join(S, "fixtures", name + ".md")
    with open(lp, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", LANE, "--rev", REV,
                        "--ledger", lp, "--work", S + "/work"],
                       capture_output=True, text=True)
    summ = [l for l in p.stdout.splitlines() if l.startswith("C1_R52:")][-1]
    det = [l for l in p.stdout.splitlines() if "%s" % path in l and l.startswith("detail:")]
    return {"case": name, "rc": p.returncode, "line": summ,
            "row_detail": det, "stderr": p.stderr.strip()[:200]}

CASES = []
def case(name, path, row):
    CASES.append((name, path, row))

P = "quality/check-tool-ledger.py"
case("00-production", P,
     "| `quality/check-tool-ledger.py` | Derives the tracked-instrument population at a revision and checks its accountability ledger. | `.ufo/waves/round-51/registration.md` |")
case("01-G-shaped-backtick-ledger-in-desc", P,
     "| `quality/check-tool-ledger.py` | Reads `quality/tool-ledger.md` and reports each instrument's accountability row. | `.ufo/waves/round-51/registration.md` |")
case("02-bare-ledger-in-desc", P,
     "| `quality/check-tool-ledger.py` | Reads quality/tool-ledger.md and reports each instrument's accountability row. | `.ufo/waves/round-51/registration.md` |")
case("03-bare-ledger-in-desc-province-ptr", P,
     "| `quality/check-tool-ledger.py` | Reads quality/tool-ledger.md and reports each instrument's accountability row. | `PROVINCE.md:118` |")
case("04-honest-paraphrase-A", P,
     "| `quality/check-tool-ledger.py` | Checks that every tracked instrument in the tool ledger has an accountable evidence pointer. | `PROVINCE.md:118` |")
case("05-honest-paraphrase-B", P,
     "| `quality/check-tool-ledger.py` | Derives the tracked-instrument population at a revision and checks every ledger row's accountability pointer. | `PROVINCE.md:118` |")
case("06-honest-paraphrase-C", P,
     "| `quality/check-tool-ledger.py` | Verifies the tool ledger is complete: one row per instrument, each with a resolvable pointer. | `PROVINCE.md:118` |")
case("07-own-header-sentence", P,
     "| `quality/check-tool-ledger.py` | check-tool-ledger.py -- PRED-C1-r51 gate: the tracked lane-level tool ledger is complete. | `PROVINCE.md:118` |")
case("08-honest-d4", P,
     "| `quality/check-tool-ledger.py` | Reads the tool ledger at one committed revision and reports each instrument's accountability row. | `PROVINCE.md:118` |")
case("09-terse-4-words", P,
     "| `quality/check-tool-ledger.py` | Checks the tool ledger. | `PROVINCE.md:118` |")
case("10-terse-5-words", P,
     "| `quality/check-tool-ledger.py` | Checks each tool ledger row. | `PROVINCE.md:118` |")
case("11-line-anchored-ledger-in-desc", P,
     "| `quality/check-tool-ledger.py` | Reads `quality/tool-ledger.md:9` and reports each instrument's accountability row. | `PROVINCE.md:118` |")
case("12-hash-anchored-ledger-in-desc", P,
     "| `quality/check-tool-ledger.py` | Reads `quality/tool-ledger.md#L9` and reports each instrument's accountability row. | `PROVINCE.md:118` |")

for name, path, row in CASES:
    r = run(name, path, row)
    print("== %-42s rc=%d" % (r["case"], r["rc"]))
    print("   " + r["line"].split("rev=")[0].strip())
    for d in r["row_detail"]:
        print("   " + d)
