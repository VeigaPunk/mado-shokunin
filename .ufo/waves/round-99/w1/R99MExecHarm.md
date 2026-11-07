# R99MExecHarm -- w1 report: the C2 harm-watch gate, counter and frozen panel (round 99)

Seat `R99MExecHarm`, lane `/home/vgpnk/Projects/shokunin/mado-shokunin`,
predicate **PRED-C2-r99-v1**. Both instruments spawn child processes (the
gate spawns every panel leg via `Popen`+`start_new_session` with a
process-group kill on timeout; the counter spawns `git`, the gate and its
own fixture selftest) -- they are instruments, not modelled candidates.
Neither writes the lane; all leg scratch lives under per-run scratch
roots marked `.harm-watch-leg-r99` (gate) / `.c2-r99-harm-watch`
(counter), and foreign unmarked entries are refused with exit 2.

## Files written (owned paths only)

- `.ufo/waves/round-99/build/harm-watch.py` -- the gate draft.
  sha256 `6b83c78424d0a3520f3c48aff86ede49ac5f93be55bf0735fcacb48b521bcb1f`.
  **Superseded**: the L1 landed `quality/harm-watch.py`
  (sha256 `37a0544b160d9c5c5568fc45f9ed309f41b36fb093983313d72699423b4165b9`)
  with the same `--only` semantics (`PANEL_ONLY_UNKNOWN` for an unknown id
  instead of my `PANEL_SETUP only-unknown-id=`); the landed selftest is
  `checks=26 failed=0` (verified first-hand), mine was `checks=28 failed=0`.
- `.ufo/waves/round-99/build/c2-r99-harm-watch.py` -- the counter draft.
  sha256 `cf68b7917a4926a589bdd72f918326b1b2991fa8d389fb4ff9f15f96c26dac19`.
  **Superseded**: the L1 landed
  `quality/counters/c2-r99-harm-watch.py`
  (sha256 `ebde11a3033f01d48b85b592e29cc24f355572bd2d0ae85a23154b970e45115a`);
  landed selftest `checks=17 failed=0` (verified first-hand), mine was
  `checks=17 failed=0`.
- `.ufo/waves/round-99/controls/harm-panel-r99.json` -- the frozen panel,
  landed sha256 `160763ce7aa447016bad8e5b2c5a7c25f8866b1e8724d8eb0b75d8abb1dae39a`
  (28 legs, `expect_legs` 28, `timeout_s` 600, 8 rounds). My last working
  copy (with per-leg wall-time notes on the four slow legs) hashed
  `baf7659b3a010f4bae6cac164e753976d4897cb5214a8013343e0c38c23e371a`; the
  landed panel differs only in those four `note` strings -- every
  id/argv/expect_rc/expect_marker is identical (verified leg-wise against
  `harm-planted/clean.json`: 28/28 semantic rows equal).
- `.ufo/waves/round-99/controls/harm-planted/{clean,dropped-leg,wrong-expect,wrong-marker,extra-leg}.json`
  -- the five planted controls, regenerated from the timeout-600 panel:
  clean `254719f9e5b1921503f68ec0c5a17632956035d91bcee6cceb23a5caaa01d1e8`,
  dropped-leg `9e23aa118ed87aba61ed3d96b7be08237f14e85fdeff01f747038cc43a98b309`,
  wrong-expect `2d016a68b25136228bea98d7f13929eb08ad4a815f1b611e7b0f1018d9cba2e6`,
  wrong-marker `ef9865d0c0465579850e897cc8b276d5088d35e4aa950881fccf93acb8eec7fa`,
  extra-leg `970ef76b7e9487e1f260d21269fdf28f67ce9be646414908aefd5e7de4134829`.
  These are the bytes the L1 landed unchanged.
- `.ufo/waves/round-99/w1/R99MExecHarm.md` -- this report.

All committed artifacts are ASCII-only and stdlib-only (verified by byte
scan and import audit).

## Gate design (`harm-watch.py`)

