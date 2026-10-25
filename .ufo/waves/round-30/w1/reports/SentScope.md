# SentScope — round-30 w1 security / write-scope sentinel

Report only. This seat wrote only this file. Audit window: `d72243e1` (start)
through `a0dd664` (04:14 snapshot); later commits exist (see §0). Methods:
source read, read-only gate/counter runs at base/data/tip/HEAD, `strace` of
write syscalls, adversarial argv/root tests under `/tmp`, git/jj state
inspection.

Verdict: **no shell injection and no credential leak**. Open security items:
the C2 counter still creates a file from a crafted REV (F1), the gate follows a
symlinked `--root` ancestor (F2), has no `--end-of-options` guard (F5), and
`--rev` still counts symlink notes (F7, partial). Write scope: no wave-seat
artifact outside the granted report dir was found; the r28 q36 receipt was
transiently rewritten out of scope and reverted (F10), and the L1's own addenda
rewrote the frozen gate/counter and one data byte while the wave ran (F12).

## 0. Baseline movement during this audit (read first)

The lane was **actively rewritten while wave 1 ran**, by commits authored as the
lane identity `mado-shokunin <mado@shokunin.local>` (the L1 identity used by the
freeze/data/records commits, not a seat name). Snapshot: **2026-10-24 04:14
-0300**, working tree dirty again.

| commit | author / time (author date) | instrument movement |
|---|---|---|
| `451e8b3` | mado-shokunin 03:5x | freeze: registration, counter, gate blob `df01b20f…`, selftest 6/6 |
| `446dc39` / `92d3c86` | mado-shokunin | data (README/QUALITY/SOURCES/lesson) and records |
| `d72243e` | protocol-shokunin 04:03:37 | integrator closure: verifier spot-check lesson |
| `15ddd7d` | mado-shokunin 04:08:40 (jj 04:09:51) | **part 1 addendum:** rewrote `quality/check-index.py` (8/8), appended SCORECARD/lesson errata, committed 27 seat reports, added `evidence/c3-repair-d72243e.txt`, reverted the q36 receipt |
| `a0dd664` | mado-shokunin 04:11:15 | **part 2 addendum:** gate v2 `sha256 51b513f5…` (9/9), repaired `.ufo/waves/round-30/c2/count.py`, edited `corpus/QUALITY.md` row 48 (one line), refreshed the repair receipt, added 3 reports + 2 receipts |

Consequences: the *frozen* registration (`451e8b3`) still specifies gate blob
`df01b20f…` and `--selftest` 6/6; the current gate is `51b513f5…` and prints
9/9. Wave-1 receipts therefore span **two gate implementations and two counter
implementations**. My §1 text records evidence against the as-frozen
instruments and the in-progress worktree; the matrix below is the status at
`a0dd664` (re-tested read-only). Any receipt that does not name its gate/counter
sha is not reproducible from the round record alone.

Status at `a0dd664` (re-tested unless marked):

| finding | status at `a0dd664` | evidence |
|---|---|---|
| F1 counter `--output=` write | **OPEN** | crafted REV still creates `<X>:corpus/QUALITY.md` (75,464 B written, 04:13) |
| F2 `--root` symlinked `corpus` ancestor | **OPEN** | `/tmp/sentinel-anc/root` -> foreign tree: `indexed=1/1` exit 0 |
| F3 `--root` missing knowledge dir | **FIXED** | `SETUP_ERROR: ... not a directory`, exit 2 |
| F4 default `master` traceback | **FIXED** | bare invocation: `SETUP_ERROR: --rev or --root is required`, exit 2 |
| F5 no `--end-of-options`/leading-`-` guard | **OPEN** (blocked by ls-tree order) | `--rev='--output=…'` exit 2 today; no guard in code |
| F6 cwd trust | **PARTIAL** | silent default rev removed; `--repo .` and the counter's cwd still trusted |
| F7 `--rev` accepts symlink notes | **PARTIAL** | NUL/`quotepath=off` fixed spaces/non-ASCII; a git-symlink note still counts (`indexed=1/1` exit 0) |
| F8 gate vs fence regex | **FIXED** | `ROW_RE` is now the fence-literal `^\| ` |
| F9 S185 "verbatim" quote | **UNCHANGED** | schematic f-string quote still in the lesson; routed by hyaku |
| F10 q36 receipt rewrite | **CLOSED** | reverted to HEAD bytes (`git diff` empty at 04:10); erratum records it |
| F11 out-of-lane scratch | **OPEN** | `SCRATCH_ROOT` still hard-coded to `/fast/scratch/hyaku/mado-r28/ExecQ36Runner` |
| F12 baseline moved mid-wave | **SEE §1 F12** | two addendum commits + dirty worktree at snapshot |

