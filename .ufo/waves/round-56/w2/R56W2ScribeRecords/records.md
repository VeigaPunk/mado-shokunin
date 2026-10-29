# R56W2ScribeRecords — round-56 record drafts (for the L1; not landed)

Seat: scribe, wave w2, leaf member, no subagents, no lane edits, no git mutation. Content revision scored: `28fc86ac2359ec27406d8a2c63bef82ea6e947ed`. Base `13f0acbe3a15da2d9c08357a576d91dcadc85273` (`frozen-tables-v2.json` `base`). Freeze v1 `3423ae285676c2a10273000f4519163472b443db`. Registration v2 `323a69c9014da1cebece67bb111b70a5630f4a60`. Lane tip named by the brief `9c3ca28a59de0dd23ee9950d22349333fc168a11`. The lane HEAD when this draft was written is `19be88b6d6112ce618c90d10999ffac031089051` (wave-2 dispatch), so `<FILL: final lane hash>` stays open.

Facts come from committed files at `28fc86ac` (or the freeze and v2 commits they name). Counter values were re-run in a `git clone --shared` scratch at `28fc86ac` and match the brief; receipts are in `receipts/` next to this file. Markers `<FILL: ...>` mark numbers or facts that depend on wave 2, the final lane hash, or a landing that has not happened.

---

## 1. LOG.md entry (paste after the round-55 entry)

