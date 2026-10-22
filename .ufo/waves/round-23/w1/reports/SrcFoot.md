# SrcFoot — round 23 w1 scribe report (C2 upstream sourcing for the foot terminal)

Scope: open primary upstream sources for the foot terminal at a pinned release tag, record
URL / access date / tag-commit / sha256 / located quote per source, extract the documentary
route claims (search path and precedence, file name and format, include mechanism, reload of a
running instance), and draft the `corpus/SOURCES.md` rows plus the route-claim rows for
`corpus/knowledge/terminal-trees-r23.md`.

**No product code was edited.** `corpus/SOURCES.md`, `corpus/knowledge/*`, `tools/`, `fixtures`
and every other seat's files were not touched. The only lane-repo write is this report; the
per-seat `w1/out/SrcFoot/` directory was **not** created because my item did not ask for it, so
all fetched bytes live outside the lane under `/tmp/footsrc/` and are reproducible from the
pinned URLs and digests recorded below. No foot binary was launched, no signal was sent to any
process, no host configuration was used as a claim source, and the host was not modified.

## Verdict

**PASS (advice + evidence).** 10 version-pinned foot sources were opened at tag `1.28.0`
(tag object `3d97bba53072ff90433ff75617f4a8e034529b57`, peeled commit
`ab33c9a19d626f8d0ac0bd1adfdba21946ada948`), each verified byte-identical to the tag archive
copy; 1 further upstream source (the upstream foot **wiki** repository) was opened at a pinned
commit `2475351ace3c8a618a3f2b8a7a486e987d125e07`. 5 documentary route claims were extracted
with located quotes, and **11 `SOURCES.md` rows** (all `mined`) plus **5 claim rows** are
drafted below. Nothing was landed here; the integration owner (MadoR23) owns landing and
running the C2 counter.

## Upstream pin

| item | value |
|---|---|
| repository | `dnkl/foot` (codeberg.org) |
| release tag | `1.28.0` |
| tag object sha | `3d97bba53072ff90433ff75617f4a8e034529b57` |
| peeled commit | `ab33c9a19d626f8d0ac0bd1adfdba21946ada948` |
| tagger date | 2026-09-02T11:02:54Z (commit date 2026-09-02T13:02:26+02:00, "meson: bump version to 1.28.0") |
| tag archive | `https://codeberg.org/dnkl/foot/archive/1.28.0.tar.gz` — 1,201,047 B, sha256 `4296be402b5684d049534598e69db92b918f92beac9dab76b585207045f0b037` |
| raw-byte form used for every repo row | `https://codeberg.org/dnkl/foot/raw/tag/1.28.0/<path>` (commit-pinned form `.../raw/commit/ab33c9a19d626f8d0ac0bd1adfdba21946ada948/<path>` verified byte-identical for `doc/foot.ini.5.scd`) |
| access date | 2026-10-22 |

Wiki (separate upstream repository, no tags): `https://codeberg.org/dnkl/foot.wiki.git`,
commit `2475351ace3c8a618a3f2b8a7a486e987d125e07` (2025-12-28T12:19:14+01:00), file `Home.md`.

## Sources opened (each with a located quote, ≤25 words)

| # | path at the pinned commit | sha256 | bytes | located quote (≤25 words) | anchor |
|---|---|---|---|---|---|
| 1 | `doc/foot.ini.5.scd` | `030014641676a18efff238a8954b5fb69e34dc9c80782236d3e85a824c11bc2b` | 76,756 | "foot will search for a configuration file in the following locations, in this order:" | :14-16 § DESCRIPTION |
| 2 | `doc/foot.1.scd` | `ad7d60aea563ae2f62290a83131e976948ad4384be1e4616872bab18a78f0c84` | 22,717 | "It also saves upstart time since the config has already been loaded and parsed" | :111-112 § OPTIONS (`--server`) |
| 3 | `doc/footclient.1.scd` | `a214ddafc671aa0b1f485c4aad5cb3f407fa31c871d24c2d39187c13d6eaa023` | 6,929 | "The following signals have special meaning in footclient:" | :200-202 § Signals |
| 4 | `README.md` | `874e192a7f322421e6c762c18dadd47239f7a5366bc47b966d12b516fd6f626d` | 24,450 | "**foot** can be configured by creating a file `$XDG_CONFIG_HOME/foot/foot.ini`" | :78-84 § Configuration |
| 5 | `foot.ini` (shipped template) | `1f3d6fa3f17292870d68bc39a2833d66300e0581684940ed0abc5e7e060763b5` | 9,158 | "# shell=$SHELL (if set, otherwise user's default shell from /etc/passwd)" | :3 (whole file is the commented template installed to /etc/xdg/foot/foot.ini, `meson.build:393`) |
| 6 | `config.c` | `bc8c134edc51e1225a583603888e3989d4f4a6acc794738bd03cd86418c3a0e1` | 136,321 | "/* First, check XDG_CONFIG_HOME (or .config, if unset) */" | :432-434 (`open_config` :421-473) |
| 7 | `main.c` | `d50034046894cde411f7c7d4fcbd8d9c65277e2cee97ea945e163b5a673217c2` | 23,528 | "if (sigaction(SIGHUP, &sig_ign, NULL) < 0 ||" | :683-684 (signal setup :675-687) |
| 8 | `terminal.c` | `27b3dfbf4cf953884632b1b798c876922fa2f11aaac68213ef1a42d4fb419544` | 148,115 | "argv[argc++] = term->conf->conf_path;" | :3821-3825 (`term_spawn_new` :3816-3831) |
| 9 | `server.c` | `bf5c2993a6c3f998b6666b667424f032062892dba19d560c4aa7f23c7e2e5631` | 18,715 | "conf = config_clone(server->conf);" | :371 (client instance :369-392) |
| 10 | `CHANGELOG.md` | `3d6c7d68224763e71f238234fbb50379ca7d2c6a66eb33ba66ae04c7334661f5` | 141,338 | "## 1.28.0" | :73 (release heading) |
| 11 | wiki `Home.md` @ `2475351ace3c8a618a3f2b8a7a486e987d125e07` | `78bd64dc27cff31a668cd3a0c58391905b9967e51eec5c0a309fe5e7035a5ff7` | 32,739 | "There is no way to dynamically reload the configuration." | :1014 § FAQ "How do I reload the configuration?" (:1011-1015) |

