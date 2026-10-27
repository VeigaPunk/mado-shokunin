# RevC2Entry — w2 attack evidence (raw)

Seat scratch: /fast/scratch/hyaku/mado-r48/RevC2Entry (created explicitly; removed at end of wave; every writer shell ran `ulimit -f 2048`).
Largest output file: pins/xkbcommon-rules.c = 74,868 B (fetch copy); replay.keymap = 73,079 B. All files < 1 MiB; total scratch < 50 MB. No installs performed (pacman paused; none needed). All commands read-only vs lane and host; xkbcli used only with compile-keymap/--test/--kccgst verbs.

## A. Pin binding (attack: upstream re-fetch)
- Command: curl of raw.githubusercontent.com xkbcommon-1.13.2 tag AND commit d1442aaa6b635551182e83c3b55037f4c118c962 (8 files); gitlab.freedesktop.org xkeyboard-config-2.48 tag AND commit cf8d1151bb4c9ef5b895828d0e6dd7860c0833e0 (rules/rules.in, symbols/br, rules/meson.build); Hyprland efb50993780079460b0cbed1363e2166a2de1d9f src/devices/IKeyboard.cpp.
- Observed: every fetch byte-equal to the lane pin. shas: rules.c 04dfd934…, xkbcomp.c ae6823a8…, include.c 95b5d8b5…, context.c e6547abb…, context-priv.c c2ffff03…, meson_options.txt 496455ea…, compile-keymap.c 099664ce…, messages-codes.h 4e721d31…, rules.in 16389776…, symbols/br 8cf65550…, rules/meson.build 1b4ab1d4…, IKeyboard.cpp 8a800efe9baa7f375a3781744372eecd98a88be2c4bedaae96c90a1102a1aa3d. Tag fetch == commit fetch in all cases.
- Host byte-equality: cmp /usr/share/xkeyboard-config-2/rules/evdev vs pin, and symbols/br vs pin → equal.
- Pin sizes/lines vs rows-c2.md: all match (rules.c 74868 B 2125 lines; xkbcomp.c 7920/239; include.c 17209/510; context.c 16074/592; context-priv.c 5898/225; meson_options 2411/102; tools 23033/631; messages 9554/214; evdev 31520/747; br 19592/368; receipt 14270 B sha ab5fa971…).

## B. Locator check (attack: quote/range drift)
Every locator in the entry verified verbatim at the cited lines of the pinned bytes: rules.c 520-535 (log_warn "More layouts…":523-526 vs log_err "Less layouts…":529-532), 1259, 1297, 1986-1992, 1995-2025 (xkb_resolve_partial_rules at 1938-1973 traverses all include paths in order), 2028-2036, 2045-2064, 2063; xkbcomp.c 60-64, 157, 161; include.c 333, 353-358, 355, 498-506, 501; context.c 243-338 (order: xdg/user, $HOME/.xkb, extra, versioned-then-unversioned extension subdirs appended in add_direct_subdirectories:212, root :317-318, legacy fallback :330-336), 503; context-priv.c 129-160, 192-217, 207-208, 218-219 (`if (rmlvo->options == NULL)`); meson_options.txt 32-59 (evdev/pc105/us at 34/40/46), 44, 46; tools-compile-keymap.c 521, 585-587 (plus placeholder → xkb_context_include_path_append_default at :601); messages-codes.h 116 (=338), 150 (=595), 162 (=661), 178 (=769), 190 (=822); rules-evdev 55-59 (incl. $jollamodels/olpc/olpcm rows), 61-64, 86 ($pcmodels = pc(%m)), 107 (`* = pc(pc104)`), 109-175, 175, 529-586, 570; symbols-br 47 + 11 xkb_symbols maps (nope/caps absent); rules/meson.build 18-39.
- Option wildcards: zero `* =` lines in any `! option` section (starts 529/729/738) → entry step 7 "no wildcard" holds for all option sections.
- MAX_INCLUDE_DEPTH 5 (rules.c) → census `max_rules_include_depth=5` ✓.

## C. Held-row attribution (attack: NO_FLAGS / never-NULL)
- Pin .ufo/waves/round-46/fetch/Hyprland-IKeyboard.cpp: line 67-73 `xkb_rule_names XKBRULES = { .rules = rules.rules.c_str(), … }` (never NULL); line 75 `xkb_context_new(XKB_CONTEXT_NO_FLAGS)`; second context at :226 also NO_FLAGS; fallback reset :107-115 (memset + layout "us"). Entry step 1/step 8 attribution to S319 matches the pinned bytes.
- libxkbcommon side: context.c:505 `use_environment_names = !(flags & XKB_CONTEXT_NO_ENVIRONMENT_NAMES)` → NO_FLAGS context reads env. context-priv.c:202-217 empty layout → env default, variant discarded (log_warn :207, hidden at default); :218-219 options only replaced when NULL → Hyprland's "" kb_options stays "".

## D. Receipt replay (attack: receipt honesty)
- `xkbcli compile-keymap --layout br --options compose:caps` → rc 0, sha256 efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81, 2090 lines / 73079 bytes, stderr empty — equal to receipt.
- `--kccgst` host names → `pc+br+inet(evdev)+compose(caps)` / `pc(pc105)` ✓; `--kccgst` no names → `pc+us` ✓.
- `--test --layout zz` → rc 1, 10 XKB-338/661/769/822 lines with include-path census ✓; `--variant nope` → rc 1 XKB-661 `br(nope)` ✓; `--options nope:nope` → rc 0 + XKB-595 ✓; `--kccgst --model nope` → geometry `pc(pc104)`, silent ✓; `--layout br,us --variant ,dvorak` → `us(dvorak):2` ✓.
- `--kccgst --layout br --variant nodeadkeys,intl` at DEFAULT log level → `xkbcommon: ERROR: Less layouts than variants: "br" vs. "nodeadkeys,intl".` rc 0 (basis of finding M1).
- Precedence probe replay: XDG_CONFIG_HOME=scratch/xdg with symbols/mado48 → rc 0.

## E. Ground / base checks
- r46 entry :69 contains "The XKB compile itself is not reproduced…" ✓; :33 is step 4 ✓; base corpus/README.md:112 contains "Still open: the XKB compile itself" ✓.
- base git show: corpus/knowledge/xkb-keymap-compile-r48.md absent ✓; SOURCES.md has zero S34x rows ✓; README anchor row `knowledge/xdg-terminal-selection-r47.md` present ✓.
- Working tree copy of the entry is byte-equal to l1-draft/xkb-keymap-compile-r48.md (diff -q clean); S346 row carries evdev pin sha 0cc48ee1279d… matching the pin.
- Entry "verified-at 2026-10-26" consistent: receipt UTC 2026-10-27T00:08:08Z = local 2026-10-26 21:08:08 -03.
