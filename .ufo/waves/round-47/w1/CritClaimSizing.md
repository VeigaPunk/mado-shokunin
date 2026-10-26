# CritClaimSizing — round-47 w1: cheap-pass survey of the C1/C2 predicates

Seat: CritClaimSizing (leaf, no subagent dispatch). Role: attack the proposed C1/C2
predicate designs (claims.md:10-17, w1-spec.json:3) for cheap passes **before** the L1
freezes them in registration.md.

Status: analysis complete. Full findings: `.ufo/waves/round-47/w1/CritClaimSizing/findings.md`.

Headline (priority order):

1. **Exfiltration is open (C1).** The frozen judge compares stdout+exit on a corpus where
   fixtures carry `expect`, and the oracle runs side-by-side in the same sandbox. A tool can
   read the manifest, the oracle's stdout/cache, or sibling `/proc` fds and echo `expect`.
   No current clause stops this. Propose: run tool before oracle, hide repo/manifest/oracle,
   and openat-audit reads to "what the pinned script itself opens".
2. **Vendoring decision must be made (C1).** An embedded copy of the pinned script interpreted
   by a tiny pure-Python POSIX-sh interpreter satisfies every letter of the contract (stdlib
   only, no process, no socket) and is byte-identical by construction. No clause stops it.
   Decide before freeze: either require independent authorship (no >40-char contiguous runs of
   the pin) or declare it a permitted residual.
3. **Nonce freshness is unstated (C1).** "Nonce-generated cases" is not enough: a seeded,
   deterministic generator is precomputable. Require a fresh CSPRNG seed at judge time and
   parameter ranges too wide to enumerate; ban embedded case→output/hash→output maps.
4. **No behavior-matrix mandate (C1).** A dominant-path approximation passes every fixture the
   corpus doesn't probe. Require the suite to exercise every output-changing branch of the
   pinned script (list-file order, data-dir precedence, Hidden/NoDisplay/show-in, Type, TryExec,
   Actions, X-TerminalArg*, %-arg composition, print modes, --dir/--title/--app-id/--hold, argv).
5. **Explain is self-verifiable (C1).** The "why" has no oracle. Require: explain matches
   print's selection on the same env; `explain --observed <capture>` returns AGREE on every
   fixture/nonce; trace playback (cited list-file:line exists and contains the entry).
6. **C2 observation must be reproduced (C2).** Citing the L1-provided host fact is not a live
   observation by the entry's author. Require this-round reproduction: command, env, receipt
   sha256, quoted output; counter replays and compares bytes. Scope the closure to selection-time
   (print mode), since launch is banned.
7. **C2 chain must be anchored + cross-checked (C2).** Bind each asserted behavior to a source
   that actually contains it, and cross-check chain order against C1's fixture oracle. Hold-ground
   list (r17/r23/omarchy) needs a reject mechanic, not just prose.

Residuals to declare: sandbox-detection (carry-over from round-46); new — the judge sees only
I/O, never method, so clauses 1-5 are load-bearing, not optional; "no process/no socket" is an
anti-wrapper clause, not a pro-fidelity clause.

No tools installed; no scratch used; no host process run.
