# OldGateBoundary — mado-verify read-only claim vs package safety (round 16, w1)

Seat: `MadoR16.OldGateBoundary` (leaf reviewer, source reading only).
Subject: `tools/mado-verify.sh` (unchanged this round). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Gate identity observed: sha256 `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207`, 3711 newline-terminated lines / 177,849 B (grep count 3712 incl. a final unterminated line). This equals the committed-bytes digest recorded in `corpus/lessons/round-15-verifier-spotcheck.md` ("Gate and correction evidence"). The `ea798ad0…` digest in `.ufo/waves/round-15/evidence/gate-shas.txt` belongs to an earlier `.tower` worktree copy and is not the lane gate.

Not performed: no gate execution (`--selftest`, `--regression`, `--snapshot`, live or `--no-live` runs), no build/lint/tests, no installs or updates, no pacman query or plan, no live compositor/service/input probes, no edits to the gate or to any file other than this report.

## Verdict

The default run (`bash tools/mado-verify.sh`, no mode flags) is read-only in effect. Its code path writes nothing, makes no package-manager call, and invokes only read verbs of `hyprctl` and `omarchy`. Four things in the gate's own labels overstate that, and the package-safety question is outside what the gate measures at all:

1. The header's read-only discipline is stale. It omits `--snapshot` and `--regression` writes, the external harness execution, and the non-`hyprctl` binaries the live plane runs.
2. Every CLEAN verdict prints `file + live planes verified read-only` (`tools/mado-verify.sh:3703`). That phrase covers far less than it reads.
3. `boundary.readonly` proves byte-identity of a suffix-filtered subset of `$ROOT/.config`, at two sample points.
4. The gate has zero package-state coverage. A CLEAN verdict is not evidence about packages, libinput, or binary integrity.

No code change is recommended this round. Editing any byte of `tools/mado-verify.sh` outside the excised marker blocks moves the regression target and forces a SETUP (`:1854`, `:1891-1894`, precedent in the `.ufo/waves/round-15/evidence` regression logs). Record these limits in prose (SKILL/corpus, L1-owned) and leave the gate bytes alone.

## Findings

### F1 — Header read-only claim is stale (High, claim accuracy)

- Header claim, `tools/mado-verify.sh:22-24`: "READ-ONLY on every substrate: hyprctl read verbs only ...; no file is written; scratch lives under /tmp/w5-mado-m52-* and only --selftest makes it."
- Contradicted by the gate's own modes:
  - `--snapshot FILE` writes a caller-named file: `:2020-2024` (discipline comment), `:2230` (`printf … >"$dest"`), `:2231` and `:2240` (`rm -f` on refusal). The config-plane exclusion (`:2200-2213`) and existence and symlink refusal (`:2110-2113`) are real guards. The write itself is TOCTOU-separated from the `-e` check.
  - `--regression` creates `/tmp/mado-verify-regression.*` (`:1860`), copies the target there (`:1882-1887`), and executes an external harness with `bash "$REGRESSION_RUNNER"` (`:1759-1760`). It keeps the workdir on FAIL and SETUP (`:1885`, `:1895`, `:1928`, `:1933`). It removes `/tmp/w5-mado-m52-selftest.*` directories named in the sweep evidence (`:1905-1912`).
  - `--selftest` creates `/tmp/w5-mado-m52-selftest.*` (`:395`) and deletes it only on pass (`:1534`).
- SKILL.md (lines 507-508) documents the regression and snapshot writes correctly. Only the header is stale.
- Operational meaning: a reader who trusts the header will classify `--regression` and `--snapshot` as read-only. Neither is.

### F2 — "hyprctl read verbs only" understates the live surface (Medium)

The default live run executes these external commands (all read at `:2968-3239` and `:3278-3479`):

| Command | Anchor | Read-class by name | Side effects verified here |
|---|---|---|---|
| `hyprctl` `version`, `-j instances`, `configerrors`, `-j getoption …` (×6), `-j binds`, `-j monitors`, `-j layers` | `:2976`, `:2986`, `:2995`, `:3017`, `:3029`, `:3038`, `:3051-3053`, `:3063`, `:3073`, `:3089`, `:3108`, `:3169` | yes; no `dispatch`, `keyword`, `reload` anywhere in the file | verified by reading |
| `pgrep -x hypridle`, `pgrep -x waybar` | `:3119`, `:3161` | yes | not verified |
| `printenv GDK_SCALE`, `printenv NVD_BACKEND` | `:3131`, `:3137` | yes | not verified |
| `waybar --version` | `:3150` | executes a package-owned binary | [UNVERIFIED] no source read of waybar |
| `walker --version` | `:3211` | executes a package-owned binary | [UNVERIFIED] no source read of walker |
| `busctl --user get-property fr.arouillard.waybar …` | `:3198` | D-Bus property read | [UNVERIFIED] whether a name lookup can D-Bus-activate a service |
| `systemctl --user is-active app-walker@autostart.service`, `elephant.service` | `:3222-3223` | read | not verified |
| `omarchy version` | `:3361` | read | [UNVERIFIED] source not read |
| `omarchy theme current` | `:3236`, `:3462` (called twice per run) | read | [UNVERIFIED] source not read |
| `omarchy commands --json --all` | `:3422` | read | source-verified: `register_command` (`~/.local/share/omarchy/bin/omarchy:125-163`) parses only leading header comments; `load_commands` (`:275-283`) registers without executing. No cache write matched. |
| `git -C <omarchy tree> describe`, `rev-parse HEAD`, `show HEAD:…` | `:3382`, `:3391`, `:3406` | read; `git status` is correctly avoided (`:3262`) | ok |
| `python3` (parsing), `sha256sum`, `readlink -f`, `find`, `wc`, `awk`, `sed` | throughout | read | ok |

