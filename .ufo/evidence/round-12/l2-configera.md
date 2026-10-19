# L2 seat R12ConfigEra-3 — final output (verbatim, 2026-10-19)

**Files written**
- `corpus/knowledge/hyprland-config-era-r12.md` — 123 lines — SHA-256 `8924143d7887862f`
- `.ufo/evidence/round-12/configera-host.txt` — 103 lines — SHA-256 `cc9cdd1854d84a0b`
- `.ufo/round-12/sources/config-era.md` — 32 lines — SHA-256 `85e10699c0b683b5`

**Behavior and evidence**
- The U2 entry documents Lua’s 0.55 transition, the exact hyprlang support-window quote, startup default-file selection, and documented window-rule changes from 0.53 through 0.56.2. Upstream claims are tagged `[INF-docs]`; host readings are kept separate as `[OBS]`.
- Host reads: `hyprctl version` reported Hyprland 0.56.2 at `efb5099…`; `hyprctl configerrors` returned empty output, exit 0; the `~/.config/hypr/*.lua` sweep found no matches; `hyprland.conf` exists; the safe `hyprctl systeminfo` projection reported `configProvider: hyprlang`.
- The exact active config path remains `[UNK]`: the safe reads did not expose it, and an explicit `--config` path cannot be ruled out. No host rule behavior was tested.
- Durable source Gate quotes are in the source fragment; command outputs and projections are in `configera-host.txt`.

**Risks / blockers:** Release summaries are not a complete parser-change history; the exact final hyprlang-supported release and active config pathname remain unknown. No blockers. No builds, tests, or linters were run.
