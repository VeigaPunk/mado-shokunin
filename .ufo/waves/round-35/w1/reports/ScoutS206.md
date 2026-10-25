# ScoutS206 — waybar config.jsonc idle-indicator verification

Scope: re-read `/home/vgpnk/.config/waybar/config.jsonc` (read-only); compare with
`.ufo/waves/round-35/fetch/S206.receipt.txt`. Date: 2026-10-24.

## Live file facts

- sha256: `a408a33df48a39dc16214124dd0b86d6ab03e13802bac173146ae8a858aae829`
- byte length: `6354`
- `custom/idle-indicator` module block: lines **207–212**
  ```
  207:  "custom/idle-indicator": {
  208:    "on-click": "omarchy-toggle-idle",
  209:    "exec": "$OMARCHY_PATH/default/waybar/indicators/idle.sh",
  210:    "signal": 9,
  211:    "return-type": "json"
  212:  },
  ```
- on-click handler line: **208**
- exact handler text: `"on-click": "omarchy-toggle-idle",`
- Module-list presence: **yes** — line **18**, inside `modules-center` (lines 11–20), between
  `custom/screenrecording-indicator` (17) and `custom/notification-silencing-indicator` (19).
- Exactly one `on-click` key in the block (no `on-click-right`/`on-click-middle`).

## Receipt comparison (S206.receipt.txt)

| Claim | Receipt | Live | Match |
|---|---|---|---|
| sha256 | `a408a33d…aae829` (line 3) | same | yes |
| bytes | `6354` (line 4) | `6354` | yes |
| list entry | line 18 `"custom/idle-indicator",` | line 18 identical | yes |
| block open | line 207 | line 207 | yes |
| on-click | line 208 `omarchy-toggle-idle` | line 208 identical | yes |
| exec/signal/return-type | 209 / 9 / json (lines 16–18) | identical | yes |
| on-click count | 1 (line 22) | 1 | yes |
| summary "located" line | 207 opens, 208 runs `omarchy-toggle-idle` | confirmed | yes |

Verdict: receipt is byte-for-byte consistent with the live file; no drift since the receipt was
written. Hash and size identical, every quoted line number and content verified in place.
