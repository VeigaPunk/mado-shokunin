# CritEntryOverreach — sentence-by-sentence overreach audit of the landed C2 entry

Seat `CritEntryOverreach`, mado round 43, w2 (falsify the landed data). Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`.
Entry under attack: `corpus/knowledge/hyprland-gkeep-geometry-r43.md` at
`1959770657f1f8665097c1aed4be6c1cbb07139f` (base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`),
80 lines, sha256 `4d16b3fb289d4844d4e6985d7ec2d10f52059cdf87a103f9333443c863b6af0a`
(`git show <rev>:corpus/knowledge/hyprland-gkeep-geometry-r43.md | sha256sum`).
Freezes read first: `registration.md` (`b2e2efd6…`), `registration-v2.md` (`496340dd…`).

Verdict: **1 material defect, 10 precision/grading defects, 0 proven false provenance.**
The predicate is not the problem — `PRED-C2-r43-v2` scored `admitted=1/1` (clause g binds quotes to
locators, not claims to evidence). The defect is content: one INF sentence states a compositor
universal that a pinned file refutes, and it is the sentence that licenses the entry's "without
`float on` the rule is inert" reading and the SKILL.md TILED row.

## Method

Every sentence of the entry was opened against the receipt it rests on: the ten files in
`.ufo/waves/round-43/fetch/` (all re-fetched from
`raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/…` and
`cmp`-identical to the fetch copies — `provenance-check.txt`), the w1 seat trees
`w1/ExecOracleGkeep/`, `w1/ExecGoalVsValue/` (its `pins/` holds `Window.cpp`, 124226 B,
sha256 `d735d454…`, `cmp`-identical to upstream), and the two C2 receipts. Quotes are ≤ 25 words,
located, and checked by `verify-quotes.py` (`verify-quotes.txt`, `VERIFY: PASS`).

Classification rules used: **SUPPORTED** = the named receipt shows the sentence's claim at the
locator; **OVERSTATED** = the receipt licenses something narrower; **UNSUPPORTED** = no receipt in
the lane shows it; **WRONG** = a receipt shows the opposite.

## Table — every sentence

Header metadata (lines 3-17) is one row per source row; each was checked against the pinned file.

