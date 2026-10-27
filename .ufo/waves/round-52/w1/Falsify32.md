# Falsify32 — C2 source quote/pin binding

## Finding

**Attacked item/predicate:** C2's binding clause — frozen `claims-frozen.md`: "each material factual proposition maps to a pinned source quote <=25 words"; frozen `registration.md`: "each maps to an opened-this-round `S###` row, **a pin path/revision and exact located quote <=25 words** … A counter checks proposition count, row/pin/quote bindings and complete mapping." Attacked specifically: the *pin path/revision* half of the binding — whether the counter's quote check binds the quote to the **source at the pinned revision**, or only to **lane-committed bytes under the pin path**.

**Concrete bypass reproduced: pin-content provenance gap.** The binding machinery (inherited pattern: `quality/counters/c2-r51-dispatch-entry.py` `clause_b`/`bind_row`, which the round-52 counter seat `C2CounterDraft` is tasked to rebuild checking "row/pin/quote bindings") verifies a quote by slicing the pin file with `at_lines` and testing `collapse(q) in hay` where the pin bytes come from `loader()` = `git show <rev>:.ufo/waves/round-<N>/fetch/<pin>` — bytes **committed in the lane repo by the same authority that wrote the entry**. The upstream URL/revision recorded in the `S###` registry row is never consulted; the lane-committed `SHA256SUMS` manifest is never read (string absent from the counter); no digest obtained from upstream is checked. The "revision" half of "pin path/revision" is decorative in the counter's eyes.

A forger can therefore: doctor a lane-committed pin file (e.g., line 32 of `Hyprland-legacy-DispatcherTranslator.cpp` at `.ufo/waves/round-51/fetch/`), regenerate the lane-committed `SHA256SUMS`, and write the entry quoting the **fabricated text** with an internally consistent digest manifest. The counter binds all rows green. The claim's "grounded in sources opened this round" is satisfied in the counter's verdict while the quoted bytes do not exist at the pinned upstream revision.

**Corroborating looseness (same clause):** "exact located quote" is enforced as *substring containment after whitespace collapse* over the cited line span (`bind_row` at `quality/counters/c2-r51-dispatch-entry.py:344-361`). A 4-character fragment (`run(`) binds against real upstream bytes as a row-supporting quote, so even non-doctored bindings can be content-free tokens.

## Reproducible setup / command / actual result

Setup: read-only lane checkout at the frozen base (`git rev-parse HEAD` = `85d57a818c3707397e21c840b6498b105ba798aa`; `git status --porcelain` before and after shows only the pre-existing untracked `.ufo/waves/round-52/`). Disk guard: `df -h /fast/scratch` → 597G free. Scratch root `/fast/scratch/hyaku/mado-r52/Falsify32/`; `git rev-parse --show-toplevel` asserted equal to each fixture dir before its commits. Fixture build (copies the lane's round-51 upstream snapshot — itself pinned at Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f` per the entry's manifest — then doctors one line; registry rows S364–S369 copied verbatim from `corpus/SOURCES.md:313-318`):

- **fixture A (attack):** `Hyprland-legacy-DispatcherTranslator.cpp` line 32 changed from `return {.success = false, .error = "Bad dispatcher"};` to `return {.success = false, .error = "Falsify32 planted refusal string"};`; `SHA256SUMS` regenerated; entry = the real `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` with all 4 `Bad dispatcher` occurrences replaced by the planted string and its digest manifest updated to the doctored sha256 (`8729df1c…0d9a`, recorded in `receipt-doctoring.txt`) so the forgery is self-consistent.
- **fixture B (control):** pristine copies, pristine entry.

Command (driver `Falsify32/driver-repro.py`, kept in seat dir; loads the real counter via importlib):

```sh
python3 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/Falsify32/driver-repro.py
```

Actual result:

```
== A: doctored pin + fabricated quote ==
clause_b: (1, 'rows=6/2 pins=6')
== B: pristine control ==
clause_b: (1, 'rows=6/2 pins=6')
== C: fragment quote on real bytes ==
bind_row: (('Hyprland-KeybindManager.cpp', 113, 113, 'run(', '**OBS** S364: planted fragment ...'), '')
```

Byte-identical verdict strings for doctored and pristine pins; the doctored S365 row binds the fabricated quote with no note. Source truth at the pinned revision (web-reader grep of `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp`, accessed 2026-10-27 — the S365 URL, a source opened in round 51, permitted under the source-only boundary):

```
 31|    if (!m_dispMap.contains(d))
*32|        return {.success = false, .error = "Bad dispatcher"};
 34|    return m_dispMap.at(d)(w);
planted string: no matches found
```

