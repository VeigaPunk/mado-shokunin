# ExecIsolationProbe — M26-5 repair evidence (round 27, wave w1)

Item: **ExecIsolationProbe** (probe seat; not a C1/C2 control, not a data seat).
Date: 2026-10-23. Host: linux 7.2.11-arch1-1 x86_64 (Arch).

## Verdict

`VERDICT ExecIsolationProbe: M26-5 repair confirmed — round-26 run_tool exposes the launcher's MADO_R27_CANARY name in the sandbox's pid-1 environ; round-27 does not. Round-26 snapshot() copies the bytes of a file symlinked outside HOME; round-27 skips it (in-HOME symlinks still copied by both). Residual hole: round-27 oracle() still uses shutil.copytree(..., symlinks=False).`

## What was done

1. Wrote `/fast/scratch/hyaku/mado-r27/iso/probe.py` (stdlib only): opens `/proc/1/environ` and
   `/proc/self/environ`, prints a JSON object with the variable **names** (split on `=`, values
   discarded), plus pid/ppid, `/proc/1/comm`, pid namespace and `--home`.
2. Wrote `/fast/scratch/hyaku/mado-r27/iso/launcher.py`: imports each harness **by path**
   (`importlib.util.spec_from_file_location`), calls `run_tool(probe, case_home)` and then
   `snapshot(case_home, fresh_dst)` on a fresh destination, and prints one combined JSON.
   It starts no Hyprland (run_tool only spawns bubblewrap).
3. Built a case home `/fast/scratch/hyaku/mado-r27/iso/case-home` containing
   `.config/hypr/hyprland.conf` (regular, 53 B), `.config/hypr/local-link.conf -> hyprland.conf`
   (symlink resolving inside HOME), and `.config/hypr/outside-link.conf ->` an 82 B canary file at
   `/fast/scratch/hyaku/mado-r27/iso/outside/canary.conf` (symlink resolving outside HOME).
4. Ran the launcher twice, each with a fresh random 33-char `MADO_R27_CANARY` in its own
   environment, under `env -i PATH=/usr/bin HOME=/home/vgpnk`:

```
cd /fast/scratch/hyaku/mado-r27/iso && env -i PATH=/usr/bin HOME=/home/vgpnk \
  MADO_R27_CANARY=<random 33-char token> timeout 300 prlimit --core=0 --as=4000000000 -- \
  python3 -I launcher.py > runN.json 2>runN.err
```

   Both runs: exit=0, stdout 3677 B, stderr 0 B.

## Measurements (identical across the two fresh-canary runs)

| measurement | round-26 harness (sha256 680798ed…) | round-27 harness (sha256 0da5b855…) |
|---|---|---|
| pid-1 process in sandbox | `bwrap` (probe is pid 2, ppid 1) | `bwrap` (probe is pid 2, ppid 1) |
| `/proc/1/environ` names | `HOME, LC_CTYPE, MADO_R27_CANARY, PATH, _` | `PATH` |
| canary name in pid-1 environ | **yes** | **no** |
| tool's own environ (`/proc/self`) | `HOME, PATH, PWD` | `HOME, PATH, PWD` |
| canary name in tool's own environ | no | no |
| `snapshot()` nfiles | 3 | 2 |
| outside-HOME symlink bytes copied | **yes** — 82 B, sha256 `4f318a7a…` = canary | **no** — destination absent |
| in-HOME symlink bytes copied | yes — 53 B, sha256 `2152bf6a…` | yes — 53 B, sha256 `2152bf6a…` |
| snapshot digest | `4351a259…` | `d2e9a941…` |

Mechanism observed: inside the sandbox `/proc/1` is the **bwrap supervisor**, not the tool
(`pid1_comm=bwrap`, probe pid 2/ppid 1); bubblewrap's `--clearenv` clears only the exec'd tool, so
the pid-1 supervisor keeps the environment `run_tool` itself was launched with, readable by the
sandboxed tool. Round-26 launches bwrap with no wrapper (oracle.py:232), so the canary name — and,
since the probe read the same `NAME=value` records, its value — was exposed. Round-27 wraps the
launch in `env -i PATH=/usr/bin` (oracle.py:234), leaving only `PATH`. The tool's own environment is
identical in both, so M26-5 fixes the supervisor-environ channel only.

