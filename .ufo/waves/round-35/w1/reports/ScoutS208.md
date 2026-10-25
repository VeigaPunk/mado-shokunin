# Scout S208 — omarchy-menu Idle Lock entry (re-verified 2026-10-24)

## Scope
Read-only re-check of `/home/vgpnk/.local/share/omarchy/bin/omarchy-menu` against
`.ufo/waves/round-35/fetch/S208.receipt.txt`.

## Findings (re-executed at write time)

- `sha256sum` → `d196b086e961d524945a899c5eb6e1aa532d9594c924d78b78c1fff183a0f79d`
- Toggle-options string containing `Idle Lock`: **line 207**
  `local options="󱄄  Screensaver\n󰔎  Nightlight\n󱫖  Idle Lock\n󰂛  Notifications\n󰍜  Top Bar\n󱂬  Workspace Layout\n  Window Gaps\n  1-Window Ratio\n󰍹  Monitor Scaling\n  Direct Boot\n󰟵  Passwordless Sudo"`
- Case arm dispatching `omarchy-toggle-idle`: **line 212**
  `*Idle*) omarchy-toggle-idle ;;`
- Only one line in the file references `omarchy-toggle-idle` (dispatch arm count: 1).

## Comparison vs. S208.receipt.txt

| Field | Receipt | Re-check | Match |
|---|---|---|---|
| sha256 | d196b08…a0f79d | d196b08…a0f79d | yes |
| `Idle Lock` options string | line 207 | line 207 | yes |
| `omarchy-toggle-idle` case arm | line 212 | line 212 | yes |
| dispatch arm count | 1 | 1 | yes |

## Verdict
File unchanged since receipt (identical sha256). No drift; receipt remains accurate.
