# ScoutShokuknow - assimilation + considerthese check, round 47 w1 (mado)
Read-only. Read: shokuknow `merge/mado/MERGE-REPORT.md` (136 l), `SOURCES.append.md` (grep), the staged knowledge files named below, `PROVINCE.md`, `considerthese/2026-10-26.md`, `corpus/lessons/round-46.md:365-373`, round-46 `ConnToolFamily.md`, round-47 `ScrToolLedger.md`, `SKILL.md` Gate registry, `corpus/README.md`, `corpus/QUALITY.md:418-459`. Nothing written under shokuknow, no campaign tool run, nothing in the lane except this seat dir.

## Part A - MERGE-REPORT.md versus the terminal / desktop-entry / session-material plane

### A0 Verdict
**No staged theme is about terminals, `xdg-terminal-exec`, desktop entries or the terminal-selection chain. Admit for C1/C2: 0.**
Evidence: `grep -n -i 'terminal|xdg-terminal|desktop entr|\.desktop|session-material|Alacritty' MERGE-REPORT.md` -> no match. Over the package (`SOURCES.append.md` + 69 knowledge files + `amendments/`): `grep -rn -i 'xdg-terminal|desktop file|desktop entry|TerminalEmulator'` -> none; the only `.desktop` hits are `wayland-wm@hyprland.desktop.service` (a unit name, `event-queue-journal-measurement-r29.md:8`, `idle-lock-runtime-state-r28.md:45`). C2's held ground (`terminal-route-r17.md`, `terminal-trees-r23.md`, `terminals-and-omarchy.md`) is therefore not duplicated or contradicted by the package. The r17 [UNK] at `terminal-route-r17.md:144-145` has no staged answer.

### A1 Entries that touch the launch path or terminals at the edges
(paths are under `merge/mado/knowledge/corpus/knowledge/`; PROVINCE basis: `PROVINCE.md:6-9` owns terminal configs + hypr keybinds; `:14-16` shape-only, no secrets; `:75-78` localized-channel rule)

| staged entry | touch | PROVINCE | call |
|---|---|---|---|
| `uwsm-app-daemon-unit-r7.md` (S262/S263/S268/S270) | the hotkey is `uwsm-app -- xdg-terminal-exec ...`; entry says the scope wrapping an app is a transient `systemd-run --user --scope --slice=app-graphical.slice` made by the app-daemon, no per-app template | IN for the launcher half (hypr binding -> uwsm-app is the owned chain); unit/slice *state* is tsukuroi's (`PROVINCE.md:24` row note, round-23 correction at `:34`) | **ADMIT-CANDIDATE (later, not for C2).** Neighbour of C2 (what wraps the terminal after selection), not part of the selection chain. Conditions: renumber (S262-S270 collide with held lane rows), re-open S262/S263 at the host's uwsm tag; S268 and S270 point at `lanes/mado/round7/fetch/*` receipts that are NOT in the package, so refuse those two rows until a fresh host read exists. Cite-only use in C2 is fine as a one-line pointer if its S-rows are re-opened. |
| `update-check-and-app-lifecycle-r31.md` (S254/S257) | S257 `omarchy-restart-app`: `pkill -x` then `setsid uwsm-app -- "$@"`; its [UNK] "unit that wraps a launched app" is what r7 closes | IN for the restart helper (omarchy skill surface is documentation, read-only); the update-chip half (S254) is a bar producer, already lane ground in `host-bar-producer-census-r40.md` | **ADMIT-CANDIDATE, split.** Fold with r7 entry (r7 supersedes the [UNK]); keep only the S257 section; refuse the S254 "up to date" half as duplicate/off-plane. Not for C2. |
| `host-bar-producers-r28.md:22` | one table row: `custom/omarchy` click opens a terminal (a second launch route that bypasses SUPER+RETURN) | IN (bar config) | **REFUSE as an entry** (superseded by lane `host-bar-producer-census-r40.md`). Use only as a lead: C2 `explain` can note that the bar click is a different route and is not modelled. |
| `gkeep-geometry-unobservable-r8.md:20-24`, `gkeep-rendered-geometry-chain-r9.md:90` | "two `Alacritty` terminals and `zcode`" from a dated `hyprctl clients -j` | IN, class-only so shape-only per R1 of the gate | **REFUSE** (superseded by lane r43/r44 gkeep entries; stale live count). |
| `gkeep-rendered-geometry-record-r14.md:55,65`, `gkeep-geometry-never-recorded-r15.md:58` | "opening one would mean launching an application" - charter boundary | IN, consistent with this round's host guard (no launching) | **REFUSE as entries** (gkeep series already closed by r43/r44); the boundary sentence agrees with C2's read-only stance, no action. |
| everything else (focus-grab x14, idle-lock x12, IPC/socket, wiki, localized: two-literature, chinese-*, japanese-*) | none on terminals | focus/idle covered by lane r35/r41; localized channel OUT (`PROVINCE.md:75-78`) | REFUSE for this round's plane (same reasons as the round-46 screen, `w1/ScoutShokuknow.md` table). |

