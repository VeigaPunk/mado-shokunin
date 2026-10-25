# ScoutSsSemantics — what `ss -x` reports for a connected unix stream socket

Seat: L1Mado37-2.ScoutSsSemantics (scout, read-only). Access date for every source: 2026-10-25 (UTC).
No tool installs. No socket connection was made: `ss` reads the kernel table over sock_diag netlink and `/proc/<pid>/fd`.
Scratch: `/dev/shm/mado37-ScoutSsSemantics/` (fetched sources and snapshots; not committed).

## Verdict summary

| Item | Verdict |
|---|---|
| ss(8) defines Recv-Q / Send-Q / users for unix rows | **FINDING: silent.** No hits locally or on man7, so the semantics below come from source |
| Recv-Q/Send-Q meaning for ESTAB unix stream rows | **PASS (sourced):** Recv-Q is unread payload bytes queued to this socket. Send-Q is skb truesize charged to this socket and not yet freed by the reader |
| Recv-Q/Send-Q meaning for LISTEN rows | **PASS (sourced):** Recv-Q is pending unaccepted connections. Send-Q is the listen backlog (Hyprland: 10) |
| Peer inode column | **PASS (sourced):** the local "port" is the socket's own inode and the peer "port" is the peer's inode. The peer address is always `*` |
| users column | **PASS (sourced):** one `("comm",pid=N,fd=N)` tuple per (pid, fd) that holds the inode. The whole column is omitted when no readable `/proc/<pid>/fd` holds it |
| Live layout matches C2 assumption (9 columns) | **PASS** for all 5 socket2-related rows |
| Layout variants | **FINDING:** four variants (V1 to V4 below). None breaks the C2 live replay as currently shaped, but V1 to V3 break naive parsers |

## Sources opened

| Id | Source | Digest / version |
|---|---|---|
| M1 | `man 8 ss`, `/usr/share/man/man8/ss.8.gz`, iproute2 7.2.0-1 (`ss -V`: `ss utility, iproute2-7.2.0`) | sha256 `3fb6042b1cf695569d90882850fbfbc68cbd7f008878bf9b653362f6218e62dc` |
| M2 | https://man7.org/linux/man-pages/man8/ss.8.html (fetched 2026-10-25T12:13Z, HTTP 200) | sha256 `0e077ba9125e0fcf017fd61a404599249ec5960b0af310d755225817849ca069` |
| P1 | iproute2 `misc/ss.c` tag v7.2.0 (git.kernel.org plain), matching the installed package | sha256 `f618add5c99e92ccb6b869aeca4a783f2403492564cec450e22e3ea61f1b0b65` |
| K1 | linux-stable `net/unix/diag.c` tag v7.2.11 (host: `7.2.11-arch1-1`) | sha256 `7301e914d891fb96f9d900f25e771ae55f9304a6899ab31fe392eebbc6ff34d2` |
| K2 | linux-stable `include/uapi/linux/unix_diag.h` v7.2.11 | sha256 `f345038d1040d7e68690d09d4764663512a02fd70823513ae65d0e091def67a4` |
| K3 | linux-stable `net/unix/af_unix.c` v7.2.11 | sha256 `be715f595ce6de8a35afd185003b352ada21775d2a0a888de369131ad2deefc4` |
| K4 | linux-stable `net/core/sock.c` v7.2.11 | sha256 `338ce751c235573610a18c8316aca3b8852c98002d7e33cc6f4fcb34b5252249` |

The kernel sources are the upstream stable tag. Arch's `-arch1` patchset was not diffed, so treat K1 to K4 as matching the host only up to Arch's patches [INFERENCE: Arch rarely touches af_unix].

## Facts (each quote ≤25 words, location given, accessed 2026-10-25)

**F1. The man page is silent on queue and process columns.**
- Command: `MANWIDTH=200 man 8 ss | col -b | grep -c -E 'Recv-Q|Send-Q'` gave `local man Recv-Q hits: 0`.
- man7 (M2) gave `Recv-Q :: ABSENT`, `Send-Q :: ABSENT`, `users: :: ABSENT`.
- What it does say:
  - M1 l.119-120: "-p, --processes Show processes using sockets."
  - M1 l.276-277: "-x, --unix Display Unix domain sockets (alias for -f unix)."
  - M1 l.36-37: "-a, --all Display both listening and non-listening (for TCP this means established connections) sockets."
  - M1 l.77-78 (the `-e` field, not printed by `-xpa`): "<inode_number> the socket's inode number in VFS".

**F2. What ss asks the kernel for.** P1 `ss.c:4596`: `req.r.udiag_show = UDIAG_SHOW_NAME | UDIAG_SHOW_PEER | UDIAG_SHOW_RQLEN;`

**F3. Recv-Q and Send-Q come straight from the kernel's `unix_diag_rqlen` struct.**
- P1 `ss.c:4512-4513`: `stat.rq = rql->udiag_rqueue;` / `stat.wq = rql->udiag_wqueue;`
- They are printed as the Recv-Q and Send-Q columns at `ss.c:1470-1473` (`out("%-6d", s->rq);` … `out("%-6d", s->wq);`).
- The column titles are at `ss.c:148-154`: "Recv-Q", "Send-Q", "Local Address:", "Peer Address:", "Process".

