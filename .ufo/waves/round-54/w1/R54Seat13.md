# R54Seat13 — uwsm-app environment frontier reconnaissance

## Axes

Coverage; operability. This is static documentary reconnaissance only; no host/domain reads or runtime behavior is asserted.

## Finding

The frozen target is genuinely new coverage-map territory: `claims-frozen.md:46-75` calls out the `uwsm-app` environment and explicitly says the frontier has been open since round 47. The existing corpus index (`corpus/README.md:42-45, 75-82`) routes idle-lock, terminal, Walker/theme, and Hyprland source topics, but contains no uwsm-app-environment entry. Existing `terminal-route-r17.md:103-105` explicitly leaves how the wrapper alters environment unknown; existing idle/launcher notes cite it as a launch command, not as sourced environment semantics. Therefore the new entry can close a documentary route only, not a runtime/environment-observation claim.

Frozen scope is specifically the pinned 0.27.1 sources and three registered claims: environment export after preparation (S375), app-daemon pipe forwarding (S376), and generated unit naming (S377), plus at least two host join citations (`registration.md:55-76`). Distinct from nearby existing coverage: terminal selection is already covered by the round-47 resolver (`README.md:75`), while this assignment concerns the wrapper's environment/launch contract, not terminal choice. No evidence here extends to observed environment contents, propagation into any actual app, or host runtime semantics.

## Independent distinct failure/input check

I selected the frozen **wrong-commit** control as a distinct failure input: `registration.md:78-90`, C2-CTL-5 mutates a source URL to the v0.26.6 commit (`469a39a5…`) and requires rejection on the pinned-commit leg. This is materially different from forged quote, missing provenance/index, or absent host joins: the prose/quote may remain plausible while the source identity is wrong. The recon confirms this control is directly tied to the entry's evidence boundary: its three source rows are required to resolve to the frozen 0.27.1 tag commit `0727985c9bae655bda488f87f99ea69a6ac1c003` (`claims-frozen.md:60-65`). I did not execute a producer, counter, or fixture; this is an assignment-specific static attack/input selection, not a claimed control-run result.

## Sibling overlap / novelty

I could verify the distinct work boundary only from the frozen registration: C2 entry/source-row/counter work is the claim surface (`registration.md:55-90`); C1 errata verifier is a separate claim (`claims-frozen.md:13-44`). The existing index demonstrates adjacent coverage already present, while no uwsm entry exists in the index. I cannot determine individual sibling seat ownership from the registration excerpt available here; no seat-specific implementation result is attributed to another seat.

## Evidence and commands

Commands/tool queries used (read-only):
- Read `.ufo/waves/round-54/claims-frozen.md:46-75` and `.ufo/waves/round-54/registration.md:55-90`.
- Read `corpus/README.md:42-45,75-82`.
- Searched `corpus/knowledge/` for `uwsm-app|environment`; relevant existing notes included `terminal-route-r17.md:103-105`, `idle-lock-plane.md:110-115,266-270`, and `walker-route-r18.md:154-160`.
- Attempted reads of `corpus/coverage-map.md` and `corpus/knowledge/coverage-frontier.md`; both paths do not exist. The actual coverage map is `corpus/README.md`.

**Trailer:** report path `.ufo/waves/round-54/w1/R54Seat13.md` relative to lane root. No tools installed or updated. No scratch artifacts created; no git/jj mutation, host read, or producer execution.