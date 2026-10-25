# ExecProcCrosscheck — mado round 37, wave 1 (executor)

Run window: 2026-10-25 ~12:13–12:17Z. Host: kernel 7.2.11-arch1-1, iproute2 ss 7.2.0, lsof 4.99.7, Python 3.14.8, wayland 1.26.0-1.
Hyprland instance `efb50993…` (pid 1619, parent `start-hyprland` 1614). The instance hash matches the S189 source commit `efb50993…` (renumber-map.md:19), so S189 line numbers apply to the running build.

## Verdict

**AGREE on both subscribers.** The `/proc`-only census, `ss -xpa` (captured three times) and `lsof +E` all report the same two event-socket subscribers, with the same pid, fd and inodes. Nothing disagrees.

| subscriber | client end (comm/pid/fd, inode) | compositor end (pid/fds, inode) | /proc vs ss | lsof |
|---|---|---|---|---|
| 1 | socat / 2293 / fd 5, ino 40790 | Hyprland / 1619 / fd 145 + 147, ino 10029 | AGREE | AGREE |
| 2 | waybar / 935660 / fd 21, ino 181143087 | Hyprland / 1619 / fd 236 + 250, ino 181151236 | AGREE | AGREE |

The listener is ino 38117, held by Hyprland at fd 10 + 11. socat 2293's parent is pid 1689 (`omarchy-hyprlan…`, child of Hyprland). waybar's parent is 1493.

## Deliverable

`.ufo/waves/round-37/w1/scratch/ExecProcCrosscheck/proc-census.py`, sha256 `f1f2c74e3728b2390774af961bc937a3c4149ae38656b118c3109394c416185a`. It:

- reads `/proc/net/unix` (inode, flags, type, state, path);
- scans `/proc/*/fd` symlinks for `socket:[N]`, plus `comm` and `Uid`;
- re-reads `/proc/net/unix` to confirm the socket2 rows did not change during the scan;
- classifies the rows bound to `$XDG_RUNTIME_DIR/hypr/<inst>/.socket2.sock` as the listener (`__SO_ACCEPTCON` flag `0x10000`) or accepted sockets (state 03);
- builds the candidate set of client ends;
- with `--ss FILE`, re-checks every claim in the `ss` capture against the `/proc` tables.

It creates no socket.

## Commands and quoted output

Two `ss -xpa` captures bracket the census run:

```
ss -xpa > ss-xpa.A.txt; python3 proc-census.py --ss ss-xpa.A.txt > census.A.txt   # rc=0
ss -xpa > ss-xpa.B.txt; python3 proc-census.py --ss ss-xpa.B.txt > census.B.txt   # rcB=0
```

`census.A.txt` comes from the first script revision (sha256 `7362091a…`). The only later change added the "no visible fd holder" line. Key lines from that output:

```
socket2 rows identical before/after fd scan: True
listener inodes: [38117]  accepted (St=03) inodes: [10029, 181151236]  other: []
compositor pid(s) (hold the listener): [1619]
  accepted 10029: held by Hyprland/1619/fd145, Hyprland/1619/fd147
  accepted 181151236: held by Hyprland/1619/fd236, Hyprland/1619/fd250
PROC-PROVES: 2 live accepted connection(s), all held only by the compositor: True
client-end candidates (unbound, stream, St=03, held outside compositor): 519; ...
heuristic H1 (nearest candidate inode to each server inode) — NOT a proof:
  server 10029 -> nearest 9903 (|d|=126) swayosd-server/1803/fd7
  server 181151236 -> nearest 181153240 (|d|=2004) waybar/935660/fd12
heuristic H2 (candidate holders whose cmdline names .socket2.sock) — NOT a proof: socat/2293
  server inode set: ss ESTAB [10029, 181151236] LISTEN [38117] vs proc [10029, 181151236] [38117] -> AGREE
  subscriber peer=40790: client socat/2293/fd5 | server 10029 Hyprland/1619/fd145, Hyprland/1619/fd147
    server-holders proc==ss: True; client-holders proc==ss: True; ss peer links back: True; peer row in /proc/net/unix unbound+stream+St03: True; peer in /proc candidate set: True; H1 picks it: False; H2 names its pid: True -> AGREE
  subscriber peer=181143087: client waybar/935660/fd21 | server 181151236 Hyprland/1619/fd236, Hyprland/1619/fd250
    server-holders proc==ss: True; client-holders proc==ss: True; ss peer links back: True; peer row in /proc/net/unix unbound+stream+St03: True; peer in /proc candidate set: True; H1 picks it: False; H2 names its pid: False -> AGREE
OVERALL: AGREE
```

