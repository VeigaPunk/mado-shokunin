# R56W2ScribeRecords — round 56, wave w2 — scribe report

Report: .ufo/waves/round-56/w2/R56W2ScribeRecords.md
Deliverable: `.ufo/waves/round-56/w2/R56W2ScribeRecords/records.md` (LOG entry, SCORECARD `## Round 56`, QUALITY 107 final text, SHONEN check, FILL register).
Receipts: `.ufo/waves/round-56/w2/R56W2ScribeRecords/receipts/` (`c1.out`, `c3.out`, `ctl-c1.out/.err`, `ctl-c2.out`, `ctl-c3.out/.err`, `index.out`, `ledger.out`, `selftest.out`, `watchplan-selftest.out`, `census-after.txt`).
Scratch: `/fast/scratch/hyaku/mado-r56/R56W2ScribeRecords/` (one `git clone --shared` at `28fc86ac`), removed before this report. No lane file, no git mutation, no tracked-file write, no install.

Wave-2 results: not used. At the time of this report the wave-2 seats had partial directories only (`w2/R56W2CritC2Cheat`, `R56W2CritC3Gaming`, `R56W2CritFreezeV2`, `R56W2ScribeLesson`, `swarm-registry.json`), and no `w2/*.md` seat report had landed. Every wave-2-dependent number is a `<FILL>` in `records.md`.

## 1. Items attacked

| Item | What was attacked | Result |
|---|---|---|
| L1 LOG entry | every number and claim in the round-56 entry against the committed files at `28fc86ac` and the freeze/v2 commits | numbers reproduced; 3 factual corrections made while drafting (2 independent readers → "at least one of two"; E-row scope citation; S391 provenance); defects D1-D6 |
| SCORECARD `## Round 56` | before -> after per claim, counting commands, capability row, harm watch, round-57 plan | numbers reproduced; plan items drawn from verified findings (below); D3, D4, D2 are harm/caveats |
| QUALITY 107 draft (`w1/R56RevQuality/criterion.md`) | whether the Check line names committed instruments; whether the cited rules, criteria and lesson exist; whether the grammar matches the entry | Check instrument absent (D1); cited criteria 77 and 97 exist (`corpus/QUALITY.md` lines 401 and 521); `CORPUS.md` rule 2 exists at `/home/vgpnk/Projects/shokunin/CORPUS.md:116`; the entry grammar (`| id | proposition | src | pin:line | quote |`) matches the criterion's third and fourth cells |
| SHONEN.md | whether any box line may change | unchanged; no named non-author verifier this round (stated in `records.md` §4) |
| FILL discipline | every wave-2 or final-hash dependent number | all marked; none guessed |

## 2. Commands and decisive output

Scratch clone at the integration revision, then read-only counting (each `--work` under scratch; receipts copied before scratch removal):

```
git clone -q --shared /home/vgpnk/Projects/shokunin/mado-shokunin lane && git -C lane checkout -q --detach 28fc86ac2359ec27406d8a2c63bef82ea6e947ed
git -C lane rev-parse --show-toplevel   -> <scratch>/lane

python3 -I quality/check-r56-controls.py --claim c1 --repo . --rev 28fc86ac... --work <s>/ctl-c1   rc 0
  MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK
python3 -I quality/check-r56-controls.py --claim c2 ...   rc 0
  MADO_R56_C2: rev=28fc86ac... fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET
python3 -I quality/check-r56-controls.py --claim c3 ...   rc 0
  MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK
  (stderr) harness metrics of the good tree: {'entries': 71, 'rows': 328, 'missing': 24, 'extra': 0, 'dangling': 0}
  (stderr) note[good]: counter and harness numbers diverge (not scored): missing counter=0 harness=24
python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev ... --work <s>/c1   rc 0
  MADO_AUTORELOAD_ENTRY: rev=28fc86ac... rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none
python3 -I quality/counters/c3-r56-used-by.py --repo . --rev ... --work <s>/c3   rc 0
  MADO_USED_BY: rev=28fc86ac... entries=71 rows=328 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none
python3 -I quality/check-index.py --repo . --rev ...   rc 0 -> MADO_INDEX: indexed=71/71 missing=0 dangling=0 duplicates=0
python3 -I quality/check-tool-ledger.py --repo . --rev ...   rc 0 -> LEDGER: population=97 ledger_rows=97 uncovered=0 ... verdict=TARGET_MET
bash tools/mado-verify.sh --selftest   rc 0 -> MADO_SELFTEST: 460/460 assertions passed
python3 -I tools/mado-watchplan.py --selftest   rc 0 -> MADO_WATCH_SELFTEST: 82/82 assertions passed
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <s>/lane/corpus/SOURCES.md   rc 0 (32 W04 lines, 1 W01 line)
python3 -I quality/counters/c1-r56-autoreload-entry.py ... (the first run on the clone was the same numbers; the counters ran twice, once per scratch)
```

