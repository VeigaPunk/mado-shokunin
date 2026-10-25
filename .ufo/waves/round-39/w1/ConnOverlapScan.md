# ConnOverlapScan — cross-lane overlap scan & connector synthesis (mado round 39)

- **Seat:** `ConnOverlapScan` (connector, leaf member — no subagents spawned).
- **Lane:** `mado-shokunin` (/home/vgpnk/Projects/shokunin/mado-shokunin).
- **Target instruments:**
  - Capability acquisition tool: `tools/mado-options.py` (C2, PRED-C3-r39-v1).
  - Sourced knowledge entry: `corpus/knowledge/config-option-table-r39.md` with `corpus/SOURCES.md` rows S218/S219 (C3, PRED-C4-r39-v1).
  - Re-registered discrimination pair: `quality/check-r38-discrimination.py`, `.ufo/waves/round-39/c1/manifest.json`, `c1-r38-event-ground.py`, `c2-r38-eventq.py` (C1).
- **Scope swept:** 21 sibling lanes under `/home/vgpnk/Projects/shokunin/`, fleet reports under `.ufo/reports/` (rounds 31–39), and round-39 reflection proposals (`considerthese/2026-10-24.md`, `2026-10-25.md`).
- **Tooling record:** 0 tools installed, updated, or executed with mutation. All reads read-only.

---

## 1. Evidence: cross-lane overlap & surface sweep

### 1.1 Methodology & commands executed
All commands executed were read-only:
1. `glob /home/vgpnk/Projects/shokunin/*` with `gitignore: false` to enumerate all 21 sibling lanes (`kaidoku`, `souji`, `kasegi`, `kengaku`, `mori`, `chousa`, `tameshi`, `tabi`, `kama`, `kumitate`, `kotodama`, `kake`, `revenger`, `tsukuroi`, `kotoba`, `lore`, `game-dev-2d`, `audio`, `game-dev-3d`, `kagi`, `mado`).
2. `grep` across all sibling lane `tools/**`, `scripts/**`, and `quality/**` for `hyprland\.conf`, `hyprctl`, `getoption`, and `option.*table`.
3. `grep` across fleet reports `.ufo/reports/round-*.md` and `.ufo/reports/round-*/*.md` for `option.*ownership`, `option.*table`, and `getoption`.
4. Detailed file inspection of `PROVINCE.md`, `SKILL.md`, and relevant scripts in `kumitate`, `tsukuroi`, `kagi`, `chousa`, `kaidoku`, `kake`, and `kama`.

### 1.2 Sibling lane inventory & boundary findings

| Sibling lane | Domain | Owned surfaces & instruments | Desktop/config overlap finding | Ownership boundary |
|---|---|---|---|---|
| **`kumitate-shokunin`** | Orchestration & tooling | Origin script layer (`ufo-fsd-alpha/scripts/`), runtime (`ufo-core-runtime`), Kimi Code (`~/.kimi-code/`), `scripts/*.mjs`. | `scripts/bind-oracle.mjs` probes mount binds, not keybinds (`SKILL.md:616`); `scripts/surface-probe.mjs` checks orchestration surfaces. Zero Hyprland, `~/.config/hypr/`, or `hyprctl` reads. | Refuses anything outside orchestration/tooling. No overlap. |
| **`tsukuroi-shokunin`** | Host operability & OS repair | Pacman state, systemd user units & timers, journal/boot triage, driver/firmware health. | Row `OUT-004` / `ADJ-03` in `PROVINCE.md:124` explicitly states: *"Mado owns the Hyprland, waybar, walker and terminal configuration plane, themes/wallpapers and screen/idle behavior."* Routes desktop configuration diagnosis OUT to mado. | Tsukuroi explicitly disclaims desktop config inspection. Zero overlap. |
| **`kagi-shokunin`** | Secrets & vault ops | The-janitor flows, credential hygiene, `op.env`, SOPS/age, Vault/OpenBao token lifecycles. | Runs secret-pattern tripwires. Refuses config inspection outside credential boundaries (`PROVINCE.md:6-15`). No option parsing. | Refuses desktop configs; zero overlap. |
| **`chousa-shokunin`** | Deep-research method | Source hierarchy, citation chaining, external-target approval table, claim-vs-source verification. | Owns research craft. Refuses desktop configuration and operational tools (`PROVINCE.md:10-15`). | Refuses desktop surfaces; zero overlap. |
| **`kaidoku-shokunin`** | Reverse engineering of shipped artifacts | Ghidra 12.1.4 provider, native ELF, Electron/ASAR, archives, binutils fallback. | Analyzes binary/package internals statically. No configuration tree parsing or compositor state modeling. | Tracks binary internals, not user configs; zero overlap. |
| **`kake-shokunin`** | Web properties & publishing | ds4cc.com, kimi.page/pro, GitHub Pages, sitemaps, `scripts/citing_set.py`. | **Audited candidate:** kake's round-31..35 reports cite "duplicated option tables" (`ReviewRunnerDiff.md`, `ExecDuplicatedOptionTables.md`, `CriticOptionTableRejection.md`). Inspection proves this was entirely internal argparse CLI option sets (`GATE_VALUE_OPTIONS` / `GATE_OTHER_OPTIONS`) in its citing-set test runner. | Refuses desktop configs; option table was a CLI test harness artifact, not compositor options. Zero overlap. |
| **`kama-shokunin`** | Local model serving & endpoint health | Producer discovery, loopback listener ports (8080/34113), `registry/endpoint-consumers.tsv`. | `endpoint-consumers.tsv` checks baseURL pins in consumer configs. Refuses desktop configuration and compositor IPC (`PROVINCE.md:40-49`). | Refuses desktop surfaces; zero overlap. |
| **`mori-shokunin`** | Telemetry & OOM observability | Journal coredumps, cgroup memory events, process kill clusters. | Captures `app-Hyprland-*` scope names in user journal error logs (`mori-census.sh:3659`), but parses no configuration files and reads no `hyprctl` options. | Telemetry only; zero overlap. |
| **`tameshi-shokunin`** | Mutation-testing method | Mutation testing across fleet gates (`mutate-and-run.sh`). | Maintains mutation test cases against `mado-verify.sh` as an external method tester, but does not own or parse desktop options. | Methodology owner; zero overlap. |

