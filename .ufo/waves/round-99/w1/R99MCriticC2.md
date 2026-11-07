# R99MCriticC2 — C2 falsification (the harm watch as an instrument)

Seat: critic, round 99 wave w1. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base
`2cbaa141f42df9dfeee4d207cae6558a4dd59863`. Contract read:
`.ufo/waves/round-99/claims-declaration-r99.md` (C2, PRED-C2-r99-v1, Shared contract 3).
Receipt: `.ufo/waves/round-99/receipts/critic-c2-r99.txt`.

This report attacks C2 only. It does not edit the tool, the panel, the counter, or any lane
artifact. Every measurement below is read-only: the legs I ran are the committed round-97
harness's own functions (`.ufo/waves/round-97/controls/harm-r97.sh`), each writing only under my
scratch root; the fixture panels are mine (scratch, `mkfix.py`); the reference tool
`ref-harm-watch.py` is a critic instrument, not a candidate.

**Instruments vs candidates.** `harm-r97.sh` (the leg runner), my `ref-harm-watch.py` (a
contract-faithful reference used only to test the contract's own sentences), my fixture panels,
and my attack driver are instruments. `quality/harm-watch.py` and
`quality/counters/c2-r99-harm-watch.py` are the candidates under attack; I ran them, never
edited them.

## 1. The leg set, re-derived

Sources: `.ufo/waves/round-98/receipts/harm-base-r98.txt` (28 `LEG` lines, artifacts tip
`06b6bf2a`), `harm-final-r98.txt` (26 `LEG` lines, records tip `020af865`), the harness
`.ufo/waves/round-97/controls/harm-r97.sh` (`ALL_LEGS`, 28 names), and the `SKILL.md` registry
rows.

### 1.1 Every leg the round-98 watch ran (28, base run)

| # | leg | base rc | final rc | registry row | row self-sufficient? |
|---|---|---|---|---|---|
| 1 | `verify_selftest` | 0 | 0 | `mado-verify` | yes (`bash tools/mado-verify.sh --selftest`) |
| 2 | `verify_file_plane` | 0 | 0 | `mado-verify` | yes (`--no-live`) |
| 3 | `index` | 0 | 0 | **none** | no row; argv only from `harm-r97.sh` |
| 4 | `ledger` | 1 | 0 | **none** | no row; argv only from `harm-r97.sh` |
| 5 | `mako_selftest` | 0 | 0 | **none** | no row; argv only from `harm-r97.sh` |
| 6 | `portals_selftest` | 0 | 0 | `mado-portals` | yes (`--selftest`) |
| 7 | `mime_selftest` | 0 | 0 | `mado-mime` | yes |
| 8 | `xdgmime_selftest` | 0 | 0 | `mado-xdgmime` | yes |
| 9 | `mimeglob_selftest` | 0 | 0 | `mado-mimeglob` | yes |
| 10 | `mimesniff_selftest` | 0 | 0 | `mado-mimesniff` | yes |
| 11 | `seat_reports_selftest` | 0 | 0 | `mado-seat-reports` | yes |
| 12 | `receipt_presence_selftest` | 0 | 0 | `mado-receipt-presence` | yes |
| 13 | `gate_selftest` | 0 | 0 | `mado-selftest-strength` | yes |
| 14 | `gate_seat_reports` | 0 | 0 | `mado-selftest-strength` | yes (tool+kills) |
| 15 | `gate_mimeglob` | 0 | 0 | `mado-selftest-strength` | yes |
| 16 | `gate_portals` | 0 | 0 | `mado-selftest-strength` | yes |
| 17 | `r90c2_receipt_presence` | 0 | 0 | `mado-r90-receipt-presence` | yes (pins in row) |
| 18 | `r92_gate_defects` | 0 | 0 | `mado-r92-gate-defects` | yes |
| 19 | `r90c1_portal_routing` | 2 | 2 | `mado-r90-portal-routing` | yes; declared SETUP_ERROR |
| 20 | `r94c1_mimeglob` | 0 | 0 | `mado-r94-mimeglob` | yes |
| 21 | `r94c2_selftest_kills` | 0 | 0 | `mado-r94-selftest-kills` | yes |
| 22 | `r93c2_selftest_strength` | 0 | 0 | `mado-r93-selftest-strength` | yes |
| 23 | `r95c1_mimesniff` | 2 | 2 | `mado-r95-mimesniff` | **no** (declaration has no counting-command block) |
| 24 | `r95c2_selftest_kills` | 2 | 2 | `mado-r95-selftest-kills` | **no** (same) |
| 25 | `r96c1_magictext` | 2 | 2 | `mado-r96-magictext` | yes; stale mutant pin (r96 D5) |
| 26 | `r96c2_selftest_kills` | 0 | 0 | `mado-r96-selftest-kills` | yes |
| 27 | `r97c1_filetype` | 0 | **dropped** | `mado-r97-filetype` | yes (full pins) |
| 28 | `r97c2_counter_selftest` | 1 | **dropped** | `mado-r97-counter-selftest` | **no** (`...` placeholders) |

### 1.2 Every leg the final run dropped

Exactly two: `r97c1_filetype` (was rc 0) and `r97c2_counter_selftest` (was rc 1, the literal
`<SKILL-AT-MEASURED-REV>` redirect). The final run's 26 = 28 − 2. No leg was added between the
two runs; the final run is the base set minus two.

### 1.3 Every leg the panel adds

The seat prompt says: all 28 base legs plus the two the final run dropped (they are already in
the 28 — the phrase is emphasis, not addition), optionally plus the two round-98 counters
(`mado-r98-execargv`, `mado-r98-sources-readback`). So the panel's legal sizes are **28** (no
r98 counters) or **30** (with them). A panel of 30 built literally as "28 + the two dropped"
instead of "28" would carry two duplicate ids and must fail `PANEL_DUPLICATE`; the prompt's
arithmetic is ambiguous and is a build hazard, not a panel property.

