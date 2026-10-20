# PlanningWalk — Bounded Planning Data Walk & Connector Synthesis (Round 15 / W1)

**Seat:** `MadoR15.PlanningWalk` (UFO-FSD connector, leaf member; no subagent dispatch, no background jobs, no commits/push)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Milestone:** U6 input evidence ladder and R14 ancillary provenance correction  
**Axes Judged On:** `coverage` (lowest active finite rubric 5/7 → 6/7)  
**Date:** 2026-10-20  
**Verification Mode:** Read-only observation of repository files and peer wave artifacts. No gate, test, build, lint, or runtime execution.

---

## 1. Naming the Axes & Lowest Active Axis Confirmation

In accordance with Godspeed principles (§1: *Name the axes*) and the canonical `AXES.md` contract:

### 1.1 Current Six-Axis Status at Baseline Revision `ea0446fcb4840089f0e541d96350144506fb5d1d`

From `/home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md` (lines 512–588, 598–621) and current HEAD:

| Axis / Sub-axis | Score (0–10) | Denominator & Status | Evidence Pointer |
|---|---|---|---|
| **coverage / sourced current-art ground** | **7.1429** | **5/7 covered U-items (U1–U5)**; uniquely lowest non-retired scored axis | `SCORECARD.md:513, 601`, `corpus/knowledge/output-colour-boundaries-r14.md` |
| coverage / admitted-note reachability | 10.0000 | 28/28 uniquely indexed knowledge notes (0 missing, 0 dangling, 0 duplicates) | `SCORECARD.md:527`, `corpus/README.md:1-55` |
| operability / hermetic selftest pass fraction | 10.0000 | 372/372 assertions passed (`tools/mado-verify.sh --selftest`) | `SCORECARD.md:535`, `round-14/evidence/gate-selftest.txt` |
| operability / named-set & non-regular census | 10.0000 | 4/4 exact set cases + 3/3 non-regular source detections | `SCORECARD.md:514`, `round-14/evidence/regular-target-mutants.txt` |
| freshness / file-plane gate agreement | 10.0000 | 29/29 verdict rows PASS on `--no-live` (0 FAIL, 0 UNKNOWN, 8 SKIP, 4 NOTE) | `SCORECARD.md:529`, `round-14/evidence/gate-file-plane.txt` |
| calibration / lesson-grounded admission criteria | 7.0588 | 12/17 criteria citing mined lessons (`corpus/QUALITY.md`) | `corpus/QUALITY.md:6-38`; R14-V1 correction is unscored |
| depth | unscored | No bounded rubric established; maintained as technical depth in notes | `SCORECARD.md:573` |
| adjacency | unscored | Maintained report-not-absorb duty across sibling provinces | `PROVINCE.md:14-18`, `SCORECARD.md:573` |

### 1.2 Lowest Scored Non-Retired Axis Confirmation
* **Coverage / sourced current-art ground is confirmed as the lowest active non-retired scored rubric at 5/7 = 7.1429/10.**
* Round 15 MUST claim exactly one improvement on this axis: **Claim C1: U1–U5 (5/7 = 7.1429/10) → U1–U6 (6/7 = 8.5714/10)**, targeting the bounded kernel-input → Wayland debugging ladder without raw input capture, keystroke recording, uinput replay, or kernel diagnosis.
* U7 (Waybar module text) is explicitly retained as the remaining uncovered gap ($1/7$).

---

## 2. Independent Causal Separability (C1 vs R14-V1 Correction)

The assignment requires: *"exactly one claim C1 coverage... R14-V1 ancillary mutation receipt precision is unscored lesson-backed correction... do not choose extra claims."*

### 2.1 Causal Separability Demonstration
1. **Claim C1 (Coverage):** Admitting substantive U6 knowledge note `corpus/knowledge/input-layer-debugging-r15.md` grounded in pinned primary specifications S051 (`libinput tools.rst` tag 1.32.0) and S052 (`wayland.xml` tag 1.26.0 core input semantics), joined reciprocally in `corpus/SOURCES.md`, indexed in `corpus/README.md`, and evaluated via `.ufo/waves/round-15/measure.py`.
   * C1 touches exclusively `corpus/` documentation and registry files. It requires no changes to `tools/mado-verify.sh`, no execution of mutation harnesses, and no modification of receipt headers.
