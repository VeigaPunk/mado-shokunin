# ReviewResolver — round 14 / w1 (rendered report, pass 2)

Companion: `.ufo/waves/round-14/w1/ReviewResolver.md` (full detail).

## Bound bytes

| Pass | sha256 | Notes |
|---|---|---|
| 1 (baseline) | `037b05dc…6569` | HEAD `873ff081`, clean |
| 2 (landed diff) | `0a2bf860…6948` | worktree M, blob `06d1e161…`, +162/−11 |

No external sources. No tools installed or updated. No checks run.

## Pass-2 result

Closed: F1 (direct `-f`), F2 (any non-regular match FAILs), F3 (N10 asserts no_gaps NOTE), F4 (N9 uses default/hypr/windows.conf), F5 (`non-regular:` token, `~/%q` names), F6 (`mapfile`, `%q`), F7 (symlink policy, documented), F11 (N12 order swap, PASS sources row).

Acknowledged: F10 (PIN_MADO untouched; R10 red until L1 recut).

Carried, Low: F8/F9 (glob detection on ROOT-prefixed `$x`; `*` only) — R1.

New, Low: R2 (dangling-glob `$t` repeated per match). Note: R3 (symlink containment not checked; matches stated policy).

No actionable defect in N9–N12 fixture logic. Expected outputs checked by reading, not executed.

## Gaps

- Shell semantics reasoned, not executed [INFERENCE].
- Hyprland directory/glob handling not verified upstream.
- Pin re-cut is L1's job.

## Final source review — ef50e262… (high/medium correctness only; no checks)

- Final bytes sha256 `ef50e262f311d74e05afd558883415d2f47fa2a0247a0c834e37f49cb60c742b`. High: none. Medium: none.
- Glob transport, dangling-once, direct `-f`, exact helper and fixture strings N4/N9–N16 agree with the code path (traced, not run).
- Correction: the N16 boundary-hash caveat does not apply; `boundary_hash` covers `$ROOT/.config` only (3668) and N16's file is under `.local/state`.
- Latent Low (out of scope): `boundary_hash` line-splits newline-named files under `.config`; not exercised.
- Carried: F8/F9 Low; R3 note; R10 red until L1 recut. No checks run.
