# RevQuoteS205 — adversarial re-quote of row S205 (wave 2, falsify)

Scope: registry row S205, receipt `.ufo/waves/round-35/fetch/S205.receipt.txt`, and the one
entry that cites it, `corpus/knowledge/idle-lock-chain-armed-r14.md`.
Seat posture: read-only attacks. Wrote only under
`.ufo/waves/round-35/scratch/RevQuoteS205/` (later relocated by an external sweep to
`scratch-evidence/` — see Evidence artifacts) and this report. No tool installs (nothing was
needed); no pacman transaction was attempted.

## Verdict

**S205 AGREES.** The gate-quote recorded in the entry is a contiguous substring of the receipt
bytes (single occurrence, byte 1091..1193 of 1194), all three facts it asserts re-verify on the
live host today, and the recomputed receipt digest equals the row's anchor digest exactly.

Five defects were found **outside** the gate-quote and the digest; none is read by any C1 clause.
They are reported below rather than folded into a disagreement claim:

- **P1** entry §1 "both fire the desktop's own lock command" — false, and contradicted by S205's
  own `declared timeouts` block (150 → `omarchy-launch-screensaver`, 152 → `omarchy-system-lock`).
- **P2** receipt's unit probe is bare `inactive`: no unit name, no exit code. Measured here,
  `inactive` is stdout for both rc=3 (exists, dead) and rc=4 (no such unit), so S205 cannot even
  establish that the unit existed.
- **P3** receipt heading "journal start lines in the current session" is false for the 13:25:00 line
  (boot −1).
- **P4** "a restart, not a first start" is wrong; each boot has exactly one start, and "two lines" is
  a journal-retention fact (boot −3 shows a pre-retention start via `Stopped` + scope `Consumed 1d 8h`).
- **P5** title "the chain will fire" contradicts the entry's own §3 UNK.
- **P6** C1 passes unchanged with the false body sentences still in place and two errata retracting
  them (`TARGET_MET`, rc=0; body lines 1/17/20 byte-identical). The predicate closes cites, not
  claims, and the errata carry no receipt/hash — verified after E2 landed (3768 B, 03:35:30).

- **P7** no crash: one start, no stop, no coredump, pid 1667 continuous 1 d 5 h 29 m — refutes a
  crash-restart reading of `inactive`, a positive the entry omitted. Same section records the
  method hazard: the audit writes `sudo coredumpctl` lines into the journal it reads, so a loose
  `hypridle` grep now yields 5 in boot 0 against 1 real start; rechecks must match `Started
  hypridle\.`.

- **P8** the registry row was rewritten mid-round (`SOURCES.md` mtime `03:40:12`; the `teaches` cell
  now says "one start line in the current boot (two across two boots)") while C1 stayed `TARGET_MET`.
  C1 never reads `teaches`, so closure is formal, not semantic; the rewrite itself is correct and was
  not mine (read-only seat).

- **P9** C1's receipt digest is dead code: `count.py:174` computes `digest`, `ok` never uses it, and
  the anchor clause only requires the frozen sha to appear in the row *text*. The repo's own content
  controls — `c1-shape-only` (56 B receipt, sha `22bdd47a…`) and `c1-fabricated-payload` (78 B, sha
  `75e98ef6…`) — both print `TARGET_MET` rc=0 against frozen `f3387bfc…`. `TARGET_MET` is shape
  closure, not provenance; both committed controls are positive and no negative control exists.

Findings P1/P2 were sharpened to the peer's corrections after a cross-check with `RevEntryR14`
(both verified here); P3/P4 quote user-journal windows, the scope S205 read. The material verdict did
not change. P9 bounds what the frozen result can mean, though: S205's agreement rests on my
independent digest, byte-offset and host checks — never on the counter alone.

## (a) Live host re-open — 2026-10-25, ~03:23–03:31 -03

| command | output | exit |
|---|---|---|
| `pgrep -x hypridle` | `1667` | 0 |
| `pgrep -ax hypridle` | `1667 /usr/bin/hypridle` (single instance) | 0 |
| `systemctl --user is-active hypridle` | `inactive` | 3 |
| `sha256sum /home/vgpnk/.config/hypr/hypridle.conf` | `e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41` | 0 |
| `grep -n timeout /home/vgpnk/.config/hypr/hypridle.conf` | `10: timeout = 150`, `16: timeout = 152` (plus the two `on-timeout` lines; exactly two `timeout` declarations) | 0 |

