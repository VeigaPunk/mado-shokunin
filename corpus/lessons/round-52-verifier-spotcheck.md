# Round 52 verifier spot-check — hyaku closure (non-author integrator)

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-27
lane: mado (round 52, hyaku run 10 attempt 1)
lane tip: `56d6e705bf9113dce0dabd5d4a7ed8e610e1a940`; base `85d57a818c3707397e21c840b6498b105ba798aa`
report: fleet `.ufo/reports/round-52/mado.md` (lane-authored commit `9d759e6f6f06d965b2d05988436235abb4f9d9ab`)

Dispatch/complete digest (`.ufo/watchdog.log`, mutable — copied per closure duty):
- 2026-10-27T09:15:52-03:00 launch mado round=52 pgid=3348186 driver=hyaku-inline attempt=1
- 2026-10-27T11:45:30-03:00 complete mado round=52; hyaku-inline attempt=1

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-52/mado.md` | `mado-shokunin mado@shokunin.local 9d759e6f6f06d965b2d05988436235abb4f9d9ab` | PASS |
| SHONEN heading + one line per box | `grep -c '^## SHONEN'` → 1; section read | 4 `[~]` lines with resolvable pointers, one per canonical box | PASS |
| Cited commits exist, ancestor of branch | `git merge-base --is-ancestor 56d6e70 master` and same for `85d57a8` | both pass (branch tested, not `@{u}`; lane is jj-colocated, HEAD detached) | PASS |
| Lane clean and pushed | `jj-lane.sh state`; `git status --porcelain` | `branch=master local=remote=56d6e705bf9113dce0dabd5d4a7ed8e610e1a940 ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty | PASS |
| Prompt carries template contract | read `.ufo/prompts/mado-round-52.md` §§1–5, §6 addendum | mission/axes, 1–3 falsifiable claims, frontier step + census command, L2 floor, report path/order, commit-before-report ("report lands last and cites the pushed lane hash"), SHONEN heading, hash citation rule, write scope, addendum dispatch mechanics | PASS; prompt itself committed (`bf5a7a5b4c3b63f03843561992bb6c161663c6ce`) |
| Dispatch/complete evidence | `grep -E 'launch\|complete mado round=52' .ufo/watchdog.log` | both lines match the digest above; no `lane-dead-no-report` for r52 | PASS |
| Substantive report | report sections read | Work performed / Landed changes / Before→after / Sources & frontier / Trend verdicts / SHONEN all present with evidence pointers and the landed hash; not a marker | PASS |

## 2. Per-claim re-check

### C1 — operability, instrument-ledger accountability check (PRED frozen in `.ufo/waves/round-52/claims-frozen.md`)

- Before, re-measured by closure: extracted `quality/counters/c1-r51-ledger.py` at base into scratch and ran `python3 -I c1-r51-ledger.py --repo <lane> --rev 85d57a818c3707397e21c840b6498b105ba798aa --work /fast/scratch/hyaku/mado-r52-closure/c1` → `population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=85d57a8…`, exit 0 — byte-identical fields to the committed receipt `.ufo/waves/round-52/receipts/c1-base.txt`. As the report states, this r51 predicate is not the C1-r52 predicate (context-blind).
- After, at `56d6e705bf9113dce0dabd5d4a7ed8e610e1a940`: `git diff 85d57a8 56d6e70 --name-only -- quality/ tools/ scripts/` → **empty**; `git ls-tree -r --name-only 56d6e70 quality/counters/ | grep -i r52` → 0 rows. No C1 counter was committed; no valid final-tip C1 measurement exists.
- Falsification evidence, verified (committed W2 seat reports, not re-executed): `w2/Attack01.md` reproduces the forged-description bypass on the W1 draft (F-all: 82/82 rows `generic_desc=0 TARGET_MET`) and on the uncommitted landed rewrite; `w2/Attack02.md` reproduces nine self-pointer laundering spellings passing `TARGET_MET` (P03–P09, P19–P21, incl. symlink mode-120000 alias P09), with pre-registered predictions all matched.
- **C1 verdict: unprovable (honest stop).** Before re-measured; after-state evidence-verified by absence of any committed counter plus the committed falsification reports. Matches the report.

### C2 — coverage, proposition-bound Hyprland dispatcher source entry

- Before, re-measured by closure: ran the r51 counter `python3 -I c2-r51-dispatch-entry.py --repo <lane> --rev 85d57a8…` (TMPDIR redirected) → `clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET`, `body_shingles=3364 files=66+cand3 max=0.1%` — field-identical to committed `receipts/c2-base.txt`. As the report states, it scores the r51 entry, not a C2-r52 baseline (the r52 slug was absent at base).
- After, at `56d6e70`: the candidate entry `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`, index row (`corpus/README.md:80`), rows S370–S373, and `fetch/` bytes are committed; no C2-r52 counter is committed. No valid final-tip counter pass exists.
- Entailment spot re-measurement by closure against committed `fetch/` bytes (SHA256SUMS all OK, `sha256sum -c` exit 0): all 18 quotes ≤25 words (max 19, whitespace-split); 17/18 verbatim whitespace-collapsed in their pinned file; **P16 fails** — the space-joined quote `sendKeyboardMods(modMask, 0, 0, 0); sendKeyboardKey(…)` occurs nowhere contiguously in `Hyprland-ConfigActions.cpp` (the calls sit at :1554 and :1558 with `if (S.m_passPressed == 1) { if (!isMouse)` elided); **P17 misattributes** the repeat logic at :619–622 to `sendshortcut`, but `sendshortcut` spans :531–589 and the pin is inside `sendkeystate` (:591–627); **P18 mislocalizes** the `:574` error return as "inside the scan" (loop closes :571). All three reproduce `w2/Attack07.md` findings A09/A11/A12 exactly.
- Counter-shape evidence verified from `w2/Attack07.md` (executed by the seat on scratch fixtures): landed counter regex expects `| P## | S### | …` while the entry table is `| P## | Proposition | S### | …` → `props=0 TARGET_MISSED` (T1); fabricated quotes at real pins pass `TARGET_MET` (T6, quote binding name-only).
- **C2 verdict: unprovable (honest stop).** Before re-measured; after-state evidence-verified: entry and rows landed, but no counter pass exists at tip and the proposition map fails source-truth on P16–P18. Matches the report.

