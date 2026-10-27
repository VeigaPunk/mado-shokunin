# R53One9 — simplifier: C1 ledger counter and C2 proposition-repair entry

Role: simplifier seat (leaf). Axes named: **operability** (C1) and **coverage** (C2).
Base: `ad4bf2059bcfafe63671d262222908ee1fe8001c`. Lane repo read-only; no tracked edit, no
commit, no jj, no dispatch. This is a design/simplification review plus measurement, **not a
vote and not an admission**; no non-author-reviewer credit is claimed here.

Attacked predicates (frozen, `.ufo/waves/round-53/claims-frozen.md`):

- **C1** — "operability: instrument-ledger accountability counter … Before: r51 counter accepts
  repeated generic descriptions and ledger self-pointers; r52 verifier reproduced bypasses.
  Target: a newly committed, scratch-aware counter with explicit selftest returns TARGET_MET on
  the production ledger, TARGET_MISSED on a no-work control and each frozen forgery fixture, with
  exact population coverage and non-self pointers."
- **C2** — "coverage: repair proposition-grounding defects in the indexed r52 dispatcher entry …
  Before: r52 verifier found P16 quote spliced, P17 misattributed, P18 mislocalized; no valid r52
  admission counter. Target: append-only correction clearly repairs those three propositions
  against opened pinned source bytes; a frozen counter rejects the old bytes and accepts corrected
  entry with quote/pin/proposition bindings."

## 1. What was measured, and on which bytes

All work in `/fast/scratch/hyaku/mado-r53/R53One9` (prototypes only; deleted at yield). Nothing
was executed against a live host surface: no `hyprctl`, no package query, no producer run, no
screenshot, no input capture. Lane bytes were read with `git show/ls-tree` at the base rev only.

Byte sets:

| Set | Identity |
|---|---|
| production ledger | `quality/tool-ledger.md` @ `ad4bf20`, 119 lines, 82 data rows |
| population | 82 = `tools/` 17 + `quality/*.py` 19 + `quality/counters/*.py` 46 (frozen r51 filter, `__pycache__`/`.pyc` excluded) |
| C1 forgery fixtures | the six r52 w1/w2 ledger forgeries + the frozen no-work control + the four w1 single-defect controls (`control-B/C/D/E`), the three `mut-*` ledgers, and the nine Attack02 self-pointer spellings (rebuilt in scratch from the production ledger, one cell changed each) |
| C2 source bytes | `.ufo/waves/round-52/fetch/` — `sha256sum -c SHA256SUMS` → 5/5 `OK` (pinned Hyprland rev `efb50993780079460b0cbed1363e2166a2de1d9f`, opened 2026-10-27) |
| C2 entry | `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` @ `ad4bf20`, 18 propositions |

No new network source was opened this round; every quote below is from the committed fetch bytes,
located by file and line, and the checksum receipt above carries the identity of those bytes.

## 2. C1 — before-state, and why the r52 layer is the right thing to delete

**Before (structural proof, not an assumption).** Two tracked instruments carry ledger
accountability today, and neither has a self-reference or description-content clause:

```
$ grep -n "self_pointer\|generic_desc\|dup_desc\|desc_short" quality/counters/c1-r51-ledger.py quality/check-tool-ledger.py
(no matches)
$ grep -n "uncovered\|dangling\|bad_pointer\|empty_desc" quality/check-tool-ledger.py | head -4
29:    uncovered        population path with no row
30:    dangling         row whose path is not in the population, …
32:    bad_pointer      pointer names no existing file, or none of the named files contains the
34:    empty_desc       description is blank or a placeholder
$ python3 -I c1-r51-ledger.py --repo <lane> --rev ad4bf20… --work <scratch>
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
```

The r51 counter is green on production and its frozen summary carries only four row fields. A
ledger of 82 repeated "Accountability row for this tracked instrument ledger." descriptions, or
82 rows pointing at the ledger itself, is indistinguishable to it. That is the before-state, and
the r52 verifier's reproductions (`.ufo/waves/round-52/w2/Attack01.md`, `Attack02.md`) are the
routed evidence for it — cited here as evidence, not re-asserted as my own run.

