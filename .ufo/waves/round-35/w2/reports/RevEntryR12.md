# RevEntryR12 — attack on `corpus/knowledge/idle-lock-never-asked-r12.md`

Seat: L1Mado35.RevEntryR12. Round 35, wave 2 (falsify). Read-only on every substrate;
writes confined to `.ufo/waves/round-35/scratch/RevEntryR12/` and this report.
Raw transcript of every command quoted below: `.ufo/waves/round-35/scratch/RevEntryR12/evidence.txt`.

## Verdict

**The file changed under this review.** I was assigned the 40-line entry
(sha256 `21c1d06d…`, the golden control). At `2026-10-25 03:35:08`, mid-analysis, a sibling's
errata was written into the live entry; it is now 60 lines (`7f27ced0…`) and carries an
`### Errata (round 35, wave 2)` block that withdraws the exact inference my §2/F1 attack was
aimed at. Both states are assessed below; §1-§6 quote the assigned bytes with line numbers that
still hold, §7 assesses the errata that now sits under them.

The entry has **two load-bearing claims**. One is true on today's bytes but is licensed by
**neither** cited receipt (it is an unlicensed negative over twelve file bodies). The other is
**falsified as evidence**: the S204 measurement (`grep -c 'omarchy-toggle'`) has *zero* detection
power over the event it denies, and the journal it measures contains a mid-session `hypridle`
termination that is exactly the toggle's disable effect. The entry's gate-quotes, hashes, source
ids and its twelve-name list all check out; the honesty failure is in what those bytes are said
to prove.

Current state, after the errata: **F1 acknowledged but only half-retracted** (the title and the
Section-1 OBS still assert it — §7.2/F8), **F2/F3/F5/F6/F7 stand unchanged**, **F4 partly answered
by E2** while E2 itself miscounts. C1 still prints `TARGET_MET closed_entries=3 closed_rows=8
open_cites=0` (exit 0) against the post-edit entry: the counter is format-only and does not read
the errata.

---

## 1. OBS → the receipt bytes that license it

Entry has 40 lines, 3 `**OBS**` sentences (l.17-21, l.23-24, l.28-29) and 1 `**UNK**` (l.31-32).
Each OBS decomposes into assertions; nothing is licensed by "the entry says so".

### OBS-1, l.17-21 — "The desktop's post-login questionnaire is a one-shot script (S203): it runs a fixed list of twelve first-run scripts when its mode file is present, and the list is [12 names]. None of the twelve asks about the idle lock."

| Assertion | Licensed? | Bytes |
|---|---|---|
| one-shot, gated on a mode file | **yes** | S203 receipt `:13` (`FIRST_RUN_MODE=~/.local/state/omarchy/first-run.mode`), `:15-16` (`if [[ -f $FIRST_RUN_MODE ]]; then` / `rm -f "$FIRST_RUN_MODE"`) — the file is deleted *before* the runs, so it is one-shot |
| "runs a fixed list of twelve first-run scripts", list = *battery monitor, internal monitor, sudoers cleanup, firewall, DNS resolver, GNOME theme, swayosd, primary paste, text scaling, elephant, welcome, wifi* | **yes** | S203 `:18-27` (body 13-22: the ten mid-list `bash` calls) and `:31-32` (body 26-27: `welcome.sh`, `wifi.sh`) — twelve `bash` invocations, in exactly the entry's order |
| "post-login questionnaire" | **no** | S203 `:8` (body 3) reads `omarchy:summary=Finish the installation of Omarchy with items that can only be done after logging in`; `:9` (body 4) `requires-sudo=true`. The script asks the operator nothing. The word is inherited from the SOURCES.md:205 scope cell, which is also unsupported by this receipt |
| "None of the twelve asks about the idle lock" | **NO** | No receipt contains the body of any of the twelve. S203 `:34-48` is a *filename listing*; S204 `:4-5` is `count: 12`. The only text that asserts the negative is the receipt's own `located:` conclusion (S203 `:51`, S204 `:8`), which shows no computation over the twelve |

