# RevHarmWatch18 — round-18 harm-watch command audit

Seat: `MadoR18.RevHarmWatch18` (reviewer, leaf; no subagents).
Date: 2026-10-20. Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

State at review: committed HEAD `d3a0000` (pre-registration); wave-1
artifacts and two tool edits are uncommitted in the worktree. Gate
`tools/mado-verify.sh` = `2bdf5e8a…` (GateRcFix mid-flight, `PIN_MADO` not
yet re-cut); the tripwire tool is mid-flight and its sha moved three times
during this audit (`962919ce…` at round 17; final value is whatever lands).
Counts below are from the reviewed bytes; L1's post-integration run is
the authoritative measurement.

Method: read-only. **No gate, selftest, scan, probe, or census was
executed.** Sources: `SCORECARD.md`, `SKILL.md`, round-17 evidence receipts,
`JjAuditMado.md`/`JjTrialMado.md`, round-18 wave specs and worktree bytes.
One usage probe (`python3 -I tools/mado-tripwire.py --help`) printed the
tool's usage/exit-2 verdict and read no files; it is disclosed here, not
counted as a harm-watch run. No tool was installed or updated.

## 1. The round's harm-watch commands and current expected outputs

Authority: `SCORECARD.md:931-984` (round-18 declared claims; harm watch at
`:982-983`), `SCORECARD.md:908-910` (round-17 harm watch at `f71ccbe`),
`SKILL.md:550,559,561-562` (registry rows), round-17 receipts under
`.ufo/waves/round-17/evidence/`. All commands run from the lane root.
"Baseline" = `d9a5a18`; "content" = the revision where both round-18 notes
and their `README.md` rows are committed.

| # | Literal command | Expected output on success | Exit | Expected move this round | Receipt / basis |
|---|---|---|---|---|---|
| HW1 | `bash tools/mado-verify.sh --selftest` | `MADO_SELFTEST: 372/372 assertions passed` (baseline, gate sha `fba82a66…`); post-GateRcFix `MADO_SELFTEST: 389/389 assertions passed` (§2) | 0; FAILED = 2 | **Count moves 372 → 389**; digest moves to the final gate sha (changes again when `PIN_MADO` is edited) | `.ufo/waves/round-17/evidence/harm-legacy-selftest.txt` (measured `f71ccbe`, exit 0, `fba82a66…`); gate bytes identical at `d9a5a18` (`git show d9a5a18:tools/mado-verify.sh \| sha256sum` = `fba82a66…`); `JjTrialMado.md` step 5 re-ran 372/372 |
| HW2 | `python3 -I tools/mado-action-plan.py --selftest` | `<last line> SELFTEST_SUMMARY: 52/52 passed`, exit 0; tool sha `226220ae…` | 0; 1 failed | **Unchanged** (no round-18 item edits this tool) | `.ufo/waves/round-17/evidence/harm-action-selftest.txt` (52/52, exit 0, `f71ccbe`); worktree and `d9a5a18` bytes both `226220ae…` |
| HW3a | `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/core` | `SELFTEST_SCRIPT_SHA256: <final tool sha>`; `SELFTEST_SUMMARY: 9/9 passed failed=[]` | 0 | **Count unchanged 9/9; sha line moves** to the final tool sha (no longer `962919ce…`) | `.ufo/waves/round-17/evidence/tripwire-selftest-core.txt` (9/9, `962919ce…`, exit 0); committed `expected.json` has 9 cases |
| HW3b | `… --selftest .ufo/waves/round-17/tripwire/compound` | `SELFTEST_SUMMARY: 16/16 passed failed=[]` | 0 | 16/16; sha line moves | `tripwire-selftest-compound.txt`; 16 cases |
| HW3c | `… --selftest .ufo/waves/round-17/tripwire/hardening` | `SELFTEST_SUMMARY: 33/33 passed failed=[]` | 0 | 33/33; sha line moves | `tripwire-selftest-hardening.txt`; 33 cases |
| HW3d | `… --selftest .ufo/waves/round-17/tripwire/w2-regressions` | `SELFTEST_SUMMARY: 30/30 passed failed=[]` | 0 | 30/30; sha line moves | `tripwire-selftest-w2-regressions.txt`; 30 cases |
| HW3e (new, C3) | `… --selftest .ufo/waves/round-18/tripwire/frozen` | `SELFTEST_SCRIPT_SHA256: <final tool sha>`; `SELFTEST_SUMMARY: 17/17 passed failed=[]` | 0 | **New suite: 17 cases**, not the 13 listed in the seat item | `.ufo/waves/round-18/tripwire/frozen/expected.json` — 17 cases, all `"mode":"frozen"`, labels cover all five outcomes; reviewed at 15:46Z |
| HW4 | `python3 .ufo/waves/round-16/measure.py REV` | `coverage.count == 7`, `coverage.items == ["U1"…"U7"]`, `coverage.score == 10.0`; `navigation.notes == navigation.indexed` = **32** at `d9a5a18`, **34** at content; missing/extra/duplicates empty | 0 even on a low count — **read the fields, not the exit** | **U stays 7/7; navigation 32 → 34** | `.ufo/waves/round-17/w2/reports/ReMeasureHarm.md` §1-2 (`coverage.count 7`, nav 32/32 at `988b858`, 30/30 at `27cd06f`); `RevNavigation.md` §1 fixes the 34/34 content expectation |
| HW5 | SCORECARD fleet-round-1 Counting command, literal fence `SCORECARD.md:69-90` (body `:70-89`), with `REV=<rev>` exported | `revision=<sha> indexed=32/32 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` at `d9a5a18`; `indexed=34/34 … coverage=10.0000/10` at content | 0; 1 on missing/dangling/duplicate | **32/32 → 34/34**; a 32/32 at content means the two note rows are missing | Fence body sha256 `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88` (round-17 `ReMeasureHarm.md` §2, recomputed there); `RevNavigation.md` §1 receipts at `d9a5a18` and `d3a0000` = 32/32 |
| HW6 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | The three historical W04 lines (S030, S042, S045), then `mado\tok\t…/corpus/SOURCES.md`; **no E-code line**; any *additional* W04 is contract-legal and must be reported, not dropped | 0; 1 on E/overdue; 2 usage/missing registry | **Textually unchanged at minimum**; new rows may add W04 (duplicate URL across scopes); any E-code is a failure | `.ufo/waves/round-18/evidence/census-start.txt` (15:31Z, identical four lines + `exit=0`); `.ufo/waves/round-17/evidence/census-end.txt` identical; script header exit map and E01-E12 list at `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:1-30` |

