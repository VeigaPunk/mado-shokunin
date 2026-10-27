# Round 51 freeze registration

Lane base: `6ca8c559a4a3d6d361101592116eea2bc7452437`; claims freeze `d274028163033244bd78938ad152dc250cc50480`; w1 dispatch `3ac316426497e8649bffedc88d28241d9bc71c52`.

Claims and targets remain exactly as declared in `claims.md`; no v2 predicate amendment is made after w1 scoring. The w1 attacks are frozen residual findings, not changes to the scored rules.

## C1 — operability: tool-ledger capability

Predicate: PRED-C1-r51, verbatim from `claims.md`: run `python3 -I quality/counters/c1-r51-ledger.py --repo <lane> --rev <rev> --work <scratch>`; it exits 0 with final line `C1_R51: population=<P> ledger_rows=<P> uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=<rev>` where `P` is the number of files under `tools/`, `quality/*.py` and `quality/counters/*.py` at `<rev>`, each such file appears exactly once in `quality/tool-ledger.md` with a non-empty description and an accountability pointer naming an existing repo file that contains the file's basename; at the round base `6ca8c559a4a3d6d361101592116eea2bc7452437` the same command prints `verdict=TARGET_MISSED ledger=absent` and exits 1.

Frozen implementation: `quality/counters/c1-r51-ledger.py` + `quality/check-tool-ledger.py`; base probe `w1/ExecLedgerCounter/receipts/base-and-setup.txt` reports `ledger=absent population=79`, exit 1. Checker selftest `w1/ExecLedgerGate/selftest.txt` = 50/50. Counter and checker residuals: w1 `RevLedgerPred/attacks.md` identifies comment-only pointer and repeated generic descriptions as literal passes; `CritLedgerForgery` supplies a ledger-wide comment-pointer forgery; `MutLedgerGate` and `MutLedgerCounter` enumerate remaining population/parse mutants. These remain explicit limitations under the frozen predicate.

## C2 — coverage: sourced dispatcher-dispatch entry

Predicate: PRED-C2-r51, verbatim from `claims.md`: `TMPDIR=<scratch> python3 -I quality/counters/c2-r51-dispatch-entry.py --repo <lane> --rev <rev>` exits 0 with final line `C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=<rev>` iff at `<rev>`: (a) `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` exists and is indexed in `corpus/README.md`; (b) its `source:` block cites ≥2 rows S364–S379 of `corpus/SOURCES.md` with status `mined`, opened 2026-10-27, each bound to a pin under `.ufo/waves/round-51/fetch/` named in the entry's pin manifest whose cited line contains the row's quote verbatim (≤25 words); (c) the entry's maximum word-8-gram shingle overlap against every `corpus/knowledge/*.md` at base `6ca8c559a4a3d6d361101592116eea2bc7452437` and every file under `.ufo/waves/round-*/candidate/` (recursive) is ≤30% per file; (d) ≥3 distinct `held:` citations each name `corpus/knowledge/<file>:<line>` at base and the named line contains every pinned key token of that citation; at base the entry is absent and the command prints `admitted=0/1 verdict=TARGET_MISSED` exit 1.

Frozen implementation: `quality/counters/c2-r51-dispatch-entry.py`; base receipt `w1/ExecCounterC2/receipt-base.txt` gives clauses_met=0, TARGET_MISSED, exit 1. Draft satisfiable fixture receipt gives clauses_met=4/TARGET_MET, exit 0; six declared mutants missed (receipt `w1/ExecCounterC2/receipt-mutants.txt`). Entry draft fit `w1/ScrDispatchEntry/counter-fit-receipt.txt` gives clauses_met=4/TARGET_MET and max overlap 0.1% against 66 knowledge files + 3 candidates.

Residuals from w1 attack: `CritHeldFacts/held-attacks.md` shows generic token `[the]` can satisfy clause (d); `RevNovelty/novelty-audit.md` says lexical overlap is not semantic novelty and omits candidate-bearing seat reports; `CritC2Stub/stub-c2.md` shows a low-overlap generic stub does not itself establish coverage. The round preserves the declared predicate and reports these limits.

## Pre-data controls

Control specs and receipts are in `w1/ExecControlsC1/` and `w1/ExecControlsC2/`; the base receipts above are the red-before checks. C1 base path is independently confirmed absent by `w1/RevC1Base/base-c1-receipt.txt` (counter itself was not available to that reviewer when it ran); C2 base path absent is confirmed in `w1/CritBaseC2/base-c2-receipt.txt` (its counter reproduction likewise predated the counter draft). The executable C2 counter later reproduced its base MISS in `receipt-base.txt`.

Frozen residuals are recorded as such; no rule was changed after data or seat scoring. Data commit occurs after this registration.

## W2 integration corrections (predicates unchanged)

- **C2 held-token attack correction:** W1 `CritHeldFacts` asserted that `tokens=[the]` passes clause (d). W2 `CritC2HeldTokens` ran that exact fixture and found `tokens=` is not parsed (`no_tokens` for all three citations); a parser-compatible `keys=the` fixture also misses because the cited base line 2 lacks `the`. Therefore the advertised generic-token bypass is **not reproduced**; do not report it as a demonstrated C2 falsification. Clause (d)'s choice of tokens remains a future design question, not an observed bypass. Evidence: `.ufo/waves/round-51/w2/CritC2HeldTokens/held-token-attack.md`.
- **C2 content correction:** W2 `RevC2EntryTruth` found source-truth overclaims in the original entry; append-only errata were added at `b742d54ce12423795b3fcdd4e3a46d8f3e711b3b`, and the unchanged predicate still measured `TARGET_MET` at corrected revision and final integration. Evidence: `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md#Errata`, `.ufo/waves/round-51/receipts/c2-after-errata.txt`, and `receipts/c2-at-integration.txt`.
- **C1 ledger residual:** W2 confirmed the frozen literal predicate allows a ledger-wide self-pointer and repeated generic descriptions; these do not falsify its exact non-empty-description/basename-presence sentence, but bound what the capability proves. Evidence: `.ufo/waves/round-51/w2/CritTrendEvidence.md`, `CritC1GenericDesc/generic-descriptions.md`.
