# ExecRefKeysymB — C1 reference B (independent how-to-type implementation)

Seat: `.ufo/waves/round-49/w1/ExecRefKeysymB/` · scratch `/fast/scratch/hyaku/mado-r49/ExecRefKeysymB/` (deleted at the end).
Wave w1 (BUILD) · base `03e4ae76aff7a4be59cb69970dd553baa319695a` · no tracked file touched, no git/jj mutation,
no pacman, no compositor call beyond the allowed read-only ones (none were needed).

## 1. What shipped

`keysym_ref.py` — 2368 lines, Python 3 standard library only (`re`, `sys`), no process, no socket,
writes nothing (stdout/stderr only). sha256 `656fbd43ec9ec3d57a2ec741f3f285461ac622e66a20fab9da0a91e552cfb3c0`.

    parse_keymap(text)        -> Keymap          # a compile-keymap text dump, v1/v2, pretty or not
    keysym_from_arg(arg)      -> int | None      # how-to-type's --keysym resolution; None == the rc 2 refusal
    how_to_type(keymap, ks)   -> (stdout, rc)    # the judge's stdout verbatim and 0
    main(argv) / __main__     -> the contract CLI: --keymap=FILE --disable-compose --keysym ARG

It reconstructs, from the serialized keymap alone, everything `xkbcli how-to-type --disable-compose` reads:
keycode range and key names, group names, per-key groups and levels, explicit and automatic key types,
type entries with their effective modifier masks, the virtual-modifier → real-modifier mapping (explicit
declarations, `modifier_map`, interpretation-derived vmodmap, and the format-2 canonical self-mapping),
`xkb_keymap_key_get_mods_for_level` including its level-0 special case and entry deactivation, and the
`print_combo` renderer (byte-exact padding, real-mod-then-vmod name order).

`gen_tables.py` regenerates the three embedded table blocks from the pinned sources
(`ks_tables.h`, `keysym-case-mappings.c`, `keysym-utf.c`); it is provenance only, not needed to run the tool.

    c1-reference-b/
      keysym_ref.py  gen_tables.py  fixtures/  receipts/  (this report one level up)

## 2. Behaviour of the judge, as implemented

- Argument: keysym name first (`xkb_keysym_from_name` with no flags: exact table hit, `U<hex>` with
  ISO-8859-1 normalisation, `0x<hex>` ≤ 0x1fffffff, and the `XF86_` → `XF86` retry), then a base-10
  number; any result of 0, or an unparseable argument, is the rc 2 refusal (`tools/how-to-type.c:269`,
  `:286`, `:291`, `:293`).
- Output: `keysym: <canonical name> (0x%04x)`, blank line, `=== Direct access ===`, blank line, the
  fixture header, then one row per (keycode, layout, level, mask) in keycode order, layout order,
  level order, entry order (`tools/how-to-type.c:625`, `:527`).
- A row is emitted only for a level holding exactly one keysym equal to the requested value; levels with
  zero or several keysyms never produce a row, but their first keysym still drives automatic type
  selection.
- Masks are the *effective* masks of each active type entry (`src/keymap.c:494`), and the modifier column
  prints every modifier whose canonical mask is contained in the row mask, real modifiers first in
  `Shift, Lock, Control, Mod1..Mod5` order, then virtual modifiers in declaration order
  (`tools/how-to-type.c:532`).
- The CLI refuses (exit 2, empty stdout) without `--disable-compose` or `--keysym`, as the contract
  requires; it reproduces getopt's `--keymap`/`--keymap=` asymmetry and rejects `--keysym=ARG` (see §5).

## 3. Evidence (all byte-exact stdout + exit status, judge vs reference)

24898 comparisons, 0 mismatched. Full per-keymap compile commands, digests and counts:
`receipts/details/`, summary and reproduce steps: `receipts/diff.txt`.

| run | what | pairs | mismatched |
|---|---|---|---|
| run9 | 60 RMLVO keymaps × 150 random (keymap, keysym) pairs, seed 4907 | 9000 | 0 |
| run11 | 40 RMLVO keymaps × 150, seed 4909 (independent draw) | 6000 | 0 |
| run10 | 8 RMLVO keymaps × 50 through the shipped file as a program | 400 | 0 |
| ex3 | every header keysym name (2638) + canonical names of unnamed syms, 3 keymaps | 7916 | 0 |
| sweep | 9 fixed keymaps: 2 RMLVO host ones, `--no-pretty`, `--format 1`, 4 crafted fixtures | 1520 | 0 |
| probe | the 5 crafted fixtures only | 59 | 0 |
| host | the claim's `br` + `compose:caps` sample (`slash`, `Return`, `nosuchsym`) | 3 | 0 |

