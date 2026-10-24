# RevRecordsChain — round-30 landed-chain review (records + claim machinery)

Seat: reviewer, records chain. Lane `mado-shokunin`, base `8f51071b`, reviewed
tip `master` = `15ddd7d`. Read-only: this seat wrote nothing except this report
(no lane file, index or jj state touched; counters/gate re-run against committed
bytes only).

**The chain moved during this review.** My first pass measured
`8f51071b..92d3c86` (3 commits). While I worked, three more commits landed:
`d72243e` and `2db0c44` (non-author integrator spot-checks, `protocol-shokunin`)
and `15ddd7d` ("w1 addendum: gate repair, receipts, lesson+scorecard errata,
seat reports", `mado-shokunin`). Everything below is re-measured at `15ddd7d`;
the retracted findings in §6 name what the extended chain resolved.

Tooling note: **no LSP device is mounted in this session** (`write xd://lsp` →
"No such tool: xd://lsp. Mounted devices: ast_edit, debug"). Caller/definition
checks were done by reading both changed Python artifacts in full plus live
re-runs; `grep` below is only literal-string/quote verification, never semantic
proof of a caller relation.

## Verdict

The chain is **scoped, linear and authorship-honest**, every cited hash resolves,
and every measured fraction reproduces from committed bytes — including under the
repaired gate. **No unrelated change.** Findings F1–F3 are record defects: one
receipt that is a tail rather than the full output the round claims, one
superseding criterion that silently drops a normative clause behind a "verbatim"
assertion, and one post-freeze instrument rewrite whose repair receipt does not
bind its tool to any measured commit. All are recommendations; nothing here is an
admission or verdict.

## 1. Chain shape, authorship, scope — verified at `15ddd7d`

`git log --oneline 8f51071b..master`:

```
15ddd7d round-30 w1 addendum: gate repair, receipts, lesson+scorecard errata, seat reports   mado-shokunin
2db0c44 round-30 verifier spot-check addendum (integrator, hyaku): wave-1 digest, routed defects  protocol-shokunin
d72243e round-30 verifier spot-check (integrator, hyaku): non-author admit/reject           protocol-shokunin
92d3c86 round-30 records: receipts, wave spec, LOG, SCORECARD                               mado-shokunin
446dc39 round-30 data: index rows, criterion grounding, S185, lesson                        mado-shokunin
451e8b3 round-30: freeze registration, counters, index gate, controls                        mado-shokunin
```

- **Linearity**: 451e8b3c←8f51071b, 446dc396←451e8b3c, 92d3c86←446dc396,
  d72243e←92d3c86, 2db0c44←d72243e, 15ddd7d←2db0c44. No merge.
- **Cited hashes**: `git merge-base --is-ancestor` true for both `451e8b3c`
  (freeze) and `446dc396` (data); each authored *and* committed by
  `mado-shokunin <mado@shokunin.local>`. `d72243e`/`2db0c44` are
  `protocol-shokunin <protocol@shokunin.local>` (the non-author integrator, as
  declared in their message and in `corpus/lessons/round-30-verifier-spotcheck.md`).
- **Scope**: cumulative name-only diff is now 55 paths — all under
  `.ufo/waves/round-30/`, `corpus/`, `quality/check-index.py`, `LOG.md`,
  `SCORECARD.md`. The filtered command printing everything *outside* those
  prefixes prints nothing.
- **Protected subtrees byte-untouched across the full range**:
  `git diff --stat 8f51071b master -- .ufo/waves/round-29/ tools/ corpus/knowledge/ SKILL.md PROVINCE.md`
  is empty (so C1's "no knowledge bytes changed" and the registered harm watch
  hold at the extended tip too).
- **Data targets unchanged after the data commit**:
  `git diff --stat 446dc396 master -- corpus/QUALITY.md corpus/README.md corpus/SOURCES.md`
  is empty — the objects C1/C2 measure are still the measured bytes at tip, and
  `c2/count.py master` still prints `TARGET_MET`.
- **Append-only, except one declared rewrite**:
  - `corpus/QUALITY.md @@ -334,3 +334,25 @@`, `corpus/README.md @@ -50,6 +50,8 @@`,
    `corpus/SOURCES.md @@ -194,6 +194,7 @@`, `LOG.md @@ -1774,3 +1774,56 @@`,
    `SCORECARD.md` (+38, then +33 — both EOF appends),
    `corpus/lessons/round-30.md` (+56, then +20 — append), new
    `corpus/lessons/round-30-verifier-spotcheck.md` (+109, +58 append).
  - **`quality/check-index.py` is the one non-append change**: `+122/−31` in
    `15ddd7d`, rewriting the blob the freeze committed
    (`df01b20f…` → `0c13f39…`). This is disclosed as a same-round erratum
    (`SCORECARD.md:1939-1968`) and is analysed in F3.
- **Freeze immutability, narrowed**: `registration.md` (110 lines) and
  `c2/count.py` (195 lines) are still byte-identical to `451e8b3c` (same blob
  ids, empty diff); the gate is not, as above.
- **q36 drift reverted in-chain**: the worktree `M quality/q36-successor-receipts.txt`
  I saw mid-review is gone; `git diff --stat 92d3c86 master -- quality/q36-successor-receipts.txt`
  is empty, and the SCORECARD erratum records the revert.
- **Working tree now**: clean except untracked seat reports
  (`RevC2Counter.md`, `RevRecordsChain.md`, `ScribeRecords.md`).

## 2. Classification of every change

| Path | Commit(s) | Class | Note |
|---|---|---|---|
| `registration.md` | freeze | claim-machinery | frozen spec; unchanged after freeze |
| `.ufo/waves/round-30/c2/count.py` | freeze | claim-machinery | C2 counter; unchanged after freeze |
| `quality/check-index.py` | freeze **+ addendum** | claim-machinery + shipped capability | capability is the C3 deliverable; rewritten in `15ddd7d` (F3) |
| `controls/C2K1-donothing.txt`, `C3K1-base-red.txt`, `C3K2-selftest.txt` | freeze | claim-machinery (controls) | `C2K1` byte-identical to `c2-before`; `C3K1/K2` match live runs |
| `evidence/c1-before`, `c2-before`, `census-before` | freeze | record | pre-data receipts |
| `corpus/README.md` | data | record / measured substrate | 2 index rows (C1 object); row B content defect F6 |
| `corpus/QUALITY.md` | data | record / rubric substrate | rows 41–52 + preamble (C2 object); row 48 defect F2 |
| `corpus/SOURCES.md` | data | record | +S185 |
| `corpus/lessons/round-30.md` | data + addendum | record | M30-1/M30-2, Gate, then w1 addendum |
| `corpus/lessons/round-30-verifier-spotcheck.md` | d72243e, 2db0c44 | record (non-author) | integrator admit/reject + wave-1 digest |
| `evidence/{c1,c2,c3}-after-446dc396.txt`, `census-end.txt`, `freeze-smoke-451e8b3c.txt` | records | record | post-data receipts (F1 applies to the last) |
| `evidence/c3-repair-d72243e.txt` | addendum | record (repair receipt) | F3 applies |
| `w1-plan.json`, `w1-spec.json`, `w1/reports/swarm-registry.json` | records / addendum | claim-machinery (wave) | 33 items/members; registry names/roles equal spec |
| `.ufo/waves/round-30/w1/reports/*.md` (27 reports) | addendum | record (wave evidence) | seat findings; artefacts used here as data |
| `LOG.md`, `SCORECARD.md` | records + addendum (SCORECARD only) | record | SCORECARD carries the C3 erratum; **LOG does not** (F3b) |
| **unrelated** | — | **none** | 0 paths outside the declared set |

## 3. Findings (severity order)

### F1 — High. The freeze-smoke receipt's C2 leg is a tail, not "full output"

`.ufo/waves/round-30/evidence/freeze-smoke-451e8b3c.txt:5-9` holds five C2 lines
(`--- C2 at freeze ---`, `UNRESOLVED criterion 39`, `UNRESOLVED criterion 40`,
`LINE 20 superseded excluded`, `verdict=TARGET_MISSED`). A live re-run at the same
revision prints **14** lines: `counter=` header, three `METRIC` lines (literal
28/40, `superseded=[20]`, `active=39 resolved_active=31`), **eight** `UNRESOLVED`
criteria (1–5, 38, 39, 40), `LINE 20 …`, verdict, and `EXIT=1`. The receipt
therefore hides 6 of 8 unresolved criteria and *all* tallies, and unlike the C1/C3
legs (`:4`, `:14`) carries no `EXIT`. The addendum did **not** correct it.

Why it matters: the round invokes its own criterion 49 for exactly this artifact
(`LOG.md:1810-1811` "print real tallies"; `registration.md:86-88` "the composite
smoke rule (criterion 49) is satisfied by running all three at their freeze
commit"), and criterion 49 (`QUALITY.md:355`) requires "its **full output** is
committed". The missing lines do not contradict the complete pre-data receipt
(`c2-before-8f51071b.txt`), so the defect is evidence completeness, not
measurement. Fix: replace the C2 section with the full 14-line output including
`EXIT=1`; keep the old receipt as an erratum.

### F2 — High. Row 48 is not "verbatim": it drops a normative clause (and the claim has propagated)

`corpus/QUALITY.md:338-346` asserts "Each superseding row below restates its rule
**verbatim**". Base criterion 32 is one 861-byte line whose final sentences are:

> Ground: lesson round21 M13, `residual/FinalBindingReview.md` F1–F5 and its six
> inert fixtures. **This criterion is added after final falsification, supplies no
> retroactive pass and no numeric C2/criterion-count credit; delivered C1 fails it
> and remains harmed.**

Tip row 48 (`QUALITY.md:354`, complete at 793 bytes, balanced parentheses) keeps
the rule sentences verbatim and folds the Ground pointer into its citation, but
the second sentence above is **absent**. That sentence is an accounting
constraint ("no numeric C2/criterion-count credit") — exactly the anti-inflation
clause that should stay in force when a round grows the criterion population
(39 → 40 active, 40 → 52 lines) and claims C2 credit from it.

Rows 46, 47 and 49–51 are different in kind and acceptable under the claim: 46 is
normalized-identical to base 18 (checked programmatically); 47 keeps 19's numbered
rule and only turns the "outside R13-V1" tag into a resolvable path; 49–51 drop
only parenthetical *evidence instances* (`count.py:100` pin, H1 receipt,
`ref-chk-*` survivors) while preserving every rule and check sentence. Row 48 is
the sole case where normative text leaves the active rubric.

Propagation: the non-author record repeats the false claim — `round-30-verifier-spotcheck.md`
("Claim re-checks", C2 row) says "rows 41–51 supersede 1–5/18/19/32/38–40
**verbatim**". Fix: append the dropped sentence to row 48 (append-only), and
correct the verifier record's wording.

### F3 — High. The frozen gate was rewritten post-data and the repair receipt does not bind its tool to a measured commit

(a) **Instrument mutation after freeze.** `registration.md:86-88` freezes the
gate in the pre-data commit; C3's receipts at `446dc396` were produced by blob
`df01b20f…` (content sha256 `fc4a10a2…`, selftest 6/6). `15ddd7d` rewrites it to
blob `0c13f39…` (content sha256 `373680fe…`, selftest 8/8). The rewrite is
**disclosed** (SCORECARD erratum `:1939-1968`; lesson w1 addendum) and does not
move any predicate — I reproduced base red `41/43` exit 1, data and `d72243e`
green `43/43` exit 0, `8/8`, bare invocation `SETUP_ERROR` exit 2 — but the
round's own new criterion 52 (`QUALITY.md:358`) says a discovered gap's repair is
"a declared claim **with its own counter**, never a silent patch inside the
discovering round's sweep row". This repair is not silent, yet it is not a
declared claim with its own predicate either; it lives inside C3's erratum and
changes C3's instrument mid-round.

(b) **The repair receipt fails criterion 24's binding.** `evidence/c3-repair-d72243e.txt`
labels its header `=== gate sha256 (repaired) ===` with `373680fe…` — true of the
gate at `15ddd7d`/master only — while every revision the receipt measures
(`8f51071b`, `446dc396`, `d72243e`) carries `sha256
git show <rev>:quality/check-index.py` = `fc4a10a2…`. Criterion 24
(`QUALITY.md:131`) requires a receipt's bytes to name its producer with
`tool_sha256=` equal to `git show <measured_commit>:<tool> | sha256sum`, plus a
`measured_commit`. The receipt has neither the label nor a `measured_commit`, so
under the only reading where the listed revisions are "measured" the equality
fails; under the reading where the tool's own commit is the measured one, the
receipt does not say so. Fix: add `tool_sha256=`/`measured_commit=15ddd7d` fields
and label the three revisions as data-under-test.

### F4 — Medium. The seed-five "grounding" cites the defect row about itself

Rows 41–45 (`QUALITY.md:347-351`) cite `lessons/round-30.md#mistakes M30-1`,
whose only content (`lessons/round-30.md:13`) is the finding that criteria 1–5 had
no lesson citation, plus `MINT.md`. `MINT.md` is real and supports row 41's
description (two numbered demand instances; "No province absorbs the compositor
config plane", `MINT.md:3-16`) — checked, not fabricated. But 5 of 40 active
criteria now "resolve" through the audit row that records their own defect. The
preamble discloses this ("its grounds are `MINT.md` … and … M30-1"), so it is not
concealment; the defect is the metric's name: C2 measures **citation
resolvability**, not lesson derivation. The round report should state that limit
instead of letting "lesson-grounded admission criteria" imply otherwise.

### F5 — Medium. S185's "verbatim" located quote is a paraphrase; its pinned hash is serialization-specific

`corpus/lessons/round-30.md:24` presents as a "located quote (≤25 words,
verbatim)":

```
revision=$rev indexed=$covered/$total missing=$missing dangling=$dangling duplicates=$duplicates coverage=$score/10
```

That string occurs **nowhere in `SCORECARD.md`** (grep over all `*.md`: only the
lesson contains it). The source line, `SCORECARD.md:84`, is an f-string:
`print(f"revision={rev} indexed={covered}/{len(notes)} missing={len(missing)} …
coverage={10*covered/len(notes):.4f}/10")`. The Gate protocol requires a verbatim
located quote, so this is a schematic rendering. The pinned digest
`8b59b503805396b5…` **does** resolve, but only under one of five serializations I
tested — the fence *inner* bytes including the trailing newline; the row does not
name the serialization. The non-author spot-check reached the same conclusion
("schematic rendering … not byte-exact") and routed it to round 31. Fix: restate
the quote as the literal `MADO_INDEX:` output line or the literal f-string, and
name the hash's byte range.

### F6 — Medium-Low. The C1 row for `mutation-testing-r28.md` over-compresses its note

The Holds cell says "a survivor is a suite limitation, not a real-fault verdict"
and "equivalent mutants bound the denominator". The note
(`corpus/knowledge/mutation-testing-r28.md:20`) says a survivor is "evidence that
the tested suite did not distinguish that mutant **under the gate's
observations**; it is not, by itself, proof of a real defect", and that equivalent
mutants "can appear as survivors" if included, while exclusion "affects the
denominator". I read both first-hand: the row drops the scope qualifier and
states the equivalence clause one-sidedly (F2/F3 of
`w1/reports/ScribeRowAccuracy.md`, whose reasoning I reproduce). The fence counts
the row either way, so C1's `43/43` is blind to cell content — the README's
Quality bar already says rows are routes, not truth, so this is a content defect
in a row the data commit added, not a false measurement. Routed to round 31 by
the spot-check; an append-only row correction is the repair.

### F7 — Low. The lesson addendum's seat-report count is wrong at its own commit

`corpus/lessons/round-30.md` w1 addendum: "24 seat reports land under
`.ufo/waves/round-30/w1/reports/`". Commit `15ddd7d` itself contains **27** `.md`
reports plus `swarm-registry.json` (28 files); the spot-check's digest counted 21
untracked at its earlier write. Dated prose about a growing directory, but it is
stale as committed. Either give the number a revision ("27 at `15ddd7d`") or drop
it.

### F8 — Low. "misroot sweep clean" still has no committed receipt

`LOG.md:1820` and `SCORECARD.md:1924-1928` end the harm watch with "no
compositor/config mutation; misroot sweep clean". Every other harm-watch item
names a command or receipt; this one names neither, and no misroot receipt exists
in `evidence/` or in the addendum. The lane half is corroborated by the diff (0
paths outside the write set); the fleet-root sweep is not verifiable from the
chain. Criterion 42 applies: commit the sweep output or drop the claim.

### F9 — Low. Counter block attribution: trailing section prose binds to the last criterion

`c2/count.py` runs each criterion's text from its numbered line to the next
numbered line with no heading awareness, so the new `## Grounding repair` heading
and preamble (`QUALITY.md:338-346`) belong to **criterion 40's** text. Harmless
here only because 40 is superseded and out of both fractions. Future vector: a
concrete `lessons/<file>.md` path appended after the last *active* criterion makes
that criterion "resolve" without a citation on its own line (literal stays red,
resolved flips green). Heading-aware blocking would remove the free-text vector;
the per-line literal vs per-block resolved asymmetry is deliberate and frozen.

### F10 — Low. Registration arithmetic wording is off by one (frozen; note only)

`registration.md:60-62`: "12 lines superseded by rows 41–51, +1 new criterion 52".
Rows 41–51 supersede **11** lines (1–5, 18, 19, 32, 38–40); the twelfth is 20
(by criterion 21, as the same document says). Landed arithmetic is correct —
52 − 12 = 40 — and the counter's superseded set equals `SCORECARD.md:1915`'s.

## 4. Claim numbers reproduced

All run against committed bytes; receipts match byte-for-byte except F1.

| Measurement | Command | Result |
|---|---|---|
| C2 at base | `python3 -I .ufo/waves/round-30/c2/count.py 8f51071b` | `literal 28/40`, `superseded=[20]`, `active=39 resolved_active=31`, UNRESOLVED {1–5,38,39,40}, `TARGET_MISSED`, exit 1 |
| C2 at data | `… count.py 446dc396` | `literal 40/52`, `active=40 resolved_active=40`, `TARGET_MET`, exit 0 |
| C2 at master | `… count.py master` | `TARGET_MET` (data files unchanged after `446dc396`) |
| C2 at freeze | `… count.py 451e8b3c` | 14 lines with METRIC tallies and `EXIT=1` — receipt has 5 (F1) |
| C3 gate at base/tip (frozen blob) | `quality/check-index.py --rev 8f51071b/446dc396 --repo .` | 41/43 exit 1; 43/43 exit 0; `--selftest` 6/6 |
| C3 gate (repaired blob) | same + `--rev d72243e`, `--selftest`, bare | 41/43 exit 1; 43/43 exit 0 at data and d72243e; 8/8; bare → `SETUP_ERROR` exit 2 |
| Harm watch | `bash tools/mado-verify.sh --selftest` | `MADO_SELFTEST: 460/460`, exit 0 (18 s) |
| Sources | recount tiers/status both revs | 184→185 rows; A 177→178; mined 165→166; queued 10; rejected 9; no dup ids |
| Coverage map | row extraction at master | 43 index rows; r26 row has **2 cells** (no Sources cell) |
| Wave registry | spec vs `swarm-registry.json` | 33/33 names, 0 role mismatches, 0 missing/extra |
| Supersede restatement | normalized diff base→rows 41–51 | 46 identical; 47/49/50/51 rule-preserving; **48 drops one normative sentence** (F2) |
| Controls | `cmp` / rerun | `C2K1 == c2-before`; `C3K1`/`C3K2` match live runs |
| q36 revert | `git diff --stat 92d3c86 master -- quality/q36-successor-receipts.txt` | empty |
| SHONEN | `grep '\[x\]\|\[~\]' SHONEN.md` | 4 × `[~]`, 0 × `[x]` — matches the spot-check |

Cross-checks of record claims: `MINT.md` supports row 41; `round-29.md` M29-sweep
records "41/43 at base and tip alike" as M30-2 states; the routed-gap pointer
`round-29-verifier-spotcheck.md:56,85-87` exists and names both notes; the new
README rows name real notes and real artifacts; S185's `used-by` paths exist;
census `185 / malformed 0 / dup ids none / mined used-by missing none`; the fleet
report pointer `.ufo/reports/round-30/mado.md` **resolves in the fleet repo**
(fleet commit `bbae16b`, authored `mado-shokunin`) — the lane's own
`.ufo/reports/` holds only round-1, so the LOG path is a fleet-root path.

No code caller other than committed receipts consumes the changed artifacts:
`quality/counter-selftest.py` is a round-26-counter harness and does not
enumerate `c2/count.py` or `check-index.py`; the two do not import each other.

## 5. Residual risk and verification gaps

- **Resume lanes: not applicable.** `w1-plan.json` `counts {spawn: 33, resume: 0}`,
  33 unique tasks, no `resume` token in the plan or spec — `resume_continuity_v1`
  has no path to exercise here, by construction.
- **One canonical runtime: holds.** Both claim instruments read committed bytes
  only (`count.py` `git show REV:…`; `check-index.py` `-C repo … show/ls-tree` in
  `--rev` mode). Neither writes to the lane (`check-index.py` writes only inside
  a `TemporaryDirectory` in `selftest()`; the repaired `--rev` path adds no
  write). Receipts use `--rev`; `--root` is exercised only by the selftest.
  Known `--root`/`--rev` divergences from `RevC1Fence`/`SentScope` F2 are latent
  on committed bytes and are their findings.
- **Record blind spot, disclosed by design**: the fence counts rows, not cell
  content. Live at master: row B's compressed claim (F6, routed) and the
  pre-existing r26 row with no Sources cell (2 cells; the r26 row is outside this
  chain's write set and correctly not repaired silently). "Coverage 10/10" is
  navigation, not row validity.
- **Not verified by me** (no artifact): saturation "9.0 / N=3"; the fleet misroot
  sweep (F8); the fleet report's own prose beyond the pointer/SHONEN lines.
- **Chain may still move.** Reviewed tip `15ddd7d`; three seat reports are still
  untracked at that tip (including this one), so a further records entry is
  expected and will change the file counts in F7 and the wave-report inventory.
- **Repair lineage is disclosed but not claim-shaped** (F3): if round 31 adopts
  criterion 52 strictly, gate repairs will need their own registered predicate
  rather than riding the claim's erratum.
