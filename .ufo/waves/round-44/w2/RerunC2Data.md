# RerunC2Data — C2 re-run and independent Gate re-derivation (round 44, w2)

Seat `w2/RerunC2Data`. Target: `quality/counters/c2-r44-gkeep-size-request-v2.py` (PRED-C2-r44-v2) at the data
commit `e46789213830597348fe96a351ae004d10587385`, base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`.
Status: **COMPLETE 2026-10-26**. Nothing outside this seat was written; the frozen counter, controls, registration,
reference, pins and lane index were not touched.

## 1. Re-run of the counting command (twice)

Exact command, run from `/home/vgpnk/Projects/shokunin/mado-shokunin`:

```
python3 -I quality/counters/c2-r44-gkeep-size-request-v2.py --repo . --rev e46789213830597348fe96a351ae004d10587385
```

- run 1: exit 0 — `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=1` (receipt `receipts/run1.txt`)
- run 2: exit 0 — byte-identical to run 1 (`diff -q` → no output), (receipt `receipts/run2.txt`)
- final line both runs: `PRED-C2-r44-v2: admitted=1/1 verdict=TARGET_MET rev=e46789213830597348fe96a351ae004d10587385`

This reproduces `receipts/c2-after-data.txt` (`admitted=1/1 TARGET_MET`). Determinism: the counter reads only
revision-addressed git objects and removes ambient `GIT_*`; two passes agree byte for byte.

## 2. Independent re-derivation (the counter is never imported)

Two scripts of my own in this seat, both reading only `git show` output:

- `rederive.py` — token-run collapse (not the counter's char-wise collapse), `(?<!\w)…(?!\w)` word boundaries,
  line-oriented comment stripping, own census scan, own twelve-surface scan.
- `rederive2.py` — registry cell arithmetic at REV vs BASE, header window, ghost tokens, README rows, Gate
  containment and quote distinctness.

Outputs: `receipts/rederive1.txt` and `receipts/rederive3.txt` are byte-identical (script re-run), plus
`receipts/rederive2.txt`.

### 2.1 Per cited id

Every value below is computed, not copied. "quote" = the GATE quote, normalized to single spaces;
"start line" = 1-based receipt line where its single word-bounded occurrence begins.

| id | GATE line (`corpus/lessons/round-44.md`) | receipt @ e467892 | sha256 = git blob | quote occurrences / start line | in any other cited receipt | entry line with quote + locator | registry row | location = pin URL | census role |
|----|------------------------------------------|-------------------|-------------------|-------------------------------|----------------------------|---------------------------------|--------------|--------------------|-------------|
| S164 | 31 | `.ufo/waves/round-44/fetch/Hyprland-Window.cpp` (124226 B) | yes, `d735d454…11ded` | 1 / **1687** | none | `corpus/knowledge/hyprland-gkeep-size-request-r44.md:28` (`Hyprland-Window.cpp:1687`) | `corpus/SOURCES.md:176`, 11 cells, `mined`, opened `2026-10-23`, recheck `on-release` | yes | Hyprland census input |
| S298 | 32 | `…/Hyprland-XDGShell.cpp` (35458 B) | yes, `d90b534c…7ed0c0` | 1 / **455** | none | entry:36 (`Hyprland-XDGShell.cpp:455`, plus `:354-358`) | `SOURCES.md:247`, new, 11 cells, `mined`, `2026-10-26`, `on-release` | yes | — |
| S299 | 33 | `…/xdg-shell.xml` (63846 B) | yes, `7ba7f9c8…c4c7df` | 1 / **1150** | none | entry:44 (`xdg-shell.xml:1150`) | `SOURCES.md:248`, new | yes | — |
| S300 | 34 | `…/gdktoplevel-wayland.c` (97548 B) | yes, `0ee38458…867fbe` | 1 / **681** | none | entry:48 (`gdktoplevel-wayland.c:681`) | `SOURCES.md:249`, new | yes | — |
| S301 | 35 | `…/gkeep-ui.py` (14639 B) | yes, `07a3c4a5…fe5d66a` | 1 / **475** (quote spans 475-476) | none | entry:56 (`gkeep-ui.py:475`) | `SOURCES.md:250`, new | yes | gkeep census input |

`git show REV:<receipt> | sha256sum` equals the GATE `sha256=` and `receipts/fetch-sha256.txt` for all five;
all five are mode `100644`. Locator receipts: `receipts/locators.txt` (produced with `grep -n`, never typed) and
`receipts/quote-verify.txt` (22/22 quoted strings and locators verified against the receipt copy).

### 2.2 Bindings cross-checked beyond the table

- **Gate section containment.** Exactly five `^GATE S` lines (31-35), all inside `## Gate`, none indented, none
  outside the section; no second GATE block.
