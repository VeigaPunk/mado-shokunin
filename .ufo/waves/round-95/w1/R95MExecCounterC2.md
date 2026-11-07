# R95MExecCounterC2 — round 95, wave w1 — C2 counter + panel (PRED-C2-r95-v1)

Seat: executor, counter lane. Item: adapt round 94's `quality/counters/c2-r94-selftest-kills.py` to PRED-C2-r95-v1
for `tools/mado-mimeglob.py` (19 checks) and `tools/mado-portals.py` (28 checks), write the panel
`.ufo/waves/round-95/controls/selftest-panel-r95.json` (>= 12 hand weakenings + >= 3 neutral edits per tool), and
DRAFT-run with R95MExecKillsC2's kill-sets via `--draft-kills`. Base rev 4a2af6817024f6ed47084a5217c1825ae247f4fe.
All runs in this report are DRAFT runs (the L1 has not frozen; nothing here is a measurement).

## Files written (mine)

| file | sha256 |
|---|---|
| `quality/counters/c2-r95-selftest-kills.py` | e021c2c2c97bbbf34c20aa67c01462577605215529ae03586386423c8243dfef |
| `.ufo/waves/round-95/controls/selftest-panel-r95.json` | 635d8ffb62805aaab7accb49d758e6b81a887627266bec0daf5d36a93c76d18b |

The counter is round 94's file with only: docstring (PRED-C2-r95-v1 sentence, 19 + 28 = 47, (vii) reworded to the
R95MExecKillsC2 candidate sets), `PRED`, `TOOLS = (tools/mado-mimeglob.py, tools/mado-portals.py)`, `KILLS =
(quality/selftest-kills/mado-mimeglob.json, quality/selftest-kills/mado-portals.json)`, `RESULT_PREFIX =
(MADO_MIMEGLOB_SELFTEST: , MADO_PORTALS_SELFTEST: )`, argparse help/setup strings (xdgmime,mime → mimeglob,portals)
and the scratch prefix `c2r95-`. `diff` against c2-r94 shows exactly those lines; `py_compile` clean. Label
derivation is unchanged: idx 0 = `checks += [("label", ...)]` list entries + `checks.append` (mado-mimeglob),
idx 1 = `chk("label", ...)` (mado-portals); NEEDLE (the single `    failed = [n for n, ok in checks if not ok]`
line) neutralises one label per variant. Both tools' tools/ bytes are untouched (sha256 65f80a6c…2453,
e46a861e…2021 as declared).

## Panel design

