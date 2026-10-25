# Study-path and Frontier Proposals — Round-39 w1 (ConnSourcePaths)

Seat: `ConnSourcePaths` (connector).
Lane repo: `/home/vgpnk/Projects/shokunin/mado-shokunin`
Deliverable: Proposals for `corpus/SOURCES.md` (`## Paths` entries) and `corpus/README.md` (Coverage map entry and `## Frontier` narrative) following round-39's additions.

---

## 1. Proposed `## Paths` Entries for `corpus/SOURCES.md`

Append the following study-path entries under `## Paths` in `corpus/SOURCES.md`:

```markdown
- **Option ownership and configuration variables (round 39)** — S218 → S219 → S158: start from the documented category-merge and syntax rules (S218: 0.56.0 Variables page `#syntax`; `hl.config()` merges per-category so later declarers override only what they pass), then the lane's static resolver (S219: `tools/mado-options.py`; traverses the config include graph in precedence order, resolving last-declarer ownership without touching a socket), then the pinned compositor query handler (S158: `src/debug/HyprCtl.cpp:613-630, 647-723`; implements `getOption` and defines `set`, type and live string representations); this order grounds the five-class divergence vocabulary (`agreement`, `agreement*`, `live-default`, `mismatch`, `config-only`) without mistaking static declarations for live compositor state.
- **Dispatcher surface and request-socket resolution (round 39 amendment)** — S187/S221 → S220 → S018: start from the dual-socket IPC contract and published request flags (S187: 0.56.0 IPC page; S221: `hyprctl` usage page flags `j`, `i`, `r`), then the documented Lua dispatcher vocabulary and purpose (S220 / S196: 0.56.0 Dispatchers page; dispatchers return description tables fed to `hl.bind()`/`hl.dispatch()`), then the pinned compositor request handler (S018: `src/debug/HyprCtl.cpp:1126-1151, 1309, 2096, 1132`; `dispatchRequest` strips flags, tokenizes the dispatcher name, looks it up in `g_pKeybindManager->m_dispatchers`, and wraps into Lua execution); this sequence connects wire grammar to C++ registration and resolves the dual-surface boundary without executing any dispatcher on-host.
```

### Rationale and Sequence Logic
1. **Option Ownership Path (`S218 → S219 → S158`)**:
   - `S218` (Hyprland wiki Variables 0.56.0) is read first: it establishes upstream's documented syntax for general configuration options and the foundational category-merge principle (later `hl.config()` blocks update only what is passed, preserving earlier keys in the same category).
   - `S219` (`tools/mado-options.py`) is read second: it operationalizes this contract across the host's actual 5-layer include hierarchy (defaults tree → theme → user files → toggles glob → `ai-usage.conf`), resolving last-declarer static ownership.
   - `S158` (`HyprCtl.cpp:613-630, 647-723`) is read third: it reveals how the running compositor's `getOption` handler evaluates options at runtime (`set` boolean, custom types, default values). Connecting S219 to S158 explains why the divergence classes (`agreement`, `agreement*`, `live-default`, `mismatch`, `config-only`) map cleanly between static declaration and live query.
   - *Anchor disambiguation*: `HyprCtl.cpp` is cited twice in the registry: S158 holds the option-query handler (`getOption`), whereas S018 holds the rule and dispatcher handlers (`dispatchGetProp`, `dispatchRequest`). S158 is the precise target for option ownership.

2. **Dispatcher Surface and Resolution Path (`S187/S221 → S220 → S018`)**:
   - `S187` / `S221` are read first: S187 defines the request-socket grammar (`[flags]/command args`) and S221 defines the valid flag set (`j`, `i`, `r`).
   - `S220` (0.56.0 Dispatchers page) is read second: it defines the published dispatcher vocabulary and establishes the contract that dispatchers return action tables meant for `hl.bind()` or `hl.dispatch()`.
   - `S018` (`HyprCtl.cpp:1126-1151`) is read third: it shows the internal bridge in `dispatchRequest`, stripping flags, parsing the command name, and looking up the dispatcher in `g_pKeybindManager->m_dispatchers`.
   - *Duplicate resolution note*: S220 shares byte identity with S196; S220 is the re-opened row dedicated to the round-39 amendment's quotes on `hl.bind()`/`hl.dispatch()`. Citing S220 preserves registration compliance while maintaining structural alignment with S187 and S018.

---

## 2. Proposed Coverage Map Addition for `corpus/README.md`

Insert the following row into the `## Coverage map` table in `corpus/README.md` (to satisfy `quality/check-index.py` index completeness):

