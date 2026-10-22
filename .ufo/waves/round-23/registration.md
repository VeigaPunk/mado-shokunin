# Mado round 23 — repair-first recovery registration (before any production edit)

Base: lane branch tip `e33ea30461f6e9bbeee40beef19770a953f7a105` (classifier `tools/mado-tripwire.py`
SHA256 `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`). Dispatched
2026-10-22T10:43:09Z under the operator recovery ruling (goal file, D11). This file, the frozen
repair set under `repair/` and the before receipts land in one commit before any change to
`tools/`. That order answers the round-22 closure's routed defect 2 (normalized expectations were
committed after implementation).

## Routed harms, before values, re-measure commands

| Harm | Source | Before value at base | Re-measure command |
|---|---|---|---|
| H1 r21 binding failures F1–F5 | MANIFEST rounds[400] (operability harmed) | already passing at base inside the round-22 primary population: 57/57 | `python3 -I .ufo/waves/round-22/oracle/measure.py --tool tools/mado-tripwire.py` |
| H2 r21 precision drop 172/175 → 166/175 | rounds[400] rechecks | 166/175 (P66/66 S17/17 W21/22 H47/52 L15/18) | `python3 -I .ufo/waves/round-20/tw-precision.py REV` |
| H3 r22 supplemental discovery red | rounds[426] C1 | 2/4 (ReturnedGlobalCallableShadow foreign lead; ForwardExistingClosure unparsed 1) | `python3 -I .ufo/waves/round-22/residual-truth/measure.py --tool tools/mado-tripwire.py` |
| H4 r22 caller-frame leak | rounds[426] C1 closure probe, notes defect 3 | false observed foreign argv when a forwarder invokes a module callback | case `ForwarderInvokesCallback` in the repair set below |
| H5 callback-store recall (v3 withdrawal reason) | rounds[426] outside_spotcheck[3] | lead kept at base | cases `CallbackStoredInDict`, `CallbackStoredOnAttribute` below |

H2 is not claimed as repaired this round. Of its nine disagreements, five are strict VCS
index-write readings (`git commit --dry-run` forms, a `jj $c` variable verb) and three are
reset-cleared helper leads that round 21 changed deliberately; one is a class-method instance case.
Which of those historic wants is right is not settled here. H2 is a no-worse guard: 166/175 with the
identical passing-case set.

## Claims (three, causally separable)

- **C1 operability (repair).** Frozen 12-case repair set `repair/expected.json`
  (SHA256 `53e34d2691f1a456ce6a4387795c84e5a55d3449b94245d68de516023187c6b9`): the four round-22
  supplemental fixtures copied byte-exact, plus eight round-23 cases for the frame leak, its
  overcorrection guards and the callback-store recall guards. Truth is mechanical:
  `repair/truth.py` runs each fixture under a recording fake `subprocess` module and passes 12/12
  (`evidence/repair-truth.json`). Counter:
  `python3 -I .ufo/waves/round-23/repair/measure.py --tool tools/mado-tripwire.py`.
  Before at base: **6/12** (`evidence/repair-before-e33ea304.json`). Target after: **12/12** at the
  landed lane tip. No-harm guards, each must hold at the landed tip (a guard failure is a harm):
  round-22 primary 57/57; round-21 oracle 35/35 + 17/17 (`round-22/replay.py --mode oracle`);
  precision 166/175 with the same passing set; eleven legacy selftest suites 247/247; whole
  1356-file corpus comparator against the base classifier with every added or removed finding group
  adjudicated and zero new error flips (`round-22/replay.py --mode corpus --before-tool <base>`);
  round-21 assignment and round-22 closure resource populations clean under 384 MiB / 15 s.
- **C2 coverage (learning, sourced).** foot, kitty and ghostty config trees exist on this host and
  have been unsourced since round 17 (`corpus/README.md` frontier). Counter: terminals among
  {foot, kitty, ghostty} with at least one route row in
  `corpus/knowledge/terminal-trees-r23.md` citing a `mined` SOURCES row opened 2026-10-22 whose
  source names that terminal: `python3 -I .ufo/waves/round-23/c2/count.py REV`. Before **0/3**
  (note absent). Target **3/3**.
- **C3 calibration (lowest scored axis, round-17 counter c1 7.1875).** SHONEN box 4 asserts
  "PROVINCE.md still accurate". Observed repo state: tracked `tools/*.py|*.sh` files that
  PROVINCE.md does not name. Counter:
  `REV=<rev>; git ls-tree --name-only $REV tools/ | grep -E '\.(py|sh)$' | while read f; do git show $REV:PROVINCE.md | grep -qF "$(basename "$f")" || echo "$f"; done | wc -l`.
  Before **4** (`mado-action-plan.py`, `mado-assessment.py`, `mado-evidence-audit.py`,
  `mado-tripwire.py`). Target **0**, by an append-only PROVINCE refinement that states each tool's
  actual read-only scope. No tool is removed to hit the number.

No exploratory claim. A miss is an honest stop; no target is narrowed after landing.

## Pre-measurement clarification (append-only, before any after-measurement)

C3's counter is committed as `python3 -I .ufo/waves/round-23/c3/count.py REV`. It reads SHONEN.md box 4
(the self-assessment "No cross-domain bleed (PROVINCE.md still accurate)") and counts tracked
`tools/*.py|*.sh` files whose names PROVINCE.md does not contain: each is a mismatch between that
self-assessment row and the observed repo. Same population and before value as the shell form
above: **4** at base (`evidence/c3-before-e33ea304.json`); target **0**. The shell form stays as
recorded; the script is the counter of record.
