# GlobalDocs — report (MadoR13.GlobalDocs, w1)

Date 2026-10-20 (UTC fetch 04:06:52Z). Baseline `7dcb785b7b943d03703181b218d7860a7b43007b`.
Leaf seat; no dispatch, no background jobs, no shared-file edits. No builds, tests, lint,
formatters or `tools/mado-verify.sh` runs. Tooling installed or updated: **none** (`wayland-utils
1.3.0-1` and `wayland 1.26.0-1` were already present; this seat only read two upstream sources and
the installed XML copy).

Outputs written (exactly two):

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/GlobalDocs.md` — full draft.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/reports/GlobalDocs.md` — this report.

## Decision

- **S042 admitted and supersedes S006.** Exact page revision established; the served page is
  byte-equal to the repo file at `main`.
- **S043 admitted** for the core registry spec (`protocol/wayland.xml`).
- **S006 unchanged** (`queued`, `used-by —`, no in-place edit); its owed anchor is closed by the
  `supersedes S006 —` link. It must not be cited as sole support.
- **No duplicate rows:** S042 reuses S006's scope byte-for-byte; S043 has a new URL and scope.

## Source opens (URL, date, quote ≤25 words, location, revision, tier, admission, flip)

1. **S042** — `https://wayland.freedesktop.org/extras.html` — opened 2026-10-20 —
   "Running `wayland-info` will list all global interfaces advertized by the compositor."
   (11 words; typo as published) — §Compositor features, `extras.html:19-20` —
   revision `extras.html` @ `wayland/wayland.freedesktop.org` commit
   `8923a19916635c21a3577b616f650a7e45d70fa9` (2026-01-15, last commit touching the file); served
   bytes, repo `main` bytes and repo bytes at that commit are all
   `sha256 97467f81afe4f3039e422e09ef3b9329a0a7206556163e4b8d796e03cf76a6d8`; the site's `pages`
   job publishes the repo tree verbatim (`mv * .public`, `only: main`), so no generator sits
   between commit and page; site HEAD `c0c9d30d…` (2026-10-19) does not touch the file — tier
   **A** (`docs`) — **admitted**, `mined`. Flip: a later commit touching `extras.html`, or a
   server page that no longer matches the repo file (then re-pin or reject the supersede).

2. **S043** — `https://gitlab.freedesktop.org/wayland/wayland/-/blob/main/protocol/wayland.xml` —
   opened 2026-10-20 — "This creates a client-side handle that lets the object emit events to the
   client and lets the client invoke requests on the object." (23 words) — `wl_registry`
   description, `protocol/wayland.xml:136-138` — revision
   `93c04ad3670633aea6f2435059378b75843b8e70` (2026-10-08, path commit = `main` HEAD at fetch;
   `sha256 4831fd1cdbca6319037660bec5da0f3c5636fd81573cb61e01e4709570dac294`) — tier **A**
   (`spec`) — **admitted**, `mined`. Flip: a protocol change to `wl_registry`/`wl_display` text
   (recheck `on-release`), or a contradiction between the XML and the generated spec page.

## Behavior described (advertisement vs bind/use/behavior)

The core text separates five levels: L0 registry object creation (`:57-63`), L1 advertisement
(`global` events carrying only `name`/`interface`/`version`, `:125-133`, `:150-160`, with
`wl_display.sync` as the end-of-burst boundary), L2 bind (a client-side handle that can emit
events and invoke requests, `:135-148`), L3 use (a request and its event/error), and L4 behavior
(the declared effect observed on the host). `global_remove` makes the key negative case explicit:
the bound object "remains valid and requests to the object will be ignored until the client
destroys it" (`:172-174`). Therefore a `wayland-info` header list is L1 evidence only; the page's
"additional information … monitor make and model, wl_seat capabilities, and wl_shm pixel formats"
(`extras.html:20-22`) are interface events — `wl_shm.format` `:498`, `wl_seat.capabilities`
`:2030`, `wl_output.geometry`/`mode` `:2951`/`:3003` in the same XML — and events require a bound
handle (`[INF]`); whether the tool binds or waits on `wl_display.sync` was not observed (`[UNK]`).
`WAYLAND_DEBUG=client` is the page's documented traffic route but "is not enough" for protocol
dumping (`extras.html:36-39`).

