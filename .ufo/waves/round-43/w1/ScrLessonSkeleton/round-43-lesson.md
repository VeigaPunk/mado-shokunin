# Lessons — mado, round 43

Round intent: registration `.ufo/waves/round-43/registration.md` (freeze `b2e2efd6e268920d31f3c32cf52dc097dd6e1d22`, base
`a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`, the round-42 tip). Host `2026-10-26`, Hyprland 0.56.2
(`efb50993780079460b0cbed1363e2166a2de1d9f`). Round 42 froze two claims with their controls and stopped before its wave ran
(`corpus/lessons/round-42-verifier-spotcheck.md:3` "honest stop", `:28` "honest stop: wave 1 never spawned"), so round 43 re-registers C1
**unchanged** and C2 with **round constants only**; neither predicate had met data before this round.

C1 lands `tools/mado-geometry.py` (operability, capability acquisition): a read-only join of the `windowrule = size W H, match:class RX`
lines in Hyprland config files with the sizes one `hyprctl clients -j` dump reports
(`hyprctl clients -j | mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf`), per matched client AGREE / DIFFER / TILED / BADSIZE,
`--selftest`; target `fixtures=37/37 verdict=TARGET_MET` under `PRED-C1-r42`, base `fixtures=0/37 tool=absent` (`receipts/c1-before-base.txt`).
C2 admits `corpus/knowledge/hyprland-gkeep-geometry-r43.md` (coverage, sourced): what determines the size of the host's gkeep window end to
end — the rule text, `RE2::RE2::FullMatch`, the `size`/`float` effects, the floating algorithm, the target and window that store the box, the
animated GOAL behind `hyprctl clients -j` `size`, the client's own `set_default_size(420, 500)`, and today's host census; target
`admitted=1/1 verdict=TARGET_MET` under `PRED-C2-r43`, base `admitted=0/1` (`receipts/c2-before-base.txt`).

Shape: **two v1 waves** — `w1` (build + first falsifiers, 38 seats, `.ufo/waves/round-43/w1-spec.json` `items` length 38 at `5add5b4`) and
`w2` (falsify, after the data commit, 32 seats). `registration.md:5` still reads "37 seats"; the 38th seat is the wave's own authoring of this
file. Decision at the data commit: <<L1>> (disclose the shape line as written, or re-register — `registration.md:72-73` allows a v2 before any
data commit).

Axes: every published axis ties at its maximum at base (`receipts/axis-base.txt`: navigation 59/59, calibration 63/63, operability 12/12,
`MADO_AXIS checked=3 mismatched=0 rev=a35cfdf…`), so **operability** and **coverage** are both lowest axes and the stagnation nudge is not needed.

