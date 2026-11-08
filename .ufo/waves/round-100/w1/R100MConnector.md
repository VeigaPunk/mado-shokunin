# R100MConnector — UFO-FSD Connector Report (Round mado 100, Wave w1)

**Seat**: `R100MConnector`  
**Role**: UFO-FSD connector / leaf member  
**Report target**: `.ufo/waves/round-100/w1/R100MConnector.md`  
**Receipt target**: `.ufo/waves/round-100/assimilation/connector-sweep-r100.txt`  
**Lane root**: `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Base revision**: `43309e6af9a3b57f1bc839a826bef1f8eb7495e4` (`master`)  

**Declared axes**:
1. **C1 `coverage`** (capability: the PATH-unset default search path of the launch load gate):
   At base `43309e6a`, GLib's `g_find_program_for_path` (`gutils.c:370-389`) unset-PATH default search path (`/bin:/usr/bin:.`) is modeled in `tools/mado-launchenv.py` (`DEFAULT_SEARCH_PATH = '/bin:/usr/bin:.'`) but exercised by zero frozen cases (both round-99 `path-unset` cases carried an absolute `Exec`). C1 freezes a `path-default` class of ≥6 cases separating unset from empty, unset from ambient, and testing the trailing `.` in working directories, verified against the pinned `/usr/bin/gio` oracle (`PRED-C1-r100-v1`).
2. **C2 `operability`** (instrument: the harm watch's per-leg cap becomes measured and the panel goes green):
   At base `43309e6a`, the frozen 28-leg harm panel (`harm-panel-r99.json`) carried `timeout_s: 600` with no per-leg timing and no headroom, timing out on two loaded legs. C2 adds monotonic `elapsed_ms` to `quality/harm-watch.py` per leg and human line, measures all 28 legs on this host, re-freezes `harm-panel-r100.json` at twice the largest measured elapsed duration, and reports 28 legs run with zero mismatches (`PRED-C2-r100-v1`).

---

## 1. Fleet-Wide Sibling-Overlap Scan (Read-Only)

An exhaustive, read-only sweep was conducted across all 20 sibling lanes in `/home/vgpnk/Projects/shokunin/*-shokunin/` for the four declared cross-surface patterns:
1. `DEFAULT_SEARCH_PATH`
2. `/bin:/usr/bin`
3. `elapsed_ms`
4. `timeout_s`

### 1.1 Summary Table Across Fleet Lanes

| Lane | PROVINCE lines | knowledge files | `DEFAULT_SEARCH_PATH` | `/bin:/usr/bin` | `elapsed_ms` | `timeout_s` | Duplicate Surface? |
|---|---|---|---|---|---|---|---|
| `audio-shokunin` | 53 | 18 | 0 | 0 | 0 | 0 | None (silent) |
| `chousa-shokunin` | 17 | 98 | 0 | 0 | 0 | 1 | None (`tools/parent-lifetime.sh:21` script timeout) |
| `game-dev-2d-shokunin` | 38 | 5 | 0 | 0 | 0 | 0 | None (silent) |
| `game-dev-3d-shokunin` | 82 | 6 | 0 | 0 | 0 | 0 | None (explicitly defers desktop/compositor craft to mado: `PROVINCE.md:75`) |
| `kagi-shokunin` | 114 | 44 | 0 | 0 | 0 | 0 | None (silent) |
| `kaidoku-shokunin` | 779 | 185 | 0 | 6 | 0 | 0 | None (subprocess runner PATH sanitizer in unpack/decompilation tools) |
| `kake-shokunin` | 747 | 92 | 0 | 0 | 0 | 0 | None (silent) |
| `kama-shokunin` | 456 | 63 | 0 | 0 | 0 | 1 | None (`tools/round61-c1-counter.py:123` benchmark timeout) |
| `kasegi-shokunin` | 237 | 107 | 0 | 0 | 0 | 0 | None (silent) |
| `kengaku-shokunin` | 1136 | 81 | 0 | 0 | 0 | 0 | None (eval benchmarks, models no desktop launch grammar) |
| `kotoba-shokunin` | 78 | 75 | 0 | 0 | 0 | 0 | None (explicitly recognizes mado ground: `PROVINCE.md:72`) |
| `kotodama-shokunin` | 31 | 6 | 0 | 0 | 0 | 1 | None (`tools/harness/claims-freshness.py:45` claims check timeout) |
| `kumitate-shokunin` | 75 | 92 | 0 | 0 | 0 | 0 | None (silent) |
| `lore-shokunin` | 35 | 26 | 0 | 0 | 0 | 0 | None (silent) |
| `mado-shokunin` (OWN) | 629 | 120 | 1 | 8 | 0 | 3 | Sole owner of launchenv & harm-watch surfaces |
| `mori-shokunin` | 700 | 102 | 0 | 1 | 0 | 7 | None (git/jj runner PATH sanitizer & watchdog timeouts) |
| `revenger-shokunin` | 59 | 28 | 0 | 0 | 0 | 0 | None (silent) |
| `souji-shokunin` | 323 | 54 | 0 | 4 | 0 | 1 | None (census hygiene subprocess PATH & cleanup timeout) |
| `tabi-shokunin` | 243 | 96 | 0 | 0 | 0 | 0 | None (explicitly defers desktop/compositor craft to mado: `PROVINCE.md:199`) |
| `tameshi-shokunin` | 199 | 73 | 0 | 0 | 0 | 4 | None (mutation benchmark registry tool timeout arguments) |
| `tsukuroi-shokunin` | 573 | 145 | 0 | 0 | 0 | 0 | None (explicitly defers desktop/compositor craft to mado: `PROVINCE.md:48, 124`) |

### 1.2 Inspection of Pattern Hits

1. **`DEFAULT_SEARCH_PATH`**:
   - `mado-shokunin`: `tools/mado-launchenv.py:121` (`DEFAULT_SEARCH_PATH = '/bin:/usr/bin:.'`).
   - All 20 other fleet lanes: **0 matches**. No sibling lane holds or models the GLib unset-PATH default search path.
2. **`/bin:/usr/bin`**:
   - `kaidoku-shokunin` (6 files: `tools/round-{42,44,49,50,67}/c1-run.sh`, `tools/round-86/gate-registry.py:99, 163`): Sets `env = {"PATH": "/usr/local/bin:/usr/bin:/bin"}` as standard subprocess execution hygiene for unpacking and analyzing binaries.
   - `mori-shokunin` (1 file: `tools/mori-round17-jj-regressions.py:207`): Uses `env.setdefault("PATH", "/usr/local/bin:/usr/bin:/bin")` for subprocess test runner execution.
   - `souji-shokunin` (4 files: `souji-citation-reconcile.py`, `souji-fleet-root-census.py:42`, `souji-freeze-check.py`, `souji-worktree-drift.py`): Sets `'PATH': '/usr/local/bin:/usr/bin:/bin'` when calling `git` or Python subcommands.
   - `mado-shokunin` (8 files): `tools/mado-launchenv.py` (models the literal `/bin:/usr/bin:.` default from `gutils.c`), `tools/mado-mime.py`, `tools/mado-xdgmime.py`, and 5 historical quality counter scripts.
   - No sibling lane models the desktop application search path or execution environment.
3. **`elapsed_ms`**:
   - Fleet-wide: **0 matches** across all 21 lanes under `tools/` and `quality/`.
   - Introduced this round in `mado-shokunin/quality/harm-watch.py` as an integer monotonic duration per leg and in `--json`.
4. **`timeout_s`**:
   - Present in 7 lanes: `chousa-shokunin` (`parent-lifetime.sh`), `kama-shokunin` (`round61-c1-counter.py`), `kotodama-shokunin` (`claims-freshness.py`), `mado-shokunin` (`quality/harm-watch.py`, `c2-r99-harm-watch.py`, `tools/mado-hostguard.py`), `mori-shokunin` (7 watchdog/census scripts), `souji-shokunin` (`souji-census.sh`), and `tameshi-shokunin` (4 registry scripts).
   - In sibling lanes, `timeout_s` is a generic CLI parameter or config option for process watchdog timeouts. Only `mado-shokunin` holds `quality/harm-watch.py` and its cross-round replay panel.

### 1.3 Adjacency & Frontier Verdict

```
CONTESTED_SURFACE: NONE
C1_SURFACE (launchenv PATH-default): UNCONTESTED across all 20 sibling lanes.
C2_SURFACE (harm-watch replay panel): UNCONTESTED across all 20 sibling lanes.
```
Mado L1 holds sole and uncontested ownership of both C1 and C2 surfaces.

---

## 2. Scan of Shokuknow Merge Package (`shokuknow/merge/mado/`)

The merge package `/home/vgpnk/Projects/shokuknow/merge/mado/` was scanned read-only for this round's themes: launch, PATH, spawn, exec, harm watch, and per-leg timing.

### 2.1 Grep Command and Output

```bash
cd /home/vgpnk/Projects/shokuknow/merge/mado && grep -niE 'launch|/bin:/usr/bin|PATH default|elapsed|per-leg|spawn' MERGE-REPORT.md SOURCES.append.md
```

Observed output (9 matches across 2 files):
```
MERGE-REPORT.md:105:| `S205` | S188 | A dispatcher returns a table that describes an action and does not invoke it; `force_idle` sets elapsed time for all idle timers ignoring idle inhibitors; `event(string)` sends an event to socket2 |
SOURCES.append.md:9:| S205 | Hyprland wiki — Dispatchers (Lua config API) — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/configuring/core/dispatchers.md | docs | A | Documented dispatcher semantics of the Hyprland Lua config API: what a dispatcher is, how it must be executed, and the idle, DPMS and event-socket dispatchers | `content/configuring/core/dispatchers.md:9-19` (dispatchers are descriptions; `hl.dispatch`), `:58-59` (`dpms`, `event`), `:69` (`force_idle`), `:82-87` (keybind warnings) @ commit `c04680a28301ab4b5ee5f94eaff5395efe28dbac`, 12879 B, sha256 prefix `c830ce0717f92776` | A dispatcher returns a table that describes an action and does not invoke it; `force_idle` sets elapsed time for all idle timers ignoring idle inhibitors; `event(string)` sends an event to socket2 | mined | 2026-10-23 | 180d — re-fetch and confirm the section headings are intact (ran 2026-10-23) | corpus/knowledge/hyprland-dispatchers-r6.md |
SOURCES.append.md:15:| S211 | Hyprland Waybar 設定：ステータスバーのモジュール化とテーマ (liz's doc) — https://doc.liz6.com/ja/tools/hyprland/04-waybar-theming | community | C | Japanese-language personal walkthrough of a module-based Waybar setup for Hyprland, from config layout to launch and service handling | § Waybar 設定とテーマ, § モジュール JSONC 構成 (`modules-left`, `waybar -c`), § systemctl --user による起動 @ page `04-waybar-theming`, 50169 B | A Japanese practitioner splits the bar configuration into per-module JSONC files under a config directory and drives the bar with `waybar -c config.jsonc -s style.css`, with `systemctl --user` for lifecycle | mined | 2026-10-23 | 180d — re-fetch and confirm the sections are still live (ran 2026-10-23) | corpus/knowledge/waybar-modular-theming-r6.md |
SOURCES.append.md:48:| S244 | Privileged Wayland Clients — blog.ce9e.org — https://blog.ce9e.org/posts/2025-10-03-wayland-security/ | community | C | The framing that places the lane's focus-control surfaces in the wider privileged-client model: what a compositor grants a privileged client, and why the sandboxing story is unfinished | § "Privileged Wayland Clients" (2025-10-03), § `WAYLAND_SOCKET` handoff, § security-context § @ page, 3135 B | Privileged interfaces are granted at bind time to clients the compositor spawns, and the `WAYLAND_SOCKET` descriptor handoff is the mechanism that makes the grant non-stealable — the context in which a focus-grab protocol matters | mined | 2026-10-23 | 180d — re-fetch the post and confirm the sections are intact (ran 2026-10-23) | corpus/knowledge/privileged-wayland-clients-r7.md |
SOURCES.append.md:61:| S257 | omarchy app restart helper (v3.8.4) — https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-restart-app | code | A | How the desktop restarts a managed application — and therefore what manages the idle daemon's lifetime, given that no hypridle unit is active on this host | `§ whole file` (`:3-7`) @ tag `v3.8.4`, 205 B, sha256 prefix `85b62c5b79b9295c` | A restart is **kill then relaunch under uwsm** — not a systemd unit operation — so an app's lifetime is owned by the session manager, which is why no `hypridle` unit appears in the host's unit list even though the unit file is installed | mined | 2026-10-23 | on-release — re-pull at the host's omarchy tag and compare sha256 (ran 2026-10-23) | corpus/knowledge/managed-app-restart-r7.md |
SOURCES.append.md:66:| S262 | uwsm upstream — the `app-graphical.slice` contract and what stops apps (README at tag v0.27.1) — https://raw.githubusercontent.com/Vladimir-csp/uwsm/v0.27.1/README.md | docs | A | uwsm's own statement of where apps live and how they are stopped, at the tag this host's package carries | README lines naming `app-graphical.slice` as the default destination, and the line stating that the slice receives stop action before the compositor is stopped | The answer to "what stops an app": apps launched as scopes land in `app-graphical.slice`, and that slice receives stop action *before* the compositor is stopped — so the app is torn down ahead of the compositor, not with it; `uwsm app` is documented as "for launching applications in graphical session" | mined | 2026-10-23 | on-release — re-pull at host tag v0.27.1 and compare sha256 (ran 2026-10-23) | corpus/knowledge/uwsm-app-slice-contract-r7.md |
SOURCES.append.md:67:| S263 | uwsm upstream — the app-daemon unit template at tag v0.27.1 — https://raw.githubusercontent.com/Vladimir-csp/uwsm/v0.27.1/systemd/user/wayland-wm-app-daemon.service.in | code | A | The unit template that generates each launched app's unit, at the tag this host's package carries | The `ExecStart=` line of the template, and its `Slice=` line | The unit that launches an app is not a per-app template file at all: uwsm runs one long-lived daemon (`wayland-wm-app-daemon.service`) whose `ExecStart` is `aux app-daemon`, and that daemon synthesises a scope per app at launch time; the daemon itself lives in `session.slice`, and it is ordered `Before=wayland-session-shutdown.target` and `Conflicts=wayland-session-shutdown.target` | mined | 2026-10-23 | on-release — re-pull at host tag v0.27.1 and compare sha256 (ran 2026-10-23) | corpus/knowledge/uwsm-app-daemon-template-r7.md |
SOURCES.append.md:71:| S267 | omarchy v3.8.4 — the stock idle configuration the desktop ships, which is byte-identical to this host's `~/.config/hypr/hypridle.conf` — https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/config/hypr/hypridle.conf | docs | A | The idle ladder itself — the two timeouts and what each fires — as the desktop ships it, identical byte-for-byte to the host's own file | The `listener` blocks of the stock file, and the `general` block's `lock_cmd` line | The idle ladder is two steps, not one: at `timeout = 150` the screensaver starts (`pidof hyprlock \|\| omarchy-launch-screensaver`), and at `timeout = 152` the system locks (`on-timeout = omarchy-system-lock`) — the comment in the file explains the 2-second offset because the lock takes two seconds to prepare | mined | 2026-10-23 | on-release — re-pull at the host's omarchy tag and compare sha256 (ran 2026-10-23) | corpus/knowledge/stock-idle-ladder-r7.md |
SOURCES.append.md:72:| S268 | host idle daemon state — the process, the unit that carries it, and the launcher's own command line (measured on this host) — lanes/mado/round7/fetch/host-idle-daemon-state.txt | own-work | A | Whether the idle daemon actually runs on this host right now, and under what unit — the premise the round-6 ledger took from a single `pgrep` that no longer holds | The `pgrep`, `ps`, `systemctl --user is-enabled/is-active` and `uwsm_app-daemon` journal lines in the file | The idle daemon *is* running: PID 1667, started by the compositor itself at session start, and carried by the transient scope `app-Hyprland-hypridle-d4bd7533.scope` — not by `hypridle.service`, which is `disabled`/`inactive`; the uwsm app-daemon's own journal log confirms it was launched by `uwsm app-daemon` at 2026-10-23 04:36:10 | mined | 2026-10-23 | 30d — re-measure on host at next session restart | corpus/knowledge/host-idle-daemon-state-r7.md |
```

### 2.2 Analysis and Assimilation Finding

- Zero hits for `/bin:/usr/bin`, `PATH default`, or `per-leg`.
- Every hit is historical material from rounds 6 and 7 (staged October 23, 2026):
  - `S205`: Hyprland Lua configuration API (`force_idle` dispatcher setting idle timer durations).
  - `S211`: Waybar modular status bar theming and user service launch.
  - `S244`: Privileged Wayland client security context descriptor handoff.
  - `S257`, `S262`, `S263`: `uwsm` systemd application scope launching and app-daemon lifecycle.
  - `S267`, `S268`: `hypridle` timeout ladder configuration and transient scope launcher.
- None of the staged sources in `shokuknow/merge/mado/` touch GLib's desktop application execution environment (`gutils.c:370-389`, `g_find_program_for_path`, `DEFAULT_SEARCH_PATH = "/bin:/usr/bin:."`, `TryExec`/`Exec`, `Path=`, `GIO_LAUNCHED_DESKTOP_FILE`) or the multi-round harm watch replay panel (`quality/harm-watch.py`, per-leg elapsed timing).

**Assimilation Verdict**: `Assimilation: none` on this round's ground.

---

## 3. Mining `considerthese/2026-11-07.md` Proposal 3 into `QUALITY.md` Criterion 173

### 3.1 Unimplemented Proposal and Grounding Pointer

From `/home/vgpnk/Projects/shokunin/mado-shokunin/considerthese/2026-11-07.md` §Self-improvement suggestions, item 3:
> *"3. **Distrust selftests written by the same author as the code.** M95-1 shows a selftest can certify the author's misreading. Suggest a standing rule: library-semantics ports carry at least one exhaustive small-domain sweep (e.g. all 256 bytes against the shipped library) as a check, since that is what caught the VT bug."*

### 3.2 Verification that the Pointer Resolves

The proposal points directly to `corpus/lessons/round-95.md#mistakes` `M95-1`:
- **File**: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-95.md`
- **Section**: lines 11–25:
  `M95-1 — the L1 wrote GLib's looks_like_text from C's isspace, and its own selftest encoded the error.`
- **Class**: Library-semantics substitution (`g_ascii_isspace` table lookup space bit excludes VT `0x0b` where C `isspace` includes it; L1 wrote selftest check `s10 VT passes looks_like_text` expecting `text/plain 0`, so `--selftest 23/23` certified the bug).
- **Evidence**: Five independent wave seats (`R95MCritic` C1-F1, `R95MReviewC1` F1, `R95MProbeC1` F1, `R95MMutC1` F1, `R95MExecCasesC1` finding 1, `R95MScribeEntry` §F1). A 7240-input host probe failed to detect the defect because sampled files carried no isolated `0x0b` bytes; an exhaustive 256-byte sweep against the compiled oracle pinpointed the exact singleton difference.
- **Predecessor**: `QUALITY.md` 163 established byte-by-byte checking for ported predicates, but did not establish a generic criterion barring author-written selftests from serving as the sole certification for library-semantics ports across small domains.
- **Verification verdict**: The pointer resolves completely to real committed lesson bytes and recorded receipts.

### 3.3 Draft Criterion Text (Drafted for `corpus/QUALITY.md`, Number 173)

*(Draft only; not edited into `corpus/`)*

```markdown
**173. A library-semantics re-implementation carries an exhaustive small-domain sweep against the shipped library, independent of author-written selftests.** A selftest written by the same author as the candidate can encode the author's misreading and certify bugs as intended behaviour; a host-file sampling probe may never hit the unexercised edge. The rule: when a tool re-implements a library function whose domain admits an exhaustive enumeration (e.g. all 256 byte values for single-byte parsers/classifiers, all single-character escape codes, or an enumerated small finite domain), the round's frozen controls must include an exhaustive sweep generated directly from the installed library/oracle, and the candidate must agree on every value of the sweep; an author-written selftest alone cannot certify domain correctness. Shown able to fail: in round 95, the L1 wrote GLib's looks_like_text using C isspace (treating VT 0x0b as whitespace), and wrote selftest check s10 expecting text/plain, so --selftest 23/23 certified the bug while the 7240-input host probe found no VT; R95MCritic's 256-byte sweep against the compiled oracle caught the singleton difference at 0x0b (lesson: lessons/round-95.md#mistakes M95-1; considerthese/2026-11-07.md proposal 3).
```

### 3.4 Gating Rule for Future Rounds

A future round counter verifying a library-semantics port (e.g. `quality/counters/c1-rN-*.py`) can gate on the following invariant:
```
domain_sweep_correct == domain_sweep_total AND domain_sweep_total >= domain_size
```
Where:
- `domain_size` is the theoretical cardinality of the small domain (e.g. 256 for byte-level primitives).
- `domain_sweep` test vectors are produced by the frozen oracle harness without author-specified expected outputs.
- A mutant that alters any single branch of the domain definition (e.g. flipping `isspace` table entries) must be flagged as a kill by the sweep leg.

---

## 4. UFO-FSD Non-Obvious Move: The Tripartite Substrate Environment Isolation Invariant

### 4.1 Evidence Across Ground & Wave Artifacts

1. **Candidate CLI and Model Invariant (`tools/mado-launchenv.py:126, 297-298, 466`)**:
   ```python
   PROCESS_PATH = object()
   if path_env is PROCESS_PATH:
       path_env = os.environ.get('PATH')
   ```
   When `--path` is omitted from CLI arguments, `mado-launchenv.py` reads `os.environ.get('PATH')`.
   - If `PATH` is absent from `os.environ`: `path_env` is `None`. In `find_program()` (line 206), `if path is None: path = DEFAULT_SEARCH_PATH` (`/bin:/usr/bin:.`).
   - If `PATH` is present in `os.environ` as `""` (empty string): `path_env` is `""`. In `find_program()` (lines 206–215), `path` is `""`, triggering the single empty entry (search cwd only).
2. **The Counter Substrate Defect (`quality/counters/c1-r99-launchenv.py:307` & `R100MExecCounterC1`)**:
   In round 99, `run_tool()` was defined as:
   ```python
   argv = [sys.executable, "-I", tool_path] + list(tool_args) + ["--json"]
   env = {"PATH": "", "LC_ALL": "C", "HOME": home}
   subprocess.run(argv, env=env, ...)
   ```
   In round 99, this passed because both `path: null` cases carried an absolute `Exec` (`/bin/true`), which returns at line 200 before `PATH` is ever inspected!
   In round 100, cases with `path: null` carry bare executable names (e.g. `probe`, `/usr/bin/true`) explicitly designed to test the default search path `/bin:/usr/bin:.`.
   **The Contradiction**: If the counter's `run_tool()` executes with `env = {"PATH": "", ...}`, then `os.environ.get('PATH')` inside `mado-launchenv.py` returns `""` (empty string), NOT `None`!
   As a consequence:
   - `mado-launchenv.py` treats the case as `PATH=""` (empty), searching only cwd!
   - Any program in `/bin` or `/usr/bin` is reported as `error=load` or `program-not-found`, while the oracle (which launched with `env -i` and no `PATH`) found it via `/bin:/usr/bin:.`.
   - Even on a fixture at the root, the returned `argv[0]` under `PATH=""` is `{root}/probe`, whereas under `PATH` unset it is `{root}/./probe` (derived from the `.` entry of `/bin:/usr/bin:.`, confirmed by `R100MLabratUnset.md` lines 41–42)!
   - Result: A false mismatch occurs on every single `path-default` case!
3. **The Control Separation Invariant (`PRED-C1-r100-v1`)**:
   `claims-declaration-r100.md` line 46 explicitly requires:
   ```
   control_unset_as_empty_correct < cases_total   (the misreading the branch guards against)
   ```
   If the counter runner itself passes `PATH: ""` for unset cases, the test runner forces the candidate to execute the very misreading the control is designed to separate!
4. **Second-Order Cross-Axis Harm Watch Interaction (C2)**:
   In `quality/harm-watch.py`, historical and current legs run under child process environments. If any leg leaks the ambient host `PATH` or sets an unmanaged `PATH`, `Terminal=true` checks would discover `/usr/bin/xdg-terminal-exec` and spawn an interactive terminal window on the operator's display (violating Host Guard rules and destroying reproducibility). Conversely, hardcoding `PATH: ""` across all legs prevents launchenv tests from distinguishing unset from empty.

### 4.2 Affected Axes

- **`coverage` (C1)**: Ensures `quality/counters/c1-r100-launchenv-path.py` and `tools/mado-launchenv.py` cleanly discriminate all three search modes:
  1. `path: null` (PATH absent): exercises `/bin:/usr/bin:.`, producing `{root}/./probe`.
  2. `path: [""]` (PATH empty): exercises cwd-only search, producing `{root}/probe`.
  3. `path: [...]` (PATH explicit): exercises specified search entries.
  Guarantees that `control_unset_as_empty_correct < cases_total` holds strictly.
- **`operability` (C2)**: Enforces that `quality/harm-watch.py` and all panel leg invocations maintain strict hermetic environment boundaries:
  - Omits `PATH` completely when testing unset semantics.
  - Passes explicit fixture PATHs when testing custom searches.
  - Blocks ambient host `PATH` leakage, preventing interactive terminal launches on `Terminal=true`.
  - Records integer monotonic `elapsed_ms` with zero cross-leg scratch collision.
- **Harms no axis**: Strictly preserves the frozen predicate `PRED-C1-r100-v1` and `PRED-C2-r100-v1` without altering pinned bytes or widening declarations.

### 4.3 Proposed Move: The Substrate Environment Tripartite Construction

Synthesize the candidate CLI, the oracle launcher, and the counter runner into a uniform tripartite environment contract:

1. **In `quality/counters/c1-r100-launchenv-path.py` (`score_case` and `run_tool`)**:
   Pass `pstr` (the oracle-normalized PATH string, or `None`) to `run_tool()`:
   ```python
   def run_tool(tool_path: str, tool_args: list[str], cwd: str, home: str,
                pstr: str | None = None,
                timeout: float = TOOL_TIMEOUT) -> tuple[str, str, int]:
       argv = [sys.executable, "-I", tool_path] + list(tool_args) + ["--json"]
       env = {"LC_ALL": "C", "HOME": home}
       if pstr is not None:
           env["PATH"] = pstr
       # When pstr is None (path: null), "PATH" is strictly absent from env!
       try:
           r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout,
                              cwd=cwd, env=env)
       except (OSError, subprocess.TimeoutExpired):
           return "crash", "", -1
       if r.returncode not in (0, 2):
           return "crash", "", r.returncode
       return "ok", r.stdout, r.returncode
   ```
2. **In `score_case()`**:
   ```python
   # When pstr is None, omit --path from CLI:
   if mode == "candidate":
       targs = [darg] + file_args + (["--path", pstr] if pstr is not None else [])
   else:
       targs = [darg] + file_args
   status, out, rc = run_tool(tool_path, targs, root, os.path.join(root, "h"), pstr=pstr)
   ```
   This ensures that when `path: null` is tested:
   - CLI receives no `--path` flag -> `path_env = PROCESS_PATH`.
   - `os.environ.get('PATH')` in `mado-launchenv.py` returns `None` (because `PATH` is absent from `env`).
   - `find_program()` evaluates `path is None` -> selects `DEFAULT_SEARCH_PATH = '/bin:/usr/bin:.'`.
   - The trailing `.` resolves bare root programs to `{root}/./probe`, matching the oracle with 100% fidelity.
   - For `control_unset_as_empty`, the control runner sets `pstr = ""` -> sets `env["PATH"] = ""` -> candidate produces `{root}/probe`, proving that `control_unset_as_empty_correct < cases_total`.

3. **In `quality/harm-watch.py`**:
   Maintain hermetic leg execution:
   - Each leg executes with `cwd = --repo`.
   - Leg scratch is allocated strictly at `<scratch-root>/<leg-id>`.
   - Monotonic `elapsed_ms` is timed via `time.monotonic()` wrapping `subprocess.run()`, emitted on the human `LEG` line and in `--json`.
   - Any leg exercising `mado-launchenv.py` runs with controlled PATH, ensuring no real terminal can spawn.

### 4.4 Risks and Verification

- **Risks**:
  - Python's standard library imports under `python3 -I` without `PATH` in `env`: On Arch Linux (glibc 2.40 / Python 3.13), Python uses `/usr/bin/python3` and binary-relative library paths; absence of `PATH` in `env` does not impede Python execution.
  - Ensuring mutants do not escape when mutating the `DEFAULT_SEARCH_PATH` string: Verified by mutant test suites checking `DEFAULT_SEARCH_PATH = ""` or `DEFAULT_SEARCH_PATH = "/bin"`, which must be killed by the `path-default` cases.
- **Verification Commands**:
  - **C1 Verification**:
    ```bash
    python3 -I quality/counters/c1-r100-launchenv-path.py --repo . --rev worktree \
      --base-rev 43309e6af9a3b57f1bc839a826bef1f8eb7495e4 \
      --cases .ufo/waves/round-100/controls/launchenv-cases-r100.json \
      --expect-cases-sha256 <PIN> \
      --mutants .ufo/waves/round-100/controls/launchenv-mutants-r100.json \
      --expect-mutants-sha256 <PIN> \
      --genseed .ufo/waves/round-100/controls/launchenv-fresh-r100.py \
      --expect-genseed-sha256 <PIN> \
      --expect-tool-sha256 <PIN> --expect-execargv-sha256 <PIN> \
      --expect-gio-sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462 \
      --scratch-root /fast/scratch/hyaku/mado-r100/R100MConnector/c1_verify
    ```
    Asserts `TARGET_MET` for `PRED-C1-r100-v1` (`default_cases >= 6`, `default_classes >= 3`, `cases_correct == cases_total`, `mutants_killed == mutants_counted`, `control_unset_as_empty_correct < cases_total`, exit 0).
  - **C2 Verification**:
    ```bash
    python3 -I quality/harm-watch.py --repo . --rev 43309e6af9a3b57f1bc839a826bef1f8eb7495e4 \
      --panel .ufo/waves/round-100/controls/harm-panel-r100.json \
      --scratch-root /fast/scratch/hyaku/mado-r100/R100MConnector/c2_verify \
      --timeout 7200 --json
    ```
    Asserts `HARM_WATCH: legs=28 ok=28 mismatch=0` (exit 0), with every leg reporting `elapsed_ms=<int>` on stdout and in JSON.

---

## 5. Summary of Deliverables

1. `.ufo/waves/round-100/assimilation/connector-sweep-r100.txt`:
   Committed receipt containing full 20-sibling lane table, detailed path enumeration for all 4 patterns, duplicate surface analysis (none found), and exact grep output on `shokuknow/merge/mado/` confirming `Assimilation: none`.
2. `.ufo/waves/round-100/w1/R100MConnector.md`:
   This report, detailing the sibling sweep, assimilation verdict, proposal 3 mining into draft `QUALITY.md` Criterion 173 and its gating rule, and the non-obvious tripartite environment substrate proposal resolving C1 unset vs empty discrimination and C2 hermetic runner safety.
3. Hygiene:
   Scratch directory `/fast/scratch/hyaku/mado-r100/R100MConnector` deleted prior to yield. Zero uncommitted artifacts left in scratch or repository.
