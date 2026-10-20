# ProducerNotPixels — critic report (MadoR16 w1)

Attack: "successful producer text equals GTK rendered text or user-visible output."
Target under attack: uncommitted `corpus/knowledge/waybar-observation-boundaries-r16.md`
(read 2026-10-20), its S053/S054 rows (`corpus/SOURCES.md:65-66`), and the U7 lines
in `corpus/lessons/round-16.md`.

**Verdict:** the note's main point holds up. Its title (`:6`), the layer table (`:38-43`),
`:48` ("Do not promote success at one layer…") and lesson `:31` ("Reject: producer
output as proof of rendered text") already reject the equivalence. Nothing in the
committed-candidate text claims that producer text equals pixels. There are still four
**fixable calibration defects** where wording leaves the equivalence partly open, plus
one **structural-counter limit** that the judge must handle by reading the note body.
None of these is a harmful tradeoff. No defect calls for a new source row in this round.

Axes: coverage (U7 credit relies on the bounded claim), calibration (precision of the
claims), operability (no probe was needed to show any of this).

## Independent source binding

I fetched the tagged raw files again on 2026-10-20 in an eval Python session with
`urllib`: `man/waybar-custom.5.scd` is **6656 B**, `efb6a63a…0d82`, and
`src/modules/custom.cpp` is **8746 B**, `2232f7f7…291f`. Both match
`.ufo/waves/round-16/evidence/source-bindings.json` and SOURCES rows S053/S054.
Line numbers below refer to these exact bytes.

## Counterexamples to the equivalence: cases where producer success ≠ displayed text

All of these are static reads; none was executed. Items C1–C6 stay inside the admitted
S053/S054 sources. Items C7–C9 need sources that are not registered, so they are
**advisory only** this round.

| # | Counterexample | Evidence | Inside S053/S054? |
|---|---|---|---|
| C1 | The producer's text appears only where `format` references it. A static `format` that also has `exec` never displays stdout; stdout only controls whether the module is visible. | S054 `custom.cpp:175-176` (`fmt::format(fmt::runtime(format_), fmt::arg("text", text_)…`). **Host:** `~/.config/waybar/config.jsonc:62-68` `custom/update` has `"format": ""` plus `"exec": "omarchy-update-available"`. The bar shows a glyph, never the script's text. | yes |
| C2 | Stdout with a nonzero exit gets hidden, not shown. | S054 `:163-166`. The module stays hidden; `label_` is not rewritten on this branch. This also answers the old `waybar-walker-semantics.md:136` question ("how a non-zero exit renders… is MAN-undocumented") at the level of the tagged source: hidden, not the kept value, `[INF-source]`, not binary-equivalent. | yes |
| C3 | Only part of the output is consumed. JSON parsing reads the first line only (`:290` `break`). Raw parsing reads lines 0–2, then `break` (`:251`). Invalid UTF-8 is replaced (`:228-229` `make_valid`). | S054 | yes |
| C4 | In continuous mode, the i3blocks roles collapse. Each `getline` becomes an entire `output_` (`:81-112`, `output_ = {0, output}` `:112`), so each line is parsed as **text**. Tooltip and class lines from a looping script then display as text in turn. | S054. The draft `waybar-draft.txt` contained this point; the integrated note **dropped it**. | yes |
| C5 | Markup is interpreted, not shown literally. The visible branch is `label_.set_markup(str)` (`:181`), and `escape` defaults to false (S053 CONFIGURATION). **Host:** `custom/omarchy` `"format": "<span font='omarchy'></span>"` (`config.jsonc:57`) feeds a 30-plus-byte markup string that becomes one glyph in a specific font. `custom/ai-usage` uses `"escape": false`, `"format": "{}"` (`:252,254`). | S053 + S054 | yes |
| C6 | `escape: true` does not escape the raw first-line tooltip. Line `:235` escapes it, then `:240` overwrites `tooltip_` with the unescaped line. The `text_ == tooltip_` check at `:189` then fails, so `:192` sends unescaped markup to the tooltip. | S054 `:233-240,189-192` | yes |
| C7 | A manual producer run is a different invocation from Waybar's. Waybar uses `/bin/sh -c`, sets `WAYBAR_OUTPUT_NAME` per bar, and captures **stdout only** (`include/util/command.hpp:110-115` @0.15.0). S054 itself shows the per-output name being passed (`:11,58,69,97,130`). | Partly S054; the env/stdout details are unregistered | partly |
| C8 | A producer can succeed while the display keeps old content. **(a)** If JSON parsing throws (`include/util/json.hpp:37`), `bar.cpp:570-575` logs it and the label and visibility stay unchanged. **(b)** In GTK 3.24.52 `gtklabel.c`, `gtk_label_set_markup` stores the new `label` first (`:2808`). On a markup parse error, `gtk_label_set_markup_internal` returns early (`:2669-2675`, `:2716-2729`) and never calls `gtk_label_set_text_internal`. The input property is then new but the displayed text is old. Example: an unescaped `A & B` with `escape:false`, since Pango uses GMarkup per `pango_markup.md:56` @1.58.2. **[INFERENCE from source; not exercised].** | GTK/Pango/Waybar util files, unregistered. Host pkgconfig reports GTK 3.24.52 and Pango 1.58.2. Fetched `gtklabel.c` @3.24.52, sha `74b0e89e…0467`. | no |
| C9 | The label can be correct while the pixels are not. `mode: invisible` or SIGUSR1 sets window opacity to 0 and leaves the label intact (`bar.cpp:365-371`; `waybar.5.scd.in:222-223`). `max-length` uses Pango end-ellipsis, and its width comes from approximate character pixels, not a character count (`ALabel.cpp:38-44`; `gtklabel.c:3663-3678,3730-3734`). Rotate, CSS, font fallback and output/rail selection also apply. | unregistered | no |

## Defects and the smallest safe corrections (all owned by L1)

1. **Uncaveated anchor quote (calibration).** `note:15-16` and `lesson:40` use S053
   DESCRIPTION, "displays either the output of a script or static text", as the opening
   statement. Read literally, that sentence *is* the equivalence. C1–C4 contradict it
   from S054.
   *Correction:* add one sentence right after the quote, for example: "S054 narrows
   'displays': only the parsed text field is inserted, only where `format` references
   it, and the exit/empty/hide branches suppress display."
2. **Raw-roles overgeneralization (coverage/calibration).** `note:19-20` says raw output
   has newline-separated text, tooltip and class, without the continuous-mode exception
   (C4) or the first-line JSON limit (C3).
   *Correction:* restore one bullet from the draft citing S054 `:81-112,251,290`.
3. **GTK-state row is ambiguous (calibration).** `note:42` says "Instrumented GTK state
   … can establish inspected label/widget state at that instant". The GTK `label`
   property can disagree with the displayed text (C8b), and window opacity can be 0
   (C9).
   *Correction, no new source needed:* reword it as "the value of the specific property
   inspected; input markup, parsed text, visibility and opacity can differ". **Keep**
   `note:68` `[UNK] GTK behavior on invalid markup`. Do not resolve it with the
   unregistered GTK reading this round, because that would be uncited expansion.
4. **Escape precision (calibration).** `note:45` says "Source parsing conditionally
   escapes text". That is true for text, but not for the raw first-line tooltip (C6).
   *Correction:* add a five-word qualifier citing S054 `:240`.
5. **Minor:** `note:22` says "`format` defaults to `{text}`", which is the manual's
   wording. The source fallback literal is `"{}"` (`custom.cpp:9`). That is equivalent
   only by fmt positional indexing `[INF]`. Optionally add "(source fallback `{}`)".

## Tradeoff the judge must apply (no fix needed)

`measure.py:160-181` `u7_facets` checks only the four level-2 headings and the `[UNK]`
marker. A note that asserted "producer stdout is the rendered text" under those headings
would still score 7/7. A phrase blacklist would be easy to game and is **not**
recommended. The closure must keep the source/body inspection that `lesson:27-28`
already declares, including a check that no producer=display claim is present. For the
current note, that check passes apart from defect 1.

## Route candidates for later rounds (not this round)

C7–C9 show that `include/util/command.hpp`, `util/json.hpp`, `src/bar.cpp`,
`src/ALabel.cpp` @0.15.0 and GTK 3.24.52 `gtklabel.c` would let the existing `[UNK]`s at
`note:68-70` become `[INF-source]`. Each needs its own registry row, and none proves
host-binary behavior. Separately, the `waybar-walker-semantics.md:136` nonzero-exit
`[UNK]` could take an append-only erratum citing S054 `:163-166`.

## Limits and disclosure

These were static source reads only. I made no producer, `exec`, signal, Waybar,
compositor or screenshot call, and no package or service query. I did three local file
reads:
- a read-only `grep -n` of `~/.config/waybar/config.jsonc` for module keys;
- `Version:` from `/usr/lib/pkgconfig/gtk+-3.0.pc` and `pango.pc`;
- the lane's own `.ufo` and corpus files.

Network fetches were limited to tagged raw source and docs. I installed and updated
nothing, and edited no files besides this report. The host-config line numbers are a
read from 2026-10-20 only.
