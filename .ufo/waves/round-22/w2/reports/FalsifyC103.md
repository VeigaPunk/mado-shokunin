# C1 CX3CaptureMutation — author-lane advisory falsification

## Findings by severity

**No actionable case-specific defect established against the sealed uncertainty contract. Verdict: agree with the recorded uncertain acceptance, not with exact command reconstruction or semantic clearance.** The one authorized measurement reports `pass: true`, runner exit `0`, scanner exit `0`, and the complete actual row multiset `[]`. Crucially, `eval_unparsed = 0` and `unparsed_spawns = 1`: this is explicit unresolved-spawn uncertainty, not a fully parsed negative.

The definite true command is absent. That limitation must remain visible, but the original proposal expressly permits this uncertainty outcome. Calling this an exact-recall success, proof that no host mutation was issued, or closure of the broader lifetime family would contradict the retained source truth.

## Scope and axes

- **Semantic fidelity:** preserve the shared object's lifetime, the returned callable's identity, and the post-mutation argv; forbid stale argv at every evidence tier.
- **Evidence calibration:** distinguish the complete exact alternate from permitted uncertainty, and distinguish zero findings from zero unresolved spawns.
- **Measurement integrity and boundedness:** one fixed tool identity, one sealed case, one capped scanner child, complete raw scanner evidence, and before/after identity checks.

Target: delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, specifically the assigned on-disk C1 tool with SHA-256 `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce`. Reviewed the relevant repair diff from registered base `741122d177ae8ff68a73768777f20484d5bdcbe4` to that revision for `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`; unrelated shell-classification changes are outside this case's conclusion. No alternate scanner/runtime or old classifier was run.

## Independent source semantics

The original proposal is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CX3CaptureMutation.json:3-19`. Its inert source is preserved in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CX3CaptureMutation.jsonl:1`. The sealed case has no correction or addendum; it retains `expected_kind: uncertain`, empty `want`, the exact alternate below, `require_signal: true`, and both stale-command exclusion lists. The original proposal, not the green measurement, supplies the semantic authority. This report does not claim that later-materialized normalized `expected.json` existed before implementation.

Reasoning without executing the payload:

1. The initial list has three items. `make(cmd)` passes the same list object into parameter `argv`; no source operation copies it. `make` creates `run`, returns that exact helper, and does not call `subprocess.run` itself.
2. The closure keeps `argv` reachable after `make` returns. `cmd[1] = "-S"` is an in-place update of that shared list at a valid index, not rebinding of `cmd` or of the callable.
3. The single subsequent `runner()` invokes that returned helper. With the ordinary standard-library bindings shown in the fixture, its one issued subprocess argv is `["pacman", "-S", "r22-cx3-mutation"]`.
4. Thus the complete exact semantic row multiset is:

   ```json
   [{"class":"host_mutation","command":"pacman -S r22-cx3-mutation","evidence":"observed"}]
   ```

   This is an unconditional directly invoked subprocess call, not an uncalled-body lead. It is a source-level statement about the issued call, not proof that a real package operation succeeded or even ran on a host. The fixture was never executed.
5. `pacman -Q r22-cx3-mutation` is only the pre-mutation list value. No subprocess call receives it. It is invalid as either `observed` or `lead` in this fixture. There is no branch, scheduled target, missing argument, alternate returned helper, or conflicting global binding that makes the true argv semantically ambiguous.

The cited local Python reference supports object binding and in-place subscription updates: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-simple_stmts.rst:143-150,190-209`. Runtime free-variable resolution is stated at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-executionmodel.rst:322`. Both source digests match those in the proposal.

The uncertainty is therefore **the detector's supported-reconstruction boundary**, not uncertainty about Python's outcome. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/supported-forms.md:15-22` permits abstention for shared mutable captured objects, prohibits stale observation, and requires full row multisets plus zero errors for an exact answer. This case's original any-tier prohibition is stronger than merely forbidding stale observation and is retained unchanged.

## Actual measurement and oracle interpretation

Executed exactly once:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CX3CaptureMutation
```

| Observable | Actual value |
| --- | --- |
| Runner status / exit | `complete` / `0` |
| Cases executed / passed | `1` / `1` |
| Scanner exit / stderr / scanner_error | `0` / empty string / `null` |
| Complete actual class-command-evidence rows | `[]` |
| Observed / lead findings | `0` / `0` |
| Eval calls / eval_unparsed / unparsed_spawns | `1` / `0` / `1` |
| Scanner first stdout line | `MADO_TRIPWIRE: clean` |
| Any-tier forbidden stale command present | No; there are no finding rows |
| Exact alternate achieved | **No** |
| Explicit permitted uncertainty achieved | **Yes**, positive `unparsed_spawns` |
| Post-run integrity errors | `[]` |

