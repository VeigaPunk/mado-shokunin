# FalsifyC122 — C1 CaptureKwargs

## Findings by severity / verdict

**Verdict: agree, limited to the sealed CaptureKwargs case on the assigned C1 bytes. No actionable defect found in this case.** This is an author-lane advisory result, not non-author admission, integration approval, host clearance, or a change to the prior r19/r20/r21 rejected-harmed receipts or streak. L1 retains planner/integration authority.

Axes: (1) independent semantic truth and complete class/command/evidence multiplicity; (2) creation-time argument lifetime and returned callable identity; (3) honest uncertainty/error accounting; (4) immutable artifact identity and bounded, single-case execution.

Delivered target: `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, with selected tool SHA-256 `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce`. I reviewed the relevant actual tool diff from registered baseline `741122d177ae8ff68a73768777f20484d5bdcbe4` to that delivery, the current relevant source paths, the original proposal, retained citation, and original F1 red. No old-tool rerun was performed.

## Independent semantic result

The inert source is retained verbatim at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CaptureKwargs.jsonl:1`; the original independent proposal is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureKwargs.json:2-18`. The sealed case at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json:1155-1212` is exact, has no correction or addendum, and preserves the original single desired row.

The retained Python reference states that a `**identifier` parameter receives a **new ordered mapping** of excess keyword arguments: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-compound_stmts.rst:1326-1336`.

Independently of scanner output:

1. At `runner = make(**spec)`, `spec` names the first literal mapping. Its string key `argv` supplies the list `["pacman", "-S", "r22-kwargs-a"]` to the newly created local `kw` mapping. There are no missing arguments, duplicate keywords, non-string keys, or unresolved expansions.
2. `make` defines and returns its one `run` function. `kw` is the enclosing function's captured local, not a later lookup of the module name `spec`.
3. The following `spec = {"argv": ["pacman", "-Q", "r22-kwargs-b"]}` rebinds only the module name. It neither mutates the captured mapping nor its list. The new mapping does not retarget the closure.
4. The sole `runner()` invocation reaches the sole `subprocess.run(kw["argv"])` call with the original `-S` list. Under the scanner's static evidence contract, that is exactly one **observed host_mutation**, command **`pacman -S r22-kwargs-a`**. It is not a runtime claim that package installation occurred; the fixture was never executed.

There is no conditional return, alternative callable, scheduler, cancellation, nonlocal mutation, or opaque value in this text. A lead-only answer or parsed-clean empty answer would lose a true command. `pacman -Q r22-kwargs-b` is not an executed command at any tier. Although its explicit case exclusion names only observed evidence, the exact complete-multiset requirement also rejects that command as an extra lead.

`accept_exact_want` is null: this is not an uncertainty case accepting either an exact answer or an uncertainty signal. The sealed default `require_signal: true` does not weaken or contradict exact comparison; the canonical exact branch returns on complete row equality and zero unparsed counters before the uncertain-case signal branch: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:736-767`.

## Relevant repair and caller review

The actual diff replaces retained `capture_owner`/`capture_call` replay at invocation with creation-time `factory_result`, and adds literal dictionary subscript resolution. The old wrong-command finding remains authoritative at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:55,70-76`; this case is a bounded `**kwargs` variant of that F1 lifetime failure, not a new measurement of the original red.

Current source agrees with the independent trace:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2203-2254` processes statements in order and updates literal/binding state after each statement. Assignment classification is stored by `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1928-1937`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1774-1783,1839-1861` routes helper-valued calls into factory-result resolution. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1642-1684` binds arguments at that boundary, resolves the returned function in its local frame, and retains its lexical overlay.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2120-2145` creates the excess-keyword mapping and binds it under the factory's `kw` parameter. The original `argv` list is retained; the later module rebinding does not rewrite this stored mapping.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2510-2516,2564-2579` applies the stored closure frame before following the resolved helper. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2407-2439` follows the zero-argument returned helper with bound state. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1361-1367` resolves its `kw["argv"]` to the captured list.

The canonical unresolved/invalid distinction remains explicit at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1629-1656,2459-2466`; this fully literal valid call does not require either path. I found no case-specific wrong identity, false observed/lead argv, stale capture, missing true command, or parsed-clean ambiguity.

## Authorized measurement and actual rows

Executed exactly once:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CaptureKwargs
```

The runner's canonical selection and scan loop are `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:789-851`. Its one scanner child used `/usr/bin/python3 -I -c <fixed import wrapper> <assigned tool> <assigned fixture>`, with `RLIMIT_AS = 402653184` bytes and a 15-second timeout enforced by `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:643-661`. No alternate tool, rerouting, extra scanner run, fixture execution, or new source-shaped probe was used.

Actual complete finding multiset:

| Class | Command | Evidence | Multiplicity |
|---|---|---|---:|
| host_mutation | `pacman -S r22-kwargs-a` | observed | 1 |

No other observed or lead rows were returned. Scanner counts: host_mutation 1; package_query, live_probe, tool_install, and vcs_write all 0. The single file row identified the exact absolute CaptureKwargs fixture and its sealed digest, with `eval_calls: 1`, `bash_calls: 0`, `eval_unparsed: 0`, and `unparsed_spawns: 0`.

Runner exit **0**, status `complete`, totals **1/1 pass**, reasons `[]`, integrity errors `[]`. Scanner child exit **1** means findings, not a scan failure; its output began `MADO_TRIPWIRE: findings`. Both runner and scanner stderr were empty, and `scanner_error` was null. The canonical output parser verifies fixture identity and both error counters at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:683-729`.

The runner integrity checks verified 57 input files, 52 proposal files, and 106 sealed source files before and after. **Only CaptureKwargs was scanned**; 57 validated files are not 57 measured cases.

Full outer/child argv, exits, stdout, stderr, scanner payload, integrity snapshots, and before/after hashes are retained at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC122/result.json`.

## Artifact identity

All following hashes were unchanged immediately before/after the measurement; receipt `hash_drift` is `{}`.

| Artifact | SHA-256 |
|---|---|
| Assigned C1 tool | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| CaptureKwargs fixture | `42b5ec3c254c55a39d40e3334321fa64da22397899e3bbcf9f6c1583fba1c2b4` |
| Oracle runner | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| Oracle expected manifest | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| Original CaptureKwargs proposal | `d817063b2878e728ba2190ab08f97cc3c65b3510d35ba1b1a3735e2da55706a6` |
| Retained compound-statements citation | `35e6dfbf2794d367774253655d95b6d5ef91ba63084685624144f2b3945e3e2f` |

## Residual risk and verification gaps

- This one finite exact case supports literal `**kwargs` capture across a module-name rebinding. It does not establish all Python closure semantics, arbitrary alias mutation, scheduled/conditional targets, complete C1-family repair, C2 arithmetic capability, whole-population no-harm, resource scaling, or saturation. The observed result agrees with independent semantic reasoning; green alone is not the proof.
- `xd://lsp` was attempted before text source searches; it returned **No such tool**, so no answering server, semantic references, definitions, or diagnostics were available. Source-range and diff review were the literal fallback, not LSP semantic proof.
- No resume path is involved in this scanner case; no `resume_continuity_v1` claim was assessed. No other runtime was invoked.
- Only the assigned report and own receipt were written. No production, fixture, expected, source, gate, registry, shared checkout configuration, or historical receipt was edited. No installs, background jobs, builds, linters, formatters, full-suite tests, generic smokes, or live/package probes were performed.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC122.md
