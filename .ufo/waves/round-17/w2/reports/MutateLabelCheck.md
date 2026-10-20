# MutateLabelCheck — round 17 wave 2

## Result

**Attack failed for all four isolated, single-defect mutants: 4 killed, 0 survived, 0 inconclusive.** Each mutant reduced the seven-claim detector from `EXPECT_SUMMARY: 7/7` to `6/7`; every restored copy returned to `7/7` with byte-identical stdout/stderr and the same exit status as its pristine run. This is scoped mutation evidence, not an integration or round-admission judgment and not proof of exhaustive checker correctness.

Axes: C1 calibration (observed outcome versus quoted expectation; measured revision attribution), detector sensitivity (preserve the got-side green control), and isolation/reversibility. No contract, claims, fixtures, or production checker was changed.

Installs/updates: **none**. No delegation, commits, git mutation, device/compositor probes, or additional runtime invocation.

## Scope and bounded detector

- Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
- Assignment names lane HEAD `988b858bd6049bc709807534fd725c05264f7e60`; the exact file bytes actually probed are identified by the hashes below.
- Scratch: `/tmp/MadoR17-MutateLabelCheck.HmiFIA`; separate subdirectories named for each mutant below.
- Copied `label-check.py` and `label-claims.json`. Claims stayed byte-for-byte unchanged. Repository-relative doc/receipt paths resolve through one shared scratch-only adapter: replace original `repo_root()` lines 63-72 with `return "/home/vgpnk/Projects/shokunin/mado-shokunin"`. This avoids /tmp repository discovery; it does not change claim checking or either expectation. Each checker still defaults to its sibling copied claims file, and the copied claims path was also passed explicitly.
- Effective argv for every pristine/mutated/restored run: `python3 -I /tmp/MadoR17-MutateLabelCheck.HmiFIA/<mutant>/label-check.py /tmp/MadoR17-MutateLabelCheck.HmiFIA/<mutant>/label-claims.json`.
- Working directory: corresponding scratch mutant directory. Per-process bound: 60 seconds; no timeout occurred. Four independent runs were launched concurrently per phase; phases were ordered pristine → mutate → restored.
- Entire supplied child environment: `PATH=/usr/bin:/bin`, `HOME=/tmp/MadoR17-MutateLabelCheck.HmiFIA`, `LC_ALL=C`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_OPTIONAL_LOCKS=0`, `GIT_TERMINAL_PROMPT=0`. Receipt/document retrieval used the checker's read-only `git show` calls.
- Detector: require `EXPECT_SUMMARY: 7/7 claims met their declared expectation` for pristine/restored, and observe a reduction below 7/7 for a killed mutant. All 12 executions exited **1** because the claims intentionally include red controls. Exit 1 by itself is therefore neither a baseline failure nor a kill signal; there was no `COULD_NOT_EVALUATE` output. All stderr was empty.

## Outcomes

| Mutant | Pristine EXPECT_SUMMARY | Mutated EXPECT_SUMMARY | Restored EXPECT_SUMMARY | Exit sequence | Verdict |
| --- | --- | --- | --- | --- | --- |
| M1-substring | 7/7 | 6/7 | 7/7 | 1 / 1 / 1 | killed |
| M2-drop-got-side | 7/7 | 6/7 | 7/7 | 1 / 1 / 1 | killed |
| M3-drop-measured-commit | 7/7 | 6/7 | 7/7 | 1 / 1 / 1 | killed |
| M4-accept-want-side | 7/7 | 6/7 | 7/7 | 1 / 1 / 1 | killed |

### Pristine output (actual, identical in all four runs)

```text
LABEL R16-V1-red MISMATCH (receipt outcome ['frozen_error'] lacks 'snapshot_tampered')
LABEL frozen-match-green ok (receipt outcome carries 'frozen_match')
LABEL spotcheck-selftest-final-green ok (receipt outcome carries 'snapshot_tampered')
LABEL want-side-only-mutant MISMATCH (receipt outcome ['frozen_error'] lacks 'snapshot_tampered')
LABEL superseded-commit-mutant MISMATCH (receipt measured_commit '9dcf248993a9622a5b016edec0003187141745d2' is not '1e31681')
LABEL honest-red-green ok (receipt outcome carries 'frozen_error')
LABEL recut-green ok (receipt outcome carries 'snapshot_tampered')
LABEL_SUMMARY: 4/7
EXPECT_SUMMARY: 7/7 claims met their declared expectation
```

Each pristine run had stderr `""`, exit 1, and no timeout.

### M1-substring: Raw-receipt substring acceptance

- Mutation anchor: Original label-check.py:136; scratch:127.
- Change: `if token in acc:` → `if token in rtext:`
- Expected detector: `want-side-only-mutant` must change from MISMATCH to ok, lowering EXPECT_SUMMARY.
- Existing control anchor: `.ufo/waves/round-17/label-claims.json:17-21; label-fixtures/want-only.json:5`.
- Actual mutated stdout:

```text
LABEL R16-V1-red MISMATCH (receipt outcome ['frozen_error'] lacks 'snapshot_tampered')
LABEL frozen-match-green ok (receipt outcome carries 'frozen_match')
LABEL spotcheck-selftest-final-green ok (receipt outcome carries 'snapshot_tampered')
LABEL want-side-only-mutant ok (receipt outcome carries 'snapshot_tampered')
LABEL superseded-commit-mutant MISMATCH (receipt measured_commit '9dcf248993a9622a5b016edec0003187141745d2' is not '1e31681')
LABEL honest-red-green ok (receipt outcome carries 'frozen_error')
LABEL recut-green ok (receipt outcome carries 'snapshot_tampered')
LABEL_SUMMARY: 5/7
EXPECT_SUMMARY: 6/7 claims met their declared expectation
```

- Actual stderr: `""`; exit 1; no timeout. Verdict: **killed**.

### M2-drop-got-side: Drop got-side outcome extraction

- Mutation anchor: Original label-check.py:84; scratch:75.
- Change: Delete `acc.update(GOT_SIDE.findall(v))`.
- Expected detector: `spotcheck-selftest-final-green` must change from ok to MISMATCH, lowering EXPECT_SUMMARY.
- Existing control anchor: `.ufo/waves/round-17/label-claims.json:12-16; action-selftest-final.json@4bfb2363afd6e05d079127d8f91e57f01bbdca92`.
- Actual mutated stdout:

```text
LABEL R16-V1-red MISMATCH (receipt outcome ['frozen_error'] lacks 'snapshot_tampered')
LABEL frozen-match-green ok (receipt outcome carries 'frozen_match')
LABEL spotcheck-selftest-final-green MISMATCH (receipt outcome [] lacks 'snapshot_tampered')
LABEL want-side-only-mutant MISMATCH (receipt outcome [] lacks 'snapshot_tampered')
LABEL superseded-commit-mutant MISMATCH (receipt measured_commit '9dcf248993a9622a5b016edec0003187141745d2' is not '1e31681')
LABEL honest-red-green ok (receipt outcome carries 'frozen_error')
LABEL recut-green ok (receipt outcome carries 'snapshot_tampered')
LABEL_SUMMARY: 3/7
EXPECT_SUMMARY: 6/7 claims met their declared expectation
```

- Actual stderr: `""`; exit 1; no timeout. Verdict: **killed**.

### M3-drop-measured-commit: Omit measured revision validation

- Mutation anchor: Original label-check.py:129-133; scratch:120-124.
- Change: Delete the single optional measured_commit validation block (including its local assignment).
- Expected detector: `superseded-commit-mutant` must change from MISMATCH to ok, lowering EXPECT_SUMMARY.
- Existing control anchor: `.ufo/waves/round-17/label-claims.json:22-26; frozen-tampered.json@1e31681e76b5e7caadd1c749e18669a3632a1c3b`.
- Actual mutated stdout:

```text
LABEL R16-V1-red MISMATCH (receipt outcome ['frozen_error'] lacks 'snapshot_tampered')
LABEL frozen-match-green ok (receipt outcome carries 'frozen_match')
LABEL spotcheck-selftest-final-green ok (receipt outcome carries 'snapshot_tampered')
LABEL want-side-only-mutant MISMATCH (receipt outcome ['frozen_error'] lacks 'snapshot_tampered')
LABEL superseded-commit-mutant ok (receipt outcome carries 'frozen_error')
LABEL honest-red-green ok (receipt outcome carries 'frozen_error')
LABEL recut-green ok (receipt outcome carries 'snapshot_tampered')
LABEL_SUMMARY: 5/7
EXPECT_SUMMARY: 6/7 claims met their declared expectation
```

- Actual stderr: `""`; exit 1; no timeout. Verdict: **killed**.

### M4-accept-want-side: Accept want-side as an observed outcome

- Mutation anchor: Original and scratch label-check.py:42.
- Change: `r"\bgot -?\d+/([a-z_]+)"` → `r"\b(?:got|want) -?\d+/([a-z_]+)"`
- Expected detector: `want-side-only-mutant` must change from MISMATCH to ok, lowering EXPECT_SUMMARY.
- Existing control anchor: `.ufo/waves/round-17/label-claims.json:17-21; label-fixtures/want-only.json:5`.
- Actual mutated stdout:

```text
LABEL R16-V1-red MISMATCH (receipt outcome ['frozen_error'] lacks 'snapshot_tampered')
LABEL frozen-match-green ok (receipt outcome carries 'frozen_match')
LABEL spotcheck-selftest-final-green ok (receipt outcome carries 'snapshot_tampered')
LABEL want-side-only-mutant ok (receipt outcome carries 'snapshot_tampered')
LABEL superseded-commit-mutant MISMATCH (receipt measured_commit '9dcf248993a9622a5b016edec0003187141745d2' is not '1e31681')
LABEL honest-red-green ok (receipt outcome carries 'frozen_error')
LABEL recut-green ok (receipt outcome carries 'snapshot_tampered')
LABEL_SUMMARY: 5/7
EXPECT_SUMMARY: 6/7 claims met their declared expectation
```

- Actual stderr: `""`; exit 1; no timeout. Verdict: **killed**.

## Restoration and byte evidence

Restoration ran in a `finally` block immediately after the mutated detector batch, rewriting each scratch checker from the saved shared pristine bytes. The restored detector then ran separately on every copy. All four restored outputs exactly matched their respective pristine outputs; the following actual restored stdout was identical in every run:

```text
LABEL R16-V1-red MISMATCH (receipt outcome ['frozen_error'] lacks 'snapshot_tampered')
LABEL frozen-match-green ok (receipt outcome carries 'frozen_match')
LABEL spotcheck-selftest-final-green ok (receipt outcome carries 'snapshot_tampered')
LABEL want-side-only-mutant MISMATCH (receipt outcome ['frozen_error'] lacks 'snapshot_tampered')
LABEL superseded-commit-mutant MISMATCH (receipt measured_commit '9dcf248993a9622a5b016edec0003187141745d2' is not '1e31681')
LABEL honest-red-green ok (receipt outcome carries 'frozen_error')
LABEL recut-green ok (receipt outcome carries 'snapshot_tampered')
LABEL_SUMMARY: 4/7
EXPECT_SUMMARY: 7/7 claims met their declared expectation
```

| Mutant | Restored stdout/stderr/exit match pristine | Before/after scratch checker SHA-256 |
| --- | --- | --- |
| M1-substring | true | `ca07da5e561d02f65a9808aa013fd7c8b962995a93569042b9f714e91743c293` |
| M2-drop-got-side | true | `ca07da5e561d02f65a9808aa013fd7c8b962995a93569042b9f714e91743c293` |
| M3-drop-measured-commit | true | `ca07da5e561d02f65a9808aa013fd7c8b962995a93569042b9f714e91743c293` |
| M4-accept-want-side | true | `ca07da5e561d02f65a9808aa013fd7c8b962995a93569042b9f714e91743c293` |

Mutated checker SHA-256 values (captured before running the mutants):

| Mutant | SHA-256 |
| --- | --- |
| M1-substring | `854001d9b7f28aa2e58ec365baa8a363ae7d2e548bf473f0fcc0f3e1e6a6b135` |
| M2-drop-got-side | `ef33ff82452b9f3f9d3b120df149ef48efa2d07b95548f8ce416e4025306bec3` |
| M3-drop-measured-commit | `af382ff342770bdf0c469aa562c6d4f21e1771e0f7fcf105e1da939ee9bf5e72` |
| M4-accept-want-side | `d5d15f187cf0d975d174f480bd92c0a0e1ecc0c686a41d3ad31a0d8529e2c4cb` |

Source and claims byte identities:

- Lane checker, before and after: `b890a5ca771bfbe6af68d07779ea2a9d5f73a5f6481091bb5b5a7f4663a41505`.
- Lane claims, before and after: `2e28fc841f466b5e1bda4dfcf36a79c05af349ccf836f6d4fd226569f79059d1`.
- Every copied claims file has the same claims hash above after the probe; claims were never mutated.
- Adapted pristine scratch checker, before each mutation and after every restoration: `ca07da5e561d02f65a9808aa013fd7c8b962995a93569042b9f714e91743c293`.

Actual final `sha256sum` output:

```text
ca07da5e561d02f65a9808aa013fd7c8b962995a93569042b9f714e91743c293  /tmp/MadoR17-MutateLabelCheck.HmiFIA/M1-substring/label-check.py
ca07da5e561d02f65a9808aa013fd7c8b962995a93569042b9f714e91743c293  /tmp/MadoR17-MutateLabelCheck.HmiFIA/M2-drop-got-side/label-check.py
ca07da5e561d02f65a9808aa013fd7c8b962995a93569042b9f714e91743c293  /tmp/MadoR17-MutateLabelCheck.HmiFIA/M3-drop-measured-commit/label-check.py
ca07da5e561d02f65a9808aa013fd7c8b962995a93569042b9f714e91743c293  /tmp/MadoR17-MutateLabelCheck.HmiFIA/M4-accept-want-side/label-check.py
2e28fc841f466b5e1bda4dfcf36a79c05af349ccf836f6d4fd226569f79059d1  /tmp/MadoR17-MutateLabelCheck.HmiFIA/M1-substring/label-claims.json
2e28fc841f466b5e1bda4dfcf36a79c05af349ccf836f6d4fd226569f79059d1  /tmp/MadoR17-MutateLabelCheck.HmiFIA/M2-drop-got-side/label-claims.json
2e28fc841f466b5e1bda4dfcf36a79c05af349ccf836f6d4fd226569f79059d1  /tmp/MadoR17-MutateLabelCheck.HmiFIA/M3-drop-measured-commit/label-claims.json
2e28fc841f466b5e1bda4dfcf36a79c05af349ccf836f6d4fd226569f79059d1  /tmp/MadoR17-MutateLabelCheck.HmiFIA/M4-accept-want-side/label-claims.json
b890a5ca771bfbe6af68d07779ea2a9d5f73a5f6481091bb5b5a7f4663a41505  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/label-check.py
2e28fc841f466b5e1bda4dfcf36a79c05af349ccf836f6d4fd226569f79059d1  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/label-claims.json
```

## Surviving mutants and limits

Survivors: **none**. Concrete coverage controls exercised: want-only false acceptance (M1/M4), missing got-side extraction (M2), and superseded measured-commit acceptance (M3). No counterexample to those four checked behaviors was found; the seven-claim detector rejected every seeded defect. No additional verifier or broader soundness claim is implied.

Only this report was written in the lane; all behavior mutations were confined to restored /tmp copies.
