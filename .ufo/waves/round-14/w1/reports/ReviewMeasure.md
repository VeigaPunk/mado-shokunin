# ReviewMeasure — rendered report (mado round 14, w1)

Status: review complete, read-only. No measure, gate, or fixture was run. No tools were installed or upgraded. Only this report and `.ufo/waves/round-14/w1/ReviewMeasure.md` were written.

Scope: `round-13/measure.py` (the round-14 `measure.py` does not exist yet) against the gate's directory and glob source resolver, the local census, and the coverage join. Axes: coverage, operability. Milestone: U5 boundaries and regular-source targets.

## Verdict on the round-13 measure

Sound on host isolation and on using a single revision as source of truth. Not reusable for round 14 without the changes below.

## Findings (by severity)

**High**
- **H1 Direct-directory is already red at baseline through a non-owning row.** `ai-usage.conf` is also in the local census; `-f` (gate 2466) fails on a directory and reports `missing:` on `hypr.local.inventory`. Baseline exit is already 1, so overall exit cannot credit C2. Credit only `hypr.root.sources_resolve` naming the directory, and keep the local-inventory FAIL as retained behaviour.
- **H2 Glob directory cases are undetected at baseline.** `compgen -G` (gate 2422) matches directories. Predicted baseline: sources_resolve PASS, include_graph PASS, exit 0 [INFERENCE]. This is the true C2 false-green. Measure it at the baseline rev; do not assert it. The all-directory fixture must account for `window-no-gaps.conf`, which the toggle row (gate 2511–2514) reads.
- **H3 Denominators are literals.** `total: 4` and `score = 2.5*detected` (round-13 lines 101–102); `/7` (line 93). Derive from the scored list; exclude controls by construction.
- **H4 The named-detection predicate hides partial pre-existing detection.** Baseline 0/4 hides that `replace-local` already reports `missing: xdph.conf` (before.txt:102) and that 3 of 4 runs were already exit 1 (before.txt:134). Report per-token baseline and after columns.

**Medium**
- **M1 Revision binding.** `rev` is not resolved to a SHA; the output echoes the input. Record the gate blob SHA and sha256 of the gate text. Take `--baseline` and `--after` as two explicit revs. (Positive: gate and fixture both come from `rev`, lines 50–56.)
- **M2 Unasserted mutations.** `str.replace` (line 70) is a silent no-op when the target is absent. Assert the mutation applied; for directories assert `is_dir()`.
- **M3 No clean or differential control.** Add unscored controls in separate trees: clean; order-swap (include_graph `line` FAIL already at baseline, sources_resolve PASS); symlink-to-regular (PASS).
- **M4 Harness faults counted as misses.** Exit ∉ {0,1} or missing `MADO_VERIFY:` verdict should be a harness error, not a 0 score; record stderr tail.
- **M5 Substring token matching.** Parse clauses and compare basenames exactly. The `non-regular` token must be one shared constant with GateImplement's gate text.
- **M6 Coverage checks question text, not answers.** U4 facets pass on question presence; the feature facet is `[UNK]` in the joined note (`wayland-protocol-boundaries-r13.md:16`), but a positive replacement would still count. `u4_facets` is a global overwritten per note (line 37); key by path. For U5, require S047 and S048 mined and reciprocal, and an explicit unknown feature facet.
- **M7 Silent registry drops.** `len(cells) == 13` (line 19) and duplicate IDs (line 20). Assert row count and uniqueness. The 11-column layout and indices 1/4/8/11 are verified against `SOURCES.md:11`.

**Low**
- L1 basename-keyed `expected` (line 48) collapses same-name notes.
- L2 hard-coded `curated` list (line 78).
- L3 no timeout; inherited env. Pin PATH and `MADO_VERIFY_*`.
- L4 unconditional `sys.exit(0)` (line 107); acceptable only with M4.

## Correct and to keep

- Host isolation: all writes in `TemporaryDirectory`; git read-only; `build_fixture` uses only `$R` (gate 236–377), no `$HOME`; symlinks inside the tree.
- Round-13 cases build independent trees.
- `REPO = parents[3]` is correct at round-14 depth.

## Predicted baseline for round-14 directory cases [INFERENCE, not run]

| Case | sources_resolve | local inventory | include_graph | exit | C2 credit at baseline |
|---|---|---|---|---|---|
| D1 direct-directory | PASS | FAIL missing ai-usage.conf | PASS | 1 | 0 (exit not attributable) |
| G1 all-directory glob | PASS | PASS | PASS | 0 | 0 |
| G2 mixed glob | PASS | PASS | PASS | 0 | 0 |
| O1 order-swap (control) | PASS | PASS | FAIL line N | 1 | retained; not improvement |

Observed: rev 7dcb785 — 0/4 named, 3 exit 1 (before.txt); rev 95cbc41 — 4/4 named (after.txt).

## Recommended rubric (for L1, before measuring)

1. `--baseline REV --after REV`; resolve SHAs once; print SHAs, gate blob SHA, gate sha256.
2. Scored (n=3): D1, G1, G2; fresh trees; mutation asserted.
3. Credit = 1 iff after-run `hypr.root.sources_resolve` FAIL, `non-regular:` clause names the basename, exit 1, verdict DIVERGED, no harness error.
4. D1: local inventory FAIL unchanged from baseline (retained, not credited).
5. Baseline column with per-token results; delta is the credited improvement.
6. Unscored controls in separate trees: clean, order-swap, symlink-to-regular.
7. Round-13 exact-set 4 cases reported separately as regression retention.
8. Coverage: U5 requires S047/S048 reciprocal mined; answer-cell facet parse; explicit unknown feature facet.

## Verification gaps

- No runs. Baseline predictions are inferred from the gate source at the lines cited.
- `non-regular` token not yet defined in the gate (GateImplement pending).
- Round-14 `measure.py` absent; a second review is required after MeasureBuild lands.
- Recommendations only; authoring review is not promotion authority.

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
