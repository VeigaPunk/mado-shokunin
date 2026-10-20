# RerunCensus — holds: requested source-register counts and new-row checks match

## Findings

No actionable discrepancy in the assigned census claims.

- **Counts hold.** Read-only parse of the `## Registry` rows from `git show 1f7f995:corpus/SOURCES.md` and `git show a4046a8:corpus/SOURCES.md` gives:

  | Revision | Rows | Tier A | Mined |
  |---|---:|---:|---:|
  | `1f7f995` | 98 | 91 | 81 |
  | `a4046a8` | 112 | 105 | 95 |

  The delta is +14 rows, +14 tier-A, +14 mined. All newly added IDs are S099–S112 (`corpus/SOURCES.md:111-124 @ a4046a8`); each row parses to 11 cells. The full register has no malformed row in either revision. Additional parse totals: baseline tiers A/B/C = 91/1/6, statuses mined/queued/rejected = 81/8/9; target tiers = 105/1/6, statuses = 95/8/9.

  Evidence: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 1f7f995:corpus/SOURCES.md` → `rows=98 tier_A=91 mined=81 malformed_rows=[]`; same command with `a4046a8` → `rows=112 tier_A=105 mined=95 malformed_rows=[]`; added-row parse → `added_ids=S099,...,S112`, `added_count=14`, `added_bad_columns=[]`, `new_rows_11_cells=14/14`. SHA-256 of the exact source blobs: `1f7f995` `ccaff539b159a7c0a431f873193e7d0969bda3d0996b1debad1cc4939315b67c`; `a4046a8` `ff69dcc8c76f55eb1968092fa7486e53a1024c855e7249702880b2a100664b1e`.

- **New `used-by` paths exist at `a4046a8`.** All 14 added rows name `corpus/knowledge/tripwire-precision-r20.md`; checked each against the exact commit with `git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -e a4046a8:<used-by-path>`. Output: `new_used_by_path_checks: missing=[] no_path_sentinel=[]`.

- **Requested validation completes cleanly apart from the reported cross-scope warnings.** Ran exactly `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`. Output contained only W04 duplicate-URL-across-scopes warnings for S030, S042, S045 and S097, followed by `mado ok /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`; no E-code finding was emitted. This is consistent with the validator's documented W04/E11 meanings (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:24-33`).

## Limits

This checks register counts, row shape, target-commit `used-by` existence and the requested validator only; it does not assess the sources' substantive authority or other round-20 claims. Four W04 warnings remain visible as non-fatal validation output.

## Installs

None.
