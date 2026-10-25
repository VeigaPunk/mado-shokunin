# RevRecordsChain — round-30 landed-chain review (records + claim machinery)

Seat: reviewer, records chain. Lane `mado-shokunin`, base `8f51071b`,
**reviewed tip `master` = `274f735`** (8 commits). Read-only review: this seat
wrote nothing except this report (no lane file, index or jj state touched;
counters/gate re-run against committed bytes only).

**The chain moved twice during this review.** Pass 1 measured
`8f51071b..92d3c86`; pass 2 re-measured at `15ddd7d`; the final pass covers
`a0dd664` and `274f735`, which repaired instrument and record defects (including
two raised by this seat). Repairs are verified below; stale assertions from
earlier passes are listed as retracted in §3c. This file's committed copies at
`a0dd664`/`274f735` are earlier passes of the same seat; this revision is final.

Tooling note: **no LSP device is mounted in this session** (`write xd://lsp` →
"No such tool: xd://lsp. Mounted devices: ast_edit, debug"). Caller/definition
checks were done by reading both changed Python artifacts in full plus live
re-runs; `grep` below is only literal-string/quote verification, never semantic
proof of a caller relation.

## Verdict

The chain is **scoped, linear and authorship-honest**; every cited hash resolves;
every measured fraction reproduces from committed bytes **at every revision and
under every instrument blob**. No unrelated change (0 paths outside the declared
set). Record defects F1/F2 were repaired in-chain at `a0dd664` and the repairs
verify. What remains is **repair provenance**: both frozen instruments were
mutated after the data commit, one evidence receipt was rewritten in place, and
one *measured* corpus row was rewritten in place — all disclosed, none moving a
verdict. Findings are recommendations; nothing here is an admission or verdict.

## 1. Chain shape, authorship, scope — verified at `274f735`

```
274f735 round-30 w1 part 3: expansion verdict correction (capability-only), corrected capability row, final seat report   mado-shokunin
a0dd664 round-30 w1 part 2: quotepath+non-ASCII selftest, counter rubric repair (identical output), record repairs + errata  mado-shokunin
15ddd7d round-30 w1 addendum: gate repair, receipts, lesson+scorecard errata, seat reports                                   mado-shokunin
2db0c44 round-30 verifier spot-check addendum (integrator, hyaku): wave-1 digest, routed defects                            protocol-shokunin
d72243e round-30 verifier spot-check (integrator, hyaku): non-author admit/reject                                           protocol-shokunin
92d3c86 round-30 records: receipts, wave spec, LOG, SCORECARD                                                               mado-shokunin
446dc39 round-30 data: index rows, criterion grounding, S185, lesson                                                        mado-shokunin
451e8b3 round-30: freeze registration, counters, index gate, controls                                                       mado-shokunin
```

- **Linearity**: strict parent chain, no merge. **Cited hashes**:
  `git merge-base --is-ancestor` true for `451e8b3c` (freeze) and `446dc396`
  (data); each authored *and* committed by `mado-shokunin <mado@shokunin.local>`.
  `d72243e`/`2db0c44` are `protocol-shokunin` (the non-author integrator, as
  declared in the spot-check record).
- **Scope**: cumulative diff is 58 paths, **0 outside** `.ufo/waves/round-30/`,
  `corpus/`, `quality/check-index.py`, `LOG.md`, `SCORECARD.md`; cumulative
  `+7920/−0` versus base (every rewritten file was *created* by this chain, so the
  rewrites appear only in per-commit diffs).
- **Protected subtrees byte-untouched at tip**:
  `git diff --stat 8f51071b master -- .ufo/waves/round-29/ tools/ corpus/knowledge/ SKILL.md PROVINCE.md`
  is empty.
- **In-chain rewrites (quantified)**: post-freeze
  `.ufo/waves/round-30/c2/count.py` `+38/−19` and `quality/check-index.py`
  `+122/−31`; post-data additionally `corpus/QUALITY.md` `+1/−1` (row 48).
  `registration.md` (110 lines) is byte-identical to `451e8b3c` — correctly not
  edited, even though its freeze sentence is now false at tip (S1).
