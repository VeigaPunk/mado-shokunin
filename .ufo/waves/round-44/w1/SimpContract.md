# w1 / SimpContract — dead weight in the C1 contract extension and the C2 clause-h delta

Leaf seat, lane `mado-shokunin`, round 44 w1, freeze `e2289516a9a857f55cda7be635933e89b931c3da`
(base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`). Frozen files were read, never edited.
**Deletions made: none** (no edit scope). **Deletion candidates: 7 in the C1 contract text, 3 in
the C2 clause-h text/code** — one of the C2 ones (D8) is a predicate hole, not only weight.

Full detail, sentence tables, mutant matrix and exact deletion text:
`.ufo/waves/round-44/w1/SimpContract/dead-weight.md`. Receipts in the same directory.

## Criterion and method

A sentence is load-bearing iff some input can distinguish a tool that obeys it from one that obeys
the rest and violates it. Two failure modes, both tested by building the pair and running the
reference:

- **entailed** — the violating tool necessarily breaks another sentence (no constraint is added);
- **unobservable** — both readings produce identical output on every input (no reading can be
  wrong).

One minimal mutant per sentence, scored with the predicate's own 26 clause-f cases plus the tool's
`--selftest` in the counter's bubblewrap sandbox (nonce `simpaudit`); then the **frozen counter
end-to-end** on the mutant the lattice cannot see. 13 mutants plus the reference control, receipts
in `w1/SimpContract/receipts-mutants.txt`.

## Findings

**F1 (C1, the one real weight). The verdict-order claim `FULLSCREEN (fsmode 2)` before
`MAXIMIZED (fsmode 1)` is unobservable — it constrains nothing and cannot be violated observably.**
- Structural: `fsmode_of` (`c1-r44-geometry-states.py:88-92`) returns one of `{0,1,2}`, so the two
  `elif` guards are mutually exclusive; the summary counters are indexed by the verdict word, so
  permuting the two branches moves nothing.
- Differential: branch-swapped tool vs reference over 17 `fullscreen` values × 8 sizes × 4 classes
  × floating true/false + 3000 random multi-client docs → **4088 inputs, 0 differing outputs**
  (`receipts-differential.txt`).
- Frozen instrument: the swapped tool scores
  `PRED-C1-r44: fixtures=26/26 tool=present verdict=TARGET_MET`, clauses `a:1 b:1 b4:1 g:1 r:1`,
  and its own selftest still passes `91/91` (no reference selftest case can exist for it).
- Cost: `.ufo/waves/round-44/receipts/ctl-c1.txt` is built from single-defect variants; "MAXIMIZED before FULLSCREEN"
  added as a future defect control would be a false expectation (it must PASS). Priority 1, D1.

**F2 (C1). The ten-value example table `(absent, null, 0, 3, -1, true, 2.0, "2", lists and objects
are 0)` is entailed by the rule it follows.** Each of the ten values falsifies "a JSON integer (not
a boolean, not a float) equal to 1 or 2" and yields 0; all ten are already drawn by `FS_POOL` /
`fsvals0`, so deleting the table loses no coverage and removes a second statement that can drift
(D2). This is a restatement, not a hole.

**F2b. The ticket's hint is refuted by measurement.** "not a float" is *load-bearing*: JSON `2.0`
parses to a Python float and compares equal to `2`, so a tool that accepts floats reports
FULLSCREEN; four fixtures catch it (`mut_float` 22/26, selftest 89/91), likewise "not a boolean"
(`mut_bool` 22/26). Only the FULLSCREEN/MAXIMIZED adjacency is dead.

**F3 (C1). Five sentences add no constraint because the round-42 contract (explicitly in force)
or another sentence of the same paragraph already states them.** Each violation is still caught by
the fixtures — it just breaks the other sentence first:
- E4 `The client line is unchanged except for the two new verdict words.` — r42's client-line
  template (`c1-r42-geometry.py:52`); `mut_clientextra` fails 19 fixtures (D3).
- E5b the position clause `between `badsize=<n>` and ` verdict=`` — the reference output template
  (`ctl-ref-tool.py.txt:67`); `mut_afterverdict` fails 9 (D4).
- E7 `FULLSCREEN and MAXIMIZED clients count as matched and never as differ …` — MATCHED is
  rule-conditional in r42 and does not read `fullscreen`; "never as differ" is the order; the top
  rules and exit codes are r42 lines 55-56; `mut_statenotmatched` fails 11 (D5).
- R3 (reference) `Such a client's reported size says nothing about the rule, so it gets its own
  verdict instead of AGREE, DIFFER or TILED.` — the order sentence; no constraint (D6, taste call).
- R7's tail `so a dump with no maximized or fullscreen matched client prints the round-43 line
  unchanged` — entailed by its own first clause (D7).

**F7 (C2, priority 1 for C2 — hole, not weight). `neither line is a clause-g claim line` never
happens, and the code implements a broader exemption that a forged entry can use.**
A census line names no `S###` id, so clause g's hit test and `all_body_lines_bound` skip it with or
without the exemption — the sentence describes an unreachable case. The code (lines 560-563)
exempts by **prefix**, so *any* line starting `gkeep client ` / `hyprland sendWindowSize ` escapes
clause g even when it cites an id without a quote or locator. Also `l not in census_lines` there is
dead (both census strings start with one of the prefixes). Simulation over the real filter
(`receipts-entrylines.txt`): a good entry is unaffected by removing all three predicates; a
prefixed forged line stops escaping. C2 has **no positive control**, so this channel is exactly
where a forged entry would go. Fix = D8; it **tightens** the predicate, so it must ride a v2
freeze, never the data commit (kill rule).

**F8-F9 (C2, inert parser detail).** With the receipts pinned by sha256, the clause-h numbers are
constants (`gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep`;
`hyprland sendWindowSize xdg_setSize=1 x11_configure=1`), so a qualification that cannot change
them is dead:
- `with `#` comments removed` — raw and stripped give the identical triple; the two matching
  `gkeep-ui.py` lines (449, 476) carry no `#` (D9). `strip_comments` must stay: clause d+
  (`quote_in_code`) uses it.
- `up to the first following line that is exactly `}`` — the first exact-`}` line is 1754, brace
  matching also ends at 1754, and no exact-`}` line sits inside 1733-1753. The *scope* (body vs
  whole file) **is** load-bearing: body gives `->setSize(=1 ->configure(=1`, the whole file `2` and
  `3` (D10).
