# Ledger rows — mado round 51 w1, C1 tool-ledger prose and pointer provenance

Seat: `ScrLedgerRows` (leaf). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Measured revision: `3ac316426497e8649bffedc88d28241d9bc71c52`; round base `6ca8c559a4a3d6d361101592116eea2bc7452437`.
Rebuild with `python3 -I build-ledger-rows.py --repo <lane> --rev <rev>` (read-only, no scratch).
This file is a draft for the tracked `quality/tool-ledger.md`; it is not that file.

## 1. Population and method

Population: every file under `tools/`, immediate children `quality/*.py` and immediate children
`quality/counters/*.py` at `3ac316426497e8649bffedc88d28241d9bc71c52`, de-duplicated — **79 distinct files** (`tools/` 17,
`quality/*.py` 18, `quality/counters/*.py` 44). See finding F1 for why the reading is pinned
this way: a git pathspec for `quality/*.py` recurses into `counters/`, a Python glob does not.

Method, all read-only over git objects:

1. Description: this seat's ≤20-word rewrite of each file's own module docstring first line
   (`tools/mado-verify.sh`: its script header). No behaviour was executed to write a description.
2. Pointer: `git grep -n -F <basename>` at `3ac316426497e8649bffedc88d28241d9bc71c52`, self-hits excluded, ranked by
   the priority `PROVINCE.md` → `SCORECARD.md` capability block → `corpus/knowledge/**`
   → `corpus/lessons/**` → `corpus/QUALITY.md` → sibling population file (successor re-registration)
   → `SCORECARD.md` non-capability row → any other tracked file.
3. Verification: each pointer line is re-read at the revision and must contain the basename;
   the script exits non-zero otherwise (0 failures at `3ac316426497e8649bffedc88d28241d9bc71c52`).

Class counts: `lesson-named` 27, `scorecard-capability` 20, `province-table` 20, `successor-named` 5, `scorecard-row` 4, `quality-named` 3

Distinct pointer files: 25.

## 2. Class legend

| class | meaning |
|---|---|
| `province-table` | `PROVINCE.md` names the file — inventory table cell or a dated refinement paragraph |
| `scorecard-capability` | `SCORECARD.md` names the file inside a `Capabilities` / `Demonstrated capability` table |
| `knowledge-named` | a `corpus/knowledge/*.md` entry names the file |
| `lesson-named` | a `corpus/lessons/*.md` file names the file, usually in a defect or spot-check sentence |
| `quality-named` | `corpus/QUALITY.md` criterion text names the file — criterion body, not a register |
| `successor-named` | only a later population file names it, as the frozen predecessor it re-registers |
| `scorecard-row` | only a non-capability `SCORECARD.md` row (move log / claim result) names it |
| `wave-artifact` | only a `.ufo/waves/**` file names it |
| `GAP` | no tracked file names it |

## 3. Rows (79; one row per population file)

