# Attack24 — C2 claim/source map completeness (W2 attack)

- Seat: `Attack24`, revenger (W2 attack #24). Target: **C2 claim/source map completeness**.
- Lane: mado-shokunin. Round 52, base `85d57a818c3707397e21c840b6498b105ba798aa`.
- Read first: `.ufo/waves/round-52/claims-frozen.md`, `registration.md`, `w2-spec.json` (item 24),
  `w1-results.json`, `w1/C2SourceRecon.md`, `w1/C2PinAudit/pin-proposition-audit.md`,
  `w1/C2EntryDraft/{entry-draft.md,proposition-map.tsv}`, `w1/C2CounterDraft/` (965-line draft),
  `validate/corpus/{README.md,SOURCES.md,knowledge/*,lessons/round-52.md}`,
  the lane working tree's `corpus/` and `quality/counters/c2-r52-proposition-entry.py`,
  and the four pinned bytes under `.ufo/waves/round-52/fetch/`.
- Boundary: no tracked edits, no fleet/sibling/source-repo writes, no git/jj mutation of the lane,
  no package queries, no live reads, no probes/screenshots, no host mutation, no subagents.
  All fixtures were throwaway git repos under `/fast/scratch/hyaku/mado-r52/Attack24/` with
  `git -C <fixture> rev-parse --show-toplevel` asserted equal to the fixture path (see A24-R2/R3).
  Scratch removed after this report; every step below is re-runnable from the lane bytes.
- Non-author boundary: I do **not** judge semantic entailment (that is the separate outside
  reviewer's seat) and I do not count this report as a vote or as admission.

## Verdict in one line

The **row map is largely complete** (4 fresh rows, 18 propositions, 17/18 quotes locatable), but the
frozen clause *"a new committed counter checks proposition count, row/pin/quote bindings and complete
mapping"* is **not reproduced**: the counter at `quality/counters/c2-r52-proposition-entry.py` is not
committed, cannot parse the landed table, and does not check pins, quotes, distinctness, base
freshness or mapping completeness. The landed source map also has two material facts asserted with
no quote anywhere (P12 rejection, P16 modifier clear) and one quote that cannot be located at its
own pin (P16).

---

## 1. Attacked clauses and outcomes

| # | Attacked clause (frozen C2 / registration) | Repro | Outcome | Verdict |
|---|---|---|---|---|
| A24-01 | "A new **committed** counter" | `git ls-files quality/counters/c2-r52-proposition-entry.py` → empty; `git status --porcelain` → `?? quality/counters/c2-r52-proposition-entry.py`; `git cat-file -e HEAD:<path>` → rc 128 "exists on disk, but not in 'HEAD'" | counter, entry and rows exist only in the working tree; `HEAD` is still the base commit | **FALSIFIED** |
| A24-02 | counter "checks proposition count" | fixture with the entry **as written**; run counter `--entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md` | `props=0 … miss=props verdict=TARGET_MISSED`; `grep -cE '^\| P[0-9]+ \| S[0-9]+ \|'` = 0, `grep -cE '^\| P[0-9]+ \| [^\|]+ \| S[0-9]+ \|'` = 18 — the counter's regex expects `id\|S-row\|claim\|…`; the entry is `id\|claim\|S-row\|…` | **FALSIFIED** (counter cannot count the landed map) |
| A24-03 | counter checks "**quote** bindings" | fixture, table reordered to the counter's grammar, every quote cell replaced with `NOPE-NOT-IN-SOURCE` | `props=18 … failures=0 verdict=TARGET_MET` | **FALSIFIED** |
| A24-04 | counter checks "**pin** bindings" | same fixture, every pin cell replaced with `NoSuchFile.cpp:1` | `props=18 … verdict=TARGET_MET` | **FALSIFIED** |
| A24-05 | counter checks "**complete mapping**" | same fixture, append fresh row `S374` (mined, 2026-10-27, used-by this entry) with no proposition | `verdict=TARGET_MET`; `rows=4` (the counter counts only rows named by propositions) | **FALSIFIED** |
| A24-06 | counter checks "proposition count" as substantive/distinct | same fixture, add `P19` identical to `P04` (same claim, pin, quote, rationale) | `props=19 … verdict=TARGET_MET` | **FALSIFIED** (count = regex matches; no distinctness) |
| A24-07 | counter checks the quote column | same fixture, P01 **support-class** cell set to 26 words, real quote untouched | `miss=quote/rationale:P01 … TARGET_MISSED` — the counter reads the *support-class* column as the "quote" (unpacked `quote` is regex group 6) | **FALSIFIED** (wrong column bound) |
| A24-08 | "each material factual proposition maps to … an exact located quote" — P16 | P16 pin `Hyprland-ConfigActions.cpp:1554-1558,1576`; quote is the `1554` mods call + the `1558` key call. Source: 1554 mods, **1555 blank, 1556-1557 guards**, 1558 key, 1576 clear. Whitespace-collapsed containment of the quote in 1554-1558 = False; the 5-clause draft counter reports `P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)` | quote is non-contiguous and the `1576` half is not in the span | **FALSIFIED** |
| A24-09 | "every material factual proposition is mapped" — P12 rejection and P16 clear | P12 claim: "…a written selector without a result is rejected"; quote stops at the selector ternary (582-583); the guard is 585-586. P16 claim: "…then clears the modifier state"; the clear is 1576. Searched every quote cell in the entry: `'window not found'` → **absent**, `'sendKeyboardMods(0, 0, 0, 0)'` → **absent** | two claim halves have no quote anywhere in the map (both are only "included in this locator" per the rationale text) | **FALSIFIED** |
| A24-10 | each proposition maps to "a pin path/revision" | entry table pin cells are `Hyprland-<file>.cpp:<lines>` only; no `fetch/` path and no revision; revision appears once in the footer, rows carry it in `SOURCES.md` | binding exists only transitively (footer + row anchor), not per proposition | **NOT REPRODUCED** (low severity; a reader cannot resolve one row standalone) |
| A24-11 | "new **indexed** … entry" | `corpus/README.md:79` is blank, `:80` is the r52 index row, `:82` is `## Quality bar` — the row sits **outside** the coverage table; both counters' index tests are substring matches (`'knowledge/<name>' in README`) and pass | indexed=1 in every run | **PARTIAL** (index is decorative, not a table row) |
| A24-12 | "an independent non-author samples actual source truth" | — | outside this seat's province; not claimed here | **NOT JUDGED** |

## 2. What the evidence does support (reproduced, not falsified)

- **Fresh rows.** Base registry at `85d57a81:corpus/SOURCES.md` has 306 row lines and no `S370-S373`;
  the working tree has 310 and exactly `S370,S371,S372,S373` are new (set difference run, no other
  added/removed ids). All four rows are `mined`, `opened 2026-10-27`, carry a 40-hex revision and a
  `used-by` naming `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`.
- **Row coverage of every pin.** `S370:531-627` covers P01-P12, P15, P17, P18; `S371:1530-1616`
  covers P13 and P16; `S372:114-117` covers P14; `S373:221-242` covers P07. No proposition's anchor
  falls outside its row's anchor cell.
- **Quote length.** All 18 quotes are ≤19 words (`quote-audit.py`; max P03 = 19).
- **Quote location, 17/18.** Whitespace-collapsed containment holds for every row except P16; the
  5-clause draft counter agrees (`quotes_bound=17/18`, `quotes_raw=6/17`).
- **Pin identity.** The four staged files' sha256 match `fetch/SHA256SUMS`
  (`7248cbb8…fbe771`, `a83abeb5…a7637`, `746c6f51…b7073`, `8d8f35fc…d4e40`), which equal the
  round-51 pin digests; the round's "opening" is a re-open of identical bytes.
- **No-work control at base.** `python3 quality/counters/c2-r52-proposition-entry.py --repo . \
  --rev 85d57a81… --work <scratch>` → `entry=absent verdict=TARGET_MISSED` rc=1. It misses for the
  right reason (entry absent), but not because any counter check compares row sets against base.

## 3. Findings, detail and exact reproduction

### A24-01 — the "new committed counter" is an untracked working-tree file (severity: high)

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin
$ git rev-parse HEAD
85d57a818c3707397e21c840b6498b105ba798aa
$ git status --porcelain
 M corpus/README.md
 M corpus/SOURCES.md
 M quality/tool-ledger.md
?? .ufo/waves/round-52/
?? corpus/knowledge/hyprland-synthetic-dispatch-r52.md
?? corpus/lessons/round-52.md
?? quality/counters/c1-r52-ledger.py
?? quality/counters/c2-r52-proposition-entry.py
$ git cat-file -e HEAD:quality/counters/c2-r52-proposition-entry.py
fatal: path 'quality/counters/c2-r52-proposition-entry.py' exists on disk, but not in 'HEAD'   (rc 128)
```

The counter listed in `quality/tool-ledger.md:122` is 47 lines / 2,584 B, mtime `11:11:56`, and the
entry is `11:13:49`; `HEAD` still equals the frozen base. The claim's "committed" clause is not met at
the observed state. This is a *time-stamped mid-integration* finding, not a prediction.

### A24-02 — the shipped counter's table grammar contradicts the entry's own table (severity: high)

Shipped counter, `quality/counters/c2-r52-proposition-entry.py:28`:

```
props=re.findall(r'^\|\s*(P\d+)\s*\|\s*(S\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*$',body,re.M)
```

That is `id | S-row | claim | pin | anchor | quote | rationale`. The entry
(`corpus/knowledge/hyprland-synthetic-dispatch-r52.md:12-29`) is
`id | Proposition | Source row | Pin:anchor | Quote | Support class | Why it supports` with the
header row declaring exactly those names. On the unmodified entry the regex matches **0** rows,
so the counter prints `props=0 … TARGET_MISSED`. The counter therefore cannot score the map it was
written for; a TARGET_MET requires rewriting the entry's column order (which I did only in a
throwaway fixture to test the counter body).

### A24-03 … A24-07 — the shipped counter implements none of the claimed bindings (severity: high)

Fixture (throwaway git repo, `git rev-parse --show-toplevel` asserted):

1. copy the lane's `corpus/` + `.ufo/waves/round-52/fetch/`, commit;
2. run the counter → as-written: `props=0 verdict=TARGET_MISSED`;
3. reorder only the seven table columns to `id|S|claim|pin|quote|support|why` → `props=18 rows=4
   indexed=1 failures=0 verdict=TARGET_MET`;
4. mutate and re-run:

```
[m1 all 18 quote cells := NOPE-NOT-IN-SOURCE]  props=18 rows=4 failures=0  TARGET_MET  (rc 0)
[m2 all 18 pin cells  := NoSuchFile.cpp:1]     props=18 rows=4 failures=0  TARGET_MET  (rc 0)
[m3 fresh unmapped registry row S374 appended] props=18 rows=4 failures=0  TARGET_MET  (rc 0)
[m4 duplicate proposition P19 == P04]          props=19 rows=4 failures=0  TARGET_MET  (rc 0)
[m5 P01 support-class cell := 26 words]        props=19 … miss=quote/rationale:P01  TARGET_MISSED
[control: S370 access date 2026-10-19]          failures=14 miss=rowmeta:S370        TARGET_MISSED
[control: only 3 propositions]                  props=3  miss=props                  TARGET_MISSED
```

Cause, by read: the loop unpacks `pid,sid,claim,pin,anchor,quote,rationale` from the seven groups;
group 6 (the support-class cell, `direct`) lands in `quote`, and `len(quote.split())>25` is the only
quote test. `pin`/`anchor` are never used. `rows` is only the registry text matched by
`^\|\s*(S\d{3,})\s*\|…$`; its checks are `mined`, the date string, `a.entry in row` and any 40-hex
substring. There is no source file read at all, no per-proposition row binding, no distinctness
test, and no unmapped-row test. The docstring (`:4`) claims "pin revision/quote binding and map
completeness" — the body does not implement either.

Additional: `--base` is parsed at `:19` and **never referenced** afterwards. Running the same fixture
with `--base 0000000000000000000000000000000000000000` still returns `TARGET_MET`, so "opened this
round" is only a date-string check, not a base-registry comparison.

Default target slug: `--entry` defaults to `corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md`
(the W1 draft name), while the landed file is `hyprland-synthetic-dispatch-r52.md`. Default run on
the fixture with the entry present → `entry=absent verdict=TARGET_MISSED`; the same run with
`--entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md` → `TARGET_MET`. The counter's default
target and the entry/rows (`used-by`) disagree by the `-key-` token.

### A24-08 — P16's quote cannot be located at its own pin (severity: high)

`corpus/knowledge/hyprland-synthetic-dispatch-r52.md:28`:

- claim: "The action sends modifier state before the key event, then clears the modifier state."
- pin: `Hyprland-ConfigActions.cpp:1554-1558,1576`
- quote: `` `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` ``

Source (`fetch/Hyprland-ConfigActions.cpp`), exact lines:

```
1554  g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);
1555  (blank)
1556  if (S.m_passPressed == 1) {
1557      if (!isMouse)
1558          g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);
1576  g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);
```

Whitespace-collapsed span 1554-1558 contains `…mods(…); if (S.m_passPressed == 1) { if (!isMouse)
…key(…)`; the quoted two-call string is not a substring. The pin cell's second range (`,1576`) is
outside the counter's accepted `name:first[-last]` grammar, so any parser takes 1554-1558 and the
quote fails. Reproduced with the W1 965-line counter (patched only `BASE` and `ENTRY_DEFAULT`):
`d ok=0 quotes_bound=17/18 … miss=P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)`.

### A24-09 — two material claim halves have no quote anywhere (severity: high)

Independent quote census over the landed table (`quote-audit.py`, read-only):

```
P12 claim: "Empty selector input produces a null optional window; a written selector without a result is rejected."
P12 quote: PHLWINDOW PWINDOW = regexp.empty() ? nullptr : …runWindow();      (582-583)
            → the rejection at 585-586 is not in the quote; rationale says "the following guard rejects…"
