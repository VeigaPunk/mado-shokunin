#!/usr/bin/env python3
"""Round-41 post-w2 repairs to the landed data (entry, README row, S283/S286 rows, tool docstring)."""
import re
L = "/home/vgpnk/Projects/shokunin/mado-shokunin/"

def edit(path, pairs):
    s = open(L + path).read()
    for old, new in pairs:
        assert old in s, (path, old[:70])
        s = s.replace(old, new, 1)
    open(L + path, "w").write(s)

E = "corpus/knowledge/hyprland-focus-grab-r41.md"
edit(E, [
 ("binds ten of them", "has ten named bind branches"),
 ("a *limiter over the client's own surfaces*, not a way to focus anyone else's", "a *limiter over a set of surfaces the client names*, not a way to focus anyone else's"),
 ("the client controls only membership. `Basis:` S283's interface description and the `commit` request text.",
  "no request names a focus target: the client controls the set, the commit timing and the grab's lifetime. `Basis:` S283's interface description and the `commit` request text."),
 ("makes the grab finish *itself*, with the `cleared` event, when the seat grab is cancelled.",
  "registers a callback that finishes the grab *itself*, with the `cleared` event; what triggers that callback lives in `CSeatGrab`, which the receipt only forward-declares."),
 ('"if (anyCommitted) start(); else finish(true);" - each surface carries a three-valued state (`PendingAddition`, `PendingRemoval`, `Committed`); a commit promotes additions into the seat grab and erases removals, and only a change of the set triggers start or finish.',
  '"if (surfacesChanged) { if (anyCommitted) start(); else finish(true); }" - each surface carries a three-valued state (`PendingAddition`, `PendingRemoval`, `Committed`); a normal commit promotes additions into the seat grab and erases removals (the destroy-path `commit(true)` only erases removals), and only a change of the set triggers start or finish.'),
 ("- the compositor treats \"grab active, nothing committed\" as a bug rather than a state.", "- the function logs an error and returns; no clear and no client error follows."),
 ("so a failed allocation is a protocol error, not a silent no-op.", "so a resource that is not `good()` is answered with `noMemory()` and dropped from the list."),
 ("**INF** The whitelist is enforced at the seat, not at the rule layer: nothing in this file consults a window or workspace rule, and the object's effect is the `CSeatGrab` it installs and removes.",
  "**INF** The whitelist is installed as the seat's grab: nothing in this file consults a window or workspace rule, and the object's effect is the `CSeatGrab` it installs and removes; how that grab filters events is unread (UNK below)."),
 ("and closes at \"Stopped Portal service (Hyprland implementation).\", and pid 1952", "and closes at \"Stopped Portal service (Hyprland implementation).\" - it belongs to the previous boot, which ended at 13:35:34 (`journalctl --list-boots`, read-only) - and pid 1952"),
 ("**INF** Only the second session is a whole advertisement: the first is a journal slice that begins after that portal was already running, so its 15 adverts are a lower bound. The census line above therefore reports the latest session - 63 distinct names, no name advertised twice - which is the only session that can be compared with the compositor's registry as a whole.",
  "**INF** The first session is a slice of the previous boot's portal (the `-- Boot` marker lies between the sessions): its 15 adverts over 8 names are a fragment and say nothing about the current registry. The census line above reports the latest session - 63 distinct names, none advertised twice - but 63 is what the log retained, not proof of the compositor's complete registry: that session holds no `wl_output` and no `zwp_linux_dmabuf_v1` advert, which the previous boot's slice shows the same portal logged and its handler binds, and the lane's round-13 wayland-info capture (a held row, 71 names) holds both. `Basis:` the journal's own lines 8-9 and the session structure."),
 ("and what follows is a fixed set of ten named branches -", "and what follows is a fixed set of ten named branches (nine direct `wl_registry_bind` calls and the foreign-toplevel branch, which hands name and version to `CToplevelManager`) -"),
 ("so the `v1.4.1` pin of the portal source row and the running unit are the same upstream release.", "so the installed package is upstream v1.4.1 at pkgrel 2; that the running binary is that package's file and that the packaging left the source untouched are not established by this receipt."),
 ("and the portal's own bind list excludes the manager.", "and the portal source's own bind branches exclude the manager."),
 ("adding a window records it and *defers* the protocol call; `sync()` is the only place that commits.",
  "adding a window sends `add_surface` at once (`grab.cpp:66`) and then records it for the commit; `sync()` is the only place that commits."),
 ('the expectation is "If a workspace windowrule contains silent then matching windows should not get focus"',
  'the expectation is "If a workspace windowrule contains `silent` then matching windows should not get focus, unless that window\'s workspace is already the active one."'),
 ("**INF** The lane holds no focus-rule knowledge either. `grep -rli 'focus_grab\\|focus-grab\\|focus grab' corpus PROVINCE.md SKILL.md tools` exits 1 at base; `window-rule-effects-getprop.md` and `workspace-rules-r27.md` contain no `focus` line, and `rule-attribution-r24.md`'s only hit is a block rule named `jetbrains-focus`.",
  "**INF** The three held rule entries named here hold no focus-rule semantics: `grep -rli 'focus_grab\\|focus-grab\\|focus grab' corpus PROVINCE.md SKILL.md tools` exits 1 at base; `window-rule-effects-getprop.md` and `workspace-rules-r27.md` contain no `focus` line, and `rule-attribution-r24.md`'s only hit is a block rule named `jetbrains-focus`; other held rule entries were not scanned."),
 ("shows why a client cannot get a grab through rules: the rule's subject is a window, the grab's subject is a set of surfaces.", "shows the rule layer deciding focus over a window; no receipt shows a rule granting a grab, and the rule's subject is a window while the grab's subject is a set of surfaces."),
 ("| What can a client ask for? | S283: two interfaces, five requests, one event (§1) | OBS |", "| What can a client ask for? | S283: two interfaces, six requests (two on the manager, four on the grab), one event (§1) | OBS |"),
 ("| Does the portal use it? | S286 and S289: logged, not bound, no other line (§3) | OBS |", "| Does `PortalManager.cpp` bind it? | S286 and S289: logged, no branch for it, no other line (§3) | OBS |"),
 ("| What must a client do between `add_surface` and `commit`? | S285: batch in `pendingAdditions`, then `sync()` commits (§4) | OBS |", "| What does this client do between `add_surface` and `commit`? | S285: record in `pendingAdditions`, then `sync()` commits (§4) | OBS |"),
 ("- The portal's non-use (§3) is a statement about v1.4.1's `PortalManager.cpp` and this journal, not about later releases.", "- The portal's non-binding (§3) is a statement about v1.4.1's `PortalManager.cpp` and this journal, not about later releases or other code paths."),
])
# the keyboard-enter condition (F13) and the S285 UNK answered from the receipts (CritEntryOverreach)
s = open(L + E).read()
s = s.replace("**UNK** Whether one Qt transaction is one frame in practice, and whether a `cleared` arriving between `add_surface` and `commit` is observable to this client. Neither is measured here.",
 "**UNK** Whether one Qt transaction is one frame in practice. A `cleared` arriving between `add_surface` and `commit` is visible in the receipts' code paths (`startTransaction()` suspends `sync()`; the handler sets `active = false` without touching `pendingAdditions`; the compositor's `finish` clears its surface map), so the client's `active` and the compositor's grab can disagree after such a `cleared`; no run observed it.")
