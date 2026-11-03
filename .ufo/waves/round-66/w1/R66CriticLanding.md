# R66CriticLanding — C2 landing instrument critique (round 66, w1)

Seat: `R66CriticLanding` (critic, leaf). Lane: `mado-shokunin`. Declared base:
`eafd500fa7be76dca59e729435e231a5032cc037`; lane HEAD during review: `ed980316e330703030d0c17b2a7098e058295b99`.
Scope: frozen C2 predicate (`claims-declaration-r66.md` §C2), the landing instrument draft
(`w1/R66ExecLanding/landing-counters.sh`), and the adjacent count path (harness + driver).
No production edits, no commits, no integration. Tests ran on sandbox copies only; fixture git
writes only under `/fast/scratch/hyaku/mado-r66/R66CriticLanding/` (removed before yield).

Artifacts reviewed (sha256):
- `landing-counters.sh` final STOP-EDITS `e4767ec74f1ff481a826573c7880f6107734ad31bd3b085e0eaba45415d82c4f`
  (history: v1 `f72e579d…` → v2 `f0c8d74f…` → v3 `1671cebc…`)
- `check-controls.py` `218781fbbb5b005e226c5fdb88289beca453b8efe7bc2c460ccd39aeafe02fd1` (earlier during review: `94941bef…`, `832d5533…`)
- `c2-r66-landing-instrument.py` `e4d62b3c1e6f19f2cc1d6540d5f7feb33136cc6cb08e68ef31392d45b7dd6d65`

## Axes

- **A1 discrimination** — do (a) genuine red marker/rc1, (b) crash rc2, (c) skipped/forced-zero
  without marker, (d) missing used-by sibling map to RED/1, ERROR/2, ERROR/2, ERROR/2, and does
  GREEN require four genuine green markers?
- **A2 scope identity** — explicit `--round N` selects the default receipts tree and its dirty
  guard (no hardcoded round); baseline/candidate bytes are not conflated; explicit paths override.
- **A3 containment** — scratch refuses tmp-family and symlink escape; inherited `GIT_*` cannot
  redirect reads.
- **A4 evidence closure** — marker literals match real children; summary lines classify; the
  frozen count actually measures selftest + real four-leg landing as the claim requires.
- **A5 mutation hardness** — the hermetic selftest pins every predicate branch.

Frontier note: v2 improves A1/A2/A3 over r65 (verified below). Remaining exposure is A4 (the
count command omits two required legs; one false-green path in nav) and A5 (unpinned branches).

## Findings

| # | Sev | Axis | Finding | Smallest safe correction |
|---|---|---|---|---|
| F1 | closed | A4 | Count instrument 218781fb ran cases a–d only and printed `correct=4/4 TARGET_MET` without selftest/landing. Fixed in `84ec73dd…`: candidate selftest rc0 gate + driver TARGET_MET gate at rev (skip disclosed in diagnostic mode). L1 installed `84ec73dd…` at `.ufo/waves/round-66/check-controls.py`; verified on the installed path: a–d 4/4, selftest rc0, driver-skip line, TARGET_MET rc0 | none |
| F2 | P2→resolved | A1 | v2 accepted an empty-note corpus as GREEN/0 (`indexed=0/0`, `coverage=0.0000/10`); r65 crashed red (`ZeroDivisionError` → nav rc1 → RED/1) | nav body: exit 1 when `notes` is empty; `marker_valid`: treat `B==0` as not-green (accept rc1 as genuine red) |
| F3 | P2 | A4 | The frozen predicate's ledger literal `MADO_TOOL_LEDGER` exists nowhere; the real ledger child prints `LEDGER:` | Declaration premise erratum already records it; no code change (draft + harness shim correctly use `LEDGER:`); do not add an alias |
| F4 | P3 | A1 | Zero-citation classification changed: r65 leg guard → RED/1; v2 marker requires `citations>0` → ERROR/2 even with rc0 and a well-formed marker | If “preserve existing behavior outside cutover” binds: return RED/1 for marker-valid rc0 + `citations==0`; otherwise document the stricter ERROR |
| F5 | P3→resolved | A3 | In-repo `refs/replace` redirected `git show`/`ls-tree` reads with no inherited env; the blanket `GIT_*` unset did not neutralize it | Fixed in final `e4767ec7…`: after the scrub it exports `GIT_OPTIONAL_LOCKS=0 GIT_NO_REPLACE_OBJECTS=1`; verified — replace-ref fixture now reads the unreplaced commit (GREEN/0, indexed=1/1) and the dirty guard still refuses (rc2) |
| F6 | P3 | A5 | 58-assertion selftest now pins empty-population red (57–58) in addition to skip/crash/red/duplicate per leg, but still not inconsistent-marker (rc0+MISSED), wrong rev, nav parity or zero-citation; the shim does not witness child argv, so dropping `--paths` from `leg_citecheck` survives selftest | Add the 4 remaining assertions; log `"$@"` to `WITNESS` and assert the round-66 receipts path appears in the citecheck argv |
| F7 | P2 | A4 | Integration coupling: at the counted rev the round-66 receipts must be committed and every cited path must resolve; currently receipts are untracked and citecheck reports `citations=4 resolved=1 missing=3 verdict=TARGET_MISSED` | L1 must commit lesson + C1 counter + C2 instrument + C2 driver + round-66 receipts in one rev; the harness’s c2 candidate marker is the driver path, so installing only `landing-counters.sh` yields `candidate=absent` |

