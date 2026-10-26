# SKILL.md gate-registry row draft — `mado-session-material`

Target: `SKILL.md`, the `### Round 33 — published-axis gate and claim-verdict gate`
registry table (header at `SKILL.md:767`, existing row `mado-axis-scores` at
`SKILL.md:769`). Proposed row, same seven columns, same cell conventions
(exit map first, self-test spelling second, pinned values third):

| name | gate/probe | entry command | verdict map | self-test command / spelling | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| mado-session-material | gate | `python3 -I quality/check-session-material.py --repo . --rev REV` | 0 clean (`findings=0`); 1 findings (`findings>0`; waived findings are excluded and counted on `SESSION_MATERIAL_WAIVED: findings=N files=N`); 2 usage or git error | `python3 -I quality/check-session-material.py --selftest`; prints `SELFTEST: passed=N/N failed=N`; 0 clean, 1 failed | summary line `SESSION_MATERIAL: files=<n> findings=<n> rev=<40 hex>`; rules `R1_CLIENT_DUMP` `R2_PROC_TABLE` `R3_MONITOR_IDENT` `R4_HOME_LISTING`; waived marker `SYNTHETIC-MATERIAL v1 kind=<fixture\|gate-copy> rules=<csv> sha256=<64 hex>` as line 1 of a tracked `<path>.synthetic` sidecar plus a matching `<path> <sha256> <rules> kind=<kind>` line in `quality/session-material-waivers.txt` | reads committed blobs via `git cat-file`/`git show` (never the working tree); selftest writes only under `$TMPDIR` | mado |

Notes the integrator needs:

- `--selftest` count at this seat's copy: 34/34 (`receipts/00-selftest.txt`).
- `--no-waivers` reproduces the pre-marker gate byte for byte on
  `4d22eeb` (`receipts/01-baseline.txt` == `receipts/01b-baseline-copy-nowaivers.txt`),
  so installing the marker layer changes no verdict on a repo with no markers.
- The registry is read from the scanned revision, so a working-tree edit cannot
  waive anything; the registry path itself must stay outside `.ufo/`.
- A row for the registry file belongs beside the gate row only if the integrator
  wants the waiver list itself pinned; the 82-row triage that produced the
  first 49 waivers is `triage.tsv` in this seat.
