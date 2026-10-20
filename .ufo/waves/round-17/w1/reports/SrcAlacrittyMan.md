# SrcAlacrittyMan — round 17 (mado-r17-w1), scoped findings

## Behavior

Answered one documentary question: which Alacritty release tag is latest, and what the pinned
man source `extra/man/alacritty.5.scd` says about the config file location search order,
`general.import`, `general.live_config_reload`, and the TOML format. No product, corpus,
registry, lesson, or scorecard file was edited. Only this report was written.

## Result — release identity

| Field | Value | How observed |
|---|---|---|
| Latest release tag | `v0.17.0` | `curl -sS -o /dev/null -w '%{http_code} %{redirect_url}' https://github.com/alacritty/alacritty/releases/latest` → `302 -> https://github.com/alacritty/alacritty/releases/tag/v0.17.0` |
| Tag type / target | `refs/tags/v0.17.0` → commit `dc946285396bd3e251b6942af7e9961b74f76bee` | `git ls-remote --tags --refs https://github.com/alacritty/alacritty.git` (network only, no local repo touched) |
| Highest tag, version sort | `v0.17.0` (no `v0.18.*`; `v0.17.0-rc1`, `-rc2` are prereleases) | same `ls-remote` list piped to `sort -V \| tail -12` |
| Release feed cross-check | first atom entry `tag:github.com,2008:Repository/51980455/v0.17.0`, title `Alacritty Version 0.17.0`, updated `2026-04-06T19:25:38Z` | `https://github.com/alacritty/alacritty/releases.atom` |
| Raw URL fetched | `https://raw.githubusercontent.com/alacritty/alacritty/v0.17.0/extra/man/alacritty.5.scd` | HTTP/2 `200`, `content-type: text/plain; charset=utf-8`, `content-length` not sent |
| Bytes / lines | **28787 bytes, 1075 lines** (final byte `\n`) | `wc -c`, `wc -l`, last-byte check |
| **SHA-256 of raw bytes** | `e444fa45fb7045a61538383c7e588c63e260b9151cb3c8c4dddb742b7a0c4107` | `sha256sum`; two independent downloads hashed identically and `cmp` reported IDENTICAL |
| Access date | `2026-10-20` (fetch completed `2026-10-20T14:01Z`) | `date -u` |

The API route (`/releases/latest`, `/tags`) returned HTTP 403 `API rate limit exceeded` for this
host's egress address; the redirect and atom feed above are the unauthenticated substitutes and
agree with the tag list. The raw endpoint's `ETag` header value (`ab1e21c2…`) does **not** equal
the SHA-256 of the served bytes, nor SHA-256 over git-blob framing of those bytes; it is
therefore not used as an identity anchor. Identity rests on the tag URL plus the byte digest.

Notation used below: line anchors are 1-based lines of the fetched file. Quotes are given as raw
source text, so scd markup survives — `_…_` is groff-style emphasis and `++` is a scd line break.
Word counts ignore markup characters.

## Quotes and anchors

### 1. TOML format (`# SYNTAX`, lines 7–10)

| Anchor | Raw line text | Words |
|---|---|---|
| 5 | `Alacritty - TOML configuration file format.` (under `# NAME`) | 6 |
| 9 | `Alacritty's configuration file uses the TOML format. The format's specification` | 11 |
| 10 | `can be found at _https://toml.io/en/v1.0.0_.` | 7 |

Joined quote (lines 9–10), 15 words:

> Alacritty's configuration file uses the TOML format. The format's specification can be found at https://toml.io/en/v1.0.0.

The page names exactly one format for the config file. The strings `yaml`, `yml`, and
`deprecat` do not occur anywhere in the 1075 lines (`grep -niE 'yaml|\.yml|deprecat'` → no
output), so this pinned revision contains no mention of YAML at all.

### 2. Config file location search order (`# LOCATION`, lines 12–25)

Lines 14–15, 20 words:

> Alacritty doesn't create the config file for you, but it looks for one in the following locations on UNIX systems:

Lines 17–21, verbatim ordered list (UNIX, in the page's own order — this is the search order):

```
17  . _$XDG_CONFIG_HOME/alacritty/alacritty.toml_
18  . _$XDG_CONFIG_HOME/alacritty.toml_
19  . _$HOME/.config/alacritty/alacritty.toml_
20  . _$HOME/.alacritty.toml_
21  . _/etc/alacritty/alacritty.toml_
```

Lines 23–25 (Windows, quoted for completeness only; not a PROVINCE surface):

```
23  On Windows, the config file will be looked for in:
25  . _%APPDATA%\\alacritty\\alacritty.toml_
```

Observed sharp edges, stated only as what the page does and does not say:

- `$XDG_CONFIG_HOME` is named without a fallback caveat on this page; line 19 separately names
  `$HOME/.config/...`, so under the XDG base-directory convention (not stated on this page) those
  two entries denote the same directory. The page does not say whether candidates 1 and 3 are
  de-duplicated.
- The UNIX list has exactly five entries (lines 17–21). There is no `$PREFIX`-relative candidate,
  no `$XDG_CONFIG_DIRS` entry (`grep -n 'XDG_CONFIG_DIRS'` → no match), and no legacy
  `alacritty.yml`/`alacritty.yaml` candidate at this tag.
- `alacritty.5.scd` does not say what happens on a partial/multi-candidate match (first hit wins vs.
  merge). That is **[UNK]** from this source.

### 3. `general.import` (`# GENERAL`, lines 27–48)

Line 29, 10 words, establishes the table name for every key in this section:

> This section documents the *[general]* table of the configuration file.

The key itself is written bare, so the fully-qualified path `general.import` is a derivation from
line 29 + line 31; the literal dotted string `general.import` does **not** occur in the man
source (`grep -n 'general\.'` → no output).

| Anchor | Raw line text | Words |
|---|---|---|
| 31 | `*import* = [_"<string>"_,]` | 3 |
| 33 | `	Import additional configuration files.` | 4 |
| 35 | `	Imports are loaded in order, skipping all missing files, with the importing` | 12 |
| 36 | `	file being loaded last. If a field is already present in a previous import,` | 14 |
| 37 | `	it will be replaced.` | 4 |
| 39 | `	All imports must either be absolute paths starting with _/_, paths relative` | 12 |
| 40 | `	to the user's home directory starting with _~/_, or paths relative from the` | 13 |
| 41 | `	current config file.` | 4 |

Quote A (lines 35–36, ending at `last.`, 16 words) — precedence and missing files:

> Imports are loaded in order, skipping all missing files, with the importing file being loaded last.

Quote B (line 36 from `If a field` through line 37, 14 words) — override direction:

> If a field is already present in a previous import, it will be replaced.

Quote C (lines 39–40, ending at `~/`, 20 words) — accepted path forms:

> All imports must either be absolute paths starting with /, paths relative to the user's home directory starting with ~/

Quote D (line 40 from `or paths` through line 41, 8 words) — the third form, closing quote C:

> or paths relative from the current config file.

Each quote above was mechanically re-checked after writing: with scd emphasis markers stripped and
whitespace collapsed, every one is an exact contiguous substring of its anchored line span, and
all are ≤25 words (counts as labelled).

Consequences that follow directly from A–D, for a documentary route note: an importer listed
later overrides an earlier one; the importing file has the last word; a missing import is not an
error; a relative entry resolves against the directory of the file that names it, so the line 47
example `alacritty-theme/themes/gruvbox_dark.toml` is read from the importer's directory.
The page states no error behaviour for an import that fails to parse — **[UNK]** here.

### 4. `general.live_config_reload` (lines 57–61)

Same table-name derivation as above (line 29); the literal `general.live_config_reload` does not
occur in the man source.

| Anchor | Raw line text | Words |
|---|---|---|
| 57 | `*live_config_reload* = _true_ \| _false_` | 2 |
| 59 | `	Live config reload (changes require restart)` | 6 |
| 61 | `	Default: _true_` | 2 |

Quotes (6 and 2 words):

> Live config reload (changes require restart)

> Default: true

The two documented facts are the default (`true`) and the presence of the parenthetical at line 59.
The page does not say which changes are exempt from the "changes require restart" caveat, nor
which config keys reload live. Whether the parenthetical qualifies the option's own value or the
reload scope is not resolvable from this text — **[INFERENCE]** at best, so it is left unresolved
rather than glossed. Reload *behaviour* was not observed (see Gates).

## Host corroboration (read-only file bytes, no probes)

`XDG_CONFIG_HOME=/home/vgpnk/.config`, `HOME=/home/vgpnk` (from the environment; `echo` only).
Each documented candidate was stat-ed, and the one existing file was hashed and grepped:

```
EXISTS /home/vgpnk/.config/alacritty/alacritty.toml        876 bytes  sha256 695301c86577c808a94a01a4227bfaab3dbbe9a394a9954032f6173adec824f8
ABSENT /home/vgpnk/.config/alacritty.toml
ABSENT /home/vgpnk/.alacritty.toml
ABSENT /etc/alacritty/alacritty.toml
```

Candidate 1 and candidate 3 on the page resolve to the same existing path on this host, so the
search order alone cannot distinguish them here. The host file's line 1 is:

```
general.import = [ "~/.config/omarchy/current/theme/alacritty.toml" ]
```

That is the dotted-key spelling of the key documented at man-source lines 29 and 31, and its
target uses the `~/` path form documented at lines 39–41. A first-pass grep anchored on
`^\s*import` missed this line; the dotted form is why. The import target exists as a plain file,
772 bytes, sha256 `8c3d1457c09d32e83367ac946ff6e85f6bda334c302587a043bef7dc7ac09139`, and its
top-level tables are `[colors.*]` only (`[colors.primary]`, `[colors.cursor]`, …); the active
theme name file reads `matte-black`. The host file has **no** `[general]` table header and **no**
`live_config_reload` key anywhere, so reload would rest on the documented default of line 61, not
on local settings. Host Alacritty **binary version is [UNK]**: no package query was run, and per
the binding pause none may be. Tag-pinned source therefore documents what v0.17.0 says, never
what this host runs.

## Citable facts for a P4 documentary route note

Four claims this item supports with a pinned source and an anchor; none of them is an observed
behaviour claim:

1. Format: the config file is TOML (man lines 5, 9–10), at tag `v0.17.0`.
2. Search order: five UNIX candidates, first at `$XDG_CONFIG_HOME/alacritty/alacritty.toml` and
   last at `/etc/alacritty/alacritty.toml` (lines 17–21). This host has the first candidate only.
3. Import: `general.import` (page: `import` under `[general]`, lines 29, 31) loads files in order,
   skips missing ones, lets the importing file win, and accepts `~/`-relative targets
   (lines 35–41); this host's first line is exactly that form, importing the omarchy theme TOML.
4. Reload: `general.live_config_reload` defaults to `true` (lines 57–61); this host sets no
   override, so the documented default would apply.

What the same source cannot support: that the host binary is v0.17.0, that a reload actually
happened, that the import was parsed, or which keys are exempt from the line 59 caveat.

## Gates

No gate, test, build, lint, census, or measurement was executed, and none was required by this
item. Nothing was executed from the fetched artifact; it was read as bytes only. The following
host actions were deliberately NOT taken, per the binding pause: pacman/yay/paru in any form
(including `-Q`/`-Si`/`-Sp`/`-Fl`), sudo, systemctl, hyprctl, libinput, evtest, wayland-info,
hypridle, hyprlock, alacritty, waybar, walker, omarchy-*, notify-send, screenshots, input or
device probes. No service or compositor operation ran. The lane was not touched with git or jj —
the sole `git` call was `git ls-remote` against the public HTTPS URL in `/tmp`, which reads no
local repository. No `~/.omp/agent/agent.db*` file, credential file, or extra omp process was
touched. No subagent was dispatched and no peer was messaged.

Tooling: nothing installed or upgraded. Used only `curl`, `python3` (stdlib `hashlib`/`json`),
`git ls-remote`, `sha256sum`, `cmp`, `grep`, `stat` — all already present.

## Touched surfaces

- Written: `mado-shokunin/.ufo/waves/round-17/w1/reports/SrcAlacrittyMan.md` (this file, absolute path).
- Read only: `.ufo/waves/round-17/w1/spec.json`, `.ufo/waves/round-17/w1/dispatch.json`,
  `corpus/lessons/round-16-verifier-spotcheck.md`, `.ufo/waves/round-17/w1/reports/ReportSkeleton.md`,
  `~/.config/alacritty/alacritty.toml`, `~/.config/omarchy/current/theme/alacritty.toml`, and
  `~/.config/omarchy/current/theme.name` (host paths as file bytes or `ls`/`readlink` metadata only).
- Scratch, outside the lane: `/tmp/alac/{rel.html,rel.atom,tags.json,alacritty.5.scd,a2.scd}`.
  Nothing was written under `/home/vgpnk/Projects/shokunin` outside this lane root.

## Confidence and remaining unknowns

- Release tag `v0.17.0` and the byte digest: **high** — three independent unauthenticated sources
  (redirect, atom feed, `ls-remote` tag list) and a twice-repeated byte-identical fetch.
- Quotes and anchors: **high** — read directly from the hashed bytes; every quote is ≤25 words
  (counts listed per row) and anchors are the file's own lines.
- Host config path selection: **high** for existence and for the `general.import` line as file
  bytes; **medium** for "this is the file the running terminal reads", because that needs the
  binary's identity and version, which the pause forbids.
- **Unknown / not resolved here:** whether candidates 1 and 3 are de-duplicated; partial-match
  semantics when several candidates exist; which keys reload live; error behaviour for a failed
  import; the parenthetical's referent at line 59; host binary version; any observed reload or
  import behaviour on this host.
- Reserved source id for the `SOURCES.md` row: **S0xx-pending** (L1 assigns at integration).
