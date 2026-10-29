# R56RevQuality — round 56, wave w1 — quality review of the frozen contract and draft criterion 107

Report: .ufo/waves/round-56/w1/R56RevQuality.md

Seat: quality reviewer, leaf member, no subagents, no lane edits, no git mutation. Lane tip read: `2aa347b1` (`round-56: wave 1 spec, dispatch, registry`); freeze `3423ae28`; base `13f0acbe`; r55 entry `63f48dc1`. Frozen contract read: `claims-frozen.md` (`#73E2`), `registration.md` (`#53F4`), `frozen-tables.json` (sha256 `d50d2b7b…f9af`, checked by the freeze). The hold-out was not looked for or opened.

## 1. Verdict in brief

- **C1 (coverage, sourced entry):** the counter design binds quotes to exact pin lines and K rows to registry rows, and the frozen counts reproduce; the contract misses QUALITY 17 (duplicate canonical URLs, unreviewed), and its scope leg is K-only so E-rows are unchecked (F3, F4). Entailment (104) is not counted (declared; F8).
- **C2 (operability, capability `tools/mado-watchplan.py`):** the sealed-hold-out design is sound in intent, but the harness layout reopens the M55-4 sibling-read channel and none of its three controls tests it. A 10-line sibling reader scores **18/18 committed fixtures** in the frozen layout (F1). The setter-citation rule (100) and the live-receipt rule (104) are unmet for the central value state and the watch-list capability wording (F5, F7).
- **C3 (calibration, registry back-references):** the counter definitions reproduce the frozen baseline exactly (`entries=70 rows=319 missing=65 extra=0 dangling=0` at `13f0acbe`, `3423ae28` and `2aa347b1`). The axis selection that makes calibration the working axis is not supported by the record: the SCORECARD records a scored calibration rubric and the claims call it unscored, which bears on QUALITY 22 (F2).
- **Draft criterion 107 (M56-1):** written at `criterion.md`, with a prototype checker `check-anchor-cover.py`. On the committed r55 entry it reads `rows=32 covered=25 miss=7 verdict=FAIL`, rc 1 — the two frozen failures K14/K17 plus five E-rows the frozen K-only leg cannot see. Controls: widened anchors read `miss=0` rc 0; shrunk S318 reads `miss=2` rc 1.
- **Process findings:** freeze-before-launch holds (QUALITY 106: `verdict=OK`). The w1 dispatch fails QUALITY 98 (`PROSE-ONLY`, `enforced=0`, rc 1). The M56-1 receipt `scope-replay-r55.txt` has no committed producer (F4).

## 2. Applicable criteria per claim and how the frozen contract satisfies or misses each

Criteria read: 95–106 (`corpus/QUALITY.md` lines 498–588), with 6, 14, 17, 22, 27, 55, 77, 84, 93, 97 and 104 for applicability. Status: **S** satisfied by evidence I checked; **P** partial; **M** missed; **G** gap (the text satisfies it, no evidence yet); **N/A** not applicable at freeze.

### C1 — coverage (sourced entry), `corpus/knowledge/hyprland-config-autoreload-r56.md`