Extra located quotes used by the claim rows below, all from the same pinned bytes:

- `doc/foot.ini.5.scd:17-18` — "XDG_CONFIG_HOME/foot/foot.ini (defaulting to $HOME/.config/foot/foot.ini if unset)".
- `doc/foot.ini.5.scd:19-20` — "XDG_CONFIG_DIRS/foot/foot.ini (defaulting to /etc/xdg/foot/foot.ini if unset)".
- `doc/foot.ini.5.scd:9-11` — "*foot* uses the standard _unix configuration format_, with section based key/value pairs."
- `doc/foot.ini.5.scd:25-27` — "Options are set using KEY=VALUE pairs:".
- `doc/foot.ini.5.scd:31-33` — "Empty values (*KEY=*) are not supported. String options do allow the empty string to be set, but it must be quoted".
- `doc/foot.ini.5.scd:110-112` — "*include* Absolute path to configuration file to import."
- `doc/foot.ini.5.scd:113-115` — "The import file has its own section scope."
- `doc/foot.ini.5.scd:117` — "The path must be an absolute path, or start with *~/*."
- `doc/foot.ini.5.scd:120` — "Nested imports are allowed."
- `doc/foot.ini.5.scd:22-23` — "An example configuration file containing all options with their default value commented out will usually be installed to /etc/xdg/foot/foot.ini."
- `doc/foot.ini.5.scd:390-393` — "Use the *color-theme-switch-dark*, *color-theme-switch-light* and *color-theme-toggle* key bindings to switch between the two themes at runtime".
- `doc/foot.1.scd:27-31` — "*-c*,*--config*=_PATH_ Path to configuration file, see *foot.ini*(5) for details." and "The configuration file is automatically passed to new terminals spawned via *spawn-terminal*".
- `doc/foot.1.scd:33-35` — "*-C*,*--check-config* Verify configuration and then exit with 0 if ok, otherwise exit with 230".
- `doc/foot.1.scd:104-112` — "Run as a server. In this mode, a single foot instance hosts multiple terminals (windows)."
- `doc/foot.1.scd:704-705` — "SIGUSR1: switch to the dark color theme (*[colors-dark]*)." and "SIGUSR2: switch to the light color theme (*[colors-light]*)."
- `doc/foot.1.scd:626` — "Foot will exit with code 230 if there is a failure in foot itself."
- `doc/footclient.1.scd:204-205` — "SIGUSR1: switch to the dark color theme (*[colors-dark]*)."
- `config.c:434` — "path = xstrjoin(xdg_config_home, \"/foot/foot.ini\");".
- `config.c:449-461` — "for (const char *conf_dir = strtok(xdg_config_dirs_copy, \":\");" and "path = xstrjoin(conf_dir, \"/foot/foot.ini\");".
- `config.c:909-911` — "if (streq(key, \"include\")) {" and "Absolute path to configuration file to import." (comment-free code path).
- `config.c:921` — "_include_path = xstrjoin3(home_dir, \"/\", value + 2);" (the `~/` expansion).
- `config.c:926-927` — "if (include_path[0] != '/') {" / "LOG_CONTEXTUAL_ERR(\"not an absolute path\");".
- `config.c:944` — "LOG_INFO(\"imported sub-configuration from %s\", include_path);".
- `config.c:3501-3506` — "config_load(struct config *conf, char *conf_path," — the single load entry point.
- `config.c:3712-3723` — "if (conf_path != NULL) {" … "conf_file = open_config();" — an explicit `--config` path bypasses the search entirely.
- `main.c:539-540` — "bool conf_successful = config_load(" — the only startup load call.
- `main.c:681-687` — "struct sigaction sig_ign = {.sa_handler = SIG_IGN};" — SIGHUP and SIGPIPE are ignored.
- `terminal.c:3822-3825` — "if (term->conf->conf_path != NULL) {" / "argv[argc++] = \"--config\";".
- `server.c:392-393` — "term_init(conf != NULL ? conf : server->conf," — a server-mode client inherits the server's already-parsed config.
- `CHANGELOG.md:112-118` — "`[colors]` and `[colors2]` config sections, and the corresponding `color-theme-switch-1` and `color-theme-switch-2` key bindings." removed in 1.28.0.
- wiki `Home.md:1011-1015` — "Restart foot. If you are running foot in server mode, you **must** restart the server."
- wiki `Home.md:1016-1020` — "For theme switching, there is builtin support (since 1.23.0) for switching between **two** themes".

### Sources opened but not registered as rows

