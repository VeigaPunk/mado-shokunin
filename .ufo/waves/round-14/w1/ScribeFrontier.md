# ScribeFrontier — mado-r14-w1 (scribe, U5 frontier wording and Gate candidates)

Date: 2026-10-20. Lane root: /home/vgpnk/Projects/shokunin/mado-shokunin. Baseline registry: `corpus/SOURCES.md` ends at S046; S047/S048 are reserved by dispatch and **not yet present**. Nothing in `corpus/` was edited. No knowledge file was written. Draft text below is proposed wording for the owners named in §7.

Labels: `[OBS]` read in this seat; `[INF-docs]` upstream documented semantics; `[INF]` inference; `[UNK]` not exercised or not measured; `[PLANNED]` path/name not yet landed.

## 1. Bottom line

- U5 can move from frontier to **sourced documentation boundary** (not to feature behaviour). Two upstream XML sources were opened at pinned revisions and one installed-package observation was made.
- The most important finding is a **revision mismatch**: the host advertises `wp_color_manager_v1` version **3**; the S048 candidate pin the round-13 README neighbourhood would naturally reuse (`3dac056d`, the S005 README revision) declares version **2**. Tag `1.49` and the installed `wayland-protocols 1.49-1` declare version **3**. S048 must therefore pin the 1.49 tag, not `3dac056d`. Any row or note that cites `3dac056d` for a v3 claim is wrong.
- The wlroots output-management XML at `cdd2c7e0` declares `zwlr_output_manager_v1` v4 and `zwlr_output_configuration_v1` v4, matching the host advertisement (v4). That matching is an advertisement-version match only.
- No test, apply, image-description query, HDR, gamma or output-power action was exercised. Those stay `[UNK]`.

## 2. Inputs read (this seat)

