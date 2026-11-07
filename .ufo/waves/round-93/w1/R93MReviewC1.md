# R93MReviewC1 — C1 candidate review: remaining GKeyFile byte classes

DRAFT evidence, pre-freeze. Nothing here is a measurement; no receipt was written. The candidate
`.ufo/waves/round-93/build/mado-portals.c1.py` (sha256 `89039e30d329bee82f20c4a32edc9fa72c02774c98364017e131a372c9fb91d3`,
= r92 `build/mado-portals.d1.py`) was reviewed against GLib 2.90.1 `gkeyfile.c`/`gstrfuncs.c`/`gutf8.c`
and labelled against the installed xdg-desktop-portal 1.22.1 (`/usr/lib/xdg-desktop-portal` sha256
`e1429fbe…3a4f8`). Base is `4c6f723f:tools/mado-portals.py` (the port diff is the ~40 lines in
`parse_keyfile`, `load_portal`, `load_config_file`, `_check_utf8`).

## Method

- Upstream fetched from the pinned URLs and hash-checked: `gkeyfile.c` `e1d1270f…ff656`, `gstrfuncs.c`
  `6ea1c433…62fd4`, `gstrfuncs.h` `298b0dc4…26e23`. `g_utf8_find_next_char` is **not** in the three pinned
  files; it lives in `gutf8.c`, fetched from the same tag, sha256 `8538bf7b60f28eb4037898f570e2bfc319e148af7b0c1df3db9c7eb6c2fa17a9`
  (unpinned by the source receipt — the L1 should add this pin if the rule is cited in the freeze).
- Ground truth was attributed at two levels: (i) the installed binary via the r90 oracle (labels), and
  (ii) a `g_key_file_load_from_data(data, len)` probe (`kfprobe.c`, gcc, glib2 2.90.1-1) on the same bytes
  printing groups/keys/values. Every finding below is reproduced by both.
- Oracle: `.ufo/waves/round-90/controls/portal-oracle-r90.py` copied to scratch with the r92/r93 byte-write
  fix only (`open(..., newline="", errors="surrogateescape")`; label dump `ensure_ascii=True` so surrogates
  survive json). 53/53 cases labelled, `incomplete=0`, `host_tail_sha256=4a4cf319…fbf9`; a second
  independent run produced a byte-identical label file (`labels.json` = `labels-r93rev.json`,
  sha256 `1379ab4d…62af`). `dir` mode only, desktop `XFCE` (one `KDE` case), 21 impl interfaces.
- Tools: the r90 counter's own `run_tool`/`case_correct` (bwrap `--unshare-all`, `--clearenv`, `LC_ALL=C`,
  `--json`), with its `materialise` monkeypatched to `write(..., errors="surrogateescape")`; candidate and base
  on the same 53 cases, jobs=4.

## Result

53 fixtures, oracle-labelled, DRAFT score: **candidate 41/53, base 37/53**. Candidate has **12 divergences,
all NUL-byte classes**; all 12 are shared with the base tool (base has 16 divergences: the same 12 plus 4
class-(a) cases the port fixes, see "Coverage" below). The candidate's `--selftest` prints
`MADO_PORTALS_SELFTEST: checks=22 failed=0`, rc 0.

## Finding F1 (high) — NUL is a C-string terminator in GKeyFile; the candidate treats it as an ordinary byte

`g_key_file_parse_line` and its helpers are C-string based. A line's content is truncated at the first
`\0` for comment/group/key-value detection (`g_key_file_line_is_comment` gkeyfile.c:4561-4563,
`g_key_file_line_is_group` 4647-4673, `g_key_file_line_is_key_value_pair` 4675-4684), key/value text is
cut at `\0` when stored (`pair->value = g_strndup (value_start, value_len)` gkeyfile.c:1796), and a line
whose first byte is NUL is a comment. The candidate converts bytes with
`decode("utf-8","surrogateescape")` (candidate:285, :361) and keeps every NUL as `"\x00"`; nothing in
`parse_keyfile` (candidate:116-168) or the readers truncates.