| # | file | one-line description | class | accountability pointer |
|---|---|---|---|---|
| 1 | `quality/check-axis-scores.py` | Calibration gate: the lane's published axis table must not be stale. | scorecard-capability | `SCORECARD.md:2087` |
| 2 | `quality/check-control-receipts.py` | QUALITY 36 successor: a round's control receipts are committed before its data commit. | lesson-named | `corpus/lessons/round-25-verifier-spotcheck.md:135` |
| 3 | `quality/check-counter-discrimination.py` | Counter-discrimination gate: can the lane's own counters tell work from shape, per frozen manifest. | province-table | `PROVINCE.md:61` |
| 4 | `quality/check-deliverables.py` | QUALITY 101 seat prototype: every deliverable a seat declares exists at the cited revision. | quality-named | `corpus/QUALITY.md:566` |
| 5 | `quality/check-evidence-pointers.py` | Evidence-pointer durability gate: every pointer in the lane's own records must resolve. | province-table | `PROVINCE.md:64` |
| 6 | `quality/check-index-rows.py` | Index-row fidelity gate: scores each coverage-map row's shape at a revision or tree. | scorecard-capability | `SCORECARD.md:2046` |
| 7 | `quality/check-index.py` | Index-completeness gate: coverage-map rows against corpus/knowledge, reporting missing, dangling and duplicate rows. | scorecard-capability | `SCORECARD.md:1932` |
| 8 | `quality/check-landed-contract.py` | QUALITY 96 gate: a landed contract is not narrower than, nor silently different from, the frozen reference. | lesson-named | `corpus/lessons/round-48.md:153` |
| 9 | `quality/check-locators.py` | Recomputes prose source locators against pinned receipts; cited lines must carry the attached fragment's identifiers. | lesson-named | `corpus/lessons/round-43-verifier-spotcheck.md:108` |
| 10 | `quality/check-population.py` | QUALITY 37 check: registered predicate metrics must agree with each receipt's metrics and population. | lesson-named | `corpus/lessons/round-26-verifier-spotcheck.md:143` |
| 11 | `quality/check-r38-discrimination.py` | Round-38 discrimination gate: do the v3 counters tell work from crib? | lesson-named | `corpus/lessons/round-38.md:8` |
| 12 | `quality/check-round-outcome-first.py` | QUALITY 99 check: a round's SCORECARD closure leads with the round-level outcome, not counter bookkeeping. | lesson-named | `corpus/lessons/round-48.md:153` |
| 13 | `quality/check-session-material.py` | Privacy gate for committed receipts: detects session-material shapes in evidence files. | province-table | `PROVINCE.md:100` |
| 14 | `quality/check-state-cite.py` | QUALITY 100 seat prototype: a host-state claim cites the source line that sets that state. | quality-named | `corpus/QUALITY.md:560` |
| 15 | `quality/check-wave-done.py` | Wave settlement check: did every dispatched seat of a round reach WAVE-DONE from committed artifacts? | scorecard-capability | `SCORECARD.md:2763` |
| 16 | `quality/counter-selftest.py` | Round-27 suite A: behavioural gate over the two round-26 counters, harness surfaces replaced with synthetic fakes. | lesson-named | `corpus/lessons/round-26-verifier-spotcheck.md:142` |
| 17 | `quality/counters/c1-idle-lock.py` | PRED-C1-r36-v1: the round-35 idle-lock admission counter, repaired. | province-table | `PROVINCE.md:56` |
| 18 | `quality/counters/c1-r37-event-ground.py` | PRED-C1-r37-v2 counter: event-socket delivery ground admitted into the corpus, scored at one revision. | lesson-named | `corpus/lessons/round-37.md:10` |
| 19 | `quality/counters/c1-r38-event-ground.py` | PRED-C1-r38-v3: event-socket delivery ground admitted into the corpus, third revision. | lesson-named | `corpus/lessons/round-38-verifier-spotcheck.md:32` |
| 20 | `quality/counters/c1-r40-live-v2.py` | PRED-C1-r40-v2: the option table merges a live compositor in its native forms. | lesson-named | `corpus/lessons/round-40-verifier-spotcheck.md:31` |
| 21 | `quality/counters/c1-r40-live.py` | PRED-C1-r40-v1: the option table merges a live compositor in its native forms; superseded by v2. | successor-named | `quality/counters/c1-r40-live-v2.py:4` |
| 22 | `quality/counters/c1-r41-globals-v2.py` | PRED-C1-r41-v2: read-only census of the compositor's advertised Wayland globals, re-registered. | scorecard-capability | `SCORECARD.md:2515` |
| 23 | `quality/counters/c1-r41-globals.py` | PRED-C1-r41-v1: read-only census of the compositor's advertised Wayland globals; superseded by v2. | quality-named | `corpus/QUALITY.md:393` |
| 24 | `quality/counters/c1-r42-geometry.py` | PRED-C1-r42: read-only join of window-rule sizes with the compositor's reported client sizes. | scorecard-capability | `SCORECARD.md:2544` |
| 25 | `quality/counters/c1-r44-geometry-states-v2.py` | PRED-C1-r44-v2: mado-geometry names maximized and fullscreen clients instead of comparing their sizes. | scorecard-capability | `SCORECARD.md:2579` |
| 26 | `quality/counters/c1-r44-geometry-states.py` | PRED-C1-r44: mado-geometry reports maximized and fullscreen clients as such; superseded by v2. | successor-named | `quality/counters/c1-r44-geometry-states-v2.py:5` |
| 27 | `quality/counters/c1-r45-monitors-v2.py` | PRED-C1-r45-v2: mado-monitors joins monitor rules with live output state, importing v1's fixtures. | scorecard-capability | `SCORECARD.md:2611` |
| 28 | `quality/counters/c1-r45-monitors.py` | PRED-C1-r45: mado-monitors joins monitor rules with live output state; superseded by v2. | successor-named | `quality/counters/c1-r45-monitors-v2.py:5` |
| 29 | `quality/counters/c1-r46-devices-v2.py` | PRED-C1-r46-v2: the input-device join, re-registered before data against a corrected reference contract. | province-table | `PROVINCE.md:109` |
| 30 | `quality/counters/c1-r46-devices-v3.py` | PRED-C1-r46-v3: same input-device join, sandboxed under bubblewrap with a socket tripwire. | province-table | `PROVINCE.md:109` |
| 31 | `quality/counters/c1-r46-devices.py` | PRED-C1-r46: mado-devices joins input/device config with live keyboard and mouse state; v1, superseded. | province-table | `PROVINCE.md:108` |
| 32 | `quality/counters/c1-r47-terminal.py` | PRED-C1-r47: mado-terminal answers which terminal xdg-terminal-exec picks, scored against fixtures. | scorecard-capability | `SCORECARD.md:2669` |
| 33 | `quality/counters/c1-r48-terminal-cache-v2.py` | PRED-C1-r48-v2: predicts terminal selection including the warm xdg-terminal-exec cache, re-registered. | scorecard-capability | `SCORECARD.md:2716` |
| 34 | `quality/counters/c1-r48-terminal-cache.py` | PRED-C1-r48: predicts terminal selection including the warm cache; superseded by v2. | lesson-named | `corpus/lessons/round-48.md:153` |
| 35 | `quality/counters/c1-r49-keysym.py` | PRED-C1-r49: mado-keysym predicts xkbcli how-to-type output for a keysym under a compiled keymap. | scorecard-capability | `SCORECARD.md:2743` |
| 36 | `quality/counters/c1-r50-bind-entry.py` | PRED-C1-r50: the Hyprland bind-key-match knowledge entry is admitted, scored at one revision. | scorecard-row | `SCORECARD.md:2754` |
| 37 | `quality/counters/c2-ledger.py` | PRED-C2-r36-v1: the lane's evidence ledger predicate, repaired against its own fail-opens. | province-table | `PROVINCE.md:59` |
| 38 | `quality/counters/c2-r37-eventq.py` | PRED-C2-r37-v2: the event-socket subscriber census runs and discriminates work from crib. | scorecard-capability | `SCORECARD.md:2385` |
| 39 | `quality/counters/c2-r38-eventq.py` | PRED-C2-r38-v3: the event-socket subscriber census predicate, third revision, running and discriminating. | lesson-named | `corpus/lessons/round-38-verifier-spotcheck.md:42` |
| 40 | `quality/counters/c2-r38-request-ground.py` | PRED-C2-r38-v1: request-socket contract ground admitted into the corpus. | scorecard-capability | `SCORECARD.md:2416` |
| 41 | `quality/counters/c2-r40-forms-entry-v2.py` | PRED-C2-r40-v2: the getoption native-forms knowledge entry is admitted, re-registered. | lesson-named | `corpus/lessons/round-40-verifier-spotcheck.md:34` |
| 42 | `quality/counters/c2-r40-forms-entry.py` | PRED-C2-r40-v1: the getoption native-forms entry is admitted; superseded by v2. | successor-named | `quality/counters/c2-r40-forms-entry-v2.py:4` |
| 43 | `quality/counters/c2-r41-focus-entry-v2.py` | PRED-C2-r41-v2: the Hyprland focus-grab entry admission predicate, re-registered. | lesson-named | `corpus/lessons/round-41-verifier-spotcheck.md:25` |
| 44 | `quality/counters/c2-r41-focus-entry.py` | PRED-C2-r41-v1: the Hyprland focus-grab entry is admitted; superseded by v2. | lesson-named | `corpus/lessons/round-41.md:128` |
| 45 | `quality/counters/c2-r42-gkeep-entry.py` | PRED-C2-r42: the Hyprland gkeep-geometry entry is admitted, sourced. | lesson-named | `corpus/lessons/round-44.md:180` |
| 46 | `quality/counters/c2-r43-gkeep-entry-v2.py` | PRED-C2-r43-v2: gkeep-geometry entry admission, second revision. | lesson-named | `corpus/lessons/round-43.md:254` |
| 47 | `quality/counters/c2-r43-gkeep-entry.py` | PRED-C2-r43: gkeep-geometry entry admission; superseded by v2. | lesson-named | `corpus/lessons/round-43.md:150` |
| 48 | `quality/counters/c2-r44-gkeep-size-request-v2.py` | PRED-C2-r44-v2: the gkeep size-request entry is admitted, with assimilation clause. | lesson-named | `corpus/lessons/round-44-verifier-spotcheck.md:12` |
| 49 | `quality/counters/c2-r44-gkeep-size-request.py` | PRED-C2-r44: the gkeep size-request entry is admitted; superseded by v2. | lesson-named | `corpus/lessons/round-44.md:179` |
| 50 | `quality/counters/c2-r45-monitor-entry-v2.py` | PRED-C2-r45-v2: the monitor-rule entry is admitted, re-registered. | lesson-named | `corpus/lessons/round-45-verifier-spotcheck.md:13` |
| 51 | `quality/counters/c2-r45-monitor-entry.py` | PRED-C2-r45: the monitor-rule entry is admitted; superseded by v2. | successor-named | `quality/counters/c2-r45-monitor-entry-v2.py:5` |
| 52 | `quality/counters/c2-r46-input-device-entry-v2.py` | PRED-C2-r46-v2: the input-device entry is admitted, re-registered. | lesson-named | `corpus/lessons/round-46-verifier-spotcheck.md:13` |
| 53 | `quality/counters/c2-r46-input-device-entry.py` | PRED-C2-r46: the input-device entry is admitted, sourced. | province-table | `PROVINCE.md:111` |
| 54 | `quality/counters/c2-r47-terminal-entry.py` | PRED-C2-r47: the terminal-selection entry is admitted, sourced. | lesson-named | `corpus/lessons/round-47.md:200` |
| 55 | `quality/counters/c2-r48-xkb-entry-v2.py` | PRED-C2-r48-v2: the XKB-compile entry is admitted, re-registered. | lesson-named | `corpus/lessons/round-48.md:153` |
| 56 | `quality/counters/c2-r48-xkb-entry.py` | PRED-C2-r48: the XKB-compile entry is admitted; superseded by v2. | lesson-named | `corpus/lessons/round-48.md:153` |
| 57 | `quality/counters/c2-r49-bind-entry.py` | PRED-C2-r49: the Hyprland bind-key-match entry is admitted, sourced. | scorecard-row | `SCORECARD.md:2737` |
| 58 | `quality/counters/c2-r50-session-gate.py` | PRED-C2-r50: the session-material gate detects the shapes it covers. | scorecard-row | `SCORECARD.md:2755` |
| 59 | `quality/counters/c3-r39-options.py` | PRED-C3-r39-v2: the option-ownership tool resolves config trees it has never seen. | scorecard-capability | `SCORECARD.md:2454` |
| 60 | `quality/counters/c4-r39-options-entry.py` | PRED-C4-r39-v1: the config-option ownership ground is admitted. | lesson-named | `corpus/lessons/round-39-verifier-spotcheck.md:28` |
| 61 | `quality/population-suite.py` | Offline gate over the round-26 population checker, exercising it against a built-in fixture set. | scorecard-row | `SCORECARD.md:1767` |
| 62 | `quality/ratio-domain-meta.py` | Re-runnable domain-versus-meta count over SCORECARD claim rows. | lesson-named | `corpus/lessons/round-44.md:251` |
| 63 | `tools/mado-action-plan.py` | Fail-closed static safety gate over a declared action plan and policy; never executes the supplied argv. | province-table | `PROVINCE.md:24` |
| 64 | `tools/mado-anims.py` | Static resolver for the animation table a Hyprland v0.56.2 config tree builds; stdout only, no socket. | province-table | `PROVINCE.md:30` |
| 65 | `tools/mado-assessment.py` | Read-only artifact assertion gate over an assessment bundle; not independent authentication of its author. | province-table | `PROVINCE.md:26` |
| 66 | `tools/mado-binds.py` | Static resolver for the bind table a Hyprland v0.56.2 config tree builds, from config bytes only. | province-table | `PROVINCE.md:29` |
| 67 | `tools/mado-devices.py` | Joins declared input/device config with a hyprctl devices dump: keyboard XKB names and mouse scroll factors. | province-table | `PROVINCE.md:105` |
| 68 | `tools/mado-eventq.py` | Read-only census of Hyprland event-socket (socket2) subscribers, their unread bytes and removal markers. | scorecard-capability | `SCORECARD.md:2385` |
| 69 | `tools/mado-evidence-audit.py` | Audits artifact arithmetic and explicit evidence labels; never execution truth, chronology or promotion. | province-table | `PROVINCE.md:27` |
| 70 | `tools/mado-geometry.py` | Joins window-rule sizes with a hyprctl clients dump: does the reported size match the rule? | province-table | `PROVINCE.md:32` |
| 71 | `tools/mado-globals.py` | Read-only census of the Wayland globals the compositor advertised, from a journal file or one allowlisted run. | province-table | `PROVINCE.md:31` |
| 72 | `tools/mado-hostguard.py` | Runs a command against a scratch HOME and fails if a declared operator-owned path changed. | scorecard-capability | `SCORECARD.md:2762` |
| 73 | `tools/mado-keysym.py` | Predicts which key and modifiers type a keysym under a compiled keymap, from xkbcli output. | scorecard-capability | `SCORECARD.md:2743` |
| 74 | `tools/mado-monitors.py` | Joins monitor rules with a hyprctl monitors dump: mode, position, scale and transform per output. | province-table | `PROVINCE.md:100` |
| 75 | `tools/mado-options.py` | Static resolver of a config tree's option table, attributing each key to its last declarer. | scorecard-capability | `SCORECARD.md:2454` |
| 76 | `tools/mado-terminal.py` | Predicts which terminal xdg-terminal-exec picks on this host, and why, without running it. | scorecard-capability | `SCORECARD.md:2669` |
| 77 | `tools/mado-tripwire.py` | Post-hoc tripwire over OMP session transcripts (JSONL), reporting issued commands as lane-local evidence. | province-table | `PROVINCE.md:25` |
| 78 | `tools/mado-verify.sh` | Config-plane verdict gate: declared planes versus live bytes and hyprctl read verbs, exit 0/1/2. | province-table | `PROVINCE.md:28` |
| 79 | `tools/mado-wsrules.py` | Static workspace-rule table from config bytes, mirroring hyprctl workspacerules -j for v0.56.2. | scorecard-capability | `SCORECARD.md:1789` |

