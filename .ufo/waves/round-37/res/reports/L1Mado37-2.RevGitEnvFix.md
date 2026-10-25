# L1Mado37-2.RevGitEnvFix — GIT_* scrub review (round-37 residual falsify)

- Reviewer: L1Mado37-2.RevGitEnvFix (Godspeed)
- Date/taken: 2026-10-25 (session)
- Lane head: `3f424257a1ea69cd2655770259ba00b423293f4f` (landed data commit; parent `80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b`)
- Git: `git version 2.56.0` (same as w1 evidence)
- Scratch: `/dev/shm/mado37-L1Mado37-2.RevGitEnvFix/` (clones `lane` @ 3f42425, `lane-base` @ 80b83c8). Lane repo untouched: both `.git/index` files byte-unchanged before/after every real-lane run (fleet `d39ceb48ced1a255`, lane `9e90765c49ebd8b4`), `GIT_OPTIONAL_LOCKS=0` used for real-lane runs.
- Ambient `GIT_*` vars in this session: `GIT_EDITOR`, `GIT_PAGER`, `GIT_TERMINAL_PROMPT` (no `GIT_DIR`/`GIT_WORK_TREE` pre-set).

---

## 1. Is the env scrub the only delta in `quality/*.py`? — PASS

The range `80b83c8..3f42425` is exactly one commit (3f42425; parent verified 80b83c8). Its `quality/*.py` portion touches exactly the four files, 17 insertions / 7 deletions, and every hunk is the GIT_* env scrub:

| file | hunks | what changed |
|---|---|---|
| `quality/check-evidence-pointers.py` | 4 | `import os` (:39); `GIT_ENV` filter constant (:66-71); `env=GIT_ENV` on git() (:80-84), status (:177-179), merge-base (:210-211) |
| `quality/check-axis-scores.py` | 2 | `env={k:v for ... if not k.startswith("GIT_")}` on `git()` (:98-99) and on sub-instrument run (:119-121) |
| `quality/check-index.py` | 1 | env filter on `_git()` (:48-52) |
| `quality/check-index-rows.py` | 1 | env filter on `_git()` (:55-59) |

- Full diff verified: `git -C <lane> diff 80b83c8..3f42425 -- quality/*.py` contains no other change (no logic, no I/O, no format change). Blob shas changed on exactly these four paths (see run2 B).
- Neutrality in plain env: original (80b83c8) vs scrubbed gates produce byte-identical output under plain env — sweep.txt plain hashes (`axis=6065f5252110b6fe`, `index=1cb91da21a5846e0`, `rows=752a8879cd9ec8f6`, pointers `6cdfdec445bd6dfe`) equal the receipt's green hashes (which used the fixed gates). The scrub is behavior-neutral absent ambient `GIT_*`.

## 2. Removing the scrub makes the red return — PASS

Unscrubbed gate = blob at 80b83c8 (`check-evidence-pointers.py` `ce0dd98b7115ce3d61e59a205074ef9db6d4e6ec`). Two reproductions:

**(a) w1-faithful, against the real lane (read-only) — byte-for-byte equals `red-green.txt` lines 66-84:**

```
$ env GIT_DIR=/home/vgpnk/Projects/shokunin/.git python3 -I <unscrubbed> --repo <lane> --rev a5aaa09ad38bfd90c13d76ccf371e36c45a2697e
PRED-PTR-r36-v1 error=revision-not-readable:a5aaa09ad38bfd90c13d76ccf371e36c45a2697e   rc=2
$ env GIT_WORK_TREE=/dev/shm python3 -I <unscrubbed> --repo <lane> --rev a5aaa09ad38bfd90c13d76ccf371e36c45a2697e
PRED-PTR-r36-v1 ... inherited_dirty=8 ... verdict=TARGET_MISSED   rc=1
  (8 `dirty:` lines are exactly the D-status lines in red-green.txt:75-82)
```

Fleet .git is non-bare (`is-bare-repository=false`), so `GIT_DIR=$FLEET_GIT` redirects every `git -C repo` call to the fleet repo, where the rev is unreadable (`git rev-parse --verify --end-of-options a5aaa09^{commit}` → `fatal: Needed a single revision`, rc=128 → gate `revision-not-readable` rc=2). `GIT_WORK_TREE=/dev/shm` points git at the wrong work tree: index paths appear deleted → `inherited_dirty=8` → `TARGET_MISSED` rc=1.

**(b) sandbox clone @ 3f42425 with the unscrubbed gate installed — same red:**

- `GIT_DIR=fleet` → rc=2 `revision-not-readable:a5aaa09...` (identical).
- `GIT_WORK_TREE=/dev/shm` → rc=2 `revision-not-readable:a5aaa09...`. Mechanism note: the sandbox repo lives **inside** `/dev/shm`, so under `GIT_WORK_TREE=/dev/shm` git's cwd-prefix filtering (worktree-relative) empties `git ls-tree -r --name-only <rev>` (`0` lines; `--full-tree` restores 10921). The gate's listing check fails closed → dies rc=2. This is a repo-location artifact of the sandbox, not a difference in the scrub; the w1-faithful run (a) shows the canonical dirty=8 red for a repo outside `/dev/shm`.