```
## Round 56 (2026-10-28, hyaku run 11, attempt <FILL: attempt>) — three claims: coverage, operability, registry back-reference consistency; wave-2 verdicts <FILL: wave-2 summary>

- Base `13f0acbe`; freeze v1 `3423ae28` (committer 2026-10-28 21:19:17 -0300) before any wave; wave-1 spec/dispatch `2aa347b1` (21:22:53), 43 seats, 0 dead (`.ufo/waves/round-56/w1-dispatch.json` `counts.spawn` 43; 43 seat reports under `.ufo/waves/round-56/w1/`). Census before `.ufo/waves/round-56/receipts/census-before.txt` (`mado ok`, rc 0; W04 28, W01 1); selftest before `receipts/selftest-before.txt` 460/460.
- Wave 1 attacked v1 and found six defect classes, disclosed in `registration-v2.md` (a)-(e) and the wave reports: control 8 of C1 unsatisfiable as written (`R56RevC1Contract` §3.1); the C2 harness put `expected.out` beside the argument paths, so a six-line sibling reader scored 18/18 committed and the hold-out (`R56CritHoldout` F1; M55-4 recurs); the C3 target was met by deleting citing tokens (`R56CritDoNothing` C3); the witness covered K rows only; a declared divergence (`GLOB_TILDE`) was not one; the F12 fixture note was wrong. QUALITY 98 failed for the w1 dispatch (`check100` `PROSE-ONLY`, rc 1; `R56RevQuality` F10).
- Pre-data re-registration v2 `323a69c9` (21:44:35), before any real C1/C3 data, the C2 tool, or the hold-out reveal: `claims-frozen-v2.md`, `registration-v2.md` (E1-E11, §C3-v2), `frozen-tables-v2.json` (sha256 `9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2`), `c3-name-only.tsv` (24 reviewed name-only pairs, sha256 `70653e095839dc82f248d77fa5a0117134406a8b9e23778d2d79bf7072c948ee`), `ctl/sibling-reader.py`. The v1 files are byte-identical.
- Integration: `2e39282e` (21:54:28) C2 tool and harness, C3 counter, harness and `used-by` fill, C1 counter and harness, hold-out reveal; `0ff41272` (21:59:02) C1 entry `corpus/knowledge/hyprland-config-autoreload-r56.md`, registry rows S383-S391, README/PROVINCE/SKILL, tool ledger, comma-separated `used-by`; `28fc86ac` (22:00:24) C1 counter drops the bare `content` leg (E14), tool ledger row fix. Integration facts E12-E14 are in `registration-v2-errata.md` (`15015e77`): `lost` is defined over the 65 base-missing pairs; `used-by` separators are commas; no bare `content` leg.
- Measured at `28fc86ac` (`.ufo/waves/round-56/w2/R56W2ScribeRecords/receipts/`): all three frozen claim lines TARGET_MET; selftest 460/460; index 71/71; census `mado ok` rc 0; tool ledger 97/97; watchplan selftest 82/82.
- Hold-out: revealed at `2e39282e`, about 10 minutes before the wave-2 dispatch `19be88b6` (22:04:27). The C2 hold-out therefore no longer guards any wave-2 falsification; it is bound only by `c2.holdout_commit_sha256` in `frozen-tables-v2.json`. Stated as a limit, not as a pass.
- Wave 2 (falsify v2; 35 seats; `.ufo/waves/round-56/w2-dispatch.json` `counts.spawn` 35): <FILL: settled count, dead count, which legs broke, which controls were defeated, counter and harness defects found>.
- Freeze order (QUALITY 106): `3423ae28` precedes wave-1 dispatch `2aa347b1`; `323a69c9` precedes wave-2 dispatch `19be88b6`. Verdict at integration: <FILL: check-freeze-order verdict at final rev>.

| Claim / axis | Before -> after | Counting command | Verdict |
|---|---|---|---|
| C1 **coverage** (sourced entry), autoreload source chain (`misc:disable_autoreload`, `m_configPaths`, watch masks, reload path) | entry, counter, harness absent at `13f0acbe` (no citation of `disable_autoreload`, `ConfigWatcher` or `IN_CLOSE_WRITE` in `corpus/knowledge`) -> `rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 TARGET_MET`; harness `controls=12/12`; knowledge entries 70 -> 71; index 70/70 -> 71/71; registry 319 -> 328 rows (S383-S391) | `python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev <rev> --work <scratch>`; `python3 -I quality/check-r56-controls.py --claim c1 --repo . --rev <rev> --work <scratch>` | **TARGET_MET** (quote identity, registry binding, anchor scope, lexical grounding); entailment is not counted (QUALITY 104; wave-2 sentence audit <FILL: wave-2 result>); the nine E-rows are not checked by the frozen C1 scope leg (`R56RevQuality` F4; M56-1); S391 is outside the frozen `new_rows` set (D2) |
| C2 **operability** (capability), `tools/mado-watchplan.py` | tool absent at `13f0acbe` -> `fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 TARGET_MET`; controls at `28fc86ac`: `const-host` 1 of 18 committed and 0 of 8 hold-out, `empty` 0/0, `sibling-reader` 0/0 (staged layout), `lookup-committed` 18 committed and 0 hold-out | `python3 -I quality/check-r56-controls.py --claim c2 --repo . --rev <rev> --work <scratch>` | **TARGET_MET**; hold-out revealed before wave 2 (above); the tool is an approximation (8 divergences from hyprlang, listed in its docstring per E8); the live receipt is option-only (`MADO_WATCH_LIVE ... AGREE`), no inotify event observed |
| C3 **calibration**, re-labelled **registry back-reference consistency** (token level, reviewed), `used-by` cell 11 against entry citations | base `entries=70 rows=319 missing=41 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24` (`receipts/c3-base-v2.txt`; the v1 token count was 65) -> `entries=71 rows=328 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 TARGET_MET`; 23 registry rows changed in cell 11 (`receipts/used-by-old-to-new.md`); no entry text changed | `python3 -I quality/counters/c3-r56-used-by.py --repo . --rev <rev> --work <scratch>`; `python3 -I quality/check-r56-controls.py --claim c3 --repo . --rev <rev> --work <scratch>` (9/9) | **TARGET_MET** for the counter; the label is not a confidence measure; 24 name-only pairs are reviewed exemptions (each judged name-only by at least one of two independent wave-1 readers); the harness reports its own `missing=24` on the good tree, not scored (D3) |

Harm watch (at `28fc86ac`): `MADO_SELFTEST: 460/460` (unchanged); `MADO_INDEX: indexed=71/71 missing=0 dangling=0 duplicates=0`; census `mado ok` rc 0 with W04 warnings 28 -> 32 (new duplicate canonical URLs S384, S387, S388, S389 across scopes; the QUALITY 17 distinct-scope review is <FILL: recorded or not>); W01 unchanged at 1 (S277); tool ledger `population=97 ledger_rows=97 uncovered=0 TARGET_MET` (round 55: 90/90); `MADO_WATCH_SELFTEST: 82/82`. Verdicts are the operator's to rule; no score delta is asserted beyond the verdicts.

### Capabilities (round 56)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| Watch-list predictor for `misc:disable_autoreload` | predict the inotify watch list Hyprland 0.56.2 registers for a config tree (main config, its `source =` closure, glob and `~` forms, symlink canonical watches), joined to a captured `hyprctl getoption` reply; read-only, stdout only (`tools/mado-watchplan.py`) | `receipts/live-watchplan.txt` (`MADO_WATCH: DONE watches=40 unsupported=0 errors=0 live=AGREE`); C2 line above | 56 |

Sources: 319 -> 328 rows (S383-S391; S391 cited only by E08 and E09 and added after the frozen row set, see D2). Knowledge entries 70 -> 71. Round: w1 43 seats (0 dead) + w2 35 seats (<FILL: settled>). Mistakes: M56-1 (anchor scope; criterion 107) and <FILL: M56-2..M56-n from the lesson>.

Open after this round (declared, not claimed): QUALITY 22 axis posture (the claims call calibration the lowest axis; the recorded calibration rubric conflicts, `R56RevQuality` F2); QUALITY 17 review of S384, S387, S388, S389; the C2 hold-out is spent; no non-author verifier this round (see SHONEN).
```