- **Instrument blobs**: gate `df01b20f` (freeze) → `0c13f39` (`15ddd7d`) →
  `891fdd6` (`a0dd664`+); counter `74a4859` (freeze, `15ddd7d`) → `bf798a0`
  (`a0dd664`+). Both are post-freeze mutations (S1).
- **Data delta since the data commit**: only `corpus/QUALITY.md` row 48;
  `corpus/README.md` and `corpus/SOURCES.md` are byte-identical to `446dc396`.
- **q36 drift reverted**: `git diff --stat 92d3c86 master --
  quality/q36-successor-receipts.txt` empty; recorded in the SCORECARD erratum.
- **Worktree at review end**: `M` on this report (the final pass),
  `RevTrendExpansion.md` and `SentScope.md` (other seats' files, modified after
  the commit), untracked `SimplifierC2.md` — wave reports are still landing; this
  report is written after `274f735`.

## 2. Classification of every change

| Path | Commit(s) | Class | Note |
|---|---|---|---|
| `registration.md` | freeze | claim-machinery | frozen spec; byte-identical at tip |
| `.ufo/waves/round-30/c2/count.py` | freeze + `a0dd664` | claim-machinery | rubric repair, output verified identical (S1) |
| `quality/check-index.py` | freeze + `15ddd7d` + `a0dd664` | claim-machinery + shipped capability | three blobs, 6/6 → 8/8 → 9/9 (S1, S2) |
| `controls/*` (C2K1, C3K1, C3K2) | freeze | claim-machinery (controls) | C2K1 byte-identical to `c2-before`; C3K1/K2 match live runs |
| `evidence/{c1,c2}-before`, `census-before` | freeze | record | pre-data receipts; all reproduce |
| `corpus/README.md` | data | record / measured substrate | 2 index rows (C1); row B content defect S7 |
| `corpus/QUALITY.md` | data + `a0dd664` | record / rubric substrate | rows 41–52; row 48 in-place correction (S3) |
| `corpus/SOURCES.md` | data | record | +S185 |
| `corpus/lessons/round-30.md` | data + addenda | record | M30-1/M30-2, Gate, addenda parts 1–3 |
| `corpus/lessons/round-30-verifier-spotcheck.md` | `d72243e`, `2db0c44` | record (non-author) | admit/reject + wave-1 digest |
| `evidence/{c1,c2,c3}-after`, `census-end`, `freeze-smoke-…txt` | records | record | `freeze-smoke` truncated, superseded by `-full` (R1) |
| `evidence/freeze-smoke-451e8b3c-full.txt` | `a0dd664` | record | complete three-leg re-capture (R1) |
| `evidence/c3-repair-d72243e.txt` | `15ddd7d`, rewritten `a0dd664` | record (repair receipt) | rewritten in place (S2); still not criterion-24-shaped (S4) |
| `evidence/selftest-d72243e.txt` | `a0dd664` | record | commits the 460/460 harm-watch run |
| `w1-plan.json`, `w1-spec.json`, `w1/reports/swarm-registry.json` | records / addendum | claim-machinery (wave) | 33 items/members, names+roles equal |
| `.ufo/waves/round-30/w1/reports/*.md` | addendum | record (wave evidence) | 27 committed at `15ddd7d`, more landing |
| `LOG.md` | records | record | no erratum for the repairs (S1b) |
| `SCORECARD.md` | records + errata parts 1–2 | record | capability correction appended at `274f735` |
| **unrelated** | — | **none** | 0 paths outside the declared set |

## 3. Findings

### 3a. Repaired in-chain (verified by re-run)

**R1 — freeze-smoke C2 leg (was High).** `evidence/freeze-smoke-451e8b3c-full.txt`
now carries all three legs with complete output; its C2 block matches a live
`c2/count.py 451e8b3c` run line-for-line (14 lines: `counter=`, 3 `METRIC`,
8 `UNRESOLVED`, `LINE 20 …`, verdict, `EXIT=1`), differing only in the rev token
because the receipt was captured with the full hash. The truncated original is
kept and the erratum cites both discovering seats. Criterion 49's "full output is
committed" is now satisfied.