### F1 — count omitted selftest and real landing (P1; closed in `84ec73dd…`, installed and verified)

At sha `218781fb…` (the copy installed at `.ufo/waves/round-66/check-controls.py`), the count ran
cases a–d only: no candidate selftest, no driver/real-landing leg, yet it printed
`correct=4/4 TARGET_MET`. Evidence: `evidence/harness-missing-final-legs-grep.txt` (grep rc=1) and
`evidence/harness-c2-candidate-v2-latest.out`.

**Verified fix in seat draft `84ec73dd…`** (run in draft-diagnostic mode with landing v3
`1671cebc…`): the harness folds two gates into the verdict — (1) the candidate instrument selftest
must exit 0 (`candidate selftest rc=0`; the recorded `candidate-selftest.out` shows `58/58`), and
(2) at an integrated rev it extracts the c2-r66 driver at `--rev`, runs it with
`--repo/--rev/--scratch-root`, parses `MADO_R66_INSTRUMENT: … verdict=TARGET_MET`, and requires
rc0 (`verdict_ok = verdict_ok and d_rc == 0 and d_tok == "TARGET_MET"`). In draft-diagnostic mode
the driver is absent at rev, so the harness prints
`candidate driver=skipped (draft-diagnostic mode: driver absent at rev; the frozen command runs it
at an integrated rev)` — disclosed, not silently omitted. Observed output: a–d candidate 4/4,
`candidate selftest rc=0`, the driver-skipped line, `correct=4/4 TARGET_MET`, rc0
(`evidence/harness-c2-candidate-v3-84ec.out`; re-run with the final STOP-EDITS `e4767ec7…` gives the
same gated output: `evidence/harness-c2-candidate-final.out`).

**Installed and verified:** L1 replaced the installed frozen copy with `84ec73dd…` during review.
Running the installed `.ufo/waves/round-66/check-controls.py` against landing v3 reproduced the
gated output on the actual frozen path: a–d candidate 4/4, `candidate selftest rc=0`, the disclosed
driver-skip line, `correct=4/4 TARGET_MET`, rc0 (`evidence/harness-installed-84ec.out`).
`evidence/artifact-sha-v3.txt` records the matching sha.

### F2 — empty-note corpus is GREEN (P2, v2 landing draft)

Fixture: `corpus/knowledge/.keep` (directory exists, no `.md` notes), README with no knowledge
rows, receipts committed. v2 prints `revision=… indexed=0/0 missing=0 dangling=0 duplicates=0
coverage=0.0000/10`, nav rc0, summary GREEN, rc0. r65 baseline on the identical fixture crashes
in the nav body (`ZeroDivisionError: division by zero`), nav rc1, summary RED, rc1. This is both a
false-green path (zero notes cannot be a genuine green navigation marker) and a behavior change
outside the declared cutover. The guard `if notes else 0` in v2’s nav body removed the only
condition that made an empty corpus red.

