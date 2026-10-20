# CustomMan — tagged Waybar custom-module man source (S053 scout)

Seat `MadoR16.CustomMan`, role scout. Round 16, wave `mado-r16-w1`.
Question: open the tagged Waybar custom-module man page for the `return-type`
and text-bearing fields, with exact quotes and anchors.

Source reading only. No compositor, bar, service, input, screenshot or producer
probe was run; no package, service or host operation was performed; nothing was
installed. Only HTTP reads of upstream source, local man-file reads, and local
hash/byte operations were used.

## 1. Source provenance (OBS)

| Fact | Value |
|---|---|
| Tag | `0.15.0` |
| Tag → commit | `90b209add8937514d0a987aa842e701bd8f1232e`, object type `commit`, committer date `2026-02-06T20:15:03Z` (GitHub ref/commit API) |
| Tagged URL opened | `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/man/waybar-custom.5.scd` |
| Commit-pinned URL | `https://raw.githubusercontent.com/Alexays/Waybar/90b209add8937514d0a987aa842e701bd8f1232e/man/waybar-custom.5.scd` |
| Bytes / lines | 6656 bytes, 250 lines |
| SHA-256 (both URLs) | `efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82` (`cmp` identical, GitHub API `size` 6656) |
| File title line | `waybar-custom(5)` (`man/waybar-custom.5.scd:1`) |

All `man/waybar-custom.5.scd:<line>` anchors below are against that tagged
source and its hash above. The installed package man was separately decompressed
and rendered for comparison (§5); it is not the anchor for S053.

Era warning (OBS, same day): upstream `master` at
`c15ec02ede4343592a59eb5c2ff4443c9c045f7c` (2026-10-19) has a materially larger
custom man (sha256 `d7b2f53d5e7d78400f728bb253b791ed838870e6fb6b3bd755e02eb8109b7297`,
identical at the commit-pinned raw URL and at `master` when fetched).
It adds `alt`, `{}`, multiline-tooltip, `format-icons` object/string and
`image-path`/`image-name`/`icon-size`. Those additions are **not** in tag
`0.15.0` and must not be cited as 0.15.0 documentation. The tag-commit URL is
the citable stable anchor.

## 2. `return-type` configuration field — exact anchors

Config entry (`man/waybar-custom.5.scd:33-35`), verbatim source lines:

```text
*return-type*: ++
	typeof: string ++
	See *return-type*
```

It declares only `typeof: string`; the value semantics live in the
`# RETURN-TYPE` section (`:148`). Do not fill the value set from this config
entry alone.

`# RETURN-TYPE` section, verbatim (`:148-166`):

````text
# RETURN-TYPE

When *return-type* is set to *json*, Waybar expects the *exec*-script  to output its data in JSON format.
This should look like this:

```
{"text": "$text", "tooltip": "$tooltip", "class": "$class", "percentage": $percentage }
```

The *class* parameter also accepts an array of strings.

If nothing or an invalid option is specified, Waybar expects i3blocks style output. Values are *newline* separated.
This should look like this:

```
$text\\n$tooltip\\n$class*
```

*class* is a CSS class, to apply different styles in *style.css*
````

Anchors: heading `:148`; json-mode sentence `:150`; JSON shape `:154`;
`class` array sentence `:157`; invalid/fallback sentence `:159`; fallback shape
`:163`; CSS-class sentence `:166`.

Exactness notes:

- `:150` literally contains a **double space** between `*exec*-script` and `to`
  (`...-script  to output...`). Preserve or normalize deliberately when quoting.
- `:163` in the scdoc source is `$text\\n$tooltip\\n$class*`; scdoc renders the
  doubled backslash as one, so the installed man shows
  `$text\n$tooltip\n$class*` (OBS via `groff -man -Tutf8` of the installed page,
  §5). The trailing `*` after `$class` is literal in both source and rendered
  page, and the document never explains it. Do not read it as a wildcard or a
  footnote marker.
- The man documents exactly one named accepted value, `json` (`:150`). Anything
  else is described only as "nothing or an invalid option" with i3blocks-style
  output (`:159`). The tag **never uses the literal value `text` for
  `return-type`**; a claim that `"return-type": "text"` is documented would not
  be sourced from this tag. (Whether 0.15.0 source code accepts `text` is
  `custom.cpp` scope, not this man.)
- The JSON example shows `percentage` unquoted and the others quoted, but the
  man declares no JSON value types; `class` additionally accepts an array of
  strings (`:157`).
