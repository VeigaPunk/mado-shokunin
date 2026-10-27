# ScrEntry — C2 entry draft: `xkb-keymap-compile-r48`

Seat: `.ufo/waves/round-48/w1/ScrEntry/` (leaf member; no dispatch, no background jobs).
Claim worked: **C2 — coverage (sourced)**, `corpus/knowledge/xkb-keymap-compile-r48.md`, rows `<S340>`..`<S350>`.
Deliverable: a draft entry in the round-46 shape, its pins, a live read-only receipt, a quote verifier — all inside the seat dir.
Nothing was integrated: `corpus/` and `corpus/SOURCES.md` are untouched (the L1 is the only integrator).

## Behavior produced

- `xkb-keymap-compile-r48.md` (116 lines) — title, eleven `source:` lines with a scope each, `verified-at`, `recheck`, `ground`,
  a nine-row question table, nine numbered steps (each with computed `file:line` locators), 19 `OBS` lines carrying 20 located quotes,
  a census line, a live host section with the five name classes, an eight-row symptom→cause→check table, and eight Limits
  bullets with `[UNK]` items. Row ids and receipt-only values are the placeholders `<S340>`..`<S350>` and `<LIVE>`.
- `fetch/` — 13 pinned files (10 code pins + `rules/meson.build`, `rules/rules.in`, and a byte-equal copy of the installed
  `rules/evdev`). Every tag URL was re-fetched at the tag's commit and compared byte-for-byte (`same` for all 13).
- `receipts/make-receipt.sh` — the generator; re-runnable, bounded, writes the receipt next to itself.
- `receipts/xkbcli-compile-keymap-r48.txt` (14 149 B, 354 lines, sha256 `7dc2ec8078ebc0a793d678776adab077453d9f0c735917808a8058c19a84c839`) —
  every command and outcome of the live battery.
- `verify-quotes.py` — the quote/pin gate: PASS all 10 pins and 20 quotes (each needle checked against the cited line, against
  the entry, and for ≤25 words; the computed locator list is printed per quote).
- `pins.tsv` — row-candidate manifest (kind, tier, file, URL, commit, bytes, lines, sha256) for the L1's row creation.

## Gates run (observed)

| gate | command | outcome |
|---|---|---|
| quote + pin verification | `python3 .ufo/waves/round-48/w1/ScrEntry/verify-quotes.py` | `PASS all 10 pins and 20 quotes`, exit 0 |
| receipt reproducible | `receipts/make-receipt.sh` (twice) | same bytes apart from the timestamp; digest re-pinned both times |
| tag == commit bytes | `cmp` of tag-URL and commit-URL fetches, all 13 | all `same` (xkbcommon-1.13.2 → `d1442aaa…`; xkeyboard-config-2.48 → `cf8d1151…`) |
| registry census (claim check) | `grep -c '^\| S[0-9]' corpus/SOURCES.md` | 276 rows, tops at S339 — matches the claim |
| host run | the receipt's 28 labelled commands (30 `rc=` blocks incl. the two inline probes) | see "Findings" |

## Findings (each names what it supports or attacks)

