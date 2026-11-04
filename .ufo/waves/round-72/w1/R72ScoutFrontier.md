# R72ScoutFrontier — frontier-step reconnaissance (round 72)

Read-only. No lane file, registry, README, ledger or receipt was edited; the only writes are
this directory (`w1/R72ScoutFrontier/`). Scratch `/fast/scratch/hyaku/mado-r72/R72ScoutFrontier/`
was used for the fixture and deleted at the end.

- base rev: `976684a27e99c2508037a60eec415f550f53d70e` (clean: 380 registry rows, max `S443`)
- worktree HEAD during probing: `fd9ea03b554d6925594957c381f09e29a2ac159e`
- **HEAD moved to `925a3e8a355bf8b343ba3591c8290dd3ffe2c609`** ("round-72: corpus, registry,
  gate registry and lesson for the two landed rules") at ≈01:43; §§1–5 below carry both the
  in-flight observation and the post-commit re-measurement.
- capture time: 2026-11-04T01:41:01-03:00 (in-flight), 01:43 (post-commit)
- **The lane was mid-write during this reconnaissance.** `corpus/SOURCES.md` carried an
  uncommitted 18-line insert (3 rows + the Round-72 note block) and two r72 knowledge files
  appeared between probes. Every count below is stated with the moment it was taken; line
  numbers move under sibling appends, so use content anchors.

## 1. Registry census

Command:

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

| probe | rc | last line |
|---|---|---|
| first (≈01:39, worktree already had the 3 uncommitted rows) | 0 | `mado ok /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` |
| second (≈01:40, after a knowledge file was referenced but not yet created) | 1 | `mado E11 S445 missing used-by corpus/knowledge/outcome-verdict-gate-summary-r72.md` |
| final (01:41) | 0 | `mado ok /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` (40 lines total) |
| post-commit (01:43, HEAD `925a3e8a`) | 0 | `mado ok /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` |

The transient `E11` is a live-write race, not a defect: the row's `used-by` cell named
`corpus/knowledge/outcome-verdict-gate-summary-r72.md` before that file existed; the file
appeared at 01:40 and the census returned to green. Snapshot kept as
`w1/R72ScoutFrontier/census-final-snapshot.txt` (rc 0, 39 warnings + `ok`).

Row count, strict pattern `^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|`:

- at base `976684a2`: **380** — matches the declared "expect 380 before appends"
- in the worktree at 01:41: **383** (380 + `S444`/`S445`/`S446`, uncommitted)
- at `925a3e8a`: **383** committed (the same three rows)

Last five ids:

- at base: `S439 S440 S441 S442 S443`
- worktree 01:41 and HEAD `925a3e8a`: `S442 S443 S444 S445 S446`

Uncommitted diff (`git diff 976684a2 -- corpus/SOURCES.md`): 1 file, **18 insertions** —
three table rows (worktree lines 394–396) plus the `## Round 72 — bounded result-object source
sweep (2026-11-04)` note block. Nothing else in the registry moved. The same insert is now
commit `925a3e8a` (which also carries the nine fetch files and the doc/ledger updates).

## 2. Id-collision pre-check for the planned S444–S446

Extraction pattern `^ {0,3}\| *S[0-9]{3,}`:

- base `976684a2`: **380** unique ids; `grep -E '^S44[456]$'` → **no match**. All three planned
  ids were free at the scored base.
- worktree 01:41: **383** unique ids; all three are now present — but they are the round's own
  uncommitted append (lines 394–396), not prior art. `git show 976684a2:corpus/SOURCES.md`
  confirms `S443` is the maximum at base.

Operational consequence: a seat that re-runs this pre-check against the live worktree will
report a false collision. The check must compare against `976684a2`, or accept the three ids as
this round's own rows.

### Guard proof (0–3-space pattern vs narrow column-zero pattern)

Fixture: `corpus/SOURCES.md` copied into scratch, then appended
`  | S002 | FIXTURE indented row | docs | A | guard proof | x |` (stored at fixture line 863).
Receipt: `w1/R72ScoutFrontier/guard-proof.txt`, fixture copy kept at
`w1/R72ScoutFrontier/fixture-SOURCES.md`.

| pattern | count of `S002` |
|---|---|
| `^\|[[:space:]]*S002[[:space:]]*\|` (narrow) | **1** |
| `^ {0,3}\|[[:space:]]*S002[[:space:]]*\|` (guarded) | **2** |

The narrow pattern misses the indented row; the 0–3-space pattern catches it. Note the real
registry currently holds **zero** indented `S`-rows (both patterns read 383 today), so the
guard is purely defensive — it changes no current count.

## 3. Coverage-map census

| probe | coverage entries (README table rows for `knowledge/*.md`) | knowledge files on disk |
|---|---|---|
| first (≈01:39) | **85** | **85** |
| final (01:41) | **87** | **87** |

The declared starting point 85/85 holds. The two planned r72 entries landed in the window:
`knowledge/summary-credit-own-detail-r72.md` and `knowledge/outcome-verdict-gate-summary-r72.md`,
registered in the README table at lines 97–98. Coverage is 1:1 at the final probe.

## 4. Ledger census

```
python3 -I quality/check-tool-ledger.py --repo . --rev master
```

rc **1**; terminal line:

```
LEDGER: population=125 ledger_rows=122 uncovered=3 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED rev=fd9ea03b554d6925594957c381f09e29a2ac159e
```

Uncovered paths, exactly the three r72 instruments (each `reason=uncovered detail=no-row`):

1. `quality/counters/c1-r72-landing-controls.py`
2. `quality/counters/c1-r72-summary-credit.py`
3. `quality/counters/c2-r72-outcome.py`

`quality/tool-ledger.md` contained no `c1-r72`/`c2-r72` row at the 01:41 snapshot (`grep` →
none), so the no-harm obligation was open then. **It closed at commit `925a3e8a`**: the commit
adds 3 lines to `quality/tool-ledger.md`, and a re-run at the new HEAD prints

```
LEDGER: population=125 ledger_rows=125 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=925a3e8a355bf8b343ba3591c8290dd3ffe2c609
```

rc **0**. `dangling=0`, `bad_pointer=0`, `empty_desc=0` throughout — no other drift.

## 5. Frontier bullet

`## Frontier` header at line 129; entries are newest-first. A round-72 entry extends the
**Round-71 kill-credit bullet** ("Round 71 moves the kill-credit rule past the exit status and
counts four more carrier shapes … rows S442/S443 … plus held S435/S438/S441"). At this snapshot
the round-72 bullet already sits first under the header (direct read at line 131; a concurrent
`grep -n` in the same batch reported 133 — the section is being edited live, so the number is
unstable and the anchor is the text).

The extension is exact against the r71 bullet's own `Still open:` clause:

- *"stale/canned/echoed summaries are indistinguishable from genuine ones (the rule reads the
  report, it does not authenticate it)"* → C1 narrows it: the last parsed `p/n` shortfall must
  be backed by the run's own `SELFTEST FAIL` lines numbering exactly `n − p`, which kills
  `bare-failing` and `mismatch-detail`. The residual (a replayed summary **with matching detail
  lines**) is declared still open by the round-72 claim itself.
- *"the unmutated selftest leg still keys on exit status"* → C2 closes it: the verdict reads the
  subject's last parsed summary, and the exit status is recorded but does not gate.

The other r71 open items (`global` rebinds, method-call mutations, deeper alias chains,
edge-resolved stores) are untouched by round 72 and remain open.

## Frozen receipts re-read (not rewritten)

Both measurement files are tracked at HEAD and end with the declared lines:

- `measurement-c1-r72.txt`: `MADO_R72_SUMMARY_CREDIT: cases=8 correct=8 base_correct=6 verdict=TARGET_MET rev=9bcb4fd5b598844f168230dc05e441721d95b272`, `C1_RC=0`
- `measurement-c2-r72.txt`: `MADO_R72_OUTCOME: cases=8 correct=8 base_correct=4 verdict=TARGET_MET rev=9bcb4fd5b598844f168230dc05e441721d95b272`, `C2_RC=0`

Tracked at HEAD under `.ufo/waves/round-72/`: claims declaration, both control baselines, both
control JSONs, both measurements, `make-spec-r72.py`, the three `proto/` scripts, the two spec
files. `.ufo/waves/round-72/fetch/` was **untracked** during probing and was **committed** in
`925a3e8a` (all nine files, 3 URLs × 3 fetches), byte-identical per URL (`sha256sum`):

```
5a6951b7…3116e8e1  Doc_builtins_stdtypes.rst.{1,2,3}
d6522f68…f7ae5b86  Doc_library_unittest.rst.{1,2,3}
12de7da0…c0a261d2  Lib_unittest_main.py.{1,2,3}
```

That corroborates the "fetched three times and byte-identical" claim at the byte level.

## Remaining unknowns

- Whether the fetched files' *content* carries the declared sections (`§ TestResult`,
  `wasSuccessful`, the runner's exit derivation) — checksums only, no content join.
- The census's `E11` window shows the registry's `used-by` edge is a hard ordering constraint:
  a row may not name a knowledge file that does not yet exist. Any later append seat must
  create the knowledge file first or point `used-by` at an existing one.
- Round-72 doc obligations landed in the same commit (`PROVINCE.md` +13, `SKILL.md` +4,
  `corpus/QUALITY.md` +31, `corpus/lessons/round-72.md` +105, `corpus/README.md` +4), but I did
  not re-read those files for consistency — out of this seat's scope.
- Both earlier open obligations (ledger rows, fetch commit) closed at `925a3e8a`; nothing else
  was observed open at the final probe.

## Tooling

No tool was installed, upgraded or removed. No `pacman`/`jj`/`git` write command ran. Read-only
git (`status`, `rev-parse`, `show`, `diff`, `ls-files`) only.
