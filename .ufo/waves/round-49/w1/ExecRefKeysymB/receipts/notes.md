# behaviours that surprised the implementation — ExecRefKeysymB, round 49 w1

Every locator below is `grep -n` output over the pinned sources listed in
`receipts/pins.txt` (libxkbcommon tag `xkbcommon-1.13.2`, work tree rebuilt from
those files).  Quotes are ≤ 25 words.  `receipts/verify-quotes.sh` re-greps each
quote against the pinned file at the recorded line; its output is
`receipts/verify-quotes.txt`.

## N1 — `--keymap FILE` with a space is not a file argument

`tools/how-to-type.c:171`: `{"keymap", optional_argument, 0, OPT_KEYMAP},`

The long option takes an *optional* argument, so getopt only binds `--keymap=FILE`.
With `--keymap FILE --disable-compose --keysym ARG` the judge sees two
positionals and exits 2 with "missing positional parameter" (measured, see
`receipts/diff.txt` §"deliberate divergences").  The tool contract text writes
`--keymap FILE`; the frozen counter must use `=`, or every fixture compares a
refusal with a refusal and measures nothing.

## N2 — the keysym argument 0 is the failure sentinel, so `NoSymbol` is not a keysym

`tools/how-to-type.c:269`: `*keysym = XKB_KEY_NoSymbol;`
`tools/how-to-type.c:286`: `*keysym = xkb_keysym_from_name(argv[optind], XKB_KEYSYM_NO_FLAGS);`
`tools/how-to-type.c:293`: `ERROR: Failed to convert argument to keysym`

`NoSymbol` resolves to 0 through the name table, which is indistinguishable from
"unresolved", so `--keysym NoSymbol` exits 2 (measured).  Consequence for line 1
of the output: `%#06x` of 0 would print `000000` (C drops the `0x` prefix for
zero) but that branch is unreachable.

## N3 — a virtual modifier with no mapping is printed for *every* mask

`src/xkbcomp/keymap.c:25` (`has_unbound_vmods`), `src/keymap.h:676`
(`entry_is_active`), `tools/how-to-type.c:532`:
`if ((mask & mod_mask) != mod_mask)`

With `mod_mask == 0` the test is always false, so the modifier's name is printed
even for an empty mask.  Probe `fx/A2.xkb` (`virtual_modifiers Foo = none;`)
yields `[ Shift Foo ]` from judge and reference alike.

## N4 — the judge re-parses the file as keymap format 2, adding canonical vmods

`src/xkbcomp/keymap.c:469`:
`if (mod->mapping == 0 && !(keymap->mods.explicit_vmods & mask)) {`

how-to-type's `--format` default is format 2, so any virtual modifier the text
leaves at zero takes its canonical encoding (its own bit) — this is why a
`--format 1` dump, where such modifiers print bare, still does not make the
judge print them.  A modifier declared `= none` is explicit and keeps mapping
zero (N3 then applies).  Missing this rule produced 102 mismatches on
`--format 1` keymaps until it was implemented.

## N5 — automatic key types depend on the keysym *case*, so the header is not enough

`src/xkbcomp/symbols.c:1594` (`FindAutomaticType`), `src/keysym-case-mappings.c:624`
(`xkb_keysym_is_lower`).

A two-level key is `ALPHABETIC` (masks `Shift` and `Lock`) when the keysyms are
lower/upper and `TWO_LEVEL` (mask `Shift` only) otherwise, so the tool must
carry libxkbcommon's compressed case-mapping tables.  `/usr/include/xkbcommon/
xkbcommon-keysyms.h` supplies name→value only: its 2638 `#define XKB_KEY_` lines
(`grep -c '^#define XKB_KEY_'`; the claim's 2659 counts 21 further occurrences
inside comment examples) are exactly the 2638 names of `src/ks_tables.h`
(verified set-equal with equal values), but the header does not say which of
those names is *canonical* for one of the 2505 named values — and line 1 of the
judge's output prints the canonical name.  The tool therefore embeds
`ks_tables.h`'s two tables (2638 alias names, 2505 canonical names, 133 alias
extras).

## N6 — `printf("%-20s")` pads by bytes, not characters

`tools/how-to-type.c:527` (`print_combo`'s field widths) with a layout name such
as `French (Ergo‑L)`, whose U+2011 hyphen is three UTF-8 bytes: the judge emits
two fewer spaces than a character-based pad.  102 of the first 9000 sampled
pairs failed on exactly this before the padding became byte-based.

## N7 — trailing `NoSymbol` levels are dropped when symbols are parsed

`src/xkbcomp/symbols.c:842` (`/* Drop trailing NoSymbol */`),
`src/xkbcomp/symbols.c:1767` (`/* Always have as many levels as the type specifies. */`)

So a 3-symbol key is typed from width 3 (`FOUR_LEVEL`, four levels) and the
serializer appends the padded `NoSymbol`; a key written with four symbols whose
last is `NoSymbol` is width 3 as well.  The tool must take the width of the
*dumped* level list for implicitly typed keys, and must not treat a trailing
`NoSymbol` as a symbol of its own.

## N8 — level-1 type entries without `preserve` are not serialized

`src/xkbcomp/keymap-dump.c:342`: `Printing level 1 entries is redundant, it's the default,`

Harmless for this contract because the judge reads the same serialized text, but
it means a type's level-1 mask set must never be reconstructed from a keymap
file: only `map[...]` lines that survived serialization exist.

## N9 — the vmodmap contribution is group 0 / level 0 only for "level1" interprets

`src/xkbcomp/keymap.c:205`, `src/xkbcomp/keymap.c:209`:
`if ((group == 0 && level == 0) || !interp->level_one_only)`

Dropping the `group == 0` half made `RALT` (ISO_Level3_Shift in the second
layout group) bind `LevelThree` to Mod1, which printed `Mod1 Alt Meta` on rows
that must show only `Mod5 LevelThree`; 43 of the first 3600 pairs failed that
way.

## N10 — multi-keysym levels never produce a row

`tools/how-to-type.c` skips any level whose symbol count is not exactly one, so
`{ a, b }` levels only influence automatic type selection (via their first
symbol).  Probe `fx/D.xkb` covers this together with an interior `NoSymbol` and
a five-symbol key (whose automatic type fails and falls back to the first type
in the file, giving a single level).
