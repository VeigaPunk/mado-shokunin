# CritOracle — round-47 w1 report

Target: the C1 real-script-as-judge design. Judge = `/usr/bin/xdg-terminal-exec` (sha256 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac, v0.14.3). All experiments run on `/fast/scratch/hyaku/mado-r47/CritOracle` (xfs), in bubblewrap, with `strace -f` and `env -i`. Full repros: `.ufo/waves/round-47/w1/CritOracle/findings.md` (F1-F11); receipts `execve-cold.log`/`execve-warm.log` beside it.

## Counterexample (strongest)
Two fixtures identical in every specified field (contents, env, args, stubs) except the creation order of two co-equal TerminalEmulator entries in the same applications dir (A then B vs B then A) produce DIFFERENT stdout: `b.desktop → kitty` vs `a.desktop → alacritty` (rc 0 both). Root cause: `find -L` at `/usr/bin/xdg-terminal-exec:795` is unsorted; fallback selection follows readdir order (`:790,:1060`). Directory order is FS-defined (xfs small dirs = insertion order; 400-file dir = neither insertion nor sorted; btrfs/ext4/tmpfs differ). Byte-identity cannot be guaranteed for ambiguous fixtures unless materialization order is pinned and single-candidate-per-dir is enforced.

## Evidence (selected)
- F1: t1(order A,B)→b.desktop; t2(order B,A)→a.desktop; t3→b.desktop again.
- F2: bwrap without `--dev`: `line 200/199/756: /dev/null: No such file or directory` → NO_TERMINAL rc=1 despite valid terminals; with `--dev /dev` rc=0. Missing /bin (shebang) or /lib64 (loader) fail earlier.
- F3: unset XDG_DATA_DIRS/XDG_CONFIG_DIRS → decision comes from host `/usr/share/xdg-terminal-exec/xdg-terminals.list` + `/usr/share/applications` (121 entries): `Alacritty.desktop` (host) rc=0.
- F4: cache key = hash of `echo 4` + XDG_CURRENT_DESKTOP + `LANG=C ls -LRl` → md5sum (`:189-203`); PATH/stub content not hashed → stale reuse across cases if XDG_CACHE_HOME shared. `save_cache` runs backgrounded (`:1457`).
- F5: cold execve set = find/awk/tr; warm = ls/md5sum/tr; non-C LC_ALL adds self-respawn (`:185,:357,:974`). Tripwire must be scoped to the tool's subtree, never wrap the judge's `/bin/sh`.
- F6: `tr` lowercasing (`:1144`) byte-identical on ÉCOLE under C/C.utf8/en_US.utf8 (ASCII-only) — locale is not a divergence source today; pin LC_ALL=C anyway.
- F8: `find -L` symlink cycles are detected (no hang), but file symlinks can pull host content into entries; forbid symlinks in fixtures and bind explicit dirs (not `--ro-bind / /`).
- F10: duplicate IDs across data dirs are deterministic; user override wins (matches L1 host fact).

## Impacted axes
Byte-identity (F1, F2, F3, F4), nondeterminism/run-reproducibility (F1, F4), tripwire soundness (F5, F8), cache modeling (F4), locale (F6), exit-status parity (F9: no-terminal rc=1, stdout empty; unknown options silently discarded, `:1317-1320`).

## Smallest safe corrections (harness)
1. Sandbox: `bwrap --unshare-all --proc /proc --dev /dev --tmpfs /tmp --ro-bind /usr /usr --ro-bind /lib64 /lib64 --ro-bind /etc /etc --bind /bin /bin --bind $ROOT $ROOT --chdir $ROOT --die-with-parent`; never whole-root binds.
2. Env: pin LC_ALL=C LANG=C; require ALL of XDG_CONFIG_HOME/XDG_CONFIG_DIRS/XDG_DATA_HOME/XDG_DATA_DIRS per fixture; XDG_CACHE_HOME fresh per case.
3. Fixture driver: canonical path-sorted creation; no symlinks; at most one candidate per applications dir unless pinned by config-list IDs; generate `expect` from the materialized case.
4. Compare stdout + rc only (stderr carries diagnostics incl. no-terminal message).
5. Tripwire: PID-ancestry scoped to the tool only.
