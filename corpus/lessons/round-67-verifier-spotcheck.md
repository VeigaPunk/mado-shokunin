# mado round 67 — verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-03
round: mado r67 (lane counter 67)
base: 0b28ffb4baac9586566d246c3f0986b2bb650a33
lane head: 92151a50cc79b40700cafab98488012089f67e34
report: `.ufo/reports/round-67/mado.md` @ 7111b67bec4c129ec49ef22d3b703262fd72ed36
dispatched prompt: `.ufo/prompts/mado-round-67.md`
scope: non-author verification only. No lane-authored file edited, no `[x]` written, no
promotion, no sibling lane touched, no lane `git`/`jj` mutation. The round's counters and
harnesses were **not executed**: their committed per-case receipts were recomputed and the
claims re-derived from committed bytes (`git show`, `grep`, `awk`, `sha256sum`, `curl`).

## Conformance (step 1)

| check | command | observed | result |
|---|---|---|---|
| report attribution | `git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-67/mado.md` | `mado-shokunin 7111b67bec4c129ec49ef22d3b703262fd72ed36` | pass |
| report lands last | lane tip vs report vs watchdog | lane tip `92151a50` 21:50:54-03:00; report `7111b67b` 21:51:20-03:00; `complete` 21:51:57-03:00 | pass |
| SHONEN contract | `grep -c '^## SHONEN' <report>` / marker lines vs `SHONEN.md` boxes | `1` heading; 4 `[~]` lines, one per each of the 4 boxes, each with a pointer | pass |
| cited commits | `git cat-file -e` + `git merge-base --is-ancestor <h> refs/heads/master` | `0b28ffb4` and the eight round commits `aa7fe5a1`, `061dc329`, `ac376ef3`, `5f9ce459`, `caf131d6`, `2447048b`, `2f052318`, `92151a50` all exist and are ancestors; `git log --oneline 0b28ffb4..92151a50` = exactly those eight | pass |
| lane state | `scripts/hyaku/jj-lane.sh state .../mado-shokunin` | `branch=master local=92151a50cc79b40700cafab98488012089f67e34 remote=92151a50cc79b40700cafab98488012089f67e34 ahead=0 behind=0 head=detached tracked=0 untracked=0` | pass |
| clean tree | `git -C .../mado-shokunin status --porcelain` | empty | pass |
| prompt fidelity | template render, substitution only | 8281-byte prefix byte-identical to `templates/round-prompt.md` after `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}`/`<mado-repo>` substitution; remainder begins `## 6. Campaign addendum` | pass |
| prompt contract items | read through | mission/axes binding, 1–3 claims, frontier step, L2 floor, report path and filename, commit-before-report, `SHONEN` heading, commit-hash citation, write scope, commit-then-push, push scope, L0 side channel all present | pass |
| dispatch digest | `.ufo/watchdog.log` lines 2149/2160 | `2026-11-03T21:20:17-03:00 launch mado round=67 pgid=3915373 driver=hyaku-inline attempt=1` / `2026-11-03T21:51:57-03:00 complete mado round=67; hyaku-inline attempt=1` | pass |
| report pushed | `git ls-remote origin refs/heads/master` + ancestry | fleet `origin/master` `6d986e2f`; report commit `7111b67b` is an ancestor | pass |
| marker test | content read | work items, evidence pointers, receipts and real commits; not a completion marker | real report |

Conformance defects (status-neutral; none bars admission):

