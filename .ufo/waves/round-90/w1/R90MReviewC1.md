# R90MReviewC1 — line-by-line review of C1 candidate vs upstream (round 90, w1, DRAFT)

Seat: R90MReviewC1 (reviewer, leaf — no subagents). Candidate: `.ufo/waves/round-90/build/mado-portals.c1.py`
(608 lines). References: xdg-desktop-portal 1.22.1 tarball (sha256
`5afeda953c3743efaa1160e73d62c5bfcac2ceca60e0e134e9b48ed651783625` — verified on download),
`src/xdp-portal-config.c` (1004 lines); GLib 2.90.1 `glib/gkeyfile.c`, `glib/gutils.c`,
`gio/gdbusutils.c` (tag 2.90.1 raw). Canonical runtime: installed `/usr/lib/xdg-desktop-portal`
(sha256 recorded in `R90MReviewC1-evidence-labels.json` as `oracle_binary_sha256`), host tail
`/usr/share/xdg-desktop-portal` digest `4a4cf31921e2…f0fbf9` (matches the declaration pin), LC_ALL=C.
Every oracle/candidate run in this report is **DRAFT** (pre-freeze); no receipt was written.
All scratch was created under `$HYAKU_SCRATCH/mado-r90/R90MReviewC1` and deleted afterwards.

Evidence files (this directory): `R90MReviewC1-evidence-probe.txt` (GLib probe T01–T24; T05 and the
first T09 sub-assertion are bad *test expectations*, annotated below — the probe binary exits 1
because of those two, not because of GLib), `R90MReviewC1-evidence-probe3.txt`, 
`R90MReviewC1-evidence-battery.txt` (17 oracle-labelled fixtures vs candidate JSON),
`R90MReviewC1-evidence-labels.json` (full cases + oracle labels + digests),
`R90MReviewC1-evidence-probe.c` / `R90MReviewC1-evidence-battery.py` (reproduction scripts).

Method: two independent tracks — (a) source reading of every candidate function against the
upstream lines it models; (b) a 17-fixture battery labelled by the oracle (`dir` mode unless noted)
and diffed against candidate `--json` output on identical inputs, plus a C probe against the
installed GLib 2.90.1 (the same library the oracle binary links) for the GKeyFile/D-Bus rules.

## 1. Confirmed divergences (tool ≠ oracle)

