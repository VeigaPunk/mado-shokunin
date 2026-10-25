# ScoutHeldCoverage — held-coverage map of the C2 ground (mado round 40, hyaku run 7)

Scope: read-only sweep of the lane corpus (`corpus/knowledge/*.md`, `corpus/SOURCES.md`,
`corpus/lessons/*.md`, `corpus/README.md`) for the C2 terms: `getoption`, `custom`, `"set"`,
`gradient`, `deg`, `no such option`, `agreement*`, `config-option-table-r39`.
Purpose: tell the C2 author exactly which lines are already held, so
`corpus/knowledge/hyprctl-getoption-native-forms-r40.md` adds new ground only.

Lane repo: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Freeze `5e7e885`, base `9fc511d`.
HEAD at sweep time `e2b51d3`. Nothing outside this seat directory was written.

---

## 1. What is ALREADY HELD (do not re-derive; cite instead)

### 1.1 The divergence-class vocabulary and the 56 live pairs — HELD

`corpus/knowledge/hyprctl-verification-layer.md` (MADO-R2-1) is the parent of C2's ground.

| Held line | Content | C2 consequence |
|---|---|---|
| `:44-51` | the class table: `agreement`, `agreement*`, `live-default`, `mismatch`, `config-only` | C2's label vocabulary is **held**; the entry must cite this note, not re-define the five classes |
| `:52-55` | "`set` flag as discriminator `[OBS]`: `set=false` on exactly the four options no file declares … `[INF]` its exact semantics … inferred from that correlation, not from documentation" | the `set` field's **meaning** is a carried `[INF]`, not an open field |
| `:67-70` | "## 3. Mapping table — 56 `getoption` claim→live pairs"; "`-j` renders `custom`-type options under a `custom` key, not `str`" | the **first** statement that `custom` is a JSON key distinct from `str` is held at `:69-70` |
| `:76-131` | the 56 rows with live values in native form: `` `custom: 0 0 0 0` ``, `` `int: 0` ``, `` `str: dwindle` ``, `` `custom: ffe68e0d 45deg` ``, `` `custom: aa595959 0deg` ``, `` `custom: ee1a1a1a 0deg` `` | **every native-form value C2 will re-cite for these 56 keys is already tabulated** (values + `set` + class) |
| `:143-146` | class census over the 56: "52 `agreement` (6 of them `agreement*`) … 4 `live-default`, **0 `mismatch`**" | a **held census at a different denominator** (56 pairs, 2026-10-14) |
| `:171-176` | §5 ownership table, incl. `general:col.active_border` and `group:col.border_active` → live `ffe68e0d 45deg` | the **same two keys and the same live value** C2's angle-inheritance rule explains |
| `:249-251` | UNK #1: "`set` field semantics: inferred from correlation … attribution precision is limited" | carried UNK |
| `:254-256` | UNK #2: "why the angle `45deg` survives a single-color assignment is **unverified**" | **this is the UNK C2's angle-inheritance rule answers** |
| `:272-273` | §11 spot-check: `hyprctl getoption general:gaps_in` → `custom type: 0 0 0 0` + `set: true` | held human-form sample |

### 1.2 The 57-row re-measure and the `kind` column — HELD

`corpus/knowledge/config-health-report-r3.md` (MADO-R3-2):

- `:48-51` — "57/57 `getoption` rows re-measured byte-identical … (46 `agreement` + 6 `agreement*` + 4 `live-default` …)"; `:71`, `:83`, `:137-143` — census at denominator 57.
- `:488-560` — **Appendix A**, the 57-row live table (Option | Live | set | class).
- `:776-807` — the reproduction TSV in exactly the `option|kind|value|set|class` shape, with the **kind column already enumerating `custom` / `int` / `float` / `str`** per key (e.g. `:781` `general:col.active_border|custom|ffe68e0d 45deg|true|agreement*`, `:779` `general:gaps_out|custom|0 0 0 0|true|agreement*`, `:778-780`).
- `:447-448` — carried UNK list item 5: "`col.active_border` `45deg` survival after single-color assignment (U2, carried)".

