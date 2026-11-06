# R88MResidCritic — round 88 residual honesty attack

Seat: residual critic, r1, on the FROZEN and MEASURED bytes. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Revisions: base `24ba2a9ddac21c1211579231e6ee1d98963f9988`; freeze `9e36e3a3103349b939982e532feca443f02e660d`;
C1 tool `650e18bdf0ae404ec9a80874c4503ecf3237e8e6`; C2 tool `7d3074865a9f5acfa0f1c9c66b460e73d4031331`;
record tip `498855cb327cd4e3debfa9446ea38398c216dda1` (detached HEAD). Read-only; host reads limited to the mako
config chain; no credential material read; no installs.

## Verdicts (per claim)

| Object | Verdict | Reason |
|---|---|---|
| C1 coverage (capability) | **STANDS** | I reproduced every scored figure byte-for-byte at `650e18bd` and at `7d307486`: `correct=62 cases=62 mutants=22 killed=22 carried=22/22 controls 14/15/33/43 score=10.0000`, rc 0. All frozen digests match the declaration. |
| C2 containment (predicate at B) | **STANDS** | Reproduced at `7d307486`: `correct=26 cases=26 mutants=7 killed=7 base_tool_correct=11 refuse_all_includes_correct=14 score=10.0000`, rc 0. Host chain still resolves (§4). |
| C2 "Before" sentence (declaration) | **FALLS as written** | "the counter at the C1 content revision (no containment) → TARGET_MISSED" is contradicted by the committed `receipts/c2-before-A-r88.txt`: at `650e18bd` the counter is `SETUP_ERROR … forgery anchor … occurs 0 times`, rc 2. No verdict exists at A. |
| Freeze ordering | **STANDS** (graph) / **WEAKENED** (as a `%ad` test) | F is an ancestor of A, B and the record tip; no frozen file changed after F. But the author timestamp the seat's command prints is jj change-creation time, not the freeze time (§1). |
| Draft revisions "none after any candidate scoring" | **STANDS (with a named caveat)** | No w1 report scores the candidate over a case file; the case-file digests inside the pre-freeze control receipts prove the last case revisions preceded those receipts (§2). |
| Round record (SCORECARD/ledger citations) | **WEAKENED** | One cited receipt is in no commit; two committed ledger figures are false for the measured revision (§3, H2/H3). |

## 1. Commit order and post-freeze drift (item 1)

`git log --format='%H %ad %s' 24ba2a9..498855` (exit 0) and the same with `--date=iso-strict` + `%cd`/`%p`:

| commit | author | committer | parent |
|---|---|---|---|
| `498855cb` records | 2026-11-06T16:41:32-03:00 | 2026-11-06T16:44:03-03:00 | `7d307486` |
| `7d307486` C2 tool | 2026-11-06T16:40:35-03:00 | 2026-11-06T16:41:32-03:00 | `650e18bd` |
| `650e18bd` C1 tool | 2026-11-06T16:40:27-03:00 | 2026-11-06T16:40:35-03:00 | `9e36e3a3` |
| `9e36e3a3` freeze | **2026-11-05T07:29:36-03:00** | 2026-11-06T16:40:29-03:00 | `f271f7fe` |
| `f271f7fe` parent | 2026-11-06T10:13:04-03:00 | 2026-11-06T10:13:04-03:00 | `1ee8b669` |

- **Order holds in the graph and in committer time**: F (`16:40:29`) < C1 (`16:40:35`) < C2 (`16:41:32`) < records
  (`16:44:03`); `650e18bd`'s parent is F and `7d307486`'s parent is C1. The tool commits are path-disjoint from the frozen files
  (`tools/mado-mako.py` only), and `tools/mado-mako.py` at F is byte-identical to base (`67a955a5…`).
