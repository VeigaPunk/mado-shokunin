# Targeted edge cases: host hyprlang 0.6.8 oracle vs the frozen reference

Each case: `oracle <case>.conf <8 names>` (host hyprlang 0.6.8, registrations copied from
Hyprland ConfigManager.cpp:481-628) and `python3 -I mado-devices.py --devices devices.json --config <case>.conf`
(reference sha256 b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b).
Oracle state cells: `s` = set by user, `d` = default, value shown; `scroll` = explicit flag + stored float.

| case | ref exit | unsupported | ref verdict | class | diverged |
| --- | --- | --- | --- | --- | --- |
| C00-normal-agree | 1 | 0 | DIFFER | MATCH | - |
| C01-first-key-not-name | 5 | 2 | NOT_COMPARED | DECLARED-UNMODELLED | blocks |
| C02-second-name | 5 | 2 | NOT_COMPARED | DECLARED-UNMODELLED | kb:kbdX; kb:kbdY; blocks |
| C03-bracket-then-name | 5 | 1 | NOT_COMPARED | DECLARED-UNMODELLED | blocks |
| C04-flat-key-outside | 5 | 1 | NOT_COMPARED | DECLARED-UNMODELLED | blocks |
| C05-flat-after-close | 5 | 1 | NOT_COMPARED | DECLARED-UNMODELLED | blocks |
| C06-space-bracket | 5 | 1 | NOT_COMPARED | DECLARED-UNMODELLED | blocks |
| C07-brackets-in-value | 1 | 0 | DIFFER | MATCH | - |
| C08-input-bracket | 1 | 0 | DIFFER | MATCH | - |
| C09-nested-block | 1 | 0 | DIFFER | MATCH | - |
| C10-hash-hash-end | 1 | 0 | DIFFER | MATCH | - |
| C11-triple-hash | 1 | 0 | DIFFER | MATCH | - |
| C12-hash-after-double | 1 | 0 | DIFFER | MATCH | - |
| C13-continuation-into-comment | 1 | 0 | DIFFER | MATCH | - |
| C14-final-continuation | 1 | 0 | DIFFER | BUG | kb:kbdX |
| C15-empty-rhs | 1 | 0 | DIFFER | MATCH | - |
| C16-scroll-1e-40 | 5 | 1 | NOT_COMPARED | MATCH | - |
| C17-scroll-0x10 | 5 | 1 | NOT_COMPARED | DECLARED-UNMODELLED | mouse:mouseA(ref -1.00 want 16.00) |
| C18-scroll-leading-space | 1 | 0 | DIFFER | MATCH | - |
| C19-scroll-plus-dot5e1 | 1 | 0 | DIFFER | MATCH | - |
| C20-scroll-1e39 | 5 | 1 | NOT_COMPARED | MATCH | - |
| C21-variable-after-use | 5 | 1 | NOT_COMPARED | DECLARED-UNMODELLED | kb:kbdX |
| C22-dollar-in-name | 5 | 2 | NOT_COMPARED | DECLARED-UNMODELLED | blocks |
| C23-final-continuation-no-nl | 1 | 0 | DIFFER | MATCH | - |
| C24-final-continuation-then-blank | 1 | 0 | DIFFER | MATCH | - |
| C25-hash-in-comment-order | 1 | 0 | DIFFER | MATCH | - |
| C26-scroll-inf | 5 | 1 | NOT_COMPARED | DECLARED-UNMODELLED | mouse:mouseA(ref -1.00 want 100.00) |
| C27-scroll-nan | 5 | 1 | NOT_COMPARED | DECLARED-UNMODELLED | mouse:mouseA(ref -1.00 want nan) |
| C28-scroll-trailing-junk | 1 | 0 | DIFFER | MATCH | - |
| C29-firstkey-then-name-then-key | 5 | 3 | NOT_COMPARED | DECLARED-UNMODELLED | kb:kbdX; blocks |
| C30-firstkey-no-name | 5 | 1 | NOT_COMPARED | DECLARED-UNMODELLED | blocks |
| C31-double-bracket-lhs | 1 | 0 | DIFFER | MATCH | - |
| C32-space-bracket-key | 1 | 0 | DIFFER | MATCH | - |
| C33-input-space-bracket | 1 | 0 | DIFFER | MATCH | - |
| C34-flat-name-stray-close | 1 | 0 | DIFFER | MATCH | - |
| C35-continuation-swallows-brace | 1 | 0 | DIFFER | MATCH | - |
| E01-second-name-only | 5 | 1 | NOT_COMPARED | DECLARED-UNMODELLED | blocks |
| E02-bare-hyprlang-comment | 5 | 1 | NOT_COMPARED | MATCH | - |
| E03-hyprlang-if-skip | 5 | 2 | NOT_COMPARED | DECLARED-UNMODELLED | kb:kbdX; blocks |
| E04-duplicate-blocks | 1 | 0 | DIFFER | MATCH | - |
| E05-global-scroll | 1 | 0 | DIFFER | MATCH | - |
| E06-scroll-clamp-200 | 1 | 0 | DIFFER | MATCH | - |
| E07-flat-name-two-line | 1 | 0 | DIFFER | MATCH | - |
| E08-global-inside-block | 1 | 0 | DIFFER | MATCH | - |
| E09-nested-then-key | 1 | 0 | DIFFER | MATCH | - |
| E10-braces-on-one-line | 1 | 0 | DIFFER | MATCH | - |
| E11-crlf | 1 | 0 | DIFFER | MATCH | - |
| E12-close-with-comment | 1 | 0 | DIFFER | MATCH | - |
| E13-empty-sentinel | 1 | 0 | DIFFER | MATCH | - |
| E14-stray-close | 1 | 0 | DIFFER | MATCH | - |
| E15-unclosed-block | 1 | 0 | DIFFER | MATCH | - |
| E16-empty-name | 1 | 0 | DIFFER | MATCH | - |
| E17-block-key-not-modelled | 1 | 0 | DIFFER | MATCH | - |

