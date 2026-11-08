---
author: hyaku closure (non-author integrator, @m_zfl)
round: 100
lane: mado
lane_round: 100
base_rev: 43309e6af9a3b57f1bc839a826bef1f8eb7495e4
lane_head: 37913833a278837f9b892944ba4be95e5ef9a04a
report: .ufo/reports/round-100/mado.md (fleet a813d13e)
verified_at: 2026-11-08
verdict: admitted
---

# mado round 100 — non-author verifier spot-check

I did not author this round. Every number below is re-derived from committed bytes or re-opened
sources; where a lane-owned gate or selftest is the evidence, I verified its committed receipt and
its pins rather than executing a sibling's gate (`PROTOCOL.md` §Gate standard, Closure consequence).

## 1. Conformance (step 1)

| Check | Command | Observed |
|---|---|---|
| report committed by the lane identity | `git log --format='%an %H' -- .ufo/reports/round-100/mado.md` | `mado-shokunin a813d13ecdee475b574ab82f575775acb0853b36`, contained by `origin/main` and `origin/master` |
| report has the `SHONEN` heading, one line per box | `grep -n '^## SHONEN' .ufo/reports/round-100/mado.md` | `213:## SHONEN`, four `[~]` lines, each with a resolvable pointer; no `[x]` (correct — no non-author verdict) |
| every cited lane commit exists and is an ancestor of the branch | `for h in 219e14f4 f94f7a94 18bce790 ae537dbe d73a0648 f791d3c0 37913833; do git merge-base --is-ancestor $h master; done` | all seven OK; no dead or orphaned hash; base `43309e6a` also an ancestor |
| lane pushed, no uncommitted round work | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git -C … status --porcelain` | `local=37913833 remote=37913833 ahead=0 behind=0 tracked=0 untracked=0`; status empty; `ls-remote origin refs/heads/master` = `37913833` |
| prompt carries the template contract | `.ufo/prompts/mado-round-100.md` | mission/axes binding (§1), 1–3 claim contract (§2), frontier step (§2b), L2 floor ≥8 in one batched call (§3), report contract with path/filename + `SHONEN` + marker rule (§4), commit-then-push + push scope + L0 channel (§5), and the report-lands-last / cite-the-pushed-hash / misroot-sweep clauses (lines 448, 454, 472, 516, 521). All five child-lane items present |
| report filed after its commit | report cites lane tip `37913833` = `ls-remote origin refs/heads/master` | OK |
| dispatch vs completion | `.ufo/watchdog.log` | `2026-11-08T01:30:12-03:00 launch mado round=100 pgid=4133656 driver=hyaku-inline attempt=1`; `2026-11-08T05:19:20-03:00 complete mado round=100; hyaku-inline attempt=1` |
| pre-file falsification ledger | `python3 scripts/hyaku/prefile-falsification.py --lane mado --round 100` | `PREFILE-FALSIFICATION: pass claims=2 rows=9 attack_seats=6 findings=0`, exit 0; the 9 rows cover both claims and every attack seat (ReviewC1, ReviewC2, CriticClaims ×2, MutPath, MutHarm, LabratUnset); both `falsifies-wording` rows name a narrowing (A1, B1) |
| corpus census at the tip | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | exit 0, `rows=469` (`grep -cE '^\|…S[0-9]{3,}' corpus/SOURCES.md` → 469), warnings W04/W01 only |

Conformance defects (status-neutral, routed in §6): the report's counter-selftest tallies (`9/9`,
twice) match no committed receipt; the round-shape role split sums to 15 while the wave ran 16
seats; the report's C2 counting command names a different `--rev` than its own receipt.

## 2. Claims re-checked (step 2)

### C1 — coverage (the unset-PATH default branch as a measured case class)

Re-measured myself over committed bytes (not the lane's counter):

```
$ git show 219e14f4:.ufo/waves/round-100/controls/launchenv-cases-r100.json | python3 -c 'cases/classes/path-default'
    cases 77  classes 35  path-default cases 10  classes 4
$ git show 43309e6a:.ufo/waves/round-99/controls/launchenv-cases-r99.json | python3 -c '…'
    r99 cases 67  classes 31  r99 path-default 0
