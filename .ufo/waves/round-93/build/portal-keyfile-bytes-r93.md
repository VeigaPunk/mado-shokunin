source: S501 (xdg-desktop-portal 1.22.1 — https://raw.githubusercontent.com/flatpak/xdg-desktop-portal/1.22.1/src/xdp-portal-config.c sha256 2da4fd835032401b2ca0e1a503cb600abdb68e27bc9d23b8fbd28f8e2d4c4fe1; host package xdg-desktop-portal 1.22.1-2, /usr/lib/xdg-desktop-portal sha256 e1429fbe1bf6c2203ba07f478b9e92e9221437b13a92eebafb0982748583a4f8), S502 (GLib 2.90.1 — https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gkeyfile.c sha256 e1d1270f6c9881daf8a9f49b41395cbdd8e99fa290212e8530e0bd3df23ff656; host package glib2 2.90.1-1), S511 (GLib 2.90.1 — glib/gstrfuncs.c sha256 6ea1c4333161ec4e7c85c212cb46200ec331e45f12ccd20c8d018a3fdaa62fd4 and glib/gstrfuncs.h sha256 298b0dc4c82805322df7534152b917f9acd54d44e81132988476bb59a6426e23 — the `g_ascii_isspace` table; row opened by the L1 this round); all four files re-fetched 2026-11-07 and digests re-checked equal to the pins in `.ufo/waves/round-93/receipts/sources-open-r93.txt`
covers: how xdg-desktop-portal 1.22.1 reads the bytes of `portals.conf` and `*.portal` through GLib 2.90.1 GKeyFile — when UTF-8 is validated, which bytes count as whitespace, repeated keys, and `x[]`/`x[C]` locale keys — and which of those rules routing can see
verified-at: 2026-11-07 — **DRAFT, not a measurement**: the 16 byte-class fixtures `.ufo/waves/round-92/controls/portals-gkeyfile-cases-r92.json` labelled by the installed `/usr/lib/xdg-desktop-portal` through the round-90 oracle in a private bus with byte-exact fixture writes; full output `.ufo/waves/round-93/w1/R93MScribeEntry-oracle-draft.txt`; the measured receipt is `<receipt>`
recheck: 90d — re-pull `gkeyfile.c`, `gstrfuncs.c`/`gstrfuncs.h` and `xdp-portal-config.c` at the next tag that changes any of them; also when `glib2` leaves 2.90.1-1 or `xdg-desktop-portal` leaves 1.22.1-2.

# GKeyFile byte classes in xdg-desktop-portal's `portals.conf` and `.portal` files

This entry states which *bytes* xdg-desktop-portal 1.22.1 accepts in the two key files it
reads — the per-directory `portals.conf` and each backend's `<name>.portal` — and how a byte
outside the ordinary ASCII range changes the decision it takes. Line numbers are those of the
upstream files at the pinned tags: `xdp-portal-config.c` (S501), `gkeyfile.c` (S502) and
`gstrfuncs.c`/`gstrfuncs.h` (S511). Behaviour is cited by the frozen fixture that measures it,
in `.ufo/waves/round-92/controls/portals-gkeyfile-cases-r92.json` (`d1-…` ids); the fixture
set the round-93 freeze carries, byte for byte. The label of every cited case is the installed
binary's own pick, taken in a private `dbus-run-session` with all roots under a scratch
directory (`.ufo/waves/round-93/w1/R93MScribeEntry-oracle-draft.txt`); those runs are DRAFT and
are not the C1 receipt.

Two words are used in a fixed sense below:

- **void** — the file contributes nothing: `g_key_file_load_from_file` fails, or the consumer
  drops the whole file after a failed key read. The *process* is unaffected and the config
  search continues with the next directory.
- **mangle** — the file loads, but a key or value carries a byte the consumer will never look
  up, so the file is present and has no effect. Routing cannot tell mangle from void; only the
  `-v` debug log can.

Both are distinct from "valid file that names no known backend", which also ends in the same
pick.

## 1. Who reads the bytes, and when

A `.portal` descriptor is loaded with `g_key_file_new()` + `g_key_file_load_from_file(…,
G_KEY_FILE_NONE, error)` (xdp-portal-config.c:189), then exactly three keys are read
immediately: `[portal] DBusName` with `g_key_file_get_string` (:201), `Interfaces` with
`g_key_file_get_string_list` (:214), `UseIn` with `g_key_file_get_string_list` (:244). A
failure at :201 or :214 is an error from the load function, logged
`Error loading …: <reason>`, and the backend is **skipped**; the `UseIn` result is not
checked at all (:244-252), so a failed `UseIn` read keeps the backend with `use_in = NULL`.
Nothing else in the file is ever read.

A `portals.conf` is loaded at xdp-portal-config.c:408, then the *whole* `[preferred]` group is
enumerated and every one of its keys is read eagerly: `g_key_file_get_keys(key_file,
"preferred", …)` (:411) followed by `g_key_file_get_string_list` per key (:427). A `NULL`
from any key read prints `Invalid portals for interface '%s' in %s` and `return NULL`
(:429-432) — the **whole config file is void**, including keys the session would never have
consulted.

Consequence: for these two files, "read at load" and "read by the consumer" are the same set
of keys. There is no lazy validation of the file as a whole.

## 2. (a) UTF-8 is a per-read check, never a load check

1. `g_key_file_load_from_file` performs no UTF-8 validation. The string
   `g_utf8_validate` occurs exactly twice in `gkeyfile.c`, at :2310 and :2427, and both are
   inside key *getters* — `g_key_file_get_string` (:2288) and `g_key_file_get_string_list`
   (:2401). The loader (`g_key_file_load_from_data` :974, `g_key_file_parse_data` :1834) only
   splits lines, strips one CR before an LF (:1856-1861) and dispatches them to
   `g_key_file_parse_line` (:1613).
2. So an invalid byte anywhere the consumer does not read is harmless: a comment, another
   group, an unread key of a `.portal`, an unread key of another group of `portals.conf`.
   `case d1-a1-nonutf8-comment-config` (`# cafe\xe9 latin` above a valid `[preferred]`) →
   FileChooser/Print/Settings `kde`, reason `default config`; `case d1-a2-nonutf8-other-group`
   (`[other] foo=bar\xe9`) → `kde`/`default config`; `case d1-a3-nonutf8-comment-portal` →
   `kde`/`default config`; `case d1-a4-nonutf8-portal-unrelated-key` (`Foo=bar\xe9` in
   `kde.portal`) → `kde`/`default config`. The log of a1-a4 contains
   `Preferred portals for interface 'default': kde`, i.e. the `[preferred]` group was read.
3. A value the consumer *does* read fails the key, and in `portals.conf` one failed key voids
   the file: `case d1-a5-nonutf8-config-read-key` (`org.freedesktop.impl.portal.Print=gnome\xe9`)
   → all three interfaces `gtk`, reason `gtk-last-resort`, and the log carries
   `Invalid portals for interface 'org.freedesktop.impl.portal.Print' in portals.conf` — the
   `Print` entry was never going to be consulted for `FileChooser`, and the config is still
   void. This is the "eager read" of §1, not a routing rule.
4. In a `.portal`, an invalid byte in `DBusName` or `Interfaces` fails only that backend
   (`Error loading …`, :201-:239); in `UseIn` it is silently dropped (the read's failure is
   unchecked, `use_in = NULL`, :244-252). The config and the other backends are unaffected. No
   frozen case holds this input — `<case-id>` (§8).
5. Read-time validation is per *value*, not per file: `g_key_file_get_string(_list)` validates
   the value string after `g_key_file_get_value` (:2179) returns it, and reports
   `G_KEY_FILE_ERROR_UNKNOWN_ENCODING` for that key alone (:2310-2325, :2427-2442).

## 3. (b) Whitespace is `g_ascii_isspace`, which has no vertical tab

6. `g_ascii_isspace(c)` is `(g_ascii_table[(guchar) c] & G_ASCII_SPACE) != 0`
   (gstrfuncs.h:85-86), with `G_ASCII_SPACE = 1 << 8` (gstrfuncs.h:54) and the table row for
   bytes 8-15 on gstrfuncs.c:264:
   `0x004, 0x104, 0x104, 0x004, 0x104, 0x104, 0x004, 0x004`. Byte 9 TAB, 10 LF, 12 FF and
   13 CR carry the bit; byte 11 VT (`\v`) does not (nor do 8 BS, 14 SO, 15 SI). Byte 32 space
   is the first entry of the next row and carries it.
7. `gkeyfile.c` uses that predicate in exactly three places on a line: the leading skip
   (:1625), the key-name trailing chomp (:1738) and the value's leading chug (:1757). All
   other whitespace handling is literal: `g_key_file_line_is_group` accepts only `' '` and
   `'\t'` after the `]` (:4647-4672), `g_key_file_is_key_name` rejects only a leading or
   trailing `' '` (:4584-4645), and a value's *trailing* bytes are never stripped — only the
   leading ones are chugged (`value_len = line + length - value_start`, :1760).
8. Therefore, per position of a `\v`:

| position | fixture | what the parser does | oracle label | why |
|---|---|---|---|---|
| before a group header | `\v[preferred]` (`case d1-b1-vt-before-group`) | the leading skip stops at `\v`; `g_key_file_line_is_comment` needs `#`/`\0`/`\n` (:4561-4564), `g_key_file_line_is_group` needs `[` (:4647), `g_key_file_line_is_key_value_pair` needs `=` (:4675-4690) — all false → `Key file contains line … which is not a key-value pair, group, or comment` (:1638-1649) → **void** | FileChooser/Print/Settings `gtk`, `gtk-last-resort`; the log has no `Preferred portals` line at all | config file dropped before any key is read |
| before a key | `[preferred]\n\vdefault=kde` (`case d1-b2-vt-before-key`) | `\v` survives the leading skip and becomes part of the key name; `g_key_file_is_key_name` accepts it → key `\vdefault` | `gtk`, `gtk-last-resort`; the log line is `Preferred portals for interface '\vdefault': kde` (split in two by any `str.splitlines()`) | **mangle**: no consumer looks up `\vdefault` |
| before `=` | `[preferred]\ndefault\v=kde` (`case d1-b3-vt-before-equals`) | the key chomp (:1738) stops at `\v`, so the key is `default\v`; valid key name | `gtk`, `gtk-last-resort`; log `interface 'default\v': kde` | **mangle**: not the `default` key |
| after `=` | `[preferred]\ndefault=\vkde` (`case d1-b4-vt-after-equals`) | the value chug (:1757) stops at `\v`, so the value is `\vkde`; the list gets the item `\vkde` | `gtk`, `gtk-last-resort`; log `interface 'default': \vkde` | **mangle**: no backend named `\vkde` |
| at value end | `[preferred]\ndefault=kde\v` (`case d1-b5-vt-trailing-value`) | trailing bytes are kept (§3.7), so the item is `kde\v` | `gtk`, `gtk-last-resort`; log `interface 'default': kde\v` | **mangle**: no backend named `kde\v` |

   Only the first row voids the file. In the other four the file loads and simply has no
   effect on routing. The declaration's sentence "a `\v` at line start/key end/value start
   makes the line invalid and voids the file" is exact for the group-header row and
   overstates the other three; the visible pick is the same either way, so the C1 predicate is
   unaffected.
9. The bytes that *are* whitespace are stripped in the same three positions, so a leading TAB
   or FF before `[preferred]`, before a key, or after `=` changes nothing
   (`\t[preferred]`, `default\t=kde`, `default=\tkde` all behave as the plain text). A
   *trailing* TAB or FF in a value is not stripped and has the same no-match effect as b5;
   no frozen case holds it — `<case-id>` (§8).
10. `\v` is not an escape either: `\v` in text is a literal byte. The only escapes GKeyFile
    decodes are `\s \n \t \r \\` and, in a list, the separator `\;`; anything else is
    `Key file contains invalid escape sequence` at read time (:4693-4770, message at :4761;
    candidate `string_list` at `.ufo/waves/round-93/build/mado-portals.c1.py:177-205`).

## 4. (c) Repeated keys: last value wins

11. `g_key_file_add_key_value_pair` (:4420-4427) does
    `g_hash_table_replace(group->lookup_map, pair->key, pair)` — the newest pair replaces the
    older one in the lookup map — and inserts the pair into the ordered list *before* the
    `sibling` that is the first existing pair for that key (`g_key_file_add_key` :4430-4447).
    Net: the key keeps its **first position** and takes its **last value**.
12. `g_key_file_get_keys` returns one entry per stored pair, duplicates included (:2005-2060),
    so xdp loops over a repeated key once per occurrence, and each read returns the last value.
    `case d1-c1-repeated-default` (`default=gnome` then `default=kde`) → `kde`,
    `default config`, log `Preferred portals for interface 'default': kde` twice (the second
    `default` is read but `default_portal != NULL` so xdp warns and ignores the duplicate:
    xdp-portal-config.c:441-446). `case d1-c2-repeated-settings`
    (`Settings=gnome` then `Settings=gtk`) → Settings `gtk`, FileChooser/Print `kde`.
13. What routing **cannot** see is the position rule: no consumer iterates `[preferred]` in
    order for a decision, so keeping the first position or moving the key to the end is
    invisible. The value rule *is* visible — c1 and c2 kill a first-value implementation.
    This is why the class is carried as a regression, not as counted coverage
    (R92MExecD1 §(c)).

## 5. (d) `x[]` and `x[C]` are plain keys

14. `key_get_locale` (:1806-1830) takes the text from the last `[` and treats it as a locale
    only when its length is greater than `2` (i.e. more than `[]`); otherwise the key has no
    locale. `g_key_file_locale_is_interesting` (:1586-1610) compares against
    `g_get_language_names()`, which under `LC_ALL=C` is `["C"]`. So `x[]` is the plain key
    `x[]`, `x[C]` is the plain key `x[C]` (interesting locale or not, the *stored* name keeps
    the suffix), and `x[en]` is dropped under `LC_ALL=C`.
15. A plain `g_key_file_get_string(key_file,"portal","DBusName")` (:201) looks up the exact
    name `DBusName`; it does not strip a `[…]` suffix. Locale suffixes are only resolved by
    the `g_key_file_get_locale_string(_list)` family (:2591, :2759), which xdp does not call.
16. Hence `case d1-d1-default-empty-locale` (`default[]=kde`) → `gtk`, `gtk-last-resort`, log
    `Preferred portals for interface 'default[]': kde` — the `default` key does not exist.
    `case d1-d2-iface-empty-locale` (`FileChooser[]=kde` plus `default=gtk`) →
    `gtk`/`default config`, log shows both `'default': gtk` and
    `'org.freedesktop.impl.portal.FileChooser[]': kde`.
17. `case d1-d3-dbusname-empty-locale` and `case d1-d4-dbusname-c-locale` put the suffix on a
    `.portal`'s `DBusName`: the backend descriptor is skipped with
    `Error loading …: Key file does not have key “DBusName” in group “portal”` in both, and
    `default=kde;gtk` then resolves to `gtk`/`default config`. The class is invisible in the
    routing label alone: the pre-port tool dropped these keys and reached the same picks
    (R92MExecD1 §(d)), so only the debug log distinguishes "key stored with a suffix" from
    "key absent".

## 6. What the lane tool models

`tools/mado-portals.py`, as ported in `.ufo/waves/round-93/build/mado-portals.c1.py`
(sha256 `89039e30d329bee82f20c4a32edc9fa72c02774c98364017e131a372c9fb91d3`):

- :68 `ASCII_SPACE = " \t\n\f\r"` (the virtual tab is absent), used for the leading skip (:128),
  the key `rstrip` (:147) and the value `lstrip` (:150) — §3;
- :171-175 `_check_utf8`, called at the head of `string_list` (:179) and `plain_string` (:216),
  is the only UTF-8 test, and the file is read as
  `open(path,"rb").read().decode("utf-8","surrogateescape")` (:284-285 for `.portal`,
  :360-361 for `portals.conf`) — §2;
- :356-376 `load_config_file` iterates every `[preferred]` key and returns `None` on the first
  `string_list` failure, which is the eager void of §1;
- :147-160 the key chomp/chug and :157-169 the locale rule (`x[]` plain, `x[C]` plain, other
  locales dropped) — §4, §5.

The rule that a *repeated* key keeps its first position is modelled (dict insertion order,
:167-169) but has no observable consequence (§4.13).

## 7. Operator consequence

A hand-edited `~/.config/xdg-desktop-portal/portals.conf` is read by both the config loader
and, for `default`/per-interface values, immediately — so two ordinary editing accidents
change behaviour silently:

- **A stray `\v` (0x0B) immediately before a `[group]` header or a `#` comment** — a paste
  from a terminal, a broken editor macro, a file copied out of a pager — makes the line
  unparsable and **drops the whole config file**: every `[preferred]` choice in it stops
  applying, and the session falls to the `UseIn` fallback and then the gtk last resort, with
  no message at the default log level (`load_from_file(…, NULL)` at
  xdp-portal-config.c:408 discards the error).
- **A Latin-1 (or otherwise non-UTF-8) byte in any `[preferred]` value** — a comment in the
  file is harmless (§2.2), but a value is not — **drops the whole config file** with a
  `CRITICAL: Invalid portals for interface '…'` line at :429-432, which is only visible with
  the portal's debug/verbose logging on.
- A `\v` at the start of a key line or inside a key or value (§3.8 rows 2-5) does not drop
  the file; it renames the key or the value, so that entry silently stops applying — and the
  file looks right in an editor that renders 0x0B as a space.

After a void, configs in *other* searched directories still apply (xdp-portal-config.c:466-508,
:538-589); only the offending file is lost.

## 8. Limits and uncovered classes

- The five `d1-…` fixtures of class (b) all have the same visible label, so the frozen set
  cannot distinguish void from mangle; the mechanisms above come from the code and from the
  `-v` log, and the log itself is split at 0x0B by any parser using `str.splitlines()` (a
  hazard for the round-93 harness — match on `pick` fields, not on re-split debug lines).
- Not covered by any frozen fixture, and not claimed as measurement:
  `<case-id>` — `\v` before a comment line (`\v# note`), expected void like b1;
  `<case-id>` — trailing TAB or FF in a value (`default=kde\t`), expected mangle like b5;
  `<case-id>` — an invalid byte in a *read* `.portal` key: `DBusName` or `Interfaces`,
  expected "backend skipped", not "config void"; `UseIn`, expected "backend kept without a
  UseIn";
  `<case-id>` — the fresh byte-class generator's cases, unfrozen at the time of writing.
- The case ids cited above are the round-92 ones; the round-93 freeze carries the same
  fixtures, and the L1 rewrites the ids if the frozen file renames them.
- Out of scope: everything else about the two files — the search order and per-directory
  selection (S501), the `none`/`*` values, the `[portal]` name validations, the first-group
  `Encoding` rule (S502 :1764-1772), and the rest of the escape/list grammar — which is the
  round-90 knowledge entry's subject, not this one's.
- The round-92 base tool's divergence on these fixtures (8 of 16 wrong: a1-a4, b1-b4) is
  recorded in `.ufo/waves/round-92/w1/R92MExecD1.md`; the measured C1 receipt is
  `<receipt>`.

## 9. Reproducing the DRAFT labels

The round-90 oracle writes fixtures strictly UTF-8, so it cannot materialise a case whose
content carries a lone surrogate; change its two writes to bytes and nothing else:

```sh
# in a copy under scratch:
#   open(p, "w", encoding="utf-8", newline="")  →  open(p, "wb")
#   fh.write(text)                              →  fh.write(text.encode("utf-8","surrogateescape"))
python3 - <<'PY'   # label the 16 fixtures; every root under scratch
import importlib.util, json, os
spec = importlib.util.spec_from_file_location("od", "oracle-draft.py")
od = importlib.util.module_from_spec(spec); spec.loader.exec_module(od)
cases = json.load(open(".ufo/waves/round-92/controls/portals-gkeyfile-cases-r92.json"))["cases"]
for c in cases:
    r = od.run_case(c, "/fast/scratch/hyaku/mado-r93/R93MScribeEntry/runs", 8.0)
    print(c["id"], r["done"], r["picks"]["org.freedesktop.impl.portal.FileChooser"],
          r["reasons"].get("org.freedesktop.impl.portal.FileChooser"))
PY
```

The 2026-11-07 run of exactly this driver is `.ufo/waves/round-93/w1/R93MScribeEntry-oracle-draft.txt`
(16/16 complete runs, `done=True`; the fixture bytes are `b'# cafe\xe9 latin\n[preferred]\ndefault=kde\n'`
and its siblings, not re-encodable text).

## 10. Placeholders, for the freeze

Everything still unfrozen at the time of writing, by the place it is used:

| placeholder | where | what it stands for |
|---|---|---|
| `<receipt>` | frontmatter `verified-at`, §8 | the measured C1 receipt (`.ufo/waves/round-93/receipts/`), written only after the L1 freezes |
| `<case-id>` | §2.4, §8 | an invalid byte in a *read* `.portal` key (`DBusName`/`Interfaces` → backend skipped; `UseIn` → backend kept with `use_in = NULL`) |
| `<case-id>` | §8 | `\v` before a comment line (`\v# note`), expected void like b1 |
| `<case-id>` | §8 | a trailing TAB or FF in a value (`default=kde\t`), expected mangle like b5 |
| `<case-id>` | §8 | the fresh byte-class generator's cases |

The `d1-…` ids in §2-§5 are frozen in round 92 and are the fixtures the round-93 set
carries; only a rename in the frozen r93 file forces them to be rewritten.

