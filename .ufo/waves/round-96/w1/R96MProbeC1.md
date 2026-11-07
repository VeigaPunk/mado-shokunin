# R96MProbeC1 -- independent byte-level probes of the C1 magic surface

Seat `R96MProbeC1` (reviewer/probe), round `mado` 96, hyaku run 15, wave w1.
Base revision `9f029f46f01f6cd3a1d29ac39bb548498a1d0c3d`. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`.

Oracle: round 95's frozen C oracle, reused unchanged --
`.ufo/waves/round-95/controls/mimesniff-oracle-r95.c`, sha256
`99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a` (verified this round).
Compiled in my scratch with
`cc -O0 -o "$S/oracle" <oracle.c> $(pkg-config --cflags --libs gio-2.0)`
against the host's glib2 2.90.1-1 / shared-mime-info 2.5.1-2.
Source of rules: the round-95 fetch copy of `xdgmimemagic.c` (sha
`fcb1eafe748d3dc18f7f405d1078c8a32e313d23d2fab86b0f12e609ac2ce742`, the same digest the
L1 opened for round 96; the round-96 `fetch/` dir was still empty when this seat read it).
Read-only: every probe is a fixture directory under scratch plus one oracle process; no
host file, service, sysctl, config or network was touched.

Artifacts:

- `.ufo/waves/round-96/controls/probes-r96.py` -- the harness (stdlib only, ASCII). It builds
  every fixture root from a declarative list (and, with `--fuzz N --fuzz-seed S`, N seeded random
  magic files from the parser's grammar), runs the oracle with
  `env -i LC_ALL=C HOME=<root>/h [XDG_DATA_HOME=<root>/dh] XDG_DATA_DIRS=...`, and with
  `--candidate PATH` runs the C1 candidate over the same bytes and prints every disagreement.
- `.ufo/waves/round-96/w1/R96MProbeC1-answers.json` -- the full oracle answer set (one record
  per probe root: the magic bytes, every input's bytes and the oracle's `type`/`uncertain`).
- This report.

Counts: **648 fixture roots, 2254 inputs, 0 oracle errors** -- 256 roots for the (a) value-byte
sweep, 256 for the (a) mask-byte sweep, and 136 structural/combo roots for (b)-(i) and the
recovery/order/name/mode probes. A seeded differential fuzz leg (`--fuzz N --fuzz-seed S`,
magic files drawn from the parser's own grammar) adds **700 roots / 2100 inputs over two seeds**
(seed 1: 400 roots, seed 2: 300), also 0 oracle errors.

Scope note on the fixture cap: the seat item caps synthetic fixtures at 200 while mandating both a
256-case value-byte sweep and a 256-byte mask sweep. Those sweeps alone are 512 magic files if
each byte must live in its own file to be attributable, so I read the cap as a budget on committed
fixtures (the committed artifact is one generator, zero fixture files) and state the exact counts
here so the L1 can re-scope if the cap was meant literally. The 512 sweep roots are the sweep the seat item itself mandates
(one value byte per magic file is the only way to make each byte's answer attributable); they
are generated, never committed, so the committed artifact stays one script. Everything the
report cites below is reproducible with
`python3 -I controls/probes-r96.py --oracle <compiled oracle> --scratch <dir> --json <out>`.

---

## 1. Ground truth measured (the rules the frozen labels must carry)

Each item names the probe id(s) in `R96MProbeC1-answers.json` that demonstrate it. Where a
probe id is not unique, the answer column in the appendix is the authority.

### 1.1 The 12-byte gate (`xdgmimemagic.c:801-819`)

- A magic file contributes only when it is at least 12 bytes **and** its first 12 bytes are
  exactly `4d 49 4d 45 2d 4d 61 67 69 63 00 0a` (`MIME-Magic\0\n`). 11 bytes -> ignored
  (`g-header11`); 12 bytes with a different 12th byte -> ignored (`g-header-wrong12`); a NUL
  instead of the newline -> ignored (`i-nul-header-12`); zero bytes -> ignored
  (`g-header-empty`); exactly the 12-byte header and nothing else -> read, zero sections
  (`g-header12-only`).
- After a passing gate the parser starts **at the byte after the header** (it does not rewind),
  so the header line itself is never parsed again (`g-header12-ok`).

### 1.2 Section header `[priority:type]` (`:230-281`)

- The priority is a run of decimal digits read by `_xdg_mime_magic_read_a_number`; **no digits
  at all returns -1 and is a parse error** (`h-prio-nodigits`: `[:x]` is an error, not
  priority 0). A stray byte before `:` is an error (`k15`: `[1-2:x]`).
- Numbers are cut at `MAX_NUMBER_SIZE` = 30 digits (`:189-215`) and then `strtol` runs, with
  `ERANGE` mapped to -1. Measured: a 31-digit `000...005` parses as **priority 0** because only
  the first 30 zeros are read (`k35`), and 30 nines overflow to a parse error (`k36`).
- `INT_MAX` (2147483647) is a legal priority and sorts above 2147483646 (`k33`);
  `INT_MAX + 1` is a parse error (`k34`, see also `b-off-overflow` for the offset).
- The type is read to the newline or a NUL, then must contain `]`; anything after the `]` on
  that line is discarded (`h-type-junk`), a second `[header]` on the same line is consumed
  (`k23-two-headers-one-line` answers `probe/k23a`), and a NUL before the `]` is an error
  (`i-nul-type`, `k29`). An empty type `[]` is legal and is answered verbatim (`h-empty-type`
  -> `""`/0).
- A header with no `]` and **no newline** (EOF) is the EOF state, not an error, and the section
  is dropped (`k07`); the same header with a newline is an error and the next section is parsed
  (`k07b`).

### 1.3 Matchlet line (`:301-514`)

- `[indent] ">" offset "=" <2 BE bytes length><value> ["&" mask] ["~" word] ["+" range] "\n"`.
  Omitted indent is 0, omitted range is 1, omitted word is 1 (`:84-105`). Leading zeros are
  ordinary digits (`k22` offset `0000` = 0; `k37` indent `01` = 1).
- The two length bytes are big-endian and **both matter**: lengths 0x0100, 0x0101, 0x00ff all
  match with data of that exact length (`k30`, `k31`, `k32`), so a model that reads one byte
  or swaps the order fails these.
- A zero-length value matches any data at an in-bounds offset (`b-len0-off0-r1`: value length 0
  matches `Z` and `\x00`), **including at offset == len** (`b-len0-off5`: offset 5 with len 5
  matches, len 4 does not). A zero-length value with range 0 never matches
  (`b-len0-off0-r0`). A zero-length value with an empty `&` mask also matches (`k11`).
- **A final matchlet whose line has no trailing newline is discarded, but the section is still
  inserted**: `k27` (no newline) -> `text/plain`, `k27b` (newline) -> the section's type. This
  is `:468-505`: the `c == '\n'` test fails on EOF, the matchlet is freed, and `:777` still
  inserts the section because `mime_type` is set.
- A value (or mask) cut short by EOF is the **EOF state**, not an error, so the section keeps
  the matchlets parsed before it (`k05` value truncated; `k04` EOF right after `&`). A value
  cut short **not** at EOF is an error (`h-short-value-mid`: declaring 5 bytes over `AB\n[4`
  consumes the rest of that line and then the orphaned matchlet line errors too).
- A CRLF line ending kills the matchlet line (`h-cr`, `k28`) because `\r` is neither `&`, `~`,
  `+` nor `\n`; the header line itself survives (the CR sits after the `]`).

### 1.4 Mask (`:400-419`, `:515-556`)

- The mask is read with exactly `value_length` bytes and compared as
  `(value[j] & mask[j]) == (data[j] & mask[j])`; both sides are masked. Byte sweep of every
  mask byte 00..ff with value == mask: every byte matches its own data (`a-mask-*` input 0) and
  only `00` matches data `ff` (input 1) -- that pair is what separates a real mask from
  "mask ignored", "value only", "data only" and "mask inverted".
- The mask is swapped with the word size (`d-w2-mask`: `00 01`/mask `00 ff` with `~2` becomes
  `01 00`/`ff 00`, so data `01 xx` matches and `00 xx` does not).

### 1.5 Word size (`:421-450`)

- Accepted: 0, 1, 2, 4. Rejected (parse error): 3 and anything else (`d-w3`), a word size with
  no digits (`k09`), and -- measured -- `~0` is accepted and behaves byte-wise (`d-w0-len3`).
- The modulo check runs only when `word_size > 1`: `value_length % word_size != 0` is a parse
  error (`d-w2-len3`, `d-w4-len6`, `d-w4-mask-len2`, `k16`). A zero-length value with `~2` is
  fine (`d-w2-len0`).
- On this little-endian host the value **and** the mask are byte-swapped per word at parse time
  (`d-w2-swap`: file `00 01 00 02` matches data `01 00 02 00`, not `00 01 00 02`; `d-w4-swap`).

### 1.6 Range (`:452-470`, `:515-556`)

- The loop is `for (i = offset; i < offset + range_length; i++)`, and **`i + value_length > len`
  returns FALSE for the whole matchlet** (it does not continue): `c06` (range 10, value `ZZ`,
  data `AAAA` -> no match; data `ZZ` -> match).
- `range 0` never compares and the matchlet is FALSE (`c05`); range 1 at the last byte matches
  (`c04`); range 2 from offset 3 over `AAAAB` matches at the last valid offset (`c03`); a hit
  after a miss inside the range matches (`c07`); a range that runs past the end still matches if
  an earlier index hit (`c08`).
- Offsets beyond `INT_MAX` are parse errors (`b-off-overflow`), `INT_MAX` parses and can never
  match (`b-off-intmax`: `i + value_length` is unsigned and exceeds `len`).

### 1.7 Indent / tree (`:557-588`)

- Top-level is indent 0: a first matchlet at indent 1 (`e-indent1-first`) or 9 (`e-indent9`) is
  never compared and the section cannot match.
- A matchlet whose next entry has a greater indent requires that deeper chain: 0-1-2 holds
  (`e-chain012`), a 0-2 jump does not (`e-chain02-jump`), any one child at the next indent
  suffices (`e-sibling`), a failing child fails its parent but the walk then skips the whole
  subtree and still tries the next level-0 entry (`e-child-fails-parent`).

### 1.8 Section order (`:596-629`, `:652-700`)

- Sections insert by priority descending; equal priorities keep file order
  (`f-same-file-tie` -> the first section; `f-prio0` -> priority 1 beats 0). The first section
  whose tree holds wins; a high-priority section that does not match does not shadow
  (`f-nohit-hi`).

### 1.9 Dirs (`xdgmime.c:129-206`, `:220-300`)

- Read order: `XDG_DATA_HOME` (or `HOME/.local/share`), then the non-empty `XDG_DATA_DIRS`
  elements. Equal priorities across dirs keep that order (`f-tie-d1-first`,
  `f-tie-d2-first`, `f-datahome-tie`), and priority beats read order (`f-prio-d2-higher`,
  `f-prio-d1-higher`).
- An empty element is skipped (`k42`), a trailing colon adds nothing (`k44`), and
  `XDG_DATA_DIRS=""` reads **no** data dirs at all (`k43`), as does `"::"` (`k45`).
- A `mime/magic` that is a directory (`k12`) or unreadable (`k13`) contributes nothing and the
  rest of the dirs still count.

### 1.10 Error recovery, precisely (`:283-300`, `:749-801`)

The parser state machine: on ERROR it calls `parse_error`, which reads bytes until the next
`\n` (consuming it) and returns SECTION. **How much it eats depends on where the error fired:**

| error site | newline already consumed? | effect |
|---|---|---|
| bad header (`:241`,`:253`), bad indent/offset/`=` (`:335-355`), `~`/`+` with no digits, invalid word size (`:440`), range overflow (`:459`), byte where `\n` was expected (`:470`) | no | `parse_error` eats the rest of the same line only; the next line is parsed normally (`k02`, `k08`, `k09`, `k14`, `k17`, `h-cr`, `i-nul-endline`) |
| `value_length % word_size != 0` (`:464` reads the next byte, `:476` fails) | **yes -- the `\n` was consumed at :464** | `parse_error` eats **the whole next line**, which is normally the next section header (`k01`, `k03`, `k16`) |

`k46` pins the mechanism: a blank line after the mod error absorbs the skip and the following
section survives; `k47` shows each mod error eating its own following line. A section is
dropped as a whole (its earlier good matchlets are lost) whenever the error is not the EOF
state (`h-bad-line-drops-section`).

### 1.11 A section with no matchlets

- It **is inserted** into the match list and is inert (its tree is NULL, so
  `matchlet_compare_level(NULL, ...)` is FALSE): `h-empty-then-hit` -> the later section,
  `h-empty-eof` -> no match, `k29` (NUL after `]` commits the section before the junk line).
- Consequence for the model: "kept only if it ends with a parsed matchlet" is the wrong reason
  but the right answer; nothing observable depends on it inside this surface (`max_extent` is
  not read by the caller).

### 1.12 NUL bytes

- NUL in a type name is an error for that section (`i-nul-type`); NUL **as a value byte** is an
  ordinary byte (`i-nul-value`, `i-nul-value3`); a NUL where the `\n` is expected is an error
  (`i-nul-endline`); a line that starts with NUL errors and its skip swallows the following
  bracket line (`i-nul-line`).

### 1.13 Fallback and the guess combination (`xdgmimeint.c:176-190`, `gcontenttype-fdo.c`)

- Empty data (len 0) short-circuits to `application/x-zerosize`/0 **before** any magic
  (`b-len0-off0` input 0). But a single name type wins even over zerosize (`j13`: empty file
  named `a.prb` -> the glob type; no name -> zerosize).
- The xdg fallback scans at most the first 128 bytes and calls data binary when a byte < 32 is
  not 9, 10 or 13 (`k39`: `A`*128 + NUL -> text; `A`*127 + NUL -> binary; `k40`: a control byte
  at 100 -> binary, at 200 -> text).
- If the xdg rule says binary, `looks_like_text` gets a second chance: every byte must be
  non-control or a space (`g_ascii_isspace` on this glib is exactly `{09,0a,0c,0d,20}`) or `\b`.
  Measured over all 256 single bytes, the **binary set is exactly
  `{00-07, 0b, 0e-1f}` (27 bytes)**; `08` and `0c` are text/plain *only* because of this second
  chance (`a-value-007`, `a-value-011`), and `7f` is text because the first rule never sees it
  as a control byte.
- The non-match answers of the 256-byte sweep are the measured fallback map: 229 `text/plain`
  and 27 `application/octet-stream` (uncertain 1 for all of them).
- **`sniffed == UNKNOWN` is a pointer comparison, not a string comparison.** A magic section
  whose type is literally `application/octet-stream` is a strdup'd string, so it is *not* the
  `XDG_MIME_TYPE_UNKNOWN` constant: the answer is that section's type with **uncertain 0**, and
  neither `looks_like_text` nor the desktop rewrite runs (`k41`: data `A` under such a section
  -> `application/octet-stream`/0, where a string comparison would give `text/plain`/0).
- Desktop: a sniffed `application/x-desktop` with a non-NULL name becomes `text/plain`
  (`j06`: name `x.bin` -> text/plain; name NULL -> application/x-desktop; name `x.txt` ->
  text/plain through the one-name-type early return, not through the rewrite).
- Name step: one name type returns before any sniffing (`j02`); several name types and no
  tie-breaker return the first uncertain (`j01`); a sniffed priority of 80 wins
  (`j04`), 79 does not (`j03`); a name type that is a subclass of the sniffed type wins certain
  (`j05`) and the reversed edge does not (`j11`); the basename is used (`j09`); a trailing `/`
  is `inode/directory` uncertain (`j08`); an alias file does not rewrite the answer (`j07`);
  an existing-but-empty `globs2` suppresses `globs` (`j12`).

---

## 2. Divergences from the round-96 shared model (for the L1 to fix before the freeze)

These are places where the contract text (claims declaration / seat brief) and the measured C
disagree. The case labels must follow the measurement.

**D1 -- "a section with a bad line is dropped entirely (skip to newline, resume at the next line
that starts a section); the file continues after it" is false for one error class.** For
`value_length % word_size != 0` the newline has already been consumed at `:464`, so
`parse_error` eats the *next line*, which is normally the next section's header. Measured:
`k01` (the following `[40:...]` header is swallowed -> `text/plain` where a "resume at the next
section" model gives that section's type), `k03` (the section after the swallowed header also
loses its matchlet line, the *third* section answers), `k16`, `k46`, `k47`. Any tool that
resumes at the next section line passes 100% of the other drop probes and fails these.

**D2 -- "a section is kept only if it ends with at least one parsed matchlet (EOF-with-mime_type
counts)" states the wrong condition.** `:777` inserts on `state == SECTION` too, so a
header-only section is kept and is inert (`h-empty-then-hit`, `h-empty-eof`, `k29`). Harmless
observationally here, but a mutant that makes such a section match would be "killed" by a case
that assumes it was dropped for the wrong reason.

**D3 -- the EOF rules are richer than "EOF-with-mime_type counts".** A final matchlet with no
trailing newline is *discarded* while the section survives (`k27` vs `k27b`); a value or mask
cut short by EOF is the EOF state, so earlier matchlets of that section stay live (`k04`,
`k05`); a length that declares more bytes than the file has swallows the whole rest of the file
and ends parsing (`k17`, where the declared length is 0x4241).

**D4 -- the guess combination's UNKNOWN test is pointer identity** (`gcontenttype-fdo.c:591`,
`:628`, `:655`). A magic section typed `application/octet-stream` is answered as a real match
(uncertain 0, no `looks_like_text`, no desktop rewrite) -- `k41`. A model that compares strings
answers `text/plain` there.

**D5 -- the text fallback's exact sets.** The xdg rule allows `{09,0a,0d}` only; the second
chance (`looks_like_text`) adds `\b` and `{09,0a,0c,0d,20}`. Net single-byte binary set:
`{00-07,0b,0e-1f}`. In particular `08` and `0c` are text and `0b` is binary -- the three bytes a
case set must carry to separate `fb-allowed` / `fb-binary` / `fb-second-chance`.

**D6 -- `XDG_DATA_DIRS=""` means no data dirs** (`xdgmime.c:246-250`), not "the defaults"; empty
elements are skipped (`k42`-`k45`). The frozen case file forbids an unset `XDG_DATA_DIRS`, which
is fine, but a `multi` case with an empty element is legal and must answer from the other dirs.

---

## 3. Candidate comparison

Measured against the in-wave C1 draft
`.ufo/waves/round-96/build/mado-mimetext.c1.py`, copied into a scratch pair
(`mado-mimetext.py` + the unchanged `tools/mado-mimeglob.py`, the frozen layout the draft expects)
at **sha256 `951a49230be98b2eb8ee29aef03793c3eff331293b8b46ea0d06fb0efe91bb97`**.

**Result: 0 disagreements over all 648 roots / 2254 inputs, plus 0 over the two fuzz legs
(700 roots / 2100 inputs, seeds 1 and 2).** The candidate answers every
probe exactly as the oracle does, including the four corners most likely to be wrong (D1 extra-line
recovery, D3 final-newline/EOF rules, D4 octet-stream pointer rule, D5 `08`/`0c` fallback bytes).
The measured sha is a moving target: the wave was still editing the draft, and an **earlier
snapshot of the same path** (md5 `2af02818c915c2192c298c6978723aa2`) had a parse loop that never
appended the parsed matchlet and failed **881/2251** inputs (every sweep root answered
`text/plain`). That is evidence the probe set detects a real parse-loss defect immediately, and it
is why the number in this section must be read as a statement about a sha, not about a path.

Two adjacent boundary checks were run by hand against the same snapshot:

- a 40-byte `mime.cache` with version 1.1 (`00 01 00 01` + 36 zero bytes) makes the oracle answer
  from the cache (`text/plain`/0 where the text magic would have matched `probe/kc`), and the
  candidate then prints `MADO_MIMETEXT: UNSUPPORTED cache-mode` and exits **3** -- the mode
  boundary and the refusal contract agree;
- cache files that do **not** load (48 bytes of garbage, 40 zero bytes, a 14-byte header) leave
  the run in text mode in both, and the magic answers (`k49`, `k50`, `k51`).

The frozen candidate must be re-measured at the freeze (the L1 lands `tools/mado-mimetext.py`);
the same command, ~140 s:

```
python3 -I controls/probes-r96.py --oracle <compiled oracle> --candidate tools/mado-mimetext.py \
        --scratch "$S" --json "$S/cmp.json"
