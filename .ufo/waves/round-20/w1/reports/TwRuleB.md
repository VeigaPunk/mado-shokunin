# TwRuleB — E1/E2/E3 patch prepared; requested suites deferred to L1

## Delivered

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/patches/TwRuleB.patch` — unified diff for `tools/mado-tripwire.py`, with required `a/tools/mado-tripwire.py` / `b/tools/mado-tripwire.py` paths. SHA-256: `9d3487c68ea8e9ffd5ed094890d76261ae1fdff4b8d64ef947aa128d8412782e`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/patches/TwRuleB-dev-cases/` — seven precision-format development fixtures and `cases.json`; current manifest SHA-256: `a276b1d07f9686e90c81fce91ebc7c044b64d83086f81c028830444a7cf1cdbf`.
- This report.

Implementation work was done in `/tmp/mado-r20-TwRuleB` at `e629f731172b8238caffe50f152217ce56535fb4`; its starting tool SHA-256 was `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`, and the final patched-copy SHA-256 is `51b20dc48b6722677939fa979cfd04b829bf48dea28a4f39f97f3d39b2c5566a`.

## Behavior changed

- Every `--scan` finding row now carries `evidence: "observed"` or `"lead"`. Ordinary shell/literal-spawn findings and reachable visible-helper spawns are observed; literal positional argv handed to unresolved bare/imported external callables is a lead. Duplicate class/rule hits on one tool call prefer observed if either path is observed. Verdicts include integer `observed_findings` and `lead_findings`, including zeroes in scan-error/usage payloads. See `/tmp/mado-r20-TwRuleB/tools/mado-tripwire.py:1896` and `:1925-1943`.
- A per-file Python binding environment now travels alongside the existing literal environment across py eval cells and is cleared by `reset`. Statement snapshots make the latest preceding binding win. Def/async-def/lambda/class/import/assignment/delete bindings are tracked; helper bodies are prepared using bindings in effect where the enclosing call runs. Literal helper argv flows through positional, keyword and `**kw` forwarding; unknown non-argv parameters remain unresolved rather than suppressing a known literal argv. Direct aliases of `subprocess` spawn functions and spawn-wrapped `functools.partial` values are recognized. See `:1387-1455`, `:1506-1561`, and `:1564-1630`.
- V1 exempted pure builtin/stdlib calls only while not rebound and treated every `del` as unresolved. V2 now restores builtin lookup after deleting a builtin shadow; deleting a non-builtin name remains unresolved. Visible helper/class behavior and selftest evidence comparison are unchanged.
- The module docstring now describes cross-cell helper binding, evidence totals, and the four-helper-hop/static-dispatch limits (`:35-49`, `:86-87`, `:101-103`). `classify_git` and `classify_jj` were not edited.

## Retained evidence

- On a fresh clone checked out at `e629f73`, ran:
  `git -C /tmp/mado-r20-TwRuleB-check apply --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/patches/TwRuleB.patch`
  Result: exit 0, no output. Patch header evidence is `TwRuleB.patch:1-4`.
- The development cases cover builtin frozenset purity, namedtuple construction, a builtin-name spawn rebind, builtin restoration on `del`, reset of a custom helper, imported external leads, and cross-cell `**kw` wrapper observation. Their `before` fields are source-based predictions marked `[INFERENCE]` in each case's `why`; they were not measured.
- Source-inspected likely suite incompatibility [INFERENCE]: round-19 `r19-helperfn/expected.json:118-122` expects `py-helper-redefined` clean, while `py-helper-redefined.jsonl:1` defines `run` twice with the same `os.system` spawning body before calling `run('pacman -S wayland')`. Under E3's latest-preceding binding, the second visible body is followed and should yield observed `host_mutation/pacman:-S` on line 1. This case does **not** encode the old unmarked-lead defect. Proposed suite-only edit for L1: change that expectation to exit 1 / `findings` with one `host_mutation`, `pacman:-S`, line 1, `evidence: observed`, and explain that the second definition is now authoritative. I did not edit the lane suite, and did not run it.

## Limits

- Per the fleet leaf instruction to skip tests while this editing wave is in flight, I did **not** run the 11 existing `--selftest` suites, the round-19 recall counter, the 20 control-line scan, the CriticC3W2 12-shape battery, or any other tests. No suite tallies or control/recall results are claimed; L1 owns post-integration verification.
- The four-helper-hop limit leaves deeper visible helper chains unresolved; the task contract defines purity only through depth four but does not specify the expected row beyond it [UNK]. Dynamic dispatch, inherited/indirect methods, metaclass/descriptor behavior, non-literal spawn arguments, and commands in written-then-run scripts remain outside this static pass.
- The development-case `before` values remain unmeasured [INFERENCE]; run the round-20 counter on both pinned revisions before using them as measured receipts.

## Installs

none

# V2 — f3da504 precision fixes

