# C1 CapturePartialNested — scoped recovery falsification

## Verdict and findings

**Verdict: agree**, limited to the complete sealed `CapturePartialNested` result on the assigned C1 bytes for delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. No actionable production defect was found for this exact case. This is an author-lane advisory recommendation, **not non-author admission**, desktop clearance, or closure of C1 as a whole. The prior r19/r20/r21 rejected-harmed receipts and rejection streak remain authoritative.

**Informational semantic caveat:** the original proposal says `functools.partial` “copies its fixed argument objects” and “freezes that list” (/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CapturePartialNested.json:16). More precisely, a partial retains references to its fixed argument objects; it does not deep-copy or make the list immutable. That wording must not support a stale-observation claim after object mutation. Here there is only rebinding to a different list, so this caveat does **not** contradict or alter the original expected row. The proposal, fixture and expectation were left unchanged.

## Axes

1. Complete semantic class/command/evidence multiset fidelity.
2. Callable identity and construction-versus-invocation lifetime fidelity.
3. Honest uncertainty, parse/error accounting and evidence strength.
4. Fixed artifact provenance and one bounded canonical scanner invocation.

## Independent semantic derivation

The sealed record is /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json:1608–1662. It declares `exact`, two `reset:false` cells, no addenda or correction, and `accept_exact_want:null`. The original cells and original expected row are independently retained in /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CapturePartialNested.json:3–14. The actual inert input is /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CapturePartialNested.jsonl:1–2.

- Cell 1 defines the module helper `run_pkg(cmd)` and factory `make(cmd)`. `make(["pacman", "-S", "r22-pn-build"])` constructs a partial of the already visible `run_pkg` function with that list as its fixed positional argument. Construction does not invoke `run_pkg` or `subprocess.run`.
- `stored` retains the resulting callable across the two persistent cells. Its function is the visible `run_pkg`, not a conditional target or a subsequently selected function.
- Cell 2 assigns a new list to the module name `cmd`. That does not modify the list retained by the partial, and the factory parameter and module name are not the same binding. `stored()` then unconditionally invokes `run_pkg` once with the original fixed argument.
- `run_pkg` binds its own `cmd` parameter to the original list and calls `subprocess.run` with it. The complete expected multiset is therefore exactly one `host_mutation / pacman -S r22-pn-build / observed` row, with both unparsed counters zero. “Observed” is the scanner's statically followed-call label, not evidence that a package command was executed on this host.

An empty result would lose a true command; a lead-only result would understate this unconditional visible call; `pacman -Q r22-pn-late` at either tier would invent the invocation-time global argv. Any extra row or duplicate also fails this exact case. There is no opaque expansion, invalid binding, reset, mutation of the retained object, callback or conditional return requiring uncertainty here.

The original source authority is /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:70–76: F1 identifies invocation-time factory binding and specifically cites the returned-partial sibling by source. Its original red receipt remains authority; the old detector was **not** rerun. This new finite case is a cross-cell returned-partial variant, not a claim that all original failure families have been closed.

## Delivered-path review

I read the actual tool-only diff from base `741122d177ae8ff68a73768777f20484d5bdcbe4` to the assigned delivered revision. Relevant changed behavior agrees with the independent derivation:

- /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1642–1684 binds the factory call in its creation environment and resolves the returned expression there. The former invocation-time `capture_owner` replay is replaced by retained closure state.
- /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1761–1769 captures a helper partial's fixed arguments through `captured_node`; :1417–1425 stores the folded literal on the synthetic node. :1355–1357 reads that captured value instead of resolving a later source-name binding.
- /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1859–1861 and :1928–1936 retain the returned callable under the assigned `stored` binding. :2824–2825 and :2859–2868 preserve per-file environments when `reset` is false.
- /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2555–2569 prepends the retained fixed argument before following the helper; :2415–2437 binds that value into the helper body. :2675–2679 classifies the resulting literal argv. The source does not need to borrow the later module `cmd` for this case.
- /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2280–2283 uses AST-only compilation. The fixture's imports and package command were never executed.

