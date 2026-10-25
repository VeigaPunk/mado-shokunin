# RevC2Tip — C2 re-derivation and per-observable attack (round 35, wave 2)

Seat: `L1Mado35.RevC2Tip` (leaf reviewer). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Scratch: `.ufo/waves/round-35/scratch/RevC2Tip/` (harness `attack.py`, cases under `cases/`, `h1/`).
Read-only on lane corpus, counters, controls, `frozen.json`, `clauses.json`, `SOURCES.md`, the ledger,
jj state and git index. No installs; pacman never invoked. `python3` = 3.14.8.

## 0. Canonical command, pasted

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json; echo rc=$?
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
rc=0
```

Same identity, rerouted: from `cwd=/tmp` with absolute `--repo`/`--frozen` → same line, `rc=0`.
Every input the counter reads is tracked and clean at `HEAD` (`19e4ab3`): `git diff --quiet HEAD --`
was clean for `c2/count.py`, `c2/frozen.json`, `c1/clauses.json`, `ledger/RevFrozenBlobs-r35.md`,
all nine control receipts and `controls/c2-donothing.txt` (`git ls-files` tracked, `git diff` empty).

**So the literal claim is TRUE and reproducible.** What it attests is the rest of this report.

## 1. `ledger_tip_ok` — I re-ran the seven `rev-parse` calls myself

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin
$ for p in .ufo/waves/round-33/c1/count.py .ufo/waves/round-33/c1/frozen.json \
           .ufo/waves/round-33/c2/count.py .ufo/waves/round-34/c1/count.py \
           .ufo/waves/round-34/c1/frozen.json .ufo/waves/round-34/c2/count.py \
           .ufo/waves/round-34/c2/frozen.json; do
      printf '%s ' "$p"; git rev-parse "dff394109f3cc3d851309ad7c67dd3b35b46adf2:$p"
  done; echo rc=$?
.ufo/waves/round-33/c1/count.py       4ab3db435dd2e396402d1d83039e35082f1138fe
.ufo/waves/round-33/c1/frozen.json    60d1094baa2992294533bae37e0990ae23077609
.ufo/waves/round-33/c2/count.py       df563528e725951b447ef31b324ec4b7d264e91b
.ufo/waves/round-34/c1/count.py       49089c186fb75f1bd2cc4c45c0161282ea6e8a46
.ufo/waves/round-34/c1/frozen.json    0bfe0d866c4e9a2d17da297a11dae389150b488b
.ufo/waves/round-34/c2/count.py       3a499a7eaa6cf5e861a5849992c37f1a7bede962
.ufo/waves/round-34/c2/frozen.json    ef3392b45f638513ff98dda95808f3f3938705e0
rc=0
```

All seven equal `frozen.json`'s `frozen_blobs` list **and** the ledger document's own table
(programmatic parse of doc §1 rows: `rows=7`, `table == spec → True`). Also verified:
`git merge-base --is-ancestor dff3941 master` → 0; `git cat-file -t dff3941` → `commit`;
`git log --follow --oneline` returns exactly one commit per path (its freeze commit), so there is
no write-then-revert on `master`. The re-issue's core measurable claim — seven blob ids at
`dff3941` — is real, and the git loop in `count.py:102-124` genuinely runs it.

Two scope facts the loop does **not** establish (see F4): the `git rev-parse` has no `--verify` and
no reachability check, and the loop iterates `spec["frozen_blobs"]`, never the ledger table.

Cross-seat note: `w2/RevTipLedger` has since falsified the *naming* around this observable
(`dff3941` is not the current tip; the round-34 label was stale by two commits, not one). I
independently reproduced the same distance: `git rev-list --count fa7ba11..dff3941` → `2`
(`fa7ba11 → 57622b8 → dff3941`). That finding is theirs; I only confirm the number.

## 2. The four observables, one at a time: the bytes that produce each number

Mechanism references are to `.ufo/waves/round-35/c2/count.py`. Every case below was run against
the committed counter with a scratch copy of the spec/ledger; the committed spec is untouched.
Driver: `python3 .ufo/waves/round-35/scratch/RevC2Tip/attack.py` (cases under `cases/`; `h1` cases
under `h1/`; per-case `frozen.json`/`clauses.json` kept as evidence).

### O1 `uncovered=0`

**Bytes that produce it**

| Input | Bytes |
|---|---|
| `c1/clauses.json:4-83` | ten `live[]` entries; nine carry `control.receipt` at lines 10, 18, 26, 34, 42, 50, 58, 66, 74; `o-nofollow-open` (line 78) carries `not-load-bearing.reason` (line 81) |
| the nine receipts | each line 3 is `PRED-C1-r35-v1 … verdict=TARGET_MISSED`, e.g. `controls/c1-digest.txt:3`; matched by `MISSED = re.compile(r"verdict=TARGET_MISSED")` (`count.py:50`) at `count.py:88-92` |
| `count.py:83-85` | the declaration branch `continue`s *before* any control is resolved |

