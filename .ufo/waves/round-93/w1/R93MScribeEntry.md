# R93MScribeEntry — draft knowledge entry for C1 (GKeyFile byte classes)

Seat: scribe (leaf, no dispatch). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base
`4c6f723f3dca3a26f9d14475d695fe797e2e972c` (master), 2026-11-07. Duty: the C1 knowledge entry in the
shape of `corpus/knowledge/xdg-mime-default-resolution-r92.md`, nothing measured, nothing frozen.

## 1. What was produced

| file | what |
|---|---|
| `.ufo/waves/round-93/build/portal-keyfile-bytes-r93.md` | the draft entry (269 lines): frontmatter `source`/`covers`/`verified-at`/`recheck`; §1 who reads the bytes; §2 class (a) UTF-8 is a per-read check; §3 class (b) `g_ascii_isspace` has no `\v`; §4 class (c) repeated keys; §5 class (d) `x[]`/`x[C]`; §6 the lane tool's lines; §7 operator consequence; §8 limits; §9 reproduce; §10 placeholders |
| `.ufo/waves/round-93/w1/R93MScribeEntry-oracle-draft.txt` | DRAFT oracle labels for the 16 byte-class fixtures (header names the oracle copy, the two-write patch, the binary pin and the `splitlines` hazard) |
| this report | — |

Every rule in the entry cites an upstream line (`gkeyfile.c`, `gstrfuncs.c`/`.h`, `xdp-portal-config.c`)
or a frozen fixture id; the ids used are the round-92 `d1-…` ones (the fixtures the r93 set carries) and
`<case-id>` only where no fixture exists (§10 lists all placeholders). The measured receipt is left as
`<receipt>`.

## 2. Commands run and exit codes

All read-only except writes to the two files above and to my scratch. No counter, no `--draft-tool`, no
mutant, no scoring, nothing under `.ufo/waves/round-93/receipts/`.

| # | command | rc |
|---|---|---|
| 1 | `mkdir -p $S && curl -sSfL -o {gkeyfile.c,gstrfuncs.c,gstrfuncs.h} https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/…` then `curl -sSfL -o xdp-portal-config.c https://raw.githubusercontent.com/flatpak/xdg-desktop-portal/1.22.1/src/xdp-portal-config.c` (GitLab served a sign-in page for the flatpak path; the GitHub mirror is byte-identical to the S501 pin) | 0 |
| 2 | `sha256sum` on the four files — `e1d1270f…f656` (gkeyfile.c), `6ea1c433…2fd4` (gstrfuncs.c), `298b0dc4…6e23` (gstrfuncs.h), `2da4fd83…4fe1` (xdp-portal-config.c), all equal to the pins in `.ufo/waves/round-93/receipts/sources-open-r93.txt` and `corpus/SOURCES.md` S501/S502 | 0 |
| 3 | `grep -n` / `sed -n` reads of the four files for the exact line numbers cited (isspace sites, both `g_utf8_validate` sites, `key_get_locale`, `add_key_value_pair`, `is_key_name`, `line_is_group`, `line_is_key_value_pair`, `line_is_comment`, CR erase, `get_keys`, and xdp `:189/:201/:214/:244/:408/:411/:427/:441/:466/:538`) | 0 |
| 4 | `sha256sum .ufo/waves/round-93/build/mado-portals.c1.py` → `89039e30d329bee82f20c4a32edc9fa72c02774c98364017e131a372c9fb91d3` (matches the seat spec) and `tools/mado-portals.py` → `d1bd9b9a…6ab1` (read only) | 0 |
| 5 | **DRAFT** oracle label run: scratch copy of `.ufo/waves/round-90/controls/portal-oracle-r90.py` with only the two fixture writes changed to `open(p,"wb")` + `text.encode("utf-8","surrogateescape")`, plus the full log returned; driver imported it and ran the 16 cases of `.ufo/waves/round-92/controls/portals-gkeyfile-cases-r92.json` (`python3 label16.py \| tee oracle-draft-16.txt`) — 16/16 `done=True` | 0 |

No installs: nothing was needed; `pacman` untouched (guard). No git or jj command was run at all.

## 3. Key result

The entry states the four byte classes from the primary sources and from the installed binary's own
`-v` log, and separates what routing can see from what it cannot:

- (a) UTF-8 is validated only in the getters (`gkeyfile.c:2310`, `:2427`; the string `g_utf8_validate`
  occurs nowhere else in the file), never at load. Harmless in a comment / another group / an unread key
  (`d1-a1`…`d1-a4` → `kde`, `default config`); a `[preferred]` value the loader has never seen is still
  read eagerly by xdp (`xdp-portal-config.c:411`, `:427`, `:429-432`) and voids the whole file
  (`d1-a5` → `gtk`, log `Invalid portals for interface 'org.freedesktop.impl.portal.Print'`).
- (b) `g_ascii_isspace` = space/TAB/LF/FF/CR, no VT (`gstrfuncs.h:85-86`, `G_ASCII_SPACE` at `:54`,
  table row `gstrfuncs.c:264` `0x004, 0x104, 0x104, 0x004, …`). **Only a `\v` before a group header
  voids the file** (`d1-b1`); at key start / before `=` / after `=` / at value end the file loads and the
  key or value is renamed (mangle), with the same visible pick (see F1).
- (c) last value wins, first position kept (`gkeyfile.c:4420-4427`); `d1-c1` → `kde`, `d1-c2` →
  Settings `gtk`; the log repeats the key line because `g_key_file_get_keys` returns one entry per pair
  (`:2005-2060`).