2. **R14-V1 (Ancillary Mutation Receipt Precision):** An append-only correction (routed by verifier spotcheck `round-14-verifier-spotcheck.md:169`) explaining that the three historical mutation receipts (`regression-recut.txt`, `regular-target-mutants.txt`, `retained-census-mutants.txt`) carry provisional worktree headers (`input_binding: provisional worktree snapshot`, raw whole-gate hashes `ef50e262…` / `d6d5eb27…`), while their `MUTATE_TARGET` lines faithfully and independently bind the committed derived target `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96`.
   * R14-V1 is an unscored correction documented in `corpus/lessons/round-15.md` and `receipt-correction.json`. It introduces zero score changes, modifies no gate logic, and adds no test wrappers.
3. **Conclusion:** C1 and R14-V1 are strictly causally separable. C1 can land and verify without R14-V1, and R14-V1 can be documented without affecting U6 coverage. Choosing an extra claim (C2) is explicitly rejected.

---

## 3. Concrete False Inference: One-Case Overfit then Generalize Evidence Ladder

### 3.1 The Concrete False Inference
> **False Inference:** *"Observing an input device enumerated by libinput (e.g. `libinput list-devices`) or advertised by the compositor (e.g. `hyprctl devices` or `wl_seat.capabilities`) proves that input events reach the targeted client application / window."*

### 3.2 The One-Case Overfit
In a trivial, idealized desktop session (a single mapped terminal window with default US keyboard layout, no active keybindings, no layer-shell overlays, and no input method engine), pressing a physical key results in a character appearing on screen.

Overfitting to this single case treats the input pipeline as a transparent pipe:
$$\text{Physical Keypress} \xrightarrow{\quad\text{assumed direct}\quad} \text{Application Text}$$
This assumption fails in real-world desktop environments due to at least **eight independent drop, interception, or transformation gates** operating across distinct architectural layers:
1. *Hardware/Driver disabled:* Device node exists in `/dev/input/` but driver is unmapped or disabled in compositor config (`m_enabled = false`).
2. *Dynamic permission deny:* Compositor denies device access via permission gate (`m_allowed = false` in `InputManager.cpp:1620`).
3. *Global keybind interception:* Compositor keybind manager consumes the keycode as a window-manager shortcut (e.g. 192 active binds in `hyprctl binds`), never forwarding it to any Wayland surface unless flagged non-consuming (`n`).
4. *Exclusive surface grab:* Layer-shell surfaces (lockscreens, app launchers, modal overlays) hold exclusive keyboard focus, discarding or redirecting input away from active windows (`InputManager.cpp:454-465`).
5. *Unbound seat resource:* Client surface is mapped and active, but client has not issued `wl_seat.get_keyboard` (silent drop in `SeatManager.cpp:256`).
6. *Null active surface:* `wl_keyboard` resource exists, but compositor has not emitted `wl_keyboard.enter` for that specific client surface (`wayland.xml:2684-2686`).
7. *IME interception:* Keystrokes are intercepted by `zwp_input_method_v2.grab_keyboard` (fcitx5/ibus), yielding preedit composing states rather than committed text.
8. *Keycode offset & layout translation:* Wayland protocol delivers raw scancodes with $+8$ offset for XKB; non-text keys (modifiers, dead keys, function keys) produce zero characters (`xkbcommon.h:2060`).

### 3.3 The Generalize Evidence Ladder (Rungs 0 through 8)

The evidence ladder systematically disentangles each layer, defining its authoritative source, what observation proves, what it CANNOT prove, and its province/safety boundary:

| Rung | Layer & Tool Surface | Sourced Support | What Observation Proves | What It CANNOT Prove | Province & Safety Boundary |
|---|---|---|---|---|---|
| **R0** | **Kernel Device Node** (`/dev/input/event*`) | S051 (`tools.rst:31`) | Linux evdev character device exists and is recognized by the kernel driver. | Does NOT prove libinput or compositor opens, configures, or receives events from it. | **Out of province (`tsukuroi`).** Requires root; direct read/injection strictly forbidden. |
| **R1** | **Libinput Device Discovery** (`libinput list-devices`) | S051 (`tools.rst:45–46`, `tools.rst:78`) | Libinput driver identifies hardware capabilities and built-in driver defaults. | Does NOT prove compositor's effective configuration! (`"does not show your desktop's configuration"`). | Read-only doc inspection. Reopens round-12 trap M04 if equated to desktop config. |
| **R2** | **Libinput Event Stream** (`debug-events`, `record`, `replay`) | S051 (`tools.rst:135`, `:220`, `:262`) | Pre-compositor evdev event processing and driver quirks. | Does NOT prove what compositor forwards to any client surface. | **Forbidden live.** Privacy hazard (keystroke logging); replay creates uinput device. |
| **R3** | **Compositor Device Inventory** (`hyprctl devices`, `hyprctl getoption input:*`) | Pinned Hyprland `HyprCtl.cpp:784`, `SKILL.md:40` | Active compositor device objects and applied config options with `set` flags. | Does NOT prove client focus, key delivery, or absence of internal permission drop gates. | Read-only probe; includes virtual keyboards; hotplug-sensitive snapshot only. |
| **R4** | **Compositor Shortcut Interception** (`hyprctl binds`, `KeybindManager.cpp`) | Pinned Hyprland `KeybindManager.cpp:409`, `keybind-rule-semantics.md` | Active compositor global shortcuts that consume key events before surface dispatch. | Does NOT prove events reach client surfaces. Un-flagged binds swallow keys completely. | Read-only static inspection of binds table; 192 binds active on host. |
| **R5** | **Wayland Seat Capabilities** (`wl_seat.capabilities`) | S052 (`wayland.xml:2030–2057`), S041 (`globals.json`) | Seat-wide presence of keyboard/pointer capability bits sent upon client binding. | Does NOT prove any client holds focus or has created `wl_keyboard` objects. | Presence $\neq$ delivery (`wayland.xml:2014-2015`). Host advertises `wl_seat` v9. |
| **R6** | **Wayland Client Surface Focus** (`wl_keyboard.enter`, `wl_keyboard.key`) | S052 (`wayland.xml:2614–2686`) | Specific surface has keyboard focus and receives serialized key event with $+8$ scancode. | Does NOT prove application text commit or user-visible character insertion. | Protocol-level contract; gated on active surface (`wayland.xml:2684`). |
| **R7** | **Toolkit & IME Boundary** (`zwp_text_input_v3`, fcitx5) | Installed `text-input-unstable-v3.xml`, `xkbcommon.h` | Text-input protocol negotiation, compose states, and input-method grabs. | Does NOT prove text insertion. Modifiers/dead keys return 0 text; IME delivers preedit. | Toolkit-dependent boundary; fcitx5 configured in autostart; behavior unexercised. |
| **R8** | **Application Event Loop & Rendering** | Application internal state | Final text buffer insertion, widget cursor rendering, or command execution. | Unexercised on host. | Strictly marked `[UNK]` under C1 scope. |

---

## 4. Synthesis Across Round 15 Proposals & Resolution of Contradictions

A review of findings across all peer seats (`ReviewDocsEra`, `ReviewCensus`, `ReviewSourceTier`, `ReviewSeat`, `ReviewSafety`, `ReviewRouted`, `AttackMetric`, `AttackText`, `AttackDelivery`, `DerivedIntent`, `ReceiptMutation`, `MistakeRecord`) reveals five major cross-cutting contradictions:

### 4.1 Contradiction 1: Mid-Round Partial Upgrade vs Running Compositor Mapping
* **Peer Findings:** `ReviewDocsEra` (F1, F2) and `ReviewSafety` (F2) discovered that at `04:25:17`, `pacman -S --needed --noconfirm libinput libinput-tools` was executed, upgrading `libinput` from `1.31.3-1` to `1.32.0-1` and installing `libinput-tools`. However, Hyprland (PID 1706) continues to map `/usr/lib/libinput.so.10.13.0 (deleted)`. Meanwhile, `ReviewLibinput` initially found no libinput tools, and `wave/.../l2-scout` historically recorded libinput as absent.
* **Resolution & Non-Obvious Move:** The U6 note must explicitly distinguish **package metadata** (libinput `1.32.0-1` on disk) from **in-memory compositor runtime** (1.31.3 code mapped). Furthermore, U6 must anchor its documentation ladder strictly to upstream immutable tag `1.32.0` (`doc/user/tools.rst` sha256 `53264328…`) rather than mutable local binary behavior or moving web pages (`doc/latest`).

