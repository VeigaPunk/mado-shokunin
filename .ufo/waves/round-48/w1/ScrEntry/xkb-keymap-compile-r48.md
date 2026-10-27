# From `input:kb_*` names to a compiled keymap on this host: which XKB names libxkbcommon 1.13.2 accepts, which it drops, and which one fails the compile Hyprland 0.56.2 falls back on

source: <S340> - xkbcommon/libxkbcommon src/xkbcomp/rules.c @ xkbcommon-1.13.2 - the RMLVO matcher: comma lists, layout/variant pairing, `%l`/`%v` expansion, the "was ignored" report
source: <S341> - xkbcommon/libxkbcommon src/xkbcomp/xkbcomp.c @ xkbcommon-1.13.2 - the RMLVO -> KcCGST -> parse pipeline and its three failure messages
source: <S342> - xkbcommon/libxkbcommon src/xkbcomp/include.c @ xkbcommon-1.13.2 - `symbols/<name>` lookup over the include paths, XKB-338 and XKB-661
source: <S343> - xkbcommon/libxkbcommon src/context.c @ xkbcommon-1.13.2 - the default include-path order, the legacy-root fallback, the default log level
source: <S344> - xkbcommon/libxkbcommon src/context-priv.c @ xkbcommon-1.13.2 - empty names replaced by defaults, layout-and-variant tie
source: <S345> - xkbcommon/libxkbcommon meson_options.txt @ xkbcommon-1.13.2 - the compiled-in default rules/model/layout/variant/options
source: <S346> - xkeyboard-config 2.48 rules/evdev (installed at /usr/share/xkeyboard-config-2/rules/evdev; generated from rules/rules.in by rules/meson.build:18-39) - the wildcard sections that turn names into KcCGST
source: <S347> - xkeyboard-config 2.48 symbols/br (tag xkeyboard-config-2.48, byte-equal to the host file) - the eleven maps `br` offers and the map names a variant must match
source: <S348> - xkbcommon/libxkbcommon tools/compile-keymap.c @ xkbcommon-1.13.2 - what `xkbcli compile-keymap` passes, what `--test` skips, the exit status
source: <S349> - xkbcommon/libxkbcommon src/messages-codes.h @ xkbcommon-1.13.2 - the numeric ids XKB-338/595/661/769/822
source: <S350> - mado host, read-only `xkbcli compile-keymap` receipt (own-work) - this host's names, the five unknown-name classes, the include-path precedence probes
verified-at: 2026-10-26
recheck: on-release - when xkbcommon leaves 1.13.2 or xkeyboard-config leaves 2.48 (or 90d at the latest) re-pull the ten code pins and re-run `receipts/make-receipt.sh`; the ruleset the host reads is generated (`rules/meson.build:18-39`), so a package rebuild can change the wildcards without any change in the tag's `rules/rules.in`
ground: the XKB compile under the input plane, held open at base - `corpus/knowledge/hyprland-input-devices-r46.md:69` ("The XKB compile itself is not reproduced") and `corpus/README.md:112` ("Still open: the XKB compile itself"); held neighbours: rows S318/S319 give the compositor's `us` default and its fallback after a keymap that does not compile, cited here and never re-claimed
Lane: mado-shokunin. Round: 48.

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| which `kb_rules` names exist on this host, and what a name that does not exist does | step 3, host table | observed 2026-10-26 |
| which `kb_layout` / `kb_variant` pairs compile, and which fail | steps 4-6, host table | observed |
| which unknown names are dropped with a message and which fail the compile | step 7, host table | observed |
| how a comma list in `kb_layout` pairs with a comma list in `kb_variant` | step 2, step 5 | sourced and observed |
| where a name is searched for, and which path wins | step 6 | sourced, precedence observed |
| what "unknown model" does when it prints nothing | step 7 | observed (the KcCGST geometry changes) |
| why a keyboard ends up on `us` after a bad name | step 8 | held: rows S318/S319, not re-run here |
| which diagnostics a failed or degraded compile prints by itself | step 9 | observed (log-level dependent) |
| whether the compositor's own context honours `XKB_DEFAULT_*` | step 1 | [UNK]: the environment route is libxkbcommon's; Hyprland's context flags are not in this round |

