# ConnReportFacts — round-18 facts for the round report (wave 2, FALSIFY)

Seat: `MadoR18.ConnReportFacts` (leaf connector, no delegation). Target root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Revisions named by hash:
baseline `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98`, integration
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`, receipts
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`. All numbers below are read from
`abfbf35` unless a path says otherwise. Read-only: `git log/show/diff/ls-tree/
rev-parse/cat-file/merge-base` plus file reads; no lane git/jj write, no lane
gate, no package/service/compositor probe, no fetch, no tool install or update.
The report path is the only file this seat wrote.

## 1. Every lane commit in `d9a5a18..abfbf35`

`git log --format='%H %an %cI %s' d9a5a18..abfbf35` returns exactly three
commits; `git log d9a5a18..refs/heads/master | wc -l` → 3;
`git rev-parse refs/heads/master` → `abfbf35b1ed4d4a1eb294d525ef286be30f3886f`;
`git merge-base --is-ancestor d9a5a18 abfbf35` → rc 0. Parent chain:
`d9a5a18 → d3a0000 → 4c103b5 → abfbf35`.

| revision | short | author / committer | date (git) | subject | change |
|---|---|---|---|---|---|
| `d3a00003e6ef0b1e3c7b4faf52d592eb293857ba` | d3a0000 | `mado-shokunin <mado@shokunin.local>` | `2026-10-20T12:34:53-03:00` | `round-18: pre-registration (claims C1-C3, baselines)` | 2 files, +60/−0 (`SCORECARD.md` +55; `evidence/census-start.txt` +5) |
| `4c103b55b1ea5c3c555884afe3eb69b5189701b7` | 4c103b5 | `mado-shokunin <mado@shokunin.local>` | `2026-10-20T12:55:36-03:00` | `round-18: wave-1 integration (frozen tripwire gate entry, gate rc fix + PIN re-cut, P3/P5 routes + S072-S095, QUALITY 24-26, lesson, round-17 erratum, registry rows, receipts)` | 250 files, +36,377/−19 |
| `abfbf35b1ed4d4a1eb294d525ef286be30f3886f` | abfbf35 | `mado-shokunin <mado@shokunin.local>` | `2026-10-20T12:56:38-03:00` | `round-18: receipts at 4c103b5 (measure before/after, tripwire re-cut r13-r16+anchor with producer header, frozen match/tampered/before, harm watch PASS)` | 30 files, +1,111/−36 |

`d3a0000` is the pre-registration, not a wave-1 result. `4c103b5` is the
integration: it adds all 88 wave-1 reports and the wave spec/dispatch/record,
`corpus/knowledge/walker-route-r18.md`, `corpus/knowledge/theme-route-r18.md`,
`corpus/lessons/round-18.md`, the S072–S095 rows, QUALITY 24–26, the
`receipt-check.py` / `measure-mutants.py` / `fetch-verify.py` /
`recut-receipts.sh` tools, the frozen snapshot, and the gate change. Its tool
numstats are `tools/mado-tripwire.py` +256/−10, `tools/mado-verify.sh` +81/−7,
`.gitignore` +2/−0. `abfbf35` adds 24 evidence files and edits 6 wave-1
reports (listed in §2).

## 2. Wave-1 seat roster and dead seats

Registry: `.ufo/waves/round-18/w1/reports/swarm-registry.json` (schema
`ufo-swarm-registry-v1`, wave `mado-r18-w1`, reportDir
`.ufo/waves/round-18/w1/reports`, createdAt `2026-10-20T15:39:34.538Z`,
updatedAt `2026-10-20T15:39:58.977Z`). `spec.json` has 88 items; the registry
has 88 members; the report directory has 88 member-named `.md` files. The
three sets are identical (0 spec-only, 0 registry-only). All entries are
`kind: spawn` with a non-null `agentId`; `dispatch.json` counts
`spawn 88, resume 0, total 88`, `maxLanes 100`.

**Dead seats: none.** Items with no report file: **[]** (0/88). No report is
zero-byte; committed report sizes run 1,906 B (`FrontierDraft`) to 51,272 B
(`RevFetchReceiptContract`), 1,459,307 B total. This is a file-presence test
only; report content is not graded here.