| fixture (round-90 schema, files written as bytes) | oracle (FC/Print/Settings/Screenshot) | candidate | base | candidate site | GLib rule |
|---|---|---|---|---|---|
| `r93-nul-config-value-tail` — portals.conf `[preferred]\ndefault=kde\x00junk\n` | kde/kde/kde/gtk | gtk | gtk | value kept verbatim at :150; list at :177-213 | value cut at NUL, gkeyfile.c:1796 → `["kde"]` |
| `r93-nul-config-group-trailer` — `[preferred]\x00junk\ndefault=kde\n` | kde/kde/kde/gtk | gtk | gtk | `_is_group_line` :89 sees `\x00junk`; :142-144 raises | line view ends at NUL; only `' '`/`'\t'` after `]`, gkeyfile.c:4663-4671 |
| `r93-nul-portal-group-trailer` — kde.portal first line `[portal]\x00junk` | kde/kde/kde/gtk | gtk | gtk | :89, :142-144, skip :311-313 | same |
| `r93-nul-portal-key-before-eq` — kde.portal `Foo\x00Bar=x` | gtk/gtk/gtk/gtk | kde | kde | accepts key `Foo\x00Bar`, :142-149 | `g_utf8_strchr` sees no `'='` before NUL → parse error voids the file, gkeyfile.c:4675-4684 |
| `r93-nul-portal-interfaces-tail` — `Interfaces=…Settings;\x00junk` | kde/kde/kde/gtk | gtk | gtk | :150 → extra piece fails :297-300 | value cut at NUL → 3 interfaces |
| `r93-nul-portal-dbusname-tail` — `DBusName=…desktop.kde\x00junk` | kde/kde/kde/gtk | gtk | gtk | :215-232 + bus-name check | value cut at NUL |
| `r93-nul-portal-usein-tail` — `UseIn=KDE\x00junk;`, desktop KDE | kde/kde/kde/gtk | gtk | gtk | :304-310 | value cut at NUL → `["KDE"]` |
| `r93-nul-own-line` — `\x00\n[preferred]\ndefault=kde\n` | kde/kde/kde/gtk | gtk | gtk | line `\x00` has no `=`, :142-144 | `*line=='\0'` is a comment, gkeyfile.c:4561-4563 |
| `r93-nul-eof` — `…default=kde\n\x00` (final fragment) | kde/kde/kde/gtk | gtk | gtk | same | final flush gkeyfile.c:1003 (flush fn 1899-1927), comment |
| `r93-nul-value-eof` — `…default=kde\x00` (no LF) | kde/kde/kde/gtk | gtk | gtk | :150 | value cut at NUL |
| `r93-nul-interfaces-mid` — `Interfaces=FileChooser;\x00Print;Settings;` | kde/gtk/gtk/gtk | gtk | gtk | :150 → :297-300 | value cut at NUL → only FileChooser |
| `r93-nul-group-trailer-space` — `[preferred]\x00 \ndefault=kde\n` | kde/kde/kde/gtk | gtk | gtk | :89 | after `]`: NUL, so the trailing space is irrelevant — group accepted |

Unit-level reproduction (candidate `parse_keyfile`):
`"[preferred]\ndefault=kde\x00junk\n"` → `{'default': 'kde\x00junk'}` (GLib probe: `kde`);
`"[preferred]\x00junk\ndefault=kde\n"` → `KeyFileError` (probe: load OK, `default=kde`);
`"[portal]\nFoo\x00Bar=x\n"` → key `Foo\x00Bar` (probe: `Invalid key line “Foo�Bar=x”` → whole file FAIL).

### F2 (high) — the recommended fix must keep two GLib length subtleties