**Registry provenance gap.** Three of the 28 legs (`index`, `ledger`, `mako_selftest`) have no
`SKILL.md` registry row at all, and two (`r95c1_mimesniff`, `r95c2_selftest_kills`) have a row
whose declaration carries no counting-command block. The panel's argv for those five cannot be
reconstructed from the registry; it comes from the round-97 harness. That is fine if the panel
says so, but the claim's "reconstruct each leg's argv from the `SKILL.md` registry rows" is not
what the registry supports.

### 1.4 Is the panel's `rounds` map complete?

The census's round checks are one-directional: `PANEL_ROUND_MISSING` fires only for a round
**declared in `rounds`** that has no row, and `PANEL_LEG_UNKNOWN`/`PANEL_LEG_MISSING` compare the
rows to `rounds`. Nothing compares `rounds` to an external list of rounds. Therefore:
- A leg dropped from `legs` **and** from `rounds` is invisible to the census.
- A whole round dropped from `rounds` is invisible to the census.
- The only independent anchor is `expect_legs`, a bare integer. If it is derived from
  `len(legs)` at build time, the census is circular and cannot detect the round-98 defect
  (legs dropped from the run) at all.

So "the `rounds` map is complete" can only mean "complete against the frozen 28/30 id list",
and that is checkable only by comparing the panel's ids to the re-derived list in §1.1 — not by
the census. The panel must therefore freeze `expect_legs` **and** the id set from the r98
receipts, and the counter must pin the panel's sha256 (it does). I check the actual panel's ids
against §1.1 in §3.

## 2. The census, attacked

Fixture panels are mine (`mkfix.py`, 20 panels). Each was run through my contract-faithful
reference (`ref-harm-watch.py`) to establish what the contract's own rules imply, and through the
candidate when it landed. The reference reports **all** census findings in the contract's
declared order.

