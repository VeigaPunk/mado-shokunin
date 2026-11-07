source: S524 (GLib 2.90.1 gio/xdgmime/xdgmimemagic.c sha256 fcb1eafe748d3dc18f7f405d1078c8a32e313d23d2fab86b0f12e609ac2ce742, 18289 B — the TEXT magic database parser and matcher), S525 (shared-mime-info spec 0.21 §2.5 "The magic files" at https://specifications.freedesktop.org/shared-mime-info/latest/ar01s02.html sha256 e00fa00e69b1e95ad8642d05fc5023c26f859bdaf8bdda3e091a55feb016c61e, 59208 B — the §2.5 scope of S523's locator, census W04; the §2.12 order is S523's held ground and is cross-referenced in §2.9, not restated), S505 (xdgmime.c afb1c1c1ba726a9fb8d8732f4031f5aa85a67ec3b7a2f989b617e4f4f5282410, 23417 B — re-opened: the text/cache mode switch, the per-directory text load, the text data path and the text subclass walk), S520 (xdgmimeint.c c2364aa825a761255fd6c3390a78c94f06eeaf9babeb07b5ea489ba4cef92f29 — the binary/text fallback), S521 (gcontenttype-fdo.c 8a5b4f475947a9de2e0ca34e60b0dc31f5c56a2d7e0a9fe8cf84002aca8a2d7c — the guess given data, looks_like_text, the desktop rewrite and the arbitration), S522 (glocalfileinfo.c b006a93d8a9733ad9245aba396ca7e3ee42019e214f3addd6e873dbd7d334497 — the GIO caller and its sniff length), S519 (xdgmimecache.c ccda4366a1b3d6feb81c6213fde4885b547189e7cfe612f81799d8c1f298db69 — cited only for the cache-mode priority-0 contrast). All seven files fetched by the L1 `MadoR96` with HTTP 200 and identical digests on two fetches (`.ufo/waves/round-96/receipts/sources-open-r96.txt`); the bytes read here are the committed copies under `.ufo/waves/round-96/fetch/` (digests re-checked by the scribe against that receipt: 3/3 equal; the remaining four files are the round-95 committed copies, digests equal to the receipt's pins).
verified-at: 2026-11-07 — the frozen candidate `tools/mado-mimetext.py` (`tool_sha256` d5f174fc33d0b1f1847897a8e63724c7112137c1bf58a89508d1c1c13b857cbd) against the oracle `.ufo/waves/round-95/controls/mimesniff-oracle-r95.c` (sha256 99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a, glib2 2.90.1-1) over the frozen cases (`284` cases, `423` inputs, 16 classes), a seeded fresh leg (40 cases / 289-319 inputs per seed, all correct), the host leg (9822 pairs: 4911 paths x 2 legs, own path and data-only) and 84 counted mutants (84 killed; 13 further mutants are not observable through this surface and are argued in the declaration's freeze block). The scribe's own labels are §7: 58 oracle fixtures / 66 inputs (`R96MScribeEntry-probe.out.txt`) plus a read-only parse of the host's text magic database; they are rule probes, not the frozen measurement, and every the pin cells cell above is filled by the L1 from `.ufo/waves/round-96/receipts/c1-measured-r96.txt`.
recheck: 90d — re-pull `xdgmimemagic.c` and `xdgmime.c` at the next GLib tag that changes either (2.90.1 is the pin); also when `glib2` leaves 2.90.1-1 or `shared-mime-info` leaves 2.5.1-2 (the host's `mime/magic` bytes are part of every host answer), and when `update-mime-database` changes its text writer. A GLib change to the state machine, the number reader or the word-size branch flips this entry.
covers: what GLib 2.90.1 `g_content_type_guess (name-or-NULL, data, len, &uncertain)` answers when the process is in the **text database mode** — no loadable `mime.cache` in any reachable directory — and the bytes reach `xdgmimemagic.c`: the 12-byte `MIME-Magic\0\n` gate, the `[priority:type]` header, the matchlet line (indent, offset, two-byte big-endian value length, value, mask, word size with little-endian swap at parse, range), the state machine's whole-section drop on a bad line, section order by priority with ties in file order, first matching section wins, the indent tree including its indent-jump blind spot, the compare's bounds rule, the priority-0 answer that cache mode does not give, the binary/text fallback and the guess combination with the text name step; the departures from the spec's §2.5 wording; and `tools/mado-mimetext.py`, the read-only tool that answers it.

# The TEXT MIME database's magic step: what GLib 2.90.1 guesses from bytes without a cache

This entry states the answer GLib 2.90.1 gives to `g_content_type_guess (filename-or-NULL, data,
len, &uncertain)` when **no loadable `mime.cache` exists in any reachable directory**, so xdgmime
reads the text `mime/magic` file instead of a cache. Its predecessors are
`corpus/knowledge/mime-glob-guess-r94.md` (the name step in both modes) and
`corpus/knowledge/mime-magic-sniff-r95.md` (the magic step in **cache** mode); this entry does not
restate either. Line numbers are those of `xdgmimemagic.c` and `xdgmime.c` as named in the front
matter; page line numbers of the spec are those of the fetched `ar01s02.html` text extraction.
Every behavioural statement carries a source line (S524/S525/S505/S520/S521/S522), a scribe probe
row of §7, or is marked **[UNVERIFIED]**.

## 1. Question and scope

- **When this path runs.** `xdg_mime_get_mime_type_for_data` (`xdgmime.c`:516-541, S505) checks the
  mode with one branch: `if (_caches) ... cache ... else ... _xdg_mime_magic_lookup_data
  (global_magic, ...)` (S505 `xdgmime.c`:530-535). `_caches` is filled per directory by
  `xdg_mime_init_from_directory`: a `mime.cache` that `_xdg_mime_cache_new_from_file` loads makes
  that directory a cache and **skips its text files** (`xdgmime.c`:137-153); a directory without a
  loadable cache contributes `globs2`/`globs`, `magic`, `aliases`, `subclasses`, `icons`,
  `generic-icons` (`:157-211`). So a text `magic` file is parsed even on a cache-mode host, but it
  is **never consulted** while any directory holds a loadable cache. This entry covers the
  zero-cache state only; a loadable cache in any reachable directory is cache mode (round 95) and
  `tools/mado-mimetext.py` refuses it (exit 3).
- **The directory list.** `$XDG_DATA_HOME/mime/`, or `$HOME/.local/share/mime/` when
  `XDG_DATA_HOME` is unset; then each `$XDG_DATA_DIRS` entry + `/mime/` (`xdgmime.c`:216-300,
  S505; quote at :231 `xdg_data_home = getenv ("XDG_DATA_HOME"); home = getenv ("HOME"); xdg_data_dirs = getenv ("XDG_DATA_DIRS"); if (xdg_data_dirs == NULL) xdg_data_dirs = "/usr/local/share/:/usr/share/";`). `XDG_DATA_DIRS` unset means
  `/usr/local/share/:/usr/share/` (`:231`), which on this host reaches `/usr/share/mime` and its
  `mime.cache`: the frozen cases therefore require a non-null `XDG_DATA_DIRS`.
- **What is parsed.** `DIR/mime/magic` only when `stat` finds it (`xdgmime.c`:180-186, S505); no
  other text file feeds the magic step. `magic-deleteall` is not implemented by the reader (§3, b).
- **Data as passed.** GLib reads exactly `data_size` bytes; the caller's sniff length is the
  caller's choice (S522 `glocalfileinfo.c`:1340-1373, r95 §1). The tool reads the whole file.
- **Out of scope.** Cache mode (r95); the name step's own glob rules (r94); the application step
  (r91/r92); `xdg_mime_get_mime_type_for_file`'s elimination loop, which the guess path does not
  reach (`xdgmime.c`:535 passes `NULL, 0`, r95 §2.3.5).
- **Evidence class.** §2-§4 carry S-row lines; §7 carries the scribe's oracle-labelled probes and a
  read-only host parse; §9 is the frozen set and carries the pins the L1 measured from the round's receipt; they are listed in the seat report.

## 2. The rules

### 2.1 The file gate

| rule | source | anchor | quote |
|---|---|---|---|
| the magic file is opened with `fopen (file_name, "r")`; failure contributes nothing | S524 | xdgmimemagic.c:809 | `magic_file = fopen (file_name, "r"); if (magic_file == NULL) return;` |
| exactly 12 bytes are read; a shorter file contributes nothing | S524 | xdgmimemagic.c:812 | `if (fread (header, 1, 12, magic_file) == 12)` |
| the 12 bytes must be `MIME-Magic\0\n`; anything else contributes nothing | S524 | xdgmimemagic.c:814 | `if (memcmp ("MIME-Magic\0\n", header, 12) == 0)` |

There is no version number and no fallback to another file name (`magic2` is the spec's future
name, P01, S525). A file whose first 12 bytes differ is silently ignored: the answer is then the
fallback of §2.9 or the name rules of §2.10 (probes A2, A3, A4 all answer `text/plain 0` for
`HI`). The gate is one `memcmp` over the exact bytes; a `\r` where `\n` belongs fails (A2).

### 2.2 The section header

The parser is a four-state machine (`SECTION`, `MAGIC`, `ERROR`, `EOF`, `xdgmimemagic.c`:41-47,
S524). A section begins with a line:

| rule | source | anchor | quote |
|---|---|---|---|
| the first byte must be `[` | S524 | xdgmimemagic.c:244 | `if (c != '[') return XDG_MIME_MAGIC_ERROR;` |
| the priority is read by the digit reader | S524 | xdgmimemagic.c:247 | `match->priority = _xdg_mime_magic_read_a_number (magic_file, &end_of_file);` |
| a `:` must follow the priority | S524 | xdgmimemagic.c:256 | `if (c != ':') return XDG_MIME_MAGIC_ERROR;` |
| the type runs to the first `]` in the rest of the line | S524 | xdgmimemagic.c:267 | `while (*end_ptr != ']' && *end_ptr != '\000' && *end_ptr != '\n') end_ptr++;` |
| a missing `]` is an error | S524 | xdgmimemagic.c:269 | `if (*end_ptr != ']') { free (buffer); return XDG_MIME_MAGIC_ERROR; }` |

The digit reader (`:184-225`, S524) accepts **digits only** (no sign, no space), at most 30 of
them, and returns -1 when there is none or when `strtol` overflows an `int`:

| rule | source | anchor | quote |
|---|---|---|---|
| the first non-digit ends the number (and is pushed back) | S524 | xdgmimemagic.c:204 | `if (! isdigit (c)) { ungetc (c, magic_file); break; }` |
| at most 30 digits are kept | S524 | xdgmimemagic.c:211 | `if (pos == MAX_NUMBER_SIZE) break;` |
| a value outside `int` is a parse error | S524 | xdgmimemagic.c:220 | `if ((retval < INT_MIN) || (retval > INT_MAX) || (errno != 0))` |

The type is read by `_xdg_mime_magic_read_to_newline` (`:147-180`), which stops at `\n` **or a
NUL** (S524 `:168`, `if (c == '\n' || c == '\000')`); a NUL inside the type therefore ends the buffer before any `]`
and the header errors (probe B6: the section is dropped and the next section answers). The type may
be **empty** (`[90:]`): the C stores `""` and, if that section matches, the guess returns an empty
type string with `uncertain = 0` (probe F1) - a label the tool must be able to print. The type keeps
spaces and `/` verbatim (probe F2: `application/x a`). Bytes between `]` and the newline are read
and discarded with the rest of the line (`read_to_newline` consumed it): `[90:application/x-a]junk`
is a normal section (probe F3; the critic's F9 measured the same). A NUL between `]` and the newline
is different: the line reader stops there, so the bytes after the NUL are parsed as a new line and
error (the section survives; that junk line is skipped).

### 2.3 The matchlet line

A matchlet line is `[indent] ">" offset "=" <len:2 bytes BE><value> ["&" mask] ["~" word]
["+" range] "\n"` (`:297-513`, S524). Defaults are set in `_xdg_mime_magic_matchlet_new`:

| rule | source | anchor | quote |
|---|---|---|---|
| indent 0 and offset 0 by default | S524 | xdgmimemagic.c:93 | `matchlet->indent = 0; matchlet->offset = 0;` |
| range 1 and word size 1 by default | S524 | xdgmimemagic.c:98 | `matchlet->range_length = 1; matchlet->word_size = 1;` |
| the offset is read by the digit reader | S524 | xdgmimemagic.c:350 | `matchlet->offset = _xdg_mime_magic_read_a_number (magic_file, &end_of_file);` |
| an `=` must follow the offset | S524 | xdgmimemagic.c:367 | `else if (c != '=') { _xdg_mime_magic_matchlet_free (matchlet); return XDG_MIME_MAGIC_ERROR; }` |
| the two length bytes are big-endian | S524 | xdgmimemagic.c:382 | `matchlet->value_length = matchlet->value_length << 8;` |
| an optional `&` starts a mask of exactly `value_length` bytes | S524 | xdgmimemagic.c:420 | `bytes_read = fread (matchlet->mask, 1, matchlet->value_length, magic_file); if (bytes_read != (size_t) matchlet->value_length)` |
| a `~` word size must be 0, 1, 2 or 4 | S524 | xdgmimemagic.c:440 | `if (matchlet->word_size != 0 && matchlet->word_size != 1 && matchlet->word_size != 2 && matchlet->word_size != 4)` |
| word > 1 requires `value_length % word_size == 0` | S524 | xdgmimemagic.c:476 | `if (matchlet->value_length % matchlet->word_size != 0) { _xdg_mime_magic_matchlet_free (matchlet); return XDG_MIME_MAGIC_ERROR; }` |
| on a little-endian host the value (and mask) are byte-swapped per word **at parse time** | S524 | xdgmimemagic.c:486 | `*((xdg_uint16_t *) (matchlet->value + i)) = SWAP_BE16_TO_LE16 (*((xdg_uint16_t *) (matchlet->value + i)));` |
| an optional `+` sets the range length | S524 | xdgmimemagic.c:453 | `if (c == '+') { matchlet->range_length = _xdg_mime_magic_read_a_number (magic_file, &end_of_file);` |
| the line must end in `\n`; the swap happens at that point | S524 | xdgmimemagic.c:471 | `if (c == '\n') { /* We clean up the matchlet, byte swapping if needed */ if (matchlet->word_size > 1)` |

Consequences measured by the probes:

- `~2` really swaps at parse: value bytes `00 01 00 02` match data `01 00 02 00` and **not**
  `00 01 00 02` (D9); `~4` swaps each 4-byte group (D10).
- `~0` is **accepted** (the check allows 0) and behaves as 1, i.e. no swap (D11); `~3` and a bare
  `~` are parse errors and drop the section (D12, D14); 3 bytes with `~2` is a parse error (D13).
- a mask of the wrong length cannot be expressed: the reader takes exactly `value_length` bytes, so
  a short mask is an EOF/error and drops the section (`:420-428`).
- an unknown byte where the newline belongs is an error (`:508-512`), so `>0=..HI!` drops the
  section (B3); a bare newline inside a section is skipped and the section continues (D17); indent
  digits not followed by `>` drop the section (D18).
- a zero-length value matches any data with `len > 0` at the first offset (D15).

Matchlets are parsed onto the head of the section's list and the list is **mirrored** when the
section closes (`:501-502`, `:777`), so the section's matchlet order is file order:

| rule | source | anchor | quote |
|---|---|---|---|
| prepend while parsing | S524 | xdgmimemagic.c:501 | `matchlet->next = match->matchlet; match->matchlet = matchlet;` |
| mirror and insert on section close | S524 | xdgmimemagic.c:777 | `match->matchlet = _xdg_mime_magic_matchlet_mirror (match->matchlet); _xdg_mime_magic_insert_match (mime_magic, match);` |

### 2.4 A bad line drops the whole section

| rule | source | anchor | quote |
|---|---|---|---|
| `parse_error` skips to the next newline and returns to `SECTION` | S524 | xdgmimemagic.c:292 | `if (c == '\n') return XDG_MIME_MAGIC_SECTION;` |
| the section's match list is freed on `ERROR` or on `EOF` without a type | S524 | xdgmimemagic.c:780 | `else if (state == XDG_MIME_MAGIC_EOF || state == XDG_MIME_MAGIC_ERROR) _xdg_mime_magic_match_free (match);` |

A section is therefore kept or dropped as a unit: one bad matchlet line after ten good ones loses
all eleven (probes B1, B3, B5, B6). A matchlet line that ends at EOF without its newline is an EOF
for the line parser (`:508-510`): the matchlet is freed and the section is inserted empty, so it
answers the fallback (probe G4). After the skip, the next line is read in `SECTION` state, so a
following matchlet line is an error again and is dropped line by line until a line starts with `[`;
a later well-formed section answers normally (B1, B2, B4). The spec's wording is narrower - only
the bad *line* should be ignored (P10, S525) - see §3(a).

One subtlety the receipt's summary compresses: the machine inserts the section when the matchlet
reader returns `SECTION` (the next line began with `[`) **or** `EOF` with a mime type set
(`:772-778`), whether or not any matchlet survived. A section with zero matchlets is therefore
inserted with an empty list; it can never match (`compare_level` starts at indent 0 over a NULL
list) and changes no answer. A value that hits EOF mid-way frees the matchlet and inserts the empty
section (probe G3), which answers the fallback.

### 2.5 Which section answers

| rule | source | anchor | quote |
|---|---|---|---|
| a higher priority is inserted before the head | S524 | xdgmimemagic.c:608 | `if (match->priority > mime_magic->match_list->priority)` |
| a new section is inserted **after** every equal priority (strict `<`) | S524 | xdgmimemagic.c:618 | `if (list->next->priority < match->priority)` |
| the lookup walks the list and takes the **first** section whose tree holds | S524 | xdgmimemagic.c:668 | `for (match = mime_magic->match_list; match; match = match->next) { if (_xdg_mime_magic_match_compare_to_data (match, data, len)) { prio = match->priority; mime_type = match->mime_type; break; }` |
| when nothing holds, the lookup returns NULL (`mime_type == NULL`) | S524 | xdgmimemagic.c:685 | `if (mime_type == NULL) { for (n = 0; n < n_mime_types; n++) { if (mime_types[n]) mime_type = mime_types[n]; } }` |

So file order is irrelevant except for equal priorities, where the earlier line (and, across
directories, the earlier directory - `$XDG_DATA_HOME` before `$XDG_DATA_DIRS`) comes first (probes
C2, C3, C4). The priority is an `int`; a value above `INT_MAX` never parses (C5), and a priority
there is no separate `priority > 0` test in text mode: **a section with priority 0 answers**
(probe C1: `[0:application/x-zero]` answers `application/x-zero 0`), unlike cache mode, which
discards it (`xdgmimecache.c:784` `if (priority > 0)`, S519; r95 §2.3.2 rule 4). The recorded
priority is not itself printed by the tool; it is the arbitration input of §2.10 (a prio-0 answer is
below the 80 threshold).

### 2.6 The matchlet tree

| rule | source | anchor | quote |
|---|---|---|---|
| only matchlets at the current indent are candidates | S524 | xdgmimemagic.c:563 | `while ((matchlet != NULL) && (matchlet->indent == indent))` |
| a holding matchlet with no deeper next is TRUE; otherwise the next indent+1 is tested as a child | S524 | xdgmimemagic.c:571 | `if ((matchlet->next == NULL) || (matchlet->next->indent <= indent)) return TRUE; if (_xdg_mime_magic_matchlet_compare_level (matchlet->next, data, len, indent + 1)) return TRUE;` |
| a failed chain skips the whole deeper subtree and continues with the next sibling | S524 | xdgmimemagic.c:582 | `do { matchlet = matchlet->next; } while (matchlet && matchlet->indent > indent);` |

The child test is a **recursion at indent+1 over the next matchlet**, not the spec's "preceding
entry with an indent one less" (P09, S525). For a well-formed file the two readings coincide; they
diverge on malformed indents, and the C's reading makes the section unmatchable:

- indent 0 then indent **2**: there is no matchlet at indent 1, the recursion returns FALSE, the
  chain fails, the do-while skips the indent-2 matchlet, and the section never matches even though
  its top-level value held (probe E6: data `AB` -> `text/plain 0`).
- a section whose **first** matchlet is at indent 1: `compare_level` starts at indent 0, the list
  head has indent 1, the loop never runs, the section never matches (probe E7).

For a well-formed tree the measured behaviour is the expected one: child holds (E1), child fails
(E2), parent fails so the child is skipped but the next top-level matchlet is still tested (E3),
either of two children holds (E4), and an indent-2 chain needs both levels (E5).

### 2.7 The compare

| rule | source | anchor | quote |
|---|---|---|---|
| every offset in `[offset, offset+range)` is tried | S524 | xdgmimemagic.c:521 | `for (i = matchlet->offset; i < matchlet->offset + matchlet->range_length; i++)` |
| a value that does not fit returns FALSE for the whole matchlet | S524 | xdgmimemagic.c:525 | `if (i + matchlet->value_length > len) return FALSE;` |
| with a mask, bytes compare as `(value & mask) == (data & mask)` | S524 | xdgmimemagic.c:532 | `if ((matchlet->value[j] & matchlet->mask[j]) != ((((unsigned char *) data)[j + i]) & matchlet->mask[j]))` |
| without a mask, bytes compare directly | S524 | xdgmimemagic.c:544 | `for (j = 0; j < matchlet->value_length; j++) { if (matchlet->value[j] != ((unsigned char *) data)[j + i])` |
| the first offset that holds makes the matchlet TRUE | S524 | xdgmimemagic.c:551 | `if (valid_matchlet) return TRUE;` |

The bounds rule is **FALSE for the whole matchlet, not `continue`**: once `i + value_length > len`
at some offset of the range, the remaining offsets are not tried (D5: `ABC` against a 4-byte value
is the fallback; D6: a 2-byte value 200 bytes in on a 2-byte buffer is the fallback). An exact fit
(`i + value_length == len`) matches (D16). A `+0` range never enters the loop and never matches
(D4). The range start may lie past the buffer (D6). `mask` is present only when `&` was parsed, and
it is compared with the same length (D7, D8).

The loop arithmetic is `unsigned int`: `i + matchlet->value_length` wraps at 2**32 before it is
compared with the size_t `len` (`:521-526`). With an offset near `INT_MAX` the C can therefore read
past the caller's buffer - undefined behaviour, not a rule; a model must refuse or fix that case
(§6). The tool's contract declares it.

### 2.8 max_extent

The text parser records the largest extent any matchlet needs
(`extent = value_length + offset + range_length`, max over the list) and exposes it as the
database's max extent:

| rule | source | anchor | quote |
|---|---|---|---|
| the extent of a matchlet is the sum of its three fields | S524 | xdgmimemagic.c:714 | `extent = matchlet->value_length + matchlet->offset + matchlet->range_length;` |
| the parser's max extent is returned to callers | S524 | xdgmimemagic.c:648 | `int _xdg_mime_magic_get_buffer_extents (XdgMimeMagic *mime_magic) { return mime_magic->max_extent;` |

On this host the text database's max extent is 18730 bytes (§7), which is above GIO's 16 KiB sniff
buffer (S522 `glocalfileinfo.c`:1345, :1351-1353; the clamp is the r95 entry's S522 reading): a
range-only matchlet whose hit lies beyond 16384 bytes can therefore never be found through GIO,
although `g_content_type_guess` with the whole file would find it. GLib's own
`xdg_mime_get_mime_type_for_file` reads `max_extent` bytes without a clamp (`xdgmime.c`:590-602).

### 2.9 The data function

`xdg_mime_get_mime_type_for_data` (`xdgmime.c`:516-541, S505) is:

| state | answer | source |
|---|---|---|
| `len == 0` | `application/x-zerosize`, prio 100, before anything else | S505 `:523-527` `if (len == 0) { if (result_prio != NULL) *result_prio = 100; return XDG_MIME_TYPE_EMPTY;` |
| a section holds | that section's type, prio = its priority | S524 §2.5 |
| nothing holds | `_xdg_binary_or_text_fallback (data, len)` | S505 `:540` `return _xdg_binary_or_text_fallback(data, len);` |

The fallback is round 95's: the first 128 bytes decide binary when a byte is below 32 except TAB,
LF, CR (S520 `xdgmimeint.c`:185-186, `if (chardata[i] < 32 && chardata[i] != 9 && chardata[i] != 10 && chardata[i] != 13) return XDG_MIME_TYPE_UNKNOWN; /* binary data */`), otherwise `text/plain` (`:189`,
`return XDG_MIME_TYPE_TEXTPLAIN;`); when the sentinel survives, `looks_like_text` over the whole buffer can promote it
(S521 `:625-628`, r95 §2.4). The VT rule carries over unchanged: a `0x0b` in the first 128 bytes
makes the data binary (probe D19: `ab\x0bcd` -> `application/octet-stream 1`; r95's D3).
Empty data is answered before the database is read at all (probe H8: `application/x-zerosize 0`).

The spec's recommended checking order is the document's, not GLib's: §2.12 puts the glob match
first and the magic sniff on conflict or failure, and treats the first 128 bytes as a text/binary
hint (S523; the ten departures are r95 §3). This entry's surface is the magic step alone; a
caller that reaches it has already lost the one-name-type short-circuit (§2.10).

### 2.10 The guess with the name step

The arbitration in `g_content_type_guess_impl` (S521 `:567-690`) is unchanged by the mode; only the
subclass test's source changes (see below). In order:

| state | answer | uncertain | source |
|---|---|---|---|
| name ends `/` | `inode/directory` | 1 | S521 `:597-603` `if (i > 0 && filename[i - 1] == '/') {` |
| exactly one name type | that type; the bytes are **not read** | 0 | S521 `:613-620` `if (n_name_mimetypes == 1)` |
| data given | `xdg_mime_get_mime_type_for_data` | - | S521 `:622-624` `if (data)` `sniffed_mimetype = xdg_mime_get_mime_type_for_data (data, data_size, &sniffed_prio);` |
| sentinel + `looks_like_text` | `text/plain` | 0 | S521 `:625-628` `if (sniffed_mimetype == XDG_MIME_TYPE_UNKNOWN &&` |
| sniffed `application/x-desktop` and a filename was given | `text/plain` | 0 | S521 `:636-638` `if (filename != NULL && strcmp (sniffed_mimetype, "application/x-desktop") == 0) sniffed_mimetype = "text/plain";` |
| zero name types | the sniffed type | 1 iff it is the sentinel | S521 `:641-647` `if (n_name_mimetypes == 0)` |
| two or more, sniffed non-sentinel, prio >= 80 | the sniffed type | 0 | S521 `:652-655` `if (sniffed_prio >= 80) /* High priority sniffing match, use that */` |
| two or more, no subclass name type | the first name type | 1 | S521 `:675-683` `mimetype = g_strdup (name_mimetypes[0]);` `*result_uncertain = TRUE;` |
| two or more, some name type is a subclass of the sniffed type | that name type | 0 | S521 `:661-671` `if ( xdg_mime_mime_type_subclass (name_mimetypes[i], sniffed_mimetype))` |

The text-mode subclass walk (S505 `:820-890`) is the text-file twin of the cache walk: it
dispatches to the cache variant only when `_caches` is set (`:830-831`), unaliases both sides
through the text `aliases` list (`:833-834`), then applies equality, a super type (`x/*`), the
`text/plain` rule and the `application/octet-stream` rule, and finally walks the text `subclasses`
parents with a cycle guard:

| rule | source | anchor | quote |
|---|---|---|---|
| cache mode dispatches to the cache subclass walk | S505 | xdgmime.c:830 | `if (_caches) return _xdg_mime_cache_mime_type_subclass (mime, base, NULL);` |
| text mode unaliases through the text alias list | S505 | xdgmime.c:833 | `umime = _xdg_mime_unalias_mime_type (mime); ubase = _xdg_mime_unalias_mime_type (base);` |
| `x/*` base holds for its own media type | S505 | xdgmime.c:841 | `if (xdg_mime_is_super_type (ubase) && xdg_mime_media_type_equal (umime, ubase))` |
| any `text/*` is a subclass of `text/plain` | S505 | xdgmime.c:847 | `if (strcmp (ubase, "text/plain") == 0 && strncmp (umime, "text/", 5) == 0)` |
| `application/octet-stream` holds for everything but `inode/*` | S505 | xdgmime.c:851 | `if (strcmp (ubase, "application/octet-stream") == 0 && strncmp (umime, "inode/", 6) != 0)` |
| parents come from the text `subclasses` list | S505 | xdgmime.c:861 | `parents = _xdg_mime_parent_list_lookup (parent_list, umime);` |

A parent relation present only in a `mime.cache` is invisible in text mode, and vice versa (r95's
§6.6 mirrored). The measured combination rows are H1-H9: one name type beats a priority-90 magic
(H1: `text/x-one 0` for binary bytes); zero name types answer the magic type (H2, both NULL and a
non-matching name); two name types with a 90 magic answer the magic type 0 (H3); with a 50 magic
the first name type wins, uncertain 1 (H4); a sniffed `text/plain` lets the first `text/*` name
type win, certain (H5); a sniffed desktop body with a name becomes `text/plain` (H6) while with no
name it stays `application/x-desktop 0`; a trailing `/` answers `inode/directory 1` (H7); empty
data answers zerosize unless one name type short-circuits it (H8); and a priority-0 magic loses to
one name type (H9).

## 3. Where GLib departs from the spec (S525 for §2.5, S523 for §2.12)

| # | GLib 2.90.1 text reader | spec | row |
|---|---|---|---|
| a | one bad matchlet line frees the **whole section** (`:283-295`, `:780-781`) | "If an unknown character is found where a newline is expected then the whole line should be ignored" (P10) | B1, B3, B5 |
| b | `>0=__NOMAGIC__` is an ordinary 10-byte value; no directory elimination exists in the reader (`grep -n NOMAGIC` over the fetched bytes: the token is absent) | the marker means earlier directories' rules MUST be discarded (P11) | not measurable through the guess; the reader has no code path |
| c | sections are re-sorted by priority on insert; file order only breaks ties (P03 says entries come first) | "Higher priority entries come first" (P03) | C2, C3 |
| d | `~0` is accepted and compared as 1 (the spec's word-size examples are 1, 2 and 4: `~2` in the table, 1 in P06, 4 in the `host32` note) | word size 1, 2, 4 | D11 |
| e | the parent is the **next** matchlet at indent+1; an indent jump leaves no parent and the section cannot match | "The parent of an entry is the preceding entry with an indent one less" (P09) | E6, E7 |
| f | an empty type is accepted and answered (`[90:]` -> `""` 0) | the type is between the brackets; nothing allows it to be empty | F1 |
| g | priority 0 answers in text mode | silent (the spec has no priority-0 rule; cache mode discards it) | C1 |

(a)-(d) are the receipt's recorded divergences; (e)-(g) are the scribe's additions from the probes
(see the report's findings list).

## 4. Operator consequences

1. **The text database is the fallback, not the norm.** On this host `/usr/share/mime/mime.cache`
   exists, so GLib is in cache mode and the text `magic` file is parsed (from cache-less
   directories) but never consulted. The text rules become live when no reachable directory holds
   a loadable cache: a fresh `~/.local/share/mime` without a cache, a container with only the text
   files, or a deleted cache. Editing `~/.local/share/mime/magic` by hand is then live, and its
   section-drop rule means one bad byte silently removes the whole type, not one rule.
2. **A hole is a hole for the whole section.** Ten good rules and one typo answer nothing (B1).
   The spec's promise that only the bad line is ignored does not hold here.
3. **Order matters only for ties.** Re-sorting means an operator can append a high-priority
   section at the end of the file; equal priorities keep file order, and across directories
   `$XDG_DATA_HOME` wins over `$XDG_DATA_DIRS` (C4). A section at priority 0 is still live (C1),
   which operators may not expect from cache-mode experience.
4. **`~0` is a silent no-op, not an error.** A rule written with `~0` parses and compares raw bytes.
5. **Malformed indents disable a section.** An indent jump (0 then 2) or a first matchlet at
   indent 1 makes the section unable to match anything, with no message.
6. **The text database is what a cache-less system sees.** `update-mime-database` writes the cache
   from the same text files; on this host the text file holds 689 sections and 1743 matchlets
   (1282 top-level), the same 689/1282 the cache encodes (r95 §2.3, §7 here).
7. **The 16 KiB sniff clamp can hide a range-only rule.** The text database's max extent on this
   host is 18730 bytes; GIO reads at most 16384 (S522), so a rule that only matches beyond that
   offset never fires for GIO callers.

## 5. The tool and how to run it

`tools/mado-mimetext.py` (target path; the in-wave draft is
`.ufo/waves/round-96/build/mado-mimetext.c1.py`) is read-only: it opens only the `mime` files under
the roots it is given and the files it is asked to sniff, writes nothing, and loads round 94's
`tools/mado-mimeglob.py` **from its own directory** for the text name step (lazily, on the main
path only, so `--selftest` runs on a lone copy).

``sh
python3 -I tools/mado-mimetext.py --json notes.txt                  # name NULL, bytes sniffed
python3 -I tools/mado-mimetext.py --json --name x.png notes.txt     # one name for every FILE
python3 -I tools/mado-mimetext.py --json --names-from-files a.pdf   # each path as its own name
python3 -I tools/mado-mimetext.py --data-home <root>/dh --data-dirs '<root>/d1:<root>/d2' --home <root>/h a.bin
python3 -I tools/mado-mimetext.py --data-home-unset --data-dirs-unset --home-unset a.bin
python3 -I tools/mado-mimetext.py --selftest                        # checks=N failed=0, rc 0
``

Output (exit 0): one `MADO_MIMETEXT: <type> uncertain=<0|1> name=<escaped|-> file=<escaped>` line
per input plus one `MADO_MIMETEXT_DIRS: mode=text|none dirs=<comma list>` line; `--json` prints one
object `{"mode","dirs","results":[{"type","uncertain","types","sniffed","prio","file","name"}]}`
(the draft's shape; `types` is the name step's list, empty when the name is NULL, and `sniffed`/`prio`
are diagnostics). The frozen cases score the text lines only.

**Verdict map.**

| GLib state | tool exit | tool line |
|---|---|---|
| answered in text mode or none mode | 0 | `type` and `uncertain` equal to the oracle's `<type>\t<0\|1>` |
| no FILE, both name options, an unreadable FILE | 2 | `mado-mimetext: setup error: ...` on stderr |
| a loadable `mime.cache` in any reachable directory | 3 | `MADO_MIMETEXT: UNSUPPORTED <reason>` per file (the reason names cache mode) |

An exit-3 run is a refusal, never an answer: a frozen cache-mode case is labelled
`["UNSUPPORTED", null]` and only exit 3 satisfies it (round 95 owns that answer). `--selftest`
prints `MADO_MIMETEXT_SELFTEST_FAIL: <label>` per failing check and
`MADO_MIMETEXT_SELFTEST: checks=N failed=0` on success (stdout, N >= 18), exit 0/1.

## 6. Limits and unknowns

1. **Text mode only.** Any loadable `mime.cache` in any reachable directory is cache mode (S505
   `:137-153`, `:530-535`); the tool refuses (exit 3). An invalid cache (e.g. 40 zero bytes) does
   not switch the mode and the text file answers (probe G1).
2. **`for_data` only.** The `mime_types` elimination loop of `_xdg_mime_magic_lookup_data`
   (`:674-692`) is unreachable for the guess (the caller passes `NULL, 0`).
3. **No caller sniff policy.** The tool reads whole files; GIO reads `min(max_extent, 16384)`
   (S522, §2.8), so a host answer for a range-only rule beyond 16384 bytes can differ from the
   tool's whole-file answer.
4. **Undefined C is refused, not reproduced** (exit 3): a compare whose `i + value_length` wraps
   the 32-bit `unsigned int` and reads past the buffer; and a matchlet chain deep enough to exhaust
   the reader's recursion (round 95 declared a 4096-level cap for its cache tree; the C1 contract
   names no cap for this tool, so the freeze should state the number it uses). The frozen set
   carries no case for either.
5. **`~0` and priority 0 are real C behaviour**, not malformed input; cases for them belong in the
   frozen set (the declaration's "1|2|4 only" wording is narrower than the C).
6. **A section with no matchlet is inert.** It is inserted (the state machine keeps it) and can
   never match; no oracle-visible case distinguishes it from a dropped section, so it is declared
   here, not measured.
7. **An empty type is printable but odd**: `[90:]` answers `""` 0; a tool that strips the field
   would diverge from the oracle's `\t0` line. The frozen `header` class should carry it.
8. **The type string is raw bytes** up to `]` (spaces and `/` kept); GLib does not validate it as a
   MIME type anywhere on this path.
9. **The number reader is locale-sensitive in principle** (`isdigit`/`strtol`), and the oracle runs
   `LC_ALL=C`; the tool pins `C`. A locale's extra digits are not modelled.
10. **The subclass walk uses the text `aliases`/`subclasses` files** (S505 `:833`, `:861`); a
    parent relation present only in a cache is invisible.
11. **Labels come from the installed glib2 2.90.1-1 and shared-mime-info 2.5.1-2** (a distro patch
    would be scored as upstream), and the host database's bytes are part of every host answer.
12. **`magic-deleteall` is not implemented by the reader** (§3 b); `update-mime-database` bakes it
    into the file it writes, so a hand-made file can express it only by omission.

## 7. Measured results (scribe probes and the host database)

### 7.1 Oracle fixtures

`R96MScribeEntry-probe.py` (kept with its output as `R96MScribeEntry-probe.out.txt`) builds 58
fixture roots under scratch (`{root}/{h,dh/mime,d1/mime,d2/mime}`), writes the `mime/magic` bytes,
and runs the round-95 oracle once per root with
`env -i LC_ALL=C HOME=<root>/h XDG_DATA_HOME=<root>/dh XDG_DATA_DIRS=<root>/d1:<root>/d2
<oracle> (0|=NAME) <datafile> ...` - 66 inputs in total. The labels below are the oracle's; the
expectation in each note is the C reading of §2. Two probe-authoring errors (a missing `cache`
argument and E4's child offset) were corrected before any label was used, and one label was **not**
predicted by the author: F1's empty type (the oracle answers an empty type with `uncertain 0`),
which is recorded as measured, not derived. Probes F3 and G4 were added after R96MCritic F9 named the
same rules, and reproduce its labels.

| probe | fixture state | name | data (hex) | oracle type | uncertain |
|---|---|---|---|---|---|
| A1-gate-ok | well-formed magic answers | `-` | `4849` | `application/x-a` | 0 |
| A2-gate-bad-nl | header ends \0\r not \0\n | `-` | `4849` | `text/plain` | 0 |
| A3-gate-short | 11-byte header | `-` | `4849` | `text/plain` | 0 |
| A4-gate-prefix | header + trailing 'X' inside the 12 bytes | `-` | `4849` | `text/plain` | 0 |
| B1-bad-line-mid | bad line mid-section; good section after | `-` | `4849` | `application/x-good` | 0 |
| B2-bad-header | priority is not a number | `-` | `4849` | `application/x-good` | 0 |
| B3-bad-char-after-value | trailing '!' where newline expected | `-` | `4849` | `application/x-good` | 0 |
| B4-type-unterminated | no ']' on the header line | `-` | `4849` | `application/x-good` | 0 |
| B5-extra-chars-two-sections | second section alone bad -> dropped; third good | `-` | `4849` | `application/x-good` | 0 |
| C1-prio-0 | priority 0 answers in text mode | `-` | `4849` | `application/x-zero` | 0 |
| C2-prio-order | 30 listed before 90, both match | `-` | `4849` | `application/x-high` | 0 |
| C3-prio-tie | equal priorities keep file order | `-` | `4849` | `application/x-first` | 0 |
| C4-prio-tie-dirs | equal priorities across dirs: XDG_DATA_HOME before XDG_DATA_DIRS | `-` | `4849` | `application/x-dh` | 0 |
| C5-prio-overflow | priority > INT_MAX is a parse error | `-` | `4849` | `application/x-good` | 0 |
| C6-indent-overflow | indent > INT_MAX is a parse error | `-` | `4849` | `application/x-good` | 0 |
| D1-range-start | offset 2, range 3, hit at 2 | `-` | `2e2e524742` | `application/x-range` | 0 |
| D2-range-late | hit at offset 3 of the range | `-` | `2e2e2e5247` | `application/x-range` | 0 |
| D3-range-none | no hit inside the range | `-` | `2e2e2e5258` | `text/plain` | 0 |
| D4-range-zero | +0 never enters the loop | `-` | `4849` | `text/plain` | 0 |
| D5-short-value | value longer than data is FALSE, not continue | `-` | `414243` | `text/plain` | 0 |
| D6-short-later-offset | same value 200 bytes in on a short buffer | `-` | `4849` | `text/plain` | 0 |
| D7-mask | masked compare | `-` | `1f99` | `application/x-mask` | 0 |
| D8-mask-fail | masked compare fails on the low nibble | `-` | `2f99` | `text/plain` | 0 |
| D9-word2-swapped | ~2 swaps the value at parse (LE) | `-` | `01000200` | `application/x-w2` | 0 |
| D9-word2-swapped | ~2 swaps the value at parse (LE) | `-` | `00010002` | `application/octet-stream` | 1 |
| D10-word4-swapped | ~4 swaps each 4-byte group | `-` | `01000000` | `application/x-w4` | 0 |
| D10-word4-swapped | ~4 swaps each 4-byte group | `-` | `00000001` | `application/octet-stream` | 1 |
| D11-word0 | ~0 is accepted and behaves as 1 | `-` | `4849` | `application/x-w0` | 0 |
| D12-word3 | ~3 is a parse error -> section dropped | `-` | `4849` | `application/x-good` | 0 |
| D13-word-len-mismatch | 3 bytes with ~2 -> parse error | `-` | `4849` | `text/plain` | 0 |
| D14-word-empty | bare '~' -> word_size -1 -> parse error | `-` | `4849` | `application/x-good` | 0 |
| D15-zero-length-value | zero-length value matches any non-empty data | `-` | `5a` | `application/x-emptyv` | 0 |
| E1-nest-hit | child holds | `-` | `4e452e2e59` | `application/x-nest` | 0 |
| E2-nest-miss | child fails -> section fails | `-` | `4e452e2e5a` | `text/plain` | 0 |
| E3-nest-skip-child | parent fails, child skipped, next top-level tested | `-` | `5a5a` | `application/x-two` | 0 |
| E3-nest-skip-child | parent fails, child skipped, next top-level tested | `-` | `58582e2e59` | `text/plain` | 0 |
| E4-nest-two-children | either child holds | `-` | `4e452e42` | `application/x-or` | 0 |
| E4-nest-two-children | either child holds | `-` | `4e452e43` | `text/plain` | 0 |
| E5-nest-deep | indent 2 chain | `-` | `414243` | `application/x-deep` | 0 |
| E5-nest-deep | indent 2 chain | `-` | `414258` | `text/plain` | 0 |
| E6-indent-jump | indent 0 then indent 2: no child at indent 1, section never matches | `-` | `4142` | `text/plain` | 0 |
| E7-first-child | a section whose first matchlet is at indent 1 never matches | `-` | `41` | `text/plain` | 0 |
| B6-type-nul | NUL before ']' in the header line | `-` | `4849` | `application/x-good` | 0 |
| F1-empty-type | empty type accepted | `-` | `4849` | `(empty)` | 0 |
| F2-type-space | type keeps a space and a slash | `-` | `4849` | `application/x a` | 0 |
| G1-invalid-cache | 40 zero bytes as mime.cache is invalid -> text mode | `-` | `4849` | `application/x-a` | 0 |
| D16-exact-length | i + value_length == len still matches | `-` | `4849` | `application/x-exact` | 0 |
| D17-blank-line | a bare newline inside a section is skipped | `-` | `4849` | `application/x-two` | 0 |
| D18-indent-non-gt | indent digits not followed by '>' | `-` | `4849` | `application/x-good` | 0 |
| D19-vt | VT (0x0b) in the first 128 bytes is binary | `-` | `61620b6364` | `application/octet-stream` | 1 |
| F3-junk-after-bracket | bytes after ']' on the header line are ignored | `-` | `4849` | `application/x-a` | 0 |
| G4-eof-no-newline | EOF after a complete value, no final newline: section inert | `-` | `4142` | `text/plain` | 0 |
| G2-no-magic | no magic file at all -> fallback | `-` | `4849` | `text/plain` | 0 |
| G3-eof-in-value | EOF inside a value: section inert | `-` | `4142` | `text/plain` | 0 |
| H1-name-one | one name type short-circuits the bytes | `'x.one'` | `0102` | `text/x-one` | 0 |
| H2-name-none | no name type -> the magic answer | `-` | `4849` | `application/x-hi` | 0 |
| H2-name-none | no name type -> the magic answer | `'zz.nomatch'` | `4849` | `application/x-hi` | 0 |
| H3-name-two-hi | two name types, magic 90 -> the sniffed type | `'x.two'` | `4849` | `application/x-hi` | 0 |
| H4-name-two-low | two name types, magic 50 -> first name type, uncertain | `'x.two'` | `4849` | `image/png` | 1 |
| H5-name-two-sub | two name types, sniffed text/plain -> first subclass name type | `'x.two'` | `4849` | `text/x-a` | 0 |
| H6-desktop-name | sniffed desktop with any name -> text/plain | `-` | `5b4465736b746f7020456e7472795d` | `application/x-desktop` | 0 |
| H6-desktop-name | sniffed desktop with any name -> text/plain | `'zz.nomatch'` | `5b4465736b746f7020456e7472795d` | `text/plain` | 0 |
| H7-dir | trailing slash before the bytes | `'d/'` | `4849` | `inode/directory` | 1 |
| H8-empty-data | len 0 answers zerosize before the magic | `-` | `(empty)` | `application/x-zerosize` | 0 |
| H8-empty-data | len 0 answers zerosize before the magic | `'x.one'` | `(empty)` | `text/x-one` | 0 |
| H9-prio0-name-one | priority 0 magic vs one name type: the name wins | `'x.one'` | `4849` | `text/x-one` | 0 |

### 7.2 The host's text magic database

Read-only parse of `/usr/share/mime/magic` by `R96MScribeEntry-hostdb.py` (stdlib; the file is
opened read-only; the parse implements the §2 state machine, reports 0 errors, and its 689
sections match the round-95 cache's 689 magic entries). Facts:

- `path /usr/share/mime/magic bytes 47524 sha256 2942f4adfca98c1816177f056d566e925e96e1c3dd562964dada066bf4a8a35c`
- `header_ok True`
- `sections 689 errors 0`
- `matchlets 1743`
- `priorities 5:3 10:34 20:1 30:3 40:19 45:3 50:452 51:1 55:1 60:78 62:1 65:3 70:38 75:9 80:35 90:8`
- `sections_at_ge80 43`
- `sections_at_0 0`
- `word_sizes 1:1733 2:4 4:6`
- `masked 43 range_gt1 259 max_range 18722`
- `indents 0:1282 1:335 2:98 3:14 4:14 max_indent 4`
- `max_extent 18730`
- `distinct_types 655`
- `types_listed_more_than_once 27`
- `longest_type_bytes 56`

The 689 sections equal the 689 magic entries the round-95 entry measured in
`/usr/share/mime/mime.cache`, and the 1282 indent-0 matchlets equal its 1282 matchlet total; the
461 deeper matchlets are the cache's `n_children` records, which the cache entry header does not
count (r95 §2.3.1). The text file's four `word_size` 2 and six `word_size` 4 matchlets are the
cache's 4 + 4 top-level ones plus two deeper ones. The parse found **0** errors: nothing on this
host exercises the section-drop rule, which is why the frozen cases must synthesise it (B1-B6).

### 7.3 The host leg (oracle only, measured by R96MExecHostC1)

The round-96 host seat ran the round-95 oracle over the committed host list
(`.ufo/waves/round-95/controls/mimesniff-host-files-r95.txt`, sha256
`9d5947a70d112796f39c3e309c5a25e5ff333b5ebeb51867ebe748af1135ba87`, 4911 paths) against a
cache-free copy of the host's eight text files (211254 B; `mime.cache` excluded), in both name
modes (`env -i LC_ALL=C HOME=<empty> XDG_DATA_HOME=<empty> XDG_DATA_DIRS=<copy>`, two legs per
path: `=basename` and `0`). Measured: **4911/4911 rows, 0 read or oracle errors**; the name leg
answers 78 distinct labels and the NULL leg 62; the top labels are `text/x-lua` 421,
`application/gzip` 367, `application/x-executable` 359, `application/x-sharedlib` 350,
`application/xml` 337, `application/octet-stream 1` 242, `image/svg+xml` 235, `text/x-python` 197.
Uncertain rows exist in real data: 242 name-leg and 276 null-leg rows answer
`application/octet-stream 1`, 23 answer `text/x-python 1` and 2 `application/x-perl 1`. The full
per-label histogram is `.ufo/waves/round-96/receipts/host-leg-r96.txt` §2 (result TSV sha256
`1507a4abbdfd2f75bfcec3935050ddfa30fd8fe49876cf9b3e40f9ba5c1cbec1`; the TSV itself lived in
scratch and is deleted). These are oracle labels for the text database, not the candidate's
answers; the candidate's host leg is the `9822 pairs (4911 paths x 2 legs: own path and data-only)` cell below.

### 7.4 The frozen measurement (L1)

| leg | expected | measured |
|---|---|---|
| frozen cases | `correct == cases` | `265` |
| per-class census | 16 declared classes, >= 8 cases each | `16 classes, 14-25 cases each (284 cases, 423 inputs)` |
| fresh seeded inputs | `fresh == fresh_total`, >= 120 | `40 cases, 289-319 inputs per seed, all correct` |
| host files | `host == host_total`, >= 1500 | `9822 pairs (4911 paths x 2 legs: own path and data-only)` |
| frozen mutants | `killed == mutants`, every class kills >= 1 | `97` |
| controls | do-nothing 0, naive < cases, memoriser 0 fresh, forgery rejected | `do-nothing 0/259 text-mode (20/20 none-mode answered), name-only 32/284, naive 101/284, base 0, memoriser fresh 0/40, forgery rejected (`audit_denials=5`)` |
| selftest | `checks=N failed=0`, N >= 18 | ``checks=50 failed=0`` |
| tool pin | `tool_pin=ok` at the measured rev | ``tool_pin=ok` at the measured rev` |

Every cell above is a placeholder for `.ufo/waves/round-96/receipts/c1-measured-r96.txt`; the seat
report lists them as the cells the scribe did not have at draft time.

## 8. Located quotes for the registry rows

The rows are `S524` (`xdgmimemagic.c`), `S525` (spec §2.5) in `corpus/SOURCES.md`, with the held
rows S505/S520/S521/S522 re-scoped to the text mode; the registry draft is
`.ufo/waves/round-96/w1/registry-rows-draft-r96.md`. Every quote below was extracted mechanically
from the fetched bytes by `R96MScribeEntry-quotes.py` (line range -> whitespace-collapsed text) and
is <= 25 words; the file digests are printed by that script.

| rule | row | anchor | quote (<= 25 words) |
|---|---|---|---|
| text magic file: 12 bytes read | S524 | xdgmimemagic.c:812 | `if (fread (header, 1, 12, magic_file) == 12)` |
| text magic file: the MIME-Magic gate | S524 | xdgmimemagic.c:814 | `if (memcmp ("MIME-Magic\0\n", header, 12) == 0)` |
| unreadable magic file contributes nothing | S524 | xdgmimemagic.c:809 | `magic_file = fopen (file_name, "r"); if (magic_file == NULL) return;` |
| section header starts with '[' | S524 | xdgmimemagic.c:244 | `if (c != '[') return XDG_MIME_MAGIC_ERROR;` |
| section priority read | S524 | xdgmimemagic.c:247 | `match->priority = _xdg_mime_magic_read_a_number (magic_file, &end_of_file);` |
| ':' after the priority | S524 | xdgmimemagic.c:256 | `if (c != ':') return XDG_MIME_MAGIC_ERROR;` |
| type runs to ']' | S524 | xdgmimemagic.c:267 | `while (*end_ptr != ']' && *end_ptr != '\000' && *end_ptr != '\n') end_ptr++;` |
| missing ']' is an error | S524 | xdgmimemagic.c:269 | `if (*end_ptr != ']') { free (buffer); return XDG_MIME_MAGIC_ERROR; }` |
| digit reader: first non-digit ends | S524 | xdgmimemagic.c:204 | `if (! isdigit (c)) { ungetc (c, magic_file); break; }` |
| digit reader: 30-digit cap | S524 | xdgmimemagic.c:211 | `if (pos == MAX_NUMBER_SIZE) break;` |
| digit reader: int range | S524 | xdgmimemagic.c:220 | `if ((retval < INT_MIN) || (retval > INT_MAX) || (errno != 0))` |
| type reader stops at NUL or newline | S524 | xdgmimemagic.c:168 | `if (c == '\n' || c == '\000')` |
| parse_error skips to the newline, back to SECTION | S524 | xdgmimemagic.c:292 | `if (c == '\n') return XDG_MIME_MAGIC_SECTION;` |
| matchlet defaults: indent 0, offset 0 | S524 | xdgmimemagic.c:93 | `matchlet->indent = 0; matchlet->offset = 0;` |
| matchlet defaults: range 1, word 1 | S524 | xdgmimemagic.c:98 | `matchlet->range_length = 1; matchlet->word_size = 1;` |
| matchlet offset read | S524 | xdgmimemagic.c:350 | `matchlet->offset = _xdg_mime_magic_read_a_number (magic_file, &end_of_file);` |
| matchlet '=' required | S524 | xdgmimemagic.c:367 | `else if (c != '=') { _xdg_mime_magic_matchlet_free (matchlet); return XDG_MIME_MAGIC_ERROR; }` |
| value length is big-endian | S524 | xdgmimemagic.c:382 | `matchlet->value_length = matchlet->value_length << 8;` |
| optional '&' mask introducer | S524 | xdgmimemagic.c:411 | `c = getc_unlocked (magic_file); if (c == '&')` |
| mask read: exactly value_length bytes | S524 | xdgmimemagic.c:420 | `bytes_read = fread (matchlet->mask, 1, matchlet->value_length, magic_file); if (bytes_read != (size_t) matchlet->value_length)` |
| word size accepts 0, 1, 2, 4 | S524 | xdgmimemagic.c:440 | `if (matchlet->word_size != 0 && matchlet->word_size != 1 && matchlet->word_size != 2 && matchlet->word_size != 4)` |
| word > 1 requires length divisible | S524 | xdgmimemagic.c:476 | `if (matchlet->value_length % matchlet->word_size != 0) { _xdg_mime_magic_matchlet_free (matchlet); return XDG_MIME_MAGIC_ERROR; }` |
| little-endian swap of the value at parse | S524 | xdgmimemagic.c:486 | `*((xdg_uint16_t *) (matchlet->value + i)) = SWAP_BE16_TO_LE16 (*((xdg_uint16_t *) (matchlet->value + i)));` |
| optional '+' range | S524 | xdgmimemagic.c:453 | `if (c == '+') { matchlet->range_length = _xdg_mime_magic_read_a_number (magic_file, &end_of_file);` |
| line must end in newline; swap then | S524 | xdgmimemagic.c:471 | `if (c == '\n') { /* We clean up the matchlet, byte swapping if needed */ if (matchlet->word_size > 1)` |
| matchlets prepended while parsing | S524 | xdgmimemagic.c:501 | `matchlet->next = match->matchlet; match->matchlet = matchlet;` |
| mirror and insert the section | S524 | xdgmimemagic.c:777 | `match->matchlet = _xdg_mime_magic_matchlet_mirror (match->matchlet); _xdg_mime_magic_insert_match (mime_magic, match);` |
| section freed on ERROR or EOF | S524 | xdgmimemagic.c:780 | `else if (state == XDG_MIME_MAGIC_EOF || state == XDG_MIME_MAGIC_ERROR) _xdg_mime_magic_match_free (match);` |
| higher priority inserted at the head | S524 | xdgmimemagic.c:608 | `if (match->priority > mime_magic->match_list->priority)` |
| equal priority inserted after equals | S524 | xdgmimemagic.c:618 | `if (list->next->priority < match->priority)` |
| first holding section wins | S524 | xdgmimemagic.c:668 | `for (match = mime_magic->match_list; match; match = match->next) { if (_xdg_mime_magic_match_compare_to_data (match, data, len)) { prio = match->priority; mime_type = match->mime_type; break; }` |
| no holding section: NULL | S524 | xdgmimemagic.c:685 | `if (mime_type == NULL) { for (n = 0; n < n_mime_types; n++) { if (mime_types[n]) mime_type = mime_types[n]; } }` |
| range loop bounds | S524 | xdgmimemagic.c:521 | `for (i = matchlet->offset; i < matchlet->offset + matchlet->range_length; i++)` |
| short buffer: FALSE for the matchlet | S524 | xdgmimemagic.c:525 | `if (i + matchlet->value_length > len) return FALSE;` |
| masked compare | S524 | xdgmimemagic.c:532 | `if ((matchlet->value[j] & matchlet->mask[j]) != ((((unsigned char *) data)[j + i]) & matchlet->mask[j]))` |
| raw compare | S524 | xdgmimemagic.c:544 | `for (j = 0; j < matchlet->value_length; j++) { if (matchlet->value[j] != ((unsigned char *) data)[j + i])` |
| first holding offset wins | S524 | xdgmimemagic.c:551 | `if (valid_matchlet) return TRUE;` |
| only the current indent is a candidate | S524 | xdgmimemagic.c:563 | `while ((matchlet != NULL) && (matchlet->indent == indent))` |
| child recursion at indent+1 | S524 | xdgmimemagic.c:571 | `if ((matchlet->next == NULL) || (matchlet->next->indent <= indent)) return TRUE; if (_xdg_mime_magic_matchlet_compare_level (matchlet->next, data, len, indent + 1)) return TRUE;` |
| failed chain skips the deeper subtree | S524 | xdgmimemagic.c:582 | `do { matchlet = matchlet->next; } while (matchlet && matchlet->indent > indent);` |
| matchlet extent sum | S524 | xdgmimemagic.c:714 | `extent = matchlet->value_length + matchlet->offset + matchlet->range_length;` |
| max extent returned | S524 | xdgmimemagic.c:648 | `int _xdg_mime_magic_get_buffer_extents (XdgMimeMagic *mime_magic) { return mime_magic->max_extent;` |
| text or cache data path | S505 | xdgmime.c:532 | `xdg_mime_init (); if (_caches) mime_type = _xdg_mime_cache_get_mime_type_for_data (data, len, result_prio); else mime_type = _xdg_mime_magic_lookup_data (global_magic, data, len, result_prio, NULL, 0);` |
| text magic lookup call | S505 | xdgmime.c:535 | `mime_type = _xdg_mime_magic_lookup_data (global_magic, data, len, result_prio, NULL, 0);` |
| empty data answers zerosize first | S505 | xdgmime.c:523 | `if (len == 0) { if (result_prio != NULL) *result_prio = 100; return XDG_MIME_TYPE_EMPTY;` |
| fallback when no section holds | S505 | xdgmime.c:540 | `return _xdg_binary_or_text_fallback(data, len);` |
| dir list env and default XDG_DATA_DIRS | S505 | xdgmime.c:231 | `xdg_data_home = getenv ("XDG_DATA_HOME"); home = getenv ("HOME"); xdg_data_dirs = getenv ("XDG_DATA_DIRS"); if (xdg_data_dirs == NULL) xdg_data_dirs = "/usr/local/share/:/usr/share/";` |
| HOME/.local/share/mime when XDG_DATA_HOME is unset | S505 | xdgmime.c:255 | `else if (home != NULL)` |
| per-directory magic file read | S505 | xdgmime.c:184 | `_xdg_mime_magic_read_from_file (global_magic, file_name);` |
| text name types from the glob hash | S505 | xdgmime.c:648 | `return _xdg_glob_hash_lookup_file_name (global_hash, file_name, mime_types, n_mime_types);` |
| cache mode dispatches the cache subclass walk | S505 | xdgmime.c:830 | `if (_caches) return _xdg_mime_cache_mime_type_subclass (mime, base, NULL);` |
| text unalias through the text alias list | S505 | xdgmime.c:833 | `umime = _xdg_mime_unalias_mime_type (mime); ubase = _xdg_mime_unalias_mime_type (base);` |
| super type rule | S505 | xdgmime.c:841 | `if (xdg_mime_is_super_type (ubase) && xdg_mime_media_type_equal (umime, ubase))` |
| text/plain rule | S505 | xdgmime.c:847 | `if (strcmp (ubase, "text/plain") == 0 && strncmp (umime, "text/", 5) == 0)` |
| application/octet-stream rule | S505 | xdgmime.c:851 | `if (strcmp (ubase, "application/octet-stream") == 0 && strncmp (umime, "inode/", 6) != 0)` |
| parents from the text subclasses list | S505 | xdgmime.c:861 | `parents = _xdg_mime_parent_list_lookup (parent_list, umime);` |
| trailing slash answers inode/directory | S521 | gcontenttype-fdo.c:597 | `if (i > 0 && filename[i - 1] == '/') {` |
| basename for the name step | S521 | gcontenttype-fdo.c:607 | `basename = g_path_get_basename (filename);` |
| one name type short-circuits | S521 | gcontenttype-fdo.c:614 | `if (n_name_mimetypes == 1)` |
| data is only used if given | S521 | gcontenttype-fdo.c:622 | `if (data)` |
| the data function call | S521 | gcontenttype-fdo.c:624 | `sniffed_mimetype = xdg_mime_get_mime_type_for_data (data, data_size, &sniffed_prio);` |
| sentinel plus looks_like_text | S521 | gcontenttype-fdo.c:625 | `if (sniffed_mimetype == XDG_MIME_TYPE_UNKNOWN &&` |
| desktop rewrite with a filename | S521 | gcontenttype-fdo.c:637 | `if (filename != NULL && strcmp (sniffed_mimetype, "application/x-desktop") == 0) sniffed_mimetype = "text/plain";` |
| zero name types use the sniffed type | S521 | gcontenttype-fdo.c:641 | `if (n_name_mimetypes == 0)` |
| priority >= 80 wins outright | S521 | gcontenttype-fdo.c:654 | `if (sniffed_prio >= 80) /* High priority sniffing match, use that */` |
| first subclass name type | S521 | gcontenttype-fdo.c:663 | `if ( xdg_mime_mime_type_subclass (name_mimetypes[i], sniffed_mimetype))` |
| first name type when nothing helps | S521 | gcontenttype-fdo.c:680 | `mimetype = g_strdup (name_mimetypes[0]);` |
| uncertain flag on the first of several | S521 | gcontenttype-fdo.c:682 | `*result_uncertain = TRUE;` |
| data_size -1 refused | S521 | gcontenttype-fdo.c:589 | `g_return_val_if_fail (data_size != (gsize) -1, g_strdup (XDG_MIME_TYPE_UNKNOWN));` |
| fallback: control byte in the first 128 bytes | S520 | xdgmimeint.c:185 | `if (chardata[i] < 32 && chardata[i] != 9 && chardata[i] != 10 && chardata[i] != 13) return XDG_MIME_TYPE_UNKNOWN; /* binary data */` |
| fallback: otherwise text/plain | S520 | xdgmimeint.c:189 | `return XDG_MIME_TYPE_TEXTPLAIN;` |
| spec: the file's magic string | S525 | smi2-s02.html:387 | `The file starts with the magic string "MIME-Magic\0\n".` |
| spec: all numbers big-endian | S525 | smi2-s02.html:391 | `All numbers are big-endian, so need to be byte-swapped on little-endian machines.` |
| spec: section form; higher priority first | S525 | smi2-s02.html:394 | `Each section is introduced by giving the priority and type in brackets, followed by a newline character. Higher priority entries come first. Example:` |
| spec: two-byte big-endian value length | S525 | smi2-s02.html:403 | `Two bytes giving the (big-endian) length of the value, followed by the value itself.` |
| spec: mask length equals value length | S525 | smi2-s02.html:405 | `The mask, which (if present) is exactly the same length as the value.` |
| spec: word size byte-swaps | S525 | smi2-s02.html:415 | `The word size is used for byte-swapping.` |
| spec: optional components | S525 | smi2-s02.html:421 | `The indent, range-length, word-size and mask components are optional.` |
| spec: defaults | S525 | smi2-s02.html:422 | `indent defaults to 0, range-length to 1, the word-size to 1, and the mask to all 'one' bits.` |
| spec: parent is the preceding indent-1 entry | S525 | smi2-s02.html:426 | `The parent of an entry is the preceding entry with an indent one less than the entry.` |
| spec: only the bad line is ignored | S525 | smi2-s02.html:429 | `If an unknown character is found where a newline is expected then the whole line should be ignored` |
| spec: magic-deleteall marker | S525 | smi2-s02.html:443 | `The magic-deleteall attribute, which means that implementations SHOULD discard information from previous directories` |

## 9. Frozen cases and pins (the case set this entry is answered by)

The frozen case file is JSON `{"version":2,"db_mode":"text|none",...}` with one case per
environment; each case holds a `{root}/h` HOME, a `{root}/dh` XDG_DATA_HOME or null, a
`{root}/d1:{root}/d2` XDG_DATA_DIRS (never null: unset reaches the host databases), the case's
`mime` files and 1..12 inputs with one oracle label each. The 16 classes are `header`, `sect`,
`value`, `mask`, `word`, `range`, `indent`, `order`, `drop`, `multi`, `glob`, `alias`, `fallback`,
`zerosize`, `mode`, `desktop`; >= 8 cases per class and >= 260 cases total. A `text` case holds at
least one `mime/magic` and no `mime.cache`; a `none` case holds no `mime/` file; a case holding a LOADABLE
`mime.cache` (regular file, >= 40 bytes, version 1.1 or 1.2 at bytes 4..7) is a cache-mode refusal case labelled
`["UNSUPPORTED", null]`; a cache that does not load leaves the directory in text mode. The host leg is answered
against a **cache-free copy** of the host's eight text files (the recipe in
`.ufo/waves/round-96/receipts/host-leg-r96.txt` §1): pointing a run at `/usr/share/mime` alone
reaches the host's `mime.cache` and the tool answers exit 3 (R96MCritic F1), so the counter must
build the text root and should print its construction (`host_root=text files=8`) in the verdict.

| artifact | path | sha256 | state |
|---|---|---|---|
| candidate | `tools/mado-mimetext.py` | `d5f174fc33d0b1f1847897a8e63724c7112137c1bf58a89508d1c1c13b857cbd` | frozen at the C1 commit |
| sibling | `tools/mado-mimeglob.py` | `65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453` (round 94, unchanged; the name step) | pinned in the run |
| oracle | `.ufo/waves/round-95/controls/mimesniff-oracle-r95.c` | `99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a` | reused unchanged |
| frozen cases | `.ufo/waves/round-96/controls/magictext-cases-r96-frozen.json` | `42ce9fc68458955e9e93c405cdbeb59f649b36d94e100240894d660391d1bed6` | |
| frozen mutants | `.ufo/waves/round-96/controls/magictext-mutants-r96-frozen.json` | `d57d678f85320bb1a3b7069982743dfcf606fab72f79d9f769f6a5bf8b3dad80` | |
| fresh generator | `.ufo/waves/round-96/controls/magictext-fresh-r96.py` | `32d38edfb2cff57de3d89297ffaf1bd781d730b7be502fbfa62efa38de0815da` | |
| host file list | `.ufo/waves/round-95/controls/mimesniff-host-files-r95.txt` | `9d5947a70d112796f39c3e309c5a25e5ff333b5ebeb51867ebe748af1135ba87` (4911 paths) | reused unchanged |
| counter | `quality/counters/c1-r96-magictext.py` | `a2fe3b31ed54be0fe418eef62dc0d81c4b028fb557d61f63dfe4aa5293900347` | |
| dirs mode line | `MADO_MIMETEXT_DIRS: mode=text\|none dirs=...` | - | scored header |
| selftest checks | `checks=N failed=0` | - | N = 50 |

Rule -> case-class map (what the frozen set must exercise, from the rows above): the 12-byte gate
and the header errors -> `header`/`sect`; value length, EOF and the exact fit -> `value`; masks ->
`mask`; `~0/2/3/4` and the modulo rule -> `word`; `+0`, late hits, short-buffer FALSE -> `range`;
the indent tree, the jump and the orphan -> `indent`; priority order, ties, cross-directory ties
and priority 0 -> `order`; the bad-line whole-section drop -> `drop`; several matching sections and
several matchlets -> `multi`; the name-step arbitration -> `glob`; the text alias/parent walk ->
`alias`; the binary/text fallback and VT -> `fallback`; `len == 0` -> `zerosize`; text vs none vs
cache refusal -> `mode`; the desktop rewrite -> `desktop`.

## 10. Erratum (round 96, after the freeze)

The sentence in §9 that places the cache version "at bytes 4..7" is wrong; the version is at **offsets 0..3** —
`GET_UINT16(buffer, 0)` is the major and `GET_UINT16(buffer, 2)` the minor (`xdgmimecache.c` validity check, mirrored
by `tools/mado-mimeglob.py` `load_cache` and by this tool). Bytes 4..7 hold the flags and content count. The rule as
measured is: a cache loads only when the file is at least 40 bytes and the big-endian u16 at offset 0 is 1 with the
u16 at offset 2 in {1, 2}; the frozen case set's five refusal fixtures carry `0001 0001`/`0001 0002` headers at offset 0
(R96MExecCasesC1 measured; `R96MExecCounterC1`'s `loadable_cache` already uses offset 0, so no measurement moves).
This correction is append-only; the superseded sentence stays above.
