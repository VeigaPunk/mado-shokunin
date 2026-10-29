# R56W2ScribeLesson — round-56 lesson skeleton (wave w2)

Report: .ufo/waves/round-56/w2/R56W2ScribeLesson.md
Deliverable: `.ufo/waves/round-56/w2/R56W2ScribeLesson/lesson.md`
Receipts: `.ufo/waves/round-56/w2/R56W2ScribeLesson/receipts/lesson-facts-check.py` and `lesson-facts-check.out`
Scope: leaf scribe. No subagent. No tracked lane file, index, commit or fleet/sibling/shokuknow write. No host read (no hyprctl, no /proc). Lane read through `git show <rev>:<path>` only. Scratch `/fast/scratch/hyaku/mado-r56/R56W2ScribeLesson/` removed before yield.
No tools installed.

## What I attacked (scribe items)

1. **Gate**: admit S383-S390 with located quotes; S391 proposed; admit the entry; rejections (allowlist name-only, numlock class, Lua/hyprlang).
2. **Registry changes old->new**: 319 -> 328; used-by edits; full table path.
3. **Mistakes M56-1..M56-7**: class, evidence pointer, captured-by, fix. Two candidates added (M56-8, M56-9) where the evidence contradicts a fix.
4. **Outside spot-check**: items ready for the closure.
5. **Census**: start receipt; end left for the L1.

## What I did, with commands and decisive output

**Gate quotes against pins** (python3 -I, substring of the stated pin line):
```
Hyprland-ConfigWatcher.cpp 34 OK | setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());
Hyprland-ConfigValues.cpp 492 OK | MS<Bool>("misc:disable_autoreload", "If true, the config will not reload automatically on save.", ...
Hyprland-PropRefresher.cpp 148 OK / 149 OK
Hyprland-EventLoopManager.cpp 128 OK
Hyprland-legacy-ConfigManager.cpp 1080 OK / 1844 OK
Hyprland-MiscFunctions.cpp 65 OK / 68 OK
Hyprland-HyprCtl.cpp 1223 OK / 1276 OK
man7-inotify.7.html 186 OK / 262 OK
Hyprland-PropRefresher.hpp 18 -> `REFRESH_CONFIG_WATCHER     = (1 << 8),`   21 -> `REFRESH_ALL = std::numeric_limits<...>::max(),`
```
Pin hash checked: `Hyprland-PropRefresher.hpp` 1322 B sha256 `37acaaf1…af0d0`.

**Entry, registry and anchors at 28fc86ac** (`receipts/lesson-facts-check.py`, read-only `git show`, output in `lesson-facts-check.out`):
```
registry rows base=319 rev=328 added=['S383'..'S391'] removed=[]
rows with used-by change=23 appended used-by paths=41
allowlist rows=24 conflicts(in used-by)=0
entry evidence rows K=30 H=3 E=9
anchor-not-covering rows=6: E01 S388 :66, E03 S383 :106, E04 S389 :1190, E05 S387 :630, E06 S387 :1838, E07 S387 :2134
```
The 23 receipt rows match the lane's cell text exactly (checked cell by cell against base and rev). All 30 K rows and 3 E rows are covered.

**Other checks**
- `grep -n -i -E 'lua|hyprlang|numlock|configStringToInt|parseFile' entry`: only UNKNOWN or declared-limit lines (61, 134, 140).
- `grep -rn 'PropRefresher.hpp' frozen-tables-v2.json frozen-tables.json`: 0 hits. `git log` shows the hpp first committed at `0ff41272` (21:59), after freeze `3423ae28` (21:19) and v2 `323a69c9` (21:44).
- `frozen-tables-v2.json`: `base_pair_count: 65`, `base_pairs_sha256 630007b0…` (lines 784-785).
- Allowlist vs critic labels (`w1/R56CritCiteDef/pairs-65.tsv`): the critic's N, M-N and R pairs (21) are all in the allowlist; the 41 filled pairs are U 36 and M-U 5.
- `receipts/census-before.txt`: 28 W04, 1 W01, `mado ok`, rc=0.
- Duplicate-URL equality for the new rows (`lesson-facts-check` logic, last URL per row): S384 shares with S215, S318; S387 with S162, S303, S317, S353, S368; S388 with S182, S321; S389 with S158, S307, S320, S366.

