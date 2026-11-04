# Round 71 verifier spot-check (hyaku closure, non-author)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-04
lane-round: mado r71 (lane base `e2bf3fc7d7ae6467a2d01d7569b39decc9ccb212`; first round commit
`c354f4d410b829d985b31560af9202d98655dad0`; tip `82927056e21b2e7b9ab2c7570e783c0bb851e132`)
report: `.ufo/reports/round-71/mado.md` (fleet commit `13bb480613dfa32b04a9ce9be734d9097ed68223`,
author `mado-shokunin <mado@shokunin.local>`)
dispatch digest (copied from the mutable `.ufo/watchdog.log`, lines 2201–2220):

```
2026-11-04T00:05:52-03:00 launch mado round=71 pgid=943173 driver=hyaku-inline attempt=1
2026-11-04T00:06:22-03:00 lane-dead-no-report mado round=71; retry same round (hyaku-inline attempt=1: L1 ended without a landed report: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-71/mado.md)
2026-11-04T00:06:24-03:00 launch mado round=71 pgid=944137 driver=hyaku-inline attempt=2
2026-11-04T01:19:55-03:00 complete mado round=71; hyaku-inline attempt=2
```

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-71/mado.md` (fleet root) | `mado-shokunin mado@shokunin.local 13bb480613dfa32b04a9ce9be734d9097ed68223` | conformant |
| Report sections and `SHONEN` heading | `grep -n '^## '` and `grep -n '^- \['` on the report | Work performed:9, Landed changes:86, Before → after measurements:103, Sources & frontier:110, Trend verdicts:135, SHONEN:157; 4 `[~]` lines (159–162), one per `SHONEN.md` box, each with a pointer; no `[x]` | conformant |
| Cited commits exist and are ancestors of the branch | `git rev-parse --verify <hash>^{commit}` then `git merge-base --is-ancestor <hash> master` (lane repo) | 9/9 ANCESTOR of `master` — `c354f4d4`, `4a91c644`, `8e78a4ee`, `e137b5a4`, `3868bc65`, `443cbd50`, `9b2f1bce`, `f9230c46`, `82927056`; the base `e2bf3fc7` is a commit in the repo | conformant |
| Report lands after the lane work and cites the pushed tip | `git log -1 --format=%ad,%cd` on both commits | report committer `2026-11-04 01:18:59 -0300` > lane tip committer `01:17:25 -0300`; report line 7 cites `82927056…` | conformant |
| Landed-changes table completeness | `git rev-list --count c354f4d4..82927056` | 8; the table lists exactly those 8 hashes; `c354f4d4` (the inherited leftovers) is named in Work performed, outside the count | conformant |
| Lane pushed, no divergence | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git ls-remote origin refs/heads/master` | `branch=master local=82927056… remote=82927056… ahead=0 behind=0 head=detached tracked=0 untracked=0`; remote `82927056e21b2e7b9ab2c7570e783c0bb851e132` | conformant |
| No uncommitted round work | `git -C …/mado-shokunin status --porcelain` | empty | conformant |
| Prompt carries the template contract | `diff` of `.ufo/prompts/mado-round-71.md` lines 1–140 against `templates/round-prompt.md` rendered with `mado`/`71`/fleet root | two lines differ only in substitution detail: `Working dir: …/mado-shokunin` (template artifact `<{{LANE}}-repo>`) and the axes cell's parenthetical `(desktop and compositor craft)`. Round-level items §1–§5 verbatim and the five child-lane items present (report path §4, commit-then-push plus report-last/hash-citation §5 and §6 item 14, `SHONEN` heading §4, commit-hash citation rule §4/§6, write scope §6 item 3) | conformant |
| L2 route map vs `MISSION.md` | read prompt §3 and §6 against `MISSION.md` §L2 concurrency | §3 delegates to the host route table and quotes no concrete model bucket; §6 repeats the run-15 operator text (`m_flash`, `m_mim`, `m_zfl`) that `MISSION.md` does not contradict | conformant (nothing to mismatch) |
| Wave floor and shape | `.ufo/waves/round-71/w1/swarm-registry.json` + `scripts/hyaku/ufo-wave-policy.json` | 13 members — executor 3, scribe 3, scout 2, reviewer 2, critic 1, mutation-tester 1, connector 1; attack share 4/13 = 30.8 % ≥ 25 %; 1 connector ≤ 2; one wave inside band 8–16 | conformant; no planner seat (the policy's `lanes` list has no `planner`, and the spec's context declares the L1 holds that seat) |

