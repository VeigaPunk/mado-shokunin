# TwMissBashCVar — variable `bash -c` recipes (round 18, wave 1)

Scope: the two admitted tripwire misses in
`/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR14/MadoR14.SourceSafety.jsonl`
lines 152 and 155. Deliverables: a unified diff against
`d9a5a18:tools/mado-tripwire.py`, a synthetic fixture suite, and this report.
Nothing under `tools/` was written; the patch is a draft for L1 to apply/merge.

## Result in one line

Patched copy (`sha256 6ec3eb9af3c98708c42261152ba399c87efb76dc4ae83b76ac451ba5c460e982`)
turns both miss lines into `package_query pacman:-Q` findings while the four
round-17 suites stay **9/9, 16/16, 33/33, 30/30**; the new suite is **15/15**.

## The miss, reproduced from the source of truth

| field | line 152 | line 155 |
|---|---|---|
| `tool_call_id` | `toolu_01DtvHZ7SLzzNUjfsPjSdmDp` | `toolu_01GGG3mRWUrRbBpWdqAQ1fAp` |
| timestamp | `2026-10-20T05:46:07.078Z` | `2026-10-20T05:46:24.897Z` |
| tool / language | `eval`, `py` | `eval`, `py` |
| shape | `recipe = r'''…pacman -Q hyprland wayland-protocols wayland-utils…'''` then `subprocess.run(["bash","-c",recipe], …)` | `recipe2 = recipe.replace(<lit>, <lit>)` then `subprocess.run(["bash","-c",recipe2], …)`; `recipe` was bound by line 152's cell |

Baseline tool `sha256 962919ce…` on a byte-exact 2-line copy
(`/tmp/real2.jsonl`, `sha256 cef8a73df5fdb50acc714db925f87235dfe2c861aad09fa980e818c3c04739b2`):

```
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "exit": 0,
 "files": [{..., "eval_calls": 2, "eval_unparsed": 0, "unparsed_spawns": 2}], "findings": []}
```

