# mado round 73 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-04 (UTC), America/Sao_Paulo round window
role: closure judge for mado lane-round 73. I authored none of this round's work: not the
instruments, controls, knowledge entries, lesson, SCORECARD/LOG entries, prompt, or report.

Inputs: report `.ufo/reports/round-73/mado.md` (fleet `029d6d0a5cc4c55c8c4ec60848d7a42f683e0d1c`,
`mado-shokunin <mado@shokunin.local>`); dispatched prompt `.ufo/prompts/mado-round-73.md`
(`e913654110f53f51f44ead6244e8729441585787`); lane base
`d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce`; lane tip `422ba69ae597f5bc81ae8bc7b8b7be45b748e988`.
Dispatch digest (`.ufo/watchdog.log`, lines 2232/2237 at read time):
`2026-11-04T01:56:07-03:00 launch mado round=73 pgid=2540157 driver=hyaku-inline attempt=1` /
`2026-11-04T02:13:29-03:00 complete mado round=73; hyaku-inline attempt=1`.

## Conformance (PROTOCOL §Round-robin step 1)

- **Report path and attribution.** `.ufo/reports/round-73/mado.md` exists at the contract path and
  its fleet commit `029d6d0a5cc4c55c8c4ec60848d7a42f683e0d1c` is authored by
  `mado-shokunin <mado@shokunin.local>` (`git log --format='%an %ae %H' -1 -- <report>`).
  Report committer time 02:12:49 -03:00 is after the lane tip commit 02:11:46 -03:00: report
  lands last. The author stamp 02:11:33 precedes the lane tip by 13 s; that is the jj author
  stamp of the report change, while the committer time and the resolvable hash carry the
  ordering. Observation, not a defect. Report is on `origin/master`
  (`git merge-base --is-ancestor 029d6d0 origin/master` → yes; fleet origin tip `5c75e6d`).
- **SHONEN heading.** `grep -c '^## SHONEN'` → `1`; four `[~]` lines, one per box in `SHONEN.md`;
  no `[x]`.
- **Cited lane commits.** 5/5 exist and are ancestors of `refs/heads/master`
  (`git merge-base --is-ancestor <hash> refs/heads/master` for `87e4c61a`, `1459cca1`,
  `fb8a3df6`, `84fc266a`, `422ba69`); branch tip = origin tip (`git ls-remote origin
  refs/heads/master` → `422ba69ae597f5bc81ae8bc7b8b7be45b748e988`).
- **Lane cleanliness and push.** `scripts/hyaku/jj-lane.sh state` → `branch=master
  local=422ba69ae597f5bc81ae8bc7b8b7be45b748e988 remote=422ba69ae597f5bc81ae8bc7b8b7be45b748e988
  ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` prints nothing.
- **Prompt contract.** `.ufo/prompts/mado-round-73.md` §§1–5 equal the rendered
  `templates/round-prompt.md` except the working-dir substitution (8 diff lines, all intended);
  the round-level items and all five child-lane items are present verbatim; §6 is the run-15
  hyaku addendum. §6's planner override (line 391: the validator rejects `planner`; the L1 holds
  the canonical planner seat) matches the wave (no planner seat).
- **Wave.** 13 seats (executor 3, scribe 3, scout 2, reviewer 2, critic 1, mutation-tester 1,
  connector 1); attack 4/13 = 30.8 %; band 8–16; `w1-results.json` has 13 entries with non-empty
  `output`; the 13 seat directories are non-empty; no dead seat.
- **Report substance.** Real committed work, evidence pointers, checkable hashes, all required
  sections — a report, not a marker: status `ok`.
- **Fleet-root sweep at closure.** `.scratch/*` modified, `.ufo/reports/round-76/tsukuroi.md`
  untracked (another lane's in-flight report), `after` untracked; no mado round-73 misroot. The
  report's "only `.scratch/*` and `after`" line predates the tsukuroi file; not mado debt.
- Tool installs: none; no pacman transaction.

## Claim re-checks (evidence-verified, not executed)

The two counters are the lane's registered gates; per PROTOCOL §Gate standard (Closure
consequence) I did not execute them. I re-derived the committed inputs — case counts, held-set
carry, digests, revisions — and read the committed receipts.

