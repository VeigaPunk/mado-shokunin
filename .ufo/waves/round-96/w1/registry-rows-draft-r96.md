# Round-96 registry rows draft (SOURCES.md) — for `corpus/SOURCES.md`

Seat `R96MScribeEntry`, 2026-11-07. The L1 fills the ids and the final digests; this draft is the
row shape, the located quote map and the correction list against
`.ufo/waves/round-96/receipts/sources-open-r96.txt`. Every quote below was extracted mechanically
from the committed fetch bytes (`.ufo/waves/round-96/fetch/`) by
`.ufo/waves/round-96/w1/R96MScribeEntry-quotes.py` (line range -> whitespace-collapsed text, word
count, digest); none is hand-typed. All quotes are <= 25 words.

## 1. Row shape (11 columns, as the registry uses it)

`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`

### S524 — GLib 2.90.1 text magic database parser and matcher

Proposed cell text (one line):

```
| S524 | GLib 2.90.1 xdgmime text magic database parser and matcher — https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/xdgmime/xdgmimemagic.c (sha256 fcb1eafe748d3dc18f7f405d1078c8a32e313d23d2fab86b0f12e609ac2ce742, 18289 B, HTTP 200 at the recorded URL); host package glib2 2.90.1-1 | code | A | how GLib answers bytes from a TEXT mime/magic file (no loadable mime.cache): the 12-byte MIME-Magic gate, the [priority:type] header and its digit-only number reader, the matchlet line (indent, offset, two-byte big-endian length, value, mask, word size with the little-endian swap at parse time, range), the state machine's whole-section drop on a bad line, section order by priority with ties in file order and first match wins, the indent tree and its indent-jump blind spot, the compare's bounds rule, and the max extent | xdgmimemagic.c:806-819 (gate), 227-280 (header), 297-513 (matchlet), 283-295 and 748-798 (drop and insert), 596-628 (order), 652-698 (lookup), 557-586 (tree), 515-555 (compare), 700-721 (extent) | the text database is parsed by section: one bad line loses the whole section; a priority-0 section answers in text mode; ~0 is accepted; a child must be the next matchlet at indent+1 | mined | 2026-11-07 | 90d | corpus/knowledge/mime-textdb-magic-r96.md, corpus/lessons/round-96.md |
```

### S525 — shared-mime-info spec §2.5 (new scope on S523's locator)

Proposed cell text (one line):

```
| S525 | Shared MIME-info Database specification, version 0.21, section 2.5 "The magic files", at the locator S523 holds — https://specifications.freedesktop.org/shared-mime-info/latest/ar01s02.html (sha256 e00fa00e69b1e95ad8642d05fc5023c26f859bdaf8bdda3e091a55feb016c61e, 59208 B, HTTP 200; the same page as S523 under a new scope, census W04 expected) | spec | A | the documented contract for mime/magic: the MIME-Magic string, big-endian numbers, the section and line forms, the two-byte value length, the equal-length mask, word size and byte-swapping, the defaults, the parent rule, the unknown-character rule, and the magic-deleteall marker | ar01s02.html page lines 387 (magic string), 391 (big-endian), 394-395 (sections; higher priority first), 403 (two-byte length), 405 (mask), 415 (word size), 421-423 (optional components and defaults), 426-427 (parent), 429-430 (unknown character), 443-446 (__NOMAGIC__) | where GLib 2.90.1's text reader departs from the spec: whole-section drop instead of one line, re-sorting by priority, ~0 accepted, the next-matchlet-at-indent+1 parent, the empty type, and a live priority 0 | mined | 2026-11-07 | 90d | corpus/knowledge/mime-textdb-magic-r96.md, corpus/lessons/round-96.md |
```

Census effect: two new tier-A rows, 458 -> 460; S525 raises the expected W04 duplicate-url warning
(same URL as S523); S524 opens a file no held row names. Status `mined` (cited by the entry).

## 2. Held rows touched (old -> new used-by)

