# RevEntryR14 — attack on `corpus/knowledge/idle-lock-chain-armed-r14.md`

Seat: `L1Mado35.RevEntryR14` · wave 2 (falsify) · round 35 · 2026-10-25
Target: `corpus/knowledge/idle-lock-chain-armed-r14.md` — **current bytes reviewed** (3768 B, mtime 2026-10-25 03:35:30, sha256 `583c708c…0bf3`). The file changed twice under me mid-review (1789 B → 2505 B at 03:33:57, → 3768 B at 03:35:30) by another seat; I re-read it after each change and re-ran C1 (still `TARGET_MET`, rc=0). The changes are two appended errata (E1, then E2). **The body and title are byte-identical to the version I first read** — lines 1, 17 and 20 still carry the three falsified statements — so every verdict below applies to the current file, and the errata status is folded into §2, §3, §4 and §6.
Licensing source under test: `.ufo/waves/round-35/fetch/S205.receipt.txt` (1194 B, sha256 `f3387bfcbac79016034be38bab6548ae31df5860e5aafaa03105aca84b08ae1a` — matches frozen, row S205, and the plane note's conf digest)
Mode: read-only. No corpus/counter/registry/fleet file touched. No lock, screensaver, suspend or idle command issued.

## Axes

- **A1 licensing** — is every OBS a substring-measurable fact of S205, every INF derivable from those OBS, every UNK genuinely unknown?
- **A2 truth** — are the claims true of the host, measured read-only today (2026-10-25)?
- **A3 provenance** — are commands, unit names, exit codes and dates recorded, or reconstructed?
- **A4 checker fidelity** — does PRED-C1-r35-v1 bound claim truth, or only row/quote/hash shape?
- **A5 residue** — which unknowns the receipt actually raises but the entry omits.

## Verdict table

| # | Claim (verbatim locus) | Verdict | Basis |
|---|---|---|---|
| 1 | "the process probe prints pid 1667" | **LICENSED** | receipt `--- process probe ---` line 1; `pgrep -a -x hypridle` → `1667 /usr/bin/hypridle` rc=0 |
| 2 | "two `Started hypridle.` lines dated 2026-10-23" | **LICENSED** (dates are not) | receipt shows `Oct 23 13:25:00` / `Oct 23 22:14:11`; the year `2026` is absent from the receipt — INF-grade detail printed as OBS |
| 3 | "the later at 22:14:11 — **a restart, not a first start**" | **FALSIFIED** | the two lines are in **two different boots**, and each is its boot's **first** start (see §2) |
| 4 | "a screensaver at 150 seconds and a lock at 152" | **LICENSED** | receipt `10: timeout = 150`, `16: timeout = 152`; conf bytes re-read, digest matches |
| 5 | "**both** fire the desktop's own **lock command**" | **FALSIFIED** | 150 s → `omarchy-launch-screensaver`; that script never locks (see §3) |
| 6 | "`systemctl --user is-active hypridle` answers `inactive`" | **UNLICENSED (command), LICENSED (word)** | receipt records only the word `inactive`; neither command nor exit code is recorded |
| 7 | INF: "the daemon runs inside a transient scope unit … the unit reading is a probe artefact" | **TRUE but UNLICENSED by S205** | verified on host (§4), absent from receipt (§5 — the named gap) |
| 8 | INF: "`idle-lock-plane.md` … this round's measurement does not contradict it … state that has moved" | **TRUE but UNLICENSED and mis-typed** | reconciliation cites a different file; needs a pid start time S205 never measured |
| 9 | UNK: "no transition triggered or observed … whether it fires … unknown" | **LICENSED but incomplete** | true of S205; omits three unknowns the receipt itself raises (§7) |
| 10 | Title: "the daemon is running and **the chain will fire**" | **FALSIFIED as a finding** | §3 of the same entry says firing is unknown; a prediction is not a measurement |
| 11 | Appended errata E1 + E2 (file now 3768 B) | **DEFECT: annotated, not applied** | E2 withdraws #3 and #5 and concedes #7's gap, yet lines 1, 17, 20 are unchanged and E1's wrong wording remains in-file (§6) |

Mechanical status is green: both frozen counters pass, rc=0.

```
$ python3 -I .ufo/waves/round-35/c1/count.py --root /home/vgpnk/Projects/shokunin/mado-shokunin --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET     # rc=0
$ python3 -I .ufo/waves/round-35/c2/count.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --frozen .ufo/waves/round-35/c2/frozen.json
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET   # rc=0
```

## 1. The named gap — what the receipt actually supports

**The receipt shows `inactive` plus a live pid. It does not show the transient scope.** That is the whole of it.

S205's four measured sections are: a process list (`1667 /usr/bin/hypridle`, `hyprlock process: none`), a unit word (`inactive`), two journal lines, and four conf lines plus a digest. There is **no** `systemctl --user status`, no `list-units`, no `/proc/<pid>/cgroup`, no `loginctl`, no unit name, no exit code. The mechanism "it runs inside a transient scope unit" is therefore **not in the receipt at any remove**: it is imported world knowledge about how `uwsm-app` launches apps, and it is asserted in the entry as though the receipt had settled it.

Three separable defects:

1. **The unit word is not merely uninformative, it is undecidable as recorded.** `is-active` prints the same word `inactive` for two different states, distinguished only by exit code:
   ```
   $ systemctl --user is-active hypridle                                → inactive   rc=3   (unit exists, stopped)
   $ systemctl --user is-active definitely-not-a-unit-xyz.service       → inactive   rc=4   (no such unit)
   $ systemctl --user is-active app-Hyprland-hypridle-d4bd7533.scope    → active     rc=0
   ```
   S205 recorded neither the unit name nor the exit code, so its `inactive` is compatible with "`hypridle.service` loaded and stopped" **and** with "`hypridle.service` does not exist" **and** with "the probe asked a different unit family entirely". The entry's command string (`systemctl --user is-active hypridle`) is a plausible reconstruction, not a recorded fact.
2. **The reconciling mechanism was two grep tokens away in the very journal S205 read.** The receipt's own probe source (the user journal) contains, in the same second as the `Started hypridle.` line it did quote:
   ```
   2026-10-23T22:14:11-03:00 plazir27 uwsm_app-daemon[1805]: sent: exec systemd-run --user --scope \
     --slice=app-graphical.slice --unit=app-Hyprland-hypridle-d4bd7533.scope --description=hypridle \
     --quiet --collect --same-dir -- hypridle
   ```
   `journalctl --user -b | grep -i hypridle` returns it (3 lines total, rc=0). The receipt grepped only `Started hypridle` and dropped the line immediately above, which *is* the scope creation. So the INF is not merely unlicensed — the licensing evidence was in hand and was discarded.
3. **The receipt's own `located:` line over-asserts.** "hypridle runs as pid 1667 **and started in this session**" — the pid's start time appears nowhere in the four sections, and the pid→journal-line link is never made. The entry quotes this line as its gate-quote, so the quote passes the counter (§6) while the sentence it quotes is itself an unsupported conclusion. "Started in this session" happens to be *true* (pid 1667 `lstart = Fri Oct 23 22:14:10 2026`, scope `ActiveEnterTimestamp `Fri 2026-10-23 22:14:11`), but it is true by luck of the host, not by measurement in S205.

Minimal repair for the entry: the INF stays, but it must be re-sourced — cite `systemctl --user show app-Hyprland-hypridle-d4bd7533.scope -p Id,ActiveEnterTimestamp,ActiveState,ControlGroup` **plus** `/proc/1667/cgroup` and the `uwsm_app-daemon` journal line as a new receipt (do not rely on `-p MainPID`: a scope tracks no main pid — the property prints nothing, rc=0, so the pid→unit link must come from `ControlGroup` or `/proc/<pid>/cgroup`), and record the `is-active` exit code in S205's unit section. As written, under the entry's own rule — "every INF must be an inference from those OBS" — it fails.

## 2. `a restart, not a first start` — falsified

The two quoted lines are **not** in one session. They are in **two boots**, and each is the **first** start of its own boot:

```
$ journalctl --user --list-boots
 -2  2026-10-23 07:18:30 → 13:21:44
 -1  2026-10-23 13:24:57 → 22:10:20
  0  2026-10-23 22:14:08 → 2026-10-25 03:30:53   (now)
$ journalctl --user -b -1 -o short-iso | grep -o 'systemd\[[0-9]*\]' | sort -u   → systemd[1529]
$ journalctl --user -b  0 -o short-iso | grep -o 'systemd\[[0-9]*\]' | sort -u   → systemd[1493]
$ journalctl --user -b -1 -o short-iso | sed -n '1p'   → 2026-10-23T13:24:57 … Queued start job for default target Main User Target.
$ journalctl --user -b  0 -o short-iso | sed -n '1p'   → 2026-10-23T22:14:08 … Queued start job for default target Main User Target.
```

These are **user-journal** windows (`journalctl --user --list-boots`) — the substrate S205 read. The system journal's windows are kernel-bounded and its indices differ: system boot −1 is 13:24:36–22:12:24, system boot 0 starts 22:14:07, and a 41-second boot (`d577c6e0…`, system index −2, 13:22:32–13:23:13) exists with no user-journal entries, so system −3 ≡ user −2 and system −1 ≡ user −1. Boot IDs agree across both.

- `13:25:00 systemd[1529]` = boot **−1**, three seconds after that manager started → **first start of boot −1**.
- `22:14:11 systemd[1493]` = boot **0**, three seconds after that manager started → **first start of boot 0**.

Neither line is a restart. The receipt's section header, "journal start lines in **the current session**", is false for the 13:25:00 line, and the entry inherited and sharpened that frame into "a restart". Note the tell was available from the receipt alone: a single session has exactly one `systemd --user` manager pid, and the receipt prints two (`1529`, `1493`).

**Errata status (E1 at 03:33:57, E2 at 03:35:30).** E2 is correct and adopts my wording — "neither `Started hypridle.` line is a restart … each is its own boot's **first** start" — and its `_BOOT_ID` values (`e55f9cd9…` = boot −1, `0a3785aa…` = boot 0) match `--list-boots` exactly. Three residual defects: (a) **E1 is still in the file** saying the sentence "holds only *across boots*" — the wrong word survives in the document and E2 only says "E1 above is corrected", so the file now contains two competing statements about one event; collapse to one errata. (b) **The body sentence is untouched** — line 17 still reads "a restart, not a first start", so a reader who stops before the errata reads the false version. (c) The receipt's "current session" heading is still unamended in S205, and C1 still passes on the unchanged gate-quote.

Retention also bounds the claim: the journal's oldest entry is `2026-10-23T07:18:30` (198.1 MB, `/var/log/journal` present), and boot −2 (07:18–13:21) holds **no** hypridle start line. "The journal holds two lines" is therefore a statement about journal depth since 2026-10-23, not about how often the daemon has ever started; it can no more support "a restart" than "a first start".

## 3. `both fire the desktop's own lock command` — falsified

The two listeners are two different actuators, and only one is a lock:

```
$ sed -n '8,19p' ~/.config/hypr/hypridle.conf
listener {  timeout = 150
    on-timeout = pidof hyprlock || omarchy-launch-screensaver }
listener {  timeout = 152
    on-timeout = omarchy-system-lock
    on-resume  = omarchy-system-wake }
$ sha256sum ~/.config/hypr/hypridle.conf
e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41  (matches S205, row S205, plane note)
```

`~/.local/share/omarchy/bin/omarchy-launch-screensaver` was read in full (59 lines): it execs a terminal (`--class=org.omarchy.screensaver`) running `omarchy-screensaver`, i.e. a `tte` animation, and returns 1 if `tte` is absent; it contains **no** invocation of `hyprlock`, `omarchy-system-lock`, or any lock primitive. `omarchy-system-lock` is the only lock (`if ! pidof hyprlock; then ( hyprlock; omarchy-system-wake ) & fi`). The lane's own `idle-lock-plane.md` says the same thing in §1: "at 150 s idle → screensaver (TTE terminal animation, **not a lock**)". The entry flattens both into "the desktop's own lock command". Correct sentence: "a screensaver at 150 s and a lock at 152 s, both via desktop scripts; only the 152 s listener locks."

**Errata status.** E2 **withdraws** the claim ("Section 1's `both fire the desktop's own lock command` is **withdrawn**") with the same byte evidence — 59 launcher lines, no `hyprlock`/`omarchy-system-lock`/`swaylock` call. But line 20 still states it, and E2 does not rewrite it. The title line 1 ("the chain will fire") is likewise flagged by E2 and still unchanged; §3's own UNK remains the only correct statement in the file. A withdrawal recorded 20 lines below the claim is not a fix: the body must lose the sentence.

## 4. A2 — the transient-scope INF is true (out of receipt)

Measured read-only today; all three sources are historical records of 2026-10-23, not drift:

```
$ cat /proc/1667/cgroup
0::/user.slice/user-1000.slice/user@1000.service/app.slice/app-graphical.slice/app-Hyprland-hypridle-d4bd7533.scope
$ systemctl --user status app-Hyprland-hypridle-d4bd7533.scope
● … - hypridle
     Loaded: loaded (/run/user/1000/systemd/transient/app-Hyprland-hypridle-d4bd7533.scope; transient)
  Transient: yes
     Active: active (running) since Fri 2026-10-23 22:14:11 -03; 1 day 5h ago
        CGroup: … └─1667 /usr/bin/hypridle
$ ps -o pid,lstart,etime,args -p 1667
 1667 Fri Oct 23 22:14:10 2026 1-05:16:49 /usr/bin/hypridle
$ systemctl --user status hypridle.service
     Loaded: loaded (/usr/lib/systemd/user/hypridle.service; disabled; preset: enabled)
     Active: inactive (dead)
```

So the entry's mechanism is materially correct, *including the word "scope"* (`app-Hyprland-hypridle-*.scope`), and the static unit is `disabled` *by design* — the daemon is launched by Hyprland autostart through `uwsm-app`. The entry is right for the wrong reason: it guessed a true mechanism and attributed the guess to a receipt that contains no unit-membership evidence. A true unlicensed claim is still unlicensed; the defect is provenance, not correctness.

**Errata status (E1 at 03:33:57, E2 at 03:35:30).** E2 states the position exactly: "The transient-scope inference is materially true but **unlicensed by S205**", citing the `uwsm_app-daemon … systemd-run --user --scope …` line S205 failed to quote and the rc=3/rc=4 `inactive` ambiguity, and credits both seats. That is the right finding — but it still is not a repair: the body INF carries no receipt anchor, the errata cites a *seat* and a journal line that has no receipt row/hash, and the source row S205 is unchanged. Under the entry's own rule ("every INF must be an inference from those OBS") the sentence stays unlicensed until a new receipt exists; E2's prose is correct about the gap, not a closure of it.

Note the converse also holds: `inactive` for `hypridle.service` is the *correct* answer to the question that unit name asks. The probe is not lying, it is answering a different question — so "probe artefact" is fair only as "a liveness reading taken from the wrong unit name", which is what the entry says, and it should say that the unit is `disabled` (predictable, not anomalous) rather than imply a surprising disagreement.

## 5. A3 — provenance reconstruction in the entry

- Command reconstructed: the receipt has no command line for the unit probe, nor an exit code. Record both, next time.
- Year reconstructed: `2026-10-23` is inferred from the receipt header's `2026-10-24`; the journal lines carry no year.
- Mechanism attributed without a citation: the transient-scope sentence has no anchor in S205 and no citation to the uwsm autostart path (`default/hypr/autostart.conf` `exec-once = uwsm-app -- hypridle`, which `idle-lock-plane.md` §3 records).
- Digest is quoted in the registry row but never used in the entry; it is the one field that makes "the running daemon loaded these bytes" checkable. Conf mtime `2026-10-03 17:44:32` precedes the daemon start `2026-10-23 22:14:10`, so "the instance loaded the digested bytes" is a legitimate INF the entry did not make — and "it parsed them without error" is a genuine UNK it did not state (§7).

## 6. A4 — the counter passes an entry with two false OBS

`c1/count.py` closes a cite on: receipt hash in the row's anchor cell, exactly one registry row, `status=mined`, valid recheck token, and **one gate-quote that is a contiguous ≤25-word substring of the receipt**. It never parses `**OBS**` / `**INF**` / `**UNK**` and never compares them to the receipt.

```
$ python3 - <<'EOF'   # contiguity of the entry's gate-quote
quote = 'located: hypridle runs as pid 1667 and started in this session; hypridle.conf sets timeout 150 and 152'
# words=17, quote in receipt = True
EOF
```

The quote is the receipt's own `located:` summary — the one line that asserts more than the measurements support. So C1's closure is satisfied *by the weakest sentence in the receipt*. `TARGET_MET` therefore attests to row/quote/hash shape, not to the entry's truth: this entry carries two falsified OBS (§2, §3) and two unlicensed INF (§4, §5) and still lands `open_cites=0`. That is a finding about the predicate's coverage, and it is the cheapest available lift for the coverage axis: either the predicate grows a claim-type check, or the census stops calling `closed_entries` a truth verdict.

**The predicate is also stable under contradiction.** After E2 the file contains, in order: the claim (line 17/20), E1's competing wrong wording, E2's withdrawal, and a title that contradicts the entry's own UNK — and C1 still returns `TARGET_MET`, rc=0, on a byte-identical gate-quote. A counter that cannot see an assertion and its retraction in the same file cannot be evidence that the assertion is gone. Wave-3 lift: require the falsified body sentence to be **removed**, not annotated, and treat an errata block as an ordinary unverified claim — it gets a receipt and a hash like everything else, or it does not count.

## 7. A5 — unknowns the receipt raises and the entry omits

1. **Did the chain fire, and was it caught?** S205 records `hyprlock process: none` and the entry never uses it. A daemon started 2026-10-23 22:14 with a 150 s timeout, sampled ~1 day later with **no** lock process, is direct evidence that at the sample instant the chain was *not* in a fired state — either the operator kept the session active, or the chain failed to fire, or it fired and was dismissed. S205 cannot distinguish these; the entry should say so, because it is the difference between "armed" and "will fire" (title).
2. **Did the running instance accept the config?** `journalctl --user -b _SYSTEMD_UNIT=app-Hyprland-hypridle-d4bd7533.scope` → `-- No entries --` rc=0, and `journalctl --user -b | grep -ic hypridle` → 3 (none from hypridle itself). Silence is not success. "Loaded without error" is unmeasured.
3. **Is the armed chain actually reachable?** Binaries exist (`hyprlock 0.9.6-3`, `hypridle 0.1.8-2`, `tte`, both omarchy scripts on PATH) and no `screensaver-off` flag is set (`~/.local/state/omarchy/toggles/` holds only `hypr/`), so the actuators are present — the entry says none of this, and its UNK therefore reads as broader than the evidence requires while missing the narrower gap (whether a *firing* was ever observed).

Also worth stating: the sample was unlocked (`LockedHint=no`, `hyprctl layers` shows only `wallpaper` and `waybar`, no lock surface) — consistent with item 1.

4. **The audit is writing into the substrate it audits.** `journalctl --user --boot=0 | grep -ic hypridle` now returns **5**, not 3: the extra two are a wave-2 seat's own read-only probes, written to the journal as sudo records —
   ```
   2026-10-25T03:34:38 sudo[2181728]: vgpnk : PWD=…/mado-shokunin ; COMMAND=/usr/bin/coredumpctl list hypridle --no-pager
   2026-10-25T03:37:19 sudo[2637509]: vgpnk : PWD=…/mado-shokunin ; COMMAND=/usr/bin/coredumpctl list hypridle --no-pager
   ```
   Starts remain 1. Consequence for the entry's `recheck: 90d`: a later naive `grep -c hypridle` over boot 0 reads 5 (and will keep growing), and the persistent journal (198.1 MB, `/var/log/journal`) keeps these lines. Any re-measurement must match `Started hypridle\.` or filter `sudo`/`coredumpctl`. This is a hazard of the entry's own method — a journal read as evidence — not of the claim.
5. **No crash, which the receipt did not check and the entry did not claim or deny.** `coredumpctl list hypridle` → `No coredumps found` (rc=0); `coredumpctl list` has no hypridle/hyprlock entry (grep rc=1); no `segfault`/`crash`/`dumped` line for hypridle in the user journal (rg rc=1); and boot 0 holds no `Stopped hypridle.` line. So the single 22:14:11 start is one continuous run, refuting a crash-restart reading of the `inactive` probe. That supports "the daemon is running" while leaving "whether it fires" exactly where §3 puts it.

Self-correction on my own probe: the per-boot loop in the log prints `boot -3: 0`, but **user numbering has no boot −3** — `journalctl --user -b -3` answers `No journal boot entry found for the specified boot (-3)` (rc=1). The `0` was `grep -c` counting an empty stream, i.e. an absent index, not a boot with zero starts. The user-journal indices are −2, −1, 0; a zero-start boot under that numbering is only −2, and it is not empty — it carries `Stopping`/`Stopped`/`Consumed` lines for the pre-retention scope.

## 8. Unverified / limits of this review

- I did not reproduce a firing, and would not: no idle/lock/suspend command was run. Items in §7.1 remain UNK for this review too; my probes are point samples at 2026-10-25 03:30–03:35 −03:00.
- The pid 1667 → 22:14:11 journal line link is established by `lstart`/`ActiveEnterTimestamp` agreement, not by a recorded correlation at probe time. It is true, but S205 did not record it, and that is the point.
- I did not verify hypridle's in-memory config path (`/proc/1667/cmdline` would, but the daemon reads the default path when no `-c` is passed; `lstart` and conf mtime ordering make the digested bytes the near-certain input). Not load-bearing for any verdict.
- S205's raw `unit probe` command remains unknown; only the word `inactive` is recorded. My rc=3/rc=4 demonstration is a property of the `is-active` verb, not a claim about what S205 ran.

## 9. Tooling

No installs, no upgrades, no pacman transaction (host-wide pause respected). All probes used in-tree `python3`, `systemctl`, `journalctl`, `ps`, `pgrep`, `stat`, `sha256sum`, `hyprctl`, `loginctl`, `sed`. No file outside my report and my scratch directory was written.

**Scratch sweep.** An external sweep removed the whole `.ufo/waves/round-35/scratch/` tree at ~03:45, including this seat's directory (`ls scratch` → exit 2). I rebuilt `scratch/RevEntryR14/probe-log.md` from the session transcript with a header recording the removal; no value was re-derived or guessed. **No verdict depends on it** — every finding in §1–§7 quotes its command and exit code inline. I re-ran the load-bearing invariants after the rebuild (03:46): entry sha256 `583c708c…0bf3` and 3768 B / 03:35:30 unchanged, S205 sha256 `f3387bfc…` unchanged, conf digest `e7d3b8dd…de41` unchanged, `pgrep -x hypridle` → `1667`, scope `active` rc=0, `hypridle.service` `inactive` rc=3, C1 `TARGET_MET` rc=0, C2 `TARGET_MET` rc=0.