P16 claim: "…then clears the modifier state."
P16 quote: mods-call (1554) + key-call (1558); the clear at 1576 is not in the quote.

needle 'window not found' in any quote                False
needle 'sendKeyboardMods(0, 0, 0, 0)' in any quote    False
```

Both claims therefore map a material fact to a *locator*, not to the frozen "pinned source quote".
The map satisfies "each proposition has a quote"; it does not satisfy "each material factual
proposition maps to a quote".

### A24-10 — pin path/revision is not per proposition (severity: low)

Every pin cell is a bare `Hyprland-<file>:<lines>`; the revision `efb50993…` appears once in the
footer (`:32`) and in each `SOURCES.md` row anchor. A row lifted out of the file cannot resolve its
pin path (`fetch/`) or revision. This is the same shape the W1 draft TSV used, but the frozen wording
says "each … maps to … a pin path/revision".

### A24-11 — the index row is not a table row (severity: medium)

`corpus/README.md:78` ends the coverage table, `:79` is blank, `:80` is the r52 index row, `:81`
blank, `:82` `## Quality bar`. The row is rendered as a paragraph, not as a coverage-map row; both
counters pass it via a substring test (`knowledge/<basename>`), so a decoration satisfies
"indexed". The row does name `source: S370–S373` and the fetch directory.