- `doc/foot-ctlseqs.7.scd`, `doc/foot.info`, `completions/`, `themes/`, `tests/`, `meson.build`
  (except the `:393` install line quoted inside row 5's anchor) were listed via the Codeberg
  contents API and the tag archive; they carry no config-route claim and are not registered.
- The wiki `Joypixels`, `Performance`, `_Footer`, `_Sidebar` pages (listed via
  `https://codeberg.org/api/v1/repos/dnkl/foot/wiki/pages`) were not opened: they carry no
  config-path, format, include or reload statement. They are recorded here as **unopened leads**.

### Unopened

- `https://codeberg.org/dnkl/foot.wiki/raw/commit/2475351ace3c8a618a3f2b8a7a486e987d125e07/Home.md`
  → **404** (11 B "Not found."). The bytes were obtained instead by cloning the upstream wiki
  repository and reading the pinned commit's blob (`git show 2475351...:Home.md`), which is the
  same object the wiki serves. The 404 is recorded as an unopened *URL*, not as an unopened
  source.
- `https://codeberg.org/dnkl/foot.wiki/raw/branch/master/Home.md` → **404** (same reason).
- `https://codeberg.org/dnkl/foot.wiki/src/commit/2475351.../Home.md` → **200 but redirects** to
  the wiki page index (`?action=_pages`); the served HTML is a listing, not the `Home.md` blob.
  This is why S149's source cell points at the repository (`https://codeberg.org/dnkl/foot.wiki.git`)
  from which the blob was read, rather than at a per-file web URL.
- `https://codeberg.org/dnkl/foot/wiki/raw/branch/master/foot.md` → **404** (no such wiki page;
  the wiki has only 5 pages, listed above).
- The wiki's rendered page `https://codeberg.org/dnkl/foot/wiki/Home` was **opened** (101,178 B,
  sha256 `71dfa2326a51f8032307b52904f1d15f3eb763526e47ab541306981812abd6ba`) and used only to
  confirm that the served page contains the same reload answer as the pinned blob; the blob is
  the cited byte source.
- No captcha, bot challenge or access control was encountered on any fetch.

## Documentary route claims (5)

**F1 — config file search path and precedence (v1.28.0).**
With no `--config`, foot looks for `XDG_CONFIG_HOME/foot/foot.ini` (defaulting to
`$HOME/.config/foot/foot.ini` when `XDG_CONFIG_HOME` is unset) and then
`XDG_CONFIG_DIRS/foot/foot.ini` (defaulting to `/etc/xdg/foot/foot.ini` when `XDG_CONFIG_DIRS`
is unset), **in that order**. The implementation (`open_config`) opens the
`XDG_CONFIG_HOME` path first and, only if that open fails, walks the colon-separated
`XDG_CONFIG_DIRS` entries and takes the **first existing file**; the two are not merged, and
the search stops at the first hit. An explicit `--config=PATH` bypasses the search entirely
and that one file is parsed. Sources: S140, S145.
Bound: documented and implemented search order at one pinned release; nothing here is a
statement about this host, and the docs and the code agree at file granularity.

**F2 — file name and format (v1.28.0).**
The configuration file is named **`foot.ini`** and lives in the foot config directory. Format:
the standard unix configuration format with section-based key/value pairs; the default section
is normally unnamed but may be written explicitly as `[main]`; options are `KEY=VALUE` pairs;
empty values are not supported, except that a string option may be set to the empty string when
quoted (`KEY=""`); a line beginning with `#` is a comment. The upstream tree ships a
fully-commented example file (`foot.ini`) that is installed to `/etc/xdg/foot/foot.ini`.
Sources: S140, S144, S145.
Bound: static format facts at the pinned tag; the parser accepts a section prefix and a
trailing `#` comment after the value, which is documented only implicitly.

**F3 — include / import mechanism (v1.28.0).**
The `[main]` section accepts an `include` key whose value is the path of another configuration
file to import. The path must be absolute or start with `~/` (the code expands `~/` against
`$HOME` and rejects anything else with "not an absolute path"); only one path per directive is
allowed, multiple `include` directives are allowed, and nested imports are allowed. The
imported file has **its own section scope**: the including file is back in the default section
after the include, whatever section the included file ended in. An import that cannot be opened
is an error. Sources: S140, S145.
Bound: parser-level facts at the pinned tag; they do not say that any particular host
`foot.ini` uses an include, and no include was executed here.

**F4 — how a running instance reloads its config (v1.28.0): it does not.**
Upstream states it outright: "Restart foot. If you are running foot in server mode, you
**must** restart the server. There is no way to dynamically reload the configuration." The
1.28.0 code agrees: the config is parsed exactly once at startup (`config_load` is called once
from `main.c`); **SIGHUP is explicitly ignored** (`SIG_IGN` for SIGHUP and SIGPIPE), so a
hangup cannot trigger a reload; and the only two signals foot handles, SIGUSR1 and SIGUSR2,
switch the **colour theme** (`[colors-dark]` / `[colors-light]`) and nothing else. There is no
reload keybinding, no `reload-config` option and no inotify/file-watch anywhere in the 1.28.0
tree (the only `reload`-named symbols in the source are font and cursor-theme reloads). The
practical routes are therefore **restart the foot process**, or **start a new terminal**: the
`spawn-terminal` action execs a fresh `foot --config <path>` process, so that new process
re-reads the file while the running one keeps the config it parsed at startup. Sources: S141,
S146, S147, S149.
Bound: the reload statement is upstream's own text in the wiki, which is a **separate upstream
repository pinned at a commit dated 2025-12-28**, not at the 1.28.0 tag; the code evidence
(rows S146, S147, S141) is tag-pinned and independently shows that no dynamic reload exists at
1.28.0. No signal was sent and no restart was performed here.

