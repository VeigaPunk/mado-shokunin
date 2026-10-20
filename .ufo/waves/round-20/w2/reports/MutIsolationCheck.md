# MutIsolationCheck — falsified: skipping mount-noop makes one known-bad harness green

## Scope, axes, and verdict

**Single checker mutant:** delete `run_case mount-noop mount-noop target` from `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/isolation-check.sh:144`, exclusively in the isolated `/tmp` clone. No harness source bytes were mutated.

Axes: **detection sensitivity** (all five known-bad harnesses must be rejected with actual failure evidence), **calibration** (an unavailable fixture is inconclusive, not a kill), **host noninterference**, and **exact-byte restoration**.

**Mutation verdict: KILLED by the five-harness behavioral detector.** Its all-five-red expectation passes on pristine and restored checker bytes, but fails on mutated bytes: `m1-nocmp.sh` changes from exit **1 → 0 → 1**. The other four harnesses remain red. Thus the weakened checker does **not** still read red for all five. This is a scoped mutation result, not a round/C1/C2 admission judgment and not evidence that the pristine checker misses this fixture.

## Isolation and commands actually run

All executions used committed revision `a4046a8216080d4004de3f268c62cf142095ac07` in `/tmp/mado-r20w2-MutIsolationCheck`; the lane checkout was not used to execute scripts or mutated. The clone's origin was removed. Setup commands:

```sh
git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado-r20w2-MutIsolationCheck
git -C /tmp/mado-r20w2-MutIsolationCheck remote remove origin
git -C /tmp/mado-r20w2-MutIsolationCheck checkout -q --detach a4046a8216080d4004de3f268c62cf142095ac07
git -C /tmp/mado-r20w2-MutIsolationCheck rev-parse HEAD
```

Output: `a4046a8216080d4004de3f268c62cf142095ac07`.

These same five commands ran in each prepared-pristine, mutated-skip-mount-noop, and restored phase. A Python subprocess driver ran the five independent commands concurrently, with a 25-second bound per command and captured exit code plus complete merged stdout/stderr. No command timed out.

```sh
/usr/bin/bash /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/isolation-check.sh /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/evidence/inns-r19-shape.sh
/usr/bin/bash /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/isolation-check.sh /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/evidence/isolation-mutants/m1-nocmp.sh
/usr/bin/bash /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/isolation-check.sh /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/evidence/isolation-mutants/m3b-capprobe.sh
/usr/bin/bash /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/isolation-check.sh /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/evidence/isolation-mutants/m4-skiptarget.sh
/usr/bin/bash /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/isolation-check.sh /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/evidence/isolation-mutants/m6-besteffort.sh
```

The detector expectation was: each command exits 1, emits at least one `FAIL_OPEN` row, emits `POSITIVE_CONTROL_OK`, and emits no `COULD_NOT_EVALUATE` row. Prepared-pristine/restored additionally each emitted all six setup-failure transcripts. These conditions distinguish real red from a failed positive control or unavailable injection.

### Initial fixture-mode obstacle — not counted as a kill

An initial five-command batch on untouched clone modes produced exit 2 for the reference harness:

```text
COULD_NOT_EVALUATE inns-r19-shape.sh (not executable)
```

The other four commands already produced their expected red rows and successful positive controls. The reference result was **inconclusive**, not a killed mutant. Actual mode commands and output:

```sh
git -C /tmp/mado-r20w2-MutIsolationCheck ls-tree HEAD .ufo/waves/round-20/evidence/inns-r19-shape.sh
stat -c '%a %n' /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/evidence/inns-r19-shape.sh
```

```text
100644 blob 26f037748f7b37012bec56579bb9ecad258edca6 .ufo/waves/round-20/evidence/inns-r19-shape.sh
644 /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/evidence/inns-r19-shape.sh
```

I used `chmod u+x /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/evidence/inns-r19-shape.sh` solely to make the committed fixture executable, then established a fresh, valid pristine baseline **before** mutating the checker. This executable mode was identical across all three scored phases; the reference's source bytes never changed. Its mode was returned to 0644 after the restored phase. The initial reference log is `/tmp/mado-r20w2-MutIsolationCheck/MutIsolationCheck-pristine-inns-r19-shape.log`, SHA-256 `db8c8ac2d22da81a54d2f1895d89b08053e21a5e038f260b9778076a90da99df`.

## One-line defect and actual outputs

The mutation removed precisely this invocation; the mode implementation and every verdict branch stayed unchanged:

```diff
-run_case mount-noop mount-noop target
```

