# AttackMistake — rendered report (round 14, w1)

The full findings live in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/AttackMistake.md`. That file is the sole authority; this summary is not.

- **Target:** `.ufo/waves/round-14/receipt.py`, SHA-256 `210d4c47…80563`, 245 lines, plus `ReceiptBuild.md`. Both read 2026-10-20.
- **Axes:** operability (the receipt can go red and gives no false provenance) and coverage/safety no-harm.
- **Not done:** no wrapper, gate or test was run, nothing outside the two granted paths was edited, and no tools were installed.

## Counterexamples

| ID | Severity | Finding | Smallest correction |
|---|---|---|---|
| CE1 | blocking | The gate digest header is not bound to the command that runs. `sh -c 'echo MADO_SELFTEST…'` would still get `status: ran` with real gate digests. | An argv allowlist: only `bash tools/mado-verify.sh --selftest` or `--no-live`. Anything else is refused with exit 2 and never runs. Add a selftest case. |
| CE2 | blocking | A plain `bash tools/mado-verify.sh` defaults to the live layer (`HEAD:tools/mado-verify.sh:84,3407-3408`). The draft persists all stdout, so output identities can reach evidence. A retained precedent: `.ufo/evidence/round-12/gate-live-after.txt:21,28`. | The same allowlist as CE1. |
| CE3 | should fix | `os.replace` overwrites any existing receipt, and refusals are written to the same path. That loses red history and contradicts the gate's rule "receipts are never overwritten" (`HEAD:tools/mado-verify.sh:1787,1902`; S7 at `:1245`). | Open the output with O_EXCL: if the file exists, exit 2 and write nothing. Add a selftest case. |
| CE4 | should fix | A refusal writes `exit=2`, which collides with the gate's own exit 2, "a failing --selftest" (`HEAD:tools/mado-verify.sh:12-13`). | On refusal write `exit=not-run` (or `wrapper-exit: 2`), never `exit=2`. |
| CE5 | should fix | The selftest only ever passes a full commit id, so the `commit:` field is never checked. A mutant that writes `('commit', revision)` survives. | Add a test that runs with `--revision HEAD` and asserts a 40-hex `commit:`. |
| CE6 | cheap | The wrapper is untracked and does not pin its own digest (QUALITY 13). | Add a `wrapper-sha256:` header line. |

Tradeoffs that are not defects: no post-run re-hash, no timestamp (date the receipt in the report line instead), inherited stdin, and untested signal mapping.

## Grounding and credit

- R13-V3 (`corpus/lessons/round-13-verifier-spotcheck.md:205`) is a conformance gap against the existing QUALITY criteria **7, 9 and 13**. Do not mint a new criterion.
- Count it as a correction only, not as score: `SCORECARD.md:482-483` calls R13 items corrections and "not a third axis claim". The selftest count goes into neither the C2 3/3 nor the gate's own selftest total.
- The wrapper does not address R13-V1. On R13-V2: the wrapper refuses once the worktree differs from the named revision, so two wrapper receipts can never show byte-identical output across before/after revisions. Cross-revision comparison belongs to `measure.py`, which extracts each revision with `git show`. `boundary.readonly` stays a within-run fact.

## Red-before / green-after evidence

The minimal set is E1 + E2 + E5. Add E3 if the wrapper is to be claimed as "shown able to fail".

- **E1:** the round-13 `gate-selftest.txt` has 0 revision/digest header lines (observed, red). The round-14 receipt should show a 40-hex `commit:` and two equal gate digests (green, L1-owned).
- **E2:** the wrapper `--selftest`, including the mismatch case and the CE1, CE3, CE4 and CE5 cases.
- **E3:** three single-edit mutants run through tameshi `mutate-and-run.sh` with suite `python3 "$MUTANT" --selftest`: drop the digest compare, record the unresolved revision, drop the allowlist. All three must be KILLED.
- **E4 (optional):** one real-repo refusal before the gate commit, written to a distinct path. The precondition holds now: worktree `b50dae25…` differs from HEAD `037b05dc…`, both observed.
- **E5:** re-derive both digests independently with `git show <commit>:<path> | sha256sum`.

## Post-decision status (appended 2026-10-20)

L1 rejected and removed `receipt.py` (`ReceiptBuild.md:1,6`). CE1–CE6 and E2–E5 now have no target and must not be run or claimed. R13-V3 stays open provenance debt; E1's red observation still stands. Nothing is credited to C2.
