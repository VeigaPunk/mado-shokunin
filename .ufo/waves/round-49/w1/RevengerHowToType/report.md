# how-to-type and `xkb_keymap_key_get_mods_for_level`: intent and history upstream

Seat `RevengerHowToType`, mado round 49 / wave w1, lane repo `mado-shokunin`, base `03e4ae7`.
Subject: **libxkbcommon** (github.com/xkbcommon/libxkbcommon), the program that C1's counter
judges (`/usr/lib/xkbcommon/xkbcli-how-to-type`, 1.13.2-1) and the library function whose
masks it prints (`xkb_keymap_key_get_mods_for_level`).

Every locator below is a **line number in a commit-pinned file** and was recomputed by
`.ufo/waves/round-49/w1/RevengerHowToType/verify-quotes.sh` (greps this seat's own pinned
copies under `src/`, `SHA256SUMS` alongside). Nothing here is quoted from a branch.

---

## 0. Bottom line

1. `how-to-type` is a **test/demo program for a public API**, not a UI: it was written to
   exercise `xkb_keymap_key_get_mods_for_level()` the week that function landed, and its
   output format is whatever was convenient to read (`188a1c79`, 2020-03-20).
2. The pinned output is therefore **an artefact of three independent decisions**: the *mask
   set* the API returns, the *name expansion* the tool does over that mask, and the
   *canonical keysym name* the library picks for the header line.
3. Of the three, only the third moved inside 1.11.0→1.13.2 for C1's contract command: the
   canonical name of keysym `0xff7e` flipped from `Mode_switch` to `ISO_Group_Shift` **in
   1.13.2 precisely** (`60d0e5f8`). Everything else on the `--keymap … --disable-compose
   --keysym …` path is source-identical from 1.11.0 through 1.13.1.
4. The pin matters at two other boundaries as well: < 1.11.0 has neither `--keymap` nor
   `--disable-compose` nor the `=== Direct access ===` section, and 1.11.0 introduced
   keymap **format v2 as the default *input* format** for all tools (`44c8deb`).
5. The keysym header `/usr/include/xkbcommon/xkbcommon-keysyms.h` is a **sufficient data
   source for explicit names and for canonical choice** — upstream itself derives the
   canonical table from exactly this file with the rule "first `#define` for a value wins"
   (`scripts/update-keysyms-derived-headers.py:47-48`) — but it is **not** sufficient for
   the whole `xkb_keysym_get_name` contract: Unicode keysyms (`U%04X`) and the unnamed
   fallback (`0x%08x`) are computed, never listed (`src/keysym.c:66,93`).

---

## 1. Pins and method

Release commits cited (all tags on the same repository; `git rev-list -n1 <tag>`):

| tag | release commit | date |
|---|---|---|
| 1.0.0 | `12f99d0dfe012c07d82d70296bbcac8a0a8ac0a9` | 2020-09-06 |
| 1.3.1 | `88222c8d40543c29af781f7d7e25d202ff40e4b7` | 2021-09-10 |
| 1.10.0 | `7888474d0296dcad50c9ba4adfdfdf2be02d35e1` | 2025-05-21 |
| 1.11.0 | `0f9cefb1fedb23433666fa5d9045e48ff030c006` | 2025-08-08 (committer) |
| 1.12.0 | `f4e247e50dd4d06542c5e177cfe53f82dfab69b6` | 2025-10-10 |
| 1.12.4 | `57e7469fe52fdeb09835b33f43ae6f4b52cc3e97` | 2025-12-03 |
| 1.13.0 | `3049d310694fd70f1269bf48a1200aa4259e79b1` | 2025-11-05 |
| 1.13.1 | `6f76d19db72b5d450e927b41e1e96cbe3252aba8` | 2025-12-03 |
| **1.13.2** | **`d1442aaa6b635551182e83c3b55037f4c118c962`** | 2026-05-30 |
| 1.14.0-beta2 | `51c1916575aa153fd9f44264e9159249619f86a7` | 2026-09-10 |

