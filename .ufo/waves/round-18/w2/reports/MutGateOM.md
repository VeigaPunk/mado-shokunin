# MutGateOM — F10/F14 mutation probe

Seat: `MadoR18.MutGateOM` · round 18, wave 2 · 2026-10-20.

## Scope, axes, invariant

- **Operability:** a failed `git show` must produce `omarchy.skill.vs_head UNKNOWN`, retain the unreadable path and producer rc, and never claim a local edit.
- **Coverage:** OM9 must exercise the failed-show path; OM10 must exercise failed `describe` and `rev-parse` independently of a successful show. Each per-verb rc knob must actually affect its verb.
- **Calibration:** distinguish behavioral failures from the existing R10 source-digest assertion; do not count a source-pin-only kill as behavioral bite.
- **Safety:** mutate only `tools/mado-verify.sh` inside isolated `/tmp` clones; restore exact bytes. No host gate run, lane source edit, integration, or contract change.

Read first: lane `SCORECARD.md` tail, including “Round 18 — declared claims”, and `corpus/lessons/round-18.md` (especially M3/M4).

Pinned parent revision: **`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`** (receipts revision). Integration reference: `4c103b55b1ea5c3c555884afe3eb69b5189701b7`.

## Result

**Requested complete detector: 8 KILLED, 0 SURVIVED, 0 INCONCLUSIVE.**

**Behavioral qualification: OM9/OM10 fail for 7 of the 8 mutants.** M07 (putting the `-z` arm first) fails **only R10's derived-target digest assertion**: 388 assertions pass and the sole failure is the recorded source pin. It therefore **survives the OM9/OM10 behavioral slice**, although the complete requested detector kills it. Do not report this as eight behavioral kills.

All eight pristine runs and all eight restored runs exited 0 with `MADO_SELFTEST: 389/389 assertions passed`. All eight mutated runs exited 2. No baseline failure was classified as a kill.

## Execution and isolation

Unmodified reference clone:

```text
/tmp/MadoR18-MutGateOM-abfbf35b.OXyCI5
```

Actual initial commands (cwd `/tmp`):

```sh
mktemp -d /tmp/MadoR18-MutGateOM-abfbf35b.XXXXXX
git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/MadoR18-MutGateOM-abfbf35b.OXyCI5
git -C /tmp/MadoR18-MutGateOM-abfbf35b.OXyCI5 checkout --detach abfbf35b1ed4d4a1eb294d525ef286be30f3886f
```

For each ID in the table below, a separate clone was created by these actual argument templates, with `ID` replaced by that row's exact ID:

```sh
git clone --no-hardlinks --no-checkout /tmp/MadoR18-MutGateOM-abfbf35b.OXyCI5 /tmp/MadoR18-MutGateOM-abfbf35b.OXyCI5-ID
git -C /tmp/MadoR18-MutGateOM-abfbf35b.OXyCI5-ID checkout --detach abfbf35b1ed4d4a1eb294d525ef286be30f3886f
```

All clone/checkouts returned 0. Eight independent copies were exercised concurrently within each stage: pristine, then mutated, then restored. Each run used the **same unchanged command**, in its clone cwd:

```sh
bash tools/mado-verify.sh --selftest
```

There were **24 detector executions**, with no detector substitution, assertion deletion, source-pin re-cut, or additional direct gate invocation. The authorized selftest internally launches its own fixture-root children and canned PATH stubs; no direct default/live gate command was issued by this probe.

For every run, `sha256sum tools/mado-verify.sh` was executed immediately before the detector. After restoration and the restored detector, each target was compared to the untouched reference using `cmp -s`, and hashed again.

## Mutants and expected detector

All line numbers below refer to `tools/mado-verify.sh` at the pinned parent revision. Each copy carried just its one listed mutation.

