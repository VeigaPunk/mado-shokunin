# Staged rows vs lane registry — matrix (seat ConnStagedVsRegistry, round-43 w1)

Scope: the staged rows cited by the 11 staged gkeep-theme files
(`merge/mado/knowledge/corpus/knowledge/gkeep-geometry-unobservable-r8.md`,
`gkeep-rendered-geometry-chain-r9.md`, `gkeep-size-rule-application-r10.md`,
`gkeep-size-to-real-size-r11.md`, `gkeep-observation-route-r11.md`,
`gkeep-client-size-request-r12.md`, `gkeep-rendered-geometry-record-r13.md`,
`gkeep-rendered-geometry-record-r14.md`, `gkeep-geometry-never-recorded-r15.md`,
`gkeep-element-rules-r30.md`, `glyph-and-geometry-r31.md`) as written in
`merge/mado/SOURCES.append.md` and each file's `source:` lines. Lane registry:
`corpus/SOURCES.md` (226 rows, tops S289; freeze base a35cfdf).

Census used: `scripts/sources-census.sh` (fleet) `validate`; URL key is
`url_of` normalized (scheme+host lowercased, trailing `/` and fragment
stripped). E04 = same URL **within same scope**, non-rejected, no
`supersedes S…` teaches → fatal. W04 = same URL across scopes → warning.

## 1. Unique staged rows cited by the theme (25)

| staged id | staged source (kind/tier) | lane registry holds the resource? | verdict | basis |
|---|---|---|---|---|
| S251 | `~/.config/hypr/gkeep.conf` (own-work, A) | presence only: S014 (gate EXPECT pin, SOURCES.md:26); contents not held | NEW ROW via planned S297 pin | round-43 fetch receipt `host-gkeep.conf` is the byte copy (sha256 prefix 3726e488…, registration §51); open S297, do not open a second own-work row from staged text |
| S255 | gkeep upstream `ui.py` @ 133b867 (code, A) | no | NEW ROW | same URL also cited by staged S285, S312 → open one row (anchor `gkeep/ui.py:476` `window.set_default_size`) |
| S256 | nerd-fonts `glyphnames.json` @ v3.5.1 (dataset, A) | no | NEW ROW | grep `ryanoasis` in SOURCES.md: no match |
| S275 | `lanes/mado/round8/fetch/host-focus-grab-and-timeout.txt` (own-work, A) | no (unreachable) | REFUSE | private receipt; staged package has no `lanes/` tree; lane has no round-8 fetch dir; cannot be re-opened |
| S284 | Hyprland `Window.cpp` @ `v0.56.2` tag (code, A) | yes — S164 (commit form) | REUSE HELD S164 | grep A below; tag resolves to same commit efb5099 (registration §4,§47); census URL differs only by spelling (`v0.56.2` vs `efb5099…`) → no W04/E04 either way |
| S285 | gkeep `ui.py` @ 133b867 (code, A) | no | NEW ROW | with S255 (same URL) |
| S286 | `docs.gtk.org/gtk4/method.Window.set_default_size.html` (docs, A) | no | NEW ROW | grep F below: no match |
| S287 | `wiki.hypr.land/0.56.0/Configuring/Basics/Window-Rules/` (docs, A) | no | NEW ROW | grep H below: no match; adjacent wiki rows exist (S017 current, S023 v0.54.0, S165 raw current) but not the 0.56.0 page |
| S292 | `lanes/mado/round9/fetch/gkeep-geometry-chain.txt` (own-work, A) | no (unreachable) | REFUSE | private receipt |
| S293 | `lanes/mado/round9/fetch/host-compositor-log-scan.txt` (own-work, A) | no (unreachable) | REFUSE | private receipt |
| S297 | Hyprland `WindowRuleApplicator.cpp` @ `v0.56.2` tag (code, A) | yes — S155 (commit form) | REUSE HELD S155 | grep B below |
| S298 | Hyprland `Window.cpp` @ `v0.56.2` tag (code, A) | yes — S164 (commit form) | REUSE HELD S164 | grep A below |
| S299 | `lanes/mado/round10/fetch/host-r4-observation-sweep.txt` (own-work, A) | no (unreachable) | REFUSE | private receipt |
| S302 | Hyprland `DefaultFloatingAlgorithm.cpp` @ tag (code, A) | no | NEW ROW via pinned S292 | round-43 fetch receipt `Hyprland-DefaultFloatingAlgorithm.cpp` (commit form) |
| S303 | Hyprland `Target.cpp` @ tag (code, A) | no | NEW ROW via pinned S293 | fetch receipt `Hyprland-Target.cpp` |
| S304 | Hyprland `WindowTarget.cpp` @ tag (code, A) | no | NEW ROW via pinned S294 | fetch receipt `Hyprland-WindowTarget.cpp` |
| S305 | Hyprland `GeometricMovableAnimated.cpp` @ tag (code, A) | no | NEW ROW via pinned S295 | fetch receipt `Hyprland-GeometricMovableAnimated.cpp` |
| S310 | `lanes/mado/round11/fetch/host-gkeep-rule-and-path.txt` (own-work, A) | no (unreachable) | REFUSE | private receipt |
| S311 | Hyprland `Window.cpp` @ tag (code, A) | yes — S164 | REUSE HELD S164 | grep A below |
| S312 | gkeep `ui.py` @ 133b867 (code, A) | no | NEW ROW | with S255 |
| S318 | Hyprland `Window.cpp` @ tag (code, A) | yes — S164 | REUSE HELD S164 | grep A below |
| S319 | Hyprland `Window.cpp` @ tag (code, A) | yes — S164 | REUSE HELD S164 | grep A below |
| S320 | `lanes/mado/round13/fetch/host-journal-map-log-sweep.txt` (own-work, A) | no (unreachable) | REFUSE | private receipt; lane round-13 dir exists without `fetch/` |
| S326 | `lanes/mado/round14/fetch/host-journal-map-log-alltime-sweep.txt` (own-work, A) | no (unreachable) | REFUSE | private receipt; lane round-14 dir exists without `fetch/` |
| S339 | `lanes/mado/round15/fetch/corpus-round24-artifacts-sweep.txt` (own-work, A) | no (unreachable) | REFUSE | private receipt; lane round-15 dir exists without `fetch/` |