- The JSON example is a single-line shape only at this tag; the "single line"
  requirement and the `jq --compact-output` advice exist only on `master`, not
  at `0.15.0`.

## 3. Text-bearing fields and replacements — exact anchors

Producer JSON fields, in the documented order (`:154`): `text`, `tooltip`,
`class`, `percentage`. Fallback line order (`:159`, `:163`): text, tooltip,
class, newline separated.

Format replacement definitions (`# FORMAT REPLACEMENTS`, `:168-174`),
verbatim:

```text
*{text}*: Output of the script.

*{percentage}* Percentage which can be set via a json return type.

*{icon}*: An icon from 'format-icons' according to percentage.
```

Anchors: heading `:168`; `{text}` `:170`; `{percentage}` `:172`; `{icon}`
`:174` (note `:172` has no colon after the bold term, unlike its neighbours).

Field anchors and quotes:

| Field | Anchor | Verbatim source line(s) | Documented limit that matters for observation |
|---|---|---|---|
| `format` | `:59-61` | `typeof: string ++` / `default: {text} ++` / `The format, how information should be displayed. On {text} data gets inserted.` | Says insertion, not paint or byte-identical rendering. |
| `format-icons` | `:63-65` | `typeof: array ++` / `Based on the set percentage, the corresponding icon gets selected. The order is *low* to *high*.` | Selection is defined by percentage only; at this tag no `alt`-keyed or string icon form is documented, and behavior when `percentage` is absent is not stated. |
| `max-length` | `:71-73` | `typeof: integer ++` / `The maximum length in character the module should display.` | "character" is undefined (codepoint/grapheme/byte, truncation marker, markup interaction all unstated). |
| `min-length` | `:75-77` | `typeof: integer ++` / `The minimum length in characters the module should accept.` | Same unit ambiguity. |
| `tooltip` | `:115-118` | `typeof: bool ++` / `default: true ++` / `Option to disable tooltip on hover.` | Tooltip is a hover surface, distinct from bar text. |
| `tooltip-format` | `:120-123` | `typeof: string ++` / `The tooltip format. If specified, overrides any tooltip output from the script in *exec*. ++` / `Uses the same format replacements as *format*.` | Script tooltip can be silently overridden by config; the man does not state precedence for any other field. |
| `escape` | `:125-128` | `typeof: bool ++` / `default: false ++` / `Option to enable escaping of script output.` | Default is **not escaped**. The man never names Pango/markup; the only markup-adjacent wording is an example comment, `:215` `"escape": true //handle markup entities`. |
| `hide-empty-text` | `:24-26` | `typeof: bool ++` / `Disables the module when output is empty, but format might contain additional static content.` | Empty script output can still yield visible static `format` content; empty output ≠ invisible module in general. |
| `class` | `:157`, `:166`, `:248-250` | `The *class* parameter also accepts an array of strings.` / `*class* is a CSS class, to apply different styles in *style.css*` / `- *#custom-<name>*` / `- *#custom-<name>.<class>*` / `- *<class>* can be set by the script...` | Class is a style selector channel, not display text. |

Static-text mode (`# DESCRIPTION`, `:8-9`), verbatim:

```text
The *custom* module displays either the output of a script or static text.
To display static text, specify only the *format* field.
```

Refresh cadence (execution, not paint): `interval` `:37-43`, including `:42`
"…If no *interval* or *signal* is defined, it is assumed that the out script
loops itself." and `:43` signal-only update; `signal` `:52-56`, including `:55`
"…*SIGRTMIN+N* = *SIGRTMAX*." and `:56` signal as the only update path without
interval. These govern when the producer runs, not whether or when the bar
paints the resulting text.

## 4. What this man does NOT establish (U7 observation boundary)

All items below are absences in the tag-0.15.0 source, verified by reading the
whole 250-line file and by literal search (`grep -c alt` = 0): `[OBS]` for the
absence in the document, `[INF]` for consequences.

