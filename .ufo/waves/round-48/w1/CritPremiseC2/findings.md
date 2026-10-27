# CritPremiseC2 findings — attacking C2's premise (XKB compile entry) before the freeze

Attacked: round-48 claim C2 (`claims.md:22-27`) — a sourced knowledge entry `xkb-keymap-compile-r48.md` for which `kb_*` names compile on this host, built on the premise that the XKB compile is unheld at base and on a live `xkbcli compile-keymap` receipt standing in for Hyprland's own compile.

## 1. Premise "compile unheld at base" — CONFIRMED

Grep at base `579f694b45c797a9c39761fdb4f9e0a1b71b3585` (whole `corpus/` + `tools/`) for `xkb.*(compile|keymap)|compile.*xkb|keymap.*(compile|exists)|xkeyboard` yields exactly two open-limit lines and one rejected-lesson line; no corpus entry and no tool holds the compile:

| locus at base | content |
|---|---|
| `corpus/README.md:112` | "Still open: the XKB compile itself (whether a layout/variant pair exists in xkeyboard-config)" |
| `corpus/knowledge/hyprland-input-devices-r46.md:69` | "The XKB compile itself is not reproduced: whether a given layout/variant pair exists in xkeyboard-config is not checked" |
| `corpus/lessons/round-46-verifier-spotcheck.md:83` | REJECT row: `Keyboard.cpp` "cannot move any step of the chain" (no compile) |

