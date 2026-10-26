# Rows draft — S298-S301 + held S164 used-by (round 44, w1, seat ScrRowsDraft)

Machine copy for the integrator: `rows-block.txt` (five table lines, nothing else matters).
This file explains each cell, the evidence behind it, and what the integrator must not change.

## Provenance

Opened 2026-10-26. All four documents were re-fetched from their canonical URLs in this seat and
compared with the frozen pins (`.ufo/waves/round-44/receipts/fetch-sha256.txt`):
receipt `fetch-recheck.txt` — four `HTTP 200 MATCH pin` lines (XDGShell.cpp `d90b534c…` 35458 B,
xdg-shell.xml `7ba7f9c8…` 63846 B, gdktoplevel-wayland.c `0ee38458…` 97548 B, gkeep-ui.py
`07a3c4a5…` 14639 B). No row cites a URL that already occurs in the registry
(`grep -n` for each of `src/protocols/XDGShell.cpp`, `xdg-shell/xdg-shell.xml`,
`gdktoplevel-wayland.c`, `VeigaPunk/gkeep/133b867…/gkeep/ui.py` in `corpus/SOURCES.md`: no match),
and the census validator reports no E04 for the appended registry (`validate-with-entry.txt`).

## The four new rows

| id | document | kind/tier | anchor (all locators computed, each echoed by `check-anchors.out`) | teaches |
|---|---|---|---|---|
| S298 | Hyprland `efb5099` `src/protocols/XDGShell.cpp` | code / A | `:354-358` setSize stores pending size; `:443-461` scheduleStateApplication; `:455` one sendConfigure; `:601-606` ack hook drops a serial below the previous; `:629-638` scheduleConfigure mints the serial; `:640-643` configure sends | A compositor size is held pending and sent on a later event-loop turn through a scheduled serial |
| S299 | wayland-protocols 1.49 `stable/xdg-shell/xdg-shell.xml` | spec / A | `:560-596` ack_configure; `:598-618` xdg_surface.configure (may discard all but the last); `:1144-1172` xdg_toplevel.configure; `:1166-1167` clients must ack; both interfaces version 7 (`:409`, `:622`) | The configure width and height are a hint; zero leaves the dimension to the client |
| S300 | GTK 4.24.1 `gdk/wayland/gdktoplevel-wayland.c` | code / A | `:606-616` handler; `:633-642` fixed_size (maximized, fullscreen, tiled, resizing); `:644-647` pending size, zero as saved_size; `:656-660` restore after maximize/fullscreen; `:662-683` next_layout size with size_is_fixed; `:382-441` update_size | The client stores the configure size and marks it fixed when the states include maximized, fullscreen or tiled |
| S301 | gkeep `133b867` `gkeep/ui.py` (full file, kind code, tier A, location = the raw GitHub URL) | code / A | `:446` GkeepApp; `:449` application_id; `:472-479` do_activate's single ApplicationWindow; `:475` undecorated; `:476` set_default_size(420, 500); `set_size_request(` occurs 0 times in 488 lines | The app states one default size and calls `set_size_request` nowhere |

Wording discipline (round-43 w2 finding: cells echoing a refuted premise): no cell claims a rule,
a compositor box, or a reported size. S298 says what the compositor code stores and when it sends;
S299 says what the protocol words mean; S300 says what GTK does with a configure; S301 says what
the client declares. None of them says which value produced a size a window reports — that is the
C2 entry's job to assemble, and S297 already carries the "cannot say which of the two" caution.

Receipt names (clause d/e of `PRED-C2-r44`): `.ufo/waves/round-44/fetch/Hyprland-XDGShell.cpp`,
`xdg-shell.xml`, `gdktoplevel-wayland.c`, `gkeep-ui.py`. Containment check (clause e) per row:
`xdgshell.cpp` ⊂ `hyprland-xdgshell.cpp`; `xdg-shell.xml` = `xdg-shell.xml`;
`gdktoplevel-wayland.c` = `gdktoplevel-wayland.c`; `ui.py` ⊂ `gkeep-ui.py` — four PASS lines in
`check-anchors.out`. S301 deliberately uses the full-file receipt, not S297's
`gkeep-ui-excerpt.py`, so the two rows keep distinct receipts (clause d: no two ids share a path).

Status/recheck: `mined` for all four (each is cited by `used-by` below, in the entry the C2 seat
writes). Recheck `on-release` for the three version-pinned upstream documents; `2027-01-24` for the
gkeep raw-URL file, matching S297's cadence for the same document family.

## Held row S164

Only cell 11 changes: `corpus/knowledge/rule-attribution-r24.md` →
`corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/hyprland-gkeep-size-request-r44.md`.
Cells 1-9 verified **byte-equal** to registry line 176 by field-wise awk split of both rows with
`\036` separators and sha256 of the two strings (`s164-cells.txt`: both
`250884ba859b13956954e48801ff831568f69649dfcde4535c038182a0269afa`, 658 B each,
`VERDICT BYTE-EQUAL`). Cell 11 is the append-only cell the contract allows to change; `opened` and
`recheck` stay as they are (`2026-10-23`, `on-release`).