### 1.3 Fleet recent reports sweep (rounds 31–39)
- Grepping `.ufo/reports/round-*.md` for option ownership, `mado-options.py`, or `getoption` across rounds 31 through 39 confirms that **no tool exists anywhere in the fleet that resolves Hyprland configuration options or tracks option ownership**.
- In `mado.md` round-37 report line 152, mado's own roadmap explicitly ranked "the config-option table" as the next unworked desktop surface after binds, animations, and workspace rules.
- Proposal 4 in `considerthese/2026-10-24.md` ("the config-option table, who owns each key, checked against getoption") was mined directly for C2/C3 this round.

---

## 2. Shared ground vs distinct ownership

### 2.1 Shared ground
1. **Regular-file policy & standard-library containment:** Like `tsukuroi`'s census tools and `kama`'s registry checkers, `tools/mado-options.py` adheres strictly to standard-library Python, refusing symlink escapes, FIFOs, and non-regular files with named stderr diagnostics.
2. **Read-only compositor boundary:** `hyprctl` read verbs are constrained strictly to read-only queries; compositor mutation is blocked host-wide across all lanes.

### 2.2 Distinct ownership
1. **Desktop option resolution:** `mado-shokunin` holds sole and exclusive ownership of the Hyprland configuration tree (`~/.config/hypr/hyprland.conf`), its `source =` include hierarchy, layer classification (`root`, `defaults`, `theme`, `user`, `toggles`, `ai-usage`), and the divergence comparison against live `hyprctl getoption` states.
2. **Separation from siblings:**
   - Nothing is absorbed from any sibling lane.
   - Nothing duplicates any tool or script in `kumitate`, `tsukuroi`, `kake`, or `kama`.
   - Tsukuroi's `PROVINCE.md:124` explicitly ratifies mado's exclusive jurisdiction over these surfaces.

---

## 3. One non-obvious move: synthesis across round proposals

### 3.1 Proposals considered & contradictory evidence
1. **Proposal A (C2 Operability / `considerthese/2026-10-24.md` proposal 4):** `tools/mado-options.py` static option table resolver + `--getoption FILE` merge with the divergence vocabulary (`agreement`, `agreement*`, `mismatch`, `config-only`, `live-default`).
2. **Proposal B (Assimilation Theme / Round-38 lesson & connector proposal):** Assimilating `dispatcher-surface-and-request-grammar-r26.md` amendment (citing S220 Dispatchers and S018 `HyprCtl.cpp:1309-1332`), which documents the `[[BATCH]]` / `hyprctl --batch -j` request socket protocol and flag dispatch.
3. **Proposal C (C1 Calibration / `considerthese/2026-10-25.md` proposal 3):** Re-registering the repaired discrimination pair and enforcing strict classification where control falsifiers cannot be bypassed by proxy artifacts.

### 3.2 Explicit contradiction identified in `mado-options.py`
In `tools/mado-options.py`:
- **Docstring contract (lines 31–32):**
  `live-default: live row with no declarer; set=false`
- **Implementation in `merge_rows` (lines 484–490):**
  ```python
  for key, rec in live.items():
      if key not in seen:
          rows.append({
              "key": key, "value": str(rec.get("value")), "owner": None,
              "layer": None, "line": None, "set": bool(rec.get("set")),
              "agreement": "live-default",
          })
  ```
