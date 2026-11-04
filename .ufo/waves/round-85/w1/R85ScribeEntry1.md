# R85ScribeEntry1 — round-85 C1 knowledge entry

Seat: scribe. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Freeze revision `3905311c75a39c5710413105865c0a1a7dd0116a`; base
`5f174ca48d4f9cf94abf1a8c58b7d6f88733aced`. Scratch
`/fast/scratch/hyaku/mado-r85/R85ScribeEntry1` (removed before yielding).

## What was written

`corpus/knowledge/bar-footprint-identity-causes-r85.md` (14,432 B, 179 lines at
handoff). Nothing else in the lane was written by this seat. No git mutation, no install, no
pacman transaction, no subagent dispatch.

The entry opens with the provenance trio (`source:`, `verified-at:`, `recheck:`), cites S486
(`corpus/SOURCES.md:438`) and the lane's own frozen controls, and carries:

- the ten-token cause vocabulary of `tools/mado-barfoot.py` at the freeze revision, each with
  its stage, its raise site (file:line), the defect class it refuses, and its frozen witness;
- what each refusal keeps out of the join — the three namespace-keyed places
  (`tools/mado-barfoot.py:492` band lookup, `:919-920` attribution map, `:1005` live lookup)
  where one name carrying two surfaces would collapse them;
- the four separations round 84 could not see (equal-valued vs interleaved duplicate keys,
  one-level vs cross-level extras, case-distinct names vs a case-variant allocation key, the
  bar's own name vs two extras);
- the measured freeze-revision result, the no-work control, and a per-mutant table naming
  the failing witness of each of the ten declared identity mutants;
- the limits the assignment named (join's input grammar rather than a layer-shell uniqueness
  law; the cause token is not a protocol error code; a right-stage wrong-cause refusal is
  caught only by the frozen population) plus the ones the round's own review measured;
- what remains unknown (arbitrary duplicate handling; protocol-level identity semantics).

## Commands actually run, with outcomes

1. Full frozen counter at the freeze revision (the declaration's counting command, no
   `--no-mutants`), exit 0:

   ```
   MADO_R85_IDENTITY: cases=72 correct=72 mutants=51 killed=51 base_correct=62/72
                      carried=61/61 tool_selftest=152/152 verdict=TARGET_MET
                      rev=3905311c75a39c5710413105865c0a1a7dd0116a
                      tool_sha256=d2eb4547b2e285fb80415e81b70c05e47aa6184eadb863e3cd72dab43e6bfd12
   ```

   Base line from the same run: `MADO_R85_BASE: correct=62/72 ... base_rev=5f174ca4…`;
   control line `carried=61/61`, controls sha256
   `bacae37d29d06e4f9d623262c05f2975bcba338e650dbd38cbbd4039ca6216a1`.

2. The same counter with `--no-mutants`, exit 0: `cases=72 correct=72 … tool_selftest=152/152`
   (a second, independent invocation of the case clause).

3. Per-witness CLI probe: the eleven round-85 identity witnesses materialised from the frozen
   control file and run through the frozen tool's real file-input CLI. Every cause token
   observed exactly as declared, e.g.
   `ERROR (stage=setup cause=alloc-duplicate-key …)`,
   `ERROR (stage=setup cause=namespace-duplicate-cross-level …)`,
   `ERROR (stage=model cause=live-duplicate-surface …)`; the accept witness
   `ns-case-distinct-accepted` returned rc 0 `verdict=CLEAN` band 66.

4. Per-mutant witness attribution, replayed through the counter's own `run_cases`
   (10 mutants, 10 lines of output, all killed). The table in the note is that output.

5. Predicate probes against the counter's own `expected_ok` (no lane file changed):
   a right-stage refusal carrying a wrong cause is accepted by all 14 carried error cases;
   `cause=alloc-duplicate-key EXTRA` accepted, `cause=alloc-duplicate-keyX` refused,
   `cause=alloc-duplicate` refused; a setup error never satisfies a model refusal.

6. Gate checks on the new note:
   - `python3 -I quality/check-index.py --root .` → `indexed=105/105 missing=0 dangling=1`.
     The one dangling index row is `knowledge/runbook-status-classes-r85.md` — the sibling C2
     entry, which does not exist yet in the working tree. Not this seat's file; the index row
     for `knowledge/bar-footprint-identity-causes-r85.md` is already present and matched.
   - `python3 -I quality/check-index-rows.py --root .` → 14 `ERROR row-outside-map` lines and
     6 warnings, byte-identical to the same gate at the freeze revision (14 errors there too).
     This gate was already red before this note; the note adds no new finding
     (`holds-no-overlap` count 0, no `cited-path-missing` for this note).
   - `python3 -I quality/check-locators.py --fetch .ufo/waves/round-84/fetch
     corpus/knowledge/bar-footprint-identity-causes-r85.md` → `CHECK_LOCATORS: locators=0
     miss=0` — identical to the r84 sibling note (the locator checker only resolves names
     that exist in the fetch directory, and this note cites no fetched receipt by locator).
   - `python3 -I quality/check-cited-revisions.py --repo . --text <the new note> --path
     quality/counters/c1-r85-identity-causes.py` → `RESULT error claims=0 mismatched=0`,
     same shape as the r84 sibling note's result (no `measured at <hash>` claim in either, so
     the probe refuses to report green in both).