- **Distinctness.** Five distinct receipt paths, five distinct sha256, five distinct quotes.
- **Header window (clause b).** Five `source:` lines on raw lines 3-7; `verified-at: 2026-10-26` line 8;
  `recheck: 90d` line 9; no `source:/verified-at:/recheck:` line after raw line 20; the entry's S-token set is
  exactly {S164, S298, S299, S300, S301} (no ghosts).
- **Registry (clause c).** S164 is the held row: base `SOURCES.md:176` and rev `SOURCES.md:176` agree byte for
  byte in cells 1-9, and the base used-by item is a subset of the rev used-by (1 → 2 items, entry added).
  S298-S301 have zero rows at base, one row each at rev, opened `2026-10-26`, and a URL location containing `/`
  and `.`. Each location occurs in exactly one row. For every cited id gated on a PINS receipt the location is
  exactly that pin's URL (`https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp`,
  `…/src/protocols/XDGShell.cpp`, `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/stable/xdg-shell/xdg-shell.xml`,
  `https://gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gdk/wayland/gdktoplevel-wayland.c`,
  `https://raw.githubusercontent.com/VeigaPunk/gkeep/133b86717a02548aeaff3f1411bf301d936c5308/gkeep/ui.py`).
  Anchor cells name their receipt with ranges inside the receipt's line count
  (`Hyprland-XDGShell.cpp:354-358`, `xdg-shell.xml:1144-1172`/`560-590`, `gdktoplevel-wayland.c:444-545`/`606-700`,
  `gkeep-ui.py:446-480`/`80-91`).
- **Census (clause h).** From `gkeep-ui.py` with `#` comments removed: one `set_default_size(420, 500)`, one
  `application_id="org.omarchy.gkeep"`, `set_size_request(` count 0 (also 0 in the raw bytes; `set_size_request`
  does not occur anywhere in the file). From `Hyprland-Window.cpp`, the `void CWindow::sendWindowSize(bool force) {`
  body is lines 1732-1754 (first following line equal to `}` is 1754) and holds `->setSize(` ×1 and
  `->configure(` ×1 (whole file 2 and 3, which is why function scope matters). The entry carries
  `gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep` once (raw line 58) and
  `hyprland sendWindowSize xdg_setSize=1 x11_configure=1` once (raw line 32); these are the only two raw lines
  starting with those prefixes, so the exact-line exemption is not a hiding channel on this entry.
- **Twelve clause-j surfaces.** Anchor line L in the pinned receipt, and the body citation (entry raw line) whose
  range covers L with the surface keyword on the same line:

  | surface | receipt | anchor L | cited range | entry line |
  |---------|---------|----------|-------------|------------|
  | report-size | Hyprland-Window.cpp | 1685 | 1685-1699 | 30 |
  | send | Hyprland-Window.cpp | 1732 | 1732 | 30 |
  | x11 | Hyprland-Window.cpp | 1751 | 1751 | 30 |
  | ack | Hyprland-Window.cpp | 1514 | 1514 | 38 |
  | setsize | Hyprland-XDGShell.cpp | 354 | 354-358 | 36 |
  | configure | Hyprland-XDGShell.cpp | 455 | 455 | 36 |
  | zero | xdg-shell.xml | 1154 | 1154-1157 | 44 |
  | ack_configure | xdg-shell.xml | 560 | 560 | 44 |
  | gtk-store | gdktoplevel-wayland.c | 681 | 681 | 48 |
  | gtk-constrain | gdktoplevel-wayland.c | 525 | 523-528 | 50 (also 74) |
  | gtk-0x0 | gdktoplevel-wayland.c | 647 | 647 | 50 |
  | gkeep-id | gkeep-ui.py | 449 | 449 | 56 |

  Every anchor occurs exactly once in its receipt; every L is ≥ 21 raw lines into the entry (outside the 20-line
  header) and unfenced. All twelve cited.
- **Decision table (clause i).** `ADMIT merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md` and
  four `REFUSE` lines (r13, r14, r15, r9) on distinct staged paths, each with a flip word; no `BAD_LOC` marker in
  the entry or in the five registry rows; the five Gate receipts cover all five PINS names.
- **README (clause f).** Exactly one column-0 index row for the entry, `corpus/README.md:72`.

## 3. Content spot-checks against the pinned bytes (falsification pass)

Each cited range in the entry was read at the rev and matched its sentence:

- entry:30 — realToReportSize at 1685-1699; X11 clamp at 1x1 is line 1691, the monitor-scale multiply 1694-1696;
  sendWindowSize's early return is 1743-1744; X11 configure 1751; the pending-ack append 1753
  (`setSize(REPORTSIZE)` serial + `REPORTSIZE.floor()`).
- entry:38 — onAck 1514, newest pair with `serial <= acked` 1515, drop-it-and-older 1521, acked-size write 1526.
- entry:44 — hint 1150, zero-size 1154-1157, states 1159-1161, `ack_configure` request 560.
- entry:48/50 — `fixed_size` 633-637; shadow-margin sum 518-521; constrain 523-528; widget-tree minimum
  (`GDK_HINT_MIN_SIZE`) 490-494; `saved_size = (width == 0 && height == 0)` 647; GTK-computed size 539-544.
