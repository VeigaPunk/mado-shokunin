# ExecHarmTip — no-harm check, base `a35cfdf` → data `1959770` (round 43, hyaku run 8, w2)

Target: **the round's no-harm claim** — that the data commit `1959770657f1f8665097c1aed4be6c1cbb07139f` breaks no lane gate or
selftest that was green at the base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`. Method: two shared clones of the lane
(`/fast/scratch/hyaku/mado-r43/ExecHarmTip/base.g0K5` @base, `data.vVb1` @data, both `git rev-parse --show-toplevel` == clone root),
each of the eight assigned commands executed at its own revision, then re-derivation at the two later commits for the one red gate.
Tabulation of all eight rows is `w2/ExecHarmTip/harm.txt`; every transcript is a copy under `w2/ExecHarmTip/logs/` with its sha256.

## Verdict

**No harm to any base-green gate**, with one bounded, *declared* exception: `quality/check-axis-scores.py` exits 1 at the data commit
(2 of 3 axis rows STALE) because the lane's axis publication rides the *later* records commit. That is true at the data commit, false
again at `2a3707c` (60/60 and 68/68 MATCH, rc 0), and the numbers the gate prints at data are exactly the two additions the round
declares — not a miscount, not a content defect. Everything else that moved is a new file whose own gate is green, or a count that grew
by the one item added (index 59→60 rows; SOURCES 226→234 rows).

## The eight assigned gates, base → data

| # | command | base @`a35cfdf` | data @`1959770` | rc | class |
|---|---|---|---|---|---|
| 1 | `bash tools/mado-verify.sh --selftest` | 460/460 assertions passed | 460/460 assertions passed | 0→0 | unchanged (byte-identical output) |
| 2 | `python3 -I tools/mado-options.py --selftest` | 211/211 passed | 211/211 passed | 0→0 | unchanged (byte-identical) |
| 3 | `python3 -I tools/mado-globals.py --selftest` | 63/63 passed | 63/63 passed | 0→0 | unchanged (byte-identical) |
| 4 | `python3 -I tools/mado-geometry.py --selftest` | absent | 73/73 passed | 2→0 | expected: **new tool** |
| 5 | `python3 -I quality/check-index.py --rev <rev> --repo .` | 59/59, missing 0 dangling 0 dup 0, coverage 10.0000/10 | 60/60, same four flags | 0→0 | expected: **new entry** (+1) |
| 6 | `python3 -I quality/check-index-rows.py --rev <rev> --repo .` | rows=59 errors=0 warns=3 | rows=60 errors=0 warns=3 | 0→0 | expected: **new entry**; the same 3 warns on the same 3 round-12/round-24 rows |
| 7 | `python3 -I quality/check-axis-scores.py --rev <rev> --repo .` | nav 59/59 · calib 63/63 · oper 12/12, mismatched=0 | nav published 59/59 vs derived 60/60 STALE · calib 63/63 vs 68/68 STALE · oper 12/12 MATCH, mismatched=2 | **0→1** | **red at the data commit**; expected-by-protocol, closed at `2a3707c` |
| 8 | `python3 -I quality/check-locators.py --selftest` | absent | cases=18 passed=18, locators=19 miss=6, teeth PASS | 2→0 | expected: **new gate** |

`mado-verify.sh`'s flat 460 is correct, not a missed growth: the script contains zero occurrences of either new tool
(`grep -c mado-geometry tools/mado-verify.sh` = 0, `grep -c check-locators …` = 0 at data).

## F1 — the one red gate: axis publication lag (expected, bounded, measured)

`check-axis-scores.py` parses the **last** `Axis table re-derived at` line of `SCORECARD.md`. At the data commit that is still the
round-41 line (`SCORECARD.md:2521` @`1959770`: *"…navigation 59/59; calibration resolved-active 63/63; operability selftest 12/12"*),
i.e. the base values, while the tree has already moved. Re-deriving each half with the axis's own instrument at `1959770`:

- navigation — `check-index.py` → `indexed=60/60`; the +1 is the new knowledge entry (gate 5).
- calibration — `.ufo/waves/round-31/c2/count.py 1959770` → `METRIC active=68 resolved_active=68 fraction=1.0000 verdict=TARGET_MET`;
  at base `active=63 resolved_active=63 fraction=1.0000`. +5 = criteria **76→81** in `corpus/QUALITY.md`, appended at EOF in one hunk
  (`git diff -U0` shows a single `@@ -397,3 +397,13 @@` — criteria 1-76 byte-unchanged). Because `unresolved_active=0` at data, all
  63 pre-existing criteria still resolve: no old grounding was traded for the new five.
- operability — `check-index.py --selftest` → 12/12 at both revisions (so this row is MATCH at data, not stale).

Re-derivation at the later commits: `a47efeb` (after-data receipts) still STALE, rc 1 → the lag spans the whole w1 wave;
`2a3707c` (round-43 records) MATCH 60/60, 68/68, 12/12, rc 0, and its `SCORECARD.md:2550` publishes
*"navigation 60/60; calibration resolved-active 68/68"* naming the data commit plus the records commit — the published cells equal my
derived cells **to the digit**. The same two-phase shape is the lane's own precedent (`SCORECARD.md:2493` round-40, `:2521` round-41
"plus the … records commit"). So the difference is declared, transient, and reconciles exactly.

Residual I do *not* fix (L1 owns `SCORECARD.md`): a consumer running the gate at the data commit itself gets exit 1, and the honest
range for "all gates green" is `2a3707c` onward, not the data commit.

## F2 — structural evidence that no instrument was weakened

`git diff --name-status a35cfdf 1959770 -- quality/ tools/ corpus/ PROVINCE.md SKILL.md` shows **no pre-existing checker, counter or
tool modified** — four `A` under `quality/`+`tools/`, six `A` files total, and five docs whose every hunk is append-only
(`PROVINCE.md` +1 row; `SKILL.md` 46 lines in 3 hunks = 2 one-line rows `:158`,`:225` + a 44-line subsection `:246-289`;
`QUALITY.md` criteria 77-81 at EOF; `README.md` 1 index row + 1 frontier section; `SOURCES.md` 8 new rows, and its only two
deletions are the row tails of S155/S158 replacing `' |'` with `', corpus/knowledge/hyprland-gkeep-geometry-r43.md |'` — cell count
12→12, one used-by item appended, nothing else in either row: an opcode diff yields exactly one `replace` per row).
`tools/mado-geometry.py` hashes **e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99** on both sides of an independent
comparison (`git show 1959770:tools/mado-geometry.py | sha256sum` vs `sha256sum .ufo/waves/round-42/c1/ctl-ref-tool.py.txt`), so the
new tool is the round-42 reference byte for byte — it can change nothing it does not run.

## F3 — supporting gates run beyond the eight (same code path, read-only)

- `quality/check-evidence-pointers.py --repo . --rev <rev> --branch <rev>`: rc 0 at **both** revs, byte-identical verdict line —
  `pointers_r35=8 … dangling_r36=0 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=1 setup=ok verdict=TARGET_MET`.
  So the data commit adds no dangling pointer, no inherited dirty file, no tracked scratch.
- `quality/counters/c1-r42-geometry.py --rev 1959770` → `fixtures=37/37 tool=present verdict=TARGET_MET`, rc 0.
- `quality/counters/c2-r43-gkeep-entry-v2.py --rev 1959770` → `admitted=1/1 verdict=TARGET_MET`, rc 0.
  Both support the L1 receipts; judgement of C1/C2 belongs to their seats, not to me.
- Not run, with reason: `check-control-receipts.py`, `check-population.py`, `counter-selftest.py`, `check-counter-discrimination.py`,
  `check-r38-discrimination.py` require round-specific registry/manifest/registration/counter arguments that this assignment does not
  name; none is a base-green gate the data commit can flip, since its inputs are per-round registries the commit does not create.

## F4 — the new gate applied to the commit it arrives with (bounded observation, not a harm)

`quality/check-locators.py` has no repo-wide default (`usage: [--fetch DIR] [--selftest] prose…`, `check-locators.py:376-379`). Driven
over the round's own prose with `--fetch .ufo/waves/round-43/fetch` at `1959770`:

- `corpus/knowledge/hyprland-gkeep-geometry-r43.md` — `locators=10 miss=0`, rc 0 (the added knowledge entry is clean);
- `corpus/README.md` — `locators=0 miss=0`; `corpus/SOURCES.md` — `locators=0 miss=0`;
- `corpus/lessons/round-43.md` — `locators=22 miss=5`, rc 1, at `:115`, `:118`, `:124`, `:216` (twice).

All five misses are the checker's declared line-local attribution meeting prose that **quotes** a defective locator: `:115`/`:118` are
the pre-fix locators lesson M43-1 exists to record (`fragments=3 supported=1` on `:115`), `:124` quotes an `ExecLocatorGate` output line
about a different tree (`LOG-a35cfdf.md`), and the two on `:216` close a sentence whose identifiers sit on the preceding line
(NOFRAG-class continuation). This turns no base-green gate red — the tool does not exist at base — but a closure row may not claim the
locator gate is "green across the round's prose": green means *the knowledge entry*, 10/10 locators, 0 miss.

## Scope, safety, and hygiene

Writes: only `w2/ExecHarmTip/` (`harm.txt`, `report.md`, `logs/`) and this file. No tracked file edited; no `git`/`jj` mutation
anywhere (clone/checkout inside my own scratch clone, read-only `git show/diff/name-status/rev-parse` elsewhere). No `pacman`, no host
service or compositor call — the run needed no live `hyprctl` (the live tool run is the C1 seat's receipt, not mine). Fixtures: none
created. Scratch `/fast/scratch/hyaku/mado-r43/ExecHarmTip/` removed at the end; all receipts copied to the seat dir first. Tools
installed: none (system `python3`, `git`, `bash`, `sha256sum`).
