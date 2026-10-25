# ConnSiblingOverlap — seat report (round 40, w1)

Status: complete. Read-only sibling-lane overlap scan delivered to
`.ufo/waves/round-40/w1/ConnSiblingOverlap.md`.

- Scope: fleet MISSION/AXES, all 21 sibling PROVINCE.md headers (tsukuroi, mori,
  kama, tameshi, kake, souji, kumitate, chousa, kotodama, kasegi, tabi, kagi,
  kengaku, kotoba, kaidoku, revenger, lore, audio, game-dev-2d/3d, mado), and
  targeted greps for `hyprctl|getoption|hyprlang|waybar|active_border|omarchy|
  ai-usage` over each lane's non-wave corpus/tools/SKILL/PROVINCE/SCORECARD.
- Method: read-only file reads and grep; no host/compositor mutation, no socket,
  no subagents, no tools installed (none needed; read-only scan).
- Result: the getoption/option-table surface is mado-exclusive (no sibling claims
  it); sibling touchpoints exist only around the ai-usage/waybar producer *timer*
  and *cache* (tsukuroi timer-drift census; kake ai-usage-cache consumption),
  plus incidental waybar observations (audio PipeWire clients, kaidoku waybar
  coredumps, tabi DOM GetOptionList — unrelated). No ownership conflict; two
  complementary dependencies recorded for the integrator.
- Report file written at the task-named path; nothing else written.