Full hash values in the entry above are the committed values from `claims-frozen-v2.md` lines 6-7 and `frozen-tables-v2.json`; re-read them at landing.

---

## 2. SCORECARD.md — `## Round 56` section (append after the round-55 section)

```
## Round 56 — three claims, one capability (2026-10-28, hyaku run 11, attempt <FILL: attempt>)

Axis posture (`claims-frozen.md` lines 12-16, unchanged by v2): the last capability row entered in round 55, so the stagnation window has not elapsed and the lowest-axis obligation applies; C3 works calibration, re-labelled as registry back-reference consistency (below). Frozen at `3423ae28`; registration corrected pre-data at `323a69c9` (v1 files untouched; E1-E11). Measured at `28fc86ac` (`.ufo/waves/round-56/w2/R56W2ScribeRecords/receipts/`); final measurement at `<FILL: final content revision>`.

| Claim / axis | Before -> after | Counting command | Verdict |
|---|---|---|---|
| C1 **coverage** (sourced), autoreload source chain | entry, counter, harness absent -> `rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 TARGET_MET`; harness 12/12; entries 70 -> 71; index 70/70 -> 71/71 | `python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev <rev> --work <s>`; `python3 -I quality/check-r56-controls.py --claim c1 --repo . --rev <rev> --work <s>` | **TARGET_MET**; entailment not counted (QUALITY 104); wave-2 result: <FILL> |
| C2 **operability** (capability), `tools/mado-watchplan.py` | tool absent -> `fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 TARGET_MET` | `python3 -I quality/check-r56-controls.py --claim c2 --repo . --rev <rev> --work <s>` | **TARGET_MET**; hold-out revealed before wave 2 (guard spent); approximation with 8 listed divergences; wave-2 result: <FILL> |
| C3 **calibration**, re-labelled **registry back-reference consistency** (token level; 24 reviewed name-only exemptions; not a measure of confidence calibration) | `entries=70 rows=319 missing=41 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24` -> `entries=71 rows=328 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 TARGET_MET`; cell 11 only, 23 rows changed | `python3 -I quality/counters/c3-r56-used-by.py --repo . --rev <rev> --work <s>`; `python3 -I quality/check-r56-controls.py --claim c3 --repo . --rev <rev> --work <s>` (9/9) | **TARGET_MET** for the counter; the harness reports its own `missing=24` on the good tree (not scored, D3); wave-2 result: <FILL> |

Harm watch: `MADO_SELFTEST: 460/460`; index 71/71; census `mado ok` rc 0, W04 28 -> 32 (S384, S387, S388, S389 duplicate canonical URLs; QUALITY 17 review <FILL>), W01 1; tool ledger 97/97 (round 55: 90/90); watchplan selftest 82/82.

### Capabilities (round 56)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| watch-list predictor for `misc:disable_autoreload` (`tools/mado-watchplan.py`) | predicts the inotify watch list Hyprland 0.56.2 registers for a config tree, joined to a captured `hyprctl getoption` reply; read-only, stdout only; source-level approximation, no event or reload observed | `.ufo/waves/round-56/receipts/live-watchplan.txt`; C2 line above | 56 |

Sources: 319 -> 328 rows (S383-S391). Knowledge: 70 -> 71 entries. Round: w1 43 seats, w2 35 seats. Mistakes M56-1 and <FILL: M56-2..n>.

### Planned (round 57; intent only)

1. Land a checker for criterion 107 (anchor covers the quoted line) that reads the nine E-rows as well as the K rows, with able-to-fail receipts committed in the lane. The draft's `quality/check-anchor-cover.py` is absent at `28fc86ac`, and the `scope-replay-r55.txt` receipt has no committed producer (`R56RevQuality` F4).
2. Reconcile the C3 harness with its counter (the harness's good-tree `missing=24` against the counter's `0`), and expand range-form citations (`S175–S177` hides S176; the expanded base count is not the literal 65; `R56RevC3Contract` F3).
3. A fresh sealed hold-out for C2 and a non-author entailment leg for C1: the junk-entry control (33 template propositions) reached TARGET_MET under the v1 legs (`R56CritDoNothing` C1.1-C1.3; v2 legs: <FILL: wave-2 result>). The duplicate canonical URLs of S384, S387, S388 and S389 need the QUALITY 17 review recorded before the next entry cites them.
```

