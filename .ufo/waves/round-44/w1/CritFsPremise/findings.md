# CritFsPremise — does C1 falsify itself? (round 44, w1, lane mado-shokunin)

Assignment: falsify C1's premise — is a DIFFER for a fullscreen/maximized client really false, and is
FULLSCREEN/MAXIMIZED the right report? Everything below is read-only: no lane file was edited, no counter or
control was run against the lane, no compositor mutation, no Wayland client.

## 0. Verdict in one paragraph

The premise's **factual core holds**: on this host's path (dwindle, default FS handler) an internal FS mode of 1
or 2 *does* replace the window's box (monitor logical box / work area), so `size` in the dump is not the rule's
box, and a rule-shaped box cannot be observed while internal FS is set. The **characterisation "false report" is
wrong**: the round-43 tool never claimed the rule failed — `tools/mado-geometry.py:57` says "DIFFER is a report,
not a fault", and SKILL.md's TILED and DIFFER rows already licence a compositor-set box as a cause. A DIFFER on
S1/S2 below is a **true** statement about the box whose *cause* was unstated; the defect is missing diagnosis,
not a falsehood. The **report word is right, the top verdict is over-read**: FULLSCREEN/MAXIMIZED is a true state
label, but the C1 contract makes it replace the verdict and then prints `verdict=OK` with `agree=0 differ=0`,
i.e. the machine-facing exit 0 now fires for a dump in which **no window was compared**. That is not new
(TILED already produced `OK`/rc 0 with nothing compared), but C1 makes it the normal outcome for the one class
the tool exists for, and the frozen registration pre-empts the concern with a sentence that is literally true and
materially misleading (`registration.md:13` calls the old report false; the counter's model at
`c1-r44-geometry-states.py:24` says the top verdict rules are unchanged). **Smallest safe correction**: keep the
state word, but do not let it erase the comparison — either keep the geometry counts for state clients and add a
`state=` field, or make `OK`/exit 0 require `agree>0` and give "matched but nothing compared" its own word for
TILED and state clients alike. Also update the SKILL exit map, which C1's scope names but whose licence C1's
text implies needs no change.

## 1. What the pins establish (the mechanism, with line numbers)

All quotes are verified line-by-line by `verify-quotes.py` (40/40 pass, `receipt-quotes.txt`); pins are byte
copies in `pins/` with `pins/SHA256SUMS` (handler twin: sha256 `5bfed3aa…` = `.ufo/waves/round-44/fetch-c1/Hyprland-FullscreenHandler.cpp`).

- `fullscreen` in the dump is the **internal** mode, `fullscreenClient` the client mode, printed side by side
  (`pins/HyprCtl.cpp:410-411`, values at `:431-432`); the enum is 0 none / 1 maximized / 2 fullscreen
  (`pins/FullscreenController.hpp:13-15`), and the two are stored separately (`:34-35`).
- The **box replacement is keyed on internal only**: `if (TARGET_INTERNAL_MODE == FSMODE_NONE) return;` then
  `MONITOR->logicalBox()` → `setPositionGlobal(MONBOX)` for 2, and `WORKSPACE->m_space->workArea(...)` →
  `setPositionGlobal(WORKAREA)` for 1 (`pins/Hypr-FullscreenHandler.cpp:191-198`). `setPositionGlobal` assigns
  the box (`pins/Hypr-Target.cpp:11`) and, for a window target, pushes it to the client
  (`pins/Hypr-WindowTarget.cpp:94`).
- `size` in the dump is the **goal**, not the on-screen value (`pins/HyprCtl.cpp:427`), so there is **no lag
  window**: the mode and the box are set in one main-thread call (handler `:96-101`, the mode setter before
  `setTargetSizeAndPosition`), and `hyprctl` cannot interleave. The "fullscreen request pending" counterexample
  is therefore **refuted** on this commit.
