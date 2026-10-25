# mado round 40 — registration (frozen before any round-40 data)

Base: `9fc511ddce708327377161202f358ce37dc266ba` (lane tip at round start; attempt 1; the watchdog
shows no `lane-dead-no-report mado round=40` before this launch). This file, the two counters,
the control harnesses and their receipts, the round-start receipts and the native-capture receipt
land in ONE freeze commit. Any later change to a counter, a control, the capture or a declared
target is a new predicate and the claim it belongs to then fails as declared. The delivered tool,
the entry, the registry rows and every Gate line are data and land after the freeze.

## Lowest-axis rule

`python3 -I quality/check-axis-scores.py --repo . --rev master` at base prints
`navigation published=56/56`, `calibration published=51/51`, `operability published=12/12`,
`MADO_AXIS: checked=3 mismatched=0` (`receipts/axis-base.txt`) — every published axis ties at
its maximum, so each is a lowest axis; C1 works operability, C2 works coverage. The stagnation
nudge does not apply: a capability row entered in round 39, inside the window N=3.

## Routed defects being worked (round-39 non-author closure)

- **D2 (over-label):** `corpus/lessons/round-39.md` labels the quarantined S224 "refused
  (fabrication class)"; the seat evidence says a rotated volatile timestamp. Corrected by an
  appended note in `corpus/lessons/round-40.md` (append-only).
- **D1 (predicate variance):** this registration's counting commands are run at the freeze
  commit (criterion 64 command) so no ruling is needed: each counter path exists at the freeze.
- **D3 (dead seats):** seat reports are written before returning (every wave item writes its
  report file first).
- Round-39 planned item 1: a live `hyprctl getoption` dump merged into the option table (C1).

## C1 — operability (capability acquisition): the option table merges the running compositor

