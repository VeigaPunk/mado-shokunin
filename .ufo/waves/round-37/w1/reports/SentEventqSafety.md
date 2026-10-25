# SentEventqSafety — sentinel, mado round 37 wave 1

Scope: security and privacy review of the C2 contract (`registration.md` C2 section + Amendment 1,
`quality/counters/c2-r37-eventq.py` = `PRED-C2-r37-v2`) on four items: ss snapshot exposure,
journal privacy, compositor-stall paths (incl. `hyprctl getoption` vs S186), subprocess hygiene.
Read-only throughout. No Hyprland socket was connected by me; the only compositor contact was two
one-shot read verbs (`hyprctl getoption debug:disable_logs -j`, `hyprctl version -j`).
Scratch: `/dev/shm/mado37-SentEventqSafety/` (counts-only scripts, upstream source copies). No tool
installed or upgraded. Two upstream files fetched read-only with curl (not committed anywhere):
`src/debug/HyprCtl.cpp` sha256 `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`,
`hyprctl/src/main.cpp` sha256 `f6b0d1fcfc6695194c70964250591a35ffe90274309303d8f5fd0ac6f8c1c93f`,
both at Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f` — the same commit as S189 and the
host build (`hyprctl version -j` → `v0.56.2 efb509937800`).

## Verdict summary

| # | Item | Verdict | Severity | Contract line it changes |
|---|------|---------|----------|--------------------------|
| F1 | Raw `ss -xpa` snapshot committed to a public repo | finding | Medium (High if a full dump lands) | registration.md:116 ("committed raw `ss -xpa` snapshot") |
| F2 | `readonly` clause is static and bypassable | finding | Low | c2-r37-eventq.py:11, :180-182 (v3 only; reviewer gate now) |
| F3 | One-shot `hyprctl getoption` vs S186 freeze rule | PASS (safe) | Info | registration.md:55 (add timeout + "one-shot, never `-f`") |
| F4 | No subprocess timeouts in the contract | finding | Low | registration.md:52-55 |
| F5 | Journal default lacks `-o cat` and `-b` | finding | Low (latent on this host) | registration.md:53-54 |
| F6 | Marker counts spoofable by logged untrusted text | finding | Low | registration.md:49-50 (marker definition) |
| F7 | Journal/log privacy: output is counts only | PASS, one gap | Info | registration.md:60 (`SETUP <reason>`), receipt content |
| F8 | Counter subprocess hygiene | PASS, one gap | Low | c2-r37-eventq.py:118 (env not scrubbed; v3 only) |
| F9 | Orphan request-socket connection on the host | side finding | Info | none (tool must never use `rollinglog -f`) |
| F10 | `HYPRLAND_INSTANCE_SIGNATURE` path join | finding | Info | registration.md:54 (`<instance>`) |

## (1) ss -xpa exposure and the minimal snapshot — F1

What a raw snapshot carries, measured on this host (`/dev/shm/mado37-SentEventqSafety/sscount.py`,
counts only; `ss -V` → `ss utility, iproute2-7.2.0`):

```
ss_bytes=205067 sha256=6068cdace3743f42 header_ok=True
rows=1085 rows_with_users=794 distinct_comms=66 abstract_addr_fields=131 path_addr_fields=301
rows_matching_sensitive_pattern=254
socket2_rows=3 (listen=1 estab=2) client_rows=2 request_socket_rows=2
minimal_snapshot_lines=6
subscriber comm=waybar recv_q=0 send_q=0
subscriber comm=socat recv_q=0 send_q=0
```

(`sensitive_pattern` = rows naming ssh/gpg/keyring/agent/dbus/pipewire/browser/editor/terminal/
password-manager sockets.) Where it would land: `gh repo view VeigaPunk/mado-shokunin --json
visibility,isPrivate` → `{"isPrivate":false,"visibility":"PUBLIC"}`. Lane scratch is not ignored:
`git check-ignore -v .ufo/waves/round-37/w1/scratch/x.txt` → `ignored_rc=1`, and
`git ls-files .ufo/waves | rg -c '/scratch/'` → `971` tracked scratch files. So a raw dump written to
lane scratch or `receipts/` is one commit away from a public inventory of every process name, pid and
filesystem/abstract socket name owned by the user.

Exploit path: Amendment 1 (registration.md:116) literally asks for "the committed raw `ss -xpa`
snapshot". An L1 following that wording commits ~1085 rows to the public repo. Impact: host process
inventory (66 programs, which apps run), 131 abstract socket names (abstract sockets have no
filesystem permission; any local process in the same network namespace can connect to a known name
unless the server checks peer credentials, so publishing names removes obscurity some apps rely on),
and 301 filesystem socket paths (agent/keyring locations). Running `ss` under `sudo` would add other
users' processes (non-root `-p` shows only own processes: 794 of 1085 rows carry `users:`).

The raw form buys no falsification power: the counter (c2-r37-eventq.py:153-176) only replays the
snapshot and compares (comm, pid, fd) triples; it never checks rawness, so a filtered snapshot of
verbatim rows replays to the identical triple set, and a raw snapshot is exactly as hand-writable
as a filtered one.

Proposed maximum for a committed snapshot (`--snapshot-out`), verbatim lines only, no field edits:
1. the ss header line (`Netid …`), required for the `ss_unparseable` check;
2. the socket2 LISTEN row (Local Address ends `/.socket2.sock`);
3. every ESTAB row whose Local Address is that socket2 path (server side, `users:(("Hyprland",…))`);
4. every row whose Local inode equals a server row's Peer inode (the subscriber side).

On this host that is 6 lines (`minimal_snapshot_lines=6`). Must never be committed: any other row —
request-socket (`.socket.sock`) rows, other processes' rows, abstract `@…` names, other socket paths,
any output of `sudo ss`, and any full `ss -xpa` dump (also not into lane scratch, which is tracked).

Current artifacts comply (counts only):
```
scratch/ExecEventqA/live-ss.txt lines=6 users_rows=5 distinct_comms=3 comms_outside_{Hyprland,waybar,socat,hyprctl}=0 abstract_rows=0
reports/ScoutWaybarDrop.md lines=176 users_rows=2 distinct_comms=1 comms_outside_{...}=0 abstract_rows=0
reports/ScoutSsSemantics.md lines=144 users_rows=5 distinct_comms=3 comms_outside_{...}=0 abstract_rows=0
```
ExecEventqA's prompt (`w1/prompts/ExecEventqA.md:8`) already specifies exactly rows 1-4.

Smallest remediation: an append-only clarifying amendment replacing "committed raw `ss -xpa`
snapshot" (registration.md:116) with "the verbatim socket2 rows of one live `ss -xpa` run, written by
the tool's `--snapshot-out` (header, socket2 LISTEN, socket2 server ESTAB rows, their peer rows)". It
changes no counter byte, so it is not a new predicate. Pre-commit gate for the L1: every line of
`receipts/eventq-live-ss.txt` is the header or has Local Address = socket2 path or Local inode ∈ the
server rows' Peer inodes.

## (2) journalctl privacy — F7 (PASS, one gap), F5, F6

Output grammar (registration.md:56-60) is counts only: `MADO_EVENTQ_MARKERS: source= overflow=
write_fail=` and the summary carry integers, the socket2 path, comm/pid/fd of subscribers and fixed
verdict tokens. No line echoes a log or journal line. Both executor candidates print no journal text:
SETUP strings are `journal_unreadable` (A, `scratch/ExecEventqA/mado-eventq.py:244`) and
`Setup(reason, f"{cmd[0]}: rc={p.returncode}")` / `type(e).__name__` (B, `…ExecEventqB/mado-eventq.py:153-155`).
PASS.

Gap: registration.md:60 leaves `SETUP <reason>` free text, and the counter does not restrict what
else `receipts/eventq-live.txt` contains (c2-r37-eventq.py:156-158 only selects prefixed lines).
Remediation: reasons are an enumerated token plus at most a path/count/errno name (both candidates
already do this); the committed receipt is the tool's stdout plus one `tool_sha256=` line, nothing
pasted by hand.

F5 — the frozen live default `journalctl --user -u wayland-wm@hyprland.desktop.service`
(registration.md:53-54) has no `-o cat` and no `-b`. Measured:
```
journal short_lines=716 cat_lines=717
journal-b short_lines=351 cat_lines=351
short_lines_starting_ERR_or_DEBUG=0 cat_lines_starting_ERR_or_DEBUG=21
3            # journalctl --user --list-boots | wc -l
```
The default short format prefixes timestamp, hostname and process[pid] (more data than needed, and
it breaks any matcher anchored at the level token: 0 vs 21 lines). Without `-b` the count spans three
boots, so a marker from an earlier compositor instance would flag `MARKERS` today. Latent on this
host because `debug:disable_logs` is 1. Both candidates add `--no-pager -q -o cat` (A:242,
B:97); neither adds `-b`. Remediation: default `journalctl --user -u wayland-wm@hyprland.desktop.service
--no-pager -q -o cat -b` (`-o cat` also minimises what is read).

F6 — the markers come from the compositor log, which also logs client-supplied strings. A client
that sets a string containing `Socket2 fd 3 overflowed event queue, removing` (e.g. a window title,
[INFERENCE] that the title reaches a DEBUG line when logs are enabled) makes an unanchored matcher
count an overflow: false `MARKERS`, never a hidden real one. Candidate A uses an unanchored search
(`A:92-93`); B anchors the tail only (`B:119-120`). The host log format allows full anchoring:
```
log_lines=27331 level_prefixed=27332 bracket_time_prefixed=0 core_level=21 log_mode=644
journal_cat_level_prefixed_b=21
```
Remediation: match `^ERR \]: Socket2 fd \d+ overflowed event queue, removing$` and
`^ERR \]: Socket2 fd \d+ failed writing event: ` on log lines and `-o cat` journal lines (fixtures
`OVERFLOW`/`WRITEFAIL`, c2-r37-eventq.py:64-65, already have that shape). If `debug:disable_time` = 0
adds a time prefix, allow an optional leading bracket group ([INFERENCE]: not observed here,
`bracket_time_prefixed=0`).

## (3) Can the tool block or stall the compositor — F3 PASS, F9

Paths the contract allows and their effect on Hyprland:
- `ss -xpa`: kernel sock_diag netlink plus `/proc/*/fd` readlinks; touches no socket queue. No stall.
- Session log and journal: plain file reads / `journalctl` against journald. No compositor contact.
- `hyprctl getoption debug:disable_logs -j`: this IS a request-socket client (S186
  `content/ipc/_index.md:14-19`), so the freeze rule applies to it. Quote, S186 bytes at
  `.ufo/waves/round-32/fetch/S186.bin` (sha256 prefix `535bc4c385a06162`, matching SOURCES.md:198):
  > :22 `Hyprland evaluates connections to this socket completely synchronously, which means that any unclosed connections *will cause Hyprland to freeze* until the five-second timeout is reached.`
  > :23 `Ensure that you always open the socket immediately before writing requests and close it afterward.`

  Server side at the host's commit (`HyprCtl.cpp`): `:2242` `accept4(...)`; `:2264` `int ret = poll(pollfds, 1, 5000);`;
  `:2266-2268` close on timeout; `:2274` one `read(…, 1023)`, loop ends `:2279` when fewer than 1023
  bytes arrive; `:2305` `successWrite(ACCEPTEDCONNECTION, reply);` with `:2174`
  `constexpr const size_t MAX_WAITS = 20; // 2000µs = 2ms` bounding the reply write; `:2313`
  `close(ACCEPTEDCONNECTION);`. Client side (`hyprctl/src/main.cpp`): `:209-210` 5 s `SO_RCVTIMEO`;
  `:234` `connect(...)` is followed directly by `:239` `writeAll(SERVERSOCKET, arg)`; `:253-271`
  read until the server closes; `:273` close.

  So the only freeze window is the gap between hyprctl's `connect` and its `write` — instructions
  apart, and capped at 5000 ms by `:2264` even if hyprctl were stopped exactly there (e.g. job-control
  stop of the tool's process group; [INFERENCE], not reproduced — reproducing it would mean stalling
  the compositor). The request is ~30 bytes (one read), the reply is ~55 bytes (bounded write). Killing
  hyprctl on a subprocess timeout closes its fd, `poll` returns, `read` returns 0, the server
  replies into a dead socket and closes. Measured one-shot:
  ```
  {"option":"debug:disable_logs","int":1,"set":false} rc=0
  real	0m0.008s
  ```
  Verdict: a one-shot `getoption` is safe. It must stay one-shot: never `rollinglog -f`/`--follow`
  (`main.cpp:422`, handled by `HyprCtl.cpp:2307-2310` as a long-lived connection with a writer
  thread), never a hand-rolled request-socket client, never a loop. (`"set":false` also says the
  value 1 is the compiled default, not a host config choice — stock hosts have unobservable markers.)
- Event socket: the contract never connects. A subscriber that stops reading is the client
  S189 `EventManager.cpp:169-175` evicts (`MAX_QUEUED_EVENTS = 64`, `overflowed event queue, removing`).

F9 (side finding, Info): the request socket currently has a Hyprland-side ESTAB row whose peer inode
is 0, still present 2 s later:
```
LISTEN 0 10
ESTAB 0 0
peer_inode=0
users_on_server_row=1
after2s peer_inode=0
```
[INFERENCE] It is a `rollinglog -f` follower whose client exited: the follow thread
(`HyprCtl.cpp:2205-2223`) closes only after a failed write, and with `debug:disable_logs` = 1 no log
line is written, so it never notices. It does not freeze the event loop (it is held by the thread, not
by `hyprCtlFDTick`). The tool must not count it: it sits on `.socket.sock`, which the fixtures
already exclude (`REQ_*`, c2-r37-eventq.py:56-58). Messaged to `L1Mado37-2.ScoutRollingLog`.

Update 12:20Z: ScoutRollingLog confirms and attributes it to its own `timeout 4 hyprctl rollinglog -f`
run at about 12:13Z (its report, "Side effect" section). Attribution comes from the run record; the
inode and fd alone cannot prove it. Its mechanism matches: the follow feed (S214:21-22) sits behind
the `m_logsEnabled` return (S214:15-16). Re-checked read-only:
```
local_inode=235508591 peer_inode=0 holder=Hyprland pid=1619 fd=153
0            # pgrep -c -x hyprctl
```
Lesson for the contract and briefs: the 5 s cap (HyprCtl.cpp:2264) does not bound `-f`, and a
`timeout`-killed follower still leaves one fd and one idle thread in the compositor until logs are
turned on or Hyprland restarts. Future briefs on this host should forbid `rollinglog -f` outright.
Cleanup needs a write verb or a restart, so it is left to the L1 or the operator; I did not touch it.

## (4) Subprocess hygiene — F4, F8, F2, F10

Contract: registration.md:52-55 names the three live commands but no timeouts, no `stdin`, no argv
form. F4 (Low): without a timeout, a wedged compositor whose request-socket backlog (10, `LISTEN 0 10`)
is full can hold hyprctl in `connect` (hyprctl sets no connect timeout, `main.cpp:202-234`), and the
tool hangs with it; journal reads are unbounded across boots. Only the tool stalls, not the compositor.
Both candidates use list argv, `stdin=subprocess.DEVNULL`, `capture_output`, and a timeout:
A `LIVE_TIMEOUT = 90` (`A:95`, `A:104-105`), B `LIVE_TIMEOUT = 30` (`B:101`, `B:150-151`, `B:256-257`).
On timeout CPython 3.14.8 `subprocess.run` does `process.kill()` then `process.wait()` (POSIX branch),
so hyprctl's fd is closed and no grandchild pipe can hang the tool. Remediation (registration.md:52-55):
argv lists, never `shell=True`, `stdin=DEVNULL`, timeouts per command (hyprctl ≤ 6 s, just over its own
5 s read timeout; `ss` 10 s; `journalctl` 30 s), each run only when its file flag is absent.

F8 (counter, c2-r37-eventq.py): PASS on argv lists and no shell (`:102`, `:116-118`, `:166-169`),
`timeout=20` on every tool run, fixtures in a `/dev/shm` `mkdtemp` (0700) removed in `finally`. Gaps:
`git` calls at `:102` have no timeout (local repo, Low); the tool runs with the full ambient environment
(`:118`, `:166`: no `env=`), so `HYPRLAND_INSTANCE_SIGNATURE`, `XDG_RUNTIME_DIR` and `PATH` reach it
during fixture runs and a tool that also goes live while given all four file flags is not caught. v3
only (the counter is frozen): run fixtures with `env` stripped of those three variables.

F2 (Low): the `readonly` clause (`:11`, `:180-182`) is a necessary-not-sufficient text check. Applying
its exact predicate to snippets (`/dev/shm/mado37-SentEventqSafety/readonly_probe.py`, static, nothing
executed):
```
readonly=0 import socket
readonly=0 s.connect(path)
readonly=1 import os, socket
readonly=1 __import__('socket')
readonly=1 importlib.import_module
readonly=1 asyncio.open_unix_connection
readonly=1 multiprocessing Client
readonly=1 subprocess socat
readonly=1 subprocess hyprctl dispatch
readonly=1 subprocess hyprctl rollinglog -f
readonly=1 getattr connect
```
Every `readonly=1` line connects to a socket or mutates/holds the compositor yet passes. Neither
candidate does any of this (their only subprocesses are `ss -xpa`, the journal read and
`hyprctl getoption debug:disable_logs -j`: `A:200,221,242`, `B:96-99`). Remediation now: reviewer gate
on the landed tool — imports ⊆ stdlib without `socket`/`asyncio`/`multiprocessing`/`importlib`, no
`__import__`/`getattr(…connect…)`, and every subprocess argv is exactly one of the three. v3: the same
as an AST check in the counter.

F10 (Info): both candidates build the instance dir with `os.path.join(base, sig)` (`A:121-125`,
`B:172-176`); an absolute or `..` `HYPRLAND_INSTANCE_SIGNATURE` points the log read elsewhere. Read-only
and same-user, so no escalation; remediation: reject a signature containing `/`. Host:
`instance_dirs=1 his_env_set=1 dir_mode=700`.

## Commands run

- `sed -n '1,35p' .ufo/waves/round-32/fetch/S186.bin`, `awk 'NR==198' corpus/SOURCES.md`
- `rg -n 'overflowed|failed writing|MAX_QUEUED|…' .ufo/waves/round-37/fetch/S189.bin`; `cat -n …/S214.bin`
- `curl -fsS --max-time 30 https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/{src/debug/HyprCtl.cpp,hyprctl/src/main.cpp}` → `/dev/shm/mado37-SentEventqSafety/`
- `python3 /dev/shm/mado37-SentEventqSafety/sscount.py` (runs `ss -xpa`, prints counts and socket2 subscriber comms only)
- `ss -xpa | awk '$5 ~ /\/hypr\/.*\/\.socket\.sock$/ …'` (state and peer inode only)
- `timeout 3 hyprctl getoption debug:disable_logs -j` (timed), `hyprctl version -j`
- `journalctl --user -u wayland-wm@hyprland.desktop.service --no-pager -q [-b] [-o cat] | wc -l` and `grep -c` on level prefixes; `journalctl --user --list-boots | wc -l`
- `grep -c` / `stat` on `$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/hyprland.log`
- `gh repo view VeigaPunk/mado-shokunin --json visibility,isPrivate`; `git check-ignore -v`; `git ls-files .ufo/waves | rg -c '/scratch/'`
- `python3 -I /dev/shm/mado37-SentEventqSafety/readonly_probe.py`
- `rg` over both executor candidates (read-only static inspection)