$ sha256sum tools/mado-launchenv.py | cut -c1-16          # -> 3b29dc65111a2f3e = --expect-tool-sha256
$ git show 219e14f4:tools/mado-launchenv.py | sha256sum   # -> 3b29dc65111a2f3e (same bytes)
$ sha256sum tools/mado-execargv.py | cut -c1-16           # -> 49f7fecdc3bef99a = the sibling pin
$ sha256sum .ufo/waves/round-100/controls/launchenv-cases-r100.json | cut -c1-16
                                                          # -> 7aba8a0f880b3e59 = the case pin
$ git show 219e14f4:quality/counters/c1-r100-launchenv-path.py | sha256sum | cut -c1-16
                                                          # -> 3cbcd82fee36140e = the tip counter
$ sha256sum /usr/bin/gio | cut -c1-16                     # -> d216426080f847bf = the pinned oracle
```

The at-base do-nothing control is a real measurement, not a claim: the r99 case file carries
**0** `path-default` cases and both `path-unset` cases give an absolute `Exec`
(`receipts/c1-at-base-r100.txt`: `r99 cases=67 classes=31 path-default cases=0`), and the same
frozen command at `--rev 43309e6a` refuses with `SETUP_ERROR tool sha256 a63c20c8… != pinned
3b29dc65…`, exit 2.

Receipt verified, not re-executed (the counter's own run is minutes of wall under fleet load and its
inputs are the pinned bytes re-hashed above): `receipts/c1-measured-r100.txt` prints
`MADO_C1_R100: TARGET_MET pred=PRED-C1-r100-v1 rev=219e14f4… cases=77 classes=35 default_cases=10
default_classes=4 mutants=6 killed=6 fresh=60 fresh_seed=b13db5203f2db30e control_unset_as_empty=75
base_set_default_cases=…`, all seven `CONJUNCT ok`, and six `MUTANT … killed` rows (`m1` killed by
`pd-dot-root`, `m2` by `pd-dot-root,pd-sysbin-unset`, …). The tool selftest is committed evidence:
`receipts/c1-tool-r100.txt:7` → `MADO_LAUNCHENV_SELFTEST: checks=95 failed=0`.

The `m1`/`m2`-survive-the-r99-set gap proof is the load-bearing part of the narrowed statement
(`controls/launchenv-mutants-r100-probe.txt`), and the entry that rests on it cites S533.

**C1 verdict: improved (coverage). Measured + evidence-verified.**

### C2 — operability (the harm watch's per-leg cap, measured)

Re-measured myself over committed bytes:

```
$ git show 43309e6a:quality/harm-watch.py | grep -c 'elapsed'    # -> 0 (absent at base)
$ sha256sum quality/harm-watch.py | cut -c1-16                   # -> acecb0ea42572685 = gate pin
$ git show ae537dbe:quality/harm-watch.py | sha256sum | cut -c1-16  # -> acecb0ea42572685 (same)
$ git show 43309e6a:.ufo/waves/round-99/controls/harm-panel-r99.json → timeout_s 600, legs 28
$ python3 -c 'json: r99 vs r100 panel'   # -> timeout 600 → 3600; legs equal True (28/28);
                                         #    the only differing key is timeout_s