⇒ The **per-key native form for 57 of the 70 keys is already tabulated, twice** (Appendix A + TSV).
C2's new content is the *rule* that produces those forms, the *native-forms ground* as a
compositor-facing surface, and the **70-key census at a new denominator** — not the values.

**Vocabulary collision to resolve in the entry (not a held-ground issue, but it touches held
definitions).** `config-only` already has two held definitions, and the round-40 native model
gives it a third: `hyprctl-verification-layer.md:50` — "`config-only` | declared, but hyprctl has no
read surface for it (or another daemon consumes it) → static evidence only, live layer UNKNOWN";
`config-option-table-r39.md:94` — "`config-only` (declared, not in the dump)"; and the C1/C2
registration's model — `no such option` from the compositor ⇒ `config-only`. Same for
`live-default` (`verification-layer.md:48`, `r39:94-95`): in the native model it is reserved for a
`--probe` key with no declarer, so over the 70 declared keys it is **0**, and `config-only` is also
**0** (all 70 declared keys are answered — the capture has 70 JSON rows and no `no such option`
line). C2 should say explicitly that it is using the five held labels in the native-model sense,
or the entry will read as contradicting `verification-layer.md:46-51`.

### 1.3 The r39 sibling entry and its own open UNK — HELD, and it is C2's pretext

`corpus/knowledge/config-option-table-r39.md` (MADO-R39-1):

- `:9`, `:21-24` — cites the 56 live pairs + five divergence classes as **held, cited not restated**.
- `:39-49` — S162 (handler registration `:601-623`) and S173 (`configSetValueSafe` `:832`, handler fallback `:839`) are already quoted here.
- `:52` — S219 own-work quote: "rows=70 owner files=6 layers defaults=57 user=7 toggles=4 theme=2" ⇒ **the number 70 and the owner-file split are HELD** (static side).
- `:89-98` — §4: the merge/label rules including "Comparison normalises numbers for int/float types, boolean spellings, and a scalar against a repeated tuple (`0` vs `0 0 0 0`); anything else is exact string equality" ⇒ **the label algorithm is HELD**.
- `:100-110` — "Falsifiable consequence … a live `getoption` after the same change on the host would then label those rows `agreement` … **the live half is open**".
- `:114-115` — "**[UNK]** No live `getoption` dump was taken this round (no socket was connected); §4 is verified on generated inputs and the selftest, not against the running compositor."

⇒ C2 is the **first live `getoption` dump in the lane** and closes r39's explicit live half.

### 1.4 `no such option` — HELD as two isolated observations, semantics NOT held

- `corpus/knowledge/executor-test-sufficiency.md:167-168` — "`group:groupbar:gaps_out` → `{"int":0,"set":true}`; `general:group:groupbar:gaps_out` → `no such option`".
- `corpus/knowledge/idle-lock-plane.md:218-220` — "`hyprctl getoption` on a deliberately bogus path (`misc:bogus_xyz_notreal`) returns `no such option`, so non-error responses below are real options."

Held: the **string** appears in two notes. **Not held anywhere in the corpus**: that it is the
compositor's own reply, that it exits 0, and that it is the signal for the `config-only` label.
(Measured now, read-only, `hyprctl getoption -j general:group:groupbar:gaps_out` → `no such option`,
rc=0; same for `misc:bogus_xyz_notreal`.) C2's `no such option` clause is **new ground**.

### 1.5 The native JSON envelope — HELD once, in one note

- `corpus/knowledge/event-queue-observability-r37.md:38` — "`debug:disable_logs: {"option":"debug:disable_logs","int":1,"set":false}`" (own-work receipt S213, GATE quote in `corpus/lessons/round-37.md:32`).
- `corpus/knowledge/executor-test-sufficiency.md:166-167` — `{"custom":"0 0 0 0","set":true}`, `{"int":0,"set":true}`.

⇒ The **`{"option":K,"set":B,"<form>":V}`** envelope has been seen in the corpus **twice, both times
as an incidental example inside another claim**. No corpus note states it as a *surface contract*.

