# R79MutC1 — C1 counter mutation audit (seat report)

Seat: R79MutC1 (mutation-tester, leaf — no subagents). Date: 2026-11-04.
Subject under mutation: the **counter** `quality/counters/c1-r79-reserve.py` (frozen; mutated only in scratch copies).
Freeze `5eb8f20fe291603c74973fa94cc55723ac8089a4`, base `e4b153dfa4a67ca56f7ec65cb6639082451626a7`.
Pristine baseline at the freeze: frozen receipt `.ufo/waves/round-79/receipts/measurement-c1-r79.txt`
(copied to `runs/` sibling `receipts/` in this dir) — `correct=23 killed=12 base_correct=18/23 carried=18/18
tool_selftest=43/43 verdict=TARGET_MET` rc 0; `tool_sha256=c9aa139152643020acf27b5aef8026ae5b8a5f70372e86abb4a032c82bed86de`
re-verified from `git show 5eb8f20…:tools/mado-barfoot.py` before mutating. Base control receipt
(`control-c1-r79-at-base.txt`, copied) — `correct=18 killed=4 verdict=TARGET_MISSED` rc 1.

Method: single-anchor mutations applied to a scratch copy of the counter; each mutant re-run with the frozen
counting command shape (`--controls .ufo/waves/round-79/controls/c1-cases-r79.json --carried …/c1-cases-r78.json`,
scratch root under `/fast/scratch/hyaku/mado-r79/R79MutC1/`, full outputs in `runs/out-<tag>.txt` here).
Counter anchor lines (frozen file, unchanged): carried check `:315-317`, verdict-only target clause `:354-355`,
anchor-absent branch `:335-338`, refusal stage pin `:156-157`, expectation comparison `:163`, selftest clause `:323`.

## 1. Counter mutants vs the freeze — survivors are the counter's holes

| counter-mutant (anchor) | still TARGET_MET? | observed verdict line (rc) | the check that would have caught it — probe evidence |
|---|---|---|---|
| carried-prefix-dropped (`:315-317`) | **YES — survivor** | `correct=23 … killed=12 … verdict=TARGET_MET` (0), `runs/out-freeze-M1-carried-dropped.txt` | Any drift of the 18 carried cases. Probe: carried r78 copy with case 0 renamed (`host-top` → `host-top-tampered`): pristine → rc 2 `ERROR (stage=setup the successor set does not carry the frozen round-78 cases unchanged)`; mutant → rc 0 `TARGET_MET` (`out-probeA-*`). Catcher: carried case `host-top` (any carried byte; expectation tampering is separately caught by `correct<23`). |
| base-correct-accepted (`:354`) | **YES — survivor** | `correct=23 … base_correct=23/23 … verdict=TARGET_MET` (0) with `--base-rev 5eb8f20…` — the MET line itself carries the violated clause, `out-freeze-M2-base-accepted.txt` | The do-nothing control. Probe: base rev pointed at the freeze (base tool = successor tool): pristine → rc 1 `TARGET_MISSED` with `base_correct=23/23` (`out-probeB-pristine-base-is-freeze.txt`); mutant → rc 0 `TARGET_MET`. |
| anchor-absent-as-killed (`:335-338`) | **YES — survivor** (branch dead at the freeze: all 12 anchors present) | identical MET line to pristine (`out-freeze-M3-anchor-absent-killed.txt`) | Nothing at the freeze. At base: pristine `killed=4` vs mutant `killed=12` (`out-probeC-*`), both `TARGET_MISSED` — `correct=18` decides, so no verdict flips anywhere; the before-state `killed` measurement silently corrupts 4→12. |
| refusal-stage-pin-dropped (`:156-157`) | **YES — survivor** | MET (0), `out-freeze-M4-stage-pin-dropped.txt` | A wrong-stage refusal. Probe: scratch-fixture rev with the tool's model-refusal literal flipped `stage=model`→`stage=setup` (`tools/mado-barfoot.py:853`): pristine → rc 1 `TARGET_MISSED`, `correct=20` — cases `dynamic-cross`, `negative-margin-refused`, `static-source-refused` all fail the stage pin; mutant → rc 0 `TARGET_MET`, `correct=23` (`out-probeD-*`). Catchers: the three `stage=model` refusal cases. |
| verdict-only-comparison (`:163`) | no — killed by the counter's own battery | rc 1 `killed=10 … verdict=TARGET_MISSED`, `out-freeze-M5a-verdict-only.txt` | n/a (not a hole). Surviving tool mutants under verdict-only scoring: `opposite-margin-dropped` and `static-dropped` — their killers flip `expected`/`reserved` while `verdict` stays `CLEAN`. |
| ignore-band-expected-only (`:163`) | **YES — survivor** (latent) | MET (0) with `killed=12` — byte-identical behavior to pristine at the freeze, `out-freeze-M5b-ignore-band-expected.txt` | Latent hole: no mutant in today's battery is separated solely by `band`/`expected` (static-dropped's killers keep `reserved` on 2/3 cases; opposite-margin-dropped keeps `reserved` on all 10). `band`/`expected` are currently not load-bearing in the verdict — defended only indirectly. |
| red-selftest-accepted (`:323`) | **YES — survivor** | MET (0), `out-freeze-M6-red-selftest-accepted.txt` | A red tool selftest. Probe: scratch-fixture rev printing `MADO_BARFOOT_SELFTEST: 43/44` (`tools/mado-barfoot.py:814` doctored): pristine → rc 1 `TARGET_MISSED`; mutant → rc 0 `TARGET_MET` with `tool_selftest=43/44` printed inside the MET line (`out-probeE-*`). Catcher: the selftest clause itself — no case catches it. |

