# ExecHarmTip — no-harm check on the round's gates (base `a35cfdf` → data `1959770`)

Target attacked: **the round-43 no-harm claim** — the data commit `1959770657f1f8665097c1aed4be6c1cbb07139f` breaks no lane gate or
selftest that was green at base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`. Full tabulation `w2/ExecHarmTip/harm.txt`, narrative
`w2/ExecHarmTip/report.md`, transcripts + sha256 `w2/ExecHarmTip/logs/` (32 files). Two shared clones, each gate run at its own
revision; both clones verified `git rev-parse --show-toplevel` == clone root.

## Verdict: no harm, one declared and bounded exception

| # | gate | base | data | rc | class |
|---|---|---|---|---|---|
| 1 | `bash tools/mado-verify.sh --selftest` | 460/460 | 460/460 | 0→0 | unchanged, byte-identical output |
| 2 | `python3 -I tools/mado-options.py --selftest` | 211/211 | 211/211 | 0→0 | unchanged, byte-identical |
| 3 | `python3 -I tools/mado-globals.py --selftest` | 63/63 | 63/63 | 0→0 | unchanged, byte-identical |
| 4 | `python3 -I tools/mado-geometry.py --selftest` | absent | 73/73 | 2→0 | expected: new tool (data-only per assignment) |
| 5 | `python3 -I quality/check-index.py --rev <rev> --repo .` | 59/59, missing/dangling/dup 0, cov 10.0000/10 | 60/60, same | 0→0 | expected: new entry |
| 6 | `python3 -I quality/check-index-rows.py --rev <rev> --repo .` | rows=59 errors=0 warns=3 | rows=60 errors=0 warns=3 | 0→0 | expected: new entry, identical 3 warns |
| 7 | `python3 -I quality/check-axis-scores.py --rev <rev> --repo .` | 59/59, 63/63, 12/12 MATCH | nav 59/59 vs 60/60 STALE; calib 63/63 vs 68/68 STALE; oper MATCH | **0→1** | **red at data**; publication lag, closed at `2a3707c` |
| 8 | `python3 -I quality/check-locators.py --selftest` | absent | cases=18 passed, teeth PASS | 2→0 | expected: new gate |

`mado-verify.sh`'s flat 460 is correct: the script enumerates neither new tool (`grep -c mado-geometry` = 0, `grep -c check-locators` = 0).

## F1 (high) — the only red gate, and why it is not content harm

`SCORECARD.md`'s last publication at data is still the round-41 line (`:2521`: nav 59/59, calib 63/63), so the gate compares the base
values against a tree that already moved. Re-derived with the axes' own instruments at data: navigation 60/60 (`check-index.py`; +1 =
the new entry), calibration `active=68 resolved_active=68 fraction=1.0000` (`.ufo/waves/round-31/c2/count.py`; base 63/63; +5 =
criteria 76→81, appended at EOF in one hunk, criteria 1-76 byte-unchanged, all 63 old criteria still resolve because unresolved=0),
operability 12/12 (MATCH). At `a47efeb` still STALE rc 1; at `2a3707c` MATCH 60/60 · 68/68 · 12/12 rc 0, and `SCORECARD.md:2550`
publishes exactly those cells naming the data commit plus the records commit. Same two-phase precedent at `:2493` (r40) and `:2521`
(r41). So: real red gate in the window `[1959770, 2a3707c)`, declared by the lane's own publication protocol, and reconciling to the
digit. Residual for L1 (I do not edit `SCORECARD.md`): any consumer running the gate at the data commit itself gets exit 1.

## F2 (high) — no instrument was weakened; every doc change is append-only

`git diff --name-status base data -- quality/ tools/ corpus/ PROVINCE.md SKILL.md`: **no pre-existing instrument modified**. Four
additions under `quality/`+`tools/` (`check-locators.py`, both c2 counters, `mado-geometry.py`) and six `A` files total. Doc hunks are
pure appends: `PROVINCE.md` +1 row; `SKILL.md` 46 lines in 3 hunks (2 one-line rows at `:158`,`:225` + 44-line subsection
`:246-289`); `QUALITY.md` criteria 77-81 at EOF (single hunk `@@ -397,3 +397,13 @@`); `README.md` 1 index row + 1 frontier section;
`SOURCES.md` 8 new rows (S290-S297) with its only two deletions being the S155/S158 row tails (`' |'` → `', corpus/knowledge/
hyprland-gkeep-geometry-r43.md |'`, cell count 12→12, one opcode `replace` per row). `tools/mado-geometry.py` sha256
`e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99` on **both** sides of an independent hash (`git show
1959770:tools/mado-geometry.py` vs `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt`), so the new tool is the r42 reference byte for byte.

## F3 (medium) — supporting gates I ran beyond the eight

`quality/check-evidence-pointers.py --repo . --rev <rev> --branch <rev>`: rc 0 at both revs with a byte-identical verdict line
(`dangling_r36=0 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=1 … verdict=TARGET_MET`) → no dangling pointer, no dirty
inheritance, no new tracked scratch. `quality/counters/c1-r42-geometry.py --rev 1959770` → `fixtures=37/37 tool=present
verdict=TARGET_MET`; `quality/counters/c2-r43-gkeep-entry-v2.py --rev 1959770` → `admitted=1/1 verdict=TARGET_MET` (supporting the L1
receipts only; C1/C2 judgement belongs to their seats). Not run: `check-control-receipts.py`, `check-population.py`,
`counter-selftest.py`, `check-counter-discrimination.py`, `check-r38-discrimination.py` — each needs round-specific registry/manifest
arguments this assignment does not name, and none is a base-green gate the commit can flip.

## F4 (medium) — the new gate is green on the entry, red on the lesson by its own declared limit

`check-locators.py` has no repo-wide default (`[--fetch DIR] [--selftest] prose…`, `:376-379`). At data, with `--fetch
.ufo/waves/round-43/fetch`: entry `hyprland-gkeep-geometry-r43.md` **locators=10 miss=0**; `README.md`/`SOURCES.md` miss=0;
`lessons/round-43.md` **locators=22 miss=5** at `:115`, `:118`, `:124`, `:216`×2 — all prose that *quotes* the defective locators M43-1
records, quotes an `ExecLocatorGate` line about another tree, or ends a sentence whose identifiers sit on the previous line (the
`:29` "Identifier tokens are a proxy for the fact" limit). No base-green gate is affected, but a closure row must scope "locator gate
green" to the knowledge entry.

## Hygiene

Wrote only `w2/ExecHarmTip/` and this file; no tracked file edited; no `git`/`jj` mutation (checkout confined to my scratch clone,
read-only `show/diff/name-status/rev-parse` elsewhere); no `pacman`, no host service or compositor call; no fixtures; nothing installed.
Scratch `/fast/scratch/hyaku/mado-r43/ExecHarmTip/` deleted after its receipts were copied here.
