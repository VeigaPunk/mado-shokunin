# L2 seat R12Reviewer-3 — final output (verbatim, 2026-10-19)

**Review of a6528e6 (round-12 pre-registration).** Read-only; I wrote only under `/tmp/mado-r12-reviewer/`. Committed-bytes measurements use `git archive a6528e6`. Worktree readings are labelled in-flight.

**Bottom line:** every recorded baseline reproduces, and the commit order is compliant. Three rubrics are vacuously satisfiable, depth and adjacency are non-compliant with AXES.md, and the C2 "re-anchor to 18/13" is blessing drift as pre-registered. The in-flight worktree already executes that re-anchor.

## (1) Re-run of every counting command (committed bytes, a6528e6)

| Command | before.txt | a6528e6 rerun | |
|---|---|---|---|
| `grep -cE '^[0-9]+\. .*lessons/' corpus/QUALITY.md` | 0 | 0 | match |
| `grep -cE '^[0-9]+\. ' corpus/QUALITY.md` | 5 | 5 | match |
| `--no-live` FAIL+UNKNOWN / PASS | 1 / 28 | 1 / 28 (`hypr.root.include_graph`, 18 vs 17) | match |
| knowledge notes with S-id `source:` in head-15 | 0 | 0 | match |
| `test -e corpus/SOURCES.md` | absent | absent (rc 1) | match |
| `grep -rc getprop corpus SKILL.md` sum | 0 | 0 | match |
| triple-header count / note count | 3 / 22 | 3 / 22 | match |
| `sha256sum tools/mado-verify.sh` | 93e43f8f… | 93e43f8f…, 3,231 L / 150,103 B | match |
| `--selftest` | 268/268 | 268/268, exit 0 | match |
| navigation fence, `REV=a6528e6 bash -s` | — | 22/22, exit 0 | — |
| navigation fence, `REV=e1d81d4` | 22/22 | 22/22, exit 0 | match |
| navigation fence, no REV (default bb08dd57) | 8/22 (SCORECARD) | 8/22, exit 1 | match |
| `covers:` count | 0 | 0 | — |
| `--regression` (committed gate) | PASS expected | PASS, PIN dc7c4141 match | match |

- The fence block extracted from `git show a6528e6:SCORECARD.md` hashes to `8b59b503…`, as pre-registered.
- The harness path in W resolves to `kaika/tameshi-shokunin`, which I symlinked from `/tmp`. Its sha is `75ed934d…`, identical to the canonical copy, and differs from the recorded `b56c6e57…`. That difference is provenance-only per the gate's own rule.
- Live layer not re-run, to avoid omarchy git verbs.

**In-flight worktree (labelled, not committed):** `tools/mado-verify.sh` is modified (PIN re-cut to `d41a884b…`, gkeep added to EXPECT and `LOCAL+=(gkeep)`). `--no-live` reads CLEAN 29/0, `--regression` PASS at the new pin, `--selftest` 268/268. QUALITY numerator is 11/16. Those readings are not the pre-registered baseline.

## (2)–(4) Findings

**F1 — BLOCKER — C2's re-anchor is blessing drift as pre-registered.**
- Evidence: `gate-standing-use.md:34-38` (§0.3) and `:222-226` (§5.4) say pins are never edited to match reality. The response to a MOVED pin is re-verification plus an appended erratum.
- `omarchy-drift-watch.md:284-287` governs "constants in §6, table in §2" of that note. It does not govern gate EXPECT (`tools/mado-verify.sh:2190-2207`) or LOCAL (`:2249`). The pre-reg cites the wrong instrument's protocol.
- Target 0 is reached only by editing the expectation. The freshness score then reads 10 while `SKILL.md:40-46` still says 17 sources / 29 L / last include `ai-usage` (state dossier §3.4). `hypr.file.sha_pin` NOTE stays open, and the rubric excludes NOTE rows.
- In-flight, gkeep (operator-owned, no fleet owner per state §3.5) is absorbed into mado's owned LOCAL inventory. That is an adjacency harm.
- Legitimate only if all of the following hold:
  - (a) the before-FAIL line is quoted (`before-no-live.txt`, already done);
  - (b) an erratum is appended in a corpus note, naming 17→18, 12→13, both sha values, the reason and the re-measure command, not only as a code comment;
  - (c) the new expectation is the named token `source = ~/.config/hypr/gkeep.conf` with its sha, not a count;
  - (d) the operator's intent to keep gkeep is on record; mado cannot self-attest;
  - (e) gkeep is not added to LOCAL;
  - (f) PIN/TABLE are re-cut via `REGRESSION_RECUT` from the measured table, with TABLE unchanged;
  - (g) freshness is scored separately, with the SKILL.md:40-46 erratum landed before any freshness score is claimed.