**C1 — calibration: the frozen outcome set separates four named rule mutations.**

```sh
jq -r '.cases|length' .ufo/waves/round-73/controls/c1-outcomes-r73.json        # 10
sha256sum .ufo/waves/round-73/controls/c1-outcomes-r73.json                    # 263b3c5a…b2832b
git show 422ba69:.ufo/waves/round-73/measurement-c1-r73.txt
git show 84fc266a:.ufo/waves/round-73/measurement-c1-r73.txt
```

Observed: 10 cases, digest `263b3c5a288c45a59587890a7e4c2e6dc3389630e5dd4a5cd1731976b5d2832b`;
the eight round-72 held cases are carried byte-identically (`json.dumps(sort_keys=True)` set
match, 8/8); the receipt at the tip prints `MADO_R73_MUTANT_KILL: cases=10 mutants=4 killed=4
base_killed=2 verdict=TARGET_MET rev=84fc266a5bf6db6cf12b6aa6106ad33121f391be`; the per-mutant
lines show N1 and N2 survive the held eight-case set (8/8, `killed=NO`) while N3 and N4 are
killed there (6/8 and 3/8), i.e. `base_killed=2`; on the ten-case set N1's only miss is
`zero-denominator` and N2's only miss is `valid-then-garbled`. The 1459cca1 run is the version of
the same receipt at commit `84fc266a` (contract line `rev=1459cca1…`, same counts); the tip file
carries the `84fc266a` run. **Verdict: improved** — the before→after is verified at both revisions.

Gate evidence gap: the committed selftest receipts are 24/24 (`w1/R73ExecC1/selftest-r73.txt`, the
instrument commit) and 25/25 (`w1/R73RevC1/receipts.json`, after `--controls` was added); the
claimed 26/26 has no committed run. Routed D2.

**C2 — operability: the guard census counts the global-declared guard and the mutated `os.environ` transport.**

```sh
jq -r '.cases|length' .ufo/waves/round-73/controls/c2-cases-r73.json          # 28
sha256sum .ufo/waves/round-73/controls/c2-cases-r73.json                      # 65e94644…ecf230d
ls quality/check-*.py | wc -l                                                 # 20
git show 422ba69:.ufo/waves/round-73/measurement-c2-r73.txt
```

Observed: 28 cases, digest
`65e9464450d58f803ca626f7b7ce6bc4712f46710ac5707602601cee9ecf230d`; 23/23 round-71 held cases
carried byte-identically; the receipt prints `MADO_R73_GUARD_SHAPES: population=20 readers=13
guarded=13 unguarded=0 controls=28/28 base_controls=25/28 verdict=TARGET_MET
rev=84fc266a…`; the base leg has exactly three `correct=no` lines — `global-rebind-guard`,
`environ-splat-guard`, `environ-call-guard` — and the candidate leg is 28/28 correct; the
`population=20` matches `ls quality/check-*.py | wc -l`. The 1459cca1 run is the version at
commit `84fc266a` with identical counts. **Verdict: improved.**

Gate evidence gap: the committed selftest tally is 75/75 (`w1/R73ExecC2/selftest.json`, pre-repair);
the claimed 78/78 has no committed run, and `receipts/repair-r73.txt` ends at the
`== C2 selftest and frozen contract after the repair ==` header with no output. Routed D2.

**No-harm rows (re-derived).**

- `git diff d3f6c9f 422ba69 -- SCORECARD.md` → one appended round-73 block, 0 deletions; no
  published score changed.