**F5 — validating a config, and the server-mode caveat (v1.28.0).**
`foot --check-config` "Verify configuration and then exit with 0 if ok, otherwise exit with
230" — that is the documented, non-mutating way to test a `foot.ini` (in that mode config
errors are fatal). In server mode (`foot --server`) the config is parsed **once** by the server
("the config has already been loaded and parsed") and every client terminal started through
that server inherits the server's already-parsed config; a `footclient` therefore does not read
`foot.ini` itself and cannot pick up an edited file. A changed `foot.ini` reaches a running
foot only through a fresh process that re-reads it. Sources: S141, S145, S146, S148.
Bound: documented and coded behaviour at the pinned tag; `--check-config` was **not** run here
(no foot binary exists on this host), and no server was started.

## Draft `corpus/SOURCES.md` rows (exact 11-column shape, not landed)

Shape: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.
Ids are the next free numbers after the last registered row (`S122`), so the assignment's
`S###-TBD` placeholders resolve to `S140`–`S149` plus `S152`; the integrator may renumber on
landing. Every `source` cell names **foot** (the C2 counter requires the terminal name in that
cell), every row is `mined`, `opened 2026-10-22`, `recheck on-release`, and
`used-by corpus/knowledge/terminal-trees-r23.md`.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S140 | foot 1.28.0 foot.ini(5) manual page — https://codeberg.org/dnkl/foot/raw/tag/1.28.0/doc/foot.ini.5.scd | docs | A | foot configuration file: search path and precedence, file name and format, the include directive, and the absence of any documented reload route at tag 1.28.0 (released 2026-09-02) | doc/foot.ini.5.scd:9-33 § DESCRIPTION, :110-121 § SECTION main `include`, :390-393 § SECTION main `initial-color-theme` @ tag 1.28.0 = commit ab33c9a19d626f8d0ac0bd1adfdba21946ada948 (sha256 030014641676a18efff238a8954b5fb69e34dc9c80782236d3e85a824c11bc2b, 76756 B) | the file is foot.ini; it is searched for at XDG_CONFIG_HOME/foot/foot.ini then XDG_CONFIG_DIRS/foot/foot.ini in that order; format is section-based KEY=VALUE with # comments; include takes an absolute or ~/ path, one per directive, nested allowed, with its own section scope; no reload route is documented | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S141 | foot 1.28.0 foot(1) manual page — https://codeberg.org/dnkl/foot/raw/tag/1.28.0/doc/foot.1.scd | docs | A | the foot command line at tag 1.28.0: how a config path is chosen, how a config is validated, server mode, and the complete set of signals foot handles | doc/foot.1.scd:27-35 § OPTIONS `--config` and `--check-config`, :103-135 § OPTIONS `--server`, :700-712 § Signals, :624-629 § EXIT STATUS @ tag 1.28.0 = commit ab33c9a19d626f8d0ac0bd1adfdba21946ada948 (sha256 ad7d60aea563ae2f62290a83131e976948ad4384be1e4616872bab18a78f0c84, 22717 B) | `--config=PATH` names the config file and is passed on to terminals spawned via spawn-terminal; `--check-config` validates and exits 0 or 230; in server mode the config is already loaded and parsed by the server; the only signals are SIGUSR1 and SIGUSR2, which switch colour theme | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S142 | foot 1.28.0 footclient(1) manual page — https://codeberg.org/dnkl/foot/raw/tag/1.28.0/doc/footclient.1.scd | docs | A | the footclient command at tag 1.28.0: it takes no config file of its own and only reacts to the theme-switch signals | doc/footclient.1.scd:23-100 § OPTIONS, :200-213 § Signals @ tag 1.28.0 = commit ab33c9a19d626f8d0ac0bd1adfdba21946ada948 (sha256 a214ddafc671aa0b1f485c4aad5cb3f407fa31c871d24c2d39187c13d6eaa023, 6929 B) | footclient has no config-file option: a client terminal started against a server inherits the server's config; SIGUSR1 and SIGUSR2 sent to a client change that instance's theme only | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S143 | foot 1.28.0 README — https://codeberg.org/dnkl/foot/raw/tag/1.28.0/README.md | docs | A | the user-facing pointer to the foot configuration file and to the man page at tag 1.28.0 | README.md:78-86 § Configuration @ tag 1.28.0 = commit ab33c9a19d626f8d0ac0bd1adfdba21946ada948 (sha256 874e192a7f322421e6c762c18dadd47239f7a5366bc47b966d12b516fd6f626d, 24450 B) | the config file is $XDG_CONFIG_HOME/foot/foot.ini defaulting to ~/.config/foot/foot.ini; a template is expected at /etc/xdg/foot/foot.ini; the man page foot.ini(5) is the reference | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S144 | foot 1.28.0 shipped example configuration — https://codeberg.org/dnkl/foot/raw/tag/1.28.0/foot.ini | code | A | the fully commented template foot installs as /etc/xdg/foot/foot.ini at tag 1.28.0, showing the file format and the section names actually in use | foot.ini:1-5 header, :110 `[colors-dark]`, :198 `[key-bindings]`; installed by meson.build:393 `install_data('foot.ini', install_dir: join_paths(get_option('sysconfdir'), 'xdg', 'foot'))` @ tag 1.28.0 = commit ab33c9a19d626f8d0ac0bd1adfdba21946ada948 (sha256 1f3d6fa3f17292870d68bc39a2833d66300e0581684940ed0abc5e7e060763b5, 9158 B) | every option is present commented out with its default; the file is a KEY=VALUE list under section headers such as [colors-dark] and [key-bindings]; this is the system-wide default foot reads from /etc/xdg/foot | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S145 | foot 1.28.0 configuration loader — https://codeberg.org/dnkl/foot/raw/tag/1.28.0/config.c | code | A | the implemented config search order, the include directive semantics, and the single load entry point at tag 1.28.0 | open_config :421-473 (XDG_CONFIG_HOME :432-434, XDG_CONFIG_DIRS loop :449-461), include branch :909-945 (`~/` expansion :921, absolute-path check :926-927, import log :944), config_load :3501-3520 and :3712-3723 @ tag 1.28.0 = commit ab33c9a19d626f8d0ac0bd1adfdba21946ada948 (sha256 bc8c134edc51e1225a583603888e3989d4f4a6acc794738bd03cd86418c3a0e1, 136321 B) | XDG_CONFIG_HOME is tried first and the first existing file wins; XDG_CONFIG_DIRS is walked colon-separated, one file only, no merge; an explicit conf_path bypasses the search; include must be absolute or ~/, nested includes are parsed recursively, each with its own section scope | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S146 | foot 1.28.0 startup and signal handling — https://codeberg.org/dnkl/foot/raw/tag/1.28.0/main.c | code | A | how a foot process handles signals and when its configuration is parsed, at tag 1.28.0 | config_load call :539-540 (the only startup load), signal registration :675-676 (SIGUSR1, SIGUSR2), SIGHUP and SIGPIPE ignored :681-687, SIGUSR handler fdm_sigusr :55-74 @ tag 1.28.0 = commit ab33c9a19d626f8d0ac0bd1adfdba21946ada948 (sha256 d50034046894cde411f7c7d4fcbd8d9c65277e2cee97ea945e163b5a673217c2, 23528 B) | the config is parsed once at startup; SIGHUP and SIGPIPE are set to SIG_IGN so a hangup cannot reload anything; SIGUSR1 and SIGUSR2 are the only handled signals and they switch the colour theme, they do not reload the config | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S147 | foot 1.28.0 spawn-terminal implementation — https://codeberg.org/dnkl/foot/raw/tag/1.28.0/terminal.c | code | A | what the spawn-terminal keybinding does to the configuration of the new terminal at tag 1.28.0 | term_spawn_new :3816-3831 (exe :3821, `--config` :3823, conf_path :3824), bound to BIND_ACTION_SPAWN_TERMINAL @ tag 1.28.0 = commit ab33c9a19d626f8d0ac0bd1adfdba21946ada948 (sha256 27b3dfbf4cf953884632b1b798c876922fa2f11aaac68213ef1a42d4fb419544, 148115 B) | spawn-terminal execs a new foot process with `--config <the path the running instance was started with>`; that new process re-reads the file, while the running instance keeps the config it parsed at startup | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S148 | foot 1.28.0 server mode — https://codeberg.org/dnkl/foot/raw/tag/1.28.0/server.c | code | A | how a foot server shares its already-parsed configuration with client terminals at tag 1.28.0 | server_init :559-600, client instance creation :369-392 (config_clone(server->conf) :371, term_init(conf != NULL ? conf : server->conf) :392-393) @ tag 1.28.0 = commit ab33c9a19d626f8d0ac0bd1adfdba21946ada948 (sha256 bf5c2993a6c3f998b6666b667424f032062892dba19d560c4aa7f23c7e2e5631, 18715 B) | the server parses the config once and clones it per client; a client terminal inherits the server's parsed config, so an edited foot.ini cannot reach a server-hosted terminal until the server restarts | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S149 | upstream foot wiki FAQ (separate repository dnkl/foot.wiki, pinned commit) — https://codeberg.org/dnkl/foot.wiki.git (blob Home.md read from the pinned commit) | docs | A | foot's own statement of the reload route; upstream project wiki, NOT pinned to a release tag, and its colour-section names are stale against 1.28.0 | Home.md:1011-1015 § FAQ "How do I reload the configuration?" @ commit 2475351ace3c8a618a3f2b8a7a486e987d125e07 (sha256 78bd64dc27cff31a668cd3a0c58391905b9967e51eec5c0a309fe5e7035a5ff7, 32739 B, fetched as a git blob from https://codeberg.org/dnkl/foot.wiki.git — the wiki's own raw and src routes return 404 / redirect to the page index) | foot cannot reload its configuration dynamically: restart foot, and in server mode restart the server; the only runtime change is colour-theme switching, which since 1.28.0 is spelled [colors-dark] and [colors-light], not the [colors]/[colors2] this older wiki page names | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S152 | foot 1.28.0 changelog — https://codeberg.org/dnkl/foot/raw/tag/1.28.0/CHANGELOG.md | docs | A | the identity of the pinned tag and the 1.28.0 removal of the older colour-section and keybinding names that the upstream wiki still uses | CHANGELOG.md:73 § 1.28.0, :110-118 § Removed (`[colors]`, `[colors2]`, `color-theme-switch-1`, `color-theme-switch-2` removed; replaced by `[colors-dark]`, `[colors-light]`, `color-theme-switch-dark`, `color-theme-switch-light`) @ tag 1.28.0 = commit ab33c9a19d626f8d0ac0bd1adfdba21946ada948 (sha256 3d6c7d68224763e71f238234fbb50379ca7d2c6a66eb33ba66ae04c7334661f5, 141338 B) | the pinned bytes belong to foot 1.28.0; that release removed the colour-section names the wiki FAQ still uses, so the wiki's reload answer is the durable part and its theme spelling is not | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |

Draft note for the registry foot: `S149` is the only row whose bytes are **not** pinned to the
1.28.0 release — it is the upstream project's own wiki repository pinned at commit
`2475351ace3c8a618a3f2b8a7a486e987d125e07` (2025-12-28). It is registered `mined` only for the
reload route, which the tag-pinned rows S141/S146/S147 independently corroborate; the stale
`[colors]`/`[colors2]` spelling in that page is corrected by S152 and is not claimed.

## Draft claim rows for `corpus/knowledge/terminal-trees-r23.md`

Shape (counter **v2**, the tightened one in the lane at
`4de44647f93bfd25ed5c979f61ff016b50456549`): the first cell must be exactly the terminal
(backticks allowed); **one cell must name the host tree `~/.config/foot/`**; and every cited
`S###` must resolve to an 11-cell `corpus/SOURCES.md` row that is `mined`, opened `2026-10-22`,
whose `source` cell names **foot** as a whole word, names **neither kitty nor ghostty**, and
points at `codeberg.org/dnkl/foot`, and whose `used-by` cell names
`corpus/knowledge/terminal-trees-r23.md`. All rows below cite only the foot rows drafted above;
each of those source cells names foot as a whole word, names no other terminal, and carries the
`codeberg.org/dnkl/foot` upstream URL.

