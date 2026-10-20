# ReviewMeasure — mado round 14 (w1)

Lane: mado-shokunin · Axes judged: coverage, operability · Milestone: U5 boundaries and regular-source targets
Reviewer: MadoR14.ReviewMeasure (leaf, no dispatch) · Date: 2026-10-20
Mode: read-only source review. **No measure runs, no gate runs, no fixture builds.** No tools installed or upgraded.

## Scope and inputs

- `.ufo/waves/round-13/measure.py` (107 lines, read in full, lines 1–107).
- `.ufo/waves/round-14/measure.py`: **not present.** MeasureBuild has not landed it. Findings below are requirements for that file, derived from the round-13 pattern it is told to reuse.
- Gate under test, read-only: `tools/mado-verify.sh` — `ROOT`/`H` (lines 83, 3415–3416), `build_fixture` (236–377), local census (2444–2486), source include graph (2371–2401), source resolver (2404–2437), toggle row (2510–2514).
- Round-13 evidence (committed artifacts, not re-run): `evidence/before.txt` (rev `7dcb785…`), `evidence/after.txt` (rev `95cbc41…`), `evidence/covering-results.tsv`.
- Registry header and one U4 note (`corpus/SOURCES.md:11–17`, `corpus/knowledge/wayland-protocol-boundaries-r13.md:14–16`).
- Round-14 spec items (`round-14/w1/spec.json`, MeasureBuild and ReviewMeasure prompts).

## Summary

Round-13 is sound on host isolation and revision source-of-truth. It has five defects that matter for round 14: the score denominators are literals; the named-detection predicate hides partial pre-existing detections; the directory cases' baseline is already mixed (one case is already red at baseline through a non-owning row); there is no clean or differential control; and harness faults are counted as misses. Coverage is also measured by question-text presence, not answer content. None of this blocks round 14, but the round-14 `measure.py` must not inherit these as-is.

## Findings by severity

### High

**H1 — Direct-directory case is already red at baseline through a non-owning row (C2 attribution).**
- `ai-usage.conf` is both a declared source (fixture `hyprland.conf` line 265, gate EXPECT line 2369) and a member of the LOCAL census (gate line 2450).
- The local census tests `[ -f "$H/$x.conf" ]` (gate 2466) and reports `missing:` on FAIL (2485). A directory named `ai-usage.conf` therefore fails `hypr.local.inventory` at baseline.
- Predicted baseline for "direct-directory replaces ai-usage.conf" [INFERENCE from code, not run]: `hypr.root.sources_resolve` **PASS** (`[ -e "$x" ]` at 2420 is true for a directory); `hypr.local.inventory` **FAIL** `missing: ai-usage.conf`; overall exit **1**.
- Consequences for the round-14 rubric: (a) "overall exit 1" cannot measure C2 for this case, because it is already 1; (b) the owning-row metric must be `hypr.root.sources_resolve` FAIL naming the directory, and must not be satisfied by the local-inventory row; (c) the round-13 isolation pattern ("local inventory PASS, untouched") does **not** apply to this case — `hypr.local.inventory` must be expected FAIL `missing: ai-usage.conf`, and that is retained behaviour, not a regression.

**H2 — Glob directory cases are undetected at baseline (predicted; this is the real C2 baseline).**
- The resolver uses `compgen -G` (gate 2422), which matches directories. Nothing checks regular-file-ness.
- Predicted baseline for all-directory toggle glob and mixed glob [INFERENCE]: `hypr.root.sources_resolve` PASS, `hypr.root.include_graph` PASS, `hypr.local.inventory` untouched (toggles directory is not in the LOCAL census), overall exit **0**. This is the true false-green the C2 change must close, and it must be recorded as 0/2 at the baseline rev, measured, not asserted.
- Caveat for the all-directory fixture: the toggle directory also holds `window-no-gaps.conf`, which the toggle row reads (gate 2511–2514, fixture line 284). If the fixture removes or replaces it, the independence claim must name the row it touches.

**H3 — Score denominators are literals, not derived from the scored set.**
- `exact_set.total: 4` (round-13 line 101) and `score = 2.5 * detected` (line 102) are hard-coded. Round-14 mixes 3 directory cases, 4 retained exact-set cases, and clean/order/symlink controls. A literal 4 or 2.5 weight silently mis-scores.
- `coverage.score = 10 * len(covered) / 7` (line 93) uses a literal universe size; prefer `len(ITEMS)` with `ITEMS = ['U1'…'U7']`.
- Requirement: `total = len(scored_cases)`, `score = 10 * detected / total` (or the weight declared once in the rubric), with controls excluded from numerator **and** denominator in code, not by convention.

