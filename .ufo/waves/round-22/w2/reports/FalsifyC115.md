# FalsifyC115 — C1 CXRecursivePartialFactory

## Findings by severity and recommendation

**Verdict: agree with the sealed uncertain expectation, for this case only.** No actionable high/medium/low detector mismatch was found in the one authorized measurement. This is an author-lane advisory recommendation, not non-author admission, a canonical judgment, desktop clearance, or a change to the r19/r20/r21 rejected-harmed receipts or streak.

**Informational source-rationale precision:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CXRecursivePartialFactory.json:11` says that calling the outer partial “unwinds the chain.” In the cited CPython source, recursive `make(n - 1)` is evaluated during factory construction; `_partial_new` flattens a partial passed as its callable (`/usr/lib/python3.14/functools.py:329-346`). The final invocation forwards the captured arguments (`:380-393`). This does not change the proposed class, command, uncertainty, or pass condition, but the implementation-level explanation should not be treated as literal evidence of invocation-time recursion. Original sealed text was not modified.

## Axes and scope

Axes examined: (1) class/command/evidence precision and potential-command recall; (2) callable identity, capture lifetime, and conditional return semantics; (3) explicit uncertainty versus invented observation or false parsed-clean claims; (4) bounded termination and immutable evidence identity.

The target is the supplied delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, specifically the current `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` bytes matching the assigned SHA-256. I reviewed the relevant callable/factory diff from base `741122d177ae8ff68a73768777f20484d5bdcbe4` to that revision, the selected sealed case, its original proposal and cited I7/V11 source, and the runner's relevant evaluation/cap logic. This is not a whole-diff, whole-corpus, C2, or no-harm certification.

`read xd://lsp` returned **“No such tool: xd://lsp”**; no LSP device is mounted. Therefore semantic references/definition/diagnostics requests were unavailable. Searches below were literal navigation followed by direct source reads, not semantic absence proofs.

## Independent expected semantics

The exact sealed record is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json:749-788`; the original proposal is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CXRecursivePartialFactory.json:2-12`. The input contains one Python eval cell, reset false.

Static reasoning, without executing the payload:

- `n = int(os.environ.get("R22_CXREC", "1"))` is not fixed by source. The default string `"1"` is not proof of the environment value.
- If conversion succeeds and `n <= 0`, `make` returns `functools.partial(run, ["pacman", "-S", "r22-cxrec"])`; the final call can reach `subprocess.run` with that exact argv. A sufficiently small positive integer, including the default 1, recursively reaches the same base return during construction and can reach the same invocation.
- An invalid integer string can raise `ValueError` before `make`; sufficiently deep positive recursion can raise `RecursionError` before any spawn. No exact recursion threshold is claimed.
- Therefore the potential command is **`host_mutation` / `pacman -S r22-cxrec`**, but its evidence cannot be `observed` from this source alone. This is genuine runtime-dependent uncertainty, not a definitely invalid call and not an exact no-execution case.
- `want: []` is not an exact-empty result assertion here. The sealed fields are `expected_kind: uncertain`, `accept_exact_want: null`, `require_signal: true`, `forbid_observed_commands: ["pacman -S r22-cxrec"]`, and `forbid_commands_any_tier: []`. Any observed row fails the uncertain rule; this case has no accepted-exact alternate. A lead for the literal command would be defensible but is not required; positive unparsed uncertainty with no rows is also allowed. There is no borrowed-global command to forbid at all tiers in this particular input, and the actual empty row multiset invents no argv at any tier.

The independent source citation `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/notes/ConnLifetime.json:47,75` supplies I7 (per-resolution owner-id boundedness) and V11 (an unconditional self-referential factory). V11 is not semantically identical to this environment-dependent/base-case variant; its exact no-process truth must not be substituted here. The frozen return documentation `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-simple_stmts.rst:494-497` supports eager return-expression evaluation and return identity.

## Current relevant path

The delivered implementation adds the bounded factory resolver. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1642-1646` returns `kind: uncertain` when the same factory owner is already resolving or the descent bound is reached. It passes the extended owner stack through prefix preparation and return resolution (`:1674-1675`). `callable_info` propagates that stack through partial's wrapped callable (`:1757-1775`) and through helper-factory resolution (`:1780-1783`). The consumer increments unparsed and stops that call path for `kind: uncertain` (`:2461-2464`).

[INFERENCE from these definitions and callers] This preserves uncertainty when resolving the recursive returned partial rather than selecting the conditional base-case helper as a definite target or following self-resolution indefinitely. The measurement below independently establishes bounded completion and the resulting counters, not a traced execution of every resolver branch. No rows are promoted from the literal base return, and no exact callable/capture reconstruction is claimed. This fixture has no Thread/Timer target and does not establish scheduled-call correctness or cross-cell capture coverage.

## Sole authorized measurement and actual rows

Executed exactly once:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CXRecursivePartialFactory
```