The canonical evaluation logic is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:736-778`: it checks any-tier and observed exclusions before accepting either outcome; exact cases require the complete multiset and `unparsed == 0`; this uncertain case's `accept_exact_want` also requires its complete multiset and zero unparsed; otherwise observed rows are rejected and an uncertainty signal is required. The actual empty multiset and positive counter take only the uncertainty branch. No subset match, exact alternate, or invented lead is being credited.

The runner verifies all 57 fixture inputs, 52 proposal files and 106 sealed sources before and after, but its exact case filter selects only one scan (`measure.py:798-810,828-839`). Those integrity counts are not 57 scanner results or a saturation claim. Its scanner subprocess receives isolated Python `-I`, `RLIMIT_AS = 384 * 1024 * 1024`, and a 15-second timeout (`measure.py:26-27,643-660`). The child is given the canonical selected tool path and the selected fixture path; it calls the scanner's `main(["--scan", fixture])`, not the payload.

## Relevant changed behavior and call path

Static source inspection supports, but does not replace, the observed receipt:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2089-2116` binds a normal Name argument through `literal_value` and retains its object in the bound mapping. `factory_result` at `1642-1684` resolves the executed returned helper and stores the bounded lexical overlay, rather than re-resolving the factory argument by its source name at later invocation.
- Subscription assignment invalidation at `2231-2242` records the root literal object's identity in `MUTATED_LITERALS`. The statement snapshot retains this marker (`2197-2200`).
- `mutated_literal` at `1326-1342` checks that identity, and closure invocation at `2510-2516` converts affected captured values to `LITERAL_MISS` using the caller's mutation set. This is conservative invalidation, not simulation of the new list item.
- `follow_helper` at `2407-2437` passes the closure environment into body scanning. The unresolved `argv` reaches the spawn argument resolver at `2632-2643,2675-2684`, which records an unparsed spawn rather than classifying the obsolete list. This explains why neither a false package-query observation nor a stale lead appears, while exact mutation recall is still absent.

The LSP device is unavailable: attempting to discover `xd://lsp` returned `No such tool`. Consequently server status, references, definition and diagnostics could not be obtained. Targeted literal searches and source/diff reads were the fallback, not semantic-reference or diagnostics proof.

## Integrity receipts

Raw scanner argv, exit, stdout, stderr, payload, complete rows, runner result, selected invocation including outer `-I`, and hash checks are retained at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC103/result.json`. The runner reconstructs its own outer argv from `[sys.executable, *sys.argv]` (`measure.py:796`), which omits interpreter flags; the receipt explicitly records the actual authorized invocation separately. The scanner child's recorded argv includes `-I`.

| Artifact | SHA-256 | Before/after |
| --- | --- | --- |
| Selected tool | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` | Same, externally checked and runner checked |
| Selected fixture | `a0b508866577e0eda2f3ad0a297e4e90e6aeb44815777989a2ab4e51eeb8e225` | Same, externally checked and population checked |
| Runner | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` | Same, externally checked and runner checked |
| Normalized expected | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` | Same, externally checked and runner checked |
| Original proposal | `74d66361c75778377cd41cd8b2c4d4d9e17611f9b8d6898cf59bdbe2b0cce456` | External precheck and pre/post sealed-source checks |

No identity drift was observed. No installs or updates were performed. No production, fixture, expectation, source, registry or shared documentation was edited; only this report and the assigned receipt were written. No additional source-shaped probe, old-tool confirmation, build, lint, formatter, full-suite run, whole-corpus scanner run, live probe, or mutation test was performed.

## Residual risk and verification gaps

- **The output is not parsed-clean.** The human banner says `clean`, but the same raw output discloses one unresolved spawn. The scanner's explicit contract at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:30-37` defines `clean` as no finding in covered forms, never proof that no host command ran. Discarding the JSON counter would turn this accepted abstention into a false negative assurance. That presentation caveat is not evidence of a new contradiction with the stated case contract.
- The true `host_mutation` command is statically definite but not reconstructed. This case supports only no-stale-row plus explicit-uncertainty behavior; it cannot establish exact mutable-object reconstruction, universal lifetime/callable correctness, no-harm across prior populations, or resource saturation.
- Conditional returns, scheduled/cancelled work, cross-cell resets, other alias/mutation shapes and resume paths are not exercised by this fixture. No `resume_continuity_v1` or recovery approval claim is made.
- Original r19/r20/r21 rejected-harmed receipts and the rejection streak remain untouched authority. This one-case advisory agreement does not supersede any prior red, establish the other guards, or grant non-author admission. L1 retains planner/integration authority.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC103.md
