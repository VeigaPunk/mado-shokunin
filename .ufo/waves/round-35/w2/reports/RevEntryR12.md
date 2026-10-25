# RevEntryR12 — attack on `corpus/knowledge/idle-lock-never-asked-r12.md`

Seat: L1Mado35.RevEntryR12. Round 35, wave 2 (falsify). Read-only on every substrate;
writes confined to `.ufo/waves/round-35/scratch/RevEntryR12/` and this report.
Raw transcript of every command quoted below: `.ufo/waves/round-35/scratch/RevEntryR12/evidence.txt`
(**[REBUILT]**: an external sweep deleted the entire `scratch/` tree at ~03:45, this seat's directory
included, mid-review; the file was reassembled from this seat's transcript at ~03:47 and carries a
provenance header. `w2/reports/` was untouched. Content is transcript-faithful, not a re-run.)

## Verdict

**The file changed under this review, twice.** I was assigned the 40-line entry
(sha256 `21c1d06d…`, the golden control). Two writes landed while I was analysing it:
`03:35:08` (3586 B, 60 lines, sha `7f27ced0…`, adds E1+E2) and `03:41:38` (4344 B, 69 lines, sha
`0bcef21f…`, adds E3). The live entry now carries an `### Errata (round 35, wave 2)` block that
withdraws the exact inference my §2/F1 attack was aimed at and the independence claim in F3.
**The author is unattributed** — see §7.2/F9; the errata's own citation points at a seat that
disclaims it. Both states are assessed below; §1-§6 quote the assigned bytes with line numbers that
still hold, §7 assesses the errata that now sits under them and the residuals it introduces.

The entry has **two load-bearing claims**. One is true on today's bytes but is licensed by
**neither** cited receipt (it is an unlicensed negative over twelve file bodies). The other is
**falsified as evidence**: the S204 measurement (`grep -c 'omarchy-toggle'`) has *zero* detection
power over the event it denies, and the journal it measures contains a mid-session `hypridle`
termination that is exactly the toggle's disable effect. The entry's gate-quotes, hashes, source
ids and its twelve-name list all check out; the honesty failure is in what those bytes are said
to prove.

Current state, after E1-E3: **F1 acknowledged but only half-retracted** — E1 retracts §2, E3
retracts the title clause "for the same reason" yet deliberately keeps the title "as landed", and
the §1 OBS is untouched (§7.2/F8). **F3 is corrected by E3 in prose while §2's sentence still
reads "Two independent negatives agree"**; **F2 is now cited to my scan** (`RevEntryR12`), which is
a seat report, not a source row (§7.2/F9); **F4 is half-answered** — E2's "13 items" is
indefensible at any count (§7.3); **F5/F6/F7 are unaddressed**. Both counters print `TARGET_MET`
against the current bytes (C1 `closed_entries=3 closed_rows=8 open_cites=0`, C2
`uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1`, both exit 0) and both gate-quotes are
still byte-exact contiguous receipt substrings: the edits did not break the frozen claim, they left
the withdrawn assertions readable.

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

## 7. Delta — the errata written into the entry at 03:35:08 and 03:41:38 (`### Errata (round 35, wave 2)`)

Author unattributed (§7.2/F9). E1+E2 landed at 03:35:08; E3 landed at 03:41:38. All three are
assessed below against the current bytes (69 lines, sha `0bcef21f…`).

### 7.1 What the errata gets right (it corroborates §2/F1 and §2/F4)

- **E1** withdraws the "never toggled" inference and names the same mechanism and the same event I
  reached independently: scope `app-Hyprland-hypridle-9408787a` `Consumed` at `19:24:38`, no
  `Stopping`/`Stopped` pair, next start `22:14:11`, no coredump.
- **E2** corrects "twelve first-run scripts" to 12 `bash` scripts plus one hook and states that
  `install/first-run/` holds 13 entries.
- **E3** withdraws the title's second clause ("for the same reason as E1" — but see F8: it keeps
  the title as landed), corrects §2's "two independent negatives agree" in prose, and records that
  §1's "none of the twelve" is true on the host but unlicensed by S203/S204, citing my scan.

I re-measured every fact the errata introduces:

