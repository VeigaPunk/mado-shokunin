# ReviewMistakesDraft — round 27 w2 review of `.ufo/waves/round-27/drafts/mistakes.md`

Reviewer: `MadoR27.ReviewMistakesDraft` (leaf, read-only). Reviewed the w1 ScribeMistakes draft row by row
against the cited evidence, checked every "captured-by" and QUALITY-criterion claim against
`corpus/QUALITY.md` and the cited lesson lines, assessed fix falsifiability, and added round-27 mistakes
visible so far in `registration.md` and the w1 reports. No counter, suite, oracle, gate or Hyprland was run;
no lane file outside this report was written; no tool was installed or updated. Hyprland coredump count
observed once this seat: 1338, delta 0 (no compositor started).

## Verdict

The draft's five rows are **accurate**: every evidence pointer resolves to the cited lines and says what the
row claims; every captured-by attribution is confirmed; every QUALITY.md citation (13, 28, 36, 37, and the
local sentence near 21) exists and is characterized correctly, and the three "None" claims hold. No factual
error was found in the draft. What the draft cannot say (it predates the w1 repair commit `b6650d5`) is the
**current tip status**: rows 1, 2 and 4 have their fixes already (partially) landed in round 27, row 3 is
drafted but not landed, row 5 is exactly what the w2 suite-B seats are building.

## Row-by-row accuracy against cited evidence

**Row 1 — SCORECARD evidence overclaim. Verified.** `corpus/lessons/round-26-verifier-spotcheck.md:146-148`
does carry the finding (":147: SCORECARD's "check-population … on both after-receipts → PASS" has no
committed run (the red/green file covers the base receipts only)"); the §2.4 table (rows at :141-144) records
the base-only evidence. The overclaimed sentence itself exists at `SCORECARD.md:1725-1726` (lane) and fleet
`.ufo/reports/round-26/mado.md:33`. QUALITY 13 is quoted correctly; the QUALITY 37 remark ("does not itself
supply the missing gate-run evidence") matches criterion 37's text. Captured-by (spot-check §2.4) correct.
*Tip status:* w1 `ExecPopulationAfter` committed the missing run —
`.ufo/waves/round-27/evidence/r26-population-after.txt` (sha256 `faf6df7e…23f98`, verified on disk): both
after-receipts → `POPULATION verdict=PASS receipts=2 agree=2`, exit 0, launched `env -i PATH=/usr/bin
HOME=/home/vgpnk`. The half of the fix that remains open: `SCORECARD.md:1725-1726` still does not cite that
evidence path or its four sha256 pins, and the seat's hidden-dependency probe (with the pre-v2 registration
at `05319e0` the same two receipts give `verdict=FAIL`, exit 1 — the sentence is true only because the
registration at its commit already carried the v2 paragraph) deserves a line beside the sentence.

**Row 2 — Stale PROVINCE behavior. Verified.** `:107-119` is the M26-10 ruling; the "Against it" paragraph
at :117-119 states exactly what the draft claims (no `environ` reference at `a496b02a`; env-using probe 3
binds vs round-25's 4; `PROVINCE.md:36-39` stale). Round-26 lesson errata M26-10 corroborates, and its
captured-by is "res CritClaims (non-author)" — `round-26/res/reports/CritClaims.md` exists, so the
captured-by chain in the draft is real. QUALITY 28 is correctly characterized (applies after a supersession
is identified; no tool-edit→row crosswalk rule). Captured-by correct.
*Tip status:* the fix landed in round-27 w1 commit `b6650d5` (10:43Z): `PROVINCE.md` now carries an
append-only "Round-27 correction (append-only; M26-10, round-26 spot-check §7 items 1 and 3)" naming the
round-25 sentence stale, with the recorded sweep `git grep -n -i 'environ\|environment' 5ddc5885 -- PROVINCE.md
corpus tools/mado-binds.py`; `tools/mado-binds.py:29-32` carries the matching "Environment limit (round-27
note, M26-10)" docstring paragraph. Verified in the worktree at tip. The behavior-limit probe (env-using tree
→ 3 binds) remains the falsification arm and was measured by the spot-check, not re-measured since.

