# mado round 69 — lesson

author: mado L1 (the scored instruments are the L1's own; the one w1 wave's seats attack them).
date: 2026-11-03/04 (America/Sao_Paulo)
base: `04093b83f73a841117d3b31dbb2a6063f4f2a454`
frozen declaration: `.ufo/waves/round-69/claims-declaration-r69.md`, `789a87f1a667b43dd759222a2f048bf8f75b43ce`
control set: `.ufo/waves/round-69/controls/c2-controls-r69.json`, sha256
`975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9` (11 cases)
pre-freeze baseline: `.ufo/waves/round-69/control-baseline-r69.txt`
measured content: `5fc29ae72e66b9347d576c796ee656aea2fdd04c`

## Outcome and boundaries

Two bounded claims, both frozen before any candidate data.

- **C1 calibration — the hardened harness kills paired (decision + oracle) forgeries.** At the
  measured revision the frozen counter `quality/counters/c1-r69-paired-recipes.py` extracts
  `quality/counters/c1-r69-landing-controls.py`, runs its `--selftest`, applies the three frozen
  recipes R1/R2/R3 exactly once each, and requires each mutant's own `--selftest` to exit nonzero;
  the same recipes are applied at the base revision to the round-68 harness, which must survive
  all three. Target `selftest=0 killed=3/3 applied=3/3 base=0/3`, bounded `10 × killed / 3`.
  Measured: `selftest=0 killed=3/3 applied=3/3 base=0/3` rc 0 (`measurement-c1-r69.txt`). At the
  base the harness is absent (`selftest=absent killed=0/3 applied=0/3 base=0/3`, rc 1); the
  do-nothing control — the r68 harness under the same recipes — survives all three (52/52 green).
- **C2 operability — the guard census requires key position and dominance.** At the measured
  revision `quality/counters/c2-r69-guard-dominance.py` reads the 20 tracked `quality/check-*.py`
  files, classifies 13 readers and 13 guarded, and scores the frozen 11-case set; the base leg
  scores the same cases with the round-68 classifier, which must miss the target. Target
  `population=20 readers=13 guarded=13 unguarded=0 controls=11/11 base_controls=7/11`, bounded
  `10 × guarded / readers`. Measured `… controls=11/11 base_controls=7/11 verdict=TARGET_MET` rc 0
  (`measurement-c2-r69.txt`). Before: the counter is absent at the base revision and the held
  round-68 rule scores `7/11` on the same set (`control-baseline-r69.txt`).

**Not claimed.** Universal fault coverage; that three recipes are the only forgeries; that an
outside attacker cannot reforge the printed line; runtime behaviour of the extracted instruments;
that the dominance rule is sound for arbitrary Python (one module, one hop, no alias/attribute/
container flow, no path-sensitivity beyond a literal-false branch); that a guarded environment
authenticates objects or protects an already-rewritten repository; state truth of any
`PROVINCE.md` cell; any `[x]`, promotion or axis retirement. Both claims are finite-control claims
and no wider guarantee is read out of a green count. Desktop, compositor, session and service
surfaces were not probed at all this round.

## Mistakes

