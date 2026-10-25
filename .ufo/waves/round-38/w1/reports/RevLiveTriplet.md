# RevLiveTriplet — independent re-derivation of the round-38 live triplet

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` (LANE). Leaf member, no subagents dispatched.
Scope: the three receipts under `LANE/.ufo/waves/round-38/receipts/` — `eventq-live.txt`,
`eventq-live-ss.txt`, `eventq-live-proc.txt` — re-derived live on 2026-10-25 ~11:15–11:20 local,
~15 min after the freeze commit. All lane paths below are relative to LANE.

**Verdict: PASS on all three items — every line SAME, none moved, none mismatched. No findings.
The committed triplet is not merely replayable; the live system state is still byte-identical to
the frozen evidence. No honest-aging caveat is needed (no new instance epoch, no new client).**

Bounds compliance: read-only throughout; no socket connection (no socat/nc/python socket);
hyprctl used only for the read verb `getoption`; no git writes in LANE (only `git log`/`status`
reads); no tool installs were needed (record: none installed).

---

## Item 1 — `eventq-live.txt` vs my own tool run

Command (exact):
```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I tools/mado-eventq.py
```
My full output (scratch: `/tmp/mado38-RevLiveTriplet/eventq-live-now.txt`), exit=0, stderr empty:
```
MADO_EVENTQ_CLIENT: comm=waybar pid=935660 fd=21 peer_recv_q=0 server_send_q=0 server_fd=250,236
MADO_EVENTQ_CLIENT: comm=socat pid=2293 fd=5 peer_recv_q=0 server_send_q=0 server_fd=147,145
MADO_EVENTQ_MARKERS: source=log:/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/hyprland.log overflow=0 write_fail=0 fds=-
MADO_EVENTQ_MARKERS: source=journal overflow=0 write_fail=0 fds=-
MADO_EVENTQ: socket2=/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/.socket2.sock subscribers=2 overflow=0 write_fail=0 lagging=0 missing_client=- markers_observable=no verdict=CLEAN
```

Line-by-line (receipt line → status → reason):

| # | Receipt line | Status | Reason / evidence |
|---|---|---|---|
| 1 | `tool_sha256=436f550e9939a783b7b95d154d099b788ad9daaed2282e19de89413e39371f24` | **SAME** | `sha256sum tools/mado-eventq.py` → `436f550e9939a783b7b95d154d099b788ad9daaed2282e19de89413e39371f24`. Tool unchanged since freeze; the "expected to differ only if tool changed" branch did not materialize. |
| 2 | `MADO_EVENTQ_CLIENT: comm=waybar pid=935660 fd=21 … server_fd=250,236` | **SAME** | Byte-identical in my run. Cross-checked in /proc: `readlink /proc/935660/fd/21`-equivalent scan → `socket:[181143087]`, which is the peer inode of server ESTAB row 181151236 (`server_fd=250,236` matches the ss holders below). |
| 3 | `MADO_EVENTQ_CLIENT: comm=socat pid=2293 fd=5 … server_fd=147,145` | **SAME** | Byte-identical. fd scan → `socket:[40790]`, peer of server ESTAB inode 10029 (holders fd 145/147). |
| 4 | `MADO_EVENTQ_MARKERS: source=log:… overflow=0 write_fail=0 fds=-` | **SAME** | Independent recount, counts only (no lines printed): `grep -cE 'Socket2 fd [0-9]+ overflowed event queue, removing' <log>` → `0`; same for `failed writing event` → `0`. Log file present, 4292103 bytes, mtime Oct 25 11:07 (post-dates the receipt and still 0/0). |
| 5 | `MADO_EVENTQ_MARKERS: source=journal overflow=0 write_fail=0 fds=-` | **SAME** | `journalctl --user -u wayland-wm@hyprland.desktop.service --no-pager -q -o cat \| grep -cE <marker>` → `0` and `0`. |
| 6 | `MADO_EVENTQ: socket2=… subscribers=2 overflow=0 write_fail=0 lagging=0 missing_client=- markers_observable=no verdict=CLEAN` | **SAME** | Byte-identical. `markers_observable=no` re-verified independently: `hyprctl getoption debug:disable_logs -j` → `{"option": "debug:disable_logs", "int": 1, "set": false }` (read verb) — logs disabled, so zero markers means "not logged", exactly as the tool's docstring defines. |
| 7 | `exit=0` | **SAME** | My run exited 0. (This line and line 1 are receipt-author wrappers, not tool stdout — the tool prints only the 5 `MADO_EVENTQ*` lines.) |

Formal diff: `diff` of committed body (minus the two wrapper lines) vs my output → empty
("identical"). Receipts committed in `58e55ec` ("round-38: freeze … live triplet …") = HEAD;
`git status --porcelain` on `receipts/` + `tools/mado-eventq.py` → 0 lines (no uncommitted drift).

## Item 2 — `eventq-live-ss.txt` vs my own `ss -xpa`

Command (exact): `ss -xpa | grep -F .socket2.sock`

My live rows (scratch: `/tmp/mado38-RevLiveTriplet/ss-now.txt`):
```
u_str ESTAB  0      0      /run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/.socket2.sock 181151236            * 181143087 users:(("Hyprland",pid=1619,fd=250),("Hyprland",pid=1619,fd=236))
u_str LISTEN 0      10     /run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/.socket2.sock 38117                * 0         users:(("Hyprland",pid=1619,fd=11),("Hyprland",pid=1619,fd=10))
u_str ESTAB  0      0      /run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/.socket2.sock 10029                * 40790     users:(("Hyprland",pid=1619,fd=147),("Hyprland",pid=1619,fd=145))
```

- The 3 socket2 rows in the committed file (`grep -F .socket2.sock eventq-live-ss.txt`) diff
  **byte-identical** against my live rows. Inodes 181151236 / 38117 / 10029 and peer inodes
  181143087 / 0 / 40790 all unchanged → **SAME** (not moved: same kernel inode numbers mean the
  same socket objects, not re-created ones).
- Client rows are present in the committed dump and pair correctly with the server rows:
  `* 181143087            * 181151236 users:(("waybar",pid=935660,fd=21))` and
  `* 40790                * 10029     users:(("socat",pid=2293,fd=5))` → **SAME**.
- The committed file is a full `ss -xpa` dump (1011 lines), not the tool's 7-line snapshot; a
  whole-file diff against today is meaningless because ~1000 unrelated sockets (browsers etc.)
  churn by design. The load-bearing content — socket2 server rows + their peer rows — matches
  byte-for-byte, which is the claim under test.
- Backlog: Recv-Q/Send-Q are 0 on every socket2 ESTAB row (LISTEN Send-Q 10 = backlog), so
  `lagging=0` in Item 1 is corroborated at the kernel level.

## Item 3 — `eventq-live-proc.txt` re-derived from `/proc/net/unix` + `/proc/<pid>/fd`

Command (exact): `grep -F .socket2.sock /proc/net/unix`, then a read-only scan of
`/proc/[0-9]*/fd` readlinks for `socket:[<inode>]` (no socket connection).

My live `/proc/net/unix` rows:
```
00000000ee48d86d: 00000003 00000000 00000000 0001 03 181151236 /run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/.socket2.sock
00000000703bc932: 00000002 00000000 00010000 0001 01 38117 /run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/.socket2.sock
00000000e2ab75f5: 00000003 00000000 00000000 0001 03 10029 /run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/.socket2.sock
```

Claim-by-claim (receipt → status → my re-derivation):

| Receipt claim | Status | Re-derivation |
|---|---|---|
| server ESTAB inode=181151236, `/proc/net/unix` row as quoted | **SAME** | Row verbatim identical (same hash prefix `ee48d86d`, state 03, inode). |
| holders: Hyprland/1619/fd236, Hyprland/1619/fd250 | **SAME** | fd scan: `pid=1619 comm=Hyprland fd=236` and `pid=1619 comm=Hyprland fd=250`, no other holder. |
| server LISTEN inode=38117, row as quoted | **SAME** | Row verbatim identical (`703bc932`, inode 38117). |
| holders: Hyprland/1619/fd10, Hyprland/1619/fd11 | **SAME** | fd scan: `pid=1619 comm=Hyprland fd=10`, `fd=11`, no other holder. |
| server ESTAB inode=10029, row as quoted | **SAME** | Row verbatim identical (`e2ab75f5`, inode 10029). |
| holders: Hyprland/1619/fd145, Hyprland/1619/fd147 | **SAME** | fd scan: `pid=1619 comm=Hyprland fd=145`, `fd=147`, no other holder. |
| `compositor pids holding socket2 inodes: ['1619']` | **SAME** | Across all three server inodes the only holder pid found is 1619. |
| "every socket2 server inode present in /proc/net/unix and held only by the compositor" | **SAME** | All three inodes present in `/proc/net/unix`; holder scan exclusive to 1619. |
| `OVERALL: AGREE` | **SAME** | Re-derived AGREE from the above. |
| `ss_sha256=653311be6bb86efbe1d4448a102c4fb64666c1c6c9b63346d7a3e930ed147d3b` | **SAME** | `sha256sum eventq-live-ss.txt` → `653311be…147d3b`. Note: this pins the **ss snapshot file**, not the ss binary (`/usr/bin/ss` = `b5956b0c…ded8b`) — the label is ambiguous but the digest resolves to the snapshot. |

Client-side closure (beyond the receipt's own claims): `socket:[181143087]` is held only by
`pid=935660 comm=waybar fd=21`; `socket:[40790]` only by `pid=2293 comm=socat fd=5` — exactly the
two CLIENT rows of Item 1, so the proc receipt, the ss receipt, and the tool output form one
consistent triplet with no orphan or extra endpoint.

## Aging assessment (new epoch / new client?)

- **No new instance epoch.** `$XDG_RUNTIME_DIR/hypr/` contains exactly one dir with the same
  signature as the receipts; `ps -o lstart= -p 1619` → `Fri Oct 23 22:14:09 2026`, which equals
  the signature timestamp `1792804449` = `2026-10-24T01:14:09Z` (local = UTC−3). Same compositor
  process, same kernel inodes → socket2 was never re-created.
- **No new client.** socat pid 2293 started `Oct 23 22:14:11` (2 s after the compositor); waybar
  pid 935660 started `Oct 25 02:06:20` — both before the 11:00 receipts, and both still hold the
  same fds at scan time. The subscriber set is identical to the frozen one.
- **Decision:** nothing invalidates the committed triplet. The only expected-difference candidate
  (tool_sha256 drift) did not occur, and the state has not aged at all between the freeze commit
  and my re-derivation. The triplet stands as committed at HEAD `58e55ec`.

## Falsification attempts that could have failed

tool changed since freeze (no — digest match) · subscriber churn/restart (no — same pids/fds/inodes)
· compositor restart or second instance dir (no — single dir, same signature, same pid)
· backlog appeared since freeze (no — all socket2 queues 0) · markers written since freeze
(no — 0/0 in both channels, log mtime 11:07 still clean) · committed snapshot not self-contained
(no — `python3 -I tools/mado-eventq.py --ss-file .ufo/waves/round-38/receipts/eventq-live-ss.txt`
reproduces the identical 2 CLIENT rows and `verdict=CLEAN`, exit=0) · receipts dirty in the worktree
(no — porcelain clean).

## Residual risk / verification gaps

- The full 1011-line ss dump outside the socket2/peer rows is not re-derivable after the fact
  (unrelated sockets churn); only its load-bearing rows were verified. This does not touch any
  round-38 claim.
- `markers_observable=no` means a zero marker count is "not logged", not "never overflowed" —
  that limitation is already encoded in the tool's semantics and in the receipt's
  `markers_observable=no` field; nothing new.
- Kernel-internal queue depth (Hyprland's in-process 64-event queue) is invisible to `ss` and
  `/proc`; out of scope for this triplet, as the tool docstring states.

Scratch artifacts: `/tmp/mado38-RevLiveTriplet/` (`eventq-live-now.txt`, `eventq-live-now.err`,
`ss-now.txt`, `ss-committed-rows.txt`, `committed-body.txt`, `eventq-replay.txt`).
Tooling installs: none.
