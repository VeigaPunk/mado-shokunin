# R69MutBattery — round-69 mutation battery (C1 calibration, C2 operability)

Seat: mutation-tester. Scratch-only: no lane, proto, draft, control, fixture or fleet file was
written by this seat. Every mutation copy lived under
`/fast/scratch/hyaku/mado-r69/R69MutBattery` (removed at exit; receipt below).

Axes: **C1 calibration** — does the C1 counter's own `--selftest` kill single-point defects in
the counter, and what does each mutant print on a known-good fixture; **C2 operability** — the
same for the C2 counter. No claim is re-scored and no target is narrowed.

## Tested bytes

| Artifact | sha256 | Where |
|---|---|---|
| C1 counter, landed | `9f17a984023829b827f44411e5d7d1e2a684e422d6b296ab90b0e2e27c206ce8` | `quality/counters/c1-r69-paired-recipes.py` at HEAD `296ed0d7` |
| C2 counter, landed | `85f9e60a6d177ba1239cf547b25f7c4596b3548fbf7ad444ede556eac44d725a` | `quality/counters/c2-r69-guard-dominance.py` at HEAD `296ed0d7` |
| C1 harness, landed | `9461a059466e723ba0ae88c86dea2fc97eb5f4fdfb15ef6c6646acce69649a73` | `quality/counters/c1-r69-landing-controls.py` at HEAD `296ed0d7` |
| C1 counter, measured content | `2060da8dcdb43bcbd08756d0e55630fe585833af3a638b5bc891aa4d77492f82` | `6a5cefd2` (measurement receipt revision) |
| C2 counter, measured content (pre-repair) | `b6bcec07ffe1849f9ef9a3c1a1e25d94743be6e01e9cae4219ea8045996b673a` | `6a5cefd2` |
| C1 harness, measured content | `b374cfb8e024971e69a19d44af21efe5ed1b46c03a3b57387f7dd7fd4eed69aa` | `6a5cefd2` |
| C1 harness prototype | `f4d138bfe806f787a98d5ca4d48ebf44896a4276cb0964df5d99e16f6b25390f` | `.ufo/waves/round-69/proto/c1-r69-landing-controls.proto.py` |
| C1 counter intermediate worktree | `aa78c2445be12d95d1c18ed8e53d0145247a4046d7cd3f656f4e9e1f49b97815` | live worktree snapshot |
| C1 harness intermediate worktree | `11aa7f89b8467bfabdfa5a5364dabf27d091c468225c649c27d2b5f3b5806ccc` | live worktree snapshot |
| Frozen controls | `975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9` | `.ufo/waves/round-69/controls/c2-controls-r69.json` |

Pinned revisions: base `04093b83f73a841117d3b31dbb2a6063f4f2a454`, measured content
`6a5cefd252c41c7ff71217da65126fc831f8bc34`, lane HEAD during the battery moved
`6a5cefd2` -> `6d21f535` -> `296ed0d7` (peer integration; this seat made no commit). The landed
counter selftests are green: C1 `27/27`, C2 `40/40`; the pin versions were `23/23` and `32/32`.
All required mutants were run against both the pin and the landed bytes; the kill/survive
pattern is identical, so the tables below use the landed bytes and note the pin counts.

## Commands (exact templates; `$S` = seat scratch, `$R` = lane root)

```sh
S=/fast/scratch/hyaku/mado-r69/R69MutBattery
R=/home/vgpnk/Projects/shokunin/mado-shokunin

# C1 counter selftest (each mutant and the pristine copy)
python3 -I "$S/final/mutants/<mutant>.py" --selftest --scratch-root "$S/final/st/<mutant>"

# C1 counter on the known-good fixture (lane measured content)
python3 -I "$S/final/mutants/<mutant>.py" --repo "$R" \
  --rev 6a5cefd252c41c7ff71217da65126fc831f8bc34 \
  --base-rev 04093b83f73a841117d3b31dbb2a6063f4f2a454 \
  --scratch-root "$S/final/run/<mutant>-lane"

# C1 counter on a fixture repo
python3 -I "$S/final/mutants/<mutant>.py" --repo "$S/fixtures/<fixture>" --rev HEAD \
  --base-rev <fixture-base-sha> --scratch-root "$S/final/run/<mutant>-<fixture>"

# C2 counter (landed); identical shape against the fixtures
python3 -I "$S/current/c2-counter-worktree.py" --repo "$R" \
  --rev 6a5cefd252c41c7ff71217da65126fc831f8bc34 \
  --base-rev 04093b83f73a841117d3b31dbb2a6063f4f2a454 \
  --controls "$R/.ufo/waves/round-69/controls/c2-controls-r69.json" \
  --scratch-root "$S/cur-run/c2-<mutant>-lane"

# Harness recipes: exact byte replace on a scratch copy, then
python3 -I "$S/final/harness/mut-<R1|R2|R3|L>.py" --selftest \
  --scratch-root "$S/final/hst/<recipe>"
```

