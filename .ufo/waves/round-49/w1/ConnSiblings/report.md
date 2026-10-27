# ConnSiblings — Sibling-Overlap Scan & UFO-FSD Connector Proposal (mado round 49 w1)

**Seat:** ConnSiblings  
**Lane:** mado-shokunin  
**Round:** 49 (hyaku run 9, 2026-10-27), Wave: w1 (BUILD)  
**Base:** `03e4ae76aff7a4be59cb69970dd553baa319695a`  
**Declared Claims:**  
- **C1 (operability):** `tools/mado-keysym.py` (which key and modifiers type a keysym; bit-for-bit reproduction of pinned `xkbcli-how-to-type --keymap=FILE --disable-compose --keysym ARG`, libxkbcommon 1.13.2).  
- **C2 (coverage):** `corpus/knowledge/hyprland-bind-key-match-r49.md` (how Hyprland 0.56.2 turns the key field of `bind` into something a key press matches: keysym resolution, `input:resolve_binds_by_sym`, modifier masks).  

---

## 1. Sibling-Overlap Census Across 20 Sibling Lanes

All 20 sibling repositories under `/home/vgpnk/Projects/shokunin/*-shokunin` were scanned read-only across their primary boundary surfaces (`PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`) for keysym, keymap, bind, and input ground.

### Sibling Inventory

| Sibling Lane | Scanned Files | Ground Found / Boundary Analysis | Contested? |
|---|---|---|---|
| `audio-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | SFX & soundtrack headless analysis; routes engine triggers to game lanes. 0 hits for xkb/keysym/keymap/bind/input. | None |
| `chousa-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | Research method, tools & verification gates. "Bind" occurs strictly as verdict/citation bindings in paperwork ledgers (`README.md:13,15,18,19`). 0 hits for xkb/keysym/keymap. | None |
| `game-dev-2d-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | 2D game production verified by headless Godot fixtures (`PROVINCE.md:3`). Owns in-engine input replay and event loops for game entities, not host compositor/XKB keymaps. | None |
| `game-dev-3d-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | 3D game production under headless fixtures. Explicitly acknowledges mado at line 75: `"Desktop/compositor display behavior belongs to mado-shokunin (../mado-shokunin/PROVINCE.md:3-12)"`. 0 hits for host xkb/keymap. | None |
| `kagi-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | Secrets & vault ops, credential custody. "Bind" occurs only as JWT audience and role bindings (`PROVINCE.md:53`). 0 hits for xkb/keysym/keymap. | None |
| `kaidoku-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | Reverse engineering of shipped artifacts with REA. "Binding" appears for snapshot SBOM manifests (`PROVINCE.md:26,209,392`). Round-36 unblob extraction touched neovim runtime syntax files (`xkb.vim`), but claims no XKB or compositor ground. | None |
| `kake-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | Web properties, Pages publishing. "Bind" occurs for network socket port binding (`PROVINCE.md:116`) and Baiduspider crawler directives (`PROVINCE.md:377`). 0 hits for xkb/keysym/keymap. | None |
| `kama-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | Local model-serving endpoint identity and health. "Bind" occurs strictly for role bindings and launcher digest verification (`README.md:22,76,107,282`). 0 hits for xkb/keysym/keymap. | None |
| `kasegi-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | Bounty & security research, CVE/VEX evidence. "Bind" occurs for capture-binding rules and directive bindings (`PROVINCE.md:71,103,132`). 0 hits for xkb/keysym/keymap. | None |
| `kengaku-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | LLM evaluation, benchmark methods. "Bind" occurs for bubblewrap container bind mounts (`bwrap --ro-bind`, `PROVINCE.md:321,323,329,330`). Cites mado's `quality/counters/c1-r41-globals.py` as prior art for sandboxed counters (`PROVINCE.md:326,344`). 0 hits for xkb/keysym/keymap. | None |
| `kotoba-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | Prompt & skill craft. Explicitly acknowledges mado at line 69: `"mado owns the Hyprland/waybar/walker/terminal config plane and display behavior read-only; it states no split with kotoba and treats the omarchy skill as read-only documentation (mado PROVINCE.md:10), claiming no lane SKILL.md."` | None |
| `kotodama-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | Generative linguistic-cultural worldbuilding for fictional worlds. 0 hits for xkb/keysym/keymap/bind/input. | None |
| `kumitate-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | OMP task/hub and ufo orchestration tooling. "Bind" occurs for dispatch-to-task result bindings. 0 hits for xkb/keysym/keymap. | None |
| `lore-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | Fictional world entities and timeline. 0 hits for xkb/keysym/keymap/bind/input. | None |
| `mori-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | Fleet/host liveness and kill/OOM reporting. "Bind" occurs strictly for dispatch-attempt bindings (`PROVINCE.md:134-135`). 0 hits for xkb/keysym/keymap. | None |
| `revenger-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | Reverse engineering of shipped binary artifacts. 0 hits for xkb/keysym/keymap/bind/input. | None |
| `souji-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | Receipt-gated artifact cleanup. "Bind" occurs for hostile bind mount defenses (`PROVINCE.md:107`) and source/fixture bindings (`PROVINCE.md:151`). 0 hits for xkb/keysym/keymap. | None |
| `tabi-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | Browser-session and web-interaction evidence. Mentions keyboard patterns for accessible widget roles (`corpus/SOURCES.md:39`), but no host XKB keymap or compositor binds. | None |
| `tameshi-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | Reusable verification and mutation-testing method. Cites mado's `tools/mado-verify.sh` (`PROVINCE.md:32-35`) as primary surface from round-6 service run. Does not own lane gates or domain contracts. | None |
| `tsukuroi-shokunin` | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` | Host operability & system repair (OS substrate, pacman packages, systemd, drivers/firmware). Holds ADJ-03 (`PROVINCE.md:48`): `"Desktop rendering, bindings, menu or idle behavior needs configuration-level diagnosis"` -> Next analysis recipient: `mado` (`../mado-shokunin/PROVINCE.md:3-16`). OUT-004 (`PROVINCE.md:124`) anchors mado as owner of Hyprland configuration, keybinds, rules, screen/idle behavior. Tsukuroi retains only OS package/driver/unit health. 0 hits for xkb/keysym/keymap in corpus. | None |

