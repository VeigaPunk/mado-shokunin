# CritRoutedItems — report (round 47 w1)

Seat: `CritRoutedItems` (leaf, routing critic). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Reviewed against `60edb66e2f1cb90acc6e9442fc93ded0ca42d750` (round-47 base; HEAD `c24adef2` =
dispatch). Full findings: `.ufo/waves/round-47/w1/CritRoutedItems/findings.md`; receipts:
`…/CritRoutedItems/receipts/{frozen-gate-base.txt,r5-base.txt}`.

Summary:

- **R1** open and unclaimed: `hyprland-input-devices-r46.md:57` still cites
  `live-devices-host-l1.txt` (l1-draft `b229efd0…`) and "one `input` block"; the landed receipt
  `live-devices-host-r46.txt` (tool `3a803689…`, omarchy default first) is the correct citation.
  Closure: appended erratum citing the r46 receipt; `git diff 1001bda0 HEAD -- <entry>` = insertions only.
- **R2** open: `out.json.rows.tsv` (3,282,451 B, sha256 `6573f76b…`) still untracked; `sha256.txt`
  has no digest. Closure: digest beside `out.json` + remove, or stated retention.
- **R3** gate blob at base is byte-identical to the frozen original (`889f8f05…`); no marker, no
  R5/R6, no registry. At `60edb66` the frozen gate reports `findings=115 files=18371` exit 1, incl.
  18 findings in 7 round-46 w1 files the draft's registry does not cover. R5 re-measured: 24 carriers,
  0 new FP (draft claim holds). Closure: merged single gate (marker + serial), registry with 47 +
  round-46 rows/sidecars, both-direction demo regenerated at the base rev, selftest ≥45/45. The gate
  stays red after R3 by design (15 real findings).
- **R4** `ExecSupersede` is stale on anchors (top S315/252 → S325/262, insert after line 274) and its
  ids `S326-S333` collide with round-47 C2's planned `S326..` rows — must be renumbered/owned before
  either lands. `ScrErrata` holds in substance; one locator (E5 `:2566`) drifted — refresh at landing.
  `CritW2Entry` is valid; entry unchanged at base (diff empty); six units verbatim.

Draft verdicts: ExecSessionTriage — stale in coverage scope (round-46 set unmarked), valid diff-base;
ExecSerialRule — stale in numbers only (claims re-verified); ExecSupersede — stale (anchors + id
collision); ScrErrata — valid, locator refresh; CritW2Entry — valid.

No lane/tracked file edited; no host call; no tool installed; scratch `/fast/scratch/hyaku/mado-r47/CritRoutedItems` deleted after copying receipts.
