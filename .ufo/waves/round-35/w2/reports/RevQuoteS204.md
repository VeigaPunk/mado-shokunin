# RevQuoteS204 — wave 2 falsification of row S204

Seat: `L1Mado35.RevQuoteS204` (leaf, no dispatch). Read-only: no lane corpus file, counter,
`SOURCES.md`, receipt, or host state was written. Installs/upgrades: none.

**Evidence locus.** `round-35/scratch/` was *moved* to `round-35/scratch-evidence/` at ~03:43–03:45
(per-seat dirs intact, 59 seats), not deleted. For this seat: the pre-sweep original is 2140 B,
sha256 `f983ba8539b60bd1d484c3e20f441571acbca4c73a55c47e845921530be105b0`, preserved in commit
`4efaf63`; the copy now in the worktree and HEAD is 5081 B, sha256
`53b5fd38558dfcfe323b1d514e793a02e585e40570acc78e6d82ee48c820c598`, and is a **rebuild from this
seat's transcript** — not the bytes measured, therefore not evidence. Every command and exit code
this report relies on is inlined in Appendix A, so the report body is the durable locus.

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
- **Not a crash.** `coredumpctl list hypridle --no-pager` → `No coredumps found.` (exit 0, replayed at rebuild time — a direct instrument, not a no-match grep). The earlier date-scoped form `coredumpctl list --since 2026-10-23 --until 2026-10-25 | grep -Ei 'hypridle'` returned no match (exit 1); `journalctl -k --since '2026-10-23 19:20' --until '2026-10-23 19:30' | grep -Ei 'segv|oom|hypridle|killed'` → no match (exit 1).
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

## Entry-side errata — attribution and residuals (not authored here)