Tally: reuse held 5 (S284, S297, S298, S311, S318, S319 via S155/S158/S164 — 6 citations, 5 distinct staged rows), new rows 8 (S251→S297, S255/S285/S312→1, S256, S286, S287, S302→S292, S303→S293, S304→S294, S305→S295), refuse 8 (S275, S292, S293, S299, S310, S320, S326, S339).

## 2. Tier / community / province

- All 25 cited staged rows are tier A; **none** is tier C or community.
- Staged community/tier-C rows exist elsewhere in SOURCES.append.md (S210, S211, S216, S217, S230, S244, S277, S323, S333, S334, S347, S348) but none is cited by the gkeep-geometry theme; the Chinese/Japanese documentation-channel ones are outside PROVINCE.md anyway.

## 3. Staged-id collisions with lane-held ids

Staged ids S284-S287 collide with lane-held rows of the same ids (different content):
- lane S284 = Hyprland focus-grab impl `FocusGrab.cpp` (SOURCES.md:233)
- lane S285 = Quickshell `HyprlandFocusGrab` client (SOURCES.md:234)
- lane S286 = xdph `PortalManager.cpp` v1.4.1 (SOURCES.md:235)
- lane S287 = Hyprland issue #565 (SOURCES.md:236)

Any row opened for a staged citation MUST take a free id (≥ S290); appending the staged id would be an E03 duplicate-id. The other cited staged ids (S251, S255, S256, S275, S292, S293, S297-S299, S302-S305, S310-S312, S318-S320, S326, S339) are free in the lane registry (grep for each id in SOURCES.md: no match).

## 4. Private receipts — contraindicated

8 of 25 cited staged rows source from `lanes/mado/roundN/fetch/...` (N = 8, 9, 10, 11, 13, 14, 15). Verified:
- staged package `/home/vgpnk/Projects/shokuknow/merge/mado/` has no `lanes/` tree (glob: path not found);
- lane `.ufo/waves/round-{13,14,15}/` exist but hold no `fetch/` subdir; rounds 8-12 fetch dirs absent.
→ these receipts cannot be re-opened anywhere; refuse; the C2 entry must not cite them.

