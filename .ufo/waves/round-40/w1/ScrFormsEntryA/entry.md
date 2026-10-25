# What `hyprctl getoption -j` answers: the four native forms

source: S162
source: S173
source: S_FORMS_1
source: S_FORMS_2
verified-at: 2026-10-25
recheck: on-change

Lane: mado-shokunin. Round: 40 (claim C2 coverage; capability C1 `tools/mado-options.py --live`). Host measured: Hyprland 0.56.2 @ `efb50993780079460b0cbed1363e2166a2de1d9f`, hyprlang 0.6.8, `.conf` era (`hyprctl version`, 2026-10-25; no Lua surface). A `<<QUOTE id: …>>` slot carries a seat-verified candidate, or a fill hint where the text belongs to a receipt this seat did not write; L1 replaces the wrapper with the round-40 Gate quote.

ground: one option key's own answer from the running compositor — reply shape, the four native forms plus
`no such option`, the per-form conversion of a declared string, and the gradient angle a redeclaration
inherits. Held, not restated: include order and the last-declarer rule (`knowledge/config-drift-r12.md`,
`knowledge/config-option-table-r39.md` §1), the parser boundary that decides which lines are options (§2
there), the 56 held claim→`getoption` pairs and their divergence classes
(`knowledge/hyprctl-verification-layer.md` §2-§4).

## §1 The reply shape

**OBS** S_FORMS_2 (measured, 2026-10-25): one key answers one JSON object holding `option`, the single
form field and `set` — never a bare value; the form field is one of `int`, `float`, `str`, `custom`,
exactly one per reply, and the host's 70 declared keys split `forms int=44 float=5 str=8 custom=13` (sum 70): <<QUOTE S_FORMS_2: forms int=44 float=5 str=8 custom=13>>.

**OBS** S_FORMS_2 (measured): an unknown key is not an error — stdout carries the plain text
`no such option` and the exit status is 0 (`hyprctl getoption -j __mado_r40_no_such_option__` → `rc=0`),
so a parser that requires JSON must handle this string first: <<QUOTE S_FORMS_2: no such option>>.

**OBS** S_FORMS_2 (measured): `set` is the declarer discriminator, not the form — the undeclared
`misc:font_family` answers `{"option": "misc:font_family", "str": "Sans", "set": false }` (engine default)
while all 70 declared keys answer `set: true`: <<QUOTE S_FORMS_2: receipt line for the misc:font_family probe (set=false)>>.

**INF** The form follows the option's registered data type, not the declared spelling: `input:sensitivity`
is declared `0` (`default/hypr/input.conf:11`) and answers `{"float": 0.000000}`; a reader keying off the
config text mislabels it.

## §2 Per-form conversion table

| form | reply field | declared → answered | where the rule is |
|---|---|---|---|
| `int` | `"int": 0` | `0`→0; `true`/`on`/`yes` prefix→1; `false`/`off`/`no` prefix→0; `0x…`→hex; `rgb(RRGGBB)`→`FF`+hex; `rgb(r,g,b)`→`0xFF000000+rgb`; `rgba(r,g,b,a)`→`round(a*255)<<24`+rgb; `rgba(RRGGBBAA)`→RGBA rotated to ARGB | S173 |
| `float` | `"float": 0.000000` | decimal text compared numerically; `0` vs `0.000000` agrees | S173 |
| `str` | `"str": "dwindle"` | declared token compared exactly (trimmed); empty string is a value | — |
| `custom` gradient | `"<hex>[ <hex>]… <N>deg"` | each colour through the same colour conversion, printed `{:x}` (lowercase, unpadded) as ARGB, then `Ndeg`; the first token containing `deg` sets the angle and ends the scan (later tokens dropped); max 10 colours; no colour at all → one transparent colour | S162, S_FORMS_1 |
| `custom` CSS gap | `"<t> <r> <b> <l>"` | 1 token → all four; 2 → vertical,horizontal,vertical,horizontal; 3 → top,horizontal,bottom,horizontal; 4 → top,right,bottom,left | S_FORMS_1 |
| `custom` font weight | `"<int>"` | case-insensitive name lookup in a fixed map (`thin` 100 … `ultraheavy` 1000, `normal` 400) | S_FORMS_1 |