### 1.6 The four other native-form renderings — HELD piecemeal

- `corpus/knowledge/keybind-rule-semantics.md:282-284` and `:313-314` — `float: 0.400000`, `int: 1` (`set: true`), `float: 2.000000` (`set: false`).
- `corpus/knowledge/window-rule-effects-getprop.md:16`, `:54-59` — `float: 1.000000`, `set: false`.
- `corpus/knowledge/hyprland-config-plane.md:126`, `:130-138`, `:214` — `int: 1`; `custom type: 0 0 0 0`.
- `corpus/knowledge/config-drift-r12.md:76-77`, `:114`, `:142` — `custom type: 0 0 0 0`, `str: br`.
- Summary repeats: `corpus/knowledge/arc-synthesis.md:227`, `:355`; `corpus/knowledge/closeout-r11.md:41`.

### 1.7 SOURCES.md registry rows the C2 entry will touch — HELD state

| id | row | held anchor / scope | does the anchor cover C2's needs? |
|---|---|---|---|
| **S162** | `corpus/SOURCES.md:174` | `src/config/legacy/ConfigManager.cpp:419-451,590-623,893-968,2016-2093`; scope "legacy windowrule keyword handlers, named special-category reconstruction, and reload traversal" | **NO** — the gradient handler lives at `:103-170` of the same file; **not** in S162's anchored ranges |
| **S173** | `corpus/SOURCES.md:185` | hyprlang `src/config.cpp:619-667,755-827,983-986`; scope "RHS `{{…}}` expression parsing" | **NO** — `configStringToInt` is at `:185-264` of that file; **not** anchored |
| **S180** | `corpus/SOURCES.md:192` | `src/config/shared/complex/ComplexDataTypes.hpp:80-120` (CCssGapData only) | **NO** — `CGradientValueData::toString` `:69-77` and `CFontWeightConfigValueData` `:138-175` are **not** anchored |
| **S158** | `corpus/SOURCES.md:170` | `src/debug/HyprCtl.cpp:346-484, 613-630, 647-723, 1463-1645, 2003-2044` | **NO** — `dispatchGetOption` is `:1647-1731`; only the registration line `:2039` is inside |
| S215 | `:193` | `ConfigValues.cpp:629,:632` (the two log switches) | unrelated |
| S219 | `:225` | own-work, round-39 tool receipt over the host tree (70 rows) | the static-ownership ground; **not** a live-forms row |

⇒ **The compositor-side source for the native forms is unheld ground**: no registry row anchors
`HyprCtl.cpp:1647-1731` (the form-key dispatch and `return "no such option";` at `:1670`), none
anchors the gradient handler `ConfigManager.cpp:103-170`, none anchors
`configStringToInt` `config.cpp:185-264`, none anchors `ComplexDataTypes.hpp:69-77 / 138-175`.
The round-24 blob `.ufo/waves/round-24/fetch/S158.bin` (sha256 `798b7c6c…`, committed) contains
`dispatchGetOption` at `:1647-1731`, and `corpus/lessons/round-37.md:114` already cites
"HyprCtl.cpp `:2039` registers `getoption`" — the *registration* is held; the *dispatch* is not.

### 1.8 The corpus holds NO instance of these C2 subjects (grep-verified, 0 hits)

`configStringToInt` (0 hits corpus-wide) · `ARGB`/`argb` (0) · `unpadded` (0) · `no such option`
only the two lines of §1.4 · `native form` (0) · `int|float|str|custom` as a *form set* (0 — each
type appears only inside per-key tables) · `font_weight` / `font weight` (0; only terminal fonts in
`terminals-and-omarchy.md:34,45`) · `group:groupbar:col` (0) · `hyprctl descriptions` (0) ·
`toString` as a compositor concept (0 in knowledge; `rule-attribution-r24.md:45` is a different
`toString`) · `inherits`/angle-inheritance as a rule (0).

---

## 2. What C2 can therefore claim as NEW GROUND (and only this)

