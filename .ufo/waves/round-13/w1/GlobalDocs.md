# GlobalDocs — U4 advertised-globals source draft (round 13, w1)

Seat: `MadoR13.GlobalDocs` (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`
at `7dcb785b7b943d03703181b218d7860a7b43007b` (working tree additionally carries the round-13
edits of other seats). Sources opened 2026-10-20 (UTC fetch 04:06:52Z).
Axes named: **coverage** (C1 — sourced U4 boundary for advertised globals) and **operability**
(a page revision that can be re-fetched and re-checked, plus a claim ladder a capture can be
graded against). Writes: this file and `reports/GlobalDocs.md` only. No shared-file changes,
no gate/build/test/formatter run; tooling installed: none (both sources are reads; `wayland-info`
and `wayland 1.26.0-1` were already installed by the capture seat, not by this seat).

## 1. Decision

- **S042 admitted, and it supersedes S006.** The exact page revision is established: content
  commit `8923a19916635c21a3577b616f650a7e45d70fa9` (2026-01-15T10:10:23+01:00), and the served
  page is byte-equal to the repo file at `main` (`sha256 97467f81…`). See §2.
- **S043 admitted** for the core registry spec: `protocol/wayland.xml` @
  `93c04ad3670633aea6f2435059378b75843b8e70` (2026-10-08), `sha256 4831fd1c…`. See §3.
- **S006 stays `queued` and is not changed in place.** Its owed anchor is closed by S042's
  `supersedes S006 —` link; S006 must not be cited as sole support while it stays queued.
- **No duplicate rows.** The draft proposed S042 on S006's exact scope cell; integration
  (`corpus/SOURCES.md:54`) instead used a narrowed scope, so the census now emits a non-failing
  W04 for `wayland.freedesktop.org/extras.html` (E04 stays exempt via the supersedes link:
  `scripts/sources-census.sh:646-649`; W04 is warning-only: `:33`, selftest `:361-364`). S043 is
  at `corpus/SOURCES.md:55` with an anchor this draft does not duplicate. §6 records the delta;
  the rows there are a revision record, **not** an append instruction.

## 2. S042 — `extras.html` revision evidence

| Fact | Value | How obtained (2026-10-20) |
|---|---|---|
| Page | `https://wayland.freedesktop.org/extras.html` | `curl -sS -D extras.hdr -o extras.html …` |
| Response | `HTTP/2 200`, `content-length: 4020`, `sha256 97467f81afe4f3039e422e09ef3b9329a0a7206556163e4b8d796e03cf76a6d8` | `sha256sum extras.html` |
| Server stamps | `date: Tue, 20 Oct 2026 04:06:52 UTC`; `last-modified: Mon, 19 Oct 2026 11:28:58 GMT`; `etag: "920a5838cbf1b53a9ecea6251d99168ed630a76a8e824d09b3025e881bd5b17a"` | response headers |
| Source repo | `wayland/wayland.freedesktop.org`, id 136, default branch `main` | `GET /api/v4/projects/136` |
| Repo HEAD at fetch | `c0c9d30d746173839cd76f5c8bf2e715f680f59e` (2026-10-19T14:27:18+03:00, `releases: add weston 16.0.1`) | `GET /api/v4/projects/136/repository/commits/main` |
| Last commit touching the page | `8923a19916635c21a3577b616f650a7e45d70fa9` (2026-01-15T10:10:23+01:00, `extras: mention wl-proxy`) | `GET /api/v4/projects/136/repository/commits?path=extras.html&per_page=5` (newest first, no later entry) |
| Content equality | repo `main` bytes, repo bytes at `8923a199`, and served bytes are all `sha256 97467f81…` | raw `/-/raw/main/extras.html` and `/-/raw/8923a199…/extras.html` vs fetched page |
| Publish path | the `pages` deploy job copies the repo tree verbatim (`mv * .public`, `only: main`); nothing generates `extras.html` | `.gitlab-ci.yml` at `main`, `pages:` stage |
| Page structure | no in-content date/revision footer; sections `Compositor features` (:17), `OpenGL features` (:26), `Protocol dumpers` (:34), `Manipulation tools` (:58), `Introspection tools` (:85) | local copy of the 104-line page |

Reading of the stamps:

- `last-modified` (2026-10-19T11:28:58Z) is the Pages **deployment** stamp, not a content edit:
  it post-dates the page's own last commit by nine months and matches the site HEAD's activity
  window. Do not cite it as the revision.
- `etag` is sha256-shaped but **not** the file digest (`920a5838…` ≠ `97467f81…`); it is a cache
  validator. Do not cite it as the revision.
- The only exact revision is the source commit, and byte equality proves the served page is that
  revision's file. `8923a199` is therefore the anchor for S042.

Grounding quote (`§Compositor features`, `extras.html:19-20`, 11 words; the typo "advertized"
is as published and is preserved from the round-12 gate quote):

> Running `wayland-info` will list all global interfaces advertized by the compositor.

Also used in the body below (`§Protocol dumpers`, `extras.html:36-39`): `WAYLAND_DEBUG=1`,
`client` and `server` are named, and a link labelled "is not enough" precedes the middle-man
dumper list — the page treats raw debug logging and protocol dumping as different capabilities.
Gate quote for a full-scope S042 anchor (16 words, `extras.html:36-39`):

> When using `export WAYLAND_DEBUG=1` (or `WAYLAND_DEBUG=client` or `WAYLAND_DEBUG=server`) is not enough, the following tools may help.

Admission: **admitted**, `docs`, tier A, scoped to "which Wayland debugging surface exists";
`[INF-docs]` only — the page is not a host observation. Status `mined` because the U4 entry
already cites S042 (§5, §6). Recheck `180d` (static page; last content commit 2026-01-15).

## 3. S043 — core registry spec revision evidence

| Fact | Value | How obtained (2026-10-20) |
|---|---|---|
| File | `protocol/wayland.xml` in `wayland/wayland` (id 121) | `GET /api/v4/projects/wayland%2Fwayland` |
| Main HEAD | `93c04ad3670633aea6f2435059378b75843b8e70` (2026-10-08T20:06:52Z, `protocol: define that wl_pointer.leave means buttons are no longer pressed`) | `GET …/repository/commits/main` |
| Last commit touching the file | same commit (newest in `?path=protocol%2Fwayland.xml`) | `GET …/repository/commits?path=protocol/wayland.xml` |
| Bytes | `sha256 4831fd1cdbca6319037660bec5da0f3c5636fd81573cb61e01e4709570dac294` at `main` **and** at `93c04ad` | raw fetch at both refs; equal digests |
| Installed copy | `/usr/share/wayland/wayland.xml`, package `wayland 1.26.0-1`, `sha256 cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07` | `sha256sum`; `pacman -Q wayland` |
| Installed vs upstream | whole-file digests differ (package snapshot predates 2026 commits), but `:110-180` — the whole registry region — is byte-identical | `diff <(sed -n '110,180p' …)` |
| Line map | `wl_display.get_registry` :55-68; `wl_registry` :117-178; `bind` :141-148; `global` :150-161; `global_remove` :163-177 | `nl -ba wayland.xml` |

The generated HTML spec at `https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_registry`
repeats the same two-argument `bind(name, id)` signature and the same description text verbatim.
It corroborates the XML text but is not a revision anchor: the site's CI builds `docs/html` from
the newest non-prerelease `wayland` tag (`git describe --tags --exclude "*.9[0-9]"` in
`.gitlab-ci.yml`, `wayland:` job), not from `main`. The XML at the pinned commit gets the single
row; no second row for the generated page.

Grounding quote (`wl_registry` description, `wayland.xml:136-138`, 23 words):

> This creates a client-side handle that lets the object emit events to the client and lets the client invoke requests on the object.

Admission: **admitted**, `spec`, tier A, scoped to core registry advertisement/bind semantics;
`[INF-docs]`, not a host fact. Status `mined` because the U4 entry already cites S043. Recheck
`on-release` (protocol text changes with Wayland releases).

**Correction carried by this anchor:** "Wayland 1.26.0" is the installed *package* version, not a
source revision. The registry region happens to be identical, but the file digests differ, so the
knowledge entry's S043 clause should name the commit and digest, not the package (§5, §10).

## 4. Global advertisement versus bind, use and behavior

All quotes below are from S043 (`protocol/wayland.xml` @ `93c04ad`); the page is S042.

### 4.1 The protocol ladder

| Step | What exists | Primary text (line) | What it licenses as evidence |
|---|---|---|---|
| L0 registry object | a per-client object created by `wl_display.get_registry` | "This request creates a registry object that allows the client to list and bind the global objects available from the compositor." (:57-59) | nothing about globals; creation is a request |
| L1 advertisement | a stream of `global` events, one per global in the registry, plus later deltas | "When a client creates a registry object, the registry object will emit a global event for each global currently in the registry." (:125-127) | an interface name and an interface version, point-in-time |
| L1 completeness | `wl_display.sync` immediately after `get_registry` marks the end of the initial burst | "To mark the end of the initial burst of events, the client can use the wl_display.sync request immediately after calling wl_display.get_registry." (:130-133) | that one snapshot is complete *if* the client synced |
| L2 bind | a new client-created object / client-side handle for that numeric name | "A client can bind to a global object by using the bind request. This creates a client-side handle that lets the object emit events to the client and lets the client invoke requests on the object." (:135-138) | that a handle exists; not that any request will succeed |
| L3 use | a request on the bound object and its event/error outcome | `bind` takes the numeric name and returns the new object (:141-148); interface events reach the handle (:136-137) | that this request was accepted or refused, for this bind |
| L4 behavior | the declared effect observed at the system under test | not defined by the registry text | that the feature works on this host, in this session |

Two properties separate the steps:

- **Advertisement carries exactly three fields.** The `global` event notifies "a global object
  with the given name is now available, and it implements the given version of the given
  interface" (:154-156) and its arguments are `name`, `interface`, `version` (:158-160). There is
  no capability, permission or behavior field.
- **Advertisement is mutable and server-wide.** "Globals come and go as a result of device or
  monitor hotplugs, reconfiguration or other events" (:127-129), and the globals are "available
  to all clients" (:119-120). A list is a timestamped sample, not a history and not a per-client
  grant.

### 4.2 Bind is not liveness, and use is not behavior

`global_remove` says the client "should now destroy that object", but also that "The object
remains valid and requests to the object will be ignored until the client destroys it, to avoid
races between the global going away and a client sending a request to it." (:167-174). So a
successfully bound handle can survive its global and silently ignore requests. Bind success and
request silence are therefore not capability or behavior evidence.

Registry creation is also not free: "the server side resources consumed in response to a
get_registry request can only be released when the client disconnects, not when the client side
proxy is destroyed" (:61-63). A diagnostic that opens registries repeatedly pays a server-side
memory cost; capture design should create one registry per run.

### 4.3 Applying the ladder to the two opened sources

- The extras page's `wayland-info` sentence claims exactly **L1**: "list all global interfaces
  advertized by the compositor" (:19-20). That is the legal claim for a registry header capture.
- The same paragraph also promises "additional information about the interfaces it knows about
  and have something to report, like monitor make and model, wl_seat capabilities, and wl_shm
  pixel formats" (:20-22). Those are interface events — the same XML defines `wl_shm.format`
  (:498), `wl_seat.capabilities` (:2030) and `wl_output.geometry`/`mode` (:2951, :3003) as events
  — and under S043 events reach only a bound handle (:136-137), so `[INF]` the tool binds for
  them. This seat did **not** observe the tool's internals: whether `wayland-info` 1.3.0 binds,
  and whether it waits on `wl_display.sync` before printing, stays `[UNK]`. Do not reclassify
  detail lines as advertisement, and do not treat the tool's list as protocol-level complete
  without that check.
- `WAYLAND_DEBUG=client` (or `=server`) logs traffic, but the page itself calls that "not enough"
  and points to middle-man dumpers/proxies (:36-39). Traffic observation is therefore an L2/L3
  route, not an L1 substitute, and not a behavior test.

### 4.4 Traps this boundary rejects

| Rejected inference | Why it fails under S042/S043 |
|---|---|
| "Interface advertised, therefore the host supports the feature." | L1 yields name/interface/version only (:158-160); no request was issued. |
| "Bind succeeded, therefore the feature works." | Bind only creates a handle (:135-138); after `global_remove` requests are ignored (:172-174). |
| "`wayland-info` printed seat capabilities / shm formats, therefore those are advertisement." | Those are interface state events, not registry fields; events require a bound handle (:136-137). `[INF]` about the tool; `[UNK]` unobserved. |
| "The globals list is a stable property of the session." | Hotplug and reconfiguration add/remove globals (:127-129); the list is a sample. |
| "Absence from one list falsifies support historically." | The snapshot is client- and session-bound; absence is only absence at that timestamp. |
| "The numeric registry name identifies the interface." | The name is the bind identifier (:146); `interface` and `version` are the stable fields (:158-160). The capture already drops numeric names. |

## 5. Integration text for `corpus/knowledge/wayland-protocol-boundaries-r13.md`

The entry `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/wayland-protocol-boundaries-r13.md`
already exists and cites both ids; no edit is made by this seat. Two owner/integrator patches are
required for the anchors to match the registry:

**(a) `source:` clause for S043** — replace `S043 (Wayland core wayland.xml, wl_registry,
Wayland 1.26.0)` with:

> S043 (Wayland core protocol `protocol/wayland.xml`, `wl_display.get_registry` :55-68 and
> `wl_registry` :117-178, @ `93c04ad3670633aea6f2435059378b75843b8e70`, sha256 `4831fd1c…`)

**(b) Replace the section `## Advertisement, binding and behavior`** (currently three summary
bullets) with the text below; it keeps the entry's `[INF-docs]` class and adds the line anchors,
the completeness boundary, the post-removal rule and the two limits.

```markdown
## Advertisement, binding and behavior

`[INF-docs]` S043, `wayland.xml` @ 93c04ad:

1. `wl_display.get_registry` creates a per-client registry object; its server-side resources are
   released only when the client disconnects (:57-63).
2. The registry emits one `global` event per global in the initial burst; `wl_display.sync`
   immediately after `get_registry` marks the end of that burst (:125-133). Hotplug and
   reconfiguration produce further `global` / `global_remove` events (:127-129).
3. A `global` event carries only `name`, `interface` and `version` — "it implements the given
   version of the given interface" (:154-160). No capability, permission or behavior is announced.
4. `wl_registry.bind` creates a client-side handle for the numeric name: "lets the object emit
   events to the client and lets the client invoke requests on the object" (:135-148).
5. After `global_remove`, "The object remains valid and requests to the object will be ignored
   until the client destroys it" (:172-174), so bind success is not liveness and request silence
   is not refusal.

Evidence ladder: L1 advertisement (this entry's host sample), L2 bind (handle exists), L3 use
(request issued, event or protocol error observed), L4 behavior (declared effect observed on the
system under test). S041's `wayland-info` header capture establishes L1 only.

`[INF]` The extras page also lists "monitor make and model, wl_seat capabilities, and wl_shm pixel
formats" (S042 :20-22); `wl_shm.format` (:498), `wl_seat.capabilities` (:2030) and
`wl_output.geometry`/`mode` (:2951, :3003) are events in the same XML, and per S043 events arrive
only on a bound handle.
Whether `wayland-info` binds, and whether it completes the initial burst with `wl_display.sync`,
was not observed here (`[UNK]`). Documented check, not run in this round: run `wayland-info` with
`WAYLAND_DEBUG=client` and record whether `wl_registry.bind` requests appear; the page notes
`WAYLAND_DEBUG` alone "is not enough" for protocol dumping (S042 :36-39).
```

Do not cite S006 as support: it stays `queued`, and S042 carries the pinned revision.

## 6. Integrated rows and the source-revision delta (do not append)

Observed after this draft's first pass (2026-10-20): `corpus/SOURCES.md:54-55` already carries
S042 and S043, both `mined`, both `used-by corpus/knowledge/wayland-protocol-boundaries-r13.md`.
Appending the rows drafted below would duplicate ids (E03), so they are retained here only as the
source-revision record; the status/used-by condition they were drafted under is already satisfied.

| id | integrated cells (line) | delta this draft supplies | contract-legal action |
|---|---|---|---|
| S042 (line 54) | integrated cells: scope `Documented compositor-global discovery, revision-anchored correction to S006`; anchor `§Compositor features`; `teaches` opens `supersedes S006 —` but names only advertised-global discovery | full-scope revision package: S006's exact scope string, both page sections, dumper content in `teaches`, digest, and a §Protocol dumpers gate quote | Land all of it while the file is uncommitted: (a) scope → `which Wayland debugging surface exists (compositor globals, protocol dumps)` — same URL and scope, so E04 stays exempt via the supersedes link and the W04 disappears; (b) anchor → `§Compositor features + §Protocol dumpers; website source extras.html @ 8923a19916635c21a3577b616f650a7e45d70fa9 (2026-01-15; served bytes sha256 97467f81…)`; (c) teaches → `supersedes S006 — wayland-info lists advertised globals and WAYLAND_DEBUG plus middle-man dumpers (wayland-tracker, wayland-tracer, wlanalyzer) are the traffic route; inventory and protocol behaviour are separate observables`; (d) gate quote `extras.html:36-39` (below). If any cell cannot change, use the fallback qualifier `§Compositor features only; §Protocol dumpers stays owed on S006` and accept the W04. |
| S043 | source `/usr/share/wayland/wayland.xml; https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_registry`; anchor `wayland 1.26.0-1 installed XML:117-177` (55) | upstream commit `93c04ad…`, `sha256 4831fd1c…`, and byte-identity of `:110-180` between the installed file and that commit | Recommended: keep the row and amend the **entry's** `source:` S043 clause to the commit + digest (§5a); the entry is not append-only, and the installed region is byte-identical. Only if the registry row itself must carry the source revision does Rule 2 require a superseding row (next unused id) — not recommended: same scope, byte-identical text, extra row volume. |

Draft record — already integrated; **do not append** (kept for the revision provenance):

```markdown
| S042 | Wayland debugging extras — https://wayland.freedesktop.org/extras.html | docs | A | which Wayland debugging surface exists (compositor globals, protocol dumps) | §Compositor features + §Protocol dumpers; extras.html @ wayland/wayland.freedesktop.org 8923a19916635c21a3577b616f650a7e45d70fa9 (2026-01-15, last commit touching the file; served bytes sha256 97467f81afe4f3039e422e09ef3b9329a0a7206556163e4b8d796e03cf76a6d8) | supersedes S006 — the official page names wayland-info as the advertised-global lister and WAYLAND_DEBUG with middle-man dumpers as the traffic route, so inventory and protocol behaviour are separate observables | mined | 2026-10-20 | 180d | corpus/knowledge/wayland-protocol-boundaries-r13.md |
| S043 | Wayland core protocol — wl_registry advertisement and bind — https://gitlab.freedesktop.org/wayland/wayland/-/blob/main/protocol/wayland.xml | spec | A | core registry advertisement and bind semantics (wl_display.get_registry, wl_registry.global, bind, global_remove) | protocol/wayland.xml:55-68,117-178 @ wayland/wayland 93c04ad3670633aea6f2435059378b75843b8e70 (2026-10-08, last commit touching the file; main HEAD at 2026-10-20; sha256 4831fd1cdbca6319037660bec5da0f3c5636fd81573cb61e01e4709570dac294) | advertisement carries only name, interface and version; events and requests exist only on a bound client-side handle, so a globals list is neither capability nor behaviour evidence | mined | 2026-10-20 | on-release | corpus/knowledge/wayland-protocol-boundaries-r13.md |
```

In-place changes proposed: **none**. S006 keeps `status queued`, `recheck 180d`, `used-by —`;
its anchor debt is recorded as closed by the S042 supersedes link, not by editing S006. The
`used-by` cell convention stays repo-relative (the census resolves it from the lane root);
absolute paths appear only in prose.

## 7. Gate block for `corpus/lessons/round-13.md` (`## Gate`)

- S042 — https://wayland.freedesktop.org/extras.html — accessed 2026-10-20 — "Running
  `wayland-info` will list all global interfaces advertized by the compositor." — §Compositor
  features, `extras.html:19-20`; revision `8923a19916635c21a3577b616f650a7e45d70fa9` (served
  bytes `sha256 97467f81…` equal repo `main`; no later path commit); tier A; `docs`;
  **supersedes S006** — admission: admitted, `mined`.
- S043 — https://gitlab.freedesktop.org/wayland/wayland/-/blob/main/protocol/wayland.xml —
  accessed 2026-10-20 — "This creates a client-side handle that lets the object emit events to
  the client and lets the client invoke requests on the object." — `wl_registry` description,
  `protocol/wayland.xml:136-138`; revision
  `93c04ad3670633aea6f2435059378b75843b8e70` (`sha256 4831fd1c…`, `main` HEAD and path commit
  agree); tier A; `spec`; admission: admitted, `mined`.

Supporting quotes used in the lesson body (not the one-quote gate field): `extras.html:20-22`
(monitor make/model, seat capabilities, shm formats), `extras.html:36-39` — "When using `export
WAYLAND_DEBUG=1` (or `WAYLAND_DEBUG=client` or `WAYLAND_DEBUG=server`) is not enough, the
following tools may help." (16 words; required if S042's anchor widens to `§Protocol dumpers`);
`wayland.xml:125-133` (burst, hotplug, `wl_display.sync`), `:154-160` (global fields),
`:172-174` (post-removal ignore), `:61-63` (registry resource cost).

Integration note: the landed S043 row (`corpus/SOURCES.md:55`) cites the installed
`/usr/share/wayland/wayland.xml` (wayland 1.26.0-1, `:117-177`). The gate line above names the
upstream commit whose registry region is byte-identical (`:110-180`, `sha256 4831fd1c…`), which is
the revision actually checked; if the lesson records the installed path instead, add the commit and
digest in the same line so a recheck can separate package drift from upstream text. S042's landed
anchor already names `8923a199`; the digest `97467f81…` belongs in the lesson body.

## 8. Search-log note for `corpus/SOURCES.md` § Search log

From the `docs` seat, round 13 (2026-10-20):

- Question: what is the exact revision of the official Wayland debugging-extras page, and which
  primary text defines the difference between an advertised global and a bound, used object?
  Where: `extras.html` over HTTPS plus the GitLab API path history and raw-`main` bytes for
  project 136; `protocol/wayland.xml` raw at `main` and at its path commit plus commit history for
  project 121; the installed `/usr/share/wayland/wayland.xml` read only to compare package
  snapshot with upstream. Identified 2 — extras page, core protocol XML; screened 2 — same opens;
  included 2 — S042, S043; excluded 0. One adjacent non-row check: the installed XML copy, used
  only to show that a package version is not a source revision (digests differ, registry region
  identical). Excluded revision candidates: the page's `Last-Modified` (Pages deploy stamp,
  2026-10-19T11:28:58Z) and its `ETag` (`920a5838…`, a cache validator, not the content digest
  `97467f81…`). Stop rationale: both revisions are pinned by byte equality at a path-specific
  commit; the core registry text is the primary definition of every admitted L1–L3 claim, and the
  only remaining question (whether `wayland-info` binds or syncs) is a traffic observation with a
  documented route, not another document.

## 9. Operability notes for the capture and gate lanes

- A globals capture is L1 evidence only. Its record needs: UTC timestamp, command, exit status,
  display socket, tool name/version/package, compositor name/version/commit, the
  `(interface, version)` pairs with multiplicity, and a set digest —
  `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/globals.json` already has
  all of these (`schema`, `captured_utc`, `probe`, `tool`, `compositor`, `globals`,
  `global_count`, `unique_interface_count`, `set_sha256`).
- Keep the sanitization boundary: no output identity, EDID strings, seat names, device paths,
  format tables or numeric registry names. The capture's `excluded` list is the correct shape.
- Repetition: one registry per run (S043 :61-63). A second run in the same session updates the
  sample; a run in another session is a different sample, not a falsification.
- Completeness: the protocol's boundary is `wl_display.sync` (S043 :130-133). Until a traffic
  capture shows the tool waits for it, describe the list as "`wayland-info` output at T", not
  "the complete protocol registry at T".
- Escalation order for a future diagnostic: L1 list (S042/S041) → `WAYLAND_DEBUG=client` traffic
  (S042 :36-39) → middle-man dumper/proxy named on the same page → a feature-specific L4 probe
  under its own authorization.

## 10. Adjacent corrections, risks and limits

| Item | Finding | Owner |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:54` (S042) | scope narrowed, and anchor/teaches cover only `§Compositor features`; §6 gives the four-cell amendment (scope, anchor, teaches, gate quote). While the file is uncommitted this is an edit, not a supersede; if the scope stays narrow, accept the W04 | L1 / SOURCES.md owner (RegistryDraft disclaims this file) |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:55` (S043) | anchor stops at `wayland 1.26.0-1 installed XML:117-177`; the checked upstream revision is `93c04ad` (`sha256 4831fd1c…`), whose registry region `:110-180` is byte-identical. Carry the commit in the entry/lesson; do not add a supersede row for identical text | L1 / SOURCES.md owner (RegistryDraft disclaims this file) |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/wayland-protocol-boundaries-r13.md` `source:` S043 clause | names "Wayland 1.26.0" (package) instead of the commit; replace per §5(a) | entry owner / L1 |
| same entry, `## Advertisement, binding and behavior` | summary bullets lack the completeness boundary and the post-removal rule; replacement text in §5(b) | entry owner |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/EvidenceChain.md` §3 table | lists `xdg_wm_base` (v6) and `wp_color_manager_v1` (v1); `globals.json` records **7** and **3** — arithmetic mismatch in a sibling artifact | EvidenceChain author |
| S006 | remains `queued`; a future round may mark it `rejected` only with a documented reason, since S042 now owns the URL and scope | RegistryDraft |
| `wayland-info` bind/sync behavior | `[UNK]`; not inferred from the page, not observed | future traffic capture |
| `extras.html` revision | pinned by commit only; the page has no in-content date, and server stamps are deploy/cache metadata | recheck 180d |

Risks / blockers: none for this scope. The S043 claims are confined to the registry text; this
draft makes no protocol-phase claim (S005/S040 own that) and no host-behavior claim (S041/L4 own
that). `wayland-info` and `wayland 1.26.0-1` were already present; this seat installed nothing.

Files written: `.ufo/waves/round-13/w1/GlobalDocs.md` (this draft) and
`.ufo/waves/round-13/w1/reports/GlobalDocs.md` (seat report). No other file was modified.
