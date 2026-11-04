# R77Mutant — independent mutation testing of the round-77 bar-footprint join and the C2 probe table

Seat: R77Mutant (mutation-tester, wave 1, round mado 77). Scope: (1) thirteen new single-anchor
mutants of `tools/mado-barfoot.py`, all outside the five frozen ones, scored on the 15 frozen C1
cases from my own copies of the frozen bytes; (2) survivor classification (model gap vs equivalent
mutant); (3) C2's twelve expectations attacked for weakness. Findings only: no production byte
touched, nothing committed, nothing rewritten (L1 integrates).

## Method and sanity

- Frozen bytes copied to scratch and hash-verified before use (all match the declaration and the
  copied baseline receipt in `evidence/control-baseline-r77.txt`): tool `409e78a4…`, C1 counter
  `56620959…`, C2 counter `056a9152…`, C1 cases `7d6e2b1a…`, C2 cases `597b2302…`.
- Harness is counter-faithful: `case_files` / `expected_ok` / `parse_result` / child run-env are
  replicated verbatim from `quality/counters/c1-r77-barfoot.py`; every mutant is a single-anchor
  replace asserted to occur exactly once (the counter's own `apply_mutation` discipline).
- Sanity: the pristine tool scores 15/15 under the harness; the naive live-echo control reproduces
  the frozen `base_correct=8/15`; the frozen tool's sha256 is identical before and after the whole
  run (`409e78a4aef2f46f…90cb15`, pre == post).
- Every verdict below is a measured run, not a prediction. One prediction was falsified by the run
  (`bottom-extent-form`, see below) — recorded as measured.

## C1 mutation results — mutant | killed/survived | case | class

| mutant | killed/survived | killing case(s) | class |
|---|---|---|---|
| bottom-extent-form | killed (14/15) | bottom-bar | edge-extent geometry |
| bottom-extent-altform | SURVIVED (15/15) | — | equivalent mutant (algebraic identity) |
| left-extent-flip | killed (14/15) | left-vertical | edge-extent geometry |
| right-extent-flip | SURVIVED (15/15) | — | coverage gap: no right-edge case in the set |
| output-exclusion-dropped | killed (14/15) | output-excluded | output model |
| namespace-default-rename | killed (4/15) | host-top +10 more | namespace default |
| vertical-hw-swap | killed (14/15) | left-vertical | height/width swap on vertical bars |
| reserved-reversed-read | killed (9/15) | host-top +5 more | reserved index order (read site) |
| margin-guard-any-to-all | killed (14/15) | per-side-margin | per-side margin precedence guard |
| zero-height-threshold | killed (5/15) | host-top +9 more | zero-size branch |
| gt-flattened | killed (14/15) | drift-box | GT admissibility |
| level-lookup-pinned | SURVIVED (15/15) | — | coverage gap: declared-level lookup unpinned |
| output-empty-include-refused | SURVIVED (15/15) | — | coverage gap: exclusion-only output spec |

13 mutants (≥8 required), 10 killed, 3 survivors, 1 of them a proven equivalent. Mutant outputs
and the full machine-readable manifest: `evidence/mutation-manifest.json` (same dir as this file).

Anchors — every mutant is exactly one anchored replacement (old → new), each asserted to occur
exactly once in the frozen source:

1. `bottom-extent-form`: `        return mon_h - box["y"]` → `        return box["y"] + box["h"]`
2. `bottom-extent-altform`: `        return mon_h - box["y"]` → `        return box["h"] + bar["margins"]["bottom"]`
3. `left-extent-flip`: `        return box["x"] + box["w"]` → `        return mon_w - box["x"]`
4. `right-extent-flip`: `    return mon_w - box["x"]` → `    return box["x"] + box["w"]`
5. `output-exclusion-dropped`: `    if monitor in exclude:` → `    if False:`
6. `namespace-default-rename`: `else "waybar"` → `else "wbar"`
7. `vertical-hw-swap`: `        if bar["height"] > 1:` → `        if bar["width"] > 1:`
8. `reserved-reversed-read`: `    band = mon["reserved"][RESERVED_INDEX[edge]]` → `    band = mon["reserved"][3 - RESERVED_INDEX[edge]]`
9. `margin-guard-any-to-all`: `    if any(isinstance(config.get(k), int) and not isinstance(config.get(k), bool) for k in per_side):` → same with `all(`
10. `zero-height-threshold`: `        if bar["height"] > 0:` → `        if bar["height"] > 1000:`
11. `gt-flattened`: `        reserved_verdict = "GT"` → `        reserved_verdict = "EQ"`
12. `level-lookup-pinned`: `    entries = levels.get(str(level))` → `    entries = levels.get("2")`
13. `output-empty-include-refused`: `    if not include:\n        return True` → `    if not include:\n        return False`

Note on axes: all nine suggested mutation axes are covered — bottom/left/right extents (1–4),
output exclusion (5, 13), namespace default (6), height/width swap on vertical bars (7), reserved
index order (8 — mutated at the read site; the frozen `reserved-wrong-edge` mutates the
`RESERVED_INDEX` table, so anchors and mechanisms are distinct), per-side margin precedence (9 —
mutates the guard; the frozen `per-side-margin-dropped` drops the values inside the branch), and
the zero-size branch (10). `gt-flattened` (11) is a bonus on the GT-admissibility rule.

## Survivor analyses

**bottom-extent-altform — equivalent mutant (proven).** For every bottom-bar path in
`declared_box` the identity `mon_h - box["y"] == box["h"] + bar["margins"]["bottom"]` holds:
height>0 branch `y = mon_h - h - m_bottom` gives `mon_h - y = h + m_bottom`; zero-height branch
`h = mon_h - m_t - m_b, y = m_top` gives `mon_h - y = mon_h - m_top = h + m_bottom`. The identity
is unconditional in the margins, so even the `expected=%d` row text is identical — measured 15/15
with byte-identical published fields. No discriminating case exists for this mutant at all; it is
genuinely equivalent, not a set weakness. (Contrast: `bottom-extent-form` was killed by
bottom-bar — for a bottom-flush bar `mon_h - y = h` but `y + h = mon_h`; my initial equivalence
guess for that mutant was wrong and the run corrected it.)

**right-extent-flip — real model-coverage gap (discriminating case named).** The frozen set has
no right-anchored bar, so the right extent expression is untested. Discriminating case: 1920x1080
monitor, config `position=right, width=40`, live level-2 waybar box `x=1880,y=0,w=40,h=1080`,
`reserved=[0,0,40,0]`. Pristine: extent `mon_w - x = 40` → EQ/CLEAN. Mutant: extent
`x + w = 1920` → band 40 < 1920 → DIFFER/rc1. One added frozen case kills it; the C1 predicate
would remain true with the set extended.

**level-lookup-pinned — real model-coverage gap (discriminating case named).** The mutant reads
level `"2"` regardless of the declared level. `declared-level-miss` does not catch it because its
distractor level is empty (`levels["2"] == []`); every other case declares `layer=top`. The frozen
`level-top-swap` kill does not cover this either (it changes the declared level mapping, not the
lookup key). Discriminating case: config `layer=bottom` with the live waybar entry ONLY at level
2 (`levels["1"]` empty) → pristine NO_LAYER/rc3, mutant finds it at `"2"` → CLEAN/rc0. One added
case kills it.

**output-empty-include-refused — real model-coverage gap (discriminating case named).** The line
`if not include: return True` encodes "an exclusion-only output spec matches every non-excluded
monitor" (the correct waybar semantics for `output: ["!M2"]`); the mutant inverts it to NO_BAR.
No frozen case reaches that line: no-output configs return at `spec is None`, and
output-excluded's monitor is excluded before the include check. Discriminating case: config
`output="!M2"` joined on monitor M1 → pristine CLEAN/EQ/rc0, mutant NOT_ON_MONITOR/NO_BAR/rc3.
One added case kills it.

Suggested frozen-set additions (three cases) that would raise the kill score to 12/13 with the
equivalent mutant remaining dead by proof, not by test: `right-vertical` (w=40, reserved
[0,0,40,0]), `bottom-level-live-distractor` (layer=bottom, waybar live only at level 2),
`exclusion-only-other-monitor` (output="!M2" on M1).

## C2 attack — probe | weakness | stronger expectation

Matcher-class finding first, then per-probe rows. All demonstrations ran against the frozen
counter's own `matched()` (unit calls, no host probes) or against the committed fetch captures
(sha-verified against the copied pre-wave receipt: layers `46eb2481…`, monitors `e732af34…`).

| probe | weakness (wrong underlying state that still passes) | stronger read-only expectation |
|---|---|---|
| all 12 rows (matcher) | `matched()` never consults rc or stderr. Proven on the frozen matcher: `empty` returns True for rc=127 with stderr "command not found"; `exact "192"` returns True with rc=1 | require `rc == 0` before kind matching (demonstrated variant refuses both cases); counter-level: gate the whole run on a liveness probe (e.g. version rc==0), else score the run as setup-error rather than matched |
| configerrors (`empty`) | canonical too-weak row: a broken or absent session (no HYPRLAND_INSTANCE_SIGNATURE, missing binary, failed pipeline) leaves stdout empty → still passes | `rc==0 AND stdout==""`; empty stdout alone must never be a pass |
| version (`contains "Hyprland 0.56.2"`) | any build string carrying the prefix passes — dirty tree, rebuild, different commit | pin the round's tree: regex `^Hyprland 0\.56\.2 built from branch v0\.56\.2 at commit efb5099[0-9a-f]{28} clean` (the live line in `evidence/pre-wave-evidence-r77.txt` carries `efb50993780079460b0cbed1363e2166a2de1d9f clean`) |
| layers-namespaces (`wallpaper,waybar`) | geometry- and level-blind: the jq walks all levels of all monitors and keeps only namespaces — a waybar demoted to level 0/3, duplicated, or shrunk/moved (the exact drift C1 measures) still prints the same list | bind namespace→level→box→reserved in one row: expect exactly `0,0,3440,26 [0,26,0,0]` from `levels["DP-1"].levels["2"][ns=waybar]` plus `.[0].reserved`, and assert `reserved_top == y+h`. Demonstrated green on the committed captures: box `0,0,3440,26`, reserved `[0,26,0,0]`, band 26 == extent 26 |
| waybar-process (`pgrep -x waybar | head -1`, regex `^[0-9]+$`) | shape-only by declared design: any pid passes; proven frozen matcher accepts pid 999999; the pid is uncorrelated with the layer surface | same-instant join: `pgrep -x waybar` pid == `layers["DP-1"].levels["2"][ns=waybar].pid` (both read-only, one session) |
| omarchy-version (anchor reuses "`omarchy theme current`") | the shared table cell satisfies the anchor without naming the version half; a table edit breaking only the version wording stays unnoticed | stronger anchor "`omarchy version`" — verified present as a substring of the committed SKILL.md cell; zero-cost swap in the control set |
| monitors rows (`.[0]`) | enumeration-order assumption: DP-1 not first → hard fail (loud, not silent — a brittleness note, not a silent weakness) | select by name: `.[] | select(.name=="DP-1")` to decouple from reply order |

Not weak, for the record: monitors-size, monitors-reserved, gaps-out, kb-layout, binds-count,
mako-mode, omarchy-theme carry exact frozen values — any wrong underlying state fails them loudly;
their only shared exposure is the matcher-class rc-blindness above.

## Restoration and cleanup evidence

- Frozen instrument bytes: unchanged across the entire run — sha256 before == after ==
  `409e78a4aef2f46f80508820f3a58ae7023c1b614f5836d52bf2e6a05490cb15`. All mutation happened in
  scratch copies (`mutants/*.py`), never in the lane tree.
- No git/jj write command run anywhere; no host state touched (no hyprctl/makoctl/busctl/systemctl
  calls at all — every demonstration is unit-level or against committed bytes); no config tree,
  service, sibling file or package transaction touched. No tooling installed or upgraded (none
  needed).
- Cited receipts copied into this dir before scratch deletion:
  `evidence/control-baseline-r77.txt` (sha256 `60759bd0…`), `evidence/pre-wave-evidence-r77.txt`
  (sha256 `3fee114e…`).
- Scratch `/fast/scratch/hyaku/mado-r77/R77Mutant/` deleted after the manifest and this report
  were written.

Report: .ufo/waves/round-77/w1/R77Mutant.md