### Summary of Contested Scope
**Contested scope: NONE (0 items).**  
No sibling lane claims keysym-to-key resolution, XKB keymap analysis, `how-to-type` reproduction, or Hyprland bind matching. Tsukuroi, kotoba, and game-dev-3d explicitly cede the desktop and compositor configuration plane (including keybinds and display behavior) to mado. Tsukuroi retains host OS package integrity (`libxkbcommon`, `xkeyboard-config`, `hyprland`), which mado respects by using read-only caller-supplied keymaps and non-mutating sandbox execution.

---

## 2. Proposed PROVINCE.md Refinement for mado

In `mado-shokunin/PROVINCE.md`, the round-46 refinement (lines 102–115) stated:
> *"the keybind keymap (`resolve_binds_by_sym`) is not part of this join."*

With round 49's C1 (`tools/mado-keysym.py`) and C2 (`corpus/knowledge/hyprland-bind-key-match-r49.md`), this join exclusion is resolved. The tool inventory and owned surfaces must be refined append-only.

### Proposed Refinement Text (to append to `mado-shokunin/PROVINCE.md`):

```markdown
**Round-49 refinement (append-only; one tool, one knowledge entry, two counters; no new write surface):** the keybind keymap and keysym-to-key resolution plane is owned here, resolving the round-46 join limit that left `resolve_binds_by_sym` out. `tools/mado-keysym.py` reads a caller-supplied compiled keymap file (`--keymap`, regular file, serialized by `xkbcli compile-keymap` from xkeyboard-config 2.48 RMLVO names) and a keysym name or numeric value (`--keysym`); it runs in-process with Python 3 stdlib only, writes nothing, starts no child process, opens no socket, and reproduces the exact stdout and exit status of pinned `xkbcli-how-to-type --disable-compose` under libxkbcommon 1.13.2. Hyprland 0.56.2 bind key-press matching (`corpus/knowledge/hyprland-bind-key-match-r49.md`) grounds how the key field of `bind` maps to keysyms (two-stage `xkb_keysym_from_name` with `XKB_KEYSYM_CASE_INSENSITIVE` fallback, `code:` keycodes) and matches key events under global `m_xkbTranslationState` vs per-device `m_xkbSymState` (`input:resolve_binds_by_sym`). Tsukuroi owns the underlying package state (`libxkbcommon`, `xkeyboard-config`, `hyprland` under ADJ-03 / OUT-004); mado owns the read-only config prediction and keymap-resolution instruments; the operator applies configuration changes.
```

---

## 3. UFO-FSD Connector Move

### (a) Evidence
1. **Contract vs Upstream Semantics:**
   - C1 draft contract specifies `mado-keysym.py how-to-type --keymap FILE --disable-compose --keysym ARG` must match pinned `/usr/lib/xkbcommon/xkbcli-how-to-type`.
   - Inspection of `how-to-type.c:286` reveals that upstream `how-to-type` parses ARG via:
     `*keysym = xkb_keysym_from_name(argv[optind], XKB_KEYSYM_NO_FLAGS);`
     This is **strictly case-sensitive**. Tested live: `/usr/lib/xkbcommon/xkbcli-how-to-type --disable-compose --keysym SLASH` exits 2 with `ERROR: Failed to convert argument to keysym`, while `--keysym slash` succeeds with rc 0.
