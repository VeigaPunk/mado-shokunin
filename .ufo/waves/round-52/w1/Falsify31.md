# Falsify31 — C2 held-ground novelty

## Finding (severity: low / bounded redundancy)

**Attacked predicate:** C2 coverage condition that the new entry be a distinct contribution, alongside the C2 held-ground novelty target. In the currently available `C2EntryDraft/proposition-map.tsv`, P15 repeats prior ground: “`sendkeystate` restores the previous press field after it delegates, so a dispatch does not leave its state behind.” The committed base entry `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:197-199` already states that `sendkeystate` writes the field itself, “saving and restoring it around its work,” citing `Hyprland-ConfigActions.cpp:1603-1615`. This overlap is factual, not merely shared terminology. Evidence copy: `.ufo/waves/round-52/w1/Falsify31/overlap-evidence.txt`.

**Reproducible comparison:** Read the above two cited ranges, then compare the draft map P15 to the base entry. Result: the restoration claim in P15 is already present in the base entry. **Reproduced: yes** (the proposition overlap). P16 (“a second implementation … also repeats on success”) adds detail not stated in the cited prior sentence, so the evidence does not establish that the whole proposed entry is non-novel or fails the frozen C2 predicate.

## Counter/control status and limits

The frozen no-work C2 control is the base revision with the target new entry absent; its absence is specified by `registration.md` and `controls/c2-do-nothing.md`. The supplied `receipts/c2-base.txt` is explicitly a C2_R51 receipt and reports `TARGET_MET` for the older entry; it does not exercise the new R52 target. No R52 C2 counter or completed entry was present in the mapped wave artifacts at inspection, so I could not run an R52 counter, reproduce a counter bypass, or score the no-work control against that new predicate.

As a separate warning about what the old counter establishes (not a claim about an unseen R52 counter): `quality/counters/c2-r51-dispatch-entry.py:512-553` accepts a held citation when the cited base file/line exists and each listed token occurs on that line. That check does not compare the held proposition's meaning to the cited text. Its implementation cannot by itself prove held-ground truth/novelty; a new counter's behavior remains untested here. The frozen C2 registration already assigns source-truth review to an outside reviewer, so this observation is not by itself a failure of the frozen contract.

## Limitations

Source-only constraints followed: no network fetch, package query, live probe, screenshot, producer execution, or source-checkout mutation. Source candidates used were already present locally. No external source candidate was consulted. No claim or predicate edits; no install. Scratch was created under `/fast/scratch/hyaku/mado-r52/Falsify31/` after the disk guard (`df -h /fast/scratch /home/vgpnk/Projects/shokunin`); the check returned successfully. No scratch evidence was retained there, so cleanup was unnecessary.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify31/overlap-evidence.txt`
- `.ufo/waves/round-52/w1/Falsify31.md`

Report: `.ufo/waves/round-52/w1/Falsify31.md`
