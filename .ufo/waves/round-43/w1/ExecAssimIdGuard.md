# Seat ExecAssimIdGuard — assimilation id guard + renumber map (item 10)

Status: DONE. Scratch-only; the frozen registry, the staging checkout and the counters were read,
never written.

## Files written

| path (from lane root) | what |
|---|---|
| `.ufo/waves/round-43/assimilation/id-guard.md` | the receipt: guard commands + output, the scratch proof, both id lists, the collision count, the 11 files' `source:` inventory, the by-document map, findings |
| `.ufo/waves/round-43/assimilation/renumber-map.tsv` | 25 rows, 4 tab fields: `staged_id, url, new_id_or_held_id, reason` |
| `.ufo/waves/round-43/assimilation/reg-ids` | 226 lane ids (guard output) |
| `.ufo/waves/round-43/assimilation/staged-ids` | 147 staged ids (guard output) |
| `.ufo/waves/round-43/assimilation/collisions` | 34 colliding ids (guard output) |
| `.ufo/waves/round-43/w1/ExecAssimIdGuard.md` | this report |

Artifact hashes (sha256, taken after the last edit of `id-guard.md`):

```
5982338de46f672816963c02dc8b9e3f951024fcc4cc64b25a7ea3b2e6b4b9ab  id-guard.md
18b3e0a7d3b77e9dc267e30996d2a4e7064e5fbedbbd82d6527cbac4e8c8b40a  renumber-map.tsv
76e986db795fd68a4613130cfd2d811cf3f5f2f764caa0cf71abe0e3b15e39b7  reg-ids
079d7538022b0acf8bfadcd150b9db16a54bb550f190361454d4649054f0925d  staged-ids
da4b74d2ac1faeb777e4d5752d159d7a5c08f908d2bb5486f0e1e8ebd3e49980  collisions
```

## Behavior (what was run)

1. Guard exactly as specified: `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` over
   `corpus/SOURCES.md` → `reg-ids`; the same over
   `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md` → `staged-ids`;
   `comm -12` → `collisions`.
   Result: `reg-ids=226`, `staged-ids=147`, `collisions=34`.
2. Guard proof on a scratch registry holding `  | S203 |` (plus an unindented `| S999 |` and a
   four-space `    | S998 |` probe row): `scratch-ids = {S203, S999}`,
   `comm -12 scratch-ids staged-ids = {S203}` (non-empty), printed in `id-guard.md` §2. The proof also
   measures the blind spot: four-space indentation is invisible to the regex.
3. Staged `source:` restriction: 26 source lines across the 11 staged gkeep files, **25 distinct
   staged ids**, **19 distinct documents** (`source_lines=26 distinct_ids=25 distinct_urls=19`).
4. By-document renumber map. Allocations: 2 documents land on **held** rows (Window.cpp → S164,
   WindowRuleApplicator.cpp → S155), 5 on this round's **pins** (DefaultFloatingAlgorithm → S292,
   Target → S293, WindowTarget → S294, GeometricMovableAnimated → S295, host `gkeep.conf` → S297),
   and **12 new ids S300-S311** for the rest (gkeep `ui.py`, gtk4 `set_default_size`, 0.56.0
   Window-Rules, nerd-fonts `glyphnames.json`, and the eight staged-only `lanes/mado/…` sweeps).
   No allocated id falls in S001-S289 or the reserved S290-S299.
5. Reproducibility check in the lane: `comm -12 reg-ids staged-ids | diff - collisions` → empty
   (`guard-reproduced`); `renumber-map.tsv` is 25 rows, every row 4 fields.

## Retained evidence (all in the seat/lane files above, none from scratch)

- Guard counts and both lists: `assimilation/reg-ids` (226), `assimilation/staged-ids` (147),
  `assimilation/collisions` (34) — re-derivable with `wc -l` and `comm`.
- Guard completeness on the registry as it stands: `grep -cE '^ {0,3}\|…S[0-9]{3,}'` = 226 and
  `grep -oE '^[[:space:]]*\|…'` = 226, i.e. no registry row escapes the indentation window.
- Held-row identity: `corpus/SOURCES.md:167` S155 (`…/efb5099…/src/desktop/rule/windowRule/WindowRuleApplicator.cpp`),
  `:176` S164 (`…/efb5099…/src/desktop/view/Window.cpp`), `:170` S158 (`…/efb5099…/src/debug/HyprCtl.cpp`);
  S018's anchor is the lane's own record that tag `v0.56.2` is commit `efb5099…`.
- Pin documents: `.ufo/waves/round-43/receipts/fetch-sha256.txt` (prefixes cited: `f05f2561…`
  DefaultFloatingAlgorithm, `49323833…` Target, `8bcaf370…` WindowTarget, `649f1a8d…`
  GeometricMovableAnimated, `3726e488…` host-gkeep.conf).
- Staged citation inventory: `id-guard.md` §4 (file:line per `source:` line, from
  `grep -nE '^[[:space:]]*[-*]?[[:space:]]*source:'` over the 11 files).

## Risks / findings handed to the L1

1. **Document-level duplicate admissions among the round's own pins.** Pin S291
   (`WindowRuleApplicator.cpp`, tag form) duplicates held S155; pin S296 (`HyprCtl.cpp`, tag form)
   duplicates held S158 (and S018 holds the `blob/v0.56.2` form). Both are the S045
   duplicate-admission shape. The five other code pins match no held row.
2. **The guard under-reports by the reserved band.** 10 staged ids (S290-S299) are absent from
   `collisions` only because the pins are not appended yet; four are cited by the gkeep theme
   (S292, S297, S298, S299) and are renumbered in the map, the other six (S290, S291, S294, S295,
   S296) remain a hazard for whichever seat adds those staged rows.
3. **Eight mapped documents are staged-only paths** (`lanes/mado/roundN/fetch/…`); the ids are
   allocated, but a lane path (or a refusal) is still needed before any of those rows can be opened.
4. **Near-miss id reuse:** staged S297/S292/S293/S298/S299 name different documents than the lane's
   same-numbered rows — a staged row copied with its id intact would silently cite the wrong document.
5. Guard blind spot measured (four-space indentation); harmless for the registry as it stands.

Blockers: none. Tools installed: none (no install was needed; only `grep`, `comm`, `wc`, `sha256sum`,
`diff`, `awk` from the base system were used; no host compositor read was needed or made; no pacman).

Scratch `/fast/scratch/hyaku/mado-r43/ExecAssimIdGuard/` was deleted after the artifacts and this
report were in place; nothing here cites a scratch path as evidence.
