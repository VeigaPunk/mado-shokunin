# RevC1Counter — report (w1, round 43, 2026-10-26)

Seat: attacked PRED-C1-r42's frozen counter `quality/counters/c1-r42-geometry.py` (sha256 `ed78d693…`, byte-identical to the 809dc2c freeze blob and the a35cfdf base blob; BASE 62dd798 lacks the tool). No counter or tracked file was edited; scratch `/fast/scratch/hyaku/mado-r43/RevC1Counter/` was created, used, and deleted. Tools installed: none.

## Verdict

The counter is sound at its core and honest about most of it: gate integrity PASS, model≡reference on 392 fresh cases, no vacuity for the classic cheat shapes. Four MEDIUM findings and eight LOW/INFO ones — none flips the verdict for a reference-class tool, three can flip or crash it for other legitimate tool shapes.

## Findings (full detail, reproductions, and evidence in `.ufo/waves/round-43/w1/RevC1Counter/findings.md`; all quotes machine-verified, `verify-quotes.txt`: 27/27 OK)

- **F1 MEDIUM** — docstring "not UTF-8 JSON … is bad_json" (:21-22) vs `json.loads` at :268 which accepts NaN/Infinity; fixture `nan0` pins the lenient reading, so a tool implementing the docstring strictly fails 36/37. Doc and fixture are not the same sentence.
- **F2 MEDIUM** — the 3-timeout breaker (:84, :207-212, :432-444) is global, order-dependent and load-sensitive: demonstrated with a clause-perfect slow tool (a/b/b2/b3/g all pass, selftest 73/73, teeth 6/6) scoring `fixtures=0/37 TARGET_MISSED` in 92 s; `many0` alone is 6.0 s = 20 % of the 30 s cap for the frozen reference, so ~5× host contention (77-seat wave) can trip a correct tool. Selftest/mutant timeouts share the fixture budget.
- **F2b MEDIUM-LOW** — clause b2 is a nonce coin-flip at the boundary: reference has 35 sites (4 summary); P(b2 pass) = 0.47/0.55/0.87 for a tool killing 26/27/30 of 35 sites — fresh-nonce runs can disagree.
- **F3 MEDIUM** — a working tool whose source `ast.parse` rejects (UTF-8 BOM) crashes the counter: clause b passes (selftest 73/73), then uncaught `SyntaxError` at :847, traceback, no final P line (evidence/e7bom.log).
- **F4 LOW-MEDIUM** — fixture vacuity: no fixture ever passes ≥4 `--rules` files (gen caps at 3, :367; multi0/order0 use 3); a tool truncating to 3 files scores 37/37, while the reference demonstrably handles 4-5 (tier2 files4/files5).
- **F5 LOW** — unpinned orderings/domains: bad_json-clients × unreadable-rules; usage × unreadable; stdin never exceeds 1048577 bytes (cap pinned only at the exact boundary).
- **F6 LOW** — clause g diverges from its docstring both ways: stricter (bare names of exec/eval/vars/compile rejected uncalled; zero-import tools rejected; os.spawn* rejected though unlisted), looser (`sys.argv[0]` reachable via `a = sys.argv; a[0]`).
- **F7 LOW** — dead guard: `not (mods & STDLIB_DENY)` (:834) implied by the allow-list (intersection empty).
- **F8 LOW** — many0's seed ignores REV (:764 `rng_for("many", …)`), contradicting the docstring's `sha256(REV:NONCE:tag:i)` (:10); no scoring consequence.
- **F9 LOW** — selftest phase runs without RLIMIT_NPROC (:883-886 vs :435) and clause g does not ban `os.fork`; docstring scopes nproc to fixture runs accurately.
- **F10 LOW** — `run_piped`'s comment (:188-190) describes a nonexistent "stub"; file-mode stdin blocks (parent holds the write end) until timeout — breaker-coupling path for buggy tools.
- **F11 INFO** — the alphabet admits catastrophic regexes (`(a|a)*b` hung my first sample run); the counter can never cover that domain without hanging on its own model — sharpens the declared re≠RE2 residual with the complexity dimension.
- **F12 INFO/PASS** — freeze integrity verified; reference re-run at base: `fixtures=37/37 … verdict=TARGET_MET`, exit 0, 10.5 s (evidence/e5ref.log), consistent with `receipts/ctl-c1.txt` :50 "reference met: 1".

## Negative results (attacked, not found)

Not vacuous for first-file-only / stdin-only / first-client-only tools (multi0/order0 pin cross-file last-wins; gen alternates stdin/file by parity); no pool-overfit path (regex0/ctlclass0/unicode0/size0/space0/float0 use non-pool values); fixed-fixture memorization unprofitable (opaque nonce-keyed dir names, nonce never given to the tool); sandbox exposes neither counter nor lane (bind set read, nothing in the lane written); judge is byte-exact with the docstring's stderr rule; teeth counting matches its docstring; fixture names unique per run.

## Residual risk / verification gaps

A TARGET_MET is strong evidence; a TARGET_MISSED is not proof of incorrectness without reading the per-fixture `ok=` lines (F2/F2b make verdicts load- and nonce-dependent at the boundary). Builder-facing traps: implement the fixtures' pinned behavior (lenient JSON, unbounded files, cap-checked stdin), not the most literal docstring reading. Not in scope: controls tally, C2, RE2 fidelity beyond the alphabet, compositor behavior.

Evidence: `.ufo/waves/round-43/w1/RevC1Counter/findings.md`, `evidence/` (tier1.log 314 cases, tier2.log 78 sandboxed cases, probes.log, e5ref.log, e6breaker.log, e7bom.log, harness/probes/tier2 scripts), `verify-quotes.txt` (27/27 OK).
