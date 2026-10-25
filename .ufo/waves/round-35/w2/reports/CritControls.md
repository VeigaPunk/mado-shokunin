# CritControls — the eleven C1 control receipts reproduce, and the kill rule still cannot see the data

Seat: `CritControls` (critic, leaf, no dispatch). Round 35, wave 2, falsify lane.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. All writes confined to
`.ufo/waves/round-35/scratch/CritControls/` and this report. No lane artifact, counter,
control, `SOURCES.md`, clause ledger or jj/git state was modified. No tools installed.

## Axes

1. **Receipt agreement** — does each committed `controls/*.txt` reproduce on stdout and rc?
2. **Control resolution** — does a receipt line distinguish the clause it is supposed to kill?
3. **Kill-rule strength** — what is the cheapest tree that still reaches `TARGET_MET`?
4. **Distinguishability** — can the counter, on its own, separate the round's real data from that tree?
5. **Clause-to-code fidelity** — does every named clause measure what its name says?

---

## 1. Eleven control trees, re-run against their committed receipts

Command, verbatim, run from the lane root for each `<tree>`:

```sh
python3 -I .ufo/waves/round-35/c1/count.py \
  --root .ufo/waves/round-35/controls/<tree> \
  --frozen .ufo/waves/round-35/c1/frozen.json
```

| control | receipt line | my line | receipt rc | my rc | agree |
|---|---|---|---|---|---|
| `c1-digest` | `PRED-C1-r35-v1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` | identical | 1 | 1 | **AGREE** |
| `c1-donothing` | `PRED-C1-r35-v1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED` | identical | 1 | 1 | **AGREE** |
| `c1-entry-symlink` | `PRED-C1-r35-v1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` | identical | 1 | 1 | **AGREE** |
| `c1-quote-absent` | `PRED-C1-r35-v1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` | identical | 1 | 1 | **AGREE** |
| `c1-quote-long` | `PRED-C1-r35-v1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` | identical | 1 | 1 | **AGREE** |
| `c1-recheck-prose` | `PRED-C1-r35-v1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` | identical | 1 | 1 | **AGREE** |
| `c1-row-duplicate` | `PRED-C1-r35-v1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` | identical | 1 | 1 | **AGREE** |
| `c1-row-extra-field` | `PRED-C1-r35-v1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` | identical | 1 | 1 | **AGREE** |
| `c1-status-queued` | `PRED-C1-r35-v1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` | identical | 1 | 1 | **AGREE** |
| `c1-usedby-extra` | `PRED-C1-r35-v1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` | identical | 1 | 1 | **AGREE** |
| `golden` | `PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET` | identical | 0 | 0 | **AGREE** |

**11/11 agree** on both stdout and exit code; no stderr on any run. The round's own
counting command on the real root also returns what it claims:

```
$ python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET      exit=0
```

The control side of the kill rule is discharged. Everything below attacks what it
is worth.

## 2. Ten negative controls, one output

All ten defect controls print the *same* line: `2/7/1`. They are not the same defect —
each one kills a different id, and between them they exercise eight distinct clauses.
Established by cell-level diff of each tree against `controls/golden`:

| control | clause it kills | id it opens | verdict |
|---|---|---|---|
| `c1-entry-symlink` | `entry-regular` | S205 (entry is a symlink) | 2/7/1 |
| `c1-row-duplicate` | `row-unique` | S205 (row count 1→2) | 2/7/1 |
| `c1-row-extra-field` | `row-well-formed` | S206 (cells 7,8,9,10 shift) | 2/7/1 |
| `c1-usedby-extra` | `used-by-exact` | S207 (cell 10) | 2/7/1 |
| `c1-status-queued` | `status-mined` | S208 (cell 7) | 2/7/1 |
| `c1-recheck-prose` | `recheck-valid` | S209 (cell 9) | 2/7/1 |
| `c1-digest` | `digest-match` (as coded) | S210 (cell 5 zeroed) | 2/7/1 |
| `c1-quote-absent` | `gate-quote-substring` | S206 | 2/7/1 |
| `c1-quote-long` | `gate-quote-word-bound` | S203 | 2/7/1 |
| `c1-donothing` | all | all 8 | 0/0/8 |

The counter prints no per-id, no per-clause, and no failing-id detail — one aggregate
tuple and an exit code, and the aggregates are degenerate at the observed defect density
(one opened id ⇒ one lost row ⇒ `2/7/1`).

**Scope of this finding.** It is *not* a false pass: each control's tree really is
`TARGET_MISSED`, so each named clause really is live (except `digest-match` — see §5).
What it bounds is what a receipt *proves*. A committed receipt establishes
"this tree scores 2/7/1"; it does not establish "this tree failed *for the named
reason*." Any single-id defect in the tree buys the identical receipt line, so a receipt
cannot be cited as evidence that its named clause fired. For eight of the ten the ledger
in `c1/clauses.json` is currently resting on that unverified step.

## 3. Cheapest tree that still reaches `TARGET_MET`

Built at `.ufo/waves/round-35/scratch/CritControls/minal-shaved/`. Twelve files, **1251
bytes total**, no knowledge in it:

```
corpus/SOURCES.md                              1091 B   eight rows, one per S203–S210
corpus/knowledge/idle-lock-never-asked-r12.md     38 B   gate-quote: S203 a / S204 a
corpus/knowledge/idle-lock-chain-armed-r14.md     19 B   gate-quote: S205 a
corpus/knowledge/idle-lock-offered-in-the-bar-r15.md  95 B   gate-quote: S206 a … S210 a
.ufo/waves/round-35/fetch/S203..S210.receipt.txt   8 B    one byte each: "x"
```

```
$ python3 -I .ufo/waves/round-35/c1/count.py --root \
    .ufo/waves/round-35/scratch/CritControls/minal-shaved \
    --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
exit=0
```

Every one of the eight receipts is a single byte and **none matches its `frozen.json`
sha256**. The entries carry no claim, no topic, no URL, no date, no provenance — eight
`gate-quote:` lines whose whole quote is the letter `a`. The rows are eight pipes-and-
frozen-digest strings: nothing but the 512 bytes of recorded sha256, the 395 bytes of
frozen entry paths, and separators. Total real evidentiary payload: **0 bytes**.

**Why nothing cheaper exists.** Each element is pinned by the counter or by `frozen.json`:

- 12 paths are forced (3 entry paths + 8 receipt paths + `corpus/SOURCES.md`). They cannot
  be aliased: a symlinked receipt or entry is rejected (`read_regular`, `S_ISLNK` walk) —
  verified, `controls/c1-entry-symlink` short-circuits on it — and a hardlink is rejected
  by `st.st_nlink != 1`. Probe: hardlinking `S203.receipt.txt` to a second name gives
  `closed_rows=7`, exit 1.
- Each quote costs ≥ 1 byte: `quote.split()` must yield 1–25 words, so `""` fails. Probe:
  emptying the `S203` quote on a golden copy gives `2/7/1`, exit 1.
- Each row costs ≥ 64 bytes of digest plus its entry path plus twelve pipe characters:
  `len(cs) == 11` forces eleven cells and `"receipt sha" in cs[5]` forces the full hex.
- `mined` (5 B) is exact; the recheck token is the only free byte and `a` is the shortest
  token `valid_recheck` admits (symbolic branch). My first tree used `1d` at 1259 B; the
  shave to `1251` is the last byte available.

Compare the real payload the same counter scores: 8468 B of receipts + 7285 B of entries.
The minimal tree is **~12× cheaper** than the evidence it is accepted in place of, and
strictly cheaper than both prior-art constructions: `RevTarget`'s `quote-only` keeps the
real receipts (8468 B) and `CritVacuous`'s tree keeps 8 rows of junk but does not shave
the receipts to one byte.

## 4. Is the real data distinguishable from it, using the counter alone?

**No — and the round's own committed fixtures are proof, without my construction.**

| tree | what it is | counter output | rc |
|---|---|---|---|
| `.` (real lane root) | the round's actual 3 entries + 8 rows + 8 real receipts | `3/8/0 TARGET_MET` | 0 |
| `scratch/CritControls/minal-shaved` | 1251 B, zero evidentiary payload | `3/8/0 TARGET_MET` | 0 |
| `controls/golden` | a **different registry** (see below) | `3/8/0 TARGET_MET` | 0 |
| `scratch/CritControls/receipt-bytes` | golden with a corruption notice appended to `S203.receipt.txt` | `3/8/0 TARGET_MET` | 0 |

The counter's entire observable surface is one `print` plus the exit code. Three
distinct artifacts — real data, a 1.25 KB shell, and a registry whose *claims differ*
from the shipped one — are byte-identical on that surface. Nothing in the counter's
output lets a reader tell which tree it ran against.

The `controls/golden` row is the sharpest case, because it is the round's own anti-
vacuity control and it turns out **not to be the artifact under test**. Cell-level diff of
`golden/corpus/SOURCES.md` against the real `corpus/SOURCES.md`, 8 rows in each:

```
cell 5 (anchor/evidence):  8/8 rows differ
cell 6 (claim):            4/8 rows differ
cell 9 (recheck):          1/8 rows differ
cells 0,1,2,3,4,7,8,10:    0/8 rows differ
```

Concretely: `S206` cell 5 reads `…6354 B, sha256 a408…` in the real registry and
`…6354 B, file sha256 a408…` in golden; `S203` cell 9 is `on-request` in the real
registry and `on-change` in golden — a genuinely different recheck policy in a
load-bearing cell, accepted because `valid_recheck` only tests the token's *syntax*.
Both registries score identically. So even holding the receipts real, two different
knowledge claims about the same eight sources are interchangeable to this counter.

Two consequences:

1. The positive control is a **pre-data fixture**, and its receipt header says so
   (`pre-data, 2026-10-24T23:23:19-03:00`). It proves the counter *can* print
   `TARGET_MET`; it cannot be evidence that the shipped registry satisfies the predicate,
   because it never ran on it. The only `TARGET_MET`-on-real-data evidence in the round is
   the counting command itself, which is the claim, not a control.