| role | count | seats |
|---|---|---|
| scout | 26 | CalibrationBaselineScout, ExistingThemeNotes, ExistingWalkerNotes, HostBackgroundChain, HostOmarchyCheckoutTag, HostThemeConsumers, HostThemeFiles, HostWalkerFiles, RubricBaselineScout, SourcesRowShape, SrcElephantProviders, SrcElephantReadme, SrcOmarchyBackground, SrcOmarchyManualThemes, SrcOmarchyThemeHooks, SrcOmarchyThemeLayout, SrcOmarchyThemeSet, SrcOmarchyWalker, SrcSwaybgMan, SrcThemeAlternates, SrcWalkerChangelog, SrcWalkerConfigPaths, SrcWalkerDefaultConfig, SrcWalkerDocsSite, SrcWalkerReadme, SrcWalkerThemes |
| executor | 16 | FetchBackfillR17, FetchVerify, FrozenProvenanceCheck, GateRcFix, HarmWatchScript, MeasureMutants, PipeRcCensus, ReceiptCheck, SessionIndexR17, TwFrozenMode, TwFrozenSelftest, TwFrozenSnapshot, TwInstallerChannels, TwMissBashCVar, TwMissHelperFn, TwRecutScript |
| reviewer | 12 | RevAdversarialLimits, RevFetchReceiptContract, RevFrozenContract, RevGateRcFixPlan, RevHarmWatch18, RevJjTrialFindings, RevNavigation, RevPreReg18, RevQualityOverlap, RevR17V1Facts, RevR17V2Facts, RevSeparability18 |
| scribe | 10 | ErratumR17, FrontierDraft, JjDisposition, LessonDraft, NoteTheme, NoteWalker, QualityDraft, ReportSkeleton, ScoreResultsDraft, SkillRegistryDraft |
| connector | 8 | ConnConsiderThese, ConnFrozenFormats, ConnJjFleetFixes, ConnLessonChain, ConnSkillSection, ConnSourcesUsedBy, ConnUnknownsJoin, SiblingOverlap18 |
| critic | 5 | CriticC1, CriticC2, CriticC3, CriticHonesty, CriticJjDisposition |
| revenger | 4 | RevengeKnownMisses, RevengePinRecut, RevengeR17Recut, RevengeTwSpec |
| sentinel | 3 | SentinelFetchBodies, SentinelFrozenPrivacy, SentinelHostPause |
| mutation-tester | 2 | MutTripwireScan, MutMeasureR17 |
| simplifier | 2 | SimplifyGateStub, SimplifyTripwire |

Revision-of-record note: all 88 reports are present at `4c103b5`; six were
amended at `abfbf35` (`RevAdversarialLimits`, `RevFetchReceiptContract`,
`RevFrozenContract`, `RevSeparability18`, `SrcThemeAlternates`,
`TwMissBashCVar`). Final report bytes are therefore the `abfbf35` blobs, not
the `4c103b5` blobs.

## 3. Routed defects and landed fixes

Sources: `corpus/lessons/round-17-verifier-spotcheck.md` §6 (R17-V1..V5),
`.ufo/waves/round-18/drafts/JjDisposition.md` (F10/F14/H4/T2/F15), and the
round-18 claim block `SCORECARD.md:931-984`.

