# CritUwsm — detailed falsification record (round 47 w2)

Target: `w1/RevengerUwsm/report.md` — "`uwsm-app` **does not alter the environment at all** … `xdg-terminal-exec`
sees the compositor's environment". Seat question: is any selection-relevant variable different?

Verdict: **NOT FALSIFIED**. Details below, each item with the exact command run.

## 1. Resolver environment surface (from the pinned script)

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/fetch/xdg-terminal-exec`
(sha256 `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`; 1499 lines).

External env reads (grep `\$\(?\{?[A-Z][A-Z0-9_]*` + context review):

| variable | use | locator |
|---|---|---|
| `XDG_CURRENT_DESKTOP` | lowercased key; hash input; OnlyShowIn/NotShowIn | :1144, :195, :848/:857/:867/:876 |
| `XDG_CONFIG_HOME`, `HOME`, `XDG_CONFIG_DIRS` | config-file search paths | :148 |
| `XDG_DATA_DIRS` | distro-level config + applications dirs | :157 |
| `XDG_DATA_HOME`, `XDG_DATA_DIRS` | applications dirs | :166 |
| `XDG_CACHE_HOME` | cache file location | :172-173 |
| `PATH` | `command -v` for TryExec / Exec[0] / cached-cmd revalidation | :936, :964, :274 |
| `LC_ALL` | forced `C` around hash/config/entry reads | :183, :355, :972 |
| `LANG` | `LANG=C` inside the hash listing | :200 |
| `XTE_DEBUG`/`DEBUG` | debug toggle (logging only) | :61 |
| `XTE_EXECARG_COMPAT` | compat-mode default execarg | :1147 |
| `XTE_CACHE_ENABLED` | cache enable | :1172 |

No `PWD` read; cwd used only post-selection (`cd "$XTE__DIRVAL"` :1496, guard :1494).

## 2. Rung comparisons (today, read-only)

Commands:

    systemctl --user show-environment | grep -E '^(XDG_|PATH=)' | sort > manager-env
    tr '\0' '\n' < /proc/1622/environ | grep -E '^(XDG_|PATH=)' | sort > hyprland-env
    diff hyprland-env manager-env          # empty → identical 19 keys
    tr '\0' '\n' < /proc/1813/environ | grep -E '^(XDG_|PATH=)' | sort > daemon-env
    diff hyprland-env daemon-env          # empty → identical

- Hyprland pid is still 1622 (same instance as w1).
- Daemon pid is still 1813 (`/usr/bin/python3 /usr/bin/uwsm aux app-daemon`).
- Extra check: compositor env has `HOME=/home/vgpnk`, `LANG=en_US.UTF-8`, and no `XTE_*`, `DEBUG`,
  `DISPLAY`, `WAYLAND_DISPLAY`, `LC_*` → no hidden opt-in override differs.

## 3. The vector and its env path (read-only)

- Live journal (76 `sent:` lines captured): all `exec systemd-run --user --scope … --same-dir -- …`, none with
  `--setenv`. Resolver vector seen: `xdg-terminal-exec --dir=/home/vgpnk/Projects/shokunin`.
- `uwsm-app` client: writes `printf '\0%s' app "$@" > "$PIPE_IN"` (:172), reads pipe, `eval "$CMDLINE"` (:202).
  No export/setenv before eval → the command runs in the client's shell with the client's env.
- `main.py`: scope branch (`final_args.append("--scope")` :3733) appends no `--setenv`; service branch would add
  `f"--setenv={var}={os.environ.get(var, '')}"` (:3738) over `Varnames.session_specific` (:146-151) — never seen
  in the live vectors. Daemon preflight `which(cmdline[0])` (:3646) is a refusal, not a selection change.
- man systemd-run: "If a command is run as transient scope unit, it will be executed by systemd-run itself as
  parent process and will thus inherit the execution environment of the caller" (lines 30-32) — verified verbatim.

## 4. Empirical dual-PATH cold-cache test

Command (scratch `S=/fast/scratch/hyaku/mado-r47/CritUwsm`):

    PATH_A=$(tr '\0' '\n' < /proc/1622/environ | grep '^PATH=' | cut -d= -f2-)
    PATH_B=/usr/bin:/usr/local/bin
    for spec in "A|$PATH_A" "B|$PATH_B"; do
      p=${spec%%|*}; pv=${spec#*|}
      rm -rf "$S/cache$p"; mkdir -p "$S/cache$p"
      env -i PATH="$pv" HOME=/home/vgpnk XDG_CACHE_HOME="$S/cache$p" \
        XDG_CONFIG_HOME=/home/vgpnk/.config XDG_CONFIG_DIRS=/etc/xdg \
        XDG_DATA_HOME=/home/vgpnk/.local/share XDG_DATA_DIRS=/usr/local/share:/usr/share \
        XDG_CURRENT_DESKTOP=Hyprland XDG_RUNTIME_DIR=/run/user/1000 \
        /bin/sh <lane>/.ufo/waves/round-47/fetch/xdg-terminal-exec \
        --print-id --print-path --print-cmd --dir=/home/vgpnk/Projects/shokunin \
        > "$S/out$p" 2> "$S/err$p"; echo "rc=$?" >> "$S/out$p"
    done
    diff "$S/outA" "$S/outB"     # identical

Output (both): `Alacritty.desktop` / `/home/vgpnk/.local/share/applications/Alacritty.desktop` /
`alacritty` / `--working-directory=/home/vgpnk/Projects/shokunin` / `rc=0`. Written cache hash
`d27b6b707781b8106c7b00390bdf2822` (matches w1 item 7). stderr empty in both.

## 5. Candidate universe

- `~/.config/xdg-terminals.list` line 3 = sole entry `Alacritty.desktop` (the only preference list entry).
- TerminalEmulator desktop entries on the host: exactly `Alacritty.desktop` (user copy
  `~/.local/share/applications/` and system copy `/usr/share/applications/`); user copy wins (last-wins alias
  registration, :780-783). Both lack OnlyShowIn/NotShowIn.
- `alacritty` resolves to `/usr/bin/alacritty` under every PATH; xterm/foot/kitty/wezterm/konsole/gnome-terminal/
  xfce4-terminal all absent.
- Therefore PATH asymmetry (shell superset vs compositor subset) cannot change the selection.

## 6. Ancillary observations

1. Interpreter sensitivity: the script is `#!/bin/sh` (line 1) and relies on alias expansion; run explicitly via
   non-interactive `bash` it fails ("No valid terminal entry was found", rc 1). Any harness must invoke it via
   `/bin/sh` (or as the shebang dictates). This is an invocation-behavior fact, not an environment-variable
   difference, and does not affect the Revenger claim.
2. `[INFERENCE]` the client process's own env at press time was not captured directly (only its peers and
   descendants); the observed scope child's env equals the compositor byte-for-byte on all 19 XDG/PATH keys,
   which is the environment the resolver actually receives.

## Receipts in this directory

- `locator-check.txt` — 20/20 locators verified by `grep -nF` (script run, output captured).
- `hyprland-env`, `manager-env`, `daemon-env`, `env-diff` (empty), `daemon_env_identical` note in command logs.
- `out-compositor-PATH`, `out-minimal-PATH` (identical; sha256 `2c1b4908…` both).
- `cacheA-content` — hash `d27b6b707781b8106c7b00390bdf2822` + selected entry record.
- `err-*` — empty.
- `journal-sent-lines` — 76 live `sent:` lines, none with `--setenv`.
