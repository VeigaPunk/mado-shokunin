# Walker live surface — `--help` / config read-only introspection (M7-3, round 7)

Lane: mado-shokunin. Assignment M7-3 (round 7): walker live surface via
read-only introspection — `walker --help*` / `--version` plus config and
binary file bytes — closing the round-5 open unknowns that this surface
can close. Measured 2026-10-14 18:20:44–18:23:13Z on host `plazir27`,
compositor session Hyprland PID 1203316 (instance time 1791994267).
Substrates READ-ONLY: nothing under `~/.config/`, `/etc/`,
`~/.local/share/` or the runtime dir was written; the sockets were
stat'd, never connected; the launcher UI was never opened; no
compositor state touched (boundary proof §7). Scratch: `/tmp/w7-m7-3/`
(ephemeral). Tag legend: **OBS** measured, **INF** inference with basis,
**UNK** not measurable this pass.

---

## §0 Claim and safety verdict

**Claim** — on this host `walker` 2.17.0 is installed and its help family
plus `--version` are provably state-free: the four executions left every
measured surface byte-identical (§7). The CLI surface is therefore a
legitimate read path — and the help text is additionally recoverable
from the binary **without executing it at all**, so the actor's own
documentation is file-byte verifiable.

Executed this pass (nothing else): `walker --version`, `walker --help`,
`walker --help-all`, `walker --help-gapplication`. Mutating verbs the
help advertises — `-q/--close` (closes a live walker), `-e/--exit`,
`-d/--dmenu` (starts a dmenu session), `activatable` D-Bus methods
(§4) — were **never** invoked. `--help` exited 0 with 0 B stderr
(harness wall time for the invocation ≤ 0.021 s).

## §1 Identity and pins (OBS)

| Object | Measured |
|---|---|
| binary | `/usr/bin/walker` (no symlink chain), owner pkg `walker 2.17.0-1`, sha256 `64826a8531eac525adfa3eff65548e93a6f7714feb1d3e13b4fa35bbcc3cfda0` |
| version | `walker --version` → bytes `32 2e 31 37 2e 30 0a` = `2.17.0\n`, 7 B, rc 0 |
| process | PID 1203471 `/usr/bin/walker --gapplication-service`, started `Wed 2026-10-14 13:11:08 -03` (unit `start_time`) |
| unit | `app-walker@autostart.service` (systemd-xdg-autostart generator, per round-5), `ExecStart` path `/usr/bin/walker` argv `/usr/bin/walker --gapplication-service`, `MainPID=1203471`, `ActiveState=active` / `SubState=running`; drop-in `~/.config/systemd/user/app-walker@autostart.service.d/restart.conf` (38 B) |
| autostart source | `~/.config/autostart/walker.desktop` sha256 `5cb9874eedbcb32c…`, `:4 Exec=walker --gapplication-service`; `diff`-clean vs `~/.local/share/omarchy/default/walker/walker.desktop` |
| elephant peer | PID 1203474 `elephant`, unit `elephant.service` `MainPID=1203474` active/running; no session-bus name (§4) |
| package files | `pacman -Ql walker` = 29 entries (10 dirs + `/usr/bin/walker` + `/etc/xdg/walker/config.toml` + `LICENSE` + 16 files under `/etc/xdg/walker/themes/default/`) — **no** man page, **no** `/usr/share/doc/walker` (0 `man|doc` hits); `/usr/bin/walker` is a plain file (root:root, 6,661,264 B, mtime 2026-07-26 21:42) |

The unit relation closes the help↔live loop: the argv the running
process carries is exactly the `--gapplication-service` option the help
text documents (§2).

## §2 CLI surface as measured (OBS, verbatim)

`walker --help` → 1,726 B stdout, **0 B stderr**, rc 0, sha256
`ca4820a827273f6a5827652c7411a8b8d72c3660a00d18714cdcef59d656cacc`,
33 lines, 26 option lines (`grep -cE '^  (-|--)'`):