Verdicts re-measured at `a0dd664`: gate base `8f51071b` `41/43` exit 1,
`446dc396`/`d72243e`/`15ddd7d`/`a0dd664` `43/43` exit 0; counter
`8f51071b` literal 28/40, active 31/39, MISSED; `446dc396`, `d72243e`,
`15ddd7d`, `a0dd664` literal 40/52, active 40/40, MET. The repaired
instruments reproduce the registered verdicts; the churn is a provenance
problem, not (so far) a verdict change.

Post-snapshot (not re-audited): `274f735` "part 3" (expansion verdict /
capability row) landed after the 04:14 snapshot; `RevTrendExpansion.md` was
modified again and `SimplifierC2.md` is untracked. Re-pin any final receipt to
the actual final tip and to the gate/counter hashes above.

## 1. Findings (severity / exploit path / evidence / impact / smallest fix)

### F1 — LOW (contract): C2 counter can create a file via git `--output=` smuggled through REV
- Path: `.ufo/waves/round-30/c2/count.py:82-84` takes `sys.argv[1]` verbatim and
  runs `git("show", f"{rev}:corpus/QUALITY.md")`; `git()` (lines 50-51) uses an
  argv array (no shell), but the token starts with `-` when REV does, so git
  parses it as an option. `--output=<value>` swallows the `:corpus/QUALITY.md`
  suffix as part of `<value>`.
- Reproduced:
  ```
  mkdir -p '/tmp/sentinel-inj:corpus'
  python3 -I .ufo/waves/round-30/c2/count.py '--output=/tmp/sentinel-inj'
  # exit 1; created '/tmp/sentinel-inj:corpus/QUALITY.md' (9417 B, git show
  # of HEAD), stale metric literal=0/0 -> TARGET_MISSED
  ```
  The docstring's "writes nothing" is therefore false for crafted argv.
- Impact: a seat that copies a REV string from a registration/receipt artifact
  (content is data, not contract) can make a measurement script create/overwrite
  `<X>:corpus/QUALITY.md` in any pre-existing writable directory `<X>:corpus`.
  The filename suffix is fixed and the parent must exist, so this is not a
  general arbitrary-write primitive; it also cannot produce a false
  TARGET_MET (the metric reads empty stdout -> 0/0).
- Smallest fix: reject revs starting with `-` (exit 2), or prefix the lookup
  with `--end-of-options` — verified working here:
  `git show --end-of-options REV:path` exit 0, `git cat-file -e --end-of-options
  REV:path` exit 0. Apply to all four call sites (lines 84, 113, 120).

### F2 — LOW (provenance): `--root` follows a symlinked `corpus/` ancestor and certifies a foreign tree
- Path: `quality/check-index.py:54-73` refuses a symlinked `corpus/knowledge`
  leaf and `corpus/README.md`, but not a symlinked `corpus` directory itself
  (`os.path.islink(root/corpus/knowledge)` is false when only its parent is a
  link).
- Reproduced: `/tmp/sentinel-anc/root/corpus -> /tmp/sentinel-anc/foreign/corpus`
  with a complete foreign tree -> `MADO_INDEX: root=... indexed=1/1 ... exit 0`.
  The leaf case is refused correctly (`REFUSED ... exit 1`), so the docstring's
  "symlinked ... members are REFUSED" reads stronger than the code.
- Impact: a `--root` receipt can print `root=<lane path>` while measuring another
  tree — fabricated-readiness shape if any receipt ever uses `--root`. C3's own
  receipts use `--rev`, so the registered claim is unaffected.
- Smallest fix: resolve `realpath(root)` and require both resolved targets to be
  contained in it (`os.path.commonpath`), or lstat each path component.

### F3 — LOW (vacuity): `--root` on a tree with no `corpus/knowledge` reports green 0/0
- Path: `quality/check-index.py:62-69` treats a missing `knowledge` directory as
  an empty note set; `evaluate`/`report` (76-102) then prints `indexed=0/0` and
  exits 0.
