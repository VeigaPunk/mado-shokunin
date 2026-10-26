# RevEntryBar — Review of `07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/knowledge/hyprland-focus-grab-r41.md` against `corpus/QUALITY.md`, `CORPUS.md`, and `PROVINCE.md`

- **Seat:** `RevEntryBar` (reviewer, leaf — no subagent dispatch)
- **Round / Wave:** mado round 41, wave w2
- **Target revision:** DATA commit `07f2641696b5ac73de1404ea737a9f27e9819aa1` (base `ab2bfaab661c846d1de9d58c01651cd156a13949`, v2 freeze `294c667901a8c7b7165ba849d03cba9a24c14fa4`)
- **Target artifact:** `corpus/knowledge/hyprland-focus-grab-r41.md` (136 lines, sha256 `da1297719ef9a9da79d52e310a569e5466c4962fd14f26b38b4739a192cb1d5a`), plus its C2 companion surfaces at `07f2641696b5ac73de1404ea737a9f27e9819aa1` (`corpus/SOURCES.md`, `corpus/README.md`, `corpus/lessons/round-41.md`, `.ufo/waves/round-41/fetch/xdph-installed-version.txt`).

---

## §1 Severity-Ranked Defects (with exact file:line and reproduction)

### HIGH

#### D1 — `corpus/knowledge/hyprland-focus-grab-r41.md:10,73` and `corpus/lessons/round-41.md:32`: S037 (`releases/tag/v1.4.1`) is cited and Gate-bound to a local pacman `desc` receipt instead of its declared URL/anchor, and its `used-by` change is not logged `old -> new` in `corpus/lessons/round-41.md`
- **Attacks:** `corpus/QUALITY.md` criteria **2 / 42** ("Every claim carries a source: a measured anchor (path:line, command, evidence id)") & **27** (reproducible row anchor); `/home/vgpnk/Projects/shokunin/CORPUS.md:112-118` (SOURCES.md Contract v1 Rules 1 & 2: Gate quote grounds `teaches` from the opened source; `used-by` in-place edits logged `old->new` in the round lesson); `PRED-C2-r41-v2` residual (`quality/counters/c2-r41-focus-entry-v2.py:85`, "a held id's receipt is not pinned").
- **Exact lines:**
  - `corpus/knowledge/hyprland-focus-grab-r41.md:10`: `source: S037 - xdg-desktop-portal-hyprland v1.4.1 release (held row; installed package 1.4.1-2) - the identity of the portal whose journal this is`
  - `corpus/knowledge/hyprland-focus-grab-r41.md:73`: `**OBS** S037 (installed package record, read-only file read of /var/lib/pacman/local/xdg-desktop-portal-hyprland-1.4.1-2/desc): "%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2" ... This receipt grounds the *installed* version, not the release page: the tag anchor v1.4.1 and its commit cc8e5ef are S037's own row, not re-fetched this round.`
  - `corpus/SOURCES.md:49`: `| S037 | xdg-desktop-portal-hyprland v1.4.1 — https://github.com/hyprwm/xdg-desktop-portal-hyprland/releases/tag/v1.4.1 | docs | A | Installed XDPH upstream release identity and release-scoped changes | “v1.4.1”, “Changes”; tag commit cc8e5ef; released 2026-07-29 | ... | corpus/knowledge/xdg-portal-routing-r12.md, corpus/knowledge/hyprland-focus-grab-r41.md |`
  - `corpus/lessons/round-41.md:32`: `GATE S037 receipt=.ufo/waves/round-41/fetch/xdph-installed-version.txt sha256=4294737aa884fd84c2e2a6bf642efa71c281bc480df4f07eb64009d812157ea8 quote="%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2"`
- **Reproduction:**
  ```sh
  git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff ab2bfaab661c846d1de9d58c01651cd156a13949 07f2641696b5ac73de1404ea737a9f27e9819aa1 -- corpus/SOURCES.md
  git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 07f2641696b5ac73de1404ea737a9f27e9819aa1:.ufo/waves/round-41/fetch/xdph-installed-version.txt
  git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/lessons/round-41.md | grep -n 'xdg-portal-routing-r12'
  ```
  1. `S037` is a `kind = docs` row whose source URL is `https://github.com/hyprwm/xdg-desktop-portal-hyprland/releases/tag/v1.4.1` and whose anchor is `“v1.4.1”, “Changes”; tag commit cc8e5ef; released 2026-07-29`. Yet `GATE S037` binds `S037` to `.ufo/waves/round-41/fetch/xdph-installed-version.txt` (a local `/var/lib/pacman/local/xdg-desktop-portal-hyprland-1.4.1-2/desc` read), and `entry:73` explicitly admits the release page was not re-fetched and that the receipt grounds the local package record rather than `S037`'s release page. (By contrast, in `corpus/SOURCES.md:45`, the local pacman `desc` read is row `S033`, not `S037`; `ScrEntryB.md:118-131` and `ScrEntryC.md:90-96` both refused to cite `S037` for this exact provenance reason.)
  2. Furthermore, `CORPUS.md:116-117` (SOURCES Contract v1 Rule 2) requires: *"Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round lesson."* `corpus/SOURCES.md:49` mutates `S037`'s `used-by` in place from `corpus/knowledge/xdg-portal-routing-r12.md` to `corpus/knowledge/xdg-portal-routing-r12.md, corpus/knowledge/hyprland-focus-grab-r41.md`, but `corpus/lessons/round-41.md` never logs the `old -> new` `used-by` transition (`grep -c xdg-portal-routing-r12` on `round-41.md` is `0`).
- **Fix for L1:** Either (a) log `S037` `used-by` `old -> new` in `corpus/lessons/round-41.md` and replace `S037` with a dedicated `own-work` / host-bytes row or remove `S037` from `source:`/`GATE`/`used-by` (keeping the 7 pinned new rows `S283-S289`, which already satisfy `PRED-C2-r41-v2` clauses b, c, d, g), or (b) log `S037` `used-by: corpus/knowledge/xdg-portal-routing-r12.md -> corpus/knowledge/xdg-portal-routing-r12.md, corpus/knowledge/hyprland-focus-grab-r41.md` in `corpus/lessons/round-41.md` if `S037` is retained under the M41-6 disclosure.

---

### MEDIUM

