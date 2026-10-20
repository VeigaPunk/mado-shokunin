# CriticC1Overfit — C1 suite is contract-anchored but has three concrete overfit holes; N/N alone is not an honest score

Scope: is the round-20 precision suite (authored same-round as the fix) overfit by
construction, what independent evidence must sit beside N/N, and what score is honest
when some cases were already green at the harmed tool. I extracted both tools
(`git show 1f7f995:tools/mado-tripwire.py` → sha `367be947…`, `9c54c56:…` → `c1ae45a7…`,
matching SCORECARD) and empirically re-scanned every landed case fixture at both
revisions in `/tmp/critic-c1` (fixture code never executed, `--scan` only).

## Verified, not assumed

- All 14 declared `before` labels in the two landed `cases.json` files reproduce
  exactly: 12 red@`1f7f995`/green@`9c54c56`, 2 green/green controls
  (`mapping-containers`, `module-alias-control`). Every L fixture in
  `CaseLeadsInvisible/` emits rows at `1f7f995` (normalized `observed`) and is clean
  at `9c54c56`.
- `evidence`, `observed_findings`, `lead_findings` appear nowhere in the harmed tool
  (grep, tool-1f7f995.py): every emitted row normalizes to `observed`. So any case
  whose expectation contains `lead` is automatically red at `1f7f995` — the harmed
  tool cannot earn a `lead` tuple by any behavior.
- The counter (`.ufo/waves/round-20/tw-precision.py`) compares exit + multiset of
  `(class, rule, line, evidence)` only — `normalized_findings` keeps exactly those
  four keys (lines 71–89, 92–94). `command`, `argv0`, `file`, `tool` are compared in
  **no** tuple position.
- The counter validates verdict shape (`schema`, `exit == rc`, `findings` list,
  lines 177–182) but never requires or types `observed_findings`/`lead_findings`.
- Per-case `sha256` is pinned inside `expected.json` and the suite is read at a
  `suite_rev` commit (lines 134–148) — post-hoc case drift is digested out. Good.
- `before` metadata lives only in seat `cases.json` drafts, is ignored by the
  counter, and (as far as the declared suite schema shows) is not carried into
  `expected.json`. [INFERENCE: final `expected.json` schema is L1's and not yet
  written; SUITE is still `None` in the counter, line 19.]

## Overfit verdict: bounded, not structural — with three fixable holes

Same-round authoring is mitigated by the contract (E1–E4 semantics), the digest pin,
and the P-at-`9c54c56` restoration anchor. But:

### F1 — `red at 1f7f995` is two different tests, and the suite may not distinguish them
Because every old row normalizes to `observed`, a case is red at the harmed tool
either because the tool **missed/misread the shape** (presence/class failure) or
because it emitted the right row with the **wrong evidence tag**. A repair could in
principle fix detection poorly yet sweep `lead` expectations by tagging alone —
guards (tw-recall 6/6, corpus diff loses-0) bound the recall side, but nothing in
the declared metrics splits red-by-presence from red-by-evidence. Honest reporting
must publish that split per family, or a `lead`-heavy suite reads as more repair
than it is.

### F2 — Tuple-only multiset forgives payload damage (weakest link)
A finding `{class: package_query, rule: pacman:-Q, line: N, evidence: observed}` with
`command: "pacman -Q"` (missing `hyprland`) or a wrong `argv0` passes the counter
identically to a correct row. Tuple-precision ≠ finding-precision — exactly the
class of subtle misreport a same-round suite can leave uncaught. Smallest safe fix:
add `argv0` (already emitted per row) to the compared tuple and to `want_findings`;
cheap, one field, no schema churn.

### F3 — `observed_findings`/`lead_findings` verdict counts are contract-required but counter-blind
Contract E1: "the verdict adds integer counts observed_findings and lead_findings."
The counter requires only schema/exit/findings. A tool emitting correct per-row
`evidence` but omitting or miscounting the two summary integers scores N/N. Fix:
two lines in `scan_case` — require `type(...) is int` for both keys whenever
`lead_findings`-bearing expectations exist, or unconditionally.

### F4 — The P-at-`9c54c56` guard is weaker than it reads
Rule B does not exist at `9c54c56`, so *every* py-eval helper-shaped P case is
trivially green there (verified: 14/14 green incl. every authored P case). The
guard therefore certifies only that no P case claims an impossible pre-harm red —
it contributes almost no *selectivity* evidence about the repaired tool.
Selectivity rests entirely on (a) the corpus diff, which is **loss-only**: an
overfit exemption list (fitting exactly the suite's `collections/shlex/json/…`
module set) loses zero corpus findings and passes; and (b) S/W families. Corpus
diff cannot see precision-only additions.

### F5 — Blindness is time-bound, not authorship-bound
The suite pin freezes bytes, but cases are authored while the fix is mid-flight and
seats can iterate against patched tools in `/tmp` (contract even instructs
`before`-measurement). The practical mitigations already in place — digest pin,
independently recomputable `before` via `tw-precision.py 1f7f995`/`9c54c56` — are
sufficient *if* the judge actually reruns the counter at both baselines and checks
`SUITE_PIN`'s commit carries no `tools/` change and is the first suite-landing
commit (the `--suite-rev` flag is a legitimate override, so the pin's provenance
must be verified, not trusted).

## What must sit beside N/N

1. **Judge-recomputed transition table**, not seat claims: per case,
   `(1f7f995, 9c54c56, final)` verdicts from the counter itself — the harness exists;
   only the reporting is missing.
2. **Red-reason split** (F1): cases red at `1f7f995` on presence/class vs. on
   evidence-tag only.
3. **A small held-out probe outside authored families** (F4): mechanical mutants —
   pure callee names no family listed (`queue.Queue(['pacman','-Q','x'])`,
   `struct.Struct`, `functools.lru_cache`-wrapped pure def), argv prog variants
   (`expac`, `pactree`-classed or non-classed literals), depth-boundary chains
   (depth 4 vs 5). Run once at final, reported separately from the suite score —
   one round of mutants kills list-fitting overfit that corpus diff cannot see.
4. **Corpus diff addition classification** (already declared) — plus explicit
   statement of how many added rows are `lead` vs `observed` (the new classes).
5. **Existing suite N/N + recall 6/6** (declared) — sufficient for regression.

## Honest score

N/N is the registered target and stays — but a bare "N/N" is inflated whenever
already-green cases fill the denominator (2 controls already landed; ≤2/seat is
contract-permitted). Honest form is three numbers: **R→G transitions** (the repair),
**stable green** (controls + non-reds), **G→R = 0** (the no-harm half), with the
red-reason split from F1. A suite of N=30 with 6 controls and 4 evidence-only reds
reports as "24→30 incl. 4 evidence-tag fixes, 6 stable, 0 regressed" — still a pass,
but a truthful one. If some P cases were green at the harmed tool, they are controls
counted toward N at every revision; they must never be narrated as repair evidence.

## Limits
Only the two landed case seats' `before` labels were re-derived (26 scans); S/W/H
seats and `expected.json` do not exist yet — F1/F2/F3 critiques are of the counter +
contract, not of unwritten cases. I did not audit the tool diff itself or any S/W/H
fixture. `before` persistence in `expected.json` is L1's undecided schema choice.

## Installs
none.
