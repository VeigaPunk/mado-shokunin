# RevFrozenBlobs-r36 — the frozen-blob ledger, measured at the tip its own rule computes

Round 35 re-issued this ledger at `dff394109f3cc3d851309ad7c67dd3b35b46adf2`. The
non-author spot-check disputed that label (D4): `dff3941` is the lane-authored
round-34 docs commit, while the last round-34-labelled commit on the branch is
`6d754bd599caa7ab21c4c20b548c0fa83914ffce`, seventeen minutes later. This round
pins **one** definition instead of a literal: the round-34 lane tip is the newest
commit whose subject names `round-34`, computed at run time by
`quality/counters/c2-ledger.py` — never typed. Measured now the rule yields the
round-34 lane tip `6d754bd599caa7ab21c4c20b548c0fa83914ffce`.

This file supersedes `.ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md`, whose
label named `dff394109f3cc3d851309ad7c67dd3b35b46adf2` as the lane point. All seven
blob ids are identical at both revisions, so the round-34 conclusion (every frozen
blob byte-identical) stands and only the label moves.

Refs resolved (2026-10-25):

- Round-34 lane tip = `master` at that point = `6d754bd599caa7ab21c4c20b548c0fa83914ffce`
- Round-34 freeze `F` = `3420e827bd7b21b1374b23245526554ffd20d096`
- Round-34 data commit = `fa7ba11346116672352b5d41494141c5c4d738d0`
- Round-34 wave-evidence commit = `57622b8453f5ca6eb720dfbd1bc6b3285ec2a818`
- Round-34 docs commit = `dff394109f3cc3d851309ad7c67dd3b35b46adf2`

## 1. Frozen blob ids at the round-34 tip `6d754bd599caa7ab21c4c20b548c0fa83914ffce`

| Path | blob @ round-34 tip |
|---|---|
| `.ufo/waves/round-33/c1/count.py` | `4ab3db435dd2e396402d1d83039e35082f1138fe` |
| `.ufo/waves/round-33/c1/frozen.json` | `60d1094baa2992294533bae37e0990ae23077609` |
| `.ufo/waves/round-33/c2/count.py` | `df563528e725951b447ef31b324ec4b7d264e91b` |
| `.ufo/waves/round-34/c1/count.py` | `49089c186fb75f1bd2cc4c45c0161282ea6e8a46` |
| `.ufo/waves/round-34/c1/frozen.json` | `0bfe0d866c4e9a2d17da297a11dae389150b488b` |
| `.ufo/waves/round-34/c2/count.py` | `3a499a7eaa6cf5e861a5849992c37f1a7bede962` |
| `.ufo/waves/round-34/c2/frozen.json` | `ef3392b45f638513ff98dda95808f3f3938705e0` |

Re-derivation command (read-only git, no write):

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse \
  6d754bd599caa7ab21c4c20b548c0fa83914ffce:.ufo/waves/round-34/c1/count.py
```

## 2. What the repaired counter now checks

The computed round-34 tip is `6d754bd599caa7ab21c4c20b548c0fa83914ffce`.
Every tip-labelled 40-hex token in this file must equal the computed tip (a line
naming `supersedes` is exempt, and at least three tip lines are required, so the
exemption cannot launder the document); the row set must equal the frozen path set;
and every row's blob id must re-derive at the computed tip. The round-35 counter
checked none of that: it grepped the document for a hardcoded hash and re-derived
the ids from its own spec, so a stale label, a corrupted row and a deleted row all
still scored `TARGET_MET` (round-36 controls `c2-tip-stale`, `c2-blob-corrupt`,
`c2-blob-row-deleted`).
