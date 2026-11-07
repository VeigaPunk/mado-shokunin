# R96MExecToolC1 — w1 report (round mado 96, hyaku 15, wave w1)

Seat: author of the C1 candidate `tools/mado-mimetext.py` (draft:
`.ufo/waves/round-96/build/mado-mimetext.c1.py`, sha256
`d5f174fc33d0b1f1847897a8e63724c7112137c1bf58a89508d1c1c13b857cbd`). Lane base
`9f029f46f01f6cd3a1d29ac39bb548498a1d0c3d`. Report date 2026-11-07.

## Files changed (write scope kept)

- `.ufo/waves/round-96/build/mado-mimetext.c1.py` — the candidate draft (mine). Earlier drafts were
  overwritten in place; the single current draft is the artifact above.
- `.ufo/waves/round-96/w1/R96MExecToolC1.md` — this report.
- Nothing else in the lane was written: no tools/, no quality/, no corpus/, no receipts (my item names
  none), no git/jj state anywhere. Scratch `$S=/fast/scratch/hyaku/mado-r96/R96MExecToolC1` is deleted
  before this report is delivered; every command below was run there or under `$S/proot`, `$S/caseroot`,
  `$S/lone`, `$S/stage`, `$S/fetch`.

## What the draft models (Shared contract 1 + the C1 shared model)

`g_content_type_guess(name-or-NULL, data, len, &uncertain)` for the text database mode:

- magic file gate: 12 bytes exactly `MIME-Magic\0\n` (xdgmimemagic.c:801-819); parse over the bytes past
  the header with a getc/ungetc cursor mirroring the FILE* code.
- sections `[priority:type]` (:230-281): strtol-style number (max 30 digits, >INT_MAX or ERANGE -> -1 ->
  parse error), `:` required, type up to the first `]` on the line (the line read stops at `\n`, `\0`,
  EOF; EOF before the newline drops the section).
- matchlet lines (:301-514): optional indent, `>`, offset (no digits -> error), `=`, two-byte BE value
  length, value, optional `&` mask (same length, short read -> EOF), optional `~` word size in
  {0,1,2,4} (:440-443; 0 behaves like 1 — no swap, no modulus test), optional `+` range (default 1,
  -1 -> error), kept only when the line ends `\n` (:498-514 — a matchlet whose line hits EOF is freed).
- errors (:283-300, :749-782): skip to the next newline, drop the whole section, resume at the next
  line that starts a section; later matchlet lines of a dropped section are each skipped as bad
  headers.
- section insert: one GLOBAL list over all dirs (:596-629), priority descending, ties keep (dir, file)
  order; a section whose header parsed is inserted even with zero matchlets (:735-747) — its tree can
  never hold, so this is unobservable; EOF with a mime type keeps the section.
- tree match (:557-588): matchlets in file order (the C prepends at parse and mirrors at insert; the
  draft appends in file order — equivalent), indent 0 top level, a held test recurses only into a next
  matchlet at exactly indent+1, any-one-at-level semantics, failed parents skip their deeper subtree,
  recursion capped at 4096 frames -> `Unsupported` (declared limit).
- compare (:515-556): i from offset while i < offset+range_length; `i + value_length > len` fails the
  matchlet outright; masked compare ANDs value and data with the mask per byte; LE byte-swap of value
  and mask per 2/4-byte word at parse (:469-505).
- data step (xdgmime.c:516-541): len 0 -> application/x-zerosize priority 100 BEFORE magic; magic
  answer used at any priority (no `prio > 0` gate — :535 passes NULL,0); else the 128-byte
  binary/text fallback (xdgmimeint.c:176-190, only 9/10/13 are spaces).
