# The idle lock was never offered as a choice at setup, and the operator never toggled it afterwards

Lane: mado-shokunin. Round: 35. Opened 2026-10-24 by this lane. Substrates
read-only: no first-run script was executed, no toggle was run and no journal entry
was written; every host read below is a file read or a read-only query.

source: [ref] - /home/vgpnk/.local/share/omarchy/bin/omarchy-first-run
source: [ref] - .ufo/waves/round-35/fetch/[ref].receipt.txt
verified-at: 2026-10-24
recheck: on-change

gate-quote: [ref] located: install/first-run/ lists 12 scripts; the omarchy-first-run body runs all 12; none is idle-lock
gate-quote: [ref] located: journalctl --user shows 0 omarchy-toggle invocations; the installer runs 12 first-run scripts

### Section 1 The setup path asks nothing about the idle lock

**OBS** The desktop's post-login questionnaire is a one-shot script ([ref]): it runs a
fixed list of twelve first-run scripts when its mode file is present, and the list is
battery monitor, internal monitor, sudoers cleanup, firewall, DNS resolver, GNOME
theme, swayosd, primary paste, text scaling, elephant, welcome and wifi. None of the
twelve asks about the idle lock.

**OBS** And the operator never exercised the toggle afterwards ([ref]): the user
journal holds zero `omarchy-toggle` invocations.

### Section 2 What this closes and what it does not

**OBS** Two independent negatives agree. The setup path offers no idle-lock choice,
and the toggle was never run in any session the journal still keeps.

**UNK** Whether the operator would rather the idle lock were off. No source can
answer it; the answer is one sentence from the person who owns the machine.

### Section 3 The scope of this entry

The package's round-12 text framed the finding as "the desktop never offers the
choice". That framing is too broad and is corrected here: this entry is about the
**setup path** only. The running interface does offer the choice, and
`corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` (adopted in the same round)
states that correction with its own evidence.

### Errata (round 35, wave 2)

- **E1 - "never toggled" withdrawn.** Section 2's inference that the operator never
  exercised the toggle is **withdrawn**. The toggle does not log under its own name, so
  a zero `omarchy-toggle` count is a null-channel reading, not a negative. The journal
  does record the daemon's lifecycle: scope `app-Hyprland-hypridle-9408787a` is
  `Consumed` at `2026-10-23T19:24:38-03:00` with no `Stopping`/`Stopped` pair (a process
  exit, not a unit stop) and the next start is `22:14:11` - a 2h50m window with the idle
  daemon down, inside the retained journal. `omarchy-toggle-idle` stops hypridle; no
  coredump exists for hypridle (`coredumpctl list hypridle` empty) and earlyoom reports
  90.86% free memory at 19:24:59, so a crash or OOM is ruled out. That a toggle-off
  happened is `[INFERENCE-STRONG]`; that it was a click, menu or keybind is unverified.
  The setup-path negative (§1) stands unchanged: no first-run script asks about the idle
  lock. See `.ufo/waves/round-35/w2/reports/RevQuoteS204.md` (seat `RevQuoteS204`).
- **E2 - thirteen items, twelve of them scripts.** The installer body executes 13 items:
  12 `bash …/*.sh` plus `omarchy-hook-install post-update …/install-voxtype.hook`. The
  phrase "twelve first-run scripts" holds for `*.sh` only; `install/first-run/` holds 13
  entries today and its mtime (`2026-10-03 17:42:32`) predates the receipt, so nothing
  changed after the read. The receipt recorded no command for its `count: 12` line.
- **E3 - the title's second clause and "two independent negatives".** This entry's title
  reads "…and the operator never toggled it afterwards"; that clause is withdrawn for the
  same reason as E1, and the title is kept as landed rather than rewritten. Section 2's
  "two independent negatives agree" is also corrected: [ref]'s `count: 12` re-derives [ref]'s
  own script list rather than independently confirming it, so the two readings are one
  measurement and one re-count. Finally, Section 1's "None of the twelve asks about the
  idle lock" is true on the host but is not licensed by [ref]/[ref], which carry no body of
  any script; wave-2 seat `RevEntryR12` re-derived it (0 `idle` matches across all 13
  files) and the claim should cite that scan.