## The compile, step by step

1. **Names and defaults.** An empty rules, model, layout or options string is replaced before any file is read: rules `evdev`, model `pc105`, layout `us` (context-priv.c:192-204; the compiled-in values at meson_options.txt:32-59, confirmed live by a run with no names). Layout and variant are tied: with an empty layout the variant is discarded and both come from the defaults, with a warning that the default level hides (context-priv.c:202-217). `xkbcli` disables the `XKB_DEFAULT_*` environment route unless `--enable-environment-names` is given (compile-keymap.c:585-587), so a receipt taken from `xkbcli` proves the names on its command line and nothing else; with the flag, `XKB_DEFAULT_LAYOUT=zz` reaches the rules (receipt).
2. **Comma lists.** The layout string is split on commas into one entry per group and the variant string likewise; a shorter variant list is zero-padded (rules.c:520-527) and a longer one is truncated with an ERROR-level line (rules.c:528-535). Both were run: `br,us` with `nodeadkeys` yields `pc+br(nodeadkeys)+us:2`, `br` with `nodeadkeys,intl` yields `pc+br(nodeadkeys)` plus `Less layouts than variants`.
3. **The rules file.** The ruleset name is resolved as `rules/<name>` over the include paths; a missing file stops the resolve at once (rules.c:1986-1992). Optional `<name>.pre` and `<name>.post` files are read around it, one per include path, in path order (rules.c:1995-2025). The package installs four rulesets - `base`, `evdev`, `xorg`, `xfree98` (receipt `ls`) - and `evdev` is the default. A file that exists can still resolve nothing: `xfree98` returns no components for this layout and the compile fails (rules.c:2028-2036, receipt rc 1).
4. **Names to components.** `rules/evdev` maps the names with wildcard sections: any model to keycodes `evdev` (`xkeyboard-config-rules-evdev:55-59`), any layout to `+aliases(qwerty)` (:61-64), any model+layout+variant to symbols `pc+%l%(v)` (:109-175), and each option name explicitly to its symbols include (:529-586). So the host's `br` + `compose:caps` becomes keycodes `evdev+aliases(qwerty)`, types and compat `complete`, symbols `pc+br+inet(evdev)+compose(caps)`, geometry `pc(pc105)` (receipt).
5. **`%l`/`%v` expansion and pairing.** A `%l` or `%v` with no index expands only when a single layout (variant) was given; with several, the index must be written or the `%i` group index used (rules.c:1257-1279). Expansion marks the name matched (rules.c:1297) - which is why an unknown layout produces no "ignored" line, but a symbols file name that does not exist. A variant is always expanded next to its layout, and the symbols value carries the group index for every layout after the first (`us:2`, receipt).
6. **File and map lookup.** The generated component names are resolved as `symbols/<file>` over the include paths, first hit wins over the ordered list (include.c:333); the order is `$XDG_CONFIG_HOME/xkb` (else `$HOME/.config/xkb`), `$HOME/.xkb`, `$XKB_CONFIG_EXTRA_PATH` (`/etc/xkb`), the versioned then unversioned extension directories, and `$XKB_CONFIG_ROOT` (`/usr/share/xkeyboard-config-2`) last (context.c:243-338). A required file that no path has logs XKB-338 with a census of the paths searched and the paths that could not be added (include.c:353-358); a file that exists but carries no map of that name logs XKB-661 with the include statement (include.c:498-506). If the configured root cannot be appended, the legacy root `/usr/share/X11/xkb` is tried instead, silently at the default log level (context.c:327-337). Precedence is live: a five-line `symbols/zz` placed at `$XDG_CONFIG_HOME/xkb` or `$HOME/.xkb` makes the otherwise fatal `zz` compile (rc 0, byte-identical keymaps), and without either path the same run fails XKB-338 (receipt).
7. **What each name class does when it is wrong.** Rules: a missing name fails; an existing name with no components fails. Model: every string matches the model wildcards, so an unknown model compiles - `--model nope` returns keycodes `evdev` and geometry `pc(pc104)` instead of `pc(pc105)`, and prints nothing even at `XKB_LOG_LEVEL=warn`, because a wildcard matched and there is nothing to report (the only trace is the geometry). Layout: the wildcard matches, `%l` substitutes the name into the symbols file, and a name with no `symbols/<name>` file fails the compile: `--layout zz` gives XKB-338 `symbols/zz`, XKB-661 `zz`, XKB-769, XKB-822, rc 1. Variant: the name is expanded into `symbols/<layout>(<variant>)`, so a variant the layout file does not define fails the same way: `br(nope)` and `br(caps)` each give XKB-661 and rc 1, while `br(nodeadkeys)` - a map the file has - compiles. Options: the option sections carry no wildcard (`xkeyboard-config-rules-evdev:529-586`), so an unmatched option is reported and dropped: `nope:nope` gives XKB-595 `Unrecognized RMLVO option "nope:nope" was ignored` and rc 0. The report itself is emitted after a successful resolve for any unmatched model, layout, variant or option (rules.c:2045-2064).
8. **What the compositor does with a failed compile.** A resolve or parse failure makes the RMLVO call return NULL (xkbcomp.c:157-166 for the resolve, xkbcomp.c:60-64 for the parse), which is the only thing Hyprland sees. Hyprland starts from `us` when no layout is configured (S318, `input:kb_layout` default) and resets a keyboard whose names did not compile to layout `us` with every other name empty (S319, the `m_currentRules` reset after a failed keymap). Both are held from round 46 (`hyprland-input-devices-r46.md:33`, its step 4) and are not re-measured here; this entry supplies only the libxkbcommon half of that chain.
9. **Which diagnostics are visible.** The default log level is ERROR (context.c:503), so WARNING lines are dropped unless `XKB_LOG_LEVEL=warn` (or `--verbose`). A layout/variant count mismatch is a warning and therefore invisible by default; the "was ignored" line for an unmatched option is ERROR-level and therefore visible even though the compile succeeds. The receipt carries the same run at both levels.

