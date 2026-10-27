# mado round 51 — declared claims (freeze of intent, 2026-10-27, hyaku run 10)

Lane: mado-shokunin. Base (lane tip at round start): `6ca8c559a4a3d6d361101592116eea2bc7452437`
(round-50 verifier spot-check commit; round-50 data tip was `74782d39e7697608917b5e909f0e8580aaa3e15c`).
Lane axes: coverage + operability. Two claims, one per axis, causally separable.

Round-50 closure routed defects carried here: D1 (final WAVE-DONE receipt must be committed at the
integration tip), D3 (`.ufo/wakes` leftover — removed at round start), D4 (M50-9 registration
manifest self-row cleanup), D5/planned-51 items 1–3 (candidate-inclusive novelty baseline;
independent behavioral fixtures; tracked lane-level tool ledger).

## C1 — operability (capability acquisition): the tracked lane-level tool ledger

Motivation: `w2/RevLedgerR50` (round 50) found the wave-seat tool ledger incomplete — two tracked
tools (`tools/mado-hostguard.py`, `tools/mado-keysym.py`) were uncovered, and no lane-level
ledger/checker exists. `considerthese/2026-10-26.md` proposal 2 (running ledger of live-state
tools) points the same way.

Artifacts: `quality/tool-ledger.md` (one row per tracked instrument: file, one-line description,
accountability pointer), `quality/check-tool-ledger.py` (the checker, hermetic `--selftest`),
counter `quality/counters/c1-r51-ledger.py` (`PRED-C1-r51`).

Frozen predicate (single sentence — plan, counter code and receipt label carry the same words):

> PRED-C1-r51: `python3 -I quality/counters/c1-r51-ledger.py --repo <lane> --rev <rev> --work <scratch>`
> exits 0 with final line `C1_R51: population=<P> ledger_rows=<P> uncovered=0 dangling=0
> bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=<rev>` where `P` is the number of
> files under `tools/`, `quality/*.py` and `quality/counters/*.py` at `<rev>`, each such file
> appears exactly once in `quality/tool-ledger.md` with a non-empty description and an
> accountability pointer naming an existing repo file that contains the file's basename; at the
> round base `6ca8c559a4a3d6d361101592116eea2bc7452437` the same command prints
> `verdict=TARGET_MISSED ledger=absent` and exits 1.

Kill rule / do-nothing controls (must all MISS, committed as receipts before data):
(a) ledger omitting one population file → `uncovered>0` MISS; (b) ledger row whose pointer file
does not contain the basename → `bad_pointer>0` MISS; (c) empty description → `empty_desc>0` MISS;
(d) ledger listing a file not in the population → `dangling>0` MISS; (e) at base, no ledger → MISS.

## C2 — coverage (sourced): the dispatcher-dispatch entry, candidate-inclusive novelty

Motivation: the round-50 C1 novelty claim was falsified — 81.7% of the entry's shingles were
covered by the round-49 candidate, and the freshness baseline did not include
`.ufo/waves/round-*/candidate/` (planned round-51 item 1). The dispatcher surface (how a keybind's
dispatcher string is parsed and executed at 0.56.2) is named open by the arc gap ledger and is not
an admitted knowledge entry.

Artifacts: `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`, new registry rows S364+ opened
2026-10-27 with pins under `.ufo/waves/round-51/fetch/`, counter
`quality/counters/c2-r51-dispatch-entry.py` (`PRED-C2-r51`).

Frozen predicate (single sentence):

> PRED-C2-r51: `TMPDIR=<scratch> python3 -I quality/counters/c2-r51-dispatch-entry.py --repo <lane> --rev <rev>`
> exits 0 with final line `C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=<rev>`
> iff at `<rev>`: (a) `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` exists and is indexed
> in `corpus/README.md`; (b) its `source:` block cites ≥2 rows S364–S379 of `corpus/SOURCES.md`
> with status `mined`, opened 2026-10-27, each bound to a pin under `.ufo/waves/round-51/fetch/`
> named in the entry's pin manifest whose cited line contains the row's quote verbatim (≤25 words);
> (c) the entry's maximum word-8-gram shingle overlap against every `corpus/knowledge/*.md` at base
> `6ca8c559a4a3d6d361101592116eea2bc7452437` and every file under `.ufo/waves/round-*/candidate/`
> (recursive) is ≤30% per file; (d) ≥3 distinct `held:` citations each name
> `corpus/knowledge/<file>:<line>` at base and the named line contains every pinned key token of
> that citation; at base the entry is absent and the command prints `admitted=0/1 verdict=TARGET_MISSED` exit 1.

Kill rule / do-nothing controls (must all MISS, committed as receipts before data):
(a) the round-50 entry bytes (`hyprland-bind-key-match-r50.md`) at the C2 path plus two new rows →
MISS via clause (c); (b) the round-49 candidate (`round-49/candidate/hyprland-bind-key-match-r49.md`)
at the C2 path → MISS via (c); (c) held-citations pointing at lines lacking the key tokens → MISS
via (d); (d) entry citing rows with no pins → MISS via (b).

## Frontier step (§2b, inside the claim cap)

Census before: exit 0 (300 rows; W04 duplicate-URL-across-scopes warnings, pre-existing class) —
receipt `receipts/census-before.txt` (this commit). Census after at round end, exit 0 required.
Mistake mined into `corpus/lessons/round-51.md ## Mistakes`. Sourced claim: C2. Assimilation
(§10): hand-check verdicts for the mado slice of the absent-defect register (13 rows, opened
round 50) + `merge/mado` theme scan — seat work this round.
