# R55CritControls — seat report (round 55, wave w1)

Role: critic on the control design (`registration.md` §C1, harness-held expectations, scratch-repo mutation, legs).
Deliverable: `.ufo/waves/round-55/w1/R55CritControls/cheats.md` (channel table, per-channel verdicts, defects with inputs,
recommended fixes). Sources and run receipts: `.ufo/waves/round-55/w1/R55CritControls/lab/`.

## 1. Verdict in one paragraph

The seven frozen C1 controls cannot tell an honest counter from a counter that passes them by reacting to the
harness's environment, to the published mutation text, or to a spot-check of exactly the sites the controls touch.
Of 13 counters built (12 cheats and the honest reference), 3 are stopped by the controls (echo, no-op, weak presence).
Eight pass the lane harness 7/7 (parent-process, scratch path, committer, scratch-repo shape, cache, mutation-text key,
spot-check, attribution); seven of those eight admit 10–12 of the 12 non-control probes, and the eighth (attribution)
cannot be separated from an honest counter by the harness. A ninth (consistent forgery) passes end to end on its own
re-pinned tree.
The biggest hole is structural: the harness only ever sees bad trees in its own environment (scratch single-commit repos with a `ctl` committer, under `--work`,
as a child of the harness), and the predicate's counter line runs in a different environment. Several cheats are
honest for the harness and green for every real lane tree. Separately, the harness, counters and constants are not in
the freeze commit, so a consistent forgery (tree + tables + counter constant re-pinned together) passes end to end.

## 2. What I did (commands and decisive output)

Setup, read-only on the lane (`git -C` on the lane for reads only):

```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse --show-toplevel
  -> /home/vgpnk/Projects/shokunin/mado-shokunin
git -C <lane> show --stat --format='%H %cd %s' 54dacbd843d64ba744cd3f1bdc2ec622e5010039
  -> 54dacbd8... Wed Oct 28 18:46:52 2026 -0300 round-55: freeze claims, registration, tables, fixtures, controls and baseline before any dispatch
git -C <lane> ls-tree -r --name-only 54dacbd843d64ba744cd3f1bdc2ec622e5010039 -- quality tools | grep -i -E 'r55|kbdopt|controls|freeze-order'
  -> (no output, exit 1)
sha256sum .ufo/waves/round-55/frozen-tables.json
  -> bf46c8896a1861fec746f8900aabe54faf7aaaa3ff5691ed0a05e8e9d4179490 (matches the constant in the w1 spec)
```

Honest reference (`lab/r55lab.py:check`, written from §C1) and harness-shaped runner (`lab/check-r55-controls.py`):

```
python3 -I check-r55-controls.py --counter counters/c_honest.py --repo lanemodel --work work/honest
  -> MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK
python3 -I counters/c_honest.py --repo lanemodel --rev HEAD --work work/t0
  -> MADO_KBD_ENTRY: rev=HEAD rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none
```

Full matrix (`python3 -I lab/driver.py`, output in `lab/matrix.txt`; 13 counters; 12 probes each; direct = predicate-style
invocation with `--rev HEAD`, no harness parent):

```
== c_honest      harness(LM) ok 7/7 OK;  probes caught=12 wrong-leg=[] admitted=[]
== c_echo        harness(LM) good=ok controls=0/7 FAIL;  admitted=all 12
== c_green       harness(LM) good=ok controls=0/7 FAIL;  admitted=all 12
== c_presence    harness(LM) good=ok controls=2/7 FAIL;  caught=3 (P06,P07,P08), admitted=9
== c_ppid        harness(LM) good=ok controls=7/7 OK;    caught=0, admitted=all 12
== c_path        harness(LM) good=ok controls=7/7 OK;    caught=0, admitted=all 12
== c_committer   harness(LM) good=ok controls=7/7 OK;    caught=0, admitted=all 12
== c_history     harness(LM) good=ok controls=7/7 OK;    caught=0, admitted=all 12
== c_cache       harness(LM) good=ok controls=7/7 OK;    caught=0, admitted=all 12 (after green run at HEAD, same --work)
== c_mutkey      harness(LM) good=ok controls=7/7 OK;    caught=0, admitted=all 12
== c_spot        harness(LM) good=ok controls=7/7 OK;    caught=1 (P10), wrong-leg=[P05], admitted=10
== c_killsink    harness(LM) good=ok controls=7/7 OK;    caught=12 only by listing every leg
== c_forged      harness(LM) good=bad controls=7/7 FAIL (its constant is for the forged tree);
                 harness(FORGE) good=ok controls=7/7 OK; direct forged tree -> TARGET_MET
```