## 4. Gap list

**Strict gap (no tracked file names the file): 0 of 79.**
Every population file is named by at least one tracked file, so under the frozen `bad_pointer`
test every row has a satisfiable pointer.

**Accountability gaps** — rows whose only naming file is not an accountability surface, by class:

`lesson-named` (27 rows):

- `quality/check-control-receipts.py` → `corpus/lessons/round-25-verifier-spotcheck.md:135`
- `quality/check-landed-contract.py` → `corpus/lessons/round-48.md:153`
- `quality/check-locators.py` → `corpus/lessons/round-43-verifier-spotcheck.md:108`
- `quality/check-population.py` → `corpus/lessons/round-26-verifier-spotcheck.md:143`
- `quality/check-r38-discrimination.py` → `corpus/lessons/round-38.md:8`
- `quality/check-round-outcome-first.py` → `corpus/lessons/round-48.md:153`
- `quality/counter-selftest.py` → `corpus/lessons/round-26-verifier-spotcheck.md:142`
- `quality/counters/c1-r37-event-ground.py` → `corpus/lessons/round-37.md:10`
- `quality/counters/c1-r38-event-ground.py` → `corpus/lessons/round-38-verifier-spotcheck.md:32`
- `quality/counters/c1-r40-live-v2.py` → `corpus/lessons/round-40-verifier-spotcheck.md:31`
- `quality/counters/c1-r48-terminal-cache.py` → `corpus/lessons/round-48.md:153`
- `quality/counters/c2-r38-eventq.py` → `corpus/lessons/round-38-verifier-spotcheck.md:42`
- `quality/counters/c2-r40-forms-entry-v2.py` → `corpus/lessons/round-40-verifier-spotcheck.md:34`
- `quality/counters/c2-r41-focus-entry-v2.py` → `corpus/lessons/round-41-verifier-spotcheck.md:25`
- `quality/counters/c2-r41-focus-entry.py` → `corpus/lessons/round-41.md:128`
- `quality/counters/c2-r42-gkeep-entry.py` → `corpus/lessons/round-44.md:180`
- `quality/counters/c2-r43-gkeep-entry-v2.py` → `corpus/lessons/round-43.md:254`
- `quality/counters/c2-r43-gkeep-entry.py` → `corpus/lessons/round-43.md:150`
- `quality/counters/c2-r44-gkeep-size-request-v2.py` → `corpus/lessons/round-44-verifier-spotcheck.md:12`
- `quality/counters/c2-r44-gkeep-size-request.py` → `corpus/lessons/round-44.md:179`
- `quality/counters/c2-r45-monitor-entry-v2.py` → `corpus/lessons/round-45-verifier-spotcheck.md:13`
- `quality/counters/c2-r46-input-device-entry-v2.py` → `corpus/lessons/round-46-verifier-spotcheck.md:13`
- `quality/counters/c2-r47-terminal-entry.py` → `corpus/lessons/round-47.md:200`
- `quality/counters/c2-r48-xkb-entry-v2.py` → `corpus/lessons/round-48.md:153`
- `quality/counters/c2-r48-xkb-entry.py` → `corpus/lessons/round-48.md:153`
- `quality/counters/c4-r39-options-entry.py` → `corpus/lessons/round-39-verifier-spotcheck.md:28`
- `quality/ratio-domain-meta.py` → `corpus/lessons/round-44.md:251`