| id | defect | landed fix | fix commit(s) | committed evidence |
|---|---|---|---|---|
| R17-V1 | Six round-17 real-transcript receipts have input digests but no producer identity; the unrecorded re-cut was narrated | `RECEIPT tool=… tool_sha256=… measured_commit=…` first line; `recut-receipts.sh` refuses on a failed `git show` (`PIPESTATUS`); QUALITY 24 | `4c103b5` (rule/script) + `abfbf35` (five re-cut receipts, summary) | `evidence/tripwire-r13..r16.txt`, `tripwire-anchor-r15.txt`; `evidence/recut-summary.json` |
| R17-V2 | Round-17 report paired `7a98720e…` (tool at `f71ccbe`) with a count that only exists at `0ab1ccc`/`962919ce…` | Append-only erratum in `corpus/lessons/round-17.md` labels both tool shas with their revisions; QUALITY 24 requires every report sha to name its revision | `4c103b5` | `corpus/lessons/round-17.md:177-201`; QUALITY 24 (`corpus/QUALITY.md:131`) |
| R17-V3 | Rubric V cannot tell a fetched row from an invented one | 24 tier-A rows S072–S095, 21 committed `mado-fetch-receipt-v1` files (301 lines), `fetch-verify.py` | `4c103b5` | `corpus/SOURCES.md:84-107`; `.ufo/waves/round-18/fetch/*/receipts.jsonl` |
| R17-V4 | Tripwire is a probe with no digest-pinned frozen input | `--frozen DIR` (+256/−10), committed `frozen/expected.json`, 5 byte-exact inputs, `provenance.json`; registry row `probe → gate` | `4c103b5` (tool/artifacts/SKILL) + `abfbf35` (replay receipts) | `frozen` match/tampered/before receipts; frozen selftest 17/17; `SKILL.md:566` |
| R17-V5 | Rubric-V tightenings were shown to bite only in a seat `/tmp` lab | `measure-mutants.py` + committed `evidence/measure-mutants.json`; QUALITY 25 | `4c103b5` | 6/6 bite, `no_bite: []`; instruments `a280b3ab…` (loose, `f52f43f`) and `de4c422b…` (tight, `d9a5a18`) |
| Jj F10 | Failed `git show` was hashed as empty input and reported as a false "local edit" | `set -o pipefail` inside the substitution, `grc≠0` → `UNKNOWN … (rc=N)`; OM9 | `4c103b5` | `evidence/gate-rc-redbefore.txt` §1; gate diff; `evidence/gate-selftest.txt` |
| Jj F14 | Selftest git stub exited 0 for every verb, so no scenario could fail | Per-verb `STUB_GIT_DESCRIBE_RC` / `STUB_GIT_REVPARSE_RC` / `STUB_GIT_SHOW_RC`; OM9/OM10 (+17 assertions) | `4c103b5` | gate selftest 389/389; `evidence/regression-recut.txt` 10/10 KILLED |
| Jj H4 / T2 | `.ufo/state/` was not ignored | `.gitignore` adds `.ufo/state/` and `__pycache__/` | `4c103b5` | `.gitignore:2-3`; `git diff abfbf35 -- .gitignore` empty |
| Jj F15 | `PIN_MADO` still named the pre-GateRcFix target | Re-cut `cd1d73d7…` → `20714096…`; `TABLE_MADO` unchanged | `4c103b5` | `tools/mado-verify.sh` pin line; `evidence/regression-recut.txt` §2/§4 |
| Jj F6/F8/F9/F16 | HEAD-as-tip rows; SKILL.md class-C recipes; `[ -d .git ]`; no gate landedness row | **Not fixed in this range** (JjDisposition: OPEN; F16 helper-only) | none | — |

R17-V1 detail. The five re-cut receipts are first-line-headered with
`tool_sha256=c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb`
and `measured_commit=4c103b55b1ea5c3c555884afe3eb69b5189701b7`. That sha
equals `git show 4c103b5:tools/mado-tripwire.py | sha256sum`; the tool is
unchanged at `abfbf35`. `recut-summary.json` says
`all_counts_identical: true`, `all_receipts_identical: true`, and per receipt
`counts_identical`, `files_identical`, `findings_multiset_identical`,
`permitted_identical`, `receipt_header_ok` all true. Counts (host_mutation /
live_probe / package_query; files/findings): r13 2/12/19, 33/33; r14 4/0/46,
33/50; r15 3/29/177, 65/209; r16 0/0/2, 97/2; anchor 2/1/5, 1/8. Receipt
sha256 values differ from round 17 because the new header is included; the
summary's "identical" fields are body/verdict-level, not file-sha identity.

`tripwire-pacmanlog-join.txt` is **not** one of the five first-line `RECEIPT`
files. Its first line is `# Round-18 C1 re-derivation…`; line 4 is
`# receipt: tool_sha256=… measured_commit=… utc=…` with no `cmd=`. The
summary records it separately (`pacmanlog_join`: 5 transactions, 4 joined,
0 orphan findings, unmatched `pacman.log:2416`), and its sha256 is
`be36165067b5f01b32aedc096026bf0dde680258026be0da3f999356e6765d92`. It is a
hand-derived awk join of `/var/log/pacman.log` and transcript call starts;
the named tool is the classifier behind the findings, not the join's producer.

