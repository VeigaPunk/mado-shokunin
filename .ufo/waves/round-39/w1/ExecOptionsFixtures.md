# Seat report — ExecOptionsFixtures (round 39, w1, C2 fixture evidence)

## Scope
Fixture suite for `tools/mado-options.py` (C2). Written only inside the seat dir
`.ufo/waves/round-39/w1/ExecOptionsFixtures/` plus this report. No tool installations
(no packages needed; Python stdlib only). No tracked lane file edited.

## Deliverables (all under `w1/ExecOptionsFixtures/`)
- `trees/main-home/.config/hypr/hyprland.conf` — entry; `$moddir = ~/.config/hypr/modules`,
  then `source =` chain in line order: `~/.../defaults/00-defaults.conf`,
  `~/.../user.conf`, `~/.../toggles/*.conf` (glob), `~/.../ai-usage.conf`,
  `$moddir/base.conf` (variable-expanded `~` module source). Also direct options, a
  trailing comment, a `##` escape, and excluded keywords (`workspace`, `windowrule`,
  `animation`, `bind`, `exec-once`).
- `trees/main-home/.config/hypr/defaults/00-defaults.conf` — variables (`$xwl = 1`),
  options, and two malformed lines (`this is not a setting`, `= broken`).
- `trees/main-home/.config/hypr/user.conf` — shadows `misc:disable_hyprland_logo`;
  value with trailing comment trimmed.
- `trees/main-home/.config/hypr/toggles/01-touchpad.conf`, `02-performance.conf` — glob
  dir (sorted); `02` uses `$xwl` from defaults.
- `trees/main-home/.config/hypr/ai-usage.conf` — shadows `decoration:rounding` and
  `misc:disable_hyprland_logo` (last declarer).
- `trees/main-home/.config/hypr/modules/base.conf`, `modules/extra/nested.conf` — module
  source + relative `source = ./extra/nested.conf` join.
- `trees/main-home/.config/hypr/live.json` — `--getoption` dump (value/custom_type/set).
- `trees/fifo-home/`, `trees/dangling-home/` — strict-file refusal cases (FIFO source;
  dangling-symlink source); `run-fixtures.sh` creates the non-regular targets.
- `expected.json` — precise rows (key, value, owner file, layer, line, set; `agreement`
  in getoption mode) for 14 static rows and 16 getoption rows.
- `run-fixtures.sh` (executable) — runs the tool per fixture, compares with the embedded
  comparator, prints `fixtures=N/N`; exits 0 iff all match.
- `observed/` — recorded tool outputs (see below).

## Commands run (current lane working tree)
```
lanesc=/home/vgpnk/Projects/shokunin/mado-shokunin
cd $lane/.ufo/waves/round-39/w1/ExecOptionsFixtures
./run-fixtures.sh
# -> fixtures=4/4 ; exit=0
# also validated from foreign cwd: cd /tmp && <seat>/run-fixtures.sh -> fixtures=4/4, exit=0
```
Individual tool invocations recorded in `observed/`:
- `python3 -I tools/mado-options.py --home trees/main-home` → `observed/treeA-static.json`
  (exit 0; 14 rows, sorted compare).
- `python3 -I tools/mado-options.py --home trees/main-home --getoption trees/main-home/.config/hypr/live.json`
  → `observed/treeA-getoption.json` (exit 0; 16 rows).
- `python3 -I tools/mado-options.py --home trees/fifo-home` → exit 3; `observed/fifo.err`
  = `mado-options.py: source = ~/pipe.conf: no matches for .../fifo-home/pipe.conf`.
- `python3 -I tools/mado-options.py --home trees/dangling-home` → exit 3;
  `observed/dangling.err` names `~/gone.conf` → `.../dangling-home/gone.conf`.

## Verified behavior (expected-vs-actual, all matching)
- Last-declarer resolution per key across traversal order: `misc:disable_hyprland_logo`
  defaults(true)→user(false)→ai-usage(true) ⇒ owner `ai-usage.conf` line 3;
  `decoration:rounding` toggles(4)→ai-usage(2) ⇒ owner `ai-usage.conf` line 2;
  `input:kb_layout` owner `user.conf` line 3; `dwindle:pseudotile` owner
  `defaults/00-defaults.conf` line 4; touchpad toggle owner `toggles/01-touchpad.conf`
  line 2; `xwayland:use_nearest_neighbor` = `1` (from `$xwl`, defined in defaults,
  used in `02-performance.conf` line 3).
- Module `~` + variable-expanded source and relative join: `misc:module_level`
  owner `modules/base.conf` line 3; `misc:module_level_nested` owner
  `modules/extra/nested.conf` line 2.
- Root-file options: `general:colormode` line 9, `misc:font_family` line 10 =
  `JetBrains Mono # Nerd Font` (`##` escape → literal `#`), `misc:disable_autoreload`
  line 16. `user.conf` `misc:splash` = `TEXT` (trailing comment trimmed). Malformed
  lines, comment-only lines, and `workspace/windowrule/animation/bind/exec-once` produced
  no rows.
- Layer labels as emitted by the tool: `hyprland.conf` → `root`, `ai-usage.conf` →
  `ai-usage`; all other sourced files → `user` (including defaults/toggles/modules).
  All rows `set: true`.
- `--getoption` merge (live.json): `misc:disable_hyprland_logo` (config true == live
  true, live set=true) → `agreement*`; `decoration:rounding` (2 vs 3) → `mismatch`;
  `input:kb_layout` (us == us, live set=false) → `mismatch`; live-only keys
  `misc:missing_key_here`, `misc:ghost_live` → `live-default` with owner/layer/line
  null (set=false); all config-only keys → `config-only`.

## Discrepancies / observations (tool not edited; reported only)
1. The fixture matrix as run could not produce the plain `agreement` label (only
   `agreement*` appeared for a matching live value). The exact trigger for plain
   `agreement` vs `agreement*` (and `mismatch` for value-equal-but-live-set=false) is
   under-specified by the spec; my expectations record the observed labels.
2. `mado-options.py:161` emits a `SyntaxWarning: "\`" is an invalid escape sequence`
   to stderr on first run (cosmetic; does not affect exit code or stdout).
3. Strict-file failure message wording is "no matches for <abs path>" (exit 3) rather
   than an explicit non-regular-file diagnostic; the contract (refusal + named path)
   holds for both FIFO and dangling-symlink sources.

## Evidence hashes
- tool `tools/mado-options.py`: `cee78d99de2e3420572aa028f439240ac12e5eb6d595de75e2fc62e5ea9ce61e`
- `run-fixtures.sh`: `5ac915b966f3a543f81be10b26f289319dbc627ba8c7081f9fe0d7f4d7d7bcd7`
- `expected.json`: `b478148c23b898a1f6da8019c6afd6fc5fa3bb8a15ad84a24869297421b126fd`

## Risks
- Expected layer labels and agreement vocabulary are pinned to the observed tool
  behavior (v1 of the tool); if the tool changes its layer classification or agreement
  mapping, `expected.json` must be re-derived. The runner is order-insensitive per key
  and treats JSON null fields as absent.
- The FIFO/dangling fixtures require the runner to create non-regular files; the runner
  is idempotent (`rm -f` + `mkfifo`/`ln -s` before each run).