`successor-named` (5 rows):

- `quality/counters/c1-r40-live.py` → `quality/counters/c1-r40-live-v2.py:4`
- `quality/counters/c1-r44-geometry-states.py` → `quality/counters/c1-r44-geometry-states-v2.py:5`
- `quality/counters/c1-r45-monitors.py` → `quality/counters/c1-r45-monitors-v2.py:5`
- `quality/counters/c2-r40-forms-entry.py` → `quality/counters/c2-r40-forms-entry-v2.py:4`
- `quality/counters/c2-r45-monitor-entry.py` → `quality/counters/c2-r45-monitor-entry-v2.py:5`

`scorecard-row` (4 rows):

- `quality/counters/c1-r50-bind-entry.py` → `SCORECARD.md:2754`
- `quality/counters/c2-r49-bind-entry.py` → `SCORECARD.md:2737`
- `quality/counters/c2-r50-session-gate.py` → `SCORECARD.md:2755`
- `quality/population-suite.py` → `SCORECARD.md:1767`

`quality-named` (3 rows):

- `quality/check-deliverables.py` → `corpus/QUALITY.md:566`
- `quality/check-state-cite.py` → `corpus/QUALITY.md:560`
- `quality/counters/c1-r41-globals.py` → `corpus/QUALITY.md:393`

