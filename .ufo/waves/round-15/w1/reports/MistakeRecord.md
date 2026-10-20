# MistakeRecord — round 15 / w1 — report (revised after AttackMistake C1–C6)

Seat: `MadoR15.MistakeRecord` (scribe, leaf; no delegation, no background jobs).
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Axis: **coverage** (mistake-row drafting for the R14-V1 correction). No axis verdict is issued.
Milestone context: U6 input evidence ladder and R14 ancillary provenance correction. No U6 content is drafted here.

## Outcome

- Drafted the R14-V1 mistake row (§1) for L1 integration. It is not written into `corpus/`; L1 owns the lesson and registry files.
- Revised after `MadoR15.AttackMistake` (C1): the previous green fixture header (`measured_commit 32118fc…`, `gate_sha256 fba82a66…`, `input_binding committed`) **must not** be applied to the three R14 receipts. Those runs finished at 05:58–06:01Z, before commit 32118fc at 06:03:28Z, and read raw gates `ef50e262…` / `d6d5eb27…`, not `fba82a66…`. The fix now uses a separate `derived_from` relation and never restates these receipts' headers.
- Revised the static header check (§3) to bind future standalone mutation receipts by `measured_commit`, `derived_target_sha256` and `spec_sha256` (C3). The full-gate `gate_sha256` is not a mutation-receipt requirement.
- No file was written except this report. No commit, test, lint, formatter, build, smoke run or live probe. No input event was read. No credential or `agent.db*` file was opened.
- Tooling record: no installs or upgrades. `python3` standard library only, run in-process through the eval kernel as a read-only text check.

## 1. Mistake row (draft for L1)

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| R14-V1 | ancillary receipt precision / provenance binding: standalone mutation receipts carry a provisional worktree input binding, whole-gate digests that are not the committed gate, and no measured-commit or derived-target binding, so they cannot be read as standalone final-gate receipts | `corpus/lessons/round-14-verifier-spotcheck.md:169` (outside R14-V1 route); `.ufo/waves/round-14/evidence/regression-recut.txt:3-4`, `regular-target-mutants.txt:3-4`, `retained-census-mutants.txt:3-4` (`input_binding: provisional worktree snapshot`; `gate_sha256` `ef50e262…` / `d6d5eb27…`; no `measured_commit`); `MUTATE_TARGET` `sha256=cd1d73d7…` in all three. Pre-commit timing and object-store facts: `.ufo/waves/round-15/w1/reports/AttackMistake.md` F1–F3, F7. | Outside non-author verifier, round 14 (hyaku closure). Existing criteria already state the rule: QUALITY 7 (label work-window hashes provisional **and re-bind them at the commit**; the provisional label is present, the re-bind is absent), QUALITY 9 (bind verdict to commit/frozen sha), QUALITY 13 (outliving evidence is a committed path). Application gap, not a missing criterion; no new numbered criterion. | Append-only correction in a new file (for example `.ufo/waves/round-15/receipt-correction.json`); no receipt or TSV bytes change. Per the attack's acceptance list: (1) map each receipt separately with its literal header value and MUTATE_DATE; (2) state that these runs predate the commit, so no `measured_commit` is assigned; (3) record `cd1d73d7…` as `derived_from: excise(git show 32118fc:tools/mado-verify.sh)`, re-derived later and not measured at the commit; (4) cite the 22 TSV mutant-hash re-derivation as the spec and mutant binding; (5) list the four excised ranges exactly (R7-SELFTEST `:440-619`, R8 `:1368-1531`, R7-REGRESSION `:1543-1983`, R8 `:1984-2506`) and note that `MADO-R8-OMARCHY-BLOCK` (`:622-801`) is not excised; (6) keep the original sha256 anchors as `subject_sha256`. Raw gates `ef50e262…`, `d6d5eb27…` and `fba82a66…` are recorded as distinct, with the unrecoverable pre-commit states stated as such. Future standalone mutation receipts bind `measured_commit`, `derived_target_sha256` and `spec_sha256` and pass the §3 check. No generic wrapper. |

Admission note: the lesson says the route is status-neutral and admission does not require rewriting these records. This row does not reopen C2 kill counts and asserts no measurement at 32118fc.

## 2. Evidence read (static, read-only)

