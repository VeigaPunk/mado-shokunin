# ExecR2Check (w2, round 47) — seat status: COMPLETE

Findings: `.ufo/waves/round-47/w2/ExecR2Check.md` (the Report for this seat).

**Premise failure recorded:** the target `…/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv` no longer exists —
the round-47 L1 removed it at `2026-10-26 19:16:55` (receipt `.ufo/waves/round-47/receipts/r2-removed.txt`, committed
in `9bddd6ac`), before w2 launched. No copy survives anywhere on the host (`find` over lane and `/fast/scratch`).
Verification was therefore done by byte-reproducing the file from the committed harness
(`gen.py` + `stmt.cpp` + `diff.py` + `round-46/l1-draft/mado-devices.py`) and re-deriving every number.

**Result:** reproduction is bit-exact (`out.json.rows.tsv` sha256 `6573f76b…`, 3 282 451 bytes, 59 395 lines;
`out.json` `946ed60d…`; `cases.tsv` `fb355339…`; `stmt` `7606f8ef…`; g++ 16.2.1 / Python 3.14.8 as in
`receipts/versions.txt`). 61 of 62 independent checks pass; the single WRONG is the digest's prose count
"16 of the 21 categories are contiguous blocks" — the true count is 18 (`runs.txt`). Two further evidence defects
(the seat's `verify-locators.sh` is dead after the removal, exit 2; `analysis.txt` prints `dump_json_break_examples
… equal=False` while the digest says identical — a tuple/list artefact, JSON-normalised comparison equal) and two
residuals that can no longer be re-observed (`cmp` against the worktree copies, the `??` status line).

The digest line the L1 commits (§6) is correct number-for-number and carries no contiguity claim.

Artifacts here: `verify.py`, `verify.txt`, `repro-sha256.txt`, `runs.txt`, `cmp-rederived.txt`,
`derive-rerun-stdout.txt`, `diff-stdout.json`, `locators-rerun.txt`. Scratch removed.
