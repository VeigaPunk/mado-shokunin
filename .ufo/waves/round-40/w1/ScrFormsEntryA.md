# Seat ScrFormsEntryA — Draft A of `corpus/knowledge/hyprctl-getoption-native-forms-r40.md`

Seat: scribe, inline v2 wave w1, mado round 40 (hyaku run 7, 2026-10-25). Leaf: no subagent
dispatch, no background jobs, no compositor mutation, no package transaction. Writes are confined to
my seat directory plus this report; no tracked file was edited; no mutating git/jj verb was run (one
read-only `git ls-tree -r --name-only 5e7e885…` to test whether `fetch/` is in the freeze — it is not).

## Deliverables

- `.ufo/waves/round-40/w1/ScrFormsEntryA/entry.md` — Draft A, **134 lines** (cap 140). Four
  `source:` lines in the first 20 lines, `verified-at: 2026-10-25`, `recheck: on-change`,
  OBS/INF/UNK sections, 14 OBS paragraphs each carrying at least one `<<QUOTE S_ID: …>>` slot
  (15 slots), both clause-h count lines verbatim on single lines.
- `.ufo/waves/round-40/w1/ScrFormsEntryA/rederive-census.py` — own re-derivation (read-only,
  stdlib only; prints, writes nothing).
- This report.

## Behavior delivered

1. §1 reply shape — one JSON object per key: `option`, exactly one of `int|float|str|custom`,
   `set`; `no such option` as plain text with exit 0; `set` as declarer discriminator; the form
   follows the registered type, not the declared spelling.
2. §2 per-form conversion table — six rows (int, float, str, gradient, CSS gap, font weight) with
   the rule location per row, plus the host's own worked values.
3. §3 gradient angle inheritance — the host's two rows (`general:col.active_border` inherits 45°;
   `group:col.border_locked_active` keeps the two-colour gradient), the control pair separating
   variable-expansion-time from angle state, and the falsifier (inheritance off ⇒ exactly 2
   mismatches on those two keys).
4. §4 the census under the native model, both count lines verbatim, the 8 shadowed keys named; §3 ends
   with the falsifier line `variant-noinherit labels agreement=62 agreement*=6 mismatch=2 config-only=0
   live-default=0` (confirmed verbatim in ExecLiveCensus's receipt), whose Gate quote is that whole line.
5. §5 what this does not license + Limits (placeholders, anchor-range erratum, the `norm()`
   Gate-quote hazard, working-tree bytes, registry location-token uniqueness).

## Gates I ran (command → output)

| # | command | outcome |
|---|---|---|
| 1 | `hyprctl version` | `Hyprland 0.56.2 … commit efb50993780079460b0cbed1363e2166a2de1d9f`; `Hyprlang: built against 0.6.8, system has 0.6.8` |
| 2 | `hyprctl getoption -j __mado_r40_no_such_option__; echo rc=$?` | `no such option`, `rc=0` |
| 3 | `hyprctl getoption -j general:col.active_border` | `{"option": "general:col.active_border", "custom": "ffe68e0d 45deg", "set": true }` |
| 4 | `hyprctl getoption -j general:gaps_in` / `general:gaps_out` | `{"custom": "0 0 0 0", "set": true }` both |
| 5 | `hyprctl getoption -j decoration:shadow:color` | `{"custom": "ee1a1a1a 0deg", "set": true }` |
| 6 | `hyprctl getoption -j general:border_size` / `input:sensitivity` / `general:layout` | `{"int": 0}`, `{"float": 0.000000}`, `{"str": "dwindle"}`, all `set: true` |
| 7 | `hyprctl getoption -j misc:font_family` | `{"option": "misc:font_family", "str": "Sans", "set": false }` (undeclared ⇒ engine default) |
| 8 | `hyprctl getoption -j decoration:blur:enabled` | `{"int": 1, "set": true}` (declared `yes, please :)`) |
| 9 | `python3 -I .ufo/waves/round-40/w1/ScrFormsEntryA/rederive-census.py` | `forms int=44 float=5 str=8 custom=13` / `labels agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0` / `rows=70 capture=70 sum_forms=70 sum_labels=70` / 8 shadowed keys / `active_border live=('custom', 'ffe68e0d 45deg', True) angle=45 decls=2` |
| 10 | `python3 -I tools/mado-options.py --home "$HOME"` | 70 rows; `input:sensitivity` = `{value:'0', owner:'.local/share/omarchy/default/hypr/input.conf', line:11}` |
| 11 | `grep -Fc` of each quote candidate in the three fetch blobs | each occurs exactly once in the blob its id names |
| 12 | counter-`norm()` test of each chosen quote (`norm(quote) in norm(blob)`) | `True` for all four source quotes (S162 ×2, S173, S_FORMS_1); **`False`** for the obvious `{:x}` gradient line (`:72`) and the `{}deg` line (`:75`) — see finding 2 |
| 13 | clause screen on `entry.md` (inline script, not committed; counter semantics: whitespace-collapse only on entry lines) | 4 source ids in the first 20 lines; per-quote clause-g hits 1/1/1/1; both count lines present and single-line; 14 OBS paragraphs, 0 without a slot; 134 lines |

Counts were re-derived from scratch (gate 9) by importing the delivered static resolver read-only
(`importlib`) and applying my own `configStringToInt` / gradient / gap / weight conversion written
from the fetched sources — the reference control `c1/ctl-ref-tool.py.txt` was neither imported nor run.

## Provenance of the numbers and quotes

- `forms int=44 float=5 str=8 custom=13`, `labels agreement=62 agreement*=8 mismatch=0
  config-only=0 live-default=0`: re-derived by me (gate 9). The **binding** own-work receipt is
  ExecLiveCensus's `w1/ExecLiveCensus/census-receipt.txt` (sha256 `6c0d38e6…`, lines 14-15, LF
  only, agreed byte-identically by that seat); it still carries the literal placeholder
  `tool sha256 <TOOLSHA>`, must gain the real `tools/mado-options.py` sha256 at the landing
  revision, and must be copied under `.ufo/waves/round-40/fetch/` — L1's act, not mine.
