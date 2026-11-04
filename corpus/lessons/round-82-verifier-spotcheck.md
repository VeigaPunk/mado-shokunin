author: hyaku closure (non-author integrator, @m_zfl)

# mado round 82 — non-author verifier spot-check

Round 82, hyaku run 15, attempt 1. Base `6ea2386d49318a5f223097c78b5fe79c31b064f8`; lane HEAD and
content tip `59813b913cd0fce28e86a2a9fbf5d43245b54ccc`; freeze `780c30fcae12d74ce8ab3b871a0888696c2415d9`;
erratum tip `12e6ad57ff97a40323fa3d77ca21352b3f5ec285`. Report `.ufo/reports/round-82/mado.md`
@`16112746`. The lane did not author this file; the judge ran no lane gate and ran no jj command
except the `jj-lane.sh` helper.

## 1. Step-1 conformance

**Report attribution and ordering.** `git log --format='%an %H' -- .ufo/reports/round-82/mado.md` →
`mado-shokunin 16112746991dba5ab1c8221ac464f4fd4e91c8f5` (2026-11-04 10:46:33 -0300). Lane identity,
not the operator identity; the report commit postdates lane HEAD `59813b91` (10:46:19 -0300) — the
report lands last.

**Cited commits.** `git merge-base --is-ancestor <h> refs/heads/master` for
`59813b91`, `780c30fc`, `12e6ad57`, `df6c613d`, `53a32d3b`, `57789ab6`, `89acb06c`, `d645edb5`,
`3ec7fb75`, `b6146ee6`, `6ea2386d` — 11/11 ancestor-OK. No dead or orphaned hash.

**Repo state.** `jj-lane.sh state` → `branch=master local=59813b913cd0fce28e86a2a9fbf5d43245b54ccc
remote=59813b913cd0fce28e86a2a9fbf5d43245b54ccc ahead=0 behind=0 head=detached tracked=0 untracked=0`.
`git -C mado-shokunin status --porcelain` → empty. No uncommitted round work.

**Prompt fidelity.** Rendered `templates/round-prompt.md` with `LANE=mado`, `ROUND=82`,
`FLEET_ROOT=/home/vgpnk/Projects/shokunin`, `AXES=coverage + operability (desktop and compositor
craft)` and diffed lines 1–140 against `.ufo/prompts/mado-round-82.md`: one difference only, the
working-dir placeholder `{{FLEET_ROOT}}/<{{LANE}}-repo>` → `/home/vgpnk/Projects/shokunin/mado-shokunin`
instead of the literal `<mado-repo>`. The mission/axes binding, the 1–3 claim rule with the
lowest-axis and exploratory clauses, the 2b frontier step, the ≥8-seat one-batch L2 floor, the report
contract with the five child-lane items, commit-then-push ordering, push scope and the L0 channel are
all present and verbatim. The §6 addendum's L2 floor (≥8) matches `MISSION.md` §L2 concurrency; no
quoted route map contradicts the current bucket table.

**Report shape.** `## SHONEN` present with one line per box, four `[~]` rows, each with a pointer; no
`[x]`. Not a marker: real committed work (11 hashes), evidence pointers and per-claim counting
commands. Required sections appear in order. Defects are in §6; none bars admission.

## 2. Claim re-checks

Each claim declares a capability acquisition; the judge re-derived the frozen inputs and the
held-control deltas from committed bytes and verified the measured outputs against the committed
receipts. **The lane's counters were not executed** (§Gate standard, Closure consequence).

### C1 — coverage: the client's own band (capability acquisition)

Re-measured from committed bytes:

```sh
jq '.cases|length' .ufo/waves/round-82/controls/c1-cases-r82.json          # 47
jq '.cases|length' .ufo/waves/round-81/controls/c1-cases-r81.json          # 39
sha256sum .ufo/waves/round-82/controls/c1-cases-r82.json
# e404bb3fa93d5f12338129adc8733574084e6fab2ee12fbb471dd45df94a315f
# case-object diff r82 vs r81: new=8 missing=0 carried-diff=0
git show 6ea2386d:tools/mado-barfoot.py | sha256sum   # a129a4355728…d1230 (blob 0e9fa220)
git show 780c30fc:tools/mado-barfoot.py | sha256sum   # 380075284d7d…cab59
git show 12e6ad57:tools/mado-barfoot.py | sha256sum   # 58ef4f6a6887…1a76 (= tip 59813b91)
grep -nE '^(CASES|MUTANTS) =' quality/counters/c1-r82-allocation-band.py   # CASES = 47, MUTANTS = 34
# 34 entries in the MUTATIONS list
```

The eight new cases are `alloc-dyn-height-top`, `alloc-dyn-height-margin`, `alloc-dyn-width-dock`,
`alloc-zero-refused`, `alloc-negative-refused`, `alloc-unknown-namespace`, `alloc-explicit-ignored`,
`alloc-composition-dyn-bar`; the 39 round-81 cases are byte-equal case objects (`carried`).

Evidence-verified (receipts, not executed):

- `receipts/control-c1-r82-at-base.txt` last line: `cases=47 correct=39 mutants=34 killed=28
  base_correct=39/47 carried=39/39 tool_selftest=121/121 verdict=TARGET_MISSED` at base `6ea2386d`,
  `tool_sha256=a129a435…`.
- `receipts/measurement-c1-r82.txt` last line: `cases=47 correct=47 mutants=34 killed=34
  base_correct=39/47 carried=39/39 tool_selftest=133/133 verdict=TARGET_MET` at `12e6ad57`,
  `tool_sha256=58ef4f6a…`.

Spot read of the mechanism (`tools/mado-barfoot.py`): `parse_allocation` (`:436-453`) rejects a
non-object, a non-integer, a bool, a negative band (Setup) and an empty namespace; `band_of`
(`:456-471`) returns the positive declaration, else the allocation for the namespace, else
`Unmodelled` (zero or absent refused); call sites `:481-482` (`declared_box`) and `:805`
(composition `bar_spec`) both route the band axis through it. The declaration arm is reachable now
(both callers pass non-zero-only after the M82-1 repair). The capability row "The client's own band"
is in `SCORECARD.md`.

**Verdict: improved.** Named limit and residual: the counter cannot discriminate the declared
allocation from an observed layers box because no frozen case expects `box=DIFFER` (V7; the critic
scored a live-box candidate 47/47). The claim as declared is the modelled surface and the code
implements the map as the band source, so the capability verifies; causality of the counter is
routed to round 83, not overclaimed.

### C2 — operability: the tray plane in the runbook (capability acquisition)

Re-measured from committed bytes:

```sh
jq '.cases|length' .ufo/waves/round-82/controls/c2-runbook-cases-r82.json  # 29
jq '.cases|length' .ufo/waves/round-81/controls/c2-runbook-cases-r81.json  # 26
sha256sum .ufo/waves/round-82/controls/c2-runbook-cases-r82.json
# 07599b24dadde52fcdfe8cd3c0eaccc6a412b37974700d78c67f405ea69647cd
# case-object diff r82 vs r81: new=3 missing=0 carried-diff=0
grep -nE '^(CASES|SHAPES|MUTANTS) =' quality/counters/c2-r82-runbook.py   # 29 / 24 / 25
sed -n '246,277p' SKILL.md | grep -c '^| '                              # 30 = header + 29 data rows
```

The three new cases/rows are `tray-owner` (`busctl --user list`, watcher line's PID a non-zero
decimal), `tray-interface` (the census carries one `org.kde.StatusNotifierWatcher interface` line)
and `tray-methods` (≥2 `.Name method` lines); they sit at `SKILL.md:274-276` inside the section
`:231-276`.

