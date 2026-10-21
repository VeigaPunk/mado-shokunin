# FalsifyC131 — C1 CapturePartialOverride

## Findings and verdict

**Verdict: agree, for this exact case on the pinned delivered tool only.** No actionable defect was found in the assigned case. This is an author-lane advisory recommendation, **not admission**, integration approval, host clearance, or a finding that the entire F1 family is repaired.

Axes: complete semantic row fidelity; observed/lead and uncertainty calibration; immutable tool/input/runner identity; bounded reproducible evidence. The single authorized measurement improved evidence on these axes without changing the sealed truth or production code.

The independent expectation and actual complete finding multiset are identical:

| Population | Class | Command | Evidence | Multiplicity |
|---|---|---|---|---:|
| Independently reasoned expectation | `package_query` | `pacman -Q r22-partial-override` | `observed` | 1 |
| Actual scanner rows | `package_query` | `pacman -Q r22-partial-override` | `observed` | 1 |

There are no additional rows at either evidence tier. In particular, `pacman -S r22-partial-fixed` appears in neither an observed row nor a lead row. Actual counters: `package_query=1`; `host_mutation=live_probe=tool_install=vcs_write=0`; `observed_findings=1`; `lead_findings=0`; `eval_unparsed=0`; `unparsed_spawns=0`. The scanner identified exactly one file, one eval call, zero bash calls, and one input line. Its finding identifies `CapturePartialOverride-0`, tool `eval`, line 1, rule `pacman:-Q`, and the selected absolute fixture path.

The measurement runner returned **exit 0**, `status=complete`, `pass=1`, `total=1`, no comparison reasons, and no integrity errors. Its single scanner child returned **exit 1**, because the one package-query finding is unpermitted with an empty permit set; this is not a scan error or the oracle comparison exit. Both runner and scanner stderr were empty. The scanner's raw stdout begins `MADO_TRIPWIRE: findings`, not a clean verdict.

Raw argv, exit, stdout, stderr, parsed rows, complete scanner payload, pre/post integrity objects, and independently observed hashes are retained without another scanner run at:

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC131/result.json`

## Independent semantic rationale

The original inert source and proposal are `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CapturePartialOverride.json:3-16`; the exact materialized record is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json:1664-1721`. The fixture is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CapturePartialOverride.jsonl:1`. No source payload was executed.

Static derivation, independent of the green comparison:

1. Defining `worker` and `make` does not execute `worker`'s body. `make()` returns a `functools.partial` of the visible `worker`; constructing that partial stores its callable and keyword, and does not call `worker`.
2. The stored keyword is `argv=["pacman", "-S", "r22-partial-fixed"]`. The later invocation explicitly supplies the same keyword name with `["pacman", "-Q", "r22-partial-override"]`.
3. The cited partial semantics merge stored keywords first and invocation keywords second. The directly inspected reference source `/usr/lib/python3.14/functools.py:380-393`, especially lines 392-393, implements `keywords = {**self.keywords, **keywords}` followed by `self.func(*pto_args, *args, **keywords)`. The independently cited documentation is [Python 3.14 functools.partial](https://docs.python.org/3.14/library/functools.html#functools.partial): additional keywords extend and override stored keywords.
4. Thus the effective call is exactly `worker(argv=["pacman", "-Q", "r22-partial-override"])`. It reaches the one visible `subprocess.run(argv)` exactly once in the straight-line source model. The overridden `-S` list is never handed to a spawn call. There is no missing argument, duplicate effective keyword, conditional target, asynchronous schedule, or opaque value in this path.
5. The command text is `pacman -Q r22-partial-override`. Its declared class is `package_query`, consistently with the detector's existing class mapping at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:738-781` (`Q` at 771-772; plain `S` at 775-780). A followed, fully literal spawn is owed `observed`, not a lead. Here `observed` describes static source reachability under the scanner's contract; it is not evidence that a host command was executed or succeeded.

The original before-red authority remains `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:53-60,70-76`. Its F1 note at line 75 identifies the returned-partial lifetime mechanism by source and explicitly says it was not probed there. I did not rerun an original fixture with an old tool. This case's invocation literal defeats the stored keyword regardless of construction-versus-invocation environment timing; its pass must not be promoted into proof of every historical lifetime counterexample.

The canonical assignment distinguishes raw truth sealed before implementation from normalized expected materialized later. This review uses the unchanged original proposal and its source semantics as authority, not an assertion that the normalized expected file itself predated implementation. This case has no correction or addendum and retains the original expected row.

## Relevant delivered change and callers

Reviewed the actual `tools/mado-tripwire.py` diff from base `741122d177ae8ff68a73768777f20484d5bdcbe4` to delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, restricted to the assigned tool and relevant factory/partial/helper hunks. Current file hash matches the fixed delivered identity below.

The relevant source path is coherent with the independent expectation:

