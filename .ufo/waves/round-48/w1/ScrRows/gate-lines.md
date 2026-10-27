# Gate lines for S340–S347 (C2, round 48 w1 BUILD) — seat `ScrRows`

Access date 2026-10-26 for every line. Every quote is at most 25 words, is a word-bounded substring of a committed receipt, and its locator is
computed — never typed — by `quote-check.py` on the whitespace-collapsed receipt lines: `quote-check.txt` reads
`QUOTE_CHECK: checked=8 failed=0` (one line per row below). Pins live next to this file under `fetch/`; each row's sha256 is the sha256 of that
pin, and the host paths named in S340, S346 and S347 were copied byte-for-byte into `fetch/` (`host-rules-evdev`,
`host-xkbcli-compile-keymap.1` decompressed, `host-xkbcommon.h`).

- GATE S340 admit, tier A, code — `/usr/share/xkeyboard-config-2/rules/evdev` (xkeyboard-config 2.48-1), pin `fetch/host-rules-evdev` sha256
  0cc48ee1…, the 2.48 tag ships rules/rules.in plus a generator, so this installed file is the 2.48-1 build product; quote `* * = pc+%l%(v)` (host-rules-evdev:175) — the generic symbols row an
  unmatched layout still reaches, so a bad layout name survives the rules step.
- GATE S341 admit, tier A, code — https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config/-/raw/xkeyboard-config-2.48/symbols/br, pin
  `fetch/xkbc-symbols-br` sha256 8cf65550… (byte-equal to the installed file); quote `xkb_symbols "nativo" {` (xkbc-symbols-br:254) — one of
  eleven named blocks, of which `sun_type6` (:366) compiles while `rules/evdev.xml` never lists it as a `br` variant.
- GATE S342 admit, tier A, code — https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/context.c, pin
  `fetch/libxkbcommon-context.c` sha256 e6547abb…; quote `XDG_CONFIG_HOME fallback is $HOME/.config/` (libxkbcommon-context.c:263) — the user
  path precedes the legacy home path and the extra path, and the host receipt names the three paths it could not add.
- GATE S343 admit, tier A, code — https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/xkbcomp/rules.c, pin
  `fetch/libxkbcommon-rules.c` sha256 04dfd934…; quote `Unrecognized RMLVO option` (libxkbcommon-rules.c:2063) — the ignored-name diagnostic,
  emitted for model, layout, variant and option after the components are already stolen.
- GATE S344 admit, tier A, code — https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/xkbcomp/include.c, pin
  `fetch/libxkbcommon-include.c` sha256 95b5d8b5…; quote `Couldn't process include statement for '%s(%s)'` (libxkbcommon-include.c:501) — the
  fatal text an unknown variant produces, after the non-fatal missing-file warning at :353-357.
- GATE S345 admit, tier A, code — https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/messages-codes.h, pin
  `fetch/libxkbcommon-messages-codes.h` sha256 4e721d31…; quote `XKB_ERROR_CANNOT_RESOLVE_RMLVO = 595,` (libxkbcommon-messages-codes.h:150) —
  the registered id the host prints as `XKB-595`, shared by the ignored-option warning and the fatal rules-load error.
- GATE S346 admit, tier A, docs — `/usr/share/man/man1/xkbcli-compile-keymap.1.gz` (libxkbcommon 1.13.2-1), pin
  `fetch/host-xkbcli-compile-keymap.1` sha256 4da49c8a… (decompressed roff); quote `If an include path is given, the default include path list is
  not used.` (host-xkbcli-compile-keymap.1:50) — caller order replaces the defaults, and `--test` (:30) is the flag that makes the receipt
  read-only.
- GATE S347 admit, tier A, docs — `/usr/include/xkbcommon/xkbcommon.h` (libxkbcommon 1.13.2-1), pin `fetch/host-xkbcommon.h` sha256
  17e58db5…; quote `A comma separated list of variants, one per layout` (host-xkbcommon.h:462) — the normative alignment the `br,us` with `,intl`
  receipt shows as `br+us(intl):2`.

## Rejected candidates

Each was opened on 2026-10-26; the receipts are `receipts/rejected-candidates.txt` (URL, HTTP status, byte count, sha256 of the fetched body,
the counts quoted) and the bodies stayed in scratch, so the counts are the citable record.

- REJECT https://wiki.archlinux.org/title/Xorg/Keyboard_configuration — a community wiki page last edited 2026-10-06 with **zero** occurrences of
  `xkbcommon`, `XDG_CONFIG_HOME/xkb` or `XKB-595`, eleven of `xkeyboard-config` and three deferrals to `xkeyboard-config(7)`. It restates the
  data files this round opened directly and pins no package version, so it cannot ground a claim about this host's 1.13.2/2.48 pair. **Flip:** the
  page states an include-order or compile-outcome fact the shipped files do not, at a pinned page revision.

