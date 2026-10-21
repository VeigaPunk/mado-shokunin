# SourceClosure — S121 proposal: CPython 3.14.8 lexical free-variable resolution and late global lookup (supports C1 F1–F3 only)

All paths are relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`. Raw bodies, response headers and receipts are in `.ufo/waves/round-22/w1/sources/SourceClosure/`. No registry edit, production edit, detector measurement, fixture/payload execution, package query or install was made. Quotes are documentary; nothing below was observed from a running interpreter.

## Verdict

The tagged CPython 3.14.8 language reference supports the truth side of C1 findings **F1, F2 and F3**, plus the module-global late-lookup boundary that separates them. It does **not** support **F4** (scheduled `Thread.run()` / `Timer.run()`) or **F5** (the reserved-key hygiene issue): those need a threading-library source, or are implementation hygiene with no language-reference counterpart. The source supports C1 only. It is not evidence of detector completeness or of complete Python semantics, and it grants no admission.

## Findings

### F1. Tag resolved (observed, high)

```
$ git ls-remote https://github.com/python/cpython.git refs/tags/v3.14.8 'refs/tags/v3.14.8^{}'
992560c2cc62d47b308cec662feb485456847931	refs/tags/v3.14.8
8e6e75d9102e39bed2a2b279203a396741180f12	refs/tags/v3.14.8^{}
```

Saved as `git-ls-remote-v3.14.8.txt` (121 B, sha256 `6549cb7c3492366c3440e8b774e38c2642d153ce3e3f660ac6d8e94b5447d0ac`). This is byte-identical to round-20 SrcPyBuiltins' saved ls-remote, so the tag has not moved.

### F2. Retained bodies (observed, high)

Accessed 2026-10-21T14:19:14Z with `curl 8.23.0 -sS -fL`. All returned HTTP 200 with no redirect (`final_url` equals the request URL).

| file (retained name) | URL | bytes | sha256 | ETag |
|---|---|---|---|---|
| `cpython-3.14.8-Doc-reference-executionmodel.rst` | https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst | 24,445 | `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89` | `e8fc9ff6…6e922` |
| `cpython-3.14.8-Doc-reference-compound_stmts.rst` | https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/compound_stmts.rst | 70,054 | `35e6dfbf2794d367774253655d95b6d5ef91ba63084685624144f2b3945e3e2f` | `c9765e86…b4eb0` |
| `cpython-3.14.8-Doc-reference-simple_stmts.rst` | https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst | 41,375 | `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc` | `54dfdcd8…f253` |

- Peeled-commit cross-check: `…/8e6e75d9102e39bed2a2b279203a396741180f12/Doc/reference/executionmodel.rst` returned HTTP 200, 24,445 B, with the same sha256 `11f99f83…eb89`.
- That digest also equals the anchor of registered **S120** (`corpus/SOURCES.md:132`, executionmodel.rst:240-256, annotation scopes). S121 uses disjoint line ranges (59–161 and 322–329) and teaches a different rule, so it is not a duplicate row.
- `receipts.jsonl` (5 lines, 2,945 B, sha256 `81780b055385838e1a80dff99f25e712ec43605bb419bf30f1b87c44261bff23`) records the URL, HTTP status, byte count, digest, ETag, server `Date`, access time and header digest for each fetch. Headers are retained as `*.rst.headers`: executionmodel `7575fc66…def4`, compound_stmts `df32ffcf…6746`, simple_stmts `51cb091d…ed6b`.

### F3. Located quotes (observed, high)

Every quote is verbatim, located by whitespace-normalised substring match within the stated line range, and at most 25 words.

**Row anchor: `Doc/reference/executionmodel.rst`**

| id | lines | quote | words |
|---|---|---|---|
| Q0 | 59–61 | "The following constructs bind names: * formal parameters to functions," | 9 |
| Q1 | 89–90 | "If a name is bound in a block, it is a local variable of that block, unless declared as :keyword:`nonlocal` or :keyword:`global`." | 22 |
| Q2 | 92–93 | "If a variable is used in a code block but not defined there, it is a :term:`free variable`." | 18 |
| Q3 | 106–108 | "If the definition occurs in a function block, the scope extends to any blocks contained within the defining one," | 19 |
| Q4 | 113–114 | "When a name is used in a code block, it is resolved using the nearest enclosing scope." | 17 |
| Q5 | 127–128 | "all uses of the name within the block are treated as references to the current block." (preceded by "If a name binding operation occurs anywhere within a code block,") | 16 |
| Q6 | 147–148 | "If the nearest enclosing scope for a free variable contains a global statement, the free variable is treated as a global." | 21 |
| Q7 | 160–161 | "The namespace for a module is automatically created the first time a module is imported." | 15 |
| Q8 | 322 | "Name resolution of free variables occurs at runtime, not at compile time." | 12 |

Lines 324–329 hold the reference's own example, which binds module `i = 10`, defines `f` printing `i`, rebinds `i = 42`, then calls `f()`. The documented output is 42.

**Corroboration (retained, not part of the row anchor)**

| id | location | quote | words |
|---|---|---|---|
| Q9 | compound_stmts.rst:1249–1251 | "This function object contains a reference to the current global namespace as the global namespace to be used when the function is called." | 23 |
| Q10 | compound_stmts.rst:1253–1254 | "The function definition does not execute the function body; this gets executed only when the function is called." | 18 |
| Q11 | compound_stmts.rst:1371–1372 | "Free variables used in the nested function can access the local variables of the function containing the def." | 18 |
| Q12 | simple_stmts.rst:974–975 | "free variables may refer to globals without being declared global." | 10 |

### F4. Coverage against round-21 F1–F5 (`.ufo/waves/round-21/residual/FinalBindingReview.md`)

| r21 finding | supported? | basis | confidence |
|---|---|---|---|
| F1: factory arguments bound at invocation time | **Yes** | Q0 and Q1: a factory's formal parameter is a local of the factory block. Q3, Q4 and Q11: a nested closure's free variable resolves to that enclosing function scope. Q10: the closure body runs only when it is called. So the closure reads the factory frame's binding. Rebinding a same-named caller or module name after the factory call does not change what it reads. | high on the rule; the application is [INFERENCE] |
| F2: unbindable factory call resolves the parameter to a module global | **Yes (as a negative)** | Q1, Q3 and Q4: the nearest enclosing scope for that name is the factory, not the module, so resolving it to a module literal is wrong. When the factory-call binding is statically unknown, the reference supplies no observed value. That fits the r21 remedy (unparsed or lead). Q6 is the only route to a global, and it needs a `global` statement in the factory. | high on the rule; [INFERENCE] that a parameter cannot also be declared `global` (not quoted here) |
| F3: returned closure identity taken from the `def`, ignoring a later rebinding | **Yes** | Q0 lists function definitions and assignment targets (lines 61–66) as binding operations. Q5: every use in the block refers to that block's binding. Q8: resolution happens at runtime. So `return name` yields the object bound to `name` when the return runs, which may be a later assignment rather than the `def`. | high on the rule; the application is [INFERENCE] |
| F4: `Thread.run()` / `Timer.run()` not followed | **No** | This is library behaviour of `threading` and is absent from these files. It needs a separate `Doc/library/threading.rst` source. | — |
| F5: reserved key `__mado_thread_target__` shadows a source global | **No** | This is detector-internal namespace hygiene. Q1 and Q4 only say that a source-level name resolves through its own scopes. No language rule names the key. | — |

### F5. A boundary C1 truth authors need (inference from Q8 and lines 324–329, medium-high)

[INFERENCE] The reference makes free-variable resolution *late*, at runtime, in two regimes:

- **Module-global free variables.** These are covered by Q8, the 42 example and Q9. A function that reads a module global sees the global's value when the function is *called*. So an invocation-time environment is *correct* for globals, including a module-level rebinding between the def and the call, and across cells (Q7: a single module namespace).
- **Enclosing-function free variables.** These are covered by Q3, Q4, Q8 and Q11. A closure reads the factory frame's variable when the closure is *invoked*. That frame is fixed by the factory call. The value is the factory local's binding at closure-invocation time: its final value once the factory has returned, or a later value if the factory rebinds it after the `def`.

The r21 checks recommend "snapshot factory-call bindings at closure creation". That matches Python only when the factory does not rebind the captured local after the nested `def`. A frozen variant that does so (`def outer(c): def inner(): run(c); c = other; return inner`) would expect `other`, not the creation-time value. Expectations SHOULD be written from this rule, not from the snapshot heuristic. This sentence is the seat's reading; it was not measured.

### F6. Why one row, anchored on one file

The assignment caps this seat at one proposed id (S121). Per round-20 SrcPyBuiltins F6, one row carries one anchor file and digest, so the anchor is executionmodel.rst alone. Q0–Q8 cover F1–F3 and the global boundary without the other files. compound_stmts.rst and simple_stmts.rst are retained with digests as corroboration only. L1 MAY open them as separate rows; this seat does not number them.

## Proposed row (no registry edit)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S121 | CPython v3.14.8 lexical name resolution, free variables and late global lookup — https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst | spec | A | static truth for C1 r21 F1–F3 (closure free variables resolve to the enclosing factory scope; returned name resolves to the binding in effect; module globals are looked up at call time); not threading (F4), not detector hygiene (F5), not detector completeness or complete Python semantics | tag v3.14.8 → tag object 992560c2cc62d47b308cec662feb485456847931, peeled commit 8e6e75d9102e39bed2a2b279203a396741180f12; Doc/reference/executionmodel.rst 24,445 B sha256 11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89 (same bytes as S120, disjoint lines); :89-90 "If a name is bound in a block, it is a local variable of that block, unless declared as :keyword:`nonlocal` or :keyword:`global`."; :113-114 "When a name is used in a code block, it is resolved using the nearest enclosing scope."; :322 "Name resolution of free variables occurs at runtime, not at compile time."; receipt .ufo/waves/round-22/w1/sources/SourceClosure/receipts.jsonl | a closure's free variable reads the enclosing factory frame's binding at invocation, never a same-named caller or module name; an unbindable factory call yields no observed value; `return name` takes the binding live at return; module globals resolve at call time | queued | 2026-10-21 | on-release | — |

## Re-derivation

```
git ls-remote https://github.com/python/cpython.git refs/tags/v3.14.8 'refs/tags/v3.14.8^{}'
curl -sSfL https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst | sha256sum   # 11f99f83…eb89
curl -sSfL https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/compound_stmts.rst | sha256sum   # 35e6dfbf…3e2f
curl -sSfL https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst | sha256sum     # d4320642…29dc
sed -n '59,61p;89,93p;106,114p;127,128p;147,148p;160,161p;322,329p' cpython-3.14.8-Doc-reference-executionmodel.rst
```

## Unknowns and limits

- F4 and F5 have no source from this seat. F4 needs a `threading.rst` opening (`Thread.run` invokes the target in the calling thread). That is unassigned here.
- [INFERENCE] The parameter-plus-`global` conflict that would close F2's single exception is a compile-time `SyntaxError`. It is not quoted from these files.
- The language reference is normative documentation, not the CPython implementation. No interpreter was run to confirm behaviour, by contract.
- F5's late-binding boundary is this seat's reading and has not been checked against any frozen fixture. Truth authors own the expectations.
- Installs and updates: none. Tools used: `curl 8.23.0`, `git ls-remote`, and `python3 -I` for local digest and quote matching only.
