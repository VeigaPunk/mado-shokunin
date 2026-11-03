# R65ScoutSources — Seat Report (round 65, wave w1)

**Seat**: `R65ScoutSources`  
**Role**: `scout`  
**Duty**: Re-open registry rows S028 and S097 for mado claim C1's sourced leg (CORPUS.md rule 1).  
**Date**: 2026-11-03  
**Lane repo**: `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Scratch**: `/fast/scratch/hyaku/mado-r65/w1/R65ScoutSources/` (cleaned up before yield)  
**Deliverables**:
- `gate-quotes.md`: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-65/w1/R65ScoutSources/gate-quotes.md`
- `report.md`: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-65/w1/R65ScoutSources/report.md`
- Report link/mirror: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-65/w1/R65ScoutSources.md`

---

## 1. Commands Executed and Return Codes (QUALITY 26 evidence)

| Step | Command | rc | Key Result |
|---|---|---|---|
| Read S028 row | `sed -n '40p' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` | 0 | Opened 2026-10-19; quote “Fixes backported”; tag 2026-08-05 |
| Read S097 row | `grep -n 'S097' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` | 0 | Line 109: sha `dbdd13a6…`, commit `8fcc9d60…`, blob `5e1a8ccae846…` |
| Live theme sha256 | `sha256sum ~/.config/omarchy/current/theme/colors.toml` | 0 | `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786` |
| Fetch S028 release | `curl -sSL "https://github.com/hyprwm/Hyprland/releases/tag/v0.56.2" -o <scratch>/s028_page.html` | 0 | 180,186 B HTML received (HTTP 200) |
| Inspect S028 time tag | `python3 -c '<soup extraction of relative-time>'` | 0 | `2026-08-05T14:14:01Z` ("05 Aug 14:14") |
| Fetch S097 raw URL | `curl -sSL "https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml" -o <scratch>/colors.toml` | 0 | 461 B received (HTTP 200) |
| Fetched bytes sha256 | `sha256sum <scratch>/colors.toml` | 0 | `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786` |
| Live theme git blob | `git hash-object ~/.config/omarchy/current/theme/colors.toml` | 0 | `5e1a8ccae8462c78a6e9fc491c48cf6d2fc85231` |
| Fetched git blob | `git hash-object <scratch>/colors.toml` | 0 | `5e1a8ccae8462c78a6e9fc491c48cf6d2fc85231` |
| Live vs fetched cmp | `cmp <scratch>/colors.toml ~/.config/omarchy/current/theme/colors.toml` | 0 | Byte-identical (461/461 B) |
| Upstream tag commit | `git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4` | 0 | `8fcc9d6048af4cb0e3af8512c78049857a3b53dd refs/tags/v3.8.4` |

---

## 2. Findings

### Row 1 — S028 (Hyprland v0.56.2 release)
- **URL**: `https://github.com/hyprwm/Hyprland/releases/tag/v0.56.2`
- **Access Date**: 2026-11-03
- **Page Verification**:
  - The page displays release `v0.56.2` under `hyprwm/Hyprland`.
  - The release tag date is confirmed as **2026-08-05** (`datetime="2026-08-05T14:14:01Z"`).
  - The release notes describe backported fixes on top of 0.56.2, including the window-rules fix: `desktop/rules: fix gaps_out rule overriding float_gaps (#15662)`.
  - All facts recorded in the current SOURCES.md row remain true and accurate.
- **Located Quote**:
  - Quote: `"Fixes backported"` (2 words, ≤ 25 words).
  - Locator: `<h2>Fixes backported</h2>` in markdown release body.
  - Supplemental context quote: `"A standard patch release backporting some fixes from main on top of 0.56.2."` (13 words, ≤ 25 words, introductory paragraph).
- **Delta vs Recorded State**:
  - **Nothing changed.** Upstream release contents, release date, and tags are unchanged. Only the recheck access date advances from `2026-10-19` to `2026-11-03`.

### Row 2 — S097 (omarchy v3.8.4 matte-black theme payload)
- **URL**: `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml`
- **Access Date**: 2026-11-03
- **Three-Way SHA-256 Comparison**:
  1. **Row's recorded sha256**: `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786`
  2. **Fetched raw bytes sha256**: `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786`
  3. **Host live theme bytes sha256** (`~/.config/omarchy/current/theme/colors.toml`): `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786`
  - **Verdict**: **ALL THREE SHAS AGREE IDENTICALLY.**
- **Git Object & Tag Verifications**:
  - Tag-to-commit mapping: `git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4` yields `8fcc9d6048af4cb0e3af8512c78049857a3b53dd refs/tags/v3.8.4` (rc=0), exactly matching the recorded commit.
  - Git blob sha of fetched file: `5e1a8ccae8462c78a6e9fc491c48cf6d2fc85231`, matching the recorded prefix `5e1a8ccae846…`.
  - Git blob sha of host live file: `5e1a8ccae8462c78a6e9fc491c48cf6d2fc85231`.
  - Direct byte comparison: `cmp` exit 0 (identical 461 bytes).
- **Located Quote**:
  - Quote: `background = "#121212"` (3 words, ≤ 25 words).
  - Locator: `themes/matte-black/colors.toml:4`.
- **Delta vs Recorded State**:
  - **Nothing changed.** All content-addressed hashes, tag commit mappings, and file contents reproduce identically. Only the recheck access date advances from `2026-10-20` to `2026-11-03`.

---

## 3. Defects Seen

- **Defects observed**: 0.
- Neither upstream source has experienced unannounced drift, silent mutation, deletion, or movement.
- Neither row's HELD pins or recorded content hashes require correction.
- No erratum required; standard recheck date advance applies.

---

## 4. Tool Installs / Upgrades

- **None**. Existing host utilities (`curl 8.11.0`, `git 2.56.0`, `sha256sum`, `python 3.14.8`) were sufficient. Pacman pause policy strictly respected.
