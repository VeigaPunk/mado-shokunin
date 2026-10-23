# ReRunC2Tip — round 24 wave 2: C2 counter re-run at tip 39c5963

Seat: MadoR24.ReRunC2Tip (leaf, no dispatch). Lane: /home/vgpnk/Projects/shokunin/mado-shokunin.
Attack target: the wave-1 claim that the frozen C2 counter gives `mismatches=0/12` and that the
counter/manifest are unchanged since freeze 4f21d995.

## What I ran

- Freeze diff (read-only, in lane): `git diff 4f21d995 39c596307333b8ca0a1e42b3f3b9a748bb8b208b -- .ufo/waves/round-24/c2/` — **empty** (no stat lines, no hunks).
- Working-tree hashes: `sha256sum` → count.py `a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8`, manifest.json `e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02`. Both equal the `counter_sha256`/`manifest_sha256` embedded in the frozen receipt `.ufo/waves/round-24/evidence/c2-after-81955bd5.txt`, and the manifest hash also appears in the SCORECARD prose at tip.
- Single sanctioned re-run (one run total, no polling, no `--keep`/`--json`):
  `timeout 900 python3 -I .ufo/waves/round-24/c2/count.py 39c596307333b8ca0a1e42b3f3b9a748bb8b208b`
  started 2026-10-23T01:09:37-03:00, finished 01:14:33-03:00, wall 296.78 s, counter_exit=0.

## Re-run output (tip) vs frozen receipt (81955bd5)

All 12 rows identical in `stated`/`observed`/OK/`exit`:

| capability | stated=observed | OK | exit | parity with receipt |
|---|---|---|---|---|
| sources registry | works | OK | 0 | identical |
| verdict gate (live + file plane) | works | OK | 0 | identical |
| hermetic self-test | works | OK | 0 | identical |
| mutation regression with re-cut | works | OK | 0 | identical |
| post-hoc transcript tripwire | works | OK | 0 | identical |
| tripwire frozen replay (gate entry) | works | OK | 1 | identical |
| landedness check | works | OK | 0 | identical |
| tripwire evidence marker | fails | OK | 0 | identical |
| harness fail-closed check | works | OK | 0 | identical |
| tripwire reached-body sweep | works | OK | 0 | identical |
| detector removal-side guard | works | OK | 0 | identical |
| artifact-only assessment integrity | works | OK | 0 | identical |

Summary line: `mismatches=0/12 revision=39c596307333b8ca0a1e42b3f3b9a748bb8b208b manifest_sha256=e02c76d1… counter_sha256=a2809501…`. The only delta vs the receipt is the `revision=` field (81955bd5 → 39c59), as expected for a tip re-run; the intentional exit=1 row (tripwire frozen replay) and the intentional `fails` row (tripwire evidence marker) reproduce exactly, so the counter is not just rubber-stamping `works`.

## Supporting checks

- Ancestry: `merge-base --is-ancestor` confirms 4f21d995 and 81955bd5 are both ancestors of 39c59; log shows 464a024 → 81955bd (C2 table) → cf86f9e (C1 route) → 39c59 (repairs), i.e. the two post-receipt commits did not disturb any frozen command's behavior.
- Manifest sanity: schema `mado-r24-c2-manifest-v1`, exactly 12 capability rows matching the receipt's row names.
- Tip SCORECARD: `### Capability status (round 24 re-demonstration)` at line 1566 with the 12-row status table (11 `works`, 1 `fails`), matching what the counter parsed.
- Counter hygiene (read of frozen source before the run): lane is touched only via `git rev-parse`/`git archive` (read-only); work happens in a unique `tempfile.mkdtemp` under `/fast/scratch/hyaku/mado-r24/c2`; children run with RLIMIT_AS 4 GiB and GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE stripped; run dir self-removed in `finally` — no `run-39c59630-*` directory remains after the run. (One unrelated dir, `run-46981925-ao_gv88w`, was present in the shared scratch afterward: a different revision prefix, i.e. a concurrent seat's in-flight run, not this invocation's.)

## Findings by severity

- None. No defect found within this seat's scope: the frozen counter re-run at tip reproduces the wave-1 receipt byte-for-byte modulo the revision field, and the freeze diff since 4f21d995 is empty.

VERDICT: holds — `mismatches=0/12` at 39c5963 confirmed by re-run; manifest/counter sha256 unchanged since 4f21d995.

## Residual risk and verification gaps

- Nondeterminism window: one run is sanctioned, so a flaky timing-sensitive capability could in principle pass here and fail elsewhere; no evidence of flakiness in this run (all exits and outputs matched the receipt exactly).
- The counter judges exit code + regex only; parity is observational, not a semantic re-derivation of each capability.
- `--json`/`--keep` modes and the `MADO_LANE` override were not exercised (out of scope; default lane path used).
- Scratch dir is shared with other concurrent wave-2 runs; unique mkdtemp naming means no collision was possible, but I only verified my own run left nothing behind.

Tooling directive: no tools installed or updated this session.
