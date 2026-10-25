# RevengerNaiveMismatch — the 14-of-70 naive mismatch

Seat `RevengerNaiveMismatch`, mado round 40 / hyaku run 7 / w1 (inline v2 wave), 2026-10-25.
Target: reconstruct the naive run (native replies normalised to the base `--getoption`
format, fed to the BASE tool) and list the mismatch rows with cause classes; report what a
reader would wrongly conclude without the conversion table.

## Method (all read-only, no compositor verb run by this seat)

1. Read the frozen registration (`.ufo/waves/round-40/registration.md`, freeze commit
   `5e7e885`), the frozen counter `quality/counters/c1-r40-live.py`, the controls
   `ctl/run-c1-controls.py` and the throwaway reference `c1/ctl-ref-tool.py.txt`.
2. Confirmed the BASE tool identity: `git show 9fc511d:tools/mado-options.py | sha256sum`
   = `461f8c3c…fb03a` = sha256 of the working-tree `tools/mado-options.py` (the working
   tree still holds the base tool; no `--live`). Git reads only, no mutation.
3. Naive normalisation: parsed the frozen capture `c1/native-capture.jsonl` (70 lines,
   one JSON object per declared key: `{"option":K,"set":B,"<form>":V}`, form in
   int|float|str|custom; recount int=44 float=5 custom=13 str=8). Each reply was mapped to
   the base `--getoption` record `{K: {"value": <text>, "custom_type": <form>, "set": B}}`
   where `<text>` is the literal value text (decimal int, float text, raw string) — **no**
   hyprlang conversion.
4. Ran the BASE tool: `python3 -I tools/mado-options.py --home /home/vgpnk --getoption
   naive.json` → rc 0, 70 rows with `agreement` labels.
5. Reference side (what the converter reports) re-derived with the frozen counter's model
   functions (`hl_int`, `gradient_text`, `gap_text`, `WEIGHTS`) plus per-key declarer state
   (`_decls`, `_angle`) from the throwaway reference resolver, and cross-checked against the
   w1 host census (`w1/RevHostCensus/census.jsonl`): converted text agree 70/70, label agree
   70/70.

Artifacts in this seat dir: `naive.json`, `labels.tsv` (all 70 rows), `mismatch.tsv`
(the 14 rows), `naive_repro.py`.

## Result: naive labels vs reference labels

| run | agreement | agreement* | mismatch | total |
|---|---|---|---|---|
| BASE tool, naive-normalised native replies | 50 | 6 | **14** | 70 |
| reference model (conversion table) | 62 | 8 | 0 | 70 |

The 8 agreement* keys under the reference model: `decoration:rounding`,
`general:border_size`, `general:col.active_border`, `general:gaps_in`,
`general:gaps_out`, `group:col.border_active`, `input:kb_layout`, `input:kb_options`
(matches `ExecutorLive/live-host-census.txt`). Under the naive run two of the eight flip to
mismatch (`general:col.active_border`, `group:col.border_active`); the six remaining rows
stay agreement* because the base tool's own scalar-vs-tuple rule absorbs `0` vs
`0 0 0 0` and exact string match absorbs `br`/`compose:caps`.

## The 14 mismatch rows

| # | key | form | declared (owner:line) | naive live text | converted (reference) | cause class |
|---|---|---|---|---|---|---|
| 1 | `animations:enabled` | int | `yes, please :)` (defaults/looknfeel.conf:82) | `1` | `1` | bool prose |
| 2 | `decoration:shadow:color` | custom | `rgba(1a1a1aee)` (:35) | `ee1a1a1a 0deg` | `ee1a1a1a 0deg` | colour rgb/rgba vs ARGB |
| 3 | `general:col.active_border` | custom | `rgb(e68e0d)` (theme/hyprland.conf:4) | `ffe68e0d 45deg` | `ffe68e0d 45deg` | colour rgb/rgba vs ARGB + gradient angle (inherited) |
| 4 | `general:col.inactive_border` | custom | `rgba(595959aa)` (:16) | `aa595959 0deg` | `aa595959 0deg` | colour rgb/rgba vs ARGB |
| 5 | `group:col.border_active` | custom | `rgb(e68e0d)` (theme/hyprland.conf:8) | `ffe68e0d 45deg` | `ffe68e0d 45deg` | colour rgb/rgba vs ARGB + gradient angle (inherited) |
| 6 | `group:col.border_inactive` | custom | `rgba(595959aa)` (:52) | `aa595959 0deg` | `aa595959 0deg` | colour rgb/rgba vs ARGB |
| 7 | `group:col.border_locked_active` | custom | `rgba(33ccffee) rgba(00ff99ee) 45deg` (:53) | `ee33ccff ee00ff99 45deg` | `ee33ccff ee00ff99 45deg` | colour rgb/rgba vs ARGB |
| 8 | `group:col.border_locked_inactive` | custom | `rgba(595959aa)` (:54) | `aa595959 0deg` | `aa595959 0deg` | colour rgb/rgba vs ARGB |
| 9 | `group:groupbar:col.active` | custom | `rgba(00000040)` (:70) | `40000000 0deg` | `40000000 0deg` | colour rgb/rgba vs ARGB |
| 10 | `group:groupbar:col.inactive` | custom | `rgba(00000020)` (:71) | `20000000 0deg` | `20000000 0deg` | colour rgb/rgba vs ARGB |
| 11 | `group:groupbar:font_weight_active` | custom | `ultraheavy` (:59) | `1000` | `1000` | weight name |
| 12 | `group:groupbar:font_weight_inactive` | custom | `normal` (:60) | `400` | `400` | weight name |
| 13 | `group:groupbar:text_color` | int | `rgb(ffffff)` (:68) | `4294967295` | `4294967295` | int-colour form |
| 14 | `group:groupbar:text_color_inactive` | int | `rgba(ffffff90)` (:69) | `2432696319` | `2432696319` | int-colour form |

