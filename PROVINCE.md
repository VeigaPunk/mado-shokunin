# mado-shokunin — Province

**Domain:** desktop & compositor craft — the Hyprland/waybar/walker
configuration plane and display behavior on this host.

**Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules,
animations), `~/.config/waybar/`, `~/.config/walker/`, terminal emulator
configs (`~/.config/alacritty|foot|kitty|ghostty/`), themes/wallpapers as
declared files, screen/idle behavior (hypridle/hyprlock where present).
The omarchy skill (`~/.agents/skills/omarchy/`) is documentation surface,
read-only. All config trees are READ-ONLY for this lane: probe, measure,
recommend — the operator applies changes.

**Refuses:** secrets in configs (shape-only, → kagi), model endpoints
(→ kama), model quality (→ kengaku). Never mutates a running compositor
state; every claim is file-byte- or screenshot-verified.

**Round-19 refinement (P5 theme/wallpaper route; resolves `:8-9`; no new write surface):** the theme/wallpaper state is the omarchy theme plane under `~/.config/omarchy/**`, read-only — IN: `current/theme.name`, the `current/background` link and `current/theme/**` as declared theme state (the hypr/waybar/walker/terminal consumers are the owned chain; `mako.ini`, `swayosd.css`, `btop.theme` and `neovim.lua` are chain evidence only, their consumer configs not owned), plus `themes/` as the declared user theme store (empty on this host; the populated 19-theme store is the read-only checkout `~/.local/share/omarchy/themes`, w2 AtkProvinceLine); OUT (report, never absorb): `hooks/**` bodies, `branding/`, `extensions/`, `themed/` template machinery, any secret-shaped value (→ kagi), and every omarchy program update, theme write or consumer reload; `~/.local/share/omarchy/**` (checkout) is read-only source evidence for this chain (gate `theme_plane()`/`omarchy_plane()` in `tools/mado-verify.sh`; route note `corpus/knowledge/theme-route-r18.md`).

**Round-23 refinement (C3 lane-tool inventory; no new write surface, no cross-domain bleed):** the lane's own analysis instruments are named here so the province accounts for every tracked tool it runs. `tools/mado-action-plan.py` reads the JSON bytes of a caller-supplied declared action plan and a JSON safety policy (regular files only; symlinks, FIFOs and devices are refused), prints one `MADO_PLAN:` line and one JSON verdict, writes no host state (its `--selftest` writes only ephemeral fixtures inside a private temporary directory and runs a copy of itself as a child process), and is therefore a lane safety gate over declared plans rather than a new desktop surface. `tools/mado-tripwire.py` reads the `.jsonl` bytes of OMP session transcripts it is pointed at, treating assistant command text as data it never executes, prints one `MADO_TRIPWIRE:` or `MADO_TRIPWIRE_FROZEN:` line and one JSON verdict, writes no file at all (its `--selftest` only re-invokes itself), and is therefore a lane evidence instrument over issued-command text rather than a new desktop surface. `tools/mado-assessment.py` reads an assessment bundle and the population and expectation files it names under `--root` (bounded, symlink- and traversal-refused), prints one JSON verdict object, writes no file at all (its `--selftest` only re-invokes itself), and is therefore a lane integrity gate over the lane's own paperwork rather than a new desktop surface. `tools/mado-evidence-audit.py` reads an evidence bundle, the snapshot it names and the inventoried files under `--root` whose digest and size it compares, prints one JSON verdict object, writes no file at all (its `--selftest` only re-invokes itself), and is therefore a lane evidence gate over artifact arithmetic rather than a new desktop surface. OUT (report, never absorb): these instruments own no config tree and no host state; the tripwire's transcript bytes are read as data and its findings are lane-local evidence about issued commands, never a fleet-wide or sibling-lane conduct verdict (transcript observation stays with mori); package state stays with tsukuroi; secret-shaped values stay with kagi (the tripwire redacts secret-shaped substrings from the command text it prints instead of reporting their content); and the reusable mutation-testing method stays with tameshi (`tools/mado-verify.sh` consumes tameshi's `mutate-and-run.sh` read-only and prints its revision as provenance, never patching it and never gating it).

