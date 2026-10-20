# ReviewSourceBar — U5 source and XML anchor audit (round 14, w1)

Role: reviewer (advisory). Date: 2026-10-20. Lane root: `mado-shokunin`.
Scope read: `corpus/QUALITY.md` (criteria 1–17), `corpus/SOURCES.md` (contract v1; rows S001–S046; collision screen), `corpus/lessons/round-13.md` (Gate candidate-decision format), `corpus/README.md` (frontier).
Authoring review is not non-author promotion authority. Nothing here is admitted; S047/S048 are proposals for the integrator.

## Tool and data provenance (criterion 13 / change-fence)

| action | channel / source | result | notes |
|---|---|---|---|
| `sudo pacman -Sw --noconfirm wlr-protocols` | pacman `extra` repo; download-only into `/var/cache/pacman/pkg/` | package `wlr-protocols-r112.a741f0a-1-any.pkg.tar.zst` present (cache mtime Nov 9 2025) | Nothing installed; `pacman -Sy` not run by me. Reason: obtain upstream XML without installing. Version recorded: r112.a741f0a-1. |
| `curl` raw fetches (gitlab.freedesktop.org) | official upstream raw URLs | hashes below | Scratch copies in `/tmp` (`cm-35d9638.xml`, `wlr-oms-a741f0a.xml`, `wlr-oms-raw.xml`): provenance only, not durable evidence. |
| `git ls-remote`, GitLab commits API (read-only) | gitlab.freedesktop.org | short SHA resolved to full commit | No writes. |
| Local `read` of `.ufo/waves/round-13/w1/globals.json` | committed capture | version rows | Read-only. |

## Findings (severity order)

### F1 — High — installed package file is not the S040-pinned revision; line anchors are revision-bound
- Local `/usr/share/wayland-protocols/staging/color-management/color-management-v1.xml` (owned by `wayland-protocols 1.49-1`): sha256 `18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9`, 1756 lines.
- Upstream `staging/color-management/color-management-v1.xml` @ `35d9638cf0c3f0bbf0c42996580a284f3d8ce564` (same revision as S040): sha256 `afa46ce15b135cce09cb46e0fbe9469914f5f9819cb938662c3cea370bd825ca`, 1756 lines.
- `diff` shows 3 changed lines (6 diff markers): line 41 (`docs/html/` locally vs `docs/book/` upstream), line 852 (`parameric` vs `parametric`), line 891 (`client client` vs `client`).
- Consequence: a citation of the installed path with a line number is not an upstream anchor. Any S048 row must name 35d9638 and sha `afa46ce1…`. The installed file may be cited only as a package observation with its own sha.
- Criterion 6/7 check: pass only after the revision-bound re-derivation below.

### F2 — High — wrong canonical URL for wlr-output-management; fixed anchor found
- Attempted `https://gitlab.freedesktop.org/wayland/wlr-protocols/-/raw/master/unstable/wlr-output-management-unstable-v1.xml`: returned a GitLab sign-in page (`text/html`), not XML. Not an anchor; no quote taken from it.
- Correct upstream per package `url` field: `https://gitlab.freedesktop.org/wlroots/wlr-protocols`.
- Short SHA `a741f0a` (package `pkgver r112.a741f0a-1`) resolved via GitLab commits API to full `a741f0ac5d655338a5100fc34bc8cec87d237346` (committed 2025-08-16; title "screencopy: deprecate in favor of ext-image-copy-capture-v1"). `a741f0a` is a true prefix of the full SHA.
- Raw fetch at full SHA: `unstable/wlr-output-management-unstable-v1.xml` sha256 `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7`, byte-identical to the package-extracted file.
- The wlr repo is NOT in `/usr/share` on this host (`wlr-protocols` not installed). The XML is an upstream observation, not a host fact.

