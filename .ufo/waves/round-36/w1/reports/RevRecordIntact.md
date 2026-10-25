# RevRecordIntact — reviewer report (mado round 36, wave 1)

Seat: `L1Mado36.RevRecordIntact`. Assignment: verify that the `record_intact`
guard is what stops a record rewrite from looking like a repair — read the
gate's `SUPERSEDED_POINTERS` and the round-35 LOG entry that cites them; then,
in `/tmp`, delete those two pointer mentions from a copy of `LOG.md` and show
the gate's `dangling_r35_closed` stays 0, quoting both runs. Lane HEAD =
`dbf8b57` (the freeze commit; `master` = `HEAD` verified). All lane work
read-only; the mutation was applied only to a `--no-hardlinks` clone under
`/tmp/revrecordintact/lane-mut`. No tools installed; no production bytes
touched.

## 1. The guard and the pointers it protects

`quality/check-evidence-pointers.py:50-53` (the C2 gate, `PRED-PTR-r36-v1`):

```python
SUPERSEDED_POINTERS = (
    ".ufo/waves/round-35/scratch/SimplifyCounter/",
    ".ufo/waves/round-35/scratch/MutC1Drop/mutants/",
)
```

Both are directory pointers (trailing `/`), resolved at gate time by
`resolves()` (`:107-112`) against `git ls-tree -r --name-only <rev>` — i.e.
they are *backticked citations in the records*, not necessarily tracked
paths.

`record_intact` is defined at `:152`:

```python
record_intact = all(p in ptr35 for p in SUPERSEDED_POINTERS)
```

and is a conjunct of the round-35 closure metric at `:160`:

```python
dangling35_closed = 1 if (record_intact and closed == len(dangling35)) else 0
```

where `closed` (:154-159) counts dangling round-35 pointers that a
`- \`old\` -> \`new\`` pair in the round-36 LOG section supersedes to a path
that resolves. `dangling35_closed` feeds the top-level `met` conjunction at
`:194`.

Why this matters: `ptr35` is *mined from the round-35 text* (`:141,145` —
LOG.md and SCORECARD.md round-35 sections). If an editor deletes the two
mentions, `dangling35` shrinks; with no other danglers it becomes `[]`,
`closed == len(dangling35)` is `0 == 0` → True, and without the
`record_intact` conjunct the metric would report the round-35 record fully
"closed" — a rewrite indistinguishable from a repair. `record_intact` is
the only term in `:160` that remembers the mentions were supposed to exist.

## 2. Where the pointers are cited

`LOG.md` round-35 section, verified at `dbf8b57` — two seat-scratch entries,
one pointer each:

- `LOG.md:1999` `## Round 35 — SimplifyCounter seat scratch (2026-10-24, wave-1)`
  → `LOG.md:2003`:
  `` `.ufo/waves/round-35/scratch/SimplifyCounter/` (`count-min.py`, 104 lines vs ``
- `LOG.md:2016` `## Round 35 — MutC1Drop seat scratch (2026-10-24, wave-1)`
  → `LOG.md:2020`:
  `` copies under `.ufo/waves/round-35/scratch/MutC1Drop/mutants/` (15 mutants, ``

`grep -n "SimplifyCounter\|MutC1Drop" LOG.md` returns only these lines plus
the sibling citations `w1/reports/SimplifyCounter.md` (:2014) and
`w1/reports/MutC1Drop.md` (:2033) — which *resolve* (tracked) and are not in
`SUPERSEDED_POINTERS`. SCORECARD.md's round-35 section contributes one
pointer (`.ufo/waves/round-35/registration.md`); re-implementing the gate's
miner over working-tree LOG+SCORECARD gives 8 round-35 pointers, matching
the gate's own `pointers_r35=8` below.

## 3. Baseline run (unmutated lane, committed record)

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && \
  python3 quality/check-evidence-pointers.py --repo .
PRED-PTR-r36-v1 rev=master pointers_r35=8 dangling_r35=2 dangling_r35_closed=0 \
  pointers_r36=0 dangling_r36=0 inherited_dirty=0 scratch_tracked=124 \
  scratch_disposition_ok=0 tip_axis_transcript=0 setup=missing-r36-sections \
  verdict=TARGET_MISSED
dangling_r35: .ufo/waves/round-35/scratch/SimplifyCounter/
dangling_r35: .ufo/waves/round-35/scratch/MutC1Drop/mutants/
tip_axis: none
exit=1
```

Baseline read: the two `SUPERSEDED_POINTERS` are exactly the two dangling
round-35 pointers (`git ls-tree -r --name-only HEAD | grep` finds no tracked
file under either directory; `scratch_tracked=124` confirms other round-35
scratch *is* tracked, so their absence is real). `record_intact` is True
here; `dangling_r35_closed=0` because `closed=0 < len(dangling35)=2` — no
round-36 supersession pairs exist yet (`pointers_r36=0`,
`setup=missing-r36-sections`), consistent with the frozen before-receipt
`.ufo/waves/round-36/receipts/before-pointers.txt` = TARGET_MISSED.

## 4. Mutation (in /tmp only) and the required run

Setup:

```
$ git clone --no-hardlinks -q /home/vgpnk/Projects/shokunin/mado-shokunin lane-mut
$ cd lane-mut && git checkout -q dbf8b57 -b master-mut
```

Mutation: deleted exactly the two backticked `SUPERSEDED_POINTERS` mentions
(`LOG.md:2003`, `:2020` — each replaced with untokened prose; every other
byte of LOG.md untouched), committed as `de32ef676b0b837cfc2bec8278d77e9a08c70cf3`:

```
$ git log --oneline -2 master-mut
de32ef6 mutant: delete superseded-pointer mentions from round-35 LOG
dbf8b57 round-36: freeze both predicates, the control manifest, the cribs and the before receipts
```

Run 2 (real gate, mutated repo — **the assignment's required run**):

```
$ python3 /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-evidence-pointers.py \
    --repo . --rev master-mut --branch master-mut
PRED-PTR-r36-v1 rev=master-mut pointers_r35=6 dangling_r35=0 dangling_r35_closed=0 \
  pointers_r36=0 dangling_r36=0 inherited_dirty=0 scratch_tracked=124 \
  scratch_disposition_ok=0 tip_axis_transcript=0 setup=missing-r36-sections \
  verdict=TARGET_MISSED
tip_axis: none
exit=1
```

The rewrite fully succeeded on the record's own terms — `pointers_r35` fell
8→6 and `dangling_r35` fell 2→**0**: after the edit, nothing in the
round-35 text references the superseded scratch dirs, so nothing dangles.
Yet **`dangling_r35_closed` stays 0** — the gate does not read the rewrite
as the record being closed/repaired.

## 5. Attribution: `record_intact` is the operative conjunct

Same mutated repo, counterfactual gate with only the `record_intact`
conjunct removed (`dangling35_closed = 1 if (closed == len(dangling35))`,
script copy at `/tmp/revrecordintact/gate-noguard.py`):

```
$ python3 /tmp/revrecordintact/gate-noguard.py --repo lane-mut \
    --rev master-mut --branch master-mut
PRED-PTR-r36-v1 rev=master-mut pointers_r35=6 dangling_r35=0 dangling_r35_closed=1 \
  pointers_r36=0 dangling_r36=0 inherited_dirty=0 scratch_tracked=124 \
  scratch_disposition_ok=0 tip_axis_transcript=0 setup=missing-r36-sections \
  verdict=TARGET_MISSED
exit=1
```

`dangling_r35_closed` flips 0→1 on the identical mutated record. The only
difference between the two runs is the `record_intact` conjunct at
`check-evidence-pointers.py:160`. This isolates it as the operative term:
deleting the mentions satisfies `closed == len(dangling35)` vacuously
(0 == 0), and only `record_intact` — which demands the superseded pointers
still appear in the mined round-35 record — keeps the metric at 0.

## 6. Verdict

**PASS.** `record_intact` is what stops a record rewrite from looking like
a repair:

- Required demonstration, both runs quoted (§3, §4): mentions deleted in a
  `/tmp` clone → `dangling_r35=0` but `dangling_r35_closed=0`.
- Attribution (§5): guard-removed counterfactual on the same bytes yields
  `dangling_r35_closed=1`; the `record_intact` conjunct at
  `quality/check-evidence-pointers.py:160` is the sole difference.

Residual notes (out of scope, no action implied): the guard holds because
the superseded dirs have no tracked children *and* no supersession pairs —
the rewrite path is the one exercised. A rewrite that instead *redirected*
the mentions (e.g. pointed them at existing paths) would still be caught,
since `record_intact` requires the exact original tokens, not resolvable
ones. The metric is binary per-record: it verifies the *mentions* persist,
not that the cited prose is unmodified around them.

Installs: none. Scratch: `/tmp/revrecordintact/` (clone + counterfactual
script); lane bytes unmodified (`git status` delta unchanged by this seat).