R17-V2 detail. The erratum at `corpus/lessons/round-17.md:177-201` states that
the re-cut did run (`MadoR17.jsonl` record 539) but reproduced identical bytes,
so no committed byte showed it; it labels `7a98720e…` as the `f71ccbe` tool
with 26/26 and `962919ce…` as the `0ab1ccc`/landed tool with 30/30, and
supersedes the receipts with the round-18 files. There is no
`.ufo/reports/round-18/mado.md` in the lane and no `mado.md` under the fleet
`.ufo/reports/round-18/` (only `kasegi.md`, `kengaku.md`, `kotodama.md` at read
time), so the report-label half of QUALITY 24 is not yet exercised in a
committed round-18 report.

R17-V3 detail. S072–S095 are 24 rows, all `tier A`, all `status mined`; 20 are
used by `corpus/knowledge/walker-route-r18.md`, 4 by
`corpus/knowledge/theme-route-r18.md`; recheck values are 15 `on-release`,
8 `on-change`, 1 `90d` (S095). At `abfbf35` there are 21 `receipts.jsonl`
files (one per seat) with 301 JSON lines, 0 malformed: 296 HTTP 200 and
5 HTTP 404. An independent URL/anchor-sha join finds at least one receipt for
every web row S072–S089 and S092–S094; S090 is a host `/var/log/pacman.log`
row with no URL, and S091/S095 are host-file rows (their anchor shas can
coincide with fetched upstream bytes). **No fetch body file is tracked at
`abfbf35`**: `git ls-tree -r abfbf35 -- .ufo/waves/round-18/fetch` lists only
the 21 `receipts.jsonl` files (0 non-receipt files). `fetch-verify.py`
re-hashes bodies from the working tree, so a clean checkout cannot reproduce
the 301 `ok` results without the untracked bodies or a re-fetch.

R17-V4 detail. `frozen/expected.json` sha256
`4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9`, schema
`mado-tripwire-frozen-v1`, 5 inputs (`r15-libinput-events`,
`r13-global-capture`, `r14-review-source-bar`, `r14-source-safety`,
`r13-root`), `expected_exit 1`, `expected_label findings`, 8
`expected_findings`, 3 `known_misses`. Receipts: `frozen_match` exit 0,
`snapshot_tampered` exit 2, and the `d9a5a18` tool (`962919ce…`) `usage` exit
2. Frozen selftest: 17/17 cases, exit 0. `SKILL.md:566` carries
`mado-tripwire-frozen | gate`; the prior `mado-tripwire` row remains `probe`.

R17-V5 detail. `measure-mutants.json` summary:
`mutants 6, bites 6, no_bite [], expectations_met 6,
expected_but_unmet [], unexpected_tight_only [], baselines_agree true`.
Each mutant is a local commit in `/tmp/mado-r18-mutants-run/<id>/repo` with a
recorded `mutant_commit` and `diff_sha256`; the lane commits only the receipt
JSON, not those /tmp objects.

Jj F10/F14 detail. Gate sha256 at `4c103b5`: `c9fb0cef…` (3,785 lines);
baseline gate `fba82a66…`. Red-before (`gate-rc-redbefore.txt` §1): the old
gate with `git show` stub rc 128 prints `omarchy.skill.vs_head FAIL … HEAD
blob e3b0c44298fc… (local edit)`, old "local edit" count 1; the edited gate
prints `UNKNOWN cannot read HEAD:default/omarchy-skill/SKILL.md (rc=128)`,
count 0. The selftest is `MADO_SELFTEST: 389/389`; the derived-target
regression is 10/10 KILLED, control 284/284, `MADO_REGRESSION: PASS`, target
`20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744` (2,460 L /
121,533 B). The 284/284 and 389/389 are different objects (derived target vs
pristine gate) and should not be summed or interchanged.

## 4. Claim measurements as committed

| claim | before (`d9a5a18`) | after (`4c103b5`) | committed receipt |
|---|---|---|---|
| C1 calibration | 15/23 = **6.5217** | 18/26 = **6.9231** | `evidence/measure-before.json.txt` / `measure-after.json.txt`; QUALITY 24–26 at `corpus/QUALITY.md:131/138/144`; lesson rows M1–M6 at `corpus/lessons/round-18.md:16-21` |
| C2 coverage (rubric V) | 4/6 = **6.6667** | count **6/6**, score **10.0** | same measure files; `walker-route-r18.md` (321 L; sections at 46/173/258/283) and `theme-route-r18.md` (145 L; 38/74/123/134); S072–S095 |
| C3 frozen capability | tool `962919ce…`; `--frozen` usage exit 2 | tool `c87a31…`; `frozen_match` exit 0, tampered exit 2, frozen selftest 17/17 | `tripwire-frozen-{before,match,tampered}.txt`; `frozen/expected.json`; `harm-tripwire-round-18-frozen.txt` |

