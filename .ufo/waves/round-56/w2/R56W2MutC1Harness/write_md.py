#!/usr/bin/env python3
"""Write mutants.md (table generated from classes.json and drive.M) into the deliverable directory."""
import json
import sys
from pathlib import Path

SCR = Path("/fast/scratch/hyaku/mado-r56/R56W2MutC1Harness")
sys.path.insert(0, str(SCR))
import drive  # noqa: E402

DEST = Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w2/R56W2MutC1Harness")
cls = json.loads((SCR / "receipts" / "classes.json").read_text())
C = cls["classes"]
NAMES = {"K-spec": "killed (spec oracle)", "K-extra": "killed (extra oracle)", "K-fix": "killed (fixture)",
         "W": "SURVIVED verdict, wrong reason", "D": "diagnostic only", "E": "equivalent (argued)"}


def clip(s, n=96):
    s = s.replace("|", "\\|").replace("\n", "\\n")
    return s if len(s) <= n else s[: n - 3] + "..."


rows = []
for mid, kind, desc, old, new in drive.M:
    c = C[mid]
    why = c["detail"] if c["category"] in ("K-spec", "K-extra") and c["detail"] else c["oracle"]
    if c["category"] in ("K-spec", "K-extra", "K-fix", "W", "D"):
        why = ("first differing oracle: `%s`. %s" % (c["oracle"], c["detail"])) if c["detail"] else \
            ("fixture `%s`" % c["oracle"] if c["category"] == "K-fix" else c["oracle"])
    if mid == "M26":
        old, new = '" The value is capped at 200 by this call."', '" The value is capped at 2 by this call."'
    rows.append("| %s | %s | %s → %s | %s | %s |" % (mid, kind, clip(old, 60), clip(new, 60), NAMES[c["category"]],
                                                  clip(why, 300)))