Zero because the one declared clause is skipped and each of the other nine receipts exists and
contains the token. Falsifiable: `u1-no-control` (control deleted) → `uncovered=1 … MISSED` rc 1;
`u4-missing-receipt` (path does not exist) → 1; `u5-met-receipt` (`golden.txt`, TARGET_MET) → 1.
So the observable is live.

**Ground truth of the receipts.** I re-ran the C1 counter against all eleven committed control
trees; every run reproduced its committed receipt line and exit code exactly, including `golden`
(`3/8/0 MET` rc 0) and `c1-donothing` (`0/0/8 MISSED` rc 1). The committed C2 negative control also
reproduces: `--frozen /fast/scratch/mado-r35/c2-donothing/frozen.json` → `uncovered=1 retired=1
toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MISSED`, rc 1, and its receipt line 6 matches it
byte for byte. Nine of the ten defect-control receipts are the identical tuple `2/7/1` (the tenth,
`c1-donothing`, is `0/0/8`; `golden` is `3/8/0`); the receipts differ only in
their header/command lines (`diff c1-digest.txt c1-status-queued.txt` → lines 1-2 only).

### O2 `retired=1`

**Bytes:** `c1/clauses.json:85-90` — `retired[0].id = "r34-word-bound-1-25"`, absent from every
live id; counted at `count.py:94-97`. The retirement is substantively justified: r34
`c1/count.py:144-154` pins `quote = spec["quotes"][sid]`, requires `found == quote`, *then* applies
`1 <= len(words) <= 25`; r34 `frozen.json` quotes are 8 and 2 words, so the bound could never fail.
Falsifiable: `r1-no-retired` → `retired=0`; `r3-retired-is-live-renewal` (id set to a live id) → 0;
`r4-two-retired` → `retired=2`. Live.

### O3 `toctou_declared=1`

**Bytes:** `c1/clauses.json:78-83` (the single `not-load-bearing` block with a truthy `reason`),
`c2/frozen.json:13` `"toctou_clause": "o-nofollow-open"`, and `count.py:99-100`
`declared == [spec["toctou_clause"]]`. Falsifiable **independently of `uncovered`**: `t1` (a second
declaration added to `digest-match`, its control kept) → `toctou_declared=0` while `uncovered`
stays 0; `t2` (declaration replaced by a control on the same clause) → `toctou=0`, `uncovered=0`;
`h1-drop-declaration` → `toctou=0`, `uncovered=0`. The observable is live and orthogonal. The
split's direction is honest: `c1-entry-symlink` reproduces `2/7/1 MISSED` against `golden`'s
`3/8/0 MET`, so the S_ISLNK walk is load-bearing and only the open-time flag is declared away.

### O4 `ledger_tip_ok=1`

**Bytes:** `c2/frozen.json:11` (blob ledger path), `:12` (`r34_tip`), the seven `frozen_blobs`
entries; the ledger document contains the tip string at lines 5, 13, 17, 19, 35, 53 (any one
suffices: `count.py:106` is `if spec["r34_tip"] in text`); `count.py:107-124` then runs
`git -C <repo> rev-parse <tip>:<path>` per **spec** entry. Falsifiable: `l1-blob-corrupt` → 0;
`l3-tip-swapped` → 0; `l4-doc-without-tip` → 0; `l6-path-blob-mismatch` → 0. The git half is real
(§1). Two holes, F4 below.

## 3. Full isolation matrix (each case = one mutation, committed inputs otherwise)