open(L + E, "w").write(s)
assert "pendingAdditions`; the compositor" in s

R = "corpus/README.md"
s = open(L + R).read()
i = s.index("| `knowledge/hyprland-focus-grab-r41.md`")
j = s.index("\n", i)
row = s[i:j]
row = row.replace("(two interfaces, five requests, one `cleared` event)", "(two interfaces, six requests, one `cleared` event)")
assert row.endswith("unknown. |"), row[-40:]
row = row + " S283-S289, S037 |"
s = s[:i] + row + s[j:]
open(L + R, "w").write(s)

S = "corpus/SOURCES.md"
edit(S, [
 ("The two interfaces, four requests and one event that define a focus grab", "The two interfaces, six requests and one event that define a focus grab"),
 ("which nine it binds, and whether focus grab is among them", "which ten branches it has (nine direct binds and foreign toplevel), and whether focus grab is among them"),
 ("(screencopy, global_shortcuts, input_capture, xdg_output, toplevel_export, wl_output, linux_dmabuf, shm, toplevel_mapping)", "(screencopy, global_shortcuts, input_capture, xdg_output, toplevel_export, wl_output, linux_dmabuf, shm, foreign_toplevel, toplevel_mapping)"),
])
# search log entry
s = open(L + S).read()
s = s.rstrip("\n") + "\n\nRound 41 (2026-10-25), one note per bounded search, by seat:\n\n- Question: what do the compositor, its portal, one client and the tracker say about the focus-grab protocol, and does this host advertise it? Searched: the pinned raw files S283-S288 (hyprland-protocols cd1aba6, Hyprland efb5099, quickshell 9b0f339, xdph v1.4.1), the GitHub issue S287, the host journal S289 and the installed package record S037. Identified 8 candidate sources, screened 8, included 7 new rows plus 1 held; excluded the staged localized-channel post (outside PROVINCE.md), the staged privileged-client blog post (generic analysis, truncated quote) and `input-capture-v1.xml` (fetched, not cited, no row). Stop rationale: every protocol, compositor, client, portal and host layer of the question has one primary source; a `CSeatGrab` routing source (seat manager) is an open lead, not a row.\n"
open(L + S, "w").write(s)

T = "tools/mado-globals.py"
edit(T, [("Exit: 0 OK, 1 MISSING_EXPECTED, 3 NO_SESSIONS, 4 UNRECOGNIZED_FORMAT, 2 usage/input\n(`MADO_GLOBALS: SETUP <reason>` on stdout), 5 live journal failure.\n",
 "Exit: 0 OK, 1 MISSING_EXPECTED, 3 NO_SESSIONS, 4 UNRECOGNIZED_FORMAT, 2 usage/input\n(`MADO_GLOBALS: SETUP <reason>` on stdout), 5 live journal failure.\n\nUsage\n    mado-globals.py --journal-file PATH [--expect NAME]... [--diff]\n    mado-globals.py --live [--journalctl PROGRAM] [--expect NAME]... [--diff]\n    mado-globals.py --selftest\nThe verdict line describes the LATEST session only; a mixed file can print\nverdict=OK with ignored>0 - read `ignored=`. `--help` is not a flag: it prints\n`SETUP usage`. Capture a file with\n`journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`.\n")])
print("fix1 ok")