- No mutating `omarchy` verb is called. The grep for `theme set`, `restart`, `refresh`, `install`, `setup`, `update`, and `pkg` found none in code.
- The header wording should name the actual set and say that `waybar`, `walker`, `omarchy`, `busctl`, and `systemctl` are invoked read-only by convention, not by proof.

### F3 — `boundary.readonly` covers a narrow, two-sample subset (Medium)

- Mechanism: `boundary_hash` (`:237-245`) hashes regular files under `$ROOT/.config` whose names match `*.conf`, `*.jsonc`, `*.css`, `*.toml`, `*.ini`, or `config`. Hashed at the start of `verify()` (`:2516`) and at the end (`:2954`). Row: `:2952-2962`. Comparison: `:2955`.
- Not covered, though read by the gate:
  - `$ROOT/.config/omarchy/current/theme.name` (read at `:3597-3601`). Suffix does not match.
  - Symlinks, including `current/background` and `.config/mako/config`. `find -type f` excludes them (`:240`); their targets are read at `:3617` and `:3625`.
  - `$ROOT/.local/state/omarchy/toggles/hypr/window-no-gaps.conf` (read at `:2764`). Outside `$C`.
  - `$ROOT/.local/share/omarchy/default/hypr/*.conf` (source census targets, `:2561-2579`, `:2633-2677`). Outside `$C`.
  - The omarchy checkout and its `.git` (`:3382-3406`), and `$ROOT/.agents/skills/omarchy`.
  - Everything outside `$ROOT`, including any cache a child process might write.
- Two-sample limit: the row proves the hashed subset is byte-identical at two points. A write and reversal between samples is invisible.
- Limit on proof strength: the only whole-tree proof is selftest scenario A (`:942-959`, `find "$A" -type f` over the fixture, `--no-live`). No whole-tree proof exists for a live run.
- Verdict semantics: `boundary.readonly` SKIP does not block CLEAN (`:2961` plus `:3699`, which only checks FAIL and UNKNOWN). A missing `.config` makes the hypr rows FAIL anyway, so this is a low edge case.
- Corroboration: SKILL.md line 450 already states that `boundary.readonly` means unchanged configuration bytes within that run, not identical outputs across revisions. The gate's CLEAN wording goes further than SKILL does.

### F4 — Zero package-state coverage; CLEAN is not package-safety evidence (High for the package-safety question)

- Whole-file searches for `pacman`, `sudo`, `libinput`, `/var/lib`, `checkupdate`, `-Qkk`, `-Sp` returned no code matches. The only system path in the file is the shebang `/usr/bin/env`. Not one `/usr`, `/etc`, or `/var` path is read in code.
- The version pins are string equality on binary output, not package or binary identity:
  - Hyprland commit `efb5099…`, `hyprctl version` (`:2984-2991`, live only).
  - Waybar `v0.15.0`, `waybar --version` (`:3149-3156`, live only).
  - walker `2.17.0`, `walker --version` (`:3206-3217`, live only).
  - omarchy `3.8.3` version file (`:3304`, file plane), `omarchy version` (`:3366`, live), tag `v3.8.4` (`:3387`, live), HEAD `8fcc9d60…` (`:3396`, live), skill leaf sha `becd149e…` (`:3337`, file plane).
- Consequences:
  - A partial upgrade that changes none of these strings is invisible. libinput, libinput-tools, pipewire, mesa, wayland, and the portal stack are not pinned anywhere in the gate.
  - R15's forbidden libinput partial upgrade (1.31.3 to 1.32.0) is not representable in this gate. The round-15 closure already says "unchanged gate is a different observable" (`corpus/lessons/round-15-verifier-spotcheck.md`, operability row).
  - A replaced binary that reports the same version string passes. The gate does no `sha256` or ownership check on `/usr/bin/waybar` or `/usr/bin/walker`. SKILL.md around line 1387-1389 shows walker integrity was checked by hand with `pacman -Qkk` in an earlier round, not by the gate.
  - `--no-live` reads none of the Hyprland, Waybar, walker, or omarchy pins. Its CLEAN is labelled "file plane only" (`:3701`), which is honest.
  - The `live.hypr.version` and `live.waybar.version` rows are the only signals a Hyprland or Waybar package change could produce, and only in a live run.