Not one of the six families but carried by the round: freshness file-plane
`29/29` (round 12, harm watch; **not re-measured** — do not present it as a
round-18 run); `.gitignore` now carries `.ufo/state/` (worktree line 2) —
no command output changes, and the directory does not exist today.

## 2. What a gate edit (GateRcFix) changes, and how the count must move

Only HW1 is affected. At the reviewed worktree (`tools/mado-verify.sh` sha
`2bdf5e8a…`) the diff against `d9a5a18` is confined to the gate:

- `:3450-3470` (was `:3406`): the `omarchy.skill.vs_head` row now captures
  the producer rc (`set -o pipefail; tmo git … show … | sha256sum | cut`)
  and routes `rc≠0` to `UNKNOWN "cannot read HEAD:<rel> (rc=N)"`; the
  empty-input digest `e3b0c442…` can no longer be compared. Correct as read:
  pipefail returns the rightmost non-zero (git's rc), and the hashed bytes
  are exactly `git show`'s stdout.
- `:663-680`: the selftest `git` stub gains `STUB_GIT_DESCRIBE_RC`,
  `STUB_GIT_REVPARSE_RC`, `STUB_GIT_SHOW_RC` (default 0, nonzero prints
  nothing).
- `:811-849`: two new OM scenarios, **OM9** (8 assertions: show rc 128 →
  `omarchy.skill.vs_head UNKNOWN`, detail names path + rc, no `local edit`;
  tag/head stay PASS; exactly one UNKNOWN and one FAIL; counts agree) and
  **OM10** (9 assertions: describe rc 128 → tag UNKNOWN, rev-parse rc 128 →
  head UNKNOWN, detail names `rc=128`, vs_head still PASS, no `MOVED:
  describe`/`MOVED: rev-parse`, exactly two UNKNOWNs, counts agree).

Measured delta from the worktree diff: **17 `st_*` assertions added, 0
removed** (`git diff -U0 -- tools/mado-verify.sh | grep '^+.*st_'` = 17;
`grep '^-.*st_'` = 0). Therefore:

- **Expected post-fix count: 389/389** (`372 + 17`), exit 0. The summary
  line is `MADO_SELFTEST: 389/389 assertions passed`.
- **`PIN_MADO` must move, and at review it has not.** The gate's derived
  regression target is built by excising the R7/R8 marker blocks; the OM
  block (`:622-849`) is *not* excised, so the 17 new assertions are inside
  the target. Recomputed with the gate's own `sed` excision: old derived
  target = `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96`
  = current `PIN_MADO`; new derived target =
  `20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744`.
  A selftest run before the re-cut prints `MADO_SELFTEST: FAILED — 388
  passed, 1 failed` with the R10 line and exits 2. That stale-pin red is
  **not** a harm-watch pass and **not** a gate bug; it is the required
  re-cut signal.
- The final gate sha cannot be stated before the PIN edit: `PIN_MADO` lives
  inside the file (inside the excised `MADO-R7-REGRESSION-BLOCK` at
  `:1591-2031`, so editing it does not change the derived target again).
  The receipt's first line must be `sha256sum tools/mado-verify.sh` of the
  final bytes, plus `measured_commit`.
- Companion gate-of-the-gate (not one of the six): `--regression` must be
  re-cut at the new target and print PASS with `10/10 KILLED`, GREEN
  control, `MUTATE_RESTORE: OK`. The old 10/10 at `cd1d73d7` does **not**
  transfer. `gate-rc-redbefore.txt` (landed) already proves the red-before
  direction: old gate on `git show` rc 128 emits
  `FAIL … HEAD blob e3b0c44298fc… (local edit)`; the fixed gate emits
  `UNKNOWN cannot read HEAD:default/omarchy-skill/SKILL.md (rc=128)` and
  zero `local edit`.

A post-edit reading of **372/372 with a changed gate sha is impossible if
the scenarios are wired** (17 assertions were added unconditionally); it
means the receipt came from the old bytes, or the OM9/OM10 block is not
executing. A reading of 388/389 is the stale-PIN signature. Any other count
means the landed diff differs from the reviewed one — recompute as
`372 + added − removed` from the final `git diff`.

HW2-HW6 are untouched by GateRcFix: the classifier, the tripwire tool, the
measure probes and the census script are not in the gate's write scope.

## 3. What the C3 tripwire edit changes

The tripwire diff is additive: hunks only in the docstring (`:24-35`), the
import, a new frozen section after `run_scan` (`:844+`), the `run_selftest`
mode branch (`:1075-1115`) and `main`'s usage (`:1139-1142`). The classifier
region (`~:48-834`) has **no** diff hunk, matching the TwFrozenMode item's
"Do not change scan classification behaviour."

- HW3a-HW3d counts must stay 9/16/33/30. Their `SELFTEST_SCRIPT_SHA256`
  line moves from the round-17 `962919ce…` to the final landed tool sha
  (re-read `sha256sum tools/mado-tripwire.py` after the last seat write;
  the value moved three times during this audit, so do not hardcode any
  mid-wave value). Comparing a post-edit receipt's sha line to the round-17
  `962919ce` receipt is a false regression.
- HW3e (new frozen suite) has **17** committed cases, all `mode: frozen`,
  spanning `frozen_match`, `frozen_verdict_mismatch`, `snapshot_tampered`,
  `unpinned_legacy`, `frozen_error`. Expected `17/17`, not 13/13; the seat
  item's list of 13 was widened by four controls (`match-permitted-only`,
  `match-permit-partial`, `absolute-input`, `verdict-exit-label`). Read the
  denominator from `expected.json`, never from the ticket prose.

