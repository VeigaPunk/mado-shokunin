# CtlC2DoNothing — C2 before value

## Control and expected detector

Control: do no capability or assessment work. Score the unchanged base and unchanged frozen-counter tip in an isolated clone, sequentially, with the lane's committed C2 counter and manifest. No control commit was created and no patch was requested or written.

- Base: `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122`.
- Tip / clone checkout: `4f21d9956e8c7a5d9f824ff24b9a4426a3f51949`.
- Clone: `/fast/scratch/hyaku/mado-r24/ctl/CtlC2DoNothing`.
- Expected detector: the frozen counter reports each capability's stated and observed status, then `mismatches=k/12`; C2's target is `mismatches=0` with exit 0. An unchanged control meeting that target would void C2 under registration lines 64–66.
- Mutant: none, by assignment. This is a baseline control, not a killed-mutant claim.
- Tools installed or updated: none.

## Exact setup and scoring commands

Commands ran from `/home/vgpnk/Projects/shokunin` for clone creation and from the clone thereafter. The tip run began only after the base run exited. Git environment overrides were unset. Recursive commands were capped at 4 GiB virtual memory; each counter run had an outer 900-second timeout (and a 30-second kill grace).

```sh
timeout 90 prlimit --as=4294967296 --core=0 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r24/ctl/CtlC2DoNothing
timeout 60 prlimit --as=4294967296 --core=0 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC2DoNothing checkout -q 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949

timeout --kill-after=30s 900s prlimit --as=4294967296 --core=0 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC2DoNothing python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122

timeout --kill-after=30s 900s prlimit --as=4294967296 --core=0 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC2DoNothing python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

Clone and checkout both exited 0 with no output.

## Frozen counter identity

The lane copies' before and after hashes were identical:

- `count.py`: sha256:`a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8`.
- `manifest.json`: sha256:`e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02`.

Each lane copy also matched its committed bytes at the frozen tip, using these exact commands (all exited 0):

```sh
timeout 30 sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/manifest.json
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949:.ufo/waves/round-24/c2/count.py | timeout 30 sha256sum
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949:.ufo/waves/round-24/c2/manifest.json | timeout 30 sha256sum
```

The first command was repeated after both runs. The two `git show` commands were read-only; no lane or fleet git/jj write command ran.

## Base — full counter output

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
mismatches=1/12 revision=8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122 manifest_sha256=e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02 counter_sha256=a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8
```

Counter/timeout exit: **1**. Tool-recorded wall time: **267.50 seconds**. No timeout occurred.

## Tip — full counter output

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

Counter/timeout exit: **1**. Tool-recorded wall time: **257.18 seconds**. No timeout occurred.

## Revision statistics

No new control commit exists. Statistics below describe the two unchanged scored commits, not changes made by this control.

Exact command (exit 0):

```sh
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC2DoNothing show --stat --format=fuller 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

```text
commit 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122
Author:     protocol-shokunin <protocol@shokunin.local>
AuthorDate: Thu Oct 22 09:19:49 2026 -0300
Commit:     protocol-shokunin <protocol@shokunin.local>
CommitDate: Thu Oct 22 09:19:50 2026 -0300

    round-23 verifier spot-check (integrator, hyaku): non-author admit/reject

 corpus/lessons/round-23-verifier-spotcheck.md | 153 ++++++++++++++++++++++++++
 1 file changed, 153 insertions(+)

commit 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
Author:     mado-shokunin <mado@shokunin.local>
AuthorDate: Fri Oct 23 00:31:24 2026 -0300
Commit:     mado-shokunin <mado@shokunin.local>
CommitDate: Fri Oct 23 00:31:24 2026 -0300

    round-24: frozen C2 counter and manifest (before controls); base smoke 1/12 mismatches

 .ufo/waves/round-24/c2/README.md               |  36 +++
 .ufo/waves/round-24/c2/count.py                | 354 +++++++++++++++++++++++++
 .ufo/waves/round-24/c2/manifest.json           | 163 ++++++++++++
 .ufo/waves/round-24/c2/smoke/base-8e5d9369.txt |  15 ++
 4 files changed, 568 insertions(+)
```

## Unchanged-byte and process-cleanup evidence

No source mutation was made, so restoration was not applicable; the control stayed at the frozen tip throughout both runs. The following command ran once during the base run and once after both runs, with identical output and exit 0:

```sh
timeout 30 sha256sum SCORECARD.md tools/mado-verify.sh tools/mado-tripwire.py tools/mado-assessment.py .ufo/waves/round-20/tw-precision.py .ufo/waves/round-20/a2/a2-guards.py
```

```text
1003b79ae3a7ccaad5a062abefa017d014e331cd55c234b232a40d099a7eb5ea  SCORECARD.md
050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1  tools/mado-verify.sh
cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84  tools/mado-tripwire.py
66aefd03f25d834fbfcfee6b295c1c032f01b2a94ca321396b7558cca59de9d4  tools/mado-assessment.py
bd3bdc23747a6d8f195e69528f532988202db4ab3476d141a8ff46871e42a8e7  .ufo/waves/round-20/tw-precision.py
414034d57ad38719df9489201c71fce7cb39edc29a5bf25ab971cbc57a4836ef  .ufo/waves/round-20/a2/a2-guards.py
```

All values in the hash output are sha256 digests. Both counter jobs completed. A cleanup query `timeout 30 pgrep --env MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC2DoNothing -a` exited 2 because this host's pgrep does not support `--env`. The fallback `timeout 30 prlimit --as=4294967296 --core=0 ps eww -eo pid,ppid,pgid,sid,args` exited 0; its output was filtered in the caller for the exact whitespace-delimited environment token `MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC2DoNothing`. It reported `MATCHING_PROCESSES: 0`, so no remaining control process required killing.

## Verdict

C2 before value: **1/12 mismatches**, reproduced at both unchanged base and unchanged tip. The sole mismatch in both runs was `tripwire evidence marker`: stated `works`, observed `fails`, command exit 0. This baseline mismatch is not a killed mutant.

CONTROL_MEETS_TARGET: no