Stability between the runs:

- `diff census.A.txt census.B.txt` differs only in the line counting socket inodes mapped to fds (988 vs 985).
- The socket2 lines of ss A and B are identical (`SS_A_B_SOCKET2_IDENTICAL`; the whole files have the same sha256, `f8efbc13…`).

The raw `ss` lines for socket2 (instance path shortened to `HYPR/`):

```
u_str ESTAB  0 0 HYPR/.socket2.sock 181151236 * 181143087 users:(("Hyprland",pid=1619,fd=250),("Hyprland",pid=1619,fd=236))
u_str LISTEN 0 10 HYPR/.socket2.sock 38117    * 0         users:(("Hyprland",pid=1619,fd=11),("Hyprland",pid=1619,fd=10))
u_str ESTAB  0 0 HYPR/.socket2.sock 10029     * 40790     users:(("Hyprland",pid=1619,fd=147),("Hyprland",pid=1619,fd=145))
u_str ESTAB  0 0 * 181143087 * 181151236 users:(("waybar",pid=935660,fd=21))
u_str ESTAB  0 0 * 40790     * 10029     users:(("socat",pid=2293,fd=5))
```

`lsof -n -w -U +E -a -p 1619` was a third reader, implemented independently of `ss`:

```
Hyprland 1619 vgpnk 145u unix 0x00000000e2ab75f5 0t0 10029 HYPR/.socket2.sock type=STREAM ->INO=40790 2293,socat,5u (CONNECTED)
Hyprland 1619 vgpnk 236u unix 0x00000000ee48d86d 0t0 181151236 HYPR/.socket2.sock type=STREAM ->INO=181143087 935660,waybar,21u (CONNECTED)
socat 2293 vgpnk 5u unix 0x00000000938c065a 0t0 40790 type=STREAM ->INO=10029 1619,Hyprland,147u 1619,Hyprland,145u (CONNECTED)
waybar 935660 vgpnk 21u unix 0x0000000090800e6d 0t0 181143087 type=STREAM ->INO=181151236 1619,Hyprland,250u 1619,Hyprland,236u (CONNECTED)
```

Read-only check: the census made zero network-class syscalls. Third run under strace, with the current script:

```
strace -f -qq -o strace.C.txt -e trace=%network python3 proc-census.py --ss ss-xpa.C.txt   # rc=0
network syscalls: 0          (strace.C.txt is empty, sha256 e3b0c442…)
strace -c: readlink 4696, openat 2908, getdents64 417 — file I/O only
census.C.txt: PROC-PROVES … True; unbound stream St=03 rows with no visible fd holder …: 51; OVERALL: AGREE
```

Run C matches run A except for churn in the candidate count (519 vs 508).

## What /proc can and cannot prove

**/proc can prove (no peer data needed):**

1. **How many live event-socket connections exist: exactly 2.** Every accepted connection creates one kernel socket that carries the listener's bound path (`/proc/net/unix` state 03, no `__SO_ACCEPTCON` flag). The table is kernel-wide and does not depend on whether fds are readable. Since a connection has exactly one server-side socket, the 2 rows mean exactly 2 connections.
2. **Who holds the server side: only Hyprland 1619.** All 3 socket2 inodes (the listener and both accepted sockets) are held there, and nowhere else.
3. **Which process holds any given inode, for every uid-1000 process.**
4. **Some per-fd state, from `fdinfo`.** Both client fds are blocking: socat fd 5 has flags `02000002`, waybar fd 21 has flags `02`. All six socket2 fds report `scm_fds: 0`.

