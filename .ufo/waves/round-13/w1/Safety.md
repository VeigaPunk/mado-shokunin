# Safety — host probes, gate filesystem reads, fixture confinement (round 13, w1)

Seat `MadoR13.Safety` (sentinel, leaf). Surfaces: the assigned host probes (GlobalCapture `wayland-info`,
LocalSurface `~/.config/hypr` census), the gate's filesystem reads in
`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh`, and the gate's temporary fixture writes and symlinks.
This seat captured no raw session data. Every host observation it made was shape-only: stat metadata, line counts,
set/unset booleans. It ran no tests, builds or gate runs, and edited no shared files.

Axes: **coverage**, since U4 admission needs a clean provenance boundary for the globals census, and **operability**, since
the exact-set census and its fixtures must be safe and deterministic. Gate anchors are cited at snapshot tag `3D69`. The file
was being edited concurrently by GateImplement, so every anchor also quotes the code.

## Verdict summary

| # | sev | surface | status |
|---|---|---|---|
| F1 | **MEDIUM** | raw `wayland-info` dumps left world-readable in `/tmp` | **remediated in-wave** by GlobalCapture; absence verified |
| F2 | LOW | "pure read" overclaim for `wayland-info`; `-i` does not reduce what it binds | open (wording) |
| F3 | LOW | `wayland-info` rc 0 ≠ complete enumeration | open (admission predicate) |
| F4 | LOW | header-line projection can be forged by newline-bearing compositor strings | open (fail-closed parse) |
| F5 | LOW | compositor-version probe and Wayland socket are not bound to the same instance | open |
| F6 | INFO | projection safety depends on the tool version (1.3.0 binds no toplevel/title globals) | pin + re-review on upgrade |
| F7 | LOW | LocalSurface read beyond "names + source declarations"; "verified" overclaim | open (report wording) |
| F8 | LOW | `boundary_hash` hashes all of `~/.config` (142 files), so unrelated writers cause false DIVERGED | pre-existing; L1 decision |
| F9 | LOW | `${t/#\~/$ROOT}` broken by `&` (patsub_replacement) | **fixed in-flight** by owner (`:2367-2370`) |
| F10 | LOW | host file names verbatim in FAIL details (newline row forgery) | **fixed in-flight** for local census (`%q`, `:2416`, `:2422`); source-line text still raw |
| F11 | LOW | stale selftest fixture dirs: no trap, kept on failure, recut path bypasses cleanup | open; L1 cleanup |
| F12 | LOW | F-scenario `rm -rf "$csp"` lacked the prefix guard used elsewhere | **fixed in-flight** by owner (`:1018-1020` @ `57C6`) |
| F13 | LOW | `--snapshot` TOCTOU: existence check, then multi-second run, then `>` follows symlinks | pre-existing |
| F14 | INFO | fixture confinement of N1–N4 and the OM fixtures is sound | positive |
| F15 | INFO | `measure.py` / `MistakeFix.py` write surface is confined | positive |

---

## A. `wayland-info` (GlobalCapture probe)

### F1 — MEDIUM — raw identity dump persisted world-readable (remediated)

- **Exploit path.** The capture redirected the unfiltered `wayland-info` stdout to `/tmp`. Any local uid, service or later agent
  with `/tmp` access could read monitor make/model/description and DRM node paths. A later "find evidence in /tmp" sweep by any
  agent would also re-ingest it.
- **Evidence (shape-only, 2026-10-20 ~01:2x -0300).** `stat`: `/tmp/wayland-info.raw` and an undocumented
  `/tmp/wayland-info.2.raw`, each 68256 bytes, `mode=644`, owner vgpnk, mtime 01:07:07 and 01:08:22 (after `spec.json` at 01:06).
  `cmp` showed they were identical. `grep -c` counts on each: 72 `^interface: ` header lines, 651 tab-indented detail lines,
  1 `\tmake: ` line, 2 `description: ` lines, 4 device-path lines, 0 `hardware serial` lines. At that point
  `GlobalCapture.md:35-37` read "Raw stdout stays at `/tmp/wayland-info.raw` by design" and did not mention the second copy.
