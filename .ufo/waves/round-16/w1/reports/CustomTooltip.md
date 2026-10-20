# CustomTooltip — Waybar 0.15.0: tooltip, class and percentage are not label text; escaping limits

Seat: `MadoR16.CustomTooltip` (leaf scout, read-only, no dispatch). Scope: exact tagged-source
facts for the U7 "Renderer boundary" and "Safe observation" sections: how `custom/` turns producer
bytes into a GTK label, why tooltip / CSS class / percentage are separate surfaces, and where the
`escape` option stops protecting markup.

Method: HTTP source reading only (raw.githubusercontent.com at tag `0.15.0`, plus GTK 3.24
sources for the API semantics Waybar calls). S053 and S054 were each fetched twice, independently,
with identical digests; the context and GTK files were fetched once and their digests are recorded
below to pin the read bytes. No producer was executed, no Waybar/GTK process or host probe was run, no
package/service operation, no install. Man-page commands are source data, not permission.

## 0. Source identity (bind every claim to these bytes)

| Ref | Artifact | Bytes | SHA-256 |
|---|---|---|---|
| S053 | `man/waybar-custom.5.scd` @ 0.15.0 | 6656 (250 lines) | `efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82` |
| S054 | `src/modules/custom.cpp` @ 0.15.0 | 8746 (292 lines) | `2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f` |
| context | `include/modules/custom.hpp` | 1094 | `c31fa6ae1be35033f4e90d1eda7d0587dc33e94515c5b6b1a3d65478b073b0f8` |
| context | `src/ALabel.cpp` (GTK label owner) | 7944 | `7000f686548fa8572aecef8073ee0e05fd30f851f9b6778e706791280d286a48` |
| context | `include/ALabel.hpp` | 1124 | `b4a9d76bc9cfc8bfd1917f2ffea54d1a1678af0dc0fcbdf9723f74c295f085db` |
| context | `src/AModule.cpp` (`tooltip` config default) | — | `57d3a1cd5fe03d11bec68f0b7d9e3e5e3fc03fa7f3a492964e4f60b588fe2650` |
| GTK 3.24 | `gtk/gtklabel.c` | 217322 | `74b0e89e8b4de6068551341d76637c543e17bdad71a193c0b5a0c1becc9e0467` |
| GTK 3.24 | `gtk/gtktooltipwindow.c` | 5862 | `f1df95d184eec2da8dcb496804d125d2599c821640f351d29e7076d9d63fe220` |
| GTK 3.24 | `gtk/gtkwidget.c` | 551996 | `5b490027b2271205e77b1a969e6b1690bfebde758c049d46a5b3982acc1be451` |

Tag resolution (two channels agree): `refs/tags/0.15.0` → commit
`90b209add8937514d0a987aa842e701bd8f1232e` (GitHub refs API; `git ls-remote --tags`).
URLs: `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/man/waybar-custom.5.scd`,
`https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/custom.cpp`; GTK files from
`https://gitlab.gnome.org/GNOME/gtk/-/raw/gtk-3-24/gtk/…` (GTK `gtk-3-24` branch read
2026-10-20; the digests pin the bytes, not a tag). Waybar sources read 2026-10-20.

**Era limit.** Tag source is not the installed binary. `corpus/knowledge/waybar-walker-plane.md`
§1 records `waybar --version` → `Waybar v0.15.0` on 2026-10-14; the package build/revision and
binary bytes were not verified and this round forbids querying them. Every statement below is
`[OBS]` in the tag, not host behaviour.

## 1. The whole update pipeline (S054 `custom.cpp`)