- `git diff … -- corpus/SOURCES.md` → 3 added rows (S447–S449), no held-cell change.
- README index 87 → 89 (`grep -cE '^\| `knowledge/'` 87 at base, 89 at tip); `ls corpus/knowledge
  | wc -l` = 89.
- `quality/tool-ledger.md` → 127 data rows (130 `^|` lines including 2 header/separator rows and
  the title row).
- Five frozen instruments are blob-identical base → tip (`git rev-parse` equal for
  `c1-r72-landing-controls.py`, `c2-r71-shapes.py`, `c2-r70-carriers.py`, `tools/mado-verify.sh`,
  `quality/landing-counters.sh`).
- Harm watch at `fb8a3df6`: `MADO_SELFTEST: 460/460`; index 89/89; ledger 127/127 `uncovered=0`;
  axis `checked=3 mismatched=0`; census exit 0; five `same` blob ids.

No owned axis is harmed; the defects below are record/evidence, not a score regression.

## Axis verdicts

| axis | verdict | evidence |
|---|---|---|
| calibration | **improved** | C1: the ten-case set separates 4/4 named mutations against the held eight-case set's 2/4; receipts at `1459cca1` (in the `84fc266a` tree) and `84fc266a`; frozen rounds unchanged |
| operability | **improved** | C2: 28/28 against the held 25/28, missing exactly the three new positives; ledger 125 → 127; two Gate-registry rows added |
| coverage | unchanged | index 89/89 at the tip (87/87 at base); the published reachability sub-axis is saturated at both ends |
| depth | unchanged | no depth claim; the two entries add corpus detail, not decision-table depth |
| freshness | unchanged | the three rows were re-fetched 3× each and quotes re-opened; the S448 digest error is a record defect (D1), not source drift |
| adjacency | unchanged | connector sibling scan; no contested scope, no sibling write |

## Discernment spot-check (LEARNING.md)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S447 admit (`global` statement) | admit, tier A, `mined` | live fetch `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst` → 41,375 B, sha256 `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc` | **agree** | Quote "The global statement causes the listed identifiers to be interpreted as globals." at :972-973, 12 words; digest matches the row; the sentence grounds a `global`-declared store as the module mapping's guard |
| S448 admit (`os.environ`) | admit, tier A, `mined` | live fetch `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/os.rst` → 208,655 B, sha256 `2d0f2892676e1cf9547be2bd94cfe2a6221dddea82d52cb2475d4a3d819b2ae5` | **agree on the admit; disagree on the recorded digest** | The quote at :193-194 is exact (21 words) and the tier/ground are right; the row and lesson record `2d0f2892676e1cf9f0d8e61c63a2e70a86f0e0a5cdb6b06dd7b7d2c9b8b88a4e`, which shares only the first 16 hex chars with the bytes. The lane's own `R73ScoutSources` F2 found this in-round and it was not swept. Routed D1 |
| S449 admit (`subprocess.run` `env`) | admit, tier A, `mined` | live fetch `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst` → 61,603 B, sha256 `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd` | **agree** | Quote "a mapping that defines the environment variables for the new process" at :88-89 (the row's :88-90 range includes it), 11 words; the paragraph passes the mapping directly to `Popen` (:90-91), so the run anchor is not false; digest matches |
| S446 reject (round 72; round 73's Gate records no reject) | reject | live fetch `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/stdtypes.rst` → 248,201 B, sha256 `5a6951b72ecc630a87f45a650fc11c186cfeb4251bedd1ea28f45bcb3116e8e1`; `Mapping Types --- dict` :5299, `setdefault` :5523, `update(**kwargs)` :5529 | **agree on the reject** | The document is mapping-method behaviour, not call/result semantics; no admitted entry needs it; the flip is recorded. The row still carries no ≤25-word located quote (r72 routed item 3) — D5 |
| Registry/census | 383 → 386 rows | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | **agree** | 386 rows, exit 0; W04 for S447/S440, S448/S113, S449/S442 (the three new rows) plus held W04s and the held W01 S277; no E-findings; 3 added rows, no held-cell change |

Discernment ruling: the outside spot-check agrees with all three admit decisions and the re-opened
reject; one recorded digest is false (D1), which is the learning the lane owes round 74. The gate
decisions themselves are sound.

## SHONEN note

The four boxes remain `[~]`; no `[x]` is warranted from this closure. Box 4 (no cross-domain
bleed) is checkable from this round's diff (no config/compositor/sibling write; PROVINCE.md gains
only the two-counter refinement), but boxes 1–3 need an outside-lane execution test and an
end-to-end domain task this round did not run (the round is instrument work). Promotion remains
operator-owned; a non-author promotion review would have to re-run the instructions cold.

## Trend verdicts

- **expansion: improved.** Two admitted entries; README index 87 → 89; the control-set entry
  cites own-work receipts and held S441/S444; the guard-carrier entry cites S447/S448/S449; the
  round-72 frontier's blind spots become load-bearing cases.
- **quality: improved.** Five review defects repaired at `84fc266a` with red/green receipts; both
  claims re-measured identically; five frozen instruments unchanged; no admitted rule found false.
  D1–D4 are record/evidence defects, routed, not rule failures.
- **discernment: improved.** The wave's scouts/reviewers/critic/mutation-tester produced the five
  repairs, four `## Mistakes` rows, and grounded criteria 118/119; my outside check agrees on the
  decisions. The S448 digest finding the lane's own scout made was not learned into the record —
  D1; that is the round-74 learning, not a reversal of the admit decisions.

## Routed defects for round 74

1. **D1 (high) — S448's recorded sha256 is false.** `corpus/SOURCES.md` S448 and
   `corpus/lessons/round-73.md` § Gate state
   `2d0f2892676e1cf9f0d8e61c63a2e70a86f0e0a5cdb6b06dd7b7d2c9b8b88a4e`; the committed fetch,
   the live URL, and S113 all hash to
   `2d0f2892676e1cf9547be2bd94cfe2a6221dddea82d52cb2475d4a3d819b2ae5` (208,655 B). The lane's own
   `w1/R73ScoutSources.md` F2 found this in-round; no correction landed. Fix: append a
   superseding row per CORPUS rule 2 (or a named erratum) and sweep every mention; never rewrite
   the row in place.
2. **D2 (medium) — the final selftest tallies have no committed run.** The report, SKILL Gate
   registry, SCORECARD, declaration and lesson state 26/26 (C1) and 78/78 (C2); the committed
   receipts stop at 24/24, 25/25 (C1) and 75/75 (C2) before the repair, and
   `receipts/repair-r73.txt` ends at the post-repair C2 selftest header with no output. Fix:
   commit the post-repair `--selftest` receipts at `84fc266a` (or the revision that produced the
   numbers) and annotate the registry/SCORECARD tallies with that revision.
3. **D3 (low) — the report says the measurement files carry "both runs"; they do not.** The tip
   files carry only the `84fc266a` run; the `1459cca1` run survives as the `84fc266a` version of
   the same paths (`git show 84fc266a:.ufo/waves/round-73/measurement-c{1,2}-r73.txt`). The
   re-measurement overwrote the first receipt in place. Fix: append both runs, or say which
   commit carries the first; never overwrite a receipt.
4. **D4 (medium) — QUALITY 118/119 landed in a new root `QUALITY.md`, not the canonical
   `corpus/QUALITY.md`.** The canonical bar (802 lines, criteria 1–117) is unchanged;
   `corpus/README.md`'s "Quality bar — See `QUALITY.md`" resolves to `corpus/QUALITY.md`, so the
   new criteria are invisible at the contract path. Fix: append 118/119 to `corpus/QUALITY.md`
   (append-only) and retire/redirect the root fragment; update the report/lesson pointers.
5. **D5 (carried) — S446 (r72 reject) still has no ≤25-word located quote.** The r72 spot-check
   routed it (item 3); the r73 Gate records no reject, so nothing was added. Fix: record the
   quote at the real `Doc/builtins/stdtypes.rst` lines in the round-74 Gate block or on a
   superseding row.
6. **D6 (observation) — the two entries' `verified-at:` names `1459cca1`, the pre-repair
   instrument commit, while the final counters are `84fc266a`.** The recheck resolves at both
   revisions with the same verdict; name the final revision at the next entry refresh. Not a
   false claim.
7. **D7 (operator note) — the run-15 addendum's routing sentence ("ONLY reviewer uses `@m_zfl`")
   is stale against the live `task.agentModelOverrides`** (executor/critic/connector/sentinel/
   scribe/mutation-tester were `@m_zfl` at the r72 closure). The prompt names the config as the
   authority and never passes a model; carried from r72, not lane debt.