Every row's reference conversion equals the live value (`ref_ok=True`), so all 14 are
presentation/grammar differences, not config drift. Owner layer: 12 rows live in the
defaults tree (`.local/share/omarchy/default/hypr/looknfeel.conf`), 2 in the theme
(`.config/omarchy/current/theme/hyprland.conf`).

## Cause classes (counts)

- **colour rgb/rgba vs ARGB — 9 rows** (2,4,6–10, + 3 and 5 where it co-occurs with the
  inherited angle): declared spellings `rgb(rrggbb)` / `rgba(rrggbbaa)` become one lowercase
  unpadded ARGB hex word per stop, e.g. `rgba(1a1a1aee)` → `ee1a1a1a`, `rgb(e68e0d)` →
  `ffe68e0d`, `rgba(33ccffee) rgba(00ff99ee) 45deg` → `ee33ccff ee00ff99 45deg`.
- **gradient angle (inherited) — 2 rows** (3, 5): `general:col.active_border` and
  `group:col.border_active` are declared twice — defaults `looknfeel.conf:4` defines
  `$activeBorderColor = rgba(33ccffee) rgba(00ff99ee) 45deg`, resolved at :15/:51; the theme
  redeclares the same key with `rgb(e68e0d)` (no `deg` token). The Hyprland gradient handler
  clears colours and only changes the angle when a `deg` token is present, so the live reply
  keeps the previous declarer's `45deg`: `ffe68e0d 45deg`. The naive run cannot explain the
  angle token, which appears in no single declaration.
- **weight names — 2 rows** (11, 12): declared `ultraheavy`/`normal` print as the numeric
  weight (`1000`/`400`, `ComplexDataTypes.hpp` parseWeight table, case-insensitive).
- **int-colour forms — 2 rows** (13, 14): `rgb(ffffff)` → 0xFFFFFFFF = 4294967295;
  `rgba(ffffff90)` → 0x90FFFFFF = 2432696319 (ARGB packed unsigned decimal).
- **bool prose — 1 row** (1): declared `yes, please :)` → int `1` (hyprlang
  `configStringToInt` prefix true/on/yes → 1). The base tool's boolean set
  (`true/yes/on/1` exact) does not contain `yes, please :)` and its float path cannot parse
  it, so it mislabels a key the compositor applies correctly.

## What a reader would wrongly conclude without the conversion table

1. **"14 of 70 options are out of sync / not applied."** All 14 have `set: true` and their
   converted value equals the live value; the naive mismatch list is entirely false alarms.
   A reader hunting for real drift would waste effort on rows that are perfectly healthy.
2. **Colours: "the declared colour is not what the compositor uses".** Naive compare
   `rgb(e68e0d)` vs `ffe68e0d 45deg` suggests the alpha/prefix is lost or the value
   rewritten. Actually the compositor stores ARGB and prints lowercase unpadded hex; the
   declared string *is* the live colour.
3. **`col.active_border` / `col.border_active`: "the live state contains a stale 45deg
   from nowhere"** (possibly from an old profile, or the two keys "randomly agreeing" with
   each other). It is the angle-inheritance rule: one declarer per key keeps the previous
   declarer's angle because the gradient handler only sets the angle when a `deg` token is
   present.
4. **Weights: "`ultraheavy`/`normal` are ignored (unsupported names)"** — the compositor
   maps names to numeric weights; the reply is the *resolved* value, not a refusal.
5. **`animations:enabled`: "`yes, please :)` is not a real value / the option is set to 1
   by a default despite the file"** — it is a real hyprlang bool whose `yes` prefix
   converts to 1.
6. **Int-colour forms: "`text_color` changed type (colour → integer) or overflowed"** —
   the int form carries the ARGB colour as unsigned decimal; 4294967295 is exactly 0xFFFFFFFF.
7. The naive run also *hides* real shadowing: the six rows that stay agreement* under the
   base rule (`gaps_in`/`gaps_out` `0` vs `0 0 0 0`, `border_size`, `rounding`, kb strings)
   still have two declarers each; a reader relying only on the naive agreement counts would
   not see the shadowed declarer uncondition.

## Grounding and limits

- Re-derived from the frozen capture and the committed base tool; no `hyprctl` verb was run
  by this seat, no write outside this seat dir, no git mutation, no tool installs (system
  `python3`/`git` only; pacman untouched).
- Reference conversions use the frozen counter's model; the angle-inheritance state comes
  from the throwaway reference resolver (`ctl-ref-tool.py.txt`) re-parsing the host tree
  (read-only). Cross-check vs `RevHostCensus/census.jsonl`: converted agree 70/70, label
  agree 70/70.
- One host, one compositor state, one captured moment; the capture is the out-of-distribution
  check of C1 and was taken before this seat ran.