**OBS** S173 (hyprlang v0.6.8 `src/config.cpp`, blob `fa1b6898…`, 43049 B): colour and boolean spellings
are decided by the leading text, so a declared value may be prose that merely starts with a keyword: <<QUOTE S173: // now we need to RGBA -> ARGB. The config holds ARGB only.>>.

**OBS** S162 (ConfigManager.cpp @ `efb5099`, blob `9db68cf4…`, 90963 B): the gradient handler is a
hyprlang handler over the option's live data object, created once and reused; `configHandleGradientSet`
spans `:103-160` (destroy `:162-165`), outside the ranges the held S162 anchor cell lists
(`:419-451,590-623,893-968,2016-2093`) but inside the same pinned blob — L1 appends that range as an
erratum, never rewrites the row: <<QUOTE S162: CVarList2 varlist(std::string(V), 0, ' '); DATA->m_colors.clear();>>.

**OBS** S_FORMS_1 (`src/config/shared/complex/ComplexDataTypes.hpp` @ `efb5099`, blob `95733223…`,
6116 B): the gradient prints its colours unpadded lowercase (`std::format("{:x} ", c.getAsHex())`, `:72`)
and appends the angle as integer degrees (`:75`); the CSS gap prints as four integers in
top/right/bottom/left order, which is why a one-token declaration answers with four:
<<QUOTE S_FORMS_1: return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);>>.

**OBS** S_FORMS_2 (measured, 2026-10-25): the host exercises the table end to end — `general:border_size` declared `2` (`default/hypr/looknfeel.conf:12`) then `0` (`toggles/hypr/window-no-gaps.conf:5`) answers `{"int": 0}`; `animations:enabled` declared `yes, please :)` (`looknfeel.conf:82`) answers `{"int": 1}`; `general:gaps_in` declared `0` answers `{"custom": "0 0 0 0"}`; `group:groupbar:font_weight_active` declared `ultraheavy` answers `{"custom": "1000"}`: <<QUOTE S_FORMS_2: census receipt lines for the four worked keys>>.

**UNK** The numeric font-weight branch is unexercised on this host (only names are declared). Read in code, an
in-range numeric weight absent from the table is parsed into `w_i` and discarded, so `m_value` keeps whatever
it held before the call (400 only while untouched since the default at `:148`), and an out-of-range number
forces 400 — no host declaration shows either outcome, so neither is a host fact here.

## §3 Gradient angle inheritance — the host's two rows

**OBS** S_FORMS_2 (measured, 2026-10-25): `general:col.active_border` answers `{"option":
"general:col.active_border", "custom": "ffe68e0d 45deg", "set": true }` — one colour plus a 45° angle the
declaring line does not contain: <<QUOTE S_FORMS_2: the census receipt's general:col.active_border line (ffe68e0d 45deg)>>.

**OBS** S_FORMS_2 (measured, tree read): the defaults tree declares the variable as a two-colour 45°
gradient and then the key, and the theme redefines the variable to one colour and re-declares the key —
`default/hypr/looknfeel.conf:4` `$activeBorderColor = rgba(33ccffee) rgba(00ff99ee) 45deg`, `:15`
`col.active_border = $activeBorderColor`; `theme/hyprland.conf:1` `$activeBorderColor = rgb(e68e0d)`, `:4`
`col.active_border = $activeBorderColor` (root sources defaults at `hyprland.conf:10`, theme at `:13`):
<<QUOTE S_FORMS_2: tree-read receipt lines for the two activeBorderColor declarations>>.

**OBS** S162 (ConfigManager.cpp): a redeclaration clears the colour list and keeps the angle unless a
`deg` token appears — the line that produces the inherited 45°: <<QUOTE S162: DATA->m_angle = std::stoi(std::string(var.substr(0, var.find("deg")))) * (std::numbers::pi / 180.0); // radians>>.

**INF** The angle is state of the option's live data object (allocated once, `m_angle` default 0), not of
the declaring line, so a second declaration without `deg` inherits the first one's angle — which is why
the live value is `ffe68e0d 45deg`, not `ffe68e0d 0deg`.

