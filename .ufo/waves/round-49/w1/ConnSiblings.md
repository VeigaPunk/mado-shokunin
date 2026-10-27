# ConnSiblings — Sibling-Overlap Scan & UFO-FSD Connector Proposal (mado round 49 w1)

**Seat:** ConnSiblings  
**Lane:** mado-shokunin  
**Round:** 49 (hyaku run 9, 2026-10-27), Wave: w1 (BUILD)  
**Base:** `03e4ae76aff7a4be59cb69970dd553baa319695a`  
**Status:** Completed.

---

## 1. Executive Summary & Sibling Scan Findings

A comprehensive scan across all 20 sibling repositories under `/home/vgpnk/Projects/shokunin/*-shokunin` was conducted over their primary boundary documents (`PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`).

### Sibling Scope Verdict
- **Contested Scope:** **NONE (0 items)**.
- No sibling lane claims keysym-to-key resolution, XKB keymap analysis, `how-to-type` reproduction, or Hyprland keybind matching.
- **Adjacent boundaries:**
  - `tsukuroi-shokunin`: Retains OS substrate, driver health, systemd units, and pacman package integrity (`libxkbcommon`, `xkeyboard-config`, `hyprland`). Under `ADJ-03` (`PROVINCE.md:48`), tsukuroi explicitly routes desktop rendering and keybinding configuration diagnosis to `mado`. Under `OUT-004` (`PROVINCE.md:124`), tsukuroi anchors mado as the exclusive owner of Hyprland configuration, keybinds, rules, and screen/idle behavior.
  - `kotoba-shokunin`: Explicitly notes in `PROVINCE.md:69` that mado owns the desktop/compositor config plane and display behavior read-only.
  - `game-dev-3d-shokunin`: Explicitly notes in `PROVINCE.md:75` that desktop/compositor display behavior belongs to mado.
  - `tameshi-shokunin`: Owns the reusable mutation-testing method; cites mado's `tools/mado-verify.sh` as a primary surface, leaving gate and domain ownership strictly with mado.

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

### Evidence
1. **Upstream `how-to-type` is strictly case-sensitive:**  
   In `libxkbcommon` 1.13.2 (`tools/how-to-type.c:286`), `--keysym ARG` is parsed via:  
   `*keysym = xkb_keysym_from_name(argv[optind], XKB_KEYSYM_NO_FLAGS);`  
   Live execution verifies: `/usr/lib/xkbcommon/xkbcli-how-to-type --disable-compose --keysym SLASH` exits 2 with `ERROR: Failed to convert argument to keysym`, while `--keysym slash` exits 0.
2. **Hyprland bind key matching is case-insensitive:**  
   In Hyprland 0.56.2 (`src/managers/KeybindManager.cpp:710-711`), key matching performs two-stage resolution:  
   `KBKEY = xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_NO_FLAGS);`  
   `KBKEYLOWER = xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_CASE_INSENSITIVE);`  
   Hyprland accepts binds such as `bind = SUPER, SLASH, ...` and resolves `SLASH` to `slash` via `XKB_KEYSYM_CASE_INSENSITIVE`.
3. **Pipeline Contradiction:**  
   Mado's `tools/mado-binds.py` emits the raw `key` from config (`"SLASH"`). Pipelining this directly to `how-to-type` fails because `how-to-type` rejects uppercase keysym names.
4. **State Lookup Mode:**  
   `Hyprland-KeybindManager.cpp:369` uses `pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState`. On the host, `input:resolve_binds_by_sym` is `false` (0), so Hyprland always evaluates binds against `m_xkbTranslationState` (layout 0).

### Affected Axes
- `operability (C1)`
- `coverage (C2)`
- `verification (Counter freeze)`

### Proposed Move
**Enforce an explicit two-tier separation between the keymap oracle (C1) and the compositor dispatcher (C2):**
1. **Tier 1 (Keymap Oracle, C1):** `tools/mado-keysym.py` MUST strictly match `xkbcli how-to-type`, refusing uppercase names like `SLASH` with exit 2 and stderr usage. It must NEVER add Hyprland-specific case-insensitivity.
2. **Tier 2 (Compositor Dispatcher, C2):** `corpus/knowledge/hyprland-bind-key-match-r49.md` and mado's PROVINCE refinement explicitly define the composition boundary: translating a Hyprland bind key field to a physical key press requires first resolving the canonical keysym name via Hyprland's case-insensitive rules (C2) before querying the keymap oracle (C1).

### Risks
- **Over-unification:** Adding case-insensitive fallback to `mado-keysym.py` would fail C1's judge check on uppercase fixture names.
- **Layout confusion:** Assuming `resolve_binds_by_sym` is active would falsely predict binds on switched layouts, whereas host Hyprland evaluates binds against base layout 0.
- **Substrate bleed:** Reading raw `/usr/share/X11/xkb` trees rather than compiled keymaps would breach sandbox isolation and tsukuroi's package ownership.

### Verification
- Ran `/usr/lib/xkbcommon/xkbcli-how-to-type --disable-compose --keysym SLASH` -> rc 2, confirmed case sensitivity.
- Inspected `Hyprland-KeybindManager.cpp:710-711` and `:369`.
- Verified `hyprctl getoption input:resolve_binds_by_sym -j` -> `{"int": 0, "set": false}`.
- Scanned all 20 sibling `PROVINCE.md`, `corpus/README.md`, and `corpus/SOURCES.md` files; confirmed 0 contested boundaries.

---
Report artifact written to `mado-shokunin/.ufo/waves/round-49/w1/ConnSiblings/report.md` and `.ufo/waves/round-49/w1/ConnSiblings.md`.
