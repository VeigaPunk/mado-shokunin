# ScoutS203 — omarchy-first-run host re-open (round-35 w1)

Scoped findings, re-measured on host 2026-10-24. Evidence file:
`.ufo/waves/round-35/scratch/ScoutS203/findings.txt`.

## Target

`/home/vgpnk/.local/share/omarchy/bin/omarchy-first-run` — re-opened read-only.

## Measured

- **sha256**: `20508471d8237a60e630baf58f87c0b5a4391e34196ce11e5034745f6a062630`
- **byte length**: `1089`

Both from a fresh `sha256sum` / `stat -c '%s'` run today.

## `install/first-run/` directory — 13 entries

```
battery-monitor.sh  cleanup-reboot-sudoers.sh  dns-resolver.sh  elephant.sh
firewall.sh  gnome-theme.sh  gtk-primary-paste.sh  install-voxtype.hook
recover-internal-monitor.sh  swayosd.sh  text-scaling.sh  welcome.sh  wifi.sh
```

12 `*.sh` files + 1 `*.hook` file.

## Scripts the installer body actually runs: 12

Script lines 13–22 and 26–27 issue `bash "$OMARCHY_PATH/install/first-run/*.sh"`
for all 12 `.sh` files, inside `if [[ -f $FIRST_RUN_MODE ]]; then … fi`
(lines 10, 28). Line 23 is different in kind:

```
23  omarchy-hook-install post-update "$OMARCHY_PATH/install/first-run/install-voxtype.hook"
```

`install-voxtype.hook` is *registered* as a post-update hook, not executed in
the body. So "runs 12" is exact; "directory contains 13 entries" is also exact.

## Idle-lock: CONFIRMED none

`grep -inE 'idle|lock|hypridle|swayidle|loginctl|screensaver|blank'` over all 13
files in `install/first-run/` returned no match (exit 1); no filename references
idle or lock either. None of the first-run scripts concerns the idle lock.

## Comparison vs committed receipt `fetch/S203.receipt.txt`

| Field | Receipt | Re-open | Verdict |
|---|---|---|---|
| sha256 (line 3) | `20508471…062630` | same | match |
| bytes (line 4) | `1089` | `1089` | match |
| script count (line 35) | `12` | 13 dir entries; 12 `.sh` | consistent *if* read as `.sh` count; the receipt's own list at lines 36–48 prints **13 names** including `install-voxtype.hook` |
| line 51 claim "lists 12 scripts; body runs all 12; none is idle-lock" | — | confirmed with precision: body runs 12 `.sh` directly; `.hook` installed via `omarchy-hook-install`, not run | no substantive difference |

**Net diff vs receipt: none substantive.** The only imprecision is that
`install/first-run/` enumerates 13 entries; the receipt's `12` counts the `.sh`
scripts, which is exactly what the body runs.

## Lines relied on

- `omarchy-first-run` lines 13–22, 26–27 — the 12 `bash` calls
- line 23 — `omarchy-hook-install post-update … install-voxtype.hook`
- lines 10, 28 — the `FIRST_RUN_MODE` gate
- receipt lines 3–4 (hash/size), 35–48 (count + 13-name list), 51 (summary claim)
