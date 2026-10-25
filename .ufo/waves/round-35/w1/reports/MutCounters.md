# MutCounters — mutation test of PRED-C1-r35-v1 and PRED-C2-r35-v1 control suites

Seat: MutCounters (mado-r35-w1 leaf). Date: 2026-10-24.
Scratch: `.ufo/waves/round-35/scratch/MutCounters/` (mutant copies + reconstructed c2-donothing fixture).
Frozen originals `c1/count.py`, `c2/count.py`, all `controls/` files were never touched — `git status --short` over `c1/ c2/ controls/ ledger/ fetch/` is empty after the run.

## Setup

Every mutant is a one-line change on a copy of the frozen counter. For c1 the four
ordered mutations map directly. c2's code has no `closed_rows`, no `NF` check and no
`recheck` validator, so each c1 mutation was mapped to its nearest structural analog
in c2 (mapping is a judgment call, stated per mutant). "Controls catch it" is
reported at two granularities:

- **verdict-kill**: the mutant's `verdict=` on the tree differs from the committed
  receipt verdict for that tree (false-accept on a defect tree or false-reject on
  golden).
- **count-kill only**: verdict identical but a reported count differs from the
  committed receipt — the tree detects the mutant only if a judge compares counts,
  not just the verdict.

### Mutants

| mutant | file | change | analog of |
|---|---|---|---|
| c1-offbyone | `scratch/MutCounters/c1/count-offbyone.py` | `closed_rows = 0` → `closed_rows = 1` (seed; count high by 1 everywhere) | ordered |
| c1-nf12 | `scratch/MutCounters/c1/count-nf12.py` | `len(cs) == 11` → `len(cs) == 12` | ordered |
| c1-norecheck | `scratch/MutCounters/c1/count-norecheck.py` | dropped `and valid_recheck(cs[9])` | ordered |
| c1-hash16 | `scratch/MutCounters/c1/count-hash16.py` | `receipt["sha256"] in cs[5]` → `receipt["sha256"][:16] in cs[5]` (left-operand truncation; truncating `cs[5]` instead is outcome-identical since the frozen sha256 occurs verbatim in the anchor cell) | ordered |
| c2-uncplus1 | `scratch/MutCounters/c2/count-uncplus1.py` | `uncovered = 0` → `uncovered = 1` | off-by-one in the scored count |
| c2-toctoumemb | `scratch/MutCounters/c2/count-toctoumemb.py` | `declared == [spec["toctou_clause"]]` → `spec["toctou_clause"] in declared` (equality widened to membership) | widened field-count check |
| c2-noverdict | `scratch/MutCounters/c2/count-noverdict.py` | dropped `not MISSED.search(receipt.read_text())` from the uncovered test (receipt need only exist) | dropped per-row validator |
| c2-hash16 | `scratch/MutCounters/c2/count-hash16.py` | `raw != blob["blob_id"]` → `raw[:16] != blob["blob_id"][:16]` | hash prefix-16 |
| c2-noreason (extra) | `scratch/MutCounters/c2/count-noreason.py` | `if nl and nl.get("reason")` → `if nl` | alternate analog of dropped validator (kept: costs nothing, tests a different clause) |

### Control surfaces

- **c1 suite** = the 11 dirs under `controls/` (`golden` + 10 `c1-*` defect trees),
  run as `python3 -I <mutant> --root controls/<d> --frozen c1/frozen.json`.
- **c2 suite** = (a) the lane repo root `--repo .` with frozen spec (the implicit
  "golden"), and (b) `controls/c2-donothing.txt`'s fixture — a scratch frozen spec
  whose `clause_ledger` points at a scratch `clauses.json` with `entry-regular`
  stripped of its `control` key. That fixture's original location
  (`/fast/scratch/mado-r35/c2-donothing/`) no longer exists; I reconstructed it at
  `scratch/MutCounters/c2-donothing/`. Replayed through the original counter it
  prints `uncovered=1 retired=1 toctou_declared=1 ledger_tip_ok=1 TARGET_MISSED
  exit=1`, matching the committed receipt byte for byte.
- c2 was also run with `--repo controls/<d>` for all 11 c1 trees, as the task
  asked: every run — original and all mutants — dies `error=clause-ledger-missing
  exit=2`. The c1 control trees carry no `c1/clauses.json`, so they have zero
  discriminative power over c2 (not even the original passes them).

## Results — c1 mutants × control trees

Baseline (original `count.py`) reproduced all committed receipts exactly:
`golden` MET (3/8/0), every `c1-*` MISSED, `c1-donothing` (0/0/8), all others (2/7/1).

