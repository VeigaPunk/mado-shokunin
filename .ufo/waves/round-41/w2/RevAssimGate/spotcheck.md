# RevAssimGate — Outside Discernment Spot-Check (Round 41, Wave 2)

Seat: `RevAssimGate` (non-author reviewer, wave `w2`).
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Data commit under review: `07f2641696b5ac73de1404ea737a9f27e9819aa1` (base `ab2bfaab661c846d1de9d58c01651cd156a13949`).
Staged package (read-only): `/home/vgpnk/Projects/shokuknow/merge/mado`.

---

## 1. Summary of Discernment Verdicts (`LEARNING.md` §Discernment)

Gate lines in `07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/lessons/round-41.md:34-36`:
- `QUOTE_VERIFIED[lesson]: "ADMIT merge/mado/knowledge/corpus/knowledge/focus-grab-protocol-live-on-host-r14.md as corpus/knowledge/hyprland-focus-grab-r41.md"` (`corpus/lessons/round-41.md:34`)
- `QUOTE_VERIFIED[lesson]: "REFUSE merge/mado/knowledge/corpus/knowledge/privileged-client-surface-r29.md reason=generic Wayland analysis, one truncated quote, no measurement and no host state"` (`corpus/lessons/round-41.md:35`)
- `QUOTE_VERIFIED[lesson]: "REFUSE merge/mado/knowledge/corpus/knowledge/focus-control-surfaces-r28.md reason=section 3 rests on a localized (Japanese) documentation channel, outside PROVINCE.md"` (`corpus/lessons/round-41.md:36`)

| # | Gate Line (`corpus/lessons/round-41.md`) | Staged Candidate | Successor / Target | Outside Verdict | Summary Reason |
|---|---|---|---|---|---|
| 1 | `ADMIT` `:34` | `focus-grab-protocol-live-on-host-r14.md` | `corpus/knowledge/hyprland-focus-grab-r41.md` | **AGREE** (with 4 concrete data defects recorded below) | The staged file's private round-14 receipt (`S328`, 2 adverts on 2026-10-23) is unreproducible and its id space (`S328–S332`) collides with the staged set; the successor faithfully re-grounds the protocol, compositor `FocusGrab.cpp`, client `grab.cpp`, portal `PortalManager.cpp`, README, issue #565, and saved host journal (`S283–S289` + `S037`) without importing unsupported package claims. |
| 2 | `REFUSE` `:35` | `privileged-client-surface-r29.md` | — | **AGREE** | Re-opening `https://blog.ce9e.org/posts/2025-10-03-wayland-security/` (3,135 B HTML) confirms every part of the refusal reason: generic Wayland analysis (`sway`/`labwc`/`grim`), zero mentions of `Hyprland` or `focus_grab`, a truncated 6-word quote (`"But there is also WAYLAND_SOCKET, which"`), no host measurement, and an unsupported inference (`"A focus-grab client is therefore a privileged client"`). |
| 3 | `REFUSE` `:36` | `focus-control-surfaces-r28.md` | — (its §1–§2 English ground folded into `hyprland-focus-grab-r41.md`) | **AGREE** | Re-opening `https://amgsk.dev/posts/hyprland-rules/` (`lang=ja-JP`) confirms §3 (`S230`) is a Japanese-language practitioner blog post, excluded by `PROVINCE.md:75` and `PRED-C2-r41-v2` clause `i` (`BAD_LOC`). Furthermore, the staged file as written makes an overbroad §2 claim from a closed 2022 issue (`S227`) and cites a stale ghost id `S199` in §4 (`:69`). Refusing the file as written while folding re-grounded §1–§2 into the successor is sound. |

---

## 2. Candidate-by-Candidate Independent Review

### 2.1 ADMIT: `merge/mado/knowledge/corpus/knowledge/focus-grab-protocol-live-on-host-r14.md` → `corpus/knowledge/hyprland-focus-grab-r41.md`