The instrument's C3 field in both measure files is `tool_present: true` plus
the tool sha (`962919ce…` before, `c87a31…` after); the before number does not
mean frozen mode existed. C1's 18/26 is 15 prior citations + one citation each
from new criteria 24, 25, 26. C2's after `score` is 10.0 in the unchanged
instrument; the declared target is the count 6/6.

Harm watch at `4c103b5` (`evidence/harm-watch-summary.txt`): 10 commands,
all `OK exit=0`, `HARM_WATCH: PASS`; includes gate selftest, action-plan
selftest, five tripwire suites (round-17 core/compound/hardening/
w2-regressions and round-18 frozen), U-measure 7/7, fleet navigation, and
census validate. The routed jj fixes are harm-watched defect repairs, not
claims (SCORECARD explicitly says so).

## 5. Contradictions and open facts for L1

1. **Criterion 24's runnable check is not green as committed.**
   `receipt-claims.json` at `abfbf35` has 15 claims, 6 of them `rev:
   "PENDING-L1"` pointing at `evidence/tripwire-{r13,r14,r15,r16,anchor-r15,
   pacmanlog-join}-recut.txt`; none of those six paths exists at `abfbf35`
   (`git cat-file -e` all MISSING; the only `*-recut.txt` path in the
   evidence dir is `regression-recut.txt`, plus `recut-summary.json`). The
   ReceiptCheck seat's own Scenario A printed
   `EXPECT_SUMMARY: 9/15`, `EXIT_A=2`; no committed receipt shows 15/15. This
   is the R17-V1/V2 check's wiring gap, not a failure of the five re-cut
   receipt bytes. The frozen replay is also absent from the claims file.
2. **Fetch receipts are committed; fetch bodies are not.**
   21 receipt files / 301 lines are tracked; 0 body files are tracked. C2's
   R17-V3 sentence says "committed raw fetch receipt (body bytes, sha256,
   byte count, fetch time)" — the receipt line is committed, but the body
   bytes it names are not, so `fetch-verify.py`'s byte re-hash needs the
   working tree (or a re-fetch). The five HTTP 404 receipts are recorded as
   404, not hidden.
3. **No round-18 report exists at `abfbf35`.** The lane has only
   `.ufo/reports/round-1/mado.md`; the fleet `.ufo/reports/round-18/`
   directory has other lanes' reports but no `mado.md`. R17-V2's
   "report labels every tool sha with the revision" requirement therefore
   has no round-18 report site yet; the erratum in `round-17.md` is the only
   committed label correction.
4. **The pacmanlog join is a derived, hand-authored receipt.** Its first line
   is a comment, not `RECEIPT`; its line-4 `# receipt:` names the tripwire
   tool sha but the join itself was produced by awk. `recut-summary.json`
   checks it only in the separate `pacmanlog_join` block (no
   `receipt_header_ok`). A strict reading of QUALITY 24 should either record
   the join's actual producer or classify it as a derived join outside the
   five tool receipts.
5. **JjDisposition's F15 "OPEN" status is superseded.** The draft read the
   lane at `d3a0000`, where `PIN_MADO` was still `cd1d73d7…`; `4c103b5`
   re-cuts it to `20714096…`, and `regression-recut.txt` §4 shows
   `REGRESSION_TARGET … match=yes` / `MADO_REGRESSION: PASS`. F10/F14 likewise
   move from PENDING to landed at `4c103b5`. Cite the landing commit, not the
   draft status.
6. **`all_receipts_identical` is body-level.** `recut-summary.json` says the
   five receipts are identical to round 17, but their file sha256s differ
   (new `RECEIPT` header). Do not quote the field as byte identity; the
   summary's per-receipt fields (`files_identical`,
   `findings_multiset_identical`, `counts_identical`, `permitted_identical`)
   are the byte/verdict comparisons.
7. **Wave-1 report bytes changed after integration.** Six reports were
   amended at `abfbf35`; any sentence citing a wave-1 report must name the
   revision it read. In particular `RevSeparability18`'s C3 path discrepancy
   (`frozen-tripwire` in the review text vs the actual
   `.ufo/waves/round-18/frozen`) was annotated there, and `TwMissBashCVar`
   records L1's relocation of its fixtures to `drafts/`.
