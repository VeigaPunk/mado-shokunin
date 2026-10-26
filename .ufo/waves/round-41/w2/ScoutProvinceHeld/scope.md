# ScoutProvinceHeld — scope and duplication (round 41 w2)

Target: PROVINCE.md vs held knowledge vs the DATA commit 07f2641 (entry `hyprland-focus-grab-r41.md`, `tools/mado-globals.py`, README row 70).
Method: read-only `git show 07f2641:<path>`, grep over the working tree (lane has no uncommitted edits to PROVINCE/README: `git status` shows only w2 paths),
and one python set-diff of `.ufo/waves/round-13/w1/globals.json` (S041) against the latest session of `.ufo/waves/round-41/fetch/xdph-journal.txt`.
Text grep is the fallback (prose corpus, no LSP symbols); it is not semantic proof.
Labels: OBS observed by me this seat, INF inference, UNK not established.

## 1. Where it belongs in PROVINCE.md

OBS: `grep -n -i -E "core|frontier|adjacent" PROVINCE.md` matches only the table header "Owner and adjacent lanes" (`PROVINCE.md:22`) and prose
"the province accounts for every tracked tool". **PROVINCE.md has no core / frontier / adjacent sections.** Its classes are `Owns (surfaces)` (`:5-10`),
`Refuses` (`:12-14`), "Out of province → report, never absorb", and append-only addenda. The Frontier lives in `corpus/README.md:103` (`## Frontier`).

INF placement:
- *focus-grab protocol* = in-domain: Domain line "desktop & compositor craft ... display behavior on this host"; it is Hyprland protocol/source-read ground, no write
  surface. Precedent: the round-38 addendum (`PROVINCE.md:84-95`) anchored request-socket documentation/source-read knowledge with no new owned surface. The localized-channel
  exclusion (`:68-80`) is respected: the entry cites no localized source and refuses `focus-control-surfaces-r28` §3 (entry header `assimilated-from:`).
- *advertised Wayland globals* = in-domain as read-only evidence of the compositor's protocol set. It is NOT an Owns surface (Owns lists config trees/units, `:5-10`). The
  tool's witness is the user journal of `xdg-desktop-portal-hyprland`. The unit's health/state is tsukuroi's ground (already named at `:23-35` table notes: "unit-state rows sit
  next to tsukuroi's unit-health ground"). mado reads advert lines only.
- `tools/mado-globals.py` is a lane tool that spawns `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso` (`tools/mado-globals.py:45`, `--live`). The
  round-23 rule says the province "accounts for every tracked tool it runs" (`PROVINCE.md:20`). OBS: `grep -n -E "mado-options|mado-globals|mado-eventq|mado-wsrules" PROVINCE.md` → no hit, so the
  inventory already stopped at round 26 (`mado-binds`, `mado-anims`); `mado-options`, `mado-wsrules`, `mado-eventq` (which also runs `journalctl`, `tools/mado-eventq.py:242`) are equally unlisted.
  So the omission is not new to this round, but `mado-globals.py` is the second journal-reading tool and the first whose only input IS a journal. It is a gap, not a violation:
  no data bytes of the defect kind (secret, write) are involved.

## 2. Duplication against held ground

| held ground | what it holds | does the new work duplicate it? |
|---|---|---|
| `wayland-protocol-boundaries-r13.md` + S041 (`.ufo/waves/round-13/w1/globals.json`, SOURCES `:53`) | the advertised/bound/behaviour split; a `wayland-info` registry capture, 2026-10-20T04:10:03Z, 72 records / 71 unique, host 0.56.2 `efb5099` | **Datum overlap: yes.** OBS: S041 contains `{'interface': 'hyprland_focus_grab_manager_v1', 'version': 1}`. The entry's §3 headline "does this host advertise it? one advert, version 1" restates an already-held fact from a second vantage. |
| same note, method | "Advertisement is not feature behavior"; "Hyprland-specific ... require their own owning-repository authority" | The entry *applies* it (§7); not a duplicate, and consistent with it. |
| `xdg-portal-routing-r12.md` | portal `.portal` descriptors, `portals.conf`, ScreenCast v6, S037 | No overlap: OBS `grep -n -i "PortalManager\|onGlobal\|registry\|global" ` hits only the `GlobalShortcuts` table row (`:50`); nothing on the xdph registry log. The entry's only use is S037 (installed 1.4.1-2), correctly cited as held. |
| `idle-lock-route-r17.md:130` | `[UNK]` whether the compositor exposes `hyprland-lock-notify-v1` | Not the entry's claim, but S041 and the journal both list `hyprland_lock_notifier_v1` ver 1. **Stale UNK** answerable at the advertisement level (binding still open). Append-only note, no edit to r17. |
| prose on focus grab | OBS `grep -rniE 'focus.?grab\|focus_grab' corpus PROVINCE.md SKILL.md tools README.md` (working tree) → only the entry, round-41 lesson, README row 70, SOURCES, and `tools/mado-globals.py`. At base ab2bfaa also none (lesson cites the same grep). | No prose duplicate. The entry's "holds no focus-rule knowledge" §5 line is accurate. |

