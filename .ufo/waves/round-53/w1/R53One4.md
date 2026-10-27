# R53One4 — reconnaissance: claims, counter-control observability, and r52 defect evidence

## Scope and registration

- Registration: `.ufo/waves/round-53/w1/swarm-registry.json:26-30` lists `R53One4` as a registered `scout`; report directory is `.ufo/waves/round-53/w1` (`:6`).
- Frozen predicate: `.ufo/waves/round-53/claims-frozen.md:5-13` governs. C1 requires a new scratch-aware counter, explicit selftest, TARGET_MET on production ledger, TARGET_MISSED on no-work and each frozen forgery fixture, full population coverage and non-self pointers; it is structural accountability, not semantic proof. C2 requires append-only repair of P16-P18, old entry rejected/corrected accepted by frozen counter with quote/pin/proposition bindings, independent source-truth review, and no expansion credit absent opened-this-round sourced ground.
- Source-only constraints followed. Disk capacity observed via `df -P /fast/scratch/hyaku/mado-r53`: 624,239,964 1K blocks available (26% used). No scratch was created, no live probes or source fetches, no installs or executions.

## C1: structural target and falsifiable risk

Observed ledger contract at `quality/tool-ledger.md:9-28,30-119`: a row has instrument path, description, pointer; a pointer must resolve and contain the basename; existing pointer classes include registration-only pointers for superseded instruments. Thus generic basename containment alone is explicitly known inadequate. The production ledger enumerates rows including 82? [UNK: current frozen-revision population count not recomputed here].

C1's frozen requirement can be demonstrated mechanically, but acceptance evidence must keep distinct: (1) population identity/completeness and uniqueness, (2) pointer existence at the requested revision, (3) non-self pointer, (4) functional/instrument-specific description, and (5) exact expected outcome for production, no-work and every frozen forgery fixture. A generic ledger self-pointer can satisfy basename containment if the ledger itself names the basename; production-only run is insufficient. A control that differs in schema/duplication could fail for irrelevant reasons, so red controls should preserve valid row grammar and differ only in the targeted self-pointer/context property. Explicit selftest should exercise those causes, not merely return a successful status. These are acceptance risks, not observations that the new counter fails.

No current r53 counter/control was present in the round-53 directory listing at reconnaissance time; no target result is claimed.

## C2: r52 routed defects as evidence, not assumed current state

Observed in `.ufo/waves/round-52/w1/C2SourceCritic.md:31-36,38-81`: r52 review found (A) `exec` claim quote locator at `DispatcherTranslator.cpp:48-51` actually pointed to `windowFromArg`, while `exec` was at `:65-70`; (B) `sendkeystate` citation pointed to `Actions::sendKeyState` at `ConfigActions.cpp:1601-1618`, which the cited review found not called by the dispatch table, whose implementation was `DispatcherTranslator.cpp:591-627`; (C) residual “five special handlers” wording/census conflicted with its own errata's four names plus boolean. Those are specific prior provenance/consistency failures, not proof of the r53 entry's state.

The frozen r53 claims specifically target proposition repairs P16-P18. This scout did not independently open pinned source bytes or assess corrected propositions. Therefore source-truth, exact corrected locations, counter acceptance/rejection, non-overlap and coverage novelty remain unresolved. Frozen C2's counter structure should bind each proposition to its source row, immutable pin revision/path and exact located quote, reject stale r52 entry bytes, and accept only the corrected append-only entry; lexical presence alone cannot settle entailment. Independent reviewer remains mandatory.

## Findings / limits

- **Observed:** r53 frozen criteria and registration; r52 C2 source critique's three routed defects; ledger's pointer grammar and known generic/self-pointer weakness.
- **Inference:** controls that vary schema or duplicates risk confounding the target; per-criterion controls and explicit target-specific diagnostics would make the frozen claim falsifiable without widening it.
- **Unknown:** r53 C1/C2 implementation, frozen forgery fixtures and their outputs; corrected P16-P18 source truth; newly opened source row and uncovered-ground status; final committed demonstration. No claim admission or axis improvement is supported by this reconnaissance alone.

Report: `.ufo/waves/round-53/w1/R53One4.md`