1. **C2 kill-rule prose does not describe the M-R decision.** The frozen declaration says "killed
   means the candidate control run exits nonzero on the mutant" and "the control set exits nonzero
   on that exact mutant". The M-R mutant's child run exits **0** (`rc=0 verdict=TARGET_MET
   missing=0 forged_credit=yes killed=yes`) and is counted killed by the harness's forged-credit
   flip (`quality/counters/c2-r67-landing-controls.py:267-269,489-490`). The printed counter line and
   the delivered control are real; the declaration's mechanism sentence is not.
2. **The "controls unchanged" sweep is path-vacuous.** `git diff aa7fe5a1..HEAD -- controls` from
   the lane root matches no path (`git ls-tree -r --name-only 92151a50 | grep -c '^controls/'` → `0`),
   so it returns empty regardless. With the nested path, `git diff aa7fe5a1 92151a50 --
   ':(glob)**/controls/**'` prints 15 lines: `score-baseline-c2.py` changed its default base
   `eafd500f` → `0b28ffb4` at `5f9ce459` (the disclosed B7 fix). The frozen case set
   `c1-controls.json` is byte-identical at both revs (blob `d5669bdc`), so no claim harm.
3. **Prompt carries two seat bands.** The template body says "each round is 32–128 seats", while
   the binding run-15 addendum says 8–16; the lane followed the addendum with 13 seats. Template
   drift, recorded, not a lane defect.

## Claims re-check

Both claims are bounded finite-control claims. The counters were **not executed**; each per-case
receipt is committed, the correct counts were recomputed from its recorded verdict flags, and the
structural claims were re-derived from committed source bytes.

### C1 calibration — register citation-to-live-object binding

Declared: the r66 counter accepts an unreferenced live object (4/6) and the r67 counter must accept
the genuine register and score 6/6 on the frozen six cases; bounded `10 × correct/6`, 6.6667 → 10.

```sh
cd mado-shokunin
git show 0b28ffb4:quality/counters/c1-r66-register.py | sed -n '99,113p'
#   checks every row's 4th receipt cell resolves and the exact live CLEAN line is in
#   LIVE_PATH's committed bytes; no LIVE_PATH-in-a-row-cell requirement.
git show caf131d6:quality/counters/c1-r67-register.py | sed -n '163,185p'
#   adds receipt-unresolved-in-receipt-cell, row-receipt-missing and
#   live-path-not-in-receipt-cell; requires the frozen live path inside some row's 4th cell.
python3 - <<'PY'
import json; d=json.load(open('.ufo/waves/round-67/controls/c1-controls.json'))
print(len(d['cases']), [(c['name'], c['expect']) for c in d['cases']])
PY
# 6 [('genuine','accept'),('duplicate-heading','reject'),('row-without-receipt','reject'),
#    ('file-plane-only','reject'),('unreferenced-live-object','reject'),
#    ('live-in-state-cell-only','reject')]
grep '^BASELINE_C1 case=' .ufo/waves/round-67/control-baseline-r67.txt
# genuine/duplicate-heading/row-without-receipt/file-plane-only correct=yes;
# unreferenced-live-object, live-in-state-cell-only correct=no  -> 4/6
grep -c 'correct=yes' .ufo/waves/round-67/control-baseline-r67.txt   # 4
grep '^C1_R67 case=' .ufo/waves/round-67/measurement-c1-after.txt
# all six correct=yes -> 6/6
grep -c 'correct=yes' .ufo/waves/round-67/measurement-c1-after.txt   # 6
git show caf131d6:PROVINCE.md | awk -F'|' '/^\| /{gsub(/^[ \t]+|[ \t]+$/,"",$5);
  if ($5 ~ /gate-live-r65\.txt/) n++} END{print n+0}'
# 4 rows cite the live receipt in their 4th cell; block has 8 group rows, 1 exact heading
git show caf131d6:.ufo/waves/round-65/receipts/gate-live-r65.txt | sha256sum
# 676ba88b484e194d4962ee27d07a54b5b7441a8461256b0f3ea0c83d1910e8ed (line 65 CLEAN, line 66 rc=0)
```

Observed: baseline `counter=quality/counters/c1-r66-register.py ... controls=6 correct=4/6`
(exit 0); candidate `MADO_R67_REGISTER: register=accept controls=6/6 headings=1 rows=8 groups=8/8
live-cited=yes verdict=TARGET_MET rev=caf131d6...` exit 0, selftest 16/16. The superseded counter's
source confirms why: it resolves row receipts and the live line but never binds the live path to a
row cell.

Verdict: **improved**, bounded (4/6 = 6.6667 → 6/6 = 10.0000). The stronger forgery
(genuine receipts, false state cells) and state-cell truth remain open as declared; no truth claim.

### C2 operability — zero-citation and replacement-ref controls

Declared: the standing instrument's selftest is green and the new control set kills M-Z (zero-citation
guard clause removed) and M-R (child's `GIT_NO_REPLACE_OBJECTS` removed); base leaves both untested
(0/2); bounded `10 × killed/2`, 0 → 10.

```sh
for f in quality/counters/c3-r56-used-by.py quality/check-tool-ledger.py tools/mado-receipt-citecheck.py; do
  echo -n "$f base="; git show 0b28ffb4:$f | grep -c 'GIT_NO_REPLACE_OBJECTS'
  echo -n "$f head="; git show caf131d6:$f | grep -c 'GIT_NO_REPLACE_OBJECTS'
