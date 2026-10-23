# AtkC2Table — attack on the C2 status table (round 24, wave 2)

Item attacked: `SCORECARD.md` `### Capability status (round 24 re-demonstration)`, commit
`39c596307333b8ca0a1e42b3f3b9a748bb8b208b`, lines 1566-1586 (12 rows). The table is byte-identical at
`81955bd5`, the revision of `evidence/c2-after-81955bd5.txt`: `SCORECARD.md` sha256
`sha256:8f2bcbaceb687643e50cb5f33c39a346d6f59faeef8016765839c58e32ae4bba` at both revisions, and
`git diff 81955bd 39c5963 -- .ufo/waves/round-24/c2/` is empty. Compared against
`evidence/c2-after-81955bd5.txt`, `controls/CtlC2DoNothing.md`, `c2/smoke/base-8e5d9369.txt`,
`c2/manifest.json` (`sha256:e02c76d1…`), `c2/count.py` (`sha256:a2809501…`) and `c2/README.md`.

All work was read-only outside this report: no lane or fleet git/jj write, no service, package, compositor
or `hyprctl` operation; scratch only under `/fast/scratch/hyaku/mado-r24/w2/`. No tools installed or updated.
The full C2 counter was not re-run (one-run cap belongs to a sibling seat); I ran the frozen commands
individually.

## A. The 12 "observed evidence" cells — all hold

The after-receipt records only `stated=… observed=… OK|MISMATCH exit=…` lines, not command stdout. For every
`works` row that line is still a proof that the row's regex matched; for the one `fails` row the raw output is
recorded separately. The base smoke at `8e5d9369` and the `81955bd5` receipt have identical
observed/exit pairs for all 12 rows (only row 8's `stated` differs, because the base tree predates the status
table). I reproduced 9 rows literally at the tip tree and checked the other 3 against independent raw output
or the frozen rule:

| # | Row | Cell claim | Check | Verdict |
|---|---|---|---|---|
| 1 | sources registry | census `mado ok`, exit 0 at `8e5d9369` | reproduced in a scratch census root at `39c5963`: `mado\tok\t…/corpus/SOURCES.md`, exit 0; base receipt exit 0 and rule requires `^mado\tok\t` | holds |
| 2 | verdict gate (live + file plane) | `--no-live` prints a `MADO_VERIFY:` verdict, exit 0; live not exercised | ran `tools/mado-verify.sh --no-live`: `MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane only — live layer skipped: --no-live)`, exit 0 | holds |
| 3 | hermetic self-test | `MADO_SELFTEST: N/N assertions passed`, exit 0 | ran `--selftest`: `MADO_SELFTEST: 460/460 assertions passed`, exit 0 | holds |
| 4 | mutation regression with re-cut | `MADO_REGRESSION: PASS`, exit 0, harness read-only | base receipt exit 0 + rule requires `^MADO_REGRESSION: PASS \(case=mado-verify-hardened; `; not re-run (600 s row). `verify.py` below printed the same PASS line with killed=10/10 | holds by rule entailment |
| 5 | post-hoc transcript tripwire | four round-17 dirs all `SELFTEST_SUMMARY: n/n`, exit 0 | ran the four-dir loop: four summaries (last 30/30), exit 0 | holds |
| 6 | tripwire frozen replay (gate entry) | `MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch`, exit 1 | ran it: exact token, exit 1, 5 inputs all `"ok": true`, `missing_findings: []`, three `extra_findings` | holds |
| 7 | landedness check | `LANDED <rev>` at `8e5d9369` | ran `landed-check.sh <lane> 8e5d9369…`: `LANDED 8e5d93691e2f…`, exit 0 | holds (lane caveat below) |
| 8 | tripwire evidence marker | L 15/18 (P 66/66) at `8e5d9369`; two reset-cleared leads pass at `28c6837`, fail now | `w1/reports/ScribeC2Evidence.md` records an independent `tw-precision.py` run: 166/175, L 15/18, P 66/66 and names the two cases; `CritC2Manifest.md` §8 re-ran it; rule requires L 17/18, so observed=fails. I did not re-run the 600 s meter | holds |
| 9 | harness fail-closed check | six forced setup failures classified, `POSITIVE_CONTROL_OK isolate.sh` | base receipt exit 0 + rule requires six `FAIL_OPEN|FAIL_CLOSED isolate.sh mode=` lines and the positive control; not re-run | holds by rule entailment |
| 10 | tripwire reached-body sweep | `recall_lost` 0 at `8e5d9369` | ran `a2-guards.py 39c5963 --fixtures-rev 6a7d9ca…`: `recall_lost: 0`, `rev: 39c5963…`, exit 0 | holds |
| 11 | detector removal-side guard | removal, crash-flip, pure-row counters 0 | same run: `recall_lost 0`, `crash_flip 0`, `pure_rows 0` (also `vcs_fn 0`, `a2_mismatch 0`, `dup_rows 0`), exit 0 | holds |
| 12 | artifact-only assessment integrity | `mado-assessment.py --selftest`: pass = total, exit 0 | ran it: `pass 20 total 20 result selftest`, exit 0 | holds |

