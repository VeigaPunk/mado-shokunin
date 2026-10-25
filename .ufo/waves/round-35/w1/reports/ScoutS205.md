# ScoutS205 — idle-lock chain re-probe (round-35, 2026-10-24)

Scoped read-only re-probe of the hypridle/hyprlock chain, compared against
`.ufo/waves/round-35/fetch/S205.receipt.txt` (host re-open earlier the same day).
No lock, screensaver, or idle command was run. All probes executed at write time.

## Process probe

```
$ pgrep -a -x hypridle
1667 /usr/bin/hypridle          # exit 0
$ pgrep -a -x hyprlock
                              # no output, exit 1
```

- **pid 1667** — identical to receipt line 3. Same process still running; it was not
  respawned between the receipt and this re-probe.
- **hyprlock: none** — identical to receipt line 4. Screen is not locked.

## Unit probe

```
$ systemctl --user is-active hypridle
inactive                      # exit 3
```

Identical to receipt line 6.

## Journal start lines (verbatim, all of them)

```
$ journalctl --user --no-pager | grep 'Started hypridle' | tail -5
Oct 23 13:25:00 plazir27 systemd[1529]: Started hypridle.
Oct 23 22:14:11 plazir27 systemd[1493]: Started hypridle.
```

Two lines total, identical to receipt lines 8–9. **No new `Started hypridle` event
since Oct 23 22:14:11** — today (Oct 24) has produced none. The two lines carry
different user-manager pids (systemd[1529] vs systemd[1493]): the 22:14:11 start
happened under a later `systemd --user` instance than the 13:25:00 one.

## Declared timeouts (`/home/vgpnk/.config/hypr/hypridle.conf`)

```
10:    timeout = 150
11:    on-timeout = pidof hyprlock || omarchy-launch-screensaver
16:    timeout = 152
17:    on-timeout = omarchy-system-lock
```

Identical to receipt lines 11–14 (same line numbers, same values: 150 s screensaver,
152 s lock with a 2 s margin on the assumption the screensaver resets the idle timer).
`lock_cmd = omarchy-system-lock` (line 2) also matches receipt lines 18–19.

sha256 of the conf at write time:
`e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41` — identical to
receipt line 16. File unchanged.

## Do the unit probe and the process probe disagree?

**Yes — and the disagreement persists unchanged from the receipt.**

- Process probe: `hypridle` alive as **pid 1667**.
- Unit probe: `hypridle` user unit is **inactive** (exit 3).
- Journal: last `Started hypridle` was Oct 23 22:14:11; no start event covers a
  currently-active unit, yet pid 1667 predates this re-probe (it was already pid
  1667 in the receipt).

Reading: pid 1667 is not a member of any `hypridle.service` unit the current
`systemd --user` manager considers active — a stray/surviving process whose unit
tracking is gone, or one started outside systemd's cgroup view. The receipt's
verdict stands: `hypridle runs as pid 1667` while its unit is `inactive`.

Consequence for the S207 waybar indicator (cross-seat observation only):
`idle.sh` checks `pgrep -x hypridle`, so the stray process still hides the
"Idle lock disabled" icon — the bar shows the chain as armed although systemd
disagrees.

## Comparison with S205.receipt.txt

| Field | Receipt | Re-probe | Match |
|---|---|---|---|
| hypridle pid | 1667 | 1667 | yes |
| hyprlock | none | none | yes |
| unit state | inactive | inactive | yes |
| journal start lines | 2, same timestamps | 2, same timestamps | yes |
| timeouts | 150 / 152, lines 10/11/16/17 | same | yes |
| conf sha256 | `e7d3b8dd…de41` | `e7d3b8dd…de41` | yes |
| unit↔process disagreement | present (located note) | present | yes |

No drift anywhere in the chain. Receipt is fully corroborated by this re-probe.