| Input | Read | Note |
|---|---|---|
| `corpus/README.md` (FF3C) | full | Coverage map rows through round 13; Frontier bullets; U5 named as still open in the round-12 bullet and "U5–U7 frontier" in round 13. |
| `corpus/lessons/round-13.md` (5126) | full | Gate candidate format: Admit / Reject / Not admitted, located-quote table, registry mutations old→new, exercised verification. |
| `corpus/lessons/round-13-verifier-spotcheck.md` (1444) | full | Outside spot-check (`agree` on U4 admit and 3 rejects); routed R13-V1/V2/V3 (not this seat's assignment; see §8). |
| `corpus/SOURCES.md` (6131) | full | Registry ends at S046. Paths section and search log read. No S047/S048 row. |
| `corpus/QUALITY.md` (CC39) | full | Criteria 1–17; 6, 7, 8, 12, 15, 16, 17 applied below. |
| `corpus/knowledge/wayland-protocol-boundaries-r13.md` (D362) | full | U4 template: three-question table, phase table, host point sample, rejected list, limits. |
| `.ufo/waves/round-13/w1/ReviewPhases.md` (E4E5) | full | Prior pins: wlroots XML `cdd2c7e0` (M02 trap), README `3dac056d`, GOVERNANCE `35d9638c`, wayland-utils tag `1.3.0`. |
| `.ufo/waves/round-13/w1/ProtocolRecon.md` (29C0) §4.3 | read | Prior fence text for U5: advertisement ≠ client configuration, test/apply, or colour pipeline. |
| `.ufo/waves/round-13/w1/globals.json` | grep | Output/colour interfaces and versions; excluded-list (line 333–343). |
| `.ufo/waves/round-14/w1/spec.json`, `dispatch.json` | read | Assignment; reserved ids S047 = wlr-output-management, S048 = color-management-v1 (OutputSpec, ColourSpec). |

## 3. Source opens (this seat)

All opens 2026-10-20. Quotes are ≤25 words, located in the fetched body.

### 3.1 Candidate S047 — wlroots output-management configuration protocol

- URL: `https://gitlab.freedesktop.org/wlroots/wlroots/-/raw/cdd2c7e0064efee7fd398b2935923508b2fa9842/protocol/wlr-output-management-unstable-v1.xml`
- Revision: `cdd2c7e0064efee7fd398b2935923508b2fa9842` (same blob cited by ReviewPhases Q11; date of that commit 2025-09-10 per ReviewPhases).
- Tier scope: A for the XML's own statements about this protocol (wlroots repository, `zwlr_*` namespace, experimental). Does not establish Hyprland's implementation.

| # | Located quote (≤25 words) | Location (fetched body) | Teaches / decision |
|---|---|---|---|
| Q-a | "The protocol described in this file is experimental and backward incompatible changes may be made." (15 words) | description, `<protocol>` header (ReviewPhases cites XML lines 32–33) | **Admit** `[INF-docs]`: upstream self-describes experimental, no compatibility promise. |
| Q-b | "The information obtained from this protocol should only be used for output configuration purposes." (16 words) | `zwlr_output_manager_v1` description | **Admit** `[INF-docs]`: purpose is configuration, not generic property reading. |
| Q-c | "This protocol is not designed to be a generic output property advertisement protocol for regular clients." (16 words) | same description (ReviewPhases cites line 68) | **Admit** as scope limit; repeats round-12 M02 rejection. |
| Q-d | "Test the new output configuration. The configuration won't be applied, but will only be validated." (15 words) | `zwlr_output_configuration_v1` `test` request | **Admit** `[INF-docs]` documented meaning of `test` only. Host effect `[UNK]`. |
| Q-e | "Sent after the compositor has successfully applied the changes or tested them." (12 words) | `zwlr_output_configuration_v1` `succeeded` event | **Admit** `[INF-docs]`. Shows apply and test share one outcome event. |
| Q-f | "Sent if the compositor rejects the changes or failed to apply them." (12 words) | `failed` event | **Admit** `[INF-docs]`, with `cancelled` (outdated serial, "destroy this object") as the third outcome. |

Interface versions in the same pinned XML: `zwlr_output_manager_v1` **version="4"**, `zwlr_output_head_v1` **4**, `zwlr_output_mode_v1` **3**, `zwlr_output_configuration_v1` **4**, `zwlr_output_configuration_head_v1` **4**. Host capture (`globals.json`): `zwlr_output_manager_v1` **4**. Match is an advertisement-version match only.

Fetched-body line numbers differ from ReviewPhases' XML line numbers by a header offset; re-derive with `curl … | grep -n` before citing a line.

### 3.2 Candidate S048 — wayland-protocols colour-management

Two revisions opened, and an installed-package observation made. The revision decision is the main output of this section.

- URL (pin A, **rejected as the S048 pin**): `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/3dac056d83ad8947eed6eb621f346e91da736efd/staging/color-management/color-management-v1.xml`
  - Declares `<interface name="wp_color_manager_v1" version="2">`.
  - Also quotes "The protocol described in this file is currently in the testing phase."
- URL (pin B, **proposed S048 pin**): `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/ee78491a237eaff9389a0ccf8680521d074407d3/staging/color-management/color-management-v1.xml` (tag `1.49`, commit `ee78491a237eaff9389a0ccf8680521d074407d3`, per ReviewPhases tag table).
  - Declares `<interface name="wp_color_manager_v1" version="3">`.
  - Same testing-phase sentence; `wp_color_manager_v1` description "Compositors should never remove this global." (7 words).
  - Pin B's feature enum adds `windows_bt2100` (`value="8"`) after `windows_scrgb` (`value="7"`), which pin A's enum ends at `[OBS]` from the two raw bodies. Installed 1.49-1 file also has `create_windows_bt2100` at `since="3"` (line 601). Not a claim about host support.
- Installed observation (read-only, this seat): `pacman -Q wayland-protocols` → **1.49-1**; installed `/usr/share/wayland-protocols/staging/color-management/color-management-v1.xml`, sha256 `18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9`, mtime 2026-06-07, declares `wp_color_manager_v1` **version="3"** (line 80) and several `wp_color_management_*` interfaces at version 3. Mapping installed package → tag 1.49 is `[INF]` from the version string; the sha was **not** compared to the tag blob in this seat.

| # | Located quote (≤25 words) | Location | Teaches / decision |
|---|---|---|---|
| Q-g | "The protocol described in this file is currently in the testing phase." (13 words) | `<description>` warning paragraph | **Admit** `[INF-docs]` for the pinned revision only. The file sits in `staging/`, but the file's own word is "testing"; that is not one of the README's three phase names, so mapping is **not admitted** (see §6 R-list). |
| Q-h | "Backward incompatible changes can only be done by creating a new major version of the extension." (16 words) | same paragraph | **Admit** `[INF-docs]` as the versioning rule for this XML; does not turn the testing phase into a frozen API. |
| Q-i | "Compositors should never remove this global." (7 words) | `wp_color_manager_v1` description | **Admit** `[INF-docs]` as the upstream compositor expectation. Says nothing about whether this host keeps the global. |
| Q-j | `<interface name="wp_color_manager_v1" version="3">` (tag 1.49, line 80 of installed file) | interface element | **Admit** `[OBS]` as the version of the 1.49 revision. The 3dac056d revision says version 2, so an S048 row citing 3dac056d **must not** be used for a version-3 claim. |

Host advertisement for comparison (committed sanitized capture, `globals.json`): `wp_color_manager_v1` **version 3**; `wl_output` 4; `zwlr_gamma_control_manager_v1` 1; `zwlr_output_power_manager_v1` 1. The capture's `excluded` list names "wp_color_manager_v1 display colorimetry blocks" and "wl_output name/description/x/physical_width/make/subpixel_orientation/mode" as **not retained**. So the host's colour *state* is `[UNK]`.

## 4. Proposed SOURCES rows (draft; owners: SourceInventory / ColourSpec / OutputSpec to reconcile)

Not written. Shape follows the 11-column registry. Status `mined` only at the commit that lands the U5 note (QUALITY 8; SOURCES rule "row only after opening").

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S047 | wlroots `protocol/wlr-output-management-unstable-v1.xml` — https://gitlab.freedesktop.org/wlroots/wlroots/-/raw/cdd2c7e0064efee7fd398b2935923508b2fa9842/protocol/wlr-output-management-unstable-v1.xml | spec | A | Upstream self-description and documented request semantics for `zwlr_output_manager_v1` / `zwlr_output_configuration_v1` (v4), wlroots-owned, experimental | description header; `test`, `apply`, `succeeded`, `failed`, `cancelled` in `zwlr_output_configuration_v1` @ cdd2c7e0 (2025-09-10 commit) | Experimental, output-configuration-only; test validates without applying; apply/test share outcome events. Does not establish compositor implementation or host behaviour | queued → mined at landing | 2026-10-20 | on-release | corpus/knowledge/output-colour-boundaries-r14.md [PLANNED] |
| S048 | wayland-protocols `staging/color-management/color-management-v1.xml` — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/ee78491a237eaff9389a0ccf8680521d074407d3/staging/color-management/color-management-v1.xml | spec | A | `wp_color_manager_v1` v3 and its testing-phase/major-version rule at tag 1.49 | tag 1.49 @ ee78491a237eaff9389a0ccf8680521d074407d3; `<interface name="wp_color_manager_v1" version="3">`; description warning paragraph | Pinned-revision version and self-described testing phase; output/surface image descriptions are the protocol's purpose; not HDR behaviour on this host | queued → mined at landing | 2026-10-20 | on-release | corpus/knowledge/output-colour-boundaries-r14.md [PLANNED] |

Collision screen (QUALITY 17): no active row cites either URL. S005 cites a different path in the same repository (`wayland-protocols` README), so no same-URL collision. S048 must **not** use the S005 `3dac056d` pin. S046 cites wayland-utils, not wlroots or color-management.

Reciprocity (J3/J4): if S041 or S043 are cited by the new U5 note, their `used-by` cells must add the note path in the same commit; otherwise they stay U4-only. Recommended: cite S041 only as a `[OBS]` host sample; add the reciprocal `used-by` cell at landing.

## 5. Proposed U5 coverage row and frontier wording (draft)

### 5.1 Coverage-map row (README table) — PLANNED, not landed

| Note | Holds | Sources |
|---|---|---|
| `knowledge/output-colour-boundaries-r14.md` (planned; round 14; covers U5) | Output-management configuration and colour-management documentation boundaries: upstream purpose and experimental/testing self-description, pinned version of each protocol revision, documented `test`/`apply` outcome semantics. Advertisement of `zwlr_output_manager_v1` v4 and `wp_color_manager_v1` v3 is a registry observation; no configuration, image-description, HDR or output-power action was exercised. Those stay UNKNOWN. | `source:` S047 (wlroots `wlr-output-management-unstable-v1.xml` @ cdd2c7e0), S048 (wayland-protocols `color-management-v1.xml` @ tag 1.49 ee78491a); host sample S041 `[OBS]`. Recheck on wlroots or wayland-protocols release, on Hyprland or wayland-protocols package change, and on any new host capture. |

Head-15 `source:` line draft (for the note body, to be bound to landed rows only):

```
source: S047 (https://gitlab.freedesktop.org/wlroots/wlroots/-/raw/cdd2c7e0064efee7fd398b2935923508b2fa9842/protocol/wlr-output-management-unstable-v1.xml); S048 (https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/ee78491a237eaff9389a0ccf8680521d074407d3/staging/color-management/color-management-v1.xml); S041 (.ufo/waves/round-13/w1/globals.json, [OBS] advertisement only)
verified-at: 2026-10-20
recheck: on-release
covers: U5
```

Must stay `covers: U5` exactly (J2). No `, U6` suffix. The note body must not cite any row whose status is queued.

### 5.2 Frontier bullets (README "## Frontier") — draft

Replace the round-12 phrase "Still open: rule *attribution*, output management, the input debugging ladder and Waybar module text" with:

> Still open: rule *attribution*, the input debugging ladder and Waybar module text. Output management and colour are bounded in round 14 (below).

Add:

> - Round 14 moves U5's output-configuration and colour-management **documentation boundary** onto sourced ground ([output and colour boundaries](knowledge/output-colour-boundaries-r14.md) [PLANNED], S047/S048 pinned at wlroots `cdd2c7e0` and wayland-protocols tag `1.49`). Test/apply outcomes on this host, output and surface image descriptions, HDR or monitor reconfiguration, gamma-control and output-power behaviour stay UNKNOWN. Advertised `zwlr_output_manager_v1` v4 and `wp_color_manager_v1` v3 are registry observations, not feature results.

## 6. Lesson Gate candidates (for the round-14 lesson author; not written here)

### 6.1 Admit

- **A1 (S047, Q-a, Q-b, Q-c).** `zwlr_output_manager_v1` and its configuration objects are experimental, output-configuration-only upstream protocols. Scope: wlroots `cdd2c7e0`. Flip: a wlroots revision that removes the experimental warning or re-scopes the purpose.
- **A2 (S047, Q-d, Q-e, Q-f).** The documented meaning of `test` (validate, do not apply) and the shared `succeeded`/`failed`/`cancelled` outcome events. Scope: documented semantics only; no client request was sent. Flip: none for the document; host behaviour needs a separately authorised measurement.
- **A3 (S048, Q-j with pin B).** `wp_color_manager_v1` is version 3 at tag 1.49 and in the installed 1.49-1 file; version 2 at 3dac056d. Admitted as a **revision-binding** correction: a version claim must cite the revision that declares it. Flip: a later revision changing the version.
- **A4 (S048, Q-g, Q-h).** The XML self-describes a "testing phase" and says only a new major version can make incompatible changes. Admitted as upstream text for tag 1.49. The mapping of "testing" to a README phase is **not** admitted. Flip: the file's own statement at a later revision, or a README sentence naming the mapping.
- **A5 (S048, Q-i) — optional, narrow.** Upstream says compositors should never remove the `wp_color_manager_v1` global. Admitted as expectation text only; whether this host keeps it is `[UNK]` (it does advertise v3 `[OBS]` at capture time).

### 6.2 Reject

- **R1.** "An advertised `zwlr_output_manager_v1` v4 proves output configuration can be changed on this desktop." Rejected: S041 is registry discovery; the `test`/`apply` outcome events were never exercised. Flip: separately authorised test/apply measurement of a named head, with the output-identity fence kept.
- **R2.** "An advertised `wp_color_manager_v1` v3 proves HDR or a wide-gamut image description is active on this output." Rejected: the capture excludes colorimetry blocks and surface/output image descriptions were never queried. Flip: a measured image-description readback under an authorised session.
- **R3.** "The `3dac056d` README revision defines `wp_color_manager_v1` v3 (host version)." Rejected: that revision declares version 2. Flip: none; re-pin to tag 1.49 (or a later revision declaring 3).
- **R4.** "wlroots output-management is a generic output-property API for regular clients." Rejected (restates round-12 M02 for the U5 scope); S047 Q-c says the opposite. Flip: a wlroots revision that changes that description.
- **R5.** "`zwlr_gamma_control_manager_v1` v1 and `zwlr_output_power_manager_v1` v1 advertised ⇒ colour calibration or display power control works." Rejected as a conclusion from registry data; neither protocol has a source row here. Flip: a sourced row for each protocol, plus separately authorised behavioural evidence.
- **R6.** "The testing-phase XML belongs to the README's staging phase, so it is a frozen stable API." Rejected: the XML says backward-compatible changes may still bump versions, and the README's staging rule is "minimize" not "forbid". Flip: normative upstream text making the 1.49 file frozen.

### 6.3 Not admitted (kept `[UNK]`)

- Test/apply behaviour, serial-change behaviour, and cancel timing on this host.
- Per-head configuration, modes, positions, scale, transform on this host.
- Surface and output image descriptions; ICC/parametric creator behaviour; `windows_bt2100` behaviour on this host.
- Hyprland 0.56.2's implementation of either manager (HyprSupport seat owns that question; no claim here).
- Gamma-control and output-power protocol content (lead only, §6.4).

### 6.4 Leads (unopened, not rows)

- `zwlr_gamma_control_manager_v1` v1 and `zwlr_output_power_manager_v1` v1 — advertised in the 1.49-era host capture; wlroots protocol files not opened in this seat.

## 7. Routing to other seats

- **SourceInventory / ColourSpec:** S048 pin must be tag 1.49 (`ee78491a…`), not `3dac056d`. If ColourSpec pins `3dac056d`, the row's version claim is wrong and must be corrected before landing.
- **OutputSpec:** S047 pin `cdd2c7e0` is verified against the fetched body (experimental warning, configuration-only purpose, `test`/`apply` text). Their line numbers must be re-derived by `grep -n` on the same URL.
- **OutputPhase:** "testing phase" (S048) vs README phase names (S005) — the mapping is unresolved and must not be inferred.
- **OutputHost:** host `wp_color_manager_v1` v3 is consistent with tag 1.49, but the mapping of installed 1.49-1 to tag 1.49 is `[INF]`.

## 8. Out-of-scope notes (not this seat's assignment)

- R13-V1/V2/V3 wording is owned by BoundaryPrecision and ReceiptBuild. The new U5 note must **not** repeat the round-13 overbroad phrasing "retained S041 data is only registry interface/version headers". Correct form: "global records contain interface/version only; sanitized probe/session metadata is also retained." State the boundary between within-run file-plane unchanged and cross-revision output equality the same way.
- C2 operability: not assessed here.

## 9. Unknowns preserved

- Host output state, colour image descriptions, HDR state, gamma and output-power behaviour — `[UNK]`.
- Whether Hyprland 0.56.2 implements `wp_color_manager_v1` v3 and `zwlr_output_manager_v1` v4 as the pinned XML describes — `[UNK]`.
- Installed-package → tag mapping for `wayland-protocols 1.49-1` — `[INF]`; sha of installed XML not compared to tag blob.
- Fetched-body line numbers vs upstream line numbers — unreconciled; re-derive.

## 10. Exercised actions and tooling record

- Read-only: `corpus/**`, `.ufo/waves/round-13/**`, `.ufo/waves/round-14/w1/**`; two upstream raw fetches at pinned revisions (cdd2c7e0, 3dac056d); one raw fetch at tag 1.49 (ee78491a); one artifact grep over the cdd2c7e0 body.
- Read-only package observation: `pacman -Q wayland-protocols wlroots hyprland`; `pacman -Qi wayland-protocols`; `sha256sum` and `grep` on `/usr/share/wayland-protocols/staging/color-management/color-management-v1.xml`.
- No protocol client, `wayland-info`, `hyprctl`, compositor command or output mutation was run.
- No checks, builds, tests, linters, or smoke runs. No commits.
- Tools installed or upgraded by this seat: **none**. `wlroots` is not installed as a package on this host (`pacman -Q` returned no row); no `/usr/share/wlr-protocols` directory found.
- Files written: this file and `reports/ScribeFrontier.md` only.