1. **The native-forms surface as a contract** — one JSON object per key, `{"option":K,"set":B,"<form>":V}`,
   forms `int|float|str|custom` for the 70 declared keys, plus the plain-text `no such option`
   reply with rc 0 ⇒ `config-only`. Held: two incidental examples (§1.5) and the `custom`-vs-`str`
   sentence (§1.1 `:69-70`). New: the contract, the `no such option` semantics, the form set.
2. **The host census over all 70 declared keys** — the first live dump in the lane (r39 `:114-115`
   says none was taken). Held: censuses at denominators **56** (verification-layer `:143-146`) and
   **57** (health-report `:48-51`, `:140-143`); and the *static* 70-row count (r39 `:52`).
   New: a **70-key live census**, whose numbers must be stated as a new denominator, not as a
   correction of 56/57 (the mado rule is append-only; the three denominators coexist).
3. **The conversion model** — hyprlang `configStringToInt` (fetched blob
   `.ufo/waves/round-40/fetch/hyprlang-config-v0.6.8.bin:185-274` — the function body measured
   ends at `:274`, not `:264` as the C1 counter docstring says: `0x` hex at `:197-206`, `rgba()`
   at `:198-231` (comma form → ARGB at `:216`, 8-hex form RGBA→ARGB at `:222-229`), `rgb()` at
   `:232-254` (comma form at `:239`, 6-hex form +`0xFF000000` at `:249-252`), `true/on/yes`→1 at
   `:258`, `false/off/no`→0 at `:261-262`, decimal at `:265-273`) and the compositor's own
   gradient/gap/font-weight renderings (`ComplexDataTypes.hpp:69-77` gradient `toString` =
   `<hex> … <N>deg`, the `{:x}` hex per colour at `:72` and the `{}deg` suffix at `:75`;
   `:80-136` `CCssGapData` 1→4 expansion at `:95-119` + `toString` at `:133-136`;
   `:138-161` font-weight name→number map `WEIGHTS` at `:158-160` + `toString` at `:154-156`).
   Zero held coverage (§1.8). Held and must be cited instead: the *label* algorithm
   (r39 `:91-97`) and the *values* (verification-layer §3, health-report Appendix A).
4. **The angle-inheritance rule** — a gradient redeclared without a `deg` token keeps the previous
   declarer's angle (`ConfigManager.cpp` `configHandleGradientSet` at `:103`, ends `:161`:
   `DATA->m_colors.clear()` at `:112`, angle set only when a `deg` token is present at `:117-120`;
   `toString` appends `{}deg` at `ComplexDataTypes.hpp:75`).
   This **closes two carried UNKs**: `hyprctl-verification-layer.md:254-256` and
   `config-health-report-r3.md:447-448`. Host instance: theme `col.active_border = $activeBorderColor`
   (`~/.config/omarchy/current/theme/hyprland.conf:1,4` = `rgb(e68e0d)`) over the defaults-tree
   gradient (`~/.local/share/omarchy/default/hypr/looknfeel.conf:4,15` = `rgba(33ccffee) rgba(00ff99ee) 45deg`)
   ⇒ live `ffe68e0d 45deg`. **The rule is new; the observation is held** (verification-layer `:79`,
   `:102`, `:175-176`; health-report `:498`, `:521`, `:781`, `:804`).
5. **The host census that the rule explains** — `general:col.active_border` and
   `group:col.border_active` read `ffe68e0d 45deg` with `set: true` (both re-measured read-only
   this sweep and present in the capture, `.ufo/waves/round-40/c1/native-capture.jsonl:21,27`).
   The split **62 `agreement` / 8 `agreement*` / 0 `mismatch`** over the 70 keys is the
   registration's stated reference-model result (`registration.md`, C2 bullet) — the C2 seat must
   re-derive it from its own tool, not recite it. Held: the 56- and 57-key censuses; the *first*
   70-key ownership-vs-live agreement statement would be C2's.
6. **Own-work census receipt bound to the committed tool sha256** — a new own-work row.

### 2.1 One nuance C2 must get right (not held anywhere, easy to get wrong)

