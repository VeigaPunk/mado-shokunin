### Correction — Round 55 registry census (2026-10-30)

The `## Gate` census paragraph above is stale: its `Rows 314 → 317` and `317 rows` counts predate the addition of registry rows S381 and S382, which entered after this lesson was written. The correct ending registry count is 319 rows. Count command (at the Round 55 post-S381/S382 registry revision): `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 187003d0:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → `319`.
