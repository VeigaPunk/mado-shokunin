# ScoutNullChannelRecheck — mado r38 w1, scout seat

Question (as assigned): re-run the null-channel basis under a **new instance epoch**. The brief
asserts "the host rebooted since round-37 (the instance dir in the receipts carries epoch
1792804449 vs round-37's)". Re-check `debug:disable_logs`, the unit journal, the session log, and
whether any **new** channel exists where the markers would land. Verdict: null-channel claim
still holds / moved.

**Verdict: the null-channel claim still HOLDS — but the premise under which I was asked to test
it is FALSE. There was no reboot since round-37, and no new instance epoch. The epoch
`1792804449_426444678` is the *same* epoch round-37 already ran under.**

Two separable results:

1. **PREMISE FALSIFIED (finding).** The brief's parenthetical is wrong: round-37's own committed
   receipts already carry epoch `1792804449_426444678`. The reboot happened *before* round-37
   (2026-10-23 22:14), not between round-37 and round-38. My re-run is therefore a **second
   observation of the same instance**, not a fresh-epoch one. All four probes still read
   null, and I added a **fresh 278-line delta window** the round-37 receipts did not have.
2. **CLAIM HOLDS (PASS).** Every channel that could carry the markers is still blind:
   `debug:disable_logs` = 1, journal 0 markers, session log 0 markers, `rollinglog` 0 core
   lines. No new channel appeared.

Privacy: counts, digests, prefixes and booleans only. No raw journal/log line text, no window
titles, no socket inodes beyond those already published in the lane's own receipts.

---

## Item 0 — The "new instance epoch" premise: **FAIL (the premise is false)**

The brief says the receipts' instance dir "carries epoch 1792804449 vs round-37's". It does not
differ from round-37's. Round-37's own committed blob carries the identical epoch string:

```
$ git show HEAD:.ufo/waves/round-37/receipts/eventq-live.txt | grep -o 'hypr/efb5[^ ]*'
hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/hyprland.log
hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/.socket2.sock
```

Round-38's receipts carry the same string (16 epoch tokens in `.ufo/waves/round-38/`,
6 in `.ufo/waves/round-37/`). Across the whole wave tree only **two** instance dirs have ever
been named:

```
$ grep -rhoE 'hypr/[a-f0-9]+_[0-9]+_[0-9]+' .ufo/waves/ | sort -u
hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120
hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678
```

- `1792655744` = 2026-10-22, `1792772698` = 2026-10-23T13:24:58-03:00, `1792804449` =
  2026-10-23T22:14:09-03:00. The **current** epoch has been in force since 2026-10-23 22:14,
  i.e. **~35 hours before round-37's receipts were taken** (`taken: 2026-10-25T09:19:03-03:00`).
- Host facts proving no reboot between the rounds:
  - `boot_id=0a3785aac7104585a914f6cda41795a7`, `journalctl --list-boots` shows boot 0 as
    `Fri 2026-10-23 22:14:07 -03` → `Sun 2026-10-25 11:15:20 -03`, "still running".
  - `uptime` = 134161 s ≈ 1 d 13 h; `who -b` = `system boot 2026-10-23 22:14`.
  - The compositor is the **same process**: PID 1619, started `Fri Oct 23 22:14:09 2026`, elapsed
    `1-13:02:37`. The r37 receipts name `pid=1619`; the r38 receipts name `pid=1619`.
  - The socket2 client `socat pid=2293` is still alive with `ELAPSED 1-13:12:41` and its cmdline
    still embeds the **current** epoch path — the same process round-37 photographed.
- Where the "reboot" impression comes from: the journal still contains **one** line naming the
  *older* epoch `_1792772698_564628331` (the pre-22:14 instance). That is the boot-−1 boot, and
  round-32/round-35 already noted that dir as stale. It is a relic, not a new boot.
- Also stale-artefact-precise: round-38 `registration.md:92` calls `_1792772698_564628331` a
  "stale artefact" — correct, and consistent with this finding.