| case | mutation | uncovered | retired | toctou | tip | rc |
|---|---|---|---|---|---|---|
| baseline | none (copies in scratch) | 0 | 1 | 1 | 1 | 0 |
| u1-no-control | drop `digest-match.control` | **1** | 1 | 1 | 1 | 1 |
| u2-receipt-swapped | `digest-match` receipt → `c1-donothing.txt` (0/0/8) | 0 | 1 | 1 | 1 | **0** |
| u3-grep-only-receipt | receipt → 1-line scratch file with only the token | 0 | 1 | 1 | 1 | **0** |
| u4-missing-receipt | receipt path nonexistent | **1** | 1 | 1 | 1 | 1 |
| u5-met-receipt | receipt → `golden.txt` (TARGET_MET) | **1** | 1 | 1 | 1 | 1 |
| r1-no-retired | `retired: []` | 0 | **0** | 1 | 1 | 1 |
| r2-invented-id | retired id → `invented-clause-not-in-r34` | 0 | 1 | 1 | 1 | **0** |
| r3-retired-is-live | retired id → a live id | 0 | **0** | 1 | 1 | 1 |
| r4-two-retired | + second retired entry | 0 | **2** | 1 | 1 | 1 |
| t1-second-declaration | declaration on `digest-match` | 0 | 1 | **0** | 1 | 1 |
| t2-declaration→control | `o-nofollow-open` given a control | 0 | 1 | **0** | 1 | 1 |
| t4-reordered-live | `live` reversed | 0 | 1 | 1 | 1 | 0 |
| l1-blob-corrupt | one `blob_id` zeroed | 0 | 1 | 1 | **0** | 1 |
| l2-blob-dropped | one `frozen_blobs` entry removed (6 left) | 0 | 1 | 1 | 1 | **0** |
| l3-tip-swapped | `r34_tip` → `19e4ab3…` | 0 | 1 | 1 | **0** | 1 |
| l4-doc-without-tip | ledger doc with no tip string | 0 | 1 | 1 | **0** | 1 |
| l5-doc-table-wrong | scratch doc: tip string + a false one-row table | 0 | 1 | 1 | 1 | **0** |
| l6-path-blob-mismatch | path → the r34 `c1/count.py` blob | 0 | 1 | 1 | **0** | 1 |
| g1/g2 | predicate / target altered | — | — | — | — | **2** |
| h1-drop-one-load-bearing | `digest-match` deleted from `live` | 0 | 1 | 1 | 1 | **0** |
| h1-live-only-declaration | `live = [o-nofollow-open]` | 0 | 1 | 1 | 1 | **0** |
| h1-drop-declaration | `o-nofollow-open` removed, `live` = 9 controls | 0 | 1 | **0** | 1 | 1 |
| h1-drop-into-retired | `digest-match` moved to `retired` | 0 | **2** | 1 | 1 | 1 |
| retired empty/missing `why` | `retired: [{id, why:""}]` / `{id}` | 0 | 1 | 1 | 1 | **0** |

Every observable is individually failable (u1/u4/u5, r1/r3/r4, t1/t2, l1/l3/l4/l6) and
`toctou_declared` is orthogonal to `uncovered` (t1, t2). Exit contract holds: 0 MET, 1 MISSED,
2 on predicate/target drift.

## 4. Findings, by severity

### F1 (HIGH) — `uncovered`'s clause domain is the ledger itself, so a clause can be deleted and the claim still passes

