# FalsifyC129 — CapturePartialGlobalLateActual

## Verdict and findings

**Verdict: agree**, limited to the sealed `CapturePartialGlobalLateActual` case on delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, selected detector SHA-256 `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce`.

**Actionable findings by severity: none in this case.** Independent static reasoning agrees with the original exact expectation, and the single authorized measurement returned exactly that complete class/command/evidence multiset with both error counters zero. This is author-lane advisory evidence, not non-author admission or an admission grant.

Axes checked: **command/class precision; true-command recall; callable identity and capture-versus-invocation lifetime; observed/lead calibration and explicit uncertainty; sealed artifact identity and bounded measurement scope.**

## Independent semantic truth

Original proposal: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CapturePartialGlobalLateActual.json:2-18`. Inert scanner input: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CapturePartialGlobalLateActual.jsonl:1`. The matching sealed entry is `.cases[] | select(.id == "CapturePartialGlobalLateActual")` in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json`.

- `run_helper` is a module-level function. Its `ARGV` access is a module-global lookup when its body is called, not a lexical local captured from `make_partial`.
- `make_partial()` returns `functools.partial(run_helper)` with **no fixed arguments or keywords**. This retains the helper callable; it neither invokes that helper nor captures the helper body's current module-global values.
- The early list is bound while the partial is created, but the module subsequently rebinds `ARGV` to `["pacman", "-Q", "r22-partial-global-late"]` before the sole `bound()` call.
- Consequently the only reachable spawn-shaped operation passes the late list to `subprocess.run`. There is no conditional return/target, dynamic expansion, unknown argument, mutation of a shared list, asynchronous scheduling, cancellation or opaque namespace write in this source.

The independently justified complete expected multiset is therefore:

| Multiplicity | Class | Command | Evidence |
|---:|---|---|---|
| 1 | `package_query` | `pacman -Q r22-partial-global-late` | `observed` |

No early `pacman -S r22-partial-global-early` row belongs at **any** evidence tier. No additional row belongs in this exact case. Here `observed` denotes the scanner's statically followed, fully bound call path; the fixture was never executed and this is not evidence of a real package query.

The sealed case has `expected_kind: exact`, `accept_exact_want: null`, no addenda/correction, and an explicit observed-only early-command prohibition. Although `forbid_commands_any_tier` is empty for this exact case, complete multiset equality also rejects an extra early **lead**, an early observed row, a late-command lead replacing the observed row, any duplicate, or a lost true row. A parsed-clean empty result would fail. This is not an uncertain case accepted through an `accept_exact_want` alternate. The general unknown-case branch applies all-tier prohibitions before either exact-alternate acceptance or explicit-uncertainty evaluation; it was read, not exercised by this measurement.

Contract references: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/supported-forms.md:7-9,13-22`; canonical comparison `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:683-778`, especially exact equality and zero-unparsed enforcement at lines 749-756.

## Relevant changed behavior and caller path

Reviewed the actual detector diff from registered base `741122d177ae8ff68a73768777f20484d5bdcbe4` to delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, restricted to `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`, plus the following relevant current definitions/callers:

1. `assignment_binding` resolves the factory-call result and retains helper metadata (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1839-1861`); straight-line assignment stores that resolved identity (`:1928-1937`).
2. New `factory_result` resolves the actual returned value after replaying the factory prefix, then restricts retained overlays to factory-bound/local names (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1642-1684`). Here the factory has no parameters or prefix local bindings, so `ARGV` is not frozen into its returned helper metadata.
3. Partial resolution keeps the wrapped helper identity and captures only the explicit fixed argument/keyword expressions (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1761-1769`); both tuples are empty here. This distinguishes capturing a callable from capturing its future global reads.
4. `statement_snapshot` follows the stored helper's AST and includes reachable names, so `ARGV` remains present in the snapshot for the later `bound()` invocation (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2163-2200`). `prepare_eval_calls` snapshots before each statement and applies the intervening literal rebind in source order (`:2217-2253`).
5. `spawn_scan` uses that call-site snapshot and overlays only retained lexical captures (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2456-2466,2510-2516`). It follows the zero-argument helper through `follow_helper`, using the current call environment (`:2556-2580,2407-2439`), and resolves the spawn argument with `literal_value` (`:2632-2643,2675-2684`). Partial construction is not treated as execution of the referenced helper body (`:2721-2728`). `pacman -Q` maps to `package_query` (`:738-772`).

Thus the actual changed path preserves the helper identity without over-freezing the unrelated module global. The observed late row is supported by this path, not inferred merely from a green harness result. The checked in-scope failure modes—stale early observation/lead, lost query, wrong returned identity and silent empty output—did not occur. There is no conditional target in this fixture, so this result does not establish conditional-target correctness elsewhere.

Original F1/F2 authority was read at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:7-17,53-60,70-83`. Those original r21 red observations remain authoritative; neither the old tool nor its original probes were rerun. This late-bound-global opposite guard is not equivalent to proving all F1/F2 variants repaired.

## Authorized measurement and actual rows

Executed once:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CapturePartialGlobalLateActual
```

Raw receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC129/result.json`. It retains the outer exact argv, exit, stdout, stderr, parsed measurement, child argv/exit/stdout/stderr, and before/after hashes. The runner's own reconstructed `argv` omits the interpreter's `-I` option because it uses `sys.argv`; the receipt's outer `argv` preserves the actual authorized invocation, and the scanner-child argv independently includes `-I`.

| Actual result | Value |
|---|---|
| Measurement status / exit | `complete` / `0` |
| Cases scanned | `1`, only `CapturePartialGlobalLateActual` |
| Case comparison | `pass: true`, `reasons: []`, totals `1/1` |
| Actual complete rows | `[{"class":"package_query","command":"pacman -Q r22-partial-global-late","evidence":"observed"}]` |
| Row identity | sealed fixture's absolute path, line `1`, tool `eval`, tool-call id `CapturePartialGlobalLateActual-0` |
| Finding details | `argv0: pacman`, `rule: pacman:-Q` |
| Observed / lead totals | `1` / `0` |
| `eval_unparsed` / `unparsed_spawns` | `0` / `0` |
| Scanner child exit | `1` — expected finding/unpermitted classification with an empty permit list, **not** evaluation failure |
| Scanner error | `null` |
| Outer / scanner stderr | both empty |
| Counts | `package_query: 1`; host mutation, live probe, tool install and VCS write all `0` |
| Integrity errors / drift | `[]` / none |

The canonical runner sets `RLIMIT_AS` to `402653184` bytes and a 15-second timeout for its single scanner child (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:643-661`). Exact case selection is at lines 803-810; lines 829-851 execute only selected cases. Before/after population verification and outcome selection are at lines 798-824 and 854-874. Both integrity snapshots verified 57 input files, 52 proposal files and 106 sealed source files; **that is integrity validation, not 57 semantic scanner runs or a 57/57 result**.

### Identity receipts

Each digest below matched before and after the single run:

| Artifact | SHA-256 |
|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CapturePartialGlobalLateActual.jsonl` | `92adf22420bd3a7cc7b207848837ef3cbf9a97ae639bff0b2d909028b50d9c09` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py` | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CapturePartialGlobalLateActual.json` | `d688b5734d01b597d5f0ec796fb7debca6d1e5c82251174f9aaf17b6e06c0833` |

The normalized expected file explicitly says it was materialized later from the prior raw truth seal; its own digest is pinned separately and was **not** part of that original raw seal. This measurement does not retroactively claim otherwise.

## Residual risk and verification gaps

- This is exactly one finite, straight-line, zero-fixed-argument returned-partial case. It establishes neither global semantic completeness nor saturation of lifetime, arbitrary callable identity, conditional target, nested capture, mutation, scheduling or unknown-case forms. No extra probe was authored or run.
- No full oracle/corpus rerun, historical precision suite, removal/addition comparison, resource population, C2 audit, build, lint, formatter or generic smoke was run. Other C1 acceptance criteria and all C2 conclusions remain outside this seat's measurement.
- `xd://lsp` is unavailable: the device returned `No such tool: xd://lsp`. Therefore server status, references, definitions and diagnostics could not be requested. Source/diff reads and literal grep were the fallback; grep was only navigation, not semantic proof.
- Production, fixtures, expectations and proposals were not edited. Only the assigned report and receipt were written. No tools were installed or updated, no old scanner was invoked, and no package/service/compositor/live probe was executed.
- This agreement does not erase the r19/r20/r21 rejected-harmed receipts or the rejection streak, satisfy required outside-lane admission falsification, grant host clearance, or transfer L1 planner/integration/closure authority.

Report: .ufo/waves/round-22/w2/reports/FalsifyC129.md
