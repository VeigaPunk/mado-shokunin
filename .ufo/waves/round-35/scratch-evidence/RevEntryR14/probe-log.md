# RevEntryR14 probe log — host plazir27, read-only
# REBUILT 2026-10-25 03:46 from the seat transcript after an external sweep removed the
# entire .ufo/waves/round-35/scratch/ tree at ~03:45 (all seat directories, not just this one).
# Values below are the ones measured and printed in-session between 03:30 and 03:41; nothing was
# re-derived or guessed. Section 11 is a fresh post-sweep spot-check of the load-bearing invariants.
# The report .ufo/waves/round-35/w2/reports/RevEntryR14.md is self-sufficient: every verdict there
# cites its command and exit code inline, so no finding depends on this file existing.

## 1. counters (mechanical status of the frozen claims)
python3 -I .ufo/waves/round-35/c1/count.py --root /home/vgpnk/Projects/shokunin/mado-shokunin --frozen .ufo/waves/round-35/c1/frozen.json
  PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   rc=0
python3 -I .ufo/waves/round-35/c2/count.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --frozen .ufo/waves/round-35/c2/frozen.json
  PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET   rc=0

## 2. gate-quote contiguity (the entry's quote, stripped of the "gate-quote: S205 " prefix)
quote = 'located: hypridle runs as pid 1667 and started in this session; hypridle.conf sets timeout 150 and 152'
  words=17  in_receipt=True   -> C1 is satisfied by the receipt's own summary line

## 3. process / unit / scope
pgrep -a -x hypridle                       -> 1667 /usr/bin/hypridle                         rc=0
cat /proc/1667/cgroup                      -> 0::/user.slice/user-1000.slice/user@1000.service/app.slice/app-graphical.slice/app-Hyprland-hypridle-d4bd7533.scope
ps -o pid,lstart,etime,args -p 1667        -> 1667 Fri Oct 23 22:14:10 2026 1-05:16:49 /usr/bin/hypridle
systemctl --user status app-Hyprland-hypridle-d4bd7533.scope
  Loaded: /run/user/1000/systemd/transient/...scope; transient   Transient: yes
  Active: active (running) since Fri 2026-10-23 22:14:11 -03; CGroup -> 1667 /usr/bin/hypridle
systemctl --user show app-Hyprland-hypridle-d4bd7533.scope -p Id,MainPID,ActiveEnterTimestamp,ActiveState,SubState,Description
  Id=... ActiveEnterTimestamp=Fri 2026-10-23 22:14:11 -03  -- NOTE: -p MainPID prints nothing, rc=0:
  a scope unit tracks no main pid, so the pid->unit link must come from ControlGroup or /proc/<pid>/cgroup
systemctl --user show app-Hyprland-hypridle-d4bd7533.scope -p Id -p ControlGroup -p ActiveState
  Id=... ActiveState=active ControlGroup=/user.slice/user-1000.slice/user@1000.service/app.slice/app-graphical.slice/app-Hyprland-hypridle-d4bd7533.scope
systemctl --user status hypridle.service
  Loaded: loaded (/usr/lib/systemd/user/hypridle.service; disabled; preset: enabled)   Active: inactive (dead)

## 4. is-active indistinguishability (word identical, rc differs)
systemctl --user is-active hypridle                             -> inactive   rc=3
systemctl --user is-active definitely-not-a-unit-xyz.service    -> inactive   rc=4
systemctl --user is-active app-Hyprland-hypridle-d4bd7533.scope -> active     rc=0

## 5. boots and manager identities (immutable history)
journalctl --user --list-boots
  -2 6a7f4fdf Fri 2026-10-23 07:18:30 -> 13:21:44
  -1 e55f9cd9 Fri 2026-10-23 13:24:57 -> 22:10:20
   0 0a3785aa Fri 2026-10-23 22:14:08 -> 2026-10-25 03:38:50
journalctl --list-boots            (system journal, kernel-bounded, extra short boot)
  -3 6a7f4fdf 07:18:30 -> 13:21:50
  -2 d577c6e0 13:22:32 -> 13:23:13     (41 s boot; no user-journal entries)
  -1 e55f9cd9 13:24:36 -> 22:12:24     (kernel first line -> UFW last line)
   0 0a3785aa 22:14:07 -> 2026-10-25 03:38:59
system -3 == user -2 ; system -1 == user -1 ; system 0 == user 0 ; boot IDs agree across both
journalctl --user -b -1 | grep -o 'systemd\[[0-9]*\]' | sort -u   -> systemd[1529]
journalctl --user -b  0 | grep -o 'systemd\[[0-9]*\]' | sort -u   -> systemd[1493]
journalctl --user -b -1 -o short-iso | sed -n '1p'  -> 13:24:57 Queued start job for default target Main User Target.
journalctl --user -b  0 -o short-iso | sed -n '1p'  -> 22:14:08 Queued start job for default target Main User Target.
journalctl        -b -1 -o short-iso | sed -n '1p;$p' -> 13:24:36 kernel: Linux version ... / 22:12:24 kernel: [UFW BLOCK]
pgrep -a -f 'systemd --user'                          -> 1493 /usr/lib/systemd/systemd --user   (current)
loginctl list-sessions                                -> 1 1000 vgpnk - 1493 manager ; 2 1000 vgpnk seat0 1523 user

## 6. hypridle journal lines (all of them)
journalctl --user -o short-iso | grep -i 'Started hypridle'
  2026-10-23T13:25:00-03:00 systemd[1529]: Started hypridle.     (boot -1)
  2026-10-23T22:14:11-03:00 systemd[1493]: Started hypridle.     (boot  0)