**Row 3 — Gates without SKILL registry rows. Verified.** `:138-148` is the gates table plus the
"None is conformant … (`git diff 96101be5 14fcb814 -- SKILL.md` empty)" sentence; "no" for each of the three
gates. The QUALITY-column "None" claim holds: no general criterion requires a registry row; the sentence
inside criterion 21's block ("The runnable check and its failure evidence are registered in SKILL.md.") is
indeed local to criterion 21, as the draft says.
*Tip status:* still open. `grep -n "counter-selftest\|check-population\|check-control-receipts" SKILL.md`
at tip → no match (exit 1). The fix exists as a draft only:
`.ufo/waves/round-27/drafts/skill-registry.md` (six rows copying the `SKILL.md:600-601` header; the three
round-27 rows explicitly marked "lands this round, pending", with contract commands and no execution
evidence claimed). Per the draft's own proposed criterion, the three *new* round-27 gates
(`quality/counter-selftest.py`, `quality/population-suite.py`, the successor
`quality/check-control-receipts.py`) will also need rows before they support a verdict — note the successor
source is landed (`sha256 2233db1d…65af2`, verified) but still has no row.

**Row 4 — Q36 successor rejects its own round's receipt format. Verified.** `:142-148` covers the successor
table row (:144: exits 1, `no-receipt-under-…/controls/`, receipts are `.txt`, "chronology itself holds by
17 s, w2 MutQ36") and `corpus/lessons/round-26.md:32` (M26-8) records the same with the 17-second margin.
The QUALITY-column characterization of criterion 36 is exact (it exits 1 on late-first-receipt chronology or
a missing named shape; it does not require a green run on the current round's receipt paths). Captured-by
(MutQ36 + spot-check) correct. The "shown able to fail = yes, as a false rejection" judgment is right.
*Tip status:* the fix landed in round-27 w1 (`b6650d5`): new `quality/check-control-receipts.py`
(sha256 `2233db1d489fa325c3b4bd9b5b1dccc68eb9311864a0d975303907463fa65af2`, verified on disk) with
repeatable `--receipt-glob` (defaults `*.md` + `*.txt`, marker required only of markdown) and `--seeds N`;
evidence `.ufo/waves/round-27/quality/q36-successor-receipts.txt` (sha256 `5c162fe5…bd6e7b`, verified):
before-state reproduced red on lane bytes (defect 5: exit 1 `no-receipt-under-…`; defect 2: exit 2
`unrecognized arguments: --seeds 2`), round-26 `--seeds 1` → exit 0 `order=ok gap_s=17`, `--seeds 2` → exit 1
naming nine short shapes, 24 synthetic fixtures (9 green / 11 red / 4 exit-2), 9/9 single-locus mutants
killed with the green baseline unmoved, and round-24/25 legacy parity (`parity=ok` both).

**Row 5 — Population-gate sensitivity. Verified.** `:143-144` — line 143 records "w2 MutQ37 3/6 survive the
committed fixtures"; M26-8 at `round-26.md:32` names the survivors (CASE-anywhere, first-PRED-only,
parse-error exit 0). The draft's "Partly" verdict on shown-able-to-fail is right (three mutants *killed* is
exercised; the survivor coverage is not). QUALITY 37 as the unenforced behavior contract: correct.
Captured-by (MutQ37) correct.
*Tip status:* independent w1 corroboration exists — `K2R26Suites-seed{1,2}.txt` score the round-26
five-fixture population runner under the C2 counter and show exactly M2/M4/M6 surviving (`exit 0`,
`pass=5/5`) with M1/M3/M5 killed. The draft's fix is precisely the w2 suite-B contract
(`quality/population-suite.py --checker PATH` must reject the survivors); it is being built now and is not
yet landed, so at tip the fix is neither landed nor shown.

## Proposed QUALITY criterion (draft's closing paragraph)