- Census first, always over the FULL panel: `PANEL_LEG_UNKNOWN` (id no
  round declares), `PANEL_DUPLICATE`, `PANEL_LEG_MISSING` (declared id
  absent), `PANEL_ROUND_MISSING`, and `PANEL_LEG_COUNT` under the
  net-of-findings rule (fires only when the row-count delta is not fully
  explained by unknown+duplicate surplus - missing; the rule is recorded
  in the panel's `census_rule` key and was adopted into the declaration).
  Any finding exits 2 before a single leg runs.
- `REV`/`SCRATCH` whole-element substitution in each leg argv; per-leg
  scratch dir `<scratch-root>/<id>` with marker file; a leftover marked
  dir is cleared and reused, any other non-empty entry refuses (exit 2).
- Timeout: `Popen` with `start_new_session`, kill of the child's process
  group on expiry (the pgid-of-the-child fix from the R99MMutC2 finding);
  `--timeout` overrides the panel's `timeout_s`.
- `--only ID` (repeatable): census over the full panel, then only the
  named legs; unknown id is a setup error. `--json` emits the human lines
  plus one JSON object as the last stdout line.
- `--selftest`: fixture panels + stub legs in a private temp dir.

## Counter design (`c2-r99-harm-watch.py`)

- Pins: gate sha256 and panel sha256 must match the pinned values (setup
  error otherwise); separability: `SETUP_ERROR quality/harm-watch.py
  absent at <rev>` when the gate is missing at `--rev`, and
  `present at base-rev` (claim void) when it exists at `--base-rev`.
- Verdict conjuncts (emitted in `missed=` on TARGET_MISSED):
  `panel_legs_eq_declared`, `panel_legs_ge_20`, `legs_run_eq_panel_legs`,
  `mismatches_zero`, `planted_dropped_leg`, `planted_wrong_expect`,
  `planted_wrong_marker`, `marker_blind_flagged`, `stub_flagged`,
  `selftest_ge_12_failed_0`.
- Planted controls after the L1 cost fix: `clean.json` reuses the main
  run's verdict; `dropped-leg`/`extra-leg` are census-only (exit 2 before
  any leg); `wrong-expect`/`wrong-marker` and the marker-blind copy are
  `--only`-scoped to the single flipped leg (`r96c2_selftest_kills`).
- Marker-blind control: the counter patches the gate's marker line
  (`marker_ok = (not marker) or ...` -> `marker_ok = True`) and requires
  the neutralised copy to ACCEPT the wrong-marker plant (exit 0) where
  the real gate rejects it (exit 1); if the pattern is absent from the
  gate bytes the counter exits 2 rather than guessing.
- Stub control: an always-OK fake gate over the dropped-leg plant must
  disagree with the real gate's verdict.
- `--selftest`: fixture git repos replay pins, separability, all five
  plants, stub, blind, scratch reuse, red panel; `C2_R99_SELFTEST_DEPTH`
  prevents recursion.

## Frozen panel and measurement