journalctl --user --boot=0 -o short-iso | grep -i hypridle     (5 lines; see §10 for the 2 reviewer lines)
  22:14:11 uwsm_app-daemon[1805]: received: app -- hypridle
  22:14:11 uwsm_app-daemon[1805]: sent: exec systemd-run --user --scope --slice=app-graphical.slice \
            --unit=app-Hyprland-hypridle-d4bd7533.scope --description=hypridle --quiet --collect --same-dir -- hypridle
  22:14:11 systemd[1493]: Started hypridle.
journalctl --user -b _SYSTEMD_UNIT=app-Hyprland-hypridle-d4bd7533.scope   -> -- No entries --   rc=0
journalctl --user -o short-iso | sed -n '1p'  -> 2026-10-23T07:18:30 (oldest entry; /var/log/journal present, 198.1M)
per-boot `grep -c 'Started hypridle\.'` (user numbering): -2:0  -1:1  0:1
  (user numbering has NO -3: `journalctl --user -b -3` -> "No journal boot entry found for the specified boot (-3)" rc=1)

## 7. conf and actuators
sha256sum ~/.config/hypr/hypridle.conf -> e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41
stat ~/.config/hypr/hypridle.conf      -> 765 bytes mtime 2026-10-03 17:44:32 (precedes daemon start)
sed -n '8,19p' ~/.config/hypr/hypridle.conf
  listener timeout=150 on-timeout = pidof hyprlock || omarchy-launch-screensaver
  listener timeout=152 on-timeout = omarchy-system-lock   on-resume = omarchy-system-wake
omarchy-launch-screensaver (read in full, 59 lines): no hyprlock / omarchy-system-lock / lock call;
  execs terminal --class=org.omarchy.screensaver -> omarchy-screensaver (tte); exits 1 if tte absent
omarchy-system-lock (read in full, 33 lines): if ! pidof hyprlock; then ( hyprlock; omarchy-system-wake ) & fi
command -v hyprlock tte omarchy-system-lock omarchy-launch-screensaver  -> all present
pacman -Q hypridle hyprlock -> hypridle 0.1.8-2 ; hyprlock 0.9.6-3
pgrep -x hyprlock -> rc=1 (none) ; pgrep -af 'omarchy-screensaver|omarchy-launch-screensaver' -> none
ls ~/.local/state/omarchy/toggles/ -> only hypr/ (no screensaver-off flag)

## 8. current lock state (read-only)
hyprctl layers -> only wallpaper (pid 1672, level 0) and waybar (pid 935660, level 2); no lock surface
loginctl show-session 1 -> Type=unspecified Active=yes State=active IdleHint=no LockedHint=no

## 9. 03:38 — post-errata re-check (entry changed twice under review)
stat: 1789 B 03:25:52 (first read) -> 2505 B 03:33:57 (E1) -> 3768 B 03:35:30 (E2)
sha256(entry) = 583c708c338ecb063f8ef38071d415c79476088f27994551fd964384be1e0bf3
body lines 1 / 17 / 20 unchanged by the errata: grep -n 'restart\|both fire\|will fire'
  1: "# The idle lock is armed ... and the chain will fire"
 17: "at 22:14:11 - a restart, not a first start."
 20: "(S205), and both fire the desktop's own lock command."
c1 counter after E2 -> PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   rc=0
  => predicate unchanged by an in-file assertion+retraction

## 10. 03:41 — journal contamination + crash check + self-correction
journalctl --user --boot=0 | grep -i hypridle   -> 5 lines, of which 2 are reviewer sudo probes:
  03:34:38 sudo[2181728] PWD=.../mado-shokunin COMMAND=/usr/bin/coredumpctl list hypridle --no-pager
  03:37:19 sudo[2637509] PWD=.../mado-shokunin COMMAND=/usr/bin/coredumpctl list hypridle --no-pager
  real starts: journalctl --user --boot=0 | grep -c 'Started hypridle\.' -> 1
coredumpctl list hypridle --no-pager -> "No coredumps found." rc=0
coredumpctl list | grep -i 'hypridle|hyprlock' -> no match (rc=1)
journalctl --user | grep -iE 'hypridle.*(segfault|crash|core-dump|dumped)' -> no match (rc=1)
journalctl -b 0 (system) grep hypridle -> only the 3 uwsm/systemd lines + the 2 reviewer sudo probes; no "Stopped hypridle."
SELF-CORRECTION: user numbering has no boot -3; `journalctl --user -b -3` -> "No journal boot entry found
  for the specified boot (-3)." (rc=1). The earlier loop's "boot -3: 0" was grep -c over an empty stream:
  an absent index, not a zero-start boot. User indices are -2, -1, 0 only.

## 11. 03:46 — post-sweep spot-check of load-bearing invariants (fresh run)
sha256(entry)        = 583c708c338ecb063f8ef38071d415c79476088f27994551fd964384be1e0bf3  (unchanged)
sha256(S205 receipt) = f3387bfcbac79016034be38bab6548ae31df5860e5aafaa03105aca84b08ae1a  (unchanged)
sha256(hypridle.conf)= e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41  (unchanged)
stat(entry)          = 3768 bytes mtime 2026-10-25 03:35:30.276175284 -0300
pgrep -a -x hypridle -> 1667 /usr/bin/hypridle
systemctl --user is-active app-Hyprland-hypridle-d4bd7533.scope -> active   rc=0
systemctl --user is-active hypridle.service                    -> inactive rc=3
C1 -> PRED-C1-r35-v1 ... verdict=TARGET_MET  rc=0
C2 -> PRED-C2-r35-v1 ... verdict=TARGET_MET  rc=0
