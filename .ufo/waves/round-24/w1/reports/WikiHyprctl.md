# WikiHyprctl — C1 source-opener report

Axis: C1 coverage, documentary source for Hyprland rule attribution. This is a source-opening handoff, not a C1 counter or judge result.

## Opened source and receipt

- Discovered with the local wiki clone search (`hyprctl` in `/fast/scratch/hyaku/mado-r24/src/hyprland-wiki/content/`) and resolved to `content/configuring/core/advanced-configuration/using-hyprctl.md`.
- Pinned source: https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/advanced-configuration/using-hyprctl.md
- Fetched bytes: `.ufo/waves/round-24/fetch/w1/WikiHyprctl-1.bin`
- Exact fetch/receipt command: `timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/advanced-configuration/using-hyprctl.md -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiHyprctl-1.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiHyprctl-1.bin && wc -c < /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiHyprctl-1.bin`
- Outcome: curl succeeded (the chained receipt commands ran); SHA-256 `95d8b8422a1fd25229bfe350e05624d8a318c746803efb7f3893015bf7c417f0`; byte count `8239`.
- Pinned commit: `c66e8de21f5ecdc4bc5e278e7d94800ea10957af`. Relevant line anchors: `192-200`, `238-262`, `284-295`.

## Observations from the bytes

- Lines 192-200 document `getprop` as getting a property value of a window; syntax takes `<window> <property>`, and the property is described by reference to `set_prop`.
- Lines 238-262 list `clients` as listing all windows with their properties, and `workspacerules` as getting the list of defined workspace rules.
- The same usage list describes `configerrors` as listing current config parsing errors (line 258), and `rollinglog` as printing the log tail with `-f/--follow` support (line 259).
- Lines 292-295 describe `r` as forcing a state refresh after commands, with layout or rule changes as examples.

Inference, not an observation about runtime: these are documented query, listing, log, and refresh affordances. The page does not specify a link from a particular client's resulting property/state to the window or layer rule that caused it. `workspacerules` is explicitly about defined workspace rules; that description alone is not a record of which rule produced an applied effect. Host behavior remains **[UNK]**. No host/compositor queries were run.

Scoped term sweep on the fetched page used the regex `workspacerules|windowrules|layerrules|clients|getprop|rollinglog|configerrors`. Matches were at lines 192, 197, 245, 246, 258, and 259 (the listed topics above); there were no `windowrules` or `layerrules` matches in this page sweep. This is limited to this file, not a claim about all Hyprland documentation or the implementation.

## Proposed C1 claim rows

All four quotes were checked against the fetched bytes with whitespace collapsed. Exact check command:

`timeout 10s python3 -c 'import sys; from pathlib import Path; s=Path(sys.argv[1]).read_text(encoding="utf-8"); qs=["clients              - lists all windows with their properties", "hyprctl getprop <window> <property>", "workspacerules       - gets the list of defined workspace rules", "- `r` - force state refresh after issuing commands (e.g., layout or rule changes)"]; norm=lambda x:" ".join(x.split()); matches=[norm(q) in norm(s) for q in qs]; print("whitespace-collapsed quote matches:", matches); raise SystemExit(0 if all(matches) else 1)' /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiHyprctl-1.bin`

Output: `whitespace-collapsed quote matches: [True, True, True, True]`.

| A1 | The documented `clients` command lists all windows with their properties. | S? | "clients              - lists all windows with their properties" |
| A2 | The `getprop` command accepts a window and property argument to retrieve a window property. | S? | "hyprctl getprop <window> <property>" |
| A3 | `workspacerules` is documented to list defined workspace rules. | S? | "workspacerules       - gets the list of defined workspace rules" |
| A4 | The `r` option can force state refresh after issuing commands, including rule changes. | S? | "- `r` - force state refresh after issuing commands (e.g., layout or rule changes)" |

## Proposed SOURCES row

| S? | Using hyprctl — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/advanced-configuration/using-hyprctl.md | docs | A | hyprctl clients/getprop, defined workspace-rule listing, refresh and log descriptions | content/configuring/core/advanced-configuration/using-hyprctl.md:192-200,238-262,284-295 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:95d8b8422a1fd25229bfe350e05624d8a318c746803efb7f3893015bf7c417f0, 8239 B> | Documents window property/client queries, a defined workspace-rule listing, and log/refresh commands; not rule-to-effect attribution | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Gates and bounds

- No source bytes were edited; the only created files are this report and the required fetch receipt.
- No tool was installed or updated.
- No lane integration, C1 counter, judge, build, or test was run. The `S?` source id and proposed rows await the integrator; no C1 verdict is claimed.
