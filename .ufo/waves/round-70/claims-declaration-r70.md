# mado round 70 — frozen claims declaration

author: mado L1 (attempt 1)
date: 2026-11-04 (America/Sao_Paulo)
base: `b37a5aec4ea03f2223d8e09dd5d386d055c24179` (round-69 closure tip)
round: mado lane counter 70 (hyaku run 15). One v1 wave of 13 seats; the L1 holds the planner seat.

This file is written **before** any candidate measurement at the scored revision. The
pre-freeze receipts are `.ufo/waves/round-70/control-baseline-r70.txt` (both do-nothing
controls) and `.ufo/waves/round-70/proto/fixture-lane.tmpl` (the feasibility fixture lane whose
three-mode probe produced the C1 base leg). Nothing in this declaration may change after the
first candidate run; a miss is an honest stop.

Two claims, distinct axes, causally separable: C1 touches only
`quality/counters/c1-r70-landing-controls.py` and `quality/counters/c1-r70-real-children.py`;
C2 touches only `quality/counters/c2-r70-carriers.py` and the frozen 17-case control set.
Neither reads the other's artifacts.

## Axis posture

Every published finite sub-axis sits at its measured maximum at the base rev (navigation
81/81, calibration 86/86, operability selftest 12/12; gate `MADO_SELFTEST: 460/460`), so no
axis is distinctly lowest (rounds 56–69 posture). The stagnation nudge does not apply: the
last capability row entered in round 69 (window N=3, gap 0). Both claims therefore take **new
finite denominators** rather than re-scoring a held rule on new inputs.

## C1 — calibration: the landing harness credits a kill only on a parsed failed assertion, and the credit is proven with real children

- **Target surface.** The kill-credit decision of the landing control harness
  (`c1-*-landing-controls.py`): the branch that turns a mutant child's exit status and output
  into `mz=pass|fail`. Round 69 froze the harness on `mz_killed = mz_rc != 0`; its paired
  assertions ("crash is not a kill", "unparseable is not a kill") ran only against scripted
  in-process stand-ins.
- **Before.** At the base rev the round-70 counter is absent. The held harness at the base rev
  credits a crashed child and a garbled-summary child as kills: on the three real-child
  scenarios it scores `base_correct=1/3` (receipt § C1 of
  `.ufo/waves/round-70/control-baseline-r70.txt`).
- **After (frozen sentence).** At `REV`, `quality/counters/c1-r70-real-children.py --repo .
  --rev REV --base-rev b37a5aec… --scratch-root DIR` prints, as its last line:

  `MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=1 verdict=TARGET_MET rev=<sha>`

  and exits 0. `quality/counters/c1-r70-landing-controls.py` is the scored harness.
- **Counting command.** The command above; bounded score `10 × correct / 3` → 10.0000;
  before `correct=absent` (0.0000) with the held harness at `base_correct=1/3` (3.3333).
- **Kill rule (before data).** Three scenarios, each a **real `bash` child** in a scratch git
  repo the counter builds (`git init`, one commit per mode, explicit identity, `-C` on every
  git call). The fixture lane `quality/landing-counters.sh` carries the frozen clause
  `[ "$citations" -gt 0 ] && ` exactly once and decides its behavior from that clause's own
  effect:
  - `genuine` — the clause's deletion makes the lane's zero-citation assertion fail
    (rc 1, `MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed`) → expected `mz=pass`;
  - `crash` — the lane exits 2 with no summary when the clause is deleted → expected `mz=fail`;
  - `garbage` — the lane prints `MADO_LANDING_COUNTERS_SELFTEST: ??? assertions passed` and
    exits 1 → expected `mz=fail`.
  A scenario is correct iff the harness's own `mz=` field equals the expectation. TARGET_MET
  iff `correct == 3` AND `base_correct == 1`. A harness that always printed `mz=fail` fails
  `genuine`; one that always printed `mz=pass` fails `crash` and `garbage`.
- **Sourced ground.** CPython `Doc/library/subprocess.rst` @ `v3.14.8` — the `returncode`
  paragraph: a nonzero status has more than one cause (a usage error, a signal death reported
  as `-N`, an ordinary missing program), so "nonzero" cannot mean "the mutant's assertions
  failed". Row id assigned at adoption; the lesson's `## Gate` records the access date,
  sha256 and a located quote, and the entry cites it.

## C2 — operability: the guard census counts four more carrier shapes and keeps the git-launch negative cases

- **Target surface.** The guard census's classifier: which constructions of the environment
  key `GIT_NO_REPLACE_OBJECTS` count as a guard that reaches a `git` launch.