**F4. The kernel fills those two values differently for LISTEN and non-LISTEN sockets.** K1 `diag.c:100-106`:
- LISTEN: `rql.udiag_rqueue = skb_queue_len_lockless(&sk->sk_receive_queue); rql.udiag_wqueue = sk->sk_max_ack_backlog;`
- Otherwise: `rql.udiag_rqueue = (u32) unix_inq_len(sk); rql.udiag_wqueue = (u32) unix_outq_len(sk);`

**F5. Stream Recv-Q is unread payload bytes.**
- K3 `af_unix.c:3254-3255`: `if (sk->sk_type == SOCK_STREAM) return READ_ONCE(unix_sk(sk)->inq_len);`
- The sender adds payload length to the receiver's counter at `:2487` (`WRITE_ONCE(otheru->inq_len, otheru->inq_len + skb->len);`).
- The reader subtracts what it consumed at `:3067` (`WRITE_ONCE(u->inq_len, u->inq_len - chunk);`).

**F6. Stream Send-Q is the sender's write-memory charge (truesize, not payload).**
- K3 `af_unix.c:3272-3274`: `long unix_outq_len(struct sock *sk) { return sk_wmem_alloc_get(sk); }`
- The stream send path allocates on the sender's socket (`:2437`, `sock_alloc_send_pskb(sk, ...)`), which calls `skb_set_owner_w(skb, sk)` (K4 `sock.c:3022`).
- That adds `skb->truesize` to the sender's `sk_wmem_alloc` (K4 `sock.c:2757`). The destructor `sock_wfree` (`:2750`) releases it when the reader frees the skb.
- Consequence [INFERENCE from F5 and F6]: for a socket2 pair, a nonzero Recv-Q on the client row comes with a nonzero Send-Q on Hyprland's server row. The two are in different units: client Recv-Q counts payload bytes, server Send-Q counts truesize including skb overhead, so server Send-Q ≥ client Recv-Q.
- Both counters see only the kernel buffer. Anything Hyprland queues in userspace after a write would block is invisible to `ss` [INFERENCE; S189 holds Hyprland's queue logic and other seats own it].

**F7. The inode and address columns.**
- Local port is the socket's own inode. P1 `ss.c:4503`: `stat.ino = stat.lport = r->udiag_ino;`
- Peer port is the peer's inode. P1 `ss.c:4529-4530` reads `UNIX_DIAG_PEER`, which K1 `diag.c:55-60` fills with `ino = sock_i_ino(peer)`. A row with no peer shows 0 (the LISTEN row: `* 0`).
- Peer address is always `*` in netlink mode. P1 `ss.c:4496` sets `struct sockstat stat = { .name = "*", .peer_name = "*" };` and the netlink path never resolves it. Only the `/proc/net/unix` fallback resolves peer names (`ss.c:4677-4687`). So a client row never names socket2: the only join is by inode.
- The local address on Hyprland's accepted (server-side) socket is the socket2 path, because the accepted socket inherits the listener's address. K3 `af_unix.c:1771-1772`: `refcount_inc(&otheru->addr->refcnt); smp_store_release(&newu->addr, otheru->addr);`
- The client socket is unbound, so its local address is `*`.

**F8. The users column.**
- It is printed only when an owner was found. P1 `ss.c:2469-2470`: `if (find_entry(s->ino, &buf, USERS) > 0) { out(" users:(%s)", buf);`
- Tuple format, one per (pid, fd) holding the inode, comma-joined. P1 `ss.c:731-733`: `"(\"%s\",pid=%d,%sfd=%d),"`. The `%s` before `fd` is empty unless `-T`, in which case it is `tid=N,`.
- Owners are found by reading `/proc/<pid>/fd/*` links that match `socket:[%u]` (`ss.c:574-596`).
- If a process's fd directory can't be opened, ss skips it silently. P1 `ss.c:566-569`: `dir = opendir(path); if (!dir) { freecon(task_context); return; }`
- comm comes from `/proc/<pid>/stat` via `fscanf(fp, "%*d (%[^)])", name)` into `char name[16]` (`ss.c:602-608`). So comm is at most 15 characters, may contain spaces, and stops at the first `)`.

**F9. The LISTEN Send-Q equals Hyprland's backlog.** S189.bin:35 (Hyprland v0.56.2 EventManager.cpp): `if (listen(m_socketFD.get(), 10) < 0) {`. The live LISTEN row shows Send-Q `10` (below).

## Live host check

Commands, run as uid 1000 at 2026-10-25T12:13Z:

```
ss -xpa > live-ss.txt                       # rc=0, stderr empty, 1102 lines (1 header + 1101 rows)
sha256sum live-ss.txt                       # 847a569b20f16218f79d21d83a2770d1ee3e583eca845c9fd65fbcfc2b20e153
grep -F .socket2.sock live-ss.txt           # 3 rows
```

The header, whitespace collapsed (the raw header right-pads the local address column):
`Netid State  Recv-Q Send-Q  …  Local Address:Port      Peer Address:Port     Process`

The C2 fixture `HDR` uses the same titles.

The socket2 rows (instance path `/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/.socket2.sock`, shown as `<S2>`):

```
u_str ESTAB  0 0  <S2> 181151236 * 181143087 users:(("Hyprland",pid=1619,fd=250),("Hyprland",pid=1619,fd=236))
u_str LISTEN 0 10 <S2> 38117     * 0         users:(("Hyprland",pid=1619,fd=11),("Hyprland",pid=1619,fd=10))
u_str ESTAB  0 0  <S2> 10029     * 40790     users:(("Hyprland",pid=1619,fd=147),("Hyprland",pid=1619,fd=145))
```

The matching peer rows, found where field 6 equals the server row's field 8:

```
u_str ESTAB 0 0 * 181143087 * 181151236 users:(("waybar",pid=935660,fd=21))
u_str ESTAB 0 0 * 40790     * 10029     users:(("socat",pid=2293,fd=5))
```

- **Inode cross-reference:** each server row's peer inode is the client row's local inode, and the client's peer inode points back. This holds for both pairs. **PASS.**
- **Column layout:** `Netid State Recv-Q Send-Q LocalAddr LocalInode PeerAddr PeerInode users` holds for all 5 rows (NF=9). **PASS.**
  - The C2 fixtures `SRV_W/CLI_W/SRV_S/CLI_S` (`quality/counters/c2-r37-eventq.py:52-55`) match these live comm/pid/fd values exactly; only the inodes are synthetic.
  - The fixture `LISTEN` row (`:51`) matches `LISTEN 0 10 <S2> <ino> * 0`.
- **Queues:** all 4 ESTAB rows are `0 0`. No subscriber had a kernel backlog at that instant.
- **Whole-table parse:** splitting each row with `split(None, 8)` and matching the users field against `users:\((\("[^"]*",pid=\d+,fd=\d+\),?)+\)` gave `maxsplit=8 parse failures: 0 of 1101`. The same pass found `rows field6 non-numeric: 0`, `rows field8 non-numeric: 0` and `peer col not *: 0`.

## Layout variants

- **V1 — more than one tuple in the users column.**
  - Both Hyprland server ESTAB rows and the LISTEN row carry two `Hyprland` tuples on two fds (250/236, 147/145, 11/10). [INFERENCE: dup'd fds]
  - 125 rows in the whole table carry two or more tuples.
  - The C2 fixtures only model single-tuple users. A regex anchored on `users:\(\("…",pid=N,fd=N\)\)` would miss these rows.
  - Client rows on socket2 are single-tuple today, so the C2 live replay (client triples) is unaffected. But a subscriber whose fd is inherited by a child would emit several (comm, pid, fd) tuples for one connection, and the count of subscribers is not the count of tuples.
- **V2 — users column missing.**
  - 291 of 1101 rows have NF=8 with no `users:` field.
  - Re-run read-only as root (`sudo -n ss -xpa`, rc=0): `0` rows lack users, and every one of the 291 inodes resolves.
  - Owning uids of the distinct pids holding them: 18× uid 0, 4× uid 1000, and the rest system uids (81, 969, 973, 974, 977, 61876).
  - So the cause is F8's silent `opendir` failure on another uid's `/proc/<pid>/fd`. It also hits 4 same-uid processes whose fd dirs are unreadable [INFERENCE: non-dumpable or in another user namespace].
  - A socket2 subscriber in that position would appear as a server ESTAB row whose peer row has no users field. It is still a subscriber, but with no comm, pid or fd. The C2 fixtures have no case for this.
- **V3 — comm with spaces.**
  - 31 rows have NF=11 or 13 because the comm contains spaces, for example `"omp daemon brok"`, `"npm exec chrome"` (15-character truncation visible).
  - Field-index parsing (`$9`, `split()[8:]` joined wrongly) breaks on these rows. `split(None, 8)` or a regex on the trailing `users:(...)` is safe.
  - `--expect-client COMM` must compare against the ≤15-character `/proc` comm. `waybar` (6 characters) is unaffected.
- **V4 — the peer address is never the socket path** (F7). Client rows read `* <ino> * <peer-ino>`, so a filter like `grep .socket2.sock` alone finds only Hyprland's side. Subscribers must be found by joining inodes. The fixtures already follow this (client rows use `*`).
- **Fixture note (not a layout variant).** C2 case `lagging` (`c2-r37-eventq.py:85`) gives the client Recv-Q 2048 while the paired server row keeps Send-Q 0. Per F5 and F6 the kernel would show server Send-Q > 0 in that state. This is harmless for a tool that reads `peer_recv_q` from the client row, but a tool that cross-checks the two counters would fail a frozen fixture.

## Remaining unknowns

- Arch's `7.2.11-arch1-1` patch delta against the upstream af_unix and diag code was not checked.
- Whether Hyprland's two fds per socket come from `dup` or from fd inheritance was not checked. It is cosmetic for C2.
- `ss -p` reads `/proc` and the netlink dump separately, so a socket created or closed between the two reads can show without users [INFERENCE from `ss.c:643-695` building the table before the dump; not observed].
