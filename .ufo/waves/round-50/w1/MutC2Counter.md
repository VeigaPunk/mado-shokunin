# MutC2Counter — round 50 w1
+
Verdict: **inconclusive / not run**. The requested target/control pairing does not identify a round-50 frozen counter: claims.md says the session-material gate v3 predicate freezes only after w1 and no round-50 frozen counter is scored during w1. The carried item instead identifies the round-49 PRED-C2-r49 bind-entry counter and its controls.
+
Evidence and hashes:
+- `quality/counters/c2-r49-bind-entry.py` SHA-256: `bc171714c5349dbe980b84f5c434126965cc8a6e8226704c28604d10cff28c69`.
+- Round-49 control summary `.ufo/waves/round-49/w1/ExecControlsC2/receipts/controls.txt` SHA-256: `afc023b08b031d5bb1c517b0d940cc56556ff6e6581958ce73f95bdd6d6ddb2f`.
+- Counter docstring describes clauses `a` through `j` and `r`; the carried target says `a-i` and `r`, while the original mutation list names eight weakenings. No defined one-mutant-per-clause mapping is supplied.
+- `score.py` explicitly runs the w1 draft at `ExecCounterC2/c2-r49-bind-entry.py` using materialized control revisions and inherited compositor socket state. It is not a harness for substituted counter bytes; clause `r` depends on a live read-only compositor socket. I did not invoke another runtime or score controls with an unvalidated substitute harness.
+
No mutant was run, so there is no killed/survived result and no restoration claim. The pristine counter bytes were not modified; their measured hash remains the reference above. The mapping/target requires resolution before a valid probe can be recorded.
