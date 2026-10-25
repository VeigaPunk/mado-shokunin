# Round 37 lesson — mado

Two claims, distinct axes, frozen before any round-37 data
(`.ufo/waves/round-37/registration.md`; v1 at `8f0a9e3`, re-frozen as v2 by Amendment 1 at
`893a8aadc80ab19bc163e366d674a8ac32feacd0`). Base `b4e47e980bfb0cbc8a4e788f59a41db858751fd8`.
Theme: **event-socket delivery** — what the compositor does to an event client that stops
reading, and how that state is observed on this host.

## Claims

- **C1 — coverage (assimilation + sourced).** Two event-delivery entries land on ground the
  lane did not hold at the base: `corpus/knowledge/event-delivery-limits-r26.md` (package
  entry, re-grounded; tokens `MAX_QUEUED_EVENTS`, `overflowed event queue`) and
  `corpus/knowledge/event-queue-observability-r37.md` (lane-authored, replacing the two refused
  package host measurements; tokens `debug:disable_logs`, `m_logsEnabled`). Predicate
  `PRED-C1-r37-v2` — the docstring of `quality/counters/c1-r37-event-ground.py`, clauses a–g.
  Counting command:
  `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r37-event-ground.py --repo . --rev <rev>`.
  Before (base): `admitted=0/2 verdict=TARGET_MISSED`, exit 1
  (`.ufo/waves/round-37/receipts/before-c1-v2.txt`). Target: `admitted=2/2 verdict=TARGET_MET`,
  exit 0. Kill rule: anything else at the measured tip is a miss, reported as an honest stop;
  no target narrowing.
- **C2 — operability (capability acquisition).** `tools/mado-eventq.py`, a read-only
  event-socket subscriber census: reads the kernel's unix-socket table (`ss -xpa`), never
  connects to a socket, reports each subscriber's unread backlog and the two failure markers
  per log channel, and whether those markers are observable at all (`debug:disable_logs`).
  Predicate `PRED-C2-r37-v2` — the docstring of `quality/counters/c2-r37-eventq.py`, ten
  embedded fixtures, a read-only clause and a live-receipt replay. Counting command:
  `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r37-eventq.py --repo . --rev <rev>`.
  Before (base): `fixtures=0/10 readonly=0 live=0 tool=absent verdict=TARGET_MISSED`, exit 1
  (`.ufo/waves/round-37/receipts/before-c2-v2.txt`). Target:
  `fixtures=10/10 readonly=1 live=1 verdict=TARGET_MET`, exit 0. Kill rule as C1; the
  capability row enters `SCORECARD.md` only with the passing run.