| line | sentence (abridged) | class | evidence |
|---|---|---|---|
| 3 | S295 = host's three rules for the class | SUPPORTED | `host-gkeep.conf:2-4` = float/center/size, one line each; comment line 1 |
| 4 | S290 = FullMatch + `negative:` prefix | SUPPORTED | `RegexMatchEngine.cpp:16`, `:7-9` |
| 5 | S155 = static arm stores size as expression | SUPPORTED | `WindowRuleApplicator.cpp:421-426` |
| 6 | S291 = first-map branch evaluates the stored size | SUPPORTED | `DefaultFloatingAlgorithm.cpp:49,55-56` |
| 7 | S292 = where a target keeps its box | SUPPORTED | `Target.cpp:10-13` |
| 8 | S293 = floating branch hands the box over | SUPPORTED | `WindowTarget.cpp:70-71` |
| 9 | S294 = GOAL against CURRENT on the animated size | SUPPORTED | `GeometricMovableAnimated.cpp:19-20` |
| 10 | S158 = `clients -j` size fields from the GOAL | SUPPORTED | `HyprCtl.cpp:427-428`, `:448` |
| 11 | S297 = lines 446-488 of ui.py at gkeep 133b867 | SUPPORTED | excerpt data lines 3-45 `diff`-identical to `ui.py:446-488`; full file sha256 `07a3c4a5…` recomputed, 488 lines, HEAD `133b8671…` |
| 12 | S296 = reduced `clients -j`, today's census | SUPPORTED | `host-clients-r43.json:1-62`, 4 objects |
| 14 | recheck: 7 Hyprland files + 3 own-work + counter; tag/config edit is the earlier trigger | SUPPORTED | 7 rows (S290, S155, S291-S294, S158); 3 own-work (S295-S297) |
| 15 | ground: why… which link decides… what the socket can and cannot tell | SUPPORTED | matches §§1-5 |
| 17 | assimilated-from r11, four-link chain | SUPPORTED | `merge/mado/knowledge/corpus/knowledge/gkeep-size-to-real-size-r11.md` exists; `**Step one**`…`**Step four**` = four links |
| 23 | table row 1: rule text, OBS | SUPPORTED | `host-gkeep.conf:1-4` |
| 24 | table row 2: regex vs app id, OBS (source) + INF (join) | SUPPORTED | `RegexMatchEngine.cpp:16`; excerpt:6 |
| 25 | table row 3: box of a **first-mapped floating gkeep window**; state "OBS (source); OBS in an isolated oracle, not on the host session" | **OVERSTATED** | the oracle's client is `gkeep-shm.c`, a 200x200 shm buffer with no `set_default_size` (`w1/ExecOracleGkeep.md` §2), not a gkeep window; and the observation needed a headless output the plain layout does not have (`40-monitor-requirement.txt`) |
| 26 | table row 4: JSON builder reads the GOAL, OBS | SUPPORTED | `HyprCtl.cpp:427-428`; `ExecGoalVsValue/finding.md` §1 |
| 27 | table row 5: "no read verb exposes CURRENT" | **OVERSTATED** | see line 56 — `eval`/`repl` at `HyprCtl.cpp:2042-2043` |
| 28 | table row 6: "four mapped tiled clients" | **OVERSTATED** (low) | the pinned dump is reduced to `address/mapped/class/floating/size/at/monitor` — no `fullscreen`; "none is floating" is the observable |
| 32 | one `size`, one `float on`, one `center on`, comment avoids the floating tag | SUPPORTED | `host-gkeep.conf:1-4` |
| 34 | FullMatch whole-string; `negative:` stripped and inverted "(constructor, lines 7-8)" | **OVERSTATED** (low) | the strip is `regex.substr(9)` at `:9`; the inversion is `!= m_negative` at `:16`, not in the constructor |
| 36 | …"the dots match any character"… | **OVERSTATED** (low) | RE2 default dot excludes `\n`: probe `FULLMATCH 'a.b' vs 'a\nb' -> False`, `Options.dot_nl = False` (`re2-probe.txt`); `re2::RE2` is built with default options at `RegexMatchEngine.cpp:12`. The other two clauses hold (`org.omarchy.gkeep2` -> False, `orgXomarchy.gkeep` -> True in the same probe) |
| 40 | `static_.size = expr;` at :426, arm resets when empty | SUPPORTED | `WindowRuleApplicator.cpp:421-426` |
| 42 | the default floating algorithm evaluates the expression **only inside its first-map branch** | SUPPORTED **as scoped to that algorithm** — not compositor-wide (see line 48) | `DefaultFloatingAlgorithm.cpp:49` gate, `:55-56` the only `static_.size` read in the file |
| 44 | `setPositionGlobal` assigns and rounds both boxes | SUPPORTED | `Target.cpp:10-13` |
| 46 | floating non-fullscreen branch hands the box to the window | SUPPORTED | `WindowTarget.cpp:70-71` |
| 48 | "A tiled window never takes this branch: the size rule only acts through the floating algorithm, so without `float on` the rule's 420x500 is inert and the tiler decides the box." | **OVERSTATED — borderline WRONG** | the branch claim holds (`floating()` = `m_window->m_isFloating`, `WindowTarget.cpp:281-282`); "only acts through the floating algorithm" and "inert" are refuted by `Window.cpp:2402-2408`: at map the non-floating arm evaluates the same expression and stores it as the target's pseudo size, and the tiled path consumes `m_pseudoSize` at `WindowTarget.cpp:197-215` |
| 52 | GOAL/CURRENT accessors at :19/:20 | SUPPORTED | `GeometricMovableAnimated.cpp:17-21` |
| 54 | `clients -j` fills size from the goal, width one line earlier, text formatter at :448 | SUPPORTED | `HyprCtl.cpp:427-428` (quote spans 428-429 verbatim), `:448` |
| 56 | "while the open animation runs, the current value differs from the goal (… `popin 87%` …), and no read verb of the request socket exposes the current value" | **OVERSTATED** (low) | the GOAL/CURRENT split and the 87 % style are receipt-backed (`pins/omarchy-looknfeel-80-96.txt:95`, `host-config-chain.txt`); "no read verb" is false as a universal: `eval`/`repl` are registered request-socket verbs and evaluate Lua (`HyprCtl.cpp:1110-1119`, `:2042-2043`), declining only because this host is hyprlang |
| 60 | app asks 420x500; "on a `Gtk.ApplicationWindow` of the application whose id is `org.omarchy.gkeep` (line 6)" | **OVERSTATED** (locator) | excerpt `:33-34` exact; the id is `:6`, but the `Gtk.ApplicationWindow` is `:31` — one locator for two facts |
| 62 s1 | two agreeing numbers are not one observation | SUPPORTED | INF; follows from excerpt:33-34 + `host-gkeep.conf:4` |
| 62 s2 | in the isolated round-27 oracle a client with that app id reported [420,500] floating true; size removed -> 200x200; 300x300 -> 300x300; float removed -> tiled | SUPPORTED | `10-cases.txt` (headlesshost/host-r1..r3 [420,500] True; floatonly [200,200] True; size300 [300,300]; nofloat [918,498] False); `20-observation.txt` §1,§5 |
| 62 s2 parenthetical | "(a Hyprland 0.56.2 nested under tinywl in bubblewrap, never the host session)" | **OVERSTATED** (low) | true as far as it goes, but the plain layout maps **no** window (`40-monitor-requirement.txt`: `monitors -j` `[]`, `mapWindow: no valid monitor/workspace`); the observation exists only after `output create headless HEADLESS-2` in the nested instance (`ExecOracleGkeep.md` §3) |
| 62 grade | the whole paragraph is graded **INF** while it carries the oracle's observations | **OVERSTATED** (label) | the table row 25 already calls the oracle OBS; the grade should be split (replacement below) |
| 62 s3 | "In that oracle, the rule, not the client, is the origin of 420x500." | SUPPORTED | the `floatonly` isolating control (`10-cases.txt`, `20-observation.txt` §5); the oracle client asked for nothing |
| 66 | four mapped clients, none floating, chromium example at :50-51, no gkeep class | SUPPORTED | `host-clients-r43.json:47-51`, `:1-62` |
| 68 | no gkeep window open; tool answers `NO_MATCHING_CLIENT` today | SUPPORTED | `receipts/live-geometry-host.txt` (`verdict=NO_MATCHING_CLIENT`, `exit=3`) |
| 70 | census recomputed by the C2 counter from the three own-work receipts | SUPPORTED | `quality/counters/c2-r43-gkeep-entry-v2.py:357-400` (`host_census`, clause h) |
| 72 | `host rules size=420x500 float=on center=on class=^(org.omarchy.gkeep)$` | SUPPORTED | `host-gkeep.conf:2-4`; recomputed line equals it |
| 73 | `host clients total=4 floating=0 gkeep=0` | SUPPORTED | `host-clients-r43.json` |
| 74 | `gkeep request default_size=420x500 application_id=org.omarchy.gkeep` | SUPPORTED | excerpt `:6`, `:33` |
| 78 | "the GOAL is what every read verb reports" | **OVERSTATED** (low) | only the geometry verbs do; `version`, `binds`, `monitors`, … report no goal |
| 79 | "the size rule is evaluated on first map only" | SUPPORTED | both reads are in `mapWindow` (`Window.cpp:2079` sets `m_firstMap` true on every map, so a remap re-evaluates; the events the bullet lists — resize, monitor change, rule reload — are not maps) |
| 80 | behaviour on any other Hyprland version | SUPPORTED | scoped to `efb5099`; self-limiting |

