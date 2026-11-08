---
author: hyaku closure (non-author integrator, @m_zfl)
round: 99
lane: mado
lane_round: 99
base_rev: 2cbaa141f42df9dfeee4d207cae6558a4dd59863
lane_head: 0e8f39f50012625e17aad8d97f29e16ddcae9916
report: .ufo/reports/round-99/mado.md (fleet f9920699, first filed 16dba8ef)
verified_at: 2026-11-08
verdict: rejected-honest-stop
---

# mado round 99 — non-author verifier spot-check

I did not author this round. Everything below is re-derived from committed bytes or re-opened
sources; where a lane-owned gate is the evidence I verified its committed receipt and its pins
rather than executing a sibling's gate (`PROTOCOL.md` §Gate standard, Closure consequence).

## 1. Conformance (step 1)

| Check | Command | Observed |
|---|---|---|
| report committed by the lane identity | `git log --format='%an %H' -- .ufo/reports/round-99/mado.md` | `mado-shokunin 16dba8ef…` (first filing) and `mado-shokunin f9920699…` (misroot note); both ancestors of fleet `9021f7a6` |
| report has the `SHONEN` heading, one line per box | `grep -n '^## SHONEN' .ufo/reports/round-99/mado.md` | `177:## SHONEN`, four `[~]` lines, each with a resolvable pointer |
| every cited lane commit exists and is an ancestor of `master` | `for h in 56a9b299 87ebed1a dc0a8637 19835e0e e39cd5e0 4c7cf0cb 3b69f041 0e8f39f5; do git merge-base --is-ancestor $(git rev-parse $h) master; done` | all eight OK (no dead, no orphaned hash) |
| lane pushed, no uncommitted round work | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git -C … status --porcelain` | `local=0e8f39f5 remote=0e8f39f5 ahead=0 behind=0 tracked=0 untracked=0`; status empty; `ls-remote origin refs/heads/master` = `0e8f39f5` |
| prompt carries the template contract | `.ufo/prompts/mado-round-99.md` | mission/axes binding (§1), 1–3 claim contract (§2), frontier step (§2b), L2 floor ≥8 (§3), report contract + path/filename + `SHONEN` + commit-hash citation (§4), commit-then-push and push scope and the L0 channel (§5), the report-lands-last and cite-the-pushed-hash clause (§6, lines 516/521). All five child-lane items present |
| report filed after its commit | report cites `0e8f39f5` = lane tip; fleet report commit follows every lane commit | OK |

Conformance defects (status-neutral, named here): none material. Two arithmetic/pointer defects are
routed in §6 below.

## 2. Claims re-checked (step 2)

### C1 — coverage (capability: the launch spawn environment)

Re-measured myself over committed bytes (not the lane's counter):

```
$ git ls-tree 2cbaa141 tools/mado-launchenv.py            # -> (no output: absent at base)
$ git ls-tree 0e8f39f5 tools/mado-launchenv.py            # -> 100755 blob dfc0976e…
$ git show 56a9b299:tools/mado-launchenv.py | sha256sum   # -> a63c20c8…eb16 = --expect-tool-sha256
$ git show 56a9b299:.ufo/waves/round-99/controls/launchenv-cases-r99.json | sha256sum
                                                          # -> 14b4cc57…82acd = row pin
$ python3 -c 'json: cases=67 classes=31 mutants=69'       # -> cases 67, classes 31, mutants 69
$ sha256sum /usr/bin/gio                                  # -> d2164260…cfc462 = the pinned oracle
```

Receipt evidence (verified, not re-executed as a full run; the counter's own 300 s wall is longer
than this session's per-command budget under fleet load, and the pins above bind its inputs):
`.ufo/waves/round-99/receipts/c1-measured-r99.txt:12` prints
`TARGET_MET pred=PRED-C1-r99-v1 … cases=67 correct=67 classes=31/31 … mutants=69 killed=69/69
crashed_not_killed=0 survived=0 class_kills=31/31 fresh=60/60 fresh_seed=7d00c2c940ceb88e …
control_naive=1/67 control_held_r98=4/67`, all `*_pin=ok`. The reported numbers match the receipt
exactly, and the receipt's inputs are the pinned bytes I re-hashed above.

Separability: `c1-at-base-r99.txt` prints `SETUP_ERROR … tools/mado-launchenv.py absent at
2cbaa141` (exit 2) — the before-state is a real refusal, not a claim. The candidate runs read-only:
`python3 -I tools/mado-launchenv.py` with no arguments answers
`MADO_LAUNCHENV: ERROR desktop-file detail=unreadable`; the extracted at-`56a9b299` copy refuses
with `SETUP_ERROR execargv-missing detail=…` (the SKILL row's exit-3 map).

**C1 verdict: improved (coverage). Measured/evidence-verified.**

### C2 — operability (the harm watch as an instrument)

Re-measured myself over committed bytes:

```
$ git ls-tree 2cbaa141 quality/harm-watch.py              # -> (no output: absent at base)
$ git ls-tree 3b69f041 quality/harm-watch.py              # -> 100755 blob fda00729…
$ git show 3b69f041:quality/harm-watch.py | sha256sum     # -> 37a0544b…65b9 = --expect-gate-sha256
$ git show 3b69f041:.ufo/waves/round-99/controls/harm-panel-r99.json | sha256sum
                                                          # -> 160763ce…e39a = --expect-panel-sha256
