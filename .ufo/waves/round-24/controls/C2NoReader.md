# Round-24 control C2NoReader

Control commit: `6219db5b16f3f424e8eb6624bafedf5f499beb87`; parent: `4f21d9956e8c7a5d9f824ff24b9a4426a3f51949`.
Scratch clone: `/fast/scratch/hyaku/mado-r24/ctl/C2NoReader`.
Axes: calibration-target sensitivity; execution provenance; exact restoration.

## Control and expected detector

The cheap control deletes all reading/checking behavior from the seven assigned lane scripts, replacing each with a silent exit-0 stub, and appends a round-24 status table marking all twelve manifest capabilities `works`. The original capability rows and the frozen counter/manifest are unchanged. The fleet sources-census script is outside the assigned seven and is not modified.

Expected detector: the frozen C2 counter must reject all stubbed capabilities because an allowed exit code alone cannot satisfy their required stdout regexes. The unaffected real sources registry can still work. Target is `mismatches=0`; a nonzero mismatch count means this control does not meet it.

## Exact construction

First read the lane's round-24 registration, `skill://godspeed`, and `/home/vgpnk/.omp/agent/RULES.md`. No tool was installed or updated; existing strace 7.2 supplied execution tracing.

Clone and checkout commands:

```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE prlimit --as=4294967296 --core=0 git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r24/ctl/C2NoReader
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/C2NoReader checkout -q 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

File operations used the write tool for whole-file replacements, not an unrecorded shell transform. These three `.sh` files were replaced with exactly the following 27-byte UTF-8 content:

- `tools/mado-verify.sh`
- `.ufo/waves/round-19/landed-check.sh`
- `.ufo/waves/round-20/isolation-check.sh`

```bash
#!/usr/bin/env bash
exit 0
```

These four `.py` files were replaced with exactly the following 43-byte UTF-8 content:

- `tools/mado-tripwire.py`
- `tools/mado-assessment.py`
- `.ufo/waves/round-20/tw-precision.py`
- `.ufo/waves/round-20/a2/a2-guards.py`

```python
#!/usr/bin/env python3
raise SystemExit(0)
```

An append-only hashline edit added the following heading and table to `SCORECARD.md` (one separating blank line; no original line removed):

```markdown
## Capability status (round 24 re-demonstration)

| Capability | Status |
|---|---|
| sources registry | works |
| verdict gate (live + file plane) | works |
| hermetic self-test | works |
| mutation regression with re-cut | works |
| post-hoc transcript tripwire | works |
| tripwire frozen replay (gate entry) | works |
| landedness check | works |
| tripwire evidence marker | works |
| harness fail-closed check | works |
| tripwire reached-body sweep | works |
| detector removal-side guard | works |
| artifact-only assessment integrity | works |
```

The single control commit was made with these exact commands; the hook override applies to this invocation only and writes no configuration:

```sh
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/C2NoReader add -- tools/mado-verify.sh tools/mado-tripwire.py tools/mado-assessment.py .ufo/waves/round-19/landed-check.sh .ufo/waves/round-20/isolation-check.sh .ufo/waves/round-20/tw-precision.py .ufo/waves/round-20/a2/a2-guards.py SCORECARD.md
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/C2NoReader -c user.name=ctl -c user.email=ctl@local -c core.hooksPath=/dev/null commit -m 'control: silent no-reader tools with all-works status'
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/C2NoReader rev-parse HEAD
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/C2NoReader show --stat 6219db5b16f3f424e8eb6624bafedf5f499beb87
```

Full `git show --stat` output:

```text
commit 6219db5b16f3f424e8eb6624bafedf5f499beb87
Author: ctl <ctl@local>
Date:   Fri Oct 23 00:42:03 2026 -0300

    control: silent no-reader tools with all-works status

 .ufo/waves/round-19/landed-check.sh    |  189 +-
 .ufo/waves/round-20/a2/a2-guards.py    |  188 +-
 .ufo/waves/round-20/isolation-check.sh |  252 +-
 .ufo/waves/round-20/tw-precision.py    |  248 +-
 SCORECARD.md                           |   17 +
 tools/mado-assessment.py               |  234 +-
 tools/mado-tripwire.py                 | 3465 +-------------------------
 tools/mado-verify.sh                   | 4195 +-------------------------------
 8 files changed, 24 insertions(+), 8764 deletions(-)
