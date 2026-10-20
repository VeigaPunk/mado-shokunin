# RevScorecard — partly falsified: pinned results reproduce, but final-tip evidence has a rerun break and one count lacks a registered derivation

## Findings

### P2 — Final tip makes the cited red isolation harness non-runnable

`SCORECARD.md:1331` reports `inns-r19-shape.sh` as the red harness (`FAIL_OPEN` in 5/6 modes, exit 1). The cited checker, `.ufo/waves/round-20/isolation-check.sh:11-13`, rejects any harness without its executable bit (`COULD_NOT_EVALUATE … (not executable)`, exit 2).

Evidence: the harness bytes are identical (`sha256 8bd507f0ea39d4d876359a0f5a1f798e810cda3c59293487af35d3a8df37ce9c`), but `git ls-tree 28c6837 …/inns-r19-shape.sh` reports mode `100755` while `git ls-tree a4046a8 …/inns-r19-shape.sh` reports `100644`; commit `4362219` records the mode-only change `100755 => 100644`. At the measured commit, the absolute-path command `bash /tmp/mado-r20w2-RevScorecard/.ufo/waves/round-20/isolation-check.sh /tmp/mado-r20w2-RevScorecard/.ufo/waves/round-20/evidence/inns-r19-shape.sh` returned exit 1 with five `FAIL_OPEN`, one `FAIL_CLOSED`, and `POSITIVE_CONTROL_OK`, matching the scorecard. Against the committed tip mode, the same checker returned `COULD_NOT_EVALUATE inns-r19-shape.sh (not executable)` and exit 2. The reported measurement is valid at `28c6837`, but a final-tree rerun of its red half now fails before testing the harness; preserve the executable bit or provide an executable test copy.

### P3 — “Five S090-only files” is not a registered tally claim

`SCORECARD.md:1277` states “five S090-only files.” The final `.ufo/waves/round-20/tally-claims.json:150-252` green registry has four entries (154 files, S096 first-line, S096 any-line, and nine OM10 occurrences) and contains no S090 check (`tally-claims.json` SHA-256 `81eed3ebe33ec0bd2a7adbb5077c51a2624e00bccd945df83477f21674b3a48d`). This is a traceability gap, not a wrong count. From cwd `/tmp/mado-r20w2-RevScorecard`, I ran:
`python3 -I /tmp/mado-r20w2-RevScorecard/.ufo/waves/round-20/tally-check.py pointer-token --counter .ufo/waves/round-19/fresh-pins.py --counter-rev 1f7f995caa25627db804e996cccd87fe38a3a1b6 --rev 1f7f995caa25627db804e996cccd87fe38a3a1b6 --token S090`
and the same command with `--token S096`. They returned S090 `any_line=12/13` and S096 `any_line=8/13`; comparing the emitted per-file token sets gave five S090-present/S096-absent files: `arc-synthesis.md`, `closeout-r11.md`, `config-health-report-r3.md`, `waybar-walker-plane.md`, and `waybar-walker-semantics.md`. The checker’s SHA-256 is `21ce9dd57a47d975623aa9ca2bf53c3dadb8fa68b6f066a92461edba2fd2aea3`; the pinned `fresh-pins.py` SHA-256 is `a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789`. Add these two exact pointer-token invocations (or a registry entry) if this count is intended to meet the cited-command standard.

## Re-derivations

- C1 precision: `python3 -I /tmp/mado-r20w2-RevScorecard/.ufo/waves/round-20/tw-precision.py 1f7f995` returned `29/175`, score `1.6571`, families P/S/W/H/L = `7/66, 2/17, 4/22, 15/52, 1/18` (tool SHA-256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`). At `28c6837` it returned `172/175`, `9.8286`, `66/66, 17/17, 21/22, 51/52, 17/18` (tool SHA-256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`). At `9c54c56` it returned `110/175`, `6.2857`, with P `66/66` (tool SHA-256 `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`). The final counter output’s three failures are exactly the named W, H, and L cases. The suite pin is `f3da504`; its manifest has 175 scored cases across the assembler’s 13 seats and 12 held-out cases. `--heldout` returned `0/12` at both `1f7f995` and `28c6837`.
- C1 guards: `tw-recall.py 28c6837` returned 6/6. `tw-recall-split.py 28c6837` returned 5 detected-observed + 1 detected-lead, 0 unmarked/undetected, and 20 control lines with 0 findings. The lead row is `r13-root.jsonl:4`. The 11 direct tripwire suites returned 247/247; round-19 frozen replay returned `frozen_match`/exit 0 and round-18 returned the expected `frozen_verdict_mismatch`/exit 1. The eight `r20_edit` cases each add one expected finding; two further existing lead cases receive marker-only edits. No scored-suite bytes changed after `28c6837`.
- C2 calibration: `measure.py 1f7f995` returned 20/28, `7.1429`; at `a4046a8216080d4004de3f268c62cf142095ac07` it returned 22/30, `7.3333`. The conditional alternate `21/29 = 7.2414` is arithmetically correct if the closure treats 30′ as a target-preserving swap. Red and green isolation checks at the measured commit reproduced 5/6 fail-open + positive control/exit 1 and 6/6 fail-closed + positive control/exit 0. `tally-check.py` returned red `5/5` mismatches (exit 1) and green `4/4` matches (exit 0); `selftest-labels` directly printed `removed_occurrences=9` and `removed_distinct=8`.
- The broad `harm-watch.sh` run at `28c6837` reported `HARM_WATCH: PASS`, 21 commands, 0 failures (20 ordinary successes and the expected round-18 baseline mismatch). Its receipts show gate selftest 460/460, action-plan selftest 52/52, tripwire suites 11/11, navigation 34/34 with no missing/dangling/duplicate entries, and census exit 0. Source rows count 98 at `1f7f995` and 112 at `a4046a8`; all 14 new rows S099–S112 are tier A/mined.

## Pending

- `SCORECARD.md:1330` explicitly leaves the whole-corpus diff against `9c54c56` pending for wave 2. I did not run or claim that no-harm comparison.
- The closure disposition of 30′ as a target-preserving swap remains conditional in `SCORECARD.md:1299-1300` and `:1331`; retain both C2 readings until that decision is recorded.

## Limits

The C1/C2 counters, suite guards, tally checks, calibration, and isolation checks were re-run in a private `/tmp` clone. The scorecard’s pinned measurements are numerically reproducible; findings above concern final-tip test-artifact mode and traceability, not a changed C1/C2 score. No LSP caller/definition/diagnostics query was applicable to this documentation-and-command reproducibility review. No package, compositor, service, device, or host probe was run.

## Installs

None.