### 4.2 Contradiction 2: S007 Queued Collision vs S051 Reservation
* **Peer Findings:** `ReviewCensus` (F5), `ReviewSourceTier` (F2), and `ReviewSafety` (F1) noted that `corpus/SOURCES.md:19` already holds row S007 (`https://wayland.freedesktop.org/libinput/doc/latest/tools.html`, status `queued`, anchor unpinned "libinput 1.32.0 documentation"). Admitting a new row S051 with the same URL would trigger duplicate URL collision (E04 in `scripts/sources-census.sh`).
* **Resolution & Non-Obvious Move:** S051 must be registered with the version-pinned raw GitLab URL `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst`, tier `A`, kind `docs`, status `mined`, anchor tag `1.32.0` / commit `5cf833b5` / blob `390bab18` / sha256 `53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f`. Its `teaches` cell MUST open with `supersedes S007 —` to resolve the owed revision anchor debt while leaving S007 `queued` in historical records.

### 4.3 Contradiction 3: S043 Installed Path Duplication vs S052 Reservation
* **Peer Findings:** `ReviewCensus` (F6), `ReviewSourceTier` (F4), and `ReviewSeat` (F8) identified that S043 already cites `/usr/share/wayland/wayland.xml` for `wl_registry`. Reusing that path for S052 duplicates the row and relies on a mutable host path.
* **Resolution & Non-Obvious Move:** S052 must be registered with the upstream immutable GitLab URL `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml`, tier `A`, kind `spec`, status `mined`, tag `1.26.0` / commit `87cc8a87` / sha256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07` (verified byte-identical to installed `/usr/share/wayland/wayland.xml`), explicitly scoped to `wl_seat` (:2004), `wl_pointer` (:2138), and `wl_keyboard` (:2573).

### 4.4 Contradiction 4: R14-V1 Ancillary Mapping vs Full-Gate Receipt Rewriting
* **Peer Findings:** `DerivedIntent`, `ReceiptMutation`, `ReviewRouted`, and `MistakeRecord` analyzed R14-V1. The three historical mutation receipts (`regression-recut.txt`, `regular-target-mutants.txt`, `retained-census-mutants.txt`) carry provisional headers (`input_binding: provisional worktree snapshot`, raw whole-gate hashes `ef50e262…` / `d6d5eb27…`). However, their `MUTATE_TARGET` and restore lines bind derived target `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96`, re-derivable from committed gate bytes via `mado_r7_target_build` excision.
* **Resolution & Non-Obvious Move:** Do not rewrite historical receipt files or build generic test wrappers. Preserve the exact bytes of the three receipts (pinned sha256: `d5462634…`, `267de2b5…`, `57c462c2…`), and append an explanatory correction in `.ufo/waves/round-15/receipt-correction.json` and `corpus/lessons/round-15.md` mapping each provisional header to the independently derivable derived target `cd1d73d7…`.

### 4.5 Contradiction 5: Structural Counter Pass vs Semantic Safety Boundary
* **Peer Findings:** `AttackMetric` demonstrated that a structural measurement probe can pass an inverted or unsafe U6 note (e.g. one claiming `sudo libinput record` is safe). `ReviewCensus` (F1, F2) identified that `measure.py` must enforce U6 body facets and reciprocity.
* **Resolution & Non-Obvious Move:** Update `.ufo/waves/round-15/measure.py` to gate U6 specifically on:
  1. Header trio (`source:`, `verified-at:`, `recheck:`) plus `covers: U6`.
  2. Reciprocal mined joins to S051 and S052 with `used-by` agreement.
  3. Structural level-2 headings: `## Layer ladder`, `## Safe boundary`, and `## Unexercised delivery`.
  4. Final section `## Unexercised delivery` MUST contain explicit `[UNK]`.
  5. State in `SCORECARD.md` that the counter validates structural compliance, while semantic safety and quote fidelity remain L1-inspected.

---

## 5. The Proposed Move: "Unified Input Evidence Ladder & Provenance Pinning Contract (UIEL-PPC)"

We propose one bounded synthesis integrating the round's work across runtime, contract, substrate, and verification surfaces:

1. **Admit U6 Note `corpus/knowledge/input-layer-debugging-r15.md`:**
   * Structured strictly around the 8-rung evidence ladder (§3.3), quoting official libinput documentation (`tools.rst` tag 1.32.0) and Wayland core protocol (`wayland.xml` tag 1.26.0).
   * Enforces the three mandatory sections: `## Layer ladder`, `## Safe boundary`, and `## Unexercised delivery` (with `[UNK]` in the final section).
   * Explicitly disclaims raw event capture, keystroke logging, uinput replay, and kernel diagnosis.