1. **Encoding uses the untruncated value length.** `value_len = line + length - value_start`
   (gkeyfile.c:1760) counts bytes **through the end of the buffer**, including NUL and trailing junk;
   the check is `value_len != strlen("UTF-8") || g_ascii_strncasecmp(...)` (1771-1772). So
   `Encoding=UTF-8\x00x` and `Encoding=UTF-8\x00` void the file even though the NUL-terminated value is
   `UTF-8`. The candidate already matches (full Python segment at :151-156); fixtures
   `r93-encoding-nul-tail`, `r93-encoding-nul-exact` hold today (both gtk, oracle gtk) and a naive
   "truncate every value at NUL" patch would break them.
2. **Group names are re-scanned backwards over the whole buffer.** `g_key_file_parse_group` starts at
   `line + length - 1` and walks back to the last `]` (gkeyfile.c:1687-1696), then `g_strndup` cuts at
   the first NUL. So `[preferred]\x00]` becomes the name `preferred]` → invalid group → file void
   (probe: `Invalid group name: preferred]`; oracle gtk), whereas a naive "truncate the line at NUL, then
   parse" accepts `[preferred]`. Fixture `r93-nul-group-trailer-bracket` holds today (both gtk, oracle gtk)
   and should stay in the frozen set as a guard.

A faithful minimal patch: after the CR-before-LF erase, take the line view `raw.split("\x00",1)[0]`,
leading-strip that view, and drive comment/group/key-value detection and key/value extraction from the
view; keep the Encoding check on the raw segment after `=`; for a group line additionally reproduce the
backwards `]` scan (or leave `_is_group_line` failing when a `]` occurs after the NUL). Value truncation
then flows automatically into `string_list`/`plain_string`/`is_bus_name`/`_by_list`.

### F3 (medium) — precedence: pre-existing gap, not a port regression

All 12 F1 cases fail identically on the base tool, so the port neither introduced nor hid them. But they
are byte-class edges on exactly C1's surface (a `.portal`/`portals.conf` byte sequence that changes the
backend xdp picks), and the sibling case set (`.ufo/waves/round-93/controls/portal-cases-r93.json`, 300
cases) contains **0 fixtures with a NUL byte in any file**. If these 12 are folded into the frozen
byte-class set unpatched, `PRED-C1-r93-v1`'s "answers every frozen case" conjunct is false for the
candidate as measured. Recommendation: patch the candidate (F2) and fold all 53.

## Coverage cases the frozen set should keep (base wrong, candidate right)

| fixture | bytes | oracle | base | rule |
|---|---|---|---|---|
| `r93-encoding-later-group2` | `[first]\nx=1\n[other]\nEncoding=caf\xe9\n[preferred]\ndefault=kde` | kde | gtk | Encoding is only checked in the *first* group (gkeyfile.c:1766); the byte is unread → file loads |
| `r93-key-name-byte-e9` | kde.portal extra `Foo\xe9=bar` | kde | gtk | main key body accepts raw bytes 0x80-0xFF (no UTF-8 validation), gkeyfile.c:4584-4614 |
| `r93-group-name-byte-e9` | portals.conf `[\xe9]` before `[preferred]` | kde | gtk | group names reject only `[`/`]` and ASCII control on char starts, gkeyfile.c:4567-4578 |
| `r93-group-header-invalid-e9` | kde.portal second group `[\xe9]` | kde | gtk | same; an unread group with invalid UTF-8 loads |

These extend r92's 16 by one representative per name class; the base fails them only because its strict
`open(..., encoding="utf-8")` voids the whole file, which is the class-(a) defect the port fixes.

## Classes that hold (candidate = oracle; frozen-set pins)

Of the candidate's 41 correct cases, 4 are coverage wins where base is wrong (table above); the other 37
agree with base as well. All are listed here with their oracle outcome.

- **NUL holds (8):** `r93-nul-config-line-start` (NUL glued to `[preferred]`: line view empty → group lost
  → following key errors → both void, gtk), `r93-nul-config-empty-value` (`default=\x00kde` → both gtk),
  `r93-nul-portal-line-start` (gtk), `r93-nul-comment-inner` (`# co\x00mment` → kde),
  `r93-nul-unread-key-value` (`foo=bar\x00junk` → kde), `r93-nul-group-name-inner`
  (`[pref\x00erred]` → gtk), `r93-nul-group-trailer-bracket` (`[preferred]\x00]` → gtk, F2 guard),
  `r93-nul-only-config` (`\x00\n` → gtk).
