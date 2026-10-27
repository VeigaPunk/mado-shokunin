# ScrRows — C2 SOURCES rows S340..S347 and their Gate lines (round 48, w1 BUILD)

Status: COMPLETE. Seat `ScrRows`, leaf member, lane `mado-shokunin` at base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`.
Nothing was integrated: the L1 is the only integrator; this seat drafted rows, gates and rejections for the C2 entry
`corpus/knowledge/xkb-keymap-compile-r48.md` and edited no corpus file.

## Behavior

1. Opened the sources the C2 entry needs, before drafting anything (all 2026-10-26, read-only):
   - libxkbcommon 1.13.2 at tag `xkbcommon-1.13.2` (annotated tag `322bf223710e9d3a646dd345896eb4e7a83f8c41`, peeled commit
     `d1442aaa6b635551182e83c3b55037f4c118c962`): `src/context.c`, `src/xkbcomp/rules.c`, `src/xkbcomp/include.c`,
     `src/rmlvo.c`, `src/messages-codes.h`, `meson.build`.
   - xkeyboard-config 2.48: `symbols/br` at tag `xkeyboard-config-2.48` (commit `cf8d1151bb4c9ef5b895828d0e6dd7860c0833e0`,
     2026-06-21) — byte-equal to the installed `/usr/share/xkeyboard-config-2/symbols/br`; the installed `rules/evdev`
     (xkeyboard-config 2.48-1) and `rules/evdev.xml`; the tag's `rules/rules.in` and the `rules/generator` tree listing.
   - Host interface docs: `/usr/include/xkbcommon/xkbcommon.h` and `/usr/share/man/man1/xkbcli-compile-keymap.1.gz`
     (both libxkbcommon 1.13.2-1).
   - Hyprland was **not** reopened as a new source: the compile-adjacent file is held (`S319`,
     `.ufo/waves/round-46/fetch/Hyprland-IKeyboard.cpp:113`, recomputed) and is cited, not re-claimed.
2. Drafted eight registry rows **S340–S347** in the 11-column format, `status mined`, `opened 2026-10-26`,
   `recheck on-release`, `used-by corpus/knowledge/xkb-keymap-compile-r48.md`, no `|` inside any cell.
3. Drafted one Gate line per row (URL or host path, access date, ≤25-word quote, computed locator), three rejected
   candidates with reason + flip condition, and the duplicate screen.
4. Ran the live read-only receipt (`xkbcli compile-keymap`, only `--test` / `--kccgst` / `--rmlvo` / `--verbose`; no
   compositor verb, no `interactive-*`, no terminal, no process other than `xkbcli`, `curl`, `grep`, `sha256sum`) for the
   host's names `kb_layout = br`, `kb_options = compose:caps` and for the failure cases the entry must teach.

## Gates (ran, observed)

- `quote-check.py` → `quote-check.txt`: `QUOTE_CHECK: checked=8 failed=0` — every Gate quote is a word-bounded substring
  of a committed receipt, exactly one occurrence, ≤25 words, locator computed on the whitespace-collapsed line.
  S340→`host-rules-evdev:175`, S341→`xkbc-symbols-br:254`, S342→`libxkbcommon-context.c:263`,
  S343→`libxkbcommon-rules.c:2063`, S344→`libxkbcommon-include.c:501`, S345→`libxkbcommon-messages-codes.h:150`,
  S346→`host-xkbcli-compile-keymap.1:50`, S347→`host-xkbcommon.h:462`.
- `row-check.py` → `row-check.txt`: `ROW_CHECK: rows=8 gates=8 rejects=3 failed=0` — 11 cells per row, no empty cell,
  single-space padding, declared status/opened/recheck/used-by, ids S340–S347 in order, **registry still 276 rows, max
  S339, none of S340–S347 taken**, all eight quoted sha256 prefixes resolve to the committed pins, every `fetch/` path
  named in either draft exists.

## Substantive findings the rows carry (each backed by a receipt in `receipts/`)

- **Rules produce components, they do not validate.** An unknown layout still maps through `* * = pc+%l%(v)`
  (`rules/evdev:175`), so `--layout zz` fails later as a missing file: rc 1, `[XKB-338] Couldn't find file "symbols/zz"`,
  then `[XKB-661] Couldn't process include statement for 'zz'`. An unknown variant fails as
  `[XKB-661] … 'br(nope)'`, rc 1.
- **Unknown option and unknown model are non-fatal.** `--options nope:nope` → rc 0 with
  `[XKB-595] Unrecognized RMLVO option "nope:nope" was ignored` and the option dropped from symbols; `--model nope` → rc 0
  and the geometry falls from `pc(pc105)` to the generic `pc(pc104)` row (`rules/evdev:107`). Unknown **rules** is fatal:
  `[XKB-338] Couldn't find file "rules/nope"` + `[XKB-595] Cannot load XKB rules "nope"`, rc 1.
