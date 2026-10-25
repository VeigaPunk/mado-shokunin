# ScribeReadme draft — corpus/README.md changes for round 37 (scratch; not a production file)

Drafted 2026-10-25 against lane `HEAD` 80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b. Every figure below is
taken from the round-37 fetch bytes (`.ufo/waves/round-37/fetch/S189.bin`, `S201.bin`, `S212.bin`,
`S213.receipt.txt`, `S214.bin`). The two entries do not exist yet: the Holds cells describe what the
registration and the re-opened receipts say each entry must carry, and the Sources cells MUST be
reconciled with each entry's final `source:` line before landing.

Landing prerequisites, all shown by the gate runs in the ScribeReadme report: both entry files in the
same commit as the rows (otherwise `check-index.py` reports `dangling`); SOURCES.md rows for S212, S213
and S214 (otherwise `cited-s-undefined`); `corpus/lessons/round-37.md` present (otherwise
`cited-path-missing`, because the Sources cells cite it). Do not write a bare package id such as "staged
S214" anywhere in a row: the row gate scans the whole line for `S###`, and lane S214 is `Logger.cpp`.

## (a) Coverage-map rows

Placement: append both lines directly under the last row of the `## Coverage map` table
(currently `knowledge/idle-lock-offered-in-the-bar-r15.md`, README line 61), with no blank line in
between. `check-index-rows.py` ends the table at the first line that does not start with `|`, so a
blank line or a row anywhere else is `row-outside-map`.

```markdown
| `knowledge/event-delivery-limits-r26.md` (round 37; package entry re-grounded; Hyprland event socket) | What Hyprland v0.56.2 does to an event client that stops reading: each socket2 client has its own queue, capped at `MAX_QUEUED_EVENTS = 64`; a client at the cap is removed, not throttled ("Socket2 fd {} overflowed event queue, removing"); a partial write resumes from the client's `writeOffset`, `EAGAIN`/`EWOULDBLOCK` leaves the event queued and `EINTR` retries, and any other write failure logs "failed writing event" and drops the client; events posted during shutdown are suppressed. The client half is Waybar 0.15.0: the backend reads each line into a 1024-byte `fgets` buffer, and the workspaces module registers for twelve events unconditionally. Source-read only: no socket was connected, no event was observed and no client was stalled. | `source:` S189, S201, S212 in [SOURCES](SOURCES.md) (S212 is the package's staged Waybar `workspaces.cpp` row, renumbered); fetched bytes `.ufo/waves/round-37/fetch/S189.bin`, `.ufo/waves/round-37/fetch/S201.bin`, `.ufo/waves/round-37/fetch/S212.bin`; Gate lines in `corpus/lessons/round-37.md`; recheck 90d. |
| `knowledge/event-queue-observability-r37.md` (round 37; lane-authored; host log channels) | Whether this host can show the two event-socket failure markers at all. Hyprland v0.56.2's core logger returns before writing while `m_logsEnabled` is false (`Logger.cpp:15-16`), and `m_logsEnabled = !*PDISABLELOGS` (`:48`); on this host `hyprctl getoption debug:disable_logs` reads 1 (`"set":false`), the session log's 21 core-logger lines all precede line 22, and a probe string found 7 times in the session log appears 0 times in the compositor unit journal. A zero count of either marker in the log or the journal is therefore a null channel, not evidence that no client was removed. Replaces the package's two refused host measurements (r28, r29). | `source:` S213, S214 in [SOURCES](SOURCES.md); receipt `.ufo/waves/round-37/fetch/S213.receipt.txt` (sha256 `1c1b0ce149ecd7b1`), fetched bytes `.ufo/waves/round-37/fetch/S214.bin` (sha256 `d04e3a2fe5c73ad8`); Gate lines in `corpus/lessons/round-37.md`; recheck on-change (flip: a host with `debug:disable_logs = 0`, re-measured). |
```

## (b) Frontier subsection

Placement: append at the end of the file, after `### Round-35 idle-lock offer route` (the newest
subsection; the file's subsections run in landing order).

```markdown
### Round-37 event-socket delivery route

- The event-socket client half of the first Frontier bullet now has sourced ground. The compositor
  side: Hyprland v0.56.2 gives each socket2 client its own queue capped at 64 events, removes a client
  at the cap instead of throttling it, resumes partial writes from a per-client offset, and drops a
  client on any other write failure ([event delivery limits](knowledge/event-delivery-limits-r26.md));
  the client this host runs, Waybar 0.15.0, reads those events through a 1024-byte line buffer. The
  host side: while `debug:disable_logs` = 1 the core logger returns before it writes, so the session
  log and the compositor unit journal are a null channel for both removal markers, and a zero count
  there cannot show that no client was ever removed
  ([event-queue observability](knowledge/event-queue-observability-r37.md)). The package's two host
  measurements that read a zero count as "never overflowed" (r28, r29) are refused, not admitted.
  Still open: no event was observed and no socket was connected; no client was stalled, so the
  64-event cap, the removal path and the partial-write resume were never exercised on this host;
  whether any client was ever removed here cannot be read from the log or journal until
  `debug:disable_logs` is 0 (a config change this lane does not make); and what Waybar does after the
  compositor removes it — the upstream listener has no reconnect path in the lines read, but no
  removal was observed.
```

If C2 reaches `TARGET_MET`, one sentence MAY be added before "Still open": "`tools/mado-eventq.py`
lists the event socket's subscribers and their unread backlog from the kernel's unix-socket table
without connecting (round-37 C2)." Leave it out unless C2's passing run lands, because the README must
not route to a tool that does not exist.

If ScoutWaybarDrop shows Waybar's post-removal behaviour from source, replace the last clause with its
located finding and keep "no removal was observed".

## (c) Optional companion edit — first Frontier bullet (round-35 precedent)

Round 35 annotated the Frontier bullet it moved in place. The matching edit for round 37 would be to
replace README lines 98–100:

```markdown
- Rendered UI, Waybar module text, Walker socket protocol, dispatcher
  behavior and per-window rule effects: [arc gap ledger](knowledge/arc-synthesis.md)
  §6. No screenshot, input injection or socket connection is added here.
```

with:

```markdown
- Rendered UI, Waybar module text, Walker socket protocol, dispatcher
  behavior and per-window rule effects: [arc gap ledger](knowledge/arc-synthesis.md)
  §6. No screenshot, input injection or socket connection is added here;
  round 37 moved the event-socket client half onto sourced ground (see the
  round-37 route below), and rendered text and delivery on this host stay open.
```
