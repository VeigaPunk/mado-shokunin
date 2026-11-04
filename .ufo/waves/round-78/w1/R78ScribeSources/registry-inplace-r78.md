# round 78 — in-place registry changes, old → new (R78ScribeSources draft)

Target: `corpus/SOURCES.md` § Registry. The header rule (`corpus/SOURCES.md:5-7`) allows only
`status`, `recheck` and `used-by` to change in place, each logged old→new in the round's lesson.
Draft is prose; the L1 integrates. No committed file is edited by this seat.

## Method (read-only)

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 93a10a13^:corpus/SOURCES.md   # before
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 93a10a13:corpus/SOURCES.md    # after
```

Parsed both revisions as pipe tables (`|`-split, stripped), keyed by the `S\d{3,}` id. Result:
**401 rows before, 401 after, no id added, no id removed.** Exactly eight rows differ, and in
every one the only differing field is index 10 (`used-by`, 0-based over the 11 stripped cells).
No `status`, `recheck`, `scope`, `anchor`, `teaches`, `tier`, `kind`, `opened` or `source` cell
changed anywhere in the table.

The eight-row set is the landed commit `93a10a13` ("round-78: C1 knowledge entry, index row and
frontier bullet; used-by for the eight reopened rows"). This seat's brief named three of them
(S457/S462/S464); the landed change is wider and is reported as observed. No `status` change is
due or made: every row was `mined` before and after (`grep`-counted below, § Census).

## Old → new pairs (field `used-by`, all eight rows)

The delta is identical on every row, so the table gives the literal cells once and the basis
per row.

| id | field | old | new | basis in the entry |
|---|---|---|---|---|
| S457 | `used-by` | `corpus/knowledge/bar-footprint-r77.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `bar-footprint-margins-r78.md:3` (`source:` names S457 `applyExclusive`/`arrangeLayerArray`), `:12` |
| S458 | `used-by` | `corpus/knowledge/bar-footprint-r77.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `bar-footprint-margins-r78.md:3` (layers reply, monitors `reserved`), `:128` |
| S459 | `used-by` | `corpus/knowledge/bar-footprint-r77.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `bar-footprint-margins-r78.md:3` (parent/child band), `:154` |
| S460 | `used-by` | `corpus/knowledge/bar-footprint-r77.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `bar-footprint-margins-r78.md:3` (exclusive-zone contract), `:154` |
| S461 | `used-by` | `corpus/knowledge/bar-footprint-r77.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `bar-footprint-margins-r78.md:3` (placement keys), `:139` (`S461.txt` in the Evidence list) |
| S462 | `used-by` | `corpus/knowledge/bar-footprint-r77.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `bar-footprint-margins-r78.md:3` (margin precedence, anchors, auto-zone call), `:154` |
| S463 | `used-by` | `corpus/knowledge/bar-footprint-r77.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `bar-footprint-margins-r78.md:154` (`S463 stays rejected`) |
| S464 | `used-by` | `corpus/knowledge/bar-footprint-r77.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `bar-footprint-margins-r78.md:3` (client auto zone), `:12` |

Notes for the L1:

1. **No status change.** All eight rows are `mined` in both revisions; the registry-wide status
   histogram is `mined=378 queued=10 rejected=13` before and after.
2. **S463 is a rejected row gaining a used-by path.** That is allowed by the header rule (only
   `used-by` changes) and is supported: the entry's `Sources` paragraph names the rejection
   rather than relying on it. `scripts/sources-census.sh` prints no E-code for it (W02 is about
   a thin `teaches` cell, which is unchanged).
3. **`used-by` addition order** is `r77 entry, r78 entry` on every row; the comma has no space,
   matching the existing multi-path rows in this table (e.g. S455's two-entry cell).
4. This seat's brief named only S457/S462/S464; if the L1 wants the narrower set, three of the
   five extra additions (S458/S459/S460/S461, and S463's) are the entry's other citations and
   would then be uncited. As landed, the entry's `source:` line names all seven and `:116` names
   S463, so all eight additions are consistent with the entry.
5. **Line numbers are pinned to the entry as rewritten during the wave.** They refer to
   `corpus/knowledge/bar-footprint-margins-r78.md` at worktree sha256 `15f30972…` (155 lines,
   HEAD `d27c5ff4`). The entry was rewritten from the 118-line version committed at `93a10a13`,
   so a line-only pointer rots; the S-id plus the section name (`source:`, §1, §4, Evidence,
   Sources) is the durable reference.