$ python3 -c 'json: expect_legs/timeout/legs'             # -> 28 / 600 / 28 legs; both
                                                          #    r92_gate_defects and r97c1_filetype present
$ ls .ufo/waves/round-99/controls/harm-planted/           # -> clean, dropped-leg, extra-leg,
                                                          #    wrong-expect, wrong-marker (5 panels)
```

The claim's committed measurement is a miss, and it says so:
`.ufo/waves/round-99/receipts/c2-measured-r99.txt` prints
`MADO_HARM_WATCH: TARGET_MISSED pred=PRED-C2-r99-v1 … panel_legs=28 declared_legs=28 legs_run=28
mismatches=2 … missed=mismatches_zero`, exit 1; the two-leg probe
(`c2-probe-r99.txt`) reproduces both legs at `rc=124 timeout-after-600s` under load average 327.
The frozen predicate's `mismatches == 0` conjunct is therefore **unmet**: the claim does not
verify. The instrument itself, its census and its five planted controls are real and their
discrimination evidence is green, but the declared before→after target is not reached.

Separability: `SETUP_ERROR … quality/harm-watch.py absent at 2cbaa141` (exit 2).

**C2 verdict: unchanged (operability).** The declared move does not verify; no prior artifact
regressed (see §3), and the lane routed the repair to round 100 as its own A9.

## 3. No axis harmed

```
$ git diff --stat 3b69f041 0e8f39f5                     # 16 files, +579 / -1 (the one deletion is the
                                                        #   claims-declaration freeze-block fill)