- **Verdict:** **AGREE**
- **Staged file inspected:** `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/focus-grab-protocol-live-on-host-r14.md` (117 lines, sha256 `8f42ebb1e4abe5ebb88502e47727481bc680fc3b43726c2f0c324fa26067664f`).
- **Staged citations re-opened:**
  1. `S328` (`/home/vgpnk/Projects/shokuknow/lanes/mado/round14/fetch/host-focus-grab-portal-advertisement.txt`, 1,073 B): private campaign receipt from 2026-10-24 claiming `QUOTE_VERIFIED[round14-adv]: "advertisement lines naming the focus-grab manager: 2"` across two 2026-10-23 boots (`pid 1959` and `pid 1918`). Not in the lane repo and not reproducible against the current journal capture (`.ufo/waves/round-41/fetch/xdph-journal.txt`, which starts `2026-10-25T13:16:45-03:00` and has 1 focus-grab advert at line 117).
  2. `S329` (`xdph-PortalManager.cpp`, 24,182 B, sha256 `15c3e39cea5af1a92924ebc1ffe0f7825c86ac3c0b49e894aede86b2e091ea55`): staged row pointed to unpinned `master`; lane row `S286` pins tag `v1.4.1` matching the installed package `1.4.1-2` (`S037`).
  3. `S330` (`quickshell-grab.cpp`, 2,568 B, sha256 `6f7cecf15a4dbfd0dc39341c8794639595a83dd2a4ab13b6b377ac970a301a40`): staged row pointed to unpinned `master`; lane row `S285` pins commit `9b0f339b19057f4731bf3b48293307d7ef241671`.
  4. `S331` (`protocols-README.md`, 1,903 B, sha256 `3c7007636e13889860491d0c57f93c29d92122d17838ca1f6559e4aeb7aa6323`): staged row pointed to `main`; lane row `S288` pins commit `cd1aba6bd78775825eb230b3a4274c48b6705eb7`.
  5. `S332` (`input-capture-v1.xml`, 6,765 B, sha256 `fff89f6f9de622fefa1a62a6e6970f76683b6328454565583046abebcfe2c360`): staged `r14:88-92` quoted XML `summary="..."` attributes (`"Bridge input capture to the compositor"`, `"add one barrier"`, `"release input capturing"`), which are stripped by `PRED-C2-r41-v2`'s HTML/XML tag stripper `norm()`. The successor entry drops `S332`/`S290` as a standalone row and instead grounds the portal's `input_capture` bind directly in `S286` (`PortalManager.cpp:99`: `if (INTERFACE == hyprland_input_capture_manager_v1_interface.name)`) and the journal (`S289` line 135: `[input-capture] init successful`).
- **Did the admitted successor import unsupported package claims?** **No.**
  - Checked against all problematic claims in the staged focus series (`r8`–`r15`, `r26`, `r28`, `r29`):
    - Staged `r14`'s `"at both of this host's boots"` / `"advertisement lines naming the focus-grab manager: 2"` (`QUOTE_VERIFIED[staged-r14]: "advertisement lines naming the focus-grab manager: 2"`, `r14:22,26`): **not imported**. Replaced by the exact census of `fetch/xdph-journal.txt`: `journal sessions=2 adverts=78 interfaces=63 focus_grab=1` (`hyprland-focus-grab-r41.md:63`), with §3 explicitly explaining that session 1 (`pid 1918`, 15 adverts) is a mid-session slice rather than a full boot advertisement.
    - Staged `r9`'s unsupported inference that focus grab is `"keyboard-retention, not pointer confinement"`: **not imported**; §2 (`:43`) cites `S284` (`FocusGrab.cpp:20-21`) showing both `m_keyboard = true` and `m_pointer = true`.
    - Staged `r10`'s self-refuted inference that `m_surfaces` (`std::unordered_map`) makes fallback focus selection unpredictable at the seat level: **not imported**.
    - Staged `r15`'s private sweep (`S338`, claiming no client binary on the host contains the string): **not imported**; §3 `:79` and §6 `:121` honestly mark `"Who binds it on this host?"` as `UNK`.
    - Staged `r28` §2's unscoped claim that `"silent is not a focus guarantee on Hyprland"`: **not imported**; §5 (`:97-109`) and §7 (`:130`) scope issue #565 (`S287`) to a closed 2022 report (`"fixed in b09f157"`) and mark 0.56.2 runtime behavior `UNK`.
    - Staged `r28` §3's Japanese blog (`amgsk.dev`) and `r29`'s `ce9e.org` blog: **not imported**.