- `[OBS]` No `alt` key anywhere: not in the JSON example (`:154`), not in
  format replacements (`:168-174`), not in `format-icons` (`:63-65`). At this
  tag, producers emitting `alt` (the lane's local omarchy producers do) rely on
  behavior outside this man. `alt`-keyed icons are **not documented at 0.15.0**;
  they become documented only on later `master`.
- `[OBS]` No `{}` placeholder; only `{text}`, `{percentage}`, `{icon}`
  (`:170-174`). The `{}` alias and its "cannot be combined" rule exist only on
  `master`.
- `[OBS]` No multiline-tooltip contract (`\r`/`\n`), no single-line JSON
  requirement, no `image-path`/`image-name`/`icon-size`, no object/string
  `format-icons` forms. All are post-tag additions.
- `[OBS]` No query/readback surface is documented here: no command, IPC verb or
  property that returns the currently displayed module text. The page documents
  configuration input and producer output only.
- `[OBS]` No rendering contract: no font, glyph fallback, width, ellipsis,
  markup language, markup validity, or visibility guarantee. `escape` is
  described only as "escaping of script output" (`:128`), with markup named only
  in an example comment (`:215`).
- `[INF]` Therefore "module text = script output" is a documented data-contract
  statement (`{text}`: "Output of the script", `:170`) at the format level, not
  an on-screen observation. Rendered text, truncation result, markup
  interpretation and glyph presence remain unmeasured and are not implied by
  this source.
- `[INF]` `max-length`'s undefined "character" and `format-icons`' percentage-only
  selection mean the man cannot adjudicate observable differences such as
  truncation boundaries or icon choice when percentage is omitted.

Not in scope here and not asserted: whether 0.15.0 `src/modules/custom.cpp`
accepts `alt`, `{}`, a literal `return-type` value `text`, or tolerates invalid
JSON. Those are the custom.cpp/exec seats' question. Also not asserted:
installed-binary behavior, live bar state, or any rendered pixel.

## 5. Installed-package man cross-check (OBS, bounded)

Local package `waybar 0.15.0-3`; `/usr/share/man/man5/waybar-custom.5.gz`,
generated by scdoc 1.11.5, man header date `2026-08-31`. Decompressed and
rendered read-only; no bar process was contacted.

Checked passages match the tagged source after scdoc rendering: description
static-text sentence, `return-type` config entry, the JSON shape, `class` array,
the i3blocks fallback sentence and its `$text\n$tooltip\n$class*` rendering,
`class`/`style.css`, `{text}`/`{percentage}`/`{icon}`, `format`, `format-icons`,
`max-length`/`min-length`, `tooltip`, `tooltip-format`, `escape`,
`hide-empty-text`, and the style selector list.

Limit: this is a passage-level comparison of rendered text, not a full
byte-for-byte scd↔roff equivalence proof (roff escapes and line wrapping are
lossy). It supports that the installed 0.15.0-3 man teaches the same tag-0.15.0
contract; it is not a package-integrity or build-reproducibility claim. The Arch
man header date (2026-08-31) differs from the tag commit date (2026-02-06) and
is a packaging/render date, not a different documented contract.

## 6. S053 row facts for L1 (proposal, not an edit)

`corpus/SOURCES.md` is L1-owned; this is source evidence only.

- id `S053`; kind `docs`; tag `0.15.0`; URL
  `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/man/waybar-custom.5.scd`
  (stable commit `90b209add8937514d0a987aa842e701bd8f1232e`).
- raw SHA-256
  `efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82`,
  6656 bytes, 250 lines.
- Anchors to cite: `:33-35` return-type config; `:148-166` return-type
  section (JSON shape `:154`, array class `:157`, fallback `:159`/`:163`,
  CSS `:166`); `:168-174` replacements; `:59-65` format/format-icons;
  `:115-128` tooltip/tooltip-format/escape; `:24-26` hide-empty-text;
  `:8-9` static text.
- Boundary sentence: the tagged man documents a producer→format data contract
  (`json` or i3blocks fallback; `text`/`tooltip`/`class`/`percentage`; `{text}`,
  `{percentage}`, `{icon}`) and does not document `alt`, `{}`, markup rendering,
  truncation semantics, a text readback/query surface, or on-screen output; it
  is an observation boundary, not rendered verification.

## 7. Confidence and remaining unknowns

- Provenance, hashes, line anchors, quoted sentences and lists: **high**
  confidence, directly read from fetched bytes; two URLs hash-identical.
- Tag-vs-master field differences: **high** for document text at the pinned
  revisions; not a code-behavior claim.
- Installed-man agreement: **high** for the checked passages; **bounded** as
  stated in §5.
- Remaining unknowns: 0.15.0 `custom.cpp` handling of `alt`/`{}`/`return-type`
  values/invalid JSON; GTK/Pango rendering and truncation of markup; whether the
  local bar's producers' `alt` reaches icon selection on this package; any
  actual painted-text observation. None of these is answerable from this man,
  and no live probe was made to close them.

No tool installs or updates. No package/service/host operation. Report only.
