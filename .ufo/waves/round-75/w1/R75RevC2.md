# R75RevC2 — C2 adversarial review

C2: survives with defects

The frozen numerical claim reproduces. Both new P2 counterexamples below were independently re-probed and are closed at repair commit `e3e29bb4bf0456f768c9839562d2db3437605b83`; the advisory fixture/model limits remain. This is a review recommendation, not admission or approval.

Axes: guard precision, guard recall, frozen-label validity, census reproducibility, and no mutation of the lane.

## Repair re-probe

Imported the committed repaired classifier extracted with `git show e3e29bb4:quality/counters/c2-r75-shapes.py`. Observed positional-metadata `(True, False)`, literal-dead delete `(True, True)`, and live delete `(True, False)`, all matching their expected classifications. Evidence: `repair-receipt.txt`. Source inspection confirms `usage_lines` now requires `env=` for the git-call branch and the new cancellation collector filters the supplied dead-line set. The two P2 findings below describe the original freeze revision and are **resolved for these witnesses**, not outstanding repair findings. The L1 reported unchanged full frozen scores at `79a4ff7b`; this seat did not independently rerun the full counter at that later revision. Earlier census/control evidence below remains explicitly tied to `def73656`.


## Original-freeze findings, by severity

### P1

None established in this bounded instrument review.

### P2 — name-neutral bindings can be credited without ever reaching `env=`

**Location:** `quality/counters/c2-r75-shapes.py:346-358`, `:410-423`, `:524-533` at `def73656c94f0e88bd671cfb4a65124338261722`.

The new branch recognizes `child` as a guard carrier, but the existing `usage_lines` accepts **any positional argument** at a call containing a git argv, not just the `env=` argument or a verified forwarding parameter. This extends the accepted population beyond the frozen sentence's explicit `env=` restriction.

```python
def wrapper(argv, metadata):
    return subprocess.run(argv)
def run():
    child = dict(GIT_NO_REPLACE_OBJECTS="1")
    wrapper(["git", "show", "HEAD:a"], child)
```

Observed held `(reader=True, guard=False)`; successor `(True, True)`. Executing the functions with a recording subprocess object produces one launch **without `env`**. The helper's `metadata` is ignored. The direct `subprocess.run(argv, child)` spelling is likewise over-credited, but the valid wrapper example is the stronger separator. The early `call_is_git` branch bypasses `_matched_env_params` and `callee_passes_param_to_git` entirely.

**Action:** require actual `env=` transport, or verified local forwarding, before crediting a name-neutral guard; add this negative as a future control without changing the frozen 47.

### P2 — a literal-dead deletion cancels a live guard (regression)

**Location:** `quality/counters/c2-r75-shapes.py:389-406`, consumers `:448-456`, `:523-532`, `:930-938`.

The new delete collector does not receive/filter `dead` lines, unlike `guard_construction_lines`. A delete under `if False` therefore invalidates a live binding solely because its line number is between construction and use.

```python
def run():
    env = dict(GIT_NO_REPLACE_OBJECTS="1")
    if False:
        del env["GIT_NO_REPLACE_OBJECTS"]
    subprocess.run(["git", "show", "HEAD:a"], env=env)
```

Observed held `(True, True)`; successor `(True, False)`. Independent Python execution records `env` carrying the key with value `"1"`. This is not merely unknown dynamic control flow: `false_guarded_lines` already identifies the literal-dead block, and the frozen `dead-branch-only` control relies on that distinction. No frozen case tests a dead cancellation.

**Action:** exclude literal-dead deletions when collecting cancellations in all dominance paths.

### Advisory — one frozen positive never reaches a launch

**Location:** `.ufo/waves/round-75/controls/c2-cases-r75.json:282-285` (`del-before-store`).

The fixture first constructs `env = {"PATH": "/usr/bin"}`, then deletes the absent guard key, then stores it. Both classifiers return `(True, True)` and agree with the positive label. Independent execution instead raises `KeyError: 'GIT_NO_REPLACE_OBJECTS'` with **zero launches**. The label is consistent with the declared syntactic rule "delete before store cancels nothing", but is not a valid runtime positive witnessing that rule. Thus 47/47 is label agreement, not proof of 47 runnable, correctly guarded launch scenarios. Preserve the frozen set; use a separately versioned, executable delete-before-store witness with the key initially present.

### Advisory — inherited cancellation scope and mapping-identity gaps remain

**Locations:** `quality/counters/c2-r75-shapes.py:1240-1246`, `:1275-1278` (inherited unchanged); `:400-406` (new plain-name cancellation).

