# mado round 75 — frozen claims declaration

author: mado L1 (hyaku run 15, attempt 1)
date: 2026-11-04 (America/Sao_Paulo)
base: `b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6` (round-74 closure tip; lane clean at freeze:
`tracked=0 untracked=0`)
round: mado lane counter 75. Shape: ONE v1 wave of 12 seats (band 8–16); the L1 holds the
planner seat (the validator rejects `planner` as a swarm role).

This file is written **before** any candidate measurement. The pre-freeze do-nothing receipt is
`.ufo/waves/round-75/control-baseline-r75.txt`, produced by the uncommitted prototypes
`.ufo/waves/round-75/proto/held-r75.py` (C2: the held round-74 classifier on the frozen
forty-seven-case set) and `.ufo/waves/round-75/proto/held-r75-c1.py` (C1: the held round-72
harness on the frozen eleven fixture lanes, through the real harness pipeline) at the base
revision. Frozen control sets: `.ufo/waves/round-75/controls/c1-harness-cases-r75.json` (sha256
`f1e851a9d6133b44f6d538e97c8448bbeb174dcb5ba0a6906fe962ed3e8a6c31`) and
`.ufo/waves/round-75/controls/c2-cases-r75.json` (sha256
`d99502ba23e969a981a856a06742d8da14e1684850c7ca0e0900cd2dc7767897`). Nothing here changes
after the first candidate run; a miss is an honest stop.

**Pre-freeze disclosure.** A three-case plumbing run of the C1 candidate harness (`right`,
`stale-witness`, `crash`) was executed before this file was written, to validate the fixture
pipeline (fixture git repo → harness extraction → M-Z clause deletion → contract line). It
produced the labels the frozen set carries; no case, label, predicate, target or counter was
re-cut after it. The full baseline receipt above contains only the two held legs.

## Axis posture

At the base rev every published finite sub-axis sits at its measured maximum (navigation 91/91,
calibration resolved-active 86/86, operability selftest 12/12, ledger 130/130; gate
`MADO_SELFTEST: 460/460`). No axis is distinctly lowest, so the lowest-axis obligation has no
distinct target; the stagnation nudge does not apply either (last capability row entered round
74, window N=3, gap 0). Both claims take **new finite denominators** rather than re-scoring a
held rule on new inputs.

## C1 — calibration: the harness credits a kill only on the run's own echo of its challenge

- **Target surface.** The round-74 witness rule's own declared limit: "the rule ships as a
  standalone instrument and is not yet wired into the frozen round-72 harness". The harness
  generation that actually performs the extraction, the instrument selftest and the M-Z kill
  still credits a kill on arithmetic alone (`c1-r72-landing-controls.py:credit`), so a captured
  block replayed with matching detail lines earns a kill there.
- **Before.** The held round-72 harness on the eleven frozen fixture modes, through the real
  harness pipeline: `base_correct=6/11` — it credits the seven modes whose detail lines add up
  (`right`, `liar-success`, `uppercase-echo`, `stale-witness`, `absent-witness`,
  `wrong-witness`, `last-wins-wrong`) (`control-baseline-r75.txt`).
- **After (frozen sentence).** The successor harness `c1-r75-landing-controls.py` loads the
  frozen round-72 generation from the measured repository (bytes pinned by sha256), draws one
  `secrets.token_hex(8)` challenge per run, hands it to the child in `MADO_LANDING_NONCE`, and
  credits the M-Z kill only when the round-72 arithmetic holds **and** the child's last parsed
  `MADO_LANDING_WITNESS: <16 hex>` line equals the challenge byte-exactly; the contract outcome
  is green only under the same echo. The standing instrument `quality/landing-counters.sh`
  echoes a well-formed challenge and only then. Eleven real `bash` fixture lanes, one per frozen
  mode: `correct=11/11` with `base_correct=6/11`.
- **Counting command.** `python3 -I quality/counters/c1-r75-harness-witness.py --repo . --rev REV
  --base-rev b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6 --controls
  .ufo/waves/round-75/controls/c1-harness-cases-r75.json --scratch-root DIR`; last line
  `MADO_R75_HARNESS_WITNESS: cases=11 correct=11 base_correct=6 verdict=TARGET_MET rev=<sha>`,
  exit 0.
- **Kill rule.** `TARGET_MET` iff `cases == 11`, `correct == 11` and `base_correct == 6`;
  `TARGET_MISSED` otherwise. Exit 0 iff met; 1 iff measured and missed (an absent candidate
  harness prints `correct=absent`); 2 on usage/setup error with the reason on stderr and no
  contract line. Bounded score `10 × correct / 11` → 10.0000 (held 5.4545).
- **Do-nothing control.** The frozen round-72 harness extracted at `--base-rev` and scored on the
  same eleven fixture lanes in the same run; it must score exactly 6/11.
- **Declared limits.** The challenge authenticates the run's echo, not the truth of the
  assertions; the eleven modes are rule separators, not fault coverage; the fixture lanes are
  test doubles, not the production instrument; the successor composes the frozen generation by
  import (the frozen bytes are read from git, never edited; the pin makes a silent edit a setup
  error) — it does not re-implement the extraction or the M-R leg.

