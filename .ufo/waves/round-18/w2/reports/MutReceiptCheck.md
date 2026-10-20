# MutReceiptCheck — round 18, wave 2

## Scope and axes

Target and detector are both pinned to `abfbf35b1ed4d4a1eb294d525ef286be30f3886f`:
`.ufo/waves/round-18/receipt-check.py` and its unchanged
`.ufo/waves/round-18/receipt-claims.json`.

Axes: **calibration** (receipt/producer binding), **operability** (expectation and exit semantics), and **coverage** (the five assigned behavior-bearing points). Isolation and exact-byte restoration are constraints, not claimed score improvements. Read the lane's round-18 declared claims and lesson before probing.

**Result: five formally INCONCLUSIVE probes, not five kills or five proved survivors.** The exact committed detector already fails its baseline: six claims remain `PENDING-L1`, so pristine and restored runs print `EXPECT_SUMMARY: 9/15` and exit **2**. No pending claim was removed, rewritten, or treated as passing. Four mutants were observationally indistinguishable from pristine; the SHA mutant changed three fixture outcomes and the summary, but still exited 2. Those observations are coverage leads, not a green-baseline mutation score. The baseline blocker was sent to `agent://MadoR18`.

## Isolation, command and expected detector

Scratch clone: `/tmp/mado-r18-mutreceiptcheck.mPCyOr`.

Actual setup commands:

```sh
mktemp -d /tmp/mado-r18-mutreceiptcheck.XXXXXX
# output: /tmp/mado-r18-mutreceiptcheck.mPCyOr
git -c core.hooksPath=/dev/null clone --shared --no-checkout --local /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado-r18-mutreceiptcheck.mPCyOr
git -C /tmp/mado-r18-mutreceiptcheck.mPCyOr -c core.hooksPath=/dev/null checkout --detach abfbf35b1ed4d4a1eb294d525ef286be30f3886f
```

The committed checker, claims and three fixtures were also inspected with `git show abfbf35b1ed4d4a1eb294d525ef286be30f3886f:<path>`; the round artifact names were enumerated with `git ls-tree -r --name-only abfbf35b1ed4d4a1eb294d525ef286be30f3886f .ufo/waves/round-18`.

Every behavioral observation used this exact command, with the scratch root as cwd:

```sh
python3 -I .ufo/waves/round-18/receipt-check.py .ufo/waves/round-18/receipt-claims.json
```

Recorded calls used `subprocess.run(..., capture_output=True, text=True, timeout=20)`; SHA observations used `sha256sum` with timeout 10. There were eleven recorded observations below, plus one initial pristine invocation with the same output and exit 2. A restored observation doubles as the next mutant's pristine observation: no intervening byte changes occur. Each probe has pristine, single-point-mutated, and exact-restored observations of the same detector. No two defects were combined.

Expected healthy detector: all declared expectations met, `EXPECT_SUMMARY: 15/15`, exit 0; a recognized but unexpected status must reduce the summary and exit 1; an unevaluated claim must exit 2. Actual baseline: nine evaluated expectations met, six unevaluated recut placeholders, exit 2. This is not a baseline from which a killed/survived verdict can be certified.

## The five mutations

Line numbers refer to the pinned original checker. Edits and their inverses were applied only to the scratch checker using the edit tool.

| ID / point | Smallest mutation | Expected detector sensitivity | Actual mutated output | Verdict |
|---|---|---|---|---|
| M1 / regex, line 47 | In `HDR_SHA`, change `tool_sha256\s*[=:]\s*` to `tool_sha256\s*=\s*` | A valid colon-separated producer SHA should stop being accepted. | Exact S0 output and exit 2; no claim distinguishes this restriction. | **INCONCLUSIVE**; undetected/conditional-survivor lead. |
| M2 / SHA comparison, line 104 | `actual == tool_sha` → `actual != tool_sha` | Existing ok, bad-SHA and cross-bound stale fixtures should disagree with their expectations. | S1: all three fixture statuses invert; summary 6/15; exit remains 2. | **INCONCLUSIVE**, not KILLED: observable assertion bite, but pristine is already non-clean. |
| M3 / missing-field branch, line 98 | `if not tool_sha or not measured:` → `if not tool_sha and not measured:` | Receipts with exactly one required provenance field should be rejected as `MISSING_PROVENANCE`, not continue into lookup/comparison. | Exact S0 output and exit 2; existing no-provenance and complete-provenance cases do not distinguish this predicate. | **INCONCLUSIVE**; undetected/conditional-survivor lead. |
| M4 / expectation comparison, line 139 | `elif status == expect:` → `elif status in allowed:` | A valid claim with a deliberately wrong allowed expectation must not count as met. | Exact S0 output and exit 2; all evaluated statuses already equal their expectations. | **INCONCLUSIVE**; undetected/conditional-survivor lead. |
| M5 / exit mapping, line 144 | `return 0 if met == n else 1` → `return 0 if met == n else 0` | An evaluated expectation mismatch must exit 1, never 0. | Exact S0 output and exit 2; the pending branch returns before this line. | **INCONCLUSIVE**; undetected/conditional-survivor lead. |

