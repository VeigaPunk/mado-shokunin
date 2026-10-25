# Round-39 verifier spot-check — mado (non-author)

author: hyaku closure (non-author integrator, @m_sonnet)
date: 2026-10-25
lane HEAD measured: b6078c3ed9272be23932e00ee21ad29e3c1fdf9d (base 08be4eb7fd13358ed29b096e8924005d46ac409c)
report: .ufo/reports/round-39/mado.md (fleet repo; commits 547b8f0d "report honest partial attempt", 2ca2f26c "mado report", both `mado-shokunin <mado@shokunin.local>`)
dispatch digest (watchdog.log, mutable — copied here): `2026-10-25T15:56:16-03:00 launch mado round=39 pgid=3182525 driver=hyaku-inline attempt=1`; `2026-10-25T17:15:05-03:00 complete mado round=39; hyaku-inline attempt=1`

## 1. Step-1 conformance

| check | result |
|---|---|
| report committed by lane identity | PASS — `git log --format='%an %ae %H' -- .ufo/reports/round-39/mado.md` → 2 commits, both `mado-shokunin mado@shokunin.local` |
| SHONEN heading, one line per box | PASS — 4 lines (all `[~]` with pointers), mirrors the 4 boxes of `SHONEN.md` at HEAD |
| cited lane commits exist + ancestors of `master` | PASS — `merge-base --is-ancestor` holds for 457d1b1, d9b4e4a, 4ec582e, 3783961, 3628472 (full 362847279eccb77b22789a37cbbe3b83b205d49c), b6078c3, and base 08be4eb |
| pushed / ahead=0 | PASS — `jj-lane.sh state` → `local=remote=b6078c3… ahead=0 behind=0 tracked=0 untracked=0`; `git ls-remote`-equivalent in the state line agrees with the report's tip |
| uncommitted round work | PASS — `git status --porcelain` empty at closure. (Closure-side note: one of this reviewer's own `echo …->tip:` commands created a stray untracked file named `tip:` in the lane repo at 17:15; it was removed before anything was staged. Nothing was committed or moved.) |
| prompt carries template contract | PASS — `.ufo/prompts/mado-round-39.md` (545 lines, committed by `mado-shokunin`) carries §2 claims 1–3, the Sources/assimilation sections, the report-section list incl. SHONEN, and the hyaku §6 addendum |
| report minimum content | PASS — Work performed, Landed changes, Before → after, Sources & frontier (census command + counts), Trend verdicts, SHONEN all present |
| report vs later errata | PASS (one erratum issued) — the report corrects the fleet round-38 report's "frozen × fixed manifest = 19/19" sentence (frozen counter × frozen manifest = 18/19; 19/19 belongs to the post-rewrite pair) |

Marker predicate: not a marker — 6 landed commits, 287 files in the records commit, checkable receipts. Status `ok`.

Conformance defects (status-neutral, routed in §6): see D1–D3.

## 2. Claims — re-measured vs evidence-verified

Gate standard binds: the three counters (`quality/check-r38-discrimination.py`, `quality/counters/c3-r39-options.py`, `quality/counters/c4-r39-options-entry.py`) and `tools/mado-verify.sh --selftest` are lane-owned gates. This closure **verified their committed evidence and did not execute them**. Plain measurements were run by this reviewer over committed bytes and over the live host tree (read-only), as listed.

### C1 — calibration (re-registration of the round-38 discrimination pair): VERIFIED (evidence)

- Before (evidence): `receipts/c1-redbefore.txt` ends `controls=19 correct=18/19 verdict=TARGET_MISSED`; the single `ok=0` line is `control=c1-duprow instrument=c1 expected=TARGET_MISSED observed=TARGET_MET ok=0` — matches the report and the round-38 closure's ruling.
- After (evidence): `receipts/c1-after-tip.txt` ends `controls=19 correct=19/19 verdict=TARGET_MET`, `exit=0`; `grep -c 'ok=1'` → 19.
- Re-measured identities: `git diff --stat 08be4eb b6078c3 -- quality/check-r38-discrimination.py quality/counters/c1-r38-event-ground.py quality/counters/c2-r38-eventq.py` → empty (counters unchanged since base). `sha256` of `.ufo/waves/round-39/c1/manifest.json` at b6078c3 = `96965518dc8a…38c8` = sha256 of `.ufo/waves/round-38/controls/manifest.json` at base 08be4eb (byte-identical), whereas `receipts/manifest-frozen-r38.json` = `14c49d9f…edb` (the older frozen manifest used for the before). So the delta is a registration/freeze event (the r38 landed pair re-frozen at 457d1b1, before round-39 data), as the report states ("the pair is the round-38 landed pair") — not new instrument capability. Grade: calibration **improved** (the round-38 closure's required re-registration is done and re-frozen).
- Residual declared by the lane (a fully fabricated self-consistent artifact can pass) stands; not a harm.

### C2 — operability / capability acquisition (`tools/mado-options.py`): VERIFIED under PRED-C3-r39-v2 (ruling below)

- Before (re-measured): `git show 08be4eb:tools/mado-options.py` → exit 128 (absent); `receipts/c2-before-base.txt`: `fixtures=0/11 tool=absent verdict=TARGET_MISSED`, `exit=1`.
- After (evidence): `receipts/c2-after-data.txt` (rev 4ec582e) and `c2-after-tip.txt` (rev 362847279…) both end `fixtures=11/11 tool=present verdict=TARGET_MET`, `exit=0`; `clauses=a:1 b:1 d:1 g:1`.
- Re-measured, independent of the lane's counter: `sha256(tools/mado-options.py)` at 4ec582e = at b6078c3 = `461f8c3c245b…b03a` = the sha named in `S219.receipt.txt`. I extracted the tool from b6078c3 to `/tmp` and ran `python3 mado-options.py --home $HOME` on the live host tree (read-only): JSON array of **70 rows**; layers `{defaults 57, user 7, toggles 4, theme 2}`; owners `looknfeel.conf 47 / input.conf(default) 8 / input.conf(user) 7 / window-no-gaps.conf 4 / envs.conf 2 / theme hyprland.conf 2` — identical to the S219 receipt summary (`rows=70 owner files=6 layers defaults=57 user=7 toggles=4 theme=2`). No row key begins with a bind-variant/`windowrule`/`env` handler name (the only `bind*` hit is the real category `binds:hide_special_on_workspace_change`), consistent with M39-2's fix. The wave-built defect (9 handler rows) is absent.
- Evidence-verified only: tool selftest 71/71 (`c2/selftest-after.txt`); mutant kills `c2/selftest-mutA.txt` → `MADO_OPTIONS_SELFTEST: 69/71 passed exit=1`; controls `c2/ctl-*.txt`.
- **Ruling on the predicate question the lane left to the operator.** `registration.md` (freeze 457d1b1) named `PRED-C3-r39-v1` = the docstring of `quality/counters/c3-r39-options.py`, but at 457d1b1 that file did not exist (`c3/freeze-counter-check.txt`: `MISSING … missing=2`; re-measured here with `git cat-file -e 457d1b1:<path>` → MISSING ×2, `d9b4e4a:<path>` → present ×2). The v1 draft was never in any commit (preserved byte-exact as `c2/c3-r39-options.v1-draft.py.txt` and shown unreachable by `w1/CritC2Control.md`). The v2 counter and its controls were committed at d9b4e4a, 32 seconds before the first C2 data commit 4ec582e (`git log --format='%h %ci' 08be4eb..b6078c3`: d9b4e4a 17:03:37, 4ec582e 17:04:09), with the counter, manifest and discrimination checker byte-unchanged from d9b4e4a to the tip (`git diff --stat d9b4e4a b6078c3 -- <counters>` → empty). The round-38 precedent (a counter/manifest changed *after data* is a new predicate and fails as declared) is not triggered: no C2 data existed before the v2 freeze, the v2 freeze is stricter than the v1 intent (it rejects the wave-built tool 1/11, first-declarer mutant 1/11, replay and empty stubs 0/11), and the kill rule ("anything other than TARGET_MET at the data tip is a miss; no narrowing") is met at the tip. C2 verifies against the attempt-2 freeze; the registration variance is disclosed, not hidden, and is already mined as M39-1 with criterion 64 (shown able to fail: missing=2 at 457d1b1 → missing=0 at d9b4e4a). Grade: operability **improved**.

### C3 — coverage (sourced entry + S218–S220): VERIFIED

- Re-measured: SOURCES data rows `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 211 at 08be4eb, **214** at b6078c3 (+S218, S219, S220; all tier A, `mined`, 2026-10-25). `git ls-tree --name-only <rev> corpus/knowledge/ | grep -c '\.md$'` → 55 → **56**; the README references 56 distinct `knowledge/*.md` and no knowledge file is unindexed (loop printed nothing) — matches `indexed=56/56 missing=0 dangling=0 duplicates=0`. `corpus/knowledge/config-option-table-r39.md` is 123 lines with `source:`/`verified-at:`/`recheck:` frontmatter. The dispatcher-entry amendment is append-only (`git diff --stat`: +53 −0).
- Receipt integrity (re-measured): `sha256` of `fetch/S218.bin`, `fetch/S219.receipt.txt`, `fetch/S220.bin` at b6078c3 equal the digests in the lesson's `## Gate` and the SOURCES rows (`218da390…`, `c15e4034…`, `0740a0c4…`).
- Evidence-verified: counter `PRED-C4-r39-v1` first data commit 3783961 → `admitted=0/1` (clause g, S219 OBS wrap), tip 3628472 → `admitted=1/1 TARGET_MET exit=0` (`c3/measure-first-data-commit.txt`, `receipts/c3-after-tip.txt`); counter unchanged between them (`git diff --stat d9b4e4a b6078c3 -- quality/counters/c4-r39-options-entry.py` → empty). The first-data miss is disclosed in the report, SCORECARD and LOG; the claim verifies at the data tip as declared. Grade: coverage **improved**.

### Harm watch

- `git diff 08be4eb b6078c3 -- SCORECARD.md` → +51/−0, a new `## Round 39` section only; no published axis score row edited. Spot reads of the table: navigation 56/56, calibration 51/51, operability 12/12 (all unchanged at the 10.0 ceiling).
- Navigation re-measured above (56/56). `MADO_SELFTEST: 460/460` evidence-verified (`receipts/selftest-after.txt`, `exit=0`); not executed. Source census re-run here (§3): `exit=0`, warnings identical to round start (W04 ×7: S030, S042, S045, S097, S119, S120, S121; W01 S277). `git diff --stat 08be4eb b6078c3 -- quality/ tools/` adds only the two counters and the tool; no gate or SKILL/PROVINCE edit.
- No axis harmed. Axes not worked: depth, freshness, adjacency — unchanged.

## 3. Discernment spot-check (LEARNING.md) — from `corpus/lessons/round-39.md` `## Gate`

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → `mado ok`, `exit=0`, seven W04 + one W01 as at round start.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S218 (hyprlang 0.56.0 page) | admit (new row) | `curl -sSL https://wiki.hypr.land/0.56.0/Hypr-Ecosystem/hyprlang/` → HTTP 200; tag-stripped, entity-decoded text contains the quote, 18 words | **agree** | The ≤25-word quote is located; it states the overwrite rule for options, which is the era-correct (hyprlang `.conf`) basis of last-declarer ownership; row carries id line, date, tier A, used-by the new entry |
| S220 (0.54.0 Keywords page) | admit (new row) | `curl -sSL https://wiki.hypr.land/0.54.0/Configuring/Keywords/` → HTTP 200; quote "Meaning lines above the source = will be parsed first, …then lines below." present, 17 words | **agree** | Quote present; the 0.54.0 archive is the last hyprlang-era page, and the row discloses that choice; justifies depth-first source order |
| S219 (own-work) | admit (new row) | `sha256 fetch/S219.receipt.txt` = c15e4034… (row/lesson digest); tool sha matches; my own run of the tool on the live tree reproduced rows=70 / layers 57-7-4-2 / 6 owner files | **agree** | Own-work row backed by a re-runnable measurement that I independently reproduced; a row whose claim is "70 options from 6 owner files" stands |
| S162 / S173 re-open + used-by extension (G162 quote ":607 registerHandler(&::handleBind, \"bind\", {true});", G173 ":869 … avoid cases where a category is called the same as a handler") | admit as held, used-by extended | raw.githubusercontent.com Hyprland `efb5099…/src/config/legacy/ConfigManager.cpp` → HTTP 200, line 607 matches, lines 601-623 carry 21 `registerHandler` calls; hyprlang `v0.6.8/src/config.cpp` → HTTP 200, line 869 matches the quote | **agree** | Line anchors and quotes resolve at the pinned commits |
| 0.56.0 Variables page as S218 | **reject** (Lua `hl.config()` era) | `curl -sSL https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/` → HTTP 200; text "You are allowed multiple hl.config() invocations, each one will update just what you pass into it" | **agree** | The page documents the Lua `hl.config({…})` surface; the host parses a `.conf` tree (`~/.config/hypr/hyprland.conf` + sourced `*.conf`). Era fence is correct; the flip condition (host moves to a Lua config) is stated |
| Dispatchers page as a new S220 | **reject** (duplicate of held S196 URL) | lane's re-open byte-identical to S196 (sha `f9b51362…`, lesson Gate line) | **agree** | A second row for the same URL would duplicate (and trip census W04); citing S196 is right |
| Quarantine S224 | refused (payload absent) | `grep -c '2026-10-23T22:52:44Z' ~/.cache/ai-usage/status.json ~/.cache/ai-usage/inception-ledger.json` → 0, 0 (file exists); `w1/ExecQuarantineSlice/verdicts.md:14` | **agree (refusal), disagree (label)** | The quoted volatile timestamp is not in the cited file, so the row is rightly not appendable; but the lesson calls S224 "refused (fabrication class)" while the seat's own verdicts say "No row is flagged as fabrication … volatile timestamp rotated". A rotated timestamp is unverifiable, not fabricated — the lesson over-labels (D2) |
| Quarantine S199/S200 (CSDN HTTP 521) | unverifiable, not fabrication | seat transcript `verdicts.md` rows 16-17 (HTTP 521 + anti-bot JS) | **agree** | Unreachable ≠ absent; correctly left in quarantine |

`corpus/SOURCES.md` newly written row re-opened: S218 (quote location `## Syntax → ### Line Style`, "Last updated on March 31, 2026" is recorded in the row; quote 18 words ≤ 25) and S220 (17 words) — both within the cap; S219's quote ("rows=70 owner files=6 layers defaults=57 user=7 toggles=4 theme=2", 12 words) is in the receipt and the lesson Gate.

## 4. Per-axis verdicts (must agree with the MANIFEST entry)

| axis | verdict | basis |
|---|---|---|
| calibration | improved | C1 — r38 pair re-registered and re-frozen before data; 18/19 → 19/19 evidence-verified; delta is registration, noted above |
| operability | improved | C2 — tool absent → present; independent live-tree run reproduces the receipt (70 rows, 57/7/4/2); v2 predicate frozen pre-data |
| coverage | improved | C3 — 211 → 214 rows, 55 → 56 indexed entries, quotes re-opened |
| depth | unchanged | no depth claim |
| freshness | unchanged | held rows re-opened byte-identical, no claim |
| adjacency | unchanged | no claim |

## 5. Trend verdicts

- **expansion: improved** — one new admitted entry on uncovered ground (whole-tree option ownership: 70 keys vs six hand-proved), citing mined S218/S219/S220; one capability row (`config-option ownership table`) with a demonstration I reproduced.
- **quality: improved** — held rows S018/S162/S173/S196 re-opened and used-by extended; the wave-built tool's boundary defect is fixed and shown by two killed mutants (69/71 evidence); criterion 64 closes the unfrozen-predicate class with a committed before/after (missing=2 → 0); no admitted entry fails its re-check.
- **discernment: improved** — the outside spot-check agrees on every sampled admit (S218, S219, S220, S162/S173) and reject (Variables page era fence, duplicate-URL S196), and on the refusal of S224; the one label disagreement (D2) is minor and routed. Criterion 64 is grounded in lesson M39-1.

## 6. Routed defects (lane fixes next round; none status-bearing)

- **D1 — predicate variance, ruled here:** C2 was registered against a counter path absent from the freeze commit; the lane re-froze before data and says C2 is "an honest miss" under registration.md. This closure rules C2 verified under the attempt-2 freeze (reasons in §2). Future registrations must run the criterion-64 command at the freeze commit so no ruling is needed.
- **D2 — over-label:** `corpus/lessons/round-39.md` Assimilation ledger labels S224 "refused (fabrication class)"; the seat evidence (`verdicts.md:14`, `:28`) says a rotated volatile timestamp, no fabrication flag. Correct by an appended note in the round-40 lesson (append-only; do not rewrite).
- **D3 — dead seats:** three seats (ExecAssimAppendBlock, ScrReportFrontier, MutC3Row) produced no retained output ("orchestrator kernel restarted mid-wave"); the report discloses it. Next round should write seat reports before returning to the orchestrator so a kernel restart cannot erase them.
- Operator note (SHONEN): all four boxes remain `[~]`; promotion is operator-owned. This closure's independent live-tree reproduction of the option table is a non-author verification of box 2 (an end-to-end domain task executed and logged); boxes 1, 3, 4 were not re-verified from outside this round. No `[x]` written.
