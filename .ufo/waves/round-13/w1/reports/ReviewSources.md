# ReviewSources — round 13 / w1 — S030 outside disagreement, corpus contract, collision and supersedes handling

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` (leaf seat `MadoR13.ReviewSources`; no delegation, no background jobs).
Mode: read-only review. No registry, lesson, knowledge, or tool file was edited. Live fetches accessed 2026-10-20.
Tooling: no installs or upgrades. Used existing `curl`, `awk`, `grep`, and the read-only fleet validator `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (validate mode; it reports that it only reads the registry). Tooling record: none.

## Verdict on the disagreement

The round-12 rejection of S030 is substantively correct: S030 and S017 are the same canonical page, and both quoted passages appear on it. The defects are in the process around that rejection: the collision test the contract implies cannot see the overlap, the row's rejected shape is not the contract's shape, and several cross-references were left stale. No finding below changes the S030 status. Findings are ordered by severity.

## Findings

### F1 (medium) — Collision check is an exact (URL, scope-string) test; overlapping scope is invisible to the census

- Contract census lines `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:75-76` check duplicate ids only. There is no URL check in the contract census. Lesson `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md:116` says the next merge "runs a URL-duplicate pass", but no such pass is in the contract census block.
- Fleet validator `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:644-645`: W04 fires when a URL was already seen under a different `scope_key = url SUBSEP scope` string. E04 (`:647-649`) fires only for the same URL and the same scope string, when the new row is not rejected and `teaches` does not match `supersedes S[0-9]{3}`. "Overlapping scope" is a semantic judgment the validator never computes.
- Observed 2026-10-20: `TZ=UTC bash scripts/sources-census.sh validate mado-shokunin --root /home/vgpnk/Projects/shokunin --today 2026-10-20` prints `mado-shokunin W04 S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes` and `ok`, exit 0. The round-12 run (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/reports/round-12/mado.md:217,223`) matches. W-codes are non-failing (`sources-census.sh:24-33`).
- Consequence: S017 and S030 had different scope strings, so the admission produced only a non-failing warning. The collision was caught by a human spot-check (`lessons/round-12.md:116`), not by the census.
- Lane-level URL pass (read-only, reproduced): `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {id=$2; src=$3; gsub(/^ +| +$/,"",id); if (match(src,/https?:\/\/[^ )]+/)) {u=substr(src,RSTART,RLENGTH); sub(/[.,;]+$/,"",u); sub(/\/$/,"",u); print u "\t" id "\t" $9}}' corpus/SOURCES.md | sort | awk -F'\t' '{c[$1]++; l[$1]=l[$1] " " $2 "(" $3 ")"} END{for(k in c) if (c[k]>1) print c[k], k, l[k]}'` → `2 https://wiki.hypr.land/Configuring/Basics/Window-Rules  S017( mined ) S030( rejected )`. This is the only URL collision among the 39 rows.
- Fix route (fleet-level; not a mado edit): key the duplicate check on normalized URL alone, with an explicit scope-equality or overlap declaration, and make E04 or a named failing code cover same-URL non-rejected pairs regardless of scope string. Until then, the census should be read as "W04 present means review required."

### F2 (medium) — Supersedes handling: the round-12 deferral reason is partly stale, and the supersedes exemption is unverified

- Owed-anchor deferral at `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:92` and `lessons/round-12.md` (report `.ufo/reports/round-12/mado.md:219`) says a superseding row on the same URL "reads as a duplicate to the fleet census (E04/W04) until the supersedes link is recognised."
- The link is already recognised, but only for E04. `sources-census.sh:648` exempts any `teaches` containing `supersedes S[0-9]{3}`. Three gaps:
  1. The contract requires the phrase to open `teaches` (`SOURCES-CONTRACT-v1.md:49-51`). The validator matches it anywhere in the cell.
  2. The validator does not check that the superseded id exists, that it shares the URL, or that it is rejected or mined. Any `supersedes S999` silences E04.
  3. W04 still fires when the superseding row's scope string differs (see F1), so the deferral was not blocked by E04 alone.
