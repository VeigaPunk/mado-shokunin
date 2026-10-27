# R54W2Seat17 — C1 P20 semantic entailment

Axes: C1 operability and truth/integrity of the certified source claim.

## Finding: P20's point anchor cannot support its proposition's temporal claim

The frozen contract requires P20's anchor to be exactly `:1576` (claims-frozen.md:25-28) and registration likewise fixes `:1576` (registration.md:25-34). At that point the pin text is only `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` (registration.md:29); the quote itself says nothing about whether the call occurs after a key/button delivery branch. Yet the proposition says “After the key/button delivery branch, `Actions::pass` clears modifier state,” and its Support asserts “the clear call follows the delivery block” (corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md:18). A one-line anchor cannot establish that ordering unless the verifier also establishes the branch and its end precedes line 1576. The frozen P20 side-claim only says the quote is at exactly line 1576 (claims-frozen.md:25-28); unlike P21 and P22, it supplies no surrounding-flow bounds (registration.md:32-34). Quote occurrence, pin hash, and exact line therefore do not entail the proposition's semantic predicate.

The strongest counterexample is a changed pin/source in which line 1576 remains byte-identical but the branch is removed, moved after the clear call, or otherwise no longer precedes it; a checker satisfying the enumerated P20 quote/anchor/hash tests could report P20 supported although the proposition is false. As frozen, the committed pin hash prevents changing this exact source artifact unnoticed; that protects artifact identity, not the entailment represented by the claim. This is a semantic gap, not evidence that the pinned source actually contradicts P20.

## Evidence and execution

Frozen specification: claims-frozen.md:20-30 (P20 anchor side-claim), registration.md:25-34 (P20 quote and side-claim); claim under test: `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md:18`. Relevant w1 report: `.ufo/waves/round-54/w1/R54Seat17.md:48-79` documented ambiguity in quote normalization, and :157-166 identified the absence of a landed counter at its attack time. P20 temporal entailment is a distinct issue: whitespace normalization or exact quote matching cannot establish preceding control flow.

Exact availability check: `glob /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters` — output listed counters only through r51, no `c1-r54-errata-truth.py`; therefore frozen command `python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev <rev>`: NOT RUN (counter absent). No counter output or exit status exists to report. The designated base was `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`; current `git rev-parse HEAD` returned `350d30e4ec5531f65ce99a57efeb8216f38e678a`, so no claim is made that the inspected live tree is the base. No pin re-execution or source/producer execution performed.

Smallest safe correction: for any future versioned registration, make P20's semantic check bind its exact line to surrounding pinned control flow (e.g. verify the relevant branch's closing boundary is before line 1576 and the clear call follows it), in addition to quote/anchor/hash; otherwise weaken the proposition to the directly supported statement that the pinned line contains the clear-modifier call. Do not alter frozen predicate or registration after scoring.

## Bounds

No lane/source/sibling edits, no git/jj mutation, no installs. Scratch `/fast/scratch/hyaku/mado-r54/R54W2Seat17` was created; removal command `rmdir /fast/scratch/hyaku/mado-r54/R54W2Seat17` was issued before writing this report. Relative report path: `.ufo/waves/round-54/w2/R54W2Seat17.md`.