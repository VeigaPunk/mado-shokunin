# MutGateWalkerArms — two behavioral survivors; two rc-handling mutants killed

## Scope and detector

- Target: `tools/mado-verify.sh` at `17661e0fa83f978fb659f5bb8fef47f0969f6945`; extracted with `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 17661e0fa83f978fb659f5bb8fef47f0969f6945:tools/mado-verify.sh`. No lane source was edited.
- Snapshot: `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/pristine.sh` (3,786 lines; 182,988 bytes); SHA-256 `c9fb0cef3e081dc878d69f8e20c148429bdfbdce949f8afaed705db957ea42b5`.
- Axes: behavioral sensitivity, identical literal-detector controls, exact-byte restoration, host isolation.
- Four independent scratch copies under `/tmp/mado-r19-MutGateWalkerArms-684m0ou2`. Each received exactly one behavior-bearing line mutation. Pristine runs were concurrent across copies, as were the mutant and restored runs; no source was shared between probes.
- Fixed literal detector, run on each pristine, mutated and restored copy: `/usr/bin/bash <absolute-copy-path> --selftest`.
- Detector environment was constructed from `PATH=/usr/bin:/bin`, `HOME=/tmp/mado-r19-MutGateWalkerArms-684m0ou2/isolated-home`, and `LC_ALL=C`; `DEFECT_ID`, host-session variables and inherited gate/stub overrides were absent. Cwd was `/tmp/mado-r19-MutGateWalkerArms-684m0ou2`. Every run was bounded by 240 seconds; none timed out. All captured stderr was empty.
- Each pristine and restored run exited **0** with exactly `MADO_SELFTEST: 389/389 assertions passed`.

### Important identity-check distinction

At `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/pristine.sh:577-589`, R10 compares the derived gate bytes with a frozen hash when `DEFECT_ID` is unset/`CONTROL`, and expects a changed hash for a non-control defect. Thus the literal detector rejects **every** one-line mutation by identity, even if the affected behavior is never asserted.

Literal outcome: **0/4 literal survivors**. Behavioral outcome: **2/4 killed, 2/4 survived; 0 inconclusive**. The walker and directory-guard runs had only the R10 identity failure; they are not behavior kills.

As a supplementary observation, I also ran the same unedited `--selftest` on each mutant with its intended `DEFECT_ID=MUT_<mutant-name>` interface. This changes only R10's control/defect expectation: walker and directory-guard mutants passed 389/389; the two rc mutants still failed four OM10 assertions. This is not represented as a second fixed-environment pristine→mutant→restore experiment: the non-control identity mode intentionally requires changed bytes. The fixed-environment triple above supplies the green controls and the behavioral failure attribution.

## Mutation results

| Mutant | Pinned source line | Single-line change | Literal mutant result | Supplementary defect-id result | Behavioral verdict |
|---|---:|---|---|---|---|
| WALKER_COMPARE | 3277 | `if [ "$kv" = "2.17.0" ]; then` → `if [ "$kv" != "2.17.0" ]; then` | rc 2; 388 passed / 1 failed, R10 only | rc 0; 389/389 passed | **SURVIVED** |
| GIT_DIRECTORY_GUARD | 3412 | `[ -d "$tree/.git" ] && omtree=1` → `[ -n "$tree/.git" ] && omtree=1` | rc 2; 388 passed / 1 failed, R10 only | rc 0; 389/389 passed | **SURVIVED** |
| GIT_DESCRIBE_RC | 3447 | On the `git describe` assignment, `grc=$?` → `grc=0` | rc 2; 384 passed / 5 failed: R10 + four OM10 assertions | rc 2; 385 passed / 4 failed, OM10 | **KILLED** |
| GIT_REVPARSE_RC | 3456 | On the `git rev-parse` assignment, `grc=$?` → `grc=0` | rc 2; 384 passed / 5 failed: R10 + four OM10 assertions | rc 2; 385 passed / 4 failed, OM10 | **KILLED** |

### Expected behavioral detectors

