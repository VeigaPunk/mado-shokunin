# mado — round 18 report (hyaku phase 2, attempt <L1>)

Lane HEAD (pushed): `abfbf35b1ed4d4a1eb294d525ef286be30f3886f` (receipts commit; results at `4c103b55b1ea5c3c555884afe3eb69b5189701b7`, the wave-1 integration commit; `abfbf35` descends from it, `git merge-base --is-ancestor` checked). Tool sha landed: `tools/mado-tripwire.py` `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb`; `tools/mado-verify.sh` `c9fb0cef3e081dc878d69f8e20c148429bdfbdce949f8afaed705db957ea42b5` (`.ufo/waves/round-18/evidence/harm-tripwire-round-18-frozen.txt`, `harm-gate-selftest.txt`). Baseline `d9a5a18` (lane branch master). Pre-registration `d3a0000` (SCORECARD.md tail "Round 18 — declared claims"). Admission is **not** asserted here; independent non-author closure and operator disposition remain required. <L1>.

Placeholder convention: every `<…>` is a value a later seat or L1 must fill from an observed command, commit, or receipt. Unfilled `<…>` at yield is a defect. Declared inputs (baseline, pre-registration, claim IDs, targets) are named from SCORECARD; no outcome is pre-filled.

Scribe note: the receipts named below are committed at `abfbf35` unless marked `(4c103b5)`. `abfbf35` changes only `.ufo/waves/round-18/{evidence,w1,fetch,frozen,tripwire}` and the fetch-verify and recut helpers; corpus and gate files are committed at `4c103b5` (ancestor of `abfbf35`). Fetch bodies are on disk but not tracked (`git ls-files` returns receipt lines only).

## Work performed

Declared claims (SCORECARD.md § "Round 18 — declared claims"; corrections § <L1>):

- **C1 calibration** (lowest scored axis at declaration). Before: QUALITY lesson-citation fraction 15/23 = 6.5217 (`.ufo/waves/round-18/evidence/measure-before.json.txt`, `python3 .ufo/waves/round-17/measure.py d9a5a18`, c1). After: 18/26 = 6.9231 (`.ufo/waves/round-18/evidence/measure-after.json.txt`, c1 `criteria: 26`, `lesson_cited: 18`). Target ≥18/26 met on the literal counter. Result: met on literal counter; semantic counter, criteria 24-26 wording and falsification status <L1>.
- **C2 coverage** (rubric V, unchanged instrument `de4c422b…`). Before: 4/6 = 6.6667 (P1, P2, P4, P6). After: 6/6 = 10.0 (`measure-after.json.txt`, c2): P3 via `corpus/knowledge/walker-route-r18.md` (`surface: P3`; credited S072–S091, of which S090, S091 are host rows) and P5 via `corpus/knowledge/theme-route-r18.md` (`surface: P5`; credited S092–S095, of which S095 is a host row). Host-row credit has no fetch receipt (file bytes, `sha256sum`). Result: met on the instrument; behaviour not observed (`[UNK]` rows in both notes, § Unexercised behavior). Result: <L1> for the verdict.
- **C3 operability — capability acquisition** (R17-V4). `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen`: `frozen_match`, exit 0 (`evidence/tripwire-frozen-match.txt`, tool `c87a31ef…` measured at `4c103b5`). Tampered copy (one byte appended to `inputs/r15-libinput-events.jsonl`): `snapshot_tampered`, exit 2 (`evidence/tripwire-frozen-tampered.txt`). `d9a5a18` tool: usage, exit 2 (`evidence/tripwire-frozen-before.txt`, tool `962919ce…`). Frozen selftest 17/17, exit 0 (`evidence/harm-tripwire-round-18-frozen.txt`). Registry row `mado-tripwire-frozen` | gate (`SKILL.md` at `4c103b5`, line 566). Result: met; detection after the fact only.
- **Routed jj-migration fixes** (not claims; harm-watched). `tools/mado-verify.sh` (`4c103b5`): producer rc captured inside the substitution; old gate `fba82a66…` `git show` rc=128 → `FAIL` with `e3b0c44298fc…` (`evidence/gate-rc-redbefore.txt` §1, `4c103b5`); new gate rc=128 → `UNKNOWN` on all three rows (§3). Selftest `389/389`, exit 0 (`evidence/gate-selftest.txt`, `evidence/harm-gate-selftest.txt`). PIN re-cut `cd1d73d7…` → `20714096…` (`evidence/regression-recut.txt` §1, §3, §4): 10/10 KILLED, `MADO_REGRESSION: PASS` in §4. Scribe re-derivation: `sed` excision of the three MADO-R7/R8 marker blocks on the committed `4c103b5` gate yields `20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744`, matching the pin. `.gitignore` `.ufo/state/` and `__pycache__/` (`4c103b5`). Result: <L1> for the JJ-F10 status.