Base and history checks (committed files):

```
git ls-tree -r --name-only 28fc86ac | grep -c anchor-cover                 -> 0
git ls-tree -r --name-only 28fc86ac | grep -c 'lessons/round-56'           -> 0
git show 28fc86ac:.ufo/waves/round-56/frozen-tables-v2.json | grep -c S391 -> 0
git show 28fc86ac:corpus/knowledge/hyprland-config-autoreload-r56.md | grep -n S391   -> lines 128, 129 (E08, E09)
git show 28fc86ac:.ufo/waves/round-56/registration-v2.md | grep -n 'S383-S39'  -> line 75 "rows S383-S390"
census W04: receipts/census-before.txt 28 -> census-after 32; new entries S384, S387, S388, S389
git show 28fc86ac:corpus/SOURCES.md  S384 URL == S215 URL == S318 URL (src/config/values/ConfigValues.cpp @ efb5099...)
git diff --stat 28fc86ac HEAD -- SHONEN.md   (empty); md5 SHONEN.md 8f6cab7f... identical at 28fc86ac and the working tree
git log: 3423ae28 21:19:17 < 2aa347b1 21:22:53 (w1 dispatch); 323a69c9 21:44:35 < 19be88b6 22:04:27 (w2 dispatch); 2e39282e 21:54:28 (hold-out reveal)
```

## 3. Deliverables and their status

- `records.md` §1 LOG entry: drafted; FILLs for attempt, wave-2 results, final hash, freeze-order verdict at final rev, M56-2..n.
- `records.md` §2 SCORECARD round-56 section: drafted; capability row for `tools/mado-watchplan.py`; harm watch; planned round 57 (3 items).
- `records.md` §3 QUALITY 107: rewritten for the final text; not landable until D1 is resolved.
- `records.md` §4 SHONEN: unchanged (md5 identical), with the no-verifier statement.
- `records.md` §5 FILL register.

Planned round-57 items (each traced to a verified finding): (1) criterion-107 checker with E-rows and committed able-to-fail receipts (D1; `R56RevQuality` F4); (2) C3 harness/counter reconciliation and range-form citations (D3; `R56RevC3Contract` F3); (3) fresh sealed C2 hold-out and a non-author C1 entailment leg, plus the QUALITY 17 review of S384/S387/S388/S389 (D4, D5; `R56CritDoNothing` C1.1-C1.3).

## 4. Defects found (input that shows each; severity)

**D1 — blocking the criterion-107 landing.** The draft's Check line names `quality/check-anchor-cover.py`, and its "shown able to fail" receipts are named under `receipts/anchor-cover-*`. At `28fc86ac` `git ls-tree -r --name-only 28fc86ac | grep -c anchor-cover` prints 0; the lesson `corpus/lessons/round-56.md` cited as `#mistakes M56-1` is also absent (`grep -c 'lessons/round-56'` prints 0). The prototype numbers (`rows=32 covered=25 miss=7`) come from `R56RevQuality` §5 at `63f48dc1`, not from a committed receipt. Severity: **blocking the claim** of a checked criterion 107 (it cannot be run as written at the revision).

**D2 — weakens the C1 record: a post-freeze registry row outside the frozen set.** `corpus/knowledge/hyprland-config-autoreload-r56.md` lines 128-129 (E08, E09) cite `S391` (PropRefresher.hpp refresh-flag enum). `frozen-tables-v2.json` has no `S391` (`grep -c S391` = 0), `registration-v2.md` line 75 says "rows S383-S390", and the counter's `new_rows=8/8` leg counts only S383-S390. The row was added in `0ff41272` (after v2 `323a69c9`) and is not in `registration-v2-errata.md`. The LOG and SCORECARD draft now disclose it (9 new rows, 8 frozen plus S391). Severity: **weakens the claim** (the E-rows are outside the frozen predicate anyway, but the change should be disclosed where the frozen set is named).

