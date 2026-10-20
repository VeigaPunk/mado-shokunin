# SentinelToolSafety — partial

Scope: the eight executable lane tools at 01b80946d92b26370d3012a7da655d00dd135154. At the start of the session `cmp` against `git show 01b8094:<path>` matched for all eight. measure-mutants lives at `.ufo/waves/round-18/measure-mutants.py`; there is no round-19 copy.

Questions asked: does any path write into the lane, run the live gate, run pacman/systemctl, follow transcript content, or execute fetched code?

- **Live gate, pacman, systemctl, fetched code: no path found.** The gate is only ever started with `--selftest` or `--regression` (harm-watch.sh:221 and :227, gate-swap.sh:263).
- **Two paths delete or overwrite outside their stated bounds.** Both are in measure-mutants and both were reproduced in /tmp.
- **Two "committed bytes only" claims are false.** In harm-watch and supersede-sweep, worktree bytes decide the result. One of these is live on the lane right now.

Every repro ran in my own /tmp clones (A = the lane clone being read, B/C/D/S = stand-ins). Nothing was written to the lane except this report.

## Findings (severity order)

### F1 — HIGH — measure-mutants `--workdir` deletes any directory the caller names, including a whole checkout
- **Exploit path.** `root = args.workdir or mkdtemp(...)` (measure-mutants.py:537). The run then calls `shutil.rmtree(mroot)` for each `root/<mutant id>` (:545). When `--keep` is absent it also calls `shutil.rmtree(root, ignore_errors=True)` (:682). There is no check that the tool created `root`, that it is empty, or that it is outside a worktree. The round-19 `--out` guard (:522) covers `--out` only.
- **Repro 1** — a workdir holding an unrelated file:
  ```
  mkdir /tmp/stsafe-wd; echo keep > /tmp/stsafe-wd/CANARY-unrelated.txt
  python3 -I /tmp/stsafe-A/.ufo/waves/round-18/measure-mutants.py --lane /tmp/stsafe-A --workdir /tmp/stsafe-wd --out ...
  rc=0
  ls: cannot access '/tmp/stsafe-wd': No such file or directory
  ```
- **Repro 2** — the workdir is a fresh full clone `/tmp/stsafe-C` (HEAD 01b8094):
  ```
  python3 -I .../measure-mutants.py --lane /tmp/stsafe-A --workdir /tmp/stsafe-C   → rc=0
  ls: cannot access '/tmp/stsafe-C': No such file or directory
  ```
- **Impact.** `--workdir /home/vgpnk/Projects/shokunin/mado-shokunin` (or `~`) would delete the lane, including `.git` and `.jj`, after a successful run. It is one mistyped flag away. [INFERENCE from the two repros; not run against the lane.]
- **Smallest remediation.** When `--workdir` is given, create `tempfile.mkdtemp(dir=args.workdir)` and only ever rmtree that. Alternatively, refuse a non-empty `--workdir`.

### F2 — MEDIUM — harm-watch runs the worktree SCORECARD block even when it differs from REV, and stamps it `measured_commit=REV`
- **Exploit path.** The fleet-round-1 navigation step pulls the `### Counting command` block out of the *worktree* `SCORECARD.md`. When the bytes differ from REV it only writes a NOTE (harm-watch.sh:387). It still runs the block with `bash -s` (:393), and the receipt carries `measured_commit=$REV_SHA` (:389).
- **The rule it breaks.** Every other step goes through `run_pinned`, which skips the command and counts a failure when the pin does not match. The header says the receipt "is only written with measured_commit=<REV> after asserting that the worktree tool bytes equal REV's bytes".
- **Repro.** I copied harm-watch into /tmp with ROOT pointed at clone A, FLEET pointed at a non-existent path, `HARM_TIMEOUT=3` and `MADO_VERIFY_HARNESS=/nonexistent`. I then added `touch /tmp/stsafe-canary-nav` to A's worktree counting block:
  ```
  -rw-r--r-- ... /tmp/stsafe-canary-nav                       ← the block was executed
  NOTE  SCORECARD.md worktree differs from REV (mismatch); counting block read from worktree
  OK    exit=0 group=navigation harm-nav-fleet-round-1.txt ...  ← counted as a pass, not blocking
  RECEIPT tool=/tmp/stsafe-A/SCORECARD.md#Counting-command tool_sha256=f9a42b61… measured_commit=01b80946d92b26370d3012a7da655d00dd135154 ...
  scorecard_sha256=eaea3776… scorecard_state=mismatch
  ```
- **Impact.**
  - Any uncommitted edit to a markdown file becomes shell code that runs.
  - Its result is credited to a commit that does not contain it, which is false provenance on line 1 of the receipt.
  - **This is live now.** The lane worktree has `M SCORECARD.md` (diff +38 lines, `git status` at 15:1x). A harm-watch run at 01b8094 today would execute and credit bytes that are not at 01b8094.
