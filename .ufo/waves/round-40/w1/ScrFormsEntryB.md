# Seat ScrFormsEntryB — draft B of the getoption native-forms entry (round 40, w1)

STATUS: DONE — draft delivered; two prerequisites flagged for the L1 (F1 blocking, F2 mechanical).

Target: `.ufo/waves/round-40/w1/ScrFormsEntryB/entry.md` — the parser-semantics ordering
(declaration → handler → stored value → toString → reply → label), written without reading
`.ufo/waves/round-40/w1/ScrFormsEntryA` (per assignment).

## Deliverables (all inside the seat directory)

| path | lines/bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-40/w1/ScrFormsEntryB/entry.md` | 89 lines, 12064 B | `d0493cd3d0b8cf4baecf5cd02eb827df7f028592c70776bbbb3314444b89786f` |
| `.ufo/waves/round-40/w1/ScrFormsEntryB/census-rows.json` | 70 rows, raw ref-tool census | `cde4b2dfb586e5d9765af1df6f73188da3537b53f13a9525d21b693684905462` |
| `.ufo/waves/round-40/w1/ScrFormsEntryB/census.txt` | own-work census summary | `db4b07896ad65d875abe732adf8db373619e1b761299689105a143953cbfa569` |

No tracked file was edited, no git/jj verb was run (read-only `git show`/`grep` only), nothing was written
outside this seat directory, `/tmp` scratch removed. No tool was installed (none needed).

## What the draft contains

Sections in parser order: §1 declaration (hyprlang `configSetValueSafe` call site and category-qualified
lookup, variable substitution before the call), §2 handler (five type arms; gradient/gap/font-weight are
registered CUSTOM setters, not directives; the gradient setter clears colours every redeclaration and sets
the angle only in the `deg` branch — hence angle inheritance), §3 toString (the `IComplexConfigValue`
print contract, `{:x}` unpadded lowercase hex + `{}deg`, four-value gaps, numeric weight), §4 reply (one
object, one form field, `no such option`, `[[EMPTY]]`, six-decimal floats, `set` semantics), §5 label
(reconstruction + held vocabulary + the two-row worked example + the census counts), §6 what this does not
license, Limits, and the required provenance split (host census vs upstream bytes vs held knowledge).

Source lines (5, within the first 20 lines): `S162`, `S173`, `S180` (held, re-opened) and `S_FORMS_1`,
`S_FORMS_2` (new). Placeholders are `S_FORMS_*` as assigned; the counter's `SRC_RE` needs `S\d{3,}`, so
**the L1 must substitute real ids (highest existing id is S277 → next free S278, S279)** or clause b fails.

## Own-work re-derivations (scratch, 2026-10-25)

1. Static key set: `python3 -I tools/mado-options.py --home $HOME` → exit 0, a 70-row JSON list.
2. Form census, one `hyprctl getoption -j KEY` per key (read-only verb, no other compositor verb run):
   `int=44 float=5 str=8 custom=13`, total 70, every reply exactly one of the four form fields, none
   `no such option`, all exit 0 — reproduces the committed capture `c1/native-capture.jsonl`
   (`1fe39c0528f1b11d7f69bf41ac236f39ff6e00b9b8a275f4e94b06c5189b4b25`).
3. Label census with the reference control tool (`.ufo/waves/round-40/c1/ctl-ref-tool.py.txt`, sha256
   `f96d9e0a0d2fe1bccb87940244db079de88c6794f03d66a36304d574694a08aa`, copied to `/tmp`, `--live --home
   $HOME`, exit 0): 70 rows, `agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0`.
   The 8 `agreement*`: `decoration:rounding`, `general:border_size`, `general:gaps_in`, `general:gaps_out`
   (toggle), `general:col.active_border`, `group:col.border_active` (theme), `input:kb_layout`,
   `input:kb_options` (user).
4. Custom-form breakdown of the 13: 9 gradients, 2 gaps (`general:gaps_in/out`), 2 font weights
   (`group:groupbar:font_weight_active` `ultraheavy`→`1000`, `…_inactive` `normal`→`400`).
5. Spot replies (verbatim, in `census.txt`): `general:col.active_border` → `ffe68e0d 45deg`;
   `group:col.border_inactive` → `aa595959 0deg`; `input:accel_profile` → `[[EMPTY]]`, `set:false`;
   `misc:font_family` → `Sans`, `set:false`; `no:such:key` → `no such option`, exit 0.

These are **scratch re-derivations, not the C2 receipt**: clause h binds the receipt to
`sha256(tools/mado-options.py at REV)` and to the two count lines, so the committed census receipt must be
produced by the delivered tool. If the delivered tool's counts differ from the reference control's, the
entry's two count lines must be regenerated from it — the numbers are a claim, not decoration.

## Quote slots — verified with the counter's own normalizer

Each quote was checked by applying the counter's `norm()` (script/style/tag stripping, entity decoding,
whitespace collapse) to the receipt bytes and to the entry line; all six bind (`id` on the same line,
quote present, 3-25 words).

| id | receipt | sha256 | anchor | words |
|---|---|---|---|---|
| S162 | `fetch/config-manager-efb5099.bin` | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | `ConfigManager.cpp:120` (m_angle) | 10 |
| S173 | `fetch/hyprlang-config-v0.6.8.bin` | `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e` | `src/config.cpp:219` (ARGB) | 14 |
| S180 | `fetch/complex-data-types-efb5099.bin` | `95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807` | `:107` (3-token gap) | 5 |
| S180 | same | same | `:134` (gap toString) | 9 |
| S_FORMS_1 | **receipt pending** — `ComplexDataType.hpp` @ efb5099 | `e7fee893be361e6e11102aeac549dd8ed527dd2c0e1a5a879f717b4c8222882e` (481 B, HTTP 200) | `:20` (`toString() = 0`) | 6 |
| S_FORMS_2 | **receipt pending** — census receipt | — | its `labels …` line | 6 |

Fetch for the pending receipt (provenance only — I read it in `/tmp`, the L1 commits the bytes):
`curl -sS -o .ufo/waves/round-40/fetch/complex-data-type-efb5099.bin https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataType.hpp`
→ sha256 `e7fee893…`, 481 B; verify with `sha256sum` before writing the Gate line.

## F1 (blocking, C2 as registered) — the planned new ComplexDataTypes row collides with S180

The registration plans "at least two new rows … (Hyprland `ComplexDataTypes.hpp` at the pinned commit; an
own-work row …)". **S180 already anchors that exact URL and file sha** (`corpus/SOURCES.md:192`,
`sha256:95733223…`). A new row on it would (i) fail `PRED-C2-r40-v1` clause e (a new id's location must
occur in no other registry row) and (ii) repeat the canonical URL that QUALITY.md criterion 17 sends to
merge review. A tag-URL rewrite (`/v0.56.2/…`) would dodge clause e on a string technicality and is not
used here.

Draft B therefore cites the ComplexDataTypes bytes through **held S180 (re-opened)** and opens a distinct
new row: **`src/config/shared/complex/ComplexDataType.hpp`** (the `IComplexConfigValue` base interface —
`toString()` is the print contract, three complex data types). Its URL tail occurs in no registry row
(checked against all 214 rows). If the L1 keeps the registration's plan instead, clause e fails and C2
scores 0/1.

## F2 (mechanical trap) — angle-bracket spans are destroyed by the gate normalizer

The counter strips `<[^>]+>` from receipts before matching. Consequences measured this round:
`std::format("{}deg", sc<int>(m_angle * 180.0 / M_PI))` (the gradient `toString`) and most of
`include/hyprlang.hpp` (the `CConfigCustomValueType` member block) do **not** survive normalization, so a
quote taken from them can never bind. Every quote in the draft was chosen after running `norm()`; the
gradient `toString` lines are cited by path:line only.

## Registry rows the L1 must write (11 cells each; `## Registry`)

