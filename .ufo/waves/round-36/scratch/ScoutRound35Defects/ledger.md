# Round-36 D-ledger — disposition of the round-35 routed defects

Source list: `corpus/lessons/round-35-verifier-spotcheck.md` "Routed defects" (D1–D10).
Produced at lane tip `dbf8b57` (the round-36 freeze); wave-1 build items are in flight,
so "pending" marks a disposition whose record bytes do not exist yet.

| Defect | Round-36 disposition | Artifact that shows it |
|---|---|---|
| **D1** — report-lands-last / no tip citation | Erratum owed to the round-35 report: names lane tip `7a068cbee3b0983230b8fb8467c02e12772832dd` and admits the report-ordering failure; facts re-derived by seat `ScoutD1Facts`. | Claim C2's subject list (`registration.md:94`); draft `.ufo/waves/round-36/scratch/ScribeReportErrata/errata.md` (pending) → lands in the round-36 report, which must land last and cite the tip. |
| **D2** — uncommitted round work at closure | Resolved as a revert: the ten inherited paths (`quality/check-evidence-pointers.py:54-65`) were restored to committed bytes — `git status --porcelain -- <the ten paths>` prints nothing now; disposition sentence for `LOG.md` still pending. | Claim C2 observable `inherited_dirty` (gate; before receipt `receipts/before-pointers.txt` records `inherited_dirty=10`); audit seat `ScoutInheritedTen`. |
| **D3** — C1 counter shape-scored | Repaired: `quality/counters/c1-idle-lock.py` binds the declared sha256 to the bytes read (`digest == receipt["sha256"]`, line ~194) and adds the registry-section clause. | Claim C1 (`PRED-C1-r36-v1`, `c1/frozen.json`); frozen reject controls `c1-shape-only`, `c1-fabricated-payload` in `controls/manifest.json`; drafted QUALITY criterion 57 (`scratch/ScribeQualityCrit/criteria.md`, pending). |
| **D4** — C2 observables fail-open | Repaired: `quality/counters/c2-ledger.py` pins the live clause set to the frozen spec, requires each control's committed receipt to record `observed=TARGET_MISSED` and name its clause, and computes the round-34 tip from git by one frozen rule. | Claim C1 (`PRED-C2-r36-v1`, `c2/frozen.json`); record edit `.ufo/waves/round-36/ledger/RevFrozenBlobs-r36.md` re-issues the disputed r34 tip label; drafted QUALITY criterion 58 (pending). |
| **D5** — dangling evidence pointers in `LOG.md` | Correction pairs required: each dead pointer must appear as `` - `old` -> `new` `` in the round-36 `LOG.md` entry with `new` resolving (`SUPERSEDED_POINTERS`, `check-evidence-pointers.py:50-53`); record edit to `LOG.md` pending. | Claim C2 observable `dangling_r35_closed`; before receipt shows `dangling_r35=2 dangling_r35_closed=0`. |
| **D6** — wrong correction count ("four" → three rows) | Erratum owed to the round-35 report: `git diff --numstat 02088b4 7a068cb -- corpus/SOURCES.md` = `3 3` over S203/S204/S205 (SCORECARD already carries the corrected figure, committed at `7d708cf`). | Claim C2's subject list; `ScoutD6Rows` report (verdict: three rows confirmed); draft in `scratch/ScribeReportErrata/errata.md` → round-36 report. |
| **D7** — stale seat-report count ("38" vs 37/40) | Erratum owed to the round-35 report naming the per-revision counts: 37 `.md` at `4f35c80`/`7b745a1`, 40 at tip `7a068cb`. | Claim C2's subject list; `ScoutD7Counts` report (verdict: D7 upheld); draft in `scratch/ScribeReportErrata/errata.md` → round-36 report. |
| **D8** — "no scratch tree left" vs 124 tracked paths | Disposition sentence required in `corpus/lessons/round-36.md` naming `.ufo/waves/round-35/scratch` and stating `tracked paths=N` equal to the live `ls-tree` count (124 at freeze). | Claim C2 observable `scratch_disposition_ok` (gate parses `tracked paths=(\d+)`, `check-evidence-pointers.py:165-172`); inventory seat `ScoutDisposition124`. |
| **D9** — entries don't open with provenance trio | Investigated, not yet applied: the three r35 entries still carry `source:`/`verified-at:`/`recheck:` at lines 7–11 after the title; `ScoutD9Provenance` proposes an append-only `## Provenance (normalized)` trailer policy, `CritD9Boundary` tests the doc-localization refusal boundary. No gate observable covers the corpus form, and no seat owns the normalization edit — record edit pending (lesson/QUALITY or per-entry trailers). | Named in C2's subject list (`registration.md:94`) but covered only by seat findings `w1/reports/ScoutD9Provenance.md`, `CritD9Boundary.md`; **no committed gate or edit yet — the weakest defect coverage this round.** |
| **D10** — no tip-revision axis transcript | Required: a committed `quality/receipts/axis-<40hex>.txt` whose `<40hex>` is an ancestor of the tip and whose `MADO_AXIS:` line reads `mismatched=0 rev=<40hex>`; `quality/receipts/` is empty at freeze, so the receipt is pending. | Claim C2 observable `tip_axis_transcript` (`check-evidence-pointers.py:174-190`); command/format seat `RevAxisTranscriptAsk`; before receipt shows `tip_axis_transcript=0`. |

## Silent-defect check

Every defect D1–D10 names a round-36 artifact above; none is silent. Honest gaps at
wave-1 build time: D2's `LOG.md` disposition line, D5's correction pairs, D8's
`tracked paths=` sentence, D10's committed transcript and all three report errata
(D1/D6/D7) are record bytes that only exist once the round-36 record edits land —
the C2 gate refuses `TARGET_MET` until they do (`before-pointers.txt`:
`verdict=TARGET_MISSED`, `setup=missing-r36-sections`). D9 alone is named in C2's
subject list without a gate observable or an owner for the normalization edit.
