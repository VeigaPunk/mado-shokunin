# AttackU7Source — round 16 U7 producer-contract falsification

Seat: `MadoR16.AttackU7Source` (leaf, read-only). Target:
`corpus/knowledge/waybar-observation-boundaries-r16.md` against tagged S053/S054.
Lane baseline named in the assignment: `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
No gate, `measure.py`, selftest, audit, build or lint was executed. No package,
service, compositor, input, signal, screenshot or producer probe ran. Network
access was limited to reading the tagged raw source bytes and one auxiliary
tagged file; nothing was installed or updated.

## Verdict

**No Producer-contract sentence is contradicted by the reopened tagged sources.**
The note's documentary route holds: S053 states the documented producer contract,
S054 shows parsing/formatting/visibility stages, and the rendering boundary is
stated without claiming pixels. Two low-severity corrections are recommended
(A1, A2) plus four informational precision notes (A3–A6). None blocks the U7
structural join in `measure.py`, which tests headings, `[UNK]` placement and
reciprocal S053/S054 rows, not sentence-level source parity.

Confidence: high on all source anchors and digests; medium only where marked
`[INFERENCE]`.

## Digest binding — reopened 2026-10-20

Fresh bytes were fetched from the exact tagged URLs and hashed in memory.

| id | fresh bytes | fresh SHA-256 | committed `source-bindings.json` | result |
|---|---|---|---|---|
| S053 | 6656 | `efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82` | same bytes and digest | exact |
| S054 | 8746 | `2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f` | same bytes and digest | exact |

The digests also match the `corpus/SOURCES.md` S053/S054 rows. Byte count and
digest equality establish that the assertions below were checked against the
same tagged artifacts the note cites, not a moving `master`.

## Assertion map

Line numbers in the note are from the working-tree file. Source line numbers are
from the tagged raw files. `custom.cpp` means S054; `waybar-custom.5.scd` means
S053.

| # | Note lines | Assertion | Reopened anchor | Verdict |
|---|---|---|---|---|
| P1 | 15–16 | S053 DESCRIPTION: “The *custom* module displays either the output of a script or static text.” | S053:8–9 | exact quote |
| P2 | 16 | For static text the manual names `format` only. | S053:9 “To display static text, specify only the *format* field.” | exact |
| P3 | 17 | For a configured producer, `exec-if` gates `exec` when its exit code is zero. | S053:21–22; S054:49–53, 121–125; **absent** from `continuousWorker` S054:66–115 | manual-exact; overbroad as implementation behavior — see A1 |
| P4 | 18–19 | JSON return-type supplies `text`, `tooltip`, `class`, `percentage`; `class` may be a string array. | S053:150–157; S054:262–287 | exact for the S053-documented keys; source also reads undocumented `alt` — A3 |
| P5 | 19–20 | Raw/i3blocks output has newline-separated text, tooltip and class. | S053:159–166; S054:226–254 | exact; raw accepts at most one class line (S054:248–251) |
| P6 | 21 | JSON parsing stops after its first input line. | S054:261–290, unconditional `break` at 290 | exact |
| P7 | 21–23 | Continuous workers publish one `getline` at a time; raw multi-line roles are not assembled across updates. | S054:21–27 dispatch, 80–114 one `getline` per wake and one `output_` line | exact |
| P8 | 23–24 | “Displays” does not promise every stdout byte is visible; a format may omit `{text}` entirely. | S053:59–61; S054:172–181 formats the configured string then calls `set_markup` | exact |
| P9 | 26 | `format` defaults to `{text}`. | S053:59–61; S054:9 passes literal `"{}"` to `ALabel`; `src/ALabel.cpp:19,31` | manual-exact; source literal differs — A6 |
| P10 | 26 | `{icon}` is selected from percentage. | S053:63–65, 174; S054:176 (format icon arg); `src/ALabel.cpp:132–151` | exact; `alt` selects the icon group, percentage indexes within it — A3 |
| P11 | 26–28 | The manual distinguishes polling `interval`, signal refresh, continuous scripts with optional `restart-interval`. | S053:37–50; S054:21–27, 92–97 | exact |
| P12 | 28–29 | None of these is authorization to trigger an update. | normative, no source claim | consistent with source-only scope |
| P13 | 29–30 | A command’s output is evidence about that invocation, not proof of consumption or retention. | boundary statement, no source claim | sound |
| R1 | 34–36 | `Custom::update` first hides when a configured `exec`/`exec-if` has empty output or nonzero exit. | S054:163–166 | exact, including the `exec || exec-if` guard |
| R2 | 36–37 | Otherwise it parses, formats, and can still hide on empty formatted text or `hide-empty-text`. | S054:167–181; S053:24–26 | exact conjunction; shorthand wording — A4 |
| R3 | 37–39 | Visible branch calls `label_.set_markup(str);`, then tooltip markup and CSS classes, then shows the event box. | S054:181, 182–193, 195–207 | exact order; tooltip path is conditional on `tooltipEnabled()` |
| R4 | 49–51 | `escape` defaults false; parsing conditionally escapes text; GTK receives markup, not literal glyphs. | S053:125–128; S054:233–247, 263–277 | exact for text; raw single-line tooltip quirk — A5 |
| T1–T4 | 42–47 | Config/source, producer result, instrumented GTK, rendered observation layers. | no source contradiction; layer distinctions match A1–R4 anchors | sound |

## Findings

### A1 (low, source scope) — `exec-if` is not applied by the continuous worker

Note line 17 states the gate without a mode qualifier. S053:21–22 does state it
without one (“*exec* will be executed if the exit code of *exec-if* equals 0”),
so the note is a faithful manual paraphrase. But the note also says “S054
narrows this contract” (line 21) and cites S054 as source; S054 narrows this
specific point too:

- Dispatch: `custom.cpp:21–27`. With no `signal`, no `interval`, no
  `restart-interval`, an `interval_` count of zero and an `exec` string, the
  constructor selects `continuousWorker()`.
- `custom.cpp:66–115` opens `config_["exec"]` directly at 67–69 and never reads
  `config_["exec-if"]`. The only worker-side `exec-if` executions/gates are
  `delayWorker` (49–53) and `waitingWorker` (121–125); `update` reads the key
  only to test whether it is configured for the hide guard at 163–166, not to
  gate `exec`.

Bounded counterexample, static control flow only: config
`{"exec": "producer", "exec-if": "gate"}` with no `interval`, `signal` or
`restart-interval` starts `producer`; `gate` is never executed and its exit code
cannot suppress the producer. This does not weaken the note's central boundary
(producer bytes still cannot establish rendered text), and it is not a false
report of S053. It is an unstated implementation exception in a sentence
presented as producer behavior.

Suggested L1 clause (text-only, note line 17 or the S054 sentence at 21):
“S054 honors `exec-if` only in the interval and signal workers (`delayWorker`,
`waitingWorker`); the continuous worker opens `exec` unconditionally.”

### A2 (low, provenance caption) — the named source subset omits two grounding symbols

Note line 1 names S053 sections `(DESCRIPTION, CONFIGURATION, RETURN-TYPE)` and
S054 symbols `(Custom::update, parseOutputJson, parseOutputRaw)`. Two claims in
the note require anchors outside those lists:

- `{icon}`/`{text}` at note:26–27 rest on S053 `FORMAT REPLACEMENTS`
  (S053:167–174), which is not in the note's S053 parenthetical.
- The one-`getline` claim at note:21–23 rests on `Custom::continuousWorker`
  (custom.cpp:66–115) and the constructor dispatch that selects it
  (custom.cpp:21–27), neither of which is in the note's S054 parenthetical.

Note line 3 says the rechecker should “inspect named sections.” A rechecker can
therefore verify the captioned subset and still miss the exact grounding for
those claims. `corpus/SOURCES.md` S053 already names `FORMAT REPLACEMENTS`; the
S054 row names only the three functions. Recommended: add `FORMAT REPLACEMENTS`
to the note's S053 parenthetical and `Custom::continuousWorker` (plus constructor
dispatch) to S054, and treat those as named sections. Owner: L1 (note and
SOURCES are L1-owned). This is a caption gap, not a false claim.

### A3 (informational) — undocumented `alt` is consumed by the JSON path

S053:150–157 documents only `text`, `tooltip`, `class`, `percentage`. S054 also
reads `alt` (268–272), formats `{alt}` (custom.cpp:175–177), and passes `alt_`
to `getIcon` (custom.cpp:176). Auxiliary tagged read `src/ALabel.cpp:132–151`
shows `alt` selecting a `format-icons` group when the object form is used, with
percentage indexing within the selected group. Thus note line 26's “`{icon}` is
selected from percentage” remains true, but the percentage selects within an
alt-chosen set. Note line 36 already acknowledges formatting `alt`, so there is
no internal contradiction. If source parity rather than S053-documented roles is
intended, add one clause: “S054 also accepts undocumented `alt`; it selects the
`format-icons` group.” The auxiliary ALabel read is not a proposed SOURCES row;
the registry remains L1-owned.

### A4 (informational) — `hide-empty-text` shorthand

Note line 37 says the module “can still hide on empty formatted text or
`hide-empty-text`.” S054:178 is the conjunction
`(config_["hide-empty-text"].asBool() && text_.empty()) || str.empty()`; S053:24–26
likewise says the option disables the module “when output is empty, but format
might contain additional static content.” The option alone does not hide; the
producer text must also be empty. The current wording is common shorthand and
not false, but an exact phrasing would be: “hide when the formatted string is
empty, or when `hide-empty-text` is set and raw producer text is empty.”

### A5 (informational) — raw single-line tooltip is not escaped even with `escape: true`

`parseOutputRaw` at S054:233–240 escapes `text_` and `tooltip_` in the `i == 0`
branch, then unconditionally executes `tooltip_ = validated_line;` at 240,
overwriting the escaped tooltip with the unescaped line. For two-line raw output
the `i == 1` branch does escape the tooltip (243–247). The JSON path escapes
`text_`, `alt_` and `tooltip_` (263–277). Note lines 49–50 say “conditionally
escapes text” and “GTK receives markup,” which is exactly true and commendably
narrow: `text_` is escaped under `escape`, while the raw single-line tooltip is
not. Do not broaden this to “`escape` sanitizes script output”; that would be
false for the raw single-line tooltip. This quirk strengthens rather than
falsifies the note's markup boundary.

### A6 (informational) — literal default differs from the documented default

S053:59–61 documents `format` default `{text}`. S054:9 passes the literal string
`"{}"` to `ALabel`; `src/ALabel.cpp:19` uses the config value when present, else
that argument, and `:31` stores it as `default_format_`. Under fmt automatic
indexing, `"{}"` should select the first named argument (`text`), making the
behavior equivalent [INFERENCE: no fmt, GTK or Waybar execution was performed].
Note line 26 is exact for the documented contract; if L1 wants source-literal
precision, attribute it to S053's `default:` and keep the `"{}"` detail out of
the claim. No correction is required for the note's current wording.

## Checked clean — exact support

- S053 DESCRIPTION quote is verbatim and correctly attributed (S053:8–9).
- Static-text instruction (“specify only the *format* field”) is exact (S053:9).
- JSON object example, `class` array form, and i3blocks newline form are exact
  (S053:154, 157, 159–163).
- Raw parser role order: line 0 text/tooltip, line 1 tooltip, line 2 class,
  then break (S054:226–254); JSON parser first-line stop (S054:261–290).
- Continuous mode reads one `getline` per wake and stores exactly one line
  (S054:80–114); mode dispatch is S054:21–27.
- Initial hide guard on configured `exec`/`exec-if` plus empty output/nonzero exit
  is reproduced exactly (S054:163–166).
- Visible-branch order `set_markup` → tooltip → class mutation → `event_box_.show()`
  is reproduced exactly (S054:181–207).
- `escape` default `false` is exact (S053:125–128).
- The four evidence-layer rows do not overclaim any source behavior; they remain
  consistent with the anchored stages.

## Limits and remaining unknowns

- No fmt/GTK/Waybar execution, no compiled test and no installed-binary
  comparison. The `"{}"` default equivalence is inference.
- The auxiliary `src/ALabel.cpp` read (tag 0.15.0, `getIcon`, constructor default)
  was used only to test the note's `{icon}` and default claims. It is not admitted
  to the registry and does not remove the note's `[UNK]` on “ALabel base-class
  details”; that line remains a truthful statement of what the note itself opened.
- No `measure.py` or gate run. Structural-impact assessment is from reading
  `.ufo/waves/round-16/measure.py` (`u7_facets` requires the four headings and
  `[UNK]` in `Unexercised rendering`; the U7 join requires reciprocal mined
  S053/S054 rows). Caption defects A2 are invisible to that counter.
- No package, service or host state was queried or changed; S053/S054 installed
  equivalence, current host Waybar version and any live rendered text remain
  unmeasured, as the note already states.
- No tools were installed or updated; no package operations were attempted.

## Recommendation to L1

1. Add the continuous-worker `exec-if` exception (A1) to note line 17 or 21;
   this is the only bounded counterexample to a producer-behavior sentence.
2. Extend the note's source caption/recheck set (A2) with S053
   `FORMAT REPLACEMENTS` and S054 `Custom::continuousWorker` plus constructor
   dispatch.
3. Optionally tighten A3 (`alt`) and A4 (`hide-empty-text` conjunction). Keep A5
   and A6 wording as-is; A5 is already conservative and A6 is manual-exact.

None of these changes the U7 claim's layer boundary or requires a new source.

Report: .ufo/waves/round-16/w2/reports/AttackU7Source.md