| terminal | host tree | claim | evidence (pinned at foot 1.28.0) | sources | bound |
|---|---|---|---|---|---|
| `foot` | `~/.config/foot/` | foot reads its configuration from `XDG_CONFIG_HOME/foot/foot.ini` (defaulting to `$HOME/.config/foot/foot.ini`) and then `XDG_CONFIG_DIRS/foot/foot.ini` (defaulting to `/etc/xdg/foot/foot.ini`), in that order; the first existing file is used, the two are not merged, and `--config=PATH` bypasses the search | `doc/foot.ini.5.scd:14-20` § DESCRIPTION; `config.c:421-473` (`open_config`), `config.c:3712-3723` | S140, S145 | documented and implemented order at one tag; the host-tree cell names the tree this row routes, it is not a claim that this host's file was read |
| `foot` | `~/.config/foot/` | the config file is named `foot.ini`; it uses the standard unix configuration format with section-based KEY=VALUE pairs, an unnamed default section that may be written as `[main]`, `#` line comments, and no empty values except a quoted empty string for string options | `doc/foot.ini.5.scd:9-33` § DESCRIPTION; `foot.ini:1-5,110,198` (shipped template) | S140, S144, S145 | static format facts at the pinned tag; a trailing `#` comment after a value is accepted by the parser but only implicit in the docs |
| `foot` | `~/.config/foot/` | the `[main]` section accepts an `include` key that imports another config file; the path must be absolute or start with `~/`, one path per directive, multiple directives and nested imports are allowed, and the imported file has its own section scope so the including file returns to the default section afterwards | `doc/foot.ini.5.scd:110-121` § SECTION main `include`; `config.c:909-945` | S140, S145 | parser-level facts at the pinned tag; whether any host foot.ini uses an include is a host claim outside this row |
| `foot` | `~/.config/foot/` | a running foot cannot reload its configuration: the config is parsed once at startup, SIGHUP is explicitly ignored, the only handled signals (SIGUSR1, SIGUSR2) switch the colour theme, and there is no reload keybinding or file watch; upstream's own answer is to restart foot, and in server mode to restart the server | `main.c:539-540,675-687`; `doc/foot.1.scd:700-712` § Signals; `terminal.c:3816-3831` (`spawn-terminal` execs a new `foot --config <path>`); wiki `Home.md:1011-1015` | S141, S146, S147, S149 | documented and coded at the pinned tag; the wiki page is pinned at its own 2025-12-28 commit, not at the tag, and its `[colors]`/`[colors2]` spelling is stale for 1.28.0; no signal was sent and no restart was performed |
| `foot` | `~/.config/foot/` | `foot --check-config` validates a config and exits 0 or 230 without starting a terminal; in server mode the config is parsed once by the server and every client terminal inherits that parsed config, so an edited foot.ini reaches a running foot only through a new process that re-reads it | `doc/foot.1.scd:33-35` § OPTIONS, :103-112; `config.c:3501-3506,3712-3723`; `server.c:369-392`; `terminal.c:3816-3831` | S141, S145, S146, S148 | documented and coded at the pinned tag; `--check-config` was not run here — no foot binary is installed on this host |

Integration notes for the owner:

- The note file must exist at the landed revision for the counter to score; the counter
  (`python3 -I .ufo/waves/round-23/c2/count.py REV`) requires the note's rows to cite `S###`
  tokens that resolve in `corpus/SOURCES.md` at the same revision. At the current lane HEAD
  (`4de44647f93bfd25ed5c979f61ff016b50456549`) the note does not exist and the **v2** counter
  reports `{"note_present": false, "count": "0/3"}` (observed, exit 1 — see below).
- The counter is **v2** (`counter_version: 2` in its own output). v2's per-row requirements
  are met by the drafts above: exact first cell `foot`, a `~/.config/foot/` cell, and cited
  `S###` rows that are `mined` / opened `2026-10-22` / name foot as a whole word in the
  `source` cell / name no other terminal / carry `codeberg.org/dnkl/foot` / have
  `used-by = corpus/knowledge/terminal-trees-r23.md`. If the integrator renumbers, the
  `sources` cells of the note rows must be renumbered in step.
- Row shape is machine-checked: exactly 11 pipe-separated cells, `status` in cell 8 and
  `opened` in cell 9, and no literal `|` inside a cell.
- The foot rows count for foot only if the note's first cell is exactly `foot` (backticks
  allowed).
