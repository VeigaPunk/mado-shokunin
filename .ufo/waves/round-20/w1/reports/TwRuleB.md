# TwRuleB — E1/E2/E3 patch prepared; requested suites deferred to L1

## Delivered

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/patches/TwRuleB.patch` — unified diff for `tools/mado-tripwire.py`, with required `a/tools/mado-tripwire.py` / `b/tools/mado-tripwire.py` paths. SHA-256: `9d3487c68ea8e9ffd5ed094890d76261ae1fdff4b8d64ef947aa128d8412782e`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/patches/TwRuleB-dev-cases/` — seven precision-format development fixtures and `cases.json`; manifest SHA-256: `c2e282180e46e391741444107213debecfa6a1c789c9840e5d4bff26a3277481`.
- This report.

Implementation work was done in `/tmp/mado-r20-TwRuleB` at `e629f731172b8238caffe50f152217ce56535fb4`; its starting tool SHA-256 was `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`, and the final patched-copy SHA-256 is `51b20dc48b6722677939fa979cfd04b829bf48dea28a4f39f97f3d39b2c5566a`.

## Behavior changed

- Every `--scan` finding row now carries `evidence: "observed"` or `"lead"`. Ordinary shell/literal-spawn findings and reachable visible-helper spawns are observed; literal positional argv handed to unresolved bare/imported external callables is a lead. Duplicate class/rule hits on one tool call prefer observed if either path is observed. Verdicts include integer `observed_findings` and `lead_findings`, including zeroes in scan-error/usage payloads. See `/tmp/mado-r20-TwRuleB/tools/mado-tripwire.py:1896` and `:1925-1943`.
- A per-file Python binding environment now travels alongside the existing literal environment across py eval cells and is cleared by `reset`. Statement snapshots make the latest preceding binding win. Def/async-def/lambda/class/import/assignment/delete bindings are tracked; helper bodies are prepared using bindings in effect where the enclosing call runs. Literal helper argv flows through positional, keyword and `**kw` forwarding; unknown non-argv parameters remain unresolved rather than suppressing a known literal argv. Direct aliases of `subprocess` spawn functions and spawn-wrapped `functools.partial` values are recognized. See `:1387-1455`, `:1506-1561`, and `:1564-1630`.
- Pure builtin constructors/callables and the specified known-pure stdlib callable families are exempt only when the name is not rebound. Visible pure helpers/classes do not become leads for receiving argv-shaped data; reachable helper bodies, explicit constructors, and directly resolved class methods are followed. `del` leaves an explicit unresolved binding so a literal argv call becomes a lead. The selftest compares evidence only if any expected finding supplies it (`:2356-2362`).
- The module docstring now describes cross-cell helper binding, evidence totals, and the four-helper-hop/static-dispatch limits (`:35-49`, `:86-87`, `:101-103`). `classify_git` and `classify_jj` were not edited.

## Retained evidence

- On a fresh clone checked out at `e629f73`, ran:
  `git -C /tmp/mado-r20-TwRuleB-check apply --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/patches/TwRuleB.patch`
  Result: exit 0, no output. Patch header evidence is `TwRuleB.patch:1-4`.
- The development cases cover builtin frozenset purity, namedtuple construction, a builtin-name spawn rebind, delete/reset unbinding leads, imported external leads, and cross-cell `**kw` wrapper observation. Their `before` fields are source-based predictions marked `[INFERENCE]` in each case's `why`; they were not measured. They are not a substitute for running the precision counter.
- Source-inspected likely suite incompatibility [INFERENCE]: round-19 `r19-helperfn/expected.json:118-122` expects `py-helper-redefined` clean, while `py-helper-redefined.jsonl:1` defines `run` twice with the same `os.system` spawning body before calling `run('pacman -S wayland')`. Under E3's latest-preceding binding, the second visible body is followed and should yield observed `host_mutation/pacman:-S` on line 1. This case does **not** encode the old unmarked-lead defect. Proposed suite-only edit for L1: change that expectation to exit 1 / `findings` with one `host_mutation`, `pacman:-S`, line 1, `evidence: observed`, and explain that the second definition is now authoritative. I did not edit the lane suite, and did not run it.

## Limits

- Per the fleet leaf instruction to skip tests while this editing wave is in flight, I did **not** run the 11 existing `--selftest` suites, the round-19 recall counter, the 20 control-line scan, the CriticC3W2 12-shape battery, or any other tests. No suite tallies or control/recall results are claimed; L1 owns post-integration verification.
- The four-helper-hop limit leaves deeper visible helper chains unresolved; the task contract defines purity only through depth four but does not specify the expected row beyond it [UNK]. Dynamic dispatch, inherited/indirect methods, metaclass/descriptor behavior, non-literal spawn arguments, and commands in written-then-run scripts remain outside this static pass.
- The development-case `before` values remain unmeasured [INFERENCE]; run the round-20 counter on both pinned revisions before using them as measured receipts.

## Installs

none