## C00-normal-agree

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = de$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## C01-first-key-not-name

config (`cat -A`):
```
device {$
    kb_layout = de$
    name = kbdX$
}$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C01-first-key-not-name.conf at line 2: special category's first value must be the key. Key for <device> is <name>" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set=""

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=0 stale=0 unsupported=2 verdict=NOT_COMPARED
```

## C02-second-name

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = de$
    name = kbdY$
    kb_variant = intl$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdY" exists=1 set="kb_layout,kb_variant"

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=s:de kb_variant=s:intl kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=2 verdict=NOT_COMPARED
```

## C03-bracket-then-name

config (`cat -A`):
```
device[kbdX]:name = kbdY$
device[kbdX]:kb_layout = de$
device[kbdY]:kb_variant = intl$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=2 | ORACLE_CAT: idx=0 name="kbdY" exists=1 set="kb_variant" | ORACLE_CAT: idx=1 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=s:intl kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=yes layout="us" variant="intl" options="" model="" rules="" kb_file=- differ=layout,variant verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEV_BLOCK: name="kbdY" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=2 stale=0 unsupported=1 verdict=NOT_COMPARED
```

## C04-flat-key-outside

config (`cat -A`):
```
device:kb_layout = de$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C04-flat-key-outside.conf at line 1: special category's first value must be the key. Key for <device> is <name>" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="0" exists=1 set=""

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=0 stale=0 unsupported=1 verdict=NOT_COMPARED
```

## C05-flat-after-close

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = de$
}$
device:kb_variant = intl$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C05-flat-after-close.conf at line 5: special category's first value must be the key. Key for <device> is <name>" | ORACLE_NKEYS: n=2 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout" | ORACLE_CAT: idx=1 name="0" exists=1 set=""

- "kbdX": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=1 verdict=NOT_COMPARED
```

