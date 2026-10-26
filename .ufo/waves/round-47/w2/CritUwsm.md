# CritUwsm — w2 FALSIFY of RevengerUwsm (round 47)

Seat: CritUwsm (w2 falsify). Target: `w1/RevengerUwsm/report.md` claim: `uwsm-app --` does not alter the
resolver's environment; under the hotkey `xdg-terminal-exec` sees the compositor's environment.

## Verdict: NOT FALSIFIED

Every falsifiable step of the claim was re-run on the host today (read-only; `xdg-terminal-exec` only with
`--print-*` and `XDG_CACHE_HOME` in scratch). The environment `uwsm-app --` gives the resolver is the
compositor's environment, byte-identical for every selection-relevant variable. The one selection-relevant
variable that *does* differ between a login shell and the hotkey path — `PATH` — is proven harmless today by a
cold-cache dual-PATH experiment (identical stdout + rc, including under a minimal `/usr/bin:/usr/local/bin`
PATH). No hole found; nothing here needs re-registration.

## Method

1. Enumerated the resolver's complete external environment surface from the pinned real script
   `.ufo/waves/round-47/fetch/xdg-terminal-exec` (sha256 `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`):
   - `XDG_CURRENT_DESKTOP` (lowercased :1144; hashed :195; OnlyShowIn/NotShowIn :848,:857,:867,:876)
   - `XDG_CONFIG_HOME`/`HOME`/`XDG_CONFIG_DIRS` (:148), `XDG_DATA_DIRS` (:157), `XDG_DATA_HOME`/`XDG_DATA_DIRS` (:166)
   - `XDG_CACHE_HOME` (:172-173, cache file location)
   - `PATH` through `command -v`: TryExec :936, Exec[0] :964, cached-cmd revalidation :274
   - `LC_ALL` forced to `C` (:183,:355,:972); `LANG=C` in the hash listing (:200)
   - opt-in overrides `XTE_DEBUG`/`DEBUG` (:61), `XTE_EXECARG_COMPAT` (:1147), `XTE_CACHE_ENABLED` (:1172)
   - no `PWD` read; cwd used only post-selection at :1496 (`cd "$XTE__DIRVAL"`)
2. Compared rungs today: `systemctl --user show-environment` (XDG_*+PATH) vs `/proc/1622/environ` (Hyprland,
   same pid as w1) → `diff` empty (receipt `env-diff`, 0 lines); daemon pid 1813 identical (receipt
   `daemon_env_identical`); `HOME`/`LANG` equal; no `XTE_*`, `DEBUG`, `DISPLAY`, `WAYLAND_DISPLAY`, `LC_*`
   in the compositor env (no hidden override).
3. Re-read the live vector: `journalctl --user -u wayland-wm-app-daemon.service` → 76 `sent:` lines, all
   `--scope` + `--same-dir`, none with `--setenv`; the resolver vector matches the w1 line (`xdg-terminal-exec
   --dir=...`). Unit `ExecStart`/`EnvironmentFile` at :11/:14 feed the *daemon* only; the client
   (`/usr/bin/uwsm-app`) writes NUL args (:172) and `eval "$CMDLINE"` (:202) with no env mutation; man
   systemd-run lines 30-32 verified verbatim.
4. Empirical dual-PATH test (cold cache, `/bin/sh`): PATH(A) = exact compositor PATH vs PATH(B) =
   `/usr/bin:/usr/local/bin`; env otherwise identical (config/data/desktop/cache in scratch). Both produced
   identical stdout+rc: `Alacritty.desktop` / `/home/vgpnk/.local/share/applications/Alacritty.desktop` /
   `alacritty` / `--working-directory=/home/vgpnk/Projects/shokunin`, rc 0. Written cache hash
   `d27b6b707781b8106c7b00390bdf2822` == w1 item 7.
5. Candidate universe: exactly one terminal entry ID, `Alacritty.desktop` (user copy wins over the system
   duplicate via last-wins alias registration; both lack OnlyShowIn/NotShowIn); `alacritty` resolves to
   `/usr/bin/alacritty` under every PATH; no other `TerminalEmulator` desktop entry exists in any applications
   dir. So PATH asymmetry cannot change selection today.

## Findings

- **F1 (supports)**: All selection-relevant XDG_* values, cache location, and desktop id are byte-identical on
  the compositor, manager, and daemon rungs today; the observed scope child equals the compositor on all 19
  XDG/PATH keys. The resolver's env under the hotkey is the compositor's.
- **F2 (supports)**: The live daemon vector never uses `--setenv`; the service branch (main.py:3738) and its
  five session vars are inert for the hotkey, and those five values equal the compositor's anyway.
- **F3 (partly supports, residual)**: `PATH` is the single selection-relevant variable that differs between a
  login shell (superset) and the compositor/hotkey path (subset). On this host it provably cannot change the
  verdict (F-test above); it remains a latent divergence mechanism if a future candidate lived only under
  shell-only PATH dirs. Not a falsification.
- **F4 (ancillary, harness note)**: the resolver relies on alias expansion under `/bin/sh` (shebang line 1);
  invoked via non-interactive bash it fails with "No valid terminal entry was found" (rc 1). Any harness that
  runs the real pinned script must use its `/bin/sh` interpreter.

## Evidence in this seat dir

`locator-check.txt` (20/20 OK), `hyprland-env`, `manager-env`, `daemon-env`, `env-diff` (empty),
`out-compositor-PATH`, `out-minimal-PATH` (identical), `cacheA-content` (hash d27b6b7…), `err-*` (empty),
`journal-sent-lines` (76). Locators computed via `grep -nF`, never typed.

Safe-observation ledger: `xdg-terminal-exec` run twice, both `--print-id --print-path --print-cmd --dir=…`,
cache in scratch, rc 0. No terminal launched, no uwsm-app/systemd-run/systemctl start/hyprctl dispatch, no
pacman, no input injection, no GUI. Scratch `/fast/scratch/hyaku/mado-r47/CritUwsm` removed after copying.
