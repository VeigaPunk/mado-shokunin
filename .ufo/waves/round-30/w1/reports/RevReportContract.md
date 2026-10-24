# RevReportContract — round-30 report contract attack

Scope: report only. Artifact under test:
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/mado.md` (fleet commit
`bbae16bf9615fa8eb3619c03348f6388b23271cb`, 2026-10-24 04:00:43 -03, 10,669 B).
Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`; no lane write beyond this report.
No language server applies to a Markdown artifact; pointer resolution was done against
committed git blobs and filesystem existence. All measurements read committed bytes
(`git show REV:path`) or the fleet report file; none read the lane worktree.

## Verdict

**Conformant on the four mandatory checks; three minor presentation/conformance defects,
no missing required section and no unreproducible claim count.**

- Six required sections are present, as `##` headings, in the frozen order:
  Work performed (r:10), Landed changes (r:59), Before → after measurements (r:75),
  Sources & frontier (r:98), Trend verdicts (r:121), SHONEN (r:139). A seventh
  section `Round shape, waves, seats` (r:158) follows SHONEN — same placement as the
  r29 report, not a contract break. No placeholder tokens (`{{`, TODO, TBD, FIXME).
- Every claim number reproduces (table below).
- Every cited lane hash is an ancestor of `master`: `8f51071b`, `451e8b3c`, `446dc396`,
  `92d3c86` all pass `git merge-base --is-ancestor <hash> master` (master at review
  `d72243e1`; report's write-time tip `92d3c86` was the true tip then: lane commit
  times 03:59:42 vs report 04:00:43, next lane commit 04:03:37).
- SHONEN: exactly four `[~]` bullets, matching the four `SHONEN.md` boxes; the only
  literal `[x]` is inside the sentence "No \`[x]\`".

## Reproduced counts

| Report claim | Command run | Observed | Match |
|---|---|---|---|
| C1 41/43 exit 1 @ 8f51071b | frozen SCORECARD fence body (1,063 B / 20 lines, sha256 `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`) with `REV=8f51071b…` | `indexed=41/43 missing=2 dangling=0 duplicates=0 coverage=9.5349/10`, exit 1 | yes |
| C1 43/43 exit 0 @ 446dc396 | same fence, `REV=446dc396…` | `indexed=43/43 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0 | yes |
| C2 28/40, 31/39, UNRESOLVED {1–5,38–40}, TARGET_MISSED @ base | `python3 -I .ufo/waves/round-30/c2/count.py 8f51071b…` | identical to report and to `controls/C2K1-donothing.txt`, exit 1 | yes |
| C2 40/52, 40/40, superseded {1–5,18,19,20,32,38,39,40}, TARGET_MET @ 446dc396 | same counter at `446dc396…` | identical to report, exit 0 | yes |
| C3 41/43 exit 1 @ base; 43/43 exit 0 @ 446dc396; selftest 6/6 | `python3 -I quality/check-index.py --rev REV --repo .` and `--selftest` | matches `controls/C3K1-base-red.txt`, `C3K2-selftest.txt`, `evidence/c3-after-446dc396.txt` | yes |
| sources 184 → 185; A +1; no flips; no frontier advance; 7 W04; malformed 0; no dup ids; no missing used-by | frozen census (`CORPUS.md:135` greps) on `git show REV:corpus/SOURCES.md`; census validate with absolute script path | rows 184/185; tiers A=177→178 B=1 C=6; status mined=165→166 queued=10 rejected=9; malformed 0; dup ids empty; used-by missing empty; validate exit 0 with the same 7 W04 ids | yes |
| `MADO_SELFTEST: 460/460`, exit 0 | `bash tools/mado-verify.sh --selftest` at master | `MADO_SELFTEST: 460/460 assertions passed`, exit 0 | yes |
| 33 prepared seats; 6/3/3/1/11/4/2/1/1/1 roles | `w1-plan.json` counts and `w1-spec.json` item roles | spawn=33, total=33; role histogram identical | yes |
| "twelve ungrounded criteria are superseded" (r:127-129) | counter supersession targets + base literal gap | base literal gap = 40−28 = 12 = {1–5,18,19,20,32,38,39,40}; all 12 are supersession targets at tip (rows 41–51 plus pre-existing 21→20); claimed fraction 31/39→40/40 exact | yes (see note N1) |

Data-commit shape also matches Landed changes: `git show --stat 446dc396` = README +2
rows, QUALITY +22 lines (0 deletions, append-only), SOURCES +S185 only (single-line
insertion; no existing row touched), lesson 56 lines. Freeze `451e8b3c` carries the
registration, `c2/count.py`, `quality/check-index.py`, three controls and three
before-receipts. Records `92d3c86` carries the after-receipts, freeze smoke,
`census-end.txt`, wave spec+plan.

## Findings (severity-ordered)

### F1 — Minor (conformance): Sources & frontier prints no row-counting command (r:100-107)

Frozen contract (`/home/vgpnk/Projects/shokunin/templates/round-prompt.md:111-112`):
"`SOURCES.md` rows before→after **with the counting command**". The report prints two
"counting commands":

1. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
   — verified: prints the 7 W04 lines and `mado ok .../corpus/SOURCES.md`, exit 0;
   **it prints no row count**. The same relative path is fleet-root-only: run from the
   lane root it fails `bash: scripts/sources-census.sh: No such file or directory`,
   and the report never states that command's cwd while its other commands are
   lane-root commands.
2. "the frozen manual census (`CORPUS.md`)" — a file reference, not a command and no
   line; the row-producing grep is fleet `CORPUS.md:135`
   (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`).

