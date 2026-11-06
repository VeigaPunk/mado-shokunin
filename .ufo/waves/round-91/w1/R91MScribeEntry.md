# R91MScribeEntry — round-91 w1 seat report

Seat: R91MScribeEntry (scribe). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Base revision
`cc0381db585cc44c3dfc13ced807409c32c45bb0` (master; read-only `git rev-parse HEAD` → that value).
Assignment: draft the C1 knowledge entry (the L1 lands it at `corpus/knowledge/mime-default-resolution-r91.md`).

## Files written

| path | role | sha256 | bytes |
|---|---|---|---|
| `.ufo/waves/round-91/w1/R91MScribeEntry-draft.md` | the C1 knowledge-entry draft (355 lines) | `c610867ac1516cf46321c1661da71ac8cf724047ef88122ae4ecc769352ecb3f` | 28487 |
| `.ufo/waves/round-91/w1/R91MScribeEntry.md` | this report | (this file) | — |

No other lane file was created or modified. `git status --porcelain` at the end of the seat shows the same three
pre-existing untracked entries (`.ufo/waves/round-91/`, the two counters) as at the start; I did not touch them.

## What the draft contains

Front matter `source:` / `verified-at:` / `recheck:` in the house shape of
`corpus/knowledge/xdg-portal-routing-resolver-r90.md`, then §1 the plane, §2 the search order, §3 the per-directory
file and group order, §4 the default algorithm, §5 the two lists, §6 the desktop-file load rules, §7 the MIME-database
alias/parent rules, §8 eleven quirks (the four the seat spec named plus seven more), §9 a 43-row decision table where
every row carries an L1 case id and gio's label copied verbatim from the case file, §10 how to run `tools/mado-mime.py`
on the host, §11 this host's answers (DRAFT), §12 named limits, §13 unknowns, §14 rejected readings.

Every upstream rule cites a line range of the GLib tag 2.90.1 files, and every one of those files was fetched and
opened by this seat (ten files, sha256 below). Nothing in the draft is marked `[UNVERIFIED]` because everything
cited was read; the two places where behaviour is *inferred* rather than observed are called out in Findings F2.

## Sources fetched and opened (scratch, then hashed)

`curl -fsSL https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/<path>` for the ten paths below; all ten succeeded
(no `FETCH_FAIL` line), `sha256sum` exit 0:

| file | sha256 |
|---|---|
| `gio/gdesktopappinfo.c` | `8e9ce1a8327a2daf6bc16e8dcfb653c482afde7bebc2ca2621747626b5495b0d` (equals the declaration's pin) |
| `gio/gcontenttype-fdo.c` | `8a5b4f475947a9de2e0ca34e60b0dc31f5c56a2d7e0a9fe8cf84002aca8a2d7c` |
| `gio/xdgmime/xdgmime.c` | `afb1c1c1ba726a9fb8d8732f4031f5aa85a67ec3b7a2f989b617e4f4f5282410` |
| `gio/xdgmime/xdgmimecache.c` | `ccda4366a1b3d6feb81c6213fde4885b547189e7cfe612f81799d8c1f298db69` |
| `gio/xdgmime/xdgmimealias.c` | `a1e67ae3604c437b8516d6bc4c67f31afea6fc58393b9afe1c42a8b424111394` |
| `gio/xdgmime/xdgmimeparent.c` | `9c85c35f143b4fbf274ba07f433ad9102270ededf1a95f6cf0cc320d941f35e3` |
| `gio/gio-tool-mime.c` | `40a450ec0ce177e61aae66175c02b3ebdb50aff1ec5ae65732cb800a60b2bd60` |
| `glib/gkeyfile.c` | `e1d1270f6c9881daf8a9f49b41395cbdd8e99fa290212e8530e0bd3df23ff656` (equals S502's pin) |
| `glib/gshell.c` | `640a0d0fbc9c50d0c70eb8f9ff2c4994392515c6174f76ade9292d7500e60442` |
| `glib/gutils.c` | `65086c293646bf83884f56f54bb5e2e872adb28ee77f1223d6d9f095a75e3771` |

Case set read (not re-labelled by me): `.ufo/waves/round-91/controls/mime-cases-r91-l1.json`,
sha256 `42a08f2cc19f137ac591df5f558e0fb2fba65c7471ce0760e2d755497c53e874`, 83 cases; every label in §9 was copied
from that file's `expect` object.

## Runs (every one is DRAFT, per the declaration's draft-scoring rule)

| # | command | result | rc |
|---|---|---|---|
| 1 | ten `curl` fetches of the tag-2.90.1 sources | 10/10 present, digests above | 0 |
| 2 | `sha256sum` of the fetched files | table above | 0 |
| 3 | `sha256sum` of candidate, oracle, generator, counter, `/usr/bin/gio`, `libgio-2.0.so.0.9000.1` | candidate `79645659c5a257e57c90ef4fb25d32bfb134b6f2ed03d3ead6788bdfbb1be160`; oracle `c3a13e26…`; generator `e1f3d53e…`; counter `f2b23fb8…`; gio `d2164260…`; libgio `b38001cc…` | 0 |
| 4 | `python3 -I .ufo/waves/round-91/build/mado-mime.c1.py --selftest` | `MADO_MIME_SELFTEST: checks=17 failed=0` | 0 |
| 5 | candidate `--json` + `gio mime <TYPE>` (one argument each) over 537 types (union minus one) | 535 exact, 2 shape-only (`[]` vs no lists) | 0 |
| 6 | same comparison over the full 538-type union (script in scratch) | `default_agree=538`, `lists_agree_where_printed=536`, `bad=[]`, `no_default_shape_only=2` (`application/uproject`, `x-scheme-handler/zwork`) | 0 |
| 7 | `git cat-file -e cc0381db:tools/mado-mime.py` and `…:corpus/knowledge/mime-default-resolution-r91.md` | both `does not exist in …` — the tool and the entry are absent at base | 128 each |
| 8 | `git rev-parse HEAD`; `git status --porcelain`; `git ls-tree -r --name-only cc0381db corpus/knowledge` | `cc0381db…`; three untracked round-91 paths; 111 knowledge files | 0 |
| 9 | `grep -c '='` + `sha256sum` on the four host inputs; `mime.cache` header `struct.unpack('>HH', …)` | 56 / 149 / 522 keys; digests in §11 of the draft; `mime.cache` version `(1, 2)`, size 207520 | 0 |
| 10 | `pacman -Q glib2 shared-mime-info desktop-file-utils` (read-only) | `glib2 2.90.1-1`, `shared-mime-info 2.5.1-2`, `desktop-file-utils 0.28-1` | 0 |
| 11 | `grep` of the candidate for write-mode `open(` and for `subprocess`/`os.system` | one write-open, inside `--selftest`'s temp fixture helper; no subprocess call | 0 |

No counter was run (I have no mutants file and this seat does not measure); no receipt was written; nothing was
written under `.ufo/waves/round-91/receipts/`.

## Findings

**F1 — gio cannot label the two lists when there is no default (documentation hazard, not a defect).**
`gio/gio-tool-mime.c:115-152`: the registered/recommended printing sits inside the `else` of a found default. The
case schema encodes this as `null` for all three fields (e.g. case `l11-defaults-list-added-ignored`: `null`;
case `l08-desktop-specific-added-ignored`: `null`). Consequence for the entry: §1 and §12 say the lists are
unobservable without a default, and the DRAFT sweep's only two mismatches out of 538 types
(`application/uproject`, `x-scheme-handler/zwork`) are exactly this shape — the tool prints `[]`, gio prints
nothing, the answer is the same. The counter must keep mapping `[]` onto `null`; the draft states the answer, not
a labelled list.

**F2 — [INFERENCE] the alias-chain case reaches its second hop through the type-list BFS, not through unalias.**
`_xdg_mime_unalias_mime_type` is a single lookup (`gio/xdgmime/xdgmime.c:735-747`; cache path
`xdgmimecache.c:1051-1062`), yet case `x11-alias-chain-not-followed` labels `app/x` as
`default a.desktop; registered [a.desktop,b.desktop]; recommended []` with `aliases` = `app/x app/y`,
`app/y app/z` and cache rows `app/z=a.desktop`, `app/y=b.desktop`. Mechanism I read off the sources: the type
list is seeded with `unalias(app/x)=app/y` and then grown with `_g_unix_content_type_get_parents(element)`, whose
first entry is `unalias(element)` (`gcontenttype-fdo.c:83-110`, used at `gdesktopappinfo.c:4552-4588`) — a second
hop to `app/z`; and cache keys are unaliased when stored (`gdesktopappinfo.c:839`), so `app/y=b.desktop` lands
under `app/z` and both ids come from that one key. The label is gio's own (copied from the case file); the
*mechanism sentence* is my inference and is written as such in §7, not as an observation.

**F3 — a `subclasses`/`aliases` line without a final newline loses the last character of the target.**
`gio/xdgmime/xdgmimeparent.c:127-138` (and `xdgmimealias.c:120-131`) do `sep[strlen (sep) - 1] = '\000'`
unconditionally. Case `x13-file-without-final-newline-chops` ships `subclasses` = `app/x app/zz` (no trailing
newline) and labels `default a.desktop; registered [a.desktop]; recommended []` — the parent became `app/z`, which
is the key carrying `a.desktop`. Reproducing input is that fixture; the label is gio's.

**F4 — `Encoding=ISO-8859-1` voids a whole `mimeapps.list`, not just a key.**
GKeyFile rejects a first-group `Encoding=` value other than `UTF-8` (`glib/gkeyfile.c:1768-1782`), and a
`mimeapps.list` has no other group, so that group *is* the start group. `is_invalid_key_error`
(`gdesktopappinfo.c:1886-1892`) lets only `GROUP_NOT_FOUND`/`KEY_NOT_FOUND` through, so the loader skips the file
(`:909-913`). Case `k06-encoding-latin1-voids` labels `a.desktop; [a.desktop]; [a.desktop]` — the cache's
`a.desktop`, not the file's `c.desktop`. Case `k02-bad-escape-skips-key-only` is the contrast: an invalid escape in
one *value* kills that key alone, because `get_string_list` returns NULL for the key while the file load succeeded.

**F5 — `registered` and `recommended` genuinely differ once an ancestor contributes.**
Case `x04-parent-registered-not-recommended` labels `b.desktop; [b.desktop,a.desktop]; [b.desktop]`; the host sweep
shows the same at `text/x-c` (`libreoffice-writer.desktop` registered through `text/plain`, absent from
`recommended`). Any check that treats the two lists as one is wrong.

**F6 — every gio output I compared came from the read form only.** Every host call was `gio mime TYPE` with exactly
one argument; no `gio mime TYPE HANDLER`, no `xdg-mime`, no `update-desktop-database`, no application launch.

## Limits of this seat's evidence

- The host section (§11) is a DRAFT run of the candidate, not the frozen tool; it carries no receipt and no
  measurement. The declaration forbids writing under `.ufo/waves/round-91/receipts/`, and I wrote none.
- I did not re-label any case with the oracle; labels are the case file's, read at the digest above.
- The entry's rule set is read-only knowledge: it does not prove any host write path, launch path or portal path.
- §11's environment and input digests were read once, in this shell; a session started with a different
  `XDG_CURRENT_DESKTOP` would be a different fixture.

## Process notes (disclosed, no effect on the work)

- One command-substitution fallback in a counting pipeline created an empty `/tmp/.x` and removed it in the same
  command (`rm -f`); nothing was read from or written to it. This is the seat's one deviation from the
  "never hardcode /tmp" rule.
- One `edit`-style replacement in a batch reported `MISS 0` (a wrapped line did not match); the affected sentence
  was corrected afterwards by a targeted `edit`. No stale citation remains (`grep` for `:345-353`, `:313-321`,
  `:4735`, `:1764` over the draft returns nothing).
- Scratch `$S=$HYAKU_SCRATCH/mado-r91/R91MScribeEntry` (sources + the two comparison scripts) was removed on exit;
  nothing cited from it lives only there — every cited digest is in this report and in the draft.

## Out of scope (for the L1)

- Registering the proposed SOURCES row (next free id after S503) for the ten GLib files.
- Landing the entry at `corpus/knowledge/mime-default-resolution-r91.md` and replacing `verified-at:` with the
  measured receipt and the frozen case-set digest.
- Adding the `corpus/README.md` index row and any PROVINCE/SKILL/SCORECARD mention of the new capability.

## Installs

None. No pacman transaction, no `uv tool install`, no binary placed in a PATH directory.
