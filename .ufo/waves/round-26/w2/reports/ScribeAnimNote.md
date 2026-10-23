# ScribeAnimNote — C1 animation knowledge note

## Behavior and findings

Drafted the C1 explanation of how Hyprland v0.56.2's legacy `animation` and `bezier` handlers configure the static animation tree and how `hyprctl animations` serializes that tree and the bezier inventory. It covers node parents/inheritance, `overridden`, handler validation and error conversion, JSON fields and numeric formatting, and the distinction between upstream source evidence and the local tool/counter contract.

The note cites the opened round-26 source rows S175, S176, S177, S158, and S162 with pinned file paths and line anchors. Provenance read: `.ufo/waves/round-26/fetch/WikiAnimations-legacy.bin`, `SrcAnimTree.bin`, `SrcAnimTreeHyprutils.bin`, `SrcHyprctlAnims.bin`, and `SrcAnimConfig.bin`; source-opening reports: `.ufo/waves/round-26/w1/reports/SrcHyprctlAnims.md` and `SrcAnimConfig.md`.

## Gates and exact commands

- Drafting only. No counter, Hyprland instance, live `hyprctl`, build, or test was run; no execution receipt exists and no `TARGET_MET` verdict is claimed.
- The tool command and frozen-counter invocation are documented in the note, but were not executed in this assignment:

  ```sh
  python3 -I tools/mado-anims.py --home DIR
  timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file <file>
  ```

- No tool install/update was needed.
- No conflicts encountered.

## Touched surfaces and scope

- Created `.ufo/waves/round-26/drafts/animation-table-r26.md`.
- Created this report at `.ufo/waves/round-26/w2/reports/ScribeAnimNote.md`.
- Did not edit the source ledger, product code, counter, harness, or `corpus/knowledge/hyprctl-verification-layer.md`.
- Out of scope: runtime capture, checking the executor's tool, counter scoring, and source-ledger integration.

## Verification-layer [INF] closure text

For `corpus/knowledge/hyprctl-verification-layer.md:158`, replace the phrase `directive→entry expansion [INF]` with:

> directive→entry expansion (see `corpus/knowledge/animation-table-r26.md`, §§ “Fixed node tree and inheritance”, “Directive validation and error path”, and “hyprctl animations -j table shape”)

The verification-layer file was not edited.

## Known limits

The note is a static-source account, not a fresh compositor observation. The cited handler does not establish whether style-validation errors are rolled back later, nor does the callback excerpt establish the complete user-facing diagnostic path. The note marks these limits and does not claim stable output ordering.

## Artifacts

- `.ufo/waves/round-26/drafts/animation-table-r26.md`
- `.ufo/waves/round-26/w2/reports/ScribeAnimNote.md`
