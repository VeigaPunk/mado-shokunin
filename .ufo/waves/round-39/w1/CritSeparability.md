# CritSeparability — cross-claim separability proof (round-39 w1)

Date 2026-10-25. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, freeze HEAD
`457d1b125932c1e0d797061a2156b917bcd7edaa` (`git rev-parse HEAD`). No tools installed;
no lane file written except this report; all scratch under `/tmp/r39-sep`.

## 1. Method

Data deliverables (C2 tool/counter/fixture, C1 manifest/receipts, C3 entry/SOURCES
rows) are **uncommitted** at review time (`git status --porcelain=v2` shows `? tools/mado-options.py`,
`? quality/counters/c3-r39-options.py`, `? .ufo/waves/round-39/w1/`, `? .ufo/waves/round-39/c1/`,
`? .ufo/waves/round-39/receipts/`). A sandbox clone with full history was made
(`git clone /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/r39-sep/sb`), and four
synthetic revs were committed there (sandbox identity, per round precedent):

| rev | sha | content |
|---|---|---|
| F | `457d1b12…` (== lane HEAD) | freeze commit |
| D | `8e5755c7fa73358ec4c72790ae102c6dae24cdb4` | F + C2 tool `tools/mado-options.py`, counter `quality/counters/c3-r39-options.py`, fixture `.ufo/waves/round-39/w1/ExecOptionsFixtures/` (incl. trees/expected.json), C1 manifest + `receipts/` |
| E | `cf70d2a19cabcf03cf96b3e96515bb1f5d80ce41` | D + C3 entry `corpus/knowledge/config-option-table-r39.md` (ScrKnowledgeEntry draft) + SOURCES rows S218/S219 appended (ScrSourcesRows draft) |
| X | `8ed73f59cca58b59cfa42aa9830cc83a74302631` | D − `tools/mado-options.py` − `quality/counters/c3-r39-options.py` (C2 artifacts deleted) |
| Y | `9838474ade05e00e8821a81b500d031d54ed060d` | D − `.ufo/waves/round-39/c1/manifest.json` − `.ufo/waves/round-39/receipts/` (C1 artifacts deleted) |

Tool/counter bytes in D are byte-identical to lane working tree
(`sha256sum`): `tools/mado-options.py` `cee78d99…61e`, `c3-r39-options.py`
`16544cbde4ed67cf…` (same as `git show D:…`).

C1 checker runs: original `quality/check-r38-discrimination.py` at rev F; for the
variants a copy with `LANE = "/tmp/r39-sep/sb"` (source repo swapped; all other bytes
identical, sha `884f6b8369d912d4` for each of the 4 copies). Manifest passed from an
external copy (sha `96965518dc8ad98b…`, byte-identical to `c1/manifest.json`); the
manifest has zero `"op": "file"` writes, so `controls_dir` is irrelevant.

## 2. C1 checker — verdict never moves

```
MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET   (exit 0)
```
Identical at F, D (C3 artifacts deleted), E (C3 present), X (C2 artifacts deleted),
Y (C1 manifest+receipts deleted from tree). Receipts byte-identical:
`sha256sum receipts/c1-*.txt receipts/base-c1.txt` → all `8fe55d81a816e54469e5dd6474596b8ea19feaebf7ed5d5e6d153c01933d2e74`.
Full 19-line control runs in `receipts/{base-c1,c1-D,c1-E,c1-X,c1-Y}.txt`.

Structural reason: the checker clones `LANE`, sparse-cones `corpus tools quality .ufo/waves/round-38`
(`check-r38-discrimination.py` `--170-171`), and scores c1/c2 event counters against
control writes on `tools/mado-eventq.py` and `.ufo/waves/round-38/receipts/` only. It
never reads any round-39 deliverable (its only round-39 input is the external `--manifest`).

## 3. C2 counter — verdict never moves across the other claims' deletions

```
rev D (8e5755c7…): PRED-C3-r39-v1: fixtures=0/4 tool=present verdict=TARGET_MISSED (exit 1)
rev E (cf70d2a1…): PRED-C3-r39-v1: fixtures=0/4 tool=present verdict=TARGET_MISSED (exit 1)
rev Y (9838474ade…): PRED-C3-r39-v1: fixtures=0/4 tool=present verdict=TARGET_MISSED (exit 1)
rev X (8ed73f59…):  PRED-C3-r39-v1: fixtures=0/1 tool=absent  verdict=TARGET_MISSED (exit 1)
```
Normalized (strip `rev=…`) outputs for D, E, Y are **byte-identical**
(`diff` empty; `receipts/c2-<sha>.txt`). So C2 is unaffected by deleting C3
entry+rows (D vs E) and by deleting C1 manifest+receipts (Y); it is sensitive only to its
own artifacts (X: `tool=absent`). C2 reads only `tools/mado-options.py` and
`.ufo/waves/round-39/w1/ExecOptionsFixtures/run-fixtures.sh` blobs at `--rev`
(`c3-r39-options.py:24-26,59,84`).

**Observed claim-level defect (separate from separability):** C2 cannot currently reach its
frozen target at any state. (1) Clause b expects `(\d+)\s*/\s*(\d+)\s+assertions?` > 40,
but the tool's selftest emits exactly one line `MADO_OPTIONS_SELFTEST: 69/69 passed` →
`assertions=0`, `clause=b … ok=0` even though rc=0. (2) Clauses c/d extract the fixture
script alone into a temp dir and run it there, so `HERE`/`LANE`/`TOOL`/`trees` resolve to
nonexistent paths → `fixtures=0/4`; the same fixture run from its real relative layout passes
(`fixtures=4/4`, rc=0). This is a counter↔tool/fixture interface mismatch, not a deletion effect.

## 4. C3 leg — not executable (counter artifact absent)

`quality/counters/c4-r39-options-entry.py` does not exist in any ref, worktree, or seat:
`find … -name 'c4*'` empty; `grep -rn 'PRED-C4' quality/ corpus/ tools/ .ufo/waves/round-39/`
only matches `registration.md:79` (predicate text) and the peer report `w1/CritC3Control.md`;
no w1 seat produces a c4 counter (64-seat spec: counter seats are `ExecOptionsCounter`,
`RevC2Counter`, `MutC1Counter` — none for c4). `CritC3Control.md:11` independently concludes
"the C3 counting command cannot be executed at review time; PRED-C4-r39-v1 is not yet measurable".
Therefore the two legs "C3 unaffected by deleting tool/manifest" cannot be executed; the C3
verdict is unmeasurable until the counter lands. The C3 entry+rows drafts exist only in seat
dirs (`ScrKnowledgeEntry/`, `ScrSourcesRows/rows.md`, S219 receipt INCOMPLETE), not at canonical paths.

## 5. Verdict

- **Separability holds for the claims that are measurable:** C1 ↔ C2 are causally
  independent — deleting C2 artifacts does not move C1 (19/19 MET before and after), deleting
  C3 entry+rows or C1 manifest+receipts does not move C2 (identical MISSED output); each
  checker reads a disjoint artifact set, sharing only the lane repo substrate. No shared artifact.
- **C3 legs cannot be verified** — the c4 counter artifact is absent (blocker, corroborated by CritC3Control).
- **Flag for main:** C2's frozen counting command cannot produce `TARGET_MET` even with all
  deliverables present (selftest format mismatch + fixture isolation), so the C2 claim as
  wired is currently unachievable; this is a counter/tool/fixture interface defect, not a
  separability coupling.

Receipts retained at `/tmp/r39-sep/receipts/` (c1-*.txt, base-c1.txt, c2-*.txt).
