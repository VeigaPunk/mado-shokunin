# RevGateDelta50 — gate v3 delta review

## Verdict
The landed v3 scan adds seven standing findings across both scopes. Six are R1/R2/R3 fixture findings in wave artifacts; one R8 receipt finding is a real account-column disclosure. The v3 install also invalidates an unchanged round-48 gate-copy waiver. No newly flagged `corpus/`, `quality/`, or `tools/` file was found.

## Evidence
Ran the installed gate (sha256 `ffdc9d62c387050e016cf9d0eaacbf87f37d6647021cbd2c492eb6328dddbb61`) from a `git clone --shared` scratch clone at base `8ae47b957034ae21012bbf09173cca2c48be345e` and tip `b4a79843cc2545bbe800db9322e58f6e00436629`, with `--scope all` and `--scope ufo`. Base counts reproduce the w1 receipts exactly.

| scope | base counts R1/R2/R3/R4/R7/R8/R9/R5 | tip counts | total findings base → tip |
|---|---|---|---|
| all | 40/40/13/3/49/54/4/25 | 42/42/15/3/49/55/4/25 | 228 → 235 (+7) |
| ufo | 39/37/12/3/49/54/4/22 | 41/39/14/3/49/55/4/22 | 220 → 227 (+7) |

New rule counts by prefix/path:
- `.ufo/waves/round-48/w1/ExecSessionMarker/check-session-material.py`: R1=1 file (4 objects), R2=1 (3 rows), R3=1 (1 object). The file sha is unchanged (`82c9053a…`); its existing `gate-copy` waiver now rejects all three with `gate-source-mismatch`, because the installed gate source changed from v2 to v3. Waived total correspondingly falls 52/48 → 49/47. This is a waiver-invalidation regression introduced by the gate upgrade.
- `.ufo/waves/round-50/w1/ExecGateV3/check-session-material.py`: R1=1 (4), R2=1 (3), R3=1 (1). This is a copied gate artifact, not registered/sidecar-waived.
- `.ufo/waves/round-50/w1/ScrCorrectionsR50/receipts/d2-seat-state.txt`: R8=1 file, 2 `ls -l` owner/group rows. A shape-only check found two real-account rows; the account value is intentionally omitted. This is a genuine self-inflicted privacy finding.
- R7/R9: no newly flagged files. R1/R2/R3/R8 are the only rule deltas. No newly flagged `corpus/`, `quality/`, or `tools/` file (defect set: empty). Eight existing outside-`.ufo` findings at tip were identical at base, so are not new.

The two new round-50 finding files were introduced in `1b37a59e`; the round-48 file was not modified. Scan summaries and masked evidence are under `.ufo/waves/round-50/w2/RevGateDelta50/receipts/`.