| QUALITY | Why it applies | How the frozen contract satisfies or misses it | Status |
|---|---|---|---|
| 6, 27 | pins and named revision | `c1.commit = efb5099…`, `pin_sha256` for all eight pins, `host_pin_sha256`; `freeze-verify.txt` reports every quote at its line. `man7` is pinned by sha, not commit, which 27 admits. | S |
| 14 | census names missing and extra | `new_rows` names the eight rows S383–S390 and `new_rows=m/8`; the C3 counter names `missing`, `extra`, `dangling` | S |
| 17 | repeated canonical URLs need an explicit distinct-scope review or a supersession row | `source_cell` admits a row whose URL equals an existing row. S384 (K01/K02, `Hyprland-ConfigValues.cpp:492`) must carry the canonical URL of S318 and S215 (`…/src/config/values/ConfigValues.cpp` at `efb5099`), because `source_cell` fixes the URL suffix to `pin_suffix`. `ConfigManager.cpp` duplicates S162 and S317. Nothing in §C1 or the harness reviews this (F3). | M |
| 77, 97 | prose locators resolve to the cited receipt and contain the fact | K-row `pin:line` is exact; locators in the entry body are not read by any frozen leg, so `check-locators.py` is not in the predicate (F9). Registration's own citation `Hyprland-legacy-ConfigManager.cpp:1810-1850` misses the bogus leg at 1803–1805 (F6, C2). | P |
| 55 | counter cribs named, each with a control | the declared limit names the lexical crib (a forged proposition reusing a quote identifier and quote numbers passes); no committed control exercises it (10 controls, none for it) | P |
| 104 | each mechanism sentence within its pinned evidence; word-level claims need checked branches | `tok` and `num` are lexical; entailment is deferred to the wave-2 sentence audit and declared | M (declared) |
| 100 | a host-state claim cites the line that sets the state | K04 (`setWatchList(... getConfigPaths())`) is a set site for the watch list; it satisfies 100 for that state | S |
| 105 | a falsification reproduces the exact grammar | `freeze-verify.txt` shows every frozen quote at its line and free of `|`; each control mutates one leg | S |
| 93 | a gate has a clean-state receipt at the revision it scores | counter not landed; receipt pending | G |
| 95 | a scoring instrument writes only under `--work` and carries a before/after inventory | §C1 says the counter "writes nothing"; no inventory receipt is named in the contract | G |
| 98 | scratch bound enforced by the dispatch | `w1-spec.json` `check100` → `PROSE-ONLY` (F10) | M |
| 106 | freeze strictly before launch | `freeze-order-w1.out`: `freeze_time=2026-10-28T21:19:17-03:00 launch=2026-10-29T00:22:47.615Z verdict=OK`; no freeze file changed after freeze | S |
| 101 | declared deliverables exist | this seat's declarations are in the `Deliverables` list below and `test -f`-proven before yield | S (own report) |

### C2 — operability (capability), `tools/mado-watchplan.py`

| QUALITY | Why it applies | How the frozen contract satisfies or misses it | Status |
|---|---|---|---|
| 55 | harness cribs named, each with a control; M55-4 sibling-read channel | harness exports fixtures beside `expected.out` and runs the tool with cwd = export root (`registration.md` §C2); no private directory (the r55 fix `quality/r55_ctl_c2.py`, absent in the r56 tree); the three controls do not read a sibling. Sibling reader: `committed=18/18` (F1). | M |
| 96 | landed tool not narrower than the frozen out-of-contract list | applies at landing; the tool is absent at `2aa347b1` (`tools/` holds only `mado-kbdopts.py`). The five divergences in §C2 must appear in the docstring as `Out of contract:` / `Also out of contract:` sentences for `check-landed-contract.py` to read. | G |
| 100 | value or watch-list state cites the line that sets it | `misc:disable_autoreload` is set by the hyprlang parser; no pin contains the set site (`configStringToInt` has no hit in `fetch/`). The cited lines are the declaration (`ConfigValues.cpp:492`) and the reader (`ConfigWatcher.cpp:33`). "Last accepted value wins" is therefore uncited (F5). | M |
| 104 | source-level behaviour not promoted to host behaviour without a live receipt | capability row says "predict the inotify watch list Hyprland sets"; the only live join is `disable_autoreload` (`MADO_WATCH_LIVE`). The declared limit states that no event is generated and no reload observed, so the capability row needs that label (F7). | P |
| 77 | cited range contains the fact | `handleSource` cited `1810-1850`; the bogus leg is at 1803–1805 (`receipts/handleSource-pin-lines.txt`) (F6) | M |
| 86 | counter runs the tool where it cannot see the judge; cases drawn from a nonce | hold-out is sealed with a commitment (`holdout_commit_sha256`); the export layout defeats this under F1 unless the tool runs in a private directory | P |
| 84 | counter pins each receipt it reads | commitments pin the fixture trees; `frozen-tables.json` is embedded-sha checked | S |
| 95 | writes only under `--work` | tool "writes nothing" by contract; no inventory receipt named | G |
| 98 | scratch bound enforced by dispatch | as C1 (F10) | M |
| 93 | clean-state receipt at scored revision | tool not landed | G |
| 106 | freeze before launch | as C1 | S |