**R2 — row 48 verbatim (was High).** `corpus/QUALITY.md:354` at tip is 957 bytes
with the restored accounting sentence — "This criterion is added after final
falsification, supplies no retroactive pass and no numeric C2/criterion-count
credit; delivered C1 fails it and remains harmed." — followed by the citation;
parentheses balanced. Every superseding row's rule text is now present at tip, so
the preamble's "restates its rule verbatim" is supportable (rows 49–51 still omit
their parenthetical *evidence instances*, which are not rule text). The repair
mechanism raises S3.

### 3b. Standing

**S1 — Medium. Both frozen instruments were mutated after the data commit.**
The registration freezes "the counters and the gate in the pre-data commit"
(`registration.md:86-88`); at tip the gate has three blobs (`df01b20f` → `0c13f39`
→ `891fdd6`) and the counter two (`74a4859` → `bf798a0`). All mutations are
disclosed (SCORECARD errata parts 1–2, lesson addenda) and none moves a verdict —
I re-ran every predicate under every blob (base 41/43 exit 1; data and `d72243e`
43/43 exit 0; selftest 6/6 → 8/8 → 9/9; C2 28/40, 31/39 → 40/52, 40/40 at data,
`d72243e`, `15ddd7d`, master; old-vs-new counter output byte-identical at
`8f51071b`, `446dc396`, `15ddd7d`). But under the round's own criterion 52
(`QUALITY.md:358`) a discovered gap's repair is "a declared claim **with its own
counter**"; these repairs ride C3/C2 errata and their selftests instead. Sub-item
**(b)**: `LOG.md` — the round's primary chronological record — carries **no**
erratum for either repair, so its round-30 entry still presents the 6/6 gate and
frozen instruments as current while SCORECARD and the lesson say otherwise.

**S2 — Medium. An evidence receipt was rewritten in place.**
`evidence/c3-repair-d72243e.txt` at `15ddd7d` recorded the v2 gate
(sha `373680fe…`, `8/8`); at `a0dd664` the same path records the v3 gate
(sha `51b513f5…`, `9/9`) — `+3/−3`. The v2 receipt therefore no longer exists as
bytes (only the erratum prose preserves it), which contradicts the append-only
evidence discipline the lane applies elsewhere: the truncated freeze-smoke was
kept and a `-full` sibling added. Fix: re-cut as
`c3-repair-<rev>-v<n>.txt`, never overwrite.

**S3 — Medium-Low. Row 48 was repaired by rewriting a measured corpus row.**
The `a0dd664` correction is a one-line replacement of a row added in the data
commit (`corpus/QUALITY.md +1/−1` after `446dc396`), while the same preamble says
"corrections land as new rows, never rewrites" (`QUALITY.md:344-345`). Substance
is correct and disclosed, but the *measured* revision `446dc396` still lacks the
sentence, so a reader at the measured commit sees the defective row; and the
correction makes the data object differ from its measured bytes. An erratum row
appended as row 53 would satisfy both the rule and the measurement.

**S4 — Low-Medium. The repair receipt still does not satisfy criterion 24's
binding.** Criterion 24 (`QUALITY.md:131`) requires `tool_sha256=` equal to
`git show <measured_commit>:<tool> | sha256sum` plus `measured_commit`. The
receipt's header is `gate sha256 (repaired v2, quotepath=off)`, its sha
`51b513f5…` equals the gate only at `a0dd664`+, while every revision it measures
(`8f51071b`, `446dc396`, `d72243e`) carries `fc4a10a2…` (v1) — and no
`measured_commit` is declared. The SCORECARD correction now says the original
demonstration "pins the pre-repair blob `df01b20f`", which is honest prose but not
the receipt-shaped binding the criterion asks for.