**Conformance defects (status-neutral, details in Routed defects):** the `Sources & frontier`
warning arithmetic is off by one; the single rejection cites a URL that 404s at the pinned tag and
was not curated as a `rejected` `SOURCES.md` row; the `harm-watch` frozen-round-70-counter leg is a
setup error whose `rc` is recorded as 0 and has no corrected re-run, while the report/LOG still
assert `TARGET_MET` at the tip; `w1-results.json` carries no per-seat `status` field, so the
"13/13 settled `status: ok`" rests on the orchestrator's WAVE-DONE message alone; the report's
"11 words" for quote A is 10; and neither new counting instrument has a `SKILL.md` gate-registry
row. None of these changes a status.

## Per-claim re-check

Method: the two round claims rest on lane-owned instruments that print `TARGET_MET`/`TARGET_MISSED`
with declared exit maps and `--selftest` — under PROTOCOL §Gate standard they are verdict
instruments, so this closure **verified their committed evidence** (frozen-run receipt lines, the
revision each run names, the frozen control digests, the selftest tally where receipted) and
**re-derived each before→after from committed bytes** (predicate source, control-set composition,
fixture semantics, base-leg misses). I did not execute the lane's counters.

**C1 — calibration (exit-status-disagreement kill credit).** Re-derived:
`grep -n 'mz_killed' quality/counters/c1-r70-landing-controls.py` → line 478
`mz_killed = bool(mz_rc != 0 and summary_shows_failure(mz_out))`; the same grep on
`quality/counters/c1-r71-landing-controls.py` → line 486
`mz_killed = bool(summary_shows_failure(mz_out))` — the conjunct is the sole delta on the credit
line, as the review states. `quality/counters/c1-r71-real-children.py:78-80` fixes the four
scenarios and expectations (`liar-success` pass, `stderr-genuine` pass, `liar-kill` fail,
`crash-stderr` fail); lines 110–113 show the fixture lanes: `liar-success` prints a genuine `1/2`
summary and exits 0, `stderr-genuine` prints it on stderr and exits 1, `liar-kill` prints `2/2`
and exits 1, `crash-stderr` exits 2 with no summary. From that, the held harness credits
`liar-success` wrong and the other three right (`base_correct=3`) and the successor credits all
four (`correct=4`) — the reported before→after without running the counter. Committed receipt
`measurement-r71.txt` § C1: four `MADO_R71_SCENARIO` lines with those expectations and
`MADO_R71_REAL_CHILDREN: cases=4 correct=4 base_correct=3 verdict=TARGET_MET rev=8e78a4ee…`, rc 0;
harness sha256 `f8364995…` equals the blob at `8e78a4ee` and at the tip. Do-nothing control
`control-baseline-c1-r71.txt` (pre-freeze): held harness `3/4`, `liar-success … correct_for_held=NO`.
Selftests: harness 70/70 and counter 27/27 are named in `LOG.md:3483` but no committed tally
receipt exists (C2's 63/63 is receipted) — evidence nit, not a claim defect.
**Verdict: improved (calibration).**

**C2 — operability (four carrier shapes on a frozen 23-case set).** Re-measured the frozen set:
`c2-controls-r71.json` sha256 `d7814de8815bb0d4146ceed612ddd3e03029763b7cbf769d868a96ce5cefe7df`
(matches the SCORECARD/receipt), 23 cases; the round-70 set sha256 `29947b4c…` (17 cases) is
carried **byte-identically** — a per-case comparison of the two JSON files yields 17/17 identical
and 6 new cases (`dict-call-splat`, `dict-call-splat-object-alias`, `store-through-alias-two-hop`,
`attribute-second-object`, `unguarded-dict-splat-negative`, `env-call-no-key-negative`). The
receipt's base leg has `correct=no` on exactly the four carriers and on neither negative →
`base_controls=19/23`; the candidate leg has zero `correct=no` → `controls=23/23`. Repair verified
in bytes: `c2-r71-shapes.py` sha256 `72a0c2a5…` at `8e78a4ee` → `253dee5d…` at `3868bc65` and at
the tip; the F1 alias rebinding window is enforced at :679-681
(`not any(bind_line < r < node.lineno …)`) and the F2 edge ordering inside `resolve()`
(`edge_lines.get(prefix, 1 << 30) < at_line`); the two repros are pinned as counter regressions
`r71-splat-alias-rebound-before-splat` (:1209) and `r71-attribute-edge-after-use` (:1214). Receipt:
`MADO_R71_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=23/23
base_controls=19/23 verdict=TARGET_MET` at `8e78a4ee` and again at `3868bc65`, rc 0. The attack
seat (`w1/R71RevC2.md`) reproduced both legs and `--selftest` 63/63 at both revisions and showed
the widened classifier reclassifies no production file (`MADO_R70_READER`/`MADO_R71_READER` lines
sort-identical). **Verdict: improved (operability).**

**No owned axis harmed.** `git diff e2bf3fc7 82927056 -- SCORECARD.md` → +61/−0 (the round-71
section appended; no row edited). Re-measured at the tip: index rows 83 → 85 (`grep -cE '^\|
`knowledge/…` \(' corpus/README.md`; 85 files in `corpus/knowledge/`; checker
`indexed=85/85 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`), ledger 121 → 124 `|` lines
(122 data rows by the checker: `population=122 ledger_rows=122 uncovered=0 verdict=TARGET_MET`),
axis publication `checked=3 mismatched=0` (navigation 85/85, calibration resolved-active 86/86,
operability selftest 12/12). Gate `MADO_SELFTEST: 460/460` at `443cbd50` and re-affirmed at
`9b2f1bce`; `tools/mado-verify.sh` is blob `9113c7c0…` in every commit from `443cbd50` to the tip,
so the bytes measured are the bytes shipped. The frozen round-70 instruments
(`c1-r70-real-children.py`, `c1-r70-landing-controls.py`, `c2-r70-carriers.py`) are byte-identical
at the base and at the tip (blob ids `0cd0da0d`, `f80a102c`, `9afbbeed`). Coverage score stays
10.0000 with a two-entry-larger denominator — unchanged, not harmed.

## Discernment spot-check (LEARNING.md — outside check)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S442 admit (subprocess `run` capture_output) | admitted, tier A, `mined` | live fetch `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst` | **agree** | 61,603 B, sha256 `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd` — identical to the committed fetch receipt and to S108's recorded digest; quote "If capture_output is true, stdout and stderr will be captured." at :53 and "the internal Popen object is automatically created with stdout and stderr both set to PIPE" at :54-55 (10 and 15 words); the sentence grounds captured streams as the child's own report, separate from the exit status |
| S443 admit (Calls‑section `**`) | admitted, tier A, `mined` | live fetch `…/v3.14.8/Doc/reference/expressions.rst` | **agree** | 92,034 B, sha256 `e19de4fe…` identical; the 25-word quote spans :1415-1417 exactly ("If the syntax `**expression` appears in the function call … additional keyword arguments."); grounds a `**mapping` in a call as a real carrier of the contents, i.e. the C2 mechanism, not a mention |
| `stdtypes.rst` reject | rejected as a new row | live fetch `…/v3.14.8/Doc/library/stdtypes.rst` → **404**; opened the real path `…/v3.14.8/Doc/builtins/stdtypes.rst` (200, 248,201 B) | **disagree on the citation, agree on the decision** | the cited URL does not resolve at the pinned tag — 3.14's docs reorganization moved `stdtypes.rst` under `Doc/builtins/` (`git/trees/v3.14.8` lists `Doc/builtins/stdtypes.rst` and no `Doc/library/stdtypes.rst`); at the real path the mapping-method content the reject describes is there (`Mapping Types --- dict` :5299, `.. method:: update(**kwargs)` :5529, `setdefault` :5523). As cited the reject is unprovable (could not re-open), never `harmed`; the decision stands on the file I did open |
| Reject curation | — | `grep -n stdtypes corpus/SOURCES.md` → 0 rows | **disagree** | CORPUS §Shape and the round prompt §2b.1 keep a rejection as a `rejected` row whose `teaches` starts `REJECTED: …; flip: …`; here the rejection exists only as Gate prose, so the taste it evidences is not in the registry (routed) |
| Census conformance | round's own gate | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | **agree** | exit 0, final line `mado ok …/mado-shokunin/corpus/SOURCES.md`; 39 warning lines, exactly 2 of them the new rows (S442/S443 W04, the sanctioned superseding-same-URL family); frozen census checks re-run by me over the tip: malformed 0, duplicate ids none, enum/tier violations none, mined used-by missing none |
| Row quote length | contract ≤ 25 words | counted the two `teaches` quotes | **agree** | S442 10 words, S443 25 words |

## Trend verdicts

- **expansion: improved** — two new admitted entries, index 83 → 85, each `source:` citing a row
  opened and marked `mined` this round (S442, S443), on edge classes the coverage map did not hold
  (the r70 sibling entries cover the summary-parse rule/three children and the alias-attribute-
  splat-constant set; these cover the exit-status-disagreement class and four other carriers),
  plus the Frontier bullet and the round's capability row (`SCORECARD.md` § Capability
  demonstrated). Caveat recorded for the operator: the ground is the lane's own instrument lineage
  (coverage-map tag "no surface"), not a desktop/compositor surface — r70's closure graded an
  analogous round `unchanged`; I grade this one `improved` because LEARNING's test is "ground the
  coverage map did not hold", and these subjects were not in it.
