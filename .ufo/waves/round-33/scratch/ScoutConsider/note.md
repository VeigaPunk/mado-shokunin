# ScoutConsider — proposal 5 vs the frozen S190 open

Source read: `considerthese/2026-10-24.md` (file dated 2026-10-24), proposal 5 only, read-only — file untouched.

Proposal 5 text (line 50): **"Verify one cited fact first-hand per day, read-only.** For example, re-open one of S178–S182 and confirm the quoted line, so each reflection has at least one claim I checked myself rather than relayed."

## What the reflection actually cites

- Line 21: workspace-rule resolver "sourced to **S178–S182**" (S178 wiki Workspace-Rules.md; S179 WorkspaceRuleManager.cpp; S180 ComplexDataTypes.hpp; S181 ParserUtils.cpp; S182 MiscFunctions.cpp).
- Line 31: "new sources beyond **S183–S185**" (two mutation-testing papers, one own-work SCORECARD block).
- **S190 appears nowhere in `considerthese/2026-10-24.md`** (grep `S19[0-9]` → zero hits).

## What the S190 open verified first-hand (2026-10-24)

- `.ufo/waves/round-33/fetch/S190.bin`, sha256 `799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e` — matches the w1-spec pin; byte-identical to `scratch/ScoutS190/S190.bin` (`diff -q` silent).
- Content: Waybar `src/modules/hyprland/backend.cpp` (tag 0.15.0), 246 lines, namespace `waybar::modules::hyprland`.
- The staged gate-quote `$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr` is a contiguous substring, verbatim at **line 38** (`spdlog::warn("...")` inside `IPC::getSocketFolder`).
- S190 is staged for registry append (`.ufo/waves/round-33/assimilation/staged-ids`, used-by `corpus/knowledge/waybar-module-text-route-r25.md`); it is **not yet in `corpus/SOURCES.md`** (grep count 0).

## Verdict: demand NOT met as written

Proposal 5 requires confirming a claim *of the reflection* — its example names S178–S182, the ids the file itself cites. S190 underlies no claim in `considerthese/2026-10-24.md`, so this open checks a round-33 staged row, not a reflection claim. Mechanism satisfied (read-only, first-hand, dated today, quoted line located in the bytes); target missed. To satisfy it, open one of S178–S182 (e.g. S179 `WorkspaceRuleManager.cpp:25-32,34-52` behind the 41/41 claim) and confirm the quoted lines.