`count.py:76-92` validates `ledger["live"]`, and nothing cross-checks that list against
`c1/count.py`. Deleting one load-bearing clause *and its control* from the committed ledger —
`digest-match` — yields `uncovered=0 … verdict=TARGET_MET` rc 0
(`h1-drop-one-load-bearing`). The extreme form, `live = [o-nofollow-open]` only, also yields
`TARGET_MET` rc 0 (`h1-live-only-declaration`). So `uncovered=0` is fail-open on deletion: it
proves "every clause the ledger lists is covered", not "the ledger lists every clause".
`c2/count.py:9` says "live clauses of the round-35 admission counter"; that referent is never read.
(Class already shown in w1 by `CritVacuous2` attempt A with a self-authored one-clause ledger; the
witness here is the committed ledger minus a clause, which is the mutation wave 2's `MutC2Real`
suite does not contain — its M1 removes a receipt's token, not the clause.)

### F2 (HIGH) — coverage is a token grep, and receipts are interchangeable across clauses

`uncovered` is `re.search("verdict=TARGET_MISSED", receipt)` on whatever path the clause names.
Two witnesses with the committed counter:
- `u2`: point `digest-match`'s receipt at `controls/c1-donothing.txt` — the `0/0/8` do-nothing tree
  that isolates no clause — and `uncovered` stays 0. Any in-family MISSED receipt covers any
  clause.
- `u3`: point it at a one-line scratch file whose whole content is `verdict=TARGET_MISSED` and
  `uncovered` stays 0. `control.tree` is never read and no control is ever executed.

`c1/clauses.json`'s own `note` states this rule, so the predicate is honest about it; the
inference it cannot support is "each live clause is load-bearing *for the reason the clause
states*". All nine receipts carry the same line 3, so even a genuine receipt cannot attribute a
kill to a clause. (`RevC2Clause` w1 and `MutC2Real` w2 M1 established the token-grep class; `u2`
adds the in-family cross-clause swap.)

### F3 (HIGH) — one clause C2 certifies as covered is not the clause `clauses.json` declares

`c1/clauses.json:54-59` declares `digest-match` as "The row's anchor cell carries the sha256 of the
named receipt", covered by `controls/c1-digest.txt`. In the counter, `c1/count.py:174` computes
`digest = hashlib.sha256(blob).hexdigest()` and **never uses it** (`grep -n digest
.ufo/waves/round-35/c1/count.py` → one hit, line 174); the only anchor test is
`receipt["sha256"] in cs[5]` (line 192), i.e. the frozen manifest string against the row cell.
I re-derived the consequence: copy `controls/golden`, append
`CORRUPTED DOCUMENT - not the fetched evidence` to `fetch/S203.receipt.txt` (actual sha
`15c5fe43…`, frozen `1b7fa87f…`) →

```
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET     rc=0
```

The receipt bytes are not measured, yet C1 still scores MET. The `c1-digest` control zeroes the
*row cell*, so it kills the coded conjunct and not the declared clause. Therefore
`uncovered=0` includes a clause whose named control does not exercise the declared property.
`w2/CritControls` §5 reports the same defect and proposes the one-line fix
(`and digest == receipt["sha256"]`); this seat re-derived it independently as a C2-coverage
consequence. Fixing it is a C1 counter change, out of scope for a read-only seat.

### F4 (MEDIUM) — `ledger_tip_ok` verifies the spec's own list, not the ledger's table, and the seven is unpinned

`count.py:107` iterates `spec["frozen_blobs"]`. Two directions:
- `l2`: delete one entry from `frozen_blobs` (six left, ledger doc still lists seven) →
  `ledger_tip_ok=1`, `TARGET_MET`.
- `l5`: replace the ledger document with one line naming the tip plus a deliberately false one-row
  blob table → `ledger_tip_ok=1`, `TARGET_MET`.

On the committed bytes the two domains happen to agree (doc §1 table parsed == spec list, 7/7), so
the committed number 1 is factually right; the observable just cannot detect a divergence.
(`MutC2Real` M3d/`CritVacuous2` covered the doc-table half; the six-of-seven spec-shrink is this
seat's witness.)

### F5 (LOW) — `retired` is an unbound string set, and the predicate's named clause does not exist

`count.py:94-97` reads only `id`; `why` is never read (`retired: [{id: x, why: ""}]` and
`retired: [{id: y}]` both give `retired=1`, `TARGET_MET`). `r2` shows any invented id absent from
`live` satisfies it. The frozen predicate names "the r34 `quote-equals-frozen` clause"
(`c2/frozen.json:3`, `count.py:41`) but no artifact in the lane carries that as an id; the ledger
retires `r34-word-bound-1-25`, an id that first appears in commit `19e4ab3` (`git log -S`), and
round 34 ships no clause ledger at all. So the predicate's named referent and the ledger's retired
id are two different strings with no file binding them. (`CritDeadClause` w1 line 58 already
recorded "any retired id"; the name mismatch and the unread `why` are this seat's.)

## 5. Verdict on C2

- **Literal predicate: TRUE.** `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1
  verdict=TARGET_MET`, rc 0, reproduced from two working directories; all four observables are
  live (each has a mutation that flips it) and the seven blob ids genuinely re-verify at `dff3941`.
- **As evidence of the thing the round is claiming — that the r35 clause ledger is complete and
  every live clause is load-bearing as declared — FALSE.** Three of the four observables are
  token/self-description checks over files the ledger itself names (F1, F2, F5), and the one
  clause C2 credits with a real control (`digest-match`) is not the clause the ledger declares
  (F3). `c2/count.py`'s own closing sentence ("This counter scores the lane's self-description of
  its own evidence, not the corpus") is accurate; the score it produces cannot be cited as
  coverage.

## 6. Residual risk and verification gaps

- I did not re-execute the C1 *mutations* each control tree encodes against the real corpus; I
  reproduced the eleven committed outputs exactly and audited the `grep` semantics of the clauses
  instead. Whether each tree fails for its named reason is `CritControls`/`RevQuoteS20x` territory;
  for nine of the ten defect controls the identical `2/7/1` line cannot attribute the failure, so
  that step stays unverified.
- I verified the eight `fetch/S20[3-9]`/`S210` receipts only by sha256 against `c1/frozen.json`
  (8/8 match); I did not compare their bytes to an upstream source.
- `ledger_tip_ok`'s behaviour on an unreachable/dangling but present commit, on abbreviated or
  ambiguous revisions, and on `--repo` pointing at a foreign worktree was not exercised (the first
  needs git object writes, which this seat may not make); `count.py` has no `--verify`, no
  reachability check and no path/role check on the tip occurrence.
- Scratch writes only: `.ufo/waves/round-35/scratch/RevC2Tip/**` and this file. Lane corpus,
  counters, controls, `SOURCES.md`, `frozen.json`, the ledger doc, jj state and the git index were
  not modified (`git status --porcelain` shows only pre-existing wave work and `scratch/`).

Reproduction:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 .ufo/waves/round-35/scratch/RevC2Tip/attack.py           # 20 cases, §3 table
# h1 cases: h1/*/frozen.json, run as
#   python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen <case>/frozen.json
# digest probe: scratch/RevC2Tip/digest-probe (golden + corrupted S203 receipt)
```