`wave-artifact` (0 rows):


Rows with no `province-table` naming at all: **59 of 79**.
`tools/mado-hostguard.py` and `tools/mado-keysym.py` — the two the round-50 wave-seat ledger
missed — are covered here by `SCORECARD.md` capability rows, not by a PROVINCE row.

## 5. Pending rows (absent at the measured revision)

Population files this round adds, absent at `3ac316426497e8649bffedc88d28241d9bc71c52`; each needs a durable pointer once landed:

- `quality/check-tool-ledger.py` — C1 checker over this ledger: population coverage, pointer and description clauses, hermetic selftest. — `.ufo/waves/round-51/claims.md:20` (verified)
- `quality/counters/c1-r51-ledger.py` — PRED-C1-r51 counter: scores this ledger's coverage and pointer clauses at one revision. — `.ufo/waves/round-51/claims.md:21` (verified)

Consequence for the freeze: at the revision where PRED-C1-r51 is scored, both files exist, so
`P = 81` — the ledger must carry these two rows (each pointing at a naming file that exists at that
revision) or `uncovered` is 2. `quality/tool-ledger.md` itself is not in the population.

## 6. Findings routed to the L1 freeze

**F1 — the population sentence admits two different `P`.** `quality/*.py` as a git pathspec recurses
into `quality/counters/` (62 paths = 18 + 44), so a summing implementation counts 123 entries for 79
distinct files; as a filesystem glob it returns 18. `appears exactly once` already implies a set — pin
the de-duplicated reading (`P = 79` here) in the counter, or the frozen clause is ambiguous.