Source explanation: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/evidence/isolation-mutants/m1-nocmp.sh:26-30` checks mount exit codes but omits post-bind comparison. The no-op mount case is its sole observed failing setup in the pristine checker. Removing that one invocation removes its only rejection witness.

| Harness | Prepared-pristine exit / FAIL_OPEN modes | Mutated exit / FAIL_OPEN modes | Restored exit / FAIL_OPEN modes |
| --- | --- | --- | --- |
| `inns-r19-shape.sh` | 1 / mount-nonzero, mount-noop, partial-arm, missing-target, missing-stub | 1 / mount-nonzero, partial-arm, missing-target, missing-stub | 1 / mount-nonzero, mount-noop, partial-arm, missing-target, missing-stub |
| `m1-nocmp.sh` | **1 / mount-noop** | **0 / none** | **1 / mount-noop** |
| `m3b-capprobe.sh` | 1 / unshare-refused | 1 / unshare-refused | 1 / unshare-refused |
| `m4-skiptarget.sh` | 1 / missing-target | 1 / missing-target | 1 / missing-target |
| `m6-besteffort.sh` | 1 / partial-arm | 1 / partial-arm | 1 / partial-arm |

Every command in this table emitted `POSITIVE_CONTROL_OK`, with exit 0 and canary present for its positive control; none emitted `COULD_NOT_EVALUATE` or `NEVER_RUNS`. Each pristine/restored run exercised six setup-failure modes; each mutated run exercised five.

Discriminating pristine excerpt from `/tmp/mado-r20w2-MutIsolationCheck/MutIsolationCheck-prepared-pristine-m1-nocmp.log:18-24`:

```text
TRANSCRIPT setup-failure harness=m1-nocmp.sh mode=mount-noop targets=1
INJECTION: PATH-stub
output:
forced successful no-op mount
harness exit: 0; canary=present; injected-marker=present
FAIL_OPEN m1-nocmp.sh mode=mount-noop
```

The omitted `COMMAND:` line in that excerpt invokes the unchanged harness with a stub, target and payload entirely under `/tmp/mado-isolation-check.g3VCHQ/`; full command is retained in the log. Checker exit was **1**.

Mutated excerpt from `/tmp/mado-r20w2-MutIsolationCheck/MutIsolationCheck-mutated-skip-mount-noop-m1-nocmp.log:40-48`:

```text
harness exit: 125; canary=absent; injected-marker=absent
FAIL_CLOSED m1-nocmp.sh mode=missing-stub