Routed defect disposition (R17-V1..V5; source `corpus/lessons/round-17-verifier-spotcheck.md` §6). Status vocabulary: `closed` (fix plus runnable failing control committed), `partial`, `open`.

| ID | Routed defect (one line) | Disposition this round | Evidence (path, commit) | Status |
|---|---|---|---|---|
| R17-V1 | Tripwire scan receipts `tripwire-r13..r16.txt`, `tripwire-anchor-r15.txt`, `tripwire-pacmanlog-join.txt` carry no tool sha256 or `measured_commit`; `lessons/round-17.md` claims a re-cut under `962919ce…` that git never recorded | Five scan receipts re-cut with `RECEIPT … tool_sha256=c87a31ef… measured_commit=4c103b5…` as line 1; counts, files and findings identical to round-17 (`recut-summary.json`, `all_receipts_identical: true`). The join file is **not** re-cut: its line 1 is a `#` comment, the `RECEIPT` form is absent, and its body is a hand-assembled join (sha `be361650…` recorded in `recut-summary.json` `pacmanlog_join`). | `.ufo/waves/round-18/evidence/tripwire-r13.txt`:1, `tripwire-r14.txt`:1, `tripwire-r15.txt`:1, `tripwire-r16.txt`:1, `tripwire-anchor-r15.txt`:1, `recut-summary.json`, `tripwire-pacmanlog-join.txt`:1 (`abfbf35`) | `partial` |
| R17-V2 | Round-17 before→after table cites tool sha `7a98720e…` (the `f71ccbe` tool), not landed `962919ce…` | Both shas cited with labels in the round-18 lesson erratum: `corpus/lessons/round-17.md:198-199` (`4c103b5`). Round-17 report `.ufo/reports/round-17/mado.md` not re-read here. | `corpus/lessons/round-17.md:198-199` (`4c103b5`) | <L1> |
| R17-V3 | Rubric V cannot tell a fetched row from an invented one; new credited rows need raw fetch receipts (sha256, bytes, fetch time) | 301 `mado-fetch-receipt-v1` lines in 21 tracked seat directories (`fetch/<Seat>/receipts.jsonl`). Re-hash on disk: 301/301 bodies match `sha256` and `bytes` (scribe re-check; bodies untracked). Not committed: `fetch/ReopenS072/receipts.jsonl` (2 lines), `fetch/MadoR18.ReopenS081/receipts.jsonl` (2 lines); `fetch/MadoR18.RevengeTarballRepro/` holds tarball and HTML artifacts with no receipt. 5 receipts record HTTP 404 and no SOURCES row cites them. S084 (docs.rs `latest` HTML) is admitted despite the round-18 gate text (`lessons/round-18.md` § Gate). | `.ufo/waves/round-18/fetch/*/receipts.jsonl` (`abfbf35`); `fetch/ReopenS072`, `fetch/MadoR18.ReopenS081` (untracked); `corpus/SOURCES.md` S084 (`4c103b5`) | `partial` |
| R17-V4 | Tripwire is a probe with no frozen input snapshot; inputs live under mutable `~/.omp/agent/sessions`, pinned only by `session-index.json` | `--frozen` replay over five committed inputs; `frozen/provenance.json` names `tool_receipt_sha256 962919ce…` and `session-index.json`; tampered-input and missing-input cases in the frozen selftest (17/17). | `.ufo/waves/round-18/frozen/provenance.json`, `frozen/inputs/*.jsonl`, `evidence/tripwire-frozen-match.txt`, `evidence/tripwire-frozen-tampered.txt`, `evidence/harm-tripwire-round-18-frozen.txt` (`abfbf35`) | `closed` (proposed; <L1> confirms) |
| R17-V5 | M3 instrument tightenings shown to bite only in a seat `/tmp` lab (`lessons/round-17.md:156-158`); no committed mutant receipt for `measure.py` | Six tightenings: each mutant credited by loose instrument `f52f43f8…` (sha `a280b3ab…`) and rejected by tight instrument `d9a5a18` (sha `de4c422b…`). `summary`: mutants 6, bites 6, `no_bite []`, `expectations_met 6`, `baselines_agree true`. Harness `.ufo/waves/round-18/measure-mutants.py` sha `075815bd…`. Mutant repos are under `/tmp/mado-r18-mutants-run` (kept by `--keep`, not committed). | `.ufo/waves/round-18/evidence/measure-mutants.json` (`4c103b5`) | `closed` (proposed; mutant repos ephemeral; <L1>) |

