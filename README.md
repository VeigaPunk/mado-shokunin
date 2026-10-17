# mado-shokunin — desktop & compositor craft

**Probe, measure, recommend. The operator applies the change.**
A fresh agent holding only `SKILL.md` should be able to run a scoped
config verification end-to-end: pick a claim or a plane, route it to
its evidence class, stay inside the safety fence, classify any
divergence, and report with measured anchors.

This is a [shokunin](https://github.com/VeigaPunk/shokunin) lane for the
Hyprland / waybar / walker configuration plane and display behavior on
this host. Rank: shonen.

All config trees are **read-only**. This lane never mutates a running
compositor. Every claim is file-byte- or screenshot-verified.
Observation / inference / unknown stay separate: `[OBS]`, `[INF]`,
`[INF-docs]`, `[UNK]`.

## Province

**Owns:** `~/.config/hypr/` (hyprland.conf, keybinds, rules,
animations); `~/.config/waybar/`; `~/.config/walker/`; terminal emulator
configs (`~/.config/alacritty|foot|kitty|ghostty/`); themes / wallpapers
as declared files; screen / idle behavior (hypridle / hyprlock where
present). The omarchy skill is a documentation surface, read-only.

**Refuses:** secrets in configs (shape-only, → kagi); model endpoints
(→ kama); model quality (→ kengaku). Docs-inference (`[INF-docs]`) is
never asserted as host state — the wiki can be a different era than the
installed compositor (recorded: wiki lua-era vs host Hyprland 0.56.2).

Version pins in `SKILL.md`: Hyprland 0.56.2 (commit `efb5099…`), waybar
v0.15.0. Re-read those pins before reusing a citation. Full boundary:
[`PROVINCE.md`](PROVINCE.md).

## Start here

1. [`SKILL.md`](SKILL.md) — evidence-class table, safe-probe discipline, checklists.
2. [`PROVINCE.md`](PROVINCE.md) — owned surfaces and the never-mutate rule.
3. [`tools/mado-verify.sh`](tools/mado-verify.sh) — the config-plane verdict gate.

## The verify gate

```
bash tools/mado-verify.sh              # live run against $HOME (read-only)
bash tools/mado-verify.sh --no-live    # file plane only
bash tools/mado-verify.sh --selftest   # hermetic fixtures, no substrate reads
```

Verdict line: `MADO_VERIFY: CLEAN` or `MADO_VERIFY: DIVERGED`. Exit `0`
CLEAN · `1` DIVERGED (a check failed, or a required check was
UNVERIFIABLE) · `2` tool / usage error. Live hyprctl verbs are read-only
(`version`, `instances`, `configerrors`, `getoption`, `binds`,
`monitors`, `layers`). A plane that cannot be verified reads UNKNOWN
and blocks CLEAN.

## What's in the repo

```
mado-shokunin/
├── SKILL.md          operating manual (sufficient alone)
├── PROVINCE.md       domain boundary
├── SHONEN.md         promotion checklist
├── MINT.md           why this lane was minted
├── LOG.md            append-only audit trail
├── SCORECARD.md      axis verdicts
├── AGENTS.md         operating rules
├── tools/            mado-verify.sh
├── plans/            round plans
├── reports/          verifier / adjudicator reports
└── corpus/           knowledge/, lessons/, QUALITY.md
```

Protocol: append-only corpus; secrets are shape-only; rounds are
non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme) for how a lane
learns.