- 24 hand weakenings (`glob-w01…w12`, `por-w01…w12`), each weakening exactly one check while the selftest stays
  green: 22 full tautologies ("expected replaced by the observed one", e.g. `r.resolve(FC) == r.resolve(FC)`),
  `glob-w10` (t15's no-exception arm records `not False`) and `por-w08` (both negative bus-name branches dropped).
  A full tautology makes the check unable to fail on any mutant, so once conjunct (ii) holds (every label covered
  by >= 1 kill whose must_fail names it), every weakening is forced to flag — the panel does not bet on which
  field a specific mutant perturbs. Two checks are left unweakened per tool on purpose (t04/t06/t08/t12/t14/t16/t19
  and the portals interface-key/UseIn/gtk-last-resort cluster) — 12 >= 12 per tool as required.
- 6 neutral edits (`glob-z01…z03`, `por-z01…z03`): trailing comments (checks list, chk def, failed-list line) and
  two reorders of independent checks (t01/t02 in the `checks +=` list; the pure `string_list`/`bus name` chk pair).
  No production line is touched, so no kill `find` can lose its unique match.
- The r94 invariants hold: all 30 finds occur exactly once in their tool; all 30 variants keep the selftest green
  with the byte-identical result line (`checks=19 failed=0` / `checks=28 failed=0`); all 47 single-label
  neutralisations green (my `validate.py`, 30/30 + 47/47 OK, exit 0).

## Evidence (all DRAFT, scratch /fast/scratch/hyaku/mado-r95/R95MExecCounterC2)

1. Both tools green at <rev>: `MADO_MIMEGLOB_SELFTEST: checks=19 failed=0` rc 0; `MADO_PORTALS_SELFTEST:
   checks=28 failed=0` rc 0. Gate sha at <rev> = `2d6f1219…da61b` (frozen round-93 gate), tools' shas equal the
   declaration's.
2. Labels: 19 unique mimeglob labels, 28 unique portals labels — each equals its result line's checks=N.
3. Smoke DRAFT run of the counter (micro kill-sets of my own, one held kill per tool: ascii_tolower→identity /
   current_desktops lower→identity; scratch only, NOT the sibling draft): rc 3,
   `DRAFT_TARGET_MISSED pred=PRED-C2-r95-v1 … tools=2 checks=47 positive=OK:0,OK:0 neutralised_flagged=2/47
   hand_flagged=2/24 neutral_ok=6/6 do_nothing_flagged=0 always_ok_flagged=0 always_weak_positive=WEAK:1,WEAK:1
   shadiff_neutral_ok=0/6 gate_selftest=ok control_hand_flagged=2/24 singleton_labels=2/47 tool_pin=ok,ok` —
   79 probes, 10.8 s. This exercises every conjunct's plumbing; with 1-kill sets only the two covered labels flag,
   as expected.
4. Do-nothing figure: `do_nothing_flagged=0` — none of the 47 neutralisations (nor the 24 weakenings) changes the
   selftest result line. **0/47.**
5. Separability (declaration: the counter at the C1 commit stops SETUP_ERROR with kill-sets absent): non-draft run
   at rev 4a2af68 → `SETUP_ERROR … absent at 4a2af68…: quality/selftest-kills/mado-mimeglob.json,
   quality/selftest-kills/mado-portals.json`, rc 2. Verified.

## Sibling kill-set DRAFT run (`--draft-kills` with R95MExecKillsC2's candidate sets)

Ran after the files landed. Inputs: `.ufo/waves/round-95/build/mado-mimeglob-kills.c2.json`
(sha256 `f4b80be6ffbbe47d1280edb2858a7528182679d2f232c8c1a4e818de3ab521c7`, 17 kills, pins tool `65f80a6c…`) and
`.ufo/waves/round-95/build/mado-portals-kills.c2.json` (sha256 `64b3c10d22da05cd9da5f2200ded96e058fee5d913a07e2d509ff153c8a5c8f4`,
27 kills, pins tool `e46a861e…`). Command (reproducible; counter path repo-relative):

```
python3 -I quality/counters/c2-r95-selftest-kills.py --repo <lane> \
  --rev 4a2af6817024f6ed47084a5217c1825ae247f4fe \
  --panel .ufo/waves/round-95/controls/selftest-panel-r95.json \
  --expect-panel-sha256 635d8ffb62805aaab7accb49d758e6b81a887627266bec0daf5d36a93c76d18b \
  --expect-gate-sha256 2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b \
  --expect-kills-sha256 f4b80be6…,64b3c10d… --scratch-root <scratch>/s-real \
  --control-kills <build>/mado-mimeglob-kills.c2.json,<build>/mado-portals-kills.c2.json \
  --expect-control-kills-sha256 f4b80be6…,64b3c10d… \
  --draft-kills <build>/mado-mimeglob-kills.c2.json,<build>/mado-portals-kills.c2.json --workers 8
```

rc 3 (DRAFT), 61 s, 79 probes. Result line:

```
MADO_SELFTEST_KILLS: DRAFT_TARGET_MISSED pred=PRED-C2-r95-v1 rev=draft gate_pin=ok kills_pin=ok,ok tools=2 checks=47 positive=OK:0,OK:0 neutralised_flagged=47/47 hand_flagged=24/24 neutral_ok=6/6 do_nothing_flagged=0 always_ok_flagged=0 always_weak_positive=WEAK:1,WEAK:1 shadiff_neutral_ok=0/6 gate_selftest=ok control_hand_flagged=24/24 singleton_labels=36/47 tool_pin=ok,ok kill_paths=quality/selftest-kills/mado-mimeglob.json,quality/selftest-kills/mado-portals.json gate_sha256=2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b kills_sha256=f4b80be6ffbbe47d1280edb2858a7528182679d2f232c8c1a4e818de3ab521c7,64b3c10d22da05cd9da5f2200ded96e058fee5d913a07e2d509ff153c8a5c8f4
```

Per-probe (all 79 seen in the run log): T1 pos OK:0, T2 pos OK:0; all 47 `N:` probes WEAK:1; all 24 `W:` probes
WEAK:1; all 6 `Z:` probes OK:0. **Each control's result**: always-OK gate `always_ok_flagged=0` (flags no
weakening); always-WEAK gate `always_weak_positive=WEAK:1,WEAK:1` (fails (i) on both tools); sha-diff gate
`shadiff_neutral_ok=0/6` (flags every neutral edit, so it fails (iv)); do-nothing instrument
`do_nothing_flagged=0` — **0/47**, no neutralisation (and no weakening) changes the selftest result line; gate
`--selftest ok`.

