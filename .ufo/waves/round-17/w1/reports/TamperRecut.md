# TamperRecut — R16-V1 tamper control re-receipt

Seat: MadoR17.TamperRecut. Round 17, wave 1. Lane root
/home/vgpnk/Projects/shokunin/mado-shokunin. Measured at lane HEAD
`0175f13d83dceb9344fd0ecc5f94aa4aac5dfb53`.

## Files changed (assigned only)

- `.ufo/waves/round-17/evidence/frozen-tampered-recut.json` — new receipt, both
  tampered and control runs.
- `.ufo/waves/round-17/w1/reports/TamperRecut.md` — this report.

## Behavior observed

Copied `.ufo/waves/round-16/frozen` (`expected.json`, `plan.json`,
`policy.json`) into two fresh `mktemp` dirs. In the tampered copy, altered
`plan.json` by exactly one byte: argv element `"libinput"` → `"libinpuv"`
(ASCII `t` → `v`, length preserved; file remains valid JSON and still has
`argv[0] "sudo"`, so only the digest pin can catch it).

- Tampered copy: `python3 -I tools/mado-action-plan.py --frozen
  /tmp/mado-r17-frozen-tamper-PDanoS` → exit **2**,
  `MADO_PLAN: snapshot_tampered`, detail
  `plan.json sha256 052c03b2…f157 != pinned 82bc765…ebc3`.
- Untampered control: same command on
  `/tmp/mado-r17-frozen-control-kGThY6` → exit **0**,
  `MADO_PLAN: frozen_match`, detail
  `frozen verdict denied_executable:sudo/1 matched`.

Both match expectations.

## Exact retained evidence

- `.ufo/waves/round-17/evidence/frozen-tampered-recut.json` — full receipt:
  label, `measured_commit` `0175f13…`, `action_gate_sha256`
  `226220ae41436506c048258aff15fff83577acf0ae71ffa955d585a18ba5aea3` (= the
  round-16 final digest), pristine snapshot digests, tamper description,
  post-tamper digest, exact commands, exits, stdout, stderr for both runs.
- Detection mechanism (read, tools/mado-action-plan.py `run_frozen`,
  ~l.461–470): `expected.json`'s pinned `plan_sha256`/`policy_sha256` are
  compared against fresh SHA-256 of the files actually read; any mismatch →
  `snapshot_tampered`/2 before replay. The R16-V1 defect does not re-fire
  because the frozen `expected.json` now pins
  `expected_finding denied_executable:sudo / expected_exit 1`, a reachable
  pair at current content (the round-16 receipt at `9dcf248` recorded
  `frozen_error` "pair 1/'denied_executable:sudo' is unreachable" — that
  defect was fixed by the final commit).

## Risks / blockers

None. Receipt evidence only — tmp dirs left under `/tmp`
(`mado-r17-frozen-{tamper-PDanoS,control-kGThY6}`) and may be swept by tmp
cleanup; all digests/outputs are committed in the receipt.

## Tooling installs

None. Only `cp`, `mktemp`, `sha256sum`, `git rev-parse`, `edit`, and
`python3 -I tools/mado-action-plan.py` (read-only script on /tmp copies) —
permitted. No pacman/sudo/systemctl/hyprctl or any host probe (HOST PAUSE
observed; L1 reminder acknowledged).