#### D2 — `corpus/knowledge/hyprland-focus-grab-r41.md:85`: Overstated claim ("adding a window records it and *defers* the protocol call") contradicts `quickshell-grab.cpp:66`
- **Attacks:** `corpus/QUALITY.md` criteria **1 / 41** & **2 / 42** (claim stronger than / contradicted by its cited source line).
- **Exact line:** `corpus/knowledge/hyprland-focus-grab-r41.md:85`:
  `**OBS** S285 (FocusGrab::addWaylandWindow): "this->pendingAdditions.append(window); this->commitRequired = true;" - adding a window records it and *defers* the protocol call; sync() is the only place that commits.`
- **Reproduction:**
  ```sh
  git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 07f2641696b5ac73de1404ea737a9f27e9819aa1:.ufo/waves/round-41/fetch/quickshell-grab.cpp | sed -n '65,69p'
  ```
  Output:
  ```cpp
  void FocusGrab::addWaylandWindow(QWaylandWindow* window) {
  	this->add_surface(window->surface());
  	this->pendingAdditions.append(window);
  	this->commitRequired = true;
  }
  ```
  In `FocusGrab::addWaylandWindow` (`quickshell-grab.cpp:65-69`), `this->add_surface(window->surface());` is called **immediately** on line 66 before `this->pendingAdditions.append(window);` on line 67. Only when a `QWindow` does not yet have a `QWaylandWindow` or `wl_surface` (`FocusGrab::addWindow`, lines 21-53) is `addWaylandWindow` deferred to `surfaceCreated`/`visibleChanged`; once inside `addWaylandWindow`, the `add_surface` protocol request is sent immediately and only the `commit` protocol request (`this->commit()` in `sync()`, line 75) is deferred.
- **Fix for L1:** Change line 85 from `adding a window records it and *defers* the protocol call; sync() is the only place that commits.` to `adding a Wayland window sends add_surface immediately, records the window in pendingAdditions, and *defers* the commit; sync() is the only place that commits.` (keeps the Gate/OBS quote `"this->pendingAdditions.append(window); this->commitRequired = true;"` and `S285` intact).

#### D3 — `corpus/knowledge/hyprland-focus-grab-r41.md:69` vs `corpus/SOURCES.md:235` (and `232`): Internal count contradiction — `onGlobal` has 10 bind branches (and 6 protocol requests), while `SOURCES.md` says "nine" (and "four requests")
- **Attacks:** `corpus/QUALITY.md` criteria **2 / 42** & **10** (count accuracy against the source bytes); `/home/vgpnk/Projects/shokunin/CORPUS.md:34-38,112-115`.
- **Exact lines:**
  - `corpus/knowledge/hyprland-focus-grab-r41.md:69`: `... what follows is a fixed set of ten named branches - screencopy, global shortcuts, input capture ("if (INTERFACE == hyprland_input_capture_manager_v1_interface.name)"), xdg-output, toplevel export, wl_output, dmabuf, wl_shm, foreign toplevel, toplevel mapping.`
  - `corpus/SOURCES.md:235` (row `S286`):
    - `scope`: `Which advertised globals the installed portal logs and which nine it binds, and whether focus grab is among them`
    - `anchor`: `... :90-129 and :247-259 the bind branches (screencopy, global_shortcuts, input_capture, xdg_output, toplevel_export, wl_output, linux_dmabuf, shm, toplevel_mapping) ...` (omits `zwlr_foreign_toplevel_manager_v1` at `:249-255`)
    - `teaches`: `A Got interface line is a registry global reaching the portal before any bind, and the portal binds nine named interfaces none of which is the focus-grab manager`
  - `corpus/SOURCES.md:232` (row `S283` `scope`): `The two interfaces, four requests and one event that define a focus grab...` vs `corpus/knowledge/hyprland-focus-grab-r41.md:115` (`two interfaces, five requests, one event`) vs actual XML (`focus-grab-v1.xml`: 2 requests on manager + 4 requests on grab = **6** `<request>` elements, 5 distinct request names).
- **Reproduction:**
  ```sh
  git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 07f2641696b5ac73de1404ea737a9f27e9819aa1:.ufo/waves/round-41/fetch/xdph-PortalManager.cpp | grep -n 'INTERFACE =='
  git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 07f2641696b5ac73de1404ea737a9f27e9819aa1:.ufo/waves/round-41/fetch/focus-grab-v1.xml | grep -n '<request '
  ```
  `xdph-PortalManager.cpp` has **10** `INTERFACE ==` branches (lines 90, 95, 99, 102, 108, 113, 122, 246, 249, 257: 9 call `wl_registry_bind` directly in `onGlobal` and the 10th at `:249-255` constructs `CToplevelManager(name, version)` for `zwlr_foreign_toplevel_manager_v1_interface.name`). `focus-grab-v1.xml` has **6** `<request>` tags (`create_grab` :44, manager `destroy` :52, `add_surface` :79, `remove_surface` :91, `commit` :105, grab `destroy` :115 — 6 requests across 5 distinct member names).
- **Fix for L1:** Harmonize `S286` in `corpus/SOURCES.md:235` (`ten named branches — nine direct wl_registry_bind calls plus CToplevelManager for zwlr_foreign_toplevel_manager_v1`) and `S283` in `corpus/SOURCES.md:232` / `entry:115` / `README.md:70` (`six requests (five distinct names)`).

#### D4 — `corpus/knowledge/hyprland-focus-grab-r41.md:21,35,63,65,67,69,71,109`: Stated counts lack inline `<n> — <command> <date>` format and the journal slice count omits the expected 71-global set comparison (`S041`)
- **Attacks:** `corpus/QUALITY.md` criteria **10** ("Report each count as `<n> — <command> <date>` and rederive it from the named revision"), **11** (absence sweep with pinned version and matching locations), and **14** ("A census compares expected and observed sets and names both missing and extra members"); `/home/vgpnk/Projects/shokunin/CORPUS.md:34-41`.
- **Exact lines:**
  - `corpus/knowledge/hyprland-focus-grab-r41.md:21`: `the manager has exactly two requests`
  - `corpus/knowledge/hyprland-focus-grab-r41.md:63,65,67`: `journal sessions=2 adverts=78 interfaces=63 focus_grab=1`, `with 15 adverts`, `carries the other 63`, `63 distinct names, no name advertised twice`
  - `corpus/knowledge/hyprland-focus-grab-r41.md:69`: `a fixed set of ten named branches`
  - `corpus/knowledge/hyprland-focus-grab-r41.md:71`: `` `grep -in focus` over `PortalManager.cpp` exits 1 - the string does not occur in the file at all - and in the whole journal the string `focus` occurs exactly once ``
  - `corpus/knowledge/hyprland-focus-grab-r41.md:109`: `` `grep -rli 'focus_grab\|focus-grab\|focus grab' corpus PROVINCE.md SKILL.md tools` exits 1 at base ``