- **Deliverable:** `tools/mado-options.py` gains `--live` (one `hyprctl getoption -j KEY` per
  declared key through the compositor's own read verb), `--hyprctl PATH` and `--probe KEY`
  (extra live keys with no declarer → `live-default`). Native replies are compared in their native
  forms (`int`, `float`, `str`, `custom`), converted per hyprlang v0.6.8 `configStringToInt`,
  Hyprland v0.56.2 gradient/gap/font-weight handlers; a gradient redeclared without an angle token
  inherits the previous declarer's angle. Exit 5 on a compositor failure naming the key; exit 2
  for a hostile probe key (no program run); standard library only; no write.
- **Predicate `PRED-C1-r40-v1`:** the docstring of `quality/counters/c1-r40-live.py` — the code is
  the same sentence. It generates 8 trees seeded by sha256(REV:i) (15 options each: every type,
  every label, host spellings, one gradient redeclared without an angle), a probe tree, two
  failure trees, a missing-program tree and a hostile-probe tree, drives a stub `hyprctl`
  that emits only the four native forms and `no such option`, and checks the labels, the exact
  argv and that the config root is unchanged.
- **Counting command:**
  `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r40-live.py --repo . --rev <rev>`
- **Before** (measured at base): `fixtures=0/13 tool=present verdict=TARGET_MISSED`, exit 1
  (`receipts/c1-before-base.txt`; base has no `--live`).
- **Target:** `fixtures=13/13 tool=present verdict=TARGET_MET`, exit 0, at the data commit and the
  tip. Clause b requires the delivered `--selftest` at `k == n >= 79` (base: 71).
- **Kill rule:** anything other than TARGET_MET at the data tip is a miss, reported as an honest
  stop; no narrowing.
- **Do-nothing control:** the unmodified base tool scores `0/13` (`receipts/ctl-c1.txt`
  `BASE-tool`). The reachability control (`c1/ctl-ref-tool.py.txt`, a throwaway reference, never
  delivered) scores `13/13` on the fixtures but `TARGET_MISSED` overall (clause b: its selftest
  is the base's 71 and k clause needs the capture), so the fixtures are reachable and the target is not
  met by the reference. 16 mutants (one defect each: all-agree, raw compare, bool exactness,
  angle ignored, 3-value gap, config-only as mismatch, extra argv, `set` ignored, shadow ignored,
  hostile probe accepted, failure swallowed, write to the config root, int normalisation dropped,
  live field dropped, angle inheritance absent, probe default masked) each score `<13`:
  `CTL_C1: controls=18 correct=18/18` (`receipts/ctl-c1.txt`, harness `ctl/run-c1-controls.py`).
- **Residual (declared):** a tool that hardcodes the reference model's conversion tables for this
  generator's value space passes the fixtures; the live host receipt (`70/70` under the reference
  model, `w1`) is the out-of-distribution check and is reported, not scored.

## C2 — coverage (sourced): the getoption native-forms ground is admitted

- **Deliverable:** `corpus/knowledge/hyprctl-getoption-native-forms-r40.md` — what the compositor
  answers to `getoption -j` (the four native forms and `no such option`), how a declared string
  is converted per form (hyprlang colour/bool/hex forms; gradient colours + angle; CSS gap
  expansion; font-weight names), the angle-inheritance rule (observed on the host: the theme's
  single-colour `col.active_border` reads `ffe68e0d 45deg` because the defaults tree declared a
  45deg gradient first), and the host census (62 agreement / 8 agreement*, 0 mismatch under the
  native model — the number the receipt states). Cited rows: held S162 (ConfigManager.cpp
  gradient handler, re-opened) and S173 (hyprlang config.cpp `configStringToInt`, re-opened),
  plus at least two new rows opened this round (Hyprland `ComplexDataTypes.hpp` at the pinned
  commit; an own-work row for the live census receipt).
- **Predicate `PRED-C2-r40-v1`:** docstring of `quality/counters/c2-r40-forms-entry.py`
  (clauses a–h; clause h binds the own-work receipt to the committed tool sha256 and to two
  count lines the entry repeats verbatim).
- **Counting command:**
  `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r40-forms-entry.py --repo . --rev <rev>`
- **Before:** at base the entry does not exist → `admitted=0/1 verdict=TARGET_MISSED`, exit 1
  (`receipts/c2-before-base.txt`).
- **Target:** `admitted=1/1 verdict=TARGET_MET`, exit 0.
- **Kill rule:** as C1.
- **Controls:** 20 mutants of an admitted fixture (missing entry, missing rows, wrong sha, absent
  quote, 26-word quote, missing index row, one new id, held row rewritten, duplicate location,
  entry line without the quote, wrong date, staged ids as-is, status candidate, receipt outside
  fetch, no own-work row, used-by missing, stale tool sha, disagreeing counts, label sum wrong,
  count lines absent from the entry) each score `0/1`; the fabricated self-consistent control P
  scores `1/1` (the declared residual): `CTL_C2: controls=21 correct=21/21`
  (`receipts/ctl-c2.txt`, harness `ctl/run-c2-controls.py`, fixture repos created with
  `mktemp -d` and `git -C "$D"`, the toplevel verified equal to `$D` before the first commit).
- **Residual (declared):** a fabricated self-consistent set passes; committed bytes cannot prove
  the receipt is what the location served or what the compositor answered.
- **Separability:** C1 is judged by the tool and a stub compositor; C2 by entry/registry/receipt
  bytes and the committed tool's sha. C2's counter passes a dummy tool (control P) without C1's
  verdict, and C1 shares no file with C2.

## Frontier step, assimilation, considerthese

- Census command (round start, `receipts/census-before.txt`): exit 0, seven W04 + one W01.
- **Assimilation (rides inside §2b; no claim slot):** package `merge/mado/` (read-only) theme
  "the host's bar producers" — `host-bar-producers-r28.md` and `host-producer-outputs-r29.md`
  (round-3/4 entries). Held: `waybar-walker-semantics.md` already maps the 19 modules and names
  the producer scripts (`grep` for `indicators/idle.sh`, `screen-recording.sh`, `weather.sh`,
  `omarchy-update-available` hits it); not held: the gkeep/ai-usage producers' current-output
  decidability, the upstream-vs-host config byte difference (6354 B host, 5114 B upstream is held).
  Each entry is scope-checked and gated in the lesson (≥1 admit and ≥1 reject recorded); quarantine
  slice re-derived; id-collision guard run in scratch. No staged row is appended as-is.
- **considerthese:** `2026-10-25.md` proposal 2 (count dead attempts and dirty closures from the
  watchdog digests) mined as a lesson table; round-39 planned item 1 is C1.

## Harm watch (every claim)

- `bash tools/mado-verify.sh --selftest` stays `MADO_SELFTEST: 460/460` (`receipts/selftest-base.txt`).
- `python3 -I tools/mado-options.py --selftest` stays all-pass with n ≥ 79 (C1 clause b).
- `quality/check-index.py` complete; only the C2 entry adds a row (baseline 56/56).
- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` exit 0 at round end.
- `python3 -I quality/check-axis-scores.py` `mismatched=0`.
- No config tree, compositor state, service, sibling lane or fleet-repo path other than the
  report is written; `hyprctl getoption -j` is the only compositor verb run, read-only.