The 184/185 numbers are still supported: both receipts are committed
(`census-before.txt` prints `=== rows at base blob 8f51071b === 184`, `census-end.txt`
prints `=== rows === 185`) and I reproduced both with the frozen grep. But the section
as printed does not carry the command that yields them — the r29 report printed the
grep inline (r29 report r:113-114). Fix: paste the frozen grep (or cite
`CORPUS.md:135`) and use the absolute path for the validator.

### F2 — Minor (pointer): `census-end.txt` path split across a code-span newline (r:105-106)

Line 105 ends ``(`.ufo/waves/round-30/evidence/`` and line 106 begins
``census-end.txt`: `validate` exit 0; ...)``. A soft line break inside a code span
renders as a space, so the pointer as displayed is
`.ufo/waves/round-30/evidence/ census-end.txt`, which does not resolve. The receipt
exists at `.ufo/waves/round-30/evidence/census-end.txt` (present in `git ls-tree
92d3c86`). This is the only code span in the report where the wrapped newline falls
inside a path (checked every code span; the other wraps fall on word boundaries of
commands/output and render correctly). Fix: rejoin the path on one line.

### F3 — Minor (executability): C1's counting command is not runnable as printed (r:77)

`REV=<rev> python3` followed by "literal fence (the SCORECARD 'Counting command'
block)". Alone, `python3` with no script/stdin reads the REPL. The named block does
reproduce both numbers exactly (table above), and its body sha is pinned by S185, so
this is a presentation defect, not a false number. Fix: cite `SCORECARD.md:69-89`
(body `:70-89`, sha `8b59b503…`) or inline the heredoc, as C2/C3 commands are inline.

## Notes (not defects)

- **N1 — "twelve ungrounded criteria" is reproducible, but only under the literal
  rubric.** The 12 = base literal gap (40−28) = {1–5,18,19,20,32,38,39,40}, and all 12
  are supersession targets at tip. Under the resolved-active rubric the base was
  already 31/39 with only 8 UNRESOLVED, and criterion 20 was superseded before this
  round; this round's own rows 41–51 supersede 11 criteria (r:42-43 says this
  correctly). If a reader takes r:127-129 as the round delta, it reads one high. Not
  an unreproducible count; optional precision fix ("eleven this round; twelve lines
  superseded at tip").
- **N2 — SHONEN sentence is time-bound.** "No `[x]`: every box lacks a named
  non-author verifier on record this round" was true at write (04:00:43). The
  non-author spot-check landed at `d72243e1` at 04:03:37, after the report; it is now
  on lane master and reaches the same four `[~]` dispositions, so no SHONEN mark is
  wrong. Closure should treat the sentence as stale-by-later-commit, not as a false
  claim.
- **N3 — Sourced-claim pointer is accurate but its target is not verbatim.** The report
  points only at "gate quote in `corpus/lessons/round-30.md` `## Gate`"; that lesson
  quote is a schematic rendering (`$covered/$total`) rather than the fence's f-string.
  The non-author spot-check already routes this to round 31; the report itself makes no
  "verbatim" claim, so this is not a report defect.

- **N4 — Wave/seat counts are point-in-time.** "Round total: 33 prepared seats,
  0 dispatched, 0 dead" (r:158-166) and "Wave 2: not prepared — wave-1 reports do not
  exist yet" were true at write; the orchestrator has since dispatched wave 1 (the
  seats producing these reports), which the report itself frames as outside the lane's
  action ("the orchestrator dispatches prepared waves itself between rounds").
  Closure should read those sentences as write-time state, not as a standing claim.

## Residual risk / verification gaps

- Harm-watch items `MADO_SELFTEST: 460/460`, "misroot sweep clean (0 mado-owned files
  at fleet root)" and "no compositor/config mutation" have no committed receipt under
  `.ufo/waves/round-30/evidence/`. I reproduced the selftest (460/460, exit 0, 19 s)
  and the census validate (exit 0); the misroot and compositor assertions are not
  re-derivable from committed bytes and rest on the report's word.
- Point-in-time claims are not receipt-backed: `0 dispatched`, `ahead=0`,
  "clean worktree at dispatch", and the watchdog lines. The live fleet
  `.ufo/watchdog.log` corroborates the two named lines
  (`:1162 launch mado round=30 … attempt=1` at 03:44:14, `:1163 complete …` at
  04:00:56), and `lane-dead-no-report mado round=30` is absent. `92d3c86` is an
  ancestor of both local and remote `master`; the report's closure state
  (local=remote=92d3c86, ahead=0) is confirmed by the non-author spot-check's
  conformance block, not by a round-30 receipt.
- The lane worktree is clean at review (`git status --porcelain` = only untracked
  `.ufo/waves/round-30/w1/`). A peer observed a transient
  `M quality/q36-successor-receipts.txt` at 04:06; it is not present now, and no
  committed byte used here changed.
- Out of scope here and left to sibling items: semantic truth of the two README rows,
  "verbatim" supersession of QUALITY rows 41–51, gate/fence semantic equivalence, and
  the trend-verdict adjudications. I did not re-run `sources-census.sh` census mode
  (tier histogram via the live script); I used the frozen grep.