**OBS** S_FORMS_2 (measured): the control pair that separates the mechanisms — the same variable read at
an earlier parse position still held the gradient: `group:col.border_locked_active` (declared only at
`looknfeel.conf:53`, before the theme redefines the variable) answers `"ee33ccff ee00ff99 45deg"`, two
colours; `group:col.border_active` (re-declared at `theme/hyprland.conf:8`) answers `"ffe68e0d 45deg"`,
one colour — same key family, same variable name, two live values: <<QUOTE S_FORMS_2: the census receipt's border_locked_active line>>.

**INF** `rgba(33ccffee)` → `ee33ccff` in both rows: the declared RGBA byte order is rotated to ARGB on the
way in, so a comparison against the declared text must convert, never string-compare.

**OBS** S_FORMS_2 (own work): the model is falsifiable on this host — with angle inheritance switched off the
same census reads `variant-noinherit labels agreement=62 agreement*=6 mismatch=2 config-only=0 live-default=0`,
flipping exactly `general:col.active_border` and `group:col.border_active`, the two rows §3 names:
<<QUOTE S_FORMS_2: variant-noinherit labels agreement=62 agreement*=6 mismatch=2 config-only=0 live-default=0>>.

## §4 The host census under this model

**OBS** S_FORMS_2 (own work, 2026-10-25; `.ufo/waves/round-40/fetch/` receipt): `forms int=44 float=5 str=8 custom=13` and `labels agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0` — both
sums 70, the 70 keys of the static table, each labelled against its native reply; the 8 `agreement*` rows
are the shadowed ones (`decoration:rounding`, `general:border_size`, `general:col.active_border`,
`general:gaps_in`, `general:gaps_out`, `group:col.border_active`, `input:kb_layout`, `input:kb_options`):
<<QUOTE S_FORMS_2: labels agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0>>.

**OBS** S_FORMS_2 (own work): both counts re-derive from the delivered static resolver plus the committed capture — `python3 -I tools/mado-options.py --home "$HOME"` (70 rows) and `.ufo/waves/round-40/w1/ScrFormsEntryA/rederive-census.py`, which prints the two lines above, `mismatch=0`, the 8 shadowed keys and the `45deg` inheritance without the reference tool: <<QUOTE S_FORMS_2: the re-derivation output block (forms/labels/rows lines)>>.

**INF** `mismatch=0` under this model means every declared key's live value is explained by its
declaration plus the conversion rules above; it is not a claim that the config is what the user intended,
nor that a runtime override never happened.

## §5 What this does NOT license

- Runtime `hyprctl keyword` overrides are outside: nothing here says how a keyword interacts with a reload, whether it survives one, or how to attribute a live value no declaration explains.
- Nothing is claimed about options the host never declares. A probe answers a default (`misc:font_family` → `Sans`, `set:false`) — the engine's default, not a declaration, no owner.
- The parser boundary excludes plugin-registered options, so a `plugin { }` key's reply is covered by neither §2 nor the census.
- No claim about the write path, sockets, batching or any failure exit status: those belong to the tool contract (C1), not to the compositor's answer.
- The census is one host, one date, one theme/toggle state; a toggle or theme switch moves the labels — re-run, do not reuse the counts.

## Limits

- The census covers the 70 keys the tree declares; the wider option universe (`hyprctl descriptions -j`) is separate round-40 ground, not cited here.
- `S_FORMS_1` and `S_FORMS_2` are placeholders: L1 assigns registry ids and renames them in this file, the registry rows and the lesson Gate lines together (clause b needs four `source: S###` lines); the new row's location cell must end with a token no other row uses — S180 already owns this URL's bare form (`sha256:95733223…`, byte-identical).
- The S162 anchor-cell range gap (§2) is an erratum for the held row, appended, never rewritten.
- Two source lines can never be Gate quotes: the counter's `norm()` deletes `<…>` spans, and `sc<int>` on
  ComplexDataTypes.hpp `:75` closes a span opened at `:62`, so `:72` and `:75` vanish from the normalized
  blob (measured, `norm(q) in norm(blob)` false) — §2 quotes the gap `toString` instead.
- Every slot names text this seat read in the fetch blobs or measured live; the sha256 binding and Gate receipt path are L1's to commit — until then these are working-tree bytes.
