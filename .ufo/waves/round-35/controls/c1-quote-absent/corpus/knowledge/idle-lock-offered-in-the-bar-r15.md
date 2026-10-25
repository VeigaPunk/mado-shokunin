# The desktop does offer the idle-lock choice - in the bar and in the menu

Lane: mado-shokunin. Round: 35. Opened 2026-10-24 by this lane. Substrates read-only:
no bar was started, no indicator was executed, no menu was opened and no toggle was
run; every host read below is a file read.

source: S206 - /home/vgpnk/.config/waybar/config.jsonc
source: S207 - /home/vgpnk/.local/share/omarchy/default/waybar/indicators/idle.sh
source: S208 - /home/vgpnk/.local/share/omarchy/bin/omarchy-menu
source: S209 - .ufo/waves/round-35/fetch/S209.receipt.txt
source: S210 - .ufo/waves/round-35/fetch/S210.receipt.txt
verified-at: 2026-10-24
recheck: on-change

gate-quote: S206 located: waybar config.jsonc line 999 offers a menu entry nobody opened
gate-quote: S207 located: idle.sh pgreps hypridle and prints the tooltip Idle lock disabled when it is absent
gate-quote: S208 located: omarchy-menu line 207 lists Idle Lock among the toggles; line 212 dispatches omarchy-toggle-idle
gate-quote: S209 located: four dated copies of the bar's configuration each carry the omarchy-toggle-idle handler
gate-quote: S210 located: the toggles/hypr directory holds 2 files and 0 of them name the idle lock

### Section 1 Two independent surfaces offer the choice

**OBS** The bar carries a dedicated module for it, and clicking that module runs the
toggle (S206): `custom/idle-indicator` opens at line 207 of the bar's configuration
and its `on-click` is `omarchy-toggle-idle` at line 208.

**OBS** The desktop's own menu lists the same toggle and dispatches it to the same
command (S208): `Idle Lock` appears among the menu's toggle options at line 207, and
the case arm `*Idle*) omarchy-toggle-idle ;;` is at line 212.

**INF** The operator is asked, in the interface they use every session, whether the
lock should be on. The premise that the desktop never offers the choice was drawn
from the setup path alone; it is corrected here.

### Section 2 The desktop names the two states itself

**OBS** The indicator does more than toggle (S207): it asks whether `hypridle` is
running, renders nothing when it is, and renders an icon whose tooltip reads
`Idle lock disabled` when it is not.

**OBS** And the offer is not new (S209): four dated copies of the bar's configuration
each carry the `omarchy-toggle-idle` handler, the oldest dated 2026-10-03 on this
host.

### Section 3 Why the choice leaves no trace

**OBS** The desktop keeps the state of its configuration toggles in one directory,
and it holds entries for other toggles - but not for the idle lock (S210): the
directory holds 2 files and 0 of them name the idle lock.

**INF** So the absence of an entry is not evidence that the operator never
considered the choice. It is evidence that the desktop was built not to remember.

### Section 4 What this closes and what it does not

**OBS** The premise is corrected: the desktop offers the choice in two surfaces,
since at least 2026-10-03 on this host, and shows which state is in force.

**UNK** The operator's preference. No source can answer it, and this round does not
pretend otherwise.

### Section 5 Divergence from the package text

The package's round-15 text dated the oldest dated copy 2026-10-06. This round's own
sweep of the same four copies dates the oldest 2026-10-03, and the count of copies
carrying the handler (4) agrees. The lane's measured figure is the one recorded here.
