# AttackCoverage — report (MadoR14.AttackCoverage, critic, 2026-10-20)

Full findings, source-open records and anchors: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/AttackCoverage.md`.

Target: the proposed U5 output-management/colour boundary (C1 4/7 → 5/7) and the round-14 seat drafts feeding it.

Axes: coverage. Operability (C2) is not affected.

## Verdict input

**5/7 is supportable as a documentation boundary**, provided K1–K6 below are corrected in the landed note and rows. Complete output and HDR behaviour stays `[UNK]`; nothing found falsifies that.

The judge should **reject** the claim if the landed note:
- carries wlr `test`/serial/`cancelled` semantics onto this desktop;
- infers HDR from an advertisement or from a supported-TF list;
- pins S047 to the `wlroots/wlroots` copy;
- uses a floating `main`/`master` URL as a pin.

## Strongest counterexample

The text of the owning protocol is not the text Hyprland compiled, and Hyprland visibly diverges from the wlr semantics:

- **Owning text vs compiled text.** Hyprland v0.56.2 (`CMakeLists.txt:553`) compiles a vendored `wlr-output-management` XML that is byte-identical to wlr-protocols `4264185` (2022-09-05, sha `890594ae…`). Current upstream is a different text: `a5028afb` = `a741f0a` = `bf4fc79a`, sha `65b0f82a…`, with 30 differing diff lines. The interface versions are the same, so only the version claims carry over.
- **`test` always succeeds.** `OutputManagement.cpp:353` reads "TODO: STUB: applyTestConfiguration for test not implemented, returning true."
- **The serial is ignored.** The `create_configuration` serial argument (`:22`) is never read again.
- **`cancelled` is never sent.** The file contains 0 occurrences of "cancel".

## Must fix

- **K1 — wrong owner.** S047's owner is `wlroots/wlr-protocols` (README: "designed for use in wlroots (and other compositors)").
  - `wlroots/wlroots@cdd2c7e0` is a downstream copy (commit title "sync with wlr-protocols"). Reject ScribeFrontier's pin to it.
  - EvidenceChain's Hyprland header is generated from the vendored 2022 copy, not from S047's bytes.
- **K2 — spec presented as host behaviour.** These statements describe the upstream document only:
  - OutputSpec §2.2 and §2.4;
  - WlrVersion's "KMS driver" wording;
  - SourceInventory's "stale serial cancels".

  ScribeFrontier's R1 flip ("test/apply measurement") tells you nothing here, because test always succeeds. Record Hyprland conformance as `[UNK]`. There is no admissible row for it (S018 is getprop-only).
- **K3 — OutputSpec transcription errors.**
  - It says "must revert" and "mandatory rollback"; XML `:509-510` says **should** revert.
  - It calls the package "tagged `r112`", but upstream has 0 tags; `r112` is the Arch pkgver.
- **K4 — HDR inferred without display evidence.**
  - Hyprland advertises the PQ and HLG transfer functions unconditionally (`ColorManagement.cpp:52-53`).
  - The output image description is the encoding "the output expects" (XML `:671-672`).
  - `render:cm_auto_hdr` (default 1) switches HDR by compositor policy.
  - So ScribeFrontier's R2 flip ("image-description readback") cannot show HDR on the display; that would need DRM/KMS evidence from the sibling province.
  - ColourSpec line 135 treats `cm_enabled` / `wp_cm_1_2` as HDR rendering. They actually control protocol registration and version (`ProtocolManager.cpp:234-235`).
- **K5 — wrong versions and anchors.**
  - OutputHost: `set_custom_mode` is v1, not v4. The parametric creator is v1, not v3. v3 adds only `create_windows_bt2100`.
  - Verified history: the colour manager is v1 at tags 1.41–1.46, v2 at 1.47–1.48, and v3 at 1.49.
  - OutputPhase claims "all children v3", but `wp_image_description_reference_v1` is v1 and frozen.
  - OutputPhase's 11 interface line anchors are wrong.
  - OutputPhase gives tag 1.49 as `a8d65d7f`, which is the tag object; the commit is `ee78491a` (a repeat of round-13 A7).
- **K6 — floating URLs.**
  - EvidenceChain cites `raw/master` and `raw/main` as if they were pins. The `main` colour XML (`afa46ce1…`) is not the 1.49 file (`18a2678e…`).
  - Pin S048 to the 1.49 commit `ee78491a`. It matches the installed bytes, and Hyprland compiles from the system package data directory. The `35d9638c` pin is a stated-tradeoff alternative.

## Should fix

- **S1 — other colour authorities.** The capture also advertises two more colour authorities that the note must mark out of scope:
  - `zwlr_gamma_control_manager_v1` v1, owned by wlr;
  - `hyprland_ctm_control_manager_v1` v2, owned by Hyprland.
- **S2 — two copies of the colour XML.** Qt 6.11.2 installs its own colour XML at v1, so Qt clients bind at most v1. Hyprland's v1 path sends the deprecated sRGB transfer functions.
- **S3 — historical advertisement is config-dependent.**
  - The v3 advertisement depends on config and needs a restart to change: registered only if `cm_enabled`, at `wp_cm_1_2 ? 3 : 1`.
  - The option's description says "version 2" even though the code registers 3.
  - `wlr-protocols` was installed after the capture, by a round-14 seat. Hyprland does not use it.
  - EvidenceChain's "pre-installed" and ScribeFrontier's "no wlr-protocols" are both wrong.
- **S4 — monitor rules are a third surface.** The dossier's definition of U5 includes compositor monitor-rule HDR/ICC policy. Name it as outside the boundary.

## Counter gap (M1)

`measure.py` `body_facets` checks only the headings and an `[UNK]` marker. A note that claims "HDR works" still scores U5. Record a hand facet check next to the count:
- no positive host claim;
- S047 owner is wlr-protocols;
- the S048 revision declares v3;
- text from the upstream document is labelled as such;
- Hyprland conformance is `[UNK]`.

## Record

- Installs by this seat: none. OutputSpec installed `wlr-protocols r112.a741f0a-1` at 2026-10-20T02:41:32-0300.
- I read only upstream sources at pinned revisions and host package files (`pacman -Q/-Qi/-Qo`, `sha256sum`, and pacman-log transaction lines).
- I ran no compositor, client or `hyprctl` command, and read no host config.
- `/tmp` scratch held only upstream bytes and has been removed.
- No checks were run.
- Checks for L1 after integration:
  - re-derive the S047/S048 anchors with `grep -n` on the pinned raw bodies;
  - run the census;
  - run `measure.py` and the M1 hand check.

## Addendum: landed note review (output-colour-boundaries-r14.md, S047–S049; parent's S050)

- **No reject condition is present. 5/7 is supportable.** The note resolves the following:
  - **Owner and pin.** wlr-protocols is pinned at `a741f0ac…`, sha `65b0f82a…`.
  - **Revert wording.** The note says "should revert".
  - **HDR.** Nothing is inferred from advertisement, and `target_luminance` is called theoretical.
  - **Pins and conformity.** Each source has one pin, and there is no conformity claim.
  - **Spot-checks.** "Disabled heads" and "head name is not a DRM connector" both match XML `:49` and `:155-157`.
- **S050 corroborated.** I checked it independently at sha `148f12d7…`:
  - `setDisableHead` calls `scheduleReload` at `:321` and stores state at `:323`, before any test or apply.
  - The test stub is at `:352-354`.
  - **Guard:** the file calls `scheduleReload` only at `:321` (disable_head) and `:422` (apply). Scope S050 to "`disable_head` schedules a reload", not to every request.
  - Optional for the same anchor: the serial is unused after `:22`, and the file never sends `cancelled`.
- **Non-blocking fixes:**
  - **N1.** Add commit `ee78491a…` to the S048 anchor. The URL uses the tag-name ref `raw/1.49`.
  - **N2.** Add one limit sentence: Hyprland compiles a vendored older wlr XML (`4264185`, `890594ae…`, `CMakeLists.txt:553`), so S047 is not the compiled text.
  - **N3.** Add CTM and monitor-rule HDR/ICC policy to the `[UNK]` and out-of-boundary list.
  - **N4 (optional).** Note that `supported_tf_named` is creator-scoped (XML `:552-556`).
  - **M1.** Record the hand facet check next to the count.
- No runs. The `/tmp` scratch has been removed.
- **Cleanup re-confirmed.** `rm -rf -- /tmp/ac14` now tests `absent`.
- **jj disclosure.** I made one early `jj log -r @` call without `--ignore-working-copy`. jj reported "Reset the working copy parent…" and "Done importing changes from the underlying Git repo", which may have updated `.jj` operation state. No other jj calls were made, and lane history was not edited. From now on, read-only jj must use `--ignore-working-copy`.
