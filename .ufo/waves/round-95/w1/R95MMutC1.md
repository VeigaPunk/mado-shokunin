# R95MMutC1 — C1 mutation report (DRAFT; every run below is a DRAFT run, not a measurement)

Seat R95MMutC1 (mutation tester, C1 `mado-mimesniff`). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Scratch `S=$HYAKU_SCRATCH/mado-r95/R95MMutC1` (`/fast/scratch/hyaku/mado-r95/R95MMutC1`), deleted on exit.

Pins: candidate `.ufo/waves/round-95/build/mado-mimesniff.c1.py` sha256
`a13b6e0e3b0c399892ff027309f942daa96e92713851e8d8cfb736b277cde99d` (matches the declaration); name step
`tools/mado-mimeglob.py` sha256 `65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453` (unchanged, copied
next to the candidate); oracle `.ufo/waves/round-95/controls/mimesniff-oracle-r95.c` sha256
`99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a`, compiled in scratch against the installed
`gio-2.0` 2.90.1 (glib2 2.90.1-1, shared-mime-info 2.5.1-2).

## Files written by this seat

| path | what | sha256 |
|---|---|---|
| `.ufo/waves/round-95/controls/mimesniff-mutants-r95.json` | 87 counted mutants + 2 `equivalent_not_counted` | `a6c7fcbe5bfccf05f54e05e08f462bcf088380222c3e6a792026ec8429ac6781` |
| `.ufo/waves/round-95/w1/R95MMutC1-cases.json` | 51 oracle-labelled cases (the cheapest killer per counted mutant) | `f9bffdf71e395d3319314276fb28baea30c9e4f420384149d4ae059298258356` |
| `.ufo/waves/round-95/w1/R95MMutC1-harness.py` | the generator/runner cited below (regenerates cases, labels, kill map) | `d529d50ce676913646f064a2ea316e625c6f8f1a8d6f5f6d43154feb64ba71b8` |
| `.ufo/waves/round-95/w1/R95MMutC1-killmap.json` | DRAFT kill map: per mutant all killers, the cheapest one, its label, the mutant's actual output | `a40bd288e71367e3d3c49c9b549519235a6d0d21dc35d62425bbb72829201a52` |
| `.ufo/waves/round-95/w1/R95MMutC1-mutants-c1b.json` | the same set regenerated against the L1's `c1b` candidate: 88 counted + 1 equivalent | `fec738028ce834589188ec1b58886668f3ecd7f324295302754e8ce9cf5b4e60` |
| `.ufo/waves/round-95/w1/R95MMutC1-cases-c1b.json` | the 51 cases + `nest-04-513` (c1b's `MAX_NEST` makes `nest_ge` countable) | `30eaa2d486064a55640f30a53c5cd6a2851d49b4a31dfb6196c8f0d1585865d0` |
| `.ufo/waves/round-95/w1/R95MMutC1.md` | this report | — |

Scratch helpers cited in the command table are kept as `R95MMutC1-check-cases.py` and `R95MMutC1-c1b-variant.py`.

## Method

- 89 mutants, each a single `find` -> `replace` on the candidate; every `find` occurs **exactly once** in the
  candidate (checked programmatically: 89/89 unique, 0 duplicates). Each mutant copy is written next to a copy of
  `mado-mimeglob.py`, `py_compile`d, and run with `/usr/bin/python3 -I` and `PATH` = an empty directory.
- 74 cases in the declaration's CASE FILE SCHEMA (one input each), materialised under the scratch; labels from the
  compiled oracle run as `env -i LC_ALL=C HOME=... [XDG_DATA_HOME=...] XDG_DATA_DIRS=... oracle <0|=NAME> <file>`.
  A case whose oracle run crashes is labelled `["UNSUPPORTED", null]` (3 such cases: `wrap-02-past-2^32` rc -11,
  `nest-03-cycle` rc -11, `bounds-06-value-past-page` rc -11).
- Baseline before mutating: the unmodified candidate answers all 74 cases = **74/74** (so every kill below is a
  behaviour change, not a broken fixture).
- Each mutant is run on all 74 cases; the cheapest killer (min total fixture+input bytes) is kept. The 51 kept
  cases were re-materialised **from the emitted JSON** and the unmodified candidate passes **51/51** of them.

## Result

- **87/87 counted mutants killed** (each by at least one oracle-labelled case); **2 not countable** (arguments
  below). 51 distinct cheapest cases cover all 87.
- The kill map (all killers per mutant, with the mutant's actual output) is `R95MMutC1-killmap.json`.

| mutant | rule | cheapest killer case | oracle label | mutant output |
|---|---|---|---|---|
| `alias_bounds_removed` | the alias list header is bounds-checked | `bounds-04-alias-list` | app/child 0 | exit 3 |
| `alias_first_cache` | the alias is searched in every cache | `alias-04-second-cache-nontext` | app/old 0 | app/old 1 |
| `alias_lt_ge` | binary search on strcmp < 0 | `alias-03-nontext` | app/old 0 | app/old 1 |
| `alias_return_name` | the alias list maps the name | `alias-03-nontext` | app/old 0 | app/old 1 |
| `byte_past_mapping` | a cache read past the zero-filled last page is refused | `bounds-06-value-past-page` | UNSUPPORTED | exit 1 (IndexError: index out of range) |
| `cache_order_reversed` | caches are consulted in directory order | `prio-01-equal-caches` | app/first 0 | app/second 0 |
| `child_bounds_after_value` | a child list that fails the bounds check makes the matchlet false before its own test | `bounds-07-child-before-value` | text/plain 0 | exit 3 |
| `child_fail_aborts` | a matchlet holds when any child holds | `nest-01-child-holds` | app/nest 0 | application/octet-stream 1 |
| `child_stride_16` | child = child_offset + 32 * i | `nest-01-child-holds` | app/nest 0 | application/octet-stream 1 |
| `desktop_guard_removed` | the desktop rule needs a filename | `desktop-01-no-name` | application/x-desktop 0 | text/plain 0 |
| `desktop_is` | the desktop test is strcmp | `desktop-02-with-name` | text/plain 0 | application/x-desktop 0 |
| `desktop_replacement` | a sniffed desktop with a name becomes text/plain | `desktop-02-with-name` | text/plain 0 | text/x-desktop 0 |
| `empty_constant_value` | EMPTY is application/x-zerosize | `zerosize-01-empty` | application/x-zerosize 0 | application/x-empty 0 |
| `entries_bounds_removed` | the magic entry array is bounds-checked | `bounds-02-entry-array` | text/plain 0 | exit 3 |
| `entries_reversed` | the first match entry in cache order is returned | `order-03-two-entries` | app/first 0 | app/second 0 |
| `entry_mlo_field` | matchlet_offset = GET_UINT32(offset + 12) | `alias-03-nontext` | app/old 0 | app/old 1 |
| `entry_mo_field` | mimetype_offset = GET_UINT32(offset + 4) | `alias-02-second-cache` | text/x-old 0 | text/x-old 1 |
| `entry_nm_field` | n_matchlets = GET_UINT32(offset + 8) | `alias-03-nontext` | app/old 0 | app/old 1 |
| `entry_oob_break` | an out-of-bounds matchlet list skips its entry | `bounds-03-entry-matchlets` | app/second 0 | text/plain 0 |
| `entry_prio_field` | priority = GET_UINT32(offset) | `nameN-01-two-types` | app/hi 0 | t/one 1 |
| `fallback_127` | the fallback reads the first 128 bytes | `fallback-06-127th` | application/octet-stream 1 | text/plain 0 |
| `fallback_129` | the fallback reads the first 128 bytes | `fallback-07-129th` | text/plain 0 | application/octet-stream 1 |
| `fallback_cr` | 13 is allowed by the fallback | `fallback-11-cr-del` | text/plain 0 | application/octet-stream 1 |
| `fallback_first_name_last` | none -> the first name type, uncertain | `bounds-05-parent-list` | app/child 1 | text/x-old 1 |
| `fallback_space` | a byte < 32 other than 9, 10, 13 -> UNKNOWN | `fallback-10-space-del` | text/plain 0 | application/octet-stream 1 |
| `fallback_tab` | 9 is allowed by the fallback | `fallback-12-tab-del` | text/plain 0 | application/octet-stream 1 |
| `fallback_text_prio` | the fallback keeps priority 0 | `alias-01-unaliased` | text/x-old 0 | text/plain 0 |
| `fallback_text_to_unknown` | text data -> the TEXTPLAIN constant | `fallback-07-129th` | text/plain 0 | application/octet-stream 1 |
| `fallback_unknown_to_text` | binary data -> the UNKNOWN constant | `fallback-02-binary` | application/octet-stream 1 | text/plain 0 |
| `first_match_skipped` | a matching entry is returned at once | `alias-03-nontext` | app/old 0 | app/old 1 |
| `len_check_ge` | stop false as soon as i + value_length exceeds len | `alias-03-nontext` | app/old 0 | app/old 1 |
| `lltext_126` | 0x7f is rejected (not 0x7e) | `lltext-06-del` | application/octet-stream 1 | text/plain 0 |
| `lltext_128` | looks_like_text scans the whole data | `lltext-08-past-128` | application/octet-stream 1 | text/plain 0 |
| `lltext_13` | 0x0d is not rejected | `lltext-05-0d` | text/plain 0 | application/octet-stream 1 |
| `lltext_15` | no byte 0x0e-0x1f | `lltext-04-0e` | application/octet-stream 1 | text/plain 0 |
| `lltext_inverted` | looks_like_text is the negation of the control scan | `fallback-02-binary` | application/octet-stream 1 | text/plain 0 |
| `lltext_le8` | 0x08 (backspace) passes looks_like_text | `lltext-01-backspace` | text/plain 0 | application/octet-stream 1 |
| `lltext_lt7` | no byte 0x00-0x07 | `lltext-02-bel` | application/octet-stream 1 | text/plain 0 |
| `lltext_no127` | 0x7f is rejected | `lltext-06-del` | application/octet-stream 1 | text/plain 0 |
| `magic_list_bounds_removed` | the magic list header is bounds-checked | `bounds-01-magic-list` | text/plain 0 | exit 3 |
| `magic_list_off_20` | list_offset = GET_UINT32(buffer, 24) | `alias-03-nontext` | app/old 0 | app/old 1 |
| `mask_data_unmasked` | data byte compared under the mask | `mask-01-basic` | app/masked 0 | application/octet-stream 1 |
| `mask_ignored` | with a mask, every byte compared under the mask | `mask-01-basic` | app/masked 0 | application/octet-stream 1 |
| `mask_value_unmasked` | value byte compared under the mask | `mask-02-value-bits` | app/m2 0 | application/octet-stream 1 |
| `matchlets_short` | every matchlet of an entry is tried | `alias-03-nontext` | app/old 0 | app/old 1 |
| `max_nest_zero` | MAX_NEST = 100000 | `nest-01-child-holds` | app/nest 0 | exit 3 |
| `name_always_null` | the filename is passed when --name is given | `alias-01-unaliased` | text/x-old 0 | text/plain 0 |
| `name_basename_removed` | the basename is passed to the name step | `name1-03-basename-literal` | t/single 0 | app/hi 0 |
| `name_one_type_ge` | exactly one name type -> it, certain | `alias-01-unaliased` | text/x-old 0 | app/child 0 |
| `nest_raise_removed` | nested deeper than 100000 is refused | `nest-03-cycle` | UNSUPPORTED | hang (no exit within 10 s) |
| `no_children_false` | a matchlet holds when it has no children | `alias-03-nontext` | app/old 0 | app/old 1 |
| `no_types_uncertain_one` | no name type: uncertain only for UNKNOWN | `bounds-01-magic-list` | text/plain 0 | text/plain 1 |
| `prio_strict_gt` | a cache's answer replaces the running one only when its priority is strictly greater | `prio-01-equal-caches` | app/first 0 | app/second 0 |
| `prio_threshold_79` | the priority threshold is 80 | `prio-05-79` | t/one 1 | app/lo79 0 |
| `prio_threshold_gt` | a sniffed type wins outright when priority >= 80 | `prio-04-exactly-80` | app/p80 0 | t/one 1 |
| `prio_unsigned` | priorities are ints (>= 2^31 negative) | `prio-02-negative` | text/plain 0 | app/neg 0 |
| `priority_ge_zero` | a cache answer is used only when priority > 0 | `alias-01-unaliased` | text/x-old 0 | app/child 1 |
| `range_end_inclusive` | while i < range_start + range_length | `range-02-end-exclusive` | text/plain 0 | app/endx 0 |
| `range_end_mask` | range_length 32-bit wrap in range_start + range_length | `wrap-01-range-wrap` | text/plain 0 | app/wrap 0 |
| `range_start_zero` | for i from range_start | `wrap-02-past-2^32` | UNSUPPORTED | text/plain 0 |
| `read_4096` | the data is the whole file | `range-03-beyond-4096` | app/far 0 | text/plain 0 |
| `s32_mask` | the sign bit is 0x80000000 | `prio-02-negative` | text/plain 0 | app/neg 0 |
| `slash_rule` | a trailing / is inode/directory | `slash-01-directory` | inode/directory 1 | app/hi 0 |
| `slash_uncertain` | the directory answer is uncertain | `slash-01-directory` | inode/directory 1 | inode/directory 0 |
| `sniffed_always` | a sniffed type other than UNKNOWN wins | `nameN-02-unknown-sniffed` | t/one 1 | t/one 0 |
| `stack_empty` | the traversal starts from the top matchlet | `nest-01-child-holds` | app/nest 0 | application/octet-stream 1 |
| `subclass_break_removed` | the search stops after the first matching parent entry | `alias-01-unaliased` | text/x-old 0 | hang (no exit within 10 s) |
| `subclass_certain_one` | a subclass name type is certain | `alias-01-unaliased` | text/x-old 0 | text/x-old 1 |
| `subclass_eq_removed` | equal unaliased names are subclasses | `alias-03-nontext` | app/old 0 | app/old 1 |
| `subclass_first_cache` | every cache's parent list is searched | `subclass-08-second-cache` | app/child 0 | app/child 1 |
| `subclass_loop_reversed` | the first name type that is a subclass wins | `subclass-03-supertype` | app/x 0 | app/y 0 |
| `subclass_media_slice` | xdg_mime_media_type_equal compares up to and including / | `subclass-04-media-slice` | app/x 1 | app/x 0 |
| `subclass_octet_inode` | base application/octet-stream and mime not inode/* | `subclass-06-octet-inode` | app/y 0 | inode/x 0 |
| `subclass_parents_bounds_removed` | the parent list header is bounds-checked | `bounds-05-parent-list` | app/child 1 | exit 3 |
| `subclass_recurse_base` | the parent is tested against the base | `bounds-04-alias-list` | app/child 0 | app/child 1 |
| `subclass_seen_removed` | parents already seen are skipped | `subclass-07-cycle` | app/a 1 | exit 1 (RecursionError: maximum recursion depth exceeded) |
| `subclass_super_slash` | base x/* with the same media type | `subclass-03-supertype` | app/x 0 | app/x 1 |
| `subclass_text_media_removed` | base text/plain and mime text/* | `alias-01-unaliased` | text/x-old 0 | app/child 0 |
| `textplain_constant_value` | TEXTPLAIN is text/plain | `alias-01-unaliased` | text/x-old 0 | app/child 1 |
| `unknown_constant_value` | UNKNOWN is application/octet-stream | `fallback-02-binary` | application/octet-stream 1 | application/x-unknown 1 |
| `unknown_identity_guess` | UNKNOWN is compared by pointer | `fallback-09-magic-octet` | application/octet-stream 0 | text/plain 0 |
| `unknown_identity_uncertain` | UNKNOWN is compared by pointer (uncertain) | `fallback-09-magic-octet` | application/octet-stream 0 | application/octet-stream 1 |
| `unsupported_exit_zero` | UNSUPPORTED exits 3 | `bounds-06-value-past-page` | UNSUPPORTED | exit 0 (no JSON) |
| `wrap_raise_removed` | i + value_length past 2^32 is refused | `wrap-02-past-2^32` | UNSUPPORTED | text/plain 0 |
| `zerosize_prio_zero` | empty data -> priority 100 | `zerosize-02-two-names` | application/x-zerosize 0 | t/one 1 |
| `zerosize_removed` | empty data -> application/x-zerosize with priority 100 | `zerosize-01-empty` | application/x-zerosize 0 | text/plain 0 |
| `zerosize_type_text` | empty data -> the EMPTY constant | `zerosize-01-empty` | application/x-zerosize 0 | text/plain 0 |

## Not counted (2)

### `nest_ge` — the nest limit is `> 100000` (mutant: `>= MAX_NEST`)

Not countable under the case schema. A chain of N matchlets reaches stack depth **N-1** (the last node has no
children and returns before a push), so the only separating input is **N = 100001**: there the correct tool answers
(measured rc 0, `app/deep 0`) while the mutant raises (rc 3) — but the oracle's C recursion overflows its 8 MiB stack
at that depth (measured SIGSEGV, rc 139), so the case's label is `UNSUPPORTED` and the correct tool itself must exit 3
-> the case would be a **false kill of the correct tool**. At N >= 100002 both the correct tool and the mutant exit 3
(measured); at N <= 100000 both answer identically (measured at 50000 and 100000). No oracle-labelled case separates
them.

### `text_mode_removed` — text mode is refused (mutant: `if False:`)

Not countable under the case schema. The distinguishing input is a directory with no loadable `mime.cache`; there the
oracle **always answers** (it reads the `magic`/`globs2` text files: measured `globs2` = `50:text/x-text:*.txt` with
name `x.txt` -> `text/x-text 0`), so a case's label can never be `UNSUPPORTED` (the schema reserves that for an oracle
crash or hang) and a text-mode case would be a **false kill of the correct tool**. The refusal is C1's declared named
limit ("cache mode only"), not a rule a case can measure. See finding F3.

## Findings (candidate defects, with reproducing cases)

### F1 — `looks_like_text` allows VT (0x0b); GLib rejects it

- `tools/mado-mimesniff.py:208` (`return not any(b < 8 or 14 <= b < 32 or b == 127 for b in data)`) omits `b == 11`.
  The installed GLib's `g_ascii_isspace(0x0b)` is **0** (measured with a C probe against `gio-2.0` 2.90.1), so
  `looks_like_text` in `gcontenttype-fdo.c:533-548` rejects VT. The docstring's "i.e." set at line 15
  (`0x00-0x07, 0x0e-0x1f, 0x7f`) is wrong for the same reason, and selftest check `s10 VT passes looks_like_text`
  (line 467) encodes the bug.
- Reproducing case (schema; 80-byte empty cache, base64
  `AAEAAgAAACgAAAAsAAAAMAAAADQAAAA8AAAAQAAAAEwAAABMAAAATAAAAAAAAAAAAAAAAAAAAAAAAAA8AAAAAAAAAAAAAAAAAAAATAAAAAA=`):
  `{"id":"lltext-vt-01","class":"lltext","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1:{root}/s2"},"files":{"dh/mime/mime.cache":"<that base64>"},"inputs":[{"name_b64":null,"data_b64":"YWILY2Q="}],"labels":[["application/octet-stream",1]]}`
  (`data_b64` = `ab\x0bcd`).
- Measured: oracle `application/octet-stream 1`; candidate `text/plain 0`. Also on the host DBs (no synthetic cache):
  `printf 'ab\x0bcd' > vt.bin; env -i LC_ALL=C HOME=$S/probe/h $S/oracle 0 vt.bin` -> `application/octet-stream 1`;
  the tool with `--data-home-unset --data-dirs-unset` -> `text/plain 0`.
- Sweep: all 256 one-byte inputs through both (one cache present) -> exactly **1** divergence, byte `0x0b`.
- Peers hit the same: `w1/R95MScribeEntry-case-vt.json` (0/1 against the unmodified candidate) and
  `w1/R95MCritic-cases.json` `lltext-01-vt-only`, `lltext-02-vt-in-text` (both fail).
- Fix: add `or b == 11` at line 208 and correct the docstring/selftest.

### F2 — the 32-bit wrap check raises before the length check (over-refusal)

- `tools/mado-mimesniff.py:112-114`: the tool raises `Unsupported` whenever `i + value_length > M32`, but the C
  computes `i + data_length` in 32-bit arithmetic and returns FALSE when the **wrapped** sum exceeds `len`
  (`xdgmimecache.c:167-210`). The raise must come **after** the length test and only when the wrapped sum passes it:
  `total = (i + value_length) & M32; if total > len(data): return False; if i + value_length > M32: raise ...`.
- Reproducing case: `w1/R95MCritic-cases.json` `wrap-01-wrapped-sum-above-len` (matchlet `start=0xFFFFFFF0,
  length=2, value_length=32, value_offset=44`, data `ABCD`, label `text/plain 0`): the oracle returns `text/plain 0`,
  the candidate exits 3. Measured directly: tool rc 3, oracle rc 0 `text/plain 0`.
- Contrast (the refusal is right there): `wrap-02-past-2^32` (`start=0xFFFFFFF0, length=0xF, value_length=32`,
  data 16 bytes) -> wrapped sum 16 <= len 16, the C really does `memcmp(data + 0xFFFFFFF0, ...)` -> SIGSEGV (rc 139);
  the candidate exits 3 = correct.

### F3 — the text-mode refusal cannot be exercised by an oracle-labelled case

The oracle answers in text mode (measured `text/x-text 0`), the tool exits 3. A text-mode case in the shared schema
would therefore fail the correct tool. Either the frozen `mode` class stays cache-present only (my
`mode-01-cache-beats-text` is such a control: cache in `dh`, `globs2` in `s1`, answer `app/hi 0`), or the schema needs
an explicit "tool must refuse" label for this declared limit. ExecCasesC1 and the L1 must decide; I did not put a
text-mode case in my cases file.

### F4 — one mutant is killed by a hang, so the counter needs a per-case tool timeout

`nest_raise_removed` is killed by `nest-03-cycle` only because the unmutated tool raises at 100001 frames while the
mutant loops forever. My harness bounds each tool run at 10 s. If the frozen counter has no tool timeout, that mutant
will hang the measurement instead of being killed.

### F5 — the mutants are pinned to the candidate bytes

Every `find` is a substring of sha256 `a13b6e0e...`. c1b (sha256 `abef0014...`) touches five of them; the
regenerated and verified set is `R95MMutC1-mutants-c1b.json` + `R95MMutC1-cases-c1b.json` (section above). Any
further candidate edit requires the same regeneration.

## c1b variant (the L1's second candidate, sha256 `abef0014…`)

`build/mado-mimesniff.c1b.py` (sha256 `abef00143e306fbdc970cc04b2af576e492e570a2b5d6430bf09f97f6895006c`) fixes both
defects this seat found — F1 (`b == 11` added at `looks_like_text`, docstring and selftest s10 corrected) and F2 (the
wrapped-sum test moved before the refusal) — and changes `MAX_NEST` from 100000 to 512. Five of the 89 `find` strings
no longer occur in c1b (`wrap_raise_removed`, `len_check_ge`, `nest_raise_removed`, `max_nest_zero`, `lltext_lt7`);
the other 84 are unchanged. I regenerated the set against c1b and verified it end to end:

- `w1/R95MMutC1-mutants-c1b.json` (sha256 `fec738028ce834589188ec1b58886668f3ecd7f324295302754e8ce9cf5b4e60`):
  **88 counted + 1 equivalent** (`text_mode_removed`). `nest_ge` becomes countable on c1b: with `MAX_NEST = 512` a
  513-deep chain reaches stack depth 512 (not > 512) and answers, the mutant raises, and the oracle answers at 513
  (measured `app/deep 0`) — a valid kill.
- `w1/R95MMutC1-cases-c1b.json` (sha256 `30eaa2d486064a55640f30a53c5cd6a2851d49b4a31dfb6196c8f0d1585865d0`): the 51
  cases + `nest-04-513` (16.5 KB cache, oracle `app/deep 0`).
- c1b `--selftest`: `checks=23 failed=0` (rc 0). c1b baseline on the 52 cases: **52/52**. Counted mutants killed:
  **88/88**, no survivors.

### F6 — c1b's `MAX_NEST = 512` refuses chains GLib answers

Measured with a 1000-matchlet chain: oracle `app/deep 0` (rc 0), c1b exit 3 (`matchlet children nested past 512`).
The C recursion survives 50000 (measured rc 0) and overflows at 100000 (measured SIGSEGV), so depths 514..~50000 are
legitimate inputs that c1b refuses. The declaration's named limit still says "nested deeper than 100000". Either
re-freeze the declaration with the 512 limit — and then no frozen `nest` case may use a chain deeper than 513 — or
keep 100000 (then the c1 package above applies and `nest_ge` stays `equivalent_not_counted`). The two packages are
each internally consistent; the declaration must match whichever candidate is frozen.

## Peer cross-check (DRAFT)

- `w1/R95MCritic-cases.json` against the unmodified candidate: **2/5** (failures: `lltext-01-vt-only`,
  `lltext-02-vt-in-text` -> F1; `wrap-01-wrapped-sum-above-len` -> F2).
- `w1/R95MScribeEntry-case-vt.json`: **0/1** (F1).
- `.ufo/waves/round-95/controls/mimesniff-cases-r95.json` (R95MExecCasesC1) was **absent** when this seat closed, so
  the cross-run against the frozen case file was not performed.

## Commands run (exit codes)

| command (in `$S`) | rc | result |
|---|---|---|
| `cc -O0 -o "$S/oracle" .../mimesniff-oracle-r95.c $(pkg-config --cflags --libs gio-2.0)` | 0 | oracle built |
| `env -i PATH=$S/emptybin LC_ALL=C HOME=$S/h /usr/bin/python3 -I tools/mado-mimesniff.py --selftest` | 0 | `checks=23 failed=0` |
| `python3 harness.py prepare` | 0 | 74 cases labelled by the oracle (3 UNSUPPORTED by crash) |
| `python3 harness.py baseline` | 0 | `74/74 ok` |
| `python3 harness.py mutants` | 0 | 87 killed, 2 survivors (`nest_ge`, `text_mode_removed`) |
| `python3 pick.py` | 0 | 51 cheapest cases |
| emitted-cases re-check from `R95MMutC1-cases.json` | 0 | `51/51 ok` |
| 256-byte sweep, oracle vs candidate | 0 | 1 divergence (`0x0b`) |
| `python3 check_cases.py w1/R95MCritic-cases.json` | 0 | `2/5 ok` |
| `python3 check_cases.py <scribe vt case>` | 0 | `0/1 ok` |
| oracle at nest depth 50000 / 100000 / 100001 / 100002 | 0 / 139 / 139 / 139 | 139 = SIGSEGV |
| candidate tool at depth 100001 / 100002 | 0 / 3 | answers / raises |
| `nest_ge` mutant at depth 100001 / 100002 | 3 / 3 | raises / raises |
| oracle text mode (`globs2` + name `x.txt`) | 0 | `text/x-text 0`; tool rc 3 |
| c1b `--selftest` / baseline / mutant sweep on the 52 c1b cases | 0 | `checks=23 failed=0`; 52/52 baseline; 88/88 killed |

No installs or upgrades were made; no pacman transaction was run. No host file outside `/usr` and the lane was read;
`update-mime-database` was never run (no `real` case was built by this seat).

## Scratch

`/fast/scratch/hyaku/mado-r95/R95MMutC1` deleted on exit; the cited artifacts above are the copies kept in `w1/`.