- Header disclosure: `tools/mado-verify.sh:78-80` lists what is not verified (window rules, dispatcher behaviour, module text, idle/lock transitions, per-window rules). It does not list package state, binary integrity, or non-pinned libraries. That is the omission to record.
- The gate contains no install predicate and no `pacman -Sp` or installed-name logic. The R15 overlap fixtures are not in this file, so nothing here corroborates or refutes them.

### F5 — `--regression` executes unpinned external code (Medium, mode-scoped)

- Harness path: `MADO_R7_FLEET` is derived from the script location (`:1643-1644`), giving `$MADO_R7_FLEET/tameshi-shokunin/tools/mutate-and-run.sh` by default (`:1854`). `MADO_VERIFY_HARNESS` overrides it.
- The harness is run with `bash` (`:1759-1760`). Its sha256 is printed as "provenance, not gated" (SKILL.md:507-508; `REGRESSION_HARNESS` line in the round-15 evidence).
- Running the gate from a `.tower` worktree yields a different `MADO_R7_FLEET` (dirname^3 of the script path), so the default harness path will not exist and the run reports SETUP unless `MADO_VERIFY_HARNESS` is set. This matches the round-15 evidence, which set the variable explicitly.
- The default run never reaches this code.

### F6 — Guard and cleanup weaknesses (Low)

- `:1038-1041` (nested selftest cleanup): the path is parsed from child stdout and matched with an unanchored `case` pattern `/tmp/w5-mado-m52-selftest.*`. In bash `case`, `*` matches `/`, so `/tmp/w5-mado-m52-selftest.x/../../<dir>` would pass the guard before `rm -rf`. The current producer, `echo "fixtures kept: $T"` (`:1540`), emits an mktemp path (`:395`), so this is latent, not reachable from current code.
- `:1905-1912` (regression cleanup) uses a slash-free regex on evidence and `[ -d ]`, so traversal is blocked. It still removes any existing directory with a matching name, not only ones this run created. Other concurrent runs could be affected.
- `:121` `tmo`: without `timeout` on PATH, commands run unbounded. A hung `hyprctl` or `busctl` would hang the gate. Coreutils `timeout` is expected on this host ([INFERENCE]).

### F7 — What the gate cannot be cited for (boundary statement, for L1)

Record these in SKILL/corpus prose this round, without editing the gate:

- A gate CLEAN is not evidence of package integrity, partial-upgrade absence, library versions, binary identity, or rendered output.
- `boundary.readonly` is byte-identity of a suffix-filtered `$ROOT/.config` subset at two points during one run. It is not a proof of no-write across the run or the host.
- `--regression` and `--snapshot` are not read-only in the header's sense.
- Module text (Waybar), dispatcher behaviour, and window-rule effects are explicitly unverified (`:78-80`).

## Checked and clean

- No mutating `hyprctl` verb is reachable. Live-plane calls are version, instances, configerrors, getoption, binds, monitors, layers (`:2968-3239`).
- No mutating `omarchy` verb is reachable. Live calls are `version`, `theme current`, `commands --json --all` (`:3236`, `:3361`, `:3422`, `:3462`).
- No package-manager, `sudo`, or service-control call exists in the default path.
- The default run's only writes are none. `mktemp` and `cp` appear only inside selftest (`:395`, `:1026-1042`), regression (`:1860`), and the snapshot write (`:2230`).
- Selftest is hermetic on substrate: live-mode scenarios use `PATH=$SANDBOX` or `PATH=$OMB` with stubs, so `hyprctl` and the real session are not reached (`:994`, `:685-797`, `:1433`).
- Snapshot config-plane and existence guards are real (`:2110-2113`, `:2200-2213`), subject to the TOCTOU and `.config`-only limits noted in F1.

## Verification gaps (not run, by constraint)

- The `waybar --version` and `walker --version` side effects, and `busctl` name-activation behaviour, were not source-verified.
- `omarchy version` and `omarchy theme current` were not source-read; only `commands` was.
- `--regression` and `--snapshot` behaviour is from code reading, not execution. No run was performed.
- The `grep` tool truncated several broad searches in this session. The external-command inventory is anchored on full reads of the live plane (`:2968-3239`), omarchy plane (`:3278-3479`), theme plane (`:3593-3635`), verdict (`:3640-3712`), hypr file plane (`:2543-2800`), waybar/walker/terms rows (`:2803-2883`), and helpers (`:122-236`). Regression-harness body (`:1545-1880`) and snapshot parse (`:2071-2180`) were read partially, and only for write sites and guards.

## Installs and tooling

None. Pacman transactions remain paused host-wide per the round-16 instruction. No package was installed, updated, planned, or queried. No `~/.omp/agent` or credential file was opened.