| Errata claim | My check | Verdict |
|---|---|---|
| no coredump for `hypridle` | `coredumpctl list hypridle` → `No coredumps found.` | **true** |
| scope died without a `Stopping`/`Stopped` pair | only `Stopping`/`Stopped hypridle` lines in the journal are at 13:21:39 (prior session teardown) | **true** |
| next start 22:14:11; "2h50m window" | 19:24:38 → 22:14:11 = 2 h 49 m 33 s wall clock, **across a reboot** (system journal: boot -1 last entry 22:12:24, boot 0 first 22:14:07). In-session absence: 19:24:38 → 22:10:20 = 2 h 45 m 42 s | **true as a gap, not as operator state** — see §7.3(a) |
| earlyoom 90.86 % free at 19:24:59 | system journal: `2026-10-23T19:24:59 earlyoom[1381]: mem avail: 19479 of 21438 MiB (90.86%)` | **true** |
| `install/first-run/` mtime `2026-10-03 17:42:32` predates the receipt | `stat` matches to the nanosecond | **true** |
| installer body "executes 13 items" | inside the `if`: 1 `rm -f "$FIRST_RUN_MODE"` + 12 `bash` + 1 `omarchy-hook-install` + 1 `sudo rm -f /etc/sudoers.d/first-run` = **15**; **14** excluding the guard's own state-file rm; **12** scripts | **false at every count** — "13 items" matches none; see §7.3(c) |
| `omarchy-hook-install` counted as an "item" | it *copies* the hook; the hook's own `rm -f "$0"` (line 6) has not run — artifact present at `~/.config/omarchy/hooks/post-update.d/install-voxtype.hook`, 174 B, 755 — and `/usr/bin/voxtype` is absent | **wrong verb** — installed, never executed; see §7.3(d) |
| E3: title "kept as landed rather than rewritten" | live l.1 still reads *"…and the operator never toggled it afterwards"* | **accurate description, defective policy** — see F8 |
| E3: §1 claim unlicensed, cites `RevEntryR12` | my scan: 13 files, 0 `idle` hits — accurate; but a seat report is not a registry row | **true and mis-sourced** — see F9 |

### 7.2 Findings on the errata itself

**F8 — HIGH: the retraction is incomplete, and E3 makes the omission deliberate.**
E1 retracts "Section 2's inference"; E3 retracts the title clause "for the same reason as E1" and
then says the title *"is kept as landed rather than rewritten."* All three assertion sites are
therefore live in the current bytes while the errata calls all three withdrawn:

- title, l.1: *"… and the operator never toggled it afterwards"*
- §1 OBS, l.23-24: *"And the operator never exercised the toggle afterwards (S204): the user
  journal holds zero `omarchy-toggle` invocations."*
- §2 OBS, l.28-29: *"Two independent negatives agree… the toggle was never run in any session the
  journal still keeps."*

Retraction-by-errata is a note, not an edit: a reader who stops at the title, or who consumes the
entry through an index or a `used-by` link, takes away claims the entry has itself withdrawn. The
title is the worst place to keep one — it is the line every downstream consumer reproduces, and
"kept as landed" converts an oversight into a decision. Required: rewrite l.1 to the setup-path
claim alone, strike or inline-mark both OBS sentences, and put the errata pointer above §1.

**F9 — HIGH (process and provenance): the lane corpus was written twice during a read-only wave by
an unattributed writer, and the appended facts carry no source row.**

What is measured:

- Two writes during this review: `03:35:08` (3586 B, 60 lines, sha `7f27ced0…`, E1+E2) and
  `03:41:38` (4344 B, 69 lines, sha `0bcef21f…`, +E3).
- The wave-2 seat contract forbids it: *"Write ONLY under `.ufo/waves/round-35/scratch/<YourSeatName>/`
  and your own report file. Never edit lane corpus files, counters, controls, SOURCES.md…"*.
- **Host forensics cannot name the writer, and I checked.** No journal line mentions the entry path
  (`journalctl | grep idle-lock-never-asked` → 0); no `mount --bind`/`umount` on the lane today; the
  only privileged commands in 03:30-03:45 are read-only `journalctl`/`coredumpctl`; agent file writes
  reach neither journal. This is *unattributed* — do not name a seat.
- **The file's own citation does not survive contact.** E1 says *"See
  `.ufo/waves/round-35/w2/reports/RevQuoteS204.md` (seat `RevQuoteS204`)"*, but that seat states it
  never wrote under `corpus/` (its declared writes: the report, and
  `scratch/RevQuoteS204/verify.log` at 03:37:07 — verified), and the cited report's mtime (03:40:46,
  since revised 03:43:39) **post-dates the E1 write by 5 m 38 s**. A citation to an artifact that did
  not yet exist in that form is not provenance. Phrase-matching the report proves nothing: it now
  quotes the errata, so the phrases appear there by quotation.
- The only lane-side process active at plan time, `.ufo/waves/round-35/assimilation/` (registration
  collision check), last wrote `03:30:46` — before both corpus writes — and is not the writer. No
  wave-2 seat in `w2-plan.json` (40 tasks) is chartered to edit corpus.

**Provenance of the appended facts.** E1's earlyoom reading, its `coredumpctl` result, the directory
mtime — and E3's citation of my twelve-file scan — enter through a **seat report**, not a registry
row whose anchor carries a receipt sha256, which is how every measurable claim enters this lane.
Either open receipted rows for the `hypridle`-death measurement and the `idle` scan E3 now depends
on, or label the errata explicitly "lane-reported, not admitted". As it stands, a frozen-claim
artifact C1 treats as closed carries unreceipted measurements and a citation to a seat.

