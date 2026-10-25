# The idle lock was never offered as a choice at setup, and the operator never toggled it afterwards

Lane: mado-shokunin. Round: 35. Opened 2026-10-24 by this lane. Substrates
read-only: no first-run script was executed, no toggle was run and no journal entry
was written; every host read below is a file read or a read-only query.

source: S203 - /home/vgpnk/.local/share/omarchy/bin/omarchy-first-run
source: S204 - .ufo/waves/round-35/fetch/S204.receipt.txt
verified-at: 2026-10-24
recheck: on-change

gate-quote: S203 #!/bin/bash  # omarchy:summary=Finish the installation of Omarchy with items that can only be done after logging in. # omarchy:requires-sudo=true  set -e  FIRST_RUN_MODE=~/.local/state/omarchy/first-run.mode  if [[ -f $FIRST_RUN_MODE ]]; then   rm -f "$FIRST_RUN_MODE"    bash "$OMARCHY_PATH/install/first-run/battery-monitor.sh"   bash "$OMARCHY_PATH/install/first-run/recover-internal-monitor.sh"
gate-quote: S204 located: journalctl --user shows 0 omarchy-toggle invocations; the installer runs 12 first-run scripts

### Section 1 The setup path asks nothing about the idle lock

**OBS** The desktop's post-login questionnaire is a one-shot script (S203): it runs a
fixed list of twelve first-run scripts when its mode file is present, and the list is
battery monitor, internal monitor, sudoers cleanup, firewall, DNS resolver, GNOME
theme, swayosd, primary paste, text scaling, elephant, welcome and wifi. None of the
twelve asks about the idle lock.

**OBS** And the operator never exercised the toggle afterwards (S204): the user
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
