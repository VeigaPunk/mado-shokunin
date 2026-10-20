# QuoteAdmission — quote ≤25-word and source-location admission review (S053/S054)

Seat: `MadoR16.QuoteAdmission` (reviewer, leaf). Lane: `mado-shokunin`. Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
Method: source reading only. Read-only lane files; public raw tagged sources fetched with `curl -fsSL … | sha256sum` / `| wc -c` / in-memory Python (no files written, no lane edits). No census, lint, build, test, gate, package, service, or host probe run. Installs: none.

Axes: (1) admission rule correctness, (2) location precision (path:line, tag, digest), (3) boundary honesty of teaching cells. Coverage is the target axis; operability is untouched by this seat.

## Verdict

S053 and S054 are source-real: both tagged URLs resolve, both raw SHA-256 values in the registry match the fetched bytes, and every prose quote I tried matches the tagged bytes exactly. The rows are **not yet admission-complete** because of four gaps: (A) both `used-by` paths are absent on disk, (B) anchors lack line numbers and byte counts, (C) the ≤25-word rule is a lesson convention with no stated count method or code-quote rule, (D) the S054 teaching omits a source-located escape defect. Closing A–D is needed before the Gate table can claim verbatim, located quotes.

## Findings by severity

### F1 — HIGH — `used-by` targets missing, so `mined` cannot validate yet
- `corpus/SOURCES.md` S053 `used-by` = `corpus/knowledge/waybar-observation-boundaries-r16.md`. **Missing on disk** (`ls`/exists check at 05:39–05:40).
- `corpus/SOURCES.md` S055 `used-by` = `corpus/lessons/round-16.md`. **Missing on disk.**
- Census `E11` (`scripts/sources-census.sh` `usedby_findings`) fails any `mined` row whose used-by path does not exist. L1 must land both files before the single post-integration verification; otherwise the rows fail as written.
- Note: `.ufo/waves/round-16/waybar-draft.txt` exists; it is a draft, not the used-by target.

### F2 — HIGH — Quote-admission rule is a convention, not a codified or countable rule
- The `≤25 words` requirement lives only in lesson § Gate prose (`corpus/lessons/round-13.md:28`, `round-14.md:59`, `round-15.md:85`, `round-15-verifier-spotcheck.md:195-196`). `corpus/QUALITY.md` (criteria 1–20) and `SKILL.md` contain no quote-length or quote-location criterion. The census does not count quotes.
- Consequence: the only admission evidence is the lesson table. It must state the counting method, or the count is not reproducible.
- Required in the round-16 lesson Gate (for S053/S054 and any other new row):
  1. Count = `len(quote.split())` over the quote as it appears in the tagged bytes, after hard line-wrap normalization only. Say so explicitly.
  2. scdoc markup: S053 prose contains `*emphasis*` markers and `++` line-break markers. Either quote the raw bytes including `*`, or state that `*` is stripped. Do not quote across `++`. Token counts are unaffected by attached asterisks, but exact-match is.
  3. Code quotes (S054) are not prose: quote one verbatim source line, state its file line number, and count whitespace tokens on that line only. Do not present multi-line code as one quote.
  4. Record byte size and SHA-256 per source (round-15 precedent: "16990 bytes" plus digest).
- Optional, for QUALITY owner (QualityGround/L1): a candidate criterion making these four points admission law. Not required for S053/S054 to be admitted under the lesson table.

### F3 — MEDIUM — Location anchors are section/function names, not line anchors (QUALITY 2 asks for path:line)
- S053 anchor: "DESCRIPTION, CONFIGURATION exec/return-type/interval/signal, RETURN-TYPE, FORMAT REPLACEMENTS". Measured section lines in the tagged file: `# DESCRIPTION` :6, `# CONFIGURATION` :11, `# RETURN-TYPE` :148, `# FORMAT REPLACEMENTS` :168, `# EXAMPLES` :176. Keys: `*exec*` :15, `*return-type*` :33, `*interval*` :37, `*restart-interval*` :45, `*signal*` :52, `*tooltip-format*` :120, `*escape*` :125.
- S053 byte size: **6656 bytes** (add to anchor).
- S054 anchor: "Custom::update, parseOutputJson, parseOutputRaw". Measured: `update()` :162–220, `parseOutputRaw()` :222–255, `parseOutputJson()` :257–292 (its `break;` at :290 is the first-line-only JSON read). Add these ranges plus `set_markup` :181, `set_tooltip_markup` :188/:190/:192, empty-output hide :164–166.
- S054 byte size: **8746 bytes** (add to anchor).
- Recommended anchor wording (S054): `tag 0.15.0; custom.cpp:162-220 update, :222-255 parseOutputRaw, :257-292 parseOutputJson, :181 set_markup, :233-240 escape/tooltip assignments; 8746 bytes; raw sha256 2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f`.

### F4 — MEDIUM — S054 teaching omits a source-located tooltip/escape defect
- `custom.cpp` `parseOutputRaw()`, tagged bytes:
  - :233 `if (config_["escape"]…asBool()) {`
  - :235 `tooltip_ = Glib::Markup::escape_text(validated_line);` (escaped)
  - :238 `tooltip_ = validated_line;` (else branch)
  - **:240 `tooltip_ = validated_line;`** — unconditional, after the if/else, overwrites the escaped tooltip with the raw line.
- Source-level reading: with `escape: true` in raw (non-JSON) mode, `text_` is escaped (:234) but the tooltip is not (:240 wins). The tooltip is then set as markup at :188/:190/:192.
- Limit: this is a tagged-source observation (0.15.0), not installed-binary behavior and not rendered output. Scope the claim exactly that way.
- Any draft line saying "escape applies to script output" must be bounded to text and JSON mode, or cite :240.
- CustomTooltip scout and WaybarDraft should carry this; the S054 row should be updated only after L1 decides the teaching wording.