No cell contradicts either receipt. Caveat on row 7: the `CtlC2DoNothing.md` base run at the same revision
shows `landedness check … exit=1`, which looks like a contradiction. It is a `{LANE}` artifact: with the
canonical lane the script printed `LANDED 8e5d9369…`, exit 0; against the control clone it printed
`LOCAL_ONLY 8e5d9369… (ancestor of refs/heads/master; remote tip 87429be6… is absent locally; ancestry
untestable without a fetch)`, exit 1. The cell is true for the canonical lane but the table does not name the
lane; the same-revision control value is `exit=1`. That is a reproducibility caveat, not a false cell, and is
the manifest leniency already reported as `CritC2Manifest.md` row 7.

## B. `tripwire frozen replay` = `works` with exit 1 — honest under the manifest rule

- Manifest row (`manifest.json`, "tripwire frozen replay (gate entry)"): `exit_ok` `[0, 1]`, regex
  `^MADO_TRIPWIRE_FROZEN: frozen_(match|verdict_mismatch)$`, `forbid_regex` `"ok": false`, pin
  `.ufo/waves/round-18/frozen`.
- My run at `39c5963`: `MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch`, `"exit": 1`, all five inputs
  `"ok": true`, three extra findings (`package_query` on `r13-root.jsonl:4`, `r14-source-safety.jsonl:2,3`),
  no missing findings. The replay executed and the input digests verified; the mismatch is verdict-level.
- Round 19 records the round-18 pin's expected mismatch as the declared baseline:
  `.ufo/waves/round-19/w2/reports/RerunSuites.md:73`, `ScribeScorecardCheck.md:14`, `ReviewFrozen19.md:39`,
  and `HarmWatch19.md:13` treats `(1, frozen_verdict_mismatch)` as `BASELINE`.
- The row's own claim is "0 match / 1 mismatch / 2 tampered, unpinned or baseline error", so exit 1 is a
  declared outcome, not a replay failure. The cell states the token, the exit and that the mismatch is the
  frozen verdict, which is exactly what the command printed.

Honest. Residual, already reported by `CritC2Manifest.md` §6: the rule is too lenient (it never positively
asserts digest verification and accepts either verdict), and the r18 pin is known-stale, so `works` here means
"the replay mechanism ran and reported", not "the pinned verdict matches". The table's own wording says that,
so this is a manifest-fit defect, not a dishonest status.

## C. The 3 capability rows outside `Capabilities` headings — the round must report, and the claim does not hold

Enumeration: every markdown table whose first header cell is `Capability` yields **15** rows. Importing the
frozen counter's own `parse_scorecard` and calling it on `git show 39c5963:SCORECARD.md` yields **12**. The
three skipped rows are:

- `SCORECARD.md:437` `source-fragment collision screen` (r13, under `### Sources and demonstrated repertoire`
  `:425`);
- `SCORECARD.md:438` `digest-pinned frozen regression` (r13, same heading);
- `SCORECARD.md:782` `finite declared-action classifier` (r16, under `### Demonstrated capability` `:778`).

Their tables use the same `Capability | What it can now do | … | First-working round` schema as the counted
tables. None has a manifest row or a row in the round-24 status table, so each defaults to `stated=works` and
the counter's own documented convention ("no manifest command … fails with 125", `c2/README.md:20`,
`c2/count.py:16-17`) would score it MISMATCH if enumerated. The `c2/README.md:20` population sentence
restricts "every markdown table under a heading matching `^#{2,3} Capabilities`"; the frozen predicate says "a
capability named in a SCORECARD.md capability table" with no heading restriction. So the 12-row population is a
heading-scoped subset, not the predicate's population.

This is not only a scope defect. One excluded row is observably false at the tip:

```
$ python3 -I .ufo/waves/round-13/w1/reports/MistakeFix.py --registry corpus/SOURCES.md   # 39c5963 tree
MISTAKE_FIX: COLLISION S117 -> S119 :: same canonical URL among active rows; …
MISTAKE_FIX: COLLISION S120 -> S121 :: same canonical URL among active rows; …
MISTAKE_FIX: FAIL registry=corpus/SOURCES.md rows=168 urls=140 no_url=21 collisions=4
  rejected_history=3 supersedes=7 errors=0
exit=1
```

The `:437` row's evidence says "real historical registry exits 1 naming S017/S030, **current exits 0**"; the
current registry exits 1 with `collisions=4`. The row's selftest does pass (`MISTAKE_FIX_SELFTEST: PASS 25/25`,
exit 0), and the two other skipped capabilities do re-demonstrate:

- `python3 .ufo/waves/round-13/frozen/verify.py` → `MADO_FROZEN: MATCH`, `FROZEN_ID: frozen_match`, exit 0;
- `python3 -I tools/mado-action-plan.py --selftest` → `SELFTEST_SUMMARY: 52/52 passed`, exit 0;
- `python3 -I tools/mado-action-plan.py --frozen .ufo/waves/round-16/frozen` → `MADO_PLAN: frozen_match`,
  exit 0.

So the population omission hides at least one real SCORECARD-vs-repo disagreement (the collision-screen row's
"current exits 0"), not merely three unmeasured-but-healthy capabilities.

The status table also asserts two universals that are false for these rows: "Each capability in the tables
above was re-run with its frozen command … on the base tree" (`SCORECARD.md:1568-1570`) and "This table
supersedes the implied `works` of every earlier row" (`:1570`). The table has 12 rows and the three skipped
rows have no frozen command and no row, so neither sentence is true as written. The diff from base is
append-only (`git diff --numstat 8e5d9369 39c5963 -- SCORECARD.md` → `29 0`), so the false universal ships in
the landed SCORECARD.

Wave 1 already found the scope defect (`w1/reports/RevRegistration.md` H2, `w1/reports/CritC2Manifest.md` F0)
and the sibling wave-2 seat `AtkC2Calibration.md` §C repeats it, so the round *has* reported it in prose — but
the landed table and the closure value `mismatches=0/12` still read as full coverage. Under the predicate's
plain wording the count is **3/15** (three rows with no frozen command, using the counter's own no-command
convention); using the rows' own commands it is at least **1/15** (the registry check exits 1). In neither
reading is `0` a predicate-complete value.

Smallest safe correction (post-freeze, so a disclosure, not a predicate or manifest edit):

1. Report the C2 value as `0/12` over the heading-scoped subset and name the three excluded rows; do not offer
   `mismatches=0` as "SCORECARD capability tables match observation".
2. Append to SCORECARD (append-only; no removed lines) a scope note after the status table naming the three
   rows and their observed state: two re-demonstrate, the collision-screen row's "current exits 0" is stale
   (registry exit 1, `collisions=4`).
3. Route the pre-existing S117→S119 and S120→S121 duplicate-URL collisions (and the stale row claim) to the
   open coverage/frontier record; do not re-cut the frozen manifest or predicate after data.
4. If the canonical judge reads "capability table" literally, record C2's target as not met (3/15) rather than
   met (0/12).

## D. Impacted axes and verdict

Impacted axes:

- **calibration (C2, primary):** the measured population is 12 of 15 capability rows, and the landed table's
  two universal sentences are false for the three omitted rows; `mismatches=0/12` is not a predicate-complete
  calibration value.
- **coverage / frontier (secondary, via the hidden mismatch):** the `:437` row's "current exits 0" is stale;
  the live registry reports four collisions, including the active duplicate URLs S117→S119 and S120→S121.
- **reproducibility (minor):** the landedness cell's `LANDED` value is lane-dependent (canonical lane `exit 0`,
  control clone `exit 1`); the table does not name the lane, though the manifest already permits both classes.

Fixable versus rejectable: the 12 row-level cells and the frozen-replay `works` are defensible and need no
change; the population exclusion is a fixable *disclosure* defect (the omitted rows can be named and their
observed state recorded append-only without touching the frozen counter or manifest), but it makes the
unqualified `0/12` target claim rejectable, and the `:437` row is a genuine pre-existing SCORECARD-vs-repo
mismatch rather than a mere measurement gap.

**VERDICT: partial** — the 12 row-level "observed evidence" cells hold (9 reproduced literally here; row 8
independently evidenced; rows 4 and 9 rest on the frozen rule plus the recorded exit), and calling
`tripwire frozen replay` `works` at exit 1 is honest under the frozen manifest rule and the row's own 0/1/2
contract. The population and universal-coverage claim does not hold: the counter measures 12 of 15 capability
rows, the excluded `source-fragment collision screen` row is observably false at the tip (registry exit 1,
`collisions=4`), and the landed table's "each capability in the tables above was re-run" and "supersedes the
implied `works` of every earlier row" are false for those three. The closure must report the 12-of-15
population and must not read `mismatches=0/12` as C2's target met; under the predicate's plain wording C2 is
3/15 (or at least 1/15 on the rows' own commands) and the target is not met.

### Evidence paths

- Status table: `SCORECARD.md:1566-1586` at `39c5963` (sha256 `8f2bcb…`, identical at `81955bd5`).
- Receipts: `.ufo/waves/round-24/evidence/c2-after-81955bd5.txt`,
  `.ufo/waves/round-24/c2/smoke/base-8e5d9369.txt`,
  `.ufo/waves/round-24/controls/CtlC2DoNothing.md`.
- Frozen counter/spec: `.ufo/waves/round-24/c2/{count.py,manifest.json,README.md}`.
- Frozen replay: `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen` → exit 1; round-19
  expected-mismatch records cited in §B.
- Excluded rows: `SCORECARD.md:437-438`, `:782`; registry/selftest/frozen runs as quoted in §C.