- **No frozen drift**: `git diff --stat 9e36e3a3 498855 -- quality/counters .ufo/waves/round-88/controls` prints nothing, exit 0.
  Each of the six declared sha256 (cases, mutants, both counters, containment cases/mutants) matches at F and at the tip
  (`git show <rev>:<path> | sha256sum`, exit 0). The declaration itself is unchanged after F (full diffstat F..tip lists 15 files,
  none of them the declaration).
- **Metadata trap (H6)**: the freeze's *author* date precedes its own parent by 27 h and the round's declared date (2026-11-06).
  The commit object carries a jj `change-id lvnzypvtvnywzvtulvoyslvknplqkuow`, and `1793874576` equals the **base** commit's
  committer second (`24ba2a9` committer `1793874576`) — i.e. the author date is when the round's jj change was created, preserved
  across the day's rewrites. `%ad` therefore cannot prove the freeze ordering; `%cd` and the parent graph can, and they do.
  QUALITY 147 already states the rule ("the freeze ordering is proved by the commit graph, not by a timestamp in the file"), so this
  is a reading trap, not a false claim.
- **Candidate identity is sound**: `build/mado-mako.c1.py` and `.c2.py` inside the freeze commit hash to `07930521…` / `c374d715…`,
  exactly the `tools/mado-mako.py` bytes at A and at B (`sha256sum`; `git diff --no-index` build-vs-tool at A and at B → exit 0,
  identical). The pre-freeze control receipts name those same two digests.

## 2. Draft revisions vs candidate scoring (item 2)

- No candidate *score* exists before the freeze. `R88MCritic.md:4` states "No candidate scoring was run"; `grep -rn "62/62\|26/26"`
  over `.ufo/waves/round-88/w1/` → 0 hits; the only case-file counter runs in w1 (`R88MExecForgery.md:107-108,145-146`) are over
  **forged** revisions (`rev=36f2460…`, `147b134…`), never `650e18bd`/`7d307486`; `R88MExecSelftest` runs the candidates' own
  `--selftest` (checks=40/45) and `R88MExecHostDiff` runs them on the host config — neither is a case-file score.
- The last two draft revisions did precede the freeze, provably without git: both pre-freeze control receipts were produced against
  the **frozen** bytes — C1 `cases=62 cases_sha256=a0e81b19… candidate_file_sha256=07930521…`, C2 `cases=26 cases_sha256=8b16c0cb…
  candidate_file_sha256=c374d715…` (`receipts/c1-controls-prefreeze-r88.txt:1`, `c2-controls-prefreeze-r88.txt:1`). If c60–c62
  (rev 6) or k18–k26 (rev 5) had been added after those runs, the receipts would carry the earlier digests `a00d50c3…`/`3ee0dc9b…`
  that `R88MExecForgery`/`R88MScribeCasesC2` used. They do not.
- **Caveat (declared)**: candidate-derived controls existed pre-freeze (`inputs_ignored_correct=43`, `refuse_all_includes_correct=14`),
  and the L1 who wrote the candidate also authored k18–k26 and c60–c62. The declaration discloses both (Named limits third bullet);
  the case bytes themselves are the Cases seats' assignment, not mine.
- w1 settlement: `w1-results.json` has `seats=12`, `rows=12`, zero null outputs; the 12 report files exist in the freeze tree.

## 3. Figures, universal clauses, axis naming (item 3)

Reproduced with my own runs (commands and exit codes in §5):

