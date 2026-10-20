# Mado R16 w2 — S054 `custom.cpp` vs the integrated `## Renderer boundary`

Seat: `MadoR16.AttackU7Code` (scout, leaf). Date 2026-10-20. Read-only
falsification of the integrated U7 note; no gate, test, probe, producer,
package or service operation. `corpus/lessons/round-15-verifier-spotcheck.md`
was read first. No tools installed or updated.

## Question and byte identity

Question: do the note's hide/markup branch assertions in
`corpus/knowledge/waybar-observation-boundaries-r16.md` §`## Renderer boundary`
(lines 32–52) survive comparison with the tagged S054 source the note binds?

Reopened in this session:

- <https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/custom.cpp>
  — 292 lines, **8746 bytes**, SHA-256
  `2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f`.
  This matches `.ufo/waves/round-16/evidence/source-bindings.json` S054 and
  the S054 digest cell in `corpus/SOURCES.md`, so the compared bytes are the
  admitted bytes.
- Control-flow context from the same tag (not new registry sources):
  `include/modules/custom.hpp`, `src/ALabel.cpp`, `include/ALabel.hpp`,
  `src/AModule.cpp`, `include/AModule.hpp`, `include/util/command.hpp`, and
  `man/waybar-custom.5.scd` **only** for the `escape` default sentence that
  sits inside the Renderer paragraph (S053 semantics otherwise belong to
  `AttackU7Source`).

The note heading at line 32 is exactly `## Renderer boundary`, matching the
`measure.py` U7 facet key; the text below is the body a reader actually
inherits.

## Assertion-by-assertion (note text vs tagged source)

| # | Note assertion (note lines) | S054 anchor | Observation | Verdict |
|---|---|---|---|---|
| A1 | "first hides the module when a configured `exec`/`exec-if` has empty output or nonzero exit status" (34–35) | 163–166 | `(exec.isString() \|\| exec-if.isString()) && (output_.out.empty() \|\| output_.exit_code != 0)` → `event_box_.hide()` | **exact**, both disjuncts and the config guard. `event_box_` is the module widget (`src/AModule.cpp:283`). |
| A2 | "Otherwise it parses JSON or raw output" (35–36) | 168–172 | exact-string `return-type == "json"` → `parseOutputJson()`; every other value (including absent and `i3blocks`) → `parseOutputRaw()` | **exact**; the note does not claim i3blocks has a separate parser, and the source folds it into raw. |
| A3 | "formats text/alt/icon/percentage" (36) | 175–177 | `fmt::format(runtime(format_), text, alt, getIcon(percentage_, alt_), percentage)` | **exact** as argument list; `getIcon` is the base-class selector (`src/ALabel.cpp:132–152`). |
| A4 | "can still hide on empty formatted text or `hide-empty-text`" (36–37) | 178–180 | `(hide-empty-text.asBool() && text_.empty()) \|\| str.empty()` → hide | **mechanism exact, wording overbroad (F1)**. `str.empty()` hides unconditionally; `hide-empty-text` hides only together with `text_.empty()`; the flag alone is never sufficient. |
| A5 | "The visible branch calls `label_.set_markup(str);`" (37–38) | 181 | first statement of the else-branch, literal call text | **exact**. |
| A6 | "then sets tooltip markup and CSS classes before showing the event box" (38–39) | 182–207 | tooltip setters at 188/190/192 are **inside `if (tooltipEnabled())`**; class removal/addition 195–206; `event_box_.show()` 207 | **ordering exact; "sets tooltip markup" unconditional is overbroad (F2)**. |
| A7 | "These are static control-flow observations, not a record of this host executing the branch" (39–40) | 219 + `src/ALabel.cpp:130` + `src/AModule.cpp:93–98` | `ALabel::update()` only forwards to `AModule::update()`, which forks `on-update` and never writes visibility; nothing after line 207 re-shows the event box in this call | **supported**; the hide/show decision is not undone by the parent call. |
| A8 | "`escape` defaults false per S053" (49) | man lines 125–128 | "default: false" under `*escape*` | **exact**. |
| A9 | "Source parsing conditionally escapes text" (49) | 233–239, 243–247, 263–277 | text escaped only when `escape` is a true bool; JSON escapes text/alt/tooltip | **exact for `text_`**; see F3 for the unclaimed tooltip asymmetry. |

