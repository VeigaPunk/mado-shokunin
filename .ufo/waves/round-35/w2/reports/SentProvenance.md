# SentProvenance — are the eight S203–S210 receipts real host reads?

Round 35, wave 2, seat `L1Mado35.SentProvenance`. Attack only; no lane corpus file,
counter, control, SOURCES.md row or receipt was edited. Scratch and raw transcripts:
`.ufo/waves/round-35/scratch/SentProvenance/`.

## Axes

1. **Document integrity** — are the receipt bytes on disk the bytes the registry declares?
2. **Figure fidelity** — does every number/hash/line in a receipt reproduce on this host now?
3. **Command runnability** — can the producing command be run (or unambiguously reconstructed)?
4. **Claim binding** — does the re-derived figure actually measure the property the entry cites it for?

Axis 4 is where this attack lands. Every receipt passes 1–3; one fails 4 decisively.

## Verdict

| id | real host read? | figures re-derived | rank | deciding command |
|---|---|---|---|---|
| S203 | yes | 6/6 | **real** (1 label defect) | `sha256sum …/omarchy-first-run` → declared hash, rc 0 |
| S204 | yes | 4/4 | **partly-unverifiable** — numbers real, cited inference falsified | `journalctl --user --no-pager \| grep -c 'omarchy-toggle'` → `0`, rc 1 |
| S205 | yes | 6/6 | **real** | `pgrep -a hypridle` → `1667 /usr/bin/hypridle`, rc 0 |
| S206 | yes | 5/5 | **real** | `sha256sum …/waybar/config.jsonc` → declared hash, rc 0 |
| S207 | yes | 5/5 | **real** | `sha256sum …/waybar/indicators/idle.sh` → declared hash, rc 0 |
| S208 | yes | 5/5 | **real** | `sha256sum …/bin/omarchy-menu` → declared hash, rc 0 |
| S209 | yes | 5/5 | **real figures / defective framing** | `date -d @1791314470` → `2026-10-06T16:21:10-03:00` ≠ advertised `2026-10-03` |
| S210 | yes | 5/5 | **real** (registry prose overreaches) | `ls -1A …/toggles/hypr \| wc -l` → `2`, rc 0 |

No receipt is fabricated. None is a synthesised document: every figure in all eight matches
the live host, several to the nanosecond. **S204 is the exception in substance, not in
authenticity** — it is a faithful transcription of a real command whose output cannot
discriminate the event class it is cited to exclude.

## 1. Document integrity (axis 1)

`sha256sum .ufo/waves/round-35/fetch/S20[3-9].receipt.txt .ufo/waves/round-35/fetch/S210.receipt.txt` (rc 0)
returns, for all eight, exactly the receipt hash declared in `corpus/SOURCES.md`:

| receipt | sha256 (actual = declared) |
|---|---|
| S203 | `1b7fa87ffe933990ee59acf3629ffbe3a90106bc9ebcce082237f7f495dd1646` |
| S204 | `4cd5ba6518e4a6d950fcb510d2482e33be78abb20d22bef41d21a66f7d1c54ad` |
| S205 | `f3387bfcbac79016034be38bab6548ae31df5860e5aafaa03105aca84b08ae1a` |
| S206 | `1d30e4a999b53d5288369edc7573d7ceee0aef99570a55d781c4625440a938d5` |
| S207 | `81c33e7926f0bad071d31e9fc67e1d06967e3142da40ea3c93b16510b0adec59` |
| S208 | `6e72f0db3d7bbfecf4096b0aa22f716f417c00caa50b6d3319106387d6ce4654` |
| S209 | `a170c7a50b9305b3448fc85ecddb0d7b1f1c3ff5e42c78cdc2d07718c3bdd27c` |
| S210 | `ef282e386cdfb686fd331f4ed2fa7f0a33faf3ef4714844639b3eee4790b8726` |

No receipt was altered after registration. `stat -c '%y'` on the eight files gives
`2026-10-24 23:21:13` / `…23:21:21`, consistent with a single fetch pass on the stated
re-open date.

