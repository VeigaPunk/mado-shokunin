# RevAssimGate — Wave 2 Falsification Report

Seat: `RevAssimGate` (wave `w2`, round 41, 2026-10-25).
Target: Assimilation gate decisions (`ADMIT` `focus-grab-protocol-live-on-host-r14.md` as `corpus/knowledge/hyprland-focus-grab-r41.md`, `REFUSE` `privileged-client-surface-r29.md`, `REFUSE` `focus-control-surfaces-r28.md` §3) in `07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/lessons/round-41.md`, and the id-guard numbers (`reg 219, staged 147, collisions 27`) in `.ufo/waves/round-41/assimilation/id-guard.md`.
Deliverables:
- `.ufo/waves/round-41/w2/RevAssimGate/spotcheck.md` (full outside discernment spot-check)
- `.ufo/waves/round-41/w2/RevAssimGate/verify-spotcheck.py` (re-runnable verification script for id-guard counts and located quotes)
- `.ufo/waves/round-41/w2/RevAssimGate.md` (this report)

---

## 1. Outside Discernment Verdicts (`LEARNING.md` §Discernment)

All three staged package files under `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/` and their underlying sources (including live re-reads of `https://blog.ce9e.org/posts/2025-10-03-wayland-security/`, `https://amgsk.dev/posts/hyprland-rules/`, `/home/vgpnk/Projects/shokuknow/lanes/mado/round14/fetch/host-focus-grab-portal-advertisement.txt`, and all 8 receipts in `.ufo/waves/round-41/fetch/`) were independently re-opened:

1. **`ADMIT merge/mado/knowledge/corpus/knowledge/focus-grab-protocol-live-on-host-r14.md as corpus/knowledge/hyprland-focus-grab-r41.md` (`corpus/lessons/round-41.md:34`) → AGREE**
   - Staged `r14` could not be admitted as-is: its `source:` ids (`S328–S332`) come from the staged package's unaligned id space, its `S328` own-work receipt (`lanes/mado/round14/fetch/host-focus-grab-portal-advertisement.txt`, claiming `QUOTE_VERIFIED[round14-adv]: "advertisement lines naming the focus-grab manager: 2"` across two 2026-10-23 boots) is private to the shokuknow checkout and no longer reproducible in the host's journal (`fetch/xdph-journal.txt` starts `2026-10-25T13:16:45-03:00` with 1 advert at line 117), its code/doc URLs (`S329–S331`) pointed to unpinned `master`/`main` branches, and its `S332` quotes were XML `summary="..."` attributes that `PRED-C2-r41-v2`'s tag-stripping `norm()` erases.
   - The admitted successor (`07f2641:corpus/knowledge/hyprland-focus-grab-r41.md`) faithfully re-grounds the theme on commit-pinned upstream receipts (`S283` `focus-grab-v1.xml` @ `cd1aba6`, `S284` `FocusGrab.cpp` @ `efb5099`, `S285` `quickshell-grab.cpp` @ `9b0f339`, `S286` `xdph-PortalManager.cpp` @ `v1.4.1`, `S288` `protocols-README.md` @ `cd1aba6`), a 2026-10-25 capture of issue #565 (`S287`), the saved host journal (`S289`), and the installed xdph package record (`S037`).
   - It imports **zero** unsupported package claims (no "2 adverts at both boots", no `r10` unordered_map seat-fallback fallacy, no `r15` unverified host binary sweep, no `r28` unscoped 2022 `silent`-rule guarantee claim, and no localized `amgsk.dev` or generic `ce9e.org` claims).
   - `python3 -I quality/counters/c2-r41-focus-entry-v2.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1` scores `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=1`, `verdict=TARGET_MET` (exit 0).

2. **`REFUSE merge/mado/knowledge/corpus/knowledge/privileged-client-surface-r29.md reason=generic Wayland analysis, one truncated quote, no measurement and no host state` (`corpus/lessons/round-41.md:35`) → AGREE**
   - Re-opening `https://blog.ce9e.org/posts/2025-10-03-wayland-security/` (3,135 B HTML) confirms the refusal reason on every point:
     - Generic Wayland analysis (`sway`, `flameshot`, `grim`, `swaylock`, `labwc` PR `#3089`) with **0** occurrences of `Hyprland` or `focus_grab`.
     - Truncated 6-word body quote in staged `r29:22`: `QUOTE_VERIFIED[staged-r29]: "But there is also `WAYLAND_SOCKET`, which"` (cut mid-clause before `"tells them to use an already connected file descriptor instead"`).
     - Zero host measurements (acknowledged by `r29:35-36` itself).
     - Unsupported inference (`QUOTE_VERIFIED[staged-r29]: "A focus-grab client is therefore a privileged client"` via compositor-spawned `WAYLAND_SOCKET` handoff), contradicted by `Hyprland-FocusGrab.cpp:149-155` and `xdph-journal.txt:117` showing `hyprland_focus_grab_manager_v1` advertised on the normal `wl_registry`.

