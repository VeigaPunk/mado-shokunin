# C2 assessment probe: shonen_x_without_nonauthor

## Verdict

**Frozen case correct; nearby artifact mutant SURVIVED.** Retain finding **R21-C2-SHONEN-NONAUTHOR-NA-PREFIX**: an explicitly author-only box-1 `[x]` with `non-author verifier: N/A` is accepted as `assessment_clean`. This is a false negative relative to the frozen case's absent-verifier rationale, not evidence of authentic independent assessment or promotion eligibility. No production repair was attempted.

Axes: **coverage** (one neighboring malformed/absence assertion), **calibration** (artifact acceptance versus authenticated authority), and **operability/isolation** (consistent exit/result/finding, bounded C2-only execution, exact restoration).

## Scope and tested bytes

- Seat: `MadoR21-2.GateShonenXWithoutNonauthor-2`; advisory only, no delegation or integration.
- Tested source: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py`.
- Tested source SHA-256, identical for all three invocations and after restoration: `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7`.
- Parent identified the current candidate as `f499a8db7171b7476fe9f204ab9edbac5a956fa9`, superseding the initial `2ac0f9ba69051aea22cab3b6cfebe4d906b72d17` task context. This report binds its observations to the actual source SHA above; it did not inspect or modify VCS state.
- Frozen input: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/cases/shonen_x_without_nonauthor.json`.
- Private inert input: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/GateShonenXWithoutNonauthor-2/shonen-probe.json`.
- C2 root: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures`.

The frozen expected record says `code: 1`, `result: failed`: the complete row marks box 1 `x` while its evidence is author-only and names no non-author verifier. Source lines 145–146 and the frozen-case mapping at line 181 identify `unnamed_nonauthor_verifier` as its stable finding.

## One artifact mutation and expected detector

Only the box-1 evidence tail changed; JSON structure, box number, `x` mark, other evidence rows, chronology strings, population, oracle and history remained equal. The detector expected the tuple `(exit 1, code 1, result failed, finding_ids [unnamed_nonauthor_verifier])` for the pristine, mutated and restored artifacts: neither evidence text asserts a named non-author assessment.

Original box-1 evidence:

```text
SKILL.md contains real decision tables, error patterns, checklists, cited sources; author-only assessment, with no non-author verifier named.
```

Single altered box-1 evidence:

```text
SKILL.md contains real decision tables, error patterns, checklists, cited sources; author-only assessment, with no non-author verifier: N/A.
```

The mutation is confined to replacing `non-author verifier named.` with `non-author verifier: N/A.` in that one string. A structural equality assertion confirmed that undoing this evidence-string replacement makes the two decoded objects equal. Production and frozen bytes were never edited.

