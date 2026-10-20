# ReviewReceipt — mado-r14-w1 (seat MadoR14.ReviewReceipt)

**Status: advisory, rejected design.** Parent integration decision: no receipt wrapper ships; H1–H4 and M1–M8 are not adopted as gate changes. Retained as record only.

Role: reviewer (UFO-FSD leaf; no delegation, no background jobs).
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Milestone: U5 boundaries and regular-source targets. Judged on: coverage, operability.
Scope: the planned minimal receipt wrapper (`ReceiptBuild`: `.ufo/waves/round-14/receipt.py --revision REV --output PATH -- COMMAND`) against the spec's four requirements (gate revision/digest equality, worktree digest equality, command exit propagation, stable receipt text) and the round-13 missing-header case.
Method: read-only. Reads of spec/dispatch JSON, round-13 evidence, `tools/mado-verify.sh`, lessons and seat reports. No gate, selftest, build, git-hash or sha256 command was run. No shared file edited; no commit, push or install.
Tags: [OBS] read here; [INF] inference from [OBS]; [UNK] not settled by repo.

## 0. Verdict

Not ready to implement as written. Four findings (H1–H4) need a planner decision before `receipt.py` is accepted; the Medium items are the contract text the builder must write down. The receipt file does not exist yet: `.ufo/waves/round-14/` holds only `evidence/census-before.txt`, `w1/spec.json`, `w1/dispatch.json` and `w1/reports/swarm-registry.json` [OBS, find listing].

Lane HEAD at read time: `refs/heads/master` = `873ff081b2ac363df771261b0ed950cba50d8988` [OBS `.git/refs/heads/master`]. The gate's current worktree digest is **not** computed here [UNK]; round-13's recorded digest `037b05dcd3f86e12e1b89ee5631f76ce95301b7c411957fad17ff0d7438a6569` is for measured commit `95cbc41` [OBS `.ufo/waves/round-13/evidence/committed-bindings.json:2,4`] and is not asserted current.

## 1. The round-13 missing-header case (R13-V3)

- Routed defect: "future standalone selftest receipts should carry the measured gate revision/digest. `gate-selftest.txt` lacks its own revision header" [OBS `corpus/lessons/round-13-verifier-spotcheck.md:205`].
- The file has only `command:`, `cwd:`, `stdout:` (`MADO_SELFTEST: 310/310 assertions passed`), `stderr:`, `exit=0`, `elapsed_seconds=7.351` [OBS `.ufo/waves/round-13/evidence/gate-selftest.txt:1-9`]. No revision, no gate digest. The same header shape appears in `gate-file-plane.txt:1-3` and `frozen-selftest.txt:1-2`.
- Attribution is therefore external and ambiguous. The lesson names two commits: measured content `95cbc41` and delivered `59cfbdc` [OBS `round-13-verifier-spotcheck.md:94`]. `committed-bindings.json` names `95cbc41` as measured commit [OBS :2]. Seat reports name base `7dcb785…` [OBS `w1/CensusRecon.md:6`, `w1/ReviewNavigation.md:3`]. Three revision strings, and nothing in the selftest file says which one it ran against. The receipt header must close exactly this gap.
- The same file carries `elapsed_seconds` (nondeterministic). "Stable receipt text" must therefore exclude or isolate it (M1).

## 2. Findings (severity-ordered)

### High

**H1. Refusal exit 2 is indistinguishable from a propagated child exit 2.**
- The gate's exit map already gives 2 a fixed meaning: "2 = tool/usage error (bad args; a failing --selftest)" [OBS `tools/mado-verify.sh:12-13`].
- The snapshot writer already uses 2 for every refusal: `:1903`, `:1913`, `:1924`, `:1932`, `:2024`, `:2033` [OBS].
- Round-13's own registry review logged "four modes give `2` four meanings" as a Medium defect [OBS `.ufo/waves/round-13/w1/ReviewRegistry.md:83`, F4]. The planned wrapper adds a fifth meaning.
- Requirement: on refusal, write no receipt file and print a stable first line `RECEIPT: REFUSED <reason>`. A receipt file exists iff COMMAND ran. The planner may keep exit 2 for refusal (the spec says so) only with that marker and file-absence as the documented discriminator.

