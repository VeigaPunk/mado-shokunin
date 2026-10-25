# ScrRowsDraft — SOURCES.md rows S283–S290 for the C2 entry (round 41, w1)

Seat `ScrRowsDraft`. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`. Nothing outside
`.ufo/waves/round-41/w1/ScrRowsDraft/` was written; no git/jj command was run; no counter was run
against the lane (the counter was imported read-only for its `norm()`/`journal_counts()` and row regex).

- `rows-block.txt` — the eight table rows only (no header), ready to append.
- Insertion point: directly after `corpus/SOURCES.md:231` (the `S282` row), before the blank line and
  `## Paths` (`corpus/SOURCES.md:233`). The registry is not id-ordered, so append-at-end is the existing
  convention.

## Rows (as drafted)

See `rows-block.txt`; reproduced verbatim below for review.

| id | source cell (title - location) | kind | tier | status | opened | recheck |
|---|---|---|---|---|---|---|
| S283 | Hyprland focus-grab protocol v1 - upstream XML at protocols `cd1aba6…` | spec | A | mined | 2026-10-25 | on-release |
| S284 | Hyprland 0.56.2 focus-grab implementation - `src/protocols/FocusGrab.cpp` at `efb5099…` | code | A | mined | 2026-10-25 | on-release |
| S285 | Quickshell HyprlandFocusGrab client - `focus_grab/grab.cpp` at `9b0f339…` | code | B | mined | 2026-10-25 | on-release |
| S286 | xdg-desktop-portal-hyprland v1.4.1 registry handler - `src/core/PortalManager.cpp` | code | A | mined | 2026-10-25 | on-release |
| S287 | Hyprland issue 565 - the rule-level counterpart | community | B | mined | 2026-10-25 | 180d |
| S288 | hyprland-protocols README at `cd1aba6…` | docs | A | mined | 2026-10-25 | on-release |
| S289 | mado saved xdph journal - `.ufo/waves/round-41/fetch/xdph-journal.txt` | own-work | A | mined | 2026-10-25 | on-change |
| S290 | Hyprland input-capture protocol v2 - upstream XML at `cd1aba6…` | spec | A | mined | 2026-10-25 | on-release |

Tier notes (curation, scoped):

- S285 is **B**, not A: the file is primary for what that one third-party client does, but quickshell is
  not installed on this host (`quickshell`/`qs` not on PATH, `ScoutPackageFocus/survey.md` §own-work
  re-checks) and is authoritative for nothing beyond its own lifecycle. The row's scope says so.
- S287 is **community/B**: the kind enum forbids A for `community`; the thread carries reproducible
  detail (rule lines, log excerpts, state), but the row scopes it to the 2022 hyprlang era and states the
  closure, so it cannot be read as a 0.56.2 guarantee.
- S289 is the **single** `own-work` row among the new ids, as clause h requires (`kind` cell = `own-work`).

## Location uniqueness (counter clause e)

Each cell 1 ends with a distinct last whitespace token; every token was grepped against the current
registry first (0 occurrences each) and then checked with the counter's own clause-e expression against
the 219 existing rows plus the 8 new ones:

```
hyprland-focus-grab-v1.xml 0 | FocusGrab.cpp 0 | focus_grab/grab.cpp 0 | core/PortalManager.cpp 0
issues/565 0 | protocols/README.md 0 | xdph-journal.txt 0 | input-capture-v1.xml 0
```

```
E S283 same=['S283'] OK   E S284 same=['S284'] OK   E S285 same=['S285'] OK   E S286 same=['S286'] OK
E S287 same=['S287'] OK   E S288 same=['S288'] OK   E S289 same=['S289'] OK   E S290 same=['S290'] OK
clause e all unique: True
```