| mistake | class | evidence | captured-by | fix and failure it can now show |
|---|---|---|---|---|
| M69-1: the round-68 reviewer's recipe **L** (`mz_killed = mz_rc != 0` → `mz_killed = mz_rc != 0 or mz_rc is None`) was recorded as a credit widening, but it is an **equivalent mutant**. | misclassification | `corpus/lessons/round-68.md` (RevC1 survivor L) vs `quality/counters/c1-r68-landing-controls.py:435,439` — the text sits inside `try:` after `mz_rc = r.returncode`, so `mz_rc` is an int there and the disjunct can never be the reason for a kill; `.ufo/waves/round-69/control-baseline-r69.txt` § L probe: the mutant keeps a green `59/59` selftest. | `none` as an enforced rule — no QUALITY criterion required a frozen recipe to change a printed observable before it was counted in the denominator. | The round's frozen set excludes recipe L and uses R1/R2/R3, each of which changes a scripted case's printed line (`measurement-c1-r69.txt`: three mutants with three failing assertion lines); the baseline receipt keeps the equivalence probe as the red state. A recipe whose mutant prints an identical contract line is now refusable before freeze (QUALITY 111(a)). |
| M69-2: the round-68 guard classifier accepted a key's **string in value position** — `{"LABEL": "GIT_NO_REPLACE_OBJECTS"}` counted as a guard while constructing none. | over-inclusion | `.ufo/waves/round-69/control-baseline-r69.txt` § C2: the round-68 classifier scores `controls=7/11`, accepting `value-position-only`, `dead-branch-only`, `uncalled-helper` and `overwritten-env`. | `none` at round 68 — the claim scored a population count, never a control set that pinned the construction shape. | The round-69 rule counts the key only in key position and requires the guarded environment to reach a git launch (three declared flows); the frozen 11-case set scores `11/11` and the four rejected shapes are `(reader, no guard)` (QUALITY 111(b)). |
| M69-3: the standing landing instrument's default `--citecheck-paths` points at `.ufo/waves/round-N/receipts`, which this round does not create, so the first harm-watch run exited 2 (`citecheck path missing`) before any leg ran. | setup-default | `.ufo/waves/round-69/harm-watch-r69.txt` (first run) vs the second run with explicit paths (`MADO_LANDING_COUNTERS: RED (… ledger=1 …)`, which is the real ledger finding). | `none` — the instrument documents the flag but has no preflight that names the default when it is absent. | The round passes explicit receipt paths in every invocation; the misread is kept in the receipt so a reader can see the two runs differ only by argv. A red leg must be a red leg of a leg, not of a setup refusal. |

A fix counts only on its named red/green evidence. M69-1 and M69-2 have both states in
`control-baseline-r69.txt`; M69-3's two runs are in `harm-watch-r69.txt` and
`measurement-*.txt` invocations.

## Gate

Admitted: **S438**, scoped to the lane's guard grammar — the documented identity of the
`--no-replace-objects` flag and the `GIT_NO_REPLACE_OBJECTS` environment.

- Canonical URL: `https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc`
- Access date: 2026-11-03; fetched three times, byte-identical (`sha256`
  `050c5330f1a231be22bee3db27c7ef90d8ba22bb7bd6c72c8bab462f6f0a1f79`, 47005 bytes, 1212 lines).
- Located quote, 14 words, git.adoc:180-181:
  "This is equivalent to exporting the `GIT_NO_REPLACE_OBJECTS` environment variable with any
  value."
- Second located quote, 17 words, git.adoc:928-929:
  "Setting and exporting this environment variable tells Git to ignore replacement refs and do
  not replace Git objects."
- Why it grounds the claim: the dominance rule is not a lane convention about Python — it is the
  documentary statement that what acts on a git child is the *exported environment*, which a
  constructed-but-dropped mapping is not.

Rejected: `https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc` as a
**new** row for this round. Reason: duplicate scope — the replacement rule is held ground in
S436 with its own tag-pinned quotes, and this round cites it without re-opening it
(`git ls-tree` check: S436 is the existing row for that URL). Flip condition: a later round that
must re-quote `git-replace.adoc` bytes from a different tag (for example when the host git leaves
2.56.0) re-opens it as a superseding row rather than a duplicate.

Registry cell changes (old → new, logged per `CORPUS.md` rule 2):

- S436 `used-by`: `corpus/lessons/round-67.md, corpus/knowledge/replace-ref-citation-boundaries-r67.md,
  corpus/knowledge/gate-git-read-guards-r68.md` → the same list plus
  `corpus/knowledge/gate-guard-dominance-r69.md` (the new entry re-quotes the replacement rule).
- S437 `used-by`: `corpus/lessons/round-68.md,corpus/knowledge/gate-git-read-guards-r68.md` → the same
  list plus `corpus/knowledge/gate-guard-dominance-r69.md` (the new entry cites the object-read verb
  family). No `status` and no `recheck` cell changed; S438 is a new append.

Assimilation: none this round — no `merge/mado/` theme was taken. `considerthese/2026-10-28.md`
proposal 4 (a live-tool table) is named in the round report as an unmined proposal, not adopted;
it adds no claim slot and no registry row.
