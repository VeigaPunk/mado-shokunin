# mado round 76 — frozen claims, predicates, counting commands, kill rules, targets

Round 76 of lane `mado-shokunin` (hyaku run 15). Base revision:
`c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf` (lane branch tip, the round-75 verifier
spot-check commit). This file is written **before** any candidate measurement; the only
pre-freeze run was a three-leg plumbing check that labelled the fixture modes
(disclosed: it scored the frozen successor harness against its own modes, never against
the targets below; the round-75 R6 lesson requires the exception to be stated in the
same breath).

Both claims are causally separable: C1 is a counter over the landing harness and its
outcome field; C2 is a census rule over the lane's own `quality/check-*.py`
population. Neither depends on the other landing.

## C1 — calibration: the successor counter certifies the contract outcome field

**Prior state.** `quality/counters/c1-r75-harness-witness.py` parses the harness's `mz=`
field only. A rule mutation that keeps the M-Z kill term and drops the *outcome* term
(`green_with_witness`) therefore survives every frozen denominator the lane holds
(round-75 declared limit, critic finding; the `uppercase-echo` separator is also
probabilistic because `token_hex(8)` may draw sixteen decimal digits — M75-4).

**Claim (frozen).** A successor counter,
`quality/counters/c1-r76-outcome-field.py`, scores **both** the `mz=` field and the
`verdict=` field of `quality/counters/c1-r76-landing-controls.py` against a frozen
fifteen-case expectation, and separates four named mutations of the outcome rule at
unique source anchors.

**Counting command** (run from the lane root; `REV` = the commit carrying the
instruments):

```sh
python3 -I quality/counters/c1-r76-outcome-field.py --repo . --rev REV \
  --base-rev c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf \
  --controls .ufo/waves/round-76/controls/c1-outcome-cases-r76.json \
  --scratch-root <scratch>
```

**Frozen case set.** `.ufo/waves/round-76/controls/c1-outcome-cases-r76.json`, sha256
`ff97505f7cce829e3e15d356fd4305a39825d47997e4dac20be034931da7fc40`, fifteen real
`bash` fixture lanes, one per mode, each labelled with `expect_mz` and `expect_verdict`.
The four green modes are the outcome-rule separators; `green-mutant` is the case where
the outcome field is not redundant with `mz` (`mz=fail`, `verdict=pass`).

