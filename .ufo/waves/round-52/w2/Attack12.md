# Attack12 — C2 held overlap and source novelty

Seat: Attack12 (revenger, leaf; W2 attack #12). Lane `mado-shokunin`, base
`85d57a818c3707397e21c840b6498b105ba798aa`. Read before judging: `claims-frozen.md`,
`registration.md`, W1 seats `C2Novelty`, `C2PinAudit`, `C2EntryQuality`, `C2SourceRecon`,
`C2CounterDraft`, `OverlapScan`, plus the W1 draft artifacts and the data-seat rows/entry present in
the working tree at 2026-10-27 11:17.

Axes named: **coverage** (is the claimed coverage delta new ground?) and **operability** (does the
named instrument actually measure the clause it is credited for?). This is an attack, not a vote and
not an admit/reject: no claim text, predicate, control, row or entry was edited by this seat, and
nothing here decides source entailment for the human reviewer.

## Attacked clauses (verbatim)

- `claims-frozen.md` C2: "a distinct new indexed knowledge entry is grounded in sources opened this
  round; each material factual proposition maps to a pinned source quote <=25 words and explicit
  support rationale. A new committed counter checks proposition count, row/pin/quote bindings and
  complete mapping".
- `registration.md` C2: "one new indexed entry on a distinct Hyprland dispatcher-execution
  mechanism"; "each maps to an opened-this-round `S###` row, a pin path/revision and exact located
  quote <=25 words".
- `corpus/QUALITY.md:34` (rule 17, invoked by W1 `C2PinAudit` finding 2): repeated canonical URLs
  must go to explicit distinct-scope review, and "a warning-only shared census is not this review".

## Findings

### F1 — Source novelty is zero at byte level; four of four pins are round-51 bytes (REPRODUCED)

Commands (`source-novelty.txt` §§1–3): `sha256sum .ufo/waves/round-51/fetch/<pin>
.ufo/waves/round-52/fetch/<pin> .ufo/waves/round-52/w1/C2EntryDraft/fetch/<pin>`; plus
`git show 85d57a8:corpus/SOURCES.md` and `git show 85d57a8:corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`.

Observed:

| pin | r51 = r52 = draft | base registry row for the same URL |
|---|---|---|
| Hyprland-legacy-DispatcherTranslator.cpp | EQUAL `7248cbb8…` | S365 |
| Hyprland-ConfigActions.cpp | EQUAL `a83abeb5…` | S367 |
| Hyprland-ConfigActions.hpp | EQUAL `746c6f51…` | none (but r51 pin manifest row `S367`, and r51 entry line 144 quotes `Hyprland-ConfigActions.hpp:114`) |
| Hyprland-KeybindManager.cpp | EQUAL `8d8f35fc…` | S352 (r50) **and** S364 (r51) |

Base registry holds 306 rows, last id `S369`, so `S370–S373` are new ids by construction. The
round-51 pin manifest declares all four files (`…ConfigActions.hpp | … | S367`, `…KeybindManager.cpp
| … | S364`, etc.), and r51 step 4 already quotes line 114 of the header.

Verdict: "grounded in sources opened this round" **reproduces only in the row-id sense**; as new
evidence bytes it is 0/4. The draft's `pins.txt` cell "`none (new URL)`" for `ConfigActions.hpp` is
registry-true and novelty-false — this seat could not distinguish it from a re-open on any byte or
provenance test. This is the same defect `C2Novelty` N2 reported; I reproduce it independently and
add that the fourth file is not new either.

Limit: no network access and no actor-intent evidence; a lane may legitimately define "opened" as
"opened a row". The finding is about what the bytes license, not about what the seat did.

### F2 — Held overlap is 3 of 18 propositions; two reuse the exact lines admitted entries already cite (REPRODUCED, with a corrected count)

Commands: `heldscan-landed.py` (in `w2/Attack12/held-overlap.json`; metric: cited line span vs
`file:line` citations present in the 67 base `corpus/knowledge/*.md` entries, plus longest common
token run of quote/claim). Decisive hits:

| proposition (landed entry) | held citation | quote common run |
|---|---|---|
| P06 "sendshortcut requires exactly three fields" | r51 line 204-205 cites `Hyprland-legacy-DispatcherTranslator.cpp:532-535` | 8 tokens |
| P07 "stringToModMask uppercases input and checks … substring membership" | r50 line 66 cites `Hyprland-KeybindManager.cpp:224`, `:236` | 4 tokens |
| P15 "sendkeystate saves the prior m_passPressed value" | fact held at r51 line 199 (`ConfigActions.cpp:1603-1615`, the twin); translator anchor is new | 4 tokens |

All other 15 propositions have no held line citation and no shared run >3 tokens. Additionally the
landed P17 quotes a substring of P04's quote (`if (keyState == 2 && result.success) …` at `:619-622`)
and restates the same fact a second time, so 18 propositions are 17 distinct facts.

Verdict: `C2Novelty`'s "~13 of 17 propositions rest on ground no admitted entry holds" is **not
reproduced** as stated: it was measured on a 17-row pre-correction map (`C2Novelty.md:14,22`), while
the landed entry has 18 propositions with P16/P17 renumbered and replaced. Recount on the landed
artifact: 15/18 propositions are new by line/quote test, 3 restate held ground, one duplicate pair →
14 distinct new facts over 17 distinct propositions.

Limit: held-fact identity is semantic. I can prove same-line reuse and long shared runs; paraphrase
can hide further overlap, and the exact 8-gram shingle metrics that the r51 predicate used found
**nothing** here (0 shared 8-grams for P06's claim against r51, despite the same cited lines), which
is a metric limitation, not evidence of absence.

### F3 — The QUALITY17 distinct-scope review that the new rows require is absent, and the lane's own log says so (NOT REPRODUCED)

Command: compare each appended row's declared anchor against held citations
(`held-overlap.txt`, section 2; rows read from fixture commit `008c57d`).

| new row | declared scope | held citation inside it |
|---|---|---|
| S370 | DispatcherTranslator.cpp:531-627 | r51 `…:532-535` |
| S371 | ConfigActions.cpp:1530-1616 | r51 `…:1603-1615` |
| S372 | ConfigActions.hpp:114-117 | r51 `…:114` |
| S373 | KeybindManager.cpp:221-242 | r50 `…:224`, `…:236` |

The lane's own search log, appended in the same working-tree change
(`git diff corpus/SOURCES.md`, line beginning "Round 52 — synthetic shortcut path"), reads: "S370,
S371 and S373 reuse canonical URLs with new scopes; **distinct-scope review remains outstanding**."
W1 `C2PinAudit.md:20` also deferred it ("data seat must record it"); no seat in `w1/` records the
review, and `OverlapScan.md` is a cross-claim scan, not a scope review.

Fairness note, and it matters: every held citation above is **outside** the anchor cell of the row
that holds the fact (`S365` = `:30-35,797-867`; `S367` = `:1664-1682`; `S352` = `:369,652,691-724,…`).
The new rows therefore scope bytes no held row anchors — a genuine distinct-scope case rather than a
duplicate, which is exactly why rule 17 sends it to review instead of rejecting it. The defect is
the missing review record, not the reuse.

Verdict: the "distinct" premise is **not established by any artifact in the lane**; it is
undecided at data time. This seat does not assert non-distinctness.

### F4 — The frozen predicate's counter admits a zero-novelty restatement (REPRODUCED: control passes)

Fixture (`w2/Attack12/fixture/hyprland-held-restatement-r52.md`, rows in
`fixture/restatement-rows.txt`): four propositions, each a fact admitted in
`hyprland-dispatcher-dispatch-r51.md` (r51 steps 1, 4, 7: the single translator closure at
KeybindManager.cpp:113, the `DISPATCHER->second(k->arg)` call at :812, the `m_passPressed = -1` reset
at :814, the `ARGS.size() != 3` gate at DispatcherTranslator.cpp:533-534), re-anchored to new rows
`S374`/`S375`. No new mechanism, no new byte, no new scope.

Run (draft counter `C2CounterDraft/c2-r52-proposition-entry.py`, sha256 `55452a3d…`, copied
unmodified; fixture commit `f1bcab31…`; `counter-restatement-control.txt`):

```
C2_R52: a ok=1 ... b ok=1 propositions=4 ... c ok=1 rows_bound=2/4 distinct_rows=2
C2_R52: d ok=1 quotes_bound=4/4 ... pins_prior_equal=2/4
C2_R52: e ok=1 prose_rows=2 prop_rows=2 ...
C2_R52: clauses=abcde clauses_met=5 admitted=1/1 verdict=TARGET_MET
```

Verdict: the predicate's "distinct new entry" **is not among the measured clauses**. Its only
freshness test is row-id absence at base, and its byte-equality diagnostic
(`pins_prior_equal`) is printed but non-gating. A held-ground restatement reaches `TARGET_MET`.
This is the complement control the frozen predicate lacks: the frozen no-work control is base-rev
slug absence (`registration.md`, last paragraph), which cannot see a restatement at candidate rev.

Limit: a control on the instrument, not a statement about the candidate's content. `C2Novelty` N1
predicted this structurally; F4 is the executed receipt.

### F5 — The **committed** counter drops the freshness and binding clauses and passes fabricated sources (REPRODUCED)

`quality/counters/c2-r52-proposition-entry.py` (sha256 `5c7fb820…`, untracked at read time) is 47
lines, not the 965-line draft. Source inspection: it never reads the base registry, never resolves a
pin file, never compares a quote to pin bytes; `--base` is parsed and unused. Probe
(`counter-committed-reuse.txt`, fixture commit `30f937c`): an entry with four propositions citing
**base** rows `S364`/`S365` (only their `used-by` cell amended), four nonexistent pin files, junk
anchors and quotes that appear in no source:

```
C2_R52: props=4 rows=2 indexed=1 failures=0 verdict=TARGET_MET
```

and the same command with `--base 1111…` prints identical bytes, proving the base is never read. The
draft counter on the same commit prints `row_not_new(S364)`, `row_not_new(S365)` and four
`pin_file_absent(...)` — i.e. the committed counter is a regression against its own draft on exactly
this claim's clauses.

Also: on the **landed** candidate the committed counter prints
`props=0 rows=0 indexed=1 failures=1 verdict=TARGET_MISSED` (`counter-committed-candidate.txt`), not
because of the data but because its table regex expects the source row as the second column while
the entry has the proposition there. So the committed instrument cannot measure the artifact it is
credited to measure.

Verdict: the claim sentence "A new committed counter checks proposition count, row/pin/quote
bindings and complete mapping" is **not reproduced** by the committed counter: it checks row
metadata presence (`mined`, `2026-10-27`, entry path, 40-hex) and a ≤25-word quote length, nothing
else. Operability axis: the C2 receipt the claim depends on cannot be produced by these bytes.

Limit: the file is uncommitted and may change before integration; I attacked the bytes present at
2026-10-27 11:17 (sha recorded).

### F6 — Candidate clause reproduction: 2/5 as landed, 3/5 after anchor repair (REPRODUCED)

Draft counter on the landed candidate (fixture commit `008c57d`, `counter-candidate.txt`):

```
a ok=1; b ok=1 propositions=18; c ok=0 rows_bound=0/18 miss=anchor_no_fetch_root ×18
d ok=0 quotes_bound=17/18 quotes_raw=6/17 pins=4 pins_prior_equal=4/17
      miss=P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)
e ok=0 miss=P01..P18:id_not_referenced
clauses_met=2 admitted=0/1 verdict=TARGET_MISSED
```

With only the four row anchors qualified by `.ufo/waves/round-52/fetch/` (fixture commit
`ba4daaaa…`): `c ok=1 rows_bound=4/18`; `d` still fails P16; `e` still fails. Attribution:

1. The appended row anchors carry the pin path and a 40-hex revision but not the round fetch root,
   so the draft counter's clause (c) rejects all 18. The frozen text asks for "a pin path/revision",
   which the rows do carry — this is a counter-vs-claim mismatch the integration must settle, not a
   data defect.
2. P16's locator is a comma list (`1554-1558,1576`); the parser binds only `1554-1558`. Even there
   the quote cannot bind: it splices `:1554` and `:1558`, skipping the intervening
   `if (S.m_passPressed == 1) { if (!isMouse)` lines, so it is not a contiguous substring of the
   span — hence `quote_not_at_pin`. And the entry's claim ("then clears the modifier state")
   depends on `:1576`, the one line the parser dropped.
3. The landed entry has no prose that names a P-id, so clause (e) fails 18/18; the draft's
   "what the evidence licenses" table, which supplied those references, was dropped on landing.

Verdict: the claim's mechanical receipt is **not reproducible on the landed artifact**; it becomes
reproducible only after entry/row edits that no W1 seat performed.

### F7 — W1 receipts are stale against the landed artifact; the reviewer handoff names a proposition that no longer exists (REPRODUCED)

| artifact | count / anchor |
|---|---|
| `C2EntryDraft/proposition-map.tsv` and `quotes-check.txt` (current) | 18 props, P16 = xtract `:47-49`, P18 = `:574` |
| `C2PinAudit/pin-audit-receipt-r52.txt:5` | `TSV rows=17 ids=[…P17]`; its P16 = `ConfigActions.cpp:1578-1579` |
| `C2PinAudit.md:3` | "17/17 proposition quotes" |
| `C2EntryQuality.md:13` | "`quotes-check.txt` reports 16 props" |
| `C2Novelty.md:14,22` | "17 propositions P01-P17", "~13 of 17" |
| landed `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` | 18 props; P16 = modifier ordering `:1554-1576`; P17 = repeat duplicate; P18 = `:574` |

So three W1 seats audited three different revisions and none covers the 18-proposition artifact that
was landed. Consequence for this seat's clause: the held-overlap judgment in W1 was taken on a map
whose P16 (xtract) and P17 (frozen-null) do not exist in the landed entry — the "first sample" that
`C2Novelty` handed the outside reviewer (`P16`) is now a different proposition. The only receipt
covering 18/18 is the entry seat's own `quotes-check.txt`, which is candidate-authored.

### F8 — Smaller errors found while reproducing (each with locator)

1. `w1/C2EntryDraft/entry-draft.md` "held: `corpus/knowledge/bind-table-r25.md:42`" for the
   uppercase/substring claim: line 42 is the zero-mask rejection; the substring statement is line
   44, and line 44 is scoped "the a3w1 walk observed …", not a mechanism fact. The mechanism is held
   at `hyprland-bind-key-match-r50.md:66` (`:224`, `:236`), so the claim survives on a different cite.
2. Landed P17 mislabels its subject: "`sendshortcut`'s repeat branch …"; lines 619-622 are inside
   `sendkeystate` (`sendshortcut` closes at `:589`, `sendkeystate` opens at `:591`).
3. Landed P12's rationale relies on the guard at `:585` that its quote does not contain
   (`PHLWINDOW PWINDOW = regexp.empty() ? nullptr : …` is `:583` only) — the M51-2 shape
   (claim slightly broader than the cited line, rescued by an uncited one), still present after the
   step 6 rewrite that removed the "no focus switch" claim.
4. `.ufo/waves/round-52/fetch/SHA256SUMS` names absolute host paths; digests match (4/4) but the
   manifest is not portable and cannot be checked off this host.
5. `C2PinAudit/pin-audit-receipt-r52.txt` prints `manifest_match=None` for all four digests while
   `C2PinAudit.md:3` claims equality with the round-51 manifest. Equality is true (F1), but that
   receipt line does not carry it.

## What survives (fairness record)

- Subject distinctness holds: none of the base corpus entries contains the identifiers
  `m_keyToCodeCache`, `m_timeLastMs`, `sendKeyboardKey`, `sendKeyboardMods`, or an `xtract(` call or
  definition (`git grep` at base; a bare `xtract` grep only matches the word "extract"), so the
  landed entry's state alphabet, delegate rebuild, keysym scan/cache, timestamp/offset/mask
  ordering and selector-null propositions are new mechanism, not a restatement of the held map.
- Row ids `S370–S373` are absent at base (306 rows, last `S369`), so the letter of "new rows/index
  row" is satisfiable; the entry is indexed in `corpus/README.md` (clause a green).
- All four pins are immutable-commit pins (`efb50993…`) with matching digests, so the evidence is
  reproducible even though it is old evidence.
- The scopes are scope repairs of held citations that sit outside the held rows' anchor cells (F3),
  which is a legitimate rule-17 review case, not automatic duplication.

## Limitations

- Source-only: no network, no host read, no dispatcher run, no screenshot, no package query, no
  install. Novelty and overlap are judged from repo bytes at base and from the working-tree
  artifacts present at 11:17; I did not observe the data seat's intent.
- Held overlap is semantic; F2's three items are proven, further paraphrase overlap is not excluded.
- My counter runs use the draft counter (`55452a3d…`) and the committed counter (`5c7fb820…`) copied
  unmodified, on scratch clones only: two commits for the candidate (`008c57d` as landed, `ba4daaa`
  anchor-qualified) plus `f1bcab31` (restatement control) and `30f937c` (held-row reuse). No lane,
  fleet, sibling or source-repo write; no git/jj mutation outside `/fast/scratch`.
- I did not run the entry seat's `check-quotes.py`; the draft counter's clause (d) is the independent
  binding check I used.
- Nothing here is an admit/reject and nothing scores either claim.

## Deliverables

| artifact | path (relative to lane root) |
|---|---|
| this report | `.ufo/waves/round-52/w2/Attack12.md` |
| source-novelty receipt | `.ufo/waves/round-52/w2/Attack12/source-novelty.txt` |
| held-overlap receipt (rows, propositions, duplicate pair) | `.ufo/waves/round-52/w2/Attack12/held-overlap.txt` |
| per-proposition overlap JSON (draft map / landed entry) | `.ufo/waves/round-52/w2/Attack12/held-overlap.json`, `…/landed-overlap.json` |
| draft counter on landed candidate | `.ufo/waves/round-52/w2/Attack12/counter-candidate.txt` |
| draft counter on restatement control | `.ufo/waves/round-52/w2/Attack12/counter-restatement-control.txt` |
| committed counter on landed candidate | `.ufo/waves/round-52/w2/Attack12/counter-committed-candidate.txt` |
| committed counter on held-row reuse + bogus base | `.ufo/waves/round-52/w2/Attack12/counter-committed-reuse.txt` |
| fixture bytes (entries + appended rows) | `.ufo/waves/round-52/w2/Attack12/fixture/` |

Reproduction recipe (scratch, removed after the run):

```
git clone --shared <lane> <scratch>/fixture
# candidate: copy working-tree corpus/SOURCES.md, corpus/README.md,
#   corpus/knowledge/hyprland-synthetic-dispatch-r52.md, .ufo/waves/round-52/fetch/*; commit -> 008c57d
python3 -I counter-r52.py --repo <fixture> --rev 008c57d… \
  --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md \
  --fetch-root .ufo/waves/round-52 --work <scratch>/work/cand
# restatement control: add rows S374/S375 + entry + README row; commit -> f1bcab31; same command with --entry …
# held-row reuse: from base, append the fixture entry path to S364/S365 used-by + entry; commit -> 30f937c
python3 -I counter-committed.py --repo <fixture> --rev 30f937c… --work <scratch>/work/reuse1 \
  --entry corpus/knowledge/held-rows-reuse-r52.md
```

Scratch `/fast/scratch/hyaku/mado-r52/Attack12/` removed on exit; receipts copied first. No installs;
tooling authorization read at `/home/vgpnk/.omp/agent/RULES.md` (nothing needed).

## Report

```
seat=Attack12 wave=w2 round=52 lane=mado-shokunin base=85d57a818c3707397e21c840b6498b105ba798aa
claim=C2 coverage proposition-bound dispatcher source entry
attacked=C2 clauses "distinct new entry" + "sources opened this round" + "committed counter checks row/pin/quote bindings"; registration "distinct mechanism"; QUALITY.md rule 17 distinct-scope review
verdict=F1 source novelty 0/4 new bytes (REPRODUCED as defect); F2 held overlap 3/18 landed propositions, P06/P07 same cited lines (REPRODUCED; W1 13/17 count NOT REPRODUCED); F3 distinct-scope review absent, lane log says "remains outstanding" (NOT REPRODUCED); F4 frozen counter admits zero-novelty restatement TARGET_MET (predicate distinctness NOT MEASURED); F5 committed counter passes base-row reuse + fabricated pins/quotes/anchors TARGET_MET, --base unused (claim sentence NOT REPRODUCED); F6 landed candidate 2/5 clauses, 3/5 after anchor repair (P16 locator, no prose ids); F7 W1 receipts stale 16/17/17/18, reviewer handoff P16 no longer exists; F8 cite/label errors
survives=subject distinctness (m_keyToCodeCache/m_timeLastMs/sendKeyboardKey/sendKeyboardMods/xtract absent from base corpus); row ids absent at base; pins immutable-commit and digest-stable; star scopes are unanchored held cites, i.e. a legitimate rule-17 review case
receipts=w2/Attack12/{source-novelty.txt,held-overlap.txt,held-overlap.json,landed-overlap.json,counter-candidate.txt,counter-restatement-control.txt,counter-committed-candidate.txt,counter-committed-reuse.txt,fixture/}
report=.ufo/waves/round-52/w2/Attack12.md
```