**H4 — The named-detection predicate hides partial pre-existing detection; baseline 0/4 is not "nothing was detected".**
- `named_set_detection` (line 76) requires the conjunction of all tokens in the owning row. At baseline:
  - `replace-local`: the gate already reports `missing: xdph.conf` (before.txt line 102) — only `extra:` is absent.
  - `replace-source` and `missing-gkeep`: exit already 1 (before.txt lines 113, 125). `overall_failing_runs` = **3** at baseline (before.txt line 134). The gate was already red in 3 of 4 cases; the measure reports 0 detections.
- The round-13 result therefore conflates "gate already detects" with "gate detects by named set". The before→after delta is correct, but the rendered report must show per-token attribution (baseline exit, baseline owning row, baseline tokens present, after tokens present), or the reader cannot tell which capability changed.
- `overall_failing_runs` (line 99) counts exit==1 across runs, not detections. Rename or drop it for round 14.

### Medium

**M1 — Revision binding is weaker than its appearance.**
- Good: the gate and fixture both come from the same `rev` (lines 50–56: `source('tools/mado-verify.sh')`), and knowledge/registry come from `git show rev:…` (lines 14–15, 21). The gate under test is the committed one, not the worktree.
- Gaps: `rev` (line 11) is never resolved. A symbolic ref (`HEAD`, a branch) can move between the calls, and the output echoes the input string (line 80), not a SHA. The gate's blob SHA and the gate text's sha256 are not recorded, so an output cannot be tied back to the exact gate bytes.
- Requirement: `git rev-parse --verify --end-of-options "<rev>^{commit}"` once; print the full SHA; record `git rev-parse <sha>:tools/mado-verify.sh` and `sha256(gate.encode())`; take **two** explicit revs (`--baseline`, `--after`) rather than one argv.

**M2 — Mutations are not asserted to have applied.**
- `replace-source` (line 70) uses `str.replace`; if the target string is absent the replacement is a silent no-op, the tree stays clean, and the case is recorded as a gate miss. Requirement: assert `old != new` and that the line was present before writing.
- Directory cases: a directory must replace a file, so the builder must `unlink` then `mkdir`. Requirement: assert `Path(p).is_dir()` after mkdir and `not Path(p).exists()` before.

**M3 — No clean or differential control inside the measure.**
- Nothing proves that the same tree without the mutation is GREEN on the target row. A detection is only attributable if the unmutated tree passes that row and the mutated one fails it.
- Requirement (controls not in score): (a) clean tree — exit 0, owning row PASS; (b) order-swapped same-set tree — `hypr.root.include_graph` FAIL with a `line` clause (gate 2391–2393, **already detected at baseline** — report as retained, do not count as improvement), `hypr.root.sources_resolve` PASS (set exact, targets exist); (c) recommended addition: a symlink-to-regular-file tree — PASS, to pin the "follow file symlink" policy the GateImplement spec introduces. Each control in its own temp tree.

**M4 — Harness faults are counted as misses.**
- `detected` requires `returncode == 1` (line 76). A gate crash (exit 2), a missing verdict line, or a bash error is silently a non-detection. stderr is captured (line 73) but never recorded in the result.
- Requirement: `harness_error` predicate when exit ∉ {0,1} or the `MADO_VERIFY:` verdict line is absent; record stderr tail per case; a harness error must fail the measure, not score 0.

**M5 — Token matching is substring over the whole row.**
- `all(token in detail …)` (line 76) matches `extra:` / `missing:` / `extra.conf` anywhere in the row, including substrings such as `extra.conf.bak`.
- Requirement: parse the detail into clauses (`missing:`, `extra:`, `non-regular:`) and compare basenames exactly.
- Dependency: the `non-regular` literal is not yet defined in the gate. GateImplement's clause token and the measure's token must be a single shared constant, or the measure silently scores 0.

**M6 — Coverage facets check question text, not answers.**
- U4 facets (lines 36–43) pass if the question string is present, not if the answer is valid. In the joined note the feature facet is answered `[UNK]` (`wayland-protocol-boundaries-r13.md:16`), which is correct — but a note that replaced `[UNK]` with a positive claim would still score. "No feature exercise" is therefore not enforced by the measure.
- `u4_facets` (line 37) is one global dict overwritten per U4 note; with two U4 notes the reported facets may describe a non-joined note. Key by path.
- Requirement for U5: parse the answer cell; output-management and colour facets must cite S047/S048 in the same row; the feature facet must be an explicit unknown token (`[UNK]`), and any positive feature claim must fail the join.