- Source quotes (each verified once, gate 11/12):
  `config-manager-efb5099.bin` sha256 `9db68cf4…` 90963 B (= held S162's anchor sha256),
  `hyprlang-config-v0.6.8.bin` sha256 `fa1b6898…` 43049 B (= held S173's anchor sha256),
  `complex-data-types-efb5099.bin` sha256 `95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807`
  6116 B (HTTP 200, `EFFECTIVE_URL` …/efb5099378…/src/config/shared/complex/ComplexDataTypes.hpp).
  All three are **working-tree** bytes: `git ls-tree 5e7e885 .ufo/waves/round-40/fetch/` is empty,
  so nothing there is a receipt until L1 commits it.
- Executor quote files read and used: `w1/ExecFetchConfigMgr/quotes.md`,
  `w1/ExecFetchHyprlang/quotes.md`, `w1/ExecFetchComplexTypes/quotes.md`.

## Findings for L1

1. **S162 anchor-range gap (append-only erratum).** The held row's anchor cell lists
   `:419-451,590-623,893-968,2016-2093`; `configHandleGradientSet` is `:103-160` (destroy
   `:162-165`) and is registered as the `gradient` custom type at `:510` and `:2178` — same pinned
   blob (`9db68cf4…`), outside the listed ranges. My first draft said `:103-170`; ExecFetchConfigMgr
   corrected it (line 168 starts `configHandleGapSet`), and the entry now says `:103-160`.
2. **Gate-quote hazard the entry now documents.** `quality/counters/c2-r40-forms-entry.py` `norm()`
   deletes `<…>` spans; in `ComplexDataTypes.hpp` the `<` at `:62` closes at the `>` of `sc<int>` on
   `:75`, so `norm(blob)` loses `:62-75` — including the `{:x}` colour print (`:72`) and the `{}deg`
   angle print (`:75`). Measured: `norm("{:x} quote") in norm(blob)` is `False`. My first draft used
   that line as the S_FORMS_1 slot; it is now prose and the Gate quote is the gate-safe gap
   `toString` (`:134`, 9 words; signature `:133`). The same trap is why the S162 colour-clear quote is the 6-word
   two-line span (`CVarList2  varlist(…); DATA->m_colors.clear();`) rather than the 1-word
   `DATA->m_colors.clear();` (below the 3-word floor).
3. **Placeholders.** `S_FORMS_1` (new: `ComplexDataTypes.hpp` @ `efb5099`) and `S_FORMS_2` (new:
   own-work census receipt) must be renamed in the entry, the registry rows and the Gate lines
   together (clause b needs four distinct `source: S###` lines).
4. **Registry location-token hazard (clause e).** S180 already registers the same
   ComplexDataTypes URL with the same sha256 (`95733223…`, 6116 B) and its `cells[1]` ends with the
   bare URL. A new row whose location cell ends with that bare URL fails clause e (`same == [i]`);
   the new row needs a unique last token (e.g. `…/ComplexDataTypes.hpp:75`). Reported by
   ExecFetchComplexTypes, not acted on here.
5. **Slots.** Six slots carry a verified candidate that L1 can fill as-is (S162 ×2, S173,
   S_FORMS_1, the `forms` line, the `labels` line, `no such option`); the rest carry a fill hint
   naming the receipt line to quote (font_family probe, the four worked keys, the two census reply
   lines, the tree-read declarations, the re-derivation block, the `variant-noinherit` line). A hint
   left unfilled leaves that OBS line without a Gate quote — fill from the executors' `quotes.md` or
   drop the slot. Clause d/g are already satisfied by the pre-filled lines.
6. **Numeric font-weight quirk (kept as UNK, wording corrected by ExecFetchComplexTypes).**
   `parseWeight` assigns only on a table hit (`:169`) or an out-of-range integer (`:173`): an
   in-range numeric weight absent from the table is parsed into `w_i` and discarded, so `m_value`
   keeps whatever it held **before** the call — 400 only while untouched since the default at
   `:148` (e.g. a numeric 550 after a prior `bold` read stays 700). The host declares only names,
   so the branch is unexercised; the entry states this without claiming a host outcome.

## Out of scope / not done

- No `quality/` counter was run (both need a committed revision); no C1 tool path was exercised.
- No registry row, lesson Gate line, README index row or final id was written.
- No socket connect; compositor verbs used were only `hyprctl version` and `hyprctl getoption -j`.
- No tool installed or updated (python3 stdlib only was needed).

## Artifact paths

- `mado-shokunin/.ufo/waves/round-40/w1/ScrFormsEntryA/entry.md` (Draft A, 134 lines)
- `mado-shokunin/.ufo/waves/round-40/w1/ScrFormsEntryA/rederive-census.py`
- `mado-shokunin/.ufo/waves/round-40/w1/ScrFormsEntryA.md` (this report)