Stale-lane: <L1> (driver mode, other open missions, round-18 start state, inherited dirty or clean tree at dispatch, files read and left unedited).

Tool installs: <L1> — no install or update record appears in the committed receipts at `abfbf35`; L1 confirms against the lane log.

jj notes: <L1> — lane is jj-colocated. The scribe seat issued read-only git only (`log`, `show`, `ls-tree`, `ls-files`, `rev-parse`, `diff`, `merge-base`, `check-ignore`) and no jj command. The `.gitignore` effect (`.ufo/state/`, `__pycache__/`) is visible at `4c103b5`. Seat-level read-only git and misroot use are <L1>.

Host and fetch (file reads only): walker `2.17.2-1` (`/var/log/pacman.log:2929`, `2026-10-20T09:16:46-0300`; prior `2.17.0-1` at `:1943`), elephant `2.22.1-1` (`:3095`, `2026-10-20T09:31:03-0300`), omarchy checkout tag `v3.8.4` (`corpus/knowledge/theme-route-r18.md`, "Tag selection": `refs/tags/v3.8.4` and `ORIG_HEAD` both name `8fcc9d60…`; checkout `.git` file bytes not separately re-read here). Fetch receipt count `301` committed across `21` seat directories (plus 4 untracked receipt lines in `ReopenS072` and `MadoR18.ReopenS081`). Walker and elephant versions are log lines, not running-binary facts (S090 caveat).

## Landed changes

All on the mado remote (`git -C mado-shokunin log d9a5a18..abfbf35`, all `mado-shokunin <mado@shokunin.local>`); LOG.md § <L1>.

| Commit | Change |
|---|---|
| `d3a0000` | pre-registration (declared claims, SCORECARD tail) — baseline for this round's diffs |
| `4c103b5` | wave-1 integration (single commit; per-change split <L1>): frozen tripwire gate entry, gate rc fix and PIN re-cut, P3/P5 routes and S072–S095, QUALITY 24–26, `lessons/round-18.md`, round-17 erratum, registry rows, round-18 evidence |
| `abfbf35` | receipts at `4c103b5`: measure before/after, tripwire re-cut r13–r16 and anchor with producer header, frozen match/tampered/before, harm watch PASS |

Tooling landed: `tools/mado-tripwire.py` `--frozen` mode (`4c103b5`), `tools/mado-verify.sh` rc capture (`4c103b5`), `.gitignore` `.ufo/state/` (`4c103b5`). Each row above is cited from `git log` output, not from a seat's report.

## Before → after measurements

| Claim | Counting command | Before (declared, `d9a5a18` / `d3a0000`) | After (`abfbf35` / `4c103b5`) |
|---|---|---|---|
| C1 | `git show REV:corpus/QUALITY.md \| grep -cE '^[0-9]+\. .*lessons/'` over `grep -cE '^[0-9]+\. '`; also `python3 .ufo/waves/round-17/measure.py REV` key c1 | 15/23 = 6.5217 | 18/26 = 6.9231 (`measure-after.json.txt`; `grep -cE` values <L1>) |
| C2 | `python3 .ufo/waves/round-17/measure.py REV` (sha256 `de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc`, receipt `measure-before.json.txt` / `measure-after.json.txt`) | 4/6 = 6.6667 (P1, P2, P4, P6) | 6/6 = 10.0 (P3 walker-route-r18.md, P5 theme-route-r18.md) |
| C3 | `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen`; `--selftest` on round-17 suites `core` 9, `compound` 16, `hardening` 33, `w2-regressions` 30 | probe only (`--frozen` usage, exit 2, `tripwire-frozen-before.txt`) | `frozen_match` exit 0; tampered `snapshot_tampered` exit 2; frozen selftest 17/17; round-17 suites 9/9, 16/16, 33/33, 30/30 (`harm-tripwire-round-17-*.txt`); tool sha `c87a31ef…` |
| R17-V1/V2 | `sha256sum tools/mado-tripwire.py`; `git log -1 --format=%H -- tools/mado-tripwire.py` | receipts without tool sha or measured revision (lesson M1) | receipts line 1 carries `tool_sha256=c87a31ef…`, `measured_commit=4c103b55…`; `git log -1` for `tools/mado-tripwire.py` = `4c103b5` |
| JJ-F10 | `tools/mado-verify.sh` failing-git-stub scenario (producer rc non-zero must not yield `e3b0c442…`) | old gate: `FAIL`, `HEAD blob e3b0c44298fc…` (`gate-rc-redbefore.txt` §1) | new gate: `UNKNOWN … (rc=128)` on all three rows (§3); OM9/OM10 inside selftest 389/389 |