```

## Frozen detector identity and bounds

Lane counter SHA256 before and after all runs: `sha256:a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8`.
Lane manifest SHA256 before and after all runs: `sha256:e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02`.
`git show 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949:.ufo/waves/round-24/c2/count.py` and the corresponding manifest in the clone, piped to bounded `sha256sum`, returned these same digests. All three counter outputs also report them. Neither frozen file was edited.

Every detector invocation below runs the lane's committed counter and manifest, with `MADO_LANE` set to the clone. The wrapper is identical except REV and trace filename: outer timeout 900 seconds, 4 GiB address-space ceiling, no core dumps, and strace `--kill-on-exit -f` to contain the traced process tree. The counter supplies its own per-row timeouts/process-group cleanup. All invocations completed normally with exit 1, not timeout 124. strace returned after its traced descendants terminated; no detector process tree remains running.

Initial detector hashing command:

```sh
timeout 30 sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/manifest.json
```

## Pristine invocation

Run before editing any clone byte. Actual tool-reported wall time: 488.94 seconds.

```sh
timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C2NoReader prlimit --as=4294967296 --core=0 strace --kill-on-exit -f -qq -e trace=execve -s 4096 -o /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/pristine.execve python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

Full stdout (stderr empty):

```text
sources registry	stated=works	observed=works	OK	exit=0
verdict gate (live + file plane)	stated=works	observed=works	OK	exit=0
hermetic self-test	stated=works	observed=works	OK	exit=0
mutation regression with re-cut	stated=works	observed=works	OK	exit=0
post-hoc transcript tripwire	stated=works	observed=works	OK	exit=0
tripwire frozen replay (gate entry)	stated=works	observed=works	OK	exit=1
landedness check	stated=works	observed=works	OK	exit=1
tripwire evidence marker	stated=works	observed=fails	MISMATCH	exit=0
harness fail-closed check	stated=works	observed=works	OK	exit=0
tripwire reached-body sweep	stated=works	observed=works	OK	exit=0
detector removal-side guard	stated=works	observed=works	OK	exit=0
artifact-only assessment integrity	stated=works	observed=works	OK	exit=0
mismatches=1/12 revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 manifest_sha256=e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02 counter_sha256=a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8
```

Exit: **1**. The pre-existing mismatch is `tripwire evidence marker`.

## Mutated invocation — scored control commit

Both the clone checkout and archived REV contain the stubs at the time of this run. Actual tool-reported wall time: 2.39 seconds.

```sh
timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C2NoReader prlimit --as=4294967296 --core=0 strace --kill-on-exit -f -qq -e trace=execve -s 4096 -o /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/mutated.execve python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py 6219db5b16f3f424e8eb6624bafedf5f499beb87
```

Full stdout (stderr empty):

```text
sources registry	stated=works	observed=works	OK	exit=0
verdict gate (live + file plane)	stated=works	observed=fails	MISMATCH	exit=0
hermetic self-test	stated=works	observed=fails	MISMATCH	exit=0
mutation regression with re-cut	stated=works	observed=fails	MISMATCH	exit=0
post-hoc transcript tripwire	stated=works	observed=fails	MISMATCH	exit=0
tripwire frozen replay (gate entry)	stated=works	observed=fails	MISMATCH	exit=0
landedness check	stated=works	observed=fails	MISMATCH	exit=0
tripwire evidence marker	stated=works	observed=fails	MISMATCH	exit=0
harness fail-closed check	stated=works	observed=fails	MISMATCH	exit=0
tripwire reached-body sweep	stated=works	observed=fails	MISMATCH	exit=0
detector removal-side guard	stated=works	observed=fails	MISMATCH	exit=0
artifact-only assessment integrity	stated=works	observed=fails	MISMATCH	exit=0
mismatches=11/12 revision=6219db5b16f3f424e8eb6624bafedf5f499beb87 manifest_sha256=e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02 counter_sha256=a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8
```

Exit: **1**.

### Every row still observed `works`

Only **`sources registry`** remains `observed=works`, exit 0. Its real `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate` ran against the extracted control tree. That fleet script and `corpus/SOURCES.md` were not stubbed, so this is an unaffected real check, not a silent-stub acceptance hole.

No capability backed by any of the seven stubbed scripts remains `works`: all eleven are observed `fails` despite exit 0. Ten formerly working capabilities switch to fails; `tripwire evidence marker` was already fails on pristine bytes.

### Which script bytes actually ran

The frozen manifest deliberately uses the clone checkout, not the archived REV, for `tw-precision.py` and `a2-guards.py` (argv and cwd both use `LANE`). The successful execve records at `mutated.execve:811,845` are:

```text
26655 execve("/usr/bin/python3", ["python3", "/fast/scratch/hyaku/mado-r24/ctl/C2NoReader/.ufo/waves/round-20/tw-precision.py", "6219db5b16f3f424e8eb6624bafedf5f499beb87"], 0x55bfa5744d00 /* 267 vars */) = 0
26657 execve("/usr/bin/python3", ["python3", "/fast/scratch/hyaku/mado-r24/ctl/C2NoReader/.ufo/waves/round-20/a2/a2-guards.py", "6219db5b16f3f424e8eb6624bafedf5f499beb87", "--fixtures-rev", "6a7d9ca0d2124a4077074b800c94a9bc1184441c"], 0x55bfa5740ee0 /* 267 vars */) = 0
```

Both clone files had the Python-stub SHA256 `sha256:29453a6f2fb8c3e5f0e6fefb688ae00cbc5d2d36d2eb762112a1553e33167ae0` before restoration. Thus the control really executed the stubs at the two `LANE` paths, not pristine lane copies or merely archived stubs. The identical a2 command is cached once by count.py and supplies both `tripwire reached-body sweep` and `detector removal-side guard`.

The other five assigned scripts ran from the extracted tree `/fast/scratch/hyaku/mado-r24/c2/run-6219db5b-l1uvrkww/tree`. Successful execve evidence is in `mutated.execve` at lines 701/718/735 (`mado-verify` modes), 753/755/757/759 plus 777 (`mado-tripwire` suites and frozen mode), 794 (`landed-check`), 828 (`isolation-check`), and 862 (`mado-assessment`). The working-directory-relative tripwire suite paths resolve under TREE per the frozen manifest. The unchanged fleet census script ran at trace line 68. The counter removed its temporary extracted tree on exit.

## Restoration and restored invocation

After the mutated detector returned, this exact command restored all seven scripts and SCORECARD to their original bytes, without adding a second commit or changing the preserved control commit:

```sh
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/C2NoReader restore --source=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 --worktree -- tools/mado-verify.sh tools/mado-tripwire.py tools/mado-assessment.py .ufo/waves/round-19/landed-check.sh .ufo/waves/round-20/isolation-check.sh .ufo/waves/round-20/tw-precision.py .ufo/waves/round-20/a2/a2-guards.py SCORECARD.md
```

`sha256sum` was run on all eight paths before mutation, on the mutated checkout, immediately after restoration, and again after the restored detector. Exact command for the eight-file measurements:

```sh
timeout 30 sha256sum /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/tools/mado-verify.sh /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/tools/mado-tripwire.py /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/tools/mado-assessment.py /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/.ufo/waves/round-19/landed-check.sh /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/.ufo/waves/round-20/isolation-check.sh /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/.ufo/waves/round-20/tw-precision.py /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/.ufo/waves/round-20/a2/a2-guards.py /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/SCORECARD.md
```

Observed hashes (the pristine and both restored measurements agree byte-for-byte):

| File | Pristine SHA256 = restored SHA256 | Mutated SHA256 |
|---|---|---|
| `tools/mado-verify.sh` | `sha256:050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1` | `sha256:fb99eae951f1adc14d1a4a9a186c21930db2786b3208c94c7d9af382bd1048e5` |
| `tools/mado-tripwire.py` | `sha256:cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84` | `sha256:29453a6f2fb8c3e5f0e6fefb688ae00cbc5d2d36d2eb762112a1553e33167ae0` |
| `tools/mado-assessment.py` | `sha256:66aefd03f25d834fbfcfee6b295c1c032f01b2a94ca321396b7558cca59de9d4` | `sha256:29453a6f2fb8c3e5f0e6fefb688ae00cbc5d2d36d2eb762112a1553e33167ae0` |
| `.ufo/waves/round-19/landed-check.sh` | `sha256:ca1f76b4c19563f44d919b06ee815c3e18e5dd6598304d420d84ec64974ae63c` | `sha256:fb99eae951f1adc14d1a4a9a186c21930db2786b3208c94c7d9af382bd1048e5` |
| `.ufo/waves/round-20/isolation-check.sh` | `sha256:f7aa051faee522f3c4b61494a7a75078b469a1b0f1d0f7503caa3f89777736e1` | `sha256:fb99eae951f1adc14d1a4a9a186c21930db2786b3208c94c7d9af382bd1048e5` |
| `.ufo/waves/round-20/tw-precision.py` | `sha256:bd3bdc23747a6d8f195e69528f532988202db4ab3476d141a8ff46871e42a8e7` | `sha256:29453a6f2fb8c3e5f0e6fefb688ae00cbc5d2d36d2eb762112a1553e33167ae0` |
| `.ufo/waves/round-20/a2/a2-guards.py` | `sha256:414034d57ad38719df9489201c71fce7cb39edc29a5bf25ab971cbc57a4836ef` | `sha256:29453a6f2fb8c3e5f0e6fefb688ae00cbc5d2d36d2eb762112a1553e33167ae0` |
| `SCORECARD.md` | `sha256:1003b79ae3a7ccaad5a062abefa017d014e331cd55c234b232a40d099a7eb5ea` | `sha256:32245c2f2c6121201dd5cbd464fe4dfbe1e0f4869d2dc289b83e30cffc603bae` |


