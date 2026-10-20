# ScribeFrontier — rendered report (mado-r14-w1)

Date: 2026-10-20. Seat: MadoR14.ScribeFrontier (scribe, leaf). Milestone: U5 boundaries and regular-source targets. Axes: coverage, operability (this seat addresses coverage only).

## Behavior

Drafted U5 coverage-row and frontier wording plus Gate admit/reject candidates. Opened two upstream protocol XML revisions and one installed package file, read-only. Full findings: `.ufo/waves/round-14/w1/ScribeFrontier.md`.

## Gates

- No gate, selftest, file-plane, census, or regression run. No `tools/mado-verify.sh` edit.
- No knowledge file, SOURCES row, lesson, or README edit. All U5 text is proposed draft for owners.
- S047/S048 are reserved ids and are **not** in `corpus/SOURCES.md` (registry ends at S046); their rows are drafts pending landing.

## Touched surfaces

- Written: `.ufo/waves/round-14/w1/ScribeFrontier.md`, `.ufo/waves/round-14/w1/reports/ScribeFrontier.md`.
- Read only: `corpus/README.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/lessons/round-13.md`, `corpus/lessons/round-13-verifier-spotcheck.md`, `corpus/knowledge/wayland-protocol-boundaries-r13.md`, `.ufo/waves/round-13/w1/{ReviewPhases.md,ProtocolRecon.md,globals.json}`, `.ufo/waves/round-14/w1/{spec.json,dispatch.json}`.
- Remote read (pinned): wlroots `cdd2c7e0` `wlr-output-management-unstable-v1.xml`; wayland-protocols `3dac056d` and tag `1.49` (`ee78491a`) `staging/color-management/color-management-v1.xml`.
- Local read-only package: `/usr/share/wayland-protocols/staging/color-management/color-management-v1.xml` (sha256 `18a2678e…49f9`).

## Findings

1. **Revision mismatch (material).** Host advertises `wp_color_manager_v1` **v3**. Pin `3dac056d` (the S005 README revision) declares **v2**. Tag `1.49` and installed `wayland-protocols 1.49-1` declare **v3**. Proposed S048 pin: tag 1.49 (`ee78491a…`). Any S048 row citing `3dac056d` for a v3 claim is wrong.
2. **wlroots output-management** at `cdd2c7e0` is self-described experimental and configuration-only; declares `zwlr_output_manager_v1` v4 (matches host v4 advertisement). `test` validates without applying; `succeeded`/`failed`/`cancelled` events are the outcome set. Documented only.
3. **Testing-phase wording.** The colour XML says "currently in the testing phase" but sits in `staging/`. That is not a README phase name; mapping is not admitted.
4. **Advertisement is not behaviour.** No test, apply, image-description query, HDR, gamma-control or output-power action was exercised. Host output/colour state is `[UNK]`. The round-13 capture excluded colorimetry blocks.
5. **Leads (not rows):** `zwlr_gamma_control_manager_v1` v1 and `zwlr_output_power_manager_v1` v1 advertised; no source row, not opened.

## Proposed U5 coverage row (PLANNED)

`knowledge/output-colour-boundaries-r14.md` — covers U5; sources S047 (cdd2c7e0) and S048 (tag 1.49), host sample S041 `[OBS]`. Note may cite only rows already `mined` (J3); S041 used-by must gain the note path at landing (J4). Full wording in findings §5.

## Lesson Gate candidates

- **Admit:** A1 S047 experimental/configuration-only purpose; A2 S047 `test`/`apply`/outcome-event semantics as documented; A3 S048 version-3 at tag 1.49 vs version-2 at 3dac056d (revision-binding correction); A4 S048 self-described "testing phase" and major-version rule, without the phase mapping; A5 S048 "should never remove this global" as expectation text only (optional).
- **Reject:** R1 advertised output manager ⇒ configuration works; R2 advertised colour manager v3 ⇒ HDR/wide-gamut active; R3 `3dac056d` defines host v3; R4 wlroots output-management is a generic property API (restates round-12 M02); R5 gamma/power advertised ⇒ calibration/power control works; R6 testing-phase XML is a frozen stable API.
- **Not admitted:** test/apply on this host, per-head config, image descriptions, Hyprland implementation, gamma/output-power content.

Flip conditions for each row are in findings §6.

## Out-of-scope items

- R13-V1/V2/V3 wording: owned by BoundaryPrecision and ReceiptBuild. The U5 note must avoid the round-13 "retained data is only registry headers" phrasing and must not infer cross-revision output equality from within-run boundary receipts.
- C2 operability: not assessed.
- Registry rows, SOURCES census, README edits, lesson file: owned by other seats or the integrator.

## Owner routing

- SourceInventory / ColourSpec: S048 must pin tag 1.49, not `3dac056d`.
- OutputSpec: re-derive S047 line numbers with `grep -n` on the cited URL before use.
- OutputPhase: "testing" vs README phase names unresolved.
- OutputHost: installed 1.49-1 ↔ tag 1.49 mapping is `[INF]`.

## Artifact paths

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/ScribeFrontier.md`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/reports/ScribeFrontier.md`

## Tooling record

No installs, upgrades, or package operations. Read-only `pacman -Q`/`-Qi`, `sha256sum`, `grep` on the installed XML; `curl`-equivalent raw reads through the read tool. No `wayland-info`, `hyprctl`, protocol client, or compositor command. No commits.