## C2 — operability: the guard census counts the copy spellings and the `del` cancellation

- **Target surface.** `quality/check-*.py` guard census (`c2-*-shapes.py` chain): the round-74
  classifier counts an env-named binding whose mapping carries the key, and a one-hop
  `os.environ` alias whose store reaches the launch. Two real idioms still escape it: a copy that
  carries the key in key position bound to a name that is not env-named
  (`child = dict(env, GIT_NO_REPLACE_OBJECTS="1")`, `child = {**env, "GIT_NO_REPLACE_OBJECTS":
  "1"}`) and handed as `env=child`; and a `del env["GIT_NO_REPLACE_OBJECTS"]` between a guard
  construction and the launch, which the held classifier still credits as guarded.
- **Before.** The held round-74 classifier on the frozen forty-seven-case set: `41/47`, missing
  exactly the four copy positives and the two `del` negatives (`control-baseline-r75.txt`).
- **After (frozen sentence).** The successor counts **any** simple name bound to a mapping that
  carries the guard key in key position and handed as `env=`, under the same dominance test (the
  binding strictly before the launch, no plain rebinding of the name in between); a copy without
  the key, a key in value position, and a rebound copy stay unguarded. It treats
  `del env[KEY]` (literal key, same scope) strictly between the guard construction and the launch
  as a cancellation, while a delete of another key and a delete before the store cancel nothing.
  The thirty-six round-74 cases stay byte-identical; the census stays `population=20 readers=13
  guarded=13 unguarded=0`; `controls=47/47 base_controls=41/47`.
- **Counting command.** `python3 -I quality/counters/c2-r75-shapes.py --repo . --rev REV
  --base-rev b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6 --controls
  .ufo/waves/round-75/controls/c2-cases-r75.json --scratch-root DIR`; last line
  `MADO_R75_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=47/47
  base_controls=41/47 verdict=TARGET_MET rev=<sha>`, exit 0.
- **Kill rule.** `TARGET_MET` iff population 20, readers 13, guarded 13, unguarded 0,
  `controls == 47` and `base_controls == 41`; `TARGET_MISSED` otherwise; same exit map as C1.
  Bounded score `10 × controls / 47` → 10.0000 (held 8.7234).
- **Do-nothing control.** The held round-74 classifier at `--base-rev` scored on the same
  forty-seven cases in the same run; it must score exactly 41/47.
- **Declared limits.** Line order is not execution order (the same cross-method approximation the
  attribute flow declares); one object-alias edge and one `os.environ` alias, no chains; the
  name-neutral rule counts a mapping handed as `env=`, not the truth of its values; `del` is
  modelled for a literal key in the same scope only; a syntactic approximation that does not
  interpret values.

## No-harm obligations (both claims)

`bash tools/mado-verify.sh --selftest` stays 460/460; the round-74 frozen instruments
(`c1-r72-landing-controls.py`, `c1-r73-summary-mutants.py`, `c2-r73-shapes.py`,
`tools/mado-verify.sh`) stay byte-identical; `c2-r74-shapes.py` stays byte-identical (the
successor carries its cases and is scored against it); the index, ledger, axis table and
navigation checks stay at their measured values; the three new instruments enter
`quality/tool-ledger.md` in the same round (`quality/check-tool-ledger.py` `uncovered=0`);
`quality/landing-counters.sh` is the one declared instrument amendment (a nonce-gated echo that
prints nothing when the challenge is absent, so every held caller keeps its output). Neither claim
touches configuration, the compositor, a service, a sibling repo or `~/.config`.

## Sources plan (frontier step)

Two rows opened this round with three byte-identical fetches each (receipts under
`.ufo/waves/round-75/fetch/`): CPython 3.14.8 `Doc/reference/simple_stmts.rst` § The `del`
statement (the subscription delete is passed to the primary object, so `del env[KEY]` mutates the
mapping handed to the child) and `Doc/library/stdtypes.rst` § `dict` (a `dict(mapping, **kwargs)`
copy carries the keyword pairs, so the copied mapping holds the guard key). Duplicate-id and
duplicate-URL checks run before any append; the registry census must exit 0 at round end.

## Routed-defect dispositions (round-74 closure D1–D5)

D1 (`SKILL.md:734` says 21/21 where the rule prints 23/23) is corrected in place and the LOG
correction appended; D2 (post-repair selftest receipts unlanded) by committing the receipts with
`--controls` named (`receipts/selftest-r75.txt`); D3 (S446 quote count 23 vs 21) recorded as a
corrected count in this round's lesson; D4 (declaration seat count) by stating the actual wave
size in this declaration and the report; D5 (advisory: `mado-r74-witness-rule` registered `gate`
with only a `--selftest` entry) by reclassifying that ledger row as `probe` in the same row's
class cell, and the carried `tools/mado-verify.sh:418` hardcoded `/tmp` scratch by honouring
`TMPDIR`/`MADO_SELFTEST_SCRATCH` there with its own red-before receipt. None of these changes a
frozen claim.