**Frozen mutants** (anchored at `green_with_witness`'s single return line):

| mutant | rule change | separator case |
|---|---|---|
| `outcome-term-dropped` | the outcome ignores the echo | `green-absent` |
| `prefix-match` | echo equality becomes a prefix test | `green-overlong` |
| `first-witness-wins` | the first parsed echo wins | `green-last-wrong` |
| `case-insensitive` | the echo comparison folds case | `green-uppercase` |

**Kill rule (frozen).** A mutant is killed iff its two-field score is below fifteen. The
**do-nothing control** is the held round-75 scoring rule, which reads `mz=` only: a
mutant is base-killed iff its mz-only score is below fifteen.

**Target (frozen).** Exit 0 and `verdict=TARGET_MET` iff
`cases=15 correct=15 mutants=4 killed=4 base_killed=0`. Exit 1 iff measured and missed;
2 on usage/setup error.

**Grammar and challenge (frozen, in the successor harness).** G1: the witness grammar
reads sixteen **or more** hex characters, so an over-long echo is a parsed mismatch
(under the round-75 sixteen-only grammar prefix-versus-equality was unobservable).
G2: the per-run challenge is drawn by rejection sampling until it contains at least one
`a-f` letter, so uppercasing it always changes its bytes (deterministic uppercase
oracle; closes M75-4).

**Declared limits.** The mutants patch the outcome helper only, so the kill path stays
correct by construction — that is exactly why the held rule cannot see them. The
fifteen modes are rule separators, not fault coverage; the challenge authenticates the
echo, not the truth of the assertions.

## C2 — operability: the census counts an interprocedural cancellation and a dynamic key

**Prior state.** `quality/counters/c2-r75-shapes.py` models `del env[KEY]` for a literal
key in the same scope only. A delete inside a callee that receives the mapping, and a
delete whose key is a same-scope name bound to the guard key, are invisible (round-75
declared limits, planned item 3).

**Claim (frozen).** The successor census `quality/counters/c2-r76-shapes.py` counts
both shapes and keeps its population verdict.

**Counting command:**

```sh
python3 -I quality/counters/c2-r76-shapes.py --repo . --rev REV \
  --base-rev c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf \
  --controls .ufo/waves/round-76/controls/c2-cases-r76.json \
  --scratch-root <scratch>
```

**Frozen control set.** `.ufo/waves/round-76/controls/c2-cases-r76.json`, sha256
`df9e89841ed560613d7a05ad50f345b2d6bbf0d8e40a98f51e8b8134492b3948`, fifty-nine cases:
the forty-seven round-75 cases carried byte-identically (hash-checked against
`.ufo/waves/round-75/controls/c2-cases-r75.json`, sha256 `d99502ba…`) plus twelve
round-76 cases:

| case | expectation |
|---|---|
| `callee-del-literal` | reader, **not** guarded |
| `callee-del-store` | reader, **not** guarded |
| `dynamic-key-del` | reader, **not** guarded |
| `dynamic-key-module-const` | reader, **not** guarded |
| `callee-del-param-rebound-live` | reader, guarded (the delete targets a copy) |
| `callee-del-other-key` | reader, guarded |
| `callee-del-dead-branch` | reader, guarded |
| `callee-never-called` | reader, guarded |
| `callee-called-after-launch` | reader, guarded |
| `callee-del-param-rebound` | reader, guarded |
| `dynamic-key-other` | reader, guarded |
| `dynamic-key-rebound` | reader, guarded |

**Target (frozen).** Exit 0 and `verdict=TARGET_MET` iff
`population=20 readers=13 guarded=13 unguarded=0 controls=59/59 base_controls=55/59`.
Exit 1 iff measured and missed; 2 on usage/setup error.

**Rule deltas (frozen).** D3: a live `del m[KEY]` inside a local function `f(m)` cancels
a guard on the mapping the caller hands to `f(env)`, under the dominance test (the call
line strictly between the guard line and the first launch use). D4: `del env[k]` where
`k` is bound exactly once in the same scope, before the delete, to the guard key (a
literal or a module constant), cancels the store.

**Declared limits.** Line order is not execution order; the callee is matched by simple
call shape (a positional first argument), never through a function alias or a call
chain; the callee's delete key is a literal or module constant (not a dynamic key); D3
is modelled in the env-named/subscript carrier flows, not in the attribute flow; the
census is a syntactic approximation that does not interpret values.

## No-harm watch (frozen dispositions)

- `tools/mado-verify.sh`: **byte-identical** this round (no claim touches it); its
  selftest must stay `460/460`.
- Held instruments (round-72/73/74/75 counters, `quality/landing-counters.sh`,
  `quality/check-tool-ledger.py`, `quality/check-axis-scores.py`,
  `quality/check-index.py`): byte-identical to the base revision.
- Index: 93/93 at base; the round adds knowledge entries and keeps it complete.
- Tool ledger: 133 rows at base; every new instrument gets a ledger row in the same
  round.
- No live desktop, compositor, service or session probe this round; no credential or
  session material in any receipt.
- SOURCES registry: appended rows pass the census (exit 0) at round end.

## Routed-defect dispositions (round-75 closure R1–R8)

- R1 (seat-count drift): this declaration names no seat count; the report states the
  dispatched and settled counts from `w1-dispatch.json` and `w1-results.json`.
- R2 (a declared selftest receipt with no committed stdout): every selftest tally quoted
  this round is committed as a receipt with its command, stdout and exit code under
  `.ufo/waves/round-76/receipts/`.
- R3 (severity misattribution): seat findings are cited with the seat's own severity
  string; re-grades are recorded with a reason.
- R4 (`used-by` not extended): every `mined` row adopted this round names its citing
  entry in `used-by`, and each change is logged old → new in the lesson.
- R5 (measured rev vs instrument last change): the report states the measurement
  revision and each instrument's last-change commit separately.
- R6 (freeze wording): disclosed in the header of this file.
- R7 (receipts without command/rc): receipt files this round carry command, stdout tail
  and exit code.
- R8 (doc nits): the usage examples in every new counter name the base revision actually
  used above.
