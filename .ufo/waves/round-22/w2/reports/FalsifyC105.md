# FalsifyC105 — C1 / CX5AfterReturn

## Findings by severity

No actionable defect found in the assigned case on the fixed delivered tool. **Verdict: agree**, bounded to `CX5AfterReturn`; author-lane advisory only, not non-author admission or a round verdict.

Axes: (1) returned-callable identity and lifetime, (2) return reachability and true-command recall, (3) complete class/command/evidence precision, (4) uncertainty/error honesty, and (5) fixed-byte identity and bounded measurement integrity. No production or fixture changes were made, and no new source-shaped probe was introduced.

## Independent semantic judgment

The original proposal is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CX5AfterReturn.json:2-14`. The sealed case in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` retains its exact expectation, with no correction or addendum and `accept_exact_want: null`.

`make` binds `a` and `b` to two distinct nested function objects. Defining `b` does not call it. At `return a`, `a` still denotes the first function; the following `a = b` is unreachable. The assignment makes `a` local at compile time, but the preceding `def a` has already initialized that local. Returning the function object preserves its lifetime after the factory returns. The second call in `make()()` invokes that returned `a` once, reaching the literal `subprocess.run(["pacman", "-Q", "r22-cx5-early"])`.

Source authority is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-simple_stmts.rst:494-503`: evaluate the return expression, then leave the current function call with that value. No `finally`, conditional return, opaque argument, mutable capture, scheduling, or later rebinding complicates this exact text.

Consequently, the **complete expected multiset**, independently reasoned rather than inferred from a green receipt, is:

| Class | Command | Evidence | Multiplicity |
| --- | --- | --- | ---: |
| `package_query` | `pacman -Q r22-cx5-early` | `observed` | 1 |

Zero additional rows and zero parse/unparsed errors are required. `pacman -S r22-cx5-early` is unreachable, including as a lead for this exact case. The explicit sealed forbidden list rejects it as observed; complete multiset equality also rejects it as a lead or any other extra row. Losing the query, downgrading it to a lead, inventing the mutation, or duplicating the query would fail this expectation.

This is not an uncertain case. The manifest's `require_signal: true` does not require an extra lead: the canonical exact branch checks full multiset equality plus zero unparsed and returns before the uncertain-case branch. `accept_exact_want` and the uncertainty escape are not applicable. The distinction is explicit in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:732-778`.

## Delivered diff and relevant path

Reviewed the actual classifier diff from registered base `741122d177ae8ff68a73768777f20484d5bdcbe4` to delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, scoped to `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`.

- The former def-name-index selection and invocation-time `capture_owner` replay are replaced by `factory_result`. Current `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1642-1684` selects the top-level return, prepares only the prefix before that return, and then resolves its expression against those bindings. In this fixture the prefix contains the two defs, never the unreachable assignment, so the result is `a`, not `b`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1748-1783` resolves the immediate factory result; `:1882-1885` installs each def's identity. The closure overlay is consumed at `:2510-2516`, and `:2547-2579` follows the selected helper rather than choosing a helper by its source name again.
- Deferred function bodies are excluded from eager traversal at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1993-2001,2051-2058`; merely binding `b` therefore does not emit its command. The new top-level return break at `:2251-2253` also prevents the ordinary helper scan from replaying statements after this return.
- Existing r21 F3 authority is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:85-88`: the original defect ignores a binding effective **before** the return. CX5 is a complementary guard against replaying a binding **after** it. The original red remains authoritative; no old tool was run and this single guard does not independently remeasure that red.

The source reasoning is textual/manual. `xd://lsp` was unavailable (`No such tool`), so no server status, references, definition, or diagnostics could be obtained. Text search was used only to locate relevant implementation sections, not presented as semantic-server proof.

## Sole authorized measurement and actual rows

Executed exactly once:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CX5AfterReturn
```

The canonical runner's `main` selects one exact case after full-population integrity validation (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:789-839`). Its scanner child uses 384 MiB address-space limits and a 15-second timeout (`:26-27,643-660`); no second scanner child or fixture execution was requested.

Observed results:

- Measurement exit **0**, status `complete`, totals **1/1**, reasons `[]`, integrity errors `[]`.
- Scanner exit **1**, expected for the unpermitted package-query finding, not a parse failure or an oracle failure. Runner and scanner stderr are both empty.
- Actual full row multiset: **one** `package_query / pacman -Q r22-cx5-early / observed`. `observed_findings=1`, `lead_findings=0`, `unpermitted=1`; all other class counts are zero.
- Selected file has `eval_calls=1`, `bash_calls=0`, `eval_unparsed=0`, `unparsed_spawns=0`. Finding identity is the selected absolute fixture, transcript line 1, `tool=eval`, `tool_call_id=CX5AfterReturn-0`, `argv0=pacman`, rule `pacman:-Q`.
- The scanner-reported input SHA-256 equals the sealed CX5 input digest. Canonical pre/post integrity records both verify 57 input files, 52 proposal files, and 106 sealed source files. Those are integrity checks, **not 57 scanner measurements**; only CX5 ran.

Raw runner argv/exit/stdout/stderr, its parsed canonical output, scanner argv/exit/stdout/stderr and payload, and independent before/after hashes are retained at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC105/result.json`. The outer argv preserves the requested interpreter `-I`; the runner's own reported argv is retained unmodified.

### Identity pins

Each following SHA-256 was observed with `sha256sum` before and after the sole measurement; no drift was observed.

| Artifact (absolute path) | SHA-256 |
| --- | --- |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CX5AfterReturn.jsonl` | `37447d955d6a914eeaee604d90b9b9af47a113d03520d83fc3fffca661a5d9f1` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py` | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CX5AfterReturn.json` | `98925a43044075a7320afec0f571a9aec76b91a952e81bba216ca12b1c07e241` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-simple_stmts.rst` | `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc` |

## Residual risk and verification gaps

This receipt supports the declared straight-line executed-return boundary in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/supported-forms.md:7-11,20-22` for this one input. It is not saturation, a whole-family proof, a no-harm corpus comparison, C2 evidence, or host clearance. Conditional/non-Name returns, later mutable/nonlocal capture, Thread/Timer behavior, and reset/resume continuity are not present in CX5 and were not exercised. No alternative runtime, full oracle, generic smoke, build, lint, formatter, fixture command, or installation was run. Static `observed` evidence here identifies a reachable source-shaped spawn invocation; it does not assert that a real package command executed or succeeded.

The separate preimplementation raw-truth seal and later normalized manifest remain distinct; this run's integrity record does not retime normalization or erase prior r19/r20/r21 rejected-harmed receipts and the rejection streak. L1 retains planning/integration authority. No admission is granted.

Report: .ufo/waves/round-22/w2/reports/FalsifyC105.md