**D3 — weakens the C3 claim: the harness does not agree with the counter it controls.** `receipts/ctl-c3.err` (run at `28fc86ac`): `harness metrics of the good tree: {'entries': 71, 'rows': 328, 'missing': 24, 'extra': 0, 'dangling': 0}` and `note[good]: counter and harness numbers diverge (not scored): missing counter=0 harness=24`. The harness's `missing` equals the 24 exempt pairs, which suggests the harness does not apply the frozen allowlist; I did not open the harness code to confirm the cause (unverified root cause). The 9 controls report `controls=9/9` on their own metric, so the harness's pass is not evidence about the counter's `missing`. Severity: **weakens the claim**.

**D4 — weakens the C1 admission: QUALITY 17 review not recorded.** Census W04 warnings rose 28 -> 32 (`receipts/census-after.txt` lines 30-33: S384, S387, S388, S389 "duplicate url ... across scopes"). S384 carries the same canonical URL as S215 and S318 (`.../src/config/values/ConfigValues.cpp` at `efb5099...`), and S387 the same as S162 and S317 (`.../src/config/legacy/ConfigManager.cpp`). No committed distinct-scope review exists (the lesson is absent, D1). `R56RevQuality` F3 reached the same finding from the freeze side. Severity: **weakens the claim** (QUALITY 17 unmet for four rows; the C1 counter does not check it).

**D5 — weakens the C2 falsification: the hold-out was revealed before the wave that attacks it.** Commit `2e39282e` ("hold-out reveal", 21:54:28) precedes the wave-2 dispatch `19be88b6` (22:04:27). A wave-2 seat that reads `fixtures/c2-holdout` by absolute path is not defeating a guard, because none is left; the claim binds only `c2.holdout_commit_sha256`. Stated in the LOG draft as a limit. Severity: **weakens the claim** (the C2 wave-2 attack cannot count as a hold-out test).

**D6 — unverified: the junk-entry control under v2 legs.** `R56CritDoNothing` C1.1-C1.3 reports that a 33-row template entry reaches TARGET_MET under the v1 legs. The v2 legs (E4 echo, E5 controls 11-12) may defeat it; I did not run a v2 junk-entry control (that would be a new attack, outside the scribe seat). The SCORECARD and LOG draft say so and leave `<FILL>`. Severity: **unknown**; it decides whether planned item 3 is already partly met.

**Not defects, checked:** freeze order (`3423ae28` before `2aa347b1`; `323a69c9` before `19be88b6`) holds by commit timestamps; the v2 files named in the LOG hash match `claims-frozen-v2.md` lines 6-7; `SHONEN.md` unchanged.

## 5. Not verified (said plainly)

- Wave-2 results: not read (no `w2/*.md` report landed). Every wave-2 dependent claim is a FILL. The wave-2 seat directories I saw are partial.
- The QUALITY 98 failure of the w1 dispatch and the QUALITY 22 axis conflict are taken from `R56RevQuality` F10 and F2; I did not re-run `tools/check100.py` or reopen `SCORECARD.md` lines 2722 and 244. They appear in the LOG draft as cited findings, not as my checks.
- The criterion-107 check was not run against the round-56 entry (the instrument is absent at `28fc86ac`).
- The `scope-replay-r55.txt` producer was not searched beyond `R56RevQuality` F4's `git grep` report.
- The C3 harness root cause (D3) and the C2 sibling-read repair under E6/E7 were not re-attacked here.
- The lane HEAD is `19be88b6`, not the brief's `9c3ca28a`; the LOG draft uses `28fc86ac` as the scored revision and leaves the final hash as a FILL.
- Mirror-count checks in the census (`W01`/`W04` meaning) were compared by count only.

## 6. Tools

None installed or upgraded. The counting commands used only the lane's committed Python and bash instruments, `python3 -I` and `bash`, plus the fleet census script in read-only `validate --file` mode.
