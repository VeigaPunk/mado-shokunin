# RevTruthE: round-23 C1 truth attack on two forwarder cases

Seat: MadoR23.RevTruthE (reviewer, leaf). Lane: /home/vgpnk/Projects/shokunin/mado-shokunin.
Reviewed: `repair/expected.json` entries ForwarderPassesCallerArgument (starts line 157) and
ForwarderInvokesFactoryClosure (starts line 174), their fixtures, `repair/truth.py`, `repair/measure.py`.
Classifier at base: `tools/mado-tripwire.py`, sha256 cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84.

## Verdict

| Case | Truth | Pass rule | Base result |
|---|---|---|---|
| ForwarderPassesCallerArgument | truth-correct | neither too loose nor too strict | observed row correct; fails only on a phantom `unparsed 1` |
| ForwarderInvokesFactoryClosure | truth-correct | neither too loose nor too strict | observed row and both forbidden-command guards correct; fails only on a phantom `unparsed 1` |

Guard-level finding, not a case error: the unparsed clause is count-based, and the corpus comparator does not diff
unparsed counters, although `corpus/QUALITY.md:312` says the no-harm requirement covers them (section 4, item 2).

## 1. What I ran

All runs were sequential, one child at a time. No installs or updates. No writes to the lane. Read-only git only.

1. `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/repair/truth.py`
   Exit 0. `passed 12, total 12`, Python 3.14.8, expected sha256 53e34d26... matches.
   ForwarderPassesCallerArgument executed `["pacman -Q r23-forwarded-argument"]`.
   ForwarderInvokesFactoryClosure executed `["pacman -Q r23-closure-captured"]`.
2. `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/repair/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`
   Exit 1. `passed 6, total 12`. tool_sha256 cd9da20c..., helper_sha256 4eb893d2..., expected_sha256 53e34d26...
   Both target cases: `passed false`, `unparsed 1`, rows `[package_query, <command>, observed]`.
   This matches `evidence/repair-before-e33ea304.json` exactly (lines 135-148 and 150-163, totals 6/12).
3. Compile-only symbol tables: `python3 -I -S -c` reads the fixture's first JSON line, then calls
   `symtable.symtable(code, "<fixture>", "exec")`. The fixture code is compiled, never executed. Output is quoted in sections 2 and 3.
4. Read-only checks:
   - Fixture sha256 match expected.json (63041df9... and 7a4c7a2b...).
   - Each fixture is one JSONL record (`grep -c ''` = 1, final byte newline), so truth.py's first-line read is complete.
   - `git show a28e4815:tools/mado-tripwire.py | sha256sum` = cd9da20c...
   - `git merge-base --is-ancestor e33ea304 a28e4815`: true.
   - `git diff e33ea304 a28e4815 -- tools/`: empty.

## 2. ForwarderPassesCallerArgument (kind exact)

Fixture code:

```
import subprocess
def run(actual):
    subprocess.run(actual)
def forward(callback, value):
    callback(value)
forward(run, ["pacman", "-Q", "r23-forwarded-argument"])
```

Python semantics. `forward` calls its parameter `callback` with `value`, the list literal. So `run` receives the list as
its own parameter `actual`. There is no free variable, so the S121 lexical-versus-late-global rule changes nothing here.
Symbol table: `function:run | actual [param, local]`; `function:run | subprocess [global_implicit]`.
Exactly one spawn executes: `pacman -Q r23-forwarded-argument`.

Truth: correct. truth.py passed, and the forbid list is empty.

Rule (measure.py judge, exact clause: rows equal want, `unparsed == 0`, no forbidden command):
- Command: determined by Python.
- Class `package_query`: the tool's own taxonomy. `pacman -Q` maps to package_query (tools/mado-tripwire.py:771-772). Not a Python fact, but the tool's contract.
- Evidence `observed`: the call runs unconditionally with a literal argv. The tool defines rows from followed literal calls as observed and reserves lead for paths that may not run (tools/mado-tripwire.py:43-46).
- `unparsed == 0`: Python executes no non-literal spawn.
- Looseness: any extra row (other command, class, evidence, or a duplicate) fails. Not too loose.
- Strictness: the rule demands nothing beyond Python plus the tool's own taxonomy. Not too strict.

