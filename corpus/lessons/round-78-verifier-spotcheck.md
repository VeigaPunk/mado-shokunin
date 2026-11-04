author: hyaku closure (non-author integrator, @m_zfl)
# mado round 78 — non-author verifier spot-check (hyaku run 15, closure)

Scope: `.ufo/reports/round-78/mado.md` for lane round 78, base
`f597eccbffefd5fd6bbb01f3511c88bbeaed493c`, landing tip
`a6ed9867afc83ab0a66372c8df6c4fea484147f0`. Nothing here is lane-authored: every number was
re-measured, and every source re-opened, by the integrator on 2026-11-04 (UTC).

## 1. Conformance (PROTOCOL §Round-robin steps 1 and 4)

- **Report identity and ordering.** `.ufo/reports/round-78/mado.md` is committed as `32bb928a`
  by `mado-shokunin <mado@shokunin.local>`, one file (208 lines), at 06:58:19-03:00 — after the
  lane tip `a6ed9867` (06:57:00) and before the driver's `complete` line (06:59:32). Pathspec was
  the report only.
- **SHONEN heading.** `## SHONEN` is present with one line per box; all four are `[~]` with
  evidence pointers, matching the four `[~]` in `SHONEN.md` (no `[x]` written).
- **Cited commits.** Every cited lane hash resolves
  (`git cat-file -e <h>^{commit}`) and is an ancestor of `master`
  (`git merge-base --is-ancestor <h> master`): the 24 commits of the landing table plus the
  r77-era `9197405c`. `1bceb514…` and `e54787b7…` are sha256 prefixes of the tool, not commits.
  The lane repo has 23 commits in `f597eccb..a6ed9867`, all authored by `mado-shokunin`.
- **Lane push state.** `jj-lane.sh state` reports branch `master`
  `local=a6ed9867 remote=a6ed9867 ahead=0 behind=0 tracked=0 untracked=0`; `git status
  --porcelain` is empty. No uncommitted lane round work.
- **Prompt contract.** `.ufo/prompts/mado-round-78.md` (committed `64ebb50a`) lines 1–140 are
  `templates/round-prompt.md` byte-for-byte after template substitution; the hyaku §6 addendum
  follows. The five child-lane items (report path, commit-before-report, SHONEN heading,
  commit-hash citation, lane write scope) and the round-level items (MISSION/AXES binding, L2
  floor, commit-then-push, push scope, L0) are present.