| ID | Exact scoped mutation | Expected behavioral detector | Actual failures | Complete verdict |
|---|---|---|---|---|
| `m01-drop-pipefail` | L3477: remove `set -o pipefail;` inside the blob command substitution; leave the pipeline and `grc=$?` intact | OM9 failed-show UNKNOWN, path/rc, no local-edit claim, UNKNOWN/FAIL counts | OM9: 5; R10 pin: 1 | KILLED |
| `m02-invert-grc` | L3480: `if [ "$grc" != 0 ]; then` → `if [ "$grc" = 0 ]; then` | OM9 failed-show handling; OM10 successful-show comparison | OM9: 5; OM10: 2; OM1/OM4/OM6: 4; R10 pin: 1 | KILLED |
| `m03-ignore-describe` | Delete L672, the entire `STUB_GIT_DESCRIBE_RC` conditional exit line | OM10 tag UNKNOWN with rc=128 and two-UNKNOWN census | OM10: 3; R10 pin: 1 | KILLED |
| `m04-ignore-revparse` | Delete L675, the entire `STUB_GIT_REVPARSE_RC` conditional exit line | OM10 head UNKNOWN with rc=128 and two-UNKNOWN census | OM10: 3; R10 pin: 1 | KILLED |
| `m05-ignore-show` | Delete L678, the entire `STUB_GIT_SHOW_RC` conditional exit line | OM9 failed-show UNKNOWN, path/rc, no local-edit claim, counts | OM9: 5; R10 pin: 1 | KILLED |
| `m06-drop-rc-detail` | L3481: remove only ` (rc=$grc)` from the UNKNOWN detail string | OM9 detail must include unreadable path and `(rc=128)` | OM9 detail: 1; R10 pin: 1 | KILLED |
| `m07-z-arm-first` | L3480–3483: move the entire `-z "$blob"` arm ahead of the nonzero-rc arm, retaining each arm's original detail string | Tests would need an empty blob together with a failed producer/pipeline to distinguish which UNKNOWN reason wins | No OM9/OM10 failure; R10 pin: 1 only | KILLED by pin only; behavioral slice SURVIVED |
| `m08-status-clobber` | L3478–3479: move `; grc=$?` from the blob assignment to the end of the following `sw=$(sha256sum …)` assignment | OM9 must reject losing the failed git rc to a later successful worktree hash | OM9: 5; R10 pin: 1 | KILLED |

M07's mutated branch order was exactly:

```sh
      if [ -z "$blob" ]; then
        row omarchy omarchy.skill.vs_head UNKNOWN "cannot read HEAD:$OMARCHY_SKILL_REL from the checkout"
      elif [ "$grc" != 0 ]; then
        row omarchy omarchy.skill.vs_head UNKNOWN "cannot read HEAD:$OMARCHY_SKILL_REL (rc=$grc) — worktree/HEAD relation unverified"
```

M08's mutated assignments were exactly:

```sh
      blob=$(set -o pipefail; tmo git -C "$tree" show "HEAD:$OMARCHY_SKILL_REL" 2>/dev/null \
        | sha256sum | cut -d' ' -f1)
      sw=$(sha256sum "$leaf" 2>/dev/null | cut -d' ' -f1); grc=$?
```

### Coverage interpretation

The complete detector includes R10, which rejects all eight changed derived-target digests. Seven mutants also fail the named OM9/OM10 assertions, so their failures are not merely source identity alarms.

M07 has no non-R10 assertion failure. With OM9's healthy `sha256sum` and `cut`, failed git still yields a nonempty empty-input digest, so reordering the empty-blob guard does not change this fixture's behavior. This is a bounded behavioral-coverage limit, **not proof that this reorder harms the tested git-failure case**, and not authority to change the contract or weaken/re-cut the pin. No empty-digest/hash-reader failure scenario was added or run.

## Hash receipts and restoration evidence

Common pristine/restored SHA-256 (**P**):

```text
c9fb0cef3e081dc878d69f8e20c148429bdfbdce949f8afaed705db957ea42b5
```

This was measured on the untouched reference, on every pristine target, on every restored target before its restored selftest, and on every restored target after that selftest. `P` below denotes that exact full hash, not an abbreviated hash.

| ID | Before | Mutated SHA-256 | Restored, before and after detector | `cmp -s` to reference |
|---|---|---|---|---|
| `m01-drop-pipefail` | P | `e937f9825dde73eda42840331947e3bcf0e516b5e20f17ce4f541cc27dd397bb` | P | 0, no output |
| `m02-invert-grc` | P | `f98c82e990fd3610cbbbb778650187ee13c839a8c7768e593d454188cc78213d` | P | 0, no output |
| `m03-ignore-describe` | P | `fb5490647c56dc361b29d954aeb6a54d55575e8cc877825bd2fbe895a2672c86` | P | 0, no output |
| `m04-ignore-revparse` | P | `902fc7d1a06ec4532080826e9a677be1cd0f15d646fe50ebc2e08c6669ce6eb9` | P | 0, no output |
| `m05-ignore-show` | P | `a6b70ef68da72e61fed2974877482b61b72a9711e9082f002dc9af2ab9ff961c` | P | 0, no output |
| `m06-drop-rc-detail` | P | `9ec7e4279e05f9beac777cddc3c3724357c0984375c171c172f379ce4ae9dd90` | P | 0, no output |
| `m07-z-arm-first` | P | `56d9f9fd618425756173a5bd5da421f1265cee95bd12551e9b0c93844a239eed` | P | 0, no output |
| `m08-status-clobber` | P | `8ea5b4caafdecb2821c09a22f0a1c3c0a7794f3ac6dd11a212c19401a4351f26` | P | 0, no output |