None of the eight locations contains `amgsk.dev`, `zhihu`, `/zh` or `/ja` (clause i's `BAD_LOC`).

## Schema census (frozen CORPUS.md commands, on `SOURCES.md` + `rows-block.txt` in a `/tmp` copy)

```
rows=227   malformed=0   A=217 B=3 C=7   mined=208 queued=10 rejected=9   dups-done   enums-done
```

`NF=13` (11 cells) for all eight; `opened` = 2026-10-25 for all eight (clause c: ids absent at BASE);
`recheck` values `on-release` ×6, `180d`, `on-change` — all match `^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)$`;
`used-by` = `corpus/knowledge/hyprland-focus-grab-r41.md` as the only item.

## Gate quotes (clause d) — proposed, each verified present

Each quote is 3–25 whitespace words, occurs in the **normalized** text of that id's own receipt
(`norm()` from `quality/counters/c2-r41-focus-entry.py`: tags/scripts/styles stripped, entities decoded,
whitespace collapsed), and no two quotes repeat. Clause g needs the same string, verbatim, on the entry
line that names the id.

| id | receipt (all under `.ufo/waves/round-41/fetch/`) | bytes | sha256 (first 16) | quote | words |
|---|---|---|---|---|---|
| S283 | `focus-grab-v1.xml` | 5447 | `0bc60c14d27f9079` | `This interface restricts input focus to a specified whitelist of surfaces` | 11 |
| S284 | `Hyprland-FocusGrab.cpp` | 6242 | `53b762f7149bf1c3` | `m_grab->m_keyboard = true;` | 3 |
| S285 | `quickshell-grab.cpp` | 2568 | `6f7cecf15a4dbfd0` | `the protocol will always send cleared() when the grab is deactivated,` | 11 |
| S286 | `xdph-PortalManager.cpp` | 24182 | `15c3e39cea5af1a9` | `Got interface: {} (ver {})` | 5 |
| S287 | `issue-565.html` | 475170 | `148a9053e813a7d9` | `Tried to set workspace silent rule to a nofocus window!` | 10 |
| S288 | `protocols-README.md` | 1903 | `3c7007636e138898` | `for grabbing input focus, primarily for complex context menus` | 9 |
| S289 | `xdph-journal.txt` | 19130 | `bf8fa91a32119727` | `Got interface: hyprland_focus_grab_manager_v1 (ver 1)` | 5 |
| S290 | `input-capture-v1.xml` | 6765 | `fff89f6f9de622fe` | `Add one barrier to the current session` | 7 |

Run output (`present=True uniq=True` for all eight):

```
S283 bytes=5447 sha=0bc60c14d27f9079 words=11 present=True uniq=True
S284 bytes=6242 sha=53b762f7149bf1c3 words=3 present=True uniq=True
S285 bytes=2568 sha=6f7cecf15a4dbfd0 words=11 present=True uniq=True
S286 bytes=24182 sha=15c3e39cea5af1a9 words=5 present=True uniq=True
S287 bytes=475170 sha=148a9053e813a7d9 words=10 present=True uniq=True
S288 bytes=1903 sha=3c7007636e138898 words=9 present=True uniq=True
S289 bytes=19130 sha=bf8fa91a32119727 words=5 present=True uniq=True
S290 bytes=6765 sha=fff89f6f9de622fe words=7 present=True uniq=True
```

Receipt paths are distinct and every receipt is ≥ 512 B (clause d). The eighth receipt pair is not a
collision: S286's quote is the format string, S289's is the logged advert line.

Gate line form (one per id, column 0, in `corpus/lessons/round-41.md` `## Gate`):

```
GATE S283 receipt=.ufo/waves/round-41/fetch/focus-grab-v1.xml sha256=0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4 quote="This interface restricts input focus to a specified whitelist of surfaces"
GATE S284 receipt=.ufo/waves/round-41/fetch/Hyprland-FocusGrab.cpp sha256=53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1 quote="m_grab->m_keyboard = true;"
GATE S285 receipt=.ufo/waves/round-41/fetch/quickshell-grab.cpp sha256=6f7cecf15a4dbfd0dc39341c8794639595a83dd2a4ab13b6b377ac970a301a40 quote="the protocol will always send cleared() when the grab is deactivated,"
GATE S286 receipt=.ufo/waves/round-41/fetch/xdph-PortalManager.cpp sha256=15c3e39cea5af1a92924ebc1ffe0f7825c86ac3c0b49e894aede86b2e091ea55 quote="Got interface: {} (ver {})"
GATE S287 receipt=.ufo/waves/round-41/fetch/issue-565.html sha256=148a9053e813a7d912c3c2e9fdb234ef42d20004438d33b41f1110d37679d1dc quote="Tried to set workspace silent rule to a nofocus window!"
GATE S288 receipt=.ufo/waves/round-41/fetch/protocols-README.md sha256=3c7007636e13889860491d0c57f93c29d92122d17838ca1f6559e4aeb7aa6323 quote="for grabbing input focus, primarily for complex context menus"
GATE S289 receipt=.ufo/waves/round-41/fetch/xdph-journal.txt sha256=bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7 quote="Got interface: hyprland_focus_grab_manager_v1 (ver 1)"
GATE S290 receipt=.ufo/waves/round-41/fetch/input-capture-v1.xml sha256=fff89f6f9de622fefa1a62a6e6970f76683b6328454565583046abebcfe2c360 quote="Add one barrier to the current session"
```

Held ids the entry also cites need their own Gate lines with their own receipts; that is the lesson
seat's file, not mine (see the used-by section for which held ids are plausible).

## Provenance: the receipts are the pinned upstream bytes

Read-only re-fetch of each pinned URL on 2026-10-25 (`curl -sSL`, into `/tmp`, deleted after), compared
byte-for-byte with the committed fetch receipt:

```
xml    http=200 bytes=5447  sha256=0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4
fgcpp  http=200 bytes=6242  sha256=53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1
qsgrab http=200 bytes=2568  sha256=6f7cecf15a4dbfd0dc39341c8794639595a83dd2a4ab13b6b377ac970a301a40
xdph   http=200 bytes=24182 sha256=15c3e39cea5af1a92924ebc1ffe0f7825c86ac3c0b49e894aede86b2e091ea55
readme http=200 bytes=1903  sha256=3c7007636e13889860491d0c57f93c29d92122d17838ca1f6559e4aeb7aa6323
inpc   http=200 bytes=6765  sha256=fff89f6f9de622fefa1a62a6e6970f76683b6328454565583046abebcfe2c360
```

Every hash equals `sha256sum` of the corresponding file in `.ufo/waves/round-41/fetch/`. URLs used:
`raw.githubusercontent.com/hyprwm/hyprland-protocols/cd1aba6bd78775825eb230b3a4274c48b6705eb7/{README.md,protocols/hyprland-focus-grab-v1.xml,protocols/hyprland-input-capture-v1.xml}`,
`raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/FocusGrab.cpp`,
`raw.githubusercontent.com/quickshell-mirror/quickshell/9b0f339b19057f4731bf3b48293307d7ef241671/src/wayland/hyprland/focus_grab/grab.cpp`,
`raw.githubusercontent.com/hyprwm/xdg-desktop-portal-hyprland/v1.4.1/src/core/PortalManager.cpp`.
`issue-565.html` was **not** re-fetched for byte comparison (GitHub serves a dynamic page); the row states
it as a capture of 2026-10-25 and cites receipt lines, not a live anchor.

## Facts each row's cells assert (all re-derived in this seat)

- S283 `:39-58` manager, `:60-77` grab description, `:79-127` requests + `cleared` (verified with `awk`
  on the receipt: line 39 `<interface name="hyprland_focus_grab_manager_v1" version="1">`, 58 `</interface>`,
  60 `<interface name="hyprland_focus_grab_v1" version="1">`, 77 `</description>`, 79 `<request name="add_surface">`,
  127 `</interface>`). Interface text at `:62-63` is the whitelist sentence; `:121` is `<event name="cleared">`.
- S284 function boundaries verified (`grep -n '^void|^bool|^CFocusGrab|^}'`): ctor `:15-29`, dtor `:31-33`,
  `start` `:47-56`, `finish` `:58-71`, `refocusKeyboard` `:94-111`, `commit` `:113-143`, `bindManager`
  `:149-155`, `onCreateGrab` `:165-173`. `m_grab->m_keyboard = true;` at `:20`; `finish(true)` callback at
  `:22`; `sendCleared` guard `:68-69`; dtor calls `finish(false)` at `:32`.
- S285 line anchors verified: `add_surface` `:66`, `commit()` `:75`, the cleared comment `:78`, activated
  emit `:83-85`, `hyprland_focus_grab_v1_cleared` `:98-101`.
- S286 `onGlobal` `:85-88` logs before any bind branch; nine binds at `:92, :97, :101, :104, :110, :116,
  :129, :247, :259`; registry callbacks `:300-301`. `grep -ci 'focus_grab|focus-grab|focus grab'
  xdph-PortalManager.cpp` = **0** (exit 1), so "none of which is the focus-grab manager" is an observed
  absence in this file, scoped to v1.4.1's `PortalManager.cpp`.
- S287: `"state":"CLOSED"` and `"stateReason":"COMPLETED"` in the embedded data; `"createdAt":"2022-08-23T14:03:55Z"`;
  maintainer replies `2022-08-25`; the log marker occurs at receipt lines 686 (embedded body) and 706
  (rendered body). No `closedAt` field exists in the page, so the row does **not** assert a closure date.
- S288 `:5` bridge sentence, `:13` `## Finished protocols`, `:17` focus-grab bullet, `:22` input-capture bullet.
- S289: `wc -l` 153; boot marker `:78`; the focus-grab advert `:117`; the counter's own `journal_counts()`
  on the receipt returns `(2, 78, 63, 1)` = sessions, adverts, distinct names in the latest session,
  focus-grab adverts in the latest session.
- S290 `:34-36` description, `:38-51` manager v2, `:53-58` session-interface description, `:67-78`
  add_barrier, `:105-112` `eis_fd` (line 113 is the next event, `disabled`).

## Used-by additions for held rows the entry cites (old → new, cell 11 only)

Clause c requires, for an id present at BASE, cells 1–10 byte-equal to the BASE row and used-by listing
the entry. **Status now: `ScrEntryA` cites exactly one held id, `S037`; `ScrEntryB` and `ScrEntryC` cite
none** (each seat's own message). So S037's row below is the only one that applies if A is the selected
entry; the rest stay conditional and must not be applied otherwise (an unused addition makes the registry
claim a citation that does not exist).

| id | old used-by (cell 11) | new used-by (cell 11) | status |
|---|---|---|---|
| S037 (`corpus/SOURCES.md:49`) | `corpus/knowledge/xdg-portal-routing-r12.md` | `corpus/knowledge/xdg-portal-routing-r12.md, corpus/knowledge/hyprland-focus-grab-r41.md` | **apply if A is selected** |
| S041 (`:53`) | `corpus/knowledge/wayland-protocol-boundaries-r13.md, corpus/knowledge/output-colour-boundaries-r14.md` | `corpus/knowledge/wayland-protocol-boundaries-r13.md, corpus/knowledge/output-colour-boundaries-r14.md, corpus/knowledge/hyprland-focus-grab-r41.md` | conditional |
| S043 (`:55`) | `corpus/knowledge/wayland-protocol-boundaries-r13.md` | `corpus/knowledge/wayland-protocol-boundaries-r13.md, corpus/knowledge/hyprland-focus-grab-r41.md` | conditional |
| S052 (`:64`) | `corpus/knowledge/input-debugging-boundaries-r15.md` | `corpus/knowledge/input-debugging-boundaries-r15.md, corpus/knowledge/hyprland-focus-grab-r41.md` | conditional |
| S162 (`:174`) | `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md, corpus/knowledge/animation-table-r26.md, corpus/knowledge/workspace-rules-r27.md, corpus/knowledge/config-option-table-r39.md, corpus/knowledge/hyprctl-getoption-native-forms-r40.md` | same, plus `, corpus/knowledge/hyprland-focus-grab-r41.md` | conditional |
| S031 (`:43`) | `corpus/knowledge/xdg-portal-routing-r12.md` | `corpus/knowledge/xdg-portal-routing-r12.md, corpus/knowledge/hyprland-focus-grab-r41.md` | conditional |

Each such change is an in-place `used-by` edit and must be logged old→new in the round-41 lesson
(`SOURCES.md` contract rule 2).

**S037's Gate receipt (required if A is selected).** A's proposed new fetch file is
`.ufo/waves/round-41/fetch/xdph-installed-version.txt` — 1442 B, sha256
`4294737aa884fd84c2e2a6bf642efa71c281bc480df4f07eb64009d812157ea8`, byte-copied from
`.ufo/waves/round-41/w1/ScrEntryA/s037-installed-version.txt` (verified: same size and hash). It is a
read-only capture of `/var/lib/pacman/local/xdg-desktop-portal-hyprland-1.4.1-2/desc` plus the command and
its output; no package transaction ran. Its Gate quote
`%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2` (4 words) is present in the receipt under `norm()`
and on A's S037 line (line 73), and is distinct from every other id's quote. Caveat for the L1: this
receipt grounds the **installed package record** (`1.4.1-2`), not S037's release-page anchor
(`releases/tag/v1.4.1`, tag commit `cc8e5ef`); S037's cells 1–10 stay byte-equal to BASE, and the row's
`teaches` already scopes itself to "installed XDPH upstream release identity", which the package record
supports at the version level only.

**Held rows cost a receipt too.** Clause d applies to *every* cited id, not only the new ones: a cited
held id needs one `GATE` line whose `receipt=` path starts with `.ufo/waves/round-41/fetch/`, is ≥ 512 B,
has the sha256 the line states, and is distinct per id. `round-41/fetch/` today holds nine files, none of
them a receipt for S037, S041, S043, S052, S162 or S031 (`ls .ufo/waves/round-41/fetch/`), so the lesson
seat must commit one distinct round-41 receipt per held id it cites (for S041 the existing
`.ufo/waves/round-13/w1/globals.json` would have to be copied into `round-41/fetch/`, which is a new file
in the fetch dir, not an edit to the frozen round-13 artifact). A held id cited without such a receipt
fails clause d and takes the whole predicate to `TARGET_MISSED`.

## Cross-check against the two entry drafts that existed when this seat closed

`ScrEntryB/hyprland-focus-grab-r41.md` and `ScrEntryC/hyprland-focus-grab-r41.md` were read after they
were written; the check is clause g's own rule (an unfenced line that names the id and carries the Gate
quote), run with the counter's `unfenced()` and my proposed quotes:

```
== ScrEntryA  8 source lines (S283-S289 + S037)  S283..S289:ok  S037:ok  S290:not cited
== ScrEntryB  85 lines  S283:ok S284:ok S285:ok S286:ok S287:ok S288:ok S289:ok S290:ok
== ScrEntryC  67 lines  S283:ok S284:ok S285:ok S286:ok S287:ok S288:ok S289:ok S290:not cited
```

- **A cites S037**, so if A is selected the S037 used-by edit above applies *and* the new receipt
  `.ufo/waves/round-41/fetch/xdph-installed-version.txt` must be committed (1442 B, sha256
  `4294737a…`); A's `gates.txt` already carries the matching `GATE S037` line and its S037 quote
  (`%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2`) is on A's S037 line (line 73). A cites no other
  held id.
- **S290 is cited only by B.** `rows-block.txt` drafts S290 as `mined` with the entry in used-by, which is
  correct if B is selected. If A or C is selected, S290 is uncited by the entry, and the `SOURCES.md`
  contract defines `mined` as "cited by ≥1 path in used-by": the L1 must then either drop S290 from the
  block or land it as `status queued` with `used-by —` (the counter only requires that *cited* ids be
  `mined` with the entry listed, so a `queued` S290 does not fail clause c; a `mined` S290 naming an entry
  that does not cite it would be a false registry claim).
- First pass: B's S287 line (`:69`) quoted `New windows in inactive workspaces stealing focus`, which is
  **not** in `issue-565.html` (`grep -c` = 0 in both drafts and in the receipt's text). B was told, fixed
  the line, and re-ran its own `verify-quotes.py`; the pass above is the post-fix state. Both drafts'
  census lines match the counter's `journal_counts()` = `(2, 78, 63, 1)`.
- C's header first stated the issue was "closed 2022-08-25"; the receipt has no `closedAt` field, so C was
  told and corrected it to `createdAt 2022-08-23, state CLOSED reason COMPLETED, replies dated 2022-08-25`
  (re-checked at 67 lines: 7/7 quote alignment still passes, no closure date asserted). The row (S287)
  asserts only `CLOSED`/`COMPLETED` plus the 2022-08-25 reply date.

## Out of scope / not drafted

- `fetch/Hyprland-FocusGrab.hpp` (sha256 `dce47251853f8d95…`, 2607 B) and a `FocusState.cpp` row (scout
  fetched it in scratch, sha256 `9b971362bba97f20…`) are not in the assigned S283–S290 set. If the entry
  cites them they need S291/S292 rows plus receipts under `round-41/fetch/`; the `.hpp` receipt is present
  and unused, `FocusState.cpp` is not in `fetch/`.
- No registry edit was made: `corpus/SOURCES.md` is untouched (frozen for this seat); the L1 appends.
- No claim is made that `corpus/lessons/round-41.md` or `corpus/README.md` exist yet; clauses d/f/g/i are
  the entry and lesson seats' deliverables.