- If any condition fails, record C2 as "FAIL → re-anchor owed" (the state dossier's C1′ fallback), not freshness 1→0.

**F2 — MAJOR — C2's freshness rubric measures gate agreement, not claim freshness.** It is `10×PASS/(PASS+FAIL+UNKNOWN)` over file-plane rows. NOTE and SKIP rows are excluded, so the open `sha_pin` NOTE is invisible. AXES.md's freshness definition is "skill claims re-verified against live surfaces". Fix: add a claim-level sub-rubric (present-tense SKILL claims contradicted by live = 0).

**F3 — MAJOR — freshness rubric silently swapped.** State dossier §2.1/§2.4 lists freshness(a) = 3/22 = 1.3636, the `verified-at` observable that LEARNING.md's quality trend uses. The pre-reg substitutes gate-plane (b) = 9.6552 with no recorded rejection. Calibration (0) is still lowest under (a), so claim selection survives, but the freshness score misreports. Fix: record both candidates and the reason for the choice.

**F4 — MAJOR — "calibration is the lowest non-retired axis by the lane's own record" is not established.**
- The lane's own record never scored calibration. SCORECARD fleet-round-1 lists it as `unprovable-but-better`.
- Calibration's 0.0000 comes from a rubric written this round against a 5-line QUALITY.md.
- The pre-reg's own table shows a tie at 0.0000 (coverage/sourced-art), which the text does not mention.
- State dossier §2.4 called the lowest axis "indeterminate" and recommended freshness.
- The obligation is met under the tie, but the stated rationale is false. Fix: state the tie and the rule, and cite the §2.4 disagreement.

**F5 — MAJOR — C1 rubric is vacuously satisfiable, and target and rubric disagree.**
- `grep -cE '^[0-9]+\. .*lessons/'` counts any criterion line containing `lessons/`. Fixture `/tmp/mado-r12-reviewer/fixture/QUALITY.md` with `lessons/does-not-exist.md` gives numerator 1.
- Target "≥5 cited" is a count. The rubric is 10×cited/criteria. Adding 5 cited rows to the existing 5 uncited gives 5.0000, not a saturation target. The pre-reg never defines the target score.
- Citations are self-authored, with no non-author check. In-flight, 11/16 criteria cite the lane's own `lessons/round-12.md#mistakes`.
- Fix: count only criteria whose cited path resolves at the round commit, and state the target as a score. Record a non-author spot-check (≥1 admit, ≥1 reject) in `lessons/round-12.md ## Gate`.

**F6 — MAJOR — C3's `covers:` count is vacuous.** The pre-reg sums two separate commands: sourced entries + `covers:` lines. It does not intersect them.
- Fixture: `a.md` (no source, `covers: U1`), `b.md` (no source, `covers: U1`), `c.md` (no source, `covers: U1, U2`).
- Result: sourced entries 0, `covers` sum 3, distinct covered items 2. The rubric should read 0/7; the commands print 3.
- The S-id regex also matches leads, and no `mined` status is checked. SOURCES-CONTRACT-v1 rule 4 requires a `mined` row on uncovered ground.
- Fix: one per-file predicate: head-15 `source:` cites a `mined` row in `corpus/SOURCES.md` whose `used-by` names the file, AND `covers: U<k>`. Count distinct k. Run the contract census (SOURCES-CONTRACT-v1 lines 64–80) and require empty output for the uniq-d and mined-used-by checks.

**F7 — MAJOR — depth and adjacency declared unscored is non-compliant with AXES.md:75-83.** The axes row requires a score 0–10 with evidence, or an `unprovable-but-better` verdict with a named non-author reviewer. Retirement requires justification (line 83). The pre-reg's basis is state §2.4's "declare unscored", which is not in AXES.md. Fix: retire each with justification, or give a verdict. A measurable adjacency rubric exists: count of sibling- or operator-owned paths absorbed into gate inventories (committed 0; in-flight 1, gkeep).

**F8 — MAJOR — the navigation-counter harm watch fails as pre-registered.**
- The four new notes (`config-drift-r12`, `window-rule-effects-getprop`, `hyprland-config-era-r12`, `xdg-portal-routing-r12`) need `corpus/README.md` rows of the form `` | `knowledge/<name>.md` ``.
- The fence reads `ls-tree rev:corpus/knowledge` against README rows. Any unindexed note gives missing ≥1 and exit 1.
- Committed README indexes 22/22 today; the pre-reg says nothing about rows.
- Fix: add rows and the Frontier bullet update in the same commit. Add the acceptance `REV=<round commit>` → 26/26, exit 0.

**F9 — MAJOR — U1's grounding cites a negative claim contradicted at help level.**
- `arc-synthesis.md:300` says "no rule-read verb in Hyprland 0.56". `config-health-report-r3.md:449` and `:997` repeat it.
- Host `hyprctl --help` line 51 reads `getprop ... → Gets a window property`. Verified read-only.
- `keybind-rule-semantics.md:206-210` already tabulates documented rule effects `[INF-docs]`, so U1's real gap is measured effects. The pre-reg does not say so.
- Fence rules forbid editing existing notes. The correction belongs in the new entry's `## Rejected` section and the round lesson, as a `supersedes` row (SOURCES rule 2).

**F10 — MINOR — U-list tags and boundaries.**
- U3–U6 come from one `[INFERENCE]` bullet (`mado-art.md:8`). The pre-reg does not carry the tag.
- U2 is partly covered (`keybind-rule-semantics.md:31`, `:291`; `SKILL.md:344`).
- U3 host portal inventory exists (`remaining-planes-census.md:227-233`; `hyprland-config-plane.md:167`).
- Fix: tag them, and state the boundary between host inventory and upstream routing/lifecycle.
- Line anchors otherwise check out: `arc-synthesis.md` §6 rows, `SKILL.md:344`, `mado-art.md:5-24`.

**F11 — MAJOR — no non-author spot-check is named.** `LEARNING.md:38-43` requires one each round. C1 is a discernment claim, and its verdict cannot be recorded without it. Fix: name the reviewer seat and the sample before admission.

**F12 — MINOR — baseline provenance.**
- `before.txt` header says "tree clean: [1 dirty paths]", with the path unnamed. The baseline was taken on the worktree, not committed bytes. My committed-bytes rerun reproduces every value, so there is no numeric impact.
- Count lines `3` and `22` are unlabelled.
- `.ufo/evidence/round-12/gate-regression-before.txt` is untracked, so the regression baseline is not durable evidence.

**F13 — MINOR — harness provenance.** `gate-standing-use.md` §5.5 says the harness is `cf41efaa…` "today". Current is `75ed934d…`. The round record should pin `MADO_VERIFY_HARNESS` explicitly, because the default from W resolves to a sibling worktree.

**F14 — MINOR — not blind.** The rubrics and baselines were already in the state dossier (§2.1, §2.4, §6) about a minute before commit (`before.txt` 18:42:56, commit 18:43:51 local). The claim numbering also differs from the state dossier (state C1=freshness, C2=coverage, C3=calibration). Disclose both.

## Compliant checks
- `e1d81d4` is the parent of `a6528e6`. HEAD of `kaika/round` is `a6528e6`, with no later commits. The commit touches only SCORECARD.md and five evidence files.
- All round-12 content in the worktree (`tools/mado-verify.sh`, fragments, lesson, SKILL/QUALITY edits, new notes) is dated 19:07 or later, after the commit. `.ufo/round-12/` was created empty at 18:42:36, before the commit.
- Pre-reg line anchors resolve at committed bytes: EXPECT `:2190`, LOCAL `:2249`, PIN_MADO `:1290`, TABLE_MADO `:1293`, MADO_R7_FLEET `:1295`, harness default `:1505`.

**Verification gaps:** the live layer was not re-run. Worktree readings are in-flight and not the pre-registered baseline. The sources fragments and the new notes were not reviewed. The sibling seat's in-flight diff may change again before the round commit.
