# SrcKitty — round 23 w1 scribe report (C2 upstream sourcing for the kitty terminal)

Scope: open primary upstream sources for the kitty terminal at a pinned release tag, record
URL / access date / tag-commit / sha256 / located quote per source, extract the documentary
route claims (search path and precedence, file name and format, include mechanism, reload of a
running instance), and draft the `corpus/SOURCES.md` rows plus the route-claim rows for
`corpus/knowledge/terminal-trees-r23.md`.

**No product code was edited.** `corpus/SOURCES.md`, `corpus/knowledge/*`, `tools/`, `fixtures`
and every other seat's files were not touched. The only lane-repo writes are this report and
the read-only evidence under `.ufo/waves/round-23/w1/out/SrcKitty/`. No terminal was launched,
no kitty process was signalled, no host configuration was used as a claim source (a read-only
directory listing of `~/.config/kitty` was made for orientation only and is recorded as
out-of-scope below), and the host was not modified.

## Verdict

**PASS (advice + evidence).** 10 version-pinned kitty sources were opened at tag `v0.49.2`
(commit `b2cb871254fbdac19a085188813c8dfb258b95cd`), every fetched file is byte-identical to
the tag tarball copy, 5 documentary route claims were extracted with located quotes, and
11 `SOURCES.md` rows (10 `mined`, 1 `queued`) plus 5 claim rows are drafted below. The
integration owner (MadoR23) owns landing them; nothing was landed here. C2's kitty half is
**not** counted by me — the counter is the integrator's to run after landing.

## Upstream pin

| item | value |
|---|---|
| repository | `kovidgoyal/kitty` (github.com) |
| release tag | `v0.49.2` |
| tag object sha | `e300597364aabb4890ebdd3a5491397f858fd714` |
| peeled commit | `b2cb871254fbdac19a085188813c8dfb258b95cd` |
| release date | 2026-10-01 (`docs/changelog.rst:202` → `0.49.2 [2026-10-01]`) |
| tag tarball | `https://codeload.github.com/kovidgoyal/kitty/tar.gz/refs/tags/v0.49.2` — 9,768,806 B, sha256 `e9ca20b49d0c262af956058ceb97cfef505552dc447d8328ea96d069a04570f3` |
| raw-byte form used for every row | `https://raw.githubusercontent.com/kovidgoyal/kitty/b2cb871254fbdac19a085188813c8dfb258b95cd/<path>` |
| access date | 2026-10-22 |

`git ls-remote https://github.com/kovidgoyal/kitty refs/tags/v0.49.2 refs/tags/v0.49.2^{}`
returned the two shas above; each raw file's sha256 equals the sha256 of the same path inside
the tag tarball (all ten `identical_to_tag_tarball: true` in the receipt).

## Sources opened (each with a located quote, ≤25 words)

