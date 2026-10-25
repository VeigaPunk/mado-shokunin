# ExecEventqA — candidate A of tools/mado-eventq.py (mado r37 w1)

**Result:** Candidate A gets `fixtures=10/10 readonly=1 live=0` from the frozen `PRED-C2-r37-v2` counter, run with the prescribed sandbox procedure. `live=0` is expected, because the live receipt belongs to the L1. A live read-only run on this host found 2 subscribers (waybar, socat) and returned `verdict=CLEAN markers_observable=no`. Replaying the run's snapshot gave the same (comm, pid, fd) client set.

- Candidate: `.ufo/waves/round-37/w1/scratch/ExecEventqA/mado-eventq.py` (285 lines)
- `sha256sum`: `436f550e9939a783b7b95d154d099b788ad9daaed2282e19de89413e39371f24`
- Lane HEAD that was cloned: `80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b`
- Nothing was written under LANE except this report and my scratch directory. The candidate made no socket connection. hyprctl was only called with `getoption`. Nothing was installed.

## Axes
- **C2 fixtures:** PASS, 10/10.
- **readonly:** PASS, 1. `grep -c 'connect(' candidate` gives `0`, and there is no `import socket`.
- **live:** not mine to commit. A sandbox-only probe (see below) shows the live clause is reachable with this tool, and that the counter rejects two forged variants.

## Item 1: counter on the candidate (official procedure) — PASS (live=0 expected)
I ran `git clone -q --no-local <LANE> /dev/shm/mado37-ExecEventqA/sb`, copied the candidate to `sb/tools/mado-eventq.py`, and ran the sandbox-identity `add -A && commit -qm cand`. Then:
`python3 -I <LANE>/quality/counters/c2-r37-eventq.py --repo /dev/shm/mado37-ExecEventqA/sb --rev HEAD`

Full output:
```
PRED-C2-r37-v2 case=clean want_rc=0 rc=0 ok=1
PRED-C2-r37-v2 case=overflow-log want_rc=1 rc=1 ok=1
PRED-C2-r37-v2 case=writefail-journal want_rc=1 rc=1 ok=1
PRED-C2-r37-v2 case=not-listening want_rc=2 rc=2 ok=1
PRED-C2-r37-v2 case=missing-client want_rc=1 rc=1 ok=1
PRED-C2-r37-v2 case=lagging want_rc=0 rc=0 ok=1
PRED-C2-r37-v2 case=unparseable want_rc=2 rc=2 ok=1
PRED-C2-r37-v2 case=logs-disabled want_rc=0 rc=0 ok=1
PRED-C2-r37-v2 case=overflow-twice want_rc=1 rc=1 ok=1
PRED-C2-r37-v2 case=decoy want_rc=0 rc=0 ok=1
PRED-C2-r37-v2 fixtures=10/10 readonly=1 live=0 tool=present verdict=TARGET_MISSED rev=0c6ef6c59bb3109c84fa910b216a9a5fe01bb7a8
counter_exit=1
```
The committed blob matches the file: `git show HEAD:tools/mado-eventq.py | sha256sum` printed `blob_sha=436f550e9939a783b7b95d154d099b788ad9daaed2282e19de89413e39371f24`, which equals the file's sha256. The commit's parent is `80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b`.

## Item 2: live run on this host, read-only — PASS
`python3 -I candidate --expect-client waybar --snapshot-out /dev/shm/mado37-ExecEventqA/live-ss.txt` exited `0`:
```
MADO_EVENTQ_CLIENT: comm=waybar pid=935660 fd=21 peer_recv_q=0 server_send_q=0 server_fd=250,236
MADO_EVENTQ_CLIENT: comm=socat pid=2293 fd=5 peer_recv_q=0 server_send_q=0 server_fd=147,145
MADO_EVENTQ_MARKERS: source=log:/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/hyprland.log overflow=0 write_fail=0 fds=-
MADO_EVENTQ_MARKERS: source=journal overflow=0 write_fail=0 fds=-
MADO_EVENTQ: socket2=/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/.socket2.sock subscribers=2 overflow=0 write_fail=0 lagging=0 missing_client=- markers_observable=no verdict=CLEAN
```
- `markers_observable=no` came from the live getoption call, which returned `{"option": "debug:disable_logs", "int": 1, "set": false }`. It agrees with the key finding: the zero marker counts above cannot show "never overflowed".
- I cross-checked the subscriber set by hand with `ss -xpa | grep socket2`. It shows 1 LISTEN row (inode 38117) and 2 ESTAB server rows whose peer inodes are 181143087 and 40790. Those peer rows are held by `waybar,pid=935660,fd=21` and `socat,pid=2293,fd=5`. This matches the tool's output.
- The snapshot has 6 lines (the header, the LISTEN row, 2 server rows and 2 peer rows), sha256 `fee7629de526b2226b6b4a20b8de3e863ad82867ddaa322e7113745338e795be`. A copy is in my scratch directory as `live-ss.txt` (its rows contain socket paths and comms only, no titles). The live output is saved as `live-out.txt` (sha256 `3067d076…a84006`).

