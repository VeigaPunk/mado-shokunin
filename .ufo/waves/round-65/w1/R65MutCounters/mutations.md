# mado round-65 w1 — mutation report: the new counters (seat R65MutCounters)

Date 2026-11-03. Leaf seat; no subagent dispatch. Every mutation ran on a COPY under
`/fast/scratch/hyaku/mado-r65/w1/R65MutCounters/`; the drafts in
`.ufo/waves/round-65/w1/{R65ExecC1Counter,R65ExecLandingCounters}/` were only read.

## 0. Targets and tested bytes

| target | path (read-only) | sha256 tested | bytes |
|---|---|---|---|
| A — C1 counter | `.ufo/waves/round-65/w1/R65ExecC1Counter/c1-r65-register.py` | `2ccedc6852a35a8cfbaaf8a92b1ad473c1464499cc892fa8753dc199eaaa1871` | 11668 |
| B — C2 instrument | `.ufo/waves/round-65/w1/R65ExecLandingCounters/landing-counters.sh` | `c12b72e20cfaeb92e7ff242b26f2a26eecd6184610e78287fb7b326a30fd5e9a` | 9902 |

Both drafts were still being iterated when first seen: an earlier instrument revision
(sha `55d39b6f…`, 19:37) failed its own selftest **18/19** — `SELFTEST FAIL 19: a15 selftest
scratch removed on exit` plus `line 1: SW: unbound variable` (EXIT trap referenced a function-local
`SW`). That revision was replaced by the tested `c12b72e2…`, whose selftest is 19/19. **The whole
battery below was re-run on the final bytes above**, and both draft shas were re-checked at write
time and matched.

## 1. Method

Detectors are the same commands the executors ran, not new contracts:

- **A (C1 counter has no `--selftest`)** — the claim's counting command against a matrix of
  purpose-built git fixtures (positive + negative), plus the do-nothing base control:
  `python3 c1-r65-register.py --repo fx/<name> --rev <rev>`. A mutant is KILLED when any
  `(fixture, verdict, rc)` triple moves off the pristine baseline.
- **B (instrument)** — its own frozen detector:
  `bash <copy>/quality/landing-counters.sh --selftest --scratch-root <scratch>/st/<id>`.
  A mutant is KILLED when that selftest exits non-zero / prints a `SELFTEST FAIL` the pristine
  bytes do not (baseline: rc=0, `MADO_LANDING_COUNTERS_SELFTEST: 19/19 assertions passed`).
  The copy sits in a lab tree with the three real sibling instruments
  (`quality/check-tool-ledger.py`, `quality/counters/c3-r56-used-by.py`,
  `tools/mado-receipt-citecheck.py`) so the script's own-path resolution works as at landing.

Each mutant is exactly one textual/behavioural change, applied by an exact single-match
replacement (the harness refuses a patch whose pattern does not occur exactly once). Nothing was
restored: every run used a fresh copy; the pristine bytes were never edited.

### 1.1 C1 fixture matrix — pristine baseline (11 fixtures)

`python3 c1-r65-register.py --repo fx/<name> --rev <rev>`; fixture revs in
`evidence/fixture-revs.txt`.

| fixture | what it is | verdict | rc |
|---|---|---|---|
| pos | 8 rows, 8 groups, 2 receipts resolved, gate-live carries `MADO_VERIFY: CLEAN` | TARGET_MET | 0 |
| pos-extra | valid block + 1 extra non-group row (rows=9) | TARGET_MET | 0 |
| neg-dupgroup¹ | 8 rows, all 8 groups, one duplicated row | TARGET_MET | 0 |
| neg-droprow | windows-desktop row deleted (rows=7, groups=7/8) | TARGET_MISSED | 1 |
| neg-gate-dirty | same rows, gate receipt says `MADO_VERIFY: DIRTY` | TARGET_MISSED | 1 |
| neg-dangling | one row points at a receipt absent from the rev | TARGET_MISSED | 1 |
| neg-nearmiss | first cell `walkerX` instead of `walker` | TARGET_MISSED | 1 |
| neg-base | no 2026-11-03 block | TARGET_MISSED | 1 |
| neg-8r7g-gateok | 8 rows, 7 distinct groups (waybar twice), gate ok | TARGET_MISSED | 1 |
| neg-sentinel-leak | 7 rows, sentinel, then a windows-desktop row after it | TARGET_MISSED | 1 |
| neg-wt-only | PROVINCE at rev has no block; worktree has the block (uncommitted) | TARGET_MISSED | 1 |
| lane @ base `524fa1f9…` (control) | real lane, do-nothing control | TARGET_MISSED | 1 |