## Registry rows (integrated while this seat worked)

`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:54-55` now carries S042 and S043,
both `mined` and both used-by the U4 entry. The rows in the full draft are therefore a revision
record and **must not be appended** (E03 duplicate id). Delta on the landed cells:

- **S042 (line 54), four-cell amendment while the file is uncommitted:** (a) scope → S006's exact
  string `which Wayland debugging surface exists (compositor globals, protocol dumps)` — same URL
  and scope, so E04 stays exempt via the supersedes link and the W04 disappears; (b) anchor →
  `§Compositor features + §Protocol dumpers; website source extras.html @ 8923a199… (2026-01-15;
  served bytes sha256 97467f81…)`; (c) `teaches` → after `supersedes S006 —`, name the dumper
  content (wayland-tracker, wayland-tracer, wlanalyzer) and the inventory-vs-traffic distinction;
  (d) gate quote `extras.html:36-39` — "When using `export WAYLAND_DEBUG=1` (or
  `WAYLAND_DEBUG=client` or `WAYLAND_DEBUG=server`) is not enough, the following tools may help."
  (16 words). Fallback if any cell cannot change: keep the narrow anchor, qualify `teaches` with
  "§Compositor features only; §Protocol dumpers stays owed on S006", and accept the W04.
  `SOURCES.md` is not RegistryDraft's write scope (it owns only
  `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/RegistryDraft.md`), so the
  amendment routes to L1.
- **S043 (line 55):** anchors the installed `/usr/share/wayland/wayland.xml` (wayland 1.26.0-1,
  `:117-177`) plus the generated docs page. This seat's upstream anchor is `93c04ad…` with
  `sha256 4831fd1c…`; the registry region `:110-180` is byte-identical between the installed file
  and that commit, so the quoted text is the same. Recommended fix is the entry's `source:` clause
  (draft §5a), not a new row; a Rule 2 supersede row would duplicate scope for identical text.

Draft row shape was checked locally before integration: `NF=13`, valid kind/tier/status enums, no
`|` inside cells; normalized URLs `wayland.freedesktop.org/extras.html` and
`gitlab.freedesktop.org/wayland/wayland/-/blob/main/protocol/wayland.xml` (distinct from S005/S006).

## Corrections handed to owners (not edited by this seat)

- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/wayland-protocol-boundaries-r13.md`
  `source:` S043 clause names the package ("Wayland 1.26.0"); replace with the commit + digest
  (exact replacement text in the draft §5a), and replace its `## Advertisement, binding and
  behavior` bullets with the anchored section in §5b (adds the sync boundary, the post-removal
  rule, and the `[UNK]` tool limit).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:54-55` (RegistryDraft): S042's
  narrowed scope yields a non-failing W04; S043's anchor stops at the package version. Recommend
  keeping both rows and carrying the commit revision in the lesson and the entry (§6 of the
  draft), not appending a Rule 2 supersede row.
- Registry arithmetic (verified for the attack seat; not edited): `SOURCES.md:116` prints `8 7 1`
  as `len`, `len-1`, literal `1`, so it measures nothing; the candidate statuses do support
  7 mined + 1 rejected (S005, S017, S040-S044 mined; S045 rejected). Rejected rows are now 4
  (S011, S012, S030, S045), and the W04 set is 3 (S030 and S045 on the Window-Rules URL, S042 on
  extras), i.e. S045 adds the second Window-Rules warning. The census has no
  duplicate-correction tag and contract Rule 2 prescribes the correction row, so keep-and-tag in
  the round lesson is the defensible option.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/EvidenceChain.md` §3 lists
  `xdg_wm_base` v6 and `wp_color_manager_v1` v1;
  `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/globals.json` records **7**
  and **3**. Arithmetic mismatch in a sibling artifact.
- Owed-anchor note `corpus/SOURCES.md:92`: the round-13 supersede row is the recognized form; no
  in-place S006 change is required.

## Risks / blockers

None for this scope. No protocol-phase claim (S005/S040 own it) and no host-behavior claim
(S041/L4 own it) is made here. The page has no in-content revision, so the commit is the only
revision; `Last-Modified` (deploy stamp) and `ETag` (cache validator, ≠ content digest) were
explicitly rejected as revision evidence. Verification (census, gate) was not run by this seat, per
the wave contract.
