# R99MMutC2 - C2 harm-watch mutant population

Seat: R99MMutC2 (mutation-tester), round 99, wave w1, 2026-11-07.
Anchor: `.ufo/waves/round-99/build/harm-watch.py` sha256
`8ad90bed84eb31bfc3d2d98ae0ea630530bb3bb0a83d7bcdec383c2b11a34574`, the C2 tool draft owned
by R99MExecHarm (re-hashed before and after the sweep; unchanged). Panel measured:
`controls/harm-panel-r99.json` sha256 `7bf25b73bc868fba685bed9381f09be26f7e16ef72980aaac8fd61512827ec2a`
(28 rows). Base revision `2cbaa141f42df9dfeee4d207cae6558a4dd59863`.

## 1. Deliverable

`controls/harm-mutants-r99.json` sha256
`dfc353c49403aa25cf8fd7c48522e3f614b3f0bd2d59b1940a48774771e4ce61`:

- **32 counted mutants**, each `{"id","find","replace","rule","expect":"kill"}` plus
  `killed_by` and `observed`; every one is killed by the committed panel or a planted panel;
- **3 `equivalents`**, **28 `not_observable`**, **4 `outside_region`**, each with a written
  argument;
- `anchor_sha256` equals the tool sha above; every counted `find` occurs exactly once in the
  whole file and once in the production region (source up to the first literal
  `def selftest(`, line 398 of 592); no `find` equals its `replace`; the file is ASCII.

The tool moved twice during the wave (`0abb788f` after the two blockers below, then
`8ad90bed`). The document was re-bound at `8ad90bed` and every find re-verified; the sweep's
mutated copies differ from the final bytes only by their mutation (checked: `diff` of the
`rev-drop` copy against the tool is exactly one line).

## 2. Detector and control set

Observable answer = exit code + the census finding lines + the `HARM_WATCH:` summary tuple +
the per-`LEG` rows (id, rc, expect, marker) + the `HARM_WATCH_SELFTEST:` tuple. A kill is a
well-formed difference from the pristine run on a control; a traceback or an exit outside
{0,1,2} on that control is a crash and is never credited. A crash on one control does not
cancel a kill on another (the lane's rule: a crash is not a kill, but it is not a verdict on
the mutant either).

Controls: the committed panel, the three planted panels, and `--selftest`.

The committed panel's legs are multi-minute. Measured with a 5 s cap: fourteen legs finish in
0.05-0.39 s; `gate_mimeglob` 1.15 s, `gate_portals` 1.90 s, `r90c1_portal_routing` 2.46 s,
`gate_seat_reports` 3.76 s; ten legs exceed 5 s and `r92_gate_defects` exceeds 300 s. A full
pristine run reached leg 19 of 28 in about 40 minutes under host load average 105 and was
abandoned; the owner's measurement pass is the authority for the full 28-row panel.

The differential sweep therefore ran on a seat copy carrying the fourteen legs that finish
under 0.4 s **verbatim** (same ids, argv, expect_rc, expect_marker), with `expect_legs` and
`rounds` adjusted, and the three planted transforms applied to that copy (dropped-leg removes
`mako_selftest` and keeps it declared, so the explained-delta rule yields exactly one finding;
extra-leg appends an undeclared id; wrong-expect flips `index` to rc 1). The per-leg cap was
3 s against a 0.4 s maximum, and two pristine runs agreed. The sweep was repeated after the
classifier fix (the first run counted a crash as a kill).

| control | pristine rc | pristine answer |
|---|---|---|
| fast panel (14 committed rows) | 0 | `HARM_WATCH: legs=14 ok=14 mismatch=0` |
| planted dropped-leg | 2 | `PANEL PANEL_LEG_MISSING id=mako_selftest round=base` |
| planted wrong-expect | 1 | `HARM_WATCH: legs=14 ok=13 mismatch=1` |
| planted extra-leg | 2 | `PANEL PANEL_LEG_UNKNOWN id=sneaky` |
| selftest | 0 | `HARM_WATCH_SELFTEST: checks=26 failed=0` |