**What the failing r52 draft cost.** `.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py`
is 847 lines with `SELFTEST_CHECKS = 53`, and its context clause is a four-filter phrase lift
(`bigrams`, `path_fragments`, `path_words`, `population_path_words`, lines ~404-437). Attack01
T2 measured that clause at a **total** bypass (82/82 forged rows `TARGET_MET`); Attack02 measured
the self clause at exact string equality and defeated it with **nine spellings**. Four filters
did not buy what one integer buys.

## 3. C1 — the simplest counter that meets the frozen target, with measured margins

Proposal `quality/counters/c1-r53-ledger.py` (self-contained; no `--checker` subprocess, no
second authority). Predicates, all structural, each printed as its own field:

1. `population` — the frozen r51 filter at `--rev`, derived from the tree, never from the ledger
   (the counter includes itself once committed).
2. Row coverage — `uncovered`/`dangling`/`dup` and `schema` (exactly three cells; **fenced rows
   skipped** — the ledger's own grammar example at `quality/tool-ledger.md:11-13` is a row only to
   a counter that does not skip fences).
3. Pointer — every path-shaped token must resolve at `--rev` (`unresolved_token`); the accountable
   target must be a regular blob (`mode != 120000`, `symlink_target`); it must contain the row's
   basename and must not be the row itself (`bad_pointer`).
4. `self_pointer` — **normalized identity**, not string equality: strip backticks, a `:N`/`:N-M`/
   non-numeric suffix, leading `./`, leading `/`, collapse `//`, strip trailing punctuation,
   casefold; compare against the ledger path **and the ledger basename in the pointer region**,
   and against the row's own path and basename. Descriptions are never scanned (see the G finding
   below): a legitimate instrument that *reads* the ledger must stay green.
5. `desc_short` — **≥8 raw words** (whitespace tokens, no stopword list). `desc_namebound` —
   ≥6 words that are not drawn from the instrument's own path tokens. `desc_ungrounded` — ≥3 words
   occurring verbatim (word-boundary) in the instrument's own bytes at `--rev`. These three replace
   the four lexical filters.
6. `desc_dup` — normalized descriptions pairwise unique; `desc_template` — no 3-word shingle may
   occur in `≥ max(4, ceil(population/10))` rows (the "repeated generic descriptions" defect,
   measured as repetition rather than judged as prose).
7. `--selftest` — explicit, in-process, over a frozen fixture map (no git, no temp repo):
   production green, no-work control red, each frozen forgery red on its named field, one green
   self-reader control, one red per pointer defect, and the two fence/grammar checks. Exit 0 only
   when every check passes; prints `C1_R53_SELFTEST: n/n passed`.
8. Scratch-aware — `--work` (or mkdtemp under `TMPDIR`) refused under `/tmp`, `/var/tmp`,
   `/dev/shm`; the created clone/work removed in `finally`; nothing written inside the repo.

Measured matrix (prototype, predicates exactly as above; `<L>` = lane, `R` = base rev, `<F>` = a
fixture path — the prototype took `--repo <L> --rev R [--ledger <F>]`):