- Reproduced: `/tmp/sentinel-empty` with only `corpus/README.md` ->
  `indexed=0/0 ... coverage=0.0000/10`, exit 0.
- Impact: a mistyped/wrong root that still contains a `corpus/README.md`
  certifies an empty index instead of failing as a setup error (docstring maps
  bad input to exit 2). The selftest's case 6 deliberately blesses an *existing*
  empty directory; absence should be distinguishable.
- Smallest fix: `if not os.path.isdir(kdir): SETUP_ERROR, exit 2` (keep the
  existing empty-dir case clean).

### F4 — LOW (error-path): gate's default `master` lookup raises instead of SETUP_ERROR
- Path: `quality/check-index.py:213` `_git(args.repo, "rev-parse", "master")` is
  outside the `try` at 39-46.
- Reproduced on a main-only temp repo: traceback and **exit 1**, i.e. the *gap*
  exit code, not the documented setup code 2. Only the absent `MADO_INDEX:` line
  distinguishes it from a measured red.
- Smallest fix: wrap the rev-parse in the same `CalledProcessError` handler ->
  `SETUP_ERROR`, exit 2.

### F5 — LOW (defense-in-depth): no `--end-of-options` guard in the gate's `--rev`
- Path: `quality/check-index.py:40-41` interpolates REV into both tokens.
- Reproduced: `--rev='--output=/tmp/sentinel-inj2'` -> `SETUP_ERROR: error:
  unknown option 'output=...'`, exit 2. The write is prevented today only because
  `git ls-tree` runs first and has no `--output` option; the `git show` at line
  41 accepts it (verified directly: `git show '--output=/tmp/x:corpus/README.md'`
  enters git's write path). Safety is incidental to the current ls-tree option
  set, not enforced.
- Smallest fix: same leading-`-` rejection / `--end-of-options` as F1.

### F6 — LOW (cwd trust): both tools depend on the caller's cwd
- Gate default `--repo "."` (line 199) and `rev-parse master` fallback; counter
  has no `-C`/repo pin (`count.py:50-51,84`). Both are documented as "run from
  the lane root".
- Verified fail-closed: from the fleet root, gate -> `SETUP_ERROR ... exit 2`;
  counter -> `SETUP_ERROR ... exit 2`. No silent wrong-repo green was observed.
  Residual: a run from a different repo that happens to carry the named rev
  would measure that repo.
- Smallest fix: gate — require `--repo` or `--rev`; counter — accept/require a
  repo and call `git -C <repo>`, or resolve `rev-parse --show-toplevel` and
  assert it equals the lane root.

### F7 — LOW (asymmetry): `--rev` mode accepts symlinked/non-regular notes
- `git ls-tree --name-only` (line 40) lists symlink blobs (mode 120000) as note
  names; the gate then counts a README row for them as indexed, while `--root`
  refuses them. Reproduced: temp repo with `corpus/knowledge/a.md` as a symlink
  -> `indexed=1/1`, exit 0.
- No live exposure: all 43 committed notes are mode `100644`
  (`git ls-tree -r HEAD corpus/knowledge | awk '{print $1}' | sort | uniq -c` ->
  `43 100644`).
- Smallest fix: use `git ls-tree -l` and admit only `100644`/`100755` blobs
  (or state the `--rev` exception in the docstring).

### F8 — LOW (semantics drift): gate row regex is a superset of the frozen fence
- Gate `ROW_RE` is `^\|\s*` (`quality/check-index.py:29`); the frozen fence in
  `SCORECARD.md` §Counting command is `^\| ` (exactly one space).
- Reproduced: row `|  \`knowledge/a.md\` | x | y |` -> gate `indexed=1/1`,
  exit 0; the fence regex over the same file returns `[]`. C3's claim is that
  the gate "implements the fence's row-set semantics"; today the two agree on
  the measured revisions (41/43 and 43/43), but a future two-space row would be
  green in the gate and red in the scoring fence.
- Smallest fix: use the fence's exact prefix in `ROW_RE` (or document the
  deliberate superset in the C3 capability row).

### F9 — LOW (provenance accuracy): S185's "verbatim" quote is schematic
- `corpus/lessons/round-30.md` §Gate quotes
  `revision=$rev indexed=$covered/$total ...`, which does not appear in the
  block (the block is an f-string with `{rev}`/`{covered}`). The pinned block
  digest does verify: recomputed sha256 of the SCORECARD block =
  `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`, exactly
  the S185 row value.