Broad second grep at base for `xkbcli|compile-keymap|xkeyboard-config|XKB_DEFAULT|RMLVO|KcCGST` returns the same two lines only. `tools/mado-devices.py:9,84` mentions the fallback but does not compile. Registry check: `corpus/SOURCES.md` has 276 rows, top row S339 (matches `claims.md`). Premise holds; at HEAD (5ff1674) the same two lines are still open (the claim's source of truth is not dated away).

## 2. Premise "xkbcli compile-keymap behaves like Hyprland's own compile" — HOLD ONLY UNDER EXPLICIT NAMES + SAME ENVIRONMENT

Both invoke the identical library entry point with identical compile flags:

- Hyprland 0.56.2 `Hyprland-IKeyboard.cpp:99`: `xkb_keymap_new_from_names2(CONTEXT, &XKBRULES, XKB_KEYMAP_FORMAT_TEXT_V2, XKB_KEYMAP_COMPILE_NO_FLAGS)`; context at `:75` is `xkb_context_new(XKB_CONTEXT_NO_FLAGS)`.
- `xkbcli compile-keymap` (`tools/compile-keymap.c` at tag xkbcommon-1.13.2): `load_keymap` → `xkb_keymap_new_from_names2(ctx, rmlvo, keymap_input_format, XKB_KEYMAP_COMPILE_NO_FLAGS)`; `keymap_input_format = DEFAULT_INPUT_KEYMAP_FORMAT` = `XKB_KEYMAP_FORMAT_TEXT_V2` (`src/keymap-formats.h:13`).

The differences that break a blanket equivalence:

1. **Context flags.** Tool: `XKB_CONTEXT_NO_DEFAULT_INCLUDES` always, plus `XKB_CONTEXT_NO_ENVIRONMENT_NAMES` unless `--enable-environment-names` (compile-keymap.c `main`). Hyprland: `XKB_CONTEXT_NO_FLAGS` → environment names ON.
2. **Names: Hyprland never passes NULL.** `XKBRULES` is filled from `rules.rules.c_str()` etc. (`Hyprland-IKeyboard.cpp:67-73`); unset config fields are `""`, not NULL. `xkbcli` leaves omitted CLI fields NULL.
3. **sanitize treats "" and NULL the same for rules/model/layout, not for options.** `xkb_context_sanitize_rule_names` (`src/context-priv.c:186-225`): rules/model/layout use `isempty` (NULL or `""` → default, env-overridable when `use_environment_names`); options use `== NULL` alone (`:219`), so `""` is respected as empty and the env default is skipped.
4. **Hyprland's layout is never empty** (global default `"us"` at `Hyprland-ConfigValues.cpp:272`), so `XKB_DEFAULT_LAYOUT`/`XKB_DEFAULT_VARIANT` are never consulted by Hyprland; `XKB_DEFAULT_OPTIONS` is skipped because the options string is `""` non-NULL; only `XKB_DEFAULT_RULES`/`XKB_DEFAULT_MODEL` could reach Hyprland (via its `""`→env fill), and only if the compositor environment sets them. A bare tool run uses all five/env defaults only with `--enable-environment-names`.

Empirical confirmation on host (receipt `receipts-xkbcli-empirical.txt`):

- R1: clean-env `--rmlvo` → `rules: "evdev" model: "pc105" layout: "us" variant: "" options: ""` (matches meson defaults in `meson_options.txt`).
- R2: `XKB_DEFAULT_LAYOUT=br` without the flag → still `us` (ignored).
- R3: with `--enable-environment-names` → `layout: "br" options: "compose:caps"` (honored).
- R4/R5: a custom `symbols/zz` under `$HOME/.xkb` and under `$XDG_CONFIG_HOME/xkb` compiles (`--layout zz --test` rc 0).
- R6: with both user dirs absent, only one include path is searched: `/usr/share/xkeyboard-config-2` (`[XKB-338]` lists 1 searched, 3 failed). `/usr/share/X11/xkb` is a symlink to `/usr/share/xkeyboard-config-2` (host fact, receipt R0).
- R7: a broken user `symbols/xyzzy` is read before the system root (`xyzzy:1:1: syntax error`), proving user-before-root order.

**Counterexample for the planned entry:** "xkbcli compile-keymap reproduces the resolver's compile" is false as stated. A run with `XKB_DEFAULT_RULES`/`XKB_DEFAULT_MODEL` in the environment diverges between Hyprland (would use them) and bare xkbcli (won't). The claim holds only for (a) all five names passed explicitly — the planned receipt does pass `--layout br --options compose:caps`, and its remaining fields resolve identically on both sides — and (b) the same `HOME`/`XDG_CONFIG_HOME`/`XKB_CONFIG_ROOT` (user include paths can change which file wins, R4-R7).

## 3. Ownership — mado input plane, not tsukuroi/kotoba

- mado `PROVINCE.md:102-114` (round-46 refinement) owns "the input-device plane … the `input` block's `kb_layout`, `kb_variant`, `kb_options`, `kb_model`, `kb_rules`, `kb_file` keys … at the resolution Hyprland 0.56.2 gives it". Compile-of-names is that resolution; placement is correct.
- tsukuroi owns OS substrate/package state (`tsukuroi-shokunin/PROVINCE.md:3-4`): whether the packages exist, not the keymap behavior. ADJ-03 routes config-level diagnosis to mado (`tsukuroi-shokunin/PROVINCE.md:48`).
- kotoba owns prompt/skill craft (`kotoba-shokunin/PROVINCE.md:3-6`); unrelated.

## 4. Which sentences would be generic (library) rather than host-plane knowledge

The entry must not present library mechanics as host findings; each must carry a source pin (libxkbcommon tag `xkbcommon-1.13.2` = commit `d1442aaa6b635551182e83c3b55037f4c118c962`; xkeyboard-config 2.48):

| sentence class | generic (pin) | host-only (receipt) |
|---|---|---|
| RMLVO→KcCGST matching, `*`/`<none>` wildcards, skip rules | `src/xkbcomp/rules.c` | — |
| unknown-option/model/layout/variant dropped with "Unrecognized RMLVO … was ignored" (XKB-595; rc 0) | `src/xkbcomp/rules.c:2048-2063` | measured rc for the host's names (L1) |
| unknown layout/variant/rules fail with "Couldn't find file …"/"Couldn't process include statement …" (rc 1) | `src/xkbcomp/include.c`/rules.c | measured rc per name (L1) |
| include-path order ($XDG_CONFIG_HOME/xkb → $HOME/.xkb → extra (/etc/xkb) → root; env overrides `XKB_CONFIG_ROOT`/`XKB_CONFIG_EXTRA_PATH`) | `src/context.c` (`xkb_context_include_path_append_default`, `xkb_context_include_path_get_system_path`/`_get_extra_path`) | this host's root = `/usr/share/xkeyboard-config-2` via symlink; 3 user/extra paths absent (R0, R6) |
| env names `XKB_DEFAULT_*` behavior | `src/context-priv.c:150-225` | — |
| defaults evdev/pc105/us | `meson_options.txt` (build config) | R1 |

Hyprland's fallback-to-`us` must be cited from the held r46 entry (step 4, rows S318/S319), never re-claimed.

## 5. Smallest safe corrections (for the L1 freeze)

1. Scope the receipt equivalence: "with the five names the config yields passed explicitly, `xkbcli compile-keymap` invokes the same library call with the same flags as Hyprland's compile (both `xkb_keymap_new_from_names2`, TEXT_V2, COMPILE_NO_FLAGS); the two diverge only through environment-name handling and include-path environment".
2. State explicitly that Hyprland passes `""` (never NULL) for unset names and that its layout default `"us"` blocks env layout/variant/options; warn against `XKB_DEFAULT_RULES`/`XKB_DEFAULT_MODEL` only.
3. Pin the generic mechanics to libxkbcommon 1.13.2 source rows (new SOURCES rows) with the tag commit; keep host receipts to measured compile outcomes + the root path.
4. Cite the r46 fallback instead of re-deriving it; add the r46 entry as the held neighbour.
5. Make the live receipt reproducible as a recorded command transcript (rc + stdout + stderr), not a summary.

Impacted axes: coverage (the claim's sourced ground depends on pinning generic vs host sentences), quality (an equivalence claim wider than the evidence would fail a judge; r46's held fallback must stay cited).
