# Falsify29 — C2 source proposition entailment: a verbatim ≤25-word span can contradict the proposition it is mapped to

Seat: `Falsify29` (revenger, falsification item 29). Lane: mado-shokunin. Round 52, wave 1.
Base read: `85d57a818c3707397e21c840b6498b105ba798aa` (`git rev-parse HEAD` in the lane; the
only working-tree entry is the untracked round directory).
Axes named: **coverage** (C2's owned axis; attacked) and **operability** (C1's owned axis; no
artifact of this seat touches it, and no package/host/state change was made).
Source-only: no package query, live read, process/compositor probe, input capture, screenshot,
producer execution, or host mutation.

## Attacked clause

Round-52 `claims-frozen.md:11`:

> each material factual proposition maps to a pinned source quote <=25 words and explicit
> support rationale. A new committed counter checks proposition count, row/pin/quote bindings
> and complete mapping; an independent non-author samples actual source truth.

and `registration.md:9`:

> each maps to an opened-this-round `S###` row, a pin path/revision and exact located quote <=25
> words, with a written support rationale; every material factual proposition is mapped. A
> counter checks proposition count, row/pin/quote bindings and index; outside reviewer judges
> source truth.

Attacked item: the **`maps to`** relation. The frozen predicate is satisfiable when every
proposition owns an `S###` row, a pin, a verbatim located span of ≤25 words and a rationale,
while the span does not carry the proposition's operative predicate. Nothing in the frozen
predicate requires the quote to contain the asserted predicate, a complete clause, or the
negation/condition the proposition depends on; `complete mapping` is satisfied by a table row
per proposition regardless of what the quote says.

Distinct from the sibling attacks: `Falsify24` (quote/pin binding) tests whether a quote binds
at all — here every quote binds; `Falsify22`/`Falsify30` test the absence of a proposition map /
line-level granularity — here a full proposition table exists and is honoured; `Falsify21`
attacks the same clause from a different fixture. This seat shows the hole that survives a
correctly built proposition table.

## Mechanism (three named sub-modes, one root)

The nearest committed acceptance code, `quality/counters/c2-r51-dispatch-entry.py:329-375`
(`bind_row`), accepts a quoted span when it is whitespace-collapsed-substring-contained in the
cited pin span (`:372`) and its word count is ≤25 (`:370`). Substring containment is indifferent
to where the span starts and ends inside the source statement, so the author controls which
tokens are inside the support:

1. **Negator elision.** The quote starts after a leading `not`/`!`/`!=` that the proposition needs.
2. **Omitted setter/initializer.** The quote covers the branch but not the initialisation line the
   proposition names.
3. **Span widening.** The locator names a line range; the quote is lifted from one statement in
   the range while the gating statement is the other.

## Reproducible setup and commands