```
Usage:
  walker [OPTION…]

Help Options:
  -?, --help                Show help options
  --help-all                Show all help options
  --help-gapplication       Show GApplication options

Application Options:
  -v, --version             show version
  -n, --nosearch            hide search input
  -N, --nohints             hide keybind hints
  -I, --inputonly           only show input. dmenu only.
  -x, --password            use as password input. sets dmenu automatically.
  -X, --selectsingle        auto-select single entry
  -i, --index               prints the selected index instead of its value. dmenu only.
  -m, --provider            exclusive provider to query
  -s, --set                 provider set to use
  -p, --placeholder         input placeholder.
  -h, --height              forced height. concerned with overall box. min 1. DONT USE SHORTHAND.
  --minheight               min height. concerned with scrolled content. min 1.
  --maxheight               max height. concerned with scrolled content. min 1.
  -c, --current             mark current value. dmenu only.
  -w, --width               forced width. concerned with overall box. min 1. DONT USE SHORTHAND.
  --minwidth                min width. concerned with scrolled content. min 1.
  --maxwidth                max width. concerned with scrolled content. min 1.
  -t, --theme               theme to use
  -d, --dmenu               dmenu
  -q, --close               closes walker when open
  -H, --hideqa              hides quick activation buttons
  -k, --keepopen            keep walker open after selection. only when using service. dmenu only.
  -e, --exit                exit after this dmenu call. only when using service. dmenu only

```

- `walker --help-all` adds the GApplication section (`--gapplication-service`
  "Enter GApplication service mode (use from D-Bus service files)") —
  1,867 B, sha256 `b513c43fc9b70393…`; `walker --help-gapplication`
  prints only that section (144 B, sha256 `0945536ca6e90c2a…`).
- **No `--config` option exists** (full text above; INF: the config path
  is not CLI-selectable — the binary carries a single `config.toml`
  filename token plus XDG_* env tokens, §3).
- The help text is **compiled into the binary as one concatenated blob**
  (offset ≈818,871 region, `strings -n 5` line 2336: the option
  descriptions run together, `…hide search inputhide keybind hints…`);
  no external help file ships (package list §1). Executing and reading
  the binary therefore agree byte-for-byte on the option descriptions —
  a spot-check cross-verifies the two read paths (§6.1/§6.2).
- `-q/--close`, `-e/--exit`, `-d/--dmenu` are mutating/session verbs and
  stay fenced for this lane (PROVINCE: never disturb a live session).

## §3 Config read surface (OBS, with INF marked)

**Layers re-measured** (round-5 `walker-deep.md` §2.1 stands):

| Layer | Object | This pass |
|---|---|---|
| L0 embedded default | compiled into `/usr/bin/walker` | `python3`: byte run at offset **784,064** still equals `/etc/xdg/walker/config.toml` **verbatim** (`match True`; same offset as round-5 §14.1) |
| L1 packaged | `/etc/xdg/walker/config.toml` | sha256 `5b4e47b7d2314bf8…`, 13,220 B, mtime 2026-07-26 21:42:11 -03 |
| L2 user | `~/.config/walker/config.toml` | sha256 `fecf71fa4253803e…`, 1,336 B, mtime 2026-10-03 17:44:32 -03; identical hash to `~/.local/share/omarchy/config/walker/config.toml` (stock copy) |
| L3 env/config-dir | binary tokens | see below |

**OBS** — the user file (49 L, read in full) carries the six overrides
from round-5 §2.4 unchanged: `force_keyboard_focus=true`,
`selection_wrap=true`, `theme="omarchy-default"`,
`additional_theme_location="~/.local/share/omarchy/default/walker/themes/"`,
`hide_action_hints=true`, `[keybinds] quick_activate=[]`,
`[columns] symbols=1`, `[providers] max_results=256`, `default=[desktopapplications,websearch]`,
six `[[providers.prefixes]]`, and one `[[emergencies]]` entry
(`text="Restart Walker"`, `command="omarchy-restart-walker"`). A
secret-shape scan (`grep -inE 'token|secret|password|api[_-]?key|bearer'`)
returns **no hits** — the live config is not secret-bearing.