**Conjunct (vii) is not satisfiable with the current panel alone**: the first-draft sets already flag 24/24 hand
weakenings (`control_hand_flagged=24/24` == `hand_flagged=24/24`; DRAFT_TARGET_MISSED is printed for exactly this
reason — in DRAFT the control sets are the same files). Round-94's mechanism is required: the panel's hand set
must grow by the mutation pass's green weakenings that the draft sets escape (r94 note: "+ R94MMutC2's green hand
weakenings"), and the frozen sets get the corresponding closing kills; then hand grows past 24 while
control_hand_flagged stays 24. Recommendation to the L1: keep this panel as the base (its 24 are all
draft-flagged, which (iii) needs) and append the mutation seat's green escapes before freezing; without added
closing kills (vii) fails as written. Informational: `singleton_labels=36/47` — 11 labels are covered only by
multi-label must_fail kills in the draft sets; that is legal for the gate but a single-check neutralisation of
those 11 is caught only through set-mismatch (WRONG_CHECK), which the 47/47 above confirms works.

## Risks / notes for the L1

- RESOLVED by the DRAFT run: the first-draft sets cover all 47 labels (`neutralised_flagged=47/47`) and flag all
  24 panel weakenings (`hand_flagged=24/24`) — conjuncts (i)–(vi) are in the TARGET_MET shape at draft; the only
  conjunct not satisfied is (vii) (see the section above; needs closing kills + appended green weakenings, r94
  pattern).
- Pins for the freeze commit: panel sha256 `635d8ffb62805aaab7accb49d758e6b81a887627266bec0daf5d36a93c76d18b`;
  counter = `quality/counters/c2-r95-selftest-kills.py` sha256
  `e021c2c2c97bbbf34c20aa67c01462577605215529ae03586386423c8243dfef`; frozen kill-set paths (from <rev> via git
  show): `quality/selftest-kills/mado-mimeglob.json`, `quality/selftest-kills/mado-portals.json`; control
  (`--control-kills` + `--expect-control-kills-sha256`) = the R95MExecKillsC2 build files above
  (`f4b80be6…,64b3c10d…`). The measurement invocation is exactly the command in the section above, minus
  `--draft-kills` and with `--expect-kills-sha256` set to the frozen candidates' shas.
- The 24 weakenings are all full-weak (check cannot fail), so (iii) is insensitive to which field a mutant
  perturbs; the two non-tautology entries (`glob-w10`, `por-w08`) also cannot pass a mutant they used to catch.
- Separability verified both ways: non-draft mode at the base rev stops `SETUP_ERROR` rc 2 (kill-sets absent);
  DRAFT mode with file kill-sets ignores git for the kill-sets only.
- Installs: none. Host writes: none outside my seat paths and scratch. No peer messages, no spawns.

## Scratch status

Scratch `/fast/scratch/hyaku/mado-r95/R95MExecCounterC2` removed at exit; all cited outputs are quoted in this
report (no extra evidence files were created under w1/ — write scope). Nothing under receipts/ was written.
Dead steps: none — the sibling kill-set files landed mid-wave and the run completed.
