# RerunCensus — mado round-43 w2 (falsify the landed data)

**Attacked:** `.ufo/waves/round-43/receipts/census-after-data.txt` and the "226 → 234 rows" claim of the data commit.
**Revs:** base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`, data `1959770657f1f8665097c1aed4be6c1cbb07139f` (lane HEAD
`2a3707c` during the run; `git diff 1959770 HEAD -- corpus/SOURCES.md` = 0 bytes, so the worktree registry **is** the
data-commit registry: blob `3c564e7d…` on both sides).
**Verdict: both attacked artifacts HOLD at the data commit. No defect found on this axis.** Evidence: seat
`receipt.txt` + files in `.ufo/waves/round-43/w2/RerunCensus/`. No w1 finding is re-reported: the one w1 result this
report touches (F4, `ExecHarmBase.md` finding 3) is re-measured at the data commit and shown still to hold.

## Findings

**F1 — the census receipt reproduces byte for byte (support).**
`./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → the same 9 lines as
`receipts/census-after-data.txt` and **exit 0** (`census-validate-fleet-root.txt`, sha256 `858315d2…`). The committed
receipt is exactly that stdout plus one `exit=0` line (sha256 `53f2201e…`; `diff` with the last line removed is empty).
The `mado ok …/corpus/SOURCES.md` path, the 7 × W04 set and the W01 S277 line are all reproduced, not stale.

**F2 — 226 → 234 is true, measured two independent ways (support).**
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` gives **226** at base and **234** at data (seat copies whose
sha256 match the `git show` blobs, `df130e81…` / `b603fe42…`). The census tool's own `census` mode agrees:
`rows` 226 → 234, `tier.A` 216 → 224, `status.mined` 207 → 215, with `tier.B` 3, `tier.C` 7, `queued` 10, `rejected` 9,
`invalid` 0, `missing` 0 unchanged. The +8 is exactly eight tier-A mined rows; no other status moved.

**F3 — the row delta is exactly S290–S297, well-formed, and nothing else changed (support).**
`diff` of the two registries is three hunks: `167c167` (S155), `170c170` (S158), `238a239,246` (eight appends).
`check-registry.py` (74 checks, 0 FAIL): every new row splits to **11 cells** (NF 13), `status=mined`,
`opened=2026-10-26`, `tier=A`, `used-by=corpus/knowledge/hyprland-gkeep-geometry-r43.md`; base row order is a strict
prefix (append-only, new ids last, unique, ascending); the other **224** rows are byte-identical. S155/S158: columns
id..recheck byte-equal, used-by item lists 1→2 and 5→6 with prior items unchanged in order and the entry appended once.
One precision: the append is not a strict byte-prefix — the base cells end `…r8.md ` / `…r24.md ` (trailing space, no
comma) and the data cells read `…r8.md, corpus/knowledge/hyprland-gkeep-geometry-r43.md `, i.e. `, <entry> ` replaces the
trailing space. "One item appended" is right; "byte-prefix extended" would not be.

**F4 — the W-set difference base → data is empty (support).**
Run against faithful base and data trees (`git archive` of each rev, registry sha256 equal to the seat copies), not
against a stray copy: `validate --file` exits 0 at both revs with the identical normalized W-set — 7 × W04
(S030, S042, S045, S097, S119, S120, S121) + 1 × W01 (S277) + `ok`. The live fleet-root run normalizes to the same set.
So the eight rows introduce no duplicate-URL warning, silence none, and add no E-code. This also means w1
`ExecHarmBase.md` finding 3 (round-41's 2-line census block is an abbreviated capture; base prints 9 lines) still holds
unchanged at the data commit.

**F5 — the gate is not vacuous on these rows (support).**
Six mutants of the landed registry, scored in scratch: status `watch` → `E07`, recheck cell deleted → `E01`, future
`opened` → `E08`, dangling used-by → `E11`, duplicated id → `E03`, used-by `—` → `W03`; rename control reproduces the
clean output. Every property F3 verifies by hand is one the fleet gate also rejects when broken — the clean exit means
what it appears to mean.

**F6 — LOW, open observation: the row count is not evidenced by the receipt it is filed under.**
`validate` prints no `rows` metric, so `receipts/census-after-data.txt` cannot support "226 → 234"; that number rests on
the registry bytes (F2) and on `census` mode, which the round does not commit as a receipt. Anyone citing the receipt for
the row count is citing it for something it does not print. Not a data defect; a citation-scope note for the closure.

**F7 — LOW, reading hazard: `LOG.md:2492` numbers the dropped drafts in draft space.**
The LOG says "the drafts' S291/S296 rows were dropped". In the landed numbering **S291 and S296 exist** with different
content (DefaultFloatingAlgorithm.cpp, host-clients-r43.json). `w1/ScrEntryB/registry-rows.md` drafts ten rows S290–S299
whose S291 is `WindowRuleApplicator.cpp` and S296 is `HyprCtl.cpp` — the two sources already held by S155/S158 — so the
sentence is true of the drafts and misleading against the registry. The eight survivors were renumbered compactly. Fix
wording only; no row changes.

**F8 — INFO, pre-existing: one id-order inversion.**
`S277` precedes `S218` in both registries (1 inversion at base, 1 at data); unchanged by the data commit, untouched by
the appended rows, and irrelevant to the census parser (ids need not be sorted). No w1 report reports it (the id lists in
`assimilation/id-guard.md` and `assimilation/reg-ids` carry S218 without ordering it); recorded, not scored.

## What this supports / does not touch

- Supports: the census receipt as a reproducible instrument at the data commit; the 226 → 234 registry claim; the
  "append-only, eight well-formed rows, nothing else moved" shape of the data commit; the LOG's "same W04 x7 + W01 S277".
- Does not touch: C1/C2 verdicts (other seats), the entry's quotes and locators (`quality/check-locators.py`, other
  seats), the fetch pins, and whether the eight rows' *content* is true — my axis is the registry and the census gate,
  not the sources.
- Residuals of my own method: the base/data trees were archived with `git archive` (so E11 resolves used-by against the
  rev's tree, which is the faithful reading, but `--file` otherwise uses the file's parent dir); the census gate checks
  cell count, enums, dates, id uniqueness and used-by existence, **not** that a used-by path is the *right* document, and
  not that an anchor is true — both are other seats' axes.

## Hygiene

Write scope respected: only `.ufo/waves/round-43/w2/RerunCensus/` (plus this report) was written; no tracked file, counter,
receipt, freeze or index was touched; read-only git only (`show`, `archive`, `diff`, `rev-parse`, `hash-object`, `log`,
`status`). No pacman, no installs, no host-service or compositor writes, no Wayland connection. Scratch
`/fast/scratch/hyaku/mado-r43/RerunCensus` (two 232 M archives + mutants, peak < 0.5 G) deleted before finishing; every
cited path is in the seat dir.