- entry:56/60 — `window.set_decorated(False)` 475 and `set_default_size(420, 500)` 476; `application_id` 449;
  `min-height` 87 / `min-width` 88 inside the button rule only.

## 4. Disagreements between the counter and the independent derivation

**None.** Every number the counter printed was reproduced independently: quote start lines 1687 / 455 / 1150 /
681 / 475; the twelve surface anchors 1685, 1732, 1751, 1514, 354, 455, 1154, 560, 681, 525, 647, 449; census
`420x500`, `0`, `org.omarchy.gkeep`, `1`/`1`; registry statuses, opens and locations; clause f's single README row;
the ADMIT/REFUSE set.

## 5. OPEN predicate defect (one; latent, not exercised by this data)

**What it attacks:** clause d's own text, `quality/counters/c2-r44-gkeep-size-request-v2.py:32` —
"a new id's receipt must be one of" (the sentence continues with `PINS;` on :33).
**Severity: LOW.** **Classification: OPEN predicate defect** (code weaker than the frozen docstring); no
re-registration after data.

The per-id rule is not implemented. `pin_ok` at :489-491 accepts a basename absent from `PINS`
(`PINS.get(os.path.basename(path)) in (None, digest)`), and the only PINS guard is the collective coverage test at
:646 (`bad |= not set(PINS) <= used`). With the landed entry the gap is unreachable: five cited ids, five distinct
receipt paths and five pins, so coverage at :646 forces each receipt onto a pin — the rule holds by arithmetic.

**Reproduction (fixture, scratch clone, deleted after the copy).** A sixth cited id `S302` gated on an invented
`.ufo/waves/round-44/fetch/unpinned-receipt.txt` (sha256 `c0b4bb40b8ee0d8f98fdcd248b99ba4948b5bce98a75c6f51e52020b430bb66f`,
four readable lines), with all five real pins still cited by the five real ids, scores
`clause=d id=S302 gates=1 bound=1` and `admitted=1/1 verdict=TARGET_MET` at fixture commit
`84153f4b4094d55fda2072248f081d5f0d670483` (receipts `receipts/fixture-unpinned.txt`,
`receipts/fixture-diff.txt`, `receipts/fixture-diff-stat.txt`). Attacker capability needed: the ability to add a
sixth id plus a self-authored receipt under `fetch/`; the docstring says this must be rejected, the code admits it.
**Smallest correction (L1's call):** in the clause-d loop, require `os.path.basename(path) in PINS` for ids absent
from `reg_base` (or for every cited id), instead of relying on set coverage at :646.

## 6. Observations that are not disagreements

- Three of the five GATE quotes sit at the predicate's 3-word floor (`len(quote.split())` = 3 for S298, S300, S301;
  S164 = 4, S299 = 18). Each is a complete statement in the pinned bytes, so no binding fails, but the floor admits
  a three-token quote as "sourced".
- The census exemption in clause g is exact-line only; verified this entry has no other line sharing those prefixes,
  so the w1 F2 hiding channel stays closed here.
- `sendWindowSize`'s body bound depends on the first following line that is exactly `}` (1754 today); a column-0
  `}` inside the body would shrink it. No effect on the landed counters (X=Y=1).

## 7. Risks and blockers

No blocker. The re-run and every Gate binding reproduce the counter's verdict. The only open item is the latent
clause-d gap in §5, which the landed five-id data does not reach.

## 8. Evidence in this seat

| file | what it is |
|------|------------|
| `receipts/run1.txt`, `receipts/run2.txt` | the two counter runs (identical) |
| `receipts/rederive1.txt`, `receipts/rederive3.txt` | independent derivation, two passes (identical) |
| `receipts/rederive2.txt` | registry/base arithmetic, header window, README, Gate containment |
| `receipts/locators.txt` | every locator cited here, from `grep -n` / `sed -n` on the rev blobs |
| `receipts/fixture-unpinned.txt` | counter score of the sixth-id fixture (clause d bound, admitted 1/1) |
| `receipts/fixture-diff.txt`, `receipts/fixture-diff-stat.txt` | the fixture commit's diff |
| `receipts/quote-verify.txt` | 22/22 quoted strings and locators verified against the receipts |
| `rederive.py`, `rederive2.py`, `build_unpinned_fixture.py`, `verify_quotes.py` | the scripts that produced the above |

## 9. Tooling record

No tool installed or updated (python3 stdlib only). No pacman transaction, no host-service or compositor
mutation, no input injection, no Wayland connection. Scratch `/fast/scratch/hyaku/mado-r44/RerunC2Data`
(including the fixture clone) deleted at completion. Lane index untouched; writes confined to this seat dir.