- `round-14-verifier-spotcheck.md:169` routes R14-V1 and names the three receipts; kill counts and C2 remain verifiable through the `MUTATE_TARGET` derived target.
- Headers at lines 1–9 of each receipt: `regression-recut.txt` (`input_binding: provisional worktree snapshot`, `gate_sha256: ef50e262…`, MUTATE_DATE 05:58:44Z); `regular-target-mutants.txt` (`d6d5eb27…`, 06:00:23Z); `retained-census-mutants.txt` (`d6d5eb27…`, 06:01:00Z). None has a `measured_commit:` line. All three have `MUTATE_TARGET: … sha256=cd1d73d7…`.
- Contrast: `round-14/evidence/gate-selftest.txt:3-4` carries `measured_commit: 32118fc1…` and `gate_sha256: fba82a66…` as a whole-gate receipt. That shape is correct for the full gate and is not a template for mutation receipts.
- AttackMistake F1–F10 (its recomputation, adopted here and **not independently recomputed** by this seat): the committed gate is `fba82a66…` at 32118fc; neither provisional gate digest exists in the object store; excision gives `cd1d73d7…`; all 22 TSV mutant shas re-derive from it; the receipts and TSVs are unchanged since 32118fc.

## 3. Static receipt-header check (revised)

Scope: three header facts for **future** standalone mutation receipts. It reads one file, writes nothing and runs no gate. It is not applied to the three R14 receipts as a passing binding.

```python
import pathlib, re, sys

CHECKS = {
    "measured_commit": r"^measured_commit: [0-9a-f]{40}$",
    "derived_target_sha256": r"^derived_target_sha256: [0-9a-f]{64}$",
    "spec_sha256": r"^spec_sha256: [0-9a-f]{64}$",
}
bad = False
for p in sys.argv[1:]:
    t = pathlib.Path(p).read_text()
    miss = [k for k, rx in CHECKS.items() if not re.search(rx, t, re.M)]
    print(f"RECEIPT_HEADER {p}: " + ("FAIL missing=" + ",".join(miss) if miss else "PASS"))
    bad |= bool(miss)
sys.exit(1 if bad else 0)
```

Observed in this seat (static read; same logic inlined through the eval kernel, no file written):

```text
RECEIPT_HEADER regression-recut.txt: FAIL missing=measured_commit,derived_target_sha256,spec_sha256
RECEIPT_HEADER regular-target-mutants.txt: FAIL missing=measured_commit,derived_target_sha256,spec_sha256
RECEIPT_HEADER retained-census-mutants.txt: FAIL missing=measured_commit,derived_target_sha256,spec_sha256
RECEIPT_HEADER in-memory-shape-fixture: PASS
```

The fixture uses zero/placeholder digests (`0`×40, `c`×64, `d`×64). It is a shape-only synthetic input, not a measurement, and it is not written into any receipt. The check's failure on the three R14 receipts is the intended result: their headers are not restated to satisfy it. The process exit code was not separately observed; the script as written exits 1 on any FAIL.

## 4. Limits

- The check tests shape only. It does not verify that a `derived_target_sha256` equals `excise(git show <measured_commit>:tools/mado-verify.sh)`, or that a `spec_sha256` matches the spec bytes. A value-level check of that kind belongs to L1 or a future harness step.
- The check does not verify GREEN, KILLED or RESTORE verdicts. Those remain observations from the historical run.
- The check omits `harness_sha256` (AttackMistake C3 names it). The harness sha is not left unbound: each R14 receipt's stdout carries `MUTATE_TOOL: … sha256=75ed934d…` (receipt line 6), and that is the value a future receipt should carry. The check is not extended to it here; L1 may add `harness_sha256` to `CHECKS` if it promotes the check to a standing gate.
- The previously proposed `gate_sha256 == git show …|sha256sum` value check is **withdrawn** for mutation receipts (AttackMistake C3). It is correct only for whole-gate receipts such as `gate-selftest.txt`.
- The three R14 receipts remain unbound by header. Their binding is the separately recorded `derived_from` relation plus the 22 TSV re-derivations (AttackMistake F5), not a header.
- The proposed `measured_commit` / `derived_target_sha256` / `spec_sha256` header names are proposals, not existing repository conventions. L1 should confirm them before citing.

## 5. Recommended follow-up for L1 (not done here)

1. Write the R14-V1 correction as a new append-only file that meets the seven acceptance conditions in `AttackMistake.md:54-61`. Do not edit the receipts or TSVs.
2. Do not add a numbered criterion. QUALITY 7/9/13 cover the rule.
3. Promote the header check to `tools/` only if L1 wants it as a standing gate; a wave-local script is not a standing gate.

## 6. Sources and files

- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-14-verifier-spotcheck.md:169` — R14-V1 statement.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-14.md:16-17, 184-187` — M3 header audit and the red/green pattern.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md:12-16, 57-60` — criteria 7, 9, 13 and the R13-V2/V3 note.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/evidence/{regression-recut,regular-target-mutants,retained-census-mutants}.txt:1-9` — the three receipt headers read.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/evidence/gate-selftest.txt:1-4` — whole-gate header shape (not a mutation-receipt template).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/AttackMistake.md` — C1–C6, F1–F10 and acceptance conditions, adopted from its recomputation.

Files written by this seat: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/MistakeRecord.md` (this report) only.