Evidence: `evidence/landing-empty-corpus-v2.out`, `evidence/landing-empty-corpus-r65-baseline.out`
(+ `.err`). Correction: keep the marker well-formed and exit 1 when `notes` is empty; in
`marker_valid`, before the green branch, `if [ "$B" -eq 0 ]` accept only `rc=1` as genuine red
(or return 1 → ERROR/2). One condition in each place; no predicate change.

**Resolved in v3 `1671cebc…` (verified).** v3 sets `raise SystemExit(1 if not notes or missing …)`
and requires `B>0` for the green branch; the empty-note fixture now yields nav rc1 and
`MADO_LANDING_COUNTERS: RED (nav=1 …)` rc1 (`evidence/landing-empty-corpus-v3-resolved.out`),
selftest 58/58 including named empty-population assertions 57–58 (`evidence/selftest-v3.out`), the
real four-leg landing is still GREEN/0 (`evidence/landing-real-round65-v3.out`), and the frozen
harness still scores candidate 4/4 vs baseline 1/4 (`evidence/harness-c2-candidate-v3.out`).
The final STOP-EDITS `e4767ec7…` retains this behavior: empty corpus RED/1, selftest 58/58,
landing GREEN/0 (`evidence/landing-empty-corpus-final.out`, `selftest-final-e476.out`,
`landing-real-round65-final.out`).
The zero-citation ERROR/2 decision (F4) is documented by the executor as intentional.

### F3 — ledger marker literal (P3, declaration defect; erratum present)

`MADO_TOOL_LEDGER` appears only in `claims-declaration-r66.md`. The real child prints
`LEDGER:` (`quality/check-tool-ledger.py:350,368`), verified by direct run (`LEDGER: population=106
… verdict=TARGET_MET rev=ed980316…`, rc0). v2 and the harness shim bind `LEDGER:`; the erratum
`marker-premise-erratum.md` records the premise defect. Code is correct; the frozen literal is not.
Residual risk is closure-literal conformance only; nothing to fix in code, and no alias should be
added.

### F4 — zero citations: RED/1 → ERROR/2 (P3)

v2’s citecheck marker check requires `citations>0` and `citations==resolved+missing`; a rc0 child
with `citations=0` is classified ERROR/2 (`evidence/landing-zerocite-v2.out`, rc2). r65’s leg-level
zero-citation guard returned rc1 → RED/1. Not exercised by a–d; a deliberate strictness change.
If the “preserve existing behavior” clause is enforced strictly, map marker-valid rc0 + zero
citations back to RED/1; otherwise state the ERROR classification as intended.

### F5 — in-repo replace refs remain a read redirect (P3, residual)

No inherited environment needed: `git replace C1 C2` in a fixture makes
`git show C1:corpus/README.md` return C2’s bytes, and v2’s nav leg reads the substituted content
(RED/1 on the substituted corpus; `evidence/git-inrepo-replace-draft-v1.out`). This is outside the
predicate’s literal “inherited `GIT_*`” guarantee and the lane has zero replace refs
(`evidence/lane-state.txt`), so it is not live. Optional hardening is one line
(`export GIT_NO_REPLACE_OBJECTS=1` after the unset loop) if “bytes at rev” identity matters.

**Resolved in final `e4767ec7…` (verified).** The draft now exports
`GIT_OPTIONAL_LOCKS=0 GIT_NO_REPLACE_OBJECTS=1` immediately after the `GIT_*` scrub. Fixture with
`git replace C1 C2`: nav now reads the unreplaced C1 (`indexed=1/1`, `MADO_LANDING_COUNTERS:
GREEN`, rc0), where the pre-fix draft read the substituted corpus (RED/1)
(`evidence/git-inrepo-replace-final-GREEN.out`). Ambient `GIT_REPLACE_REF_BASE=refs/altpre/` remains
neutralized (GREEN, `evidence/git-replace-base-final-GREEN.out`). `GIT_OPTIONAL_LOCKS=0` does not
weaken the dirty guard: an uncommitted file in the selected round-66 receipts still refuses rc2
(`evidence/dirty-guard-final.out`). Selftest 58/58 and the real four-leg landing GREEN/0 are
unchanged (`evidence/selftest-final-e476.out`, `evidence/landing-real-round65-final.out`).

### F6 — selftest coverage gaps (P3, mutation hardness)

