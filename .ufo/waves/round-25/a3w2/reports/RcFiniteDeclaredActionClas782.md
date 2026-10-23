# RcFiniteDeclaredActionClas782 — C2 ledger attack on CapFiniteDeclaredActionClas782

Reviewed report: `.ufo/waves/round-25/a3w1/reports/CapFiniteDeclaredActionClas782.md`
Row under review: `SCORECARD.md:782` (`finite declared-action classifier`), base `41cc04c8`.

## Method

Independent re-derivation, not a re-read of the executor's claims:

1. `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 41cc04c8:SCORECARD.md` → sha256 `6b6995ff6998a405c2d4472463204b16e644829ad821a368922a65a60853ca08`, 1618 lines (matches the executor's stated hash/size).
2. `git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/rc/CapFiniteDeclaredActionClas782`, `git checkout -q --detach 41cc04c8` (GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset); `HEAD` = `41cc04c8d593837a0d5078bffaacdaa163d12897`.
3. Re-ran the row's two named commands plus the section's two plan controls under `timeout 600 prlimit --as=4000000000` in the clone.
4. Verified in-tree artifacts: tool hash, frozen pins, evidence receipts, tool git history, superseding text, retirement entries.
5. Deleted the clone (`rm -rf`, absent afterward).

## Observed at 41cc04c8 (this reviewer's runs)

| Command | Exit | Key output |
|---|---|---|
| `python3 -I tools/mado-action-plan.py --selftest` | 0 | `SELFTEST_SCRIPT_SHA256: 226220ae…a3`; 52 `SELFTEST PASS` lines; `SELFTEST_SUMMARY: 52/52 passed` |
| `python3 -I tools/mado-action-plan.py --frozen .ufo/waves/round-16/frozen` | 0 | `MADO_PLAN: frozen_match`; verdict JSON `"detail": "frozen verdict denied_executable:sudo/1 matched"`, `"schema": "mado-action-plan-verdict-v1"` |
| `--plan fixtures/tight-red.json --policy safety-policy.json` | 1 | `MADO_PLAN: denied_executable:sudo` |
| `--plan fixtures/tight-green.json --policy safety-policy.json` | 0 | `MADO_PLAN: plan_safe` |

Identical to the executor's verbatim output, byte-for-byte on all four runs (selftest pass names, ordering, JSON fields all match). Evidence is run, not copied: I observed the runs in my own clone; the executor's receipt files could not produce them.

## Cross-checks

- Row 782 verbatim: `| finite declared-action classifier | Refuse blocked declared kinds, the 12 pinned argv[0] names, unknown kinds and malformed inputs; compare a digest-pinned declared-plan replay | python3 -I tools/mado-action-plan.py --selftest 52/52 and --frozen .ufo/waves/round-16/frozen frozen_match at corrected content; evidence/action-selftest-final.json, action-frozen-final.json, committed-bindings.json | 16 |` — matches the report's "Row under test" summary.
- Tool identity: `tools/mado-action-plan.py` sha256 `226220ae41436506c048258aff15fff83577acf0ae71ffa955d585a18ba5aea3`, 39152 bytes; `committed-bindings.json` pins the same sha/bytes at `measured_commit 1e31681e…`; `git log` shows only `1e31681` and `9dcf248` (both round 16) touched it.
- `PINNED_DENY_EXECUTABLES` (`tools/mado-action-plan.py:109`) = {pacman, yay, paru, systemctl, hyprctl, omarchy, libinput, evtest, sudo, sh, bash, env} — exactly 12 names; policy validator enforces set equality (`:258-262`). Row's "12 pinned argv[0] names" confirmed.
- Frozen pins: `plan.json` sha256 `82bc7652…ebc3`, `policy.json` sha256 `fb134d8f…b7fc` equal `expected.json`'s `plan_sha256`/`policy_sha256`; the digest comparison sits at `tools/mado-action-plan.py:425-437` (report said 427-437 — same block).
- Evidence pointers exist: `evidence/action-selftest-final.json` (measured_commit `1e31681e…`, exit 0), `action-frozen-final.json` (exit 0, stdout identical to my run), `committed-bindings.json` (sha `226220ae…`, 39152 bytes).
- Superseding pointer: `SCORECARD.md:1588-1597` wave-2 correction states the `finite declared-action classifier` (round 16) "prints `SELFTEST_SUMMARY: 52/52 passed`, exit 0" re-run at `39c59630`, does not re-run `--frozen`, and places the row outside the 12-row counted population — exactly as the ledger line records. No contradiction.
- Later `classifier` mentions (lines ~1440-1524) all bind to `tools/mado-tripwire.py` (classifier SHA `46c82902`, `8c742093`, `e1dc8029`, `cd9da20c`), a different tool. No retirement entry names this capability.
- Claim-form check: the row's own caveat (`plan_safe` is not arbitrary-command safety/host prevention; unlisted wrappers unanalyzed) is carried in the report; no overclaim detected — the report explicitly scopes the observation to the two named commands plus the section's controls and declines to score the caveat.

## Findings

- **No defect.** Observed status, exit codes, key output, command form and superseding pointer all reproduce at the correct revision.
- Cosmetic (non-blocking): the report cites the round-16 heading `## Round 16 — committed results and bounded author verdicts` at `SCORECARD.md:740`; the heading is at `:737` (line 740 is the measured-commit text inside it). The ledger line itself names only `:782` and `:1591-1592`, both correct.
- Residual risk: the frozen replay is a pin match, not a live capture — the report states this itself ("byte-level pin check, not a live capture"). The claim "no later round changed the tool" rests on `git log` over the path, which I reproduced; rename history is a theoretical gap but the sha256 equality with the round-16 receipt makes it moot.

## Verdict

`RECHECK CapFiniteDeclaredActionClas782: agree`