- **Walker compare:** a matching pinned version must emit `live.walker.version PASS`; a different version must emit `FAIL` with `pin changed`. The inverted predicate violates both decisions (`/tmp/mado-r19-MutGateWalkerArms-684m0ou2/pristine.sh:3271-3281`). Neither result was asserted by the present suite against this mutation.
- **Checkout directory guard:** with `git` available but `$tree/.git` absent, `omarchy.git.tag` and `omarchy.git.head` must remain `UNKNOWN` with `no git checkout`, and `omarchy.skill.vs_head` must remain `UNKNOWN`. The mutant treats any nonempty constructed pathname as a checkout (`/tmp/mado-r19-MutGateWalkerArms-684m0ou2/pristine.sh:3411-3412,3439-3444,3467-3468`). The negative prerequisite was not behaviorally detected.
- **Describe rc:** existing OM10 must require `omarchy.git.tag UNKNOWN`, preserve `rc=128`, forbid a false `MOVED: describe`, and retain exactly two omarchy UNKNOWNs (`/tmp/mado-r19-MutGateWalkerArms-684m0ou2/pristine.sh:832-848`). All four corresponding assertions failed on this mutant.
- **Rev-parse rc:** existing OM10 must require the analogous HEAD UNKNOWN/rc/no-false-MOVED/count decisions. All four corresponding assertions failed on this mutant.

## Actual mutant output

Commands below used the corresponding absolute `.../<mutant>/gate.sh` path. The literal and defect-id runs captured the following full stdout; stderr was empty in each case.

### WALKER_COMPARE

Literal command: `/usr/bin/bash /tmp/mado-r19-MutGateWalkerArms-684m0ou2/WALKER_COMPARE/gate.sh --selftest`

```text
MADO_SELFTEST: FAILED — 388 passed, 1 failed
  - R10: derived target equals the recorded gate revision (got 'bc33d726b8210ae5621202e19a484566112b93970cfd5dffb3c0ae845592e1be' want '20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744')
fixtures kept: /tmp/w5-mado-m52-selftest.jbkSH8
```

Supplementary command: `DEFECT_ID=MUT_WALKER_COMPARE /usr/bin/bash /tmp/mado-r19-MutGateWalkerArms-684m0ou2/WALKER_COMPARE/gate.sh --selftest`

```text
MADO_SELFTEST: 389/389 assertions passed
```

### GIT_DIRECTORY_GUARD

Literal command: `/usr/bin/bash /tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_DIRECTORY_GUARD/gate.sh --selftest`

```text
MADO_SELFTEST: FAILED — 388 passed, 1 failed
  - R10: derived target equals the recorded gate revision (got '5bbc1c66848a7b5c45a6e86d02364b31ab598ed19eeaa6528921fe2bc17a1f10' want '20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744')
fixtures kept: /tmp/w5-mado-m52-selftest.qpNdGc
```

Supplementary command: `DEFECT_ID=MUT_GIT_DIRECTORY_GUARD /usr/bin/bash /tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_DIRECTORY_GUARD/gate.sh --selftest`

```text
MADO_SELFTEST: 389/389 assertions passed
```

### GIT_DESCRIBE_RC

Literal command: `/usr/bin/bash /tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_DESCRIBE_RC/gate.sh --selftest`

```text
MADO_SELFTEST: FAILED — 384 passed, 5 failed
  - R10: derived target equals the recorded gate revision (got '0ff3914d5afd2b6f35e20931eb706cb1b597478267c18b3c4b6feabacaa2be13' want '20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744')
  - OM10 (describe rc=128 is unverified) (want row omarchy.git.tag UNKNOWN)
  - OM10: the UNKNOWN names the rc (want row omarchy.git.tag UNKNOWN containing 'rc=128')
  - OM10: no false tag MOVED (unexpected: MOVED: describe)
  - OM10: exactly two omarchy UNKNOWNs (tag + head) (got '1' want '2')
fixtures kept: /tmp/w5-mado-m52-selftest.RUJdUB
```

Supplementary command: `DEFECT_ID=MUT_GIT_DESCRIBE_RC /usr/bin/bash /tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_DESCRIBE_RC/gate.sh --selftest`

```text
MADO_SELFTEST: FAILED — 385 passed, 4 failed
  - OM10 (describe rc=128 is unverified) (want row omarchy.git.tag UNKNOWN)
  - OM10: the UNKNOWN names the rc (want row omarchy.git.tag UNKNOWN containing 'rc=128')
  - OM10: no false tag MOVED (unexpected: MOVED: describe)
  - OM10: exactly two omarchy UNKNOWNs (tag + head) (got '1' want '2')
fixtures kept: /tmp/w5-mado-m52-selftest.lJXuYK
```

### GIT_REVPARSE_RC

Literal command: `/usr/bin/bash /tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_REVPARSE_RC/gate.sh --selftest`

```text
MADO_SELFTEST: FAILED — 384 passed, 5 failed
  - R10: derived target equals the recorded gate revision (got 'c443cd580974d6f49813a792b4274328ceaa06a53fa801a6f9ce868fa10ee5b6' want '20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744')
  - OM10 (rev-parse rc=128 is unverified) (want row omarchy.git.head UNKNOWN)
  - OM10: the UNKNOWN names the rc (want row omarchy.git.head UNKNOWN containing 'rc=128')
  - OM10: no false head MOVED (unexpected: MOVED: rev-parse)
  - OM10: exactly two omarchy UNKNOWNs (tag + head) (got '1' want '2')
fixtures kept: /tmp/w5-mado-m52-selftest.1jUcLz
```