### Axis verdicts / scorecard harm check

| Axis | Verdict | Evidence |
|---|---|---|
| operability (C1) | unprovable | Falsified draft, no committed counter at tip, honest stop. Base inventory re-verified 82/82 TARGET_MET. |
| coverage (C2) | unprovable | New sourced ground landed but admission counter never passed; P16–P18 fail quote entailment; candidate not admitted. |
| depth / freshness / calibration / adjacency | unchanged | `git diff 85d57a8 56d6e70 -- SCORECARD.md` appends the round-52 honest-stop record only; no inherited axis row, capability, or score changed; assimilation none; no cross-domain write (diff outside `.ufo/waves/round-52/` touches only LOG.md, SCORECARD.md, corpus README/SOURCES + the two new corpus files). |

No owned axis is harmed on the scorecard surface; the two declared axis-moves are `unprovable`.

## 3. Discernment spot-check (LEARNING.md; outside the lane)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| Admit S370 (`DispatcherTranslator.cpp` @ efb5099, tier A, scope `sendshortcut`/`sendkeystate` parsing) | admit (row landed `mined`, used-by the r52 entry) | committed `.ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp` (SHA256 verified); quote cells P01–P06, P08–P11 re-checked verbatim and ≤25 words | agree | Row is source-accurate at the pinned revision for the parser-boundary/key-resolution scope; fetch checksums OK; census exit 0. Residual: row reuses the S365 URL — W04 duplicate-scope warning; QUALITY 17 distinct-scope review still owed (lane-reported unresolved). |
| Reject the C1 accountability counter (draft + landed rewrite) | reject — not committed, claim stopped | `w2/Attack01.md` (forged-phrase bypass to 82/82; landed bytes also break the green clause, red-signal clause, selftest), `w2/Attack02.md` (nine laundering spellings green; predictions pre-registered, all matched) | agree | Both attacks are concrete, reproduced, and their predictions matched; keeping the counter out of `quality/counters/` is the correct gate call. The honest-stop report matches the evidence. |

Newly written `SOURCES.md` row quote check (S370 family): the row's grounding quotes live in the entry's proposition map; all ≤25 words (max 19), 17/18 verbatim at pins, P16 spliced — disagree with the entry text as written, agree with the lane's own Attack07 verdict; the lane did not admit the entry, so the registry row itself stands but the entry needs P16–P18 repair or per-row marking next round.

Census re-run by closure: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → exit 0, `mado ok`; rows 306→310 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at base vs tip re-derived by closure); W04 warnings now include S370/S371/S373 duplicate URLs, as reported.

## 4. Trend verdicts (closure-graded)

- **expansion: unprovable-but-better.** New sourced ground is real (four tier-A rows, fetch bytes checksum-verified, 15/18 propositions quote-entailed), and a new index route landed (knowledge 67→68, re-derived); but C2 admission failed its frozen counter/source-truth criterion, so no admitted expansion credit. Matches the report.
- **quality: harmed.** P16 (spliced quote), P17 (false subject), P18 (false localization) remain in the committed, indexed knowledge entry unmarked at entry level; the defects are recorded only in M52-1 and the W2 seat report. LEARNING.md grades this harmed: a false entry was found and left unmarked where a reader consumes it. The lane's own trend verdict (harmed) agrees.
- **discernment: unprovable-but-better.** The outside sample above agrees with both sampled gate decisions (admit S370; reject the C1 counter), and the lane's falsification wave behaved well (pre-registered predictions, exact reproductions, honest stop). But within-round the gate records are incomplete (see defects) and the W2 seats are lane-dispatched, so no in-round non-author discernment credit exists; my sample lands at closure.

## 5. Routed defects / next-round queue (route to mado round 53)

1. `corpus/lessons/round-52.md` `## Gate` carries no per-row records for S370–S373: CORPUS.md SOURCES contract rule 1 requires the lesson's Gate to record, for every new row, the URL, access date, and a ≤25-word located quote grounding `teaches`. The section contains only the instruction to do so. Append the four records (new entry, never rewrite).
2. Same lesson, `## Changes` reads "Pending final integration revisions and receipts" — stale against the landed state (changes did land at `56d6e70`); correct in the next lesson/entry per append-only discipline.
3. QUALITY 17 distinct-scope review for the reused URLs S370≡S365, S371≡S367, S373≡S364 is still owed; W04 is a warning, not the review. Record the verdict.
4. `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` P16–P18: repair the spliced quote (contiguous excerpt or per-clause rows), re-attribute P17 to `sendkeystate`, re-scope P18, or mark the entry superseded — until then the entry must not be cited as admitted ground.
5. Conformance note for the operator: all four SHONEN boxes remain `[~]` with historical pointers; none gained a new non-author verifier this round, and promotion is operator-owned.

## Closure summary

Status `ok` (substantive lane-authored report; conformance clean). Claims: C1 unprovable, C2 unprovable — neither admitted; quality trend harmed. Verdict: **rejected-honest-stop**, admitted=false. Lane work and wave evidence are committed and pushed (`ahead=0`); no uncommitted round work; no SHONEN box was written by this closure; no promotion or mint action taken.
