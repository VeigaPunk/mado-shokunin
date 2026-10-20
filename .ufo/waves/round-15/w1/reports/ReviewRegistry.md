# ReviewRegistry — mado round 15, w1 (U6 registry integration)

Scope: adversarial review of the U6 integration risk — append-only source rows, with mutable `status` / `recheck` / `used-by` cells logged old→new. Read-only seat. Baseline `ea0446f`; `corpus/SOURCES.md` had no worktree change at review time (`git diff --stat -- corpus/SOURCES.md` empty). Not run: census validator, `measure.py`, gate, tests, lint. No registry, lesson or knowledge file edited.

## Findings, by severity

**F1 — High. S007 must not be mined in place.**
- `corpus/SOURCES.md:19` S007: `queued`, anchor `§Helper tools + §libinput record and replay, libinput 1.32.0 documentation (opened 2026-10-19)`. No commit, no digest; the page is the mutable `…/doc/latest/tools.html`.
- The in-progress note `corpus/knowledge/input-debugging-boundaries-r15.md` (untracked, 89 L) line 1 cites S007 in its `source:` line. Mining S007 in place would also require editing its anchor, which the header forbids (`SOURCES.md:5-7`: only `status`, `recheck`, `used-by` change in place).
- Owed-anchor rule (`SOURCES.md:115`) lists S006, S008, S009, S010 only. **S007 has the same date-only anchor and is missing from that list** — a registry defect to correct in the round-15 lesson, not in the row.
- Precedent for the correct route: S042 supersedes S006 (`SOURCES.md:54`); S006 stays `queued`, `used-by` `—` (`SOURCES.md:18`). Also QUALITY criterion 17 (`corpus/QUALITY.md:34-35`).
- Fix: mint S051 with `teaches` opening `supersedes S007 —` and a revision-pinned anchor (F6). S007 keeps `queued` and `used-by` `—`.

**F2 — High. S051/S052 identity conflict in the in-flight draft.**
- Reserved mapping (`SCORECARD.md:601-606`; `.ufo/waves/round-15/measure.py:14-23`): S051 = libinput 1.32.0 `tools.rst`; S052 = core Wayland 1.26.0 `wayland.xml`; S007 "never" used.
- The draft's line 1 maps S051 to `/usr/share/wayland/wayland.xml` (host path), i.e. the S052 scope, and cites S007. The draft is therefore inconsistent with both the reserved mapping and the in-flight measure.
- Reuse of S043 for the wl_keyboard/wl_pointer scope is rejected: `SOURCES.md:55` anchors `wayland 1.26.0-1 installed XML:117-177`, scope `wl_registry`, no commit. Changing its anchor or teaches is an immutable-cell edit; only `used-by` may move.
- A host `/usr/share/...` path is not a durable anchor (QUALITY criterion 13, `corpus/QUALITY.md:19-20`). The row's source must be the committed gitlab URL at a commit, with the host file only as an equality check.
- Fix: rewrite the draft's `source:` line to cite S051 and S052 (both `mined`), with S007 at most named as superseded history. Its body reference to S051 for `wl_seat`/`wl_pointer`/`wl_keyboard` must move to S052.

**F3 — Medium. Measurement join: reserved pair now enforced; duplicate-id masking remains.**
- Round-14 precedent `.ufo/waves/round-14/measure.py:167-168,193-194` let one mined A/B id satisfy U6; reciprocity existed only in the U5 branch. The in-flight `.ufo/waves/round-15/measure.py:155` (`U6_SOURCES = ('S051','S052')`) and `:205-223` (both reserved rows mined A/B, `used_by` the note, `inverse` over all mined rows naming it) close that gap. Verified by reading, not executed.
- Still open: `measure.py:149-150` and round-14 `:98-99` key the registry by id with last-wins. A duplicate appended id silently collapses; only census `E03` (`scripts/sources-census.sh:641`) would catch it. Fix: fail on any duplicate id in `measure.py`.
- The round-14 `round14_reserved` block (`round-14/measure.py:546-558`) is hard-coded to S047/S048; the round-15 output must carry an S051/S052 equivalent, not a stale one.

