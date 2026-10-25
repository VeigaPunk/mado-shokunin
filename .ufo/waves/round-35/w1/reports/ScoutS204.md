# ScoutS204 — re-run of the paired negative (host re-open 2026-10-24)

Scope: re-execute the two read-only checks in `.ufo/waves/round-35/fetch/S204.receipt.txt` and compare observed values against the receipt's claims. Leaf member; no subagent dispatch.

## Observed values

| Check | Command | Observed | Receipt claim | Match |
|---|---|---|---|---|
| omarchy-toggle journal count | `journalctl --user --no-pager \| grep -c 'omarchy-toggle'` | `0` (exit 1 = no match) | `0` | yes |
| first-run script count | `grep -c 'bash "\$OMARCHY_PATH/install/first-run/' /home/vgpnk/.local/share/omarchy/bin/omarchy-first-run` | `12` (exit 0) | `12` | yes |

## Evidence

- `journalctl --user --no-pager | grep -c 'omarchy-toggle'` printed `0` and exited 1 (grep no-match). The user journal in fact holds **zero** `omarchy-toggle` invocations — the operator never toggled.
- `omarchy-first-run` is a 1089-byte bash script (`file`: Bourne-Again shell script, mode 0755). Its body contains exactly 12 `bash "$OMARCHY_PATH/install/first-run/<name>.sh"` invocations inside the `if [[ -f $FIRST_RUN_MODE ]]` block:
  battery-monitor, recover-internal-monitor, cleanup-reboot-sudoers, firewall, dns-resolver, gnome-theme, swayosd, gtk-primary-paste, text-scaling, elephant, welcome, wifi.
  (The `omarchy-hook-install post-update` call and `sudo rm -f /etc/sudoers.d/first-run` are not counted — the receipt's "12" covers only the bash-run scripts.)

## Verdict

Both numbers reproduce exactly: journal omarchy-toggle count = **0**, first-run scripts = **12**. The paired negative in S204.receipt.txt stands — the setup path asks nothing and the operator never toggled.