Supplementary command: `DEFECT_ID=MUT_GIT_REVPARSE_RC /usr/bin/bash /tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_REVPARSE_RC/gate.sh --selftest`

```text
MADO_SELFTEST: FAILED — 385 passed, 4 failed
  - OM10 (rev-parse rc=128 is unverified) (want row omarchy.git.head UNKNOWN)
  - OM10: the UNKNOWN names the rc (want row omarchy.git.head UNKNOWN containing 'rc=128')
  - OM10: no false head MOVED (unexpected: MOVED: rev-parse)
  - OM10: exactly two omarchy UNKNOWNs (tag + head) (got '1' want '2')
fixtures kept: /tmp/w5-mado-m52-selftest.e1J1CL
```

## Scenario proposals for the gate writer

### W1 — Reach and assert the walker version arm

[INFERENCE] The survival is explained by live-plane preflight returning before this arm: the OM PATH fixture includes neither `hyprctl` nor `walker` (`/tmp/mado-r19-MutGateWalkerArms-684m0ou2/pristine.sh:631-688`), and `live_plane` returns UNKNOWN when `hyprctl` is absent (`/tmp/mado-r19-MutGateWalkerArms-684m0ou2/pristine.sh:3033-3047`). No runtime branch trace was taken.

Extend an existing hermetic fixture with a **strict, fixture-only PATH** containing inert `hyprctl` and `walker` stubs, plus a fixture `HYPRLAND_INSTANCE_SIGNATURE`. The `hyprctl version` stub must succeed so preflight reaches the walker code. Every other host-facing name must remain absent or be a fixture stub, never fall through to a host command.

- Stub `walker --version` to the gate's declared pin and assert the **named row** is PASS, including the pin detail.
- Stub it to a distinct version and assert that same row is FAIL with `pin changed` and the observed version.
- Assert the stub was actually called with `--version`; an early `live.plane UNKNOWN` must not satisfy this case.
- At this revision the values can be `2.17.0` / `2.17.2`. If the writer re-pins the gate to `2.17.2`, update the matching fixture and retain a distinct drift value; do not conflate the pin update with this coverage proposal.
- Do not use only overall rc/DIVERGED: unrelated absent fixture consumers may already make the gate red. These assertions must kill the comparator inversion directly.

### G1 — Git available, checkout metadata absent

[INFERENCE] Existing OM success fixtures create `$tree/.git` as a directory (`/tmp/mado-r19-MutGateWalkerArms-684m0ou2/pristine.sh:633-634`), so they do not challenge replacement of the directory predicate by a nonempty-path predicate.

Copy the existing OM fixture, omit only the scratch `.git` directory, and retain the strict OM PATH with its canned-success `git` reader, version file, skill link and leaf. Assert:

- `omarchy.git.tag UNKNOWN` and `omarchy.git.head UNKNOWN`, both naming `no git checkout`;
- `omarchy.skill.vs_head UNKNOWN`, naming the unreadable checkout/leaf relation;
- No `describe`, `rev-parse`, or `show` call appears in a fixture git-call ledger for this case.

The `-n` mutant would use the canned successes rather than decline the probe, so these named-row assertions would challenge the missing guard. This proposal preserves the current directory-based contract; it does not decide support for valid `.git` indirection files or change any contract. No extra scenario is needed to explain the two tested rc kills: OM10 already detects them.

## Hashes and restoration evidence

All four files were restored in a `finally` path **before** restored detector runs. In-memory comparison against the extracted source bytes returned `True` for every restored copy. Pristine/restored file size was 182,988 bytes. The detector did not change any tested copy: before/after hashes within every run matched.

Common pristine and restored SHA-256: `c9fb0cef3e081dc878d69f8e20c148429bdfbdce949f8afaed705db957ea42b5`.

| Copy | Mutated SHA-256 (both mutant runs) | Pristine / restored rc | Exact-byte restoration |
|---|---|---|---|
| WALKER_COMPARE | `518228429ec5e2c325b35e2597c980eb58101b61fbcbdc15b0acb39506a2df55` | 0 / 0; each 389/389 | True; common SHA above |
| GIT_DIRECTORY_GUARD | `a9aa48988d1ba03a699d1a336219e0d3872b77d621c901aa574a508f2464ffa4` | 0 / 0; each 389/389 | True; common SHA above |
| GIT_DESCRIBE_RC | `d6b9d50777c8df719266d9b5a31c1b64c42978385dba60b48dca2b13ee6ea57e` | 0 / 0; each 389/389 | True; common SHA above |
| GIT_REVPARSE_RC | `8ed6a2ad179a9f1ba0162cb92f5f5309cf34f9e1bfe277b3567789419125c507` | 0 / 0; each 389/389 | True; common SHA above |