```markdown
| `knowledge/config-option-table-r39.md` (round 39; surface P1 Hyprland general options) | The static option-ownership table across the Hyprland include graph: five-layer precedence (defaults → theme → user → toggles → ai-usage), last-declarer ownership, comment and variable boundaries, divergence vocabulary against live `getoption` dumps (`agreement`, `agreement*`, `live-default`, `mismatch`, `config-only`), and static-vs-runtime limits; no compositor socket connected. | `source:` S218, S219 in [SOURCES](SOURCES.md); tool `tools/mado-options.py`; recheck on-release. |
```

---

## 3. Proposed `## Frontier` Narrative Update for `corpus/README.md`

Append the following subsection under `## Frontier` in `corpus/README.md`:

```markdown
### Round-39 config-option ownership and dispatcher resolution route

- **Config-option ownership (C2 / C3)**: The hypr-plane option ownership space (identifying which configuration file owns each general `key = value` setting across the include graph) moves from manual point inspection onto automated static prediction: `tools/mado-options.py` (round-39 C2) and [`knowledge/config-option-table-r39.md`](knowledge/config-option-table-r39.md) (round-39 C3). Grounded in documented category-merge semantics ([Variables 0.56.0](SOURCES.md#s218), S218: `hl.config()` merges per-category so later declarers override only the options they pass) and own-work resolver implementation ([options tool](SOURCES.md#s219), S219). The tool traverses the configuration graph in strict precedence order (built-in defaults → theme files → user configs → toggles glob → `ai-usage.conf`), resolving last-declarer ownership without socket access or compositor interaction. When supplied a live `getoption` dump, it automates classification under the established divergence vocabulary (`agreement`, `agreement*`, `live-default`, `mismatch`, `config-only`), closing the manual-checking gap left since round 2 (`knowledge/hyprctl-verification-layer.md`).
  *Still open*: Runtime option mutations via `hyprctl keyword`, Lua-era configuration execution, dynamic variable expansions beyond plain `$VAR` replacement, non-standard key syntax, and specialized configuration directives (binds, animations, window/workspace rules). Static parsing proves declaration precedence within the traversed graph, not live compositor acceptance or engine health.

- **Dispatcher name resolution (Assimilation riding C3 / §10)**: The interface between the request-socket grammar (`dispatch <dispatcher> <args>`) and the keybind manager's internal dispatcher registry moves from documentary inference onto source-verified C++ implementation ground at the host's exact commit `efb50993` ([amended dispatcher surface](knowledge/dispatcher-surface-and-request-grammar-r26.md), S220 and S018). Grounded in the re-opened 0.56.0 Dispatchers documentation ([Dispatchers 0.56.0](SOURCES.md#s220), S220) and tagged `HyprCtl.cpp` source ([HyprCtl.cpp](SOURCES.md#s018), S018). Proves that `dispatchRequest` strips `[flags]` and `dispatch`, tokenizes the dispatcher name, looks it up in `g_pKeybindManager->m_dispatchers.find(DISPATCHSTR)`, returning "Invalid dispatcher" on lookup failure or wrapping execution into the Lua dispatch machinery (`hl.dispatch`).
  *Still open*: No dispatcher was fired, no socket was connected, and server-side execution of individual dispatcher actions remains unmeasured on this host.

- **Instrument calibration repair (C1)**: Calibration re-registers the repaired round-38 discrimination pair (`.ufo/waves/round-39/c1/manifest.json`, `MANIFEST-r39-v1`) with `c1-duprow` properly inside `## Registry`, restoring score from red-before `18/19` (exit 1) to `19/19 TARGET_MET` (exit 0) at freeze commit `457d1b1` and tip without counter mutation.
```

---

## 4. Cross-Axis Synthesis and Safety Invariants

1. **Navigation Axis**:
   - `check-index.py` target: 55/55 → 56/56. Adding `knowledge/config-option-table-r39.md` to `corpus/README.md`'s coverage table keeps the index complete without dangling or missing entries.
   - `corpus/SOURCES.md` `## Paths`: Restores path coverage that halted at round 19, establishing clear discovery routes for option ownership and dispatcher IPC resolution.

2. **Calibration Axis**:
   - `check-axis-scores.py` remains 0 mismatches.
   - `sources-census.sh validate` remains exit 0: S220's duplicate URL with S196 is documented and scoped, avoiding E04 collision.
   - S158 vs S018 citation boundary is maintained: option queries target S158; dispatcher request resolution targets S018.

3. **Operability Axis**:
   - Grounding `tools/mado-options.py` (S219) within the study path clarifies its input and output contracts, regular file policies, and divergence vocabulary for downstream tooling and operators.