Keymaps were compiled at run time by the pinned `/usr/lib/xkbcommon/xkbcli-compile-keymap` from RMLVO
names drawn from `xkbcli list` (184 models, 598 layout/variant pairs over 99 layouts, 217 options;
1–3 layouts, 0–4 options per keymap) in `env -i PATH=/usr/bin` with `HOME`/`XDG_*` inside the scratch
tree. Every judge call used `--keymap=FILE --disable-compose --keysym ARG`. Pins (`receipts/pins.txt`):
how-to-type `f6c0b122…`, compile-keymap `43b924f6…`, `/usr/bin/xkbcli` `af42b0e6…`, keysyms header
`13023369…` (all three identical to the claim), plus sha256 for all 22 fetched libxkbcommon files at
`xkbcommon-1.13.2` tag URLs.

`receipts/host-sample.txt` reproduces the claim's sample exactly: `slash` → AD01 levels 3 and 4 with
`[ Mod5 LevelThree ]`, `[ Lock Mod5 LevelThree ]`, `[ Shift Mod5 LevelThree ]`,
`[ Shift Lock Mod5 LevelThree ]` and AB11 level 1 `[ ]`; `Return` → RTRN level 1; `nosuchsym` → rc 2.

## 4. Surprises (each with its source line; quotes re-grepped by `receipts/verify-quotes.sh`)

Full text in `receipts/notes.md`; verification output `receipts/verify-quotes.txt` (`all quotes located`).

1. **`printf("%-20s")` pads by bytes.** Layout names carry non-ASCII (e.g. `French (Ergo‑L)` with
   U+2011), so a character-based pad loses two spaces (`tools/how-to-type.c:527`). 102/9000 pairs failed
   on this before the padding became byte-based, and the CLI now writes UTF-8 bytes
   (`sys.stdout.buffer`), not text.
2. **The judge always parses the file as keymap format 2**, whatever produced it, so a virtual modifier
   left without a mapping takes its canonical self-mapping (`src/xkbcomp/keymap.c:469`); only an explicit
   `virtual_modifiers M = none;` keeps it at zero. A `--format 1` dump, where such modifiers print bare,
   still yields no `Hyper`/`ScrollLock` noise — my first reading of the v1 text produced 102 mismatches
   until this was modelled.
3. **An unmapped virtual modifier prints on every row.** With mapping 0 the containment test
   `(mask & mod_mask) != mod_mask` is always false (`tools/how-to-type.c:532`, `src/keymap.h:676`,
   `src/xkbcomp/keymap.c:25`), so `[ Shift Foo ]` appears for `virtual_modifiers Foo = none;` (probe
   `fixtures/A2.km`, judge and reference identical).
4. **`--keymap FILE` with a space is not a file.** The long option's argument is *optional*
   (`tools/how-to-type.c:171`), so `--keymap FILE --disable-compose --keysym ARG` makes the judge exit 2
   with "missing positional parameter". The contract text writes the space form; the frozen counter must
   write `--keymap=FILE` or it measures refusals against refusals.
5. **`NoSymbol` is not a usable argument**: it resolves to 0, which is also the "failed to convert"
   sentinel (`tools/how-to-type.c:269`), so `--keysym NoSymbol` is rc 2 — and the `%#06x` of zero
   (`000000`, no `0x`) is unreachable.
6. **Automatic key types depend on keysym case**, so a two-level key is `ALPHABETIC` (masks `Shift` and
   `Lock`) or `TWO_LEVEL` (mask `Shift` only) purely by keysyms (`src/xkbcomp/symbols.c:1594`,
   `src/keysym-case-mappings.c:624`). The keysym header cannot supply this: it gives name→value only —
   its 2638 `#define XKB_KEY_` lines are exactly the 2638 names of the library's table (verified
   set-equal, values equal; the claim's 2659 includes 21 comment occurrences) — while line 1 of the
   output needs the *canonical* name (2505 canonical values, 133 alias extras). Both tables are
   embedded, so the tool needs no header at run time.
7. **Trailing `NoSymbol` levels are dropped at parse time** (`src/xkbcomp/symbols.c:842`), then the level
   array is resized to the type (`…:1767`), so a 3-symbol key is `FOUR_LEVEL` and the dump shows four
   entries with a padded `NoSymbol`; the width for automatic typing must come from the dumped list.
8. **Level-1 type entries without `preserve` are never serialized** (`src/xkbcomp/keymap-dump.c:342`) —
   harmless here only because the judge reads the same serialized text.