counts = cls["counts"]
md = f"""# R56W2MutC1Harness — mutation test of `quality/r56_ctl_c1.py` at `28fc86ac2359ec27406d8a2c63bef82ea6e947ed`

Seat: R56W2MutC1Harness (wave 2, falsify). Subject: the C1 control harness (`quality/r56_ctl_c1.py`, 632 lines, the twelve
controls of `registration.md` §C1 as amended by `registration-v2.md` E5, the good-tree judgement, the denominator). The
counter under test is `quality/counters/c1-r56-autoreload-entry.py` at the same revision (git blob `5290d681…`, read via `git archive`). Nothing in the lane was edited; every mutant lives in a copy under
`/fast/scratch/hyaku/mado-r56/R56W2MutC1Harness/` (removed before yield, copied here first).

## Result in one table

| measure | value |
|---|---|
| mutants (one-line edits of a copy of the harness module) | {cls['mutants']} |
| oracle runs per mutant (battery) | {cls['oracles']} (listed below) |
| killed (stdout or exit status differs from the pristine harness) | {cls['killed']} = {cls['kill_rate_all']*100:.1f}% of all |
| … of which killed by the three oracles the spec names (real counter, always-green stub, reject-all stub) | {cls['killed_by_spec_oracles']} |
| argued equivalent (no oracle differs; reason in the table) | {counts.get('E', 0)} |
| diagnostic-only (stderr notes or print width; verdict identical; not a control defect) | {counts.get('D', 0)} |
| verdict-relevant, non-equivalent | {cls['verdict_relevant_nonequivalent']} |
| kill rate excluding equivalent | {cls['kill_rate_excl_equiv']*100:.1f}% ({cls['killed']}/{cls['mutants']-counts.get('E',0)}) |
| kill rate excluding equivalent and diagnostic (the honest denominator) | {cls['kill_rate_excl_equiv_and_diag']*100:.1f}% ({cls['killed']}/{cls['verdict_relevant_nonequivalent']}) |
| spec-only oracles on the honest denominator | {cls['spec_only_kill_rate_on_verdict_relevant']*100:.1f}% ({cls['killed_by_spec_oracles']}/{cls['verdict_relevant_nonequivalent']}) |
| verdict-level survivors (wrong-reason controls) | {counts.get('W', 0)}: M23, M24, M25, M58, M60 |
| with P1 (pinned missed sets) — the five verdict-level survivors killed (verified); the other 44 are killed by the battery already | 5 of 5 survivors killed |

Read the honest denominator, not the all-mutant rate. Two numbers the frozen battery does not reach on its own:
the three spec oracles kill half of the verdict-relevant mutants; the rest need the extra oracles and fixtures below.

## Oracle battery (40 runs per mutant)

- `real`: the real counter exported at the revision, run through the unchanged harness (no `--counter`).
- `stub_green` (always green, TARGET_MET with the full counts), `stub_reject` (TARGET_MISSED, `index`), `stub_kitchen`
  (TARGET_MET with every registered leg, rc 1). The first two are the spec's oracles; the third is mine.
- 21 further stubs (`stub_legonly_*`, one leg each, with the count of controls each should pass pre-computed from the
  control table; `stub_malformed_leg`, `stub_newrows390`, `stub_green{{badrev,badcount,missed}}`).
- 9 wrappers `w_*` that run the REAL counter and forge one property: rev, exit 0 on a miss, exit 2 on a miss, duplicate
  stdout line, stderr noise on a green run, content 33/33, verdict word `TARGET_MAYBE`, rows denominator `/31`, and the
  good tree alone broken (`w_goodonly`). `w_stderr` is benign and the pristine harness correctly scores it `12/12 OK`
  (the registration only mandates "reason on stderr" on the exit-2 path).
- 6 variant trees (good tree with one entry edit): fenced copy of K05 (`var_fence3`), 4-space fence (`var_fence4`),
  `~~~` fence containing a ```` ``` ```` line (`var_tilde`), duplicated K05 row (`var_dupK05`), closed HTML comment on K05
  (`var_comment`), K05 with a sixth cell (`var_6cell`).
- Pristine expectations, checked: real `good=ok controls=12/12 verdict=OK`, rc 0; green `good=ok controls=0/12 verdict=FAIL`;
  reject `good=bad controls=0/12 verdict=FAIL`. Deterministic across two runs (stdout and stderr byte-identical).
- Classification: KILLED if stdout or exit status differs from the pristine run of the same oracle (SHA values in
  stderr normalized to `<SHA>`, since scratch commits are timestamped); DIAG if only stderr differs; SURVIVED otherwise.

Fixtures added after the battery (run in `extra_variants.py`, differential against pristine):
`var_srcline2` (the `source:` line moved to line 2) kills M63; `var_pinlink` (the pinned `Hyprland-ConfigWatcher.cpp` made a
symlink) kills M15 and M16.

## Mutants and their outcomes

Each row is one line of a copy of `quality/r56_ctl_c1.py`. Multi-line `old` anchors (M21, M40, M44, M45) exist only for
uniqueness; the replacement changes one line. The `old` text occurs exactly once in the pristine module (asserted by
`drive.py`). M26 changes a constant inside the appended proposition text.

| id | kind | edit (old → new) | outcome | killing oracle / argument |
|---|---|---|---|---|
{chr(10).join(rows)}

## Survivors, in full

### W — verdict-level survivors (controls still `ok`, for the wrong reason). Non-equivalent.

- **M23** `_join` separator `" | "` → `" |"`. Every row the harness rewrites becomes malformed, so the counter reports
  `row:<id>` for rows the control never touched: control 2 misses `row:K01…` (+57 more), control 3 misses `row:K04,num:K04`.
  Verdict unchanged. *Proposal P3* (row-grammar legs only for the mutated row) → `controls=7/12`, verified.
  *P1* → `7/12`, verified.
- **M24** junk text for K rows changed from `placeholder proposition text …` to `placeholder host proposition K.., not a
  read`. Stronger, not weaker: it exposes a hole in the frozen control 2. The pristine junk text shares the identifier
  `source` with K23's quote (`source= skipping directory {{}}`), so K23 gets no `tok:` leg. Pristine control 2 pins 32 of 33
  tok legs; M24 pins 33. Verdict unchanged. *P1* → `11/12`, verified. The root-cause fix (token-disjoint junk text, the
  M24 text) is verified by the M24 receipts: 33/33 tok legs, verdict unchanged.
- **M25** junk applied to K rows only (`for rid in ctx["k_ids"]`). Control 2 no longer asserts that H01–H03 are unreadable.
  Verdict unchanged. *P4* (`tok:H01`, `tok:H02`, `tok:H03` required in control 2) → `controls=11/12`, verified (the pristine
  run keeps `12/12`). *P1* → `11/12`, verified. M24 is not killed by P4 (correct: it flags H rows too).
- **M58** quote-echo threshold `>= 30` → `>= 31`. K07's quote is exactly 30 characters, so K07 is not echo-mutated, and
  control 11 still passes on the other rows. *P2* (`echo:K07` required in control 11) → `controls=11/12`, verified. *P1* → `11/12`.
- **M60** H placeholder text identical for every H row (`"placeholder host proposition, not a read"`). Duplicate
  propositions make the counter report `row:H01,row:H02,row:H03`. Verdict unchanged. *P3* → `11/12`, verified. *P1* → `11/12`.

### D — diagnostic only (not verdict-relevant)

- **M55** `_expected_leg` collateral allowance removed; affects only the `note:` line on stderr.
- **M56** `_clip` width 8 → 1; affects only how many legs are printed.
  Neither changes a control's pass/fail. They are listed, not counted as survivors. P1 correctly does not kill them.

### E — equivalent (argued; every oracle identical)

- M01 (`CHILD_TIMEOUT` 120 → 1): the unloaded counter run takes 0.18 s; the battery ran 12 parallel jobs and no receipt has a
  TIMEOUT. A deadline hazard on a slow host, not a control weakness. Equivalent on this host only.
- M05, M12, M13, M17, M54: equivalent for every input (argument in the table).
- M14, M57: equivalent for every accepted input. M14: the tables file must be a regular blob before export. M57: the
  tables sha is checked first, so `k=30, h=3` always.
- M27, M29, M31, M32, M35, M59, M65: a different instance of the same defect class (another pin's row, another
  status, another quote character, another pinned file, another past-EOF number). The counter's legs are identical in
  every oracle.

M15, M16 and M63 were equivalent on the frozen tree but are not in general; they are killed by fixtures (above).

## Proposed additions, each verified

Every proposal is a text insertion into the harness module (`verify_props.py`). Verification means: (a) the pristine
harness with the addition still scores `good=ok controls=12/12 verdict=OK`, rc 0, on the real counter; (b) the survivor
with the addition scores FAIL on the same counter.

| proposal | what it adds | pristine | survivors killed (verified) | survivors not killed |
|---|---|---|---|---|
| P1 pinned missed sets | each control's full missed set must equal the one recorded from the pristine run on the real counter (`gold.json`) | 12/12 | M23 (7/12), M24 (11/12), M25 (11/12), M58 (11/12), M60 (11/12) | M55, M56 (diagnostic) |
| P2 `echo:K07` | control 11 must see the 30-character quote row's echo leg | 12/12 | M58 (11/12) | M23, M24, M25, M60 |
| P3 row locality | a control may report `row:` legs only for the row it mutates (7 → K17, 8 → K05) | 12/12 | M23 (7/12), M60 (11/12) | M24, M25, M58 |
| P4 H rows junked | control 2 must see `tok:H01..H03` | 12/12 | M25 (11/12) | M23, M24, M58, M60 |
| fixture `var_srcline2` | `source:` on line 2 (window-dependent) | 12/12 | M63 (11/12) | — |
| fixture `var_pinlink` | pinned `ConfigWatcher.cpp` is a symlink | 10/12 (good=bad) | M15 (good=ok, 12/12), M16 (11/12) | — |

Smallest per survivor: M58 → P2; M23, M60 → P3; M25 → P4; M24 → the token-disjoint junk text (root cause, verified by the
M24 receipts) or P1; M23/M58/M60 also by P1. The P1 golden is pinned to this counter's output, so a legitimate counter
change must regenerate it (maintenance cost, stated).

## Findings the survivors point to (not counted as kills)

1. **Control 2 has a lexical hole at K23** (verdict-neutral): the junk proposition shares `source` with K23's quote.
   Verified by `final_table.py` (`control2_no_tok_rows: ["K23"]`) and M24.
2. **Five controls pass on the wrong reason** (M23, M60, plus partial vacuity in M24, M25, M58): their verdict cannot tell
   a row-grammar fault or a duplicate-proposition fault from the intended defect.
3. **The registration's collateral lists are incomplete**: the pristine harness prints `note: collateral legs beyond the
   registered ones` for controls 4, 5, 7, 8, 10, 11, 12 (e.g., control 7 adds `source_cell:K17, scope:K17, tok:K17, num:K17,
   echo:K17`). Cosmetic for the verdict, a documentation gap for the registration.
4. **Stderr from the counter is not judged on a green run** (`w_stderr` → `12/12 OK`). The registration does not require it;
   noted, not a defect.
5. **The denominator guard is needed**: M47 (`and` → `or` in the OK verdict) prints `good=ok controls=0/12 verdict=OK` on the
   always-green counter. The frozen harness prints FAIL there, which is the spec's requirement and holds.

## Limits

- The 66 mutants are a sample of one-line edit classes (operator, off-by-one, constant, regex, dropped leg, inverted test,
  removed guard, swapped arguments), not an exhaustive enumeration. Kill rates describe this sample.
- The extra oracles (kitchen-sink, single-leg stubs, wrappers, variant trees) are mine. The frozen harness has no control
  for them; the verdict-relevant kill rate counts them separately so the spec-only figure is visible.
- Proposals were verified on the real counter's tree (pristine), and each survivor was checked with its addition. The
  proposal runs were not repeated on all 40 oracles.
- Equivalence is argued for this counter and this tree, not proved for all counters.
- No counter was modified; the counter is read as written.

## Reproduce

```
cd /fast/scratch/hyaku/mado-r56/R56W2MutC1Harness      # scratch; copies of the scripts in this directory
python3 -I gen_stubs.py stubs                           # 24 stubs
python3 -I drive.py                                     # 66 mutants x 40 oracles (JOBS=12, ~20 min on 32 cores)
python3 -I final_table.py                               # receipts/classes.json
python3 -I extra_variants.py                            # var_srcline2, var_pinlink (fixtures)
python3 -I verify_props.py M23 M24 M25 M58 M60 M55 M56  # P1, P2, P3 matrix
python3 -I verify_p4.py                                 # P4 (H rows junked)
python3 -I write_md.py                                  # this file
```

The per-oracle receipts are in `receipts.tar.gz` (`receipts/<MUTANT>/<oracle>.{{out,err,rc}}`, `receipts/PRISTINE/`),
`receipts/run-full.log`, `receipts/summary.json`, `receipts/classes.json`; the proposal runs are in `proposals/`.

## Host and tooling

No tool was installed or upgraded. Python 3.14.8 and git 2.56.0 were used as present. No `sudo`, no `pacman`, no
compositor or service change; nothing under `~/.config` or `~/.local` was written.
"""
(DEST / "mutants.md").write_text(md)
print("wrote", DEST / "mutants.md", len(md), "bytes")