| Figure (where) | Reproduced? |
|---|---|
| C1 62/62, mutants 22/22, carried 22/22, controls 14/15/33/43, score 10.0000 (SCORECARD 5137) | yes — my re-run at `650e18bd` and at `7d307486` |
| C1 "3/12 → 10/12" fields | yes — base `MODELLED_FIELDS` 3 at `tools/mado-mako.py:75`; candidate tuple 10 at `:87-88` |
| C1 "33/62 = 5.3226" | yes arithmetically; the base-tool control's 29 failures are **21 `exit=2`** (r87 CLI rejects the new flags) + 8 unexpected-refusal — a CLI-contaminated before, disclosed in the declaration, not labelled in the SCORECARD cell |
| C1 at B 62/62 (SCORECARD 5139) | yes — my re-run at `7d307486` |
| C2 26/26, 7/7, base 11, refuse-all 14, 10.0000 (SCORECARD 5138) | yes — my re-run at `7d307486` |
| C2 "C1-revision tool 11/26 = 4.2308" (SCORECARD 5138) | yes **as a base-tool control** (`c2-supp-base-is-A-r88.txt`, whose only difference from the B receipt is the `base_rev` pins; all 88 per-case lines are byte-identical between base=24ba2a9 and base=650e18bd) — not as a counter verdict |
| C2 declaration "Before: the counter at the C1 content revision → TARGET_MISSED" (declaration:127-128) | **no** — at `650e18bd` the counter prints `SETUP_ERROR forgery anchor 'if not self.within_roots(real):' occurs 0 times`, rc 2 (`receipts/c2-before-A-r88.txt`) |
| census "428 → 430 rows" (SCORECARD 5139, lesson §Census) | from the tree, not the receipt: `corpus/SOURCES.md` rows `428` at `24ba2a9` and `430` at `498855`; both census receipts carry no row count |
| census "55 `W04` before and after" | yes — `grep -c W04` = 55 in both committed receipts |
| harm watch index 109/109 · ledger 163/163 · selftest 460/460 · file plane 29 pass (SCORECARD 5139) | figures yes (my runs at `498855`), but the cited `receipts/harm-final-r88.txt` is **in no commit** (see H2) |
| ledger "19 sha-pinned mutants" (`quality/tool-ledger.md:200`) and "29 selftest checks" (`:197`) | **no** — frozen mutant file has 22 (`mutants=22` in the receipt); the tool at the tip prints `checks=52` |
| lesson "no `invisible` token in the r87 set (22 cases)" | yes — 0 matches, 22 cases |
| lesson base-tool cites `:75`, `:113-114` | yes |
| lesson domain share `| wc -l` = 4 | yes — command returns 4 at the tip |

Universal clauses:
- Declaration/SCORECARD "Every scored axis sits at 10 on its finite rubric" — the SCORECARD axis table still carries
  `freshness / file-plane gate agreement (omarchy-host rubric) | 9.6552 — dormant, host-absent`. Literally false unless "scored"
  excludes a dormant sub-axis; the lane's convention does exclude it, but the bare universal invites the misreading. (H5)
- QUALITY 147 "the freeze ordering is proved by the commit graph, not by a timestamp in the file" — **holds**; it is exactly why §1
  is judged on the graph (and it anticipates the `%ad` trap).
- QUALITY 146 "A resolver claim replays the host's own configuration once" — **holds** in this round: the freeze carries the replay,
  and I reproduced it (base `invisible 0`, B `invisible 1`).
- "none after any candidate scoring" — holds for the candidate score (§2); candidate-derived control numbers did exist pre-freeze.

Axis naming: **none named by number only.** The SCORECARD names `coverage` (capability) and `operability`; the declaration's posture
names navigation/calibration/selftest/file plane; `C1`/`C2` are claim ids, `W04`/`Q146` are warning/criterion ids, not axes.

## 4. Is C2 a genuine operability gain? (item 4)

Host chain, read-only, `--config ~/.config/mako/config --home $HOME --app-name Slack --mode do-not-disturb`
(config is a symlink to `omarchy/current/theme/mako.ini`; the include is `core.ini` under `$HOME`):

| tool | result | `effective.invisible` |
|---|---|---|
| base `24ba2a9` | `resolved=37 refusals=8` | `0` (refuses `core.ini:15/:18` `invisible='true'/'false'`) |
| C1 `650e18bd` | `resolved=37 refusals=6` | `1` |
| C2 `7d307486` | `resolved=37 refusals=6` | `1`; refusals are the `:20` urgency-needs-input line and the five `summary~` lines — **none containment-related** |