Supporting host facts, same run:

- `ps -o pid,ppid,lstart,etimes,cmd -p 1667` → `1667 1619 Fri Oct 23 22:14:10 2026 105367 /usr/bin/hypridle`.
  Parent 1619 is `Hyprland --watchdog-fd 4`.
- `cat /proc/1667/cgroup` → `/user.slice/user-1000.slice/user@1000.service/app.slice/app-graphical.slice/app-Hyprland-hypridle-d4bd7533.scope`.
- `systemctl --user status app-Hyprland-hypridle-d4bd7533.scope` → `active (running) since Fri 2026-10-23 22:14:11`,
  `Transient: yes`, `CGroup: … └─1667 /usr/bin/hypridle`, last journal line
  `Oct 23 22:14:11 plazir27 systemd[1493]: Started hypridle.` (exit 0).
- `systemctl --user show hypridle.service -p ActiveState -p SubState -p UnitFileState` →
  `ActiveState=inactive`, `SubState=dead`, `UnitFileState=disabled` (exit 0).
- `loginctl` → session 1 (manager, leader 1493) and session 2 (wayland, leader 1523), both with
  timestamp `Fri 2026-10-23 22:14:08 -03`, both `Active=yes`. `uptime -s` → `2026-10-23 22:14:06`.
- `pgrep -ax hyprlock` → no output, exit 1 (receipt's `hyprlock process: none` holds).

Every value matches the receipt's own probe block, down to the pid.

## (b) Gate-quote contiguity and fact match

Entry line 11 of `corpus/knowledge/idle-lock-chain-armed-r14.md`:

```
gate-quote: S205 located: hypridle runs as pid 1667 and started in this session; hypridle.conf sets timeout 150 and 152
```

Byte check against the receipt (`python3`, read-only):

```
quote_len 102 words 17
offset 1091 end 1193 file 1194
tail_after b'\n'
occurs 1
```

So: one occurrence, contiguous, 17 words (within the 1–25 bound), ending at the receipt's final
line plus newline. `grep -boF '<quote>'` independently reports `1091:<quote>`.

The counter's own extractor (`c1/count.py`, `gate_quote`) uses needle `gate-quote: S205 ` and takes
the rest of the line, i.e. exactly the 102-byte string above — the `S205 ` prefix is a source label,
not part of the quote. Consistent with my measurement.

Fact-by-fact, against the host reading in (a):

| gate-quote fact | host evidence | verdict |
|---|---|---|
| `hypridle runs as pid 1667` | `pgrep -ax hypridle` → `1667 /usr/bin/hypridle`; scope CGroup lists `└─1667` | TRUE |
| `started in this session` | pid 1667 `lstart` = 2026-10-23 22:14:10; sessions stamped 22:14:08; boot 0 since 22:14:06; scope active since 22:14:11 with the `Started hypridle.` line from systemd[1493] (this boot) | TRUE |
| `hypridle.conf sets timeout 150 and 152` | live conf lines 10 and 16; exactly two `timeout` declarations | TRUE |

The pid is not a fresh coincidence: the receipt was written 2026-10-24, the process lstart is
2026-10-23 22:14:10, and pid 1667 is still the live daemon on 2026-10-25 — the number in the
receipt was valid at write time and remains the same live process.

## (c) Receipt digest vs row anchor

```
sha256(.ufo/waves/round-35/fetch/S205.receipt.txt) = f3387bfcbac79016034be38bab6548ae31df5860e5aafaa03105aca84b08ae1a
```

Row S205 (`corpus/SOURCES.md:207`) anchor cell carries:
`… hypridle.conf sha256 e7d3b8dd…07de41; receipt sha256 f3387bfcbac79016034be38bab6548ae31df5860e5aafaa03105aca84b08ae1a`.

- Receipt digest equals anchor digest: **exact, all 64 hex chars**.
- Conf digest in the anchor equals the live conf digest: **exact**.
- The anchor digest also equals `c1/frozen.json` receipts.S205.sha256.
- Row shape: 11 cells (`awk -F'|' 'NR==207'` → `fields=11`), status `mined`, recheck `90d`,
  used-by exactly `corpus/knowledge/idle-lock-chain-armed-r14.md` (the only entry citing S205;
  `grep -rn S205 corpus/knowledge/*.md` returns only r14).

Context run of the two frozen counters (read-only; no writes):

```
python3 -I .ufo/waves/round-35/c1/count.py --root … --frozen …  → TARGET_MET closed_entries=3 closed_rows=8 open_cites=0  exit=0
python3 -I .ufo/waves/round-35/c2/count.py --repo … --frozen …  → TARGET_MET uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1  exit=0
```

## Findings (severity-ordered; none of these is read by a C1 clause)

### P1 — Entry §1 "both fire the desktop's own lock command" is false, and S205 contradicts it

Entry sentence: "**OBS** The declared chain is a screensaver at 150 seconds and a lock at 152
(S205), and both fire the desktop's own lock command."

The receipt's own `declared timeouts` block already refutes the second clause:

```
10:    timeout = 150
11:    on-timeout = pidof hyprlock || omarchy-launch-screensaver
16:    timeout = 152
17:    on-timeout = omarchy-system-lock
```

So S205 licenses "screensaver at 150, lock at 152" and explicitly shows that the 150 s action is
`omarchy-launch-screensaver`, not the lock command.

Host bytes confirm the launcher never reaches a lock:

- `/home/vgpnk/.local/share/omarchy/bin/omarchy-launch-screensaver` (59 lines): `grep -cE
  'hyprlock|omarchy-system-lock|swaylock'` → `0`, exit 1.
- It execs `omarchy-screensaver` (35 lines, same directory): same grep → `0`, exit 1; that script
  is a `tte` (TerminalTextEffects 0.15.0, present at `/usr/bin/tte`) animation loop with no lock call.
- Only the 152 s listener runs `omarchy-system-lock`.

The 150 s step starts a screensaver; the surface at 152 s locks. The clause is withdrawn in the
entry's own errata E2, but the sentence in §1 is still present and still cites (S205) for it.
This is a false claim *contradicted by the cited receipt*, not merely an unlicensed inference.

### P2 — Receipt's unit probe is unit-ambiguous and exit-code-free

Receipt lines 5–6 are:

```
--- unit probe ---
inactive
```

`grep -cE 'systemctl|is-active|pgrep|journalctl|sha256sum' S205.receipt.txt` → `0`: the receipt
names no command, no unit, and records no exit code.

The omission is load-bearing. Measured on this host:

| invocation | stdout | rc |
|---|---|---|
| `systemctl --user is-active hypridle` (unit exists, dead) | `inactive` | 3 |
| `systemctl --user is-active definitely-not-a-unit-xyz` | `inactive` | 4 |

Identical stdout; only the exit code discriminates "exists but stopped" from "no such unit".
S205 carries `inactive` with no code, so it cannot establish that `hypridle.service` existed at all.

Consequently entry §2's "`systemctl --user is-active hypridle` answers `inactive` (S205)" attributes
a command string the receipt never records, and the entry's INF (the unit probe measures the wrong
thing) is not licensed by S205: it needs the transient-scope evidence (cgroup, scope unit, uwsm
`systemd-run` line) that I gathered from the host, not from the receipt. Errata E2 states this
correctly; §2 of the entry still reads as if S205 licensed it.

