# ReviewSourceBar — rendered report (round 14, w1)

Date: 2026-10-20. Full findings: `.ufo/waves/round-14/w1/ReviewSourceBar.md`. Advisory reviewer output; not admission or promotion authority.

## Verdict

The two U5 upstream anchors are supportable once bound to revisions:

- **wlr-output-management**: `wlroots/wlr-protocols` @ `a741f0ac5d655338a5100fc34bc8cec87d237346`, `unstable/wlr-output-management-unstable-v1.xml`, sha256 `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7`. Admit scoped to the spec text (test vs apply, configuration result events, experimental header).
- **color-management-v1**: `wayland/wayland-protocols` @ `35d9638cf0c3f0bbf0c42996580a284f3d8ce564`, `staging/color-management/color-management-v1.xml`, sha256 `afa46ce15b135cce09cb46e0fbe9469914f5f9819cb938662c3cea370bd825ca`. Admit scoped to interface versions, testing-phase warning, and the immutability description.

Two anchors that look valid are not: the installed `/usr/share/wayland-protocols/…` file (sha `18a2678e…`, three lines differ from 35d9638) and the `wayland/wlr-protocols` URL (returns a sign-in page).

## Findings by severity

1. **High — installed colour file ≠ pinned revision.** Lines 41, 852, 891 differ. Cite only 35d9638 with its sha.
2. **High — wrong wlr URL.** Correct repo is `wlroots/wlr-protocols`; `a741f0a` is a true prefix of `a741f0ac…237346`.
3. **Medium — test ≠ apply.** Spec: "The configuration won't be applied, but will only be validated" (lines 483–484); "Even if the compositor succeeds to test a configuration, applying it may fail" (486–487).
4. **Medium — governance scope.** S040 governs wayland-protocols namespaces, not wlr. Colour is "currently in the testing phase" (35d9638 lines 74–75), not stable.
5. **Medium — advertisement is version identity only.** `zwlr_output_manager_v1` v4 and `wp_color_manager_v1` v3 in the round-13 capture match XML version attributes; they prove no behaviour.
6. **Low — community tier.** wayland.app (S010) must never be sole support.
7. **Info — collision screen clean.** No existing row cites either file; S040 shares commit 35d9638 but a different path.
8. **Gap — host implementation not reviewed.** OutputPhase must supply a tagged-source anchor before any U5 host-support claim.

## Rejection and flip (advisory)

- Reject: wlr protocol is stable. Flip: stable-namespace revision.
- Reject: a successful test proves apply. Flip: authorized apply observation.
- Reject: advertised manager proves HDR or output behaviour. Flip: authorized exercised test.
- Reject: installed-file line 41 as upstream anchor. Flip: S048 at 35d9638.
- Reject: wayland.app as sole support. Flip: primary anchor.

## Proposed rows for the integrator (not written here)

- S047 — wlr-output-management, spec, tier A, anchor a741f0a… + sha `65b0f82a…`; lines 32–34, 42, 424, 466, 481, 495, 507, 517.
- S048 — color-management-v1, spec, tier A, anchor 35d9638… + sha `afa46ce1…`; lines 42–44, 74–75, 80, 88, 634, 664, 704.

## Counts (2026-10-20)

- 611 lines wlr XML — `grep -c '' /tmp/wlr-oms-a741f0a.xml`.
- 5 wlr interfaces — `grep -c '<interface name=' /tmp/wlr-oms-a741f0a.xml`.
- 1756 lines upstream colour XML — `wc -l /tmp/cm-35d9638.xml`.
- 3 changed lines installed vs upstream — `diff <installed> /tmp/cm-35d9638.xml | grep -c '^[<>]'` → 6 markers.
- 2 host version rows matched — `grep -n -E 'zwlr_output_manager|wp_color_manager_v1' .ufo/waves/round-13/w1/globals.json`.

## Tooling record (operator directive)

- `sudo pacman -Sw --noconfirm wlr-protocols` — channel: pacman `extra`; version r112.a741f0a-1; download-only to pacman cache; nothing installed; reason: obtain the upstream XML. No `-Sy` run.

## Verification gaps

- No independent non-author verifier. Outside spot-check pending by lane policy.
- No host-implementation source reviewed (OutputPhase).
- Installed wayland-protocols 1.49-1 has no commit tie; only its own sha is recorded.