The actual comparison command for each row was:

```sh
cmp -s /tmp/MadoR18-MutGateOM-abfbf35b.OXyCI5/tools/mado-verify.sh /tmp/MadoR18-MutGateOM-abfbf35b.OXyCI5-ID/tools/mado-verify.sh
```

Exact original lines were restored with surgical edits, including reinsertion of the three deleted rc-knob lines. All eight scratch targets remain restored.

## Pristine and restored detector outputs

Every pristine/restored run printed exactly this one line:

```text
MADO_SELFTEST: 389/389 assertions passed
```

| ID | Pristine rc / elapsed seconds | Restored rc / elapsed seconds |
|---|---|---|
| `m01-drop-pipefail` | 0 / 12.898 | 0 / 11.905 |
| `m02-invert-grc` | 0 / 12.896 | 0 / 11.917 |
| `m03-ignore-describe` | 0 / 12.899 | 0 / 11.909 |
| `m04-ignore-revparse` | 0 / 12.908 | 0 / 11.917 |
| `m05-ignore-show` | 0 / 12.923 | 0 / 11.901 |
| `m06-drop-rc-detail` | 0 / 12.921 | 0 / 11.861 |
| `m07-z-arm-first` | 0 / 12.916 | 0 / 11.915 |
| `m08-status-clobber` | 0 / 12.912 | 0 / 11.859 |

## Mutated detector outputs — verbatim combined stdout/stderr

### m01-drop-pipefail — exit 2

```text
MADO_SELFTEST: FAILED — 383 passed, 6 failed
  - R10: derived target equals the recorded gate revision (got 'f034b8393beadb8072ae17d015d824595b6425507d1d8d463ecd6af2fb36d289' want '20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744')
  - OM9 (a failed show can never be compared) (want row omarchy.skill.vs_head UNKNOWN)
  - OM9: the UNKNOWN names the unreadable path and the producer rc (want row omarchy.skill.vs_head UNKNOWN containing 'cannot read HEAD:default/omarchy-skill/SKILL.md (rc=128)')
  - OM9: no false local-edit claim (unexpected: local edit)
  - OM9: exactly one omarchy UNKNOWN (the failed read) (got '0' want '1')
  - OM9: exactly one omarchy FAIL — the unreproducible sha row (got '2' want '1')
fixtures kept: /tmp/w5-mado-m52-selftest.FTkC7l
```

### m02-invert-grc — exit 2

```text
MADO_SELFTEST: FAILED — 377 passed, 12 failed
  - R10: derived target equals the recorded gate revision (got 'fd1c0a8fe4e8131a4c4f6915fd8ccd94bc6966917aef763f6d147eaf43894111' want '20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744')
  - OM1 (same bytes both sides) (want row omarchy.skill.vs_head PASS)
  - OM1: zero omarchy UNKNOWN (got '1' want '0')
  - OM4: two omarchy UNKNOWNs, no silent pass (got '3' want '2')
  - OM6: a worktree edit is detected without git status (want row omarchy.skill.vs_head FAIL containing 'local edit')
  - OM9 (a failed show can never be compared) (want row omarchy.skill.vs_head UNKNOWN)
  - OM9: the UNKNOWN names the unreadable path and the producer rc (want row omarchy.skill.vs_head UNKNOWN containing 'cannot read HEAD:default/omarchy-skill/SKILL.md (rc=128)')
  - OM9: no false local-edit claim (unexpected: local edit)
  - OM9: exactly one omarchy UNKNOWN (the failed read) (got '0' want '1')
  - OM9: exactly one omarchy FAIL — the unreproducible sha row (got '2' want '1')
  - OM10 (show succeeds; the comparison still runs) (want row omarchy.skill.vs_head PASS)
  - OM10: exactly two omarchy UNKNOWNs (tag + head) (got '3' want '2')
fixtures kept: /tmp/w5-mado-m52-selftest.cpknrI
```

### m03-ignore-describe — exit 2