¹ file-name artifact from the fixture generator; the bytes are a positive shape and were kept as
an extra positive control.

### 1.2 Instrument baseline

```
bash lab/quality/landing-counters.sh --selftest --scratch-root …/st/baseline
→ rc=0  MADO_LANDING_COUNTERS_SELFTEST: 19/19 assertions passed
```

## 2. Mutants — target A (C1 counter)

| # | mutation (single change) | expected observation | observed | killed |
|---|---|---|---|---|
| M1 | `met = (len(rows) >= 8 and` → `>= 9` (off-by-one up) | `pos` (8 rows) flips MET→MISSED | `pos`: MET/rc0 → MISSED/rc1; `neg-dupgroup` likewise | **yes** |
| M2 | same `>= 8` → `>= 7` (off-by-one down) | a 7-row fixture wrongly MET | no deviation on any of 11 fixtures | **no** (equivalent — §3.1) |
| M3 | `len(groups) == len(GROUPS)` → `>= 7` | `neg-8r7g-gateok` (rows=8, groups=7) wrongly MET | `neg-8r7g-gateok`: MISSED/rc1 → MET/rc0; `neg-nearmiss` likewise | **yes** |
| M4 | `GATE_TOKEN = "MADO_VERIFY: CLEAN"` → `"MADO_VERIFY"` | `neg-gate-dirty` wrongly MET | MISSED/rc1 → MET/rc0 | **yes** |
| M5 | drop `and len(resolved) == len(receipts)` | `neg-dangling` wrongly MET | MISSED/rc1 → MET/rc0 | **yes** |
| M6 | `name in first_cells` → `any(name in cell for cell in first_cells)` (substring match) | `neg-nearmiss` (`walkerX`) wrongly MET | MISSED/rc1 → MET/rc0 | **yes** |
| M7 | `province = git(repo, "show", "<rev>:PROVINCE.md")` → `open(<repo>/PROVINCE.md)` (worktree read) | `neg-wt-only` wrongly MET | MISSED/rc1 → MET/rc0 | **yes** |
| M8 | `return 0 if met else 1` → `return 0` | negatives print MISSED but exit 0 | rc 1→0 on 6 negative fixtures (verdict line unchanged) | **yes** |
| M9 | drop the sentinel arm (`cand.startswith("## ") or … SENTINEL` → `## ` only) | `neg-sentinel-leak` wrongly MET | MISSED/rc1 → MET/rc0 | **yes** |
| M10 | remove `"windows desktop plane"` from the `GROUPS` tuple (drop a required group) | 8-row/7-group fixture wrongly MET | `neg-8r7g-gateok`: MISSED/rc1 → MET/rc0 | **yes** |

Base-run control per mutant (`--repo <lane> --rev 524fa1f9…`): **all ten stayed
`TARGET_MISSED rc=1`**. The base control is necessary but non-discriminating: at base the counter
returns at the `block is None` branch before any mutated predicate runs (M8's always-0 return is
not even reached). All kills above come from the fixture matrix.

## 3. Mutants — target B (instrument)