The compositor's dispatch emits **nine** JSON keys in source (`HyprCtl.cpp:1702-1727`): `int`,
`bool`, `float`, `vec2`, `str`, `custom`, `css`, `gradient`, `font_weight`. The **host answered
only `int`, `float`, `str`, `custom`** for the 70 declared keys — even for gap, gradient and
font-weight options, which live in the host tree as hyprlang custom types and therefore answer
`custom` (`general:gaps_in` → `"custom":"0 0 0 0"`; `general:col.active_border` →
`"custom":"ffe68e0d 45deg"`; `group:groupbar:font_weight_active` → `"custom":"1000"`).
The source-level `css` / `gradient` / `font_weight` keys are the *legacy config-value* renderings
(`HyprCtl.cpp:1723/1725/1727`) and are not what this host's `.conf` tree produces — **[INF]** from
the dispatch's `std::type_index` dispatch plus the observation that the three host keys of those
shapes answer `custom`; the corpus holds nothing on this, so C2 should say which forms it
*observed* and which source branches *exist*, rather than implying the source emits four keys.

---

## 3. Constraints the frozen C2 counter imposes on the entry (read from `quality/counters/c2-r40-forms-entry.py`)

These are not negotiable; they decide what "held vs new" can even be expressed.

- **Clause b** — the first 20 lines must carry `verified-at: 2026-10-25` and a `recheck:` matching
  `^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)(\s|$)`; and **≥4 distinct S-ids**, counted **one per
  `source:` line** (`SRC_RE` is anchored at line start and matches only the first id of a line —
  `head` = first 20 lines). ⇒ use **four separate `source: Sxxx …` lines** (as the control fixture
  does), not one comma-separated line.
- **Clause c** — every id in the header must have **exactly one** registry row with **11 cells**;
  `status` = `mined`; `used-by` must contain the new entry path; **≥2 ids new** (not in the base
  registry) with `opened` = `2026-10-25`.
  For **held** ids (S162, S173) the counter enforces `old[:10] == new[:10]` ⇒ **only `used-by`
  (cell 11) may change**; scope / anchor / teaches / status / opened / recheck of S162 and S173 must
  be byte-identical to base. Re-opening S162/S173 therefore *cannot* be expressed by rewriting their
  anchors — the gradient-handler and `configStringToInt` lines must live in **new rows**.
- **Clause e** — for each **new** id, the last whitespace token of the *source* cell must be unique
  across the whole registry. S180's source cell ends in the `…/ComplexDataTypes.hpp` URL
  (`corpus/SOURCES.md:192`), so a new ComplexDataTypes row must **not** end its source cell with
  that same token — end it with the round-40 receipt path (e.g.
  `.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin`) or another distinct trailing token.
  (The mado census `scripts/sources-census.sh` would additionally flag the repeated URL: **W04**
  when the scope string differs — exit 0, acceptable; **E04** when the scope string is identical
  to S180's — exit 1, not acceptable. So the new row's *scope* cell must also differ from S180's
  scope "Four-sided gap parsing used by legacy workspace-rule gapsin and gapsout".)
- **Clause d** — each id needs a `GATE <id> receipt=… sha256=… quote="…"` line in the
  `## Gate` section of `corpus/lessons/round-40.md`, with `receipt=` under
  `.ufo/waves/round-40/fetch/`, the sha256 matching the blob **as committed at the data rev**, and a
  quote of **3–25 words** that is present (whitespace-normalised) in that blob.
- **Clause g** — for each id, some line of the entry must contain the id (word-boundary) **and**
  the same quote.
