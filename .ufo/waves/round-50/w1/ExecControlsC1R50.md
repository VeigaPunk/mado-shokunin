# ExecControlsC1R50 — section-9 do-nothing controls for PRED-C1-r50

Seat `ExecControlsC1R50`, mado round 50 (hyaku run 9), wave w1, 2026-10-27. Lane
`mado-shokunin`; scored revision `8ae47b957034ae21012bbf09173cca2c48be345e` (round-50 base);
round-49 counter `quality/counters/c2-r49-bind-entry.py` sha256
`bc171714c5349dbe980b84f5c434126965cc8a6e8226704c28604d10cff28c69` — `git show
8ae47b95:quality/counters/c2-r49-bind-entry.py | sha256sum` gives the same digest, so the
instrument run here is the committed frozen one, not a worktree variant.

## 1. Verdict

- **8/8 controls read `TARGET_MISSED` with exit 1 on the frozen round-49 counter**
  (`receipts/controls-r49.txt`, `BUILD-CONTROLS: ... verdict=ALL_MISSED`). Each one stops at a
  named clause, and the clause that stops it is the control's own delta wherever the control
  can reach that clause.
- **The same 8 controls read `TARGET_MISSED` on the PRED-C1-r50 draft**, snapshot
  `.../w1/ExecCounterC1R50/c1-r50-bind-entry.py` sha256
  `17ad31c1d9bd9571b499f9d9bce7ee0066ec2f154d7af68c352f16399f068908` (amended after my first
  run against `3e2bf669…`, whose verdicts were identical), copied to scratch before the run so
  a live edit cannot move it (`receipts/controls-c1draft.txt`). There the misses are
  structural: `OLDPATHS` is `clause=a entry_absent`, and every other control stops at the
  counter's fetch gate `clause=c fetch_pins=0 under .ufo/waves/round-50/fetch/` because that
  directory is still empty at the scored revision.
- **The counter is satisfiable, and the round-49 stop's stated reason does not reproduce.**
  `PROBE FULL` (the committed round-49 candidate plus an index row plus 12 Gate admit lines,
  nothing else) scores `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1
  verdict=TARGET_MET` (`receipts/r49-logs/full.log`, last line). That is a measurement, not a
  judgement; §5 F1 routes it.

## 2. What each control holds

One `git clone --shared` per control into `--work`, toplevel verified equal to the clone dir,
the control committed there under a throwaway identity, then the counter run as
`python3 -I <counter> --repo <clone> --rev HEAD` (+ the counter's own `BASE_DEFAULT` unless
`--base` is given) with `HOME`/`XDG_*` under `--work` and `TMPDIR=--work/tmp`.

| control | substrate written into the clone | at which paths |
|---|---|---|
| BASE | nothing (empty commit) | — |
| STUB | provenance head with 3 real registry ids (S349-S351) + `verified-at` + `recheck` + one sentence | counter `ENTRY` |
| HELD | same head + `corpus/knowledge/keybind-rule-semantics.md` §2.3 pasted verbatim | counter `ENTRY` |
| OLDPATHS | round-49 candidate entry (131 lines) + its 12 rows in the Registry + its live receipt, all byte-unchanged | **round-49 paths** (`corpus/knowledge/hyprland-bind-key-match-r49.md`, `.ufo/waves/round-49/receipts/`) |
| NOLIVE | same candidate at the counter's paths, receipt file removed (entry's receipt line kept) | counter `ENTRY`/`RECEIPTS` |
| NOROWS | same candidate, no registry rows appended | counter `ENTRY`/`RECEIPTS` |
| FORGEDQUOTE | same candidate with one step quote changed by one word (`case-insensitive`→`case-sensitive`; the counter reports it at its unfenced-line index 61) | counter `ENTRY`/`RECEIPTS` |
| BRANCHURL | same candidate with row S352's URL ref `efb50993…` replaced by `main` | counter `ENTRY`/`RECEIPTS` |
| PROBE FULL | candidate + one `knowledge/` index row in `corpus/README.md` + 12 `**S### admit**` lines inside the existing `## Gate` of the lesson | counter `ENTRY`/`RECEIPTS` |