2. Prior art already showed a junk tree passes (`CritVacuous`, `RevTarget` — both
   `TARGET_MET`, exit 0, on shape-only trees). What is new here is that the failure is not
   only reachable by an adversary: the round's shipped golden fixture diverges from the
   data in three of its cells and remains indistinguishable.

## 5. `digest-match` is tautological as coded (smallest safe correction found)

`c1/count.py:174` computes the receipt digest and throws it away:

```python
digest = hashlib.sha256(blob).hexdigest() if blob is not None else ""
```

`digest` appears on that line and nowhere else in the file (verified by grep: one hit).
The only anchor clause, `count.py:192`, is `receipt["sha256"] in cs[5]` — a substring
test of the **manifest's recorded string** inside the row. The registry quotes the
manifest back at the counter; the receipt's bytes are never hashed against anything.

Probe: take `controls/golden`, append
`CORRUPTED DOCUMENT - this is not the fetched evidence.` to `S203.receipt.txt`.

```
S203 actual sha256: 3420ec65e64d2c9137cc9bd769299deb67580d36b5a1437bd1856650b9760bc3
S203 frozen sha256: 1b7fa87ffe933990ee59acf3629ffbe3a90106bc9ebcce082237f7f495dd1646
$ … --root …/receipt-bytes …
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET      exit=0
```

The predicate text says "whose anchor cell carries the sha256 **of the named receipt**".
The code tests "carries the string frozen.json recorded". Nothing measures the receipt.
`c1-digest` mutates the *row cell* (S210 cell 5 → zeros), so it kills the coded clause and
nothing else; **no control exercises receipt bytes**, and the clause ledger lists
`digest-match` as live and covered. For the record the real receipts are honest — all
8/8 hash to their frozen values — so this is a counter defect, not a data defect.

**Smallest safe correction** — one conjunct, after `receipt["sha256"] in cs[5]`:

```python
                and digest == receipt["sha256"]
```

Tested on a patched copy in scratch (`scratch/CritControls/count-fixed.py`), same
`frozen.json`:

| tree | unpatched | patched |
|---|---|---|
| `.` real lane root | `3/8/0 TARGET_MET` rc 0 | `3/8/0 TARGET_MET` rc 0 |
| `controls/golden` | `3/8/0 TARGET_MET` rc 0 | `3/8/0 TARGET_MET` rc 0 |
| `scratch/…/minal-shaved` (1251 B junk) | `3/8/0 TARGET_MET` rc 0 | `0/0/8 TARGET_MISSED` rc 1 |
| `scratch/…/receipt-bytes` (corrupted receipt) | `3/8/0 TARGET_MET` rc 0 | `2/7/1 TARGET_MISSED` rc 1 |

One line separates fabricated evidence from real evidence; the round's claim survives
it. It does **not** repair §4's registry-level indifference (`golden` still passes with
`on-change` where the real data says `on-request`, and a different cell-6 claim), which
needs a clause relating row content to entry content and is a predicate change, not a
one-line fix — out of scope here.

---

## Verdict

- **Kill rule, as receipts:** discharged. 11/11 control trees reproduce their committed
  stdout and exit code exactly; golden `MET`, ten defect controls `MISSED`. Nothing to
  correct.
- **Kill rule, as guarantee:** the receipt set proves *liveness* of eight clauses and
  *reachability* of `TARGET_MET`. It does not prove that a receipt's `2/7/1` came from
  the clause the receipt is named for (§2), and it does not bind receipt content (§5).
- **The target is shape-reachable at 1251 bytes of zero knowledge** (§3), and the
  counter cannot distinguish that tree, the real data, or the round's own divergent
  golden registry from each other (§4).
- **Fixable defect, not a tradeoff:** `digest == receipt["sha256"]`. Add the conjunct,
  re-run the eleven controls — all eleven keep their current receipt lines, since none of
  them touches receipt bytes — and commit a twelfth control
  (`c1-receipt-bytes`: real tree, one receipt with a byte appended) whose receipt would
  read `2/7/1 MISSED` only after the fix. That control is what §5 is missing.

## Reproduction

Scratch, all under `.ufo/waves/round-35/scratch/CritControls/`:

| path | what |
|---|---|
| `minimal/` | 1259 B first-cut minimal tree |
| `minal-shaved/` | 1251 B floor tree (§3) |
| `receipt-bytes/` | golden + corrupted `S203.receipt.txt` (§4, §5) |
| `hardlink-receipt/` | golden + hardlinked receipt, `closed_rows=7` (§3) |
| `empty-receipt/` | golden + emptied receipt, `2/7/1` (§3) |
| `empty-quote/` | golden + empty `S203` quote, `2/7/1` (§3) |
| `sha-only/` | minimal with receipts replaced by digests, `0/0/8` (quote binding is the only receipt requirement) |
| `count-fixed.py` | `c1/count.py` + the one-line digest conjunct (§5) |
| `*.out`, `*.err` | captured stdout/stderr of the eleven runs (§1) |

Unverified / not attempted: nothing in this report rests on an unquoted run. I did not
re-derive C2; I did not judge, admit, edit, integrate or ship anything; no installs, so
no tool record.