So C2 adds **no refusal** and loses nothing on the host chain: the containment test never fires there. The operability label is
defensible as "bounds the read set while still resolving the host", and it closes r87 R2, but the host run is *identical* at A and B,
so the host chain proves **no regression**, not a gain; the gain is measured on the K=26 surface (and the escape class). One design
consequence worth naming: the C2 counter cannot score a containment-free tool at all (the forgery anchor is built from the measured
tool), which is precisely why its "before" must be the base-tool control and not a counter verdict.

## 5. Findings and smallest safe corrections

| # | Severity | Finding (file:line, reproducing input) | Smallest safe correction |
|---|---|---|---|
| H1 | **high** | Declaration:127-128 "Before: the counter at the C1 content revision (no containment) → TARGET_MISSED" — the instrument cannot produce that verdict. Repro: `python3 -I quality/counters/c2-r88-include-containment.py --repo . --rev 650e18bd --base-rev 24ba2a9 --cases .ufo/waves/round-88/controls/containment-cases-r88.json --expect-cases-sha256 8b16c0cb… --expect-mutants-sha256 ff76cd69… --scratch-root DIR` → `SETUP_ERROR forgery anchor 'if not self.within_roots(real):' occurs 0 times`, rc 2 (committed as `c2-before-A-r88.txt`). | Post-freeze **erratum block** (never a predicate edit): "at A the counter exits 2 (forgery anchor absent); A's 11/26 is the base-tool control reading in `c2-supp-base-is-A-r88.txt`". The C2 predicate at B is untouched. |
| H2 | **high** | SCORECARD:5139 cites `receipts/harm-final-r88.txt`; that file exists only untracked in the worktree (`git status` → `?? …/harm-final-r88.txt`; `git log --all -- <path>` → empty; `git show 498855:<path>` → `fatal: path … exists on disk, but not in '498855cb…'`). No committed receipt carries the gate/index/ledger figures (I verified they are true: 109/109, 163/163, 460/460, 29 pass). | Commit `harm-final-r88.txt` in the record (or replace the pointer with the two rev-bound receipts that do exist and drop the gate figures that have none). |
| H3 | **medium** | Committed `quality/tool-ledger.md:200` says the C1 counter has "19 sha-pinned mutants" (frozen file: 22) and `:197` says `tools/mado-mako.py` has "29 selftest checks" (tip tool: 52). `check-tool-ledger` passes because it checks pointers, not descriptions. The correction is sitting in the working tree, uncommitted (` M quality/tool-ledger.md`). | Commit the already-written ledger rows (22 mutants, 52 checks, containment/grammar description) with the record. |
| H4 | **medium** | Census "428 → 430 rows" (SCORECARD:5139, lesson §Census) is not in either census receipt (they contain 55 W04 + 1 W01 + `mado ok …/corpus/SOURCES.md` + `rc=0`). It reproduces only from `corpus/SOURCES.md` row counts. | Have the census receipt print `rows=N` (or cite `grep -cE '^\| *S[0-9]+' corpus/SOURCES.md`). |
| H5 | low | Declaration:11 and SCORECARD:5136 "every axis sits at 10" while the axis table keeps `9.6552 — dormant, host-absent` (freshness/file-plane omarchy-host rubric). | "every non-dormant scored axis sits at 10". |
| H6 | low | Freeze author date `2026-11-05T07:29:36-03:00` precedes its own parent (`f271f7fe`, `2026-11-06T10:13:04`) and the round date; jj `change-id` present and the author second equals the base commit's committer second — the author date is change-creation time, preserved. `%ad` cannot prove ordering. | Say "committer order / parent graph" wherever the freeze time is asserted; keep QUALITY 147 as the rule of record. |

Nothing found that changes either score: C1 and C2 both reproduce exactly, and the frozen bytes are identical at the freeze and at
the tip. The defects are in the *narrative and record* (a false "before" verdict, one unlanded receipt, two stale ledger figures),
not in the measurements.

## 6. Commands run (all read-only) and exit codes

