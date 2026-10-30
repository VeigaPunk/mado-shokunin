# Second kernel watch-table sample

Axes: C1 coverage; C2 operability/capability acquisition (this seat); C3 registry consistency/calibration. Orthogonal review axes: inode identity, watch count, registration-order consistency, mask fidelity, temporal stability.

Sample UTC: 2026-10-30T05:04:00.275753+00:00
Pinned content revision: `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`. Working command and pinned scratch copy produced byte-identical output; tool sha256 `3ccf070841b3c0134a05f612a35e553364f318a9d36843455f4207df118f22b7`.

```text
1622  1000 Mon Oct 26 12:08:38 2026  3-13:55:21 Hyprland
MADO_WATCH: config=/home/vgpnk/.config/hypr/hyprland.conf autoreload=on disable_autoreload=unset paths=40 unsupported=0 errors=0
MADO_WATCH: DONE watches=40 unsupported=0 errors=0 live=NONE
{"all_kernel_masks_8": true, "fd_link_changes": ["172", "165"], "identity": "   1622  1000 Mon Oct 26 12:08:38 2026  3-13:55:21 Hyprland
", "inode_extra": [], "inode_intersection": 40, "inode_missing": [], "inotify_fds": {"12": 40, "86": 40}, "journal_rc": 0, "kernel_count": 40, "pid": 1622, "predicted_primary": 40, "predicted_total": 40, "prior_inode_order_unchanged": true, "registration_order_match": 40, "rev": "0f3a54361a9824484d0801679ceb1fd8ac7c32e1", "samples_stable": false, "selected_fd": "86", "time_utc": "2026-10-30T05:04:00.275753+00:00", "tool_sha256": "3ccf070841b3c0134a05f612a35e553364f318a9d36843455f4207df118f22b7", "watch_tables_stable": true}
```

## Side-by-side tables

| predicted n | predicted inode (decimal) | predicted path | kernel wd (decimal) | kernel inode (decimal) | kernel mask (hex) | match |
|---|---|---|---|---|---|---|
| 1 | 21221 | /home/vgpnk/.config/hypr/hyprland.conf | 1 | 21221 | 0x8 | yes |
| 2 | 822 | /home/vgpnk/.local/share/omarchy/default/hypr/autostart.conf | 2 | 822 | 0x8 | yes |
| 3 | 825 | /home/vgpnk/.local/share/omarchy/default/hypr/bindings/media.conf | 3 | 825 | 0x8 | yes |
| 4 | 824 | /home/vgpnk/.local/share/omarchy/default/hypr/bindings/clipboard.conf | 4 | 824 | 0x8 | yes |
| 5 | 826 | /home/vgpnk/.local/share/omarchy/default/hypr/bindings/tiling-v2.conf | 5 | 826 | 0x8 | yes |
| 6 | 828 | /home/vgpnk/.local/share/omarchy/default/hypr/bindings/utilities.conf | 6 | 828 | 0x8 | yes |
| 7 | 830 | /home/vgpnk/.local/share/omarchy/default/hypr/envs.conf | 7 | 830 | 0x8 | yes |
| 8 | 27329 | /home/vgpnk/.config/omarchy/current/theme/gum.env.conf | 8 | 27329 | 0x8 | yes |
| 9 | 832 | /home/vgpnk/.local/share/omarchy/default/hypr/looknfeel.conf | 9 | 832 | 0x8 | yes |
| 10 | 831 | /home/vgpnk/.local/share/omarchy/default/hypr/input.conf | 10 | 831 | 0x8 | yes |
| 11 | 838 | /home/vgpnk/.local/share/omarchy/default/hypr/windows.conf | 11 | 838 | 0x8 | yes |
| 12 | 821 | /home/vgpnk/.local/share/omarchy/default/hypr/apps.conf | 12 | 821 | 0x8 | yes |
| 13 | 802 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/1password.conf | 13 | 802 | 0x8 | yes |
| 14 | 803 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/bitwarden.conf | 14 | 803 | 0x8 | yes |
| 15 | 804 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/browser.conf | 15 | 804 | 0x8 | yes |
| 16 | 807 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/hyprshot.conf | 16 | 807 | 0x8 | yes |
| 17 | 808 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/jetbrains.conf | 17 | 808 | 0x8 | yes |
| 18 | 809 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/localsend.conf | 18 | 809 | 0x8 | yes |
| 19 | 811 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/pip.conf | 19 | 811 | 0x8 | yes |
| 20 | 812 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/qemu.conf | 20 | 812 | 0x8 | yes |
| 21 | 813 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/retroarch.conf | 21 | 813 | 0x8 | yes |
| 22 | 814 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/steam.conf | 22 | 814 | 0x8 | yes |
| 23 | 806 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/geforce.conf | 23 | 806 | 0x8 | yes |
| 24 | 810 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/moonlight.conf | 24 | 810 | 0x8 | yes |
| 25 | 815 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/system.conf | 25 | 815 | 0x8 | yes |
| 26 | 816 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/telegram.conf | 26 | 816 | 0x8 | yes |
| 27 | 818 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/typora.conf | 27 | 818 | 0x8 | yes |
| 28 | 817 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/terminals.conf | 28 | 817 | 0x8 | yes |
| 29 | 819 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/walker.conf | 29 | 819 | 0x8 | yes |
| 30 | 820 | /home/vgpnk/.local/share/omarchy/default/hypr/apps/webcam-overlay.conf | 30 | 820 | 0x8 | yes |
| 31 | 27331 | /home/vgpnk/.config/omarchy/current/theme/hyprland.conf | 31 | 27331 | 0x8 | yes |
| 32 | 21226 | /home/vgpnk/.config/hypr/monitors.conf | 32 | 21226 | 0x8 | yes |
| 33 | 21330 | /home/vgpnk/.config/hypr/input.conf | 33 | 21330 | 0x8 | yes |
| 34 | 21219 | /home/vgpnk/.config/hypr/bindings.conf | 34 | 21219 | 0x8 | yes |
| 35 | 21225 | /home/vgpnk/.config/hypr/looknfeel.conf | 35 | 21225 | 0x8 | yes |
| 36 | 21218 | /home/vgpnk/.config/hypr/autostart.conf | 36 | 21218 | 0x8 | yes |
| 37 | 27226 | /home/vgpnk/.local/state/omarchy/toggles/hypr/flags.conf | 37 | 27226 | 0x8 | yes |
| 38 | 28604 | /home/vgpnk/.local/state/omarchy/toggles/hypr/window-no-gaps.conf | 38 | 28604 | 0x8 | yes |
| 39 | 76185 | /home/vgpnk/.config/hypr/ai-usage.conf | 39 | 76185 | 0x8 | yes |
| 40 | 26324557 | /home/vgpnk/.config/hypr/gkeep.conf | 40 | 26324557 | 0x8 | yes |

