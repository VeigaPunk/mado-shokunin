# ScoutQuarantineB — mado never-checked rows vs SOURCES.md

Source register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(second table, "Rows whose quotes were NEVER CHECKED"; the class legend's
`unreachable` class — the checker never attempted a match, so no row below is
a fabrication verdict). Registry grepped:
`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`
(grep for each id and each locator, whole file, case-sensitive).

| id | register round | register class / why not checked | cited source / locator | id in SOURCES.md | locator in SOURCES.md | classification |
|---|---|---|---|---|---|---|
| S199 | round2 | `unreachable` — "the cited source could not be fetched, so no quote was checked" | https://blog.csdn.net/2301_76324845/article/details/149787804 | no | no | NOT-IN-REGISTRY |
| S200 | round2 | `unreachable` — "the cited source could not be fetched, so no quote was checked" | https://blog.csdn.net/lxyoucan/article/details/164457293 | no | no | NOT-IN-REGISTRY |
| S209 | round3 | `unreachable` — "the gate block named no locator, so no quote was checked" | `## Gate — S209` (prose anchor, no URL) | no | n/a — no locator named | UNVERIFIABLE |
| S222 | round4 | `unreachable` — "the gate block named no locator, so no quote was checked" | `## Gate — S222` (prose anchor, no URL) | no | n/a — no locator named | UNVERIFIABLE |
| S223 | round4 | `unreachable` — "the gate block named no locator, so no quote was checked" | `## Gate — S223` (prose anchor, no URL) | no | n/a — no locator named | UNVERIFIABLE |
| S225 | round4 | `unreachable` — "the gate block named no locator, so no quote was checked" | `## Gate — S225` (prose anchor, no URL) | no | n/a — no locator named | UNVERIFIABLE |
| S235 | round5 | `unreachable` — "the gate block named no locator, so no quote was checked" | `## Gate — S235` (prose anchor, no URL) | no | n/a — no locator named | UNVERIFIABLE |

## Notes

- All seven rows sit in the register's never-checked table, not the
  `payload-absent` table. Per the register's own legend, `unreachable` rows
  must be re-fetched or marked unverifiable — none is a confirmed fabrication.
- S199/S200 name real CSDN URLs; neither the URL nor the id appears anywhere in
  `corpus/SOURCES.md` (442 lines grepped). They are register-side rows with no
  registry counterpart under any id → NOT-IN-REGISTRY.
- S209/S222/S223/S225/S235 cite only a `## Gate — Snnn` prose anchor. The
  register names no resolvable locator, so no quote could ever have been
  checked and no registry row can be matched or excluded → UNVERIFIABLE. Their
  ids are also absent from SOURCES.md, but absence cannot be distinguished
  from an unlocatable citation.
