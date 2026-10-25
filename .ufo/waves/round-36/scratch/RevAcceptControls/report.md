# RevAcceptControls — review of round-36 control manifest, acceptance controls, reject-input isolation, and discrimination receipts

Reviewer: L1Mado36.RevAcceptControls. Read-only on production files; all gate/scoring runs
wrote only to /tmp (fixtures, receipts) — no lane bytes were mutated. Commands and
quoted outputs below are the exact evidence.

## What I checked

1. Manifest shape (`controls/manifest.json`): 25 controls — 3 accepts (`c1-live`,
   `c1-golden-r36`, `c2-live`) and 22 rejects. Kinds: the two c1 accepts are `kind=tree`
   (committed crib trees), `c2-live` is `kind=live` (lane root). Rejects are 16 c1 tree
   cribs + 8 c2 mutants (`kind=mutant`). Requisite rows carry `clause=<id>` for the
   clause they are meant to kill (except `c1-donothing` and all c2 entries, which have
   `clause=-`).

2. Frozen-spec input pinning (`c1/frozen.json`, `c2/frozen.json`):
   - C1 inputs per scored root: `corpus/SOURCES.md`,
     `corpus/knowledge/idle-lock-never-asked-r12.md`, `idle-lock-chain-armed-r14.md`,
     `idle-lock-offered-in-the-bar-r15.md`, and the eight receipts
     `.ufo/waves/round-35/fetch/S203.receipt.txt … S210.receipt.txt`.
   - C2 inputs: `c2/clauses.json` (clause ledger), blob-ledger doc
     `ledger/RevFrozenBlobs-r36.md`, and the per-clause receipt files named in that
     ledger (10 files under `controls/receipts/`). The counter also reads git history
     (`GIT_DIR` inherited, so `--repo /tmp/...` still sees the lane's history — that is
     how the tip and frozen-blob IDs are pinned).

3. Counter behavior (the two repaired counters under `quality/counters/`):
   - `c1-idle-lock.py` reads exactly that file set from `--root`; the registry section
     is the table under a line that equals `## Registry`; rows are matched, used-by
     sets checked, digest and gate-quote clauses enforced.
   - `c2-ledger.py --repo <root>` loads `clauses.json` (gate on frozen expected live /
     retired IDs), parses the blob ledger, re-derives the 7 blob rows, verifies the tip
     and the receipts per clause.

4. Empirical discrimination run (the gate itself, profile r36, manifest, repo=., outputs
   to /tmp — no lane writes):
   ```
   control=c1-live ... expected=TARGET_MET observed=TARGET_MET ok=1
   control=c1-golden-r36 ... expected=TARGET_MET observed=TARGET_MET ok=1
   control=c1-donothing ... expected=TARGET_MISSED observed=TARGET_MISSED ok=1
   ... (all 25)
   MADO_DISCRIMINATION: profile=r36 instruments=c1,c2 controls=25 correct=25/25 label='round-36 repaired counters' verdict=TARGET_MET
   exit=0
   ```
   Every one of the 25 controls classifies exactly as the manifest declares: 3 accepts →
   TARGET_MET, 22 rejects → TARGET_MISSED.

5. Accept controls:
   - `c1-live`: `git status --porcelain -- <12 input paths>` prints nothing (clean);
     all 12 files are tracked at HEAD. Live bytes == committed lane bytes. ✓
   - `c1-golden-r36`: whole-tree diff vs the round-35 golden shows **only**
     `corpus/SOURCES.md` differs, and byte-wise `r36 = header_lines + r35_bytes`
     (verified with `endswith` — the r35 table is the exact tail).
     It differs from live SOURCES.md (live has expanded registry), which is the named
     intended difference in the prompt (the crib is the r35 golden with the round-36
     `## Registry` heading restored — not a byte copy of the live lane).
   - `c2-live`: runs with `--repo .` against the lane root; inputs tracked and clean at
     HEAD; verdict TARGET_MET.