- **Clause h** — exactly **one** new own-work row (kind `own-work`); its receipt must contain the
  **sha256 of the committed `tools/mado-options.py` at that rev** and two lines matching
  `^forms int=(\d+) float=(\d+) str=(\d+) custom=(\d+)$` and
  `^labels agreement=(\d+) agreement\*=(\d+) mismatch=(\d+) config-only=(\d+) live-default=(\d+)$`,
  whose sums are equal, and **both lines must appear verbatim in the entry**.
  ⇒ The forms sum must equal the labels sum: over 70 keys, `int 44 + float 5 + str 8 + custom 13 = 70`
  and labels `agreement 62 + agreement* 8 + mismatch 0 + config-only 0 + live-default 0 = 70`.
  ⇒ The counter reads that receipt as the **GATE-bound blob for the own-work id**
  (`receipts[own[0]]`), so the census receipt must be the *same* file named in the id's
  `GATE … receipt=` line — i.e. it lives under `.ufo/waves/round-40/fetch/`, is committed with the
  data, and its sha256 is the one printed in the gate line. The two count lines must also be
  quoted **verbatim** in the entry body.
- **Clause f** — exactly one `corpus/README.md` row matching ``^| `knowledge/hyprctl-getoption-native-forms-r40.md` ``.
  `quality/check-index.py` also requires every note in `corpus/knowledge/` to have exactly one
  index row ⇒ the note adds a 57th index row (baseline 56/56).

### 3.1 Two sequencing hazards visible from the freeze

- `.ufo/waves/round-40/fetch/` is **currently untracked** (`git status` → `?? .ufo/waves/round-40/fetch/`).
  Clause d reads receipts with `git show <rev>:<path>`, so those blobs must be **committed** with the
  data, otherwise every gate binding is `None` and clause d fails for all ids.
- Clause h binds the receipt to the **sha256 of the committed tool**. The tool is C1's deliverable,
  so the own-work receipt must be produced **after** C1's tool lands (sha of the committed bytes),
  not from a work-tree copy.

### 3.2 Re-open evidence already on disk (byte-identical to the held rows)

| blob | sha256 | identical to |
|---|---|---|
| `.ufo/waves/round-40/fetch/config-manager-efb5099.bin` | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | S162's anchored sha (`corpus/SOURCES.md:174`) — byte-identical re-open |
| `.ufo/waves/round-40/fetch/hyprlang-config-v0.6.8.bin` | `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e` | S173's anchored sha (`corpus/SOURCES.md:185`) — byte-identical re-open |
| `.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin` | `95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807` | S180's anchored sha (`corpus/SOURCES.md:192`) — byte-identical re-open |
| `.ufo/waves/round-40/fetch/hyprctl-efb5099.bin` | `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` | S158's anchored sha (`corpus/SOURCES.md:170`) — byte-identical re-open, and the file that contains `dispatchGetOption` `:1647-1731` |

---

## 4. Overlap ledger — the exact lines C2 must cite rather than restate