| # | path at the pinned commit | sha256 | bytes | located quote (≤25 words) | anchor |
|---|---|---|---|---|---|
| 1 | `docs/conf.rst` | `da42c340321755a25718b5c9a467f0a6bba33f88342d7c4a35e87a6795d4f498` | 3,901 | "You can manually reload the config by pressing reload_config_file (⌃+⌘+, on macOS) or sending kitty the SIGUSR1 signal" | :19-23 |
| 2 | `docs/changelog.rst` | `cd2046f7fb8dbe7cdbf92cda2410e862cf68cd1514380da5e0a3f9c070aa5fae` | 243,954 | "0.49.2 [2026-10-01]" | :202 (§ release headings) |
| 3 | `kitty/simple_cli_definitions.py` | `228f36b35e5e82419b8b4127742efdc5a17387763e62a1b26a73f6802a5452e3` | 30,246 | "config files are searched for in the order: $XDG_CONFIG_HOME/kitty/kitty.conf, ~/.config/kitty/kitty.conf, $XDG_CONFIG_DIRS/kitty/kitty.conf. The first one that exists is used" | :366-370 (`CONFIG_HELP`, :359) |
| 4 | `kitty/launcher/utils.h` | `32a5c10e67efe0e10b9b30d211e1e193d8bd80faaf1f2845a1a3d35188e81cfc` | 9,097 | "q = getenv(\"KITTY_CONFIG_DIRECTORY\"); … q = getenv(\"XDG_CONFIG_HOME\"); check_and_ret(q); check_and_ret(\"~/.config\");" | :210-222 (`get_config_dir`, :202) |
| 5 | `kitty/conf/utils.py` | `5af002918cbf199f2bd250527322b1b49af33fda66d255434d5efb8256eca295` | 17,984 | "Could not find included config file: {val}, ignoring" | :355 (`parse_line`, :277; include branch :295) |
| 6 | `kitty/options/definition.py` | `1ff05cd3a58612c0bd12de7a15d9f645ca3f6ebcdbbb5d0a380740730ef22cc5` | 165,097 | "Automatically reload configuration files when they are changed. The setting is the number of seconds to wait before reloading" | :3091-3100 (`auto_reload_config`) |
| 7 | `kitty/child-monitor.c` | `a4fbe5472c50249c30002919d6454aa97a7fda38d384023472af0bffedd14ae7` | 100,305 | "case SIGUSR1: ss->reload_config = true; break;" | :1708 (chain :1851-1854 → :558-566 → :640) |
| 8 | `kitty/rc/load_config.py` | `89ccc155ef6eadcc72cc81aebf22496b31dfe7ece107cb1fbbd49e66f119dc04` | 2,747 | "(Re)load the specified kitty.conf config files(s). If no files are specified the previously specified config file is reloaded." | :33-35 (`LoadConfig.desc`) |
| 9 | `kitty/cli.py` | `696d04198a48d0d8f05023755efce79f52a53e0e2e3e8abb90a2afa6010c5456` | 22,988 | "SYSTEM_CONF = f'/etc/xdg/{appname}/{appname}.conf'" | :716 (`default_config_paths`, :719-720) |
| 10 | `kitty/constants.py` | `8a0ee5204417ff90747a2965f8b4594a2d3a02d35f7b3728301350892663bde8` | 10,477 | "defconf = os.path.join(config_dir, 'kitty.conf')" | :130 (`config_dir` :128, `_get_config_dir` :109-126) |

Extra located quotes used by the claim rows below, all from the same pinned bytes:

- `docs/conf.rst:27-28` — "kitty looks for a config file in the OS config directories (usually ~/.config/kitty/kitty.conf)".
- `docs/conf.rst:32-33` — "Comments can be added to the config file as lines starting with the # character."
- `docs/conf.rst:36-37` — "Lines can be split by starting the next line with the \ character."
- `docs/conf.rst:41-42` — "You can include secondary config files via the include directive."
- `docs/conf.rst:42-43` — "If you use a relative path for include, it is resolved with respect to the location of the current config file."
- `kitty/conf/utils.py:24` — `key_pat = re.compile(r'([a-zA-Z][a-zA-Z0-9_-]*)\s+(.+)$')`.
- `kitty/conf/utils.py:439-446` — `resolve_config` yields `SYSTEM_CONF` then the resolved `defconf`.
- `kitty/options/definition.py:4694` — `'reload_config_file kitty_mod+f5 load_config_file'`; `kitty_mod` defaults to `ctrl+shift` (`:3650-3651`).
- `kitty/options/definition.py:3099-3100` — "automatic reload works only if the kitty.conf already exists when kitty is started. Changes to this setting by reloading configuration are ignored."
- `kitty/child-monitor.c:640` — `if (reload_config_called) { call_boss(load_config_file, NULL); }`.

### Unopened / not registered

- `https://sw.kovidgoyal.net/kitty/conf.html` → 325-byte JS redirect page to `conf/`; the built
  HTML was opened at `https://sw.kovidgoyal.net/kitty/conf/` (577,387 B, sha256
  `08e6411024fdfc444e47750dadc28b7d87e0bd768695cc635690916e08a9703d`) and cross-checked
  (contains `SIGUSR1`, `KITTY_CONFIG_DIRECTORY`, `globinclude`, `auto_reload_config`,
  `kitty.conf` ×50). It is a **moving build of an unpinned tree**, so it is drafted as a
  `queued` row (S132) and supports **no** claim.
- `kitty/conf/generate.py` was fetched and examined, then dropped from the registry: its
  `x.replace('-', '_')` (`:617`) is Go-API code generation, not config-key parsing, so it does
  not support a dash/underscore equivalence claim. The fetch was deleted from the evidence
  directory rather than registered.
- Nothing else was blocked: no captcha, no bot challenge, no access control was encountered.

