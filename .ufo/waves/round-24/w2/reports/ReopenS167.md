# ReopenS167 — round 24 wave 2, source re-open S167 (attack)

Reviewer: MadoR24.ReopenS167 (leaf seat, no subagents). Lane revision audited: 39c596307333b8ca0a1e42b3f3b9a748bb8b208b (`git rev-parse HEAD` matches; `git status --porcelain` shows only three untracked w2 report files, so the working-tree rows below are the pinned revision's rows). No tools installed. No git/jj write commands run in the lane.

## What I attacked

SOURCES row S167 (corpus/SOURCES.md line 179): "Using hyprctl — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/advanced-configuration/using-hyprctl.md", pin c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:95d8b8422a1fd25229bfe350e05624d8a318c746803efb7f3893015bf7c417f0, 8239 B; and every claim row citing it (exactly one: A24).

## Source re-verification

- Fresh fetch (curl, raw.githubusercontent.com, no bot bypass) of the pinned URL → sha256 `95d8b8422a1fd25229bfe350e05624d8a318c746803efb7f3893015bf7c417f0`, 8239 bytes. Both equal the row. `cmp` against `.ufo/waves/round-24/fetch/S167.bin`: byte-identical (same hash, same size).
- Pin resolves: `git ls-remote https://github.com/hyprwm/hyprland-wiki` shows `c66e8de21f5ecdc4bc5e278e7d94800ea10957af` as both `HEAD` and `refs/heads/main` (i.e. the pin is the wiki's current tip). Local read-only clone /fast/scratch/hyaku/mado-r24/src/hyprland-wiki holds the commit (2026-10-22 14:52:44 +0200, "configuring/code-snippetes: fix a var and a note mistake (#1683)") and `git show <pin>:content/.../using-hyprctl.md` hashes to the same `95d8b842…17f0` / 8239 B — raw-served bytes = commit bytes.
- Cited ranges exist and match the row's description:
  - 192-200 = `### getprop` block ("Gets a property value of a window." … `hyprctl getprop <window> <property>` …).
  - 238-262 = `## Usage` heading plus the full 22-line ```plain command list; contains `workspacerules` (245), `clients` (246), `rollinglog` (259).
  - 284-295 = `## Flags` through `- r - force state refresh after issuing commands (e.g., layout or rule changes)` (295).

## Per-row verdicts

### A24 (corpus/knowledge/rule-attribution-r24.md line 58) — VERDICT: holds

Claim: "`workspacerules` is documented to list defined workspace rules." Source: S167. Quote: "workspacerules       - gets the list of defined workspace rules".

- (a) Quote occurs verbatim: PASS. Byte-exact (7 spaces before the dash), exactly one occurrence in the pinned bytes, at byte offset 6082 = line 245, inside cited range 238-262.
- (b) TRUE of quoted bytes, no overreach: PASS. The doc line says the `workspacerules` subcommand "gets the list of defined workspace rules"; the claim restates exactly that with the correct hedge "is documented to" — a documentary claim only, no runtime-behavior or attribution assertion smuggled in. The knowledge entry uses it the same way ("`hyprctl workspacerules` lists **workspace** rules (A24)"), correctly scoped to workspace rules, not window/layer rules.
- (c) Rule attribution, not generic rule mechanics: HOLDS with a noted nuance. The row documents an introspection/exposure channel — a hyprctl verb that exposes declared rules by identity — which serves the entry's "which rules exist" axis ("what exposes rule identity"). It is not a rule-to-effect attribution claim and is not presented as one (the SOURCES row itself says "not rule-to-effect attribution"); its attribution value is the exposure asymmetry it anchors: the pinned Usage list (241-262) contains a workspace-rule listing verb and no window-rule or layer-rule listing verb. That is a boundary fact about what upstream exposes, not generic evaluation semantics of the A25/A26 kind. The nuance does not rise to a defect.

Cross-check: the round's own counter (`python3 -I .ufo/waves/round-24/c1/count.py cf86f9e0e532767bd6989e1d288a681fd72e3651`, receipt .ufo/waves/round-24/evidence/c1-after-cf86f9e0.txt) gives `A24 S167 PASS_ROW`; its three FAIL_ROW rows are A5/A7/A8 on S155/S156, outside this seat's scope.

## Findings by severity

- Critical: none.
- Major: none.
- Minor: none.
- Observations (no action): (1) the pin equals the wiki's live main tip, so the hash row stays reproducible until upstream moves — the recheck trigger ("on-release / wiki change") is the right guard. (2) `workspacerules` behavior was never runtime-verified (verified-at covers `hyprctl version` and `hyprctl clients -j` only); the claim's "is documented to" phrasing stays inside that evidence.

## Residual risk and verification gaps

- Refetch and clone agree today; a force-push of a different `c66e8de` is not detectable by hash comparison against the row alone, but ls-remote today shows the same hash at main/HEAD, so no current drift.
- The Usage list's exhaustiveness (used by the entry's "no window-rule listing verb" sweep) is documentary: absence in this pinned page, not a protocol-level proof; A24 itself does not carry that negative claim.
- I did not re-run the C1 counter (host-safety cap; run once at cf86f9e0 by wave 1) nor the c2/quality checks — out of this seat's scope.

## Summary

VERDICT: holds — S167's pin, sha256, byte count, fetch artifact, cited ranges, and its single claim row A24 all verify; (a) verbatim PASS, (b) true/no-overreach PASS, (c) attribution-relevant as an exposure-channel claim HOLDS.
