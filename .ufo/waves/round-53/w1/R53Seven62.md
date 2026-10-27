# R53Seven62 — revenger: C1 instrument-ledger counter and C2 proposition-bound entry

Seat: `R53Seven62` (revenger, leaf — no subagent dispatch). Wave: round 53, w1, lane `mado-shokunin`.
Axes named: **operability** (C1), **coverage** (C2). Base tip `ad4bf2059bcfafe63671d262222908ee1fe8001c`.
This is a reconstruction report, not a vote: no claim or predicate was edited, no lane/fleet file written,
no axis scored. Every verdict below is `reproduced` / `not reproduced` against the bytes and commands named.

Read first: `SKILL.md` (lane manual), `.ufo/waves/round-53/claims-frozen.md`, the r52 lesson and verifier
spot-check, `quality/counters/c1-r51-ledger.py`, `quality/check-tool-ledger.py`, the r52 entry and its two
surviving counter drafts. No external URL was opened this seat: the only sources touched are committed
repo bytes and the committed `.ufo/waves/round-52/fetch/` pins (registry URL pinned at revision
`efb50993780079460b0cbed1363e2166a2de1d9f`, `corpus/SOURCES.md:319-323`; access date `2026-10-27` as recorded
there; this seat fetched nothing).

## 0. Boundary and method

- Read-only on the lane and fleet: only `git show` / `ls-tree` / `rev-parse` / `cat-file` / `diff` / `sha256sum`,
  plus the committed counters executed against committed revisions. No live read, no compositor/process probe,
  no screenshot, no producer execution, no package query, no install, no git/jj mutation of the lane.
- Fixtures: six throwaway clones of the lane under `/fast/scratch/hyaku/mado-r53/R53Seven62/` (`f1`, `f2`, `f3`,
  `f4`, `f5`, `f6`), each `git rev-parse --show-toplevel` asserted to print itself before any commit; ledger
  bytes replaced, one commit per mutant. These are scratch fixture repos, never the lane; nothing outside
  scratch and this report was written. Disk guard: `/fast` 594 G free at start.
- Scratch removed before yield; `/tmp` unused.

Attacked predicates:

- r53 frozen C1: *"a newly committed, scratch-aware counter with explicit selftest returns TARGET_MET on the
  production ledger, TARGET_MISSED on a no-work control and each frozen forgery fixture, with exact population
  coverage and non-self pointers … bounded structural accountability check, not semantic proof."*
  (`.ufo/waves/round-53/claims-frozen.md:7`)
- r53 frozen C2: *"a frozen counter rejects the old bytes and accepts corrected entry with quote/pin/proposition
  bindings; independent reviewer checks source truth. No claim of expansion credit unless an admitted entry
  rests on a source row opened this round and uncovered ground per coverage map."* (`:9`)
- r52 registration C1/C2 (` .ufo/waves/round-52/registration.md:7,9`) as the predecessor predicates the r53
  targets are written against.

## 1. What was executed (command → observed)

All commands run with the lane as `--repo` and a scratch `--work` unless the fixture repo is the subject.
Digests of every input: §7.