**F4 — High. Append-only and used-by logging are not mechanically enforced.**
- `scripts/sources-census.sh validate` (fleet root) checks row shape, duplicate ids, URL duplicates, enum values and, for `mined` rows only, that each `used-by` path exists (`:538-571`, E11 at `:566-567`). It takes no baseline: an edited immutable cell passes.
- The `supersedes` exemption is a bare regex on `teaches` (`:648`, `teaches !~ /supersedes S[0-9]{3}/`). It does not check that the named id exists, that it is the same URL, or that it is the superseded row. A typo such as `supersedes S999` passes.
- `measure.py` reads a single revision (`git show`, round-14 `:56-60`); it has no diff against a prior revision.
- Historical row diff (static, read-only: row-keyed compare of `git show <rev>:corpus/SOURCES.md` across `5174e15`, `8dbfc93`, `95cbc41`, `32118fc`): existing rows changed only in `status`/`used-by` — S017 and S030 (`8dbfc93`), S005 and S017 (`95cbc41`), S041 (`32118fc`) — and each change appears in its lesson table (`corpus/lessons/round-12.md:122-124`, `round-13.md:47-48`, `round-14.md:88`). Discipline held in four commits; nothing enforces it for round 15.
- Acceptance: a row-keyed baseline diff against `ea0446f` showing (a) only additions after S050 (S051, S052); (b) changes limited to `status`/`recheck`/`used-by` on existing rows, each with an old→new line in `corpus/lessons/round-15.md` under `### Registry mutations — old → new` (table format `round-13.md:42-48`); (c) no removed, reordered, or duplicate-id rows. The clean expected case has no change to existing rows (S007 and S043 untouched).
- Rejection: any change to `opened`, `tier`, `kind`, `scope`, `anchor`, `teaches`, `source` of an existing row; any mutation missing from the lesson table; a `supersedes S0NN` naming an absent id.

**F5 — Medium. `used-by` durability and ordering.**
- All 38 `mined` rows at HEAD point under `corpus/` (checked read-only). The draft note is untracked (`git status`: `?? corpus/knowledge/input-debugging-boundaries-r15.md`). `.ufo/waves/round-15/input-draft.txt` is a wave scratch path; QUALITY criterion 13 makes it non-durable as evidence.
- E11 fails if a `mined` row's `used-by` path is absent on disk (`sources-census.sh:566`). The round-14 and in-flight `measure.py` read the note from `git ls-tree` at the revision (`measure.py:157-158`), so an uncommitted note cannot be joined.
- Acceptance: S051 and S052 `used-by` name the same committed `corpus/knowledge/<note>.md`; rows and note land in one commit.
- Rejection: `used-by` naming `.ufo/…`, an uncommitted path, or a path absent at the commit.

**F6 — Medium. Pins for the two rows (verified by this review, static fetch, 2026-10-20).**
- **S052 (core Wayland XML):** wayland tag 1.26.0 commit `87cc8a8728a923fc57938faa81ba0e74f34ecdc7` (GitLab tag API; tag object `5f430e41…`, use the commit as anchor, as S018 does). `https://gitlab.freedesktop.org/wayland/wayland/-/raw/87cc8a8728a923fc57938faa81ba0e74f34ecdc7/protocol/wayland.xml` → sha256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`, byte-identical to installed `/usr/share/wayland/wayland.xml` (pacman `wayland 1.26.0-1`). Lines: `wl_seat` 2004, `capabilities` event 2030; `wl_pointer` 2138 (enter 2197, leave 2212, motion 2224, button 2244); `wl_keyboard` 2573 (enter 2614, leave 2635, key 2669).
- **S051 (libinput tools):** libinput tag 1.32.0 commit `5cf833b572f5a33663888da321dce0ba1abd82a2` (tag object `c7e6fe66…`). `doc/user/tools.rst` at that commit → sha256 `53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f`; "Helper tools" line 4; `libinput list-devices` 37, `debug-events` 133, `record and replay` 207, autorestart 297. The versioned `…/doc/1.32.0/tools.html` returns 404 (draft already notes this).
- **Version skew:** `pacman -Q libinput` → `1.31.3-1` on this host. S051 `teaches` must say "docs at libinput tag 1.32.0; installed 1.31.3-1 not covered" (QUALITY criteria 15–16, `corpus/QUALITY.md:21-22`). S007's `latest` anchor is mutable and cannot be the pin.
- Rejection: an anchor with `latest`, no commit, or no digest; a host path as the sole anchor; a `teaches` cell that attributes docs to installed behavior.

**F7 — Medium. Draft note cannot be joined as written.**
- Draft (`corpus/knowledge/input-debugging-boundaries-r15.md`) line 1: `source:` lists S007 and S051 (mis-mapped; host path). Lines 4 `covers: U6`, 2–3 `verified-at`/`recheck` present. Under the in-flight measure, neither the S051 nor S052 join holds until the rows are appended, the note is committed, and the `source:` line is corrected.
- Keep as is: the version boundary (lines 15–18) and the separation of `[INF-docs]` from host behavior. The XML line pointers in the draft (2004–2086, 2138–2260, 2614–2699) match the tagged file's `wl_seat`, `wl_pointer`, `wl_keyboard` interface and event lines above.
- Fix: correct `source:` to S051 (libinput) and S052 (Wayland XML); cite S007 in the body only as superseded history.

**F8 — Low. URL collision and census extraction.**
- `sources-census.sh:600-604` takes the first `http(s)://` in the source cell. S043's first URL is `…/docs/html/apa.html`; S052's source cell must put its gitlab raw URL first, or a same-scope match could trigger E04. Cross-scope repeats are `W04` warnings only (`:644-645`).
- Expected census outcome: E04 absent (S051 exempt via `supersedes`, or W04 only); E11 clean once the note is committed; W04 warnings retained for S030/S042/S045 and any new cross-scope repeat (S007/S051).