**M7 — Registry parse drops rows silently.**
- `len(cells) == 13` (line 19) skips any row with a literal `|` or a malformed cell count without notice; duplicate IDs overwrite (line 20). Verified: the header has 11 data columns → 13 after the outer pipes, and indices 1/4/8/11 match `id/tier/status/used-by` (`SOURCES.md:11`).
- Requirement: count lines matching `^\| S\d{3,} ` and assert equality with parsed rows; assert ID uniqueness.

### Low

- **L1** `expected` is keyed by basename (line 48); two notes with the same basename in different directories collapse. Key by full path.
- **L2** `curated` (line 78) is a hard-coded round-13 ID list. Round-14 should declare its own list per round.
- **L3** No timeout and inherited env on `subprocess.run` (line 61, 73). Gate rows depend on `python3` (2555–2558 UNKNOWN branch). Pin `env` (PATH, `MADO_VERIFY_*` unset) so verdicts don't drift across shells.
- **L4** `sys.exit(0)` unconditional (line 107); acceptable only if M4's harness-error predicate exists.

## What is correct (keep)

- **Host isolation.** All writes go to `tempfile.TemporaryDirectory` (line 51). Git calls are `show`/`ls-tree` only. `build_fixture` (gate 236–377) is self-contained: it uses only `$R`; no `$HOME` appears in its span; symlinks are created inside the tree (312–313). The gate runs with `--root` and `--no-live` (line 73), so `ROOT` is not `$HOME` (gate 83, 3399–3411).
- **Independence of round-13 cases.** Each case builds a fresh tree (lines 58–61); no state is shared.
- **REPO resolution.** `parents[3]` resolves `mado-shokunin` from `.ufo/waves/round-N/measure.py`; the same depth holds for round 14.

## Baseline (what is already detected)

Observed (committed artifacts):
- rev `7dcb785…` (before.txt): `exact_set` 0/4 named; `overall_failing_runs` 3; `replace-local` already `FAIL missing: xdph.conf`.
- rev `95cbc41…` (after.txt): `exact_set` 4/4 named; `overall_failing_runs` 4.

Predicted for round-14 directory cases at the pre-change rev [INFERENCE from code; must be measured, not run here]:

| Case | sources_resolve | local inventory | include_graph | exit | Baseline C2 credit |
|---|---|---|---|---|---|
| D1 direct-directory `ai-usage.conf` | PASS (`-e`, 2420) | FAIL `missing: ai-usage.conf` (2466/2485) | PASS | 1 (already) | 0 — exit 1 is not attributable |
| G1 all-directory toggle glob | PASS (`compgen -G`, 2422) | PASS | PASS | 0 | 0 — true false-green |
| G2 mixed toggle glob | PASS | PASS | PASS | 0 | 0 — true false-green |
| O1 order-swap, same set | PASS (set exact) | PASS | FAIL `line N` (2391–2393) | 1 | retained; control only, not improvement |

## Recommended rubric (precise, for L1 before measuring)

1. Inputs: `--baseline REV --after REV`; resolve each to a SHA once; print SHAs, gate blob SHA, gate sha256.
2. Scored C2 cases (n = 3, `total = len(scored)`): D1, G1, G2. Each is a fresh tree; mutation asserted applied (M2).
3. Cell credit = 1 iff in the **after** run: `hypr.root.sources_resolve` FAIL, detail clauses include `non-regular:` naming the directory basename(s), exit == 1, `MADO_VERIFY: DIVERGED` present, and no `harness_error`. Weight declared once.
4. For D1, also assert `hypr.local.inventory` FAIL `missing: ai-usage.conf` is **unchanged from baseline** (retained, not credited).
5. Baseline column: the same three trees at the baseline rev, with per-token results (M4/H4). The delta is the credited improvement.
6. Unscored controls, each separate tree: clean (exit 0, all owning rows PASS); order-swap (include_graph `line` FAIL, sources_resolve PASS); symlink-to-regular (PASS). Reported in their own section.
7. Round-13 exact-set 4 cases: report separately as regression retention, not in the C2 denominator.
8. Coverage: U5 join requires S047 and S048 both mined with the note in `used-by` (reciprocal), answer-cell parse for facets (M6), feature facet explicit unknown.

## Verification gaps

