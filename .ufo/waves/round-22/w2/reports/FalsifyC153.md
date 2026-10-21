# FalsifyC153: OriginalF3ReturnedRebound (C1, exact, one-case run)

Seat: MadoR22.FalsifyC153. Role: leaf falsifier, read-only on production, fixture, expected and gate files. No subagents, no installs, no other scanner runs.
Delivered revision: 71228fd582d6d9338d7916cc64e69bd4c2e928b5.
Authority: round-21 FinalBindingReview.md (F3) remains source authority. The r21 red was not rerun with any old tool.

## Verdict

**AGREE** (this one case only). The sealed exact expectation, my independent Python-semantics derivation, and the current scanner's output coincide. The case passes with the complete multiset and zero error counters.

Admission: **none granted**. This is one of 57 frozen cases. Author-lane advisers cannot grant admission. Scope limits are in the last section.

## Sealed case (read from oracle/expected.json; not edited)

| Field | Value |
|---|---|
| id / group | OriginalF3ReturnedRebound / supplemental-original |
| expected_kind | exact |
| want | `host_mutation`, `pacman -S r21-b`, `observed` |
| accept_exact_want | null (no uncertain alternate) |
| forbid_observed_commands / forbid_commands_any_tier | [] / [] |
| require_signal | true (not consulted by the runner for exact kind; inert here) |
| cell_count / cell_reset | 1 / [false] |
| fixture / input_sha256 | inputs/OriginalF3ReturnedRebound.jsonl / 774e2946d16c23d9ebdd557ccf279143f6d2249dc7132aa567fb34d12d3d7573 |
| historical_r21 | old red row `package_query`, `pacman -Q r21-a`, `observed`; note "wrong closure body; host_mutation missing" |
| proposal / correction | null / null |

Provenance chain, checked by sha256:
- round-21 `FinalBindingReview.md` line 57 (F3 row: truth `pacman -S r21-b`, observed; old row `pacman -Q r21-a`, observed); section F3 at lines 85–88.
- `.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/returned-rebound.jsonl` = 774e2946… (byte-identical to the sealed fixture).
- `oracle/measure.py` ORIGINALS table lines 53–58: same sha, same want, table F3.
- `oracle/expected.json` case record: same sha, same want. The runner's `verify_original_cases` cross-checks these.

Fixture content, quoted as inert data. It is never executed:
```python
import subprocess
def make():
    def a():
        subprocess.run(["pacman", "-Q", "r21-a"])
    def b():
        subprocess.run(["pacman", "-S", "r21-b"])
    a = b
    return a
make()()
```

## Independent expectation (derived from Python semantics before the run)

- `make()` runs its body: `def a` and `def b` bind local function objects; `a = b` rebinds local `a` to the `b` object; `return a` returns the `b` object.
- The module-level `make()()` then calls the `b` object. Its body runs `subprocess.run(["pacman","-S","r21-b"])`, one unconditional literal spawn.
- The `a` body (`pacman -Q r21-a`) is never invoked. Its def does not run merely because a factory returned another helper.
- Complete expected multiset: `{(host_mutation, "pacman -S r21-b", observed)}`. No lead rows. `eval_unparsed` 0. `unparsed_spawns` 0. No parse errors.
- Uncertainty boundary: none required. No dynamic argv, no unresolved target, no branch, no mutation of `subprocess` after binding, no invalid call. An uncertain or lead output would be a false lead, and the exact multiset rejects it.

This matches the sealed expectation and the round-21 truth row.

## The one run (exact commands and results)

Command: `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case OriginalF3ReturnedRebound`, cwd the repo root, invoked via a Python subprocess wrapper that recorded argv, exit and raw stdout/stderr. Elapsed 0.111 s.

- Runner exit: 0. Runner stderr: empty (0 bytes). Runner stdout: 5444 bytes, one JSON line.
- Runner population validation (`verify_population`, before and after): 106 sealed sources, 52 proposal files, 57 inputs. `integrity_errors` = []. Population sha256 046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad.
- Totals: pass 1 / total 1. Runner `final_exit` 0.
- Child cap, applied in code by `scan()` (measure.py 26–27, 655–680, 643–644): one child, `RLIMIT_AS` 384 MiB (402653184 bytes), timeout 15 s, concurrency 1. Only one child was spawned, for the selected case.
- Child argv: `/usr/bin/python3 -I -c <WRAPPER> tools/mado-tripwire.py <fixture>`.
- Child exit: 1 (findings present, unpermitted 1). Child stderr: empty.
- Child stdout: `MADO_TRIPWIRE: findings`, then JSON. `counts` host_mutation 1, all other classes 0. `observed_findings` 1. `lead_findings` 0. `unpermitted` 1. `files[0]`: lines 1, eval_calls 1, bash_calls 0, eval_unparsed 0, unparsed_spawns 0, sha256 774e2946…
- Finding row: class `host_mutation`, command `pacman -S r21-b`, evidence `observed`, argv0 `pacman`, rule `pacman:-S`, line 1, tool_call_id `FBR-returned-rebound`, timestamp string `"None"` (see observation C).
- Row comparison:

| Source | class | command | evidence |
|---|---|---|---|
| sealed want | host_mutation | pacman -S r21-b | observed |
| actual | host_mutation | pacman -S r21-b | observed |
| extra rows | none (including no `pacman -Q r21-a` at any tier, no lead) | | |

Hashes (sha256), before and after the run; drift in every case = none:
- tools/mado-tripwire.py (selected tool) 36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce. Matches the C1 identity pin.
- oracle/measure.py (runner) 41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7.
- oracle/assemble.py (producer) 0270c10b90828a895ae3f0a5dec8b2c5610f960a2c1d994aa9409cad702c5600.
- oracle/expected.json b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357. Pin file 7cc4aae9017a157faea3d66e47b5bc0181ec9093a3160d1c41d8e2e93b1567f6.
- truth-seal.json 47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4.
- fixture inputs/OriginalF3ReturnedRebound.jsonl 774e2946d16c23d9ebdd557ccf279143f6d2249dc7132aa567fb34d12d3d7573.
- r21 source returned-rebound.jsonl 774e2946d16c23d9ebdd557ccf279143f6d2249dc7132aa567fb34d12d3d7573.

Note on the tool digest: the C2 identity (tools/mado-evidence-audit.py 277eced2…) was not touched or run.

Receipt: `.ufo/waves/round-22/w2/receipts/FalsifyC153/result.json`. It holds argv, cwd, exit, raw stdout and stderr with sha256 and byte counts, the parsed runner JSON, all before and after hashes, and drift flags.

## Falsification attempts for THIS case

1. **False observed or lead argv.** Not found. The only row is the true spawn. No `pacman -Q r21-a` row exists at any tier, so the old wrong row does not return. Mechanism: `factory_result` (tools/mado-tripwire.py 1642–1684) replays the factory prefix with `prepare_eval_calls` (2203–2254) and `update_bindings` (Assign branch 1928–1937). `a = b` rebinds `a` to the `b` helper before `return`, so the `a` body is never selected.
2. **Lost true command.** Not found. `pacman -S r21-b` appears exactly once, with class, evidence and text correct.
3. **Wrong identity.** Not found in the output. Mechanism is execution-order rebinding, not a def-name index. Limit: in this fixture the rebinding RHS `b` is also the last-defined helper, so "binding in effect at return" and "last-defined helper wins" give the same answer. The case does not discriminate those two. See proposal A.
4. **Lifetime.** Nothing falsified, but largely untested. The closure outlives the factory frame and reads the free global `subprocess` through the call-site snapshot (`follow_helper` cbindings). `subprocess` is never rebound and invocation is immediate. The case does not exercise late rebinding of globals after creation, delayed or stored-then-invoked calls, or cross-cell persistence.
5. **Conditional target.** Not applicable. No branch, loop, or conditional return. No uncertainty row is produced and none is required.
6. **Parsed-clean ambiguity.** Not present. The zero unparsed counters accompany a positively resolved spawn. The verdict label is `findings` with exit 1, not `clean`.
7. **Exact versus uncertain distinction.** This case is exact. `accept_exact_want` is null and the forbid lists are empty. Any extra row, including a lead, fails the exact multiset, so the wrong r21 row is rejected at every tier by the multiset alone.

## Observations (harness and tool; not failures of this case)

A. **Runner exact check does not cross-check the verdict.** `parse_scan_output` (measure.py 683–729) reads only `findings` and `files`, and accepts any child exit in {0,1}. `evaluate` (736–756) compares rows and unparsed only. A child that printed `MADO_TRIPWIRE: clean` with exit 0 and the same finding list would pass this case. This is inferred from code and was not executed. Verdict fields are at tools/mado-tripwire.py 2909–2919 (`verdict_of`, `emit`).
B. **`require_signal` is not enforced for exact cases** (evaluate 752–756). It has no effect here.
C. **Timestamp fidelity.** tools/mado-tripwire.py line 2890 writes `str(None)` when the transcript has no timestamp, so the row carries the string `"None"`, not null. The runner does not read this field. Provenance nit only.
D. **Runner compares command text, not argv.** argv0 and rule are not compared. Both are correct here.

## Scope versus the C1 target

- Covered: one of the 57 frozen cases (the r21 F3 repro, supplemental original). One child, one run, 0.111 s total.
- Not covered: the other 56 cases; F1, F2, F4, F5 families; the 50 proposal expectations; the historical 166/175 guard (floor 166); oracle35+17; incident recall; resource recipes; the 1356-fixture removal/error comparison; the closure-heavy resource population; r20 tw-precision; the C2 audit.
- The C1 "eligible frozen expectations all match" target is not evidenced by this report.

## Proposals for L1 (not executed by me; for private sandbox only)

- **Proposal A (discriminator).** A variant with the reversed def order, `def b` first, then `def a`, then `a = b; return a`. Truth: r21-b body. Def-name index → `a` body. Last-defined → `a` body. First-defined → `b`. Together with the sealed case this separates three heuristics. L1 should check whether the frozen population already has such a discriminator, without relying on this report.
- **Proposal B (verdict mutant).** Make `verdict_of` return exit 0 while findings remain. Predicted from code: the exact runner still passes this case (Observation A). L1 to confirm in a private sandbox.

## Trailer

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC153.md
Receipt: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC153/result.json
Admission: none granted.