**Consequence for the round.** Any round-38 argument that leans on "a reboot happened, so the
epoch changed" is unsupported. This is a dispatch-prompt defect, not a lane defect: no round-38
counter, receipt or registration file makes that claim. I grepped for it and found none —
`grep -rniE 'reboot|new epoch|since round-3[67]'` over `registration.md`, `receipts/`, `fetch/`
and all three `c1`/`c2` counters returns **no hits**.

---

## Item 1 — `hyprctl getoption debug:disable_logs -j` — **PASS (still 1)**

```
$ hyprctl getoption debug:disable_logs -j
{"option": "debug:disable_logs", "int": 1, "set": false }
$ hyprctl getoption debug:enable_stdout_logs -j
{"option": "debug:enable_stdout_logs", "int": 0, "set": false }
```

`set: false` = the shipped default, never overridden by the user. This is the same value the
round-37 S213 receipt recorded, and it is the value `S215:629`
(`MS<Bool>("debug:disable_logs", "disable logging to a file", true),`) makes the default for any
v0.56.2 host. Structural basis unchanged:

```
$ sed -n '14,17p;47,48p' .ufo/waves/round-37/fetch/S214.bin
void CLogger::log(Hyprutils::CLI::eLogLevel level, const std::string_view& str) {
    if (!m_logsEnabled)
        return;
    m_logger.setEnableStdout(!*PDISABLELOGS && *PENABLESTDOUT);
    m_logsEnabled = !*PDISABLELOGS;
```

Every channel (file, stdout/journal, rolling buffer) is downstream of that `return`.

---

## Item 2 — unit journal `grep -c 'Socket2 fd'` — **PASS (still 0)**

```
$ journalctl --user -u wayland-wm@hyprland.desktop.service --no-pager -q -o cat | grep -c 'Socket2 fd'
0
```

Broadened, still 0 everywhere:

| channel | `Socket2` | `Socket2 fd` |
|---|---|---|
| unit journal (all boots) | 0 | 0 |
| whole user journal | 0 | 0 |
| whole system journal | 0 | 0 |
| per-boot (4 boots, incl. the pre-reboot ones) | 0 | 0 |

The unit journal is **717 lines, sha256 `43bf1f07176502bfa073c8256b718e0bd5cdcee5b94c1d188479dec490af63d4`** —
byte-identical in length and content to round-37's S213 receipt (`unit_journal_lines: 717`).
It has not grown in the ~2 h since r37, because `enable_stdout_logs = 0` (S215:632) closes the
stdout path that feeds the journal. Journal core lines = 42 across all boots = 21 for boot 0
+ 21 for boot −1; per boot 0 it is 21.

**Positive probe (the QUALITY-62 requirement), re-verified.** The journal's 21 core lines are
**byte-identical** to the session log's 21 core lines — same sha256 over the extracted set:

```
$ diff <(grep -E '^[A-Z]+ \]' $L) <(journalctl --user -u ... -b 0 -o cat | grep -E '^[A-Z]+ \]')
IDENTICAL
file core set sha256    = 159d31e11458037fb29d2ad37a324ca5f93bc6e45320dc20319f8089e04e8e8e
journal core set sha256 = 159d31e11458037fb29d2ad37a324ca5f93bc6e45320dc20319f8089e04e8e8e
```

So the journal **does** carry the core logger — but only its 21 startup lines, all before the
second config load at line 18. That is exactly the QUALITY-62 failure mode: a channel carrying
the same logger *only before a gate closed* proves nothing about the markers. The marker lines
are `ERR`-level core-logger lines (S189:155, :175) and the channel carries **zero** `ERR` core
lines.

---

## Item 3 — session log `grep -c 'Socket2 fd'` — **PASS (still 0)**

```
$ grep -c 'Socket2 fd' $XDG_RUNTIME_DIR/hypr/*/hyprland.log
0
```

