# R99MConnector — UFO-FSD Connector Report (Round mado 99, Wave w1)

**Seat**: `R99MConnector`  
**Role**: UFO-FSD connector / leaf member  
**Report target**: `.ufo/waves/round-99/w1/R99MConnector.md`  
**Receipt target**: `.ufo/waves/round-99/receipts/connector-sweep-r99.txt`  
**Lane root**: `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Base revision**: `2cbaa141f42df9dfeee4d207cae6558a4dd59863` (`master`)  
**Declared axes**:
- **C1 `coverage`** (capability, new surface): The launch spawn environment surrounding desktop entry argv vectors (`tools/mado-launchenv.py` modeling the load gate, `Terminal=true` selection and prepend, `Path=` working directory, post-prepend `argv[0]` lookup, `GIO_LAUNCHED_DESKTOP_FILE`, and `g_find_program_for_path` semantics from `gio/gdesktopappinfo.c` and `glib/gutils.c`).
- **C2 `operability`** (instrument & regression panel): The harm watch replay instrument (`quality/harm-watch.py`) and frozen test leg panel (`.ufo/waves/round-99/controls/harm-panel-r99.json`), verifying census integrity and zero regression mismatches across historical round counter legs without dropping legs.

---

## 1. Sibling-Overlap Scan (Adjacency Axis, Read-Only)

An exhaustive, read-only sweep was conducted across all 20 sibling lanes in `/home/vgpnk/Projects/shokunin/*-shokunin/`. For every lane, we inspected `PROVINCE.md` and searched all Markdown files under `corpus/knowledge/` for the C1 and C2 surfaces:
- **C1 Surface**: `Terminal=`, `Path=` as a desktop-entry key, `g_find_program_for_path`, `prepend_terminal_to_vector`, `GIO_LAUNCHED_DESKTOP_FILE`, `gio launch`.
- **C2 Surface**: `harm watch`, `harm-watch.py`, `replay panel`, `harm-panel.json`, `leg census`, `PANEL_LEG`.

Raw findings with line counts and located citations are recorded in committed receipt `.ufo/waves/round-99/receipts/connector-sweep-r99.txt`.

### 1.1 Sibling Sweep Findings Per Lane

1. **`audio-shokunin`** (`audio-shokunin/PROVINCE.md:1-53`, 18 knowledge files):
   - **C1 Surface**: **SILENT**. PROVINCE owns game audio production (SFX, ambience, interactive soundtracks; `PROVINCE.md:2-5`); 0 hits in `corpus/knowledge/`.
   - **C2 Surface**: **SILENT**. Standard SOURCES usage; 0 harm watch / replay panel claims.

2. **`chousa-shokunin`** (`chousa-shokunin/PROVINCE.md:1-17`, 95 knowledge files):
   - **C1 Surface**: **SILENT**. PROVINCE owns deep-research method (question framing, claim-vs-source verification; `PROVINCE.md:3-6`); 0 hits in `corpus/knowledge/`.
   - **C2 Surface**: **SILENT**. Owns research methodology, not lane harm watch instruments.

3. **`game-dev-2d-shokunin`** (`game-dev-2d-shokunin/PROVINCE.md:1-38`, 5 knowledge files):
   - **C1 Surface**: **ADJACENT (Game Engine Test Loops Only)**. PROVINCE lines 18 and 23 cite headless Godot/Unity 2D engine test loops (`save/load and export/launch`); 0 desktop entry, field code, or GIO mentions.
   - **C2 Surface**: **SILENT**. Standard SOURCES usage; 0 harm watch claims.

4. **`game-dev-3d-shokunin`** (`game-dev-3d-shokunin/PROVINCE.md:1-82`, 5 knowledge files):
   - **C1 Surface**: **ADJACENT (Explicit Deferral to mado)**. PROVINCE line 75 explicitly declares:
     > *"Desktop/compositor display behavior belongs to `mado-shokunin` (`../mado-shokunin/PROVINCE.md:3-12`)."*
     0 desktop entry or GIO hits in `corpus/knowledge/`.
   - **C2 Surface**: **SILENT**. 0 harm watch claims.

5. **`kagi-shokunin`** (`kagi-shokunin/PROVINCE.md:1-114`, 43 knowledge files):
   - **C1 Surface**: **SILENT**. PROVINCE owns secret and vault operations; line 112 mentions *"operator-owned terminal actions"* (terminal ops, not desktop entries); 0 hits for desktop keys or GIO functions.
   - **C2 Surface**: **SILENT**. PROVINCE lines 8, 36, 67, 72, 78 detail lane-local census gates (`surface-census.sh`, `drift-pins.sh`, `scope-gate.sh`, `sources-census.sh`). None claim fleet harm watch or leg replay panels.

6. **`kaidoku-shokunin`** (`kaidoku-shokunin/PROVINCE.md:1-779`, 184 knowledge files):
   - **C1 Surface**: **ADJACENT (Forensic Observation of Shipped Artifacts)**. PROVINCE line 139 notes CDP/V8 inspection targets; `corpus/knowledge/2026-10-13-r4-06-1password-asar.md:213` contains `saveContentToFile(content=t, filename=n, appPath=o)` (an internal JavaScript parameter name, not a desktop entry key). Kaidoku inspects packed binaries and Electron asar archives; it models no desktop entry launch grammar.
   - **C2 Surface**: **ADJACENT (Lane-Local Record Audits)**. PROVINCE lines 530, 544 note `tools/round-71/registry-census.py` and `tools/round-72/capsule-audit.py` for kaidoku's own witnesses; 0 harm watch tools.

7. **`kake-shokunin`** (`kake-shokunin/PROVINCE.md:1-747`, 86 knowledge files):
   - **C1 Surface**: **ADJACENT (Lexical Token Hit)**. `corpus/knowledge/fleet-registry.md:70` has `updatePath == "kimi-websites-surface"` (a script variable name, not a desktop key). 0 GIO or launch environment hits.
   - **C2 Surface**: **SILENT**. Web properties and publishing; 0 harm watch claims.

8. **`kama-shokunin`** (`kama-shokunin/PROVINCE.md:1-456`, 63 knowledge files):
   - **C1 Surface**: **SILENT**. Local model serving endpoints; 0 desktop entry or launch hits.
   - **C2 Surface**: **SILENT**. PROVINCE lines 17, 186, 302, 333, 357 note lane-local censuses (`hexrun-census.py`, `census-waiver-boundary.py`, `round80-ollama-census.py`); 0 historical replay panel tools.

9. **`kasegi-shokunin`** (`kasegi-shokunin/PROVINCE.md:1-237`, 107 knowledge files):
   - **C1 Surface**: **ADJACENT (Lexical Token Hits: HTTP Cookie Path)**. Token hits in `corpus/knowledge/cloud-signed-cookies-and-user-bound-sas.md:201, 202, 236, 237` are HTTP `Set-Cookie: CloudFront-Signature=...; Path=/` header specifications, completely distinct from Desktop Entry `Path=`. PROVINCE line 94 mentions file terminal blank lines. 0 GIO hits.
   - **C2 Surface**: **SILENT**. Bounty research; 0 harm watch claims.

10. **`kengaku-shokunin`** (`kengaku-shokunin/PROVINCE.md:1-1136`, 81 knowledge files):
    - **C1 Surface**: **ADJACENT (Lexical Token Hits: Terminal-Bench Benchmark)**. PROVINCE lines 136, 146, 222, 255-322, 394-463, 561-675, 977-991, 1122 cite "Terminal-Bench 2.0" evaluation tasks and test harnesses. PROVINCE lines 347, 348, 366, 379, 384, 587 explicitly cite mado's historical sandboxes (`c1-r40-live-v2.py`, `c1-r41-globals.py`). Kengaku evaluates models; it does not model desktop application launching.
    - **C2 Surface**: **SILENT**. PROVINCE line 914 notes a grader-class census (`CLASS-CENSUS`); 0 harm watch panel tools.

11. **`kotoba-shokunin`** (`kotoba-shokunin/PROVINCE.md:1-78`, 74 knowledge files):
    - **C1 Surface**: **SILENT (Explicit Recognition of mado)**. PROVINCE line 72 explicitly acknowledges:
      > `| mado | none | 62dd798b... | mado owns the Hyprland/waybar/walker/terminal config plane and display behavior read-only...`
      0 desktop entry or GIO hits.
    - **C2 Surface**: **SILENT**. Prompt and skill craft; 0 harm watch tools.

12. **`kotodama-shokunin`** (`kotodama-shokunin/PROVINCE.md:1-31`, 0 knowledge files):
    - **C1 Surface**: **SILENT**. Linguistic-cultural worldbuilding; 0 hits.
    - **C2 Surface**: **SILENT**. 0 hits.

13. **`kumitate-shokunin`** (`kumitate-shokunin/PROVINCE.md:1-75`, 92 knowledge files):
    - **C1 Surface**: **ADJACENT (Lexical Token Hits: JS Variable Names)**. In `corpus/knowledge/ops-watchers.md:41, 217, 242, 244` and `remaining-scripts-census.md:300, 304`, tokens match JavaScript variables (`d.configPath`, `process.execPath`, `resolveWatchStatePath`, `lastPath`). 0 desktop entry keys.
    - **C2 Surface**: **ADJACENT (Lane-Local Script Census)**. PROVINCE line 14 notes `scripts/kimi-census.mjs` and line 16 notes `scripts/omp-census.mjs`; 0 fleet harm watch tools.

14. **`lore-shokunin`** (`lore-shokunin/PROVINCE.md:1-35`, 25 knowledge files):
    - **C1 Surface**: **SILENT**. Fictional-world records; 0 hits.
    - **C2 Surface**: **SILENT**. 0 hits.

15. **`mori-shokunin`** (`mori-shokunin/PROVINCE.md:1-700`, 101 knowledge files):
    - **C1 Surface**: **SILENT**. PROVINCE lines 103, 104, 587, 593 cite `tools/mori-seat-terminal.py` for passive terminal-at-scan transcript status of agent sessions; 0 desktop entry launch hits.
    - **C2 Surface**: **ADJACENT (Host Observability Regressions)**. PROVINCE lines 580, 581, 586 cite `mori-round13-regressions.py` and `mori-round17-jj-regressions.py` testing synthetic watchdog/journal fixtures. Mori monitors host telemetry and watchdogs; it does not own the lane's harm watch panel.

16. **`revenger-shokunin`** (`revenger-shokunin/PROVINCE.md:1-59`, 28 knowledge files):
    - **C1 Surface**: **SILENT**. Binary reverse engineering; 0 hits.
    - **C2 Surface**: **SILENT**. 0 hits.

17. **`souji-shokunin`** (`souji-shokunin/PROVINCE.md:1-323`, 53 knowledge files):
    - **C1 Surface**: **ADJACENT (FreeDesktop Trash Specification Consumer)**. In `corpus/knowledge/trash-spec-restorable-quarantine.md:9, 21, 35`, souji cites the FreeDesktop Trash specification's `.trashinfo` format, where the key `Path=` records the original location of a trashed file (`Path=foo/bar/meow.bow-wow`). This is the FreeDesktop Trash spec, distinct from the Desktop Entry specification's `Path=` working directory key.
    - **C2 Surface**: **SILENT**. PROVINCE lines 109, 173, 318 note process and git repository censuses (`souji-proc-census.sh`); 0 harm watch tools.

18. **`tabi-shokunin`** (`tabi-shokunin/PROVINCE.md:1-215`, 92 knowledge files):
    - **C1 Surface**: **ADJACENT (Explicit Recognition of mado; HTTP Cookie Path)**. PROVINCE line 199 explicitly records:
      > `| mado | none | 24ba2a9d... | PROVINCE.md:3 | desktop & compositor craft — the Hyprland/waybar/walker | tabi runs headless throwaway-profile browsers, never the desktop or compositor; no shared surface.`
      Hits in `external-class-fixture-v2.md:126` and `stateful-fixture-evidence.md:60, 260-288, 487` are JS variables or `Set-Cookie: ...; Path=/; HttpOnly`.
    - **C2 Surface**: **SILENT**. Browser automation; 0 harm watch claims.

19. **`tameshi-shokunin`** (`tameshi-shokunin/PROVINCE.md:1-199`, 73 knowledge files):
    - **C1 Surface**: **ADJACENT (Mutation Testing of Sibling Gates)**. PROVINCE lines 32-35, 63-69 cite mado's historical `tools/mado-verify.sh` as an external target for gate mutation testing; 0 desktop entry models.
    - **C2 Surface**: **ADJACENT (Falsification Craft)**. Tameshi crafts mutation tests and benchmark fixtures (`mutate-and-run.sh`); it does not own `quality/harm-watch.py` or the mado replay panel.

20. **`tsukuroi-shokunin`** (`tsukuroi-shokunin/PROVINCE.md:1-573`, 106 knowledge files):
    - **C1 Surface**: **ADJACENT (Explicit Deferral to mado & Systemd Units)**. PROVINCE lines 48 (ADJ-03) and 124 (OUT-004) explicitly declare:
      > `| ADJ-03 | Desktop rendering, bindings, menu or idle behavior needs configuration-level diagnosis | ... (mado) | Mado owns the Hyprland, waybar, walker and terminal configuration plane, themes/wallpapers and screen/idle behavior.`
      Hits in `corpus/knowledge/systemd-unit-fragment-plane-r74.md:60` and `systemd-unit-load-plane-r73.md:42-46` cite systemd unit properties `FragmentPath=` and `DropInPaths=`.
    - **C2 Surface**: **SILENT**. System package/service maintenance; 0 harm watch claims.

---

## 2. Cross-Source Pattern: Joining the Complete Desktop Invocation Plane

### 2.1 The Cumulative Desktop Execution Architecture

Across rounds 17, 47, 91, 92, 94, 97, 98, and now 99, `mado-shokunin` has methodically built the entire desktop MIME resolution and execution stack:

```
[1. Filesystem Path / URI]
         │
         ▼  (Round 97: tools/mado-filetype.py; glocalfileinfo.c / xdgmime)
[2. MIME Content Type] (e.g. text/plain)
         │
         ▼  (Round 91: tools/mado-mime.py & Round 92: tools/mado-xdgmime.py; mimeapps.list)
[3. Resolved .desktop Application Entry] (e.g. editor.desktop)
         │
         ▼  (Round 98: tools/mado-execargv.py; gdesktopappinfo.c expand_application_parameters)
[4. Expanded Argv Vector] (Exec macro expansion: %f, %u, quotes, escapes)
         │
         ▼  (Round 99: tools/mado-launchenv.py; gdesktopappinfo.c launch environment)
[5. Launch Spawn Environment]:
    ├── Load Gate Validation: g_find_program_for_path(argv[0], NULL, Path=) & TryExec check
    ├── Terminal Delegation:
    │   └── If Terminal=true: walks known_terminals table in GLib
    │       └── 1st entry: xdg-terminal-exec (exec_arg=NULL)
    │           └── (Round 47: tools/mado-terminal.py; xdg-terminals.list)
    │               └── Resolves host terminal emulator (Alacritty.desktop) + adds -e
    ├── Post-Prepend Resolution: g_find_program_for_path(argv[0], PATH, Path=)
    ├── Working Directory: Path= (defaults to launcher cwd)
    └── Child Environment: GIO_LAUNCHED_DESKTOP_FILE=<desktop_path>
```

### 2.2 What the Join Makes Answerable

Before Round 99, the lane held isolated fragments:
- **Round 47** (`tools/mado-terminal.py`, `xdg-terminal-selection-r47.md`) solved how `xdg-terminal-exec` reads `xdg-terminals.list` to pick `Alacritty.desktop` over `foot`/`kitty`/`ghostty`, but could not answer *when* or *how* GLib/GIO delegates to `xdg-terminal-exec`.
- **Round 98** (`tools/mado-execargv.py`, `gio-exec-argv-r98.md`) solved how `Exec=` field codes (`%f`, `%u`, etc.) expand into argv vectors, but could not answer what surrounds that vector: whether `Terminal=true` alters argv, which working directory applies, whether the program can load, or what environment variables are passed.

With **Round 99** (`tools/mado-launchenv.py`, `gio-launch-env-r99.md`):
The join connects GIO's `known_terminals` table (`gdesktopappinfo.c:2765-2778`) directly to `xdg-terminal-exec 0.14.3` (`terminal-route-r17.md`, `xdg-terminal-selection-r47.md`):
1. When a `.desktop` file declares `Terminal=true`, GIO evaluates `known_terminals[0]` = `"xdg-terminal-exec"` via `g_find_program_for_path(name, PATH, Path=)`.
2. Because `/usr/bin/xdg-terminal-exec` is installed on this host, GIO prepends `xdg-terminal-exec` with `exec_arg = NULL` (vector: `["/usr/bin/xdg-terminal-exec", <argv...>]`).
3. The joined pipeline can now statically answer:
   > *"Given a `.desktop` file with `Terminal=true`, `Path=/data`, and an argument `file.txt`, what exact command string, working directory, and terminal wrapper will execute on this host?"*
   - GLib produces: `argv=["/usr/bin/xdg-terminal-exec", "my-tool", "file.txt"]`, `cwd="/data"`, `GIO_LAUNCHED_DESKTOP_FILE=".../app.desktop"`.
   - `xdg-terminal-exec` (from round 47) resolves `~/.config/xdg-terminals.list` to `Alacritty.desktop`, reads its `-e` execution argument, and produces the final process spawn:
     `["/usr/bin/alacritty", "-e", "my-tool", "file.txt"]` running in directory `/data`.

---

## 3. Frontier / Adjacency Verdict

```
CONTESTED_SCOPE: NONE
C1_SURFACE: UNCONTESTED across all 20 sibling lanes. (game-dev-3d, tabi, and tsukuroi explicitly assign desktop & compositor craft to mado).
C2_SURFACE: UNCONTESTED across all 20 sibling lanes. (No sibling owns a harm-watch replay panel or leg census tool).
```

---

## 4. Non-Obvious Move (UFO-FSD Compatible Synthesis Across Proposals)

### 4.1 Evidence Across Wave Proposals

1. **C1 Proposal Findings (`R99MScoutEnv`, `R99MExecTool`, `R99MReviewC1`)**:
   - `gutils.c:322-327` & `344-353`: `g_find_program_for_path(program, path, working_dir)` treats `working_dir` (`Path=`) with a subtle asymmetry:
     - If `program` contains a slash (`strchr(original_program, '/') != NULL`, e.g. `./run.sh` or `bin/tool`), it tests only `working_dir/program` (or `cwd/program` if working_dir is empty). If not executable or missing, it **fails immediately** (returns NULL, never searches PATH).
     - If `program` has **no slash** (e.g. `Exec=mytool`), it tests `working_dir/mytool`. If missing, it **falls back to searching PATH**.
   - `gutils.c:486-497`: If a relative hit is found (either via relative `Path=` or relative PATH component `.`), GLib joins it with `g_get_current_dir()`, returning a **strictly absolute path**.
   - Load Gate vs Spawn Failure:
     - If `Path=` names a nonexistent directory: an `Exec` with a slash fails the load gate immediately (`load` error, exit 1). An `Exec` with a bare binary name found on system PATH passes the load gate, but fails at spawn time in `g_spawn_async_with_fds` when attempting `chdir` (`cwd-failed` error, exit 1).
   - In `gdesktopappinfo.c:2766`, `xdg-terminal-exec` is the only row in `known_terminals` with `exec_arg = NULL` (`term_argc = 1`); all other eleven terminals have non-NULL `exec_arg` (`-e`, `--`, `-x`), requiring `term_argc = 2`.

2. **C2 Proposal Findings (`R99MExecHarm`, `R99MCriticC2`, `R99MReviewRecords`)**:
   - The round-98 outside spot-check (defect 5) flagged that `harm-final-r98.txt` dropped `r97c1_filetype` and `r97c2_counter_selftest`.
   - `R99MCriticC2` and `R99MExecHarm` confirmed that replaying historical legs at the current tip requires rigorous distinction between legs that are expected to pass (`expect_rc 0`, `expect_marker "TARGET_MET"`) versus legs that hit documented setup limits at new revisions (e.g. `r90c1_portal_routing` expecting `SETUP_ERROR`, `expect_rc 2`).
   - If `quality/harm-watch.py` executes legs with a shared scratch root or ambient environment, runs interleave or collide on scratch fixtures (the M98-12 failure class). Furthermore, if a leg invokes an instrument that touches PATH without isolation, a `Terminal=true` probe could trigger a host terminal window!

### 4.2 Affected Axes

- **`coverage` (C1)**: Ensures `tools/mado-launchenv.py` models GLib's exact relative-hit canonicalization (R6), bare-vs-slash path discrimination, and the distinct `load` versus `cwd-failed` refusal boundaries.
- **`operability` (C2)**: Ensures `quality/harm-watch.py` executes all 28 historical legs (including recovered round-97 legs) with strict isolation, idempotent scratch allocation, and hermetic environment controls, preventing host application triggers and cross-leg fixture collisions.
- **Harms no axis**: Strictly additive; satisfies QUALITY 159, 162, 170 without mutating historical rows or relaxing predicate thresholds.

### 4.3 Proposed Move: The Dual-Substrate Execution Environment Invariant

Synthesize C1's static environment model and C2's dynamic execution runner into a single architectural contract:

1. **C1 Candidate Discipline (`tools/mado-launchenv.py`)**:
   Implement `find_program(program, path, working_dir, launcher_cwd=None)` with exact GLib 2.90.1 fidelity:
   ```python
   def find_program(program, path=None, working_dir=None, launcher_cwd=None):
       cwd = launcher_cwd or os.getcwd()
       has_slash = "/" in program
       
       # 1. Check working_dir if provided and program is relative
       if working_dir and not os.path.isabs(program):
           candidate = os.path.join(working_dir, program)
           if is_executable_file(candidate):
               return candidate if os.path.isabs(candidate) else os.path.abspath(os.path.join(cwd, candidate))
           if has_slash:
               return None  # Slash in program forbids PATH fallback

       # 2. If program is absolute or had slash, check directly
       if os.path.isabs(program) or has_slash:
           candidate = program if os.path.isabs(program) else os.path.join(working_dir or cwd, program)
           if is_executable_file(candidate):
               return candidate if os.path.isabs(candidate) else os.path.abspath(os.path.join(cwd, candidate))
           return None

       # 3. Walk PATH (default /bin:/usr/bin:. if unset)
       search_path = (path if path is not None else os.environ.get("PATH")) or "/bin:/usr/bin:."
       for entry in search_path.split(":"):
           dir_part = entry if entry else "."
           if working_dir and not os.path.isabs(dir_part):
               dir_part = os.path.join(working_dir, dir_part)
           cand = os.path.join(dir_part, program)
           if is_executable_file(cand):
               return cand if os.path.isabs(cand) else os.path.abspath(os.path.join(cwd, cand))
       return None
   ```
   For terminal selection, match the first hit in `known_terminals`. If `xdg-terminal-exec`, `exec_arg` is `None` (prepend 1 argument: `[found_path]`). For all other 11 terminals, prepend 2 arguments: `[found_path, exec_arg]`.

2. **C2 Dynamic Runner Hermeticity (`quality/harm-watch.py`)**:
   In `harm-watch.py`, when executing each panel leg:
   - Allocate an isolated scratch subdirectory per leg: `leg_scratch = os.path.join(scratch_root, leg["id"])` with `os.makedirs(leg_scratch, exist_ok=True)`.
   - Pass `--scratch-root {leg_scratch}` in the leg's argv so no two legs share scratch space.
   - For all historical legs, enforce `expect_rc` and `expect_marker` checking. Include all 28 legs across rounds 90–98 (restoring `r97c1_filetype` and `r97c2_counter_selftest` with their measured tip status), closing Defect 5 permanently.

### 4.4 Risks and Verification

- **Risks**:
  - `os.path.abspath` in Python uses `os.getcwd()` by default. To prevent test environment sensitivity when `mado-launchenv.py` is invoked from different directory roots, the resolver must accept an optional `launcher_cwd` or default to the directory of the desktop file when executing case fixtures.
  - Ensuring that no leg in the harm-watch panel leaks environment variables or temporary files into the git repository.
- **Verification**:
  - **C1**: Run `python3 -I tools/mado-launchenv.py --selftest`. Asserts all 6 rules (load gate, terminal prepend, post-prepend lookup, cwd, GIO_LAUNCHED_DESKTOP_FILE, and relative-path canonicalization) pass with `checks >= 20 failed = 0`.
  - **C2**: Run `python3 -I quality/harm-watch.py --repo . --rev 2cbaa141f42df9dfeee4d207cae6558a4dd59863 --panel .ufo/waves/round-99/controls/harm-panel-r99.json`. Asserts `HARM_WATCH: legs=28 ok=28 mismatch=0` (rc 0), verifying that all 28 historical legs pass with zero mismatches and clean census verification.
