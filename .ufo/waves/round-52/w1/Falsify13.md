# Falsify13 — C2 proposition/source entailment

## Deliverables
- `.ufo/waves/round-52/w1/Falsify13.md` — this report; no fixture or source files created.
## Attack
**Attacked clause:** C2 coverage predicate that each material factual proposition maps to an opened S-row, pin/revision and exact located quote (≤25 words), with a support rationale; specifically, whether exact quote-to-pin binding establishes proposition support. This does not contest the frozen claim's explicit limitation that the counter is not automated semantic-entailment proof.

**Concrete existing example:** Round-51 entry `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`, source line 15, binds S365 to the quote `Bad dispatcher` at `Hyprland-legacy-DispatcherTranslator.cpp:32`; it describes that row as teaching “how CDispatcherTranslator::run resolves a dispatcher name to its implementation and how implementations parse arguments.” The entry's body further frames the quoted error as evidence of the inner refusal (line 102). The located source bytes at the frozen pin show line 32 is only the unknown-name error branch:

```
30 SDispatchResult CDispatcherTranslator::run(const std::string& d, const std::string& w) {
31     if (!m_dispMap.contains(d))
32         return {.success = false, .error = "Bad dispatcher"};
34     return m_dispMap.at(d)(w);
```

Thus the exact quote and line prove that an unknown key gets this error, but do not themselves entail the positive lookup-and-call behavior or the plural claim about implementations parsing arguments. Those require the additional source lines / other implementation sites (the entry's body does cite line 34, but its registry row's quote does not). This is a concrete limitation of the proposition→single-quote entailment representation, not evidence that the broader entry is false. An exact quote can be mechanically bound and still be a weak or incomplete warrant for the associated proposition; an outside truth/support review remains necessary, exactly as the frozen C2 text acknowledges.

## Reproduction and result
- Setup: read-only lane at base `85d57a818c3707397e21c840b6498b105ba798aa`; local pin `.ufo/waves/round-51/fetch/Hyprland-legacy-DispatcherTranslator.cpp`; entry and counter are at that same frozen lane revision. No fixture mutation or runtime/source producer execution.
- Inspected counter `quality/counters/c2-r51-dispatch-entry.py`: `bind_row` (lines 329–375) validates that a quoted span appears in the pin's cited line span; quote-word count is bounded by `MAX_QUOTE_WORDS` (line 70). This check does not evaluate whether the quote supports the row's factual wording.
- Inspected S365 in `corpus/SOURCES.md` (row 315 in the file) and the entry's source line 15. The quote is exact and within the frozen maximum; its line is line 32 of the pin. Source location: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp`, access date recorded in registry: 2026-10-27. Located quote: `return {.success = false, .error = "Bad dispatcher"};` (source line 32).
- Actual result: **reproduced, narrowly** — this is a real structurally valid source binding whose quote alone is insufficient for the broader source description. It does not falsify C2's complete acceptance condition, which expressly requires written support rationales and an outside reviewer to judge truth; the target round-52 entry/counter is absent at the frozen base, so I did not score a round-52 artifact.
- Scratch guard: checked `/fast` before work; 627,602,788 KiB available (26% used). No scratch files were needed. No tools installed.

## Residual risk / limits
This attack demonstrates why structural quote binding must not be reported as semantic entailment, but no R52 deliverable was present to test whether its rationale or independent source review catches this pattern. I made no claim about source truth beyond the displayed pinned lines; no web fetch was performed. No counter or repository files were changed.

Report: `.ufo/waves/round-52/w1/Falsify13.md`