TRANSCRIPT positive-control harness=m1-nocmp.sh
output:
harness exit: 0; canary=present
POSITIVE_CONTROL_OK m1-nocmp.sh
```

The intervening `COMMAND:` line is omitted here; the mutated log contains no mount-noop transcript and no `FAIL_OPEN` row. Checker exit was **0**, not an unavailable-injection result. Restoring the omitted line reinstated `FAIL_OPEN m1-nocmp.sh mode=mount-noop` and checker exit **1**.

Driver result lines:

```text
BOUNDED_ALL_FIVE_RED_BASELINE PASS
BOUNDED_ALL_FIVE_RED_MUTANT FAIL
MUTATION_VERDICT KILLED
BOUNDED_ALL_FIVE_RED_RESTORED PASS
```

The original reference alone stays red even after this weakening. [INFERENCE] A checker self-test that watches only that reference's final red status would therefore miss this exact omission; asserting the individual `m1-nocmp.sh` result distinguishes it. This inference does not claim such an incomplete self-test is shipped.

## Hashes and restoration evidence

Checker SHA-256, measured with `sha256sum`:

| State | SHA-256 |
| --- | --- |
| Original committed / prepared-pristine | `2bf115db1658df32d5e89e600ad6ef47c0e2855beda5f25dfc936270604f6aa9` |
| Mutated, one invocation removed | `ee1cefc376e30ac2717fdf226d4e2fc3db70b9e2f89054d5ce0d2c38cfce8591` |
| Restored | `2bf115db1658df32d5e89e600ad6ef47c0e2855beda5f25dfc936270604f6aa9` |

After restoration, this command compared the complete scratch checker against committed bytes, not just its behavior:

```sh
git -C /tmp/mado-r20w2-MutIsolationCheck show a4046a8216080d4004de3f268c62cf142095ac07:.ufo/waves/round-20/isolation-check.sh | /usr/bin/cmp - /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/isolation-check.sh && printf 'RESTORE_EXACT_BYTES=YES\n'
chmod 0644 /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/evidence/inns-r19-shape.sh
stat -c '%a %n' /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/evidence/inns-r19-shape.sh
```

```text
RESTORE_EXACT_BYTES=YES
644 /tmp/mado-r20w2-MutIsolationCheck/.ufo/waves/round-20/evidence/inns-r19-shape.sh
```

The five fixture hashes were measured before and after the probe and matched:

| Fixture | Before = after SHA-256 |
| --- | --- |
| `inns-r19-shape.sh` | `8bd507f0ea39d4d876359a0f5a1f798e810cda3c59293487af35d3a8df37ce9c` |
| `m1-nocmp.sh` | `2f2cc63bdb4903a42d99bf5685acc12e5b221158610217e42b0c1ee3d85df359` |
| `m3b-capprobe.sh` | `a6dde1c30355b29917091f0045b51befcefc7fc78d0903c098fc880ff9099727` |
| `m4-skiptarget.sh` | `a9bfa1be563c76e74edffa480514e69f3ee85ead8415e54b865d02be10107940` |
| `m6-besteffort.sh` | `ac11cc5adb1ece61eba4d45a8e2b65016576eb247957a846afe797b9118c6ed4` |

### Raw-output receipts

All full logs remain only in the scratch clone. Each path is `/tmp/mado-r20w2-MutIsolationCheck/MutIsolationCheck-<phase>-<harness-stem>.log`:

| Phase | Harness stem | Raw-output SHA-256 |
| --- | --- | --- |
| prepared-pristine | inns-r19-shape | `37feb3d19432251b935f55a5c867d4b8b63dde27aa5e65d6876537bc8b9e6dc6` |
| prepared-pristine | m1-nocmp | `9bbdd6aba6266053ccac9f55a0ecb591189917df9341c647bfbf0278bd223ed2` |
| prepared-pristine | m3b-capprobe | `b7aee74f711e4b5a30c0fc4f6e19c07729a986fc75de372506b06b13292e4867` |
| prepared-pristine | m4-skiptarget | `3e40116c0896830d7dd78ef207574686d587900c1d348f11807b2de3f3ba155e` |
| prepared-pristine | m6-besteffort | `5b98ad9acc25d4b526f2237b5705adba120b8be8d0b8d4f2d9329a3ccce7306f` |
| mutated-skip-mount-noop | inns-r19-shape | `61faba31b5e3f15b78f68c365cfb6409e90a91eea7179ad5b9df826f128a5909` |
| mutated-skip-mount-noop | m1-nocmp | `9e4b7687298e966e794045d2250e1509bed5c631b18bddd41c0c6196c7c5eab6` |
| mutated-skip-mount-noop | m3b-capprobe | `53570fd2a7d2b55899804c6b662b32f35a5a9e3e97e0250a5c58bd03ea489784` |
| mutated-skip-mount-noop | m4-skiptarget | `75fd705ebdde66b21bda6fe45aae612149221b0623d77e238f008ded4a6beac6` |
| mutated-skip-mount-noop | m6-besteffort | `9847a0d904477191d66c54b334315e8b48062c85b02c63edd429488282ed7bbd` |
| restored | inns-r19-shape | `c4a0df5a234c6b4b1406b8950701b980dad53180abfa4d74c8e92e54cc0d6835` |
| restored | m1-nocmp | `e8f34a0d11c8c3bcb72a205f9abd7c0543f08a82e32cad5374bc9304ab93657d` |
| restored | m3b-capprobe | `837b7a93867d91d2dd8f53ce47ccd8e9cd7a2b5baec53a89e3a6e7393f808f2a` |
| restored | m4-skiptarget | `c6d073bda6f31537527650d2e1a71e8ea0ebf4dde6c81a8341c9362139da34ef` |
| restored | m6-besteffort | `9d8da61a145b40cf02992bdeb757c820fd6d0104e1572b9d5b90ef785ce535ab` |

## Limits

- Exactly one plausible checker defect was injected, as assigned to the mutation-tester role: omitting the no-op-mount invocation. The SKIP_AS_SUCCESS branch, injection-marker condition, and positive-control canary condition were not separately mutated. No claim of exhaustive mutation coverage.
- The unprepared committed reference fixture was not executable; its first result was inconclusive. Every scored phase used the explicitly documented executable-mode preparation, and both source bytes and original mode were restored.
- This was a canary-only behavioral probe, not a sandbox assurance or live host gate. The checker-created payload only writes `payload-ran` to its own `/tmp` canary; binds target checker-owned `/tmp` files inside the harness namespace. No paused package, compositor, service, device, or screenshot command ran.
- No tracked lane/fleet source, sibling file, corpus, scorecard, manifest, routing, or runtime state was changed. The only lane write is this report. Raw logs are ephemeral `/tmp` artifacts; the commands, discriminating output, exit results and hashes are embedded here for durable review.
- No integration, round verdict, other runtime invocation, or unassigned verification suite was performed.

## Installs

none