- No row in `corpus/SOURCES.md` uses `supersedes` today. The fleet precedent is in the round-12 fleet report, `/home/vgpnk/Projects/shokunin/.ufo/reports/round-12/SOURCES.md:81`, which notes that game-dev-3d has S036 superseding S011 with its path not updated. That is a path-update defect, not a validator-supported pattern.
- Fix route: the contract should say what a supersedes row must satisfy (opening phrase, existing superseded id, same normalized URL, distinct anchor or rejection form), and the validator should check it. The owed rows S006, S008, S009 and S010 stay deferred until then.

### F3 (medium) — S030 rejected row does not follow the contract's rejected shape; the census does not enforce it

- Contract `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:34-35`: "Rejected rows read `REJECTED: <reason>; flip: <what would change the verdict>`."
- Registry: S011 and S012 comply. S030 (`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:41`) has `status` = `rejected` and `teaches` = "Provides a current Lua example to contrast with the v0.54 hyprlang form." That is the admission-era text. The rejection reason is held outside the row, in `SOURCES.md:91` and `lessons/round-12.md:122`.
- Rule 2 (`SOURCES-CONTRACT-v1.md:49-51`) allows in-place change to `status`, `recheck` and `used-by` only. `teaches` cannot be rewritten. So the in-place status change is permitted, but the shape rule is unmet and no in-place route repairs it.
- The validator does not catch this. W02 (`sources-census.sh:671-672`) flags rejected rows only when `length(teaches) < 8`, so S030 passes. It checks no `REJECTED:` prefix and no `flip:` clause.
- Options, for the owner's decision: (a) record the S030 shape as a logged contract exception in the round-13 lesson, citing Rule 2 and the immutable-cell constraint; or (b) under Rule 2's correction route, append a new row (next unused id) whose `teaches` opens `supersedes S030 — REJECTED: duplicate of S017 ...; flip: ...`, with `status` rejected. The validator exempts rejected rows from E04 (`sources-census.sh:647`), so (b) does not trip E04. Neither option edits S030's historical cells.

### F4 (low–medium) — Knowledge entry: erratum enumeration is incomplete, and the Lua-call claim's grounding quote sits on the rejected row

- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/hyprland-config-era-r12.md` cites S030 at line 3 (header), 59, 67, 103, 116 and 127 (erratum). The erratum at line 127 says "read every S030 citation in this entry (header and line 67) as **S017**," but its parenthetical lists two of the six locations. The general clause still covers the others, so this is a wording gap, not a missing mapping.
- Line 67 (`[INF-docs] The current wiki demonstrates the Lua call hl.window_rule({ ... })`) is grounded in the gate quote at `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md:84` (S030). S017's gate quote at `lessons/round-12.md:71` is "All props must match for a rule to be applied." Under contract Rule 1, the grounding quote should attach to the row that is cited. Live verification (V1 below) shows the Lua call is on the same page as S017, so the claim is supported. Only the gate attachment is wrong.
- Fix route: append (not edit) a round-13 gate note to the lesson that adds the hl.window_rule quote as a grounding record for S017, pointing to the same live page.

### F5 (low) — SOURCES § Paths still routes through rejected S030 with no caution

- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:55`: "Configuration-language era (U2) — S021 → … → S029 → S030: … the current wiki last." S030 is rejected (`SOURCES.md:41`), and the path carries no caution. The round-12 fleet report flags the same point (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-12/SOURCES.md:106`).
- `Paths` is prose, not a status/recheck/used-by cell. Editing line 55 in place is a historical edit. The append-only route is a caution line in the `## Search log` errata block (`SOURCES.md:88-92`), or a dated note appended under `## Paths`.

### F6 (info) — S030 flip is satisfiable; the wiki has a distinct pinned anchor

- S030's flip (`SOURCES.md:91`): "a distinct anchor at a pinned revision that S017 does not cover." The versioned archive gives one. `https://wiki.hypr.land/0.56.0/Configuring/Basics/Window-Rules/` (HTTP 200, accessed 2026-10-20) and `https://wiki.hypr.land/0.55.0/Configuring/Basics/Window-Rules/` (HTTP 200) both carry the same `hl.window_rule` example. Under the contract's anchor rule (section plus revision, `SOURCES-CONTRACT-v1.md:32-33`), a row citing the 0.56.0 archive is a distinct anchor. Whether it adds content beyond S017 is not established: its modified date was not extracted, and it repeats the latest-git example.
- There is no 0.56.2 archive: `https://wiki.hypr.land/0.56.2/Configuring/Basics/Window-Rules/` returns HTTP 404, and the version selector (`https://wiki.hypr.land/version-selector/`, accessed 2026-10-20) lists archives up to 0.56.0 in the 0.5x series. The nearest pinned revision to host 0.56.2 is therefore 0.56.0 `[OBS]`. The host's own version is 0.56.2 per round-12 evidence; the wiki does not publish that version's window-rule page.
- This is an option for a future row, not an admission. No admission is recommended here.

### F7 (info) — Verified as correct

- Same canonical page: `https://wiki.hypr.land/Configuring/Basics/Window-Rules/` has `<link rel=canonical href=https://wiki.hypr.land/Configuring/Basics/Window-Rules/>`. The no-trailing-slash form resolves to the slashed form (HTTP 200, final URL with slash). S017 and S030 cite the same URL, so the duplicate is real, not a near-miss.
- Live `article:modified_time` 2026-08-26T14:50:40+02:00 matches the S017 and S030 anchor cells. Live note "Since Hyprland 0.55, hyprlang is deprecated in favor of lua." matches S017's teaches. `href=#notes`, `#syntax` and `#effects` anchors exist.
- Registry census, run 2026-10-20 with the contract's commands: rows 39; malformed 0; ids unique; tier A=35 B=1 C=3; status mined=27 queued=9 rejected=3; used-by paths exist for all mined rows. Fleet validator on mado: W04 S030 only, exit 0.
- S017 `used-by` (`SOURCES.md:28`) lists both knowledge files; both cite S017 (`grep`). The S030 status and S017 used-by changes are logged old→new in `lessons/round-12.md:122-124`, as Rule 2 requires.
- S023 (`https://wiki.hypr.land/0.54.0/Configuring/Window-Rules/`, HTTP 200) is a distinct URL, so it does not collide with S017.

## Source opens (2026-10-20)

| URL | Accessed | Quote, location | Revision | Tier | Disposition |
|---|---|---|---|---|---|
| https://wiki.hypr.land/Configuring/Basics/Window-Rules/ | 2026-10-20 | "All props must match for a rule to be applied." — `#syntax` (S017 grounding; present on live page) | Latest git; modified 2026-08-26T14:50:40+02:00 | A (docs, scope: Lua-era syntax) | S017 stays `mined`; no change proposed |
| same URL | 2026-10-20 | `hl.window_rule({ match = { class = "my-window" }, border_size = 10 })` (HTML-escaped quotes) — "Syntax" (S030 grounding; present on same page) | Latest git; modified 2026-08-26 | A | S030 rejection stands; same page as S017 |
| https://wiki.hypr.land/0.56.0/Configuring/Basics/Window-Rules/ | 2026-10-20 | Same `hl.window_rule` example, HTTP 200 | Archive 0.56.0; modified date [UNK] (not extracted) | A candidate | Not admitted; F6 flip candidate |
| https://wiki.hypr.land/0.56.2/Configuring/Basics/Window-Rules/ | 2026-10-20 | HTTP 404 | none | — | No 0.56.2 archive page at this path |
| https://wiki.hypr.land/version-selector/ | 2026-10-20 | Lists archives through 0.56.0 in the 0.5x series | Site index | — | Used only to bound F6 |

No new row was admitted or rejected by this review. No registry cell was changed.

## Verification gaps

- The modified date and content of the 0.56.0 archive page were not extracted; F6 says so.
- I did not run the fleet validator's selftest or a fresh full-fleet run; only the mado-lane validate call and the shared-URL call were run.
- Whether `hl.window_rule` on the 0.56.0 archive differs in substance from the latest page was not compared line by line.
- Items that belong to the wider round (the U4 frontier, rows S005–S010, the set-blind gate census) were not reviewed.

## Routing

- F1 and F2: fleet-level validator and contract owner (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`). Not a mado edit.
- F3: lane decision (contract exception vs. correction row). Requires owner choice.
- F4 and F5: append-only lane notes in `corpus/lessons/round-13.md` (to be created by the owner) or a dated errata block.
