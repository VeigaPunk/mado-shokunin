# AttackQuotes — lesson Gate new-row quote check (S053, S054, S055)

Seat: `MadoR16.AttackQuotes` (leaf reviewer; no subagent dispatch). Lane: `mado-shokunin`. Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
Target: `corpus/lessons/round-16.md` §Gate, the three new-row quotes, plus the ownwork (S055) path justification.
Method: source reading of lane files; public tagged Waybar sources fetched read-only with `curl -fsSL` and hashed/searched in memory (no files written). Git read-only (`git show 32c4fda:…`, `git log`). No census, lint, build, test, gate, pacman, package, service, omp CLI, agent.db, or live host/compositor probe. Installs or updates: none.

## Verdict

All three quotes are **exact** and **≤25 whitespace words**. None is **located to a line** in the lesson, though each is locatable from the tag/path plus a section or function name, and each has a measured line that is cited nowhere in the lesson. The ownwork (S055) path is **not adequately justified**: the lesson's sentence asserts "own-work" without a rule, and the file's own header names a non-author outside closure as author. Two findings are MEDIUM; the rest are LOW. No lesson edit was made by this seat.

## Quote-by-quote results

| Row | Lesson text (round-16.md) | Recount | Exact source match | Located in lesson | Measured location (this seat) |
|---|---|---|---|---|---|
| S053 | `The *custom* module displays either the output of a script or static text.` (line 52; "Thirteen whitespace words") | 13 | Exact, raw bytes incl. scdoc `*` markers. Tagged bytes 6656 B, sha256 `efb6a63a…d82` = registry = `evidence/source-bindings.json` | `DESCRIPTION` section name + tag 0.15.0 only; **no line** | man `waybar-custom.5.scd:8` |
| S054 | `label_.set_markup(str);` (line 56; "One token") | 1 token | Exact after stripping 8-space indent; tagged 8746 B, sha256 `2232f7f7…b291f` = registry = binding file | `Custom::update`, "visible formatted-string branch" only; **no line** | `src/modules/custom.cpp:181`, inside the `else` of the hide guard at :178–179 |
| S055 | `These are explicitly hard-coded in-memory controls, not real pacman dry-run output` (lines 59–61; "Eleven whitespace words") | 11 | Exact after hard-wrap normalization. Blob at `32c4fda` (18504 B) and working copy share the same bytes (sha256 prefix `58e247f8525483eb` both) | `corpus/lessons/round-15-verifier-spotcheck.md` + §"Gate and correction evidence"; **no line** | `corpus/lessons/round-15-verifier-spotcheck.md:161-162` (wrapped) |

Counting: the lesson gives counts as words (13/1/11). My recount with `len(q.split())` on the quote as it appears in the bytes agrees on every row. The lesson does not state the counting method (see F4).

## Findings by severity

### F1 — MEDIUM — "Located" fails at line granularity for all three new rows
- `corpus/lessons/round-16.md:51-62`: S053 anchored to `DESCRIPTION`; S054 to `Custom::update`, visible formatted-string branch; S055 to `§Gate and correction evidence`. No row gives a line number.
- QUALITY 2 (`corpus/QUALITY.md:4`) requires a measured anchor "(path:line, command, …)". Round-16 w1 `QuoteAdmission.md` F2.3 and F3 already requested line anchors for exactly these rows.
- Counterexample to "located" as a reader would apply it: a reader cannot land on S054's line without re-reading all of `Custom::update` (:162–220); S054's line is :181. The S055 location is a wrapped two-line quote; without `:161-162` the reader must search the spotcheck for a phrase that the lesson rendered with different wrapping.
- Fix for L1 (not applied here): add `man:8`, `custom.cpp:181 (within 162–220)`, and `round-15-verifier-spotcheck.md:161-162` to the Gate rows.

