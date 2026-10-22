# RevTruthD: C1 truth attack on NestedDefReadsDefiningFrame and LateGlobalRebinding

Scope: frozen repair truth in `repair/expected.json` for two overcorrection guards. Read-only. The only lane write is this report. No git or jj commands, no subagents, no installs.

## Verdicts

| Case | Frozen expectation | Python truth (argv that executes) | Base (e33ea304) | Verdict |
|---|---|---|---|---|
| NestedDefReadsDefiningFrame | exact: one `package_query` / `pacman -Q r23-nested-local` / observed row; forbid `pacman -S r23-nested-foreign` | Exactly one run: `pacman -Q r23-nested-local`. `inner` reads `argv` as a free variable (`LOAD_DEREF`) from `outer`'s parameter cell. The module-level foreign `argv` is never read. | passed; rows identical to the before receipt | **truth-correct.** Pass rule: argv expectation correct and not too strict. **Rule-too-loose** for the adjacent S121 property that enclosing cells are read late (F1). |
| LateGlobalRebinding | exact: one `package_query` / `pacman -Q r23-late-global` / observed row; forbid `pacman -S r23-early-global` | Exactly one run: `pacman -Q r23-late-global`. `helper` reads global `argv` at call time (`LOAD_GLOBAL`), and `caller()` runs after the second module binding. | passed; rows identical | **truth-correct.** Pass rule neither too loose nor too strict for its stated property (late global read). |

No truth-wrong finding. No rule-too-strict finding for either case. Both cases already pass at base, so they are no-regression guards, not repair targets. Their base row sets do not change the 6/12 count.

## Commands run and outputs