**H2. The digest comparison can fail open.**
- Fallback to a literal: the snapshot writer writes `gate-sha256: unavailable` when hashing fails (`mado-verify.sh:2006-2008`). The loader only tests non-empty (`:2091`). The diff compares strings for equality (`:2208-2211`). Two `unavailable` headers compare SAME, silently. The wrapper must not copy this. If either digest cannot be produced, exit 2 with `RECEIPT: REFUSED` and no receipt.
- Pipeline masking: the omarchy check computes `blob=$(git show "HEAD:…" | sha256sum)` [OBS `mado-verify.sh:3153`]. git's failure is hidden in the pipeline and the empty-stdin digest `e3b0c442…` is non-empty, so the empty check cannot catch it. The wrapper must check `git cat-file blob REV:tools/mado-verify.sh` returncode before hashing. Use raw `cat-file`, not `show`. The lane root has no `.gitattributes` [OBS root listing], so textconv is not expected, but raw bytes remove the question.
- Validate both digests as 64 lowercase hex before comparing.
- Resolve REV with `git rev-parse --verify --quiet "${rev}^{commit}"` (existing pattern, `harness.sh:924`) and record the input string and the full resolved SHA. A branch name moves.
- Missing-input cases (REV unresolvable, REV blob absent, worktree gate absent, unreadable) each need a selftest fixture expecting exit 2 and no file (L2).

**H3. The wrapper cannot receipt uncommitted gate edits this round.**
- GateImplement edits `tools/mado-verify.sh` in the worktree [OBS spec GateImplement "Only GateImplement edits tools/mado-verify.sh"], and the contract forbids commits for seats.
- `git cat-file REV:tools/mado-verify.sh` returns the committed gate. On REV = HEAD (`873ff08`) the worktree digest differs, so the wrapper refuses, correctly. Result: no receipt can bind the round-14 gate until a commit exists.
- [INF] This is an operability block, not a bug. The planner must choose: (a) L1 commits the gate, then receipts REV, or (b) an explicit expected-digest mode (`--gate-sha256 …`) whose header says `uncommitted`. Neither is in the spec. Do not let a receipt print a REV for an uncommitted gate.

**H4. Generic output persistence breaches the data fence.**
- Spec: "Persist command and captured output" for any COMMAND. Contract: no raw session logs/titles, no device/output identities.
- Round-13 M4 was a real incident: unfiltered Wayland output retained in scratch [OBS `corpus/lessons/round-13.md:13`].
- Receipts under `.ufo/waves/` are not ignored: `.gitignore` lists only `.ufo/interactive-sessions/` [OBS `.gitignore:1`; AttackCoverage.md:120]. A receipt of a compositor/monitor command would be committable.
- Requirement: restrict COMMAND to the gate's shape-only output for this round, or write captured output only to an operator-named path outside the lane tree, and state the fence in the receipt header. Default: restrict. Planner decision.

### Medium

**M1. Stable receipt text is undefined.**
- Specify field keys, order, encoding, trailing newline. Exclude `created` and `elapsed_seconds` from the comparable body, or place them in a labelled provenance block. The snapshot does the same: `created:` is provenance and never compared [OBS `mado-verify.sh:1814`].
- Reuse existing key names: `# tool:` and `# gate-sha256:` are written at `:2013-2014` and read at `:2057-2058`. Inventing `gate_sha256` creates a second convention.
- Exit key: round-13 evidence uses `exit=N` (`gate-selftest.txt:8`, `frozen-selftest.txt:18`), while round-14 `census-before.txt:2` uses `exit: 0`. Pick one; recommend `exit=N`, the R13-V3 file's own form.

**M2. Two whole-file/pin digests of the same gate exist.**
- Snapshot `gate-sha256` is the whole-file sha256 of the running script (`:2006`). The regression pin `PIN_MADO` hashes the file with R7/R8 marker blocks excised (`ReviewRegistry.md:86`, F7). Any edit outside those blocks moves the pin.
- Receipt header must name the digest "whole-file sha256 of tools/mado-verify.sh" so it is never confused with the pin.

**M3. Time-of-check/time-of-use and create race.**
- The gate resolves itself via `readlink -f "$0"` (`:1823`), so the file can change mid-run. Re-hash the worktree gate after COMMAND exits. If it changed, record both digests and mark the receipt `gate-changed-during-run`, exit nonzero.
- The existing writer checks `[ -e "$dest" ]` (`:1901`) and writes later with no exclusive create (`:2021`). The wrapper should reserve `--output` with `os.open(…, O_CREAT|O_EXCL|O_WRONLY)` before running COMMAND, so refusal happens before any command runs, then write once at the end.

**M4. Exit propagation needs explicit precedence.**
- Child rc 0–255 propagates unchanged. A signal (Python negative returncode) maps to 128+N and is recorded as `signal=N`.
- Precedence: receipt written and child rc ≠ 0 → exit child rc, with the receipt. Receipt write fails and child rc = 0 → exit 2 with `RECEIPT: REFUSED`. Receipt write fails and child rc ≠ 0 → exit child rc, with the REFUSED line printed. A nonzero child rc must never be masked by 0.

