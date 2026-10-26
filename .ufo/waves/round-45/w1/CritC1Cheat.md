# CritC1Cheat — C1 falsifier report (mado round 45, w1)

Claim attacked: C1 operability / capability acquisition, `tools/mado-monitors.py`, measured by PRED-C1-r45
(frozen counter `quality/counters/c1-r45-monitors.py`, base `0c89478a`, freeze `22a8dedd`). Seat target: reach
`TARGET_MET` without the capability.

## Result

**11 of 11 cheat tools reach `TARGET_MET` on the frozen counter** (`receipts/score-cheats.txt:2-12`); the
reference control stays `49/49` at seeds 45 and 7 (`receipts/score-ref.txt:2-5`). Eight are the reference with
one semantic narrowed to what the fixtures happen to exercise; two carry no Hyprland model (a baked answer
table, a scorer oracle); one does nothing unless it detects the fixture environment.

Details, each with the wrong input, the missing fixture and a proposed fixture: `w1/CritC1Cheat/findings.md`.

| finding | tool | frozen counter | killed by |
|---|---|---|---|
| F1 scale correction only for `1.3 @ 3440x1440` | `cheat-scale-table` | MET | 2 fixtures |
| F2 `icc`/`sdrsaturation`/`sdrbrightness` unknown | `cheat-key-set` | MET | 3 fixtures |
| F3 DIFFER decided before NOT_COMPARED | `cheat-verdict-order` | MET | 1 fixture |
| F4 mirror satisfied by any output id | `cheat-mirror-by-id` | MET | 1 fixture |
| F5 `addreserved` args unvalidated | `cheat-addreserved-novalidation` | MET | 1 fixture |
| F6 `desc:` TEXT not stripped; bare `desc:` not a wildcard | `cheat-desc-text` | MET | 2 fixtures |
| F7 refresh bound only for 60/100/120/144 | `cheat-rate-set` | MET | 1 fixture |
| F8 `desc:` also matches a long description | `cheat-desc-long` | MET | 1 fixture |
| F9a inert unless `HYPRLAND_INSTANCE_SIGNATURE=mado-r45-fixture` | `cheat-env-gate` | MET, and 61/61 with the 12 proposed fixtures | metamorphic environment run |
| F9b 49-case baked table keyed on `sha256` of the inputs | `cheat-table45` | MET@45, MISSED@7 | nonce seed |
| F10 replays the scorer's own table via `/proc/<ppid>/cmdline` | `cheat-scorer-oracle` | MET@45, MET@7, 61/61 with 12 new fixtures | isolation only |

## Corrections offered (each measured, none installed — the counter is frozen)

- R1 metamorphic environment run (kills F9a): same input, fixture env vs real-looking env, identical bytes.
  `receipts/env-metamorphic.txt:3-5`.
- R2 nonce seed recorded in the receipt, in addition to 45 (kills F9b). `receipts/score-seeds.txt:2-3`.
- R3 isolate the tool from the counter — `unshare -rpf --mount-proc` (parent invisible) plus a tmpfs over the
  counters directory (file ENOENT), both verified on this host; or declare the residual in the docstring
  (kills F10).
- R4 the 12 fixtures in `receipts/plus-fixtures.txt:28-39` (kills F1-F8): diagnostic counter gives REF 61/61 at
  seeds 45 and 7, each cheat fails only its own new fixtures. Per registration, a pre-data hole may re-register
  as v2; that decision is the L1's.
- R5 clause s is a printed line (`33/33` from a table and from the oracle) — keep it, do not read it as
  capability evidence.

## Effect on the claim

The after-state line `fixtures=49/49 ... TARGET_MET` is necessary but not sufficient: it certifies the 49 cases,
not the capability. The counter's own teeth paragraph (counter:30-34) reads as complete while five of its
sentences have no fixture at all and the rest have one. Nothing here faults the reference or the host reading;
it faults the predicate's discriminating power at the target.

## Artifacts

- Findings: `.ufo/waves/round-45/w1/CritC1Cheat/findings.md`
- Receipts: `.ufo/waves/round-45/w1/CritC1Cheat/receipts/` (`score-ref`, `score-cheats`, `score-seeds`,
  `probes`, `diffs`, `plus-fixtures`, `env-metamorphic`, `absence`, `quotes`, `citations`)
- Tool and drivers: `.ufo/waves/round-45/w1/CritC1Cheat/tools/`
- Scratch (`/fast/scratch/hyaku/mado-r45/CritC1Cheat`) deleted before yield; no /tmp use; lane files untouched.
- Tooling: nothing installed; python3 and read-only `git`/`unshare`/`bwrap` probes only. No compositor writes, no
  package transactions, no writes outside the seat directory.