Predicted masks: every primary requests `IN_CLOSE_WRITE|IN_DONT_FOLLOW`. Kernel fdinfo retains event mask `0x8` (`IN_CLOSE_WRITE`); `IN_DONT_FOLLOW` is an add-watch resolution flag, not a persistent event-mask bit. Raw fdinfo order is descending wd on this host; table above sorts numeric wd. Numeric wd/inode alignment is evidence consistent with insertion order, not an independent trace of historical inotify_add_watch calls.

## Match recommendation

40/40 predicted primary watches match kernel fd 86 by watch number and inode. Kernel rows=40; unique inode sets equal=True; inotify watch tables unchanged=True. Full fd symlink listings varied (see sample.json fd_link_changes), not the watch tables. No additional canonical watches were predicted. Both fd 12 and fd 86 expose identical 40-row inotify tables, before and after. They may be duplicate descriptors for one inotify instance [INFERENCE]; descriptor identity cannot be established from these reads. Do not count them as 80 independent predicted config watches.

## Journal citations

`journalctl --user -u Hyprland --no-pager --since 2026-10-28` (exit 0):
```text
-- No entries --

```

An empty unit-filtered journal is no evidence that zero reloads, coredumps, or restarts occurred. No causal explanation of intervening history can be established from this window alone. Process start identity is recorded above. The 40 inode values and their order are identical to the 2026-10-28 receipt w2/R56W2RevProcFdinfo/comparison.md: no observed watch-inode drift requires explanation. The live process started October 26, preceding both samples. This establishes process continuity only, not absence of reloads.

## Evidence and limits

Exact argv, return codes and stdout/stderr: `commands.json`. Both raw /proc inotify snapshots and all fd symlink targets: `sample.json`. Prediction: `watchplan.txt`. Journal: `journal.txt`. No compositor signal, configuration write, reload, getoption, fixture harness, or test suite was invoked. LSP is unavailable (`read xd://lsp` returned `No such tool`); no semantic caller/definition/diagnostic assertions are made. No tool installation. All scratch removed before return.

## Reproduction and parser disclosure

The sampling driver enumerated `/proc/1622/fd` with `Path.iterdir()` and `os.readlink`, and read `/proc/1622/fdinfo/*` with `Path.read_text()`, retaining only lines starting `inotify `. Two snapshots bracketed both tool invocations. Parse hexadecimal fields with `re.findall(r"(?:^|\s)(wd|ino|sdev|mask):([0-9a-fA-F]+)", line)`; the whitespace boundary prevents `ignored_mask:0` overwriting `mask:8`. The first derived parser lacked that boundary; its incorrect mask=0 and whole-fd-list stability flag were corrected from retained raw evidence, without re-sampling or changing the observation. Inode and wd parsing were unaffected.