8. **The join's unmatched transaction is still `pacman.log:2416`**
   (`pacman -S --needed --noconfirm man-pages`), and `pacman.log:2410`,
   `:2422`, `:2423`, `:2429` are the four joined findings. This agrees with
   the round-17 join; the receipt is not an incident record and the log line
   is not a running-binary fact.
9. **The `frozen` artifact path is `frozen/`, not `frozen-tripwire/`.**
   `SKILL.md:566` and the receipts use `.ufo/waves/round-18/frozen`; one
   wave-1 report initially used the other name and was amended at `abfbf35`.
   The C3 text should use the committed path.

No C3 evidence gap was found: the frozen replay, tamper refusal, pre-change
usage error, 17/17 selftest, and gate registry row are all committed. No
freshness claim is in this round.

## 6. Exact read-only commands run

```
git log --format='%H %an %cI %s' d9a5a18..abfbf35
git log --format='%h' d9a5a18..refs/heads/master | wc -l
git rev-parse refs/heads/master abfbf35 4c103b5 d3a0000 d9a5a18
git merge-base --is-ancestor d9a5a18 abfbf35
git show --stat --format='%h %an %cI %s' d3a0000 4c103b5 abfbf35
git show --numstat --format='' d3a0000 4c103b5 abfbf35 -- <paths>
git show <rev>:<path> | sha256sum          # gate, tripwire, QUALITY, SOURCES, .gitignore, receipts
git show abfbf35:<evidence file>            # headers, verdicts, recut summary, measure JSON
git ls-tree -r --name-only abfbf35 -- .ufo/waves/round-18/fetch
git ls-tree -r --name-only abfbf35 -- .ufo/waves/round-18/evidence
git ls-tree -r -l 4c103b5 -- .ufo/waves/round-18/w1/reports
git diff --stat 4c103b5 abfbf35 -- tools .gitignore corpus/QUALITY.md corpus/SOURCES.md \
  .ufo/waves/round-18/evidence/measure-mutants.json .ufo/waves/round-18/receipt-claims.json
git diff --stat abfbf35 -- .gitignore
python3 - <<'EOF' … EOF               # JSON parses of the registry, measure, recut, mutants, claims
grep/sed/wc/cat/find on the lane files above
```

I did not execute `receipt-check.py`, `fetch-verify.py`, `measure*.py`, any
tripwire suite, or any lane gate. The 9/15 figure is the ReceiptCheck seat's
retained output in its wave-1 report; the 6/6, 6.9231, 389/389, 10/10, 17/17,
and 301-receipt figures are read from committed receipt bytes. No tool was
installed or updated. No package, service, compositor, input, socket, or
screenshot command was run.

## 7. Bounded proposal (one, connector)

**Move:** make criterion 24's runnable check point at the receipts that
actually landed. In `receipt-claims.json`, replace the six `PENDING-L1`
`r18-recut-*` entries with the real `abfbf35` paths (drop the `-recut`
suffix; keep `r13…r16` and `anchor-r15`), add a frozen-replay claim for
`tripwire-frozen-match.txt`, and for the pacmanlog join either record its
actual awk producer or mark it `derived` outside the five tool receipts; then
commit the checker output. Expected totals: `15/15` if the join stays outside
the tool claims (6 round-17 red + 3 fixtures + 5 re-cut + 1 frozen), or
`16/16` if the join is also claimed with an accurate producer. Do not edit
any receipt; append a new claims revision rather than rewriting the red
PENDING record.

Affected axis: **C1 calibration** (criterion 24's check, R17-V1/V2). No C2/C3
artifact changes; no tool bytes, no receipt bytes, no gate move. Risks: editing
claims after the receipts can look like retrofitting; the join's `producer`
token is optional in `receipt-check.py` and absent from its first line, so a
naive re-point would be green for the wrong reason; a claims edit must not
relabel the six round-17 `MISSING_PROVENANCE` rows. Verification:
`python3 -I .ufo/waves/round-18/receipt-check.py` from the lane → expected
`EXPECT_SUMMARY: 15/15`, exit 0; flip one `expect` and confirm exit 1; read
the first line of each cited receipt and compare `tool_sha256` with
`git show <measured_commit>:<tool> | sha256sum`.