```

The probes a first-draft Python model is most likely to fail, in order of expected value:
`k01/k03/k16` (D1), `k27/k27b` (D3), `k41` (D4), `a-value-007`/`a-value-011` (D5, bytes `08`
and `0c`), `d-w2-len3`/`d-w4-len6` (the modulo error), `b-len0-off5` (zero-length value at
offset == len), `k30` (both length bytes), `e-chain02-jump` and `e-sibling`, `c06`
(bounds -> FALSE for the whole matchlet), `f-tie-d2-first` (tie order), `k35` (30-digit cut).

## 4. What the frozen case set should carry (per class, with reasons)

The case file needs >=8 cases per class and >=260 total. My recommendation is not "copy my 645
roots" -- it is: **every class below should include the listed probes, because each one is a
place where a plausible wrong model gives a different answer.** Probe ids are exact fixtures in
`R96MProbeC1-answers.json` (the appendix table below has the bytes).

| class | carry (probe ids) | why |
|---|---|---|
| `header` | `g-header11`, `g-header12-only`, `g-header12-ok`, `g-header-wrong12`, `g-header-empty`, `i-nul-header-12`, `g-header-13` | `g-header-13` also shows that a stray newline after the header swallows the next section line (a header-state error consumes the newline before `parse_error`) |
| `sect` | `h-prio-nodigits`, `k15`, `k35`, `k36`, `k33`, `k34`, `h-no-close`, `k07`, `k07b`, `h-type-junk`, `k23-two-headers-one-line`, `h-empty-type`, `k29`, `h-bracket-commits` | the 30-digit cut, INT_MAX, "no digits is an error", the `]` requirement, and the empty type are each a distinct wrong-model detector |
| `value` | `k30`, `k31`, `k32` (length 0x0100/0x0101/0x00ff), `k27`, `k27b`, `k05`, `b-len0-off0-r1`, `b-len0-off5`, `b-len0-off0-r0`, `a-value-007`, `a-value-011`, `a-value-000` | both length bytes; the final-newline discard; EOF-truncated value keeps the section; zero-length semantics at/beyond `len`; the `08`/`0c`/`00` fallback bytes |
| `mask` | `a-mask-000`, `a-mask-0ff`, `a-mask-00f`, `a-mask-007`, `d-w2-mask`, `k11`, `k04`, `d-w4-mask-len2` | the mask sweep pair (value==mask matches, `m^ff` matches only at 0) separates every mask mutant; `d-w2-mask` pins the word swap of the mask; `k04` the EOF mask |
| `word` | `d-w1-len3`, `d-w2-len3`, `d-w4-len6`, `d-w3`, `d-w0-len3`, `d-w2-swap`, `d-w4-swap`, `d-w2-len0`, `k09`, `k16` | the accepted set {0,1,2,4}, the modulo error and its **extra-line eat** (`k16`), the LE swap of value and mask |
| `range` | `c01-r1`, `c02-r2`, `c03-r2-off3`, `c04-r1-off4`, `c05-r0`, `c06-out-of-bounds-false`, `c07-mid`, `c08-tail` | range 0, the last valid offset, and the "return FALSE, not continue" bounds rule |
| `indent` | `e-indent0`, `e-indent1-first`, `e-indent9`, `e-chain01`, `e-chain012`, `e-chain02-jump`, `e-child-fails-parent`, `e-sibling`, `e-deep-skip`, `k37` | first-child vs any-child, the level jump, the subtree skip, and that an omitted/`01` indent parses as 0/1 |
| `order` | `f-prio-d2-higher`, `f-prio-d1-higher`, `f-tie-d1-first`, `f-tie-d2-first`, `f-nohit-hi`, `f-same-file-tie`, `f-prio0`, `k33` | priority descending, ties in read/file order, and a non-matching high-priority section |
| `drop` | `k01`, `k03`, `k16`, `k46`, `k47`, `h-bad-line-drops-section`, `k14`, `k17`, `k02`, `k08` | the D1 extra-line eat (four independent shapes) against the same-line recovery class |
| `multi` | `f-tie-d1-first`, `f-datahome-tie`, `f-prio-d2-higher`, `k42`, `k43`, `k44`, `k45`, `k12`, `k13` | home-before-dirs, empty elements, empty string, unusable magic in one dir |
| `glob` | `j01`, `j02`, `j03`, `j04`, `j05`, `j09`, `j12`, `j13` | one-type early return, 79/80 boundary, subclass tie-break, basename, globs2-suppresses-globs, zerosize-vs-name |
| `alias` | `j07`, `j11` | an alias file must not rewrite the guess; the subclass direction |
| `fallback` | `k39`, `k40`, `k41`, plus the sweep's non-match answers (`a-value-*` input 1) | the 128-byte window, the control-byte position, and the UNKNOWN-pointer rule (D4) |
| `zerosize` | `b-len0-off0` input 0, `j13`, `k11` input 0 | len 0 before magic, name-over-zerosize, zero-length match vs empty data |
| `mode` | `k49`, `k50`, `k51` (non-loadable caches stay text), plus one loadable 40-byte 1.1 cache as the refusal case (see section 3) | a cache that does not load must not flip the mode (`xdgmimecache.c:43-73`: size >= 40, major 1, minor 1-2), and a loadable one must (`xdgmime.c:129-160, 645-646`); the case generator must never leave a *loadable* `mime.cache` in a text case |
| `desktop` | `j06`, `k41` | rename only with a name; and the octet-stream pointer rule that blocks a string-comparison model |

Two of these are *not* in the declaration's rule list and should be added to the case
generator's coverage: the D1 extra-line recovery (a `drop` case family) and the D4
octet-stream pointer rule (a `fallback` case).

---

## 5. Residual risk and verification gaps

- The candidate leg is measured only at the draft sha named in section 3; the wave was still
  editing the file, so the number does not transfer to the frozen `tools/mado-mimetext.py`
  without a re-run.
- Cache mode is out of this seat's scope; the oracle in cache mode reads the binary cache, so a
  case root that accidentally carries `mime.cache` is a refusal case, not a text case.
- `max_extent` / buffer truncation and the `mime_types` elimination loop are outside the surface
  (`xdgmime.c:535` passes `NULL, 0`), so no probe covers them and a tool that models them
  cannot be distinguished here.
- The host database itself (`/usr/share/mime`, cache mode on this host) is R96MExecHostC1's
  leg, not mine.
- The 256-byte value sweep's *non-match* half also measures the fallback; its 27 binary bytes
  are the exact set for `fb-*` mutants, but the sweep says nothing about multi-byte fallback
  beyond the 128-byte window (`k39`, `k40`).
- The CLI surface beyond `FILE --name` is untested here: `--names-from-files`, `--json`, the
  `MADO_MIMETEXT_DIRS` line format and the exit codes are the counter's and the reviewer's legs;
  my harness drives only plain `FILE...` with `--name` (one invocation per distinct name) plus
  the three root flags.
- Probe roots are generated, not committed; the exact bytes of every cited fixture are in
  `R96MProbeC1-answers.json` (`magic_d1`/`magic_d2`/`magic_dh` hex plus each input's hex), so a
  case author can lift any of them verbatim.

---
## Appendix -- every non-sweep probe and the oracle's answer

`d1` is the magic file in `XDG_DATA_DIRS[0]`; the 12-byte `MIME-Magic\0\n` header is elided
from the hex column; `d2`/`dh` are shown when present; a `-` input is empty data; `files=`
lists auxiliary files under `dh/` (globs, aliases, subclasses, a non-loadable mime.cache).
Sweep roots (`a-value-NNN`, `a-mask-NNN`) are omitted here and summarised in section 1.13.

| probe | magic `d1` (hex, 12-byte header elided) | inputs -> oracle |
|---|---|---|
| `b-len0-off0` | `5b35303a70726f62652f6230315d0a303e303d0001410a` | `-` -> `application/x-zerosize`/0; `41` -> `probe/b01`/0; `42` -> `text/plain`/0; `4141` -> `probe/b01`/0 |
| `b-len2-off0` | `5b35303a70726f62652f6230325d0a303e303d000241420a` | `4142` -> `probe/b02`/0; `41` -> `text/plain`/0; `414258` -> `probe/b02`/0; `4241` -> `text/plain`/0 |
| `b-len2-off1` | `5b35303a70726f62652f6230335d0a303e313d000241420a` | `584142` -> `probe/b03`/0; `5841` -> `text/plain`/0; `58` -> `text/plain`/0; `58414258` -> `probe/b03`/0 |
| `b-len2-off2` | `5b35303a70726f62652f6230345d0a303e323d000241420a` | `58584142` -> `probe/b04`/0; `585841` -> `text/plain`/0; `5858` -> `text/plain`/0; `5858584142` -> `text/plain`/0 |
| `b-len2-off3` | `5b35303a70726f62652f6230355d0a303e333d000241420a` | `585858` -> `text/plain`/0; `58585841` -> `text/plain`/0; `5858584142` -> `probe/b05`/0 |
| `b-len1-off4` | `5b35303a70726f62652f6230365d0a303e343d0001410a` | `41414141` -> `text/plain`/0; `4141414141` -> `probe/b06`/0 |
| `b-len0-off0-r1` | `5b35303a70726f62652f6230385d0a303e303d00002b310a` | `5a` -> `probe/b08`/0; `-` -> `application/x-zerosize`/0; `00` -> `probe/b08`/0 |
| `b-len0-off5` | `5b35303a70726f62652f623038625d0a303e353d00000a` | `5a` -> `text/plain`/0; `5a5a5a5a5a` -> `probe/b08b`/0; `5a5a5a5a5a5a` -> `probe/b08b`/0 |
| `b-len0-off0-r0` | `5b35303a70726f62652f6230395d0a303e303d00002b300a` | `5a` -> `text/plain`/0; `-` -> `application/x-zerosize`/0 |
| `b-big-off` | `5b35303a70726f62652f6231305d0a303e36353533353d0001410a` | `41414141` -> `text/plain`/0 |
| `b-off-overflow` | `5b35303a70726f62652f6231315d0a303e343239343936373239353d0001410a5b34303a70726f62652f623131625d0a303e303d0001410a` | `41` -> `probe/b11b`/0 |
| `b-off-intmax` | `5b35303a70726f62652f6231325d0a303e323134373438333634373d0001410a` | `41` -> `text/plain`/0 |
| `c01-r1` | `5b35303a70726f62652f6330315d0a303e303d0001422b310a` | `4141414142` -> `text/plain`/0 |
| `c02-r2` | `5b35303a70726f62652f6330325d0a303e303d0001422b320a` | `4141414142` -> `text/plain`/0 |
| `c03-r2-off3` | `5b35303a70726f62652f6330335d0a303e333d0001422b320a` | `4141414142` -> `probe/c03`/0; `41414141` -> `text/plain`/0 |
| `c04-r1-off4` | `5b35303a70726f62652f6330345d0a303e343d0001422b310a` | `4141414142` -> `probe/c04`/0 |
| `c05-r0` | `5b35303a70726f62652f6330355d0a303e303d0001422b300a` | `4141414142` -> `text/plain`/0; `42` -> `text/plain`/0 |
| `c06-out-of-bounds-false` | `5b35303a70726f62652f6330365d0a303e303d00025a5a2b31300a` | `41414141` -> `text/plain`/0; `5a5a` -> `probe/c06`/0 |
| `c07-mid` | `5b35303a70726f62652f6330375d0a303e313d000241422b330a` | `41424142` -> `probe/c07`/0; `41424141` -> `text/plain`/0 |
| `c08-tail` | `5b35303a70726f62652f6330385d0a303e333d0001422b340a` | `4141414142` -> `probe/c08`/0 |
| `d-w1-len3` | `5b35303a70726f62652f6430315d0a303e303d00034142437e310a` | `414243` -> `probe/d01`/0; `616263` -> `text/plain`/0 |
| `d-w2-len3` | `5b35303a70726f62652f6430325d0a303e303d00034142437e320a5b34303a70726f62652f643032625d0a303e303d00034142430a` | `414243` -> `text/plain`/0 |
| `d-w2-swap` | `5b35303a70726f62652f6430335d0a303e303d0004000100027e320a` | `01000200` -> `probe/d03`/0; `00010002` -> `application/octet-stream`/1; `01000200ff` -> `probe/d03`/0 |
| `d-w2-len0` | `5b35303a70726f62652f6430345d0a303e303d00007e320a` | `5a` -> `probe/d04`/0; `-` -> `application/x-zerosize`/0 |
| `d-w4-len6` | `5b35303a70726f62652f6430355d0a303e303d00064142434445467e340a5b34303a70726f62652f643035625d0a303e303d00064142434445467e310a` | `414243444546` -> `text/plain`/0 |
| `d-w4-swap` | `5b35303a70726f62652f6430365d0a303e303d0004000102037e340a` | `03020100` -> `probe/d06`/0; `00010203` -> `application/octet-stream`/1 |
| `d-w0-len3` | `5b35303a70726f62652f6430375d0a303e303d00034142437e300a` | `414243` -> `probe/d07`/0; `434241` -> `text/plain`/0 |
| `d-w3` | `5b35303a70726f62652f6430385d0a303e303d000241427e330a5b34303a70726f62652f643038625d0a303e303d000241420a` | `4142` -> `probe/d08b`/0 |
| `d-w2-mask` | `5b35303a70726f62652f6431305d0a303e303d000200012600ff7e320a` | `0199` -> `probe/d10`/0; `0000` -> `application/octet-stream`/1; `0100` -> `probe/d10`/0; `0099` -> `application/octet-stream`/1 |
| `d-w4-mask-len2` | `5b35303a70726f62652f6431315d0a303e303d000200012600017e340a5b34303a70726f62652f643131625d0a303e303d000201000a` | `0100` -> `application/octet-stream`/1 |
| `e-indent0` | `5b35303a70726f62652f6530315d0a303e303d0001410a` | `41` -> `probe/e01`/0 |
| `e-indent1-first` | `5b35303a70726f62652f6530325d0a313e303d0001410a` | `41` -> `text/plain`/0 |
| `e-indent9` | `5b35303a70726f62652f6530335d0a393e303d0001410a` | `41` -> `text/plain`/0 |
| `e-chain01` | `5b35303a70726f62652f6530345d0a303e303d0001410a313e313d0001420a` | `4142` -> `probe/e04`/0; `4143` -> `text/plain`/0; `41425a` -> `probe/e04`/0 |
| `e-chain02-jump` | `5b35303a70726f62652f6530355d0a303e303d0001410a323e313d0001420a5b34303a70726f62652f653035625d0a303e303d0001410a323e313d0001420a` | `4142` -> `text/plain`/0 |
| `e-chain012` | `5b35303a70726f62652f6530365d0a303e303d0001410a313e313d0001420a323e323d0001430a` | `414243` -> `probe/e06`/0; `414244` -> `text/plain`/0; `4142` -> `text/plain`/0 |
| `e-child-fails-parent` | `5b35303a70726f62652f6530375d0a303e303d0001410a313e313d0001420a303e303d0001410a5b34303a70726f62652f653037625d0a303e303d0001410a` | `4143` -> `probe/e07`/0; `4142` -> `probe/e07`/0 |
| `e-sibling` | `5b35303a70726f62652f6531305d0a303e303d0001410a313e313d0001420a313e313d0001430a` | `4143` -> `probe/e10`/0; `4142` -> `probe/e10`/0; `4144` -> `text/plain`/0 |
| `e-deep-skip` | `5b35303a70726f62652f6531325d0a303e303d0001410a313e313d0001420a323e323d0001430a303e353d00015a0a` | `4142435a` -> `probe/e12`/0; `41424351` -> `probe/e12`/0 |
| `f-prio-d2-higher` | `5b35303a70726f62652f6630312d64315d0a303e303d0001410a` d2=`5b36303a70726f62652f6630312d64325d0a303e303d0001410a` | `41` -> `probe/f01-d2`/0 |
| `f-prio-d1-higher` | `5b36303a70726f62652f6630322d64315d0a303e303d0001410a` d2=`5b35303a70726f62652f6630322d64325d0a303e303d0001410a` | `41` -> `probe/f02-d1`/0 |
| `f-tie-d1-first` | `5b35303a70726f62652f6630332d64315d0a303e303d0001410a` d2=`5b35303a70726f62652f6630332d64325d0a303e303d0001410a` | `41` -> `probe/f03-d1`/0 |
| `f-tie-d2-first` | `5b35303a70726f62652f6630342d64312d625d0a303e303d0001410a` d2=`5b35303a70726f62652f6630342d64322d615d0a303e303d0001410a` | `41` -> `probe/f04-d1-b`/0 |
| `f-nohit-hi` | `5b39303a70726f62652f6630352d64315d0a303e303d0001510a` d2=`5b31303a70726f62652f6630352d64325d0a303e303d0001410a` | `41` -> `probe/f05-d2`/0 |
| `f-datahome-tie` | `5b35303a70726f62652f6630362d64315d0a303e303d0001410a` d2=`5b35303a70726f62652f6630362d64325d0a303e303d0001410a` dh=`5b35303a70726f62652f6630362d64685d0a303e303d0001410a` | `41` -> `probe/f06-dh`/0 |
| `f-same-file-tie` | `5b35303a70726f62652f6630382d615d0a303e303d0001410a5b35303a70726f62652f6630382d625d0a303e303d0001410a` | `41` -> `probe/f08-a`/0 |
| `f-prio0` | `5b303a70726f62652f6630392d7a5d0a303e303d0001410a5b313a70726f62652f6630392d6f5d0a303e303d0001410a` | `41` -> `probe/f09-o`/0 |
| `g-header11` | `4d494d452d4d61676963005b35303a70726f62652f6730315d0a303e303d0001410a` | `41` -> `text/plain`/0; `00` -> `application/octet-stream`/1 |
| `g-header12-only` | `` | `41` -> `text/plain`/0; `00` -> `application/octet-stream`/1 |
| `g-header12-ok` | `5b35303a70726f62652f6730335d0a303e303d0001410a` | `41` -> `probe/g03`/0 |
| `g-header-wrong12` | `4d494d452d4d6167696300585b35303a70726f62652f6730345d0a303e303d0001410a` | `41` -> `text/plain`/0 |
| `g-header-empty` | `-` | `41` -> `text/plain`/0 |
| `g-header-13` | `0a5b35303a70726f62652f6730365d0a303e303d0001410a` | `41` -> `text/plain`/0 |
| `h-empty-then-hit` | `5b35303a70726f62652f6830312d656d7074795d0a5b34303a70726f62652f6830312d6869745d0a303e303d0001410a` | `41` -> `probe/h01-hit`/0 |
| `h-empty-eof` | `5b35303a70726f62652f6830325d0a` | `41` -> `text/plain`/0 |
| `h-empty-blank-eof` | `5b35303a70726f62652f6830335d0a0a` | `41` -> `text/plain`/0 |
| `h-bad-line-drops-section` | `5b35303a70726f62652f6830355d0a303e303d0001410a3e303d4241440a5b34303a70726f62652f683035625d0a303e303d0001410a` | `41` -> `probe/h05`/0 |
| `h-bracket-commits` | `5b35303a70726f62652f6830365d0a303e303d0001410a5b34303a70726f62652f683036625d0a303e303d0001410a` | `41` -> `probe/h06`/0 |
| `h-cr` | `5b35303a70726f62652f6830375d0a3e303d0001410d0a5b34303a70726f62652f683037625d0a303e303d0001410a` | `41` -> `probe/h07b`/0 |
| `h-prio-nodigits` | `5b3a70726f62652f6830385d0a3e303d0001410a5b34303a70726f62652f683038625d0a303e303d0001410a` | `41` -> `probe/h08b`/0 |
| `h-prio-overflow` | `5b343239343936373239363a70726f62652f6830395d0a3e303d0001410a5b34303a70726f62652f683039625d0a303e303d0001410a` | `41` -> `probe/h09b`/0 |
| `h-no-close` | `5b35303a70726f62652f6831300a3e303d0001410a5b34303a70726f62652f683130625d0a303e303d0001410a` | `41` -> `probe/h10b`/0 |
| `h-type-junk` | `5b35303a70726f62652f6831315d6a756e6b0a3e303d0001410a` | `41` -> `probe/h11`/0 |
| `h-empty-type` | `5b35303a5d0a3e303d0001410a` | `41` -> ``/0 |
| `h-short-value-eof` | `5b35303a70726f62652f6831335d0a3e303d0001410a3e303d00054142` | `41` -> `probe/h13`/0 |
| `h-short-value-mid` | `5b35303a70726f62652f6831345d0a3e303d000541420a5b34303a70726f62652f683134625d0a303e303d0001410a` | `41` -> `text/plain`/0 |
| `i-nul-type` | `5b35303a70726f62652f693031007a5d0a3e303d0001410a5b34303a70726f62652f693031625d0a303e303d0001410a` | `41` -> `probe/i01b`/0 |
| `i-nul-value` | `5b35303a70726f62652f6930325d0a303e303d0001000a` | `00` -> `probe/i02`/0; `01` -> `application/octet-stream`/1; `-` -> `application/x-zerosize`/0 |
| `i-nul-value3` | `5b35303a70726f62652f6930335d0a303e303d00034100420a` | `410042` -> `probe/i03`/0; `414200` -> `application/octet-stream`/1 |
| `i-nul-endline` | `5b35303a70726f62652f6930345d0a3e303d000141000a5b34303a70726f62652f693034625d0a303e303d0001410a` | `41` -> `probe/i04b`/0 |
| `i-nul-line` | `005b35303a70726f62652f6930355d0a3e303d0001410a` | `41` -> `text/plain`/0 |
| `i-nul-header-12` | `4d494d452d4d6167696300005b35303a70726f62652f6930365d0a303e303d0001410a` | `41` -> `text/plain`/0 |
| `k01-mod-eats-next` | `5b35303a70726f62652f6b30315d0a303e303d0001410a3e303d00034142437e320a5b34303a70726f62652f6b3031625d0a303e303d0001410a` | `41` -> `text/plain`/0 |
| `k02-wordsize-no-eat` | `5b35303a70726f62652f6b30325d0a3e303d000241427e330a5b34303a70726f62652f6b3032625d0a303e303d0001410a` | `41` -> `probe/k02b`/0 |
| `k03-eats-exactly-one` | `5b35303a70726f62652f6b30335d0a3e303d00034142437e320a5b34303a70726f62652f6b3033625d0a303e303d0001410a5b33303a70726f62652f6b3033635d0a303e303d0001410a` | `41` -> `probe/k03c`/0 |
| `k04-mask-eof` | `5b35303a70726f62652f6b30345d0a303e303d0001410a3e303d0002414226` | `41` -> `probe/k04`/0 |
| `k05-value-eof` | `5b35303a70726f62652f6b30355d0a303e303d0001410a3e303d00054142` | `41` -> `probe/k05`/0 |
| `k07-type-no-close-eof` | `5b35303a70726f62652f6b3037` | `41` -> `text/plain`/0 |
| `k07b-type-no-close-nl` | `5b35303a70726f62652f6b3037620a3e303d0001410a5b34303a70726f62652f6b303762325d0a303e303d0001410a` | `41` -> `probe/k07b2`/0 |
| `k08-plus-nodigits` | `5b35303a70726f62652f6b30385d0a3e303d0001412b0a5b34303a70726f62652f6b3038625d0a303e303d0001410a` | `41` -> `probe/k08b`/0 |
| `k09-tilde-nodigits` | `5b35303a70726f62652f6b30395d0a3e303d0001417e0a5b34303a70726f62652f6b3039625d0a303e303d0001410a` | `41` -> `probe/k09b`/0 |
| `k11-zero-len-mask` | `5b35303a70726f62652f6b31315d0a3e303d0000260a` | `5a` -> `probe/k11`/0; `-` -> `application/x-zerosize`/0 |
| `k12-magic-is-dir` | `-` | `41` -> `text/plain`/0 |
| `k13-magic-unreadable` | `-` | `41` -> `text/plain`/0 |
| `k14-matchlet-two-errors` | `5b35303a70726f62652f6b31345d0a424f4755530a5b34303a70726f62652f6b3134625d0a303e303d0001410a` | `41` -> `probe/k14b`/0 |
| `k15-prio-trailing` | `5b312d323a70726f62652f6b31355d0a3e303d0001410a5b34303a70726f62652f6b3135625d0a303e303d0001410a` | `41` -> `probe/k15b`/0 |
| `k16-nested-err` | `5b35303a70726f62652f6b31365d0a303e303d0001410a3e303d00034142437e340a3e313d0001420a5b34303a70726f62652f6b3136625d0a303e303d0001410a` | `4142` -> `probe/k16b`/0 |
| `k17-two-bad-lines` | `5b35303a70726f62652f6b31375d0a3e303d4241440a3e303d414c534f4241440a5b34303a70726f62652f6b3137625d0a303e303d0001410a` | `41` -> `text/plain`/0 |
| `j01-name-only` | `-` | `0001` name=`a.prb` -> `text/x-probe-a`/1; `00` name=`a.unknown` -> `application/octet-stream`/1 |
| `j02-name-one-type` | `5b39303a70726f62652f6a30325d0a303e303d00025a5a0a` | `5a5a` name=`a.prb` -> `text/x-probe-a`/0; `5a5a` name=`a.other` -> `probe/j02`/0 |
| `j03-prio79` | `5b37393a70726f62652f6a37395d0a303e303d00025a5a0a` | `5a5a` name=`a.prb` -> `text/x-probe-a`/1 |
| `j04-prio80` | `5b38303a70726f62652f6a38305d0a303e303d00025a5a0a` | `5a5a` name=`a.prb` -> `probe/j80`/0 |
| `j05-subclass` | `5b35303a70726f62652f6a3530735d0a303e303d00025a5a0a` | `5a5a` name=`a.prb` -> `text/x-probe-a`/0 |
| `j06-desktop` | `5b35303a6170706c69636174696f6e2f782d6465736b746f705d0a303e303d00085b4465736b746f700a` | `5b4465736b746f7020456e74` name=`x.bin` -> `text/plain`/0; `5b4465736b746f7020456e74` -> `application/x-desktop`/0; `5b4465736b746f7020456e74` name=`x.txt` -> `text/plain`/0 |
| `j07-alias` | `5b35303a70726f62652f6a30375d0a303e303d00025a5a0a` | `5a5a` -> `probe/j07`/0; `5a5a` name=`a.prb` -> `text/x-probe-a`/0 |
| `j08-trailing-slash` | `5b35303a70726f62652f6a30385d0a303e303d00025a5a0a` | `5a5a` name=`dir/` -> `inode/directory`/1; `5a5a` name=`/` -> `inode/directory`/1 |
| `j09-basename` | `5b35303a70726f62652f6a30395d0a303e303d00025a5a0a` | `5a5a` name=`some/dir/a.prb` -> `text/x-probe-a`/0; `5a5a` name=`some/dir/noext` -> `probe/j09`/0 |
| `j10-name-vs-prio` | `5b3130303a70726f62652f6a31305d0a303e303d00025a5a0a` | `5a5a` name=`a.prb` -> `probe/j10`/0 |
| `j11-subclass-rev` | `5b35303a70726f62652f6a3530735d0a303e303d00025a5a0a` | `5a5a` name=`a.prb` -> `text/x-probe-a`/1 |
| `j12-globs-not-globs2` | `-` | `00` name=`a.prb` -> `application/octet-stream`/1 |
| `k18-type-high-byte` | `5b35303a70726f62652f6b31382dff5d0a303e303d0001410a5b34303a70726f62652f6b3138625d0a303e303d0001410a` | `41` -> `probe/k18-\xff`/0 |
| `k19-type-space` | `5b35303a70726f62652f6b3139206120625d0a303e303d0001410a` | `41` -> `probe/k19 a b`/0 |
| `k20-type-127` | `5b35303a74747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747...` | `41` -> `ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt`/0 |
| `k21-type-128` | `5b35303a74747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747474747...` | `41` -> `tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt`/0 |
| `k22-offset-zeros` | `5b35303a70726f62652f6b32325d0a303e303030303d0001410a` | `41` -> `probe/k22`/0 |
| `k23-two-headers-one-line` | `5b35303a70726f62652f6b3233615d5b34303a70726f62652f6b3233625d0a303e303d0001410a` | `41` -> `probe/k23a`/0 |
| `k24-type-tab` | `5b35303a70726f62652f6b323409545d0a303e303d0001410a` | `41` -> `probe/k24\x09T`/0 |
| `k25-empty-name` | `5b35303a70726f62652f6b32355d0a303e303d0001410a` | `41` name=`` -> `probe/k25`/0; `41` name=`.` -> `probe/k25`/0 |
| `k26-offset-127` | `5b35303a70726f62652f6b32365d0a303e3132373d0001410a` | `515151515151515151515151` -> `probe/k26`/0; `515151515151515151515151` -> `text/plain`/0; `000000000000000000000000` -> `application/octet-stream`/1 |
| `k27-value-no-final-newline` | `5b35303a70726f62652f6b32375d0a3e303d000141` | `41` -> `text/plain`/0 |
| `k27b-value-final-newline` | `5b35303a70726f62652f6b3237625d0a3e303d0001410a` | `41` -> `probe/k27b`/0 |
| `k28-crlf` | `5b35303a70726f62652f6b32385d0d0a3e303d0001410d0a5b34303a70726f62652f6b3238625d0a303e303d0001410a` | `41` -> `probe/k28b`/0 |
| `k29-nul-after-bracket` | `5b35303a70726f62652f6b32395d006a756e6b0a303e303d0001410a5b34303a70726f62652f6b3239625d0a303e303d0001410a` | `41` -> `probe/k29b`/0 |
| `k30-len-0100` | `5b35303a70726f62652f6b33305d0a3e303d0100414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414...` | `414141414141414141414141` -> `probe/k30`/0; `414141414141414141414141` -> `text/plain`/0; `414141414141414141414141` -> `probe/k30`/0 |
| `k31-len-0101` | `5b35303a70726f62652f6b33315d0a3e303d0101424242424242424242424242424242424242424242424242424242424242424242424242424242424242424242424242424242424242424242424...` | `424242424242424242424242` -> `probe/k31`/0; `424242424242424242424242` -> `text/plain`/0 |
| `k32-len-00ff` | `5b35303a70726f62652f6b33325d0a3e303d00ff434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343434...` | `434343434343434343434343` -> `probe/k32`/0; `434343434343434343434343` -> `text/plain`/0 |
| `k33-prio-intmax` | `5b323134373438333634373a70726f62652f6b33332d68695d0a303e303d0001410a5b323134373438333634363a70726f62652f6b33332d6c6f5d0a303e303d0001410a` | `41` -> `probe/k33-hi`/0 |
| `k34-prio-intmax1` | `5b323134373438333634383a70726f62652f6b33345d0a3e303d0001410a5b34303a70726f62652f6b3334625d0a303e303d0001410a` | `41` -> `probe/k34b`/0 |
| `k35-prio-30zeros` | `5b303030303030303030303030303030303030303030303030303030303030353a70726f62652f6b33355d0a3e303d0001410a5b313a70726f62652f6b3335625d0a303e303d0001410a` | `41` -> `probe/k35b`/0 |
| `k36-prio-30nines` | `5b3939393939393939393939393939393939393939393939393939393939393a70726f62652f6b33365d0a3e303d0001410a5b34303a70726f62652f6b3336625d0a303e303d0001410a` | `41` -> `probe/k36b`/0 |
| `k37-indent-leading-zero` | `5b35303a70726f62652f6b33375d0a30313e313d0001420a5b34303a70726f62652f6b3337625d0a303e303d0001410a` | `4142` -> `probe/k37b`/0 |
| `k38-offset-30digits` | `5b35303a70726f62652f6b33385d0a3e3030303030303030303030303030303030303030303030303030303030303030303030303030303030353d0001410a5b34303a70726f62652f6b3338625d0...` | `41` -> `probe/k38b`/0 |
| `k39-fallback-128` | `5b35303a70726f62652f6b33395d0a303e303d00030102030a` | `414141414141414141414141` -> `text/plain`/0; `414141414141414141414141` -> `application/octet-stream`/1; `000000000000000000000000` -> `application/octet-stream`/1; `000000000000000000000000` -> `application/octet-stream`/1 |
| `k40-fallback-ctrl-positions` | `5b35303a70726f62652f6b34305d0a303e303d0001010a` | `014141414141414141414141` -> `probe/k40`/0; `414141414141414141414141` -> `text/plain`/0; `414141414141414141414141` -> `application/octet-stream`/1 |
| `k41-unknown-type` | `5b35303a6170706c69636174696f6e2f6f637465742d73747265616d5d0a303e303d0001000a5b35303a6170706c69636174696f6e2f6f637465742d73747265616d5d0a303e303d0001410a` | `00` -> `application/octet-stream`/0; `41` -> `application/octet-stream`/0 |
| `j13-zerosize-name` | `5b35303a70726f62652f6a31335d0a303e303d0001410a` | `-` -> `application/x-zerosize`/0; `-` name=`a.prb` -> `text/x-probe-a`/0; `-` name=`a.bin` -> `application/x-zerosize`/0 |
| `k42-dirs-empty-elem` | `5b35303a70726f62652f6b34322d64315d0a303e303d0001510a` d2=`5b35303a70726f62652f6b34322d64325d0a303e303d0001410a` | `41` -> `probe/k42-d2`/0 |
| `k43-dirs-empty-string` | `5b35303a70726f62652f6b34332d64315d0a303e303d0001410a` | `41` -> `text/plain`/0 |
| `k44-dirs-trailing-colon` | `5b35303a70726f62652f6b34342d64315d0a303e303d0001510a` d2=`5b35303a70726f62652f6b34342d64325d0a303e303d0001410a` | `41` -> `probe/k44-d2`/0 |
| `k45-dirs-double-colon-only` | `-` | `41` -> `text/plain`/0 |
| `k46-mod-then-blank` | `5b35303a70726f62652f6b34365d0a3e303d00034142437e320a0a5b34303a70726f62652f6b3436625d0a303e303d0001410a` | `41` -> `probe/k46b`/0 |
| `k47-two-mod-errors` | `5b35303a70726f62652f6b34375d0a3e303d00034142437e320a3e313d00034445467e320a5b34303a70726f62652f6b3437625d0a303e303d0001410a` | `41` -> `probe/k47b`/0 |
| `k48-nomagic-literal` | `5b35303a70726f62652f6b34385d0a303e303d000b5f5f4e4f4d414749435f5f0a` | `5f5f4e4f4d414749435f5f` -> `probe/k48`/0; `5f5f4e4f4d414749435f` -> `text/plain`/0 |
| `k49-cache-garbage` | `5b35303a70726f62652f6b34395d0a303e303d0001410a` | `41` -> `probe/k49`/0 |
| `k50-cache-zeros` | `5b35303a70726f62652f6b35305d0a303e303d0001410a` | `41` -> `probe/k50`/0 |
| `k51-cache-tiny` | `5b35303a70726f62652f6b35315d0a303e303d0001410a` | `41` -> `probe/k51`/0 |