Extra demonstrations (`lab/receipts/extra-demos.txt`, `lab/c2_demo.py`):

```
harness tamper: c_green + expectations rewritten to TARGET_MET
  -> MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK
C2 hold-out lookup (SIMULATED hold-out; the sealed one was not used):
  (a) frozen ctl lookup-committed: holdout 0/8 (contract: 0/8)
  (b) lookup-ALL over export root: holdout 8/8 committed 18/18
  (c) lookup-ALL, no fixtures above the tool: committed 1/18 (F17, argv [], same usage line), holdout 0/8
freeze-order: GIT_COMMITTER_DATE=2026-10-27T09:00:00-0300 git commit -> committer-date=Tue Oct 27 09:00:00 2026 -0300
```

Negative checks run inside the lab: the honest reference catches all 12 probes with the required leg (so the probe
set is valid); the honest reference passes the good tree and all seven controls once the H-row reading in §4 is applied.

## 3. Channels (full table in cheats.md §0)

Stopped by the contract: echo of frozen tables (0/7); no-op counter (0/7); weak structural presence (2/7 harness,
admits 9 probes). Those stop only because the harness is strict on the seven controls; the probe gap remains.

Not stopped (each has a built counter that passes 7/7 on the harness):
- parent-process sniffing (`c_ppid`) — admits 12/12 probes on direct run
- scratch-path detection (`c_path`) — admits 12/12
- committer identity `ctl@ctl` (`c_committer`) — admits 12/12
- scratch-repo shape, one commit (`c_history`) — admits 12/12
- prior-run cache keyed by `--rev` string (`c_cache`) — admits 12/12 after a HEAD run; conditional on symbolic revs or reused work dirs (not run with a HEAD-form harness)
- keyed on the published control mutation text (`c_mutkey`) — admits 12/12
- spot-check of control-touched sites (`c_spot`) — admits 10/12, wrong-leg on 1
- attribution (`c_killsink`) — harness cannot distinguish; detection honest
- consistent forgery (`c_forged`) — TARGET_MET on a forged tree (ConfigValues numlock default `false` → `true`)
- expectation tampering (harness expectations in a mutable file) — 7/7 with an always-green counter
- C2 hold-out lookup over the export root — 8/8 hold-out; the frozen lookup-committed control does not test this
- freeze-order checker by commit timestamps — forgeable; no control for it

## 4. Defects and ambiguities in the contract (with the input that shows each)

1. **Harness and counters not frozen.** `git ls-tree ... -- quality tools | grep r55` at 54dacbd: no output. The
   freeze adds ctl/, fetch/, fixtures/c2/, receipts/, freeze-verify.py, frozen-tables.json, claims-frozen.md,
   registration.md. Expectations the registration says the harness "holds itself" are therefore candidate-side.
2. **Environment asymmetry.** Controls run in scratch single-commit repos under `--work` with `ctl` committer; the good
   run runs in the lane. The contract does not require controls to share the predicate's environment. This is what
   channels 4–7 exploit (see cheats.md §1).
3. **`host:<id>` unreachable under the literal reading.** "H row whose quote is not a substring of that line". The
   frozen quote is always a substring of its own pin line. The first lab run (literal reading) gave
   `C1-CTL-6 ... missed=quote:H02` only, so control 6 failed. I used the row-cell reading (the leg tests the quote in
   the row cell). Recorded as A3.
4. **"Named leg" is not exclusive.** Harness check is presence of the leg in `missed=`. A list-all counter passes
   7/7 (`c_killsink`). Recorded as A4.
5. **`tables_sha` vs "refuse".** §C1 says counters "refuse a tree whose frozen-tables.json differs" and also defines
   `tables_sha` as a leg. C1-CTL-7 changes the tables and requires `pin_hash`; a counter that refuses prints no
   `missed=` line and fails the control for the wrong reason. Recorded as A5.
6. **K17 source rule is unsatisfiable as written.** §C1 requires the registry URL to "contain the frozen commit".
   K17 reuses S052; its URL is `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml`,
   which does not contain `efb50993…`. A waiver is needed for `wayland-*` pins. Recorded as A6.
7. **K16 quote contains a pipe.** `frozen-tables.json` `c1.k` K16 quote is `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())`.
   §C1 says "no `|` inside a cell". The lab builder asserted on it; I joined tail cells. Recorded as A7.
