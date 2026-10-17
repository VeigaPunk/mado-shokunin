# mado-shokunin

Desktop and compositor craft for this host: the Hyprland, waybar, and
walker configuration plane, the terminal configs, and the display
behavior those files produce.

The lane probes, measures, and recommends. Config trees are read-only
for it. The operator applies changes. A claim is file-byte-verified or
screenshot-verified. Secrets in configs are shape-only and belong to
kagi. Model endpoints belong to kama. Model quality belongs to kengaku.
The lane never mutates running compositor state.

## The job

`PROVINCE.md` names the surfaces: `~/.config/hypr/` (hyprland.conf,
keybinds, rules, animations), `~/.config/waybar/`, `~/.config/walker/`,
terminal configs (`alacritty`, `foot`, `kitty`, `ghostty`), declared
theme and wallpaper files, and screen/idle behavior (hypridle and
hyprlock where present). The omarchy skill under `~/.agents/skills/omarchy/`
is a documentation surface, read-only.

`SKILL.md` is the operating manual. A fresh agent holding only that file
is expected to run a scoped config verification: pick a claim, route it
to an evidence class, stay inside the safety fence, classify any
divergence, and report with measured anchors. Tags in the skill keep
observation, inference, and unknown separate (`[OBS]`, `[INF]`,
`[INF-docs]`, `[UNK]`).

## Verify

`tools/mado-verify.sh` checks the declared planes against live bytes and,
where available, live `hyprctl` reads. One verdict line:
`MADO_VERIFY: CLEAN` or `MADO_VERIFY: DIVERGED`. Exit 0 is clean, 1 is
diverged (including a required check that was unverifiable), 2 is usage
or a failing selftest.

```sh
bash tools/mado-verify.sh --selftest
```

`--selftest` is hermetic and reads no substrate. The live run
(`bash tools/mado-verify.sh`) is read-only against `$HOME`. `--no-live`
stays on the file plane. `--root DIR` points the file plane at a fixture.

## Read this first

1. [`PROVINCE.md`](PROVINCE.md) — surfaces and the read-only rule.
2. [`SKILL.md`](SKILL.md) — how to scope a verification.
3. [`corpus/README.md`](corpus/README.md) — the knowledge index.
4. [`tools/mado-verify.sh`](tools/mado-verify.sh) — the verdict gate. The header is the usage contract.

## On disk

| Path | Role |
|---|---|
| `SKILL.md` | Operating manual for a scoped config verification. |
| `PROVINCE.md` | Surfaces, refusals, write boundary. |
| `tools/mado-verify.sh` | Verdict gate. |
| `corpus/` | Knowledge and lessons. |
| `plans/`, `reports/` | Round plans and reports. |
| `MINT.md`, `SHONEN.md` | Mint record and promotion checklist. Rank is shonen. |
| `LOG.md`, `SCORECARD.md` | Audit trail and axis verdicts. |

## Fleet

Protocol and roster: [shokunin](https://github.com/VeigaPunk/shokunin).
This repository is a sibling lane. It is not an object in the fleet
root's `MANIFEST.json` `roster` array (13 ids, ending at `kaidoku`,
read 2026-10-17). Rank **shonen**.