Method: full-history clone of the repository into seat scratch
(`git clone --filter=blob:none https://github.com/xkbcommon/libxkbcommon`), then every
statement resolved with `git log`/`git show`/`git diff` at commit granularity, containment
checked with `git tag --contains`, and ancestry double-checked with
`git merge-base --is-ancestor` for the commits that matter. Files that the report quotes are
extracted to `src/` in this seat directory with their sha256 (`src/SHA256SUMS`).

Caution recorded while working: **`src/ks_tables.h` carries a stale inline comment** for the
`keysym_to_name` entry of `0xff7e` on tags ≤ 1.13.1 — it says `/* ISO_Group_Shift */` while
the offset it stores resolves to `Mode_switch`. The canonical name must be resolved through
`keysym_names + offset` (`src/keysym.c:54`), never read off the comment. Receipt:
`receipt-canonical-name-decode.txt`.

Quote discipline: code quotes are matched byte-exactly against the pinned file; quotes from
commit messages and from prose documentation are whitespace-normalized (a multi-line sentence
is one sentence). `verify-quotes.sh` recomputes every locator and re-checks that the report
cites it.

---

## 2. Anatomy of the pinned output

Command under contract: `xkbcli-how-to-type --keymap=FILE --disable-compose --keysym ARG`.

`tools/how-to-type.c@d1442aaa` produces, in order:

| line(s) | emitter | what it is |
|---|---|---|
| 625 | `printf("keysym: %s (%#06"PRIx32")\n\n", name, keysym);` | header: `xkb_keysym_get_name()` + keysym value |
| 626 | `printf("=== Direct access ===\n\n");` | section marker (new in 1.11.0) |
| 627 | `printf("%-8s %-9s %-8s %-20s %-7s %-s\n", …)` | column header, widths 8/9/8/20/7 |
| 697-702 | `xkb_keymap_key_get_mods_for_level(...)`, then `print_combo(...)` per mask | one row per mask |
| 527 | `printf("%-8u %-9s %-8u %-20s %-7u [ ", …)` | row prefix (`layout+1`, `level+1`) |
| 531-534 | `xkb_keymap_mod_get_mask2(...)`; `printf("%s ", xkb_keymap_mod_get_name(...))` | mask → names |

Notes that C1's reimplementation must reproduce:

- **Name expansion is "every modifier whose mask is contained in the row mask", in modifier
  index order**, printed with a trailing space each, closed by `]`. Because a virtual modifier
  can share a real bit, one bit prints **two** names. On this host `LevelThree` encodes to
  `0x80`, i.e. `Mod5` (receipt `receipt-modmaps.txt`), hence `[ Mod5 LevelThree ]`.
- Ordering inside `[ … ]` is `xkb_keymap_mod_get_index` order (real modifiers first, virtual
  after), not a sort by name — `[ Shift Lock Mod5 LevelThree ]` is evidence.
- **Row order** is keycode ascending, then layout ascending, then level ascending, then the
  order `xkb_keymap_key_get_mods_for_level` returns masks (i.e. key-type entry order,
  with the level-0 special case first). No sorting, no de-duplication.
- **There is no Lock filtering on the direct path.** Lock rows appear whenever a key type maps
  a Lock-bearing mask to that level (`FOUR_LEVEL_SEMIALPHABETIC` maps `Lock`→2 and
  `Lock+LevelThree`→3 with `preserve`). Receipt: `receipt-keysym-names.txt`, `--keysym Q`
  yields `[ Shift ]` **and** `[ Lock ]`.
- The only Lock-specific logic in the whole tool is in the **Compose** section
  (`SHIFT_MASK`/`LOCK_MASK` at 457-460 and the "shift cancel lock" skip at 489-506), which
  `--disable-compose` never reaches.
- `%#06x` renders four hex digits for keysyms < 0x10000 (`0x002f`) and grows for larger
  values (`0x10001e9` → `0x10001e9`); it is not a fixed-width field. Receipts:
  `receipt-arg-forms.txt`, `receipt-keysym-names.txt`.

### 2.1 Where the mask set comes from

`src/keymap.c@d1442aaa:494-552`:

- reject unknown key / out-of-range layout (`506-513`);
- **level 0 special case** (519-541): a key type maps "everything not listed" to level 1, so
  instead of returning an unbounded family, the function emits the **empty mask** when level 1
  is not explicitly mapped;
- then every *active* type entry whose level matches (543-549), in table order.

