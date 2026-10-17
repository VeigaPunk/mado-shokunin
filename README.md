# mado-shokunin

Desktop and compositor craft — Hyprland, waybar, walker, and the terminals
on this host — measured, never mutated.

Mado reads the declared config plane and, where a read verb exists, the
live compositor. It recommends. The operator applies. A missing bar, a
dead idle daemon, or a theme pin that drifted is a finding with a
severity. It is not a license to rewrite `hyprland.conf`.

Rank: **shonen**. `SHONEN.md` is still here. The fleet `MANIFEST.json`
minted this lane on 2026-10-14 and withheld the roster row.

## Province

**Owns, read-only.** `~/.config/hypr/` (hyprland, keybinds, rules,
animations), `~/.config/waybar/`, `~/.config/walker/`, the terminal configs
for alacritty, foot, kitty, and ghostty, themes and wallpapers as declared
files, and screen/idle behavior where hypridle or hyprlock is present. The
omarchy skill under `~/.agents/skills/omarchy/` is documentation, also
read-only.

**Hands off.** Secrets in configs — shape only, and kagi's custody. Model
endpoints (kama). Model quality (kengaku). Any write to a running
compositor. Every claim is file-byte or screenshot verified.

## Start here

1. `PROVINCE.md` — the plane and the read-only rule.
2. `corpus/README.md` — which note covers which surface.
3. `SKILL.md` — who owns a setting, which probes are safe, which commands
   are operator-only.
4. `tools/mado-verify.sh` — the verdict gate.
5. `SCORECARD.md` — the move log is the trajectory. The early numeric
   cells are the rounds that measured them.

## Run the gate

```sh
bash tools/mado-verify.sh --selftest
bash tools/mado-verify.sh --no-live
bash tools/mado-verify.sh
```

The header is the contract. `MADO_VERIFY: CLEAN` exits 0. `DIVERGED`
exits 1. Usage and a failing selftest exit 2. `--selftest` is hermetic
and reads no substrate. `--no-live` checks the file plane only and names
that scope in the verdict. A live run uses hyprctl read verbs only
(`version`, `instances`, `configerrors`, `getoption`, `binds`, `monitors`,
`layers`). A plane that cannot be verified is `UNKNOWN` and blocks
`CLEAN`. Notes stay visible and do not flip the verdict.

Session material stays shape-only: no window titles, no full instance
signature.

## The tree

| Path | What it is |
|---|---|
| `tools/mado-verify.sh` | Declared planes versus live bytes and hyprctl reads |
| `corpus/knowledge/` | Per-surface notes, errata appended in place |
| `corpus/lessons/` | Per-round lessons |
| `reports/` | Verifier packs |
| `MINT.md` | Why the lane was minted |

## Fleet

Minted under [shokunin](https://github.com/VeigaPunk/shokunin).
Detection and recommendation only.