- **Smallest remediation.** Pull the block out of `git show "$REV_SHA:SCORECARD.md"`; the script already writes `$TMP_OBJECT` at :380. Alternatively, call `pin_skip` on mismatch as `run_pinned` does.

### F3 — MEDIUM-LOW — the measure-mutants `--out` guard only protects the `--lane` worktree; a lab run against a clone overwrites the real lane receipt
- **Exploit path.** The guard tests `out == worktree or worktree in out.parents`, where `worktree = git -C <--lane> rev-parse --show-toplevel` (:522). The docstring says this is "so a lab rerun cannot silently overwrite the lane receipt" (:21-24). A lab rerun is exactly a run with `--lane <clone>` whose `--out` points into the real lane, and the guard does not catch that.
- **Repro.** B stands in for the real lane:
  ```
  sha256 B/.ufo/waves/round-18/evidence/measure-mutants.json  58929eea…
  python3 -I A/.../measure-mutants.py --lane /tmp/stsafe-A --out /tmp/stsafe-B/.ufo/waves/round-18/evidence/measure-mutants.json
  rc=0 ; wrote /tmp/stsafe-B/...   sha256 now 9cfe5cca…
  git -C /tmp/stsafe-B status: " M .ufo/waves/round-18/evidence/measure-mutants.json"   (no --force-lane-receipt given)
  ```
- **Smallest remediation.** Resolve the worktree that contains `out.parent` (`git -C out.parent rev-parse --show-toplevel`). Refuse when that call succeeds at all, or at least when it equals `LANE_DEFAULT`.

### F4 — MEDIUM-LOW — supersede-sweep says "Reads committed bytes only"; the ledger comes from the worktree
- **Evidence.** supersede-sweep.py:34 claims committed bytes only. But `DEFAULT_LEDGER = os.path.join(os.path.dirname(__file__), "supersessions.json")` (:44) is opened from disk. The ledger defines `old`/`new`/`scope`/`rows`, so it decides the verdict. Neither its path nor its sha is printed.
- **Live demo on the lane** (read-only; the worktree ledger is currently `M`):
  ```
  sha256 committed ledger 87644b58…   worktree ledger a0e6cfbe…
  supersede-sweep.py 01b8094                         → 3 entries, STALE SKILL.md ×2, rc=1
  supersede-sweep.py 01b8094 --ledger <git show REV:…> → walker-2.17.2 files=13 pointed=13 stale=0, rc=0
  ```
  The same REV gives opposite verdicts. A clone repro that narrowed the scope gave `files=13` versus `files=1`.
- **Smallest remediation.** Default to `git show REV:.ufo/waves/round-19/supersessions.json`, and print the ledger source and sha256 on stderr.

### F5 — LOW — a non-object receipt line crashes anchor-durability with exit 1, the code for "row flagged"
- **Evidence.** :188 catches `JSONDecodeError` only. A valid-JSON non-object line such as `[1]` reaches `rec.get` at :192, which raises AttributeError. The uncaught traceback exits 1, which the tool's exit map (:47) defines as "at least one flagged", not 2 (could-not-evaluate).
- **Repro.** In clone A I committed `.ufo/waves/round-19/fetch/StsafeProbe/receipts.jsonl` = `[1]`, then ran `MADO_LANE=A anchor-durability.py <that commit>`. Result: `rc=1`, `AttributeError: 'list' object has no attribute 'get'`, 0 stdout lines. The control run at 01b8094 gave `mined=81 durable=81 … flagged=0 receipt_files=57`, rc=0.
- **Side note.** `int(rec.get("http_status"))` also accepts `200.9` and `true`→1.
- **Remediation.** Add `if not isinstance(rec, dict): bad += 1; continue`. Map any internal exception to exit 2.

### F6 — LOW — landed-check: the shallow warning depends on the caller's cwd; GIT_DIR and lane config can take over
1. **Shallow warning.** :113 `rev-parse --git-path shallow` returns the relative path `.git/shallow`, and `[ -f ]` tests it against the caller's cwd. With the committed bytes on a `--depth 1` clone, the warning is printed from cwd=clone and silently missing from cwd=/tmp. Both runs print `LANDED`.
   - The worktree already carries the fix (`--path-format=absolute`, `git diff` on landed-check.sh). It is not at 01b8094.
2. **GIT_DIR.** The script does not unset `GIT_DIR`. `GIT_DIR=/tmp/stsafe-B/.git landed-check.sh /tmp/stsafe-A <A-only commit>` printed `MISSING` for an object that is present in A, so it answered for the wrong repo.
3. **Lane config runs a program.** ls-remote (:87) obeys `remote.origin.uploadpack`. A clone configured with a wrapper script produced `/tmp/stsafe-canary-uploadpack`.
   - "Never writes git state" holds. "Read-only posture" does not cover programs that the lane's config tells git to run.
   - Against the real lane this is an https network read to github.com. That is documented at :28-29.