## Documentary route claims (5)

**K1 — config file search path and precedence (v0.49.2).**
With no `--config` given, kitty searches `$XDG_CONFIG_HOME/kitty/kitty.conf`, then
`~/.config/kitty/kitty.conf`, then `$XDG_CONFIG_DIRS/kitty/kitty.conf`, and **the first one that
exists is used**; `KITTY_CONFIG_DIRECTORY` disables that search entirely and is always used
instead; `/etc/xdg/kitty/kitty.conf` is merged **before** (lower priority than) any user config
file. The C launcher implements the same precedence at directory granularity:
`KITTY_CONFIG_DIRECTORY` → `XDG_CONFIG_HOME` → `~/.config` → (`~/Library/Preferences` on macOS)
→ each colon-separated `XDG_CONFIG_DIRS` entry → fallback creating `$XDG_CONFIG_HOME/kitty`;
a candidate directory is accepted only if `<dir>/kitty/kitty.conf` exists and the directory is
writable (`is_dir_ok_for_config`). Sources: S124, S125, S130, S123.
Bound: documented and implemented search order at one pinned release; the docs text and the C
code describe the same precedence at two different granularities (file vs directory) and both
are needed; nothing here is a statement about this host.

**K2 — file name and format (v0.49.2).**
The config file is named `kitty.conf` and lives in the kitty config directory (default
`~/.config/kitty`; `defconf = os.path.join(config_dir, 'kitty.conf')`). Format: one
`option value` per line; a `#` that is the **first** character of a line starts a comment; a
line may be continued by starting the next line with `\`; a config key matches
`([a-zA-Z][a-zA-Z0-9_-]*)\s+(.+)$` and an unknown key is logged and ignored
("Ignoring unknown config key"). Sources: S123, S126, S133 (`defconf` = `kitty.conf` in the
config dir), S127 (the documented option set that defines the accepted key names).
Bound: static format facts at the pinned tag. [INFERENCE] A top-level key spelled with a dash
(`background-opacity`) is not accepted, because the parser resolves keys by attribute lookup
on underscore-named option functions (`kitty/options/parse.py` `parse_conf_item`); this was
not executed and is not claimed as a claim.

**K3 — include / import mechanism (v0.49.2).**
`kitty.conf` supports four directives: `include`, `globinclude`, `envinclude`, `geninclude`.
A relative `include` path is resolved **relative to the directory of the including config
file**; environment variables are expanded (`${USER}.conf`, plus the special `KITTY_OS`); a
`globinclude` pattern is resolved against the including file's directory; `envinclude` reads
the matching environment variables' contents; `geninclude` runs a program and includes its
stdout (refused for security when `allow_geninclude` is false). A missing included file is
**logged and ignored, not fatal** ("Could not find included config file: {val}, ignoring"), and
each file is parsed at most once per load (`memory.seen`). Sources: S123, S126.
Bound: parser-level facts at the pinned tag; they do not say that any particular host
`kitty.conf` uses an include, and they do not prove the result of an include at runtime.

**K4 — how a running instance reloads its config (v0.49.2).**
Three documented routes exist: (a) **automatic** — `auto_reload_config` (default `0.1`
seconds, a debounce) reloads the config when it changes, but only when `kitty.conf` already
existed when kitty started, and changes to `auto_reload_config` itself are ignored on reload;
(b) **keybind** — the `reload_config_file` action is bound by default to `kitty_mod+f5`, and
`kitty_mod` defaults to `ctrl+shift` (so `ctrl+shift+f5` on Linux; `ctrl+cmd+,` on macOS);
(c) **signal** — `SIGUSR1` sent to the kitty process sets the child's `reload_config` flag,
which is turned into `reload_config_signal_received` → `reload_config_called` → the boss
action `call_boss(load_config_file, NULL)`. Sources: S123, S127, S128.
Bound: the documented and coded reload routes at the pinned tag. No signal was sent and no
reload was exercised; the running-instance behaviour on this host is not claimed.

**K5 — remote-control reload (v0.49.2).**
The remote-control command `kitten @ load-config` ("(Re)load a config file") reloads the
specified `kitty.conf` file(s) in a running kitty; with no paths, the previously specified
config file is reloaded; the specified paths must exist and be readable **by the kitty
process on the computer that process is running on**, and relative paths are resolved with
respect to the kitty config directory of the running instance. Sources: S129.
Bound: the command's own documented contract at the pinned tag; remote control was not
enabled, connected to or invoked here.

## Draft `corpus/SOURCES.md` rows (exact 11-column shape, not landed)

Shape check: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.
Ids are the next free numbers after the last registered row (`S122`), so the assignment's
`S###-TBD` placeholders resolve to `S123`–`S133`; the integrator may renumber on landing if
another seat landed first. Every `source` cell names kitty, every row is `mined` except S132,
and every row is `opened 2026-10-22` with `recheck on-release`.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S123 | kitty v0.49.2 docs source of conf.html — upstream github.com/kovidgoyal/kitty at commit b2cb871254fbdac19a085188813c8dfb258b95cd; fetched bytes https://raw.githubusercontent.com/kovidgoyal/kitty/b2cb871254fbdac19a085188813c8dfb258b95cd/docs/conf.rst | docs | A | kitty configuration file: where it lives, its text format, the include directives, and the documented reload routes at tag v0.49.2 (release 2026-10-01) | docs/conf.rst:16-63 §Overview and §include @ commit b2cb871254fbdac19a085188813c8dfb258b95cd (sha256 da42c340321755a25718b5c9a467f0a6bba33f88342d7c4a35e87a6795d4f498, 3901 B) | the file is kitty.conf in the OS config directory; comments start with # at line start; lines continue with backslash; include, globinclude, envinclude and geninclude exist; reload is by auto_reload_config, reload_config_file or SIGUSR1 | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S124 | kitty v0.49.2 CLI option definition — upstream github.com/kovidgoyal/kitty at commit b2cb871254fbdac19a085188813c8dfb258b95cd; fetched bytes https://raw.githubusercontent.com/kovidgoyal/kitty/b2cb871254fbdac19a085188813c8dfb258b95cd/kitty/simple_cli_definitions.py | code | A | the documented config-file search order and precedence as the kitty --config help text at tag v0.49.2 | CONFIG_HELP :359-380, search order :366-370 @ commit b2cb871254fbdac19a085188813c8dfb258b95cd (sha256 228f36b35e5e82419b8b4127742efdc5a17387763e62a1b26a73f6802a5452e3, 30246 B) | search order is XDG_CONFIG_HOME then ~/.config then XDG_CONFIG_DIRS, first existing file wins; KITTY_CONFIG_DIRECTORY suppresses the search; /etc/xdg/kitty/kitty.conf is merged with lower priority | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S125 | kitty v0.49.2 launcher config-directory lookup — upstream github.com/kovidgoyal/kitty at commit b2cb871254fbdac19a085188813c8dfb258b95cd; fetched bytes https://raw.githubusercontent.com/kovidgoyal/kitty/b2cb871254fbdac19a085188813c8dfb258b95cd/kitty/launcher/utils.h | code | A | the implemented config-directory selection at tag v0.49.2 | get_config_dir :202-244, KITTY_CONFIG_DIRECTORY :210-213, XDG_CONFIG_HOME :220-222, XDG_CONFIG_DIRS :226-233, is_dir_ok_for_config :190-199 @ commit b2cb871254fbdac19a085188813c8dfb258b95cd (sha256 32a5c10e67efe0e10b9b30d211e1e193d8bd80faaf1f2845a1a3d35188e81cfc, 9097 B) | directory precedence is KITTY_CONFIG_DIRECTORY, XDG_CONFIG_HOME, ~/.config, macOS preferences dir, each XDG_CONFIG_DIRS entry; a candidate is accepted only when kitty/kitty.conf exists inside it and the directory is writable | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S126 | kitty v0.49.2 config parser — upstream github.com/kovidgoyal/kitty at commit b2cb871254fbdac19a085188813c8dfb258b95cd; fetched bytes https://raw.githubusercontent.com/kovidgoyal/kitty/b2cb871254fbdac19a085188813c8dfb258b95cd/kitty/conf/utils.py | code | A | config key syntax, include-directive semantics, missing-file tolerance and config file resolution at tag v0.49.2 | key_pat :24, parse_line :277-359, include branch :295-353, missing-file log :355, resolve_config :439-446 @ commit b2cb871254fbdac19a085188813c8dfb258b95cd (sha256 5af002918cbf199f2bd250527322b1b49af33fda66d255434d5efb8256eca295, 17984 B) | keys are option tokens followed by whitespace and a value; a relative include resolves against the including file directory; a missing included file is logged and ignored; each file is read at most once; /etc/xdg system config is resolved before the user config | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S127 | kitty v0.49.2 option definitions — upstream github.com/kovidgoyal/kitty at commit b2cb871254fbdac19a085188813c8dfb258b95cd; fetched bytes https://raw.githubusercontent.com/kovidgoyal/kitty/b2cb871254fbdac19a085188813c8dfb258b95cd/kitty/options/definition.py | code | A | the auto_reload_config option and the default reload_config_file key binding at tag v0.49.2 | auto_reload_config :3090-3101, default map :4694, kitty_mod default :3650-3651 @ commit b2cb871254fbdac19a085188813c8dfb258b95cd (sha256 1ff05cd3a58612c0bd12de7a15d9f645ca3f6ebcdbbb5d0a380740730ef22cc5, 165097 B) | auto reload is on by default with a 0.1 second debounce and works only when kitty.conf existed at startup; the default reload binding is kitty_mod+f5 and kitty_mod is ctrl+shift | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S128 | kitty v0.49.2 child monitor signal handling — upstream github.com/kovidgoyal/kitty at commit b2cb871254fbdac19a085188813c8dfb258b95cd; fetched bytes https://raw.githubusercontent.com/kovidgoyal/kitty/b2cb871254fbdac19a085188813c8dfb258b95cd/kitty/child-monitor.c | code | A | the SIGUSR1 reload path from signal delivery to the load_config_file boss action at tag v0.49.2 | signal set :1708, relay :1851-1854, flag consumption :558-566, boss call :640 @ commit b2cb871254fbdac19a085188813c8dfb258b95cd (sha256 a4fbe5472c50249c30002919d6454aa97a7fda38d384023472af0bffedd14ae7, 100305 B) | SIGUSR1 is the coded reload signal: it sets the child reload flag and the loop then calls load_config_file on the boss; no restart is required by this path | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S129 | kitty v0.49.2 remote-control load-config command — upstream github.com/kovidgoyal/kitty at commit b2cb871254fbdac19a085188813c8dfb258b95cd; fetched bytes https://raw.githubusercontent.com/kovidgoyal/kitty/b2cb871254fbdac19a085188813c8dfb258b95cd/kitty/rc/load_config.py | code | A | the kitten @ load-config contract for reloading a config file in a running kitty at tag v0.49.2 | LoadConfig short_desc :31, desc :33-36, options_spec :37-55 @ commit b2cb871254fbdac19a085188813c8dfb258b95cd (sha256 89ccc155ef6eadcc72cc81aebf22496b31dfe7ece107cb1fbbd49e66f119dc04, 2747 B) | a running instance can be told to reload a specified kitty.conf; with no paths the previous file is reloaded; paths must exist and be readable by that kitty process; relative paths resolve against its config directory | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S130 | kitty v0.49.2 CLI config path constants — upstream github.com/kovidgoyal/kitty at commit b2cb871254fbdac19a085188813c8dfb258b95cd; fetched bytes https://raw.githubusercontent.com/kovidgoyal/kitty/b2cb871254fbdac19a085188813c8dfb258b95cd/kitty/cli.py | code | A | the system config path constant and the default config path resolution entry point at tag v0.49.2 | SYSTEM_CONF :716, default_config_paths :719-720 @ commit b2cb871254fbdac19a085188813c8dfb258b95cd (sha256 696d04198a48d0d8f05023755efce79f52a53e0e2e3e8abb90a2afa6010c5456, 22988 B) | the system-wide config file is /etc/xdg/kitty/kitty.conf and it is resolved ahead of the user config file; explicit --config paths replace the default resolution | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S131 | kitty v0.49.2 changelog — upstream github.com/kovidgoyal/kitty at commit b2cb871254fbdac19a085188813c8dfb258b95cd; fetched bytes https://raw.githubusercontent.com/kovidgoyal/kitty/b2cb871254fbdac19a085188813c8dfb258b95cd/docs/changelog.rst | docs | A | the identity and release date of the pinned tag used by the kitty route rows | release heading 0.49.2 [2026-10-01] :202 @ commit b2cb871254fbdac19a085188813c8dfb258b95cd (sha256 cd2046f7fb8dbe7cdbf92cda2410e862cf68cd1514380da5e0a3f9c070aa5fae, 243954 B) | the pinned bytes belong to kitty 0.49.2 released 2026-10-01; later releases may change the search order, the include set or the reload routes | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S132 | kitty built documentation (moving build) — https://sw.kovidgoyal.net/kitty/conf/ (redirected from https://sw.kovidgoyal.net/kitty/conf.html) | docs | A | the published HTML rendering of the kitty config documentation; NOT version pinned and NOT claim support | built HTML page conf/ (577,387 B, sha256 08e6411024fdfc444e47750dadc28b7d87e0bd768695cc635690916e08a9703d, opened 2026-10-22) | the published page is rebuilt from an unpinned tree and its bytes move, so the tagged docs source rows S123 and the code rows above carry every claim; the HTML only cross-checks wording | queued | 2026-10-22 | on-release | — |
| S133 | kitty v0.49.2 path constants — upstream github.com/kovidgoyal/kitty at commit b2cb871254fbdac19a085188813c8dfb258b95cd; fetched bytes https://raw.githubusercontent.com/kovidgoyal/kitty/b2cb871254fbdac19a085188813c8dfb258b95cd/kitty/constants.py | code | A | the config directory and the default config file name at tag v0.49.2 | config_dir :128, defconf :130, _get_config_dir :109-126 @ commit b2cb871254fbdac19a085188813c8dfb258b95cd (sha256 8a0ee5204417ff90747a2965f8b4594a2d3a02d35f7b3728301350892663bde8, 10477 B) | the config file is named kitty.conf and sits in the kitty config directory, which the launcher resolves at startup; an empty resolved directory falls back to a temporary directory | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |

Draft note for the registry foot: `S132` is opened but deliberately not mined — a moving build
cannot back a pinned claim; the file `conf.html` now redirects to the multi-page build at
`conf/`.

## Draft claim rows for `corpus/knowledge/terminal-trees-r23.md`

Shape: first cell names the terminal (the round-23 counter matches the first cell against
`foot|kitty|ghostty` and requires every cited `S###` to be `mined`, opened `2026-10-22`, with
the terminal named in its `source` cell). All rows below cite only the kitty rows drafted
above, each of which names kitty in its source cell.

| terminal | host tree | claim | evidence (pinned at kitty v0.49.2) | sources | bound |
|---|---|---|---|---|---|
| `kitty` | `~/.config/kitty/` | kitty reads its configuration file `kitty.conf` from the OS config directory; the search order is `$XDG_CONFIG_HOME/kitty/kitty.conf`, `~/.config/kitty/kitty.conf`, `$XDG_CONFIG_DIRS/kitty/kitty.conf` and the first existing file is used, while `KITTY_CONFIG_DIRECTORY` replaces the search and `/etc/xdg/kitty/kitty.conf` is merged with lower priority than any user file | `kitty/simple_cli_definitions.py:366-370`; `kitty/launcher/utils.h:202-244`; `kitty/cli.py:716` | S124, S125, S130 | documented and implemented order at one tag; the C code selects a directory (kitty.conf must exist inside it and it must be writable); not a host fact |
| `kitty` | `~/.config/kitty/` | the config file format is one `option value` per line, `#` at line start is a comment, a leading `\` continues a line, and the file is named `kitty.conf` inside the kitty config directory | `docs/conf.rst:26-37`; `kitty/conf/utils.py:24`; `kitty/constants.py:130` (`defconf`) | S123, S126, S133 | static format facts at the pinned tag; unknown keys are logged and ignored |
| `kitty` | `~/.config/kitty/` | secondary config files are pulled in with `include`, `globinclude`, `envinclude` and `geninclude`; a relative include resolves against the directory of the including file and a missing included file is logged and ignored rather than fatal | `docs/conf.rst:39-63`; `kitty/conf/utils.py:295-355` | S123, S126 | parser-level facts at the pinned tag; whether any host kitty.conf uses includes is a host claim outside this row |
| `kitty` | `~/.config/kitty/` | a running kitty reloads its config three ways: automatic reload on change (`auto_reload_config`, default 0.1 s debounce, only when kitty.conf existed at startup), the default keybind `kitty_mod+f5` (`ctrl+shift+f5`, kitty_mod defaults to ctrl+shift) bound to `reload_config_file`, or the `SIGUSR1` signal, whose handler calls the `load_config_file` boss action | `docs/conf.rst:19-23`; `kitty/options/definition.py:3090-3101,3650-3651,4694`; `kitty/child-monitor.c:1708,640` | S123, S127, S128 | documented and coded routes at the pinned tag; no signal was sent and no reload was exercised |
| `kitty` | `~/.config/kitty/` | the remote-control command `kitten @ load-config` reloads a specified `kitty.conf` in a running kitty; with no paths the previously specified file is reloaded, the paths must be readable by that kitty process, and relative paths resolve against its config directory | `kitty/rc/load_config.py:31-40` | S129 | command contract at the pinned tag; remote control was not enabled or invoked |

The `host tree` cell names the tree the upstream route applies to (the path only); the tree's
bytes on this host are the host seat's measurement, not mine — a read-only `ls -la
~/.config/kitty` showed the directory exists with `kitty.conf` (954 B) and
`kitty.conf.bak.20261003-190229`, and I did not use those bytes for any claim.

Integration notes for the owner:

- The note file must exist at the landed revision for the counter to score; the counter
  (`python3 -I .ufo/waves/round-23/c2/count.py REV`, **version 2** at HEAD `4de4464`) requires
  the note's rows to cite `S###` tokens that resolve in `corpus/SOURCES.md` at the same
  revision, a cell naming the host tree `~/.config/kitty/`, and registry rows whose source
  cell names kitty as a whole word, names neither `foot` nor `ghostty`, and contains
  `github.com/kovidgoyal/kitty` (or `sw.kovidgoyal.net/kitty`).
