# R55W2CritC3Stale — C3 counter vs a false P23 (round 55, wave w2)

Role: critic, leaf member, no subagents. Scored revision 57584ed67716340b3d466fa04333ac0bab3fb79e.
Full record: `.ufo/waves/round-55/w2/R55W2CritC3Stale/false-p23.md`; receipts: `.ufo/waves/round-55/w2/R55W2CritC3Stale/receipts/`.

## What I attacked

Target: `quality/counters/c3-r55-p19.py` (committed, sha256 9259af01e43c5acdbefe4425d404e5592b00596f251d53582a2daf94a47d3859,
equal to the working-tree file) and the frozen predicate PRED-C3-r55 (counter line AND `check-r55-controls.py --claim c3`).
Question: can a P23 that is false about the `else` arm pass, while keeping the 13 Q rows byte-exact and the heading, and
avoiding the `stale` leg's triggers (ASCII `only when` in any case; the exact base P19 sentence)?

## What ran

Scratch only: `/fast/scratch/hyaku/mado-r55/R55W2CritC3Stale/` (removed before yield, after copying receipts).
Driver `receipts/attack.py` (python3 -I) built, in a `git init` scratch repo whose objects are an alternates link to the lane's
read-only store, 20 commits, each = 57584ed's tree with ONLY the P23 line replaced (or a prose paragraph appended).
`git diff 57584ed <V1>` changes one line (`receipts/evidence.txt`). Every variant's bytes start with the base prefix (verified).
Counter run per commit: `python3 -I <committed counter> --repo <scratch> --rev <commit> --work <scratch>/w-*`.
Full predicate for selected variants: `python3 -I qual/check-r55-controls.py --claim c3 --repo <scratch> --rev <commit> --work <w> --counter <committed counter>`
(qual/ = committed copies of check-r55-controls.py and r55_ctl_c{1,2,3}.py at 57584ed).
Baselines at 57584ed (lane revision, read-only): counter → `MADO_P19_FIX: rev=57584ed... prefix=identical rows=13/13 pin=ok p23=ok readme=ok verdict=TARGET_MET missed=none`, rc 0;
counter `--selftest` → `MADO_P19_FIX_SELFTEST: 41/41 passed`; controls → `MADO_R55_CONTROLS: claim=c3 good=ok controls=6/6 verdict=OK`, rc 0.
The lane was read only (git cat-file/show/rev-parse via the counter and harness). No lane file written; no git mutation in the lane; no commit in the lane.
Mutation method: the counter was NOT modified (sha checked). The variants are input commits, so QUALITY 105's "unchanged instrument" holds.

## Decisive results

V1 (P23 row; else arm stated as "sends only a keyboard key RELEASED and never a keyboard key PRESSED"; all other cells and all 13 Q rows and heading untouched):
- counter: `MADO_P19_FIX: rev=267088e79f61cb191f9df4441adbd4874066b307 prefix=identical rows=13/13 pin=ok p23=ok readme=ok verdict=TARGET_MET missed=none` rc 0
- controls: `MADO_R55_CONTROLS: claim=c3 good=ok controls=6/6 verdict=OK` rc 0
- The pin refutes the sentence: `Hyprland-ConfigActions.cpp:1568` `sendKeyboardKey(... WL_KEYBOARD_KEY_STATE_PRESSED)` and `:1569` `... RELEASED` are both in the else arm (my direct read of `git show 57584ed:.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp | sed -n 1566,1576p`).

V3 (Cyrillic U+043E in "оnly when", re-asserting the P19 falsehood, plus the V1 else-arm claim): TARGET_MET rc 0; controls 6/6 OK. `stale` does not fire because the block contains no ASCII `only when` (checked on the appended block bytes: `block_has_'only when'=False`, `block_has_cyrillic_o=True`).

V18 (V1 row + appended prose "only" NEWLINE "when"): TARGET_MET rc 0; controls 6/6 OK.

## Verdict per target