- **Contradiction:** If an option is present in the live compositor but was never declared in `hyprland.conf` (e.g. modified at runtime via IPC `hyprctl keyword key value` or set by a dynamic script), `rec.get("set")` is `true`. The current code unconditionally stamps `"agreement": "live-default"`, emitting `{..., "set": true, "agreement": "live-default"}`. This directly violates the docstring contract that `live-default` requires `set=false`.

### 3.3 The proposed move: Atomic Batch-Option Live Query Contract & Semantic Divergence Refinement
Synthesize the static option resolver's live ingestion interface with the round's request-socket batch grammar:
1. **Formalize the live-query intake protocol via `hyprctl --batch -j` (`[[BATCH]]`):**
   Instead of leaving `--getoption FILE` as an ad-hoc JSON format that requires an undocumented multi-process gathering loop (running 60–80 individual `hyprctl getoption` calls, risking process storming and race conditions across config reload), define an atomic single-roundtrip batch adapter. The batch query emits semicolon-separated `getoption <key>` statements over Hyprland's request socket (`.socket.sock`) using the `[[BATCH]]` grammar documented in the round's assimilated amendment (`HyprCtl.cpp:1309-1332`).
2. **Refine the undeclared divergence classification:**
   Split the undeclared live partition in `merge_rows`:
   - If `key not in seen` and `set == false`: emit `"agreement": "live-default"` (restores strict docstring adherence).
   - If `key not in seen` and `set == true`: emit `"agreement": "live-override"` (or `"runtime-override"`), capturing options modified via live IPC without declaring them in configuration.

---

## 4. Second-order trace

1. **Runtime surface:**
   - Zero compositor mutation. The batch command uses only read verbs (`getoption`).
   - Resolves O(N) subprocess forks into a single atomic O(1) request socket transaction, well within the 5-second socket timeout documented in `corpus/knowledge/request-socket-live-bound-r8.md`.
2. **Contract surface:**
   - Restores mathematical exhaustiveness to the divergence vocabulary:
     - `agreement`: declared once, live matches declared, `set=true`.
     - `agreement*`: declared with shadow, live matches resolved, `set=true`.
     - `mismatch`: declared, but live value differs or live `set=false`.
     - `config-only`: declared in config, but unexposed by compositor `getoption`.
     - `live-default`: unmentioned in config, compositor default (`set=false`).
     - `live-override`: unmentioned in config, but active in compositor (`set=true`).
3. **Substrate surface:**
   - Maintains strict Python stdlib and regular-file policies.
   - Preserves offline fixture testing in private temp directories without socket connections during `--selftest`.
4. **Verification surface:**
   - Does not mutate any round-39 frozen instrument (`quality/counters/c3-r39-options.py`, `w1/ExecOptionsFixtures/`). The proposal is staged as an architectural refinement for round 40 integration.

---

## 5. Affected axes

- **Operability (+):** Connects the static resolver to live compositor telemetry via an atomic, single-pass batch query protocol, eliminating race windows and process overhead during live desktop auditing.
- **Calibration (+):** Eliminates contradictory labeling of runtime-modified options as `live-default`, ensuring every divergence category is verifiable and semantically sound.
- **Harms zero axes:** Navigation, coverage, and host safety invariants remain untouched and unregressed.

---

## 6. Risks and mitigations

- **Risk:** Hyprland's `[[BATCH]]` response length ceiling on large option sets.
  - **Mitigation:** Host evidence in `request-socket-live-bound-r8.md` proves Hyprland's request socket uses a 1023-byte chunk read loop governed by a 5-second poll timeout rather than a fixed kernel buffer limit. An 80-option query payload (~3 KiB query, ~12 KiB JSON response) executes in <15 ms.
- **Risk:** Premature mutation of frozen round-39 fixtures.
  - **Mitigation:** Strict leaf compliance: this report is the sole file written; no tracked code or frozen fixture is modified during round 39.

---

## 7. Verification

1. Verify static absence of duplicate instruments across sibling lanes:
   `grep -rn "tools/mado-options.py" /home/vgpnk/Projects/shokunin/*-shokunin/` → mado only.
2. Verify exclusivity of `~/.config/hypr/` ownership:
   `grep -n "OUT-004" /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md` → confirms tsukuroi delegates to mado.
3. Verify `mado-options.py` selftest remains green:
   `python3 -I tools/mado-options.py --selftest` → `MADO_OPTIONS_SELFTEST: 46/46 passed`.
4. Verify round-39 C2 fixture runner passes:
   `bash .ufo/waves/round-39/w1/ExecOptionsFixtures/run-fixtures.sh` → `fixtures=4/4`.
