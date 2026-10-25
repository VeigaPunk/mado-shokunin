# Reading an option as the parser stored it: declaration → handler → value → toString → reply → label

source: S162 - Hyprland `src/config/legacy/ConfigManager.cpp` @ efb5099 (re-opened): gradient setter, its angle branch, and the custom-type registration that makes it the handler
source: S173 - hyprlang v0.6.8 `src/config.cpp` (re-opened): `configSetValueSafe`'s type switch, `configStringToInt`
source: S180 - Hyprland `src/config/shared/complex/ComplexDataTypes.hpp` @ efb5099 (held, re-opened): the three `toString()`, `WEIGHTS`, `parseWeight`
source: S_FORMS_1 - Hyprland `src/config/shared/complex/ComplexDataType.hpp` @ efb5099 (new): `IComplexConfigValue` — `toString()` is the print contract, three complex data types
source: S_FORMS_2 - own-work (new): live `hyprctl getoption -j` census over the host's 70 declared keys, 2026-10-25
verified-at: 2026-10-25
recheck: on-change

Lane mado-shokunin, round 40 (C2). Hyprlang era only: host Hyprland v0.56.2 (`efb5099`), hyprlang 0.6.8, `.conf` tree.
`knowledge/config-option-table-r39.md` owns *which file declares a key*; this entry owns the read path *from that line to
the string `getoption` answers*, in the order the parser walks it. Held, not restated: last declarer wins and linear
`source` order (r39 §1, S218/S220); option-before-handler parse order and the parser boundary (r39 §2); the label
vocabulary (`knowledge/hyprctl-verification-layer.md` §4).

**Citation note.** The `ComplexDataTypes.hpp` bytes are cited through held S180, not through a new row: S180 already
anchors that exact URL and file sha (`95733223…`), so a second row on it would duplicate the location (QUALITY.md
criterion 17; `PRED-C2-r40-v1` clause e). The registration's "new ComplexDataTypes row" is therefore executed as a
re-open of S180, and the second new row is that file's base interface header — a distinct location.

## §1 Declaration — the text the parser is handed

**OBS** S173: the line reaches `CConfig::parse`, which tries the registered option first — `auto [f, rv]    = configSetValueSafe(LHS, RHS);` (`src/config.cpp:832`); handlers run only if that fails (`:839`). So `col.active_border = …` is an *option* assignment, not a directive.

**OBS** S173: `configSetValueSafe` builds the lookup name from the enclosing category plus the LHS (`valueName += c + ':';`, `:279-287`) and dispatches on the registered type (`switch (VALUEIT->second.m_eType) {`, `:455`). The RHS arrives as text at this point. **INF** hyprlang substitutes `$`-variables before this call: the theme's `col.active_border = $activeBorderColor` (`~/.config/omarchy/current/theme/hyprland.conf:1,4`) reads back as `ffe68e0d 45deg` although `$activeBorderColor` there is `rgb(e68e0d)` and the defaults declarer it overwrote (`default/hypr/looknfeel.conf:4,15`) used `rgba(33ccffee) rgba(00ff99ee) 45deg` — so the setter saw the expanded colour, not the variable name (S_FORMS_2).

## §2 Handler — the registered type picks the setter, the key does not

**OBS** S173: five arms, five stored shapes — INT → `configStringToInt(value)` (`:458`), FLOAT → `std::stof(value)` (`:467`), VEC2 → two `std::stof` (`:485`), STR → `setFrom(value)` verbatim (`:493`), CUSTOM → the registered callback `->handler(value.c_str(), &…->data)` (`:497-499`). The switch then sets `m_bSetByUser = true` (`:512`).

**OBS** S162: gradient, gap and font weight are CUSTOM arms registered per config var, never directives — `Hyprlang::CConfigCustomValueType{&configHandleGradientSet, configHandleGradientDestroy, …}` (`ConfigManager.cpp:509-511`; gap `:504`, weight `:506-507`), setters at `:103`, `:168`, `:193`.

