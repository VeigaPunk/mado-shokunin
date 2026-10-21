# FalsifyC113: C1 sealed case CXPartialLocalFunction

Seat: MadoR22.FalsifyC113 (leaf, author-lane advisory). Not a non-author admission, grants nothing, changes no streak. r19/r20/r21 red receipts unchanged.

## Verdict

**AGREE, case-scoped.** The selected tool's output for CXPartialLocalFunction equals the sealed exact expectation. My independent CPython 3.14 reasoning yields the same single row. No falsifier found for this case within bounds (one runner child, no new probes). This covers one case of 57. It is not population evidence and not admission.

## Expected (independently reasoned)

- Exact multiset: one row, `{class: host_mutation, command: "pacman -S r22-cxlocal", evidence: observed}`.
- Zero unparsed (`eval_unparsed + unparsed_spawns`) and zero parse or scanner errors.
- Forbidden observed: `pacman -Q r22-cxlocal-module` (module-level decoy). Forbidden at any tier: none. `accept_exact_want`: null. Kind: exact.
- Semantics: `make()()` is an unconditional module-level call. Inside `make`, `def inner` binds a local name (executionmodel.rst L89–93: a name bound in a block is local; L113–115: resolution uses the nearest enclosing scope). So `return functools.partial(inner, [...])` wraps the local `inner`, not the module `inner`. `partial` stores `func` at creation (functools.py L352) and `args` (L353). `__call__` runs `self.func(*pto_args, *args, **keywords)` (L393). The executed call is `subprocess.run(["pacman","-S","r22-cxlocal"])`. The module decoy is never invoked. One definite execution gives one observed row, and no path produces uncertainty.
- Class mapping: `pacman -S` gives host_mutation. The tool's rule `pacman:-S` agrees.
- Uncertainty boundary: none for this text. The expectation claims no lead and no uncertainty. `require_signal: true` is inert for exact cases (R2).
- Provenance: raw proposal bytes `5001bb9b…6848` are present at commit 9185f1f (11:39:45-03:00). Repair commit 330de68 (11:53:50-03:00) changed `tools/mado-tripwire.py` after that. The proposal's citation (`returned_call` 1653–1659, module bindings at 1657) matches the pre-repair file `evidence/tool-before.py` (sha `46c82902…c8c1`), checked at those lines. The fixture `inputs/CXPartialLocalFunction.jsonl` (`fedd6560…2992`) is normalized material from commit 5c7b983. The runner verified its code cell equals the sealed proposal cell.
- Nothing in the expected contradicts the raw proposal, the truth seal, or the ConnLifetime report row.

## Measured (one runner invocation, one scanner child)

- Executed: `python3 -I .../round-22/oracle/measure.py --tool .../tools/mado-tripwire.py --case CXPartialLocalFunction`.
- Runner: exit 0, stderr empty, status `complete`, `integrity_errors: []`, 1 of 1 selected case passed.
- Child (the only scanner process): argv `[/usr/bin/python3, -I, -c, WRAPPER, tools/mado-tripwire.py, inputs/CXPartialLocalFunction.jsonl]`, exit 1, stderr empty. Stdout is a banner line `MADO_TRIPWIRE: findings` followed by one JSON verdict line (`mado-tripwire-verdict-v1`).
- Caps applied by the runner: RLIMIT_AS 384 MiB and 15 s timeout (measure.py L26–27, L643–644, L658–661).
- Rows: `got_rows = [{host_mutation, "pacman -S r22-cxlocal", observed}]`. `unparsed: 0`. `reasons: []`. `pass: true`.
- Payload: counts host_mutation 1, all others 0. `observed_findings` 1, `lead_findings` 0, `unpermitted` 1. File row: `lines` 1, `eval_calls` 1, `eval_unparsed` 0, `unparsed_spawns` 0, `bash_calls` 0, `sha256` `fedd6560…2992` (equals sealed input). Finding: line 1, `tool_call_id` `CXPartialLocalFunction-0`, `rule` `pacman:-S`, `argv0` `pacman`, `timestamp` `"None"`.
- Tool hash: `36fdc459…badce` before the run (sha256sum), in the runner's `tool_sha256_before`, and after the run. No drift.
- Population integrity (runner, before and after): 106 sealed sources, 52 proposals, 57 inputs verified. Expected `b5cd4cf3…4357` matches its pin. Truth seal `47f403f6…24d4`. Producer `0270c10b…5600`. Runner `41b021bb…28c7`. Population `04616857…86ad`.

## Falsification attempts (this case)

| Family | Attack | Observed | Result |
|---|---|---|---|
| False observed/lead argv | Extra row, decoy as observed or lead, or mangled argv | One row, `lead_findings` 0, command text exact | Not falsified |
| Lost true command | `pacman -S r22-cxlocal` absent | Present, observed | Not falsified |
| Wrong identity | Module decoy chosen at the partial (pre-repair behaviour, `tool-before.py` L1657) | No `pacman -Q r22-cxlocal-module` row at any tier. Current path binds `inner` in factory-local bindings: `factory_result` L1657, L1674–1675; `update_bindings` L1884–1885 | Not falsified |
| Lifetime | Identity lost after `make()` returns | Row emitted at the post-return call. Local helper carried by closure overlay L1678–1683. `fixed_nodes` applied at invocation L1761–1769 and L2556–2564 | Not falsified for this text. Converse (module rebinding after return must not change captured identity) is not in this case |
| Conditional target | Call treated as conditional or dropped | Unconditional module call; no branch in this text | Not applicable to this text (see hypothesis below) |
| Parsed-clean ambiguity | Zero unparsed while a spawn is hidden | Counters 0/0 consistent with one resolved spawn. Child exit 1 matches `unpermitted` 1. Banner is non-JSON, so the last-line parse is unambiguous | Not falsified |