All commands run from the seat directory (absolute path
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/Falsify29`). No `TMPDIR`
artifact is written; the checker writes nothing outside it. `python3 -I`, so no user site.

```
python3 -I accept_probe.py
python3 -I c2_fixture_check.py --fixture fixture --entry entry/hyprland-dispatcher-argument-split-r52-fixture.md
python3 -I c2_fixture_check.py --fixture fixture --entry entry/hyprland-dispatcher-argument-split-r52-operator-visible.md
python3 -I c2_fixture_check.py --fixture fixture --entry entry/hyprland-dispatcher-argument-split-r52-truthful.md
python3 -I c2_fixture_check.py --fixture fixture --entry entry/absent-target.md
python3 -I truth_scope_audit.py
python3 -I draft_binding_audit.py
```

`accept_probe.py` imports `bind_row` straight out of the committed counter at the lane path (no
reimplementation) and calls it with real pin bytes; `c2_fixture_check.py` mirrors the frozen
machine-checkable conditions (index row, ≥4 propositions, non-empty row/pin/quote/rationale per
proposition, registry row `mined` + `opened 2026-10-27`, verbatim ≤25-word span at the stated
locator); `truth_scope_audit.py` prints the located bytes and the operator tokens that fall
outside the quoted span; `draft_binding_audit.py` runs the binding plus a support window over the
live draft map snapshot.

Pins are read-only copies of locally available round-51 fetches (no fetch this round):
`fixture/pins/wiki-Dispatchers.md` (sha256 `39d0747a…`, line 15) and
`fixture/pins/Hyprland-KeybindManager.cpp` (sha256 `8d8f35fc…`, line 820). Provenance in
`fixture/pins/PROVENANCE.md`.

## Results

### 1. The committed acceptance function accepts both negator-elided spans

`receipts/accept-probe.txt`:

```
ROW  S380 … BIND  ACCEPT pin=wiki-Dispatchers.md:15-15 quote='invoke any action immediately' quote_words=4
ROW  S381 … BIND  ACCEPT pin=Hyprland-KeybindManager.cpp:820-820 quote='k->submap.reset.empty()' quote_words=1
LEFT-CONTEXT …
  wiki-Dispatchers.md:15  full : … They do not invoke any action immediately, and their
                          before span: 'cribe an action you want to make. They do not '
  Hyprland-KeybindManager.cpp:820 full : if (k->handler != "submap" && !k->submap.reset.empty()) {
                          before span: '            if (k->handler != "submap" && !'
```

Both spans are verbatim, ≤25 words, at the named pin line, and both were offered for the
opposite of what the source says: the wiki says dispatchers **do not** invoke on call, and the
code requires the reset field to be **non-empty**.

### 2. A five-proposition entry passes every frozen machine condition with three false propositions

`receipts/fixture-check.txt` and `receipts/variants.txt`. Three staged entries share one shape;
the checker prints `verdict=TARGET_MET props=5` for all three:

| variant | binding | propositions | truth of P2/P4/P5 |
|---|---|---|---|
| `…-fixture.md` (negator elided) | all pass | 5 | false |
| `…-operator-visible.md` (same propositions, operator inside the quote) | all pass | 5 | false |
| `…-truthful.md` (same shape, propositions the source states) | all pass | 5 | true |

The structural verdict is identical across the false and the truthful entry — the predicate
cannot distinguish them; only reading the source does. `receipts/truth-scope.txt` shows the
located bytes behind that table:

```
P2 … quote 'invoke any action immediately' (4 words) … verbatim yes
   operator tokens before the quote (outside it): ['not']
P4 … quote 'k->submap.reset.empty()' (1 words) … verbatim yes
   operator tokens before the quote (outside it): ['!']
P5 … locator Hyprland-KeybindManager.cpp:820-823 … quote 'Config::Actions::setSubmap(k->submap.reset);'
   operator tokens before the quote (outside it): ['!']
```

P5 also consumes a four-line locator: the gated write is on line 823, its gate is line 822 —
sub-mode 3.

### 3. The live C2 draft already contains three propositions whose support lies outside the quote

Snapshot `fixture/draft-proposition-map.snapshot.tsv` (sha256
`447b84b4e448707b693b23f3eac5ef00bebf1fbeea52f6057c1f1889e52e48ce`, taken from
`.ufo/waves/round-52/w1/C2EntryDraft/proposition-map.tsv`; the peer was still editing, so the
snapshot, not the live file, is the evidence). `receipts/draft-binding.txt`: all 16 rows are
≤25 words and verbatim at their stated anchor; then:

- `P03` — proposition "`up` is the default keyState 0"; quote is lines 601-604; the initialiser
  `uint32_t keyState = 0;` is line 600, outside the quote and outside the anchor.
- `P15` — proposition "`sendkeystate` restores the previous press field after it delegates"; quote
  is only line 612 (the save); the restore is line 624, outside.
- `P16` — proposition "…and it also repeats on success"; quote is the function signature on line
  1601 only; the repeat is lines 1612-1613, outside.

These three live propositions are true against the source (the bytes are in the receipt), so this
is a *support-gap*, not a live false claim: the quote bound to each does not carry the predicate
the proposition asserts. It shows the gap arises at 3/16 without adversarial intent.

### 4. The frozen control cannot catch this

`.ufo/waves/round-52/receipts/c2-base.txt` reports an unchanged entry absent at base, and
`git ls-tree -r 85d57a8 -- corpus/knowledge` gives 67 entries with three dispatcher slugs
(`dispatcher-semantics-r25`, `dispatcher-surface-and-request-grammar-r26`,
`hyprland-dispatcher-dispatch-r51`) and no round-52 entry. My checker's absence branch
(`receipts/base-absence.txt`) prints `C2FIX: a ok=0 entry=absent` /
`verdict=TARGET_MISSED`, matching the no-work control by construction. The control tests entry
absence, which is orthogonal: it passes the control while any admitted entry, however supported,
satisfies the same predicate.

## Verdict

- **Reproduced: yes**, at the level the round permits: the committed `bind_row` acceptance runs
  and accepts both negator-elided spans; a five-proposition staged entry with three
  source-contradicted propositions reaches the full frozen machine verdict (`TARGET_MET`, exit 0)
  in `receipts/variants.txt`; the truthful twin reaches the same verdict, so the distinction is
  invisible to the predicate. The live draft's support gap reproduces on snapshot bytes.
- **Not reproduced:** no live draft row asserts a *false* proposition; the false-proposition
  instance is seat-local fixture bytes. No round-52 C2 counter exists yet, so the mirror used here
  is the frozen predicate's machine-checkable reading plus the committed `bind_row` code path; a
  newly written counter that checks only "quote is verbatim at pin, ≤25 words" inherits the hole,
  while a counter that additionally requires the recorded span to contain the predicate would not.
- **No claim or predicate edited.** The finding is about what the frozen wording admits, not a
  request to weaken it. If the evaluation wants this closed within the frozen text, the
  `outside reviewer judges source truth` clause already permits it: the reviewer must read the
  **recorded statement span**, not the quote, and must reject a mapping whose span excludes the
  proposition's operative predicate (negation, condition, initialiser, gated write). A counter
  can flag boundary risk mechanically (operator tokens in the left context, as
  `truth_scope_audit.py` prints), but a token blacklist is incomplete (`unless`, `only`, `or`,
  ternaries, short-circuit order) and must not be presented as entailment.

## Limitations and dissent

- The fixture reuses round-51 pin bytes, which are locally available, not newly opened this
  round; it is a mechanism fixture, not a C2 entry candidate, and claims nothing about which
  sources the round-52 entry must open.
- The live draft map is a peer's in-progress artifact; the snapshot is stated by hash and the
  audit does not chase later edits. Whether the shipped entry keeps `P03`/`P15`/`P16` in this shape
  is the author's and the outside reviewer's call.
- `bind_row` is round 51's code; the round-52 counter does not exist in this source view. The
  probe therefore establishes the shape a naive counter inherits, not a verdict on unwritten code.
- No arm of C1 was touched; no axis harm is claimed or observed. Round is source-only: no live
  compositor, package, or host state used.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify29.md` — this report.
- `.ufo/waves/round-52/w1/Falsify29/accept_probe.py` — imports `bind_row` from the committed
  counter and accepts both elided spans.
- `.ufo/waves/round-52/w1/Falsify29/c2_fixture_check.py` — frozen machine-checkable mirror.
- `.ufo/waves/round-52/w1/Falsify29/truth_scope_audit.py` — located bytes + outside-span operators.
- `.ufo/waves/round-52/w1/Falsify29/draft_binding_audit.py` — 16/16 binding plus support window.
- `.ufo/waves/round-52/w1/Falsify29/fixture/entry/…-fixture.md`, `…-operator-visible.md`,
  `…-truthful.md` — the three staged variants.
- `.ufo/waves/round-52/w1/Falsify29/fixture/registry/SOURCES.md`, `fixture/README.md` —
  fixture registry and index.
- `.ufo/waves/round-52/w1/Falsify29/fixture/draft-proposition-map.snapshot.tsv` — hashed draft
  snapshot.
- `.ufo/waves/round-52/w1/Falsify29/fixture/pins/{wiki-Dispatchers.md,Hyprland-KeybindManager.cpp,SHA256SUMS,PROVENANCE.md}`
  — read-only pin copies.
- `.ufo/waves/round-52/w1/Falsify29/receipts/{accept-probe,fixture-check,variants,truth-scope,draft-binding,base-absence}.txt`.

Scratch `/fast/scratch/hyaku/mado-r52/Falsify29` was created, used, and removed; `df -h /fast`
showed 600G available before the work. No installs; PACMAN not invoked; no tracked lane file
written (`git status --porcelain` shows only the pre-existing untracked round directory).

Report: `.ufo/waves/round-52/w1/Falsify29.md`
