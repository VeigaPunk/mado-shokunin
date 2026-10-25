# RevengerId — id-assignment collisions, wave S203–S210 vs staged package

Revenger seat, round-35 w1. Files re-read at write time (2026-10-24):
`frozen.json` (`.ufo/waves/round-35/c1/frozen.json`), `corpus/SOURCES.md` (live,
192 rows, max id S202), `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md`
(147 rows, S203–S349, md5 `64a65037505cbca282e86bf3729c0c2c` — regenerated
mid-wave, see C6), `MERGE-REPORT.md`, `lanes/mado/ID-REMAP.md`.

**The collision is not constructible — it is already scheduled.** The frozen
predicate assigns S203–S210 to the wave's eight host-research receipts; the
staged package's register independently allocated the same eight ids
("lane registry ends at S202; first staged id is now S203" — ID-REMAP.md). Both
parties read "registry max S202" and drew the same next-free ids. Both claims are
already written down.

## C1 — Registry row collision (8 ids, guaranteed)

Staged `SOURCES.append.md` rows S203–S210 name *different documents* than the
wave receipts:

| id | staged row names | wave receipt names |
|---|---|---|
| S203 | Hyprland IPC page, current upstream (hyprland-wiki `c04680a2`) | omarchy-first-run installer (host) |
| S204 | Hyprland IPC page, 0.56.0 version-matched | journalctl `omarchy-toggle` absence + 12 first-run scripts |
| S205 | Hyprland wiki Dispatchers, Lua config API | idle-lock chain present state (hypridle/hyprlock probes) |
| S206 | EventManager.cpp @ v0.56.2 | host `~/.config/waybar/config.jsonc` idle-indicator block |
| S207 | Waybar backend.cpp @ 0.15.0 | host `idle.sh` indicator script |
| S208 | Waybar window.cpp @ 0.15.0 | host `omarchy-menu` Idle Lock dispatch |
| S209 | Japanese ArchWiki Hyprland translation | host waybar dated-config backups sweep |
| S210 | cnblogs Fedora hyprland post (tier C) | host `toggles/hypr` directory sweep (0 idle entries) |

Adopt-checklist step 3 is `Append SOURCES.append.md to corpus/SOURCES.md` — no
precondition checks id-freeness. With the wave's rows in place, the append
produces **two rows per id for S203–S210**. Consequences:

- `count.py` (`rows_for` → `len(rows)==1` else `row=None`): all eight frozen
  cites open → `TARGET_MISSED`. Loud for the predicate.
- `sources-census.sh` validator emits **E03 duplicate id** for all eight (checked
  `validate` awk at :641). Loud *if* the census runs on the adoption path — the
  MERGE-REPORT checklist never invokes it.
- For every other consumer of the registry the dupes are silent: any
  `source: S203` cite is ambiguous between two unrelated documents.

## C2 — The silent-land variant `count.py` cannot see

`count.py` scores a row on exactly four cells plus id: `used-by` (cs[10]) ==
frozen citing set, `status` (cs[7]) == `mined`, `recheck` (cs[9]) cadence-valid,
`anchor` (cs[5]) *contains* the frozen receipt sha256. **`source`, `kind`,
`tier`, `scope`, `teaches` are never compared against the receipt.**

So the following repair is legal under the predicate and semantically corrupt:
after the C1 append, an operator "fixes" the duplicates by keeping the staged
row S203 and editing its `used-by` to
`corpus/knowledge/idle-lock-never-asked-r12.md`, then pastes the wave receipt's
sha256 into its `anchor` cell (anchors here are free text). Verbatim quote still
matches the receipt → cite closes → `TARGET_MET` — while the registry now says
the lane's omarchy-first-run evidence is the Japanese… (S209) / IPC-page (S203)
documents. Green predicate, wrong source. Any dedup tooling that "keeps last
write" produces the same shape by accident.

## C3 — Entry-path collision (byte-name, both directions lose)

The frozen `entries` map names three paths that do not exist in the lane but
exist in the staged package with **different cite sets**:

| path | wave cites | staged file cites |
|---|---|---|
| `corpus/knowledge/idle-lock-never-asked-r12.md` | S203, S204 (+`gate-quote:`) | S315, S316 (no gate-quote lines) |
| `corpus/knowledge/idle-lock-chain-armed-r14.md` | S205 (+`gate-quote:`) | S327 |
| `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` | S206–S210 (+`gate-quote:`) | S335, S336, S337, S340, S342 |

(Verified by grep: staged files carry `source:`/`Cites:` lines, zero
`gate-quote:` lines; the wave golden carries both.) Adopt step 4 (`copy each
knowledge/<path> into corpus/knowledge/<path>`) overwrites, never merges:

- **Adopt first, wave second:** wave files overwrite staged → staged rows
  S315/S316/S327/S335/S336/S337/S340/S342 keep `used-by` pointers to files that
  no longer cite them — silent used-by rot, 8 staged rows orphaned.