- **All 8 Gate quotes in `07f2641:corpus/lessons/round-41.md:25-32` verified against committed `fetch/` receipts:**
  - `S283`: `QUOTE_VERIFIED[focus-grab-v1.xml]: "This interface restricts input focus to a specified whitelist of surfaces"` (`focus-grab-v1.xml:62-63`)
  - `S284`: `QUOTE_VERIFIED[Hyprland-FocusGrab.cpp]: "m_grab->m_keyboard = true;"` (`Hyprland-FocusGrab.cpp:20`)
  - `S285`: `QUOTE_VERIFIED[quickshell-grab.cpp]: "the protocol will always send cleared() when the grab is deactivated,"` (`quickshell-grab.cpp:78`)
  - `S286`: `QUOTE_VERIFIED[xdph-PortalManager.cpp]: "Got interface: {} (ver {})"` (`xdph-PortalManager.cpp:88`)
  - `S287`: `QUOTE_VERIFIED[issue-565.html]: "Tried to set workspace silent rule to a nofocus window!"` (`issue-565.html:706`)
  - `S288`: `QUOTE_VERIFIED[protocols-README.md]: "for grabbing input focus, primarily for complex context menus"` (`protocols-README.md:17`)
  - `S289`: `QUOTE_VERIFIED[xdph-journal.txt]: "Got interface: hyprland_focus_grab_manager_v1 (ver 1)"` (`xdph-journal.txt:117`)
  - `S037`: `QUOTE_VERIFIED[xdph-installed-version.txt]: "%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2"` (`xdph-installed-version.txt:12-16`)

---

### 2.2 REFUSE #1: `merge/mado/knowledge/corpus/knowledge/privileged-client-surface-r29.md`

- **Verdict:** **AGREE**
- **Refusal line (`corpus/lessons/round-41.md:35`):**
  `REFUSE merge/mado/knowledge/corpus/knowledge/privileged-client-surface-r29.md reason=generic Wayland analysis, one truncated quote, no measurement and no host state`
- **Staged file inspected:** `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/privileged-client-surface-r29.md` (37 lines, sha256 `36a41712189d32ba2977aa626a57a495c24f839c70f6132c9028bd9236350354`), citing `S244` (`https://blog.ce9e.org/posts/2025-10-03-wayland-security/`).
- **Cited source re-opened (`https://blog.ce9e.org/posts/2025-10-03-wayland-security/`):**
  - Fetched live (HTTP 200, 3,135 B HTML) and compared against `/home/vgpnk/Projects/shokuknow/lanes/mado/round4/SOURCES-PROPOSED.md:32,106-110`.
  - **Check 1 — "generic Wayland analysis": TRUE.** The post discusses generic Wayland security concepts (`wl_client_get_credentials()`, `security-context-v1`, `WAYLAND_SOCKET`) using examples from `sway`, `flameshot`, `Gimp`, `grim`, `swayidle`/`swaylock`, and a personal PR to `labwc` (`#3089`). It contains **zero** occurrences of `Hyprland`, `hyprland`, `focus_grab`, or `focus-grab`.
  - **Check 2 — "one truncated quote": TRUE.** Staged `r29` has only two blockquotes: the HTML `<meta name="description">` front-matter (`:17`) and `QUOTE_VERIFIED[staged-r29]: "But there is also `WAYLAND_SOCKET`, which"` (`:22`), which cuts off mid-clause right after `"which"` (the source sentence continues: `"tells them to use an already connected file descriptor instead."`).
  - **Check 3 — "no measurement and no host state": TRUE.** Staged `r29:35-36` itself admits under `### §2 What this entry does not license`: `"Nothing here was measured on this host: the post is an analysis, not a measurement, and no privileged client was run."`
  - **Check 4 — Unsupported inference in staged `r29:28-30`:** Staged `r29` infers `QUOTE_VERIFIED[staged-r29]: "A focus-grab client is therefore a privileged client"` granted via `WAYLAND_SOCKET` descriptor handoff to compositor-spawned clients. Both the blog post and Hyprland's own code (`Hyprland-FocusGrab.cpp:149-155`, `CFocusGrabProtocol::bindManager`) + the portal journal (`xdph-journal.txt:117`) refute this: Hyprland advertises `hyprland_focus_grab_manager_v1` in the global `wl_registry` to normal Wayland clients without a `WAYLAND_SOCKET` spawn gate.

