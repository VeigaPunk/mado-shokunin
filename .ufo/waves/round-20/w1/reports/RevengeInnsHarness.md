# RevengeInnsHarness — recovered pre-fix script; reproduction is faithful to the fail-open shape

## Findings

**Axes:** evidence fidelity; scope/non-execution. **Confidence:** high for the recovered script and invocation; high for the qualified fidelity judgment.

### First `inns.sh` before the fix

The matching session transcript is `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR19/MadoR19.SentinelGatePath.jsonl`. Its line 34 records the first tool-call writing `/tmp/sgp/inns.sh` (call `toolu_012hy5gXKdzPkCEP4LVxSyGh`, 2026-10-20T18:05:24.012Z); the command also executes it. Recovered script text:

```bash
#!/bin/bash
set -e
for p in /usr/bin/hyprctl /usr/bin/walker /usr/bin/systemctl /usr/bin/waybar /usr/bin/busctl /usr/bin/elephant /usr/bin/notify-send /usr/bin/journalctl /usr/bin/loginctl /usr/bin/uwsm /usr/bin/makoctl /usr/bin/swayosd-client /usr/bin/pacman /usr/bin/sudo /home/vgpnk/.local/share/omarchy/bin/omarchy /home/vgpnk/.local/bin/jj; do
  [ -e "$p" ] && mount --bind /tmp/sgp/tripwire.sh "$p" && echo "armed $p"
done
set +e
"$@"
```

The exact payload invocation in that same tool-call was:

```bash
unshare --user --map-current-user --mount --propagation private /tmp/sgp/inns.sh bash -c 'id -u; head -2 /usr/bin/hyprctl; head -2 /usr/bin/walker; /usr/bin/hyprctl probe; echo rc=$?'
```

The surrounding command had made `/tmp/sgp/inns.sh` executable before this invocation and then ran `cat /tmp/sgp/tripwire.log`. The transcript's line 35 records the command result; the contemporaneous SentinelGatePath report states that each mount failed with “must be superuser to use mount,” followed by the real `hyprctl probe` returning `unknown request`, `rc=0` (`.ufo/waves/round-19/w2/reports/SentinelGatePath.md:77-79`).

### Is `inns-r19-shape.sh` faithful?

**Yes, to the vulnerable fail-open control-flow shape; no, not as a byte-for-byte or environmental replay.** Its lines 37-54 retain `set -e`, the same `[ -e "$p" ] && mount --bind ... && echo "armed $p"` conditional list, and then proceed to `exec "$@"` without a fail-closed check. Thus a failed `mount` can leave the list without triggering `errexit` and still reach the payload, matching the defect in the recovered script. The separate recorded safe reproduction used an injected mount failure (exit 32), reported `harness exit: 0` and `FAIL_OPEN` (`/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/87470.bash.log:1-6`).

It deliberately changes the namespace flag from historical `--map-current-user` to `--map-root-user`, parameterizes stub/targets, and forces mount failure through a controlled stub rather than relying on the original permission mismatch; its payload is a `/tmp` canary rather than a host binary. Those differences mean it reproduces the failure mechanism safely, not the original host-specific setup. Candidate source: `.ufo/waves/round-20/evidence/inns-r19-shape.sh:37-55`; its author's report independently describes the same qualification at `.ufo/waves/round-20/w1/reports/IsolationHarness.md:7,11`.

I only read the transcript, candidate file, and cited reports/log. I did not execute either script or any command from the transcript.

## Limits

- No historical `/tmp/sgp` filesystem snapshot or script-byte hash was available; recovery is from the recorded tool-call command text.
- I did not independently rerun the candidate's canary test or measure whether the original probe changed host state.

## Installs

none
