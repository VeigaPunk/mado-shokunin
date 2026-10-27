# ExecRefKeysymA — C1 reference A: draft `tools/mado-keysym.py`

Round 49 / wave w1 (BUILD) / lane `mado-shokunin`, base `03e4ae76aff7a4be59cb69970dd553baa319695a`.
Claim: C1 operability (`tools/mado-keysym.py`, which key and modifiers type a keysym).

status: **delivered** — the draft is at
`.ufo/waves/round-49/w1/ExecRefKeysymA/mado-keysym.py` (never at the tracked path; the L1 is the only
integrator). It is a second, independent reference implementation of the C1 contract, written from
the pinned libxkbcommon 1.13.2 sources; it is not derived from any sibling seat's draft.

## 1. Deliverable and contract

| item | value |
|---|---|
| draft tool | `.ufo/waves/round-49/w1/ExecRefKeysymA/mado-keysym.py`, 1999 lines, 92 144 B, sha256 `dcc13cce3b7134946208116cd98599fb8f56a2b81fc6f26b9598ac5429b40265` |
| generator of the embedded tables | `.ufo/waves/round-49/w1/ExecRefKeysymA/gen_tables.py` (run from the seat dir against `pins/`), blob sha256 `099e4fcaaef68a8b015a3634b3cb7fe73da36ac8bc61c104f02797db96304c46` |
| dependencies | Python 3 standard library only (`base64 json re struct sys zlib bisect`); no process, no socket, no write |
| judge | `/usr/lib/xkbcommon/xkbcli-how-to-type`, sha256 `f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54` (= pin) |
| keymap compiler | `/usr/lib/xkbcommon/xkbcli-compile-keymap`, sha256 `43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250` (= pin) |

CLI, exactly the draft contract:

```
mado-keysym.py how-to-type --keymap FILE --disable-compose --keysym ARG     # table + judge's exit status
mado-keysym.py --selftest                                                  # 38/38, exit 0 iff all pass
mado-keysym.py --help
```

`--keymap=FILE` is accepted as well as `--keymap FILE`. It refuses with exit 2 and an empty
stdout when `--disable-compose` is absent, when `--keysym` is absent, when `--keymap` is absent,
on an unknown option, and when ARG resolves to no keysym; exit 1 when the keymap file is
unreadable or unparsable. Output is the judge's `tools/how-to-type.c` output byte for byte:
`keysym: <name> (0x%04x)`, blank line, `=== Direct access ===`, blank line, the column header, then
one row per (keycode, layout, level, mask).

Selftest, from the delivered bytes: `python3 -I mado-keysym.py --selftest` →
`MADO_KEYSYM_SELFTEST: 38/38 passed`, exit 0. Its expectations are not hand-waved: every keymap case
was compiled with the pinned `xkbcli compile-keymap` and checked three ways (judge on the compiled
keymap, tool on the compiled keymap, tool on the raw keymap text) — `receipts/synthetic.txt`.

## 2. What the tool models, with the source line each rule came from

