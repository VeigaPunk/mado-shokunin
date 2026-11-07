# R92MExecD1 — re-prove mado-portals on the four M91-1 byte classes

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Base `d992ef74` (master). All runs below are DRAFT (counter `--draft-tool`, exit 3) unless stated; no receipts written.

## Oracle and harness (round 90, unchanged)

- Oracle: `.ufo/waves/round-90/controls/portal-oracle-r90.py` — installed `/usr/lib/xdg-desktop-portal` (sha256 `e1429fbe…8f8`), `dir` mode (`XDG_DESKTOP_PORTAL_DIR` single dir), 21 impl interfaces queried, completion line `XDP: org.freedesktop.portal.Desktop acquired`, host tail digest `4a4cf319…fbf9` (includes `/usr/share/xdg-desktop-portal`).
- Counter: `quality/counters/c1-r90-portal-routing.py` — sandboxed tool (`bwrap`, `--clearenv`, `LC_ALL=C`), `--draft-tool FILE` prints `DRAFT_*`, exit 3.
- Tool CLI: `mado-portals.py --portal-dir D --desktop X --json` (dir mode); `--selftest` 22 checks both before/after (rc 0).

**Caveat (must be fixed for a frozen set):** the round-90 oracle and counter materialise fixtures with `open(..., encoding="utf-8", newline="")` strict — a byte 0xE9 written as surrogate `\udce9` raises `UnicodeEncodeError` in both. My labels used the same oracle code with only the write changed to `errors="surrogateescape"` (file bytes identical, `b'caf\xe9'`); the counter/manual scorer used likewise-patched `materialise`. The L1 freezing these cases must apply the same one-line change to oracle/counter or store fixtures as `{b64:…}` floats. Otherwise the oracle cannot even materialise class (a).

## New cases — `.ufo/waves/round-92/controls/portals-gkeyfile-cases-r92.json` (16, ≥12 required)

Dir-mode fixtures (portals.conf + kde/gtk/gnome `.portal`, VT = `\x0b`, S = byte 0xE9):

| class | id | fixture essence | oracle (xdp) picks FileChooser/Print/Settings |
|---|---|---|---|
| a | d1-a1-nonutf8-comment-config | `# cafe\xe9` comment + valid `[preferred] default=kde` | kde/default-config |
| a | d1-a2-nonutf8-other-group | `[other] foo=bar\xe9` + valid preferred | kde/default-config |
| a | d1-a3-nonutf8-comment-portal | invalid comment in kde.portal | kde/default-config |
| a | d1-a4-nonutf8-portal-unrelated-key | `Foo=bar\xe9` in kde.portal, else valid | kde/default-config |
| a (control) | d1-a5-nonutf8-config-read-key | invalid `Print` value in `[preferred]` | gtk-last-resort (whole config void — eager read) |
| b | d1-b1-vt-before-group | `\x0b[preferred]` | gtk-last-resort (void) |
| b | d1-b2-vt-before-key | `\x0bdefault=kde` | gtk-last-resort (void) |
| b | d1-b3-vt-before-equals | `default\x0b=kde` | gtk-last-resort (void) |
| b | d1-b4-vt-after-equals | `default=\x0bkde` | gtk-last-resort (void) |
| b (control) | d1-b5-vt-trailing-value | `default=kde\x0b` | gtk-last-resort (void) |
| c | d1-c1-repeated-default | `default=gnome` then `default=kde` | kde (last value wins) |
| c | d1-c2-repeated-settings | `Settings=gnome` then `Settings=gtk` | Settings=gtk (last wins) |
| d | d1-d1-default-empty-locale | `default[]=kde` | gtk-last-resort (plain key `default[]`, no default) |
| d | d1-d2-iface-empty-locale | `FileChooser[]=kde`, `default=gtk` | gtk/default-config |
| d | d1-d3-dbusname-empty-locale | `DBusName[]=…kde`, `default=kde;gtk` | gtk/default-config (kde descriptor lacks DBusName) |
| d | d1-d4-dbusname-c-locale | `DBusName[C]=…kde`, `default=kde;gtk` | gtk/default-config |

Round 90's 229-case set contains none of (a)(b)(d) inputs and its only repeated-key case (g06) cannot see key order, confirming M91-1 §26. Two targeted probes (not in the set, for calibration): invalid byte in a `[preferred]` unknown key (`foo=bar\xe9`) → oracle voids the whole config (eager per-key read at config load, unlike gio's lazy per-type read in mado-mime); invalid byte in `[other]` group or unrelated `.portal` key → oracle loads normally. This is why class (a) for portals is observable only on comment/unread lines — on a read `[preferred]` key both old and new code void the config (control a5).

## Base tool (`tools/mado-portals.py`, read-only) on the 16 cases: 8/16

DRAFT manual scoring with the round-90 counter's `outcomes` (patched materialise only):
- wrong (8): a1,a2,a3,a4 (invalid UTF-8 in comment/other-group/unread key voids whole file via `open(...,encoding="utf-8")` → `UnicodeDecodeError` → config/descriptor skipped; oracle loads), b1,b2,b3,b4 (`\v` stripped as whitespace so the line parses; oracle voids config).
- ok (8): a5 (eager void coincides), b5, c1, c2, d1,d2,d3,d4 (coincide in effect — see §(c)/(d) below).

