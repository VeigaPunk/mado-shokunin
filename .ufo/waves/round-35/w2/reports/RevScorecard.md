# RevScorecard — round-35 scorecard rows re-derived cell by cell

Seat: `L1Mado35.RevScorecard` (round 35, wave 2, mado). Leaf member: no subagent dispatch.
Read-only against the lane: I wrote only this report. No corpus file, counter, control,
`SOURCES.md`, `SCORECARD.md`, Git index or sibling repo was written;
`/home/vgpnk/Projects/shokuknow` read only. Installs: none.

Every number below comes from committed bytes or from `git archive <rev>` extractions. The
`scratch/` tree was relocated and then dropped from the lane mid-run (the closing commit says
"lane closes without scratch trees"); no claim in this report depends on a scratch path, and the
extraction directory is disposable.

Tip under test: `1bb25c751409f67f1f9b6d8ac5a91faf3d92f948` (`master`). `SCORECARD.md` blob
`66ff21b98d6ce92296a1a7e72689044e3f61996f` is identical at `7b745a1` and `1bb25c7`, so the
round-35 rows (`SCORECARD.md:2161-2232`) measured here are the published ones; all three
measurements were re-run at `1bb25c7` after the closing commit.

Reproduction recipe for any revision cited below (no clone needed):

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive <rev> | tar -x -C <dir>
python3 -I <dir>/.ufo/waves/round-35/c1/count.py --root <dir> \
        --frozen <dir>/.ufo/waves/round-35/c1/frozen.json