`OLDPATHS` deliberately keeps the round-49 paths. On the round-49 counter those are its own
paths, so it is the substantive attack; on a counter that names round-50 paths it can only be
`a:0`, which is the property the control exists to show. The four `…/counter paths` members
are the same bytes relocated so they can reach the counter's later clauses.

## 3. Results — frozen round-49 counter (PRED-C2-r49, sha256 `bc171714…`)

From `receipts/controls-r49.txt` (verbatim, one line per control; logs per control in
`receipts/r49-logs/`).

| control | exit | clause vector | first failing clause and the line that pins it |
|---|---|---|---|
| BASE | 1 | `a:0` | `a` — `receipts/r49-logs/base.log:1` `clause=a entry_absent` |
| STUB | 1 | `a:1 b:0 c:0 d:1 e:0 f:0 g:0 h:0 i:0 j:0 r:0` | `b` — `r49-logs/stub.log:1` `clause=b id=S349 present_at_base`, `:7` `readme_rows=0` |
| HELD | 1 | same as STUB | `b` — `r49-logs/held.log:7` `readme_rows=0`; `:29` `new_rows=0 … overlap=0.417` (the paste would also fail `i`'s novelty probe) |
| OLDPATHS | 1 | `a:1 b:0 c:1 d:1 e:1 f:1 g:1 h:1 i:0 j:1 r:1` | `b` — `r49-logs/oldpaths.log:1` `clause=b readme_rows=0` |
| NOLIVE | 1 | `a:1 b:0 c:1 d:1 e:1 f:0 g:1 h:1 i:0 j:1 r:0` | `b` (readme) and its own delta `f` — `nolive.log:24` `clause=f receipt_missing=.ufo/waves/round-49/receipts/binds-live-r49.txt` |
| NOROWS | 1 | `a:1 b:0 c:0 d:0 e:0 f:1 g:1 h:1 i:0 j:0 r:1` | `b` — `norows.log:11` `clause=b ghost_ids=['S352','S353','S354','S355','S356','S357']` (`c/d/e/j` fall with the rows) |
| FORGEDQUOTE | 1 | `a:1 b:0 c:1 d:0 e:1 f:1 g:1 h:1 i:0 j:1 r:1` | `d` — `forgedquote.log:14` `clause=d quote_not_in_pin line=61 pin=xkbcommon-keysym.c q='The "best" case-sensitive match is the lower-case keysym name.'` |
| BRANCHURL | 1 | `a:1 b:0 c:0 d:1 e:1 f:1 g:1 h:1 i:0 j:1 r:1` | `c` — `branchurl.log:4` `clause=c id=S352 url_branch_ref:https://raw.githubusercontent.com/hyprwm/Hyprland/main/src/managers/KeybindManager.cpp` |
| PROBE FULL | 0 | `a..r all 1` | none — `r49-logs/full.log` last line `admitted=1/1 verdict=TARGET_MET rev=ff692955…` |

Reading the bundle:

- `FORGEDQUOTE`, `BRANCHURL`, `NOLIVE` and `NOROWS` each turn their own clause red
  (`d:0`, `c:0`, `f:0`, `b:ghosts` + `c/d/e/j:0`) **while every clause the other seven keep
  passes** — the deltas are individually attributable in the clause vector, not just in prose.
- The `b` miss shared by the candidate family is one fact, not five: the round-49 material has
  no `corpus/README.md` index row for its entry (`readme_rows=0`), so `b` fails before anything
  else can. This is the assembly gap that PROBE FULL closes, and it is the whole of the
  difference between `OLDPATHS` (`b:0`, rest `1`) and `PROBE FULL` (`all 1`).

## 4. Results — PRED-C1-r50 draft (sha256 `17ad31c1…`)

From `receipts/controls-c1draft.txt`, logs in `receipts/c1draft-logs/`.

| control | exit | vector | stop |
|---|---|---|---|
| BASE | 1 | `a:0` | `a entry_absent` (`c1draft-logs/base.log:1`) |
| OLDPATHS | 1 | `a:0` | `a` — round-49 paths are invisible to a round-50 counter (its own purpose) |
| STUB, HELD, NOLIVE, NOROWS, FORGEDQUOTE, BRANCHURL | 1 | `a:1 b:0 c:0` | `b` on the per-clause lines, then `c` — `c1draft-logs/stub.log` `clause=b readme_rows=0`, `clause=c fetch_pins=0 under .ufo/waves/round-50/fetch/` |

The first run of this bundle was against draft `3e2bf669…`, whose no-pins short-circuit printed
the literal `a:1 c:0`; the counter seat amended it to build the vector from what it evaluated
(their receipt `.ufo/waves/round-50/w1/ExecCounterC1R50/receipts/control-no-pins.txt`), and the
run above is the amended bytes. Verdicts and the `a`/`c` stops are unchanged; only the vector
now names `b`. At the scored revision
`.ufo/waves/round-50/fetch/` holds no pins, so **no control can reach clauses beyond `c` until
ExecFetchR50's pins are committed**; the bundle must be re-run at the revision that carries
them, on the frozen counter. Until then the draft run proves only the `a`/`c` gates.

## 5. Findings

**F1 — the round-49 candidate is admitted by the frozen round-49 counter once an index row and
Gate admit lines exist; the registration's stated failure (`clauses b/c/d/e/j fail on row-pin
binding and quote attachment`, `round-49/registration.md:24-31`) does not reproduce on
committed bytes.** Measured: `PROBE FULL` = the committed
`candidate/hyprland-bind-key-match-r49.md` (131 lines, byte-unchanged), the committed
`candidate/rows.md` (12 rows, 11 cells each) and the committed receipt, plus one README index
row and 12 `**S### admit**` lines inserted into the existing `## Gate`. Tree diff against
`8ae47b95`: 4 files, +157 lines, nothing else (`receipts/probe-full-diff.txt`:
`corpus/README.md | 1 +`, `corpus/SOURCES.md | 12 +++`,
`corpus/knowledge/hyprland-bind-key-match-r49.md | 131 ++++`,
`corpus/lessons/round-49.md | 13 +++`). Clauses `c`, `d`, `e`, `j` pass on the candidate's own
pins and quotes (`r49-logs/full.log`: `clause=c … ranges=…` per row, `clause=d quotes=86`,
`clause=e steps=17 verified_steps=17`, seven `clause=j topic=…` lines), and `r` replays the
live capture equal. Route: round-50 C1 can plan on carrying the entry and rows and adding the
index row, the Gate lines, a fresh round-50 pin set and a fresh receipt — and the round-49
closure's D4/C2 record should name this as an erratum candidate (L1's call, not mine).