Base failure. Both the observed row and the count were measured. The mechanism is code-path inference, not instrumented:
- `run` is an argument of the followed call `forward(...)`, so eager_calls records a reference whose parent is that Call (tools/mado-tripwire.py:2073, 2081-2083).
- The refs loop in spawn_scan does not skip it. The skips that could apply are the parent "invoke" check and the argument-protocol consumer filter (2687-2702). The pure/value/class parent skip (2723-2732) does not apply to a helper parent. Its kind is helper, so the loop calls `sweep_body(run)` (2742-2744).
- sweep_body treats parameters as unknown (docstring 2365; 2375-2376) and prepares the body with an empty environment (2380). `subprocess.run(actual)` therefore has a non-literal argv, which adds `unparsed += 1` (2677-2686).
- The observed row comes from the followed path `callback(value)` with `actual` bound. The scan emits the right row and a phantom unknown for the same call site.

Verdict: truth-correct. Rule neither too loose nor too strict. Base defect: phantom unparsed count from the sweep.

## 3. ForwarderInvokesFactoryClosure (kind exact)

Fixture code:

```
import subprocess
argv = ["pacman", "-S", "r23-module-foreign"]
def make(argv):
    def run():
        subprocess.run(argv)
    return run
def forward(argv, callback):
    callback()
forward(["pacman", "-S", "r23-forwarder-foreign"], make(["pacman", "-Q", "r23-closure-captured"]))
```

Python semantics. S121 (CPython 3.14.8 executionmodel, enclosing-scope rule and runtime free-variable resolution; corpus/SOURCES.md:133)
says a free variable resolves in the enclosing function scope, at runtime. Symbol table:
- `function:make | argv [param, local]`
- `function:run | argv [free]`
- `function:run | subprocess [global_implicit]`
- `module:top | argv` is a separate global. `function:forward | argv [param, local]` is unused.

`make([... r23-closure-captured])` returns `run`, whose `argv` is the captured list from make's frame. `forward` calls `callback()`,
which runs `subprocess.run` with the captured argv. Exactly one spawn executes: `pacman -Q r23-closure-captured`.

Decoys. `pacman -S r23-module-foreign` runs only if `argv` is read late from the module global, which S121 rules out.
`pacman -S r23-forwarder-foreign` runs only under a forwarder-frame leak. Both are in forbid_any, so the case rejects both
known wrong resolutions.

Truth: correct. truth.py executed exactly `["pacman -Q r23-closure-captured"]` and passed.

Rule: exact clause. Class and evidence follow the same reasoning as section 2; the closure is called unconditionally.
`unparsed == 0` matches Python, which has no unknown spawn. A late-global or frame-leak candidate fails both the row check and forbid_any.
Not too loose, not too strict.

Base failure. The mechanism is code-path inference, not instrumented:
- `make([...])` is a Call argument of the followed `forward(...)` call, recorded as a reference whose parent is that Call (2069-2073).
- The refs loop calls `callable_info(make_call)`, which goes through factory_result (1642-1686). That returns helper `run` carrying closure_env `{argv: pacman -Q r23-closure-captured}` (1675-1685). The loop then calls `sweep_body(run)` (2742-2744).
- sweep_body runs the body with an empty environment (2380). The closure environment is dropped, so `argv` is unknown and `unparsed += 1` (2677-2686).
- The observed row comes from the followed path (`callback()` runs `run` with its closure env).

Verdict: truth-correct. Rule neither too loose nor too strict. Base defect: the same phantom sweep count as section 2.

## 4. Rule-level findings for L1

