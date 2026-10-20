# Mado round 16 — SafetyReceipt (draft, w1)

Seat: `MadoR16.SafetyReceipt` (scribe). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`. Scope: draft receipt fields from
measured values only. No gate, case, or lesson file was authored. No build, lint, test,
gate selftest, `measure.py`, package query, service operation, compositor probe, input
probe, or install was run. No `~/.omp` file was opened.

Status: **draft; the receipt cannot bind a gate digest yet.** The action-plan gate and its
cases have not landed. Every field that depends on them is marked ABSENT or PENDING below.

## 1. Measured commit

| Field | Value | Command | Exit |
|---|---|---|---|
| `measured_commit` | `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea` | `git rev-parse HEAD` | 0 |
| HEAD subject | `round-15 verifier spot-check (integrator, hyaku): non-author admit/reject` | `git log -1 --format=...` | 0 |

## 2. Lane status (time-dependent, not a clean receipt baseline)

| Time (-03:00) | `git status --porcelain` | Exit |
|---|---|---|
| 05:39:21 | ` M SCORECARD.md`, `?? .ufo/waves/round-16/` | 0 |
| later re-measure | ` M SCORECARD.md`, ` M SKILL.md`, ` M corpus/QUALITY.md`, `?? .ufo/waves/round-16/` | 0 |

The `SCORECARD.md` change is a 29-line insertion, the round-16 declared-claims block
(`git diff --stat`, exit 0). It is written by a sibling seat and is not mine to commit.
The two later modifications (`SKILL.md`, `corpus/QUALITY.md`) appeared between my
measurements; I did not inspect or author them. Any closure receipt must re-measure status
after siblings finish and bind to a commit, not to the working tree.

## 3. Gate digest

| Gate file | State | SHA-256 | Measured by |
|---|---|---|---|
| `tools/mado-action-plan.py` (new SafetyGate output) | **ABSENT** at 05:39:21 | none, not fabricated | `[ -e ]` per path |
| `.ufo/waves/round-16/safety-policy.json` (new SafetyGate output) | **ABSENT** | none | `[ -e ]` |
| `.ufo/waves/round-16/measure.py` (referenced by SCORECARD C1 command) | **ABSENT** | none | `[ -e ]` |
| `tools/mado-verify.sh` (existing lane verify gate) | present, worktree == HEAD blob | `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207` | `sha256sum`, `git show HEAD:tools/mado-verify.sh \| sha256sum`, both exit 0 |

The `mado-verify.sh` digest matches the value the round-15 closure recorded at
`corpus/lessons/round-15-verifier-spotcheck.md` (§ Gate and correction evidence). It is the
existing verify gate, not the action-plan gate. It is not a digest for SafetyGate.

## 4. Input digests

| Input | SHA-256 | Command | Exit |
|---|---|---|---|
| `corpus/lessons/round-15-verifier-spotcheck.md` | `58e247f8525483eb7d4cc7a71ac4e64cb2b2ed3e5716af1234c0588cb882928a` | `sha256sum` | 0 |
| `.ufo/waves/round-16/w1/spec.json` | `21e16e6b6ebf5b99b2d9f621d170fecd665cd89bacc1208dbb70240a45ddf5cb` | `sha256sum` | 0 |
| `.ufo/waves/round-16/w1/dispatch.json` | `14fb2ece785a280a8e90156396213ee5690eab84533ee235fe4827f852fa2ebe` | `sha256sum` | 0 |
| `.ufo/waves/round-16/evidence/census-before.txt` | `6dbdb72bc76158760da493e1e71228d5f726b7021349ded5a0b305345b642865` | `sha256sum` | 0 |
| `SCORECARD.md` working tree | `978e152a2e9d158addb28115fcae85e3b2250f5a87135b342e5d191657182373` | `sha256sum` | 0 |
| `SCORECARD.md` HEAD blob | `6ff3ddb3c60d1c11763d6bc3213f297a16686588051c363954fdb70eba7cbe22` | `git show HEAD:SCORECARD.md \| sha256sum` | 0 |

The spec and dispatch digests were taken from the wave files as they stand. The census
file records `command=…sources-census.sh validate --root … mado`, `measured_commit=32c4fda…`,
and `exit=0` with four output lines. I read that file and did not re-run the census.

## 5. Actual command log (all executed by this seat)

| # | Command | Exit | Note |
|---|---|---|---|
| 1 | `git rev-parse HEAD` | 0 | 32c4fda… |
| 2 | `git log -1 --format='%H %an <%ae> %cI %s'` | 0 | protocol-shokunin commit |
| 3 | `git status --porcelain` (twice) | 0 | see §2 |
| 4 | `[ -e ]` loop over 4 gate/case paths | per-path | ABSENT for all 4 |
| 5 | `sha256sum` over 4 files | 0 | §3, §4 |
| 6 | `git show HEAD:tools/mado-verify.sh \| sha256sum` | 0 | fba82a… |
| 7 | `git diff --stat -- SCORECARD.md` | 0 | 29 insertions |
| 8 | `git show HEAD:SCORECARD.md \| sha256sum` | 0 | 6ff3dd… |
| 9 | `python3 --version` | 0 | 3.14.7, read-only probe only |
| 10 | `python3 -c` JSON read of `spec.json` and `dispatch.json` | 0 | structure only |
| 11 | `date -Iseconds` | 0 | 2026-10-20T05:39:21-03:00 |

Installs: none. Package operations: none. The round-15 `pacman -Sp` plan step does not apply
to this seat and was not run.

## 6. Receipt fields still PENDING (for L1 single verify, after integration)

These are not measured here. They must not be filled from this draft:

- `gate_digest` for `tools/mado-action-plan.py` and `.ufo/waves/round-16/safety-policy.json`,
  taken from **committed bytes** at the integrated commit.
- `gate_selftest` exit and output, `--plan`/`--policy` run exit and output, and `--frozen DIR`
  digest. Per contract these belong to L1.
- `safety-cases.json` digest and the case-run result.
- `measure.py` digest and the C1 run (SCORECARD names `python3 .ufo/waves/round-16/measure.py REV`).

## 7. Findings for L1 and the planner

1. **Gate not landed.** The action-plan classifier and policy are absent at the measured
   time. A receipt that cites a gate digest now would be fabricated; this one does not.
2. **Dirty worktree.** Status changed during this seat's run. Closure must re-measure status and
   bind every digest to the integrated commit.
3. **Hard-coded controls are not real plan validation.** Per the round-15 closure
   (R15-V2), any `--selftest` result is a fixture control. It is not proof that a real
   `pacman -Sp --print-format '%n %v'` plan or installed-name comparison ran. The receipt must
   keep that distinction in its wording.
4. **Existing verify gate is unchanged.** `tools/mado-verify.sh` is byte-identical between
   HEAD and the worktree and matches the round-15 recorded digest, so it cannot be cited as
   evidence for the new classifier.
5. **Referenced `measure.py` is absent.** The SCORECARD round-16 C1 command names a file that
   does not exist yet. Either SafetyGate or the C1 seat must land it before any C1 receipt.

Artifacts: this report only. No other file was created or modified by this seat.
