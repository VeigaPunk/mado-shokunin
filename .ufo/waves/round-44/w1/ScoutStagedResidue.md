# ScoutStagedResidue — report (round 44, w1) — status: DONE

Full survey: `.ufo/waves/round-44/w1/ScoutStagedResidue/survey.md` (per-file table, r12 refutations with computed locators, quote candidates verified unique across the 5 pins, counter constraints).

## Findings

1. **Admit `gkeep-client-size-request-r12.md` (as `hyprland-gkeep-size-request-r44.md`) only as a rewrite.** Its S311 ≡ held S164 (same sha d735d454; staged tag URL vs the commit URL), S312 ≡ new row S301
   (gkeep-ui.py). Window.cpp:1732-1754 and gkeep-ui.py:449,474-476 re-ground its two observations. No overlap with `hyprland-gkeep-geometry-r43.md` (base `git grep` = 0 hits).
2. **r12 claims the pins refute / do not support:**
   - "`xdg_toplevel.set_size`" — no such request; `set_size` is `xdg_positioner` (xdg-shell.xml:157). The wire message is the `xdg_toplevel.configure` *event* (xdg-shell.xml:1144-1171, "a hint", :1150) emitted by
     `CXDGToplevelResource::setSize`→`sendConfigure` (XDGShell.cpp:354-357, :455, :629-642).
   - "the acknowledgement is how a client could report a different size" — `ack_configure` carries only a serial (xdg-shell.xml:575-593); `onAck` writes the compositor's stored size (Window.cpp:1514-1528, :1526).
   - "a GTK4 window with no minimum-size request will adopt the compositor's size" — GDK adopts the configured size only after clamping by geometry hints (gdktoplevel-wayland.c:513-531, :525); window minimum comes from the
     unpinned widget layer; 0×0 = client decides (:647-653).
   - "client minimum excluded by its own source" — the compositor clamps a floating xdg window to the client's `set_min_size/set_max_size` on every commit (Window.cpp:2742-2746; XDGShell.cpp:244-246, :467-473;
     GTK sends them at gdktoplevel-wayland.c:1333-1334). Open UNK, not excluded. Same path contradicts r13's "client cannot substitute / compositor's value throughout".
3. **Refuse (with flips):** r13 (private S320 journal receipt; onAck absorbed), r14 (private S326; journal is tsukuroi-adjacent), r15 (private S339; superseded by r43's isolated-oracle observation), r9 (fetchClass is
   off C2's theme; S286/S287 unpinned, S292/S293 private), r31 (glyph off-theme; "deterministic across window managers" unsourced). **Withhold r30** (flip fired, no lane row for `apps/system.conf`, duplicates r43 §1).
   r8/r10/obs-r11 stay as refused in r43; r11-size untouchable. Note: the r10 refusal's flip has NOT fired against the new pins (INF).
4. **Counter constraints to respect:** all five pins cited (S164 + S298-S301), every claim line carries id + Gate quote + computed locator, comment text is stripped (`// apply pending size…` unusable), census lines
   `gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep` and `hyprland sendWindowSize xdg_setSize=1 x11_configure=1` match my own read of the pins; S164's locator cell does not list
   the lines the entry quotes (cells are frozen — the entry's computed locators carry it).
5. **Staged-id hazard:** staged S311/S312/S318-S320/S326/S339 are not lane ids; never write them in the entry. 42 staged ids collide S203..S297 (id-guard) — S216, S219, S284-S287, S292, S293 are in `collisions`.

## Not done / unverified
- Counter not run; BAD_LOC marker list not run against rows; quote candidates were uniqueness-checked by a normalizing script (not the counter's comment-stripping/word-boundary code).
- No live host reads, no journal read.

## Tools / state
Read-only bash/python stdlib/git grep. No installs, no scratch directory created, no lane/git mutation.