**OBS** S173: `configStringToInt` is the whole int conversion — `<<QUOTE S173: return (a * (Hyprlang::INT)0x1000000) + (r.value() * (Hyprlang::INT)0x10000) + (g.value() * (Hyprlang::INT)0x100) + b.value();>>` (`:219`): comma `rgba(r,g,b,a)` → ARGB with `a*255`; 8 hex digits → RGBA→ARGB (`:220-227`); `rgb(` 6 hex or 3 comma values → `0xFF000000 + …` (`:232-255`); `true|on|yes` → 1, `false|off|no` → 0 (`:259-263`); `0x…` → hex (`:195`). The declared spelling is gone in the stored value.

**OBS** S162: the gradient setter splits on spaces, clears the colour list on *every* redeclaration (`DATA->m_colors.clear();` `:112`), and assigns the angle only inside the `deg` branch — `<<QUOTE S162: DATA->m_angle = std::stoi(std::string(var.substr(0, var.find("deg")))) * (std::numbers::pi / 180.0); // radians>>` (`:117-120`) — then `break`s. No branch in `:103-161` resets `m_angle`; an empty colour list falls back to one transparent colour (`:149-151`).

**INF** So a gradient redeclared *without* a `deg` token keeps the previous declarer's angle: colours are replaced, the angle survives. That is the mechanism behind §5's worked example — a property of this setter's control flow, not of any one config file.

**OBS** S162/S180: gaps expand by token count — `<<QUOTE S180: *this = CCssGapData(toInt(varlist[0]), toInt(varlist[1]), toInt(varlist[2]));>>` (`ComplexDataTypes.hpp:94-120`): 1 → all four, 2 → (vertical,horizontal), 3 → (top,horizontal,bottom), 4 → as written. Font weight resolves through `WEIGHTS` (`:158`, lookup `:167`, `thin`=100 … `ultraheavy`=1000); a numeric weight is parsed but only *out-of-range* values are rewritten to 400 (`if (w_i < 100 || w_i > 1000)` `:172`), so an in-range numeral leaves the stored default 400.

## §3 toString — the exact printed text

**OBS** S_FORMS_1: printing is a contract, not a convenience — every complex value must implement `<<QUOTE S_FORMS_1: virtual std::string           toString() const = 0;>>` (`ComplexDataType.hpp:20`), and the enum names exactly the three shapes this entry covers (`:7-12`). What the reply prints is therefore the stored object's own string, not the declared text.

**OBS** S180: gradient — each colour as `result += std::format("{:x} ", c.getAsHex());` (`:72`), then the angle as `std::format("{}deg", sc<int>(m_angle * 180.0 / M_PI))` (`:75`, block `:69-76`). Hence, as §4's replies show: lowercase hex, no `0x`, no zero padding, one space between colours and before `deg`, angle truncated to whole degrees.

**OBS** S180: gaps print `<<QUOTE S180: return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);>>` (`:134`); font weight prints `std::format("{}", m_value)` (`:155`) — the weight *name* the operator wrote is gone, only the number is printed (`group:groupbar:font_weight_active` `ultraheavy` → `1000`, `…_inactive` `normal` → `400`, S_FORMS_2).

**UNK** `int`, `float` and `str` have no `toString()` here: their reply formatting is hyprctl's own (`HyprCtl.cpp`, not fetched this round). Observed: floats print with six decimals.

## §4 The reply — one object, one form field, or the text `no such option`

**OBS** S_FORMS_2 (own-work): all 70 keys of the host tree answer one JSON object holding `option`, `set` and exactly one of `int|float|str|custom`; none answered `no such option`. Forms: `forms int=44 float=5 str=8 custom=13`.

**OBS** S_FORMS_2: one verbatim reply per form — `{"option": "general:col.active_border", "custom": "ffe68e0d 45deg", "set": true }`, `{"option": "decoration:rounding", "int": 0, "set": true }`, `{"option": "decoration:blur:brightness", "float": 0.600000, "set": true }`, `{"option": "input:kb_layout", "str": "br", "set": true }`.

**OBS** S_FORMS_2: an undeclared name prints the bare text `no such option` and still exits 0 (`hyprctl getoption -j no:such:key`, 2026-10-25); an empty declared string prints the sentinel `[[EMPTY]]` (`input:accel_profile`). `set` is not "has a value": `misc:font_family` answers `"str": "Sans", "set": false`. **INF** `set` reports whether config assigned the value (`m_bSetByUser`, S173 `:512`), so `set=false` with a value is the engine default — the held `live-default` class.