Consistent with the routed defects and with the verified rows. Two observations for whoever promotes it:
(1) it must cover the three new round-27 gates, not only the round-26 ones (rows for them are the "pending"
drafts); (2) its "passing fixture in the round's actual receipt format" clause is exactly what row 4's fix
already demonstrates (green-txt fixtures), so promotion can cite `q36-successor-receipts.txt` as its first
worked example.

## Which proposed fix can be shown able to fail, and how

| row | fix | able to fail? | how |
|---|---|---|---|
| 1 | Commit the exact after-receipt checker runs (or correct the sentence) | **Yes — now exercised** | `.ufo/waves/round-27/evidence/r26-population-after.txt` is the run; any drift between the registration totals and the receipts' denominators/`CASE` lines flips it to `verdict=FAIL`, exit 1 — demonstrated by the seat's own sensitivity probe (pre-v2 registration → FAIL). Remaining half: cite it in `SCORECARD.md:1725-1726`. |
| 2 | Update the PROVINCE row and tool docstring in the round of the change | **Yes — landed, falsifiable** | `b6650d5` landed the append-only correction + docstring; the recorded sweep re-run (`git grep -n -i 'environ\|environment' <rev> -- PROVINCE.md corpus tools/mado-binds.py`) is the mechanical red arm (a stale present-tense seeding claim reappearing = fail), and the env-using-tree probe (3 binds vs 4) is the behavioral arm. |
| 3 | SKILL registry row per gate | **Not yet** | Nothing to fail while `SKILL.md` is unchanged and the rows are prose drafts marked pending. Once landed the check is mechanical (row present before the gate supports a verdict; a missing row or a rejection of valid current-round receipts = nonconformant), which is the draft's own proposed criterion. |
| 4 | Receipt-path/format option + positive current-format fixture | **Yes — landed and demonstrated** | 9/9 mutants killed by named fixtures (M5 restores defect 5 and is killed by `green-txt-glob`; M1/M2 pin the seed rule; M3/M4 pin glob scoping), before-state reproduced red, legacy rounds byte-parity — a committed, rerunnable red/green lattice. |
| 5 | Commit survivor witnesses as fixtures; suite proves rejection | **Yes — falsification arm already measured** | The current five-fixture runner demonstrably fails it: `K2R26Suites-seed{1,2}.txt` show M2/M4/M6 exit 0 at 5/5. The new `quality/population-suite.py` must flip those to nonzero while keeping the pristine/benign greens at 0 — directly scoreable, and the C2 counter will score exactly that. |

## Round-27 mistakes so far (registration + w1 reports)

**M-R27-1 · C1 counter v1 retired before data (fixture-role leakage).** w1 `CritC1Counter` (and
`CritRegistration` §1) showed a source-blind reader that scans every file, orders by filename buckets
(`hyprland.conf`, six-letter files) and resolves `$ws*` variables in a global prepass, meeting v1 at 41/41 on
two fresh seeds. Receipts committed and re-read by me: `controls/K1FlatScan-v1-seed{1,2}.txt` both end
`PRED-C1-r27 cases_pass=41/41 verdict=TARGET_MET`. Cause: v1 sourced every written file at the end of the
root and named generated files by role. Fix: counter v2 (DECOY files, ORDER, NESTED, GLOB, random
names/extensions). Class: M26-3 again (generator shape substituting for semantics). Captured by a non-author
critic before any data seat — the kill rule worked as designed.

**M-R27-2 · C1 v2 amended before any seat scored it (comparator + trap + prefix leak).** Two-fold: (a)
native `got == exp` plus `json.loads` lets `true≡1`, `false≡0`, `5≡5.0` pass (`CritRegistration` §3,
`CritC1Counter` §2: all 41 real tables boolean-flattened still compare equal natively); (b) v2 named every
VARREDEF variable `$wsr*` and every ordinary variable `$ws*` — a reader keyed on that prefix met v2 at 41/41
×2 (`CritC1Counter` follow-up, receipts `crit/CritC1Counter-v2-prefix-seed{1,2}.txt`, REV `a4dc0da0`). The
registration discloses that only the L1 pilot ran the unamended `f7f86d75…` bytes; the final v2 is
`25811884…` (sha re-verified by me). Fix: type-strict canonical JSON comparator + VARREDEF + v3 random
5-9-letter names.

