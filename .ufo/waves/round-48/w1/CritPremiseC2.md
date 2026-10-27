# CritPremiseC2 — report

Seat: CritPremiseC2 (UFO-FSD critic, w1). Target: falsify C2's premise before the freeze.

Status: investigation complete; findings at `.ufo/waves/round-48/w1/CritPremiseC2/findings.md`. Verdicts:
- "XKB compile unheld at base" — CONFIRMED (grep at 579f694b: only `corpus/README.md:112` and `corpus/knowledge/hyprland-input-devices-r46.md:69` name it as open; no corpus/tool line holds the compile).
- "xkbcli compile-keymap behaves like Hyprland's own compile" — TRUE only with the five config names passed explicitly and the same environment; bare `xkbcli` (no `--enable-environment-names`) differs from Hyprland's context in environment-name handling. Hyprland never passes NULL names (it passes `std::string::c_str()`, so unset fields are `""`), and its context has env names enabled; `xkbcli` defaults to `XKB_CONTEXT_NO_ENVIRONMENT_NAMES`.
- Ownership: the entry is mado input-plane ground (PROVINCE.md round-46 refinement), not tsukuroi or kotoba.
- Generic-vs-host split: RMLVO→KcCGST mechanics, include-path ordering and env semantics are generic libxkbcommon mechanics (pin the library tag); host-plane claims must be only the measured compile outcomes and the host's config root.

No code changes. Receipts in seat dir.

## Deliverables (seat dir)
- `findings.md` — full attack writeup (counterexample, evidence, impacted axes, smallest corrections).
- `receipts-xkbcli-empirical.txt` — host empirical transcript R0-R7 (sha256 2477219b908e78089142045e64c06066a9a3795d247629639ad48f51188b4980).
- `pins/` — libxkbcommon 1.13.2 tag d1442aaa P sources (6 files, SHA256SUMS) as read from clone; plus round-46 fetch pins (`Hyprland-IKeyboard.cpp`, `Hyprland-ConfigValues.cpp`) under `.ufo/waves/round-46/fetch/`.
- `verify-quotes.sh` — greps every cited quote against receipts/pins; last run rc 0 (23/23 OK).

## Verification & cleanup
- All quote locators verified by `verify-quotes.sh` (rc 0, 2026-10-26).
- Scratch `/fast/scratch/hyaku/mado-r48/CritPremiseC2/` removed after copying pins/receipts (trap).
- No pacman, no git/jj mutation, no host writes outside the seat dir and this report.
## Post-hoc L1 check (tree.json quarantine)
- The fleet-root tree.json quarantine notice was checked: this seat wrote no tree.json and no fleet-root file; all writes were under .ufo/waves/round-48/w1/CritPremiseC2/ and /fast/scratch/ (removed). Reply sent to MadoR48.