New rows (status `mined`, opened `2026-10-25`, recheck `on-change`, used-by must contain
`corpus/knowledge/hyprctl-getoption-native-forms-r40.md`):

- `S_FORMS_1` (kind `code`, tier A) — source cell ends with the `ComplexDataType.hpp` URL at `efb5099`;
  anchor `src/config/shared/complex/ComplexDataType.hpp:7-21 @ efb50993780079460b0cbed1363e2166a2de1d9f,
  sha256:e7fee893be361e6e11102aeac549dd8ed527dd2c0e1a5a879f717b4c8222882e, 481 B`; teaches "every complex
  option value must implement `toString()`; the enum names gradient, CSS-value and font-weight".
- `S_FORMS_2` (kind **own-work**, tier A) — source cell must end with the committed receipt path, e.g.
  `.ufo/waves/round-40/fetch/forms-census-r40.txt` (that tail must occur in no other row); anchor that path
  plus the tool sha and the run date; teaches "what the host's 70 declared keys answer and how they label".

Held rows `S162`, `S173`, `S180`: **only** `status`/`recheck`/`used-by` may change (cells 1-10 must stay
byte-equal to the BASE row, clause c); append the entry path to `used-by`.

## Gate lines (`corpus/lessons/round-40.md`, `## Gate`)

One line per cited id, shape
`GATE <id> receipt=<path under .ufo/waves/round-40/fetch/> sha256=<64 hex> quote="<the quote from the table>"`.
`S_FORMS_2`'s receipt must additionally contain `sha256(tools/mado-options.py at REV)`, the line
`forms int=44 float=5 str=8 custom=13` and the line
`labels agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0` (clause h; both lines already
appear verbatim in the entry). Note the quote must be 3-25 words **and** survive F2.

## Other prerequisites

- `corpus/README.md`: exactly one column-zero index row for the entry (clause f), baseline 56/56 rows.
- Replace `S_FORMS_1`/`S_FORMS_2` everywhere with `S\d{3,}` ids before counting (clause b).
- Keep the entry's `verified-at: 2026-10-25` and `recheck: on-change` lines (clause b).

## Findings against the claims

- **F1** (above): the registration's ComplexDataTypes new row is a duplicate of S180 — affects C2's
  verdict, not just its prose.
- **F2** (above): quote selection is constrained by the normalizer.
- **F3** upstream quirk, unexercised on the host: `CFontWeightConfigValueData::parseWeight` assigns 400 only
  when the parsed numeral is out of range (`ComplexDataTypes.hpp:167-175`), so an in-range numeral such as
  `600` would leave the stored default 400. Both host weight rows are names, so the census cannot show it;
  the entry states the quirk from bytes and marks it unexercised.
- **F4** the entry cannot claim hyprctl's own formatting of `int`/`float`/`str`: `HyprCtl.cpp` was not
  fetched this round (and S018 holds that URL, so a new row on it would hit F1's rule). The entry marks
  this `[UNK]` and the `set` mapping as host-observed + source-inferred.

## Out of scope (not done, not claimed)

- No registry row, Gate line, README row or lesson edit was made (L1 is the only integrator).
- No `--live` implementation, no counter run against the lane (the delivered tool does not yet exist);
  `PRED-C2-r40-v1` was read, not executed.
- No compositor verb other than `hyprctl getoption -j`; no package transaction; no host config write.
