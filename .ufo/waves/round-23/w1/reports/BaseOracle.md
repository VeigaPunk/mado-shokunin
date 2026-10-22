# Round 23 · BaseOracle · base re-measure and harness operability (item C1 no-harm baseline)

Seat: MadoR23.BaseOracle (leaf; read-only against the lane). Judged on: operability.
Lane: /home/vgpnk/Projects/shokunin/mado-shokunin. Lane HEAD: a28e4815aabfa85f55274884000fb2608355f8cf.
Raw outputs: .ufo/waves/round-23/w1/out/BaseOracle/ (index in section 9).

## Verdict

The two no-harm baselines reproduce at base, with exit 0 and identical output on a second run:

- round-22 primary oracle: **57/57** (50/50 proposal, 7/7 supplemental-original).
- round-21 oracle through `round-22/replay.py --mode oracle`: **35/35 + 17/17** (52/52), receipt exit 0.

Both harnesses run and their tamper refusals work for the inputs and the pinned expected manifest. Two defects are demonstrated and need an L1 decision before anyone relies on the harnesses' tamper or identity claims:

- **D1**: both harnesses hash the classifier's bytes for their receipts, but execute it through a bytecode cache. A same-size edit with a preserved mtime lets stale code pass with the new hash recorded (demonstrated on the real classifier: 57/57 and 52/52 with the mutated hash).
- **D2**: the round-21 harness exits 1 on tamper, the same code as a failing measurement, so `replay.py --mode oracle` cannot tell them apart by exit status.

No defect changes the base counts.

## 1. Base identity