### A24-12 — repeated canonical URLs; the lane's own review is outstanding (severity: medium)

Same-URL rows (URL including immutable commit `efb5099…`, computed from `SOURCES.md`):

| new row | same canonical URL prior row(s) | new anchor region | prior anchor region(s) |
|---|---|---|---|
| S370 | S365 | `DispatcherTranslator.cpp:531-627` | `:30-35,797-867` |
| S371 | S367 | `ConfigActions.cpp:1530-1616` | `:1664-1682` |
| S372 | — (new URL) | `ConfigActions.hpp:114-117` | — |
| S373 | S352, S364 | `KeybindManager.cpp:221-242` | `:369,419,488,537-545,652,691-724,773-793,855-899,289-334`; `:41-113,602,782,785,798-823` |

The regions are disjoint, so **materially** the distinct-scope argument holds; but QUALITY.md:34
(rule 17) requires an **explicit** repeated-URL/overlap review, and the lane's own round-52 search
log (`corpus/SOURCES.md:374`) says: "S370, S371 and S373 reuse canonical URLs with new scopes;
distinct-scope review remains outstanding." No recorded review resolves it, and the row scope cells
do not name the prior ids. Note also that `C2PinAudit` §4's collision list names only S364 for the
KeybindManager URL; **S352 collides as well** (see §5).

