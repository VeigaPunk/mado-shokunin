author: hyaku closure (non-author integrator, @m_zfl)
lane: mado · lane-round 75 · date 2026-11-04 (America/Sao_Paulo)
lane base: `b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6` · lane tip: `f1827f9d5f3fe29eb2bb7e1b8701cadd436f3069`
report: `.ufo/reports/round-75/mado.md` @ `0a54576981f96e2fdab1ef2b6e9a38a9e47295b9`
driver digest: `2026-11-04T02:59:55-03:00 launch mado round=75 pgid=168215 driver=hyaku-inline
attempt=1`; `2026-11-04T03:27:26-03:00 complete mado round=75; hyaku-inline attempt=1`

This file is the closure's non-author record. It verifies and spot-checks; it does not author round
work, and nothing here changes a lane-authored file.

## 1. Step-1 conformance — PASS

- **Attribution and order.** `git log --format='%an|%ae|%H|%s' -1 -- .ufo/reports/round-75/mado.md`
  prints `mado-shokunin|mado@shokunin.local|0a545769…|round-75: mado report`, committed
  03:26:57-03:00, after the lane tip commit `f1827f9d` at 03:26:15-03:00 and after every lane
  commit the report cites. `git merge-base --is-ancestor 0a545769 origin/master` holds on the
  fleet repo (fleet `HEAD` = `origin/master` = `4c1711cb`). The dispatch-evidence commit
  `08555038` (02:59:54) precedes the launch line (02:59:55).
- **SHONEN.** `## SHONEN` appears once; four `[~]` lines with evidence pointers, zero `[x]`;
  `SHONEN.md` is byte-unchanged across the round (`git diff --stat b149d2e f1827f9d -- SHONEN.md`
  prints nothing) and still carries four `[~]` boxes.
- **Cited commits.** Fourteen cited hashes exist and pass
  `git -C mado-shokunin merge-base --is-ancestor <hash> master` (branch ref `master`, never
  `@{u}`; HEAD is detached): `def73656`, `dd237a55`, `b545bea9`, `e3e29bb4`, `79a4ff7b`,
  `f75afbf6`, `4527fcae`, `466e1307`, `745eca38`, `a3c88663`, `1557198f`, `f0cf818d`,
  `87b85c9f`, `f1827f9d`, plus base `b149d2e`.
- **Cleanliness and push.** `scripts/hyaku/jj-lane.sh state mado-shokunin` prints
  `branch=master local=f1827f9d remote=f1827f9d ahead=0 behind=0 head=detached tracked=0
  untracked=0`; `git status --porcelain` is empty; `git ls-remote origin refs/heads/master`
  prints `f1827f9d5f3fe29eb2bb7e1b8701cadd436f3069`. Fleet-repo leftovers are orchestrator
  scratch (`.scratch/*`), not mado round work.
