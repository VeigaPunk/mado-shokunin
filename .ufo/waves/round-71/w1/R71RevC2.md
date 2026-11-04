# R71RevC2 — adversarial review of claim C2 (operability, four new carrier shapes)

Verdict: **C2 predicate UNSOUND as bounded** — two dominance bypasses live inside the
declared envelope (straight-line code, one hop, exact dotted names, no path sensitivity),
introduced by this round's widening. They flip no frozen case and no production file, so the
scored receipts remain honestly measured (all re-derived below); the defect is in the widened
predicate's dominance clause, which a future set or census reliance would inherit.

Reviewed at scored rev `8e78a4ee82f6ccdc951faf531438178a9d12245e` (base `c354f4d4…`).
`quality/counters/c2-r71-shapes.py` at that rev sha256
`72a0c2a5a268e70bc2f322be10e26557c2c9a2ae67e3b0d051d26db816c4f1d1` (working tree identical);
`quality/counters/c2-r70-carriers.py` byte-identical at base and scored rev
(`f100008df5bff9055cc601ca85c6b09c6b98a74002430dcee01700af090ee81a`), so the diff isolates
exactly the widened rules. Controls file working-tree sha256 matches the frozen
`d7814de8815bb0d4146ceed612ddd3e03029763b7cbf769d868a96ce5cefe7df`.

## Reproduced receipts (all exit codes observed, not copied)

- `python3 -I quality/counters/c2-r71-shapes.py --repo . --rev 8e78a4ee… --base-rev c354f4d4…
  --controls .ufo/waves/round-71/controls/c2-controls-r71.json --scratch-root <scratch>` → rc 0,
  last line `MADO_R71_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0
  controls=23/23 base_controls=19/23 verdict=TARGET_MET rev=8e78a4ee…`.
- Same command at tip `e137b5a4…` → rc 0, identical counts (census re-derived at the tip).
- `git diff --name-only 8e78a4ee e137b5a4 -- quality/` → 0 files (census population unchanged
  since the scored rev).
- r70 harm check at tip: `c2-r70-carriers.py` rc 0, `…GUARD_CARRIERS: population=20 readers=13
  guarded=13 unguarded=0 controls=17/17 base_controls=13/17 TARGET_MET`.
- `--selftest` → rc 0, `MADO_R71_GUARD_SHAPES_SELFTEST: 63/63 assertions passed`.
- Tampered controls (one expectation flipped) → refused rc 2, "controls file sha256 … does not
  match the frozen digest". Held-set assert ran in the canonical run: r70 controls sha256
  `29947b4c…` carried=yes; base counter sha256 `f100008d…` = the held r70 file.
- Per-file census diff: `MADO_R70_READER` vs `MADO_R71_READER` lines over the 20 population
  files sort-identical (13 readers, guard=yes in both) → **the widened classifier reclassifies
  no production file**. Candidate leg has zero `correct=no` lines; base leg `correct=no` is
  exactly {dict-call-splat, dict-call-splat-object-alias, store-through-alias-two-hop,
  attribute-second-object} and both negatives correct on base → base leg 19/23 missing exactly
  the four carriers, as frozen.

Probes below were run by importing the committed counter and calling its `classify` (repro
sources inline; runtime truth = does the handed env mapping carry the key at launch,
straight-line semantics).

## Findings

### F1 — HIGH — shape (b) splat-through-alias: alias rebinding before the splat bypasses dominance (false positive, new in r71)

`splat_aliases` (c2-r71-shapes.py:573-583) records the *first* `m = GUARD` binding with no
binding-count filter and no later-rebind check; `splat_guard_lines`
(c2-r71-shapes.py:638-656) credits `**m` unconditionally once `m` aliases a module mapping.
`carrier_guard`'s rebinding window (`unguarded_rebindings`) only ever tracks the *env-named*
name. Contrast shape (c), whose `alias_store_guard` collects `rebound` for both the alias and
the handed name (c2-r71-shapes.py:826-832) — shape (b) got no equivalent.

Repro (runtime truth: env lacks the key → NOT guarded; classifier: (True, True)):

```python
GUARD = {"GIT_NO_REPLACE_OBJECTS": "1"}
def run(repo):
    m = GUARD
    m = {"LABEL": "x"}                 # alias rebound before the splat
    env = {**os.environ, **m}          # runtime: no key
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
```

r70 classifies the same source (True, False); r71 (True, True) — the widening introduced the
escape. Same result when the rebinding targets a module-level unguarded mapping. This violates
the declaration's C2 rule, which subjects every added shape to the dominance test ("the
guarded environment must reach a `git` launch"): the module mapping's contents never reach the
launch. Not covered by the not-claimed blanket — it is one hop, exact names, no container
flow, no path sensitivity. A rebinding *after* the splat line is harmless (contents already
copied) and correctly credited; only the pre-splat window is false.

