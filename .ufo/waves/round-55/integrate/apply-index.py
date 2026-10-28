#!/usr/bin/env python3
"""L1 integration (round 55): applies the R55ScribeIndex drafts (README coverage row, errata row, Frontier bullets, PROVINCE
paragraph, tool-ledger rows) with the L1's corrections (sources cell, harness-module ledger rows). Run from the lane root."""
import re
D = ".ufo/waves/round-55/w1/R55ScribeIndex/"
def body(f, skip=2):
    return open(D + f).read().split("\n")[skip:]
# README ---------------------------------------------------------------------------------------------------------
rd = open("corpus/README.md").read().split("\n")
cov = [l for l in body("01-coverage-row.md") if l.startswith("| `knowledge/hyprland-keyboard")][0]
cov = cov.replace("S052, S162, S215, S316–S319 (held) and S378–S380 (opened 2026-10-28)", "S052, S316, S317, S318, S319 (held) and S378–S380 (opened 2026-10-28)")
err = [l for l in body("03-errata-row.md") if l.startswith("| `knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`")][0]
i = [n for n, l in enumerate(rd) if l.startswith("| `knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`")]
assert len(i) == 1
rd[i[0]] = err
rd.insert(i[0] + 1, cov)
bul = [l for l in body("02-frontier-bullets.md") if l.startswith("- Round 55")]
j = [n for n, l in enumerate(rd) if l.strip() == "## Frontier"]
assert len(j) == 1
rd[j[0] + 2:j[0] + 2] = bul
open("corpus/README.md", "w").write("\n".join(rd))
# PROVINCE -------------------------------------------------------------------------------------------------------
para = [l for l in body("05-province-round55.md") if l.startswith("**Round-55 refinement")][0]
pv = open("PROVINCE.md").read().rstrip("\n")
open("PROVINCE.md", "w").write(pv + "\n\n" + para + "\n")
# ledger ---------------------------------------------------------------------------------------------------------
rows = {re.match(r"\| `([^`]+)`", l).group(1): l for l in body("06-ledger-rows.md", 0) if l.startswith("| `")}
for m in ("c1", "c2", "c3"):
    rows["quality/r55_ctl_%s.py" % m] = ("| `quality/r55_ctl_%s.py` | Round-55 control-harness module for claim %s (loaded by `quality/check-r55-controls.py`): runs the claim's counter or tool as a child process and prints its `MADO_R55_*` line; writes only under `--work`. | `quality/check-r55-controls.py` |" % (m, m.upper()))
lg = open("quality/tool-ledger.md").read().split("\n")
for path, row in sorted(rows.items()):
    lg.append(row)
open("quality/tool-ledger.md", "w").write("\n".join(lg).rstrip("\n") + "\n")
print("README rows", len(rd), "ledger rows added", len(rows))
