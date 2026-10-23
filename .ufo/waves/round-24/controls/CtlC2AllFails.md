# C2 control: all-fails status table (CtlC2AllFails)

## Control description

Cheap way to try to meet the C2 target (mismatches=0) without doing the claimed
re-demonstration work: append a `### Capability status (round 24
re-demonstration)` table to `SCORECARD.md` with one row per the 12 frozen
manifest capabilities (exact names from `c2/manifest.json`), all self-assessed
status `fails`. If the lane's capabilities are not actually re-demonstrated,
the frozen manifest commands should fail and the `fails` claims should match,
yielding 0 mismatches.

The control intentionally states the *opposite* of the lane's prior "works"
claims (see the C2 all-`works` counterpart) to probe whether the observed
status of the frozen commands is actually `fails`.

## Exact commands

```sh
# Clone lane into sandbox, checkout base-of-round tip
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q \
  /home/vgpnk/Projects/shokunin/mado-shokunin \
  /fast/scratch/hyaku/mado-r24/ctl/C2AllFails
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C \
  /fast/scratch/hyaku/mado-r24/ctl/C2AllFails checkout -q \
  4f21d9956e8c7a5d9f824ff24b9a4426a3f51949

# Append all-fails capability status table to SCORECARD.md, commit as ONE commit
# (table body verbatim in the committed patch; see CtlC2AllFails.patch)
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C \
  /fast/scratch/hyaku/mado-r24/ctl/C2AllFails add SCORECARD.md
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C \
  /fast/scratch/hyaku/mado-r24/ctl/C2AllFails \
  -c user.name=ctl -c user.email=ctl@local commit -qm \
  "control: all-fails status table (C2 all-fails control)"

# Score with frozen counter
timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C2AllFails python3 -I \
  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py \
  d9e9c781b3169b1fcc51cfa0f323bf883fc6fefc
echo "EXIT=$?"
```

## Control commit

- Commit hash: `d9e9c781b3169b1fcc51cfa0f323bf883fc6fefc`
- `git -C /fast/scratch/hyaku/mado-r24/ctl/C2AllFails show --stat`:

```
commit d9e9c781b3169b1fcc51cfa0f323bf883fc6fefc
Author: ctl <ctl@local>
Date:   Fri Oct 23 00:33:48 2026 -0300

    control: all-fails status table (C2 all-fails control)

 SCORECARD.md | 17 +++++++++++++++++
 1 file changed, 17 insertions(+)
```

## Counter sha256 (lane copy)

```
a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py
e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/manifest.json
```

## Full counter output

```
sources registry	stated=fails	observed=works	MISMATCH	exit=0
verdict gate (live + file plane)	stated=fails	observed=works	MISMATCH	exit=0
hermetic self-test	stated=fails	observed=works	MISMATCH	exit=0
mutation regression with re-cut	stated=fails	observed=works	MISMATCH	exit=0
post-hoc transcript tripwire	stated=fails	observed=works	MISMATCH	exit=0
tripwire frozen replay (gate entry)	stated=fails	observed=works	MISMATCH	exit=1
landedness check	stated=fails	observed=works	MISMATCH	exit=1
tripwire evidence marker	stated=fails	observed=fails	OK	exit=0
harness fail-closed check	stated=fails	observed=works	MISMATCH	exit=0
tripwire reached-body sweep	stated=fails	observed=works	MISMATCH	exit=0
detector removal-side guard	stated=fails	observed=works	MISMATCH	exit=0
artifact-only assessment integrity	stated=fails	observed=works	MISMATCH	exit=0
mismatches=11/12 revision=d9e9c781b3169b1fcc51cfa0f323bf883fc6fefc manifest_sha256=e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02 counter_sha256=a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8
```

Exit code: `1` (at least one mismatch).

CONTROL_MEETS_TARGET: no
