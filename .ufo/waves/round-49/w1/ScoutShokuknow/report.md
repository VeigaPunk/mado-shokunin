# ScoutShokuknow — round-49 w1 assimilation check (read-only package)

Seat dir: `.ufo/waves/round-49/w1/ScoutShokuknow/`. All reads only; no campaign tool run.

## 1. Theme check — `shokuknow/merge/mado/` vs this round's claims

**Input theme: yes, heavily — binds only partially; keysyms/keymaps: no.**

The staged package (`MERGE-REPORT.md`: 147 rows S203–S349, 69 knowledge entries + 4 amendments) is dominated by *input mediation*: focus-grab seat-grab semantics (staged S273/S274/S288/S294/S313), seat-manager keyboard routing (`CSeatManager::sendKeyboardKey` / `sendKeyboardMods`, staged S317), input-capture EIS protocol (staged S332), Wayland input-security literature (staged S278/S279/S280/S324), Japanese input-observation sources (staged S323/S333/S334/S344), and XDPH portal binding (staged S329).

On **binds** it carries only:
- staged S349 → `https://wiki.hypr.land/configuring/core/binds/flags/` (live URL, unpinned), quoted only for `allow_input_capture`/`locked` rows (`upstream-input-holds-and-the-lock-screen-r16.md:19-21` — verified at that file:19-21). The same page's `i`/`ignore_mods` row is C2's territory and is NOT cited there.
- staged S347/S348 → community-tier keybind syntax/keybind tables (Qiita, CSDN), INF-docs level only.
- staged S217 → CSDN `hl.bind(...)` Lua examples.

It carries **nothing** on: `xkb_keysym_from_name` and its flags, translated-vs-untranslated sym, `code:N`/`mouse:`/`switch:`/`catchall` key forms, `resolve_binds_by_sym`, modmask equality rules, or keycode-vs-keysym precedence. The lane already owns the keymap-side rows (S340–S351: xkb rules matcher, compiler, include paths, br symbols file, xkbcli compile-keymap, messages-codes.h, keymap constructors) — the package does not touch them.

**Verdict for C1/C2:** the staged package does NOT preempt `tools/mado-keysym.py` (C1) or `corpus/knowledge/hyprland-bind-key-match-r49.md` (C2). C2's ground gaps — `keybind-rule-semantics.md §2.3` [INF-docs] and `hyprland-input-devices-r46.md:71` — remain open. One assimilation caveat: staged S349 names the same wiki Binds-flags page C2 will cite; C2 should cite the pinned hyprland-wiki *commit* fetch (as declared), not the live URL the staged row points at.

## 2. Id-collision guard

Command (run into seat dir):
```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <file> | grep -oE 'S[0-9]{3,}' | sort -u > <ids>
comm -12 reg-ids.txt staged-ids.txt > collisions.txt
```

| list | file | unique ids | range |
|---|---|---|---|
| reg-ids | `corpus/SOURCES.md` (lane) | **288** | S001..S351 |
| staged-ids | `merge/mado/SOURCES.append.md` | **147** | S203..S349 |
| **collisions** | — | **94** | S203–S221 (19), S253, S258, S277–S349 (73) |

Same id, different source — sampled:
- lane `SOURCES.md:298` S349 = libxkbcommon `messages-codes.h` vs staged `SOURCES.append.md:153` S349 = wiki binds/flags page.
- lane `SOURCES.md:268` S319 = `IKeyboard.cpp` @efb50993 vs staged `:123` S319 = `Window.cpp` @v0.56.2.
- lane `SOURCES.md:219` S217 = `Logger.hpp` vs staged `:21` S217 = CSDN Lua blog.
- lane `SOURCES.md:207` S205 = host idle-lock receipt (own-work) vs staged `:9` S205 = wiki dispatchers page.

Interpretation: the package's S-space was allocated when the registry topped at 192 (MERGE-REPORT.md:9); the lane has since registered S203–S351 with different sources. A naive append creates 94 ambiguous ids → **L1 must renumber the staged rows or reconcile before adoption**. Source-level duplicates also exist under different ids (lane S284=FocusGrab.cpp@efb50993 ≈ staged S273 same file @v0.56.2 tag; lane S283 ≈ staged S274/S294 focus-grab XML pinned-commit vs `main`; lane S286 ≈ staged S329 XDPH PortalManager v1.4.1 vs `master`).

### Guard proof (positive control)

Scratch registry/staged pair written at `/fast/scratch/hyaku/mado-r49/ScoutShokuknow/guard-proof/` and copied to `guard-proof/` here. The scratch `reg.md` contains an indented `  | S002 |` row; the pattern captured it, `comm -12` produced **nonempty collisions.txt = `S002`** (1 line), and a non-table `not a row S004` line was correctly excluded.

## 3. Quarantine slice — `mado` rows of `absent-defect-register.md`

Pattern `^\|[[:space:]]*`mado`[[:space:]]*\|[[:space:]]*round[0-9]+[[:space:]]*\|[[:space:]]*`?S[0-9]+`?` → **13 data rows**, verbatim in `quarantine-slice.md`:

- payload-absent (register §"Rows", header `absent-defect-register.md:27`): S189 (round1, EventManager.cpp), S195 (round2, arch-wiki-docs-zh pkg), S201 (round2, arXiv 2604.18860), S205 (round3, archwiki interwikimap API), S224 (round4, `~/.cache/ai-usage/status.json`), S228 (round5, cn-export-hyprland.html).
- never-checked (register §"Rows whose quotes were NEVER CHECKED", header `:265`): S199, S200 (round2; source unfetched), S209, S222, S223, S225, S235 (round3/4/5; gate named no locator).

Note: **S205 and S209 are both quarantined lane ids AND inside the 94-id collision set** — L1 must not let the staged S205/S209 rows mask the quarantine verdicts on the lane's own S205/S209.

## Artifacts in this seat dir
`reg-ids.txt` (288), `staged-ids.txt` (147), `collisions.txt` (94), `quarantine-slice.md` (13 rows), `guard-proof/{reg,staged}.md` + computed id/collision lists, this `report.md`.

## Tools
None installed (grep/comm/sort only). No git/jj mutations. Scratch `/fast/scratch/hyaku/mado-r49/ScoutShokuknow/` deleted at exit.