- **CR / CRLF (5):** `r93-crlf-config` (kde), `r93-crlf-group-trailing-space` (kde), `r93-cr-only-config`
  (gtk), `r93-last-line-cr` (gtk), `r93-crlf-double-cr` (gtk). GLib erases exactly one `\r` immediately
  before `\n` (gkeyfile.c:1858-1862) and flushes the final fragment at EOF (load_from_data, gkeyfile.c:1003); a lone `\r` is
  only whitespace for line-leading/`=`-adjacent positioning — it never separates lines. A final `\r`
  survives into the value (`kde\r`) and matches no backend.
- **BOM (3):** `r93-bom-config` (gtk), `r93-bom-key-line` (gtk), `r93-bom-mid-file` (gtk). No BOM stripping;
  U+FEFF is neither whitespace nor a group/comment opener → parse error → file void.
- **Group-line trailing bytes / leading whitespace (3):** `r93-group-trailing-space-tab` (kde),
  `r93-group-trailing-vt` (gtk), `r93-group-leading-formfeed` (kde). Only `' '`/`'\t'` are skipped after
  `]` (gkeyfile.c:4663-4671); VT is not `g_ascii_isspace` (ascii table gstrfuncs.c:262-282,
  `g_ascii_isspace` gstrfuncs.h:85-86 — 0x0B has `G_ASCII_CNTRL` only) and \f is.
