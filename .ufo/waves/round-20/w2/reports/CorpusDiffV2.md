# CorpusDiffV2 — holds: zero findings lost versus 9c54c56 on digest-stable coverage

## Findings

Implemented `corpus-diff-v2.py` under the assigned wave output directory. It scans the corpus once per tool revision, normalizes scan paths relative to the root, and only compares files whose pre-scan, post-scan, base-scan, and tip-scan SHA-256 values all agree. It records every excluded path and reason, rather than only drift counts (`corpus-diff-v2.py:75-172, 383-422, 448-462`). The separate `--round20-dir` result includes its own denominator, excluded-file list, and comparison (`:368-377, 424-443, 483-485`).

Findings are joined by `(file, line, tool_call_id)`. Exact rows are consumed first; remaining findings within a retained call are paired and bucketed by changed class/rule/evidence/command text. Evidence-only changes therefore enter `relabeled`, not additions or losses. Completely absent call IDs feed `lost_rows`; unpaired base rows within a still-present call ID are separately disclosed (`:215-349`).

### Registered no-harm comparison: 9c54c56 → 28c6837

Executed from the isolated clone, against the session root as data only:

```text
python3 -I /tmp/mado-r20w2-CorpusDiffV2/.ufo/waves/round-20/w2/CorpusDiffV2/corpus-diff-v2.py --base 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d --new 28c6837 --corpus /home/vgpnk/.omp/agent/sessions/-Projects-shokunin --round20-dir /home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20 --out /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w2/CorpusDiffV2/9c54c56-vs-28c6837.json
{"added_findings": 6280, "excluded_files": 158, "files_at_start": 6078, "lost_calls": 0, "lost_findings": 0, "out": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w2/CorpusDiffV2/9c54c56-vs-28c6837.json", "relabelled_findings": 0, "stable_files": 5921}
```

Result: **0 lost call IDs / 0 lost findings** on 5,921 stable files (5,921 / 6,078 = **97.417%**). The resulting findings count is 1,753 at base and 8,033 at tip; all 6,280 net additions are listed in the JSON's `comparison.added_rows` ledger. There are **98 distinct class/rule/evidence groups**. Aggregate additions:

| Class | Evidence | Added findings |
|---|---|---:|
| `live_probe` | `observed` | 20 |
| `package_query` | `lead` | 3 |
| `package_query` | `observed` | 4 |
| `tool_install` | `observed` | 121 |
| `vcs_write` | `lead` | 21 |
| `vcs_write` | `observed` | 6,111 |

The complete class/rule/evidence counts and up to eight file/line examples per group are in `CorpusDiffV2/9c54c56-vs-28c6837.json:1`, `$.comparison.added_rows`; the aggregate table above is not a substitute for that ledger. Large individual groups include `vcs_write/git:commit/observed` 1,428, `git:add/observed` 1,254, `git:checkout/observed` 1,011, `git:push/observed` 292, `jj:git/observed` 316, `tool_install/npx/observed` 114, and `live_probe/journalctl/observed` 16. No retained rows were relabeled in this comparison.

### Repair-isolation comparison: 1f7f995 → 28c6837

Executed from the same isolated clone over the same read-only session root:

```text
python3 -I /tmp/mado-r20w2-CorpusDiffV2/.ufo/waves/round-20/w2/CorpusDiffV2/corpus-diff-v2.py --base 1f7f995 --new 28c6837 --corpus /home/vgpnk/.omp/agent/sessions/-Projects-shokunin --round20-dir /home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20 --out /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w2/CorpusDiffV2/1f7f995-vs-28c6837.json
{"added_findings": 354, "excluded_files": 98, "files_at_start": 6079, "lost_calls": 90, "lost_findings": 127, "out": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w2/CorpusDiffV2/1f7f995-vs-28c6837.json", "relabelled_findings": 18, "stable_files": 5981}
```

