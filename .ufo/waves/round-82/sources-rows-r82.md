# SOURCES.md rows — round 82 (seat R82ScribeSources)

Prose draft for the L1. Freeze `780c30fcae12d74ce8ab3b871a0888696c2415d9`, base
`6ea2386d49318a5f223097c78b5fe79c31b064f8`. Two rows (S481, S482), exact 11-column schema, no
literal or escaped pipe in any cell.

**Read this first.** When this seat opened the lane at 10:28 the registry already carried S481,
S482 and S483 at `corpus/SOURCES.md:433-435`, and `fetch/` already held `S481.xml` and `S482.xml`
with a two-line `sha256-r82.txt` (both written 10:27:54). This file is a re-derivation and a
cell-by-cell delta, **never an append** — I did not write `corpus/SOURCES.md`. The bytes were
verified independently against fresh fetches before any row prose was settled.

## 1. The two rows

| S481 | wlr-protocols — unstable/wlr-layer-shell-unstable-v1.xml (`set_size`, `configure`) — https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/2b8d43325b7012cc3f9b55c08d26e50e42beac7d/unstable/wlr-layer-shell-unstable-v1.xml | spec | A | mado bar plane: what a zero width or height in `set_size` asks for, and what a zero in the compositor's `configure` hands back, so a declared dynamic band is read as the client's own allocation rather than an unknown (round-82 C1) | request `set_size` `:122-137`, its zero clause `:128-131`; the reciprocal `configure` clause `:347-348` inside the event `:327-353` (fetched 2026-11-04, sha256 87e0b9c837aecd6977f76f3c47d73088b7159871f5d979dc1840f6cadb5e2ed8, 19326 B; `.ufo/waves/round-82/fetch/S481.xml`; byte-identical to the Hyprland v0.56.2 vendored copy at efb5099 and to the held S460 pin) | `If you pass 0 for either value, the compositor will assign it and inform you of the assignment in the configure event.` (at `:128-129`) | mined | 2026-11-04 | on-change | corpus/knowledge/bar-footprint-allocation-r82.md |
| S482 | kstatusnotifieritem v6.2.0 — src/org.kde.StatusNotifierWatcher.xml — https://raw.githubusercontent.com/KDE/kstatusnotifieritem/v6.2.0/src/org.kde.StatusNotifierWatcher.xml | code | A | mado tray plane: the watcher's interface name, its two register methods and its read property, so the round-82 runbook rows bind the KDE-owned spelling and read the introspect census it prints (the freedesktop wiki names `org.freedesktop.StatusNotifierWatcher`, a different namespace) | whole file 1151 B: interface `:3`, methods `:6-8` and `:10-12`, `RegisteredStatusNotifierItems` `:17-19` (fetched 2026-11-04, sha256 19df7f185c6be476134d80ec886fcecbd80ff5b377d5349b84b951119d3eab49, 1151 B; `.ufo/waves/round-82/fetch/S482.xml`; byte-identical at v6.31.0, at master, and at plasma-workspace HEAD 31242aad `xembed-sni-proxy/`; plasma-workspace `statusnotifierwatcher/CMakeLists.txt:3-4` generates the watcher adaptor from this file) | `<interface name="org.kde.StatusNotifierWatcher">` at `:3`; `<method name="RegisterStatusNotifierItem">` at `:6`; `<property name="RegisteredStatusNotifierItems" type="as" access="read">` at `:17` | mined | 2026-11-04 | on-release | SKILL.md |

`source:` ids as the round's `corpus/knowledge/bar-footprint-allocation-r82.md` writes them: `S481`
(new), with `S464`, `S470` and the held `S460` (byte-identical to S481); `S482` is the C2 ground,
cited by `quality/counters/c2-r82-runbook.py:17`.

## 2. Provenance of the fetched bytes (access date 2026-11-04)

| id | URL fetched | bytes | sha256 | located quote (line) |
|---|---|---|---|---|
| S481 | https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/2b8d43325b7012cc3f9b55c08d26e50e42beac7d/unstable/wlr-layer-shell-unstable-v1.xml | 19326 | 87e0b9c837aecd6977f76f3c47d73088b7159871f5d979dc1840f6cadb5e2ed8 | `If you pass 0 for either value, the compositor will assign it and inform you of the assignment in the configure event.` (`:128-129`, 22 words) |
| S482 | https://raw.githubusercontent.com/KDE/kstatusnotifieritem/v6.2.0/src/org.kde.StatusNotifierWatcher.xml | 1151 | 19df7f185c6be476134d80ec886fcecbd80ff5b377d5349b84b951119d3eab49 | `<interface name="org.kde.StatusNotifierWatcher">` (`:3`) |

