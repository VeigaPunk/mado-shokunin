# R55ExecFreezeOrder — w1 report (freeze-order checker)

## Deliverables (all under `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55ExecFreezeOrder/`)
- `check-freeze-order.py` — `python3 -I … --repo PATH --rev REV --round N --wave W [--work DIR]` and `--selftest --work DIR`.
  Git objects only (`rev-parse`, `log --first-parent`, `ls-tree`, `cat-file`, `show -s --format=%cI`), no working tree/index/ref access,
  `GIT_*` env scrubbed, global/system git config disabled, `TMPDIR=--work` for children. Writes nothing except `--selftest` scratch
  repos (under `--work`, removed at the end).
- `selftest-output.txt` — 16 PASS, `MADO_FREEZE_ORDER_SELFTEST: OK`, rc=0.
- `r54-run-output.txt` — real runs on committed objects.

## Ground truth reproduced (round 54, wave w1, REV `fe03bb3` = `fe03bb3b2ec05fbf906b83096c637fd6a05b3dc8`)
```
MADO_FREEZE_ORDER: round=54 wave=w1 freeze=350d30e4ec55 freeze_time=2026-10-27T14:11:10-03:00 launch=2026-10-27T17:05:25.338Z verdict=FAIL reason=freeze_after_launch
rc=1
```
Freeze commit `350d30e4ec55…` (committer 14:11:10-03:00 = 17:11:10Z) vs createdAt 17:05:25.338Z: freeze 5m45s after launch. Matches the brief.
Note: the closure text writes "14:11:10 vs 14:05:25" comparing a -03:00 local time with a Z-time's digits; the registry's `17:05:25Z` is the correct UTC value (the claims-frozen.md "14:05:25" is the same instant in -03:00 — 17:05:25Z = 14:05:25-03:00 — so the comparison is consistent).
Other runs (informational):
- r54 w2 at fe03bb3: `launch=2026-10-27T17:46:51.625Z verdict=OK reason=ok` rc=0 (w2 launched after the late freeze).
- r55 w1 at lane HEAD: `freeze=54dacbd843d6 freeze_time=2026-10-28T18:46:52-03:00 launch=2026-10-28T21:50:15.231Z verdict=OK reason=ok` rc=0 (freeze 54dacbd matches the commit named in the assignment; 3h03m before launch).
- no `--wave` → `MADO_FREEZE_ORDER: SETUP usage` rc=2; unknown rev → `SETUP rev_not_found` rc=2.

## Selftest (scratch repos under `--work`, `GIT_COMMITTER_DATE`/`GIT_AUTHOR_DATE` controlled per commit)
Covers: OK; freeze_after_launch; equal-time (strictly-earlier rule) → FAIL; freeze_edited for `registration.md` and for `frozen-tables.json`;
edit-then-revert (blob-equality, treated as not edited); no_freeze (registration.md absent); no_registry (file absent, createdAt unparsable);
author/committer trap both directions (author early/committer late → FAIL; author late/committer early → OK); freeze split across two commits
(freeze = the later); `frozen-tables.json` optional; freeze arriving through a merge (first-parent freeze = merge commit); setup errors.
Mutation proof: swapping `%cI`→`%aI` (author time) makes both TRAP cases fail (`MADO_FREEZE_ORDER_SELFTEST: FAIL 2 failed`), so the traps are live.

## Interpretation choices / ambiguities (the spec does not decide these)
1. **freeze_edited line**: `freeze=` is the earliest commit whose blobs all equal REV's (the literal freeze-commit definition), i.e. the *editing* commit,
   not the original first appearance. Reason names the first (in `claims-frozen.md, registration.md, frozen-tables.json` order) file whose first-appearance blob ≠ REV blob. Edited check precedes the launch comparison; `launch=` is still printed if readable.
2. **Edit-then-revert** (blob returns to its first-appearance value): not reported as edited; freeze = the first commit. A change history check would need per-commit blob lineage; the contract speaks of blob ids at REV vs first appearance only.
3. **no_registry** also covers: unreadable/invalid JSON, non-object JSON, missing or unparsable `createdAt` (ISO with `Z` or ±hh:mm required). Missing fields print `none`; exit 1 (FAIL), not 2, since the spec reserves 2 for setup errors (bad repo/rev/usage/`--work` not a directory).
4. **no_freeze** exit 1, `freeze=none freeze_time=none launch=none` (launch not read).
5. Time equality → FAIL (strictly earlier required). Comparison is on aware datetimes (fractional seconds kept), freeze printed as git `%cI` (committer local offset).
6. "First appearance" is computed on the first-parent chain via `git log --first-parent --full-history -- <freeze paths>`; a file deleted and re-added is judged at its first appearance only.
7. `--selftest` requires `--work` (no implicit /tmp). `--work` for the normal mode is validated as an existing directory and only exported as `TMPDIR` to git.

## Not verified / not run
- Python versions other than the host's default not tested. No tool installs. No hold-out path seen. No host, config or compositor reads were needed.
- Not a non-author reviewer; the harness `quality/check-freeze-order.py` placement/integration is the L1's.