V2 is delivered as `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/patches/TwRuleB-v2.patch`, SHA-256 `be214cfcc7574f524470ff394aeb2629adc70fe0070fcf3f0866906e0d992277`. It is a unified diff against `f3da50488661509ce5d144c90f7780f8088e0903` (`tools/mado-tripwire.py` blob was the same `367be947...` starting tool), with only `tools/mado-tripwire.py` changed. Its header is `TwRuleB-v2.patch:1-4`. Final patched-copy SHA-256: `945e6eded74d18984bf29c7b9abcaa6d13db1bfb23a94cc8098f501abee96355`.

## V2 behavior changes

- `literal_value` expands literal `*args` sequences; spawn analysis expands positional `*argv`. Literal varargs now flow through `def *args` and `lambda *args` wrappers, including visible async helper bodies.
- Helper parameters whose actual value is unknown are tracked as callable parameters, not inert data. A literal host argv passed to that parameter is a `lead`; literal non-callable parameter values remain data. Helper call arguments are folded against the call-site literal environment, so a visible literal list assigned before a helper call can reach its body.
- A bound method of a string literal is pure when assigned to a name (for example `show = '..{!r}'.format`). Attribute calls such as `pytest.param([...])` do not become leads; a bare unbound `expect([...])` still can.
- Deleting a global builtin-name shadow restores Python's builtin lookup (e.g. `del print` or `del list` returns to the pure builtin); resetting a Python kernel likewise restores builtins. Deleting a non-builtin helper/import leaves an unresolved name and a literal argv call is still a lead.
- Per-toolCall dedup now keys on `(class, rule, evidence)`, preserving an observed and lead row of the same class/rule on one transcript line.

## V2 retained check and gates

- On a fresh clone at f3da504, ran `git -C /tmp/mado-r20-TwRuleB-v2-check apply --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/patches/TwRuleB-v2.patch`; exit 0, no output.
- L1's direct message reports the v1 tool at `125/175` overall with H pending a sibling patch; that is a parent-reported pre-v2 result, not a v2 counter result. V2 counter JSON summary: **[UNK] not run; no counter JSON output retained**.
- The 11 `--selftest` suites and `tw-recall.py` were **not run by this seat**. N/N suite tallies and recall rows are **[UNK]**, not passes. The 20 control lines and 12 CriticC3W2 shapes were also not run. The higher-priority fleet editing-wave instruction prohibits test execution here; L1 owns these gates.

## Round-19 helper-suite expectation changes

These are source-derived predictions, not measured suite failures [INFERENCE]. I did not edit `r19-helperfn/`:

| Case | V2 finding to expect | Reasoned expectation edit |
|---|---|---|
| `py-helper-defined-after-call` (`expected.json:111-115`, fixture `py-helper-defined-after-call.jsonl:1`) | `package_query/pacman:-Q`, line 1, `lead` | The call precedes the visible definition; at the call site the name is unresolved. Change clean to exit 1 / `findings` with this lead row. |
| `py-helper-redefined` (`expected.json:118-122`, fixture `py-helper-redefined.jsonl:1`) | `host_mutation/pacman:-S`, line 1, `observed` | E3 makes the latest preceding definition authoritative. Change clean to exit 1 / `findings` with this observed row. |
| `py-helper-vararg` (`expected.json:125-129`, fixture `py-helper-vararg.jsonl:1`) | `package_query/pacman:-Q`, line 1, `observed` | Literal vararg values now expand through the visible spawn wrapper. Change clean to exit 1 / `findings` with this observed row. |
| `py-helper-default-nonliteral` (`expected.json:146-150`, fixture `py-helper-default-nonliteral.jsonl:1`) | `package_query/pacman:-Q`, line 1, `observed` | The unknown default for `timeout` does not hide the explicit literal argv passed to `subprocess.run`. Change clean to exit 1 / `findings` with this observed row. |
| `py-helper-nonliteral-arg` (`expected.json:103-108`, fixture `py-helper-nonliteral-arg.jsonl:1`) | `package_query/pacman:-Q`, line 1, `observed` | `cmd` is assigned a literal argv in the transcript and resolves in the call-site literal environment. Change clean to exit 1 / `findings` with this observed row. |

None of these five predicted changes is the old unmarked-lead defect: the first is a lead whose body is unavailable at that call site; the other four have visible execution paths and are observed. The proposed edits reflect the new declared semantics. [INFERENCE]

## Class-method case

I left `W-CaseWrapperForms-class-method-instance` unchanged. From its fixture (`class-method-instance.jsonl:1`), V2 should report `package_query/pacman:-Q`, line 1, `observed`: `Runner().run([...])` resolves to a visible instance method whose body passes the literal argv to `subprocess.run`. This follows the visible execution path required by E1 rather than suppressing the finding to preserve the case's stated-miss expectation. [INFERENCE]

## V2 limits

Counter, suite and recall results remain [UNK] because they were not run. The case changes above are inferred from the committed fixture source and V2 resolver, not measured. The previous four-hop and dynamic-dispatch limits still apply.

## Installs

none