1. `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/repair/truth.py` (run once; an earlier bash call was rejected by the tool wrapper before anything ran). Output: `passed 12, total 12`, python 3.14.8, expected_sha256 `53e34d2691f1a456ce6a4387795c84e5a55d3449b94245d68de516023187c6b9`. Executed argv: NestedDef `["pacman -Q r23-nested-local"]`; LateGlobal `["pacman -Q r23-late-global"]`. Exit 0.
2. `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/repair/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` (run once). Output: `passed 6, total 12`, exit 1 (driven by the six other failing cases, no error), tool_sha256 `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`, helper_sha256 `4eb893d2337a4aa758d14c064a855032737c6e2b2b1239d7ca3502042c6c82da`. NestedDef: passed true, unparsed 0, exit 1, error null, rows `[package_query, pacman -Q r23-nested-local, observed]`. LateGlobal: passed true, unparsed 0, exit 1, error null, rows `[package_query, pacman -Q r23-late-global, observed]`. This matches `evidence/repair-before-e33ea304.json` (entries at lines 104-134) field for field.
3. `sha256sum` and `wc -lc` on the two fixtures. NestedDef: `ac38b6f3088edf3469800e571bb2a8dd4dd1def5e505a64899ccfb9d079dbe0b`, 407 B, 1 line. LateGlobal: `1141e4750e420855abd0f08eea0e0790389c9af11779227a9f92c8205d44f116`, 397 B, 1 line. Both equal the sha256 fields in `expected.json`. Each file holds one record, so truth.py's first-line read covers all content.
4. S121 source: `sha256sum .ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-executionmodel.rst` gives `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89`, equal to the `corpus/SOURCES.md` S121 row (line 133). Read lines 89-114 (enclosing-scope resolution) and 318-330 ("Name resolution of free variables occurs at runtime, not at compile time"; the `i = 10`, rebind to 42, `f()` example).
5. Static compile-only probe, `python3 -I -c` using `symtable` and `dis`. Nothing is executed (`compile` and `symtable` only parse). NestedDef: in `outer`, `argv` is a parameter and a cell (`MAKE_CELL`, `LOAD_FAST_BORROW`); in `outer/inner`, `argv` is free and read by `LOAD_DEREF`. LateGlobal: in `helper`, `argv` is an implicit global read by `LOAD_GLOBAL`; the module has two `STORE_NAME argv`, and the second precedes `caller()`.
6. Authored variant, not committed and not run through the scanner. Code: `def outer(argv)` defines `inner` reading `argv`, then rebinds `argv = ["pacman","-Q","r23-rebound-late"]` inside `outer` after the def, and returns `inner`. Called with `["pacman","-S","r23-rebound-early"]`, then `job()`. Run only through a recording fake-`subprocess` child (`python3 -I -S -c`, same shape as truth.py's CHILD). Output: `["pacman -Q r23-rebound-late"]`.
7. Static print (no execution) of all 12 frozen fixture bodies, used for the coverage reading in F1 and F5.
8. Reads: `tools/mado-tripwire.py` lines 1-63 (docstring: "Issued is not executed", line 30-31; observed means a followed visible literal call path, lines 38-46; lead means swept or unfollowed, lines 47-63), 771-772 (letter Q maps to package_query), 2911-2916 (`verdict_of`), 3396-3399 (permit empty unless given). `.ufo/waves/round-21/oracle/measure.py` WRAPPER calls `--scan` with no `--permit`.

Installs and updates: none. No pacman, no uv, no package changes, no host change.

## Findings by severity

**F1 (medium). The frozen 12 cannot tell a late enclosing-cell read from a def-time snapshot of enclosing locals.**
- I read all 12 bodies (command 7). None rebinds a name in an enclosing function after a nested def captures it. A resolver that copies enclosing-function locals at def time would therefore give the same executed argv as Python on all 12. [INFERENCE from code reading; not run against the scanner.]
- Python does not do that. The authored variant (command 6) executes `pacman -Q r23-rebound-late`. A snapshot resolver would execute `pacman -S r23-rebound-early`.
- The S121 corpus note states this rule: `corpus/knowledge/tripwire-lifetime-recovery-r22.md` row 14 ("the closure reads that enclosing cell's later binding").
- Effect: NestedDefReadsDefiningFrame does not guard the late-cell property, and the 12/12 claim does not cover it.
- Recommendation for L1, who decides: do not edit `expected.json` in place, since its SHA is pinned. Either name the limit in the C1 claim, or add one append-only pinned case (the variant above), with exact row `package_query / pacman -Q r23-rebound-late / observed` and forbid `pacman -S r23-rebound-early`, before any candidate is measured. Not measured here.

**F2 (low). truth.py checks argv only.** The exact branch compares sorted `command` strings. `class` and `evidence` in `want` are never read. The registration's "Truth is mechanical" holds for argv only. Here class `package_query` (tools/mado-tripwire.py:771-772) and evidence `observed` (docstring, lines 38-46) agree with Python, but they are the tool's own taxonomy, not oracle output.

**F3 (low). The exit-code clause is looser than the tool's own verdict.** measure.py accepts exit in (0, 1) for every case. The helper runs `--scan` with no permit, so the permit set is empty, and `verdict_of` (2911-2916) returns 1 whenever any finding exists. A tool that emits these exact rows with exit 0 would be internally inconsistent yet pass. No effect on the base (exit 1). Recommendation: for exact cases with a non-empty want, require exit 1.

**F4 (info). The `forbid_any` clause is redundant for exact cases.** Equality already excludes any row not in `want`, so the clause adds nothing. Harmless.

**F5 (info). The pair does not separate lexical from dynamic scope.** A caller-frame resolver passes LateGlobalRebinding, because `caller()` binds no `argv`. It also passes NestedDef when resolved from the immediate caller `outer`, where `argv` is the parameter. NestedDef fails only when resolved from the module frame. Dynamic-scope errors are caught by other cases: CallerLocalShadowsHelperGlobal (caller's local `argv` is foreign) and ForwarderInvokesCallback (`forward`'s parameter `argv` is foreign). Do not read these two cases as dynamic-scope discriminators.

**F6 (info, unverified). Namespace assumption.** truth.py treats the eval cell as one namespace. A def or async wrapper would not change either verdict, since both reads are closures and late-binding. A split globals/locals exec would raise NameError and execute nothing. I did not inspect the eval kernel's exec implementation. [INFERENCE]

## Residual risk and verification gaps
- F1 is analytic for the snapshot model. The scanner was not run on any authored variant, because the contract restricts scanner runs to committed fixtures.
- Not checked here: the other ten cases (other reviewers' items), class and evidence semantics beyond the tool's own docstring, and the eval kernel's exec model (F6).
- The `lsp` device is not in this session's tool inventory, so it was not used. Both fixtures are standalone snippets, so no caller graph was needed; symtable and dis (compile-only) were used instead.
- I did not review the base classifier's closure logic. Only its output rows were compared with the expectation.

## Verdict line
NestedDefReadsDefiningFrame: truth-correct; rule-too-loose for the enclosing-cell late-read property (F1). LateGlobalRebinding: truth-correct; rule adequate for its stated property. No truth-wrong and no rule-too-strict finding in either case. L1 should close F1 by an append-only pinned case or by naming the limit in the C1 claim.