v2 selftest is 56/56 (reproduced: `evidence/selftest-v2.out`). It pins skip/crash/red and
duplicate-marker for each leg, missing sibling + ERROR classification, clean-fixture no-round
rejection, dirty decoys, explicit-path dirty guard, GIT steering, round/rev requirements and
scratch refusals. It does **not** pin: inconsistent marker (rc0 + TARGET_MISSED), wrong revision in
a marker, nav parity mismatch, zero-citation classification, or the empty-corpus case. My grid
proves those branches work today (`evidence/landing-inconsistent-marker-v2.out`,
`landing-wrong-rev-v2.out`, `landing-nav-parity-v2.out`, `landing-zerocite-v2.out`), so this is
coverage, not behavior: a mutation deleting any of those branches would still score 56/56. Also the
shim records only the leg name, not `"$@"`; a mutation dropping `--paths "${CITE_PATHS[@]}"` from
`leg_citecheck` would pass selftest (the real landing catches it only at integration).

### F7 — integration prerequisites (P2, sequencing; not a landing-draft defect)

The real four-leg landing at the counted rev requires:
1. `.ufo/waves/round-66/receipts` committed — currently untracked (`?? .ufo/waves/round-66/receipts/`),
   and v2’s selected-scope dirty guard exits 2 on it (`--round 66`).
2. Every citation in the selected tree resolves at `--rev`. `evidence-scope.txt` cites
   `corpus/lessons/round-66.md`, `quality/counters/c1-r66-register.py`,
   `quality/counters/c2-r66-landing-instrument.py`; at HEAD citecheck reports
   `files=2 citations=4 resolved=1 missing=3 verdict=TARGET_MISSED`, rc1
   (`evidence/citecheck-r66-scope-at-head.out`).
3. The harness’s c2 candidate marker is `quality/counters/c2-r66-landing-instrument.py`; if only
   `quality/landing-counters.sh` is installed at rev, the harness reports `candidate=absent` and
   scores baseline-only TARGET_MISSED (`evidence/harness-c2-baseline-only-latest.out`).
   The lesson, C1 counter and C2 driver exist as drafts
   (`w1/R66ScribeLesson/round-66.md`, `w1/R66ExecRegister/c1-r66-register.py`,
   `w1/R66ExecDriver/quality/counters/c2-r66-landing-instrument.py`), so this is sequencing for L1,
   not missing work in C2 seats.

## What held (positive validations)

- **a–d discrimination (v2, current harness diagnostic):** candidate 4/4 — a RED/1, b ERROR/2,
  c ERROR/2, d ERROR/2; baseline r65 1/4 (only a correct)
  (`evidence/harness-c2-candidate-v2-latest.out`).
- **v2 selftest** 56/56, rc0 (`evidence/selftest-v2.out`).
- **v2 real four-leg landing**, lane HEAD, `--round 65` with committed r65 receipts: GREEN/0, all
  four real child markers parsed (nav `revision/indexed`, `MADO_USED_BY:`, `LEDGER:`,
  `MADO_CITECHECK:`); summary rev is the resolved full sha
  (`evidence/landing-real-round65-v2.out`).
- **Marker/rc branch behavior (v1 grid, marker_valid unchanged in v2; spot-checked on v2):**
  genuine red marker → RED/1; crash rc2 → ERROR/2; skip/rc0 no marker → ERROR/2; missing used-by →
  ERROR/2 **with** `MADO_LANDING_COUNTERS: ERROR (...)` summary in v2
  (`evidence/landing-missing-usedby-v2.out`); inconsistent verdict → ERROR/2; duplicate marker →
  ERROR/2; wrong rev → ERROR/2; nav parity mismatch → ERROR/2.
- **Scope identity:** `--round` required (clean fixture, no default); selected round dirty → 2;
  a dirty decoy round is not guarded when not selected; explicit `--citecheck-paths` override and
  their own dirty guard fires; outside-repo path and repo-root path refused; absolute paths are
  confined to the repository.
- **Containment:** `/tmp`, `/var/tmp`, `/dev/shm` refused; any symlink ancestor (including a
  missing suffix below a symlink) refused with nothing created
  (`evidence/scratch-parent-symlink-refusal.err`). Inherited `GIT_REPLACE_REF_BASE` demonstrably
  redirects r65’s nav (baseline read the substituted corpus → RED/1) while v2’s blanket
  `${!GIT_@}` unset neutralizes it (GREEN) (`evidence/git-replace-base-baseline-r65.out`,
  `evidence/git-replace-base-draft-v1.out`). `GIT_NAMESPACE=e` produced no local read redirect in
  this git build (probe limitation recorded, not a safety proof).

