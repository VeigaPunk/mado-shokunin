# ScrRowsDraft — SOURCES.md rows S283–S290 for the C2 entry (round 41, w1)

STATUS: complete. Deliverables: `.ufo/waves/round-41/w1/ScrRowsDraft/rows.md` (full draft + evidence) and
`.ufo/waves/round-41/w1/ScrRowsDraft/rows-block.txt` (the eight table rows only).

Scope: draft the eight new registry rows in the frozen 11-column schema, with unique locations (counter
clause e) and used-by `corpus/knowledge/hyprland-focus-grab-r41.md`, plus the used-by additions for held
rows the entry cites. `corpus/SOURCES.md` was **not** edited (frozen; the L1 integrates).

## Rows (S283 → S290, the assigned order)

| id | location (last token of cell 1) | kind | tier | recheck |
|---|---|---|---|---|
| S283 | `…/hyprland-protocols/cd1aba6…/protocols/hyprland-focus-grab-v1.xml` | spec | A | on-release |
| S284 | `…/Hyprland/efb5099…/src/protocols/FocusGrab.cpp` | code | A | on-release |
| S285 | `…/quickshell/9b0f339…/src/wayland/hyprland/focus_grab/grab.cpp` | code | B | on-release |
| S286 | `…/xdg-desktop-portal-hyprland/v1.4.1/src/core/PortalManager.cpp` | code | A | on-release |
| S287 | `https://github.com/hyprwm/Hyprland/issues/565` | community | B | 180d |
| S288 | `…/hyprland-protocols/cd1aba6…/README.md` | docs | A | on-release |
| S289 | `.ufo/waves/round-41/fetch/xdph-journal.txt` | own-work | A | on-change |
| S290 | `…/hyprland-protocols/cd1aba6…/protocols/hyprland-input-capture-v1.xml` | spec | A | on-release |

All eight: `status mined`, `opened 2026-10-25`, `used-by corpus/knowledge/hyprland-focus-grab-r41.md`.
S289 is the only `own-work` row (clause h). Insertion point: after `corpus/SOURCES.md:231` (S282), before
the blank line and `## Paths` (`:233`).

## Gates exercised (commands + outcomes)

1. **Schema census, frozen CORPUS.md commands** on a `/tmp` copy of `corpus/SOURCES.md` plus
   `rows-block.txt` (deleted after): `rows=227 malformed=0`, tier `A=217 B=3 C=7`, status
   `mined=208 queued=10 rejected=9`, duplicate-id check empty, enum/tier-inflation check empty.
2. **Clause-e uniqueness**, run with the counter's own expression over the 219 existing rows plus the 8
   new: `same=[S283]…[S290]`, `clause e all unique: True`; `BAD_LOC` (`amgsk.dev`, `zhihu`, `/zh`, `/ja`)
   hits: none. Pre-check: each location token grepped against the current registry first, 0 occurrences.
3. **Clause-d quote check**, using `norm()` imported read-only from
   `quality/counters/c2-r41-focus-entry.py`: all eight proposed quotes present in their own receipt,
   `words=3..11`, no duplicate quote, receipts distinct and ≥ 512 B.
4. **Journal census** with the counter's own `journal_counts()` on `fetch/xdph-journal.txt`:
   `(2, 78, 63, 1)` — matches the census line the entry must carry.
5. **Provenance re-fetch** (read-only, `curl -sSL` into `/tmp`, deleted): the six pinned raw URLs return
   HTTP 200 and byte-identical files — sha256 `0bc60c14…` (xml), `53b762f7…` (FocusGrab.cpp),
   `6f7cecf1…` (quickshell grab.cpp), `15c3e39c…` (xdph PortalManager.cpp), `3c700763…` (README),
   `fff89f6f…` (input-capture xml). `issue-565.html` was not byte-compared (dynamic page) and is cited as
   a 2026-10-25 capture.
