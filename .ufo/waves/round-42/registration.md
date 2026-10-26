# mado round 42 — registration (frozen before any round-42 data)

Lane `mado-shokunin`, base `62dd798bb08401a8697383552edcc36f109344fa` (the round-41 closure tip; the orchestrator's interrupted-run
snapshot `8af0263` added only this round's uncommitted work and no data). Host `2026-10-25`, Hyprland 0.56.2
(`efb50993780079460b0cbed1363e2166a2de1d9f`). Shape: **two v1 waves** — `w1` (build + first falsifiers, 36 seats) and `w2` (falsify,
dispatched after the data commit, 36 seats), round total 72, no residual call planned. The §3 planner seat is held by the L1
(`MadoR42`); a planning data-walk rides `ScoutStagedGkeep`.

**Lowest-axis rule.** Every published axis ties at its maximum at base (`receipts/axis-base.txt`: navigation 59/59, calibration 63/63,
operability 12/12, `MADO_AXIS checked=3 mismatched=0`), so each is a lowest axis; the stagnation nudge is not needed. Lane axes:
**operability** and **coverage**.

**Inherited state.** Two untracked scratch files of round 41 (`.ufo/waves/round-41/w2/ExecDiffFuzzV2/scratch/s-grow`, `s-size`), routed by
`corpus/lessons/round-41-verifier-spotcheck.md` §6.1, were deleted at round start (lane-authored seat scratch, not deliverables).

## Claims

- **C1 — operability (capability acquisition): `tools/mado-geometry.py`** — a read-only join of the window-rule sizes in Hyprland config
  files and the sizes the compositor reports in one `hyprctl clients -j` dump (`hyprctl clients -j | mado-geometry.py --clients -
  --rules ~/.config/hypr/gkeep.conf`). It tells, per client matched by a `windowrule = size W H, match:class RX` line, AGREE, DIFFER,
  TILED (a tiled window never reads the rule) or BADSIZE, with `--selftest`. Before: the lane holds no tool that reads a window's reported
  size (`git ls-tree 62dd798 tools/` has no geometry tool; `grep -l clients tools/*.py` names only `mado-eventq.py`, an unrelated
  socket-client count). This is also the observation route the lane's gkeep rounds named and never had: on this host it answers
  `NO_MATCHING_CLIENT` today (no gkeep window is open).
  - **Predicate `PRED-C1-r42`:** the docstring of `quality/counters/c1-r42-geometry.py` (the code is the same sentence): 37 fixtures (10
    nonce-lattice generated, 27 fixed) scored byte-exactly against the judge's model inside a bubblewrap sandbox under `RLIMIT_NPROC = 1`, plus
    clauses a (tool at REV, absent at BASE), b (selftest `k == n`, `n >= 50`), b2 (selftest teeth: 6 nonce-chosen comparison flips, >= 4
    killed, the forced one in the summary function), b3 (selftest neutral to a trailing comment and to `ast.unparse`), g (stdlib `json os re
    stat sys` only, no exec/eval/compile/`__import__`/getattr-family, no `subprocess`, no `**` call unpacking, no judge strings). A run that
    reaches 3 timeouts is not run further.
  - **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r42-geometry.py --repo . --rev <rev>`
    (fresh nonce per run, printed on the final line, replayable with `--nonce`).
  - **Before** (base): `fixtures=0/37 tool=absent verdict=TARGET_MISSED`, exit 1 (`receipts/c1-before-base.txt`).
  - **Target:** `fixtures=37/37 tool=present verdict=TARGET_MET`, exit 0, at the data commit and at the tip. **Kill rule:** anything else at the
    data tip is a miss, reported as an honest stop; no narrowing.
- **C2 — coverage (sourced; assimilation of the gkeep-geometry theme of `merge/mado/`): `corpus/knowledge/hyprland-gkeep-geometry-r42.md`** — what
  determines the size of the host's gkeep window, end to end: the rule text on the host (`~/.config/hypr/gkeep.conf`), the rule match engine
  (`RE2::FullMatch`, anchored), the `size`/`float` effects, the floating algorithm that consumes the size, the target and window that store it,
  the animated variable behind `hyprctl clients -j` `size`, the client's own request (`set_default_size(420, 500)`, application id), and what the
  host census shows today (no gkeep client). The lane holds no rendered-geometry knowledge at base (`git grep -ciE 'set_default_size|GEOMETRIC_GOAL|
  RE2::FullMatch|rendered geometry' 62dd798 -- corpus/knowledge PROVINCE.md SKILL.md tools` finds none; gkeep appears in three knowledge
  files only as installer provenance). It is the successor of the staged gkeep chain entries (`gkeep-rendered-geometry-chain-r9` …
  `gkeep-size-to-real-size-r11`), re-grounded on rows opened this round (the §2b sourced claim; assimilation item §10).
  - **Predicate `PRED-C2-r42`:** the docstring of `quality/counters/c2-r42-gkeep-entry.py` (clauses a–i; the round-41 v2 counter plus word-bounded
    quotes, a computed `<receipt>:<line>` locator per cited id, and three own-work census lines recomputed from pinned host receipts).
  - **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r42-gkeep-entry.py --repo . --rev <rev>`
  - **Before:** `admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`receipts/c2-before-base.txt`). **Target:** `admitted=1/1 verdict=TARGET_MET`, exit 0.
    **Kill rule:** as C1.
