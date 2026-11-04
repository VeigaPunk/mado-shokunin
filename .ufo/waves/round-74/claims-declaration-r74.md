# mado round 74 — frozen claims declaration

author: mado L1 (hyaku run 15, attempt 1)
date: 2026-11-04 (America/Sao_Paulo)
base: `bd5a971532f37df85a78f6f566dd1e649b79de11` (round-73 closure tip; lane clean at freeze:
`tracked=0 untracked=0`)
round: mado lane counter 74. Shape: ONE v1 wave of 12 seats (band 8–16); the L1 holds the
planner seat (the validator rejects `planner` as a swarm role).

This file is written **before** any candidate measurement. The pre-freeze do-nothing receipt is
`.ufo/waves/round-74/control-baseline-r74.txt`, produced by the uncommitted prototype
`.ufo/waves/round-74/proto/held-r74.py` (not a scored counter) at the base revision. Frozen
control sets: `.ufo/waves/round-74/controls/c1-replay-cases-r74.json` (sha256
`17c95774044fb2d8125b9f4bf85bdcb947babb60e438424f246b77785574727c`) and
`.ufo/waves/round-74/controls/c2-cases-r74.json` (sha256
`4db4cc70d1a8e86876f20a9527cfc7f0c7a344eb6d2655b398443b907b3a73d0`). Nothing here changes
after the first candidate run; a miss is an honest stop.

## Axis posture

At the base rev every published finite sub-axis sits at its measured maximum (navigation 89/89,
calibration resolved-active 86/86, operability selftest 12/12, ledger 127/127; gate
`MADO_SELFTEST: 460/460`). No axis is distinctly lowest, so the lowest-axis obligation has no
distinct target; the stagnation nudge does not apply either (last capability row entered round
73, window N=3, gap 0). Both claims take **new finite denominators** rather than re-scoring a
held rule on new inputs.

## C1 — calibration: the credit rule requires the run's own witness of the counter's challenge

- **Target surface.** The landing kill credit's declared limit (rounds 71–73): "a captured
  summary replayed with its own matching detail lines remains byte-indistinguishable from a
  genuine run — the rule bounds the summary to the run's own fail lines, it does not
  authenticate them." The held rule (`c1-r72-landing-controls.py:credit`) therefore credits a
  replay.
- **Before.** The held round-72 `credit(out)` on the twelve-case frozen set: `correct=8/12` — it
  credits all four replay cases (`control-baseline-r74.txt`).
- **After (frozen sentence).** A successor `credit(out, nonce)` credits a run only when the
  round-72 arithmetic holds **and** the run's last parsed `MADO_LANDING_WITNESS: <16 hex>` line
  equals the per-run challenge the caller supplies; a captured block carrying a stale witness, a
  block with no witness, a block whose witness is wrong, and a block whose last witness is wrong
  all earn no credit, while the eight round-72 modes keep their frozen expectations:
  `correct=12/12` with `base_correct=8/12`.
- **Counting command.** `python3 -I quality/counters/c1-r74-replay-witness.py --repo . --rev REV
  --base-rev bd5a971532f37df85a78f6f566dd1e649b79de11 --controls
  .ufo/waves/round-74/controls/c1-replay-cases-r74.json --scratch-root DIR`; last line
  `MADO_R74_REPLAY_WITNESS: cases=12 correct=12 base_correct=8 verdict=TARGET_MET rev=<sha>`,
  exit 0.
- **Kill rule.** `TARGET_MET` iff `cases == 12`, `correct == 12` and `base_correct == 8`;
  `TARGET_MISSED` otherwise. Exit 0 iff met; 1 iff measured and missed (an absent candidate rule
  prints `correct=absent`); 2 on usage/setup error with the reason on stderr and no contract line.
  Bounded score `10 × correct / 12` → 10.0000 (held 6.6667).
- **Do-nothing control.** The held `credit` extracted at `--base-rev` scored on the same twelve
  real `bash` children in the same run; it must score exactly 8/12.
- **Declared limits.** The challenge authenticates the *run's echo*, not the truth of the
  assertions: a run that echoes the challenge and lies about its own arithmetic still passes the
  arithmetic check it is built on; the twelve cases are fixture lanes, not fault coverage; the
  rule ships as a standalone instrument and is not yet wired into the frozen round-72 harness.