## §5 Label — compare the declaration with the reply, not with the reply's text

Reconstruct from the declared text the string the parser *would* print — `int` via `configStringToInt`, `float` numerically, `str` by text, `custom` by §2's expansions and §3's formats (gradient angle inherited when the line carries no `deg` token) — then apply the held vocabulary: equal + `set` + one declarer = `agreement`; equal but shadowed = `agreement*`; unequal or `set=false` despite a declarer = `mismatch`; declared and unanswered = `config-only`; answered with no declarer = `live-default`.

**OBS** S_FORMS_2 (own-work): the worked example, two rows, both `agreement*` — `general:col.active_border` declared `rgb(e68e0d)` (`theme/hyprland.conf:4`) reads `ffe68e0d 45deg`; `group:col.border_active` declared the same value (`theme/hyprland.conf:8`) reads `ffe68e0d 45deg`. The `45deg` appears in neither line: it is the defaults declarer's angle (`looknfeel.conf:4`) surviving `m_colors.clear()`. Contrast `group:col.border_inactive`, one colour with no earlier angle, reads `aa595959 0deg`.

**OBS** S_FORMS_2: the census over those 70 keys is `labels agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0`; the 8 `agreement*` are `decoration:rounding`, `general:border_size`, `general:gaps_in`, `general:gaps_out` (toggle owns), `general:col.active_border`, `group:col.border_active` (theme owns), `input:kb_layout`, `input:kb_options` (user owns).

**INF** `mismatch=0` is the model's own consistency, not independent proof: a comparison that treated the reply text as the declaration would mark the 13 `custom` rows and every `true`/`1` spelling as mismatches. The inheritance rule is what makes the two worked-example rows agree; drop it and they become mismatches.

## §6 What this does NOT license

- Runtime state: a `keyword` override or a failed reload changes the reply after the parse; the census is one point-in-time read, not the config text.
- Options the host never declares: the 70 keys are the host tree's set; a probed key with no declarer can be at best `live-default`, and the compositor's other registered options are outside this entry.
- Plugin options: excluded with the `plugin` special category (r39 §2) — not fetched, not claimed.
- `no such option` means "not a registered option name", not "no such line in a file": a line a handler claimed, or one that failed to parse, never becomes an option either.
- Gradient shapes beyond the observed one: more than 10 colours, or a `deg` token that is not last, are not exercised by the 9 gradient rows; the numeric-font-weight quirk (§2) is not exercised either — both host weight rows are names.

## Limits

- One host, one compositor build (v0.56.2/`efb5099`), hyprlang 0.6.8, one boot; dated 2026-10-25. A theme or toggle switch changes declarers *and* the inherited angle — re-run, never reuse the counts.
- The envelope and the `set` mapping rest on the 70 replies; hyprctl's formatting code was not fetched, so both are host-observed + source-inferred, never source-only.
- Falsifiable consequence: redeclare the theme's `col.active_border` with two colours and no `deg` token — the reply must keep `45deg`; add a `deg` token — the angle must change. The first half is the observed host row; the second half is unrun.

## Provenance split

- **Host census, own-work (S_FORMS_2, this round):** the four-form envelope, the form counts, `no such option` with exit 0, `[[EMPTY]]`, six-decimal floats, `set=false` with a value, the label counts, the eight `agreement*` names, and every live string quoted in §4-§5.
- **Upstream bytes at pinned revisions (S162, S173, S180, S_FORMS_1):** the type switch and `configStringToInt`'s conversions, the gradient setter's clear-and-keep-angle control flow, the gap expansion, `WEIGHTS` and the numeric-weight quirk, the `toString()` contract and the three formats.
- **Held lane knowledge, cited not restated:** last-declarer-wins and option-before-handler order (r39 §1-§2), the label vocabulary (`hyprctl-verification-layer.md` §4).
- **Not established in this entry:** hyprctl's own formatting path for `int`/`float`/`str`.