## 4. U routes, navigation, census: sequencing and the honest move

- The two new notes are **untracked drafts** at review; HW4/HW5 read
  committed bytes only. At `d9a5a18` they must read 32/32; at the content
  commit they must read 34/34. Running either against `d3a0000` after the
  notes land on disk but before the content commit legitimately reads
  32/32 — that is the wrong revision, not a coverage regression.
- The U count is `coverage.count` from the round-16 probe, not
  `u_routes` from the round-17 probe (that field counts distinct `covers:`
  tokens and must not be quoted as "7/7": `RevRubricV.md` V7), and never
  the process exit (`measure.py` exits 0 on a low count: round-17
  `RevHarmWatch.md` F2).
- Keep the two new notes on `surface: P3` / `surface: P5` only. An
  accidental `covers: U<n>` line would disturb the U-side census
  (round-17 `RevHarmWatch.md` F4).
- HW6 is working-tree-bound and E11 checks that every mined `used-by` path
  exists on disk. Run it after `corpus/knowledge/{walker,theme}-route-r18.md`
  and the assigned S072+ rows are on disk. The three historical W04 lines
  must persist; new duplicate-URL W04 lines are contract-legal but must be
  reported; any E-code returns 1 and is a real census failure.
- HW2 is independent of every round-18 edit and is the only one of the six
  whose tool bytes are guaranteed unchanged.