Separability (reverting each claim commit moves only its own counter): <L1> — no committed separability receipt; the seat report `w1/reports/RevSeparability18.md` is a seat claim, not a receipt.

Harm watch (legacy hermetic selftest, classifier selftest, U-routes, navigation, census): **PASS** (`evidence/harm-watch-summary.txt`, rev `4c103b5`, 10 commands, all `OK exit=0`). Legacy gate selftest `389/389` (`harm-gate-selftest.txt`); tripwire round-17 core 9/9, compound 16/16, hardening 33/33, w2-regressions 30/30; frozen 17/17; U-route `count 7`, `score 10.0` (`harm-measure-u.txt`); navigation `indexed=34/34 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` (`harm-nav-fleet-round-1.txt`); census validate exit 0 (`harm-census-validate.txt`).

Freshness: <L1> (not re-measured in any committed receipt).

## Sources & frontier

SOURCES rows 71 → 95 (`git show 4c103b5:corpus/SOURCES.md`, `awk -F'|' '$2~/^ *S[0-9]{3} *$/'`). Tier and state breakdown: tier A 64 → 88, tier B 1, tier C 6; mined 56 → 80, queued 8, rejected 7. Reserved ids S072–S099; assigned ids S072–S095 (24 rows, S096–S099 unused). Rows touched old→new: none (`git diff d9a5a18 4c103b5 -- corpus/SOURCES.md`: 0 removed `| S0` lines, 24 added). Same-round corrections: <L1>.

Route notes (first-15-lines check: `source:` cites mined tier-A rows whose used-by names the note; `surface: P<n>` line; four required sections each ≥3 non-blank lines, `[UNK]` inside the last):

| Note | `surface` | Credited S-rows (raw fetch receipt path) | Section check | Status |
|---|---|---|---|---|
| `corpus/knowledge/walker-route-r18.md` | P3 | S072–S089 (web; receipts in `fetch/NoteWalker/receipts.jsonl` plus `fetch/MadoR18.SrcWalkerThemes`, `fetch/SrcWalkerReadme`, `fetch/SrcWalkerChangelog`, `fetch/SrcWalkerDefaultConfig`, `fetch/SrcWalkerDocsSite`, `fetch/SrcWalkerConfigPaths`, `fetch/SrcElephantReadme`, `fetch/SrcElephantProviders`, `fetch/SrcOmarchyWalker`, `fetch/SrcOmarchyBackground`; S084 receipt is `fetch/NoteWalker/xdg-crate-basedirectories.html`); S090 (host, `/var/log/pacman.log:2929,3095`, no fetch receipt); S091 (host file bytes, no fetch receipt; web-receipted sha matches omarchy/walker config bodies) | Upstream contract 115 non-blank; Host declaration 73; Safe observation 20; Unexercised behavior 37 with `[UNK]` at lines 285–297 | <L1> (S084 gate question) |
| `corpus/knowledge/theme-route-r18.md` | P5 | S092 (`fetch/MadoR18.SrcSwaybgMan/receipts.jsonl`, `fetch/NoteTheme/receipts.jsonl`); S093 (`fetch/NoteTheme/receipts.jsonl`, `fetch/SrcOmarchyThemeSet`, `fetch/SrcOmarchyThemeLayout`, `fetch/SrcOmarchyThemeHooks`, `fetch/SrcOmarchyBackground`); S094 (`fetch/NoteTheme/receipts.jsonl`); S095 (host file bytes, no fetch receipt) | Upstream contract 22; Host declaration 34; Safe observation 6; Unexercised behavior 10 with `[UNK]` at lines 136–140 | <L1> |