Sanity (harness correctness): the full real counter run read-only against the lane at HEAD exits 0 with `clauses_met=4 admitted=1/1 verdict=TARGET_MET` (`receipt-real-counter-lane-head.txt`), so the module/driver exercised is the admitted one.

**Reproduced: yes** — fabricated provenance passes the binding clause identically to genuine provenance.

## Why the named backstop does not close this as specified

The frozen predicate outsources truth to "an independent non-author samples actual source truth". That reviewer samples *quotes*; the counter's verdict already printed TARGET_MET on a doctored entry whose every row cites registry rows that claim upstream URLs. The finding is not that semantic entailment is unautomated (conceded by the claim); it is that **provenance** — the "pin … revision" binding the predicate explicitly names — is checked against a lane-committed file with no upstream anchor, so the counter alone cannot distinguish "grounded in sources opened this round" from "grounded in lane-committed bytes labeled with a source URL". The C2 no-work control (`controls/c2-do-nothing.md`) tests entry absence at base, not pin integrity, so it cannot catch this either.

## Impacted axes

- **Coverage (C2):** the admitted entry can carry propositions bound to bytes that are not the opened source — the claim's "grounded in sources opened this round" is weaker than stated.
- **Operability (C1-adjacent, no harm):** none — C1 is causally separate; this finding touches no C1 artifact or predicate.

## Smallest safe correction

Any one of, in order of strength:

1. **Bind pins to upstream, not to the lane.** The new counter (or its selftest contract) verifies each cited pin's bytes against the upstream URL at the pinned revision — e.g., one web-reader fetch per pin compared byte-for-byte, or a digest **obtained from upstream** (not lane-committed `SHA256SUMS`) checked against the lane pin. Then the doctored fixture fails closed.
2. **Tighten the predicate wording** to "quote binds to a lane-committed pin file" and move provenance wholly onto the non-author reviewer with an explicit per-pin (not sampled) verification duty.
3. Independently cheap: require quoted spans to be whole lexical statements (e.g., minimum word count ≥ 3 and boundary characters), closing the 4-char fragment demo.

## Evidence and limits

- Frozen text: `.ufo/waves/round-52/claims-frozen.md` (C2) and `registration.md` (C2 frozen predicate, "row/pin/quote bindings"; reviewer sampling; C2 control = entry absence at base).
- Counter source (read-only): `quality/counters/c2-r51-dispatch-entry.py` — `resolve_pin` :267-281; `bind_row` :329-376 (substring containment :353-361); `clause_b` loader :402-404 (`git show <rev>:.ufo/waves/round-51/fetch/<pin>`); `SHA256SUMS` never referenced (grep count 0).
- Wave plan `.ufo/waves/round-52/w1-plan.json` seat `C2CounterDraft`: "Check proposition mapping/count, row/pin/quote bindings and index path; semantic entailment requires outside review." — no upstream-provenance step assigned anywhere in the plan; as of this seat's runs the round-52 counter is not yet committed (lane HEAD = base), so this attack is executed against the inherited binding machinery and the specified contract, not a finished r52 artifact.
- Commands/results: this report; seat-dir receipts `receipt-upstream-line32.txt`, `receipt-doctoring.txt`, `receipt-clause-b-A-doctored.txt`, `receipt-clause-b-B-control.txt`, `receipt-fragment-bind.txt`, `receipt-real-counter-lane-head.txt`, `receipt-lane-git-status.txt`; driver `driver-repro.py`.
- Source candidate: Hyprland `src/config/legacy/DispatcherTranslator.cpp` @ `efb50993780079460b0cbed1363e2166a2de1d9f`, URL above, accessed 2026-10-27 via web reader; located quote `"Bad dispatcher"` at line 32; planted string absent.
- Safety: source-only round respected — no package queries, no live host/process/compositor reads, no input capture, no screenshots, no producer execution; the one full-counter run was a read-only checker over `git show`/`ls-tree` bytes; lane tree verified untouched. Web reader used only for a source opened in round 51.
- Limitations: clause_c (novelty) and clause_d (held) are out of this seat's attack scope; the doctored fixture models a forging worker, which the round's honesty rules forbid — the value here is control falsification (the binding check cannot detect the forgery), not a recipe. Scratch removed after receipt copies; no installs were needed (no tooling changes).

## Deliverables

- `.ufo/waves/round-52/w1/Falsify32.md` — this bounded binding finding.
- `.ufo/waves/round-52/w1/Falsify32/driver-repro.py` — reproduction driver (imports the real lane counter).
- `.ufo/waves/round-52/w1/Falsify32/receipt-*.txt` — seven receipt copies of commands/results quoted above.

Report: `.ufo/waves/round-52/w1/Falsify32.md`