| # | Target | Verdict | Evidence |
|---|---|---|---|
| T1 | Counter rejects a P23 whose else-arm sentence is false (lexical `p23` leg) | **BROKEN** (as a truth check; the leg is lexical by design, see below) | V1, V2 TARGET_MET; V1 full predicate 6/6 OK |
| T2 | Full PRED-C3-r55 rejects a false P23 | **BROKEN** | V1 and V3/V4/V18: counter TARGET_MET and controls 6/6 OK on the false tree |
| T3 | `stale` catches restatement of P19 via lookalikes, whitespace, entities, line breaks | **BROKEN** | TARGET_MET for V3 (Cyrillic о), V4 (ZWSP), V5 (NBSP), V6 (`&#32;`), V7 (two spaces), V8 (tab), V9 (`ONLY\tWHEN`), V10 (fullwidth), V17/V18 (`only`↵`when` in prose) |
| T4 | `stale` catches ASCII `only when` in any ASCII case and the exact P19 sentence | **SURVIVES** | V12 `only when`, V13 `ONLY WHEN` → missed=stale rc 1; V19 P19 sentence verbatim → missed=stale rc 1 |
| T5 | Lexical `p23` leg rejects syntactic deviations (NBSP in `== 1`, `Pressed`, split row) | **SURVIVES** (non-reproducing attacks: these are syntactic rejections, reported as such) | V14, V15, V16 → missed=p23 rc 1 |
| T6 | Q rows / heading / pin / prefix legs bypassed by a P23-only edit | **NOT-REPRODUCED** (not bypassed by any variant; not separately attacked beyond V1–V19 and the counter's own 41-case selftest) | all variants rows=13/13, prefix=identical, pin=ok |
| T7 | Harness/compact spacing (V11: `\|P23\|P19\|...\|`) | counter TARGET_MET; full predicate **FAIL 5/6** because `r55_ctl_c3.py` `find_row` requires `\| P23 \|` with spaces (C3-CTL-5 cannot build its control) | a harness limitation, not a counter pass; reported so the predicate's claim is not overstated |

## What the counter proves and what it does not (required statement)

The lexical leg proves **vocabulary, not truth**. The `p23` leg checks one row's cell shape (Supersedes `P19`, Source `S371`,
Pin:anchor `Hyprland-ConfigActions.cpp:1554-1576`) and substring presence of `m_passPressed`, `== 1`, `== 0`, `PRESSED`, `RELEASED`
and one of `otherwise`/`any other`/`else` anywhere in the proposition cell. V1 satisfies every one while stating the opposite
of the pin for the else arm. The `stale` leg is a second substring test (ASCII `only when`, and the verbatim P19 sentence), so it
rejects a restatement only when the restatement uses the exact ASCII characters.

The truth of P23 therefore rests on the **sentence-to-pin audit (R55W2RevP23)**, which is the only check that reads the proposition
against the quoted pin lines. Nothing in C3 as frozen does that. The registration v2 already labels the `p23` leg "presence-only"; this
attack shows the consequence concretely: TARGET_MET is not evidence that the else arm is described correctly.

Caveat on my own pin reading: I read `Hyprland-ConfigActions.cpp:1566-1576` directly; I did not run the sentence-to-pin audit and I
did not check the real lane P23 sentence line-by-line against the pin. The real P23 in 57584ed (not my variant) is the object of R55W2RevP23.

## Not verified / not run

- Full predicate (counter + controls) was run for V1, V3, V4, V11, V18 only; V2, V5–V10, V17 were checked by the counter alone.
- I did not run any non-author sentence-to-pin reading of the real P23; that is R55W2RevP23's item.
- Runtime delivery of any arm: not in scope; not claimed.
- Q-row bypass with the rows leg was not attacked beyond what the variants above touched (no Q row was altered in any variant).
- Lookalike set is a sample (Cyrillic, zero-width, NBSP, HTML entity, fullwidth, tab, double space); not exhaustive.

## Tooling

None installed. Used git, python3 -I, sha256sum, cat, sed, grep only. No tool installed, upgraded or removed. No pacman, no network reads.

## Receipts (in .ufo/waves/round-55/w2/R55W2CritC3Stale/receipts/)

`attack.py` (driver), `results.json` (per variant: commit, rc, counter line, stale-substring flag), `commits.json`, `evidence.txt` (V1 diff, V1 P23 row,
V3/V4 byte checks, V18 prose, pin 1566-1576), `block-checks.txt` (block-only stale checks), `ctl-base.err` (controls at 57584ed: 6/6 OK),
`ctl-V1_*.err`, `ctl-V3_*.err`, `ctl-V4_*.err`, `ctl-V11_*.err`, `ctl-V18_*.err` (controls on variants), `c3-committed.py` (counter byte copy, sha 9259af01…),
`alternates-of-scratch-repo.txt`.

## Scratch

`/fast/scratch/hyaku/mado-r55/R55W2CritC3Stale/` removed after receipts were copied (see final step). Lane not written.
