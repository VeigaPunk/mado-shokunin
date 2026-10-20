## Erratum R16-V1: tamper-control evidence label (appended 2026-10-20)

Correction only. No receipt is rewritten, deleted or re-measured here. Routed by
`corpus/lessons/round-16-verifier-spotcheck.md` §Routed defects (R16-V1, status-neutral).

Superseded text, `corpus/lessons/round-16.md` lines 131–132 at baseline `27cd06f`
(identical in the working tree):

```
  Input tamper control returns **2 snapshot_tampered**, retained in
  `frozen-tampered.json`. No fixture expectation was weakened.
```

What `evidence/frozen-tampered.json` records (sha256
`34a801bd1fad32521882eac5f8906cc56b83fc70c0ebe01cda578d01be9722fa`): `measured_commit`
`9dcf248993a9622a5b016edec0003187141745d2`; `action_gate_sha256`
`13d86fb0b34c21bccde0a8314875d66deb287624a9d971e4f4ed287496dcdb73`; command
`python3 -I tools/mado-action-plan.py --frozen /tmp/mado-r16-frozen-tamper-pt60l_e_`;
`exit` 2; stdout `MADO_PLAN: frozen_error` with detail
`expected.json pair 1/'denied_executable:sudo' is unreachable`; `expected_exit` 2;
`matched_exit` true. This is the M6 expected-pair defect at the pre-fix content. It fired
before any digest comparison, so the receipt is a `frozen_error`, not `snapshot_tampered`.
`matched_exit: true` compares the exit code only; the expected finding was not compared,
so the exit-2 agreement does not evidence `snapshot_tampered`.

Where `snapshot_tampered` is evidenced: `evidence/action-selftest-final.json`
(`measured_commit` `1e31681e76b5e7caadd1c749e18669a3632a1c3b`; `action_gate_sha256`
`226220ae41436506c048258aff15fff83577acf0ae71ffa955d585a18ba5aea3`; exit 0; stdout on
JSON line 12) contains:

- `SELFTEST PASS frozen-tampered-plan: want 2/snapshot_tampered got 2/snapshot_tampered`
- `SELFTEST PASS frozen-tampered-policy: want 2/snapshot_tampered got 2/snapshot_tampered`

with `SELFTEST_SUMMARY: 52/52 passed`. These are in-process fixture self-invocations at
the corrected content, checked on code and finding. They are not a retained CLI run
against a tampered snapshot.

Round-17 recut: `.ufo/waves/round-17/evidence/frozen-tampered-recut.json` is to be
produced by the round-17 lane. It will be a CLI run of
`tools/mado-action-plan.py --frozen <tampered copy>` at the corrected content, recording
command, exit, finding and input digests. It does not exist yet; do not cite it until it
does. `evidence/frozen-tampered.json` remains as retained red evidence and is not
overwritten.

No other round-16 LOG.md or SCORECARD.md entry carries this mislabel.
