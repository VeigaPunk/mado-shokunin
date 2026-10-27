# MutC2FrozenCounter — w2 FALSIFY probe of frozen PRED-C2-r50

Date: 2026-10-27. Seat: MutC2FrozenCounter (w2, FALSIFY policy v1).
Target: frozen counter `quality/counters/c2-r50-session-gate.py`
sha256 `1d52a62cd969aba59c2cd1f944212b6f9619212b5fb313c470c4c14ebd62b298`
and the rule-removal mutants of the scored gate bytes
(`quality/check-session-material.py` v3 sha256 `ffdc9d62…`).

All scoring with the frozen counter bytes on a `git clone -q --shared` of the
lane inside scratch (`/fast/scratch/hyaku/mado-r50/MutC2FrozenCounter/lane`,
toplevel asserted), nonce **314159** (k_red=44, k_green=44), TMPDIR/`--work`
under the seat scratch, host state untouched (no installs needed; stdlib only).

## Verdict

- **C2 freeze holds.** Pristine control reads TARGET_MET at `906178b6`; every
  gate mutant is killed by the frozen counter; both counter mutants are
  verdict-preserving at the honest data rev.
- **(b) coverage finding (survivor):** one-line widening of the counter's
  `names` containment converts the frozen counter's own kill of a
  zero-v2-names gate into TARGET_MET. The exact-69-v2-name check is
  load-bearing; the frozen bytes are the only thing pinning the v2 selftest
  names. No contract change proposed — recorded as attack evidence.
- **(c) finding:** green's `files>=1` is defense-in-depth, never
  verdict-decisive: a scan-nothing gate fails under both counters (red and
  selftest kill it). Dropping `files>=1` flips green 0/44→44/44 on the
  nothing gate but cannot produce a passing verdict.
- **(d) finding:** a selftest-passing silent-scan gate is NOT caught by green
  (green passes 44/44; `files>=1` does not fire) — red (parsed `findings>=1`
  + `rule=` token) and clause d kill it.
- **(a) w1 claim verified under an independent nonce:** the R7-removal mutant
  drops exactly its family (r7-prefix/header/diag/row all 0), green stays
  clean, plus two extra kill paths (selftest 87/94, scope=blind).

## Run matrix (all nonce 314159; receipts in `receipts/`)

| # | counter | gate @ rev | verdict | key line |
|---|---|---|---|---|
| 0 | frozen | `906178b6` (pristine) | TARGET_MET rc=0 | `selftest=94/94 names=69/69 red=44/44 green=44/44 scope=seen` |
| a | frozen | R7-off `c27dff99` | TARGET_MISSED rc=1 | `selftest=87/94 red=14/44 families=r7-prefix=0/8 r7-header=0/8 r7-diag=0/7 r7-row=0/7 r8-account=7/7 r9-cache=7/7 green=44/44 scope=blind` |
| b1 | frozen | rename69 `c92c7bf4` | TARGET_MISSED rc=1 | `selftest=94/94 names=0/69 red=44/44 green=44/44 scope=seen` (names clause kills) |
| b2 | names69 `e0d6f8aa` | `906178b6` | TARGET_MET rc=0 | honest path unchanged |
| b3 | names69 `e0d6f8aa` | rename69 `c92c7bf4` | **TARGET_MET rc=0 (survivor)** | `selftest=94/94 names=0/69 red=44/44 green=44/44 scope=seen verdict=TARGET_MET` |
| c1 | frozen | nothing `1b2a452d` | TARGET_MISSED rc=1 | `selftest=crashed red=0/44 green=0/44 (files=0 vs files>=1) scope=blind` |
| c2 | nofiles `5ab491cf` | `906178b6` | TARGET_MET rc=0 | honest path unchanged |
| c3 | nofiles `5ab491cf` | nothing `1b2a452d` | TARGET_MISSED rc=1 | green flips to 44/44; `selftest=crashed red=0/44` still kill |
| d1 | frozen | silent `8a6d69d9` | TARGET_MISSED rc=1 | `selftest=94/94 red=0/44 green=44/44 (passes) scope=blind` |

## Mutants (patches as unified diffs in `receipts/patch-*.diff`)

- **M-gate-r7** rev `c27dff990a244ca186b52e02806b29b00a6d59f3`, gate blob
  sha256 `1ec97f9dc51441158ae357d6327ffd148cb2289aac18bc1734d87a06402dfc26`
  — byte-identical blob to w1's r7 mutant (w1
  `w1/ExecCounterC2R50/receipts/mutants.txt`), reproduced independently:
  `'    if total:' -> '    if False:'` (scan_blob R7 emission), anchor unique.
  Under nonce 314159: r7 families = 30 instances (8+8+7+7 of 44) all miss;
  exactly its family dropped; r8/r9 and green untouched. Extra kills beyond
  the family drop: selftest 87/94 (7 R7 unit cases fail) and scope=blind
  (clause-d fixture is an r7-prefix shape). w1 freeze claim re-verified.