**OBS — env token census of the binary** (airtight raw-byte greps):
- exactly **one** occurrence of `WALKER_` (6 bytes, offset **797,295**),
  sitting immediately after the `config.toml` filename token
  (offset 797,284) and before a Rust error string: the raw run is
  `…"visit_url" },\n]\nconfig.tomlWALKER_called \`Result::unwrap()\`…`.
- **no `WALKER_<NAME>` variable token exists anywhere** — the only match
  of `WALKER_[A-Za-z0-9_]*` is `WALKER_called`, i.e. the literal boundary
  is ambiguous (Rust rodata is not NUL-separated), and no enumerated
  walker-specific env variable name is compiled in.
- XDG env var names are present as one run (strings line 1841):
  `XDG_DATA_HOME XDG_CONFIG_HOME XDG_CACHE_HOME XDG_STATE_HOME
  XDG_DATA_DIRS XDG_CONFIG_DIRS XDG_RUNTIME_DIR`, together with the path
  fragments `~`, `.local/share`, `.cache`, `.local/state`, `.config`
  (dirs/xdg-crate style) — **INF**: the process resolves config/data
  paths from these variables at startup.
- `RUST_BACKTRACE` / `RUST_MIN_STACK` also appear (rust std runtime, not
  a walker surface).

**OBS — GSettings read surface**: the binary carries
`org.gnome.desktop.interface` + `settings-schema` + `color-scheme` +
`accent-color` (offset ≈818,930 run). Live read-only values on this
host: `gsettings get org.gnome.desktop.interface color-scheme` →
`'prefer-dark'`; `accent-color` → `'blue'` (schema present, 1 exact-name
match). No `gsettings set` was run.

**OBS — units declare no environment**: `systemctl --user show` with
`-p Environment -p EnvironmentFile` on both `app-walker@autostart.service`
and `elephant.service` printed an empty `Environment=` for each and **no**
`EnvironmentFile=` value (so L3 cannot come from the units; INF: it is
the login session, same as round-5 §1).

## §4 Live runtime surface (OBS)

