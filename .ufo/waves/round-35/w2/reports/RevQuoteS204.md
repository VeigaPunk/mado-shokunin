# RevQuoteS204 — wave 2 falsification of row S204

Seat: `L1Mado35.RevQuoteS204` (leaf, no dispatch). Read-only: no lane corpus file, counter,
`SOURCES.md`, receipt, or host state was written. Scratch:
`.ufo/waves/round-35/scratch/RevQuoteS204/`. Installs/upgrades: none.

**Revision 3.** Rev 2 withdrew my "executes 13 items" claim. Rev 3 incorporates the peer check
with `RevQuoteS203`: the counter is **vacuous**, not merely weak; the boot timeline sharpens the
P0 boundary; and the claim is re-worded to "never toggled is dead", not "the operator toggled".

Verdict: **PARTIAL.** Receipt hash and gate-quote are intact, and the quote's `12` is true of the
script set. The **second negative the entry draws from S204 — "the operator never made it
afterwards either" — is falsified by the host's own journal** (P0). The count objection survives
only as a receipt-reproducibility defect (P1).

| check | expected | observed | verdict |
|---|---|---|---|
| (a) `journalctl --user --no-pager \| grep -c omarchy-toggle` | 0 | `0` | **AGREES numerically, VACUOUS** (P0.1) |
| (a) `ls .../install/first-run/ \| wc -l` | 12 | `13` (= 12 `*.sh` + 1 `*.hook`) | **DIVERGES as instrument**, agrees as script count |
| (b) gate-quote contiguous substring of receipt bytes | yes | `True` (byte-exact, line 8 of 9) | **AGREES** |
| (b) fact "the installer runs 12 first-run scripts" | true | true: body's 12 `bash *.sh` targets set-equal the dir's 12 scripts | **AGREES**; receipt datum unreproducible as written (P1) |
| (c) `sha256sum` receipt == SOURCES.md S204 anchor | equal | equal, 64 hex | **AGREES** |

## P0.1 — the instrument is vacuous, not merely unsound

`bin/omarchy-toggle-idle` contains no journaling primitive at all: `grep -n 'logger\|systemd-cat\|journal\|echo'`
over it → **no match, exit 1**. Its OFF path is `pkill -x hypridle` + `notify-send` (writes
nothing); its ON path is `uwsm-app -- hypridle >/dev/null 2>&1 &`, whose only journal trace is
`uwsm_app-daemon: received: app -- hypridle` — a string that never contains `omarchy-toggle`.
Therefore `grep -c omarchy-toggle` returns 0 **whether or not the toggle was ever used**: the
receipt's `0` is a guaranteed constant, not a measurement. Reported as a negative, it is
unfalsifiable-by-construction; reported as agreement with a live host check, it is empty.

The consequence is useful in the other direction: the **ON** half *is* falsifiable — every
supported re-enable path routes through `uwsm-app` and emits `received: app -- hypridle`.

## P0 — the entry's "never toggled" leg is contradicted by the journal

The entry (`corpus/knowledge/idle-lock-never-asked-r12.md`, Section 2) and the S204 evidence cell
assert *"the operator never made it afterwards either"*. The effects channel records a
**disable event**, mid-boot, with no re-enable until a reboot:

```
Oct 23 13:21:39 systemd[1490]: Stopping hypridle... / Stopped hypridle.      # boot -3 teardown
Oct 23 13:21:39 systemd[1490]: app-Hyprland-hypridle-59197064.scope: Consumed ... 1d 8h 25min
Oct 23 13:25:00 uwsm_app-daemon[1838]: received: app -- hypridle           # boot -1 autostart
Oct 23 13:25:00 systemd[1529]: Started hypridle.                           # scope 9408787a
Oct 23 19:24:38 systemd[1529]: app-Hyprland-hypridle-9408787a.scope: Consumed 2.783s CPU time over 5h 59min 38.213s
Oct 23 22:14:11 uwsm_app-daemon[1805]: received: app -- hypridle           # boot  0 autostart
Oct 23 22:14:11 systemd[1493]: Started hypridle.                           # scope d4bd7533
```

Boot frame, from `journalctl --list-boots --no-pager` (exit 0):

