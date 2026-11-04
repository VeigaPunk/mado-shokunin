# R81ExecMutants — findings (labrat transcript)

Seat: independent mutation census of the six new C1 mutants. All work under
`/fast/scratch/hyaku/mado-r81/R81ExecMutants` (removed at exit); receipts copied to
`.ufo/waves/round-81/w1/R81ExecMutants/evidence/` before removal. Lane root used read-only:
`/home/vgpnk/Projects/shokunin/mado-shokunin`.

## Commands run (exact argv) and the lines that matter

1. `sed -n '33,160p' quality/counters/c1-r81-overflow-auto.py` — read the frozen `MUTATIONS` list; extracted the six `(name, anchor, replacement)` tuples for `tie-round-trunc`, `round-width-spec`, `auto-gate-open`, `auto-gate-and`, `auto-axis-swapped`, `auto-dynamic-kept`.
2. `python3` (heredoc) counting each anchor in `tools/mado-barfoot.py` → all six `count: 1` (lines 495, 504, 591, 581, 585, 572).
3. `python3` (heredoc) dumping the last 6 entries of `.ufo/waves/round-81/controls/c1-cases-r81.json` → the six new fixtures; `auto-dynamic-band-refused` expects `"error": true, "rc": 3, "stage": "model"`, the other five expect CLEAN with `band=26`.
4. `sha256sum tools/mado-barfoot.py quality/counters/c1-r81-overflow-auto.py .ufo/waves/round-81/controls/c1-cases-r81.json` → `a129a435…`, `22405133…`, `ab8154a1…` (match the frozen declaration).
5. `mkdir -p /fast/scratch/hyaku/mado-r81/R81ExecMutants/{fixtures,mutants,logs} && cp tools/mado-barfoot.py …/mado-barfoot.py` → OK.
6. Read `.ufo/waves/round-81/receipts/measurement-c1-r81.txt` → counter's own all-39 mutant scores: `tie-round-trunc 38/39`, `round-width-spec 38/39`, `auto-gate-open 36/39`, `auto-gate-and 36/39`, `auto-axis-swapped 38/39`, `auto-dynamic-kept 38/39`; `tool_selftest=121/121`, `verdict=TARGET_MET`.
7. Read `tools/mado-barfoot.py:480-610` (`std_round`, `cbox_round`, `surface_zone`) and `:610-700` (`parse_surfaces`) for anchor context.
8. Wrote `census.py` (driver; imports the counter module for `expected_ok`/`parse_result`/`parse_attr` only; replicates the counter's argv and env; applies the six mutations by hand with `assert source.count(anchor)==1`).
9. `cd /fast/scratch/hyaku/mado-r81/R81ExecMutants && python3 -I census.py 2>&1 | tee logs/census.log` →
   `VARIANT base score=6/6`; `tie-round-trunc 5/6` (FAIL `overflow-tie-negative`: `boxes: want MATCH,MATCH got MATCH,DIFFER; rc: 1; verdict: DIFFER`); `round-width-spec 5/6` (same case, same fields); `auto-gate-open 3/6` (FAIL `auto-corner-edge`, `auto-all-four-edge`, `auto-parallel-edge`: `attributed/expected 126 vs 26`, `attr 0,126,0,0`, `attr_ns` gains `panel: top:100`); `auto-gate-and 3/6` (FAIL `auto-all-four-edge`/`auto-parallel-edge` (`226` vs `26`) and `auto-left-dock` (`box/boxes DIFFER`, `attr 0,26,0,0 vs 40,26,0,0`, `attr_ns` loses `dock: left:40`)); `auto-axis-swapped 5/6` (FAIL `auto-left-dock`, same fields as auto-gate-and); `auto-dynamic-kept 5/6` (FAIL `auto-dynamic-band-refused`: `rc 0 vs 3`, no `ERROR (stage=model …)` line). Full per-case diff table in `evidence/census.log`, machine copy `evidence/census.json`.
10. `for a in <six anchors>; grep -c -F "$a" tools/mado-barfoot.py` → `1` for each; `grep -n -F -A1 '<comment anchor>'` → line 591 + `592-    return 0` (two-line anchor occurs once as a sequence; exact byte count 1 via python).
11. Anchor-absent fixture: `python3` heredoc deleted the six anchors verbatim from the tool copy (asserted each count==1 before deletion) into `absent-repo/tools/mado-barfoot.py`; wrote `carried-r80.json` = first 33 cases of the r81 control set. Then `git -C $D init -q -b master && git -C $D add … && git -C $D rev-parse --show-toplevel` → printed `$D` (fixture dir, asserted) → `git -C $D -c user.name=R81ExecMutants -c user.email=seat@local commit -q -m …` → HEAD `5b032eeef613d976d2d35214fec4b9c80cabdf9d`.
12. `python3 -I quality/counters/c1-r81-overflow-auto.py --repo $S/absent-repo --rev HEAD --base-rev HEAD --controls .ufo/waves/round-81/controls/c1-cases-r81.json --carried $S/carried-r80.json --scratch-root $S/absent-work > logs/absent-run.log 2>&1; echo rc=$?` → counter rc=1 (verdict printed, not a crash). `grep -c 'reason=anchor-absent'` = 6; literal lines quoted in the report; `grep -c Traceback` = 0; tail shows normal `MADO_R81_BARFOOT: … verdict=TARGET_MISSED` line.
13. `python3 -I` heredoc re-running the six separating (mutant, case) pairs to capture literal RESULT lines → `evidence/separators.log` (quoted in the report).
14. `python3 -I tools/mado-barfoot.py --selftest` → `MADO_BARFOOT_SELFTEST: 121/121`, rc=0. `python3 -I quality/counters/c1-r81-overflow-auto.py --selftest` → `MADO_R81_BARFOOT_SELFTEST: 72/72`, rc=0.
15. `cp logs/census.log logs/separators.log logs/absent-run.log census.json <seat>/evidence/` → copied (verified with `ls -la`).
16. `rm -rf /fast/scratch/hyaku/mado-r81/R81ExecMutants` (cleanup; trap-equivalent executed manually after evidence copy).

## Conclusions

- Independent six-case census agrees with the frozen all-39 receipt: losses 1/1/3/3/1/1 on the new six ⇒ carried 33 contribute 0 losses for every one of the six mutants; all six mutants are killed by at least one of the six new fixtures. No unkillable (real-defect) mutant.
- Per-mutant separating case and differing field: `tie-round-trunc` ← `overflow-tie-negative` (`boxes`); `round-width-spec` ← `overflow-tie-negative` (`boxes`); `auto-gate-open` ← `auto-corner-edge` (+all-four, parallel; `attributed`/`attr`/`attr_ns`); `auto-gate-and` ← `auto-left-dock` (+all-four, parallel); `auto-axis-swapped` ← `auto-left-dock`; `auto-dynamic-kept` ← `auto-dynamic-band-refused` (`rc`, refusal line).
- Each anchor occurs exactly once in the tool bytes (`grep -c -F` = 1; two-line anchor verified by line-pair + byte count).
- Deleting any of the six anchors makes the counter print `MADO_R81_MUTANT: name=<m> correct=0/39 killed=no reason=anchor-absent` — demonstrated for all six at once against a scratch fixture repo; no traceback; counter exits 1 with a normal verdict line, not a setup crash.

No tools installed or upgraded (none needed). No writes outside the seat dir + scratch. No git mutations anywhere except the single commit inside the scratch fixture repo (asserted toplevel first).

STATUS: ok