- **Separability.** C1 touches `tools/mado-geometry.py` only (plus its receipts). C2 touches the entry, registry rows, the lesson `## Gate` and the README
  index; its census lines are recomputed by C2's own parsers from pinned receipts, so C2 never runs C1's tool and C1 reads no C2 file. Each is
  verifiable without the other having landed.

## Pre-wave fetches (PINS of C2; `fetch/`, `receipts/fetch-sha256.txt`)

Hyprland v0.56.2 (`efb50993780079460b0cbed1363e2166a2de1d9f`) raw files: `Hyprland-RegexMatchEngine.cpp` (src/desktop/rule/matchEngine), `Hyprland-WindowRuleApplicator.cpp`
(src/desktop/rule/windowRule), `Hyprland-DefaultFloatingAlgorithm.cpp` (src/layout/algorithm/floating/default), `Hyprland-Target.cpp`, `Hyprland-WindowTarget.cpp`
(src/layout/target), `Hyprland-GeometricMovableAnimated.cpp` (src/desktop/view/types), `Hyprland-HyprCtl.cpp` (src/debug). Own-work: `host-gkeep.conf` (byte copy of
`~/.config/hypr/gkeep.conf`, sha256 `3726e488…`), `host-clients-r42.json` (class/size/floating/mapped/address of `hyprctl clients -j`, window titles dropped),
`gkeep-ui-excerpt.py` (lines 446-495 of `~/Projects/gkeep/gkeep/ui.py` at gkeep `133b867`). Provisional facts the wave must re-open: the match engine is
`re2::RE2::FullMatch` with a `negative:` prefix; `static_.size` is an expression (`SExpressionVec2`), consumed in the floating branch; `hyprctl clients -j` `size` is
`w->size(GEOMETRIC_GOAL)` — the animation goal, not the current value (`Hyprland-HyprCtl.cpp:394-395,412-413`); the gkeep rule file declares float/center/size 420 500.

## Controls (committed receipts at this freeze)

- **C1:** `receipts/ctl-c1.txt` — `CTL_C1`: the reference (`c1/ctl-ref-tool.py.txt`, selftest 73/73) reaches TARGET_MET; the absent base tool, three do-nothing
  controls (constant output, stdin echo, selftest-only), five cheats (zero-test selftest, no-op selftest, an `exec` alias, a `subprocess` import, `getattr`) and 37
  single-defect mutants of the reference each score below MET. Three further mutants were found equivalent while building the freeze and are excluded **by name**
  in the runner and the receipt (`M03` loop bound never decides for a regular file; `M20` the `#` test was dead because the regex alphabet has no `#` — the contract
  sentence and the code were deleted; `M38` the empty regex is already refused by the `(.+)` capture). One mutant (`M26`, strict UTF-8 decode of the clients input)
  survived the first run and is now killed by a `badjson0` input holding an invalid byte inside a JSON string.
- **C2:** `receipts/ctl-c2.txt` — `CTL_C2`: control P (genuine pre-wave receipts, real quotes, the real census lines) is admitted under the real and the pin-patched
  counter; every other control (74 in total, forgeries under the real counter, clause mutants under a counter whose PINS also hold the fixture's receipts so a mutant
  is killed by its own clause) scores `0/1`, including the round-41 closure's two routed holes (mid-word quote ends B01/B02, wrong or missing locators B03–B07).
  Building the fixture found three defects in the first draft of the controls (quotes under 3 words, a held-id entry line with no locator, F6 mutating a directory
  component the counter does not read), fixed before this freeze.
- `receipts/freeze-counter-check.txt` — criterion 64: every counter, checker and control path this file names exists at the freeze.

## Residuals (declared)

- C1: a tool that **contains** a model of the contract is an implementation; clause g is a heuristic over names; the sandbox is detectable; Python `re` is not RE2 (the
  regex alphabet is restricted to where they agree, and `ExecRe2Fuzz` tests that restriction empirically); whether Hyprland applies a rule's size to a live window is a
  compositor fact the counter does not score (an oracle observation, if the wave obtains one, is reported, not scored).
- C2: the pins are the trust root; a real receipt can be cited for a claim it does not support at a true locator with a word-bounded quote (the non-author closure's
  job); a held id's receipt is not pinned; locators of HTML receipts are not checked.
- The wave `w2` attacks both predicates and the landed data; if it finds a hole the L1 reports it as an open defect of the predicate (no third registration after data).
  A hole found by `w1` **before any data commit** re-registers as v2 with a new freeze and the report names both predicates (the round-40/41 precedent).

## Assimilation and considerthese (item §10, rides inside §2b)

- Theme: the **gkeep geometry** theme of `/home/vgpnk/Projects/shokuknow/merge/mado/` (11 staged files `gkeep-*` and `glyph-and-geometry-r31`; the round-41 scout
  ranked it the best next theme). One successor entry is admitted; at least one staged file is refused with reason and flip condition; the id guard and the quarantine
  slice run in scratch (`assimilation/`) before any registry append.
- considerthese: `considerthese/2026-10-25.md` proposal 2 ("count dead attempts and dirty closures") — landed as a lesson and a QUALITY criterion grounded in this round's
  own start state (two untracked leftovers of round 41), with the command that counts them.
