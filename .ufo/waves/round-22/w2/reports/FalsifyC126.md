# FalsifyC126 — CaptureNestedFactory

## Verdict and severity-ordered findings

**Verdict: agree with the sealed, corrected `CaptureNestedFactory` expectation, limited to this exact source shape on delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`.** No actionable current-candidate defect was found for this case. This is author-lane advisory falsification, not non-author review, admission, integration approval, or desktop clearance. Prior r19/r20/r21 rejected-harmed receipts and the rejection streak remain unchanged.

**Informational — original expectation contradiction remains visible.** The original `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureNestedFactory.json:4-12` supplies `r22-nest-inner` in the cell but incorrectly expects `r22-inner` in its row and serialization quote. The original is retained at SHA-256 `0b7a322b81624561f2c3a23a524598d33689645d9589ad4176e4509088d3b53c`; it would not agree with the actual source. The independent pre-seal correction is explicitly recorded at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/reports/CaptureNestedFactory.md:66-76`, and the sealed manifest's `rejected` record preserves the original with reason `ineligible author typo`. The accepted `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureNestedFactoryCorrected.json:4-12` changes that token, not the cell, class, or evidence tier. Agreement below is with that disclosed correction, not a claim that the original erroneous row passed or was normalized from detector output.

## Axes

1. **Semantic fidelity:** preserve the outer `host` cell through the returned `middle` callable and the distinct `pkg` cell through the returned `leaf` callable.
2. **Evidence fidelity:** exactly the complete class/command/evidence multiset, with no invented argv, lost true command, extra lead, duplicate finding, or hidden parse uncertainty.
3. **Identity and containment:** fixed candidate/fixture/runner/expected bytes; one selected scanner child under the runner's 384 MiB/15 s cap; no fixture execution or production mutation.
4. **Claim calibration:** distinguish one-case behavioral agreement from population-integrity checking, family-wide repair, and admission.

## Independent expected result

The sole inert Python cell is in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CaptureNestedFactory.jsonl:1`:

```python
import subprocess


def outer(host):
    def middle(pkg):
        def leaf():
            subprocess.run(["pacman", "-S", host, pkg])
        return leaf
    return middle


outer("r22-nest-outer")("r22-nest-inner")()
```

Reasoning independently of the green result:

- Defining `outer` does not execute its body. Calling it with the first literal binds `host` to `r22-nest-outer`, defines `middle`, and returns that function object. Returning does not destroy the free-variable binding retained by the nested function.
- Calling that returned `middle` binds its separate parameter `pkg` to `r22-nest-inner`, defines `leaf`, and returns the leaf function object. `host` is not a parameter or local rebinding of `middle` or `leaf`; its enclosing-function binding remains reachable. `pkg` resolves to the enclosing `middle` binding.
- The final empty call invokes `leaf`, reaching exactly one `subprocess.run` with argv `["pacman", "-S", "r22-nest-outer", "r22-nest-inner"]`. There is no conditional return, unknown argument, callback, coroutine, scheduling choice, mutation, name rebinding, or competing callable identity in this text. None of the factory definitions itself issues a command.
- `pacman -S` is a host-mutation command, not a package query. The exact static-source contract therefore requires one **observed** row, not a lead and not parsed-clean empty output. This describes a statically followed issuance path; it is not an OS execution observation or proof that a package installation would succeed.

Independent expected complete multiset:

```json
[{"class":"host_mutation","command":"pacman -S r22-nest-outer r22-nest-inner","evidence":"observed"}]
```

Expected counters: `eval_unparsed = 0`, `unparsed_spawns = 0`.

Language-reference support, separate from detector behavior:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-executionmodel.rst:55-63,89-115,322` — parameters bind names; local/free-variable distinction; scope extends into contained blocks unless shadowed; nearest-enclosing-scope and runtime free-variable resolution.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-compound_stmts.rst:1247-1254,1326-1329,1369-1373` — definitions bind function objects without executing their bodies; calls bind parameters; returned nested functions access enclosing locals.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-simple_stmts.rst:494-497` — `return` evaluates its expression and leaves the current call with that value.

Original r21 failure authority remains `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:49-83`. Its old-tool reds were read, not rerun.

## Candidate diff and relevant caller trace

Read the relevant actual diff from base `741122d177ae8ff68a73768777f20484d5bdcbe4` to the delivered revision, restricted to `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`, and traced the current nested-factory path directly:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1726-1783`: `callable_info` resolves the function of a chained call recursively, passing the current environment and resolving stack into `factory_result`. This replaces the old returned-def-name index plus deferred `capture_owner`/`capture_call` representation.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1642-1684`: `factory_result` binds the current factory's arguments, overlays its inherited closure environment/bindings, replays the prefix before the first direct return, resolves the returned value using those bindings, and attaches the resulting closure overlays. For this cell, the first result retains `host`; the second retains that same `host` plus the distinct `pkg`. Both returned identities are the visible `middle` and then `leaf` function objects. No conditional or non-Name return needs to be guessed.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2163-2200,2203-2254,2261-2293`: statement snapshots retain syntactically reachable names and visible callees; the Python cell is compiled with `PyCF_ONLY_AST`, not executed. These snapshots retain the reachable `subprocess` binding needed by the leaf.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2510-2516,2547-2580,2407-2439`: the selected helper's closure overlays are applied before following its body. The leaf has no parameters to overwrite either captured string. Bound literals are preserved for the spawn scan.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1993-2086,2578-2579,2685-2687`: eager calls include the chained factories, but invoke references already accounted for by the followed function expression are skipped. The factories' direct bodies only define/return helpers, so they add no command or extra lead. The measured singleton multiset also confirms no duplicate finding on this exact route.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2623-2643,2675-2684`: the leaf's fully literal argv is serialized with `shlex.join`; an unresolved argv would increment uncertainty instead. The visible-helper `observed` evidence meaning is stated at lines 38-46 of the same source, not inferred as a live process trace.