- No measurement was run; all baseline predictions for round-14 cases are [INFERENCE] from gate source at lines cited above.
- The `non-regular` token is not defined in the gate yet (GateImplement pending); M5 cannot be fully checked until it is.
- Round-14 `measure.py` absent; MeasureBuild must land it, then a second review pass is required (not performed here).
- Authoring review is not non-author promotion authority. These findings are recommendations.

## Final-source review: round-14 measure.py (appended; MadoR14.ReviewMeasure)

Scope: one bounded read of the final `.ufo/waves/round-14/measure.py` (581 lines, re-read in full), High and Medium only. No measure, gate, fixture or test was run. The only shell use was a `printf %q` check on fixture display paths. Earlier sections are unchanged; this section records status.

### Confirmed in final source
- Seven controls present: clean, order_swap, symlink_to_regular, newline_regular, ai_usage_directory_overlap, direct_missing, zero_match_glob (measure.py:364-534).
- Scored predicate: exit 1, owning row FAIL, exact single-member clause, no unresolved/missing/extra class, sole FAIL row, toggle status, second-root detail equality (322-329). Denominator derived from `len(cases)` (355, 574).
- Mutations post-asserted (258, 267, 275, 430); order swap post-read (381-386).
- Gate-side predicates match gate source: row format (gate 3682-3686), toggle NOTE for an absent or non-regular toggle (2768-2774), clause order (2687-2688), `src_disp` `%q` form (225-231).
- `printf %q` leaves `-`, `.`, `/` and `_` unescaped, so the scored and control display paths are emitted unquoted. A space is single-quoted (`'a b.conf'`).

### High
- H-A (unchanged, operability): C2 measures only committed revisions. The GateImplement change is an uncommitted working-tree edit at HEAD 873ff08, and measure.py reads the gate only via `git show <rev_sha>:tools/mado-verify.sh` (56, 214). The lane contract forbids seat commits. Until L1 commits, or receives explicit commit authority, any `measure.py <rev>` run reads the pre-change gate and must return 0/3. Before the "after" run: commit, then record `revision_sha` and `gate_sha256` for both runs.

### Medium: new in final source
- M-A: `covers:` is first-match (160, `re.search`). The docstring (5-7) and MeasureBuild admission rule 2 require exactly one. Score impact is at most one credit per note, but the stated predicate is not enforced. Fix: `re.findall`, require one match.
- M-B: C1 is a metadata-and-facet count; the semantic check stays manual. `body_facets` (112-144) checks headings and a literal `[UNK]`. `reserved` (182) checks registry status, tier and `used-by` only, so it cannot see owner or revision. A `## Colour management` section asserting HDR works still scores U5. Agreement with the landed note rests on AttackCoverage §7; I did not re-open the note. Report 5/7 as "metadata + facets; semantic hand check recorded beside it."
- M-C: acceptance wording. The spec says the direct case "replaces ai-usage.conf"; the final source uses `windows.conf` (253-261, 279-283). The rationale holds: ai-usage is in the local census (gate 2466, 2485), so baseline exit would already be 1, which matches my earlier H1. The parent must acknowledge this change before L1 uses the rubric.
- M-D: retention is not measured. The goal says exact-set and order behavior are retained. Order is measured by `order_swap` (371-391, 475-484). The four round-13 named-set cases (extra-local, replace-local, replace-source, missing-gkeep) are not in this counter. Report retention from gate selftest cases N2/N3/N4/A/B/H, or add the four as unscored controls. Do not call it measured.
- M-E: latent parse gap. `non_regular_members` splits on whitespace (86). The gate quotes a whitespace path with `%q` (`'a b.conf'`). Such a target splits into `'a` and `b.conf'` and scores 0 at line 324 even when the gate is correct. No current case has whitespace, so no current score is affected.

### Medium: carried, still open
- C-1 (prior M7): registry rows are skipped silently when `len(cells) != 13` (98), and duplicate IDs overwrite silently (99). Add a row-count assertion and an ID-uniqueness check.
- C-2 (prior M6): `u4_facets` is one global dict overwritten per U4 note (151, 169); facets test question text by substring (170-175), not answers. No current effect, since only one U4 note exists.

### Resolved since first review
- H1 (direct-directory baseline exit, via windows.conf), H3 (derived denominator), H4 (exact clause and sole FAIL predicate), M1 (revision and gate digests printed), M2 (mutations asserted), M3 (controls landed), M4 (gate exit outside 0/1 raises), M5 for C2 (clause parsed; whitespace remains M-E).

### L1 checks (not run here)
- After H-A: `measure.py 873ff08` (expect C2 0/3), then `measure.py <L1-commit>`.
- Read the collateral toggle rows per case; do not report them as "all rows unchanged."