## Observations

**OBS** <S340> (pin opened 2026-10-26): `No index provided: match only if single layout` at xkbcommon-rules.c:1259 - `%l` expands only for a one-element layout list.
**OBS** <S340>: `expanded_value->matched = true;` at xkbcommon-rules.c:1297 - a name consumed by an expansion counts as matched, so step 7's layout case prints no "ignored" line.
**OBS** <S340>: `Unrecognized RMLVO option \"%.*s\" was ignored` at xkbcommon-rules.c:2063 - reported with code XKB-595, after a resolve that succeeded.
**OBS** <S340>: `Less layouts than variants: \"%s\" vs. \"%s\".` at xkbcommon-rules.c:530 - the truncation branch's message.
**OBS** <S341>: `ok = xkb_components_from_rules_names(keymap->ctx, rmlvo, &kccgst,` at xkbcommon-xkbcomp.c:157 - the resolve that decides between a compile and an error.
**OBS** <S341>: `Couldn't look up rules '%s', model '%s', layout '%s', ` at xkbcommon-xkbcomp.c:161 - the message that carries the rejected names.
**OBS** <S342>: `Couldn't find file \"%s/%.*s\" in include paths` at xkbcommon-include.c:355 - the XKB-338 line shape, `symbols/zz` for an unknown layout.
**OBS** <S342>: `Couldn't process include statement for '%s(%s)'` at xkbcommon-include.c:501 - the XKB-661 line shape, `br(nope)` for an unknown variant.
**OBS** <S343>: `const char * const root = xkb_context_include_path_get_system_path(ctx);` at xkbcommon-context.c:317 - the root is appended last.
**OBS** <S343>: `ret |= context_include_path_append(ctx, DFLT_XKB_LEGACY_ROOT);` at xkbcommon-context.c:336 - the legacy-root fallback behind a failed root.
**OBS** <S343>: `ctx->log_level = XKB_LOG_LEVEL_ERROR;` at xkbcommon-context.c:503 - the default level that hides every WARNING line.
**OBS** <S344>: `Layout not provided, but variant set to \"%s\": ` at xkbcommon-context-priv.c:208 - an empty layout discards the variant.
**OBS** <S345>: `value: 'us',` at xkbcommon-meson_options.txt:46 - the compiled-in default layout (`default-layout` at :44).
**OBS** <S346>: `pc+%l%(v)` at xkeyboard-config-rules-evdev:175 - the catch-all symbols value; the layout and variant names are the file and map names.
**OBS** <S346>: `compose:caps` at xkeyboard-config-rules-evdev:570 - the option that the host's config uses, mapped to `+compose(caps)`.
**OBS** <S347>: `xkb_symbols "nodeadkeys" {` at xkeyboard-config-symbols-br:47 - one of the eleven maps `br` offers; `nope` and `caps` are not among them.
**OBS** <S348>: `ctx_flags |= XKB_CONTEXT_NO_ENVIRONMENT_NAMES;` at xkbcommon-tools-compile-keymap.c:587 - `xkbcli` ignores `XKB_DEFAULT_*` unless the flag is given.
**OBS** <S348>: `fprintf(stderr, "ERROR: Couldn't create xkb keymap\n");` at xkbcommon-tools-compile-keymap.c:521 - the tool's own line, after libxkbcommon's.
**OBS** <S349>: `XKB_ERROR_INCLUDED_FILE_NOT_FOUND = 338,` at xkbcommon-messages-codes.h:116 and `XKB_ERROR_CANNOT_RESOLVE_RMLVO = 595,` at :150 - the two ids that name the drop classes.