These are direct static-source conclusions, not LSP semantic proofs. `read xd://lsp` returned `No such tool`; no LSP status, references, definitions, or diagnostics device was available. Literal searches were used only to locate the relevant code, followed by reading the definitions and consumers.

## Authorized measurement and actual rows

Exactly one measurement was executed, with the actual outer argv retained including `-I`:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CaptureNestedFactory
```

The canonical runner selects one exact case at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:789-852`, imports the selected scanner and invokes its `main(["--scan", fixture])` through the isolated child wrapper at lines 34-38 and 655-671. Its child cap is `RLIMIT_AS = 402653184` bytes and timeout 15 seconds (lines 26-27, 643-660). No alternate scanner runtime, original-tool replay, new source-shaped probe, or second scanner run was used.

| Observation | Actual |
|---|---|
| Runner status / exit | `complete` / `0` |
| Selected case totals | `pass: 1`, `total: 1` |
| Scanner exit | `1` — one unpermitted finding, not a runner failure |
| Actual complete rows | exactly the singleton JSON multiset above |
| Finding metadata | `argv0: pacman`, `rule: pacman:-S`, `tool: eval`, `tool_call_id: CaptureNestedFactory-0`, selected fixture line `1` |
| Observed / lead findings | `1` / `0` |
| `eval_unparsed` / `unparsed_spawns` | `0` / `0` |
| Scanner error / comparison reasons | `null` / `[]` |
| Runner stderr / scanner stderr | empty / empty |
| Integrity errors | `[]` |

The scanner-reported fixture path and digest match the selected absolute input. Its other class counts are zero. The raw receipt retains the actual outer argv, exit, stdout, stderr, elapsed time, complete runner JSON, child argv/exit/stdout/stderr, and full scanner payload. The runner's own reconstructed top-level `argv` omits interpreter flags because it is built from `sys.argv`; it is not substituted for the separately captured actual `python3 -I ...` invocation.

The exact-case evaluator at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:683-778` validates the selected file identity and row shapes, rejects parse/output errors, and compares the complete sorted multiset with zero unparsed counters. Consequently the empty forbidden lists do not permit an extra invented observed **or lead** command in this exact case. `accept_exact_want` is `null`; the stored `require_signal: true` does not switch the exact branch to uncertainty acceptance. Unknown-case all-tier prohibitions and `accept_exact_want` handling occur separately in that evaluator and were not behaviorally exercised by this exact-case run.

## Identity and drift

Independent `sha256sum` calls before and after measurement returned identical values; the runner's before/after integrity records agree:

| Artifact (absolute path) | SHA-256, before = after |
|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CaptureNestedFactory.jsonl` | `957b8274336b918f2955e05715a160cc5420e367291f5b61f5ee3bdc3a2a7802` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py` | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |

No detected drift or moving-target substitution. The corrected proposal is pinned at `c24eb08df4d9ceda92105a3f345b648013b055124e94ca3590d27a23524846cc` and its correction report at `428cc0553c03f20d82d230094fdeeecbff968d59208ebf2eda7783722f987474`.

Receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC126/result.json`.

## Residual risk and verification gaps

- This is an eligible exact-result form under `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/supported-forms.md:5-11,20-24`: a plain nested visible factory, literal arguments, and Name returns. No unknown-case downgrade is justified for this cell. The green result agrees with the independently reasoned command, but is not itself the semantics proof.
- The case tests two-level capture propagation and selected callable identity. Because it has no rebinding, creation-time and invocation-time values coincide: it cannot independently distinguish every F1 lifetime bug. It also does not establish correctness for multiple factory instances, deeper/recursive chains, defaults, star/keyword failures, mutable/nonlocal cells, conditional targets, resets, scheduled callbacks, or the original F1-F5 population.
- The runner reports integrity verification of 57 input files, 52 proposal files, and 106 sealed source files before and after. Those are artifact checks, **not 57 scanner cases executed or 57 semantic successes**. Behavioral denominator here is exactly one. No saturation or family-wide repair claim follows.
- LSP verification was unavailable as recorded above. An initial top-level JSON read over-returned unrelated manifest metadata; subsequent expectation analysis and the sole scanner execution were restricted to `CaptureNestedFactory`.
- No fixture payload or printed command was executed. No full suite, build, lint, formatter, generic smoke, live probe, package query/install/update, mutation test, or production/fixture/expected/source edit was performed. No tools were installed or updated. Only this report and the assigned raw receipt were written.

**Recommendation:** retain this result as one bounded agreement with the disclosed corrected truth. It provides no admission grant and does not erase prior red authority.