Every fixture was built with `git -C "$D" init -q`, asserted
`git -C "$D" rev-parse --show-toplevel` == `$D` before the first commit, and committed with
`git -C "$D" -c user.name=mut-battery -c user.email=mut@example.invalid ...`. Fixture shas:
`c1-basekilled` base `7287b18884aeaf3057ff10150b8e9828327f908c`, HEAD
`8ae4108e1804f90bd25901ad9518c343f3d4888a`; `c1-inapplicable` base
`5c89362bbbb3b1953b54b2c7c30abc3f0c700b85`, HEAD
`3b4e40ac98b21822b123df209c2babd07e7967d3`; `c1-red` HEAD
`0e4badf96b35e0e45a885432a291f11429eba079`; `c2-unguarded` base
`96933fdc567084f01461a30046ecce3e0be0d85d`, HEAD
`fc151bb3740f72114ac677d3c633ac031ac30b8b`; `c2-nobase` base
`f8e0ee935cb5055c542e75d153388f2d49292f63`, HEAD
`0b67607cc2ddd64579199c14d61babdd219b12c5`.

## C1 counter kill matrix — landed `9f17a984` (selftest 27/27 green)

A mutant is **killed** iff its own `--selftest` exits nonzero. "Pin" is the same mutant against
`2060da8d` (23 assertions). External effect is measured against a known-good fixture; the lane
fixture is the real repo at the measured content.

| # | Mutant (single point) | Selftest landed | Pin | Killed? | Printed line / exit effect |
|---|---|---|---|---|---|
| a1 | skip the base-rev leg: `base_killed, base_applied = 0, 0` | 25/27 | 21/23 | yes | lane identical (`base=0/3`, MET, rc 0); on `c1-basekilled`: `base=3/3` MISSED rc 1 -> `base=0/3` MET rc 0 |
| a2 | base leg not bound to `--base-rev`: `base_sha = sha` | **27/27** | **23/23** | **no** | lane identical; on `c1-basekilled`: pristine `base=3/3` MISSED rc 1 -> mutant `base=0/3` MET rc 0 (false green) |
| b | count `applicable=no` as killed and applied | 25/27 | 21/23 | yes | lane identical; on `c1-inapplicable`: `killed=2/3 applied=2/3` MISSED rc 1 -> `killed=3/3 applied=3/3` MET rc 0 |
| b2 | count `applicable=no` as killed only (no `applied`) | 26/27 | 22/23 | yes | on `c1-inapplicable`: `killed=2/3 applied=2/3` -> `killed=3/3 applied=2/3`, rc stays 1, verdict stays MISSED (line-only lie) |
| c | count a mutant whose selftest rc is 0 as killed | 19/27 | 16/23 | yes | lane: `killed=3/3 base=0/3` MET rc 0 -> `killed=0/3 base=3/3` MISSED rc 1 (the inversion also scores the base leg) |
| d | accept an unmutated selftest rc != 0 as green (`selftest_rc is not None`) | 24/27 | 20/23 | yes | lane identical; on `c1-red`: `selftest=1 ...` MISSED rc 1 -> `selftest=1 ...` MET rc 0 |
| e1 | drop `applied` from the verdict | 26/27 | 22/23 | yes | lane identical (`killed=3/3 applied=3/3` MET rc 0); `c1-inapplicable` unchanged (`killed=2/3 applied=2/3` MISSED rc 1); test-only kill |
| e2 | drop `applied` from the printed line | rc 2 | rc 2 | yes | no contract line; stderr `c1-r69-paired-recipes.py: emitted contract line does not match CONTRACT_RE`; rc 2 |

