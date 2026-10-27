# R53Five43 — bounded mutation probe

Axes: operability (C1) and coverage (C2). Scope is a mutation probe, not admission or non-author review. Frozen C1 requires a new scratch-aware counter to distinguish the production ledger from the no-work control for self-pointer/context defects; C2 requires proposition-grounded, source-opened entry repair. The current `quality/counters/` inventory contained only the r51 C1/C2 counters, so no round-53 candidate was available to probe. I therefore used the prior C1 r52 draft and frozen control only as routed evidence; C2 was not mutated.

## C1 — mutation and detector

**Mutant.** In an isolated copy of `.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py`, changed only the self-pointer fallback branch at line 381 from `elif wide_self:` to `elif False and wide_self:`. This disables that branch for a control whose ledger pointer occurs in the description cell. No lane source was changed. Original and restored counter SHA-256: `0fe862f116a789e8f6bebf38dea74b1f5ee20b3c810190ecf295621a3c34dc31`; mutant SHA-256: `0b174a9a400efbd209de14458a91ecd9adde55990b7b34c0005082a4acf5bb40`.

**Expected detector.** Same bounded pure-Python detector on pristine, mutant, and restored module bytes: import `measure()`/`summarise()` and evaluate the frozen control bytes against an in-memory Reader (population paths `tools/mado-verify.sh`, `quality/tool-ledger.md`; no Git or external runtime calls). Pass only when the run reports both `self_pointer > 0` and `generic_desc > 0`; this checks the named red signals rather than accepting `TARGET_MISSED` alone.

Exact command for each state:

```sh
python3 -I /fast/scratch/hyaku/mado-r53/R53Five43/detector.py \
  /fast/scratch/hyaku/mado-r53/R53Five43/counter.py \
  /fast/scratch/hyaku/mado-r53/R53Five43/control.md
```

**Actual outputs.** Pristine (exit 0):

```text
CONTROL C1_R52: population=1 ledger_rows=2 uncovered=0 dup=1 dangling=0 bad_pointer=0 self_pointer=1 generic_desc=1 verdict=TARGET_MISSED rev=fixture-rev
SIGNALS self_pointer=1 generic_desc=1 dup=1 uncovered=0 bad_pointer=0
DETAIL self_pointer path=tools/mado-verify.sh target=quality/tool-ledger.md
DETAIL generic_desc path=tools/mado-verify.sh reason=no-instrument-specific-phrase
DETAIL dup path=tools/mado-verify.sh already-seen
DETECTOR PASS frozen self/context signals
detector_exit=0
```

Mutant (exit 1):

```text
CONTROL C1_R52: population=1 ledger_rows=2 uncovered=0 dup=1 dangling=0 bad_pointer=1 self_pointer=0 generic_desc=1 verdict=TARGET_MISSED rev=fixture-rev
SIGNALS self_pointer=0 generic_desc=1 dup=1 uncovered=0 bad_pointer=1
DETAIL bad_pointer path=tools/mado-verify.sh pointer='nothing | generic accountability pointer to this ledger itself' reason=no-target-names-the-instrument
DETAIL generic_desc path=tools/mado-verify.sh reason=no-instrument-specific-phrase
DETAIL dup path=tools/mado-verify.sh already-seen
DETECTOR FAIL missing frozen self/context signal
detector_exit=1
```

Restored (exit 0): same output as pristine, including `self_pointer=1 generic_desc=1 dup=1`, and SHA-256 exactly equal to the pristine bytes.

**Verdict: killed.** The detector caught loss of the self-pointer signal even though the summary remained `TARGET_MISSED`; a verdict-only detector would have missed the defect. This was a bounded probe of r52-draft logic, not a test of the unavailable round-53 counter.

## Control limitation and C2 evidence boundary

The frozen r52 C1 do-nothing fixture itself has two identical rows (control file lines 3–4). The r52 C1 draft receipt measured `population=82 ledger_rows=2 uncovered=81 dup=1 … self_pointer=1 generic_desc=1 TARGET_MISSED` (`.ufo/waves/round-52/w1/C1CounterDesign/receipts/receipts.txt:16-32`). Thus the named signals are present, but the fixture also fails uniqueness and completeness; it does not isolate a self-pointer/context-only failure. My normalized in-memory probe confirms the duplicate remains (`dup=1`) and the mutant still prints `TARGET_MISSED`. Treat this as an operability-control limitation, not a claim that the r53 target passed.

For C2, the routed r52 `C2CounterDraft.md:246-263` records that P16's quote was correctly located at the cited lines while its attached factual claim was wrong; the structural counter still returned 5/5. This is evidence that quote/pin binding cannot establish proposition truth, consistent with the frozen C2 requirement for an independent source-truth review. No C2 counter/control mutation was run: there is no round-53 candidate to mutate, and I did not run r52's Git-mutating fixture suite under this seat's no-Git-mutation boundary. C2 remains unprobed/inconclusive here.

No external source was opened (no URL/date/quote applies). Disk guard check: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh check` with `HYAKU_DISK_LOG=/dev/null` returned rc 0 (`/tmp 4%`, `/var/tmp 35%`, `/fast/scratch/hyaku 27%`). Scratch `/fast/scratch/hyaku/mado-r53/R53Five43` was removed; cleanup confirmed absent. No installs, live desktop reads, source-repository writes, Git/jj mutation, or commits.

Report: `.ufo/waves/round-53/w1/R53Five43.md`
