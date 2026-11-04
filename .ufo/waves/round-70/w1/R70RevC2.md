# R70RevC2 — adversarial C2 review

Axes: calibration (C1), operability (C2). Scope: C2 only. Recommendation: **unsound**. The numerical frozen target passes, but the carrier predicate violates its frozen dominance/binding requirements on in-scope inputs. This is a review recommendation, not admission or integration.

## Findings by severity

1. **High: attribute carriers bypass dominance.** `quality/counters/c2-r70-carriers.py:613-622` at the pinned revision gathers every matching attribute store across the AST, then accepts any git call using the same dotted spelling, without checking store-before-use or intervening replacement. `a13-attribute-rebound` and `a14-attribute-guard-after-use` both return `(True, True)` although the launched environment lacks the guard. Both are straight-line, same-scope, one-dotted-name shapes; neither needs path sensitivity or additional alias hops. Frozen rule requires all four carriers to retain dominance. `carrier_guard` immediately returns this result at lines 644-647. Blocker to “sound as bounded.”
2. **High: constant-key resolution ignores local shadowing.** `const_key_names` / `key_is_guard` / `subscript_guard_lines` (lines 533-567) identify module constant names, not the binding visible at the store. `a07b-const-key-local-shadow` sets local `KEY = "OTHER"`, stores under `env[KEY]`, and receives `(True, True)`; held classifier returns `(True, False)`. This contradicts the frozen value-based key rule within one module, one scope and one key store. Blocker to predicate soundness.
3. **Medium: splat and alias scope prose is broader than implementation.** `splat_guard_lines` (594-609) requires `ast.Dict`, so `dict(os.environ, **GUARD)` is missed. `alias_guard_lines` (565-589) requires the source name already be env-named, so `base={}; a=base; a[KEY]="1"; env=base` is missed. These are FNs under broad readings of the frozen “expanded with ** into the env mapping” and “two names bound to the same mapping expression” wording. Do not silently narrow those frozen sentences; disclose the exact implementation limits. The first two findings do not depend on these interpretive issues.

Exact-count success does **not** prove per-file soundness; compensating false positives/negatives could preserve totals. No such compensation was established in the frozen population.

## Reproduction and identities

Pinned instrument revision: `5144a6b5f43225d8021a469f4d24c19558026b9e`; base `b37a5aec4ea03f2223d8e09dd5d386d055c24179`.
Pinned counter SHA256: `87ca466432302feaabf2c504dc131184178afe199d8b84fa492ad3b5211af9f7`.
Held counter SHA256: `53f256f4693526f2c37cced5203c2e1d6007b721c4b6c0d7fa522e165597e929`.
Frozen 17-control SHA256 verified: `29947b4ce5890f5c977f3ec74bafd14ba12b0d581dcb03ef1e3b637017a778ff`.
Held 11-control SHA256: `975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9`.

Run all persisted exact-source attacks, denominator checks and scratch-clone attacks:

```sh
python3 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-70/w1/R70RevC2/reproduce.py
```

Observed runner rc=0 (runner completed; not a soundness verdict). `evidence.json` retains exact argv, rc, stdout and stderr per subprocess. Pinned instrument is a byte-identical snapshot, not production code edits. The lane advanced during review; a first worktree run used an observability-only control-leg-label change. The definitive persisted run executes the pinned blob, not that changing worktree.

## Frozen population and controls

Pinned counting command:

```sh
python3 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-70/w1/R70RevC2/instrument-pinned.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 5144a6b5f43225d8021a469f4d24c19558026b9e --base-rev b37a5aec4ea03f2223d8e09dd5d386d055c24179 --controls /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-70/controls/c2-controls-r70.json --scratch-root /fast/scratch/hyaku/mado-r70/R70RevC2
```

Observed rc=0; last line:

```
MADO_R70_GUARD_CARRIERS: population=20 readers=13 guarded=13 unguarded=0 controls=17/17 base_controls=13/17 verdict=TARGET_MET rev=5144a6b5f43225d8021a469f4d24c19558026b9e
```

Twenty-file table:

```
MADO_R70_READER file=quality/check-anchor-cover.py reader=yes guard=yes
MADO_R70_READER file=quality/check-axis-scores.py reader=yes guard=yes
MADO_R70_READER file=quality/check-control-receipts.py reader=yes guard=yes
MADO_R70_READER file=quality/check-counter-discrimination.py reader=no guard=no
MADO_R70_READER file=quality/check-deliverables.py reader=yes guard=yes
MADO_R70_READER file=quality/check-evidence-pointers.py reader=yes guard=yes
MADO_R70_READER file=quality/check-freeze-order.py reader=yes guard=yes
MADO_R70_READER file=quality/check-index-rows.py reader=yes guard=yes
MADO_R70_READER file=quality/check-index.py reader=yes guard=yes
MADO_R70_READER file=quality/check-landed-contract.py reader=yes guard=yes
MADO_R70_READER file=quality/check-locators.py reader=no guard=no
MADO_R70_READER file=quality/check-population.py reader=no guard=no
MADO_R70_READER file=quality/check-r38-discrimination.py reader=no guard=no
MADO_R70_READER file=quality/check-r55-controls.py reader=no guard=no
MADO_R70_READER file=quality/check-r56-controls.py reader=no guard=no
MADO_R70_READER file=quality/check-round-outcome-first.py reader=yes guard=yes
MADO_R70_READER file=quality/check-session-material.py reader=yes guard=yes
MADO_R70_READER file=quality/check-state-cite.py reader=no guard=no
MADO_R70_READER file=quality/check-tool-ledger.py reader=yes guard=yes
MADO_R70_READER file=quality/check-wave-done.py reader=yes guard=yes
```

Counts are unchanged: population 20; readers/guarded/unguarded = 13/13/0. The base comparison table was produced by round 69, not invented as a round-70 before measurement; `.ufo/waves/round-69/measurement-c2-r69.txt` has identical per-file reader/guard values. Pre-freeze `.ufo/waves/round-70/control-baseline-r70.txt` records held 13/17. Independently rederived held 13/17 and candidate 17/17. All eleven held cases agree with frozen expectations and retain identical name/source/reader/guard fields. Four rejected shapes (`value-position-only`, `dead-branch-only`, `uncalled-helper`, `overwritten-env`) and both git-launch negatives remain `(True, False)` under both classifiers. Only the four positive carrier controls improve relative to held.

A preliminary worktree selftest returned 49/49, rc=0; this is not substituted for pinned measurement evidence.

## Exact attack sources and results

All sources below were fed verbatim to both pinned classifiers. Every source is a reader. TP/FP/FN/TN concern guard classification (TN is a correct negative, not a false positive). Expected fields distinguish bounded coverage from runtime truth. For **each** case reproduce with the runner above; individual source and both outputs are also indexed by name in `attack-sources.json` and `evidence.json`.

### a01-two-hop-alias

Expected under declaration: outside one-hop coverage. Classification: **FN, inside declared limits**.
Observed pinned r70=(True, False); round69=(True, False).

```python
def run(repo):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    a = env
    b = a
    b["GIT_NO_REPLACE_OBJECTS"] = "1"
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
```

### a02-alias-then-env-rebind

Expected under declaration: false. Classification: **TN (correct rejection)**.
Observed pinned r70=(True, False); round69=(True, False).

```python
def run(repo):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    alias = env
    alias["GIT_NO_REPLACE_OBJECTS"] = "1"
    env = {"PATH": "/usr/bin"}
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
```

### a03-attr-different-attribute

Expected under declaration: false. Classification: **TN**.
Observed pinned r70=(True, False); round69=(True, False).

```python
class Runner:
    def __init__(self):
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env["GIT_NO_REPLACE_OBJECTS"] = "1"

    def head(self, repo):
        return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=self.environ)
```

### a04-attr-object-alias

Expected under declaration: outside receiver-alias coverage. Classification: **FN, inside declared limits**.
Observed pinned r70=(True, False); round69=(True, False).

```python
class Runner:
    def __init__(self):
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env["GIT_NO_REPLACE_OBJECTS"] = "1"

    def head(self, repo):
        r = self
        env = r.env
        return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
```

### a05-splat-non-guarded

Expected under declaration: false. Classification: **TN**.
Observed pinned r70=(True, False); round69=(True, False).

```python
OTHER = {"PATH": "/usr/bin"}


def run(repo):
    env = {**os.environ, **OTHER}
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
```

