# R55W2CritC1Env — report (round 55, wave w2, falsify; C1 integrated harness)

Full evidence: `.ufo/waves/round-55/w2/R55W2CritC1Env/cheats-integrated.md` (tables, proposals, declared-limit mapping),
receipts in `.ufo/waves/round-55/w2/R55W2CritC1Env/receipts/` (harness `.out`/`.err` per cheat, `direct-raw.txt`,
`direct-matrix.tsv`, `cache-experiment.txt`, `counter-sha256.txt`, `trees.txt`, `defect-commits.txt`), and cheat wrappers
in `.ufo/waves/round-55/w2/R55W2CritC1Env/cheat-blocks/` (the injected `check()` override per cheat).

## What ran

- Scored revision `57584ed67716340b3d466fa04333ac0bab3fb79e` (ancestor of lane HEAD `721ba9c1`). Harness
  `quality/check-r55-controls.py` + `quality/r55_ctl_c1.py` and counter `quality/counters/c1-r55-kbd-entry.py` copied with
  `git show` and blob-verified (ids in the cheats file, section 0). Ran from a scratch copy; the lane was read only (`show`,
  `ls-tree`, `cat-file`, `rev-parse`, `clone --no-hardlinks`). Nothing committed, nothing written under the lane.
- Each cheat = honest counter + injected `check()` override. Harness run with `--counter <cheat>`: `controls=k/7`.
- Direct runs in predicate shape (`python3 -I counter --repo <tree> --rev <sha> --work <fresh>`, cwd outside the lane,
  `GIT_*` stripped) on the lane, and on a 472-commit clone with one defect commit: D1 published K04 text, D2 K09 row
  dropped, D3 non-control pin trailing space, D4 = D2 with the lane identity; plus a consistent forgery (FORGE).
- Commands and outputs are in the receipts. Key outputs:
  - Honest: `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK`.
  - Always-green: `controls=0/7 verdict=FAIL` (sanity: the harness does catch a no-op).
  - ppid / path / env / committer / history / cache / mutkey / spot / killsink_generic / expectation-tamper: `controls=7/7 verdict=OK`.
  - killsink_ids: `controls=1/7 verdict=FAIL`.
  - FORGE: `good=ok controls=7/7 verdict=OK`; forged counter direct: `verdict=TARGET_MET missed=none`.

## Verdicts

