author: hyaku closure (non-author integrator, @m_zfl)
lane: mado · lane-round 77 · date 2026-11-04 (America/Sao_Paulo)
lane base: `aeeef067bd63672dfc681d6dacc3797f53ffd1f9` · lane tip: `d71b93fbadde05319f1645842d24b6e21b354a62`
report: `.ufo/reports/round-77/mado.md` @ `74fe9fd88d70b11e6ab2d9c39097ef152df7bba5` (first filed `10dbd564`, rewritten in place at `74fe9fd8`)
driver digest: `2026-11-04T04:47:56-03:00 launch mado round=77 pgid=620308 driver=hyaku-inline attempt=1`;
`2026-11-04T05:54:46-03:00 complete mado round=77; hyaku-inline attempt=1`

This file is the closure's non-author record. It verifies and spot-checks; it does not author round
work, and nothing here changes a lane-authored file. No lane instrument was executed: both claims
rest on lane-owned registered gates, and PROTOCOL §Gate standard (Closure consequence) binds the
integrator to verify their committed evidence, never to run a sibling's gate.

## 1. Step-1 conformance — PASS with status-neutral defects

- **Attribution and order.** `git -C /home/vgpnk/Projects/shokunin log --format='%an <%ae> %H %ci %s'
  -1 -- .ufo/reports/round-77/mado.md` prints `mado-shokunin <mado@shokunin.local>
  74fe9fd88d70b11e6ab2d9c39097ef152df7bba5 2026-11-04 05:54:22 -0300 round-77: mado report — final
  tool sha in Work performed`. The lane tip `d71b93fb` is dated 05:53:19-03:00, so the report lands
  after every lane commit it cites. `git log --format='%an <%ae> %H %ci %s' -1` over the *first*
  report commit prints `mado-shokunin … 10dbd564 … 2026-11-04 05:54:06 -0300`; the 16-second
  follow-up rewrote two filed lines rather than appending an erratum (defect D10).
- **Report path and SHONEN.** Exact path `.ufo/reports/round-77/mado.md`; `grep -c '^## SHONEN'`
  prints `1`; `grep -c '^- \[~\]'` prints `4` and `grep -c '\[x\]'` prints `0` — one asserted line
  per `SHONEN.md` box with an evidence pointer, no self-promotion. Required sections appear in
  order (Work performed → Landed changes → Before → after measurements → Sources & frontier →
  Trend verdicts → SHONEN); the extra Wave disclosures, Stale-lane, Routed-defect dispositions and
  Tool installs sections do not displace them.
- **Cited lane commits.** The report cites 23 commit hashes in its Landed-changes table (several
  rows bundle two commits; `git rev-list --count aeeef067..d71b93fb` prints `25`) plus two hashes
  used as revision arguments (`5dade9b3`, `3588a527`). All 25 hashes resolve
  (`git cat-file -e <hash>^{commit}`) and are ancestors of the branch ref
  (`git merge-base --is-ancestor <hash> refs/heads/master`, 25/25 yes). The report's "twenty-five
  lane commits between `aeeef067` and this tip" is exact.
- **Push state.** `scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/mado-shokunin`
  prints `state branch=master local=d71b93fb… remote=d71b93fb… ahead=0 behind=0 head=detached
  tracked=0 untracked=0`; `git ls-remote origin refs/heads/master` prints the same hash;
  `git status --porcelain | wc -l` prints `0`. No lane work is unpushed, and the fleet remote
  carries the report (`git log -1 origin/master -- .ufo/reports/round-77/mado.md` →
  `74fe9fd8`).
- **Prompt fidelity.** `.ufo/prompts/mado-round-77.md` is committed in the fleet repo at
  `de9e7b30` by `mado-shokunin`. `diff` of `templates/round-prompt.md` (with `{{ROUND}}`=77,
  `{{LANE}}`=mado, the lane-repo and axes substitutions applied) against prompt lines 1–140 shows
  only those expected substitutions; sections 1–5 therefore render the template verbatim —
  mission/axes binding, 1–3 claims, the frontier step, the L2 floor (≥8 seats in one batched
  wave), the report contract with the five child-lane items (path and filename, commit-then-push,
  `## SHONEN` heading, commit-hash citation, lane write scope), commit/push scope and the L0 side
  channel. §6 carries the hyaku run-15 addendum and §7 the scratch discipline; no L2 route map in
  the prompt names a model alias contradicting `MISSION.md`.
