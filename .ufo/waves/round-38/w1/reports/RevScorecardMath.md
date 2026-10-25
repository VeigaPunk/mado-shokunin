# RevScorecardMath — r38 w1: independent recomputation of the axis math

Reviewer: L1Mado38.RevScorecardMath (leaf; no subagents). Read-only on production
files; the only bytes I wrote are this report. No tools installed.

## What I attacked

The axis after-state the round-38 report will claim — navigation, calibration
(resolved-active), operability (selftest) — given the landed artifacts (v3
counters, the new request-ground counter, three entries), the Move-log rows,
and the axis publication the lane's own gate parses.

## The pinned instruments (SCORECARD's AXES block)

SCORECARD.md:1-6 (the AXES block):

> Lane axes per AXES.md (six-axis vocabulary; primary verdicts per
> LEARNING.md trends). Probation rounds 1-3 build the initial measurements.
> Axes will be pinned with their counting commands as rounds land.

The counting commands are pinned in `quality/check-axis-scores.py` (docstring,
the gate the registration's lowest-axis rule invokes):

```
Axes re-derived (frozen set):
  navigation   quality/check-index.py --rev <rev> --repo .   -> indexed=A/B
  calibration  .ufo/waves/round-31/c2/count.py <rev>         -> resolved_active=A active=B
  operability  quality/check-index.py --selftest             -> A/B assertions passed
```

The gate takes the LAST unquoted `Axis table re-derived at` publication in
SCORECARD.md and compares it against the values re-derived at `--rev`; any
mismatch is exit 1. AXES.md (fleet root) defines calibration as
"SHONEN.md/SCORECARD entries match observed repo state".

## Measurements (exact commands, quoted output)

Lane HEAD = `bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5`; r38 base =
`f6e3247f73152a39afb86066af48f3cedf95fb0a`; chain: `58e55ec` (freeze) →
`245065c`/`efb0ec2` (data) → `859d0cf`/`b6c1d31` (counter/manifest fixes) →
`f0c9432`/`bb1adce` (records).

| rev | navigation (derived) | calibration (derived) | operability (derived) | gate |
|---|---|---|---|---|
| base `f6e3247` | 52/52 | 50/50 | 12/12 | `mismatched=0` exit 0 |
| data `efb0ec2` | **55/55** | 50/50 | 12/12 | (publication still 52/52) |
| records `f0c9432` | 55/55 | 50/50 | 12/12 | `mismatched=1` exit 1 — navigation STALE |
| tip `bb1adce` | 55/55 | 50/50 | 12/12 | `mismatched=1` exit 1 — navigation STALE |

- Base (`.ufo/waves/round-38/receipts/axis-base.txt`, quoted):
  `MADO_AXIS_ROW: axis=navigation published=52/52 derived=52/52 verdict=MATCH` /
  `axis=calibration published=50/50 derived=50/50 verdict=MATCH` /
  `axis=operability published=12/12 derived=12/12 verdict=MATCH` /
  `MADO_AXIS: checked=3 mismatched=0 rev=f6e3247f73152a39afb86066af48f3cedf95fb0a`.
- Tip: `python3 -I quality/check-index.py --rev bb1adce… --repo .` →
  `MADO_INDEX: rev=bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5 indexed=55/55 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0.
- Tip: `python3 -I quality/check-index.py --selftest` →
  `MADO_INDEX_SELFTEST: 12/12 assertions passed`, exit 0.
- Tip: `python3 -I .ufo/waves/round-31/c2/count.py bb1adce…` →
  `METRIC active=50 resolved_active=50 fraction=1.0000` …
  `PRED-C2-r31-v2 verdict=TARGET_MET`, exit 0 (7 pre-existing WARN lines on
  outside-lane refs — QUALITY.md is untouched this round, so they are not r38-caused).
- Tip gate: `MADO_AXIS_ROW: axis=navigation published=52/52 derived=55/55 verdict=STALE` …
  `MADO_AXIS: checked=3 mismatched=1 rev=bb1adce…`, exit 1. Same at `f0c9432`.
- Denominators: `git ls-tree --name-only <rev>:corpus/knowledge | wc -l` →
  base 52, HEAD 55. `git diff --stat f6e3247..HEAD` touches only SCORECARD.md
  (+16), corpus/README.md (+14), corpus/SOURCES.md (+8/−2) and the three new
  entries (+48/+50/+60) — **corpus/QUALITY.md and quality/check-index.py are
  untouched by every r38 commit** (`git log f6e3247..HEAD -- corpus/knowledge
  corpus/QUALITY.md` → only `efb0ec2`, `245065c`).
- Counter before/after: `--rev f6e3247` → `admitted=0/3 verdict=TARGET_MISSED`
  exit 1; `--rev efb0ec2` and `--rev HEAD` → `admitted=3/3 verdict=TARGET_MET`
  exit 0 (entries `hyprctl-flags-r28.md` ids=S221, `request-socket-live-bound-r8.md`
  ids=S158,S187,S277, `request-limits-upstream-r31.md` ids=S253; all indexed —
  6 README rows match the three names at HEAD).

## Correct after-state (the answer)

| Axis | r37 published | r38 correct after-state | Why |
|---|---|---|---|
| navigation | 52/52 | **55/55** (fraction 1.0 → 1.0; denominator 52→55) | the three entries landed at `245065c`/`efb0ec2` and are indexed; every r38 commit after them adds no entry |
| calibration resolved-active | 50/50 | **50/50** (unchanged) | corpus/QUALITY.md untouched; counter `resolved_active=50 active=50` |
| operability selftest | 12/12 | **12/12** (unchanged) | quality/check-index.py untouched; selftest 12/12 |

As 0–10 fractions all three stay 10.0000. As **published A/B cells** — the
thing the gate parses — navigation must move to 55/55.

## Findings

- **F1 (major) — SCORECARD.md:2420-2422 publishes the stale cell and mislabels
  the move.** Quote: "Axis table at `f0c9432`: navigation 52/52, calibration
  resolved-active 50/50, operability selftest 12/12 — the moves above are
  instrument and domain moves, not axis-score changes." The domain move IS a
  navigation axis move on the published cell: the lane's own gate re-derives
  `published=52/52 derived=55/55 verdict=STALE` at `f0c9432` and at HEAD, exit 1.
  Round 36 set the precedent (`quality/receipts/red-axis-publication-stale-at-data-commit.txt`):
  a stale publication at the data commit is a defect the records commit repairs
  by appending the re-derived table. The report must not repeat this sentence.
- **F2 (major) — no r38 axis publication exists.** The last unquoted
  `Axis table re-derived at` in SCORECARD.md is still round 37's (SCORECARD.md:2398-2399:
  "Axis table re-derived at `3f424257…` … navigation 52/52; calibration
  resolved-active 50/50; operability selftest 12/12."), so
  `python3 -I quality/check-axis-scores.py --repo . --rev master` exits 1 at
  HEAD. The tail sentence ("Axis table at `f0c9432`") is not parsed — the gate's
  marker is `Axis table re-derived at`. Exact repair line proposed below.
- **F3 (minor) — the two landed r38 Move-log rows are orphaned.** SCORECARD.md:200-201
  sit between the fleet-round-1 erratum prose (:198) and `## Capabilities` (:202),
  detached from the `## Move log` table header (:9-10); they render as a
  headerless fragment, not Move-log rows. The coverage row below should land
  adjacent to them, and the records commit should consider relocating the trio
  under the real table header.
- **F4 (minor) — the registration's unheld-ground sentence overstates the base
  grep.** registration.md §C2 says base `git grep` "finds no `flag list`, …".
  Measured: `git grep -F 'flag list' f6e3247 -- corpus/knowledge` hits 2×
  (`walker-deep.md:314`, `waybar-walker-plane.md:480` — both the walker
  `--help` flag list, not hyprctl flags); `select instance`, `poll(pollfds`,
  `REQUEST_LIMIT`, `FOLLOW_QUEUE_LIMIT` are 0-hit. The intent (no hyprctl-flag
  vocabulary at base) survives; the sentence as written is false.
- **F5 (info)** — the calibration counter's 7 WARN lines are pre-existing
  outside-lane refs; not r38-caused (QUALITY.md unchanged).

## Proposed Move-log row (exact text to append)

The only missing axis row — calibration and operability rows already landed at
SCORECARD.md:200-201. Append immediately after :201:

```
| 38 | coverage | corpus/knowledge held 0 request-socket entries at base `f6e3247` — `select instance`, `poll(pollfds`, `REQUEST_LIMIT`, `FOLLOW_QUEUE_LIMIT` 0 hits in `corpus/knowledge`; navigation 52/52 | three request-socket package entries admitted re-grounded — `hyprctl-flags-r28.md` (S221), `request-socket-live-bound-r8.md` (S158/S187/S258/S277), `request-limits-upstream-r31.md` (S253); navigation 52/52 → 55/55 (fraction 1.0 unchanged) | `python3 -I quality/counters/c2-r38-request-ground.py --repo . --rev HEAD` → admitted=3/3 TARGET_MET (before: admitted=0/3 at f6e3247); `python3 -I quality/check-index.py --rev bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5 --repo .` → indexed=55/55 missing=0 dangling=0 duplicates=0 |
```

## Proposed axis publication line (exact text)

Append in the round-38 section of SCORECARD.md, replacing the F1 sentence
(which the gate cannot parse and which publishes the stale cell):

```
Axis table re-derived at `bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5` (the round-38 tip; data commits `245065c`/`efb0ec2` add three indexed entries and no criterion, the records commits add neither): navigation 55/55; calibration resolved-active 50/50; operability selftest 12/12.
```

The derived values are identical at `efb0ec2`, `f0c9432` and `bb1adce` (all
measured above). Acceptance: `python3 -I quality/check-axis-scores.py --repo .
--rev master` → `mismatched=0`, exit 0. If the records commit adds any entry or
criterion after `bb1adce`, re-derive at the new tip before publishing.

## Residual risk / verification gaps

- I re-ran the lane's committed instruments read-only at four revisions; I did
  not re-run the discrimination gate or the eventq v3 counters (sibling
  reviewers own those). The frozen-pair 18/19 issue (LOG.md round-38 errata,
  `859d0cf`/`b6c1d31` post-freeze patches) is out of my scope and changes no
  axis number — the registration's §"Not claimed" says no axis score change is
  claimed by either counter, and the axis instruments do not read them.
- The r37 claims (navigation 52/52 etc.) were taken from the SCORECARD
  publication and the axis-base receipt, not re-derived from the r37 report
  prose; the gate's MATCH at base is the binding check.