### C3 — calibration (registry back-references), `corpus/SOURCES.md` cell 11

| QUALITY | Why it applies | How the frozen contract satisfies or misses it | Status |
|---|---|---|---|
| 14 | census names missing and extra | `missing`, `extra`, `dangling` named; controls 1–6 each produce one leg | S |
| 22 | re-derive every active axis under its recorded rule before selecting the lowest; report literal and semantic counters separately | claims call calibration "unscored" with "a counted rubric introduced this round". SCORECARD records a calibration rubric re-derived in every round to round 48: `calibration resolved-active 86/86` at `a582e0e5` (`SCORECARD-13f0acbe.md:2722`), which is 10.0. Freshness is 9.6552 and is the lowest scored sub-axis in the claims. Navigation 10.0 and operability 10.0 are round-12 baselines (`e1d81d4`), not re-derived at the frozen revision (F2). | M |
| 55 | counter cribs and controls | six controls; lexical crib in `CITE`: a citation inside an HTML comment or a negated mention counts as a citation (F12); not named in the contract | P |
| 84 | counter reads only what it pins | reads `SOURCES.md` and `corpus/knowledge/*.md` at `--rev` by blob | S |
| 95 | writes only under `--work` | counter "writes nothing" by contract; no inventory receipt | G |
| 98 | dispatch-enforced scratch | as C1 | M |
| 106 | freeze before launch | as C1 | S |
| 27 / 17 | row anchors, duplicate URLs | C3 edits cell 11 only; no new rows | N/A |

## 3. Findings (ranked by severity)

**F1 — HIGH — C2 sibling-read channel open; the three controls do not test it (M55-4 recurs).** Inputs: `registration.md` §C2 harness: exports the tool and `fixtures/c2`, `fixtures/c2-holdout` into a scratch dir; runs each fixture with `cwd = export root` and `{FX}` replaced by the absolute fixture directory (`args.json` of F01: `["--config","{FX}/tree/hyprland.conf","--display-root","{FX}"]`). `expected.out` sits in that same fixture directory. Test: a 10-line reader that replays `expected.out` beside the fixture named by `--config` (or `--display-root`), run with the same layout by `receipts/run-c2-committed.py`: `tool=sib.py committed=18/18 mismatches=[]` (`receipts/sibling-reader-committed.out`). The controls: `const-host.py` passes one fixture, `empty.py` none, `lookup-committed.py` tests only an `F##` path part; none of them reads a sibling. The r55 fix (`quality/r55_ctl_c2.py`: "a private directory that holds only a copy of the tool and the input files its argv names") is not in the r56 contract. The hold-out, once revealed into the export by the same layout, is expected to be readable the same way [INFERENCE: same layout, not run; the hold-out was not opened]. Because the wave is launched and no C2 score exists yet, the remedy is the rule's: a pre-data re-registration in a new versioned file (private-directory run, as r55), before any C2 scoring.

**F2 — HIGH — axis posture vs the recorded calibration rule (QUALITY 22).** Inputs: `claims-frozen.md` lines 12–16: "calibration, depth and adjacency are unscored … C3 therefore works the least-evidenced axis, **calibration**, with a counted rubric introduced this round." Record at `13f0acbe`: `SCORECARD.md:2722` "Axis table re-derived at `a582e0e5` … calibration resolved-active 86/86"; the round-12 table (`SCORECARD.md:244`) names `calibration / lesson-grounded admission criteria` with a counting command; round-55 closure (`SCORECARD.md:2867`) says "lowest-axis obligation waived" for r55; the window statement ("not elapsed") is the claims' own, lines 12–13. Consequence: if calibration is still 86/86 = 10.0, the lowest scored sub-axis is freshness at 9.6552, and 22 requires the lowest axis to be selected under the recorded rules. The contract's choice of calibration is therefore either a rule the record does not contain or a mis-selection. Also: the claims quote navigation 10.0, operability 10.0 and freshness 9.6552 from the round-12 baseline; none is re-derived at the frozen revision. Not verified here: calibration after round 48 (no later axis line in the SCORECARD) and the current freshness value (I did not run `tools/mado-verify.sh --no-live`). Routing: the owner must re-derive all four under their recorded rules and either move C3 to the lowest axis or record the override.