- **Marker check.** The report names real committed work, evidence pointers, a LOG entry per
  landed change and a resolvable lane hash — a report, not a completion marker. Status `ok`.

Status-neutral defects are routed in §6; none changes the lane status.

## 2. Claim re-checks

Both claims rest on lane-owned registered gates (`mado-r77-barfoot-counter`,
`mado-r77-runbook`; `SKILL.md:744-745`), so both are **evidence-verified** against committed
receipts plus independent plain counts over committed bytes. Re-executed lane instruments: none.

### C1 — coverage: the bar-footprint chain becomes a measured join

Counting command as reported: `python3 -I quality/counters/c1-r77-barfoot.py --repo . --rev REV
--controls .ufo/waves/round-77/controls/c1-cases-r77.json --scratch-root DIR`.

- **Instrument bytes and revision.** `sha256` of the committed tool at the tip is
  `e54787b75645a97780984aa1e5bf9187b81b400b42ea5b0e04cb46387769b093`, equal to the receipt's
  `tool_sha256=e54787b7…`; the freeze bytes hash `409e78a4aef2f46f80508820f3a58ae7023c1b614f5836d52bf2e6a05490cb15`,
  equal to the report's "freeze bytes were `409e78a4…`". `git log -1 -- tools/mado-barfoot.py`
  at the tip prints `9197405c` (2026-11-04T05:26:15-03:00) and `git log -1 --
  quality/counters/c1-r77-barfoot.py` prints `de627316` (05:17:53); both are ancestors of the
  measured revision `d362908b` (`git merge-base --is-ancestor`, yes/yes), and no later commit
  touches either path, so the measured bytes are the tip bytes.
- **Frozen set.** `jq '.cases|length' .ufo/waves/round-77/controls/c1-cases-r77.json` → `15`; the
  committed file's sha256 is
  `7d6e2b1a5e046dff768d8705abde9f79ee3f34c9095e81e78059e47ededf74ab`, equal to the receipt's
  `MADO_R77_CONTROL` line and unchanged from the freeze. The fifteen case names in the JSON equal
  the fifteen `MADO_R77_CASE` lines one-for-one, and the five `MUTATIONS` entries in the counter
  (`level-top-swap`, `exclusive-false-ignored`, `no-centred-width`, `reserved-wrong-edge`,
  `per-side-margin-dropped`) equal the receipt's five `MADO_R77_MUTANT` rows.
- **Before leg.** At base `aeeef067` the tool, the counter and the case set are all absent
  (`git cat-file -e aeeef067:<path>` fails for all three), so the join did not exist; the receipt's
  control rule `MADO_R77_BASE: correct=8/15 rule=live-echo(no-config-model,no-reserved-model,no-drift)`
  records the do-nothing control's ceiling.
- **After leg.** `receipts/measurement-final-r77.txt` ends C1 with
  `MADO_R77_BARFOOT: cases=15 correct=15 mutants=5 killed=5 base_correct=8/15 tool_selftest=18/18
  verdict=TARGET_MET rev=d362908b… tool_sha256=e54787b7…`, rc 0; the fifteen case rows print
  `correct=yes` and the five mutant rows `killed=yes`. The receipt header states the run came from
  a non-session shell (no `HYPRLAND_INSTANCE_SIGNATURE`/`OMARCHY_PATH`), so the instrument is not
  depending on the session environment.
- **Live join re-derived independently.** From the committed captures: `fetch/live-monitors-r77.json`
  DP-1 = `width 3440, height 1440, refreshRate 99.99700, scale 1, transform 0, reserved [0,26,0,0]`;
  `fetch/live-layers-r77.json` `."DP-1".levels."2"[] | select(.namespace=="waybar")` = `x 0, y 0,
  w 3440, h 26`; the host config `~/.config/waybar/config.jsonc` declares `layer top`,
  `position top`, `height 26`, no margin and no `exclusive` key (defaults). With a top-anchored,
  zero-margin, exclusive bar of height 26 on an unscaled monitor, the box is `0,0,3440,26` and the
  reserved top is 26 — the receipt's `box=MATCH reserved=EQ band=26 expected=26` is re-derivable
  from committed bytes plus the host declaration, without the lane tool. Capture sha256s
  `46eb2481…`/`e732af34…` equal the report's.