- **Client-only fullscreen exists and leaves the box alone**: `fullscreenstate` takes internal and client
  separately (`pins/Hypr-DispatcherTranslator.cpp:188-206`), so `fullscreenstate 0 2` gives internal 0 / client
  2 while `setTargetSizeAndPosition` returns at the internal-0 guard. The window keeps its rule-shaped box. This
  is why internal-only is the **right key** for the box question (and why the frozen control list can mark a
  `fullscreenClient`-reading variant MISSED, `receipts/ctl-c1.txt` K10).
- `sync_fullscreen` is a window rule (`pins/Hypr-WindowRuleEffectContainer.cpp:59`) that forces the two equal;
  without it they diverge. It is not a falsifier, it is the exception that proves the separation.
- **Maximized is also the default handler's work area only.** On the scrolling layout the handler sets the
  column width, not the work area (`pins/Hypr-ScrollingFullscreenHandler.cpp:523`); the host runs
  `general:layout=dwindle` (`receipt-host.txt`), so the pinned grounding covers the host. The claim's prose
  ("a maximized window's box is the work area") is handler-specific, not general.
- **Window groups**: the group target forwards its box to the *current* member only
  (`pins/Hypr-WindowGroupTarget.cpp:34`), so "the fullscreen window's box is the monitor box" is really "the
  current group member's box". Report word unaffected; premise wording overbroad.
- **The rule's size is not meaningless while maximized/fullscreen**: the `size` rule is read only on the first
  map (`pins/Hypr-DefaultFloatingAlgorithm.cpp:49,55`); afterwards the floating algorithm uses the **remembered**
  box (`:85-87`), which the handler stores at the moment of entering FS (`pins/Hypr-FullscreenHandler.cpp:131`).
  So for a floating window that was 420x500 and then went fullscreen, the 420x500 returns on exit — the rule
  remains the window's stored geometry, invisible to `clients -j`. This supports "not comparable" over the
  registry's "the rule's box was replaced, so say FULLSCREEN and OK".
- **TILED was not a false report for maximized tiled windows.** A non-floating window's `size` rule is stored as
  the *pseudo* size (`pins/Window.cpp:2408`) and decides the box only when the target is pseudo
  (`pins/Hypr-WindowTarget.cpp:197`). For an ordinary tiled maximize the rule never shaped the box, so TILED was
  true; the claim's "and a maximized tiled one TILED" (registration) is an overstatement. The genuine TILED hole
  is the pseudo-tiled one, already listed as closure D3 and already narrowed in SKILL.md's TILED row.

## 2. Counterexample 1 — the state verdict turns a true mismatch into exit 0

Inputs are frozen dumps in `scenarios/`, run through both tools; the full byte output is `receipt-runs.txt`
(`r43` = `tools/mado-geometry.py` at base e2289516, `r44` = `pins/ref-tool.py`, `cmp` IDENTICAL to
`.ufo/waves/round-44/c1/ctl-ref-tool.py.txt`). Rules file: `float on` + `size 420 500` for
`^(org\.omarchy\.gkeep)$`. Host geometry for the numbers: DP-1 3440x1440, reserved top 26 → work area
3440x1414 (`receipt-host.txt`).

S1 (floating gkeep, internal 2, box = monitor box 3440x1440):

```
r43 MADO_GEOM_CLIENT: … size=3440x1440 want=420x500 float_rule=on verdict=DIFFER
r43 MADO_GEOMETRY: … matched=1 … agree=0 differ=1 tiled=0 badsize=0 verdict=DIFFER     rc=1
r44 MADO_GEOM_CLIENT: … size=3440x1440 want=420x500 float_rule=on verdict=FULLSCREEN
r44 MADO_GEOMETRY: … matched=1 … agree=0 differ=0 tiled=0 badsize=0 maximized=0 fullscreen=1 verdict=OK   rc=0
```

Both client lines are true. The **summaries disagree**, and r44's is an unearned conformance claim: the rule is
demonstrably not in effect, `differ` is now 0 because the client was removed from the comparison, and rc 0 is
what a caller gates on. S2 (internal 1, work area 3440x1414) and S7 (two state clients, both mismatched) behave
the same: `differ 2 → 0`, `DIFFER rc 1 → OK rc 0`.