**/proc cannot prove:**

1. **Which client inode is the peer of which server socket.** `/proc/net/unix` has no peer column, and its `Num` column is a hashed kernel address (`%pK`). `fdinfo` has no peer either. Only the `sock_diag` `UNIX_DIAG_PEER` attribute, read over netlink, provides it. strace shows both `ss` (`socket(AF_NETLINK, SOCK_RAW|SOCK_CLOEXEC, NETLINK_SOCK_DIAG)`) and `lsof` (`socket(AF_NETLINK, SOCK_DGRAM, NETLINK_SOCK_DIAG)`) use that interface. So `ss` and `lsof` are two userland implementations reading one kernel source; they are not independent at the kernel level.
2. **Pairing by heuristic is unsound, and this host shows it.**
   - Nearest-inode guessing (H1) picks the wrong client for **both** subscribers (swayosd-server fd 7; waybar fd 12 instead of fd 21).
   - The inode order is not even monotonic: server inode 10029 is *lower* than its client 40790. This fits per-CPU batched `get_next_ino()` [INFERENCE: kernel mechanism, not read].
   - Searching cmdlines (H2) finds socat, whose argv names the path, but misses waybar.
3. **Holders it cannot see.** 1291 pids had unreadable `fd` directories (other uids), and 51 connected unbound stream rows have no visible holder. A root process could reach the 0700 socket directory and would be invisible to unprivileged `/proc` and to `ss -p`.
   - This does not affect the count of 2 (point 1 above): `/proc/net/unix` lists those rows whether or not their holder's fds are readable.
   - It does not affect the pairing either, because both peers were found with uid-1000 holders.
   - Fds in flight via `SCM_RIGHTS` are also invisible; all socket2 endpoints report `scm_fds: 0`.
4. **Queue depth and stalled readers.** `/proc/net/unix` has no queue columns. `ss` reports the kernel's queues: Recv-Q and Send-Q were 0 on all four ESTAB endpoints in all three captures. The LISTEN line shows Recv-Q 0 (no un-accepted connections waiting) and Send-Q 10, which matches `listen(fd, 10)` at S189:35.

Hyprland's own userspace queue cannot be seen by `/proc`, `ss` or `lsof` (`m_clients[].events`, capped at `MAX_QUEUED_EVENTS = 64`, S189:169-177). It only starts filling after `write()` returns `EAGAIN` (S189:152-153), meaning after the kernel socket buffer is full (`wmem_default` 212992). So "Recv-Q 0 now" says nothing about past overflows. The only evidence that one happened is the absence of a client that should be present, together with the log line at S189:175. With `disable_logs = 1`, that log line is never written.

## Findings and risks

- **F1 — every event-socket fd is held twice by Hyprland.** This applies to the listener (10+11) and to each accepted socket (145+147, 236+250). The `wayland-1` client connection to waybar shows the same pattern (220+230). Each pair has identical fdinfo: flags `02004002`, same inode.
  - **Cause (peer-sourced, ScoutS189 report §7, not re-fetched by me):** libwayland 1.26.0 `src/event-loop.c` (sha256 `eabcb4d6…71b7`) duplicates the fd in `wl_event_loop_add_fd` (`source->base.fd = wl_os_dupfd_cloexec(fd, 0);` at :188). The duplicate is what epoll watches. The original fd is kept separately (:190) and passed to the callback (:113). `wl_event_source_remove` closes the duplicate (:836-841).
  - **My earlier lookup-miss lead is refuted.** The callback receives the original fd, which is the same value as `SClient.fd`, so `findClientByFD` at S189:106 and :120 does match.
  - Consequence for anyone parsing the overflow log: the "fd N" in `Socket2 fd N …` (S189:175) is `SClient.fd`, which is the original fd `accept4` returned. [INFERENCE] That is likely the lower fd of each pair (10, 145, 236): the dup takes the lowest free fd right after `accept4` takes its own, so it should land higher unless another thread frees a lower fd in between. This is not proven. ScoutS189 cautions that `F_DUPFD_CLOEXEC` with a minimum of 0 takes the lowest free fd (libwayland `wayland-os.c:133-145`), so number size alone proves nothing. Agreed: the dup lands lower only if an fd below the original is closed between S189:73 and :88. The gaps in the pairs (146, 237-249) show those slots were occupied, not that one was freed. Proof would need the order the fds were created, for example an `fd {}` line from S189:85 in the Hyprland log. That source isn't available: a read-only search of `$XDG_RUNTIME_DIR/hypr/<inst>/hyprland.log` (27332 lines) found **zero** `Socket2 …` lines of any kind (accept, hung up, overflowed, failed writing). The log header (line 13) says further logging is disabled by default. So the log can't settle the fd question, and the absence of overflow lines is not evidence that no overflow happened.
