# R56W3MutC2Harness — wave 3 (falsify): mutation test of the C2 control harness

Attacked item: the C2 harness as landed at the lane tip `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` —
`quality/r56_ctl_c2.py` (sha256 `080d7720…2923e`) and its dispatcher `quality/check-r56-controls.py`
(sha256 `e34ef1b9…489f2e`). Question: the artifacts landed once and their harness runs are the only kill
evidence — does that run actually kill one-line defects in the harness itself?

## Result in one paragraph

46 one-line mutants (staging-path swaps 10, sandbox-flag drops 11, expectation inversions 10, denominator
changes 12, dispatcher 3; one ambiguous anchor re-anchored and re-run) went through an 11-probe battery: the
frozen claim's own observables (green line + rc 0 on the honest exported tool copy; no-bwrap fail-closed
refusal; degraded `--no-sandbox` must report `sandbox=none`), eight discrimination probes (cheat tool, broken
tool, wrong-rc tool, tampered fixture note, tampered hold-out note, three over-answering control stubs), and
work-dir leftover diagnostics. **41 of 46 are killed (89.1 %)** — 31 by the claim's own evidence, 7 only by
added discrimination probes, 3 only by E10 leftovers. **5 survive**, of which 4 are non-equivalent sandbox-flag
drops (B01/B04/B05/B09) with verified killing additions, and 1 (S05) is argued equivalent. No pristine-harness
defect was found; the findings are coverage gaps in the frozen predicate, one pristine E10 residue, and one
wording mismatch, all routed.

Full write-up, the 46-row table, per-mutant receipts and the verified proposals:
`.ufo/waves/round-56/w3/R56W3MutC2Harness/mutants.md` (+ `receipts/`, `driver.py`, `verify2.py`, `classify.py`).

## What I did (commands and decisive output)

```
S=/fast/scratch/hyaku/mado-r56/R56W3MutC2Harness   D=<…>/w3/R56W3MutC2Harness
python3 -I $D/driver.py   $S $D    # 46 mutants x 11 probes, 6 workers, ~4.5 min
python3 -I $D/verify2.py  $S $D    # E09 rerun (fixed anchor) + proposal verifications -> ALL PROPOSAL CHECKS: PASS
python3 -I $D/classify.py $D       # -> KILLED-ORACLE 31 / KILLED-EXTENDED 7 / KILLED-DIAGNOSTIC 3 / SURVIVED 5
```

Method: `git archive 0f3a5436…` into a fresh scratch repo (toplevel asserted, identity `ctl`), nine probe commits
each = base + one change, two bwrap-hidden invocation modes (private mount namespace, `mount --bind /dev/null
/usr/bin/bwrap`; host untouched, verified), every mutant applied to a fresh COPY of the harness in scratch, every
probe compared with the pristine harness's observable on the same probe. Pristine baseline (the seat's oracle):

```
MADO_R56_C2: rev=df3285c9… fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET  rc 0
no-bwrap:    rc 2, stdout empty, stderr "setup error: bwrap is not installed: …"
degraded:    same green line, stderr "r56_ctl_c2: sandbox=none …"
```

Restoration evidence: the lane files are byte-identical to the tip blobs (sha256 above, both match
`git show 0f3a5436:<path>`), `git status --porcelain --untracked-files=no` in the lane is empty; scratch was
removed after the deliverables were copied. Tools installed: none.

## Defects (input that shows each + severity)