### A24-13 — W1 counter green does not transfer to the landed artifacts (severity: high)

The W1 965-line draft (`w1/C2CounterDraft/c2-r52-proposition-entry.py`) run against the actual
working-tree artifacts, with a scratch copy patched in exactly two constants
(`BASE`→fixture base commit, `ENTRY_DEFAULT`→landed slug), returns **2/5 clauses**:

```
C2_R52: a ok=1 index_row=`knowledge/hyprland-synthetic-dispatch-r52.md` (round 52;…
C2_R52: b ok=1 propositions=18 ids=18 forms=table
C2_R52: c ok=0 rows_bound=0/18 distinct_rows=0 miss=P01:anchor_no_fetch_root,…
C2_R52: d ok=0 quotes_bound=17/18 quotes_raw=6/17 pins=4 policy=whitespace-collapsed miss=P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)
C2_R52: e ok=0 prose_rows=4 prop_rows=4 manifest_rows=0 miss=P01:id_not_referenced,…
C2_R52: clauses=abcde clauses_met=2 admitted=0/1 verdict=TARGET_MISSED
```

- (c) fails because the `SOURCES.md` anchor cells say `…; r52 fetch SHA256 <digest>` and never name
  the fetch root (`.ufo/waves/round-52`) the counter requires; passing `--fetch-root 'r52 fetch'`
  makes (c) fail on the pin name instead (`P01:anchor_no_pin(Hyprland-legacy-DispatcherTranslator.cpp)`)
  and (d) fail with `pin_file_absent` for every proposition, because the pin index is built by
  `ls_files(repo, rev, fetch_root)`. **No single `--fetch-root` value satisfies both (c) and (d) for
  these rows as written.**
