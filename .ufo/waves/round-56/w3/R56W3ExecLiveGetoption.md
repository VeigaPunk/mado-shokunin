# R56W3ExecLiveGetoption — attempt-2 live sample

## Item attacked
Fresh live sample for the `misc:disable_autoreload` capability row. This is a second observation, not a new claim.

## Actions and exact evidence
Read the frozen v2 claim and registration first (`claims-frozen-v2.md`, `registration-v2.md`) and v1 registration where v2 is silent. No tools were installed or updated.

Commands exercised:

```text
hyprctl version -j
hyprctl getoption misc:disable_autoreload -j
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-watchplan.py --config ~/.config/hypr/hyprland.conf --getoption /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ExecLiveGetoption/getoption.json --home "$HOME"
pgrep -a Hyprland
ps -o pid=,lstart= -p 1622
```

The captures are preserved as `version.json` and `getoption.json` alongside `live-a2.txt` in this report's evidence directory. Decisive captured values:

```text
version=0.56.2
commit=efb50993780079460b0cbed1363e2166a2de1d9f
option=misc:disable_autoreload int=0 set=false
MADO_WATCH: config=... autoreload=on disable_autoreload=unset paths=40 unsupported=0 errors=0
MADO_WATCH_LIVE: option=misc:disable_autoreload config=0 live=0 verdict=AGREE
MADO_WATCH: DONE watches=40 unsupported=0 errors=0 live=AGREE
WATCHPLAN_RC=0
1622 Hyprland --watchdog-fd 4
1622 Mon Oct 26 12:08:39 2026
```

Captured at `2026-10-30T02:03:33-03:00`; process start was `2026-10-26 12:08:39`, approximately 61h55m earlier. The first capture attempt's `ps -C` was unsupported by this host's ps implementation; the supported `ps -o ... -p` command above succeeded. This limitation did not affect the final receipt.

Attempt-1 reference: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/receipts/live-watchplan.txt` records `config=0 live=0 verdict=AGREE` and `DONE watches=40 unsupported=0 errors=0 live=AGREE`. Those values match this sample. Attempt-1 receipt does not preserve raw getoption JSON, so its `set` boolean cannot be compared; attempt-2 raw sample has `set=false`. No observed drift in the represented integer/config agreement, watch count, unsupported count, or errors.

## Deliverables
- `.ufo/waves/round-56/w3/R56W3ExecLiveGetoption/live-a2.txt`
- `.ufo/waves/round-56/w3/R56W3ExecLiveGetoption/version.json`
- `.ufo/waves/round-56/w3/R56W3ExecLiveGetoption/getoption.json`

## Defects, risks, and blockers
No defect demonstrated; the live comparison supports the capability row for this observation. Risk/limitation: attempt-1's raw option JSON is unavailable in its receipt, preventing comparison of its `set` field. The first `ps -C` command did not run successfully (host ps does not support `-C`); replaced with successful pid-specific `ps -o`.