Broadened: bare `Socket2` = 0; `overflowed event queue` = 0; `failed writing event` = 0;
`overflow` = 0; `queue` = 0; `removing` = 0; `failed writing` = 0. Only `socket` = 1 (a
non-marker word, in the aquamarine channel).

Structural basis unchanged: `S189:155` and `S189:175` are both `Log::logger->log(Log::ERR, ...)`,
i.e. core-logger lines behind the Item-1 gate.

### Item 3a — the delta window since round-37: **PASS, and this is the genuinely new evidence**

r37's S213 receipt froze the log at `bytes: 4259033 / lines: 27331`. Since then the file grew:

```
now: 27609 lines / 4300419 bytes   (mtime 2026-10-25 11:28:38 -0300)
delta_bytes=41386  delta_lines=278
delta_core_lines=0
delta_socket2=0
total_core_lines=21
last_core_line_number=21
```

**278 new lines of real compositor activity in the window, and the core logger still wrote
nothing** — the core-line count is still exactly 21 and the last core line is still line 21.
Every new line is aquamarine. The delta's 278 lines contain 9 distinct aquamarine shapes, all
`DEBUG from aquamarine ]`.

This is stronger than r37's evidence on the growth axis: it is not a static file. The log
*is* moving, the gate *is* closed, and the zeros are not an artefact of a stale file.

### Item 3b — file vs rolling buffer lag: **CONFIRMED, unchanged shape**

Round-37 (ScoutRollingLog, item 4) found the file trails the in-memory rolling buffer. Re-measured
now:

```
file_bytes=4292103  rollinglog_bytes=4034
longest_rl_prefix_that_is_file_suffix=831   unflushed_bytes=3203
file_ends_with_newline=False
```

The last byte of the file is `G` (0x47), not `\n` — the file stops mid-line, and 3203 of the
rolling buffer's 4034 bytes are still unflushed. This reproduces r37's finding exactly
(1309/4041 flushed then; 831/4034 now). All 26 `rollinglog` lines *are* present in the file as
whole lines (`not_in_file=0`) — the flush lag is a partial-line tail, not missing content.

---

## Item 4 — `hyprctl rollinglog` prefix histogram (count only) — **PASS, no new channel**

```
$ hyprctl rollinglog | grep -oE '^[A-Z]+( from [a-z]+)? \]' | sort | uniq -c | sort -rn
     26 DEBUG from aquamarine ]
```

- 26 lines, **0** core lines (`^[A-Z]+ ]` with no `from`), 26 aquamarine.
- Markers in the rolling buffer: `Socket2 fd` 0, `Socket2` 0, `overflowed event queue` 0,
  `failed writing event` 0, `hung up` 0.
- Byte-identical shape to r37 (26 lines, 0 core, 4041 bytes then; 4034 bytes now —
  it is a live 4 KiB ring, hyprutils `ROLLING_LOG_SIZE`).
- Rolling-buffer sha256 `232b4876ef150e2abd895b4ee43b5ec57645b4717279428e740d972ab0e656f5`.

### Any NEW channel where the markers would land? — **NO. Exhaustively enumerated.**

I searched for a channel beyond the three r37 knew (file / journal / rollinglog):

