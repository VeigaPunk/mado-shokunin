# mado — round 18 report (hyaku phase 2, attempt <ATTEMPT>)

Lane HEAD (pushed): `<LANE_HEAD_SHA>` (results at `<RESULTS_SHA>`; tool sha `<TOOL_SHA_LANDED>…`). Baseline `d9a5a18` (lane branch master). Pre-registration `d3a0000` (SCORECARD.md tail "Round 18 — declared claims"). Admission is **not** asserted here; independent non-author closure and operator disposition remain required. `<ADMISSION_NOTE>`.

Placeholder convention: every `<…>` is a value a later seat or L1 must fill from an observed command, commit, or receipt. Unfilled `<…>` at yield is a defect. Declared inputs (baseline, pre-registration, claim IDs, targets) are named from SCORECARD; no outcome is pre-filled.

## Work performed

Declared claims (SCORECARD.md § "Round 18 — declared claims", corrections § `<CORRECTIONS_SECTION>`):

- **C1 calibration** (lowest scored axis at declaration). Declared before-state: QUALITY lesson-citation fraction 15/23 = 6.5217 (`python3 .ufo/waves/round-17/measure.py REV`, key c1). Target ≥18/26 via append-only QUALITY criteria 24-26 and lesson round-18 Mistakes rows. Result: `<C1_RESULT>`.
- **C2 coverage** (rubric V unchanged; PROVINCE surfaces P1 Hyprland, P2 Waybar, P3 Walker, P4 terminals, P5 themes/wallpapers, P6 idle/lock). Declared before-state: 4/6, P3 and P5 open. Two new documentary route notes: `corpus/knowledge/walker-route-r18.md` (`surface: P3`) and `corpus/knowledge/theme-route-r18.md` (`surface: P5`). Result: `<C2_RESULT>`.
- **C3 operability — capability acquisition** (R17-V4). `python3 -I tools/mado-tripwire.py --frozen <DIR>`: digest-pinned frozen replay over a committed snapshot of real incident transcript lines; registry row probe → gate. Result: `<C3_RESULT>`.
- **Routed jj-migration fixes** (not claims; harm-watched): `tools/mado-verify.sh:3406` producer rc capture with failing git-stub scenario (JjAuditMado F10); measured PIN_MADO re-cut; `.ufo/state/` into `.gitignore` (L1). Result: `<JJ_FIX_RESULT>`.

Routed defect disposition (R17-V1..V5; source `corpus/lessons/round-17-verifier-spotcheck.md` §6). Status vocabulary: `closed` (fix plus runnable failing control committed), `partial`, `open`.

| ID | Routed defect (one line) | Disposition this round | Evidence (path, commit) | Status |
|---|---|---|---|---|
| R17-V1 | Tripwire scan receipts `tripwire-r13..r16.txt`, `tripwire-anchor-r15.txt`, `tripwire-pacmanlog-join.txt` carry no tool sha256 or `measured_commit`; `lessons/round-17.md` claims a re-cut under `962919ce…` that git never recorded | `<V1_DISPOSITION>` | `<V1_EVIDENCE>` | `<V1_STATUS>` |
| R17-V2 | Round-17 before→after table cites tool sha `7a98720e…` (the `f71ccbe` tool), not landed `962919ce…` | `<V2_DISPOSITION>` (both shas cited with labels) | `<V2_EVIDENCE>` | `<V2_STATUS>` |
| R17-V3 | Rubric V cannot tell a fetched row from an invented one; new credited rows need raw fetch receipts (sha256, bytes, fetch time) | `<V3_DISPOSITION>` (`fetch/<Seat>/receipts.jsonl`) | `<V3_EVIDENCE>` | `<V3_STATUS>` |
| R17-V4 | Tripwire is a probe with no frozen input snapshot; inputs live under mutable `~/.omp/agent/sessions`, pinned only by `session-index.json` | `<V4_DISPOSITION>` (`--frozen` replay, `frozen-tripwire/provenance.json`) | `<V4_EVIDENCE>` | `<V4_STATUS>` |
| R17-V5 | M3 instrument tightenings shown to bite only in a seat `/tmp` lab (`lessons/round-17.md:156-158`); no committed mutant receipt for `measure.py` | `<V5_DISPOSITION>` | `<V5_EVIDENCE>` | `<V5_STATUS>` |

Stale-lane: `<STALE_LANE_LINE>` (driver mode, other open missions, round-18 start state, inherited dirty or clean tree at dispatch, files read and left unedited).