| id | finding | verified kill (mutant → input → pristine vs mutant) | severity |
|---|---|---|---|
| D1 | control bounds are loose and there are no negative controls: D06 (`<=1`→`<=2`), D07 (`==0`→`<=1`), D09 (`==18`→`>=17`) keep the green line; D12 (drop `ctl_ok==4`) too | P7b/P7a/P7c: a stub answering 2 / 1 / 17 makes pristine `controls=3/4 TARGET_MISSED` and the mutant `4/4 TARGET_MET` | weakens the claim |
| D2 | the commitment terms are invisible on the clean tree: D10 (drop `ho_commit=="ok"`), D11 (drop `fx_ok`) keep the green line | P8/P6: one appended byte in H01/F01 `note.txt` → pristine `holdout_commit=bad`/`fixture_commit=bad` TARGET_MISSED, mutant TARGET_MET | weakens the claim |
| D3 | the exit-status comparison is invisible: E10 (drop `rc == exp_rc`) keeps the green line — no fixture's expected.rc differs from the honest tool's rc | P9: a tool printing F01's expected bytes but exiting 1 → pristine 0/18, mutant 1/18; PR-wrong-rc: a fifth control replaying F02's out with rc 1 (expected to pass 0) → pristine `controls=5/5 TARGET_MET`, E10 `4/5 TARGET_MISSED` | weakens the claim |
| D4 | sandbox-flag drops B01/B04/B05/B09 are invisible to every fixture and control (green line + refusal + degraded token all unchanged) | jail-shape probe: B01 shares the host network namespace (`ifaces=['lo','enp7s0','docker0',…]`), B04 leaves cwd=`/`, B05 drops `/lib`, B09 has no in-jail observable; PR-jail (self-probe the jail, fail closed on deviation) → pristine TARGET_MET, B01/B04/B05 TARGET_MISSED; PR-argv (assert `--die-with-parent`/`--unshare-all` in the built argv) → pristine TARGET_MET, B09 rc 2 | weakens the claim (isolation guarantees unpinned) |
| D5 | pristine E10 residue: the fail-closed refusal path leaves `stage-1/` (a copy of the committed fixture tree) and `cwd-1/` in `--work` (per-fixture cleanup is skipped when `staged_run` raises) | observed on the pristine P2 run | cosmetic |
| D6 | per-fixture stage/cwd cleanup (S08/S09) is invisible to the claim line; only work-dir leftovers reveal it | leftover listings on 10 probes | cosmetic |
| O2 | the wave-3 dispatch wording "run without bwrap: must refuse with sandbox=none" does not match the landed text: the refusal prints `setup error: bwrap is not installed…` (no `sandbox=` token); `sandbox=none` appears only on the waived `--no-sandbox` path | pristine P2/P3 receipts | cosmetic / documentation |

D1–D4 are round-57 material: the claims, counters, kill rules and targets are frozen, so none of the verified
proposals (three negative control stubs, a wrong-rc control, a commitment tamper self-check, a jail-shape
self-probe, a sandbox-argv assertion) is applied to the lane.

## Not verified / limits

- One host only (bwrap 0.13.1, python 3.14.8); hosts without user namespaces untested. The no-bwrap probes are
  mount-namespace simulations, not a bubblewrap-less host.
- The proposal patches are scratch simulations; PR-wrong-rc's denominator bump (`controls=4/4` → `5/5`) is itself
  a registration change round 57 would have to freeze.
- S05's equivalence is argued (code reading + identity on all 11 probes), not an exhaustive input differential.
- B09's parent-death behaviour was not executed (operator stop: no further target execution); only the in-jail
  shape and the argv assertion are evidenced.
- Tool semantics (`tools/mado-watchplan.py`) are out of scope here — wave 2 R56W2MutC2ToolA/B covered them; the
  tool blob is unchanged since `8a7b7346…`, so those findings carry.
- Per the operator stop, no probes were run after the receipt capture; everything above is from the completed
  battery and its saved receipts.

## Deliverables

- `.ufo/waves/round-56/w3/R56W3MutC2Harness.md` — this report
- `.ufo/waves/round-56/w3/R56W3MutC2Harness/mutants.md` — full write-up (method, 46-row table, survivors,
  proposals, limits, reproduce steps)
- `.ufo/waves/round-56/w3/R56W3MutC2Harness/{driver.py,verify2.py,classify.py}` — the driver scripts
- `.ufo/waves/round-56/w3/R56W3MutC2Harness/receipts/` — per-mutant per-probe stdout/stderr/rc, `mutant.json`
  (before/after hashes), `summary.json`, `classified.tsv|json`, `proposals/` (PR-wrong-rc, PR-jail, PR-argv
  runs + `verify2.json`), `jail-shape-probe.txt`

Scratch `/fast/scratch/hyaku/mado-r56/R56W3MutC2Harness` removed.
