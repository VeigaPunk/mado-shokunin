# ReviewRowSchema — staged rows S190, S191, S197

Lane: mado-shokunin · Round 33 / w1 · 2026-10-24
Input: `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md` — staged rows only, nothing appended.
Schema authority: fleet `scripts/sources-census.sh` (SOURCES-CONTRACT-v1, 11 columns, statuses queued|mined|rejected).

## Method (evidence)

1. Field dump: `awk -F'|'` over line 11 (S190), 12 (S191), 18 (S197) of the staged file. `NF=13` for all three — the column count is correct, so no E01 from these rows.
2. Escaped-pipe sweep: `grep -n '\\|'` over the staged file hits lines 42, 51, 52, 71 and 121–138 — none of them the three scoped rows. S190/S191/S197 contain no escaped pipe.
3. Validator run on a throwaway lane: staged rows 11/12/18 placed under a `## Registry` heading, `corpus/knowledge` symlinked to this lane's real knowledge dir, then:

   ```
   bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-24 <tmp-lane>
   E09 S190 · E09 S191 · E09 S197 · E11 S190 · E11 S191 · E11 S197 (×2 paths)   exit=1
   ```

## Findings — cells that fail the census, and the normalized cell

### F1 · `recheck` — prose instead of a cadence (E09, all three rows)

Staged shape (sha prefix elided): `` on-release — re-pull at tag `0.15.0` and compare sha256 (expect prefix …) (ran 2026-10-23) ``.

Why it fails: the validator accepts only an ISO date, `NNd`, or a symbolic token matching `^[A-Za-z][A-Za-z0-9 _-]*$`. The em dash, backticks, parentheses and dots in the prose break the symbolic match → `E09`.

Side effect: in `overdue` mode these rows print neither `cadence` nor `overdue` (verified: exit 0, empty output). A prose recheck silently removes the row from recheck tracking.

Normalized cell: `on-release`. This is the registry's own dominant shape (131 existing rows) and matches the Waybar rows already registered (S053, S054). No information is lost: the tag and expected sha256 prefix already live in each row's `anchor` cell; the ran-date belongs in the round log (`LOG.md`), not in a schema-checked cell.

### F2 · `used-by` — paths pointing at unadopted knowledge entries (E11)

Every `used-by` path in the three rows fails `[ ! -e "$dir/$path" ]` against this lane's root:

| row | staged used-by cell | on disk |
|---|---|---|
| S190 | `corpus/knowledge/waybar-module-text-route-r25.md` | no |
| S191 | `corpus/knowledge/waybar-module-text-route-r25.md` | no |
| S197 | `corpus/knowledge/host-bar-and-idle-binding-r26.md`, `corpus/knowledge/event-delivery-limits-r26.md` | no, no |

`corpus/knowledge/` holds 46 adopted files; none of the three staged names is among them.

Normalized cell: `—` (and accept W03 "mined but unused" — a warning that never fails the lane or the census exit code), **unless** the same append adopts the knowledge entries under those names. Verified existing candidates for option (b), requiring a coverage read before adoption:

- `corpus/knowledge/ipc-contract-r25.md` — covers the two sockets, request grammar and event framing and already mentions Waybar; plausible adopted target for S190's transport claims.
- `corpus/knowledge/waybar-observation-boundaries-r16.md` — already cited by the registered S054 Waybar-module row; plausible for S191/S197 label-text claims.

Naming an unrelated existing file would be evidence corruption; naming the staged-but-nonexistent path is a guaranteed E11. Between `—` and an unverified path, `—` is the safe normalization.

## Checks that passed (no change needed)

- NF=13 in all three rows; no unescaped and no escaped pipe inside their cells.
- No E02/E03: S190, S191, S197 do not exist in `corpus/SOURCES.md` yet (verified by id grep).
- No E04/W04: their URLs are distinct from the two registered Waybar rows (S053 man page, S054 `src/modules/custom.cpp`).
- No E05–E08, E10: kind `code`, tier `A`, status `mined`, opened `2026-10-23` all pass enum/range checks; community-at-A not applicable.

## Adjacent blockers in the same staged file (outside the three scoped rows)

1. **Duplicate ids.** S186, S187, S188, S189 and S196 are staged *and* already present in `corpus/SOURCES.md` (grep-verified, count=1 each side). Appending the whole file trips E03 five times. Only S190, S191, S197 are new.
2. **Missing heading.** The staged file has no `## Registry` heading; validating it standalone reports E12 for every row. The rows must land under the existing `## Registry` in `corpus/SOURCES.md`.
3. **Escaped pipes elsewhere.** Staged rows at lines 42, 51, 52, 71 and 121–138 contain `\|` (e.g. a `case` pattern cell). awk splits fields on the pipe regardless of the markdown escape, so those rows arrive with NF≠13 → E01 once appended. Same append carries them; they need the same normalization pass.

Nothing appended; nothing outside `.ufo/waves/round-33/` written.