Killing assertions (landed): a1 — "a base-leg kill blocks the target" + "base-hurt path exits
1"; b/b2 — "a recipe that does not occur exactly once is not applicable" (b also "inapplicable
path exits 1"); c — the scripted happy-path line and exit assertions plus the survivor case; d —
"a red candidate selftest is not a pass" + "red path exits 1"; e1 — "verdict requires every
recipe applied"; e2 — `CONTRACT_RE` refusal in `measure()` (rc 2, no selftest diagnostic).

**Survivor iff:** only `a2` survives, and only because the selftest's scripted `git show` does
not distinguish the declared base revision from HEAD (R69-MUT-R1). Every other row is killed by
the counter's own selftest on both the landed and the pinned bytes.

## C2 counter kill matrix — landed `85f9e60a` (selftest 40/40 green)

"Pin" is the same mutant against the pre-repair `b6bcec07` (32 assertions).

| # | Mutant (single point) | Selftest landed | Pin | Killed? | Printed line / exit effect (lane `$R` at measured content unless noted) |
|---|---|---|---|---|---|
| a | guard accepted in value position (`mapping_has_key` also accepts KEY inside dict values) | 37/40 | 30/32 | yes | `controls=11/11` MET rc 0 -> `controls=10/11` MISSED rc 1; population `20/13/13/0` unchanged |
| b | dominance clause dropped (any construction counts) | 33/40 | 29/32 | yes | `controls=9/11` MISSED rc 1; population unchanged |
| c | literal-false branch exclusion dropped (`dead = set()`) | 37/40 | 30/32 | yes | `controls=10/11` MISSED rc 1; population unchanged |
| d | population regex widened to `^quality/[^/]+\.py$` | **40/40** | **32/32** | **no** | `population=29 readers=20 guarded=13 unguarded=7` MISSED rc 1 (pristine `20/13/13/0` MET rc 0) |
| e | `unguarded` computed as 0 unconditionally | **40/40** | **32/32** | **no** | lane identical (`unguarded=0` is true there); on `c2-unguarded` (13 readers, 12 guarded): pristine `guarded=12 unguarded=1` MISSED rc 1 -> mutant `guarded=12 unguarded=0` MISSED rc 1 (field lies) |
| f1 | `controls` term dropped from the verdict | 39/40 | 31/32 | yes | lane identical (`controls=11/11`, MET rc 0); no external flip is reachable: `load_controls` pins the frozen sha256 and the 11 cases score 11/11 |
| f2 | `base_controls` term dropped from the verdict | 39/40 | 31/32 | yes | lane identical (`base_controls=7/11`); on `c2-nobase` (base counter absent): `base_controls=0/11` MISSED rc 1 -> `base_controls=0/11` MET rc 0 |

Killing assertions (landed): a — `classify value-position-only` and `the four rejected shapes`;
b — `classify uncalled-helper`, `classify overwritten-env` and the four-shape group; c —
`classify dead-branch-only` and the four-shape group; f1 — "verdict requires every control
correct"; f2 — "verdict requires the frozen base-control score".

**Survivors iff:** `d` survives iff no selftest case exercises `population_at`/`POPULATION_RE`
(R69-MUT-R2); `e` survives iff no case exercises a population with `readers > guarded`
(R69-MUT-R3). Both are caught by a real measurement that changes the denominator or the
reported field, not by the selftest.

## Harness side — three frozen recipes + equivalence probe

Exact copies, each recipe applied once (`occurrences=1` on every artifact), then the artifact's
own `--selftest`:

| Artifact | sha256 | unmutated | R1 | R2 | R3 | L (equivalence probe) |
|---|---|---|---|---|---|---|
| prototype | `f4d138bf...` | 59/59 rc 0 | 57/59 rc 1 | 58/59 rc 1 | 57/59 rc 1 | 59/59 rc 0 |
| draft (now landed) | `9461a059...` | 59/59 rc 0 | 57/59 rc 1 | 58/59 rc 1 | 57/59 rc 1 | 59/59 rc 0 |
| pinned production | `b374cfb8...` | 59/59 rc 0 | 57/59 rc 1 | 58/59 rc 1 | 57/59 rc 1 | 59/59 rc 0 |
| intermediate worktree | `11aa7f89...` | 59/59 rc 0 | 57/59 rc 1 | 58/59 rc 1 | 57/59 rc 1 | 59/59 rc 0 |