## C06-space-bracket

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = de$
}$
device [kbdX]$
device:kb_variant = intl$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C06-space-bracket.conf at line 5: Invalid config line\nConfig error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C06-space-bracket.conf at line 6: special category's first value must be the key. Key for <device> is <name>" | ORACLE_NKEYS: n=2 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout" | ORACLE_CAT: idx=1 name="0" exists=1 set=""

- "kbdX": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=1 verdict=NOT_COMPARED
```

## C07-brackets-in-value

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = de[foo]$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:de[foo] kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de[foo]" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## C08-input-bracket

config (`cat -A`):
```
input[x]:kb_layout = de$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=0

- "kbdX": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="de" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="de" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=0 stale=0 unsupported=0 verdict=DIFFER
```

## C09-nested-block

config (`cat -A`):
```
misc {$
    device {$
        name = kbdX$
        kb_layout = de$
    }$
}$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C09-nested-block.conf at line 3: config option <misc:device:name> does not exist.\nConfig error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C09-nested-block.conf at line 4: config option <misc:device:kb_layout> does not exist." | ORACLE_NKEYS: n=0

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=0 stale=0 unsupported=0 verdict=DIFFER
```

## C10-hash-hash-end

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = de ##$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:de # kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de #" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## C11-triple-hash

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = de ###$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:de ## kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de ##" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## C12-hash-after-double

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_variant = a##b#c$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_variant"

- "kbdX": kb_layout=d:us kb_variant=s:a#b kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="us" variant="a#b" options="" model="" rules="" kb_file=- differ=layout,variant verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## C13-continuation-into-comment

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = de \$
# tail comment$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## C14-final-continuation

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = de \$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C14-final-continuation.conf: Last line ends with backslash\nConfig error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C14-final-continuation.conf: Unclosed category at EOF" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set=""

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## C15-empty-rhs

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout =$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s: kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## C16-scroll-1e-40

config (`cat -A`):
```
device {$
    name = mouseA$
    scroll_factor = 1e-40$
}$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C16-scroll-1e-40.conf at line 3: failed parsing a float: stof" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="mouseA" exists=1 set=""

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=yes scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="mouseA" keys=0 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=1 verdict=NOT_COMPARED
```

## C17-scroll-0x10

config (`cat -A`):
```
device {$
    name = mouseA$
    scroll_factor = 0x10$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="mouseA" exists=1 set="scroll_factor"

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=1 float=16
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=yes scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="mouseA" keys=0 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=1 verdict=NOT_COMPARED
```

## C18-scroll-leading-space

config (`cat -A`):
```
device {$
    name = mouseA$
    scroll_factor =  1.5$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="mouseA" exists=1 set="scroll_factor"

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=1 float=1.5
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=yes scroll_factor=1.50 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="mouseA" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## C19-scroll-plus-dot5e1

config (`cat -A`):
```
device {$
    name = mouseA$
    scroll_factor = +.5e1$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="mouseA" exists=1 set="scroll_factor"

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=1 float=5
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=yes scroll_factor=5.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="mouseA" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## C20-scroll-1e39

config (`cat -A`):
```
device {$
    name = mouseA$
    scroll_factor = 1e39$
}$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C20-scroll-1e39.conf at line 3: failed parsing a float: stof" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="mouseA" exists=1 set=""

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=yes scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="mouseA" keys=0 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=1 verdict=NOT_COMPARED
```

## C21-variable-after-use

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = $layout$
}$
$layout = de$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:$layout kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=0 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=1 verdict=NOT_COMPARED
```

## C22-dollar-in-name

config (`cat -A`):
```
device {$
    name = kbd$X$
    kb_layout = de$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbd$X" exists=1 set="kb_layout"

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=0 stale=0 unsupported=2 verdict=NOT_COMPARED
```

## C23-final-continuation-no-nl

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = de \
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C23-final-continuation-no-nl.conf: Last line ends with backslash\nConfig error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C23-final-continuation-no-nl.conf: Unclosed category at EOF" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set=""

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=0 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## C24-final-continuation-then-blank

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = de \$
$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C24-final-continuation-then-blank.conf: Unclosed category at EOF" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## C25-hash-in-comment-order

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = de##x#y$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:de#x kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de#x" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## C26-scroll-inf

config (`cat -A`):
```
device {$
    name = mouseA$
    scroll_factor = inf$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="mouseA" exists=1 set="scroll_factor"

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=1 float=inf
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=yes scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="mouseA" keys=0 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=1 verdict=NOT_COMPARED
```

## C27-scroll-nan

config (`cat -A`):
```
device {$
    name = mouseA$
    scroll_factor = nan$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="mouseA" exists=1 set="scroll_factor"

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=1 float=nan
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=yes scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="mouseA" keys=0 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=1 verdict=NOT_COMPARED
```

## C28-scroll-trailing-junk

config (`cat -A`):
```
device {$
    name = mouseA$
    scroll_factor = 1.5x$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="mouseA" exists=1 set="scroll_factor"

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=1 float=1.5
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=yes scroll_factor=1.50 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="mouseA" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## C29-firstkey-then-name-then-key

config (`cat -A`):
```
device {$
    kb_layout = de$
    name = kbdX$
    kb_variant = intl$
}$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C29-firstkey-then-name-then-key.conf at line 2: special category's first value must be the key. Key for <device> is <name>" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_variant"

- "kbdX": kb_layout=d:us kb_variant=s:intl kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=0 stale=0 unsupported=3 verdict=NOT_COMPARED
```

## C30-firstkey-no-name

config (`cat -A`):
```
device {$
    kb_layout = de$
}$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C30-firstkey-no-name.conf at line 2: special category's first value must be the key. Key for <device> is <name>" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="0" exists=1 set=""

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=0 stale=0 unsupported=1 verdict=NOT_COMPARED
```

## C31-double-bracket-lhs

config (`cat -A`):
```
device[a][b]:kb_layout = de$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="a][b" exists=1 set="kb_layout"

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="a][b" keys=1 verdict=NO_SUCH_DEVICE
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=1 unsupported=0 verdict=DIFFER
```

## C32-space-bracket-key

config (`cat -A`):
```
device [kbdX]:kb_layout = de$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C32-space-bracket-key.conf at line 1: config option <device :kb_layout> does not exist." | ORACLE_NKEYS: n=0

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=0 stale=0 unsupported=0 verdict=DIFFER
```

## C33-input-space-bracket

config (`cat -A`):
```
input [x]:kb_layout = de$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C33-input-space-bracket.conf at line 1: config option <input :kb_layout> does not exist." | ORACLE_NKEYS: n=0

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=0 stale=0 unsupported=0 verdict=DIFFER
```

## C34-flat-name-stray-close

config (`cat -A`):
```
device:name = kbdX$
}$
device:kb_layout = de$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C34-flat-name-stray-close.conf at line 2: Stray category close" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## C35-continuation-swallows-brace

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = de \$
}$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/C35-continuation-swallows-brace.conf: Unclosed category at EOF" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:de} kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de}" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## E01-second-name-only

