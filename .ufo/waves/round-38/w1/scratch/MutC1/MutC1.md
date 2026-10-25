# MutC1 — mutation probe of `PRED-C1-r38-v3` (mado round 38, wave 1)

Attacked: `quality/counters/c1-r38-event-ground.py` at lane `master` HEAD
`bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5` (lane file sha256
`6872e18d3003b5fcbf94adac4b259a4a3651d313e848dda8999572851fe71866`, unchanged before and
after every run — the lane was never written by this probe). Detector: the frozen
discrimination gate `quality/check-r38-discrimination.py` (sha256
`529569f692e653b532cb4dcb0325efb43b3bcac0421d34754c0e4d0667f00d77`) over the frozen
manifest `MANIFEST-r38-v1` (sha256
`96965518dc8ad98b52b28b406d66841758c80fd75610f9b94e0239b8adf838c8`, 19 controls), run
from a byte-identical scratch copy (`diff -r` clean).

**Result: all six mutants survive 19/19.** No control in the frozen manifest kills any of
the six mutations at verdict level; the pristine baseline reproduces the landed claim
(`correct=19/19 verdict=TARGET_MET`, exit 0), so nothing is inconclusive. Six coverage
findings below.

## Bounds compliance

- Lane production files read-only; the only lane writes are this report and a copy at
  `.ufo/waves/round-38/w1/scratch/MutC1/MutC1.md`. All mutants and run artifacts live in
  `/tmp/mado38-MutC1/`; gate sandboxes lived under `/dev/shm/mado38-MutC1-sb` and
  `/dev/shm/mado38-MutC1-diag` and were removed after use (`/dev/shm` back to 153M used).
- No git mutation in the lane (read-only `rev-parse`/`show`/`ls-tree` only; the gate
  itself clones with `--no-local` into its own tempdir). No socket contact, no
  compositor/config/service/package change, no subagent dispatch, no installs (none
  needed).

## Method

Scratch setup (all copies verified against lane digests):

```
cp LANE/quality/counters/c1-r38-event-ground.py  /tmp/mado38-MutC1/pristine/c1.py
cp LANE/quality/counters/c2-r38-eventq.py        /tmp/mado38-MutC1/pristine/c2.py
cp -r LANE/.ufo/waves/round-38/controls          /tmp/mado38-MutC1/controls
for i in 1..6: cp pristine/c1.py mutants/m$i.py   # then one edit each
```

Per run (mutant substituted for `--c1`; everything else frozen):

```
python3 -I LANE/quality/check-r38-discrimination.py \
  --c1 /tmp/mado38-MutC1/<variant>.py \
  --c2 /tmp/mado38-MutC1/pristine/c2.py \
  --manifest /tmp/mado38-MutC1/controls/manifest.json \
  --rev bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5 \
  --out /tmp/mado38-MutC1/runs/<name>.receipt
```

Baseline pristine run (quoted):

```
control=c1-live ... observed=TARGET_MET ok=1          (all 19 controls ok=1)
MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET
```

exit 0. The landed round-38 claim reproduces at lane HEAD.

## The six mutants (exact diffs vs pristine)

```
m1  203c203   len(rows.get(i, [])) == 1 and (        ->  len(rows.get(i, [])) >= 1 and (
m2  150-152   quote_floor_ok body                    ->  return True
m3  235c235   for rpath, digest, quote in pin_gates.get(i, []):
                                                   ->  for rpath, digest, quote in gates.get(i, []):
m4  193c193   c["a"] = int(body is not None and show(repo, base, path) is None)
                                                   ->  c["a"] = int(body is not None)
m5  243c243   g_ok = g_ok and stated and any("**OBS**" in l and re.search(rf"\b{i}\b", l) for l in lines)
                                                   ->  g_ok = g_ok and stated and any("**OBS**" in l for l in lines)
m6  251c251   c["l"] = int(hits >= need)             ->  c["l"] = 1
```

m1 note: the literal removal of the `== 1` check would crash `rows[i][0]` on row-less
ids, so the minimal non-crashing form keeps "at least one row" and drops only uniqueness.
m3 note: `gates` values are the same `(receipt, sha256, quote)` triples as `pin_gates`;
only the pin-cell requirement is skipped — the blob/digest/quote-in-blob checks in d stay.

Post-run mutant digests (m1–m6):
`c581f02244cee6de…`, `cbd93d7966658f2d…`, `89f16e5a3ee59be0…`, `e59074abed41a803…`,
`4b2e56033b614a32…`, `c2e8994c7e8afe39…` (full values in `/tmp/mado38-MutC1/` listings;
files unmodified by any run).

