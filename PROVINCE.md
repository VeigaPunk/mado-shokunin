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
