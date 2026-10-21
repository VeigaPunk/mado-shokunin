# C1 CapturePartialFixed — FalsifyC127

## Findings by severity

**No actionable defect found in the assigned sealed case. Verdict: agree.** This is an author-lane advisory recommendation for the pinned delivered classifier, not admission, integration approval, a non-author attack receipt, or a reversal of any r19/r20/r21 rejected-harmed receipt.

Assigned revision: `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. Reviewed the classifier diff from registered base `741122d177ae8ff68a73768777f20484d5bdcbe4` to that revision, restricted the semantic review to the factory/direct-partial/assignment/spawn route relevant to this case, and measured the current classifier whose bytes match the assigned C1 SHA-256. No claim is made about the identity of unrelated working-tree files.

## Axes

1. Creation-time argument lifetime and wrapped-callable identity.
2. Complete class/command/evidence multiset, missing true commands, invented observed/lead commands, and honest parse uncertainty.
3. Independent original truth, exact fixture identity, and before/after artifact integrity.
4. One-case measurement/resource bounds, read-only source handling, and advisory authority.

## Independent semantic expectation

Source authorities:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CapturePartialFixed.json:2-19` and `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/reports/CapturePartialFixed.md:17-57`.
- Original F1 mechanism and actual earlier red: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:53-76`. That original fixture differs from this partial variant; its reported red remains authority and was not rerun.
- Sealed case: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json:1433-1491`. It preserves `expected_kind: exact`, the original `want`, no correction/addenda, and `accept_exact_want: null`.
- Inert source: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CapturePartialFixed.jsonl:1`.

Static reasoning, independently of the green comparison: `factory(argv)` supplies the initial list `["pacman", "-S", "r22-partialfixed-held"]` to parameter `cmd`. Constructing `functools.partial(subprocess.run, cmd)` stores that argument object and the current `subprocess.run` callable. The later assignment to module name `argv` creates a different list binding; it does not mutate the held list or replace the partial's stored target. The sole `runner()` call therefore supplies exactly the held list to the stored spawn callable. There is no conditional target, unresolved expansion, opaque callback, cancellation, list mutation, or namespace reset in this source.

The complete expected multiset is exactly:

| class | command | evidence | multiplicity |
|---|---|---|---:|
| `host_mutation` | `pacman -S r22-partialfixed-held` | `observed` | 1 |

The `-S` class is independently consistent with `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:738-780`; the decoy `-Q` would instead be a package query, but neither decoy is executed by the source. Zero parse/unparsed counters are appropriate for this fully literal, straight-line form. Here “observed” is the scanner's static evidence tier, not a claim that the payload ran on the host.

Both `pacman -Q r22-partialfixed-decoy` and `pacman -S r22-partialfixed-decoy` are explicitly forbidden as observed by the original proposal. The any-tier exclusion list is empty for this exact case, but complete multiset equality also rejects either decoy as a lead, any other extra finding, missing true argv, duplicate output, or an observed-to-lead downgrade. Unknown-case acceptance was not substituted: `accept_exact_want` is null, and the exact branch requires equality plus zero unparsed. The distinction is explicit in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:736-778`: any-tier prohibitions precede both branches; the accepted-exact alternate exists only in the uncertain branch. An empty parsed-clean result cannot pass this case.

## Changed path and caller review

Relevant current logic in `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`:

- `prepare_eval_calls` snapshots statement-local environments before retaining subsequent updates (`2203-2254`). The `runner` assignment therefore resolves while `argv` still denotes the held list.
- `update_bindings` resolves the assigned value (`1928-1936`); `assignment_binding` now retains a returned `spawn` as well as helper/uncertain/invalid identities (`1859-1861`).
- `callable_info` routes a visible factory call through `factory_result` (`1780-1783`). `factory_result` binds arguments, overlays the factory frame, and resolves the return expression in that frame (`1642-1684`; literal binding at `2089-2116`).
- The partial-of-spawn branch preserves the wrapped spawn dictionary and eagerly folds fixed arguments from that creation frame (`1761-1775`). On the later name call, the stored binding is returned (`1748-1753`); the invocation does not reevaluate `Name(argv)` to manufacture the decoy.
- `spawn_scan` resolves the current callee (`2456-2466`) and consumes stored partial arguments with explicit mutation invalidation (`2630-2684`). This case has no mutation, so the stored held argv reaches classification. Ordinary findings receive the explicit observed marker during serialization (`2875-2893`).

