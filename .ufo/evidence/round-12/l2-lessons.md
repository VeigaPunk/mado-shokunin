# L2 seat R12Lessons-3 — final output (verbatim, 2026-10-19)

Implemented only the assigned files.

- `corpus/lessons/round-12.md` — 52 lines; SHA-256 `53897738e8da4611…`. Records M1–M14, the seven external inference traps, dispositions, and the requested Gate line.
- `corpus/QUALITY.md` — 24 lines; SHA-256 `c093ab4d301d94f8…`. Appends criteria 6–16, each with a lesson citation, plus the SOURCES registry note.

Retained measurements:
- 52 matches / 17 files — `git grep -c 'a5171' HEAD -- '*.md' | awk -F: '{s+=$NF;n++} END{print s,n}'` — 2026-10-19; matches the dossier.
- 79 `/tmp` paths, 51 top directories, 0 existing — the pointer sweep commands recorded in the lesson — 2026-10-19.
- Hyprland 0.56.2 — `hyprctl version`; help sweep found `getprop` at line 51 and `workspacerules` at line 58 — 2026-10-19.
- M7 remeasures: 315 lines, 7 S3 headers, 119 bytes, and 2,887 gate lines — commands recorded in the lesson — 2026-10-19.
- The committed and worktree AUD-M9 hashes both resolved to `866272e…`; `ten-round-synthesis.md` was absent at HEAD while `arc-synthesis.md` existed.

Risks and routing: `getprop` behavior and rule attribution remain unverified; upstream documentation does not establish host behavior. M12 and M14 are fleet-level and routed to the integrator. M4 and M10 remain process rules, not admission criteria.

No builds, tests, linters, or formatters were run. Parent-owned checks: the requested QUALITY lesson-citation count, `git diff --numstat corpus/QUALITY.md`, and lesson-pointer resolution.
