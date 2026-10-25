# ExecEventqB — candidate B of tools/mado-eventq.py (mado r37 w1)

Verdict: **PASS** on everything this seat can reach. Counter: `fixtures=10/10 readonly=1 live=0` (live=0 was expected: the live receipt is the L1's job). The live host run is read-only and returns CLEAN with 2 subscribers. Replaying its snapshot gives the identical client set. In a sandbox-only receipt commit the counter reaches `TARGET_MET`, and a tampered receipt flips it back to MISSED.

## Files changed
- `.ufo/waves/round-37/w1/scratch/ExecEventqB/mado-eventq.py` — the candidate, 326 lines, sha256 `bb84e159ea83ff290c2fb16fcd8092153e4e19a0e714f8892598aee8bbb16917` (git blob `8a60b72af22cd75ac63d61f9d165bb64cc9d9105`).
- `.ufo/waves/round-37/w1/scratch/ExecEventqB/setup-reasons.py` — a scratch harness, sha256 `1ba33ba189add03547a51b63a45057e67f586d7a55cf06249bf10fba1d126a97`.
- This report. No production file, LANE git/jj state, compositor, config or service was touched. The only commits went into `/dev/shm/mado37-ExecEventqB/sb` under the sandbox identity. No tools were installed.

## Design (candidate B)
- **Table-driven parser.** The `SS_COLUMNS` table (name, pattern, converter) builds one anchored row regex: `Netid State Recv-Q Send-Q LocalAddr(lazy) LocalInode PeerAddr PeerInode [users:(...)]`. A separate regex reads the `users:` tuples. The first tuple is used, because host server rows carry two tuples, e.g. `users:(("…",pid=1619,fd=250),("…",pid=1619,fd=236))`.
- **Census.**
  - It needs a LISTEN row on socket2.
  - Every ESTAB row whose LocalAddr equals socket2 counts as one subscriber.
  - The peer is the non-socket2 row whose LocalInode equals the server row's PeerInode.
  - If the peer row is missing, or has no `users:` field, the client is printed as `comm=- pid=- fd=-` and still counted, so `subscribers` always equals the number of CLIENT lines.
  - Whitespace in a comm becomes `_`, so the counter's `\S+` triple regex stays valid.
- **Markers.**
  - Overflow uses `\bSocket2 fd \d+ overflowed event queue, removing\s*$`.
  - Write failure uses `\bSocket2 fd \d+ failed writing event: \S`. Both quote the exact S189 format strings (:175, :155).
  - ANSI colour codes are stripped first, in case `colored_stdout_logs` reaches the journal.
  - The summary adds the counts from all channels; the docstring warns that a line echoed to both file and journal counts twice.
- **`markers_observable`.** `--disable-logs` 0 → yes, 1 → no. When live, it reads `hyprctl getoption … -j` and uses its `"int"` value: nonzero → no, unreadable → unknown.
- **SETUP output.** Everything is buffered, so a SETUP prints exactly one line and nothing else. argparse errors are routed to `SETUP usage` (exit 2), not argparse's stderr usage text.
- **`--snapshot-out`.** It writes the raw header line plus the LISTEN, server and peer rows, in their original order, only after every input has been read successfully.
- **Docstring.** It covers the purpose, the S189 rule (MAX_QUEUED_EVENTS = 64 at :169, removal on overflow :175 and on write error :155, EAGAIN keeping events queued), the `debug:disable_logs` caveat (Logger.cpp:15-16), the ss column meanings (including LISTEN-row Recv-Q/Send-Q), the exit map with all 14 SETUP reasons, and the read-only guarantee.

## 1. Counter score — PASS (fixtures 10/10, readonly=1; live=0 as expected)
Command: `git clone -q --no-local /home/vgpnk/Projects/shokunin/mado-shokunin /dev/shm/mado37-ExecEventqB/sb`, copy to `sb/tools/mado-eventq.py`, sandbox `add -A` + `commit -qm cand`, then `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r37-eventq.py --repo /dev/shm/mado37-ExecEventqB/sb --rev HEAD`:
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
PRED-C2-r37-v2 fixtures=10/10 readonly=1 live=0 tool=present verdict=TARGET_MISSED rev=a2b86ce60a4aa4ceebc4d0cccf70d463d97b60ba
counter_rc=1
```
(The sandbox commit `a2b86ce` sits on lane base `80b83c8`.)

Static read-only checks on the sandbox blob: `grep -c 'connect('` → `0`; the counter's socket-import regex → `0`; the shebang is `#!/usr/bin/env python3`. The imports are only `argparse json os re subprocess sys` (lines 88-93).

## 2. Live run on this host — PASS (read-only)
Command: `python3 -I sb/tools/mado-eventq.py --snapshot-out /dev/shm/mado37-ExecEventqB/live-ss.txt --expect-client waybar` → `live_rc=0`
```
MADO_EVENTQ_CLIENT: comm=waybar pid=935660 fd=21 peer_recv_q=0 server_send_q=0
MADO_EVENTQ_CLIENT: comm=socat pid=2293 fd=5 peer_recv_q=0 server_send_q=0
MADO_EVENTQ_MARKERS: source=log:/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/hyprland.log overflow=0 write_fail=0
MADO_EVENTQ_MARKERS: source=journal overflow=0 write_fail=0
MADO_EVENTQ: socket2=/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/.socket2.sock subscribers=2 overflow=0 write_fail=0 lagging=0 missing_client=- markers_observable=no verdict=CLEAN
```
- **Key finding confirmed independently.** `hyprctl getoption debug:disable_logs -j` → `{"option": "debug:disable_logs", "int": 1, "set": false }`. Note that `set: false` means 1 is the default value, not a user override. The tool therefore reports `markers_observable=no`, so the `overflow=0` above is not evidence that no overflow happened.
- Channel sizes, as counts only: the session log has 27331 lines (4259033 bytes) and the unit journal has 717 lines.
- The live mode ran only `ss -xpa`, the journalctl command and the hyprctl getoption call.

## 3. Snapshot replay — PASS (same client set)
- The snapshot has 6 lines: the header, the LISTEN row, 2 server ESTAB rows and 2 client rows.
- Replay command: `--ss-file live-ss.txt --log empty.log --journal-file empty.journal --disable-logs 1`. It returned `replay_rc=0` and the same two CLIENT lines, with `subscribers=2 … markers_observable=no verdict=CLEAN`.
- `diff` of the sorted (comm, pid, fd) triples between the live and replay output → `triples identical: 2`.
- Cross-check against the whole table: a separate `ss -xpa` capture (1075 lines) fed through `--ss-file` → `full-table triples identical`.

sha256sum:
```
bb84e159ea83ff290c2fb16fcd8092153e4e19a0e714f8892598aee8bbb16917  sb/tools/mado-eventq.py
038e9d5a32f8c1351e5f0d7407d2ffcea0574e604820dc948a9864eba8a46fca  live-ss.txt
072e7622d2335dc25b3389621e3009e025a432d50ca24720d9ab6a5e668b3b6a  live-out.txt
cb1204ad1f6193dacc338083894dc02b2faf138ebad152964e6ecbc0eec1e73e  replay-out.txt
```
(All under `/dev/shm/mado37-ExecEventqB/`.)

## 4. Every SETUP reason can be triggered — PASS (17/17)
Command: `python3 -I scratch/ExecEventqB/setup-reasons.py sb/tools/mado-eventq.py /dev/shm/mado37-ExecEventqB/harness`. Inputs are driven only by files and env (`PATH` set to an empty dir, `XDG_RUNTIME_DIR`, `HYPRLAND_INSTANCE_SIGNATURE`). Each SETUP case must produce rc 2, exactly one line, and no `verdict=`.
```
case=usage rc=2 ok=1 :: MADO_EVENTQ: SETUP usage argument --disable-logs: invalid choice: '2' (choose from '0', '1')
case=ss_file_unreadable rc=2 ok=1 :: MADO_EVENTQ: SETUP ss_file_unreadable …/nope: No such file or directory
case=ss_unavailable rc=2 ok=1 :: MADO_EVENTQ: SETUP ss_unavailable ss: FileNotFoundError
case=ss_unparseable rc=2 ok=1 :: MADO_EVENTQ: SETUP ss_unparseable no Netid header
case=socket2_not_listening rc=2 ok=1 :: MADO_EVENTQ: SETUP socket2_not_listening no LISTEN row ending /.socket2.sock
case=socket2_not_listening(--socket2) rc=2 ok=1 :: MADO_EVENTQ: SETUP socket2_not_listening /x/.socket2.sock
case=socket2_ambiguous rc=2 ok=1 :: MADO_EVENTQ: SETUP socket2_ambiguous 2 listeners; pass --socket2
case=no_runtime_dir rc=2 ok=1 :: MADO_EVENTQ: SETUP no_runtime_dir XDG_RUNTIME_DIR unset
case=instance_missing rc=2 ok=1 :: MADO_EVENTQ: SETUP instance_missing …/rt-empty/hypr/bogus
case=no_instance rc=2 ok=1 :: MADO_EVENTQ: SETUP no_instance …/rt-empty/hypr
case=instance_ambiguous rc=2 ok=1 :: MADO_EVENTQ: SETUP instance_ambiguous 2 dirs under …/rt-two/hypr
case=log_unreadable rc=2 ok=1 :: MADO_EVENTQ: SETUP log_unreadable …/nope.log: No such file or directory
case=journal_file_unreadable rc=2 ok=1 :: MADO_EVENTQ: SETUP journal_file_unreadable …/nope.j: No such file or directory
case=journal_unavailable rc=2 ok=1 :: MADO_EVENTQ: SETUP journal_unavailable journalctl: FileNotFoundError
case=snapshot_unwritable rc=2 ok=1 :: MADO_EVENTQ: SETUP snapshot_unwritable …/no/dir/s.txt: No such file or directory
case=observable_unknown rc=0 ok=1 :: MADO_EVENTQ: socket2=/run/user/1000/hypr/HIS/.socket2.sock subscribers=3 overflow=0 write_fail=0 lagging=2 missing_client=- markers_observable=unknown verdict=CLEAN
case=edges rc=0 ok=1 :: MADO_EVENTQ: socket2=… subscribers=3 overflow=0 write_fail=0 lagging=2 missing_client=- markers_observable=yes verdict=CLEAN
    MADO_EVENTQ_CLIENT: comm=Web_Content pid=9 fd=7 peer_recv_q=2048 server_send_q=4352
    MADO_EVENTQ_CLIENT: comm=- pid=- fd=- peer_recv_q=- server_send_q=0
    MADO_EVENTQ_CLIENT: comm=- pid=- fd=- peer_recv_q=5 server_send_q=0
setup_harness fails=0/17
```
(The `…` stands for `/dev/shm/mado37-ExecEventqB/harness`, shortened here.)

## 5. Live clause reachable, and a falsifier — finding
These ran in the sandbox only; this is not the L1's receipt. I committed `receipts/eventq-live.txt` (a `tool_sha256=bb84e1…` line plus the live output) and `receipts/eventq-live-ss.txt` (the snapshot):
```
PRED-C2-r37-v2 fixtures=10/10 readonly=1 live=1 tool=present verdict=TARGET_MET rev=2fa87a91f533fc1cd16787a5de7f5945aa3453c5
met_rc=0
```
Then I changed `pid=2293` to `pid=2294` in the receipt only:
```
PRED-C2-r37-v2 fixtures=10/10 readonly=1 live=0 tool=present verdict=TARGET_MISSED rev=2abbf6dfc772be0a5125605957c75ad7a62ab632
tamper_rc=1
```
So the v2 replay rejects a hand-edited receipt whose digest is correct but whose client set has drifted.

## Risks
- **Double counting.** If `debug:enable_stdout_logs` is on, one marker can appear in both the file and the journal and is then counted twice in the summary. This is documented. Each per-channel MARKERS line is still exact.
- **Marker strictness.** The overflow regex needs the message to end the line, and the write-fail regex needs `: <reason>`. Both follow the S189 format strings. A future Hyprland that adds a suffix would read as zero. [INFERENCE] I found no such suffix in v0.56.2.
- **Address parsing.** A LocalAddr containing ` <digits> ` could misparse under the lazy LocalAddr column. Real Hyprland paths do not contain one.
- **`server_send_q` meaning.** I describe it in the docstring as af_unix write-memory accounting that can exceed `peer_recv_q`. This comes from the kernel's unix_diag behaviour as I remember it, not from a source fetched this round, so it is [INFERENCE].
- **Live receipt.** For the lane to reach live=1, the L1 must commit `receipts/eventq-live.txt` and `eventq-live-ss.txt` made with the blob it adopts.

Blockers: none.