- **Prompt fidelity.** `.ufo/prompts/mado-round-75.md` lines 1–140 equal
  `templates/round-prompt.md` verbatim modulo the lane/round/fleet substitutions (`diff` shows
  only `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` lines), so §1 mission/axes, §2 claims
  1–3, §2b frontier, §3 the L2 floor (≥8, one batched call, band 8–16), §4 report contract plus
  `SHONEN`, §5 commit-then-push, push scope and L0 are carried. The five child-lane items are
  present: report path/filename (§4), commit-then-push (§5), `SHONEN` heading (§4), the
  commit-hash citation rule and the lane write scope (addendum §6: "The report lands last and
  cites the pushed lane hash"; "**Write scope:** /home/vgpnk/Projects/shokunin/mado-shokunin").
- **Status-neutral notes.** (a) The run-15 routing sentence ("ONLY reviewer uses `@m_zfl`") is
  stale against the live `task.agentModelOverrides` (reviewer/critic/executor/mutation-tester/
  connector/sentinel/scribe are `@m_zfl`); harmless — the prompt names that config as authority,
  dispatch carries zero `model` keys, and `MISSION.md`'s role-class table is advisory. (b) The L1
  held the planner seat because the validator rejects `planner` as a swarm role; the 13 seats are
  otherwise the template's split, 13 ≥ 8. (c) The frozen declaration still says "ONE v1 wave of
  12 seats" (see routed defect R1).

## 2. Claim re-checks

Freeze integrity first: the control files changed only at `def73656`
(`git log --format='%h' -- .ufo/waves/round-75/controls/` → `def73656`), so no case, label,
predicate or target was re-cut after the freeze. Hashes recomputed today:
`sha256sum .ufo/waves/round-75/controls/*.json` → `f1e851a9…` (11 cases, `jq length` = 11) and
`d99502ba…` (47 cases) — both equal the declaration, SCORECARD and receipts. The pre-freeze
do-nothing baseline reads `correct=6/11` and `held_correct=41/47`. Both claims are
**evidence-verified**, not re-executed: PROTOCOL §Gate standard bars the integrator from running
a sibling's gate, so I re-derived every tally the receipts state from committed bytes with
`awk`/`jq`/`sha256sum`/`git ls-tree`.

**C1 — calibration: witness-gated credit in the landing harness. Verdict: improved.**
- Instrument identity at the measured revision: `git show a3c88663:quality/counters/c1-r75-landing-controls.py | sha256sum`
  → `51652b43…` (the receipt's pin); `git show b149d2e:quality/counters/c1-r72-landing-controls.py | sha256sum`
  → `b6108c86…`, and `git show b149d2e:… | grep -c token_hex` → `0`: the held harness cannot echo
  a per-run challenge.
- Code inspection at the measured content: `witness_state`/`last_witness` parse the last
  `MADO_LANDING_WITNESS: <16 hex>` line; `credit_with_witness` and `green_with_witness` conjoin
  the frozen r72 predicate with `last_witness(out) == nonce`; `contract_line` greens only through
  `green_with_witness` and refuses on `killed != 2`; the generation is loaded under the
  `b6108c86` sha256 pin and written `O_NOFOLLOW`; `describe_env` redacts `MADO_LANDING_NONCE`.
- Receipt tally (committed at `1557198f`, measured `rev=a3c88663`):
  `awk '/^MADO_R75_CASE/{n++; if(/correct=yes/)y++} END{print n, y}' .ufo/waves/round-75/measurement-c1-r75-final.txt`
  → `11 11`; base leg `base=pass` on 7 modes and `base=fail` on 4, i.e. 6 correct (2 genuine
  passes + 4 correct fails) against the receipt's `base_correct=6`. Every expected label in the
  controls (`expect_kill` true for `right`/`liar-success`, false for the other nine) matches the
  receipt's `expect=` column.
- Limits, as declared: the counter scores the M-Z decision only; the outcome clause is
  implemented and inspected but not certified by the frozen denominator (critic finding, carried
  as a named limit and planned item 1). Bounded 10 × 11/11 = 10.0000 against held 5.4545.

**C2 — operability: two guard-census deltas. Verdict: improved.**
- Instrument identity: `git show 4527fcae:quality/counters/c2-r75-shapes.py | sha256sum` →
  `0544c0ef…`; held `c2-r74-shapes.py` → `eb43e2b6…` (the receipt's pin). The 36 carried cases
  are byte-identical to the round-74 set: `jq -S '.cases[0:36]'` on the r75 file and
  `jq -S '.cases'` on the r74 file both hash `e61b35fd…`.
- Receipt tally (committed at `466e1307`, measured `rev=4527fcae`):
  `awk` over `measurement-c2-r75-final.txt` → candidate leg `47` lines, `47` `correct=yes`;
  base leg `47` lines, `41` `correct=yes` (the six misses are the four copy positives and the
  two delete cancellations). Every candidate `expect_*` equals the observed `reader`/`guard`.
- Population, re-derived without the lane gate: 20 `quality/check-*.py` files exist at
  `4527fcae` (`git ls-tree … | wc -l` → `20`); exactly 13 of them contain
  `GIT_NO_REPLACE_OBJECTS`, and those 13 names equal the receipt's 13 `reader=yes` rows; the
  receipt reports `guarded=13 unguarded=0`. This corroborates `population=20 readers=13
  guarded=13 unguarded=0` independently of the instrument.
- Bounded 10 × 47/47 = 10.0000 against held 8.7234.

**No-harm watch (spot reads + counts).**
`git diff --numstat b149d2e f1827f9d -- SCORECARD.md` → `100 0` (append-only; no existing score
line changed); `LOG.md` `54 0`; `PROVINCE.md` `18 0`; `corpus/QUALITY.md` `36 0`;
`corpus/SOURCES.md` `2 0`; `corpus/README.md` `3 0`; `SKILL.md` `4 1` (three registry rows added,
the `mado-r74-witness-rule` row corrected to 23/23 and reclassed `probe`).
`git ls-tree -r --name-only <rev> -- corpus/knowledge | wc -l` → `91` at base, `93` at tip, and
`corpus/README.md` links exactly 93 distinct knowledge files. Instrument population re-derived
from the ledger's own rule (tools/ + `quality/*.py` + `quality/counters/*.py`, excluding
`__pycache__`/`*.pyc`/`*.txt`/`*.json`) → `130` at base, `133` at tip, matching the ledger's 133
data rows. `grep -cE '^\| S[0-9]{3,}' corpus/SOURCES.md` → `391` (389 + S453/S454), malformed-row
awk → `0`. The gate amendment (`tools/mado-verify.sh` +16/−4) derives its selftest scratch from
`MADO_SELFTEST_SCRATCH`/`TMPDIR` with `/tmp` as the default; `PIN_MADO` re-cut
`367ff5ec…` → `49567a0f…`; the committed receipt `w1/R75ExecGate/gate-current.txt` shows
`MADO_SELFTEST: 460/460` at the amended bytes and `gate-frozen-red.txt` shows the frozen script
ignoring `TMPDIR` (the red-before). `quality/landing-counters.sh` gained only
`landing_witness()`, which returns before printing when the challenge is absent or malformed, so
held callers keep their output.

## 3. Axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| depth | unchanged | no claim; the two entries add sourced rules without rewriting held ones |
| coverage | unchanged | harm watch only: index 91 → 93 (README links 93/93), no surface claimed |
| operability | **improved** | C2 41/47 → 47/47 on frozen cases; population 20/13/13/0 re-derived; gate 460/460 at amended bytes |
| freshness | unchanged | no claim; harm watch holds; revision-attribution defects routed (R5) |
| calibration | **improved** | C1 6/11 → 11/11 on frozen modes; instrument pinned `b6108c86` → `51652b43`; outcome leg declared uncertified |
| adjacency | unchanged | no sibling surface written; `PROVINCE.md` append-only |

## 4. Discernment spot-check (non-author)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S453 — CPython v3.14.8 `Doc/reference/simple_stmts.rst` § del | admit (`mined`, tier A, `used-by corpus/knowledge/guard-carrier-copy-del-r75.md`) | live `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst`, fetched 2026-11-04; sha256 `d4320642…`, 41,375 B (equals the committed fetch trio); lines 468–469 | **agree** | The quote "Deletion of attribute references and subscriptions is passed to the primary object involved" is verbatim at `:468-469`, tokenises to 13 words (≤25), and grounds exactly the subscription-delete rule C2 counts; `used-by` resolves to an existing file. |
| S454 — CPython v3.14.8 `Doc/builtins/stdtypes.rst`, `dict(mapping, **kwargs)` | admit (`mined`, tier A, same `used-by`) | same live fetch; sha256 `5a6951b7…`, 248,201 B (equals the committed trio); lines 5350–5352; constructor at 5325–5327 | **agree** | "If keyword arguments are given, the keyword arguments and their values are added to the dictionary created from the positional argument" is verbatim at `:5350-5352`, 21 words, and grounds the copy-carries-the-key rule; scope is the constructor, not S446's method behaviour, so no supersession is needed. |
| S446 — same document, mapping methods | reject (kept, `rejected`, flip: a mapping-method claim) | same live fetch; `:5521-5531` (`setdefault`, `update` forms) | **agree** | The document is method behaviour (argument forms/defaults), not call-site or result-object semantics; no admitted entry needs it. The lesson's correction of the round-74 quote count from 23 to 21 words is right: `"If key is in the dictionary, return its value. If not, insert key with a value of default and return default."` tokenises to 21. |

Census, run from the lane root: `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin mado` → exit 0, 47 lines, byte-identical to the committed
`.ufo/waves/round-75/census-end-r75.txt` (`diff` empty). Both new rows raise the documented
non-failing W04 duplicate-URL warning.

## 5. Trend verdicts

- **expansion: improved.** Two admitted knowledge entries on the round-74 frontier ground
  (harness wiring; copy/delete carriers), each `source:`-bound to a `mined` row (S453/S454;
  S450 plus own-work for C1); the index grows 91 → 93 with zero removals; two tier-A rows opened
  with byte-identical three-fetch receipts re-verified against the live URLs.
- **quality: improved.** Ten wave-found defects repaired at named commits without touching a
  frozen predicate, label, control set or target; four QUALITY criteria (124–127) land from
  lessons M75-1…M75-4, each citing its lesson and showing a red-before; the gate is re-measured
  460/460 at its amended bytes with `PIN_MADO` re-cut; both claims are re-measured at their final
  instrument commits. The routed defects below are evidence/attribution nits; no admitted entry
  is false or stale-unmarked.
- **discernment: improved.** This outside spot-check agrees with both admits and the re-opened
  reject, on re-opened sources and re-derived counts; the round's own wave found ten defects the
  L1's selftests missed and each is repaired with a flip receipt or carried as a named limit.

## 6. Routed defects for round 76 (status-neutral)

- **R1 — D4 repeated.** `claims-declaration-r75.md:6` says "ONE v1 wave of 12 seats"; the
  dispatch carries `counts.spawn=13`, 13 results, and the declaration's own D4 disposition claims
  it states the actual size. Not rewritten (frozen); carry the actual count next declaration.
- **R2 — D2 partially repeated.** The declaration's D2 disposition names
  `receipts/selftest-r75.txt`, which does not exist, and the registry row
  `mado-r75-harness-witness` declares a 17/17 selftest tally with no committed stdout anywhere
  (`MADO_R75_HARNESS_WITNESS_SELFTEST` appears only in the instrument source). Committed tallies
  exist for the sibling instruments (landing-controls 20/20 at `def73656`, c2 97/97, r74 rule
  23/23, gate 460/460). Commit a receipt or cite the actual path.
- **R3 — severity misattribution.** The report and SCORECARD call R75RevC2's two findings "P1"s;
  the seat's own file says "P1 — None established" and lists both as P2. Cite the seat's severity
  or record the re-grade with a reason.
- **R4 — `used-by` not extended.** `corpus/knowledge/harness-witness-credit-r75.md` cites S450,
  but S450's `used-by` still names only `replay-witness-credit-r74.md`, and the lesson logs no
  cell change. Per CORPUS rule 2, extend `used-by` and log old → new.
- **R5 — revision attribution.** SCORECARD says C2 was measured at `4527fcae` "(its instrument's
  last change)", but `c2-r75-shapes.py` last changed at `f75afbf6`; the entry, README row and
  SCORECARD say C1's final measured content is `4527fcae` while the final C1 receipt is at
  `a3c88663`. State measured-rev versus instrument-last-change separately.
- **R6 — freeze wording.** The declaration says it is "written **before** any candidate
  measurement" and then discloses a three-case pre-freeze plumbing run; state the exception in
  the same sentence next round.
- **R7 — receipts without command/rc.** `receipts/red-scratch-before.txt` and
  `green-scratch-valid.txt` carry only the tally line, while lesson M75-6 says the receipts carry
  commands and rc; the command+rc evidence lives in `w1/R75ExecGate/`.
- **R8 — doc nits.** `c2-r75-shapes.py`'s usage example still shows
  `--base-rev bd5a9715…`; the report's landing-counters sentence attributes the later instrument
  repairs to a file that changed only at `def73656`.

## 7. Closure

Both declared claims verify on frozen, do-nothing-separated denominators (11/11 vs 6/11;
47/47 vs 41/47), no owned axis is harmed (SCORECARD append-only; index 93/93; ledger 133/133;
sources 391 rows; gate 460/460 at amended bytes; census exit 0), and the non-author
discernment check agrees with the gate on two admits and one re-opened reject. **Admitted.**
