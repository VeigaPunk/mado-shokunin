# Lessons — mado, round 43

Round intent: registration `.ufo/waves/round-43/registration.md` (freeze `b2e2efd6e268920d31f3c32cf52dc097dd6e1d22`, base
`a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`, the round-42 tip). Host `2026-10-26`, Hyprland 0.56.2
(`efb50993780079460b0cbed1363e2166a2de1d9f`). Round 42 froze two claims with their controls and stopped before its wave ran
(`corpus/lessons/round-42-verifier-spotcheck.md:3` "honest stop", `:28` "honest stop: wave 1 never spawned"), so round 43 re-registers C1
**unchanged** and C2 with **round constants only**; neither predicate had met data before this round. Wave w1 then showed the C2
v1 target reachable without the claimed coverage, so C2 was re-registered **before any data** as `PRED-C2-r43-v2`
(`.ufo/waves/round-43/registration-v2.md`, freeze `496340dd53fabd800be42e8fb19090f35e2c235c`); the claim is judged on v2.

C1 lands `tools/mado-geometry.py` (operability, capability acquisition): a read-only join of the `windowrule = size W H, match:class RX`
lines in Hyprland config files with the sizes one `hyprctl clients -j` dump reports
(`hyprctl clients -j | mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf`), per matched client AGREE / DIFFER / TILED / BADSIZE,
`--selftest`; target `fixtures=37/37 verdict=TARGET_MET` under `PRED-C1-r42`, base `fixtures=0/37 tool=absent` (`receipts/c1-before-base.txt`).
C2 admits `corpus/knowledge/hyprland-gkeep-geometry-r43.md` (coverage, sourced): what determines the size of the host's gkeep window end to
end — the rule text, `RE2::RE2::FullMatch`, the `size`/`float` effects, the floating algorithm, the target and window that store the box, the
animated GOAL behind `hyprctl clients -j` `size`, the client's own `set_default_size(420, 500)`, and today's host census; target
`admitted=1/1 verdict=TARGET_MET` under `PRED-C2-r43-v2`, base `admitted=0/1` (`receipts/c2-v2-before-base.txt`).

Shape: **two v1 waves** — `w1` (build + first falsifiers, 38 seats, `.ufo/waves/round-43/w1-spec.json` `items` length 38 at `5add5b4`) and
`w2` (falsify, after the data commit, 32 seats). `registration.md:5` still reads "37 seats"; the 38th seat (`CritClaimSizing`) was added
when the spec builder showed the attack share at 9/37; the frozen file was not edited and LOG.md Round 43 records the change.

Axes: every published axis ties at its maximum at base (`receipts/axis-base.txt`: navigation 59/59, calibration 63/63, operability 12/12,
`MADO_AXIS checked=3 mismatched=0 rev=a35cfdf…`), so **operability** and **coverage** are both lowest axes and the stagnation nudge is not needed.