3. **`REFUSE merge/mado/knowledge/corpus/knowledge/focus-control-surfaces-r28.md reason=section 3 rests on a localized (Japanese) documentation channel, outside PROVINCE.md` (`corpus/lessons/round-41.md:36`) → AGREE**
   - Re-opening `https://amgsk.dev/posts/hyprland-rules/` (`<html ... lang=ja-JP>`, title `Hyprlandで役に立つウィンドウルール`) confirms that §3 (`S230`, `QUOTE_VERIFIED[staged-r28]: "windowrule = match:class ^(.*jetbrains.*)$ title:^(win.*)$, no_focus on"`) is Japanese-language practitioner documentation, excluded by `PROVINCE.md:75` (`QUOTE_VERIFIED[PROVINCE.md]: "documentation written in a localized channel — is outside the province"`) and forbidden by `PRED-C2-r41-v2` clause `i` (`BAD_LOC` contains `"amgsk.dev"`).
   - Moreover, as written, `focus-control-surfaces-r28.md` has three further defects that preclude raw admission: (a) §1 quotes raw `<interface ...>` tags that strip to empty under `norm()`, (b) §2 generalizes a closed 2022 bug (`issues/565`, fixed in `b09f157` on 2022-08-25) into an unscoped claim about Hyprland's `silent` rule, and (c) §4 (`:69`) cites a ghost id `S199` (`QUOTE_VERIFIED[staged-r28]: "The round-2 paper (wave-2 row S199) measured focus hijacking on X11"`) absent from its header. Refusing `r28` as written while folding its re-grounded English §1–§2 (`S283`, `S287`) into `hyprland-focus-grab-r41.md` is sound.

---

## 2. Check of `id-guard.md` Numbers (`reg 219, staged 147, collisions 27`)