```
 -3 6a7f4fdf...  2026-10-23 07:18:30 → 2026-10-23 13:21:50
 -2 d577c6e0...  2026-10-23 13:22:32 → 2026-10-23 13:23:13
 -1 e55f9cd9...  2026-10-23 13:24:36 → 2026-10-23 22:12:24
  0 0a3785aa...  2026-10-23 22:14:07 → (current)
```

The 19:24:38 kill sits **5h59m into boot -1** and ~2h48m before that boot's last entry; the next
boundary is a **reboot** (boot 0, 22:14:07), not a session restart. Both observed hypridle starts
follow boot headings and are autostart (`exec-once = uwsm-app -- hypridle`,
`default/hypr/autostart.conf:1`). **No `received: app -- hypridle` line exists between 19:24:38
and 22:14:11** — so neither of the two supported re-enable paths ran for the rest of that boot.

Both kill paths, read directly:

- `bin/omarchy-toggle-idle:6` — `pkill -x hypridle` (OFF), `:9` — `uwsm-app -- hypridle` (ON).
- `bin/omarchy-restart-app:6-7` — `pkill -x $1` then `setsid uwsm-app -- "$@"`, reached via
  `bin/omarchy-restart-hypridle:5`. A restart would emit `received: app -- hypridle` within
  seconds; nothing does.

Exclusions, each run with its exit code:

- **Not OOM.** `journalctl --no-pager --since '2026-10-23 19:20' --until '2026-10-23 19:30' | grep -Ei 'oom|killed process|hypridle'` → only the Consumed line (exit 0); earlyoom at 19:24:59 reports `mem avail: 19479 of 21438 MiB (90.86%)`, swap 92.30% free.
- **Not a crash.** `coredumpctl list --since 2026-10-23 --until 2026-10-25 | grep -Ei 'hypridle'` → no match (exit 1); `journalctl -k --since '2026-10-23 19:20' --until '2026-10-23 19:30' | grep -Ei 'segv|oom|hypridle|killed'` → no match (exit 1).
- **Not a boot/session boundary.** Boot -1 spans 13:24:36–22:12:24; 19:24:38 is deep inside it. `journalctl --user --no-pager | grep -c 'Starting hyprland.desktop and waiting'` → `2` (13:25:00, 22:14:09), exit 0 — nothing at 19:24. The compositor logged a heartbeat at 19:23:53.
- **Not a config event.** `sha256sum ~/.config/hypr/hypridle.conf ~/.local/share/omarchy/config/hypr/hypridle.conf` → both `e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41`, mtime `2026-10-03 17:44:32` (exit 0). No refresh and no edit.
- **Not a package update.** `grep -c '^\[2026-10-23' /var/log/pacman.log` → `0` (exit 0), with the log demonstrably covering the day: per-day counts `10-21: 20, 10-22: 2, 10-23: 0, 10-24: 22, 10-25: 31`.
- **No service confound.** `systemctl --user list-unit-files | grep -i hypridle` → `hypridle.service disabled` (exit 0); `list-units --all` shows only the transient `app-Hyprland-hypridle-d4bd7533.scope` running. Correcting the peer note: the unit *file* exists but is disabled, so it is not a live path. The Stopping/Stopped-vs-Consumed differential is about **who initiated the stop of the same transient scope** — systemd on session teardown (13:21:39) versus the main process exiting on its own (`--collect` release, 19:24:38). `[INFERENCE-STRONG]`: systemd semantics, not reproduced, because reproducing it would mutate host state.

State facts: `ps -o lstart -p 1667` → `Fri Oct 23 22:14:10 2026`; `pgrep -ax hypridle` →
`1667 /usr/bin/hypridle` (exit 0); `ls -laR ~/.local/state/omarchy/toggles/` → only
`hypr/flags.conf` and `hypr/window-no-gaps.conf`, no idle flag.

**Wording discipline (peer limit, verified).** Sender identity is unrecoverable: `auditd`,
`psacct` and `acct` are all `inactive`, `/var/log/account/pacct` does not exist, and
`~/.bash_history` is 4572 B with `0` hits for `hypridle` and `0` for `omarchy-toggle` (exit 2/1).
So the defensible claim is **"'never toggled' is dead"** — the idle lock entered the disabled
state inside boot -1 and no supported re-enable ran before the reboot — **not** "the operator
toggled it" and not "it was disabled for 2h50m" (a bare `hypridle &` from a terminal would be
journal-invisible, and no instrument here can attribute the kill).

