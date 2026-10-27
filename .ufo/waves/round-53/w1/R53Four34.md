# R53Four34 — bounded counter/control mutation

## Scope and safety

Attacked the frozen round-53 C1 operability claim and examined C2 coverage evidence. Read `SKILL.md`, round-53 `claims-frozen.md`, `w1-spec.json`, `w1-dispatch.json`, and the assigned registry entry. The frozen claims name C1 as a scratch-aware accountable-instrument ledger counter and C2 as proposition-grounding repair of the indexed r52 dispatcher entry. No tracked lane/source bytes were changed; no Git/JJ mutations, source fetches, live probes, package queries, producers, or installs were performed. `disk-guard` was not available on PATH; `df -h /fast` reported 591G available. Scratch was confined to `/fast/scratch/hyaku/mado-r53/R53Four34`.

## C1 mutation — production-shaped ledger control

**Mutant:** starting from the exact ledger bytes at the frozen revision, changed only the 82 data rows: preserved each unique instrument path and full population, replaced each description with a distinct generic string (`unrelated generic filler placeholder NNN`), and pointed every row to `quality/tool-ledger.md` itself. This avoids a duplicate-row/schema/population confound while challenging both named defects.

**Detector:** the r52 C1 prototype `c1-r52-ledger.py` (SHA-256 `0fe862f116a789e8f6bebf38dea74b1f5ee20b3c810190ecf295621a3c34dc31`), run read-only against repo revision `ad4bf2059bcfafe63671d262222908ee1fe8001c`. This is a wave artifact, not a claim that a new C1 counter is committed at the r53 base.

Exact detector invocations (the only argument changing across legs is the ledger input and scratch work directory):

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev ad4bf2059bcfafe63671d262222908ee1fe8001c --ledger /fast/scratch/hyaku/mado-r53/R53Four34/pristine-ledger.md --work /fast/scratch/hyaku/mado-r53/R53Four34/work-pristine
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev ad4bf2059bcfafe63671d262222908ee1fe8001c --ledger /fast/scratch/hyaku/mado-r53/R53Four34/mutated-ledger.md --work /fast/scratch/hyaku/mado-r53/R53Four34/work-mutant-2
# After restoring mutated-ledger.md byte-for-byte:
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev ad4bf2059bcfafe63671d262222908ee1fe8001c --ledger /fast/scratch/hyaku/mado-r53/R53Four34/mutated-ledger.md --work /fast/scratch/hyaku/mado-r53/R53Four34/work-restored
```

**Actual output / verdict:**

- Pristine, exit 0: `C1_R52: population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=0 verdict=TARGET_MET rev=ad4bf2059bcfafe63671d262222908ee1fe8001c`
- Mutant, exit 1: representative details were `self_pointer path=tools/mado-action-plan.py target=quality/tool-ledger.md` and `generic_desc path=tools/mado-action-plan.py reason=no-instrument-specific-phrase`; final line: `C1_R52: population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=82 generic_desc=82 verdict=TARGET_MISSED rev=ad4bf2059bcfafe63671d262222908ee1fe8001c`
- Restored, exit 0: `C1_R52: population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=0 verdict=TARGET_MET rev=ad4bf2059bcfafe63671d262222908ee1fe8001c`

**Verdict: KILLED** for this combined self-pointer/generic-context mutant. Full population remained 82/82 with `dup=0`, `uncovered=0`, and no dangling rows. Since both defects were in one control, this run does not independently establish the counter's sensitivity to self-pointer-only and generic-context-only fixtures.

**Hashes / restoration:** frozen-base `git show` ledger and working ledger both hashed to `df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b`; scratch pristine hash was the same. Mutant hash: `931987738c4364694de87ad7df9237d1fe63724427999ac1b8be0e0402c191f5`. Restored `mutated-ledger.md` hash returned to `df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b`, byte-equal to the pristine copy; the restored detector leg passed.

## C2 — current counter/control limits and routed r52 evidence

The only proposition counter available for this probe was the r52 W1 draft `C2CounterDraft/c2-r52-proposition-entry.py` (SHA-256 `55452a3d6eab7cca2b20095f8678fbe936c8c65f241a561611a675defd8379fb`); no integrated `quality/counters/c2-r52-proposition-entry.py` exists at the inspected r53 tree. The draft's documented default slug is `corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md`, while the indexed entry is `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`.

- On r53 base `ad4bf2059bcfafe63671d262222908ee1fe8001c` with the default entry, exact result was `a ok=0 entry=absent`, clauses b–e skipped, `clauses_met=0 admitted=0/1 verdict=TARGET_MISSED`, exit 1.
- Supplying the actual entry path explicitly produced `a ok=1`, `b ok=1 propositions=18 ids=18 forms=table`, but `c ok=0 rows_bound=0/18 ... anchor_no_fetch_root`, `d ok=0 quotes_bound=0/18 ... pin_file_absent`, and `e ok=0 ... id_not_referenced`; final `clauses_met=2 admitted=0/1 verdict=TARGET_MISSED`, exit 1. Thus this r52 draft does not admit the indexed r52 entry in this read-only run. These are observations about the r52 draft, not claims about a proposed r53 replacement.
- The base no-work control at `85d57a818c3707397e21c840b6498b105ba798aa` returned `entry=absent`, clauses 0/5, `TARGET_MISSED`, exit 1. This is the expected C2 no-work result, not a mutant-kill result.

No C2 mutant was run: reproducing the recorded quote-forgery fixture requires a committed scratch-repo revision for the counter's `git show` inputs; round-53 bounds prohibit Git/JJ mutations. Therefore C2 mutation verdict is **INCONCLUSIVE / NOT RUN**, not killed or survived.

Routed round-52 evidence was checked against the retained local pins rather than assumed:

- `Attack32/ev-integrated-mutants.txt` records the integrated counter accepting the fabricated-P01-quote fixture: `C2_R52: props=18 rows=4 indexed=1 failures=0 verdict=TARGET_MET rev=364cdd343b7c73811dfb2125f327b1e1d753bd6c`, `exit=0`. This is a prior recorded run, not a fresh r53 reproduction.
- `Attack32/ev-quote-verify.txt` records P16 `collapsed=False raw=False`; its report explains that P16 splices the calls at `ConfigActions.cpp:1554` and `:1558`, omitting the intervening conditional. I independently read the local pinned lines: `:1554 sendKeyboardMods(...)`, `:1556 if (S.m_passPressed == 1) {`, `:1558 sendKeyboardKey(...)`, `:1576 sendKeyboardMods(0, ...)`.
- The retained dispatcher pin defines `sendshortcut` at `:531`, `sendkeystate` at `:591`, and places the repeat double-call at `:619-622` inside `sendkeystate`; this supports the routed P17 attribution defect without asserting runtime behavior.

Opened source records (no external fetch; access date in the registry is 2026-10-27): S371, `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.cpp`, located quote: `if (S.m_passPressed == 1) {` (line 1556), between the cited modifier and key calls. S370, `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp`, located quote: `if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);` (line 621), within `sendkeystate` (line 591). Pin SHA-256s: S371 `a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637`; S370 `7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771`.

## Scratch disposition

The scratch inputs, outputs, receipts, and work directories were removed before handoff; only this assigned report was written in the lane.

Report: `.ufo/waves/round-53/w1/R53Four34.md`
