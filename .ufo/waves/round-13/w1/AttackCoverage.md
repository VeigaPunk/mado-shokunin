# AttackCoverage — U4 knowledge admission (round 13, w1, critic)

Seat: `MadoR13.AttackCoverage` (critic, leaf; no dispatch, no background jobs). Status: findings only. I did not judge, admit, edit, integrate, ship or run checks.
Attacked: the integrated entry `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/wayland-protocol-boundaries-r13.md` (working tree, untracked, 2026-10-20 01:12 -03), rows S005 and S040–S043 in `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` (working tree, uncommitted), and the drafts `ProtocolPhases.md`, `GlobalCapture.md`, `globals.json`, `SourceRevision.md`, `ReviewPhases.md` and `ProtocolRecon.md` under `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/`.
Axes: **coverage** (does `covers: U4` mean all three facets are on sourced ground?) and **operability** (can the pins and recheck commands be re-run and still give the same identity?).

## Verdict input (for L1; not a verdict)

- **C1 4/7 can stand only after A1 is fixed.** A1 is a false observation statement inside the admitted entry. A4 and A8 change cells in rows that are new this round, so they cost almost nothing before commit. Nothing else here requires the judge to reject the claim.
- **The counter alone cannot support 4/7 (A2).** An entry holding only the header still scores U4. L1 has to record a hand facet check next to the count.
- **Attacks that failed (they hold up):** the entry cites no tier-B or tier-C source (S008, S009 and S010 stay queued). S005's immutable anchor was left untouched. U5–U7 are fenced. The rejection "name/version encodes phase" is true when measured (A3, A5).

## Findings, most severe first

### A1 — The third facet, "unexercised behavior", is stated falsely (fix before admission)

- **Counterexample.** The entry's `wp_color_manager_v1` row reads "Registry advertisement only; no HDR, renderer or display-path verdict" (`wayland-protocol-boundaries-r13.md:55`). Line 42 says `wayland-info` "may bind interfaces". In fact `wayland-info` 1.3.0 does more than list the registry when one of these interfaces is advertised:
  - Its `global_handler` binds 10 interface types: `wl_seat`, `wl_shm`, `zwp_linux_dmabuf_v1`, `wl_output`, `wp_presentation`, `zwp_tablet_manager_v2`, `zxdg_output_manager_v1`, `wp_drm_lease_device_v1`, `wp_color_manager_v1` and `wp_color_representation_manager_v1` (`wayland-info.c:3125-3145`).
  - It then sends query requests on those objects:
    - `zxdg_output_manager_v1_get_xdg_output` (`:1775`);
    - `zwp_linux_dmabuf_v1_get_default_feedback` (`:2031`);
    - `wp_color_manager_v1_get_output` (`:2744`);
    - `wp_color_management_output_v1_get_image_description` (`:2750`);
    - `wp_image_description_v1_get_information` (`:2626`).
  - The capture's own `excluded` list includes "wp_color_manager_v1 display colorimetry blocks" and "zwp_linux_dmabuf_v1 device and modifier blocks" (`globals.json:331-341`). That data only exists because those objects were bound and queried.
  - `-i` does not narrow the interaction. It filters printing only (`:3163`, help text `:3202-3203`); binding happens unconditionally in `global_handler`.
- **Impacted axes.** Coverage: the entry separates advertisement from bind/use, yet mislabels its own probe. This breaks QUALITY criterion 3 (`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md:6`). Operability: a re-run "advertisement only" probe is not what actually ran.
- **Smallest safe correction.**
  - Rename the table column at `:50` from "Bound of observation" to "Retained in S041".
  - Replace "may bind" at `:42` with: "`wayland-info` 1.3.0 binds up to ten interface types when advertised and issues read-only information requests on `zxdg_output_manager_v1`, `zwp_linux_dmabuf_v1` and `wp_color_manager_v1`. S041 retains only the registry headers."
  - Ground it with a new code row for `wayland-info.c` @ tag 1.3.0 (open record O1 below), or tag the sentence `[INFERENCE]` if no row is added.
  - The capture stays valid. It was not a mutation, and nothing in GlobalCapture's no-injection boundary is violated.

### A2 — The counter scores an empty U4 entry as covered (do not accept 4/7 on the counter alone)