**S5 — Medium, recorded limit (not repaired by design).** C2's 40/40 measures
**citation resolvability**, not lesson derivation: rows 41–45 resolve through
`M30-1`, the audit row recording their own defect, plus `MINT.md` (verified real,
`MINT.md:3-16`, but outside the counter's `lessons/` namespace). Erratum part 2
now records exactly this limit; the round report should repeat it so
"lesson-grounded admission criteria" is not read as derivation.

**S6 — Medium. S185's "verbatim" located quote is still schematic.**
`corpus/lessons/round-30.md:24` quotes
`revision=$rev indexed=$covered/$total missing=$missing … coverage=$score/10`;
that string exists nowhere in `SCORECARD.md` (the source, `SCORECARD.md:84`, is an
f-string). The pinned block digest `8b59b503…` resolves only under the
fence-inner-bytes serialization, which the row does not name. The non-author
spot-check reached the same conclusion and routed it to round 31; the bytes at tip
are unchanged.

**S7 — Medium-Low. The C1 row for `mutation-testing-r28.md` over-compresses its
note (live record defect).** The row says "a survivor is a suite limitation" and
"equivalent mutants bound the denominator"; the note
(`corpus/knowledge/mutation-testing-r28.md:20`) bounds that to "under the gate's
observations", says equivalent mutants "can appear as survivors" when included,
and says exclusion "affects the denominator". Verified first-hand; matches
`w1/reports/ScribeRowAccuracy.md` F1–F3. The fence counts the row either way, so
C1's 43/43 is blind to it — the README Quality bar already says rows are routes.
Routed to round 31; repair is an append-only row correction.

**S8 — Low. The lesson's "24 seat reports" count is stale.**
`corpus/lessons/round-30.md:60`; `15ddd7d` itself carried 27 `.md` reports +
`swarm-registry.json`, and more landed afterwards. Give counts a revision or drop
them.

**S9 — Low. "misroot sweep clean" still has no committed receipt.**
`LOG.md:1820`, `SCORECARD.md:1924-1928`. The new `evidence/selftest-d72243e.txt`
receipts the 460/460 harm-watch tally (and the erratum notes the head-label
mismatch), but not the fleet-root sweep. Criterion 42 applies: commit it or drop
the clause.

**S10 — Low. Counter block attribution remains heading-blind.**
`c2/count.py` still binds section prose to the preceding criterion, so a concrete
`lessons/<file>.md` appended after the last *active* criterion would resolve it
without a citation on its own line. Harmless at tip (criterion 40, which receives
the `## Grounding repair` block, is superseded); the repair added position-guarded
supersession and `act_n > 0`, which are both verified, but not section scoping.
Routed to counter v2.

**S11 — Low. Registration arithmetic off-by-one, now recorded.**
`registration.md:61` says "12 lines superseded by rows 41–51"; rows 41–51
supersede 11 (1–5, 18, 19, 32, 38–40), the twelfth being 20 via criterion 21.
Frozen file not edited; the erratum records it. Landed arithmetic (52 − 12 = 40)
is correct, and the counter's superseded set equals `SCORECARD.md:1915`.

### 3c. Retracted from earlier passes

- **Report pointer** (my pass-1 F8): `.ufo/reports/round-30/mado.md` resolves in
  the **fleet** repo (fleet commit `bbae16b`, authored `mado-shokunin`); the
  lane's `.ufo/reports/` holds only round-1, so the LOG path is a fleet-root path.
  Not a defect.
- **Selftest symlink gap** (pass-1 F6): closed — gate case 8 refuses a symlinked
  note, case 9 covers non-ASCII/space names via a real git fixture.
- **q36 worktree drift** (pass-1 F9): reverted to committed bytes and recorded.
- **"Data targets unchanged after `446dc396`"** (pass-2 §1): no longer true after
  `a0dd664` rewrote row 48; superseded by S3.

## 4. Claim numbers reproduced at tip `274f735`

| Measurement | Command | Result |
|---|---|---|
| C1 fence, base/data | SCORECARD counting block at `REV=` | `41/43 missing=2` exit 1; `43/43` exit 0 |
| C2, base | `python3 -I .ufo/waves/round-30/c2/count.py 8f51071b` | `literal 28/40`, `superseded=[20]`, `active=39 resolved_active=31`, `TARGET_MISSED`, exit 1 |
| C2, data / `d72243e` / `15ddd7d` / master | same | `literal 40/52`, `superseded=[1..5,18..20,32,38..40]`, `active=40 resolved_active=40`, `TARGET_MET`, exit 0 |
| C2 repair is output-neutral | old blob (`15ddd7d:…`) vs tip counter at `8f51071b`, `446dc396`, `15ddd7d` | `diff` empty at all three |
| C2, freeze | tip counter at `451e8b3c` | 14 lines incl. tallies, `EXIT=1`; matches `-full` receipt |
| C3 gate, v1 (`df01b20f`) | `--rev 8f51071b/446dc396`, `--selftest` | 41/43 exit 1; 43/43 exit 0; 6/6 |
| C3 gate, v2/v3 (`0c13f39`, `891fdd6`) | same + `--rev d72243e`, `--rev master`, bare | 41/43 exit 1; 43/43 exit 0; **9/9**; bare → `SETUP_ERROR` exit 2 |
| Repair receipt sha | `git show master:quality/check-index.py \| sha256sum` | `51b513f5…` = receipt (tip only; S4) |
| Harm watch | `bash tools/mado-verify.sh --selftest` | `460/460`, exit 0; receipted at `d72243e` |
| Sources | tier/status recount both revs | 184→185; A 177→178; mined 165→166; queued 10; rejected 9; no dup ids |
| Coverage map | row extraction at tip | 43 rows; r26 row **2 cells** (no Sources cell) |
| Wave registry | spec vs `swarm-registry.json` | 33/33 names, 0 role mismatches |
| Supersede text | normalized diff, base criteria → rows 41–51 | all rule text present at tip; 49–51 omit only evidence instances |
| Controls / q36 / SHONEN | `cmp`, `git diff`, `grep` | controls match live runs; q36 diff empty; 4×`[~]`, 0×`[x]` |

Cross-checks: `MINT.md` supports row 41; `round-29.md` M29-sweep records
"41/43 at base and tip alike"; the routed-gap pointer
`round-29-verifier-spotcheck.md:56,85-87` exists; new README rows name real notes
and artifacts; S185's `used-by` paths exist; census `185 / malformed 0 / dup ids
none / mined used-by missing none`; the fleet report pointer resolves (`bbae16b`).
No code caller other than committed receipts consumes the changed artifacts:
`quality/counter-selftest.py` is a round-26-counter harness and enumerates
neither new script; the two do not import each other.

## 5. Residual risk and verification gaps

- **Resume lanes: not applicable.** `w1-plan.json` `counts {spawn: 33, resume: 0}`,
  33 unique tasks, no resume token — `resume_continuity_v1` has no path here.
- **One canonical runtime: holds.** Both instruments read committed bytes only
  (`git show` / `git -C repo … show|ls-tree`); neither writes to the lane
  (`check-index.py` writes only inside `TemporaryDirectory` in `selftest()`; the
  `--rev` path gained no write). Receipts use `--rev`; `--root` is selftest-only,
  and its known divergences are the other seats' findings.
- **Record blind spot by design**: the fence counts rows, not cell content. Live
  at tip: row B's compressed claim (S7) and the pre-existing r26 row with no
  Sources cell — both invisible to C1's 43/43, both routed.
- **Not verified by me** (no artifact): saturation "9.0 / N=3"; the fleet misroot
  sweep (S9); the fleet report's prose beyond pointer and SHONEN lines.
- **The chain is live.** Final tip reviewed `274f735`; another seat's `SentScope.md`
  is modified in the worktree and `SimplifierC2.md` is untracked, so a further
  records entry will change the file counts (S8) and may add errata. This report
  itself is written after the tip and is therefore an untracked delta unless a
  later records commit lands it.
- **Repair lineage needs a policy** (S1–S4): this round established that frozen
  instruments can be repaired mid-round with disclosed errata, but left three
  shapes of same-class evidence treatment — overwrite (repair receipt), sibling
  (`-full` smoke), and in-place row rewrite. Criterion 52 strictness for round 31
  should pick one.
