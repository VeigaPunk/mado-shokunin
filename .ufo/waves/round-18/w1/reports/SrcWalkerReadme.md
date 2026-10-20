# SrcWalkerReadme — walker upstream at tag v2.17.2 (P3 route scout)

Date: 2026-10-20. Role: leaf scout (read-only). Scope: resolve the walker tag
matching 2.17.2, fetch the tag's raw `README.md` (plus the tag's
`resources/config.toml` it points at), and record tag→commit, digests, and
≤25-word quotes with body-line anchors on (a) what walker is, (b) the elephant
relation, (c) config location. This file and the two fetch receipts are the
only writes. No pacman/expac/systemctl/journalctl/hyprctl/walker/elephant
invocation, no compositor or service operation, no `jj`/git write, no tool
installed or upgraded.

Tags: **[OBS]** read from bytes/outputs this pass, **[INF-docs]** upstream
documentation inference scoped to the tag, **[UNK]** not established here.
Line anchors are lines of the fetched raw body (`walker-readme`,
`walker-config-toml`), which equal README/config line numbers (no added lines).

## 1. Pin resolution and receipts

[OBS] `git ls-remote https://github.com/abenz1267/walker refs/tags/v2.17.2 'refs/tags/v2.17.2^{}' refs/heads/master`
(2026-10-20T15:40Z) returned:

```text
a515085fd39fae80acc086c8fbfd9b7771a9a11d	refs/heads/master
a515085fd39fae80acc086c8fbfd9b7771a9a11d	refs/tags/v2.17.2
```

- **Tag → commit: `v2.17.2` = `a515085fd39fae80acc086c8fbfd9b7771a9a11d`.**
- No `refs/tags/v2.17.2^{}` line → a lightweight tag (the ref points at the
  commit directly). Master happened to point at the same commit at fetch time;
  the pin used below is still the tag ref, not master.
- README and default config were fetched **by tag ref**, so the pin does not
  depend on master staying put.

[OBS] Receipts written as two `mado-fetch-receipt-v1` JSON lines in
`.ufo/waves/round-18/fetch/SrcWalkerReadme/receipts.jsonl`; bodies saved beside
them as `walker-readme` / `walker-config-toml`; both re-hashed against the
receipts (bytes and sha256 match):

| Body | URL | HTTP | Bytes | Lines | sha256 |
|---|---|---|---|---|---|
| `walker-readme` | `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md` | 200 | 7,926 | 233 | `9755f955d5c4e460ac8538e1b648ba2a3c86da37ceaa4d0655dca4d1ea3d2456` |
| `walker-config-toml` | `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/config.toml` | 200 | 13,743 | 305 | `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b` |

Fetch command shape (re-derivable): `curl -sSL --max-time 60 -o BODY -w
'%{http_code} %{url_effective}' URL`; `curl 8.23.0`. No redirects
(`final_url` = URL); both bodies < 1 MiB (nothing skipped).

## 2. What walker is — upstream quotes with anchors

[INF-docs] All quotes are verbatim from `walker-readme` at tag v2.17.2; each
states what the *tag's documentation declares*, never host behavior.

| Anchor | Quote (≤25 words) | Establishes |
|---|---|---|
| `walker-readme:3` | "A fast, customizable application launcher built with GTK4 and Rust, designed for Linux desktop environments." | identity: GTK4 + Rust application launcher for Linux desktops |
| `walker-readme:5` | "[GitBook Documentation/Wiki](https://benz.gitbook.io/walker/)" | documentation surface is external GitBook, not in-tree |
| `walker-readme:13` | "The following Elephant providers are implemented by default:" | feature list is a list of *Elephant providers*, not built-in app code |
| `walker-readme:59` | "make sure [elephant](https://github.com/abenz1267/elephant) is running before starting Walker" | runtime ordering requirement: elephant must already run |
| `walker-readme:163` | "Make sure `elephant` is running and you have providers installed." | same requirement, naming concrete provider binaries (`elephant-providerlist`, `elephant-desktopapplications`) |
| `walker-readme:167` | "In order to improve startup performance, run a Walker service with:" | documented service mode |
| `walker-readme:170` | "walker --gapplication-service" | the service-mode invocation (fenced code line) |
| `walker-readme:182` | "nc -U /run/user/1000/walker/walker.sock" | a documented walker socket at a literal UID-1000 path (see caveat §4) |
| `walker-readme:213` | "Configuration should be done in `~/.config/walker`." | config location |
| `walker-readme:219` | "Themes inherit the default theme by default" | theme inheritance; custom CSS is `themes/yours/style.css` |
| `walker-readme:225` | "You can set the default theme in your `config.toml` f.e. `theme = \"yours\"`." | theme selected by a config key |

Adjacent documented surfaces (same README): 20 default-provider bullets
`:13-34`; basic usage `:159-185`; keybind values `:203-209`; theming
`:217-225`.