The comment states the intent in the function's own words: "This is almost always what we
want. If applicable, given it priority" (`527`) — that is the reason a plain `<AB11>` level 1
row prints `[ ]` rather than a list of masks.

---

## 3. Timeline (what happened, in order)

Bold = visible on C1's stdout/stderr/rc.

| date | commit | first release | change |
|---|---|---|---|
| 2020-02-05 | `d92a248` | 1.0.0 | **new API** `xkb_keymap_key_get_mods_for_level`; motivation: "invert the keycode->keysym transformation" for auto-type/desktop automation |
| 2020-03-20 | `188a1c7` | 1.0.0 | **`test/how-to-type.c` demo**: codepoint + RMLVO, tab-separated, "Pipe into `column -ts $'\t'`" |
| 2020-04-05 | `860cfc0` | 1.0.0 | API fix: unhit level falls back to the **empty mask** (issue #140) — the `[ ]` row |
| 2020-06-22 | `ec2bbe5` | 1.0.0 | file moved `test/` → `tools/` |
| 2020-07-09 | `7141820` | 1.0.0 | **rc 2 on invalid usage** for all tools (`EXIT_INVALID_USAGE` = 2, `meson.build:166`) |
| 2020-07-13 | `7d36a3d` | 1.0.0 | `getopt_long` |
| 2020-09-09 | `c5565bd` | 1.0.1 | **self-aligned columns** replace tabs + external `column` |
| 2021-07-31 | `f8c430c` | 1.3.1 | **`--keysym`** added |
| 2024-09-12 | `0cd1087` | 1.10.0 | **argument grammar** (literal char / decimal / `0x` / `U+` for codepoints; name / `0x` / decimal for keysyms) |
| 2025-05-06 | `82ea291` | 1.11.0 | `--format`, and default *output* format = `XKB_KEYMAP_USE_ORIGINAL_FORMAT` |
| 2025-05-07 | `44c8deb` | 1.11.0 | **keymap format v2 introduced and made the default *input* format** for the tools |
| 2025-05-12 | `61d8ec6` | 1.10.0 | **`%#06x`**: `keysym: X (0x002f)` replaces `(0x2f)` |
| 2025-05-12 | `2617ebc`, `b49a440` | 1.10.0 | modifier count type; refactor |
| 2025-08-04 | `9d4885d` | 1.11.0 | **keysym parsing fixes** (`errno` reset; name parsing as fallback) + argument tests |
| 2025-08-04 | `29579ad` | 1.11.0 | `--verbose` |
| 2025-08-05 | `6df4512` | 1.11.0 | **`--keymap`** (file or stdin) |
| 2025-08-06 | `7394a3c` | 1.11.0 | **mask→name fix**: use `xkb_keymap_mod_get_mask2`, not `1 << mod` |
| 2025-08-06 | `13ae4a2` | 1.11.0 | **Compose support on by default, `--disable-compose`, `=== Direct access ===`** |
| 2025-10-30 | `52fe698` | 1.13.0 | Compose lookup by UTF-8 too (issue #904) — compose path only |
| 2026-05-30 | `60d0e5f8` | **1.13.2** | **canonical name of `0xff7e`: `Mode_switch` → `ISO_Group_Shift`**; new keysyms |
| 2026-02-17 → 2026-09-09 | `7949954`, `4bc4d78`, … | 1.14 only | usage prints `v1`/`v2` labels; `--version` — **outside the pin** |

---

## 4. Why each piece exists (intent, from the commits themselves)

### 4.1 The API was built for synthesising keystrokes

`d92a248` (2020-02-05), body: "The new API is useful to implement features like auto-type and
desktop automation." That framing explains the design: the caller already knows the **keysym**
it wants, not the key. The function is the inverse of `keycode+state → keysym`, and it is
deliberately *not* a full search — it reports the type entries of the key that produce the
requested level, so the caller still picks a keycode.

### 4.2 The demo, and the fallback that makes level 1 special

`188a1c7` states its own purpose: it "was written to exercise the new
`xkb_keymap_key_get_mods_for_level()` function". Its example output in the commit message is
already the shape we still see (`keysym: A (0x41)`, `KEYCODE KEY NAME LAYOUT# …`).

Two months later `860cfc0` fixed the API (issue #140, reported by AliKet): key types rely on
the implicit "no entry matches ⇒ level 1" rule, so the function returned nothing at all for
`a` in `us`. The fix is the level-0 special case cited in §2.1, and it is the reason the
tool is usable at all for the first level of a key.

### 4.3 Exit-code discipline

`7141820` (2020-07-09) made every tool return `2` for invalid usage instead of a mixture of
`1`/`EXIT_FAILURE`. The constant is not in a header: it is injected by the build,
`configh_data.set('EXIT_INVALID_USAGE', '2')` (`meson.build:166`). This is the
`rc=2` that C1's contract relies on for refusals and for "argument is not a keysym"
(`ERROR: Failed to convert argument to keysym` + usage on stderr, observed in
`receipt-arg-forms.txt`).

### 4.4 Output alignment moved into the program

`c5565bd` (2020-09-09) removed the "pipe into `column`" advice and padded the columns itself:
`printf("%-8u %-9s %-8u %-20s %-7u [ ", …)`. The widths still in the pinned binary are from
that commit; no commit since has changed them (the 1.11.0 diff reuses the same `print_combo`).

### 4.5 `--keysym`

`f8c430c` (2021-07-31): "Previously, could only check how to type a Unicode codepoint, but
searching for a keysym directly is also occasionally useful." Semantics: skip codepoint
parsing entirely, so `--keysym 97` means keysym `0x61`, not character `a`.

### 4.6 The 1.11.0 rewrite: `--keymap`, format selection, Compose

Three commits in four days (`9d4885d`, `6df4512`, `13ae4a2`) turned a 316-line demo into an
827-line tool. `6df4512` added `--keymap` with the stated purpose of being usable with the
`dump-keymap-*` tools; `13ae4a2` added Compose support **on by default**, which forced the
`=== Direct access ===` heading (the older flat table could not coexist with a second
section) and pulled in the "shift cancel lock" filtering for compose sequences.

That is why `--disable-compose` exists and why it is *not* cosmetic: without it the tool also
walks a Compose table from the locale and appends a second table. The pinned contract's
`--disable-compose` removes that whole branch; the direct section is byte-identical either
way.

### 4.7 The mask test had to stop assuming `1 << index`

`7394a3c` (2025-08-06): "tools: Fix how-to-type modifier mask test". The old code tested
`mask & (1 << mod)`, i.e. it assumed the modifier's *index* equals its *bit*. That assumption
broke once real modifiers can be encoded independently of their index: the fix reads the
encoding (`xkb_keymap_mod_get_mask2`, pinned at `tools/how-to-type.c:531`) and prints a name
when the whole encoding is contained in the mask. This is exactly the code path that makes
`LevelThree` appear next to `Mod5` in the same brackets.

### 4.8 Format v2 is the *parse* default, and it is invisible for compiled keymaps

`44c8deb` (2025-05-07) made `XKB_KEYMAP_FORMAT_TEXT_V2` the default **input** format of every
tool and of `xkb_keymap_new_from_names()`; `src/keymap-formats.h:13-14` is the pinned state:

```
#define DEFAULT_INPUT_KEYMAP_FORMAT  XKB_KEYMAP_FORMAT_TEXT_V2
#define DEFAULT_OUTPUT_KEYMAP_FORMAT XKB_KEYMAP_USE_ORIGINAL_FORMAT
```

Consequences that matter for C1:

- `xkbcli-how-to-type --help` prints the *numeric* enum: `The keymap format to use (default:
  2)`. (1.14.0 changes this to labels `v1`/`v2` — `7949954` — so a pin bump changes the usage
  text, which is part of the "refuses with usage on stderr" output.)
- Serialization is format-agnostic **today**: `compile-keymap --output-format v1` and
  `--output-format v2` on this host produce the **same bytes**
  (sha256 `efd487a3…fce81` for both, receipt `receipt-v1-v2-bytes.txt`). "Format" is a parse
  mode, not a syntax.
- v2 does have semantics that v1 lacks — notably the auto-encoding of unmapped virtual
  modifiers (`doc/keymap-text-format-v1-v2.md:2767-2771`: virtual modifiers "are mapped to
  their [*canonical* mapping]"). For C1's fixtures this is inert, because a keymap that has
  been round-tripped through `compile-keymap` carries explicit encodings (the br keymap has
  `virtual_modifiers … Hyper=0x4000,ScrollLock=0x8000;` plus `modifier_map` bindings). It
  becomes visible only for a hand-written keymap file with unmapped vmods — which the
  contract already excludes by defining FILE as compile-keymap output.

---

## 5. Canonical keysym name selection

`xkb_keysym_get_name` (`src/keysym.c:70-94`) is a three-tier function:

1. explicit table hit → named string (`79`), from `keysym_to_name` (offset into
   `keysym_names`, `54`);
2. Unicode keysyms in `[XKB_KEYSYM_UNICODE_MIN, XKB_KEYSYM_UNICODE_MAX]` →
   `snprintf(buffer, size, "U%04"PRIX32, ks & UINT32_C(0xffffff))` (`66`) — uppercase,
   zero-padded to 4 digits;
3. otherwise `snprintf(buffer, size, "0x%08x", ks)` (`93`).

All three tiers are observable in the pinned binary (receipt `receipt-keysym-names.txt`):

```
ARG=0x00E9     -> keysym: eacute (0x00e9)          # tier 1
ARG=0x10001e9  -> keysym: U01E9 (0x10001e9)        # tier 2
ARG=0x10000e9  -> keysym: 0x010000e9 (0x10000e9)   # tier 3 (below UNICODE_MIN)
ARG=0x1fffffff -> keysym: 0x1fffffff (0x1fffffff)  # tier 3
```

Tier 1's data is generated from the **public header**, and the header documents its own rules
(`src/xkbcommon-keysyms.h@host-1.13.2:104-105`): "Where several mnemonic names are defined
for the same keysym in this file, the first one listed is considered the 'canonical' name."
The generator implements exactly that
(`scripts/update-keysyms-derived-headers.py:47-48`: keep the first name seen per value), and
that is how the pinned table was built. Deprecation is a separate, also header-documented
rule (lines 116-136: parenthesised Unicode mapping, an explicit "deprecated" comment, an
explicit "non-deprecated alias" comment, else implicit deprecation for later aliases).

**Copying an alias line out of the header is not the same as reproducing the table**, because
the header lists aliases as ordinary defines. On this host the header has **2638**
`#define XKB_KEY_` lines covering **2505** distinct values, of which **120 carry more than one
name** — e.g. **9** names for `0xff7e`, of which `Mode_switch` carries the comment
`/* non-deprecated alias for ISO_Group_Shift */` (header line 286). The generator's
"first wins" rule, applied in file order, is what selects `ISO_Group_Shift`.

The flip at 1.13.2 is the only canonical-name change inside the pin window:

| tag | `xkb_keysym_get_name(0xff7e)` | evidence |
|---|---|---|
| 1.11.0, 1.12.4, 1.13.1 | `Mode_switch` | decoded `keysym_to_name` offset 19891 → `Mode_switch` |
| 1.13.2 | `ISO_Group_Shift` | same table, offset 17760 → `ISO_Group_Shift` |

Observed on the pinned binary, 2026-10-27: `--keysym 0xff7e` prints
`keysym: ISO_Group_Shift (0xff7e)` and the *alias* `--keysym Mode_switch` prints the same
header (receipt `receipt-0xff7e-name.txt`). So the ARG a bind would use (`Mode_switch`) and the
name the tool echoes back are different strings on 1.13.2, and were the same string on ≤1.13.1.

`60d0e5f8` says it plainly: "`ISO_Group_Shift` is now the canonical name of the corresponding
keysym. Previously it was `Mode_switch`, which refers to a core X group mechanism obsoleted
by XKB." The same commit adds `XKB_KEY_dead_apostrophe`, `XKB_KEY_SSHARP`,
`XKB_KEY_leftsingleanglequotemark`, `XKB_KEY_rightsingleanglequotemark` and several
`XF86ElectronicPrivacyScreen*` / `XF86ActionOnSelection` / `XF86Contextual*` names
(1.13.2 release notes), which changes which `--keysym <name>` arguments are accepted at all.

This is not cosmetic for a *serialized keymap* either: keymap text stores keysym **names**.
The same commit's test fixture diff rewrites `interpret Mode_switch+AnyOfOrNone(all) {` to
`interpret ISO_Group_Shift+AnyOfOrNone(all) {`, and this host's br+`compose:caps` keymap
(pinned 1.13.2) contains `interpret ISO_Group_Shift+AnyOfOrNone(all)` at line 1123, although
xkeyboard-config 2.48's source spells it `interpret Mode_switch {`
(`/usr/share/xkeyboard-config-2/compat/basic:28`). Recompiling the same RMLVO under 1.13.1
therefore produced different fixture bytes. *[INFERENCE — the 1.13.1 binary was not run; the
claim rests on the fixture diff in `60d0e5f8` plus the source name at
/usr/share/xkeyboard-config-2/compat/basic:28.]*

---

## 6. What changed across 1.11.0 → 1.13.2 that can move the contract

Scoped to what the contract command can observe.

### 6.1 The tool source

`git diff 1.11.0 1.13.2 -- tools/how-to-type.c` is **10 insertions / 2 deletions**, entirely
inside `lookup_compose_sequences()` (the `xkb_keysym_to_utf8` fallback of `52fe698`).
`--disable-compose` skips that function; therefore **the tool's direct section is
source-identical across the pin window**, and so is `tools-common.c`'s contribution
(`tools-common.c` diff in that range is the 1.13 `print_modifiers_encodings` change plus
logging).

### 6.2 The library functions on that path

`git log 1.11.0..1.13.2 -- src/keysym.c` is **empty**: name selection code unchanged.
`src/keymap.c` changes in that range are confined to constructors, `get_as_string*` and
`key_by_name` (hunk headers), i.e. **not** `xkb_keymap_key_get_mods_for_level`,
`key_get_name`, `num_levels_for_key` or `key_get_syms_by_level`.

### 6.3 The data, which is where the pin actually bites

| release | commit | effect on the contract |
|---|---|---|
| 1.12.0 | `584e0690`, `cb53e79e`, `8a5a3393` | keysym set/case-mappings updated; `XF86BrightnessAuto` deprecated. New names become accepted `--keysym` arguments. |
| 1.12.0 | `#849` fix | keymaps may now use keycodes `0 .. 0xfffffffe`, previously capped at `0xfff` (parse side). |
| 1.13.0 | `244f3a81` | `XF86MediaPlayPause`, `XF86Exit`, `XF86AudioBassBoost` added. |
| 1.13.2 | `60d0e5f8` | canonical `0xff7e` flip + new keysyms (also changes compile-keymap output bytes). |
| 1.13.2 | `dc5625f6` | UTF translations for `XF86Numeric[0-9]` (affects UTF-8/UTF-32 conversions, not name lookup). |
| 1.13.2 | `0e033b6f`, `0e1f8401`, `e1983ab8`, `1cf97d4a` | xkbcomp parse fixes: malformed key types/interpret sections that were silently accepted now **fail the compile**, and default-section tag detection is corrected. |
| 1.13.2 | `12359667` | perfect-hash layout only (perf). |

### 6.4 Verdict for the pin

- **1.11.0 … 1.13.1**: C1's stdout/rc for `--keymap FILE --disable-compose --keysym ARG` is
  identical (source-level evidence above). Only 1.13.0's compose fix differs, and it is
  unreachable under `--disable-compose`.
- **1.13.1 → 1.13.2**: the name on the header line can differ (`0xff7e`), the set of accepted
  `--keysym` names grows, and compile-keymap fixture bytes can differ by keysym-name spelling.
- **< 1.11.0**: the command does not exist in this shape (no `--keymap`, no
  `--disable-compose`, no `=== Direct access ===` at 1.10.0: 316 lines, zero occurrences of
  either option).
- **1.14.0**: usage text changes (labels, `--version`); still outside the pin.

---

## 7. Observed receipts on the pinned host binaries

All captured with `env -i PATH=/usr/bin HOME=<scratch> XDG_CONFIG_HOME=<scratch>`, stdout only,
keymap compiled at capture time by the pinned `xkbcli-compile-keymap` (sha256
`43b924f6…77250`) from `--layout br --options compose:caps` (keymap sha256
`efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81`).

| receipt | shows |
|---|---|
| `receipt-arg-forms.txt` | `Return`/`0xff0d`/`slash`/`47` accepted; **`U+002F` rejected, rc 2** with usage; `nosuchsym` rc 2 |
| `receipt-keysym-names.txt` | Lock row for `Q`; three `get_name` tiers; `%#06x` widths |
| `receipt-modmaps.txt` | `LevelThree: 0x00000080 # Mod5` — why `[ Mod5 LevelThree ]` |
| `receipt-v1-v2-bytes.txt` | `--output-format v1` == `v2` == default, byte for byte |
| `receipt-canonical-name-decode.txt` | `0xff7e` canonical name per tag |
| `receipt-ks-tables-sha.txt` | `src/ks_tables.h` sha256 per tag |
| `receipt-keymap-sample.txt` | the compiled keymap's `FOUR_LEVEL_SEMIALPHABETIC` type with its `map[Lock…]`/`preserve` entries |
| `receipt-0xff7e-name.txt` | pinned binary prints `ISO_Group_Shift` for `--keysym 0xff7e`; `Mode_switch` is accepted as an alias |
| `receipt-60d0e5f8-fixture-diff.txt` | the 1.13.2 commit's own fixture diff: `interpret Mode_switch…` → `interpret ISO_Group_Shift…` |
| `receipt-commit-messages.txt` | full commit bodies quoted in this report, with their SHAs |
| `receipt-verify-quotes.txt` | output of `verify-quotes.sh`: 29 checks, 0 failures |

Seat material (this directory): `report.md` (this file), `verify-quotes.sh` (recomputes every
locator above and re-checks that each quote is in this report), `src/` with the commit-pinned
sources named in the text plus `SHA256SUMS`, and the `receipt-*.txt` captures.

The key type behind the host's Lock rows, from the compiled keymap:

```
type "FOUR_LEVEL_SEMIALPHABETIC" {
    modifiers= Shift+Lock+LevelThree;
    map[Shift]= 2;  map[Lock]= 2;
    map[LevelThree]= 3;  map[Lock+LevelThree]= 3;  preserve[Lock+LevelThree]= Lock;
    map[Shift+LevelThree]= 4;  map[Shift+Lock+LevelThree]= 4;  preserve[Shift+Lock+LevelThree]= Lock;
```

`preserve` does **not** remove Lock from the mask the API reports — it only means Lock is not
consumed. A reimplementation that filtered "preserved" modifiers out of the printed mask would
disagree with the judge.

---

## 8. Consequences for the C1 freeze (what this history implies for the counter)

1. **Pin the tool identity, not just the version string.** The name table is compiled into the
   binary; `sha256 f6c0b122…7e54` is the only safe anchor. 1.13.1 and 1.13.2 differ on stdout
   for at least one keysym value.
2. **Fixture bytes are version-bound in a second way**: `compile-keymap` writes keysym *names*
   into the keymap text, so a 1.13.1 fixture and a 1.13.2 fixture of the same RMLVO can differ
   (`Mode_switch` vs `ISO_Group_Shift`). Compiling in the counter at count time (as declared)
   removes this; pre-baked fixture files would not.
3. **The keysym name table cannot be derived at run time from the header unless the header is
   shipped**, and even then three rules must be applied: first-`#define`-wins for canonical,
   deprecation annotations for `from_name` acceptance, and the two computed tiers
   (`U%04X`, `0x%08x`). Because the sandbox sees only the keymap file, the tool should embed a
   table generated from the pinned header (the header is a pure `#define` list; a generated
   Python literal is ~2638 entries) and implement the computed tiers by hand.
4. **`ARG` grammar is narrower than the usage text suggests.** With `--keysym`, the accepted
   forms are: an explicit name (case-sensitive, `XKB_KEYSYM_NO_FLAGS`), a `0x…` hexadecimal
   value, or a **decimal** value. `U+002F` is rejected (rc 2) — the `U+` prefix belongs to
   codepoint parsing, which `--keysym` bypasses. Fixtures that feed `U+…` will fail the judge
   for a reason that is not the tool's fault.
5. **`rc` on refusal is 2 with usage on stderr** (`EXIT_INVALID_USAGE` = 2, `meson.build:166`);
   any tool that returns 1 or prints usage on stdout disagrees.
6. **Masks must be printed with the keymap's own encodings.** `1 << mod_index` is wrong
   (`7394a3c`); the encoding is `xkb_keymap_mod_get_mask2`. A pure-Python reimplementation has
   to model modifier encodings, including the v2 auto-encoding rule for unmapped vmods, or it
   will print `Mod5` where the judge prints `Mod5 LevelThree`.

---

## 9. Confidence and open items

- **High confidence** (commit + diff + regenerated receipts): all dates, tags, bench of the
  timeline, the anatomy line numbers, the mask algorithm, the name tiers, the 1.11.0 option
  set, the `0xff7e` name on 1.13.2 (observed on the pinned binary), the v1/v2 byte-identity on
  this keymap.
- **Medium** (marked `[INFERENCE]`): the *1.13.1 and older* side of the name flip — the 1.13.1
  binary was never run; the claim rests on the decoded `keysym_to_name` offsets, the commit's
  own fixture/test diffs, and the observed 1.13.2 behaviour.
- **Not attempted**: building 1.11.0/1.12.x to diff binary output. The source-level argument
  (identical tool source on the reachable path, empty `src/keysym.c` log) is stronger and
  cheaper, but it is a *source* argument, not a binary one.
- **Out of scope by design**: Compose semantics, `xkb_keysym_from_name` case-insensitive mode,
  and the 1.14 series beyond noting what would break the frozen usage text.

---

### Citation index (commit-pinned)

- API origin: <https://github.com/xkbcommon/libxkbcommon/commit/d92a248>
- Demo origin: <https://github.com/xkbcommon/libxkbcommon/commit/188a1c7>
- Fallback fix: <https://github.com/xkbcommon/libxkbcommon/commit/860cfc0>
- rc 2: <https://github.com/xkbcommon/libxkbcommon/commit/7141820>
- Alignment: <https://github.com/xkbcommon/libxkbcommon/commit/c5565bd>
- `--keysym`: <https://github.com/xkbcommon/libxkbcommon/commit/f8c430c>
- Argument grammar: <https://github.com/xkbcommon/libxkbcommon/commit/0cd1087>
- Format v2 default: <https://github.com/xkbcommon/libxkbcommon/commit/44c8deb>
- `%#06x`: <https://github.com/xkbcommon/libxkbcommon/commit/61d8ec6>
- Keysym parsing fixes: <https://github.com/xkbcommon/libxkbcommon/commit/9d4885d>
- `--keymap`: <https://github.com/xkbcommon/libxkbcommon/commit/6df4512>
- Mask→name fix: <https://github.com/xkbcommon/libxkbcommon/commit/7394a3c>
- Compose + `=== Direct access ===`: <https://github.com/xkbcommon/libxkbcommon/commit/13ae4a2>
- Compose non-canonical fix: <https://github.com/xkbcommon/libxkbcommon/commit/52fe698>
- Canonical name flip: <https://github.com/xkbcommon/libxkbcommon/commit/60d0e5f8>
- Pinned sources (path + line numbers above):
  <https://github.com/xkbcommon/libxkbcommon/blob/d1442aaa6b635551182e83c3b55037f4c118c962/tools/how-to-type.c>,
  <https://github.com/xkbcommon/libxkbcommon/blob/d1442aaa6b635551182e83c3b55037f4c118c962/src/keymap.c>,
  <https://github.com/xkbcommon/libxkbcommon/blob/d1442aaa6b635551182e83c3b55037f4c118c962/src/keysym.c>,
  <https://github.com/xkbcommon/libxkbcommon/blob/d1442aaa6b635551182e83c3b55037f4c118c962/src/keymap-formats.h>,
  <https://github.com/xkbcommon/libxkbcommon/blob/d1442aaa6b635551182e83c3b55037f4c118c962/doc/keymap-text-format-v1-v2.md>,
  <https://github.com/xkbcommon/libxkbcommon/blob/d1442aaa6b635551182e83c3b55037f4c118c962/scripts/update-keysyms-derived-headers.py>,
  <https://github.com/xkbcommon/libxkbcommon/blob/d1442aaa6b635551182e83c3b55037f4c118c962/meson.build#L166>
