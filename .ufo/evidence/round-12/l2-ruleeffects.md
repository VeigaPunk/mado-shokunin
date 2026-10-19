# L2 seat R12RuleEffects-3 — final output (verbatim, 2026-10-19)

Implemented **MADO-R12-1 (U1)**. `hyprctl getprop` is an effect-value read on this host, **not** a matched-rule attribution interface. The selected Alacritty window returned `opacity=0.97`, `opacity_inactive=0.9`, `opacity_fullscreen=1`, and `opacity_override=false`; global active/inactive opacity options were `1.000000` with `set: false`. The entry corrects the two prior negative claims without editing those notes.

- `corpus/knowledge/window-rule-effects-getprop.md` — 154 lines — SHA-256 prefix `f1d7b1d2f27b`
- `.ufo/evidence/round-12/getprop-help.txt` — 107 lines — SHA-256 prefix `64a10736b19a`
- `.ufo/evidence/round-12/getprop-measure.txt` — 113 lines — SHA-256 prefix `9e77fc42c670`
- `.ufo/round-12/sources/getprop.md` — 22 lines — SHA-256 prefix `9365bf17b321`

Evidence retains the v0.56.2 help/version output, title-free client projection, property/default/workspace-rule reads, and usage/error outputs. Risk: opacity values are shared by host rule declarations, so the matching rule remains unknown; current wiki documentation is latest-git Lua-era context, not host-version proof. No blocker. Builds, tests, linters, and formatters were not run.