- **Counterexample, run on a scratch copy** at `/tmp/acov/cx`, 2026-10-20 (the repo was not touched):
  - I cut the entry down to its 4 header lines plus "Nothing about phases or globals."
  - The round-12 C3 loop (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/evidence/round-12/after-measure.sh:24-25`) still printed `covers: U1`…`covers: U4`.
  - The source join printed nothing for the entry. Its only output was two in-flight lines for `corpus/lessons/round-13.md` (see A11).
  - The rubric (`SCORECARD.md:237`, `:334-338`) checks the header join. It never checks facet content.
- **Impacted axes.** Coverage (premature saturation risk). Calibration of the verdict.
- **Smallest safe correction.** Do not change the pre-registered counter mid-round. Record a facet check next to the C1 count instead, for example:
  - `grep -cE '^\| (Which upstream|Which interface/version|Does the intended)' corpus/knowledge/wayland-protocol-boundaries-r13.md` → `3`;
  - the header cites at least one mined phase row (S005/S040) **and** at least one mined advertisement row (S041/S043).
  - Label it as a hand check by a non-author (QUALITY criterion 12).

### A3 — The phase table assumes every advertised protocol has a phase; 27 of 71 do not

- **Counterexample.** The table "Upstream category" (`:22-28`) has five categories, and the route at `:14` sends readers to "its owning repository's XML, README and pinned release".
  - I joined `globals.json` against the host's installed `wayland-protocols 1.49-1` XML (`/usr/share/wayland-protocols/{stable,staging,unstable}`) and `/usr/share/wayland/wayland.xml`. Of the 71 distinct advertised interfaces:
    - **44** are in wayland-protocols: stable 5, staging 27, unstable 12;
    - **6** are core `wayland.xml`: `wl_seat`, `wl_data_device_manager`, `wl_compositor`, `wl_subcompositor`, `wl_shm`, `wl_output`. The core protocol has no phase;
    - **21** come from other repositories: `zwlr_*` 8, `hyprland_*` 8, `org_kde_kwin_server_decoration_manager`, `wl_drm`, `vicinae_hotkey_manager_v1`, and the two `zwp_` names `zwp_input_method_manager_v2` and `zwp_virtual_keyboard_manager_v1`, which do not appear in wayland-protocols at all.
  - GlobalCapture's crosswalk (`GlobalCapture.md:169-175`) puts the 6 core interfaces in "outside" together with the 21. Core and foreign are different authorities.
  - `hyprland_*` has no wayland-protocols phase. ReviewPhases found no "hypr" entry in MEMBERS.md (`ReviewPhases.md:46`).
- **Impacted axes.** Coverage: the phase facet is unanswerable through S005/S040 for 38% of the host sample. Calling the U4 phase facet "covered" needs an explicit "phase not applicable" branch.
- **Smallest safe correction.**
  - Add one table row: "core `wayland.xml` or other repository | S005/S040 do not apply; core = S043; others need their own authority | 'every advertised global has an upstream phase'".
  - Add an `[OBS]` sentence with the 44/6/21 split and a re-derivation command, pinned to the host 1.49-1 tree or tag 1.49 (not `main`; see A6).

### A4 — Unsupported host-version inference: the advertised set depends on config, hardware and sandboxing, not only on Hyprland 0.56.2

- **Counterexample (Hyprland v0.56.2 source, commit `efb5099…` = host `hyprctl` commit).** `src/managers/ProtocolManager.cpp` registers globals conditionally:
  - `wp_commit_timing_manager_v1` only `if (*PENABLECT)` = `render:commit_timing_enabled` (`:137`, `:225-226`);
  - `wp_color_manager_v1` only `if (*PENABLECM)` = `render:cm_enabled`. Its **advertised version** is config-selected: `*PCMV1_2 ? 3 : 1`, from `experimental:wp_cm_1_2` (`:134-136`, `:234-235`);
  - `wp_drm_lease_device_v1` once per DRM backend whose lease is `good()` (`:239-246`). This explains the two lease advertisements;
  - `wp_linux_drm_syncobj_manager_v1` only with explicit sync plus syncobj-timeline support (`:249-255`);
  - `zwp_linux_dmabuf_v1` and `wl_drm` only when DRM formats are non-empty (`:258-263`).
- **Sandbox filtering.** `src/Compositor.cpp:262-266` (`filterGlobals`) plus `:283` (`wl_display_set_global_filter`) hide every non-whitelisted global from security-context-sandboxed clients. The whitelist is at `ProtocolManager.cpp:348-403`.
- **Measured.** Every interface named in `ProtocolManager.cpp` (69) appears in `globals.json`. The two advertised names not in that file are the image-capture-source managers, which are created in another constructor. So every gate was true on this host at capture time. The capture therefore tells us about this host's config and GPU, and about an unsandboxed client.
- **Why it matters.** The entry rightly calls `wp_color_manager_v1`/3 "an advertisement example". But S041's scope cell reads "This client's time-bound Hyprland 0.56.2 interface/version advertisements". That invites the reading "0.56.2 advertises v3". On this source, a 0.56.2 host with default `experimental:wp_cm_1_2` off, or with `render:cm_enabled` = 0, advertises v1 or nothing. (The defaults were not checked.)
- **Impacted axes.** Coverage (host boundary). Operability: a recheck on another session or config "fails" for reasons other than drift.
- **Smallest safe correction.**
  - S041 is new this round and uncommitted. Set its scope to "advertisements to one unsandboxed client, under this host's config and DRM hardware, Hyprland 0.56.2 `efb5099`".
  - Add one Limits sentence: "Hyprland 0.56.2 registers several globals and versions conditionally on config and DRM capability and filters globals for sandboxed clients", anchored by open record O2 as a new code row, or tagged `[INFERENCE]`.
  - Record the socket-to-instance join in the recheck checklist. `hyprctl` uses its own IPC, not `wayland-1`. I observed exactly one `wayland-N` socket and one Hyprland instance directory under `/run/user/1000` at 2026-10-20T04:1xZ. That was after the capture, so I cannot attest it for 04:10:03Z.

### A5 — Observed counterexample that spec text predicts advertisement: `xwayland_shell_v1`

- **Evidence.** `globals.json` lists `xwayland_shell_v1@1` (GlobalCapture row #40), seen by the non-Xwayland client `wayland-info`. The staging XML says "A compositor must not allow clients other than Xwayland to bind to this interface. A compositor should hide this global from other clients' wl_registry." (`/usr/share/wayland-protocols/staging/xwayland-shell/xwayland-shell-v1.xml:67-69`, wayland-protocols 1.49-1).
- In Hyprland 0.56.2 the only filter is the sandbox filter (A4), so unsandboxed clients see it.
- **Use.** This is the strongest local `[OBS]` for the entry's rule that "phase and spec do not predict advertisement, and advertised does not mean intended for this client". It needs no new probe.
- **Never bind it to "test" it.** The spec makes that an implementation-defined error, outside any authorized scope.
- **Correction (optional, coverage gain).** Add one `[OBS]` + `[INF-docs]` line under "Advertisement, binding and behavior".

### A6 — Two authorities for the same upstream pin (low; fix the new-row cell before commit)

- **The conflict.**
  - S040 is pinned to `main` `35d9638c…` (2026-10-12), which is newer than the last release.
  - ProtocolPhases pins the same file to tag `1.49` → commit `ee78491a…`, blob `b09930ca…` (`ProtocolPhases.md:24`).
  - ReviewPhases recommends `main` (`ReviewPhases.md:81`).
  - GlobalCapture classified phases against `main` `35d9638c` (`GlobalCapture.md:198-208`).
  - The host has `wayland-protocols 1.49-1`, and the README says "Each release … finalizes the version of the protocols" (`README.md:255-256`).
- **Measured: no result changes.**
  - The GitLab compare from `ee78491a` to `35d9638c` shows 7 commits and XML edits, but only GOVERNANCE `:174` changes in the governance files ("persuant" → "pursuant").
  - `README.md` is byte-identical (sha256 `e81ad629…`) at `3dac056d`, tag 1.49 and `main`.
  - All 45 phased line/version anchors in GlobalCapture's table match the host's installed 1.49-1 XML exactly (scripted check: 45 checked, 0 mismatches).
  - `main` adds the experimental `xx_hotkey_manager_v1` and `xx_image_capture_color_manager_v1`, which no release has.
- **Correction.** Before commit, append to S040's anchor: "= tag 1.49 `ee78491a` except GOVERNANCE.md:174 spelling". Classify any per-interface phase against tag 1.49 or the installed 1.49-1 tree, never against unreleased `main`.

### A7 — SourceRevision draft: wrong line anchors and a tag/commit identity mix-up (reject if merged into `lessons/round-13.md` § Gate)

- **Line anchors.** `SourceRevision.md` claims its quotes come from blob `e81ad629…`. Checked against that blob, these locations are wrong:
  - "There is no expectation…" is cited `:179-181`, but is at `:194-195`;
  - the staging disclaimer is cited `:194-197`, but is at `:211-214`;
  - "Once it has been concluded…" is cited `:207-209`, but is at `:223-225`;
  - "Note that the major version…" is cited `:213-215`, but is at `:230-231`;
  - "Protocols shall try…" is cited `:154-155`, but is at `:170-171`;
  - the deprecation quote is cited `:53-54`, but is at `:52-53`;
  - the legacy `z` quote is cited `:63-65`, but is at `:61-63`;
  - its section spans "(170–184, 186–205, 207–238)" are really experimental `:184-197`, staging `:199-219`, stable `:221-251`.
- **Identity mix-up.** It gives "Target Commit: `a8d65d7f…`" for tag 1.49. That is the annotated **tag object**; the commit is `ee78491a…` (ProtocolPhases `:33` has this right).
- **Contract problem.** Its recommendation to widen S005's `anchor` span is an in-place edit of an immutable cell; only `status`, `recheck` and `used-by` may change (`SOURCES.md:3-7`). L1 correctly left the anchor alone.
- **Contrast.** ProtocolPhases' line anchors all check out against `e81ad629…`; spot-checked 21 spans.
- **Correction.** Take line numbers only from ProtocolPhases. If the wider S005 span is wanted, carry it in the lesson Gate entry.

### A8 — S041's immutable anchor has no content identity (fix before commit)

- **Counterexample.** S041's anchor is "captured_utc …; probe rc 0; tool …; compositor efb5099…" with no sha. The census checks that `used-by` paths exist, not anchor paths (`after-measure.sh:33`). If `globals.json` were left out of the commit, or changed later, the row would still pass.
  - Note: `.ufo/waves/` is not gitignored (`.gitignore` ignores only `.ufo/interactive-sessions/`), so the file can be committed.
- **Correction.**
  - Add `set_sha256 9569d02fe2b04bf62079258b1d74f5d2ad8510c26ef0710a1a64c95f1a9becaa` to the anchor. It is a property of the content, so it does not depend on the commit.
  - Add the work-window file sha `d9169df49ef26b5b2ba044fcd3808ccf37a1b0fba4d31f1aa6c268dac877716c`, labelled provisional, to be re-bound with `git show <commit>:…` (QUALITY criteria 7, 8, 13).
  - Commit `globals.json` in the same commit as the row.

### A9 — S042 page pin: the branch choice matters (low)

- **Evidence.**
  - The served `https://wayland.freedesktop.org/extras.html` (sha256 `97467f81…`, fetched 2026-10-20) is byte-equal to `raw/main/extras.html`. `main` is the project's default branch, head `c0c9d30d…`.
  - The file was last touched by `8923a199…` (2026-01-15, "extras: mention wl-proxy"), which is S042's pin.
  - The `master` branch also exists. Its `extras.html` is a different blob (sha256 `9eabc717…`), last touched `04c4f396…` in 2021.
  - The page text "list all global interfaces advertized by the compositor" means all globals visible to that client (A4 sandbox filter, A5).
- **Correction.** Append "branch main" to S042's anchor before commit. The entry already scopes advertisement to "this client", so the entry itself needs no change.

### A10 — S043 has two anchors for one authority (low)

- S043 cites both the installed `/usr/share/wayland/wayland.xml` (wayland 1.26.0-1, sha256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`; `wl_registry` spans `:117-178` and `global_remove` is at `:163`) and the unpinned website `docs/html/apa.html`.
- The website is generated from whatever Wayland version was deployed.
- **Correction.** Make the installed XML plus its sha the authority. Treat the website URL as a locator only.

### A11 — In flight, not a settled defect

On the scratch copy of the current tree, the join printed `row S017 used-by corpus/lessons/round-13.md does not cite it` and the same for S044, because `corpus/lessons/round-13.md` does not exist yet. This is a mid-edit state (QUALITY criterion 9). L1 should re-run the join after the lesson lands.

### A12 — Installed trees can never classify experimental globals (low; recheck checklist)

- Upstream `meson.build` @ tag 1.49 adds stable, staging and unstable files to `installed_protocol_files` (`:118,131,144`). Experimental files go only into `protocol_files` (`:157`), and only `installed_protocol_files` is installed (`:167-177`). File sha256 `6f09b022…`.
- So the host has no `experimental/` directory, even though the 1.49 tree has 7 `xx-*` directories. A host-local lookup would label an advertised `xx_*` global "outside".
- The 1.49 tree also has no `deprecated/` directory, so zero deprecated protocols exist at 1.49.
- **Correction.** In "Safe recheck checklist", classify against the upstream tag tree, not `/usr/share/wayland-protocols`, whenever an `xx_` name appears.

### A13 — Experimental compatibility wording changed recently (watch)

- Commit `7bc5f735…` (2026-01-16) deleted "A protocol in the experimental phase should expect to see backward incompatible changes at any time" along with its procedure. The current text puts every phase under "Backward-incompatible changes can only be introduced in a new major version of a protocol" (`README.md:24-25`).
- The entry's experimental row (`:24`) is consistent with the current text.
- Any older copy or mirror (S010 wayland.app, S008 book) quoting the "at any time" wording is stale against S005. This is one more reason they stay queued and uncited.

## Source opens (this seat, accessed 2026-10-20)

| # | Source / URL | Exact quote (≤25 words) + location | Revision | Tier / kind | Admission | Flip |
|---|---|---|---|---|---|---|
| O1 | https://gitlab.freedesktop.org/wayland/wayland-utils/-/raw/1.3.0/wayland-info/wayland-info.c | "-i\|--interface <interface>: Only print information about the Wayland globals containing <interface> in their name" — `:3202-3203`; `wp_color_manager_v1_get_output(` — `:2744` | tag 1.3.0 → `d01edd68961ca01779dcb96afe56c2d99ff79067` (2025-11-24); file sha256 `fcdc6c09d8111c8bcec407299be9ef582105c8ff954ebf9b57fa25b5e86c46a6`; host package 1.3.0-1 | A / code | Candidate row: what the probe binds and requests (A1) | A new wayland-utils release changes `global_handler`; or the host package version ≠ 1.3.0 |
| O2 | https://github.com/hyprwm/Hyprland/blob/v0.56.2/src/managers/ProtocolManager.cpp | "PROTO::colorManagement = makeUnique<CColorManagementProtocol>(&wp_color_manager_v1_interface, *PCMV1_2 ? 3 : 1, \"ColorManagement\", *PDEBUGCM);" — `:235` | tag v0.56.2 → commit `efb50993780079460b0cbed1363e2166a2de1d9f` (GitHub ref API, type commit); sha256 `b4a91b2647f3bb80dd28b41377465916c00ba84da9f3494370bd90302b9e8622` | A / code | Candidate row: conditional registration and version (A4). Scope is the source only, never a host result | The host `hyprctl` commit differs from `efb5099` |
| O3 | https://github.com/hyprwm/Hyprland/blob/v0.56.2/src/Compositor.cpp | "if (!PROTO::securityContext->isClientSandboxed(client)) return true;" — `:263-264`; "wl_display_set_global_filter(m_wlDisplay, ::filterGlobals, nullptr);" — `:283` | same commit; sha256 `74833ecbf0e2b6f8ad84345ac0716a3295a0e347420a188be0ab4f6a684af7c0` | A / code | Candidate (same row as O2): advertisement depends on the client (A4, A5) | As O2 |
| O4 | `/usr/share/wayland-protocols/staging/xwayland-shell/xwayland-shell-v1.xml` | "A compositor must not allow clients other than Xwayland to bind to this interface. A compositor should hide this global from other clients' wl_registry." — `:67-69` (24 words) | wayland-protocols 1.49-1 (pacman, built 2026-06-07) | A / spec | Supports A5 as `[INF-docs]`; the host advertisement is `[OBS]` from S041 | A later release changes the paragraph |
| O5 | https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/README.md | "Note that the major version of the stable protocol, as well as all the interface versions and names, must remain unchanged." — `:230-231` | tag 1.49 `ee78491a…`; blob sha256 `e81ad629…` (same as S005) | A / docs | Already within S005. It is the README rule that makes prefix → phase impossible (A3); no new row needed | README changes the promotion rule |
| O6 | `/usr/share/wayland-protocols/unstable/linux-dmabuf/linux-dmabuf-unstable-v1.xml` | "Disclaimer: This protocol extension has been marked stable. This copy is no longer used and only retained for backwards compatibility." — `:94-95` | wayland-protocols 1.49-1 | A / spec | Grounds the "a name in both stable/ and unstable/ resolves to stable" rule GlobalCapture used | Disclaimer removed |
| O7 | https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/meson.build | `installed_protocol_files += unstable_protocol_files` (`:144`) versus `protocol_files += experimental_protocol_files` (`:157`) | tag 1.49; sha256 `6f09b022a334de6c6ecbce095db8816a102993b29f46d340348a684f4c12d5ad` | A / code | Supports A12 only | A release installs experimental XML |
| O8 | https://wayland.freedesktop.org/extras.html (+ `raw/main` and `raw/master` of `wayland/wayland.freedesktop.org`) | "Running wayland-info will list all global interfaces advertized by the compositor." — §Compositor features, html `:19-20` | served = main sha256 `97467f81…`; last touch `8923a19916635c21a3577b616f650a7e45d70fa9`; master blob `9eabc717…` (2021) | A / docs | Confirms S042's pin; rejects any master-branch pin (A9) | The deployed branch changes |
| O9 | GitLab API `repository/compare?from=ee78491a…&to=35d9638c…` and `commits/7bc5f735…/diff` | (API metadata; no prose quote) | 7 commits; README untouched; GOVERNANCE differs only at `:174` | A / dataset | Supports A6 and A13 | — |

Rejected for use as support: S008 (tier B, draft book), S009 (no page revision), S010 (tier C). The entry already does not cite them. No change needed.

## Commands used (read-only; no repo writes beyond this file and its report)

- **Packages:**
  - `pacman -Q wayland wayland-protocols wayland-utils hyprland`;
  - `pacman -Qi …`: wayland-utils 1.3.0-1, installed 2026-10-20 01:06:49 -03; hyprland 0.56.2-2, built 2026-09-01; wayland-protocols 1.49-1, built 2026-06-07.
- **Disclosure:** I also ran a `grep` over `/var/log/pacman.log` for those three package names. Only package-transaction lines were read, and none are reproduced here beyond those install facts.
- **Upstream fetches:**
  - `curl` of the GitLab API and raw files for wayland-protocols, wayland-utils and wayland.freedesktop.org;
  - GitHub raw files for Hyprland v0.56.2.
  - Local copies under `/tmp/acov` are provenance only (QUALITY criterion 13).
- **Host file reads:** `/usr/share/wayland/wayland.xml` and `/usr/share/wayland-protocols/**` (read only).
- **Instance join:** `ls /run/user/1000 | grep -E '^wayland-'` and a count of `/run/user/1000/hypr/` entries. Instance signatures were not printed.
- **Not run:** no `hyprctl`, no `wayland-info`, and no compositor command of any kind.
- **Scratch counterexample (A2):** a copy of `corpus/` in `/tmp/acov/cx`, scored with the round-12 C3 and join loops.
- **Tooling record:** I installed or upgraded nothing. `wayland-utils 1.3.0-1` was installed earlier by `MadoR13.GlobalCapture` (pacman, recorded in `GlobalCapture.md:20-22`).

## Checks for L1 (not run by this seat)

1. After fixing A1 and A4: `grep -nE 'Bound of observation|may bind' corpus/knowledge/wayland-protocol-boundaries-r13.md` → no matches.
2. The A2 facet check, recorded next to the C1 count.
3. `jq -r '.globals[] | "\(.interface)@\(.version)"' .ufo/waves/round-13/w1/globals.json | sort | sha256sum` → `9569d02f…`, then `git show <commit>:.ufo/waves/round-13/w1/globals.json | sha256sum` to bind S041.
4. Re-run the round-12 join loop once `corpus/lessons/round-13.md` lands (A11).
