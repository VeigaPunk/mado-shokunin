# R55W2MutC1CounterB — wave 2 falsification: C1 counter parsing and binding rules (mutation test)

Seat: R55W2MutC1CounterB (leaf, no subagents). Deliverable: `.ufo/waves/round-55/w2/R55W2MutC1CounterB/` (`mutants.md`, `mutants/mNN.py`, `mutants/mNN.diff`, `receipts/`).

## What ran

- Lane revision: scored rev `57584ed6`. Lane HEAD is `721ba9c1`; `git diff --stat 57584ed6 HEAD -- quality corpus tools .ufo/waves/round-55/frozen-tables-v2.json .ufo/waves/round-55/fetch` is empty, so the scored content equals HEAD for these paths. All files were read from `git archive 57584ed6` into scratch.
- Scratch repo: `/fast/scratch/hyaku/mado-r55/R55W2MutC1CounterB/repo`, built from the exported C1 surface (`quality`, `corpus`, `tools`, `.ufo/waves/round-55/{fetch,claims-frozen.md,registration-v2.md,frozen-tables-v2.json}`). Commit `937fb030`. `git init` was followed by a `rev-parse --show-toplevel` check. The one commit used `cd` + `git -c user.name=ctl -c user.email=ctl@ctl commit` rather than `git -C`; it was a fresh scratch repo, not the lane or fleet repo.
- Baseline (unmutated instrument, `python3 -I`):
  - `python3 -I repo/quality/counters/c1-r55-kbd-entry.py --selftest --repo repo --rev HEAD --work work/base` → `MADO_KBD_ENTRY_SELFTEST: 50/50 passed`, rc 0.
  - `python3 -I repo/quality/check-r55-controls.py --claim c1 --repo repo --rev HEAD --work work/base` → `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK`, rc 0.
- Mutants: 24 copies of the instrument, each with exactly one line changed (`mutants/mNN.diff`). Every mutant was run through its own selftest and through the independent harness with `--counter mutants/mNN.py` (`receipts/mNN/`). Runner: `receipts/run_one.sh`.
- Probes (`receipts/probe.py`, output in `receipts/probe-output.txt`): synthetic trees built with the instrument's own `good_files`/`build_repo`, run on the unchanged instrument and on the surviving mutant. Each probe is an in-grammar input (exact frozen grammar, only the named field changed).
- Tooling: none installed or upgraded. Only the system `python3` (stdlib) and `git` were used. No pacman, no network, no hyprctl calls.
- Where mutations happened: only on scratch copies. Nothing in the lane was edited, restored or committed. The lane was read-only (`git archive`, `git cat-file`, `git rev-parse`, `git diff --stat`).

## Results

Killed 12 of 24, survivors 11, equivalent 1. The harness killed 3 mutants (m01, m04, m23) and 0 survivors; all 7 controls passed on every survivor. Table with edits and risk: `mutants.md`.

| target (rule) | mutants | guard verdict |
|---|---|---|
| TABLES_SHA256 constant | m01 | GUARDED (selftest rc 2; harness good=bad) |
| 40-hex commit test in valid_shape | m02 | GAP, low–medium (probe P1) |
| Hyprland- prefix rule for source_cell | m03 (HIGH), m04 | m04 GUARDED; m03 GAP |
| K/H id ranges | m23 (N_H 6→7) GUARDED; m20 (ROW_ID boundary) GAP, false-reject direction | |
| 40/20-character proposition floor | m05 (K 40→39) GAP; m06 (H 20→19) GAP; m14 (leading space) GAP | |
| S-id regex (SRC_ID, S_IN_LINE, SID) | m08 GAP; m07 GAP; m22 EQUIVALENT | |
| CRLF / trailing-space handling | m09, m10 | GUARDED |
| symlink-blob rejection | m11 | GUARDED |
| fenced-code / HTML-comment skipping | m12, m13 | GUARDED |
| rev echo | m18 | GUARDED |
| registry admission (tier A, opened date) | m15, m16 | GAP |
| provenance verified-at date | m17 | GUARDED |
| quote delimiter (backtick style) | m19 | GUARDED |
| H-row src-cell `host` check | m21 | GUARDED |
| quote-in-pin-line binding | m24 | GAP, localisation only |

## Decisive outputs

Baseline: selftest `50/50 passed`, harness `good=ok controls=7/7 verdict=OK`.

Killed mutants (selftest/harness output, in `receipts/mNN/`):
- m01 (sha constant, last digit 9→8): selftest aborts rc 2 (`selftest needs frozen-tables.json at --rev matching the embedded sha256`); harness `good=bad controls=7/7 verdict=FAIL`.
- m04 (Hyprland- → wayland-): selftest `12/50 passed`; first failure `good-tree expected=none got=source_cell:K17`; harness `good=bad controls=2/7`, with `C1-CTL-2 spliced-quote: FAIL - leg source_cell:K17 names a row the mutation did not touch`.
- m23 (N_H 6→7): selftest rc 2 (setup); harness `controls=0/7`, counter stdout empty.
- m09/m10/m11/m12/m13/m17/m19/m21: selftest 48–49/50; the failing cases are named in `receipts/mNN/selftest.out`.
- m18 (rev echo): `good-tree` exact-line check fails, and `repo-path-is-a-symlink` and `dirty-working-tree-ignored` fail on the `rev=` text.