- **M-gate-rename69** rev `c92c7bf4d853aed43c856babb26ee2a4425eb6de`, blob
  sha256 `3f201325998b4bf2baf38def3e1970257c8521d7fe034d1e5c31cc2244ec2739`
  — all 69 v2 selftest case-name emissions prefixed `zz-` (63 literals +
  2 `"waiver-title-%s-*"` templates; census-verified the 6 waiver-title names
  are template-built). Selftest 94/94 still passes; detection intact.
- **M-gate-silent** rev `8a6d69d9da4060ffc9912e9935f694b2faf3d0da`, blob
  sha256 `fe838f70ff46d4d40f6b210c7a756510c1fae2e21ed810c49b7b027352ca1ce0`
  — `emit()` FINDING loop gated on env `CSM_SELFTESTING`, `selftest()` sets
  it. Passes selftest 94/94; under scan prints `SESSION_MATERIAL` summary
  (rc still 1 internally on reds) but zero FINDING lines.
- **M-gate-nothing** rev `1b2a452dfa5c5956421bcf43f35f07cc1cb72789`, blob
  sha256 `392aab403450bd3c37394bce3c9ac6f5e593b42778049e4574f0a40bfd78f968`
  — `run()` returns `files=0, findings=[]` (scan-nothing).
- **counter-names69** sha256 `e0d6f8aa1821577d95e90ba04e12a5f3378ab82607e76b6b07d6a169a46b2849`
  — one-line mutant of the frozen counter: `not missing` →
  `len(got_names) >= len(wanted)` (any 69-case set accepted).
- **counter-nofiles** sha256 `5ab491cfa62fc41079d232af34aeedd2825331b20275c796112ef42ebe6c3c24`
  — green ok drops `and (result["files"] or 0) >= 1`.

## Analysis

(b) The frozen counter kills rename69 via `selftest_ok = … and not missing`
(`c2-r50-session-gate.py:467-470`): names=0/69 → TARGET_MISSED even with
red/green/scope perfect. The widened counter admits the same gate
(TARGET_MET, receipt `b3-names69-at-rename69.txt`) — a gate keeping **zero**
of the 69 pinned v2 case names would pass. Finding supports the freeze: the
exact-name containment is the sole pin of the v2 selftest surface.

(c) Scan-nothing gate cannot pass either counter. Frozen: green fails
files>=1 (files=0), red fails findings=0, selftest crashes — three
independent kills. With files>=1 dropped (c3): green flips to 44/44, yet
verdict stays MISSED via selftest crash and red=0/44. So `files>=1` guards
nothing the verdict depends on; it only turns a silent green run from
pass-clean-fail-files into pass-clean.

(d) Silent-scan gate: green **passes** (rc=0, findings=0, files=1≥1);
`files>=1` never fires. Red kills it because the counter parses findings
from emitted `FINDING` lines, not from rc — the gate's internal rc=1 is
invisible. Clause d adds a second kill (default scope findings=0). Answer to
the seat question: green must NOT still fail — it doesn't; red and scope
catch the silent gate.

## Restoration / hygiene

- Lane repo untouched: `quality/counters/c2-r50-session-gate.py` sha256
  `1d52a62c…` and `quality/check-session-material.py` sha256 `ffdc9d62…` at
  HEAD `b4a79843` (re-hashed after all runs; diff `906178b6..b4a79843` empty
  for both files).
- Base gate bytes restored in the clone: `git show 906178b6:quality/
  check-session-material.py | sha256sum` = `ffdc9d62…` after all mutant runs;
  clone working tree clean (`git status --porcelain` empty); mutants live only
  on fixture branches.
- No tools installed (stdlib only). Scratch dir deleted after receipt copy.

## Deliverables

- Report: `.ufo/waves/round-50/w2/MutC2FrozenCounter.md` (this file)
- Receipts: `.ufo/waves/round-50/w2/MutC2FrozenCounter/receipts/`
  (`0-pristine-frozen.txt`, `a-r7-off-frozen.txt`, `b1-rename69-frozen.txt`,
  `b2-names69-at-data.txt`, `b3-names69-at-rename69.txt`,
  `c1-nothing-frozen.txt`, `c2-nofiles-at-data.txt`,
  `c3-nofiles-at-nothing.txt`, `d1-silent-frozen.txt`,
  `patch-*.diff` ×6)
