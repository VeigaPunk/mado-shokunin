# Round 55 verifier spot-check — mado

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-10-28
lane base: `3b55b6e91e40f455dd56b2985e4ffc087ada92d5`; lane tip: `63f48dc1b240b707c5ab9d634e2395ab90e1540c`
report: `.ufo/reports/round-55/mado.md` (fleet commit `efbe50f986b47a5764b77f9a3b515a3131536cc4`)
driver digest (`.ufo/watchdog.log`, copied):
`2026-10-28T18:36:01-03:00 launch mado round=55 pgid=2192556 driver=hyaku-inline attempt=1`
`2026-10-28T20:54:51-03:00 complete mado round=55; hyaku-inline attempt=1`

Method note: the lane's counters, harnesses and selftests (`quality/counters/*`, `quality/check-r55-controls.py`, `tools/mado-verify.sh --selftest`, `check-freeze-order.py`, ...) were NOT executed by this closure (PROTOCOL §Gate standard, Closure consequence; round 54's closure-correction). Gate-backed claims are **evidence-verified** (committed receipt `.ufo/waves/round-55/receipts/at-final.txt`, revision `d3fc9ac14a673a7d56f11b6d4956d754179067bf`) plus **independently re-measured** with plain commands/scripts of the closure's own over committed bytes, as listed below. I also ran `tools/mado-kbdopts.py --selftest` once out of an export in `/tmp` (`83/83 assertions passed`); that is informational and no grade relies on it.

## 1. Step-1 conformance

