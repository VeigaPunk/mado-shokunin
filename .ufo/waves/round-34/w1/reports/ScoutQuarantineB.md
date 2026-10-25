# ScoutQuarantineB — mado prose-class slice rows vs SOURCES.md

**Scope:** the seven never-checked mado rows in the corpus-expansion-1
absent-defect register (S199, S200, S209, S222, S223, S225, S235), classified
against `corpus/SOURCES.md`. Read-only over the register; no registry edits.

**Method:**
1. Read `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
   (lines 349-355 hold all seven rows in the "Rows whose quotes were NEVER
   CHECKED" table — the class legend's `unreachable` class; no quote was ever
   matched, so none is a fabrication verdict).
2. Grepped `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`
   (442 lines) for `S199|S200|S209|S222|S223|S225|S235` — **no matches**.
   Grepped for the two locators (`csdn.net`, `2301_76324845`, `lxyoucan`,
   `149787804`, `164457293`) — **no matches**.

**Result (full table at `.ufo/waves/round-34/scratch/ScoutQuarantineB/table.md`):**

| id | register round | register class / why not checked | locator | classification |
|---|---|---|---|---|
| S199 | round2 | `unreachable` — cited source could not be fetched | https://blog.csdn.net/2301_76324845/article/details/149787804 | NOT-IN-REGISTRY |
| S200 | round2 | `unreachable` — cited source could not be fetched | https://blog.csdn.net/lxyoucan/article/details/164457293 | NOT-IN-REGISTRY |
| S209 | round3 | `unreachable` — gate block named no locator | `## Gate — S209` (prose anchor only) | UNVERIFIABLE |
| S222 | round4 | `unreachable` — gate block named no locator | `## Gate — S222` (prose anchor only) | UNVERIFIABLE |
| S223 | round4 | `unreachable` — gate block named no locator | `## Gate — S223` (prose anchor only) | UNVERIFIABLE |
| S225 | round4 | `unreachable` — gate block named no locator | `## Gate — S225` (prose anchor only) | UNVERIFIABLE |
| S235 | round5 | `unreachable` — gate block named no locator | `## Gate — S235` (prose anchor only) | UNVERIFIABLE |

**Findings:**
- 0 rows are IN-REGISTRY-SAME-ID or IN-REGISTRY-DIFFERENT-ID — no id or
  locator string from these register rows appears anywhere in SOURCES.md.
- S199/S200: named CSDN locators exist but are absent from the registry under
  any id → NOT-IN-REGISTRY. Both are `unreachable`, not `payload-absent`; the
  register itself warns against treating them as fabrications.
- S209/S222/S223/S225/S235: the register cites only a `## Gate — Snnn` prose
  anchor. No locator was ever named, so no quote could be checked and no
  registry row can be matched or ruled out → UNVERIFIABLE. Their ids are also
  absent from SOURCES.md, but that absence cannot be distinguished from an
  unlocatable citation.

**Not done (out of scope):** no re-fetch of the CSDN URLs attempted; the task
bounds the check to register-vs-registry string evidence.