Supplementary measurement (evidence, same file): when one of the four roots is itself a symlink
resolving outside HOME (`rootlink-home/.config/hypr -> outside/rootdir`), **both** harnesses copy the
outside file's bytes (nfiles=1, `root_canary_copied=true`, sha256 matches). `snapshot()` resolves the
root with `os.path.realpath(src)` before `os.walk`, and the round-27 guard checks only symlinked
*files* met during the walk, so a root-level outside symlink is not covered by either harness.

## Retained evidence

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/evidence/isolation-r27.txt`
  (15337 B, sha256 `9313c6aa5897513c77f07098894144260f154a1e9a5a8d62153321f5362e1fb6`): artifacts and
  sha256s, exact commands, **verbatim stdout of both runs** (`run1.json` sha256 `25e2c6e8…`,
  `run2.json` sha256 `8d0d7a81…`) and of the supplementary root-symlink run (`rootlink.json`
  sha256 `dc698f41…`), each verified as a byte-substring of the receipt; code anchors, host safety.
- Probe: `/fast/scratch/hyaku/mado-r27/iso/probe.py` (1572 B, sha256 `e7e03d3e…`).
- Launcher: `/fast/scratch/hyaku/mado-r27/iso/launcher.py` (4165 B, sha256 `99174d17…`).
- Root-symlink helper: `/fast/scratch/hyaku/mado-r27/iso/rootlink-snapshot.py` (2755 B, sha256
  `9baaa654…`).
- Raw run outputs: `/fast/scratch/hyaku/mado-r27/iso/run1.json`, `run2.json`, `rootlink.json`
  (+ empty `*.err`).

## Host safety

No Hyprland/tinywl was started and no `hyprctl` was invoked by this probe; nothing inherited
`WAYLAND_DISPLAY`/`HYPRLAND_INSTANCE_SIGNATURE`; `/dev/dri` untouched. `coredumpctl` Hyprland count
1338 before / 1338 after (delta 0). `/fast`: 115 G → 114 G available (86 % used). `run_tool` is
synchronous and both runs returned exit=0; no bwrap/python process from these runs remained. A
transient bwrap pair seen in one `ps` snapshot had already exited on inspection (concurrent seat
activity, not launched here). One read-only listing of `/proc/1614/environ` **names only** was made
to identify the operator's live Hyprland; no values were printed or stored.

## Risks / notes for the L1

1. **Outside-HOME ingress still exists at root level (measured):** `snapshot()` resolves each of the
   four roots with `os.path.realpath(src)` before walking, and the r27 guard (oracle.py:78) tests only
   symlinked *files*. An outside-HOME **root** symlink is followed by both harnesses (supplementary
   measurement: both copy the outside bytes). If any of `~/.config/hypr`, `~/.config/omarchy/current/theme`,
   `~/.local/share/omarchy/default/hypr`, `~/.local/state/omarchy/toggles/hypr` resolves outside HOME,
   that content enters `snap0` — and every case home copied from it — under either harness. Whether
   the operator's `current/theme` link leaves HOME is not measured here.
2. **Residual outside-HOME copy path in `oracle()` (code-read, not exercised):** both harnesses'
   `oracle()` still copy the case tree with `shutil.copytree(case_home, ohome, symlinks=False)`
   (r26:139, r27:141), which follows symlinks, so an `oracle()` called on a raw, symlink-bearing tree
   would still pull outside bytes into the oracle home (or fail on a dangling link). The C1 counter
   is safe from this specific path: it snapshots `~` into `snap0` first (`c1/count.py:260-261`), builds
   every case home as a copy of `snap0` (`:266`), and passes only those `snap0`-derived trees to
   `oracle()` (`:272-274`); `snap0` contains no symlinks (in-HOME links are dereferenced, outside file
   links skipped by r27). The risk is for future `oracle()` callers that skip `snapshot()`; note it
   does not mitigate risk 1, because root-level outside bytes are already inside `snap0`.
3. The M26-5 fix is launcher-side (`env -i PATH=/usr/bin`): only `PATH` reaches the bwrap
   supervisor now. Any future caller that injects more variables through that wrapper would expose
   them again; `--clearenv` continues to protect the tool's own environ.
4. `oracle()`'s Hyprland path was not run here (would start Hyprland; out of this item's scope).
5. No tools installed or upgraded; no lane files touched except this report and the named evidence
   path. No git/jj write commands were run.