Honesty about novelty: round 43 already printed `verdict=OK` rc 0 when the only matched client was TILED
(S3 r43: `tiled=1 agree=0 differ=0 verdict=OK rc=0`). So "OK with nothing compared" is **not new** — C1 enlarges
an existing hole to the class the tool was built for (the registration says gkeep is fullscreen when open).
That makes the correction a frontier-step fix (same word for both), not a C1-only defect.

## 3. Counterexample 2 — the exit map the claim leaves standing

`SKILL.md:281`: "Exit map: 0 `OK` · 1 `DIFFER` (at least one matched client differs) …". After C1, exit 0 no
longer implies the parenthetical (S1: no matched client differs *because none was compared*). C1's scope names
"its SKILL/PROVINCE rows"; the claim text simultaneously says the top verdict rules "and their exit codes are
unchanged" (`c1-r44-geometry-states.py:24`). Both can be true only if the SKILL row is rewritten to say what the
codes now mean — which the registration does not name. **Fixable documentation defect**, one row.

## 4. Counterexample 3 — "false report" is the wrong diagnosis, and it costs the signal

- The word was already disclaimed: `tools/mado-geometry.py:57` — DIFFER "is a report, not a fault: a user may
  have resized the window, or the compositor may have clamped the rule's size."
- SKILL.md's DIFFER and TILED rows licence exactly the compositor-set box and the pseudo-tiled exception, so
  DIFFER/TILED were the documented semantics, not errors.
- Consequence: C1 removes the only field (`differ`) that told a reader "the rule is not in effect", and replaces
  it with a state word that the exit map does not licence. The information is recoverable only by a human who
  knows `fullscreen=1` implies "not compared".
- Where C1 is **right and should not be weakened**: S5 (internal 2, size exactly 420x500) — r43 prints AGREE,
  crediting a coincidence; the r44 contract refuses it (`c1-r44-geometry-states.py:238`, fixture `fsagree0`). That
  is a genuine false-positive fixed. The fix should keep refusing the coincidence *and* keep the mismatch.

## 5. Verdict per scenario (tool output · true state · right/wrong)

True state is from the pins, not from the tool; "r43"/"r44" are byte outputs in `receipt-runs.txt`.

| # | dump | true state (source) | r43 | r44 | judgement |
|---|---|---|---|---|---|
| S1 | float, internal 2, 3440x1440 | box = monitor logical box (`Handler:192-194`); rule stored as floating box (`DFA:85-87`, `Handler:131`) | client DIFFER; `differ=1`; rc 1 | client FULLSCREEN; `differ=0`; `verdict=OK` rc 0 | r44 **client right, summary wrong** — OK asserts conformance where the rule is not in effect |
| S2 | float, internal 1, 3440x1414 | box = work area (`Handler:196-198`) | DIFFER, rc 1 | MAXIMIZED, agree=0 differ=0, OK rc 0 | same; MAXIMIZED is the right word |
| S3 | tiled, internal 1, 1720x1414 | rule never shaped the box; only pseudo size (`Window.cpp:2408`, `WindowTarget:197`) | TILED, OK rc 0 | MAXIMIZED, tiled=0, OK rc 0 | both true; r44 **less explanatory** (hides that tiling is the reason), no factual error |
| S4 | float, no mode, 420x500 | rule applied at first map (`DFA:49,55`) | AGREE, OK rc 0 | **byte-identical** | right; the "no state ⇒ unchanged line" clause holds |
| S5 | float, internal 2, size = 420x500 | box is the monitor box; the match is a coincidence | AGREE (credits the coincidence) | FULLSCREEN, agree=0 | r44 **right**, r43 wrong — the strongest support for C1 |
| S6 | float, internal 0, client 2, 3440x1440 | client hid decos; box untouched (`DispatcherTranslator:188-206`) | DIFFER rc 1 | DIFFER rc 1 | right for the box question; client FS invisible — a declared exclusion (control K10) |
| S7 | internal 2 + internal 1, both mismatched | both boxes compositor-set | DIFFER rc 1 | OK rc 0 (fullscreen=1 maximized=1) | same defect as S1, twice |
| S8 | internal 2 mismatched + a genuine DIFFER | one box differs for a real reason | DIFFER rc 1 | DIFFER rc 1 | right; shows the defect only bites when *every* mismatch is state-caused |