Restored detector command, still using the same frozen detector and the restored clone checkout, with the original REV archived again. Actual tool-reported wall time: 546.36 seconds.

```sh
timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C2NoReader prlimit --as=4294967296 --core=0 strace --kill-on-exit -f -qq -e trace=execve -s 4096 -o /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/restored.execve python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

Full stdout (stderr empty):

```text
sources registry	stated=works	observed=works	OK	exit=0
verdict gate (live + file plane)	stated=works	observed=works	OK	exit=0
hermetic self-test	stated=works	observed=works	OK	exit=0
mutation regression with re-cut	stated=works	observed=works	OK	exit=0
post-hoc transcript tripwire	stated=works	observed=works	OK	exit=0
tripwire frozen replay (gate entry)	stated=works	observed=works	OK	exit=1
landedness check	stated=works	observed=works	OK	exit=1
tripwire evidence marker	stated=works	observed=fails	MISMATCH	exit=0
harness fail-closed check	stated=works	observed=works	OK	exit=0
tripwire reached-body sweep	stated=works	observed=works	OK	exit=0
detector removal-side guard	stated=works	observed=works	OK	exit=0
artifact-only assessment integrity	stated=works	observed=works	OK	exit=0
mismatches=1/12 revision=4f21d9956e8c7a5d9f824ff24b9a4426a3f51949 manifest_sha256=e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02 counter_sha256=a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8
```

Exit: **1**. The result and every capability row exactly match the actual pristine invocation.

Final hash command:

```sh
timeout 30 sha256sum /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/tools/mado-verify.sh /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/tools/mado-tripwire.py /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/tools/mado-assessment.py /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/.ufo/waves/round-19/landed-check.sh /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/.ufo/waves/round-20/isolation-check.sh /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/.ufo/waves/round-20/tw-precision.py /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/.ufo/waves/round-20/a2/a2-guards.py /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/SCORECARD.md /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/manifest.json /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/pristine.execve /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/mutated.execve /fast/scratch/hyaku/mado-r24/ctl/C2NoReader/restored.execve
```

Trace artifact hashes:

- `/fast/scratch/hyaku/mado-r24/ctl/C2NoReader/pristine.execve`: `sha256:48da98d8d6ecad0b7a698b869d4786e410a93bbba8489c6544d92430f232c625`
- `/fast/scratch/hyaku/mado-r24/ctl/C2NoReader/mutated.execve`: `sha256:32df032d354589cf3f337787c8bd9f4f53759eba84b068fe7f69ff2bd2822c2a`
- `/fast/scratch/hyaku/mado-r24/ctl/C2NoReader/restored.execve`: `sha256:b4ce3e5fd0c764b060d9b8933fb4e75adb4c4122d517e52cdb681ea9b519254a`

## Commit patch and verdict

Patch export executed as a bounded subprocess, with its complete stdout saved byte-for-byte by the write tool to `.ufo/waves/round-24/controls/C2NoReader.patch`:

```sh
timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE prlimit --as=4294967296 --core=0 git -C /fast/scratch/hyaku/mado-r24/ctl/C2NoReader format-patch -1 --stdout
```

Patch export exit: 0; bytes: 427217; SHA256 of captured patch bytes: `sha256:8c51d7c9782cdc94b6f0d0a37c24763f1589e16c8357d58344b640284bc8b998`. Export occurred after restoration; `format-patch` reads HEAD's committed tree, not the restored working files, so the patch contains the actual stub control.

The clone HEAD remains `6219db5b16f3f424e8eb6624bafedf5f499beb87` to retain the one control commit, while all eight working files are intentionally restored to parent bytes. To reproduce the scored control in that clone, restore those eight paths from the control commit before scoring: the two `LANE` scripts are checkout-bound, not REV-bound. The frozen counter was never edited to hide this distinction.

Mutation-test verdict: **inconclusive**, not killed or survived, because the pristine detector already fails (1/12 mismatches). The observed control result is nevertheless unambiguous: **11/12 mismatches, target not met**, and no stubbed row is leniently accepted. Restored bytes and behavior match pristine. This receipt neither changes the contract nor integrates/ships the control.

CONTROL_MEETS_TARGET: no