## Defects and findings (with input and severity)

| id | finding | input that shows it | severity |
|---|---|---|---|
| D1 | Six E rows cite lines outside their registry anchors (M56-1 recurrence outside the K-only scope leg). | `lesson-facts-check.out`: E01, E03, E04, E05, E06, E07. Anchors: S388 `65,68`; S383 `…,105`; S389 `1223,1276`; S387 `776,1070,1079-1080,1816,1835-1836,1844`. | weakens the claim (E rows are uncounted; the entry presents them as registry-backed). |
| D2 | S391 (PropRefresher.hpp) pin is not in the frozen tables; the S391 row was added at integration. | `grep -c` over both frozen tables = 0; first commit `0ff41272`. Quotes at lines 18 and 21 verified here. | weakens (E08, E09 only; uncounted). |
| D3 | `lost` leg covers only the 65 base-missing pairs; the written §C3-v2 definition reads PAIRS(base) (381). | `registration-v2-errata.md:5-11`; `frozen-tables-v2.json:784-785`; `registration-v2.md:56`. | weakens (declared in the errata; a counter-to-hash alignment after the first failed run). |
| D4 | Five M-U pairs in the 41 fill (S015; S158, S162, S175, S177 on `hyprctl-verification-layer.md`, an errata sentence writing the range `S175-S177`). | critic labels in `pairs-65.tsv`; C3 reads literal tokens, so the range hides S176. | weakens the reliance reading. |
| D5 | Four allowlist pairs labelled U, M-U or R by the critic sit in the allowlist (R56RevC3Contract judged them name-only). | critic labels: U 1, M-U 2, R 1 among the 24. | cosmetic to weakens; open for closure. |
| D6 | Gate access date 2026-10-28 is the spec value; the w1 run read pins on 2026-10-29. | `w1/R56ScribeSourcesA.md` D4. | cosmetic (disclosed). |
| D7 | Census: the E11 count of 23 rows (errata E13) has no receipt in the lane. | `grep -rn E11 receipts/` empty. | unverified (not a defect of the claim). |
| D8 | The C2 hold-out is revealed, so a tool can read it by absolute path. | `w1/R56CritHoldout.md:41-43`; registration-v2 declared limit. | weakens C2 (declared, not a new defect). |

No finding blocks the frozen predicates: the K-row scope leg holds at 30/30 and the C3 allowlist conflict count is 0.

## Deliverables

- `.ufo/waves/round-56/w2/R56W2ScribeLesson/lesson.md`: Gate, Registry changes old->new, Mistakes (M56-1..M56-7, plus proposed M56-8 and M56-9), Outside spot-check, Census / source changes.
- `.ufo/waves/round-56/w2/R56W2ScribeLesson/receipts/lesson-facts-check.py` and `lesson-facts-check.out`.
- This report.

## Not verified / not run

- The end census: not run. The `sources-census.sh validate` command was not run here (it belongs to the L1 and the harm watch). The W04 count is expected to rise; the exact count is `[L1]`.
- Counter results at `28fc86ac` (C1 `TARGET_MET`, C2 `4/4`, C3 `missing=0`, C3 controls `9/9`): taken from the L1 brief, not re-run.
- Upstream bytes: the pins were compared to each other and to the quotes; no upstream fetch was made. The S391 hash is not checked against upstream.
- Entailment of the entry's propositions to the pinned lines: not audited (claims-frozen-v2: reported, not counted).
- The r55 scope-replay receipt (`receipts/scope-replay-r55.txt`) was not reproduced (no committed producer; errata F4 in w1).
- `grep -n -i numlock` on the entry found no hit; no other numlock-class check was run.