**F3 — HIGH — C1: duplicate canonical URLs enter without the QUALITY 17 review.** Inputs: `frozen-tables.json` `c1.k`: K01/K02 cite `S384` on `Hyprland-ConfigValues.cpp:492`; the base registry already has `S215` and `S318` with URL `…efb5099…/src/config/values/ConfigValues.cpp` (`receipts/url-duplicates-base.txt`, `receipts/duplicate-url-rows.txt`); `ConfigManager.cpp` is already in `S162` and `S317`. The `source_cell` leg accepts a URL that ends in `pin_suffix` and contains the `rev_rule` token; nothing in §C1 tests for an existing row with the same URL. The lane's precedent is to admit with a `census W04` warning and a distinct-scope note (r55 S380/S363). Recommendation: the wave's rows carry a distinct-scope sentence against S318/S317, with anchors disjoint from those rows, logged in the round lesson, or a supersession row per 17.

**F4 — HIGH — the M56-1 able-to-fail receipt has no producer; the frozen scope leg misses E-rows.** Inputs: `.ufo/waves/round-56/receipts/scope-replay-r55.txt` is three lines (`REPLAY scope leg … K rows 18 scope-failing 2`, K14, K17). `git grep -l scope-failing 2aa347b1` returns only that file; no committed script produces it, so the receipt cannot be reproduced from committed bytes (criterion 76, 93). My replay of the same rule — a prototype `check-anchor-cover.py` at `63f48dc1` — reproduces K14 and K17 (`receipts/anchor-cover-r55-63f48dc1.out`) and additionally fails five E-rows in the same committed entry: E04 (S052, 2732), E05 (S052, 2740), E11 (S052, 2740), E08 (S316 anchor `1213-1295,1350-1383,2119-2131`, line 1195), E14 (S379 anchor `Seat.cpp:441-448,603-609`, line 350). The r55 entry's own registry-gap paragraph (`corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md:148`) names K14, K17, E04, E05, E08 and does not name E11 or E14. The frozen r56 scope leg is K-only (`scope:<id>`, "(K)"), and the r56 row grammar ignores E-rows, so an r56 E-row can carry the same defect undetected. Recommendation: extend the leg to every evidence row with a registry id (the draft criterion 107 does this), or register it in a new versioned file before any r56 scoring.

**F5 — MEDIUM — C2 setter of `misc:disable_autoreload` is uncited (QUALITY 100).** Inputs: `registration.md` §C2 "Model": `misc:disable_autoreload` value parsed by `configStringToInt`; "last accepted value wins". The pins cite the declaration `Hyprland-ConfigValues.cpp:492` and the reader `Hyprland-ConfigWatcher.cpp:33`. `grep -nE 'configStringToInt|disable_autoreload|handleSource' fetch/*.cpp` has no `configStringToInt` hit; the parser lives in the hyprlang library, which is not pinned. The claim is a host-consequence model and needs its set site or an explicit `[INFERENCE]`/`UNKNOWN` label.

**F6 — MEDIUM — registration cites a range that omits the bogus leg (QUALITY 77).** Inputs: `registration.md` §C2 "Source handling": "(legacy `handleSource`, `fetch/Hyprland-legacy-ConfigManager.cpp:1810-1850`)". The pin (`receipts/handleSource-pin-lines.txt`): line 1802 is the signature, 1803–1805 are the `rawpath.length() < 2` → `bogus!` leg that the model's step (1) reproduces. The model is right; the citation does not contain its own fact. The frozen text cannot be edited; disclose, and the wave's report should cite 1802–1850.

**F7 — MEDIUM — C2 capability wording exceeds its live evidence (QUALITY 104).** Inputs: `claims-frozen.md` line 56: capability "predict the inotify watch list Hyprland sets for a config tree". The live join is `misc:disable_autoreload` only (`MADO_WATCH_LIVE`). The contract's own limit says "approximation … no filesystem event is generated and no reload is observed". The SCORECARD capability row should carry that boundary (source-level, option-only live receipt).