**F10 — LOW: the errata is unattributed and its dates disagree with its own header.** It says
"round 35, wave 2", defers authorship to a peer report, and leaves the front matter at
`verified-at: 2026-10-24` while the appended material is from 2026-10-25 03:35/03:41. Two writes five
minutes apart, no author, no per-entry date: the append-only trail cannot be reconstructed from the
file. Stamp each errata item with its date, and move `verified-at` forward with the last one.

**F11 — LOW: `[INFERENCE-STRONG]` on "a toggle-off happened" is still an attribution.** The errata
concedes "that it was a click, menu or keybind is unverified", but `pkill -x hypridle` is not
unique to the toggle; any manual `pkill`, or any other agent, produces the identical footprint. The
honest statement is "the idle daemon was terminated mid-session by a signal from outside systemd;
the toggle's disable branch is one producer of exactly that footprint". One detail the errata is
missing strengthens the click/menu story without proving it: `walker` — the dmenu front-end of
`omarchy-menu`, whose Toggle submenu carries `Idle Lock` (`omarchy-menu:21-43`, `:207`, `:212`) —
logged a frame-timing line at `19:24:37`, one second before the kill.

### 7.3 Residuals the errata introduces or leaves (each re-measured)

**(a) "2h50m window with the idle daemon down" is a wall-clock gap across a reboot.** System-journal
boundaries: boot -1's last entry is `22:12:24`, boot 0's first is `22:14:07` (kernel line), `hypridle`
starts `22:14:11`. The gap `19:24:38 → 22:14:11` is `2h49m33s`, of which the machine was off for
~`1m43s`; the in-session absence is `19:24:38 → 22:10:20` = `2h45m42s` (user-journal last entry).
The daemon being down is a fact; that the *operator* left it down is the inference an earlier
revision dropped and E1 quietly restores.

**(b) Re-enable is only visible through `uwsm-app`.** Every supported re-enable path logs the same
signature — the toggle's ON branch (`uwsm-app -- hypridle`) and `omarchy-restart-hypridle:5` →
`omarchy-restart-app:7` (`setsid uwsm-app -- "$@"`). A bare `hypridle &` produces nothing. So the
journal proves no *supported* re-enable ran in that session; it does not prove the daemon was never
restarted. (`omarchy-restart-app:6` is off by one — the `setsid uwsm-app` line is 7.)

**(c) The count is 15 / 14 / 12, not 13.** Inside the mode-file guard: `rm -f "$FIRST_RUN_MODE"` (1)
+ 12 `bash` (12) + `omarchy-hook-install` (1) + `sudo rm -f /etc/sudoers.d/first-run` (1) = **15**;
excluding the guard's own state-file rm, **14**; scripts, **12**. E2's "13 items" matches none — and
it is the same miscount the errata was written to remove.

**(d) The hook was installed, never executed.** `omarchy-hook-install` copies `install-voxtype.hook`
to `~/.config/omarchy/hooks/post-update.d/`; the artifact is there (174 B, mode 755), and its own
line 6 `rm -f "$0"` has never run — the file would be gone. `voxtype` is not installed
(`/usr/bin/voxtype` absent). So the thirteenth artifact neither asks the operator anything nor has
ever run; E2's framing of it as an executed "item" is wrong in verb and in count.

**(e) E3's support for §1 is a seat, not a source.** E3 records that §1's claim is unlicensed and
"should cite that scan", naming `RevEntryR12`. The scan is real (13 files, 0 `idle` hits — §2/F2),
but a seat report is not a registry row; citing it puts the entry's one surviving content claim on
the same unreceipted footing as the rest of the errata (F9).

**Net effect on the entry.** §1's setup-path negative survives (true; still unreceipted — F2/F9).
§2 is withdrawn *in the errata* while its sentence still reads as a claim, and the title keeps the
withdrawn clause by explicit decision (F8). F3 is corrected in prose, not in text. F4 is half-answered
by an E2 that miscounts at every reading (§7.3c). E3 supports the one surviving content claim with a
seat name rather than a row (§7.3e). Both counters print `TARGET_MET` on these bytes, so the lane's
closure metric cannot see any of it.

## 8. Tooling

No installs; no package manager invoked (PACMAN paused). Only `journalctl` (user and system),
`grep`, `sha256sum`, `stat`, `pgrep`, `coredumpctl`, `find`, `diff`, `python3 -I` — all read-only.
Two counter runs on the post-edit bytes: C1 `…/c1/count.py` → `closed_entries=3 closed_rows=8
open_cites=0 TARGET_MET` (exit 0); C2 `…/c2/count.py` → `uncovered=0 retired=1 toctou_declared=1
ledger_tip_ok=1 TARGET_MET` (exit 0).

**Environment note.** The `scratch/` tree was deleted by an external sweep at ~03:45 mid-review; this
seat's evidence file was rebuilt from transcript (§0 header). The live entry itself was written twice
during the review by an unattributed writer (§7.2/F9), so every finding above is stamped with the
bytes it was measured against: assigned 40-line state (`21c1d06d…`) for §1-§5, current 69-line state
(`0bcef21f…`) for §7.