### P3 — Receipt heading mislabels the earlier start line as this session's

Receipt section heading: `--- journal start lines in the current session ---`, listing

```
Oct 23 13:25:00 plazir27 systemd[1529]: Started hypridle.
Oct 23 22:14:11 plazir27 systemd[1493]: Started hypridle.
```

Windows are journal-scope-dependent, and both readings are right for their own journal (peer
correction verified):

| scope | earliest | boot −1 | boot 0 |
|---|---|---|---|
| `journalctl --user --list-boots` | `−2` 07:18:30–13:21:44 | 13:24:57–22:10:20 | 22:14:08–… |
| `journalctl --list-boots` (system) | `−3` 07:18:30–13:21:50; `−2` 41 s boot 13:22:32–13:23:13 | 13:24:36–22:12:24 | 22:14:07–… |

Boot ids agree across scopes: user −2 = system −3 = `6a7f4fdf…`, user −1 = system −1 =
`e55f9cd9…`, user 0 = system 0 = `0a3785aa…`. The 41 s boot `d577c6e0…` exists only in the system
journal (`journalctl --user --list-boots` omits it; it has no user-journal entries). S205's lines are
`systemd[NNNN]` user-manager messages, so the **user** windows `13:24:57–22:10:20` and `22:14:08–…`
are the ones to quote; the system windows I first published are the same boots seen from PID 1's
journal, indexed one higher because of the 41 s boot.