- Landing the raw.githubusercontent.com URL alone in a source cell would **not** satisfy the v2
  upstream-token rule; each of my mined rows now carries the `github.com/kovidgoyal/kitty`
  upstream token plus the fetched-bytes URL.
- Row shape is machine-checked: exactly 11 pipe-separated cells, `status` in cell 8 and
  `opened` in cell 9, and no literal `|` inside a cell.
- The kitty rows count for kitty only if the note's first cell is exactly `kitty` (backticks
  allowed).
- Id bands agreed across the three C2 source seats (kitty/ghostty/foot), no overlap:
  kitty **S123–S133** (this seat; S132 is the queued unpinned docs build), ghostty
  **S134–S139**, foot **S140–S146**. All three bands are `mined` except my S132, tier A,
  opened 2026-10-22, recheck on-release, used-by `corpus/knowledge/terminal-trees-r23.md`.
  Confirmed by direct peer exchange, not by reading the other seats' files.

### Shape and rule self-check against the lane's own counter v2 (observed, on my draft rows)

The lane's C2 counter was tightened mid-round: `.ufo/waves/round-23/c2/count.py` at HEAD
`4de4464` is `counter_version: 2` (v1 is in lane history at `6b383c46`). v2 additionally
requires, per note row, a cell containing the host tree `~/.config/kitty/`; and per registry
row, a source cell that names `kitty` as a whole word, names neither `foot` nor `ghostty` as a
whole word, and contains `github.com/kovidgoyal/kitty` or `sw.kovidgoyal.net/kitty`.