- Adjacent, not dead weight: `set_default_size(W, H)` in the docstring does not say the regex
  requires `", "` with the space (line 391); a pin without the space makes `len(sd)==0` and clause
  h false with no diagnostic. Under-specified, reported only.

## Preserved contract

Nothing above changes an admissible behaviour. Every load-bearing sentence stays: the fsmode rule
with all three qualifications, the order BADSIZE → state → TILED → AGREE → DIFFER minus the
unobservable adjacency, the summary condition and its fields, the client line, the top verdict
rules and exit codes, and `otherwise it is byte-identical to the round-43 line` (that one is
**retained deliberately**: it is the claim clause r tests; deleting the sentence would orphan the
check). C2 keeps both entry-side census lines, `verbatim / outside fences / exactly once`, the body
scope, and recomputation-from-pins. Clause f, b, b4, g and r are untouched; after D1-D7 the
mutants in the receipt would still fail the same fixtures and `mut_swap` would still pass 26/26.

## Tradeoffs

- D2/D3/D4/D5 remove standalone readability (examples, the client-line sentence, the field
  position) in exchange for one statement per rule; all four are recoverable from the reference,
  the model and clause f.
- D6 (R3) is the most compact rationale in the reference docstring while constraining nothing —
  listed as a taste call, not a correctness one.
- D1 changes two document texts that must move together (counter docstring and reference); doing it
  to one only would leave the reference stating a rule the predicate does not score.
- E3e (AGREE before DIFFER) is unobservable for the same structural reason (`mut_differagree`
  26/26) but is **inherited from round 42 and out of scope**: not proposed for change.
- The inherited `PRED-C2-r43-v2 text` block still carries the old clause h; the precedence sentence
  at line 27 reconciles it and the block is marked inherited, so nothing is proposed there.

## Not run / limits

- No entry was built and no positive control exists for C2; I did not run the counter against a
  modified clause-h code path (frozen file). D8's safety rests on reading every `entry_lines` use
  (lines 560, 575, 580, 583 — all name-gated) plus the filter simulation.
- C2 was not scored end-to-end (nothing to score at the freeze); only `host_census` was called
  directly on the pins.
- The candidate texts were not applied anywhere: no frozen file was edited, and no measurement
  claims a post-deletion score. The claim is narrower and mechanical: no input can distinguish the
  deleted sentences' readings.

## Evidence

`w1/SimpContract/dead-weight.md` (sentence tables, exact deletion text, quote locators),
`receipts-mutants.txt` (13 mutants + control, and end-to-end `TARGET_MET` on the swapped tool),
`mut_swap.py` (the one-change tool the finding scores), `mutrun.py` / `receipts.py` (repro);
`receipts-differential.txt` (4088 inputs, 0 differing), `receipts-entailment.txt` (E2 entailment,
E6 identity 500/500, C2 comment/body/census measurements, source hashes),
`receipts-entrylines.txt` (exemption reachability), `verify-quotes.py` (**41 quotes, 0 failures**:
each present on its cited line, locator recomputed, ≤25 words, present in the receipt).

Nothing was installed (python3 3.14.8 stdlib, host `bwrap`, host `git`). Scratch
`/fast/scratch/hyaku/mado-r44/SimpContract` removed on exit; lane bytes outside my seat dir are
untouched (`git status --porcelain` shows only the wave's untracked directories).