Between 03:35:08 and 03:41:38 on 2026-10-25 the frozen entry
`corpus/knowledge/idle-lock-never-asked-r12.md` was written twice by **another seat**:
3586 B at 03:35:08 (E1+E2), then 4344 B / sha256 `0bcef21fc93fe32f5f926b21d4f6f9655ffb32bd41f49280b0c074fb4469c504`
/ 69 lines at 03:41:38 (adds E3). This seat did not write to lane corpus; its only writes are
this report and the scratch log (pre-sweep `stat`: report 03:40:46, log 03:37:07; that log was
relocated to `scratch-evidence/` and a 03:46 rebuild replaced it in the worktree — both shas in the
header and Appendix A). The errata text is not a
copy of this report: an overlap probe run at 03:41 against the then-current report
(`grep -c` for "thirteen items, twelve of them scripts" / "null-channel reading" / "2h50m window
with the idle daemon down") returned 0 / 0 / 0. That probe is **historical and cannot be re-run
now**: this paragraph and item 3 quote the strings, so a fresh grep would match itself. Recorded
here as the observed result, not as a reproducible step.

Post-edit integrity, re-checked after both writes: `c1/count.py` → `closed_entries=3 closed_rows=8
open_cites=0 verdict=TARGET_MET` (exit 0); `c2/count.py` → `uncovered=0 retired=1
toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET` (exit 0); both gate-quotes still contiguous
byte-exact receipt substrings and still present in the entry.

Residuals I cannot close from outside that file:

1. **The withdrawn assertion is still asserted three times.** `never toggled it afterwards`
   (title line 1), `never exercised the toggle afterwards` (§1 OBS) and `the toggle was never run
   in any session the journal still keeps` (§2 OBS) all remain as text; E3 explicitly keeps the
   title "as landed". Retraction-by-errata leaves the claim live for a reader who stops at the
   title. That is a lane decision, not this seat's; recorded, not edited. Recommended fix: a
   banner above H1 plus inline withdrawal markers at §1 line 23 and §2 line 29, since anything
   quoting the title inherits the withdrawn claim (concurring with `RevEntryR15` and
   `RevQuoteS203`).
2. **E2 reproduces my withdrawn error.** "The installer body executes 13 items: 12 `bash …/*.sh`
   plus `omarchy-hook-install`" — `omarchy-hook-install` is `mkdir`/`cp`/`chmod` and does not
   execute the hook, and the enumeration omits `sudo rm -f /etc/sudoers.d/first-run`. Mechanically
   counted, the body invokes **15** external commands inside the mode-file guard: 1
   `rm -f "$FIRST_RUN_MODE"`, 12 `bash …/*.sh`, 1 `omarchy-hook-install post-update`, 1
   `sudo rm -f /etc/sudoers.d/first-run`. Excluding the guard's own state-file `rm`: **14**.
   Twelve remains the correct *script* count; "13 items" is not defensible under any of the three
   readings.
3. **E1 reintroduces an inference this report withdrew.** E1 states "a 2h50m window with the idle
   daemon down". Rev 3 drops that framing: the journal proves the *scoped* daemon was down and
   that no supported re-enable ran (toggle ON and `omarchy-restart-app` both log
   `received: app -- hypridle`); a bare `hypridle &` is journal-invisible, so the window is
   bounded, not proven. Defensible sentence: "the idle lock was disabled at 19:24:38 and no
   supported re-enable ran before the 22:14:07 reboot".
4. **E1's boundary is a reboot, not a session.** `journalctl --list-boots`: boot -1 `e55f9cd9…`
   runs 13:24:36 → **22:12:24**; boot 0 `0a3785aa…` starts 22:14:07.
5. **Unsourced measurements.** E1/E2/E3 carry figures (the 19:24:38 scope release, 90.86 % free,
   0 `idle` matches) with no source id and no receipt; under the lane contract they need a
   receipted row or an explicit "lane-reported, not admitted" label. This report is review-grade
   evidence — commands and exit codes quoted — not an admitted source.

## Registry mutation (SOURCES.md) — observed, not authored here

At 2026-10-25 03:40:12 `corpus/SOURCES.md` was rewritten: sha256
`0bf117e2f472ec4f80adec17d58fe50b4fbd4fa9568ffa8523a4bfc272950d51`, 171446 B (earlier state per
peer report: `848a7680…`). `c1/frozen.json` pins `id`, `predicate`, `target`, `entries` and
`receipts{path,sha256}` — **no registry hash and no entry hash** — so C1 cannot see registry or
entry prose rewrites; it re-checks only that each anchor cell carries the pinned receipt sha256
and that each entry gate-quote is contiguous. Verified after the rewrite: row 206 anchor still
`4cd5ba65…54ad`, row 205 anchor still `1b7fa87f…1646`, both `c1` and `c2` → TARGET_MET (exit 0).

Row-level residuals in the mutated registry:

- **Row 206 (S204), purpose cell still asserts the withdrawn claim:** "host evidence that the idle
  lock was never asked about and never toggled … the journal's absence of any omarchy-toggle
  invocation". The evidence cell now calls the same count "a null channel" — the two cells
  contradict each other.
- **Row 206, note cell is self-contradictory:** it opens "Two independent negatives agree" and
  ends "which is a null channel rather than a negative". A null channel cannot be the second of
  two agreeing negatives.
- **Row 206, evidence cell wording:** "the daemon's stop/start is consistent with a toggle-off" is
  accurate but should say *a disable event, unattributed* — sender identity is unrecoverable
  (§Residual risk), and only the toggle-OFF and restart paths are excluded by the ON-path
  visibility, not a manual kill.
- **Row 205 (S203), note cell regressed in precision:** "runs thirteen items … none of the
  thirteen executed items asks about the idle lock". "Thirteen commands" is also wrong — it drops
  L24 (`sudo rm -f /etc/sudoers.d/first-run`) — and the hook is installed, not executed. The body
  runs 15 commands (14 excluding its own mode-file cleanup). A line true under both readings:
  "thirteen first-run artifacts — twelve scripts that run, one hook that is installed and does not
  run; the body also clears `/etc/sudoers.d/first-run`".
- The `recheck` cell moved `on-request` → `on-change`; still a valid cadence token under C1.

## Residual risk and verification gaps

- **Compatible causes beyond the toggle.** A manual `pkill -x hypridle` from a terminal, or a
  keybind wrapper that calls it, is equally compatible with the 19:24:38 release: both are
  journal-invisible, and `~/.bash_history` holds no `hypridle` command (0 hits). The evidence
  identifies the *effect* (daemon killed mid-boot), never the *agent*.
- **Sender identity is unrecoverable.** `auditd`, `psacct`, `acct` all `inactive`; no
  `/var/log/account/pacct`; `~/.bash_history` 4572 B with `0` hits for `hypridle` and
  `omarchy-toggle`. So "'never toggled' is dead" is verified; "the operator toggled" is not, and
  is not claimed anywhere in this report.
- **The stop differential is inference.** Stopping/Stopped (systemd-initiated) vs Consumed-only
  (self-exit of a `--collect` scope) is systemd semantics, `[INFERENCE-STRONG]`, not reproduced —
  reproducing it would mutate host state.
- **A bare `hypridle &` is invisible** to every instrument used here. `bash_history` shows no such
  command, which weakens but does not eliminate the possibility.
- **The journal is no longer pristine for `hypridle` greps.** This seat's read-only probes added
  `sudo[...]: COMMAND=/usr/bin/coredumpctl list hypridle` lines (2026-10-25 03:34, 03:37). The
  `omarchy-toggle` count is unaffected.
