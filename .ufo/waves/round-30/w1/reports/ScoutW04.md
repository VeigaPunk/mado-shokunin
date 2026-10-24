# ScoutW04 — W04 duplicate-URL audit vs criterion 17

READ-ONLY scout finding. Tip audited: `92d3c867` (worktree = HEAD; committed
bytes match). No files edited.

## Live warning set

`bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
(fleet census script, read-only) at tip prints exactly **7 W04 warnings** then `ok`,
exit 0:

```
W04 S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
W04 S042 duplicate url wayland.freedesktop.org/extras.html across scopes
W04 S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
W04 S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
W04 S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
W04 S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
W04 S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
```

The census warns on non-first occurrences: the Window-Rules URL collides with
S017 (first occurrence, `SOURCES.md:29`); extras.html with S006 (`:18`);
colors.toml with S094 (`:106`); imaplib.py with S117 (`:129`);
executionmodel.rst is shared 3-way with S111 (`:123`).

## Criterion under test (QUALITY.md:34, committed)

> 17. Before source-fragment renumbering/merge, screen repeated canonical URLs
> across active rows even when scope wording differs. Review overlapping scope
> explicitly; reject/merge duplicates or append a genuine superseding row with
> a resolvable prior id. Preserve rejected history, and send distinct-scope
> reuse to human review rather than claiming URL equality proves semantic
> duplication. A warning-only shared census is not this review.

Disposition under audit (corpus/lessons/round-30.md:36-41): "each pair is
supersession or distinct-scope reuse with the rejected history preserved
(S030→S045 rejected-duplicate, S042 supersedes S006 in a disjoint scope, S119
supersedes S113's scope, S120/S121 pin different sections of one file, S097
supersedes S094)".

## Per-warning audit

| W04 row | Collision partner | Scope / anchor cells (committed) | Supersession trail | Verdict |
|---|---|---|---|---|
| S030 (`:42`) | S017 (`:29`) | scope "Current Lua window-rule syntax"; anchor `“Syntax”; page modified 2026-08-26` — same page, overlapping S017's `#syntax/#effects/#notes` scope, **no supersedes link** | Search log `SOURCES.md:275`: orchestrator spot-check disagreed; `mined → rejected` in place; `used-by` moved to S017; rejection reason preserved in search log + lessons/round-12.md because teaches cell is append-only | **Match** — rejected duplicate, history preserved |
| S045 (`:57`) | S017, S030 | scope "Duplicate current-wiki source admission, not a new window-rule fact"; anchor `Latest git introductory Note and Syntax, page modified 2026-08-26; reopened 2026-10-20` | teaches opens `supersedes S030 —` (resolvable id); status `rejected`; records the collision-review flip in its own row | **Match** — "S030→S045 rejected-duplicate" as claimed |
| S042 (`:54`) | S006 (`:18`) | S006 scope "which Wayland debugging surface exists", anchor §Compositor features + §Protocol dumpers, access date only; S042 scope "Documented compositor-global discovery, revision-anchored correction to S006", anchor pins `extras.html @ 8923a199…` | teaches opens `supersedes S006 —` (resolvable); S006 stays `queued`, its bytes untouched. Search log `:276` "owed anchors" rule prescribes exactly this fix for S006 | **Match** — distinct-scope supersession (see nuance 1) |
| S097 (`:109`) | S094 (`:106`) | S094 scope "(the only theme on this host)", anchored to per-fetch GitHub HTML tree digests; S097 scope corrects to "not the host's only theme — 19 payload dirs ship…", anchored to tag commit + tree/blob ids + raw sha | S097 title carries "(supersedes S094)"; teaches opens `supersedes S094 —` (resolvable); S094 `rejected` and retained verbatim | **Match** — "S097 supersedes S094" |
| S119 (`:131`) | S117 (`:129`) | same file/tag/sha/`Popen :1809-1812` quote; S117 scope = the entry point itself; S119 scope = "correction of S113's unsupported universal inference; the os process-management quote remains valid in its own scope" | teaches opens `supersedes S113 —` (resolvable id S113 at `:125`, still `mined`); S119 anchor notes "same opened raw source as S117" | **Match** — "S119 supersedes S113's scope"; URL reuse vs S117 is distinct-scope (see nuance 2) |
| S120 (`:132`) | S111 (`:123`), S121 (`:133`) | scope "annotation evaluation timing"; anchor `executionmodel.rst:240-256` lazy-evaluation section | no supersedes needed — disjoint sections of one pinned file (same sha `11f99f83…`) | **Match** |
| S121 (`:133`) | S111, S120 | scope "enclosing factory scope and late module-global lookup"; anchor `:89-114,322-329` | same as above; S111 pins `:59-61,:136-144` | **Match** — "S120/S121 pin different sections of one file" |

## Verdict on the lesson's claim

**Confirmed.** All seven W04 rows satisfy a criterion-17 disposition exactly as
the round-30 lesson states: two rejected duplicates with preserved history
(S030, S045 — S045 also carrying the resolvable `supersedes S030` link), three
appended superseding rows with resolvable prior ids (S042→S006, S097→S094,
S119→S113), and two distinct-scope same-file section pins (S120, S121). No row
was rewritten in place; every rejected row's original cells survive. No row
disproves the disposition.

## Nuances (not violations)

1. S042's `supersedes S006` is scoped to the compositor-global discovery claim;
   S006's §Protocol-dumpers sub-scope was never separately superseded — S006
   stays `queued` under the owed-anchor rule (`SOURCES.md:276`), so the
   supersession edge is narrower than S006's whole row. Consistent with the
   rule's "the round that mines any of them appends a superseding row"; the
   lesson's "disjoint scope" phrasing is loose but not wrong.
2. S119's *URL* collision is with S117, while its *supersedes* edge targets
   S113 (different file, os.rst). Both facts are committed in S119's cells
   ("same opened raw source as S117"; "supersedes S113 —"). The warning is
   therefore discharged by the union of distinct-scope reuse (vs S117) and
   supersession (vs S113).
3. The S120/S121 share is 3-way with S111; all three pin disjoint line ranges
   of the same pinned blob — no supersession edge needed or present.

## Evidence cited

- `corpus/SOURCES.md` rows at `:18,29,42,54,57,106,109,123,125,129,131-133`;
  search-log supersession trail `:275-276`.
- `corpus/QUALITY.md:34` (criterion 17), `:36-39` (lane-local screen note).
- `corpus/lessons/round-30.md:36-41` (claim under audit).
- `scripts/sources-census.sh validate` output reproduced above (7 W04, `ok`,
  exit 0) — read-only run, no mutation.

## Tooling

None installed; no upgrades needed. Confidence: high — all cells read at tip
`92d3c867`, warning list reproduced live.