```
HELD (cite, do not restate)
  knowledge/hyprctl-verification-layer.md:44-51    five divergence classes
  knowledge/hyprctl-verification-layer.md:52-55    set as discriminator ([INF] semantics)
  knowledge/hyprctl-verification-layer.md:67-70    56 pairs; -j renders custom under "custom", not "str"
  knowledge/hyprctl-verification-layer.md:76-131   per-key native values + set + class
  knowledge/hyprctl-verification-layer.md:143-146  census @56 (52 agreement / 6 agreement* / 4 live-default / 0 mismatch)
  knowledge/hyprctl-verification-layer.md:171-176  §5 ownership incl. both 45deg border keys
  knowledge/hyprctl-verification-layer.md:249-251  UNK set semantics
  knowledge/hyprctl-verification-layer.md:254-256  UNK 45deg survival  <- C2 closes this
  knowledge/hyprctl-verification-layer.md:272-273  gaps_in spot-check
  knowledge/config-health-report-r3.md:48-51       census @57 (46 / 6 / 4)
  knowledge/config-health-report-r3.md:137-143     census @57 restated
  knowledge/config-health-report-r3.md:447-448     UNK 45deg survival (carried)  <- C2 closes this
  knowledge/config-health-report-r3.md:488-560     Appendix A, 57 rows (Option|Live|set|class)
  knowledge/config-health-report-r3.md:776-807     TSV option|kind|value|set|class (kind column enumerated)
  knowledge/config-option-table-r39.md:9,21-24    cites the 56 pairs + classes as held
  knowledge/config-option-table-r39.md:39-49       S162/S173 quotes already in the corpus
  knowledge/config-option-table-r39.md:52          static 70 rows / 6 owner files (S219)
  knowledge/config-option-table-r39.md:89-98       merge + label + comparison rules
  knowledge/config-option-table-r39.md:100-110     falsifiable consequence; "live half is open"
  knowledge/config-option-table-r39.md:114-115     UNK: no live dump was taken  <- C2 is that dump
  knowledge/executor-test-sufficiency.md:37,51,96,166-167   {"custom":…},{"int":…} envelope, no such option
  knowledge/executor-test-sufficiency.md:133-137   no-arg getoption does not enumerate
  knowledge/executor-test-sufficiency.md:167-168   no such option (2nd key)
  knowledge/idle-lock-plane.md:218-220            no such option on a bogus path
  knowledge/event-queue-observability-r37.md:38    native envelope once ({"option":…,"int":1,"set":false})
  knowledge/keybind-rule-semantics.md:282-284,313-314   float/int renderings
  knowledge/window-rule-effects-getprop.md:16,54-59      float + set:false
  knowledge/hyprland-config-plane.md:126,130-138,214      int / custom type renderings
  knowledge/config-drift-r12.md:76-77,114,142            custom type / str / set
  knowledge/arc-synthesis.md:227,355 ; knowledge/closeout-r11.md:41   summary repeats
  SOURCES.md:170 S158 | :174 S162 | :185 S173 | :192 S180 | :193 S215 | :225 S219   registry rows
  lessons/round-37.md:32 (GATE S213) ; lessons/round-37.md:114 (HyprCtl.cpp :2039 registers getoption)
  lessons/round-39.md:80-82 (considerthese proposal 4 -> C2/C3 of round 39)

NEW (C2's own ground)
  the native-forms contract (4 forms + envelope) as a surface, incl. no-such-option semantics
  the live 70-key census (first live dump in the lane) at a NEW denominator
  configStringToInt conversion (0 held hits) ; ComplexDataTypes toString forms (0 held hits)
  the angle-inheritance rule and its two closed UNKs
  the own-work census receipt bound to the committed tool sha256
  the nine source form-keys vs the four observed host forms (see §2.1)
```

---

## 5. Commands run (read-only; no write outside this seat directory)

- `read`/`grep` over `corpus/knowledge/*.md`, `corpus/SOURCES.md`, `corpus/lessons/*.md`, `corpus/README.md`, `corpus/QUALITY.md`.
- `git -C <lane> rev-parse HEAD`, `git log --oneline -3`, `git ls-tree -r --name-only HEAD -- .ufo/waves/round-40/`, `git status --porcelain -- .ufo/waves/round-40/fetch/` (read-only; no mutating git anywhere).
- `sha256sum` on the round-40 and round-24 fetch blobs; byte comparison against the SOURCES anchors.
- `python3 -I tools/mado-options.py --home $HOME` (static table only, no `--live`): 70 rows, key set
  identical to the 70 keys of `.ufo/waves/round-40/c1/native-capture.jsonl` (0 extra, 0 missing).
- `hyprctl getoption -j general:group:groupbar:gaps_out`, `hyprctl getoption misc:bogus_xyz_notreal`
  → `no such option`, rc 0; `hyprctl getoption -j input:touchpad:scroll_factor` →
  `{"option": …, "float": 0.400000, "set": true }`. Read-only verb only.
- Tooling: none installed, none needed; no pacman, no package transaction.

## 6. Remaining unknowns for the C2 author (not resolvable from the corpus)

1. Whether the 8 `agreement*` keys are the 8 shadowed-by-theme/toggle pairs or a different set — the
   lane holds no 70-key ownership-vs-live cross table (r39 §3 has the static side only).
2. Whether the compositor ever answers `bool` / `vec2` for any *declared* key on this host (the 70
   captured replies contain none); only the source branches can say the keys exist.
3. The tool's final sha256 (C1 deliverable) — clause h cannot be satisfied until it lands.
