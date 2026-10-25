# ScribeConsider — mined proposal, grounded

**Source:** `considerthese/2026-10-24.md` (window 2026-10-21 09:52 → 2026-10-24 09:52 BRT),
§"Self-improvement suggestions (proposals only; not acted on)", item **4** (file line 49).
Grounded 2026-10-24. The considerthese file was not edited.

## What the proposal demands

> "Suggest the next desktop table explicitly. With binds, animations and workspace rules
> covered, I could read PROVINCE.md and propose which Hyprland surface is next (window rules,
> monitors, layer rules) with the sources that would ground it, so the planner has a concrete
> domain option next to the self-audit queue."

Demand: read `PROVINCE.md`; name the next Hyprland config table the lane should resolve
statically; ground the choice in sources. Motivation is the file's own "Open debt" line —
no `tools/` or `corpus/knowledge/` change since round 27; four straight self-audit rounds.

## What the lane already holds

- `tools/mado-binds.py` (r25), `tools/mado-anims.py` (r26), `tools/mado-wsrules.py` (r27) —
  the three-table static-resolver pattern, each verified against the matching `hyprctl -j`
  oracle on host v0.56.2.
- `PROVINCE.md` owns `~/.config/hypr/` incl. rules, and names "display behavior on this host".
- Sources already mined: **window rules** are deep — S017/S030 wiki rows, S154–S160 tagged
  v0.56.2 rule-engine/window-rule code, S162 ConfigManager handlers, S168 rule semantics;
  **layer rules** S163 + S166; **monitors** — no dedicated rows (only kitty `child-monitor.c`,
  unrelated); `hyprctl monitors/layers` live reads already exercised by `mado-verify.sh` and
  `remaining-planes-census.md` §4.
- `corpus/knowledge/window-rule-effects-getprop.md` + `rule-attribution-r24.md` already chart
  the getprop/property read route.

## Grounded evidence (verified first-hand, 2026-10-24, host Hyprland 0.56.2 `efb5099`)

| Candidate table | Oracle verb exists? | Declared lines on host | Verdict for the r27 pattern |
|---|---|---|---|
| **window rules** | `hyprctl windowrules -j` → `unknown request` (same for `rules`, `layerrules`) | 78 `windowrule =` lines across `~/.config/hypr` + omarchy defaults | Largest declared surface, but **no readback oracle** — the r25–r27 predict-vs-`hyprctl -j` method does not transfer. Verification must route through `clients -j`/`getprop` (already the S016–S020, r24 line of work), a different measurement shape. |
| **layer rules** | no verb | 2 `layerrule =` lines | Thin surface, no oracle — poor cost/insight. |
| **monitors** | `hyprctl monitors -j` works; returns 36 fields | 1 `monitor =` line (`monitors.conf:10` `DP-1, 3440x1440@100, 0x0, 1`) | Only candidate with a live JSON oracle. But most fields are runtime state (`dpmsStatus`, `focused`, `activeWorkspace`, `vrr`, …); a static resolver can predict only the declared subset (name, mode, position, scale, transform). |

Other first-hand checks:
- `hyprctl help` → `unknown request` (no help verb on v0.56.2).
- `hyprctl workspacerules -j` → returns the rule table `[{"workspaceString":"1",…}]` —
  confirms the proposal's premise that the r27 oracle exists.
- **Adjacent defect found while grounding:** `PROVINCE.md` "Round-23 refinement" claims its
  table "covers every tracked file under `tools/`", but `tools/mado-wsrules.py` (landed r27)
  has no row — the inventory is stale.

## Disposition

**→ lesson** (a `corpus/lessons/round-34` entry or appended to the daily reflection chain),
not a QUALITY.md criterion and not a SOURCES row:

- Not QUALITY: the proposal is domain planning, not a rubric. (The PROVINCE inventory gap
  could feed the existing index/provenance gates, but that is a separate defect.)
- Not a SOURCES row: the grounding evidence is host probe output and existing S-rows, not a
  new external source to register.
- As a lesson, the transferable facts are: (a) the hyprctl-oracle table frontier on v0.56.2
  is *exhausted for rules* — `windowrules`/`layerrules` have no verbs, so rule work must use
  the per-window `clients`/`getprop` attribution route the lane already documented; (b) the
  only unresolved `hyprctl` table with both an oracle and a declared-file surface is
  **monitors** (1 line, small but cleanly verifiable), making it the honest "next table" if
  the lane wants a cheap domain win; (c) a bigger swing — static window-rule *resolution with
  getprop-spot attribution* — is possible but is a different claim shape, so a round that
  picks it must re-scope its oracle before promising "predicts the table".

Concrete next-round option the note grounds: `tools/mado-monitors.py` resolving the declared
`monitor =` set vs `hyprctl monitors -j` declared-subset fields — or a window-rule matcher
whose oracle is `clients -j` tags/`getprop` fields, explicitly not a table oracle.
