# RevAxisStale — is the published axis table stale? (round-35, w1, rev seat)

2026-10-24. Scope: read the last `Axis table re-derived at` publication in
`SCORECARD.md`, name the three counters it publishes, re-run each at the repo
as it stands, and compare published vs derived fractions. Leaf seat, no
dispatch. Instruments were re-run at write time; every output below is quoted
from this session, not copied from a ledger.

## Verdict

**Not stale.** All three derived fractions equal the published fractions at
HEAD `19e4ab3171c1540c40d6b12097745af98053b07d`. The committed gate agrees,
exit 0:

```
$ python3 -I quality/check-axis-scores.py --repo . ; echo "exit=$?"
MADO_AXIS_ROW: axis=navigation published=47/47 derived=47/47 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=41/41 derived=41/41 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=19e4ab3171c1540c40d6b12097745af98053b07d
exit=0
```

## Published vs derived, side by side

Publication under test — `SCORECARD.md:2110` (last `Axis table re-derived at`
marker; landed in `dff3941`, round-34 claim rows, 2026-10-24 22:46 -0300).
The three counters it names, with each instrument re-run at HEAD:

| Axis | Published (`SCORECARD.md:2110`) | Derived at `19e4ab31…` | Instrument (re-run, quoted) | Verdict |
|---|---|---|---|---|
| navigation | 47/47 = 1.0 | 47/47 | `python3 -I quality/check-index.py --rev 19e4ab3171c1540c40d6b12097745af98053b07d --repo .` → `MADO_INDEX: rev=19e4ab3171c1540c40d6b12097745af98053b07d indexed=47/47 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | MATCH |
| calibration resolved-active | 41/41 = 1.0 | 41/41 | `python3 -I .ufo/waves/round-31/c2/count.py 19e4ab3171c1540c40d6b12097745af98053b07d` → `METRIC active=41 resolved_active=41 fraction=1.0000` | MATCH |
| operability selftest | 12/12 = 1.0 | 12/12 | `python3 -I quality/check-index.py --selftest` → `MADO_INDEX_SELFTEST: 12/12 assertions passed` | MATCH |

## Why it is still fresh one commit later

The publication says "at the round-34 data tree", but HEAD is the round-35
freeze `19e4ab31…` ("round-35: freeze C1 and C2 predicates, the clause ledger,
the control receipts and the re-issued blob ledger"). That commit touched only
`.ufo/` paths (`git show 19e4ab31… --name-only --format= -- . ':!.ufo'` →
empty): no `corpus/knowledge/` note, no `corpus/README.md` row, no
`SCORECARD.md`/`SHONEN.md` edit — none of the three counters' surfaces moved,
so the fractions happen to carry over unchanged.

Working-tree check: `git status --porcelain` shows only untracked
`.ufo/waves/round-35/` runtime (`dispatch-w1.sh`, `dispatch.out`, `scratch/`,
`w1-spec.json`, `w1-taskcall.json`, `w1/`). All three instruments are
commit-based (`--rev` / blob reads), so untracked runtime cannot move them;
this report, once committed under `.ufo/waves/round-35/`, is likewise outside
every counter surface.

## Caveat (label, not fractions)

The publication's state label ("round-34 data tree") is one round behind HEAD,
while its fractions remain correct. If round-35 lands a knowledge note or a
SCORECARD/SHONEN cite without appending a fresh `Axis table re-derived at`
line, `quality/check-axis-scores.py` will go red (`STALE`), which is the
designed tripwire — no correction is owed today.