- **The XML registry is not the compile gate.** `symbols/br` defines eleven blocks; `rules/evdev.xml` declares eight `br`
  variants (no `abnt2`, `olpc`, `sun_type6`). `--variant sun_type6` compiles rc 0 although unlisted.
- **Variants are positionally aligned.** `--layout br,us --variant ,intl` → `pc+br+us(intl):2`;
  `--variant nativo` → `pc+br(nativo)+us:2`; `--variant nativo,nodeadkeys` fails on the second index (`us(nodeadkeys)`),
  matching `rules.c:985-1036` and the header's "one per layout" statement (`xkbcommon.h:462`).
- **Include order, measured and sourced.** `--verbose` prints the three failed user paths
  (`~/.config/xkb`, `~/.xkb`, `/etc/xkb`), two extensions paths, then `Include path added: /usr/share/xkeyboard-config-2` —
  the order `context.c:243-290` builds; `/usr/share/X11/xkb` is a symlink to the versioned root, which `context.c:330-340`
  explains as the post-2.45 split.
- **`--kccgst` is not a compile.** Under `--kccgst` the bad-layout and bad-variant cases return rc 0 (receipts
  `kccgst-*`); the same names under `--test` return rc 1 (`test-*`). The C2 entry must not cite a `--kccgst` rc as a
  compile verdict — this trap is recorded in S346's `teaches`.
- **Message ids are registered numbers** (`messages-codes.h:150` → 595), and one id carries both a warning and a fatal
  message; `XKB-338` is `INCLUDED_FILE_NOT_FOUND` (:116), `XKB-661` is `INVALID_INCLUDED_FILE` (:162).

## Duplicate screen (census W04/E04)

`grep -F` over `corpus/SOURCES.md` (276 rows): `xkbcommon` → 1 hit, S008 line 20, prose in the `teaches` cell, not a URL;
`xkeyboard-config`, `/usr/include/xkbcommon`, `xkbcli`, `rules/evdev`, `symbols/br` → 0 hits. **0 W04, 0 E04.** S316/S319
mention XKB names but are Hyprland source rows on other URLs.

## Touched surfaces

Created (this seat only, `mado-shokunin/.ufo/waves/round-48/w1/ScrRows/`, 612 KB total):
`rows.md`, `gate-lines.md`, `quote-check.py`, `quote-check.txt`, `row-check.py`, `row-check.txt`,
`fetch/` (11 pins, each ≤ 88 KB), `receipts/` (host compile triples, host source reads, rejected-candidate screen).
Report file: `.ufo/waves/round-48/w1/ScrRows.md` (this file).

Not touched: `corpus/SOURCES.md`, `corpus/README.md`, any knowledge/lesson file, `tools/`, `quality/`, `MANIFEST.json`,
`.ufo/state/`, the lane or fleet git/jj index, `~/.local/bin`, host config trees. No package transaction, no install, no
compositor command, no `xdg-terminal-exec` run, no terminal launch. Scratch `/fast/scratch/hyaku/mado-r48/ScrRows`
removed at the end; the rejected-candidate HTTP bodies stayed there, and only their URL/status/sha256/counts receipt is
kept (`receipts/rejected-candidates.txt`).

## Out of scope / open items handed to the L1

- **Id reservation.** S340–S347 are consumed here. If the C2 executor lands its own own-work receipt row for the live
  compile bundle, it must take **S348**; the eight rows already carry the pins and the host-byte receipts.
- **Used-by cell** names the entry as declared in the round-48 claims; if the entry is renamed, only that cell changes.
- **`src/rmlvo.c`** (sha256 `bc510290…`) was opened as corroboration of the layout/variant builder and is deliberately not
  a row; it stays in `fetch/` if the L1 wants a ninth row.
- **Provenance caveat recorded, not hidden:** `rules/evdev` has no file at the 2.48 tag (HTTP 404 at
  `…/raw/xkeyboard-config-2.48/rules/evdev`); the tag ships `rules/rules.in` (sha256 `16389776…`) plus a Python
  generator, so the installed 31520 B file is the 2.48-1 build product. S340's anchor states this rather than claiming
  tag-byte equality; `symbols/br` **is** byte-equal to its tag file.
- **Held material** cited only: the `us` fallback after a failed compile (entry step 4 at
  `corpus/knowledge/hyprland-input-devices-r46.md:33`, S319 observation at `:43`, pin `IKeyboard.cpp:113`), and the open
  ground closed by this entry (`hyprland-input-devices-r46.md:69`, `corpus/README.md:112`). No row restates either.
- **Not verified by this seat:** that the C2 knowledge entry text will in fact cite every row (the executor writes it), and
  the Hyprland-side claim mapping beyond what the held rows already state.