| candidate channel | result |
|---|---|
| whole system journal | 0 `Socket2` |
| whole user journal (all units) | 0 `Socket2` |
| per-boot journals (all 4 boots) | 0 `Socket2` |
| `journalctl _COMM=Hyprland` | 0 `Socket2`; 102 lines, 42 core `DEBUG ]` |
| `journalctl _PID=1619` (the compositor) | 0 `Socket2`; 51 lines, 21 core `DEBUG ]` |
| `hyprctl rollinglog` | 0 `Socket2`, 0 core |
| coredumps (`coredumpctl list`) | no Hyprland entry (5 entries, none Hyprland) |
| `/tmp/hypr/` crash dir | does not exist |
| `~/.local/state/hyprland/` | exists, holds only `lastNag`, `lastVersion` — no logs |
| `~/.cache/hyprland/` | does not exist |
| any other `*hyprland*.log` on disk | only the one instance log (+ sibling agents' `/tmp` fixtures) |
| compositor fd table (`/proc/1619/fd/*`) | **exactly one** file fd, and it is the session log itself; stdout+stderr → `socket:[32004]`, which `/proc/net/unix` shows is the journald stdout socket → the unit journal, already counted |

The fd census is the decisive one: the compositor holds **one** regular-file descriptor
(`/run/user/1000/hypr/…_1792804449_426444678/hyprland.log`) plus stdout/stderr bound to the
journal socket. There is no fourth sink for a marker to appear in.

The only new *content* since r37 is more aquamarine bytes — a channel that cannot carry a core
marker by construction (S216:304-307 hands aquamarine the raw hyprutils logger, so it bypasses
the `m_logsEnabled` gate; it is a different logger, not the core one).

---

## Item 5 — Verdict on the claim under test: **STILL HOLDS**

`corpus/knowledge/event-queue-observability-r37.md` (the claim) asserts the markers cannot be
observed on this host. Every element of it re-verified:

| claim element | r38 recheck | status |
|---|---|---|
| `debug:disable_logs` = 1, default, never overridden | `{"int":1,"set":false}` | PASS |
| both markers are core-logger `ERR` lines | S189:155, :175 unchanged | PASS |
| core logger returns before every write | S214:15-16, :48 unchanged | PASS |
| session log's 21 core lines end at line 21 | still 21, still ends at line 21 | PASS |
| unit journal carries none of the runtime log | 0 markers; 42 core lines are all startup | PASS |
| `rollinglog` carries none of the core lines | 0 core, 26 aquamarine | PASS |
| zero ⇒ null channel, not "never overflowed" | positive probe satisfied: journal carries the same logger's startup lines and **zero** `ERR` core lines | PASS |
| flip condition (operator sets `disable_logs=false`) | unchanged, still operator-owned; not touched | unchanged |

The refusal of `event-queue-host-measurement-r28.md` and `event-queue-journal-measurement-r29.md`
(`corpus/lessons/round-38.md:40-41`) therefore still stands, and the r38 re-derivation adds one
thing r37 could not have: **278 lines of post-r37 growth with the gate still closed.**

---

## Item 6 — Two incidental observations (not part of the claim; reported, not acted on)

1. **The round-38 live receipt lost its provenance header.** r37's `eventq-live.txt` began with a
   comment line, `taken: 2026-10-25T09:19:03-03:00` and the `$ python3 -I tools/mado-eventq.py …`
   invocation line. r38's committed `eventq-live.txt` has **none** of the three:
   ```
   $ diff .ufo/waves/round-37/receipts/eventq-live.txt .ufo/waves/round-38/receipts/eventq-live.txt
   1,2d0
   < # eventq live receipt — tools/mado-eventq.py run read-only on this host
   < taken: 2026-10-25T09:19:03-03:00
   4d1
   < $ python3 -I tools/mado-eventq.py --snapshot-out .ufo/waves/round-37/receipts/eventq-live-ss.txt
   ```
   The `MADO_EVENTQ*` payload lines are byte-identical between the two rounds, so the counter's
   live clause still has what it parses. But the receipt no longer states **when** it was taken or
   **how** it was produced. The r38 `eventq-live-proc.txt` does keep a `taken: 2026-10-25` line and
   an `ss_sha256=` binding that matches the committed snapshot
   (`653311be6bb86efbe1d4448a102c4fb64666c1c6c9b63346d7a3e930ed147d3b` = `sha256sum` of the
   committed `eventq-live-ss.txt`), so the triplet is still internally consistent. The missing
   header is a **provenance regression, not a live-clause failure**. Flagging only; the counter's
   `live_check` does not require the header, and I am read-only here.

2. **The round-37 rolling-log follower orphan is still present.** `ss -xap` shows one
   `.socket.sock` ESTAB row held by the compositor at `fd=153` with peer inode `235508591` and
   `Recv-Q`/send-q 0 — exactly the leaked follower r37's ScoutRollingLog (side-effect section)
   and F9 documented. It survived the day. My own runs used only the **non-following**
   `hyprctl rollinglog` (no `-f`), and I verified afterwards that **no** new follower appeared:
   the `.socket.sock` ESTAB count is still 1 (the pre-existing `fd=153`), and `pgrep -a hyprctl`
   is empty. The orphan is r37's, not mine. Remediation needs a write verb or a compositor
   restart, both outside this seat.

---

## Bounds kept

- **Lane:** READ-ONLY on every lane production file. Wrote only this report and scratch under
  `.ufo/waves/round-38/w1/scratch/ScoutNullChannelRecheck/`. No `git add/commit/stash/checkout/
  reset/push` in LANE; no lane file edited. No git write at all (nothing needed a sandbox clone).
- **Compositor:** hyprctl **read verbs only** — `version`, `getoption` (×2), `rollinglog`
  (non-following). **No** socket connected: no `socat`, no `nc`, no python `socket`. `ss -xap`
  and `/proc` were read for the fd census; nothing was dialled.
- **System:** `pacman -Q` only (read-only query, no transaction). No pacman install — pacman is
  paused host-wide, and no tool was needed beyond stock `coreutils`/`procps`/`iproute2`/
  `systemd`/`jq`-free shell.
- **Tools installed or updated: none.**
- **Privacy:** counts, digests, prefixes and booleans only; no raw journal/log line text, no
  window titles. Socket inodes quoted only where the lane's own committed receipts already
  publish them.

## Scratch / receipts

- `.ufo/waves/round-38/w1/scratch/ScoutNullChannelRecheck/host-snapshot.txt` — log size, line
  count, delta window, core-line count, marker counts, log sha256.
- `.ufo/waves/round-38/w1/scratch/ScoutNullChannelRecheck/channel-snapshot.txt` — the two
  `getoption` JSONs, journal line count / marker count / core count / sha256, whole-user and
  whole-system journal marker counts, boot id, compositor pid + start, uptime.
- `.ufo/waves/round-38/w1/scratch/ScoutNullChannelRecheck/rollinglog.raw` — the 26-line
  `rollinglog` snapshot (sha256 `232b4876ef150e2a…`).
- `/tmp/mado38-ScoutNullChannelRecheck/delta.log` — the 278-line post-r37 delta window.

## Unresolved / limits

- The **fresh-epoch** test the brief asked for could not be performed, because no reboot has
  occurred. The only way to obtain a genuinely new epoch is a host reboot, which is outside
  this seat's bounds and is not mine to trigger. What I could do instead — and did — is extend
  the observation window over 278 lines of new activity on the *same* epoch, which is the
  strongest available form of this test short of a reboot.
- Whether a core marker would land if the gate opened **on this host** remains untested: that
  needs `debug:disable_logs = false`, an operator-owned write. The flip condition in
  `event-queue-observability-r37.md` is unchanged and still operator-owned.
- The r38 `eventq-live.txt` header loss (Item 6.1) means the round-38 live receipt cannot, on
  its face, establish its own capture time. Its payload is identical to r37's, and the
  `eventq-live-proc.txt` sibling still binds the snapshot digest, so the triplet is consistent —
  but a reader cannot tell from the receipt alone whether it was re-taken in round 38.
- I did not re-derive the `hyprutils` v0.14.2 source that r37 fetched from upstream, so I rely
  on r37's source reading for the rolling-buffer internals; my measurement of the buffer's
  behaviour (0 core lines, 26 aquamarine, 4 KiB ring, partial-flush lag) is first-hand.
