# From the `kb_*` names to a compiled keymap: which XKB names this host accepts

source: S340 - libxkbcommon 1.13.2 rules compiler, RMLVO matching and the ignored-name warnings (pin `.ufo/waves/round-48/fetch/libxkbcommon-rules.c`)
source: S341 - libxkbcommon 1.13.2 context, the default include-path order and the system root (pin `.ufo/waves/round-48/fetch/libxkbcommon-context.c`)
source: S342 - xkeyboard-config 2.48 symbols/br, the Brazil layout's default section and its named variants (pin `.ufo/waves/round-48/fetch/xkeyboard-config-symbols-br`)
verified-at: 2026-10-26
recheck: on-release
ground: the RMLVO-to-keymap compile on this host, measured read-only with xkbcli 1.13.2 against xkeyboard-config 2.48; held neighbours: the stored names and the fallback in hyprland-input-devices-r46.md (rows S318-S319)
Lane: mado-shokunin. Round: 48. Recheck trigger: libxkbcommon or xkeyboard-config changes on the host; re-run `xkbcli compile-keymap` for the names and re-hash the keymap.

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| which names the config hands the compiler | step 1 | sourced (held rows S318-S319) |
| how a layout name becomes a symbols section | steps 2 and 4 | sourced |
| which include paths are searched, in which order | step 3 | sourced |
| which unknown names fail the compile and which are dropped | step 5 and the host matrix | sourced, executed |
| how a failed compile maps onto Hyprland's `us` fallback | step 6 | sourced (held) |

## The chain, step by step

1. The config names. Hyprland stores `kb_layout`, `kb_variant`, `kb_options` and `kb_rules` as strings (Hyprland-ConfigValues.cpp:271-279), so the compiler is handed RMLVO names, not files.
2. Rules first. The rules compiler matches every layout, variant and option name against the ruleset and logs the unmatched ones (libxkbcommon-rules.c:2048-2066).
3. Include paths. The compile searches `$XDG_CONFIG_HOME/xkb`, `$HOME/.config/xkb`, `$HOME/.xkb`, the extra path and then the system root (libxkbcommon-context.c:243-280), so a user symbols file can shadow the packaged one.
4. Symbols section. The layout name selects `symbols/<layout>` and the variant selects a `xkb_symbols "<variant>"` section inside it; `br`'s default is the abnt2 section (xkeyboard-config-symbols-br:3-4).
5. Failure or warning. A missing symbols file or section aborts the compile; an unmatched option is dropped with a logged warning (libxkbcommon-rules.c:2063).
6. Hyprland's fallback. When the compile fails, the keyboard falls back to `us` rather than keeping the rejected names (Hyprland-IKeyboard.cpp:101-116); the round-46 note holds the full step.

## Observations (upstream bytes, read-only)

- The warning is one of four sibling messages, each emitted only for an unmatched non-empty name: `Unrecognized RMLVO option`, libxkbcommon-rules.c:2063.
- An unmatched layout is logged with the same shape: `Unrecognized RMLVO layout`, libxkbcommon-rules.c:2053.
- The user include paths accept an empty `XDG_CONFIG_HOME` and report it: `Accept empty string, which may be unintentional and should be reported`, libxkbcommon-context.c:255.
- When `XDG_CONFIG_HOME` is unset the fallback is announced in the source: `XDG_CONFIG_HOME fallback is $HOME/.config/`, libxkbcommon-context.c:263.
- The Brazil layout's own header says what it is: `Keyboard layouts for Brazil.`, xkeyboard-config-symbols-br:1.
- The default section is named: `xkb_symbols "abnt2"`, xkeyboard-config-symbols-br:4.

## This host

The host config's names are layout `br` and options `compose:caps`. A read-only run of `xkbcli compile-keymap --layout br --options compose:caps` on xkbcli 1.13.2 (libxkbcommon 1.13.2-1) exits rc 0 and prints a 2090-line keymap whose sha256 is efd487a39920152354f0... (full digest and line count in `.ufo/waves/round-48/receipts/xkb-live.txt`).
The negative matrix, same receipt: unknown layout `--layout zz` rc 1 (XKB-338).
An unknown variant `--layout br --variant nope` rc 1 (XKB-661).
An unknown option `--layout br --options nope:nope` rc 0 with XKB-595 "Unrecognized RMLVO option ... was ignored".

## Symptom to cause

| symptom | cause | check |
|---|---|---|
| a keyboard prints `us` though the config names `br` | the compile failed and the fallback kept the old names | step 6; run `xkbcli compile-keymap --layout br` |
| a variant name is silently ignored | the variant does not exist in that layout | step 5 and the XKB-661 line in the receipt |

## Limits

- The compile is read-only: it says what libxkbcommon would build, not what the running compositor has loaded; a runtime `hyprctl switchxkblayout` is not observed here.
- No compositor mutation and no input injection were performed; the host's `hyprctl devices -j` keymap fields are the round-46 join's ground, not this entry's.
- The rules path is the packaged one; a user rules file under `$XDG_CONFIG_HOME/xkb` changes the result and is [UNK] for this host.