- REJECT https://xkbcommon.org/doc/current/index.html — opened, 20500 B, project number 1.13.2, so the version is right; but the index carries
  **zero** occurrences of `rmlvo`, `include path` or `XKB-NNN` and links only `doxygen_crawl.html` and `md_doc_2quick-guide.html`. Scope-empty for
  this entry: the include order, the "ignored" diagnostics and the message ids sit in `src/context.c`, `src/xkbcomp/rules.c` and
  `src/messages-codes.h`, which are already admitted. **Flip:** a page of that doc set (or a `doc/`-sourced page of the tag) states RMLVO
  resolution, the default include order or the message ids in a form the shipped header and sources do not.

- REJECT a ninth row for Hyprland's keymap compile (`src/devices/IKeyboard.cpp`) — the compile-adjacent Hyprland surface is held: `S319` already
  carries the file, and the held entry records the fallback (`corpus/knowledge/hyprland-input-devices-r46.md:33` step 4 and the `S319` observation
  at `:43`, pin `.ufo/waves/round-46/fetch/Hyprland-IKeyboard.cpp:113`, recomputed: `m_currentRules.layout  = "us";`). A new row on the same file
  and scope reads as a duplicate (census E04). **Flip:** a Hyprland-side compile fact the held rows do not carry — for example a release where the
  after-failure fallback changes.

## Held material this draft cites and never re-claims

- The `us` fallback after a keymap that does not compile: held entry step 4 (`corpus/knowledge/hyprland-input-devices-r46.md:33`) and `S319`
  (`:43`), pin `Hyprland-IKeyboard.cpp:113`. This round adds only what the compile itself does; it does not restate the fallback as new.
- The five stored names and their defaults: rows `S316`–`S318` (`corpus/SOURCES.md:265-267`), unchanged.
- The open ground this entry closes was recorded at `corpus/knowledge/hyprland-input-devices-r46.md:69` ("The XKB compile itself is not
  reproduced") and `corpus/README.md:112`; the registry itself stays the integrator's to edit, so nothing here rewrites either line.

## Live read-only receipt (supports the entries, no new row needed)

`receipts/*.rc`, `*.out`, `*.err` — `xkbcli compile-keymap` only (`--test`, `--kccgst`, `--rmlvo`, `--verbose`), stdout/stderr only, no
compositor verb and no `interactive-*`; the host's own names are `kb_layout = br`, `kb_options = compose:caps`
(`receipts/host-source-reads.txt`, `/home/vgpnk/.config/hypr/input.conf:10-11`). Observed outcomes, each from its `.rc`/`.out`/`.err` triple; `test-*` receipts use the full compile (`--test`), `kccgst-*` receipts use `--kccgst` only, and the pair is what shows that stage skipping the symbols compile:

- host names: rc 0; `--rmlvo` prints `rules: "evdev"`, `model: "pc105"`, `layout: "br"`, `variant: ""`, `options: "compose:caps"`; `--kccgst`
  prints `pc+br+inet(evdev)+compose(caps)`.
- `--layout zz`: rc 1, `[XKB-338] Couldn't find file "symbols/zz" in include paths`, then `[XKB-661] Couldn't process include statement for 'zz'`.
- `--layout br --variant nope`: rc 1, `[XKB-661] Couldn't process include statement for 'br(nope)'`.
- `--layout br --options nope:nope`: rc 0 with `[XKB-595] Unrecognized RMLVO option "nope:nope" was ignored`, symbols drops the option.
- `--layout br --model nope`: rc 0, geometry falls from `pc(pc105)` to `pc(pc104)`.
- `--rules nope --layout br`: rc 1, `[XKB-338] Couldn't find file "rules/nope"`, `[XKB-595] Cannot load XKB rules "nope"`.
- `--layout br,us --variant ,intl`: rc 0, `pc+br+us(intl):2`; `--layout br,us --variant nativo`: rc 0, `pc+br(nativo)+us:2` — variants are
  positionally aligned.
- `--layout br,us --variant nativo,nodeadkeys`: rc 1 on `us(nodeadkeys)` — `br(nativo)` resolved, the second index did not.
- `--layout br --variant sun_type6`: rc 0 (not in the XML registry); `--variant abnt2`, `--variant nativo-epo`: rc 0.
- `--verbose --kccgst --layout br`: rc 0, `receipts/verbose-include-paths.err` prints `Include path failed: "/home/vgpnk/.config/xkb"`, then
  `"/home/vgpnk/.xkb"`, then `"/etc/xkb"`, then the two extensions paths, and last `Include path added: /usr/share/xkeyboard-config-2` — the
  order `src/context.c:243-290` constructs, with the root appended after the extras branch.