Verbose journal metadata confirms the provenance:

- 13:25:00 line → `_PID=1529`, `_BOOT_ID=e55f9cd9ec4e4dd5bf0ce775977af5a5` (boot −1), `_SYSTEMD_USER_UNIT=init.scope`.
- 22:14:11 line → `_PID=1493`, `_BOOT_ID=0a3785aac7104585a914f6cda41795a7` (boot 0, `/proc/sys/kernel/random/boot_id`).

Only the later line is in the current session; the 13:25:00 line is from the previous boot, present
because the journal is persistent. The row's `teaches` cell **was rewritten during this round**
(`corpus/SOURCES.md` mtime `2026-10-25 03:40:12`): it first read "the journal holds two start lines
on 2026-10-23", and now reads "the journal holds one start line in the current boot (two across two
boots) on 2026-10-23" — consistent with E2 (see P8). No C1 clause reads receipt headings or the
`teaches` cell, so this is prose-level imprecision, not a frozen-claim break. It is the exact kind
of cross-boot/provenance slip a reader would inherit if they quoted the heading.

Recommendation: retitle to `journal start lines across the last two boots` (or annotate the 13:25
line with `boot -1`). No change to the gate-quote, digest, or row is warranted by this finding.

### P4 — "a restart, not a first start" is wrong; "two lines" is a retention fact

`corpus/knowledge/idle-lock-chain-armed-r14.md` §1: "the user journal holds two `Started hypridle.`
lines dated 2026-10-23, the later at 22:14:11 - a restart, not a first start."

Per-boot start counts, user-journal numbering (`journalctl --user --boot=<n> | grep -c 'Started hypridle\.'`), with the system index in parentheses:

| user index (system) | starts | note |
|---|---|---|
| −2 (system −3) | 0 | holds `Stopping hypridle` / `Stopped hypridle.` plus `app-Hyprland-hypridle-59197064.scope: Consumed … 1d 8h 25min 52.144s` |
| — (system −2) | — | 41 s boot, `d577c6e0…`, no user-journal entries and no hypridle line in either scope |
| −1 | 1 | 13:25:00, systemd[1529]; first and only start of that boot |
| 0 | 1 | 22:14:11, systemd[1493]; first and only start of that boot |

The same counts read through the system journal (`journalctl --boot=<n>`) are `−3:0, −2:0, −1:1,
0:1` — identical boots, shifted index. The conclusion is scope-independent.

So neither line is a restart: each is its boot's first and only start. My earlier P3 wording
("defensible under the cross-boot reading") was too generous — "restart" implies an instance
restarting itself inside a boot, and no such event exists in the retained journal. Correct phrasing:
two boots, one start each, each the first of its boot.

Retention boundary: oldest journal entry is `2026-10-23 07:18:30` (user −2 / system −3). That boot's
`Stopped hypridle.` and its scope's `Consumed … 1d 8h 25min` line prove a start predating the
retained window. The statement "the journal holds two `Started hypridle.` lines" is therefore a fact
about journal retention, not about the daemon's start history.

The `13:24:57` / `22:10:20` pair the peer quoted is the user-manager window (first/last `--user`
entries for that boot); `13:24:36` / `22:12:24` is the system window (kernel first line, UFW last
line); `22:14:07` vs `22:14:08` is system vs user first entry for the current boot. All six values
reproduce; none changes the start-count conclusion.

### P5 — Title forecasts what §3 declares unknown

Entry line 1: `# The idle lock is armed on this host - the daemon is running and the chain will fire`,
while §3 states "No lock, screensaver or suspend transition was triggered or observed. … whether it
fires … stay[s] unknown." Errata E2 records the contradiction but the title itself is unchanged. On
the bytes I can check, the title's "the chain will fire" is a forecast with zero firing observation
behind it — and P1 shows that even the 150 s half of the chain does not lock. Editorial, not a
frozen-claim break.

### P6 — C1 is invariant under an assertion plus its retraction (verified)

State at 03:40: entry `3768 B`, mtime `2026-10-25 03:35:30`; errata E1 at line 41, E2 at line 49;
body lines 1, 17, 20 are byte-identical to the pre-errata text:

```
1  # The idle lock is armed on this host - the daemon is running and the chain will fire
17 at 22:14:11 - a restart, not a first start.
20 (S205), and both fire the desktop's own lock command.
```

C1 re-run with E1+E2 in the file: `closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET`,
rc=0. C2 likewise `TARGET_MET`, rc=0. Gate-quote line 11 is unchanged; the receipt digest is
unchanged (`f3387bfc…`).

So the frozen predicate closes **cites**, not claims: an entry can carry a false body sentence,
append two errata retracting it, and still count as `mined`/closed, because the only truth test is
the gate-line substring. The retraction is also unbacked — neither E1 nor E2 carries a receipt path
or hash and S205's digest is unchanged, so nothing in the artifact set records the correction. That
makes the peer's A4 lift ("remove the falsified body sentence; errata need their own receipt+hash or
they do not count") the right remedy: an errata that changes what an entry asserts must itself be a
cited, hashed artifact, or the entry's truth status stays unmeasured. The file currently holds E1
and E2 as competing statements about one event, and the counter cannot arbitrate between them.



### P7 — No crash (a positive the entry never made), and the audit mutates its own substrate

No-crash check, measured 2026-10-25 ~03:44:

```
$ coredumpctl list hypridle --no-pager
No coredumps found.
rc=1
$ coredumpctl list --no-pager >/dev/null; echo $?      # all coredumps, list succeeds
0
$ coredumpctl list | grep -iE 'hypridle|hyprlock'      # no match
rc=1
$ journalctl --user --boot=0 | grep -iE 'hypridle.*(segfault|crash|dumped)'
rc=1
$ journalctl --user --boot=0 | grep -c 'Stopped hypridle\.'
0
$ journalctl --user --boot=0 | grep -c 'Started hypridle\.'
1
$ ps -o pid,lstart,etime,cmd -p 1667
1667 Fri Oct 23 22:14:10 2026 1-05:29:03 /usr/bin/hypridle
```