### Captured run receipts

Each absolute JSON receipt records command, complete explicit environment, timestamp, rc, timeout flag, full stdout/stderr, and before/after copy hashes. SHA-256 below is for the JSON bytes written. Full mutant stdout is also embedded above so the key evidence is retained in this report independently of `/tmp` lifetime.

| Receipt path | rc | Receipt SHA-256 |
|---|---:|---|
| `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/WALKER_COMPARE/pristine.json` | 0 | `c97573f593ad0f6a89df1e0ddf714b1482dd3a93eda6b4fcce5a02a78a2e23d3` |
| `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/WALKER_COMPARE/mutated-literal.json` | 2 | `6bb9763c52de8bd0af374bccae5d21e2599f2b9d3d7d288991678c19eb85e016` |
| `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/WALKER_COMPARE/mutated-defect-id.json` | 0 | `25e77c598fca7ea76f21eab2dea91472dbf1d853dad8829bfd6aadcf82e663d0` |
| `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/WALKER_COMPARE/restored.json` | 0 | `fb66462e544de6754c4cccbfd628e0f29bd153ad4fc343e95af416742f5bf65f` |
| `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_DIRECTORY_GUARD/pristine.json` | 0 | `302159204b5678caa5611a28f4d7c2453b11d9a12d943cb53087642519850c81` |
| `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_DIRECTORY_GUARD/mutated-literal.json` | 2 | `7b78020c3a3f7a6a91527816d964962b3f4d9ffcfdebacce134d8a4aaab3103e` |
| `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_DIRECTORY_GUARD/mutated-defect-id.json` | 0 | `f63a21d51feca26cf06870493fc4b5d2ad3ce1bce7e4f8a94684accf32d7e3a5` |
| `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_DIRECTORY_GUARD/restored.json` | 0 | `6bef2ea0189a6c2902848f3d63164790361a9322f571a42364e446dc6a0a9706` |
| `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_DESCRIBE_RC/pristine.json` | 0 | `2c6f4e439064628faeff7f38ff85f5a926a9a3e9c31570552b222766eb3da17c` |
| `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_DESCRIBE_RC/mutated-literal.json` | 2 | `9ccc05d520d7d1079932cffac1f0acfc7fe29de1576eed8b31d13e8921594b79` |
| `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_DESCRIBE_RC/mutated-defect-id.json` | 2 | `1f13b6c0e1e5d596159f8d63d07d163bb05c3f953b024c74435271bd39f1a29a` |
| `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_DESCRIBE_RC/restored.json` | 0 | `18afb22d2b64a621fed09fbd8997e4298939af0d16329a99674003dddc591622` |
| `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_REVPARSE_RC/pristine.json` | 0 | `ced893a825e770c265c3cebf34808a2c85d251e50b28c277b3d491db15938fbc` |
| `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_REVPARSE_RC/mutated-literal.json` | 2 | `a68a92d689135f29ead6e31798542a8447237b48ea991ba061cd5f562497b72c` |
| `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_REVPARSE_RC/mutated-defect-id.json` | 2 | `fe01e21d9501dded7c2cfae098fd3c0069c98b7afc13ae51838d197288e90286` |
| `/tmp/mado-r19-MutGateWalkerArms-684m0ou2/GIT_REVPARSE_RC/restored.json` | 0 | `55808420ef9fc6031119c525929b7e8e10b6f87bee3a787ecc5be004d25c3479` |

## Limits

- This is a bounded mutation probe of the pinned revision, not a review of concurrent lane changes or an integration/ship decision. Only the four specified behavior points were mutated.
- Literal identity rejection is not presented as behavioral coverage. The two survivor labels mean behavioral assertions survived; the unmodified literal command did reject their changed bytes through R10.
- Proposed scenarios were not implemented or run. Behavioral effects not exercised by the suite are derived from the shown source, not claimed as live observations.
- No live gate, real walker, compositor, service operation, package-manager command, web fetch, git write, jj command, sibling runtime, or subagent was invoked. Direct execution was limited to the assigned `--selftest` command; it used its existing hermetic regression/snapshot fixtures internally.
- No canonical source, tests, docs, manifests or fleet file was edited. The only lane write is this report; scratch scripts/receipts and selftest failure fixtures are under `/tmp` and are ephemeral.

## Installs

none
