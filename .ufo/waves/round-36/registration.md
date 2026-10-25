# Round 36 — registration (frozen before any round-36 data)

Lane: mado-shokunin. Round: 36. Base: `4243d031e3441f5063f92c33aa58377c6f9ff120`
(`master`, pushed; the round-35 verifier spot-check commit).
Prompt: `/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-36.md`.
Written after reading `MISSION.md`, `AXES.md`, `CORPUS.md`, `LEARNING.md`,
`PROTOCOL.md`, the lane `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`,
`corpus/QUALITY.md`, `corpus/README.md` and
`corpus/lessons/round-35-verifier-spotcheck.md` (the non-author check of round
35, which routed defects D1–D10 and rejected C2 as `unprovable`).

Round 35 closed on the spot-check's verdict: C1 `improved` (re-measured), C2
`unprovable` — "the round demonstrates the instrument is vacuous". The routed
defects D3 (C1's counter is shape-scored: the digest is computed and discarded)
and D4 (C2's observables are fail-open: the ledger scans its own clause list,
covered clauses are `verdict=TARGET_MISSED` token greps, `ledger_tip_ok` is a
substring test over prose) are the two the operator's claim-sizing lesson calls
out: *every declared claim must be one a do-nothing control cannot reach and
that your instrument cannot pass fail-open*. This round takes exactly those two
and nothing else as claims.

## Claims (2; distinct axes; causally separable)

### C1 — calibration: the two round-35 admission counters are repaired and shown to discriminate

Axis: **calibration** (self-assessment quality: overreach caught). This is one
of the two axes tied at the lowest published score (`calibration 43/43` = 10.0,
`saturation` 9.0, N=3; a capability row entered in round 34, so the
`AXES.md` stagnation nudge does **not** waive the lowest-axis obligation).

Subject: the lane's own admission instruments for the round-35 claims. Repaired
as standing tools under `quality/counters/`:

- `quality/counters/c1-idle-lock.py` — `PRED-C1-r36-v1`: the round-35 counter's
  nine live clauses kept, with the dead `digest-match` clause bound to the bytes
  actually read and a `row-in-registry` clause added (the census's E12 fence,
  routed by round-35's `RevC1Tip` F2).
- `quality/counters/c2-ledger.py` — `PRED-C2-r36-v1`: the ledger is parsed, the
  clause set is pinned by the frozen spec (a deleted clause is uncovered, not
  skipped), every load-bearing clause must name a control whose committed
  receipt records a `TARGET_MISSED` **and** names that clause, and the tip is
  computed from git by one frozen rule instead of grepped from prose.

Frozen predicate text lives verbatim in `.ufo/waves/round-36/{c1,c2}/frozen.json`;
each counter refuses to run (`error=predicate-drift`, exit 2) if its own text or
target differs.

**Counting command** (one command, two profiles, before and after):

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I quality/check-counter-discrimination.py --profile r35 \
  --manifest .ufo/waves/round-36/controls/manifest.json \
  --receipts .ufo/waves/round-36/controls/receipts-r35  # before
python3 -I quality/check-counter-discrimination.py --profile r36 \
  --manifest .ufo/waves/round-36/controls/manifest.json \
  --receipts .ufo/waves/round-36/controls/receipts  # after
```

Prints one line per control (`control=<id> instrument=<c1|c2> expected=<v>
observed=<v> ok=<1|0>`), then
`MADO_DISCRIMINATION: profile=<p> controls=N correct=C/N verdict=<...>`, then the
clause-binding table `clause=<id> controls=<n> missed=<n>`.

**Target: `correct == controls`** (N = 25 in the frozen manifest: 3 accept
controls, 22 reject controls). Exit 0 iff met; exit 1 otherwise; exit 2 on
setup error.

**Kill rule (the counter must be able to fail):** the counter reports
`TARGET_MET` only when *every* control is classified correctly, so a degenerate
instrument cannot reach it — an instrument that always rejects fails the 3
accept controls, an instrument that always accepts fails the 22 reject controls,
an instrument that crashes (exit 2 or no verdict line) is counted `ERROR`, never
`ok`. Frozen before data.

**Do-nothing control (built before any data, scored with the frozen counter):**
the round-35 counters themselves, unmodified, under `--profile r35`. They must
score **below** N; if they score N the control set is wrong and no data is
taken. Recorded at freeze in `.ufo/waves/round-36/receipts/before-discrimination.txt`; the
repaired profile's own before-state is the same command with `--profile r36` at the
freeze commit, where `quality/counters/` does not yet exist and every leg reads
`ERROR` (an unbuilt instrument is never a pass).

The fifteen `c1` cribs are committed trees. The eight `c2` fixtures are generated
outside the lane (`/tmp/mado-r36-mutants-<profile>`) by the committed generator,
because they are byte-deterministic from the committed ledger and criterion 39 asks
for the regenerating command, not the tree.

### C2 — operability: the lane's records pass an evidence-pointer durability gate

Axis: **operability** (runnable artifacts: a checklist item can be run and
produces the stated outcome). Tied-lowest with C1.

Subject: the routed record defects D1, D2, D5, D6, D7, D8, D9, D10 — every one
of them a pointer, count or disposition in the lane's own records that a reader
cannot re-derive from committed bytes. The gate is the deliverable:

`quality/check-evidence-pointers.py` — `PRED-PTR-r36-v1`, five observables:

| Observable | Rule |
|---|---|
| `dangling_r35_closed` | for every lane-relative evidence pointer cited in the round-35 `LOG.md` entry and `SCORECARD.md` sections that does not resolve at the checked tree, a round-36 correction pair `` - `old` -> `new` `` in `LOG.md` must carry it as `old` with a `new` that resolves |
| `dangling_r36` | lane-relative evidence pointers cited by the round-36 `LOG.md` entry, `SCORECARD.md` sections and `corpus/lessons/round-36.md` that do not resolve — must be 0 |
| `inherited_dirty` | the ten round-35 closure paths still reported by `git status --porcelain` — must be 0 |
| `scratch_disposition_ok` | the round-36 lesson names a disposition for `.ufo/waves/round-35/scratch` and states a path count equal to `git ls-tree -r --name-only <rev> .ufo/waves/round-35/scratch \| wc -l` |
| `tip_axis_transcript` | a committed `quality/receipts/axis-<40hex>.txt` exists, `<40hex>` is an ancestor of the branch tip, and its `MADO_AXIS:` line reads `mismatched=0 rev=<40hex>` |

**Counting command:**

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I quality/check-evidence-pointers.py --rev <rev> --repo .
```

**Target: `dangling_r35_closed == dangling_r35_found AND dangling_r36 == 0 AND
inherited_dirty == 0 AND scratch_disposition_ok == 1 AND tip_axis_transcript ==
1`**, exit 0. Absence is never a pass: if the round-36 record sections do not
exist the gate prints `setup=missing-r36-sections` and exits 1.

**Do-nothing control:** run the same gate at the freeze commit — it must read
`TARGET_MISSED`. It does: the round-35 record cites two paths that are absent at
the tip (D5: `.ufo/waves/round-35/scratch/SimplifyCounter/`,
`.ufo/waves/round-35/scratch/MutC1Drop/mutants/`), the ten inherited paths are
dirty, no disposition exists and no tip-revision axis transcript was committed.

## Control manifest — frozen before data

`.ufo/waves/round-36/controls/manifest.json`. N = 25.

| Instrument | Accept | Reject |
|---|---|---|
| `c1` | `c1-live` (the lane), `c1-golden-r36` | 14: `c1-donothing`, `c1-digest`, `c1-entry-symlink`, `c1-quote-absent`, `c1-quote-long`, `c1-recheck-prose`, `c1-row-duplicate`, `c1-row-extra-field`, `c1-status-queued`, `c1-usedby-extra`, `c1-shape-only`, `c1-fabricated-payload`, `c1-no-registry-heading`, `c1-row-moved-out` |
| `c2` | `c2-live` | 8: `c2-tip-stale`, `c2-tip-one-copy`, `c2-blob-corrupt`, `c2-blob-row-deleted`, `c2-clause-deleted`, `c2-receipt-token`, `c2-receipt-unbound`, `c2-retired-also-live` |

The two content cribs are the round-35 committed trees
(`.ufo/waves/round-35/controls-content/`), which the round-35 counter accepts;
`c1-golden-r36`, `c1-no-registry-heading` and `c1-row-moved-out` are round-36
trees (the first is the round-35 `golden` with the live registry's
`## Registry` section restored; the other two remove or move that fence).

The eight `c2` controls are **mutation kinds**, not fixed trees: at data time
`.ufo/waves/round-36/c2/gen-mutants.py` materialises each kind from whichever
ledger the profile names (round 35's for the before run, round 36's for the
after run) and copies every file the counter reads, so a mutant differs from the
accept control in exactly one committed input. The kinds are frozen here; a kind
added after the before receipt is a new claim, not this one.

Demonstration obligation for every `c2` control: the same mutation kind must be
shown to be *accepted* by the round-35 counter (before) unless the round-35
counter already killed it — both directions are recorded in the receipts, never
asserted.

## Multiple-comparison and harm watch (every claim)

- `bash tools/mado-verify.sh --selftest` stays green (the gate is not touched).
- `python3 quality/check-index.py --repo .` stays complete.
- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
  exits 0 at round end.
- No config tree, compositor state, sibling repo or `/home/vgpnk/Projects/shokuknow`
  write. All host reads are the declared read-only planes.
- No axis is harmed: `git diff <base> <tip> -- SCORECARD.md` carries no lowered
  row; the three published axis fractions must not decrease.

## Saturation, retirement, assimilation, considerthese

- Saturation 9.0, stagnation window N=3 — unchanged.
- **Retirement this round:** `sourced-art` (published 1.0 in round 32, dropped
  from the publication in round 34 while `## Retired` still read "none") is
  retired explicitly in `SCORECARD.md` with its reason, per round-35's recorded
  r36 item. No other axis is retired.
- **Assimilation: none this round.** Round 35 adopted the `merge/mado/` core
  theme (three entries, eight rows) and its counter is the instrument this round
  repairs; §10 allows a round to declare `Assimilation: none` without penalty.
  The package is not re-adopted while its evidence chain is under repair.
- **considerthese:** one still-unimplemented proposal from
  `considerthese/2026-10-24.md` — proposal 1, "track a domain-versus-meta ratio
  per window … flag when the lane goes two or more rounds without a
  desktop-facing change" — lands as a `QUALITY.md` criterion plus the round
  report's own ratio line. It points at the 42-commit window the file measures;
  the reflection is a pointer, not evidence, so the criterion is grounded in the
  lane's own commit record re-derived this round.

## Round shape (declared)

Two v1 waves under `scripts/hyaku/ufo-wave-policy.json` (band 32–64): wave 1 —
build (64 seats), wave 2 — falsify (32–64 seats) only if wave 1 yields ≥32
distinct attack items. `planner` is held by the L1; the planning data-walk rides
`connector`/`scout` items. Residual checks, if any, go in one ordinary `task`
call of ≤8 seats counted in the total.