Tool installs: `<TOOL_INSTALLS>` — one line per install or update: tool, version, channel (`uv tool` / `npx` / `~/.local/bin` release binary / `cargo` / `npm -g`), reason. If none: `none (<ROLE_COUNT> reporting seats)`. Host pacman transactions remain PAUSED (orchestrator ruling 2026-10-20); no pacman, yay, paru, or sudo invocation is recorded here unless `<PAUSE_STATUS>` says the pause lifted.

jj notes: `<JJ_NOTES>` — lane is jj-colocated; state which seats used read-only git only, that no jj command was issued, and any `.ufo/state/` or `.gitignore` effect observed by file read.

Host and fetch (file reads only): `<HOST_FILE_READ_NOTES>` — walker `<WALKER_VERSION>` (`/var/log/pacman.log:<LINE>`), elephant `<ELEPHANT_VERSION>` (`:<LINE>`), omarchy checkout `<OMARCHY_TAG>` (`.git` file bytes); fetch receipt count `<FETCH_RECEIPT_COUNT>` across `<FETCH_SEAT_COUNT>` seats.

## Landed changes

All on the mado remote (`git -C mado-shokunin log d9a5a18..<RESULTS_SHA>`, all `mado-shokunin <mado@shokunin.local>`); LOG.md § `<LOG_SECTION_HEADING>`.

| Commit | Change |
|---|---|
| `d3a0000` | pre-registration (declared claims, SCORECARD tail) — baseline for this round's diffs |
| `<COMMIT_SHA>` | `<CHANGE_SUMMARY>` |
| `<COMMIT_SHA>` | `<CHANGE_SUMMARY>` |

Tooling landed: `tools/mado-tripwire.py` `--frozen` mode (`<FROZEN_COMMIT>`), `tools/mado-verify.sh` rc capture (`<VERIFY_COMMIT>`), `.gitignore` `.ufo/state/` (`<GITIGNORE_COMMIT>`). Each row above is cited from `git log` output, not from a seat's report.

## Before → after measurements

| Claim | Counting command | Before (declared, `d9a5a18` / `d3a0000`) | After (`<RESULTS_SHA>`) |
|---|---|---|---|
| C1 | `git show REV:corpus/QUALITY.md \| grep -cE '^[0-9]+\. .*lessons/'` over `grep -cE '^[0-9]+\. '`; also `python3 .ufo/waves/round-17/measure.py REV` key c1 | 15/23 = 6.5217 | `<C1_AFTER>` (target ≥18/26) |
| C2 | `python3 .ufo/waves/round-17/measure.py REV` (sha256 `<MEASURE_SHA>`, run receipt `<MEASURE_RECEIPT>`) | 4/6 = 6.6667 (P1, P2, P4, P6) | `<C2_AFTER>` (P3, P5 open or closed) |
| C3 | `python3 -I tools/mado-tripwire.py --frozen <DIR>`; `--selftest` on round-17 suites `core` 9, `compound` 16, `hardening` 33, `w2-regressions` 30 | probe only (no frozen replay) | `<C3_AFTER>` (outcome line, exit, `tool_sha256`) |
| R17-V1/V2 | `sha256sum tools/mado-tripwire.py`; `git log -1 --format=%H -- tools/mado-tripwire.py` | `<V12_BEFORE>` | `<V12_AFTER>` |
| JJ-F10 | `tools/mado-verify.sh` failing-git-stub scenario (producer rc non-zero must not yield `e3b0c442…`) | `<JJF10_BEFORE>` | `<JJF10_AFTER>` |

Separability (reverting each claim commit moves only its own counter): `<SEPARABILITY_RESULT>`.
Harm watch (legacy hermetic selftest, classifier selftest, U-routes, navigation, census): `<HARM_WATCH_RESULT>`.
Freshness: `<FRESHNESS_RESULT>`.

## Sources & frontier

SOURCES rows `<SOURCES_BEFORE>` → `<SOURCES_AFTER>` (`awk -F'|' '$2~/^ *S[0-9]{3} *$/' corpus/SOURCES.md`). Tier and state breakdown: tier A `<TIER_A_COUNT>`, tier C `<TIER_C_COUNT>`; mined `<MINED_COUNT>`, rejected `<REJECTED_COUNT>`, queued `<QUEUED_COUNT>`. Reserved ids S072-S099 (L1 assigns; drafts carry `S0xx-pending`); assigned ids `<ASSIGNED_IDS>`. Rows touched old→new: `<ROWS_TOUCHED>`. Same-round corrections: `<SAME_ROUND_CORRECTIONS>`.