Cause: `classify_eval` accepted only `ast.Constant` string arguments and
all-constant lists; an `ast.Name` payload fell through to `unparsed += 1`
(the docstring's stated limit for non-literal spawn arguments). The two cells
were counted, never classified.

Patched tool on the same 2-line file:

```
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 2}, "exit": 1,
 "files": [{..., "eval_calls": 2, "eval_unparsed": 0, "unparsed_spawns": 0}],
 "findings": [line 1 pacman:-Q toolu_01Dt…, line 2 pacman:-Q toolu_01GG…]}
```

Whole-file rescans of `MadoR14.SourceSafety.jsonl` (193 lines), baseline vs
patched, show the change is exactly the two admitted lines:

| | baseline `962919ce…` | patched `6ec3eb9a…` |
|---|---|---|
| label / exit | `findings` / 1 | `findings` / 1 |
| counts | `package_query 5` | `package_query 7` |
| findings | lines 38, 45 (`-Qo`), 45 (`-Ql`), 107, 107 | same five, **plus 152, 155** |
| `unparsed_spawns` | 2 | 0 |
| `eval_unparsed` | 0 | 0 |

No prior finding changed class, rule, line or command text.

## The rule (narrowest sound form)

A spawn payload is classified when, and only when, the text fixes its value:

1. **Fold literal-only expressions exactly** (`literal_value`): a `str`
   constant; a name; `str + str`; a two-argument `str.replace` on already
   resolved strings; a list/tuple of resolved strings. No f-strings,
   `.format`, `%`, `os.environ`, file reads, calls, or concatenation with an
   unresolved operand — those stay `unparsed_spawns`.
2. **A name is eligible only if it is bound one way**: a straight-line
   module-level `name = <expr>` (or annotated `name: T = <expr>`). Any other
   binding form in the cell makes the name permanently ineligible for that
   cell (`module_unsafe_names`): assignments inside `if`/`try`/`for`/`with`,
   tuple/multiple targets, `+=`, walrus, `del`, `import`, `def`/`class` names,
   `global`/`nonlocal`, comprehension targets, `match` capture patterns,
   `type` aliases. A non-literal rebinding drops the name instead of keeping
   a stale value.
3. **Statement order is honoured**: each call uses a snapshot of the module
   environment at its own statement, so use-before-binding and
   spawn-before-rebinding resolve to the right side of the change.
4. **Deferred scopes are not resolved from the module snapshot**
   (`scoped_call_ids`): calls lexically inside a `def`/`async def`/lambda body
   or a class body may run later or in another namespace, so only literals
   written inside the call expression itself are folded there.
5. **The py kernel environment is per transcript file** and carried across
   `eval` cells, because the eval tool documents persistent top-level state
   and line 155 reads a name that line 152 bound. It is invalidated by
   anything that can rebind behind the resolver's back
   (`exec`/`eval`/`globals`/`locals`/`vars`/`__import__`/`compile`/
   `setattr`/`delattr`, `import *`) and by a cell carrying `"reset": true`.
6. Anything not covered stays `unparsed_spawns`; no heuristic string
   searching of unresolved payloads was added. No new classes, rule names or
   permit semantics.

Why the carry is part of the "same text" rule rather than an extra
assumption: 155's payload is `recipe2 = recipe.replace(…)` where `recipe` is
*not* bound in that cell; a same-cell-only rule must either leave 155
unparsed or scan the replacement literals instead of the executed text (the
unsound direction — contradicted by the `replace-removes-command` control).
The carry is a small `scan_file` block (`envs = {}`, `language`/`env`/`reset`
handling, one extra argument); deleting it reverts the patch to in-cell-only
resolution if L1 prefers that trade.

## Fixture suite `.ufo/waves/round-18/drafts/tripwire/r18-bashcvar/`

14 synthetic transcripts, 15 cases, `expected.json` schema
`mado-tripwire-selftest-v1` (same loader as the four existing suites).
`expected.json sha256 a83b7008f82825b71db141968c1ecb0d7abcb6dbfc37fa9770f66a6dd74e2424`.

Positives (fail on the baseline tool):

| case | pins |
|---|---|
| `cell-var-literal` | the 152 shape: literal recipe in a variable, spawned |
| `cell-var-literal-permitted-permit` | same finding, `--permit package_query` → exit 0, label `permitted_only` |
| `cell-replace-keeps-command` | in-cell `str.replace(lit, lit)` chain folding |
| `carry-two-cells` | the 155 shape: binding cell, then replace + spawn cell |
| `list-var` | a whole argv held in a list variable |
| `plus-concat` | `str + str` folding |

Negative controls (must stay `clean`; each is shown able to fail under a
mutant in the next table):

| case | pins |
|---|---|
| `reassign-nonliteral-clean` | later cell rebinds the name to a call result |
| `reassign-conditional-clean` | same-cell conditional reassignment (no straight-line value) |
| `nonliteral-undefined-clean` | payload name never bound |
| `replace-removes-command-clean` | resolution follows the replace **result**, not the base text |
| `function-param-shadow-clean` | the name is a parameter inside a deferred body |
| `exec-clears-carry-clean` | `exec` rebinding invalidates the carried name |
| `reset-clears-carry-clean` | `"reset": true` starts a fresh kernel |
| `js-cell-separate-kernel-clean` | a js cell never feeds the py environment |
| `use-before-binding-clean` | spawn before the assignment in the same cell |

Runs (repo paths, patched tool copy):

```
python3 -I /tmp/applycheck/tools/mado-tripwire.py --selftest .ufo/waves/round-18/drafts/tripwire/r18-bashcvar
SELFTEST_SCRIPT_SHA256: 6ec3eb9a…  SELFTEST_SUMMARY: 15/15 passed failed=[]
```

Same suite against the baseline tool `962919ce…`: **9/15**, failing exactly
the six positive cases with `got=(0, [])` — the clean controls pass
trivially, the positives are what the patch buys.

Mutants (each applied to a copy of the patched tool, suite rerun; the named
negative control fails, so the control is discriminating):

| mutant | failed case |
|---|---|
| remove the unsafe-name filter entirely (fold any literal-bound name) | `reassign-conditional-clean` |
| keep the old value when a rebinding is non-literal | `reassign-nonliteral-clean` |
| return the `replace` base instead of its result | `replace-removes-command-clean` |
| resolve module names inside deferred bodies | `function-param-shadow-clean` |
| ignore `"reset": true` | `reset-clears-carry-clean` |
| ignore the opaque-mutation clear | `exec-clears-carry-clean` |

Additional ad-hoc probes on the patched copy (not in the suite): `match`
capture binding, `del`, top-level `for` target, `+=`, `global` in a def, and
class-body use are all unresolved/`clean`; inline literals inside a function
body are still found; `from os.path import *`, `globals().update({})` and
`del` in a later cell clear the carried name. All 15 ad-hoc probes returned
sane verdicts with no internal error.

## Four existing suites on the patched /tmp copy

`/tmp/applycheck/tools/mado-tripwire.py` = `d9a5a18:tools/mado-tripwire.py`
+ `drafts/TwMissBashCVar.patch`, verified by `git apply --check` in a fresh
`/tmp` repo and `sha256sum` **6ec3eb9a…**.

| suite | result | SELFTEST_SCRIPT_SHA256 |
|---|---|---|
| `.ufo/waves/round-17/tripwire/core` | 9/9 passed | `6ec3eb9a…` |
| `.ufo/waves/round-17/tripwire/compound` | 16/16 passed | `6ec3eb9a…` |
| `.ufo/waves/round-17/tripwire/hardening` | 33/33 passed | `6ec3eb9a…` |
| `.ufo/waves/round-17/tripwire/w2-regressions` | 30/30 passed | `6ec3eb9a…` |

Counter delta beyond the suites' assertions: all 82 round-17 fixture
transcripts scanned file-by-file with both tools (79 scanned, 3 refused as
designed) give **identical findings (91 each)** and identical `eval_unparsed`
(2); the only counter change is
`hardening/eval-nonliteral-unparsed-clean.jsonl` `unparsed_spawns 1 -> 0`
(its `cmd = ['ls']` now resolves exactly and yields no finding). The case
asserts findings only, so it still passes; the round-17 audit note that this
fixture's counter "is 1 today" is superseded.

## Patch facts and apply checks

- `drafts/TwMissBashCVar.patch`, `sha256
  6911e949c72b2b98394238b9cd8b58e1a0f7fd8a26ee27ec13c1e38eb8edd22f`, 1 file,
  8 hunks, **221 insertions / 18 deletions** (`git apply --stat`).
- applies cleanly to `git show d9a5a18:tools/mado-tripwire.py`; the applied
  file hashes to `6ec3eb9a…`, the file every receipt above was measured with.
- also applies (dry run, `patch -p1`) to the current **uncommitted** working
  tree copy (which already carries the `--frozen` patch), at the moment it
  hashed to `c87a31ef…`: hunks 2–8 land with a 9-line offset, no fuzz, no
  rejects. The working tree is being edited concurrently, so re-check
  `sha256sum tools/mado-tripwire.py` before applying.
- no new line exceeds the file's existing 99-column spread (baseline already
  has 9 such lines; this patch adds none).