### A2 Session-material gate (QUALITY 85, `quality/check-session-material.py`)
- The gate reads only tracked files under `.ufo/` at a rev (`check-session-material.py` docstring, "Every file under ``.ufo/`` tracked"). Staged knowledge would land in `corpus/knowledge/`, outside that gate: **adoption of any staged entry is not covered by criterion 85** unless the L1 widens the pathspec or runs the same four patterns by hand.
- I ran the four shapes over the package by grep: `users:\(\(`, `pid=\d+`, `"serial"`, `"title"`/`"initialTitle"`, `/home/<user>/` -> hits are only host paths inside `source:` lines and SOURCES rows (`host-bar-producers-r28.md:8`, `host-producer-outputs-r29.md:10-12`, `host-producer-current-outputs-r30.md:11-12`, `gkeep-element-rules-r30.md:8`, `idle-lock-offered-in-the-bar-r15.md:10-12`, `SOURCES.append.md:28,43-45,53-55,139-141`): single quoted paths, allowed by the task's rule ("a single quoted path in a sentence is fine"). **No process table, serial, title or listing in the package.** Residual: S339/S340/S342 (`SOURCES.append.md:143-146`) cite `lanes/mado/round15/fetch/*` receipts that are absent, so their content (a toggle-state directory sweep, dated backups sweep) is unreviewable for session material.
- C1/C2 consequence: `mado-terminal.py` and its fixtures read host `.desktop` files and PATH; the entry must record host observations shape-only (ids, the one override path as a quoted sentence-path, no `ls ~/.local/share/applications` dump - R4 trips above 10 bare `/home/..` lines). Any `explain` receipt committed under `.ufo/` should be run through the gate before the L1 commits.

### A3 Package-level facts for the L1 (C2 adoption hazard)
- ID collision is wider than round 46 recorded: MERGE-REPORT.md:9 says first staged id S203; staged space runs S203-S349 (147 rows). The lane tops at S325, and this round's C2 rows are S326.. Staged `S326` is a different row (cited at `gkeep-rendered-geometry-record-r14.md:55`: the journal row). Never run adopt-step 3 (append `SOURCES.append.md`) without renumbering past this round's last S-row.
- No staged row covers `Vladimir-csp/xdg-terminal-exec`. C2 rows S326.. are first-hand; uwsm's repo (S262/S263, same author) is the only adjacent staged source.

## Part B - considerthese/2026-10-26.md proposals (`:47-52`)

| # | proposal | status at tip c24adef2 | evidence |
|---|---|---|---|
| 1 | privacy check on new receipts | **landed r45** | QUALITY 85 (`corpus/QUALITY.md:418`), `quality/check-session-material.py`; r46 R3 marker draft (`w1/ExecSessionTriage`) routed to this round as R3 |
| 2 | running ledger of live-state tools | **NOT landed**: draft only | `lessons/round-46.md:367` "has a draft at `w1/ConnToolFamily/`, not landed"; `ConnToolFamily.md:160` proposes `corpus/knowledge/live-state-tool-ledger.md` (absent from `corpus/knowledge/`); r47 `ScrToolLedger.md` is a stub ("IN PROGRESS", no `ledger.md` in its dir when I read it) |
| 3 | track routed defects | **landed r46** | QUALITY 90 (`corpus/QUALITY.md:454`), `lessons/round-46.md:365-369` |
| 4 | re-run a tool myself | blocked on operator OK + machine access (proposal text `:50`) | not landable by a seat |
| 5 | domain-to-meta ratio | effectively covered by `quality/ratio-domain-meta.py` (round 44, from `considerthese/2026-10-25.md:46`); same idea, earlier file | `git log` e4678921 |
| 6 | lead with outcomes | style rule for the daily writer, not repo-landable | - |