- **Impact.** Breaches the contract ("No secrets/session titles/raw environment/logs"; "Write only your explicit draft/report
  path") and `SKILL.md:33-34` / `:234-236` (session material stays shape-only). QUALITY criterion 13
  (`corpus/QUALITY.md:19`, "`/tmp` records provenance only") governs durability. It does not license keeping identity data.
- **Smallest remediation (done).** I messaged GlobalCapture. It deleted `/tmp/wayland-info.raw`, `/tmp/wayland-info.2.raw` and
  `/tmp/wayland-info.err`, and reworded its draft. Re-check: `ls /tmp/wayland-info*` returned "No such file or directory".
  Durable rule for future captures: project in a pipe (`wayland-info | sed -n …`) and never persist raw. If scratch is
  unavoidable, use `mktemp -d` (0700) with `trap 'rm -rf "$d"' EXIT`.
- **Artifact check.** `globals.json` has 72 entries. Every entry has exactly the keys `{interface, version}`, every name matches
  `^[a-z][a-z0-9_]*$`, every version is an int, and there are no registry ids. `set_sha256` replays exactly as the sorted
  `interface@version` lines, newline-terminated, through sha256 (`9569d02f…`). The file sha is `d9169df4…`, matching
  `GlobalCapture.md:65`.

### F2 — LOW — "pure read" overclaims; `-i` is not an exposure control

- **Evidence.** In wayland-info 1.3.0, `global_handler` (`wayland-info.c:3120-3146`) binds `wl_seat`, `wl_shm`, `zwp_linux_dmabuf_v1`,
  `wl_output`, `wp_presentation`, `zwp_tablet_manager_v2`, `zxdg_output_manager_v1`, `wp_drm_lease_device_v1`,
  `wp_color_manager_v1` and `wp_color_representation_manager_v1` whenever they are advertised. The `-i` filter only gates printing:
  `strstr(global->interface, wayland_info->interface)` at `:3163` inside `should_print_info`. On keyboard-capable seats it also
  creates a `wl_keyboard` (`:829`). Binding a lease device makes the compositor send a DRM fd (drm-lease spec quote below).
- **Impact.** It creates no surfaces, injects no input and changes no compositor config. Every object it creates is transient and
  per-connection. "Pure read" or "zero footprint" is still an inaccurate provenance claim, and suggesting `-i` "for less exposure"
  would be false hardening.
- **Remediation.** Describe the probe as a *read-only observational protocol client: it binds globals and creates transient
  per-connection objects; no compositor state mutation*. The only exposure control is the output projection.

### F3 — LOW — rc 0 does not prove a complete registry enumeration

- **Evidence.** `main` calls `wl_display_roundtrip(info.display);` (`:3258`), ignores the return value, and ends with `return 0;`
  (`:3267`). Only a failed connect returns −1 (exit 255).
- **Exploit path.** A protocol error mid-enumeration (for example a compositor rejecting one bind) yields rc 0 with a truncated list.
  The truncated list would then be admitted as "the host set".
- **Remediation.** The admission predicate should be rc == 0 **and** empty stderr **and** at least one header line **and**
  `wl_compositor` present. This capture meets it: `stderr_bytes: 0` is recorded and the sanitized set contains `wl_compositor@6`.
  Record the predicate in `globals.json`/S041 so it can be checked.

### F4 — LOW — header projection integrity

- **Evidence.** Header format `printf("interface: %-45s version: %2u, name: %2u\n", …)` (`:421`). Detail lines carry
  compositor-supplied free text without escaping, including `make`/`model` (`:520`), xdg_output `description` (`:1687`), lease
  connector `description` (`:2377`) and tablet names/paths. The replay regex in `GlobalCapture.md:274` uses `[^']*` and does not
  restrict the character set.
- **Exploit path.** A string containing `\ninterface: 'x', version: 9, name: 1` starts a column-0 line that the projection would
  accept as a global. A monitor-supplied EDID string can be such a string [INFERENCE: newline survival depends on compositor/EDID
  parsing].
- **Remediation.** Fail closed. Reject the whole capture if any column-0 line fails
  `^interface: '[a-z][a-z0-9_]*', +version: +[0-9]+, name: +[0-9]+$`. Do not skip such lines.

### F5 — LOW — version probe and socket are not bound to one instance

- **Evidence.** The compositor version came from `hyprctl -j version`, which follows `HYPRLAND_INSTANCE_SIGNATURE`. The globals came
  from `WAYLAND_DISPLAY=wayland-1` (`globals.json` `probe.display_socket`). Both variables are set in agent shells (I checked
  set/unset only).
- **Exploit path.** With a nested or second compositor, the globals would be attributed to Hyprland 0.56.2 `efb5099…` (false
  provenance).
- **Remediation.** Record two shape-only booleans: `hyprctl -j instances` count == 1, and that instance's socket == `$WAYLAND_DISPLAY`.
  [INFERENCE: the instances JSON carries a `wl_socket` field. `strings /usr/bin/hyprctl | grep -c wl_socket` returned 1, but I did
  not run the verb.] The gate already applies the count guard as `live.hypr.instances`.

### F6 — INFO — projection safety depends on the tool version

The host advertises `ext_foreign_toplevel_list_v1`, `zwlr_foreign_toplevel_manager_v1`, `zwlr_screencopy_manager_v1` and
`hyprland_toplevel_export_manager_v1` (`globals.json`). wayland-info 1.3.0 does not bind any of them (`:3120-3146`), so no window
titles or app_ids reached even the raw dump. Tablet `hardware serial` (`:896`) and DRM node paths (`:651`, `:2370`) are printed
when present, and the projection drops them. A future wayland-utils that binds foreign-toplevel would print session titles. Keep the
pin (`wayland-utils 1.3.0-1`, binary sha `d9d851d5…`, already recorded) and require a `global_handler` re-review before reusing the
probe after an upgrade. Membership also depends on hotplug (`wl_output`, the two `wp_drm_lease_device_v1`, tablets), so compare
captures as dated multisets. GlobalCapture already keeps multiplicity.

## B. `~/.config/hypr` census (LocalSurface probe)

### F7 — LOW — scope creep and an overclaim in `LocalSurface.md`

- **Evidence.** The role column at `LocalSurface.md:32-46` describes file contents ("(org.omarchy.ai-usage)", "Operator local notes
  window rules", "Display output resolutions, positions, refresh rates") and gives byte sizes. The assignment was "names and
  hyprland.conf source declarations". I saw no secret values in the report.
- **Accuracy.** `LocalSurface.md:142-144` says a same-count source substitution produced a baseline `sources_resolve` PASS. That is
  true for that one row, but the baseline positional `include_graph` check already FAILed any same-count substitution, so the
  baseline verdict was never CLEAN for that case. Only the member names were missing. The verdict-blind seam was the local census
  (a stray `*.conf`). The phrase "(as verified by `measure.py` scenario `replace-source`)" is unobserved: running was out of scope.
- **Remediation.** Drop the role and size columns, or mark them as inferred from file names. Change "verified" to "to be verified by
  L1". Pattern for future probes: `find ~/.config/hypr -maxdepth 1 -printf '%f\n'` plus `grep -E '^[[:space:]]*source[[:space:]]*='
  ~/.config/hypr/hyprland.conf`, and nothing else.

## C. Gate filesystem reads (`tools/mado-verify.sh` @ `3D69`)

**Positive (new census).** `for x in "$H"/*.conf; do [ -f "$x" ] && lobs+=("${x##*/}")` (`:2406-2408`) reads names only, never
content. When nothing matches, the literal glob fails `-f` and is skipped. `export LC_ALL=C` (`:79`) gives a stable order.
`*.bak.*` backups do not match. `envs.conf` is still only counted (`nenv=$(grep -cE …)`, `:2447`). A symlinked conf counts as
present via stat, and nothing reads through it. A dangling symlink counts as missing. Hidden `.*.conf` files are not enumerated:
that is a scope note, not a defect.

### F8 — LOW (pre-existing) — `boundary_hash` covers far more than the declared planes

- **Evidence.** `boundary_hash()` (`:222-229`) hashes every `*.conf|*.jsonc|*.css|*.toml|*.ini|config` under `$ROOT/.config`. On
  this host that is 142 files across 83 top-level dirs (`find … | wc -l`, counts only, 2026-10-20). A mismatch emits
  `row gate boundary.readonly FAIL "config plane changed during the run — investigate immediately"` (`:2652`).
- **Exploit/failure path.** Any unrelated app that writes its config while live hyprctl verbs run (each can take up to 5 s via
  `tmo`) flips the run to DIVERGED and blames the gate. Contents of unrelated, possibly credential-bearing `*.conf` files are read
  into `sha256sum`. They are not emitted: the detail carries only a 12-hex combined prefix. So the cost is footprint, not a leak.
- **Remediation (L1 decision; moves the PIN).** Limit the hash to the declared plane dirs (hypr, waybar, walker, alacritty, foot,
  kitty, ghostty, omarchy, mako, swayosd), and word the FAIL as "writer unknown".

### F9 — LOW — `&` in ROOT corrupted `~` expansion (fixed in-flight)

`x="${t/#\~/$ROOT}"` was affected by bash 5.3's default-on `patsub_replacement`. I measured it:
`R="/tmp/a&b"; t="~/x"; echo "${t/#\~/$R}"` printed `/tmp/a~b/x`. I reported it to GateImplement, who replaced it with
`'~'*) x="$ROOT${t#\~}"` (`:2367-2370`); L1 should verify. The residual is that `compgen -G "$x"` (`:2373`) still treats glob
metacharacters in ROOT as patterns. ROOT is operator-controlled and mktemp roots are alphanumeric, so this needs no action.

### F10 — LOW — host names in FAIL details (largely fixed in-flight)

Local missing/extra names now go through `printf -v xq '%q'` (`:2416`, `:2422`), and plain names such as `extra.conf` are
unchanged, so the N-scenario assertions still match. The `include_graph` detail `"$miss$sdiff"` (`:2352`) and the `sources_resolve`
`tset` still echo raw `source =` value text, inline comments included. Even unescaped, a forged row cannot flip the verdict, which
comes from the counters, and `--snapshot` fails closed on `row parse does not reconcile` (`:1948`). Receipts written under
`.ufo/evidence/` are committed: `.gitignore` excludes only `.ufo/interactive-sessions/`. So host conf names become durable
evidence. That is names only, which is acceptable.

### Info (pre-existing, outside round scope)

`live.env.gdk_scale`/`nvd_backend` read the gate's own environment (`gdk=$(printenv GDK_SCALE …)`, `:2825`), not Hyprland's.
"Session env" provenance therefore depends on the invoking shell. The values printed are two non-secret variables.

## D. Fixture temporary writes and symlinks

### F14 — INFO — confinement is sound

- Root: `T=$(mktemp -d /tmp/w5-mado-m52-selftest.XXXXXX)` (`:380`), a random 0700 directory. Every write is under `$T`.
- N1–N4 (`:1059-1131`) live under `$T/census/*`, built by `mkdir -p` plus `cp -a "$A/."`. `$A`'s only symlinks are relative
  (`ln -s theme/backgrounds/0-fixture.jpg …`, `ln -s ../omarchy/current/theme/mako.ini …`, `:311-312`), so each copy is
  self-contained. N2's `sed -i` edits a regular file in the copy.
- The absolute fixture symlink `$OMR/.agents/skills/omarchy → $OMR/…` (`:617`) is re-pointed after every `cp -a` and before any
  write: `rm -f` + `ln -s` (`:711-713`) and `rm -f` + `mkdir` (`:740-743`). Nothing writes through it into a sibling fixture. Keep
  this pattern for any future scenario that copies `$OMR`.
- Sandbox PATH dirs symlink host binaries (`ln -sf "$(command -v "$c")"`). Those binaries are only executed, and `rm -rf` does not
  follow symlinks, so cleanup cannot touch the targets.

### F11 — LOW — stale fixture dirs

- **Evidence.** 8 stale `/tmp/w5-mado-m52-selftest.*` dirs (0700): 4 at 2026-10-19 23:16 and 4 at 2026-10-20 00:58 (-0300). I did
  not open them. The selftest keeps `$T` on failure by design (`echo "fixtures kept: $T"`, `:1304`) and installs no trap, so an
  interrupted run also leaks its directory.
- **Likely source [INFERENCE].** Direct `REGRESSION_RECUT` harness runs. Each KILLED mutant's failing selftest keeps its fixtures, and
  the direct path bypasses `run_regression`'s prefix-guarded cleanup (`/tmp/w5-mado-m52-selftest.*)`, `:1661-1662`).
- **Remediation.** After L1's recut, with no selftest running, run `rm -rf /tmp/w5-mado-m52-selftest.*`. Optionally add an
  `INT TERM` trap that keeps the failure-retention behaviour.

### F12 — LOW — unguarded cleanup in scenario F (fixed in-flight)

At `3D69`, `[ -n "$csp" ] && rm -rf "$csp"` (`:1018`) deleted a path parsed from child stdout without the prefix guard that
`:1661` uses. Exploiting it required controlling the child's output, and the child is the same script, so this was defence in
depth. GateImplement adopted the guard. At tag `57C6`, `:1018-1020` reads
`case "$csp" in /tmp/w5-mado-m52-selftest.*) rm -rf "$csp" ;; esac`. GateImplement reports derived target `0f865d19d5f9cfba…`
(2,160 L) with `PIN_MADO` untouched, so L1's measured re-cut is still owed.

### F13 — LOW (pre-existing) — snapshot write TOCTOU

The existence check `if [ -e "$dest" ] || [ -L "$dest" ]` (`:1863`) runs before a multi-second child run, and the write
`printf '%s' "$content" >"$dest"` (`:1983`) follows symlinks. A same-user racer could plant a symlink in between and get an
arbitrary user-writable file overwritten. Smallest fix: `( set -C; printf '%s' "$content" >"$dest" )`, which is O_EXCL with no
format change. Doc drift: the header (`:23-24`) still says "no file is written", although `--snapshot` writes one.

### F15 — INFO — other wave scripts

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/measure.py` uses `tempfile.TemporaryDirectory(prefix='mado-r13-measure-')`
  (`:42`), which auto-cleans even on exception, and runs a copy of the gate with `--root <tree> --no-live`. Its builder slices from
  `build_fixture() {` to `\nselftest() {` (`:46`), so any top-level code placed between those markers would run. Today the slice
  contains only the function. It makes no host writes.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/reports/MistakeFix.py` contains no `open(`/`write`/`tempfile`/`subprocess`
  pattern. Its docstring says "Read-only: no network, no writes" (`:65`).

`resume_continuity_v1` (role clause) does not apply here. The only match in this repo is a historical transcript under
`.ufo/interactive-sessions/`, and no assigned surface implements resume.

## Source opens

1. **wayland-utils `wayland-info.c` @ tag 1.3.0.** URL `https://gitlab.freedesktop.org/wayland/wayland-utils/-/raw/1.3.0/wayland-info/wayland-info.c`.
   Accessed 2026-10-20. Revision: tag object `88c6b220…`, which peels to commit `d01edd68961ca01779dcb96afe56c2d99ff79067`
   (`git ls-remote`). Tier A (upstream source, matching installed `wayland-utils 1.3.0-1`).
   - Quote (`:3162-3163`, `should_print_info`): "return !wayland_info->interface || strstr(global->interface, wayland_info->interface);"
   - Quote (`:3258`, `:3267`): "wl_display_roundtrip(info.display);" … "return 0;"
   - Admitted: the bind set, the print-only filter, the rc semantics and the printed identity fields (F2–F6).
   - Rejected: as evidence of Hyprland behaviour, and for any other wayland-utils version.
   - Flip: re-open on any `wayland-utils` upgrade (pin `1.3.0-1`, binary sha `d9d851d5…`).
2. **wayland-protocols `staging/drm-lease/drm-lease-v1.xml` @ `35d9638cf0c3f0bbf0c42996580a284f3d8ce564`.** URL
   `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/35d9638cf0c3f0bbf0c42996580a284f3d8ce564/staging/drm-lease/drm-lease-v1.xml`.
   Accessed 2026-10-20. Tier A.
   - Quote (`:84-88`, `drm_fd` event): "The compositor will send this event when the wp_drm_lease_device_v1 global is bound … The
     included fd is a non-master DRM file descriptor" (abridged, 25 words).
   - Admitted: binding transfers a non-master fd, so the probe is not zero-footprint (F2).
   - Rejected: as proof that Hyprland's implementation complies.
   - Flip: re-open on a protocol bump past v1.
3. **Own work (this seat), 2026-10-20.** Measured bash semantics: `bash --version` → 5.3.15, `shopt patsub_replacement` → on,
   expansion result `/tmp/a~b/x` (F9). Tier A (own measurement). Admitted for F9 only.

## Tooling record

I installed or upgraded nothing. I used `curl`, `git ls-remote`, `stat`, `grep -c`, `cmp`, `find | wc -l` and `strings`.
GlobalCapture recorded its own `wayland-utils 1.3.0-1` install (pacman extra).

## Checks for L1 (not run by this seat)

- `ls /tmp/wayland-info* 2>&1` → no such file (F1 stays closed).
- `grep -nE "x=\"\\\$ROOT\\\$\\{t#|printf -v xq '%q'" tools/mado-verify.sh` → the in-flight F9/F10 fixes are present. Then run the
  one post-wave `--selftest` and confirm the N1–N4 detail assertions still match with `%q` names.
- After the recut: `ls -d /tmp/w5-mado-m52-selftest.* | wc -l` → 0 once cleaned (F11).