## Authorized measurement and actual rows

Executed **once**, with no extra scanner run or source-shaped probe:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CapturePartialNested
```

The canonical runner selects exactly one matching case at /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:803–810 and runs only that selected list at :828–851. Its scanner child applies `RLIMIT_AS=402653184` bytes and a 15-second timeout at :643–660. No second runtime, alternate tool, full-oracle scan or old-tool confirmation was invoked.

| Class | Command | Evidence | Multiplicity |
|---|---|---|---:|
| `host_mutation` | `pacman -S r22-pn-build` | `observed` | 1 |

Actual metadata: `argv0=pacman`, `rule=pacman:-S`, fixture line `2`, tool-call identity `CapturePartialNested-1`. No `pacman -Q r22-pn-late` row appeared at any tier. Counts were `host_mutation=1`, all four other classes `0`; `observed_findings=1`, `lead_findings=0`. The file row identified the exact selected absolute fixture path and digest, two eval calls, two lines, `eval_unparsed=0`, and `unparsed_spawns=0`.

Scanner exit was **1**, with one unpermitted finding and empty scanner stderr: this is the expected policy finding exit, not a parse failure. The comparison runner returned **0**, `status=complete`, `pass=true`, totals `1/1`, empty reasons, `scanner_error=null`, and no integrity errors. No runner stderr was emitted in the tool response. Raw scanner argv/exit/stdout/stderr and the complete runner stdout are retained in the receipt.

The green comparison is not my semantic proof. The runner's exact comparator at /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:732–756 compares full sorted class/command/evidence multisets, retaining duplicate multiplicity, and requires zero combined unparsed counters. Its input identity checks are at :683–729. Its separate uncertain-case branch at :758–778 permits a complete `accept_exact_want` alternate only when declared; otherwise observed rows are rejected and explicit uncertainty is required when warranted. The any-tier forbidden-command checks at :740–748 run before either branch. None of those uncertain-case allowances relax this exact case.

## Artifact identity and raw receipt

Separate pre/post `sha256sum` calls returned identical values for all five artifacts:

| Artifact | SHA-256 before = after |
|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CapturePartialNested.jsonl` | `fea762dedf8f6027faf14a5db2ceaffd2988be641045a099ec6794f9b8ec4da8` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py` | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CapturePartialNested.json` | `13a9f4866f8cffa13c648f227b6b2bd3862b9558e45bed839ee8cadc93af0379` |

The selected tool and oracle match the assignment pins; no moving-target drift was observed. Runner integrity records additionally agree before/after on the tool, runner, expectation, population and truth-seal identities. They validate 106 sealed source files, 52 proposal files and 57 input files. Those are **integrity validation counts**, not 57 executed cases or a saturation claim; only this one scanner case was measured. Normalized expected materialization is not represented as the original raw-truth landing event.

Receipt: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC130/result.json

## Residual risk and verification gaps

- This result closes only this finite unmutated-list, visible-helper, cross-cell returned-partial shape. It does not establish correctness for mutable captured objects, nonlocal mutation, late-bound free globals, conditional targets, resets, cancellation/races, other partial constructions, the remaining 56 oracle cases, historical guards or C2. No family-wide repair, resource saturation or admission claim follows.
- LSP was unavailable: reading `xd://lsp` returned `No such tool: xd://lsp`. Therefore references/definition/diagnostics could not be performed. Caller-path review used targeted source reads and literal grep as fallback; grep was not treated as semantic proof.
- No builds, lints, formatters, generic smoke checks, full-suite runs, original-red reruns, fixture execution, live host probes, installs or updates were performed. No production, fixture, expected, source, registry or shared documentation bytes were changed. Only this assigned report and its uniquely assigned receipt were written.
- The recommendation is **agree for this exact current target**, not “safe because parsed clean.” Static reasoning supplies the expected behavior; the one bounded measurement supplies evidence that these pinned bytes match it.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC130.md