So **proposal 2 is the one unimplemented, landable proposal** (4-6 are blocked, redundant or non-artifact).

### B1 Why it is worth landing now (measured gaps)
`grep -c <tool> SKILL.md corpus/README.md PROVINCE.md` per tool (14 files in `tools/`):
- Gate registry (`SKILL.md:684-` states "This `SKILL.md` is the registry home"): **0 rows** for `mado-anims`, `mado-binds`, `mado-eventq`, `mado-options`, `mado-wsrules` (0 mentions in SKILL.md at all); mado-monitors 1 mention, mado-assessment 1.
- `corpus/README.md`: 0 mentions of `mado-globals`, `mado-assessment`, `mado-action-plan`, `mado-evidence-audit`.
- `PROVINCE.md` tool table (round-23 table, `:22-32`): 0 mentions of `mado-eventq`, `mado-options`, `mado-wsrules` (the table stops at geometry, `:32`; monitors/devices live only in refinement paragraphs `:100,:102`).
- The considerthese numbers are stale: it says tools/ went "9 to 12 files"; the directory now holds 14.
- `mado-terminal.py` would be the 15th tool and the first ledger consumer: its row (question: which terminal does SUPER+RETURN launch; inputs: XDG_* env, PATH, list files, `.desktop` files; live receipt: `explain --observed` on the host) is the natural first test that the ledger is current at landing.

### B2 How it would land (smallest set that touches every reader path, no new write surface)
1. **Artifact:** `corpus/knowledge/live-state-tool-ledger.md` (name taken from `ConnToolFamily.md:160`). One table per tool: question answered; inputs (file / dump / journal / hyprctl verb / env); starts process? opens socket? (declared vs enforced by which counter - ConnToolFamily §5: record the enforcement layer, because "starts no process" in a docstring is not what a counter proved); last committed live receipt path + round + verdict; operator invocation; exit map; staleness date. Two family invariants from ConnToolFamily §6 (summary line names the counters behind DIFFER; where the domain-empty verdict sits in the exit ladder).
2. **README table:** one row in `corpus/README.md` "Province routes - choose a surface" (`:81-`), not a new "Round-47 route" prose block, pointing at the ledger; plus a Frontier line for `mado-terminal.py` per the existing round-N route pattern (`:215-:310`).
3. **QUALITY criterion 91** (next free number; 90 is the last, `:454`): "every tool under `tools/` has exactly one ledger row, and a row's last-live-receipt path exists at the tip and names the round that produced it; a round that adds or changes a tool updates the row in the same commit." Check: a seat instrument that diffs `ls tools/mado-*` against ledger rows and `git cat-file -e` for each receipt path. Shown able to fail today: the five tools with 0 SKILL rows and the three with 0 PROVINCE rows above, and once the ledger exists, delete one row or point one receipt at a missing path. Mark it a seat instrument (same shape as 88: "provenance, not credit under criterion 25").
4. **Lesson:** `lessons/round-47.md` states the proposal-2 provenance (`considerthese/2026-10-26.md:48`) the way round 46 did for proposal 3 (`lessons/round-46.md:365-369`); the next considerthese can then drop its "relayed numbers" caveat for tool state because the ledger carries receipts.
5. **PROVINCE.md:** append-only refinement (pattern of `:100,:102`) naming `tools/mado-terminal.py`: reads env `XDG_*`/`PATH` values as strings and the `xdg-terminals.list` + `.desktop` bytes under the XDG dirs, stats PATH entries, runs no process, opens no socket, writes nothing; terminal launch selection is owned by `PROVINCE.md:6-9` ("terminal emulator configs", hypr keybinds). Without this the new tool is the third (after eventq/options/wsrules) missing from the inventory.
6. **SKILL.md Gate registry:** add rows for the tools in B1 including `mado-terminal` (name / probe / command / verdict map / selftest / write scope / owner), so the registry-home claim at `:686` holds.

Risk (same as ConnToolFamily): staleness. Mitigation is criterion 91's receipt-exists check, not prose.

## Confidence / not examined
High: A0 absence (grep over report + package), B status table (cited lines), B1 counts (grep -c). Medium: A1 PROVINCE calls for uwsm/lifecycle (judgement; the unit-state boundary with tsukuroi is the open edge). Not done: full read of the 14 focus-grab entries (not on this plane); I did not run any counter or the session-material gate (grep only); the ScrToolLedger seat was still a stub, so B2 may be overtaken by its `ledger.md`.