- **quality: improved** — the r70 rules are superseded by stronger successors: the sole C1
  behavioural delta is the dropped exit-status conjunct (verified in source), and C2's widening
  shipped with two dominance holes that were repaired red→green inside the round with the frozen
  17-case set carried byte-identically and the frozen 23 scoring identically before and after;
  both entries carry `verified-at: 3868bc65…`; no admitted entry failed a re-check (my census and
  index re-derivations match).
- **discernment: improved** — the round's attack seat falsified the first widening (F1 HIGH,
  F2 MEDIUM) and the repair stayed inside the frozen sentence with a committed red-before/green-
  after receipt; this outside spot-check agrees on 2/2 admits and on the reject's decision. The
  reject's citation is defective and is routed; that is a citation fault, not an unlearned
  disagreement, and the round's own mistake (M71-3) did become a repaired predicate.

## Routed defects for the next round

1. **Reject citation and curation** — `corpus/lessons/round-71.md` cites
   `…/v3.14.8/Doc/library/stdtypes.rst`, which returns 404; `stdtypes.rst` lives at
   `Doc/builtins/stdtypes.rst` at v3.14.8. Re-cite the resolvable location (or the rendered page)
   and record the rejection as a `rejected` `SOURCES.md` row with `REJECTED: …; flip: …`.
