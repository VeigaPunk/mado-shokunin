# mado-shokunin — Scorecard

Lane axes per AXES.md (six-axis vocabulary; primary verdicts per
LEARNING.md trends). Probation rounds 1-3 build the initial measurements.
Axes will be pinned with their counting commands as rounds land.

## Move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 1 | coverage | seed at `74d3b7b`: `corpus/knowledge/` did not exist (0 files), coverage map 0 rows, SKILL.md cited 0 sources | 3 notes — `hyprland-config-plane.md` (217 L), `terminals-and-omarchy.md` (179 L), `waybar-walker-plane.md` (364 L), all `wc -l` — covering every PROVINCE-declared surface group: hypr plane incl. the separate consumers (hypridle/hyprlock/hyprsunset/xdph), waybar/walker/mako/swayosd, all four terminals + theme plane + omarchy skill anatomy; per-surface sweep: 12/12 PROVINCE keywords hit ≥1 note | `git ls-tree 74d3b7b corpus/knowledge/ \| wc -l` → 0; `git show 74d3b7b:corpus/README.md \| grep -cE '^\| '` → 1 (header row only); `wc -l corpus/knowledge/*.md` → 217 / 179 / 364; sweep `grep -il <kw> corpus/knowledge/*.md` for config/hypr, waybar, walker, alacritty, foot, kitty, ghostty, theme, wallpaper, hypridle, hyprlock, hyprsunset → each ≥1 note. Re-run 2026-10-14 (MADO-SCRIBE) |
| 1 | operability | seed SKILL.md: 22 L, 0 tables, 0 commands, 0 probes ("sections will land" placeholder) | SKILL.md 186 L: who-owns-it table 19 rows, read-only probe table 15 rows (each a command + observed sample; caption: executed 2026-10-14), omarchy-boundary routing table 5 rows, 6 mutating commands fenced operator-only; probe tools exist: 10/10 spot-checked names resolve on PATH. Named ceiling: 0 committed verdict gates — `find corpus -name '*.sh'` → 0, no `corpus/scripts/`; probes are prose + sample output, not re-runnable verdicts (round-2/3 work) | `git show 74d3b7b:SKILL.md \| wc -l` → 22; same `\| grep -cE '^\| '` → 0; `wc -l SKILL.md` → 186; per-section awk counts of `^\|` lines → 21/17/7 table lines = 19/15/5 data rows (minus header+separator); `command -v hyprctl omarchy makoctl busctl grim slurp hyprpicker systemctl pgrep jq` → 10/10 found. Re-run 2026-10-14 (MADO-SCRIBE) |