| # | Subject | Command (abridged) | Observed |
|---|---|---|---|
| E1 | C1 green arm, committed r51 pair at base tip | `python3 -I quality/counters/c1-r51-ledger.py --repo <lane> --rev ad4bf205… --work <scratch>/work1` | `detail: checker selftest ok (ratio=50/50 form=with-work)`; `detail: checker ledger ok`; `C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=ad4bf205…`; exit 0 |
| E2 | r51 base absence | same, `--rev 6ca8c559…` | `detail: quality/tool-ledger.md absent at 6ca8c559a4a3`; `C1_R51: verdict=TARGET_MISSED ledger=absent population=79 rev=6ca8c559…`; exit 1 |
| E3 | F1: 82 rows, desc `Generic accountability note <i>.`, production pointers (fixture `f1` @`671ebeb…`) | `--repo <f1> --rev 671ebeb…` | `C1_R51: population=82 ledger_rows=82 … empty_desc=0 selftest=ok verdict=TARGET_MET rev=671ebeb…`; exit 0 |
| E4 | F7: all 82 descs identical `Generic accountability note.` (`f6` @`4e1e430…`) | `--repo <f6> --rev 4e1e430…` | `… empty_desc=0 … verdict=TARGET_MET`; exit 0 |
| E5 | F2: every pointer cell `quality/tool-ledger.md` (the ledger itself), production descriptions (`f2` @`bf22be6…`) | `--repo <f2> --rev bf22be6…` | `detail: checker ledger ok`; `C1_R51: population=82 ledger_rows=82 … bad_pointer=0 … verdict=TARGET_MET`; exit 0 |
| E6 | F3: one row's pointer `quality/alias-anims.md`, a git symlink (mode 120000) whose blob text is `../tools/mado-anims.py` (`f3` @`2d5c8e4…`) | `--repo <f3> --rev 2d5c8e4…`; `git ls-tree` shows `120000 blob … quality/alias-anims.md` | `… bad_pointer=0 … verdict=TARGET_MET`; exit 0 — the row is certified by a pointer to itself through an alias |
| E7 | r52 no-work control `.ufo/waves/round-52/controls/c1-do-nothing.md` as the ledger (`f4` @`1b3756e…`) | `--repo <f4> --rev 1b3756e…` | counter: `C1_R51: population=82 ledger_rows=2 uncovered=81 dangling=0 bad_pointer=1 empty_desc=0 selftest=ok dup=1 checker=failed verdict=TARGET_MISSED`; checker alone: `LEDGER: population=82 ledger_rows=0 uncovered=82 dangling=2 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED`; exit 1 — same bytes, two different measurements, no self-pointer field |
| E8 | Four frozen forgery fixtures (Attack01 controls) as the ledger, one commit each in `f5` | `--repo <f5> --rev <each>` | F-all `305aa9e…`, H2n `f9550f0…`, H3n `f89bef2…`, H4n `fb05eef…`: **all four** `C1_R51: … verdict=TARGET_MET`, exit 0 |
| E9 | W1-reviewed draft `0fe862f1…` (847 L) on the same four fixtures, `--ledger <fixture>` | `python3 -I .ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py --repo <lane> --rev ad4bf205… --ledger <control>` | F-all `TARGET_MET`, H2n `TARGET_MET`, H3n `TARGET_MET`, H4n `generic_desc=1 verdict=TARGET_MISSED` — 1 of 4 caught |
| E10 | Draft on E3/E5/E6 fixtures (`--repo <fixture> --rev <fixture rev> --ledger <fixture ledger>`) | as above | F1: `generic_desc=82 verdict=TARGET_MISSED`; F2: `bad_pointer=82 self_pointer=0 verdict=TARGET_MISSED` (self-reference reported as an unresolvable pointer); F3: `verdict=TARGET_MET` (symlink self-alias accepted) |
| E11 | Scratch refusal, committed pair | `--repo <f6> --rev 4e1e430… --work <f6>/inside-work` | `verdict=TARGET_MET`; `<f6>/inside-work` remains after the run — a scratch dir inside the scored repo is accepted and left behind |
| E12 | C2 W1 draft `55452a3d…` (965 L) on the committed entry | `python3 -I .ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py --repo <lane> --rev ad4bf205… --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md --fetch-root .ufo/waves/round-52/fetch --work <scratch>/wd-c2` | `C2_R52: a ok=1 index_row=…`; `b ok=1 propositions=18 ids=18 forms=table`; `c ok=0 rows_bound=0/18 miss=P01:anchor_no_fetch_root,…`; `d ok=0 quotes_bound=17/18 quotes_raw=6/17 pins=4 … miss=P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)`; `e ok=0 … miss=P01:id_not_referenced,…`; `clauses=abcde clauses_met=2 admitted=0/1 verdict=TARGET_MISSED`; exit 1 |
| E13 | Independent quote/pin census of all 18 rows against `fetch/` (own script, whitespace-collapsed) | `python3 qcheck.py` | 18/18 ≤25 words (max 19, P03); 17/18 contiguous inside the declared pin span and in the file; **P16 false in both**; enclosing definition of every anchor printed (`P07→stringToModMask@221`, `P17→sendkeystate@591`, `P18→sendshortcut@531`, …); **P17 quote is a proper substring of the P04 quote** |
| E14 | P16 clause split | own script, per `;` clause | clause 1 verbatim at `ConfigActions.cpp:1554`; clause 2 verbatim at `:1558` (and again at `:1568`); the **joined cell is contiguous nowhere** and not inside `1554-1558` |
| E15 | P18 loop geometry | print `DispatcherTranslator.cpp:559-580` | `559 if (!g_pKeybindManager->m_keyToCodeCache.contains(KEYPAIRSTRING)) { … 565 for (… ++kc) { … 571 } … 573 if (!keycode) 574 return …"key not found"}; … 577 }` — the return is **after** the loop closes, inside the cache-miss branch |
| E16 | Proposed corrected rows | `python3 verify_corrected.py` | P16a @1554 at-line True; P16b contiguous in span True; P16c @1576 True; P18 @573 (span to 574) True; attribution `enclosing ∈ named` True for all; `ALL True` |
| E17 | Registry digests vs fetch bytes | `sha256sum` of the four fetch files vs `grep -oE 'r52 fetch SHA256 …' corpus/SOURCES.md` | identical sets (`REGISTRY-DIGESTS-MATCH-FETCH-BYTES`); `sha256sum -c fetch/SHA256SUMS` → 5 OK |
| E18 | Population arithmetic | r51 rule over `git ls-tree -r` | `6ca8c559 79`, `85d57a81 82`, `ad4bf205 82`; `r52-counters-at-HEAD=0`; receipts dir holds only `c1-base.txt`, `c2-base.txt` |