- **F2 — two subscribers, not one.** Besides waybar there is a long-lived `socat` reader (running about 126 ks, started by an omarchy helper under Hyprland). A tool or counter that assumes waybar is the only socket2 client is wrong on this host.
- **Risk:** this is a point-in-time census. waybar 935660 is a recent pid (its client inode 181143087 is far above socat's 40790), so the subscriber set has changed before and will change again.

- **Operator decision (not taken by this seat):** the only remaining way to see the order fds are created in (S189:85) or to get overflow evidence (S189:155, :175) is to re-enable Hyprland logging. That changes the host config, so it is the operator's call. ScoutS189 checked the log independently and agrees: 0 `Socket2` lines (report §7).

## Revision 12:18Z

F1 was revised after ScoutS189 replied with libwayland source citations. The doubled fds are now explained, and my lookup-miss lead is withdrawn. Nothing in the census, the per-subscriber verdicts or the digests changed.

## Bounds compliance

- No socket was opened by me or by the script; strace confirms 0 network syscalls. `ss`/`lsof` opened only kernel `NETLINK_SOCK_DIAG` sockets, as sanctioned for comparison.
- No hyprctl verb was used. No compositor, config, service or package was touched.
- Writes went only to `.ufo/waves/round-37/w1/scratch/ExecProcCrosscheck/` (script and census/strace outputs), to this report, and to `/dev/shm/mado37-ExecProcCrosscheck/`. The raw `ss`/`lsof` captures stay in `/dev/shm`, not the lane, because they list every socket on the host.
- No raw journal lines and no window titles are included. Only comm names, pids, fds and inodes appear.
- Tools installed or updated: **none**. strace, lsof, ss and python3 were already present. No pacman transaction was run (`pacman -Q wayland` is a read-only query).

## Evidence digests (sha256)

| file | sha256 |
|---|---|
| proc-census.py (final) | f1f2c74e3728b2390774af961bc937a3c4149ae38656b118c3109394c416185a |
| census.A.txt (scratch) | a9f7368385ced9d9080cf370c441b821205693986aca980e0ddb117cb85e52e8 |
| census.C.txt (scratch) | 2232e676aa2bf7aea47451a769222d04494b3b963bf1e5f43676fc278addbb17 |
| census.noss.txt (scratch) | ef8536d79ce3834fbc811c74e33e9992a8374cd169e308557899115ec02f95a7 |
| /dev/shm ss-xpa.A.txt = B.txt | f8efbc1377206ff5f65ab32e417daf841e1ae809a877e755272c95240ea7cf07 |
| /dev/shm ss-xpa.C.txt | 0cf704e1efacd8b31a239dc061f86642d8821ccd77f9168d136001f4d103cbea |
| /dev/shm lsof.txt | 909862c5eb4e3f34622996e0d7f40923c51681b9f7a0eddf1f57ada2313d8be6 |
| S189.bin (read) | eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d |

Suggested check for the parent: `python3 .ufo/waves/round-37/w1/scratch/ExecProcCrosscheck/proc-census.py --ss <(ss -xpa)` should end `OVERALL: AGREE`.
