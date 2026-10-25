# ScrLesson — round-39 lesson draft report (w1)

Seat: `ScrLesson` (leaf scribe). Deliverable:
`.ufo/waves/round-39/w1/ScrLesson/round-39.md` (8030 B) — the round-39 lesson
draft with `## Gate` (refused package entries with reasons; admitted S218/S219/
S220 rows with URL + access date 2026-10-25 + ≤25-word located quotes; spot-check
results) and `## Mistakes` (both required mistakes with red-before states), plus
the touched-row status/recheck/used-by change record.

## Evidence gathered (commands, outputs, exit codes)

- Registration read first: `.ufo/waves/round-39/registration.md` (frozen claims
  C1/C2/C3, routed defects incl. the refuted addendum-5 and the inherited
  uncommitted reports).
- C1: `receipts/c1-redbefore.txt` → `controls=19 correct=18/19 verdict=TARGET_MISSED`
  (exit 1, sole failure `c1-duprow`); `ExecC1After.md` → after-freeze/after-tip
  `controls=19 correct=19/19 verdict=TARGET_MET` (exit 0, 1672 B identical),
  manifest byte-copy sha256 `96965518…f838c8` (`cmp` exit 0).
- Row quotes: verified against receipt bytes —
  - S218: `sha256sum S218.bin` → `400d18195020316c25e1874e567d868458b69e342a019b3ec8da6211d7222801`; quote "You are allowed multiple hl.config() invocations, each one will update just what you pass into it." found rendered-verbatim at raw offset 268844 (inline `<code>` tag); canonical URL `https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/`.
  - S220: `sha256sum S220.bin` → `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2`; quote "Their purpose is to be fed into hl.bind() or hl.dispatch()." rendered-verbatim at raw offset 262827; canonical URL `https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/`; fully bytes-verbatim alternative "Dispatchers return tables that describe an action you want to make." at raw offset 262669.
  - S219: `sha256sum tools/mado-options.py` → `cee78d99de2e3420572aa028f439240ac12e5eb6d595de75e2fc62e5ea9ce61e` (worktree at draft finalization, 37358 B; first draft hash `9787b53b…` was stale — the tool changed mid-wave); quote is docstring line 1 (`tools/mado-options.py:2`). Peer SctRegistrySnapshot confirmed the current hash independently; lesson updated to `cee78d99…9ce61e`.
- Refusals: round-38 lesson `:40-43` + round-38-verifier-spotcheck.md `:50` (re-opened, agree) — four package entries re-recorded with unchanged reasons.
- Mistakes: refuted addendum-5 grounded in registration item 2 + round-38-verifier-spotcheck.md `:20` and `:85` + errata commits `c46f868`/`f551b70` (`git show` stats read); inherited-dirty closure grounded in spot-check `:17`, registration item 4, `git show 457d1b1 --stat` (+53/+8/+133, −7 folded under the freeze).
- Touched rows: current SOURCES has no S218/S219/S220 rows (grep count 0); S018 row read (`used-by` currently `corpus/knowledge/window-rule-effects-getprop.md`).

## Limits

- The round-39 data commit has NOT landed (HEAD == freeze `457d1b1`): tool/counter/
  entry/SOURCES rows are uncommitted worktree state. S219's receipt is therefore
   bound by *worktree* sha256 `cee78d99…`; the lesson instructs re-hashing at the
  data tip (`git show <data-tip>:tools/mado-options.py | sha256sum`). The lesson
  draft states this openly; no sha256 fabricated.
- Peer seat outputs used: ExecAssimFetches.md (S218/S220 canonical receipts+quotes,
  S219 unverifiable at its fetch window), ExecOptionsCounter.md/ScrScorecard.md
  (pending cells), ScrDispatcherAmendment.md (amendment quote map),
  ScrKnowledgeEntry.md (provisional OBS S218/S219 — superseded by the located Gate
  quotes recorded here).
- No tool installs (nothing needed beyond the repo's python3/git; RULES.md read;
  no pacman/uv/npx). No mutating git/jj; only the two seat files written.

## Final answer (≤6 lines)

1. Lesson draft written to `.ufo/waves/round-39/w1/ScrLesson/round-39.md` (only file besides this report).
2. Gate: S218/S220 quotes verified against receipt bytes (sha256 400d1819…/f9b51362…, ≤25 words, located); S219 bound to worktree tool sha256 cee78d99… (re-hashed after the file changed mid-wave) until data tip re-hash; four package refusals re-recorded with unchanged reasons.
3. Spot-check section records C1 red-before 18/19 (exit 1) → after 19/19 TARGET_MET @ freeze/tip, exit 0.
4. Mistakes: inherited-dirty closure (red-before = 3 uncommitted reports at closure; fix = freeze commit 457d1b1) and refuted addendum-5 reporting (captured by c46f868/f551b70; red-before receipt c1-redbefore.txt).
5. Touched-row status/recheck/used-by changes recorded (S218/S219/S220 new; S018 used-by extended to dispatcher-surface-and-request-grammar-r26.md).
6. No installs; no other files written; data-commit-dependent cells marked pending, none invented.