### F2 — MEDIUM — shape (d) attribute-through-second-object: the object-alias edge itself is not order-checked (false positive with a live launch, new in r71)

`attribute_flow` collects `object_edges` from all live `X.y = name` assigns with no position
constraint relative to the call (c2-r71-shapes.py:694-702); only the *stores* are
line-ordered. The frozen sentence (d) requires "store-before-use and no-replacement dominance"
and is silent on the edge's position, so the implementation is sentence-faithful — the gap is
in the sentence's dominance clause. Repro with a genuinely executing launch (truth: the
pre-bound `cfg.runner` has no key → NOT guarded; r71: (True, True); r70: (True, False)):

```python
class Box: pass
cfg = Box()
cfg.runner = Box()
cfg.runner.env = {"PATH": "/usr/bin"}
def run(repo):
    runner = Box()
    runner.env = {}
    runner.env["GIT_NO_REPLACE_OBJECTS"] = "1"
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=cfg.runner.env)  # pre-bound object
    cfg.runner = runner                                                        # edge after the call
```

Store (line 8) precedes the use (line 9) per the sentence; the bridge does not exist at the
launch. Edge retargeting is defensively handled (a second `cfg.runner = …` assignment drops
the edge via the count==1 filter — verified, probe B7 rejects), so only the edge-after-use
ordering escapes.

### F3 — LOW (inherited into shape (a)) — function-scoped `global` rebind of the module mapping escapes the bound-once filter

`splat_mapping_names` (c2-r71-shapes.py:559-566) counts only `tree.body` assigns, so a
`def poison(): global GUARD; GUARD = {"LABEL": "x"}` executed before the splat keeps GUARD in
`maps` while the runtime contents changed. Verified for both the held r70 `{**os.environ,
**GUARD}` splat and the new `dict(os.environ, **GUARD)` (both (True, True), truth unguarded).
The r70 half is pre-existing scored behavior outside this round's delta (doctrine: no
interprocedural ordering); the r71 half shows shape (a) inherits it. Residual, disclose.

### F4 — LOW — edge resolution is directional: stores spelled through the edge do not resolve (under-inclusion outside the sentence's spelled direction)

`resolve()` is applied to uses and to replacements, never to store targets
(c2-r71-shapes.py:703-717). `cfg.runner.env["GIT_NO_REPLACE_OBJECTS"] = "1"` (store via the
edge) with launch `env=runner.env` (plain) is not credited though runtime-guarded (probe B12).
The sentence spells store plain / use dotted, so this is within the declared spelling bound;
disclose as a fidelity asymmetry, not a defect.

## Attacks that failed (predicate held)

Over-inclusion probes, all correctly rejected: alias of a mapping mentioning the key in value
position, via `{**m}` and via `dict(**m)` (B5/B5b); splat of a mapping with the key only in a
nested value dict (B6); unrelated second object `other.runner.env` (B13); module mapping
rebound at module level before/after (B2/B2b — a module-bottom rebind executes at import, so
the conservative reject matches runtime truth); dict-call splat then env rebound to an
unguarded dict (B10); attribute store postdating the call (B8). Shape (c) rebinding attacks
are closed: a rebinding of the handed name between alias and store forces a second Dict/dict
binding, which the exactly-once `bind_counts` filter disqualifies (B3 rejects), and between
store and call the `blockers` window blocks (B4 rejects). The frozen negatives hold on both
legs. Keyword-after-splat value override (`dict(**GUARD, GIT_NO_REPLACE_OBJECTS="0")`) counts
as guarded — consistent with the lane's value-agnostic key-position doctrine (r69), not a new
gap.

## Residual limits the round report must disclose

1. Shapes (b)/(d) dominance bypasses above (F1/F2) are invisible to the frozen 23-case set —
   candidate next-set negatives: alias-rebind-before-splat; edge-after-use with pre-bound
   object.
2. Function-scoped `global` rebind of the module mapping (F3) escapes both splat carriers.
3. Key presence is value-agnostic; a later keyword/splat/value can neutralize the setting.
4. Method-call mutations (`.clear()`, `.pop()`) and non-Assign replacements of a guarded
   mapping/attribute are untracked (inherited r70 bound).
5. Cross-method attribute order is source-line order (docstring-disclosed approximation);
   edge position is unordered (F2).
6. `alias_store_guard` is conservative: any second binding of the handed name disqualifies
   (may under-credit); deeper alias chains and non-Name splat operands stay uncovered.

## Scope discipline

Read-only review: no production path written, no git/jj mutation in any repo (fixtures
unnecessary — probes ran against the committed counter via importlib in scratch). No tool
installed or upgraded (none needed; pacman pause respected). Scratch
`/fast/scratch/hyaku/mado-r71/R71RevC2/` (probe outputs, extracted counters, tamper test)
removed after this report.