- **Contract shape.** The counter's target line requires `correct==15 and killed==5 and base<15 and
  selftest_ok` and the receipt satisfies every clause; the registry row's verdict map
  (`0 clean / 1 failed / 2 could-not-evaluate`) matches the counter's printed contract.
- Verdict: **improved**, evidence-verified (the live join re-derived; the fifteen-case score and
  the five kills are the gate's committed verdict, not re-executed).

### C2 — operability: the SKILL.md read-only probe table executes end-to-end

Counting command as reported: `python3 -I quality/counters/c2-r77-runbook.py --repo . --rev REV
--controls .ufo/waves/round-77/controls/c2-runbook-cases-r77.json`.

- **Instrument bytes and revision.** The committed case set hashes
  `597b230216ca1645d659381dd314d39399eb03979440c22a259fd4425d4c1741` (12 cases,
  `jq '.cases|length'` → `12`), equal to the report's `597b2302…`. `git log -1 --
  quality/counters/c2-r77-runbook.py` at the tip prints `bce906f3` (05:33:20); the rc-guard repair
  landed there and no later commit touches the file. `bce906f3` is an ancestor of `d362908b`, the
  revision the final receipt measures.
- **Anchor binding.** The twelve `skill_anchor` values (9 unique) all occur verbatim in the
  committed `SKILL.md` at the tip (checked one by one with fixed-string grep; 12/12 present). Each
  anchor names a row of the `### Read-only probes` table (`SKILL.md:204-223`); the two rows that
  print no sample value are the ones the declaration erratum names (`monitors-reserved`,
  `waybar-process`), so the binding claim is scoped, not overreaching.
- **Read-only discipline.** Every frozen `argv` is a read verb: `hyprctl version|configerrors|
  monitors|getoption|binds|layers`, `pgrep -x waybar`, `makoctl mode`, `omarchy theme current`,
  `omarchy version`. No write, no reload, no socket of the lane's own.
- **Before/after.** The receipt's control rule is
  `MADO_R77_BASE: executed=0 matched_by_read=12/12 rule=read-the-table` — a rule that only reads
  the table cannot claim an execution; the candidate ends
  `MADO_R77_RUNBOOK: cases=12 executed=12 matched=12 unexecuted=0 anchors=12/12 verdict=TARGET_MET
  rev=d362908b…`, rc 0. The wave's own red/green (`receipts/repair-r77-c2-env.txt`) shows the
  pre-repair run `matched=3 … verdict=TARGET_MISSED` and the post-repair run `12/12`, so the
  environment discovery is a real fix that can fail.
- Verdict: **improved**, evidence-verified (the twelve executions are the gate's committed verdict,
  not re-executed).

### Harm watch

- `git diff --numstat aeeef067 d71b93fb -- SCORECARD.md SKILL.md PROVINCE.md corpus/QUALITY.md
  corpus/README.md` = `72/0, 4/0, 14/0, 34/0, 2/0`: additions only, no score line lowered.
- Frozen instrument blobs are identical base→tip for `tools/mado-verify.sh` (`7956c78781c8`),
  `quality/landing-counters.sh` (`fd579df872b8`), `quality/check-tool-ledger.py`
  (`2ab958bbfcf7`), `quality/check-axis-scores.py` (`7ae3b8b2b2cf`) and
  `quality/counters/c2-r76-shapes.py` (`16b59e7f7a24`). The one changed counter,
  `quality/counters/c1-r76-outcome-field.py` (`8ba5144b2718` → `80b312a1de17`), changes docstring
  text only — the diff's four mutant names, the `cases=16` contract example and one wording line —
  and `receipts/parity-r76-docstring.txt` shows the identical `cases=16 correct=16 mutants=4
  killed=4` verdict before and after; the receipt's before-hash
  `6c7fd2bd…` equals `git show 94b5afb1:quality/counters/c1-r76-outcome-field.py | sha256sum`.
- Index: `git ls-tree -r --name-only <rev> corpus/knowledge | wc -l` → `95` (base) / `96` (tip);
  receipt `MADO_INDEX: indexed=96/96 missing=0 dangling=0 duplicates=0`.
- Ledger: data rows 136 (base) → 140 (tip) (`grep -cE '^\| '` gives 138/142 including the header
  and separator); the diff adds exactly four rows, the two round-77 counters, the tool and the
  cited-revision probe.
- Committed harm-watch receipt (`receipts/harm-watch-r77.txt`, at `d71b93fb`): gate
  `MADO_SELFTEST: 460/460 assertions passed`; `MADO_AXIS: checked=3 mismatched=0`;
  `MADO_WAVE_DONE: round=77 waves=1 settled=1 verdict=OK`; census rc 0. `quality/` and `tools/`
  bytes do not change between `d362908b` and the tip (only receipts and `LOG.md` are added), so
  the tip counts are the measured counts.