| fixture | intent | reference verdict |
|---|---|---|
| `pass-dash-marker` | leg with `expect_marker: "-"`, output contains `-` | pass (rc 0) |
| `pass-dash-noliteral` | `expect_marker: "-"`, output has no `-` | pass only if `-` means "no marker" |
| `pass-marker-twice` | marker appears twice | pass |
| `pass-two-legs-one-round` | two rows in one round | pass |
| `pass-round-int` | row `round` is int 97, `rounds` key "97" | pass only with str() coercion |
| `pass-rc-string` | `expect_rc: "0"` (string) | **mismatch** under strict compare |
| `pass-empty-marker` | `expect_marker: ""` | pass (vacuous) |
| `pass-empty-panel` | `expect_legs:0, rounds:{}, legs:[]` | **pass (vacuous green)** |
| `fail-count` | 1 row, `expect_legs:3` | `PANEL_LEG_COUNT` |
| `fail-duplicate` | id twice | `PANEL_DUPLICATE` |
| `fail-round-missing` | round 98 declared, no row | `PANEL_ROUND_MISSING 98` + `PANEL_LEG_MISSING z` |
| `fail-leg-unknown` | row id not in `rounds` | `PANEL_LEG_UNKNOWN b` |
| `fail-leg-missing` | declared id, no row, count adjusted | `PANEL_LEG_MISSING b` (single) |
| `fail-dropped-unchanged` | one row removed, `expect_legs` unchanged | **`PANEL_LEG_COUNT` + `PANEL_LEG_MISSING b`** |
| `fail-round-silent` | rounds `{97:[a,b]}`, rows a(97), b(98) | **pass (silent)** |
| `run-wrong-rc` | rc 0 vs expect 5 | mismatch, `marker=ok` |
| `run-wrong-marker` | marker absent | mismatch, `marker=MISS` |
| `run-timeout` | leg sleeps 30 s, `timeout_s:1` | mismatch (rc −9) |
| `run-rev-sub` | argv `[..., "REV", "PREVIEW"]` | exact-token substitution only |
| `run-census-norun` | census-failing panel whose leg writes a file | exit 2, file absent |

### 2.1 False positives

None on the pass fixtures except the two type-dependent ones: a panel with `expect_rc` as a JSON
string, or a row `round` as an int against a string key, is rejected by a strict implementation.
Both are panel-authoring hazards (the panel must use ints and matching key types), not tool
defects — but the contract does not say so, and the panel builder can trip on either.

### 2.2 False negatives (the census's real holes)

