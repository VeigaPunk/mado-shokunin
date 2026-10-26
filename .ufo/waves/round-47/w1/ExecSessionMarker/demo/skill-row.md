# SKILL.md gate-registry row — `mado-session-material` (replaces the round-46 row)

Target: `SKILL.md`, the `### Round 33 — published-axis gate and claim-verdict gate` table
(header `SKILL.md:767`, existing row `mado-session-material` at `SKILL.md:770`). Same seven
columns, same cell conventions as `mado-axis-scores` (`SKILL.md:769`).

## The row

| name | gate/probe | entry command | verdict map | self-test command / spelling | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| mado-session-material | gate | `python3 -I quality/check-session-material.py --repo . --rev REV` | 0 clean (`findings=0`); 1 findings (`findings>0`; a waived finding is excluded from the count and counted on its own `SESSION_MATERIAL_WAIVED: findings=<n> files=<n>` line); 2 usage, git error, or a failed/unserialled `hyprctl` read | `python3 -I quality/check-session-material.py --selftest`; prints `SELFTEST: passed=N/N failed=N`; 0 clean, 1 failed | summary line `SESSION_MATERIAL: files=<n> findings=<n> rev=<40 hex>`; rules `R1_CLIENT_DUMP` `R2_PROC_TABLE` `R3_MONITOR_IDENT` `R4_HOME_LISTING` `R5_SERIAL_PROSE` `R6_SERIAL_EXACT`; synthetic marker `SYNTHETIC-MATERIAL v1 kind=<fixture\|gate-copy> rules=<comma list of R1-R4 only> sha256=<64 hex>` as line 1 of a tracked `<path>.synthetic` sidecar, plus the matching `<path> <sha256> <rules> kind=<kind>` row in `quality/session-material-waivers.txt` (read from the scanned revision, never the working tree); a serial finding on a marked file is `WAIVER_REJECTED … reason=serial-rule-not-waivable` and R5/R6 can never be waived | reads committed bytes only (`git ls-tree`, `git cat-file --batch`); `--serial-from-host` runs exactly one `hyprctl monitors all -j` read and prints counts, never values; `--selftest` writes only under `$TMPDIR` | mado |

## Notes the integrator needs

- Selftest at the delivered file: **63/63** (`receipts/00-selftest.txt`), of which 34 are the
  marker gate's and 29 are new (23 serial-rule cases + 6 marker×serial interaction cases).
- There is **no flag that drops a rule**. R1-R4 and R5 are always scored; R6 contributes only
  when `--serial-from-host` supplies the values. `--rules` is deliberately absent; a selftest
  case (`e2e-no-rule-can-be-dropped`) asserts argparse rejects it with exit 2.
- Scope: `--scope ufo` (default, the historical `.ufo/`-only behaviour) or `--scope all`
  (whole tracked tree; this is where three held `corpus/knowledge/` prose serials sit, plus
  the 18 wave copies of them).
- The registry is a review surface, not a proof: W1 keeps it outside `.ufo/`, W2 pins the
  exact bytes of the waived file, W3 requires a second, separate registry line, W4a limits
  `gate-copy` to a blob byte-identical to the gate, W4b refuses any real identity value.
- With no registry and no sidecars the verdict is byte-identical to the tracked gate's: on
  `60edb66` the tracked gate prints `findings=115` and the marker gate prints the same 115
  plus the 21 R5 prose serials (`receipts/01-baseline.txt:117`, `receipts/02-new-gate-no-markers.txt:138`).
- Install order: (1) drop `check-session-material.py` in as `quality/check-session-material.py`;
  (2) copy `demo/sidecars/` into the lane (each file keeps its lane-relative path);
  (3) commit `demo/registry-round47.txt` as `quality/session-material-waivers.txt`;
  (4) run the gate: `SESSION_MATERIAL_WAIVED: findings=55 files=49` and `findings=84` — the
  remaining real material listed in the report §4.
- `demo/registry-round47-refreshed.txt` (51 rows) is the same set after the two stale gate copies
  (`round-45/w1/ExecPrivacyGate`, `round-46/w1/ExecSessionTriage`) are refreshed to the installed gate
  bytes, which closes their six findings (waived 55 → 61, remaining 84 → 78); the two extra sidecars are
  in `demo/sidecars-refreshed/`.