| Step | Anchor | Fact |
|---|---|---|
| hide gate | 163-166 | With `exec`/`exec-if` configured, `output_.out.empty() \|\| output_.exit_code != 0` calls `event_box_.hide()` and **returns without touching the label**. |
| parse | 168-172 | `return-type == "json"` → `parseOutputJson()`, else `parseOutputRaw()`. |
| render | 174-177 | `str = fmt::format(fmt::runtime(format_), fmt::arg("text", text_), fmt::arg("alt", alt_), fmt::arg("icon", getIcon(percentage_, alt_)), fmt::arg("percentage", percentage_))` — exactly four named arguments. |
| label | 181 | `label_.set_markup(str)` — the **only** label-text setter in the module (grep: `set_text`/`set_label` absent from `custom.cpp`). |
| tooltip | 182-194 | `if (tooltipEnabled())` then one of three `label_.set_tooltip_markup(...)` branches. |
| classes | 195-206 | remove every style class except `id_`; add `class_`, then `flat`, `text-button`, `MODULE_CLASS`; `event_box_.show()`. |
| parent | 219 | `ALabel::update()`; `ALabel::update()` is `AModule::update()` (`ALabel.cpp:130`) and that body only forks the `on-update` command (`AModule.cpp:93-98`) — it does not set text. |

The label's text is therefore exactly the last `str` passed at line 181 (or its initial empty
value). Nothing else in the module writes label text.

## 2. Tooltip is not label text

- **T1 [OBS]** Different call and different widget property: `label_.set_markup` (181) vs
  `label_.set_tooltip_markup` (188, 190, 192), the latter on the `Gtk::Label label_` member
  (`ALabel.hpp:22`).
- **T2 [OBS]** Tooltip source is chosen by a three-way precedence (`custom.cpp:182-194`):
  1. `tooltip-format` configured (`tooltip_format_enabled_`, set once in the constructor at 13) →
     the *format expansion* of `tooltip-format` with `{text}/{alt}/{icon}/{percentage}` (184-188);
  2. else `text_ == tooltip_` → the **formatted label string** `str` is reused as the tooltip
     (189-190), so static format text and icons leak into the tooltip;
  3. else the parsed `tooltip_` field (192).
  The manual agrees for case 1: "The tooltip format. If specified, overrides any tooltip output
  from the script in *exec*." (S053:120-123, 14 words), "Uses the same format replacements as
  *format*." (123).
- **T3 [OBS]** `tooltip` is a separate boolean, default **true**: man S053:115-118
  ("default: true", "Option to disable tooltip on hover."); source default
  `isTooltip{config_["tooltip"].isBool() ? config_["tooltip"].asBool() : true}` (`AModule.cpp:17`),
  consumed by `tooltipEnabled()` (`AModule.cpp:280`). `tooltip: false` means the three
  `set_tooltip_markup` calls never run.
- **T4 [OBS + API]** GTK semantics make the tooltip a **different label in a different window**:
  `gtk_widget_set_tooltip_markup` merely sets the `tooltip-markup` property
  (`gtkwidget.c:15507-15513`); at display time `gtk_tooltip_set_markup`
  (`gtktooltip.c:246-252`) → `gtk_tooltip_window_set_label_markup`
  (`gtktooltipwindow.c:94-101`) → `gtk_label_set_markup` on the tooltip window's own label.
  GTK docs: "Sets `markup` as the contents of the tooltip, which is marked up with the Pango text
  markup language." (`https://docs.gtk.org/gtk3/method.Widget.set_tooltip_markup.html`).
  Consequence: no read of the module label's string can recover the tooltip, and tooltip markup
  validity is only exercised at hover time.
- **T5 [OBS]** There is no `{tooltip}` (and no `{class}`) format replacement. `fmt` receives only
  `text`, `alt`, `icon`, `percentage` (175-177 for `format`; 186-187 for `tooltip-format`); the man
  documents only `{text}`, `{percentage}`, `{icon}` (S053:168-174). An unknown `{name}` raises
  `fmt::format_error`, which the local catch at 209-216 only filters for the manual/automatic
  indexing message and otherwise rethrows — the failed expansion cannot become label text.
- **T6 [INF]** An empty `tooltip_` is still a non-NULL `std::string` passed to
  `set_tooltip_markup` (188/192 in the branches that run), so GTK sets `has-tooltip` TRUE
  (`gtkwidget.c:15512`; docs above) even for `""`. Whether an empty hover bubble appears was not
  observed.

## 3. `class` is CSS-selector state, never text

- **C1 [OBS]** Producer sources: i3blocks mode takes exactly one class from the **third line**
  (`i == 2`, `custom.cpp:248-249`); a fourth line breaks the loop (250-251). JSON mode accepts
  `class` as a string or an array of strings (278-284). The man: "The *class* parameter also
  accepts an array of strings." (S053:157), payload shape `$text\\n$tooltip\\n$class*` (163).
