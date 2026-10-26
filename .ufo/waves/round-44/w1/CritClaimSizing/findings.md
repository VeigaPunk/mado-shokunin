# CritClaimSizing — round-44 w1 claim-sizing attack

Lane `mado-shokunin`, round 44 (`hyaku` run 9, 2026-10-26), w1. Target: the claim sizing before any data
(prompt `.ufo/prompts/mado-round-44.md` §6 item 9). Frozen artifacts attacked: registration
`.ufo/waves/round-44/registration.md` (freeze `e2289516a9a857f55cda7be635933e89b931c3da`), counters
`quality/counters/c1-r44-geometry-states.py` and `quality/counters/c2-r44-gkeep-size-request.py`, reference
`.ufo/waves/round-44/c1/ctl-ref-tool.py.txt`, receipts `receipts/axis-base.txt`, `receipts/ctl-c1.txt`,
`receipts/ctl-c2.txt`. Controls built and scored under
`.ufo/waves/round-44/w1/CritClaimSizing/controls/`, receipts beside this file in `receipts/`; scratch
`/fast/scratch/hyaku/mado-r44/CritClaimSizing/` was deleted before yield — every fixture revision cited
below is a commit in a clone whose `git rev-parse --show-toplevel` was the scratch dir
(`receipts/fixture-facts.txt`), and the control bytes and scorer logs are copied into this seat dir.

Headline numbers (all my own runs, receipts in `receipts/`):

| control | C1 (PRED-C1-r44) | C2 (PRED-C2-r44) |
|---|---|---|
| README-only commit `e4f6ee5b` (tool bytes unchanged, sha `e3c2e471…`) | `fixtures=14/26 … verdict=TARGET_MISSED` exit 1 (`receipts/c1-readme-only.log`) | `admitted=0/1 … TARGET_MISSED` exit 1 (`receipts/c2-readme-only.log`) |
| 12-added-line patch of the round-43 tool (`controls/patch10.py`) | `fixtures=26/26 clauses=a:1 b:0 b4:0 g:1 r:1 … TARGET_MISSED` exit 1 (`receipts/c1-patch10.log`) | — |
| 30-added-line patch (`controls/patch17.py`) | `fixtures=26/26 clauses=a:1 b:1 b4:1 g:1 r:1 … TARGET_MET` exit 0 (`receipts/c1-patch17.log`) | — |
| reference installed as the tool (one `cp`, rev `7acbf9c0`) | `fixtures=26/26 … TARGET_MET` exit 0 (`receipts/c1-ref-installed.log`) | — |
| 18-line quote-only entry (`controls/entry-minimal.md`) | — | `admitted=1/1 verdict=TARGET_MET` exit 0, rev `4fce5c90` (`receipts/c2-minimal-quotes.log`) |
| staged r12 predecessor re-pointed to lane ids (`controls/entry-r12-repoint.md`, 27 lines) | — | `admitted=1/1 verdict=TARGET_MET` exit 0, rev `de2c7ee7` (`receipts/c2-r12-repoint.log`) |