Pinned files: `.ufo/waves/round-82/fetch/S481.xml` (frozen generation of the protocol) and
`.ufo/waves/round-82/fetch/S482.xml` (interface declaration). Manifests: `.ufo/waves/round-82/fetch/sha256-r82.txt`.

Byte-identity checks made today, all `cmp`-empty:

- S481: gitlab `@2b8d4332` == Hyprland v0.56.2 vendored copy `@efb5099` == held `.ufo/waves/round-79/fetch/S460.bin`. `2b8d4332` (2024-01-26, "layer-shell: add set_exclusive_edge") is the last commit touching the file in the wlr-protocols history, and the file there is identical to `master` today.
- S482: kstatusnotifieritem `v6.2.0` == `v6.31.0` == `master` == plasma-workspace `xembed-sni-proxy/org.kde.StatusNotifierWatcher.xml` at HEAD `31242aad`. The file's last change is `506bdfca` (2014-03-21).

## 3. Gate-table quotes (≤25 words, located)

| row | located quote | file:line | what it licenses / does not |
|---|---|---|---|
| S481 | `If you pass 0 for either value, the compositor will assign it and inform you of the assignment in the configure event.` | `.ufo/waves/round-82/fetch/S481.xml:128-129` (22 words; the request is `:122-137`) | asks the compositor to assign an omitted dimension and report it; it does **not** say the client decides, nor that the allocation is the band |
| S481 | `If the width or height arguments are zero, it means the client should decide its own window dimension.` | `.ufo/waves/round-82/fetch/S481.xml:347-348` (inside `<event name="configure">` `:327-353`) | the reciprocal clause: a zero the compositor sends back hands the dimension to the client; it belongs to `configure`, not to `set_size` |
| S481 | `You must set your anchor to opposite edges in the dimensions you omit; not doing so is a protocol error.` | `.ufo/waves/round-82/fetch/S481.xml:130` | a zero dimension is legal only on a both-edges-anchored axis; it does not say which edge owns the exclusive zone |
| S482 | `<interface name="org.kde.StatusNotifierWatcher">` | `.ufo/waves/round-82/fetch/S482.xml:3` | the interface name only; the bus name and object path are licensed by the implementation files in §5 |
| S482 | `<method name="RegisterStatusNotifierItem">` and `<property name="RegisteredStatusNotifierItems" type="as" access="read">` | `.ufo/waves/round-82/fetch/S482.xml:6` and `:17` | the declared members the census prints; not their behaviour on a running watcher |

## 4. What each source licenses — and what it does NOT

### S481 (wlr-layer-shell protocol XML)

**Licenses.** The file carries its own permissive wlroots-style grant at `:3-16`: "Permission to
use, copy, modify, distribute, and sell this software and its documentation for any purpose is
hereby granted without fee, provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in supporting documentation"
(`:6-10`), with the warranty disclaimer at `:13-16`. The pin keeps the whole file, notice included,
so the copy is compliant. Substantively it licenses exactly four sentences:

1. a zero width/height in `set_size` is a request for the compositor to assign that dimension and
   report the assignment in `configure` (`:128-129`);
2. omitting a dimension requires opposite-edge anchors, else protocol error (`:130`);
3. both values default to 0 (`:131`);
4. a zero (or smaller) `configure` payload is a hint the client may take up, and a zero payload
   means the client decides (`:341-348`).

**Does NOT license.** (a) That the compositor's assigned size is the client's allocation, or that
the allocation is the band — that is S464's `current_allocation` read; (b) that the band equals the
exclusive zone — that is `set_exclusive_zone` `:152-188` plus `set_margin`'s "The exclusive zone
includes the margin" `:196`; (c) that the arranged box equals the band — that is S470's arrange
pass; (d) that a `height = 0` in a waybar declaration is a request of this kind, or that waybar
sends 0 on this host; (e) any host observation. It also does not license quoting the `configure`
sentence (`:347-348`) as `set_size`'s clause: the two messages run in opposite directions.

### S482 (kstatusnotifieritem interface XML)

**Licenses.** The interface name `org.kde.StatusNotifierWatcher` (`:3`); the two methods, each with
one `s` in-argument: `RegisterStatusNotifierItem` (`:6-8`) and `RegisterStatusNotifierHost`
(`:10-12`); the read properties `RegisteredStatusNotifierItems` type `as` (`:17-19`),
`IsStatusNotifierHostRegistered` type `b` (`:21`), `ProtocolVersion` type `i` (`:23`); and four
signals (`:28-40`). It is also the file plasma-workspace's watcher build generates its adaptor from
(`plasma-workspace@31242aad`, `statusnotifierwatcher/CMakeLists.txt:3-4`), so the declared members
are the ones the implementation registers.