## Kill table (verdict level)

Every mutant × every control: `observed == expected`, `ok=1`. Gate summaries (quoted):

```
pristine rc=0 :: MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET
m1       rc=0 :: MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET
m2       rc=0 :: MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET
m3       rc=0 :: MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET
m4       rc=0 :: MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET
m5       rc=0 :: MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET
m6       rc=0 :: MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET
```

| mutant | controls killing it | verdict |
|---|---|---|
| m1 (c uniqueness) | none (0/19) | SURVIVED |
| m2 (quote floor) | none (0/19) | SURVIVED |
| m3 (d pin matching) | none (0/19) | SURVIVED |
| m4 (a new-at-base) | none (0/19) | SURVIVED |
| m5 (g OBS-id) | none (0/19) | SURVIVED |
| m6 (l lineage) | none (0/19) | SURVIVED |

c2 controls (10) are structurally unaffected — the mutants only alter the c1 instrument —
and scored `ok=1` in all seven runs, doubling as a harness-stability check.

That the harness really runs the `--c1` path it is given is proven inside the table: m1
changes `c1-duprow`'s failing set from `c,j` to `j`, m2 changes `c1-quotefloor`'s from
`d,f,g,h` to `d,f,g` (h flips 0→1), and m6 admits an entry pristine rejects (below). Same
harness, only `--c1` varied — so m3/m4/m5's total absence of change is a result, not a
wiring artifact.

## Clause-level diagnosis — which clause carries each reject instead

Recreated every (variant × c1-control) sandbox exactly as the gate does (clone → checkout
→ `apply_writes` → sandbox commit → counter run); 63 dumps at
`/tmp/mado38-MutC1/runs/diag-<variant>-<control>.txt`. Zero-clauses per entry (`E1` =
event-delivery-limits-r26.md, `E2` = event-queue-observability-r37.md):

| control (expect) | pristine | m1 | m2 | m3 | m4 | m5 | m6 |
|---|---|---|---|---|---|---|---|
| c1-live (MET) | —/— | —/— | —/— | —/— | —/— | —/— | —/— |
| c1-donothing (MISSED) | all/all | all/all | all/all | all/all | all/all | all/all | all–l/all–l |
| c1-selfreceipt (MISSED) | c,d,f,g,h,j,l | same | same | same | same | same | c,d,f,g,h,j |
| c1-quotefloor (MISSED) | d,f,g,h | same | d,f,g | same | same | same | same |
| c1-duprow (MISSED) | c,j | **j** | c,j | c,j | c,j | c,j | c,j |
| c1-nolineage (MISSED) | l / g,l | l / g,l | l / l | l / g,l | l / g,l | l / g,l | **—(admitted)** / g |
| c1-r28-verbatim (MISSED) | — / g,l | — / g,l | — / l | — / l | — / g,l | — / g,l | — / g |
| c1-token-stub (MISSED) | g,l | g,l | g,l | g,l | g,l | g,l | g |
| c1-clause-b (MISSED) | b,k | b,k | b,k | b,k | b,k | b,k | b,k |

(`all` = a,b,c,d,e,f,g,h,j,k,l — entries absent at the donothing rev. m6's donothing row
shows `l` forced to 1 by the mutant.)

## Findings

- **F1 (m1, clause c uniqueness) — SURVIVED.** The uniqueness predicate
  `len(rows.get(i, [])) == 1` appears twice, at `c1-r38-event-ground.py:203` (clause c)
  and `:226` (clause j), over the same ids. With c's copy dropped, `c1-duprow` is still
  killed by j alone (`m1 c1-duprow: … zeros=j ok=0`). One of the two copies is redundant
  by construction; no control can kill either copy without killing both.
- **F2 (m2, clause i quote floor) — SURVIVED.** With the floor off, `c1-quotefloor` still
  dies via d and f (`m2 c1-quotefloor: … zeros=d,f,g`, h now 1). Two causes, both verified
  on committed bytes: (a) the control's own rewrite regex `quote="[^"]*"` truncates S213's
  embedded-quote Gate value at its first inner `"` — the parsed quote becomes
  `e"option":"debug:disable_logs","int":1,"set":false}`, which is not in the S213 receipt
  blob, so d=0; (b) all four surface tokens live only inside backtick spans in the real
  entries (verified: present in body, absent outside backticks), so the control's body
  rewrite destroys them and f=0 regardless of quote handling. The floor clause is not the
  discriminator for its own named control; that control is over-determined and carries a
  quote-mangling artifact.