### F3 — Medium — test and apply are distinct; "test passes" must not be admitted as "applies"
- Upstream a741f0a, `zwlr_output_configuration_v1` (line 424): `apply` request at 466; `test` at 481; events `succeeded` 495, `failed` 507, `cancelled` 517.
- Located quote, test (lines 483–484): "The configuration won't be applied, but will only be validated."
- Located quote, test (lines 486–487): "Even if the compositor succeeds to test a configuration, applying it may fail."
- Located quote, apply (lines 470–472): "there is no guarantee that the new output state matches completely the requested configuration."
- Admit (scoped): the protocol specifies a validate-only `test` request separate from `apply`, each followed by succeeded/failed/cancelled. Reject: "a successful test proves the configuration will apply." Flip: an authorized apply observation (mutating; out of this round's fence).

### F4 — Medium — governance scope: S040 does not govern wlr; colour phase is "testing", not stable
- S040 (`GOVERNANCE.md` @ 35d9638) governs wayland-protocols namespace inclusion. It does not classify `wlr_output_management_unstable_v1`, which lives in the wlroots repo. Do not cite S040 for wlr phase.
- wlr header (a741f0a lines 32–34): "Warning! The protocol described in this file is experimental and backward incompatible changes may be made."
- Colour header (35d9638 lines 74–75): "Warning! The protocol described in this file is currently in the testing phase."
- Reject: "wlr-output-management is stable" and "color-management is stable". Flip: a named stable-namespace revision for each.

### F5 — Medium — host advertisement supports version identity only, not feature behavior
- `.ufo/waves/round-13/w1/globals.json:155-156`: `"interface": "zwlr_output_manager_v1", "version": 4`. XML a741f0a `zwlr_output_manager_v1` is `version="4"` (line 42). Match.
- `globals.json:295-296`: `"interface": "wp_color_manager_v1", "version": 3`. XML 35d9638 `wp_color_manager_v1` is `version="3"` (line 80). Match.
- Admit (scoped): advertised interface/version agrees with the named revision's XML `version=` attribute on 2026-10-20 capture (captured_utc 2026-10-20T04:10:03Z).
- Reject: "advertised output or colour manager proves output configuration or HDR behavior" (same reject as round-13 Gate). Flip: separately authorized exercised test.
- Note: capture excludes `wp_color_manager_v1` display colorimetry blocks (`globals.json:336`); no colorimetry claim can rest on it.

### F6 — Medium — colour upstream anchor (admit scope)
- Upstream 35d9638 `wp_color_manager_v1` at line 80 (version 3); `wp_color_management_output_v1` at 634 (version 3), request `get_image_description` at 664; `wp_color_management_surface_v1` at 704, request `set_image_description` at 730.
- Located quote (lines 42–44): "The color properties are represented as an image description object which is immutable after it has been created." (18 words)
- Located quote (line 88): "Compositors should never remove this global." (6 words; `wp_color_manager_v1` description)
- Admit (scoped): interface names, versions, the phase warning, and the immutability description at 35d9638. Reject: any claim of HDR display behavior from these lines (F5).

### F7 — Low/Process — community tier never sole support
- S010 (wayland.app, tier C) is the only protocol-index row and is already restricted by its own row ("never sole support for an admitted entry"). Reject any U5 entry supported only by a community index. Flip: a primary anchor at a pinned revision (F2/F6 provide these).

### F8 — Info — collision screen (criterion 17) clean
- No registry row cites `wlroots/wlr-protocols` or `staging/color-management/color-management-v1.xml`. S040 uses `wayland-protocols` at the same commit 35d9638 but a different file (GOVERNANCE.md). Distinct scope; no merge trigger. Reuse of the same commit is fine when the file differs.

### F9 — Gap (not a defect in this wave's inputs)
- No Hyprland 0.56.2 source anchor for output-management or colour-manager implementation was opened by this seat. U5 host support statements stay unadmitted until OutputPhase provides a tagged-source anchor.

## Proposed registry rows (for integrator; not written by this seat)

| id | source | kind | tier | anchor (revision + sha + lines) | status proposal |
|---|---|---|---|---|---|
| S047 | wlr-output-management-unstable-v1 — https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/blob/a741f0ac5d655338a5100fc34bc8cec87d237346/unstable/wlr-output-management-unstable-v1.xml | spec | A | `unstable/wlr-output-management-unstable-v1.xml` @ a741f0ac5d655338a5100fc34bc8cec87d237346, sha256 65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7; lines 32–34, 42, 424, 466, 481, 495, 507, 517 | mined only after integrator confirms opened row fields |
| S048 | color-management-v1 — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/35d9638cf0c3f0bbf0c42996580a284f3d8ce564/staging/color-management/color-management-v1.xml | spec | A | `staging/color-management/color-management-v1.xml` @ 35d9638cf0c3f0bbf0c42996580a284f3d8ce564, sha256 afa46ce15b135cce09cb46e0fbe9469914f5f9819cb938662c3cea370bd825ca; lines 42–44, 74–75, 80, 88, 634, 664, 704 | mined only after integrator confirms opened row fields |

Do not use the installed `/usr/share/wayland-protocols/...` file as the S048 anchor (F1). Do not use `wayland/wlr-protocols` (F2).

## Rejection and flip register (advisory)

| claim | disposition | flip |
|---|---|---|
| wlr-output-management is stable | reject (F4) | stable-namespace revision |
| wayland-protocols GOVERNANCE (S040) classifies wlr protocols | reject (F4) | wlr governance source at a named revision |
| test succeeded, therefore apply will succeed | reject (F3) | authorized apply observation |
| apply succeeded, therefore state equals requested | reject (F3) | exercised state readback |
| installed-file line 41 as upstream anchor | reject (F1) | S048 at 35d9638 with sha |
| `wayland/wlr-protocols` raw URL | reject (F2) | `wlroots/wlr-protocols` at full SHA |
| advertisement proves HDR/output behavior | reject (F5) | authorized exercised test |
| wayland.app index as sole support | reject (F7) | primary anchor |
| testing-phase colour spec is stable | reject (F4) | stable revision |
| S047 admission on the wlr XML header and request/event lines | admit, scoped (F3) | — |
| S048 phase and interface anchors at 35d9638 | admit, scoped (F6) | — |
| host version rows match XML version attributes | admit, scoped identity only (F5) | — |

## Counts (criterion 10; re-derive with the commands shown; date 2026-10-20)

- 611 lines: `grep -c '' /tmp/wlr-oms-a741f0a.xml`.
- 5 wlr interfaces (lines 42, 128, 369, 424, 542): `grep -c '<interface name=' /tmp/wlr-oms-a741f0a.xml`.
- 1756 lines upstream colour file: `wc -l /tmp/cm-35d9638.xml`.
- 3 changed lines between installed and upstream colour files: `diff /usr/share/wayland-protocols/staging/color-management/color-management-v1.xml /tmp/cm-35d9638.xml | grep -c '^[<>]'` → 6 markers = 3 lines.
- 2 host version rows checked: `grep -n -E 'zwlr_output_manager|wp_color_manager_v1' .ufo/waves/round-13/w1/globals.json`.
- 2 source hashes re-derived at full SHAs (`curl … | sha256sum`), matching the scratch copies.
- Opened sources this seat: 3 upstream/package documents (wlr-protocols XML, colour XML at 35d9638, the wrong-URL fetch) plus 1 committed host capture.

## Re-derivation commands (criterion 6)

```
curl -fsSL https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/a741f0ac5d655338a5100fc34bc8cec87d237346/unstable/wlr-output-management-unstable-v1.xml | sha256sum   # expect 65b0f82a…
curl -fsSL https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/35d9638cf0c3f0bbf0c42996580a284f3d8ce564/staging/color-management/color-management-v1.xml | sha256sum   # expect afa46ce1…
```

## Verification gaps

- Pinned host implementation (OutputPhase) not reviewed here.
- The wlr-protocols package sha (`65b0f82a…`) was checked by extraction and by raw fetch; no independent non-author verifier has reviewed it.
- The local package revision of wayland-protocols 1.49-1 is not tied to a commit; only its own sha `18a2678e…` is recorded.
- No promotion or admission authority is claimed; the outside spot-check remains pending by lane policy.
