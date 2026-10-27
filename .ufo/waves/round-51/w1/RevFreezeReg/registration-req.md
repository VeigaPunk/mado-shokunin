# mado round 51 — registration freeze requirements

This checklist is a pre-dispatch gate. The L1 MUST complete and commit the registration, counter files, fixture/control artifacts, base receipts, and check receipts at the freeze commit before any wave is dispatched or any seat is scored. A seat-written counter is data, not a frozen predicate (corpus/QUALITY.md criterion 64).

## Required freeze checklist

- [ ] **Freeze identity and ordering:** Record the round-51 freeze commit and the round-51 claims path. Freeze only after w1 returns and before w2 dispatch. Record that no seat was scored before this freeze; if any seat was scored, do not reword or re-freeze its predicate.
- [ ] **Counter files present:** Both `quality/counters/c1-r51-ledger.py` and `quality/counters/c2-r51-dispatch-entry.py` exist in the freeze commit. Record both paths explicitly in registration. Run the criterion-64 presence command against the freeze commit and registration:

  ```sh
  for p in $(git show <freeze>:<registration> | grep -oE 'quality/(counters/)?[A-Za-z0-9_.-]+\.py' | sort -u); do git cat-file -e <freeze>:$p || echo MISSING $p; done
  ```

  Commit the command output with the freeze; it MUST contain no `MISSING` line. The command must cover every counter or checker path named by registration, not only these two counter paths.
- [ ] **Frozen predicates, byte-for-byte:** Include the complete frozen predicate sentence from `.ufo/waves/round-51/claims.md` for each counter, without paraphrase or alteration. Each counter's docstring MUST quote its corresponding predicate sentence byte-for-byte. Register the counter path and its digest at the freeze. No predicate wording may change after any seat has been scored; preserve the frozen sentence even if later work exposes a defect, and report the defect separately.
- [ ] **Controls and fixtures committed:** Commit the C1 and C2 do-nothing controls, their fixture definitions/inputs, expected outputs, and execution receipts at the freeze. Register the paths and identify which frozen counter scored each control. C1 controls must cover the claim's omission/uncovered, bad-pointer, empty-description, dangling-row, and base-absent cases; every control must MISS. C2 controls must cover the round-50 entry at the C2 path with two rows, round-49 candidate at the C2 path, held citations missing key tokens, and rows without pins; every control must MISS. Expected outputs and verdicts must agree with claims.md's kill rules; a control reading MET invalidates that claim's control set.
- [ ] **Base receipts committed:** Commit a receipt for each counter run at the round base `6ca8c559a4a3d6d361101592116eea2bc7452437`, with exact invocation, exit status, and full output. C1 base result MUST be `verdict=TARGET_MISSED ledger=absent`, exit 1; C2 base result MUST include `admitted=0/1 verdict=TARGET_MISSED`, exit 1. Register the receipt paths. These are required frozen controls, not inferred from source review.
- [ ] **Freeze evidence and binding:** The registration, counters, fixtures, expected-output files, base receipts, and presence-command output are all committed at the recorded freeze revision. Record hashes for the frozen counter bytes and bind all stated results to that revision. Confirm the committed paths exist at that revision (not merely in the working tree).
- [ ] **Dispatch gate:** Dispatch only after all checklist items pass and the freeze evidence is committed. If any required artifact is absent, any presence check prints `MISSING`, a base result differs, a required control does not MISS, or any docstring differs byte-for-byte, the freeze is incomplete and wave dispatch MUST wait.

## Claim anchors

- C1 frozen predicate: `.ufo/waves/round-51/claims.md` § C1 (`PRED-C1-r51`).
- C2 frozen predicate: `.ufo/waves/round-51/claims.md` § C2 (`PRED-C2-r51`).
- Presence/order rule: `corpus/QUALITY.md`, criterion 64.
- Prior registration form: `.ufo/waves/round-50/registration.md`.
