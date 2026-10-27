# R54W2Seat28 — C2 host-join citation falsification

## Frozen contract and evidence boundary

Base requested: `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`. The inspected lane currently reports `git rev-parse HEAD` = `350d30e4ec5531f65ce99a57efeb8216f38e678a`; no mutation was performed. I treated the frozen claims and registration as immutable.

`.ufo/waves/round-54/claims-frozen.md:55-65` defines PRED-C2-r54: clause (c) requires at least two host-join citations among registration's frozen host set, and clause (d) requires rejecting all six frozen controls. `registration.md:71-76` specifies citation representation as `file:line`, with host set `~/.local/share/omarchy/default/hypr/autostart.conf:1` through `:6`, `~/.config/hypr/bindings.conf:2`, and `~/.local/share/omarchy/bin/omarchy-toggle-idle:9`. `registration.md:78-90` says C2-CTL-6 removes all host joins and must be rejected, while the counter contract emits the frozen line and has a selftest requirement.

My W1 report (`.ufo/waves/round-54/w1/R54Seat28.md:240-253`) attacked C1 source-truth and normalization, explicitly did not exercise C2. It supplies no prior C2 host-join result; this report is the distinct C2 host-line-number mutation test. W1 report's evidence limitation is at lines 255-264.

## Attempt and outcome

The live tree at this observation has no C2 counter at `quality/counters/c2-r54-uwsm-entry.py` (read returned not found), and no landed C2 entry in the observed `corpus/knowledge/` listing. Therefore there is no runnable pinned counter to exercise against the requested mutants. Per assignment, I did not fabricate an outcome or run a substitute implementation. C2 controls and the frozen command are **NOT RUN / absent**. This does not establish that the eventual counter fails or passes.

The requested mutation is to keep filenames unchanged while changing citation line numbers. The frozen host-membership rule, as written, recognizes literal full `file:line` citations, so changing a correct numeric suffix to a different line should cease matching that frozen host citation. It does not, however, establish whether the citation line points to a real `uwsm-app`-routed launch/join: the registration provides a finite list of accepted file:line strings, but no expected line contents or semantic join criteria. A counter that compares the whole literal citation would distinguish the altered citation from the enumerated one; a counter that checks only host filenames would not. Because the counter is absent, which matching strategy it implements is unresolved. Even exact literal matching demonstrates membership, not that source line content actually performs a join; that stronger semantic property is not specified in the frozen predicate.

No pinned command was rerun: `python3 -I quality/counters/c2-r54-uwsm-entry.py --repo . --rev <rev>` is unavailable because its counter file is absent. No fixtures, host reads, or source execution were performed.

## Result

Attack item 28 remains **unresolved empirically**: frozen controls name an exact `file:line` host set, but no available counter can show whether line-number mutations are rejected. Contract-level observation: exact citation membership is required; semantic validation of the cited source line is not stated. Confidence: high for frozen wording, none for actual counter behavior. No predicates, registration, lane/source files, or sibling files were changed.

## Trailer

- Report (relative to lane root): `.ufo/waves/round-54/w2/R54W2Seat28.md`
- Exact observed command/output/exit: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD` → `350d30e4ec5531f65ce99a57efeb8216f38e678a` (exit 0; differs from assigned base, no mutation); `mkdir -p /fast/scratch/hyaku/mado-r54/R54W2Seat28 && rmdir /fast/scratch/hyaku/mado-r54/R54W2Seat28` → `scratch-clean: exit=0` (exit 0)
- Counter command: NOT RUN — counter absent at `quality/counters/c2-r54-uwsm-entry.py` (read returned not found)
- Scratch remaining: none; mandated scratch directory was explicitly created then removed
- Tooling installed/updated: none
