# ExecC1After — C1 after-measurement (round-39 w1, inline v2 wave)

Seat: `ExecC1After` (leaf executor). Scope: C1 re-registration after-measurement at the freeze commit and tip; manifest byte-copy verification at base. No tool installs (stdlib + read-only git only; no pacman/uv/npx). No files written outside the seat dir except this report.

## Environment

- Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`
- Tip == freeze commit: `457d1b125932c1e0d797061a2156b917bcd7edaa` (HEAD, `git rev-parse HEAD`), "round-39: freeze registration + base receipts + inherited r38 seat reports"
- Base: `08be4eb7fd13358ed29b096e8924005d46ac409c` (registration.md §Base; `git log` confirms `08be4eb` is the parent of the freeze commit)

## Measurements

Both runs used `python3 -I quality/check-r38-discrimination.py --c1 quality/counters/c1-r38-event-ground.py --c2 quality/counters/c2-r38-eventq.py --manifest .ufo/waves/round-39/c1/manifest.json`; stdout saved, `echo "exit=$?"` appended.

### Freeze commit (`--rev 457d1b125932c1e0d797061a2156b917bcd7edaa`)
- Exit: 0
- stdout (`.../w1/ExecC1After/after-freeze.txt`, 20 lines): all 19 controls `ok=1`; line 20:
  `MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET`
- `--out` file: `.../w1/ExecC1After/after-freeze-out.txt` (1672 bytes)

### Tip (`--rev $(git rev-parse HEAD)` = `457d1b125932c1e0d797061a2156b917bcd7edaa`)
- Exit: 0; TIP echo confirmed `457d1b125932c1e0d797061a2156b917bcd7edaa` (tip == freeze commit)
- stdout (`.../w1/ExecC1After/after-tip.txt`, 20 lines): identical 19/19, line 20:
  `MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET`
- `--out` file: `.../w1/ExecC1After/after-tip-out.txt` (1672 bytes)

Both files and their `--out` twins are 1672 bytes; freeze and tip content identical (same commit).

## Manifest byte-copy verification

- Working tree: `cmp .ufo/waves/round-39/c1/manifest.json .ufo/waves/round-38/controls/manifest.json` → exit 0 (identical)
- At base: `cmp <(git show 08be4eb...:.ufo/waves/round-38/controls/manifest.json) <(git show 457d1b...:.ufo/waves/round-39/c1/manifest.json)` → exit 0 (round-39 c1 manifest at freeze == round-38 landed controls manifest at base)
- sha256 (both files, and both `git show` streams): `96965518dc8ad98b52b28b406d66841758c80fd75610f9b94e0239b8adf838c8`

## Evidence retention

- `.../w1/ExecC1After/after-freeze.txt`, `after-freeze-out.txt`, `after-tip.txt`, `after-tip-out.txt` (all in seat dir)
- This report at `.ufo/waves/round-39/w1/ExecC1After.md`

## Result

C1 after-measurement: TARGET_MET at freeze commit and tip (19/19, exit 0). Manifest confirmed byte copy of the round-38 landed manifest at base. No blockers, no risks beyond the declared C1 residual (fabricated artifacts may pass — declared in registration.md §C1).