Source explanation: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py:145-146` uses the search pattern `\bnon-author verifier:\s*[A-Za-z0-9][A-Za-z0-9_.-]*`. It can match the `N` prefix of `N/A` without requiring a complete verifier value; it also does not distinguish the preceding `no` from a positive assertion. Thus the malformed absence value satisfies its lexical check. This finding does not presume that a token matching the pattern would be a real or independent person.

## Bounded detector execution

Exactly three invocations of the same C2 `--check` path ran: pristine, one mutant, restored. Each used Python **3.14.8**, isolated/no-bytecode flags `-I -B`, one child, a **15-second timeout**, and `RLIMIT_AS = 402653184` bytes (384 MiB). No full selftest, corpus, C1 source, C1 classifier or C1 result was executed.

The child used `runpy.run_path` on the authorized C2 source with this exact gate argv:

```json
["/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py", "--root", "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures", "--check", "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/GateShonenXWithoutNonauthor-2/shonen-probe.json"]
```

An unchanged standard-library audit wrapper recorded lane file opens and rejected any lane input outside the four-file allowlist below, and rejected nested process events. Wrapper SHA-256: `beab83c43067257d6807b0c93c1df7f26895a42ad73bec53b12a9c5e6899b52b`.

### Actual outcome tuples

| State | Process exit | JSON code | JSON result | JSON finding_ids | Expected missing-verifier finding detected? |
|---|---:|---:|---|---|---|
| Pristine | 1 | 1 | `failed` | `["unnamed_nonauthor_verifier"]` | Yes |
| Mutated | 0 | 0 | `clean` | `["assessment_clean"]` | **No** |
| Restored | 1 | 1 | `failed` | `["unnamed_nonauthor_verifier"]` | Yes |

Exit, JSON code, result and finding-ID meaning agree in each state. The pristine exit 1 is the expected fixture rejection, not a failed baseline test. The input mutant **survived the gate** because it was admitted clean; the scoped detector exposed that admission as the retained false-negative finding. No timeout, resource error or invalid output occurred.

Pristine and restored stdout were identical:

```json
{"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-baseline.txt", "sha256": "16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 1, "finding_ids": ["unnamed_nonauthor_verifier"], "result": "failed"}
```

Mutated stdout:

```json
{"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-baseline.txt", "sha256": "16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 0, "finding_ids": ["assessment_clean"], "result": "clean"}
```

## Explicit C1 dependency check

Static inspection covered the complete C2 source. Its imports are standard-library imports only. `--check` calls `evaluate`/`check`; that path reads the assessment artifact, the population bytes it names, and C2 `expected.json` bytes for their hash. The subprocess loop is in the uninvoked `--selftest` branch. The historical `c2_independent: false` value is checked as artifact content, not obtained from a C1 result.

In all three actual child runs the audit output reported exactly these unique lane file opens:

1. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py`
2. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/GateShonenXWithoutNonauthor-2/shonen-probe.json`
3. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/snapshots/population-baseline.txt`
4. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/expected.json`

Every audit output had `"process_events": []`. No C1 classifier or C1 result path was opened. This dynamically confirms the inspected C2 path's lack of a C1 dependency for these three observations; it is not a claim of arbitrary-future-code isolation or a general sandbox proof.

## Actual-byte hashes and restoration

| Input | Before SHA-256 | After SHA-256 |
|---|---|---|
| C2 source, absolute path above | `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7` | `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7` |
| Frozen case, absolute path above | `bf0dd2d165e4bfccebcbb8ae1b37da75e76eecda6394efe763639f083c97f2cf` | `bf0dd2d165e4bfccebcbb8ae1b37da75e76eecda6394efe763639f083c97f2cf` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/snapshots/population-baseline.txt` | `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed` | `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/expected.json` | `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e` | `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e` |

Private fixture SHA-256 progression:

- Pristine: `bf0dd2d165e4bfccebcbb8ae1b37da75e76eecda6394efe763639f083c97f2cf`
- Mutated: `ca8ad4334416ee29317eff4a3aaab53e089af306aeaceba33228f67adb86799f`
- Restored: `bf0dd2d165e4bfccebcbb8ae1b37da75e76eecda6394efe763639f083c97f2cf`

The restored private artifact was compared byte-for-byte against both the original captured frozen bytes and the still-current frozen file: equality was `true`. Before/after hashes of all four shared inputs were equal. Population and expectation hashes came from actual file bytes, independently of the artifact's asserted `actual_sha256` field. Only this advisory report and the uniquely scoped inert fixture were written; the retained fixture is restored, not the bypass variant.

## Limits and authority

Only the assigned gate case and one neighboring altered artifact were exercised. No full suite, full selftest, corpus or historical unsafe-resource failure was rerun; no live compositor/service/package/host operation occurred. Timestamp strings and verifier-name strings remain assertions, not authenticated chronology, identity or independence. The literal input path strings shown inside stdout are artifact data. The gate's existing authority disclaimer remained present in every result. This seat supplies neither independent promotion authority nor round admission. No tools installed or updated.