I therefore revised the drafts: every mined source cell now carries
`upstream github.com/kovidgoyal/kitty at commit b2cb871254fbdac19a085188813c8dfb258b95cd`
next to the fetched-bytes URL (the raw URL alone does **not** contain the required
`github.com/kovidgoyal/kitty` substring, because it reads `githubusercontent.com`), and each of
the five note rows gained a `host tree` cell reading `~/.config/kitty/`.

Validation was then run with the lane's own module — `importlib` load of
`.ufo/waves/round-23/c2/count.py` at HEAD `4de4464`, its `cells`, `names` and `source_ok`
functions applied to the two draft tables in this report (the landed `SOURCES.md` was neither
read for this nor modified):

```
registry rows parsed: 11 (all with 11 cells)
  S123 S124 S125 S126 S127 S128 S129 S130 S133 -> source_ok(kitty) = True
      upstream token matched: github.com/kovidgoyal/kitty ; names foot=False ghostty=False
  S132 -> source_ok(kitty) = False (status queued, as intended: it supports no claim)
claim rows: 5 ; first cell `kitty` in all five ; host-tree cell present in all five
  counted S-ids per row: S124,S125,S130 | S123,S126,S133 | S123,S126 | S123,S127,S128 | S129
kitty counted: S123 S124 S125 S126 S127 S128 S129 S130 S133 -> kitty counts
```