Census of the pinned bytes:

compile_defaults rules=evdev model=pc105 layout=us variant=empty options=empty include_paths=4 base(+2 extension dirs) rules_files=4 br_maps=11 msg_ids=338,595,661,769,822 max_rules_include_depth=5

## Live host run (read-only)

The host's names are `kb_layout = br` and `kb_options = compose:caps` in `~/.config/hypr/input.conf` (sha256 `3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4`, lines 10-11), after the omarchy default input file (`bee5aa68cbec0c428fae7a5faf7da49a30e6f78ed96e78a063f08b66942448b8`, `kb_layout = us` at line 3) that `hyprland.conf` sources first - the file order recorded in the round-46 erratum. `xkbcli compile-keymap --layout br --options compose:caps` exits 0, prints nothing on stderr, and produces a keymap of <LIVE> bytes / <LIVE> lines with sha256 `<LIVE>` (receipt). Its KcCGST line is `pc+br+inet(evdev)+compose(caps)`.

The verbose log shows the search order step 6 predicts: `~/.config/xkb`, `~/.xkb` and `/etc/xkb` could not be added, the two extension directories `/usr/share/xkeyboard-config-2.d` and `/usr/share/xkeyboard-config.d` do not exist, and `/usr/share/xkeyboard-config-2` is the one include path added (receipt).

The five name classes, each run on this host against libxkbcommon 1.13.2-1 and xkeyboard-config 2.48-1 (receipt):

| name | value | stdout / stderr | rc |
|---|---|---|---|
| `--rules` | `base`, `xorg` | compiles, symbols `pc+br+inet(pc105)` | 0 |
| `--rules` | `xfree98` | XKB-595 `No components returned from XKB rules "xfree98"` | 1 |
| `--rules` | `nope` | XKB-338 `rules/nope`, XKB-595 `Cannot load XKB rules "nope"`, XKB-822 | 1 |
| `--model` | `nope` | silent at every level; geometry `pc(pc104)` instead of `pc(pc105)` | 0 |
| `--layout` | `br` | compiles | 0 |
| `--layout` | `zz` | XKB-338 `symbols/zz`, XKB-661 `zz`, XKB-769, XKB-822 | 1 |
| `--variant` | `nodeadkeys` (on `br`) | compiles | 0 |
| `--variant` | `nope`, `caps` (on `br`) | XKB-661 `br(nope)` / `br(caps)`, XKB-769, XKB-822 | 1 |
| `--options` | `compose:caps` | compiles, `+compose(caps)` | 0 |
| `--options` | `nope:nope` | XKB-595 `Unrecognized RMLVO option "nope:nope" was ignored` | 0 |