The delivered diff removes the old deferred factory-argument rebinding route and broadens returned-callable handling to include spawn results. The old returned-partial factory branch only retained helpers; the present case additionally exercises retention of a direct spawn partial. This is not evidence that the old tool emitted the decoy for this exact variant, and no old-tool measurement was performed. The current result agrees for both lifetime and returned-spawn identity rather than merely avoiding one forbidden spelling.

## Authorized measurement and actual rows

Executed exactly once, with this outer argv:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CapturePartialFixed
```

The canonical runner validates the full frozen population before selection, then selects exactly one matching case (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:789-852`). Its sole scanner child uses isolated Python, imports the selected classifier, and scans only the selected inert JSONL. `RLIMIT_AS` is 402653184 bytes and the child timeout is 15 seconds (`643-661`). The fixture's Python is AST input, never executed. No additional scanner, old-tool, corpus, mutation, or source-shaped probe ran.

Observed results:

- Outer measurement exit **0**, status `complete`, comparison **1/1**, reasons `[]`.
- Scanner exit **1**: one unpermitted finding, **not** a comparison failure or package operation.
- Both outer and scanner stderr empty; scanner error null.
- Exactly one file: selected absolute fixture path, input digest matching the seal, `eval_calls=1`, `bash_calls=0`, `eval_unparsed=0`, `unparsed_spawns=0`.
- Counts: `host_mutation=1`; `package_query=live_probe=tool_install=vcs_write=0`. Observed findings **1**, leads **0**.
- Complete actual row: `{"class":"host_mutation","command":"pacman -S r22-partialfixed-held","evidence":"observed"}`. Metadata: `argv0="pacman"`, `rule="pacman:-S"`, `tool="eval"`, `tool_call_id="CapturePartialFixed-0"`, line `1`, and the exact selected fixture file.
- No decoy command at any evidence tier, no lost true command, no wrong target/class, no lead promotion/demotion, and no parse-error-to-clean ambiguity in this result.

Raw outer argv/exit/stdout/stderr, the complete runner/scanner payloads and child argv, stdout/stderr hashes, and artifact hashes are retained without trimming in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC127/result.json`. The runner's self-reported outer argv omits the interpreter flag because it constructs that field from `sys.argv`; the receipt separately retains the actual supplied argv including `-I`.

## Identity and integrity

Independent `sha256sum` observations before and after the measurement were identical:

| Artifact | SHA-256 before = after |
|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CapturePartialFixed.jsonl` | `2a9e6dae161d4b9043666ef2732bd293ae1fc2234e32a4ffb1f26a48ac88ced9` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py` | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CapturePartialFixed.json` | `714fe0db2a36b6b59c1c74957d8f141d0e7a7f0690e4146165722193448a4c13` |

The runner additionally reports matching before/after population integrity: 106 sealed source files, 52 proposal files, and 57 input files verified; integrity errors `[]`. **These are integrity counts, not 57 executed cases.** Population digest: `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad`. No tool/fixture/runner drift was observed.

## Residual risk and verification gaps

- This closes only the assigned direct partial-of-spawn fixed-literal rebinding example. It does not establish all F1 variants, mutable-object/nonlocal behavior, conditional returns, nested helper partials, late globals, scheduling, F2-F5, corpus no-harm, C2, or resource scaling/saturation. There is one canonical runner and one selected scanner child here; no same-identity rerouting or resume path is exercised. No broader runtime, routing, or `resume_continuity_v1` judgment follows from this case.
- `xd://lsp` is not mounted: the device-documentation request returned `No such tool`. Status, references, definition, and diagnostics could not be requested; this was not an empty/cold-index result. Targeted literal source/diff inspection was the fallback and is not presented as semantic reference proof. No diagnostics/build/lint/formatter/full-suite/generic smoke was run.
- Original independent truth and earlier red receipts remain unchanged. The raw truth seal predates implementation; later expected materialization is used as the sealed comparison artifact, not misrepresented as an earlier raw file.
- Only this assigned report and receipt were authored. No production, fixture, expectation, proposal, gate, registry, or other documentation edits; no tool installs/updates, live host probes, package operations, delegation, or background jobs.

**Recommendation: agree for CapturePartialFixed on the pinned delivered C1 bytes; no admission granted.**

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC127.md