```
$ python3 c1proto.py <L> R
C1_R53: population=82 ledger_rows=82 uncovered=0 dangling=0 dup=0 schema=0 self_pointer=0 schema_self_pointer=0 symlink_target=0 bad_pointer=0 unresolved_token=0 desc_short=0 desc_namebound=0 desc_ungrounded=0 desc_dup=0 desc_template=0 red=- verdict=TARGET_MET

$ python3 c1proto.py <L> R .ufo/waves/round-52/controls/c1-do-nothing.md
… schema=2 dup=1 self_pointer=0 schema_self_pointer=1 bad_pointer=1 desc_short=1 desc_ungrounded=1 uncovered=81 …
red=schema,dup,bad_pointer,desc_short,desc_ungrounded,uncovered verdict=TARGET_MISSED

$ python3 c1proto.py <L> R .ufo/waves/round-52/w2/Attack01/controls/F-all-forged.md
… desc_short=82 desc_ungrounded=61 desc_template=3 … red=desc_short,desc_ungrounded,desc_template verdict=TARGET_MISSED

$ python3 c1proto.py <L> R .ufo/waves/round-52/w2/Attack01/controls/H2n-verify.sh-forged.md
… desc_short=1 … red=desc_short verdict=TARGET_MISSED

$ python3 c1proto.py <L> R <P21 spelling fixture>   # `Quality/tool-ledger.md` + PROVINCE.md
… self_pointer=1 … red=self_pointer verdict=TARGET_MISSED

$ python3 c1proto.py <L> R <symlink-target fixture>  # pointer = a tracked mode-120000 path
… symlink_target=1 … red=symlink_target verdict=TARGET_MISSED
```

Full matrix (verdict and the `red=` field only; every row measured on the same run):

| Fixture | Source | Verdict | named defect fields |
|---|---|---|---|
| production ledger | `quality/tool-ledger.md` | **MET** | — |
| `c1-do-nothing.md` | r52 `controls/` | MISSED | schema, dup, bad_pointer, desc_short, desc_ungrounded, uncovered |
| `control-F3-forged.md` | r52 w1 | MISSED | desc_namebound, desc_ungrounded, desc_template |
| `control-H-minimal-forgery.md` | r52 w1 | MISSED | desc_short, desc_ungrounded |
| `F-all-forged.md` | r52 w2 A01 | MISSED | desc_short, desc_ungrounded, desc_template |
| `H2n-verify.sh-forged.md` | r52 w2 A01 | MISSED | desc_short |
| `H3n-c2r51-forged.md` | r52 w2 A01 | MISSED | desc_short, desc_ungrounded |
| `H4n-nameonly-forged.md` | r52 w2 A01 | MISSED | desc_short |
| `control-B-row-selfpointer.md` | r52 w1 | MISSED | self_pointer, bad_pointer, desc_short, desc_ungrounded, desc_dup, desc_template |
| `control-C-ledger-selfpointer.md` | r52 w1 | MISSED | self_pointer, bad_pointer |
| `control-D-generic-desc.md` | r52 w1 | MISSED | desc_short, desc_ungrounded, desc_dup, desc_template |
| `control-E-one-selfpointer.md` | r52 w1 | MISSED | self_pointer, bad_pointer |
| `mut-badpointer.md` | r52 w1 | MISSED | bad_pointer, unresolved_token (only the injected defect) |
| `mut-dup.md` | r52 w1 | MISSED | dup (only the injected defect) |
| `mut-emptydesc.md` | r52 w1 | MISSED | desc_short, desc_ungrounded |
| 9 self-pointer spellings (rebuild of Attack02 P03/P04/P05/P06/P07/P19/P20/P21 + `QUALITY/…` upper case) | scratch | MISSED | `self_pointer=1` each — one field, isolated |
| symlink target (tracked mode-120000 path) | scratch | MISSED | `symlink_target=1` |
| unresolvable pointer token | scratch | MISSED | `unresolved_token=1` |
| duplicate description + 83rd row | scratch | MISSED | dup, desc_dup |
| `control-G-legit-ledger-reader.md` (legit 8-word reader row) | r52 w1 | **MET** | — |
| extended G (same row, 12 words) | scratch | **MET** | — |

**Margins on production** (measured, one row each): raw words floor **9** (the row
`quality/counters/c2-r51-dispatch-entry.py`); non-path words floor **9**; instrument-grounded floor
**3** (`quality/counters/c2-r51-dispatch-entry.py` — zero margin); max 3-shingle multiplicity **2**
against a limit of 9. Against the fixtures: H2n/H4n sit at 7/6 raw words (1-2 below the floor),
F-all at 6, the template fixtures at multiplicity 82 (73 above the limit).