**Access date.** Every row opened this round carries `opened 2026-10-26` — S290-S299 are all new rows (the lane registry tops at S289 = 226
rows; `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` prints 226 at this round's base) — and the entry's header
carries exactly one `verified-at: 2026-10-26` (PRED-C2-r43 clauses b and c). No held row's opened/recheck date changes this round; the only
held-row edits this round are used-by additions, logged below.

## Gate

GATE S290 receipt=.ufo/waves/round-43/fetch/Hyprland-RegexMatchEngine.cpp sha256=8ca655336cd111df1136be76bbdf91bd6830e7e8891df4bb8c766f1e55a3a282 quote="return re2::RE2::FullMatch(other, *m_regex) != m_negative;"
GATE S291 receipt=.ufo/waves/round-43/fetch/Hyprland-WindowRuleApplicator.cpp sha256=fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b quote="case WINDOW_RULE_EFFECT_SIZE: { const auto& expr = std::get<Math::SExpressionVec2>(value); if (expr.empty()) static_.size.reset(); else static_.size = expr;"
GATE S292 receipt=.ufo/waves/round-43/fetch/Hyprland-DefaultFloatingAlgorithm.cpp sha256=f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 quote="const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);"
GATE S293 receipt=.ufo/waves/round-43/fetch/Hyprland-Target.cpp sha256=49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06 quote="void ITarget::setPositionGlobal(const STargetBox& box, uint8_t) {"
GATE S294 receipt=.ufo/waves/round-43/fetch/Hyprland-WindowTarget.cpp sha256=8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d quote="if (floating() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) { m_window->setBox(m_box.logicalBox);"
GATE S295 receipt=.ufo/waves/round-43/fetch/Hyprland-GeometricMovableAnimated.cpp sha256=649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d quote="case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();"
GATE S296 receipt=.ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp sha256=798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa quote="sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x), sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), w->m_workspace ? w->workspaceID() : WORKSPACE_INVALID,"
GATE S297 receipt=.ufo/waves/round-43/fetch/host-gkeep.conf sha256=3726e488c0bf93028f1bba11017cf02d26da6dc3604362815bc4f3738b8e9949 quote="windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$"
GATE S298 receipt=.ufo/waves/round-43/fetch/host-clients-r43.json sha256=21db902e1f1234b9f52411cf7885097a18d67b00b9dd0110f9bbd2b36fb442ad quote=""mapped": true, "class": "Alacritty", "floating": false,"
GATE S299 receipt=.ufo/waves/round-43/fetch/gkeep-ui-excerpt.py sha256=3695b788c6d766b8e87c01916a6594158a26c2cf816f991ccf30b72d9c5d1713 quote="window.set_default_size(420, 500) self.board = Board(window)"

ADMIT merge/mado/knowledge/corpus/knowledge/gkeep-size-to-real-size-r11.md as corpus/knowledge/hyprland-gkeep-geometry-r43.md
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-size-rule-application-r10.md reason=its central inference that the client decides the reported size is overturned by the pinned floating-algorithm and window-target path
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-geometry-unobservable-r8.md reason=superseded by the r9 to r11 chain, its residual stale, and its S275 receipt a path this lane does not hold
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-observation-route-r11.md reason=single-source restatement of r11 on the same host receipt, adding no independent ground beside the rule text
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-element-rules-r30.md reason=the 875x600 explanation rests on a config comment and not on any pinned measurement, while the three rule lines are re-grounded as S297

Receipts above: the ten pre-wave pins (`git ls-tree -r HEAD .ufo/waves/round-43/fetch/`, all mode 100644), hashes recomputed by this seat with
`sha256sum` against `receipts/fetch-sha256.txt` — all ten agree. The seven Hyprland pins are byte-identical to the round-42 pins (same sha256 at
`.ufo/waves/round-42/fetch/`); `host-gkeep.conf` is byte-identical to round 42's copy; `host-clients-r43.json` is a new capture (4 clients,
none floating) and `gkeep-ui-excerpt.py` is regenerated (sha256 `3695b788…` against round 42's `48a5c92f…`, see M43-5). Each GATE quote was
checked by this seat against the receipt's whitespace-collapsed text: 4-15 words, word-bounded at both ends, and absent from every other cited
receipt (`quote_at`-equivalent check, receipt in `.ufo/waves/round-43/w1/ScrLessonSkeleton/receipts.txt`). Locators the entry's claim lines
must carry (clause g, computed the same way): `Hyprland-RegexMatchEngine.cpp:16`, `Hyprland-WindowRuleApplicator.cpp:421`,
`Hyprland-DefaultFloatingAlgorithm.cpp:56`, `Hyprland-Target.cpp:10`, `Hyprland-WindowTarget.cpp:70`,
`Hyprland-GeometricMovableAnimated.cpp:19`, `Hyprland-HyprCtl.cpp:427`, `host-gkeep.conf:4`, `host-clients-r43.json:4`,
`gkeep-ui-excerpt.py:33`.

**Two caveats the L1 must settle before the data commit (found by this seat, no data committed yet).**

1. **Clause e collides for S291 and S296 if their rows reuse the held rows' location strings.** PRED-C2-r43 clause e requires a new id's
   location (fragment stripped) to occur in no other registry row. The lane already holds
   `S155` with last cell-1 token `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.cpp`
   and `S158` with `…/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp` — exactly the addresses these two pins were fetched from.
   Two admissible resolutions, both before any data commit: (a) register S291/S296 with the tag address (`…/Hyprland/v0.56.2/<path>`), which is
   how the staged package and S018 already cite the same bytes, so the row set gains no second copy of an existing address; or (b) cite the held
   S155 and S158 instead and open only eight new rows (S290, S292-S295, S297-S299), dropping S291/S296 — clause d requires a distinct receipt
   path per id, so an id may not be added beside the held row that already cites those bytes. Either way the GATE lines above stand; only the
   registry rows move. Chosen: <<L1>>.
2. **S291 and S296 are `code` rows for files whose *rule-side* facts this lane already records at S155/S158** (`S155` "Window-rule matching,
   static and dynamic application", `S158` "`clients` JSON tags"). If the L1 takes resolution (b), the S291/S296 GATE lines above become dead
   lines (clause d ignores GATE lines for uncited ids, but a dead line is still dead prose) and must be deleted, not left standing.

## Assimilation ledger (theme: gkeep geometry; package `merge/mado/`, read-only)

| candidate | scope (PROVINCE) | held | quality bar | verdict |
|---|---|---|---|---|
| `gkeep-size-to-real-size-r11.md` | in (upstream code at the host's tag, host rule file) | the lane holds no rendered-geometry text at base (`git grep -ciE 'set_default_size\|GEOMETRIC_GOAL\|RE2::FullMatch\|rendered geometry' a35cfdf -- corpus/knowledge PROVINCE.md SKILL.md tools` finds none) | four of its five sources are this round's pins (S302-S305 ↔ S292-S295); its `S310` host receipt is re-grounded as S297/S298 | **admitted as the successor** (`ADMIT` above) |
| `gkeep-size-rule-application-r10.md` | in | — | its §1 inference ("the number the compositor reports is whatever the client actually used") is refuted by the pinned path: S292 writes the rule's value into `windowGeometry`, S294 pushes the target box onto the window. The package's own r11 §2 says so | **refused**; flip if a pinned source shows the reported size coming from the client's acknowledgement instead of the rule |
| `gkeep-geometry-unobservable-r8.md` | in | — | superseded twice (r9 amends it, r10-r11 amend the chain); its "nothing else is missing" residual predates the two gates r13/r14 found; its cited receipt path `lanes/mado/round8/…` does not exist in this lane (`git ls-tree -r --name-only HEAD \| grep -c 'round8/fetch'` → 0) | **refused**; flip if a round-43 row re-sources its S275 identity receipt inside this lane |
| `gkeep-observation-route-r11.md` | in | — | one source (`S310`), a restatement of its sibling round; the observation route it names is now sourced directly as S296 (`w->size(GEOMETRIC_GOAL)`) | **refused** as a duplicate; flip if an independent witness for the observation route is added |
| `gkeep-element-rules-r30.md` | in, narrowly | — | the three rule lines are real and re-grounded as S297, but the entry's explanation of 875×600 rests on the config file's own comment, not on a measurement, and it predates the whole source chain | **refused**; flip if the 875×600 stock size is measured or sourced from the desktop's shipped config |
| `gkeep-rendered-geometry-chain-r9.md` | in | partly held as prose (no lane row cites it) | its class-is-app_id link rests on `Window.cpp` and the window-rules wiki, neither of which is among this round's pins | not adopted this round: its one unique link (`fetchClass`) is outside the pins; residue for a later round |
| `gkeep-client-size-request-r12.md` | in | — | rests on `Window.cpp::sendWindowSize`, not among this round's pins | not adopted; residue |
| `gkeep-rendered-geometry-record-r13.md`, `-r14.md`, `gkeep-geometry-never-recorded-r15.md` | in | — | their decisive sources are `Window.cpp::onAck`, the map-time DEBUG log and three journal sweeps; none is among this round's pins, and the entry makes no log claim | not adopted; residue (the journal route stays open for a later entry) |
| `glyph-and-geometry-r31.md` | in, but off-theme | — | a two-theme entry (weather glyph + gkeep size); its §2 rests on round-5 rows whose rule text S297 now holds | not adopted; the glyph half belongs to the bar theme |
| the staged ids `S203`-`S349` | — | collide with the lane's own S203-S289 and are the package's numbering | id mapping is by document, never arithmetic | no row of the package is carried over; every cited row is a lane id |

## Registry changes logged old→new (CORPUS.md rule 2)

- New rows S290-S299 (ten, or eight under Gate caveat 1(b)): status `mined`, `opened 2026-10-26`, `used-by` = `corpus/knowledge/hyprland-gkeep-geometry-r43.md`.
  No predecessor row is edited: nothing of the old→new form changes in cells 1-9 of any BASE row.
- Held rows cited (only under caveat 1(b)): `S155` `used-by` `corpus/knowledge/rule-attribution-r24.md` → `…, corpus/knowledge/hyprland-gkeep-geometry-r43.md`;
  `S158` `used-by` likewise. Under caveat 1(a) neither row is touched. Landed form: <<L1>>.
- No row's `status` and no row's `recheck` cell changes this round; `S290`-`S299` carry recheck cells the drafter chooses, and the entry re-tests
  them at <<L1>>.
- Census after the data commit: <<L1>> (`receipts/census-after.txt`), expected to carry the same W04 ×7 (S030, S042, S045, S097, S119, S120, S121) + W01 S277 set as `receipts/census-before.txt`.

## Round-42 closure items (from `corpus/lessons/round-42-verifier-spotcheck.md` §6)

1. **No round-42 lesson, no Mistakes, no sourced claim** (`:57`, `:82` item 1 → M43-4): this file is the repair; the sourced claim is C2.
2. **Wrong prose locators** (`:83-84` → M43-1): the pinned receipts put `w->size(GEOMETRIC_GOAL)` at `Hyprland-HyprCtl.cpp:427-428` and `:448`,
   `starts_with("negative:")` at `Hyprland-RegexMatchEngine.cpp:7-8` and `FullMatch` at `:16`; the correction entry LOG.md owes is <<L1>>
   (append-only; this seat did not write LOG.md).
3. **C1 control tally stated three ways** (`:85` → M43-2): the definition now sits in one place, `registration.md:59` ("`controls=` counts the
   do-nothing controls, cheats and mutants and excludes REF and BASE-absent; the verdict denominator adds BASE-absent").
4. **SHONEN box 2 pointer did not resolve** (`:87` item 4 → M43-3): this round commits `receipts/live-geometry-host.txt` — `hyprctl version`,
   `sha256sum tools/mado-geometry.py ~/.config/hypr/gkeep.conf`, the run and `exit=3` with `verdict=NO_MATCHING_CLIENT` — a pointer that resolves
   to bytes. The box itself is the report's, not this file's: <<L1>>.
5. **L2 floor unmet** (`:88` item 5 → M43-6): mined as a mistake this round rather than left as an orchestrator note.
6. **Attribution note on `8af0263`** (`:89` item 6): history not rewritten; nothing this round touches it.
7. **Still open from round 41** (`:90` item 7): S041 held-row citation, tool ergonomics O1-O5, the `PROVINCE.md:75-76` cite — status at the data
   commit: <<L1>>.

## Mistakes

**M43-1 — a prose locator named line ranges of a file that does not contain the claim, and no instrument compared the two.** Class: source
location asserted, not computed (the class the round-41 closure routed as `PROVINCE.md:75` → `75-76`). Evidence: `LOG.md:2483` at `a62f2e0`
carries "`hyprctl clients -j` `size` is `w->size(GEOMETRIC_GOAL)` … (`Hyprland-HyprCtl.cpp:394-395,412-413`)" and round 42's
`registration.md:61` repeats it; in the pinned receipt the `GEOMETRIC_GOAL` size calls are at lines 427-428 and 448 and the cited 394-395 and
412-413 carry other fields (`grep -n 'GEOMETRIC_GOAL' .ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp` → 426, 427, 428, 447, 448). The closure
routed the same defect for `Hyprland-RegexMatchEngine.cpp:10-16` → `:7-8` and `:16` (`round-42-verifier-spotcheck.md:84`); this seat could not
re-open the report copy of that string because the report commit `da384db4…` does not resolve in this repo (`git cat-file -t da384db4…` →
"could not get object info") and `.ufo/reports/round-42/` is absent at every ref (see F3). Captured-by: none at the freeze — no instrument
compares a prose locator against receipt line numbers; the non-author closure caught it one round later. Fix: this round quotes only bytes it
opened, and the entry's claim lines carry the counter-computed locator (`<receipt>:<line>`, the list above the ledger); the checker that must
show the fix can fail is the wave's own `ExecLocatorGate`, whose receipt is <<L1>>. Shown able to fail: <<L1>> (that seat's control run over
the round-42 LOG bytes).

**M43-2 — the C1 control tally was stated three ways in one report.** Class: a count published without its definition. Evidence: the closure
quotes the report as "46 controls (absent base, 3 do-nothing, 5 cheats, 37 mutants)" (`round-42-verifier-spotcheck.md:85`), while
`receipts/ctl-c1.txt:1` reads `controls=46` and `:50` reads `0 of 47`; the receipt holds 48 `ok` lines of which 38 are `M*` mutants
(`grep -cE '^ok  M[0-9]' receipts/ctl-c1.txt` → 38), and the runner prints `controls=%d` as `len(jobs) - 2`, excluding REF and BASE-absent
(`.ufo/waves/round-42/ctl/run-c1-controls.py:139`). Three numbers (45, 46, 47) name three different sets. Captured-by: none — the report's own
prose; the closure caught it. Fix: `registration.md:59` states the count and its definition once for round 43, and this lesson uses only that
form. Shown able to fail: <<L1>> (a w2 checker that recounts `M*` lines and compares the report's tally — none exists yet).

**M43-3 — a SHONEN box pointed at a LOG.md entry that was never written, and the assertion behind it lived only in the registration.** Class: a
pointer to a run that was never recorded. Evidence: the closure's spot-check row (`round-42-verifier-spotcheck.md:66`) reproduces the live run
and records that "the report says the run is 'recorded in LOG.md Round 42'", but `git grep -n NO_MATCHING a62f2e0 -- LOG.md` finds nothing
(re-run by this seat: no hit) and the only tracked assertion is round-42 `registration.md:24`; at `a62f2e0` the `NO_MATCHING_CLIENT` string
appears in `ctl-ref-tool.py.txt`, `run-c1-controls.py`, `make-w1-spec.py`, `w1-spec.json`, the counter, and `registration.md` — never in a run
receipt. Captured-by: none in round 42; the closure. Fix: this round's wave dir carries `.ufo/waves/round-43/receipts/live-geometry-host.txt` — untracked at this seat's read, landed by the data commit — (11 lines:
`hyprctl version`, the two sha256 sums, the run, `verdict=NO_MATCHING_CLIENT`, `exit=3`), so the box can point at bytes instead of at a claim;
the box itself: <<L1>>. Shown able to fail: <<L1>> (a pointer check greping the box's path for the verdict line).

**M43-4 — the round ended with no lesson at all, so the round's own record of its Gate, assimilation and mistakes did not exist.** Class: the
frontier step skipped, not deferred. Evidence: `git ls-tree -r --name-only a62f2e0 -- corpus/lessons/ | grep -c round-42` → 0 (closure `:57`
states the same: "0 of 59 files"), so there was no `## Gate`, no `## Mistakes` and no admit/refuse decision to sample; the closure had to sample
non-gate decisions instead (`:58-59`). Captured-by: none at the round; the closure's step-1 read. Fix: this file, landed before the data commit.
Shown able to fail: PRED-C2-r43 clause d — a lesson with no `## Gate` prints `gates=0 bound=0` for every cited id and `clause=d:0`
(`quality/counters/c2-r43-gkeep-entry.py:396-446`); measured at the data commit: <<L1>>.

**M43-5 — a generated excerpt's header named lines 446-495 of a 488-line file and its body carried one extra blank line.** Class: a generated
artifact whose header was asserted rather than computed. Evidence: round-42 `fetch/gkeep-ui-excerpt.py:1` says "lines 446-495", while
`wc -l ~/Projects/gkeep/gkeep/ui.py` → 488; the body is 44 lines against the file's 43 for that range —
`diff <(tail -n +3 .ufo/waves/round-42/fetch/gkeep-ui-excerpt.py) <(sed -n '446,$p' ~/Projects/gkeep/gkeep/ui.py)` prints `44d43` with an
empty line, i.e. one extra blank line at the end. Captured-by: none — nothing compared the header to the file length or the body to the range.
Fix: round 43's excerpt is regenerated with `sed -n '446,$p'` and its header says "446-488 (end of file)" (45 lines, sha256 `3695b788…`
against round 42's `48a5c92f…`). Shown able to fail: the same diff against the round-43 bytes is empty — the check fails on the round-42 input
and passes on the round-43 input, so it discriminates rather than merely passing.

**M43-6 — a driver `complete` line and a clean `git status` were read as the round having succeeded, for a round that spawned no seat.** Class:
completion recorded at the driver layer, read as a statement about the work (this is the mistake `considerthese/2026-10-25.md` proposal 2 asks
to count). Evidence: the fleet digest reads `2026-10-26T01:03:32-03:00 complete mado round=42; hyaku-inline attempt=1`
(`/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1462`), while the lane holds 29 files under `.ufo/waves/round-42/`, **0** seat reports
(`git ls-tree -r --name-only HEAD .ufo/waves/round-42/ | grep -c '/w1/.*\.md$'` → 0) and no `w1-results.json`; the closure says it plainly
("honest stop: wave 1 never spawned", `round-42-verifier-spotcheck.md:28`; "0 seats spawned", `:88`), and its §1 records a clean tree
(`untracked=0`, `round-42-verifier-spotcheck.md:21`). Captured-by: none — a driver line and `git status` are both orthogonal to whether any work happened; the closure's manual read
is what named it. Fix: the round's outcome is read from its seat reports and counter receipts, never from the digest or the tree state; round 43's
w1 has 38 dispatched seats (`.ufo/waves/round-43/w1-spec.json`) and this round's verdict is read from the two counters at the data commit (<<L1>>).
Shown able to fail: <<L1>> (a closure check that counts seat reports per wave and refuses a `complete`-only round).

## Spot-check (non-author closure; placeholders)

| check | command | expected |
|---|---|---|
| report committed by lane identity, after the lane commit | `git log --format='%an %H' -- .ufo/reports/round-43/mado.md`; commit times vs the lane tip | <<L1>> |
| lesson landed, unfenced, Gate section complete | `grep -c '^## Gate' corpus/lessons/round-43.md`; `grep -c '^GATE S' corpus/lessons/round-43.md` | 1; <<L1>> (10, or 8 under Gate caveat 1(b)) |
| every GATE quote re-opened in its receipt | recompute `sha256sum`; locate each quote word-bounded; confirm it is absent from the other receipts | <<L1>> |
| every new row's location unique, `opened 2026-10-26`, `used-by` names the entry | `grep -nE '^\| S(29[0-9])\b' corpus/SOURCES.md`; `sources-census.sh validate` | <<L1>> |
| C1 at the data commit and the tip | `python3 -I quality/counters/c1-r42-geometry.py --repo . --rev <rev>` | `fixtures=37/37 … TARGET_MET`, exit 0: <<L1>> |
| C2 at the data commit and the tip | `python3 -I quality/counters/c2-r43-gkeep-entry.py --repo . --rev <rev>` | `admitted=1/1 … TARGET_MET`, exit 0: <<L1>> |
| admission decisions re-read against the package | re-open the four REFUSE files and the one ADMIT file in `merge/mado/knowledge/corpus/knowledge/` | <<L1>> |
| axis + harm at the tip | `MADO_AXIS …`, `MADO_SELFTEST`, `MADO_OPTIONS_SELFTEST`, the tool selftests | <<L1>> |

## Census and measurements

- C1 at the data commit: <<L1>> (`receipts/c1-after-data.txt`); at the tip: <<L1>> (`receipts/c1-after-tip.txt`). Base: `fixtures=0/37
  tool=absent verdict=TARGET_MISSED` (`receipts/c1-before-base.txt`).
- C2 at the data commit: <<L1>> (`receipts/c2-after-data.txt`); at the tip: <<L1>> (`receipts/c2-after-tip.txt`). Base: `admitted=0/1`
  (`receipts/c2-before-base.txt`).
- Controls at the freeze (evidence-verified by this seat as bytes, not executed): `CTL_C1: controls=46` and `CTL_C1 VERDICT: PASS (controls
  scoring TARGET_MET: 0 of 47; reference met: 1)` (`receipts/ctl-c1.txt:1`, `:50`); `CTL_C2: controls=74 correct=74/74`
  (`receipts/ctl-c2.txt`: <<L1>> line number and the `ok=` tally).
- Registry rows 226 → <<L1>>; knowledge entries 59 → <<L1>>; `corpus/README.md` index rows <<L1>> (`PRED-C2-r43` clause f needs exactly one).
- Host census as recomputed by the counter from the pinned own-work receipts (the three lines the entry must carry verbatim):
  `host rules size=420x500 float=on center=on class=^(org.omarchy.gkeep)$`, `host clients total=4 floating=0 gkeep=0`,
  `gkeep request default_size=420x500 application_id=org.omarchy.gkeep` (clause h; this seat re-derived all three from
  `host-gkeep.conf:2-4`, `host-clients-r43.json` and `gkeep-ui-excerpt.py:6,33`).
- The live host receipt is reported, not scored: `receipts/live-geometry-host.txt` (4 clients, no gkeep window,
  `verdict=NO_MATCHING_CLIENT`, `exit=3`).
