# CritProvince — is upstream Waybar source inside mado's province?

Lane: mado-shokunin. Round 34, wave 1. Scoped finding on the round-34
adoption `corpus/knowledge/waybar-module-text-route-r25.md` (landed `fa7ba11`),
which cites S201 (`Alexays/Waybar@0.15.0` `src/modules/hyprland/backend.cpp`)
and S202 (`window.cpp`).

## Verdict

**IN PROVINCE.** Upstream Waybar source — specifically the Hyprland
backend and the window module — is an in-province read-only authority
surface for this lane, on the same footing the lane already established
for upstream Hyprland compositor source.

## Evidence

1. **The domain line names Waybar.** `PROVINCE.md:3-4`: "desktop &
   compositor craft — the Hyprland/waybar/walker configuration plane and
   display behavior on this host." `~/.config/waybar/` is a listed owned
   surface (`PROVINCE.md:7`). Waybar is named in the domain, not an
   adjacent project.

2. **The compositor-source precedent is this lane's own.** The Hyprland
   C++ source is already in mado's registry, not a sibling's: S189 =
   `hyprwm/Hyprland@efb50993` `src/managers/EventManager.cpp`, tier A,
   "the compositor-side event socket as implemented at the host's own
   version v0.56.2" (`corpus/SOURCES.md:201`). The Hyprland IPC wiki rows
   S186–S188 and S196 sit beside it (`SOURCES.md:198-202`). If the
   producer's event-socket C++ is tier-A authority for the lane's IPC
   knowledge, the consumer's IPC-client C++ is the same class. Rejecting
   S201/S202 while keeping S189 is an asymmetric rule with no basis in
   PROVINCE.md.

3. **"Owns (surfaces)" is not limited to config trees.** The omarchy
   skill is explicitly owned "documentation surface, read-only"
   (`PROVINCE.md:10-11`), and the round-19 refinement absorbed the
   omarchy theme plane's read-only documentation (`PROVINCE.md:18`).
   `CORPUS.md` rule 1 expects rows opened in-round; `SOURCES.md` exists
   to hold external sources. Reading upstream tagged source is a probe,
   not a mutation — no refused act is committed.

4. **The entry is scoped correctly.** The entry's claims are strictly
   what the upstream bytes say (socket-folder fallback `backend.cpp:38`;
   `m_ipc.registerForIPC("activewindow", this)` `window.cpp:27`), and it
   disclaims the host inference: "Whether this host's bar uses the
   Hyprland window module is unverified… Upstream source is not host
   behavior" (entry UNK block). This mirrors S189's version-pinning
   discipline rather than overreaching it.

## The challenge considered

The strongest attack: the owns list enumerates config trees plus one
named documentation surface, and says nothing about upstream source
trees — so Waybar C++ could be "foreign surface" under `mado-shokunin/
AGENTS.md` ("Substrates outside this repo are read-only unless
PROVINCE.md declares otherwise"). That reads "substrates" as writable
trees; the lane never writes any config tree ("All config trees are
READ-ONLY"), so the write/read distinction does not exclude a read-only
authority. The compositor's own C++ (S189) is already absorbed under the
identical reading — upstream source is province evidence, not province
substrate.

## Alternative lanes — none fits better

- **tsukuroi** — owns pacman state and host operability, not bar display
  semantics. `waybar --version` is already a mado probe inside
  `tools/mado-verify.sh` (`PROVINCE.md:32`), so host-version matching is
  also mado's.
- **revenger / kaidoku** — reverse engineering of shipped artifacts;
  upstream tagged source reading is not artifact RE, and neither province
  names waybar or the desktop config plane.
- **chousa** — research method, not a domain surface owner.

## Residual (not a defect, flagged)

S189 is version-matched to the host compositor (v0.56.2); S201/S202 are
pinned to upstream tag 0.15.0 with no stated host-version match. The
entry's UNK block covers this. A future tightening could bind the
cited tag to `waybar --version` output on this host; the adoption does
not require it.