## 2. Reconstructed contracts (what the code actually does)

### 2.1 C1 — committed r51 counter (`quality/counters/c1-r51-ledger.py`, sha `d5c2447d…`)

- Population (`:133-149`): every blob under `tools/` plus direct children `quality/*.py` and
  `quality/counters/*.py` at `--rev`, `__pycache__`/`.pyc`/`.pyo` excluded; the ledger itself is not an
  instrument.
- Rows (`:155-175`): unfenced pipe rows; first cell stripped of emphasis; rows without `/` or with a
  separator-only first cell skipped; `desc` = cell 2, `pointer` = cells 3+ joined.
- Pointer (`:177-209`): backticked tokens (else split on `,;`/space), `./` stripped, trailing `:N`/`:N-M`
  stripped, absolute/`~`/`$`/template tokens dropped; a token is a hit iff it is a tracked path **and** the
  blob text contains the row's basename. There is **no** self-reference test, no mode test, no
  population/exclusion test, no line-anchor requirement.
- Description (`:211-249`): counted only when empty after emphasis stripping or matching
  `^[\s\-–—_*`.]+$`. Repeated, template or name-restating text passes.
- Checker clause (`:278-328`): the lane checker at `--checker` (default `quality/check-tool-ledger.py`) must
  print a `LEDGER:` line, its selftest must pass (`n/n` or a `selftest=ok` token), its verdict must be
  `TARGET_MET`, and its six numbers must equal the counter's own. The default checker (`6dd4061c…`) shares the
  same pointer rule (`quality/check-tool-ledger.py:268-328`: `names_basename` over blob text, no mode, no
  self/population exclusion) but parses **exactly three cells only** (`:234-256`).
- Scratch (`:331-347`): explicit `--work` is created and never removed; without `--work` a `mkdtemp` under
  `TMPDIR` is created and removed. `REFUSED_ROOTS` = `/tmp`, `/var/tmp`, `/dev/shm`; nothing refuses a work
  dir inside the scored repo (E11).
- The r51 predicate therefore certifies **coverage + uniqueness + resolvability + non-empty description**, and
  nothing about ownership. That is the last-known-good invariant and it still holds (E1).

### 2.2 C2 — entry shape and the two surviving counters

- Committed entry `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (sha `bee0d143…`, identical at
  `56d6e705` and at base tip): 7-column table `| ID | Proposition | Source row | Pin:anchor | Quote | Support
  class | Why it supports |` (`:11`), pins written as bare fetch basenames
  (`Hyprland-legacy-DispatcherTranslator.cpp:591-594`), with the fetch root declared only in prose (`:30`), no
  `pin` manifest table, no `held:` lines, and the `source:` line naming four S-rows (`:5`).
- The r51 C2 counter (`quality/counters/c2-r51-dispatch-entry.py`, `ebe39e11…`) scores a **different grammar**:
  `source:` lines with `quote`(Pin:123) shapes, a pin-manifest table, `held:` lines, 8-gram shingle overlap
  (`PRED = "PRED-C2-r51"`, `ENTRY = …dispatcher-dispatch-r51.md`, `:56-79`). It is not a candidate for the r52
  entry and does not parse it.