$ sha256sum .ufo/waves/round-100/controls/harm-panel-r100.json | cut -c1-16  # -> 6d259164de900f99 = pin
$ sha256sum .ufo/waves/round-100/receipts/panel-timing-r100.txt | cut -c1-16 # -> e7280b53a90caa36 = pin
$ grep -c '^LEG' …/panel-timing-r100.txt                        # -> 28
$ grep -n 'TIMING-DONE' …/panel-timing-r100.txt                 # -> 36:TIMING-DONE rev=43309e6a…
$ awk 'elapsed_ms > 600000' …/panel-timing-r100.txt             # -> exactly one: r92_gate_defects 708014
```

The `h3b` fix is in the committed bytes, not only in prose: `quality/harm-watch.py:539-543` parses
`elapsed_ms=(\d+)` and requires `int(...) >= 1000`, with the comment naming the substring bug.

Receipt verified: `receipts/c2-measured-r100.txt` prints `MADO_C2_R100: TARGET_MET
pred=PRED-C2-r100-v1 rev=d73a0648… gate_sha256=acecb0ea… panel_legs=28 legs_run=28 mismatches=0
selftest_failed=0 max_elapsed_ms=708014 control_600s_would_mismatch=1 timing_legs_timed=28 exit=0`,
all nine `CONJUNCT ok`, and `GATE_SUMMARY HARM_WATCH: legs=28 ok=28 mismatch=0` over 28 printed
`GATE_LEG` lines. Runs 1–2 (`mismatches=1`, `r97c1_filetype` rc=2 from a deep scratch root) are
disclosed with their measured cause and with a standalone green leg
(`c2-leg-r97c1-standalone-r100.txt`). The gate selftest tally is committed:
`receipts/c2-gate-r100.txt:6` → `HARM_WATCH_SELFTEST: checks=33 failed=0`.

**C2 verdict: improved (operability). Measured + evidence-verified.**

## 3. No axis harmed

```
$ git diff --stat 43309e6a 37913833 -- quality/harm-watch.py   # 59 added / 8 removed, all inside the
                                                               #   docstring line, the return dicts and the
                                                               #   LEG line (elapsed_ms added; no census,
                                                               #   exit-map, --only/--timeout/scratch or
                                                               #   json-key change)
$ git diff --stat 43309e6a 37913833 -- SCORECARD.md corpus/QUALITY.md corpus/README.md LOG.md SKILL.md
                                                               # +40 / +23 / +3 / +61 / +11: all additive
$ git diff --name-status 43309e6a 37913833 -- corpus/lessons/round-99.md   # M, +10 (append-only errata)
```

No existing counter changed; no admitted entry is shown false or stale-and-unmarked; the round-99
append-only errata cite the superseded text (§6), which is the contract for corrections. The tools
the gate judges are untouched (`tools/mado-launchenv.py` gains selftest-only lines: 29 changed
lines, all inside the selftest body per `w1/R100MMutPath.md`).

Per-axis grades: **coverage improved**, **operability improved**, **depth unchanged**,
**freshness unchanged**, **calibration unchanged**, **adjacency unchanged** (no claim, no harm).

## 4. Discernment spot-check (step 3)

`corpus/lessons/round-100.md` `## Gate` admits one row (S533) and rejects one (the staged `S205`
Hyprland dispatcher row). I re-opened both, plus the registry cell the admit moved.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S533 `gutils.c` (PATH default) | admit (A) | live `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gutils.c` — HTTP 200, `sha256 65086c293646bf83884f56f54bb5e2e872adb28ee77f1223d6d9f095a75e3771`, 100534 B | agree | `grep -n '"/bin:/usr/bin:\.'` prints `388:` and `sed -n '376,389p'` shows the unset block closing with `path = "/bin:/usr/bin:.";` — the lesson's quote (`path = "/bin:/usr/bin:.";` at `:388`, block `:376-389`) is exactly located, ≤25 words, and the live bytes hash to the row's pin |
| staged `S205` Hyprland dispatchers (shokuknow `merge/mado/SOURCES.append.md`) | reject (assimilation: none) | live `raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a…/content/configuring/core/dispatchers.md` — HTTP 200, 12879 B, sha256 prefix `c830ce07…` as the staged row states | agree | the only `elapsed` hit is `:69`: `force_idle( int ) | Sets elapsed time for all idle timers in seconds, ignoring idle inhibitors.` — an idle-timer dispatcher, not a per-leg wall clock and not GLib's launch environment; the reject names the theme boundary and a concrete flip condition |
| S533 `used-by` cell (registry move) | status/used-by change | `awk -F'|' '$2 ~ /S533/ {print $12}' corpus/SOURCES.md` | agree | the cell now reads `corpus/knowledge/gio-launch-env-r99.md, corpus/knowledge/gio-launch-path-default-r100.md` (comma-separated, which the read-back gate requires); registry rows stay 469 and knowledge entries are 121 (`ls corpus/knowledge/*.md | wc -l`), matching the round's `entries=121` claim |

No disagreement to convert into a criterion. One observation for the lane's own gate: neither
attack seat re-opened its claim's selftest tally, which is where the round's false numbers survived
(§6.1).