### OBS-2, l.23-24 — "the operator never exercised the toggle afterwards (S204): the user journal holds zero `omarchy-toggle` invocations."

| Assertion | Licensed? | Bytes |
|---|---|---|
| the journal holds zero `omarchy-toggle` **line matches** | **yes** | S204 `:2-3`: `command: journalctl --user --no-pager \| grep -c 'omarchy-toggle'` → `0`. Reproduced: `0`, pipeline exit 1 under `pipefail`, over 165,725 journal lines |
| the journal holds zero **invocations** | **no** | `grep -c` counts lines containing a substring. The command that actually toggles is `omarchy-toggle-idle` (S206 `:208`), whose 316-byte body never emits the string `omarchy-toggle` (evidence `[E15]`) |
| "the operator never exercised the toggle afterwards" | **NO** | Same instrument. It is blind by construction: disable → `pkill -x hypridle` (journal lines say `hypridle`, not `omarchy-toggle`); enable → `uwsm-app -- hypridle` (journal lines say `uwsm_app-daemon … app -- hypridle`, `Started hypridle.`). Neither branch names the command |

### OBS-3, l.28-29 — "Two independent negatives agree. The setup path offers no idle-lock choice, and the toggle was never run in any session the journal still keeps."

| Assertion | Licensed? | Bytes |
|---|---|---|
| "two independent negatives" | **no** | S204 `:4-5` (`count: 12`) is a re-derivation of S203; the two receipts are one witness plus one instrument, not two witnesses |
| "the setup path offers no idle-lock choice" | **no**, same gap as OBS-1's last sentence | — |
| "never run in any session the journal still keeps" | **no** | Same insensitive grep. The retention half is honest but unquantified: the user journal holds 3 boots, 2026-10-23T07:18:30 → 2026-10-25T03:31 (`[E8]`), ≈44 h |
| UNK l.31-32 (operator preference) | honest as written | — |

---

## 2. Does the entry claim more than the receipts support?

Yes, in seven places. Severity order.

### F1 — CRITICAL (assigned bytes; partially answered by the 03:35 errata, see §7): the second claim is falsified as evidence, and the journal holds a candidate counterexample

The entry's title (l.1) and OBS-2 (l.23-24) assert an unbounded "never". The only instrument is
`grep -c 'omarchy-toggle'`, and that string is emitted by **no branch of the toggle**:

```
/home/vgpnk/.local/share/omarchy/bin/omarchy-toggle-idle  (316 B)
 5 if pgrep -x hypridle >/dev/null; then
 6   pkill -x hypridle                      <- disable branch: journal shows "hypridle", no command name
 9   uwsm-app -- hypridle                   <- enable branch:  journal shows "uwsm_app-daemon … app -- hypridle"
13 pkill -RTMIN+9 waybar                    <- not journaled
```

Three invocation surfaces exist and none is journaled by name: the bar click
(`config.jsonc:208`, S206), the menu arm (`omarchy-menu:212`, S208), and a **keybinding**
(`default/hypr/bindings/utilities.conf:30`: `bindd = SUPER CTRL, I, Toggle locking on idle, exec, omarchy-toggle-idle`).
Zero detection power is therefore structural, not a matter of sample size.

The same journal contains a mid-session `hypridle` termination whose shape is the toggle's disable branch:

```
2026-10-23T13:25:00 Started hypridle.                              (boot -1 autostart)
2026-10-23T19:24:38 app-Hyprland-hypridle-9408787a.scope: Consumed 2.783s CPU
                    over 5h 59min 38.213s wall clock time
```