Evidence-verified: `receipts/measurement-c2-r82.txt` → `cases=29 executed=29 matched=29 shapes=24/24
anchors=29/29 rows=29/29 control_new=0/3 mutants=25 killed=25 verdict=TARGET_MET tree=bound` at
`12e6ad57`; the held r81 instrument at this tree → `MADO_R81_RUNBOOK: ERROR (stage=setup the runbook
section carries 0 command rows, frozen target expects 26)` rc 2
(`receipts/control-c2-held-instrument-r82.txt`). Capability row "The tray plane's runbook rows" is in
`SCORECARD.md`.

**Verdict: improved.** Named limits: the `control_new=0/3` clause is tautological by construction
(V8) and `--no-mutants` is parsed but unguarded in the C1 counter (V9) — both disclosed and routed.

### Round shape and harm watch

Wave: `jq '.items|length' w1-spec.json` → 14; roles `connector 1, critic 1, executor 3,
mutation-tester 1, reviewer 2, scout 2, scribe 3, sentinel 1`; attack seats 4/14 = 28.6 %
(reviewer+critic+mutation-tester+labrat), sentinel named separately. `jq '.results|length'
`w1-results.json` → 14; `jq '[.results[]|select((.output//"")|length==0)]|length'` → 0. The seat
reports carry `STATUS: ok` in seven and `STATUS: defect` in seven — see D2.

Harm watch re-derived where countable, else evidence-verified:

| Metric | Before | After | How |
|---|---|---|---|
| knowledge index rows | 100 | 101 | `git show <rev>:corpus/README.md \| grep -cE '^\| `knowledge/'` |
| instrument ledger population | 148 | 150 | instrument-file set under `tools/`, `quality/*.py`, `quality/counters/*.py` at each rev; the two new counters |
| held checkers/frozen gate | — | — | `git rev-parse <rev>:<path>` identical for `quality/landing-counters.sh`, `check-tool-ledger.py`, `check-axis-scores.py`, `check-index.py`, `tools/mado-verify.sh` |
| gate selftest | 460/460 | 460/460 | `receipts/gate-selftest-r82.txt`, `receipts/harm-watch-r82.txt` (not executed) |
| axis table | — | `mismatched=0` | `receipts/axis-r82.txt` (not executed) |

## 3. Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| coverage | improved | C1 capability admitted; 47/47 frozen cases (8 new, 39 carried byte-equal); held r81 tool 39/47; index 100 → 101 |
| operability | improved | C2 capability admitted; 29/29 cases and rows, 24/24 shapes, 25/25 mutants; held instrument rc 2 at this tree; ledger 148 → 150 |
| depth | unchanged | no held entry rewritten weaker; the new entry states both zero-size clauses separately and its limits (§5.2/§5.3) |
| freshness | unchanged | no older row's `status`/`recheck`/`used-by` moved; S481 is a new id for the byte-identical held S460 pin, disclosed |
| calibration | unchanged | SHONEN stays `[~]`×4, no new non-author promotion verdict; axis table `mismatched=0`; held instruments frozen |
| adjacency | unchanged | connector seat finds no sibling claim on either ground (`w1/R82ConnSiblings.md`); contradicted-name evidence rejected rather than absorbed |

No axis is harmed.

## 4. Discernment spot-check (LEARNING.md: non-author, ≥1 admit and ≥1 reject)

Every source below was re-opened live on 2026-11-04 and hashed; all three reproduce byte-identically
to the committed captures, and every quoted location was re-read.

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S481 Hyprland 0.56.2 `wlr-layer-shell-unstable-v1.xml` | admit, tier A, `mined` | `raw.githubusercontent.com/hyprwm/Hyprland/efb50993…/protocols/wlr-layer-shell-unstable-v1.xml` → sha256 `87e0b9c8…`, 19326 B | **agree** | The `set_size` zero clause reads "If you pass 0 for either value, the compositor will assign it and inform you of the assignment in the configure event." at `:128-129` (22 words), and the `configure` zero sentence at `:347-348`. Admitting this source for the client's-band claim is correct. Anchor precision defect D5 (span overruns) does not change the decision. |
| S482 kstatusnotifieritem v6.2.0 `org.kde.StatusNotifierWatcher.xml` | admit, tier A, `mined` | `raw.githubusercontent.com/KDE/kstatusnotifieritem/v6.2.0/src/org.kde.StatusNotifierWatcher.xml` → sha256 `19df7f18…`, 1151 B | **agree** | Interface at `:3`, `RegisterStatusNotifierItem` `:6`, `RegisterStatusNotifierHost` `:10`, `RegisteredStatusNotifierItems` `:17`; the KDE-prefixed name the runbook rows bind is the file's own. |
| S483 freedesktop wiki watcher page | reject, tier B | `www.freedesktop.org/wiki/Specifications/StatusNotifierItem/StatusNotifierWatcher/` → sha256 `f22928e1…`, 6395 B | **agree** | The page head carries "There will be a single org.freedesktop.StatusNotifierWatcher service instance registered on the session" (14 words); the row's rejection reason and flip are exactly what the source supports. |

Quote-length check: S481 22 words, S482 4 tokens, S483 14 words — all ≤25. No newly written
`SOURCES.md` row was found with an unverified quote.

## 5. Trend verdicts

- **expansion — improved.** The round admits one new `corpus/knowledge/` entry on ground the
  coverage map did not hold (the client's own band), indexed 100 → 101 (command in §2), citing new
  `mined` row S481; three sources opened (S481/S482 mined, S483 rejected with a flip), no older row
  edited.
- **quality — improved.** 47 frozen C1 cases with 34/34 mutants killed and 29 frozen C2 cases with
  25/25 mutants killed; seven attack-seat defects were found in-round (a dead resolver branch, an
  inert allocation entry, two false runbook cells, a missing mutation, a missing bool case, array/
  stage matching gaps) and five were fixed in-round; the entry and lesson were rewritten after
  re-opening the sources; the held instruments and the gate are byte-identical at both ends. The
  routed evidence-hygiene defects below are not domain falsity and are queued, not waved through.
- **discernment — improved.** The outside spot-check agrees with the gate on both admits and the one
  reject with reasons on record; the lesson seat refused a coordinator-proposed mistake for lack of a
  pinned transcript and the round reports the refusal instead of keeping the row; the round's own
  construction runs falsified two assumptions before the freeze (a dead branch; a contradictory bus
  name).

## 6. Routed defects (lane must fix next round; all status-neutral)

- **D1 (medium) — the new knowledge entry's receipt pointer no longer resolves.**
  `corpus/knowledge/bar-footprint-allocation-r82.md:3-5` says `verified-at: 780c30fc… (the measured
  receipt … measurement-c1-r82.txt records rev=780c30fc… tool_sha256=38007528…)`. That receipt was
  overwritten in place at `53a32d3b` and now records `rev=12e6ad57… tool_sha256=58ef4f6a…`
  (`git log -- .ufo/waves/round-82/receipts/measurement-c1-r82.txt` → `b6146ee6`, `53a32d3b`). Fix:
  append an erratum block (or a superseding entry) naming the current receipt line, or point at the
  still-standing `receipts/measurement-c1-r82-at-tip.txt` (`rev=57789ab6`, `tool_sha256=38007528…`).
- **D2 (medium) — the report's seat-status sentence contradicts its own table and the seat files.**
  `.ufo/reports/round-82/mado.md:79` says "Eleven seats report `STATUS: ok`; three report `STATUS:
  defect` — the entry, source and lesson scribes". The committed seat reports carry 7 × `STATUS: ok`
  and 7 × `STATUS: defect` (`grep -rn 'STATUS:' .ufo/waves/round-82/w1/*.md`): the three scribes plus
  `R82ReviewerC1`, `R82ReviewerC2`, `R82CriticClaims` and `R82Sentinel`; the report's own seat table
  also lists seven of each. Fix: correct the sentence in the next report's erratum/notes.
- **D3 (medium) — the census-start receipt is not a faithful capture.** The command over the base in
  a clean extraction (`git archive 6ea2386d | tar -x -C …`; `sources-census.sh validate <dir>`) prints
  55 lines (53 × W04, 1 × W01 S277, 1 × ok, exit 0), while
  `receipts/census-start-r82.txt` carries one W04 and `ok`. The report also calls the tip warning set
  "standing W04 duplicate-URL warnings only"; the live run at the tip prints 56 lines (54 × W04, 1 ×
  W01 S277, 1 × ok, exit 0) including a new W04 for S481. Row count 415 → 418 and exit 0 are correct.
  Fix: commit the unfiltered capture and restate the warning set.
- **D4 (low) — the LOG entry retains the clause conflation the entry seat fixed.**
  `LOG.md:4072` cites `set_size :347-348`; `:347-348` is the `configure` event's zero-size sentence
  (the `set_size` clause is `:128-129`). A corrected fact left standing in a sibling file is still a
  defect (`PROTOCOL.md` Evidence standard, "Corrections sweep every mention").
- **D5 (low) — S481's anchor span is loose in every carrier.** The row (`corpus/SOURCES.md:433`),
  `corpus/README.md:133,186`, the report and the entry say `set_size :122-138` (zero clause
  `:128-131`); the request closes at `:137` and the quoted sentence ends at `:129`. The lesson
  (`## Gate` precision notes) already states the verified spans; the fix is to re-anchor the row's
  text, which may be done as a new `supersedes S481 —` row.
- **D6 (low) — "wave-done receipt" does not exist.** The Landed-changes row
  (`.ufo/reports/round-82/mado.md:126`) and the round-shape paragraph cite a wave-done receipt behind
  `59813b91`, but `git ls-tree -r --name-only 59813b91 -- .ufo/waves/round-82` has no such file and
  the gate's `seats=14 dispatched=14 settled=14 verdict=OK` output is not committed. The underlying
  counts were re-derived by the judge with `jq` (14 items, 14 results, 0 empty outputs), so the fact
  holds; the pointer does not.
- **D7 (low) — the harm-watch revision citation is stale.** The report says "measured at the content
  tip `df6c613d`"; `receipts/harm-watch-r82.txt` header says `53a32d3b`. (Index/ledger/axis/gate
  values re-derived or evidence-verified as stated in §2.)
- **D8 (info) — mixed hash units.** The report's harm-watch sentence compares the base tool's git blob
  short id (`0e9fa220…`) with the tip's sha256 (`58ef4f6a…`); both are correct but in different
  spaces (blob pair `0e9fa220` → `c3573920`; sha256 pair `a129a435…` → `58ef4f6a…`).
- **D9 (low) — prose count.** "with eight cases, six refusals" (report `:103`) does not decompose:
  there are 8 new cases of which 3 are refusals (`alloc-zero-refused` rc 3; `alloc-negative-refused`
  and `alloc-unknown-namespace` rc 2); the 47-case set carries 9 non-zero exits (6 × rc 3, 2 × rc 2,
  1 × rc 1).
- **D10 (info) — the lesson's Gate row quotes a different sentence than the registry row.**
  `corpus/lessons/round-82.md` quotes the `configure` sentence (`:347-348`) for S481 while the
  admitted row's quote is the `set_size` sentence (`:128-129`). Both ground the claim; the gate table
  should quote the row it admits.

**SHONEN note for the operator.** The four `[~]` rows carry resolvable pointers (`SKILL.md:231-276`
+ the new entry; `LOG.md` round 82 + `w1/R82ScoutLive.md`; `w1/R82ExecC1Run.md` /
`w1/R82ExecC2Run.md`; `w1/R82ConnSiblings.md`), and the round now has an outside-lane verifier on
record; boxes 1–4 look checkable by a non-author. Promotion is operator-owned and was not touched.
