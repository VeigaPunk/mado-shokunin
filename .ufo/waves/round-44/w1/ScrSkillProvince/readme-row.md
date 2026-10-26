# corpus/README.md — index row + Frontier advance (round 44)

Target: `corpus/README.md` (301 lines at base `6a1a905`). Coverage-map table rows run to `:71`
(`hyprland-gkeep-geometry-r43.md`); blank `:72`; `## Quality bar` `:73`; `## Frontier` `:250`;
last line `:301` (end of the Round-43 route section).

Ids: `S164` is held (`Hyprland-Window.cpp`); `S297` is held (`gkeep/ui.py` lines 446-488 excerpt) and is
**not** cited here — the full-file pin supersedes it. `S298`-`S301` are the four provisional new ids for
the round-44 pins (`Hyprland-XDGShell.cpp`, `xdg-shell.xml`, `gdktoplevel-wayland.c`, `gkeep-ui.py`),
appended to `corpus/SOURCES.md` at the data commit by the L1. The row cites exactly the five ids the
C2 counter's clause i+ requires the entry to cite (all five PINS).

---

## 1. Coverage-map index row — insert after `corpus/README.md:71`

Becomes new line **72** (blank `:72` → `:73`, `## Quality bar` → `:74`). One physical line, column 0:

```
| `knowledge/hyprland-gkeep-size-request-r44.md` (MADO-R44-1, round 44; assimilation of the gkeep-theme residue, successor path to the held excerpt S297) | What happens after Hyprland sets the gkeep window's box: the compositor takes the real box and reports it (`CWindow::sendWindowSize` calls `realToReportSize`, `Hyprland-Window.cpp:1732` and `:1741`), hands it to the client as an xdg toplevel configure (`setSize` stores the pending size and calls `scheduleConfigure`, `Hyprland-XDGShell.cpp:354-357` and `:629-643`) or as an X11 configure (`Hyprland-Window.cpp:1751`), and queues the configure serial on its pending-size-ack list, cleared by `onAck` (`Hyprland-Window.cpp:1514-1521`); xdg-shell 1.49 calls the configure width and height "a hint to the window" that a client need only acknowledge (`xdg-shell.xml:1144-1165`, ack at `:1163`), GTK 4.24.1's Wayland toplevel applies the configured size through `gdk_wayland_toplevel_update_size` (`gdktoplevel-wayland.c:513-536`), and gkeep 133b867 declares `set_default_size(420, 500)` under `application_id="org.omarchy.gkeep"` with zero `set_size_request` calls (`gkeep-ui.py:449`, `:476`). No client was run and no socket was opened; the ack round-trip and the drawn size stay UNK. | S164, S298, S299, S300, S301 |
```

Cell notes (what the gate reads):

- Cell 1 names the note by its `knowledge/…` path — the completeness gate's fence key.
- Cell 2 is non-empty and states only what the pins show; every locator is a `grep -n` line number of the
  pinned file, not a recollection.
- Cell 3 carries the five ids in ascending order and no backticked path (so `cited-path-missing` has
  nothing to resolve). All five must exist in `corpus/SOURCES.md` at the scored revision or the row is
  `ERROR cited-s-undefined`.
- `holds-no-overlap` is a WARN, not an error: it fires only if cell 2 shares no five-word run with the
  note's own bytes. The cell was written from the same pins the entry must cite
  (`sendWindowSize`, `realToReportSize`, `scheduleConfigure`, `pending-size-ack`, `onAck`,
  `set_default_size(420, 500)`, `set_size_request`), so the entry is expected to overlap; the final check
  belongs to whoever lands the entry, on the landed bytes.

---

## 2. Frontier advance — append at end of file, after `corpus/README.md:301`

```
### Round-44 gkeep size-request route

- Advances the Round-43 route's open item "the client's acknowledgement path" onto sourced ground, and
  corrects one of its verdicts. What the compositor does after it sets the box:
  `CWindow::sendWindowSize` reports the real size (`realToReportSize`, `Hyprland-Window.cpp:1732,1741`)
  and hands it to the client as an xdg toplevel configure (`setSize` → `scheduleConfigure`,
  `Hyprland-XDGShell.cpp:354-357,629-643`) or as an X11 configure (`Hyprland-Window.cpp:1751`), queueing
  the serial for `onAck` (`Hyprland-Window.cpp:1514-1521`); the configure is "a hint to the window" that
  the client must acknowledge but need not follow (`xdg-shell.xml:1144-1165`); GTK 4.24.1's Wayland
  toplevel applies it as its own size (`gdktoplevel-wayland.c:513-536`); and gkeep 133b867 declares
  `set_default_size(420, 500)` and never calls `set_size_request` ([size request](knowledge/hyprland-gkeep-size-request-r44.md),
  rows S164 plus S298-S301). The same round moves the tool's vocabulary: `tools/mado-geometry.py` now
  prints FULLSCREEN and MAXIMIZED for a client whose `fullscreen` field is 2 or 1 instead of reporting the
  monitor box or the work area as a difference, and TILED is narrowed to "not floating" — a pseudo-tiled
  client takes its box from the stored pseudo size, which `clients -j` does not print. Still open: no live
  gkeep window was observed, no client was run and no socket was opened, so the ack round-trip, the
  pending-list ordering under a real client and the drawn size remain unmeasured.
```

The bullet is additive: the Round-43 section above keeps its wording, including its older verdict list
(AGREE / DIFFER / TILED / BADSIZE), which this section supersedes for the tool's current vocabulary.

---

## 3. Gate run (this seat, scratch clone)

Receipt: `.ufo/waves/round-44/w1/ScrSkillProvince/receipts/index-rows-gate.txt`. Fixture:
`git clone -q --shared <lane>` into `/fast/scratch/hyaku/mado-r44/ScrSkillProvince/gitfix2`
(toplevel-checked, base `ae996fcf…`), then the row above inserted after `:71`, the §2 Frontier block
appended, and provisional `corpus/SOURCES.md` rows for S298-S301 added — committed **in the fixture
only**; the lane's index was never touched.

| Run | Command (repo = fixture, rev = HEAD) | Result |
|---|---|---|
| baseline | `quality/check-index-rows.py` | `rows=60 errors=0 warns=3` (the 3 WARNs are pre-existing round-12/24 glob rows) |
| G1 | `check-index-rows.py` with the row, the Frontier block and the four provisional registry rows, note absent | `rows=61 errors=0 warns=3` |
| G2 | `check-index.py` (completeness), note absent | `indexed=60/60 missing=0 dangling=1 duplicates=0` → rc 1 — **the row is dangling until the entry lands** |
| G2b | `check-index.py`, note present (fixture stub) | `indexed=61/61 missing=0 dangling=0 duplicates=0` → rc 0 |
| G3 | `check-index-rows.py`, note present | `rows=61 errors=0 warns=3` — no `holds-no-overlap` for this row |
| C1 ctl | provisional S298-S301 rows deleted | `errors=4`, one `cited-s-undefined` per id → the ids are load-bearing |
| C2 ctl | Sources cell emptied | `ERROR row-cells: … at line 72 carries 3 cells (need 3 non-empty)` |
| C3 ctl | `tools/nope-r44.py` added to the Sources cell | `ERROR cited-path-missing: `tools/nope-r44.py`` |

Row text validated: sha256 `d70340393ef5d9f772a9c368c4ec6e49ed97a2da3fe2e6751e38f7389aa7317a`, 1,270 B,
3 cells. Landing order is forced: **row + entry in one commit**, and `corpus/SOURCES.md` rows for
S298-S301 before or with them.
