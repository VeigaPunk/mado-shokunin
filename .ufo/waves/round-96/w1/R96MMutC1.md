# R96MMutC1 — mutation report: the C1 TEXT-mode magic candidate

Seat: mutation tester for the C1 coverage claim (the text-mode `mime/magic` parser + matcher behind
`g_content_type_guess`). I mutated the C1 candidate only; the candidate, the cases, the counters and the
sibling lane were never written.

## Anchored bytes (the deliverable is pinned to these)

- candidate: `.ufo/waves/round-96/build/mado-mimetext.c1.py`
- **sha256 `d5f174fc33d0b1f1847897a8e63724c7112137c1bf58a89508d1c1c13b857cbd`**, 44,244 B, 983 lines,
  mtime 12:10 (the L1's final draft; the 951a4923 and bde03578 builds I measured first are superseded and
  are not the bytes this set is anchored to)
- candidate `--selftest` on a lone copy: `MADO_MIMETEXT_SELFTEST: checks=50 failed=0`
- mutant file: `.ufo/waves/round-96/controls/magictext-mutants-r96.json`,
  **sha256 `b7b964c637980af002ac4cfa5f040164362eeef011b9c1a0874ed4b6e8dce863`**
  (schema `{"mutants":[{"id","rule","find","replace","class"}],"equivalent_not_counted":[...]}`, r95 shape)
