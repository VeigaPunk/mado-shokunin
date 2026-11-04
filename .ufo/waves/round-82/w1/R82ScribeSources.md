# R82ScribeSources — the two new sources, opened and pinned (round 82, wave 1)

Seat: scribe-sources. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Freeze
`780c30fcae12d74ce8ab3b871a0888696c2415d9`, base `6ea2386d49318a5f223097c78b5fe79c31b064f8`.
Read-only fetches; no registry append; no instrument, control or receipt edited. Session clock at
close: 2026-11-04T13:35Z.

## 1. Behaviour — what was opened and where it is pinned

Both sources were fetched from primary endpoints, stored under
`.ufo/waves/round-82/fetch/`, and listed in `.ufo/waves/round-82/fetch/sha256-r82.txt` with
lane-relative paths.

| id | endpoint | HTTP | bytes | sha256 | pinned as |
|---|---|---|---|---|---|
| S481 | `https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/2b8d43325b7012cc3f9b55c08d26e50e42beac7d/unstable/wlr-layer-shell-unstable-v1.xml` | 200 | 19326 | `87e0b9c837aecd6977f76f3c47d73088b7159871f5d979dc1840f6cadb5e2ed8` | `S481.xml` |
| S482 | `https://raw.githubusercontent.com/KDE/kstatusnotifieritem/v6.2.0/src/org.kde.StatusNotifierWatcher.xml` | 200 | 1151 | `19df7f185c6be476134d80ec886fcecbd80ff5b377d5349b84b951119d3eab49` | `S482.xml` |
| S483 (not a row of this seat) | `https://www.freedesktop.org/wiki/Specifications/StatusNotifierItem/StatusNotifierWatcher/` | 200 | 6395 | `f22928e1f6010838fdb416025dad15c6ad68b22b2300d459bf6b6c61e3288069` | `S482.html` |

Access date for all three: 2026-11-04.

`2b8d4332` (2024-01-26, "layer-shell: add set_exclusive_edge") is the **last commit touching the
file** in the wlr-protocols history (`gitlab API …/repository/commits?path=unstable%2Fwlr-layer-shell-unstable-v1.xml`),
and the file at that commit is identical to `master` today. `v6.2.0` is a live tag in
`KDE/kstatusnotifieritem`; the XML there is identical to `v6.31.0`, `master`, and plasma-workspace's
`xembed-sni-proxy/` copy, and its last change is `506bdfca` (2014-03-21).

Both registry rows are drafted in `.ufo/waves/round-82/sources-rows-r82.md`, exact 11-column schema,
no literal or escaped pipe in any cell (validated by splitting every row: 11 cells each, zero `\|`).
`corpus/SOURCES.md` was **not** touched: it already carried S481/S482/S483 at `:433-435` before this
seat read it (mtime 10:29:37, sha256 `2ca8fcd9…`), so the draft is a re-derivation and delta.

## 2. Gates

- `sha256sum -c .ufo/waves/round-82/fetch/sha256-r82.txt` **from the lane root** → 3/3 `OK`, rc 0
  (`S481.xml`, `S482.xml`, `S482.html`).
  Note: the manifest stores lane-relative paths; running `-c` inside `fetch/` fails with
  "No such file or directory". That is a path convention, not a bad digest.
- `cmp` empty for every byte-identity claim: S481 == gitlab `@2b8d4332` == Hyprland v0.56.2
  `@efb5099` == held `.ufo/waves/round-79/fetch/S460.bin`; S482 == `v6.2.0` == `v6.31.0` ==
  `master` == plasma-workspace `@31242aad` `xembed-sni-proxy/`.
- Quotes re-read from the pins: `set_size` `:122-137`, zero clause `:128-129` (22 words ≤ 25), anchor
  rule `:130`, default `:131`, double-buffered `:133`; `configure` `:327-353` (hint `:341-345`, zero
  `:347-348`); interface `:3`, methods `:6-8`/`:10-12`, property `:17-19`, `:21`, `:23`, signals
  `:28-40`.
- Sizes re-read with `stat -c '%s'` → 19326 / 1151 / 6395 B.

## 3. Touched surfaces (all writes)

- `.ufo/waves/round-82/fetch/S481.xml`, `S482.xml` — pre-existing at 10:27:54, verified only.
- `.ufo/waves/round-82/fetch/sha256-r82.txt` — appended one line for `S482.html` (now three lines).
- `.ufo/waves/round-82/fetch/S482.html` — **created** from the page fetch whose digest equals the one
  already cited by the committed S483 row; the file was absent at 10:28.
