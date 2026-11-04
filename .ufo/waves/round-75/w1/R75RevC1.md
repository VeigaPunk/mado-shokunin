# R75RevC1 — C1 falsification review

Full findings: [R75RevC1/review.md](R75RevC1/review.md).
Evidence: [counter.txt](R75RevC1/counter.txt), [probes.txt](R75RevC1/probes.txt), [probes.py](R75RevC1/probes.py), [absent-candidate.txt](R75RevC1/absent-candidate.txt).

- **P2:** uppercase fixture's always-fail expectation is wrong for valid digits-only challenges: forced `0123456789012345` yields genuine matching echo, M-Z pass, TARGET_MET, rc 0. Probability `(10/16)^16 ≈ 0.05421%`; the counter would incorrectly mark the conforming harness wrong. Frozen counter lines 94-95/304-308; successor line 225.
- **P2:** absent candidate promises measured miss `correct=absent`, exit 1, but frozen counter lines 205-209/282 raise SetupError; observed rc 2 and no contract line when measuring the base revision.
- **Advisory:** right/liar-success are behavior-identical before and after M-Z mutation, including exit 0 on the mutant's reported assertion failure; the distinct liar label adds no behavioral separator.

Independent frozen counter reproduced cases=11 correct=11 base_correct=6 TARGET_MET, rc 0. No absent-echo bypass, ambient nonce inheritance, pin bypass, or verdict/exit divergence observed in scoped probes. Pin freezes r72 generation only; witness= describes original selftest, not assertion truth. Parser scores mz only, so its green result alone does not verify the whole contract. LSP unavailable; production integration and full no-harm gate unexercised. No production edits or tool installations. Scratch removed after preserving receipts.

C1: survives with defects