---

### 2.3 REFUSE #2: `merge/mado/knowledge/corpus/knowledge/focus-control-surfaces-r28.md`

- **Verdict:** **AGREE**
- **Refusal line (`corpus/lessons/round-41.md:36`):**
  `REFUSE merge/mado/knowledge/corpus/knowledge/focus-control-surfaces-r28.md reason=section 3 rests on a localized (Japanese) documentation channel, outside PROVINCE.md`
- **Staged file inspected:** `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/focus-control-surfaces-r28.md` (79 lines, sha256 `14fe9341c73be200421b6067faab4b120e3df45109fb6be347c0796d3540a527`), citing `S227` (issue #565), `S229` (`hyprland-focus-grab-v1.xml`), and `S230` (`https://amgsk.dev/posts/hyprland-rules/`).
- **Cited sources re-opened:**
  1. `S230` (`https://amgsk.dev/posts/hyprland-rules/`): re-opened live (HTTP 200, `<html ... lang=ja-JP>`, `<meta property="og:locale" content="ja_JP">`, title `Hyprlandで役に立つウィンドウルール`). Section `JetBrains IDE のフォーカス問題を修正` contains the exact lines quoted in staged `r28:57-59` (`QUOTE_VERIFIED[staged-r28]: "windowrule = match:class ^(.*jetbrains.*)$ title:^(win.*)$, no_focus on"`).
  2. **Check 1 — Refusal reason is true:** `PROVINCE.md:73-75` states: `QUOTE_VERIFIED[PROVINCE.md]: "documentation written in a localized channel — is outside the province"`. `PRED-C2-r41-v2` clause `i` (`quality/counters/c2-r41-focus-entry-v2.py:121-122,462-468`) explicitly rejects any cited row containing `"amgsk.dev"`. Furthermore, the English-channel rule semantics for `no_focus` and `no_initial_focus` are already held by the lane in `corpus/knowledge/keybind-rule-semantics.md:189,210,225,229-232`.
  3. **Check 2 — Additional defects in `focus-control-surfaces-r28.md` as written:**
     - In §1 (`:20-22`), the quotes `<interface name="hyprland_focus_grab_manager_v1" version="1">` are raw XML tags that vanish under `PRED-C2-r41-v2`'s `norm()`.
     - In §2 (`:48-50`), it infers `"silent is not a focus guarantee on Hyprland"` as a present-tense property from `S227` (`issues/565`), omitting that issue #565 was closed as completed on 2022-08-25 (`"fixed in b09f157"`).
     - In §4 (`:69`), it cites `QUOTE_VERIFIED[staged-r28]: "The round-2 paper (wave-2 row S199) measured focus hijacking on X11"` — an un-declared ghost citation (`S199` is not in its `source:` header and in `absent-defect-register.md` `S199` is a CSDN blog post, while the arXiv paper is `S218`/`S280`/`S325`).
  4. **Check 3 — Soundness of partial fold-in:** Refusing `focus-control-surfaces-r28.md` as a file while re-sourcing its valid English-channel ground (`S229` protocol XML → `S283`, `S227` issue #565 → `S287` with honest 2022 closure scoping) into `corpus/knowledge/hyprland-focus-grab-r41.md` is the right curation move.

---

## 3. Verification of `id-guard.md` Numbers (`reg 219, staged 147, collisions 27`)

Target: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/assimilation/id-guard.md` (`QUOTE_VERIFIED[id-guard.md]: "Result: **reg=219 staged=147 coll=27**"`).

### 3.1 Procedure Re-run at Base (`ab2bfaab661c846d1de9d58c01651cd156a13949`)

Command run (`verify-spotcheck.py` and bash):
```bash
S=/home/vgpnk/Projects/shokuknow
L=/home/vgpnk/Projects/shokunin/mado-shokunin
git -C "$L" show ab2bfaab661c846d1de9d58c01651cd156a13949:corpus/SOURCES.md \
  | grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]+' | sort > reg-ids.base
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/mado/SOURCES.append.md" \
  | grep -oE 'S[0-9]+' | sort > staged-ids
comm -12 reg-ids.base staged-ids > collisions.base
```

Measured outputs at base `ab2bfaa`:
- **`reg` = 219** (`S001..S282`, non-contiguous; input `ab2bfaa:corpus/SOURCES.md` sha256 `51a65515231b0a180f88c4fa1bc71482afa5f3eaeede4bdfbe6c4869493812ce`; output `reg-ids` sha256 `744a99450f29cd8f9db0bcf35dc26f832dbdc357ca141f3ef57be95e903e4424`, 0 duplicates).
- **`staged` = 147** (`S203..S349`, contiguous; input `merge/mado/SOURCES.append.md` sha256 `684efe8c23b8b64d789187dab61bfbf7c0dcef4f0428e447c94d7be4e73a27c0`; output `staged-ids` sha256 `079d7538022b0acf8bfadcd150b9db16a54bb550f190361454d4649054f0925d`, 0 duplicates).
- **`collisions` = 27** (`S203..S221`, `S253`, `S258`, `S277..S282`; output `collisions` sha256 `aad91fd08891238d70923bff6da469fb558207fa752d41e8e9247576688e020a`).
- **Verdict on `id-guard.md` §1–§5:** Exact byte-for-byte match at base `ab2bfaa`.

### 3.2 Procedure Re-run at Data Commit (`07f2641696b5ac73de1404ea737a9f27e9819aa1`)

Running the exact same command in `id-guard.md:18-22` against the post-data `corpus/SOURCES.md` (`07f2641`):
- **`reg` = 226** (`219 + 7` new rows `S283..S289`).
- **`staged` = 147** (`S203..S349`).
- **`collisions` = 34** (`27 + 7`, because `S283..S289` fall inside the staged range `S203..S349`).
- Note: `id-guard.md:307-310` anticipated this (`"The new-id range overlaps the staged range (S283–S304 ⊂ S203–S349)"`), and the committed files `.ufo/waves/round-41/assimilation/{reg-ids,staged-ids,collisions}` record the pre-append (`ab2bfaa`) state.

---

## 4. Defects Found in the Data Commit (`07f2641696b5ac73de1404ea737a9f27e9819aa1`)

While the three gate decisions (`ADMIT` r14, `REFUSE` r29, `REFUSE` r28 §3) are sound (**AGREE** on all 3), our attack on the assimilation artifacts and re-opened sources uncovered **four concrete text/internal-consistency defects** in the committed data files that the L1 can repair before closure:

1. **[D-ASSIM-1] Internal contradiction in `corpus/lessons/round-41.md` on whether `S290` exists as a registry row (`round-41.md:38` vs `:44, :51-53`):**
   - Attacking: `07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/lessons/round-41.md:38,44,51-53`.
   - Evidence: Line 38 states `QUOTE_VERIFIED[lesson]: "S290 (`input-capture-v1.xml`) is **not** cited by the entry and has no row."` (which is true: `07f2641:corpus/SOURCES.md` ends at `S289`, line 238). However, six lines later in the Assimilation ledger (`:44`), the lesson says `QUOTE_VERIFIED[lesson]: "re-grounded this round as C2 with lane ids S283–S290"`, and in `:51-53` says `"the new rows S283-S289 continue in the order ScrRowsDraft drafted them: ... the own-work journal S289, input-capture-v1.xml S290."` (`QUOTE_VERIFIED[lesson]: "the own-work journal S289, `input-capture-v1.xml` S290."`).
   - Fix for L1: Change `S283–S290` at `round-41.md:44` (and `:173` if filled with final count) to `S283–S289`, and clarify at `:53` that `S290` was drafted for `input-capture-v1.xml` but dropped because the entry does not cite it.

2. **[D-ASSIM-2] Request-count disagreement (`four requests` vs `five requests` vs `six requests`) between `corpus/SOURCES.md:232` and `corpus/knowledge/hyprland-focus-grab-r41.md:113` (and `corpus/README.md:70`):**
   - Attacking: `07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/SOURCES.md:232`, `corpus/knowledge/hyprland-focus-grab-r41.md:113`, `corpus/README.md:70` against `.ufo/waves/round-41/fetch/focus-grab-v1.xml:44-119`.
   - Evidence: `focus-grab-v1.xml` defines **6** `<request>` elements across the two interfaces (`create_grab`, `destroy` on the manager; `add_surface`, `remove_surface`, `commit`, `destroy` on the grab) with **5** distinct request names. Yet `SOURCES.md:232` (`S283` scope cell) says `QUOTE_VERIFIED[SOURCES.md]: "The two interfaces, four requests and one event that define a focus grab"` (counting only the 4 requests on `hyprland_focus_grab_v1`), while `hyprland-focus-grab-r41.md:113` (`§6` table) says `QUOTE_VERIFIED[entry]: "What can a client ask for? | S283: two interfaces, five requests, one event (§1)"` and `corpus/README.md:70` says `"two interfaces, five requests, one cleared event"`.
   - Fix for L1: Align `SOURCES.md:232` and the entry/README on the exact request count (`six requests across two interfaces (two on the manager, four on the grab; five distinct request names)`).

3. **[D-ASSIM-3] Portal bind-branch count disagreement (`nine` vs `ten`) between `corpus/SOURCES.md:235` and `corpus/knowledge/hyprland-focus-grab-r41.md:6,69`:**
   - Attacking: `07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/SOURCES.md:235` vs `corpus/knowledge/hyprland-focus-grab-r41.md:6,69` against `.ufo/waves/round-41/fetch/xdph-PortalManager.cpp:90-260`.
   - Evidence: In `xdph-PortalManager.cpp:90-260`, `CPortalManager::onGlobal` has **10** `INTERFACE == ...` branches, **9** of which call `wl_registry_bind` directly in `onGlobal` and the 10th (`zwlr_foreign_toplevel_manager_v1_interface.name`, `:249-255`) constructs `CToplevelManager(name, version)` and calls `activate()`. The entry (`:6, :69`) says `"binds ten of them"` / `QUOTE_VERIFIED[entry]: "and what follows is a fixed set of ten named branches"`, whereas `SOURCES.md:235` (`S286` scope and teaches cells) says `"which nine it binds"` and `QUOTE_VERIFIED[SOURCES.md]: "and the portal binds nine named interfaces none of which is the focus-grab manager"`.
   - Fix for L1: Align `SOURCES.md:235` (`S286`) with `hyprland-focus-grab-r41.md:6,69` (e.g. `"ten interface branches (nine direct wl_registry_bind calls plus CToplevelManager)"`).

4. **[D-ASSIM-4] Two different per-document renumber maps named in the wave (`assimilation/id-guard.md` §7 vs `corpus/SOURCES.md` / `corpus/lessons/round-41.md:49-53`):**
   - Attacking: `.ufo/waves/round-41/assimilation/id-guard.md:259-282` vs `07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/lessons/round-41.md:49-53`.
   - Evidence: `round-41.md:49-53` cites `assimilation/id-guard.md` (`seat ExecAssimIdGuard`) and then gives `ScrRowsDraft`'s numbering (`S283`=`focus-grab-v1.xml`, `S284`=`FocusGrab.cpp`, `S285`=`quickshell-grab.cpp`, `S286`=`xdph-PortalManager.cpp`, `S287`=`issues/565`, `S288`=`protocols-README.md`, `S289`=`xdph-journal.txt`). In `assimilation/id-guard.md:259-282` (§7), `S283`–`S289` are mapped to *different* documents (`S283`=`issues/565`, `S284`=`focus-grab-v1.xml`, `S285`=`amgsk.dev`, `S286`=`FocusGrab.cpp`, `S287`=`round8/fetch/...`, `S288`=`arxiv.org/abs/2604.18860`, `S289`=`quickshell.org/docs/...`). If `.ufo/waves/round-41/assimilation/` is committed at closure (per M41-3), a reader following `round-41.md:49`'s pointer to `assimilation/id-guard.md` encounters a conflicting `S283–S289` table.
   - Fix for L1: Note in `round-41.md:49-53` (or `id-guard.md` §7) that `id-guard.md` §7 was an initial 22-document theme enumeration, whereas `corpus/SOURCES.md` landed `ScrRowsDraft`'s 7-row assignment (`S283–S289`).
