# ReviewCorrections — R13-V1..V3 correction paths (report)

Seat: MadoR14.ReviewCorrections · 2026-10-20 · lane `mado-shokunin` HEAD `873ff08` · read-only review.
Full findings, verbatim draft errata blocks and per-item checklist: `.ufo/waves/round-14/w1/ReviewCorrections.md`.
Tools installed or upgraded: none. Checks: read-only only (file reads, `git show <rev>:<path> | sha256sum`, JSON key queries). No gate, selftest, build or regression run. No web sources opened.

## Findings by severity

1. **Blocking for V3 closure (D1).** The planned receipt wrapper binds to a committed REV. The round-14 gate is uncommitted during the wave, and the wave forbids commits, so an in-wave receipt cannot bind and will refuse. Resolve by integrator commit before L1 receipts, or by a labelled provisional receipt rebound at commit (QUALITY.md criterion 7).
2. **Unreachable unless assigned (D2).** V1 and V2 need errata appended to two knowledge notes. No seat owns those files. L1 must apply them at integration.
3. **Historical record must not be edited (D3).** The V2 fleet statement at `.ufo/reports/round-13/mado.md:68` is in the fleet root, read-only to this lane. Correct it only by a lane erratum citing that line.
4. **Guard (D4).** Do not change `tools/mado-verify.sh:2703` ("config plane byte-identical before/after"). Editing it moves the gate sha from `037b05dc…` and forces a regression re-cut.

## Per-item status

- **R13-V1 retained-data wording — path reachable.** Line 43 of `corpus/knowledge/wayland-protocol-boundaries-r13.md` is too broad. `globals.json` `globals[]` records carry only `interface` and `version`. The top-level `probe`, `tool`, `compositor`, `multiplicity`, `session_binding` and count/digest fields are retained, and `excluded` lists the discards. Correction: appended errata block after line 104; line 43 unchanged; cite the "Host point sample" section, not the following paragraph.
- **R13-V2 boundary vs revision output — path reachable.** `gate-file-plane.txt:47` supports only a within-run before/after equality (combined sha `3cb692751b4d…`). Committed combined digests differ across receipts (`364b4f5e…`, `48c882b9…`, `3cb69275…`), so cross-run equality is not established. Correction: appended block in `corpus/knowledge/gate-standing-use.md` after line 402; the 29 PASS / 0 FAIL / 0 UNKNOWN result is preserved.
- **R13-V3 standalone receipt digest — forward path reachable; round-13 receipt stays unedited.** `gate-selftest.txt` (blob `b093dc4b…`) has no revision or digest header. The binding is recoverable: `git show 95cbc41:tools/mado-verify.sh | sha256sum` = `037b05dc…`, equal at `59cfbdc` and in `committed-bindings.json`. Forward: round-14 standalone receipts go through `.ufo/waves/round-14/receipt.py` (ReceiptBuild). Subject to D1.

## Acceptance checklist (summary; full list in the findings file)

- [ ] V1-1 Line 43 unchanged; errata appended; old sentence quoted; new wording enumerates top-level retained fields.
- [ ] V1-6 Not touched: `globals.json`, round-13 lesson, S041 row, README U4 row.
- [ ] V2-1/2 Errata states within-run scope and excludes cross-revision equality, citing the three digests.
- [ ] V2-3 Fleet report line 68 named; fleet file not edited.
- [ ] V2-4 29 PASS / 0 FAIL / 0 UNKNOWN / 8 SKIP / 4 NOTE, exit 0 preserved.
- [ ] V2-6 `grep -c 'config plane byte-identical before/after' tools/mado-verify.sh` = 1 at integration.
- [ ] V3-1 `gate-selftest.txt` unchanged.
- [ ] V3-2 Binding errata with derivation command, citing the base `7dcb785` gate as not bound.
- [ ] V3-3/4 Round-14 receipts via `receipt.py`; mismatch exit 2; no passing receipt on mismatch.
- [ ] V3-5 Provisional label and rebinding at commit, if D1 option (b).

## Decisions requested

- D1: choose integrator-commit-then-receipt (a) or labelled-provisional wrapper change (b) for V3.
- D2: assign L1 to apply the V1 and V2 errata at integration.
- D3: confirm the fleet report stays unedited.
- D4: keep `tools/mado-verify.sh:2703` text unchanged.

## Verification gaps

- No gate, selftest or regression was run; all receipt facts are read from committed bytes.
- `receipt.py` does not exist yet, so the V3 forward path is unverified.
- The V2 wording remains open to misreading ("before/after"); the errata reduce this but do not remove it.