Multi-layout: `--layout br,us --variant nodeadkeys` gives symbols `pc+br(nodeadkeys)+us:2+inet(evdev)` and only a WARNING about the missing second variant (visible at `XKB_LOG_LEVEL=warn`); `--layout br --variant nodeadkeys,intl` drops the second variant with an ERROR-level line and still exits 0; `--layout br,us --variant ,dvorak` pairs `dvorak` with `us`. `--layout '' --variant intl` discards the variant and compiles `us`.

## Reading a failure

| symptom | most likely cause | check |
|---|---|---|
| keyboard prints `us`, config says another layout | compile failed and the compositor reset it (step 8) | `xkbcli compile-keymap --test --layout <name> --variant <v> --options <o>`; rc 1 names the class |
| `Couldn't find file "symbols/<name>"` | layout name has no symbols file on any include path | `ls /usr/share/xkeyboard-config-2/symbols/<name>`; or the file is in a user path that is not on the list (step 6) |
| `Couldn't process include statement for '<layout>(<variant>)'` | variant is not a map in that layout's symbols file | `grep -n '^xkb_symbols' /usr/share/xkeyboard-config-2/symbols/<layout>` |
| `Cannot load XKB rules "<name>"` | no `rules/<name>` in any include path | `ls /usr/share/xkeyboard-config-2/rules/` |
| `No components returned from XKB rules "<name>"` | the ruleset exists but maps nothing for these names | `xkbcli compile-keymap --kccgst --rules <name> --layout <l>` |
| `Unrecognized RMLVO option ... was ignored`, rc 0 | option typo; the compile succeeds without it | compare against `[[:space:]]<option>[[:space:]]*=.*symbols` in `rules/evdev` |
| no diagnostic at all, but the keymap looks wrong | an empty or defaulted name (step 1), or a WARNING hidden by the default log level (step 9) | re-run with `XKB_LOG_LEVEL=warn` |
| user file in `$XDG_CONFIG_HOME/xkb` or `$HOME/.xkb` has no effect | an earlier path supplied the file, or the name is not the file the rules generate | the XKB-338 census lists the paths searched, in order |

## Limits

- The compositor half is held, not measured: no Hyprland restart, reload or keymap dump was taken this round; steps 8 cite S318/S319. Whether Hyprland's own context is created with `XKB_CONTEXT_NO_ENVIRONMENT_NAMES` or with extension directories enabled is [UNK].
- `kb_file` bypasses this whole chain - a keymap file is parsed directly, so a readable `kb_file` makes every table here about names moot (round-46 step 4, held).
- Options that land in compat or types rather than symbols (`grp:*`, `caps:escape*`, `lv3:*` and the keypad options) were not enumerated; only `compose:caps` and one unknown option were run. The option sections of `rules/evdev` are the place to extend this.
- Per-layout variant lists are not enumerated: `br` has eleven maps, and the same check on another layout needs its own `symbols/<layout>` read. No layout other than `br`, `us` and the synthetic `zz` was compiled.
- The keymap body itself is not archived (about 73 KB); only its digest, byte count and line count are held, so a byte-level comparison of two builds is possible but a semantic diff was not run.
- The ruleset the host reads is generated at package build time; the tag's `rules/rules.in` and the generator inputs were not re-run here, so the mapping from `rules.in` to the installed `rules/evdev` is [UNK] beyond the meson target's name.
- Only `xkbcli` was executed. The compositor links its own libxkbcommon build; the package is the same 1.13.2-1, but build options (extra include paths, extension directories) are [UNK] for that binary.
- The two user include paths were probed in a scratch `XDG_CONFIG_HOME`/`HOME`, not in the real ones; the host's own `~/.config/xkb` and `~/.xkb` do not exist (receipt, XKB-338 census), so their absence is a host fact but their behaviour is inferred from the scratch probe.