| row | file | old used-by | new used-by | why |
|---|---|---|---|---|
| S505 | xdgmime.c | `corpus/knowledge/mime-glob-guess-r94.md,corpus/knowledge/mime-magic-sniff-r95.md,corpus/lessons/round-95.md` | append `,corpus/knowledge/mime-textdb-magic-r96.md` | text/cache switch, per-directory text load, text data path, text subclass walk |
| S519 | xdgmimecache.c | `corpus/knowledge/mime-magic-sniff-r95.md,corpus/lessons/round-95.md` | append `,corpus/knowledge/mime-textdb-magic-r96.md` | cache-mode priority-0 contrast only (`:784`) |
| S520 | xdgmimeint.c | `corpus/knowledge/mime-magic-sniff-r95.md,corpus/lessons/round-95.md` | append `,corpus/knowledge/mime-textdb-magic-r96.md` | the binary/text fallback reached when no section holds |
| S521 | gcontenttype-fdo.c | `corpus/knowledge/mime-magic-sniff-r95.md,corpus/lessons/round-95.md` | append `,corpus/knowledge/mime-textdb-magic-r96.md` | the guess arbitration, looks_like_text, the desktop rewrite |
| S522 | glocalfileinfo.c | `corpus/knowledge/mime-magic-sniff-r95.md,corpus/lessons/round-95.md` | append `,corpus/knowledge/mime-textdb-magic-r96.md` | the 16 KiB sniff clamp vs the text DB's 18730-byte extent |
| S523 | ar01s02.html | `corpus/knowledge/mime-glob-guess-r94.md,corpus/knowledge/mime-magic-sniff-r95.md,corpus/lessons/round-95.md` | append `,corpus/knowledge/mime-textdb-magic-r96.md` | §2.12 cross-reference (the §2.5 scope is S525) |

Only `used-by` cells change; no anchor, digest or scope cell moves in a held row (CORPUS rule 2).
If the L1 folds S525's scope into S523 instead of opening a row, drop S525 above, move the §2.5
quotes to S523's row as a new scope block, and replace `S525` by `S523` in the entry (no line
moves; the entry's §8 table carries the page lines).

## 3. Corrections to the receipt's line map (found by mechanical extraction)

The quotes in `sources-open-r96.txt` are correct; these anchor/range cells were wrong at receipt
time and are fixed in the quote map below (the L1 confirmed the fixes in the 11:39Z message):

| receipt claim | correct | evidence |
|---|---|---|
| S524 memcmp quote at line 815 | 814 | `nl -ba` of the committed bytes |
| S524 mask read at 400-419 | 420 (the `&` branch opens at 410-411) | quote M20 |
| S524 word/length check at 421-450 | 476 | quote M22 |
| S524 word-size set "1\|2\|4 only" | 0, 1, 2, 4 | quote M21; probe D11 |
| S524 "section kept only if a matchlet parsed" | the section is inserted on `SECTION` or `EOF`-with-type even with zero matchlets; such a section can never match | `:772-778`; probe G3 |
| S525 two-byte length at 407-410 | 403 | quote P04 |
| S525 defaults at 429-433 | 421-423 | quotes P07, P08 |
| S525 parent at 435-439 | 426-427 | quote P09 |
| S525 unknown character at 441-446 | 429-430 | quote P10 |
| S525 `__NOMAGIC__` at 445-446 | 443-446 | quote P11 |
| counting command `--expect-oracle-sha256` 63 hex chars | `99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a` | `sha256sum` of the control file |

Also corrected in the entry: the text reader's parse error drops the section (the spec says the
line); the C accepts an empty type (`[90:]` -> `""` 0, probe F1); text mode has no `priority > 0`
gate (probe C1); an indent jump makes a section unmatchable (probes E6, E7).

## 4. Located quote map (all rows, mechanically extracted)

Columns: rule | row | anchor | quote. The anchor is exactly `file:line` and it is the line the
quote starts on; the row id sits in the second column, never in the third, so the unique-anchor rule
(QUALITY 107) is met by construction once the ids are filled.

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

## 5. Fetch provenance for the rows

- `sources-open-r96.txt` records two fetches per URL, both HTTP 200, identical digests:
  `xdgmimemagic.c` `fcb1eafe...ce742` (18289 B), `xdgmime.c` `afb1c1c1...82410` (23417 B),
  `ar01s02.html` `e00fa00e...c61e` (59208 B).
- The committed bytes are `.ufo/waves/round-96/fetch/{xdgmimemagic.c,xdgmime.c,smi-ar01s02.html}`;
  the scribe re-hashed them: 3/3 equal to the receipt (11:43Z).
- `ar01s03.html` was probed this round (HTTP 200, 7048 B) and holds no `MIME-Magic` text: a
  considered-and-rejected row (no separate scope; record the rejection in the lesson's Gate).
- The host package pins are part of the rows: glib2 2.90.1-1, shared-mime-info 2.5.1-2.
