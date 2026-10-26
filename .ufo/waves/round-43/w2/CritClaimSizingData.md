# CritClaimSizingData — report (mado round 43, w2, after the data commit 1959770657f1f8665097c1aed4be6c1cbb07139f)

STATUS: **complete**. Detailed findings, commands, outputs and receipts: `.ufo/waves/round-43/w2/CritClaimSizingData/findings.md`
plus eleven receipts in that seat dir (`receipt-commits`, `-tool-identity`, `-pointers`, `-check79`, `-counters`, `-axis-universals`,
`-counter-clauses`, `-v2-provenance`, `-quotes`, `-cleared`, `-quotes-verified`). Every quote in the findings is located and
machine-verified by `verify-quotes.sh` (27 checks, all OK, exit 0). No tracked file edited; no mutating git; no pacman; no
compositor verb; no tool installed (none needed). Scratch `/fast/scratch/hyaku/mado-r43/CritClaimSizingData/` removed at close.

Scope: re-attack the round's claim sizing after data (prompt §6 item 9; both verdicts). Read `registration.md`,
`registration-v2.md`, `w1/CritClaimSizing.md`, the committed receipts, the data commit's lesson/entry/QUALITY/README/PROVINCE/SKILL,
and the w1 reports the entry names (`ExecOracleGkeep`, `ExecGoalVsValue`, `ExecIndepA/B/C`, `ExecLiveHost`).

## Answers to the five assigned questions

1. **v2 frozen strictly before data — YES at commit level.** `496340d` (04:46:55) is the data commit's parent (04:53:45);
   the real entry and tool are ABSENT at `496340d`; the only entry-path files at the freeze are 32-line forgery fixtures
   (the genuine sample cites S050/S290-S299, not the round's ten rows). Qualification F6 below: the C1 tool's final bytes
   already sat at `tools/mado-geometry.py` in the worktree and had been run on the host 29 minutes before the freeze.
2. **Target reached by something other than the claimed work?** C1 **yes and v2 declares it** — the tool is byte-identical to
   the round-42 reference the lane held at BASE (`e3c2e471…`, both trees), so the move is installation, not authoring.
   C2 **no** — clause i+ forces all ten PINS, the pins are committed at the freeze and not in the data commit, the entry
   cites all ten, and both counters replay MET at data and at the tip.
3. **Is C1's "capability acquisition" honest?** Not as the corpus records it: `corpus/lessons/round-43.md:11` says "C1 lands
   … (operability, capability acquisition)" with no provenance; v2's mandated "reference installed as `tools/mado-geometry.py`,
   falsified by three independent implementations" appears only in the post-data LOG. The falsification itself is real (A/B/C).
4. **Universal clause the counter does not enumerate?** Yes, three: the seven pins vs round 42, "the only held-row edits", and
   "the entry and SKILL.md read locators=15 miss=0" (SKILL.md is never read by PRED-C2).
5. **Axis naming.** C2's moved surface is `corpus/README.md` (index row + Frontier bullet; PROVINCE moved only C1's tool row).
   The published coverage score is `coverage=10.0000/10` at base **and** at data, so the coverage axis does not move; the
   lesson's Axes sentence cites `axis-base.txt`, which enumerates three axes and not coverage.

## Findings (details + receipts in findings.md)

| # | sev | attack | one-line evidence | smallest correction |
|---|---|---|---|---|
| F1 | MEDIUM | lesson names four receipts, none present at `1959770`; two (`c1-after-tip.txt`, `c2-after-tip.txt`) exist at no revision; the round's own check79 prints `FAIL` on it and cannot see the two dead tip pointers (keyword-gated R2) | `receipt-pointers.txt`, `receipt-check79.txt` | land the two tip receipts (or drop the tip clause); widen check79's R2 gate |
| F2 | MEDIUM | the entry's oracle evidence (`ExecOracleGkeep/20-observation.txt`, `10-cases.txt`, `ExecGoalVsValue/finding.md`) was unlanded at the data commit; §4's only non-source OBS had no committed receipt there | `receipt-pointers.txt` | name the w1 receipts with commit `2a3707c` and shas |
| F3 | MEDIUM | C1 worded "capability acquisition" in the data commit's lesson, no provenance, against v2's required "installed … falsified by three independent implementations" | `receipt-tool-identity.txt`, `receipt-quotes.txt` | the report uses v2's sentence (still unwritten); any lesson append carries it |
| F4 | LOW/MED | three universal sentences the counter does not enumerate (pins vs round 42; the only held-row edits; SKILL.md locators) — all three hold at data, none is scored | `receipt-counter-clauses.txt`, `receipt-axis-universals.txt` | add the round-42 pin comparison to the closure; scope the held-row sentence; commit the locator output |
| F5 | LOW | coverage score unmoved (`10.0000/10` base and data); `axis-base.txt` has no coverage row; w1's LOW still holds at `1959770`, now in the durable lesson | `receipt-counters.txt`, `receipt-axis-universals.txt` | cite `check-index.py … coverage=10.0000/10` in the Axes sentence |
| F6 | LOW/MED | frozen v2 says the tool was "never installed, never run on the host as a tool of the lane"; its own committed receipt shows the run at 04:17:54 from `tools/mado-geometry.py` | `receipt-v2-provenance.txt` | the report states the true sequence |

## Verdicts

Both targets hold by replay at `1959770` and at `2a3707c` (`receipt-counters.txt`): C1 `fixtures=37/37 tool=present
verdict=TARGET_MET` (fresh nonces `1bdbe7e30d441225`, `10fd21bc58df93e7`), C2 v2 `admitted=1/1 verdict=TARGET_MET` (clauses
a-i all `:1`). Controls and predicates are untouched by the data commit (`git diff --stat 496340d 1959770 -- quality/counters
.ufo/waves/round-43/ctl .ufo/waves/round-43/registration*.md` empty). None of F1-F6 changes a verdict; all are record and
provenance corrections for the report and the closure. No predicate hole was found that data can still close.
