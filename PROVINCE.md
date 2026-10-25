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
