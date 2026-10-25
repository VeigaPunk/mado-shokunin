# ExecEventqSnapshot report

## Scope and files
- Created `.ufo/waves/round-39/w1/ExecEventqSnapshot/eventq-live-census.txt`.
- Created `.ufo/waves/round-39/w1/ExecEventqSnapshot/eventq-after.txt` (standalone counter receipt).
- No tools installed.

## Evidence
- Command: `python3 -I tools/mado-eventq.py --snapshot-out /tmp/eventq-live-census.txt` (lane cwd), exit 0. Live output: 2 clients (`socat` pid 2377 fd 5; `waybar` pid 1683 fd 19), overflow=0, write_fail=0, lagging=0, markers_observable=no, verdict=CLEAN.
- The census snapshot retains only socket2 listener/server rows and matched subscriber peer rows; unlike committed `.ufo/waves/round-38/receipts/eventq-live-ss.txt`, unrelated full-table sockets and their process/pid/fd details were omitted.
- Tool SHA256 is included in the live census receipt. Counter command: `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r38-eventq.py --repo . --rev 457d1b125932c1e0d797061a2156b917bcd7edaa`, exit 0. Exact stdout saved as `eventq-after.txt`: `fixtures=14/14 readonly=1 live=1 tool=present verdict=TARGET_MET`; live detail `replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1`.

## Risks / blockers
- Live values may change between runs. Counter evaluated the requested freeze revision and its persisted artifact set.