**F2 — the Gate requirement is satisfied by bare markers.** The probe's admit lines are
`- **S### admit** control fixture; opened 2026-10-27.` with no located quote; clause `i`
accepts them (`all 1`). So clause `i` measures the presence of `**S### admit**` inside `## Gate`,
not the quoted gate the lesson describes. Declared residual in the counter docstring, but it is
the mechanical reason F1 is cheap; the round-50 freeze should decide whether to keep it.

**F3 — a do-nothing bundle must not assemble the landing.** The same two artifacts that make
`PROBE FULL` pass are exactly what a "complete candidate" assembly tempts a control builder to
add. `OLDPATHS` therefore holds the round-49 bytes *unchanged* (no index row, no Gate lines);
with them it would be a positive control, not a negative one. Any round-50 control bundle that
adds an index row or Gate lines will read `TARGET_MET` for the wrong reason.

**F4 — the fetch gate masks every later clause.** Both counters short-circuit when `FETCH` is
empty (`c2-r49-bind-entry.py:1225-1228`; draft `17ad31c1`:1245-1253). The round-49 counter then
prints the literal `a:1 c:0`; the amended draft prints `a:1 b:<computed> c:0`, so `b` is named
and `d..r` are not scored and not claimed. For a control bundle this means: run it at a revision
whose `FETCH` directory carries the citing rows' pins, or every control reads `c` and the bundle
discriminates nothing. The L1 re-run must therefore name a revision at/after the pin commit.

**F5 — held-text paste is caught only by the novelty metric.** `HELD`'s log shows
`overlap=0.417` (`r49-logs/held.log:28`) against the base tree's 6-word shingles — the counter's
own declared calibration for a one-word-in-nine paraphrase. It does not reach clause `i` here
(no rows, no receipt), but on a substrate that reaches `i` the 0.15 threshold is the only thing
between held text and admission.