**F9 — Low. `opened` cell is immutable.** The draft says S007 was "opened 2026-10-20". The registry `opened` cell remains `2026-10-19`; the reopen is recorded in the round-15 lesson, not by editing the row (precedent: S049 correction as a new row, `round-14.md` mutation table).

## Acceptance conditions (all must hold before the round commit)

1. IDs: S051 = libinput tools (F6), S052 = Wayland core XML (F6); appended after S050 (`SOURCES.md:62`), before `## Paths` (`:64`); no reuse of S007, S043, S008, S009, S010.
2. S051 row: tier A, `kind` docs, `status` mined, `opened` 2026-10-20, `teaches` begins `supersedes S007 —`, anchor carries commit `5cf833b5…` and sha `5326…`, `used-by` = the committed note.
3. S052 row: tier A, `kind` spec, `status` mined, anchor carries commit `87cc8a87…` and sha `cc860987…`, source cell gitlab raw URL first, `used-by` = the same note.
4. S007 unchanged: `queued`, `used-by` `—`, all other cells identical to `ea0446f`.
5. Baseline row diff vs `ea0446f`: no immutable cell changed on S001–S050; any `status`/`recheck`/`used-by` change has an old→new line in `corpus/lessons/round-15.md`.
6. Owed-anchor list (`SOURCES.md:115`) gains S007 by append-only erratum in the round-15 lesson or search-log note, not by editing the list entry.
7. Census (`sources-census.sh validate`, for L1 to run once): exit 0; no E03/E04/E08/E11; warnings only W04 for known same-URL cross-scope pairs. Expected post state from HEAD counts (computed, not measured): rows 52 (A 48 / B 1 / C 3); status mined 40 / queued 8 / rejected 4.
8. `measure.py` (round 15): U6 counted only when S051 AND S052 are mined, tier A/B, name the note in `used-by`, and are cited on the note's `source:` line; duplicate id fails. Coverage 6/7 = 8.5714/10 is the only admissible score.
9. Note committed at the path named in `used-by`; not under `.ufo/` (F5).

## Rejection conditions (any one rejects the U6 registry integration)

- R1: S007 mined, its anchor edited, or its `used-by` changed.
- R2: S043 reused, its anchor or teaches changed, or its `used-by` extended to cover wl_keyboard/wl_pointer without a new row.
- R3: a host `/usr/share` path or a `latest` URL as the sole anchor.
- R4: any mutation not in the lesson table, or any immutable cell changed.
- R5: `supersedes S0NN` naming an absent or unrelated id, or used as a bare substring.
- R6: `used-by` path uncommitted, absent at the commit, or under `.ufo/`.
- R7: covers U6 with only one reserved row mined; a duplicate id accepted.
- R8: a row removed, reordered, or the rejected history (S030, S045, S011, S012) dropped (QUALITY criterion 5, `corpus/QUALITY.md:8`).

## Residual risk

- Census and `measure.py` were read, not executed. Their behaviour is taken from source (`sources-census.sh:538-571,600-604,641-649`; `measure.py:149-155,205-224`).
- Pins fetched 2026-10-20 from GitLab (static). Drift between that and the commit must be rechecked at commit time (the note's own `recheck` line requires it).
- `SCORECARD.md` is modified in the worktree and sibling seats are writing round-15 files; a registry edit by a sibling would invalidate this review. Re-run the baseline row diff at integration time.
- `/tmp/mado-r15-wayland-1.26.0.xml` and `/tmp/mado-r15-libinput-tools-1.32.0.rst` are scratch provenance only (QUALITY 13); durable evidence is the committed URL plus sha.

## Verification gaps (for L1, once)

- Run `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` after rows and note land; expect exit 0 and no E-class findings.
- Run the round-15 `measure.py REV` after commit; confirm S051/S052 reciprocity and that a duplicate-id fixture fails once the F3 duplicate check is added.
- Re-run the row-keyed baseline diff vs `ea0446f` on the final commit.
- Re-fetch both pinned raw files and compare sha256 against F6 at integration time.

## Tooling record

No tools installed or updated. Used existing `git`, `curl` (static GET of two GitLab raw files and two GitLab API tag records, written to `/tmp` only), `python3` (read-only row diff over `git show` output, no output file in the repo), and `pacman -Q` (read-only). No credential or auth file opened; no `~/.omp/agent/agent.db*` touched; no omp CLI run; no delegation.
