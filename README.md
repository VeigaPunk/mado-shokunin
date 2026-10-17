# mado-shokunin

Desktop and compositor craft on this host: the Hyprland, waybar, and
walker configuration plane, terminal emulator configs, and display
behavior.

Rank: **shonen**. [`SHONEN.md`](SHONEN.md) marks its boxes `[~]` from
historical assertions. Outside-lane verification is still owed, and the
checklist says so.

Fleet: [shokunin](https://github.com/VeigaPunk/shokunin).

## The question

> Does the declared config plane match the bytes on disk, and, where a
> live read is allowed, the compositor's own report?

The lane probes, measures, and recommends. The operator applies changes.
Config trees are read-only here. A claim is file-byte verified or
screenshot verified. Secrets and session material (window titles, log
lines, instance signatures) are shape-only.

Version pins live in `SKILL.md` (Hyprland, waybar, walker, and the two
different omarchy pins). Re-verify them before reusing a claim under a
newer release. Window-rule syntax in particular moves between versions.

## Boundary

**Owns:** `~/.config/hypr/`, `~/.config/waybar/`, `~/.config/walker/`,
terminal configs (`alacritty`, `foot`, `kitty`, `ghostty`), declared
themes and wallpapers, and screen or idle behavior where hypridle or
hyprlock is present. The omarchy skill tree is a documentation surface,
read-only.

**Hands off:** secrets (kagi), model endpoints (kama), model quality
(kengaku). The lane never mutates a running compositor.

## Run

```sh
bash tools/mado-verify.sh --selftest
bash tools/mado-verify.sh --no-live
```

`mado-verify.sh` checks the declared planes (hypr core, waybar, walker,
terminals). Verdict line `MADO_VERIFY: CLEAN` or `DIVERGED`. Exit `0`
clean, `1` diverged or unverifiable, `2` usage or a failing selftest.
`--selftest` is hermetic and reads no substrate. `--no-live` is the file
plane only. A bare run reads `$HOME` and may call `hyprctl` read verbs.
The script header lists those verbs; it does not write a file.

## Map

| Path | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | operating manual, config-plane map, safe-probe discipline |
| [`PROVINCE.md`](PROVINCE.md) | surfaces and the read-only rule |
| [`corpus/knowledge/`](corpus/knowledge/) | measured notes (binds, window rules, health reports) |
| [`corpus/README.md`](corpus/README.md) | coverage index |
| [`reports/`](reports/) | verifier reports |
| [`LOG.md`](LOG.md), [`SCORECARD.md`](SCORECARD.md) | rounds and axis verdicts |

Tags in the skill: `[OBS]` measured, `[INF]` inferred from measurements,
`[INF-docs]` inferred from documentation, `[UNK]` unknown. Keep them
separate.