## 5. Findings (severity order)

### F1 — medium (harm-watch false red): draft `r18-*` tripwire suites are expected red against the landed tool

The HarmWatchScript item says to run `--selftest <suite>` "for each suite
dir under `.ufo/waves/round-18/tripwire`". Three draft items
(`TwMissBashCVar`, `TwMissHelperFn`, `TwInstallerChannels`) create
`r18-bashcvar/`, `r18-helperfn/`, `r18-installers/` suites whose positive
cases encode *patches that are not applied* to the landed tool (their
prompts say "tested on a /tmp copy", "draft (do not apply)"). At integration
those suites will fail by design (exit 1), and a blanket enumeration would
misreport that as harm to HW3. Required shape: the all-pass tally is the
four round-17 suites plus `frozen`; if the script enumerates every dir, it
must read each `expected.json` and record non-frozen draft suites separately
as expected-red, never in the pass denominator or the "axes harmed" line.

### F2 — medium (stale count): 372/372 is the pre-edit expectation, not the round's

The pre-registration (`SCORECARD.md:982`) correctly says "hermetic selftest
N/N (re-cut if the gate moves)". The moved gate's N is 389 (17 added, 0
removed at the reviewed diff). Two failure modes to reject: copying 372
forward after the gate edit; or reading 388/389 and calling it a gate
regression when the PIN is merely stale. The landed `gate-selftest.txt`
must print the final denominator, the final gate sha, and
`measured_commit`; a 372/372 line beside a new gate sha is a stale receipt.

### F3 — medium (instrument substitution): U 7/7 is `coverage.count`, not the exit or `u_routes`

Round-17 already caught this (F2/V7). Restated because the round-18 report
will have both probes available: `python3 .ufo/waves/round-16/measure.py REV`
must be parsed for `coverage.count == 7` / `coverage.items` U1-U7 /
`coverage.score == 10.0`; the round-17 probe's `u_routes == 7` is a
different observation and `measure.py` exits 0 regardless of count.
Similarly, the navigation expectation is **34/34** at content, not 32/32;
both HW4's `navigation` block and HW5's fence must agree, and both must be
run at the content revision.

### F4 — low (census text): expected lines are four, not "three W04 and nothing else"

HW6's success text is exactly the three historical W04 lines plus
`mado\tok\t…/corpus/SOURCES.md` at `d9a5a18`; at content, additional W04
lines are legal and must be reported. No E01-E12 line may appear (E11 in
particular: every mined `used-by` path must exist — the two new note files
must be on disk with the exact `corpus/knowledge/<name>` path). The census
cannot prove the row delta; row/tier/status movement comes from
`measure.py` `source_registry`.

### F5 — low (tripwire sha line): counts stay, digests move

HW3a-HW3d receipts after the C3 edit will carry the new
`SELFTEST_SCRIPT_SHA256` with unchanged counts. The frozen suite's count is
17, read from `expected.json`; a 13/13 transcription from the seat item is
wrong. `--frozen` itself is C3's claim, not a harm-watch count.

### F6 — informational (gate-of-the-gate): PIN and regression re-cut are mandatory and unlanded at review

At 15:46Z `PIN_MADO` still reads the `d9a5a18`-derived
`cd1d73d7…`; the new derived target is `20714096…`. `gate-selftest.txt`
and `regression-recut.txt` are not yet on disk. Until they are, HW1's post
expectation is a prediction from the diff, not a measured receipt. The
red-before receipt (`gate-rc-redbefore.txt`) is landed and agrees with the
fix's intended direction.

### F7 — informational (`.gitignore`): no command effect

