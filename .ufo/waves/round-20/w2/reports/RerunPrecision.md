# RerunPrecision — holds: recorded precision receipts reproduce exactly with no per-case divergence

Axes: counter reproducibility, receipt provenance, and final-commit behavior.

## Findings

- **All eight requested counters ran from the scratch clone.** I cloned the lane to `/tmp/mado-r20w2-RerunPrecision`, removed its origin, and copied the counter bytes from commit `28c68378eccbd5f227cdc28a62406ff390e3540a` to `tw-precision-rerun.py` there. Its SHA-256 is `bd3bdc23747a6d8f195e69528f532988202db4ab3476d141a8ff46871e42a8e7`. Command template: `python3 -I /tmp/mado-r20w2-RerunPrecision/.ufo/waves/round-20/tw-precision-rerun.py REV [--heldout]` (each output was saved at the corresponding path below).

  | Target | Scored | Heldout | Scored output SHA-256 | Heldout output SHA-256 |
  |---|---:|---:|---|---|
  | `1f7f995` | 29/175, score 1.6571 | 0/12, score 0.0 | `aee664097db7797b49f8ffb3627a0ce8b8b4b485b9f47a4d9a52a1eede27099e` (`/tmp/mado-r20w2-RerunPrecision/rerun-precision-1f7f995.json:1`) | `e24c9e463e7a68508439a625543dc15cba7d9195cac20995597c955363160b84` (`/tmp/mado-r20w2-RerunPrecision/rerun-precision-heldout-1f7f995.json:1`) |
  | `9c54c56` | 110/175, score 6.2857 | 3/12, score 2.5 | `de4fed29f197350477f6dd365780ffb11fc41a67413db8ee97808b8da86fa3a6` (`/tmp/mado-r20w2-RerunPrecision/rerun-precision-9c54c56.json:1`) | `b93eaa4b91966da405f7281b0df679a66a57a47cf4dc0bdcb81dde16d9fbd50b` (`/tmp/mado-r20w2-RerunPrecision/rerun-precision-heldout-9c54c56.json:1`) |
  | `28c6837` | 172/175, score 9.8286 | 0/12, score 0.0 | `dec728fe803ea32ecffee4bf86c223c79a90f4f85fd5279d036338ad2140ebbe` (`/tmp/mado-r20w2-RerunPrecision/rerun-precision-28c6837.json:1`) | `69a998a83cb4f275f48b9b53338186e3de3d8cdd4061e39a42ec42c58ee6f4b7` (`/tmp/mado-r20w2-RerunPrecision/rerun-precision-heldout-28c6837.json:1`) |
  | `a4046a8` | 172/175, score 9.8286 | 0/12, score 0.0 | `e256953ebb6f99d4641e342e26b5119b5cfe4244acc3fc15888245b05c132a06` (`/tmp/mado-r20w2-RerunPrecision/rerun-precision-a4046a8.json:1`) | `a866cd4b6b319535183721ac7d053e64d475f3d93f3a4d7aeb6467f03695eb91` (`/tmp/mado-r20w2-RerunPrecision/rerun-precision-heldout-a4046a8.json:1`) |

  The JSON results report target-tool SHA-256 values of `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d` (`1f7f995`), `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd` (`9c54c56`), and `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c` (`28c6837` and `a4046a8`).

- **No case differs from any recorded receipt body.** Parsed each receipt's complete JSON body (line 2) and compared it with the rerun JSON for its `argv`: all five available receipts are exact body matches, with zero differing cases. In each header (line 1), `measured_commit` is `28c68378eccbd5f227cdc28a62406ff390e3540a`; `tool` is `.ufo/waves/round-20/tw-precision.py`; and `tool_sha256` is `bd3bdc23747a6d8f195e69528f532988202db4ab3476d141a8ff46871e42a8e7`, equal to `sha256sum` of `git show <measured_commit>:<tool>` from the clone. The comparison output was `body_equal=True differing_cases=0 header_sha_matches_git_show=True` for each of:
  - `evidence/precision-1f7f995.txt:1-3` (receipt SHA-256 `9fbef2c79dfbb9f29b9fd36d70661973fdcded3372ac0e99666c74127bdf50ff`)
  - `evidence/precision-9c54c56.txt:1-3` (receipt SHA-256 `dbcff6bbeb7db30260f64c4a63e4bc5331b2a4fb93ac6d9ef4c43776b256e145`)
  - `evidence/precision-final.txt:1-3` (receipt SHA-256 `629724dce770aad74a4e268fc36a2061d93fcf5f3c8bd77beee777d61f80e98c`)
  - `evidence/precision-heldout-1f7f995.txt:1-3` (receipt SHA-256 `3675153ec34efd28872b487f7c6341a830f7c7d299d4a52c5f3efcf164c02718`)
  - `evidence/precision-heldout-final.txt:1-3` (receipt SHA-256 `2868c3c9c5aca8a63ab38c4077a518ef1b49048cf11d1cea3218028f2336d9cb`).

- **Final behavior is identical at `28c6837` and `a4046a8`.** Case-object comparison found 0 differences across 175 scored cases and 0 differences across 12 heldout cases; both runs report the same target-tool SHA-256 above. Thus, although there is no `a4046a8`-named receipt, the final rerun matches the available final (`28c6837`) receipt's cases.

## Limits

- The evidence directory contains no `precision-heldout-9c54c56.txt` and no `a4046a8`-specific precision receipt. The `9c54c56` heldout counter was rerun (3/12), but cannot be compared to a corresponding recorded body; the `a4046a8` results were compared case-by-case with `28c6837` because their target-tool hashes are identical.
- This assignment covered counter reproduction and receipt provenance, not call-site/definition/diagnostic review.

## Installs

None.