## Counterexample for the material defect (line 48)

A **tiled** window carrying `windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$` (with or
without `float on`):

1. `Window.cpp:2407-2408` — the non-floating arm of `mapWindow` sets
   `setPseudo = true; m_target->setPseudoSize(*COMPUTED);` from
   `calculateExpression(*m_ruleApplicator->static_.size)` (`:2403`). The rule is **read** for a
   tiled window, outside the floating algorithm.
2. `Target.cpp:93-97` stores it (`m_pseudoSize = size; recalc();`) and `setPseudo` (`:80-87`) later
   recalculates through the same box.
3. `WindowTarget.cpp:197-215` — the non-FS **tiled** branch replaces `calcSize` with `m_pseudoSize`
   whenever `isPseudo()` (`:210`, `:215`).

So on this host a tiled gkeep window with pseudo enabled is 420x500 **because of the size rule**.
"the size rule only acts through the floating algorithm", "the rule's 420x500 is inert" are false;
only "the tiler decides the box" survives (and the oracle's `nofloat` case, 918x498, is the box-level
observation of exactly that).

The entry's INF carries no `Basis:` and the w1 receipt it leans on skips the site: the map-path
walk in `w1/ExecGoalVsValue/finding.md` §2 lists `window.cpp:2079, 2383, 2520, 2524, 2526` and
concludes "a tiled target goes to `m_tiled->newTarget(target)`, where the `static_.size` branch is not
reached" — true of that branch, silent about `:2402`. The round's own survey had already flagged the
path (`w1/ScoutStagedGkeep/survey.md:137`: the pseudo-size path "flips only with Window.cpp pinned"),
and w1 then pinned `Window.cpp`. The draft `w1/ScrEntryA/…:47` said "cannot reach a tiled window"
and `:55` noticed the tiled path "computes … pseudo size"; the landed entry kept the conclusion and
dropped the counter-evidence it had in hand.