### CAND-1 — the GKeyFile `Encoding` start-group rule is not modelled (CONFIRMED, kills d2)
- Upstream: `gkeyfile.c:1768-1781` — while parsing a key line, if the group is the **first group of
  the file** (`start_group == current_group`) and the key is exactly `Encoding`, a value that is not
  precisely `UTF-8` (5 chars after leading-whitespace chomp; case-insensitive) fails
  `g_key_file_load_from_file` → the whole file is rejected. Verified by probe T02 (rejects),
  T03/T04 (`UTF-8`/`utf-8` accepted), probe2 E1 (a later group's `Encoding` is ignored).
- Candidate: `parse_keyfile` (`.c1.py:115-152`) has no `Encoding` rule; `load_portal:254-281` and
  `load_config_file:323-347` accept such files.
- Fixture d2 (`dir`, desktop Hyprland): `kde.portal` = `[portal]` + `Encoding=ISOLatin1` + valid
  DBusName/Interfaces; `gtk.portal` valid (gtk DBusName, FileChooser+Settings); `portals.conf`
  `default=kde`.
  - oracle: FileChooser=**[gtk]**, Settings=**[gtk]**, reason `gtk-last-resort` (kde.portal skipped
    at load);
  - candidate: FileChooser=**[kde]**, Settings=**[kde]**, reason `default config` / `config`
    (kde.portal registered).
- Repro: `R90MReviewC1-evidence-battery.py`, case `d2_encoding`; labels in
  `R90MReviewC1-evidence-labels.json`. Any frozen case whose `.portal` or `portals.conf` first
  group carries `Encoding≠UTF-8` fails the candidate as-is.

### CAND-2 — a failed `UseIn` read skips the whole backend file (CONFIRMED, kills d3)
- Upstream: `xdp-portal-config.c:244-252` — `use_in = g_key_file_get_string_list(… "UseIn" …,
  error)`; the returned error is **never checked**; the portal is unconditionally inserted and
  `register_portal` returns TRUE. A `UseIn` value with an invalid escape sequence (probe T12:
  load succeeds, `get_string_list` returns NULL with error) therefore registers the backend with
  `use_in == NULL` — exactly as if the key were absent.
- Candidate: `.c1.py:277` — `use_in = string_list(g["UseIn"]) if "UseIn" in g else None` sits
  inside the try block; `string_list` raises `KeyFileError` on the invalid escape and
  `load_portal` skips the entire file (warning printed).
- Fixture d3 (`dir`, desktop Hyprland): `hyprland.portal` with
  `UseIn=Hyprland;\q` (invalid escape), Interfaces FileChooser;Screenshot; `portals.conf`
  `default=hyprland`.
  - oracle: FileChooser=**[hyprland]**, Screenshot=**[hyprland]**, reason `default config`;
  - candidate: backends=∅ → FileChooser/Settings=**[]** reason `no-backend`
    (warning: `invalid escape sequence \q`).
- Repro: case `d3_useinescape` in the battery files. DBusName/Interfaces failures must still skip
  the file (upstream does); only the `UseIn` read is error-tolerant upstream.

## 2. Source-verified divergences the oracle harness cannot reach

These cannot be labelled by `portal-oracle-r90.py` (its `materialise` synthesises
XDG_CONFIG_DIRS/XDG_DATA_DIRS with no empty elements, writes files as UTF-8 text, and derives
paths from JSON keys), so they are source+probe findings only. They should be fixed with CAND-1/2
or re-declared as limits.

- CAND-3 — **empty `XDG_CONFIG_DIRS`/`XDG_DATA_DIRS` elements**: GLib `gutils.c:2597-2608`
  (`g_build_system_data_dirs`) and `:2633-2640` (`g_build_system_config_dirs`) only substitute the
  default when the variable is unset *or entirely empty*, then `g_strsplit(v, ":", 0)` which
  **keeps empty elements** (probe T23: `"a::b"` → 3 elements). Upstream then
  `g_build_filename("", "xdg-desktop-portal", …)` → consults the **relative** path
  `xdg-desktop-portal/…` (against the daemon cwd). Candidate `split_path_list` (`.c1.py:482-486`)
  drops empty elements (`[p for p in v.split(":") if p]`). Relative *non-empty* paths are kept by
  both (match).
- CAND-4 — **non-UTF-8 file bytes**: candidate reads files with `encoding="utf-8"`
  (`.c1.py:258, .c1.py:325`) and skips the whole file on `UnicodeDecodeError`; upstream reads
  bytes and fails only the individual getter whose raw value is not valid UTF-8
  (`gkeyfile.c:2310-2317` / `:2424-2431`). A config whose *comment* holds a stray invalid byte is
  fully usable upstream but discarded by the candidate. The declaration's named limit ("Invalid
  UTF-8 … treated as unreadable") covers the practical case, but note it is broader than needed.
- CAND-5 — **non-UTF-8 filenames crash the sort**: `sort_impls` (`.c1.py:301-320`) does
  `a.source.encode()`; a filename containing undecodable bytes arrives as a surrogateescape str and
  `.encode()` raises `UnicodeEncodeError`, aborting the tool. Upstream compares bytes
  (`g_strcmp0`). Inexpressible in the case JSON format; theoretical robustness gap.
- CAND-6 — **HOME unset**: candidate falls back to `/` (`.c1.py:489`), GLib falls back to the
  passwd home. The oracle always pins HOME; unreachable in the harness. Cosmetic.

## 3. Oracle parser (`portal-oracle-r90.py` `run_case`) review

- **O1 (CONFIRMED defect, d11) — DONE marker as a substring of any line lets an incomplete run
  count complete.** `run_case` breaks reading at the first line containing
  `"org.freedesktop.portal.Desktop acquired"` and `done` is that substring test. With `-v` the
  binary echoes fixture-controlled strings, notably `g_debug("loading %s", path)`
  (xdp-portal-config.c:193) and `g_debug("Preferred portals for interface '%s': %s", …)`
  (xdp-portal-config.c:431-434). A fixture **filename or config value** containing the marker
  stops the read before the decision lines; `done=True`, every not-yet-decided interface is
  labelled `[]`, and `main` reports success (no `ORACLE_INCOMPLETE`). Demonstrated: case
  `d11_marker_injection` (a portal file named `evil org.freedesktop.portal.Desktop acquired.portal`,
  truth FileChooser=[a]) → oracle label FileChooser=**[]** while the candidate correctly answers
  **[a]**. Fix suggestion: anchor the marker (e.g. the actual name-acquired log format) or scan
  the whole log after EOF and require the marker in the final line, or filter out `Xdp-DEBUG`
  echo lines before the substring test. The frozen case set must not contain the marker in any
  filename/value — worth an L1 check over `portal-cases-r90.json`.
- O2 — non-Settings `(config)` lines: the parser skips reason `config` for non-Settings ifaces.
  Correct for the pinned binary: `(config)` is logged only by
  `xdp_portal_config_find_impl_configs_by_iface` (:812), reachable only from `find_all`, which
  1.22.1 only uses for Settings. If the binary changed, labels would silently lose picks; the
  recorded `oracle_binary_sha256` pins this.
- O3 — interleaved log: all decision lines are emitted from the single-threaded start-up sequence
  before the bus name is acquired; `subprocess` line iteration preserves order; no interleaving
  vector found.
- O4 — genuine incompleteness (timeout `-s KILL 8`, crash before acquisition) yields `done=False`,
  `ORACLE_INCOMPLETE` on stderr and exit 1 with no label written — correct. Verified: battery run
  `incomplete=0`, rc=0.
- O5 — docstring/code drift: the docstring offers `Providing portal …Registry` as an alternative
  completeness marker; `DONE_MARKERS` implements only the acquired line. Harmless today, but the
  drift is what makes O1 easy to miss.
- O6 — `errors="replace"` on log decode: marker bytes can't hide in invalid UTF-8 (replaced chars
  never match), and labels can't be poisoned by binary output. OK.
