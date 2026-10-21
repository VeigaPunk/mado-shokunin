# C1 retained-memory review

Axes: clean-verdict correctness and retained memory (peak RSS); elapsed time and bounded completion are secondary checks.

## Finding — Medium: eager-call snapshots remain quadratic

C1 removes the assignment-only snapshot growth measured before the repair, but the snapshot retention still scales quadratically for wide cells where many statements contain eager calls or references. In `prepare_eval_calls`, the per-statement `dict(env)` and `dict(bindings)` copies are still made whenever `eager_calls([stmt])` returns a call or reference, and `call_env`/`binding_env` retain those copies until `spawn_scan` completes (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1978-2001`). The call path is used by the top-level eval, deferred-body sweep and followed helpers (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2036, 2126, 2191`).

A wide, shallow, 1,000-statement inert cell demonstrates the remaining shape: 500 unique scalar assignments followed by 500 `str(binding_N)` call statements. The assignments grow `env` and `bindings` (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1749-1756`); each `str(...)` is collected as an eager call (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1845-1850`). Thus each of the 500 call statements copies both 500-entry maps, retaining about 500,000 dictionary entries across those snapshots. This is a source-proven O(n²) case, not a claim that the bounded run saturated.

The assignment-only comparison on the exact current candidate used 29,012 KiB peak RSS; the retained-call fixture used 32,324 KiB. Both completed cleanly. The bounded observation confirms the snapshots are not omitted for this call-bearing shape, but it does **not** demonstrate saturation at 1,000 statements or establish a failure threshold. Given the allowed probe limit, no larger variant was run.

## Historical receipts

The committed 1000/2000/4000 assignment-only receipts show the intended improvement. These are historical measurements, not runs of the current candidate:

| Mode / measured code | 1,000 statements | 2,000 statements | 4,000 statements |
|---|---:|---:|---:|
| `module-main`, pre-fix commit `eaec245731926827c72b2fff47cb61afdf5d7c91`, tool SHA-256 `a57d4fe9277ff06c9b5916fc731e91f05bcd69cf05639cb2090ebcb00b5b6458` | clean, 47,164 KiB | clean, 132,160 KiB | exit 1, `MemoryError` in `prepare_eval_calls`, 381,464 KiB |
| `module-main`, post-fix commit `843d301d1b17af78427918f7845af336b2218de0`, tool SHA-256 `56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11` | clean, 20,036 KiB | clean, 23,616 KiB | clean, 29,204 KiB |

The pre-fix CLI receipts at all three sizes returned exit 2 / `could_not_evaluate` with `internal RuntimeError` and no file records; the post-fix CLI receipts returned clean exit 0 at all three sizes. The runner capped child address space at 402,653,184 bytes and wall time at 15 seconds. I did not rerun those historical unsafe loads.

## Current-candidate bounded probes

Exact tested scanner bytes: SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`, identical at current `HEAD` `a8da015624c92f4cb4a7de92adbf6643a3f8b38a` and requested candidate `f499a8db7171b7476fe9f204ab9edbac5a956fa9`. Both probes used the same `module-main` wrapper from `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/resource/measure.py` (SHA-256 `6d0362e1920b8c8f010bd83619f9b6c15fb705a67614a7c9b5d5d314937987d4`) and `/usr/bin/python3.14`, with the runner's 384 MiB / 15 s child limits:

| Input | Fixture SHA-256 | Result | Peak RSS | Elapsed |
|---|---|---|---:|---:|
| 1,000 assignment-only statements | `cada424f6584b7085b8c8ade33d872bf42e10d3bcba9402b8ef0a851de0a0acf` | exit 0, clean, zero findings | 29,012 KiB | 0.032913 s |
| 500 assignments + 500 `str(...)` call statements | `e8ec1d082c2157907c5dc4183bd77e701ca92d04fc9b7c180d33bba86c0f9235` | exit 0, clean, zero findings | 32,324 KiB | 0.042012 s |

For both, measured tool and fixture hashes matched before and after; the child was reaped, did not time out, and stderr was empty. The second fixture is inert JSONL data and was scanned, not executed: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/ResourceMemory-2/retained-calls-1000.jsonl`.

## Review coverage and residual risk

- Verdict: the assignment-only memory repair is effective on its recorded population, but the code still retains O(n²) environment/binding snapshots when many statements carry eager calls/references. Treat any broad claim that the scanner's retained memory is now bounded/linear as unsupported.
- No larger call-heavy probe was run, so observed saturation, a failing threshold, and behavior beyond 1,000 such statements remain unverified. Do not infer an OOM from the 1,000-statement result.
- No `lsp` device is mounted: attempting `read xd://lsp` returned “No such tool: xd://lsp”. The literal `prepare_eval_calls` search was therefore a fallback only; its results are not semantic proof. I read the three current call-site ranges noted above, but LSP references/definition/diagnostics were unavailable.
- No tools were installed or updated. No full suite, corpus, or historical unsafe load was run.

Report: `.ufo/waves/round-21/w2/reports/ResourceMemory.md`
