# RevHostCensus — mado r40 w1 — independent host census

**Verdict: my own census confirms the provisional 62 agreement / 8 agreement\* / 0 mismatch
exactly, including the same 8 keys. Zero disagreements with the provisional census.**

Runtime (verified, my own calls): `hyprctl version` → Hyprland 0.56.2, commit
`efb50993780079460b0cbed1363e2166a2de1d9f`, Hyprlang built against 0.6.8 (`hypr-version.txt`).
`hyprctl` at `/usr/bin/hyprctl`; `HYPRLAND_INSTANCE_SIGNATURE` present in the exec shell.

## Method (independent — no lane tool code read or reused)

1. **Key universe** (the one given input from the tool): `python3 -I tools/mado-options.py
   --home $HOME` → 70 keys (`keys.json`, `keylist.txt`).
2. **Live side, mine:** 70 × `hyprctl getoption -j KEY` (read-only verb), every call exit 0
   (`live.jsonl`, `live-exits.txt`: `70 0`). Forms observed: int 44, float 5, custom 13, str 8;
   no `no such option`.
3. **Declared side, mine:** own throwaway resolver `census_resolver.py` over the host tree
   rooted at `~/.config/hypr/hyprland.conf`: depth-first `source =` (with `~` expansion and
   sorted glob expansion), global hyprlang variables with sequential parse-time substitution,
   brace sections folded to dotted keys, last declarer wins. Every source resolved
   (incl. `~/.config/omarchy/current/theme/gum.env.conf` and the toggles glob); every one of the
   70 keys has ≥1 declarer; 87 keyed directives tracked overall (the rest are positional
   `bind*`/`env`/`monitor`/`windowrule`/`animations:bezier` style lines).
4. **Host conversion, mine, per observed native form:** `configStringToInt` semantics (0x hex;
   decimal; `rgb()`/`rgba()` hex → packed `0xAARRGGBB` for the int-typed color keys
   `group:groupbar:text_color*`; truthy/falsy); float/str direct; custom per type — gradient
   (colors cleared each declaration, `AARRGGBB` lowercase, angle kept when a later declaration
   has no `deg` token — state mutated per option in declaration order), CSS gap expansion
   (`0` → `0 0 0 0`), font-weight names (`ultraheavy`→1000, `normal`→400).
5. **Labels** (lane divergence vocabulary): agreement = live == converted declared ∧ set=true ∧
   one declarer; agreement\* = same but key has >1 declarer; mismatch otherwise.

## Result

`census: checked=70 agreement=62 agreement*=8 mismatch=0` (full per-key table: `census.jsonl`).

The 8 agreement\* keys (each exactly 2 declarers; live still equals the resolved last declarer
after host conversion):

| key | declarers (file:line) | last decl → live |
|---|---|---|
| `decoration:rounding` | looknfeel.conf:29, toggles/window-no-gaps.conf:9 | 0 → 0 |
| `general:border_size` | looknfeel.conf:12, window-no-gaps.conf:5 | 0 → 0 |
| `general:gaps_in` | looknfeel.conf:9, window-no-gaps.conf:4 | 0 → `0 0 0 0` |
| `general:gaps_out` | looknfeel.conf:10, window-no-gaps.conf:3 | 0 → `0 0 0 0` |
| `general:col.active_border` | looknfeel.conf:15, theme/hyprland.conf:4 | `rgb(e68e0d)` → `ffe68e0d 45deg` |
| `group:col.border_active` | looknfeel.conf:51, theme/hyprland.conf:8 | `rgb(e68e0d)` → `ffe68e0d 45deg` |
| `input:kb_layout` | default input.conf:3, `~/.config/hypr/input.conf:10` | br → br |
| `input:kb_options` | default input.conf:6, `~/.config/hypr/input.conf:11` | compose:caps → compose:caps |

Mechanism evidence for the non-obvious cells:

- **Angle inheritance** (`col.active_border`, `col.border_active`): theme redeclares a single
  colour with no `deg`; live reads `ffe68e0d 45deg` — the 45° set by the earlier looknfeel
  declaration survives, colours are cleared. Single-declarer gradients (`col.inactive_border`,
  `border_inactive`, `border_locked_inactive`, `groupbar:col.*`, `shadow:color`) all read
  `<color> 0deg` as declared; `col.border_locked_active` (declared once, with angle) reads
  `ee33ccff ee00ff99 45deg` exactly.
- **`animations:enabled = yes, please :)`** (looknfeel.conf:82): live `int 1`, `set=true`.
  Mechanism pinned in hyprlang v0.6.8 `src/config.cpp:259-262` — `configStringToInt` uses
  *prefix* truthiness (`VALUE.starts_with("yes")` → 1), and `m_bSetByUser=true` is set after a
  successful parse (same file, line 513). So this is a clean **agreement** (single declarer),
  not an exception.
- **Int-typed colors**: `group:groupbar:text_color = rgb(ffffff)` → 4294967295 and
  `text_color_inactive = rgba(ffffff90)` → 2432696319 (0x90FFFFFF) — `rgba(RRGGBBAA)` packs as
  `0xAARRGGBB`, matching live exactly.
- **Variables**: sequential/global substitution confirmed by live data — theme's
  `$activeBorderColor = rgb(e68e0d)` redefinition applies only to lines parsed after it (theme
  `col.active_border`/`col.border_active` read `ffe68e0d`), while looknfeel's
  `col.border_locked_active` still reads the old variable's `ee33ccff ee00ff99`.

Cross-checks: my live capture is value-identical to the frozen
`.ufo/waves/round-40/c1/native-capture.jsonl` (same 70-key set, zero field diffs — only float
text formatting `0.6` vs `0.600000` differs). mado-options' owner/line for every key agrees with
my resolver's last declarer.

## Diff vs provisional census (62 / 8 / 0)

None. Same counts, same partition, same 8 keys. The provisional census is independently
reproduced under my own resolver, my own capture and my own converter.

## Residual risk / verification gaps

- Compositor state is a moving target in principle; census is valid for the capture instant
  (2026-10-25). Both captures (mine, L1's) agree, so no drift occurred between them.
- Glob ordering for the toggles source is assumed alphabetical (`flags.conf` before
  `window-no-gaps.conf`); unobservable here since `flags.conf` declares no keys.
- My converter covers the value spellings present in this tree (packed hex colors, `deg`
  gradients, single-token gaps, named/numeric weights, decimal ints/floats). hyprlang also
  accepts comma-separated `rgb(r, g, b[, a])`, `px`-suffixed ints and bare hex — none occur in
  the 70 declarations; their conversion is untested here (out of scope for this census).
- I did not re-verify mado-options' static parser beyond owner/line agreement on the last
  declarer; multi-declarer *counting* is from my own walker only.

## Artifacts

All in `.ufo/waves/round-40/w1/RevHostCensus/`: `census_resolver.py` (my script),
`census.jsonl` (per-key rows), `live.jsonl` + `live-exits.txt` (my 70-call capture, all exit 0),
`keylist.txt`, `keys.json`, `hypr-version.txt`, `hyprlang-config.cpp` (v0.6.8 source fetched for
the prefix-truthiness evidence).

## Tooling

No tools installed or updated (tooling authorization noted; nothing needed). System `curl` used
once, read-only, to fetch hyprlang v0.6.8 `src/config.cpp` from the official GitHub repo for
cited evidence. Compositor verbs used: `hyprctl getoption -j` ×70 and `hyprctl version` ×1 —
both on the allowed read-only list. No writes outside my seat directory and this report.