On 5,981 stable files (5,981 / 6,079 = **98.388%**), the harmed-tool comparison has **90 lost call IDs / 127 associated findings**, grouped under 23 class/rule/evidence rows: `package_query` observed 1 and `vcs_write` observed 126. The 354 additions comprise `live_probe` observed 10, `package_query` lead 1 and observed 1, and `vcs_write` lead 21 and observed 321 (36 groups in the JSON). Eighteen retained-call relabels were recorded: 16 command-text changes and 2 `observed` → `lead` evidence changes. No class- or rule-rename bucket occurred in these corpus runs. Another 18 base findings were unmatched within call IDs that remain present; the JSON reports these separately from lost call IDs. These 1f-to-tip removals are reported, not independently adjudicated here.

### Drift coverage and the round-20 session

The guard run started with 6,078 files and ended with 6,079; the two scans each enumerated 6,078. The diff excluded 158 paths: 157 changed during the run and one added during it. Hash mismatches were separately counted (105 base and 149 tip; these overlap the changed-file count). The full excluded-path list, with per-path reasons, is `$.coverage.excluded_files` in the guard JSON. The repair-isolation run started/ended with 6,079 files, excluded 98 changed files, and recorded 63 base / 94 tip scan-digest mismatches; its complete path list is in the isolation JSON. Example excluded round-20 paths from the guard inventory include `MadoR20/MadoR20.AdvCrash.jsonl`, `MadoR20/MadoR20.AdvLeadMarks.jsonl`, and `MadoR20/MadoR20.AdvRecallShapes.jsonl` (`9c54c56-vs-28c6837.json:1`, `$.round20_session.coverage.excluded_files`).

The explicitly separated session was `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20`—163 files at start and after the guard run, 124 stable, 39 excluded (**76.074%**). Within its stable subset, 5 base findings became 168 tip findings: 0 lost, 163 added, 40 class/rule/evidence groups. The 163 additions break down as `package_query/lead` 2, `tool_install/observed` 2, and `vcs_write/observed` 159. The complete separate round-20 addition ledger and 39 excluded paths are in the guard JSON under `$.round20_session`.

In the 1f7f995 isolation run, that same session subset had 136 stable / 163 files (**83.436%**); its 27 excluded paths are listed separately in the isolation JSON. It contained 27 lost call IDs / 41 associated findings, 4 added findings, 9 relabels (7 command-text, 2 evidence-only), and 11 unmatched base findings within retained call IDs. Because this session contains the round-20 seat fixture activity, these counts are kept distinct from the older corpus; they are not independent validation of fixture behavior.

The tripwire source states it parses bash/eval tool calls and does not execute transcript text (`tools/mado-tripwire.py:4-8, 92`). Neither transcript commands nor raw tool-call IDs are copied into the JSON artifacts; examples contain only file paths and line numbers. Both JSON files are below the 2 MiB limit.

## Limits

- This is a digest-stable subset comparison, not a frozen snapshot. The scan-time hashes make excluded live files explicit; see each JSON's complete `coverage.excluded_files` and `round20_session.coverage.excluded_files` arrays. The 9c54c56 guard result covers 97.417% of the starting file count, and the round-20 subdirectory only 76.074%.
- Added-row ledgers are detector output, not truth adjudication. Round-20 seat transcripts are self-referential fixture material by assignment; their findings are separated, not treated as an independent corpus.
- The 1f7f995 → 28c6837 lost rows are shown as exact observed differences; I did not inspect transcript command text or decide which removals are intended. Rule/class rename implementation was exercised on the corpus but no class/rule rename example occurred.
- No separate selftest, build, lint, or formatter was run. The two requested full-corpus diff commands are the exercised checks.

## Installs

none.

## Artifact hashes

- `corpus-diff-v2.py` — SHA-256 `f464e72f9615e75497528b671bbd420615e9e786fa4f3fc5d448e7eb830d050c`
- `9c54c56-vs-28c6837.json` — SHA-256 `bd048df90b1f7f15016ab7aea1782ea4feea655ecca0c8f3e6bdcf5896356f77` (104,312 bytes)
- `1f7f995-vs-28c6837.json` — SHA-256 `948e9eaaeb9d733febb8a019e778d2d7122db233c0ff359dcadfba4473ac9c38` (73,981 bytes)