| command | rc |
|---|---|
| `git log --format='%H %ad %s' 24ba2a9..498855`; same with `%cd %p --date=iso-strict` | 0 / 0 |
| `git diff --stat 9e36e3a3 498855 -- quality/counters .ufo/waves/round-88/controls` | 0 (empty) |
| `git diff --stat 9e36e3a3 498855` | 0 (15 files, none frozen) |
| `git show <rev>:<frozen path> \| sha256sum` for 6 files at F and at tip | 0 (all six match the declaration) |
| `git show <rev>:tools/mado-mako.py \| sha256sum` at base/F/A/B/tip | 0 (67a955…, 67a955…, 079305…, c374d7…, c374d7…) |
| `git diff --no-index` build c1/c2 vs tool at A/B | 0 / 0 (identical) |
| `git cat-file -p 9e36e3a3`; `git cat-file -p` base/A/B/tip headers | 0 |
| C1 counter `--rev 650e18bd` (full pins) | 0 — `TARGET_MET … correct=62 … score=10.0000` |
| C1 counter `--rev 7d307486` (harm check) | 0 — `TARGET_MET … correct=62 … score=10.0000` |
| C1 counter `--rev 9e36e3a3` | 2 — `SETUP_ERROR mutant M11-string-mismatch-ignored: anchor occurs 0 times in the measured tool` (declared "before") |
| C2 counter `--rev 7d307486 --base-rev 24ba2a9` | 0 — `TARGET_MET … correct=26 … base_tool_correct=11 refuse_all_includes_correct=14` |
| C2 counter `--rev 650e18bd --base-rev 24ba2a9` | 2 — `SETUP_ERROR forgery anchor … occurs 0 times` (reproduces `c2-before-A-r88.txt`) |
| C2 tool at B, host chain | 0 — `MADO_MAKO: resolved=37 refusals=6`, `invisible=1` |
| C1 tool at A, host chain | 0 — `resolved=37 refusals=6`, `invisible=1` |
| base tool at `24ba2a9`, host chain | 0 — `resolved=37 refusals=8`, `invisible=0` |
| `python3 -I quality/check-index.py --repo . --rev 498855` | 0 — `indexed=109/109 … coverage=10.0000/10` |
| `python3 -I quality/check-tool-ledger.py --repo . --rev 498855` | 0 — `population=163 ledger_rows=163 … TARGET_MET` |
| `bash tools/mado-verify.sh --selftest` | 0 — `460/460` |
| `bash tools/mado-verify.sh --no-live` | 0 — `CLEAN (29 pass, 4 notes)` |
| `grep -c W04` over both census receipts | 55 / 55 |
| `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| *S[0-9]+'` at base/tip | 428 / 430 |
| r87 case file `sha256sum`; case count; `invisible` token count | `0a955874…`; 22; 0 |
| `git diff --name-only --diff-filter=AM 24ba2a9..HEAD -- corpus/knowledge tools quality/counters \| wc -l` | 4 |
| `git status --porcelain`; `git log --all -- <harm receipt>`; `git show 498855:<harm receipt>` | 0 (shows `?? harm-final-r88.txt`, ` M quality/tool-ledger.md`); empty; fatal (path not in commit) |
| `grep -rn "62/62\|26/26" .ufo/waves/round-88/w1/` | no hits |
| `diff` of `c2-measured-B` vs `c2-supp-base-is-A` | 1 (only the three `base`/`base_rev`/`tool_sha` pin lines differ; all 88 per-case lines identical) |

Dead steps: none of the counter runs failed; the only errors are the two intentional `SETUP_ERROR` reproductions (rc 2) and the
`git show` fatal above (the finding H2 itself). Scratch `/fast/scratch/hyaku/mado-r88/R88MResidCritic` deleted on exit. No installs,
no pacman transactions, no sysctl changes, no mutating git/jj command in the lane.

Report: .ufo/waves/round-88/r1/R88MResidCritic.md
