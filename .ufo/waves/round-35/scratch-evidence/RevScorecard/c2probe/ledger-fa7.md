# RevFrozenBlobs — round 35 re-issue, measured at the round-34 lane tip

The round-34 artifact `.ufo/waves/round-34/w1/reports/RevFrozenBlobs.md` measured its
blob table at `fa7ba11346116672352b5d41494141c5c4d738d0` and labelled that commit the
lane tip. The round-34 lane tip is `dff394109f3cc3d851309ad7c67dd3b35b46adf2`
(`master`, pushed). The conclusion — PROVEN, not amended — stands: every frozen blob is
byte-identical at the real tip too, and the round-34 closure re-verified all seven
there. The artifact's own **label** was stale by one commit. This is the re-issue:
the same seven paths, measured and named at the real tip.

Refs resolved (2026-10-24):

- Round-34 lane tip = `master` = `dff394109f3cc3d851309ad7c67dd3b35b46adf2`
- Round-34 freeze `F` = `3420e827bd7b21b1374b23245526554ffd20d096`
- Round-34 data commit = `fa7ba11346116672352b5d41494141c5c4d738d0`
- Round-34 wave-evidence commit = `57622b8453f5ca6eb720dfbd1bc6b3285ec2a818`
- Round-34 docs commit = `dff394109f3cc3d851309ad7c67dd3b35b46adf2`

## 1. Frozen blob ids at the round-34 tip `dff394109f3cc3d851309ad7c67dd3b35b46adf2`

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
  dff394109f3cc3d851309ad7c67dd3b35b46adf2:.ufo/waves/round-34/c1/count.py
```

## 2. Per-path history on `master`

Each frozen path was written once, at its freeze commit, and no later commit on
`master` touched it — so no write-then-revert is possible.

- `.ufo/waves/round-33/c1/count.py` → `9a46ccf3282117f960b8d53cd71599a91f388ee3`
- `.ufo/waves/round-33/c1/frozen.json` → `9a46ccf3282117f960b8d53cd71599a91f388ee3`
- `.ufo/waves/round-33/c2/count.py` → `9a46ccf3282117f960b8d53cd71599a91f388ee3`
- `.ufo/waves/round-34/c1/count.py` → `3420e827bd7b21b1374b23245526554ffd20d096`
- `.ufo/waves/round-34/c1/frozen.json` → `3420e827bd7b21b1374b23245526554ffd20d096`
- `.ufo/waves/round-34/c2/count.py` → `3420e827bd7b21b1374b23245526554ffd20d096`
- `.ufo/waves/round-34/c2/frozen.json` → `3420e827bd7b21b1374b23245526554ffd20d096`

## 3. Verdict

PROVEN at the real round-34 tip `dff394109f3cc3d851309ad7c67dd3b35b46adf2`: every
frozen counter path was written once, at its freeze commit, and no later commit on
`master` touched it. The round-34 artifact's **label**, not its conclusion, was the
defect routed by the round-34 closure. This file is the re-issue; it does not rewrite
the round-34 artifact, which stays in place as the record of what it measured.

Round-34 lane tip = fa7ba11346116672352b5d41494141c5c4d738d0
