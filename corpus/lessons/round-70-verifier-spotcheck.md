# Round 70 verifier spot-check (hyaku closure, non-author)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-04
lane-round: mado r70 (base b37a5aec4ea03f2223d8e09dd5d386d055c24179, tip 9fe84c1633a02ca8fb09442eea965765dccc6c74)
report: .ufo/reports/round-70/mado.md (fleet commit 43af7177a919cdd69997e98c74cad40673175932, author mado-shokunin <mado@shokunin.local>)

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %ae %H %s' -- .ufo/reports/round-70/mado.md` (fleet root) | `mado-shokunin mado@shokunin.local 43af7177… round-70: mado report` | conformant |
| SHONEN heading, one line per box | `grep -n '^## SHONEN'` + `grep -c '^- \['` on the report | heading at report line 93; 4 `[~]` lines, each with a resolvable pointer | conformant |
| Cited commits exist and are ancestors of the branch | `git merge-base --is-ancestor <hash> master` for all 15 landed commits, the base and the tip (lane repo) | 17/17 ANCESTOR-OK | conformant |
| Landed-changes table completeness | `git log --reverse --format='%H' b37a5aec..master \| wc -l` | 15 commits, all authored `mado-shokunin`, matching the report's 15/15 table | conformant |
| Lane pushed, no divergence | `scripts/hyaku/jj-lane.sh state mado-shokunin` | `branch=master local=9fe84c16… remote=9fe84c16… ahead=0 behind=0` | conformant |
| Prompt carries the template contract | read of `.ufo/prompts/mado-round-70.md` | round-level items (mission/axes binding §1, L2 floor §3, commit-then-push §4/§5, push scope §5, L0 side channel §5) and the five child-lane items (report path §4, commit-before-report §4, SHONEN heading §4, commit-hash citation rule §4, write scope §3) all present verbatim | conformant |
| No uncommitted round work | `git status --porcelain` (lane) | **DEFECT**: 4 modified round-70 files (below) | defect, status-neutral |

**Conformance defect (routed to lane for round 71):** four round-70 seat-report files sit modified in the
lane working tree, never committed: `.ufo/waves/round-70/w1/R70ScribeEntryC1.md`,
`.ufo/waves/round-70/w1/R70ScribeEntryC1/draft/corpus/knowledge/landing-kill-credit-real-children-r70.md`,
`.ufo/waves/round-70/w1/R70ScribeEntryC2.md`, `.ufo/waves/round-70/w1/R70ScribeRowLesson.md`
(mt 2026-11-03 23:47–23:48 -03, before the 23:54:26 complete line — round-70 leftovers, not a later round's
work; mado round 71 has no dispatch line). The round's own harm-watch already flagged the dirty `w1` dir on
the committed-seat-report citecheck leg. Per the inherited-state rule the lane commits them under its next
round entry or reverts them; the closure never edits lane files.

## Per-claim re-check

