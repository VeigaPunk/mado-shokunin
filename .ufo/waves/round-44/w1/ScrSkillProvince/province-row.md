# PROVINCE.md append — round 44 C1 (`tools/mado-geometry.py`)

Target: `PROVINCE.md` (97 lines at base `6a1a905`). The `tools/mado-geometry.py` inventory row is
line 32 (read surface: rule-file bytes + one `hyprctl clients -j` dump; writes: nothing, stdout only;
`--selftest` writes nothing). The row is **not** rewritten — the file's convention for a moved tool
fact is an append-only correction paragraph, as with rounds 23, 25, 27, 36 and 38.

Append at end of file, after the last line `:97` (`half).`), separated by one blank line:

```
**Round-44 correction (append-only; C1, closure D3):** the `tools/mado-geometry.py` row above stays
true about surfaces — same two inputs, no socket, no process, stdout only — but the tool now reads one
more field of the same dump. For each mapped client it takes `fullscreen` (Hyprland prints it from
`Fullscreen::controller()->getFullscreenModes(w).internal`, `Hyprland-HyprCtl.cpp:431`; the enum is
0 none / 1 maximized / 2 fullscreen, `Hyprland-FullscreenController.hpp:12-15`), accepts it only as a
JSON integer 1 or 2, and returns FULLSCREEN or MAXIMIZED instead of DIFFER or TILED. Why this is a
province fact and not tooling detail: Hyprland 0.56.2 sets a fullscreen window's box to the monitor's
logical box and a maximized window's to the workspace work area
(`Hyprland-FullscreenHandler.cpp:191-198`), so the round-43 tool's DIFFER for a fullscreen gkeep
window was a false report about the display plane, not an inert mismatch. The verdict order becomes
BADSIZE | FULLSCREEN | MAXIMIZED | TILED | AGREE | DIFFER, and the summary gains
` maximized=<n> fullscreen=<n>` only when those counts are non-zero, so every other line is unchanged.
No new write surface, no operator act, and the tool still never applies a rule: it reads bytes the
caller supplied.
```

Notes for the landing seat:

- Placement is EOF on purpose: `PROVINCE.md` has no subject index, so a correction paragraph at the
  end is the established shape (`## Round-38 addendum`, `:86-97`).
- No SOURCES ids appear in `PROVINCE.md`; the paragraph cites pin paths and line numbers instead, which
  is what the existing correction paragraphs do (e.g. the round-27 correction cites `a496b02a` and the
  tool's docstring).
- The row's ownership cell ("mado, round 43 …") stays as written; this paragraph, not a row edit,
  carries the round-44 state.