- **97 counted mutants** + **14 `equivalent_not_counted`** entries with arguments
- every `find` occurs **exactly once in the whole candidate file** (the counter's rule) and in non-selftest
  code: 95 before `def selftest(`, 2 inside `main()`; the builder refuses to emit a variant otherwise
- one class per mutant, 4-9 per class, 16/16 classes:
  header 4, sect 9, value 7, mask 6, word 7, range 8, indent 8, order 7, drop 4, multi 4, glob 8,
  alias 7, fallback 6, zerosize 5, mode 4, desktop 3

The name step (globs2/globs, literal/suffix/fnmatch, weights, the suffix trie) and the cache-loadability
rule live in the sibling `tools/mado-mimeglob.py`, which the candidate imports through its one pinned
`spec_from_file_location`; those rules are outside the candidate's mutable bytes and are declared in
`equivalent_not_counted`, not silently dropped.

## Runner (exact commands, replayed verbatim)

The draft lives in `build/`, where its sibling is absent. The tool loads `mado-mimeglob.py` from its own
directory, so the measurement uses a staged copy exactly as `tools/` will look:

    S=/fast/scratch/hyaku/mado-r96/R96MMutC1
    mkdir -p "$S/tool"
    cp .ufo/waves/round-96/build/mado-mimetext.c1.py "$S/tool/mado-mimetext.py"
    cp tools/mado-mimeglob.py "$S/tool/"

Baselines (a baseline failure is inconclusive, not a killed mutant):

    python3 -I "$S/run_cases.py" --tool "$S/tool/mado-mimetext.py" --cases "$S/probe-cases.json" \
      --scratch "$S/base" --jobs 16
    python3 -I "$S/run_cases.py" --tool "$S/tool/mado-mimetext.py" \
      --cases .ufo/waves/round-96/controls/magictext-cases-r96.json --scratch "$S/basedraft2" --jobs 16

Mutants (`mutants.py` applies each `find`/`replace`, stages the variant beside the sibling, runs the same
comparison, and writes the per-mutant kill lists):

    python3 "$S/mutants.py" --tool "$S/tool/mado-mimetext.py" --mutants "$S/mut.json" \
      --cases "$S/probe-cases.json" --scratch "$S/mrun" --jobs 24 --out "$S/probe-summary.json"
    python3 "$S/mutants.py" --tool "$S/tool/mado-mimetext.py" --mutants "$S/mut.json" \
      --cases .ufo/waves/round-96/controls/magictext-cases-r96.json --scratch "$S/mrund2" --jobs 24 \
      --out "$S/draft-summary.json"
    python3 "$S/analyse.py" --scratch "$S/mrund2" \
      --cases .ufo/waves/round-96/controls/magictext-cases-r96.json \
      --summary "$S/draft-summary.json" --out "$S/draft-kinds.json"   # kills that are refusals/crashes

One case invocation (per input, because the CLI's `--name` applies to every FILE):

    env -i LC_ALL=C PATH=/usr/bin:/bin HOME=<root>/h \
      python3 -I "$S/tool/mado-mimetext.py" <datafile> [--name <NAME>] --home <root>/h \
      [--data-home <root>/dh | --data-home-unset] --data-dirs <root>/d1:<root>/d2

and the variant's **last parsed `MADO_MIMETEXT:` line** (or `UNSUPPORTED`) is compared to the case's label
pair. A kill is a case where the pristine candidate is exactly right and the variant's parsed answer
differs; no answer line (traceback, rc != 0) is recorded as ERROR and is **not** a kill. The crash check
(`analyse.py`) confirmed every counted kill is a wrong answer: `no-genuine-answer 0` on both sets.

## Two case sets (why two)

1. **The cases seat's draft** `.ufo/waves/round-96/controls/magictext-cases-r96.json`
   (sha256 `4b3645ae83f6bb1822ebdacd4e42c2dc0fdd152bdca8fc4ff558985052f1d565`, 284 cases, 16 classes).
   This is the set the frozen file is made from; the kill numbers that matter are against it.
2. **My probe set** (`$S/probe-cases.json`, 171 cases, 244 inputs, all 16 classes, every label from the
   compiled round-95 oracle via `env -i LC_ALL=C HOME=... XDG_DATA_DIRS=...`; the four cache-mode cases
   carry the contract's `["UNSUPPORTED",null]`). It is not a deliverable; its job is to name the exact
   fixture that closes a gap when the draft does not kill a mutant.

Baselines on the anchored bytes: probe `cases=171 passed=171 failed=0` (both CLI modes, flags and env);
draft `cases=284 passed=284 failed=0`. There is therefore no inconclusive mutant.

## Kill table — the draft case set (284 cases)

`class_kills = 16/16`; killed **84/97**; 265 of the 284 draft cases kill at least one mutant.

| class | mutants | killed | one killing mutant | its first killing draft case |
|---|---|---|---|---|
| header | 4 | 2 | `header-gate-removed` | `header-03-gate-wrong-case-inert` |
| sect | 9 | 9 | `sect-priority-empty-becomes-0` | `sect-21-priority-less` |
| value | 7 | 5 | `value-length-little-endian` | `alias-01-data-answer-raw-type` |
| mask | 6 | 5 | `mask-any-byte-starts-mask` | `alias-01-data-answer-raw-type` |
| word | 7 | 7 | `word-zero-rejected` | `word-05-word0-odd-length-matches` |
| range | 8 | 8 | `range-default-zero` | `alias-01-data-answer-raw-type` |
| indent | 8 | 8 | `indent-default-one` | `indent-20-omitted-indent-zero` |
| order | 7 | 7 | `order-ascending` | `multi-03-priority-beats-dir-order` |
| drop | 4 | 4 | `drop-error-section-kept` | `drop-01-bad-line-drops-whole-section` |
| multi | 4 | 4 | `multi-dir-order-reversed` | `drop-17-eof-mid-line-no-matchlet-inert` |
| glob | 8 | 7 | `glob-single-type-not-early` | `alias-05-single-alias-name-early-return` |
| alias | 7 | 3 | `alias-unalias-skipped` | `alias-02-subclass-tiebreak-via-alias` |
| fallback | 6 | 6 | `fb-all-bytes` | `fallback-04-control-at-128-ignored` |
| zerosize | 5 | 5 | `zs-unknown` | `mode-15-none-with-home-only` |
| mode | 4 | 1 | `mode-no-cache-refusal` | `mode-04-declared-refusal-cache-valid-in-d1` |
| desktop | 3 | 3 | `desk-no-rename` | `desktop-01-magic-desktop-named-no-types` |

(The "first killing draft case" is the lexicographically first in the kill list, not a claim that the
draft case is specific to that rule.)

## Kill table — my probe set (171 cases)

`class_kills = 16/16`; killed **94/97**; 156 probe cases kill at least one mutant.

| class | mutants | killed | one killing mutant | its first killing probe case |
|---|---|---|---|---|
| header | 4 | 4 | `header-gate-removed` | `header-01-wrong-byte` |
| sect | 9 | 9 | `sect-priority-empty-becomes-0` | `sect-16-empty-priority` |
| value | 7 | 7 | `value-length-little-endian` | `alias-05-octet-base` |
| mask | 6 | 6 | `mask-any-byte-starts-mask` | `alias-05-octet-base` |
| word | 7 | 7 | `word-zero-rejected` | `word-05-zero` |
| range | 8 | 8 | `range-default-zero` | `alias-05-octet-base` |
| indent | 8 | 8 | `indent-default-one` | `alias-05-octet-base` |
| order | 7 | 7 | `order-ascending` | `multi-01-dir-priority` |
| drop | 4 | 4 | `drop-error-section-kept` | `drop-01-badline` |
| multi | 4 | 4 | `multi-dir-order-reversed` | `multi-03-tie` |
| glob | 8 | 8 | `glob-single-type-not-early` | `desktop-02-name` |
| alias | 7 | 7 | `alias-unalias-skipped` | `alias-01-unalias-eq` |
| fallback | 6 | 6 | `fb-all-bytes` | `fallback-05-after128` |
| zerosize | 5 | 5 | `zs-unknown` | `mode-01-none` |
| mode | 4 | 1 | `mode-no-cache-refusal` | `mode-04-cache` |
| desktop | 3 | 3 | `desk-no-rename` | `alias-06-desktop-base` |

The 16/16 class kills hold on both sets. The mutants that only my probe set kills are the gaps below: they
are not evidence of a tool defect, they are the places where the draft's fixtures do not separate the rule
from its mutant.

## No draft case kills these (13 survivors) — what the cases must close

Each line names the rule, the mutant (in the frozen JSON, with `rule`/`find`/`replace`), and the fixture
that kills it in my probe set. The last three are not per-input-label observable at all (see G2).

### G1. Case gaps: a fixture exists and is named (10)

1. `header-gate-11-prefix` — the gate must compare all 12 bytes including the trailing newline; the mutant
   accepts an 11-byte prefix. **Fixture** (probe `header-12-bad-prefix-then-section`): one magic file
   `b"MIME-Magic\0Z" + "[50:text/x-h12]\n>0=\x00\x02AB\n"`; input data `b"AB"`, name NULL. Correct
   `text/plain 0` (gate fails); the mutant parses the section and answers `text/x-h12 0`.
2. `header-gate-10-prefix` — same rule, the mutant accepts `MIME-Magic` plus any two bytes. Same fixture
   kills it.
3. `value-trailing-byte-ends-line` — a matchlet line must end with `\n`; any other trailing byte is a parse
   error for the section. **Fixture** (probe `value-12-trailing-junk`): sections
   `[50:text/x-v12]` with `b">0=\x00\x02AB!\n"` (the `!` after the value), then a lower-priority
   `[10:text/x-v12b]` with `b">0=\x00\x02AB\n"`; data `b"AB"`. Correct `text/x-v12b 0` (the bad line drops
   the whole first section); the mutant keeps the matchlet and answers `text/x-v12 0`.
4. `value-eof-keeps-matchlet` — EOF in the middle of a matchlet frees it; the section is still inserted but
   its tree cannot hold. **Fixture** (probe `value-13-eof-mid-line`): magic bytes
   `b"MIME-Magic\0\n[50:text/x-v13]\n>3=\x00\x02AB"` (no trailing newline after the value); data
   `b"xxxAB"` (so a kept matchlet at offset 3 would match). Correct `text/plain 0`; the mutant answers
   `text/x-v13 0`.
5. `mask-short-read-error` — a truncated mask at EOF is the EOF state (the section survives with the
   matchlets already parsed); the mutant calls it a parse error and drops the section. **Fixture** (probe
   `mask-09-truncated-after-match`): magic
   `b"MIME-Magic\0\n[50:text/x-m9]\n>0=\x00\x02AB\n>2=\x00\x02CD&\xff"` (EOF in the mask); data `b"AB"`.
   Correct `text/x-m9 0`; the mutant answers `text/plain 0`.
6. `glob-full-name-not-basename` — the name is reduced to its basename before the glob lookup. **Fixture**
   (probe `glob-13-basename`): no magic section (`mime/magic` is the 12-byte gate only), `globs2`
   `b"50:text/x-g13:sub/*\n"`, input name `b"sub/a"` with data `b"hi"`. Correct `text/plain 0` (the
   basename is `a`); the mutant matches the full name and answers `text/x-g13 0`.
7. `alias-split-last-space` — an aliases line is split at its FIRST space (the last byte of the remainder is
   chopped). **Fixture** (probe `alias-10-two-spaces`): `globs2` `b"60:text/x-a10:*.a10\n50:text/x-a10b:*.a10\n"`,
   `aliases` `b"text/x-a10 text/x-a10can extra\n"`, magic section `[50:text/x-a10can extra]` with
   `b">0=\x00\x02AB\n"`, input name `b"a.a10"`, data `b"AB"`. Correct `text/x-a10 0` (the alias resolves
   to the sniffed type, certain); the last-space mutant resolves to `extra` and answers `text/x-a10 1`.
8. `alias-parent-one-level` — the subclasses parents are followed recursively. **Fixture** (probe
   `alias-04-subclass-transitive`): `globs2` `b"60:application/x-a4a:*.a4\n50:text/x-a4:*.a4\n"`,
   `subclasses` `b"text/x-a4 text/x-a4mid\ntext/x-a4mid text/x-a4base\n"`, magic
   `[50:text/x-a4base]` with `b">0=\x00\x02AB\n"`, input name `b"a.a4"`, data `b"AB"`. Correct
   `text/x-a4 0` (a two-level parent chain); the mutant stops after one level and answers `text/x-a4 1`.
9. `alias-text-super-off` — `text/plain` is a supertype of every `text/*`. **Fixture** (probe
   `alias-07-text-base`): `globs2` `b"60:application/x-a7a:*.a7\n50:text/x-a7b:*.a7\n"`, magic
   `[50:text/plain]` with `b">0=\x00\x02AB\n"`, name `b"a.a7"`, data `b"AB"`. Correct `text/x-a7b 0`
   (the first name type that is a subclass, certain); the equality-only mutant answers `application/x-a7a 1`.
10. `alias-octet-super-off` — `application/octet-stream` is a supertype of every type not under `inode/`.
    **Fixture** (probe `alias-05-octet-base`): `globs2`
    `b"60:application/x-a5a:*.a5\n50:application/x-a5b:*.a5\n"`, magic
    `[50:application/octet-stream]` with `b">0=\x00\x02AB\n"`, name `b"a.a5"`, data `b"AB"`. Correct
    `application/x-a5a 0`; the equality-only mutant answers `application/x-a5a 1`.

Also worth adding even though the draft already kills them (they are the geometry cuts the L1 named): a
`[0:type]` section with a matchlet must match (draft `sect-21-priority-less` and my `sect-13` both kill the
`priority > 0` gate), a `~0` matchlet must parse and compare byte-wise (draft
`word-05-word0-odd-length-matches`), and `__NOMAGIC__` must stay a literal value (draft kills
`value-nomagic-deleteall`).

### G2. Not observable through per-input labels (3)

These three are contract-level and were measured directly (two files in one invocation, and the DIRS line):

- `mode-refusal-one-line` — cache mode prints one refusal line per FILE; the mutant prints one line for the
  run. Measured: pristine 2 lines for 2 files, mutant 1 line, both rc 3. A counter that runs one case as
  one invocation sees it; my per-input harness cannot.
- `mode-refusal-exit-zero` — the refusal exits 3 (contract) and the mutant exits 0. Measured: pristine rc 3,
  mutant rc 0, same lines. Only a counter that pins the exit code sees it.
- `mode-none-counts-magic-only` — mode `none` means no text file at all (five names); the mutant counts only
  `mime/magic`. Measured on a dir with `globs2` only: pristine `MADO_MIMETEXT_DIRS: mode=text`, mutant
  `mode=none`; every per-input answer is identical. Only a counter that compares the DIRS line to the case's
  `db_mode` sees it.

If the C1 counter checks rc and the DIRS line (the declaration's clause (i) says "every frozen case exactly"
and the refusal carries `UNSUPPORTED` per file), those three die too; if it compares only the per-input
type/uncertain pairs, they are unkillable by construction and should be read as case-format limits, not
case gaps.

### G3. Declared equivalent — `equivalent_not_counted` (14, with the argument)

| id | rule | why no case can separate it |
|---|---|---|
| `range-bounds-continue` | `i + value_length > len` fails the whole matchlet | monotone in `i`: every later `i` fails too, so FALSE and continue agree for finite data (only a 32-bit `i` wrap could differ) |
| `range-wrap-refused` | `i + value_length` past 2^32 | the Python model has no wrap; the C case is UB (the oracle reads out of bounds), so no oracle-labelled case can exist |
| `word-swap-guard` | the swap block runs only for `word_size > 1` | a size-1 swap is a no-op and size 0 cannot reach the block; `>1`, `>0`, `!=1` agree, and `!=0` divides by zero |
| `drop-skip-to-newline` | a parse error skips to the next newline | skipping one byte ends at the same newline (every non-`[` byte re-enters the error state); measured identical |
| `drop-eof-section-freed` | a parse error at EOF ends the file | returning SECTION at EOF only reaches `parse_header`, which reads EOF and ends the loop |
| `sect-keep-empty-inert` | a matchlet-less section is inserted but can never hold | the `mime_types` elimination loop is outside this surface, so inserted and dropped answer nothing |
| `mode-cache-loadable` | only a loadable `mime.cache` makes cache mode | loadability (size/version) is decided in the sibling `mado-mimeglob.py` Resolver |
| `glob-weights-descending` | name types are sorted by weight, descending | the sort is in the sibling's `finish()`; the list order is covered by `glob-types-reversed` |
| `glob-deepest-suffix` | the deepest suffix glob wins | the suffix trie is in the sibling module |
| `indent-depth-guard` | nesting deeper than 4096 is refused | the only observable effect of weakening it is a refusal, not a wrong type; 4097-deep fixtures are a declared limit (measured: the depth-guard mutant's kills were refusals in both sets, so it was replaced by `indent-skip-current-level`) |
| `header-gate-rewind` | parsing starts just past the 12 header bytes | the gate rejects every non-conforming file, so the only reachable files start exactly `MIME-Magic\0\n`; re-parsing from 0 reads `M` as a bad header, skips to the header's own newline (index 11) and lands on byte 12 (measured: survives 171 probe cases) |
| `order-tie-prepend` | equal priorities keep file order (insert before equals) | each section passes through two insertions (the file's own list, then the global list) and the insert-before-equals permutation is an involution, so the second pass restores file order (measured identical on the tie cases) |
| `fb-cr-treated-binary` | 9, 10, 13 are the allowed controls in the fallback | CR is rejected by the fallback but accepted by `looks_like_text`, which is applied to exactly that UNKNOWN result; the guess still answers `text/plain` (measured survivor) |
| `multi-globs-other-dir` | globs and magic may come from different dirs | both steps read the same dirs list built by the sibling; no mutation in this candidate splits them beyond the covered `multi-*` mutants |

## What the numbers do and do not say

- The set exercises every class on both case sets (16/16), kills 84/97 on the draft and 94/97 on my probe
  set, and every kill is a parsed wrong answer (`no-genuine-answer 0` on both sets).
- The 10 G1 survivors are actionable: the fixture that kills each is given with its exact bytes, and every
  one is an oracle-labelled case in my probe set (the labels above are the oracle's answers, not my model's).
- A killed mutant proves the frozen cases exercise the rule it breaks; it does not prove the rule population
  is complete. The 14 equivalents are argued, not assumed, and two of them were measured survivors before
  being moved out of the counted set.
- Declared limit: the `mime_types` elimination loop is outside the surface (`xdgmime.c:535` passes `NULL, 0`),
  and the 32-bit wrap of `i + value_length` is UB in the oracle, so no labelled case can pin it.

## Tool installs

None. No pacman/uv/npx/binary install this seat; the oracle was compiled in scratch from
`.ufo/waves/round-95/controls/mimesniff-oracle-r95.c` with the host `cc` and `pkg-config gio-2.0`.

## Scratch

`$HYAKU_SCRATCH/mado-r96/R96MMutC1` is removed before yield. The artifacts that matter are the mutant file
above and this report; the probe set and the runner were instruments in scratch and are described here by
their commands and fixtures so the measurement can be rebuilt.