- **Before.** At the base rev the round-70 counter is absent. The held round-69 classifier
  scores `13/17` on the new 17-case set: it misses `alias-carried`, `attribute-carried`,
  `splat-carried` and `constant-key` (receipt § C2 of
  `.ufo/waves/round-70/control-baseline-r70.txt`).
- **After (frozen sentence).** At `REV`,
  `quality/counters/c2-r70-carriers.py --repo . --rev REV --base-rev b37a5aec…
  --controls .ufo/waves/round-70/controls/c2-controls-r70.json --scratch-root DIR` prints, as
  its last line:

  `MADO_R70_GUARD_CARRIERS: population=20 readers=13 guarded=13 unguarded=0 controls=17/17 base_controls=13/17 verdict=TARGET_MET rev=<sha>`

  and exits 0.
- **Counting command.** The command above; bounded discrimination score
  `10 × controls / 17` → 10.0000; before `13/17` = 7.6471 by the held rule.
- **Kill rule (before data).** The 17-case set is frozen at
  `.ufo/waves/round-70/controls/c2-controls-r70.json`, sha256
  `29947b4ce5890f5c977f3ec74bafd14ba12b0d581dcb03ef1e3b637017a778ff`. Eleven cases are the
  round-69 set carried forward byte-identically; six are new: four carriers (alias, attribute,
  splat of a literal-name mapping constant, literal-name string constant as the subscript key)
  and two git-launch negatives (`guarded-env-for-a-non-git-call`, `git-called-without-env`).
  A case is correct iff reader and guard both match its frozen expectation. The population,
  reader and guarded counts are re-derived at `REV` and must stay `20 / 13 / 13 / 0` (a
  stricter rule that reclassified a real file would be reported, not tolerated). TARGET_MET
  iff all six of `population==20`, `readers==13`, `guarded==13`, `unguarded==0`,
  `controls==17`, `base_controls==13`.
- **Rule (frozen).** Round-69 key position and dominance flows stay in force. Added:
  (a) *alias-carried* — two names bound to the same mapping expression and no rebinding of the
  env-named one after the guard; (b) *attribute-carried* — the guard key stored on an attribute
  (`self.env[KEY] = …`) and that attribute passed as `env=`; (c) *splat-carried* — a
  module-level literal-name mapping constant that carries the key, expanded with `**` into the
  env mapping; (d) *constant-key* — a module-level literal-name string constant equal to the
  key used as the subscript key. All four still require one of the three dominance flows.
- **Sourced ground.** CPython `Doc/reference/expressions.rst` @ `v3.14.8` — the dictionary
  display and subscription-assignment grammar (a `**` operand is unpacked into the mapping; a
  subscript target stores under the key expression's value, not its spelling), which is what
  makes a splat and a name-valued key real carriers rather than mentions. Combined with the
  held S438 (the exported environment is what acts on the git child). Row id assigned at
  adoption; the lesson's `## Gate` records access date, sha256 and located quotes.

## Control set provenance (frozen)

| file | sha256 | cases |
|---|---|---|
| `.ufo/waves/round-70/controls/c2-controls-r70.json` | `29947b4ce5890f5c977f3ec74bafd14ba12b0d581dcb03ef1e3b637017a778ff` | 17 |

The 11 held cases are byte-identical to `.ufo/waves/round-69/controls/c2-controls-r69.json`
(`975ca3ba…`). The counter must assert both digests and refuse (rc 2) on a mismatch.

## Not claimed

Universal fault coverage; that three scenarios exhaust the kill-credit hazards; that the
fixture lane represents the lane's real landing instrument; that `**`/attribute/name-valued
carriers are the only remaining Python shapes; that the dominance rule is sound for arbitrary
Python (one module, one hop, no alias/attribute flow beyond the four added shapes, no
path-sensitivity beyond a literal-false branch); runtime behaviour of the extracted
instruments; that a guarded environment authenticates objects or repairs a rewritten
repository; desktop, compositor, session, service or package state (none is probed this
round); any `[x]`, promotion or axis retirement.

## Harm watch

`bash tools/mado-verify.sh --selftest` stays `n/n`; `quality/landing-counters.sh --round 69`
stays GREEN; `quality/counters/c1-r69-paired-recipes.py --rev REV` stays `killed=3/3
base=0/3 TARGET_MET` (the frozen round-69 counter must keep passing: the round-69 harness file
stays byte-identical); `quality/check-axis-scores.py` re-derived; no config tree, compositor,
service or sibling repo is written.
