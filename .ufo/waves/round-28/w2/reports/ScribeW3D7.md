# ScribeW3D7 — C2 D7 w3 seat reconciliation

## Axis and result
C2 calibration, defect D7 (literal w3 seat-count reconciliation). Declared 8 seats; 7 reports found; delta is 1 unreported seat. The evidence file contains the required exact summary tokens. The eighth seat's identity is unknown; none is inferred.

## Basis and findings
The round-27 report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-27/mado.md:120-121` says “attempt 2 — w3 residual 8 seats (in-tree)”; lines 124-125 give the slot grant `granted lane=mado wave=w3 seats=8`.

The seven report headers/seat labels are:
- `CritC1Claim.md` — Crit / critic (`CritC1Claim`, header line 1).
- `CritC2Claim.md` — Crit / critic (`CritC2Claim`, header line 1).
- `ExecWsToolC.md` — Exec / executor (`MadoR27.ExecWsToolC`, header lines 3-6 call these executor seats).
- `MutWsTool.md` — Mut / mutation tester (`MadoR27.MutWsTool`, header lines 1-4 describe the mutation check assignment).
- `RevProvenance.md` — Rev / reviewer (`MadoR27.RevProvenance`, header line 3).
- `RevSourcesFinal.md` — Rev / reviewer (`MadoR27.RevSourcesFinal`, header line 3).
- `RevSpotcheckDebt.md` — Rev / reviewer (`MadoR27.RevSpotcheckDebt`, header line 3).

The tracked and live w3 directory inventory contains only those seven reports; the w3 directory contains only `reports/`. The tracked round-27 wave-root spec/run files are w1 and w2 only. Their run records identify `mado-r27-w1` and `mado-r27-w2`, respectively. The round report carries only the aggregate 8-seat grant, not an individual seat list. There is no w3 spec/registry file, registry row, or committed per-seat w3 dispatch/run record; therefore the unmatched seat has no evidenced identity.

## Commands and outcomes
All commands below ran read-only and exited 0. Output lines are verbatim, with directory metadata omitted where it is not relevant.

1. `git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-files .ufo/waves/round-27/w3` — exit 0:
```text
.ufo/waves/round-27/w3/reports/CritC1Claim.md
.ufo/waves/round-27/w3/reports/CritC2Claim.md
.ufo/waves/round-27/w3/reports/ExecWsToolC.md
.ufo/waves/round-27/w3/reports/MutWsTool.md
.ufo/waves/round-27/w3/reports/RevProvenance.md
.ufo/waves/round-27/w3/reports/RevSourcesFinal.md
.ufo/waves/round-27/w3/reports/RevSpotcheckDebt.md
```
2. `ls -1 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/w3/reports` — exit 0; output:
```text
CritC1Claim.md
CritC2Claim.md
ExecWsToolC.md
MutWsTool.md
RevProvenance.md
RevSourcesFinal.md
RevSpotcheckDebt.md
```
3. `git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-files '.ufo/waves/round-27/*-spec.json' '.ufo/waves/round-27/*-run.json'` — exit 0:
```text
.ufo/waves/round-27/w1-run.json
.ufo/waves/round-27/w1-spec.json
.ufo/waves/round-27/w2-run.json
.ufo/waves/round-27/w2-spec.json
```
4. `ls -1 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/w3` — exit 0:
```text
reports
```
5. `ls -la /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/w3` — exit 0; relevant output:
```text
reports
```
6. `ls -la /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/w3/reports` — exit 0; entries:
```text
CritC1Claim.md
CritC2Claim.md
ExecWsToolC.md
MutWsTool.md
RevProvenance.md
RevSourcesFinal.md
RevSpotcheckDebt.md
```

## Gates, scope, and limits
- D7 literal evidence: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/evidence/w3-seats-reconciliation.txt`.
- This report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/w2/reports/ScribeW3D7.md`.
- Only those two round-28 files were written. No round-27 record, registration, counter, or dispatch artifact was edited; no git/jj mutation was run.
- No counter, test, build, or other runtime gate was run. No tool was installed or updated.
- One edit call supplied a duplicated lane path; the hashline tool warned the literal path did not exist, matched by filename and snapshot tag to the intended absolute files, and returned the applied edits. No edit failed.
- No failed check or dead end. The absent identity is a limit of the documentary evidence, not a guessed seat assignment.