### F5 — LOW — Negative claim "`{alt}` not documented in the man" is verified and needs its sweep recorded
- Command evidence (tagged man bytes): `count('{alt}') = 0`; `\balt\b` matches = 0. The FORMAT REPLACEMENTS section (:168–175) lists exactly `{text}` :170, `{percentage}` :172, `{icon}` :174.
- Code supplies an `alt` argument to `fmt::format` at :175 and :186 (`fmt::arg("alt", alt_)`), and parses JSON `alt` at parseOutputJson.
- Per QUALITY 11, an absence claim must carry its sweep, pinned tag, and matching locations. Record the two commands above (or equivalent) in the lesson. The claim is consistent with the existing note `corpus/knowledge/waybar-walker-semantics.md:161` ("alt (undocumented)"), which is not a new contradiction.

### F6 — LOW — Two prose quotes are sensitive to scdoc `*` markers; one JSON literal is not prose
- Quote `When *return-type* is set to *json*, …` contains markers in-line. Quote raw or declare stripping (F2.2).
- The `return-type` JSON example line (`{"text": "$text", "tooltip": "$tooltip", …}`) is a literal, not prose; do not count it toward the 25-word prose rule and do not quote it as a prose sentence.

### F7 — ADJACENT (not in S053/S054 scope; flagged for L1) — S055 anchor misstates the reviewed baseline
- `corpus/SOURCES.md` S055 anchor reads "closure at baseline 32c4fda873c9cb47a84c549b24b80ead2bcaa1ea".
- The closure lesson states: reviewed baseline `ea0446fcb4840089f0e541d96350144506fb5d1d` (`corpus/lessons/round-15-verifier-spotcheck.md:6-9`), measured content `5f13870…`, delivered `9ebd737…`. `32c4fda` is the git commit that **recorded** the closure (`git log`: "round-15 verifier spot-check (integrator, hyaku): non-author admit/reject").
- Recommended: "reviewed baseline ea0446f…; delivered 9ebd737…; closure recorded at 32c4fda…". Also see F1 for the missing `used-by` target.

## Verified quote table (exact match against tagged bytes, 2026-10-20 fetch)

| row | location (tag 0.15.0) | quote (raw) | prose tokens | match |
|---|---|---|---|---|
| S053 | man :8 | The *custom* module displays either the output of a script or static text. | 13 | exact |
| S053 | man :9 | To display static text, specify only the *format* field. | 9 | exact |
| S053 | man :42 | If no *interval* or *signal* is defined, it is assumed that the out script loops itself. | 16 | exact |
| S053 | man :50 | Once the script exits, it'll be re-executed after the *restart-interval*. | 10 | exact |
| S053 | man :128 | Option to enable escaping of script output. | 7 | exact |
| S053 | man :150 | When *return-type* is set to *json*, Waybar expects the *exec*-script  to output its data in JSON format. | 17 | exact (source has a double space before "to"; normalize whitespace and say so) |
| S053 | man :159 | If nothing or an invalid option is specified, Waybar expects i3blocks style output. | 13 | exact |
| S053 | man :170 | *{text}*: Output of the script. | 5 | exact |
| S054 | cpp :165 | `(output_.out.empty() \|\| output_.exit_code != 0)) {` | code line | exact |
| S054 | cpp :181 | `label_.set_markup(str);` | code line | exact |
| S054 | cpp :240 | `tooltip_ = validated_line;` | code line | exact (see F4) |
| S054 | cpp :290 | `break;` (parseOutputJson, first-line-only) | code line | exact |
| S054 | cpp :95 | `std::max(1L,` (restart-interval floor, ms) | code line | exact; supports man "Minimum value is 0.001 (1ms)" only via :95 expression, not the man's wording |

Digests (computed, matching registry): man `efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82`, 6656 bytes; cpp `2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f`, 8746 bytes.

## Verification commands (reproducible, read-only; L1 may rerun once)

```sh
curl -fsSL https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/man/waybar-custom.5.scd | sha256sum   # efb6a63a…
curl -fsSL https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/custom.cpp | sha256sum      # 2232f7f7…
curl -fsSL https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/man/waybar-custom.5.scd | grep -c '{alt}'  # 0
```

## Checks I did not run (per lane contract)
- `scripts/sources-census.sh validate` (E11 would fail until F1 is resolved). Left for L1's single post-integration verification.
- No quote word-count script was saved to the lane; counts above are my in-memory counts and are reproducible from the commands.

## Residual risk and limits
- Tag-source equivalence is not installed-binary equivalence. The installed Waybar 0.15.0-3 was not queried (no host probe). Any "installed/host" wording is out of scope.
- The `escape` defect (F4) is a static reading of one tag; it is not reproduced by execution and must stay labelled `[INF-src]`/source-only.
- Rendered GTK output, tooltip display, and signal delivery remain unobserved, consistent with the U7 boundary.

## Recommended edits for L1 (not applied by this seat)
1. Land `corpus/knowledge/waybar-observation-boundaries-r16.md` and `corpus/lessons/round-16.md` before validation (F1).
2. Add line anchors and byte counts to S053/S054 anchors; correct S055 anchor (F3, F7).
3. In the lesson Gate table, add quote-count method, raw-byte statement, and code-line rule (F2, F6).
4. Carry the raw-mode tooltip escape observation (F4) into the S054 teaching or the note, bounded to tag-source.
5. Record the `{alt}` absence sweep (F5).