## Validation (mirror, scratch; counter contract untouched)

Mirror = `cp -a` of the lane `corpus/` plus symlinks `tools .ufo quality SKILL.md` to the lane
(needed because many base rows cite those paths), and the four new rows **inserted from
`rows-block.txt` itself** plus the S164 line taken from the same file, so the validated bytes are
the delivered bytes: `roundtrip.txt` reads both back out of the mirror registry and compares —
`S298-S301 rows read back vs rows-block.txt lines 1-4: MATCH`, `S164 row read back vs
rows-block.txt line 5: MATCH`.

- `validate-base.txt` — pristine registry, exit 0, `file ok`, 8 W codes (W04×7, W01×1).
- `validate-no-entry.txt` — my rows, entry absent, exit 1: exactly five E11 lines
  (S164, S298, S299, S300, S301 each `missing used-by corpus/knowledge/hyprland-gkeep-size-request-r44.md`),
  the same 8 W codes, no other E.
- `validate-with-entry.txt` — my rows plus a three-line placeholder entry
  (`source: placeholder for E11 resolution only …`; the real entry is the C2 seat's deliverable),
  exit 0, `file ok`, the same 8 W codes. **The placeholder exists only in the scratch mirror**; no
  file was written under the lane's `corpus/knowledge/`.
- `census-mirror.txt` — frozen CORPUS.md census on the mirror: rows 238 (234 + 4), malformed 0,
  duplicate ids none, enum/tier violations none, status histogram mined=219 queued=10 rejected=9.
- The mirror paths in those receipts are scratch and were deleted after the receipts were copied;
  the registry bytes they describe are reproducible from `rows-block.txt` (round-trip above).

## Locator verifier

`check-anchors.sh` (seat dir) re-derives every anchor and has three parts: 40 `file:line` needle
checks plus one count check (`set_size_request(` = 0), a cited-locator section (every token of the
form `file:N` or `:N-M` in a new row's anchor cell must be inside the file's line count, and its
first line number must be one of the needle-checked lines), and the clause-e containment check.
`check-anchors.out`: 49 PASS (41 needle-class + 4 sha256/bytes + 4 containment) and 1 SKIP for the
held row, 21 ECHO lines (each cited line printed verbatim), `SUMMARY failures=0`.
`check-anchors-red.out`: two mutants of `rows-block.txt` (locator `476`→`477`; location
`gkeep/ui.py`→`gkeep/main.py`) each exit 1 with `SUMMARY failures=1`, so the verifier is shown able
to fail; an unreadable rows block exits 2 with `SETUP FAIL …` instead of scoring zero failures.
The verifier keeps its one temp file in the seat dir and removes it on exit; it needs no scratch dir
(an earlier revision used `mktemp` under `/fast/scratch/…` and turned vacuous once that dir was
deleted — the setup guard exists because of that).

## Handoff constraints for the integrator and the C2 seat

1. Append the four rows after S297; ids S298-S301 are provisional. They are absent at BASE
   `6a1a905` and at the freeze `e228951` (both registries: 234 rows, max id S297), so any
   renumbering at the data commit must be by document and must keep each row's receipt name
   (clause e containment) and its pinned sha256.
2. The C2 entry must cite S298-S301 **and** held S164; `corpus/lessons/round-44.md` § Gate needs
   one `GATE <id> receipt=… sha256=… quote="…"` line per cited id, quotes 3-25 words, occurring
   once at word boundaries in the normalized receipt and in no other cited receipt.
3. `PRED-C2-r44` clause h census lines, cross-checked against the pins by this seat (not scored
   here): `gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep`
   (gkeep-ui.py `:476`, `:449`, `set_size_request(` count 0) and
   `hyprland sendWindowSize xdg_setSize=1 x11_configure=1` (Window.cpp body `:1732-1754` — the first
   line that is exactly `}` is 1754; `->setSize(` once at `:1753`, `->configure(` once at `:1751`).
4. Do not touch S290-S294 (frozen round-43 rows) and do not reuse S297's excerpt receipt for S301.

## Known limits

- The six "teaches" cells are the non-author reading of the pinned bytes; the counter cannot check
  that a true locator supports its sentence (declared residual of `PRED-C2-r44`).
- S300's anchor cites six range boundaries (`:616`, `:647`, `:660`, `:683`, `:642`, `:441`) that are
  range ends, not needles; the verifier checks them for existence only. S299's `:596`, `:618`,
  `:1172` and S298's `:358`, `:461`, `:606`, `:638`, `:643` are the same kind of end.
- The mirror's exit 0 depends on a placeholder entry; with the entry absent the validator reports
  exactly the five expected E11 lines and nothing else.
