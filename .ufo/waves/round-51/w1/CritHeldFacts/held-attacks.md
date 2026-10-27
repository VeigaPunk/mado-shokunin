# C2 clause (d): vacuous-held-token attack

## Frozen wording
At claims.md lines 61–63, clause (d) requires “≥3 distinct `held:` citations” naming base knowledge lines, with each named line containing “every pinned key token of that citation.” It does not prescribe token selection, minimum token count, token specificity, uniqueness, or a role for an independent selector. Thus the counter can mechanically accept a vacuous binding while every path and line is genuine.

## Exact vicious fixture
Target C2 entry's `held:` block (all three are distinct held lines at base):

```
held: corpus/knowledge/hyprland-bind-key-match-r50.md:1 tokens=[the]
held: corpus/knowledge/hyprland-bind-key-match-r50.md:2 tokens=[the]
held: corpus/knowledge/hyprland-bind-key-match-r50.md:3 tokens=[the]
```

Token sets are respectively `{the}`, `{the}`, `{the}`. The cited lines exist at base and each contains the lowercase token `the` (line 1 title; lines 2–3 prose). Under the frozen wording the clause-(d) counter verdict is PASS: three distinct citations, each line contains every pinned token. This is vacuous: the token is ubiquitous and establishes no relationship to dispatcher parsing or execution. Even enforcing three distinct tokens per citation would not solve it if an author picks generic words; conversely, permitting the same token across distinct citations is plainly allowed by the sentence.

The actual round-50 entry also exposes an identity issue: its `ground:` at line 19 names facts and earlier knowledge/lesson lines, but round-51 wording only checks token containment in a cited line. It does not require the citation's tokens to be the facts asserted in the new entry, nor require ground to distinguish reused facts from novelty.

## Is three the right floor?
Three is an arbitrary quantity, not an evidentiary threshold. Three citations can be three vacuous or redundant lines (fixture above); two precise, independent citations could be materially stronger. If the goal is a minimum breadth signal, keep >=3 only as a declared breadth convention, not as a quality guarantee. Prefer each held fact/claim to have an explicit, non-generic token set grounded in the proposition being reused, with citations distinct by fact rather than merely by line.

## Does (d) distinguish reuse from novelty?
No. It tests a one-way lexical containment predicate. It neither maps the entry's claims to held facts nor measures whether those facts are reused, extended, or absent. It can be passed by irrelevant held lines and can miss reuse expressed with synonyms. Clause (c) independently gates document-level shingle overlap, but that is not a substitute for causal/factual distinction; the frozen (d) wording itself makes no novelty judgment.

## Recommendation
CHANGE the counter contract in a future freeze, not the current frozen sentence: pin token sets in an independently authored, committed fixture/control (or derive them from explicit held-fact assertions); reject stopwords/generic tokens and require a meaningful multi-token phrase or exact fact-bearing anchor; require the cited span to support the mapped held assertion, not mere token presence. Keep >=3 only if the intended floor is three distinct held propositions, and count propositions rather than citations. For this round, preserve the frozen wording and disclose the false-positive as a limitation; do not silently reinterpret it.