9. **vmodmap is bound only at group 0 / level 0 for `useModMapMods=level1` interprets**
   (`src/xkbcomp/keymap.c:209`). My first version dropped the group test and made `RALT` bind
   `LevelThree` to Mod1, printing `Mod1 Alt Meta` on rows that must show only `Mod5 LevelThree`
   (43/3600 pairs).

Two implementation-scale observations for the freeze: the reference needs ~28–60 ms to parse an 80 KB
keymap and ~0.3 ms to render a query, but a full `python3 keysym_ref.py …` invocation costs ~0.39 s on
this host, ~0.34 s of which is interpreter start-up, so ~3600 CLI pairs ≈ 23 minutes; driving
`parse_keymap` once per fixture and calling `how_to_type` per keysym is ~1000× cheaper.

## 5. Deliberate divergences from the judge (the counter must stay inside the contract)

1. No `--disable-compose` (or no `--keysym`): the contract requires exit 2, the judge would print the
   Compose section / reinterpret ARG. Every judged invocation must pass both flags.
2. `--keymap FILE` (space) and `--keysym=ARG`: judge exit 2, reference exit 2 — reproduced on purpose.
3. A stdin keymap (`--keymap` without `=`, one positional) and RMLVO compilation are out of contract;
   the reference refuses with exit 2 (the judge would compile defaults).
4. `--help`/`-h`: both print usage on stdout with exit 0, but the line embeds `argv[0]`, so the two
   cannot be byte-identical; do not put it in the counter.

## 6. Risks / recommendations for the frozen counter

- **Freeze the invocation form**: `--keymap=FILE --disable-compose --keysym ARG` as separate argv
  entries, judge and tool both. Anything else measures the refusal path (§4 item 4, §5).
- **Freeze the keymap production**: pinned `compile-keymap` from RMLVO, default formats, with
  `env -i PATH=/usr/bin HOME=<scratch>/home XDG_CONFIG_HOME=<scratch>/home/.config
  XDG_CACHE_HOME=<scratch>/home/.cache`. `--no-pretty` and `--format 1` files also pass (§3 sweep), so a
  format nonce is safe; hand-written raw XKB is not (the tool consumes compiled text).
- **Compare bytes, not text**: rows contain non-ASCII layout names, and byte-vs-character padding is
  exactly the trap in §4 item 1. Compare `stdout` bytes and the exit status only; stderr strings differ
  by program name.
- **Nonce keysyms**: draw from `/usr/include/xkbcommon/xkbcommon-keysyms.h` names (all 2638 pass
  exhaustively), from each fixture's own symbols (rows guaranteed), and include refusals
  (`nosuchsym`, `U+0041`, `0xGG`, `NoSymbol`, oversized decimals) — the reference reproduces all of them.
  Note `U+0041` is *not* a keysym name: `--keysym` mode has no Unicode-notation branch that accepts `+`.
- **Sanity floor for a verifier**: the host `br` + `compose:caps` sample (§3) is a one-command check that
  distinguishes a working reference from a vacuous one; the level structure (`[ ]` at level 1 and a
  non-empty mod list at levels 3/4) is what a stub would miss.
- Not covered by this seat (out of contract, must not be frozen in): Compose sequences, character /
  code-point interpretation, `--format 1` *input* to how-to-type, RMLVO keymap compilation by the tool,
  and any keymap text that `compile-keymap` cannot produce (e.g. a vmod explicitly mapped to a vmod bit
  is representable, but a raw include-based source is not).

## 7. Tooling and host hygiene

- No package install or upgrade, no pacman call, no network service beyond reading pinned tag URLs with
  `curl` (source pins only). `gcc` was used once, inside scratch, to confirm C's `%#06x` of zero prints
  `000000`; that binary never left scratch.
- xkbcli use was limited to `compile-keymap`, `how-to-type` and `list`, stdout only, in `env -i` with
  `HOME`/`XDG_*` under scratch. No compositor query was needed. No home state, no fleet-root file, no
  tracked lane file written; the only writes are the seat directory (its report at
  `.ufo/waves/round-49/w1/ExecRefKeysymB.md`) and the scratch tree, which has been removed
  (`rm -rf /fast/scratch/hyaku/mado-r49/ExecRefKeysymB`). Session material: receipts contain only
  generated keymap text, RMLVO names and libxkbcommon source fragments — no device names, window
  titles, monitor data or home listings.

## 8. Blockers

None. The one open question for the L1 is a contract decision, not an implementation gap: the tool
contract's `--keymap FILE` vs the judge's `--keymap=FILE` (§4 item 4). The reference matches the judge in
both cases, but only the `=` form exercises the capability.