Sweep: 55 bound rows applied; 51 killed, 3 survived, 1 crash. Of the 51, **32 are observed by
a panel or planted control** and are counted; **19 are observed only by the gate's
`--selftest`** and are moved to `not_observable` (finding F3: the C2 counter never runs the
gate's selftest, so no round instrument sees them).

## 3. Kill table (32 counted)

| rule | mutant | killed by | observed difference |
|---|---|---|---|
| census-leg-count | `census-leg-count-invert` | panel | panel: c: rc 0 -> 2; planted_dropped: c: census_ids ['PANEL_LEG_MISSING'] -> ['PANEL_LEG_COUNT', 'PANEL_LEG_MISSING']; planted_wrong: c: rc 1 -> 2; planted_extra: c: census_ids ['PANEL_LEG_UNKNOWN'] -> ['PANEL_LEG_COUNT', 'PANEL_LEG_UNKNOWN'] |
| census-duplicate | `census-duplicate-invert` | panel | panel: c: rc 0 -> 2; planted_dropped: c: census_ids ['PANEL_LEG_MISSING'] -> ['PANEL_DUPLICATE', 'PANEL_LEG_MISSING']; planted_wrong: c: rc 1 -> 2; planted_extra: c: census_ids ['PANEL_LEG_UNKNOWN'] -> ['PANEL_DUPLICATE', 'PANEL_LEG_UNKNOWN'] |
| census-round-missing | `census-round-missing-invert` | panel | panel: c: rc 0 -> 2; planted_dropped: c: census_ids ['PANEL_LEG_MISSING'] -> ['PANEL_LEG_MISSING', 'PANEL_ROUND_MISSING']; planted_wrong: c: rc 1 -> 2; planted_extra: c: census_ids ['PANEL_LEG_UNKNOWN'] -> ['PANEL_LEG_UNKNOWN', 'PANEL_ROUND_MISSING'] |
| census-leg-unknown | `census-leg-unknown-drop` | planted_extra | planted_extra: c: census_ids ['PANEL_LEG_UNKNOWN'] -> ['PANEL_LEG_COUNT']; selftest: c: rc 0 -> 1 |
| census-leg-unknown | `census-leg-unknown-invert` | panel | panel: c: rc 0 -> 2; planted_dropped: c: census_ids ['PANEL_LEG_MISSING'] -> ['PANEL_LEG_COUNT', 'PANEL_LEG_MISSING', 'PANEL_LEG_UNKNOWN']; planted_wrong: c: rc 1 -> 2; planted_extra: c: census_ids ['PANEL_LEG_UNKNOWN'] -> ['PANEL_LEG_COUNT', 'PANEL_LEG_UNKNOWN'] |
| census-leg-missing | `census-leg-missing-drop` | planted_dropped | planted_dropped: c: rc 2 -> 0; selftest: c: rc 0 -> 1 |
| census-leg-missing | `census-leg-missing-invert` | panel | panel: c: rc 0 -> 2; planted_wrong: c: rc 1 -> 2; planted_extra: c: census_ids ['PANEL_LEG_UNKNOWN'] -> ['PANEL_LEG_MISSING', 'PANEL_LEG_UNKNOWN'] |
| census | `census-skip` | planted_dropped | planted_dropped: c: rc 2 -> 0; planted_extra: c: rc 2 -> 0; selftest: c: rc 0 -> 1 |
| census-exit | `census-exit-zero` | planted_dropped | planted_dropped: c: rc 2 -> 0; planted_extra: c: rc 2 -> 0; selftest: c: rc 0 -> 1 |
| census-exit | `census-exit-one` | planted_dropped | planted_dropped: c: rc 2 -> 1; planted_extra: c: rc 2 -> 1; selftest: c: rc 0 -> 1 |
| census-exit | `census-continue` | planted_dropped | planted_dropped: c: rc 2 -> 0; planted_extra: c: rc 2 -> 0; selftest: c: rc 0 -> 1 |
| marker | `marker-invert` | panel | panel: c: rc 0 -> 1; planted_wrong: c: summary [14, 13, 1] -> [14, 0, 14]; selftest: c: rc 0 -> 1 |
| marker | `marker-prefix` | panel | panel: c: rc 0 -> 1; planted_wrong: c: summary [14, 13, 1] -> [14, 12, 2] |
| rc | `rc-drop` | planted_wrong | planted_wrong: c: rc 1 -> 0; selftest: c: rc 0 -> 1 |
| rc | `rc-invert` | panel | panel: c: rc 0 -> 1; planted_wrong: c: summary [14, 13, 1] -> [14, 1, 13]; selftest: c: rc 0 -> 1 |
| rc | `rc-off-by-one` | panel | panel: c: rc 0 -> 1; planted_wrong: c: summary [14, 13, 1] -> [14, 0, 14]; selftest: c: rc 0 -> 1 |
| timeout | `timeout-zero` | panel | panel: c: rc 0 -> 1; planted_wrong: c: summary [14, 13, 1] -> [14, 0, 14]; selftest: c: rc 0 -> 1 |
| rev | `rev-drop` | panel | panel: c: rc 0 -> 1; planted_wrong: c: summary [14, 13, 1] -> [14, 12, 2]; selftest: c: rc 0 -> 1 |
| rev | `rev-empty` | panel | panel: c: rc 0 -> 1; planted_wrong: c: summary [14, 13, 1] -> [14, 11, 3]; selftest: c: rc 0 -> 1 |
| cwd | `cwd-wrong` | panel | panel: c: rc 0 -> 1; planted_wrong: c: summary [14, 13, 1] -> [14, 0, 14] |
| exit | `exit-mismatch-zero` | planted_wrong | planted_wrong: c: rc 1 -> 0; selftest: c: rc 0 -> 1 |
| exit | `exit-green-one` | panel | panel: c: rc 0 -> 1; selftest: c: rc 0 -> 1 |
| exit | `exit-mismatch-two` | planted_wrong | planted_wrong: c: rc 1 -> 2; selftest: c: rc 0 -> 1 |
| summary | `summary-legs-plus-one` | panel | panel: c: summary [14, 14, 0] -> [15, 14, 0]; planted_wrong: c: summary [14, 13, 1] -> [15, 13, 1]; selftest: c: rc 0 -> 1 |
| summary | `summary-ok-eq-legs` | planted_wrong | planted_wrong: c: summary [14, 13, 1] -> [14, 14, 1]; selftest: c: rc 0 -> 1 |
| summary | `summary-mismatch-zero` | planted_wrong | planted_wrong: c: summary [14, 13, 1] -> [14, 13, 0]; selftest: c: rc 0 -> 1 |
| summary | `summary-swap` | panel | panel: c: summary [14, 14, 0] -> [14, 0, 14]; planted_wrong: c: summary [14, 13, 1] -> [14, 1, 13]; selftest: c: rc 0 -> 1 |
| summary | `summary-ok-count-drop` | panel | panel: c: rc 0 -> 1; planted_wrong: c: summary [14, 13, 1] -> [14, 0, 14]; selftest: c: rc 0 -> 1 |
| summary | `summary-k-from-n` | panel | panel: c: rc 0 -> 1; planted_wrong: c: summary [14, 13, 1] -> [14, 13, 14]; selftest: c: rc 0 -> 1 |
| leg-line | `leg-line-rc-expect` | planted_wrong | planted_wrong: c: leg index ['0', '1', 'ok'] -> ['1', '0', 'ok'] (1 changed); selftest: c: rc 0 -> 1 |
| leg-line | `leg-line-id-length` | panel | panel: c: leg ids 14 -> 10 (missing=['gate_selftest', 'index', 'ledger', 'mako_selftest'] extra=['13', '15', '16', '17']); planted_wrong: c: leg ids 14 -> 10 (missing=['gate_selftest', 'index', 'ledger', 'mako_selftest'] extra=['13', '15', '16', '17']); selftest: c: rc 0 -> 1 |
| leg-line | `leg-line-only-mismatch` | panel | panel: c: leg ids 14 -> 0 (missing=['gate_selftest', 'index', 'ledger', 'mako_selftest'] extra=[]); planted_wrong: c: leg ids 14 -> 1 (missing=['gate_selftest', 'ledger', 'mako_selftest', 'mime_selftest'] extra=[]); selftest: c: rc 0 -> 1 |

## 4. Non-killers and their arguments

### equivalents (3)

- `eq-cwd-drop` (cwd): The counter invokes the tool with cwd=--repo (the tool contract only says the legs run with cwd=--repo, and the tool is itself started from the repo), so dropping the explicit cwd changes no leg on any control. Verified: the equivalent row is byte-identical to mutant cwd-drop, which survived.
- `eq-census-first-only` (census): Every control that reaches the census prints exactly one finding (the explained-delta rule keeps the planted dropped-leg and extra-leg panels at one line, and the selftest's duplicate/round-empty/count fixtures each produce one), so printing only the first finding is identical on every control.
- `eq-census-row-guard` (census): No control panel carries a non-object row; every row is a dict, so the guard is dead on the control set (and dropping it would crash, not answer).

### not_observable (28)

The 19 selftest-only rows are listed in the JSON with the F3 argument; the rest:

- `no-census-unreadable-legs` (census): No control panel has an empty or non-list legs field; the selftest's unreadable check uses an absent file (load_panel fails before census), so the guard is dead on the control set. Removing it with a bad panel would crash (TypeError), which is never a kill.
- `no-scratch-escape` (scratch): No control leg id escapes the scratch root (all ids are plain alphanumerics), so the guard is dead on the control set.
- `no-bad-leg-id` (scratch): No control leg id contains a path separator or a leading dot; the guard is dead on the control set.
- `no-json-exit-field` (json): The selftest's json-mode check reads legs_run, mismatch and the leg array, never the exit field; the counter reads the text face. No control reads the JSON exit field.
- `no-json-census-field` (json): The JSON census field is a constant empty list in production (census findings return before the JSON face); no control reads it.
- `cwd-drop` (cwd): No control observed a well-formed difference (sweep verdict survived; rcs {"panel": 0, "planted_dropped": 2, "planted_extra": 2, "planted_wrong": 1, "selftest": 0}). The mutation changes only a path the committed panel, the three planted panels and --selftest do not exercise.
- `scratch-marker-drop` (scratch): The gate's --selftest crashes on it (traceback: without the marker the foreign scratch dir is refused and a later fixture run aborts), and a crash is not a kill; no panel or planted control observes it.
- `json-legs-run` (json): No control observed a well-formed difference (sweep verdict survived; rcs {"panel": 0, "planted_dropped": 2, "planted_extra": 2, "planted_wrong": 1, "selftest": 0}). The mutation changes only a path the committed panel, the three planted panels and --selftest do not exercise.
- `json-mismatch` (json): No control observed a well-formed difference (sweep verdict survived; rcs {"panel": 0, "planted_dropped": 2, "planted_extra": 2, "planted_wrong": 1, "selftest": 0}). The mutation changes only a path the committed panel, the three planted panels and --selftest do not exercise.

### outside_region (4)

Rows inside `def selftest(` (or replacing its dispatch), listed for coverage and never counted:
the lane's `check-selftest-strength.py` cuts at the first literal `def selftest(`, and a
kill-set mutant there could silence its own check.

- `outside-selftest-line-renamed` (selftest): Inside def selftest(, so outside the declared non-selftest mutant region; the lane's check-selftest-strength.py cuts at `def selftest(` and a kill-set mutant there could silence its own check. Listed for coverage, never counted.
- `outside-selftest-checks-zero` (selftest): Inside def selftest(; outside the declared region. It would be killed by a counter that ran the gate's --selftest, but the C2 counter does not (finding F3), and the region rule forbids counting it anyway.
- `outside-selftest-fail-silent` (selftest): Inside def selftest(; outside the declared region. Not observable anyway: the pristine selftest is green, so no control forces failed>0.
- `outside-selftest-vacuous` (selftest): Inside main() but it replaces the selftest dispatch; the region rule is about the selftest body, and this row is the coverage finding: a vacuous selftest printing checks=99 failed=0 is indistinguishable to the counter, which reads only the count. Outside the counted region by the same rule.

## 5. Findings for the L1

F1. **The timeout handler killed its own process group (fixed after this seat's report).**
`os.killpg(os.getpgid(e.cmd and 0 or 0), signal.SIGKILL)`; `e.cmd and 0 or 0` is always 0, so
this is `os.getpgid(0)` = the tool's own pgid. Measured under `setsid`: a panel with one
`sleep 30` leg and `--timeout 1` produced no output and killed the whole session; `--selftest`
died at its timeout check in about 1.8 s with no `HARM_WATCH_SELFTEST:` line. Reported at
18:27Z; the owner replaced it with `subprocess.Popen` + `os.getpgid(p.pid)`. Verified after the
fix: the selftest completes and the slow leg records `rc=124`, `timeout-after-1s`, and the gate
survives.

F2. **The selftest was red on two fixtures (fixed after this seat's report).**
`scratch-foreign-refused` expected rc 2 but production answered a per-leg setup error as a
mismatch (rc 1); `leg-logs-written` counted 4 `.log` files because the scratch dir is reused
across checks. Reported at 18:29Z; the owner moved the setup exit into `run_panel` (exit 2 with
`HARM_WATCH: setup-error leg=<id> detail=<...>`) and fixed the fixture count. Current:
`HARM_WATCH_SELFTEST: checks=26 failed=0`.

F3. **The C2 counter never runs the gate's `--selftest` (the round-98 F5 class, open again).**
`--selftest` appears only in the counter's own argparse (`c2-r99-harm-watch.py:429`); the
`run_gate` argv has no `--selftest`; the predicate's `selftest_checks >= 12 AND
selftest_failed == 0` is the *counter's* fixture selftest (`selftest_checks()` builds a
MINI_GATE and reruns the counter on it). Consequence: a gate whose `--selftest` is vacuous
(prints `checks=99 failed=0` and runs nothing) or red passes the counter. Evidence: the
`outside-selftest-vacuous` row in the deliverable is a well-formed gate that passes every
counter-visible control, and 19 of this seat's 51 kills are invisible to the counter for the
same reason.

F4. **PANEL_LEG_COUNT, PANEL_DUPLICATE and PANEL_ROUND_MISSING are invisible to every control
except the gate's selftest.** The explained-delta rule (`explained = unknown + dup_surplus -
missing`) keeps the planted dropped-leg and extra-leg panels at exactly one finding, so a gate
that drops the count check still passes the committed panel, the three planted panels and the
stub; only the gate's `--selftest` catches it, and the counter does not run that (F3). The same
holds for the duplicate and empty-round checks: no planted panel carries a duplicate or an
empty round. `panel-pin-expect-legs-drop` is killed by `--selftest` only.

F5. **The planned planted wrong-expect flips a leg slower than any practical per-leg cap.**
The owner's plan (IRC, 18:35Z; the planted dir had not landed when this report was written)
flips `r96c2_selftest_kills` (measured > 5 s). At the panel's own `timeout_s` it is a
clean single mismatch; under a 1 s or 3 s cap the flipped leg times out in both the clean and
the wrong panel, so the control is indistinguishable from clean. Not a defect at the frozen
timeout, but the discrimination is fragile: a later re-freeze that lowers `timeout_s` silently
voids the control. This seat proved the rc-test mutants on a seat wrong-expect copy whose
flipped leg is fast (`index`, rc 0 expect 1).

F6. **The JSON face is additive and only partially read.** The gate prints the human lines and
then one JSON object; the counter takes `mismatch` from the human summary and `legs` from the
JSON for the wrong control, but never reads `exit` or `legs_run`. Mutants that change only those
fields survive (`json-mismatch`, `json-legs-run`). `legs_run = len(json.legs) or panel_legs` is
vacuous when the JSON is absent.

F7. **The census carries two findings outside the contract's five** (`PANEL_UNREADABLE`,
`PANEL_ROW`). They are setup findings, not census findings; no planted control exercises them.
Named limit, not a defect.

F8. **The gate's `--json` object is printed after the summary line**, so a consumer that parses
the last `{` line gets it; a consumer that parses only the human lines still gets every count.
Both faces were exercised by the selftest.

## 6. Tooling

No tool was installed or upgraded. All runs used the system `python3` (stdlib only) and
read-only `git`; no pacman transaction, no network, no host service.

## 7. Scratch

All work ran under `/fast/scratch/hyaku/mado-r99/R99MMutC2` (harness `probe.py`/`runmut.py`,
binder, bound mutants, per-mutant tool copies, run outputs). The directory is removed before
yield; the committed artifacts are this report and `controls/harm-mutants-r99.json`.