## 3. With the scrub restored: plain vs ambient outputs are byte-identical — PASS

Sandbox `lane` @ 3f42425, committed (scrubbed) gates, run under `plain` / `GIT_DIR=/home/vgpnk/Projects/shokunin/.git` / `GIT_WORK_TREE=/dev/shm`:

| gate | cmd | rc (all 3) | sha256 (all 3, cmp IDENTICAL) |
|---|---|---|---|
| pointers | `python3 -I quality/check-evidence-pointers.py --rev a5aaa09...` | 0 | `6cdfdec445bd6dfe` (verdict=TARGET_MET) |
| axis | `python3 -I quality/check-axis-scores.py --repo . --rev master` | 1 | `b1457509ec47a10a` (see §5.2) |
| index | `python3 -I quality/check-index.py --rev master --repo .` | 0 | `667bdf4711cbc441` (`indexed=52/52`) |
| rows | `python3 -I quality/check-index-rows.py --rev master --repo .` | 0 | `062c284f0e8e8ae6` (`rows=52`) |

`cmp` on plain-vs-GIT_DIR and plain-vs-WORKTREE outputs: all four gates IDENTICAL. Combined ambient `GIT_DIR=<fleet> GIT_WORK_TREE=/dev/shm` run: rc=0, sha=`6cdfdec445bd6dfe` (same output) — reproduces red-green.txt's "GREEN extra".

## 4. Comparison with `receipts/git-env-green.txt` — PASS (exact reproduction)

Reproduced the receipt's exact green hashes at base commit 80b83c8 with the scrub backported (copied the four scrubbed files; pointed `refs/heads/master` at 80b83c8 so `--rev master` resolves like the original runs):

| receipt line | expected sha256 | reproduced (3 envs, rc=0) |
|---|---|---|
| pointers `--rev a5aaa09...` | `6cdfdec445bd6dfe` | `6cdfdec445bd6dfe` ✓ |
| axis `--repo . --rev master` | `6065f5252110b6fe` | `6065f5252110b6fe` ✓ |
| index `--rev master --repo .` | `1cb91da21a5846e0` | `1cb91da21a5846e0` ✓ |
| rows `--rev master --repo .` | `752a8879cd9ec8f6` | `752a8879cd9ec8f6` ✓ |

Outputs quoted (axis): `MADO_AXIS: checked=3 mismatched=0 rev=80b83c856...`; (index): `MADO_INDEX: rev=master indexed=50/50 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`; (rows): `MADO_INDEX_ROWS: rev=master rows=50 errors=0 warns=3` — identical to the receipt lines 6-14 and to sweep plain hashes. Selftests also match the receipt: `MADO_INDEX_SELFTEST: 12/12 assertions passed`, `MADO_INDEX_ROWS_SELFTEST: 10/10 assertions passed`.

## 5. Residual risk / observations

1. **Selftest fixtures still inherit ambient `GIT_*`** (low, pre-existing, documented): `quality/check-index.py:285-287` and `quality/check-index-rows.py:408-410` run fixture `git init/add/commit` with `env=dict(os.environ, ...)` — they do not strip `GIT_*`. Under `GIT_DIR=<fleet>` the sandbox selftest exits rc=1 (output suppressed); w1's `decoy.txt` shows these fixture writes redirect into a named repo under ambient `GIT_DIR`. The scrub's claim (receipt) covers the gate runs only, and the selftest lines in the receipt are plain-env; this residual is out of the scrub's scope, not a regression of 3f42425.
2. **Axis gate at 3f42425 tip is STALE** (observation, unrelated to scrub): `MADO_AXIS: checked=3 mismatched=2 rev=3f424257...` with `navigation published=50/50 derived=52/52 STALE`, `calibration published=48/48 derived=50/50 STALE`, rc=1 — identical across all three envs, so the byte-identity claim holds (the gate is red at tip for a data/delta reason, not an env reason). At base it is MATCH (receipt-reproduction §4).
3. **Sandbox-location artifact** (see §2b): with the repo under `/dev/shm`, `GIT_WORK_TREE=/dev/shm` triggers git's prefix filtering (`ls-tree` empty), so the unscrubbed gate dies rc=2 rather than the canonical dirty=8 rc=1. This is an artifact of where the scratch clone lives, not of the scrub.

## Verdict

All four assigned items PASS: (1) scrub is the only `quality/*.py` delta; (2) removing it restores the red under both `GIT_DIR=<fleet>` (rc=2 `revision-not-readable`) and `GIT_WORK_TREE=/dev/shm` (rc=1, inherited_dirty=8), byte-matching the w1 red transcript; (3) with the scrub, plain and ambient outputs are byte-identical for all four gates (and under both vars simultaneously); (4) the committed `git-env-green.txt` hashes reproduce exactly at the same base/rev conditions. No actionable defect found in the landed scrub.