## 3. Elephant relation — exactly what the tag says

[OBS] The README names elephant in four distinct ways:

1. **Provider model** — `:13` introduces the feature list as "Elephant
   providers"; `:163` names `elephant-providerlist` and
   `elephant-desktopapplications` as installables.
2. **Startup ordering** — `:59` "elephant is running before starting Walker";
   `:163` repeats it.
3. **Packaging** — the Nix section `:66-74` sets walker's
   `inputs.elephant.follows = "elephant"`, i.e. upstream packaging treats
   elephant as a separate flake input walker follows.
4. **Service launch** — `:97` recommends launching "the elephant and walker
   services using your desktop".

[INF-docs] So the documented contract is: walker is the GTK4 UI; elephant is a
separately installed, already-running provider daemon whose providers supply
the launcher's content. The README does **not** document the transport,
provider discovery, handshake, or version compatibility.

## 4. Config location and config surface (from tag bytes)

- [OBS] Config root: `~/.config/walker` (`walker-readme:213`).
- [OBS] On-disk shape implied by the README: `config.toml` at that root
  (`:225`) and a `themes/` subtree (`:219`, `themes/yours/style.css`).
- [OBS] Shipped default config is `resources/config.toml` (`:215` link; 305
  lines, sha256 `3c5c6867…`). Keys seen read-only: `theme = "default"` (`:9`),
  `[niri]` launch options (`:24-27`), `[shell]` layer/anchor block (`:29-35`),
  `[columns]` (`:37-38`), `[placeholders]` (`:40-41`), `[providers]`
  defaults/empty/ignore list (`:58-66`), `[[providers.prefixes]]` table
  (`:75-113`: `;` `>` `/` `.` `!` `%` `=` `@` `:` `$`), `[providers.actions]`
  (`:118`).
- [OBS] **`additional_theme_location` is absent from the tag's default
  config** (`grep -c` = 0) and from the README (`grep -c` = 0), while the host
  user config declares it (see §5). [INF-docs] Absence in a sample config is
  not an absence claim about the binary (QUALITY criterion 11); the key's
  upstream status stays **[UNK]** here.
- [OBS] README links that resolve to **master**, not the tag: `:9`
  (`refs/heads/master/resources/screenshot.png`), `:116`, `:130`, `:133`
  (`github.com/.../blob|tree/master/...`), `:215`
  (`refs/heads/master/resources/config.toml`). A note citing upstream must
  fetch follow-ups by tag; the row anchor is the tag bytes fetched here.
- [OBS] `:182` hardcodes UID 1000 (`/run/user/1000/walker/walker.sock`); the
  README never mentions `$XDG_RUNTIME_DIR`, so treat the literal UID as an
  illustrative example, not a general path rule.

## 5. Host declaration (file bytes only; not a source claim)

[OBS] `/var/log/pacman.log` (plain read):

- `:1095` `[2026-10-03T17:44:26-0300] [ALPM] installed walker (2.16.2-1)`
- `:1943` `[2026-10-11T16:14:39-0300] [ALPM] upgraded walker (2.16.2-1 -> 2.17.0-1)`
- `:2929` `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`
- `:1096` `[2026-10-03T17:44:26-0300] [ALPM] installed elephant (2.21.0-1)`
- `:3095` `[2026-10-20T09:31:03-0300] [ALPM] upgraded elephant (2.21.0-1 -> 2.22.1-1)`