```

---

## 1. C1 row (`coverage`) — cell by cell

Command in the row, run verbatim:
`python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json`

| Cell | Published claim | Re-derived | Verdict |
|---|---|---|---|
| axis | `C1 **coverage**` — idle-lock control surface | `coverage` is the `navigation` sub-axis in the lane's table; the surface is named in `PROVINCE.md:9` ("screen/idle behavior (hypridle/hyprlock where present)") | AGREE |
| "three admitted entries + eight registry rows S203–S210, adopted from `merge/mado/` with ids re-pointed by document" | — | `git ls-tree --name-only HEAD corpus/knowledge/` carries all three `idle-lock-{never-asked-r12,chain-armed-r14,offered-in-the-bar-r15}.md`; `corpus/SOURCES.md` carries exactly one 11-cell row for each of S203–S210; the entries' `source:` lines use the lane ids, and the package originals under `shokuknow/merge/mado/knowledge/…` cite S315/S316, S327, S335/S336/S337/S340/S342 — the lesson's own remap table (`corpus/lessons/round-35.md:106-131`) | AGREE |
| freeze `19e4ab3`: `closed_entries=0 closed_rows=0 open_cites=8 TARGET_MISSED` exit 1 | before | archive of `19e4ab3`: `PRED-C1-r35-v1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED`, `exit=1` | AGREE |
| data `02088b4`: `closed_entries=3 closed_rows=8 open_cites=0 TARGET_MET` exit 0 | after | archive of `02088b4`: `PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET`, `exit=0`; at `HEAD` (after all errata appends to the entries): same line, `exit=0` | AGREE |
| "(re-run after every errata append, unchanged)" | stability | `git diff --stat 02088b4..HEAD -- .ufo/waves/round-35/fetch/` → empty, so the eight receipts never moved; the entry errata appends do change the entries, and the counter still reads 3/8/0 | AGREE |
| "registry 192 → 200 rows" | 192 → 200 | `git show 19e4ab3:corpus/SOURCES.md \| grep -cE '^\| S[0-9]'` → **192**; `git show 02088b4:…` → **200**; `HEAD` → 200; `git diff --numstat 19e4ab3 02088b4 -- corpus/SOURCES.md` → `8 0` (additions only) | AGREE |
| "navigation 47/47 → 50/50" | 47/47 → 50/50 | `quality/check-index.py --rev 19e4ab3` → `indexed=47/47 … exit 0`; `--rev 02088b4` → `indexed=50/50 … exit 0`; `--rev HEAD` → `indexed=50/50 … exit 0` | AGREE |
| counting-command cell | as published | byte-equal to `registration.md` §C1 | AGREE |
| "shape-scored (dead `digest` clause; shape-only and fabricated-payload cribs both reach `TARGET_MET`: `controls-content/`)" | — | `count.py:174` computes `digest = hashlib.sha256(blob).hexdigest()` and never reads it (the conjunct is `receipt["sha256"] in cs[5]`, the spec digest in the cell). `python3 -I …count.py --root .ufo/waves/round-35/controls-content/c1-shape-only …` → `3/8/0 TARGET_MET` `exit=0`; same for `c1-fabricated-payload` | AGREE |
| "all eight receipts were re-opened and re-hashed 8/8" | 8/8 | `sha256sum` of `.ufo/waves/round-35/fetch/S20{3..9,10}.receipt.txt` equals the frozen digest for 8/8 (`1b7fa87f…`, `4cd5ba65…`, `f3387bfc…`, `1d30e4a9…`, `81c33e79…`, `6e72f0db…`, `a170c7a5…`, `ef282e38…`) | AGREE |
| "a one-line digest repair keeps the real root `TARGET_MET` and kills both cribs" | — | `.ufo/waves/round-35/scratch-evidence/L1DigestFix/count-fixed.py` (sha256 `a833da2a4008a13f…`) differs from the counter by exactly `+ and digest == receipt["sha256"]` (line 193). Root: `3/8/0 TARGET_MET` `exit=0`; shape-only: `0/0/8 TARGET_MISSED` `exit=1`; fabricated-payload: `0/0/8 TARGET_MISSED` `exit=1` | AGREE (demonstrated, though labelled a round-36 claim) |
| "wave-2 seats falsified three inferences in the admitted text (withdrawn by errata)" | 3 | see F5: the errata set is 10 bullets (r12: E1–E3; r14: E1–E2; r15: E1–E5) plus two in-section correction blocks; no plain reading yields three | **DIVERGE** |

## 2. C2 row (`calibration`) — cell by cell

Command in the row, run verbatim:
`python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json`

| Cell | Published claim | Re-derived | Verdict |
|---|---|---|---|
| axis | `C2 **calibration**` | distinct from C1's coverage; both sit on the tied-lowest set (§4) | AGREE |
| "r34 tip `dff3941` had no clause ledger (`error=clause-ledger-missing` exit 2)" | before | committed r35 counter with `--repo` = archive of `dff3941`: `PRED-C2-r35-v1 error=clause-ledger-missing`, `exit=2` (`.ufo/waves/round-35/` does not exist at that revision) | AGREE |
| "`02088b4`: `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 TARGET_MET` exit 0" | after | at `HEAD`: same line, `exit=0`; `git diff --stat 02088b4 HEAD -- .ufo/waves/round-35/{c1/clauses.json,c2,ledger,controls,c1/frozen.json,c1/count.py}` → empty, so the HEAD run is the data-commit run | AGREE |
| counting-command cell | as published | byte-equal to `registration.md` §C2 | AGREE |
| "(a) `ledger_tip_ok` scores `TARGET_MET` on the round-34 defect itself (stale `fa7ba113` label …)" | mechanism | scratch spec pinned to `r34_tip=fa7ba113…` + a ledger doc naming it → `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET`, `exit=0`; the check is a literal substring plus `git rev-parse <tip>:<path>` blob ids (`count.py:104-131`) | AGREE |
| "(b) `dff3941` was master for 0:17:37 and the last round-34-labelled commit is `6d754bd`; the blob ids verify identically at both" | disputed tip | `git show -s --format=%ct dff3941` = 1792892809, `6d754bd` = 1792893866 → **1057 s = 17m37s**; `6d754bd` is titled "round-34 verifier spot-check"; all seven frozen blob ids are identical at `dff3941`, `6d754bd` and `19e4ab3` | AGREE |
| "(c) `uncovered=0` is fail-open on clause deletion with its control, and covered-receipts are token greps" | mechanism | deleting one live clause **and** its control from the ledger → `uncovered=0 … verdict=TARGET_MET`, `exit=0`; the receipt check is `is_file()` plus `re.search("verdict=TARGET_MISSED")`, with no binding to the clause | AGREE |
| verdict "NOT ADMITTED" | author verdict | consistent with (a)–(c) as reproduced; the counter's four observables are shape checks | AGREE (as a verdict about the claim, not a re-score) |

## 3. Section prose — numbers and labels

| Claim | Re-derived | Verdict |
|---|---|---|
| "two v1 waves, 64 + 40 = **104 seats** … wave 1: executor 13, scout 12, reviewer 11, critic 8, scribe 7, connector 4, mutation-tester 3, sentinel 2, revenger 2, simplifier 2" | `w1-spec.json` role census → 13/12/11/8/7/4/3/2/2/2 = **64**; `w1/reports/*.md` = 64 | AGREE (note: `w1/seat-plan.tsv` carries only 63 data rows — 11 scout — so the plan file is short one row; the row's number matches the spec and the reports, not the plan) |
| "wave 2: reviewer 21, executor 3, mutation-tester 3, critic 3, sentinel 2, revenger 2, scout 2, scribe 2, simplifier 1, connector 1" | `w2-spec.json` role census → exactly that, total **40**; `w2/reports/*.md` = 40 | AGREE |
| "Axis table re-derived at `02088b4` plus the round-35 errata: navigation 50/50; calibration 43/43; operability 12/12." | at `02088b4`: `MADO_AXIS_ROW: axis=navigation published=47/47 derived=50/50 verdict=STALE`, `axis=calibration published=41/41 derived=41/43 verdict=STALE`, `operability 12/12 MATCH` → `checked=3 mismatched=2` `exit=1`. The `43/43` holds only at `HEAD`/`4f35c80`, not at `02088b4` | **DIVERGE on the label** (F2) |
| "Axis table re-derived at `4f35c80` … (round-35 wave-2 close, **the publication the gate reads**): navigation 50/50; calibration resolved-active 43/43; operability selftest 12/12." | `quality/check-axis-scores.py --rev 4f35c80` → `axis=calibration published=- derived=43/43 verdict=NOT-PUBLISHED`, `axis=operability published=- … NOT-PUBLISHED`, `checked=3 mismatched=2` `exit=1`. The parseable line landed in `7b745a1` ("republish the axis table in the gate's own format"); at `HEAD` the gate is `checked=3 mismatched=0` `exit=0` | **DIVERGE** (F1) |
| "No axis is claimed harmed: index gate 50/50 exit 0, axis gate re-derives all three rows to MATCH, operability `MADO_SELFTEST: 460/460 assertions passed` (byte-identical suite to the round-34 tip)" | index at `HEAD` → `indexed=50/50 … exit 0`; axis gate at `HEAD` → 3× MATCH, `mismatched=0`, `exit=0`; `bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 460/460 assertions passed`, `exit=0`; `tools/mado-verify.sh` blob `9113c7c05e58…` identical at `dff3941` and `HEAD` | AGREE at `HEAD`; the MATCH half is false at both mid-round revisions the section cites (F1) |
| "the axis publication was stale for ~15 minutes … (`mismatched=2`)" | `mismatched=2` at `02088b4` confirmed. Data commit 03:23:36 → errata commit 03:34:26 = 10m50s → parseable publication (03:42:29) = 18m53s | AGREE on `mismatched=2`; "~15 minutes" is an honest midpoint, not a measured figure |
| "the pre-data `golden` control's rows differ from the shipped registry in anchor/teaches cells" | cell 6 (`teaches`) differs for all of S203–S210; cell 5 (`anchor`) differs for all; **S204 also differs in cell 4 (`scope`) and cell 9 (`recheck`)** | **DIVERGE** — incomplete (F4) |
| "Sources 192 → 200 … no existing row's status/recheck/used-by changed; **four** new rows' `scope`/`teaches` cells were corrected in-round" | 192→200 ✓ and the append is additions-only ✓, so no existing row changed ✓. Corrected rows since the data commit: **S203** (cells 6, 9), **S204** (4, 6, 9), **S205** (6) — three rows, and the corrected cells include `recheck` (9), not only `scope`/`teaches` | **DIVERGE** (F3) |
| "Capabilities: None entered." | `## Capabilities` still `| — none yet — |`; `### Capabilities (round 35)` holds prose only, no table row; `git diff` of `SCORECARD.md` for a capability row is absent | AGREE |
| "Saturation 9.0 / N=3 unchanged; retired: none." | unchanged text; `## Retired` still "none retired" | AGREE |
| "Frontier advanced: the round-35 idle-lock offer route (consumer half measured; transitions remain open)" | no frontier list exists in `PROVINCE.md` or `SCORECARD.md` to check a frontier state transition against; the C1 correction block itself says part of the route was already reviewed at `dff3941` | **UNVERIFIED as a formal state change** (label follows rounds 32/34 usage) |

## 4. The four mandated structural checks

1. **Distinct axes.** AGREE — C1 `coverage`, C2 `calibration`; causally separable (C1 reads
   `corpus/` + receipts; C2 reads the clause ledger, receipts and git blobs; neither counter
   reads the other's artifacts).
2. **At least one claim works the lowest non-retired axis.** AGREE, and more strongly than the
   row claims. At the round-34 tip the three published sub-axes were all at 1.0
   (`navigation 47/47`, `calibration 41/41`, `operability 12/12`), the round-34 capability row
   exists (`SCORECARD.md:2142`), and the declared window N=3, so the AXES.md stagnation nudge
   does not waive. At the data commit calibration derived **41/43 = 0.9535**, making it the
   uniquely lowest scored sub-axis, with C2 sitting on it. The row's own correction records the
   fourth cell (`sourced-art 1.0`) that the three-cell quote omits; all four are tied, so the
   conclusion survives.
3. **No axis claimed harmed** — claimed, and the three measurements that carry it reproduce at
   `HEAD` (§3). The one defect is locational: the section's "axis gate re-derives all three rows
   to MATCH" is true at `7b745a1` only, not at the two mid-round revisions it cites (F1).
4. **Capabilities table untouched** — AGREE, and no row was entered without a demonstration:
   the round-35 section explicitly enters none, and the canonical table still reads
   `— none yet —`. (The round-34 row lives in its own per-round subsection; that split predates
   this round.)

## 5. Findings, by severity

**F1 — MEDIUM — "the publication the gate reads" is mis-attributed; the lane's calibration gate
was red at the revision it names.**
`quality/check-axis-scores.py --rev 4f35c80` prints
`calibration published=- derived=43/43 verdict=NOT-PUBLISHED` and
`operability published=- derived=12/12 verdict=NOT-PUBLISHED`, `checked=3 mismatched=2`, exit 1.
The parseable publication was added one commit later, in `7b745a1` ("republish the axis table in
the gate's own format"), where the gate is `mismatched=0`. A reader re-deriving the sentence at
the cited commit gets the opposite verdict. Reword to name `7b745a1`, or move the caption to the
line that actually parses.

**F2 — MEDIUM — the first axis line's numbers are not the values at the revision it names.**
"Axis table re-derived at `02088b4` … calibration 43/43" is false there: the derivation is
`41/43` (exit 1, `mismatched=2`). `43/43` becomes true only after `4f35c80`. The words "plus the
round-35 errata" carry the repair, but the number is presented as measured at `02088b4`. State
the two revisions separately (`02088b4`: navigation 50/50, calibration 41/43, operability 12/12;
`4f35c80`: 50/50, 43/43, 12/12).

**F3 — MEDIUM — the Sources prose miscounts the in-round row corrections and misnames their cells.**
"four new rows' `scope`/`teaches` cells were corrected in-round": `git diff 02088b4 HEAD --
corpus/SOURCES.md` is 3 insertions / 3 deletions over **three** rows — S203 (teaches, recheck),
S204 (scope, teaches, recheck), S205 (teaches). There is no fourth row, and `recheck` is not
named.

**F4 — LOW — the golden-vs-shipped divergence is under-described.** The pre-data `golden` rows
differ from the shipped registry not only in `anchor` (cell 5) and `teaches` (cell 6), which is
true for all eight, but S204 additionally differs in `scope` (cell 4) and `recheck` (cell 9).
The conclusion ("the controls never exercise the live bytes") holds; the enumeration does not.

**F5 — LOW — "three inferences … withdrawn by errata" does not match the errata set.** Committed
errata bullets: `idle-lock-never-asked-r12.md` 3 (E1 never-toggled, E2 thirteen-items, E3
title/independent-negatives), `idle-lock-chain-armed-r14.md` 2 (E1 transient-scope unlicensed,
E2 two boots / "both fire" withdrawn), `idle-lock-offered-in-the-bar-r15.md` 5 (E1 dating clock,
E2 "never taken it", E3 "built not to remember", E4 one-state-named, E5 "leaves no trace" scope)
— 10 bullets, each withdrawing or narrowing at least one assertion, plus two in-section
correction blocks. Either name the three it means or publish the measured count.

**F6 — LOW — transcription and adjacent-file nits.**
(a) Both row cells quote counter output with the `verdict=` token elided
(`… open_cites=8 TARGET_MISSED`, `… ledger_tip_ok=1 TARGET_MET`); the counters print
`verdict=TARGET_MISSED` / `verdict=TARGET_MET`. (b) `w1/seat-plan.tsv` has 63 data rows (11
scout) although wave 1 dispatched 64 seats and produced 64 reports — the row's seat numbers are
right against the spec and reports, but the plan file contradicts them.

**F7 — NOTE — the digest-repair patch's evidence path moved at the close.**
`scratch/` was dropped from the lane at `1bb25c7` ("lane closes without scratch trees"); the
patch is now tracked at `.ufo/waves/round-35/scratch-evidence/L1DigestFix/count-fixed.py`
(sha256 `a833da2a4008a13f182c63ce8c2968bed1294d1ce303f20a387ab3de847a0cfd`, re-verified at this
tip: root `TARGET_MET` exit 0, shape-only `TARGET_MISSED` exit 1). Any citation of a
`.ufo/waves/round-35/scratch/…` path for this artifact is now dangling; cite the
`scratch-evidence/` file or its sha256.

## 6. What the rows get right (verified, so it is not re-argued)

- Both frozen targets reproduce at their stated commits: C1 `0/0/8 MISSED exit 1` at `19e4ab3`
  and `3/8/0 MET exit 0` at `02088b4`/`HEAD`; C2 `clause-ledger-missing exit 2` at `dff3941`
  and `0/1/1/1 MET exit 0` at `02088b4`/`HEAD`.
- Registry 192 → 200 and navigation 47/47 → 50/50 reproduce exactly, with an additions-only append.
- The C1 verdict's three routed defects are all real, and the one-line digest repair demonstrably
  keeps the root green and kills both content cribs.
- The C2 verdict's (a), (b) and (c) all reproduce; `0:17:37` is exact (1057 s), the last
  round-34-labelled commit is `6d754bd`, and the seven blobs are identical at both revisions.
- Seat counts and role breakdowns for both waves are exact against the plans; 104 total.
- No axis is harmed as measured at the tip: index 50/50, axis gate 3× MATCH, selftest 460/460 on
  a gate blob byte-identical to the round-34 tip.

## 7. Residual risk and verification gaps

- **R1 — the nudge depends on which "capabilities table" counts.** The round-34 row sits in
  `### Capabilities (round 34)` while the canonical `## Capabilities` table still reads
  `— none yet —`. Reading only the canonical table would make the stagnation nudge *available*
  (it waives the lowest-axis duty; it does not harm). The round-35 conclusion is unaffected
  either way here, but the two tables should be reconciled.
- **R2 — inputs are worktree bytes.** `clauses.json` and every receipt are read through
  `repo / path`; only `ledger_tip_ok` touches git. The C2 row says this (F1–F5 of `RevC2Tip`),
  and my deletion probe confirms it.
- **R3 — shape vs truth for C1.** The admitted `TARGET_MET` is a shape verdict; the round says
  so and routes the repair. `closed_rows=8` is not a truth claim about the eight receipts.
- **Unverified by this seat:** the claim that the wave validator "rejects a `planner` seat"
  (no validator transcript is cited in the tree I read); the construction of the two
  `controls-content/` cribs (I ran them, not their provenance); and the "~15 minutes" interval,
  which is an approximation between 10m50s and 18m53s depending on which commit ends the window.
- **Environment note:** the `scratch/` tree was relocated to `scratch-evidence/` mid-run and then
  dropped from the lane at `1bb25c7`. Every measurement above is from committed bytes or
  `git archive <rev>` extractions, so the relocation/deletion affects no number in this report.
  `w1/reports` holds 64 `.md` seat reports at the closing tip, `w2/reports` 40.