done
# 0/0/0 → 1/1/1; the three diffs are one added env assignment each
git diff 0b28ffb4 caf131d6 -- quality/landing-counters.sh | grep -E '^[+-][^+-]'
# +27/−1: the single-line citecheck fixture becomes if [ zero ] / else; the non-zero branch is unchanged
git show caf131d6:quality/landing-counters.sh | grep -cF '[ "$citations" -gt 0 ] && '   # 1
grep -c '^SELFTEST ok' .ufo/waves/round-67/measurement-selftests-r67.txt                # 62
cat .ufo/waves/round-67/control-baseline-r67.txt
# C2 exit=1; zero_citation_case=0 replace_ref_case=0 usedby_guard=0 ledger_guard=0
# child_env_read=forged guarded_read=real; killed=0/2 verdict=TARGET_MISSED
cat .ufo/waves/round-67/measurement-c2-after.txt
# selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET rc 0
# M-Z rc=1 failed_assertions=3 killed=yes; M-R rc=0 TARGET_MET missing=0 forged_credit=yes killed=yes
cat .ufo/waves/round-67/measurement-baseline-derived.txt
# same harness at 0b28ffb4: selftest=0 mz=fail mr=fail killed=0/2 TARGET_MISSED rc 1
```

Observed: base 0/2, candidate 2/2; instrument selftest 62/62, harness selftest 47/47. The mutation
targets exist exactly once (guard clause; child env line), and the base instrument has neither the
zero-citation case nor a child guard.

Verdict: **improved**, bounded (0/2 = 0.0000 → 2/2 = 10.0000), with the kill-rule wording defect
routed below. Read literally for M-R ("mutant run exits nonzero") the declaration does not describe
the delivered observable; the delivered control is a real forged-credit flip, so the claim is graded
on the counter's measured `killed=2/2`, not on the mis-worded mechanism sentence. B1's limit stands:
M-R is landing-path-protected by inheritance and vulnerable standalone; the claim does not widen to
universal fault coverage.

## Axis verdicts

| axis | verdict | evidence |
|---|---|---|
| calibration | improved | C1 4/6 → 6/6 on the frozen six cases; live path bound inside a row receipt cell; r66 blob unchanged; stronger-forgery/state-truth limits declared |
| operability | improved | C2 0/2 → 2/2; three git-reading children now guard themselves; standing instrument 62/62, harness 47/47; real four-leg landing GREEN at `caf131d6` (nav 79/79, used-by missing=0, ledger 110/110, citations 7/7, all rc=0) |
| coverage | unchanged | no desktop surface or PROVINCE frontier move; the PROVINCE paragraph is a lane-instrument refinement, no new heading; knowledge entry is lane-tooling scoped |
| depth | improved (bounded) | one 189-line knowledge entry (blob/tree/commit replacement levels, presence-vs-truthiness of the guard, reader census, R-control limits) + SKILL registry rows + QUALITY 109 |
| freshness | unchanged | no existing knowledge entry re-verified; SOURCES diff is `1 0` (S436 only), no existing `status`/`recheck`/`used-by`/`opened` cell edited |
| adjacency | unchanged | connector screened sibling prior art and assimilation; no cross-domain write; the privacy finding is routed to L0, not absorbed |

## Discernment spot-check (LEARNING.md)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S436 — git-replace.adoc v2.56.0 | admit | `curl -fsSL https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc`; `git ls-remote https://github.com/git/git 'v2.56.0' 'v2.56.0^{}'` | agree | Bytes sha256 `3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631`, 5398 B, exactly as pinned; DESCRIPTION lines 34–36 carry the 21-word quote and 55–56 the 16-word guard sentence; tag object `24785443…` peels to `a0189536…`; host `git version 2.56.0`. Scope is correctly bounded to replacement-lookup semantics, not desktop state. |
| `core.useReplaceRefs` config-plane candidate | reject (screened, not a row) | `https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/config/core.adoc:761-764` | agree | The tag says only "If set to `false`, behave as if the `--no-replace-objects` option was given on the command line." It is a repo/user config plane; the bound child builds `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, so config cannot bind the process-level env guard. The flip condition (env-over-config precedence sentence, or a guard setting both planes) is the right bar. |
| "the guard proves authenticity or protects a rewritten repository" | reject (claim) | same `git-replace.adoc` (DESCRIPTION/BUGS/CAVEATS read in full) | agree | The document states lookup precedence and escape hatches; it makes no signature, provenance or un-rewrite claim. No admitted entry rests on authenticity. |
| S436 registry row shape | row check (new row) | `corpus/SOURCES.md:386` at `caf131d6` | agree | `NF=13` (11 cells, no literal pipe); kind `docs`, tier `A`, status `mined`, opened `2026-11-03`, recheck `on-release`; `used-by` names two paths that exist; `teaches` quote is 21 words. |

## Trend verdicts

- **expansion: improved (bounded)** — one admitted knowledge entry on ground the coverage map did
  not hold (`git diff --numstat 0b28ffb4 caf131d6 -- corpus/knowledge corpus/README.md` → `189 0`
  and `1 0`), its `source:` citing the mined `S436` row, coverage-map row landing in the same
  commit. No desktop or PROVINCE frontier move is claimed; the entry's Scope disclaims desktop
  coverage and state truth.
- **quality: improved** — two instruments tightened with owned controls and hermetic selftests
  (4/6→6/6, 0/2→2/2 at a named revision), QUALITY 109 grounded in the measured base failure, the
  standing instrument grew to 62/62 with the real four-leg landing GREEN; no admitted entry was
  found false or stale and left unmarked (no existing entry changed).
- **discernment: improved** — this outside sample agrees with the Gate's admit (S436) and both
  rejects (config-plane, authenticity); the round's own attack seats produced a mined mistake
  (M67-1, quote the child literal before freezing) and the B3 repair at integration with
  `FROZEN_VERDICT_CHANGES=0`. The defects below are evidence-wording defects, not gate taste.

## Routed defects (round 68 must fix; status-neutral)

1. **Freeze the per-mutant observable, not an M-Z-shaped sentence.** The C2 kill rule says the
   candidate control run "exits nonzero on the mutant"; M-R's mutant child exits 0 and is killed by
   the forged-credit flip. Freeze "unmutated control green; mutant child returns `rc=0
   TARGET_MET missing=0` → killed", or make the mutant path exit nonzero; stop describing the
   difference as merely "stricter" (B9).
2. **Fix the vacuous controls sweep.** The report's `git diff aa7fe5a1..HEAD -- controls` matches
   nothing from the lane root; use the explicit path and state the `score-baseline-c2.py` base
   correction (B7) in the same sentence as the unchanged `c1-controls.json`.
3. **Keep open (already planned):** the citecheck tool's standalone zero-citation contract
   (`TARGET_MET` at `citations=0`); the harness self-mutant `mr_killed = True` survivor; the C1
   row-count equivalent mutant; the unguarded git-reader census. None widens the frozen claim.
4. **Carry the B1 limit into the C2 row:** the M-R child is landing-path-protected by inheritance
   and vulnerable only standalone; the next C2-family claim must name that scope in the predicate,
   not only in the lesson.

## Notes for the operator

- All four `SHONEN.md` boxes remain `[~]`; the report's four `[~]` lines match one-per-box. Boxes 1
  (SKILL tables, cited sources) and 4 (province boundary) look mechanically checkable by a fresh
  non-author; boxes 2/3 rest on historical end-to-end evidence and outside-lane clearance.
  Promotion is operator-owned; this closure writes no `[x]` and performs no promotion.
- Open L0 questions r57–r60, the standing L2-floor line, the host-recovery pacman pause and the new
  r37/r38 session-material history question remain operator-owned; no waiver is inferred.