**Score: 5 hard survivors with demonstrated holes** (carried-prefix, base-correct, anchor-absent, stage-pin, red-selftest)
plus 1 latent (band/expected not load-bearing); the full verdict-only mutant is killed by the mutant battery.
All probes used the frozen bytes elsewhere; probe revs live only in the deleted scratch fixture repo
(`p1-stage-setup b8fe73c0…`, `p2-red-selftest 6cde7063…`, base `30299f03…`).

## 2. The twelve tool mutants — separation audit (per-case differential, counter's own `run_cases`)

All 12 killed at the freeze (killed=12 confirmed). Killer case = a case the pristine tool passes and the mutant fails.

| tool-mutant | killer case(s) [flipped expect fields] | sole separator? | kill class |
|---|---|---|---|
| opposite-margin-dropped | 10: top-margin-int, top-margin-css-2, top-margin-asym, bottom-margin, left-margin, right-margin, width-with-margins, static-composed [expected+reserved]; second-consumer, reserved-differ [expected] | no | composition fields; robust |
| horizontal-margin-leak | 10: same margin set, most [expected+rc+reserved+verdict] | no | robust |
| level-bottom-swap | layer-bottom [band+box+expected+rc+reserved+verdict] | **SOLE** | the layer case is a single point of failure |
| right-extent-flip | right-margin, right-zero-margin [expected+rc+reserved+verdict] | no (2) | right-edge cases |
| per-side-margin-dropped | top-margin-asym [box+expected+rc+reserved+verdict] | **SOLE** | single point of failure |
| negative-margin-accepted | negative-margin-refused [rc 3 refusal guard] | **SOLE** | **killed only by a refusal** — composition semantics never see a negative margin; if the guard case moved, this anchor is unguarded |
| opposite-edge-wrong | top-margin-asym [rc+reserved+expected+verdict] | **SOLE** | shares its separator with per-side-margin-dropped (double duty on one case) |
| static-dropped | static-composed [reserved+expected], static-exclusive-false [expected], static-last-wins [reserved+expected] | no (3) | new-term cases |
| static-order-swapped | static-composed, static-exclusive-false, static-last-wins [rc+box+…] | no (3) | new-term cases |
| static-first-wins | static-composed, static-other-edge, static-exclusive-false, static-last-wins [rc+box+…] (correct=19/23 today; frozen receipt line says 22/23 — see finding 3) | no (4 today) | new-term cases |
| static-box-unoffset | static-composed, static-other-edge, static-exclusive-false, static-last-wins [rc+box+…] | no (4) | new-term cases |
| static-selector-ignored | static-last-wins [rc+box+reserved+expected+verdict] | **SOLE** | the last-wins case is the only guard for the selector anchor |