- Impact: provenance text overstates precision; the row itself is anchored by
  the correct digest. Already routed by the integrator's closure note
  (`corpus/lessons/round-30-verifier-spotcheck.md`, "S185 lesson quote is
  schematic").
- Smallest fix: replace the quote with the literal `MADO_INDEX:` output line or
  the literal f-string and keep the digest.

### F10 — MEDIUM (live write-scope violation): committed r28 evidence rewritten in place during wave 1
- `quality/q36-successor-receipts.txt` is tracked (committed in `77cdda8`, present at
  tip `d72243e1`). It was rewritten at **04:06:46.868** while wave 1 ran, after
  the wave's reports were authored. `git status` now shows
  `M quality/q36-successor-receipts.txt` — outside the round-30 tree and outside
  the four named corpus files, and outside every wave-1 item path.
- Cause: `quality/q36-successor-run.sh:7,21` assigns `RECEIPTS=$ROOT/quality/q36-successor-receipts.txt`
  then truncates it (`: > "$RECEIPTS"`) and appends rows. The worktree diff is
  4 lines, all ephemeral run directories (`/tmp/mado-r28-q36-ge5zx30t` ->
  `g3nfq53x`; `/fast/scratch/hyaku/...`); every `rc`/`expected`/`PASS`/`FAIL`
  column is unchanged, so no verdict moved. Blob evidence:
  `HEAD:quality/q36-successor-receipts.txt` = `8f8e74a917ad719a4c84d3ac38782b37927f0650`,
  worktree `git hash-object` = `d032704d8c26c568436cef53fd5042441d2a8cde`.
- The same run created `/fast/scratch/hyaku/mado-r28/ExecQ36Runner` at 04:06
  (empty; its `run.XXXXXXXX` workdir was removed by the script's `trap`) —
  scratch outside the lane. Independently observed by `RevC1Fence`
  (r30 w1 report) at the same mtime; not restored by either seat.
- Attribution: no wave-1 report names `q36` or this file (grep over the 13
  reports); actor unresolved. `ExecSelftest`'s `git status --porcelain` receipt
  predates the mutation (its report is 04:04), so the wave's clean-worktree
  evidence understates current state.
- Impact: provenance (the committed receipt no longer matches the committed run
  bytes) and scope discipline; the lane's closure/conformance text assumes a
  clean worktree. Content impact is cosmetic (temp paths only).
- Smallest fix: run the successor witness in a `/tmp` clone or redirect its
  output under `.ufo/waves/round-30/evidence/`; restore the tracked bytes
  (`git checkout -- quality/q36-successor-receipts.txt`) or commit the change
  deliberately with its rationale. Not restored here (report-only seat).
- **Status at `a0dd664`:** reverted to committed bytes in `15ddd7d` (erratum
  part 1 records the same handling as round 29; `git diff` empty at 04:10).
  The runner still writes the tracked path, so the latent write remains.

### F11 — LOW (out-of-lane scratch): processes created dirs under `/fast/scratch/hyaku/mado-r28/`
- `/fast/scratch/hyaku/mado-r28/ExecQ36Runner/` was created at 04:06 by
  `quality/q36-successor-run.sh:8,14-15` (hard-coded `SCRATCH_ROOT`); its
  ephemeral `run.XXXXXXXX` workdir was removed by the script's `trap`.
  `/fast/scratch/hyaku/mado-r28/ExecCountV5/` appeared at 04:05 containing
  `probe_boolword.py`; no lane script references that path.
- Impact: writes outside the lane and outside the registered write set; no
  lane, sibling-repo, compositor or config bytes were touched, and the scratch
  root predates the round (Oct 23 20:38; r28 convention). Declared for
  completeness, not a lane mutation.
- Smallest fix: point `SCRATCH_ROOT` at `mktemp -d` under `/tmp`, or declare
  `/fast/scratch/hyaku/mado-r28` as an allowed scratch path in the wave context.

### F12 — MEDIUM (integrity/process): the frozen instruments and one data byte were rewritten by two L1 addenda while wave 1 ran
- The wave context and registration declare `quality/check-index.py` and
  `.ufo/waves/round-30/c2/count.py` frozen/L1-owned. Both were edited after the
  freeze and after the data/records commits: `15ddd7d` rewrote the gate
  (8/8) and `a0dd664` rewrote it again (`sha256 51b513f5…`, 9/9) and repaired
  the counter (supersession position guard, `expand_ids` grammar, `active=0`
  guard). `a0dd664` also edited `corpus/QUALITY.md` row 48 (one line) — a named
  data-rule byte — and both addenda appended SCORECARD/lesson errata. See §0.
- Attribution: git author `mado-shokunin <mado@shokunin.local>`, the same lane
  identity as the freeze/data/records commits; jj committed at 04:09:51. This
  reads as the L1's own integration rather than a wave-seat write. If the
  orchestrator did not authorize it, it is a direct violation of the wave's
  "never edit" freeze; either way the wave's baseline moved twice under the
  running seats.
- Live state at the 04:14 snapshot: the worktree is dirty again
  (`M w1/reports/RevC1Fence.md`, `M w1/reports/RevRecordsChain.md`,
  `M SCORECARD.md`, `?? w1/reports/RevTrendExpansion.md`); 31 reports exist,
  27 committed in part 1, 3 in part 2, 1 untracked. Part 1's lesson text says
  "24 seat reports"; that count was already stale when committed.
- Impact: any receipt/claim that does not pin its gate/counter sha is not
  reproducible from the round record; a seat re-running the gate before/after
  04:09 measured different artifacts. The registered verdicts themselves were
  unchanged in my re-runs (gate 41/43 -> 43/43; counter 28/40,31/39 -> 40/52,40/40),
  but the frozen registration still describes the pre-repair instruments
  (`df01b20f…`, 6/6) and was not amended.
- Smallest remediation: stop instrument edits now; publish one labeled
  addendum that (a) names the final gate/counter sha256 and commit, (b) re-pins
  every C1/C2/C3 receipt to those hashes and the final tip, (c) records the
  registration delta explicitly (do not edit the frozen registration in
  place), and (d) commits the remaining report. Route further repairs to round
  31.

## 2. Write-scope audit (8f51071b..a0dd664, addenda noted)

Committed set at `d72243e` (full `git diff --name-status 8f51071b d72243e1`):
- **Named/allowed:** `corpus/README.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`,
  `corpus/lessons/round-30.md`, `quality/check-index.py` (C3), and all 14
  `.ufo/waves/round-30/**` files (registration, c2/count.py, controls, evidence,
  w1-spec.json, w1-plan.json).
- **Record plane (outside the item's strict path list, conventional):**
  `LOG.md`, `SCORECARD.md` (commit `92d3c86` "records: receipts, wave spec,
  LOG, SCORECARD").
- **Integrator closure (outside the registration's data rule, protocol-consistent):**
  `corpus/lessons/round-30-verifier-spotcheck.md`, commit `d72243e1`
  ("round-30 verifier spot-check (integrator, hyaku)"), authored 04:03:37 while
  wave 1 was running. Same artifact class as `round-29-verifier-spotcheck.md`
  (base commit `8f51071b`). Not authored by a wave-1 seat; it moved master one
  commit past the receipts' cited tip.
- **L1 addenda (lane identity, in-role but outside the seat scope):** `15ddd7d`
  and `a0dd664` wrote `quality/check-index.py` (frozen instrument, twice),
  `.ufo/waves/round-30/c2/count.py` (frozen instrument), `corpus/QUALITY.md`
  (one line), `SCORECARD.md` + `corpus/lessons/round-30.md` (append-only
  errata), the refreshed `evidence/c3-repair-d72243e.txt`, two new evidence
  files, and the wave reports. `q36-successor-receipts.txt` was mutated by an
  unidentified process and reverted in `15ddd7d` (F10).
- **Wave-1 seat writes:** only `.ufo/waves/round-30/w1/reports/` (31 `.md`
  plus the harness `swarm-registry.json`): 27 committed in `15ddd7d`, 3 in
  `a0dd664`, 1 (`RevTrendExpansion.md`) untracked at snapshot. All inside the
  granted report dir; no seat artifact outside it was found.
- **Other:** at first audit (04:02) the tree was clean except
  `?? .ufo/waves/round-30/w1/`; at the 04:14 snapshot the tree is dirty again
  (`M w1/reports/RevC1Fence.md`, `M w1/reports/RevRecordsChain.md`,
  `M SCORECARD.md`, `?? RevTrendExpansion.md`) and `c3-repair-d72243e.txt` was
  refreshed at 04:12:16. This seat wrote only this report; it did not touch
  jj or the lane index. No world-writable or setuid/setgid files under the
  round tree; new scripts `0755`, artifacts `0644`.
- **Fleet repo:** no lane-side write path targets `/home/vgpnk/Projects/shokunin`
  (grep of the gate/counter/round-30 specs finds only prompt/context text). The
  fleet worktree churn seen (`SCORECARD.md` mtime 2026-10-23 20:10,
  `.ufo/state/*.report-baseline` 03:44, `.ufo/watchdog.log` 04:00, untracked
  `AGENTS.md`/`bm.json`/`.omp/mcp.json` dated 2026-10-22) is not attributable to
  mado round-30 seats from local evidence; none is a lane path.
- No compositor/config/sibling-repo writes were observed.

## 3. Credential-shaped strings

Precise scan of `corpus/README.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`,
`corpus/lessons/round-30.md`, the round-30 md/json/txt/py artifacts, and
`quality/check-index.py` for: `AKIA…`, `ghp_/gho_/ghu_/ghs_/ghr_`,
`github_pat_`, `sk-…`, `xox[baprs]-`, PEM private-key blocks,
`password|passwd|secret|token|api_key` assignments, `Bearer` tokens, and
`scheme://user:pass@` URLs — **no matches**. The broad high-entropy pattern
matched only sha256 provenance digests in `SOURCES.md` (expected, not secrets).

## 4. Verified non-findings

- **No shell injection:** neither script contains `shell=True`,
  `os.system`, `os.popen`, `eval`, or a string-form subprocess; every git call
  is an argv list (`check-index.py:41-44` `_git`, `:132` `_run`, and the new
  git-fixture call at `:265-269` uses argv tuples; `count.py:76-77`). The frozen
  SCORECARD fence uses a single-quoted heredoc (`<<'PY'`), passes REV via the
  environment, and interpolates nothing into shell text.
- **Normal runs write nothing:** `strace -f -e openat,creat,unlink,rename,mkdir`
  on the frozen gate `--rev 8f51071b` shows only `/dev/null` `O_RDWR`; on the
  repaired gate (`a0dd664`) it shows **0** non-`/dev/null` write opens; a
  normal `count.py 8f51071b` run likewise shows only `/dev/null` write opens
  (90 events). All real writes are confined to `selftest()`'s
  `TemporaryDirectory`.
- **C3/C2 verdicts reproduce (read-only):** frozen gate at base `8f51071b` ->
  `indexed=41/43 missing=2`, exit 1; at `92d3c86` -> `43/43`, exit 0; selftest
  6/6. Repaired gate (`a0dd664`, sha256 `51b513f5…`): selftest 9/9; base
  `41/43` exit 1; `446dc396`, `d72243e`, `15ddd7d`, `a0dd664` `43/43` exit 0.
  Counter: `8f51071b` literal 28/40, active 31/39, TARGET_MISSED; `446dc396`,
  `d72243e`, `15ddd7d`, `a0dd664` literal 40/52, active 40/40, TARGET_MET.
- **`--rev`/`--root` mutual exclusion and bad-repo handling** return
  `SETUP_ERROR`, exit 2 as documented (`--rev --root`, nonexistent `--repo`);
  the repaired gate also requires one of `--rev`/`--root` (exit 2).

## 5. Remediation priority

1. **F1/F5 (open at `a0dd664`)**: reject leading `-` revs or add
   `--end-of-options` in `count.py` and `check-index.py`; the counter still
   creates `<X>:corpus/QUALITY.md` from a crafted REV. Highest security item.
2. **F2 (open)**: realpath containment for `--root`; F3 is fixed. **F7
   (partial)**: `--rev` still counts symlink blobs — filter on `%(objectmode)`
   (`100644`/`100755`) if the "regular files only" promise is to hold in both
   modes. **F6 (partial)**: require `--repo` (or `-C`) instead of trusting cwd.
3. F4 and F8 are fixed; F9 is a documentation correction.
4. F10 is closed (bytes reverted); redirect `q36-successor-run.sh` output so it
   cannot recur.
5. F11: move `SCRATCH_ROOT` under `/tmp` or declare it in the wave context.
6. **F12**: publish one labeled addendum naming the final gate/counter sha256
   and commit, re-pin every C1/C2/C3 receipt to those hashes and the final tip,
   record the registration delta without editing the frozen registration, and
   commit the remaining report; then stop instrument edits for the round.

No tools were installed or upgraded for this review; nothing was fetched.