## Item 3: replay comparison — PASS
`python3 -I candidate --ss-file live-ss.txt --log empty.log --journal-file empty.journal --disable-logs 1` exited `0`. These are the same arguments the counter's replay uses. It printed the same two CLIENT lines, and its summary reads `subscribers=2 … verdict=CLEAN`. Diffing the sorted `comm/pid/fd` triples between the live and replay outputs printed `triples_identical n=2`. The replay output is saved as `replay-out.txt` (sha256 `274488f5…37fb170`).

## Item 4: sandbox-only live-clause probe — finding (not a receipt)
This probe ran in my sandbox clone only. I wrote `tool_sha256=<candidate sha>` plus the live output to `receipts/eventq-live.txt`, copied the snapshot to `receipts/eventq-live-ss.txt`, committed, and ran the counter:
- Genuine receipt and snapshot: `fixtures=10/10 readonly=1 live=1 tool=present verdict=TARGET_MET`, exit 0.
- Waybar row removed from the snapshot: `live=0 … TARGET_MISSED`, exit 1.
- First digest character changed: `live=0 … TARGET_MISSED`, exit 1.

So once the L1 commits its own receipt and snapshot made with this exact blob, the candidate can reach the target. The live clause also rejects both forgeries.

## Item 5: edge falsifiers (synthetic `ss` files in /dev/shm) — PASS
| case | result |
|---|---|
| comm with spaces, 2 holders, Recv-Q 512 | `comm=Isolated_Web_Co pid=7 … peer_recv_q=512`, `lagging=1`, rc 0; `--expect-client 'Isolated Web Co'` is not reported missing |
| two `.socket2.sock` LISTEN rows, no `--socket2` | `SETUP socket2_ambiguous candidates=2`, rc 2 |
| same file with `--socket2 B` | `socket2=…/B/.socket2.sock subscribers=0 verdict=CLEAN`, rc 0 |
| server ESTAB row whose peer row is gone | `comm=- pid=- fd=- peer_recv_q=- server_send_q=4096`, rc 0 |
| LISTEN only, `--expect-client waybar` twice | `subscribers=0 missing_client=waybar verdict=MISSING_CLIENT`, rc 1 (duplicate removed) |
| one overflow and one write_fail in a log, `--disable-logs 1` | `fds=31,12`, `overflow=1 write_fail=1 markers_observable=no verdict=MARKERS`, rc 1 |
| unreadable `--ss-file` or `--log` | `SETUP ss_unreadable path=…` or `SETUP log_unreadable path=…`, rc 2 |
| `HYPRLAND_INSTANCE_SIGNATURE=bogus` in live mode | `SETUP no_instance dir=/run/user/1000/hypr/bogus`, rc 2 |
| `--disable-logs 2` | argparse rejects it, rc 2 |

## Design notes
- **Parsing `ss` rows** (`parse_row`): live `ss -xpa` has rows with 8, 9, 11 and 13 fields. The 11- and 13-field rows come from comms with spaces, such as "Isolated Web Co". So the tool splits the row at ` users:(`, takes LocalInode, PeerAddr and PeerInode from the right edge, and reads holders with the regex `\("…",pid=N,fd=N\)`. A comm's whitespace is printed as `_` so the `\S+` fields stay parseable.
- **Extra fields** (both optional; the fixture regexes allow them):
  - `server_fd=` on CLIENT lines lists the compositor-side fds. That is the `fd N` that appears in the S189 markers, so a marker can be matched to a subscriber.
  - `fds=` on MARKERS lines lists the fds named in the matched markers.
- **Marker sum:** the summary adds the log and journal counts together. S214 `recheckCfg` turns on stdout (the journal) only when `!disable_logs && enable_stdout_logs`, so with both enabled one event could be counted twice. The docstring says so. The verdict is unaffected because it only tests for non-zero.
- **Docstring** covers the purpose, the S189 queue cap of 64 and the two removal rules (:155 and :175), the `ss` column meanings, the exit map, the live defaults and the read-only guarantee.

## Risks and blockers
- **`/dev/shm` quota:** it is mounted `usrquota` and shared by every seat on this uid. My first final-bytes commit failed with `fatal: unable to write loose object file: Disk quota exceeded`, so that run's counter output read `tool=absent`. That was an environment failure, not a candidate result. After I deleted my second clone the commit succeeded and Item 1 is that run. All my clones are now deleted (`du -sh /dev/shm/mado37-ExecEventqA` gives `20K`). Other seats may hit the same quota.
- **Shared fds:** when several processes hold a client fd, only the first `users:` entry is named. This is documented in the docstring.
- **Not proven by these runs:** a real overflow on this host. With `disable_logs=1` the markers cannot be written, and I did not stall any client.
- **Checks the L1 should run:** after integrating, run the counter at the lane tip once its own `eventq-live.txt` and `eventq-live-ss.txt` are committed, using this exact blob (`436f550e…1f24`). Editing the tool changes its digest and invalidates the receipt.
