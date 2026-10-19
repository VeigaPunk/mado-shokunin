# L2 seat R12Connector-3 — final output (verbatim, 2026-10-19)

### Sibling-Overlap Scan: Mado Round 12

| Lane | Surface | Evidence (`path:line`) | Mado Action |
|---|---|---|---|
| **tameshi** | `mutate-and-run.sh` | Main & kaika worktree both `75ed934d…` vs mado r8 `cf41efaa…` (`gate-standing-use.md:228`), r10/r11 `75ed934d…` (`closeout-r11.md:102,273`, `round-10.md:181`) | Read-only harness; print sha as provenance, never patch or gate (`tools/mado-verify.sh:1270-1273,1505`). |
| **kagi** | Secrets shape-only | `kagi-shokunin/SKILL.md:14-17,144-148` (hard rule: never print/copy tokens; state pinned by shape, not content) | Mirror shape-only reads for window titles, logs, signatures (`SKILL.md:32,232`); configs store zero secret material. |
| **chousa** | Research method | `chousa-shokunin/SKILL.md:8-11,15-24`; `SOURCES-CONTRACT-v1.md:52-55` Rule 3 (no second research method) | Keep `SOURCES.md` strictly as a curated registry; do not duplicate chousa's hierarchy or claim-verification method. |
| **kama** | Model endpoints vs UI | `kama-shokunin/SKILL.md:8-10,27-31` (owns local model ports); `mado-shokunin/SKILL.md:46,67` (`ai-usage.conf`) | Mado owns desktop display (waybar `custom/ai-usage`, hypr float rules); kama owns endpoint process and port health. |
| **souji** | Hygiene & operator configs | `souji-shokunin/SKILL.md:2,21-24` (never operator config); `souji-shokunin/MINT.md:31` (mado is detect-and-report) | Detect and report config/artifact drift; never delete operator configs, external repos, or sibling worktrees. |
| **audio** | Portal & bar PipeWire clients | `audio-shokunin/corpus/live/r80-scout/runs/p7-linkauthority/F-wpctl/status.stdout:3,5,9` (xdph & waybar clients) | Mado owns compositor layers & portal configs (`xdph.conf`); audio-shokunin monitors PipeWire streams. |
| **tsukuroi** | Walker packaging & hooks | `tsukuroi-shokunin/SKILL.md:101,404,755,842` (`walker 2.17.0-1`, `omarchy-walker`, `walker-restart.hook`) | Mado inspects user config, sockets, layers, D-Bus (`dev.benz.walker`); tsukuroi owns pacman package/hook repair. |

### Cross-Lane Patterns: SOURCES.md, QUALITY.md, Mistakes
- **Adopt (Conventions):**
  - *SOURCES registry*: 11 columns, scoped tiers (A/B/C per topic), exact commit/line anchors, valid `used-by` paths pointing to real files, and unopened leads kept in `## Leads` bullets (`chousa-shokunin/corpus/SOURCES.md:10-28`, `kama-shokunin/corpus/SOURCES.md:10-33`, `SOURCES-CONTRACT-v1.md:19-41`).
  - *QUALITY criteria*: Pair every rule with a mined mistake from `corpus/lessons/round-12.md` `## Mistakes M<k>` with an explicit violation trigger (`kagi-shokunin/corpus/QUALITY.md:20-49`, `kengaku-shokunin/corpus/QUALITY.md:71-80`, `souji-shokunin/corpus/QUALITY.md:24-35`).
  - *Mistakes taxonomy*: Numbered M1..M14 incidents stating class, evidence anchor, and corrective criterion (`mado-state.md:270-285`).
- **Avoid (Anti-patterns):**
  - *Row-count Goodhart*: Inflating row quotas rather than admitting grounded knowledge (`SOURCES-CONTRACT-v1.md:56-58`).
  - *Tier inflation*: Marking community/tertiary sources as Tier A (contract rule: `community is never A`, `SOURCES-CONTRACT-v1.md:30,78`).
  - *Placeholder rows*: Committing `<FILL>` / draft placeholder rows or unopened URLs into the registry table (`kagi-shokunin/corpus/QUALITY.md:45`).
  - *Unanchored criteria*: Bare abstract rules without lesson citations (mado's legacy 5-line probation draft; `mado-state.md:302`).

### Contested Scope & Adjacency: `~/Projects/gkeep`
- **Evidence:** Unmanaged operator repository (`grep -c gkeep /home/vgpnk/Projects/shokunin/MANIFEST.json` → 0). Installer `~/Projects/gkeep/install.sh:21-36,60-82,88-95` mutates mado config surfaces (`~/.config/hypr/hyprland.conf`, `gkeep.conf`, `~/.config/waybar/config.jsonc`, `style.css`) and reloads daemons (`hyprctl reload`, `omarchy restart waybar`).
- **Recommended Report-Not-Absorb Wording:**
  *"Adjacency (operator scope): `~/Projects/gkeep` is an unmanaged operator project outside the fleet manifest (`MANIFEST.json` count: 0). Mado measures, re-anchors, and gates config drift resulting from external execution (`install.sh`), but treats the tool and its repository as out-of-province; mado reports foreign mutations to the operator/integrator and never absorbs, edits, or deletes unmanaged external trees."*