Survivors (both selftest 50/50 and harness 7/7 OK), each with the probe that separates it from the unchanged instrument (`receipts/probe-output.txt`):
- **P13, m03 (HIGH).** Non-new pin S316 (cited by K01–K07), registry URL with the commit replaced by zeros, path suffix intact.
  - ORIG: `rows=18/18 hosts=6/6 sources=11/18 new_rows=3/3 verdict=TARGET_MISSED missed=source_cell:K01,…,source_cell:K07`
  - m03: `rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none`
  - Real risk: if someone re-points a Hyprland registry row at another revision, the counter still prints green. The instrument as committed does enforce this rule; the gap is that nothing tests it.
- **P1, m02.** frozen-tables with `c1.commit` = `efb5099` (7 hex). ORIG `rows=0/18 … missed=tables_sha`; m02 `rows=18/18 … missed=tables_sha`. Reachable only with a changed embedded sha, so low–medium.
- **P3a/P3b, m05.** K02 proposition of 39 chars: ORIG `rows=17/18 … missed=row:K02`; m05 `TARGET_MET`. At 40 chars both pass.
- **P4a, m06.** H04 proposition of 19 chars: ORIG `hosts=5/6 … missed=row:H04`; m06 `TARGET_MET`.
- **P5, m07.** `source: S3160`: ORIG `missed=provenance`; m07 `TARGET_MET`.
- **P6, m08.** registry row `|S378| …`: ORIG `sources=17/18 new_rows=2/3 missed=source_cell:K10,new_rows`; m08 `TARGET_MET`.
- **P7, m14.** K02 proposition with a leading space: ORIG `missed=row:K02`; m14 `TARGET_MET`.
- **P8, m15.** new row at tier B: ORIG `new_rows=2/3 missed=new_rows`; m15 `TARGET_MET`.
- **P9, m16.** new row opened 2026-10-27: ORIG `new_rows=2/3 missed=new_rows`; m16 `TARGET_MET`.
- **P10, m20.** added line `| K03 extra | prose note |` after the K03 row: ORIG `TARGET_MET`; m20 `rows=17/18 … missed=row:K03` (false reject, not false green).
- **P12, m24.** K04 pin line altered, hash now mismatched: ORIG `missed=quote:K04,pin_hash`; m24 `missed=pin_hash`. The verdict stays red; only the row-level leg is lost.
- **P11, m22 (equivalent).** K02 source cell `S316x`: ORIG and m22 print identical output (`source_cell:K02`). The `$` is redundant because the registry lookup is exact.

## Verdict on the target

- No mutant shows a defect in the committed instrument's behaviour: every survivor is a behaviour the instrument already implements, which the selftest and harness do not check.
- Target verdicts for the C1 counter's parsing and binding rules: GUARDED where a mutant was killed (sha constant, Hyprland prefix swap, CRLF, trailing whitespace, symlink blob, fence, HTML comment, rev echo, provenance date, backtick delimiter, host src check, id count); GAP where it was not (commit regex, Hyprland commit requirement, K/H floors, S-id grammar, registry tier/opened admission, ROW_ID boundary, quote-in-pin localisation).
- The harness is not a guard against any of these gaps (0 of 11 survivors detected). Its 7 controls cover only the frozen mutations.
- Falsification of PRED-C1-r55 by this seat: NOT-REPRODUCED. No in-grammar input against the unchanged committed instrument gave a wrong verdict in these probes; the probes exercised the counter's rules only as its code implements them, and the gaps are in test coverage. The HIGH gap (m03) matters only if registry rows change; it is not a current wrong verdict on the committed registry, which passes.

## Could not verify / limits

- Entailment of propositions by quotes: out of scope for a mutation test (declared limit in registration-v2).
- The branch "sha matches but shape invalid → rc 2" is not reachable by a one-edit mutant. I did not test it with a two-edit copy.
- Probes use synthetic trees built with the instrument's own helpers, not the committed entry. The committed entry was scored green by the instrument (baseline) but not mutated.
- Harness controls were run only against the mutated instrument, not against an independently written harness.

## Hygiene

- No `commit`, `push`, `stash`, `reset`, `checkout` or jj command against the lane or fleet repo. The only commit was in the scratch repo.
- No hyprctl, pacman, network or service call. No task or background job.
- Deliverables written only under `.ufo/waves/round-55/w2/R55W2MutC1CounterB/` and this report.
- Scratch `/fast/scratch/hyaku/mado-r55/R55W2MutC1CounterB/` removed before yield (receipts copied first).