8. **`freeze-verify.py` checks the working tree, not git objects.** `LANE = os.getcwd()` and `open(f"{W}/...")` for
   every pin, quote and fixture. It proves the checkout is self-consistent, not that it matches 54dacbd or upstream.
   Recorded as A8.
9. **Hold-out commitment base unspecified** (`<relpath>` relative to what). Recorded as A9.
10. **`--rev` form and `--work` freshness unspecified** (precondition for the cache channel). Recorded as A10.
11. **C1 controls only sample the mutation space** (7 sites). Probes P01–P12 show the gap: the spot-check counter
    passes 7/7 and misses 10 of 12 probes.
12. **C2 control `lookup-committed.py` reads only `fixtures/c2`**, so the frozen controls do not test a lookup over
    the export root. The hold-out is exported into the tool's tree at integration, so the frozen control passes
    while a lookup-all counter gets 8/8 on hold-out (C2-a). The only defence in the text ("reads only the files named")
    is not enforced.
13. **Freeze-order checker has no control and trusts commit timestamps** (F-1; demonstrated with `GIT_COMMITTER_DATE`).

Recommended fixes (cheats.md §7): run controls in the predicate's own environment; make counters environment-invariant
and test them in two environments; sample a sealed random defect set in addition to the seven controls; require exact
`missed=` sets; freeze the harness, counters and constants and anchor pins and tables to `git show <freeze>:…`; settle
A3, A5, A6, A7, A9, A10 in the text; run C2 tools with no fixtures above them; anchor the freeze-order checker to git
objects, not timestamps.

## 5. What I could not verify

- **The real harness.** It is not in the lane at the freeze and is not written yet. `lab/check-r55-controls.py` is my
  reconstruction, and results on the real harness may differ in details A1–A6.
- **The real entry, counters and C2 tool.** Not read. The lane model uses a synthetic entry built from the frozen tables
  and registry rows I wrote for the lab. `tools/mado-kbdopts.py` does not exist at the freeze.
- **The sealed C2 hold-out.** Not looked for, not opened, not used. `fixtures/c2-holdout/` does not exist in the lane
  at the freeze, and I did not read it. The C2 demonstration used a simulated hold-out I wrote in scratch.
- **C3 counter and controls.** Not built (no C3 counter exists at the freeze). The expected result that a spot-check
  passes all six C3 controls is an inference, not run.
- **HEAD-form harness for the cache channel.** Not run. The cache channel is shown with a direct HEAD run after a green
  HEAD run, not with the harness itself using symbolic revs.
- **Time-gated and environment-variable cheats.** Not built (no env var is set by the contract's harness; no
  time-dependent path is needed). Reasoning only.
- **Parser behaviour for multi-line counter output.** Not built. The contract says "one line"; the harness's handling of
  two lines is unspecified.
- **The first lab run used the literal H-row reading** and its control-6 result (`missed=quote:H02`) is the receipt
  for A3; I did not keep a copy of that log in the receipts (the run was superseded by the patched reading, which
  is in `lab/r55lab.py`). The patched behaviour is in `lab/receipts/harness-honest-lane.log`.

## 6. Tooling, host and scope bounds

- **Tooling.** No installs or upgrades. Python 3 stdlib (`python3 -I`) and git only. Nothing added to any PATH.
- **Host.** No host reads (`~/.config/hypr/input.conf`, `hyprctl`) were made by this seat. The lab does not touch the
  host.
- **Lane.** Read-only git on `/home/vgpnk/Projects/shokunin/mado-shokunin` (`log`, `show`, `ls-tree`, `archive`,
  `cat-file`, `rev-parse`). No edits to tracked files, no commits, no pushes, no git/jj mutations, no writes to the
  fleet repo, sibling lanes or shokuknow. The only lane-side writes are this report and the `w1/R55CritControls/`
  directory (cheats.md and lab/).
- **Scratch.** All clones, fixtures and work trees were under `/fast/scratch/hyaku/mado-r55/R55CritControls/` (lane
  model, probe clones, forged clone, control trees, simulated C2 tree). Nothing under `/tmp`. Scratch is removed
  before yield; the sources and receipts are copied into `w1/R55CritControls/lab/` first. The copied counters
  import `r55lab` from the absolute scratch path, noted in cheats.md §8.
- **No subagent dispatch.** Leaf member.
- **Git identities.** Lab commits use `ctl <ctl@ctl>` for control trees and `L1 <l1@lane.model>` for lane-model,
  probe and forged commits, in scratch only.