- **Reproduction:**
  ```sh
  python3 -c '
  import json, re
  s41 = json.load(open("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/globals.json"))
  s41_names = {g["interface"] for g in s41["globals"]}
  j = open("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/fetch/xdph-journal.txt").read().splitlines()
  s1 = {m.group(1) for l in j[:78] if (m := re.search(r"Got interface: (\S+)", l))}
  s2 = {m.group(1) for l in j[78:] if (m := re.search(r"Got interface: (\S+)", l))}
  print("S041 distinct:", len(s41_names), "s2 distinct:", len(s2), "missing in s2 vs S041:", sorted(s41_names - s2), "in s1:", sorted(s1))
  '
  ```
  Output:
  `S041 distinct: 71 s2 distinct: 63 missing in s2 vs S041: ['ext_foreign_toplevel_image_capture_source_manager_v1', 'ext_image_copy_capture_manager_v1', 'wl_drm', 'wl_output', 'wp_color_manager_v1', 'wp_drm_lease_device_v1', 'wp_linux_drm_syncobj_manager_v1', 'zwp_linux_dmabuf_v1'] in s1: ['ext_foreign_toplevel_image_capture_source_manager_v1', 'ext_image_copy_capture_manager_v1', 'wl_drm', 'wl_output', 'wp_color_manager_v1', 'wp_drm_lease_device_v1', 'wp_linux_drm_syncobj_manager_v1', 'zwp_linux_dmabuf_v1']`
  1. **Criterion 14 / Held-knowledge join:** `corpus/knowledge/hyprland-focus-grab-r41.md:67` states: *"Only the second session is a whole advertisement ... 63 distinct names, no name advertised twice - which is the only session that can be compared with the compositor's registry as a whole."* In fact, the lane already holds `S041` (`.ufo/waves/round-13/w1/globals.json`, `corpus/SOURCES.md:53`), which recorded **71** distinct globals on this same Hyprland `efb5099` build (including `hyprland_focus_grab_manager_v1` v1!), and the 8 globals missing from session 2 (`pid 1952`, 63 globals) are the **exact 8 distinct globals** present in session 1 (`pid 1918`, 15 adverts over 8 interfaces: `wl_output` ×6, `wp_drm_lease_device_v1` ×2, plus 6 singletons). Session 2 (`pid 1952`) is missing `wl_output` and `zwp_linux_dmabuf_v1` despite logging `Initializing xdph...` and `Gathering exported interfaces` (`xdph-journal.txt:81-83`). Calling session 2 "a whole advertisement" without naming the 8 missing globals (or citing `S041`'s prior capture of `hyprland_focus_grab_manager_v1` v1) violates Criterion 14's set-comparison rule and overlooks held datum `S041`.
  2. **Criterion 10:** Counts (`2`, `5`, `15`, `63`, `78`, `10`, `1`) are not written in the strict `<n> — <command> <date>` form (note that line 63 `journal sessions=2 adverts=78 interfaces=63 focus_grab=1` is required verbatim on its own line by `PRED-C2-r41-v2` clause h, so any `<n> — <command> <date>` addition must sit on an adjacent prose line, never altering line 63).
  3. **Criterion 11:** Line 71 scopes the `grep -in focus` negative sweep to `PortalManager.cpp` (`src/core/PortalManager.cpp`), without noting that `PortalManager.cpp:300` (`registry->setGlobal(...)`) is the single registry callback in xdph.

#### D5 — `corpus/knowledge/hyprland-focus-grab-r41.md:67,77,109`: Three `**INF**` paragraphs omit the explicit `Basis:` tag used by the other five `**INF**` paragraphs
- **Attacks:** Task prompt ("is each INF marked with its basis") and `corpus/QUALITY.md` criteria **2 / 42** & **3 / 43**.
- **Exact lines:**
  - `corpus/knowledge/hyprland-focus-grab-r41.md:37`: has `` `Basis:` S283's interface description and the `commit` request text. `` (OK)
  - `corpus/knowledge/hyprland-focus-grab-r41.md:55`: has `` `Basis:` S284's constructor, `start` and `finish`. `` (OK)
  - `corpus/knowledge/hyprland-focus-grab-r41.md:67`: **missing `Basis:`** (explains the basis in prose from S289's two sessions, but has no `Basis:` marker or S-id on the line)
  - `corpus/knowledge/hyprland-focus-grab-r41.md:75`: has `` `Basis:` S283, S286, S289. `` (OK)
  - `corpus/knowledge/hyprland-focus-grab-r41.md:77`: **missing `Basis:`** (cites S284 and `hyprctl version` in prose, no `Basis:` marker)
  - `corpus/knowledge/hyprland-focus-grab-r41.md:91`: has `` `Basis:` S285's `sync`, `startTransaction`, `completeTransaction`. `` (OK)
  - `corpus/knowledge/hyprland-focus-grab-r41.md:105`: has `` `Basis:` S283, S284, S287. `` (OK)
  - `corpus/knowledge/hyprland-focus-grab-r41.md:109`: **missing `Basis:`** (cites the base grep command and three corpus files in prose, no `Basis:` marker; also mixes an `[OBS]` command execution — `grep -rli ... exits 1 at base` — inside an `**INF**` paragraph).
- **Reproduction:**
  ```sh
  git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/knowledge/hyprland-focus-grab-r41.md | grep -n '^\*\*INF\*\*'
  ```
  5 of 8 `**INF**` lines carry `` `Basis:` ``; lines 67, 77, and 109 do not.

---

### LOW

#### D6 — `corpus/knowledge/hyprland-focus-grab-r41.md:97`: Quote from `issue-565.html:659` is a truncated clause prefix that drops the conditional `", unless that window's workspace is already the active one."`
- **Attacks:** Task prompt ("any claim stronger than its quote") and `corpus/QUALITY.md` criteria **1 / 41** & **2 / 42**.
- **Exact line:** `corpus/knowledge/hyprland-focus-grab-r41.md:97`:
  `**OBS** S287 (issue 565, body): the reporter's rule is windowrule = workspace 4 silent,^(pavucontrol)$ and the expectation is "If a workspace windowrule contains silent then matching windows should not get focus", while the observed behaviour is that "When the new window opens in a different workspace, it seems to steal it momentarily" and then hands focus back to the previous window.`
- **Reproduction:**
  ```sh
  git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 07f2641696b5ac73de1404ea737a9f27e9819aa1:.ufo/waves/round-41/fetch/issue-565.html | sed -n '659p'
  ```
  Output:
  `If a workspace windowrule contains <code class="notranslate">silent</code> then matching windows should not get focus, unless that window's workspace is already the active one.</p>`
  The full sentence is 22 words (within the 25-word limit), and its second clause qualifies the expectation (`unless that window's workspace is already the active one`). The entry's immediate continuation (`When the new window opens in a different workspace...`) supplies the different-workspace context, so the claim is not substantively false, but quoting the 13-word prefix without the `unless...` clause makes the quoted expectation look unconditional.

#### D7 — `corpus/README.md:70` and `corpus/SOURCES.md:286-449`: Companion-surface gaps (`README.md` row has 2 cells instead of 3; `SOURCES.md` `## Search log` has no round-41 note)
- **Attacks:** `/home/vgpnk/Projects/shokunin/CORPUS.md:46-48,82,126-128` (SOURCES Contract v1 Rule 5: `## Search log` one prose note per bounded search; `corpus/README.md` table schema `| Note | Holds | Sources |`).
- **Exact lines:**
  - `corpus/README.md:70`: `| knowledge/hyprland-focus-grab-r41.md (MADO-R41-1, round 41; ...) | Focus as a protocol surface: ... a decision table of what is observed, inferred and unknown. |`
  - `corpus/SOURCES.md:440-449`: `## Search log` ends at Round 28; no round-41 search-log note was appended.
- **Reproduction:**
  ```sh
  git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/README.md | awk -F'|' '/^\| `knowledge\// && NF!=5 {print NR, "NF=" NF, $2}'
  ```
  Output:
  `70 NF=4  `knowledge/hyprland-focus-grab-r41.md` (MADO-R41-1, round 41; assimilation of the focus-control theme, successor to the staged `focus-grab-protocol-live-on-host-r14` and the English-channel part of `focus-control-surfaces-r28`) `
  Every other row in `corpus/README.md` (lines 12–69, 58 rows) has `NF=5` (3 columns: `| Note | Holds | Sources |`); line 70 omits the `Sources` column (`S283–S289, S037 |`).

---

## §2 Verdict per Criterion in `corpus/QUALITY.md` (1–68)

Every numbered criterion in `07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/QUALITY.md` (lines 1–383, criteria 1–68) is evaluated below with one verdict (`pass` / `fail` / `n.a.`) and the exact line(s) of `corpus/knowledge/hyprland-focus-grab-r41.md` (or companion file).

| Criterion | `QUALITY.md` line | Summary | Verdict | Entry line(s) & Evidence |
|---|---|---|---|---|
| **1** (superseded by **41**) | `:3` | Every claim falsifiable or marked opinion | **fail** (minor, see 41) | `entry:85` overstates deferral of `add_surface` vs `quickshell-grab.cpp:66` (D2); all other lines (`1-84, 86-136`) falsifiable and verified against receipts. |
| **2** (superseded by **42**) | `:4-5` | Every claim carries a source: measured anchor (path:line, command, evidence id) | **fail** (see 42) | `entry:10,73` cites `S037` (a release-tag URL row) for a local `/var/lib/pacman/local/.../desc` receipt (D1); `entry:67` omits `Basis:`/S-id on the INF line (D5). |
| **3** (superseded by **43**) | `:6` | Observation, inference, and unknown stay separate | **fail** (minor, see 43) | `entry:109` tags a paragraph `**INF**` that contains a direct command observation (`grep -rli ... exits 1 at base`). All other `**OBS**` (`19,21,33,35,43,45,47,49,51,53,61,65,69,71,73,83,85,87,89,97,99,101,103`), `**INF**` (`37,55,67,75,77,91,105`), and `**UNK**` (`39,57,79,93,107`) stay separate, and `§6` (`113-126`) maps each question to `OBS`/`INF`/`UNK`. |
| **4** (superseded by **44**) | `:7` | Errata are append-only blocks | **n.a.** | New entry in round 41 (`entry:1-136`); no errata block yet. |
| **5** (superseded by **45**) | `:8` | A rejection is kept, not silently dropped | **pass** | `entry:15,136` and `corpus/lessons/round-41.md:35-36,45-46` explicitly keep and document the refusals of `privileged-client-surface-r29.md` and `focus-control-surfaces-r28.md` §3. |
| **6** | `:12` | Publish each pinned value with a re-derivation command and named revision; shortened hash must be a true prefix/suffix | **pass** | `entry:3-9,77,101`: full 40-hex commits (`cd1aba6bd78775825eb230b3a4274c48b6705eb7`, `efb50993780079460b0cbed1363e2166a2de1d9f`, `9b0f339b19057f4731bf3b48293307d7ef241671`), full 64-hex sha256 (`bf8fa91a...600aaf7`), tag `v1.4.1`, and `b09f157` (exact 7-char prefix of `b09f157b93576ccd5bd1038df2ab8f84f03ec4c8` in `issue-565.html`) + `cc8e5ef` (`entry:73`). |
| **7** | `:13` | Hash committed artifacts from `git show <commit>:<path>` | **pass** | `entry:9` (`bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7` = `git show 07f2641696b5ac73de1404ea737a9f27e9819aa1:.ufo/waves/round-41/fetch/xdph-journal.txt \| sha256sum`), plus all 8 Gate digests in `lessons/round-41.md:25-32`. |
| **8** | `:14` | Confirm path exists at named commit before treating as landed or recheck target | **pass** | `entry:9,15,109`: `.ufo/waves/round-41/fetch/xdph-journal.txt` exists at `07f2641696b5ac73de1404ea737a9f27e9819aa1`; `window-rule-effects-getprop.md`, `workspace-rules-r27.md`, and `rule-attribution-r24.md` exist under `corpus/knowledge/` at `ab2bfaab661c846d1de9d58c01651cd156a13949`. |
| **9** | `:15` | Bind each audit verdict to a commit or frozen-copy sha | **pass** | `entry:3-9,77,109` and `receipts/c2-v2-after-data.txt:26` (`rev=07f2641696b5ac73de1404ea737a9f27e9819aa1`). |
| **10** | `:16` | Report each count as `<n> — <command> <date>` and rederive from named revision | **fail** | `entry:21,63,65,67,69,71,109` state counts (`2`, `5`, `15`, `63`, `78`, `10`, `1`) in prose without the `<n> — <command> <date>` format (D4), and `SOURCES.md:232,235` disagrees with `entry:69,115` on `9` vs `10` branches and `4` vs `5` vs `6` requests (D3). All counts in the entry itself (`2`, `15`, `63`, `78`, `1`, `10`) re-derive accurately from the receipts. |
| **11** | `:17` | Absence claim about a tool includes `--help`/man/source sweep, pinned version, matching locations | **fail** (minor) | `entry:71` (`grep -in focus` over `PortalManager.cpp` exits 1, pinned at `v1.4.1` via `S286`/`S037`) and `entry:55` (nothing in `FocusGrab.cpp` consults a rule, pinned at `0.56.2`/`efb5099`). Minor gap: `entry:71` sweeps only `src/core/PortalManager.cpp` without stating why that single file suffices for the whole portal binary (`PortalManager.cpp:300` is the sole `wl_registry` callback) (D4). |
| **12** | `:18` | `[x]` requires a named non-author verifier and dispatching lane; lane seat stays `[~]` | **n.a.** | `entry:1-136` makes no `[x]` / SHONEN promotion claim (`lessons/round-41.md:67` keeps SHONEN `[~]`). |
| **13** | `:19` | Evidence meant to outlive a round is a committed path or quoted lines plus sha; `/tmp` provenance only | **pass** | `entry:3-10` and `lessons/round-41.md:25-32`: all 8 receipts are committed under `.ufo/waves/round-41/fetch/` at `07f2641696b5ac73de1404ea737a9f27e9819aa1` with sha256 and verbatim quotes; no `/tmp` path in the entry. |
| **14** | `:20` | Census compares expected and observed sets and names both missing and extra members | **fail** | `entry:63-67` calls session 2 (`63` distinct globals) "a whole advertisement ... that can be compared with the compositor's registry as a whole" without comparing it to the held `S041` registry capture (`71` distinct globals on the same Hyprland `efb5099` build) or naming the 8 globals missing from session 2 that were present in session 1 (`wl_output`, `zwp_linux_dmabuf_v1`, `wl_drm`, `wp_color_manager_v1`, `wp_drm_lease_device_v1`, `wp_linux_drm_syncobj_manager_v1`, `ext_image_copy_capture_source_manager_v1`, `ext_image_copy_capture_manager_v1`) (D4). |
| **15** | `:21` | Label every protocol or config inference by layer, phase, and version/era; do not substitute protocol status or docs for host behavior | **pass** | `entry:1,3-10,37,55,75,77,91,105,130-135` explicitly separates protocol XML (`S283`, `cd1aba6`), compositor seat-grab implementation (`S284`, Hyprland `0.56.2` `efb5099`), portal advertisement (`S286`/`S289`, xdph `v1.4.1`), client (`S285`, quickshell `9b0f339`), and 2022 rule tracker (`S287`), and `entry:130` bars inferring live grab behavior from advertisement/code. |
| **16** | `:22` | Upstream docs/releases support only dated `[INF-docs]`; never promote to host/end-to-end facts without host measurement | **pass** | `entry:73,77,107,130,132,135` keeps upstream docs/tracker/code bounded and states that no live grab or focus transition was exercised on this host. |
| **17** | `:34` | Screen repeated canonical URLs across active rows before source-fragment renumbering/merge | **pass** | `receipts/census-after-data.txt:1-10` and `quality/counters/c2-r41-focus-entry-v2.py` clause e (`c2-v2-after-data.txt:25` `e:1`): none of `S283-S289` repeats any existing registry URL. |
| **18** (superseded by **46**) | `:43-49` | Declared config `source =` targets must be regular files | **n.a.** | Applies to Hyprland `source =` config-tree parsers (`mado-verify.sh`/`mado-binds.py`), not this protocol knowledge entry. (For C2 receipts, regular-file mode `100644` is verified in criterion 55.) |
| **19** (superseded by **47**) | `:50-55` | Scope retained-data statements to actual field or record class | **pass** | `entry:61-67,131` accurately describes what `xdph-journal.txt` retains (two portal sessions, timestamps, PIDs, boot line, 78 adverts) without claiming "only headers". |
| **20** (superseded by **21**) | `:72-78` | Pre-install `pacman -Sp` comparison | **n.a.** | Superseded while host pause holds (criterion 21); no tool or package was installed (`entry:73` is a read-only file read of `/var/lib/pacman/local/.../desc`). |
| **21** | `:82-101` | Host-install pause and no-live-probe boundary | **pass** | `entry:71,73,77,79,107,130`: no pacman command, no Wayland client, no compositor socket connection (only allowed `hyprctl version` and read-only `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`). |
| **22** | `:107` | Re-derive every active axis before selecting lowest axis | **n.a.** | Round-level planning criterion (`lessons/round-41.md:17-19`), not an entry-text criterion. |
| **23** | `:111-122` | Sentence attributing a verdict token to a receipt must match the receipt's token and revision | **n.a.** | `entry:1-136` attributes no `MADO_<NAME>:` or selftest verdict token. |
| **24** | `:131-137` | Scan/selftest/measure/replay receipt cites `tool_sha256` and `measured_commit` | **n.a.** | `entry:1-136` relies on upstream code/XML/HTML fetches and a raw `journalctl` capture (`S289`), not a lane tool scan/selftest receipt. |
| **25** | `:138-143` | Instrument tightening counts as biting only with committed mutant receipt | **n.a.** | Instrument/counter criterion, not applicable to a `corpus/knowledge/` entry. |
| **26** | `:144-154` | Digest, count, or identity taken through a pipe carries producer exit status | **pass** | `entry:9,71,109`: `S289` sha256 (`bf8fa91a...600aaf7`) is the true digest of the 19,130-byte file, and `entry:71,109` explicitly record the exit status (`exits 1`) of both `grep` commands. |
| **27** | `:174-182` | Credited source row's anchor is reproducible (tag/commit-pinned bytes with sha256) | **pass** (on `S283-S289`; see D1 on `S037`) | Verified via `python3 -I .ufo/waves/round-19/anchor-durability.py 07f2641696b5ac73de1404ea737a9f27e9819aa1` → `mined=207 durable=207 flagged=0` (`S283` `cd1aba6`, `S284` `efb5099`, `S285` `9b0f339`, `S286` `v1.4.1`, `S287` captured `2026-10-25` sha256 `148a9053…`, `S288` `cd1aba6`, `S289` local receipt sha256 `bf8fa91a…`). Note: `entry:3-9` replaces the staged package's unpinned `master`/`main` URLs (`focus-grab-protocol-live-on-host-r14.md:10-13`) with commit/tag pins. |
| **28** | `:183-190` | Present-tense value supersession sweep across owned files | **pass** | Verified via `python3 -I .ufo/waves/round-19/supersede-sweep.py 07f2641696b5ac73de1404ea737a9f27e9819aa1` → `stale=0`; the entry introduces new focus-grab ground and does not supersede a held present-tense value. |
| **29** | `:232-248` | Isolation harness fails closed | **n.a.** | Applies to isolation harnesses (`isolate.sh`, `bwrap`), not a knowledge entry. |
| **30** | `:249-259` | Detector recall change requires precision evidence | **n.a.** | Applies to transcript detector changes (`mado-tripwire.py`), not a knowledge entry. |
| **31** | `:298` | Detector no-harm bounded resource evidence | **n.a.** | Applies to detector tools, not a knowledge entry. |
| **32** (superseded by **48/53**) | `:306` | Claimed binding repair separates lifetime, scope, and callable identity | **n.a.** | Applies to `mado-tripwire.py` AST binding analysis, not a knowledge entry. |
| **33** | `:318` | Detector/gate repair discovery attacks frozen before patch | **n.a.** | Applies to `tools/` detector/gate repairs, not C2 knowledge entry. |
| **34** | `:319` | Scratch measurement receipt absolute paths and tool sha256 | **n.a.** | Applies to tool measurement receipts, not the knowledge entry. |
| **35** | `:320` | Fixture discovered after patch is never credited as pre-patch guard | **n.a.** | Applies to tool fixtures, not the knowledge entry. |
| **36** | `:324` | Counter controls committed before data wave | **n.a.** | Counter-admission rule (`receipts/ctl-c2-v2.txt`), not an entry-text rule. |
| **37** | `:328` | Predicate population and counter population are one number | **n.a.** | Counter-receipt rule (`admitted=1/1`), not an entry-text rule. |
| **38** (superseded by **49**) | `:332` | Composite counter smoke-run at freeze | **n.a.** | Counter-freeze rule, not an entry-text rule. |
| **39** (superseded by **50**) | `:334` | Claim leg depending on ephemeral bytes commits them | **pass** (see 50) | All 8 receipts cited by `entry:3-10` are committed in `.ufo/waves/round-41/fetch/` at `07f2641696b5ac73de1404ea737a9f27e9819aa1`. |
| **40** (superseded by **51**) | `:336` | Held-out mutant rows authored against suite probe discriminators | **n.a.** | Mutation-testing criterion, not an entry-text rule. |
| **41** (supersedes **1**) | `:347` | Every claim falsifiable or marked opinion | **fail** (minor) | `entry:85` (`adding a window records it and *defers* the protocol call`) is falsified by `quickshell-grab.cpp:66` (`this->add_surface(window->surface());` is called immediately; only `commit` is deferred) (D2). All other claims in `entry:1-136` pass. |
| **42** (supersedes **2**) | `:348` | Every claim carries a source: a measured anchor (path:line, command, evidence id) — never oral knowledge | **fail** | `entry:10,73` cites held row `S037` (`releases/tag/v1.4.1`) for a local pacman `desc` receipt while admitting `S037`'s release page was not re-fetched (D1); `entry:67` (`**INF**`) has no `Basis:` or S-id on the line (D5). |
| **43** (supersedes **3**) | `:349` | Observation, inference, and unknown stay separate | **fail** (minor) | `entry:109` is marked `**INF**` but reports an observed command outcome (`grep -rli ... exits 1 at base` and file checks) alongside its inference, and omits `Basis:` (D5). All other `**OBS**`, `**INF**`, and `**UNK**` paragraphs and `§6` (`entry:113-126`) cleanly separate the three states. |
| **44** (supersedes **4**) | `:350` | Errata are append-only blocks | **n.a.** | First landing of `hyprland-focus-grab-r41.md` (`entry:1-136`); no errata block. |
| **45** (supersedes **5**) | `:351` | A rejection is kept, not silently dropped | **pass** | `entry:15,136` and `lessons/round-41.md:35-36,45-46` retain the refusals of `focus-control-surfaces-r28.md` §3 and `privileged-client-surface-r29.md`. |
| **46** (supersedes **18**) | `:352` | Declared config `source =` targets must be regular files | **n.a.** | Applies to Hyprland config `source =` targets, not this entry. |
| **47** (supersedes **19**) | `:353` | Scope retained-data statements to actual field or record class; keep diagnostic requests, retained evidence and behavioral conclusions separate | **pass** | `entry:61-67,75,79,130-131` separates the retained journal log (`S289`), the portal's `onGlobal` code (`S286`), and unexercised runtime grab behavior. |
| **48** (superseded by **53**) | `:354` | Binding repair lifetime/scope | **n.a.** | Superseded by 53; applies to `mado-tripwire.py`. |
| **49** (supersedes **38**) | `:355` | Composite counter smoke-run at freeze | **n.a.** | Counter-freeze rule. |
| **50** (supersedes **39**) | `:356` | Claim leg depending on ephemeral bytes commits those bytes | **pass** | `entry:3-10` and `lessons/round-41.md:25-32`: all 8 receipts (`focus-grab-v1.xml`, `Hyprland-FocusGrab.cpp`, `quickshell-grab.cpp`, `xdph-PortalManager.cpp`, `issue-565.html`, `protocols-README.md`, `xdph-journal.txt`, `xdph-installed-version.txt`) are committed at `07f2641696b5ac73de1404ea737a9f27e9819aa1`. |
| **51** (supersedes **40**) | `:357` | Held-out mutant rows authored against probe discriminators | **n.a.** | Mutation-testing rule. |
| **52** | `:358` | Sweep surfacing an inherited defect records and routes it forward | **n.a.** | No inherited defect sweep in this entry (`ScoutHeldOverlap` noted `idle-lock-route-r17.md:130`'s UNK on `hyprland-lock-notify-v1`, which is outside the focus-grab entry). |
| **53** (supersedes **48**) | `:359` | Binding repair lifetime/scope/callable identity | **n.a.** | Applies to `mado-tripwire.py`. |
| **54** | `:360` | Recheck command referencing `file#anchor` resolves against named file only | **pass** | `entry:12` (`recheck: 90d - ...`) uses no broken `file#anchor`. |
| **55** | `:361` | Counter reading tree shape checks regular file mode and binds receipt digests | **pass** | All 8 receipts in `.ufo/waves/round-41/fetch/` have git mode `100644` at `07f2641696b5ac73de1404ea737a9f27e9819aa1`, and `c2-r41-focus-entry-v2.py` clauses d/g bind their sha256 and quotes to `entry:19,43,61,69,73,83,99,103`. |
| **56** | `:362` | Live clauses of a frozen counter named in a clause ledger | **n.a.** | Counter-design criterion, not an entry-text criterion. |
| **57** | `:364` | Control attribution across competing clauses | **n.a.** | Counter-control criterion, not an entry-text criterion. |
| **58** | `:365` | Counter scoring a document parses its table and compares digests to bytes at claimed path | **pass** | `entry:23-31,63,113-126` and `c2-r41-focus-entry-v2.py` (`c2-v2-after-data.txt`: `admitted=1/1 TARGET_MET`). |
| **59** | `:366` | Mutation fixture preserves accept control's environment | **n.a.** | Counter-fixture criterion. |
| **60** | `:367` | Round report states last-30-commit domain-vs-meta ratio | **n.a.** | Round-report criterion, not an entry-text criterion. |
| **61** | `:369` | Registration commands runnable verbatim at freeze | **n.a.** | Registration criterion. |
| **62** | `:371` | Zero count in a log channel requires a positive probe from the same logger at the same level inside the same window | **pass** | `entry:71` claims `focus` occurs 0 times outside the advert line in `xdph-journal.txt` and immediately supplies the positive probes from the **same logger** (`xdg-desktop-portal-hyprland` `[LOG]` level) in the **same session window** (`pid 1952`): the advert line itself (`[LOG]  \| Got interface: hyprland_focus_grab_manager_v1 (ver 1)` at `:117`), `[LOG] [input-capture] init successful` (`:135`), and `[LOG] [globalshortcuts] registered` (`:128`). |
| **63** | `:373` | Worktree observable commits its raw witness beside the receipt | **pass** | `entry:9,73` commits the raw host witnesses `.ufo/waves/round-41/fetch/xdph-journal.txt` and `.ufo/waves/round-41/fetch/xdph-installed-version.txt` in `07f2641696b5ac73de1404ea737a9f27e9819aa1`. |
| **64** | `:375` | Counter paths exist at freeze commit | **n.a.** | Freeze-commit criterion (`receipts/freeze-counter-check-v2.txt`). |
| **65** | `:377` | Lattice fixtures and single-defect mutants for conversion/comparison tools | **n.a.** | Applies to C1 tool counters, not C2 knowledge entries. |
| **66** | `:379` | Sandbox hides judge from tool under test | **n.a.** | Applies to C1 tool counters, not C2 knowledge entries. |
| **67** | `:381` | Read-only claim about external verb allowlists every argv element | **pass** | `entry:9,77` runs only literal `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso` and `hyprctl version` with no config-derived argv elements. |
| **68** | `:383` | Reference model of a host parser names the parser it copies (`file:line`) and avoids unenumerated universals | **pass** | `entry:43-53,69` names `src/protocols/FocusGrab.cpp` methods and `src/core/PortalManager.cpp` `CPortalManager::onGlobal` lines `85-261` explicitly, and `entry:39,57,133` marks unread `CSeatGrab` internals as `UNK` rather than stating a universal. |

---

## §3 Verdict against `CORPUS.md` Rules

Checked against `/home/vgpnk/Projects/shokunin/CORPUS.md`:

| `CORPUS.md` Rule | Line | Verdict | Evidence |
|---|---|---|---|
| Provenance trio (`source:`, `verified-at:`, `recheck:`) opens the entry, citing `S###` alongside URL/anchor | `:18, 163-170` | **pass** | `entry:3-12`: 8 `source: S###` lines (lines 3–10), `verified-at: 2026-10-25` (line 11), `recheck: 90d - ...` (line 12), all within the first 20 raw lines outside fences. |
| Falsifiable or marked opinion; no unverifiable claims | `:26` | **fail** (minor) | Pass on all lines except `entry:85` (D2: `add_surface` is not deferred in `addWaylandWindow`). |
| A count carries its command (`<number> — <command> <date>`) | `:34-38` | **fail** | `entry:21,63,65,67,69,71` state counts in prose without `<n> — <command> <date>` (D4), and `SOURCES.md:232,235` has `4` requests / `9` binds vs `entry:115,69`'s `5` requests / `10` branches (D3). |
| A negative claim carries its sweep | `:39-41` | **pass** (with minor scope note) | `entry:71` (`grep -in focus` over `PortalManager.cpp` exits 1; journal `focus` count = 1) and `entry:109` (`grep -rli 'focus_grab\|focus-grab\|focus grab' corpus PROVINCE.md SKILL.md tools` exits 1 at base). |
| A quote names its location | `:42-45` | **pass** | All 31 source quotes in `entry:19-103` name their XML interface/request, C++ method/file:line, journal session/timestamp/pid, package record path, or issue section, and all 31 are verified verbatim and `<= 25` words by `.ufo/waves/round-41/w2/RevEntryBar/verify_quotes.py` (`checked=31 failed=0`). |
| An index row is a claim (`corpus/README.md`) | `:46-48` | **fail** (minor) | `corpus/README.md:70` exists at `07f2641696b5ac73de1404ea737a9f27e9819aa1`, but has only 2 cells (`NF=4`) instead of the 3-cell `\| Note \| Holds \| Sources \|` schema (`NF=5`) used by all 58 prior rows (D7). |
| No credential material, ever | `:49-52, 129` | **pass** | Swept `entry:1-136` and `fetch/xdph-journal.txt`: no secrets, tokens, cookies, or `op://` refs (the journal's `com.onepassword.OnePassword` lines at `xdph-journal.txt:17-22` are D-Bus object paths/appids only, not credentials, and are not quoted in the entry). |
| SOURCES Contract v1 Rule 1: `## Gate` records URL, access date, `<= 25`-word quote grounding `teaches` | `:112-115` | **fail** (on `S037`) | `S283-S289` pass (`lessons/round-41.md:25-31`). `S037` (`lessons/round-41.md:32`) binds a local pacman `desc` receipt instead of `S037`'s GitHub release URL/anchor (D1). |
| SOURCES Contract v1 Rule 2: Append-only; in-place `used-by` changes logged `old->new` in the round lesson | `:116-118` | **fail** | `corpus/SOURCES.md:49` edits `S037`'s `used-by` in place, and `corpus/lessons/round-41.md` does not log the `old -> new` change (D1). |
| SOURCES Contract v1 Rule 5: `## Search log` note in `corpus/SOURCES.md` | `:82, 126-128` | **fail** (minor) | `corpus/SOURCES.md` `## Search log` (`:286-449`) has no round-41 entry (D7). |
| SOURCES Contract v1 Census commands | `:133-148` | **pass** | `rows=226`, `malformed=0`, `tier: A=216 B=3 C=7`, `status: mined=207 queued=10 rejected=9`, `duplicate_ids=0`, `enum_violations=0`, `missing_used_by=0` at `07f2641696b5ac73de1404ea737a9f27e9819aa1`. |

---

## §4 Specific Targeted Questions from Assignment

1. **Is each `INF` marked with its basis?**
   - **No (5 of 8 yes, 3 of 8 missing `Basis:`).**
   - Lines `37`, `55`, `75`, `91`, and `105` carry explicit `` `Basis:` ... `` markers naming their `S###` rows and sections.
   - Lines **`67`**, **`77`**, and **`109`** are marked `**INF**` without a `` `Basis:` `` marker (and line `67` names no `S###` id on the line; line `109` mixes an `[OBS]` command run into an `**INF**` block) — **Defect D5**.

2. **Is each `UNK` a real unknown?**
   - **Yes (5 of 5 in body + 3 in `§6` table are genuine unknowns under the round's receipts and host safety rules):**
     - `entry:39`: What `"implementation-defined criteria"` and `"similar action"` cover beyond pointer/touch-outside and a competing grab — the XML (`focus-grab-v1.xml:72-76`) does not enumerate them, and `CSeatGrab` is outside `FocusGrab.cpp`.
     - `entry:57`: How `CSeatGrab` routes an event that falls outside the set — `SeatManager.cpp` is not in `.ufo/waves/round-41/fetch/`.
     - `entry:79`: Which process on this host binds `hyprland_focus_grab_manager_v1` today — the journal logs registry advertisements (`onGlobal`), not client binds, and running a Wayland client/compositor-socket probe is prohibited.
     - `entry:93`: Whether one Qt transaction is one frame in practice, and whether a `cleared` arriving between `add_surface` and `commit` is observable to quickshell — requires running quickshell / a live Wayland client, which is prohibited.
     - `entry:107`: Whether Hyprland `0.56.2` still exhibits the momentary focus steal of `#565` — `#565` is from Aug 2022 (`b09f157`), and testing it on `0.56.2` requires window opening / focus-transition probing, which is prohibited.

3. **Is any claim stronger than its quote?**
   - **Yes, two instances:**
     - `entry:85` (**D2**, Medium): quotes `"this->pendingAdditions.append(window); this->commitRequired = true;"` and claims *"adding a window records it and \*defers\* the protocol call"*, whereas `FocusGrab::addWaylandWindow` (`quickshell-grab.cpp:66`) calls `this->add_surface(window->surface());` immediately on the line above the quote and defers only `this->commit()`.
     - `entry:97` (**D6**, Low): quotes the 13-word prefix `"If a workspace windowrule contains silent then matching windows should not get focus"` from `issue-565.html:659`, dropping the trailing qualification `", unless that window's workspace is already the active one."`

4. **Is there any scope creep beyond `PROVINCE.md`?**
   - **No.**
   - Checked against `PROVINCE.md:1-95`:
     - The localized Japanese documentation channel (`focus-control-surfaces-r28.md` §3, `amgsk.dev/posts/hyprland-rules/`) is explicitly excluded (`entry:15,136`; `lessons/round-41.md:36,46`; `PROVINCE.md:67-81`).
     - No secrets, model endpoints, or model-quality claims (`PROVINCE.md:14-15`).
     - No compositor mutation, input injection, or Wayland client/socket connection (`PROVINCE.md:15-16`; `entry:79,107,130`).

5. **Is there any sibling-domain bleed (Wayland security literature)?**
   - **No.**
   - The staged package's three generic security/literature notes (`compositor-focus-manipulation-literature-r26.md` on arXiv:2604.18860 OSWorld X11 agent attacks, `wayland-input-security-literature-r8.md` on XDC 2014 / JRES 2017, and `privileged-client-surface-r29.md` on `blog.ce9e.org`) are refused/not adopted (`lessons/round-41.md:35,45,47`).
   - `entry:134` explicitly states: *"Nothing here says the protocol is a security boundary. No receipt gates it by client identity, and no malicious or racing client was tested."*

6. **Is there any duplicate of held knowledge (grep the corpus)?**
   - **No prose duplicate; one unacknowledged datum overlap (`S041`).**
   - Command run against base `ab2bfaab661c846d1de9d58c01651cd156a13949`:
     ```sh
     git -C /home/vgpnk/Projects/shokunin/mado-shokunin grep -nEi 'focus_grab|focus-grab|focus grab|FocusGrab|CSeatGrab|quickshell|issues/565' ab2bfaab661c846d1de9d58c01651cd156a13949 -- corpus/ PROVINCE.md SKILL.md tools/
     ```
     Only hit at base is `corpus/lessons/round-35.md:138` (noting that the staged package's S3xx ids name quickshell and `hyprland-protocols`). No `corpus/knowledge/` file at base discusses the focus-grab protocol, `FocusGrab.cpp`, `quickshell`, or issue `#565`.
   - However, held datum `S041` (`.ufo/waves/round-13/w1/globals.json`, cited in `corpus/knowledge/wayland-protocol-boundaries-r13.md`) already recorded `{"interface": "hyprland_focus_grab_manager_v1", "version": 1}` among its 71 distinct globals on this host (`2026-10-20`). The entry does not duplicate `wayland-protocol-boundaries-r13.md`'s prose, but should cite `S041` when comparing session 2's 63 globals against the compositor's 71-global set (see **D4**).

---

## §5 Verification & Tooling Record

- **Commands run:**
  - `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r41-focus-entry-v2.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1` → `PRED-C2-r41-v2: admitted=1/1 verdict=TARGET_MET rev=07f2641696b5ac73de1404ea737a9f27e9819aa1` (exit 0).
  - `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/anchor-durability.py 07f2641696b5ac73de1404ea737a9f27e9819aa1` → `mined=207 durable=207 per_fetch_digest=0 unpinned_alias=0 flagged=0` (exit 0).
  - `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/supersede-sweep.py 07f2641696b5ac73de1404ea737a9f27e9819aa1` → `stale=0` across all 3 ledgers (exit 0).
  - `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w2/RevEntryBar/verify_quotes.py` → `ENTRY_QUOTES_SUMMARY checked=31 failed=0` (exit 0).
- **Tooling installed/updated:** None (existing `python3`, `git`, `awk`, `grep`, `sed` were sufficient; `pacman` is paused host-wide).