Both claims RE-MEASURED (I ran the lane's frozen counting commands myself at the closure-required
revision 9fe84c1633a02ca8fb09442eea965765dccc6c74; scratch roots under
`/fast/scratch/hyaku/closure-mado-r70/`, caller-created outside /tmp per the receipt's own note).

**C1 — calibration (real-children kill credit).** Command:
`python3 -I quality/counters/c1-r70-real-children.py --repo . --rev 9fe84c16… --base-rev b37a5aec… --scratch-root /fast/scratch/hyaku/closure-mado-r70/c1`
Observed: `MADO_R70_SCENARIO` genuine `candidate_mz=pass base_mz=pass correct=yes base_correct=yes`;
crash `candidate_mz=fail base_mz=pass correct=yes base_correct=no`; garbage
`candidate_mz=fail base_mz=pass correct=yes base_correct=no`; contract line
`MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=1 verdict=TARGET_MET rev=9fe84c16…`, rc 0.
Matches the frozen sentence and the report's measured content receipt byte-for-byte in substance.
Freeze order verified by commit graph: declaration + do-nothing receipts + frozen control set land in
`bc18399b` (committer 1793759225), the instruments in `5144a6b5` (+161 s) and the measurement receipt in
`71caa8b7` — freeze strictly before data. Do-nothing control (evidence-verified, not re-executed):
`control-baseline-r70.txt` shows the held r69 harness crediting crash and garbage (`base_correct=1/3`).
**Verdict: improved.**

**C2 — operability (guard carrier census).** Command:
`python3 -I quality/counters/c2-r70-carriers.py --repo . --rev 9fe84c16… --base-rev b37a5aec… --controls .ufo/waves/round-70/controls/c2-controls-r70.json --scratch-root /fast/scratch/hyaku/closure-mado-r70/c2`
Observed: controls header `cases=17 sha256=29947b4ce5890f5c977f3ec74bafd14ba12b0d581dcb03ef1e3b637017a778ff`
(digest re-verified with `sha256sum` over the committed file); 13 readers all `guard=yes`; all 17 candidate
controls `correct=yes`; base leg `controls=13/17` with the four carriers (`alias-carried`,
`attribute-carried`, `splat-carried`, `constant-key`) missed as the do-nothing control must;
contract line `MADO_R70_GUARD_CARRIERS: population=20 readers=13 guarded=13 unguarded=0 controls=17/17
base_controls=13/17 verdict=TARGET_MET rev=9fe84c16…`, rc 0. Matches the frozen sentence and the report.
**Verdict: improved.**

**No owned axis harmed.** `git diff b37a5aec 9fe84c16 -- SCORECARD.md` is purely additive (the round-70
entry plus the round-69 B1–B11 closure dispositions). Axis table, index and ledger re-measured by me at the
tip: `check-index.py` → `indexed=83/83 coverage=10.0000/10`; `check-tool-ledger.py` →
`population=119 ledger_rows=119 uncovered=0 verdict=TARGET_MET`; both rc 0. The gate legs (selftest 460/460,
r69 frozen pair counter TARGET_MET, landing GREEN on explicit committed paths, instrument selftests
68/68, 26/26, 54/54, 43/43, 59/59) are lane-owned gate evidence — verified as committed receipts in
`harm-watch-r70.txt` (fd2599c9) and `final-record-checks-r70.txt` (5a7af0fb), not re-executed per the
Gate standard's closure consequence. Frontier numbers re-measured: census `mado rows 378, tier.A 364,
tier.B 7, tier.C 7` with before-receipt 375/361 in `w1/R70ScoutCensus/census-census-r70.txt` (+3 A/docs/mined,
as reported); QUALITY criteria 112–113 present with shown-able-to-fail evidence; LOG round-70 entry verified
at LOG.md:3408–3465 (wc -l LOG.md = 3465).

## Discernment spot-check (LEARNING.md — outside check)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S439 admit (expressions.rst dictionary unpacking) | admitted, tier A | fetched `raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/expressions.rst` | **agree** | sha256 `e19de4f…` byte-identical to the lesson's record; located quote "A double asterisk ** denotes dictionary unpacking. Its operand must be a mapping. Each mapping item is added to the new dictionary." present at lines 514–517; 22 ≤ 25 words; grounding sentence real |
| S440 admit (simple_stmts.rst subscription target) | admitted, tier A | fetched `…/v3.14.8/Doc/reference/simple_stmts.rst` | **agree** | sha256 `d432064…` byte-identical; quote "If the target is a subscription: The primary expression in the reference is evaluated. Next, the subscript expression is evaluated." present at lines 190–192; the row honestly records the sentence is NOT in expressions.rst (E4 correction) — the admit targets the page that actually carries the claim |
| S441 admit (rendered subprocess.html returncode) | admitted, tier A | fetched `docs.python.org/3.14/library/subprocess.html` | **agree** | both located quotes present at lines 361–365 ("Exit status of the child process…", "A negative value -N indicates…"); live page digest drifted (`c8a66b3a…` → `cba9aefe…`) which is expected for a rendered doc — the quote location holds; distinct artifact from S108's raw rst is a sound basis |
| subprocess.rst as a NEW row | rejected (duplicate of S108) | fetched `…/v3.14.8/Doc/library/subprocess.rst` + read S108's registry row | **agree** | fetched bytes 61,603 B sha256 `05cd782c…`, byte-identical to S108's recorded digest; S108 already indexes the same URL; a second row would double-index one page; the flip (re-open S108 as a superseding row per CORPUS rule 2) is the correct mechanism |
| ast.rst as a new row | rejected (implementation shape, not runtime semantics) | row reasoning checked against the claim's subject | **agree** | the claim rests on what an environment is at runtime (what reaches a child); ast.rst documents the node vocabulary the detector reads — tier-A-for-this-scope would misground the claim; flip condition (a classifier-grammar claim) is reasonable |

New registry rows S439/S440/S441 re-opened and quote-checked (≤25-word quotes, all present at recorded
locators; S439/S440 digests byte-identical to the rows' pins). `sources-census.sh validate --root … mado`
run by me: exit 0, final line `mado ok /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`
(38 warnings, all pre-existing W01/W04 duplicate-url families; no E-class errors). Spot-check agrees with
the gate on 3/3 admits and 2/2 rejects sampled.

## Trend verdicts

- **expansion: unchanged** — `git diff b37a5aec 9fe84c16 -- corpus/README.md` adds two knowledge rows and a
  Frontier row, both on the held lane-tooling ground (landing harness / guard census, the r67–r69
  instrument family); no new desktop-domain surface enters the coverage map, matching the report.
- **quality: improved** — re-measured 1/3 → 3/3 (real-child kill credit) and 13/17 → 17/17 (carrier
  discrimination) at the round tip; the reviewer's attribute/constant-shadow counterexamples were repaired
  with committed red-before/green-after (`c2-classifier-repair-r70.txt`); remaining breadth limits
  (splat/alias shapes, agreement-only stand-in) are explicitly disclosed and pinned in selftests, so the
  improvement is bounded but real.
- **discernment: improved** — this outside spot-check agrees with every sampled gate decision (3 admits,
  2 rejects); the lane refused a duplicate and an ill-grounded row, kept its red receipts, and corrected
  its own attribution mistakes as errata E1–E6 without rewriting the frozen declaration.

## Routed defects for the next round

1. **Uncommitted round-70 leftovers** (4 files, named in Step-1): commit under the round-71 entry or
   revert; until then the lane working tree is dirty against a closed round.
2. **Standing instrument wart** (already the lane's own erratum E2): `quality/landing-counters.sh`
   default `--citecheck-paths` points at a `round-N/receipts` directory no round commits, so the default
   invocation exits 2 as a setup error; either commit receipts at that path or change the default.
3. Round-69 deliverable/report-citation defects (`check-deliverables.py` red on r69 seat reports) remain
   observed-not-repaired per the report; they belong to a round-69 correction entry, not this round.

## SHONEN note for the operator

All four SHONEN boxes stand at `[~]` with resolvable pointers; the report's evidence (decision tables and
checklists in SKILL.md, the round-3 end-to-end LOG entry, PROVINCE boundary reads) looks mechanically
checkable by a non-author promotion reviewer. Promotion authority is operator-owned; this closure writes no
`[x]`.
