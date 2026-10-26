# RevC1Counter seat report — round 45 w1 (C1 counter review)

Status: COMPLETE 2026-10-26. Detailed review: `.ufo/waves/round-45/w1/RevC1Counter/review.md`.

Object: `quality/counters/c1-r45-monitors.py` (392 lines), sha256 `c69ddee44a9fa3c442b910541038a9440ac72c2b5f21fe4899cb8f5df9213f34`, byte-identical to the freeze blob at 22a8dedd (verified). Contract: the reference tool docstring `.ufo/waves/round-45/l1-draft/mado-monitors.py:3-90`.

## Findings (severity-ranked; details + evidence in review.md)
- **F1 MEDIUM** — clause r never observes the `--selftest` run: selftest env is `PATH=/usr/bin:/bin` (c1-r45-monitors.py:343), outside the fakebin/marker guard that only wraps the 49 fixture runs (:311, :354-356, :362). Repro `receipts/toy-selftest-gap-run.txt`: a tool running `hyprctl` in selftest executed the real host `/usr/bin/hyprctl` while the counter still printed `clause=r marker=absent`. Code matches the fixture-scoped docstring (:20), but a counter-passing tool violates the registration's plain "no hyprctl on PATH run" reading; also gives a scored-vs-production behavior fork channel. Fix requires re-registration (v2).
- **F2 LOW-MEDIUM** — no global deadline: selftest timeout (60 s) does not skip the 49 fixture runs (10 s each) → ~9.5 min for an already-decided MISS (:343, :352, :358-361, :315).
- **F3 LOW** — SETUP teeth partial: no fixture forces `too_large`, a FIFO input, or invalid UTF-8 (only truncated ASCII JSON + a directory). A tool with broken size/type handling passes clause f.
- **F4 LOW** — only `TimeoutExpired` is caught (:316); any other exception exits 1 with a traceback and no final line, colliding with the documented exit-code contract (:22-23). Scratch is still cleaned (:384-385). Not triggerable on this host.
- **F5 INFO** — a noexec `--work` mount would silently void clause r (stubs chmod 0o755, :274-278); /fast is exec-allowed here, not triggerable.
- **F6 INFO** — tool blob extracted once (:336-339), shared by all fixtures → state/order channel; docstring only promises a fresh cwd per fixture (:13), code matches.
- **F7 INFO** — clause-s parser accepts non-ASCII decimal digits via `isdigit` (:349).

## Verified-good (executed, not assumed)
- Frozen integrity: working-tree counter == freeze-commit blob (sha256 match).
- All 4 clauses audited docstring-vs-code — no divergence besides F1's scoping.
- FIXTURES = 49; the ten assigned teeth hand-re-derived against the reference docstring — all ten agree (incl. the scale-1.3 correction arithmetic: K=156, first hit 160/120=4/3 at i=4, |1.33333333−4/3|≈3.3e-9 < 1e-4).
- Name generator: seeds 0..500 — {A}{B}{C} always distinct, never prefixes, never the `none` sentinel; names(45) = DP-5, eDP-7, DVI-D-5, "Dell Inc. 6AHUHV"; substitution covers configs, dumps and expected lines.
- Scratch hygiene: everything under `--work` (all `mkdtemp` calls pass `dir=`), `finally` rmtree incl. bad-rev path; zero `c1r45-*` residue after 4 full runs; relative `--work` safe (mkdtemp absolutizes — tested, full run rc=0).
- Crash paths live: base rev → exit 1 with exactly the registration's "Before" line; bad rev → exit 2 `SETUP bad rev`; binary stdout → graceful FAIL; 64 MB output → graceful FAIL; 15 s hang → `FAIL timeout`, clean finish.
- Positive control re-run: reference installed at the freeze in a scratch clone → `fixtures=49/49 selftest=ok(33/33) readonly=ok verdict=TARGET_MET`, exit 0 — the counter is not vacuous and the R/O/S formats line up byte-exactly.
- 53/53 quote locators script-verified (`receipts/locator-check.txt`); two drifted cites were caught and fixed by it.

## Receipts
`.ufo/waves/round-45/w1/RevC1Counter/receipts/`: `base-run.txt`, `badrev-run.txt`, `ref-run.txt`, `ref-run-relwork.txt`, `toy-selftest-gap-run.txt`, `chaos-run.txt`, `chaos2-run.txt`, `locator-check.txt`.

## Tools
No tools installed or updated (none needed). No lane files touched besides this report and the seat dir; scratch `/fast/scratch/hyaku/mado-r45/RevC1Counter` deleted after receipt copy. Hyprland reads: none (the only compositor touch was the toy's in-counter `hyprctl version` probe, run without HYPRLAND_INSTANCE_SIGNATURE — no connection; only rc/byte-lengths recorded).

Report: .ufo/waves/round-45/w1/RevC1Counter.md