[OBS] `~/.config/walker/config.toml`: 1,336 B, 49 lines, sha256
`fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787` (same
bytes as the lane's earlier `fecf71fa…`[:16] record, `waybar-walker-plane.md:21`);
`:3 theme = "omarchy-default"`; `:4 additional_theme_location =
"~/.local/share/omarchy/default/walker/themes/"`; `:7` `[placeholders]`; `:16`
`[providers]` with `default = ["desktopapplications","websearch"]` (`:18-21`)
and prefixes `/` `.` `:` `=` `@` `$` (`:24,28,32,36,40,44`). Host-declared
keys, not behavior.

[OBS] Omarchy walker theme root
`~/.local/share/omarchy/default/walker/themes/omarchy-default/` holds
`layout.xml` (6,488 B) and `style.css` (1,243 B); `style.css:1` is
`@import "../../../../../../../.config/omarchy/current/theme/walker.css";` —
a file-level edge to P5 (theme), recorded here as bytes only.

[INF] The installed package version string (2.17.2-1) coincides with the tag
name, but **tag source never proves the host binary**; the prior binary sha
`64826a85…` and version `2.17.0` in `walker-live-surface.md:33-49` predate the
2026-10-20 upgrade and must not be reused as a current pin.

## 6. Constraints for the P3 route note (handoff)

Per the round-18 C2 admission rule, the note
(`corpus/knowledge/walker-route-r18.md`, `surface: P3`) must have, in its first
15 lines, a `source:` line citing **mined, tier-A** rows whose `used-by` names
the note, at least one upstream https docs/spec/code row naming walker/elephant;
then `## Upstream contract`, `## Host declaration`, `## Safe observation`,
`## Unexercised behavior` (≥3 non-blank lines each, `[UNK]` inside the last).
Documentary only; host binaries stay [UNK].

Suggested source-line shape (ids pending L1 assignment; S072-S099 reserved):

```text
source: S0xx-pending (walker v2.17.2 README.md:3,13,59,163,213,219,225; walker v2.17.2 resources/config.toml:9,58,75-113); S0xx-pending host ~/.config/walker/config.toml:3-4,16,23-44; /var/log/pacman.log:2929,3095
```

Safe-observation material (re-runnable, read-only): re-fetch the two tag bodies
and compare sha256; `sha256sum`/`wc -l` the host config; read pacman.log lines.
Forbidden and to be named as such in the note: running walker/elephant, opening
`walker.sock`/`elephant.sock`, any pacman query, any theme/service operation.

## 7. Proposed SOURCES rows (`S0xx-pending`; L1 assigns ids)

Existing registry: 71 rows S001-S071; `grep -i 'walker\|elephant' corpus/SOURCES.md`
→ 0 hits, so **no existing row covers this README** and no duplicate-screen
collision exists. Precedent for shape: S065 ("hypridle README @ v0.1.8",
docs/A).

Row A — required (upstream row naming walker):

```text
| S0xx-pending | walker README @ v2.17.2 — https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md | docs | A | walker's documented identity, elephant provider dependency/ordering, config root and theme selection at the pinned tag | whole file sha256 9755f955d5c4e460ac8538e1b648ba2a3c86da37ceaa4d0655dca4d1ea3d2456 (7,926 B; HTTP 200, fetched 2026-10-20T15:40:04Z, receipt .ufo/waves/round-18/fetch/SrcWalkerReadme/); :3 identity, :13 provider list lead, :59 elephant-before-walker, :163 elephant plus provider binaries, :213 ~/.config/walker, :219/:225 theme selection; tag v2.17.2 → commit a515085fd39fae80acc086c8fbfd9b7771a9a11d | what the launcher declares about itself: GTK4/Rust app, an elephant-provider surface, config rooted at ~/.config/walker, theme chosen by a config key; not runtime behavior, transport, or version compatibility | mined | 2026-10-20 | on-release | corpus/knowledge/walker-route-r18.md |
```

Row B — recommended if the note leans on the shipped default surface:

```text
| S0xx-pending | walker default config @ v2.17.2 — https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/config.toml | code | A | the tag's shipped default config surface and provider prefix table | whole file sha256 3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b (13,743 B, 305 lines; HTTP 200, fetched 2026-10-20T15:40:15Z); :9 theme, :24-27 [niri], :29-35 [shell], :37-38 [columns], :40-41 [placeholders], :58-66 [providers], :75-113 [[providers.prefixes]] | which keys the upstream default config ships and their example values; `additional_theme_location` is absent here and its upstream status is not claimed | mined | 2026-10-20 | on-release | corpus/knowledge/walker-route-r18.md |
```

## 8. Search-log entry draft for L1

> From the `walker-readme` seat (2026-10-20): question — what does walker's
> upstream at the installed tag declare about identity, the elephant relation
> and config location? Where: direct opens of tag-pinned raw `README.md` and
> `resources/config.toml` at `v2.17.2`, no search engine. Identified 2,
> screened 2, included 2, excluded 0. Stop rationale: the tag's README is the
> primary doc surface and it links the default config; the GitBook site,
> elephant repo, changelog, theme/layout files and config-path questions were
> left to sibling seats.

## 9. Boundaries and remaining unknowns

- Not duplicated here (sibling scopes): elephant repo docs (`SrcElephantReadme`,
  `SrcElephantProviders`), walker docs site (`SrcWalkerDocsSite`), default
  config paths (`SrcWalkerDefaultConfig`, `SrcWalkerConfigPaths`), changelog,
  theme set, walker source tree.
- [UNK] walker↔elephant transport/protocol (README documents none); provider
  discovery and version negotiation; whether installed `2.17.2-1` bytes match
  this tag's sources (no binary inspection); `~` expansion in
  `additional_theme_location`; precedence of packaged
  `/etc/xdg/walker/config.toml` (prior lane OBS, not re-measured) over
  `~/.config/walker/config.toml`; theme search order between
  `additional_theme_location` and built-in themes; any rendered output.
- Files written: this report; `receipts.jsonl` (2 lines) and the two raw
  bodies under `.ufo/waves/round-18/fetch/SrcWalkerReadme/`. No tools
  installed or upgraded; no lane gate run.
