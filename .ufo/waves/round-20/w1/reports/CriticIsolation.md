# CriticIsolation — PATH-stub `mount` is adequate for the EPERM mode, but the check exercises only ONE failure mode and demonstrably passes fail-open harnesses green

Scope: attack QUALITY 29's runnable check (`.ufo/waves/round-20/isolation-check.sh`, sha `9937310f…` per IsolationHarness.md) against real failure modes: unshare refused, bind EPERM, cmp mismatch, stub missing. All runs were canary writes into `/tmp/critiso-mut/` only; no host binary, service, or compositor call was made; `unshare`/`mount` ran only inside fresh user+mount namespaces with `/tmp` files (same scope IsolationHarness and ScoutUnshareHost already exercised).

## What the shipped check does today

`isolation-check.sh:26-31` writes one PATH-first `mount` stub that exits 32; `:46-51` runs the harness once under `PATH=$tmp/fail-bin:$PATH`; `:59-67` verdicts FAIL_OPEN (canary exists) / FAIL_CLOSED (nonzero harness exit, no canary) / COULD_NOT_EVALUATE; `:70-94` positive control with real mount. Reproduced:

- `isolate.sh` → FAIL_CLOSED (harness exit 125) + POSITIVE_CONTROL_OK, check exit 0.
- `evidence/inns-r19-shape.sh` → FAIL_OPEN (harness exit 0, canary written), check exit 1. Red demonstrated — and the red is faithful to the incident mechanism: the reconstruction keeps `set -e`, yet the payload still ran because the failing `mount` is a non-final element of the `&&` list (observed in my run; ScoutUnshareHost.md reproduced the same on the real binary; `SentinelGatePath.md:77`).

## Q: PATH-stub `mount` vs real EPERM — adequate proxy?

Adequate **for the mode it tests**. ScoutUnshareHost observed on this host that `--map-current-user` produces the real EPERM: `mount: …: must be superuser to use mount.`, **mount exit 32** — the stub reproduces exactly the contract-relevant signal (nonzero exit, stderr). The fail-open mechanism (`[ -e ] && mount && echo` not tripping `set -e`) is insensitive to *who* returns 32, so the stub red is a faithful stand-in. Two residual fidelity gaps, both minor: a harness that keys on the literal "must be superuser" stderr text would see different text [hypothetical], and the stub never tests mount-absent (exit 127).

The check's defect is not the injection's fidelity — it is **coverage**: exactly one mode is exercised, and each untested mode has a demonstrated fail-open harness the check passes green.

## Counterexamples (all observed, all mutants under /tmp/critiso-mut/)

1. **MUST — exit-0-no-bind (cmp-verification is dead code to the check).** `m1-nocmp.sh` = `isolate.sh` minus the `cmp -s` loop (`isolate.sh:60-62`). Shipped check: FAIL_CLOSED + POSITIVE_CONTROL_OK → **green**. Under a PATH stub `mount` that exits 0 *without* binding: `exit=0, canary=PAYLOAD-RAN`, target left with real bytes — the payload ran against an unstubbed target. The check never exercises the harness's second half (post-mount verification), so deleting `cmp` changes nothing. This also covers "mounted but wrong content" and "mount is a silent no-op".
2. **MUST — unshare refused.** `m3b-capprobe.sh` aborts correctly on inner mount failure and on missing `cmp`, but degrades (`namespaces unavailable; running unisolated`) only when `unshare` itself fails. Shipped check: FAIL_CLOSED → **green**. Under a PATH stub `unshare` exiting 1 (`Operation not permitted`, the kernel-denial shape): `exit=0, canary=PAYLOAD-RAN` — payload ran **outside any namespace**. This is a real mode: `max_user_namespaces`, seccomp, or AppArmor can refuse userns on other hosts (host-dependent per ScoutUnshareHost.md).
3. **MUST — partial arm (multi-target, selective failure).** `m6-besteffort.sh` aborts only if *zero* targets arm. Shipped check (all mounts fail): FAIL_CLOSED → **green**. With two targets and a mount stub failing only for `*t2*` (exit 32): `exit=0, canary=PAYLOAD-RAN` with only t1 armed — the exact continue-on-failure-inside-the-loop class from R19, invisible to a single-target, all-fail injection. `isolate.sh` itself aborts correctly in this scenario (exit 125, no canary).
4. **SHOULD — missing target.** `m4-skiptarget.sh` (`[ -e "$t" ] || continue`): shipped check → **green** (its target always exists). With a nonexistent `--target`: `exit=0, canary=PAYLOAD-RAN`, zero arms. `isolate.sh` fails closed here (mount: "mount point does not exist", exit 125). Whether a skipped missing target is a "setup failure" is contract-dependent, but the R19 harness skipped on exactly `[ -e ]` — same class.
5. **SHOULD — missing stub path.** `--stub /nonexistent` never occurs in the check (it always creates the stub). `isolate.sh` aborts 125 via mount failure; `inns-r19-shape.sh` shape would fail open. Cheap variant of mode 1 but a different trigger (caller error, not EPERM).
6. **Defect — injection is not attested, FAIL_OPEN conflates "payload ran" with "stub never invoked".** `m2-absmount.sh` = `isolate.sh` with `/usr/bin/mount` instead of `command mount` (correct `|| exit 125` + `cmp` logic). Shipped check: **FAIL_OPEN** — but the harness is not fail-open; the failure was simply never injected (absolute path bypassed the stub). A real harness may reasonably use absolute paths; the verdict should be COULD_NOT_EVALUATE. Fix: the stub writes a marker file; canary present + marker absent → "injection did not reach the harness" → exit 2.
7. **Minor — `NEVER_RUNS` exits 1, same as FAIL_OPEN.** On a host where unshare is refused the positive control cannot run; the criterion then *fails* rather than reporting unevaluable. Should be exit 2.
8. **Minor — `unset -f mount` (`:22`) covers one bypass;** if `unshare`/`cmp` stubs are added they need the same `unset -f`, and a harness keying on `command -p` or absolute paths re-triggers finding 6.