The worktree `.gitignore` line 2 is `.ufo/state/` (+1 line; `git
check-ignore .ufo/state/` matches). No harm-watch command reads `.gitignore`;
the directory is absent today, so the rule is forward-looking only.

### F8 — informational (freshness): carried, not measured

The round's harm-watch prose also carries freshness file-plane `29/29`
(round 12). It is not one of the six commands and is not re-measured this
round; do not report it as a round-18 observation.

### F9 — informational (hermeticity invariant): OM9/OM10 keep the PATH-staged stub

The new scenarios follow the existing rule: the gate is re-invoked with
`env PATH="$OMB"` (fixture stubs only) and `--root "$OMR"`, so no substrate
is read. The rule "every live-requested sub-invocation sets `PATH=`" remains
the gate's hermeticity invariant (round-17 F7); the new cases do not weaken
it.

## 6. Residual risk and verification gaps

- **No command was executed here.** Every expectation is receipt- and
  byte-derived; L1's single post-integration run is the confirming
  measurement. A runtime failure that differs from the receipts cannot be
  detected by this report.
- The gate and tripwire were **mid-flight** at review; their shas and the
  gate's selftest denominator can change before landing. The stable
  invariants are: gate = 372 + added − removed; tripwire legacy counts =
  9/16/33/30; frozen = `len(expected.json.cases)` = 17.
- The census is working-tree-bound; the navigation and U checks are
  revision-bound. They must be run against the intended tree/revision, and
  the census only after the notes and registry rows exist.
- Host package/service state is not observed or cleared; the host pause is
  binding and none of these commands queries it. R15-V1 stays
  operator-owned.
- Freshness `29/29` is a carried value, not this round's measurement.

## 7. Digests and anchors used

| Object | Value |
|---|---|
| HEAD / pre-registration | `d3a00003e6ef0b1e3c7b4faf52d592eb293857ba` |
| Baseline gate at `d9a5a18` | `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207` |
| Reviewed gate (pre-PIN) | `2bdf5e8afbb617142e4a881943084f94c9513327b1de25170ad71db113983925` |
| Old derived target = old `PIN_MADO` | `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96` |
| New derived target (reviewed bytes) | `20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744` |
| Classifier tool | `226220ae41436506c048258aff15fff83577acf0ae71ffa955d585a18ba5aea3` (unchanged) |
| Tripwire tool, round 17 | `962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072`; the round-18 final is `sha256sum` of the landed file (moved during review) |
| Round-16 measure probe | `ea3db43fdc75634b02c3fd4f1bc7aa1e54700b2e2d1ae2261e4b78ec1782c73c` |
| Round-17 measure probe | `de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc` |
| Navigation fence | `SCORECARD.md:69-90` (body `:70-89`); body sha `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88` |
| Gate selftest receipt (pre-edit) | `.ufo/waves/round-17/evidence/harm-legacy-selftest.txt` (372/372, exit 0, `f71ccbe`) |
| Classifier receipt (pre-edit) | `.ufo/waves/round-17/evidence/harm-action-selftest.txt` (52/52, exit 0, `f71ccbe`) |
| U/nav receipt | `.ufo/waves/round-17/w2/reports/ReMeasureHarm.md` §1-2; `.ufo/waves/round-18/w1/reports/RevNavigation.md` §1 |
| Census baseline (round 18) | `.ufo/waves/round-18/evidence/census-start.txt` (15:31Z, three W04 + ok, exit 0) |
| Gate red-before | `.ufo/waves/round-18/evidence/gate-rc-redbefore.txt` (old FAIL `local edit`/`e3b0c442…`; new UNKNOWN rc=128) |

**Verdict for the assignment:** the six harm-watch families are host-safe
(file/git-object reads, `/tmp` fixture scratch, stdout only; no
hyprctl/pacman/systemctl/service/compositor/input call). GateRcFix changes
**only HW1**, moving the expected count **372 → 389** and the gate digest,
with a mandatory `PIN_MADO`/regression re-cut; C3 changes only HW3's sha
line (counts 9/16/33/30) and adds the 17-case frozen suite. Navigation must
move **32/32 → 34/34** at content; U stays 7/7; the census keeps its four
baseline lines with no E-code. The only way this watch can silently
misreport is the three hazards named in F1-F3: draft-suite enumeration,
stale counts, and instrument substitution.