One start, no stop, no coredump, same pid for 1 d 5 h 29 m: the 22:14:11 start is a single
continuous run. That **refutes a crash-restart reading** of the `inactive` unit probe (rc=3 dead, yet
the process has never crashed and lives in a scope), and it is a positive the entry never made while
asserting the unsupported scope mechanism. Correction to the peer's note: `coredumpctl list
hypridle` exits **1**, not 0 (the message is `No coredumps found.`); only bare `coredumpctl list`
exits 0. In a lane that grades on (command, exit code), that rc matters.

**Method hazard — the audit writes into the substrate it audits.** The journal is persistent and
grows: `journalctl --disk-usage` reports `249.9M` system-wide and `journalctl --user --disk-usage`
`198.1M` (the peer's 198.1 MB is the user-scope figure — same scope split again), and boot 0's loose
`grep -ic hypridle` count is now `5` while `Started hypridle\.` remains `1` and the `sudo` probe
count is `2`. The two extra lines are wave-2 seats' own probes:

```
Oct 25 03:34:38 … sudo[2181728]: vgpnk : PWD=…/mado-shokunin ; USER=root ; COMMAND=/usr/bin/coredumpctl list hypridle --no-pager
Oct 25 03:37:19 … sudo[2637509]: vgpnk : PWD=…/mado-shokunin ; USER=root ; COMMAND=/usr/bin/coredumpctl list hypridle --no-pager
```

So any 90-day re-measurement of this row must count `Started hypridle\.` (or exclude
`sudo`/`coredumpctl`), never a loose `hypridle` grep — otherwise the count inflates with reviewer
activity and can be misread as daemon restarts. The closed claim itself is safe: the receipt is
frozen bytes (`1194 B`, mtime `2026-10-24 23:21:21`, digest `f3387bfc…` unchanged), so audit growth
can only corrupt *re-derivation*, not the archived artifact. That is the same class of failure as
P6: the predicate measures an artifact, while the world underneath it keeps moving.

### P8 — The registry row itself was rewritten mid-round, and C1 did not move

`corpus/SOURCES.md` mtime is `2026-10-25 03:40:12`, and row S205's `teaches` cell (the counter's
`cs[6]`) changed between my first read and my post-E2 re-read:

- first read: `… the journal holds two start lines on 2026-10-23, while the unit probe reads inactive …`
- now: `… the journal holds one start line in the current boot (two across two boots) on 2026-10-23, while the unit probe reads inactive …`

Everything C1 constrains is unchanged: 11 fields, status `mined`, recheck `90d`, used-by exactly
`corpus/knowledge/idle-lock-chain-armed-r14.md`, anchor still carrying `f3387bfc…`. C1 re-run after
the rewrite: `TARGET_MET`, rc=0. The rewrite is semantically correct (it agrees with E2), and I did
not make it — this seat is read-only over the corpus.

Provenance of the comparison: the pre-rewrite text is from this seat's first read at ~03:33 (before
the `03:40:12` mtime); it is also commit-pinned independently — `git show 02088b4:corpus/SOURCES.md`
carries "…holds two start lines on 2026-10-23…", and `git show 4f35c80:corpus/SOURCES.md` carries
"…holds one start line in the current boot (two across two boots)…". Commit `4f35c80` is dated
`2026-10-25 03:42:04` and its subject is `round-35: wave-2 falsifications as errata — the
shape-scored counter, the falsified ledger claim, the census gaps and the misroot`. `git status` is
clean for `corpus/SOURCES.md` at HEAD `25536e6` (`round-35: closure sweep`), so the rewrite is
committed, not staged. The checkpoint transcript carries no row capture (`grep '^| S205 |'` on
`4efaf63:…/evidence.txt` = 0), so the 03:33 half of the comparison is transcript-based.

The point is structural, and it is P6's point one level out: a row's prose is free text that no
clause reads. The registry can be edited to agree with an errata, or to disagree with it, and the
frozen predicate cannot tell — it checks file identity, digest containment, status, cadence, used-by,
and the gate-quote substring. So `closed_rows=8` certifies that eight rows are well-formed and
receipt-anchored; it does **not** certify that their `teaches` text is true. Any inference from
closure to row truth is unsupported by the predicate.

Recommendation: bind the `teaches` cell to a hashed snapshot at freeze time, or state in the
criterion that closure is formal rather than semantic. Without one of those, a mid-round rewrite of
the thing being certified is invisible to the measurement — which is exactly what happened here.

### P9 — C1 never compares the receipt digest: fabricated receipts close with TARGET_MET

`c1/count.py:174` computes `digest = hashlib.sha256(blob).hexdigest()` and the variable is never used
again. The anchor clause is `receipt["sha256"] in cs[5]` — the **row text** must contain the frozen
sha; the receipt's actual bytes are never hashed against it. The repository's own content controls
prove the hole (run by me, read-only, rc as printed):

```
$ python3 -I .ufo/waves/round-35/c1/count.py --root .ufo/waves/round-35/controls-content/c1-shape-only --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
rc=0
$ python3 -I .ufo/waves/round-35/c1/count.py --root .ufo/waves/round-35/controls-content/c1-fabricated-payload --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
rc=0
```

Payloads, measured:

| root | r14 entry (whole file) | S205 "receipt" | receipt sha256 |
|---|---|---|---|
| `c1-shape-only` | `gate-quote: S205 snarfg plugh` | 56 B: `111111111111 snarfg plugh 999999999999 lorem ipsum void` | `22bdd47a10235e40f46b8e03c76d44167e3d69598632068a1e8efc615b5bb76c` |
| `c1-fabricated-payload` | `gate-quote: S205 fabricated attestation for S205` | 78 B: `THIS IS NOT A FETCHED RECEIPT` / `fabricated attestation for S205` / `ZERO REAL BYTES` | `75e98ef620ef50674511a311f7c06b90128f2a9c387b1436053e8e5063f9f5e6` |

Frozen S205 sha is `f3387bfc…`. Neither receipt matches; both close. The entry that "closes" in the
fabricated root contains nothing except a gate-quote over a 78-byte non-receipt.

Consequences:

- `TARGET_MET` certifies **shape**: three entry files exist; eight rows have 11 cells carrying the
  frozen digest *text*, correct status/cadence/used-by; and a 1–25-word quote is a substring of
  whatever bytes sit at the receipt path. It does not certify that any receipt was fetched, nor that
  S205's content is the measured host state.
- My S205 agreement is therefore **not** a counter result. I compared `sha256sum` of the receipt to
  the row anchor and to `c1/frozen.json` myself (all three `f3387bfc…`), byte-checked the 102-byte
  quote at offset 1091, and re-ran every host probe. That independent chain is what makes S205 real;
  the predicate alone would accept a 56-byte impostor.
- Both committed controls are **positive** (they pass). A content-integrity predicate needs a
  **negative** control — a root whose receipt bytes do not hash to the frozen sha and must print
  `TARGET_MISSED`. Without it the pair demonstrates "shape is sufficient", not "integrity is
  checked".
- One-line fix: use the computed value in `ok` (`digest == receipt["sha256"]`). Both mutants then
  fail, and the current lane must still pass.

Recommendation: report C1 as *shape closure*, never as coverage, and add the negative control before
any reader takes `closed_rows=8` as evidence that receipts are genuine.

## Positive corroboration of the entry's INF

The entry infers that `is-active` measures the wrong thing because the daemon runs in a transient
scope. The uwsm log for the same second makes this first-hand rather than inferred:

```
Oct 23 22:14:11 plazir27 uwsm_app-daemon[1805]: received: app -- hypridle
Oct 23 22:14:11 plazir27 uwsm_app-daemon[1805]: sent: exec systemd-run --user --scope --slice=app-graphical.slice --unit=app-Hyprland-hypridle-d4bd7533.scope --description=hypridle --quiet --collect --same-dir -- hypridle
Oct 23 22:14:11 plazir27 systemd[1493]: Started hypridle.
```

The `Started hypridle.` message names the **scope description** `hypridle`, not
`hypridle.service`; that service is `inactive/dead/disabled`. The entry's INF is therefore
supported verbatim by primary evidence — **but not by S205**, which never quotes the uwsm line, the
scope name, the cgroup, or an exit code (P2). The support is my host reading, and it is the reason
the INF is materially true despite S205 under-licensing it.

Scope-measurement nit, confirmed: `systemctl --user show …scope -p MainPID` prints an empty value
and exits 0 — a scope tracks no main pid. The process binding must be read from `ControlGroup`
(`… /app-Hyprland-hypridle-d4bd7533.scope` → `└─1667 /usr/bin/hypridle`) or from the scope's
`status`, not from `MainPID`.

## Cross-check with `RevEntryR14` (errata E1/E2)

Peer message received after my first report; every corrective claim was re-measured here, not
accepted on assertion:

| peer claim | independent check | result |
|---|---|---|
| 13:25:00 is boot −1's first start | `journalctl --boot=-1 \| grep -c 'Started hypridle\.'` → 1 | confirmed |
| 22:14:11 is boot 0's first start | `journalctl --boot=0 \| grep -c 'Started hypridle\.'` → 1 | confirmed |
| neither is a restart | per-boot counts 1/1; no second start in either boot | confirmed |
| boot −2 has no hypridle line | `journalctl --boot=-2 \| grep -ci hypridle` → 0 | confirmed |
| journal oldest entry 07:18:30 | `journalctl \| head -1` → `Oct 23 07:18:30` | confirmed |
| "two lines" is retention, not history | boot −3 holds `Stopping/Stopped hypridle` + scope `Consumed … 1d 8h 25min` (pre-retention start) | confirmed |
| 150 s step never locks | launcher 59 lines, screensaver 35 lines, 0 matches for `hyprlock\|omarchy-system-lock\|swaylock` | confirmed |
| `MainPID` empty for a scope | `-p MainPID` empty, exit 0 | confirmed |
| `inactive` cannot separate rc=3 from rc=4 | `is-active` existing → `inactive`/3; nonexistent → `inactive`/4 | confirmed |
| boot −1 spans 13:24:57–22:10:20 | `journalctl --user --list-boots` → `13:24:57–22:10:20`; system `--list-boots` → `13:24:36–22:12:24` | **scope distinction, not an error: both verified; S205 is user-journal so the user window is the one to quote** |
| no coredumps for hypridle | `coredumpctl list hypridle` → `No coredumps found.` | confirmed content; **rc=1, not 0** (bare `coredumpctl list` is the rc=0 case) |
| boot 0 has no `Stopped hypridle.` | `grep -c 'Stopped hypridle\.'` → 0; `Started` → 1 | confirmed; one continuous run |
| audit pollutes loose counts | loose `grep -ic hypridle` on user boot 0 → 5 vs `Started` → 1; the 2 extras are `sudo … coredumpctl list hypridle` probe lines at 03:34:38/03:37:19 | confirmed; rechecks must match `Started hypridle\.` |

Ownership note: I did not append errata E1 or E2 to
`corpus/knowledge/idle-lock-chain-armed-r14.md`. This seat is read-only over the lane corpus; my
deliverable is this report. Both errata postdate my first report write (03:32): E1 landed at 03:33
(file 2505 B), E2 at 03:35:30 (file 3768 B). E1's "holds only *across boots*" phrasing is the one the
peer asks to fix; E2 directly below it already corrects it (neither line is a restart; each boot's
first start), so E2 supersedes E1 and the pair should be collapsed to a single errata entry. Their
coexistence is itself evidence for P6: the document holds two competing statements, and C1 cannot
tell them apart.

## Residual risk / verification gaps

- All live probes are point samples from 2026-10-25 03:23–03:45 -03. A daemon exit or restart after
  the write would date the gate-quote's pid; the quote is session-scoped ("in this session"), so the
  snapshot is honest but not durable across a reboot.
- I did not and cannot observe the host state at receipt-write time (2026-10-24); what I verified is
  that the pid/digest/session facts hold now and that the lstart (2026-10-23 22:14:10) predates the
  receipt, so no pid-reuse explanation is available.
- The 13:25:00 line's boot attribution is **direct**, not by exclusion: `journalctl --list-boots`
  prints boot −1's full id `e55f9cd9ec4e4dd5bf0ce775977af5a5`, and the verbose entry for that line
  carries `_BOOT_ID=e55f9cd9ec4e4dd5bf0ce775977af5a5`. The 22:14:11 line carries
  `_BOOT_ID=0a3785aac7104585a914f6cda41795a7`, which equals boot 0's id and
  `/proc/sys/kernel/random/boot_id`. (An earlier draft hedged this as exclusion — it is a direct
  match; `--list-boots` does print full ids.)
- Entry prose semantics ("restart, not a first start") is not machine-checked by any counter; my
  reading of it is a human judgment and is filed as P4, not as a claim failure.
- The retention conclusion (P4) assumes the journal was not vacuumed *and* that a start line could
  not have been written to a different journal file; the `Consumed 1d 8h` scope line in user −2 /
  system −3 is positive evidence of a pre-retention start, but the absolute start count of the daemon
  over the host's lifetime is unknowable from what is retained.
- Journal-scope caveat: `--user` and system `--list-boots` number the same boots differently once the
  41 s system-only boot `d577c6e0…` is in range. Ids, not indices, are the join key; every count here
  is stated with its scope.

## Evidence artifacts

Evidence was relocated mid-review. `scratch/` was **moved** (not deleted) to `scratch-evidence/` at
~03:45 by an external sweep; `scratch/` was then partly re-created and swept again. Two copies
matter, and they are not the same bytes:

1. **Pre-move transcript, commit-pinned.** `4efaf63:.ufo/waves/round-35/scratch-evidence/RevQuoteS205/evidence.txt`
   — blob `9620ca1580e92256558870e17f905d07cc80c7c2`, 8205 B, 190 lines, header
   `# RevQuoteS205 evidence 2026-10-25T03:31:59-03:00`. It carries the live probes, the gate-quote
   byte offset, row checks, both journal scopes, per-boot counts, provenance, and the post-E2
   C1/C2 runs. It predates the no-crash block (`grep coredumpctl` there = 0).
2. **Rebuild — explicitly not the measured bytes.** `scratch-evidence/RevQuoteS205/evidence.txt` in
   the worktree: 9858 B, 203 lines, sha256
   `e6c8e30e9542874d63260741db8535ac0a5ad42e2835000ae8d903f584097283` (git blob `a3355706…`, staged
   in the index while HEAD is `4efaf63`). It adds the P7 no-crash/coredump and audit-hazard blocks.
   A rebuild is a convenience copy, not evidence.

3. **Control roots (P9).** `.ufo/waves/round-35/controls-content/{c1-shape-only,c1-fabricated-payload}`
   — 24 tracked files, worktree clean at HEAD `25536e6`; the S205 payload shas are pinned in P9.
   Both close `TARGET_MET` rc=0 when re-run by me.

P7 and P8 were measured after the checkpoint, so their decisive commands and outputs are inlined in
those sections above; no finding depends on either scratch copy. The report body is the durable
evidence locus — the checkpoint is a 03:43 snapshot and `scratch/` is not stable.

Every command quoted here was run on this host during the review; no value is copied from the receipt
or from another seat's report without a re-run recorded here.