- **Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/assimilation/id-guard.md` (`QUOTE_VERIFIED[id-guard.md]: "Result: **reg=219 staged=147 coll=27**"`).
- **Command run:** `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w2/RevAssimGate/verify-spotcheck.py` (which executes the exact `^ {0,3}\|[[:space:]]*S[0-9]{3,}` extraction and set intersection against both `ab2bfaa:corpus/SOURCES.md` and `07f2641:corpus/SOURCES.md`).
- **Result at base (`ab2bfaa`):**
  - `reg = 219` (`S001..S282`, sha256 of `reg-ids` = `744a99450f29cd8f9db0bcf35dc26f832dbdc357ca141f3ef57be95e903e4424`)
  - `staged = 147` (`S203..S349`, sha256 of `staged-ids` = `079d7538022b0acf8bfadcd150b9db16a54bb550f190361454d4649054f0925d`)
  - `collisions = 27` (`S203..S221`, `S253`, `S258`, `S277..S282`, sha256 of `collisions` = `aad91fd08891238d70923bff6da469fb558207fa752d41e8e9247576688e020a`)
  - **No defect in the base id-guard numbers or hashes.**
- **Result at data commit (`07f2641`):**
  - After appending `S283..S289`, running the procedure against `07f2641:corpus/SOURCES.md` yields `reg = 226`, `staged = 147`, `collisions = 34` (the 27 base collisions plus `S283..S289`, which overlap the staged `S203..S349` range as noted in `id-guard.md:307-310`).

---

## 3. Concrete Findings on the Committed Data (`07f2641696b5ac73de1404ea737a9f27e9819aa1`)

 ranked by severity (all are data/prose inconsistencies fixable by the L1 before closure; none invalidates `PRED-C2-r41-v2` admission):

### Finding 1 (Low / Data prose contradiction) — `corpus/lessons/round-41.md:38` vs `:44, :51-53` contradicts itself on whether `S290` is a landed row
- **Attacks:** `07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/lessons/round-41.md:38,44,51-53`
- **Evidence:**
  - `round-41.md:38` correctly states: `QUOTE_VERIFIED[lesson]: "S290 (`input-capture-v1.xml`) is **not** cited by the entry and has no row."` (`07f2641:corpus/SOURCES.md` ends at `S289` on line 238).
  - Yet `round-41.md:44` (Assimilation ledger) states: `QUOTE_VERIFIED[lesson]: "re-grounded this round as C2 with lane ids S283–S290"`, and `round-41.md:51-53` states: `"the new rows S283-S289 continue in the order ScrRowsDraft drafted them: ... the own-work journal S289, input-capture-v1.xml S290."` (`QUOTE_VERIFIED[lesson]: "the own-work journal S289, `input-capture-v1.xml` S290."`).
- **Recommendation for L1:** Update `round-41.md:44` to `S283–S289` and clarify at `:53` that `S290` was drafted in w1 but omitted from `corpus/SOURCES.md` because the entry does not cite it.

### Finding 2 (Low / Cross-file count mismatch) — Request count for `S283` (`four requests` in `SOURCES.md:232` vs `five requests` in entry `:113` and `README.md:70` vs `6` `<request>` elements in `focus-grab-v1.xml`)
- **Attacks:** `07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/SOURCES.md:232` vs `corpus/knowledge/hyprland-focus-grab-r41.md:113` and `corpus/README.md:70`
- **Evidence:**
  - `.ufo/waves/round-41/fetch/focus-grab-v1.xml` contains 6 `<request>` tags (`create_grab` at `:44`, `destroy` at `:52` on the manager; `add_surface` at `:79`, `remove_surface` at `:91`, `commit` at `:105`, `destroy` at `:115` on the grab), with 5 distinct request names.
  - `SOURCES.md:232` (`S283` scope cell) reads: `QUOTE_VERIFIED[SOURCES.md]: "The two interfaces, four requests and one event that define a focus grab"` (counting only the 4 grab-interface requests).
  - `hyprland-focus-grab-r41.md:113` (§6 table) reads: `QUOTE_VERIFIED[entry]: "What can a client ask for? | S283: two interfaces, five requests, one event (§1)"` (and `corpus/README.md:70` also says `"two interfaces, five requests, one cleared event"`).
- **Recommendation for L1:** Harmonize `SOURCES.md:232`, `hyprland-focus-grab-r41.md:113`, and `corpus/README.md:70` (e.g., `"two interfaces, six requests (five distinct names) and one event"`).

### Finding 3 (Low / Cross-file count mismatch) — Portal bind count for `S286` (`nine` in `SOURCES.md:235` vs `ten` in `hyprland-focus-grab-r41.md:6,69`)
- **Attacks:** `07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/SOURCES.md:235` vs `corpus/knowledge/hyprland-focus-grab-r41.md:6,69`
- **Evidence:**
  - In `.ufo/waves/round-41/fetch/xdph-PortalManager.cpp:90-260`, `CPortalManager::onGlobal` has 10 `INTERFACE == ...` branches: 9 call `wl_registry_bind` directly in `onGlobal` (`:92, :97, :101, :104, :110, :116, :129, :247, :259`) and 1 (`zwlr_foreign_toplevel_manager_v1_interface.name`, `:249-255`) delegates to `std::make_unique<CToplevelManager>(name, version)`.
  - `hyprland-focus-grab-r41.md:6` says `"binds ten of them"` and `:69` says `QUOTE_VERIFIED[entry]: "and what follows is a fixed set of ten named branches"`.
  - `SOURCES.md:235` (`S286` scope and teaches cells) says `"which nine it binds"` and `QUOTE_VERIFIED[SOURCES.md]: "and the portal binds nine named interfaces none of which is the focus-grab manager"`.
- **Recommendation for L1:** Harmonize `SOURCES.md:235` with the entry by stating `"ten named interfaces (nine bound directly in onGlobal plus foreign_toplevel via CToplevelManager)"`.

### Finding 4 (Low / Documentation pointer mismatch) — `round-41.md:49` cites `assimilation/id-guard.md` for the id map, but `id-guard.md` §7 maps `S283–S289` to different documents than `SOURCES.md`
- **Attacks:** `.ufo/waves/round-41/assimilation/id-guard.md:259-282` vs `07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/lessons/round-41.md:49-53`
- **Evidence:**
  - `id-guard.md:259-268` maps `S283`→`issues/565`, `S284`→`focus-grab-v1.xml`, `S285`→`amgsk.dev`, `S286`→`FocusGrab.cpp`, `S287`→`round8/fetch/...`, `S288`→`arxiv.org/abs/2604.18860`, `S289`→`quickshell.org/docs/...`.
  - `corpus/SOURCES.md:232-238` and `round-41.md:51-53` use `ScrRowsDraft`'s map (`S283`→`focus-grab-v1.xml`, `S284`→`FocusGrab.cpp`, `S285`→`quickshell-grab.cpp`, `S286`→`xdph-PortalManager.cpp`, `S287`→`issues/565`, `S288`→`protocols-README.md`, `S289`→`xdph-journal.txt`).
- **Recommendation for L1:** Distinguish `id-guard.md` §7's 22-document theme survey map from `ScrRowsDraft`'s landed `S283–S289` assignment in `round-41.md:49-53`.

---

## 4. Verification & Hygiene

- **Verification script run:** `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w2/RevAssimGate/verify-spotcheck.py` → `ID-GUARD BASE: reg=219 staged=147 collisions=27 -> OK`, `SUMMARY: checked=27 failures=0`, all `DOC QUOTE` checks pass (exit 0).
- **Write scope:** Wrote only `.ufo/waves/round-41/w2/RevAssimGate.md`, `.ufo/waves/round-41/w2/RevAssimGate/spotcheck.md`, and `.ufo/waves/round-41/w2/RevAssimGate/verify-spotcheck.py`. Zero tracked files edited; zero mutating git/jj commands run; `/tmp` scratch cleaned up.
- **Tooling:** None installed (system `python3`, `git`, coreutils).

Report: .ufo/waves/round-41/w2/RevAssimGate.md