**Sockets** (stat'd, never connected):

| Path | Type | Mode | Size | mtime (-03) |
|---|---|---|---|---|
| `$XDG_RUNTIME_DIR/walker/walker.sock` | socket | 755 `srwxr-xr-x` | 0 | 13:11:09.144101315 |
| `$XDG_RUNTIME_DIR/elephant/elephant.sock` | socket | 755 `srwxr-xr-x` | 0 | 13:11:09.110101284 |

(`$XDG_RUNTIME_DIR` = `/run/user/1000`; both parent dirs `drwxr-xr-x` 755,
owner `vgpnk:vgpnk`.) The mtimes equal the session start second (13:11:09
= 16:11:09 UTC) and were **identical before and after all probes**.
Path-construction token in the binary (offset 818,871):
`XDG_RUNTIME_DIRwalkerwalker.sock` — **INF**: socket path =
`$XDG_RUNTIME_DIR` + app-named subdir + fixed name.

**D-Bus** (identity + read-only introspection; no `Activate`/`Open`):

- `busctl --user list` → `dev.benz.walker` owner **PID 1203471** (= the
  walker PID), process `walker`, unique name `:1.23`, unit
  `user@1000.service`. `:1.23` is the same connection.
- `busctl --user introspect dev.benz.walker /dev/benz/walker` shows
  interfaces: `org.freedesktop.Application` (`Activate`,
  `ActivateAction`, `Open`), `org.gtk.Actions` (`List`, `Activate`,
  `Describe`, `DescribeAll`, `SetState`, `Changed` signal),
  `org.gtk.Application` (`Activate`, `CommandLine`, `Open`,
  `Busy=false` property), plus `org.freedesktop.DBus.{Introspectable,
  Peer, Properties}`.
- `busctl --user call dev.benz.walker /dev/benz/walker org.gtk.Actions
  List` → `as 0` — the GTK action list is **empty** (re-confirms round 3;
  §10 row below).
- **elephant holds no session-bus name**: `busctl --user list | grep -ci
  elephant` → 0. **OBS** absence ⇒ **INF**: elephant's IPC is the unix
  socket only; there is no D-Bus read path to the provider engine.

**Layer invariant** (read-only `hyprctl -j layers`): DP-1 level 0
`wallpaper` pid 1203358, level 2 `waybar` pid 1203352 — **no walker
namespace**, i.e. the launcher is closed (same as round-5/6). Stated as
the gate invariant: *if* a walker namespace ever appears, its pid must
equal the walker pid (1203471); absence is a NOTE, never a pass/fail
signal by itself (round-7 plan §(c)).

**Service-mode fallback message token** found file-byte:
`make sure 'walker --gapplication-service' is running!` — **INF**: the
dmenu path speaks to the running service over the socket; **OBS**: the
message names the exact argv the live process carries (§1).

## §5 Round-5 closure ledger (walker-deep.md §10 / §11)

### §10 Introspection ledger — re-measured

| Question | Round-5 | This pass | Evidence |
|---|---|---|---|
| Is walker running, how? | OBS | **OBS re-measured** | PID/unit/argv §1 |
| Is it open / where? | OBS (closed) | **OBS re-measured**: closed | layers §4 |
| D-Bus identity / actions? | OBS; `Actions.List` empty (r3) | **OBS extended**: owner pid == walker pid; full interface set; `List` = `as 0` | §4 |
| What config does it read? | OBS | **OBS extended**: no `--config` flag exists; L0/L1 byte-equality re-proven; env census | §2/§3 |
| What providers exist? | OBS/RUN | not re-measured here (elephant plane; read path `elephant listproviders`, round-5 §4.1) | — |
| What does it *render*? | UNK | **still UNK by constraint** (no screen read; launcher never opened) | — |
| Sockets protocol? | UNK | **still UNK by constraint** (never connected); path/mode/size/owner now pinned | §4 |

### §11 Unknowns — status after this pass

| # | Round-5 unknown | Status now | What is new / the residual barrier |
|---|---|---|---|
| 1 | theme/layout resolution order for partial themes | **sharpened, UNK** | exact fallback string `theme not found. using default theme.` and CSS failure string `Can't find stylesheet to import.` located; the 16 shipped `item_*.xml`/`layout.xml`/`preview.xml`/`style.css` files are the part set; order needs a live render |
| 2 | emergency trigger condition | **sharpened, UNK** | live config has one emergency (`Restart Walker` → `omarchy-restart-walker`); binary tokens `menus-emergency`, `is_emergency`, `struct EmergencyEntry with 2 elements`; the trigger path is still not observable read-only |
| 3 | `walker.sock` protocol / query API | **UNK (constraint)** | never connected; new: exact path/mode/size + path-construction token (§4) |
| 4 | `installed_providers` semantics | **UNK** | token appears only in the field-name run (round-5 §2.3); no file sets it; no CLI surface mentions it |
| 5 | `WALKER_` env-override surface | **sharpened to a precise census** | exactly one bare `WALKER_` literal (offset 797,295) adjacent to the `config.toml` token; **zero `WALKER_<NAME>` tokens**; help has no env section; units declare none. Residual UNK: whether the literal is used as a runtime prefix and which names would be read |
| 6 | unknown-key / parse-error behaviour | **sharpened, UNK** | embedded crate path `toml_parser-1.0.6+spec-1.1.0`; serde/toml error templates (`Unexpected missing field named `, ``unknown variant ` ``, `Expected string.`, `Expected integer`, `invalid filename`, `Failed to set loaded config`) and the `unknown_fields` token. Closing it needs a run against a mutated config — barred (the walker binary opens the launcher; write-only-to-scratch copy would still start UI/service mode) |
| 7 | `~` expansion in `additional_theme_location` | **UNK, token census negative** | no `shellexpand`/`tilde`/`home_dir`/`expand_path` token; dirs/xdg-crate `~` + `.config`-style fragments present; the live value keeps `~/…`; expansion semantics unexercised |
| 8 | elephant-side delimiter counterpart | **out of this surface** (elephant plane) — UNK | unchanged from round-5 §4.3 |
| 9 | rendered walker pixels | **UNK (constraint)** | no screen read, launcher never opened |
| 10 | `[providers.sets]` with a real set | **UNK** | help documents `-s, --set provider set to use`; error token `can't find specified set`; `struct ProviderSet with 2 elements`; no set defined in either layer |

**Errata route** — `walker-deep.md` §10/§11 errata were **not appended by
this lane** (assignment writes only this file). This ledger is the
substance for that append; the lane owning `walker-deep.md` should carry
it there, append-only. The round-7 plan's stage-(c) *gate wiring* (live
rows for sockets / D-Bus owner / layer invariant) is likewise not in
this file — this note is the measured surface it would cite.

## §6 Reproducible spot-checks

1. **Help capture is stable and compiled-in**:
   `timeout 10 walker --help | sha256sum` → `ca4820a827273f6a…` (rc 0,
   0 B stderr). File-byte twin:
   `strings -n 5 /usr/bin/walker | grep -c 'hide search input'` → 1
   (one concatenated description blob, offset ≈818,871 region).
2. **`WALKER_` census**: `grep -aob 'WALKER_' /usr/bin/walker` → single
   hit `797295`; `grep -aoE 'WALKER_[A-Za-z0-9_]*' /usr/bin/walker` →
   only `WALKER_called` (boundary ambiguity, see §3); no `WALKER_<NAME>`
   exists.
3. **Embedded default == packaged file** (round-5 §14.1 re-run):
   `python3 -c "b=open('/usr/bin/walker','rb').read();
   f=open('/etc/xdg/walker/config.toml','rb').read();
   i=b.find(b'force_keyboard_focus = false'); print(i,
   b[i:i+len(f)]==f)"` → `784064 True`.
4. **Empty GTK action list**: `busctl --user call dev.benz.walker
   /dev/benz/walker org.gtk.Actions List` → `as 0`.
5. **Sockets untouched**: `stat -c '%n %a %s %y'
   /run/user/1000/walker/walker.sock` → mode 755, size 0, mtime
   13:11:09.144101315 -03 (same value before/after; §7).
6. **GSettings read surface**: `gsettings get org.gnome.desktop.interface
   color-scheme` → `'prefer-dark'`; `accent-color` → `'blue'`.

## §7 Boundary proof (this pass)

Before snapshot 18:20:44Z, after snapshot 18:23:13Z, same probes:

| Surface | Before | After |
|---|---|---|
| `walker.sock` / `elephant.sock` mode·size·mtime | 755·0·13:11:09.144 / 755·0·13:11:09.110 | identical |
| walker pid / elephant pid | 1203471 / 1203474 | identical |
| `app-walker@autostart` / `elephant` `MainPID`·state | 1203471·active / 1203474·active | identical |
| `~/.config/walker/config.toml` sha256 | `fecf71fa4253803e…` | identical |
| `/etc/xdg/walker/config.toml` sha256 | `5b4e47b7d2314bf8…` | identical |
| `~/.config/autostart/walker.desktop` sha256 | `5cb9874eedbcb32c…` | identical |
| `find ~/.config/walker ~/.cache/walker ~/.local/share/walker ~/.local/state/walker $XDG_RUNTIME_DIR/{walker,elephant} -newermt '@1792002044'` | (baseline) | **empty** |
| `hyprctl -j layers` | wallpaper 1203358 / waybar 1203352 | identical |

Probes used (all read verbs): `which`, `readlink`, `pacman -Qo/-Ql`,
`walker --version/--help/--help-all/--help-gapplication`, `stat`, `find`,
`pgrep`, `systemctl --user show`, `busctl --user list/introspect/call
(List only)`, `hyprctl -j layers/instances`, `gsettings get`,
`sha256sum`, `strings`, `grep`, `python3`, `xxd`, `diff`. No `/proc`
environ read (barred); no strace attempted (a stronger proof is possible
if the environment permits ptrace).

## §8 Unknowns of this pass (kept, not inferred away)

1. Whether the bare `WALKER_` literal is a runtime env prefix and what
   names it would read — no execution with a set env was performed.
2. Whether `--help` behaves identically under a headless/no-session
   context — not tested (would need a different environment).
3. Rendered UI, socket protocol, GSettings *writes* by walker — unmeasured
   by constraint (no screen, no socket connect; only reads were set up).
4. Elephant version/identity was not re-measured this pass (out of the
   walker surface; round-5 §1 pins it at 2.21.0).
5. Whether the help blob's literal boundaries (option descriptions) are
   stable across rebuilds — only this build (`64826a85…`) is pinned.

## Freshness pointer (round 19, 2026-10-20)

- The walker version pins in this note (lines 19, 37, 38) are dated 2026-10-14 (the measurement window in line 6) and describe walker 2.17.0. On 2026-10-20 the host package moved to 2.17.2: `/var/log/pacman.log:2929` ([ref]); the host binary bytes were re-read this round and are recorded as S096 (sha256 `25240650…`, one `2.17.2` literal) [wave-2 corrected wording]. Current routing: corpus/knowledge/walker-route-r18.md.
- Version-bound, therefore dated to the 2.17.0 build: §1 binary sha256 `64826a85…`, owner pkg `walker 2.17.0-1`, the `--version` bytes; §1 package file list (29 entries) and packaged `/etc/xdg/walker/config.toml` (13,220 B, sha `5b4e47b7…`); §2 help text and its sha256 `ca4820a8…` with the help-all and gapplication captures; §3 L0 embedded-default equality at offset 784,064.
- Version-independent in kind, but host-state dated 2026-10-14: §3 user config `~/.config/walker/config.toml` (1,336 B, sha `fecf71fa…`) and its overrides; §3 GSettings values and unit environment; §4 PIDs, sockets, D-Bus owner and layer invariant; §7 boundary snapshot. None of these is re-asserted for 2026-10-20.
- Not re-measured live this round (host pause): behaviour of the 2.17.2 binary stays [UNK].

### Wave-2 corrections (round 19, append-only)

- S096 is a recorded mined row (landed in `df84807`); the host walker bytes were re-read this round (`/usr/bin/walker` sha256 `25240650…`, literal `2.17.2` at 856,302).
- The §2 help/capture digests are GLib-bound rather than walker-version-bound: walker's 838-byte option-description run is byte-identical between the 2.17.0 and 2.17.2 binaries (w1 DeltaWalkerCli, w2 AtkDeltaCli) while glib2 moved 2.88.3 → 2.90.1 (`/var/log/pacman.log:2554`); the rendered help bytes stay [UNK].
- The 29-entry package file list is version-invariant (both packages list the same 29 entries); only the packaged config content moved (13,220 B `5b4e47b7…` → 13,743 B `3c5c6867…`, [ref]). The §1 PIDs and unit state (lines 39-42) are dated 2026-10-14 like §3/§4/§7.
- Further delta sites (w2 ReviewDeltaCarry): the binary-offset claims at lines 130-132, 172, 229 and 249-258 describe the 2.17.0 binary (e.g. `WALKER_` 797,295 → 820,714; embedded default 784,064 → 806,960); they are dated like the version pins.