**Finding — the stopword list was the false economy, and it decided the G conflict.** My first
variant filtered stopwords and required ≥7 *content* words. Under it the r52 legitimate control G
(`quality/check-tool-ledger.py` = "Reads \`quality/tool-ledger.md\` and reports each instrument's
accountability row.") is red (5 content words) while the shebang-lifted forgery H2n is also 6 —
i.e. **no single content-word floor both accepts G and rejects H2n** (measured: G = 5 content / 8
raw; H2n = 6 content / 7 raw). Dropping the stopword list and reading **raw** words at ≥8 resolves
it: G (8) green, H2n (7) red, production floor 9 with margin 1, and there is no frozen vocabulary
list to maintain. That is why the recommended floor is raw ≥8, not content ≥7.

**Residual, stated in the claim's own language.** A per-row structural check cannot separate a
motivated forgery from a real description: on the known F3 forgery, 41 of 82 rows pass every
per-row predicate (only the file-level `desc_template` and the 41 flagged rows make the file red),
and a forger who writes 8 raw words, 3 of them lifted from the instrument, passes. C1 is a bounded
structural accountability check, not prose entailment; the counter's receipt should print that
number (rows flagged / rows scored) so the bound travels with the verdict.

## 4. C2 — the three defects, located, and the append-only repair that clears them

Defects re-measured against the committed fetch bytes (independent of the r52 seats' text):

| Row | Located truth | Consequence |
|---|---|---|
| P16 | `Hyprland-ConfigActions.cpp:1554` `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);`, `:1556-1557` `if (S.m_passPressed == 1) { if (!isMouse)`, `:1558` `g_pSeatManager->sendKeyboardKey(…PRESSED);`, `:1576` `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` | the entry's space-joined quote exists nowhere: `contiguous=False`; the guard is elided, and the clear call is located but not quoted |
| P17 | `sendshortcut` span **531-589**, `sendkeystate` span **591-627** (derived by brace counting from the column-0 definitions) | pin `:619-622` is inside `sendkeystate`; the proposition names `sendshortcut` → subject false. It also restates P04 |
| P18 | loop `:565-571`, return `:574` | `:574` is after the loop closes → "inside the scan" is false |

Contiguity/word-cap sweep over all 18 rows (whitespace-collapsed quote must occur inside the pin
span; ≤25 words): **17/18 contiguous**, word counts 5-19, **P16 the only splice**. This reproduces
the routed finding and nothing more.

Proposed append-only section (adds rows, leaves the 18 base rows byte-identical; ready to paste
into `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`):

```
## Correction ledger (round 53) — append-only

| ID | Base row | Defect | Repair | Evidence pin |
| R16 | P16 | quote spliced: :1554 and :1558 joined while the `m_passPressed`/`isMouse` guard sat between them; the clear call was located at :1576 but never quoted | P16 withdrawn; P16a restates delivery with one contiguous quote, P16b quotes the clear call | Hyprland-ConfigActions.cpp:1554-1558,1576 |
| R17 | P17 | subject misattributed: :619-622 lies in `sendkeystate` (591-627), not in `sendshortcut` (531-589); the mechanism duplicates P04 | P17 withdrawn; the restore step it should have described is recorded as P19 | Hyprland-legacy-DispatcherTranslator.cpp:591-627,624 |
| R18 | P18 | localization false: :574 runs after the scan loop closes at :571, in the cache-miss branch | P18 restated as P18a with the loop inside the locator | Hyprland-legacy-DispatcherTranslator.cpp:565-574 |
```

with four proposition rows appended in the same 7-column shape: **P16a** (quote = the contiguous
`:1554-1558` collapse, 16 words, guard included), **P16b** (quote = `:1576`, 5 words), **P19**
(quote = `:624` `Config::Actions::state()->m_passPressed = oldPassPressed;`, 3 words), **P18a**
(quote = `:574`, 10 words, locator `:565-574`).

Frozen counter `c2-r53-proposition-repair.py`, five clauses (all mechanical, ~160 lines):

1. `quote_contiguous` — whitespace-collapsed quote ⊆ whitespace-collapsed pin span, and
   `3 ≤ words ≤ 25`.
2. `subject_outside_span` — for every backticked token in the proposition/rationale that names a
   column-0 function **defined in the pinned file**, every anchor line must fall inside that
   function's derived span (brace counting from the definition line). This is what makes P17's
   false subject a machine finding rather than a reader's judgement.
3. `containment_false` — if the proposition claims "inside/in/within the scan|loop", the pin's
   end line must lie inside a derived loop span; if it claims "after the … scan|loop", the pin span
   must contain a loop that ends before the last anchor.
4. `pin_file` — the pin file resolves under `--fetch` and matches `SHA256SUMS`.
5. `append_only` / `unrepaired` — every base row present at `--base-entry` must appear
   byte-identical; every base row that fails a clause must be named by a repair row's `Base row`
   cell, and a repair row may not name a non-existent base id.

Measured arms:

```
$ python3 c2proto.py --fetch <lane>/.ufo/waves/round-52/fetch --entry <base entry at ad4bf20>
C2_R53: props=18 repairs=0 red=P16:quote_not_contiguous;P17:subject_outside_span=sendshortcut;P18:containment_false verdict=TARGET_MISSED

$ python3 c2proto.py --fetch <…>/fetch --entry <base+correction> --base-entry <base>
C2_R53: props=22 repairs=3 red=- verdict=TARGET_MET
```

Clause isolation (mutations of the corrected entry, same command shape):

| # | Mutation | Observed |
|---|---|---|
| M1 | re-splice P16a's quote (drop the guard) | `P16a:quote_not_contiguous` |
| M2 | P19 subject → `sendshortcut` | `P19:subject_outside_span=sendshortcut` |
| M3 | reinstate "Inside the scan" on P18a | `P18a:containment_false` |
| M4 | rewrite base row P06's text | `P06:append_only_violated+unrepaired` |
| M5 | repair row names `P99` | `P17:…+unrepaired;R17:supersedes_unknown=P99` |
| M6 | drop the R18 repair row | `P18:containment_false+unrepaired` |
| M7 | inflate P19's quote to 30 words | `P19:quote_words=30+quote_not_contiguous` |

Residual: clause 1 proves a quote is *there*, not that it *entails* the proposition (M7's inverse —
a true-but-weak quote at a true pin — passes). Sufficiency stays a non-author reading, as the
entry's own footer says. Also `NO expansion credit`: the repair re-pins S370/S371/S372/S373, all
already-held ground; the corrected entry must not be scored as new coverage, and P19 must be
recorded as a repair row, not as an expansion proposition.

## 5. Test cases to freeze before data

C1 (each is one command, one expected line; the arm shapes are the ones measured above):

| # | Case | Expect |
|---|---|---|
| T1 | production ledger at `--rev` | MET, all fields 0, `rows == population` |
| T2 | `controls/c1-do-nothing.md` | MISSED; `schema`, `dup`, `uncovered`, `unresolved_token`/`bad_pointer` |
| T3 | F3, F-all, H-minimal, H2n, H3n, H4n | MISSED; the named fields in §3 |
| T4 | `control-G-legit-ledger-reader.md` (8 raw words, names the ledger in its description) | **MET** — the self clause must not read descriptions |
| T5..T13 | nine self-pointer spellings, one at a time | MISSED with `self_pointer=1` and nothing else |
| T14 | pointer = tracked mode-120000 path | MISSED `symlink_target=1` |
| T15 | pointer token that does not resolve | MISSED `unresolved_token=1` |
| T16 | 83rd row / duplicated description | MISSED `dup` / `desc_dup` |
| T17 | population mutated by one instrument with no row | MISSED `uncovered=1` |
| T18 | ledger with the fenced grammar example only in a fence | MET (fence skip proven by T1) |
| T19 | `--selftest --work /tmp/x` | exit 2 (refused root) |
| T20 | `--selftest` | `C1_R53_SELFTEST: n/n passed`, exit 0 — and `n` must equal the number of checks the receipt cites |

C2: the two arms plus M1-M7 (§4), plus `pin_file` (corrupt one fetch byte in a copy → red) and
`≥4 substantive propositions` (drop to 3 → red).

## 6. Simplification ledger — what this deletes

| Deleted | Why it is safe to delete |
|---|---|
| the four-filter `generic_desc` phrase lift (r52 draft, ~40 lines + 4 helpers) | measured total bypass (82/82); replaced by three integers (`desc_short`/`desc_namebound`/`desc_ungrounded`) plus a repetition rule |
| the r51 counter's `--checker` subprocess + field-agreement block (~60 lines) | a second tracker of the same six fields; the counter must print those fields itself, and the cross-check cannot catch a shared blind spot |
| the r52 draft's `fixture_repo`/selftest-over-git (~140 lines, 53 checks needing a temp repo) | a pure `measure(population, files, modes, blobs)` core makes the selftest a dict-fed table; no git, no work dir, no refused-root exposure |
| any frame/prefix heuristic at a fixed absolute threshold | fixed thresholds false-positive on legitimately similar tools (`mut-badpointer` at 3 rows); the relative limit `max(4, ⌈pop/10⌉)` keeps the fixture margin (82 vs 9) and clears the mutation |
| the stopword list (my own first draft) | it forced the G/H2n conflict and needs maintenance; raw-word floors at 8 separate them |

Kept deliberately: population derivation from the tree, fence skipping, pointer resolution, the six
frozen summary fields (`population ledger_rows uncovered dangling bad_pointer empty_desc`), exit
0/1/2, and the r51 refused-root behaviour.

## 7. Limitations

- Prototypes were scratch-only and are deleted; the numbers above are the durable receipts. The
  lane must re-derive them with its committed counter before any admission — that is the point of
  T20.
- The "before" arm for C1 could not be executed on a forged ledger: neither r51 instrument accepts
  `--ledger`, and building a scratch repo would need a commit (forbidden for this seat). The
  before-state is proven from the contract text and the clause-absence grep, plus the committed
  r52 reproductions, and is labelled as such.
- Counts are per-population-at-base (82). At the r53 tip the new counter adds itself: population
  83, so `quality/tool-ledger.md` must gain exactly one row naming `quality/counters/c1-r53-ledger.py`
  with a **non-self** pointer (a round-53 document that contains that filename; not the ledger, not
  the counter). Any sibling counter committed this round adds one more row each — the counter
  derives the population, so a missing row is `uncovered`, never a silently smaller denominator.
- C2's C++ span derivation is brace counting over column-0 definitions; it is exact on these two
  files (verified: 531-589 / 591-627 / loop 565-571) and would need re-checking before reuse on a
  file with macros that open braces.

## 8. Hygiene

- Wrote only this report at `.ufo/waves/round-53/w1/R53One9.md`. No tracked lane file, no fleet
  file, no sibling/seat directory, no scripts/templates/state/watchdog, no shokuknow write.
- No commit, no jj, no `task`, no background job, no subagent dispatch. Lane repo read-only
  (`git show`, `git ls-tree`, `git rev-parse`).
- No package transaction or query, no install, no live read, no compositor/service/config mutation,
  no screenshot, no input capture, no producer execution. No disk-guard script exists under the
  lane root (`ls scripts/` → no such directory); `df -h /fast` → 591 G free, no ENOSPC.
- Scratch `/fast/scratch/hyaku/mado-r53/R53One9` removed at yield; nothing under `/tmp`.

Report: `.ufo/waves/round-53/w1/R53One9.md`