## Ported candidate — `.ufo/waves/round-92/build/mado-portals.d1.py` (sha256 `89039e30…91d3`)

Copied `tools/mado-portals.py` and ported exactly the four `tools/mado-mime.py` rules (no other changes):
- (a) `mado-mime.py:178-185,210-211,237-239` — `_check_utf8` + `_check_utf8()` as first statement of `string_list`/`plain_string`; file read as bytes `decode("utf-8","surrogateescape")` (`mado-mime.py:230-239`). Net effect here: parse no longer fails at load; the read of a key whose value is invalid UTF-8 raises per-key. Callers already handle that per-key: `load_portal` skips the descriptor (invalid `Interfaces`/`DBusName`), `load_config_file` returns `None` on the first invalid `[preferred]` list (matches oracle eager void, incl. probes). `Encoding` check now `value.encode("utf-8","surrogateescape")` (`mado-mime.py:162`).
- (b) `mado-mime.py:87` — `ASCII_SPACE = " \t\n\f\r"` (`\v` excluded); used for leading-strip, key `rstrip`, value `lstrip` (`mado-mime.py:138,157,160`).
- (c) `mado-mime.py:170-174` — plain `grp[key] = value` (removed `grp.pop(key,None)`); last value wins, first position kept.
- (d) `mado-mime.py:164-169` — `loc = key[key.rindex("["):] …; if len(loc)>2 and loc[1:-1].lower()!="c": continue` (so `x[]` and `x[C]` are plain keys; `x[en]` dropped under `LC_ALL=C`).

Results: **16/16 ok** on the new cases (`python3 score.py candidate`, exit 0). `--selftest` 22/22, rc 0.

## Frozen round-90 set (`portal-cases-r90.json`, 229 cases): 229/229 before and after

- DRAFT counter run (`--draft-tool candidate`, `--fresh 120`, empty scratch mutants file): `MADO_PORTAL_ROUTING: DRAFT_TARGET_MISSED … cases=229 correct=229 blind=66/66 fresh=120/120 fresh_seed=2298715696 mutants=0 killed=0 r12_rule_correct=70 host_table_correct=10 do_nothing_correct=35 base_correct=229 … tool_sha256=89039e30…` rc 3 (MISSED only because `killed==0` of the `{"mutants":[]}` scratch file — not a case failure). Direct `outcomes` on the frozen set: base 229/229, candidate 229/229.
- **Blocked for a real mutant leg:** 8 frozen mutants no longer apply, because their `find` is the old bytes being removed: M03,M27,X05 (`lstrip/rstrip(" \t\n\v\f\r")`), X04 (leading-strip loop), M37 (`value.encode("utf-8")`), M31 (`grp.pop` dance), X06 (old `[` locale comment). A frozen-mutant run against the ported tool hits `SETUP_ERROR "find occurs 0 times"` (or refuses, depending on counter version). The L1 must regenerate those `find` strings against the new file (or re-target to `ASCII_SPACE`) — expected kill is on the new cases (a1–a4, b1–b4) and old cases that touch whitespace/locale; I did not fabricate mutant files.

## (c) and (d) — honest negative results

- (c) Repeated-key first-position kept (port + comment verbatim from `mado-mime.py:170-174`) but is **not observable** through portals routing on my probes: `load_config_file`/`find`/`find_all` look keys up by name, never iterate key order; c1/c2 ok identically before/after (last value wins both ways). Keeping the port is still correct for any future ordered iteration (e.g. a Settings-accumulating reader) and costs nothing; no case can kill an order-mutant here without changing a consumer. Worth the L1 knowing before freezing a mutant on it.
- (d) `[]`-as-plain-key is observable only in the negative sense: d1–d4 all end in gtk fallback/default-config **identically before and after** (old code dropped the key entirely; new code keeps `default[]`/`DBusName[]` which never match `default`/`DBusName`, and keeps `x[C]` which likewise never matches). The port is the correct GLib rule and is proved by the parser-level fact that `parse_keyfile("[preferred]\ndefault[]=kde")` now yields key `default[]` instead of none; end-to-end picks coincide. (A usable distinguisher would need a consumer that enumerates keys — xdp/web doesn't.)

## Risks / for L1

1. Classes (a)+(b) are now 8/8 killed end-to-end; (c)/(d) are rule-correct but effect-invisible — do not claim them as measured coverage until a consumer iterates keys.
2. Round-90 oracle/counter strict-UTF-8 materialise (above) must be patched before freezing; case file stores surrogates + `host_tail_sha256`/`oracle_binary_sha256` pins.
3. 8 round-90 mutants' `find` strings are stale against any port — regenerate before the measured run.
4. No `tools/` edit made; no git/jj mutation; no install (pacman paused; none needed). Scratch `/fast/scratch/hyaku/mado-r92/R92MExecD1` (label_run/score scripts, probe JSONs) — cited outputs copied above; scratch deleted on exit by yield wrapper (this text was written before exit; if a stray dir remains it is my defect).

Report: .ufo/waves/round-92/w1/R92MExecD1.md