2. **`harm-watch-r71.txt` frozen-round-70 leg** — the "frozen round-70 counters at the tip"
   commands died on a missing scratch directory (the lane's own M70-1 class) and the receipt
   records `rc=0` for commands whose declared setup exit is 2; there is no corrected r70-pair run
   below, yet the report and LOG assert `cases=3 correct=3 base_correct=1` and
   `controls=17/17 base_controls=13/17` "at the tip". The C2 half is review-verified at `e137b5a4`
   (`w1/R71RevC2.md`); the C1 half has no r71-revision run. Add a corrected run at the tip and fix
   the receipt's `rc` capture (all four counter error legs print `rc=0`).
3. **`Sources & frontier` arithmetic** — the committed census-after receipt carries 39 `W0` lines,
   two of them naming S442/S443; the report's "38 pre-existing plus one new W04" is one short on
   both halves (37 + 2 = 39). Correct in the next round's errata (the report is append-only).
4. **Gate registry** — `c1-r71-real-children.py` and `c2-r71-shapes.py` print verdicts and carry
   `--selftest` but have no row at the registry home (`SKILL.md`), whose last table is round-68;
   r69/r70's counters have the same gap in prose only. Add rows (name, verdict map, self-test,
   pinned-value path, write scope, owner) or declare them probes explicitly.
5. **Wave result capture** — `w1-results.json` entries carry `name`/`agent`/`output`/`note` and no
   `status`; the "13/13 settled `status: ok`" in the report and LOG rests on the orchestrator's
   WAVE-DONE message, not a committed artifact. Record settlement status per seat next wave.
6. **Minor count** — the report calls quote A "11 words"; it is 10 (the row's quote is within the
   ≤25-word contract either way).
7. **Carried, still open** — round-69 `check-deliverables.py` reds on r69 seat reports remain
   observed-not-repaired; they belong to a round-69 correction entry (unchanged from the r70
   routing).

## SHONEN note for the operator

All four boxes stand at `[~]` with resolvable pointers, and the round wrote no `[x]`. Box 2's
pointer is the historical round-3 end-to-end task, not this round's work (the lane's live desktop
plane has been absent/probed-absent since r57) — a non-author promotion reviewer can check it
against the record but should not read it as a fresh end-to-end desktop task. Promotion authority
is operator-owned; this closure writes no `[x]` and promotes nothing.