## Resolved during review (do not chase)

The harness draft moved during this critique. At sha `94941bef…` the frozen command crashed with
`TypeError: not all arguments converted during string formatting` (tuple `case` at
`build_c2_fixture`, line 314; C1 side also called `build_c1_fixture` without its `rev` argument;
`evidence/harness-tuple-crash-old-sha.err`). Current sha `218781fb…` fixes the crash, extracts the
C2 baseline from the declared base rev `eafd500f…`, detects the candidate via the c2 driver marker,
runs both instruments from inside their committed fixtures, and separates `diag-all-green`
(shim-driven, GREEN/0 for candidate) from `diag-real-children` (observe-only: baseline RED/1,
candidate ERROR/2 on the minimal fixture). F1 above is the only remaining count-path defect I found.

## Limitations

- Controls a–c were exercised with my own synthetic marker shim (independent of the harness shim);
  d and the real landing used real children.
- The real landing was observed at `--round 65` only. The claim’s `--round 66` real landing at the
  integration rev is **not** claimed here: receipts are untracked and three cited paths are absent
  at HEAD (F7).
- Drafts moved during review (harness `94941bef` → `832d5533` → `218781fb`; landing `f72e579d` →
  `f0c8d74f`). Findings are pinned to the shas above; `evidence/artifact-sha.txt` records them.
- Fixture git writes were confined to my scratch tree with `git -C` and toplevel verification;
  no lane git/jj mutation, no host configuration/service/compositor changes, no credentials or
  session reads, no whole-repo build/lint/formatter run.
- The scratch root `/fast/scratch/hyaku/mado-r66/R66CriticLanding/` was removed before yield;
  curated raw outputs are retained under `w1/R66CriticLanding/evidence/`.

## Changed drafts

None. This seat is a critic: it did not edit the frozen target, the landing draft, the harness,
the driver, or any lane file.

## Evidence index (committed-path-ready, under `w1/R66CriticLanding/evidence/`)

- `artifact-sha.txt`, `lane-state.txt`
- `harness-c2-candidate-v2-latest.out` (+ `.err`), `harness-c2-baseline-only-latest.out`,
  `harness-missing-final-legs-grep.txt`
- `harness-tuple-crash-old-sha.out`/`.err` (historical sha `94941bef`)
- `selftest-v2.out`
- `landing-real-round65-v2.out`
- `landing-empty-corpus-v2.out`, `landing-empty-corpus-r65-baseline.out`/`.err`
- `landing-missing-usedby-v2.out`
- `landing-inconsistent-marker-v2.out`, `landing-duplicate-marker-v2.out`,
  `landing-wrong-rev-v2.out`, `landing-nav-parity-v2.out`, `landing-zerocite-v2.out`
- `git-replace-base-baseline-r65.out`, `git-replace-base-draft-v1.out`,
  `git-inrepo-replace-draft-v1.out`, `git-namespace-baseline.out`, `git-namespace-draft.out`
- `scratch-parent-symlink-refusal.err`
- `citecheck-r66-scope-at-head.out`
- v3 correction verification: `selftest-v3.out`, `landing-empty-corpus-v3-resolved.out`,
  `landing-real-round65-v3.out`, `harness-c2-candidate-v3.out`, `landing-zerocite-v3.out`,
  `artifact-sha-v3.txt` (landing v3 `1671cebc…`; installed count `218781fb…`; seat harness draft
  `84ec73dd…` is not the installed frozen copy)
- `harness-c2-candidate-v3-84ec.out`, `harness-installed-84ec.out` (gates folded on the installed
  frozen path: selftest 0, driver skip disclosed, a–d 4/4)
- `candidate-selftest-84ec.out` (v3 `58/58`, rc0, captured by the harness gate)
- final STOP-EDITS `e4767ec7…` verification: `selftest-final-e476.out`,
  `landing-real-round65-final.out`, `landing-empty-corpus-final.out`,
  `git-inrepo-replace-final-GREEN.out`, `git-replace-base-final-GREEN.out`,
  `dirty-guard-final.out`, `harness-c2-candidate-final.out`