6. Reject single-input isolation:
   - The ten inherited r35 c1 cribs each differ from `c1-golden-r36` in exactly one
     file (`corpus/SOURCES.md`) — they are the r35 golden (mutation included) *without*
     the `## Registry` heading, so they die at the row-in-registry fence
     (`registry_section()` → empty; `open_cites=8`). The named clause for each is not
     the direct cause of rejection in the r36 frame; the lane documents and proves the
     per-clause load-bearing property separately (committed `receipts/clause-attribution.txt`,
     header-restored re-scores: each named clause shows exactly one open cite).
   - The r36-native rejects are single-file single-mutations of the golden:
     `c1-no-registry-heading` (r35 golden itself; header absent), `c1-row-moved-out`
     (row relocated under `## Leads (unopened)`; header present → exactly one open cite:
     `closed_entries=2 closed_rows=7 open_cites=1`).
   - The eight c2 mutants regenerate deterministically with
     `gen-mutants.py --profile r36 --repo . --out /tmp/...`; per mutant, the only lane
     input file(s) that differ from live:
     * `c2-tip-stale` / `c2-tip-one-copy` → only `ledger/RevFrozenBlobs-r36.md`
       (one hex token replaced by the stale r34 tip `fa7ba113…`);
     * `c2-blob-corrupt` → ledger row hash zeroed;
     * `c2-blob-row-deleted` → ledger row removed;
     * `c2-clause-deleted` → `clauses.json` drops the live clause (with its control) —
       counter reports `uncovered=1`;
     * `c2-receipt-token` → `controls/receipts/c1-entry-symlink.txt` replaced by an
       unbound token file (starts `ZZZZ NOT A RECEIPT …`);
     * `c2-receipt-unbound` → same receipt replaced; coverage loses `entry-regular`;
     * `c2-retired-also-live` → `clauses.json` moves the retired clause into live[]
       (counter: `uncovered=3 retired=0`).
   All eight scored TARGET_MISSED with the intended observable failing.

7. Receipt fidelity: the lane's committed `controls/receipts/` (25 files, tracked, clean
   at HEAD) match the gate's regenerated outputs exactly in every verdict line
   (`instrument= … expected= … observed= … ok=1`, `PRED-C…`). The only deltas are the
   `$` command echoes pointing to different ephemeral /tmp fixture trees (committed ones
   use `/tmp/mado-r36-mutants-r36/…`; my run used `/tmp/mado-r36-review-discrimination-mutants/…`)
   — the two fixture trees themselves are byte-identical (verified per mutant).

## Verdicts

- Manifest shape: **PASS** (25 controls; 3 accept / 22 reject; kinds match).
- Accept controls: **PASS** — c1-live byte-identical to committed inputs; c1-golden-r36
  is the r35 golden + registry heading (single intended file delta); c2-live accepts.
- Reject single-mutation isolation: **PASS** with the documented caveat that the ten
  inherited r35 cribs carry two deltas vs `c1-golden-r36` (their mutation *and* the
  missing `## Registry` heading); they are correctly rejected (fence), and per-clause
  load-bearing is proven by the committed header-restored re-scores. The six r36-native
  rejects are clean single-mutations.
- Counter discrimination: **PASS** — 25/25, verdict TARGET_MET.
- Receipt fidelity: **PASS** — 25/25 verdict-equivalent; only ephemeral /tmp paths in the
  command echo differ.

## Residual risk / gaps

- I did not re-run the full header-restored clause-attribution set (that writes under
  /tmp only; the committed artifact already documents each named clause yielding exactly
  one open cite after restoration). My independent runs confirm the two polarity cases:
  no-header → 8 open; header+row-moved → 1 open.
- `c2-live` depends on `superseded_ledger` semantics (a path absent at scoring is the
  intended supersede state) — verified via the committed receipt showing `old=1` and the
  fresh run agreeing.
- The gate's committed receipts were generated from `/tmp/mado-r36-mutants-r36`; that
  path is ephemeral, but the fixture regeneration is deterministic from the lane and
  matches byte-for-byte, so the committed receipts are reproducible.