- **Amendment 1 (append-only, before any data).** The v1 `c1-golden` control was a token-only
  stub ("body naming MAX_QUEUED_EVENTS and …") wired to the real receipts and it reached
  `admitted=2/2 TARGET_MET`; the v1 C2 `live` clause trusted a receipt a hand could write with
  the right digest. `PRED-C1-r37-v2` adds clause **g** (for every cited S-id the entry body
  carries one of that id's located Gate quotes verbatim and an `**OBS**` line naming the id);
  the v1 golden is kept as control `c1-token-stub` (must miss) and `c1-golden-v2` must meet.
  `PRED-C2-r37-v2` adds the replay: the committed raw `ss -xpa` snapshot
  `receipts/eventq-live-ss.txt`, re-run through the committed tool, must yield the receipt's
  (comm, pid, fd) client set. Targets, kill rules, counting commands and the target entry set
  are unchanged; v1 receipts stay as the v1 record, v2 receipts carry `-v2`; nothing measured
  under v1 is reused. Controls under v2: `controls=13 correct=13/13`
  (`.ufo/waves/round-37/receipts/controls-v2.txt`).
- **Separability.** C1 reads only `corpus/` and the `fetch/` receipts; C2 reads only
  `tools/mado-eventq.py`, its own fixtures and the live receipt. No C1 entry cites the tool or
  its receipt; the tool reads no corpus file.

## Gate

### Census before → after

Command, run at round start and round end:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

**Before** (round start at base `b4e47e9`, 201 data rows S001…S211), exit **0**
(`.ufo/waves/round-37/receipts/census-before.txt`):

```text
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
```

**After** (round end, at `<tip>`, `<N>` data rows), exit **`<rc>`**:

```text
<AFTER: paste the round-end census output verbatim; exit 0 is required>
```

Rows `201 → <N>`. Rows added by tier: `<S212, S213, S214 — tier A each, if appended>`.
Rows touched old→new: see *Used-by changes* below.

### Sources cited this round (S189, S201 re-opened; S212, S213, S214 new)

Each line binds a committed receipt by sha256 and a quote that `grep -F` finds in those bytes
(≤25 words). S189 carries two lines because both admitted entries cite it and each states a
different located quote (clause g of `PRED-C1-r37-v2` needs one of the id's Gate quotes in
each citing entry's body).

```text
GATE S189 receipt=.ufo/waves/round-37/fetch/S189.bin sha256=eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d quote="const size_t MAX_QUEUED_EVENTS = 64;"
GATE S189 receipt=.ufo/waves/round-37/fetch/S189.bin sha256=eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d quote="Socket2 fd {} overflowed event queue, removing"
GATE S201 receipt=.ufo/waves/round-37/fetch/S201.bin sha256=799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e quote="std::array<char, 1024> buffer;  // Hyprland socket2 events are max 1024 bytes"
GATE S212 receipt=.ufo/waves/round-37/fetch/S212.bin sha256=1e19d92638e7923f0e72f6e65c83f579e32b41d588d166d6efef543c3f97d7e9 quote="m_ipc.registerForIPC("workspacev2", this);"
GATE S213 receipt=.ufo/waves/round-37/fetch/S213.receipt.txt sha256=1c1b0ce149ecd7b1d20b0a83f266197c89c9f5334d17dc035fe499d93272ce58 quote="debug:disable_logs: {"option":"debug:disable_logs","int":1,"set":false}"
GATE S214 receipt=.ufo/waves/round-37/fetch/S214.bin sha256=d04e3a2fe5c73ad8684377856ce8301e493929ed9f391e405fde4975eaf6b868 quote="m_logsEnabled = !*PDISABLELOGS;"
```

| id | URL / artefact | accessed | bytes | located at | words |
|---|---|---|---|---|---|
| S189 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp | 2026-10-25 | 6,479 | `:169` and `:175` | 5 / 7 |
| S201 | https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp | 2026-10-25 | 6,550 | `:115` (two spaces before `//`) | 11 |
| S212 | https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/workspaces.cpp | 2026-10-25 | 41,392 | `:804` | 2 |
| S213 | own-work, host: current-session `hyprland.log`, `journalctl --user -u wayland-wm@hyprland.desktop.service`, `hyprctl getoption debug:*` — receipt taken 2026-10-25T09:00:04-03:00 | 2026-10-25 | 1,814 | receipt line 28 | 2 |
| S214 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/log/Logger.cpp | 2026-10-25 | 1,789 | `:48` | 3 |

Re-open on 2026-10-25T09:16:10-03:00: each of the four URLs answered HTTP 200 and `cmp`
reported the bytes identical to the committed receipt; S189 and S201 are also byte-identical
to `.ufo/waves/round-32/fetch/S189.bin` and `.ufo/waves/round-34/fetch/S201.bin`
(`assimilation/renumber-map.md`).

### Assimilation — package `/home/vgpnk/Projects/shokuknow/merge/mado/` (read-only), one theme

| package entry | verdict | reason | flip |
|---|---|---|---|
| `event-delivery-limits-r26.md` | **admit** after re-grounding | Every kept sentence re-checked against bytes re-opened this round (S189, S201, S212); the package's ids S187/S188/S214 are re-pointed by document to S189/S201/S212; its §2 host UNK is replaced by a pointer to `event-queue-observability-r37.md` | — |
| `event-queue-host-measurement-r28.md` | **refuse** | Infers "never overflowed" from a zero marker count in the session log, but with `debug:disable_logs` = 1 the core logger that writes both markers returns before writing (S214 `Logger.cpp:15-16`, `:48`); the log's 21 core-logger lines all precede line 22 (S213). A zero cannot tell "never overflowed" from "not logged". Its source instance `_1792772698_564628331` no longer exists on the host | A host with `debug:disable_logs = 0`, re-measured |
| `event-queue-journal-measurement-r29.md` | **refuse** | Same null channel, wider: the unit journal carries what the same disabled core logger never wrote, and a probe string the log carries 7× (all seven `ERR from aquamarine` lines) is 0× in the journal (S213) | A host with `debug:disable_logs = 0`, re-measured |

### Id collisions and renumber map

The round prompt §10 collision block (0–3-space row pattern), run against `corpus/SOURCES.md`
at base and `merge/mado/SOURCES.append.md`, outputs committed under
`.ufo/waves/round-37/assimilation/`:

- `reg-ids`: 201 ids (S001…S211). `staged-ids`: 147 ids (S203…S349).
- `collisions`: **9** — S203 S204 S205 S206 S207 S208 S209 S210 S211. None of the nine is
  appended; no staged row is appended as-is.
- Guard proof (`assimilation/guard-proof/`): a scratch registry whose `  | S002 |` row is
  indented two spaces — the 0–3-space pattern finds `S002` (n=1), the column-zero pattern
  finds none (n=0).
- Renumber map, by document, never arithmetic: `.ufo/waves/round-37/assimilation/renumber-map.md`
  — staged S214 → lane **S212**; entry note "wave-1 S187" → held **S189**; "wave-1 S188" →
  held **S201**; staged S226 and S242 refused (no row); lane own-work **S213**; lane **S214**
  (Logger.cpp).

### Quarantine slice — register row S189

The mado slice of the absent-defect register holds 13 data rows
(`.ufo/waves/round-37/assimilation/quarantine-slice`). One names a document an admitted entry
rests on: `round1 S189` (`EventManager.cpp`, class `payload-absent`, quote
``auto eventString = std::format(...)``). **Verdict: present** — line 128 of the re-opened
bytes reads `auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));`
(`grep -nF` → `128`); the register's escaped `\"`/`\\n` form is why its own check found
nothing. Adopted with the anchor located here, `:128`. The other 12 slice rows (S195,
register-S201 [an arXiv paper, not the lane's S201], S205, S224, S228, S199, S200, S209,
S222, S223, S225, S235) name documents no admitted entry cites; they stay quarantined,
unappended and unchecked this round.

### Used-by changes (old → new)

| id | column | old | new |
|---|---|---|---|
| S189 | used-by | `corpus/knowledge/ipc-contract-r25.md` | `corpus/knowledge/ipc-contract-r25.md, corpus/knowledge/event-delivery-limits-r26.md, corpus/knowledge/event-queue-observability-r37.md` |
| S201 | used-by | `corpus/knowledge/waybar-module-text-route-r25.md` | `corpus/knowledge/waybar-module-text-route-r25.md, corpus/knowledge/event-delivery-limits-r26.md` |
| S212 | row | — (new) | used-by `corpus/knowledge/event-delivery-limits-r26.md`, status `mined` |
| S213 | row | — (new) | used-by `corpus/knowledge/event-queue-observability-r37.md`, status `mined` |
| S214 | row | — (new) | used-by `corpus/knowledge/event-queue-observability-r37.md`, status `mined` |

No `status` or `recheck` cell of an existing row changes. S189 and S201 keep status `mined`,
opened `2026-10-24`, recheck `90d`.

## Mistakes

Four mistakes, named at section level so a citation check reading `#mistakes` sees them:
**M37-1** an accept control that was itself a token stub (instrument) · **M37-2** a gate whose
git calls inherit the caller's `GIT_*` (instrument) · **M37-3** a clean-tree assertion that
was never measured (hygiene) · **M37-4** a zero count read on a null channel (inference).
`<L1: confirm ids, classes and final wording; each fix counts only once shown able to fail>`

### M37-1 — the v1 accept control was a token stub that met C1

**What happened.** The v1 `c1-golden` control wrote each target entry as
`body naming MAX_QUEUED_EVENTS and overflowed event queue.` (`git show
8f0a9e3:.ufo/waves/round-37/controls.py`, `entry()` at :50-52), wired to the real receipts,
and scored `PRED-C1-r37-v1 admitted=2/2 verdict=TARGET_MET`. A control meant to prove the
accept path exists proved instead that an entry with no evidence in it meets the counter —
the junk-commit pattern of the kake r34 closure.

**Evidence pointer.** `.ufo/waves/round-37/receipts/controls.txt`
(`control=c1-golden expect=TARGET_MET rc=0 ok=1 :: PRED-C1-r37-v1 admitted=2/2 verdict=TARGET_MET`);
`.ufo/waves/round-37/registration.md` Amendment 1.

**Captured-by.** `corpus/QUALITY.md` criterion 36 requires reject controls that skip the
claimed work; it says nothing about the accept control, so a golden that skips the work
passed it. Caught by the L1 applying the cheapest-control rule to its own controls, before
any seat was dispatched.

**Fix.** Clause g in `PRED-C1-r37-v2`; the v1 golden kept as the must-miss control
`c1-token-stub`. Demonstrated able to fail (`receipts/controls-v2.txt`): `c1-token-stub`
reads `g=0 … admitted=0/2 verdict=TARGET_MISSED` while `c1-golden-v2` (minimal entries that
state their located quotes) reads `admitted=2/2 verdict=TARGET_MET`; `controls=13
correct=13/13`. Proposed criterion: the accept control is built as the minimal honest
artefact, and its stub (the same artefact with the evidence removed) is a committed reject
control.

### M37-2 — the pointer gate's git calls inherit the caller's GIT_*

**What happened.** `quality/check-evidence-pointers.py` runs `git -C <repo>` with the
caller's environment (`:76`, `:172`, `:204` — no `env=`). `git -C` does not override an
inherited `GIT_DIR` or `GIT_WORK_TREE`, so the same revision scores differently by who runs
it. Found by attempt 1 of this round.

**Evidence pointer.** `.ufo/waves/round-37/w1/scratch/ExecPointerEnv/red-green.txt` at
`--rev a5aaa09`: plain → `inherited_dirty=0 … verdict=TARGET_MET`; with
`GIT_DIR=/home/vgpnk/Projects/shokunin/.git` → `error=revision-not-readable:a5aaa09…`; with
`GIT_WORK_TREE=/dev/shm` → `inherited_dirty=8 … verdict=TARGET_MISSED`.

**Captured-by.** none — criterion 59 keeps a *fixture's* environment resolvable, and
criterion 29's check scrubs the environment of one harness; no criterion requires a gate to
be environment-independent.

**Fix.** Every git subprocess runs with all `GIT_*` removed (scratch copy
`.ufo/waves/round-37/w1/scratch/ExecPointerEnv/check-evidence-pointers.py`, the only delta).
Demonstrated able to fail: the fixed copy reads `verdict=TARGET_MET` plain, under `GIT_DIR`,
under `GIT_WORK_TREE` and under both; at `4243d03` (before any round-36 section) it still
reads `setup=missing-r36-sections verdict=TARGET_MISSED`, so the scrub does not green-wash.
Both round-37 counters already scrub (`c1-r37-event-ground.py:49`). `<L1: add the sweep of
quality/*.py, tools/*.py and tools/mado-verify.sh from ExecPointerEnv's report>`

### M37-3 — round 36 asserted a clean tree it never measured

**What happened.** The round-36 report says "Lane tip at closure: `a5aaa09…`, working tree
clean" (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-36/mado.md:379`) while
`.ufo/waves/round-36/w1/reports/DistillerFindings.md` (19,033 B) sat untracked in the lane
work tree (`corpus/lessons/round-36-verifier-spotcheck.md` §5 R1). The pointer gate's
`inherited_dirty` checks only the ten round-35 closure paths
(`quality/check-evidence-pointers.py:23`, `:171`), so the round's own untracked output was
invisible to it.

**Evidence pointer.** spot-check §5 R1; the file was committed in `80b83c8` (this round).

**Captured-by.** none for the round's own paths — the D2 class was closed for round 35's
paths only, and the gate's path list is fixed to them.

**Fix.** The report's clean-tree line is a pasted `git status --porcelain` output at the
named tip, committed as a witness, never prose. Demonstrated able to fail, in a sandbox clone
(`/dev/shm/mado37-ScribeLessonGate/sb`): at `a5aaa09` with the file present, porcelain prints
`?? .ufo/waves/round-36/w1/reports/DistillerFindings.md`; at `80b83c8` it prints 0 lines and
`git ls-files --error-unmatch` finds the file.

### M37-4 — the package read a null channel as "never overflowed"

**What happened.** Package entries `event-queue-host-measurement-r28.md` (title "Measured:
the compositor's event queue has never overflowed on this host"; `**INF**` at :27) and
`event-queue-journal-measurement-r29.md` (`**INF**` at :26) count zero markers and conclude
the 64-event queue never overflowed. On this host `debug:disable_logs` is 1 and the core
logger returns before writing (S214 `Logger.cpp:15-16`, `:48`); both markers are core-logger
lines (S189 `:155`, `:175`). A channel that cannot carry the marker cannot show its absence.

**Evidence pointer.** `.ufo/waves/round-37/fetch/S213.receipt.txt` (core-logger lines 21,
last at line 21; live `debug:disable_logs` int 1); the package files at
`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/`.

**Captured-by.** none — the same class was named in round 35 as an erratum
(`corpus/lessons/round-35.md:183-184`; `corpus/knowledge/idle-lock-never-asked-r12.md` E1: "a
zero `omarchy-toggle` count is a null-channel reading, not a negative") but never became a
QUALITY criterion, so it recurred in package material.

**Fix.** Proposed criterion: a zero count counts as a negative only beside (a) the writer's
gate state for the window and (b) a positive probe from the same writer in the same channel
and window; otherwise it is recorded as a null-channel reading. Able to fail: applied to r28
and r29 it refuses both (gate state `disable_logs=1`; no core-logger line after line 21).
`<L1: the accept half is owed — this host has no core-logger channel that passes (a); name the
accept fixture (a log with disable_logs=0) or record the half as declared>`

## considerthese

`considerthese/2026-10-24.md` proposal 4 — "Suggest the next desktop table explicitly …
propose which Hyprland surface is next (window rules, monitors, layer rules) with the sources
that would ground it" — operator-authored, mined, not edited. The reflection is a pointer, not
evidence.

- **Already mined once.** Round 34 mined the same item as planning knowledge about oracle
  availability (`corpus/lessons/round-34.md:96-106`) and chose no surface. This round makes
  the choice the proposal asks for. `<L1: confirm that re-mining item 4 to its unmade half
  counts as "still unimplemented">`
- **This round's choice: the event socket's client half**, not a config table — the
  `corpus/README.md` *Frontier* bullet "Rendered UI, Waybar module text, Walker socket
  protocol, … No screenshot, input injection or socket connection is added here". It is
  grounded by S189 (the 64-event cap and removal), S201 and S212 (the host's own event client
  and its subscriptions), S214 (the logger gate) and S213 (this host's channels), and it is
  observable without touching the socket (`ss -xpa`).
- **Why not window or layer rules.** Re-observed first-hand on 2026-10-25T09:17:43-03:00 with
  read verbs on `v0.56.2 efb50993…`: `hyprctl windowrules -j`, `layerrules -j` and `rules -j`
  each print `unknown request`, so the round-25–27 predict-the-table method has no oracle
  there; `hyprctl monitors -j` answers (1 monitor) and `workspacerules -j` answers (1 rule).
- **Next table, for a later round:** the monitor table, which has a live oracle. Its sources
  are not opened here, so it is no row (CORPUS.md rule 1).