**M-R27-3 · C1 counter v3 retired before data (generator-shape leakage, no label keying).** Two readers that
key on no name met v3 at 41/41 ×2 each (REV `71d4ea79`): GlobalOnce (single-definition names bound
everywhere; whole-field substitution; each file read once) and FileScope (sourced-file definitions never
reach the sourcer). Cause: v3 wrote all definitions at the top of the root, used whole fields only, and never
sourced a file twice. Fix: v4 adds SRCDEF, VAREMBED, USEBEFOREDEF, TWICE ( Hyprland-hyprlang semantics
checked against pinned sources: global variable list, substring substitution, no source dedup). Pilots and
the w1 rescores confirm partial readers no longer meet it (v4 L1 pilots 24/18/16; `K1FileScope` v4 seeds
29/41 and 32/41; `K1NoMerge` v4 7/41 and 9/41).

**M-R27-4 · C2 counter v1 retired before data (non-behavioral classifier + weak H validity + unsandboxed
suites).** w1 `CritC2Counter`: a classifier that normalizes the two generated benign-edit shapes and SHA-pins
the pristine subjects accepted 8/8 greens and rejected 15/15 W with **zero subjects executed**
(`NOT_A_CANONICAL_SCORE` diagnostic, two seeds); the H loader accepted comment-only equivalents, six
syntax-broken rows and eight copies of one effect as "valid"; every nonzero exit counted as a kill; and two
W `new` strings occur in pristine bytes, weakening the literal W-blocklist control. w1 `SentinelC2Clone`
(HIGH): suites ran as ordinary same-UID host subprocesses against a `--shared` clone (lane object store and
user files reachable; `--suite-*-rel` path escape). Fix: counter v2 — sealed behaviour-preserving edits join
the green set (b_valid), per-row compile/AST-distinct/byte-distinct validation, `--seal` manifest, `--no-local`
clones, bubblewrap sandbox hiding `/home` and `/fast`, shuffled runs, min-per-subject floor. The fix bites:
the L1 sealed rescore (`controls/v2/L1-sealed-rescore-summary.txt`, REV `b6650d58`, seal
`c2/heldout-seal.txt`, h_valid=18, h_need=14, min/subject 6) shows the normalized pin now failing green
(`K2NormPin green=8/17 … TARGET_MISSED`) and every control missing target. `ReviewWSet` verified all 15 W
mutants reproduce their round-26 probes (11 byte-exact; q37-M5 a documented, behaviourally identical textual
re-expression — noted so a future hash cross-diff is not misread as a defect).

**M-R27-5 · Harness residuals carried into round 27 (M26-5 fixed; snapshot ingress open).** w1
`ExecIsolationProbe` *measured* the M26-5 fix: with a fresh canary variable, round-26's sandbox pid-1 environ
exposed `MADO_R27_CANARY`, round-27's shows only `PATH` (receipt
`.ufo/waves/round-27/evidence/isolation-r27.txt`, sha `9313c6aa…`). Still open, and now evidenced rather
than hypothetical: (a) a **root-level** symlink resolving outside HOME makes *both* harnesses copy
outside-HOME bytes into the snapshot (`root_canary_copied=true` in the same receipt; `SentinelHarness27`
MEDIUM: the per-file guard tests HOME, not the resolved root; in-HOME links also escape the selected root);
(b) LOW TOCTOU between check and read; (c) both bwrap launches spell the wrapper as bare `env`, resolved via
the caller's PATH before `env -i` applies (`/usr/bin/env` would pin it); (d) `oracle()`'s own
`shutil.copytree(..., symlinks=False)` follows links for any caller that skips `snapshot()` (C1 is safe; the
contract note belongs in the next harness). The harness is frozen and pinned (sha `0da5b855…`, re-verified),
so like M26-5 these route to a successor harness; no measurement run touched the live session.