Fine points:
- The decoy separates module-level lookup from factory-local lookup. It does not separate a factory-local executed binding from a def-name search inside the factory body. Both select the single local `inner`. That separation is untested here.
- Partial construction produced no lead rows. `functools.*` appears in a pure-stdlib predicate (L1588–1592). This is [INFERENCE]; I did not read the enclosing function in full.
- [INFERENCE, untested] `factory_result` selects the first top-level `return` (L1649), and `prepare_eval_calls` breaks only at a top-level `return` (L2252–2253). An earlier `return` nested under an `if` is therefore not treated as a branch by that selection. Whether this yields a false definite identity for conditional factories needs an assigned probe.

## Runner and comparator observations (none changes this verdict)

- R1: `parse_scan_output` accepts child exit 0 or 1 (measure.py L687–688) and never ties it to findings or `unpermitted`. Here both agree (exit 1, unpermitted 1).
- R2: `require_signal: true` is inert for exact cases. `evaluate()` returns at L752–756 before the signal check at L765–767.
- R3: `scan_file` deduplicates identical (class, rule, evidence, text) per eval call (scanner L2875–2885). A true multiplicity above 1 cannot be represented. True multiplicity here is 1.
- R4: The rationale says a decoy-free resolver miss "would be silent". For the exact kind, a silent miss still fails because the required want row is absent. The real gap is coverage of decoy-free, def-name-index and rebinding shapes, not detection of this shape.
- R5: `timestamp` is the string `"None"` when the fixture line lacks one (scanner L2890). Cosmetic, not compared.
- R6: The sealed citation names `tools/mado-tripwire.py sha256 46c82902…c8c1`. Those bytes now live at `evidence/tool-before.py`. The live path holds `36fdc459`. The line numbers are correct only for the pre-repair file.
- R7: `evidence/first/oracle-before-new50.json` has top-level `selected_tool_sha256` = `36fdc459`. Its nested runner output and child argv name `evidence/tool-before.py` with sha `46c82902`. The nested fields are authoritative, and the wrapper field is mislabelled. I did not rely on it.
- R8 (out of lane): `evidence/first/oracle-after-all57.json` has top-level `audit_tool_sha256` = `56091de7…afce9`, not the pinned C2 audit sha `277eced2…`. Not analysed here.

## Prior receipts (read only; no old tool run)

- `oracle-after-all57.json`: tool `36fdc459`, measured commit 5c7b983. The child payload for this case is identical to this run's payload. Case pass true. Nested totals 57/57.
- `oracle-before-new50.json`: pre-repair tool `46c82902` (group proposal, nested totals 13/50). Case pass false. `got_rows` = `package_query, pacman -Q r22-cxlocal-module, observed`. Reason: forbidden observed command. This reproduces the mechanism cited at `tool-before.py` L1653–1659.

## Scope against the current target

- Covered: 1 sealed proposal case of 50 eligible proposals (57 total with 7 supplemental originals). One scanner child.
- Target (registration.md): every eligible frozen expectation matches, original reds resolve without expectation change, guards retained. This case is one passing expectation, nothing more.
- Not covered: OriginalF1–F5 and the control fixture, OriginalR19PureFrozenClosure, the 166/175 historical guard, the 1356-fixture removal comparison, resource recipes, the C2 audit, and any multi-case or population claim.

## Provenance and receipts

- Delivered HEAD `71228fd`: `tools/mado-tripwire.py` blob = `36fdc459`. Commit 5c7b983: same blob. Working-tree file: same blob, `git status` clean for that path.
- Raw truth at 9185f1f: proposal `5001bb9b`, tool blob `46c82902`. Repair 330de68 follows the raw seal.
- Receipts: `.ufo/waves/round-22/w2/receipts/FalsifyC113/` holds `result.json` (argv, exit, verbatim stdout and stderr, child payload, all hashes, checks, prior-receipt comparison), `measure.stdout`, `measure.stderr`, `python-version.txt`.
- Non-scanner executions: `python3 -VV` (3.14.8, version query only), `sha256sum`, and read-only `git show`, `git log`, `git status`, `git cat-file`. No scanner child beyond the runner's one, no fixture execution, no old tool, no `pacman`. No installs or updates.

## Verification gaps and handoff

- Untested shapes that need an assigned probe: (1) decoy-free variant, (2) factory-body def-name index versus executed binding, (3) module rebinding after factory return, (4) conditional early `return` ahead of the top-level one.
- Determinism: two separate processes (prior after-all57 and this run) agree. Hash seed is not pinned. This is supporting, not proof.
- Code reading covered the cited paths only. `spawn_scan` and `eager_calls` were not read end to end.
- Main should run the population check once for admission-facing evidence. This seat did not run it.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC113.md