### a06-splat-dict-call

Expected under declaration: true under broad frozen ** wording; display-only implementation. Classification: **FN; scope discrepancy**.
Observed pinned r70=(True, False); round69=(True, False).

```python
GUARD = {"GIT_NO_REPLACE_OBJECTS": "1"}


def run(repo):
    env = dict(os.environ, **GUARD)
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
```

### a07-const-key-rebound-module

Expected under declaration: false. Classification: **TN**.
Observed pinned r70=(True, False); round69=(True, False).

```python
KEY = "GIT_NO_REPLACE_OBJECTS"
KEY = "OTHER"


def run(repo):
    env = {"PATH": "/usr/bin"}
    env[KEY] = "1"
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
```

### a07b-const-key-local-shadow

Expected under declaration: false. Classification: **FP; in-scope constant binding defect**.
Observed pinned r70=(True, True); round69=(True, False).

```python
KEY = "GIT_NO_REPLACE_OBJECTS"


def run(repo):
    KEY = "OTHER"
    env = {"PATH": "/usr/bin"}
    env[KEY] = "1"
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
```

### a08-const-key-value-position

Expected under declaration: false. Classification: **TN**.
Observed pinned r70=(True, False); round69=(True, False).

```python
KEY = "GIT_NO_REPLACE_OBJECTS"


def run(repo):
    env = {"LABEL": KEY}
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
```

### a09-alias-source-not-env-named

Expected under declaration: true under symmetric two-name wording; counter requires env-named source. Classification: **FN; scope discrepancy**.
Observed pinned r70=(True, False); round69=(True, False).

```python
def run(repo):
    base = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    a = base
    a["GIT_NO_REPLACE_OBJECTS"] = "1"
    env = base
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
```

### a10-module-map-mutated-after-splat

Expected under declaration: outside literal-initializer coverage; true after module import. Classification: **FN at runtime, inside declared limits**.
Observed pinned r70=(True, False); round69=(True, False).

```python
GUARD = {"PATH": "/usr/bin"}


def run(repo):
    env = {**os.environ, **GUARD}
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)


GUARD["GIT_NO_REPLACE_OBJECTS"] = "1"
```

### a11-env-substring-name-openvswitch

Expected under declaration: true. Classification: **TP**.
Observed pinned r70=(True, True); round69=(True, True).

```python
def run(repo):
    openvswitch = {"PATH": "/usr/bin"}
    openvswitch["GIT_NO_REPLACE_OBJECTS"] = "1"
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=openvswitch)
```

### a12-splat-local-source

Expected under declaration: outside module-level coverage; runtime true. Classification: **inside declared limits (runtime FN)**.
Observed pinned r70=(True, False); round69=(True, False).

```python
def run(repo):
    guard = {"GIT_NO_REPLACE_OBJECTS": "1"}
    env = {**os.environ, **guard}
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
```

### a13-attribute-rebound

Expected under declaration: false. Classification: **FP; violates frozen dominance**.
Observed pinned r70=(True, True); round69=(True, False).

```python
def run(repo):
    self.env = {}
    self.env["GIT_NO_REPLACE_OBJECTS"] = "1"
    self.env = {}
    return subprocess.run(["git", "show", "HEAD:a"], env=self.env)
```

### a14-attribute-guard-after-use

Expected under declaration: false. Classification: **FP; violates frozen dominance**.
Observed pinned r70=(True, True); round69=(True, False).

```python
def run(repo):
    self.env = {}
    subprocess.run(["git", "show", "HEAD:a"], env=self.env)
    self.env["GIT_NO_REPLACE_OBJECTS"] = "1"
```

## Denominator / verdict attack

- Truncated controls: CLI rc=2, frozen SHA mismatch.
- Renamed case: CLI rc=2, frozen SHA mismatch.
- Sixteen-case controls: CLI rc=2, frozen SHA mismatch (count assertion is additional defense; digest fails first).
- `base_controls=17`: `verdict_met(20,13,13,0,17,17)` returns false; generated line says TARGET_MISSED.
- `controls=16`: `verdict_met(20,13,13,0,16,13)` returns false; generated line says TARGET_MISSED.
- Population 19: actual scratch-clone commit removes nonreader `quality/check-state-cite.py`; CLI rc=1, population=19 readers=13 guarded=13 unguarded=0, TARGET_MISSED.