| Check | Command / evidence | Observed | Result |
|---|---|---|---|
| Report identity | `git log --format='%an %H' -- .ufo/reports/round-55/mado.md` | `mado-shokunin efbe50f986b4…` (author date 20:44:06, committer date 20:49:37) | pass |
| Report after lane work | `git -C mado-shokunin log -1 --format='%ad / %cd' 63f48dc1` | lane tip author 20:49:01, committer 20:49:02-03; report committer 20:49:37-03 (the report's author-date 20:44:06 precedes the tip, the committer date follows it) | pass; author-date artefact only |
| SHONEN | `grep -c '^## SHONEN'`; `grep -cE '^- \[' SHONEN.md` | one heading, four `[~]` lines = four boxes | pass |
| Cited commits exist + ancestry | `git merge-base --is-ancestor <h> master` for `54dacbd8 3c868d82 dbc2eefe 5a43d67f ebd66fbf 57584ed6 721ba9c1 187003d0 d3fc9ac1 63f48dc1` | all ten `ok`; `master` = `63f48dc1…` | pass |
| Clean + pushed | `scripts/hyaku/jj-lane.sh state mado-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote `63f48dc1…` | pass |
| Prompt contract | `.ufo/prompts/mado-round-55.md` (689 lines) | §1 mission/axes binding, §2 claims, §2b frontier, §3 L2 floor, §4 report contract (SHONEN), §5 commit/push scope, §6 hyaku addendum, §7 scratch all present | pass |
| Freeze before launch | `git show -s --format='%H %an %cI' 54dacbd8`; w1/w2 `swarm-registry.json` `createdAt` | freeze committer 2026-10-28T18:46:52-03; w1 `createdAt=21:50:15.231Z` = 18:50:15-03; w2 `createdAt=23:19:14.796Z` = 20:19:14-03 (w2 spec commit `721ba9c1` 20:19:19-03) | pass; the round-54 defect (M54-2/M54-4) is not repeated |
| Pre-data errata v2 | `git log --diff-filter=A --format='%h %cI'` for `registration-v2.md`, `frozen-tables-v2.json`, the entry, counters, tool, hold-out | v2 `5a43d67f` 20:11:17-03; entry, `c1-r55-kbd-entry.py`, `c3-r55-p19.py`, `check-r55-controls.py`, `tools/mado-kbdopts.py`, `fixtures/c2-holdout` all first appear in `ebd66fbf` 20:16:27-03 | v2 **counts as pre-data** (committed 5m before any real entry/counter/tool existed; claim sentences, targets and control counts unchanged); disclosed by the lane. It followed w1's attacks, so it is not pre-wave |
| Sealed hold-out | `holdout_commit_sha256` in `frozen-tables.json` at `54dacbd8` vs a closure-computed commitment (`sha256` over `<relpath>\0<sha256(bytes)>\n`, sorted) of `fixtures/c2-holdout` at `63f48dc1` | both `1275d7f804c887c1109e3c9e0c4cc590c162399660301da5fa4196c05a92c549` | pass |
| WAVE-DONE evidence | `at-final.txt` `MADO_WAVE_DONE: round=55 waves=2 settled=2 verdict=OK` | seats 40 + 37 dispatched and settled (two w1 seats dead on a provider limit, disclosed M55-6 and re-issued in w2) | pass; evidence-verified |

Status-neutral defects named for the lane: (a) the helper rewrote the freeze commit (`59e3763f` -> `54dacbd8`, disclosed M55-7); (b) hold-out destination named to a builder seat (M55-5, disclosed); (c) `corpus/lessons/round-55.md` still carries stale counts in `## Gate` ("Rows `314 → 317`", "317 rows" in the census paragraph) while its last section, the report and `SOURCES.md` say 319 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 319). No conformance defect bars admission.

## 2. Per-claim re-check

Re-measured = a command of the closure's own over committed bytes at `63f48dc1` (corpus/tool/fixtures are unchanged from `d3fc9ac1` apart from LOG/SCORECARD/lesson/receipts per the report; the closure measured the tip). Evidence-verified = the lane's committed gate receipt only.

### C1 coverage — sourced entry on keyboard repeat rate / repeat delay / numlock — **improved** (re-measured + evidence-verified)

- Before at base: `git grep -lE 'repeat_info|m_repeatRate' 3b55b6e -- corpus/knowledge | wc -l` → `0`. After: `grep -lE 'repeat_info|m_repeatRate' corpus/knowledge/*.md` → `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` (1 file).
- Knowledge files / README index rows: `git ls-tree --name-only <rev> corpus/knowledge/ | wc -l` and `git show <rev>:corpus/README.md | grep -c '^| `knowledge/'` → `69 69` at `3b55b6e`, `70 70` at `63f48dc1`.
- Rows: the closure's script over the entry found 24 rows (18 `K`, 6 `H`); all 38 quote cells (K, H, E rows) are exact substrings of the stated line of the stated pin under `.ufo/waves/round-55/fetch/` (`/tmp/r55chk.py`: `38 0` = 38 hits, 0 misses). Every S-id cited by K rows (S052, S316-S319, S378-S380) is one registry row of 11 cells with `used-by` containing the entry path.
- Pins vs upstream: `curl` of `raw.githubusercontent.com/hyprwm/Hyprland/efb50993…/src/{managers/SeatManager.cpp,protocols/core/Seat.cpp,devices/IKeyboard.hpp,config/values/ConfigValues.cpp}` and `gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml`: sha256 equal the committed pins (`bd748553…`, `cc23bb8b…`, `82e0bc9e…`, `a76f0507…`, `cc860987…`).
- Registry: rows `314 → 319` (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at both revisions); the closure diffed every cell of every pre-existing row base→tip: only cell index 10 (`used-by`) changed on S052, S316-S319; new ids S378-S382; no other edit (append-only holds).
- Lane gate output `MADO_KBD_ENTRY: … rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none` and `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK` are in `receipts/at-final.txt` — evidence-verified, not executed here. The lane's own declared limit stands: the counter proves quote identity, not entailment; junk or false-proposition entries pass it. The closure's sentence-level reads of K04-K07, K09-K12, K18 (above) found them supported by the pinned lines.

### C2 operability — `tools/mado-kbdopts.py` capability — **improved** (re-measured + evidence-verified)

- Before: `git ls-tree -r --name-only 3b55b6e tools | grep -c mado-kbdopts` → `0`; after: tool present, first added in `ebd66fbf`.
- Closure's own runner (export of `tools/mado-kbdopts.py`, the fixtures and `fetch/` at `63f48dc1` into `/tmp/r55x`; each fixture run as `python3 -I tools/mado-kbdopts.py <args.json>` from the exported root; stdout bytes + rc vs `expected.out`/`expected.rc`): committed `c2` **18/18**, `c2-holdout` **8/8**, `c2-extra` **24/24** (a first pass reported `17/18` because the export had omitted `fetch/`; re-run with `fetch/` → F02 byte-identical).
- Hold-out sealed before reveal and commitment equal (see §1). Candidate tools were committed at `3c868d82` before the hold-out reveal at `ebd66fbf`.
- Lane gate lines (`MADO_R55_C2: … fixtures=18/18 holdout=8/8 holdout_commit=ok controls=3/3 verdict=TARGET_MET`) are evidence-verified from the receipt, not executed. Declared limits stand: the tool is an approximation of hyprlang (docstring lists divergences); the frozen sentence "models source-level semantics" overclaimed and the docstring was corrected (M55-12). Capability row present in `SCORECARD.md` (`### Capabilities (round 55)`) with a live read-only receipt `receipts/live-kbdopts.txt`.

### C3 freshness — append-only correction of false P19 — **improved** (re-measured + evidence-verified)

- Before: `git show 3b55b6e:corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md | grep -c P23` → `0`; after: `grep -c P23` → `6`.
- Append-only: `git diff 3b55b6e 63f48dc --stat -- <entry>` → `38 insertions(+)`, `0` deletions; the P19 row (line 17) still stands as history, with a P23 row superseding it.
- Truth check against the round-52 pin `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp:1560-1572`: the `else` arm (`m_passPressed` neither 1 nor 0) sends a keyboard PRESSED then RELEASED (`!isMouse`) and pointer PRESSED then RELEASED otherwise — P23's three-arm statement is true and P19's "only when `m_passPressed == 1`" was false.
- README row updated (`corpus/README.md:118`, round-55 note + index row mention P23). `grep -rn P19` over non-`.ufo`/non-lesson docs finds no further live statement of the false wording.
- Lane gate line `MADO_P19_FIX … TARGET_MET` + `controls=6/6` evidence-verified from the receipt. The lexical `p23` leg proves vocabulary only (lane's own limit); the closure's pin read above supplies the truth check.

### Harm watch

`git diff 3b55b6e 63f48dc --numstat -- SCORECARD.md LOG.md corpus/QUALITY.md` → `27/0`, `8/0`, `6/0` (additions only). `corpus/README.md`: 5 changed lines (4 insertions, 1 deletion: the index row of the r53 errata rewritten to mention P23, same entry). `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` run by the closure → `mado ok`, exit 0 (W04 warnings including S380-S382, W01 S277, all warning classes; S380-S382 are the lane-disclosed same-URL distinct-scope rows). Lane receipt `MADO_SELFTEST: 460/460`, `MADO_INDEX 70/70`, `LEDGER: population=90 … TARGET_MET` evidence-verified only.

### Axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| coverage (C1) | improved | repeat_info/m_repeatRate files 0 → 1; knowledge/index 69 → 70; 38/38 quotes at pin lines; pins byte-equal upstream |
| operability (C2) | improved | tool absent → present; 18/18 + 8/8 + 24/24 re-run by closure; hold-out commitment equals the frozen sha |
| freshness (C3) | improved | `grep -c P23` 0 → 6; 38 insertions 0 deletions; pin else-arm confirms P23 |
| depth | unchanged | no depth claim |
| calibration | unchanged | no calibration claim; lane's discernment self-verdict "unchanged" is superseded by the outside spot-check below |
| adjacency | unchanged | the lane's adjacency sweep found no sibling holding the keys; nothing absorbed |

No owned axis is evidenced harmed. All three claims verify; admitted.

## 3. Discernment spot-check (LEARNING.md)

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S378 | admit | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/SeatManager.cpp` (fresh `curl`, sha256 `bd748553…` = pin), lines 175-177 | agree | `void CSeatManager::updateActiveKeyboardData() { if (m_keyboard) PROTO::seat->updateRepeatInfo(m_keyboard->m_repeatRate, m_keyboard->m_repeatDelay);` — the lesson's located quote is exact at :177 and the teaches ("handed to the seat protocol ... only when a keyboard is set; no host event asserted") is within it |
| S379 | admit | `…/src/protocols/core/Seat.cpp` (fresh `curl`, sha256 `cc23bb8b…` = pin), lines 441-448 | agree | line 442 holds `m_resource->version() < 4` as one of three OR-joined guard terms, :443 `return;`, :447 `sendRepeatInfo(rate, delayMs);`; the lane's later S381 supersession correctly adds the bind-time route (:350) |
| S380 | admit, narrowly | `…/src/devices/IKeyboard.hpp` (fresh `curl`, sha256 `82e0bc9e…` = pin), lines 119-124 | agree | `m_repeatRate = 0;` :121, `m_repeatDelay = 0;` :122, `m_numlockOn = -1;` :123; the narrowing is right (members only, base class IKeyboard — what S382 states; S363 anchors `:13-22,100-101,124` are disjoint) |
| numlock 0..1 range as a source fact | reject | same ConfigValues.cpp (fresh `curl`, sha256 `a76f0507…` = pin), line 277 | agree | `MS<Bool>("input:numlock_by_default", …, false, {.refresh = …})` has no `.min/.max`, while :279-280 (`repeat_rate`, `repeat_delay`) do; applying 0..1 is a modelling rule, as the tool docstring says |
| K17/E rows as client behaviour | reject | `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml` (sha256 `cc860987…` = pin), lines 2573, 2732-2741, 2752 | agree | the quoted sentence lines are in the XML; the registry anchor `wl_keyboard :2573-2699` ends before `repeat_info` (:2732) so the row supports the protocol statement only, never a client delivery (and the entry records the anchor gap) |
| New `SOURCES.md` row S378 quote (≤25 words) | admit | row 328 and lesson `## Gate` S378 quote re-opened above | agree | the quote `PROTO::seat->updateRepeatInfo(m_keyboard->m_repeatRate, m_keyboard->m_repeatDelay);` is one line and 2 whitespace-separated tokens (≤25 words), located (`Hyprland-SeatManager.cpp:177`); row has 11 cells, status `mined`, opened 2026-10-28, `used-by` the entry |

Census command (step 3): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → `mado ok`, exit 0.

## 4. Trends

- **expansion: improved** — a sourced chain `input:` key → `applyConfigToKeyboard` → stored members → seat → `wl_keyboard.repeat_info` entered on ground with 0 corpus hits for `repeat_info`/`m_repeatRate`; entry cites mined rows S316-S319, S052, S378-S380; a capability row (`mado-kbdopts`) admitted to `SCORECARD.md`; frontier bullets updated.
- **quality: improved** — the false P19 is superseded append-only by P23 (38 insertions / 0 deletions, pin-checked); no admitted entry failed its re-check in the closure's reads. The wave-2 findings the lane disclosed (content-blind counters M55-9, weak mutation kill power M55-11) are real and routed below; they do not make an admitted entry false.
- **discernment: improved** — a non-author re-opened S378, S379, S380 (admits) and the numlock-range and K17 rejections against fresh upstream bytes and agreed on all; the lane's own self-verdict was "unchanged" for lack of any non-author sample at filing, which this spot-check now supplies.

## 5. Routed defects for next round (owner: mado)

1. `corpus/lessons/round-55.md` `## Gate` / census paragraph still say `314 → 317` / `317 rows`; the registry has 319 (S381, S382 added later). Add an appended correction (do not rewrite).
2. M55-9 (content-blind C1/C3 predicates: junk/false entries and a false P23 pass): land the registry-membership/scope check and ordered P23 pattern routed in `SCORECARD.md` "Planned (round 56)".
3. M55-11 / M55-10: raise counter and harness kill power; the harness-sniffing channels (consistent forgery) remain declared limits, not fixed.
4. Frozen-sentence honesty: a future frozen predicate must be satisfiable as literally written (v1 C1 K16 `||`, K17 S052 leg were not); run `freeze-verify` against the counter grammar before the freeze commit, not after wave 1.
5. SHONEN: all four boxes appear checkable by a non-author from existing evidence (SKILL decision tables, round-55 end-to-end task + live read-only run, entry "How to verify", PROVINCE/adjacency sweep); promotion is operator-owned and this closure wrote no `[x]`.