The runner caps its scanner child at **402653184 bytes (384 MiB) RLIMIT_AS and 15 seconds** (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:643-660`). Its exact-case filter selects one record (`:803-810`); its selected-case loop launched one child (`:828-852`). Integrity validation of all 57 input files is not 57 scanner executions. No additional scanner, old-tool reproduction, new source probe, fixture execution, test suite, build, lint, formatter, or generic smoke was run.

Actual result:

```json
{
  "runner_exit": 0,
  "scanner_exit": 0,
  "pass": true,
  "got_rows": [],
  "observed_findings": 0,
  "lead_findings": 0,
  "eval_unparsed": 0,
  "unparsed_spawns": 1,
  "scanner_error": null,
  "reasons": [],
  "stderr": ""
}
```

All five class counts were zero; the reported fixture path and SHA-256 matched the selected input. The runner reported `totals: {"pass": 1, "total": 1}`, `status: complete`, no integrity errors, and identical before/after integrity values. Captured wall duration was approximately 0.105 seconds; this is not a peak-memory or asymptotic measurement.

The runner checks forbidden commands before acceptance, exact cases by complete sorted class/command/evidence multiset plus zero unparsed, and uncertain cases by complete accepted-exact equality or no observed rows plus the required uncertainty signal (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:736-778`). Here the positive unparsed count, not an accepted-exact alternate or an invented lead, accounts for the pass.

## Evidence identity

Independent `sha256sum` calls before and after the measurement matched all five values below; runner integrity agreed. **No drift observed.**

| Artifact (absolute path) | SHA-256 before = after |
| --- | --- |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py` | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CXRecursivePartialFactory.jsonl` | `0e29e3be777cf89d87af23a9afe110a33d689ee514d47408f79258305f7b3eac` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CXRecursivePartialFactory.json` | `58aa71a7f0b9041f7536102f025773ce4a2b40d2a88d1ef1d472debea8f8fb64` |

The cited host `/usr/lib/python3.14/functools.py` matched its proposal digest `9db56d38172c4c9e689b21cc58c8538008b09d86b682faf4dd193b529cdd79d5`; it is supplemental read-only host source, not a newly frozen wave artifact. The frozen return document digest was `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`; ConnLifetime note digest was `8269d02dc5ac49ad05b018715611446b15c815fcea0258d745b288adb7fa8ebe`.

Raw receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC115/result.json`. It retains the exact external argv including `-I`, process exit, unmodified runner stdout/stderr, nested scanner argv/exit/stdout/stderr and payload, counters, and hashes. The runner's self-reported argv omits the interpreter's `-I` flag because it reconstructs argv from `sys.argv`; the separately captured invocation preserves it.

## Residual risks and verification gaps

- The actual scanner banner is **`MADO_TRIPWIRE: clean`**, but `unparsed_spawns: 1` makes this an **uncertain, not parsed-clean** result. This is compatible with the existing documented CLI contract (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:30-37,133-137`): `clean`/exit 0 means no finding/no unpermitted finding, not no host command. Any downstream claim of semantic cleanliness from this banner or the harness pass alone would contradict this receipt. No such clearance is granted here.
- The zero rows do not prove the possible command cannot execute, nor prove all recursive/conditional return shapes are repaired. Supported-forms boundaries explicitly keep arbitrary recursive/conditional return evaluation outside exact-result claims (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/supported-forms.md:18-22`).
- The specified runner imports the selected module and invokes `main` (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:34-38`); this receipt does not separately exercise the scanner's standalone `__main__` stack wrapper. No second run was authorized or performed.
- No LSP-backed call graph/diagnostics, exact-result sibling cases, historical reds, full no-harm population, resource scaling, C2 arithmetic audit, canonical runtime, rerouting/resume behavior, or saturation claim is established by this scoped measurement. Existing reds remain source authority; they were not rerun to reconfirm them.

Only the assigned report and receipt were written. No production/fixture/expected/source files were changed; no delegates, background jobs, installations, package transactions, or live probes were used. L1 retains planner/integration authority.

Report: .ufo/waves/round-22/w2/reports/FalsifyC115.md