- **F3 (m3, clause d pin matching) — SURVIVED, zero observable effect.** No control ever
  places a non-pin Gate line for a pinned id, and h already requires pin-matched lines to
  exist, so iterating all Gate lines in d changes nothing anywhere. A control that could
  kill this mutant would need a pinned id whose pin-matched Gate line fails the blob check
  (wrong digest) while a self-consistent non-pin line passes — no such control exists in
  MANIFEST-r38-v1.
- **F4 (m4, clause a new-since-base) — SURVIVED.** `c1-donothing` checks out the round-37
  base `b4e47e98…`, where neither target entry exists (`git ls-tree -r --name-only
  b4e47e98… -- corpus/knowledge` lists neither file), so `body is None` → a=0 under
  pristine and mutant alike — the control rejects for absence, not for held ground. No
  control places a pre-existing entry with otherwise-valid wiring; clause a is never the
  deciding clause.
- **F5 (m5, clause g OBS-id requirement) — SURVIVED.** Every g-failure in the manifest is
  carried by `stated` (the Gate quote must appear in the entry body), not by the id
  requirement: token-stub states no quotes at all; nolineage/r28-verbatim fail g even with
  the id check removed (`m5 … zeros=g,l` / `zeros=g,l` unchanged). Notably, nolineage-E2's
  g=0 is itself a floor×stated interaction: S217's only floor-passing pin-matched quote is
  `bool                    m_logsEnabled = true;` while the crib states S217's other
  quote (`if (!m_logsEnabled)`, 2 words/19 chars, floor-rejected). A control stating real
  quotes next to an **OBS** block that omits or misnames an id would kill this mutant;
  none exists.
- **F6 (m6, clause l lineage) — SURVIVED at verdict level, with one entry-level flip.**
  For `c1-nolineage` × E1, l is the sole killer under pristine (`zeros=l`); under m6 that
  entry is admitted: `m6 c1-nolineage: event-delivery-limits-r26.md zeros=none ok=1 |
  event-queue-observability-r37.md zeros=g ok=0 | … admitted=1/2 verdict=TARGET_MISSED`.
  The control verdict stays MISSED only because the sibling entry still fails g — verdict
  masking. r28-verbatim and token-stub are then carried by g alone. Clause l's unique
  coverage is exactly one (control, entry) pair and is invisible at the verdict level the
  gate scores.

## Interpretation (coverage finding, not a contract change)

The frozen 19/19 discrimination result does not depend on any of the six mutated
behaviors: every reject in MANIFEST-r38-v1 is carried by some other clause (j for c; d+f
for i; h for d's pin restriction; entry absence for a; stated-quote for g's id check; g
for l, except the masked nolineage-E1 case). This is the same shape the registration
already declares as the residual ("fabricated self-consistent artifacts still pass") but
one level down: the v3 clauses are mutually redundant on this control set, so the manifest
cannot detect a counter that silently loses any one of them. Per probe discipline this is
recorded as a coverage finding; the counter, manifest and claims are untouched.

## Incident log

- First execution batch ran 7 gates concurrently and produced 3 harness ERRORs
  (`c1-nolineage` clone-failed, `c1-token-stub` clone-failed, `c1-clause-b`
  checkout-failed) while `/tmp` sat at 95% (6.6G free). Outputs preserved as
  `runs/*.contended.out`; superseded by the clean sequential reruns above (19 leftover
  `mado38-dsc-*` sandbox roots removed, ~28G freed). Disclosure: `mado38-dsc-` is the
  gate's default tempdir prefix, so that cleanup may also have removed in-flight sandbox
  dirs of a concurrent sibling's gate run (e.g., MutC2); gate sandboxes are per-run
  ephemeral scratch and no durable artifact matches the prefix, but the possibility of
  cross-agent interference is flagged here for the record.
- No tools installed (tooling directive: nothing needed).

## Artifacts

`/tmp/mado38-MutC1/`: `pristine/` (c1, c2), `mutants/m1..m6.py`, `controls/` (byte-identical
manifest copy), `runs/{pristine,m1..m6}.out` + `.receipt` (gate receipts),
`runs/diag-<variant>-<control>.txt` (63 clause dumps), `runs/*.contended.out`,
`controls-dump.txt`, `head-entries/` (E1/E2 at HEAD). Lane-side copy of this report:
`.ufo/waves/round-38/w1/scratch/MutC1/MutC1.md`.