No required verdict assertion is missing. The regex accepts a *forged* syntactically valid MET/base17 line because it validates format, not arithmetic. This is not the counter's acceptance rule: canonical `measure` derives both receipt verdict and exit status from `verdict_met`. Direct verdict tests are function results, not claimed CLI executions for base17/controls16 scores.

## Held-set guard

`held_check` (lines 727-754) extracts the round-69 JSON at the scored commit; asserts pinned digest, len=11, and name/source/expect_reader/expect_guard identity against the frozen 17 controls. It is called before population scoring in `measure`. Identity is semantic field equality, not independently serialized byte comparison; the digest pins the original bytes.

Scratch clone was checked to have its own exact git toplevel before mutation. Clone was anchored at the pinned instrument revision. Only fixture commits used explicit `user.name=R70RevC2`, `user.email=r70revc2@scratch.invalid`; no lane commits. Appending a newline to held JSON preserves all eleven case identities but breaks its digest; committing it and measuring that commit returned rc=2:

```
c2-r70-carriers.py: held controls sha256 e25d250806a173fafe159ea9462fbaec351fa10bfa2e839ea65774ed6eff8af0 does not match the frozen digest
```

Thus the digest assertion is exercised independently of case identities. Both pinned digests passing makes a divergent identity difficult to construct without changing the instrument; the identity assertion exists, but no digest-bypassed identity-negative experiment is claimed.

## Source grounding

Read primary source: https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/expressions.rst
SHA256 `e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a`.

- Lines 493-518: dictionary-display grammar permits `"**" or_expr`; “Its operand must be a mapping. Each mapping item is added to the new dictionary.” **Sufficient** for display splat as a real carrier. It does not establish dominance, immutability, module constancy, mutation tracking, or argument-to-environment flow. That quote alone does not ground function-call `dict(**GUARD)` syntax.
- Lines 1128-1141 explicitly say the subscript is a single expression/key for mappings and “At runtime, the interpreter will evaluate the primary and the subscript” before calling `__getitem__`/`__class_getitem__`. Lines 1161-1165 say assignment targets call `__setitem__` instead of `__getitem__`. Together **sufficient in substance** for name-valued subscription keys and stores; do not claim the store paragraph alone explicitly states key-expression evaluation. It does not establish that a module constant is still the binding visible at that store (local-shadow attack), or that its value is unchanged.
- Stronger explicit store wording independently read at https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst lines 190-194: “Next, the subscript expression is evaluated. Then, the primary's __setitem__ method is called with two arguments: the subscript and the assigned object.” SHA256 `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`. This is an additional source, not misattributed to expressions.rst.

## Residual limits and verification gaps

Disclose one-hop alias-only coverage, exact dotted-attribute identity (no receiver alias), dict-display-only module-literal splats, no arbitrary mapping mutation tracking, no local splat-source support, env-name substring matching, and no arbitrary Python path or cross-module flow analysis. These limits do not excuse the straight-line dominance or local-shadow FPs above. No universal coverage or saturation inferred from 17/17.

LSP device unavailable: `read xd://lsp` reported “No such tool”; no semantic references/definition/diagnostics service was available. Findings use pinned source inspection plus executable classifier probes, not grep as semantic proof. Canonical runtime identity/rerouting/resume contracts are outside this C2 counter diff and were not exercised. No tools installed; no credentials, desktop, session, compositor, services or package manager probed. Production paths unchanged.

Scratch `/fast/scratch/hyaku/mado-r70/R70RevC2` removed in runner finally; observed `scratch_removed=true`. Production drafts: none. Reproduction artifacts and SHA256 manifest are in the seat directory.

Self-evaluation: accuracy 4 (scope wording ambiguities explicitly separated); completeness 4 (identity-negative protected by digest not bypassed); clarity 4 (long exact-source appendix required); actionability 5 (one-command reproduction and retained receipts); conciseness 4 (all 15 sources retained for exactness). Overall 4.2. Improvements: fix the two in-scope FPs before making a bounded-soundness claim; retain frozen claims while reporting prose/implementation discrepancies. User-agreement check: reproducible evidence outranks numerical success alone.

Report: .ufo/waves/round-70/w1/R70RevC2.md