**M-R27-6 · Report transcription error in w1 `ExecBeforeReplicate.md` (receipts unaffected).** The report's
"Frozen pins re-verified" bullet writes the oracle pin as `0da0b85570e1…87601`; the true value in that seat's
own receipt line 1 (`evidence/c1-before-543f0445-run2.txt:1`), in every other w1 artifact that prints it, and
in my direct `sha256sum` is `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601`. `0da0b855`
is neither the value nor a true prefix/suffix — a plain transcription slip in a report (QUALITY 6/10
hygiene); the frozen evidence is correct. Cheap fix: erratum in that report; nothing else cites the wrong
prefix (grep-clean).

**M-R27-7 · Open instrument caveats now attached to the active v4 rule (visible, unremediated).**
(a) `layoutopt` is generated (`count-v4.py:104,121-122`) but never serialized by `workspacerules -j`
(`ReviewCounterCode` F3, pin-exact source check): a predictor that ignores `layoutopt` is indistinguishable
from one that models it — case descriptors overstate that feature's coverage. (b) The C1 counter still
builds BASE/APPEND from the invoking HOME at run time (`count-v4.py:362`, `os.path.expanduser("~")`): the
79-file snapshot digest is printed but the bytes are not committed, so "one command over committed bytes" is
bounded by the live HOME at measurement time (`CritRegistration` §4; input identity per receipt, not a
committed input). (c) `CritRegistration`: counter docstrings' "same sentence in the receipt" is literally
too strong (receipts carry the predicate identifier and measurements); and C1 passing output equality does
not by itself prove the "sourced" qualifier. None of these voids the frozen rule; all belong in the round
note or the next counter revision.

**Positive verifications (things round 27 got right that the draft's context implies were risks):**
M26-9 not repeated — every C1 control has two committed seeds per counter version (`controls/v2/*-seed{1,2}.txt`
… `controls/v4/*-seed{1,2}.txt`); the L1 re-scored every C2 control with the sealed H set before data
(`L1-sealed-rescore-summary.txt`); both before-receipts were replicated at base with fresh seeds
(`evidence/*-before-543f0445-run2.txt`, verdict-bearing lines byte-identical); all frozen pins I checked
match the registration (c1 v2-final `25811884…`, v3 `ee4cea19…`, v4 `635ae788…`, c2 v2 `4dfb34b5…`, oracle
`0da5b855…`).

## Residual risk and verification gaps

- I ran no counter, suite, oracle, gate or checker; every "pass/fail" quoted above is cited from committed
  receipts and reports, spot-checked for internal consistency (pins, verdict lines, exit codes), not
  re-executed. In particular the Q36 successor's green on round 26 and the 9/9 mutant kills are read from
  `q36-successor-receipts.txt`, not rerun.
- I did not open any sealed held-out file, `/fast/scratch/hyaku/mado-r27/crit|rescore|heldout|heldout-receipts`,
  or any Held* witness; held-out facts come from the w1 Held seat reports (counts + sha256 lines only) and the
  L1 sealed-rescore summary.
- `CritC1Counter` warns that readers meeting v2/v3 sit under `/fast/scratch/hyaku/mado-r27/crit/`; the data
  seats' no-read contract already covers this, but the L1's offer to copy those readers into `controls/` as
  K1 controls (so the kill evidence is lane-committed, like K1FlatScan/K1PrefixKeyed were) is still open for
  GlobalOnce/FileScope — their only lane-committed receipts at v4 are the L1 pilots plus the K1NoMerge seat's
  re-scores.
- Whether the operator's real `~/.config/omarchy/current/theme` root symlink stays inside HOME (M-R27-5a
  exposure) is not measured by any report I read.
- The draft's "shown able to fail?" column is about detection of each mistake, not about the fix; this report
  separates the two (table above), which is the only structural improvement it needs.

Report: `.ufo/waves/round-27/w2/reports/ReviewMistakesDraft.md`