config (`cat -A`):
```
device {$
    name = kbdX$
    name = kbdY$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdY" exists=1 set=""

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=0 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=1 verdict=NOT_COMPARED
```

## E02-bare-hyprlang-comment

config (`cat -A`):
```
#hyprlang$
device {$
    name = kbdX$
    kb_layout = de$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=1 verdict=NOT_COMPARED
```

## E03-hyprlang-if-skip

config (`cat -A`):
```
#hyprlang if $NOSUCHVAR$
device {$
    name = kbdX$
    kb_layout = de$
}$
#hyprlang endif$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=0

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=2 verdict=NOT_COMPARED
```

## E04-duplicate-blocks

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = de$
}$
device {$
    name = kbdX$
    kb_layout = fr$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:fr kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="fr" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## E05-global-scroll

config (`cat -A`):
```
input:scroll_factor = 2.0$
device {$
    name = mouseA$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="mouseA" exists=1 set=""

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=yes scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="mouseA" keys=0 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## E06-scroll-clamp-200

config (`cat -A`):
```
device {$
    name = mouseA$
    scroll_factor = 200$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="mouseA" exists=1 set="scroll_factor"

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=1 float=200
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=yes scroll_factor=100.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="mouseA" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## E07-flat-name-two-line

config (`cat -A`):
```
device:name = kbdX$
device:kb_layout = de$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## E08-global-inside-block

config (`cat -A`):
```
device {$
    name = kbdX$
    input:kb_layout = de$
}$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/E08-global-inside-block.conf at line 3: config option <device:input:kb_layout> does not exist." | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set=""

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=0 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## E09-nested-then-key

config (`cat -A`):
```
device {$
    name = kbdX$
    foo {$
    }$
    kb_variant = intl$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_variant"

- "kbdX": kb_layout=d:us kb_variant=s:intl kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="us" variant="intl" options="" model="" rules="" kb_file=- differ=layout,variant verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## E10-braces-on-one-line

config (`cat -A`):
```
device { name = kbdX }$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=0

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=0 stale=0 unsupported=0 verdict=DIFFER
```

## E11-crlf

config (`cat -A`):
```
device {^M$
    name = kbdX^M$
    kb_layout = de^M$
}^M$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## E12-close-with-comment

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = de$
} # done$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## E13-empty-sentinel

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_variant = [[EMPTY]]$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_variant"

- "kbdX": kb_layout=d:us kb_variant=s: kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## E14-stray-close

config (`cat -A`):
```
}$
device {$
    name = kbdX$
    kb_layout = de$
}$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/E14-stray-close.conf at line 1: Stray category close" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## E15-unclosed-block

config (`cat -A`):
```
device {$
    name = kbdX$
    kb_layout = de$
```

oracle: ORACLE_PARSE: error=1 message="Config error in file /fast/scratch/hyaku/mado-r46/ExecHyprlangOracleB/work/E15-unclosed-block.conf: Unclosed category at EOF" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="kbdX" exists=1 set="kb_layout"

- "kbdX": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=yes layout="de" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="kbdX" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=1 differ=1 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

## E16-empty-name

config (`cat -A`):
```
device {$
    name =$
    kb_layout = de$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="" exists=1 set="kb_layout"

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "mouseA": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=no scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="" keys=1 verdict=NO_SUCH_DEVICE
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=1 unsupported=0 verdict=DIFFER
```

## E17-block-key-not-modelled

config (`cat -A`):
```
device {$
    name = mouseA$
    sensitivity = 0.5$
    kb_layout = de$
}$
```

oracle: ORACLE_PARSE: error=0 message="" | ORACLE_NKEYS: n=1 | ORACLE_CAT: idx=0 name="mouseA" exists=1 set="kb_layout,sensitivity"

- "kbdX": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbdY2": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "kbd$X": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "0": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>
- "mouseA": kb_layout=s:de kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=-1
- "hl-virtual-keyboard-1": kb_layout=d:us kb_variant=d kb_options=d kb_model=d kb_rules=d kb_file=d scroll=explicit=0 float=<nullptr>

reference:
```
MADO_DEV_KEYBOARD: name="kbdX" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="kbdY" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER
MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-1" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
MADO_DEV_MOUSE: name="mouseA" block=yes scroll_factor=-1.00 reported=1.00 verdict=DIFFER
MADO_DEV_MOUSE: name="touchpadB" block=no scroll_factor=-1.00 reported=-1.00 verdict=AGREE
MADO_DEV_BLOCK: name="mouseA" keys=1 verdict=MATCHED
MADO_DEVICES: keyboards=3 agree=0 differ=2 fallback=0 virtual=1 mice=2 mice_differ=1 blocks=1 stale=0 unsupported=0 verdict=DIFFER
```