## Exact replacement text (every non-SUPPORTED sentence)

**L34** — replace `and the result is inverted (constructor, lines 7-8).` with:

> and the result is inverted (constructor, lines 7-9; the inversion itself is the `!= m_negative` at line 16).

**L36** — replace the parenthetical clause `the dots match any character, so a class such as `orgXomarchy.gkeep` would` with:

> the unescaped dots match any one character except a newline (RE2's default options, none passed at `RegexMatchEngine.cpp:12`), so a class such as `orgXomarchy.gkeep` would

**L48** — replace the whole sentence with:

> **INF** A tiled window never takes this branch — `floating()` is `m_window->m_isFloating` (`Hyprland-WindowTarget.cpp:281-282`) — and the box a tiled window gets is the tiler's, which is why the oracle's `nofloat` case reported the layout's 918x498 and not 420x500. The rule's text is not inert for a tiled window, though: at map the same expression is read once in the non-floating arm (`if (m_ruleApplicator->static_.size) { … m_target->setPseudoSize(*COMPUTED); }`, `Window.cpp:2402-2408`, pin `.ufo/waves/round-43/w1/ExecGoalVsValue/pins/window.cpp`) and stored as the target's pseudo size, and the tiled path substitutes `m_pseudoSize` for `calcSize` whenever the target is pseudo (`if (isPseudo() && m_window && …`, `Hyprland-WindowTarget.cpp:197-215`). So `size 420 500` decides a tiled gkeep window's pseudo-tile size; its tiled box is still the tiler's.

**L56** — replace the final clause `and no read verb of the request socket exposes the current value.` with:

> and no geometry read verb of the request socket exposes the current value (no `GEOMETRIC_CURRENT` occurs anywhere in `Hyprland-HyprCtl.cpp`); the one general reader is `eval`/`repl`, which evaluates Lua and declines unless the config manager is Lua (`return "eval is only supported with the lua config manager";`, `HyprCtl.cpp:1110-1112`, registered `:2042-2043`), and this host's config chain is hyprlang `.conf`.

**L27 (table row 5, answer cell)** — replace `the animated type keeps GOAL apart from CURRENT; no read verb exposes CURRENT` with:

> the animated type keeps GOAL apart from CURRENT; no geometry read verb exposes CURRENT (`eval`/`repl` would need a Lua config manager, `HyprCtl.cpp:1110-1112`)

**L25 (table row 3, state cell)** — replace `OBS (source); OBS in an isolated oracle, not on the host session` with:

> OBS (source); OBS in an isolated oracle for a stand-in client carrying gkeep's app id (a 200x200 buffer, no `set_default_size`), not on the host session

**L28 (table row 6, answer cell)** — replace `today's census: four mapped tiled clients, none of them gkeep` with:

> today's census: four mapped clients, none floating, none of them gkeep

**L60** — replace `on a `Gtk.ApplicationWindow` of the application whose id is `org.omarchy.gkeep` (line 6).` with:

> on a `Gtk.ApplicationWindow` (`window = Gtk.ApplicationWindow(application=self, title="gkeep")`, line 31) of the application whose id is `org.omarchy.gkeep` (line 6).

**L62 parenthetical** — replace `(a Hyprland 0.56.2 nested under tinywl in bubblewrap, never the host session)` with:

> (a Hyprland 0.56.2 nested under tinywl in bubblewrap inside the round-27 harness, with a headless output created in the nested instance because the plain layout maps no window, never the host session)

**L62 label** — split the one **INF** into three grades (the oracle figures are observations, and the table already calls them OBS):

> **INF** Two agreeing numbers are not one observation: the client's default size and the rule's size coincide, so a 420x500 report alone cannot say which of the two set it. **OBS** In the isolated round-27 oracle (…) a client with that app id reported `"size": [420, 500]`, `"floating": true` under the host's three rules; with the size line removed … it was tiled (…). **INF** In that oracle the rule, not the client, is the origin of 420x500: the `floatonly` control, with no size rule, reported the client's own 200x200.

**L78** — replace `- The current (drawn) size of a gkeep window at any moment on the host; the GOAL is what every read verb reports.` with:

> - The current (drawn) size of a gkeep window at any moment on the host; the GOAL is what every read verb that reports a window's geometry reports.

## Collateral (outside my write scope, same defect)

`SKILL.md:270` TILED row, landed by the same claim:
`| TILED | the matched client is not floating, so the first-map floating branch that reads ``static_.size`` never ran for it: the rule's size is inert for this client | … |`
The first clause is true; "inert for this client" repeats L48's error (the value is the client's
pseudo size). Smallest safe edit: `the rule's size never reaches this client's box (it is still
stored as the target's pseudo size, Window.cpp:2402-2408)`. Leaving it would make the entry and the
skill row two authorities that disagree once the entry is repaired.