## Which modes must be in the check

Minimum set to make "fails closed" a demonstrated property rather than a single datapoint — all are the same stub-dir pattern, ~30 lines:

| mode | injection | verdict if canary |
|---|---|---|
| mount nonzero (EPERM) | have (exit 32) | FAIL_OPEN — covered |
| unshare refused | PATH stub `unshare` exit 1 | FAIL_OPEN — **missing (must)** |
| mount exit-0-no-bind | PATH stub `mount` exit 0 | FAIL_OPEN — **missing (must)** |
| partial arm | 2 targets, stub fails on named mount-point only | FAIL_OPEN — **missing (must)** |
| missing target | `--target` a nonexistent path | harness must exit nonzero or skip-and-refuse — recommended |
| missing stub | `--stub` a nonexistent path | recommended |
| injection attestation | stub drops marker; marker absent ⇒ COULD_NOT_EVALUATE | fixes finding 6 |

Also note the current check never exercises repeated `--target` at all — the harness signature advertises it (`isolate.sh:20-23`), and mode 4 is exactly where per-target gating bugs live.

## Fidelity note on the red artifact (informational)

`inns-r19-shape.sh:37` uses `--map-root-user`; the incident used `--map-current-user` (`RevengeInnsHarness.md:24,33`). Correct choice — it makes the positive control exercisable and confines failure injection to the stub — and the IsolationHarness report discloses it. Because `--map-current-user` produces the EPERM *naturally* on this host (ScoutUnshareHost.md, mount exit 32), an alternate red variant using `--map-current-user` with no PATH stub would demonstrate fail-open against the *real* failure, not an injected one. Optional; the stubbed red is already valid.

## Impact

C2 criterion 29's check is real and correctly discriminates the two shipped harnesses (red on the R19 shape, green on `isolate.sh`), but it certifies only one failure mode. Three distinct fail-open classes — unshare refusal, verification-omission (mount exit-0-no-bind), and partial arm — each have a demonstrated harness that passes the check green while running the payload unprotected under the real failure. The smallest safe correction is the three "must" arms plus the injection marker (finding 6) and exit-2 for NEVER_RUNS (finding 7). This is a fixable defect, not a tradeoff the judge must reject.

## Limits

- Did not test: mount-absent (exit 127) mode, `cmp` stub mode, exported `BASH_FUNC_*`/BASH_ENV bypasses beyond `unset -f mount`, target-is-symlink or target-is-directory shapes (`isolate.sh` refuses dir targets via `cmp` failure — conservative, good), payload exit-125 indistinguishability from setup-125 (inherent to the reserved code; the ready marker only records that the payload ran).
- Mutants are plausible bug shapes I authored; none were claimed to be the shipped harness. `isolate.sh` itself passed every mode I threw at it: exit-0-no-bind → 125, unshare-refused → 125, missing target → 125, selective partial failure → 125.
- Did not re-run the original incident; relied on `SentinelGatePath.md:77`, `RevengeInnsHarness.md`, and `ScoutUnshareHost.md` for the real-EPERM facts.

## Installs

none (bash, util-linux unshare/mount already present; pacman pause honoured — no pacman, sudo, systemctl, hyprctl or host probe was run; all payloads were canary writes under `/tmp/critiso-mut/`).