- Id bands agreed across the three C2 source seats by direct peer exchange (not by reading the
  other seats' files): kitty **S123–S133**, ghostty **S134–S139** plus **S150–S151**, foot
  **S140–S149** plus **S152**. No id is claimed twice.
- Cross-seat convergence on v2 (reported to me directly by the other two seats, 2026-10-22):
  all three seats independently adapted their drafts to `counter_version: 2` and each ran the
  lane's own v2 counter in its own throwaway clone with only its own rows present, each
  scoring its own terminal as counted (`1/3`, exit 1 only because the other two terminals are
  absent from that clone). Kitty reported 9 mined rows passing `source_ok` (its 10th row stays
  `queued` and supports no claim); ghostty reported 8 counted S-ids. Neither seat landed
  anything. So the three drafts are mutually compatible and individually v2-clean; the
  integrator's landed run is the one that produces 3/3.

### Shape self-check (observed, on my draft rows only)

**Counter-version note.** The lane's `c2/count.py` was **tightened from v1 to v2 mid-round**
(the lane commit `4de4464` "round-23: tighten C2/C3 counters and record registration
clarifications", committed before any after-measurement). v2 adds three requirements that the
drafts above now satisfy: the note row must contain a cell naming the host tree
`~/.config/<terminal>/`; the registry row's `source` cell must name the terminal as a **whole
word** and must **not** name either of the other two terminals; and that same `source` cell
must point at the terminal's upstream host (`codeberg.org/dnkl/foot` for foot). The `used-by`
cell must name `corpus/knowledge/terminal-trees-r23.md` (all foot rows do). My earlier v1-era
draft of the claim rows lacked the host-tree cell; it has been added.

I ran the **actual lane counter** against a throwaway simulation: a fresh clone of the lane at
HEAD (`/tmp/footsim`, `git clone -q <lane>`), my 11 draft source rows appended to
`corpus/SOURCES.md`, and my 5 draft note rows written to
`corpus/knowledge/terminal-trees-r23.md`, committed **in the clone only** and measured with
`python3 -I .ufo/waves/round-23/c2/count.py <sim-rev>`:

```
{"rev": "8fdccac93b99cc7f3fff12baf4c04f9da6004119", "counter_version": 2,
 "note_present": true,
 "terminals": {"foot": ["S140","S141","S144","S145","S146","S147","S148","S149"],
               "kitty": [], "ghostty": []},
 "count": "1/3"}
```

So with only my foot material landed (the other two seats' rows absent from the simulation),
the **real v2 counter scores foot as counted**; `kitty` and `ghostty` are empty only because
their seats' drafts are not in the simulation. The lane repo itself was not modified — the
simulation lived entirely in `/tmp/footsim`, which has been removed afterwards.

A second, independent check re-implemented the v2 registry parser and note matcher over the
two draft tables in this report (the landed `SOURCES.md` was not written and not modified):

```
11 source rows parsed; every row: cells == 11, status mined, opened 2026-10-22,
  recheck on-release, "foot" a whole word in the source cell, no other terminal named,
  upstream codeberg.org/dnkl/foot present, used-by names terminal-trees-r23.md
5 claim rows parsed; first cell `foot` in all five; a ~/.config/foot/ cell in all five;
  counted S-ids per row:
  S140, S145 | S140, S144, S145 | S140, S145 | S141, S146, S147, S149 | S141, S145, S146, S148
```

Both checks are parses/measures of **my draft text in a throwaway copy**, not a measurement of
the counter at a landed revision in the lane; the integrator's own run is the one that counts.

## Exact commands run

```
curl -sS -m 40 "https://codeberg.org/api/v1/repos/dnkl/foot/tags?limit=15"
curl -sS -m 40 "https://codeberg.org/api/v1/repos/dnkl/foot/git/refs/tags/1.28.0"
curl -sS -m 40 "https://codeberg.org/api/v1/repos/dnkl/foot/git/tags/3d97bba53072ff90433ff75617f4a8e034529b57"
curl -sS -m 40 "https://codeberg.org/api/v1/repos/dnkl/foot/contents/doc?ref=1.28.0"
curl -sSL -m 120 -o foot-1.28.0.tar.gz "https://codeberg.org/dnkl/foot/archive/1.28.0.tar.gz"
tar xzf foot-1.28.0.tar.gz                      # -> foot/
curl -sS -m 60 -O "https://codeberg.org/dnkl/foot/raw/tag/1.28.0/<path>"        # for every registered file
curl -sS -m 60 -o cmt_footini5.scd "https://codeberg.org/dnkl/foot/raw/commit/ab33c9a19d626f8d0ac0bd1adfdba21946ada948/doc/foot.ini.5.scd"
sha256sum <each fetched file>
diff -q <fetched raw file> foot/<same path>    # all identical
git clone -q --filter=blob:none https://codeberg.org/dnkl/foot.wiki.git footwiki
git -C footwiki show 2475351ace3c8a618a3f2b8a7a486e987d125e07:Home.md > wiki-Home-pinned.md
sha256sum wiki-Home-pinned.md
curl -sS -m 40 "https://codeberg.org/api/v1/repos/dnkl/foot/wiki/pages"          # 5 titles, none config-related
curl -sSL -m 45 -o /dev/null "https://codeberg.org/dnkl/foot.wiki/raw/commit/2475351.../Home.md"   # 404
curl -sSL -m 45 -o /dev/null "https://codeberg.org/dnkl/foot.wiki/raw/branch/master/Home.md"      # 404
curl -sSL -m 45 -o wt2.html "https://codeberg.org/dnkl/foot.wiki/src/branch/master/Home.md"        # 200 -> page index
curl -sSL -m 45 -o wiki-home.html "https://codeberg.org/dnkl/foot/wiki/Home"                       # 200 rendered page
curl -sSL -m 45 -o /dev/null "https://codeberg.org/dnkl/foot/wiki/raw/branch/master/foot.md"        # 404
pacman -Q foot ; pacman -Qs foot ; ls -l /usr/bin/foot                          # host probe, foot not installed
git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD ; git log --oneline -1
python3 -I .ufo/waves/round-23/c2/count.py HEAD          # -> 0/3, counter_version 2, exit 1

# counter-v2 dry run against my own draft rows, in a throwaway clone (lane untouched)
git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/footsim
#   (append the 11 draft source rows to corpus/SOURCES.md, write the 5 draft note rows to
#    corpus/knowledge/terminal-trees-r23.md inside /tmp/footsim only, commit there)
git -C /tmp/footsim add -A && git -C /tmp/footsim -c user.email=a@b -c user.name=c commit -qm "sim"
python3 -I /tmp/footsim/.ufo/waves/round-23/c2/count.py $(git -C /tmp/footsim rev-parse HEAD)
rm -rf /tmp/footsim
```

Read-only greps (`grep -n`) over the extracted tag tree located every quoted line; no upstream
file was modified, no foot binary was run, and no host file was changed.

## Evidence paths

| artifact | path |
|---|---|
| this report | `.ufo/waves/round-23/w1/reports/SrcFoot.md` |
| fetched upstream bytes (outside the lane, ephemeral) | `/tmp/footsrc/` — `foot/` (tag archive), `footwiki/` (wiki clone), `wiki-Home-pinned.md` (sha256 `78bd64dc…`), `wiki-home.html` (rendered wiki page, sha256 `71dfa232…`), `foot-1.28.0.tar.gz` (sha256 `4296be40…`) |
| re-fetch route | every file is retrievable at the URL and digest recorded in the two tables above; no receipt file was written into the lane because my item did not request one |

## Gates

- Lane bounds honoured: only this report file was written in the lane repo; `SOURCES.md`,
  `corpus/knowledge/*`, `tools/`, `fixtures` and every other seat's files were not touched, and
  `w1/out/SrcFoot/` was not created.
- Host safety: no package transaction (`pacman -Q`/`-Qs` reads only), no service or display
  change, no `~/.config` write, no foot process started or signalled; only ordinary HTTP fetches
  and local reads.
- Source discipline: every claim rests on bytes pinned to commit
  `ab33c9a19d626f8d0ac0bd1adfdba21946ada948` (tag `1.28.0`), each verified byte-identical to
  the tag archive copy; the one non-tag-pinned artifact (the upstream wiki) is registered with
  that limitation stated in its scope cell and is used only for the reload route.
- Nothing was installed or upgraded; no tooling change was needed.

## Out of scope (not claimed, not done)

- Host foot state: `foot` is **not installed** on this host (`pacman -Q foot` → "package 'foot'
  was not found"; no `/usr/bin/foot`), yet `~/.config/foot/foot.ini` (516 B, sha256
  `3e88354476f2682e7a1a0bc840d04e221e5c6a7312b3ee9dcf76ec16d0842e60`) exists and includes
  `~/.config/omarchy/current/theme/foot.ini` (378 B, sha256
  `d9c2e20e079a9314ec4cfd87370436ee0f34759a76bcdb0d5e1128ce672dcbeb`). Those bytes were read
  read-only for orientation and are **not** used as a claim source; the host-seat inventory owns
  them.
- Whether foot is the terminal this host launches, and any `xdg-terminal-exec` route — round-17
  territory owned by other rows.
- Running foot or footclient, sending SIGUSR1/SIGUSR2/SIGHUP to anything, `--check-config`,
  editing any config, starting a server.
- The other two terminals (kitty, ghostty) — separate seats.

## Open items and residual risk

1. The counter is the integrator's to run. Observed at the current lane HEAD
   (`4de44647f93bfd25ed5c979f61ff016b50456549`):
   `python3 -I .ufo/waves/round-23/c2/count.py HEAD` → `{"note_present": false, "count": "0/3",
   "terminals": {"foot": [], "kitty": [], "ghostty": []}}`, exit 1. That is the before value; it
   can only change when the SOURCES rows and the note rows land together.
2. `S149` (wiki) is upstream-primary but not release-pinned and its colour-section names are
   stale for 1.28.0 (S152 records the removal). If a later round wants a release-pinned reload
   statement, foot 1.28.0 has none — the tag-pinned evidence is the *absence* of any reload
   path (S146, S147), which is the durable form of the claim.
3. The tag archive bytes I compared against are from `https://codeberg.org/dnkl/foot/archive/
   1.28.0.tar.gz` (Codeberg's archive route, not a codeload mirror); the archive digest is
   recorded so it can be re-checked.
4. Id bands are peer-agreed by IRC exchange; if the integrator renumbers on landing, the
   claim-row `sources` cells must be renumbered in step — the `S###` tokens are the only link
   between the two files.

## Verdict line

**VERDICT: PASS** — 11 foot sources opened (10 pinned to tag 1.28.0 / commit
`ab33c9a19d626f8d0ac0bd1adfdba21946ada948`, 1 upstream wiki pinned at commit `2475351…`), 5
documentary route claims extracted with located ≤25-word quotes, 11 `mined` SOURCES rows and 5
note claim rows drafted in the exact 11-column shape; the lane's own **v2** C2 counter, run
against a throwaway clone carrying only this draft, scores **foot as counted** (`1/3` with the
other two seats absent); nothing landed, no host change, no terminal run.
