# RevengerUwsm — what `uwsm-app --` does to the resolver's environment

Seat: RevengerUwsm (round 47, w1 BUILD). Target: round-17 `[UNK]`, corpus/knowledge/terminal-route-r17.md:104-105
("`[UNK]` how it alters the environment"). All reads read-only; nothing launched, no pacman, no compositor
dispatch, no input injection. `xdg-terminal-exec` was run only with `--print-*` and only with
`XDG_CACHE_HOME=/fast/scratch/hyaku/mado-r47/RevengerUwsm/cache` (scratch now deleted).

## Verdict

`uwsm-app` **does not alter the environment at all**. It is a thin FIFO client for a systemd *user* service that
only *composes an argument vector*; the client then `eval`s it in its own shell, so the command runs as a child of
the client and inherits the caller's environment. The vector it evals is
`exec systemd-run --user --scope … -- xdg-terminal-exec …` — a transient **scope**, which systemd-run execs itself
"as parent process and will thus inherit the execution environment of the caller"
(systemd-run(1), man page line 30-33). Therefore, under the hotkey, `xdg-terminal-exec` sees the **compositor's**
environment, not the systemd user manager's and not a shell's — and not a modified copy of the compositor's.

## Chain, with code

| rung | evidence |
|---|---|
| hotkey `bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir=…` (~/.config/hypr/bindings.conf:2) | Hyprland runs the `exec` line under a shell; the `$(omarchy-cmd-terminal-cwd)` substitution requires one `[INFERENCE]` |
| `/usr/bin/uwsm-app` (POSIX sh; `set -e` at :13; sha256 `8be631ab…5a42bbc4c`, owned by `uwsm 0.27.1-1`) | `printf '\0%s' app "$@" > "$PIPE_IN"` (:172) — NUL-separated args to `$XDG_RUNTIME_DIR/uwsm-app-daemon-in` |
| daemon `wayland-wm-app-daemon.service`: `ExecStart=/usr/bin/uwsm aux app-daemon`, `EnvironmentFile=-%t/uwsm/env_session.conf` (unit :11,:14) → `/usr/share/uwsm/modules/uwsm/main.py` (`7dd63632…a976c72`) | `app_daemon()` calls `app(..., return_cmdline=True)` and sends `args_out = f"exec {shlex.join(app_args)}"` (main.py:3949) |
| `app()` composes (main.py:3731-3778): `final_args = ["systemd-run", "--user"]` (:3731) + `final_args.append("--scope")` (:3733) + `SourcePath`/`--slice=app-graphical.slice`/`--unit=app-…scope`/`--quiet`/`--collect` + `f"--working-directory={workdir}" if workdir else "--same-dir"` (:3774) + `--` + cmdline | default unit type is `"scope"` (main.py:2089/2091), overridable only by `-t` or `UWSM_APP_UNIT_TYPE` |
| client `eval "$CMDLINE"` (/usr/bin/uwsm-app:202) | runs in the client shell → caller's env |

The **only** place `uwsm-app` adds environment of its own is the *service* branch: `f"--setenv={var}={os.environ.get(var, '')}"`
(main.py:3738) over `Varnames.session_specific` = `{XDG_SEAT, XDG_SEAT_PATH, XDG_SESSION_ID, XDG_SESSION_PATH, XDG_VTNR}`
(main.py:146-152), taken from the **daemon's** env. That branch is not taken for the hotkey (see the live vector below);
even if it were, those five values equal the compositor's.

Two other env-sensitive points inside uwsm-app, both harmless here:
- `if cmdline and not which(cmdline[0]):` (main.py:3646) — the *daemon* pre-flights the command name against the
  **daemon's** PATH and errors before any resolver runs (a refusal, not a different selection).
- with `-T`, terminal-entry discovery `find_terminal_entry()` would run in the daemon env; the hotkey does not use
  `-T` (it names `xdg-terminal-exec` itself), so that path is dead here.

## Observed (host, read-only)