So the drafted material satisfies the v2 rules for kitty: once the rows and the note rows are
landed at the same revision, kitty counts in the counter. This is a check of my draft text
against the counter's own functions — not a measurement of the counter at a landed revision,
which is the integrator's to run.

## Exact commands run

```
git ls-remote https://github.com/kovidgoyal/kitty refs/tags/v0.49.2 refs/tags/v0.49.2^{}
curl -sS https://api.github.com/repos/kovidgoyal/kitty/tags?per_page=20
curl -sSL -o kitty-v0.49.2.tar.gz https://codeload.github.com/kovidgoyal/kitty/tar.gz/refs/tags/v0.49.2
tar xzf kitty-v0.49.2.tar.gz -C /tmp/kitty-src
curl -sSL -o <out>/raw/<path> https://raw.githubusercontent.com/kovidgoyal/kitty/b2cb871254fbdac19a085188813c8dfb258b95cd/<path>
curl -sSL -o <out>/raw/conf.html.live https://sw.kovidgoyal.net/kitty/conf.html
curl -sSL -o <out>/raw/conf.html.live https://sw.kovidgoyal.net/kitty/conf/
sha256sum <each fetched file>
diff -q <fetched raw file> /tmp/kitty-src/kitty-0.49.2/<same path>   # all identical
```