- Assignment binding calls `callable_info` and retains a resolved returned helper: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1820-1838,1859-1861,1928-1936`.
- A visible helper call resolves through `factory_result`, which selects the executed top-level return after preparing its prefix: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1642-1684,1780-1781`. In this source `make` has no preceding statements or ambiguous return.
- Partial construction resolves the original `worker` identity and captures the fixed keyword's literal using `captured_node`: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1417-1425,1761-1769`.
- The decisive changed merge is `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2556-2563`: names explicitly supplied at invocation form `overridden`; matching stored keywords are omitted before invocation keywords are appended. For this source that removes stored `argv` and retains only the call-site `argv`. It neither emits the fixed command nor constructs a duplicate-key helper call.
- `bind_literal` then binds the surviving keyword to `worker`'s parameter, and `follow_helper` overlays that bound parameter before scanning its body: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2089-2160,2407-2439,2564-2579`. The invalid-call and lead fallback paths exist but are not needed for this valid literal call.

These are textual source and diff observations, not LSP semantic proof. `read xd://lsp` returned **No such tool**, and its mounted-device inventory contained no LSP device; status, references, definition, and diagnostics could not be obtained. Text inspection was used only after that unavailability was established, not an empty cold-index result.

## Oracle comparison and uncertainty boundaries

This is an **exact** case, with `accept_exact_want=null`, empty `forbid_commands_any_tier`, and an explicit observed-only prohibition on the stale fixed command. The exact branch at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:732-756` compares the full sorted class/command/evidence multiset, preserving multiplicity, and requires zero aggregate unparsed counters. Therefore an extra stale lead would fail even though the explicit prohibition only names observed evidence. A missing true command, evidence downgrade, fabricated extra command, or duplicate row would also fail.

The materialized `require_signal=true` does **not** demand an artificial lead for this exact case: the exact branch returns before the uncertainty branch. The separate uncertainty rules at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:740-778` apply any-tier bans before either branch, allow only a complete zero-error `accept_exact_want` when one is explicitly supplied, otherwise reject observed rows and apply the required uncertainty signal. No unknown-case waiver, acceptance normalization, or parsed-clean substitute was used here.

Input identity and counters were checked by the runner's canonical parsing logic at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:683-729`, including selected file path, sealed digest, one-file shape, evidence markers, and nonnegative integer error counters. Raw findings independently show the same selected fixture and call ID.

## Bounded execution and identity evidence

Only this measurement command was invoked, once:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CapturePartialOverride
```

The runner validates the full frozen population but selects only one case for scanning: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:789-839`. Actual integrity objects before and after report 106 sealed source files, 52 proposal files, and 57 input files verified. Those are **integrity counts**, not 57 executed semantic cases. Actual semantic total is **1**.

The one scanner child used `/usr/bin/python3 -I -c WRAPPER` with the same absolute selected tool and fixture paths. The wrapper calls the selected module's `main(["--scan", fixture])` and no substitute scanner. The runtime cap is 402653184 bytes (384 MiB) address space and a 15-second timeout, enforced by `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:26-38,643-661`. There was no second scanner, fallback runtime, new source-shaped probe, or old-tool run. The runner's reconstructed top-level `argv` omits interpreter flags because it is built from `sys.argv` at line 796; the receipt separately retains the actual launched outer argv including `-I`, plus the actual scanner argv.

Independent `sha256sum` observations before and after the measurement were identical:

| Artifact | SHA-256 before = after |
|---|---|
| Tool `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| Fixture `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CapturePartialOverride.jsonl` | `ca1c96233167e494cc4b6da2be776317dfbe997759a0f350272c4c0916f220ae` |
| Runner `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py` | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| Expected `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| Proposal `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CapturePartialOverride.json` | `f5bdc465f9608f5d90fba2fce1d389ca909cf38d74e51768b1d742ff1c6ad1af` |

The runner also reports identical before/after population digest `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad` and raw truth seal digest `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4`. There is no reported identity drift or moving-target comparison.

## Residual risk and verification gaps

- This literal, unconditional keyword-override case cannot establish general lifetime correctness: it has no rebinding between construction and invocation, no conditional or non-Name returned target, no unknown `*`/`**` expansion, no captured mutable-object change, no nested partial composition, and no scheduled/cancelled target. It supports only the named bounded form claimed at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/supported-forms.md:7-11`; it is not saturation evidence for all such programs.
- No fixture Python, printed host command, package query, live probe, process/session inspection, or host mutation was executed. `subprocess.run` and `pacman` in the payload remained inert scanner input. Actual host execution and environmental command success are intentionally unverified.
- No full oracle/corpus/no-harm/resource sweep, C2 audit, build, lint, formatter, generic smoke, or mutation test was run. Those are not implied by this one-case agreement. LSP references/definitions/diagnostics remain unavailable as recorded above.
- No production, fixture, expected, proposal, gate, registry, or documentation source was edited. Deliverables are this assigned report and its raw receipt. No tools were installed or updated.
- The prior r19/r20/r21 rejected-harmed receipts and streak remain authoritative. The historical target qualifications and no-harm rules in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/guard-clarifications.md` are unchanged. L1 retains planner/integration authority; this report grants no non-author admission.

Report: .ufo/waves/round-22/w2/reports/FalsifyC131.md