1. **The literal vector the daemon sent** — journal of the daemon, one line per press:
   `sent: exec systemd-run --user --scope --slice=app-graphical.slice '--unit=app-Hyprland-xdg\x2dterminal\x2dexec-8fafeb04.scope' --description=xdg-terminal-exec --quiet --collect --same-dir -- xdg-terminal-exec --dir=/home/vgpnk/Projects/shokunin`
   (journalctl --user -u wayland-wm-app-daemon.service, line 166 of `-o cat`). No `--setenv`, `--scope` present,
   `--same-dir` present, and the `--dir` value is the caller's cwd at press time.
2. **A live terminal from that path**: unit `app-Hyprland-xdg\x2dterminal\x2dexec-84981931.scope` is `active running`;
   its process (pid 3173, `comm`=alacritty) has cgroup
   `/user.slice/user-1000.slice/user@1000.service/app.slice/app-graphical.slice/app-Hyprland-xdg\x2dterminal\x2dexec-84981931.scope`,
   i.e. it *is* the scope child.
3. **The env it received** equals the compositor's exactly: `diff` of `/proc/1622/environ` (Hyprland) vs `/proc/3173/environ`,
   keys `PATH` + all `XDG_*` → **identical, 19 keys** (incl. `XDG_CURRENT_DESKTOP=Hyprland`,
   `XDG_DATA_DIRS=/usr/local/share:/usr/share`, `XDG_CACHE_HOME=/home/vgpnk/.cache`). cwd of both: `/home/vgpnk`.
4. **Manager env** (`systemctl --user show-environment`, XDG_*+PATH only) vs Hyprland: **identical, 19 keys**.
   Daemon `/proc/1813/environ` (XDG_*+PATH only) vs Hyprland: **identical**. So the three rungs agree; only a login
   shell differs (below).
5. **Shell vs compositor**: identical on every `XDG_*`; `PATH` differs — the compositor's 13 dirs are a strict subset of
   this shell's 20, the 7 shell-only dirs being fnm multishells ×2, mise node, `.minimax/bin`, `.minimax-code/bin`,
   `.grok/bin`, `.kimi-code/bin`.
6. **Cold-cache reproduction from a shell** (env of this shell, cache in scratch):
   `Alacritty.desktop` / `/home/vgpnk/.local/share/applications/Alacritty.desktop` / `alacritty` / `--working-directory=/home/vgpnk`, rc 0;
   `sha256sum /usr/bin/xdg-terminal-exec` = `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` (matches the pin).
7. **Effective-path-set identity**: the resolver's cache hash covers `XDG_CURRENT_DESKTOP` plus `LANG=C ls -LRl` of the
   config and applications dirs (xdg-terminal-exec:195, :200). The hash my cold run wrote in scratch
   (`d27b6b707781b8106c7b00390bdf2822`) equals the hash line of the host cache file `/home/vgpnk/.cache/xdg-terminal-exec`
   (which also records `alacritty`, the user override path, `Alacritty.desktop`). Same XDG_CURRENT_DESKTOP and same
   effective path set ⇒ same hash. (That cache file's mtime moved 17:42→18:49 while this wave ran — a concurrent writer —
   so I use its *content*, never its timestamp, as evidence.)

## Can the hotkey selection differ from a shell-run `--print-id`? Conditions

No, not by anything `uwsm-app` does. Divergence is possible only through inputs the wrapper passes through untouched:

1. **PATH asymmetry** — the resolver tests candidates with `command -v` (TryExec xdg-terminal-exec:936, Exec :964) and
   re-validates a cached command with `command -v "$xte__cached_cmd"` (:274), and PATH is *not* in the hash (:191-201).
   A terminal installed only on a shell-only PATH dir would be selected by a shell run and skipped under the hotkey.
   **Not the case today**: the only applicable candidate is `Alacritty.desktop`, the sole entry of
   `~/.config/xdg-terminals.list` (line 3; its header states "the first found and valid terminal will be used", line 2) and
   `alacritty` resolves to `/usr/bin/alacritty` under both PATHs; also `which`-identical for kitty/foot/wezterm/konsole/gnome-terminal/xfce4-terminal/xterm (all absent in both).