## 5. Census W04/E04 for new rows S290-S299 (the entry's planned rows)

New rows cite commit-form URLs from the round-43 fetch pins. Three planned rows touch URLs already held:
- **S291** (WindowRuleApplicator.cpp @ efb5099) = URL of held **S155** (SOURCES.md:167)
- **S296** (HyprCtl.cpp @ efb5099) = URL of held **S158** (SOURCES.md:170)
- S290 (RegexMatchEngine.cpp), S292-S295 are new files → no duplicate. S297/S298/S299 are local-path sources (no URL) → no E/W04.

Baseline (live lane, `validate --today 2026-10-26`): exit 0, E-free; existing warnings:
```
mado-shokunin	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado-shokunin	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado-shokunin	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado-shokunin	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado-shokunin	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado-shokunin	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado-shokunin	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado-shokunin	W01	S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md
```

**Case A — distinct scope (e.g. `C2-gkeep-geometry`): exactly two new W04 lines, validation still passes (exit 0).** Reproduced with the actual held rows S155/S158/S164 + proposed S290-S299 (fixture A, evidence/fixtureA-SOURCES.md):
```
a-shokunin	W04	S291 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.cpp across scopes
a-shokunin	W04	S296 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp across scopes
```
(remaining fixture E11 lines are artifacts of the fixture lacking `corpus/knowledge/…` files, not real findings)

**Case B — S291/S296 reuse the held rows' scope strings (S155 scope "Window-rule matching, static and dynamic application, property masks, reset, and setter priority"; S158 scope "`clients` JSON tags, `getprop` property response, `layers` output, registered rule-list commands"): E04 fires, validate fails (exit 1).** Reproduced (fixture B):
```
b-shokunin	E04	S291 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.cpp within scope Window-rule matching, static and dynamic application, property masks, reset, and setter priority
b-shokunin	E04	S296 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp within scope `clients` JSON tags, `getprop` property response, `layers` output, registered rule-list commands
```

Recommendation for the entry: do not open S291/S296 at all — cite held S155/S158 (their anchored line ranges already cover the appliedator size arm and the `clients` JSON `size` emission); only if a row must exist for counter pinning, give it a distinct scope (W04 only) or a `supersedes S155`/`supersedes S158` teaches.

## 6. Exact grep outputs (verified)

```
$ grep -n 'efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window\.cpp' corpus/SOURCES.md
176:| S164 | Hyprland v0.56.2 CWindow implementation — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp | code | A | …

$ grep -n 'efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator\.cpp' corpus/SOURCES.md
167:| S155 | Hyprland v0.56.2 WindowRuleApplicator.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.cpp | code | A | …

$ grep -n 'efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl\.cpp' corpus/SOURCES.md
170:| S158 | HyprCtl.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp | code | A | …

$ grep -n 'hyprwm/Hyprland/v0\.56\.2/' corpus/SOURCES.md   → no match (rc=1)
$ grep -n 'VeigaPunk/gkeep' corpus/SOURCES.md                 → no match (rc=1)
$ grep -n 'docs\.gtk\.org' corpus/SOURCES.md                 → no match (rc=1)
$ grep -n 'ryanoasis' corpus/SOURCES.md                      → no match (rc=1)
$ grep -n 'wiki\.hypr\.land/0\.56\.0/Configuring/Basics/Window-Rules' corpus/SOURCES.md → no match (rc=1)
$ grep -n 'gkeep\.conf' corpus/SOURCES.md
26:| S014 | mado gate — `tools/mado-verify.sh` | … EXPECT gains `~/.config/hypr/gkeep.conf` …
```

## 7. Evidence

- `evidence/fixtureA-SOURCES.md`, `evidence/fixtureB-SOURCES.md` — census fixtures (held rows S155/S158/S164 + proposed S290-S299; B differs in S291/S296 scope).
- Census runs: live lane validate (exit 0, lines quoted in §5), fixture A (W04 S291/S296), fixture B (E04 S291/S296).
- Registration cross-references: pins byte-identical to round-42 (`registration.md:45-55`); `v0.56.2` tag = commit `efb50993780079460b0cbed1363e2166a2de1d9f` (`registration.md:4`).