- Census re-run by this closure: `./scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin mado` → rc 0, `mado ok …/corpus/SOURCES.md`, with the documented
  W04 duplicate-URL warnings and one `W01 S277 tierC mined used-by=…` warning.

## 3. Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| coverage | improved | C1: join absent at `aeeef067` (tool/counter/case set all absent) → 15/15 cases and 5/5 mutants at the instrument's last changes (`de627316`, `9197405c`, measured at `d362908b`); live join re-derived from committed captures (level 2, box 0,0,3440,26, reserved [0,26,0,0]); index 95 → 96 |
| operability | improved | C2: read-the-table control `executed=0` → 12/12 executed and matched, `anchors=12/12`, measured at the counter's last change `bce906f3`; ledger 136 → 140 rows, uncovered 0; gate 460/460 unchanged |
| calibration | unchanged | axis table re-derived 3/3; no calibration score moved. Two self-record inaccuracies are routed, not scored: the stale final tool revision in `SCORECARD.md` (D3) and the LOG mistake count (D4); neither lowers a measured axis |
| freshness | unchanged | no host-register re-derivation claimed; r76 stale-revision defect was corrected and the r77 instruments carry `verified-at`/`recheck`; the host register (dormant 9.6552) stays operator-owned |
| depth | unchanged | the new entry's anchors re-check (bar.cpp `419-426`, Renderer `2575-2583`/`2577`/`2609-2620`, gtk-layer-shell `264-292`), but no depth rubric moved |
| adjacency | unchanged | the connector's 20-repo scan reports 0 `hyprctl layers` hits and no sibling claim; `PROVINCE.md` gains an append-only refinement naming no new write surface |

No owned axis is harmed by a measured move. The routed defects are conformance items, not score
changes.

## 4. Discernment spot-check (LEARNING.md · `corpus/lessons/round-77.md` `## Gate`)