2. **Hash-covered env** — `XDG_CURRENT_DESKTOP` or the effective `XDG_CONFIG_HOME`/`XDG_CONFIG_DIRS`/`XDG_DATA_HOME`/`XDG_DATA_DIRS`
   path set (or the listings under it) differing between compositor and shell. Today identical (item 3/4/7). Conditions that
   would break it: a shell that re-exports `XDG_CURRENT_DESKTOP`/`XDG_DATA_DIRS`, or a second session of another desktop.
3. **Cache file location** — `XDG_CACHE_HOME` selects `$XDG_CACHE_HOME/xdg-terminal-exec` (xdg-terminal-exec:172-173), and a
   *reused* cache short-circuits selection (:274). A different `XDG_CACHE_HOME` can therefore print a stale id. Today all four
   captured envs (compositor, manager, daemon, this shell) set `XDG_CACHE_HOME=/home/vgpnk/.cache`, so they share one cache
   file; even where it is unset the default `${HOME}/.cache` lands on the same path. The warm result equals the cold result.
   Print modes do save the cache when it was not reused (`save_cache "$1" &` at :1455-1457), which is why C1 must keep
   `XDG_CACHE_HOME` in scratch.
4. **uwsm-app refusal** — if `xdg-terminal-exec` were reachable only from the shell's PATH, the *daemon* would refuse at
   main.py:3646 before the resolver runs. A launch failure, not a different verdict. Not the case (`/usr/bin`).
5. **cwd** — unchanged (the client never `chdir`s; `--same-dir`, main.py:3774). The resolver does not read `PWD`; its only cwd
   use is `cd "$XTE__DIRVAL"` before `exec "$@"` (:1496, :1499). Selection is cwd-independent.

## Closure of the round-17 [UNK]

"how `uwsm-app` alters the environment" → **it does not**; the launch is a transient user *scope* that inherits the caller's
environment (man systemd-run:30-33), and the observed scope child's environment is byte-identical to the compositor's for
every `PATH`/`XDG_*` key. The C1 host fact (`Alacritty.desktop`, user override path, `alacritty`, rc 0) is reproducible from
a plain shell with a redirected cache, and the only shell-vs-compositor delta (PATH) cannot change today's verdict because
the single applicable candidate lives in `/usr/bin`.

Scope note: this seat's evidence covers only the wrapper. The resolver's own selection rules, list-file order and entry
validation remain C2/other seats' ground.

## Receipts

- Read-only pins: `/usr/bin/uwsm-app` sha256 `8be631abfe3671f618ba4d4866ba85c4d79bd58c15a5afd9065e4cc5a42bbc4c`
  (owner `uwsm 0.27.1-1`), `/usr/share/uwsm/modules/uwsm/main.py` sha256 `7dd6363244c101c7a0e7641684e29b6a13905e98f9fc3a4c81421e536a976c72`
  (the module `/usr/bin/uwsm` imports), `/usr/bin/xdg-terminal-exec` sha256 `89f2be9a…3127ac` (matches the C1 pin).
- Every `file:line` locator above was re-checked mechanically: a 24-case script re-read each cited line and asserted the quoted
  substring is present → `locator check: 24/24 matched`. Locators themselves came from `grep -n`, never typed.
- The man-page locator (30-33) is within `man systemd-run | col -b` output, i.e. the DESCRIPTION paragraph
  "If a command is run as transient scope unit, it will be executed by systemd-run itself as parent process …".
- Env captures compared with `diff` on `PATH` + `XDG_*` keys only: Hyprland `/proc/1622/environ`, scope child
  `/proc/3173/environ`, app-daemon `/proc/1813/environ`, `systemctl --user show-environment`, this shell — 19 keys each.
- Safe-observation ledger: `xdg-terminal-exec` executed once, with `--print-id --print-path --print-cmd --dir=/home/vgpnk`
  and `XDG_CACHE_HOME` in scratch (rc 0). `uwsm-app`, `systemd-run`, `systemctl start/restart`, `hyprctl dispatch`,
  `uwsm` itself: **not run**. No pacman, no input injection, no GUI launch. Scratch `/fast/scratch/hyaku/mado-r47/RevengerUwsm`
  removed after copying.
