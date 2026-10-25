# Round-36 report errata owed to round-35 (crate-text corrections)

Scribe seat: `ScribeReportErrata`, mado round 36 wave 1.
Target: the round-36 fleet report is to carry these three errata for the
round-35 report (`.ufo/reports/round-35/mado.md`). Draft only — the fleet
report itself is not edited (write-limit: `scratch/ScribeReportErrata/`).

All numbers below are the ones `ScoutD1Facts`, `ScoutD6Rows` and
`ScoutD7Counts` report under `.ufo/waves/round-36/w1/reports/` (all read at
final draft time).


---

## D1 — report-lands-last and tip citation

Round-35 report text (`.ufo/reports/round-35/mado.md:94` at `763734e1`):

> Lane tip at closure: the tip named by `git -C mado-shokunin rev-parse master`
> at read time (the lane kept moving as seats finished; see the sweep list
> below) (`ahead=0`, working tree clean). The tip moved twelve times inside
> round 35 — `02088b4` data, `4f35c80` errata, `7b745a1` axis republication,
> then evidence-and-closure sweeps — which is the provenance defect
> `SentBoundary` routed.

Correction: the round-35 lane tip at closure is
`7a068cbee3b0983230b8fb8467c02e12772832dd` ("round-35: close",
2026-10-25 03:53:37 -0300). The report named no fixed tip hash; it deferred
to `rev-parse master` at read time. The report's **last** committed version
(`763734e1`, committer 2026-10-25 03:53:15 -0300, "mado report — the
row-section gap and the dead digest store named per seat") landed **before**
three lane commits — `567945e`, `2eddc38`, `7a068cb` (committer dates
03:53:26 / 03:53:32 / 03:53:37) — so the report did not land last and did not
cite the tip hash. `[pending scout]` ScoutD1Facts re-derivation of the exact
one-sentence erratum wording and the fleet-commit report first-land. The
round-36 report should state the tip hash `7a068cb…` and follow the
report-after-last-commit convention going forward.

---

## D6 — corrected row-correction count

Round-35 report text (`.ufo/reports/round-35/mado.md:133-134` at `763734e1`):

> Rows touched old→new: **0** — no existing row's `status`/`recheck`/`used-by`
> changed; four of the new rows' `scope`/`teaches` cells were corrected in-round
> to match the entry errata.

Correction (`ScoutD6Rows` verdict: **confirmed**): committed bytes show exactly
**three** rows changed, `S203`, `S204`, `S205` (`git diff --numstat 02088b4
7a068cb -- corpus/SOURCES.md` → `3 3`, one commit `4f35c80` touched the file in
the range), and the corrected cells are `teaches` (3 rows), `recheck` (2 rows),
`scope` (1 row) — so the round-35 wording is wrong twice: the count (four →
three) and the cell set (it omitted `recheck`). SCORECARD.md already carries the
corrected figure (commit `7d708cf`); the round-36 report needs the matching
erratum.

---

## D7 — stale seat-report count

Round-35 report text (`.ufo/reports/round-35/mado.md` at `763734e1`):

- line 39 (Work-performed bullet): `` `.ufo/waves/round-35/w2/reports/` (38 reports) ``
- line 88 (commit-table row for `4f35c80`): "… the committed content cribs, the
  **38 wave-2 reports**, `scratch/L1DigestFix` …"
- line 194: "Dead/no-report seats: wave 2 dispatched 40; **40 wrote reports** …"

Per-revision counts (`ScoutD7Counts` verdict: **D7 upheld exactly**):

| revision | `.md` count in `.ufo/waves/round-35/w2/reports/` | supports / contradicts |
|---|---|---|
| `4f35c80` | 37 | contradicts both "38" sentences (lines 39 and 88) |
| `7b745a1` | 37 | contradicts both "38" sentences (identical listing to `4f35c80`) |
| `7a068cb` (round-35 tip) | 40 | supports line 194's "40 wrote reports" |

38 was never committed at any revision (the count jumps 37 → 40 at
`b632f0b`); the round-36 report should say which revision each count describes.

---

## Verification notes (read-only, run at draft time)

The values above were cross-checked directly against the lane:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
git diff --numstat 02088b4 7a068cb -- corpus/SOURCES.md
# 3	3	corpus/SOURCES.md
for rev in 4f35c80 7b745a1 7a068cb; do
  git ls-tree --name-only $rev .ufo/waves/round-35/w2/reports/ | grep -c '\.md$'
done
# 37 / 37 / 40
git show -s --format='%h committer:%cd %s' --date='iso-strict' 567945e 2eddc38 7a068cb
# 567945e committer:2026-10-25T03:53:26-03:00 … 2eddc38 …03:53:32… 7a068cb …03:53:37…
```

Report-text line numbers above are for the report tip `763734e1`
(`git show 763734e1:.ufo/reports/round-35/mado.md`); `ScoutD7Counts` cites the
same sentences at lines 39/85/191 in the earlier version `af1e1ca5` (the
3-line offset comes from the three bullet lines added by `763734e1`).
