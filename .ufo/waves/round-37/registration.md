# mado round 37 — registration (frozen before any round-37 data)

Base: `b4e47e980bfb0cbc8a4e788f59a41db858751fd8` (lane `master` at round start; attempt 2).
Attempt 1 (06:05–06:46 -03) left one empty directory, `.ufo/waves/round-37/assimilation/`,
and no file; nothing is inherited from it. This file, the two counters, `controls.py`, the
control receipt and the source receipts under `fetch/` land in one freeze commit; any later
change to a counter is a new predicate and the claim it belongs to then fails as declared.

## Lowest-axis rule

`python3 -I quality/check-axis-scores.py --repo . --rev master` at the base prints
`navigation published=50/50`, `calibration published=48/48`, `operability published=12/12`,
`MADO_AXIS: checked=3 mismatched=0` — every published axis ties at its maximum, so each is a
lowest axis. The stagnation nudge does not apply (two capability rows entered in round 36,
window 3). C1 works `coverage` (published as navigation), one of the tied lowest axes. Neither
claim is a calibration claim; attempt 1's draft calling calibration "the lowest" is withdrawn
because the tie makes that unsupported.

## Theme and surface

One theme: **event-socket delivery** — what the compositor does to an event client that stops
reading (`EventManager.cpp`: a 64-event per-client cap, removal on overflow, partial-write
resume), and how that state is observed on this host. Ground unheld at the base:
`git grep -l -F <token> master -- corpus/knowledge` is empty for `MAX_QUEUED_EVENTS`,
`overflowed event queue`, `debug:disable_logs` and `m_logsEnabled`; the lane held the queue
cap only as a quoted line in lessons (round-33/34), never in a knowledge entry. Frontier row
moved: `corpus/README.md` *Frontier* — "Waybar module text, Walker socket protocol … No …
socket connection is added here" (the event-socket client half).

## C1 — coverage (assimilation + sourced): two event-delivery entries land on unheld ground

- **Predicate `PRED-C1-r37-v1`** — the docstring of `quality/counters/c1-r37-event-ground.py`
  is the predicate; the code is the same sentence. Target set (frozen):
  `corpus/knowledge/event-delivery-limits-r26.md` (package entry, re-grounded; tokens
  `MAX_QUEUED_EVENTS`, `overflowed event queue`) and
  `corpus/knowledge/event-queue-observability-r37.md` (lane entry replacing the two refused
  package host measurements; tokens `debug:disable_logs`, `m_logsEnabled`).
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r37-event-ground.py --repo . --rev <rev>`
- **Before** (at base): `admitted=0/2 verdict=TARGET_MISSED`, exit 1. **Target:** `admitted=2/2 verdict=TARGET_MET`, exit 0.
- **Kill rule:** anything other than `admitted=2/2` at the measured lane tip is a miss, reported
  as an honest stop; no target narrowing.
- **Sourced:** both entries rest on rows opened this round (S189, S201 re-opened; S212, S213,
  S214 new), each with a Gate line binding a committed receipt by sha256 and a located quote.

## C2 — operability (capability acquisition): a read-only event-socket subscriber census

- **Deliverable:** `tools/mado-eventq.py` — reads the kernel's unix-socket table (`ss -xpa`),
  never connects to a socket, and reports who is subscribed to the compositor's event socket,
  each subscriber's unread backlog, and the two failure markers in the session log and the
  compositor unit journal, plus whether those markers are observable at all
  (`debug:disable_logs`). Interface (frozen by the fixtures):
  `--ss-file`, `--log` (repeatable), `--journal-file`, `--disable-logs 0|1`,
  `--expect-client COMM` (repeatable), `--socket2 PATH`; live defaults read `ss -xpa`,
  `$XDG_RUNTIME_DIR/hypr/<instance>/hyprland.log`, `journalctl --user -u
  wayland-wm@hyprland.desktop.service` and `hyprctl getoption debug:disable_logs -j`.
  Output: `MADO_EVENTQ_CLIENT: comm= pid= fd= peer_recv_q= server_send_q=` per subscriber,
  `MADO_EVENTQ_MARKERS: source= overflow= write_fail=` per channel, and one
  `MADO_EVENTQ: socket2= subscribers= overflow= write_fail= lagging= missing_client=
  markers_observable= verdict=CLEAN|MARKERS|MISSING_CLIENT`; exit 0 CLEAN, 1 MARKERS or
  MISSING_CLIENT, 2 `MADO_EVENTQ: SETUP <reason>`.
- **Predicate `PRED-C2-r37-v1`** — the docstring of `quality/counters/c2-r37-eventq.py`; its
  ten fixture cases (inputs and expected exits/lines) are embedded in that file.
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r37-eventq.py --repo . --rev <rev>`
- **Before** (at base): `fixtures=0/10 readonly=0 live=0 tool=absent verdict=TARGET_MISSED`, exit 1.
  **Target:** `fixtures=10/10 readonly=1 live=1 verdict=TARGET_MET`, exit 0.
- **Kill rule:** as C1. The capability row enters `SCORECARD.md` only with the passing run.

## Separability

C1 reads only `corpus/` (entries, `SOURCES.md`, the round-37 lesson, `README.md`) and the
`fetch/` receipts. C2 reads only `tools/mado-eventq.py`, its own embedded fixtures and the
live receipt. No C1 entry cites the tool or its receipt; the tool reads no corpus file. Each is
measurable with the other's files deleted.

## Controls (do-nothing and cribs, scored with the frozen counters before data)

`python3 -I .ufo/waves/round-37/controls.py --out .ufo/waves/round-37/receipts/controls.txt`
builds each control in a `/dev/shm` sandbox clone at the base and scores it. C1: do-nothing,
byte-exact package copy with index rows, fabricated quotes, wrong digest, an E2 citing only
the receipt that lacks one token, unindexed, rows `queued` — all `TARGET_MISSED`; a golden
synthetic tree wired to the real receipts — `TARGET_MET` (the accept path exists). C2:
do-nothing (tool absent), an always-clean stub, a grep-only stub, a stub importing `socket` —
all `TARGET_MISSED` (best 2/10). C2's accept half is the deliverable itself.

## Assimilation (rides C1; no extra claim)

Package `/home/vgpnk/Projects/shokuknow/merge/mado/` (read-only). Theme entries considered:
`event-delivery-limits-r26.md` — **admit** after re-grounding; `event-queue-host-measurement-r28.md`
and `event-queue-journal-measurement-r29.md` — **refuse**: both infer "never overflowed" from a
zero marker count, but on this host `debug:disable_logs` is 1, so the core logger that writes
both markers returns before writing (S214 `Logger.cpp:15-16`, `:48`); the session log's 21
core-logger lines all precede line 22, and an ERR line present in the log is absent from the
journal (S213). A zero there cannot tell "never overflowed" from "not logged". r28's own
source (instance `_1792772698_564628331`) no longer exists on the host. Flip: a host with
`debug:disable_logs = 0` re-measured. Id collisions and the renumber map live in
`assimilation/`; ids follow documents, never arithmetic.

## Not claimed

No score change on any axis is claimed by either counter; no transition, event or socket
connection is made; no config, service or compositor state is touched.