`13:25:00 + 5:59:38.213 = 19:24:38.213` (arithmetic checked, `[E10]`). The session did not end
until 22:10:20. There is **no** `Stopping hypridle.` / `Stopped hypridle.` for this scope (the only
`Stopped hypridle` in the journal is at 13:21:39, the previous session's teardown), and
`coredumpctl list hypridle` returns **no coredumps** (`[E11]`), so it was not a crash and not a
systemd-initiated stop: the process took a signal from outside. `hypridle` then stayed absent for
2 h 49 m until the next boot's autostart at 22:14:11. One second before the kill, `walker` — the
dmenu front-end that renders `omarchy-menu`'s Toggle submenu (`omarchy-menu:21-43`) — logged its
frame-timing warning at 19:24:37.

`pkill` sends SIGTERM by default, which is precisely the toggle's line 6. **Attribution to a toggle
invocation is `[INFERENCE]`**, not proof: a manual `pkill hypridle` produces the same bytes, and
`notify-send` leaves no journal trace (0 hits for `locking computer when idle`). But that is the
finding: the entry's cited instrument cannot distinguish "clicked the bar" from "never happened",
so the OBS is unsupported; and the journal does retain a concrete event of the denied class, which
the entry never mentions. The correct claim from these bytes is "the journal retains no line naming
the toggle command", which is true and worthless.

Consequence: C1 counts this entry as one of `closed_entries=3` (`c1/frozen.json:10`), and the
counter's predicate is format-only (row well-formedness, gate-quote contiguity). A falsified clause
passes C1 while being false evidence. That is a coverage-metric fact for the axis owner, not a
counter defect.

### F2 — HIGH: "None of the twelve asks about the idle lock" is an unlicensed content claim (it happens to be true)

Neither receipt carries the body of any of the twelve. S203 `:34-48` lists names; S204 `:4-5`
prints a count. The sentence is a claim about file *contents*, licensed by filename semantics and
by the receipt's own `located:` conclusion. The entry promotes that conclusion to `**OBS**` and
quotes it as its gate-quote (`:12`), so the reader is given a receipt line that reads like a
measurement but shows no scan.

I ran the scan the receipts are missing: `grep -ci idle` over all 13 files in
`install/first-run/` → **0 hits each** (`[E4]`), and the transitive calls inside the twelve
(`omarchy-battery-present`, `omarchy-battery-monitor.timer`,
`omarchy-recover-internal-monitor.service`, `omarchy-hw-match`) never reach `hypridle`. So the
claim is **true today** and the finding is evidentiary, not factual — the entry is right by luck of
the substrate, not by the bytes it cites. It must either cite the twelve bodies (new receipt) or
weaken to "none of the twelve is named for the idle lock".

### F3 — HIGH: "Two independent negatives agree" is false

S204's second block (`count: 12`, `:4-5`) is S203's number re-printed; the receipt's own title
(`:1`) states the setup-path conclusion as a premise. The two "negatives" are (i) one filename/list
inspection and (ii) one insensitive grep. Agreement between a witness and an instrument that cannot
see the event is not corroboration. Because `Two independent negatives agree` is the sentence that
does the epistemic work in Section 2 ("What this closes"), this overstatement is what makes the
entry look closed.

### F4 — MEDIUM: the "twelve" is a constructed set, and the receipt contradicts itself on 12 vs 13

S203 `:35` prints `12` directly above lines `:36-48`, which contain **13** filenames, including
`install-voxtype.hook`. The live directory has exactly 13 entries: 12 `.sh` + 1 `.hook` (`[E3]`).
The script itself executes **14** statements: the 12 `bash` calls plus
`omarchy-hook-install post-update …/install-voxtype.hook` (S203 `:28`) and
`sudo rm -f /etc/sudoers.d/first-run` (`:29`). The entry adopts the count `12` without reconciling
the receipt's 12-vs-13 contradiction and without disclosing that the 13th artifact in the same
directory is also processed by the same script. The negative survives — the hook has 0 `idle` hits
— but "the list is [12]" is the `bash`-call set, not `install/first-run/`'s list, and an unstated
selection is exactly what an honesty check is for. Same defect propagates into SOURCES.md:205's
`teaches` cell.

### F5 — LOW: "post-login questionnaire"

The cited body asks nothing; it is an installer hook body (`Finish the installation …`,
`requires-sudo=true`). The word imports the very behaviour the entry denies ("asks nothing"). It is
inherited from SOURCES.md:205, so the fix is registry-first. Load-bearing vocabulary, cheap to fix.

### F6 — LOW: recheck cadence

Entry says `recheck: on-change` (l.10); the registry rows say `on-request` (SOURCES.md:205-206,
col 11). C1's validator accepts both (`SYMBOLIC` matches), so closure is unaffected — but a
journal-derived negative whose truth flips on one operator click should carry a dated cadence and a
stated journal span (3 boots, 2026-10-23T07:18:30 → measurement), not `on-change`. As written the
entry cannot be re-falsified on a schedule; it can only be re-read.

### F7 — LOW: "(adopted in the same round)" (l.39) is unreceipted

No adoption record exists in the lane: `grep -rn 'adopted'` over `corpus/` and
`.ufo/waves/round-35/` finds this phrase only in this entry (and its control copies);
`corpus/QUALITY.md` has no `idle-lock` line; `.ufo/waves/round-35/ledger/` holds only
`RevFrozenBlobs-r35.md`. The cross-reference itself is sound — I re-read
`corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` and it does state the bar/menu correction
with S206-S210 — but "adopted" is an administrative claim no byte supports. Say "cross-referenced"
or cite the adoption record.

---

## 3. Is the 12-script list in the text exactly the list in the receipt?

**Against S203's body (:18-27, :31-32): exactly — 12/12, same order.** Machine check:
`re.findall(r'bash "\$OMARCHY_PATH/install/first-run/([a-z0-9-]+\.sh)"', body)` returns
`battery-monitor, recover-internal-monitor, cleanup-reboot-sudoers, firewall, dns-resolver,
gnome-theme, swayosd, gtk-primary-paste, text-scaling, elephant, welcome, wifi` (`[E20]`), which maps
one-to-one onto the entry's prose ("battery monitor, internal monitor, sudoers cleanup, firewall,
DNS resolver, GNOME theme, swayosd, primary paste, text scaling, elephant, welcome and wifi").

**Against S203's "first-run scripts on this host" block (:34-48): no.** That block lists 13 names
(alphabetical, includes `install-voxtype.hook`) under a header that says `12`. The entry silently
takes the body's 12. Both readings are defensible; the entry does not say which it took or why, and
the receipt's own count/list cardinality disagrees within four lines.

---

## 4. Do the `source:` ids resolve?

**Yes, both, cleanly.**

| Entry line | id | Registry row | Checks |
|---|---|---|---|
| l.7 | S203 → `/home/vgpnk/.local/share/omarchy/bin/omarchy-first-run` | SOURCES.md:205 | 13-column row, tier A, `status=mined`, `used-by=corpus/knowledge/idle-lock-never-asked-r12.md`; anchor file sha256 `20508471…` recomputed equal; 1089 B recomputed equal; receipt sha256 `1b7fa87f…` recomputed equal |
| l.8 | S204 → `.ufo/waves/round-35/fetch/S204.receipt.txt` | SOURCES.md:206 | 13-column row, tier A, `status=mined`, `used-by=` this entry; anchor receipt sha256 `4cd5ba65…` recomputed equal |

Gate-quotes (C1's own rule, `[E20]`): both are contiguous substrings of their receipts, 14 and 13
words, within 1-25. `S203 located: …` matches receipt `:51`; `S204 located: …` matches `:8`
byte-for-byte. `verified-at: 2026-10-24` is not stale: the host file still hashes identically today
and the grep still prints 0.

---

## 5. What the entry would have to say to be honest

1. Replace OBS-2 with: "the user journal retains no line naming `omarchy-toggle`; this command
   writes no such line, so the measurement cannot establish whether the toggle was used" — and cite
   the toggle body as its own source (S206 is insufficient; the body of `omarchy-toggle-idle` is
   not in any receipt).
2. Report the 2026-10-23T19:24:38 mid-session `hypridle` SIGTERM and say whether it can be
   attributed. It cannot, from these bytes — which is the point.
3. Either receipt the twelve bodies or narrow the negative to naming.
4. Drop "two independent negatives" and "questionnaire"; state the journal span (3 boots,
   2026-10-23T07:18:30 →) instead of "any session the journal still keeps".
5. State the 13th artifact (`install-voxtype.hook`) and the two non-`bash` statements.

---

## 6. Residual risk and verification gaps

- **Attribution of 19:24:38 is `[INFERENCE]`.** Manual `pkill -x hypridle` and the toggle produce
  identical journal bytes; `notify-send` is not journaled, so no branch can be positively confirmed
  journal-side. I did not run the toggle (forbidden) and did not test the footprint empirically.
  What is *not* inference: the string `omarchy-toggle` is emitted by no branch of the toggle
  (body read in full), and the three call sites run the command with no name in the output path.
- **Journal contamination.** ~90 concurrent seats are writing to this host; the journal contains
  fleet-generated `systemd-run` probes (e.g. `Started [systemd-run] /bin/sleep 30`). No
  fleet line names a toggle, but "user journal" is not a pristine operator artifact this round.
- **Unrelated oddity, recorded and not used as evidence:** `waybar` cored at 2026-10-25T02:06:16,
  `Signal: 11 (SEGV) si_code: SI_USER`, restarted 4 s later. It shows the journal records process
  deaths *with signal detail* — the reason the `hypridle` silence at 19:24:38 is informative — but
  the toggle sends `SIGRTMIN+9` to waybar, so this is not toggle evidence.
- **Not checked:** the round-12 package text the entry says it corrects (outside this entry's own
  claims); the twelve bodies under *historical* versions (only the live copy was read).
- **The substrate moved during the review.** The live entry changed at 03:35:08 (§7). The golden
  control `controls/golden/corpus/knowledge/idle-lock-never-asked-r12.md` (sha `21c1d06d…`) no
  longer matches the live entry (`7f27ced0…`; 20 changed lines). C1's `count.py` has no golden
  comparison, so `TARGET_MET` is unaffected (re-run: still `TARGET_MET`, exit 0), but any control
  seat that diffs golden against live now sees a deviation that is not an injected mutation.
- **My earlyoom probe initially looked like a false errata claim and is not one.** `grep -ci
  earlyoom` over `journalctl --user` returns 0; earlyoom is a *system* unit and the line the errata
  cites exists in the system journal (`2026-10-23T19:24:59 earlyoom[1381]: mem avail: 19479 of
  21438 MiB (90.86%)`). Recorded because a reader repeating the user-journal grep would wrongly
  conclude the errata invented it.

## 7. Delta — the errata written into the entry at 03:35:08 (`### Errata (round 35, wave 2)`)

### 7.1 What the errata gets right (it corroborates §2/F1 and §2/F4)

- **E1** withdraws the "never toggled" inference and names the same mechanism and the same event I
  reached independently: scope `app-Hyprland-hypridle-9408787a` `Consumed` at `19:24:38`, no
  `Stopping`/`Stopped` pair, next start `22:14:11`, no coredump.
- **E2** corrects "twelve first-run scripts" to 12 `bash` scripts plus one hook and states that
  `install/first-run/` holds 13 entries.

I re-measured every fact the errata introduces:

| Errata claim | My check | Verdict |
|---|---|---|
| no coredump for `hypridle` | `coredumpctl list hypridle` → `No coredumps found.` | **true** |
| scope died without a `Stopping`/`Stopped` pair | only `Stopping`/`Stopped hypridle` lines in the journal are at 13:21:39 (prior session teardown) | **true** |
| next start 22:14:11; "2h50m window" | 19:24:38 → 22:14:11 = 2 h 49 m 33 s | **true** (rounded) |
| earlyoom 90.86 % free at 19:24:59 | system journal: `2026-10-23T19:24:59 earlyoom[1381]: mem avail: 19479 of 21438 MiB (90.86%)` | **true** |
| `install/first-run/` mtime `2026-10-03 17:42:32` predates the receipt | `stat` matches to the nanosecond | **true** |
| installer body "executes 13 items" | 12 `bash` + `omarchy-hook-install` + `sudo rm -f /etc/sudoers.d/first-run` = **14** external commands | **imprecise** — the sudoers rm is dropped |

### 7.2 Findings on the errata itself

**F8 — HIGH: the retraction is incomplete; the entry now contradicts itself.**
E1 retracts "Section 2's inference". The identical assertion still stands, unqualified, twice
above it in the live file:

- title, l.1: *"… and the operator never toggled it afterwards"*
- §1 OBS, l.23-24: *"And the operator never exercised the toggle afterwards (S204): the user
  journal holds zero `omarchy-toggle` invocations."*

Only §2 (l.28-29) carries the withdrawal. A reader who stops at the title or §1 takes away the
claim the entry itself has withdrawn — and the title is the one line every index and `used-by`
consumer reproduces. Required: retitle to the setup-path claim alone, strike or explicitly mark
§1's second OBS, and put the pointer to the errata at the top of the file, not after §3.

**F9 — HIGH (process): the lane corpus was written during a read-only wave, and the appended facts
are unreceipted.**
The wave-2 seat contract says *"Write ONLY under `.ufo/waves/round-35/scratch/<YourSeatName>/` and
your own report file. Never edit lane corpus files, counters, controls, SOURCES.md…"*. The live
entry changed mid-wave anyway. Beyond the contract breach, the errata's new measurements
(earlyoom, `coredumpctl`, directory mtime) carry **no source id and no receipt** — the evidence
line is another seat's report path. Under this lane's own contract every measurable claim enters
through a registry row whose anchor carries a receipt sha256; as it stands, a file C1 treats as
closed now contains unreceipted measurements. Either open a receipted row for the `hypridle`-death
measurement or label the errata explicitly as lane-reported and not admitted.

**F10 — LOW: the errata is undated and unattributed.** It says "round 35, wave 2" and defers
authorship to a peer report; the front matter still reads `verified-at: 2026-10-24`. An
append-only errata needs its own date and author, or `verified-at` must move forward with it —
otherwise the file's top says one date and its last section is from another.

**F11 — LOW: `[INFERENCE-STRONG]` on "a toggle-off happened" is still an attribution.** The errata
concedes "that it was a click, menu or keybind is unverified", but `pkill -x hypridle` is not
unique to the toggle; any manual `pkill`, or any other agent, produces the identical footprint. The
honest statement is "the idle daemon was terminated mid-session by a signal from outside systemd;
the toggle's disable branch is one producer of exactly that footprint". One detail the errata is
missing strengthens the click/menu story without proving it: `walker` — the dmenu front-end of
`omarchy-menu`, whose Toggle submenu carries `Idle Lock` (`omarchy-menu:21-43`, `:207`, `:212`) —
logged a frame-timing line at `19:24:37`, one second before the kill.

**Net effect on the entry.** §1's setup-path negative survives (true, still unlicensed — F2);
§2 is withdrawn (correctly, on verified facts); the title and §1 still assert the withdrawn claim
(F8); F3's "two independent negatives agree" is untouched in the live bytes and is now doubly
wrong, since one of its two legs has been retracted.

## 8. Tooling

No installs; no package manager invoked (PACMAN paused). Only `journalctl`, `grep`, `sha256sum`,
`stat`, `pgrep`, `coredumpctl`, `python3 -I` — all read-only. One C1 counter run
(`python3 -I .ufo/waves/round-35/c1/count.py …`, exit 0, `TARGET_MET`) to confirm the mid-wave
corpus edit did not move the frozen target.
