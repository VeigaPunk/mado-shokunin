# SrcAlacrittyChangelog — Alacritty CHANGELOG at the latest release tag

Role: scout, report only. No lane file was edited; no tool was installed or updated;
no sudo/pacman/yay/paru/systemctl/hyprctl/live probe was run (host pause obeyed).

## Question

Pin Alacritty's `CHANGELOG.md` at the latest release tag, record its SHA-256, and quote
the version-anchored entries for the YAML→TOML migration and the `[general]`
`import` / `live_config_reload` moves, so the host Alacritty config can be era-labelled
from file bytes alone.

## Provenance (all fetches 2026-10-20, raw bytes, no transformation)

| Artifact | URL | HTTP | Bytes | SHA-256 |
|---|---|---|---|---|
| CHANGELOG @ tag | `https://raw.githubusercontent.com/alacritty/alacritty/v0.17.0/CHANGELOG.md` | 200 | 63098 | `c38487aa1ccb11882d94e014c8eedd0a3a96f6c767c9fd0322a9d29f0aa3370a` |
| `alacritty.5.scd` @ tag | `https://raw.githubusercontent.com/alacritty/alacritty/v0.17.0/extra/man/alacritty.5.scd` | 200 | 28787 | `e444fa45fb7045a61538383c7e588c63e260b9151cb3c8c4dddb742b7a0c4107` |
| CHANGELOG @ v0.14.0 (cross-check) | `https://raw.githubusercontent.com/alacritty/alacritty/v0.14.0/CHANGELOG.md` | 200 | 59553 | `42b0f9198d956a96c4ea9ea660b8f5400620510bf47acc170f6332138f450913` |
| CHANGELOG @ master (not cited) | `https://raw.githubusercontent.com/alacritty/alacritty/master/CHANGELOG.md` | 200 | 63575 | `0b86a090d3c7cd11fd234654002df2fba36b963bba95e825517cf232a8f06223` |

Latest-release resolution (GitHub REST API was unavailable: `HTTP/2 403`,
`x-ratelimit-remaining: 0`, so no API claim is made):

- `curl -sSI https://github.com/alacritty/alacritty/releases/latest` → `302`,
  `location: https://github.com/alacritty/alacritty/releases/tag/v0.17.0`.
- `git ls-remote --tags --refs` newest strict `vX.Y.Z` tags:
  `v0.15.0 v0.15.1 v0.16.0 v0.16.1 v0.17.0`.
- `https://github.com/alacritty/alacritty/releases.atom` first (non-RC) entry:
  `Alacritty Version 0.17.0` with `updated 2026-04-06T19:25:38Z`; RC2 `2026-04-02`,
  RC1 `2026-03-21`; prior stable `0.16.1` at `2025-10-20T05:34:00Z`.

Result: the latest release tag is **v0.17.0**. The tag-pinned file's first version
section is `## 0.17.0` (l.11) with no `Unreleased` section. The `master` copy begins
with `## 0.18.0-dev` (unreleased, 477 bytes longer) and is **not** used for any claim.

Access date for every URL above: **2026-10-20**.

## Version-anchored findings (`CHANGELOG.md` @ v0.17.0 line anchors)

| Version | Line | Entry (verbatim, ≤25 words) |
|---|---|---|
| 0.6.0 | 689 | `Configuration file option for sourcing other files (`import`)` |
| 0.13.0 | 249–250 | `Configuration file now uses TOML instead of YAML` / `Run `alacritty migrate` to automatically convert all configuration files` |
| 0.13.0 | 253 | `Deprecated config option `key_bindings`, use `keyboard.bindings`` |
| 0.13.0 | 258 | `OSC 52 paste ability is now **disabled by default**; use `terminal.osc52` to adjust it` |
| 0.13.1 | 201 | `` `alacritty migrate` will ignore null values in yaml instead of erroring out `` |
| 0.14.0 | 128 | `` `alacritty migrate` support for TOML configuration changes `` |
| 0.14.0 | 136–137 | `Moved config options `import`, `working_directory`, `live_config_reload`, and `ipc_socket`` / `to the new `general` section` |
| 0.15.0 | 112–113 | `` `alacritty migrate` crashing with recursive toml imports `` / `Migrating nonexistent toml import breaking the entire migration` |
| 0.16.0 | 58 | `Add `/etc/alacritty/alacritty.toml` fallback for system wide configuration` |
| 0.17.0 | 22 | `Support TOML 1.1 syntax` |

Section headers used above are at v0.17.0 `CHANGELOG.md` lines 221 (`## 0.13.0`),
119 (`## 0.14.0`), 93 (`## 0.15.0`), 46 (`## 0.16.0`), 11 (`## 0.17.0`). The same
`[general]` entry is byte-present in `CHANGELOG.md` at the `v0.14.0` tag
(`grep -n -A1 'Moved config options'` → lines 28–29), so it was shipped, not
retro-edited.

Pinned manual cross-check (`alacritty.5.scd` @ v0.17.0): `# GENERAL` at l.27,
`This section documents the *[general]* table of the configuration file.` at l.29,
`*import* = [_"<string>"_,]` at l.31, `*live_config_reload* = _true_ | _false_` at
l.57 with `Default: _true_` at l.61. So the current canonical paths are
`general.import` and `general.live_config_reload`, not top-level keys.