### F2 — MEDIUM — S055 ownwork justification is incomplete and contradicted by the file's own header
- Lesson `round-16.md:59-63` says: "own-work source opened at baseline, not external authority … Full local source path is the URL substitute for this own-work row." It gives no rule for what "own-work" means.
- The file header states authorship outside the lane: `round-15-verifier-spotcheck.md:1` "author: hyaku closure (non-author integrator, @m_strong)"; `:5` "Reviewer: `hyaku-closure (@m_strong session, non-author)`". Its git commit `32c4fda` is by `protocol-shokunin` with subject "round-15 verifier spot-check (integrator, hyaku): non-author admit/reject".
- Other own-work rows in `corpus/SOURCES.md` (S001, S002, S014, S015, S019, S041, S044, S049) are lane-authored tools, lessons or captures. S055 is the first own-work row whose content is authored by a non-author closure. The label is repository residency, not authorship, and the lesson does not say so.
- "Not external authority" is also inaccurate as a justification: the incident is established by the operator's report as relayed in the closure (`round-15-verifier-spotcheck.md:189` "Established operator incident"; `:261` "The user/operator supplied the violation as established"). The authority for the incident is the operator, and S055 only carries the closure's relay of it.
- Census check: `scripts/sources-census.sh:655` validates `kind` against an enum that includes `own-work`. It does not check authorship, so the label passes validation without justifying itself.
- Fix for L1: state the rule in the lesson Gate. Example: "own-work = a lane-resident file retained as evidence; authorship is the non-author closure at `round-15-verifier-spotcheck.md:1`; the incident authority is the operator relay quoted at :261." Alternatively, cite the operator relay as the authority and keep S055 as a lane-retained row.

### F3 — LOW — S055 registry anchor and "baseline" wording are ambiguous or wrong
- `corpus/SOURCES.md:67` S055 anchor: "closure at baseline 32c4fda873c9…". `32c4fda` is the commit that recorded the closure (see `git log`). The closure's own reviewed baseline is `ea0446fcb4840089…` (`round-15-verifier-spotcheck.md:6-9`), measured content `5f13870…`, delivered `9ebd737…`.
- The lesson's "own-work source opened at baseline" (`round-16.md:61`) uses "baseline" without saying which. Under the lane contract it means `32c4fda`; under the file it means `ea0446f`. A reader cannot tell.
- Fix for L1: anchor S055 as "reviewed baseline ea0446f…; delivered 9ebd737…; recorded at 32c4fda…" and say "lane baseline 32c4fda" explicitly in the lesson.

### F4 — LOW — Counting method is not stated
- Lesson counts (13/1/11) are asserted, not defined. `round-16.md` Gate states no method and no code-quote rule (QuoteAdmission F2.1–F2.3 asked for both).
- Counterexample: without a rule, "whitespace words" for S053 could be read as counting `*custom*` as one token (13, agrees) or with `*` stripped (13, agrees); S054 could be read as 1 token or as 3 if one counts `(`, `)`, `;` as separate tokens. The lesson's numbers survive the natural reading but the reading is not stated.
- Fix for L1: add one sentence: "Count = `len(quote.split())` on the quote as it appears in the raw bytes, after hard line-wrap normalization only; code quotes are one verbatim source line counted on that line."

### F5 — LOW — Prior w1 F1 (missing used-by targets) is resolved
- Both lesson/knowledge targets now exist as untracked lane files: `corpus/knowledge/waybar-observation-boundaries-r16.md` and `corpus/lessons/round-16.md`. The `used-by` values at `corpus/SOURCES.md:65-67` resolve. This seat did not run the census (E11) and does not claim it passes.

## Verified-as-correct items (no finding)
- S053 quote: exact at man:8; 6656 bytes; sha256 `efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82` = `.ufo/waves/round-16/evidence/source-bindings.json` = `corpus/SOURCES.md:65`.
- S054 quote: exact at cpp:181; the branch is the visible one (hide guard :178–179 precedes it); 8746 bytes; sha256 `2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f` = binding file = `corpus/SOURCES.md:66`.
- S055 quote: exact across wrap at `round-15-verifier-spotcheck.md:161-162`; committed blob at `32c4fda` matches working copy (`git diff --stat` on the file is empty).
- All three recounts ≤25 words.

## Residual risk and limits
- The S053/S054 source was read as tagged bytes (0.15.0). It is source-only; not installed-binary equivalence and not rendered output. The `label_.set_markup` line shows the GTK-markup route, not pixels.
- The S055 claim is a relay of an operator-established incident. This seat did not re-verify the pacman transaction, did not query the host, and does not assert host state.
- I did not read `corpus/knowledge/waybar-observation-boundaries-r16.md` beyond its S053/S054 mentions; the note's bounded claims are outside this assignment.

## Checks L1 should run once after integration
- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` (E11 now has targets; confirm no E-class failures for S053–S055).
- Re-fetch and sha256 the two tagged sources to confirm the binding file (no change expected).
