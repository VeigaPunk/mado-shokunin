# mado-shokunin — 窓

**Desktop and compositor craft** — the Hyprland / waybar / walker
configuration plane and display behavior on this host.

Mado probes, measures, and recommends. The operator applies changes.
A fresh agent holding only [`SKILL.md`](SKILL.md) should be able to run
a **scoped config verification** end-to-end: pick a claim or a plane,
route it to its evidence class, stay inside the safety fence, classify
divergence, and report with measured anchors.

This is a **shokunin lane** of the [shokunin fleet](https://github.com/VeigaPunk/shokunin).
Rank: **shonen** (probation; roster row withheld).

## The craft

- Keybind and window-rule semantics, reconciled against live
  `hyprctl binds -j` where the host still offers it
  (`corpus/knowledge/keybind-rule-semantics.md`).
- Waybar / walker / terminal-emulator configs as declared files.
- Screen / idle behavior (hypridle / hyprlock where present).
- The omarchy skill is a **documentation** surface, read-only.

Tag legend (load-bearing): `[OBS]` measured · `[INF]` composite
inference · `[INF-docs]` documentation, not host-verified · `[UNK]`
unknown. A claim with only one anchored side is an UNK item, not a
finding.

Version pins in `SKILL.md` (re-verify before reuse): Hyprland 0.56.2,
waybar v0.15.0, walker 2.17.0. Omarchy carries two pins — `omarchy
version` vs checkout `git describe --tags`. Window-rule syntax changes
between releases.

## Province

Owns: `~/.config/hypr/`, `~/.config/waybar/`, `~/.config/walker/`,
terminal emulator configs, declared themes/wallpapers, idle/lock files.
**All config trees are read-only for this lane.**

**Refuses:** secrets in configs (shape-only → kagi), model endpoints
(→ kama), model quality (→ kengaku). Never mutates a running compositor.
Every claim is file-byte- or screenshot-verified.

See [`PROVINCE.md`](PROVINCE.md).

## What's in this repository

```
mado-shokunin/
├── SKILL.md            operating manual for scoped config verification
├── PROVINCE.md
├── SHONEN.md
├── LOG.md
├── SCORECARD.md
├── MINT.md
├── AGENTS.md
├── tools/
│   └── mado-verify.sh  lane gate
├── reports/
├── plans/
└── corpus/
    ├── knowledge/      keybind/rule semantics, walker-deep, sufficiency tests
    └── lessons/
```

## Start here

```sh
bash tools/mado-verify.sh
```

Then read [`SKILL.md`](SKILL.md) standing rules before opening a live
compositor socket. Session material (window titles, `hyprland.log`,
instance signatures) is shape-only.

## How a round works

One axis-move. Lane identity: `mado-shokunin <mado@shokunin.local>`.
Commits carry that identity (`AGENTS.md`).

## Fleet

[VeigaPunk/shokunin](https://github.com/VeigaPunk/shokunin) ·
[tsukuroi-shokunin](https://github.com/VeigaPunk/tsukuroi-shokunin)
(OS / driver health is adjacent, not owned) ·
[kimi-shokunin](https://github.com/VeigaPunk/kimi-shokunin)