Era summary for the move: `import` was introduced top-level in **0.6.0**; the whole
config file format flipped YAML→TOML in **0.13.0** (with `alacritty migrate` as the
converter); `import`, `working_directory`, `live_config_reload` and `ipc_socket` moved
under `[general]` in **0.14.0**; TOML 1.1 parsing arrived in **0.17.0**.

## Host config era label (file bytes only, no execution)

Observed paths and digests:

| Path | Bytes | SHA-256 |
|---|---|---|
| `~/.config/alacritty/alacritty.toml` | 876 | `695301c86577c808a94a01a4227bfaab3dbbe9a394a9954032f6173adec824f8` |
| `~/.config/alacritty/alacritty.toml.bak.20261003-190229` | 873 | `ea3e0fa094ca2c763d284dbba39730ee3638ed20c97da6e69adb45f77ee1207a` |
| `~/.config/omarchy/current/theme/alacritty.toml` (import target) | 772 | (not digested; colors-only, read in full) |

`diff` of live file vs its dot-timestamped backup shows exactly one changed line:
`size = 9` → `size = 12.5`. Nothing else differs.

Discriminating key: the live file's first line is

```toml
general.import = [ "~/.config/omarchy/current/theme/alacritty.toml" ]
```

`general` (as a dotted key, semantically the same table as `[general]`) exists only
from **0.14.0**. A 0.13-era config would carry a top-level `import = [...]` and no
`general` table. Therefore the host config is written for **≥0.14.0 schema**; it is
not YAML-era and not 0.13-era.

Supporting key-era observations in the same file, all canonical post-0.13 spellings:

- `[terminal] osc52 = "CopyPaste"` — `terminal.osc52` introduced 0.13.0 (l.258).
- `[keyboard] bindings = [...]` — rename from `key_bindings` in 0.13.0 (l.253).
- `[env]`, `[font].{normal,bold,italic,size}`, `[window].{padding,decorations}` —
  long-standing keys, no era discrimination on their own.

Every key the host file uses resolves in the pinned v0.17.0 manual:
`import` (l.31), `padding` (l.104), `decorations` (l.117), `normal` (l.239),
`size` (l.267, float — `12.5` is valid), `osc52` (l.618), `bindings` (l.751), plus
the `# ENV` section (l.69). No key used by the host file was removed by 0.17.0.

Corroborating negatives/positives: `ls ~/.config/alacritty/` contains only the two
`.toml` files (no `alacritty.yml`/`.yaml` remnant; `grep -i 'yml\|yaml'` over the
listing returns nothing, exit 1). The import target
`~/.config/omarchy/current/theme/alacritty.toml` exists (772 bytes) and is a
colors-only TOML file with no `[general]` key. `readlink -f ~/.config/omarchy/current`
returns the path unchanged: it is a real directory, not a symlink.

Era label reached: **TOML-era, `[general]`-era (≥0.14.0) config schema**, file mtimes
`2026-10-03`, i.e. authored after the 0.16.1 (2025-10-20) and 0.17.0 (2026-04-06)
releases. Upper bound from bytes alone: the file contains no 0.15/0.16/0.17-only
syntax, so the bytes do not prove it was written against 0.17.x; they prove only
≥0.14.0.

## Confidence

- **High** — latest release tag is v0.17.0 and the quoted digests/line anchors are
  from the tag-pinned raw file (two independent route checks plus atom date).
- **High** — version mapping YAML→TOML = 0.13.0; `[general]` move = 0.14.0; both
  re-read in the v0.14.0-tag changelog and the v0.17.0 manual.
- **High** — host config is ≥0.14.0-schema TOML (decisive `general.import` key),
  containing no removed keys as of 0.17.0.
- **Medium** — that the host config was authored against 0.17.x specifically; only
  the timeline (mtime 2026-10-03 after the 0.17.0 release) supports it, and that is
  inference, not observed schema evidence.

## Remaining unknowns

- **Host Alacritty binary version: `[UNK]`.** No package query was permitted under
  the host pause, and a tag's source cannot establish an installed binary. The era
  label above describes the config *schema*, never the running binary.
- Whether `alacritty migrate` was ever invoked on this host, and by which version:
  `[UNK]` (no shell-history or binary provenance was consulted).
- Whether the live config actually parses on the installed binary, and whether
  `live_config_reload` resolves that import at runtime: **unobserved by design**
  (documentary/changelog evidence only; no invocation, no live probe).
- Whether the `.bak` naming convention implies an Omarchy-managed rewrite: **not
  investigated**, outside this question.

## Verification performed

- `sha256sum` on each fetched file (digests above); `wc -c` for byte sizes.
- `grep -n` + a Python pass that attributes every cited line to the nearest preceding
  `## <version>` header, so no entry is credited to the wrong release.
- `grep -n -A1 'Moved config options'` on the v0.14.0-tag changelog (lines 28–29).
- `sed -n '18,70p'` on the v0.17.0 manual to confirm `# GENERAL` scope of `import`
  and `live_config_reload`.
- `cat -n`, `diff -u`, `sha256sum`, `ls` over `~/.config/alacritty/` and the imported
  theme file; `readlink -f` on `~/.config/omarchy/current`.

No installs or updates were made, so there is nothing to record for the tooling
directive. No file outside this report was written.