Blast radius: the *first* negative survives (`grep -ril idle` and `grep -ril lock` over
`install/first-run/` return no match, exit 1 each). The *second* negative fails. The S206/bar-side
claim is corroborated (`config.jsonc:208` `on-click: omarchy-toggle-idle`). Note for re-measurers:
my own read-only probes have since added `sudo[...]: COMMAND=/usr/bin/coredumpctl list hypridle`
lines to this journal (2026-10-25 03:34 and 03:37), so future `grep -i hypridle` runs are no
longer pristine; the `omarchy-toggle` count is unaffected.

## P1 (corrected) — the count is right; the receipt datum is unreproducible

Withdrawn in rev 2 and re-verified rather than trusted:

- `bin/omarchy-hook-install:27-29` is `mkdir -p` / `cp` / `chmod 755` only — no `bash`/`source`. first-run **installs** the hook; `bin/omarchy-hook:22-27` runs `$HOOK_DIR/*` later, on a `post-update` event.
- Set check (python3 -I, exit 0): `bash_targets: 12`, `dir_sh: 12`, `SET_EQUAL: True`, `body_minus_dir: set()`, `dir_minus_body: set()`, `hook_installed_not_run: ['install-voxtype.hook']`.
- Empirical: `~/.config/omarchy/hooks/post-update.d/install-voxtype.hook` still exists, 174 B, mode `-rwxr-xr-x`, its own line 6 `rm -f "$0"` unexecuted ⇒ never ran.

So "the installer runs 12 first-run scripts" is true of the script set, and "None of the twelve
asks about the idle lock" is sound. Remaining defect, receipt-side only: `ls .../ | wc -l` → 13
(exit 0, repeated) while `ls .../*.sh | wc -l` → 12 (exit 0); and S204's receipt records **no
command** for the datum (line 4 header, line 5 bare `count: 12`), so it cannot be re-run. Unlike
S203's receipt, there is no printed-vs-listed name mismatch here, because S204 lists no names.

## Peer-verified cautions

- `install/login/default-keyring.sh` `lock-on-idle=false` is `[keyring]`-scoped (gnome-keyring), not the desktop idle lock; never cited here.
- Setup *does* install the idle-lock config silently: `install/config/config.sh:3` `cp -R ~/.local/share/omarchy/config/* ~/.config/`, with `hypridle.conf` present in both trees (765 B, identical sha). So "the setup path asks nothing" holds; "setup never touches the idle lock" would be false, and is not claimed.

## P2 — receipt/anchor integrity: clean

- `sha256sum .../fetch/S204.receipt.txt` → `4cd5ba6518e4a6d950fcb510d2482e33be78abb20d22bef41d21a66f7d1c54ad` (445 B), exit 0.
- `SOURCES.md:206` `receipt sha256` cell → byte-identical 64-hex; compared over the full row (`hash_equals_anchor: True`). The `...` seen in a grepped view was renderer truncation.
- Gate-quote is a contiguous, byte-exact substring (`quote_in_receipt_bytes: True`) and appears verbatim in the entry (`quote_in_entry: True`); line 8 of 9.

## Counter status (read-only, run once)

```
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET      # exit 0
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET   # exit 0
```

Both frozen claims still hit TARGET_MET. C1's predicate is quote-contiguity plus registry/anchor
hygiene — it certifies that gate-quotes are contiguous receipt substrings, **not** that the
entries are true. It must not be reported as truth of content.

## Minimal fix (recommendation only — not applied)

1. Receipt: record the producing command with its population — `ls install/first-run/*.sh | wc -l`
   (=12) — and note the directory holds 13 entries because `install-voxtype.hook` is *installed*,
   not executed (copy+chmod; artifact still on disk).
2. Entry Section 2: delete *"the operator never exercised the toggle afterwards"*. If any negative
   is kept, base it on the hypridle scope lifecycle: *"the idle lock was disabled at 2026-10-23
   19:24:38 (scope released without a systemd stop) and no supported re-enable ran before the
   22:14:07 reboot"* — and drop the vacuous `grep omarchy-toggle` leg entirely.
3. S203's parallel defect is its receipt listing 13 names under `12` (their LOW-1); same re-mint
   pass, different fix.