- The r52 W1 draft (`55452a3d…`) is table-shaped but binds anchors under its own declared fetch root and
  demands id-referencing prose and a manifest; it misses the committed entry for shape reasons (E12).
- The 47-line landed r52 counter (`5c7f820…` per `.ufo/waves/round-52/w2/Attack07.md` T1/A01) is **not in the
  tree at any revision** (`git cat-file -e HEAD:quality/counters/c2-r52-proposition-entry.py` → fatal; 0 `r52`
  files under `quality/counters/` at HEAD). I could not re-execute it; I mark that claim `[OBS-report]`.

## 3. Prior-round failure reconstruction

**C1 — last-known-good, then a clause that no implementation can satisfy.**
1. r51 landed a predicate that is *true and green* (E1) and *absent at its base* (E2). Its pointer rule is
   "any tracked file whose bytes name the basename" — a property the ledger itself has 82 times over.
2. r52 registration added "**non-self** pointer … instrument-specific functional context" and a red control
   with repeated generic self-pointers. The frozen sentence is not a tightening of the r51 predicate; it is a
   *new* predicate that the r51 code cannot express. Nothing measured the gap before the wave: the r51 pair is
   green on the very shapes the new predicate forbids (E3–E6), and green on all four frozen forgery fixtures
   (E8).
3. r52's counter draft closed *short* generic filler (E10, F1) and direct full-path self-pointers (misreported
   as `bad_pointer`, E10/F2) but not the class: functional-phrase camouflage (E9, F-all) nor alias self-reference
   (E10/F3). The r52 attack wave reproduced both; the 78-line "landed" rewrite was a different artifact that
   could not even pass green (fenced grammar row parsed as data), had no selftest body and could not report the
   red signals (Attack01 O1–O3) — so no counter was committed (`r52-counters-at-HEAD=0`; E18) and the claim
   honestly stopped.
4. The failure is therefore **not** a defective counter to repair; it is a predicate whose context clause is
   lexical while its target is semantic. Measured: the strongest reviewed draft's context filter accepts three
   of the four frozen semantic forgeries (E9), and a header-bound content-token rule does not separate cleanly —
   the longest shared consecutive content-token run between description and the instrument's own header block is
   `min=1` for production (3 of 82 rows at 1, 10 at 2) and `max=1` for F-all (58 at 0, 24 at 1) on the same
   tokenizer, so threshold `≥2` rejects F-all but fails 3 real rows, and any forger who lifts a two-token header
   phrase passes the same rule. `M52-1` already ordered the fix in words: *"retain the discovered
   forged-description case as an explicit counter limitation … do not call the C1 signal semantic
   accountability"* (`corpus/lessons/round-52.md:21`).

**C2 — a green counter for one entry shape reused against a different entry shape.**
1. Last-known-good: the r51 counter is green against the r51 entry and its base-absence control (report §2.2).
2. r52 changed the artifact shape (7-column proposition map, prose pin root, no manifest/held lines) without a
   counter that parses it. The landed 47-line counter's row regex expected `| P## | S### | …` while the table is
   `| P## | Proposition | S### | …` → `props=0` at any revision containing the entry (E12 is the surviving
   draft's analogue; the shape fact is readable from the entry header itself).
3. Because no counter ran green before commit, the three proposition defects went in with the index row:
   P16 spliced (E13/E14), P17 wrong subject and duplicate of P04 (E13), P18 wrong localization (E15). The
   r52 lesson's `## Gate` carries no per-row record for S370–S373 and `## Changes` still says "Pending final
   integration revisions and receipts" (`corpus/lessons/round-52.md:5-17,23-25`), so the lesson cannot carry the
   admission either.

## 4. Divergences (reconstructed)

Severity is the lane's S1–S3 scale applied to the instrument/entry surface (r52 closure graded quality
`harmed`; nothing here is a host behavior claim).