- **C2 [OBS]** `class_` reaches only the GTK style context (201-203) and is never an argument to
  `fmt::format` (175-177). `{class}` is not a replacement (T5). The man defines it as
  "a CSS class, to apply different styles in *style.css*" (166) and the style selectors
  `#custom-<name>` / `#custom-<name>.<class>` (248-249).
- **C3 [OBS]** Class state is rebuilt on every update: every class except the module `id_` is
  removed (195-200), then the current list is added (201-203). A class is transient style input,
  not a durable attribute of the text.
- **C4 [OBS]** `escape` does not apply to the class value (raw push at 249; JSON push at 279/282
  are direct `asString()` calls). Class is not markup, so "escaping" it is meaningless; it is
  also not text and cannot be observed from the label string.

## 4. `percentage` is numeric renderer state, not text

- **P1 [OBS]** `int percentage_` (`custom.hpp:40`) initialised to 0 (`custom.cpp:14`). It is
  written only in the JSON parser: `percentage_ = lround(asFloat())` when the field is
  non-empty *and* `isNumeric()` (285-287), else reset to 0 (288). `parseOutputRaw` (222-255)
  never touches it, so an i3blocks-style module has percentage 0 forever.
- **P2 [OBS]** Its only renderer entries are the `{percentage}` argument (176-177; also 186-187
  for `tooltip-format`) and the `{icon}` selection:
  `fmt::arg("icon", getIcon(percentage_, alt_))` (176) → `ALabel::getIcon`
  (`ALabel.cpp:132-152`) clamps `percentage / (100 / size)` into the `format-icons` array
  (141-146). The man: "Based on the set percentage, the corresponding icon gets selected. The
  order is *low* to *high*." (S053:63-65); "`{percentage}` Percentage which can be set via a json
  return type." (172); "`{icon}`: An icon from 'format-icons' according to percentage." (174).
- **P3 [OBS]** It is not injected into the label string on its own: the documented default format
  is `{text}` (S053:60) and the source default literal is `"{}"` passed at `custom.cpp:9`
  (resolved in `ALabel.cpp:19`). Under either, `percentage_` appears only if the configured
  `format` names `{percentage}` (or an icon derived from it). So a module can display text while
  carrying a percentage that is invisible in the label.
- **P4 [OBS]** JSON type matters: a quoted `"percentage": "50"` fails `isNumeric()` and is
  normalised to 0 (285-288); only a JSON number is used. Only the first output line is parsed —
  the loop `break`s at 290, so pretty-printed multi-object/multi-line JSON is not supported.
- **P5 [INF]** Negative percentages are not clamped before the `getIcon(uint16_t, …)` call
  (`ALabel.hpp:18`, `custom.cpp:176`): `-5` becomes 65531 and the array index clamps to the top
  icon. Out-of-range/negative producer values are therefore icon-selection edge cases, not an
  error path.

## 5. Escaping limits (the part most likely to be overclaimed)

- **E1 [OBS]** `escape` is opt-in, default **false**: man S053:125-128 ("default: false",
  "Option to enable escaping of script output."). Every use is guarded by
  `config_["escape"].isBool() && config_["escape"].asBool()` (233, 243, 263, 268, 273). A string
  `"true"` does not enable it.
- **E2 [OBS]** It applies only to **producer-derived payload fields**: raw `text`+`tooltip`
  (233-247) and JSON `text`, `alt`, `tooltip` (263-277). It never applies to the `format` or
  `tooltip-format` templates, to `class`, to `{icon}` values, or to config literals. Static format
  content is therefore always Pango markup by design.
- **E3 [OBS + docs]** The escaping domain is markup, not HTML sanitisation and not shell quoting:
  `Glib::Markup::escape_text` calls `g_markup_escape_text`, documented as "Escapes text so that
  the markup parser will parse it verbatim. Less than, greater than, ampersand, etc. are replaced
  with the corresponding entities." (`https://docs.gtk.org/glib/func.markup_escape_text.html`).
  Both sinks are markup sinks: `Gtk.Label.set_markup` "Parses `str` which is marked up with the
  Pango text markup language, setting the label's text and attribute list based on the parse
  results." (`https://docs.gtk.org/gtk3/method.Label.set_markup.html`); the same doc recommends
  `g_markup_escape_text()` for external data.