- O7 — `materialise` writes JSON-decoded strings only, so invalid-UTF-8 fixtures are inexpressible
  (consistent with the declaration's named limit; see CAND-4).

## 4. Refuted suspicions (each probed; candidate == upstream)

| # | Suspicion | Refuted by |
|---|---|---|
| R1 | key containing `]` accepted by candidate (probe T01, fixture d1) | candidate `_valid_key_name` stop-set `"=[]"` includes `]` — file voided exactly like GLib (`gkeyfile.c:4584-4637`); battery d1 SAME |
| R2 | value leading whitespace kept upstream | `gkeyfile.c:1757` chomps leading isspace; fixture d4 SAME (`default= kde` → kde both) |
| R3 | group names trimmed inside brackets | `gkeyfile.c:1664-1680` keeps the raw name; fixture d5 SAME (`[ preferred ]` unusable both) |
| R4 | trailing `\v`/`\f`/whitespace-only lines handled differently | `parse_line:1622-1623` chomps `g_ascii_isspace` (incl. `\v \f`); blank lines never reach `parse_line` (`gkeyfile.c:1856-1868`); CRLF erased at `:1856-1861`; candidate matches; probe3: `\v` inside a group line voids the file in both |
| R5 | `"a;b;"` list trailing piece | GLib keeps the non-empty tail: `{a,b}` (probe2 E2 — my first probe assertion was wrong); candidate identical |
| R6 | `org.1a` valid bus name in GLib (digit after dot) | `gdbusutils.c:34-77`: the char after every `.` must be a valid *initial* char (no digit); probe T21; candidate regexes equivalent; also `:1.2` valid, hyphen-initial elements valid (`org.-foo.bar-1`), 255/256-byte boundary exact (probe T21, fixtures d8/d9 SAME) |
| R7 | `\;` mishandled in scalars or lists | `gkeyfile.c:4732-4735`: `\;` decodes only when splitting (pieces≠NULL), invalid in scalar get_string — candidate `plain_string`/`string_list` match (probe T10, fixture d7 SAME) |
| R8 | inner spaces in keys rejected | `gkeyfile.c:4599-4605` accepts inner spaces (only initial/final rejected); candidate matches (probe T14) |
| R9 | locale-suffixed keys modelled wrong | C locale drops `[de]` but keeps `default[C]` under its raw name as a non-default key (probe T13; fixtures d14/d15 SAME — the empty-but-present `[preferred]` group also stops the dir search in both) |
| R10 | duplicate-key lines | `g_hash_table_replace` (gkeyfile.c:4425) → last value wins; candidate matches (probe T20) |
| R11 | non-ASCII desktop token | both drop it (`validate_xdg_desktop` is ASCII-only); fixture d20 SAME |
| R12 | sort comparator divergence (case handling, tiebreak, `break`) | `xdp-portal-config.c:268-296` vs `.c1.py:301-320` equivalent; fixture d12 SAME (sorted-first UseIn pick); d10 SAME (Settings `kde;*` → kde,gtk,hyprland) |
| R13 | duplicate source names across directories | xdg-mode fixture x1 SAME: `data_home` wins over `data_dirs/0` for `homekde.portal`; config_home beats config_dirs/0; host tail merged identically (backends include gnome-keyring/kwallet/gtk/hyprland) |
| R14 | `none` semantics / empty-list semantics | d19 SAME (`FileChooser=none;kde` → none wins); interface key checked exclusively when present, else default (`xdp-portal-config.c:646-674` vs `.c1.py:388-391`) |

## 5. Function-by-function mapping (candidate → upstream)

| Candidate (line) | Upstream modelled | Verdict |
|---|---|---|
| `_is_group_line` (:82) | `gkeyfile.c:4620-4645` line_is_group (first `]`, then only ` ` `\t` to EOL) | match |
| `_valid_key_name` (:91) | `gkeyfile.c:4584-4637` is_key_name (`=[]` stop, initial/final space, tag charset alnum∪`-_.@`, tag must close at end) | match |
| `_valid_group_name` (:109) | `gkeyfile.c:4567-4581` is_group_name (reject `[`,`]`, 0x00-0x1f, 0x7f, empty) | match |
| `parse_keyfile` (:115) | `gkeyfile.c:1613-1650` parse_line, `:1664-1680` parse_group (no name trimming), `:1699-1800` parse_key_value_pair (key chomp :1738-1743, is_key_name :1745, value leading chomp :1757-1759, locale drop :1788-1790), `:1856-1868` CRLF/blank, `:4693-4801` escape decode | match **except CAND-1** (Encoding :1768-1781 unmodelled) |
| `string_list` (:155) | `g_key_file_get_string_list` `gkeyfile.c:2401-2473` + split/decode `:4693-4801` (`\;` ok in lists, trailing empty dropped, invalid escape → error) | match |
| `plain_string` (:192) | `g_key_file_get_string` `gkeyfile.c:2288-2340` (`\s \n \t \r \\` only; `\;`/unknown → error) | match |
| `is_bus_name` (:218) | `gdbusutils.c:114-151` g_dbus_is_name + `:25-77` is_valid_* (unique `:1.x` digit-initial ok, per-element digit ban, hyphens, 255 bytes) | match |
| `is_interface_name` (:228) | `gdbusutils.c:235-261` (no `-`, no digit-initial elements) | match |
| `current_desktops` (:236) | `xdp-portal-config.c:115-131` validate_xdg_desktop, `:134-159` get_valid_current_desktops, `:161-170` lowercase | match |
| `Impl`/`load_portal` (:254) | `xdp-portal-config.c:177-253` register_portal | match **except CAND-2** (:244-252 error-tolerant UseIn) |
| `load_portal_dir` (:284) | `:299-342` load_installed_portals_dir (suffix filter; first-of-name wins :196-202) | match (candidate checks `seen` before parse; upstream after — same set) |
| `sort_impls` (:301) | `:268-296` sort_impl_by_use_in_and_name (per-desktop case-insensitive UseIn, break on tie-true, strcmp tiebreak) | match |
| `load_config_file` (:323) | `:396-464` load_portal_configuration_for_dir (no `[preferred]` → NULL; per-key list failure voids file; `default` singled out; **empty group still yields a config**) | match (shares CAND-1) |
| `load_config_directory` (:350) | `:467-508` (desktop files in order, then `portals.conf`) | match |
| `Resolver.__init__` (:358) | `:618-628` xdp_portal_config_new, `:344-394` load_installed_portals (dir override :359-365; DATA_HOME→DATA_DIRS→DATADIR :367-384), `:511-604` load_portal_configurations (CONFIG_HOME→CONFIG_DIRS→SYSCONFDIR→DATA_HOME→DATA_DIRS→DATADIR :538-600; no dedup) | match **except CAND-3** (empty env elements) |
| `_prefers_none` (:388) | `:646-677` (iface key exclusive when present; else default) | match |
| `_by_list` (:393) | `:735-777` by_iface + `:694-712` find_any (`*` = first sorted supporting, stops list) + `:714-732` by_name | match |
| `_usein` (:408) | `:889-916` (find) / `:977-999` (find_all) loops | match (all-mode dedup — upstream binary would duplicate an impl matching ≥2 desktops; the oracle parser dedups too, so labels agree; already declared) |
| `_gtk` (:421) | `:824-853` gtk last resort by DBusName | match |
| `find` (:427) | `:856-926` xdp_portal_config_find | match |
| `_all_by_list`/`find_all` (:445/:456) | `:928-1004` find_all + `:779-822` by_ifaceS (portals-outer×sorted-impls-inner, dedup, default only if iface added none, `*` adds all supporting) | match |
| `resolve` (:476) | Settings→find_all, else find (matches observed binary labels) | match |
| `split_path_list`/`build_from_args` (:482/:488) | `gutils.c:2597-2608/2633-2640` defaults `/usr/local/share/:/usr/share/`, `/etc/xdg`; empty→default | match **except CAND-3/CAND-6** |
| `report`/`selftest`/`main` (:501/:522/:581) | tool-own contract (reason vocabulary matches the oracle's regex literals; selftest 19/19, DRAFT exit 0) | ok |

## 6. Residual risk and verification gaps

1. CAND-1/CAND-2 will fail any frozen case that exercises them; either fix the tool before the
   freeze (both are small, upstream-cited patches) or ensure the case set contains no `Encoding`
   first-group file and no invalid-escape `UseIn` (checking the frozen `portal-cases-r90.json`
   for these two patterns is cheap and mechanical).
2. O1: run a mechanical scan of the frozen case set for the substring
   `org.freedesktop.portal.Desktop acquired` in any filename or value before trusting labels.
3. CAND-3/4/5/6 are untestable through this harness; if the L1 wants them measured, the harness
   needs a byte-level file writer and raw-env control — out of my seat.
4. The counter/`--rev` path and case-freeze mechanics were not my scope; I ran only `--selftest`
   (19/19 pass, DRAFT), the oracle, and direct candidate invocations.
5. No installs were performed (pacman guard respected; nothing beyond the tarball/raw fetches
   already authorised by the item). Scratch `$HYAKU_SCRATCH/mado-r90/R90MReviewC1` deleted.