| ID | Divergence | Evidence | Sev | Conf |
|---|---|---|---|---|
| D1 | The r51 pointer rule has no self-reference test; the ledger is a valid evidence target for its own rows. | code `:196-209`; E5 (82/82 `TARGET_MET`) | S2 | [OBS] |
| D2 | Description accountability is emptiness only; 82 repeated/identical generic descriptions pass. | `:247`; E3, E4 | S2 | [OBS] |
| D3 | Git symlink blob text is accepted as evidence (mode 120000 ignored): a pointer to an alias of the row's own instrument passes counter **and** checker. | code `:206`/`names_basename`; E6 | S2 | [OBS] |
| D4 | The frozen r52 red control does not isolate its defect classes: counter and checker measure different ledgers (2 vs 0 rows) and neither reports a self-pointer class. | E7 | S2 | [OBS] |
| D5 | All four frozen forgery fixtures are certified accountable by the committed pair. | E8 | S2 | [OBS] |
| D6 | The W1-reviewed draft catches only H4n of the four; F-all/H2n/H3n pass. | E9 | S2 | [OBS] |
| D7 | No lexical context rule separates production from F-all at any threshold that keeps production green (measured run-length distribution). | §3.4; own measurement | S2 | [OBS]/[INF] |
| D8 | `--work` inside the scored repo is accepted and left behind. | E11 | S2 (hygiene) | [OBS] |
| D9 | The counter's checker-agreement clause binds it to the committed checker, which shares D1–D3; a corrected counter would disagree with it on every red fixture and could not be green. | code `:302-328` + `check-tool-ledger.py:268-328` | S2 | [INF] |
| D10 | C1 and C2 are not operationally independent: each new counter is a population file. One counter → population 83; both → 84; the ledger must carry both rows at the final commit or the green arm misses on `uncovered=1`. | E18 arithmetic + `:133-149` | S2 (sequencing) | [OBS] |
| D11 | The r52 entry's table is 7-column with `Proposition` in cell 2; a positional `| P## | S### |` parser yields zero rows — the landed counter could not parse its own target. | entry `:11`; E12 shape; Attack07 A01 [OBS-report: bytes absent at HEAD] | S2 | [OBS]/[OBS-report] |
| D12 | No r52 C1/C2 counter is committed at base tip and receipts are base probes only; no green receipt exists for any revision containing the entry. | E18; `ls .ufo/waves/round-52/receipts/` | S2 | [OBS] |
| D13 | P16's quote cell is a splice: each clause is verbatim at its own line (1554 / 1558), the cell as written is contiguous nowhere, and the elided `m_passPressed == 1` / `!isMouse` guard makes the shown PRESSED call branch-conditioned. | E13, E14 | S2 | [OBS] |
| D14 | P17's quote is a strict substring of P04's quote at the identical pin `:619-622`; the anchor lies inside `sendkeystate` (591-627) while the proposition names `sendshortcut` (531-589). | E13; `DispatcherTranslator.cpp:531,591,619-622` | S2 | [OBS] |
| D15 | P18's "inside the scan" is false: the return at `:574` executes after the loop closes at `:571`, inside the cache-miss branch (559-577). | E15 | S2 | [OBS] |
| D16 | The r52 lesson's `## Gate` has no per-row record for S370–S373 and `## Changes` is stale — the routed defects 1–2 are still open at base tip. | `corpus/lessons/round-52.md:5-17,23-25` | S3 | [OBS] |
| D17 | P15's change-clause ("before changing it") still rests outside its quote/pin (`:612` only; writes at `:614-617`, restore `:624`), a routed residual of the same class as P16–P18. | E13 table; `DispatcherTranslator.cpp:612-624` | S3 | [OBS] |

## 5. Minimal corrected contract

### 5.1 C1-r53 — accountable instrument ledger (operability)

Frozen predicate sentence to register before data (the only reading of the r53 target that is internally
coherent with its own "not semantic proof" bound):

> `C1_R53:` `python3 -I quality/counters/c1-r53-ledger.py --repo <lane> --rev <rev> --work <abs-scratch>`
> exits 0 with final line `C1_R53: population=<P> ledger_rows=<P> uncovered=0 dangling=0 bad_pointer=0
> self_pointer=0 dup=0 empty_desc=0 selftest=<n/n> fixtures=<k/k> verdict=TARGET_MET rev=<sha>`, where `P` is
> the r51 population at `<rev>` plus the new counter itself; every population file has exactly one unfenced
> row; every row's pointer is a tracked **non-population, non-ledger** file at `<rev>`, reached by a
> `path:line` anchor that exists and names the row's basename on the anchored line; no pointer is a
> self-reference under normalized identity; no pointer target is a symlink blob; descriptions are non-empty,
> non-placeholder, not a restatement of the row's own name, and pairwise distinct. At `6ca8c559…` the same
> command prints `verdict=TARGET_MISSED ledger=absent` and exits 1.