Read-only greps (`grep -n`) over the extracted tag tree located every quoted line; no
upstream file was modified, no kitty binary was run, and no host file was changed.

## Evidence paths

| artifact | path |
|---|---|
| this report | `.ufo/waves/round-23/w1/reports/SrcKitty.md` |
| fetch receipt (sha256 + URL + tarball equality per file) | `.ufo/waves/round-23/w1/out/SrcKitty/fetch-receipt.json` |
| raw pinned bytes | `.ufo/waves/round-23/w1/out/SrcKitty/raw/` (10 pinned files + `conf.html.live`) |

## Gates

- Lane bounds honoured: only the report file and `w1/out/SrcKitty/` were written; `SOURCES.md`
  and `corpus/knowledge/` were not edited.
- Host safety: no package transaction, no service or display change, no `~/.config` write,
  no kitty process started or signalled; only ordinary HTTP fetches and local reads.
- Source discipline: every claim rests on bytes pinned to commit
  `b2cb871254fbdac19a085188813c8dfb258b95cd` (tag `v0.49.2`), each verified byte-identical to
  the tag tarball; the one unpinned artifact is registered as `queued` and supports no claim.
- Nothing was installed or upgraded; no tooling change was needed.

## Out of scope (not claimed, not done)

- Host kitty state (installed version, `~/.config/kitty/kitty.conf` bytes and its `.bak`, which
  exists on this host) — that is the host-seat's measurement, not mine; I did not use it as a
  claim source.
- Whether kitty is the terminal this host launches, and any `xdg-terminal-exec` route — round-17
  territory owned by other rows.
- Running kitty, sending SIGUSR1, editing any config, enabling remote control.
- The other two terminals (foot, ghostty) — separate seats.

## Open items and residual risk

1. The counter is the integrator's to run; I did not run `c2/count.py` because the note file
   and the `SOURCES.md` rows do not exist yet at any revision I may touch — running it now would
   only re-measure the registered 0/3 baseline.
2. The published HTML (S132) is a moving build; if a later round needs the rendered page as a
   citation, it must be replaced by the tagged `docs/conf.rst` row (S123) or a dated snapshot.
3. [INFERENCE] The dash-spelling of a top-level option key is rejected by the parser; this was
   not executed and is therefore kept out of the claim rows.
4. The v0.49.2 pin is the newest kitty release at the access date; a later release could move
   the search order, the include set or the reload routes, so `recheck on-release` is the
   standing trigger for every kitty row.
5. The C2 counter was tightened mid-round (v1 `6b383c46` → v2 `4de4464`). My drafts were
   written against v1 and were revised against v2; if the counter is tightened a third time
   before landing, the same drill applies — re-run the `source_ok` check above against the new
   module rather than trusting this text.