## Impacted axes

- **Coverage** (C2's axis): one INF sentence wrong about a compositor mechanism; nine precision
  defects in the same deliverable. `verdict=TARGET_MET` still measures the *predicate* correctly —
  `PRED-C2-r43-v2` clause g binds quotes to locators and has no claim-to-evidence binding (the
  declared v2 residual, `registration-v2.md`: A1/A2/D1/E2/H1/X1 stay admitted). This is an open
  defect of the predicate's *reach*, not a miscount.
- **Operability** (C1): unaffected. C1 reads no C2 file; `tools/mado-geometry.py` is byte-identical
  to the round-42 reference (`e3c2e471…` in `receipts/c1-after-data.txt`, `live-geometry-host.txt`),
  and TILED verdicts do not depend on the pseudo-size path. Nothing here asks C1 to change.
- **Navigation / calibration**: untouched; no registry row, locator or tally is affected (all ten
  ids resolve at their claimed lines; provenance re-fetch is byte-identical).

## Residuals of this review

- I did not run the C2 counter or any control (main-agent/L1 work); `receipts/c2-after-data.txt` was
  read as given.
- The `Window.cpp` site is proven from a w1 pin that is `cmp`-identical to upstream at `efb5099`
  (`provenance-check.txt`); it is not one of the entry's ten PINS, so a L1 fixing L48 must either
  cite the w1 pin or open `Window.cpp` as a row (S301 already proposes it).
- "no read verb" is a universal negative; I falsified the absolute form only. I did not enumerate
  plugin-registered verbs (`CHyprCtl::registerCommand` / `unregisterCommand`, `HyprCtl.cpp:2054-2060`,
  an open registry), which is a second reason to keep the sentence scoped to the built-in set.
- `m_firstMap` is set true on every `mapWindow()` (`Window.cpp:2079`), so line 79's "first map only"
  is "only on a map"; the bullets' listed events are unaffected. Noted, not scored.

## Tooling

`google-re2 1.1.20251105` via `uv pip` into a scratch venv under
`/fast/scratch/hyaku/mado-r43/CritEntryOverreach/venv` (channel: uv pip; reason: to run the entry's
own regex through the RE2 library that `RegexMatchEngine.cpp` links instead of asserting dot
semantics from memory). No pacman, no host verb beyond the allowed reads. Scratch tree deleted at
seat end; every citable file is in this directory.

## Reproduce

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 .ufo/waves/round-43/w2/CritEntryOverreach/verify-quotes.py      # VERIFY: PASS
git show 1959770657f1f8665097c1aed4be6c1cbb07139f:corpus/knowledge/hyprland-gkeep-geometry-r43.md | sha256sum
sed -n '2399,2409p' .ufo/waves/round-43/w1/ExecGoalVsValue/pins/window.cpp
grep -c GEOMETRIC_CURRENT .ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp   # 0
```
