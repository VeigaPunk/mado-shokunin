# C1 ledger forgery review

The frozen predicate is an existence-and-coverage test, not an accountability-quality test. It requires one row per population file, a non-empty description, and a pointer to an existing repo file containing that file's basename. It does not require pointer uniqueness, semantic relevance, evidence of tool use, or a description beyond non-emptiness. Therefore a green verdict establishes mechanical reachability only; it cannot by itself establish real accountability.

## Forgery cases

| Forgery | Exact verdict under frozen predicate | Operability harm? | Smallest safe correction |
|---|---|---|---|
| One newly created file holds every tool basename in a comment, and every row points to it | **TARGET_MET**, provided every population basename occurs there, each population entry is represented exactly once, descriptions are non-empty, and selftest passes. The predicate imposes no per-pointer relevance or uniqueness. | **Yes, substantive accountability is harmed.** A shared name dump does not identify how a tool is governed, exercised, or checked; it manufactures coverage without useful operational ownership. | Require each pointer to resolve to a meaningful, tool-specific accountability artifact/section (or an explicitly approved shared control whose section names and explains that tool), not merely contain a basename. Add a negative fixture with a basename-dump file. |
| Descriptions are generated from filenames, e.g. “Runs mado-hostguard.py” | **TARGET_MET** if the generated string is non-empty and all other conditions hold. “Auto-generated” has no special predicate status; empty-description control only catches empty values. | **Potentially yes.** A filename paraphrase can be content-free and does not explain capability or safe use. If it accurately identifies the tool's function, however, generation alone is not a defect; provenance of wording is not specified. | Require a minimally informative description checked against actual tool behavior, ideally reviewed or validated by a semantic fixture. Do not reject merely because text was generated. |
| Every row points to the ledger itself | **TARGET_MET** if the ledger contains every row's basename and remaining conditions hold. The ledger is an existing repo file; self-reference is not excluded. | **Yes.** The purported accountability evidence is only the inventory asserting itself, with no independent operational evidence. | Explicitly forbid the ledger/checker/counter themselves as accountability targets, and require an evidence-bearing target distinct from the row inventory. |

## Strongest counterexample

A single comment such as `# mado-hostguard.py mado-keysym.py ...` is enough to satisfy the stated basename-containment test for every row. This counterexample follows directly from “existing repo file that contains the file's basename”; nothing in the sentence requires a link to a relevant section or evidence. It is not a checker bug relative to the frozen sentence: rejecting it now would change the predicate after freeze. The gap is a limitation of what the predicate certifies, not a reason to call its mechanically specified verdict MISS.

The control set does not close this gap: omission, missing basename, empty description, dangling population entry, and absent base ledger are all explicitly tested, but none tests a content-free shared pointer or self-pointer. Thus all listed controls can MISS while these forgeries MET.

## Axis impact and ruling

Impacted axis: **operability** (capability acquisition). A false sense of tool accountability can leave operators without actionable ownership or evidence when a tool fails. This does not show that merely using a shared artifact is always harmful: a genuinely useful shared runbook can be valid; the harmful case is a basename-only artifact presented as accountability.

Smallest safe action for this wave: retain the frozen predicate and report its exact MET/MISS semantics; do not claim that TARGET_MET alone proves meaningful accountability. For a future predicate, add a relevance/evidence rule and a basename-dump negative control, while preserving the current coverage checks. Do not alter frozen C1 wording or its controls in response to this review.