Counter clauses (each mechanically checkable; anchors are the r51 functions they replace/extend):

1. **Population** (`:133-149`, unchanged): tree-derived, blobs only, direct children only; never the ledger.
2. **Rows** (`:155-175`, unchanged): fence-aware; exactly three cells; exact path identity; `dup=0`.
3. **Non-self pointers** (new, closes D1/D3): normalize the token (strip `./`, leading `/`, collapse `//`,
   casefold, strip `:N`/`:N-M`, strip trailing punctuation inside the backticks), then self iff it equals the
   ledger path, the ledger basename, or the row's own path/basename. Target must be a non-population file
   (a peer instrument is not accountability) and its git mode must not be `120000` (reject or resolve, never
   read the blob text as evidence). Require at least one `:line` anchor; the anchored line must name the
   basename (`names_basename` semantics). This is Attack02's "smallest safe correction" plus the anchor and
   population exclusions the r52 draft lacked.
4. **Description** (`:247`, extended): non-empty; not placeholder; not name-restatement (all content tokens
   drawn from the row's path/basename); pairwise distinct after normalization. **No semantic check.** The
   counter prints `limitation=semantic_desc_not_checkable` and cites `M52-1`.
5. **Checker clause** (`:302-328`, narrowed): `quality/check-tool-ledger.py` must be updated in the same commit
   to clauses 3–4 (it is the same population row, so population is unchanged); then the counter compares the six
   fields and the verdict exactly as today. If the checker is not updated, drop the clause — do not ship a
   counter that disagrees with the tree's own gate on every red fixture (D9).
6. **Scratch** (`:331-347`, tightened): `--work` required, absolute, refused when its realpath is inside the
   scored repo or a refused root; clone and child sandbox env (`HOME`, `TMPDIR`, `XDG_*`) under it; remove what
   the run created; no ambient `TMPDIR` steering; measurement writes only under `--work`.
7. **Selftest** (`checker_selftest` analogue, made real): builds a fixture repo and asserts, with red/green
   receipts, at least: accept (production at a commit containing the counter), reject-absent (`6ca8c559`),
   reject-uncovered, reject-dangling, reject-dup, reject-empty, reject-placeholder, reject-name-restatement
   (H4n shape), reject-self in ≥6 spellings (full path, basename, `./`, `//`, case, trailing `)`, `:x` suffix),
   reject-symlink-alias (mode 120000), reject-peer-pointer, reject-parrot-checker (numbers agree, verdict
   differs), reject-work-inside-repo (exit 2), fence-not-a-row, and **limitation-accept**: F-all shape →
   `TARGET_MET` with the limitation token.
8. **Fixture manifest**: the required-miss set is the **structural** mutants above plus H4n (name-restatement).
   F-all, H2n and H3n are ceiling fixtures: the contract requires them to be *reported accepted* and bound to
   `M52-1`. If the registration instead requires F-all to miss, the claim is falsified in advance: the strongest
   reviewed draft passes it (E9), and the only threshold found that rejects it also rejects real rows (§3.4) and
   is defeated by lifting a header bigram. Registration must enumerate the fixture set by path — "each frozen
   forgery fixture" is ambiguous between the semantic set (`w2/Attack01/controls/*`) and the structural set
   (`w2/Attack02` probes, `controls/c1-do-nothing.md`). The red controls must also be three-cell ledgers: the
   frozen 4-cell `c1-do-nothing.md` is `dangling`/malformed on any 3-cell parser (E7), so it cannot isolate a
   self-pointer or description defect — one defect per one-difference mutant, everything else production bytes.
9. **Sequencing / fixed point** (D10): the ledger must gain the row for every new counter committed in the same
   commit; the C1 and C2 green arms must be measured at a tip that contains both counters (population 84) or the
   registration must scope each claim to its own commit. `claims-frozen.md` calls C1 and C2 "causally separate";
   this is a mechanical coupling, not a causal one, and must be frozen explicitly.

### 5.2 C2-r53 — repair of the three proposition-grounding defects (coverage)

**Entry repair, append-only** (base table untouched; the block appended to the same file keeps the index row and
avoids the novelty/overlap clause a second entry would face). Verified against `fetch/` by E16:

```
## Errata (round 53, append-only; supersedes P16, P17, P18)

| ID | Proposition | Source row | Pin:anchor | Quote (<=25 words) | Support class | Why it supports | Supersedes |
|---|---|---|---|---|---|---|---|
| P16a | The action sends the modifier mask to the seat before the key-event branch. | S371 | Hyprland-ConfigActions.cpp:1554-1558 | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);` | direct | Line 1554 precedes the branch at 1556; the pin span carries the order. | P16 |
| P16b | The PRESSED key event is sent only when `m_passPressed` is 1 and the input is not a mouse button. | S371 | Hyprland-ConfigActions.cpp:1556-1558 | `if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` | direct | The guard text and the call appear contiguously in the quote. | P16 |
| P16c | The action clears the modifier state after the key-event branch. | S371 | Hyprland-ConfigActions.cpp:1576 | `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` | direct | Line 1576 follows the branch 1556-1574; the quote is the clear call. | P16 |
| P17 | Withdrawn: the base quote duplicates P04 at the identical pin, and its subject (`sendshortcut`'s repeat branch) is false — `:619-622` lies in `sendkeystate` (:591-627). | S370 | — | — | withdrawn | Duplication proof: the base P17 quote is a proper substring of the P04 quote at pin :619-622. | P17 |
| P18 | In `sendshortcut`, a keyboard-range scan that leaves `keycode` 0 reaches a guard returning the `key not found` error. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:565-574 | `if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};` | direct | The quote is the post-scan guard; the pin span carries the loop (565-571) that leaves `keycode` 0. | P18 |
```

Word counts of the repaired quotes (whitespace-split): 4 / 12 / 4 / 0 / 12. Each is contiguous in its span (E16). P13's quote is a
substring of P16b's, so the duplicate rule must be *same source row AND same pin span AND one quote contained in
the other* — that rejects old P17/P04 (`:619-622` both) and spares P13 (`:1558` vs `:1556-1558`).

**Frozen counter predicate sentence to register before data:**

> `C2_R53:` `python3 -I quality/counters/c2-r53-proposition-entry.py --repo <lane> --rev <rev>` exits 0 with
> final line `C2_R53: props=<n> rows_bound=<n> quotes_bound=<n> dup_quote=0 attr=<n> pins_verified=<n>
> old_bytes=REJECT new_bytes=ACCEPT verdict=TARGET_MET rev=<sha>` iff, at `<rev>`: the entry is indexed;
> the table is parsed **by header name**; every row's `Source row` exists in `corpus/SOURCES.md` with status
> `mined`, the recorded date and a pin whose sha256 equals the blob's; every `Quote` cell is ≤25 words and
> contiguous (whitespace-collapsed) inside one declared span of its pin; no two rows share (row, pin span) with
> one quote contained in the other; every function name the proposition asserts is the enclosing definition at
> the anchor; rows superseded by the errata block are not scored on quote truth; and no row is withdrawn
> without a named duplicate. At `56d6e705bf9113dce0dabd5d4a7ed8e610e1a940` the same command prints
> `verdict=TARGET_MISSED` with `P16:quote_not_contiguous` and `P17:dup_quote` and exits 1.

Accepted/rejected controls for its selftest: accept = corrected tip; reject = `56d6e705` (old bytes, both
defects); reject = fabricated quote at a real pin (Attack07 T6 shape); reject = pin digest mismatch; reject =
proposition naming a function other than the anchor's enclosing definition; reject = index row absent; reject =
registry row not `mined`. Exit map 0/1/2 (setup). Scratch rules as §5.1.6.

**Independent reviewer step** (not automatable, and the freeze says so): P18's localization and P16's branch
materiality are source-truth judgments; the counter rejects the old bytes on P16-contiguity and P17-duplication,
which is sufficient for "rejects the old bytes", but admission still needs the non-author sentence-to-pin review
(QUALITY 104). No seat counts as that reviewer.

**Axis effect (coverage).** The repaired entry adds no `S###` row and no `covers: U#` line; under the lane's
coverage sub-axis rubric (`SCORECARD.md:247`) a note is covered only when it opens with a `source:` line citing
a `mined` row *and names the U-item* — `grep -c '^covers: U[1-7]'` is 0 for this entry while 6 knowledge files
carry one. So C2-r53 restores an indexed-but-unadmitted entry; it earns no expansion delta, and the frozen
"no expansion credit" clause is already satisfied by construction. C1-r53 earns operability only.

**Routed r52 defects also evidence-checked (not repaired here):** D16 (Gate records absent, `## Changes` stale)
and D17 (P15 quote gap) remain open at base tip; D17's fix is the same one-row/one-contiguous-excerpt rule.

## 6. Not established / limits

- The 47-line landed r52 counters (`c1-r52` sha `923faf02…`, `c2-r52` sha `5c7fb820…`) are absent from the tree
  at every revision; my statements about them are `[OBS-report]` from committed attack reports, not executed
  here. I did not reconstruct their bytes from `__pycache__` (present only for the W1 drafts) — inference from
  compiled scratch would be weaker evidence than the reports already in the record.
- E9/E10 were run against the lane at base tip with `--ledger` naming fixture bytes; the draft resolves
  instruments and pointer targets at `--repo/--rev`, so F2/F3 were re-run with the fixture repo as `--repo` to
  give the aliases a real existence at the measured rev (E10). F1's ledger is a fixture rev; no result depends on
  an unpublished revision.
- The header-binding measurement (§3.4) uses a stated tokenizer (lowercase `[a-z0-9]+`, length ≥4, a fixed
  stopword list, first docstring or leading comment block as the header). Another tokenizer moves the numbers;
  the direction (production spans 1–9, F-all 0–1) is what the conclusion uses, and it is an `[INF]` on top of
  `[OBS]` inputs.
- No axis score was computed; SCORECARD was read only for the rubric text and the r52 record.
- Working-tree note at yield: the lane carried sibling/orchestrator edits (`M corpus/SOURCES.md` adding a S374
  row, `?? corpus/lessons/round-53.md`). No measurement here reads them; the entry was byte-identical to the
  committed blob (`bee0d143…`) when opened, and every counter run resolved bytes by `--rev`.
- No non-author judgment is claimed by this seat, and no capability is admitted.

## 7. Input digests (sha256) and revisions

`quality/tool-ledger.md` `df5b3705…` · `quality/check-tool-ledger.py` `6dd4061c…` ·
`quality/counters/c1-r51-ledger.py` `d5c2447d…` · `quality/counters/c2-r51-dispatch-entry.py` `ebe39e11…` ·
entry `bee0d143…` (== `git show 56d6e705:corpus/knowledge/hyprland-synthetic-dispatch-r52.md`) ·
`corpus/lessons/round-52.md` `4a81e934…` · Attack01 controls F-all `d793c9ef…`, H2n `859e45ed…`, H3n
`92ed1e46…`, H4n `86e953ee…` · `controls/c1-do-nothing.md` `ad72f72f…` · W1 C1 draft `0fe862f1…` · W1 C2
draft `55452a3d…` · fetch SHA256SUMS verified 5/5 OK. Revisions: `6ca8c559` (r51 base, 79), `85d57a81` (r52
base, 82), `56d6e705` (r52 landing), `ad4bf205` (r53 base tip, 82). Fixture revs are run-local (E3–E8).

## 8. Trailer

- Report: `.ufo/waves/round-53/w1/R53Seven62.md` (paths relative to lane root `mado-shokunin/`).
- Scratch `/fast/scratch/hyaku/mado-r53/R53Seven62` — fixture clones `f1`–`f6`, work dirs, `qcheck.py`,
  `hdr.py`/`hdr2.py`, `verify_corrected.py`, digest lists — removed on yield; nothing written outside it and
  this report.
- No tracked lane/fleet file, sibling path, script/template/state/watchdog, or shokuknow write; no git/jj
  mutation of the lane; no task/delegation/background job; no package query, install, or pacman transaction;
  no live read, probe, capture, screenshot, or producer execution; source repo read-only.
- Tooling: preinstalled `python3`, `git`, `sha256sum`, `diff` only; nothing installed, so `/home/vgpnk/.omp/agent/RULES.md`
  was not needed for an install and is not claimed as read for this seat.