All quotes were re-opened at the pinned upstream bytes (fetched live 2026-11-04); the Gate table's
≤25-word quotes are the cells checked, because the registry's 11-column shape carries no quote
column (CORPUS.md contract v1: the quote lives in the round lesson's Gate).

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S457 — Hyprland v0.56.2 `src/render/Renderer.cpp` @ `efb5099` | admit, tier A, `mined` | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/render/Renderer.cpp` | agree | Quote `box.width = bounds.width - (PSTATE->margin.left + PSTATE->margin.right);` is literal at line 2637 inside the cited `arrangeLayerArray :2587-2670`; `applyExclusive` at 2529 and `arrangeLayersForMonitor` at 2673 also resolve. The row grounds the box/margin rule and does not claim a margined auto zone. |
| S458 — Hyprland v0.56.2 `src/debug/HyprCtl.cpp` @ `efb5099` | admit, tier A, `mined` | same tree, `src/debug/HyprCtl.cpp` | agree | Quote `sc<int>(m->m_reservedArea.left()), sc<int>(m->m_reservedArea.top())` is literal at line 281 (cited print `:281-282`); `layersRequest` at 647 and the `layers` registration at 2010 resolve. It licenses the reply shape and the reserved order only, as the row says. |
| S461 — installed `waybar(5)` 0.15.0 | admit, tier A, `mined` | `/usr/share/man/man5/waybar.5.gz` (installed; sha256 `3972caaf…` = the row's pin) and `fetch/S461.txt` | agree | `waybar --version` prints `Waybar v0.15.0`; `zcat` of the installed page is byte-identical to the committed `S461.txt`; the quote `Bar position, can be \fBtop\fR, \fBbottom\fR, \fBleft\fR, \fBright\fR.\&` is line 91 of the render, exactly where the row points; 7 words. |
| S464 — gtk-layer-shell v0.10.1 `src/layer-surface.c` @ `v0.10.1` | admit, tier A, `mined` | `https://raw.githubusercontent.com/wmww/gtk-layer-shell/v0.10.1/src/layer-surface.c` | agree | Quote `new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_BOTTOM];` is literal at line 280 inside the cited `:264-292`; reading the whole function confirms the horizontal branch adds the non-anchored (opposite) edge margin, which is the ground for refusing margined auto zones (`NOT_MODELLED`). |
| S460 — `wlr-layer-shell-unstable-v1.xml` @ `efb5099` | admit, tier A, `mined` | Hyprland tree, `protocols/wlr-layer-shell-unstable-v1.xml` | agree on substance, disagree on locator | The quote `The exclusive zone includes the margin.` is literal, but at line 196 inside `set_margin` (`:193-200`), not inside the cited `set_exclusive_zone :152-190` (that request ends at 191). The level enum `:86-90` resolves. Substance stands; the locator is routed as D8. |
| S463 — wayland.app `wlr-layer-shell-unstable-v1` | reject, tier C | `https://wayland.app/protocols/wlr-layer-shell-unstable-v1` (147,036 B; sha256 `6a3f6683…`, equal to `fetch/S463.bin`) | agree | The page renders the protocol text and links `wlr-protocols` at the moving `master` branch; no commit, tag or protocol revision is pinned anywhere in the 147 KB page, so it cannot ground a versioned 0.56.2 claim. The title quote `wlr layer shell protocol` is literal. The flip condition (a commit/tag pin) is sound and the pinned XML (S460) is the authoritative copy. |

No sampled admit or reject disagrees with the gate. The `S460` locator drift is a provenance defect,
not a wrong gate decision, and it is routed rather than left standing.

## 5. Trend verdicts

- **expansion: improved.** One new `corpus/knowledge/` entry on ground the coverage map did not
  hold (`bar-footprint-r77.md`; knowledge files 95 → 96, index receipt `indexed=96/96`), seven
  tier-A mined rows opened and cited by the entry (`S457`–`S462`, `S464`), one tier-C rejection
  kept with its flip (`S463`), and a Frontier bullet at `corpus/README.md`. Qualification: one
  host, one bar, no rendered-output claim — the entry says so; and the report's own count "six
  mined source rows" undercounts the seven (D11).
- **quality: improved.** Both claims meet their frozen targets at their instruments' last changes
  (`de627316`/`9197405c`; `bce906f3`), the base controls miss (`8/15`; `executed=0`), the hermetic
  gate stays 460/460 at unchanged bytes, QUALITY 132–135 land from the round's mistakes and the
  wave findings, and the two wave-found hardening repairs each carry a committed red/green. The
  r76 routed defects D1–D8 are dispositioned append-only (`3e35d0a9`, `8722d564`, `adf8875b`,
  `cb8d559d`). Qualification routed: the SCORECARD's own final-revision label is stale (D3), the
  LOG undercounts the mistake table (D4), and two "shown able to fail" pointers are not durable
  (D6, D7).
- **discernment: improved.** The outside spot-check agrees with four sampled admits and the reject;
  the wave's scout/revenger found real model gaps that are now refusals with red/green pairs; the
  mutant's rc-blindness in the C2 matcher became QUALITY 135; and the cited-revision probe lands
  the first in-class check that can fail with a red/green pair on the r76 row itself (`red` on
  `5dade9b3`, `green` on `3588a527`, selftest 6/6). Qualification: the round repeats the
  stale-revision and mistake-count classes inside its own records (D3, D4, D11) and leaves the
  check un-wired for routine invocation (deferred to r78) — the improvements are real, the class
  is not yet closed.

## 6. Routed defects (lane fixes next round)

- **D1 (report count).** `.ufo/reports/round-77/mado.md` Sources & frontier says "`SOURCES.md` 393 →
  400 rows"; measured `git show <rev>:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} '` → `393`
  (base) / `401` (tip), and the same report's Work performed and the used-by receipt
  (`rows=401`) both say 401. Fix: append the corrected count.
- **D2 (report "rows touched").** The same section says "Rows touched old→new: none (no status,
  recheck or used-by edit to an existing row)". The base→tip `corpus/SOURCES.md` diff has six
  modified rows (`S435`, `S441`, `S442`, `S444`, `S448`, `S455`; six deletions and six insertions)
  from the `a0a8b2a0` used-by repair, and the lesson's `## Registry used-by updates` logs each
  old→new. Fix: name the six rows and the twelve pairs in the next report/erratum.
- **D3 (SCORECARD stale revision; repeat of the class r76 D2 fixed).** `SCORECARD.md`'s round-77
  `### Corrections (round 77)` says "Final instrument revisions: C1 counter `de627316`, tool
  `2df46e29`, tool sha256 `446d197f…`". Measured: `git log -1 -- tools/mado-barfoot.py` →
  `9197405c` and `git show <rev>:tools/mado-barfoot.py | sha256sum` → `e54787b7…`; `446d197f…` is
  the tool at `2df46e29` only. The report and the final receipt carry the correct values. Fix:
  append-only correction naming old → new; do not re-describe a superseded revision as final.