**3/3 killed / 1/1 survivor** on every artifact. R1 fails "a crashing M-R child is not a kill
(decision + oracle pair)" and its exit assertion; R2 fails "an M-Z run with no assertion summary
is not a kill"; R3 fails the two live spawn-guard assertions. L (`mz_killed = mz_rc != 0 or
mz_rc is None`) is the declared equivalent mutant and survives at 59/59, as the control receipt
states. The draft file was `89b0cb1c...` at first survey and `9461a059...` when tested (its
owner changed it); the tested bytes were identical before and after this seat's recipe runs.

## Survivors — named residuals

### R69-MUT-R1 — C1 base leg is not bound to `--base-rev`

- Mutant: `c1-a2-base-alias`; landed mutant sha256
  `191ea289d99d0f93e925190711efcce7cd4d59f89e96414ed68bbe971607a2ae`, diff sha256
  `cbe5b9f022159e75e33d14aa1f17f61c6336efe75c8b584eeec7eb007d0f249a`.
  Diff: `-    base_sha = rev_parse(repo, base_rev)` / `+    base_sha = sha`.
- Selftest: 27/27 survive. Lane line unchanged.
- False green: fixture `c1-basekilled` (base commit's `c1-r68-landing-controls.py` slot holds
  the r69 harness; HEAD's slot holds the real r68 harness). Pristine:
  `selftest=0 killed=3/3 applied=3/3 base=3/3 verdict=TARGET_MISSED` rc 1. Mutant:
  `... base=0/3 verdict=TARGET_MET` rc 0.
- Survives iff the selftest's scripted `git show` returns the same bytes regardless of the
  requested revision (it keys on the path, not the rev), so `base_sha` is never asserted.
- One-line flip: key the scripted `git show` on `rev` and add a case where HEAD's r68 slot is
  green while the declared base's r68 slot is red; the current base-hurt case must then stay
  `base=3/3` rc 1.
- Pin-version digest: `dc13284445c3d848761b0b0da8ead71a231ce0d5257a5996c199156c8bc66a09`
  (diff `1f3eb53d2c323a9ace81b1ff5f5bae950163ac302fc66b5e6a645a575840d97f`).

### R69-MUT-R2 — C2 population regex is not pinned by the selftest

- Mutant: `c2-d-population-wide`; landed mutant sha256
  `e57f0b2830fd0ce7ee41f8d4c2058a348daf88c555b62b6e8ef538ada681149f`, diff sha256
  `8c24fdb3ad03c3c830705bbe62610cce7b03734fbf1238e3427810a77b2ca9ff`.
  Diff: `-POPULATION_RE = re.compile(r"^quality/check-[^/]+\.py$")` /
  `+POPULATION_RE = re.compile(r"^quality/[^/]+\.py$")`.
- Selftest: 40/40 survive (it never calls `population_at`; it tests `classify`, `verdict_met`,
  `contract_line`, controls and argument parsing only).
- Measured effect: lane `population=29 readers=20 guarded=13 unguarded=7 ... TARGET_MISSED`
  rc 1, versus pristine `population=20 readers=13 guarded=13 unguarded=0 ... TARGET_MET` rc 0.
- Survives iff no selftest case scripted a `git ls-tree` population. It is caught by the real
  measurement (red, not false-green), so this is a coverage residual, not a false pass.
- One-line flip: add a scripted `ls-tree` output containing `quality/counter-selftest.py` and
  assert `population == 20` (or assert `POPULATION_RE` excludes it).
- Pin-version digest: `844b46ad86401c58da13c7c485b31b5ba9b047a20e0c072d8d13260acfdfd17d`
  (diff `1dadab563ba74e3ac4a658d4299caf606a1c5bd1899ca90cb33d31c10ab956fd`).

### R69-MUT-R3 — C2 `unguarded` is not derived/asserted

- Mutant: `c2-e-unguarded-zero`; landed mutant sha256
  `27452463aa2f75d81d0fdd03adef06802abf9e7b1c372b51034c464573f482d9`, diff sha256
  `cb26827964e469255f9a9fe3e3e904161279df1a7c6ce339f7368b67d9bb39a5`.
  Diff: `-    unguarded = readers - guarded` / `+    unguarded = 0`.
- Selftest: 40/40 survive. Lane line is identical because the lane is genuinely 13/13.
- Reporting effect: fixture `c2-unguarded` (13 readers, 12 guarded) prints
  `guarded=12 unguarded=0` while the true value is 1 (pristine prints `unguarded=1`), rc
  unchanged at 1.
- Survives iff no selftest/measure case exercises a population with `readers > guarded`.
- One-line flip: add a scripted population with 13 readers and 12 guarded and assert the printed
  `unguarded` is 1.
- The frozen verdict cannot be flipped by this mutant (`TARGET_MET` requires `guarded == 13`
  and `readers == 13`, which forces `unguarded == 0`); the residual is reporting integrity, not
  a false green.
- Pin-version digest: `42d2715e6605f3420b6ffb71ef7dcb3593054623705920fc24664f72d80ad965`
  (diff `057cfa92ec5f099d8587146fff703dacf1edca3d293b13e8b9fac282b51560e2`).

## Killed, but only by a test-only assertion or a crash

- **e1 (C1, `applied` in the verdict)**: the selftest kills it with the direct
  `verdict_met(0, 3, 2, 0)` assertion. In `measure()` the counter can only reach `killed == 3`
  through three applied recipes, so `killed == 3` implies `applied == 3`; no fixture line or
  exit changes. Removing that unit assertion would leave an equivalent mutant in the scored
  path.
- **b2 (C1, inapplicable counted killed only)**: the selftest kills it on the inapplicable
  line; in `measure()` the verdict stays MISSED because `applied == 2`. The `applied` term is
  load-bearing for the line, and for the verdict only in the bundled b mutant.
- **f1 (C2, controls term)**: killed by "verdict requires every control correct"; externally
  unobservable because `load_controls` refuses any file whose sha256 differs from the frozen
  digest, so a valid run always scores 11/11. If that digest gate were removed or a re-frozen
  file scored below 11, f1 would be a false green.
- **e2 (C1, `applied` in the printed line)**: killed by `CONTRACT_RE` refusal (rc 2, stderr),
  not by an assertion; no contract line is emitted.
- **c (C1, rc 0 counted as killed)**: the same `mutation_score` scores the base leg, so the
  mutant also prints `base=3/3`; the observed lane line is
  `killed=0/3 applied=3/3 base=3/3 ... TARGET_MISSED` rc 1.

## Restoration evidence

- No production path was written. All mutants are copies under the seat scratch; the lane was
  read with `git show`/file reads only. No `git`/`jj` mutation was run in the lane, the fleet
  repo or any sibling lane; fixture repos were scratch-only and are removed.
- `proto/c1-r69-landing-controls.proto.py` sha256 `f4d138...` before and after the recipe run:
  identical.
- Harness draft tested bytes `9461a059...` before and after the recipe run: identical (the
  file's earlier `89b0cb1c...` state was changed by its owner before the battery; not this
  seat).
- Production harness at the pin `b374cfb8...` and at HEAD `9461a059...`: read-only; the recipe
  runs used scratch copies.
- Landed counters read-only: `9f17a984...` (C1), `85f9e60a...` (C2); pin versions
  `2060da8d...`/`b6bcec07...` read via `git show`.
- Every fixture asserted its own `git rev-parse --show-toplevel` and used the explicit
  `-c user.name/-c user.email` identity; no inherited TMPDIR, no `/tmp`/`/var/tmp` write.

## Scratch cleanup receipt

```sh
rm -rf -- /fast/scratch/hyaku/mado-r69/R69MutBattery
test ! -e /fast/scratch/hyaku/mado-r69/R69MutBattery
```

Verified 2026-11-04T01:57:08Z: `CLEANUP_VERIFIED=yes rc=0`; the seat scratch path is absent.
No other scratch directory was created by this seat.

## Not claimed

No universal fault coverage; not the only possible forgeries; not that these five/six mutants
exhaust the counter's failure modes; not the counters' behaviour on arbitrary Python beyond the
declared one-module/one-hop limits; not that a guarded environment makes the git guard effective
at runtime. The harness's real-children leg remains the harm-watch leg. These findings do not
change the frozen predicates or targets; the survivors are coverage findings.

Report: mado-shokunin/.ufo/waves/round-69/w1/R69MutBattery.md