2. **Hyprland Bind Matching Semantics:**
   - Inspection of Hyprland 0.56.2 `src/managers/KeybindManager.cpp:710-711` reveals:
     `const auto KBKEY = xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_NO_FLAGS);`
     `const auto KBKEYLOWER = xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_CASE_INSENSITIVE);`
     Hyprland accepts case-insensitive keysym names in `bind = MODS, KEY, ...` (e.g. `SLASH`, `Return`, `q`).
3. **Existing Tool Chain:**
   - Mado's existing `tools/mado-binds.py` (round 25) extracts the raw `key` string from `hyprland.conf` (e.g. `"SLASH"`).
   - If a naive caller pipelines `mado-binds.py`'s `key` field directly into `how-to-type --keysym <key>`, uppercase keysym names like `SLASH` fail with rc 2.
4. **State Selection (`resolve_binds_by_sym`):**
   - In `Hyprland-KeybindManager.cpp:369`:
     `const xkb_keysym_t keysym = xkb_state_key_get_one_sym(pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState, KEYCODE);`
   - Host receipt (`hyprctl getoption input:resolve_binds_by_sym -j`) confirms `int: 0` (false). Hyprland evaluates key presses against `m_xkbTranslationState` (global layout 0), NOT the per-device switched layout `pKeyboard->m_xkbSymState`.

### (b) Affected Axes
- **operability (C1):** Capability acquisition of `tools/mado-keysym.py` to predict which key and modifiers type a keysym.
- **coverage (C2):** Sourced ground in `corpus/knowledge/hyprland-bind-key-match-r49.md` explaining Hyprland bind matching.
- **verification (Quality/Freeze):** Preventing specification divergence between C1's strict judge compliance and C2's case-insensitive bind matching.

### (c) Proposed Move: Explicit Two-Tier Architecture in Province & Contracts
Do not conflate the keymap resolution oracle with the compositor bind matcher:
1. **Preserve C1 Contract Purity:** `tools/mado-keysym.py` MUST strictly mirror `xkbcli how-to-type` (refusing uppercase names like `SLASH` with exit code 2 and stderr usage, exactly as the pinned judge does). It MUST NOT implement case-insensitivity or Hyprland heuristics in `mado-keysym.py`.
2. **Document Two-Tier Pipeline in C2 & PROVINCE:** Explicitly document in `corpus/knowledge/hyprland-bind-key-match-r49.md` and the PROVINCE refinement that:
   - Tier 1 (Compositor Bind Interpretation, C2): Translates Hyprland config strings to canonical keysyms via two-stage lookup (`XKB_KEYSYM_NO_FLAGS` then `XKB_KEYSYM_CASE_INSENSITIVE`).
   - Tier 2 (XKB Keymap Resolution, C1): Traces canonical keysyms (or numeric values) through the compiled keymap to physical keycodes and modifier combinations.
   - Pipelining `mado-binds.py` to `mado-keysym.py` requires normalizing through C2's canonical keysym resolver.

### (d) Risks
1. **Specification Leakage:** If a developer attempts to make `mado-keysym.py` "helpful" by accepting uppercase keysym names like `SLASH` without error, the tool will produce stdout on inputs where the pinned judge exits 2, causing the C1 counter to fail.
2. **Layout Assumption Drift:** Assuming `input:resolve_binds_by_sym` is true would lead to predicting binds based on active layout switches rather than layout 0 (`m_xkbTranslationState`). The live host state confirms it is false (0).
3. **Substrate Bleed:** Attempting to read `/usr/share/X11/xkb` raw include files directly rather than compiled keymap files or `/usr/include/xkbcommon/xkbcommon-keysyms.h` would violate bubblewrap isolation and encroach on tsukuroi's package domain.

### (e) Verification
1. **Live Judge Verification:** Confirmed that `/usr/lib/xkbcommon/xkbcli-how-to-type --disable-compose --keysym SLASH` fails with exit code 2, while `--keysym slash` succeeds with exit code 0.
2. **Hyprland Source Check:** Confirmed `Hyprland-KeybindManager.cpp:710-711` uses `XKB_KEYSYM_CASE_INSENSITIVE` for keybind matching.
3. **Host Option Probe:** Confirmed `hyprctl getoption input:resolve_binds_by_sym -j` returns `{"int": 0, "set": false}` on the host.
4. **Sibling Boundaries:** Verified 20/20 sibling lanes show 0 competing claims over keybind, keymap, or keysym ground.