28 legs across 8 rounds (base selftest/gate legs + r90-r97 counting
commands). Every `expect_rc`/`expect_marker` was frozen from **three
agreeing measurements** at rev `2cbaa141f42df9dfeee4d207cae6558a4dd59863`
in a clean clone (`pass1`, `pass2`, `pass3`; pass2 and pass3 verified
byte-identical on all 28 legs' rc/marker/verdict). Pass 3 ran the landed
panel shape (`timeout_s` 600): `HARM_WATCH: legs=28 ok=28 mismatch=0`,
wall span ~1270 s.

Per-leg evidence (pass 3; identical in pass 2):

| leg | round | expect_rc | measured rc | marker | verdict |
|---|---|---|---|---|---|
| verify_selftest | base | 0 | 0 | ok | ok |
| verify_file_plane | base | 0 | 0 | ok | ok |
| index | base | 0 | 0 | ok | ok |
| ledger | base | 0 | 0 | ok | ok |
| mako_selftest | base | 0 | 0 | ok | ok |
| portals_selftest | base | 0 | 0 | ok | ok |
| mime_selftest | base | 0 | 0 | ok | ok |
| xdgmime_selftest | base | 0 | 0 | ok | ok |
| mimeglob_selftest | base | 0 | 0 | ok | ok |
| mimesniff_selftest | base | 0 | 0 | ok | ok |
| seat_reports_selftest | base | 0 | 0 | ok | ok |
| receipt_presence_selftest | base | 0 | 0 | ok | ok |
| gate_selftest | base | 0 | 0 | ok | ok |
| gate_seat_reports | base | 0 | 0 | ok | ok |
| gate_mimeglob | base | 0 | 0 | ok | ok |
| gate_portals | base | 0 | 0 | ok | ok |
| r90c2_receipt_presence | r90 | 0 | 0 | ok | ok |
| r92_gate_defects | r92 | 0 | 0 | ok | ok |
| r90c1_portal_routing | r90 | 2 | 2 | ok | ok |
| r94c1_mimeglob | r94 | 0 | 0 | ok | ok |
| r94c2_selftest_kills | r94 | 0 | 0 | ok | ok |
| r93c2_selftest_strength | r93 | 0 | 0 | ok | ok |
| r95c1_mimesniff | r95 | 2 | 2 | ok | ok |
| r95c2_selftest_kills | r95 | 2 | 2 | ok | ok |
| r96c1_magictext | r96 | 2 | 2 | ok | ok |
| r96c2_selftest_kills | r96 | 0 | 0 | ok | ok |
| r97c1_filetype | r97 | 0 | 0 | ok | ok |
| r97c2_counter_selftest | r97 | 0 | 0 | ok | ok |

Measured wall times (pass 3; pass 2 in parentheses): r92_gate_defects
322 s (309), r97c1_filetype 381 s (281), r93c2_selftest_strength 180 s
(124), r97c2_counter_selftest 138 s (79), r94c1_mimeglob 106 s (54),
r94c2_selftest_kills 59 s (21), r96c2_selftest_kills 54 s (30),
r90c2_receipt_presence 20 s (20); every other leg <= 3 s. The four >60 s
legs the L1 named are exactly the four that timed out at `--timeout 60`;
`timeout_s` 600 gives ~36% headroom over the worst observed (381 s).

## rc deltas vs the r98 receipts (the two the L1 asked for)

1. **ledger**: r98-base receipt rc=1
   (`.ufo/waves/round-98/receipts/harm-base-r98.txt:4`, note: "the four
   ledger rows were still uncommitted at this tip") -> tip rc=0
   (`harm-final-r98.txt:4` "the ledger rows are committed at this tip";
   confirmed rc=0 in all three r99 passes). Not a new harm: an
   uncommitted-rows artifact of the base measurement.
2. **r97c2_counter_selftest**: r98-base receipt rc=1
   (`harm-base-r98.txt:28`, note: "the leg's argv carries the literal
   placeholder `SKILL-AT-MEASURED-REV` ... the shell fails before the
   counter runs") -> tip rc=0. The r99 panel fills both placeholders with
   the `git show 2cbaa141:` hashes of SKILL.md and
   quality/tool-ledger.md and pins `--rev` literally to 2cbaa141 (the
   counter validates the pins against its own `--rev`); this is the r98
   spot-check defect-5 / D5 fix, verified rc=0 in three passes.

All other 26 legs match the r98 receipts exactly.

## Declared-state legs (named, not silently frozen)

Four legs freeze `expect_rc=2` as the **declared** state, not a green
outcome: `r90c1_portal_routing` (declared SETUP_ERROR since round 93),
`r95c1_mimesniff` and `r95c2_selftest_kills` (the r95 declaration has no
parseable counting-command block for `run-decl-counter`), `r96c1_magictext`
(the r96 counter's known stale mutant pin, r96 D5). `r97c1_filetype` is
the leg the r98 final 26-leg run dropped (r98 spot-check defect 5); this
panel replays it and it measures rc=0. The r98 counters were excluded per
the L1's measured harm-r98c1/c2-at-r99 receipts (c2 fails SETUP_ERROR on
planted drift).

## Deviations and decisions

- Census rule is net-of-findings (see Gate design); recorded in the panel
  and adopted into the declaration by the L1.
- `r97c2` registry/ledger pins are literal `git show 2cbaa141:` hashes;
  `--rev` pinned to the same rev.
- Measurement ran in a clean clone at 2cbaa141 to stay immune to the
  L1's in-flight working-tree edits; legs that read the working tree
  (ledger/index/gate legs) therefore measure the freeze tip.
- L1 landing: the L1 patched the landed copies (`quality/harm-watch.py`,
  `quality/counters/c2-r99-harm-watch.py`, the panel) with equivalent
  `--only`/scoping semantics and re-froze `timeout_s` 600; my `build/`
  drafts remain as the wave artifacts and were not rewritten after the
  handover. Landed-vs-draft differences are confined to the `--only`
  unknown-id finding name (`PANEL_ONLY_UNKNOWN` vs my
  `PANEL_SETUP only-unknown-id=`), the selftest check counts (26 vs 28),
  and four panel `note` strings (my wall-time annotations; `clean.json`
  carries them, the landed panel does not -- notes are not part of any
  check).

## Risks

- Slow-leg wall variance is real (r97c1: 281 s pass 2 -> 381 s pass 3).
  `timeout_s` 600 holds today; a heavily loaded host could push a leg
  toward the bound, in which case the leg reads rc=TIMEOUT mismatch --
  loud, never silent.
- Legs that read the working tree rather than `git show REV:` will
  reflect whatever tip they run at; the panel is frozen for 2cbaa141 and
  any future round that changes ledger rows or gate files must re-freeze
  or accept the drift as a measured mismatch.
- The counter's planted `clean.json` reuse assumes clean == panel
  semantics; it holds because the diff functions compare only
  id/expect_rc/expect_marker, and the planted files were regenerated from
  the same panel bytes.

## Tools installed

None. (No tooling changes were needed; pacman was paused host-wide
anyway.)

## Verification exercised (first-hand)

- `python3 -I quality/harm-watch.py --selftest` -> `checks=26 failed=0`.
- `python3 -I quality/counters/c2-r99-harm-watch.py --selftest` ->
  `checks=17 failed=0`.
- Draft selftests before landing: gate `checks=28 failed=0`, counter
  `checks=17 failed=0`.
- Three full-panel passes at 2cbaa141: `legs=28 ok=28 mismatch=0` each;
  pass 2 and pass 3 byte-identical on every leg line.
- `--only` smoke test on the real panel: census clean, exactly the named
  legs ran, summary counts the run legs.
- Planted census controls measured: dropped-leg -> exactly
  `PANEL PANEL_LEG_MISSING id=r97c1_filetype round=r97` rc 2; extra-leg ->
  exactly `PANEL PANEL_LEG_UNKNOWN id=gate_xdgmime` rc 2.
- ASCII scan: 0 non-ASCII lines in all eight committed artifacts; import
  audit: stdlib only.