**Access date.** Every row opened this round carries `opened 2026-10-26` — S290-S297 are all new rows (the lane registry tops at S289 = 226
rows; `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` prints 226 at this round's base) — and the entry's header
carries exactly one `verified-at: 2026-10-26` (PRED-C2-r43 clauses b and c). No held row's opened/recheck date changes this round; the only
held-row edits this round are the used-by additions on S155 and S158, logged below.

## Gate

GATE S290 receipt=.ufo/waves/round-43/fetch/Hyprland-RegexMatchEngine.cpp sha256=8ca655336cd111df1136be76bbdf91bd6830e7e8891df4bb8c766f1e55a3a282 quote="return re2::RE2::FullMatch(other, *m_regex) != m_negative;"
GATE S155 receipt=.ufo/waves/round-43/fetch/Hyprland-WindowRuleApplicator.cpp sha256=fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b quote="static_.size = expr;"
GATE S291 receipt=.ufo/waves/round-43/fetch/Hyprland-DefaultFloatingAlgorithm.cpp sha256=f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 quote="const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);"
GATE S292 receipt=.ufo/waves/round-43/fetch/Hyprland-Target.cpp sha256=49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06 quote="void ITarget::setPositionGlobal(const STargetBox& box, uint8_t) {"
GATE S293 receipt=.ufo/waves/round-43/fetch/Hyprland-WindowTarget.cpp sha256=8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d quote="if (floating() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) { m_window->setBox(m_box.logicalBox);"
GATE S294 receipt=.ufo/waves/round-43/fetch/Hyprland-GeometricMovableAnimated.cpp sha256=649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d quote="case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();"
GATE S158 receipt=.ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp sha256=798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa quote="sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), w->m_workspace ? w->workspaceID() : WORKSPACE_INVALID, escapeJSONStrings(!w->m_workspace ? "" : w->m_workspace->m_name),"
GATE S295 receipt=.ufo/waves/round-43/fetch/host-gkeep.conf sha256=3726e488c0bf93028f1bba11017cf02d26da6dc3604362815bc4f3738b8e9949 quote="windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$"
GATE S296 receipt=.ufo/waves/round-43/fetch/host-clients-r43.json sha256=21db902e1f1234b9f52411cf7885097a18d67b00b9dd0110f9bbd2b36fb442ad quote=""class": "chromium", "floating": false,"
GATE S297 receipt=.ufo/waves/round-43/fetch/gkeep-ui-excerpt.py sha256=3695b788c6d766b8e87c01916a6594158a26c2cf816f991ccf30b72d9c5d1713 quote="window.set_default_size(420, 500) self.board = Board(window)"

ADMIT merge/mado/knowledge/corpus/knowledge/gkeep-size-to-real-size-r11.md as corpus/knowledge/hyprland-gkeep-geometry-r43.md
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-size-rule-application-r10.md reason=its central inference that the client decides the reported size is overturned by the pinned floating-algorithm and window-target path; flip if a pinned source shows the reported size coming from the client's acknowledgement
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-geometry-unobservable-r8.md reason=superseded by the r9 to r11 chain, its census of three clients and its nothing-else-is-missing residual both refuted by this round's receipts; flip if a lane row registers the host build identity it rests on and a fresh census matches it
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-observation-route-r11.md reason=single-source restatement of r11 on the same host receipt, adding no ground beyond the held S158 GOAL read and this round's census; flip if it carries a route step those two do not

Receipts above: the ten pre-wave pins (`git ls-tree -r <rev> .ufo/waves/round-43/fetch/`, all mode 100644), hashes equal to
`receipts/fetch-sha256.txt`. The seven Hyprland pins are byte-identical to the round-42 pins; `host-gkeep.conf` is byte-identical to round 42's
copy; `host-clients-r43.json` is a new capture (4 clients, none floating) and `gkeep-ui-excerpt.py` is regenerated (M43-5). Each quote was checked
by the L1 with the v2 counter's own functions (`quote_at`, `occurrences`, `quote_in_code`, imported read-only): 3-11 words, exactly one
word-bounded occurrence, outside comments, absent from every other cited receipt. Locators the entry carries (computed): `Hyprland-RegexMatchEngine.cpp:16`,
`Hyprland-WindowRuleApplicator.cpp:426`, `Hyprland-DefaultFloatingAlgorithm.cpp:56`, `Hyprland-Target.cpp:10`, `Hyprland-WindowTarget.cpp:70-71`,
`Hyprland-GeometricMovableAnimated.cpp:19`, `Hyprland-HyprCtl.cpp:428-429`, `host-gkeep.conf:4`, `host-clients-r43.json:50-51`, `gkeep-ui-excerpt.py:33-34`
(ranges where the quote spans two receipt lines; the counter reads the start line, M43-7).
The scribe drafts' first HyprCtl.cpp quote occurred twice in its receipt (lines 427 and 447-448) and ScrEntryB's clients-JSON quote four
times (one per 1720x1414 object, lines 6/21/36/51; `w2/RevLesson.md` F3), which v2's d+ refuses; the quotes above replace them.

**Held rows instead of two new rows (the drafting seat's caveat 1, resolved (b)).** The lane already holds `S155`
(`…/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.cpp`) and `S158` (`…/efb5099…/src/debug/HyprCtl.cpp`),
the exact documents of two pins, and v2 e+ requires the commit-form URL for every `Hyprland-*` receipt, so a new row would duplicate a held
location (clause e, census E04). The entry cites the held rows; their Gate receipts are the pinned bytes (sha256 equal to the PINS values,
`receipts/fetch-sha256.txt`), so the unpinned-held-receipt residual (`w1/RevC2Counter/findings.md` F1) is not used. The new rows are numbered
by document, append-only and gap-free: S290 RegexMatchEngine.cpp, S291 DefaultFloatingAlgorithm.cpp, S292 Target.cpp, S293 WindowTarget.cpp,
S294 GeometricMovableAnimated.cpp, S295 host-gkeep.conf, S296 host-clients-r43.json, S297 gkeep-ui-excerpt.py (the registration's
reservation S290-S299 shrinks to S290-S297; S298 and S299 stay free).

## Assimilation ledger (theme: gkeep geometry; package `merge/mado/`, read-only)

| candidate | scope (PROVINCE) | held | quality bar | verdict |
|---|---|---|---|---|
| `gkeep-size-to-real-size-r11.md` | in (upstream code at the host's tag, host rule file) | the lane holds no rendered-geometry text at base (`git grep -ciE 'set_default_size\|GEOMETRIC_GOAL\|RE2::FullMatch\|rendered geometry' a35cfdf -- corpus/knowledge PROVINCE.md SKILL.md tools` finds none) | four of its five sources are this round's pins (S302-S305 ↔ S291-S294); its `S310` host receipt is re-grounded as S295/S296 | **admitted as the successor** (`ADMIT` above) |
| `gkeep-size-rule-application-r10.md` | in | — | its §1 inference ("the number the compositor reports is whatever the client actually used") is refuted by the pinned path: S291 writes the rule's value into `windowGeometry`, S293 pushes the target box onto the window. The package's own r11 §2 says so | **refused**; flip if a pinned source shows the reported size coming from the client's acknowledgement instead of the rule |
| `gkeep-geometry-unobservable-r8.md` | in | — | superseded twice (r9 amends it, r10-r11 amend the chain); its "nothing else is missing" residual predates the two gates r13/r14 found; its cited receipt path `lanes/mado/round8/…` does not exist in this lane (`git ls-tree -r --name-only HEAD \| grep -c 'round8/fetch'` → 0) | **refused**; flip if a round-43 row re-sources its S275 identity receipt inside this lane |
| `gkeep-observation-route-r11.md` | in | — | one source (`S310`), a restatement of its sibling round; the observation route it names is now sourced directly as held S158 (`w->size(GEOMETRIC_GOAL)`) | **refused** as a duplicate; flip if an independent witness for the observation route is added |
| `gkeep-element-rules-r30.md` | in, narrowly | — | the three rule lines are real and re-grounded as S295, but the entry's explanation of 875×600 rests on the config file's own comment, not on a measurement, and it predates the whole source chain | refused at the data commit; **refusal withdrawn after w2**: the flip had already fired (`apps/system.conf:4`, see Post-data corrections); not adopted this round, first candidate for the next |
| `gkeep-rendered-geometry-chain-r9.md` | in | partly held as prose (no lane row cites it) | its class-is-app_id link rests on `Window.cpp` and the window-rules wiki, neither of which is among this round's pins | not adopted this round: its one unique link (`fetchClass`) is outside the pins; residue for a later round |
| `gkeep-client-size-request-r12.md` | in | — | rests on `Window.cpp::sendWindowSize`, not among this round's pins | not adopted; residue |
| `gkeep-rendered-geometry-record-r13.md`, `-r14.md`, `gkeep-geometry-never-recorded-r15.md` | in | — | their decisive sources are `Window.cpp::onAck`, the map-time DEBUG log and three journal sweeps; none is among this round's pins, and the entry makes no log claim | not adopted; residue (the journal route stays open for a later entry) |
| `glyph-and-geometry-r31.md` | in, but off-theme | — | a two-theme entry (weather glyph + gkeep size); its §2 rests on round-5 rows whose rule text S295 now holds | not adopted; the glyph half belongs to the bar theme |
| the staged ids `S203`-`S349` | — | collide with the lane's own S203-S289 and are the package's numbering | id mapping is by document, never arithmetic | no row of the package is carried over; every cited row is a lane id |

## Registry changes logged old→new (CORPUS.md rule 2)

- New rows S290-S297 (eight; caveat 1 resolved (b)): status `mined`, `opened 2026-10-26`, `used-by` = `corpus/knowledge/hyprland-gkeep-geometry-r43.md`.
  No predecessor row is edited: nothing of the old→new form changes in cells 1-9 of any BASE row.
- Held rows cited (caveat 1(b)): `S155` `used-by` `corpus/knowledge/rule-attribution-r24.md` → `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/hyprland-gkeep-geometry-r43.md`;
  `S158` `used-by` `…, corpus/knowledge/hyprctl-getoption-native-forms-r40.md` → `…, corpus/knowledge/hyprctl-getoption-native-forms-r40.md, corpus/knowledge/hyprland-gkeep-geometry-r43.md` (one item appended; cells 1-10 untouched).
- No row's `status` and no row's `recheck` cell changes this round; S290-S294 carry `on-release`, S295-S297 carry `2027-01-24` (own-work, 90 days);
  the entry's own `recheck: 90d` names the triggers.
- Census after the data commit: `receipts/census-after.txt` (expected: the same W04 ×7 (S030, S042, S045, S097, S119, S120, S121) + W01 S277 set as `receipts/census-before.txt`, exit 0).

## Round-42 closure items (from `corpus/lessons/round-42-verifier-spotcheck.md` §6)

1. **No round-42 lesson, no Mistakes, no sourced claim** (`:57`, `:82` item 1 → M43-4): this file is the repair; the sourced claim is C2.
2. **Wrong prose locators** (`:83-84` → M43-1): the pinned receipts put `w->size(GEOMETRIC_GOAL)` at `Hyprland-HyprCtl.cpp:427-428` and `:448`,
   `starts_with("negative:")` at `Hyprland-RegexMatchEngine.cpp:7-8` and `FullMatch` at `:16`; the correction entry is the first bullet of LOG.md Round 43
   (append-only; this seat did not write LOG.md).
3. **C1 control tally stated three ways** (`:85` → M43-2): the definition now sits in one place, `registration.md:59` ("`controls=` counts the
   do-nothing controls, cheats and mutants and excludes REF and BASE-absent; the verdict denominator adds BASE-absent").
4. **SHONEN box 2 pointer did not resolve** (`:87` item 4 → M43-3): this round commits `receipts/live-geometry-host.txt` — `hyprctl version`,
   `sha256sum tools/mado-geometry.py ~/.config/hypr/gkeep.conf`, the run and `exit=3` with `verdict=NO_MATCHING_CLIENT` — a pointer that resolves
   to bytes. The box itself is the report's (`.ufo/reports/round-43/mado.md` SHONEN box 2 points at this receipt).
5. **L2 floor unmet** (`:88` item 5 → M43-6): mined as a mistake this round rather than left as an orchestrator note.
6. **Attribution note on `8af0263`** (`:89` item 6): history not rewritten; nothing this round touches it.
7. **Still open from round 41** (`:90` item 7): S041 held-row citation, tool ergonomics O1-O5, the `PROVINCE.md:75-76` cite — status at the data
   commit: still open; this round does not touch S041, the round-41 tool or `PROVINCE.md:75-76` (no claim covers them).

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
show the fix can fail is the wave's own `ExecLocatorGate`, whose receipt is `.ufo/waves/round-43/w1/ExecLocatorGate/receipt.txt`, landed as `quality/check-locators.py`. Shown able to fail:
`receipt.txt:60` — `LOC …/LOG-a35cfdf.md:2483 Hyprland-HyprCtl.cpp:394-395,412-413 fragments=6 supported=1 verdict=MISS`, `CHECK_LOCATORS: locators=1 miss=1`,
and `miss=0` on the corrected copy (`:67`); the same MISS on round-42 `registration.md:61` (`:72-73`). It then caught M43-7 below.

**M43-2 — the C1 control tally was stated three ways in one report.** Class: a count published without its definition. Evidence: the closure
quotes the report as "46 controls (absent base, 3 do-nothing, 5 cheats, 37 mutants)" (`round-42-verifier-spotcheck.md:85`), while
`receipts/ctl-c1.txt:1` reads `controls=46` and `:50` reads `0 of 47`; the receipt holds 48 `ok` lines of which 38 are `M*` mutants
(`grep -cE '^ok  M[0-9]' receipts/ctl-c1.txt` → 38), and the runner prints `controls=%d` as `len(jobs) - 2`, excluding REF and BASE-absent
(`.ufo/waves/round-42/ctl/run-c1-controls.py:139`). Three numbers (45, 46, 47) name three different sets. Captured-by: none — the report's own
prose; the closure caught it. Fix: `registration.md:59-61` states the count and its definition once for round 43, and this lesson uses only that
form. Shown able to fail: not shown this round — no checker recounts a report's tally (`grep -cE '^ok  M[0-9]' receipts/ctl-c1.txt` → 38 is the manual check); open.

**M43-3 — a SHONEN box pointed at a LOG.md entry that was never written, and the assertion behind it lived only in the registration.** Class: a
pointer to a run that was never recorded. Evidence: the closure's spot-check row (`round-42-verifier-spotcheck.md:66`) reproduces the live run
and records that "the report says the run is 'recorded in LOG.md Round 42'", but `git grep -n NO_MATCHING a62f2e0 -- LOG.md` finds nothing
(re-run by this seat: no hit) and the only tracked assertion is round-42 `registration.md:24`; at `a62f2e0` the `NO_MATCHING_CLIENT` string
appears in `ctl-ref-tool.py.txt`, `run-c1-controls.py`, `make-w1-spec.py`, `w1-spec.json`, `w1-dispatch.json`, the counter, and `registration.md` — never in a run
receipt. Captured-by: none in round 42; the closure. Fix: this round's wave dir carries `.ufo/waves/round-43/receipts/live-geometry-host.txt` — untracked at this seat's read, landed by the data commit — (11 lines:
`hyprctl version`, the two sha256 sums, the run, `verdict=NO_MATCHING_CLIENT`, `exit=3`), so the box can point at bytes instead of at a claim;
the box itself: the report's SHONEN box 2. Shown able to fail: `grep -c 'verdict=NO_MATCHING_CLIENT' .ufo/waves/round-43/receipts/live-geometry-host.txt` → 1 here, 0 on round 42's
pointer target (`git show a62f2e0:LOG.md | grep -c NO_MATCHING` → 0).

**M43-4 — the round ended with no lesson at all, so the round's own record of its Gate, assimilation and mistakes did not exist.** Class: the
frontier step skipped, not deferred. Evidence: `git ls-tree -r --name-only a62f2e0 -- corpus/lessons/ | grep -c round-42` → 0 (closure `:57`
states the same: "0 of 59 files"), so there was no `## Gate`, no `## Mistakes` and no admit/refuse decision to sample; the closure had to sample
non-gate decisions instead (`:58-59`). Captured-by: none at the round; the closure's step-1 read. Fix: this file, landed before the data commit.
Shown able to fail: PRED-C2-r43 clause d — a lesson with no `## Gate` prints `gates=0 bound=0` for every cited id and `clause=d:0`
(`quality/counters/c2-r43-gkeep-entry.py:396-446`); the fail was demonstrated by w2 seat `RevLesson` on a scratch fixture with the Gate section removed (`gates=0 bound=0`, `d:0`,
`admitted=0/1`, `.ufo/waves/round-43/w2/RevLesson/receipt-nogate-demo.txt`); the pass at the data commit is `receipts/c2-after-data.txt`.

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
w1 has 38 dispatched seats (`.ufo/waves/round-43/w1-spec.json`) and this round's verdict is read from the two counters at the data commit (`receipts/c1-after-data.txt`, `receipts/c2-after-data.txt`).
Shown able to fail: `ls .ufo/waves/round-42/w1/*.md 2>/dev/null | wc -l` → 0 against round 43's `ls .ufo/waves/round-43/w1/*.md | wc -l` → 36 or more; the count separates a
round whose wave ran from one whose wave never spawned. Not yet a gate (open).

**M43-7 — this round's own entry first carried single-line locators for quotes that span two receipt lines.** Class: the M43-1 class,
repeated by the L1 while fixing it (a locator computed for where a quote starts, read as where the fact is). Evidence: the first integration
draft cited `Hyprland-WindowTarget.cpp:70`, `Hyprland-HyprCtl.cpp:428`, `gkeep-ui-excerpt.py:33` and `host-clients-r43.json:50`; the four quotes
continue onto the next line, and `python3 -I quality/check-locators.py --fetch .ufo/waves/round-43/fetch corpus/knowledge/hyprland-gkeep-geometry-r43.md`
printed `verdict=MISS` for exactly those four (`CHECK_LOCATORS: locators=10 miss=4` plus the historical LOG miss). Captured-by: the new
`quality/check-locators.py` (criterion 77); the C2 counter's clause g accepts the start line alone, so it would not have caught it. Fix: the
locators became ranges (`:70-71`, `:428-429`, `:33-34`, `:50-51`), which satisfy both the counter's start-line token and the checker
(`locators=10 miss=0`). Shown able to fail: the MISS lines above, on this round's own draft.

**M43-8 — round 42 froze a coverage predicate that counted citations instead of enumerating the chain its claim named.** Class: a universal
clause ("end to end", eight links) judged by a counter that enumerates only "at least four ids" (prompt §6 item 9: no universal clause unless
the counting command enumerates the full set). Evidence: `w1/CritClaimSizing.md` finding 2 — a 17-line entry citing three own-work receipts
and one upstream file is `admitted=1/1` under `PRED-C2-r43` (`w1/CritClaimSizing/c2-4new-receipt.txt`); `w1/CritC2Cheat.md` X3 (no Hyprland
receipt at all) likewise. Captured-by: §6 item 9 of the round prompt, which the round-42 freeze did not apply to C2's clause b. Fix:
`PRED-C2-r43-v2` (i+: the Gate receipts of the cited ids must cover every PINS name), frozen before data at `496340d`. Shown able to fail:
`ctl/v2-forgeries/more-v2.log` — `X3-own-work-only … admitted=0/1` under v2, `1/1` under v1 (`w1/CritC2Cheat/run-more.log`).

**M43-9 — an INF line said "never" from a walk of the pinned excerpts, and the counterexample sat in a file the round had already pinned.**
Class: a universal inference drawn from a partial source set (the round-38 "absence in a log" class, for source code). Evidence: the data
commit's entry §2 said "A tiled window never takes this branch … the rule's 420x500 is inert"; `Window.cpp:2402-2408` (pinned by w1 seat
`ExecGoalVsValue` at `.ufo/waves/round-43/w1/ExecGoalVsValue/pins/window.cpp`) stores the same size as the tiled target's pseudo size
(`w2/CritEntryInf.md` F1). Captured-by: none mechanically (the C2 counter scores quotes, not inferences; the locator checker scores
locators); the w2 critic. Fix: the entry's INF lines carry a `Basis:` pointer, and "never/only" in an INF is written only after a
whole-tree grep of the variable it is about (`grep -rn 'static_.size'` at the pinned commit), which is the check that would have failed
here (two read sites, not one). Shown able to fail: `w2/CritEntryInf/receipts/grep-static-size-src.txt` lists both sites.

## Post-data corrections (wave w2; data commit `1959770657f1f8665097c1aed4be6c1cbb07139f`)

Every correction below landed in the round's correction commit after the data commit; the C2 v2 counter still reads `admitted=1/1`
on the corrected bytes (`receipts/c2-after-tip.txt`), C1 is untouched (`receipts/c1-after-tip.txt`).

- **Entry, tiled path** (`w2/CritEntryInf.md` F1, `w2/CritEntryOverreach.md`): "a tiled window never takes this branch … the rule's 420x500
  is inert" was false. `mapWindow`'s non-floating arm evaluates the same `static_.size` and stores it as the target's pseudo size
  (`Window.cpp:2402-2408` in `w1/ExecGoalVsValue/pins/window.cpp`), which decides the box when the window is pseudo-tiled. The entry's §2
  INF and the SKILL.md TILED licence row were rewritten. The tool's docstring (`tools/mado-geometry.py:6`, "a tiled window never reads
  it") and its TILED verdict carry the same premise; the tool is left byte-identical and the defect is open for the next C1 registration.
- **Entry, first map** (`w2/CritEntryInf.md` F2): `m_firstMap` is set on every map (`Window.cpp:2079`) and cleared at its end (`:2513`), so
  "evaluated on first map only" became "re-applied on every map; nothing re-evaluates it while mapped".
- **Entry, precision** (`w2/CritEntryOverreach.md`): RE2 dots exclude newline by default; `negative:` is stripped at line 9 and inverted by
  the comparison at line 16; "no read verb" became "no geometry read verb"; the census row says "none floating", not "tiled"; the
  `Gtk.ApplicationWindow` is excerpt line 31. The link `*m_realSize = x.size();` (`Hyprland-GeometricMovableAnimated.cpp:45`) was added
  (`w2/CritAssimilation.md` F2: the ADMIT claimed a four-link chain the entry did not show), and "four-link chain" in the header became
  the named chain.
- **Entry, oracle sentence** (`w2/CritOracleClaim.md`): the run is an adaptation of the round-27 harness (a headless output added), the
  client is a shm stand-in that requests no size, and the 200x200 control ran a separate build of it; the sentence now says so and is
  tagged OBS for the isolated oracle only.
- **Assimilation** (`w2/CritAssimilation.md` F1, F3, F4): the `gkeep-element-rules-r30.md` refusal is withdrawn — its flip condition had
  already fired (`~/.local/share/omarchy/default/hypr/apps/system.conf:4` `windowrule = size 875 600, match:tag floating-window`, captured in
  `w1/ExecLiveHost/live-census.txt:232`); it is not admitted this round (no pin, no row) and is the first candidate for the next one. The r8
  and obs-route flips were rewritten to conditions that can fire. Residue-row notes (F5, F6: the r10 refusal also has an experimental
  falsifier, the oracle's 200x200 stand-in reporting 420x500; "three journal sweeps" is two journal sweeps and one artifact sweep; r14
  borders tsukuroi's journal ground) are recorded here and not re-graded.
- **Registry wording** (`w2/ScoutRowsA.md`, `ScoutRowsB.md`, `ScoutRowsC.md`): S290's teaches cell mixes the host regex in; S291's title
  overstates (the tiled pseudo-size consumer exists); S292's and S294's teaches cells end in a cross-row inference; S293's teaches cell
  simplifies the desired-geometry fallbacks (`WindowTarget.cpp:323-364`). CORPUS.md rule 2 lets only status, recheck and used-by change in
  place, so these cells stay as landed and the next round supersedes the rows with corrected text. Hashes, URLs, anchors, quotes and
  Gate lines of all ten cited rows were re-opened today and hold.
- **PROVINCE.md** (`w2/SentLiveRun.md` F3): `--selftest` opens `/nonexistent/none`, `/` and `/dev/null` read-only to test refusals; the row
  said it opens no file. Corrected.
- **SKILL.md** (`w2/CritC1Capability.md` F3, `w1/RevRefTool.md` V1): the support ceiling (single `match:class` criterion only, `source` not
  followed: 3 of the host's 7 size rules) and the backtracking hang with its `timeout 5` guard are now stated.
- **Locator checker limits** (`w2/CritLocatorGate.md`): numbers are never compared and a shared identifier can pass a wrong range;
  criterion 77 states a stronger rule than the checker enforces. Open; the checker is a floor, not the rule.

- **Dating** (`w2/RevLesson.md` F6): this file landed in the data commit `1959770`, but several things it names landed later — LOG.md
  Round 43 and the w1 evidence at `2a3707c`, the after-tip receipts and `receipts/census-after.txt` with the closing commit, the report on
  the fleet repo after that. Read every pointer at the lane tip, not at `1959770`.
- **Degraded seat**: w2 `ScoutRowsD` returned only a summary in `w2-results.json` (its `rows.md` was never written and its report file
  says `status: started`); its S295-S297 findings (two-line Gate quotes, S296 teaches overreach, S297 kind/scope/anchor wording) are kept
  from that summary and are part of the supersession note above.

## Spot-check (non-author closure; placeholders)

| check | command | expected |
|---|---|---|
| report committed by lane identity, after the lane commit | `git log --format='%an %H' -- .ufo/reports/round-43/mado.md`; commit times vs the lane tip | (closure) |
| lesson landed, unfenced, Gate section complete | `grep -c '^## Gate' corpus/lessons/round-43.md`; `grep -c '^GATE S' corpus/lessons/round-43.md` | 1; 10 |
| every GATE quote re-opened in its receipt | recompute `sha256sum`; locate each quote word-bounded; confirm it is absent from the other receipts | (closure) |
| every new row's location unique, `opened 2026-10-26`, `used-by` names the entry | `grep -nE '^\| S(29[0-7])\b' corpus/SOURCES.md`; `sources-census.sh validate` | (closure) |
| C1 at the data commit and the tip | `python3 -I quality/counters/c1-r42-geometry.py --repo . --rev <rev>` | `fixtures=37/37 … TARGET_MET`, exit 0 |
| C2 at the data commit and the tip | `python3 -I quality/counters/c2-r43-gkeep-entry-v2.py --repo . --rev <rev>` | `admitted=1/1 … TARGET_MET`, exit 0 |
| admission decisions re-read against the package | re-open the four REFUSE files and the one ADMIT file in `merge/mado/knowledge/corpus/knowledge/` | (closure) |
| axis + harm at the tip | `MADO_AXIS …`, `MADO_SELFTEST`, `MADO_OPTIONS_SELFTEST`, the tool selftests | (closure) |

## Census and measurements

- C1 at the data commit: `receipts/c1-after-data.txt`; at the tip: `receipts/c1-after-tip.txt`. Base: `fixtures=0/37
  tool=absent verdict=TARGET_MISSED` (`receipts/c1-before-base.txt`).
- C2 (v2) at the data commit: `receipts/c2-after-data.txt`; at the tip: `receipts/c2-after-tip.txt`. Base: `admitted=0/1`
  (`receipts/c2-before-base.txt`).
- Controls at the freeze (evidence-verified by this seat as bytes, not executed): `CTL_C1: controls=46` and `CTL_C1 VERDICT: PASS (controls
  scoring TARGET_MET: 0 of 47; reference met: 1)` (`receipts/ctl-c1.txt:1`, `:50`); `CTL_C2: controls=74 correct=74/74`
  (`receipts/ctl-c2.txt`: 74 `ok=1` lines, last line `CTL_C2: controls=74 correct=74/74`; v2: `receipts/ctl-c2-v2.txt`, the same tally).
- Registry rows 226 → 234 (S290-S297); knowledge entries 59 → 60; one `corpus/README.md` index row for the entry (clause f).
- Host census as recomputed by the counter from the pinned own-work receipts (the three lines the entry must carry verbatim):
  `host rules size=420x500 float=on center=on class=^(org.omarchy.gkeep)$`, `host clients total=4 floating=0 gkeep=0`,
  `gkeep request default_size=420x500 application_id=org.omarchy.gkeep` (clause h; this seat re-derived all three from
  `host-gkeep.conf:2-4`, `host-clients-r43.json` and `gkeep-ui-excerpt.py:6,33`).
- The live host receipt is reported, not scored: `receipts/live-geometry-host.txt` (4 clients, no gkeep window,
  `verdict=NO_MATCHING_CLIENT`, `exit=3`).