## C2 — operability: the guard census counts the two-hop object alias and the environment alias

- **Target surface.** `quality/check-*.py` guard census (`c2-*-shapes.py` chain): the round-73
  classifier reaches a guard through a literal, a one-hop mapping alias, an attribute store, a
  `global`-declared name and a mutated `os.environ` copied by `{**os.environ}` / `dict(os.environ)`.
  Two real idioms still escape it: an object alias bound to a dotted path (`r = cfg.runner`) whose
  `.env` is stored and handed at the *other* spelling (`env=cfg.runner.env` / `env=r.env`), and a
  one-hop alias of `os.environ` whose key store reaches a launch that copies the alias
  (`dict(env)` / `{**env}`).
- **Before.** The held round-73 classifier on the thirty-six-case set: `32/36`, missing exactly
  the four new positives (`control-baseline-r74.txt`).
- **After (frozen sentence).** The successor resolves a one-hop object alias both directions and
  counts a guard stored at either spelling of the dotted path, under the same dominance test (the
  store strictly before the launch, no replacement of the dotted path in between, the alias bound
  exactly once); it follows a one-hop alias of `os.environ` and counts a store into the alias when
  the launch's `env=` is the alias itself, `dict(alias)` or `{**alias}`, with a rebinding of the
  alias or a store after the launch not counted. The twenty-eight round-73 cases stay
  byte-identical: `controls=36/36 base_controls=32/36`.
- **Counting command.** `python3 -I quality/counters/c2-r74-shapes.py --repo . --rev REV
  --base-rev bd5a971532f37df85a78f6f566dd1e649b79de11 --controls
  .ufo/waves/round-74/controls/c2-cases-r74.json --scratch-root DIR`; last line
  `MADO_R74_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=36/36
  base_controls=32/36 verdict=TARGET_MET rev=<sha>`, exit 0.
- **Kill rule.** `TARGET_MET` iff population 20, readers 13, guarded 13, unguarded 0,
  `controls == 36` and `base_controls == 32`; `TARGET_MISSED` otherwise; same exit map as C1.
  Bounded score `10 × controls / 36` → 10.0000 (held 8.8889).
- **Do-nothing control.** The held round-73 classifier at `--base-rev` scored on the same
  thirty-six cases in the same run; it must score exactly 32/36.
- **Declared limits.** Line order is not execution order (the same cross-method approximation the
  attribute flow already declares); one object-alias edge and one `os.environ` alias, no chains;
  the generic env-named flow's `del env[KEY]` cancellation is still unmodelled; a syntactic
  approximation that does not interpret values.

## No-harm obligations (both claims)

`bash tools/mado-verify.sh --selftest` stays 460/460; the frozen round-72/73 instruments stay
byte-identical; the index, ledger, axis table and navigation checks stay at their measured values;
both new instruments enter `quality/tool-ledger.md` and the `SKILL.md` Gate registry in the same
round (`quality/check-tool-ledger.py` `uncovered=0`). Neither claim touches configuration, the
compositor, a service, a sibling repo or `~/.config`.

## Sources plan (frontier step)

Three rows opened this round with three byte-identical fetches each (receipts under
`.ufo/waves/round-74/fetch/`): CPython 3.14.8 `Doc/library/secrets.rst` (the `token_hex` challenge
the C1 rule compares), `Doc/reference/simple_stmts.rst` § assignment statements, attribute
references (the C2 two-hop store), and `Doc/library/os.rst` § `environ` (the alias's mutation is
the same mapping). Duplicate-id and duplicate-URL checks run before any append; the registry
census must exit 0 at round end.

## Routed-defect dispositions (round-73 closure D1–D6)

D1 (S448 digest false) is repaired by a superseding row in this round's Gate block, append-only,
with the re-derived digest; D2 (post-repair selftest tallies without a committed run) by
committing the post-repair selftest receipts at the measured commit; D3 (a receipt overwritten in
place) by appending both runs; D4 (QUALITY 118/119 in the root fragment) by appending them to the
canonical `corpus/QUALITY.md` and redirecting the root fragment; D5 (S446 has no ≤25-word located
quote) by recording it in this round's Gate block; D6 (pre-repair `verified-at:`) is a note carried
to the next entry refresh, not a false claim. None of these changes a frozen claim.