**M5. Do not inherit the gate's 0/1-only rule silently.**
- Snapshot writes only if child rc ∈ {0,1}; otherwise refuses (`mado-verify.sh:1909-1915`). A generic wrapper should record any rc. If the planner wants the 0/1 rule, it must be stated, because it is gate-specific.

**M6. Stream capture versus pass-through.**
- The snapshot merges streams via `$(… 2>&1)` (`:1906`), strips trailing newlines, and echoes (`:1908`). S1 asserts the child verdict still prints (`:1182`).
- The spec says stdout and stderr are captured separately. Then the wrapper must tee to the terminal as well, or operators see nothing of the gate verdict. Recommend: capture separately as `stdout:`/`stderr:` sections (matching `gate-selftest.txt`) and tee to the terminal.

**M7. Reuse decision: `--snapshot` already exists.**
- `--snapshot FILE` already writes a v1 receipt with `gate-sha256`, never-overwrite, row-count verification, and self-checking counts (`:1851-1855`, `:2011-2036`). It covers verdict rows only, not selftest or regression output.
- A second receipt format is justified only for standalone selftest/regression output. The planner must either extend the v1 header (`# revision:`, gate-only) or justify a separate format, and must not leave two undocumented conventions.

**M8. Revision claim scope (R13-V2).**
- A receipt binds one run to one gate digest. It does not establish the lane tree, the verdict, or equality of outputs across revisions. The gate reads `$HOME` config planes (`ROOT="${MADO_VERIFY_ROOT:-$HOME}"`, `:83`), so verdict depends on environment. Receipt text must not say "byte-identical across revisions" or "verdict at REV". Name the digest "gate file" explicitly, not "worktree".

### Low

**L1. Undefined roots.** "Runs COMMAND from lane root": derive via `git rev-parse --show-toplevel` and assert it; the script location (`.ufo/waves/round-14/`) is not the lane root. `--output` relative base must be stated (recommend lane root).

**L2. Selftest coverage is incomplete.** The spec lists matching and mismatching digest, exit propagation, stable ids. Add: unresolvable REV; missing REV blob; missing worktree gate; existing output refused before COMMAND runs; signal exit; refusal vs child exit 2 distinguishable; gate changed mid-run; non-hex digest. "Stable ids" is undefined: specify the marker strings. Fixtures must live in a temp git repo, never the lane repo.

**L3. Red-before evidence is missing from the plan.** A selftest can pass vacuously if it never asserts the mismatch path. Round-13 showed an unexercised helper defect (`UnboundLocalError`) that only the first self-invocation caught [OBS `.ufo/waves/round-13/evidence/frozen-selftest.txt:5-16`; lesson M5]. L1 must run the selftest once and must see it red against a broken mutant (digest comparison removed).

**L4. Info.** `git show` does not carry the exec mode of a blob [OBS `harness.sh:1489`]. Irrelevant to digest equality; relevant only if the wrapper ever executes the gate from a blob.

## 3. Requirement-by-requirement

| Spec requirement | Status | Finding |
|---|---|---|
| Gate source revision/digest equality | Under-specified | H2, H3, M2 |
| Worktree digest equality | Ambiguous ("worktree" = gate file only?) | M2, M3, M8 |
| Command exit propagation | Under-specified; collision | H1, M4, M5 |
| Stable receipt text | Undefined | M1, L2 |
| Round-13 missing-header case | Addressed only if header carries REV + digest + exit key | §1, M1 |

## 4. Residual risk and verification gaps

- No digest computed; the current gate's whole-file sha256 is [UNK]. `committed-bindings.json` is historical.
- `receipt.py` absent at review; findings bind to the spec text, not to builder bytes. Re-review when it lands.
- Single-host, no-run review: the selftest and the refusal paths are unexercised [UNK]. L1 must run them once, red-before and green-after.
- No external sources opened; none admitted or rejected.
- Tooling installed or updated by this seat: none.

## 5. Checks for the main agent

1. Decide H1 (refusal marker + file absence), H3 (committed vs expected-digest mode), H4 (COMMAND scope). Blocking.
2. Confirm M7: extend `--snapshot` or justify a second format.
3. After landing: run `receipt.py --selftest` once red-before (mutant) and green-after; assert all L2 cases.
4. Compute the gate's whole-file sha256 at the receipt revision and compare with `committed-bindings.json` only as provenance, not as current status.