**Duplication finding D1 (DATA, entry):** the entry never cites S041. OBS: `git show 07f2641:corpus/knowledge/hyprland-focus-grab-r41.md | grep -c S041` → `0`; its `source:` header cites S283–S289 + S037 only.
ScoutHeldOverlap (w1) already told the L1 "The entry must cite S041 as a held second-client advertisement" (`w1/ScoutHeldOverlap.md:7-10`). It was not applied. The consequence is a weaker entry: its §3 "UNK: which process binds it" and "63 in the latest session" are
stated without the second, earlier, independent vantage that already says `focus_grab` v1 was advertised to a client (not just logged by the portal) on 2026-10-20.

**Duplication finding D2 (DATA, entry; claim contradicted by held data):** §3 INF says "Only the second session is a whole advertisement ... 63 distinct names ... the only session that can be compared with the compositor's registry as a whole."
OBS (python set-diff, this seat): S041 71 unique (name, version) pairs; journal session 1952 63; `only journal = []`; `only S041 =`
`ext_foreign_toplevel_image_capture_source_manager_v1@1, ext_image_copy_capture_manager_v1@1, wl_drm@2, wl_output@4, wp_color_manager_v1@3, wp_drm_lease_device_v1@1, wp_linux_drm_syncobj_manager_v1@1, zwp_linux_dmabuf_v1@5`.
`wl_output` is in every compositor's registry, yet it is absent from the 63 (`grep -n wl_output xdph-journal.txt` → only pid 1918 lines 9,26,29,35,38,70,73). So the 63 is NOT the compositor's registry as a whole;
S041 (and the pid-1918 slice) hold 8 names it lacks. Cause UNK (portal log vs client registry vantage, boot/session timing, the 1952 session's 13:36 start). The word "whole advertisement" and "the compositor's registry as a whole" are unsupported.
Suggested fix: reword to "the latest portal session's 63 names, a subset of S041's 71 (8 missing, incl. wl_output)", and cite S041 for the focus-grab advert and the superset. Note this does not change the C2 predicate target (the entry is admitted on its own clauses).

**Duplication finding D3 (DATA, README row 70 is malformed):** OBS: python scan of `git show 07f2641:corpus/README.md` → every coverage-map row `| \`knowledge/...` has 3 cells except line 70, which has **2** (note + holds, no Sources). The table header is `| Note | Holds | Sources |` (README `:10`). The row therefore (a) renders with an empty Sources cell
and (b) omits S283–S289/S037 that every adjacent row (S253, S218–S220, S280–S282) lists. The check `quality/check-index-rows.py` is the row-fidelity gate; I did not run it (not assigned). Fix below.

**D4 (tool, mild):** `tools/mado-globals.py` classes (`CLASSES`, `:48-71`) are a new curated list of 10 classes including `focus-grab`; it is not a duplicate of `wayland-protocol-boundaries-r13.md`'s safe-recheck snippet (that one needs a `wayland-info` client = Wayland socket connection, forbidden here), and is complementary: no-socket witness vs client witness.
Neither of them holds a per-name class table, so no duplicate. The one scope caveat: the tool header states "the one read-only witness ... that needs no socket connection", whereas S041/`wayland-info` is the held other witness; the docstring should not imply uniqueness beyond "needs no socket" (it doesn't, literally). No defect.

## 3. Coverage-map row vs Frontier: should either move?

- **Do not move or edit the r13 row (`README.md:38`) or r12 row (`:36`).** They are admitted historical rows; the entry extends U4's advertised-global route to one concrete Hyprland protocol and does not retract either. Append-only is the lane's rule.
- Row 70 stays where it is (the newest row, last in the coverage map), with the third cell added. No `covers:` token: the entry header has none; prior rows say "covers U4/U5" in the row text only when the note does. Add "extends U4" text to the Holds cell rather than editing r13.
- **Frontier:** add one bullet at the top (precedent: the round-40 bullet is first under `## Frontier`, `README.md:103-105`). The entry's own UNKs are the open list. No existing Frontier bullet is *closed* by this entry (the r13 bullet's "Feature behavior ... remain unclaimed" stays true).

### Recommended exact edits (for the L1; I edit nothing tracked)

**E1 — `corpus/README.md`, coverage-map row 70: append a Sources cell and tighten the globals claim.** Replace the final `... a decision table of what is observed, inferred and unknown. |` with:

`... a decision table of what is observed, inferred and unknown. The latest portal session's 63 names are a subset of the earlier client capture's 71 (S041, which also holds the focus-grab advert, version 1; 8 names such as `wl_output` are absent from the portal log, cause unknown); who binds the manager on this host is unknown. | `source:` S283–S289 and S037 in [SOURCES](SOURCES.md); held S041 (`.ufo/waves/round-13/w1/globals.json`); fetched receipts `.ufo/waves/round-41/fetch/`; tool `tools/mado-globals.py`; recheck 90d or on a Hyprland tag after v0.56.2. |`

(Keep the "63 globals in the latest portal session" wording only if the S041 subset clause is added; otherwise drop "63".)

**E2 — `corpus/README.md`, `## Frontier` (`:103`), insert as the first bullet:**

`- Round 41 moves the focus-grab protocol surface onto sourced ground ([focus grab](knowledge/hyprland-focus-grab-r41.md): two interfaces, five requests, one \`cleared\` event; the compositor's seat-grab enforcement; this host's advert via S289 and the held S041; one client's lifecycle; issue 565 as the rule-level counterpart) and adds \`tools/mado-globals.py\`, a no-socket census of the globals the compositor advertised to its portal. Still open: which process binds \`hyprland_focus_grab_manager_v1\` on this host, how \`CSeatGrab\` routes an event outside the set, the "implementation-defined criteria" that clear a grab, whether 0.56.2 still shows issue 565's momentary focus steal, and why the portal's latest session lacks eight names the earlier client capture holds (S041). Advertisement of \`hyprland_lock_notifier_v1\` is held (S041, journal) but binding stays open; \`idle-lock-route-r17.md\` keeps its dated UNK.`

**E3 — `PROVINCE.md`, append after the round-38 addendum (`:84-95`, append-only; mirror its form), title `## Round-41 addendum — advertised-globals tool and focus-grab knowledge ground (append-only)`:**

`The lane's \`tools/mado-globals.py\` reads one saved or live user-journal stream (\`journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso\`) and prints one census of the \`Got interface:\` lines the portal logged; it connects to no socket, runs no other process, binds no global and writes nothing (\`--selftest\` writes only an ephemeral private temp dir). The journal is read as evidence of the compositor's advertised protocol set only; the portal unit's health and package state stay tsukuroi's, and no host service is touched. The focus-grab note (\`corpus/knowledge/hyprland-focus-grab-r41.md\`) is documentation/source-read knowledge of a Hyprland protocol plus one dated host advertisement count: no client is run, no input injected, no surface is added to Owns. It cites no localized-channel source (see the round-36 refinement).`

(An inventory row for `mado-globals.py` in the round-23 table is the other acceptable form; the addendum is cheaper and has the r36/r38 precedent. `mado-options.py`, `mado-wsrules.py` and `mado-eventq.py` are equally unlisted and are out of this seat's scope; report, not fix.)

**E4 (optional, append-only, not required by the predicates) — `corpus/SOURCES.md`:** add S041's used-by list the entry id (`corpus/knowledge/hyprland-focus-grab-r41.md`) if the entry cites S041 after D1 is fixed; S037's used-by is already updated (`SOURCES.md:49`).

## 4. Findings summary

| id | attacks | verdict | repro |
|---|---|---|---|
| F1 / D1 | entry omits the held S041 | DEFECT (data) | `git show 07f2641:corpus/knowledge/hyprland-focus-grab-r41.md \| grep -c S041` → 0; `jq '.globals[]\|select(.interface=="hyprland_focus_grab_manager_v1")' .ufo/waves/round-13/w1/globals.json` → present |
| F2 / D2 | entry §3 "whole advertisement" / "registry as a whole" | DEFECT (data, overclaim) | python set-diff in this report: 8 names only in S041; `grep -n wl_output .ufo/waves/round-41/fetch/xdph-journal.txt` → only pid 1918 |
| F3 / D3 | README row 70 | DEFECT (data, structural) | cell count of row 70 is 2 vs 3; header `README.md:10` |
| F4 | PROVINCE tool inventory / addendum | GAP (data, doc) | `grep -n mado-globals PROVINCE.md` → empty |
| F5 | stale UNK in `idle-lock-route-r17.md:130` | note only (no edit; append-only) | `grep -n hyprland_lock_notifier .ufo/waves/round-13/w1/globals.json` present |
| F6 | PROVINCE has no core/frontier/adjacent headings | observation | `grep -n -i -E "core|frontier|adjacent" PROVINCE.md` |

No defect found in: any move of the r12/r13 rows (none needed), duplication against `xdg-portal-routing-r12.md` (no registry-log content), the refusal of the localized section (`PROVINCE.md:68-80` holds; the entry cites none), or duplication of the tool against held code (no globals-census tool exists; `ls tools` has no sibling).
No predicate defect found in scope: nothing here attacks the frozen counters (C1/C2 targets are unaffected by D1-D3; D3 may or may not be caught by C2 clause for README row and `check-index-rows.py` — not run).

## Evidence / state
Tools: none installed. Commands: `git show 07f2641:...`, grep/python read-only parses of tracked files and receipts; no counter run, no host command, no network. Wrote only `.ufo/waves/round-41/w2/ScoutProvinceHeld/scope.md` and `.ufo/waves/round-41/w2/ScoutProvinceHeld.md`. `/tmp/r41-readme.txt` scratch left for deletion.