**F6 — `r` (live replay) still matches the round-49 receipt today** (`full.log`: `r:1`), i.e.
the host's `hyprctl binds -j` digest still equals the receipt's `9a47199e…`. Not a finding
about the counter; recorded because the probe's admission depends on it and it will not hold
after the next bind change.

## 6. Harness contract (`build-controls.py`, the deliverable)

- `--counter PATH --repo LANE --rev REV --work DIR` (plus `--base`, `--only NAME,…`,
  `--logdir`, `--probe`, `--keep`, `--timeout`). `--work` is required unless `TMPDIR` is set,
  and a work dir under `/tmp`, `/var/tmp`, `/dev/shm`, or inside `--repo` is refused with exit 2
  (`receipts/refusals.txt`: four refusals, `exit=2` each, nothing created under `/tmp`).
- Paths come from the counter's own constants (`ENTRY`, `REGISTRY`, `README`, `LESSON`,
  `FETCH`, `HELD_FETCH`, `RECEIPTS`, `PRED`, `BASE_DEFAULT`, `OPENED`), so the frozen round-50
  counter is scored at round-50 paths with no edit to either file.
- Scratch clones only: `git clone --shared` from `--repo`, `git rev-parse --show-toplevel`
  asserted equal to the clone before the first commit, commits under
  `-c user.name=control -c user.email=control@control.invalid -c commit.gpgsign=false -c
  core.hooksPath=/dev/null`. No lane write, no `pack`/`gc`, clone removed after scoring.
- Output: one `CONTROL name=… exit=… verdict=… first_fail=… final=…` line per control, plus a
  `BUILD-CONTROLS:` summary line; exit 0 iff all controls missed, 1 if any was admitted, 2 on a
  refusal or an unrunnable control. Per-control counter output goes to `--logdir`.

## 7. Receipts and commands

Run 1 (frozen round-49 counter):

```
python3 .ufo/waves/round-50/w1/ExecControlsC1R50/build-controls.py \
  --counter quality/counters/c2-r49-bind-entry.py \
  --repo . --rev 8ae47b957034ae21012bbf09173cca2c48be345e \
  --work /fast/scratch/hyaku/mado-r50/ExecControlsC1R50/work --probe \
  --logdir .ufo/waves/round-50/w1/ExecControlsC1R50/receipts/r49-logs
```

Run 2 (draft snapshot `17ad31c1…`, `--work .../work-c1draft`, `--logdir .../receipts/c1draft-logs`).

- `receipts/controls-r49.txt`, `receipts/r49-logs/{base,stub,held,oldpaths,nolive,norows,forgedquote,branchurl,full}.log`
- `receipts/controls-c1draft.txt`, `receipts/c1draft-logs/*.log`
- `receipts/probe-full-diff.txt` (probe tree diff vs `8ae47b95`), `receipts/refusals.txt`
- Harness: `build-controls.py`. Every receipt was produced by this file at its
  delivered bytes; the harness prints the counter path with `~` for the home
  directory, so no receipt carries an absolute home path.

## 8. Risks, limits, and what was not done

- The scored instrument is round 49's frozen counter; the round-50 freeze does not exist yet.
  Run 2 is a snapshot of a live draft (sha256 `17ad31c1…`, copy made before the run), so it is
  a reading of those bytes, not of whatever the freeze becomes.
- Both runs are at `--rev 8ae47b95`; the round-50 probe cannot pass there (no round-50 pins, no
  round-50 entry). F1 is a round-49 measurement and the L1 must decide whether it is an erratum
  for the round-49 record or an input to the round-50 C1 plan.
- The probe's index row and Gate lines are fixture text; F2 is about the counter's reach, not
  about whether such a row would be good prose.
- No tool installation or upgrade was needed. No host state written: `HOME`/`XDG_*` were
  scratch dirs for every counter run, the only host reads were the counter's own `hyprctl`
  replay (`binds -j`, `getoption`, read-only), and scratch was removed.
- Not done, by seat scope: the round-50 counter port, the freeze, any lane commit, and any
  judgement of the round-49 closure.