- (d) `x[]` and `x[C]` are literal key names (`key_get_locale` `:1806-1830`; `get_string` looks up the
  exact name), so `d1-d1`…`d1-d4` never see `default`/`DBusName`; invisible in the label, visible in the
  log (`'default[]': kde`, `Error loading …: Key file does not have key “DBusName”`).

## 4. Gates

None run — the seat measures nothing. Status of what the L1 will need before the freeze:

- the round-93 oracle and case file do not exist yet (``.ufo/waves/round-93/controls/` is empty), so the
  cited case ids are the round-92 ones; the entry tells the L1 to rewrite them only if the frozen file
  renames them;
- the round-90 oracle **cannot materialise** the 16 fixtures as-is (strict UTF-8 writes) — the L1 must
  carry the two-write patch into the round-93 oracle and the counter before freezing (F5);
- `<receipt>` in the entry is the only receipt placeholder; no receipt was written by this seat.

## 5. Findings (each with a reproducing input)

**F1 — declaration §C1 class (b) overstates "voids the file".** The declaration says "a `\v` at line
start/key end/value start makes the line invalid and voids the file". Only the group-header position
does. Reproducing input `{"id":"…","mode":"dir","desktop":"XFCE","files":{"portals.conf":
"[preferred]\ndefault\v=kde\n", …}}` (`d1-b3-vt-before-equals`): oracle FileChooser/Print/Settings =
`gtk`, reason `gtk-last-resort`, and the log contains `Preferred portals for interface 'default\v': kde`
— the config **loaded**; the key is simply not `default`. Same for `d1-b2` (key `\vdefault`), `d1-b4`
(value `\vkde`), `d1-b5` (value `kde\v`); only `d1-b1` (`\v[preferred]`) has no `Preferred portals`
line, i.e. a load failure. Source: `gkeyfile.c:1625` skips only `g_ascii_isspace`; `:1738` chomps the
key, `:1757` chugs the value, `:1760` keeps trailing bytes; `g_key_file_is_key_name` (`:4584-4645`)
rejects only leading/trailing `' '`. **The C1 predicate is unaffected** (the pick is `gtk` either way);
the entry states the mechanism per position and §8 says the frozen set cannot distinguish void from
mangle. Recommend the L1 reword the declaration clause or leave it and note the entry as the precise
statement.

**F2 — R92MExecD1 §"New cases" is wrong for b2-b4.** The round-92 report's table marks `d1-b1`…`d1-b4`
"(void)"; only b1 is. Same inputs and log evidence as F1. Route to the L1 as an append-only correction
if that report is ever re-read as evidence.

**F3 — class (c) is partly observable; guidance for the mutant seat.** `d1-c1` (`default=gnome` then
`default=kde`) distinguishes last-value from first-value: a first-value implementation returns `gnome`
and the frozen label is `kde`, so c1 (and c2 for Settings) **kill** such a mutant. What no fixture can
see is the position rule (first position kept, `gkeyfile.c:4420-4427`), because nothing iterates
`[preferred]` in order. The entry says both; R92MExecD1 §(c) only said "not observable", which is
right for the position and too strong for the value.

**F4 — class (d) is invisible in the label, visible in the log.** `d1-d3`/`d1-d4` produce
`Error loading …: Key file does not have key “DBusName” in group “portal”` and `default=kde;gtk` →
`gtk`/`default config`. A `[C]` suffix is *not* stripped by `get_string`: even under `LC_ALL=C` the
stored key is `DBusName[C]` and the plain lookup misses. Any future C1 case that wants to count (d) must
score the descriptor load, not the pick.

**F5 — harness hazards the freeze must carry.** (i) The round-90 oracle writes fixtures with
`open(..., encoding="utf-8", newline="")` (two sites, lines 108 and 121) and raises on the `\udce9`
fixtures; the round-93 oracle and the counter must write bytes (`errors="surrogateescape"` or `{b64:…}`).
(ii) Any log parser that uses Python `str.splitlines()` splits at 0x0B: the b2-b5 `Preferred portals`
debug lines arrive in two pieces (sidecar shows it), so parse decision lines, not re-split debug text.

**F6 — `.portal` `UseIn` failure is unchecked.** `xdp-portal-config.c:244-252`: the `UseIn` result is
assigned and the backend inserted with no NULL check, so an invalid byte in `UseIn` leaves
`use_in = NULL` and the backend **kept** — unlike `DBusName`/`Interfaces` (`:201`, `:214`), which skip
it. No frozen case holds any of the three; the entry records it as `<case-id>` and the declaration does
not claim it.

## 6. Out of scope / not done

- No edits to `tools/`, `quality/`, `corpus/`, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`,
  the declaration, the candidate, the round-90/92 controls, or any other lane file. The entry sits in
  `build/`; moving it to `corpus/knowledge/` and adding the SOURCES/README rows is the L1's integration.
- No measurement, no receipts, no mutants, no fresh generator, no case ids added or renamed.
- No base-tool or candidate run: the base's 8/16 and the candidate's 16/16 are cited from
  `.ufo/waves/round-92/w1/R92MExecD1.md`, not re-executed here.
- No installs, no git/jj commands, no host services touched.

## 7. Scratch

`S=/fast/scratch/hyaku/mado-r93/R93MScribeEntry` held the four upstream files, the patched oracle copy,
the driver and the 16 run roots; the cited output was copied to
`.ufo/waves/round-93/w1/R93MScribeEntry-oracle-draft.txt` and the directory is deleted on exit (a
remaining directory is a defect).

Report: .ufo/waves/round-93/w1/R93MScribeEntry.md