- **E4 [OBS — escape bypass in 0.15.0]** In `parseOutputRaw`, line **240** `tooltip_ = validated_line;`
  runs unconditionally *after* the escape branch (233-239), so the escaped assignment at 235 is
  dead. With `escape: true` and single-line raw output, `text_` is escaped but `tooltip_` is the
  **unescaped** line; `text_ == tooltip_` is then false whenever escaping changed bytes, so
  `update()` line 192 sets the raw line as markup. The first-line tooltip therefore bypasses
  `escape` in exactly the single-line case. With two or more lines, `i == 1` overwrites
  `tooltip_` with the escaped second line (243-247) and the hole closes.
- **E5 [OBS — GTK source]** Invalid markup is not neutralised and not replaced. `gtk_label_set_markup`
  calls `gtk_label_set_markup_internal`; on parse failure it logs
  `Failed to set text '%s' from markup due to error parsing markup: %s` and **returns without
  changing the label** (`gtklabel.c:2656-2675`, failure at 2669-2675). With the default
  `escape: false`, a bare `&` or `<` in producer output can therefore make an update a visible
  no-op while the process continues: the new text is neither shown nor recoverable from the
  widget, and the previous text remains. For the tooltip the same parser runs at hover time on the
  tooltip window's label (`gtktooltipwindow.c:94-101`), so an invalid tooltip fails only on hover.
- **E6 [OBS/UNK]** JSON mode performs **no** UTF-8 repair: the raw path runs
  `Glib::ustring::validate()/make_valid()` (227-230) before escaping; `parseOutputJson` (257-290)
  does not. GLib's escapable input is "Some valid UTF-8 text" (docs above); what happens to
  invalid UTF-8 in JSON `text`/`alt`/`tooltip` with `escape: true` was not read into jsoncpp/GLib
  internals → **[UNK]**, treat as undefined rather than repaired.
- **E7 [OBS/UNK]** GLib documents that escaped control characters become `&#x1; … &#x1f;`
  references "not valid XML 1.0 … valid XML 1.1" and accepted by GMarkup (same doc). Pango is the
  parser here, not GMarkup; whether such producer bytes still break the Pango parse is **[UNK]**.
  Do not claim `escape: true` makes arbitrary bytes safe.
- **E8 [INF]** `alt` is escaped (268-271) and then used as the `format-icons` object key
  (176; `ALabel.cpp:135`). If `alt` contains markup-significant characters, enabling `escape`
  changes the lookup key, so the selected icon can change. `alt` itself is not documented for
  `custom` (S053 FORMAT REPLACEMENTS 168-174, RETURN-TYPE 148-166) though the source consumes it.
- **E9 [OBS]** Order is parse/escape first (233-277), format second (175-177). `fmt` arguments are
  opaque, so `{`/`}` in producer text are not re-interpreted; conversely the `format` template is
  `fmt::runtime` syntax and config literals must double braces. Format-string errors are not
  escaping concerns.

## 6. Renderer boundary chain (what a "label text" claim actually covers)

- **R1 [OBS]** The module's contract ends at a markup string: `label_.set_markup(str)`
  (`custom.cpp:181`); GTK then parses Pango markup, applies attributes, decodes entities, and lays
  out glyphs in the theme font. The bytes set are not the visible glyph sequence.
- **R2 [OBS]** `max-length` mutates visible text: `ALabel.cpp:38-41` sets
  `set_max_width_chars`, `Pango::EllipsizeMode::ELLIPSIZE_END`, `set_single_line_mode(true)`.
  The rendered text is a truncation of `str`, not `str`. `min-length` only sets width (47-49);
  `rotate`/`align`/`justify` are geometry (`ALabel.cpp:51-67`, 118-125). `custom` passes the
  ALabel `ellipsize` argument default `false` (`custom.cpp:9`, `ALabel.hpp:14`), so no automatic
  ellipsis is added without `max-length`.
