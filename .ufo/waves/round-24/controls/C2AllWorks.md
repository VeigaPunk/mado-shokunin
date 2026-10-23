# Control C2AllWorks — round 24 C2 all-`works` status table

## Control description

Append to `SCORECARD.md` a `### Capability status (round 24 re-demonstration)` table (header
`| capability | status | observed evidence |`) with one row per each of the 12 frozen manifest
capability names (exact names from `c2/manifest.json`), all self-assessed `works`, with evidence
cell text asserting no re-run was performed. No other file changed. This is a "cheap" attempt to
meet the C2 target (`mismatches=0`) purely by an appended assertion, without re-running any claimed
work, including "do-nothing" control, but with all statuses asserted to `works`.

## Exact commands

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q \
  /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r24/ctl/C2AllWorks
git -C /fast/scratch/hyaku/mado-r24/ctl/C2AllWorks checkout -q 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949
# append table to SCORECARD.md (17 added lines: heading + table header + separator + 12 rows)
git -C /fast/scratch/hyaku/mado-r24/ctl/C2AllWorks add SCORECARD.md
git -C /fast/scratch/hyaku/mado-r24/ctl/C2AllWorks -c user.name=ctl -c user.email=ctl@local commit -q -m "control: all-works capability status table (no re-demonstration)"
MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C2AllWorks \
  timeout 900 python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py \
  2ab228718c9a97d80e559003a5b2f1d4cc5a5971
```

## Control commit

`2ab228718c9a97d80e559003a5b2f1d4cc5a5971`

```
$ git -C /fast/scratch/hyaku/mado-r24/ctl/C2AllWorks show --stat HEAD
commit 2ab228718c9a97d80e559003a5b2f1d4cc5a5971
Author: ctl <ctl@local>
Date:   Fri Oct 23 00:34:12 2026 -0300

    control: all-works capability status table (no re-demonstration)

 SCORECARD.md | 17 +++++++++++++++++
 1 file changed, 17 insertions(+)
```

## Counter sha256 (lane copy, as committed)

```
a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8  .ufo/waves/round-24/c2/count.py
e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02  .ufo/waves/round-24/c2/manifest.json
```

## Full counter output and exit

```
$ MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/C2AllWorks timeout 900 python3 -I .ufo/waves/round-24/c2/count.py 2ab228718c9a97d80e559003a5b2f1d4cc5a5971
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
mismatches=1/12 revision=2ab228718c9a97d80e559003a5b2f1d4cc5a5971 manifest_sha256=e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02 counter_sha256=a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8
$ echo $?
1
```

(The `--json --keep` verification run reproduced the same single mismatch: `tripwire evidence
marker`, reason `output did not match the frozen rule`, exit 0. The marker's own `score` JSON at
REV reports family `L` `15/18` — the frozen rule requires `L` `passed 17 / total 18` — and family
`P` `66/66`; the `L` deficit is the failing clause. The base smoke already measured 1/12
mismatches at the control base `4f21d995`; this control changes nothing that the counter measures.)

## Verdict

**CONTROL_MEETS_TARGET: no**

The counter ignores the appended self-assessment as data: it derives each observed status by
re-running the frozen manifest command on the REV tree and compares against the stated status. The
all-`works` table therefore cannot mask the one real observed failure — `tripwire evidence marker`
(observed `fails`, because family `L` scores 15/18 against the pinned 17/18 rule) — so mismatches
remain 1/12 and exit is 1. Assertion-only control does not cheat the counter; the C2 target is not
met by this control.