**Axis 3 caveat, systemic.** Only S204 records its command (`command: journalctl --user
--no-pager | grep -c 'omarchy-toggle'`). The other seven receipts print section headings and
results but never the producing command. I re-derived them by reconstructing the obvious
read (all reconstructions below are mine, not the receipt's). The receipts therefore are
*result documents*, not the (claim, command) pairs S001/S003 make the lane's unit of
evidence.

## 2. Per-receipt re-derivations

Every command below was run by this seat on 2026-10-25 between 03:30 and 03:36 -03.
Exit codes are the tool's; `grep -c` returning `1` means "no match", not command failure.

### S203 — omarchy first-run installer · **real**

| figure | receipt | re-derived | command | rc |
|---|---|---|---|---|
| file sha256 | `20508471…a062630` | identical | `sha256sum /home/vgpnk/.local/share/omarchy/bin/omarchy-first-run` | 0 |
| file size | 1089 B | `1089` | `stat -c '%s' …` | 0 |
| body lines 1–28 | printed verbatim | byte-identical, 28 lines | `sed -n '1,28p' …` | 0 |
| first-run script count | 12 | `12` (`*.sh`) / `13` (all entries) | `ls -1 …/install/first-run/*.sh \| wc -l` | 0 |
| bash invocations in body | 12 ("runs all 12") | `12` | `grep -c 'bash "$OMARCHY_PATH/install/first-run/' …` | 0 |
| idle-lock hits in first-run dir | none | `0` | `grep -ril idle …/install/first-run \| wc -l` | 0 |

Defect (low): the receipt prints the count `12` immediately followed by **13** names
(`install-voxtype.hook` included). The `12` is the `*.sh` count; the printed list cannot
reproduce it. The body does run 12 `.sh` and passes the `.hook` to `omarchy-hook-install`
(line 23), so the registry sentence "runs twelve first-run scripts" holds — but the receipt
does not state which glob produced `12`.

Scope check (not a defect in the receipt, a check on its wider use): the setup path has no
idle-lock question anywhere. `grep -ril idle …/omarchy/install/` returns only
`install/login/default-keyring.sh:12` (`lock-on-idle=false`, a keyring policy) and
`install/omarchy-base.packages:53` (`hypridle`). `welcome.sh` is a single `notify-send`.

### S204 — "the operator never toggled" · **partly-unverifiable**

| figure | receipt | re-derived | command | rc |
|---|---|---|---|---|
| `omarchy-toggle` occurrences | 0 | `0` | `journalctl --user --no-pager \| grep -c 'omarchy-toggle'` | **1** (no match) |
| first-run script count | 12 | `12` | `ls -1 …/install/first-run/*.sh \| wc -l` | 0 |
| implied journal window | not stated | starts `2026-10-23 07:18:30`, 3 boots retained | `journalctl --user --no-pager \| head -1`; `journalctl --user --list-boots` | 0 |

The numbers are exact. The claim they are cited for is not re-derivable, for three
independent reasons:

**(a) Null instrument.** The string `omarchy-toggle` is never written by anything in the
chain. The toggle's body (`/home/vgpnk/.local/share/omarchy/bin/omarchy-toggle-idle`,
lines 5–13) is: `pgrep -x hypridle` → `pkill -x hypridle` | `uwsm-app -- hypridle`,
then `pkill -RTMIN+9 waybar`, then `notify-send`. The journal's footprint of those actions
is `uwsm_app-daemon[…]: received: app -- hypridle`, `systemd[…]: Started hypridle.`, and
scope `Consumed`/`Stopping`/`Stopped hypridle.` — never the command's own name. Measured:
`journalctl --user --no-pager | grep -ci hypridle` → **10** lines, `grep -c 'omarchy-toggle'`
→ **0**. The counter returns 0 whether or not the operator ever clicked.