1. **The planted `dropped-leg` control is unsatisfiable under the contract's literal rule.**
   Removing one row while leaving `expect_legs` unchanged makes **two** census conditions true:
   `PANEL_LEG_COUNT` (rows ≠ `expect_legs`) and `PANEL_LEG_MISSING` (declared id, no row). The
   contract's control sentence says the planted panel "must produce exactly `PANEL_LEG_MISSING
   <id>`". A literal implementation prints both; one that stops at the first finding in the
   declared order prints `PANEL_LEG_COUNT` first. The gate resolves this by suppressing
   `PANEL_LEG_COUNT` when the delta is explained by the other findings (measured: exactly
   `PANEL PANEL_LEG_MISSING id=b round=97`), and the panel now carries that `census_rule`. So the
   **tool is right and the claim sentence is wrong**; the freeze block must adopt the rule (F1).
   A reader who re-derives the census from the claim gets a different answer.
2. **A row's `round` field is not cross-checked as a `ROUND_MISSING` condition.** The gate
   catches a row whose round disagrees with its declaring key as `PANEL_LEG_UNKNOWN` (measured:
   `fail-round-silent` → `PANEL PANEL_LEG_UNKNOWN id=b`), not as `PANEL_ROUND_MISSING`. That is
   a fail, so the panel is still rejected; the finding id is just not the one a reader expects
   from "a declared round with no row". A round dropped from `rounds` entirely remains invisible
   (see §1.4).
3. **A leg dropped from `legs` and `rounds` together, with `expect_legs` decremented, passes.**
   The census cannot detect a leg dropped from the panel itself; only a leg declared-but-absent.
   The round-98 defect was exactly a leg dropped from the run, so the census's "fails closed"
   property does not cover the defect the claim says it covers. The defense is the independently
   frozen count and id set, nothing in the tool.
4. **`expect_marker: ""` and `expect_marker: "-"` are free passes.** The contract defines the
   marker as a literal substring; `""` is a substring of everything, and `-` is a substring of
   almost every command line and most output. If the panel uses `-` for "no marker", the tool
   must special-case it (the contract does not say so), and every such leg's marker check is
   vacuous. If the tool treats `-` literally, a leg with no `-` in its output MISSes.
5. **An empty panel is green under the contract's rules.** `expect_legs:0, rounds:{}, legs:[]`
   → `HARM_WATCH: legs=0 ok=0 mismatch=0`, exit 0 for a literal implementation (my reference
   does this). The gate is stronger: it returns `PANEL PANEL_UNREADABLE legs-missing-or-empty`,
   exit 2. The contract does not require the rejection, so a future implementation may be
   vacuous-green. State the rejection in the contract (the gate already does it).

## 3. The panel

Measured draft: `.ufo/waves/round-99/controls/harm-panel-r99.json`, sha256
`7bf25b73bc868fba685bed9381f09be26f7e16ef72980aaac8fd61512827ec2a`, 28 legs,
`expect_legs=28`, `timeout_s=3600`, plus a top-level `census_rule` key.

### 3.1 Leg set and map consistency

| check | observed |
|---|---|
| `len(legs)` vs `expect_legs` | 28 = 28 |
| duplicate ids | none |
| ids vs the re-derived r98 base set (§1.1) | exactly equal, all 28 |
| the two dropped legs present | `r97c1_filetype`, `r97c2_counter_selftest` both present |
| `rounds` union vs the id set | 28 = 28 (no `PANEL_LEG_UNKNOWN`, no `PANEL_LEG_MISSING`) |
| `rounds` sizes | `base` 16, r90 2, r92 1, r93 1, r94 2, r95 2, r96 2, r97 2 |
| `PANEL_ROUND_MISSING` | none |

**The panel's `expect_legs`/`rounds`/`legs` are mutually consistent and the leg set is
correct**: it is the 28-leg r98 base set with both dropped legs restored. A dropped leg is
detected — measured on the real panel: removing `r97c1_filetype` gives exactly
`PANEL PANEL_LEG_MISSING id=r97c1_filetype round=r97`, exit 2; adding `gate_xdgmime` gives
exactly `PANEL PANEL_LEG_UNKNOWN id=gate_xdgmime`, exit 2.

Two limits of that consistency:
1. The `base` bucket holds 16 legs from rounds 5..95 as one key. The map is complete but not
   per-round: a reader cannot tell which round contributed `verify_selftest` or `mime_selftest`,
   and the census cannot detect a *round* dropped from `rounds` (it only checks declared rounds
   with no row). The map is a completeness device, not a provenance record.
2. `expect_legs=28` is the only independent anchor. It is correct here because it equals the
   r98 base set, not because the tool can derive it.

### 3.2 The two dropped legs

- `r97c1_filetype`: full argv from the registry row/`harm-r97.sh`; I ran it at `2cbaa141`:
  rc 0, `MADO_FILETYPE_COUNT: TARGET_MET … cases=157 correct=157 classes=15/15 mutants=101
  killed=101`. The panel's `expect_rc=0`, marker `MADO_FILETYPE_COUNT: TARGET_MET` reproduce.
  Wall time ~7 min (measured), so `timeout_s=3600` is adequate.
- `r97c2_counter_selftest`: the row pins `--rev` **literally** to `2cbaa141` and carries
  `--expect-registry-sha256 2597e936…` (SKILL.md at `2cbaa141`) and
  `--expect-ledger-sha256 7c7037d3…` (ledger at `2cbaa141`). I ran the row exactly: rc 0,
  `MADO_COUNTER_SELFTEST_COUNT: TARGET_MET pred=PRED-C2-r97-v1 rev=2cbaa141…`. The expectation
  reproduces. But this row is **not a measured-rev leg**: it ignores `REV` and runs at the base,
  so it does not exercise the round-99 tree. The note states this. The r97 freeze values
  (SKILL.md `fab1ff74…`, ledger `fb0f2f3c…`) are superseded — measured: with the r97 pins the
  same command prints `SETUP_ERROR … SKILL.md sha256 != --expect-registry-sha256`. No false
  provenance (the note records it), but the freeze block must name the row as a base-rev
  historical replay, not a leg of the measured tree.

### 3.3 Marker brittleness (the frozen-expectation defect)

Nine rows freeze a marker that embeds a **check count**:

| leg | frozen marker |
|---|---|
| `mako_selftest` | `MADO_MAKO_SELFTEST: checks=62 failed=0` |
| `portals_selftest` | `MADO_PORTALS_SELFTEST: checks=28 failed=0` |
| `mime_selftest` | `MADO_MIME_SELFTEST: checks=17 failed=0` |
| `xdgmime_selftest` | `MADO_XDGMIME_SELFTEST: checks=12 failed=0` |
| `mimeglob_selftest` | `MADO_MIMEGLOB_SELFTEST: checks=19 failed=0` |
| `mimesniff_selftest` | `MADO_MIMESNIFF_SELFTEST: checks=26 failed=0` |
| `seat_reports_selftest` | `SEAT_REPORTS_SELFTEST: checks=23 failed=0` |
| `receipt_presence_selftest` | `RECEIPT_PRESENCE_SELFTEST: checks=6 failed=0` |
| `gate_selftest` | `SELFTEST_STRENGTH_SELFTEST: checks=11 failed=0` |

All nine reproduce at the base (I ran every one; rc 0, exact line). But a count is a moving
value: a later round that legitimately adds one check to any of these tools makes the panel red
while the leg's rc is unchanged. The declaration's named limit covers "a later tree that
legitimately changes a leg's rc"; it does not cover a marker-only change. The stable substring
is `failed=0` (or the verdict token). This is the "a leg whose expectation is a scratch path or
a timestamp is a defect" class, with a count in place of the timestamp.

The other markers are stable: `assertions passed` (verify), `missing=0 dangling=0 duplicates=0`
(index), `uncovered=0` (ledger), `MADO_VERIFY: CLEAN`, the `TARGET_MET`/`SETUP_ERROR` verdict
tokens, and the `SELFTEST_STRENGTH: OK tool=…` lines.

### 3.4 The `census_rule` key

The panel now carries a top-level `census_rule` stating the net-of-findings rule the gate
implements. The gate's docstring states it too. The **claim text does not**: it says
`PANEL_LEG_COUNT (row count ≠ expect_legs)`. A reader re-deriving the census from the claim gets
a different answer than the tool. The freeze block must adopt the panel's rule (or the tool must
change). This is the one contract sentence the wave reversed; it must not be left implicit.

## 4. Discrimination

Measured against the counter `007072dd…` and the gate `8ad90bed…`. The counter's `--gate` draft
mode was used with my own planted panels (the seat's `controls/harm-planted/` had not landed at
measurement time; the counter's planted-panel logic is the same in both modes). A 3-leg panel
was used so the runs are fast; the only predicate condition that misses on it is
`panel_legs_ge_20`, which is visible in every line.

| gate under test | counter verdict | caught? |
|---|---|---|
| the real gate (`8ad90bed`) | `planted_dropped_leg=1 planted_wrong_expect=1 planted_extra_leg=1 stub_flagged=1 mismatches=0` | green (only `panel_legs_ge_20` misses on my 3-leg panel) |
| always-OK stub (my `stub-always-ok.py`) | all planted flags 0 | **caught** (`TARGET_MISSED`) |
| row-counting stub (`stub-count-only.py`, never runs a leg) | `planted_dropped_leg=0 planted_wrong_expect=0 planted_extra_leg=0 stub_flagged=0` | **caught** (`TARGET_MISSED`) |
| gate with `rc_ok = True` (ignores `expect_rc`) | `planted_wrong_expect=0` | **caught** (`TARGET_MISSED`) |
| gate with `marker_ok = True` (ignores `expect_marker`) | `planted_dropped_leg=1 planted_wrong_expect=1 planted_extra_leg=1 stub_flagged=1 mismatches=0` | **NOT caught** |

The marker-ignoring gate is the counterexample: every control passes, `mismatches=0`, and on
the real 28-leg panel the only remaining condition (`panel_legs_ge_20`) is satisfied. **A gate
that never checks `expect_marker` would be scored `TARGET_MET`.** The counter has no planted
marker-miss panel, and it never runs the gate's own `--selftest` (the gate's 26 checks include
a marker-miss check; the counter's `selftest_checks` is its own 15-check fixture pipeline). The
marker half of the model is therefore unverified by the counting command.

Two more discrimination facts:
- `stub_flagged` is a **counter self-check**, not a gate control. The counter writes its own
  always-OK `STUB_GATE`, runs it on the dropped-leg panel, and sets
  `stub_flagged = stub_ok_while_red and flags["dropped"] == 1`. It is 1 iff the real gate
  already flagged the dropped panel. It does not test whether the real gate resists a stub; the
  `planted_*` flags do that. The claim's control sentence ("an always-OK stub must be flagged")
  is implemented as a self-test of the counter, not of the gate.
- `legs_run` is `len(gate_json["legs"])`; the gate reports one entry per row whether or not the
  leg ran. A gate that prints per-row entries without spawning would pass
  `legs_run == panel_legs`; only the planted panels defend that, and they do not cover markers.

## 5. Frozen expectations — five legs, run by me

All at `2cbaa141` with the committed round-97 harness, my scratch root
`/fast/scratch/hyaku/mado-r99/R99MCriticC2/legs*`.

| leg | measured rc | stable marker (substring of its own verdict line) | brittle marker (must NOT be frozen) |
|---|---|---|---|
| `verify_selftest` | 0 | `MADO_SELFTEST:` … `assertions passed` | `460/460` (assertion count grows) |
| `index` | 0 | `missing=0` / `coverage=10.0000/10` | `rev=2cbaa141…` (rev changes every round), `indexed=119/119` |
| `ledger` | 0 | `verdict=TARGET_MET` | `population=195` (new tools/counters change it), `rev=…` |
| `mako_selftest` | 0 | `MADO_MAKO_SELFTEST:` … `failed=0` | `checks=62` (checks grow) |
| `r90c1_portal_routing` | 2 | `MADO_PORTAL_ROUTING: SETUP_ERROR` | the whole line (carries the mutant id) |

Additional measured legs (same run): `verify_file_plane` 0 (`MADO_VERIFY: CLEAN`),
`portals_selftest` 0 (`checks=28 failed=0`), `mime_selftest` 0 (`checks=17`),
`xdgmime_selftest` 0 (`checks=12`), `mimeglob_selftest` 0 (`checks=19`),
`mimesniff_selftest` 0 (`checks=26`), `gate_selftest` 0 (`checks=11`),
`seat_reports_selftest` 0 (`checks=23`), `receipt_presence_selftest` 0 (`checks=6`),
`r95c1_mimesniff` 2 (`SETUP_ERROR no counting-command block`),
`r96c1_magictext` 2 (`SETUP_ERROR … mutants sha256 448150e2… != pinned f8d461e8…`),
`r97c2_counter_selftest` 1 (`bash: SKILL-AT-MEASURED-REV: No such file or directory`).

**The dropped leg `r97c2_counter_selftest` is not replayable with its r97 pins at any later
rev.** Measured: at `2cbaa141` with the r97 freeze values (SKILL.md `fab1ff74…`, ledger
`fb0f2f3c…`, both computed from `65ff5591`, the r97 measured rev), the counter prints
`MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR pred=PRED-C2-r97-v1 SKILL.md sha256 !=
--expect-registry-sha256`. The r99 base's SKILL.md is `2597e936…` and its ledger `7c7037d3…`.
The leg's own pins are rev-specific by construction, so "replay the dropped leg" can only mean
(a) re-pin to the measured rev — a command that is not the r97 command and must be re-pinned
every round, or (b) freeze rc 2 with the r97 pins — a leg that proves nothing (the
`r90c1_portal_routing` class). The panel chose (a) with the base rev and the base pins, and its
note states it; measured green (§3.2). The remaining obligation is the freeze block's: say that
this row is a base-rev replay, not a leg of the measured tree.

`r97c1_filetype` completed in my own run (rc 0, ~7 min, `MADO_FILETYPE_COUNT: TARGET_MET`);
`r97c2_counter_selftest` via the harness (placeholder) rc 1, and via the panel's re-pinned row
rc 0. Every other leg I ran matches the panel's frozen rc and marker.

## 6. Findings and the smallest safe corrections

Ordered by what the freeze block must decide; F1–F3 are the ones that change a verdict.

**F1 — the census rule in the claim is not the census rule in the tool (contract).**
Claim: `PANEL_LEG_COUNT (row count ≠ expect_legs)`. Tool and panel: `PANEL_LEG_COUNT` fires only
when the delta is not explained by the other findings. Measured: a panel with one row removed and
`expect_legs` unchanged prints exactly `PANEL PANEL_LEG_MISSING id=b round=97` and **no**
`PANEL_LEG_COUNT`. Without the suppression the contract's own planted control ("exactly
`PANEL_LEG_MISSING`") is unsatisfiable. Smallest correction: adopt the panel's `census_rule` in
the claim/freeze block (the tool and panel already say it), or drop the "exactly" in the control
sentence. Impact: the census rule a reader re-derives; not the tool's behavior.

**F2 — the predicate cannot see a gate that ignores `expect_marker` (counter).**
Measured: a gate with `marker_ok = True` passes every planted control
(`planted_dropped_leg=1 planted_wrong_expect=1 planted_extra_leg=1 stub_flagged=1`,
`mismatches=0`); on the 28-leg panel the only remaining condition is satisfied → `TARGET_MET`.
The counter has no marker-miss plant, and it never runs the gate's `--selftest` (whose 26 checks
include a marker-miss). Smallest correction: add a fifth planted panel `marker-miss.json` (one
leg's `expect_marker` replaced by a string absent from its output) and require exactly one
`LEG … marker=MISS` mismatch; or run the gate's `--selftest` and require
`HARM_WATCH_SELFTEST: checks>=12 failed=0`. Impact: `mismatches == 0` is gate-self-reported; the
marker half of the model is otherwise unverified.

**F3 — `selftest_checks` is the counter's selftest, not the gate's (counter provenance).**
The predicate's `selftest_checks >= 12 AND selftest_failed == 0` is measured as the counter's own
15-check fixture pipeline (`selftest=checks=15 failed=0`). The gate's
`HARM_WATCH_SELFTEST: checks=26 failed=0` is never run by the counting command. A gate with a
broken selftest (but a green frozen panel) passes. Smallest correction: name whose selftest the
predicate means and run that one; running both is stronger.

**F4 — nine markers embed a check count (panel brittleness).**
`mako 62, portals 28, mime 17, xdgmime 12, mimeglob 19, mimesniff 26, seat_reports 23,
receipt_presence 6, gate_selftest 11` (all `checks=N failed=0`). A legitimate later round that
adds one check makes the panel red with the rc unchanged; the named limit covers rc changes
only. Smallest correction: freeze `failed=0` (or the verdict token) for those nine.

**F5 — `r97c2_counter_selftest` is a base-rev replay, not a measured-rev leg (panel).**
The row pins `--rev` literally to `2cbaa141` and the base pins; it ignores `REV`. Measured green
at the base; measured `SETUP_ERROR` with the r97 pins. The note is honest; the freeze block must
name the row as a historical replay so a reader does not count 28 legs of the measured tree.

**F6 — `-` is a literal marker, not "no marker" (gate, minor).**
Measured: `expect_marker: "-"` MISSes on output with no `-`; an empty marker is a free pass. The
lane's CLI convention uses `-` for "none" (`terminal=<name|->`), so a panel author may trip. The
frozen panel uses no `-` and no empty marker, so the measured run is unaffected; state the
semantics in the contract.

**F7 — `--json` prints the human lines and the JSON (gate, minor).**
The docstring now says so; the shared contract 3 does not define `--json` output. The counter
parses the last line, so it works. State it in the contract or make `--json` exclusive.

**F8 — the census is one-directional on rounds (gate, minor).**
A row whose `round` field disagrees with the declaring round is reported as `PANEL_LEG_UNKNOWN`
(measured: `fail-round-silent` → `PANEL_LEG_UNKNOWN id=b`), not `PANEL_ROUND_MISSING`; a round
dropped from `rounds` entirely is invisible. The five finding ids do not cover "a round with no
row" when its ids are declared elsewhere. Either widen `PANEL_ROUND_MISSING` to "no row carries
this round" or state the narrower meaning.

**F9 — a per-leg setup failure aborts the remaining legs (gate, minor).**
The gate prints the LEG line with `rc=SETUP`, then `HARM_WATCH: setup-error leg=<id> detail=…`
and exits 2, without running the rest of the panel. The contract says each leg runs once; a
scratch refusal on leg 1 hides legs 2..N. State it as a named limit or continue the panel and
exit 2 at the end.

**F10 — the counter's predicate has two conditions the claim's predicate does not list
(counter/claim divergence, minor).**
The claim lists `panel_legs == declared_legs`, `legs_run == panel_legs`, `mismatches == 0`,
`planted_dropped_leg_flagged`, `planted_wrong_expect_flagged`, `stub_flagged`, and the selftest
pair. The counter also requires `panel_legs >= 20` and `planted_extra_leg == 1` (a fourth
planted panel, `extra-leg.json`). Both are strengthenings, not weakenings, but a reader
re-deriving `TARGET_MET` from the claim gets a different answer for a small or extra-leg-red
panel. The freeze block should print the counter's actual condition list, or the claim should
add the two.

**Build observation (not a finding).** The gate draft at sha `6d18d8c3` (18:28) failed its own
selftest 9/26 (`FIXTURE_VERDICT: GOOD rev=` read `sys.argv[3]`, which the 1-argument fixture rows
do not carry); the counter draft at `7d179c76` crashed on the main path (`%d` on the
`st_failed` list). Both were fixed in later revisions (`8ad90bed`, `007072dd`), which is why the
report measures the fixed bytes. The freeze block must pin the fixed shas, not the drafts.

**Tool/version/channel record.** No tool was installed or upgraded; no pacman transaction; no
network fetch beyond the committed round-99 fetch dir. Instruments used: `python3` (host),
`git` (read-only `show`/`cat-file`), `setsid`/`timeout` (process isolation), the committed
`harm-r97.sh` harness, and my own scratch fixtures.
