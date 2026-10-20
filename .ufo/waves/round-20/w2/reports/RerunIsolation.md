# RerunIsolation — partly falsified: fail-closed repair passes, but one committed control is not directly runnable

## Findings

- **P2 — The committed legacy control cannot be evaluated from a clean checkout without an undocumented mode change.** At `a4046a8216080d4004de3f268c62cf142095ac07`, `git ls-tree` reports `.ufo/waves/round-20/evidence/inns-r19-shape.sh` as mode `100644`; `isolation-check.sh:11-13` rejects any harness lacking execute permission. Running the copied committed file directly therefore returned `COULD_NOT_EVALUATE inns-r19-shape.sh (not executable)` (exit 2), rather than testing it. I added execute permission only to the `/tmp` clone and reran the same committed bytes; the resulting five fail-open cases and one fail-closed case match the stored transcript. This leaves the prescribed clean-checkout command unreproducible for this control without a scratch-tree preparation step.
  - Evidence: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-tree a4046a8216080d4004de3f268c62cf142095ac07 .ufo/waves/round-20/evidence/inns-r19-shape.sh` → `100644 blob 26f037748f7b37012bec56579bb9ecad258edca6`.
  - Failed direct invocation: `bash /tmp/mado-r20w2-RerunIsolation/.ufo/waves/round-20/isolation-check.sh /tmp/mado-r20w2-RerunIsolation/.ufo/waves/round-20/evidence/inns-r19-shape.sh` → `COULD_NOT_EVALUATE inns-r19-shape.sh (not executable)`, exit 2.
  - After `chmod +x` on that `/tmp` copy only: `bash /tmp/mado-r20w2-RerunIsolation/.ufo/waves/round-20/isolation-check.sh /tmp/mado-r20w2-RerunIsolation/.ufo/waves/round-20/evidence/inns-r19-shape.sh` → `FAIL_OPEN` for `mount-nonzero`, `mount-noop`, `partial-arm`, `missing-target`, `missing-stub`; `FAIL_CLOSED` for `unshare-refused`; positive control passed; exit 1.

- **P3 — The combined saved receipt is not revision-bound.** `.ufo/waves/round-20/evidence/isolation-check-run.txt:1` still says `measured_commit=PENDING`. The rerun below observed the result at clone `HEAD=a4046a8216080d4004de3f268c62cf142095ac07`, but the committed transcript itself does not identify the commit it measured.

## Rerun results and comparison

Copied the named committed source bytes into `/tmp/mado-r20w2-RerunIsolation` and confirmed the clone's `HEAD` was `a4046a8216080d4004de3f268c62cf142095ac07`. Each test was run as `bash /tmp/mado-r20w2-RerunIsolation/.ufo/waves/round-20/isolation-check.sh /tmp/mado-r20w2-RerunIsolation/<harness>`; only the legacy control needed the scratch-only execute-bit adjustment described above.

| Harness | Observed result | Comparison |
|---|---|---|
| `.ufo/waves/round-20/isolate.sh` | All six setup failures were `FAIL_CLOSED` with canary absent; positive control wrote canary; exit 0. | Matches `.ufo/waves/round-20/evidence/crit29-isolate.txt:3-57` and `isolation-check-run.txt:3-60`. |
| `evidence/inns-r19-shape.sh` | Five `FAIL_OPEN` results and one `FAIL_CLOSED` (`unshare-refused`); positive control passed; exit 1 after scratch chmod. | Matches `crit29-inns-r19-shape.txt:3-57` and `isolation-check-run.txt:62-120`. |
| `evidence/isolation-mutants/m1-nocmp.sh` | `mount-noop` was `FAIL_OPEN`; other setup failures were closed; positive control passed; exit 1. | Matches `isolation-check-run.txt:122-179`. |
| `evidence/isolation-mutants/m3b-capprobe.sh` | `unshare-refused` was `FAIL_OPEN`; other setup failures were closed; positive control passed; exit 1. | Matches `isolation-check-run.txt:181-238`. |
| `evidence/isolation-mutants/m4-skiptarget.sh` | `missing-target` was `FAIL_OPEN`; other setup failures were closed; positive control passed; exit 1. | Matches `isolation-check-run.txt:299-354`. |
| `evidence/isolation-mutants/m6-besteffort.sh` | `partial-arm` was `FAIL_OPEN`; other setup failures were closed; positive control passed; exit 1. | Matches `isolation-check-run.txt:240-297`. |

Representative outputs from this rerun: baseline `harness exit: 125; canary=absent` followed by `FAIL_CLOSED isolate.sh mode=partial-arm`; `m3b-capprobe.sh` on unshare refusal `harness exit: 0; canary=present` followed by `FAIL_OPEN`; `m4-skiptarget.sh` on missing target `harness exit: 0; canary=present` followed by `FAIL_OPEN`; and `m6-besteffort.sh` on partial arm `harness exit: 0; canary=present` followed by `FAIL_OPEN`.

SHA-256 of the copied inputs:

- `isolation-check.sh`: `2bf115db1658df32d5e89e600ad6ef47c0e2855beda5f25dfc936270604f6aa9`
- `isolate.sh`: `332b3fed6ad680f0bd2eec35ff686b768e2619a828925f13d429807a817fcccc`
- `inns-r19-shape.sh`: `8bd507f0ea39d4d876359a0f5a1f798e810cda3c59293487af35d3a8df37ce9c`
- `m1-nocmp.sh`: `2f2cc63bdb4903a42d99bf5685acc12e5b221158610217e42b0c1ee3d85df359`
- `m3b-capprobe.sh`: `a6dde1c30355b29917091f0045b51befcefc7fc78d0903c098fc880ff9099727`
- `m4-skiptarget.sh`: `a9bfa1be563c76e74edffa480514e69f3ee85ead8415e54b865d02be10107940`
- `m6-besteffort.sh`: `ac11cc5adb1ece61eba4d45a8e2b65016576eb247957a846afe797b9118c6ed4`

## Limits

- This run demonstrates the specified canary behavior for injected setup failures, missing paths, and a positive control. It does not establish that `isolate.sh` is a general-purpose sandbox or that the host environment is isolated.
- The only permission change was `chmod +x` on the legacy-control copy under `/tmp`; the lane checkout was not modified. The control's byte hash remained the committed hash above.
- No `lsp` device/server was exposed in the available tool inventory; no cross-reference or diagnostics claims are made.

## Installs

None.