**Does NOT license.** (a) The **bus name** — the XML names the interface, not a service; the bus
name is licensed by `plasma-workspace@31242aad`, `applets/systemtray/statusnotifieritemhost.cpp:28`
(`s_watcherServiceName = "org.kde.StatusNotifierWatcher"`) and `:86` (constructed on
`/StatusNotifierWatcher`); (b) the **object path** — not present anywhere in the XML; licensed by
`statusnotifierwatcher/statusnotifierwatcher.cpp:27` (`registerObject("/StatusNotifierWatcher")`);
(c) that the implementation honours the declaration: `RegisterStatusNotifierHost` is a no-op
(`Q_UNUSED(service)`, `statusnotifierwatcher.cpp:92-95`), `IsStatusNotifierHostRegistered` returns
`true` unconditionally (`:97-100`) and `ProtocolVersion` returns 0 (`:102-105`); (d) that a watcher
is running, or that waybar owns the name — that is the live `busctl --user list` read; (e) that the
freedesktop wiki's `org.freedesktop.StatusNotifierWatcher` is the same service — a different
namespace, which is why the page is S483 (rejected), not this row; (f) the property's value.

**Licence of the file itself.** The XML has no licence header (line 1 is the DOCTYPE) and the
repository tree listing shows no `.license` sidecar for it; the repository carries
`LICENSES/LGPL-2.0-or-later.txt` and `LICENSES/CC0-1.0.txt`. Which applies to this path is **not
established from the bytes I opened**; the pin is a 1151 B citation copy of an interface
declaration, and the row is not a licence grant.

## 5. Deltas against the committed rows at `corpus/SOURCES.md:433-435`

Read at `corpus/SOURCES.md` sha256 `2ca8fcd95885db8f64d53f3c392a49904ac2cee24b9863f78eed2d3219e1af24`
(379916 B, mtime 10:29:37). Cell order below is the registry's.

1. **S481 (:433) — anchor boundary. Factual.** Committed cell 6 says "`set_size` `:122-142`". In the
   pinned 407-line file `set_size` is `:122-137`; `:138` is blank, `:139` opens `set_anchor`, and
   `:142` is inside `set_anchor`'s own description. A reader following the committed span reads two
   requests. Truth: `set_size` `:122-137`, zero clause `:128-131`.
2. **S481 (:433) — quote attribution. The one that matters.** Committed cell 7 quotes
   `If the width or height arguments are zero, it means the client should decide its own window
   dimension.` at `:347-348`, and cell 5 says the row is "what a zero width/height in `set_size`
   means". That sentence sits in `<event name="configure">` (`:327-353`) and describes a zero the
   **compositor sends**; `set_size`'s own zero clause (`:128-129`) says the **compositor assigns**
   and informs. Keeping the committed quote with the committed teaches sentence tells a reader that
   `set_size` says the client decides, which is the reverse direction. My row quotes `:128-129` and
   names the `configure` clause separately in the anchor cell. (The knowledge entry has already
   separated the two, `corpus/knowledge/bar-footprint-allocation-r82.md:50` and `:59`.)
3. **S481 — URL.** Committed uses the Hyprland v0.56.2 vendored copy at `efb5099`; my row uses the
   canonical wlr-protocols pin `2b8d4332`. Both are live today and byte-identical (19326 B,
   `87e0b9c8…`), and so is S460's round-79 pin. The canonical URL is the authority for the clause
   and avoids the exact-duplicate-URL census warning that S460 already owns; the vendor copy stays
   S460's. If the L1 prefers the committed URL, nothing else in my row changes.
4. **S481 — kind and recheck.** Committed `code` / `on-release`; S460, the same bytes, is filed
   `spec`. My row files `spec` for consistency with S460 and `on-change` because a wlr-protocols
   commit pin has no release signal (calendar fallback 2027-05-03 if the lane prefers dates). Both
   are cosmetic; the L1 may keep the committed pair.
5. **S482 (:434) — method spans.** Committed anchor names methods `:6`/`:10`, the `<method>` name
   lines only. The elements are `:6-8` and `:10-12` (each has one `s` in-arg). My anchor gives the
   spans. The byte provenance in the row (v6.2.0, 1151 B, `19df7f18…`) re-verifies exactly.
6. **S482 (:434) — used-by.** `SKILL.md` is an attribution, not a literal citation: the string
   `S482` does not occur in `SKILL.md`. The round's literal citation is
   `quality/counters/c2-r82-runbook.py:17`. If the lane wants the used-by target to name the id, the
   SKILL.md tray rows (`:274-276`) need a `source:` note. L1 call, named not forced.