$ git diff --name-status 2cbaa141 0e8f39f5 -- tools/ quality/
A quality/counters/c1-r99-launchenv.py
A quality/counters/c2-r99-harm-watch.py
A quality/harm-watch.py
M quality/tool-ledger.md
A tools/mado-launchenv.py
```

The standing gate `tools/mado-verify.sh` is untouched, no existing counter changed, and every
SCORECARD/QUALITY/LOG/lesson edit is additive (`git diff --stat 2cbaa141 0e8f39f5 --
SCORECARD.md corpus/QUALITY.md` → `+56` / `+36`, zero deletions). No axis is harmed.

Per-axis grades: **coverage improved**, **operability unchanged**, **depth unchanged**,
**freshness unchanged**, **calibration unchanged**, **adjacency unchanged** (no claim, no harm).

## 4. Discernment spot-check (step 3)

`corpus/lessons/round-99.md` `## Gate` admits three rows and rejects none this round; the reject
side of that gate is therefore untested. I sampled all three admits and two reject-class decisions
that hold equivalent weight for this round (the round's own assimilation refusal, and a round-98
gate reject re-opened to test the gate's discrimination).

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S532 `gio-tool-launch.c` | admit (A) | live `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gio-tool-launch.c` — HTTP 200, sha256 `16b4c868…6595a` | agree | quote `args = g_list_append (args, g_file_new_for_commandline_arg (argv[i]));` is at `:116` (6 words), the live bytes hash to the row's pin, and the round-98 lesson's listed-but-unregistered row is a real registry gap |
| S533 `gutils.c` | admit (A) | committed `.ufo/waves/round-99/fetch/gutils.c` sha256 `65086c29…3771`; `grep -n 'Locates the first executable named'` | agree | the quote is at `:280-281` exactly as the Gate row says (17 words), the scope is new on a file already held (S506) and the census W04 for it is expected and declared |
| S534 recognised-keys spec | admit (A) | committed `fetch/spec-recognized-keys.html` sha256 `7bc0b640…03d9`; second fetch `spec-terminal-path.html` byte-identical; quote at rendered `:128` | agree | `If entry is of type Application, the working directory to run the program in.` (14 words) is the located sentence, and the `Terminal` sentence at `:130` supports the second half of `teaches` |
| round-99 assimilation: "none" | reject the staged theme | `/home/vgpnk/Projects/shokuknow/merge/mado/MERGE-REPORT.md`; `grep -niE 'launch\|terminal\|Exec=\|TryExec\|Path='` | agree | the sweep returns no hit on the launch/terminal/Exec plane, so the refusal is correct and is not a silent skip |
| round-98 gate: `%d`/`%n`/`%N` "unimplemented" | reject as a model fact | `.ufo/waves/round-98/fetch/gdesktopappinfo.c`; `grep -nE "case 'n'\|case 'D'\|case 'N'"` | agree | cases `'d'`/`'D'`/`'n'`/`'N'` are all implemented at `:2528-2539` (and `:2621-2641`), so the spec's "unimplemented" reading is a model fact the bytes refute — the gate's reject side discriminates |

Both refuses are real refusals with reasons, and the three admits are all tier-A primary sources
opened this round with ≤25-word located quotes. No disagreement to convert into a criterion.

## 5. Trend verdicts (my own, with evidence)

- **expansion — improved.** One admitted knowledge entry on ground the coverage map did not hold
  (`corpus/knowledge/gio-launch-env-r99.md`, provenance trio present) citing three `mined` rows
  opened this round (S532/S533/S534), plus a capability row in `SCORECARD.md` demonstrated by a
  receipt; `corpus/SOURCES.md` 466 → 469 rows (my census run: `rc=0`, `rows=469`, `ok`).
- **quality — improved.** The round-98 record errors are re-verified and corrected append-only
  (fresh seed `f00d3edc…` against the row's `e2bf4d1b…`; the gated revision's `462/118` against the
  row's `466/119`), the admitted entry carries its trio and a 69/69 mutant kill, and QUALITY gains
  criteria 170–172; no admitted entry is shown false or stale-and-unmarked.
- **discernment — improved.** The wave's attack seats falsified three claim sentences and the
  round narrowed them pre-file (A1/A3/A4/A5/A6) instead of filing the wider wording; the
  attempt-4 re-derivation caught the C2 miss and reported `TARGET_MISSED` rather than reusing the
  unrecorded attempt-3 `TARGET_MET`; M99-3 became QUALITY criterion 172; and my outside sample
  agrees on every admit and every reject I re-opened.

## 6. Routed defects (lane to fix in round 100)

1. **Off-by-one pointer (record accuracy).** `corpus/lessons/round-99.md` M99-3 and
   `corpus/QUALITY.md` criterion 172 state `git show 2cbaa141:tools/mado-mime.py | grep -n 'def
   find_program'` prints `:467`; it prints `466` (`467` is the docstring line that names
   `g_find_program_for_path`, which is a defensible pointer but not what the command prints).
   Correct the stated output append-only, or cite the docstring line by name.
2. **Attack-share arithmetic.** The report and SCORECARD row say "attack 6/12 = 50 %"; the twelve
   seats carry five attack roles (2 reviewers, 1 critic, 2 mutation-testers) and the connector is
   not an attack role under the campaign definition — 5/12 = 42 %, still above the ≥25 % floor.
   Count attack roles only in the round-shape sentence.
3. **C2 panel headroom (already routed by the lane as A9).** The frozen 600 s per-leg cap has no
   headroom for `r92_gate_defects` / `r97c1_filetype` under fleet load, so the lane's cross-round
   harm watch turns red from host load alone. Re-freeze the cap above the measured worst leg plus
   headroom, or declare a per-leg expectation; do not move the target after the data.
4. **C1 A8 residual.** The unset-PATH default branch is modelled but no frozen case exercises it:
   add a frozen case or drop the modelled branch from the claim's surface list.
5. **Unreceipted measured line.** The attempt-3 `TARGET_MET` line left no receipt; the report
   discloses it correctly. Keep the practice: every measured line lands with its receipt in the
   same commit.

Promotion note for the operator (promotion is operator-owned; I wrote no `[x]`): all four
`SHONEN.md` boxes look checkable by a non-author from resolvable evidence — SKILL rows
`:2983-2986` + prose `:3013-3034`, the round's end-to-end task and its LOG entry, the pinned
counting argv in `claims.json`, and the connector sweep — so a promotion review is available to
the operator whenever they choose to run it.
