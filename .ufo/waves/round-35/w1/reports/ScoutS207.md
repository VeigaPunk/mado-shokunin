# ScoutS207 — idle.sh re-open (round-35, 2026-10-24)

Scoped read-only re-open of `/home/vgpnk/.local/share/omarchy/default/waybar/indicators/idle.sh`,
compared against `.ufo/waves/round-35/fetch/S207.receipt.txt`. Script was not executed.

## sha256

```
6d8d2c11d3c3b15fa0aa31a830410c98d9e630a7683a9cedffb888d10f0f1750
```

Measured via `sha256sum` at write time. **Identical to receipt line 3** — file unchanged since
the receipt was taken. Hash equality also implies the 159-byte size recorded on receipt line 4.

## Full body (7 lines)

```
     1	#!/bin/bash
     2	
     3	if pgrep -x hypridle >/dev/null; then
     4	  echo '{"text": ""}'
     5	else
     6	  echo '{"text": "󱫖", "tooltip": "Idle lock disabled", "class": "active"}'
     7	fi
```

Byte-for-byte identical to the receipt's `--- body ---` block (receipt lines 6–12).

## Which branch renders the tooltip

The **`else` branch (line 6)** renders `"tooltip": "Idle lock disabled"`.

- `then` branch (line 4) — taken when `pgrep -x hypridle` succeeds, i.e. a `hypridle` process
  **is running**: emits `{"text": ""}`, no icon, no tooltip. Indicator hidden.
- `else` branch (line 6) — taken when `pgrep` exits non-zero, i.e. **no hypridle process**:
  emits icon `󱫖`, tooltip `Idle lock disabled`, waybar class `active`.

The tooltip string appears exactly once in the file (consistent with the receipt's
`--- tooltip count ---` of `1`).

## Comparison with S207.receipt.txt

| Field | Receipt | Re-open | Match |
|---|---|---|---|
| sha256 | `6d8d2c11…f1750` | `6d8d2c11…f1750` | yes |
| body lines | 7, verbatim | 7, verbatim | yes |
| tooltip count | 1 | 1 | yes |
| branch claim | "prints the tooltip Idle lock disabled when it [hypridle] is absent" | else branch, taken on `pgrep` failure (hypridle absent) | yes |

No drift. Receipt is fully corroborated by this re-open.