- **Defects (status-neutral).** (a) The report's `mado | round-78` L0 line is appended to
  `.ufo/l0-questions.md` but uncommitted at closure (`git status` shows `M`; `git show
  HEAD:.ufo/l0-questions.md` lacks it); durability is owed by the integrator's next pass — this
  pass wrote only its two closure artifacts. (b) The C1 "before" bullet cannot be reproduced by
  the pasted counting command at the base revision: the counter mutates the candidate source, so
  the base rev needs `--no-mutants` (without it the run exits 2, "mutant opposite-margin-dropped
  anchor occurs 0 times"); the receipt's `mutants=0 killed=0` is that path. (c) Self-description
  drift: the tracked tool's `VERSION` is still `r78-v1` while report/SCORECARD/registry call the
  repair `r78-v2`, and `quality/counters/c1-r78-margins.py`'s docstring contract still prints
  `tool_selftest=22/22`; the observed tip is `28/28`. (d) The README round-78 frontier bullet
  names three re-opened rows (`S457/S462/S464`) where the lesson and report name seven. None is
  a marker predicate and none changes the status.

## 2. Claim re-checks (re-measured by the integrator)

### C1 — coverage: margined auto exclusive-zone composition

```sh
python3 -I quality/counters/c1-r78-margins.py --repo . \
  --rev a6ed9867afc83ab0a66372c8df6c4fea484147f0 \
  --base-rev f597eccbffefd5fd6bbb01f3511c88bbeaed493c \
  --controls .ufo/waves/round-78/controls/c1-cases-r78.json --scratch-root <dir>
```
Observed at the tip (rc 0):
`MADO_R78_BARFOOT: cases=18 correct=18 mutants=7 killed=7 base_correct=8/18
tool_selftest=28/28 verdict=TARGET_MET rev=a6ed9867… tool_sha256=1bceb514…`.
Mutant scores reproduced exactly: `opposite-margin-dropped` 9/18, `horizontal-margin-leak` 9/18,
`level-bottom-swap` 17/18, `right-extent-flip` 16/18, `per-side-margin-dropped` 17/18,
`negative-margin-accepted` 17/18, `opposite-edge-wrong` 17/18.
The before state (same base rev, `--no-mutants`) reproduced rc 1:
`cases=18 correct=8 mutants=0 killed=0 base_correct=8/18 tool_selftest=18/18
verdict=TARGET_MISSED`. Tool digests match the report: tip `1bceb514e95f…`, base
`e54787b756…`. The control set carries 18 cases (`jq '.cases|length'`); the generator derives
the expected band from `height/width + the two band-axis margins`, not from a tool run.

### C2 — operability: churn-resistant read-only runbook

```sh
python3 -I quality/counters/c2-r78-runbook.py --repo . \
  --rev a6ed9867afc83ab0a66372c8df6c4fea484147f0 \
  --controls .ufo/waves/round-78/controls/c2-runbook-cases-r78.json --scratch-root <dir>
```
Observed at the tip (rc 0): `MADO_R78_RUNBOOK: cases=17 executed=17 matched=17 shapes=12/12
anchors=17/17 control=5/17 mutants=5 killed=5 verdict=TARGET_MET rev=a6ed9867…`.
The before state (base rev) reproduced rc 2:
`ERROR (stage=setup anchor 'hyprctl activeworkspace' for active-workspace not in a SKILL.md
table row at f597eccbffef; anchor 'hyprctl workspaces -j' for workspaces-count not in a SKILL.md
table row …)`. Independent byte checks: 17 cases, 12 shape kinds, 17/17 row-bound command cells,
13 distinct anchors (the named residual); the two bar captures are `levels_dump` and
`array_fields` rows. Counter selftests: `MADO_R78_BARFOOT_SELFTEST: 24/24` and
`MADO_R78_RUNBOOK_SELFTEST: 40/40`, matching the registry rows.

### Supporting measurements

- `SOURCES.md`: 401 rows both ends (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`); the
  column diff of the committed file shows exactly eight rows changed and only in `used-by`
  (S457–S464 each gain `corpus/knowledge/bar-footprint-margins-r78.md`); status/recheck/tier/kind
  unchanged; tier histogram A=386 B=7 C=8. Frozen census checks: malformed rows 0, duplicate ids
  none, enum violations none, missing used-by paths none.
- Index/coverage: `corpus/knowledge/*.md` 96 at base → 97 at tip; README index rows 96 → 97.
- Instrument ledger: 142 rows (143 `| \`` lines minus the grammar template), matching
  `LEDGER: population=142 ledger_rows=142 uncovered=0`.
- Host join re-run over the committed reduced captures: zero-margin declaration `CLEAN
  band=26 expected=26`; the `margin: 4` fixture `DIFFER band=26 expected=34 rc=1` — reproduced
  exactly; the monitors capture carries no serial/description.
- `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` exits 0
  with the standing W04 duplicate-URL warnings and one `W01 S277 tierC mined`.
- Wave: dispatch `counts.spawn=13` inside the 8–16 band; 13 seat results; attack roles
  reviewer×2 + critic + mutation-tester + sentinel = 5/13 (38%); two seats settled without a
  report and are disclosed, not backfilled.

## 3. Axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | improved | C1: held r77 model 8/18 → 18/18 at the tip; the margined-band ground the r77 entry left `NOT_MODELLED` is modelled with 7/7 mutants killed; index 96/96 → 97/97 |
| operability | improved | C2: base rev cannot bind the runbook (rc 2) → 17/17 executed+matched, 12/12 shape-bound, 17/17 row-bound; held fixed-value rule 5/17; five matcher mutants killed |
| depth | unchanged | no depth claim this round; the new kernel is corpus expansion, not a SKILL depth move |
| freshness | unchanged | seven rows re-opened and re-fetched byte-identically; no freshness score claim; the r77 tool row's time-bound phrase is marked in SCORECARD |
| calibration | unchanged | no new calibration claim; SHONEN stays 4×`[~]`; limits named (second consumer, scaled outputs, centring rounding, second output identifier) |
| adjacency | unchanged | PROVINCE.md unchanged; the connector found one shared read verb with game-dev-2d and no contested ownership |

No axis is harmed: the harm-watch receipts are committed at the measured rev (`460/460`
selftest, index 97/97, ledger 142/142, axis table 3/3, used-by 401 rows 97 entries 0
missing/extra/stale, session-material 291 at both ends with no round-78 path), the SCORECARD diff
is additive only, and the frozen r72–r77 instruments keep their base blob ids.

## 4. Discernment spot-check (LEARNING.md §Discernment is checked from outside)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S457 — Hyprland Renderer.cpp, `applyExclusive` | admit (rule the claim rests on) | live URL pinned at `efb5099…`, `src/render/Renderer.cpp:2577`; sha256 `9af8a74e…` equals the committed fetch | **agree** | the exact line `*edges[i].positive_axis += exclusive + edges[i].margin;` sits inside the `exclusive + edges[i].margin > 0` guard selected by edge/anchor; the quote is ≤25 words and located |
| S464 — gtk-layer-shell 0.10.1, `layer_surface_update_auto_exclusive_zone` | admit (rule the claim rests on) | live URL v0.10.1, `src/layer-surface.c:280`; sha256 `deef9c81…` equals the committed fetch | **agree** | `new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_BOTTOM];` is guarded by `if (!self->anchors[…BOTTOM])` — the unanchored-edge addition the entry states |
| S460 — wlr-layer-shell XML, `set_margin` | admit (supporting quote) | live URL pinned at `efb5099…`, `:196`; sha256 `87e0b9c8…` equals the committed fetch | **agree** | "The exclusive zone includes the margin." is verbatim at line 196 inside `set_margin :193-200`; the r77 D8 locator correction is right |
| S461 — waybar(5) 0.15.0 | admit (supporting quote) | committed render `.ufo/waves/round-78/fetch/S461.txt:91` | **agree** | `Bar position, can be \fBtop\fR, \fBbottom\fR, \fBleft\fR, \fBright\fR.\&` is at the cited line |
| S463 — Wayland Explorer protocol page | reject | live `https://wayland.app/protocols/wlr-layer-shell-unstable-v1`, sha256 `6a3f6683…`, 147036 B (the row's pin and size) | **agree** | no protocol/compositor revision pin; its compositor table lists Hyprland **0.52.1**, not 0.56.2, so it cannot ground a 0.56.2 claim; the title quote is exact |

No new `SOURCES.md` row was written this round (verified by the column diff: 401 → 401, only
`used-by` cells moved), so the "new row's ≤25-word quote" check is inapplicable; the re-opened
admit/reject rows above carry their Gate quotes and were re-opened instead.

## 5. Trend verdicts

- **expansion — improved.** One net-new admitted entry
  (`corpus/knowledge/bar-footprint-margins-r78.md`) on ground the coverage map did not hold (the
  r77 entry left it `NOT_MODELLED`), `source:` citing mined S457/S458/S459/S460/S461/S462/S464;
  index 96/96 → 97/97 at the tip.
- **quality — improved.** The weaker r77 margin limit is superseded by the stronger entry with an
  appended erratum; the stale r77 registry row, index row and present-tense claims are corrected
  (append-only where the record is history); the tool's output/margin/centring/overflow defects
  were repaired with six red-before/green-after fixtures, and no case, mutant or control count
  moved. The residual self-description drift is routed below, not hidden.
- **discernment — improved.** The outside spot-check agrees with the Gate on all three sampled
  decisions (admits S457/S464, reject S463), and every wave disagreement became a committed
  repair or a named limit.

## 6. Routed defects (lane fixes next round)

1. **Instrument self-description (quality).** `tools/mado-barfoot.py:62` still says
   `VERSION = "r78-v1"` while the report/SCORECARD/registry call the repaired bytes `r78-v2`;
   bump the constant (or drop the report-only label), and update
   `quality/counters/c1-r78-margins.py:15`'s contract example from `tool_selftest=22/22` to the
   current green tally (`28/28`). The r77 erratum's "the tracked tool is `r78-v1` … selftest is
   22/22" sentence then needs a one-line append-only correction.
2. **Before-command reproducibility (evidence).** The report's C1 before-command needs
   `--no-mutants` (or the counter must fall back to zero-mutant mode when the base rev lacks the
   anchors); as filed, following the pasted command at `f597eccb` exits 2 instead of printing
   `TARGET_MISSED`. Record the corrected command in round 79's report or a SCORECARD correction.
3. **Frontier-row count.** `corpus/README.md`'s round-78 bullet names three re-opened rows where
   the lesson and report name seven (S457–S462, S464); align on the next append (append-only).
4. **Residual wave coverage.** The two partial seats (`R78ExecC1Tool`, `R78RevC2`) leave the C1
   tool's adversarial fixtures and the C2 byte-fidelity review at seat-report level; the round
   already names successor cases, and they stay round-79 ground.
5. **L0 durability (integrator).** `.ufo/l0-questions.md` carries the mado round-78 serial
   question uncommitted at closure; the integrator's next pass owes the pathspec-limited commit
   (not lane work).