```text
MADO_SELFTEST: FAILED — 385 passed, 4 failed
  - R10: derived target equals the recorded gate revision (got '4e5adff99ba56335f94c5e6bcaa17dc0fd42943f13fbc5b46314aadc38d987c2' want '20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744')
  - OM10 (describe rc=128 is unverified) (want row omarchy.git.tag UNKNOWN)
  - OM10: the UNKNOWN names the rc (want row omarchy.git.tag UNKNOWN containing 'rc=128')
  - OM10: exactly two omarchy UNKNOWNs (tag + head) (got '1' want '2')
fixtures kept: /tmp/w5-mado-m52-selftest.DfoLwC
```

### m04-ignore-revparse — exit 2

```text
MADO_SELFTEST: FAILED — 385 passed, 4 failed
  - R10: derived target equals the recorded gate revision (got 'd3e228655b012ef0b820d484d3ac51a8e66e654eb78de7cf0c09420293061452' want '20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744')
  - OM10 (rev-parse rc=128 is unverified) (want row omarchy.git.head UNKNOWN)
  - OM10: the UNKNOWN names the rc (want row omarchy.git.head UNKNOWN containing 'rc=128')
  - OM10: exactly two omarchy UNKNOWNs (tag + head) (got '1' want '2')
fixtures kept: /tmp/w5-mado-m52-selftest.5PV6cQ
```

### m05-ignore-show — exit 2

```text
MADO_SELFTEST: FAILED — 383 passed, 6 failed
  - R10: derived target equals the recorded gate revision (got '03daf2bbecf8fb06f513e6ed36d0cdf50e1143ee7d51ba6471d940355754b943' want '20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744')
  - OM9 (a failed show can never be compared) (want row omarchy.skill.vs_head UNKNOWN)
  - OM9: the UNKNOWN names the unreadable path and the producer rc (want row omarchy.skill.vs_head UNKNOWN containing 'cannot read HEAD:default/omarchy-skill/SKILL.md (rc=128)')
  - OM9: no false local-edit claim (unexpected: local edit)
  - OM9: exactly one omarchy UNKNOWN (the failed read) (got '0' want '1')
  - OM9: exactly one omarchy FAIL — the unreproducible sha row (got '2' want '1')
fixtures kept: /tmp/w5-mado-m52-selftest.BkwObx
```

### m06-drop-rc-detail — exit 2

```text
MADO_SELFTEST: FAILED — 387 passed, 2 failed
  - R10: derived target equals the recorded gate revision (got '5d725bdef3fc85a455dfd7e54cbc201e09d072ca93a58c6f0a2b94e094ca4491' want '20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744')
  - OM9: the UNKNOWN names the unreadable path and the producer rc (want row omarchy.skill.vs_head UNKNOWN containing 'cannot read HEAD:default/omarchy-skill/SKILL.md (rc=128)')
fixtures kept: /tmp/w5-mado-m52-selftest.M1Kqjn
```

### m07-z-arm-first — exit 2

```text
MADO_SELFTEST: FAILED — 388 passed, 1 failed
  - R10: derived target equals the recorded gate revision (got '6b414f1bf371ae1ed74993cdde1dca8f58e8aaa2d549a1a51cbf5ab46a7d66e5' want '20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744')
fixtures kept: /tmp/w5-mado-m52-selftest.WPuJoC
```

### m08-status-clobber — exit 2

```text
MADO_SELFTEST: FAILED — 383 passed, 6 failed
  - R10: derived target equals the recorded gate revision (got '80a7172add35233642ab5dd2813d04706231e2cfed8a9457a66190be88a70c05' want '20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744')
  - OM9 (a failed show can never be compared) (want row omarchy.skill.vs_head UNKNOWN)
  - OM9: the UNKNOWN names the unreadable path and the producer rc (want row omarchy.skill.vs_head UNKNOWN containing 'cannot read HEAD:default/omarchy-skill/SKILL.md (rc=128)')
  - OM9: no false local-edit claim (unexpected: local edit)
  - OM9: exactly one omarchy UNKNOWN (the failed read) (got '0' want '1')
  - OM9: exactly one omarchy FAIL — the unreproducible sha row (got '2' want '1')
fixtures kept: /tmp/w5-mado-m52-selftest.qbwbw4
```

## Boundary and handoff

- Only this report was written in the lane. All source mutations and git writes were confined to this seat's `/tmp` clones; no lane git/jj write or jj command was issued.
- No packages/tools installed or updated; no package-manager, privilege, service, compositor, device, screenshot, network-fetch, REA, or browser operation was used.
- No fix integrated, no contract changed, no admission judgment made. The scoped deliverable is the eight mutation receipts, the pin-only qualification for M07, and exact-byte restoration evidence above.
