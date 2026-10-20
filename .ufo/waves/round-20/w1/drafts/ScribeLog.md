Draft for L1 integration: append after LOG.md line 1338 (1338 lines at both `1f7f995` and `e629f73`). `«»` = hash or number L1 fills from receipts; delete this line before integrating.

## 2026-10-20 — round 20: tripwire precision repair, calibration 29/30, round-19 corrections

Trigger: round-19 closed **rejected-harmed** (`corpus/lessons/round-19-verifier-spotcheck.md`, routed R19-V1..V6) at baseline `1f7f995caa25627db804e996cccd87fe38a3a1b6` (round-19 tip `b435568` + closure). The harm: HelperFn rule B (tool `367be947…`) turns provably pure data `BLOCK=frozenset(['pacman','-Q','hyprland'])` into an ordinary `package_query` finding with no lead marker. Pre-harm baseline for every no-harm comparison: `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d` (tool `c1ae45a7…`). Claims pre-registered at `e629f73` (SCORECARD tail, "Round 20 — declared claims"; 2026-10-20 16:23 -03). Wave-1 integration `«»`; receipts `«»`; round-20 tip `«»`. Host pause carried: no package query or transaction, service, compositor, input or screenshot operation, no real `hyprctl`; host files read as bytes only. R15-V1 remains operator-owned, state `[UNK]`.

Claims (declared at `e629f73`; before values at `1f7f995` unless stated):

C1 operability/tripwire precision (sourced): `python3 -I .ufo/waves/round-20/tw-precision.py REV` over the round-20 precision suite `.ufo/waves/round-20/precision/`, families P (pure containers/formatters, want clean), S (binding/shadowing), W (real wrapper misses, want observed), H (help/dry-run non-writes, want clean, with write negatives such as `git commit -n` = `--no-verify`), L (invisible-body leads, want `lead`). Evidence marker E1: `observed` or `lead`; a row without the key matches `observed`. Score `10·passed/N`. Before `1f7f995`: «passed»/«N» (tool `367be947…`); before `9c54c56`: «passed»/«N» (tool `c1ae45a7…`); after: «passed»/«N» at `«»`. Guards: `tw-recall.py` «6/6» unchanged with the observed/lead split reported; zero findings on the 20 control lines «0/20»; every P case also passes at `9c54c56` «»; whole-corpus diff vs `9c54c56` loses «0» findings and classes every added row «»; existing tripwire suites «N/N, each case edit with its reason»; round-19 frozen replay «re-pinned / unchanged». Sourced on SOURCES rows «S1xx» (git help/dry-run semantics, jj help, Python builtins).

C2 calibration: `python3 .ufo/waves/round-17/measure.py REV`, key `c1`, instrument unchanged. Before `1f7f995`: 20/28 = 7.1429 (`.ufo/waves/round-20/evidence/measure-before.txt`). Pre-registered target 22/30 = 7.3333 with two lesson-cited criteria, each red on a real round-19 artifact: **29** an isolation harness fails closed (red: the round-19 `inns.sh` `[ -e ] && mount && echo` shape; the payload is a canary file write into `/tmp`, never a host probe); **30** a count stated in a SCORECARD/lesson/report claim is re-derived at the measured revision by a cited command (red: "155 transcripts" vs a 154-file receipt; "5/13 name S096" vs 8/13 any-line / 6/13 first-line; "ten OM10 assertions" vs nine labeled occurrences / eight distinct). Measured after: «N/30» = «score». Neither criterion restates 24, 27 or 28; R19-V1 stays a miss and this target is registered fresh.

Non-claim repairs (harm-watched, append-only):

- R19-V2 (S096 tally): see correction below; freshness claims remain provenance, not walker behaviour.
- R19-V4 (isolation): the fail-open mount/script-wrapper incident is routed to C2 criterion 29; the written-script scan blindness stays explicit; the 155-vs-154 receipt count is repaired; self-report is not counted as tripwire detection.
- R19-V5 (OM10): "ten OM10 assertions" is corrected to nine labeled occurrences (eight distinct); OM10A/B guarantees are kept «gate selftest N/N».
- R19-V6 (lane paths): absolute lane paths at every seat boundary; dead seats remain uncredited (below).
- R19-V3 is the C1 repair above; R19-V1 is preserved as recorded.

### Round-19 correction — R19-V2 S096 tally (append-only)

The round-19 entry's "5/13 name S096 on the crediting line" is stale at `b435568`. Registered measurement: a file is credited if any line matching the version+source regex contains `\bS096\b`: **8/13** at `b435568` (`«»`). First-matching-line reading: **6/13** (`«»`). Five files still have no S096 on a qualifying line (`arc-synthesis.md:392`, `closeout-r11.md:299`, `config-health-report-r3.md:1009`, `waybar-walker-plane.md:479`, `waybar-walker-semantics.md:467`); their dated pointers cite the pre-existing S090 row. The round-19 claim that every file cites the new host-byte row stays unmet; the 13/13 count is pointer provenance, not walker behaviour.

### Round-19 correction — closure and no-harm scope (append-only)

Round-19's "Harm watch PASS" covered gate, classifier, suites and census. It did not establish the precision no-harm condition for C3; closure `rejected-harmed` (`corpus/lessons/round-19-verifier-spotcheck.md` §C3) records the independent counterexample: `9c54c56` exit 0 clean, `b435568` exit 1 `package_query/pacman:-Q`, on a data-only fixture whose code was never executed.

## Waves and accounting

Waves: w1 85 seats (`w1/dispatch.json` counts.spawn 85; `w1/task-result.json` attempts `[[1,16:36,85],[2,16:39:52,85],[3,16:42:57,0]]` — `«L1 reconciles: one batched task call or a duplicate spawn; agent counts»`). Dead seats without a report: «N», uncredited. Provider-rate-limit recoveries: «N»; recovered output is not claim evidence. w2 «N seats» (falsify). Harm watch at `«»`: gate selftest «N/N», regression «PASS», classifier «N/N», tripwire suites «N/N», U «N/N», rubric V «N/N», navigation «complete», census exit «0».

Installs: «none, or tool/version/channel/reason per install (none by L1 or any seat in the host pause)».

Admission not asserted.
