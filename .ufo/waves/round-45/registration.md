# mado round 45 — registration (frozen BEFORE any round-45 data commit)

Base `0c89478af821a6424c9ac922eafe02e39630cf4f` (round-44 tip `8ac15c41` + its closure). Hyaku run 9, attempt 1 (`watchdog.log` shows one
launch, no earlier attempt). L1 `MadoR45` holds the §3 planner seat; bounded planning walks ride scout/connector items.
Round shape: two v1 waves — `w1` build + first falsifiers, `w2` falsify after data — 64-128 seats in total.

## Lowest axis

`receipts/axis-base.txt`: `MADO_AXIS: checked=3 mismatched=0` (navigation 61/61, calibration 71/71, operability 12/12): every published axis
ties at its maximum, so each is a lowest axis and the claims' after-states are their counters' lines (round-44 w1/CritClaimSizing F6/F9 practice).
The lane's axes are coverage + operability; both claims work them on a surface the lane did not hold.

## C1 — operability (capability acquisition): `tools/mado-monitors.py`

- **Surface moved:** a new read-only tool: the join of `monitor =` rules (one or more config files) with one `hyprctl monitors all -j` dump —
  which rule each output gets (one rule per selector, newest match wins, empty-selector fallback, `desc:` prefix), whether the running mode,
  position, scale (after Hyprland's 1/120 correction) and transform agree, DISABLED / UNRULED verdicts, NOT_COMPARED when `monitorv2` blocks or
  unmodelled lines could change which rule applies. Prior art at base, disclosed: `tools/mado-verify.sh:3518-3530` checks one hardcoded output
  (DP-1 3440x1440 within 0.5 Hz of 100) without reading any rule (`receipts/c2-ground-base.txt`, second part). The command that would show the
  surface unmoved: `git ls-tree <rev> -- tools/mado-monitors.py` (empty).
- **Predicate `PRED-C1-r45`:** the docstring of `quality/counters/c1-r45-monitors.py` (clauses a, s, f, r; 49 fixtures, seeded output names,
  default seed 45 so a bare run reproduces — round-44 closure D4).
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r45-monitors.py --repo . --rev <rev> --work <scratch>`
- **Before** (base): `fixtures=0/49 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED`, exit 1 (`receipts/c1-before-base.txt`).
  **Target:** `fixtures=49/49 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, exit 0, at the data commit and at the round tip.
- **Kill rule:** anything else at the data tip is a miss, reported as an honest stop; no narrowing and no re-registration after data. A hole `w1`
  finds before any data commit may re-register as v2 with a new freeze and new controls.
- **Controls** (`ctl/run-c1-controls.py` → `receipts/ctl-c1.txt`): REF = `l1-draft/mado-monitors.py` (the reference, selftest 33/33) must be MET;
  K00 base (tool absent), K01 `tools/mado-geometry.py` copied, K02 a stub printing OK and 33/33, and K03-K15 — the reference minus one semantic each
  (60 Hz default, `< 1` bound, scale correction, newest-match, erase-on-add, dump-not-live, v2, unknown-key drop, `desc:`, transform modifier,
  addreserved default, mirror, unsupported) — must all be MISSED.
- **Residuals (declared):** a tool holding a model of the contract is an implementation of it; the fixtures are the contract's cases, not
  Hyprland's runtime; the read-only clause catches PATH lookups only; whether the contract matches Hyprland beyond the pins is the non-author reading.

## C2 — coverage (sourced): `corpus/knowledge/hyprland-monitor-rule-r45.md`

- **Surface moved:** U5 output management, the "runtime state agreement" the round-14 entry left UNK
  (`corpus/knowledge/output-colour-boundaries-r14.md`): the monitor rule chain from the `monitor =` line to `hyprctl monitors all -j` —
  parser, handler grammar and key loop, rule storage and lookup, mode choice and closeness bound, scale correction, explicit positions,
  the JSON fields, the documented format and its `sdr_eotf` divergence. Ground at base: `receipts/c2-ground-base.txt` (claim grep exit 1; held
  neighbours disclosed: the round-3 point sample of DP-1's 99.997 Hz classed "EDID nominal quantization [INF]", the workspace-rule selector of
  `workspace-rules-r27.md`).
- **Sources:** nine pins fetched and opened 2026-10-26 (`fetch/`, sha256 in `receipts/fetch-sha256.txt`), new rows S302-S310 (registry tops at
  S301, 238 rows). Two locations repeat held rows under a different scope (S303 = S162's legacy ConfigManager.cpp URL, S307 = S158's
  HyprCtl.cpp URL): the census reports these as W04, not errors; the counter's clause e allows exactly that case.
- **Predicate `PRED-C2-r45`:** the docstring of `quality/counters/c2-r45-monitor-entry.py` (clauses a-j: the round-44 v2 a-g with T1-T4, a monitor
  census for h, i = location markers + pin coverage, j = seventeen surfaces with a 30-line locator width bound — round-44 closure D5).
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r45-monitor-entry.py --repo . --rev <rev>`
- **Before** (base): `admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`receipts/c2-before-base.txt`). **Target:** `admitted=1/1
  verdict=TARGET_MET`, exit 0, at the data commit and the tip. **Kill rule:** as C1.
- **Controls** (`ctl/run-c2-controls.py` → `receipts/ctl-c2.txt`): positive control P (`l1-draft/build-pos.py` on a clone of the freeze) admitted;
  C2-BASE, R14-COPY, SHELL, WIDE-RANGE, HIDDEN-LINE, FORGED-PIN, FALSE-URL, PROSE-CENSUS, ANCHOR-PAST-EOF all rejected. P is a control, not the
  data: the data commit is integrated from P and the w1 drafts and re-scored.
- **Residuals (declared):** claim-to-quote binding and registry prose cells are the non-author reading; clause j binds a locator and a keyword
  per surface, not the truth of the sentence; the census line is bookkeeping of pinned bytes.

## Separability

C1's counter reads only `tools/mado-monitors.py` at the revision; C2's reads only the entry, registry, lesson, README and the pins. Either can land
and verify without the other (w1 checks both directions).

## Not claims (routed work riding the round)

Round-44 closure D1 (tracked live window titles in `.ufo/waves/round-43/`), D2 (SCORECARD after-values), D3 (tip receipts at the final tip), D4
(seeded counter — done in C1's counter), D5 (C2 width bound — done; the round-44 counters are not reused), D6 (S290-S297 supersession), D7
(ConnCalibration errata); considerthese `2026-10-26.md` proposal 1 (a privacy check on committed receipts) as a QUALITY criterion plus a gate shown
able to fail at base. Assimilation: none planned (no `merge/mado/` theme on the monitor plane; w1 confirms). No exploratory claim.