7. **S483 (:435) — dangling evidence pointer, repaired.** The row cites
   `.ufo/waves/round-82/fetch/S482.html`, 6395 B, sha256 `f22928e1…`; at 10:28 the file did not
   exist and was unlisted in `sha256-r82.txt`, and the round-82 lesson records the same absence at
   `corpus/lessons/round-82.md:86` ("pin the page or drop the pointer"). I fetched the page
   (`https://www.freedesktop.org/wiki/Specifications/StatusNotifierItem/StatusNotifierWatcher/`,
   HTTP 200, 6395 B), whose digest equals the cited one, wrote it to `fetch/S482.html`, and added the
   manifest line. `sha256sum -c` now reports 3/3 OK. Its head does say
   `There will be a single org.freedesktop.StatusNotifierWatcher service instance registered on the
   session`, so the rejection reason is supported verbatim. The name `S482.html` for the S483 source
   is the committed row's; a rename to `S483.html` must move the row's anchor cell and the manifest
   line together.
8. **Frozen declaration anchor (report-only, not editable by a seat).**
   `.ufo/waves/round-82/claims-declaration-r82.md:37` cites `set_size` `:116-123`. In the pinned bytes
   `:116-119` is the `layer_surface` unmapping description and `set_size` is `:122-137`; the citation
   is not re-derivable from `fetch/S481.xml`. The claim's substance is unaffected. The lesson's
   precision note reaches the same conclusion.

## 6. Verification actually run (read-only)

- `sha256sum -c .ufo/waves/round-82/fetch/sha256-r82.txt` **from the lane root** → `S481.xml: OK`,
  `S482.xml: OK`, `S482.html: OK`, rc 0. The manifest stores lane-relative paths, so `-c` run from
  inside `fetch/` fails with "No such file or directory"; that is a path convention, not a bad hash.
- `cmp` against independent fetches: S481 == gitlab `@2b8d4332` == Hyprland `@efb5099` == `S460.bin`;
  S482 == kstatusnotifieritem `v6.2.0` == `v6.31.0` == `master` == plasma-workspace `xembed-sni-proxy/`.
- `stat -c '%s'` → 19326 / 1151 / 6395 B, matching every size cited above.
- GitLab commits API `?path=unstable/wlr-layer-shell-unstable-v1.xml` → `2b8d4332`
  (2024-01-26); GitHub commits API `?path=src/org.kde.StatusNotifierWatcher.xml` → `506bdfca`
  (2014-03-21).
- Line numbers re-read from the pinned bytes: `set_size` `:122-137` (clause `:128-129`, anchor rule
  `:130`, default `:131`, double-buffered `:133`); `configure` `:327-353` (hint `:341-345`, zero
  `:347-348`); interface `:3`; methods `:6-8`, `:10-12`; property `:17-19`; `:21`; `:23`; signals
  `:28-40`.
- Word count of the S481 quote: 22 (limit 25).

## 7. Limits

- The fetches are today's network reads; the pinned files plus their digests are the offline
  re-check. I did not mirror the URLs anywhere else.
- No host probe was run: no `busctl`, no `hyprctl`, no D-Bus call. Neither row asserts that a
  watcher runs, who owns the name, or what the census prints on this machine.
- The freedesktop page and the KDE XML are different namespaces; the page is cited only as the
  rejected S483 and is never used to spell the rows' bus name.
- The KDE XML's file-level licence is not established (no header, no sidecar in the tree listing);
  only the repository's `LICENSES/` directory was observed.
- `S482.html` is the S483 source's bytes under the committed row's filename, not S482's.
- I did not append to `corpus/SOURCES.md`, and I did not edit the frozen instruments, the controls,
  the receipts or the claims declaration.

**Defect, named with file:line.** `corpus/SOURCES.md:433` cites `set_size` `:122-142` (the request
ends at `:137`, and `:139-142` belong to `set_anchor`) and uses the `configure` event's clause
`:347-348` as the row's `set_size` quote; the exact bytes are `set_size` `:122-137`, zero clause
`:128-129`, `configure` `:327-353`. Also the frozen declaration's `set_size` `:116-123`
(`.ufo/waves/round-82/claims-declaration-r82.md:37`) is not re-derivable from the pin. Repaired:
`corpus/SOURCES.md:435` cited `.ufo/waves/round-82/fetch/S482.html` (the lesson records the absence
at `corpus/lessons/round-82.md:86`), and the file was absent until this seat wrote it (digest equals
the cited `f22928e1…`).

STATUS: defect
