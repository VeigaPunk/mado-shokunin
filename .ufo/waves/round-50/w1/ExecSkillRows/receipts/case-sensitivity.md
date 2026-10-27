# ExecSkillRows r50 — F1: the section's 'rc 2 means NoSymbol' read vs Hyprland's case-insensitive resolution
# libxkbcommon 1.13.2, ctypes xkb_keysym_from_name(name, flags): 0 = XKB_KEYSYM_NO_FLAGS, 1 = XKB_KEYSYM_CASE_INSENSITIVE;
# xkb_keysym_get_name(value) gives the canonical spelling the header carries.
# Hyprland: exact then CI (KeybindManager.cpp:710-711), either matches (:724). how-to-type: NO_FLAGS only (how-to-type.c:286).
# host binds (hyprctl binds -j, read-only): total=192, keysym-named rows=142, distinct keysym names=58
exact_fail_distinct=14/58; CI-resolves=14; fail_both=0
keysym-named bind rows resolving ONLY case-insensitively: 53 of 142
per-name rows: {"BACKSPACE":3,"COMMA":5,"DELETE":1,"DOWN":4,"ESCAPE":1,"LEFT":5,"PERIOD":1,"PRINT":4,"RETURN":3,"RIGHT":5,"SLASH":1,"SPACE":5,"TAB":11,"UP":4}

## the section's own first read, verbatim (mado-keysym.py how-to-type --keymap FILE --disable-compose --keysym NAME)
# name as stored in the live bind | rc | lower-case rc | canonical spelling | canonical rc
BACKSPACE  rc=2 | backspace  rc=2 | BackSpace      rc=0 keysym: BackSpace (0xff08)
COMMA      rc=2 | comma      rc=0 | comma          rc=0 keysym: comma (0x002c)
DELETE     rc=2 | delete     rc=2 | Delete         rc=0 keysym: Delete (0xffff)
DOWN       rc=2 | down       rc=2 | Down           rc=0 keysym: Down (0xff54)
ESCAPE     rc=2 | escape     rc=2 | Escape         rc=0 keysym: Escape (0xff1b)
LEFT       rc=2 | left       rc=2 | Left           rc=0 keysym: Left (0xff51)
PERIOD     rc=2 | period     rc=0 | period         rc=0 keysym: period (0x002e)
PRINT      rc=2 | print      rc=2 | Print          rc=0 keysym: Print (0xff61)
RETURN     rc=2 | return     rc=2 | Return         rc=0 keysym: Return (0xff0d)
RIGHT      rc=2 | right      rc=2 | Right          rc=0 keysym: Right (0xff53)
SLASH      rc=2 | slash      rc=0 | slash          rc=0 keysym: slash (0x002f)
SPACE      rc=2 | space      rc=0 | space          rc=0 keysym: space (0x0020)
TAB        rc=2 | tab        rc=2 | Tab            rc=0 keysym: Tab (0xff09)
UP         rc=2 | up         rc=2 | Up             rc=0 keysym: Up (0xff52)

lower-case retry does NOT resolve 10 of 14 CI-only names (canonical spelling is not the lower-case form); canonical resolves 14/14

## a working host bind the row mislabels: key "SLASH" (1 row, modmask 65, dispatcher exec)
# row 7 rule: 'SLASH and slash both work'; row 7 first read: rc 2 means NoSymbol, next step 'fix the spelling'.
# measured: --keysym SLASH rc 2 (no output), --keysym slash rc 0 with the AB11 level-1 row -> the row's first read contradicts its rule