Route notes (first-15-lines check: `source:` cites mined tier-A rows whose used-by names the note; `surface: P<n>` line; four required sections each ≥3 non-blank lines, `[UNK]` inside the last):

| Note | `surface` | Credited S-rows (raw fetch receipt path) | Section check | Status |
|---|---|---|---|---|
| `corpus/knowledge/walker-route-r18.md` | P3 | `<WALKER_ROWS>` | `<WALKER_SECTIONS>` | `<WALKER_STATUS>` |
| `corpus/knowledge/theme-route-r18.md` | P5 | `<THEME_ROWS>` | `<THEME_SECTIONS>` | `<THEME_STATUS>` |

Census start (`evidence/census-start.txt`) and end (`evidence/census-end.txt`):

```text
$ <CENSUS_COMMAND>
<CENSUS_OUTPUT>
exit=<CENSUS_EXIT>
```

Frontier advanced: `<FRONTIER_MOVE>` (README § Frontier). Still open: `<FRONTIER_OPEN>`. Sourced claims rest on rows opened this round: `<ROWS_OPENED>`. Mined mistakes: `lessons/round-18.md` § Mistakes `<MISTAKE_ROWS>`, each with a runnable check shown able to fail (`<FAILING_CONTROLS>`).

## Trend verdicts

- **Expansion: `<EXPANSION_VERDICT>`.** `<EXPANSION_EVIDENCE>` (route notes, rubric V movement, new capability). Not behaviour coverage unless `<BEHAVIOUR_NOTE>`.
- **Quality: `<QUALITY_VERDICT>`.** `<QUALITY_EVIDENCE>` (QUALITY criteria 24-26, failing controls, frozen replay, fixed receipts). Open debt: `<QUALITY_DEBT>`.
- **Discernment: `<DISCERNMENT_VERDICT>`.** `<DISCERNMENT_EVIDENCE>` (findings by lane seats versus non-author checks; non-author agreement `<NON_AUTHOR_STATUS>`).

## SHONEN

- [`<S1>`] SKILL.md contains real decision tables, error patterns, checklists, cited sources — evidence: `<SHONEN_1_EVIDENCE>`; non-author verifier `<SHONEN_1_VERIFIER>`.
- [`<S2>`] At least one end-to-end domain task executed and logged in LOG.md — evidence: `<SHONEN_2_EVIDENCE>` (round 18 desktop task present or absent; host pause `<PAUSE_STATUS>`).
- [`<S3>`] Instructions executable by an agent without oral context — evidence: `<SHONEN_3_EVIDENCE>`; lane-dispatched seats are not outside verifiers.
- [`<S4>`] No cross-domain bleed (PROVINCE.md still accurate) — evidence: `<SHONEN_4_EVIDENCE>`.

Each box is `[ ]`, `[~]`, or `[x]`. `[x]` requires a non-author check named in the evidence cell.

## Waves, seats, dead seats, misroots, L0

- Wave 1 (`mado-r18-w1`): `<W1_COUNT>` seats — role mix `<W1_ROLE_MIX>`. Dead: `<W1_DEAD>`.
- Wave 2: `<W2_COUNT_OR_NONE>` seats — role mix `<W2_ROLE_MIX>`. Dead: `<W2_DEAD>`.
- Round total: `<TOTAL_SEATS>` seats (limit ≤200); job-cap refusal `<JOB_CAP_STATUS>`.
- Misroot sweep: `git -C /home/vgpnk/Projects/shokunin status --porcelain` (read-only) shows `<MISROOT_FLEET_STATUS>`; mado seat files at fleet root `<MISROOT_FILES>`; relative-path misroots `<MISROOT_RELATIVE>`.
- Seat conduct (C3 over round-18 transcripts): `<CONDUCT_RESULT>`; unparsed spawns `<UNPARSED_SPAWNS>` (`clean` meaning `<CLEAN_MEANING>`).
- Host (file read of `/var/log/pacman.log` only): round window `<PACMAN_WINDOW_RESULT>`; earlier unattributed runs `<PRIOR_RUNS_NOTE>`.
- jj: `<JJ_SEAT_NOTE>` (cross-reference "Tool installs" and "jj notes" above).
- L0: `<L0_LINES>`. Existing host-recovery lines `.ufo/l0-questions.md` L54/L55 (R15-V1 operator-owned, current state `<R15V1_STATE>`). New questions: `<NEW_L0_QUESTIONS>`.