**F8 — MEDIUM (declared) — C1 entailment is not counted (QUALITY 104).** `tok` and `num` are lexical. The contract says so (`claims-frozen.md` lines 36–39; `registration.md` §C1 "What the counter proves"). `MADO_AUTORELOAD_ENTRY … TARGET_MET` is quote identity and lexical grounding, not sentence support; the wave-2 audit must carry 104 before any coverage row cites the entry as supported.

**F9 — MEDIUM — prose locators in the C1 entry are unchecked (QUALITY 77, 97).** The `index`, `prov` and row legs read the README row, the header and table rows only. Run `quality/check-locators.py` (criterion 77 instrument) on the entry in wave 2, with the r56 pins as `--fetch`.

**F10 — MEDIUM — the w1 dispatch fails QUALITY 98.** Input: `python3 -I tools/check100.py --spec .ufo/waves/round-56/w1-spec.json` → `PROSE /…/w1-spec.json ceiling=50 MB`, `ceiling=1 MiB`, `CHECK100: sources=1 enforced=0 prose=2 verdict=PROSE-ONLY`, rc 1 (`receipts/check100-w1-spec.out`). The 43 spawn items carry no `ulimit -f` or `RLIMIT_FSIZE`. This seat also ran without a command-level cap; its largest scratch file is under 1 MB (scratch total 2.2 MB, `find -size +1M` empty). The w1 wave is launched, so the remedy is the dispatch's fix for w2.

**F11 — LOW — counters and harnesses lack a before/after inventory receipt (QUALITY 95).** All three contracts say the counter writes nothing. Criterion 95 requires the receipt (`find <scored tree> -newer <marker>` before and after). Add it to each claim's harness output.

**F12 — LOW — C3 `CITE` is lexical (QUALITY 55).** `registration.md` §C3 counts any `S###` token outside fences, including HTML comments and negated mentions. The counter is conservative (more `missing` than semantic), which is safe for `missing` but can count a negated mention as a citation; the contract does not name this crib.

**F13 — AMBIGUITY (frozen text, C1 scope leg).** `registration.md` §C1 `scope:<id>`: "the comma-separated list of `N` or `N-M` locators". Real anchors carry trailing prose: S318 `Hyprland-ConfigValues.cpp:271-279 input kb options, …:296 input scroll_factor`. A whole-item reading (`271-279 input kb options` is not an `N-M` item) would fail K13 at line 279, which is correct. A leading-locator reading passes K13 (my prototype does, `receipts/anchor-cover-r55-63f48dc1.out` line for K13 is OK). The frozen text does not say which; I did not run the whole-item variant [INFERENCE on its result]. A second ambiguity: the leg's basename comes from `pin_suffix`, which exists only for the r56 pins; the r55 K17 pin (`wayland-1.26.0-wayland.xml`) has no mapping, so the replay used some other basename. K17 fails under any basename, because S052's anchor names no `wayland.xml:` at all.

**F14 — AMBIGUITY (frozen text, C2 export layout).** `registration.md` §C2 says the harness exports "into a scratch dir" without fixing the root. `ctl/lookup-committed.py` locates `fixtures/c2` as `Path(__file__).parent.parent / "fixtures/c2"`, which implies `<root>/ctl` and `<root>/fixtures/c2`. A runner that keeps the lane's `.ufo/waves/round-56/` prefix breaks that stub (my first attempt read 0/18 for this reason). The contract should fix the root.

## 4. Registration vs items (reported disagreement check)

I compared the predicate sentences, output formats, leg lists, control counts (10, 3, 6), baselines (65; 70/319) and fixture counts (18 committed, 8 hold-out) in `claims-frozen.md` against `registration.md` §C1–§C3. They agree. The disagreement I did find is between `claims-frozen.md` lines 12–16 (calibration "unscored", "counted rubric introduced this round") and the recorded SCORECARD calibration rule (F2). Registration does not state an axis posture, so no registration-wins rule applies to F2; it is a claims-versus-record disagreement and is reported as such.

## 5. M56-1 review and draft criterion 107