7. Registry back-reference measurement (the lane's own `quality/counters/c3-r56-used-by.py`),
   in a scratch clone only: adding this note to the clone without a SOURCES used-by pointer
   produces `missing: S486 corpus/knowledge/bar-footprint-identity-causes-r85.md`
   (`missing=20`, the base being `missing=19`); adding the pointer to S486's used-by cell in
   the clone returns that leg to `missing=19`. The two `extra` pairs the same run reports
   (`S488`/`S489` → `corpus/knowledge/runbook-status-classes-r85.md`) belong to the sibling C2
   entry and resolve when that file lands.

## Findings that constrain what the entry may claim

- **Nine of the ten tokens are bound by the frozen population, not ten.** `alloc-negative`
  has no cause-bound witness: the carried case `alloc-negative-refused`
  (`.ufo/waves/round-85/controls/c1-cases-r85.json:2744-2757`) pins stage and exit code
  only. The entry says this in the table and in the limits, and cites the round's own reviewer
  measurement: a tool refusing the negative band with `cause=alloc-not-object` instead of
  `cause=alloc-negative` scores 72/72 on the frozen cases — a case score, not a full-gate
  pass, because the change breaks the negative-allocation mutant's anchor and the tool's own
  cause selftest.
- **The cause check is a space-delimited substring over the whole stdout, not one canonical
  error record** (`quality/counters/c1-r85-identity-causes.py:310-318`). The entry records the
  measured consequences and the reviewer's cause-flooding variant (72/72 cases, selftest
  152/152, but only 48/51 mutants die).
- **The frozen 72 cases do not discriminate three scorer weakenings or a whitespace-aliased
  tool key**, per `.ufo/waves/round-85/w1/R85MutationTester.md`: a bare-substring cause
  scorer, a casefolded cause scorer and a prefix stage scorer each still score 72/72; a tool
  storing `out[name.rstrip()]` also scores 72/72 because no frozen witness carries a
  whitespace-aliased allocation key. The entry states this as a limit on what the cases
  discriminate, and does not claim the frozen predicate is false.
- **The held round-84 tool is the no-work control at 62/72**, carrying the same 61 cases
  unchanged; the 61 carried cases are byte-equal to
  `.ufo/waves/round-84/controls/c1-cases-r84.json` (verified by comparison, not transcription).
- The `alloc-unknown-namespace` token is raised at **two** sites with different messages
  (`:823-825` composition path, `:1021-1023` single-surface path); the entry says so rather
  than implying one site.

## Gates the entry deliberately does not claim

- No round admission, no promotion, no axis movement, no causal certification of the join.
- No claim that the ten-token vocabulary is complete: the entry names the nine bound tokens,
  the one unbound token, and the fact that the vocabulary was declared by
  `.ufo/waves/round-85/claims-declaration-r85.md`, not derived by this note.
- No claim about the compositor, the layer-shell protocol, or any host: no compositor IPC,
  socket request, config write or live capture was performed by this seat.
- The entry's own source line cites S486 and the frozen controls only; no new SOURCES row is
  proposed or written by this seat.

## Sibling-owned state observed, not touched

`corpus/README.md`, `corpus/SOURCES.md` and `corpus/QUALITY.md` already carry round-85
working-tree edits from the L1 (index rows for both round-85 entries, S488/S489/S490 rows,
QUALITY criteria 140-142). This seat did not edit them. The one item the L1 may still need for
this entry is the S486 used-by pointer named in finding 7 above: without it the lane's
`c3-r56-used-by.py` reports `missing: S486 corpus/knowledge/bar-footprint-identity-causes-r85.md`.
The pointer itself is in SOURCES.md, which this seat does not own.

## Recheck

```
python3 -I quality/counters/c1-r85-identity-causes.py --repo . --rev REV \
  --base-rev 5f174ca48d4f9cf94abf1a8c58b7d6f88733aced \
  --controls .ufo/waves/round-85/controls/c1-cases-r85.json \
  --carried .ufo/waves/round-84/controls/c1-cases-r84.json --scratch-root DIR
```

Expected at the freeze revision: `cases=72 correct=72 mutants=51 killed=51
base_correct=62/72 carried=61/61 tool_selftest=152/152 verdict=TARGET_MET`, exit 0.

## Honesty ledger

Every number in the entry is either (a) copied from a command this seat ran and named, (b)
copied from a committed receipt or report file that is named, or (c) a file:line at the
freeze revision that is named. The three review-derived measurements (the wrong-negative
cause scoring 72/72, the cause-flooding variant, the three scorer weakenings and the
whitespace alias) are attributed to `.ufo/waves/round-85/w1/R85ReviewerC1.md` and
`.ufo/waves/round-85/w1/R85MutationTester.md`, which this seat read rather than re-ran; this
seat's own measurements of those same properties are the predicate probes in item 5 above.
No check is reported as passed that was not run.
