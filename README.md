# mado-shokunin — desktop and compositor craft

The question this lane answers is what the Hyprland, waybar, walker, and terminal configuration on this host actually does, measured from files and read-only probes (`PROVINCE.md`).

**Rank:** `SHONEN.md` boxes are `[~]`, each marked as a historical assertion. The notes say outside-lane verifier independence is not established. That is not a promotion. `MINT.md` records the mint against the omarchy skill and `omarchy-usage-tray`, with the roster scan rejecting kagi, kama, kumitate, and kake.

## Owns / refuses

Owns, as read-only surfaces: `~/.config/hypr/`, `~/.config/waybar/`, `~/.config/walker/`, terminal configs for alacritty, foot, kitty, and ghostty, declared theme and wallpaper files, and screen and idle behavior where hypridle or hyprlock is present. The omarchy skill is documentation, read-only. The lane probes, measures, and recommends. The operator applies changes (`PROVINCE.md`).

Refuses secrets in configs (shape-only, to kagi), model endpoints (kama), and model quality (kengaku). It does not mutate a running compositor. Every claim is file-byte or screenshot verified (`PROVINCE.md`).

## Start here

Prefer the hermetic self-test. `tools/mado-verify.sh` says a live run reads `$HOME` and, where available, hyprctl. `--selftest` uses fixtures and does not read the substrate.

```sh
bash tools/mado-verify.sh --selftest
```

The header's verdict line is `MADO_VERIFY: CLEAN` or `MADO_VERIFY: DIVERGED`. Exit `0` is CLEAN, `1` is DIVERGED, `2` is a tool or usage error. `--no-live` is the file plane only. A plane that cannot be verified reads UNKNOWN and blocks CLEAN (`tools/mado-verify.sh` header). Do not run a mutating hyprctl verb. The read-verb whitelist is in `corpus/knowledge/hyprctl-verification-layer.md`, indexed from `corpus/README.md`.

## How to read the corpus

`corpus/README.md` says it is a navigation map of admitted evidence, not a current desktop-health verdict. It is line-cited (`corpus/README.md:54` in the fleet-round-1 navigation smoke), so it was not reflowed. Follow a note's recheck before reusing a live value. `corpus/QUALITY.md` is the admission bar. `corpus/knowledge/` holds the plane notes. `corpus/lessons/` holds round lessons.

## Map

| Path | What it is |
|---|---|
| `PROVINCE.md` | Read-only surfaces and refusals |
| `SKILL.md` | Safe-probe discipline and checklists |
| `SHONEN.md` | Checklist, historical `[~]` |
| `MINT.md` | Mint cause |
| `LOG.md` | Append-only record |
| `SCORECARD.md` | Axis verdicts |
| `AGENTS.md` | Operating rules |
| `corpus/` | Knowledge, lessons, quality bar, index |
| `tools/mado-verify.sh` | Config-plane verdict gate |
| `plans/` | Round plans |
| `reports/` | Round reports |
| `.ufo/` | Round machinery |

## Neighbors

kagi (secret-shaped config), kama (endpoints), kengaku (model quality), tsukuroi (OS unit and driver health underneath a desktop symptom; see `tsukuroi-shokunin/PROVINCE.md` ADJ-03). Out of province is reported, not absorbed.

Fleet protocol: [VeigaPunk/shokunin](https://github.com/VeigaPunk/shokunin).