**F1 — the claims call the unknown-option line a "warning"; it is emitted at ERROR level.**
`~/.config`-free reproduction: `xkbcli compile-keymap --test --layout br --options nope:nope` prints
`xkbcommon: ERROR: [XKB-595] Unrecognized RMLVO option "nope:nope" was ignored` and exits 0
(receipt lines under "unknown option"). XKB-595 is `XKB_ERROR_CANNOT_RESOLVE_RMLVO`
(`fetch/xkbcommon-messages-codes.h:150`), and the call site is `log_err` (`fetch/xkbcommon-rules.c:2045-2064`). What is
WARNING-level (`log_warn`) is hidden by default (`fetch/xkbcommon-context.c:503`, default level ERROR): the "More layouts
than variants" line only appears with `XKB_LOG_LEVEL=warn` (receipt, same run at both levels). Attacks the phrasing of the C2
host fact at claims.md and `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/claims.md` ("dropped with a
warning (unknown option: XKB-595 …)"); the entry records the observed level. Freeze-time decision for the L1.

**F2 — an unknown model is not "dropped": it matches the wildcards and changes the geometry component, silently.**
`--model nope` exits 0 with keycodes `evdev+aliases(qwerty)` and geometry `pc(pc104)` instead of `pc(pc105)`, and prints
nothing even at `XKB_LOG_LEVEL=warn` (receipt). Cause: `rules/evdev` maps any model (`fetch/xkeyboard-config-rules-evdev:55-59`)
and any model to a geometry (`:74-107`, `pc(pc104)` at `:107`); a wildcard match sets `matched`, so no report is due
(`fetch/xkbcommon-rules.c:1507-1510`, report at `:2045-2064`). Supports step 7 and the decision table.

**F3 — an empty `kb_layout` with a set `kb_variant` discards the variant.**
`--layout '' --variant intl` warns `Layout not provided, but variant set to "intl": ignoring variant and using defaults for
both: layout="us", variant=""` and compiles `us` (`fetch/xkbcommon-context-priv.c:202-217`; receipt). Relevant to this host's
own file: `# kb_layout = us,dk,eu` and `# kb_variant = intl` sit at `~/.config/hypr/input.conf:5` and `:8`; uncommenting only
the second line would silently give `us`, not `us(intl)`. Extra beyond the declared C2 bullets.

**F4 — a rules name can exist and still not compile.** `--rules xfree98` finds the file, returns no components, and fails with
XKB-595 `No components returned from XKB rules "xfree98"` (`fetch/xkbcommon-rules.c:2028-2036`; receipt rc 1). Attacks any
"the ruleset exists, so it works" reading of `ls rules/`.

**F5 — include-path precedence is proven by exit status, not only by source.** A five-line `symbols/zz` at
`$XDG_CONFIG_HOME/xkb` compiles `--layout zz` (rc 0, 68 176 B keymap, sha256 `0f752872…`), the same file at `$HOME/.xkb`
produces a byte-identical keymap (rc 0), and with neither path the run fails XKB-338 `symbols/zz` (rc 1) — all three in the
receipt under "include-path precedence". Probes ran in scratch `XDG_CONFIG_HOME`/`HOME`, never in the real ones.

**F6 — the 2.48 tag has no `rules/evdev`; the installed file is generated.** `rules/evdev.in` is a 404 at the tag; the tag ships
`rules/rules.in` and `rules/meson.build` (`custom_target` for `base`/`evdev` at `rules/meson.build:18-39`). The row for the
ruleset therefore pins the package bytes (byte-equal copy in `fetch/`) plus the generator, not a raw tag path. Anything that
cites `rules/evdev` at a tag URL would be citing a 404 page.

**F7 — `xkbcli` ignores `XKB_DEFAULT_*` unless told otherwise.** Without `--enable-environment-names` the context sets
`XKB_CONTEXT_NO_ENVIRONMENT_NAMES` (`fetch/xkbcommon-tools-compile-keymap.c:585-587`); `XKB_DEFAULT_LAYOUT=zz` then still
compiles `us`, and with the flag it resolves `zz` (receipt). A receipt that forgot the flag measures defaults, not names.

**F8 — default log level hides every WARNING.** `fetch/xkbcommon-context.c:503`; observed as the difference between the two
"two layouts, one variant" runs. Consequence for step 8: a compositor that logs at the default level shows the failure
(ERROR) but not the count-mismatch warning, so a user-visible log can under-report a degraded keymap.

## Row drafts for `corpus/SOURCES.md` (S340–S350)

The L1 should re-derive `status`/`used-by` per its own bookkeeping; the anchors below are computed (`grep -n`) and hashed.
Receipt paths are relative to the lane root.

```
| S340 | xkbcommon/libxkbcommon src/xkbcomp/rules.c @ xkbcommon-1.13.2 — https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/xkbcomp/rules.c | code | A | the RMLVO matcher: comma list parsing, layout/variant pairing, %l/%v expansion, the unmatched-name report | xkbcommon-rules.c:32 MAX_INCLUDE_DEPTH, :520-535 the name pairing warning/truncation, :1257-1297 %l/%v expansion marks matched, :1893-2025 rules-file read and .pre/.post, :2045-2064 the "was ignored" report @ tag xkbcommon-1.13.2 commit d1442aaa6b635551182e83c3b55037f4c118c962, 74868 B sha256:04dfd93468369de226b47c94475c1df93a41ce85bdd698c761312a38204e42a8; receipt .ufo/waves/round-48/w1/ScrEntry/fetch/xkbcommon-rules.c | comma lists pair by index, a %l/%v expansion marks the name matched so an unknown layout fails later rather than being reported, and an unmatched option is reported only after a successful resolve | mined | 2026-10-26 | on-release | .ufo/waves/round-48/w1/ScrEntry/xkb-keymap-compile-r48.md |
| S341 | xkbcommon/libxkbcommon src/xkbcomp/xkbcomp.c @ xkbcommon-1.13.2 — https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/xkbcomp/xkbcomp.c | code | A | the RMLVO -> KcCGST -> parse pipeline and its failure messages | xkbcommon-xkbcomp.c:60-64 parse failure, :141-194 text_v1_keymap_new_from_names (resolve, KcCGST log, parse), :157-166 the resolve-failure branch @ tag xkbcommon-1.13.2 commit d1442aaa6b635551182e83c3b55037f4c118c962, 7920 B sha256:ae6823a876691c340362fb43a784ad4f45a3a96869474503965bfef4481dd74c; receipt .ufo/waves/round-48/w1/ScrEntry/fetch/xkbcommon-xkbcomp.c | a failed resolve makes the call return NULL with "Couldn't look up rules …" — the only thing a compositor sees | mined | 2026-10-26 | on-release | .ufo/waves/round-48/w1/ScrEntry/xkb-keymap-compile-r48.md |
| S342 | xkbcommon/libxkbcommon src/xkbcomp/include.c @ xkbcommon-1.13.2 — https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/xkbcomp/include.c | code | A | `symbols/<file>` lookup over the include paths, with the XKB-338 and XKB-661 reports | xkbcommon-include.c:320-363 FindFileInXkbPath (first hit over the ordered paths, XKB-338 at :353-358), :378-510 ProcessIncludeFile (file+map, XKB-661 at :498-506) @ tag xkbcommon-1.13.2 commit d1442aaa6b635551182e83c3b55037f4c118c962, 17209 B sha256:95b5d8b53be3d53e30d07824cae6952f2f148c63c29e552592cf1dd6da68eaef; receipt .ufo/waves/round-48/w1/ScrEntry/fetch/xkbcommon-include.c | the first include path that has the file wins, and "no file" and "file without that map" are two different failures with two different ids | mined | 2026-10-26 | on-release | .ufo/waves/round-48/w1/ScrEntry/xkb-keymap-compile-r48.md |
| S343 | xkbcommon/libxkbcommon src/context.c @ xkbcommon-1.13.2 — https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/context.c | code | A | the default include-path order, the legacy-root fallback, the default log level | xkbcommon-context.c:90-97 the extra path env, :243-338 the default order (XDG, HOME/.xkb, extra, extensions, root) and the legacy-root fallback at :327-337, :503 default log level ERROR @ tag xkbcommon-1.13.2 commit d1442aaa6b635551182e83c3b55037f4c118c962, 16074 B sha256:e6547abb657d27cdb42907d254d9bdd047435db8b5f59bb88fe69a315b84b8b7; receipt .ufo/waves/round-48/w1/ScrEntry/fetch/xkbcommon-context.c | the search order a user override must beat, why a failed root still compiles, and why WARNING lines are invisible by default | mined | 2026-10-26 | on-release | .ufo/waves/round-48/w1/ScrEntry/xkb-keymap-compile-r48.md |
| S344 | xkbcommon/libxkbcommon src/context-priv.c @ xkbcommon-1.13.2 — https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/context-priv.c | code | A | empty names replaced by defaults, and the layout-and-variant tie | xkbcommon-context-priv.c:128-184 the XKB_DEFAULT_* getters, :186-225 xkb_context_sanitize_rule_names (empty layout discards the variant at :202-217) @ tag xkbcommon-1.13.2 commit d1442aaa6b635551182e83c3b55037f4c118c962, 5898 B sha256:c2ffff03f40181e4110d5549d4cab3be002cfc4258125a15d6f4876f31724c10; receipt .ufo/waves/round-48/w1/ScrEntry/fetch/xkbcommon-context-priv.c | an empty or missing name is defaulted before any file is read, and a variant without a layout is discarded with a WARNING | mined | 2026-10-26 | on-release | .ufo/waves/round-48/w1/ScrEntry/xkb-keymap-compile-r48.md |
| S345 | xkbcommon/libxkbcommon meson_options.txt @ xkbcommon-1.13.2 — https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/meson_options.txt | code | A | the compiled-in default rules/model/layout/variant/options | meson_options.txt:32-59 (`default-rules` evdev, `default-model` pc105, `default-layout` us, `default-variant` and `default-options` empty) @ tag xkbcommon-1.13.2 commit d1442aaa6b635551182e83c3b55037f4c118c962, 2411 B sha256:496455ea3c5b368b382e3b155e66eb43226f66b0a0d1eeabbca450976175c32d; receipt .ufo/waves/round-48/w1/ScrEntry/fetch/xkbcommon-meson_options.txt | the five values an empty name becomes, confirmed live by a run with no names | mined | 2026-10-26 | on-release | .ufo/waves/round-48/w1/ScrEntry/xkb-keymap-compile-r48.md |
| S346 | xkeyboard-config 2.48 rules/evdev — the installed file, generated from rules/rules.in by rules/meson.build:18-39 (byte-equal copy: .ufo/waves/round-48/w1/ScrEntry/fetch/xkeyboard-config-rules-evdev) | code | A | the wildcard sections that turn names into KcCGST | rules/evdev:55-64 model and layout to keycodes, :71-107 geometry wildcards (pc(pc104) at :107), :109-175 symbols with the catch-all pc+%l%(v) at :175, :529-586 the option rows (compose:caps at :570); provenance rules/meson.build + rules/rules.in @ tag xkeyboard-config-2.48 commit cf8d1151bb4c9ef5b895828d0e6dd7860c0833e0; installed file 31520 B sha256:0cc48ee1279d91045fe2cf092ee5a0744cbee1c02bd164f02871d13140d12132 (package xkeyboard-config 2.48-1) | which name classes are matched by a wildcard (model, layout, variant) and which are matched only by name (option) — hence which typo fails and which is dropped | mined | 2026-10-26 | on-release | .ufo/waves/round-48/w1/ScrEntry/xkb-keymap-compile-r48.md |
| S347 | xkeyboard-config 2.48 symbols/br — https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config/-/raw/xkeyboard-config-2.48/symbols/br | code | A | the maps `br` offers, i.e. the variant names that can succeed | symbols/br:1-4 the default map (abnt2), :47 nodeadkeys, 11 xkb_symbols maps in all, byte-equal to /usr/share/xkeyboard-config-2/symbols/br @ tag xkeyboard-config-2.48 commit cf8d1151bb4c9ef5b895828d0e6dd7860c0833e0, 19592 B sha256:8cf65550e08b598407d5f7317f297e186561a94c866ab95d0c9a8737ef3bf35e; receipt .ufo/waves/round-48/w1/ScrEntry/fetch/xkeyboard-config-symbols-br | a variant is a map name in this file: nodeadkeys compiles, nope and caps fail with XKB-661 on br(...) | mined | 2026-10-26 | on-release | .ufo/waves/round-48/w1/ScrEntry/xkb-keymap-compile-r48.md |
| S348 | xkbcommon/libxkbcommon tools/compile-keymap.c @ xkbcommon-1.13.2 — https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/tools/compile-keymap.c | code | A | what `xkbcli compile-keymap` passes, what `--test` skips, its exit status | compile-keymap.c:508-535 print_keymap (compile, `--test` skips serialization, EXIT_FAILURE at :520-522), :585-604 context flags and include defaults, :630 return rc @ tag xkbcommon-1.13.2 commit d1442aaa6b635551182e83c3b55037f4c118c962, 23033 B sha256:099664cea533c2ea4c85b2bd45b8f3dc0f9ed4e2b39f904b2cf5c165f10e533d; receipt .ufo/waves/round-48/w1/ScrEntry/fetch/xkbcommon-tools-compile-keymap.c | a receipt from `xkbcli` proves the command-line names only (environment names are off by default) and rc 1 is the tool's own failure path after libxkbcommon's lines | mined | 2026-10-26 | on-release | .ufo/waves/round-48/w1/ScrEntry/xkb-keymap-compile-r48.md |
| S349 | xkbcommon/libxkbcommon src/messages-codes.h @ xkbcommon-1.13.2 — https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/messages-codes.h | code | A | the numeric ids in the diagnostic lines | messages-codes.h:116 XKB-338, :150 XKB-595, :162 XKB-661, :178 XKB-769, :190 XKB-822 @ tag xkbcommon-1.13.2 commit d1442aaa6b635551182e83c3b55037f4c118c962, 9554 B sha256:4e721d31ebd9b8979efb46905644f8f19dcdb450f6a00e57be48cf2cf013631d; receipt .ufo/waves/round-48/w1/ScrEntry/fetch/xkbcommon-messages-codes.h | XKB-338 is "included file not found", XKB-595 is "cannot resolve RMLVO" and is also the id of the non-fatal "was ignored" line, XKB-822 is the keymap-compilation failure | mined | 2026-10-26 | on-release | .ufo/waves/round-48/w1/ScrEntry/xkb-keymap-compile-r48.md |
| S350 | mado host read-only XKB compile receipt — .ufo/waves/round-48/w1/ScrEntry/receipts/xkbcli-compile-keymap-r48.txt | own-work | A | this host's XKB names, the five name classes, the include-path precedence probes, the log-level difference | generator .ufo/waves/round-48/w1/ScrEntry/receipts/make-receipt.sh; /usr/bin/xkbcli 1.13.2 (libxkbcommon 1.13.2-1, xkeyboard-config 2.48-1); 354 lines, 14149 B sha256:7dc2ec8078ebc0a793d678776adab077453d9f0c735917808a8058c19a84c839; the host keymap itself is not archived (2090 lines, 73079 B, sha256 efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81) | `br` + `compose:caps` compiles; `zz`, `br(nope)`, `br(caps)`, `rules nope`, `rules xfree98` fail; `nope:nope` and `model nope` do not; a user `symbols/zz` compiles only from a user include path | mined | 2026-10-26 | on-release | .ufo/waves/round-48/w1/ScrEntry/xkb-keymap-compile-r48.md |
```

`pins.tsv` carries the same rows as tab-separated fields (kind, tier, file, URL, commit, bytes, lines, sha256) plus the
commit-resolution record for both tags.

## Touched surfaces

- New, inside the seat dir only: `xkb-keymap-compile-r48.md`, `pins.tsv`, `verify-quotes.py`,
  `receipts/make-receipt.sh`, `receipts/xkbcli-compile-keymap-r48.txt`, `fetch/` (13 files).
- This report: `.ufo/waves/round-48/w1/ScrEntry.md`.
- Untouched: `corpus/` (entry and `SOURCES.md`), `tools/`, `quality/`, `.ufo/state/`, the lane's git/jj index, the fleet root.

## Out-of-scope / not done (deliberate)

- No compositor interaction: no `hyprctl` verb at all, no restart, no keymap dump; the compositor half is held from S318/S319.
- No option enumeration beyond `compose:caps` and one unknown option; no second layout's variant list; no `kb_file` path.
- No integration: the entry is not placed under `corpus/knowledge/`, no SOURCES rows were added, no manifest/verdict touched.
- No work on C1, the routed round-47 closure items (D1–D4, R3, R4b, M47-10), or the counters.

## Host safety / tool state

- Read-only verbs only: `xkbcli --version`, `compile-keymap` (`--test`, `--kccgst`, `--verbose`, full compile to a file in
  scratch), `pacman -Q` (a query; **no transaction**), `readlink`, `ls`, `grep`, `sha256sum`, `cmp`, `curl` for tag pins.
- No terminal, GUI, socket, compositor, input injection or host-config write. The real `~/.cache`, `~/.config` and
  `~/.local/share` were read only; `~/.config/hypr/input.conf` and the omarchy default were read for their `kb_` lines and hashed.
- Scratch: `/fast/scratch/hyaku/mado-r48/ScrEntry/` (probes in `mktemp -d` subdirs, removed by trap; the root removed at
  finish). Nothing citable lives there; every cited probe is reproducible from `receipts/make-receipt.sh`.
- Tool installs: **none** (no pacman transaction, no uv, no npm). Versions used as installed:
  `/usr/bin/xkbcli` 1.13.2, libxkbcommon 1.13.2-1, xkeyboard-config 2.48-1.
- One host quirk recorded in the receipt header: `/usr/bin/pacman` prints `error: openai-chatgpt: missing required signature`
  on every query, so the package query is filtered to the two package lines. It is pre-existing host noise, not a version fact,
  and no package operation was attempted.

## Known limits of this seat's output

- The entry uses `<S340>`..`<S350>` placeholders: the L1 must bind them to the rows it actually creates (renumber if it splits
  or merges the `rules/evdev` provenance row) before the freeze.
- `<LIVE>` appears three times (the host keymap's bytes, lines and sha256); the values are in `receipts/xkbcli-compile-keymap-r48.txt:59-63` and in the
  `S350` row draft. Filling them is a mechanical copy, not a re-run.
- `receipts/make-receipt.sh` embeds a timestamp line, so a re-run changes the receipt digest; `verify-quotes.py` does not pin
  the receipt, only the ten code pins.
- The scratch `XDG_CONFIG_HOME`/`HOME` probes are reproducible from the recipe printed in the receipt, but the probe directory
  names in that output are ephemeral (`/fast/scratch/.../probe.XXXXXX`); they are not evidence paths — the exit statuses are.
