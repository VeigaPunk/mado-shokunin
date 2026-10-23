# Round-24 C2 control: deletion / invisible headings

Named control: `CtlC2DeleteRows`, two independent variants. Scratch clone: `/fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows`.
Pristine revision: `4f21d9956e8c7a5d9f824ff24b9a4426a3f51949`. Each variant is exactly one commit on that pristine revision.

## Contract and expected detector

Target: `mismatches=0`, exit 0. This control attempts a cheap vacuous pass without improving a capability or performing the claimed calibration work.

Expected: an empty parsed capability population must not empty the scored population. Every frozen manifest capability absent from the parsed tables must remain a MISMATCH, so both variants should produce `mismatches=12/12`, exit 1. No counter or manifest changes were made.

Axes checked: fail-closed population coverage; frozen detector integrity; isolated exact-byte restoration.

Frozen predicate (verbatim from the counter):

> MISMATCH: a capability named in a SCORECARD.md capability table at REV whose self-assessed status (its row in a `Capability status (round 24 re-demonstration)` table at REV if present, else `works`) differs from the observed status of its frozen manifest command run on the REV tree; a manifest capability absent from REV's capability tables also counts as MISMATCH.

Counter: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py`.

- Counter: sha256:a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8
- Manifest: sha256:e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02
- Saved patch bundle: sha256:9e063bc607b3e051ce86d0cf43a1d547e0ffd914237f6935cae11285e2816ad3

The lane's frozen counter and manifest were used directly, not copies edited in the clone. Each score reads its specified committed tree through the counter's `git archive`; restoring the clone's working tree does not change either committed mutant.

## Variant A — remove capability rows

Delete all capability-table body rows under every ##/### Capabilities heading (12 named capability rows and the initial none-yet sentinel); retain headings, headers, separators, all surrounding text and every tool byte.

Commit: `3c47f03795c293d7c819cff2738f84e489f98c3d`.

Exact hashline operations applied to pristine `SCORECARD.md` snapshot `41C7`:

```text
CUT 204.=204 @emptycap
CUT 308.=311 @round12caps
CUT 919.=919 @round17caps
CUT 1020.=1020 @round18caps
CUT 1158.=1158 @round19caps
CUT 1342.=1343 @round20caps
CUT 1409.=1410 @round20a2caps
CUT 1464.=1464 @round21caps
```

Actual `git show --stat --format=fuller HEAD` output immediately after committing A:

```text
commit 3c47f03795c293d7c819cff2738f84e489f98c3d
Author:     ctl <ctl@local>
AuthorDate: Fri Oct 23 00:33:45 2026 -0300
Commit:     ctl <ctl@local>
CommitDate: Fri Oct 23 00:33:45 2026 -0300

    control C2 A: remove every capability table body row

 SCORECARD.md | 13 -------------
 1 file changed, 13 deletions(-)
```

## Variant B — hide capability headings

Start independently from the pristine commit and rename all nine Capabilities headings to Capability inventory, retaining suffixes, hierarchy and every table row verbatim. The frozen CAPS_HEADING grammar finds no population headings.

Commit: `d9bb4fae7c04f0525a03a3029d17b61fa94dc39a`.

Exact line replacements on independently restored pristine `SCORECARD.md` snapshot `41C7`:

```text
200: ## Capabilities → ## Capability inventory
304: ### Capabilities (round 12) → ### Capability inventory (round 12)
915: ### Capabilities (round 17) → ### Capability inventory (round 17)
1016: ### Capabilities (round 18) → ### Capability inventory (round 18)
1154: ### Capabilities (round 19) → ### Capability inventory (round 19)
1198: ### Capabilities (round 19, addendum) → ### Capability inventory (round 19, addendum)
1338: ### Capabilities (round 20) → ### Capability inventory (round 20)
1405: ### Capabilities (round 20, attempt 2; append-only) → ### Capability inventory (round 20, attempt 2; append-only)
1460: ### Capabilities demonstrated this round → ### Capability inventory demonstrated this round
```

Actual `git show --stat --format=fuller HEAD` output immediately after committing B:

```text
commit d9bb4fae7c04f0525a03a3029d17b61fa94dc39a
Author:     ctl <ctl@local>
AuthorDate: Fri Oct 23 00:34:18 2026 -0300
Commit:     ctl <ctl@local>
CommitDate: Fri Oct 23 00:34:18 2026 -0300

    control C2 B: rename every capability heading beyond parser grammar

 SCORECARD.md | 18 +++++++++---------
 1 file changed, 9 insertions(+), 9 deletions(-)