## 5. Trend verdicts (mine, with evidence)

- **expansion — improved.** One admitted knowledge entry on ground the coverage map did not hold
  (`corpus/knowledge/gio-launch-path-default-r100.md`, provenance trio present, `source:` citing
  S533 — `mined`), a `SCORECARD.md` capability row demonstrated by `receipts/c1-measured-r100.txt`,
  and a `corpus/README.md` frontier bullet that closes the round-99 A8 residual (verified: the
  round-99 SCORECARD section states "the unset-PATH default is modelled but no frozen case exercises
  it (A8)" and the round-100 bullet replaces it).
- **quality — improved.** The gate now measures its legs and its cap is derived from a 28-leg
  timing receipt instead of guessed (600 s → 3600 s = 2.5× the measured worst leg, panel leg rows
  byte-identical); the round's own first-draft selftest blind spot (`h3b`) was closed with the
  parse fix; the round-99 pointer errata land append-only (QUALITY 172a); the census/read-back/index
  surfaces stay green (`rows=469`, `entries=121`). The unmet `mismatches == 0` runs are reported,
  not hidden.
- **discernment — improved.** Both claims' wording was falsified by attack seats *before* filing and
  narrowed with the forcing artifact named (A1–A5, B1–B5), the mutation seats found two instrument
  defects that were fixed rather than argued, and my outside sample agrees on the admit and on the
  reject. Discounted: the two false selftest tallies (§6.1) survived the lane's own gate — a
  report-accuracy class its criteria do not yet catch.

## 6. Routed defects (lane to fix in round 101)

1. **Counter-selftest tallies are false as printed (round report, two instances).** The report says
   both counters' `--selftest` is `9/9`. No receipt carries `9/9`: `receipts/c1-counter-selftest-r100.txt:10`
   prints `MADO_COUNTER_SELFTEST: checks=24 failed=0` and `receipts/c2-counter-selftest-r100.txt:28`
   prints `MADO_C2_R100_SELFTEST: checks=21 failed=0`. Worse for the evidence chain, both receipts ran
   the **build** copies (sha `2a930048…`, `b22ab669…`), not the committed counters
   (`3cbcd82f…`, `ce37b492…`), so neither committed counter has a selftest receipt at all
   (§Gate standard: a verdict names the revision it was measured against). Fix: re-run both committed
   counters' `--selftest`, land the receipt with the committed hash in its header, and correct the
   report's numbers append-only in the next round's lesson.
2. **Round-shape arithmetic and attack share.** The report and the SCORECARD row say "2 scouts,
   6 executors, 1 scribe, 2 reviewers, 1 critic, 2 mutation-testers, 1 connector" — 15 seats — while
   `w1-results.json` carries 16: 7 executor-agent seats, one of which is `R100MLabratUnset` (the
   labrat role riding an executor seat). Attack share is `6/16 = 37.5 %` under the run-15 definition
   (reviewer, critic, mutation-tester, labrat), not `5/16 = 31 %`; both clear the ≥25 % floor, so
   this is a counting defect, not a floor miss. Count roles from `w1-results.json`.
3. **C2 counting command does not reproduce its receipt.** The report's C2 block names
   `--rev ae537dbe…`; `receipts/c2-measured-r100.txt` and `claims.json.measured_rev` name
   `d73a0648…` (the commit that carries the committed counter). Paste the receipt's argv verbatim.
4. **Carried from the lane's own disclosures:** the round-97 leg binds an AF_UNIX fixture inside its
   scratch and fails closed above 108 bytes (`sun_path`) — bound the fixture path in the leg and let
   the panel refuse an over-long leg path; and the harm watch's clock source is unpinned (mutant `h2`
   survives every lane instrument) — either pin `time.monotonic` observably or keep the limit named.

Promotion note for the operator (promotion is operator-owned; I wrote no `[x]`): all four
`SHONEN.md` boxes look checkable by a non-author from resolvable evidence — the SKILL registry rows
and round-100 prose (`SKILL.md:2983-2986`, `:3025-3032`), the round's end-to-end launch-path task
and its LOG entry, the pinned counting argv in `claims.json`, and the connector sweep — so a
promotion review is available whenever the operator chooses to run it.