### Actual stdout S0

This is the full stdout of every pristine/restored observation and of M1, M3, M4 and M5. Stderr was empty; exit 2.

```text
RECEIPT r17-tripwire-r13 MISSING_PROVENANCE
RECEIPT r17-tripwire-r14 MISSING_PROVENANCE
RECEIPT r17-tripwire-r15 MISSING_PROVENANCE
RECEIPT r17-tripwire-r16 MISSING_PROVENANCE
RECEIPT r17-tripwire-anchor-r15 MISSING_PROVENANCE
RECEIPT r17-tripwire-pacmanlog-join MISSING_PROVENANCE
RECEIPT r18-fixture-ok ok
RECEIPT r18-fixture-bad-sha SHA_MISMATCH
RECEIPT r18-fixture-stale-rev SHA_MISMATCH
RECEIPT r18-recut-tripwire-r13 PENDING
RECEIPT r18-recut-tripwire-r14 PENDING
RECEIPT r18-recut-tripwire-r15 PENDING
RECEIPT r18-recut-tripwire-r16 PENDING
RECEIPT r18-recut-tripwire-anchor-r15 PENDING
RECEIPT r18-recut-tripwire-pacmanlog-join PENDING
EXPECT_SUMMARY: 9/15
```

### Actual stdout S1

Full stdout of M2 only. Stderr was empty; exit 2.

```text
RECEIPT r17-tripwire-r13 MISSING_PROVENANCE
RECEIPT r17-tripwire-r14 MISSING_PROVENANCE
RECEIPT r17-tripwire-r15 MISSING_PROVENANCE
RECEIPT r17-tripwire-r16 MISSING_PROVENANCE
RECEIPT r17-tripwire-anchor-r15 MISSING_PROVENANCE
RECEIPT r17-tripwire-pacmanlog-join MISSING_PROVENANCE
RECEIPT r18-fixture-ok SHA_MISMATCH
RECEIPT r18-fixture-bad-sha ok
RECEIPT r18-fixture-stale-rev ok
RECEIPT r18-recut-tripwire-r13 PENDING
RECEIPT r18-recut-tripwire-r14 PENDING
RECEIPT r18-recut-tripwire-r15 PENDING
RECEIPT r18-recut-tripwire-r16 PENDING
RECEIPT r18-recut-tripwire-anchor-r15 PENDING
RECEIPT r18-recut-tripwire-pacmanlog-join PENDING
EXPECT_SUMMARY: 6/15
```

### Recorded run matrix

All timestamps are UTC on 2026-10-20. Every row ran the exact command above; stderr length was zero in every row.

| Observation | Time | Checker hash | Stdout | Exit |
|---|---|---|---|---|
| M1 pristine | 16:02:36.480022 | B | S0 | 2 |
| M1 mutated | 16:02:45.843209 | M1 | S0 | 2 |
| M1 restored / M2 pristine | 16:02:54.026412 | B | S0 | 2 |
| M2 mutated | 16:03:13.615903 | M2 | S1 | 2 |
| M2 restored / M3 pristine | 16:03:20.228850 | B | S0 | 2 |
| M3 mutated | 16:03:26.725502 | M3 | S0 | 2 |
| M3 restored / M4 pristine | 16:03:34.754839 | B | S0 | 2 |
| M4 mutated | 16:03:40.863301 | M4 | S0 | 2 |
| M4 restored / M5 pristine | 16:03:47.587564 | B | S0 | 2 |
| M5 mutated | 16:03:54.784628 | M5 | S0 | 2 |
| M5 restored | 16:04:04.959477 | B | S0 | 2 |

SHA-256 of stdout, including its final newline:

- S0: `f21e882eeedda713b6e51238cc4f21635b6f1d57d1846a5f2f9df142655fad06`.
- S1: `60b1e0fdac8ae107e2afca7019adfe3e029b4f42c34de36b6715f5818d7ad91b`.

## Before / mutated / after hashes and restoration

Every probe's checker sequence was **B → its named mutant → B**:

| Key | SHA-256 of checker bytes |
|---|---|
| B, pristine and every restoration | `5aec6154085c22cd8de34ec32d8ffdb29e783955ab52c6282d25344f559dc7b2` |
| M1 | `92c2fe20514be0705a8071b23f25d09957c737dcba46fda7f08f42e8c0f14eee` |
| M2 | `a8e964283b0c629b4f58995697c045f814453e4c08914b99fe37ac1b6a42b152` |
| M3 | `1326a1c7ee509d7d747a5117655b391e9d90b0bd86ac1b96762dc72d677bc580` |
| M4 | `490b11a1a8fd892d3e1a5e004bd9458844c40e61cf27d9bc4ee294e90c646ab4` |
| M5 | `2a4e7c33d459956b50165f85b119936311b843bb33260296960bbc999153a1da` |

The claims hash was checked with every recorded observation and never changed:
`14aaee0f051788662948510c4faf116f86f44f34a3248405f206bc5a697b0628`.

These fixture hashes were measured before mutation and after the final restoration; all were identical:

| Fixture | Before = after SHA-256 |
|---|---|
| `ok-receipt.txt` | `04b431ff5c87d5868f91eb7e69f088d457d4ba71abaadaabc5551a6f836e8177` |
| `bad-sha-receipt.txt` | `2018ca40bbaceb5b3af46460d6c340c4e6367cf6f53a5567a075b6b47e817517` |
| `stale-rev-receipt.txt` | `6ad4af1026245c4525c7e25079348e8cad1a2a5146e95622b8e2b8c5de51dd92` |

The measurement command was `sha256sum .ufo/waves/round-18/receipt-check.py .ufo/waves/round-18/receipt-claims.json .ufo/waves/round-18/receipt-fixtures/ok-receipt.txt .ufo/waves/round-18/receipt-fixtures/bad-sha-receipt.txt .ufo/waves/round-18/receipt-fixtures/stale-rev-receipt.txt` in the scratch root. Each restored run reproduced pristine exit/stdout/stderr exactly as well as restoring B. No scratch fixture or claims bytes were edited.

## Proposals for ReceiptCheckFix — not executed or integrated here

These are leads from the undetected mutants and inspected branches, **not certified survivor kills or a contract change**:

1. **Establish a green full-corpus baseline first.** Replace the six `PENDING-L1` placeholders with explicit committed receipt revisions and real committed paths. At this revision they name `*-recut.txt`, whereas the enumerated committed evidence names are `tripwire-r13.txt` through `r16.txt`, `tripwire-anchor-r15.txt`, and `tripwire-pacmanlog-join.txt`. Do not make them green by filtering or accepting PENDING.
2. **Header / M1:** cover every syntax the repaired contract retains, including a valid colon-separated SHA if retained and the real single-line `RECEIPT … tool_sha256=… measured_commit=…` shape. All three current authored fixtures put the SHA on a standalone equals-separated line; none tests colon SHA or that real single-line shape. Add a negative body-only/input-digest case so non-header data cannot impersonate a producer header. [INFERENCE] The old standalone `HDR_SHA`/`HDR_REV` regexes cannot by themselves parse the declared single-line RECEIPT shape; pending recut claims never reach parsing.
3. **Missing fields / M3:** two independent negative header claims, one with only `tool_sha256`, one with only `measured_commit`, each expecting `MISSING_PROVENANCE`. The current both-absent/complete shapes do not distinguish `or` from `and`.
4. **True STALE versus SHA_MISMATCH:** retain the existing cross-bound stale fixture (correctly expected as SHA_MISMATCH), but propose a separate self-consistent old `(measured_commit, tool_sha256)` pair against an explicitly declared newer expected producer revision. A STALE test needs an independent expected producer binding; receipt storage revision is not necessarily its producer revision. [INFERENCE] The pinned evaluator compares the claimed SHA to the tool at the claimed commit and has no independent freshness expectation, so an internally consistent old pair is not tested as stale by this corpus.
5. **Expectation / M4 and exit / M5 require negative invocations, not just more correct claims.** A separate one-claim run with a valid receipt but deliberately wrong allowed expectation must assert its actual status, `EXPECT_SUMMARY: 0/1`, and exit 1. With no pending rows, M4 would incorrectly count it and M5 would incorrectly map the mismatch to exit 0. Merely adding correctly expected STALE/header rows cannot distinguish these mutants on a green corpus. Also retain independent exit-2 assertions for unreadable/malformed inputs rather than letting placeholders mask the exit-1 path. These are proposed detector cases; they were not run in this assignment.

## Boundaries

Only this report was written in the lane. All source mutations and git writes occurred in the assigned `/tmp` clone, and the checker was restored exactly. No delegation, sibling-file writes, lane git/jj writes, live host checks, package-manager commands, installs, upgrades, network activity, or other lane test suites were used. No gate fix, integration, admission judgment, or runtime orchestration was attempted. Tool installs/updates: **none**.