- **Wave first, adopt second:** staged files overwrite wave → `gate-quote:`
  lines vanish → 8 open cites, `TARGET_MISSED`. Loud for the predicate, and the
  staged entries claim "new-file" while clobbering existing wave files — the
  checklist's only protection is step 6's "duplicate target" language, which
  does not list these three.

## C4 — Same-document double registration

The wave's eight receipts re-open the same host documents the package staged
under S315/S316/S327/S335/S336/S337/S340/S342 (mapping verified row-by-row:
S203↔S315 first-run script; S204↔S316 never-asked probe; S205↔S327 chain state;
S206↔S335 waybar config; S207↔S336 idle.sh — sha256 `6d8d2c11…` matches;
S208↔S337 omarchy-menu; S209↔S340 dated backups; S210↔S342 toggles sweep).
If both sides' rows land, the registry holds two ids per document → census
E04 duplicate-url-class noise and the S045 "duplicate source admission"
precedent applies.

## C5 — Silent land *without* any collision: amendment cites into live files

Adopt step 5 appends `amendments/corpus/knowledge/*` into existing lane entries.
Those payloads carry staged-meaning ids: `ipc-contract-r25.md` cites
**S203/S204/S206**, `waybar-module-text-route-r25.md` cites **S207/S208**,
`dispatcher-semantics-r25.md` cites **S205**,
`two-literature-coverage-r25.md` (new file) cites **S209/S210/S211**.
Post-append, the lane's live `ipc-contract-r25.md` contains `source: S203` — a
line that, under the wave's registry, resolves to the omarchy-first-run script,
not the IPC page. The cite is well-formed, resolves to an existing row, and is
wrong. No gate checks `source:`-to-row coherence, so this lands silently unless
the staged ids are moved first. (This is exactly the failure ID-REMAP.md warns
about: "a round-blind substitution … while every structural check stayed
green.")

## C6 — Mutable package + renumbering generations

`SOURCES.append.md` on disk was regenerated this wave: an earlier read returned
147 rows numbered **S197–S336** (gen-B numbering); current bytes hold
**S203–S349** (gen-C, post-REMAP). Same packaging timestamp (Oct 24 23:26).
Every generation renumbers the id space; lane artifacts that name package ids
are pinned to the generation they read. `corpus/lessons/round-32.md` (:108-113)
and `round-34-verifier-spotcheck.md` (:192,250) already cite staged ids
("S189", "S195", "S205", "S209", "S210", "S211", "S222"…, two-literature ids)
from older numbering — under the current package those tokens name different
rows or none. Any staged-id reference recorded before adoption is a
mis-binding-in-waiting. MERGE-REPORT's own premise ("lane registry currently
holds 192 rows; first staged id is S203") is stale the moment the wave's rows
land — the package's freeness check ran at packaging time, not adopt time.

## What the lane should do

1. **Do not append `SOURCES.append.md` while the wave's S203–S210 rows stand.**
   The only non-colliding orders are (a) lane keeps wave ids, renumber staged
   S203–S349 a second time (base S350; touch the register plus the 4 amendment
   files' and `two-literature-coverage-r25.md`'s `source:` lines — a remap of
   147 ids, error-prone, already done once and it failed to prevent this); or
   (b) renumber the wave to S350–S357 — re-freeze `frozen.json` (entries map +
   receipt names), rename `fetch/S2xx.receipt.txt`, rewrite the three entries'
   `source:`/`gate-quote:` lines and any rows already written. (b) touches ~25
   wave-internal artifacts and leaves the package untouched; (a) is cheaper in
   count but contradicts the package's own completed remap.
   **Recommendation: (b)**, or hold adoption until the wave's rows are in the
   registry and then renumber the *package* — never renumber whichever side is
   already committed to `corpus/SOURCES.md`.
2. **Three same-name entries: fold, don't copy.** Wave versions are canonical
   (they carry the `gate-quote:` lines the predicate needs); append the staged
   texts as dated amendment sections, keeping both cite sets (wave ids +
   staged S315+ ids). This satisfies both `used-by` closures; a copy lands
   either C3 direction.
3. **Same-document rows (C4):** keep the wave rows (fresh host re-opens, receipt
   -pinned); mark the staged S315/316/327/335/336/337/340/342 rows
   `supersedes`-style or drop them and repoint the staged entries' `source:`
   lines to the wave ids — otherwise E04 fires on adopt.
4. **Fix the adopt checklist** (operator-side, name it in the round report):
   precondition step 3 on `comm -12 <(registry ids) <(append ids) = ∅` *at adopt
   time*, and pin the package by sha256 at freeze — the file has already mutated
   once mid-wave.
5. **Predicate blind spot to name for a later round:** `count.py` binds a cite
   only to `used-by`/`status`/`recheck`/`anchor∋sha` — a row about a different
   document can close a cite (C2). A future predicate should also check the
   row's `source` cell names the receipt's document.

Bottom line: the only *silent* loss paths are C2 (shape-only row check), C3a
(staged cites rot when wave files overwrite), and C5 (amendment cites landing on
same-numbered wrong rows). Everything else fails loudly at the predicate — but
only at the predicate; the registry and census don't share the predicate's view.