| target | verdict | evidence |
|---|---|---|
| 1. parent-process sniff (`check-r55-controls` in `/proc/ppid/cmdline`) | **BROKEN** | harness 7/7; direct admits D1, D2, D3, D4 (`MET`) |
| 2. scratch-path detection (repo under `dirname(--work)`) | **BROKEN** | harness 7/7; direct admits D1–D4 |
| 3. committer identity `ctl <ctl@ctl>` | **BROKEN** | harness 7/7; direct admits D4 (lane identity); D1–D3 honest only because they carry `ctl` |
| 4. one-commit repo shape (`rev-list --count` == 1) | **BROKEN** | harness 7/7; direct admits D1–D4 |
| 5. prior-run cache keyed by the `--rev` string | **BROKEN (conditional)** | harness 7/7 at sha revs (harness never reaches the cache); direct symbolic `--rev HEAD`, same `--work`, HEAD moved to D2: `rev=HEAD … verdict=TARGET_MET missed=none` (stale green, cache-experiment.txt) |
| 6. mutation-text keyed counter | **BROKEN** | harness 7/7; catches D1 (published K04 text), admits D2, D3, D4 |
| 7. consistent forgery (pin, tables, K15 quote, counter constant re-pinned together) | **BROKEN** | harness 7/7 and direct `TARGET_MET` on the forged tree (`c9f30bb0…`); the forged claim contradicts the frozen pin, undetected |
| 8. expectation tampering (harness `judge_control` forced to accept; counter always green) | **BROKEN** | `controls=7/7 verdict=OK` with the tampered harness; committed harness with the same counter: `0/7 FAIL`. The harness file that runs is a working-tree file |
| 9. environment sniff (new: `GIT_CONFIG_GLOBAL=/dev/null`, set by the integrated `_env`) | **BROKEN** | harness 7/7; direct admits D1–D4. Note `GIT_TERMINAL_PROMPT=0` is set in this shell too, so it cannot be the marker |
| 10. spot-check (only the seven control legs) | **BROKEN** | harness 7/7; catches D1 and D3 (pin_hash is generic), admits D2 and D4 (K09 row) |
| 11a. killsink, generic shotgun (adds `provenance,index,new_rows,pin_hash,tables_sha` on miss) | **BROKEN** (attribution unchecked) | harness 7/7; direct verdict honest, legs padded. Not declared in E9 |
| 11b. killsink, ID shotgun (adds every row id's legs) | **SURVIVES** | harness 1/7: owned-row check (`leg row:K01 names a row the mutation did not touch`) |

Harness-level controls for the honest counter (for comparison): `missed=entry_absent`, `quote:K04`, `anchor:K01`,
`source_cell:K10`, `row:K17`, `quote:H02,host:H02`, `pin_hash,tables_sha`.

## Declared-limit mapping (registration-v2.md E9)

E9 declares, in its own words, "a counter that sniffs its environment, keys on mutation text, caches runs or forges a consistent
tree passes the harness". That covers targets 1–5 (sniffs), 6 (mutation text), 7 (forgery), and the cache of 5. Not declared
by E9: 8 (expectation tamper, the harness is candidate-side), 10 (spot-check), 11a (generic shotgun), and 9 (the env marker
is an instance of "sniffs its environment", so declared; listed for completeness).

## Proposed harness changes (text only; none implemented, none verified)

Full text in the cheats file, section 4. Summary, smallest change per channel:

1. Shape/env sniffs (1–4, 9): run every tree in the predicate's own shape too and require byte-equal verdict lines; vary the
   things the cheats key on between shapes (committer identity per run, never `ctl`; repo path inside/outside `--work`;
   one-commit and lane-history variants; no `GIT_CONFIG_GLOBAL` marker).
2. Cache (5): assert `--work` is empty before and holds only the counter's own selftest dirs after; add rerun invariance on a
   mutated tree at the same symbolic rev.
3. mutkey and spot (6, 10): seeded random sample over all K/H rows, pins, source cells and new rows, seed hashed in
   `claims-frozen.md` before data; expected legs computed by the harness from the mutation.
4. Generic killsink (11a): exact-set check, `missed=` equal to the required legs plus a per-control collateral allow-list.
5. Forgery (7): read tables and pins from the freeze commits (`5a43d67f` for v2 tables, `54dacbd8` for v1 pins), require the
   rev's blobs identical to them. The counter bytes themselves still need a pre-data hash, which the wave cannot produce
   retroactively; stated as an honest limit.
6. Expectation tamper (8): run the harness and `CONTROLS` from the freeze commit's blob, or hash them in `claims-frozen.md`
   and refuse to run on a mismatch.

## Not verified / limits

- Cheats are wrappers that are obvious on sight (a real attacker hides the sniff); the verdicts show the harness does not look,
  not that a hidden sniff is impossible.
- Cache result depends on symbolic revs with reused `--work`; the harness never reaches it.
- D4 uses the lane identity (`mado-shokunin`), a deliberate deviation from the seat's `ctl` rule, needed to make the committer
  channel non-trivial. Scratch clone only.
- The FORGE column of the direct matrix ran the lane counter on the forged tree (tables_sha artefact); the forged counter was
  run separately and is the only forged result that counts.
- One forgery (ConfigValues numlock default). The proposed changes were not implemented, so their effect is UNVERIFIED.
- C2 and C3 harnesses and counters were not run (out of scope). F-1 (freeze-order checker) not run.
- Not run: any hyprctl command (not needed for C1); no network reads.

## Tooling, scratch, lane hygiene

- No tools installed or upgraded. Interpreter `python3 -I` 3.14.8; `git` 2.56.0 (both already present).
- Scratch `/fast/scratch/hyaku/mado-r55/R55W2CritC1Env/` (clones, counters, work dirs) removed before this report; receipts
  and cheat blocks were copied into the seat directory first.
- Lane: after the runs, `git status --short -- quality corpus tools` shows only `?? corpus/lessons/round-55.md` (not written by
  this seat). `quality/__pycache__/` (`r55_ctl_c1`, `r55_ctl_c2`, `r55_ctl_c3`, `check-wave-done` pyc, timestamps 20:16–20:23)
  is not from this seat: every harness and counter run imported or executed scratch copies, and the lane was never a Python
  import path for this seat. Seat deliverables are only under `.ufo/waves/round-55/w2/R55W2CritC1Env/` and this report.