| # | rule | source (libxkbcommon `xkbcommon-1.13.2`, pinned in `pins/`) |
|---|---|---|
| 1 | 8 real modifiers with canonical mappings, then virtual modifiers appended in declaration order | `src/keymap-priv.c:38`, `src/xkbcomp/vmod.c:178` |
| 2 | `virtual_modifiers M=0x...` sets an explicit real-mod mapping | `src/xkbcomp/vmod.c:101` (`HandleVModDef`) |
| 3 | group type: explicit `type=` / `type[GroupN]=`, else the automatic type from the group's levels, else the first defined type | `src/xkbcomp/symbols.c:1594` (`FindAutomaticType`), `:1647` (`FindTypeForGroup`) |
| 4 | every group is padded/truncated to the type's level count; trailing `NoSymbol` levels were dropped at parse time | `src/xkbcomp/symbols.c:1767`, `:842`, `src/xkbcomp/ast-build.c:191` |
| 5 | `interpret SYM+PRED(mods)` matched per key/group/level against the key's `modifier_map` mask builds the key's vmodmap | `src/xkbcomp/keymap.c:86` (`FindInterpForKey`), `:177` (`ApplyInterpsToKey`) |
| 6 | each vmodmap bit ORs the key's `modifier_map` mask into that virtual modifier's mapping | `src/xkbcomp/keymap.c:447` |
| 7 | format 2 (how-to-type's default input format) maps any still-unbound virtual modifier to its own index bit | `src/keymap-formats.h:13` (`DEFAULT_INPUT_KEYMAP_FORMAT = XKB_KEYMAP_FORMAT_TEXT_V2`), `src/xkbcomp/keymap.c:457` |
| 8 | an entry's mask is real mods + its virtual modifiers' mappings + bits above `num_mods`; an entry naming an unbound virtual modifier is inactive | `src/xkbcomp/keymap.c:489`, `src/state.c:1614`, `src/keymap.h:676` (`entry_is_active`) |
| 9 | level masks: for level 1 the empty mask first unless an active empty-map entry exists, then every active entry of that level in file order, at most 100 | `src/keymap.c:494`, `tools/how-to-type.c:27` (`MAX_TYPE_MAP_ENTRIES 100`) |
| 10 | row format and modifier printing (a modifier prints when its *mapping* mask is contained in the row mask, virtual modifier names included) | `tools/how-to-type.c:522` (`print_combo`), `:527` (row), `:625` (keysym line), `:627` (header) |
| 11 | keysym resolution for ARG: `xkb_keysym_from_name` with no flags, then a base-10 `strtol` | `tools/how-to-type.c:284-299`, `src/keysym.c:237` |
| 12 | keymap level numbers are 1-based in the text and 0-based in the model | `src/xkbcomp/expr.c:435` |

Rule 10 is the one that decides the shape of a row, and it is not obvious: the mask printed is the
type entry's *effective* mask, but the names printed are every modifier (real **and** virtual)
whose own mapping is contained in that mask. `br` + AltGr therefore prints `[ Mod5 LevelThree ]`
(real Mod5 first, then the virtual name at its own index), which is exactly the host sample.

## 3. Is `/usr/include/xkbcommon/xkbcommon-keysyms.h` sufficient as the keysym data source?

**No.** It is a header, not the table the library uses, in four ways that matter to byte-exactness:

1. **Canonical name choice is not in it.** The pinned header has 2638 `^#define XKB_KEY_` lines
   (sha256 `13023369…`, matching the brief). The brief's "2659 `#define XKB_KEY_` lines" is the
   count of *mentions*: 21 of them sit inside doc comments (`grep -n ... | grep -v ':#define')`. Those 2638 names map to 2505 distinct
   keysyms — the canonical count `XKB_KEYSYM_COUNT_EXPLICIT` in the same tag's `src/keysym.h`. The
   header gives no way to tell which of two names for one value `xkb_keysym_get_name` prints.
2. **The names are not the whole grammar.** `xkb_keysym_from_name` also accepts four special
   spellings (any/nosymbol → NoSymbol, none/voidsymbol → VoidSymbol), `U<hex>` (with `xkb_utf32_to_keysym`
   normalisation), `0x<hex>` without normalisation, and an `XF86_` → `XF86` retry — `src/keysym.c:237-350`.
3. **`U<hex>` needs the keysym↔Unicode table** (`src/keysym-utf.c`, `keysymtab[]`), which is not in
   the header.
4. **Automatic type selection needs the case predicates** — `is_lower` = "has an upper mapping, no
   lower", `is_upper_or_title` = "has a lower mapping" (`src/keysym-case-mappings.c:624`, `:647`),
   backed by a compressed legacy table (0..0x13be) and Unicode table (0x100..0x1f189) that the header
   does not carry.

So the tool **embeds a generated table** (30 767 B, base85(zlib(...))): the 2505 canonical pairs plus
the 133 alias names, the keysym→Unicode table (763 entries), and case-predicate runs. It was
generated from the same tag's `src/ks_tables.h` (sha256 `6960e7e4…`), `src/keysym-utf.c`
(`a66da728…`) and `src/keysym-case-mappings.c` (`86e7f7a2…`) by `gen_tables.py`. That the generated
table is the *right* table was checked against the running judge, not against the sources:
**all 2638 names and 6182 numeric keysyms** (0..0x300, the Latin-1/keysym boundaries, 0x1000000..
0x1000300, 0x10ff00..0x110100, every 0x1001 up to 0x20000000, and invalid values) reproduce the
judge's exit status and `keysym: <name> (0x...)` line — 0 failures, `receipts/keysym-tables.txt`.

## 4. Agreement with the real judge

Method (all in scratch, `HOME`/`XDG_*` under scratch, `env -i PATH=/usr/bin`):

* compile each RMLVO with the pinned `xkbcli-compile-keymap`,
* run the judge: `xkbcli-how-to-type --keymap=FILE --disable-compose --keysym ARG`,
* run the draft: `python3 -I mado-keysym.py how-to-type --keymap FILE --disable-compose --keysym ARG`,
* require stdout **bytes** and exit status to be equal.

Real keymaps: `receipts/agree.txt` — 7797 (keymap, keysym) pairs over 69 compiled
keymaps (every one of the 69 RMLVO specs compiled, 0 compile failures), **7797 agree, 0 disagreements**. The matrix spans single layouts (`us`, `us(intl)`,
`us(dvorak)`, `us(colemak)`, `us(altgr-intl)`, `br`, `br(nodeadkeys)`, `br(nativo)`, `de`,
`de(neo)`, `de(T3)`, `fr`, `fr(oss)`, `fr(bepo)`, `gb`, `gb(intl)`, `es`, `it`, `pt`, `ru`,
`ru(phonetic)`, `ua`, `gr`, `gr(polytonic)`, `pl`, `cz(qwerty)`, `tr`, `jp`, `kr`, `in`, `ir`,
`ca(multix)`, `ch(fr)`, `ch(de)`, `no`, `se`, `fi`, `nl`, `dk`, `hu`), multi-layout
(`us,br`, `us,ru`, `de,fr`, `us,ru,de` + `grp:*_toggle`), and options that change levels/vmods
(`compose:caps`, `lv3:ralt_switch`, `lv3:ralt_switch_multikey`, `lv3:lalt_switch`, `lv3:switch`,
`lv5:caps_switch_lock`, `lv5:lsgt_switch_lock`, `caps:escape`, `ctrl:swapcaps`,
`keypad:pointerkeys`, `altwin:swap_alt_win`, `euv:EuroSign`, `numpad:mac`, `kana:ligature`) plus
models `pc105`, `pc104`, `evdev`. Keysyms: 113 forms per keymap, including names, `0x` forms,
decimal, `U…`, `XF86_…`, keysyms that no level carries, an unnamed value, and refusals.

Host sample reproduced byte for byte (same keymap the claim names,
`compile-keymap --layout br --options compose:caps`):

```
$ python3 -I mado-keysym.py how-to-type --keymap br.kmap --disable-compose --keysym slash
keysym: slash (0x002f)

=== Direct access ===

KEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS
24       AD01      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]
24       AD01      1        Portuguese (Brazil)  3       [ Lock Mod5 LevelThree ]
24       AD01      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]
24       AD01      1        Portuguese (Brazil)  4       [ Shift Lock Mod5 LevelThree ]
97       AB11      1        Portuguese (Brazil)  1       [ ]
```
`cmp` against the judge's stdout: identical. `--keysym Return` → `36 RTRN … 1 [ ]`;
`--keysym nosuchsym` → empty stdout, exit 2.

Synthetic keymaps (the self-test fixtures, `receipts/synthetic.txt`): 31 cases where
judge(compiled) == tool(compiled) == tool(raw) — including the judge's own exit-2 refusals — plus the
tool's contract-only refusals, which the judge does
not share because it has no such contract (below).

### 4.1 Independent cross-check: the C1 counter scored the same bytes

`ExecCounterC1` adopted those exact bytes into a scratch clone (`tools/mado-keysym.py`, commit
`c28346289aaab49adf759f3fcde557014d1cc233`) and scored them in its own bubblewrap sandbox on
two nonces, 633 fixtures + 60 generated pairs each. Both runs:

```
PRED-C1-r49: fixtures=633/633 generated=60/60 selftest=ok readonly=ok tool=present verdict=TARGET_MET
```

receipts `.ufo/waves/round-49/w1/ExecCounterC1/receipts-refA.txt` (nonce 49) and
`…/receipts-refA-nonce2.txt` (nonce 20261027). That is an independent implementation of the same
contract reaching the same verdict on the same bytes, which is the strongest evidence available
before the freeze. The tool's sha256 did not change after that scoring.

## 5. Disagreements, and where a source line explains them

**None on any compiled RMLVO keymap** (7797 pairs, 0 disagreements) and none on any synthetic
keymap's behaviour rows.

Three receipt rows read `DIFF` and are *by design*, not disagreements about libxkbcommon:

| case | judge | draft | why |
|---|---|---|---|
| `refuse-no-disable-compose` | prints the table plus the `=== Access via Compose sequences ===` section, exit 0 (`tools/how-to-type.c:710-711` prints it when `use_compose` is on) | exit 2, no table | the draft contract puts Compose out of scope, and the judge has no way to refuse it |
| `refuse-no-keysym` | tries the argument as a character/code point first (`tools/how-to-type.c:272`) and then resolves `Escape` as a keysym anyway, exit 0 | exit 2, no table | the contract puts character/code-point interpretation out of scope |
| `refuse-unknown-option` (case passes `--format 2`) | accepts `--format` (`tools/how-to-type.c:170`) and prints the table, exit 0 | exit 2, no table | the contract's CLI is exactly `--keymap/--disable-compose/--keysym`; every other judge option is out of scope and refused |

Deviations the implementation deliberately accepts, all outside what a serialized keymap contains:

* a modifier name the model does not know in a mask is skipped, where the C compiler drops the whole
  statement (`src/xkbcomp/types.c:352-366`) — serialized keymaps never name unknown modifiers;
* symbol lists written as a string literal (multi-code-point keysym, `src/xkbcomp/parser.y:873`)
  are read as empty levels;
* `interpret` merge prefixes are not modelled (`src/xkbcomp/compat.c:812`, `si.merge`); the
  serializer never emits them;
* the parser accepts the serialized grammar plus `GroupN` indices; it is not a general xkbcomp.

Two further deviations were measured and are **provably outside the fixture space**, so the scored
bytes keep them (changing them now would move the bytes the counter scored):

| input | judge | draft | why it cannot occur in contract |
|---|---|---|---|
| a keymap with **no `xkb_types` section** (probe: the compiled `br` keymap with that section cut out) | rc 0, 176 B of table (libxkbcommon synthesises a `ONE_LEVEL` type, `src/xkbcomp/types.c:783`) | rc 1, empty stdout | the pinned serializer writes the section unconditionally (`src/xkbcomp/keymap-dump.c:1061`), and the compiler always creates at least that default type; all 69 compiled fixtures have it (`grep -l '^xkb_types' val/k/*.kmap` → 69 of 69) |
| a keymap with a **UTF-8 BOM** | rc 0, 176 B | rc 1, empty stdout | `xkbcli compile-keymap` writes no BOM; 0 of 69 compiled fixtures start with `EF BB BF` |

The hardening, if the freeze ever widens the input beyond compiled keymaps, is three lines: a
`[\ufeff\s]` whitespace class in the tokenizer, and a synthetic `ONE_LEVEL` type when
`km.types` is empty. Not applied here on purpose: `ExecCounterC1` scored sha256 `dcc13cce…`, and
those must stay the delivered bytes.

## 6. What the L1 should freeze, and what would break it

* **Input**: FILE must be the output of the pinned `xkbcli compile-keymap` (format 2 text). A raw
  source with includes is out of contract: the tool parses the serialized grammar only and exits 1
  on such a file instead of guessing what `include` would have merged. Fixtures compiled at count
  time, as the claim says, are exactly right.
* **Flags**: the judge invocation must keep `--disable-compose --keysym`; drop either and the
  judge's own behaviour widens (Compose section, character interpretation) while the tool still
  refuses, so the counter must not treat a judge-only widening as a tool failure.
* **Refusals to pin**: exit 2 + empty stdout for a missing flag, a missing `--keymap`, an unknown
  option, a non-keysym ARG, `NoSymbol`, and `0x` values above `0x1fffffff`; exit 1 + empty stdout
  for an unreadable or unparsable keymap. All are judge-compatible (the judge gives 2 or 1 with an
  empty stdout there too, checked in `receipts/synthetic.txt`).
* **Selftest**: `--selftest` must print `MADO_KEYSYM_SELFTEST: N/N passed` last, with N ≥ 25, exit
  0; this draft prints `38/38`. It writes nothing (keymaps are served from memory), so it runs in a
  read-only sandbox.
* **Do not** make a fixture out of a keymap whose levels carry more than one keysym per level:
  `how-to-type` skips those levels itself (`tools/how-to-type.c:658-661`), so a counter that
  expected a row there would be testing its own assumption, not the tool.
* **Table regeneration**: the blob is data; if the L1 changes the tool, `gen_tables.py` plus the
  pinned `src/ks_tables.h`, `src/keysym-utf.c`, `src/keysym-case-mappings.c` regenerate it
  deterministically (the header pins are in `receipts/pins.txt`).

## 7. Exact retained evidence

| receipt | content |
|---|---|
| `receipts/pins.txt` | sha256 + bytes + tag URL of every libxkbcommon source used (24 files, copied under `pins/`) |
| `receipts/keysym-tables.txt` | 2638 names + 6182 numeric keysyms vs the judge, 0 failures |
| `receipts/agree.txt` | 69 keymaps × 113 keysyms: one `ok`/`DIFF` line per pair, 7797 `ok`, 0 `DIFF`, tool sha256 in the header (671 121 B) |
| `receipts/tables-blob.b85` | the exact 30 767-byte table blob the tool embeds (text sha256 `099e4fca…`); `python3 gen_tables.py` from the seat dir reproduces it byte for byte against `pins/` |
| `receipts/synthetic.txt` | each self-test keymap compiled and compared three ways (31 agree, 3 contract-only refusals, 4 non-applicable) |
| `receipts/selftest.txt` | `python3 -I mado-keysym.py --selftest` output and exit status |
| `receipts/host-sample.txt` | the `br` + `slash` case, `cmp` against the judge |
| `receipts/session-material.txt` | the sanitised keymap census used (layout/variant/option names only, no device names, no `~` paths) |

Every locator in §2 was computed with `grep -n` over the copied pins, e.g.
`grep -n 'MAX_TYPE_MAP_ENTRIES' how-to-type.c` → `27`.

## 8. Host safety

* No writes outside the seat dir; every `xkbcli` call ran with `env -i PATH=/usr/bin` and
  `HOME`/`XDG_CONFIG_HOME`/`XDG_CACHE_HOME` inside scratch (`/fast/scratch/hyaku/mado-r49/ExecRefKeysymA`).
* `HOME`, `XDG_CONFIG_HOME`, `XDG_CACHE_HOME`, `XDG_DATA_HOME` pointed into scratch for every
  `xkbcli` and tool run; `XDG_CACHE_HOME` was never the operator's, and no operator-owned path was
  read or written (no M48-10 class of write was possible: the seat wrote only under the lane's seat
  dir and `/fast/scratch/hyaku/mado-r49/ExecRefKeysymA`).
* No pacman, no package transaction, no compositor read, no GUI program, no terminal, no `hyprctl`.
* `xkbcli` used: only `compile-keymap` and `how-to-type` (`list` not needed).
* No tool installed or upgraded this wave.
* Scratch (`/fast/scratch/hyaku/mado-r49/ExecRefKeysymA`) is removed at the end of the seat.

## 9. Risks

* **The blob is the risk surface.** Any byte error in it shows up as a wrong canonical name or a
  wrong automatic type. It is pinned by digest here and validated name by name (§3), so the counter
  will catch it rather than the operator.
* **Layout names longer than 20 bytes** are not truncated by either side; the tool pads by *bytes*
  (`_ljust`), matching C's `%-20s`. xkeyboard-config 2.48's names are ASCII in every keymap tested.
* **The counter's sandbox** must contain the keymap at the path it passes; the tool reads only that
  file and never the keysym header, so a sandbox without `/usr/include` is fine.
* Nothing here is blocked.
