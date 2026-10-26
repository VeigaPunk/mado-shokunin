# CritC2Forgery — round 45 w1 (mado, C2 coverage predicate)

**Attack surface.** `PRED-C2-r45` (`quality/counters/c2-r45-monitor-entry.py`, frozen, not edited): admitted `1/1`
means the entry's claims are sourced. The question this seat answers: does the predicate admit an entry, registry row
or lesson that is *wrong*?

**Answer: yes, nine ways.** All nine forged revisions score `admitted=1/1 verdict=TARGET_MET`, exit 0, all clauses
`a:1 … j:1`. Five of the nine are closable by a one-line tightening that keeps the frozen positive control P
admitted; four are the docstring's declared residuals, and **three of the admitted classes are not in the docstring's
residual list at all**.

Findings file: `.ufo/waves/round-45/w1/CritC2Forgery/forgeries.md`.

## Method (reproducible from the seat directory only)

`build-forgeries.py` rebuilds P (freeze `22a8ded` + `l1-draft/build-pos.py`, per the positive-control recipe), then
commits one forgery on top of P per class; `tighten.py` patches *copies* of the counter in scratch with the five
proposed edits and runs the 60-cell matrix (5 counters × P + 9 forgeries); `evidence.py` builds the evidence receipt
and verifies every quote. Scratch was rebuilt from empty and deleted afterwards; nothing outside
`.ufo/waves/round-45/w1/` was written and no compositor command was run.

## The nine admitted forgeries

| # | forgery | false against | clause that should catch it | frozen | disposition |
|---|---|---|---|---|---|
| F1 | inverted lookup claim next to the true `erase_if` quote and its locator | MRM.cpp:96 reverse scan | g (quote+locator), j | admitted | declared residual (counter:62) |
| F2 | header table overclaims; state column forged (`OBS (verified on the host)`) | MonitorRule.hpp:46 (60 Hz), legacy ConfigManager key loop | g/j bind only id-naming lines | admitted | declared residual (counter:63) |
| F3 | census contradicted **in tokens** one space from the regex (`scale_search = 44`, `default_refresh : 45`) | Monitor.cpp:1010 (89 steps), MonitorRule.hpp:46 | h (prose census scan) | admitted | **T1 closes** |
| F4 | census contradicted **in words** ("two hertz", "ninety steps", "nine key pairs") | Monitor.cpp:837, :1010, 8 keys | h | admitted | residual (words ≠ tokens) |
| F5 | registry S304 cell 6: "Supersedes S158 and S162; the first matching rule … wins" | MRM.cpp:96; S158/S162 are other files | c (cells 2,3,6 unread) | admitted | **T2 closes** the supersession half; rest residual |
| F6 | false decision table inside a fenced block | MRM.cpp:96, MonitorRule.hpp:46, HyprCtl.cpp:327 | b/g/j/h all skip fences (counter:16) | admitted | **T3 closes** |
| F7 | §6 claims 59.94 Hz / scale 1.25 / `DIFFER` while citing the receipt that says 99.997 / 1 / `AGREE` | live-monitors-host-l1.txt | i (no clause reads `receipts/`) | admitted | **T4 closes** |
| F8 | README row says `merged` + `supersedes S290-S297` | the round's own draft status | f (counter:615 matches the prefix) | admitted | **T5 closes** |
| F9 | the sentence that satisfies the closeness surface is inverted (`100 px and 10 Hz`) with locator+keyword kept | Monitor.cpp:837 | j (locator+keyword, not truth; counter:64) | admitted | declared residual |

## Tightenings — all tested, all keep P admitted, each rejects only its target

60-cell matrix (`frozen-and-tightened-matrix.txt`): 55 admitted, 5 missed — one miss per tightening, P `admitted=1`
under all five, no collateral on the other eight forgeries.

- **T1** counter:588 → `r"\b(%s)\s*[:=]\s*(\S+)"` (census token followed by spaced `=` or `:`). F3 → `h:0`.
- **T2** clause c new-id branch → reject `supersed*|replac*|obsolet*` anywhere in a new row. F5 → `c:0`. This is the
  round-44 D6 class (false supersession) arriving through a cell no clause reads.
- **T3** every fenced block must occur verbatim in a pinned receipt (a fence is a quotation, not a claim). P has zero
  fences, so vacuous for P; F6 → `b:0`.
- **T4** a line carrying a verdict token *and* a `receipts/…` citation must find that token in the cited receipt.
  P's §6 line cites the live receipt for `AGREE`, which it contains; F7 → `i:0`.
- **T5** the README index row must be three cells, `draft`, expanding to exactly the cited id set. F8 → `f:0`.

## What the predicate's self-account misses (the part that matters)

The frozen docstring declares four residuals (counter:62-65: quote-beside-claim, id-less table, unread registry
cells 2/3/6, clause j's truth gap). F1, F2, F4, F5-content and F9 are inside that account — honest, unfixable by a
counter. **But three admitted classes are outside it:**

1. **Fences (F6).** counter:16 removes fenced text from every match; the residual list never says fenced content is
   unbound. The `HIDDEN-LINE` control only tested the *unfenced* shape (`g:0`), so `receipts/ctl-c2.txt` PASS is not
   evidence about a fence. A false table is admitted in a fence and rejected one line later without one.
2. **Verdict citations (F7).** Clause i reads as coverage of the receipts plane; nothing binds a sentence to the
   receipt it cites, so a claim can cite the receipt that refutes it.
3. **The index row (F8).** Clause f checks one column-0 prefix and nothing after it; the row's status and id list —
   its only claim — are free.

`receipts/ctl-c2.txt` (10/10 as designed) is disjoint from all nine classes: the controls test provenance (bytes,
digests, URL, locator width) and one unfenced hidden line.

## Recommendation to the L1 (before any data commit)

- If C2 keeps PRED-C2-r45 as frozen: the admission must be read as **provenance only**, and the three undeclared
  classes (fences, verdict citations, index row) should be added to the residual list so the claim's scope is honest.
- If the round wants them shut, the kill rule allows a v2 re-registration with a new freeze before data; T1–T5 compose
  (disjoint in the matrix), each is a single string replacement, and each was tested to keep P admitted.
- Do **not** try to close F4 (word-numbers) or F5's content half with a counter: the synonym table needed is a prose
  model, i.e. the non-author reading already declared.

## Evidence (all in `.ufo/waves/round-45/w1/CritC2Forgery/`)

`forgeries.md` (per-forgery lines, clause, tightening or residual) · `evidence.txt` (pin/counter/live/registry
chapters at the cited locators + the census recomputed from the pins) · `forgery-diffs.txt` (the forged lines,
cited by line) · `forgery-scores.txt` (frozen counter per forgery, incl. `surface=get-reverse … cited=1` for F1 and
`surface=closeness … cited=1` for F9) · `frozen-and-tightened-matrix.txt` · `p-control.txt` · `revs.txt` (commit map)
· `quote-check.txt` (31/31 quotes verified) · `build-forgeries.py`, `tighten.py`, `evidence.py`.

**Limits.** Candidates on a clone of the freeze; no round-45 data commit existed to attack, and this seat did not
read, edit or predict it. No host mutation, no pacman, no installs. **Not claimed:** that the L1 would make these
mistakes in good faith — only that the predicate would not stop it if it did.