- guess combination (gcontenttype-fdo.c, round 95's model, mirrored from tools/mado-mimesniff.py):
  trailing `/` -> inode/directory uncertain; exactly one name type -> it, certain (no sniff);
  UNKNOWN + looks_like_text -> text/plain (GLib isspace = 0x09,0x0a,0x0c,0x0d,0x20 — FF passes, VT
  does not); sniffed application/x-desktop with a name -> text/plain; no name type -> sniffed,
  uncertain only if still the UNKNOWN constant (a distinct `_Const` object, so a magic answer
  "application/octet-stream" is NOT the constant and stays certain); several name types -> sniffed
  with priority >= 80 wins, else first name type that is a subclass of it, else first name type
  uncertain.
- text-mode subclass (xdgmime.c:820-891): unalias via the text aliases files (one level), equal, base
  `/*` + media equal, base text/plain + mime text/*, base application/octet-stream + mime not
  inode/*, else subclasses-file parents recursively; the seen-set holds LINE INSTANCES (the C
  compares strdup'd pointers, so duplicate parent lines are distinct); chain deeper than 4096 ->
  `Unsupported`. Alias/parent parsers from the S505-pinned bytes (xdgmimealias.c, xdgmimeparent.c):
  fgets-255 chunks, `#` comments, first space splits, the LAST byte of the remainder is chopped (a
  last line without newline loses a real byte — modelled), qsort by key, glibc bsearch ((l+u)/2).
- mode (xdgmime.c:99-213, 391-436): per dir a LOADABLE mime.cache makes a cache; any cache -> refuse
  per contract 1 (`MADO_MIMETEXT: UNSUPPORTED cache-mode` one line per FILE, exit 3); otherwise the
  five text files (globs2/globs, magic, aliases, subclasses) decide `mode=text|none`; icons and
  generic-icons do not affect any answer and do not flip the mode.
- name step delegated to tools/mado-mimeglob.py (r94, unchanged; its sha at this base is
  65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453) via `_load_mimeglob()` bound at
  the module level; `LC_ALL=C` through `mg._libc.setlocale(mg._LC_ALL, b"C")` on the main path only.

CLI, output lines, exit codes and `--json` follow contract 1 and the r95 tool's conventions (see
"Retained evidence" for the smoke results). Module API for the probe/counter (mirrors r95's Sniffer):
`Sniffer(dirs)` with `.guess(name_bytes_or_None, data) -> {"type","uncertain","types","sniffed",
"prio"}`, `.mode` ("text"|"none"), `.dirs`; `xdgmime_dirs(dh, home, dd)`; `esc(b)`; `Unsupported`.

## Retained evidence (exact commands, run in $S)

Oracle (Shared contract 3, compiled once):

    cc -O0 -o "$S/oracle" \
      /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-95/controls/mimesniff-oracle-r95.c \
      $(pkg-config --cflags --libs gio-2.0)

1. Selftest, lone copy and beside the sibling (contract 1: >= 18 checks, no sibling import):

    cp build/mado-mimetext.c1.py "$S/lone/mado-mimetext.py"; cd "$S/lone"
    python3 -I mado-mimetext.py --selftest
    -> MADO_MIMETEXT_SELFTEST: checks=50 failed=0   (rc 0; also green beside the sibling, staged)

  50 labelled checks (m01..m50) covering: the 12-byte gate (short header, wrong 12th byte), section
  header parse (no priority, no ':', no ']', first-']' type, EOF after ']'), value length (BE two
  bytes, zero-length, bounds rule), masks (masked compare, literal compare), word sizes (2/4 swap of
  value AND mask, modulus error, size 3 error, size 0 legal and swap-free), ranges (scan window,
  default 1, range 0, bounds fail-outright), tree (any child at indent+1, exact+1 requirement, failed
  parent skips subtree, top-level sequences), order (priority desc, ties in file order, global list
  over dirs, priority 0 with no gate, `__NOMAGIC__` as a literal), drops (bad line drops the section,
  file continues, no rescan, EOF keeps the section but frees the trailing matchlet), zerosize before
  magic, fallback (text/binary, 128-byte window, VT vs FF through the guess layer), mode (none, magic
  alone = text, loadable-cache refusal), aliases/subclasses (one-level unalias, newline-less chop,
  text/plain super, parent chain, alias inside the subclass walk), guess combination (no name type,
  UNKNOWN uncertain, looks_like_text, trailing slash). Every label names its rule and the C anchor;
  expectations were derived from the C bytes in `.ufo/waves/round-96/fetch/` (byte-identical to the
  r95 copies I first read: sha fcb1eafe…/afb1c1c1… match the sources receipt) plus the S505-pinned
  xdgmimealias.c/xdgmimeparent.c.

2. Differential battery vs the compiled oracle (my scratch driver, 41 hand-built cases / 132 inputs;
   the driver and the full case list lived in $S/probe-vs-oracle.py, deleted with the scratch — the
   case list is reproduced below in the appendix):

    python3 -I probe-vs-oracle.py stage/mado-mimetext.py "$S/oracle" "$S/proot"
    -> PROBE total=132 diffs=0

  Covers both batteries: basics, priority 0/90/ties/INT_MAX/overflow(2^31, 30 digits), multi-dir
  (priority across dirs, ties across dirs, bad dir skipped, globs in one dir + magic in another,
  aliases in one dir + subclasses in another, HOME/.local/share user dir), lengths (3, 16, 256, 0),
  bounds, masks (incl. NUL data), word sizes {0,1,2,3,4} with mask swaps and two-word swaps, ranges
  {0,1,3,8,far}, trees (any-child, gap, skip subtree, 3-deep chain, sibling skip), parse-error drops
  (bad char, missing offset, range overflow, indent overflow, `[:]`, no leading bracket, NUL in
  header, empty line, CRLF, lone `>`, header-only file, empty section), `__NOMAGIC__` literal,
  EOF variants, zerosize, fallback window/VT/FF/DEL, desktop rule (name/no-name/slash), glob
  combinations (one-certain, two-types prio80, two-types subclass, alias-in-subclass, duplicate alias
  lines, alias chop without newline, non-ASCII glob byte, globs v1), mode none/globs-only, broken
  caches (garbage, version 2.0, version 1.0 — GLib falls through to text; my tool agrees), trailing
  slash, empty name, root name.

3. Frozen case file (`.ufo/waves/round-96/controls/magictext-cases-r96.json`, FROZEN sha
   `42ce9fc68458955e9e93c405cdbeb59f649b36d94e100240894d660391d1bed6`, 265 cases / 404 inputs):

    python3 -I score-vs-cases.py stage/mado-mimetext.py <cases.json> "$S/caseroot"
    -> SCORE cases=265 inputs=404 diffs=0
       PERCLASS alias=14/14 desktop=21/21 drop=29/29 fallback=16/16 glob=23/23 header=29/29
       indent=27/27 mask=33/33 mode=29/29 multi=25/25 order=17/17 range=30/30 sect=30/30
       value=36/36 word=31/31 zerosize=14/14

  Measured by my scorer on the immediate predecessor build
  fb924d962e0fa5977f6fe3f0316e4455c06bb5d2cc56c089282e5506238ccaf4 AND on the final bytes d5f174fc
  (both 265/265, 0 diffs); R96MReviewC1 and the counter independently scored the final bytes
  265/265. The only change between fb924d96 and d5f174fc is the identifier rename of main's module
  local (checker name-collision fix).

4. CLI smoke (contract 1): DIRS line then one answer line per FILE; `--json` = one object with
   mode/dirs/results[type,uncertain,sniffed,prio,types,file,name] in FILE order; refusal prints
   `MADO_MIMETEXT: UNSUPPORTED cache-mode` once per FILE, rc 3, no JSON body even with --json; rc 2
   for no FILE / unreadable FILE / missing sibling; `--name=X` and `--name X` both accepted;
   `--names-from-files` passes each path. All verified by invocation.

5. Structural self-audit: 0 non-ASCII bytes; imports {__future__, argparse, importlib.util, json, os,
   sys} with tempfile only inside `selftest()`; exactly ONE textual `spec_from_file_location`
   (location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mado-mimeglob.py")); mg
   attribute uses {Resolver, xdgmime_dirs, g_path_get_basename, esc, _libc, _LC_ALL}; no
   subprocess/socket/ctypes/eval/exec/getattr in the candidate; no temp files on the main path
   (tempfile fixtures under os.getcwd() so the audit launcher's work-tree allow covers them).

## Findings for the wave

1. **Case defect found and FIXED by the cases seat: the old `mode-06-junk-cache-declared-refusal`.**
   Its `mime.cache` was 16 junk bytes (`JUNKNOTACACHE000`) — it does not load. The draft-case labels
   were the CACHE_RE existence sentinel (`["UNSUPPORTED", null]`), but the C (xdgmime.c:131-141) only
   treats a cache that LOADS as cache mode: the compiled oracle answered `app/x-md6 0` / `app/x-md6g 0`
   from the text files, and my candidate answered the same. Reported with evidence to
   R96MExecCasesC1 and MadoR96; the cases seat froze the fix — the case now carries the oracle labels
   and the refusal sentinel survives only on the loadable-cache cases. FROZEN case file
   `.ufo/waves/round-96/controls/magictext-cases-r96.json` sha
   `42ce9fc68458955e9e93c405cdbeb59f649b36d94e100240894d660391d1bed6`, 265 cases / 404 inputs.
   My scorer over the frozen file: `SCORE cases=265 inputs=404 diffs=0`, per-class census full
   (alias 14, desktop 21, drop 29, fallback 16, glob 23, header 29, indent 27, mask 33, mode 29,
   multi 25, order 17, range 30, sect 30, value 36, word 31, zerosize 14).

2. **Reviewer-driven structural reshapes (R96MReviewC1, three rounds, all folded):**
   - round 1: `cls.__new__` in the lone constructor and the `mg = mod` module-store failed the
     counter's static_check; selftest tempfile fixtures must not live under /tmp.
   - round 2: the checker rejects every bare Load of a module-var name — the accepted shape is:
     `_load_mimeglob()` returns the module and raises SystemExit on a missing sibling; `main` binds it
     as a LOCAL and touches it only through the allowlisted attributes; the selftest injects a fake
     through a constructor parameter.
   - round 3: the checker keeps one global name set — my `m`/`mp` locals collided with loop variables
     named `m`/`mp` elsewhere; the module local is now `mimeglob_mod` (unique in the file), the
     magic-path loop var stays `mp`, the matchlet loop vars are `mt`.
   Final shape: `Sniffer.__init__(dirs, resolver=None, lone=False)` does both constructions (selftest:
   `Sniffer(dirs, lone=True)` with an empty `_NoNames` name table; main passes
   `resolver=mimeglob_mod.Resolver(dirs)`); the selftest cache-refusal check injects a fake resolver —
   no `__new__`, no global swap; selftest fixtures live in `TemporaryDirectory(dir=os.getcwd())`.
   One textual `spec_from_file_location` (location names `__file__` + `mado-mimeglob.py`); mg-module
   attribute touches are only Resolver / xdgmime_dirs / g_path_get_basename / esc / _libc.setlocale /
   _LC_ALL, always as `name.Attr`; imports {__future__, argparse, importlib.util, json, os, sys} with
   tempfile inside `selftest()`; 0 non-ASCII bytes; no subprocess/socket/ctypes/eval/exec; no temp
   files on the main path.
   NOTE for the counter: importing the candidate does NOT execute the sibling at import time (no
   module-level binding); the sibling loads on the first main-path construction.

3. **Model corrections from the L1 (folded, with selftest checks):** word_size {0,1,2,4} (0 legal,
   swap-free, no modulus test); text mode has no `prio > 0` gate (xdgmime.c:535); `__NOMAGIC__` is a
   literal value with no deleteall semantics.

4. **API note for the probe/counter** (mirrors r95's Sniffer shape): module-level
   `xdgmime_dirs(data_home, home, data_dirs)`, `esc(b)`; `Sniffer(dirs)` (loads the sibling, refuses a
   loadable cache with `Unsupported("cache-mode")`), `.guess(name_bytes_or_None, data) ->
   {"type","uncertain","types","sniffed","prio"}`, `.mode` ("text"|"none"), `.dirs`; optional
   `resolver=` injection for tests; `Unsupported` exported.

## Rules I had to take from bytes the wave did not fetch (all oracle-validated)

- xdgmimealias.c / xdgmimeparent.c (the text aliases/subclasses parsers). I fetched both twice,
  HTTP 200 both times, byte-identical, shas `a1e67ae3604c437b8516d6bc4c67f31afea6fc58393b9afe1c42a8b424111394`
  and `9c85c35f143b4fbf274ba07f433ad9102270ededf1a95f6cf0cc320d941f35e3` — both EQUAL to the S505
  pins already in corpus/SOURCES.md, so no new source row is needed. Commands:
  `curl -sSL -o xdgmimealias.c.1 -w '%{http_code} %{url_effective} %{size_download}' https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/xdgmime/xdgmimealias.c` (and .2, and the xdgmimeparent.c pair) in `$S/fetch`.
- glibc qsort/bsearch behaviour for duplicate alias keys: qsort has been introsort (unstable) since
  glibc 2.37, so the winner among duplicate aliases with different targets is unspecified C; the
  draft models stable insertion order + glibc bsearch ((l+u)/2). My `dup_alias_lines` battery case
  matched the oracle; any future case with a different glibc placement must be oracle-labelled.
- `sep[strlen(sep)-1] = '\000'` on an empty remainder (a trailing space at EOF) writes out of bounds
  in C; modelled as an empty mime string. Unobservable through the oracle so far.
- A directory named `magic`/`aliases`/`subclasses`: fopen succeeds, fread fails; modelled as an
  unreadable file contributing nothing (matches the C's short-read path).

## Rules with residual risk (declared guesses, oracle-checked where possible)

- Empty-section insertion (header followed by another header) is modelled as inserted-but-unmatchable;
  no oracle case can distinguish it, and the mutant `sect-keep-empty`/`sect-keep-eof` may be
  unkillable by answer-difference alone (flagged here so the mutant seat is not surprised).
- Duplicate-parent (same parent line twice) seen-set semantics: modelled per line instance; deep
  chains are capped at 4096 frames as the declared refusal. Exponential blowup on adversarial
  duplicate graphs is possible in the C too; no case exercises it.
- Very long alias/subclass lines chunk at 255 bytes like fgets; no oracle case exercised a >254-byte
  line yet.

## Tool installs

None. No pacman transaction, no uv/npm/cargo install; all work used the host's existing python3, cc,
pkg-config, curl, coreutils.

## Risks / blockers

- None open on the tool side at report time: selftest green (50/0, lone and staged), oracle battery
  132/132, frozen cases 265/265 (mine on fb924d96; R96MReviewC1 and the counter on the final
  d5f174fc), and R96MReviewC1's re-run of the counter's static_check on d5f174fc returned [].
- The mutants file (`.ufo/waves/round-96/controls/magictext-mutants-r96.json`, 115 rules) carries
  `find`/`replace` = `<awaiting-candidate>`; they must be instantiated against the frozen candidate
  bytes (sha above). Hints for the mutant seat:
  - `indent-mirror`: the C's prepend+mirror is modelled as a direct file-order append in
    `_parse_magic_file` (line `match["matchlets"].append(ml)`); a mutant that prepends+reverses
    reproduces the bug class.
  - `sect-keep-empty`/`sect-keep-eof`: empty sections are unobservable through answers (they can never
    match), so answer-difference alone cannot kill them; the mutant seat should expect equivalents or
    give them a structural kill.
  - `range-wrap-refused` has no text-mode analogue (the 32-bit wrap is a cache-reader rule, r95);
    text ranges are Python ints.
- The fresh-leg generator (magictext-fresh-r96.py) had not landed at report time; my 41-case battery
  above is the stand-in differential evidence, and the reviewer measured 265/265 frozen + 120/120
  fresh + 300/300 host sample on the predecessor build.

## Appendix — the differential battery (41 cases; driver shape: materialize case files, run the
oracle once per case over its inputs with the case env, run the candidate once per input with the
same env, diff (type, uncertain) pairs)

basic50 (AB/ABX data-only and named), prio0, order90, tie50, multidir, multidir_tie, len256,
len0, bounds, short_value_eof, mask, word2, word4, word2mask, word0, word2odd, word3, word1, range3,
range1def, range0, range8, tree_any, tree_gap, tree_skip, tree_deep, tree_sibling_skip,
seq_toplevel, drop_middle, prio_overflow, prio_30digits, indent_overflow, offset_missing,
range_overflow, badchar_after_value, no_bracket, nul_in_header, empty_line, nomagic_literal,
eof_nomime, zerosize, fallback_text (plain/128+ctl/127+ctl/VT/FF/DEL), desktop
(name/no-name/slash), glob_one_certain, glob_two_prio80, glob_two_subclass, alias_in_subclass,
alias_chop_no_newline, glob_ff_byte, mode_none, mode_globs_only, slash_name (d/, "", /), empty_section,
lone_gt, header_only, crlf_line, explicit_indent0, magic_over_fallback, len16, word4_two_words,
masked_nul_data, range_far, int_max_prio, glob_v1, globs_merge_dirs, alias_dir_subclass_dir,
subclass_cycle, dup_alias_lines, type_with_space, empty_type, no_leading_bracket,
fallback80_two_types, comment_lines, cache_garbage, cache_version_20, cache_version_10,
bad_dir_skipped, home_user_dir. (Case ids may combine several of these fixtures; total 41 cases,
132 input pairs, 0 diffs.)