Full data: `part3.json` in this dir. Mechanism note for static-first-wins: the mutant
(`c1-r79-reserve.py` MUTATIONS, applied at `tools/mado-barfoot.py:374` → first-wins form `:376`) makes the
tool print `MADO_BARFOOT_STATIC: monitor=M1 top=0 right=0 bottom=0 left=0` (rc 1) on `static-composed` —
the kept slot is a zero/earlier slot, so single-rule static cases over-die (a stricter kill, not a hole).

Named answers to the seat question:
- **Killed only by a refusal:** `negative-margin-accepted` (sole killer `negative-margin-refused`, rc 3 guard).
- **Killed only by an unrelated field:** none — every killer flips composition-relevant fields (expected/reserved/box/rc).
- **Sole separators:** `layer-bottom`, `top-margin-asym` (×2 mutants), `negative-margin-refused`, `static-last-wins`
  (the last-wins case is the only guard for `static-selector-ignored`, and per the frozen receipt also for `static-first-wins`).

## 3. Findings (data; counter/instrument files untouched)

1. **Five counter holes, all verdict-level at the freeze.** Dropping the carried-prefix check
   (`c1-r79-reserve.py:315-317`), accepting `base_correct != 18` (`:354`), counting an absent anchor as killed
   (`:335-338`), dropping the refusal stage pin (`:156-157`), and accepting a red tool selftest (`:323`) each still
   print `verdict=TARGET_MET` rc 0 against the freeze. Each hole was demonstrated with a minimal probe
   (tampered carried copy / base-rev=freeze / base-rev run / wrong-stage probe rev / red-selftest probe rev);
   pristine counter fails every probe, the mutant passes. These clauses are currently validated only by the
   before-state runs and by code review, not by any freeze-time differential.
2. **`band`/`expected` are not load-bearing.** A counter that ignores them still prints `killed=12 … TARGET_MET`
   at the freeze (`out-freeze-M5b-*`); only a full verdict-only comparison trips the battery (`killed=10`:
   `opposite-margin-dropped`, `static-dropped` survive). A future tool mutant separated solely by band/expected
   numbers would pass the current 12-mutant battery under such a counter.
3. **Receipt divergence (verdict-neutral):** frozen `receipts/measurement-c1-r79.txt` line
   `MADO_R79_MUTANT: name=static-first-wins correct=22/23 killed=yes` does not reproduce against the frozen bytes:
   the counter's own internal battery today prints `correct=19/23 killed=yes` (same in my independent differential;
   `out-freeze-M1-carried-dropped.txt`), with the identical `tool_sha256=c9aa1391…`. Both are killed=yes and
   `killed=12`/`TARGET_MET` is unaffected, but the receipt's per-mutant intermediate for `static-first-wins`
   is not reproducible — likely measured against a pre-freeze counter build.
4. **Carried drift reports rc 2, not a verdict.** A moved carried case raises Setup (`:316-317`,
   "never a verdict", exit map says rc 2 is inconclusive), while the declaration's kill rule says
   `carried != 18/18` → the claim *fails*. The counter cannot express that fail as a verdict today.
5. **Robust where it matters:** the anchor-absent mutation cannot flip any verdict (dead branch at the freeze;
   at the base `correct=18` decides), and the wrong-stage probe is caught redundantly by three refusal cases.

## Commands

Counter-mutant run (each of the 7 freeze runs + probes):
`python3 -I <scratch>/c1-mut-<name>.py --repo <repo> --rev 5eb8f20fe291603c74973fa94cc55723ac8089a4 --base-rev e4b153dfa4a67ca56f7ec65cb6639082451626a7 --controls .ufo/waves/round-79/controls/c1-cases-r79.json --carried .ufo/waves/round-78/controls/c1-cases-r78.json --scratch-root <scratch>/sroot/<tag>`
Per-case differential reused the counter's own `run_cases`/`apply_mutation` on the freeze tool bytes (driver in scratch, outputs in `runs/`).

No tool installs were needed. No git/jj write command touched the lane repo; the only `git add/commit` ran
inside the scratch fixture repo after `git rev-parse --show-toplevel` asserted it (scratch deleted below).
Lane repo `git status --porcelain` after the run shows only this seat's new w1 artifacts; frozen instrument
hashes re-verified: counter+tool sha256 recorded in the run log, freeze tool sha matches `c9aa139152643020…`.
Scratch `/fast/scratch/hyaku/mado-r79/R79MutC1/` deleted at finish.