---

## 3. corpus/QUALITY.md — criterion 107 (final text; draft `.ufo/waves/round-56/w1/R56RevQuality/criterion.md` rewritten)

Placement: after criterion 106 in `corpus/QUALITY.md`. Landing it requires the checker and its receipts (see Status below).

```
## Criterion from the round-55 scope mistake (round 56; M56-1, mined from round 55; lesson `corpus/lessons/round-56.md` M56-1; extends 77 and 97)

**107.** **A registry row cited by an entry's evidence row has an anchor that names the row's own source file and covers the quoted line** — For every evidence row of a knowledge entry whose third cell is a registry id `S###` and whose fourth cell is `<file>:<N>` (the K-row and E-row grammar of `corpus/knowledge/`; H rows, whose third cell is `host`, are outside this criterion), the registry row of that id in `corpus/SOURCES.md` must satisfy: NAME, the last path component of the last `http(s)://` token of that row's source cell (the upstream file the row credits), occurs in the anchor cell (cell 6) as `NAME:` not preceded by an identifier character, followed by a comma-separated list of locators whose first item is `N` or `N-M` (later items continue the list only while they begin with digits); and some range in that list includes `N`, the quoted line. A row whose anchor names no such file, or whose ranges all exclude `N`, is a violation whatever its quote or proposition says. The fix is a supersession row with a widened anchor, with the old row's `status` changed in place (only `status`, `recheck` and `used-by` change in place; `CORPUS.md` rule 2), or a re-cite of a row whose anchor covers the line; each such change is logged in the round lesson. An entry with no evidence rows reads `rows=0` and fails, so an empty entry is not vacuously green.
Check: `python3 -I quality/check-anchor-cover.py --repo . --rev <rev> --entry corpus/knowledge/<entry>.md --work <scratch>` prints one `ANCHOR_COVER: row=<id> sid=<S###> line=<N> name=<NAME> locators=<list> verdict=OK|MISS [reason=no-name|no-cover]` line per evidence row, then `CHECK107: rows=<n> covered=<k> miss=<m> verdict=OK|FAIL`; the requirement is `miss=0` with `rows>0`; exit 0 on OK, 1 on FAIL, 2 on setup error (stdout empty). The instrument reads git objects at `<rev>` only and writes only under `--work`. Shown able to fail: <FILL: committed instrument path and receipts>. On the round-55 entry `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` at `63f48dc1` the prototype reads `rows=32 covered=25 miss=7 verdict=FAIL`, rc 1 (K14 anchor `ConfigValues.cpp:271-279,296` against line 280; K17 anchor names no `wayland.xml:` against line 2741; E04, E05 and E11 on S052 at 2732, 2740 and 2740; E08 on S316 against 1195; E14 on S379 against 350); with the anchors widened in a scratch registry it reads `covered=32 miss=0`, rc 0. Lesson: `corpus/lessons/round-56.md` M56-1; round-55 replay `.ufo/waves/round-56/receipts/scope-replay-r55.txt` (producer: <FILL: committed producer, or retire the receipt>).
Declared limit: the check reads the anchor text, not the upstream file, so an anchor that names the right file and a range whose lines carry a different statement passes (the sentence-to-pin audit of criterion 104 carries that); a source URL whose last component is not the file the anchor names (a rename, or a directory-qualified name such as `legacy/ConfigManager.cpp` cited as `ConfigManager.cpp`) reads MISS and must be read before it is treated as a violation; the criterion counts E-rows, which the frozen round-56 C1 scope leg does not check.
```

Status of this text (for the L1):
- Not landable at `28fc86ac`. `quality/check-anchor-cover.py` is not in the lane tree (`git ls-tree -r --name-only 28fc86ac | grep -c anchor-cover` prints 0), and neither the `receipts/anchor-cover-*` files nor `corpus/lessons/round-56.md` exist there. The draft's Check line names an instrument that is not committed.
- The prototype figures in the text come from `R56RevQuality` §5 (a scratch prototype at `63f48dc1`); they are not committed receipts and must be replaced by committed ones before landing.
- The criterion has not been run against the round-56 entry; that result is `<FILL>`.
- `CORPUS.md` rule 2 is at `/home/vgpnk/Projects/shokunin/CORPUS.md:116` (fleet root, not in the lane tree); the citation is correct.

---

## 4. SHONEN.md — box lines

No change. `SHONEN.md` at `28fc86ac` and in the working tree are byte-identical (md5 `8f6cab7fca09eb2a70cffc139f9436e7`). No named non-author verifier exists for round 56: the wave-1 and wave-2 seats are dispatched attack and build seats of this round, and the last non-author spot-check in the lane is the round-55 commit `13f0acbe` (the base), which is not a round-56 verifier. The four `[~]` lines stay as they are:

- `[~] SKILL.md contains real decision tables ...` (MADO-R3-4)
- `[~] At least one end-to-end domain task executed and logged in LOG.md` (VER-M3)
- `[~] Instructions executable by an agent without oral context` (MADO-R3-4)
- `[~] No cross-domain bleed (PROVINCE.md still accurate)` (VER-M4B)

---

## 5. FILL register

| Marker | Depends on | Source to fill from |
|---|---|---|
| `<FILL: attempt>` (LOG and SCORECARD headers) | run bookkeeping | orchestrator |
| `<FILL: wave-2 summary>`, wave-2 settled and dead counts, which legs and controls wave 2 broke | wave 2 | `.ufo/waves/round-56/w2/*.md`, `w2-results.json` once landed |
| `<FILL: final content revision>`, `<FILL: final lane hash>` | integration after wave 2 | `git rev-parse` at the final commit |
| `<FILL: check-freeze-order verdict at final rev>` | integration | `quality/check-freeze-order.py` at the final rev |
| QUALITY 17 review of S384, S387, S388, S389 | scribe / lesson | lesson `corpus/lessons/round-56.md` once landed |
| `<FILL: M56-2..n>` | lesson | lesson |
| criterion 107 status (instrument path, able-to-fail receipts, r56 entry result, producer of `scope-replay-r55.txt`) | round-57 instrument or waiver | L1 |
| wave-2 results for the C1 sentence audit, the C2 hold-out, and the C3 allowlist; v2 result for the junk-entry control | wave 2 | w2 reports |
