# ScoutShokuknow — round-49 w1 report (assimilation check, read-only)

## Assimilation check — `shokuknow/merge/mado/` themes

- **Input theme: yes, heavily.** The 147-row/69-entry package is dominated by input mediation: focus-grab seat-grab semantics and whitelist admission, `CSeatManager::sendKeyboardKey`/`sendKeyboardMods` routing, the input-capture EIS protocol, Wayland input-security literature, Japanese input-observation sources, XDPH binding.
- **Binds: partial only.** Staged S349 = `wiki.hypr.land/configuring/core/binds/flags/` (live URL, unpinned) cited only for `allow_input_capture`/`locked`; S347/S348 community keybind tables; S217 Lua `hl.bind` examples. Nothing on `xkb_keysym_from_name` flags, translated/untranslated sym, `code:N`/`mouse:`/`switch:`/`catchall`, `resolve_binds_by_sym`, modmask equality, or keycode-vs-keysym precedence.
- **Keysyms/keymaps: no.** The lane already owns the keymap rows S340–S351; the package adds none.
- **Verdict:** package does NOT preempt C1 (`tools/mado-keysym.py`) or C2 (`hyprland-bind-key-match-r49.md`). Ground gaps `keybind-rule-semantics.md §2.3` and `hyprland-input-devices-r46.md:71` stay open. Caveat: staged S349 overlaps the wiki page C2 will cite — C2 should cite the pinned-commit fetch, not the staged row's live URL.

## Id-collision guard (run into seat dir)

| list | count | range |
|---|---|---|
| reg-ids (`corpus/SOURCES.md`, pattern `^ {0,3}\|[[:space:]]*S[0-9]{3,}`) | 288 | S001..S351 |
| staged-ids (`merge/mado/SOURCES.append.md`) | 147 | S203..S349 |
| **collisions (comm -12)** | **94** | S203–S221, S253, S258, S277–S349 |

Same id, different source, proven at the row level: lane `SOURCES.md:298` S349=libxkbcommon messages-codes.h vs staged `:153` S349=wiki binds/flags; lane `:268` S319=`IKeyboard.cpp` vs staged `:123` S319=`Window.cpp`; lane `:207` S205=idle-lock receipt vs staged `:9` S205=wiki dispatchers. Cause: package's S-space was allocated when the registry topped at 192 (MERGE-REPORT.md:9); the lane has since registered S203–S351. Naive append → 94 ambiguous ids; L1 must renumber/reconcile. Cross-id source duplicates also exist (lane S284≈staged S273 FocusGrab.cpp; lane S283≈staged S274/S294 XML; lane S286≈staged S329 PortalManager).

**Guard proof (positive control):** scratch `reg.md` with indented `  | S002 |` row + `staged.md` with `| S002 |` → `collisions.txt` nonempty = `S002`; a non-table `not a row S004` line was excluded. Artifacts in `w1/ScoutShokuknow/guard-proof/`.

## Quarantine slice (`absent-defect-register.md`, lane `mado` data rows)

**13 rows** — payload-absent: S189, S195, S201, S205, S224, S228; never-checked: S199, S200, S209, S222, S223, S225, S235. Verbatim rows: `w1/ScoutShokuknow/quarantine-slice.md`. Note: S205 and S209 are both quarantined lane ids AND inside the collision set — the staged rows must not mask those verdicts.

## Artifacts

`.ufo/waves/round-49/w1/ScoutShokuknow/`: `report.md` (full detail), `reg-ids.txt`, `staged-ids.txt`, `collisions.txt`, `quarantine-slice.md`, `guard-proof/` (scratch inputs + computed lists).

No tools installed; no git/jj mutations; no writes outside the seat dir; scratch `/fast/scratch/hyaku/mado-r49/ScoutShokuknow/` removed.