- `str_list()` is deleted: `literal_value()` subsumes it (all-string
  list/tuple). A sibling patch that edits `str_list` must rebase.
- merge anchors: new helpers sit between `dotted()` and `classify_eval`;
  `classify_eval(code, language, env=None)` gained the optional env; `scan_file`
  gains `envs = {}` before its line loop and the env/reset block in the `eval`
  branch.

## Limits (stated, not hidden)

- Deferred scope calls stay unparsed even when the name is a module literal:
  `recipe = "pacman -Q x"` then `def f(): subprocess.run(["bash","-c",recipe])`
  is `clean` + `unparsed_spawns 1`. The call's value depends on when/if `f`
  runs; this is conservative, not a detection.
- Comprehension targets taint a module name for the whole cell (conservative
  over-approximation).
- The cross-cell carry is justified by the eval tool's documented persistent
  top-level state per transcript. Kernel loss can at most turn a carried
  spawn into a `NameError`; the tool already counts issued calls regardless of
  result (`toolResult` records are ignored by design). `reset` and opaque
  mutation are honoured, but a rebinding through an untracked channel (e.g. a
  C extension mutating globals) would not be seen.
- f-strings, `.format`, `%`, `os.environ`, and file-read payloads remain
  unparsed; installer channels (another round-18 seat) are untouched.
- The patch is **not landed**; no commit records `6ec3eb9a…`. Suite tallies
  here are for the patched `/tmp` copy, not for `HEAD`.

## Integration notes for L1 (receipts hygiene R17-V1/V2, CriticHonesty H5)

- L1's disposition: the fixture suite lives under `drafts/tripwire/` and the
  frozen pin keeps its known misses — i.e. the pin describes the **pre-patch**
  classifier and stays valid only while this patch is unlanded. If it lands,
  re-cut the pin at the landed tool and quote the landed sha. Lines 152/155
  would then change from no finding to `package_query pacman:-Q` (and drop
  their `unparsed_spawns`), so a `known_misses` entry for either line becomes
  `frozen_verdict_mismatch` at that point.
- Every existing receipt that quotes `962919ce…` (four suite tallies,
  adversarial 4/26, round-17 real-transcript scans) is superseded by this
  classifier change and needs a re-cut at the landed revision.
- This work is a harm-watched defect repair, not a claim: `clean` still means
  "no finding in the covered forms", and the two named lines were the only
  delta on the source transcript.

## Files written

- `.ufo/waves/round-18/drafts/TwMissBashCVar.patch`
- `.ufo/waves/round-18/drafts/tripwire/r18-bashcvar/expected.json`
- `.ufo/waves/round-18/drafts/tripwire/r18-bashcvar/*.jsonl` (14 transcripts, listed above)
- `.ufo/waves/round-18/w1/reports/TwMissBashCVar.md` (this report)

Tooling installed or updated: none.

## Relocation by L1

The fixture directory was authored under
`.ufo/waves/round-18/tripwire/r18-bashcvar/`; L1 moved it during integration
to `.ufo/waves/round-18/drafts/tripwire/r18-bashcvar/` ("patches stay drafts
this round", frozen pin keeps the known misses). A restore of the original
path was compared with the drafts copy before deletion: 15/15 files present
on both sides, `sha256sum` lists identical, every file `cmp`-clean. The
restored duplicate was then deleted, and the drafts copy was re-run:
15/15 on the patched tool `6ec3eb9a…`, `expected.json sha256 a83b7008…`.
The original `.ufo/waves/round-18/tripwire/` now holds only the sibling
`frozen/` pin.
