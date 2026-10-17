# mado-shokunin — 窓

**Desktop and compositor craft.** The Hyprland / waybar / walker /
terminal configuration plane, and whether live display behavior matches
the files that claim to produce it.

A **shokunin lane**: an expert agent for one domain, minted and trained
under the [shokunin skill](https://github.com/VeigaPunk/shokunin).
Rank: **shonen**. Promotion is a named non-author review of
[`SHONEN.md`](SHONEN.md), never self-attestation.

This lane answers: *does this host's desktop config still mean what the
corpus says it means — measured from files and `hyprctl` reads, never
by restarting the compositor?*

## Domain

From [`PROVINCE.md`](PROVINCE.md): `~/.config/hypr/`, `~/.config/waybar/`,
`~/.config/walker/`, terminal emulator configs, themes/wallpapers as
declared files, screen/idle behavior (hypridle/hyprlock where present).
The omarchy skill is documentation surface, read-only.

**All config trees are read-only for this lane.** Probe, measure,
recommend. The operator applies changes. This lane never mutates a
running compositor.

Version pins in [`SKILL.md`](SKILL.md) (re-verify before reuse):
Hyprland 0.56.2, waybar v0.15.0, walker 2.17.0. Window-rule syntax
changes between releases.

**Refuses:** secrets in configs (shape-only →
[kagi](https://github.com/VeigaPunk/kagi-shokunin)); model endpoints
(→ [kama](https://github.com/VeigaPunk/kama-shokunin)); model quality
(→ [kengaku](https://github.com/VeigaPunk/kengaku-shokunin)). Session
material (window titles, `hyprland.log`, instance signatures) is
shape-only too.

Observation / inference / unknown stay separate. Tag legend in
`SKILL.md`: `[OBS]` `[INF]` `[INF-docs]` `[UNK]`.

## What's here

| Path | Role |
|---|---|
| [`SKILL.md`](SKILL.md) | operating manual: a fresh agent can run a scoped config verification end-to-end |
| [`PROVINCE.md`](PROVINCE.md) | owned surfaces and the write fence |
| [`tools/mado-verify.sh`](tools/mado-verify.sh) | declared-plane verdict gate |
| [`corpus/`](corpus/) | knowledge and lessons (keybind/rule semantics, live vs file) |
| [`SCORECARD.md`](SCORECARD.md) · [`LOG.md`](LOG.md) · [`SHONEN.md`](SHONEN.md) | axes, trail, promotion |

## The gate

```sh
bash tools/mado-verify.sh --help
bash tools/mado-verify.sh --selftest      # hermetic fixtures, no substrate
bash tools/mado-verify.sh --no-live       # file plane only
bash tools/mado-verify.sh                 # live read-only against $HOME
```

Verdict: `MADO_VERIFY: CLEAN|DIVERGED`. Exit `0` / `1` (usage error:
`2`). A plane that cannot be verified reads UNKNOWN and **blocks CLEAN**
— never a fake pass. Live verbs are `hyprctl` reads only.

## How a lane learns

Append-only corpus; every claim separates observation / inference /
unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).