| # | mutation (single change) | expected observation | observed | killed |
|---|---|---|---|---|
| I1 | citecheck leg skipped (`if [ "$leg" = citecheck ]; then rc=0; else "leg_$leg"; rc=$?; fi`) | selftest FAIL | `19/19`, rc=0 — no assertion notices the leg never ran | **no** (§3.2) |
| I2 | `"leg_$leg"; rc=$?` → `"leg_$leg" \| tail -1; rc=$?` (producer rc replaced by tail's rc) | selftest FAIL | a9 FAIL: `fixture landing run exits 1 when a leg is red (want=1 got=0)`; 18/19 rc=1 | **yes** |
| I3 | `landing_verdict` `&&` → `\|\|` (flip the conjunction) | selftest FAIL | a9, a12 (`want=RED got=GREEN`), a13 FAIL; 16/19 rc=1 | **yes** |
| I4 | `[ "$verdict" = GREEN ]; exit $?` → `exit 0` | selftest FAIL | a9 FAIL (want=1 got=0); 18/19 rc=1 | **yes** |
| I5 | remove the `/tmp` arm from the first scratch guard | selftest FAIL | a2 side-effect assertion FAIL: `nothing created under /tmp` (the second guard still returned rc=2, so the *rc* check passed — only the directory's existence betrayed it); 18/19 rc=1 | **yes** |
| I6 | delete `[ -L "$SCRATCH" ]` refusal | selftest FAIL | a3 FAIL: `symlinked scratch-root refused (want=2 got=1)`; 18/19 rc=1 | **yes** |
| I7 | default citecheck path `round-65/receipts` → `round-64/receipts` | selftest FAIL | `19/19`, rc=0 | **no** (§3.3) |
| I8 | `[ "$n" -gt 0 ]` → `[ "$n" -ge 0 ]` (accept `--citecheck-paths` with no value) | selftest FAIL | `19/19`, rc=0 | **no** (§3.4) |
| I9 | `USEDBY_SIBLING` → `…/absent-sibling.py` (broken sibling path) | selftest FAIL | `19/19`, rc=0 | **no** (§3.5) |

## 3+. Survivor analysis (a survivor is a coverage gap, not a failed mutant)

**3.1 M2 — equivalent mutant, not a gap.** `rows >= 7` differs from `rows >= 8` only when
`rows == 7`; seven data rows can contribute at most seven distinct first cells, so `groups == 8`
is then unsatisfiable. The two predicates are semantically identical under the frozen
conjunction (`rows>=8 AND groups==8 AND all-resolved AND gate==ok`). No fixture can exist that
distinguishes them. Consequence worth recording: the `rows` leg is **not independently
discriminating** — every case where it matters is already caught by `groups == 8` (extra rows
never fail, missing rows lose a group). The frozen `rows=8` observable in the claim is therefore
carried by the groups cell, and a landed register with 8 rows and a duplicated group is accepted
(`neg-dupgroup` is MET) — which is intended by the frozen predicate (`rows >= 8`), but means the
printed `rows=` number is the only place the duplicate is visible.

**3.2 I1 — a leg can be skipped and still reported `rc=0`; landing goes GREEN.**
Detector: `19/19`, rc=0. Direct probe at `cb63ab13…` (r65 receipts exist; the real citecheck leg
is red because `quality/landing-counters.sh` is not yet in that tree):

```
pristine : LANDING_LEG citecheck rc=1 → MADO_LANDING_COUNTERS: RED  (…citecheck=1…) rc=1
I1       : LANDING_LEG citecheck rc=0 → MADO_LANDING_COUNTERS: GREEN(…citecheck=0…) rc=0
```

Gap: a7 asserts only that a `LANDING_LEG <leg> rc=<digits>` **line** exists; it does not assert
that the leg's child ran or that its rc came from a child. The mutant prints the line without
executing anything. This is the exact r64 class (a producer that never ran reported green) and it
is not caught. Closing assertion type: per-leg invocation witness (a shim/child that writes a
marker under the scratch root, asserted present) or an end-to-end fixture where exactly one known
leg is red and that leg's `rc=` is asserted non-zero.

**3.3 I7 — the default receipt tree can be redirected and landing goes GREEN.**
Detector: `19/19`, rc=0. Direct probe at `cb63ab13…`:

```
pristine (round-65 receipts): MADO_CITECHECK … files=6 citations=10 resolved=9 missing=1
                              verdict=TARGET_MISSED → LANDING_LEG citecheck rc=1 → RED rc=1
I7 (round-64 receipts):       MADO_CITECHECK … files=21 citations=18 resolved=18 missing=0
                              verdict=TARGET_MET  → LANDING_LEG citecheck rc=0 → GREEN rc=0
```

Gap: the selftest's fixture carries only a `round-65/receipts` directory and legs are allowed to
be red, so nothing pins which tree the default path names. Closing assertion type: the fixture
receipt cites a path that exists only in the fixture, and the selftest asserts the fixture
landing's citecheck leg is green (which can only happen if the default path is the fixture's
round-65 receipts).

**3.4 I8 — `--citecheck-paths` with no value is accepted.**
Detector: `19/19`, rc=0. Probe: pristine refuses `rc=2`
(`landing-counters.sh: --citecheck-paths needs at least one PATH`); mutant runs with the default
tree and exits `rc=1` with `MADO_LANDING_COUNTERS: RED …`. Gap: no CLI negative case for the
option. Low severity (it fails red, not green) but the frozen contract names the refusal.

**3.5 I9 — a broken sibling path is invisible to the selftest.**
Detector: `19/19`, rc=0. Probe at `cb63ab13…`: `LANDING_LEG usedby rc=2`,
`MADO_LANDING_COUNTERS: RED (…usedby=2…) rc=1`. Gap: the fixture run's legs may legitimately be
red, so "sibling missing" is indistinguishable from "sibling ran and failed". The same blindness
is visible without any mutation: the unmutated bytes pass `19/19` when copied to a directory whose
`../quality/…` siblings do not exist (`probe-location-blind.log`, rc=0). Closing assertion type:
assert all three sibling paths exist/are executable, and assert a leg that the fixture is built to
satisfy (nav, whose fixture corpus is consistent) actually returns rc=0.

## 4. Verdict

- **C1 counter (A): fails loudly.** 9 of 10 mutants are killed; the single survivor is provably
  equivalent. Every frozen clause (`rows`, `groups`, exact first-cell equality, receipt
  resolution, gate substring, rev-only read, exit code, sentinel boundary, required-group set) is
  independently discriminating under at least one fixture. Caveat: the claim's one-command base
  control kills none of them — discrimination comes from fixtures that do not live in the lane.
- **C2 instrument (B): fails loudly only for arithmetic/guard mutations.** 5 of 9 killed. The four
  survivors include two (`I1`, `I7`) that turn the real landing at `cb63ab13…` from RED into
  GREEN — the instrument's own failure mode — because the selftest checks line shape and rc
  arithmetic, not provenance of each rc or of the receipt tree. `--selftest` is therefore
  necessary but not sufficient evidence for the C2 landing claim.

## 5. Commands and exit codes (evidence)

| command | rc |
|---|---|
| `python3 targets/c1-r65-register.py --repo <lane> --rev 524fa1f9…` (base control) | 1 (TARGET_MISSED) |
| `python3 mut_c1.py` (baseline 11-fixture matrix + 10 mutants; log `evidence/c1-mut.log`) | 0 |
| `python3 targets/c1-r65-register.py --repo fx/pos --rev 61ea1fb6…` | 0 (TARGET_MET) |
| `python3 targets/c1-r65-register.py --repo fx/neg-wt-only --rev 9286e34f…` | 1 |
| `bash targets/landing-counters.sh --selftest --scratch-root …/st/blind` (siblings absent) | 0 (19/19 — location-blind) |
| `bash lab/quality/landing-counters.sh --selftest --scratch-root …/st/baseline` | 0 (19/19) |
| `python3 mut_i.py` (baseline + 9 mutants; log `evidence/instr-mut.log`) | 0 |
| `bash lab/quality/landing-counters.sh --repo <lane> --rev cb63ab13… --scratch-root …` | 1 (RED, citecheck=1) |
| `bash …/I1/… --repo <lane> --rev cb63ab13…` | 0 (GREEN, citecheck "0" never run) |
| `bash …/I7/… --repo <lane> --rev cb63ab13…` | 0 (GREEN over round-64 receipts, files=21) |
| `bash lab/… --citecheck-paths` (no value) | 2 (refusal); I8 mutant: 1 |
| `bash …/I9/… --repo <lane> --rev cb63ab13…` | 1 (RED, usedby=2) |
| `bash -n` on every tested/copied script | 0 |
| earlier instrument revision `55d39b6f…` `--selftest` | 1 (18/19; `a15` + `SW: unbound variable`) — fixed in tested `c12b72e2…` |

## 6. Reproduction inventory (copied into this seat dir before scratch removal)

- `evidence/tested-bytes/` — the exact tested copies + `SHA256SUMS`.
- `evidence/c1-mut/`, `evidence/instr-mut/` are not copied (large); their sha256 list is in
  `evidence/mutant-hashes.txt`, and every patch is the `old → new` string in the harnesses.
- `evidence/harness/{mkfx.py,mut_c1.py,mut_i.py}` — fixture generator and both batteries.
- `evidence/c1-mut.log`, `evidence/instr-mut.log`, `evidence/*probe*.log`,
  `evidence/pristine-selftest.log`, `evidence/base-selftest.log` (failing early revision),
  `evidence/fixture-revs.txt`, `evidence/mutant-hashes.txt`.

Bounds honoured: writes only in this seat dir and `/fast/scratch/hyaku/mado-r65/w1/R65MutCounters/`;
no git mutation in the lane, no pacman, no network, no r56 credential material, no
credential-shaped capture, no compositor/session state touched, no installs needed.