**(b) Window.** `journalctl --user --list-boots` retains exactly three boots
(-2: 2026-10-23 07:18:30–13:21:44; -1: 13:24:57–22:10:20; 0: 22:14:08–now). Coverage is
**44.29 h** from 2026-10-23 07:18:30. The offer has existed since at least 2026-10-03
17:44:32 (S209's oldest copy), i.e. **513.85 h**. The command witnesses **8.6 %** of the
period the entry's "never … afterwards" quantifies over; 469.57 h are unwitnessed.

**(c) A live event of exactly the class the receipt claims to exclude, inside the window.**
`journalctl --user --no-pager | grep 'app-Hyprland-hypridle'` (rc 0) shows the scope
`app-Hyprland-hypridle-9408787a.scope` **ending mid-session at 2026-10-23 19:24:38**
(`Consumed 2.783s CPU time over 5h 59min 38.213s wall clock time`), 2 h 46 min before that
session's last entry (22:10:20), with no restart until the next login's autostart
(22:14:11). Attribution checks:

- no systemd stop job at that instant (`grep 'Stopp.* hypridle'` returns only 13:21:39,
  the previous session's teardown `systemd[1490]`);
- no coredump: `sudo coredumpctl list hypridle --no-pager` → `No coredumps found.` (rc 0);
- no OOM: every `Memory cgroup out of memory: Killed process` line in 19:00–22:30 names a
  `cap-run-*` scope / `MainThread`, never hypridle;
- no suspend or lock event that day (`sudo journalctl … | grep -i suspend` → only
  `nvme … setting simple suspend`; `grep -icE 'hyprlock|omarchy-system-lock'` → 0).

A fatal signal is ruled out: `cat /proc/sys/kernel/core_pattern` →
`|/usr/lib/systemd/systemd-coredump …`, `Storage=external`, and the same evening produced
**20 coredump records** (`sudo coredumpctl list --since '2026-10-23 13:00' --until
'2026-10-23 22:30'`), including `19:37:50` — twelve minutes after the exit. `sudo
coredumpctl list hypridle --no-pager` returns one line (header only): no hypridle core has
ever been recorded. So SIGSEGV/SIGABRT does not explain the exit; the remaining classes are
a termination signal (`pkill -x hypridle` is the toggle's off-branch) or a voluntary exit
for which the evidence shows no trigger.

I report it as an **unattributed daemon termination, consistent with the toggle's off-path**,
not as a toggle: intent (click, menu, keybind) is unverified and this seat does not infer it.
The point for provenance is narrower and sufficient: the receipt's command reports `0` for a
window that contains a hypridle lifetime discontinuity it cannot express.

For completeness: the two `Started hypridle.` lines S205 cites are autostarts, not toggles —
`/home/vgpnk/.local/share/omarchy/default/hypr/autostart.conf:1` is
`exec-once = uwsm-app -- hypridle`, and each start lands 3 s after its boot's first entry.
Both statements can be true at once; that is precisely why the command must name the
channel it reads.

Rank: **partly-unverifiable.** Figures pass; the cited inference must not pass. The entry's
hedged sentence ("never run in any session the journal still keeps", r12:29) survives only
if the window is printed; the flat sentence (r12:23–24) and the title do not.

### S205 — idle-lock chain present state · **real**

| figure | receipt | re-derived | command | rc |
|---|---|---|---|---|
| daemon pid | `1667 /usr/bin/hypridle` | `1667 /usr/bin/hypridle` | `pgrep -a hypridle` | 0 |
| `hyprlock` present | none | none | `pgrep -x hyprlock` | 1 |
| unit probe | `inactive` | `inactive` | `systemctl --user is-active hypridle` | 3 |
| conf sha256 | `e7d3b8dd…8307de41` | identical | `sha256sum ~/.config/hypr/hypridle.conf` | 0 |
| timeouts | 150 at line 10, 152 at line 16 | `10: timeout = 150`, `16: timeout = 152` | `grep -n 'timeout = ' …` | 0 |
| declared lock commands (2,3,5,11,17) | printed | identical | `sed -n '2p;3p;5p;11p;17p' …` | 0 |
| journal start lines | 2 (`13:25:00` systemd[1529], `22:14:11` systemd[1493]) | identical, both systemd PIDs and seconds | `journalctl --user --no-pager \| grep 'Started hypridle'` | 0 |

`ps -o lstart` gives `Fri Oct 23 22:14:10 2026` and the unit list shows
`app-Hyprland-hypridle-d4bd7533.scope  loaded active running  hypridle`, so the entry's
INF (the daemon runs in a transient scope, not a `hypridle` service) is directly confirmed,
not merely plausible. Note the pid is a time-bound figure: it survives only until the next
hypridle restart, while the entry sets `recheck: 90d`. Pin the shape ("a live
`/usr/bin/hypridle` process in an `app-Hyprland-hypridle-*.scope`") and keep the pid in the
receipt.

### S206 — bar idle-indicator module · **real**

| figure | receipt | re-derived | command | rc |
|---|---|---|---|---|
| config sha256 | `a408a33d…58aae829` | identical | `sha256sum ~/.config/waybar/config.jsonc` | 0 |
| size | 6354 B | `6354` | `stat -c '%s' …` | 0 |
| lines 18–19 | `custom/idle-indicator`, `custom/notification-silencing-indicator` | identical | `sed -n '18p;19p' …` | 0 |
| block 207–212 | printed verbatim | identical | `sed -n '207,212p' …` | 0 |
| handler count | 1 | `1` | `grep -c omarchy-toggle-idle …` | 0 |

Corroboration the receipt did not need to state: line 18 sits inside `modules-center`
(lines 11–20), so the module renders; and `"signal": 9` is exactly what the toggle pushes
(`pkill -RTMIN+9 waybar`). The two files cohere mechanically.

### S207 — idle indicator script · **real**

| figure | receipt | re-derived | command | rc |
|---|---|---|---|---|
| sha256 | `6d8d2c11…d10f0f1750` | identical | `sha256sum …/indicators/idle.sh` | 0 |
| size | 159 B | `159` | `stat -c '%s' …` | 0 |
| body 3–6 | pgrep / empty text / tooltip | identical | `sed -n '3,6p' …` | 0 |
| tooltip count | 1 | `1` | `grep -c 'Idle lock disabled' …` | 0 |
| line count (implied) | 7 lines shown | `7` | `wc -l …` | 0 |

### S208 — desktop menu Idle Lock entry · **real**

| figure | receipt | re-derived | command | rc |
|---|---|---|---|---|
| sha256 | `d196b086…83a0f79d` | identical | `sha256sum …/bin/omarchy-menu` | 0 |
| size | 33017 B | `33017` | `stat -c '%s' …` | 0 |
| line 207 | `local options="… Idle Lock …"` | identical | `sed -n '207p' …` | 0 |
| line 212 | `*Idle*) omarchy-toggle-idle ;;` | identical | `sed -n '212p' …` | 0 |
| dispatch arm count | 1 | `1` | `grep -c omarchy-toggle-idle …` | 0 |

Reachability confirmed, which the receipt only implies: `show_toggle_menu` is called from
`omarchy-menu:101` (`*Toggle*) show_toggle_menu`) and `:860` (`*toggle*`); the menu is
invoked by the bar (`"custom/omarchy": { "on-click": "omarchy-menu" }`,
`config.jsonc:56-58`) and by `SUPER CTRL, O … exec, omarchy-menu toggle`
(`default/hypr/bindings/utilities.conf:5`). The host's `~/.config/hypr/bindings.conf:35`
has `SUPER, SPACE` commented out, but two uncommented routes remain.

### S209 — dated bar-config copies · **real figures, defective framing**

| figure | receipt | re-derived | command | rc |
|---|---|---|---|---|
| copies present | 4 | `4` | `ls -1 …/config.jsonc.bak* \| wc -l` | 0 |
| handler per copy | 1,1,1,1 | `bak=1 bak.1791314470=1 bak.1792203278=1 bak.1792267376=1` | `for f in …; do grep -c omarchy-toggle-idle $f; done` | 0 |
| mtimes | 2026-10-11 10:36 / 10-03 17:44 / 10-16 23:14 / 10-17 17:02 | identical to the nanosecond | `stat -c '%y %n' …` | 0 |
| oldest by mtime | (header says `.bak`; stat line says `.1791314470`) | `.bak.1791314470` at `2026-10-03 17:44:32.097653608` | `stat -c '%Y %y %n' … \| sort -n \| head -1` | 0 |
| copy names' epoch → time | not decoded | `date -d @1791314470` → `2026-10-06T16:21:10-03:00` | `date -d @<epoch> -Is` | 0 |

Two defects, one of them material.

*Label defect (low).* The section `--- oldest dated copy ---` prints the path
`/home/vgpnk/.config/waybar/config.jsonc.bak` (which is the **newest** of the four by mtime,
2026-10-11) and then the stat of `.bak.1791314470`. The two lines disagree; the second is
the true oldest.

*Metric swap (medium).* The copies are made by
`/home/vgpnk/.local/share/omarchy/bin/omarchy-refresh-config:23-29`:
`backup_config_file="$user_config_file.bak.$(date +%s)"` then `cp -f "$user_config_file"
"$backup_config_file"`. Naming clock and mtime are therefore the **same instant** (plain
`cp -f` resets mtime to copy time). Two copies obey that: name `1792203278` = mtime
`2026-10-16 23:14:38`, name `1792267376` = mtime `2026-10-17 17:02:56`.

The anchor copy does not: name `1791314470` = `2026-10-06T16:21:10-03:00`, mtime
`2026-10-03 17:44:32`, a **70.61 h** disagreement. Under the host's own backup tool that
pairing is impossible unless the mtime was set back afterwards (or the file was restored
with `cp -p`). The `style.css` siblings show the same pattern (`.bak.1791314470` and
`.bak.20261003-190229` share content and the `2026-10-03 19:02:29` mtime), so the
`1791314470` pair was taken on 2026-10-06 from sources last written on 2026-10-03.

Consequence for the entry: r15 §5 claims the package text "dated the oldest dated copy
2026-10-06" while "this round's own sweep … dates the oldest 2026-10-03". **Both are
readings of the same copy.** `2026-10-06` is exactly `date -d @1791314470`. The "divergence"
is a metric selection (filename clock vs mtime), not a re-measurement, and the receipt
discloses neither the filename clock nor the anomaly. Registry wording "the oldest dated
2026-10-03 on this host" should read "the oldest copy's mtime is 2026-10-03; its backup name
encodes 2026-10-06".

### S210 — toggle-state directory · **real**

| figure | receipt | re-derived | command | rc |
|---|---|---|---|---|
| files in `toggles/hypr` | 2 | `2` | `ls -1A ~/.local/state/omarchy/toggles/hypr \| wc -l` | 0 |
| file names | `flags.conf`, `window-no-gaps.conf` | identical | `ls -1A …` | 0 |
| files naming the idle lock | 0 | `0` | `grep -ril idle …/toggles/hypr \| wc -l` | 0 |
| toggles root | (implied single dir) | `hypr` only | `ls -1A ~/.local/state/omarchy/toggles` | 0 |
| does the idle toggle write here? | not cited | **no** — `grep -c toggles …/omarchy-toggle-idle` → `0` | `grep -n toggles …/omarchy-toggle-idle` | 1 |

The absence is real and, unusually, it is *meaningful*: `omarchy-toggle-idle` persists no
state at all (state = process presence). That is the decisive premise for the entry's INF
("built not to remember") and S210 does not cite it — S208's path happens to be the same
file. Cite `omarchy-toggle-idle:5-13` explicitly.

Registry prose defect (low): "holds entries for other toggles" (plural). `flags.conf` is a
comment-only sentinel (`# Do not remove this file (as the directory always needs at least
one file).`); only `window-no-gaps.conf` is a real toggle, written by
`omarchy-hyprland-window-gaps-toggle:5` → `omarchy-hyprland-toggle window-no-gaps` →
`~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf`. Say "one other toggle".

## 3. Findings, severity and remediation

**F1 (High) — S204's negative is a null instrument.** Exploit: any consumer (entry, counter,
gate) that reads `0` as "the operator never toggled" is satisfied by construction — the
measurement cannot return anything else. Evidence: 10 `hypridle` journal lines vs 0
`omarchy-toggle` lines; `omarchy-toggle-idle:9` runs `uwsm-app -- hypridle`, whose journal
text is `received: app -- hypridle`. Impact: r12's title and §1 OBS are unsupported; C1
counts the entry as closed on it. Remediation: replace with the daemon-lifetime witness and
print it:
`journalctl --user --no-pager | grep -E 'Started hypridle|Stopping hypridle|Stopped hypridle|app-Hyprland-hypridle.*Consumed'`

**F2 (High) — the claim's window is 8.6 % of the interval it quantifies over.** 44.29 h of
journal vs 513.85 h since the offer existed; 469.57 h unwitnessed, and the journal retains
three boots. Remediation: print `journalctl --user --list-boots` in the receipt and scope the
sentence to the retained window, or drop S204 and keep S203's positive setup-path claim.

**F3 (Medium-High) — an unrecorded daemon termination inside the window.** 2026-10-23
19:24:38: scope `app-Hyprland-hypridle-9408787a` ends mid-session; no stop job, no OOM
attribution, and no coredump — while coredump capture is demonstrably working on this host
(`Storage=external`, 20 records that evening including 19:37:50, zero for hypridle ever), so
a fatal-signal crash is ruled out. Signature matches the toggle's off-branch
(`pkill -x hypridle`); intent unverified. It must be reported as **unattributed** in the
receipt; while it stands unclassified, S204 cannot carry "never toggled".

**F4 (Medium) — S209's date metric is undeclared and its anchor copy is inconsistent with
the host's own backup tool.** Name `date +%s` and plain `cp -f` imply name ≡ mtime; the
anchor copy differs by 70.61 h. r15 §5's "divergence" from the package text is a metric
swap, not a measurement. Remediation: tabulate both clocks per copy, mark the
`.bak.1791314470` anomaly, and restate the offer's start as "at least 2026-10-06 (backup
name) / 2026-10-03 (mtime)".

**F5 (Low) — S209's `oldest dated copy` header names the newest file.** Re-derive with
`stat -c '%Y %y %n' … | sort -n | head -1`.

**F6 (Low) — S203 prints `12` above 13 names.** The `12` is `*.sh`; the list is `ls -1`.
Print the glob used.

**F7 (Low, systemic) — 7 of 8 receipts record no command.** This is the (claim, command)
pair requirement (S001, S003) unmet at document level: every figure had to be re-derived by
reconstruction. Remediation: each receipt section prints its exact command and exit code,
as S204 already does.

**F8 (Low) — pin hygiene.** S205's pid and S209's mtimes are state-bound; `recheck: 90d` on
a pid will go stale on the next hypridle restart. Pin the shape, keep the sample.

**F9 (Low) — S210 registry prose plural.** "entries for other toggles" is one real toggle
plus one sentinel file.

## 3a. Concurrent sibling edits during this attack

At 03:35:08 and 03:35:30 -03 — mid-run, after I read the entries at ~03:30 — other wave-2
seats rewrote all three entry files (`stat -c '%y'`: r12 `03:35:08`, r14 and r15
`03:35:30`). I made none of those edits; my analysis stands on the pre-edit text and is
reproducible from the receipts and the host alone.

The errata they appended independently converge with F1–F4 from the other direction:
r12 §Errata E1 withdraws "never toggled" as a "null-channel reading", names the same
`19:24:38` scope `Consumed` event, and E2 records the 12-vs-13 count (my F6);
r15 §Errata E1 names the dating clock and `date -d @1791314470` (my F4), E2 withdraws the
"never taken it" inference. Two seats reaching the same two defects through different
commands is the strongest confirmation this attack can offer that the defects are in the
receipts, not in one reader. What remains unresolved between us is only the strength of the
`19:24:38` attribution: one erratum calls a toggle-off `[INFERENCE-STRONG]`; this seat keeps
it unattributed (termination signal is the surviving mechanism, intent is not observable).

## 4. Effect on the round-35 claims

- C1 is not falsified: the three entries exist, the eight rows exist, the eight receipts are
  authentic and their figures match the host. What C1 counts as a *closed* entry is not the
  same as a *sound* one — `idle-lock-never-asked-r12.md` closes on F1–F3.
- C2 is unaffected by this seat: nothing here touches uncovered/retired/TOCTOU/ledger-tip.
- The receipts' authenticity is a positive result worth keeping: six of eight reproduce to
  the byte and the nanosecond, and all eight hashes match the registry.

## 5. Limits of this attack

- Read-only throughout. I did **not** execute `omarchy-toggle-idle`, `hypridle`, any lock,
  screensaver or suspend path; no journal entry was written by this seat. The toggle's
  journal footprint was established from its source and from the session's own log, not by
  running it.
- The 19:24:38 termination is reported as unattributed. Distinguishing a deliberate
  toggle-off from a silent crash would need evidence this host no longer keeps (no core, no
  per-process exit record).
- No tool was installed or upgraded; no package manager was invoked (pacman is paused
  host-wide).