Not verified (declared): a live fullscreen/maximized window (`clients -j` on this host has none; creating one
needs a compositor mutation, forbidden); a fullscreen **group** member's dump; the map-order of the `size` rule
vs a `maximize`/`fullscreen` rule for a rule-born maximized window (the rule branch is first-map-only, so the
"restored on exit" argument is evidenced for transition-into-FS only).

## 6. Impacted axes

- **operability (C1)**: the state word is a real improvement (S5), but the contract as frozen scores `verdict=OK`
  for S1/S2/S7 — the counter's clause `f` *requires* it, so no control can catch it; the controls check
  conformance to the model, not the model's honesty.
- **the no-harm clause `r` is vacuous for this change**: `quality/counters/c1-r42-geometry.py` contains no
  `fullscreen` token at all (`grep -c fullscreen` = 0), so every r42 fixture has fsmode 0 and the old contract
  cannot observe the new behaviour. "No harm to the round-43 contract" is true only because the old contract
  never sees the field.
- **documentation**: `SKILL.md:281` exit map, the § "Rule size versus reported size" verdict table (needs a
  FULLSCREEN/MAXIMIZED row with the "not compared" licence), PROVINCE.md row, and a lesson row for the exit-map
  change. Also SKILL.md:225's summary example if it is refreshed.
- **coverage (C2)**: the round-44 entry must say *which* box is sent after the compositor sets it — internal
  mode only, client mode not — otherwise the entry inherits the same conflation (client FS versus internal FS)
  that the state verdict now makes load-bearing.

## 7. Smallest safe correction (ranked)

1. **Make exit 0 mean "compared and agreed".** Keep the r44 client-line verdicts and the ` maximized= fullscreen=`
   segment; add one branch: when `matched > 0` and `agree == 0` and `differ == 0` (TILED-only, state-only, or
   both), print a distinct word (e.g. `NOT_COMPARED`) with a non-zero exit instead of `OK`. One branch, one exit
   code, fixes the pre-existing TILED hole and the new state hole together; S1/S2/S3/S7 then stop claiming
   conformance. Requires the registration's "exit codes unchanged" sentence to be withdrawn, not the model.
2. **Keep the comparison as an annotation.** Add `state=<none|maximized|fullscreen>` to the client line and keep
   `agree/differ` computed as in round 43 (a state client with `size != want` still counts in `differ`; a state
   client with `size == want` counts in neither, so S5's coincidence stays uncredited). Strictly more
   information than option 1, but it needs a fourth tally and a summary-field change, and the frozen fixtures
   (26) would all need re-deriving.
3. **Do nothing to the model, fix the prose.** Withdraw "false report" from the registration and the lesson,
   rewrite `SKILL.md:281` and the verdict table, and record the OK-without-compare hole as an open predicate
   defect for round 45. Cheapest, but it leaves the exit code lying.

## 8. Evidence index (all in this seat dir)

- `pins/` + `pins/SHA256SUMS` — 15 fetched files at Hyprland `efb50993…` plus the ref-tool copy.
- `scenarios/` — the eight dumps and `rules.conf`.
- `receipt-runs.txt` — `cmp` identity, both tools' full stdout/rc per dump.
- `receipt-host.txt` — `hyprctl version|getoption general:layout|monitors|clients` (read-only).
- `quotes.json`, `verify-quotes.py`, `receipt-quotes.txt` — 40/40 quotes verified at their cited lines.