- **R3 [OBS — adjacent, ALabel-owned]** `format-alt` can change label text without any producer
  change: a configured `format-alt-click` toggles `alt_` and swaps `format_` (`ALabel.cpp:180-190`);
  `custom`'s click handlers then wake the producer (`custom.cpp:144-161`), and the next update
  formats with the new template. Label text is therefore also a function of click state.
- **R4 [OBS]** Visibility is not text: the hide path (164-166, 178-179) never clears `text_` or
  the label markup, so the widget retains its last string; and `hide-empty-text` tests
  `text_.empty()` (178) while the label would still carry static format content (man 24-26:
  "Disables the module when output is empty, but format might contain additional static content").

## 7. Doc/source deltas the note must not paper over

- **D1 [OBS + INF]** Man says `format` default `{text}` (S053:60); source default literal is `"{}"`
  (`custom.cpp:9` → `ALabel.cpp:19`). **[INF]** fmt automatic indexing binds that `{}` to the first
  argument (the `text` named arg), so both readings are text-only; this was not executed. Do not
  claim byte-identical defaults.
- **D2 [OBS]** Man declares `format-icons` as `array` (S053:64); source also accepts an object
  keyed by `alt` with a `default` fallback (`ALabel.cpp:134-140`). `alt` is undocumented
  (S053:168-174) but used by the live producers (existing note `waybar-walker-semantics.md` §3.3).
- **D3 [OBS]** Man documents `tooltip` as a bool default true (S053:115-118); source's non-bool
  value silently means true (`AModule.cpp:17`). `"tooltip": "false"` does not disable.

## 8. Hand-off: what the U7 note may and may not claim (feed to the four level-2 sections)

- **Producer contract** — producer fields are `text`, `tooltip`, `class`, `percentage` (+
  undocumented `alt`); raw mode is `text\ntooltip\nclass`, one class only; JSON mode parses the
  first line only; percentage must be numeric. Escape is opt-in and applies only to payload
  fields. No producer was run in this round.
- **Renderer boundary** — label text = Pango markup expansion of `format`; tooltip = separate
  string on a separate label/window (hover); class = GTK style classes; percentage = numeric
  input to `{percentage}`/`{icon}` only. Cite T1-T4, C1-C3, P1-P3, R1-R2.
- **Safe observation** — from source/config alone one may predict the *markup string* and its
  admissible replacements, the three tooltip precedences, the class set, and the percentage's
  narrow effect. One may not read rendered glyphs, tooltip content, CSS outcome, or class from
  label text. Cite E4-E8 for what escape does and does not neutralise; cite E5 for the
  invalid-markup no-op.
- **Unexercised rendering [UNK]** — no Pango layout/glyph rendering, no theme/CSS application, no
  hover/tooltip display, no host binary identity vs tag, no producer execution, no GTK control of
  empty-tooltip/underscore/control-character cases.

**Suggested short quotes for the note (each ≤25 words, all located):**
S053:118 "Option to disable tooltip on hover."; S053:122 "The tooltip format. If specified,
overrides any tooltip output from the script in *exec*."; S053:128 "Option to enable escaping of
script output."; S053:166 "*class* is a CSS class, to apply different styles in *style.css*";
S053:172 "*{percentage}* Percentage which can be set via a json return type."; GTK Label doc
"Parses `str` which is marked up with the Pango text markup language"; GTK tooltip doc "Sets
`markup` as the contents of the tooltip"; GLib doc "Escapes text so that the markup parser will
parse it verbatim."

## 9. Remaining unknowns

1. Installed package build/revision vs tag commit `90b209a` (host probe forbidden this round).
2. Pango's own parser behaviour for GLib's `&#x1;…&#x1f;` control references and other
   syntactically odd but GMarkup-accepted input (Pango source not read).
3. Invalid-UTF-8 JSON payload with `escape: true` (E6), and whether jsoncpp rejects it earlier.
4. Tooltip lifecycle/timing (when GTK parses and shows), and whether an empty tooltip string
   produces a visible empty bubble (T6).
5. `alt` escaping side effect on icon lookup (E8) is code-derived only, not observed.
6. GTK3 CSS support for generated content that could turn a class into visible text — not read;
   do not claim either way.

No file outside this report was written. No sibling file, gate, package, service, compositor,
input device or screenshot was touched; no omp/agent DB or credential path was read.
