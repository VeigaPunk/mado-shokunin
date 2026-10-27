# C2 novelty audit

## Computation

Compared `corpus/knowledge/hyprland-bind-key-match-r50.md` (entry) against `.ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md` using lowercase ASCII alphanumeric word tokens (`[a-z0-9]+`) and sets of consecutive 8-token tuples. Denominator is the entry's unique shingles; numerator is entry shingles also present in the candidate.

```text
r50_shingles 4864 intersection 3939 coverage_percent 80.98273026315789
symmetric_jaccard_percent 73.62616822429906
```

Thus the reported 81.7% is not exactly reproducible with this explicit tokenization/set-coverage convention; it is close (80.98%). Different tokenization/normalization and denominator conventions can account for differences. The high overlap is reproduced in substance.

## Clause (c) audit

A ~50% entry-shingle overlap passes a `<=30%` maximum only if the compared file overlap is computed in the opposite direction or has a substantially larger denominator; under the stated maximum entry-shingle coverage, 50% fails. But paraphrase/synonym replacement can drive lexical 8-gram overlap below threshold while conveying the same facts. The threshold alone is not a semantic novelty test. Recommendation: retain the quantitative clause as a lexical screen and add a semantic-ground check in review; do not claim it proves new ground. No defensible numeric threshold can prevent paraphrase evasion. If forced to choose, lower threshold is not a solution to synonym substitution.

## Baseline omissions / pinning

The sentence names all `corpus/knowledge/*.md` at BASE and candidate files recursively, but not seat reports under `.ufo/waves/round-*/w1|w2/**`; these can contain candidate text and can evade the specified corpus. Whether they matter depends on whether they contain candidate-bearing content, not merely reports. The broad w1/w2 trees contain many reports and are not equivalent to the candidate directory; excluding them is a real gap if such text is admitted as prior candidate material. Baseline is pinned to the explicit round base hash, so later additions to corpus do not change the comparison set. However, an older entry quoted from its own `rev...` tree can be missed if it is not present in the base corpus or candidate path; corpus growth alone does not establish that every historical version/entry is covered.

## Recommendation

Change clause (c) to include all prior candidate-bearing artifacts, not just `candidate/`, while keeping the corpus comparison pinned at BASE. Suggested exact sentence:

> (c) the entry's maximum word-8-gram shingle overlap against every `corpus/knowledge/*.md` at base `6ca8c559a4a3d6d361101592116eea2bc7452437` and every prior-round candidate-bearing file under `.ufo/waves/round-*/` (recursive, excluding reports that do not contain candidate text) is ≤30% per file;

This still cannot establish semantic novelty; state that the counter is lexical screening and require human novelty/ground review. Treat exact historical `rev...` artifacts as baseline candidates where they are in scope rather than relying on corpus growth.