- `.ufo/waves/round-82/sources-rows-r82.md` — created (this seat's row draft).
- `.ufo/waves/round-82/w1/R82ScribeSources/` — this report plus `evidence/`
  (`statusnotifieritemhost.cpp`, `statusnotifierwatcher.cpp`,
  `statusnotifierwatcher-CMakeLists.txt`, `org.kde.StatusNotifierWatcher-v6.31.0.xml`,
  `sha256-support.txt`). Evidence hashes: `statusnotifieritemhost.cpp` `55bb554f…`,
  `statusnotifierwatcher.cpp` `95f11d77…`, `statusnotifierwatcher-CMakeLists.txt` `075dfaa6…`,
  `org.kde.StatusNotifierWatcher-v6.31.0.xml` `19df7f18…`.
- Scratch `/fast/scratch/hyaku/mado-r82/R82ScribeSources/` — fetched probes and API replies, not
  part of the lane; removed at close by the seat's trap.

Nothing was written to the fleet repo, a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`,
`.scratch/`, `/tmp`, or any `PATH` directory.

## 4. What each source licenses, and what it does not

**S481** (protocol text; the file carries its own permissive wlroots-style grant at `:3-16`, "use,
copy, modify, distribute, and sell … provided that the above copyright notice appear in all copies",
`:6-10`). It licenses four sentences only: a zero `set_size` dimension is a request for the
compositor to assign and report (`:128-129`); omitting a dimension requires opposite-edge anchors
(`:130`); both default to 0 (`:131`); a zero/smaller `configure` payload is a hint and a zero one
means the client decides (`:341-348`). It does **not** license: that the assigned size is the
client's allocation (S464), that the allocation is the band or the exclusive zone (S464's
`current_allocation`, `set_exclusive_zone` `:152-188`, `set_margin` `:196`), that the arranged box
equals the band (S470), that a config `height = 0` is such a request, or that waybar sends 0 on this
host — no host fact at all. In particular the `configure` sentence `:347-348` is **not** `set_size`'s
clause; the two messages run in opposite directions.

**S482** (interface declaration). It licenses exactly the names, signatures and arrows it contains:
`org.kde.StatusNotifierWatcher` (`:3`), `RegisterStatusNotifierItem` and `RegisterStatusNotifierHost`
with one `s` in-arg each (`:6-8`, `:10-12`), `RegisteredStatusNotifierItems` `as` read (`:17-19`),
`IsStatusNotifierHostRegistered` `b` and `ProtocolVersion` `i` (`:21`, `:23`), four signals
(`:28-40`). It is the file plasma-workspace's watcher build generates its adaptor from
(`statusnotifierwatcher/CMakeLists.txt:3-4`). It does **not** license: the bus name
(`statusnotifieritemhost.cpp:28` and `:86` at plasma-workspace `31242aad`), the object path
(`statusnotifierwatcher.cpp:27`, `/StatusNotifierWatcher` — absent from the XML), any implementation
behaviour (`RegisterStatusNotifierHost` is `Q_UNUSED`, `:92-95`; `IsStatusNotifierHostRegistered`
returns `true` always, `:97-100`; `ProtocolVersion` returns 0, `:102-105`), the existence or owner of
a running watcher, the property's value, or that the freedesktop wiki's
`org.freedesktop.StatusNotifierWatcher` is the same service.

**Licence of S482's file.** No header (line 1 is the DOCTYPE) and no `.license` sidecar in the tree
listing; the repository carries `LICENSES/LGPL-2.0-or-later.txt` and `LICENSES/CC0-1.0.txt`, but
which applies to this path is not established from the bytes I opened. The pin is a 1151 B citation
copy of an interface declaration; the row is not a licence grant.

## 5. Findings

- **D1 (real, fixed by this seat's draft, registry still carries it).**
  `corpus/SOURCES.md:433` cites "`set_size` `:122-142`" — the request is `:122-137`; `:139` opens
  `set_anchor` and `:142` is inside its description. The same row's quote cell is the `configure`
  event's sentence at `:347-348`, while its teaches cell says "what a zero width/height in
  `set_size` means". The pinned bytes have `set_size`'s own zero clause at `:128-129` ("the
  compositor will assign it"), the reciprocal `configure` clause at `:347-348` ("the client should
  decide"), and the anchor requirement at `:130`. Suggested fix is in the draft row: span
  `:122-137`, quote `:128-129`, `configure` `:327-353` named separately. The round-82 lesson's own
  precision note (`corpus/lessons/round-82.md:80-84`) reaches the same conclusion from the same
  bytes.
- **D4 (real, frozen, report-only).** `.ufo/waves/round-82/claims-declaration-r82.md:37` cites
  `set_size` `:116-123`. In the pinned bytes `:116-119` is the `layer_surface` unmapping description,
  `:120` closes that description and `set_size` opens at `:122`; the citation is not re-derivable
  from `fetch/S481.xml`. The claim's substance is unaffected; a seat may not edit the declaration, so
  this is named for the L1.
- **D2 (real, repaired).** `corpus/SOURCES.md:435` cites
  `.ufo/waves/round-82/fetch/S482.html` (6395 B, `f22928e1…`); at 10:28 the file did not exist and
  the manifest had two entries. The round-82 lesson now records the same absence at
  `corpus/lessons/round-82.md:86` ("pin the page or drop the pointer"). This seat fetched the page,
  whose digest equals the cited one, wrote it to `fetch/S482.html`, and appended the manifest line;
  `sha256sum -c` is 3/3. The page's
  head does say `There will be a single org.freedesktop.StatusNotifierWatcher service instance
  registered on the session`, so S483's rejection reason is supported verbatim. The file name is
  the third source's bytes under an S482-ish name; a rename to `S483.html` must move the row's
  anchor cell and the manifest line together.
- **D3 (seat-brief defect, report-only).** The brief's fallback URL "the vendor copy in the pinned
  Hyprland tree at `6ea2386d49318a5f223097c78b5fe79c31b064f8`" returns HTTP 404:
  `6ea2386d…` is the **lane's base revision**, not a Hyprland commit. The lane's actual Hyprland pin
  is `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2), whose `protocols/wlr-layer-shell-unstable-v1.xml`
  is live and byte-identical (HTTP 200, 19326 B, `87e0b9c8…`).