| control | offbyone | nf12 | norecheck | hash16 |
|---|---|---|---|---|
| golden | **KILL-V** (MISSED, rows=9) | **KILL-V** (MISSED, 0/0/8) | pass (MET, correct) | pass (MET, correct) |
| c1-digest | KILL-C (8 vs 7) | KILL-C | pass (2/7/1 MISSED) | pass (2/7/1 MISSED) |
| c1-donothing | KILL-C (1 vs 0) | pass (0/0/8 identical) | pass | pass |
| c1-entry-symlink | KILL-C (8 vs 7) | KILL-C | pass | pass |
| c1-quote-absent | KILL-C (8 vs 7) | KILL-C | pass | pass |
| c1-quote-long | KILL-C (8 vs 7) | KILL-C | pass | pass |
| c1-recheck-prose | KILL-C (8 vs 7) | KILL-C | **KILL-V** (MET, false accept) | pass |
| c1-row-duplicate | KILL-C (8 vs 7) | KILL-C | pass | pass |
| c1-row-extra-field | KILL-C (8 vs 7) | KILL-C (nf12 passes the 12-cell row but shifted cells still fail) | pass | pass |
| c1-status-queued | KILL-C (8 vs 7) | KILL-C | pass | pass |
| c1-usedby-extra | KILL-C (8 vs 7) | KILL-C | pass | pass |

Kill score (verdict-level): **offbyone 1/11, nf12 1/11, norecheck 2/11, hash16 0/11 → hash16 SURVIVES the entire c1 suite.**
Count-level: offbyone detected 11/11, nf12 10/11 (invisible to c1-donothing), norecheck 1/11, hash16 0/11.

## Results — c2 mutants × control surfaces

Baseline reproduced: lane-root `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 MET`,
reconstructed c2-donothing fixture `uncovered=1 … MISSED`.

| surface | uncplus1 | toctoumemb | noverdict | hash16 | noreason |
|---|---|---|---|---|---|
| lane-root (golden) | **KILL-V** (MISSED, unc=1) | pass (MET) | pass (MET) | pass (MET) | pass (MET) |
| c2-donothing fixture | KILL-C (unc=2 vs 1) | pass (1/1/1/1 MISSED) | pass | pass | pass |
| all 11 `controls/` dirs | exit=2 ledger-missing — no discrimination, same as original | same | same | same | same |

Kill score: **1/5 mutants killed (uncplus1, by the lane-root baseline only); the
committed c2 control (c2-donothing) kills 0/5 at verdict level and 1/5 at count
level.** No committed control produces MET, so there is no c2 "golden" that a
too-strict mutant could trip on; conversely no fixture exercises `retired`,
`toctou_declared` or `ledger_tip_ok` failure modes, so too-lenient mutants sail
through.

## Findings — is the control set strong enough?

**c1 suite: strong for lenient-field mutants, one demonstrated hole.**

- 3/4 mutants verdict-killed; each targeted clause control does its job
  (`c1-recheck-prose` alone flips for `norecheck`).
- `hash16` survives: `c1-digest` poisons the whole anchor sha256 with
  `0000…0000`, so any comparator that still inspects the first 16 hex chars keeps
  failing. A control whose anchor shares the true digest's first 16 chars but
  diverges after would kill it. Cost: one row edit in a new control tree.
- **Incidental defect (report, not fix — file is frozen):** `c1/count.py:174`
  computes `digest = hashlib.sha256(blob).hexdigest()` and never uses it. The
  anchor check is `receipt["sha256"] in cs[5]` — registry text vs frozen text.
  Receipt *bytes* are never hashed. A control whose receipt file contains wrong
  bytes (while the anchor still claims the right sha) would score closed today.
  Consequence for the hash16 mutant: `cs[5][:16]`-style right-side truncation is
  equivalent on this suite only because the anchor embeds the frozen hash
  verbatim.
- Both too-strict mutants (`offbyone`, `nf12`) are caught at verdict level only by
  `golden`; the negative controls detect them only in the counts. If verdict alone
  gates promotion, a too-strict counter regresses to "all trees MISSED" and is
  indistinguishable from a merely correct one on defect trees — count-equality
  receipts are what keep that signal.

**c2 suite: weak — one fixture, four unchecked failure modes.**

- `c2-donothing` only exercises `uncovered` via a control-less clause. Nothing in
  the committed suite can produce `retired≠1`, `toctou_declared≠1`, or
  `ledger_tip_ok=0` while holding the others at target, so `toctoumemb`,
  `hash16`, `noreason` and `noverdict` all survive verdict-level.
- Cheapest kills missing: a scratch ledger keeping a retired id live (`retired=0`),
  a scratch ledger adding a second `not-load-bearing` clause
  (`toctou_declared=0` under the correct counter; the `toctoumemb` mutant would
  print 1 — the only mutant that fixture distinguishes), a frozen spec with a
  corrupted `frozen_blobs` entry or missing ledger doc (`ledger_tip_ok=0`), and a
  control receipt file lacking `verdict=TARGET_MISSED` (`uncovered=1` under the
  correct counter, `0` under `noverdict`).
- The c1 `controls/` trees are dead weight against c2: uniform
  `clause-ledger-missing` exit=2 before any predicate logic runs.

## Commands

```
python3 -I scratch/MutCounters/c1/count-<m>.py --root .ufo/waves/round-35/controls/<d> \
        --frozen .ufo/waves/round-35/c1/frozen.json
python3 -I scratch/MutCounters/c2/count-<m>.py --repo {.|<tree>} \
        --frozen {.ufo/waves/round-35/c2/frozen.json|scratch/MutCounters/c2-donothing/frozen.json}
```

All output above is from runs executed in this session on 2026-10-24; baselines
reproduced the committed receipts (`controls/*.txt`) verbatim.

Tooling: none installed (stdlib python3, coreutils only).
