# mado-shokunin

**Desktop and compositor craft — probe, measure, recommend. The operator
applies the change.**

A **shokunin lane** minted and trained under the
[shokunin](https://github.com/VeigaPunk/shokunin) skill. Mado owns the
Hyprland / waybar / walker configuration plane and display behavior on
this host.

**Wiki:** [lane overview](https://app.devin.ai/org/veigapunk/wiki/VeigaPunk/mado-shokunin?branch=master)

## Domain

From `PROVINCE.md` and `SKILL.md` (read-only config trees):

- `~/.config/hypr/` — hyprland.conf, keybinds, rules, animations
- `~/.config/waybar/`, `~/.config/walker/`
- terminal emulator configs (`alacritty` / `foot` / `kitty` / `ghostty`)
- themes / wallpapers as declared files
- screen / idle behavior (hypridle / hyprlock where present)
- the omarchy skill as a documentation surface

Every claim is file-byte- or screenshot-verified. The lane never mutates
a running compositor. Version pins in `SKILL.md` (Hyprland 0.56.2,
waybar v0.15.0, walker 2.17.0, omarchy 3.8.3 / checkout v3.8.4) must be
re-verified before reuse — window-rule syntax in particular changes
between releases.

Tag legend used throughout the skill: `[OBS]` measured · `[INF]`
composite inference · `[INF-docs]` documentation inference · `[UNK]`
unknown.

## What it refuses

Secrets in configs (shape-only) → [kagi](https://github.com/VeigaPunk/kagi-shokunin).
Model endpoints → [kama](https://github.com/VeigaPunk/kama-shokunin).
Model quality → [kengaku](https://github.com/VeigaPunk/kengaku-shokunin).
Package / driver / unit health that is not a config question →
[tsukuroi](https://github.com/VeigaPunk/tsukuroi-shokunin).

## In this repository

```
PROVINCE.md     owned surfaces + read-only fence
SKILL.md        scoped-verification manual
SHONEN.md  SCORECARD.md  LOG.md  MINT.md
corpus/         knowledge/, lessons/, QUALITY.md
reports/
tools/
  mado-verify.sh
```

## Verify

```bash
bash tools/mado-verify.sh
```

The tool measures declared config against live compositor state. It does
not apply a bind, a rule, or a theme.

## How a lane learns

Append-only corpus; every claim separates observation / inference /
unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).