- (e) fails for all 18 ids: the landed entry is table-only; each `Pxx` appears exactly once, and the
  counter requires an id to be drawn on outside its own map row.

So the W1 "r-green" result is a property of the W1 synthetic fixture, not of the landed state —
consistent with the W1 signal, now measured against the actual artifacts.

### A24-14 — the map's own census was not re-run after the table was rewritten (severity: medium)

`w1/C2EntryDraft/entry-draft.md` §Census states "propositions 18, quotes over 25 words 0, quotes not
found at anchor 0 (receipt `quotes-check.txt`)" and `C2PinAudit` §2 states "17/17 PASS" — both were
computed on the W1 TSV/entry revision. The landed 18-row table is not the same table (P16/P17 were
replaced), and its P16 quote fails containment. Neither census applies to the landed bytes, and no
revision note records the re-cut. (This is a scope/currency error in the W1 evidence, not a
misstatement of what those seats measured on their own inputs.)

## 4. Explicitly not covered

- Semantic entailment of any quote (frozen: independent non-author judgement; Attack23's target).
- Whether the entry's mechanism claims are true beyond the four pinned files; no dispatcher, socket,
  hyprctl, input or UI action was performed.
- URL re-fetching: pin identity rests on the local digests agreeing with `fetch/SHA256SUMS` and the
  immutable commit in each URL, plus the W1 audit's earlier agreement with round-51 digests.
- The source-truth sample required by the frozen C2 ("an independent non-author samples actual source
  truth") — that is a separate seat's judgement; this report only supplies structure and locations.

## 5. Errors found in W1 artifacts (reported, not absorbed)

1. **`C2PinAudit` §4 collision list is incomplete**: it lists S370≡S365, S371≡S367, S373≡S364 and
   omits **S352**, whose canonical `KeybindManager.cpp` URL is the same. (S352's anchors do not
   overlap `:221-242`, so the distinct-scope conclusion survives; the census is short one row.)
2. **`C2PinAudit` §2 / `C2EntryDraft` census are stale for the landed table**: the landed P16 quote
   is non-contiguous and fails the same whitespace-collapsed location test those receipts passed on
   the W1 revision; no re-cut is recorded.
3. **`C2CounterDraft` r-green (5/5) does not transfer**: against the actual artifacts the same script
   (two constants patched) is 2/5 (`c`, `d`, `e` red). The W1 signal is confirmed by measurement.
4. **Shipped counter docstring vs body** (`quality/counters/c2-r52-proposition-entry.py:4`): it claims
   "pin revision/quote binding and map completeness"; the body has no source read, no pin use, no
   quote read, no distinctness and no unmapped-row test, and `--base` is dead.
5. **Default target slug mismatch**: counter default `hyprland-synthetic-key-dispatch-r52.md` vs
   landed `hyprland-synthetic-dispatch-r52.md` (rows' `used-by` names the latter).
6. **Registry search log admits rule-17 review outstanding** (`corpus/SOURCES.md:374`) while the same
   paragraph records "excluded 0"; three of the four included rows repeat canonical URLs.

## 6. Severity ranking

1. High — shipped counter cannot parse the landed table and implements none of the claimed bindings
   (A24-02…A24-07, A24-13); "committed" clause unmet (A24-01).
2. High — P16 quote not locatable; P12/P16 material facts have no quote anywhere (A24-08, A24-09).
3. Medium — index row outside the table; repeated-URL review outstanding; W1 census stale
   (A24-11, A24-12, A24-14).
4. Low — per-proposition pin path/revision only transitive (A24-10).

## 7. Reproduction notes

All counters were invoked as `python3 <counter> --repo <fixture> --rev <HEAD> --work <scratch>`
(plus `--entry`, `--base`, `--fetch-root` where named). The shipped counter reads only
`git show <rev>:corpus/{README.md,SOURCES.md}` and the entry; it never reads the fetch root, so the
fixture's pin bytes are irrelevant to its verdicts. The fixture was a fresh `git init` containing a
copy of the lane's `corpus/` and `.ufo/waves/round-52/fetch/`; each mutation was committed so
`rev:path` resolved it, and the working tree was never the lane's. The 965-line draft counter was
copied to scratch and patched in exactly two constants; a third fixture reproduced the frozen-base
shape by materialising `85d57a81:corpus/{README.md,SOURCES.md,QUALITY.md}` and dropping the r52 entry
from the base README, so clause (c)'s base comparison had a real base to read.

Scratch `/fast/scratch/hyaku/mado-r52/Attack24/` (fixtures, receipts, audit scripts) was removed after
this report; the inline commands and outputs above are the durable record.

Report: .ufo/waves/round-52/w2/Attack24.md
