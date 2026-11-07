# Round-96 SKILL.md and PROVINCE.md diff draft — `tools/mado-mimetext.py`

Seat `R96MScribeEntry`, 2026-11-07. Exact text, in the shape of the tables/refinements already in
the files; the L1 applies it. Pipes inside code spans are escaped as `\|`, exactly as the
neighbouring rows do (an unescaped `|` would split the cell).

## 1. SKILL.md — tool-registry row

**Where.** The tool registry table that opens at `SKILL.md:786` (`| name | gate/probe | entry
command | verdict map | self-test command / spelling | pinned-value path | write scope | owner |`);
insert after the last row of that table, `mado-r95-mimesniff` (`SKILL.md:886`), so the mime tools
stay together. The row has the same eight content cells; the owner cell is empty like its
neighbours.

**Exact row text** (one physical line):

```
| mado-mimetext | probe | `python3 -I tools/mado-mimetext.py [--name NAME \| --names-from-files] [--data-home DIR \| --data-home-unset] [--data-dirs COLON_LIST \| --data-dirs-unset] [--home DIR \| --home-unset] [--json] FILE ...` (needs `tools/mado-mimeglob.py` beside it; text database mode only) | 0 every file answered (`MADO_MIMETEXT: <type> uncertain=<0\|1> name=<escaped\|-> file=<escaped>` plus one `MADO_MIMETEXT_DIRS: mode=text\|none dirs=<comma list>` line; no `--name` = filename NULL); 2 setup error (no FILE, unreadable FILE, both name options); 3 `MADO_MIMETEXT: UNSUPPORTED <reason>` per file (a loadable `mime.cache` in any reachable directory; round 95 owns that answer) | `python3 -I tools/mado-mimetext.py --selftest`; prints `MADO_MIMETEXT_SELFTEST: checks=N failed=0` on the landed tool (N >= 18) and exits 0, 1 on any failed check; a failing check prints `MADO_MIMETEXT_SELFTEST_FAIL: <label>` | `corpus/knowledge/mime-textdb-magic-r96.md` (text-mode magic per `mime/magic`: the 12-byte gate, sections and matchlets, the whole-section drop, priority order with ties, the indent tree and its jump blind spot, the compare's bounds rule, priority 0, `~0`, the fallback and the text name step; spec departures; §6 limits, §9 frozen cases); model source xdgmimemagic.c (S524), spec §2.5 (S525), xdgmime.c (S505), xdgmimeint.c (S520), gcontenttype-fdo.c (S521) | reads `mime/magic` (and, for the name step, `mime/globs2`/`mime/globs`) under the xdgmime data roots it is given and the FILEs named; runs no program but ctypes' libc lookup (inherited from mimeglob), writes nothing; a reachable `mime.cache` is refused, not read | |
```

**Why the verdict map says "text database mode only".** The tool answers the zero-cache state and
refuses cache mode (exit 3); `tools/mado-mimesniff.py` answers the cache state, so the two rows sit
side by side without overlapping surfaces.

## 2. PROVINCE.md — refinement paragraph (the shape used by rounds 94/95)

**Where.** At the end of the round-refinement block (after the Round-95 C1/C2 refinements,
`PROVINCE.md:552-561`).

**Exact text** (three lines, appended as one paragraph):

```
**Round-96 refinement (C1) — file bytes → MIME type in the TEXT database mode (read-only); no new write surface.**
`tools/mado-mimetext.py` reads the text `mime/magic` file (its `MIME-Magic` sections, matchlets,
word sizes and ranges, plus round 94's name step from `mime/globs2`/`mime/globs`) under the xdgmime
data roots it is given and the files it is asked to sniff (S524, S525, S505, S520, S521, S522), and
writes nothing; it never runs `update-mime-database`, never edits `~/.local/share/mime`, and refuses
(exit 3) any state where a loadable `mime.cache` exists in a reachable directory — that state is
round 95's `tools/mado-mimesniff.py`. Its callers are the same GIO `standard::content-type` path as
round 95, but only on a host whose reachable directories hold no loadable cache; `xdg-open` on
Hyprland still uses `file(1)` (revenger's ground) and is outside it.
```

## 3. PROVINCE.md — inventory-table row (optional; only if the L1 wants the table backfilled)

The Round-23 inventory table (`PROVINCE.md:23`, columns `Tool | Reads | Writes | Owner and adjacent
lanes`) has no row for `tools/mado-mime.py`, `tools/mado-mimeglob.py` or `tools/mado-mimesniff.py`
— those three were recorded only as refinement paragraphs (r92, r94, r95). Adding one row for the
round-96 tool alone would make the inventory lopsided; the recommendation is the paragraph in §2.
If the L1 prefers a row anyway, the exact text is:

```
| `tools/mado-mimetext.py` | `DIR/mime/magic` (the `MIME-Magic\0\n` text format: sections, matchlets, masks, word sizes, ranges) and, for the name step, `DIR/mime/globs2`/`DIR/mime/globs`, under `$XDG_DATA_HOME/mime` (or `$HOME/.local/share/mime`) and each `$XDG_DATA_DIRS` entry + `/mime`; plus the FILEs named on the command line | nothing — no file is created or modified; stdout only; `--selftest` reads only its own fixtures | mado (desktop MIME classification in the no-cache text mode); revenger owns `file(1)`/libmagic, which this tool never reads; `update-mime-database` and `~/.local/share/mime` stay operator-owned |
```

## 4. What not to change

- `tools/mado-mimesniff.py` and its row: unchanged (cache mode, round 95).
- `tools/mado-mimeglob.py`: unchanged (round 94); the new tool imports it lazily and pins the one
  `spec_from_file_location` call (QUALITY 165).
- No `quality/selftest-kills/` entry for the new tool is claimed this round: a kill-set needs a
  frozen `tool_sha256` and a singleton kill per check label (round-95 gate semantics); that is a
  candidate for a later round, not a byte this seat writes.
