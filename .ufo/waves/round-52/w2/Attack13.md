# Attack13 — W2 attack #13: C2 index row ↔ knowledge entry match

Seat: Attack13 (reviewer, leaf). Round 52, wave 2, lane `mado-shokunin`.
Frozen base `85d57a818c3707397e21c840b6498b105ba798aa`. Lane HEAD at observation: `85d57a81` (= base).
Target clause: C2 "new **indexed** knowledge entry" — the binding between `corpus/README.md`
coverage-map row and `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`, and the counter's
check of that binding.
Method: read-only lane inspection + fixture reproductions in scratch clones under
`/fast/scratch/hyaku/mado-r52/Attack13/` (each `git rev-parse --show-toplevel` asserted inside the
fixture before mutation; the real lane was never mutated). No installs, no host/package/live reads.

## Verdict summary

The index row and the knowledge entry **do match at the text level** in the working tree (row
`corpus/README.md:80` names the file, describes its `sendshortcut`/`sendkeystate` scope, cites
S370–S373 and `.ufo/waves/round-52/fetch/` — all consistent with the entry's own header/map).
**But the match is unverifiable under the C2 contract as landed**: (1) nothing is committed, so no
counter can see the pair at any revision; (2) the committed counter does not check a row–entry
match at all — it checks basename substring presence and passes with zero index rows or a
wrong-subject row; (3) the committed counter cannot even parse the landed entry (reports
`props=0`); (4) the landed row sits outside the coverage-map table (lane gate ERROR); and (5) the
W1-drafted counter, run against a committed copy of the landing, also fails — including one real
data defect (P16 quote not at its cited pin span). Verdict: **falsifier reproduced** — claim not
met at present lane state; "specified control" (counter checks the index/entry binding) is absent
in the committed counter.

## Findings

### F1 — HIGH: landing is uncommitted; no revision contains the row or the entry

`git status --short` in the lane (read-only):

```
 M corpus/README.md
 M corpus/SOURCES.md
 M quality/tool-ledger.md
?? .ufo/waves/round-52/
?? corpus/knowledge/hyprland-synthetic-dispatch-r52.md
?? corpus/lessons/round-52.md
?? quality/counters/c1-r52-ledger.py
?? quality/counters/c2-r52-proposition-entry.py
```

`git log -1` = `85d57a81` = the frozen base. `git show
HEAD:corpus/knowledge/hyprland-synthetic-dispatch-r52.md` → `fatal: path ... exists on disk, but not
in 'HEAD'`; `git show HEAD:corpus/README.md | grep -c hyprland-synthetic` → 0. The new counter reads
only git objects (`git -C <repo> show <rev>:<path>`), so the index row and the entry are invisible
to it at every scoreable revision:

```
$ python3 quality/counters/c2-r52-proposition-entry.py --repo <lane> --rev HEAD \
    --work <scratch> --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md
C2_R52: entry=absent verdict=TARGET_MISSED rev=HEAD          (exit 1)
```

Same result for the default entry slug. Note `.ufo/` is tracked in this lane (24,238 wave blobs at
HEAD), so a conforming landing must commit corpus diffs *and* the wave tree. As observed, C2's
"committed counter / new indexed entry" has not landed in any commit; consistent with the wave
signal "counter draft r-green proves a separate synthetic fixture only, not landing." Limitation:
this may be a pre-integration snapshot; the structural defects below remain at any commit of the
current artifacts.

### F2 — HIGH: committed counter cannot parse the landed entry at all (`props=0`)

The working-tree file `quality/counters/c2-r52-proposition-entry.py` (47 lines, uncommitted) is a
gutted rewrite of the W1 965-line draft — not the "byte-identical copy" the W1 report prescribes.
Its proposition regex requires `P##` then `S###` in cells 1–2
(`^\|\s*(P\d+)\s*\|\s*(S\d+)\s*\|…`), but the landed entry's table is
`ID | Proposition | Source row | Pin:anchor | Quote | Support class | Why` (cell 2 is prose).
Reproduction — scratch fixture `lane-landing` = `git clone` of HEAD + landing snapshot committed
as `0ce0d17c`:

```
$ python3 c2-r52-proposition-entry.py --repo <fixture> --rev 0ce0d17c --work <scratch> \
    --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md
C2_R52: props=0 rows=0 indexed=1 failures=1 verdict=TARGET_MISSED rev=0ce0d17c
miss=props                                                     (exit 1)
```

Even after integration commits the landing, this committed counter can never report TARGET_MET on
the landed entry. (At base it correctly reports `entry=absent`, the frozen control.)

### F3 — HIGH: `indexed` is a basename substring test — absent and wrong rows both pass

Committed counter line: `indexed = f'knowledge/{os.path.basename(a.entry)}' in idx`. Two fixture
runs (scratch repo `fix-b`, entry/SOURCES crafted to the committed counter's own grammar so
`props>0`):

- **B1 (no index row at all)** — README contains the basename only in prose and inside a fenced
  code block, zero table rows for it:
  `C2_R52: props=4 rows=2 indexed=1 failures=0 verdict=TARGET_MET` (exit 0).
- **B2 (wrong row)** — README has a proper coverage-map row for the entry basename that describes
  *wallpaper theming* and cites sources `S099–S100` not present in the entry or registry:
  `C2_R52: props=4 rows=2 indexed=1 failures=0 verdict=TARGET_MET` (exit 0).
- **B3 (control)** — basename fully absent: `indexed=0 … miss=index TARGET_MISSED` (exit 1).

The check fires on substring presence anywhere in README — no row existence, no table membership,
no row↔entry content match, no source-id cross-check. The claim's "indexed" requirement and this
seat's target (row matches entry) are not verified by the committed counter.

### F4 — MEDIUM: committed counter's default slug ≠ landed slug

`--entry` default is `corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md`; the landed file is
`corpus/knowledge/hyprland-synthetic-dispatch-r52.md`. At fixture rev `0ce0d17c`:
`C2_R52: entry=absent verdict=TARGET_MISSED` for both the default and the old `-key-` slug. Any
no-`--entry` run (and the frozen control) silently targets a path that was never landed. The W1
draft warned "if the landed path differs, change that one constant" — it wasn't changed.

### F5 — MEDIUM: the index row is outside the coverage-map table (lane gate ERROR)

`git diff corpus/README.md` inserts the r52 row **after a blank line** following the r51 row, so it
renders as a separate one-row table outside the `|Note|Holds|Sources|` block:

```
$ python3 quality/check-index.py     --root .   → MADO_INDEX: indexed=68/68 missing=0 …
$ python3 quality/check-index-rows.py --root .   → rows=68 errors=1
    ERROR row-outside-map: knowledge/hyprland-synthetic-dispatch-r52.md at line 80
```

The lane's own row-fidelity gate flags it: the row exists but is not *in the index map* — i.e.,
under the corpus's own rules the entry is not properly indexed. Neither C2 counter checks
placement (committed: substring; draft: any unfenced table row), so this defect passes both.

### F6 — MEDIUM: W1-drafted counter also fails the committed landing (incl. one real data defect)

`w1/C2CounterDraft/c2-r52-proposition-entry.py` (965 lines, sha256 `55452a3d…` per W1 report) run
against fixture rev `0ce0d17c` with `--fetch-root .ufo/waves/round-52/fetch`:

```
a ok=1 index_row=`knowledge/hyprland-synthetic-dispatch-r52.md` (round 52;...
b ok=1 propositions=18 ids=18 forms=table
c ok=0 miss=P01:anchor_no_fetch_root,…            (landed S370–S373 anchor cells lack the
                                                    `.ufo/waves/round-52` fetch path the seat
                                                    warned the data seat to include)
d ok=0 quotes_bound=17/18 quotes_raw=6/17 pins=4 miss=P16:quote_not_at_pin
                                                    (Hyprland-ConfigActions.cpp:1554)
e ok=0 miss=P01:id_not_referenced,…               (landed stripped entry references no P## id
                                                    in prose — the draft required each id drawn on)
verdict=TARGET_MISSED (exit 1)
```

- **P16 is a landed-data defect**: the quote
  ``sendKeyboardMods(modMask, 0, 0, 0); … sendKeyboardKey(S.m_timeLastMs, key - 8, …)``
  splices statements at :1554 and :1558 that are not adjacent in the pin (an `if` block intervenes,
  lines 1556–1574), and the locator `…:1554-1558,1576` carries a discontiguous tail the pin grammar
  truncates. A structural binding the W1 green run passed no longer holds in the landed bytes —
  post-`r-draft-fixed` landing drift.
- With the default `--fetch-root .ufo/waves/round-52` the draft additionally reports
  `pin_file_absent` for every pin: the committed wave tree contains each basename twice
  (`fetch/` + `w1/C2EntryDraft/fetch/`, plus `w1/Falsify29/fixture/pins/Hyprland-KeybindManager.cpp`),
  and the draft drops ambiguous basenames — the drafted counter cannot score a landing that commits
  the whole wave tree.

So neither counter can certify the row↔entry binding on the landed artifacts: the committed one
never checks it (F3) and can't parse the entry (F2); the drafted one checks it but fails on
registry-anchor shape, entry completeness, and the P16 quote.

### F7 — INFO: pin bytes and URL-collision status

`sha256sum -c .ufo/waves/round-52/fetch/SHA256SUMS` → all 5 files OK; digests match the S370–S373
anchor cells. The four r52 pins are byte-equal to prior-round pins (draft prints
`pins_prior_equal=4/17`), and S370/S371/S373 reuse URLs already held by S365/S367/S352. The
SOURCES.md search-log line (working tree, uncommitted) itself records: "S370, S371 and S373 reuse
canonical URLs with new scopes; **distinct-scope review remains outstanding**" — the QUALITY17
distinct-scope review the wave brief names is, by the lane's own record, not yet performed. New
scopes are textually distinct in the `scope`/`anchor`/`teaches` cells, but that is my reading, not
the required review.

## Text-level match (fairness)

Independently of the mechanism, the row's *content* does describe the landed entry accurately:
same slug, same sendshortcut/sendkeystate scope, same four source ids, same fetch path, same
"implementation only / no dispatcher run" boundary, and the entry's own `source:` line, verified-at
date and pin footer agree. The failure is that the claim's "indexed … grounded … counter checks
bindings" is not mechanically demonstrable on the current artifacts — and the committed counter
cannot distinguish this honest row from B1/B2 nonsense.

## Reproduction index

| step | command (scratch paths elided) | result |
|---|---|---|
| F1 | `git -C <lane> status --short`; `git show HEAD:corpus/knowledge/hyprland-synthetic-dispatch-r52.md` | `??`/` M` only; `exists on disk, but not in HEAD` |
| F1 | committed counter `--repo <lane> --rev HEAD --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md` | `entry=absent TARGET_MISSED` |
| F2 | committed counter `--repo <fixture> --rev 0ce0d17c --entry …/hyprland-synthetic-dispatch-r52.md` | `props=0 indexed=1 TARGET_MISSED` |
| F3 | committed counter on `fix-b` B1 (no row) / B2 (wrong row) / B3 (no basename) | MET / MET / `miss=index` MISSED |
| F4 | committed counter on fixture, default and `-key-` slug | `entry=absent` both |
| F5 | `python3 quality/check-index-rows.py --root <lane>` | `ERROR row-outside-map … line 80` |
| F6 | draft counter `--repo <fixture> --rev 0ce0d17c --fetch-root .ufo/waves/round-52/fetch` | 2/5 clauses; `P16:quote_not_at_pin` |
| F7 | `sha256sum -c <lane>/.ufo/waves/round-52/fetch/SHA256SUMS` | 5/5 OK |

Fixture construction: `git clone <lane> lane-landing`; copy landing bytes over; `git add -A && git
commit` → `0ce0d17cad16e429a8de572d265630fe4d95fe43` on top of base `85d57a81`. All commits inside
the scratch clone only; lane untouched (verified by identical `git status` before/after).

## Limitations

- Did not perform the QUALITY17 distinct-scope judgment or non-author source-truth entailment
  review — out of seat scope; reported as observed status only.
- P16 `quote_not_at_pin` is proven for whitespace-collapsed single-span binding (the drafted
  counter's frozen policy); if a multi-span policy were adopted the quote still splices
  non-adjacent statements without marking the omission, so it is a data defect under any verbatim
  policy.
- Whether an integrator will commit the artifacts or rewrite the counter before scoring is
  outside this lane observation; every defect above is reproduced on the artifacts as they exist.
- Bash tool aborted compound commands on first nonzero exit during reproduction; each counter run
  was re-issued singly with `||` guards — results unaffected.
- Scratch `/fast/scratch/hyaku/mado-r52/Attack13/` (fixture clones `lane-landing`, `fix-b`, run
  outputs `r*.out`, `landing-rev.txt`) removed after this report; all outputs are reproduced above.

Report: .ufo/waves/round-52/w2/Attack13.md
