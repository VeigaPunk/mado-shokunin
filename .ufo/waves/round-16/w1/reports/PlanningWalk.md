# PlanningWalk — Round 16 data walk, one false Waybar inference, U7 route

**Seat:** `MadoR16.PlanningWalk` (UFO-FSD connector, leaf member; no subagent dispatch, no commits, no installs, no live probes)
**Lane:** `/home/vgpnk/Projects/shokunin/mado-shokunin`, baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`
**Scope:** source reading only. No build, lint, test, gate, package, service, compositor, input, screenshot or Waybar producer execution.

## 1. Axes named

Scored sub-axes, read from `SCORECARD.md` (round-12 calibration and coverage rubrics; round-13–15 closures):

| Axis / sub-axis | Rubric | Last recorded value | Recomputed here |
|---|---|---|---|
| coverage / sourced current-art documented routes (C1) | `10 × covered U-items / 7` | U1–U6 → 6/7 = **8.5714** (round 15) | unchanged, 6/7 = 8.5714 |
| coverage / admitted-note reachability | `10 × indexed / notes` | 29/29 (round 15) | 29 `knowledge/*.md` files; README index unchanged here |
| operability / hermetic selftest | `10 × passed / total` | 372/372 (round 15) | not re-run (no-check rule) |
| freshness / file-plane agreement | `10 × PASS/(PASS+FAIL+UNKNOWN)` | 29 PASS, 0 FAIL, 0 UNKNOWN (round 15) | not re-run |
| calibration / lesson-grounded admission criteria | `10 × criteria citing a lesson / criteria` | 6.8750 (round 12, resolver-dependent); round-15 walk wrote 12/17 = 7.0588 | **16/21 = 7.6190 literal upper bound** (see §2) |
| depth, adjacency | unscored (no bounded rubric) | — | — |

## 2. Data walk and a contradiction the wave must see

**Coverage (verified by grep, this session).** `covers: U1`…`covers: U6` each occur once in `corpus/knowledge/` (window-rule-effects-getprop.md, hyprland-config-era-r12.md, xdg-portal-routing-r12.md, wayland-protocol-boundaries-r13.md, output-colour-boundaries-r14.md, input-debugging-boundaries-r15.md). No `covers: U7` exists. U7 (Waybar module text) is the only uncovered item: 6/7 → 7/7 lifts the rubric to 10.0000 on its finite denominator.

**Contradiction — "coverage is the lowest active rubric" is not supported by the current file.**
- `QUALITY.md` now has criteria 1–21. Criteria 6–21 each carry a `(lesson: …)` citation (16 of 21). Literal rubric: 16/21 = **7.6190**. Citation resolution can only lower this, so 7.6190 is an upper bound.
- Coverage is 8.5714. Calibration is therefore lower on the current literal count.
- The round-15 PlanningWalk (`.ufo/waves/round-15/w1/reports/PlanningWalk.md` §1.1) tabulates calibration **7.0588** and coverage **7.1429**, then §1.2 declares coverage "uniquely lowest." Its own table contradicts that claim (7.0588 < 7.1429). The round-15 closure did not re-measure calibration.
- Consequence: a U7 move makes coverage 10.0000 on its finite rubric and leaves **calibration (≤7.6190)** as the lowest recorded axis. The wave premise should be reconciled by L1 before the claim is stated. This seat does not rewrite the plan; it names the contradiction.

**Operability and freshness.** Round-15 closure recorded host-safety harm (forbidden libinput partial upgrade) and kept the gate digest `fba82a66…` unchanged. Nothing in this walk touches the host. The U7 move (corpus-only) does not change those rows.

**Lane state checked.** `corpus/SOURCES.md` registry ends at S052; S053–S055 are unused and reserved for this wave. `corpus/README.md` indexes 29 notes and names U7 as frontier (`README.md` Frontier, lines 104–109).

## 3. One false Waybar inference

**False inference (F-W1):** *"A pure-read producer run now prints the text the bar currently displays."*

**One-case overfit (the instance the corpus already contains):** `corpus/knowledge/waybar-walker-semantics.md` §3.3, row `custom/idle-indicator` (line 139). The RUN column records `{"text": "U+F1AD6", "tooltip": "Idle lock disabled", "class": "active"}` with `pgrep -x hypridle` empty. Read as bar text, that yields "the bar now shows the idle-lock-disabled glyph."

**Why it is false (each point has an anchor):**
1. **Refresh is signal-only.** The module declares no `interval`; `waybar-custom(5)` says "If no interval is defined then a signal will be the only way to update the module" (installed man, zcat lines 90; also lines 66–68). The note itself says the three indicators "move only when their producer fires" (semantics §4, lines 192–194). A fresh RUN is a new sample, not the last value the bar holds.
2. **The bar's value is a function of past executions, not of now.** The displayed text is the output of the last execution the bar performed, possibly before the current hypridle state. The note's own §2.3 ledger says "What text does module X show right now? … **UNK**" (line 102). The RUN column contradicts §2.3 by treating a sample as display.
3. **Format and parse transform the output.** `return-type` selects parse mode; with no `return-type` or an invalid one, Waybar expects i3blocks style (zcat lines 244–249). `format` inserts `{text}` (zcat line 98), `tooltip-format` overrides the script tooltip (zcat lines 186–190), `escape` changes markup (zcat line 194). The displayed string is therefore not the producer's raw stdout.
4. **Class is a style input, not text.** `class` only selects CSS (`waybar-custom(5)` §Style, zcat line 351 region). "Glyph shown = lock disabled" is a rendered-glyph claim the corpus cannot make (`tofu`/font presence is unmeasured here).
5. **Restart state.** Module changes require `omarchy restart waybar` (semantics §6.8 triage table "bar edit did nothing", line 364); the running module may not reflect current config bytes.

**Boundary:** the RUN payload is a dated producer sample. It is evidence of the producer's output at time *t*, not of the bar's text at time *t*. Bar text remains UNK under §2.3 because no IPC or query verb exists in waybar 0.15.0 (`arc-synthesis.md` §6, line 301).

## 4. Generalized route (no extra claims)

The one-case fault generalizes: for any custom module, displayed text = f(last successful execution output, `return-type` parse mode, `format`/`format-icons`, `tooltip-format`, `escape`, `exec-if` history, refresh cadence, process restart state, `$OMARCHY_PATH` in the bar's environment). Several inputs are not observable here. The route therefore stops at the observable rungs and labels the rest UNK.

| Rung | Layer | Source / anchor | Observable here | What it proves | What it cannot prove |
|---|---|---|---|---|---|
| G0 | Declared config bytes | `config.jsonc` module objects, semantics §3 anchors | yes, sha-bound | which module, exec, cadence, format are declared | that the bar runs or shows them |
| G1 | Documented producer contract | `waybar-custom(5)` (S053, reserved; installed man sha256 `c9938e44…` as data cross-check, zcat 351 lines) | yes | exec / exec-if / interval / signal / return-type / format / escape / tooltip-format semantics | the 0.15.0 implementation's exact parse behavior |
| G2 | Parse and format implementation | `src/modules/custom.cpp` tagged 0.15.0 (S054, reserved; opened by other seats, not here) | pending S054 | how stdout is parsed and mapped to text/class | rendered glyph or CSS result |
| G3 | Producer sample | RUN payloads in semantics §3 (dated, pure-read, historical) | yes, as dated history only | producer output at its sample time | bar text now |
| G4 | Displayed text | none (no IPC/query verb, arc §6) | **no** | — | **UNK** |
| G5 | Rendered pixels / glyph | excluded (no screenshot, no screen read) | **no** | — | **UNK** |

**Final section requirement:** `## Unexercised rendering` must carry explicit `[UNK]` for G4, G5, last-execution time, restart state and `$OMARCHY_PATH` in the bar's environment.

## 5. Proposed move (single, bounded)

**Move:** one new knowledge note for U7 — the Waybar module-text observation boundary — stating the producer contract and the producer-to-bar gap, with G0–G3 sourced and G4–G5 labelled UNK. It claims no rendered verification and no live text.

- Required structure (matches the round-16 measure spec, not re-derived here): provenance trio (`source:`, `verified-at:`, `recheck:`), exactly `covers: U7`, reciprocal mined A/B joins S053 (man) and S054 (custom.cpp), level-2 headings `## Producer contract`, `## Renderer boundary`, `## Safe observation`, `## Unexercised rendering`, `[UNK]` in the last section.
- Admission bar: QUALITY criteria 2, 3, 15, 16 (source anchors; observation/inference/unknown separated; config/doc inference never promoted to host behavior). The false inference F-W1 should be stated as a rejected inference.
- Registry (L1): S053 and S054 as `mined`, tier A, `used-by` the new note; S055 is reserved for closure own-work safety and is not needed for this move.
- Index and scorecard (L1): one `corpus/README.md` row (29 → 30), `SCORECARD.md` C1 6/7 → 7/7 (8.5714 → 10.0000) on the declared finite rubric, with the calibration contradiction in §2 recorded beside it.

**Axis verdicts this move would make (predicted, not measured):**
- coverage: improved (6/7 → 7/7).
- operability: unchanged (corpus-only; no host action; gate untouched).
- freshness: unchanged (dated notes keep their recheck; no live reads).
- calibration: unchanged by this move; the lowest-axis contradiction stays open and visible.
- depth, adjacency: unchanged.

**Harm check:** no host probe, no producer execution, no Waybar signal or restart, no `/proc` environment read, no config write. Gate digest unchanged. Navigation counter moves 29 → 30 only if the README row is added.

## 6. Risks

| Risk | Second-order effect | Mitigation |
|---|---|---|
| The note reads RUN as display text (F-W1 reintroduced) | false U7 coverage; calibration falls | `## Renderer boundary` names G3 ≠ G4; `[UNK]` for display; criterion 15/16 cited |
| Citing the installed man as S053 | non-tagged, version-unpinned evidence | S053 must be the tagged 0.15.0 man; installed man is a data cross-check only |
| Over-claiming coverage after 7/7 | finite rubric saturates at 10; looks like full Waybar coverage | state the denominator; broader Waybar behavior stays open |
| Calibration contradiction ignored | wave reports the wrong lowest axis | L1 must reconcile §2 before SCORECARD text lands |

## 7. Verification guidance for L1 (not run by this seat)

1. `sources-census.sh validate` for the S053/S054 rows (expect exit 0; W04 warnings pre-existing).
2. `python3 .ufo/waves/round-16/measure.py HEAD` U7 facets, if that measure exists in the wave.
3. `bash tools/mado-verify.sh --no-live` and `--selftest` (harm watch only; gate unchanged).
4. Confirm `corpus/README.md` lists 30 notes matching `corpus/knowledge/*.md`.
5. Recount calibration from `QUALITY.md` with a resolver before writing any calibration number.

## 8. Limits

- Tagged Waybar 0.15.0 source (S053/S054) was not opened by this seat; those rows belong to the CustomMan/CustomSource/CustomExec seats.
- The installed `waybar-custom(5)` was read as data (sha256 `c9938e4454977ebbf7b8d8631d80103e4b21ce017309e7ca54aae8c7cdf54e93`). Its package identity is the one recorded in the semantics note (waybar 0.15.0-3), not re-queried here.
- Calibration 16/21 is a literal upper bound; resolution was not run.
- Nothing here measures rendered Waybar, module text, host state or input behavior.

## 9. Tooling record

No tools installed, updated or removed. No `pacman`, `-S`, `-Sy`, `-Syu`, `-U`, `-R`, downgrade or service operation was run. Read `/home/vgpnk/.omp/agent/RULES.md` before any install consideration; installs are paused this round, so none were made.
