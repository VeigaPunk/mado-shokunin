# RevHostGuard — host-state guard review

## Verdict
The round-49 draft demonstration passes its declared fake-home behaviors when relocated to this round's scratch: the HOME-based mutant was caught unsandboxed (exit 3), contained by masking (exit 0), and the other declared cases all returned their expected status. Frozen counters explicitly isolate HOME/XDG state in scratch. No actionable defect found in this scope.

## Evidence
- `demo.sh` lines 4–16 describe the fake-home-only demonstration and expected cases; lines 23–35 set up fakehome/cache and trap scratch cleanup; lines 51–66 write only `$HOME/.cache/xdg-terminal-exec`.
- Executed the copied draft under `/fast/scratch/hyaku/mado-r50/RevHostGuard/` after relocating its scratch/receipt paths. Output: `caseA_exit=3`, `caseA2_exit=3`, `caseB_exit=0`, `caseB2_exit=0`, `caseC_exit=0`, `caseC2_exit=0`, `caseG_exit=3`, `caseH1_exit=0 caseH2_exit=0`, `caseI1_exit=3`, `caseI2_exit=0`. The driver completed and its EXIT trap removed the scratch tree. Case A is the requested unsandboxed fake HOME write; B is masked containment.
- Draft `hostguard.py` lines 4–27 documents the guard's digest-before/after contract, redirected HOME/XDG/TMPDIR, real-home refusals, mask semantics, and bwrap behavior. Its statement is observational (no change observed), not proof of causality (lines 10–13).
- `quality/counters/c1-r49-keysym.py` lines 27–31 specifies HOME and XDG_CONFIG_HOME under `--work` for judge runs; lines 41–53 require strace+bwrap and prohibit post-start writes except the selftest's fresh `/tmp` tmpfs; lines 55–72 document fresh-root bwrap isolation and in-sandbox HOME=/nonexistent.
- `quality/counters/c2-r49-bind-entry.py` lines 117–128 requires scratch TMPDIR (refuses `/tmp`) and lines 119–123 run hyprctl with scratch HOME/XDG_* while inheriting only compositor socket route variables; lines 1043–1053 construct those scratch dirs.

## Residual risk / verification gaps
This was the round-49 draft and demo, not an installed/frozen round-50 guard or a mutation of either counter. The demo exercises a small fake home only; it does not establish that all possible hardcoded paths or concurrent writes are contained. C2 intentionally inherits XDG_RUNTIME_DIR and HYPRLAND_INSTANCE_SIGNATURE for read-only compositor access. No live host-state probe was run.