2. **Register S051 and S052 with Clean Provenance:**
   * S051: Pinned to `libinput` tag 1.32.0 raw GitLab URL, sha256 `53264328…`, `teaches` opening `supersedes S007 —`.
   * S052: Pinned to `wayland` tag 1.26.0 raw GitLab URL, sha256 `cc860987…`, scoped to core seat/pointer/keyboard semantics.
   * Both rows set to `tier = A`, `status = mined`, `used-by = corpus/knowledge/input-layer-debugging-r15.md`.
3. **Execute R14-V1 Ancillary Receipt Correction:**
   * Author `.ufo/waves/round-15/receipt-correction.json` providing the exact mapping from provisional headers (`ef50e262…`, `d6d5eb27…`) to the committed derived target `cd1d73d7…`.
   * Keep historical mutation receipts byte-identical.
4. **Update Indexing & Scorecard:**
   * Add `input-layer-debugging-r15.md` to `corpus/README.md` table (advancing indexed notes from 28 to 29).
   * Advance `SCORECARD.md` Claim C1 from 5/7 (7.1429/10) to 6/7 (8.5714/10), noting U7 as the sole retained gap.

---

## 6. Risks and Mitigations

| Risk | Severity | Second-Order Impact | Mitigation |
|---|---|---|---|
| **URL Duplicate Collision in Census** | High | S051 using the same URL as queued S007 triggers `sources-census.sh` E04 failure. | Use the version-pinned raw GitLab URL for S051 and open `teaches` with `supersedes S007 —`. |
| **Package vs Runtime Version Desync** | High | Claiming host libinput is 1.32.0 when Hyprland maps deleted 1.31.3 library introduces false host fact. | Explicitly decouple on-disk package version (`1.32.0-1`) from running compositor mapping (`1.31.3`), anchoring ladder to upstream spec. |
| **Keystroke Logging Privacy Leak** | High | Recommending `debug-events` or `record` captures operator passwords / sensitive scancodes. | Explicitly forbid event recording in `## Safe boundary`; label all event capture out of province (`kagi`/contract fence). |
| **Counter False-Green on Inverted Boundary** | Medium | Structural counter passes a note that claims live event capture is safe. | Counter gates on `[UNK]` in `## Unexercised delivery`; L1 conducts explicit semantic quote audit. |
| **Numerator Trap in SCORECARD Count** | Medium | Grepping `source:` lines yields 6 or 7 due to multi-source notes or non-U notes. | Counter strictly reports `len(covered)` unique U-items; score is reported as 6/7 = 8.5714, not 10. |
| **Excision Target Movement (PIN_MADO)** | Low | Editing `tools/mado-verify.sh` outside excised blocks moves derived target SHA. | Gate code remains completely untouched in Round 15; exact gate SHA `fba82a66…` is preserved. |

---

## 7. Verification Plan for L1 Integration

Post-integration verification sequence for the canonical planner:

1. **Source Registry Census & Integrity:**
   ```bash
   /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
   ```
   *Must exit 0 (`mado ok`), with zero E-code errors (retaining only pre-existing W04 warnings).*
2. **File Plane & Selftest Verification (Harm Watch):**
   ```bash
   bash tools/mado-verify.sh --selftest
   bash tools/mado-verify.sh --no-live
   ```
   *Selftest must pass 372/372 assertions; `--no-live` must remain 29 PASS, 0 FAIL, 0 UNKNOWN, 8 SKIP, 4 NOTE.*
3. **C1 Revision-Bound Measurement Probe:**
   ```bash
   python3 .ufo/waves/round-15/measure.py HEAD
   ```
   *Must report `covered: ['U1', 'U2', 'U3', 'U4', 'U5', 'U6']`, `count: 6`, `score: 8.5714`, with U6 structural facets true and S051/S052 reciprocal joins true.*
4. **README Navigation Completeness:**
   *Verify `corpus/README.md` lists exactly 29 knowledge notes matching `corpus/knowledge/*.md` (0 missing, 0 dangling, 0 duplicates).*
5. **Historical Receipt Byte Integrity:**
   *Confirm SHA-256 of `.ufo/waves/round-14/evidence/{regression-recut,regular-target-mutants,retained-census-mutants}.txt` remain byte-identical to `d5462634…`, `267de2b5…`, `57c462c2…`.*

---

**Tooling Record:** No tools installed or upgraded during this data walk. Standard read-only inspection tools were used.