## Findings

**F1 — `hide-empty-text` compressed into a standalone hide condition
(precision; high confidence).** The note's "or `hide-empty-text`" reads as
"setting the flag causes hiding." Source requires both the flag and
`text_.empty()` (custom.cpp:178). Bounded static counterexample:
`{"hide-empty-text": true, "format": "{text}", "exec": "printf hi"}` with
stdout `hi`, exit 0 → `text_ = "hi"`, `str = "hi"`, flag true → the visible
branch runs (181). Conversely `str.empty()` hides even when the flag is false
or absent (format `""`, or a format whose substitutions are all empty), so
the two clauses are not interchangeable. A second byte-level misreading is
possible because `text_` is the parsed field, not `output_.out`: JSON
`{"tooltip":"t"}` with `hide-empty-text: true` and static format text hides
although stdout was nonempty. The draft
(`.ufo/waves/round-16/waybar-draft.txt:28`) stated "hide-empty-text is set
and the text is empty"; integration shortened away the qualifier.

**F2 — tooltip setter is conditional on `tooltipEnabled()` (precision; high
confidence).** All three `set_tooltip_markup` calls (188, 190, 192) sit under
`if (tooltipEnabled())` at 182, whose value is `config["tooltip"]` with
default `true` (`src/AModule.cpp:17,280`; man lines 115–118). Bounded static
counterexample: `tooltip: false` → zero tooltip setters, while
`set_markup(str)`, the class block and `event_box_.show()` still run. The
sentence's ordering claim survives; only the unqualified verb is too broad.
The draft (line 29) described the tooltip branches separately; integration
flattened them.

**F3 — unclaimed source nuances, not contradictions (observation; high
confidence).**
(a) `exec-if` output is structurally empty: `execNoRead` returns
`{WEXITSTATUS(stat), ""}` (`include/util/command.hpp:133–139`) and both
polling workers assign that to `output_` (custom.cpp:50, 122). So A1's
"empty output" for an `exec-if` is the buffer, not an observation of the
command's stdout; a module with `exec-if` but no `exec`/`interval`/`signal`
takes the hide branch on success because `out` is `""`. The note's wording is
literally true but could be read as "exec-if printed nothing."
(b) In raw mode the first line's escaped tooltip is written at 235 and then
unconditionally overwritten with the unescaped line at 240; JSON mode escapes
text, alt and tooltip consistently (263–277). The note never claims tooltip
escaping, and this asymmetry actually reinforces "GTK receives markup, not a
promise of literal glyphs." The draft recorded it (line 30); integration
dropped it, which loses detail but creates no false claim.

**Suggested minimal tightening for L1 (note is L1-owned; this seat did not
edit it).** Replace A4–A6 with:
"…can still hide on an empty formatted string, or when `hide-empty-text` is
true and the parsed text is empty. The visible branch calls
`label_.set_markup(str);`, then — when tooltips are enabled — sets tooltip
markup, then CSS classes, before showing the event box."
This keeps the exact branch order and adds only the two source qualifiers.

## Verdict

No falsifying counterexample was found for the load-bearing hide/markup
mechanism: A1, A2, A3, A5, A7, A8 and A9 match the tagged bytes exactly, and
the parent-call check confirms the note's static-control-flow framing. F1 and
F2 are literal overbreadths introduced by compression — each is instantiable
by a concrete configuration, so a hostile reader can call the sentences false
even though the intended mechanism is right. F3 supplies context the note
does not claim either way. Record confidence: high for all source readings;
the recommendation is wording, not mechanism.

## Limits and remaining unknowns

- Tagged 0.15.0 bytes only; no installed-binary/source equivalence, no host
  configuration, no GTK/Pango outcome, no rendered pixels. Actual Pango
  handling of unescaped producer text remains `[UNK]`, as the note states.
- No producer, Waybar, gate, measure, selftest or test was executed; no
  package/service/input/compositor/screenshot operation ran. Counterexamples
  above are static deductions from the quoted branches, not observations.
- S053 semantics beyond the `escape` default and the Producer-contract
  section are out of this seat's scope (`AttackU7Source` owns them); no
  registry, lesson or note edit was made.
- `measure.py` U7 facets were read, not run; structural facet admission and
  final verification remain L1's.

Report: .ufo/waves/round-16/w2/reports/AttackU7Code.md