- **D4 (LOG mistake count; repeat of the r76 D4 class).** `LOG.md` round-77 says "Five mined in
  `corpus/lessons/round-77.md`: M77-1 … M77-5"; the lesson holds six rows
  (`grep -c '^| M77-' corpus/lessons/round-77.md` → `6`; M77-6 is the wave-found C2 environment
  mistake). The report says six. Fix: appended correction derived from the lesson rows.
- **D5 (wave disclosure).** The report's per-seat table has 11 rows; the wave had 12 seats and the
  report's own summary counts "9 report-bearing seats, 3 partial/dead". The missing row is
  `R77RevClaims` (reviewer; its deliverable is `.ufo/waves/round-77/w1/R77RevClaims.md`, and the
  lesson cites it). Fix: add the row in the next report or an erratum.
- **D6 (M77-2 red evidence).** Lesson M77-2 cites "`receipts/control-baseline-r77.txt` first
  section (ERROR stage=setup)" as the red half of its red/green. The committed receipt is 54
  lines and contains no `ERROR`/`stage=setup`/`not a git repository` line (`grep -n` prints
  nothing). The green half is real. Fix: commit the red output, or restate the pointer to a
  committed artifact.
- **D7 (QUALITY 132 / M77-1 red evidence in scratch).** Both cite
  `/fast/scratch/hyaku/mado-r77/census2.txt` (E01 `fields=12`) as the failure evidence. Scratch is
  uncommitted and reaper-eligible (PROTOCOL §Evidence standard: a pointer a fresh session cannot
  reach is not evidence; QUALITY-class, see the scratch rule). Fix: commit the E01 census output
  under `.ufo/waves/round-77/` in the next round.
- **D8 (S460 locator).** The lesson Gate cell and the SOURCES `S460` anchor say
  `set_exclusive_zone :152-190`; the quoted sentence is at line 196 in `<request name="set_margin">`
  (`:193-200`; `set_exclusive_zone` ends at 191). Fix: append the corrected locator; the quote
  itself is verbatim.
- **D9 (scratch not removed).** `/fast/scratch/hyaku/mado-r77/` still exists after landing (the
  `l1-src/Hyprland` and `l1-src/Waybar` clones, `wayland-app-layer-shell.html`, seat dirs and
  `c1`/`c2rc`; directory mtime 2026-11-04 05:53), while the report's Tool installs section says the
  two source trees "were removed with the lane's scratch after landing". §7.2 binds the L1 to
  remove the round scratch root. Fix: remove it and record the cleanup; keep the §7.5 reaper as
  backstop only.
- **D10 (report rewritten after filing).** The report was committed at `10dbd564` (committer
  05:54:06) and its filed bytes were rewritten at `74fe9fd8` (05:54:22) — two lines replaced, not
  appended. PROTOCOL §Round-robin: a correction to a filed report lands in the correcting round's
  report or as an appended erratum naming the superseded text, never as a rewrite. The corrected
  value is right; the mechanism is the defect. Fix: append-only from here.
- **D11 (expansion count).** Trend verdicts say "six mined source rows"; the Gate holds seven
  (`S457`–`S462`, `S464`). Fix: one count, derived from the Gate rows.
- **D12 (census description).** The report describes the census result as "W04 duplicate-URL
  warnings only"; the actual output also carries `W01 S277 tierC mined used-by=…`. Fix: name both
  classes (the lesson's M77-1 already says "W04/W01").
- **D13 (gate selftest evidence at last change).** The registry rows cite `--selftest` tallies
  (`15/15` for the C1 counter, `9/9` for the C2 counter), but the committed tallies are from the
  freeze receipt (`a83e9bee`); the counters changed afterwards (`de627316`, `bce906f3`) and no
  post-change selftest tally is committed (the final receipt prints the tool's `18/18`). The
  frozen-run verdicts at the last changes are committed, so this is an evidence gap, not a red
  gate. Fix: re-run both selftests at the tip and commit the tally with the next round's
  harm-watch receipt.

## 7. Operator note (promotion stays operator-owned)

No `[x]` is written here. All four `SHONEN.md` boxes look checkable from repo bytes by a fresh
non-author — the `SKILL.md` decision tables and registry rows resolve, the round ran two end-to-end
tasks with receipts, the counters and case sets are in-repo with `--selftest` modes, and
`PROVINCE.md` names no new write surface — but promotion is operator-owned and this closure is not
an outside-lane verifier for it.