- **Escapes (6):** `r93-escape-s-space` (kde), `r93-escape-semicolon` (gtk), `r93-escape-tab-backslash`
  (kde), `r93-escape-s-next-to-vt` (kde), `r93-escape-invalid-backslash-v` (gtk),
  `r93-escape-trailing-backslash` (gtk). Escape set `s n t r \\ ;` plus `\;` only meaningful when a list
  separator exists; `\v` and a trailing `\` are INVALID_VALUE (gkeyfile.c:4710-4776), and a list keeps no
  trailing empty piece (gkeyfile.c:4786-4792). The escaped `\;` becomes a literal `;` inside one item, so
  no backend matches.
- **Encoding (5):** `r93-encoding-invalid-first-group` (gtk), `r93-encoding-lowercase-ok` (kde),
  `r93-encoding-later-group` (gtk — here the invalid Encoding *is* in the first group `[other]`),
  `r93-encoding-nul-tail` (gtk), `r93-encoding-nul-exact` (gtk).
- **Name-validity (8, of which `key-name-byte-e9`, `group-name-byte-e9`, `group-header-invalid-e9` are
  coverage wins with base wrong):** `r93-key-locale-superscript`, `r93-key-locale-half` (kde; Python
  `str.isalnum("²"/"½")` and `g_unichar_isalnum` both true — probed, `type=15`), `r93-key-name-control-vt`
  (kde; a VT inside a key body is accepted by GLib, only group names reject ASCII controls),
  `r93-group-name-d7f` (gtk; 0x7F is `g_ascii_iscntrl`), `r93-key-locale-invalid-e9` (gtk; invalid UTF-8
  inside the `[...]` suffix fails `g_unichar_isalnum` → invalid key → whole file void), plus the three
  coverage rows above.
- **Whole-file invalid (2):** `r93-all-invalid-config` (gtk), `r93-empty-config` (gtk).

### The two name-validity rules, stated for the freeze

- **Group name** (`g_key_file_is_group_name`, gkeyfile.c:4567-4578, with `g_utf8_find_next_char`
  gutf8.c:178-194): iterate character starts (continuation bytes 0x80-0xBF are skipped); reject `]`, `[`,
  and bytes where `g_ascii_iscntrl` is true (ASCII 0x00-0x1F, 0x7F) on a char start; empty rejected.
  **No UTF-8 validation**, so bytes 0x80-0xFF — valid or invalid UTF-8 — are accepted in a group name.
- **Key name** (`g_key_file_is_key_name`, gkeyfile.c:4584-4638): the main body accepts any char except
  `=`, `[`, `]` (leading/trailing `' '` rejected) with no UTF-8 or control check; only a trailing
  `[...]` locale suffix requires `g_unichar_isalnum` or `- _ . @` on valid characters. Consequently an
  invalid byte in the key body is accepted while the same byte inside the locale suffix voids the file.

## Residual risk

- NUL in the trailing junk of a group line that itself contains `]` is covered only by
  `r93-nul-group-trailer-bracket`; other junk shapes (multiple `]`, NUL inside the scanned name before a
  later `]`) were reasoned from gkeyfile.c:1677-1701 but not each materialised.
- Python `str.isalnum` vs `g_unichar_isalnum` may diverge for exotic code points in a locale suffix;
  probed only `²`, `½` (both agree) and invalid UTF-8 (both reject).
- Candidate `len(loc) > 2` (:158) counts Python characters where GLib counts bytes; for every non-empty
  locale both are `>2` and for `x[]` both are `2`, so no observable difference was found, but the
  equivalence is reasoning, not a fixture.
- The candidate hardcodes the "interesting locale" set to `{c}` (comment at :159-161); correct only under
  the oracle's `LC_ALL=C` (g_get_language_names() == ["C"]). Other harness envs would diverge.
- xdg-desktop-portal 1.22.1 sources were **not** fetched; per-key eager-read semantics are inferred from
  oracle labels (consistent with r92 R92MExecD1), not read from `xdp-portal-config.c`.

## Verification gaps

- All labels are from the installed binary via the r90 oracle; `dir` mode only (no `xdg`-mode copy of
  these byte classes), 21 interfaces, desktop XFCE (+1 KDE UseIn case).
- No measured run: no counter CLI, no receipts; the numbers above come from the r90 counter's
  `run_tool`/`case_correct` invoked in-process (DRAFT).
- The candidate and base were run read-only; the candidate file was not modified.

## Commands (DRAFT; exit codes)

- `curl` of the four upstream files + `sha256sum` — matched the receipt hashes (gutf8.c recorded above).
- `gcc kfprobe.c $(pkg-config --cflags --libs glib-2.0)` → rc 0; probes reproduced every rule cited.
- `python3 portal-oracle-r93review.py --cases fixtures.json --label labels.json --scratch-root … --jobs 4`
  → rc 0, `PORTAL_ORACLE cases=53 incomplete=0 host_tail_sha256=4a4cf319…fbf9`; second run rc 0, labels
  byte-identical.
- `python3 score.py labels.json` → rc 0, `correct: {'base': 37, 'candidate': 41} of 53`.
- `python3 .ufo/waves/round-93/build/mado-portals.c1.py --selftest` → rc 0, `checks=22 failed=0`.
- No install; no git/jj mutation; no write outside this report, the fixtures file, and scratch.

## Files written

- `.ufo/waves/round-93/w1/R93MReviewC1.md` (this report).
- `.ufo/waves/round-93/w1/R93MReviewC1-fixtures.json` — **53 cases, JSON list** in the round-90 input
  schema (`id, mode, desktop, files{name: text}`; byte content as lone surrogates `\udcXX`; each case is
  self-contained with the kde/gtk/gnome descriptor trio). sha256
  `45b05a70096c0ff8ce4ce355a4a4d95442405ba8ccd0258b231b27158c5432d7`. It is a bare list per the seat
  item; the oracle CLI needs `{"cases": <list>}` — wrap with
  `python3 -c 'import json,sys; json.dump({"cases": json.load(open(sys.argv[1]))}, open(sys.argv[2],"w"))' in out`.
  Rerun labelling with the r93 oracle (byte writes) — the r90 oracle needs the `surrogateescape` write
  fix for the 8 fixtures with invalid bytes; NUL-only fixtures are safe either way.

Report: .ufo/waves/round-93/w1/R93MReviewC1.md