| Tool | Reads | Writes | Owner and adjacent lanes |
|---|---|---|---|
| `tools/mado-action-plan.py` | the JSON bytes of a caller-supplied declared action plan and a JSON safety policy (regular files only; symlinks, FIFOs, devices and directories refused), or in `--frozen` the pinned `plan.json`, `policy.json` and `expected.json` of a snapshot directory | no host state; `--selftest` writes only ephemeral fixtures inside a private temporary directory it removes on exit, and runs a copy of itself as a child process | mado (declared-plan safety gate; it never executes the supplied argv), tsukuroi (package and service state), operator applies any resulting change |
| `tools/mado-tripwire.py` | the `.jsonl` bytes of OMP session transcripts it is pointed at — assistant `toolCall` blocks only (bash `arguments.command`, python eval `arguments.code`), text treated as data and never executed; symlinks, `agent.db`-named files and paths under `~/.omp/agent` outside `sessions/` are refused; `--frozen` also reads the pinned `expected.json` and `inputs/*.jsonl` | nothing — no file is created or modified; stdout only, plus a `--selftest` child process of itself | mado (lane-local evidence about issued commands only; never a fleet or sibling-lane conduct verdict), mori (transcript observation), tsukuroi (package state), kagi (secret-shaped substrings are redacted, not reported) |
| `tools/mado-assessment.py` | the JSON bytes of an assessment bundle and, under `--root`, the population and `expected.json` files that bundle names (bounded to 2 MiB each; symlinks, path traversal and escaping paths refused); `--selftest` reads the sealed round-21 fixtures | nothing — no file is created or modified; stdout only, plus a `--selftest` child process of itself | mado (artifact-assertion integrity gate over the lane's own paperwork; no admission, closure or promotion authority) |
| `tools/mado-evidence-audit.py` | the JSON bytes of an evidence bundle and the snapshot that bundle names under `--root`; `--selftest` additionally reads the sealed round-22 fixture manifest and re-hashes every inventoried file, comparing each sha256 and size against the pinned inventory | nothing — no file is created or modified; stdout only, plus a `--selftest` child process of itself | mado (artifact arithmetic and evidence-label audit only; not execution truth, chronology, admission or promotion) |
| `tools/mado-verify.sh` | the file bytes of the declared config planes (hypr, waybar, walker, terminal and omarchy-theme trees) and `hyprctl` read verbs only (version, instances, configerrors, getoption, binds, monitors, layers); `--regression` writes the embedded defect spec (byte-identical to tameshi's recorded case) into scratch, hashes the harness and its own bytes, and hands the spec to tameshi's `mutate-and-run.sh` read-only | no config bytes; scratch only under `/tmp/w5-mado-m52-*` (selftest) and `/tmp/mado-verify-regression.*` (regression, removed unless `--keep`) | mado (config-plane verdict gate; the operator applies changes), tameshi owns the mutation-testing method — `mutate-and-run.sh` is consumed read-only and its revision is printed as provenance, not gated |
| `tools/mado-binds.py` | the bytes of `DIR/.config/hypr/hyprland.conf` under `--home DIR` and every file its `source =` lines reach (`~` = DIR, globs, relative paths); no compositor, socket, network or environment beyond `HOME` | nothing — stdout only (one JSON array, the 18 `hyprctl binds -j` fields per entry) | mado, round 25 (static prediction of the Hyprland v0.56.2 bind table a config tree builds, before the operator applies it; the operator applies changes; not live state — binds created at runtime by exec'd commands are outside it) |
| `tools/mado-anims.py` | the bytes of `DIR/.config/hypr/hyprland.conf` under `--home DIR` and every file its `source =` lines reach (`~` = DIR, globs, relative paths; absolute `source =` paths are followed as Hyprland follows them); no compositor, socket, network or environment variables | nothing — stdout only (one JSON array `[nodes, beziers]`, the six node and five bezier fields of `hyprctl animations -j`) | mado, round 26 (static prediction of the Hyprland v0.56.2 animation table a config tree builds, before the operator applies it; the operator applies changes; not live state — `hyprctl keyword animation` at runtime is outside it) |
| `tools/mado-globals.py` | the bytes of a caller-supplied journal file (`--journal-file`, read whole, 8 MiB cap; missing/unreadable path = setup error) or, under `--live`, the stdout of exactly one program (`journalctl`, or `--journalctl PROG` resolved to an absolute regular, non-group/other-writable file) run with exactly `--user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`, stdin `/dev/null`, env `PATH`/`XDG_RUNTIME_DIR`/`DBUS_SESSION_BUS_ADDRESS`/`LC_ALL`; no compositor socket, no Wayland client, no network, no config tree | nothing — stdout only (`MADO_GLOBALS_SESSION:`, `MADO_GLOBAL:`, `MADO_GLOBALS_DIFF:`, `MADO_GLOBALS:` lines); `--selftest` (63/63 passed this seat) writes only inside a private temporary directory it removes | mado, round 41 (read-only census of the advertised globals; class table is static — a name, not a capability proof; operator applies changes) |
| `tools/mado-geometry.py` | the bytes of one or more caller-supplied Hyprland config files (`--rules`, each read whole, 1048576 B cap; a missing, unreadable, directory, FIFO or any non-regular path is a setup error) and one caller-supplied `hyprctl clients -j` dump (`--clients`, a regular file or `-` for standard input, at most 1048577 B, UTF-8 JSON holding a list of objects); no compositor socket, no Wayland client, no network, no config tree, no process started | nothing — stdout only (`MADO_GEOM_RULE:`, `MADO_GEOM_CLIENT:`, `MADO_GEOMETRY:` lines); `--selftest` writes nothing; it opens only the fixed paths `/nonexistent/none`, `/` and `/dev/null` read-only to test its refusals (`.ufo/waves/round-43/w2/SentLiveRun/findings.md` F3) | mado, round 43 (a read-only join of a rule's declared size against the goal box the compositor prints; it never reads the compositor itself — the caller supplies the dump — and an AGREE verdict says nothing about the rendered size, the client's own request or which rule wrote the box; the operator applies any rule change) Round 44: also reads each client's `fullscreen` integer (1 maximized, 2 fullscreen) to name the state instead of comparing (FULLSCREEN, MAXIMIZED; top verdict NOT_COMPARED, exit 5); still no compositor read of its own (`.ufo/waves/round-44/registration-v2.md`) |
| `tools/mado-watchplan.py` | the bytes of the `--config` file when it is a regular file, at most one `--getoption` file (a captured `hyprctl getoption -j` reply) and every regular file its `source =` lines reach (absolute, `~` under `--home`, relative and glob forms; 1 MiB per file; `--display-root` only changes how paths print), with `stat`, `lstat`, `realpath`, `glob`, `isdir`, `lexists` and `islink` on those paths only | nothing — stdout only (`MADO_WATCH:` and `MADO_WATCH_LIVE:` lines); no process, no socket; `--selftest` writes only inside a private temporary directory it removes | mado, round 56 (static prediction of the inotify watch list Hyprland 0.56.2 registers for a config tree, joined to `misc:disable_autoreload`; no filesystem event is generated and no reload is observed) |

**Round-23 wave-2 correction (append-only; CritProvinceBleed, CritSeparability):** the inventory above covers every tracked file under `tools/`, not "every tracked tool it runs": the lane also tracks scripts under `.ufo/waves/**`, which are round evidence and not inventoried here. Corrections to the rows: `tools/mado-verify.sh` also runs live read-only probes (`systemctl --user is-active` on the two Walker units, `busctl --user get-property`, `pgrep`, `walker --version` and `waybar --version`, three `omarchy` read subcommands, read-only git on the omarchy checkout); its unit-state rows sit next to tsukuroi's unit-health ground, which stays tsukuroi's. `tools/mado-tripwire.py` redacts only its three fixed secret patterns; other secret shapes can reach its stdout, so secret handling stays kagi's and its output is treated as possibly sensitive. Its read surface (OMP session files) is shared with mori's transcript observation; this overlap is named for the integrator, not self-certified as no bleed, and the tool is run on mado's own seats' transcripts by policy, not by enforcement. The line "every claim is file-byte- or screenshot-verified" predates the live read-only probes of `mado-verify.sh`; those probes are read-only observations, never mutations.

**Out of province → report, never absorb.**

**Round-25 residual correction (append-only; RevToolProvenance):** the `tools/mado-binds.py` row's read surface is
wider than "under `--home DIR`": like Hyprland, it follows absolute `source =` paths anywhere, and it seeds config
variables from the whole process environment (`os.environ`), so `source = $VAR` can also leave `DIR`. It still writes
nothing, opens no socket and runs no process; run it on trees you mean to read.

**Round-27 correction (append-only; M26-10, round-26 spot-check §7 items 1 and 3):** the round-25 residual correction
above is stale as to environment seeding. Since `a496b02a`, `tools/mado-binds.py` does not seed config variables from
`os.environ`: a `$NAME` supplied only by the environment stays literal, and `source = $VAR` using only an environment
value is not followed (unlike hyprlang v0.6.8). Variables declared in the config tree still expand, and absolute
`source =` paths are still followed anywhere, so the tool still reads outside `DIR` when the tree says so. The tool's
docstring states the same limit. Sweep (`git grep -n -i 'environ\|environment' 5ddc5885 -- PROVINCE.md corpus
tools/mado-binds.py`): the other hits are historical lessons (round-25, round-26 and their spot-checks), left as
records, and `tools/mado-anims.py` notes, which are unrelated.

**Round-36 refinement (append-only; two counters and two record gates; no new desktop surface):** the lane
now tracks four record instruments under `quality/`, and they are named here for the same reason the round-23
table names the `tools/` instruments — the province accounts for every tracked tool it runs, and none of these
touches a declared config plane.
`quality/counters/c1-idle-lock.py` (`PRED-C1-r36-v1`) reads `corpus/SOURCES.md`, the three round-35 idle-lock
entries and the eight fetch receipts under `.ufo/waves/round-35/fetch/`, plus the frozen spec
`.ufo/waves/round-36/c1/frozen.json`; it writes nothing and prints one verdict line.
`quality/counters/c2-ledger.py` (`PRED-C2-r36-v1`) reads the clause ledger, the frozen-blob ledger, the
committed discrimination receipts and — for the tip rule and the blob ids — read-only git in the lane; it writes
nothing. `quality/check-counter-discrimination.py` reads the frozen manifest, runs the two counters as child
processes and writes one receipt per control (and nothing else); its fixtures are generated outside the lane by
`.ufo/waves/round-36/c2/gen-mutants.py`, which writes only beneath `--out`.
`quality/check-evidence-pointers.py` (`PRED-PTR-r36-v1`) reads `LOG.md`, `SCORECARD.md`,
`corpus/lessons/round-36.md`, the tree at one revision and read-only `git status`; it writes nothing.
All four are record instruments: they score the lane's own evidence and paperwork, never a compositor, a config
plane or a host service, and none of them is a desktop surface.

**Round-36 refinement (append-only; resolves spot-check D9 and `CritD9Boundary`):** the refusal boundary for
documentation-localization material was practised in four rounds of lessons and spot-checks and stated nowhere in
this file (`git log -S 'localiz' -- PROVINCE.md` → empty). It is stated now, once, and it decides the r28
(URL), r29 (snapshot semantics) and r30 (revision bookkeeping) entries and the round-16 Chinese config guide the
same way:

> Material about the *documentation artifacts* of the desktop plane and their localization — the Chinese/Japanese
> ArchWiki channel, its URLs, snapshot semantics, revision bookkeeping and translation drift, and any
> documentation written in a localized channel — is outside the province; only the omarchy skill's own files
> (`~/.agents/skills/omarchy/`) are documentation surface, and those are read-only.

This is a *channel* rule, which is what the lane has actually done: the English upstream documentation channels
remain admissible for config-plane claims (round-35's S203 flip rests on one), while the localized documentation
channel and its mechanics stay out. It does not widen any owned surface and leaves line 10's omarchy ownership
intact.


## Round-38 addendum — request-socket knowledge ground (append-only)

The lane's two-socket IPC contract (`corpus/knowledge/ipc-contract-r25.md`)
and its round-38 edge classes live here as documentation/source-read knowledge:
the request socket's published flag vocabulary (`hyprctl-flags-r28.md`), its
live bound — a five-second poll timeout, not a byte cap, read at the host's own
commit — (`request-socket-live-bound-r8.md`), and the upstream request/follow
ceilings at a later revision (`request-limits-upstream-r31.md`). All are
read-only byte work: no socket is ever connected, no request is sent, and no
compositor or config state is touched. This anchors the runtime-IPC knowledge
half (tsukuroi's OUT-004 routes only this file's lines 3–16, the config-plane
half).


**Round-45 refinement (append-only; one tool, two counters, one record gate; no new write surface):** `tools/mado-monitors.py` reads caller-supplied config files (`--config`, regular files, 1 MiB cap) and one `hyprctl monitors all -j` dump (`--monitors`, file or stdin); it writes nothing, starts no process, opens no socket. `quality/counters/c1-r45-monitors*.py` and `c2-r45-monitor-entry*.py` score round evidence (the v2 C1 counter runs the tool under bubblewrap); `quality/check-session-material.py` reads tracked blobs at one revision and writes nothing. Output configuration stays operator-owned: the lane reads `monitors`, never `keyword` or `output`.

**Round-46 refinement (append-only; one tool, three counters, one entry; no new write surface):** the input-device
plane of the owned config tree - the `input` block's `kb_layout`, `kb_variant`, `kb_options`, `kb_model`, `kb_rules`,
`kb_file` keys and the `device` / `device[NAME]` blocks with the `kb_*` and `scroll_factor` values they set - is owned
here at the resolution Hyprland 0.56.2 gives it. `tools/mado-devices.py` reads only the config files the caller names
(`--config`, regular files, 1 MiB cap) and one `hyprctl devices -j` dump (`--devices`, file or stdin); it follows no
`source =`, writes nothing, starts no process and opens no socket; the operator captures the dump with the read verb
and applies any change. The round's record instruments are `quality/counters/c1-r46-devices.py` (v1, superseded),
`c1-r46-devices-v2.py` (v2, failed its own controls), `c1-r46-devices-v3.py` (`PRED-C1-r46-v3`: runs the scored tool
under bubblewrap with an allowlist root of /usr and /etc, its own run directory writable, and a unix-socket tripwire
it listens on outside the sandbox), and `c2-r46-input-device-entry.py` / `-v2.py` (read git objects of the entry,
registry, lesson, README and the ten pins under `.ufo/waves/round-46/fetch/`; write nothing). None touches a config
plane, the compositor or a host service. Global `input:scroll_factor` and the libinput settings stay readable only
through `hyprctl getoption`; the keybind keymap (`resolve_binds_by_sym`) is not part of this join.

**Round-51 refinement (append-only; lane-level instrument ledger, no desktop write surface):** `quality/tool-ledger.md` names each
tracked instrument under `tools/`, top-level `quality/*.py` and `quality/counters/*.py`, with a description and an accountability
pointer. `quality/check-tool-ledger.py` derives that population from a pinned revision and checks row coverage, dangling paths,
pointer presence and empty descriptions; it reads Git objects only, writes no repo state, and its `--selftest` uses caller scratch.
`quality/counters/c1-r51-ledger.py` scores the ledger against the frozen round-51 population predicate. These record instruments
do not touch config planes, a compositor socket or a host service.

**Round-55 refinement (append-only; one read-only tool, four record instruments, one knowledge entry and one errata correction; no new write surface):** `tools/mado-kbdopts.py` is a read-only join. It reads only the files its caller names: each `--config` path (Hyprland config text, regular files, 1 MiB cap) and at most one `--getoption` path (a captured `hyprctl getoption -j` reply). From these it computes the effective per-keyboard `input:repeat_rate`, `input:repeat_delay` and `input:numlock_by_default` values under the hyprlang 0.6.8 subset it models, and compares the global values with the live reply. Constructs it refuses are counted `unsupported` and ignored, never guessed; a `source =` line is skipped without a count and its file is not followed, and the tool's docstring lists the known divergences from Hyprland's own parser (round-55 wave-2 source review). It starts no process, opens no socket and writes nothing; the operator captures the `getoption` reply with the read verb and applies no change. The round's record instruments are `quality/counters/c1-r55-kbd-entry.py` (PRED-C1-r55, the entry's counter), `quality/counters/c3-r55-p19.py` (PRED-C3-r55, the errata correction counter), `quality/check-r55-controls.py` (the independent harness that builds the frozen negative controls in scratch git repositories and runs the counters and the C2 fixtures as child processes under its `--work` directory) and `quality/check-freeze-order.py` (the freeze-order gate delivered as the M54-2/M54-4 mistake fix; its input contract is not stated in the frozen registration and is unverified until it lands). The counters and harness write only under `--work`; none touches a config plane, the compositor, a socket or a host service. Keypress delivery, client-side repeat and the seat's numlock state are outside every instrument.

**Round-56 refinement (append-only; one read-only tool, three record instruments, one knowledge entry; no new write surface):** `tools/mado-watchplan.py` is a read-only join. It reads only the files its caller names: `--config` (the main Hyprland config, a regular file), at most one `--getoption` file (a captured `hyprctl getoption misc:disable_autoreload -j` reply, 1 MiB cap), and the files that the config's `source =` lines reach (absolute, `~` with `--home`, relative and glob forms); on those paths it calls only `stat`, `lstat`, `realpath`, `glob` and the `isdir`, `lexists` and `islink` checks. From these it predicts the inotify watch list Hyprland 0.56.2 registers for the config tree and reads `misc:disable_autoreload` the way hyprlang does. Constructs outside its model are counted `unsupported` and never guessed. It starts no process and opens no socket, and writes nothing except under `--selftest`, which uses a private temporary directory it removes; the operator captures the `getoption` reply with the read verb and applies no change. Its capability row enters SCORECARD only on the round's C2 `TARGET_MET`. The record instruments are `quality/counters/c1-r56-autoreload-entry.py` (the entry's counter), `quality/counters/c3-r56-used-by.py` (the registry used-by counter) and `quality/check-r56-controls.py` (the independent harness). The two counters read git objects only, at the revision they are given, and write nothing. The harness also reads git objects, but it builds scratch repositories, exports the tool and its fixtures and runs them and the counters as child processes, writing only under its `--work` directory; it never writes the lane or the fleet repo. None of them touches a config plane, the compositor, a socket or a host service. Reload, inotify delivery and the Lua config provider stay outside every instrument.

**Round-57 host-change record (append-only; dated 2026-10-31; §6 absent-surface correction — protocol work, not a failure).** The lane's live host changed: rounds 1–56 were observed on the omarchy Linux host (`~/.config/hypr/`, waybar, walker, `hyprctl`; last live host state recorded 2026-10-28). This round runs on a **Windows 11 Home host, build 26200 (`MINGW64_NT-10.0-26200`, `Win32_OperatingSystem` caption above)**, and every Linux/compositor surface the sections above own is **absent here** — probed 2026-10-31, all read-only:

```
for c in hyprctl waybar walker hypridle hyprlock hyprsunset mako swayosd grim slurp omarchy \
         -> command -v: ABSENT (11/11)
for d in .config/hypr .config/waybar .config/walker .config/alacritty .config/foot \
         .config/kitty .config/ghostty .config/omarchy .local/share/omarchy .agents/skills/omarchy \
         -> test -e "$HOME/$d": ABSENT (10/10), HOME=/c/Users/jpvei
bash tools/mado-verify.sh --no-live -> MADO_VERIFY: DIVERGED (17 fail, 7 unknown, 2 pass),
         first fail hypr.file.root (missing: /c/Users/jpvei/.config/hypr/hyprland.conf);
         gate boundary.readonly PASS (config-plane bytes unchanged by the run)
```

The omarchy-era text above stays as the frozen record of that host; nothing in it is claimed about this host. `tools/mado-verify.sh` and every config-tree-reading tool remain valid against the committed fixtures and any future host that restores those trees; on this host their live objects are absent (the freshness rubric "file-plane gate agreement 28/29" is **not re-derivable here** — recorded in SCORECARD, not silently retired; L0 question filed).

**This Windows desktop is the lane's real live observation surface, read-only:** window-manager state, DPI facts and compositor (DWM) state, observed through read-only PowerShell queries. The lane observes and recommends; every change (settings, registry, processes) stays operator-owned. The instrument is `tools/mado-win-desk.py` (round 57): it spawns exactly one read-only PowerShell child (fixed embedded script — `Win32_OperatingSystem`, `System.Windows.Forms.Screen`, two in-process registry-read layers, `dwmapi!DwmIsCompositionEnabled`, `Get-Process` census and `GetForegroundWindow`), parses its stdout as JSON, and re-prints whitelisted fields only; `--from-file` re-derives a verdict from a captured snapshot; `--selftest` spawns nothing. It never prints window titles, clipboard contents, environment values or file contents, never echoes raw child output, writes no file, opens no socket and mutates nothing (round-56 M56-17 rule carried over: a channel may be asserted to exist, its values are never printed). Secret-shaped values stay kagi's (unchanged); process names and window handles it does print are desktop facts, not credentials, and window titles are excluded precisely because they can carry secret material.

### Surface state register (2026-10-31, this host)

Each row: the PROVINCE-declared surface group, its state **on this host**, the observation date, and the read-only probe that re-derives the state.

| surface group | state (date) | probe (read-only) |
|---|---|---|
| hypr plane (`~/.config/hypr/**`, `hyprctl`) | absent (2026-10-31) | `command -v hyprctl` → not found; `test -d ~/.config/hypr` → missing |
| waybar (`~/.config/waybar/**`, process) | absent (2026-10-31) | `command -v waybar` → not found; `test -d ~/.config/waybar` → missing |
| walker (`~/.config/walker/**`) | absent (2026-10-31) | `command -v walker` → not found; `test -d ~/.config/walker` → missing |
| terminal configs (alacritty/foot/kitty/ghostty) | absent (2026-10-31) | `test -e ~/.config/{alacritty,foot,kitty,ghostty}` → all missing |
| theme/wallpaper omarchy plane | absent (2026-10-31) | `test -e ~/.config/omarchy ~/.local/share/omarchy` → missing |
| idle/lock plane (hypridle/hyprlock/hyprsunset) | absent (2026-10-31) | `command -v hypridle hyprlock hyprsunset` → not found (3/3) |
| omarchy skill docs (`~/.agents/skills/omarchy/`) | absent (2026-10-31) | `test -d ~/.agents/skills/omarchy` → missing |
| windows desktop plane (WM state, DPI, DWM) | observed (2026-10-31) | `python tools/mado-win-desk.py` → `MADO_WINDESK: CLEAN (screens=1 dpi=96 dwm=on …)`; cross-check 5/5 stable fields agree with independently executed probes (`corpus/knowledge/windows-desktop-plane-r57.md` § Verify) |

| Tool | Reads | Writes | Owner and adjacent lanes |
|---|---|---|---|
| `tools/mado-win-desk.py` | live mode: the JSON stdout of exactly one spawned read-only PowerShell child (`--powershell`, default `powershell.exe`, resolved on PATH) running a fixed embedded script whose only inputs are `Win32_OperatingSystem` (CIM read), `System.Windows.Forms.Screen` (in-process assembly), the registry values `HKCU\Control Panel\Desktop\WindowMetrics!AppliedDPI` and `HKCU\Control Panel\Desktop!LogPixels` (read twice via `Get-ItemProperty` and `Microsoft.Win32.Registry.GetValue`), `dwmapi!DwmIsCompositionEnabled`, `Get-Process` and `GetForegroundWindow`; `--from-file`: one caller-named JSON snapshot (4 MiB cap); `--selftest`: nothing (in-memory only) | nothing — stdout only (one `MADO_WINDESK:`/`MADO_WINDESK_SELFTEST:` line plus one JSON object line); it never prints window titles, clipboard, environment values or file contents, and never echoes raw child output | mado, round 57 (read-only observation of the Windows desktop plane: point-in-time, no setting is read through any privileged API, no mutation, no rendered-output claim); operator applies any change; kagi keeps secret-shaped values (titles are excluded from the output by design) |

**Round-60 refinement (append-only; one read-only tool; no new write surface):** `tools/mado-win-dpi.py`
observes the Windows DPI-virtualization layer read-only. Live mode spawns exactly one PowerShell child
(`--powershell`, default `powershell.exe`) running a fixed embedded script whose only inputs are user32
getters — `GetThreadDpiAwarenessContext` and `GetAwarenessFromDpiAwarenessContext` (the calling thread's
own awareness), `GetSystemMetrics(SM_CXSCREEN/SM_CYSCREEN)` beside `GetSystemMetricsForDpi(…, 96)`,
`GetWindowDpiAwarenessContext` per main window of the `Get-Process` census (histogram counts only),
`GetForegroundWindow` and `GetDpiForWindow` (point-in-time) — parses its stdout as JSON, and re-prints
whitelisted fields only; `--from-file` re-derives a verdict from a captured snapshot (4 MiB cap);
`--selftest` (10 assertions) spawns nothing. It collects no window titles, no process names and no window
handles into its output, never echoes raw child output, writes no file, opens no socket and mutates
nothing: no `Set*` verb exists in it, and setting thread DPI awareness stays operator-owned (SKILL §
Round 57 rule 4 carried). The awareness getter identifies the caller branch; the metrics join alone
cannot (vacuous at effective 96 — `corpus/knowledge/windows-dpi-awareness-metrics-r60.md` J13).

| Tool | Reads | Writes | Owner and adjacent lanes |
|---|---|---|---|
| `tools/mado-win-dpi.py` | live mode: the JSON stdout of exactly one spawned read-only PowerShell child (`--powershell`, default `powershell.exe`, resolved on PATH) running a fixed embedded script whose only inputs are the user32 getters `GetThreadDpiAwarenessContext`, `GetAwarenessFromDpiAwarenessContext`, `GetWindowDpiAwarenessContext`, `GetForegroundWindow`, `GetDpiForWindow`, `GetSystemMetrics` and `GetSystemMetricsForDpi`, plus the `Get-Process` main-window census (handles filtered, never emitted); `--from-file`: one caller-named JSON snapshot (4 MiB cap); `--selftest`: nothing (in-memory; ephemeral fixtures in a private temp dir it removes) | nothing — stdout only (one `MADO_WINDPI:`/`MADO_WINDPI_SELFTEST:` line plus one JSON object line); it never prints window titles, process names, window handles, clipboard, environment values or file contents, and never echoes raw child output | mado, round 60 (read-only observation of the DPI-virtualization layer: point-in-time census/foreground, no privileged API, no mutation, no rendered-output claim); operator applies any change; kagi keeps secret-shaped values (titles and names are not collected at all) |

**Round-61 refinement (append-only; one read-only tool; no new write surface):** `tools/mado-win-display.py`
observes the native display-topology and display-mode layer read-only. Live mode spawns exactly one PowerShell child
(`--powershell`, default `powershell.exe`) running a fixed embedded script whose only inputs are user32 getters —
`EnumDisplayMonitors` (hdc and clip NULL: the documented enumerate-all shape) with `GetMonitorInfoW` per returned
handle into a MONITORINFOEXW (szDevice, rcMonitor, rcWork, dwFlags), and `EnumDisplaySettingsW` in its three
documented iModeNum shapes (ENUM_CURRENT_SETTINGS −1, ENUM_REGISTRY_SETTINGS −2, graphics-mode index series 0..N
bounded at 256, stopping at the documented zero return) — parses its stdout as JSON and re-prints whitelisted fields
only; `--from-file` re-derives a verdict from a captured snapshot (4 MiB cap); `--selftest` (10 assertions) spawns
nothing. It collects no window titles, no process names and no window handles, never echoes raw child output, writes
no file, opens no socket and mutates nothing: no Set*/Change* verb exists in it, and display-mode changes stay
operator-owned (SKILL § Round 57 rule 4 carried). The work-area subtraction's owner (which appbar occupies the band)
is not observed — no Shell surface is queried — and the documented 0-failure return classes (a current mode that
fails to report; a zero frequency/dimension/bpp) are treated as CHECK FAILED, never a measurement
(`corpus/knowledge/windows-display-topology-r61.md` H19/H20, J17).

| Tool | Reads | Writes | Owner and adjacent lanes |
|---|---|---|---|
| `tools/mado-win-display.py` | live mode: the JSON stdout of exactly one spawned read-only PowerShell child (`--powershell`, default `powershell.exe`, resolved on PATH) running a fixed embedded script whose only inputs are the user32 getters `EnumDisplayMonitors` and `GetMonitorInfoW` (MONITORINFOEXW fill) and the `EnumDisplaySettingsW` mode family (device name taken from the enumeration, never guessed); `--from-file`: one caller-named JSON snapshot (4 MiB cap); `--selftest`: nothing (in-memory; ephemeral fixtures in a private temp dir it removes) | nothing — stdout only (one `MADO_WINDISPLAY:`/`MADO_WINDISPLAY_SELFTEST:` line plus one JSON object line); it never prints window titles, process names, window handles, clipboard, environment values or file contents, and never echoes raw child output | mado, round 61 (read-only observation of the native topology + mode layer: point-in-time, no privileged API, no mutation, no rendered-output claim); operator applies any change; kagi keeps secret-shaped values (titles and names are not collected at all) |
| `tools/mado-win-dwm.py` | live mode: the JSON stdout of exactly one spawned read-only PowerShell child (`--powershell`, default `powershell.exe`, resolved on PATH) running a fixed embedded script whose only inputs are the dwmapi getters `DwmIsCompositionEnabled`, `DwmGetWindowAttribute` (DWMWA_CLOAKED per enumerated top-level window; DWMWA_EXTENDED_FRAME_BOUNDS for the probe's own console/foreground window) and `DwmGetCompositionTimingInfo` (both documented call shapes; the non-NULL shape recorded, never asserted), plus the user32 getters `EnumWindows`, `IsWindowVisible`, `IsWindow`, `GetWindowRect`, `GetConsoleWindow` and `GetForegroundWindow`; `--from-file`: one caller-named JSON snapshot (4 MiB cap); `--selftest`: nothing (in-memory; ephemeral fixtures in a private temp dir it removes) | nothing — stdout only (one `MADO_WINDWM:`/`MADO_WINDWM_SELFTEST:` line plus one JSON object line); it never prints window titles, process names, window handles, clipboard, environment values or file contents, and never echoes raw child output | mado, round 62 (read-only observation of the DWM client-attribute plane: point-in-time counts and reason buckets, no per-window rows, no privileged API, no mutation, no rendered-output claim); operator applies any change; kagi keeps secret-shaped values (titles and names are not collected at all) |
| `tools/mado-win-displayconfig.py` | live mode: the JSON stdout of exactly one spawned read-only PowerShell child (`--powershell`, default `powershell.exe`, resolved on PATH) running a fixed embedded script whose only inputs are the user32 CCD getters `GetDisplayConfigBufferSizes` and `QueryDisplayConfig` (QDC_ONLY_ACTIVE_PATHS, `currentTopologyId` NULL per the documented requirement; the documented mutator `SetDisplayConfig` is named by neither artifact); `--from-file`: one caller-named JSON snapshot (4 MiB cap); `--selftest`: nothing (in-memory; ephemeral fixtures in a private temp dir it removes) | nothing — stdout only (one `MADO_WINDISPLAYCONFIG:`/`MADO_WINDISPLAYCONFIG_SELFTEST:` line plus one JSON object line); it never prints window titles, process names, window handles, adapter LUID halves, target/source id integers, device or monitor names, clipboard, environment values or file contents (the documented name getter `DisplayConfigGetDeviceInfo` is deliberately not called), and never echoes raw child output | mado, round 63 (read-only observation of the CCD path/target plane: point-in-time counts, rationals, flags and enum integers, no privileged API, no mutation, no rendered-output claim); operator applies any change; kagi keeps secret-shaped values (names and ids are not collected at all) |

**Round-62 refinement (append-only; one read-only tool; no new write surface):** `tools/mado-win-dwm.py`
observes the DWM client-attribute plane read-only. Live mode spawns exactly one PowerShell child
(`--powershell`, default `powershell.exe`) running a fixed embedded script whose only inputs are the
dwmapi getters — `DwmIsCompositionEnabled`, `DwmGetWindowAttribute` with `DWMWA_CLOAKED` per
enumerated top-level window (counts and the three documented reason buckets only: DWM_CLOAKED_APP /
DWM_CLOAKED_SHELL / DWM_CLOAKED_INHERITED — no per-window rows, no handles, no titles) and with
`DWMWA_EXTENDED_FRAME_BOUNDS` for the probe's own console window (fallback: the foreground window),
`DwmGetCompositionTimingInfo` in its two documented call shapes (the Windows 8.1+ NULL requirement,
and the non-NULL shape the page promises E_INVALIDARG for — recorded, never asserted: the host fails
both with `0x88980090`, entry finding D04) — and the user32 getters `EnumWindows`, `IsWindowVisible`,
`IsWindow`, `GetWindowRect`, `GetConsoleWindow`, `GetForegroundWindow` (fallback only). It parses its
stdout as JSON and re-prints whitelisted fields only; `--from-file` re-derives a verdict from a captured
snapshot (4 MiB cap); `--selftest` (11 assertions) spawns nothing. The verdict line is built from
structure only because the census counters churn with desktop activity (the churn class is named per
field in `.ufo/waves/round-62/receipts/windwm-live-churn-diff.txt`). It collects no window titles, no
process names and no window handles, never echoes raw child output, writes no file, opens no socket and
mutates nothing: no Set*/Move*/Change* verb exists in it, and cloaking, attribute writes and composition
changes stay operator-owned (SKILL § Round 57 rule 4 carried). Which cloaked windows are also
`IsWindowVisible` is not observed (J22's `[UNK]`: the layers are separate axes, the tool records
counts, never a per-window tabulation).

**Round-63 refinement (append-only; one read-only tool; no new write surface):** `tools/mado-win-displayconfig.py`
observes the CCD (DisplayConfig) path/target plane read-only — the second documented refresh getter the r62 D04
route named. Live mode spawns exactly one PowerShell child (`--powershell`, default `powershell.exe`) running a
fixed embedded script whose only inputs are the user32 getters `GetDisplayConfigBufferSizes` and
`QueryDisplayConfig` — called with `QDC_ONLY_ACTIVE_PATHS` (0x2) and `currentTopologyId = NULL` (the documented
requirement for any non-`QDC_DATABASE_CURRENT` flags value) — marshaling the documented structures
DISPLAYCONFIG_PATH_INFO / PATH_SOURCE_INFO / PATH_TARGET_INFO / MODE_INFO / TARGET_MODE / VIDEO_SIGNAL_INFO /
RATIONAL / 2DREGION (the adapter LUID carried as two 32-bit layout halves, never emitted). It parses its stdout as
JSON and re-prints whitelisted fields only (counts, rationals, flags, enum integers — no adapter LUID halves, no
target/source ids, no device or monitor names; the documented name getter `DisplayConfigGetDeviceInfo` is
deliberately not called); `--from-file` re-derives a verdict from a captured snapshot (4 MiB cap); `--selftest`
(13 assertions) spawns nothing. Sanity layers treat the documented failure return classes as CHECK FAILED never a
measurement, require `DISPLAYCONFIG_PATH_ACTIVE` on every returned path, a positive refresh rational, in-bounds
mode indexes and the documented SOURCE=1/TARGET=2 vocabulary, and record the undocumented 0xFFFFFFFE sentinel the
host writes into the target mode's frequency fields as `vsync=unavailable(0xfffffffe)` — recorded, never guessed
at (entry finding D05, cause `[UNK]`). It collects no window titles, no process names, no window handles, never
echoes raw child output, writes no file, opens no socket and mutates nothing: no Set*/Change* verb exists in it,
and topology, mode and refresh changes stay operator-owned (SKILL § Round 57 rule 4 carried).

**Round-64 refinement (append-only; one read-only tool; no new write surface):** `tools/mado-receipt-citecheck.py`
audits the lane's own record hygiene read-only — it extracts repo-relative committed file-path citations from
caller-named artifacts (strict anchored grammar: the token must start with a lane top — `.ufo/ corpus/ tools/
quality/ plans/` — at a token boundary, and its last segment must carry an extension; bare-directory tokens,
rev-prefixed `rev:path` forms, absolute host paths and URLs are not citations) and verifies every extracted path
resolves in the git tree at `--rev`, using exactly one `git ls-tree -r --name-only <rev>` child per run. MISSING
citations are named with their citing files, never silently skipped; files over a 4 MiB read cap are skipped and
counted. `--selftest` (12 assertions) is hermetic: pure functions over in-memory fixtures plus a private temp
tree under the caller-declared `--scratch-root` (M57-1 policy; `/tmp` refused), removed at exit; it spawns
nothing. The tool writes nothing, opens no socket and mutates nothing; its scan scope is the paths the caller
names, and it is never run over r56-era material (the standing security boundary). First working demonstration
(round 64): the red run at the r63 base rev reports exactly the closure's routed citation
(`.ufo/waves/round-63/receipts/broken-fixture.json`, from `windisplayconfig-error-path.txt`) MISSING with
`TARGET_MISSED` rc=1, and the landing-state run reports `TARGET_MET` after the fixture landed — the ephemeral-
fixture class the r63 closure routed by hand is now a standing one-command check.

### Surface state register (2026-11-03, this host re-observed; supersedes the 2026-10-31 Windows-host block — append-only record)

Provenance: every state cell below was re-observed read-only on the returned omarchy host on 2026-11-03 by round-65 wave w1 seat R65ExecRegisterBlock (each probe command run verbatim today, exit codes in that seat's report), and each row's receipt pointer is committed under .ufo/waves/round-65/receipts/ at the round-65 landing revision; the 2026-10-31 block above stays as the frozen Windows-host record and nothing in it is claimed about this host.

| surface group | state (date) | probe (read-only) | receipt |
|---|---|---|---|
| hypr plane | present (2026-11-03): `~/.config/hypr` present (root conf 32 L, include graph 18/18 PASS in the file-plane gate); `hyprctl` answers the live session — Hyprland 0.56.2, 1 instance (pid 1665, wayland-1) | `command -v hyprctl && hyprctl version && hyprctl instances -j && test -d ~/.config/hypr` | .ufo/waves/round-65/receipts/before-register-probes-r65.txt .ufo/waves/round-65/receipts/gate-live-r65.txt |
| waybar | present (2026-11-03): `~/.config/waybar` present (config.jsonc 260 L); waybar v0.15.0 running (pid 1720; DP-1 top layer 3440x26 PASS in the live gate) | `command -v waybar && waybar --version && pgrep -x waybar && test -d ~/.config/waybar` | .ufo/waves/round-65/receipts/before-register-probes-r65.txt .ufo/waves/round-65/receipts/gate-live-r65.txt |
| walker | present (2026-11-03): `~/.config/walker` present; walker 2.17.2; app-walker@autostart.service and elephant.service both active | `command -v walker && walker --version && test -d ~/.config/walker && systemctl --user is-active app-walker@autostart.service elephant.service` | .ufo/waves/round-65/receipts/before-register-probes-r65.txt .ufo/waves/round-65/receipts/gate-live-r65.txt |
| terminal configs | present (2026-11-03): `~/.config/alacritty`, `foot`, `kitty`, `ghostty` all present; alacritty is the only installed consumer (foot, kitty and ghostty binaries are not on PATH — gate theme.parts.declared_only NOTE); font 12.5 and padding 14 agree across the four configs (gate terms.* PASS) | `for d in alacritty foot kitty ghostty; do if test -d "$HOME/.config/$d"; then echo "$d config present"; else echo "$d config missing"; fi; if command -v "$d" >/dev/null; then echo "$d bin present"; else echo "$d bin not found"; fi; done` | .ufo/waves/round-65/receipts/gate-fileplane-r65.txt .ufo/waves/round-65/receipts/before-register-probes-r65.txt |
| theme/wallpaper omarchy plane | present (2026-11-03): `~/.config/omarchy` and `~/.local/share/omarchy` present; theme.name = matte-black; `current/background` → theme backgrounds/0-ship-at-sea.jpg; theme chain 9/9 PASS with 1 declared-only NOTE in the file-plane gate; swayosd binary absent, so its theme css part has no consumer | `test -d ~/.config/omarchy && test -d ~/.local/share/omarchy && cat ~/.config/omarchy/current/theme.name && readlink ~/.config/omarchy/current/background && if command -v swayosd >/dev/null; then echo "swayosd present"; else echo "swayosd not found"; fi` | .ufo/waves/round-65/receipts/gate-fileplane-r65.txt .ufo/waves/round-65/receipts/before-register-probes-r65.txt |
| idle/lock plane | binaries present, no live consumer (2026-11-03): hypridle, hyprlock and hyprsunset all on PATH (under /usr/bin); `pgrep -x` finds no process for any of the three — the declared 150s/152s idle chain has no consumer (F1/S1, operator-owned) | `for b in hypridle hyprlock hyprsunset; do printf '%s ' "$b"; command -v "$b"; done; for p in hypridle hyprlock hyprsunset; do if pgrep -x "$p" >/dev/null; then echo "$p: running"; else echo "$p: no process"; fi; done` | .ufo/waves/round-65/receipts/before-register-probes-r65.txt .ufo/waves/round-65/receipts/gate-live-r65.txt |
| omarchy skill docs | present (2026-11-03): `~/.agents/skills/omarchy` is a symlink → /home/vgpnk/.local/share/omarchy/default/omarchy-skill (one leaf file; sha256 becd149e… and version 3.8.3 held by the file-plane gate) | `test -d ~/.agents/skills/omarchy && readlink -f ~/.agents/skills/omarchy` | .ufo/waves/round-65/receipts/before-register-probes-r65.txt .ufo/waves/round-65/receipts/gate-fileplane-r65.txt |
| windows desktop plane | not re-derivable on this host (2026-11-03): no powershell.exe, pwsh or powershell on PATH, so the read-only Windows instruments (`tools/mado-win-desk.py` and successors) cannot run here; the r57–64 Windows records stand (`corpus/knowledge/windows-desktop-plane-r57.md`), not retired; the absence probe is committed as a receipt and its in-memory selftest re-runs 10/10 on this host | `for b in powershell.exe pwsh powershell; do printf '%s ' "$b"; if command -v "$b" >/dev/null; then echo present; else echo 'not found'; fi; done` | .ufo/waves/round-65/receipts/windows-plane-absence-r65.txt |

<!-- r65 register end -->

**Round-67 refinement — no new desktop/write surface.** `quality/counters/c1-r67-register.py`
requires the returned-host register block to cite the live receipt inside a table row's receipt
cell (the r66 tree-level check accepted an unreferenced live object) and scores the frozen six-case
control set; `quality/counters/c2-r67-landing-controls.py` extracts the standing landing instrument
at a revision, runs its own selftest and kills the two named defect mutants (the zero-citation guard
clause and a child's `GIT_NO_REPLACE_OBJECTS`). The landing script gains one zero-citation selftest
case and the git-reading children set the replacement-object guard themselves. These are lane record
instruments: they do not measure state-cell truth, authenticate children, or protect a repository
already rewritten. Evidence: `corpus/lessons/round-67.md`,
`corpus/knowledge/replace-ref-citation-boundaries-r67.md`.


**Round-65 refinement (append-only; two record counters, one standing instrument, no new write surface):** the round-65 instruments are `quality/counters/c1-r65-register.py` (reads git objects at `--rev`, checks the register block above; writes nothing), `quality/counters/c2-r65-landing-instrument.py` (a read-only driver that extracts its own four dependencies into scratch and runs `quality/landing-counters.sh`; refuses /tmp-family and symlink scratch roots), and `quality/landing-counters.sh` (four legs: navigation, used-by, ledger, citecheck; each leg rc captured; `MADO_LANDING_COUNTERS: GREEN|RED`). They score the lane’s own record and the receipts it lands; none touches a config plane, a compositor socket or a host service. The omarchy-host freshness and gate-selftest rubrics are re-derived by the committed round-65 gate receipts (`.ufo/waves/round-65/receipts/gate-fileplane-r65.txt`, `gate-live-r65.txt`).

**Round-66 refinement — no new desktop/write surface.** `quality/counters/c1-r66-register.py`
checks unique heading/group rows, row-local resolving receipts and the exact committed live-gate
line; it reads Git objects only. `quality/counters/c2-r66-landing-instrument.py` extracts the
standing script and dependencies at a revision, runs its selftest and real round-66 landing
inside caller scratch, and removes its private work. `quality/landing-counters.sh` now requires
`--round N` and binds child markers to actual exit status: GREEN/0, genuine RED/1, ERROR/2.
These are lane record instruments, not desktop-state or child-honesty proofs. The live receipt
check is tree-level: an unreferenced live object can satisfy it; forged state cells remain
unmeasured. Existing r65 counter files stay unchanged; the r65 standing script is preserved
at its historical revisions, while its current path is the r66 cutover. No historical invocation
is claimed valid against unpinned current bytes. Evidence: `corpus/lessons/round-66.md`.

**Round-68 refinement (append-only; three lane record instruments and twelve gate envs; no new desktop or write surface.)**
The round adds `quality/counters/c1-r68-landing-controls.py` (a control harness whose `--selftest`
drives its own measurement body with scripted children), `quality/counters/c1-r68-selfmutants.py`
(three frozen forced-credit recipes scored against that harness and against the pinned r67
harness) and `quality/counters/c2-r68-reader-guard.py` (a census of the standing gate population's
git-object reads and their `GIT_NO_REPLACE_OBJECTS` construction). The population is exactly the
tracked `quality/check-*.py` set at the scored revision; per-round counters and their pinned
history are outside it. Twelve of those gates gain a guard key in their own git environment; their
argv, stdout and exit codes are unchanged. All three instruments read git objects and write only
caller scratch (the census writes nothing). None touches a config plane, the compositor, a socket
or a host service, and the census's guard is presence-tested, not interpreted. Evidence:
`corpus/lessons/round-68.md`.

**Round-69 refinement (append-only; three lane record instruments and one gate population unchanged; no new desktop or write surface.)**
The round adds `quality/counters/c1-r69-landing-controls.py` (the round-68 harness successor: its `--selftest`
drives the real measurement body with scripted children and pairs each decision with its oracle),
`quality/counters/c1-r69-paired-recipes.py` (three frozen paired recipes scored against that harness and against
the pinned r68 harness at the base revision) and `quality/counters/c2-r69-guard-dominance.py` (the guard census,
now requiring key position and dominance: the guarded environment must reach a `git` launch by an inline `env=`,
an env-named binding or local producer with no intervening unguarded rebinding, or a one-hop argument matched to
the callee's env-named parameter). The population is unchanged: exactly the tracked `quality/check-*.py` set at
the scored revision (20 files, 13 readers, 13 guarded). All three instruments read git objects and write only
caller scratch (the census writes nothing). None touches a config plane, the compositor, a socket or a host
service, and the dominance rule is a bounded syntactic approximation, not a runtime proof. Evidence:
`corpus/lessons/round-69.md`.

**Round-70 refinement — three lane record instruments; no new desktop/write surface.**
`quality/counters/c1-r70-landing-controls.py` is the successor credit harness;
`quality/counters/c1-r70-real-children.py` builds scratch Git fixtures and launches real Bash
children to score its three frozen scenarios; `quality/counters/c2-r70-carriers.py` reads Git
objects and classifies the unchanged 20-file check population against the 17-case carrier set.
All writes and fixture subprocesses stay in caller scratch; no config plane, compositor,
session, socket or service is probed. The classifiers are bounded source approximations, not
runtime guarantees. See `corpus/lessons/round-70.md` for the review repairs and remaining limits.

**Round-71 refinement — one successor harness, two record counters; no new desktop/write surface.** `quality/counters/c1-r71-landing-controls.py` is the landing harness's round-71 successor: the M-Z kill credit follows the child's own parsed `MADO_LANDING_COUNTERS_SELFTEST: p/n assertions passed` summary with `p < n` whatever the child's exit status (the round-70 `mz_rc != 0` conjunct is dropped); a crash or an unparseable summary still earns no credit, and both captured streams are read in the round-70 concatenation order. `quality/counters/c1-r71-real-children.py` drives that harness and the byte-frozen round-70 harness with four real `bash` children whose exit status disagrees with their own summary (`liar-success`, `stderr-genuine`, `liar-kill`, `crash-stderr`) in a scratch git fixture the counter builds. `quality/counters/c2-r71-shapes.py` extends the carrier census with four shapes — a `dict(<args>, **module_mapping)` call splat, the splat through a one-hop alias of that mapping, a key store through a one-hop alias of the mapping handed to the launch, and an attribute store bridged to a dotted use by one object-alias edge — each under the held dominance test, with the round-70 seventeen-case set carried forward byte-identically. All three are record instruments: they score the lane's own landing evidence, never a compositor, a config plane or a host service. Evidence: `corpus/lessons/round-71.md`, `corpus/knowledge/kill-credit-exit-disagreement-r71.md`, `corpus/knowledge/guard-carrier-shapes-r71.md`.

**Round-72 refinement — one successor harness, two record counters; no new desktop/write surface.**
`quality/counters/c1-r72-landing-controls.py` is the landing harness's round-72 generation, carrying
two disjoint rule deltas: the M-Z kill credit now requires the last parsed `p/n` summary to report a
shortfall AND the run's own `SELFTEST FAIL` lines to number exactly that shortfall (a bare or replayed
summary line earns no credit), and the contract verdict now reads the extracted instrument's last
parsed summary (`n > 0` and `p == n`) instead of its exit status. `quality/counters/c1-r72-summary-credit.py`
builds a scratch git fixture lane in eight summary modes and scores that harness against the
byte-frozen round-71 harness (8/8 vs 6/8); `quality/counters/c2-r72-outcome.py` loads both harnesses
and scores the committed outcome functions on eight frozen `(summary, rc, killed)` cases (8/8 vs 4/8).
All three read git objects, launch only their own fixture children, and write caller scratch only;
no config plane, compositor, session, socket or service is probed, and the rules remain bounded
syntactic/evidence reads, not authentication of a forged report. Evidence: `corpus/lessons/round-72.md`.

**Round-73 refinement — the control set as an instrument and two more guard carriers; no new desktop/write surface.**
`quality/counters/c1-r73-summary-mutants.py` extracts the round-72 outcome rule at `--rev` and
scores four named literal mutations of it against the round-73 ten-case set and the held eight-case
set (4/4 vs 2/4); the ten cases are the round-72 eight carried byte-identically plus
`zero-denominator` and `valid-then-garbled`, each the sole separator of one mutation.
`quality/counters/c2-r73-shapes.py` is the guard census's round-73 generation: the held round-71
classifier plus a `global`-declared store detector and a mutated-`os.environ` transport detector,
scoring 28 frozen cases (28/28 vs 25/28) over the unchanged `quality/check-*.py` population
(20 files, 13 readers, 13 guarded). Both read git objects and committed bytes, write caller scratch
only, and never probe a config plane, compositor, session, socket or service. The census remains a
bounded syntactic approximation: line order not execution order, one `global` declaration, one
`os.environ` store and two copy spellings, no value interpretation. Evidence:
`corpus/lessons/round-73.md`.

**Round-74 refinement (append-only; three record instruments, no new write surface):**
`quality/counters/c1-r74-witness-rule.py` is the successor landing-credit rule — the round-72
arithmetic plus the run's last parsed `MADO_LANDING_WITNESS: <16 hex>` echo of a caller-supplied
per-run challenge; it reads only the output text it is handed, writes nothing, and its `--selftest`
is hermetic. `quality/counters/c1-r74-replay-witness.py` builds twelve `bash` fixture lanes inside
the caller-declared scratch root (each with the landing harness's zero-citation clause deleted
exactly once), runs each child with a fresh `secrets.token_hex(8)` challenge in
`MADO_LANDING_NONCE`, and scores the successor rule against the held round-72 rule on the same
outputs (12/12 vs 8/12); it starts only `bash` children and `git show` reads, and writes scratch
only. `quality/counters/c2-r74-shapes.py` is the guard census's round-74 generation: the held
round-73 classifier plus a one-hop object-alias resolver (`r = cfg.runner`, store at `r.env[KEY]`,
launch at `env=cfg.runner.env` or the reverse) and a one-hop `os.environ` alias detector
(`env = os.environ`; store; `env=env`, `dict(env)` or `{**env}`), scoring 36 frozen cases (36/36 vs
32/36) over the unchanged `quality/check-*.py` population (20 files, 13 readers, 13 guarded). All
three read committed bytes and caller scratch, never a config plane, compositor, session, socket or
service; the census remains a bounded syntactic approximation (line order not execution order, one
alias edge, no chain, no value interpretation). Evidence: `corpus/lessons/round-74.md`.

The round-75 generation moves the same two instruments one surface further, still read-only.
`quality/counters/c1-r75-landing-controls.py` loads the frozen round-72 harness from the measured
repository under a sha256 pin (`b6108c86…`), draws one `secrets.token_hex(8)` challenge per run,
hands it to the child in `MADO_LANDING_NONCE` (the child-env evidence line redacts the value), and
credits the M-Z kill and the outcome green only when the child's last parsed
`MADO_LANDING_WITNESS: <16 hex>` equals it; the extraction, the instrument selftest, the M-Z clause
deletion and the M-R pair are the frozen round-72 code. `quality/counters/c1-r75-harness-witness.py`
scores eleven real `bash` fixture lanes through that pipeline (11/11 vs the held 6/11).
`quality/counters/c2-r75-shapes.py` adds a name-neutral keyed-mapping rule (a mapping carrying the
guard key in key position bound to any simple name and handed as `env=`, under the dominance test)
and a literal-key `del env[KEY]` cancellation between the guard construction and the launch,
scoring 47 frozen cases (47/47 vs 41/47) over the unchanged `quality/check-*.py` population
(20 files, 13 readers, 13 guarded); `quality/landing-counters.sh` adds a nonce-gated witness echo
that prints nothing when no challenge is supplied. All read committed bytes and caller scratch,
never a config plane, compositor, session, socket or service; the census remains a bounded
syntactic approximation, and the challenge authenticates the run's echo, not the truth of the
assertions. Evidence: `corpus/lessons/round-75.md`.

Round 76 (2026-11-04) adds two read-only instrument surfaces inside the lane's own tooling scope,
not the desktop plane: `quality/counters/c1-r76-landing-controls.py` and `c1-r76-outcome-field.py`
score the frozen round-72 landing harness's M-Z decision and its contract outcome field over
sixteen real `bash` fixture modes (four named mutations of the named `outcome_green` rule killed
4/4; the echo-dropping class recorded unobservable because `killed == 2` already requires the
echo), and `quality/counters/c2-r76-shapes.py` extends the guard census with an interprocedural
cancellation (a callee deleting the guard key from the mapping it receives, under the dominance
test) and a dynamic-key `del` resolved through a same-scope single-binding constant, scoring 59
frozen cases (59/59 vs the held 55/59) over the unchanged `quality/check-*.py` population
(20 files, 13 readers, 13 guarded). All three read committed bytes and caller scratch only; no
config plane, compositor, session, socket or service is touched, and the census remains a bounded
syntactic approximation. Evidence: `corpus/lessons/round-76.md`.

**Round-77 refinement (append-only; one read-only tool, two record counters, one knowledge entry; no new write surface):**
the bar-footprint join is a lane instrument over the layer plane the lane already owns (the bar/launcher
consumer chain), not a new desktop surface. `tools/mado-barfoot.py` reads only the files its caller names —
the waybar JSONC config, at most one captured `hyprctl layers -j` reply and one captured
`hyprctl monitors -j` reply (regular files or stdin, 1 MiB cap, symlinks refused) — and writes nothing; it
starts no process and opens no socket. Its verdict is a prediction/join over captured bytes, never a
compositor mutation, and the operator applies any change. `quality/counters/c1-r77-barfoot.py` extracts the
tool from `--rev` and scores fifteen frozen artifacts in private caller scratch (git reads only; no host
write); `quality/counters/c2-r77-runbook.py` runs the twelve frozen read verbs of the SKILL.md probe table in
the caller's session environment (read verbs only; stdout only; no host or repo write). The knowledge entry
`corpus/knowledge/bar-footprint-r77.md` is documentation of the layer/declared-bar plane; the host join it
records was captured read-only (2026-11-04). No config tree, compositor state, service or sibling repo is
written by this round.

**Round-79 refinement (append-only; one read-only input, no new write surface):** `tools/mado-barfoot.py`
gains an optional `--rules` input — the Hyprland config file that declares the joined monitor's
`monitor =` rules — from which it derives the static reserved area (`addreserved`, written TOP,
BOTTOM, LEFT, RIGHT) and composes it under the bar's own band. It reads that one regular file
(1 MiB cap, symlinks/FIFOs/devices refused, UTF-8 required) and the same three caller-supplied
artifacts as before; it writes nothing, starts no process and opens no socket. A rules file carrying
a `source =` line, a `$`-bearing rule or a non-integer `addreserved` field is refused (`stage=model`)
rather than guessed, as are the four documented refusals the round-79 runbook executes (a `mode`
preset, a scaled monitor, the `background` layer, a spaced output pattern). The round's record
instruments (`quality/counters/c1-r79-reserve.py`, `c2-r79-runbook.py`) read committed bytes and
caller scratch only; the C2 counter executes the lane's read verbs and that read-only join. No
config tree, compositor, service or sibling repo is written by this round.

**Round-80 refinement (append-only; one read-only declaration, no new write surface):**
`tools/mado-barfoot.py` gains an optional `--surfaces` input — a caller-supplied JSON list of the
layer surfaces the join should compose (namespace, level, anchor, desired size, margins, requested
exclusive zone, exclusive edge, rule order) — and, when at least one entry is present, arranges
every declared surface in level order against the running usable box and attributes each exclusive
surface's shrink by the first matching edge. It reads that one regular file (1 MiB cap,
symlinks/FIFOs/devices refused) beside the same three caller-supplied artifacts; it writes nothing,
starts no process and opens no socket. A declaration the compositor would refuse is refused
(`stage=model`) rather than guessed: an `exclusiveEdge` outside the declared anchor set, a level
outside 0–3, a non-integer margin or an unknown position. The round's record instruments
(`quality/counters/c1-r80-multisurface.py`, `c2-r80-runbook.py`) read committed bytes and caller
scratch only; the C2 counter executes the lane's read verbs and that read-only join. The knowledge
entry `corpus/knowledge/bar-footprint-composition-r80.md` is documentation of the layer plane the
lane already owns; the host join it records was captured read-only. No config tree, compositor,
service or sibling repo is written by this round.

**Round-81 refinement (append-only).** The same read-only join now models the box rounding the
compositor applies after arranging a layer surface (hyprutils `CBox::round`, S478) and the auto
exclusive zone the client library actually sends (gtk-layer-shell's `horiz XOR vert` gate, the
allocation as its size, the unanchored margins — S464 held), and it *refuses* an auto zone whose
band size is dynamic instead of printing a zero band. It still reads only caller-supplied artifacts;
the declaration grammar's `exclusive` default remains `auto`, so a plain client must say `0`. The
round's record instruments (`quality/counters/c1-r81-overflow-auto.py`, `c2-r81-runbook.py`) read
committed bytes and caller scratch only; the C2 counter executes the lane's read verbs, including
`omarchy menu keybindings --print` and `pgrep -x waybar`, both non-mutating. The knowledge entry
`corpus/knowledge/bar-footprint-rounding-auto-r81.md` documents the layer plane the lane already
owns; the host join it records was captured read-only with the monitor's identifying fields redacted.
No config tree, compositor, service or sibling repo is written by this round.

**Round-84 refinement — no new desktop or host-write surface.**
The r82/r83/r84 bar-footprint generations retain the supplied-file/read-only boundary.
Round84 refuses repeated declaration namespaces (bar included) and repeated allocation-object
keys; uniqueness is the instrument's grammar, not a protocol-wide identity guarantee.
`quality/counters/c1-r84-namespaces.py` reads Git objects, runs extracted tool copies and writes
caller scratch only. `quality/counters/c2-r84-runbook.py` executes the committed read-only runbook
verbs plus contained synthetic shell producers, never a custom live producer, writes caller
scratch only and emits output-size metadata instead of live stdout. Its fifteen pipeline guards
propagate nonzero status; a successful tail never proves live tray health.
The earlier source-only/no-live examples do not grant general execution authority: the round's
explicitly assigned frozen read verbs and contained fixtures are its bounded execution surface.
No config edit, reload, dispatcher, input capture, package transaction, screenshot, service
mutation or sibling-method ownership follows. Unit health remains tsukuroi's, mutation craft
tameshi's, and cross-lane orchestration/record tooling kumitate's; this lane owns only these
applications and evidence. See round84 connector report and the runbook interpretation caption.

**Round85 refinement — same read-only surface.** The layer join's exception metadata gains
literal identity-cause tokens and distinguishes repeated declaration sites without folding
namespace case. It still reads supplied files only. Round85 counters extract Git objects or
execute the same bounded runbook queries plus contained, finite stdout-only producers.
The numeric0/7/141 pipeline observations do not prove a unique termination cause, producer
truth, rendered UI or service health. OS diagnosis, reusable testing method and fleet record
governance remain sibling-owned; source docs support only this desktop-runbook application.
Frozen C2 failure and successor limitations are retained in lesson85, not province expansion.

**Round-87 refinement — read-only resolver, two record instruments; no new write surface.** `tools/mado-mako.py` resolves the effective
settings of one notification from the mako config bytes the caller names (`--config`, `--home`; regular files only; `include=` followed
under the manual's absolute or `~/` rule; `--mode` supplies the enabled set as an input). Its selftest writes only inside
`--scratch-root`; it starts no process and opens no socket. `quality/counters/c1-r87-mako-criteria.py` and
`quality/counters/c2-r87-control-fidelity.py` are record instruments: the first scores the tool over a frozen case set and two
do-nothing controls, the second re-derives the round-86 figures and reconciles them against append-only corrections. The lane reads
`~/.config/mako`; it never writes it, and the operator applies any change.

**Round-91 refinement — the default-application plane (read-only resolver); no new write surface.** The
question "which `.desktop` application opens this MIME type or URI scheme" (`xdg-open`, file managers and OpenURI reduce
to GLib's `g_app_info_get_default_for_type`) is in province: it is desktop behavior configured by Omarchy's
`~/.config/mimeapps.list` and `~/.config/<desktop>-mimeapps.list`. `tools/mado-mime.py` reads, read-only, only
`mimeapps.list`, `<desktop>-mimeapps.list`, `defaults.list`, `mimeinfo.cache` and `*.desktop` under the XDG config and
data roots (`~/.config`, `/etc/xdg`, `~/.local/share/applications`, `/usr/local/share/applications`,
`/usr/share/applications`), the `mime/{mime.cache,aliases,subclasses}` files under the data roots, and stats `PATH`
entries; it launches nothing and calls the C library's `qsort`/`bsearch` only to replay xdgmime's alias lookup.
Writing an association (`gio mime TYPE HANDLER`, `xdg-mime default`, `xdg-settings set`, `update-desktop-database`)
is operator-owned and never run by the lane.

**Round-91 refinement (C2) — one record gate; no new write surface.** `quality/check-seat-reports.py` reads the lane's own wave
dispatches (`--rev` reads committed bytes; `--worktree` reads the lane tree) and writes nothing.

**Round-92 refinement — `xdg-open`'s own resolver (read-only); no new write surface; corrects the round-91 refinement.**
The round-91 sentence "`xdg-open`, file managers and OpenURI reduce to GLib's `g_app_info_get_default_for_type`" is
wrong for `xdg-open` on this host: xdg-utils 1.2.1 maps the unrecognised `XDG_CURRENT_DESKTOP=Hyprland` to `generic`
(xdg-open.in:595-596) and asks `xdg-mime query default TYPE`, whose shell resolver `defapp_generic` differs from GLib
on 378 of the host's 1133 types (S508; `.ufo/waves/round-92/receipts/host-run-r92.txt`). Both resolvers are in
province: GLib's (`tools/mado-mime.py`) answers `gio open`, GTK and portal callers; xdg-utils' (`tools/mado-xdgmime.py`)
answers `xdg-open` and every program that shells out to it. `tools/mado-xdgmime.py` reads, read-only, the same
mimeapps/defaults/mimeinfo.cache/`*.desktop` files under the XDG config and data roots, lists directories for the
pathname expansions xdg-mime performs, and stats `PATH` entries and the working directory; it runs no program (not
xdg-mime, not a shell) and writes nothing (`--selftest` writes only ephemeral fixtures in a private temporary
directory). Launching (`xdg-open`, `gtk-launch`) and writing associations (`xdg-mime default`, `xdg-settings set`)
stay operator-owned and are never run by the lane.

**Round-92 refinement (C2) — the record gate fails closed; no new write surface.** `quality/check-seat-reports.py` still reads
only the lane's own wave dispatches and writes nothing; it now refuses (setup error) a dispatch path that is not a regular
file instead of skipping or blocking on it, and in `--worktree` it resolves real paths to keep reports inside the lane.

**Round-93 refinement (C1) — portal key-file bytes (read-only); no new write surface.** `tools/mado-portals.py` now reads
`portals.conf` and `.portal` files as bytes and applies GLib 2.90.1 GKeyFile's byte rules (S511–S514): UTF-8 is checked
when a value is read, VT is not whitespace, a NUL ends a line's C string. It still reads only the XDG config/data roots it is
given and writes nothing; editing `~/.config/xdg-desktop-portal/portals.conf` stays operator-owned.

**Round-93 refinement (C2) — one record gate; no new write surface.** `quality/check-selftest-strength.py` copies a lane
gate into scratch, applies the committed kill-set's mutants there and runs its `--selftest`; it reads only the lane tree and
writes only scratch.

**Round-94 refinement (C1) — file name → MIME type (read-only); no new write surface.** `tools/mado-mimeglob.py` reads
`mime.cache`, `globs2` and `globs` under the xdgmime data roots it is given (S515–S518, S505) and writes nothing; it
never runs `update-mime-database` or edits `~/.local/share/mime`, which stay operator-owned. Content sniffing is outside it.

**Round-94 refinement (C2) — two kill-sets; no new write surface.** `quality/selftest-kills/mado-xdgmime.json` and
`quality/selftest-kills/mado-mime.json` are data for the unchanged round-93 gate, which copies `tools/mado-xdgmime.py` or
`tools/mado-mime.py` into scratch, applies a kill there and runs its `--selftest`; nothing outside scratch is written.

**Round-95 refinement (C1) — file bytes → MIME type (read-only); no new write surface.** `tools/mado-mimesniff.py`
reads `mime.cache` (its magic, alias and parent sections, plus round 94's name step) under the xdgmime data roots it is
given and the files it is asked to sniff (S519–S523, S505), and writes nothing; it never runs `update-mime-database`
and never reads text `magic` files (that mode is refused). Its caller on this host is GIO's `standard::content-type`;
`xdg-open` on Hyprland uses `file(1)` (revenger's ground for libmagic rules) and is outside it.

**Round-95 refinement (C2) — two kill-sets; no new write surface.** `quality/selftest-kills/mado-mimeglob.json` and
`quality/selftest-kills/mado-portals.json` are data for the unchanged round-93 gate, which copies `tools/mado-mimeglob.py`
or `tools/mado-portals.py` into scratch, applies a kill there and runs its `--selftest`; nothing outside scratch is
written. The gate's own selftest stays without a kill-set (lesson M95-3).


**Round-96 refinement (C1) — file bytes → MIME type in the TEXT database mode (read-only); no new write surface.**
`tools/mado-mimetext.py` reads the text `mime/magic` file (its `MIME-Magic` sections, matchlets,
word sizes and ranges, plus round 94's name step from `mime/globs2`/`mime/globs`) under the xdgmime
data roots it is given and the files it is asked to sniff (S524, S525, S505, S520, S521, S522), and
writes nothing; it never runs `update-mime-database`, never edits `~/.local/share/mime`, and refuses
(exit 3) any state where a loadable `mime.cache` exists in a reachable directory — that state is
round 95's `tools/mado-mimesniff.py`. Its callers are the same GIO `standard::content-type` path as
round 95, but only on a host whose reachable directories hold no loadable cache; `xdg-open` on
Hyprland still uses `file(1)` (revenger's ground) and is outside it.

**Round-97 refinement (C1) - a path's content type, not an input's (read-only); no new write surface.**
`tools/mado-filetype.py` stats the paths it is given (two-stage lstat then a guarded follow: a broken or
looped symlink answers `inode/symlink`, a directory/chardev/blockdev/FIFO/socket its `inode/*`, a
zero-size regular `application/x-zerosize`, and only a non-`EACCES` lstat failure is refused), then runs
round 94's basename guess and - only when that guess is uncertain and the full attribute is asked -
sniffs the file for the database's own max extent (clamped to 16384) through round 95's cache-mode or
round 96's text-mode matcher (S522, S526, S527, S518, S521, S524, S525). It reads the paths and the
reachable `mime/` trees only; it writes nothing, never launches an application and never asks `file(1)`
(revenger's ground). Its caller is a file manager's `standard::content-type`; `gio info -a` is the CLI
that exposes it.

**Round-98 refinement (C1) - the launch argv sequence (read-only); no new write surface.**
`tools/mado-execargv.py` models, from a desktop file's bytes and a FILE argument list, the argv
vectors GIO 2.90.1's `g_desktop_app_info_launch_uris_with_spawn` builds: the `[Desktop Entry]` read
(Exec, Name, Icon, Type, Path, Terminal, Hidden read but not refused), the `%` walk with the selector
byte consumed, the field codes (`%f %F %u %U %d %D %n %N %i %c %k %m %%` and the unknown-code drop),
the `force_file_uri` file-path rule, the head-pointer no-substitution fallback, `g_shell_quote`, the
`g_shell_parse_argv` grammar, and the one-process-per-iteration loop (S528-S532). It reads the desktop
file and stats the arguments it is given; it writes nothing, never launches a process, never reads
`~/.config`, and never asks `gio` or a shell to answer a modelled question. `gio launch` on a fixture
desktop file is the *oracle* the committed case set was measured against, never a runtime dependency
of the tool. Whether the launched process starts, `Terminal=true`'s terminal prepend, `Path=` as cwd,
DBus activation and the portal path stay frontier.

**Round-98 refinement (C2) - the registry citation read-back (read-only); no new write surface.**
`quality/check-sources-readback.py` reads `corpus/SOURCES.md` and `corpus/knowledge/*.md` and reports
R1 (a repo path in a `recheck` cell), R3 (a `used-by` path that does not exist), R4 (a `mined` row an
entry's `source:` frontmatter cites but whose `used-by` does not name that entry), R5 (a cited id with
no row) and R6 (a duplicate id); it writes nothing. The 21 repaired `used-by` cells are registry
records, not a new write surface: the registry is the lane's own corpus file and every change is
logged old -> new in `corpus/lessons/round-98.md`.

**Round-99 refinement (C1) - the launch spawn environment (read-only); no new write surface.**
`tools/mado-launchenv.py` models, from a desktop file's bytes, a FILE argument list and a `PATH`
string, what surrounds the argv vectors `tools/mado-execargv.py` already answers: the load gate
(`TryExec` then `Exec`, each through `g_find_program_for_path(program, process PATH, Path=)`, whose
failure is `Unable to load application information`), the `Terminal=true` prepend (the twelve
`known_terminals` in table order, each searched with the entry's `Path=` as working dir, the
`exec_arg` column, and `Unable to find terminal required for application` when none is found), the
post-prepend `argv[0]` lookup (`Program '<x>' not found in $PATH`), the child's cwd (`Path=`, with an
empty value inheriting and an unenterable one failing the spawn), and `GIO_LAUNCHED_DESKTOP_FILE`
(S532, S533, S534). It reads the desktop file and performs the same filesystem tests
`g_find_program_for_path` performs; it writes nothing, never launches a process, never reads
`~/.config`, and never asks `gio` or a shell to answer a modelled question. `gio launch` on a fixture
desktop file under a case-controlled PATH is the *oracle* the committed case set was measured
against, never a runtime dependency of the tool. Whether the launched process survives, the
`gio-launch-desktop` wrapper's own environment handling, `DBusActivatable` activation and the portal
path stay frontier.

**Round-99 refinement (C2) - the harm watch as an instrument (read-only); no new write surface.**
`quality/harm-watch.py` replays a frozen panel of the lane's prior counting-command legs, each with a
frozen expected exit status and a stdout marker, and its census fails closed on a leg the panel
declares but does not carry (`PANEL_LEG_COUNT`, `PANEL_DUPLICATE`, `PANEL_ROUND_MISSING`,
`PANEL_LEG_UNKNOWN`, `PANEL_LEG_MISSING`). It runs each leg as a child process in the lane tree and
writes nothing outside the caller's scratch; the panel is the record, and a leg whose expectation
must change is re-frozen in the round that changes it.