**F2 — self-pointer loophole: 26 of 79 files contain their own basename.**
A row whose pointer is the file itself therefore satisfies `pointer file contains the basename` and
`bad_pointer` stays 0. Add `pointer_file != row.file` plus a control that a self-pointer MISSes.

**F3 — ledger-self loophole.** `quality/tool-ledger.md` will contain every basename and is not in the
population, so any row can point at the ledger and pass. Add `pointer_file != quality/tool-ledger.md`
and a control that such a pointer MISSes.

**F4 — no durable instrument register for the `quality/` instruments.** 27 rows are accountable only
through lesson prose (mostly recording a defect in the counter), 5 only through the successor that
superseded them, 4 only through a move-log row, 3 only through a QUALITY criterion body. Coverage is
obtainable (0 strict gaps); accountability for two-thirds of the instruments is incidental prose.
This ledger is the first durable register — it should stay the register.

**F5 — `:line` suffixes are rev-stable only while `PROVINCE.md`/`SCORECARD.md`/`corpus/**` do not move.**
All 79 pointers resolve identically at base `6ca8c559a4a3d6d361101592116eea2bc7452437` and at the measured revision because those trees are
byte-identical (`git diff --stat <base>..<rev>` empty). A later insertion drifts the numbers while the
basename test still passes. Either drop the `:line` suffix from the frozen row format or freeze it as
provenance only.

**F6 — shared pointers.** 7 pointer lines are shared by more than one row (`PROVINCE.md:100` ×2, `PROVINCE.md:109` ×2, `SCORECARD.md:2385` ×2, `SCORECARD.md:2454` ×2, `SCORECARD.md:2669` ×2, `SCORECARD.md:2743` ×2, `corpus/lessons/round-48.md:153` ×5).
Legitimate, but per-file accountability for those rows cannot be argued from the ledger alone —
a reader must follow the line.
