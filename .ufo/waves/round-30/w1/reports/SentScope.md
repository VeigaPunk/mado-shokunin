# SentScope — round-30 w1 security / write-scope sentinel

Report only. No lane bytes edited; this file and nothing else was written by
this seat. Lane audited at `d72243e1` (tip at audit time; wave receipts cite
`92d3c86`). Methods: source read, read-only gate/counter runs at base and tip,
`strace` of write syscalls, adversarial argv/root tests under `/tmp`, git/jj
state inspection.

Verdict: **no shell injection and no credential leak**; one *writes-nothing*
contract violation in the C2 counter, two `--root`-mode provenance/vacuity
defects in the C3 gate, and no seat write outside the round's declared
artifacts aside from the integrator closure commit noted in §2.

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

## 2. Write-scope audit (8f51071b..d72243e1)

Committed set (full `git diff --name-status 8f51071b d72243e1`):
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
- **Wave-1 seat writes:** only `.ufo/waves/round-30/w1/reports/` (13 `.md` plus
  the harness `swarm-registry.json`), untracked; inside the granted report dir.
- **Other:** at audit start `git status` was clean except
  `?? .ufo/waves/round-30/w1/`; at 04:06:46 a live process rewrote
  `quality/q36-successor-receipts.txt` (F10), so the current status is
  `M quality/q36-successor-receipts.txt` plus `?? .ufo/waves/round-30/w1/`.
  jj working copy empty at audit start, parent `d72243e1`; no lane jj/index
  mutation by this seat. No world-writable or setuid/setgid files under the
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

- **No shell injection:** neither new script contains `shell=True`,
  `os.system`, `os.popen`, `eval`, or string-form subprocess; every git call is
  an argv list (`check-index.py:32-36,105-110`; `count.py:50-51`). The frozen
  SCORECARD fence uses a single-quoted heredoc (`<<'PY'`), passes REV via the
  environment, and interpolates nothing into shell text.
- **Normal runs write nothing:** `strace -f -e openat,creat,unlink,rename,mkdir`
  on `check-index.py --rev 8f51071b` shows only `/dev/null` `O_RDWR` (2 events);
  a normal `count.py 8f51071b` run likewise shows only `/dev/null` write opens
  (90 events). All real writes are confined to `selftest()`'s
  `TemporaryDirectory` (`check-index.py:123-186`).
- **C3 kill rule holds (independently reproduced, read-only):** gate at base
  `8f51071b` -> `indexed=41/43 missing=2`, exit 1; at `92d3c86` -> `43/43`,
  exit 0; `--root .` -> `43/43`, exit 0; `--selftest` -> `6/6`, exit 0.
- **`--rev`/`--root` mutual exclusion and bad-repo handling** return
  `SETUP_ERROR`, exit 2 as documented (`--rev --root`, nonexistent `--repo`).

## 5. Remediation priority

1. Reject leading `-` revs (or add `--end-of-options`) in `count.py` and
   `check-index.py` — closes F1/F5 in ~4 lines.
2. `--root`: realpath containment (F2) and `isdir(kdir)` setup error (F3).
3. Wrap the gate's `rev-parse` fallback in the existing setup-error handler (F4).
4. F6-F9 are documentation/consistency; no lane state changes needed.
5. F10: restore `quality/q36-successor-receipts.txt` from HEAD (or commit the
   regenerated receipt deliberately); redirect future runner output out of the
   tracked path.
6. F11: move `SCRATCH_ROOT` under `/tmp` or declare it in the wave context.

No tools were installed or upgraded for this review; nothing was fetched.