- The registration names base tip e33ea304 (round-22 tip). Lane HEAD is a28e481 (round-23 spec commit); its parent 6b383c4 is the registration commit, and e33ea304 is an ancestor (`git merge-base --is-ancestor` succeeded).
- `tools/mado-tripwire.py` is sha256 `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84` at e33ea304, 6b383c4, a28e481, and in the lane working copy. The base counts therefore apply to either base name.
- Base copy: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show a28e4815aabfa85f55274884000fb2608355f8cf:tools/mado-tripwire.py > /fast/scratch/hyaku/mado-r23/BaseOracle/base-tool.py` (sha cd9da20c, verified with sha256sum).

## 2. Requested re-measures (base classifier)

All commands are `python3 -I` runs; each was launched alone (one process at a time).

| # | Command (abbreviated) | Exit | Result | Receipt |
|---|---|---|---|---|
| 1 | `python3 -I .ufo/waves/round-22/oracle/measure.py --tool /fast/scratch/hyaku/mado-r23/BaseOracle/base-tool.py` | 0 | status complete; **57/57** (proposal 50/50, supplemental-original 7/7); integrity_errors []; sealed sources 106, proposal files 52, input files 57; tool sha cd9da20c before and after; 1.31 s; stderr empty | out/BaseOracle/r22-measure-run1.stdout.json |
| 2 | same command, second run | 0 | **57/57**; stdout byte-identical to run 1 (sha256 006cde07...) | out/BaseOracle/r22-measure-run2.stdout.json |
| 3 | `python3 -I .ufo/waves/round-22/replay.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/out/BaseOracle/base-tool.py --mode oracle` | 0 | receipt exit 0, timed_out false, setup_error null, timeout 810 s; tool sha cd9da20c before and after; nested round-21 oracle totals **primary 35/35, supplemental 17/17** (52 cases); scanner exits 0 and 1 only; ~1.1 s | out/BaseOracle/r21-replay-oracle-run1.receipt.json |
| 4 | same command, second run | 0 | nested stdout identical to run 3 (sha256 d98ab799...); tool sha unchanged; 1.09 s | out/BaseOracle/r21-replay-oracle-run2.receipt.stdout (file name differs because of the capture helper) |

Helper checks (`--help`, no scanning): round-22 measure (`--tool`, `--case`, `--group`), round-22 replay (`--tool`, `--mode {oracle,resource-api,resource-cli,corpus}`, `--before-tool`), round-21 oracle (`--tool` only). All exit 0.

Tool-path note: the replay driver refuses any tool outside the lane (defect D3). I therefore used a byte-identical copy inside my out dir (out/BaseOracle/base-tool.py, sha cd9da20c), not the lane's mutable `tools/mado-tripwire.py`. Reasons: the harness loader writes a bytecode cache next to the tool, which would write into the lane's `tools/__pycache__`, and the lane file can change under the run. The round-22 measure used the scratch copy, as the assignment said.

## 3. Controls and tamper probes (scratch copies only; lane files untouched)

Each harness directory was copied to /fast/scratch/hyaku/mado-r23/BaseOracle/tamper/ and modified there.

| # | Case | Exit | Result | Receipt |
|---|---|---|---|---|
| 5 | replay with scratch-path tool (`--tool /fast/scratch/.../base-tool.py --mode oracle`) | 2 | setup_error "ValueError: --tool must resolve inside the repository"; no child spawned (argv empty) | replay-scratch-path-probe.stdout |
| 6 | registered counter form from another directory: `python3 -I .../round-22/oracle/measure.py --tool tools/mado-tripwire.py`, cwd /tmp | 2 | status refused, "[Errno 2] No such file or directory: '/tmp/tools'" (console output, not saved) | none |
| 7 | round-22 copy, unmodified | 0 | 57/57 | r22-copy-control.stdout |
| 8 | round-22 copy, inputs/TimerRun.jsonl with one space before the final newline | 2 | status refused: "input digest/newline mismatch for TimerRun" | r22-tamper-input.stdout |
| 9 | round-22 copy, expected.json with one byte appended | 2 | status refused: "expected.json digest does not match the exact expected.sha256 pin" | r22-tamper-expected.stdout |
| 10 | round-21 copy, unmodified | 0 | primary 35/35, supplemental 17/17 | r21-copy-control.stdout |
| 11 | round-21 copy, inputs/PureJson.jsonl with one space before the final newline | **1** | stdout empty; stderr "snapshot_tampered: inputs/PureJson.jsonl" | r21-tamper-input.stdout / .stderr |
| 12 | round-21 copy, expected.json with one byte appended | **1** | stderr "snapshot_tampered: expected.json" | r21-tamper-expected.stdout / .stderr |
| 13 | round-21 copy, legitimate failure: a mutated classifier (section 4, mutation B) | **1** | primary 19/35, supplemental 10/17 | r21-mutated-tool-legit-fail.stdout |

Result: round-22 refusals exit 2 and round-21 tamper exits 1, the same code as a real failure (row 13). The replay driver passes the child code through, so its exit status cannot separate them (D2).

## 4. Bytecode identity probes (defect D1)

Both harnesses run the classifier as `python3 -I -c WRAPPER <tool> <fixture>`. WRAPPER loads the file with `importlib` (round-22 measure.py:34-38; round-21 measure.py:13-17). That loader writes and reads `<tool dir>/__pycache__/<name>.cpython-314.pyc` and uses it whenever the source's whole-second mtime and size match. Receipts record the sha of the source bytes, not of the code that ran.

Toy module, same loader as WRAPPER (sequence A, B, reader, mtime change; output in harness-probes.summary.json):

- A: source "version-A" → prints version-A; cache written.
- B: same size (19 bytes) and same mtime, contents "version-B" → prints **version-A** (stale; the file's sha is B's).
- Bytes-compile loader (`compile()` of the file bytes, no cache): prints version-B.
- Same B bytes, mtime changed → prints version-B (cache rejected).

Real classifier, round-22 harness, scratch copy (summary in stale-probe.summary.json):

| Step | Case | Exit | Pass | Tool sha in receipt |
|---|---|---|---|---|
| A | base bytes, mtime fixed, cache created | 0 | **57/57** | cd9da20c (base) |
| B | mutated bytes (`"findings": findings, "counts": counts,` → `"findingS": ...`, same size 162432, same mtime), cache still present | 0 | **57/57** (false pass) | 95eed74b... (mutated); integrity_errors [] |
| C | same mutated bytes, cache removed (fresh compile) | 1 | **0/57** | 95eed74b... (mutated) |

Round-21 harness, same stale state (summary in stale-probe-r21-fix.summary.json):

| Step | Harness | Exit | Pass | Tool sha |
|---|---|---|---|---|
| A | old WRAPPER, base bytes, cache created | 0 | 52/52 | cd9da20c |
| B | old WRAPPER, mutated bytes, stale cache | 0 | **52/52** (false pass) | 95eed74b... |
| C | bytes-compile WRAPPER (copy of round-21 harness, same stale cache present) | 1 | **29/52** | 95eed74b... (matches the fresh mutated run, row 13) |

Lane exposure (read-only check, nothing executed): the lane cache `tools/__pycache__/mado-tripwire.cpython-314.pyc` (gitignored by .gitignore line 3) has a header whose source mtime (1792600104) and size (162432) equal the current file, so the loader would accept it. Its code objects equal a fresh compile of the current lane bytes once one internal field is excluded. That field (`co_flags`) also differs for the scratch control built from the same base bytes, so it is a comparison artifact. The cache was written 37 s after the source's last modification. The lane is therefore not stale today, but the hazard is latent.

## 5. Coverage probe (not a harness defect; D5)

Three `"lead"` evidence sites were relabelled to `"leaD"` (same length; each mutant compiled fresh, no cache): base lines 2387 (`return [tuple(hit[:4]) + ("lead",) ...], unparsed`), 2620 (`hits.extend(tuple(hit[:4]) + ("lead",)`), and 2883 (`if evidence == "lead" and ...`). Each mutant scored **57/57** on the round-22 oracle (stale-probe-candidate-*.stdout; stale-probe-candidates-no-effect.summary.json). The oracle does not observe these three sites.

## 6. Harness defects, ranked

**D1 (high impact, latent in lane). Bytecode identity gap in both harnesses.** Evidence: section 4 (B rows: 57/57 and 52/52 with a mutated hash); toy probe. Trigger: a cache from an earlier run, plus a same-size edit whose whole-second mtime matches the cache. Ordinary edits change size or mtime. Restores that keep mtime (tar -x, cp -p, rsync -t, touch -r) can trigger it. Fix options:
  (a) WRAPPER compiles the bytes it has hashed (`src=open(p,"rb").read(); exec(compile(src,p,"exec"), module dict)`). Tested on the round-21 copy (row C: correct 29/52) and on the toy. Not tested on round-22.
  (b) Operational, no code change: delete `<tool dir>/__pycache__` before any measurement, or measure a freshly copied tool.
  Caveat: round-22 measure.py checks its own bytes against expected.json `runner_sha256` (measure.py:473-475). Changing its WRAPPER therefore requires re-sealing expected.json and expected.sha256, which is a frozen-artifact decision for the L1. Round-21 has no such self-check, but it is a frozen round directory too.

**D2 (medium). Round-21 tamper exits 1.** round-21 oracle/measure.py:50-57 raises SystemExit with a string, which exits 1. Line 71 returns 1 for any failing case. Measured in rows 11, 12, 13. Round-22 uses 2 for refusals (rows 8, 9). Fix: refusals exit 2 (edit to a frozen round-21 harness; L1 decision) or the replay driver maps "snapshot_tampered" to a distinct receipt field.

**D3 (low-medium, operability). replay.py path rule.** replay.py:39-45 requires `--tool` (and `--before-tool` in corpus mode, replay.py:140) to resolve inside the lane. Measured in row 5. Consequence: every base copy used by replay or corpus mode has to be staged in the lane, which creates a `__pycache__` there. Fix: document it, or allow a fixed scratch root.

**D4 (low, write bounds). Registered counter form is cwd-relative and loads from the lane.** The registration's H1 command uses `--tool tools/mado-tripwire.py` (row 6, cwd-sensitive). Run from the lane, it would load the classifier through the lane's `tools/__pycache__` and could refresh that cache. [INFERENCE] This is the section 4 mechanism; I did not run it in the lane. Fix: run counters on a copy outside the lane, as done here.

**D5 (low-medium, coverage). Oracle blind spots.** Section 5: three lead-evidence sites change no oracle result when mutated. This limits what the 57/57 claim protects. Fix: one case per path, or record the gap.

**D6 (low, code-read, not exercised). Round-21 checks are looser.** round-21 oracle/measure.py:41-42 defaults a missing evidence key to "observed"; :58-64 never checks the scanner-reported file sha or path against the fixture; :58 records the tool sha once and never re-checks it after the run (round-22 re-checks at measure.py:~856); :51 takes `split()[0]` of the pin file, so trailing text is accepted.

**D7 (info).** (a) `replay.py --mode oracle` runs the round-21 oracle, not the round-22 one; the name is confusing but the registration uses it consistently. (b) Replay receipts embed the child's JSON as an escaped string, so consumers must parse twice. (c) round-22 measure.py:16 hard-codes the lane path (machine-specific).

Nondeterminism: none observed (rows 1-2 and 3-4 each identical). Wrong paths: only D3 and D4 (row 5, row 6). Child caps (384 MiB, 15 s) are as coded; not separately exercised.

## 7. Deviations and constraints

- Tool path: a lane-resident copy in my out dir instead of the lane's `tools/mado-tripwire.py` (section 2 note).
- The lane was not written. Checked after all runs: `git status --short` shows only the pre-existing untracked round-23 entries (w1-assignments.json, w1-record.json, w1-run.json, w1-spec.json, w1/); HEAD still a28e481; tools/__pycache__ and the round-21/22 oracle caches unchanged; oracle directories and tools/ clean in git.
- Scratch work lives under /fast/scratch/hyaku/mado-r23/BaseOracle/ (base-tool.py, tamper/, stale-probe/, pyc-probe/).
- I removed the bytecode cache my out-dir copy created (out/BaseOracle/__pycache__). The out dir holds one copy of the classifier (base-tool.py, sha cd9da20c). Integration should treat it as a probe input, not a tool.
- Four untracked round-23 files in the lane are not mine; not read or changed.
- No subagents spawned; no `tools/`, `corpus/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `PROVINCE.md`, `SHONEN.md`, fixtures, expected files, or other seats' files were written.

## 8. Residual risk and verification gaps

- Not run (outside this item): round-22 replay corpus and resource modes, selftests, precision (H2), supplemental residual truth (H3), the C2 and C3 counters. Not run at any landed tip.
- Not verified: the bytes-compile fix on the round-22 harness (needs re-seal, see D1); a same-size restore in the lane itself (the lane cache is currently consistent).
- The registration's base name (e33ea304) and the assignment's base name (a28e481) refer to the same classifier bytes; I measured the bytes.
- Installs and updates: none. The harnesses need only the system python3 standard library; no packages were installed, no pacman transaction ran, and no host state changed.

## 9. Receipts (out/BaseOracle/)

- base-tool.py: classifier copy, sha256 cd9da20c...
- r22-measure-run1.stdout.json, r22-measure-run2.stdout.json, each with a .stderr (empty).
- r21-replay-oracle-run1.receipt.json (.stderr empty); r21-replay-oracle-run2.receipt.stdout (.stderr empty).
- replay-scratch-path-probe.stdout/.stderr.
- r22-copy-control, r22-tamper-input, r22-tamper-expected (.stdout/.stderr).
- r21-copy-control, r21-tamper-input, r21-tamper-expected, r21-mutated-tool-legit-fail (.stdout/.stderr).
- stale-probe-A-base-creates-pyc, stale-probe-B-mutated-same-size-same-mtime-stale-pyc, stale-probe-C-mutated-cache-removed-fresh (.stdout/.stderr).
- stale-probe-r21-A-old-wrapper-base-creates-pyc, stale-probe-r21-B-old-wrapper-mutated-stale-pyc, stale-probe-r21-C-bytes-wrapper-mutated-stale-pyc-present (.stdout/.stderr).
- stale-probe-candidate-cand-retlead, stale-probe-candidate-cand-hitsextend, stale-probe-candidate-cand-dedupe (.stdout/.stderr).
- Summaries: harness-probes.summary.json (toy probe and first tamper records), stale-probe.summary.json, stale-probe-r21-fix.summary.json, stale-probe-candidates-no-effect.summary.json.

## Verdict line

Baselines reproduce at base: round-22 primary 57/57 and round-21 oracle 35/35 + 17/17, both exit 0 and deterministic. Harness operability is confirmed for these runs. D1 (bytecode identity gap, demonstrated on the real classifier) and D2 (round-21 tamper exit code 1, demonstrated) need an L1 decision before the after-measurement's tamper claims rely on these harnesses. No defect changes the base counts.