1. **Count-based unparsed clause.** Both cases can be satisfied by making the phantom disappear, which is also correct for these fixtures. The same clause is satisfied by silencing any unknown spawn, which is not a resolution. Judge candidates by mechanism, not by the count.
2. **Guard gap.** `corpus/QUALITY.md:312` says the original no-harm requirement covers "per-file unparsed counters". `round-21/corpus/compare.py` diffs only findings (the key includes evidence, lines 58-59; Counter diff 104-108) and errors (96-114). It reads `stats` only for sha256/path attribution (87-91). A candidate that drops unparsed counters passes the comparator with zero rows lost or added. The round-21 oracle does require `not unparsed` on every case it scores (`round-21/oracle/measure.py:64`; 35 + 17 cases per the registration), but that is not the corpus. Recommendation: add per-file eval_unparsed and unparsed_spawns before/after to the comparator. Any decrease needs an observed or lead row for the same call site.
3. **Layer mismatch.** The scanner's selftest `eval-nonliteral-unparsed-clean` expects exit 0 (`.ufo/waves/tripwire/hardening/expected.json` lines 157-163), so the scanner's verdict tolerates unparsed spawns. The round-22 audit contract (`.ufo/waves/round-22/audit-contract.json` line 7) requires zero errors (the sum of unparsed counters) before a clean claim. The repair exact clause follows the audit semantics. That is consistent and not too strict, but L1 should know the two layers differ.
4. **Present clause has no unparsed check.** `repair/measure.py` judge: `clean and set(want_present) <= present and not forbidden`. truth.py is the same. Present cases can pass with unresolved spawns. This matters for CallbackStoredInDict and CallbackStoredOnAttribute, which other seats own.
5. **truth.py checks argv sets only.** Class, evidence, unparsed and exit are not checked by truth. The registration's "truth is mechanical" holds for argv only. The class and evidence labels are author judgments that match the tool's taxonomy for these two cases.

## 5. Cross-check: the same branch is the recall path for a present case

CallbackStoredInDict hands `run` on through `register(run)`. Its only base row is the lead `pacman -S r23-hook-dict`
(receipt lines 164-178). [INFERENCE, not instrumented] That lead comes from the same refs-loop sweep (2742-2744), since
sweep_body turns literal spawns into lead rows (2387). So the branch that causes the phantom in sections 2 and 3 is also the
recall path for H5.

Consequence for the fix: removing that branch wholesale would break the present case. A fix has to separate:
- a sweep whose spawn is literal, which must keep its lead row, from
- a sweep whose spawn depends on a parameter or closure value already bound on a followed path, which should not count as unparsed.

Candidate directions, unverified:
- For section 3, pass the factory's closure_env into the sweep. The duplicate lead would be dropped by the observed-row dedupe (2883-2884).
- For section 2, record which callables were already followed with bound literals, and suppress only their unknown-parameter sweep.

Both need corpus review, because a skip can lose leads from branches the followed call did not take. The corpus comparator lists lost rows for adjudication (96-114), so such a loss would surface there.

## 6. Residual risk and gaps

- The base failure mechanism for both cases is code-path inference from reading tools/mado-tripwire.py. I did not instrument the scanner or run it over variants; the contract limits classifier runs to committed fixture data.
- I did not run the other cases, the corpus, or the resource guards. Those belong to other seats.
- The frozen 12 cases could be passed by special-casing their command strings. No guard in the set detects that.
- Base identity: the goal header names a28e4815 as lane head, and the registration names e33ea304 as base. Both have identical tools/ bytes (sha cd9da20c; tools/ diff empty), so the classifier base is unambiguous.

## 7. Verdict line

ForwarderPassesCallerArgument: truth-correct. Rule neither too loose nor too strict. Base fails only on a phantom unparsed count; its observed row is correct.

ForwarderInvokesFactoryClosure: truth-correct. Rule neither too loose nor too strict. Base fails only on a phantom unparsed count; its observed row and both forbidden-command guards are correct.

Guard-level: rule-too-loose on silenced counts, because the corpus comparator does not diff unparsed counters (section 4, item 2).

Installs or updates: none.