Census start (`evidence/census-start.txt`, `4c103b5`) and end (`evidence/census-end.txt`, **absent** at `abfbf35`; nearest committed receipt is `evidence/harm-census-validate.txt`, a `validate` run):

```text
$ scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
exit=0
```

Frontier advanced: <L1> (README § Frontier). Still open: <L1>. Sourced claims rest on rows opened this round: S072–S095 (receipted web rows S072–S089, S092–S094; host rows S090, S091, S095). Mined mistakes: `lessons/round-18.md` § Mistakes M1–M6, each with a runnable check shown able to fail (<L1> for the failing-control mapping; M2 `measure-mutants.json` 6/6 bites; M3 `gate-rc-redbefore.txt` §1 red before green after).

## Trend verdicts

- **Expansion: <L1>.** P3 and P5 routes present, rubric V 6/6 on the instrument (`measure-after.json.txt`). Not behaviour coverage: both notes list `[UNK]` observations (§ Unexercised behavior). Behaviour note: <L1>.
- **Quality: <L1>.** QUALITY criteria 24–26 (c1 18/26), failing controls M2 and M3, frozen replay 17/17, five re-cut scan receipts (`recut-summary.json`). Open debt: join file not re-cut (R17-V1 `partial`); 4 untracked fetch receipt lines; S084 gate conformance; regression receipt names gate `2bdf5e8a…` while the committed gate is `c9fb0cef…` (derived target unchanged, see § Routed fixes); no round-17 or round-18 transcript scan (see Seat conduct). <L1>.
- **Discernment: <L1>.** Findings by lane seats versus non-author checks; non-author agreement <L1>.

## SHONEN

- [`<L1>`] SKILL.md contains real decision tables, error patterns, checklists, cited sources — evidence: registry row `mado-tripwire-frozen` | gate, `SKILL.md` line 566 (`4c103b5`); non-author verifier <L1>.
- [`<L1>`] At least one end-to-end domain task executed and logged in LOG.md — evidence: <L1> (round 18 desktop task present or absent; host pause status <L1>).
- [`<L1>`] Instructions executable by an agent without oral context — evidence: <L1>; lane-dispatched seats are not outside verifiers.
- [`<L1>`] No cross-domain bleed (PROVINCE.md still accurate) — evidence: <L1>.

Each box is `[ ]`, `[~]`, or `[x]`. `[x]` requires a non-author check named in the evidence cell.

## Waves, seats, dead seats, misroots, L0

- Wave 1 (`mado-r18-w1`): <L1> seats — role mix <L1>. Dead: <L1>.
- Wave 2: <L1> seats — role mix <L1>. Dead: <L1>.
- Round total: <L1> seats (limit ≤200); job-cap refusal <L1>.
- Misroot sweep: <L1> (`git -C /home/vgpnk/Projects/shokunin status --porcelain` is not run by this seat).
- Seat conduct (C3 over round-18 transcripts): **not scanned in committed receipts.** The `tripwire-r13..r16` receipts list `MadoR13.*`–`MadoR16.*` transcripts only (line 2); no `MadoR17.*` or `MadoR18.*` file appears. Unparsed spawns in committed receipts (R13–R16 only): r13 5, r14 8, r15 8, r16 12. Unparsed spawns for round 18: <L1>; `clean` meaning <L1>.
- Host (file read of `/var/log/pacman.log` only): round window `20T00–06` (-0300) per `tripwire-pacmanlog-join.txt` (`awk '/^\[2026-10-(19T2|20T0[0-6])/ …'`). That window excludes 13 `[PACMAN] Running` transactions dated `2026-10-20T07:45:36-0300`–`09:39:21-0300` (`pacman.log:2440, 2448, 2454, 2461, 2462, 3064, 3085, 3091, 3092, 3125, 3126, 3132, 3152`, including `pacman -Syu` at `2462`, `09:15:30`). Attribution of these runs to any lane seat: <L1> (no committed transcript scan covers them). Earlier runs: `pacman.log:2404` (`2026-10-19T21:02:21`, gitleaks), `:2410` (joined to `MadoR13.GlobalCapture`), `:2416` (`man-pages`, unmatched in the join).
- jj: <L1> (cross-reference "Tool installs" and "jj notes" above).
- L0: <L1>. Existing host-recovery lines `.ufo/l0-questions.md` L54/L55 (R15-V1 operator-owned, current state <L1>). New questions: <L1>.