- **Remediation.**
  - Make the fix above absolute in a committed revision.
  - Run `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR -u GIT_OBJECT_DIRECTORY -u GIT_INDEX_FILE`.
  - Use `ls-remote --upload-pack=git-upload-pack`.

### F7 — LOW (doc) — gate-swap says "Read-only on the lane" but writes into the lane
- gate-swap.sh:46 says "Read-only on the lane", yet :255 runs `install -m 0644 … "$EV"` into `.ufo/waves/round-19/evidence/`.
- The write is disclosed at :23-24 and guarded: write-once, refuses to overwrite different bytes.
- Its selftest target is a /tmp copy (:263). The fixture is 17661e0's gate plus one block. In that version the live-plane runs use a sandbox PATH with no hyprctl, so there is no host contact. [INFERENCE from grep: every `MADO_VERIFY_LIVE=yes` run is under `PATH=$SANDBOX`/`$OMB`, and OMB links only coreutils, python3 and git stubs (mado-verify.sh:731-733).]
- **Remediation.** Reword :46 to "read-only on git state; writes only the absent evidence fixture".

### F8 — LOW / latent — harm-watch environment and cleanup
- **No `-I` on two steps.** The round-16/17 `measure.py` (harm-watch.sh:343, :349) and the counting block's `python3 -` run without `-I`. The script directory, or the lane root for `-`, sits first on `sys.path`, and PYTHONPATH and user site-packages apply. A stray `json.py`/`subprocess.py` there would run unpinned under a pinned receipt. None exists today: I listed round-16, round-17 and the lane root.
- **The regression harness is not pinned.** `--regression` (:227) runs `${MADO_VERIFY_HARNESS:-…/tameshi-shokunin/tools/mutate-and-run.sh}` (mado-verify.sh:2166). That is another lane's script, recorded "provenance, not gated" (:2178), and harm-watch passes the env override through.
- **A timeout leaves gate fixtures behind.** The gate has 0 `trap` lines. My `HARM_TIMEOUT=3` run returned `exit=124` for the selftest. `/tmp/w5-mado-m52-selftest.dpLTeR` (15:08:22) and `.fCtmPV` (15:08:24) appeared during that run. They are probably mine [INFERENCE: peers run selftests concurrently]; I left them in place rather than risk deleting a peer's live directory.
- **OUTDIR.** By default (:55) harm-watch writes into the lane under `evidence/harm/`, which is currently untracked. That is its stated purpose.

## Checked and holding
- **mado-tripwire.py executes no transcript content.**
  - eval cells are parsed with `compile(..., PyCF_ONLY_AST)` (:1328). `exec`/`eval` appear only as names to classify (:1060).
  - It opens no file for writing.
  - Its only subprocess is itself, `sys.executable -I me` in `--selftest` (:2005, :2010, :2021).
  - `refuse_path` (:1476-1491) refuses symlinks, anything under `~/.omp/agent` outside `sessions/`, and `agent.db*` names. Only `.jsonl` files are opened.
  - The selftest suites have no absolute args. The two `..` args are the F2 fixtures inside the suite directory.
- **frozen-repin.py stays inside its target, with two side notes.**
  - Writes go only to a staging dir in `--to`'s parent, then one `os.replace`. It refuses symlink, non-empty or non-directory targets and runs only the caller's `--tool`.
  - On SIGKILL, `.frozen-repin-*` could be left in the parent; `finally` covers normal exits.
  - It copies whole transcript lines byte-for-byte: round-19/frozen/inputs equals round-18/frozen/inputs, all 5 files identical, first committed in 4c103b5. Thinking blocks are included.
  - A secret-pattern grep found 1 hit, inside a base64-like blob ("…Me8sk-nniw…"). [INFERENCE: false positive, not a key.]
- **supersede-sweep.py and anchor-durability.py** run only `git -C <lane> rev-parse/ls-tree/show`, never the network, and parse receipts as JSON data only.
- **pacman, systemctl, walker, hyprctl.** None of the eight tools calls them. Gate selftest live checks use replaced-PATH stubs (`PATH="$WLB"; walker_live_rows`, mado-verify.sh:1261).

## Limits
- I did not run gate-swap.sh, a full harm-watch run without a timeout, or measure-mutants against the real lane. I did not test frozen-repin's SIGKILL path.
- The lane worktree drifted from 01b8094 during the session: SCORECARD.md, supersessions.json, landed-check.sh, mado-verify.sh and corpus files are `M`. All findings are cited against the committed bytes, read from clone A checked out at 01b8094. F2 and F4 note where the current worktree drift makes them live.
- Whether the harm-watch/gate selftest leftovers in /tmp are mine is [UNK] beyond the timing evidence.
- All /tmp/stsafe-* scratch has been removed.

## Installs
none