Verdicts per asked attack: **(1) near-do-nothing reaches C2, not C1** (F1, F2, F6); **(2) C1 is a contract
extension, not a false-report fix** (F5); **(3) C2 is named open ground in `corpus/README.md:301`, but 3 of
its 6 elements are the staged predecessor's and the counter measures none of the 5 new ones** (F3);
**(4) universal clauses: two predicate-text contradictions in C2 and one overstated label in C1** (F4, F8,
plus F9's registration universal); **(5) the lowest-axis argument is unsupported for C2 and vacuous for C1**
(F9); **(6) separability holds** (F10, PASS).

---

## F1 [HIGH] The C2 target is reached by the cheapest control that skips the claimed work

**Exact claim attacked** (registration:20–23, C2): what happens after the box is set —
"sendWindowSize -> realToReportSize -> xdg toplevel setSize -> scheduleConfigure, the pending-size-ack list
and onAck (Window.cpp), the X11 configure branch, what xdg-shell 1.49 says a client may do with a configure
size, what GTK 4.24.1's Wayland toplevel does with it, and what gkeep 133b867 declares".

**Counterexample.** The staged r12 predecessor (`gkeep-client-size-request-r12.md`), with its two package ids
re-pointed to the lane rows (`S311→S164`, `S312→S301`), the three remaining pins cited with one quote each,
and the two census lines added, is `admitted=1/1 verdict=TARGET_MET`. The entry is 27 lines / 205 words and
holds none of the five behaviours the claim names (`receipts/admitted-control-surface-counts.txt`, same counts for
both admitted controls):

```
$ grep -c scheduleConfigure  .ufo/waves/round-44/w1/CritClaimSizing/controls/entry-r12-repoint.md   # 0
$ grep -c onAck              …/entry-r12-repoint.md                                                # 0
$ grep -c X11                …/entry-r12-repoint.md                                                # 0
$ grep -c xdg_surface        …/entry-r12-repoint.md                                                # 0
$ grep -c ack_configure      …/entry-r12-repoint.md                                                # 0
```

The 18-line quote-only entry (`entry-minimal.md`, 129 words) is also admitted; its only content is five real
quotes (each `occurrences=1`, verified with the counter's own `occurrences()`/`quote_in_code()`), the two
census lines, five `source:` lines and one ADMIT/REFUSE pair. Run:

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r44-gkeep-size-request.py \
  --repo <fixture> --rev de2c7ee745cb4b01edb5add41f2fafc3304a6baa --base 6a1a90528fe533cadee506a9fa3e9d13d15cc41f
→ PRED-C2-r44 hyprland-gkeep-size-request-r44.md clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=1
→ PRED-C2-r44: admitted=1/1 verdict=TARGET_MET rev=de2c7ee745cb4b01edb5add41f2fafc3304a6baa   (exit 0)
```

**Why this is a sizing defect, not a residual.** Prompt §6 item 9: "Before freezing, build the cheapest
control that skips the claimed work, score it with the frozen counter, and commit that receipt: if it meets
the target, the counter or target is wrong — fix it before data." No clause of PRED-C2-r44 recomputes any of
the five named behaviours from the pins; clauses b–i+ are structural (4+ `source:` lines, one registry row
per cited id, one Gate quote per id, one quote-bearing line per id, README row, two census lines, ADMIT+REFUSE).
The registration's own rule (registration, "Residuals": "A hole `w1` finds **before any data commit**
re-registers as v2 with a new freeze") applies: the freeze is one commit old and no data commit exists.

**Impacted axes.** Coverage (C2): the after-state `admitted=1/1` cannot be re-derived to the claimed
coverage; a near-duplicate of a pre-existing package note earns the same 1/1 as the intended entry.

**Smallest safe correction.** Re-register C2 with one clause that binds the five surfaces to the pin bytes the
way clause h already binds the census: compute from `Hyprland-Window.cpp` the `if (m_isX11 && m_xwaylandSurface)`
branch and the `else if (m_xdgSurface && m_xdgSurface->m_toplevel)` branch with their two call sites
(`->configure(`, `->setSize(`) and require entry lines stating both; compute the `onAck`/`m_pendingSizeAcks`
mechanism (a second recomputed locator); require a phrase set drawn from `xdg-shell.xml`'s toplevel
`set_size`/`configure` text and from `gdktoplevel-wayland.c`'s `xdg_toplevel_configure` handler, each with its
computed locator. Minimum fallback if the L1 will not re-freeze: shrink the claim sentence to what the counter
does measure (five quotes + two census lines) and record the coverage as the predecessor's, not the
extension's.

## F2 [HIGH] The frozen C2 control set is incomplete on the exact variant the assimilation contract requires

**Exact claim attacked** (receipt `receipts/ctl-c2.txt`): "CTL_C2 VERDICT: PASS (controls scoring TARGET_MET: 0 of 3)".
The three controls are base, the staged r12 copied verbatim with package ids, and a header+census shell.

**Counterexample.** The verbatim copy fails only because its ids (`S311`, `S312`) are not lane rows; the
assimilation contract (§6 item 10) *requires* re-grounding each entry in-round and re-pointing ids to the lane
registry. That single step — no new coverage — flips the control to `admitted=1/1` (F1's receipt). So the
freeze's evidence that "a do-nothing control cannot reach the target" does not cover the cheapest near-do-nothing
control. The registered control's own log shows the margin: `C2-STAGED-COPY … a:1 b:0 c:0 d:0 e:0 f:1 g:0 h:0 i:0`
— every failing clause is structural registry/Gate binding, not content.

**Impacted axes.** Coverage (C2); also calibration of the freeze (a control claim that reads as a guarantee).

**Smallest safe correction.** Add the re-pointed-r12 control (this seat's `controls/entry-r12-repoint.md`,
rev `de2c7ee7`) to the C2 control receipt and count it as MET; the freeze cannot claim 0-of-N until the
F1 clause lands.

## F3 [MEDIUM] C2 is named open ground, but its measured after-state is admission, not the claimed coverage

**Exact claim attacked** (registration:20–22 vs `corpus/README.md:301`): the README names "the client's
acknowledgement path" as still open after round 43, so the surface is legitimately frontier→core. But 3 of
the claim's 6 elements are already held by the staged predecessor, verbatim:

```
$ cd /home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge && grep -n \
    "void CWindow::sendWindowSize\|REPORTSIZE = realToReportSize\|m_pendingSizeAcks.emplace_back\|window.set_default_size" \
    gkeep-client-size-request-r12.md
24:> "void CWindow::sendWindowSize(bool force) {"
26:> "const auto REPORTSIZE = realToReportSize();"
28:> "m_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor());"
43:> "window.set_default_size(420, 500)"
```
(lines 44–45 add "no `set_size_request` call at all".)

The genuinely new r44 half is `onAck`, `scheduleConfigure`, the X11 branch, the xdg-shell client permission
and GTK's handling — the five surfaces F1 shows are unmeasured. A coverage claim must name the surface it
moves and the command that would show it unmoved (prompt §6 item 9); `admitted=1/1` shows neither the
colonisation of the new five nor their absence in a clone of the predecessor.

**Impacted axes.** Coverage; calibration (an admission counter is read as a coverage measure).

**Smallest safe correction.** As F1; additionally the SCORECARD row should record the coverage as
"acknowledgement-path entry admitted (5 pins bound, 2 census lines)" and not as the five-surface claim.

## F4 [MEDIUM] C2's frozen predicate text contradicts its own code on two universal clauses

**Exact sentences.** Docstring of `quality/counters/c2-r44-gkeep-size-request.py`:

- `:49` "ten pinned receipts are cited: the whole chain the claim names, not any four of it" — but the
  r44 `PINS` map (`:167`) has five entries and the code enforces `set(PINS) <= used` (`:604`).
- `:107` "exactly three new cited rows have kind own-work and their receipts are host-gkeep.conf,
  host-clients-r43.json and gkeep-ui-excerpt.py" — receipts that are **not** in the r44 `PINS`, and that the
  rebuilt clause h (`host_census`, `:382`) does not check; the code instead requires `gkeep-ui.py` and
  `Hyprland-Window.cpp` (`:388`).

**Counterexample.** A reader who re-derives clause i+/h from the frozen docstring gets "ten pins" and the
round-43 own-work receipts; the code accepts my five-pin entry (`receipts/c2-minimal-quotes.log`:
`clauses=… h:1 i:1`). The predicate is therefore not "the same sentence in the plan, the same condition in
the counter's code and the same label in the receipt" (prompt §6 item 9).

**Impacted axes.** Calibration (frozen-predicate integrity); coverage (the accepted set is under-specified).

**Smallest safe correction.** In the r44 re-registration, rewrite clause h and i+ in place (five PINS by
name, the rebuilt census sentence) instead of prefixing an override paragraph to inherited text; the docstring
is the contract, so an inherited contradiction is a predicate defect.

## F5 [MEDIUM] C1 is a contract extension, not a false-report fix; and the same change is double-booked

**Exact sentences.**

- registration:13 — "the round-43 tool reports a fullscreen or maximized gkeep window as DIFFER or TILED
  although Hyprland replaced the rule's box (a false report found".
- `tools/mado-geometry.py:57` — "DIFFER is a report, not a fault: a user may have resized the window".
- `corpus/knowledge/hyprland-gkeep-geometry-r43.md:46` — "for a floating, non-fullscreen window the stored
  box is handed to the window itself" (`!Fullscreen::controller()->isFullscreen(...)`); i.e. round-43's own
  admitted entry already says the rule's box is not applied to a fullscreen window, so the dump's different
  box and DIFFER are the expected, contract-correct output.
- registration:82 — "this round's own C1 finding (the tool shipped in round 43 reports a fullscreen window
  as DIFFER)" is booked under *Mistake mining*, while registration:12 books the same change as claim C1.

**Counterexample.** Under PRED-C1-r42, DIFFER means "the printed goal box differs from the rule's size"; that
is true for a fullscreen client and is explicitly licensed as "a report, not a fault". The tool was not
lying; it lacked state context. Calling it false (a) misstates the round-43 instrument, (b) converts a
feature extension into a bug fix, and (c) books one change twice — as a claim and as a mined mistake.

**Impacted axes.** Operability (C1's surface is the verdict vocabulary, not a false report); calibration
(the round-43 self-verdict is retroactively misread); adjacency/mistake mining (the D-list).

**Smallest safe correction.** Strike "false report" from registration:13 and from the entry/lesson wording;
keep "DIFFER is a report, not a fault"; and choose one booking — either C1 is the claim (then drop the
mistake-mining line 82) or it is a frontier-step fix (then it cannot carry an axis claim). Given the new
verdict words and summary fields, the claim reading is the defensible one.

## F6 [MEDIUM] C1's target is reachable by a 30-line local patch (and by copying the committed reference); the last increment is bookkeeping

**Counterexample.** `controls/patch10.py` (12 added lines: mode read, two verdict branches, tally keys,
conditional summary — no new selftest cases) reproduces all 26 fixtures byte-exactly and the round-43 37/37:
`fixtures=26/26 clauses=a:1 b:0 b4:0 g:1 r:1 … TARGET_MISSED` (only `b` fails; `selftest=73/73` < 80).
`controls/patch17.py` (30 added lines: the same plus 7 state assertions and a `**kw` helper) is
`fixtures=26/26 clauses=a:1 b:1 b4:1 g:1 r:1 … TARGET_MET`, `selftest=80/80`, `b4 sites=15 killed=15 need=12`
(`receipts/c1-patch17.log`). And the registered reference, committed at
`.ufo/waves/round-44/c1/ctl-ref-tool.py.txt` (sha256 `8e871a00…`), installed as `tools/mado-geometry.py` in one
`cp` and committed (`7acbf9c0`), scores `fixtures=26/26 … verdict=TARGET_MET` exit 0 without `--tool`
(`receipts/c1-ref-installed.log`); scoring the same bytes directly gives the same result (`receipts/c1-ref-copy.log`).

**Why it matters.** C1's whole contract is written in the counter docstring and a byte-identical implementation
sits in the same freeze; the claim's work is a small local edit, and the difference between the 12-line and
30-line versions is the `>= 80` assertion threshold, not correctness. That is legitimate as an operability fix
but it does not move the published operability number (`receipts/axis-base.txt` operability 12/12 is
`quality/check-index.py --selftest`, which reads neither the tool nor the fixtures).

**Impacted axes.** Operability (the claim's measured surface is a new sub-axis, not the published one);
calibration (before→after is a counter verdict, not a score).

**Smallest safe correction.** Declare a bounded operability sub-axis with a number: e.g. "geometry-tool state
verdict words present/correct: 0/2 → 2/2, fixtures 0/26 → 26/26, selftest 73 → ≥80", with the counting command;
and note in the claim that the reference is an answer key (the round-43 admission already records
"the tool is the round-42 reference installed byte-identically").

## F7 [MEDIUM] C1's declared surface includes SKILL/PROVINCE rows that no clause reads

**Exact sentence** (registration:47): "C1 touches `tools/mado-geometry.py` (and its SKILL/PROVINCE rows);
its counter reads only the tool and the round-42 counter."

**Counterexample.** The frozen counter contains no SKILL/PROVINCE logic at all —
`grep -c "SKILL\|PROVINCE" quality/counters/c1-r44-geometry-states.py` → `0`; its only inputs are the tool
bytes and `quality/counters/c1-r42-geometry.py`. The narrowed TILED licence (closure D3) and the new
FULLSCREEN/MAXIMIZED rows in `SKILL.md`'s verdict table (`SKILL.md:270-277`) are therefore unmeasured: a C1
that lands only the tool bytes passes the frozen target while its declared documentation surface stays stale
(and the round-43 capability row, which lists "AGREE / DIFFER / TILED / BADSIZE", also goes stale).

**Impacted axes.** Operability (documented licence is part of the runnable artifact's contract); freshness.

**Smallest safe correction.** Either add one clause that reads the SKILL verdict table (count
FULLSCREEN/MAXIMIZED rows + the narrowed TILED licence sentence, `quality/check-locators.py` style), or scope
C1's sentence to the tool bytes and carry D3 as a frontier-step fix.

## F8 [LOW] C1 clause b4's "state teeth" label overstates the mechanism

**Exact sentence** (`quality/counters/c1-r44-geometry-states.py:37`): "state teeth: the comparison sites of
every function (selftest, main, usage and functions". `state_sites` (`:265`) selects every single-op
comparison in any function whose body contains a string constant with "fullscreen" — not comparisons about
the mode.

**Counterexample.** My `patch10.py` gains 15 sites, five of them in `report` (sites 10–14: `rules==0`,
`differ>0`, `matched==0`), and `patch17` kills all 15 with the **pre-existing** 73-case selftest
(`b4 sites=15 killed=15`). A tool can pass b4 by mentioning "fullscreen" in a function it already tests,
without any state-specific discrimination. The registration's declared residual only covers the
unnamed-helper case.

**Impacted axes.** Calibration (a clause labelled as state teeth measures general selftest reach).

**Smallest safe correction.** Restrict `state_sites` to the function that computes the mode (or to comparisons
whose identifiers/constants touch the mode), or relabel the clause in the docstring.

## F9 [MEDIUM] The lowest-axis argument is unsupported for C2 and vacuous for C1

**Exact sentence** (registration:16): "**Lowest-axis rule.** Every published axis ties at its maximum at base
(`receipts/axis-base.txt`: navigation 60/60, calibration 68/68, …)".

**Counterexample.** `receipts/axis-base.txt` is a staleness check, not a ranking:

```
MADO_AXIS_ROW: axis=navigation published=60/60 derived=60/60 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=68/68 derived=68/68 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=6a1a905…
```

- It has **no coverage row**, so it cannot support C2's coverage claim at all; "every published axis ties at
  its maximum" is a statement about the three axes `quality/check-axis-scores.py` derives
  (`AXES = ("navigation","calibration","operability")`), not about the lane's six.
- It has **no row for the surface C1 changes**: operability's published fraction is
  `check-index.py --selftest` (12 assertions), which reads neither `tools/mado-geometry.py` nor the
  round-42 counter. C1 moves no published number.
- Both claims' after-states are counter verdicts (`TARGET_MET`), not scores; AXES.md requires "pick the
  axis, land one verifiable improvement, measure it … record before→after in `SCORECARD.md`".
- The nudge is not waived: `SCORECARD.md` declares saturation 9.0 / N = 3, every published fraction is 1.0
  (≥ the line), and a capability entered in round 43 (round-43 capabilities table), inside the window — so
  the lowest-axis obligation stands and must be met by a *numbered* sub-axis, not by a tie reading.

**Impacted axes.** Calibration (lowest-axis compliance is asserted from a receipt that does not measure
ranking or coverage); coverage/operability (the claim's score delta is undeclared).

**Smallest safe correction.** Add the coverage row (and the new geometry-state operability sub-axis) to the
base derivation, or name each claim's new bounded sub-axis with its 0–10 before→after and its counting
command in the registration; state the capability-window status explicitly (round 43 reset it).

## F10 [PASS] Separability holds as registered

**Check.** C1's instrument reads only `tools/mado-geometry.py` at REV plus `quality/counters/c1-r42-geometry.py`
(invoked by `regress`, `:309`); C2's reads the entry, `corpus/SOURCES.md`, `corpus/lessons/round-44.md`,
`corpus/README.md` and the five pinned receipts (no tool). Disjoint file sets, disjoint counters: either can
land alone. Evidence of independence in practice: my C2-only fixture commits (`4fce5c90`, `de2c7ee7`) leave
`tools/mado-geometry.py` byte-identical (`receipts/fixture-facts.txt`: base/readme tool sha `e3c2e471…`), and
my C1-only tool controls score without any registry/lesson bytes (they use the frozen repo's own).

**Caveat (not a coupling).** Because C1's SKILL/PROVINCE edits are unmeasured (F7), a partial C1 (tool only)
passes; the round's closures cannot detect the missing documentation half. Fix F7 rather than changing the
separability statement.

---

## Attack ledger (asked items 1–6)

1. **Cheapest controls.** README-only commit: C1 `14/26 MISSED`, C2 `0/1 MISSED` — no reach. 12-line patch:
   C1 `26/26 fixtures` but `TARGET_MISSED` (clause b). 30-line patch: C1 `TARGET_MET` (a *minimum
   implementation*, not a skip; see F6 for its size). Staged r12 re-pointed: C2 `TARGET_MET` (F1, F2).
   18-line quote-only entry: C2 `TARGET_MET` (F1).
2. **C1's surface.** `tools/mado-geometry.py`'s per-client verdict vocabulary and summary line (two new
   verdict words, two counters). It is an extension of the round-43 capability, not a bug fix of a false
   DIFFER (F5) — so it can count as operability only with a declared new sub-axis (F9) and without the
   mistake-mining double book.
3. **C2's ground.** New for this lane per `corpus/README.md:301` (the client's acknowledgement path is named
   open) but 3 of 6 elements are the staged predecessor's already, and the counter measures none of the new
   five (F1, F3).
4. **Universal clauses.** C1's contract values are enumerated by `FS_POOL` + `fsvals0` (list/dict/bool/float/
   str all present) and the r43 byte-identity by clause r — no defect there. C2 has two text/code
   contradictions (F4) and C1's b4 label overstates (F8); registration:16's universal over "published axes"
   is not enumerated by its receipt (F9).
5. **Lowest-axis argument.** F9.
6. **Separability.** F10 (PASS).