6. **Cross-check against the entry drafts**: with the counter's `unfenced()` and the proposed quotes,
   `ScrEntryA` (8 source lines: S283–S289 + S037) passes all eight, `ScrEntryB` (85 lines) passes all
   eight, `ScrEntryC` (67 lines) passes its seven (S290 not cited). B's first pass failed S287 (it quoted a
   phrase absent from the receipt); B was told, fixed the line, and the pass above is the post-fix state.
   A's S037 Gate quote `%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2` is present in its proposed
   receipt (`s037-installed-version.txt`, 1442 B, sha256 `4294737a…`) and on its S037 line.
7. **Held-id receipt verified for A**: `.ufo/waves/round-41/fetch/xdph-installed-version.txt` (proposed
   path) is ≥512 B, distinct from the other eight receipts, and its sha256 matches the seat's copy — so
   clause d is satisfiable for S037 if the L1 accepts a package-record capture as the held row's receipt.

## Touched surfaces

- Written: `.ufo/waves/round-41/w1/ScrRowsDraft/rows.md`, `.ufo/waves/round-41/w1/ScrRowsDraft/rows-block.txt`,
  this report. `/tmp` scratch for the census copy and the re-fetch, deleted.
- Read only: `corpus/SOURCES.md`, `/home/vgpnk/Projects/shokunin/CORPUS.md`, `registration.md`,
  `quality/counters/c2-r41-focus-entry.py`, the nine `fetch/` receipts, the two entry drafts, sibling seat
  reports (`ScoutPackageFocus/survey.md`, `ScoutHeldOverlap/overlap.md`), `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md`.
- No git/jj command of any kind; no pacman; no journal verb; no Wayland/compositor/portal connection; no
  counter run against the lane. No tool installed (nothing was needed).

## Findings for the L1

1. **Held rows cost a round-41 receipt.** Clause d applies to every cited id. `round-41/fetch/` holds nine
   files, none for S037/S041/S043/S052/S162/S031, so citing a held id needs a new distinct receipt under
   `round-41/fetch/` plus a `GATE` line. A meets this with `xdph-installed-version.txt` (1442 B, sha256
   `4294737a…`, a read-only `/var/lib/pacman/local/xdg-desktop-portal-hyprland-1.4.1-2/desc` capture) and
   cites S037 only; B and C cite no held id (B states S041 as prose only, which clause c does not count).
   The used-by table in `rows.md` is applied for S037 if A wins and otherwise not applied.
   Caveat: that receipt grounds the installed package record (`1.4.1-2`), not S037's
   `releases/tag/v1.4.1` anchor; S037's cells 1–10 stay byte-equal to BASE either way.
2. **S290 is cited only by B.** If A or C is selected, the L1 must drop S290 from the block or land it as
   `status queued` with `used-by —` (contract: `mined` = cited by ≥1 path); a `mined` S290 naming an entry
   that does not cite it would be a false registry claim.
3. **S287 honesty.** The issue is `CLOSED`/`COMPLETED` with `createdAt 2022-08-23T14:03:55Z` and
   maintainer replies dated 2022-08-25; the page has no `closedAt` field, so the row asserts no closure
   date. Its teaches states the *expected* behaviour and that the report shows focus was still taken — not
   that `silent` guarantees focus suppression on 0.56.2.
4. **S286 scope.** "None of the nine binds is the focus-grab manager" is an absence observed in
   `PortalManager.cpp` at v1.4.1 (`grep -ci` = 0), not a claim about other xdph files.
5. **S285 is B by choice**: one third-party client's source, quickshell is not installed on this host.
6. **Two extra candidate rows are out of the assigned set**: `fetch/Hyprland-FocusGrab.hpp` (unused
   receipt, 2607 B) and a `FocusState.cpp` row (not in `fetch/`). If the selected entry cites them they
   need S291/S292 plus a receipt each.

## Artifact paths

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w1/ScrRowsDraft/rows.md`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w1/ScrRowsDraft/rows-block.txt`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w1/ScrRowsDraft.md`