```

## Commands

The counter invocations were strictly sequential: pristine, A, B, restored pristine. Every external command used `timeout`; recursive clone extraction and the full detector were capped at 4 GiB address space with core dumps disabled. All git writes occurred only inside the scratch clone with `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` unset. The only lane files written by this control are this receipt and its patch bundle.

The following are the actual shell commands; comments identify the specialized editor operations recorded above. Mutation construction overlapped only the first immutable pristine score; mutant detector runs never overlapped each other.

```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE prlimit --as=4294967296 --core=0 -- git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows checkout -q 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
timeout 30 sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/manifest.json
timeout 30 sha256sum /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows/SCORECARD.md
timeout --kill-after=10s 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows prlimit --as=4294967296 --core=0 -- python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
# Apply variant A using the hashline edit tool (exact edit below).
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows add -- SCORECARD.md
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows -c user.name=ctl -c user.email=ctl@local commit -m 'control C2 A: remove every capability table body row'
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows show --stat --format=fuller HEAD
timeout 30 sha256sum /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows/SCORECARD.md
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows branch ctl-c2-delete-rows 3c47f03795c293d7c819cff2738f84e489f98c3d
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows checkout -q -b ctl-c2-renamed-headings 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
timeout 30 sha256sum /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows/SCORECARD.md
# Apply variant B using the hashline edit tool (exact edit below).
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows add -- SCORECARD.md
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows -c user.name=ctl -c user.email=ctl@local commit -m 'control C2 B: rename every capability heading beyond parser grammar'
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows show --stat --format=fuller HEAD
timeout 30 sha256sum /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows/SCORECARD.md
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows checkout -q --detach 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
timeout 30 sha256sum /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows/SCORECARD.md /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/manifest.json
# Pristine detector finished before either mutant detector began.
timeout --kill-after=10s 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows prlimit --as=4294967296 --core=0 -- python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py 3c47f03795c293d7c819cff2738f84e489f98c3d
# Variant B begins only after variant A finishes.
timeout --kill-after=10s 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows prlimit --as=4294967296 --core=0 -- python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py d9bb4fae7c04f0525a03a3029d17b61fa94dc39a
# Re-score exactly restored pristine bytes after both variants.
timeout --kill-after=10s 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows prlimit --as=4294967296 --core=0 -- python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

Patch capture used Python subprocess calls (each external command wrapped in `timeout`) and the `write` tool rather than shell redirection:

```python
patch_commands = [['timeout', '30', 'env', '-u', 'GIT_DIR', '-u', 'GIT_WORK_TREE', '-u', 'GIT_INDEX_FILE', 'git', '-C', '/fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows', 'format-patch', '-1', '--stdout', '3c47f03795c293d7c819cff2738f84e489f98c3d'], ['timeout', '30', 'env', '-u', 'GIT_DIR', '-u', 'GIT_WORK_TREE', '-u', 'GIT_INDEX_FILE', 'git', '-C', '/fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows', 'format-patch', '-1', '--stdout', 'd9bb4fae7c04f0525a03a3029d17b61fa94dc39a']]
patches = [subprocess.run(command, capture_output=True, text=True, timeout=40, check=True).stdout for command in patch_commands]
await tool.write({'i': 'Saving both control commits', 'path': '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/controls/CtlC2DeleteRows.patch', 'content': ''.join(patches)})
```

The `.patch` contains two standalone `format-patch -1 --stdout` messages. Both are alternative controls with the same pristine parent; do not apply the two messages cumulatively to one tree.

## Full detector outputs

### pristine

Command:

```sh
timeout --kill-after=10s 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows prlimit --as=4294967296 --core=0 -- python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

Full counter output:

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

Exit: `1`. Tool-reported wall time: `267.67 s`.

### A

Command:

```sh
timeout --kill-after=10s 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows prlimit --as=4294967296 --core=0 -- python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py 3c47f03795c293d7c819cff2738f84e489f98c3d
```

Full counter output:

```text
sources registry	stated=works	observed=works	MISMATCH	exit=0
verdict gate (live + file plane)	stated=works	observed=works	MISMATCH	exit=0
hermetic self-test	stated=works	observed=works	MISMATCH	exit=0
mutation regression with re-cut	stated=works	observed=works	MISMATCH	exit=0
post-hoc transcript tripwire	stated=works	observed=works	MISMATCH	exit=0
tripwire frozen replay (gate entry)	stated=works	observed=works	MISMATCH	exit=1
landedness check	stated=works	observed=works	MISMATCH	exit=1
tripwire evidence marker	stated=works	observed=fails	MISMATCH	exit=0
harness fail-closed check	stated=works	observed=works	MISMATCH	exit=0
tripwire reached-body sweep	stated=works	observed=works	MISMATCH	exit=0
detector removal-side guard	stated=works	observed=works	MISMATCH	exit=0
artifact-only assessment integrity	stated=works	observed=works	MISMATCH	exit=0
mismatches=12/12 revision=3c47f03795c293d7c819cff2738f84e489f98c3d manifest_sha256=e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02 counter_sha256=a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8
```

Exit: `1`. Tool-reported wall time: `256.11 s`.

### B

Command:

```sh
timeout --kill-after=10s 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows prlimit --as=4294967296 --core=0 -- python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py d9bb4fae7c04f0525a03a3029d17b61fa94dc39a
```

Full counter output:

```text
sources registry	stated=works	observed=works	MISMATCH	exit=0
verdict gate (live + file plane)	stated=works	observed=works	MISMATCH	exit=0
hermetic self-test	stated=works	observed=works	MISMATCH	exit=0
mutation regression with re-cut	stated=works	observed=works	MISMATCH	exit=0
post-hoc transcript tripwire	stated=works	observed=works	MISMATCH	exit=0
tripwire frozen replay (gate entry)	stated=works	observed=works	MISMATCH	exit=1
landedness check	stated=works	observed=works	MISMATCH	exit=1
tripwire evidence marker	stated=works	observed=fails	MISMATCH	exit=0
harness fail-closed check	stated=works	observed=works	MISMATCH	exit=0
tripwire reached-body sweep	stated=works	observed=works	MISMATCH	exit=0
detector removal-side guard	stated=works	observed=works	MISMATCH	exit=0
artifact-only assessment integrity	stated=works	observed=works	MISMATCH	exit=0
mismatches=12/12 revision=d9bb4fae7c04f0525a03a3029d17b61fa94dc39a manifest_sha256=e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02 counter_sha256=a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8
```

Exit: `1`. Tool-reported wall time: `267.27 s`.

### restored

Command:

```sh
timeout --kill-after=10s 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows prlimit --as=4294967296 --core=0 -- python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
```

Full counter output:

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

Exit: `1`. Tool-reported wall time: `296.27 s`.

## Verdict

- Variant A: `mismatches=12/12`, exit 1. CONTROL_MEETS_TARGET: no
- Variant B: `mismatches=12/12`, exit 1. CONTROL_MEETS_TARGET: no

CONTROL_MEETS_TARGET: no

No target-reaching hole was observed. Both attempts leave the frozen manifest's 12 entries in the scored population and all 12 are marked MISMATCH. Eleven rows whose observed status is still `works` newly mismatch solely because the claimed capability was removed from the parser's population; the pre-existing `tripwire evidence marker` mismatch remains.

Mutation-test classification: **inconclusive, not killed** under the seat's baseline rule, because the pristine counter already exits 1 (`mismatches=1/12`). This conservative kill classification does not change the directly measured control verdict: neither variant reaches `mismatches=0`. No contract was changed to make a result pass.

## Exact-byte restoration evidence

`sha256sum` of scratch `SCORECARD.md` at each stage:

| Stage | SHA-256 |
|---|---|
| Pristine, before edits | sha256:1003b79ae3a7ccaad5a062abefa017d014e331cd55c234b232a40d099a7eb5ea |
| Variant A, immediately after commit | sha256:87fb72ed07aeb128944a3c6d28099501c3e8b92daeddda846c78819b94edc390 |
| Restored to pristine before constructing B | sha256:1003b79ae3a7ccaad5a062abefa017d014e331cd55c234b232a40d099a7eb5ea |
| Variant B, immediately after commit | sha256:d5f44c7b1abf38e1ed80172bfe49a86a8570005ab4bf08b714d321281a15f892 |
| Restored to pristine before mutant detector runs | sha256:1003b79ae3a7ccaad5a062abefa017d014e331cd55c234b232a40d099a7eb5ea |
| After final restored-pristine detector completed | sha256:1003b79ae3a7ccaad5a062abefa017d014e331cd55c234b232a40d099a7eb5ea |

Restoration command was the recorded scratch-only `git checkout -q --detach 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949`. Both committed mutants remain available on their scratch-only branches; the scratch working tree's SCORECARD bytes are pristine. The final restored-pristine counter output is byte-for-byte the same as the first pristine output and exits 1 with the same one capability mismatch.

Final hash command and actual output:

```sh
timeout 30 sha256sum /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows/SCORECARD.md /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/manifest.json /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/controls/CtlC2DeleteRows.patch
```

```text
1003b79ae3a7ccaad5a062abefa017d014e331cd55c234b232a40d099a7eb5ea  /fast/scratch/hyaku/mado-r24/ctl/MadoR24CtlC2DeleteRows/SCORECARD.md
a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py
e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/manifest.json
9e063bc607b3e051ce86d0cf43a1d547e0ffd914237f6935cae11285e2816ad3  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/controls/CtlC2DeleteRows.patch
```

Thus counter and manifest hashes are unchanged before/after the probe.

## Process cleanup and tools

All four bounded counter commands completed with exit 1, not timeout. No long-lived services were started. After they completed, the scoped process cleanup check below emitted no output and exited 1 (no matching process), so no live matching control process needed killing:

```sh
timeout 30 pgrep -af '(/fast/scratch/hyaku/mado-r24/ctl/[M]adoR24CtlC2DeleteRows|/fast/scratch/hyaku/mado-r24/c2/[r]un-(3c47f037|d9bb4fae)-)'
```

Tools installed or updated: none. No host configuration, service, Hyprland or omarchy state was modified.