- Fix adequacy: the frozen scope leg fixes K14 and K17 for K rows. It does not cover E-rows (F4), and its able-to-fail receipt has no committed producer (F4).
- Draft: `criterion.md` (criterion 107, check command, shown able to fail, declared limit). Prototype: `check-anchor-cover.py` (this directory; stdlib only; reads git objects at `--rev`; writes only under `--work`).
- Able-to-fail, on committed objects:
  - Real: `63f48dc1`, `rows=32 covered=25 miss=7 verdict=FAIL`, rc 1 (`receipts/anchor-cover-r55-63f48dc1.out`).
  - Positive control, scratch repo with anchors widened: `rows=32 covered=32 miss=0 verdict=OK`, rc 0 (`receipts/anchor-cover-variant-positive.out`).
  - Negative control, S318 shrunk to `271-278`: `rows=32 covered=30 miss=2 verdict=FAIL`, rc 1 (`receipts/anchor-cover-variant-negative.out`).
- Not run: the criterion against the r56 entry (not yet written).

## 6. Sibling-read control result (F1) — details

Runner: `receipts/run-c2-committed.py` (child processes, `python3 -I`, scrubbed env, cwd = export root, stdout bytes and rc compared with `expected.out`/`expected.rc`). Layout: `git archive 3423ae28 .ufo/waves/round-56/fixtures/c2` extracted into a scratch root. Reader: `receipts/sib-reader-crib.py` (reads `Path(--config).parent.parent / "expected.out"`, or the `--display-root` fixture when there is no `--config`). Output: `tool=sib.py committed=18/18 mismatches=[]`. A first run scored 16/18 because my reader resolved symlinks; the fixture `tree/hyprland.conf` is a symlink to `real/main.conf` in F06. That was a bug in my reader, corrected before the result above.

## 7. Not verified / limits

- The frozen counters `quality/counters/c1-r56-…`, `quality/counters/c3-r56-…`, `quality/check-r56-controls.py` and the C2 tool are not in the lane at `2aa347b1`; I did not run them.
- Hold-out: not looked for or opened. F1's hold-out expectation is [INFERENCE].
- Freshness, navigation, operability and calibration were not re-derived; the mado-verify gate was not run (F2 is therefore a record-based finding).
- `check-locators.py` was not run on the r55 entry (F9 is a recommendation).
- Live host: no `hyprctl` command beyond the reads I did not need; no live watch receipt (F7 is textual).
- The criterion-107 prototype is my implementation of the leg; the lane's instrument will need its own clean-state receipt (QUALITY 93).
- The r55 S052 K17 scope claim relies on the anchor text only; I did not inspect the wayland pin (not in the r56 `fetch/`).

## 8. Tooling

No tools installed or upgraded. Used `python3 -I`, `git` (read-only: `cat-file`, `show`, `ls-tree`, `grep`, `archive`, `diff`, `merge-base`), `sed`, `tar`. No pacman, no uv, no npm. The scratch `git init` repo for controls (`work/tmp.eAwUmHrWaC`) was asserted by `git rev-parse --show-toplevel` before each commit; commits used `-c user.name=ctl -c user.email=ctl@ctl`. Nothing was committed to the lane.

## Deliverables

- `criterion.md`
- `check-anchor-cover.py`
- `receipts/commands.txt`
- `receipts/anchor-cover-r55-63f48dc1.out`
- `receipts/anchor-cover-variant-positive.out`
- `receipts/anchor-cover-variant-negative.out`
- `receipts/sibling-reader-committed.out`
- `receipts/sib-reader-crib.py`
- `receipts/run-c2-committed.py`
- `receipts/c3-count.py`
- `receipts/c3-baseline-13f0acbe.out`
- `receipts/c3-baseline-2aa347b1.out`
- `receipts/freeze-order-w1.out`
- `receipts/check100-w1-spec.out`
- `receipts/scorecard-excerpt.txt`
- `receipts/url-duplicates-base.txt`
- `receipts/duplicate-url-rows.txt`
- `receipts/handleSource-pin-lines.txt`
- `receipts/anchor-cover-r55.stderr`
