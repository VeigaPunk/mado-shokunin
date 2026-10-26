# CritEntryOverreach — overreach audit of the landed C2 entry (w2)

Seat `CritEntryOverreach`, mado round 43 w2. Attack surface:
`corpus/knowledge/hyprland-gkeep-geometry-r43.md` at `1959770657f1f8665097c1aed4be6c1cbb07139f`
(sha256 `4d16b3fb…`). Full table + exact replacements:
`.ufo/waves/round-43/w2/CritEntryOverreach/findings.md`.

**Verdict: 1 material defect, 10 precision/grading defects; provenance clean; C1 untouched.**

## The material defect (entry line 48, the §2 INF)

> "A tiled window never takes this branch: the size rule only acts through the floating algorithm,
> so without `float on` the rule's 420x500 is inert and the tiler decides the box."

Counterexample, from a pinned source file: at map, the **non-floating** arm of `mapWindow` evaluates
the very same size expression and stores it as the target's pseudo size —
`if (m_ruleApplicator->static_.size) { … m_target->setPseudoSize(*COMPUTED); }`
(`Window.cpp:2402-2408`, pin `.ufo/waves/round-43/w1/ExecGoalVsValue/pins/window.cpp`,
`cmp`-identical to upstream at `efb5099`) — and the tiled branch consumes it:
`if (isPseudo() && m_window && …` substituting `calcSize = m_pseudoSize` (`Hyprland-WindowTarget.cpp:197-215`).
So `size 420 500` is **not inert** for a tiled gkeep window: it is that window's pseudo-tile size.
The surviving clause is "the tiler decides the box" (oracle `nofloat` case: 918x498,
`w1/ExecOracleGkeep/10-cases.txt`). The entry's INF carries no `Basis:`, and the w1 map-path walk it
leans on skipped `:2402`; w1's own survey had flagged the pseudo-size path as the thing `Window.cpp`
would settle (`w1/ScoutStagedGkeep/survey.md:137`), and w1 then pinned that file.

## Precision defects (all with replacement text in findings.md)

- **L56 / table row 27**: "no read verb of the request socket exposes the current value" — `eval`/`repl`
  are registered request-socket verbs that evaluate Lua (`HyprCtl.cpp:1110-1119`, `:2042-2043`); they
  decline only because this host is hyprlang. Scope it to *geometry* read verbs.
- **L78**: "the GOAL is what every read verb reports" — only the geometry verbs do.
- **L36**: "the dots match any character" — RE2's default dot excludes `\n`
  (probe `re2-probe.txt`: `a.b` vs `"a\nb"` → False, `Options.dot_nl = False`; no Options passed at
  `RegexMatchEngine.cpp:12`). The other two clauses hold.
- **L34**: the `negative:` strip is `regex.substr(9)` at `:9`; the inversion is `!= m_negative` at `:16`,
  not "constructor, lines 7-8".
- **L60**: `(line 6)` locates the `application_id`; the `Gtk.ApplicationWindow` is excerpt `:31`.
- **L62 parenthetical**: the plain round-27 layout maps no window
  (`40-monitor-requirement.txt`); the observation needed a headless output created in the nested
  instance (`ExecOracleGkeep.md` §3).
- **L62 grade**: the paragraph is graded INF although it carries oracle observations the table calls OBS.
- **Table row 25**: the oracle observed a stand-in (`gkeep-shm.c`, 200x200 buffer), not "a gkeep window".
- **Table row 28**: "four mapped tiled clients" — the reduced dump has no `fullscreen` field;
  `floating: false` is what it shows.

## Collateral (outside my write scope)

`SKILL.md:270` (TILED row) repeats the same error ("the rule's size is inert for this client").
Repairing the entry alone would leave entry and skill row disagreeing; exact edit in findings.md.

## What I verified, and with what

- `verify-quotes.py` → `verify-quotes.txt`: **53 quotes, 0 fails, VERIFY: PASS** (each quote ≤ 25 words,
  matched at its claimed physical line; `GEOMETRIC_CURRENT` count in `HyprCtl.cpp` = 0).
- `provenance-check.txt`: all 7 Hyprland files re-fetched from `raw.githubusercontent.com` at
  `efb50993780079460b0cbed1363e2166a2de1d9f` are `cmp`-identical to `fetch/`; the w1 `window.cpp` pin is
  identical to upstream (sha256 `d735d454…`). No false provenance.
- Own-work: gkeep excerpt data lines `diff`-identical to `ui.py:446-488`; full-file sha256
  `07a3c4a5…` recomputed, 488 lines, HEAD `133b8671…`. Census lines match the receipts.
- Not run (not my assignment): the C1/C2 counters and controls; `receipts/c2-after-data.txt` read as given.

## Tooling

`google-re2 1.1.20251105` via `uv pip` into `/fast/scratch/hyaku/mado-r43/CritEntryOverreach/venv`
(reason: run the entry's own regex through the library `RegexMatchEngine.cpp` links, instead of
asserting dot/newline semantics from memory). No pacman, no host write verb, no compositor mutation.
Scratch tree deleted; all citable files are in `.ufo/waves/round-43/w2/CritEntryOverreach/`.