An uncalled nested `def unrelated(env): del env[KEY]` between an outer `env = os.environ; env[KEY] = "1"` and `env=dict(env)` launch cancels the outer store in `environ_alias_guard`: the collector walks the entire AST and indexes only by spelling. Both held and successor return `(True, False)`, while independent execution records the guard. In contrast, a direct child mapping's nested-local delete is correctly excluded by `scoped_nodes`; not every cancellation path shares that protection. This is inherited, not a new round-75 regression, but qualifies the stated "same scope only" boundary.

Also observed: `child = dict(GIT_NO_REPLACE_OBJECTS="1"); env = child; del env[KEY]; launch(env=child)` yields successor `(True, True)` although the recording launch receives no guard key. The new cancellation tracks the deleted spelling, not mapping identity. Treat this as a residual bounded-model limitation rather than evidence that the frozen score failed.

## Exercised evidence

- Read the frozen declaration, baseline receipt, candidate receipt, all 47 case sources/labels, the actual held-to-successor textual delta, and the construction/usage/cancellation dominance paths.
- Extracted the committed successor with `git show def73656c94f0e88bd671cfb4a65124338261722:quality/counters/c2-r75-shapes.py` into the seat scratch; SHA-256 `dd9a9a9ae90dce1628bb29af86c61a807ee25bf3bce25952254d564b7dc054f1`.
- Extracted controls hash matched frozen `d99502ba23e969a981a856a06742d8da14e1684850c7ca0e0900cd2dc7767897`.
- Ran the exact frozen counter once with explicit `--repo`, `--rev def73656c94f0e88bd671cfb4a65124338261722`, `--base-rev b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6`, frozen `--controls`, and seat `--scratch-root`. Exit 0; all 47 candidate and 47 held per-case legs inspected. Candidate 47/47; held 41/47, missing exactly four copy positives and two live-delete negatives. Exact terminal line is transcribed in `counter-result.txt`.
- Independently imported that extracted committed counter, imported the held classifier from the base revision, and re-derived two positives (`copy-dict-kw-bound`, `copy-splat-bound`) and two negatives (`copy-dict-value-position`, `del-env-literal-cancel`). Additionally executed those four source snippets in Python with a recording subprocess object and isolated fake `os.environ`: positives hand key `"1"` as `env=`, negatives hand an `env=` mapping without the key. Receipt: `targeted-receipt.txt`.
- Independent population enumeration used `git ls-tree -r --name-only REV -- quality`, filtering direct-child filenames beginning `check-` and ending `.py`, without reusing the counter regex. Reclassified every resulting source extracted at the freeze revision. Result **20 population, 13 readers, 13 guarded, 0 unguarded**. Set difference versus `population_at` was empty; every per-file classification matched the committed receipt. No differently inspected file found.
- Readers/guarded: `check-anchor-cover.py`, `check-axis-scores.py`, `check-control-receipts.py`, `check-deliverables.py`, `check-evidence-pointers.py`, `check-freeze-order.py`, `check-index-rows.py`, `check-index.py`, `check-landed-contract.py`, `check-round-outcome-first.py`, `check-session-material.py`, `check-tool-ledger.py`, `check-wave-done.py` (all under `quality/`).
- Nonreaders: `check-counter-discrimination.py`, `check-locators.py`, `check-population.py`, `check-r38-discrimination.py`, `check-r55-controls.py`, `check-r56-controls.py`, `check-state-cite.py` (same directory).

## Residual risk and verification gaps

- `xd://lsp` returned **No such tool**; no language-server device/server was available for status, references, definition, or diagnostics. Source inspection and executable witnesses are fallback evidence, not semantic-reference proof.
- No production commands were launched by adversarial snippets: recording substitutes observe Python argument/mapping transport, not Git behavior. No fleet gate or broader selftest was run; this seat was assigned the frozen C2 counter and bounded adversarial executions only.
- Numerical saturation is honest only for this frozen label set. The two P2 witnesses show that it must not be generalized to saturation of guard precision or recall across Python idioms.
- One canonical frozen C2 implementation was imported and exercised; no alternative runtime, rerouting, resume path, integration, judgment, or shipping action was attempted. No tools installed or upgraded. No git/jj write commands used. Scratch removed after preserving receipts/scripts under this seat directory.

Self-evaluation: accuracy 4 (runtime observations use recording substitutes); completeness 4 (bounded classifier review, not full Python flow analysis); clarity 4 (finite score separated from generalized defects); actionability 4 (exact witnesses and branch locations, no edits permitted); conciseness 4 (full evidence retained for the requested thorough review). Overall 4.0. Highest-impact improvement is adding the two new separators to a future control generation, not rewriting this frozen evidence. The user should agree this is a bounded falsification attempt, not an approval.
