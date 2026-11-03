# Gate Quotes — mado round 65 (2026-11-03)

Sourced leg for claim C1: re-opening registry rows S028 and S097 per CORPUS.md rule 1.
All probes executed on 2026-11-03.

---

## Row 1 — S028

- **Row ID**: S028
- **Title**: Hyprland v0.56.2 release
- **URL**: `https://github.com/hyprwm/Hyprland/releases/tag/v0.56.2`
- **Access Date**: 2026-11-03
- **Locator**: Release notes markdown body heading `<h2>Fixes backported</h2>` (in `div.markdown-body[data-test-selector="body-content"]`)
- **Located Quote** (2 words, ≤ 25 words):
  > "Fixes backported"
- **Context / Extended Quote** (13 words, ≤ 25 words; 1st paragraph of release notes directly preceding heading):
  > "A standard patch release backporting some fixes from main on top of 0.56.2."
- **Rule Fix Evidence** (9 words, ≤ 25 words; 5th bullet under `Fixes backported`):
  > "desktop/rules: fix gaps_out rule overriding float_gaps (#15662) by @Dregu"
- **Recorded State in `corpus/SOURCES.md:40`**:
  - `| S028 | Hyprland v0.56.2 release — https://github.com/hyprwm/Hyprland/releases/tag/v0.56.2 | docs | A | 0.56.2 rule behavior fix | “Fixes backported”; v0.56.2 tag, released 2026-08-05 | Shows why patch-level window-rule behavior must be rechecked. | mined | 2026-10-19 | on-release | corpus/knowledge/hyprland-config-era-r12.md |`
  - Previous access/opened date: 2026-10-19
  - Recorded facts: tag date 2026-08-05, rule behavior fix backported.
- **Observed Upstream State (2026-11-03)**:
  - Page fetched via HTTP 200 (`curl -sSL "https://github.com/hyprwm/Hyprland/releases/tag/v0.56.2"`).
  - Title: `Release v0.56.2 · hyprwm/Hyprland · GitHub`.
  - Tag name: `v0.56.2`.
  - Tag date: `2026-08-05` (`<relative-time datetime="2026-08-05T14:14:01Z">05 Aug 14:14</relative-time>`).
  - Release body: Unchanged. Lists backported fixes including the window-rules fix (`desktop/rules: fix gaps_out rule overriding float_gaps (#15662)`).
- **What changed vs row's recorded state**:
  - **Nothing changed.** All recorded facts (v0.56.2 release, tag date 2026-08-05, rule behavior fix in backported fixes) remain true and identical upstream. Only the recheck access date advances from `2026-10-19` to `2026-11-03`.

---

## Row 2 — S097

- **Row ID**: S097
- **Title**: omarchy v3.8.4 matte-black theme payload
- **URL**: `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml`
- **Access Date**: 2026-11-03
- **Locator**: `themes/matte-black/colors.toml:4`
- **Located Quote** (3 words, ≤ 25 words):
  > `background = "#121212"`
- **Recorded State in `corpus/SOURCES.md:109`**:
  - `| S097 | omarchy v3.8.4 matte-black theme payload (supersedes S094) — https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml | code | A | upstream official payload for the matte-black theme, this host's applied theme (~/.config/omarchy/current/theme.name = matte-black, 12 B); not the host's only theme — 19 payload dirs ship under ~/.local/share/omarchy/themes with the same 19 names as the tag's themes/ tree, and ~/.config/omarchy/themes is empty | tag v3.8.4 → commit 8fcc9d6048af4cb0e3af8512c78049857a3b53dd (lightweight: git ls-remote refs/tags/v3.8.4 has no ^{} line and git rev-parse v3.8.4^{commit} agrees); themes/matte-black tree 3fc08f954e5a3f67072a79a7c52d94e0a153b9ec, blobs btop.theme c8cdcd02f5a5… 2648 B, colors.toml 5e1a8ccae846… 461 B, icons.theme a3c0a4ca6d3c… 9 B, neovim.lua 7b3f72b21147… 150 B, preview-unlock.png e23b46655c97… 22524 B, preview.png ed9c7b47bc6c… 470315 B, unlock.png 1a60e7094726… 2512 B, vscode.json 7786fc79047a… 65 B; themes/matte-black/backgrounds tree ff02c34193836c016d8e57bde56bcef5f3c64b4c, blobs 0-ship-at-sea.jpg 4375ee2bdd03… 1681677 B, 1-dark-waters.jpg 2afb1bcb16a5… 1033920 B, 2-dot-hands.jpg b76792cb81eb… 482067 B, omarchy.png b34300c1a912… 4491 B; raw themes/matte-black/colors.toml sha256 dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786, 461 B | supersedes S094 — ... | mined | 2026-10-20 | on-release | corpus/knowledge/theme-route-r18.md |`
- **Observed Upstream & Live State (2026-11-03)**:
  - Upstream tag commit: `git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4` → `8fcc9d6048af4cb0e3af8512c78049857a3b53dd` (reproduces row mapping).
  - Fetched bytes: 461 B via `curl -sSL "https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml"`.
  - Git blob hash: `git hash-object` on fetched file = `5e1a8ccae8462c78a6e9fc491c48cf6d2fc85231` (matches recorded prefix `5e1a8ccae846…`).
  - Git blob hash on host live file `~/.config/omarchy/current/theme/colors.toml` = `5e1a8ccae8462c78a6e9fc491c48cf6d2fc85231`.
  - sha256 comparison:
    1. Row recorded sha256: `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786`
    2. Fetched raw bytes sha256: `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786`
    3. Host live theme bytes sha256 (`~/.config/omarchy/current/theme/colors.toml`): `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786`
  - Agreement: **ALL THREE SHAS AGREE**.
  - Byte-by-byte comparison (`cmp`): Fetched upstream bytes and host live file are 100% byte-identical.
- **What changed vs row's recorded state**:
  - **Nothing changed.** All content-addressed hashes (sha256 digest `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786`, git blob sha `5e1a8ccae8462c78a6e9fc491c48cf6d2fc85231`), tag-to-commit mapping (`8fcc9d6048af4cb0e3af8512c78049857a3b53dd`), file size (461 B), and live host theme match are identical. Only the recheck access date advances from `2026-10-20` to `2026-11-03`.

---

## Verbatim Gate Block Lines (for `corpus/lessons/round-65.md`)

```markdown
### Sourced re-openings (C1)

- **S028 re-opened (2026-11-03)** — `https://github.com/hyprwm/Hyprland/releases/tag/v0.56.2` (accessed 2026-11-03, HTTP 200). Tag date 2026-08-05 confirmed. Located quote: "Fixes backported" (`<h2>Fixes backported</h2>`, 2 words). State unchanged vs recorded row.
- **S097 re-opened (2026-11-03)** — `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml` (accessed 2026-11-03, HTTP 200). Located quote: `background = "#121212"` (`themes/matte-black/colors.toml:4`, 3 words). sha256 `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786` (461 B); git blob `5e1a8ccae8462c78a6e9fc491c48cf6d2fc85231`; tag commit `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`. Agrees with recorded row sha and live host theme bytes (`~/.config/omarchy/current/theme/colors.toml`). State unchanged vs recorded row.
```