- **Precision notes (not defects).** (a) `SKILL.md` does not contain the string `S482`; the S482
  row's `used-by` is an attribution, and the round's literal citation is
  `quality/counters/c2-r82-runbook.py:17`. (b) The knowledge entry quotes `set_size`'s clause as
  `(S481:128-131)` where the sentence ends at `:129`; `:130-131` is the anchor rule and the default.
  (c) S460, the same bytes as S481, is filed `kind=spec` / `recheck=180d` while the committed S481
  row is `kind=code` / `on-release`; the draft row uses `spec` / `on-change` and says why.

## 6. Verification actually run

Read-only only: `curl` fetches (HTTP codes and sizes above), GitLab/GitHub API replies for commit
history and tags, `sha256sum`, `cmp`, `stat`, `python3` for row-cell validation and JSON, `awk`/`sed`
for line-number reads. No `busctl`, no `hyprctl`, no D-Bus call, no host probe, no build, no test
suite, no `task` dispatch, no commit or other mutating git verb.

Commands of record:

```
sha256sum -c .ufo/waves/round-82/fetch/sha256-r82.txt     # from the lane root → 3 OK, rc 0
cmp .ufo/waves/round-82/fetch/S481.xml .ufo/waves/round-79/fetch/S460.bin   # empty
cmp .ufo/waves/round-82/fetch/S482.xml <v6.31.0 fetch>                      # empty
```

## 7. Tooling

None installed, upgraded or removed. No `pacman` transaction was attempted (host pause respected);
no `uv tool`, `npx` or binary download was needed.

## 8. Limits

- Today's network reads are the only observation of the URLs; the pins plus their digests are the
  offline re-check. No mirror was made.
- The two rows assert document and code facts only. Nothing here says a watcher is running, who owns
  `org.kde.StatusNotifierWatcher`, or what `busctl --user introspect` prints on this machine.
- `S482.html` is the S483 source's bytes, written under the committed row's filename.
- `corpus/SOURCES.md` was already carrying the rows when this seat opened it; no append was made and
  no claim of one is implied.

## 9. Status

**Defect, named with file:line.** `corpus/SOURCES.md:433` cites `set_size` `:122-142` (the request
ends `:137`) and uses the `configure` clause `:347-348` as the row's `set_size` quote; the pinned
bytes say `set_size` `:122-137` with its zero clause at `:128-129`. The frozen declaration's
`set_size` `:116-123` (`.ufo/waves/round-82/claims-declaration-r82.md:37`) is likewise not
re-derivable from the pin. Repaired: `corpus/SOURCES.md:435` cited an absent `fetch/S482.html` (the
lesson records it at `corpus/lessons/round-82.md:86`); the file is now materialized with the cited
digest `f22928e1…` and the manifest verifies 3/3.

STATUS: defect
