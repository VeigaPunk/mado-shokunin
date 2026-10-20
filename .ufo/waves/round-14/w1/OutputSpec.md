# OutputSpec — wlr-output-management unstable protocol specification (mado-r14-w1)

Date: 2026-10-20. Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Seat: `OutputSpec` (scout).
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Reserved source row: `S047`.
Evaluation axes: **coverage** (C1 sourced U5 output-management boundaries) and **operability** (C2 source target resolver).

Labels: `[OBS]` observed in this seat from primary files; `[INF-docs]` documented protocol semantics; `[UNK]` unexercised host behavior.

---

## 1. Executive Summary & Source Precedence

Per the assignment directive, installed protocol files are preferred when version-pinned, followed by canonical upstream raw URLs.

1. **Installed Protocol File `[OBS]`**:
   - Package: `wlr-protocols r112.a741f0a-1` installed via official Arch Linux channel (`extra/wlr-protocols`).
   - File path: `/usr/share/wlr-protocols/unstable/wlr-output-management-unstable-v1.xml`
   - File length: 611 lines.
   - SHA-256 digest: `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7`
   - Installed package commit: `a741f0ac5d655338a5100fc34bc8cec87d237346` (tagged `r112`, 2025-08-16).

2. **Upstream Git Repositories `[OBS]`**:
   - Primary protocol repository: `https://gitlab.freedesktop.org/wlroots/wlr-protocols`
   - Exact commit touching `unstable/wlr-output-management-unstable-v1.xml`: `a5028afbe4a1cf0daf020c4104c1565a09d6e58a` (2025-07-02, author Simon Ser, title *"output-management: refer to wl_output instead of xdg-output"*).
   - Canonical raw URL: `https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/a5028afbe4a1cf0daf020c4104c1565a09d6e58a/unstable/wlr-output-management-unstable-v1.xml`
   - Sibling wlroots repository reference: `https://gitlab.freedesktop.org/wlroots/wlroots/-/raw/cdd2c7e0064efee7fd398b2935923508b2fa9842/protocol/wlr-output-management-unstable-v1.xml` (cited in round 13 `ReviewPhases.md`).
   - Byte verification: The installed XML and the raw upstream XML at `a5028afb` / `cdd2c7e0` share the identical SHA-256 digest (`65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7`).

3. **Client Protocol Execution**:
   - In accordance with seat instructions, no live Wayland protocol clients were executed.

---

## 2. Protocol Architecture & Semantic Boundaries

The protocol defines five interfaces forming two strictly separated operational planes: the **read-only advertisement plane** and the **staged transactional mutation plane**.

```
[ Read-Only Advertisement Plane ]
  zwlr_output_manager_v1 (v4)
    ├── event: head ──────────────► zwlr_output_head_v1 (v4)
    │                                 ├── events: name, description, physical_size, make, model, serial_number
    │                                 ├── events: enabled, current_mode, position, transform, scale, adaptive_sync
    │                                 └── event: mode ──► zwlr_output_mode_v1 (v3)
    └── event: done(serial) ──┐                           ├── events: size, refresh, preferred
                              │
[ Staged Transaction Plane ]  │ (ties transaction to topology generation)
  zwlr_output_manager_v1.create_configuration(serial)
    │
    ▼
  zwlr_output_configuration_v1 (v4)
    ├── request: enable_head ─────► zwlr_output_configuration_head_v1 (v4)
    │                                 └── requests: set_mode, set_custom_mode, set_position,
    │                                               set_transform, set_scale, set_adaptive_sync
    ├── request: disable_head
    ├── request: test  ───────────┐ (non-mutating validation probe)
    ├── request: apply ───────────┼──► Exactly ONE terminal response:
    └── request: destroy          │     ├── event: succeeded (destroy object; changes batched to done)
                                  │     ├── event: failed (destroy object; compositor reverts changes)
                                  └─────└── event: cancelled (destroy object; serial stale, retry)
```

### 2.1 Read-Only Advertisement vs. Mutation Plane
- **Read-only objects**: `zwlr_output_manager_v1`, `zwlr_output_head_v1`, `zwlr_output_mode_v1`.
  - Heads represent display devices (physical monitors or virtual windows) and are advertised even when powered off or disabled (unlike `wl_output`).
  - Clients cannot create or destroy heads or modes.
  - Read-only metadata (`name`, `description`, `physical_size`, `make`, `model`, `serial_number`, supported modes) cannot be altered by clients.
  - Mutable properties (`enabled`, `current_mode`, `position`, `transform`, `scale`, `adaptive_sync`) cannot be directly mutated on head objects; head events merely report state after atomic commit via `zwlr_output_manager_v1.done`.
- **Transactional mutation objects**: `zwlr_output_configuration_v1`, `zwlr_output_configuration_head_v1`.
  - Created specifically for a single atomic reconfiguration attempt.
  - **Exhaustive configuration requirement**: Every head known to the client must be explicitly configured via `enable_head` or `disable_head`. Omitting any head triggers fatal protocol error `unconfigured_head` (value 2).
  - Configuring the same head twice triggers fatal protocol error `already_configured_head` (value 1).

### 2.2 Configuration Test vs. Apply Semantics
- **`test` request (`zwlr_output_configuration_v1`)**:
  - Semantic: Server-side validation dry-run without altering compositor display state (`[INF-docs]`).
  - Scope: Non-mutating probe in the specification. Validates whether the hardware and compositor can satisfy the requested modes, scale, position, and timings.
  - Caveat 1: Protocol explicitly specifies that succeeding a `test` request does not guarantee that a subsequent `apply` request will succeed (e.g., dynamic hardware resource allocation changes).
  - Caveat 2 (Host Divergence): Documented non-mutating behavior is an `[INF-docs]` protocol specification semantic, not guaranteed host behavior. Pinned Hyprland v0.56.2 (`src/protocols/OutputManagement.cpp:343-346`) stubs `applyTestConfiguration` to unconditionally return `true`, and `disable_head` (`:298-324`) eagerly saves `enabled=false` and calls `scheduleReload` before `apply` or `test` is even invoked.
- **`apply` request (`zwlr_output_configuration_v1`)**:
  - Semantic: Commits the requested output configuration to hardware and compositor layout.
  - Scope: Mutating transaction.
  - Post-condition: Sending any request other than `destroy` after `apply` or `test` is fatal protocol error `already_used` (value 3).

### 2.3 Terminal Events (`succeeded`, `failed`, `cancelled`)
Following an `apply` or `test` request, the compositor MUST respond with exactly one terminal event:
1. **`succeeded`**:
   - Indicates successful validation (for `test`) or successful hardware/compositor application (for `apply`).
   - If output state changed as a result of `apply`, updated head/mode events are emitted, followed by a new `zwlr_output_manager_v1.done` event.
   - Client obligation: destroy the configuration object upon receipt.
2. **`failed`**:
   - Sent when the compositor rejects the configuration or fails hardware application.
   - Compositor obligation: reversibility — the compositor must revert any intermediate state changes made by the triggering apply request.
   - Client obligation: destroy the configuration object upon receipt.
3. **`cancelled`**:
   - Sent when the output topology changes concurrently (e.g. monitor hotplug, disconnect) before the configuration could be evaluated, invalidating the client's topology assumptions.
   - Client obligation: destroy the configuration object, read newly emitted head events, obtain the new configuration serial from `done`, and reconstruct the configuration transaction.
   - Host Implementation Note: Serial invalidation and `cancelled` event emission are specification requirements (`[INF-docs]`); Hyprland v0.56.2 does not emit `sendCancelled()` or enforce serial matches on `create_configuration`.

### 2.4 Serial Changes & Hotplug Race Protection
- Generation tracking: `zwlr_output_manager_v1.done` passes a `serial: uint` representing the current output generation.
- Binding: `create_configuration(serial)` binds the proposed transaction to that exact generation.
- Concurrency protection: If any output changes between client receipt of `done` and compositor evaluation of `apply` or `test`, the serial is obsolete and the transaction is aborted with `cancelled` (`[INF-docs]`).
- Host limitation: While the wire protocol requires serial tracking, host compositors may accept transactions blindly (in Hyprland 0.56.2, serial is unused in `create_configuration`).

---

## 3. Candidate Full Registry Row (S047)

Prepared for incorporation into `corpus/SOURCES.md`:

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S047 | wlr-output-management protocol — /usr/share/wlr-protocols/unstable/wlr-output-management-unstable-v1.xml; https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/a5028afbe4a1cf0daf020c4104c1565a09d6e58a/unstable/wlr-output-management-unstable-v1.xml | spec | A | wlr-output-management v1 transaction model: read-only head advertisement, serial-guarded atomic test/apply, terminal outcome events | wlr-protocols r112.a741f0a-1 XML @ a5028afb (2025-07-02); zwlr_output_manager_v1:43-125, zwlr_output_head_v1:129-143, zwlr_output_configuration_v1:423-539 | Documented protocol semantics [INF-docs]: heads are read-only; configuration staging is explicit and must account for all heads; test validates without mutation; apply mutates; failure requires compositor revert; outdated serial causes cancellation. Does not assert host compositor implementation fidelity | mined | 2026-10-20 | on-release | corpus/knowledge/wayland-output-management-r14.md |

---

## 4. Located Quotations (≤ 25 Words Each)

All quotes located directly in the pinned `/usr/share/wlr-protocols/unstable/wlr-output-management-unstable-v1.xml` (SHA-256 `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7`), opened 2026-10-20:

| # | Topic | Location | Exact Quote | Words | Teaches / Scope |
|---|---|---|---|---|---|
| 1 | Read-only head | `zwlr_output_head_v1` description (`:132-135`) | "A head object only advertises properties and cannot be used directly to change them. A head has some read-only properties: modes, name, description and physical_size." | 24 | [INF-docs] Heads advertise properties; metadata cannot be client-mutated. |
| 2 | Serial binding | `zwlr_output_manager_v1.done` description (`:94-95`) | "A serial is sent to be used in a future create_configuration request." | 12 | [INF-docs] Configuration creation requires explicit serial binding. |
| 3 | Exhaustive heads rule | `zwlr_output_configuration_v1` description (`:429-432`) | "It is a protocol error to send two enable_head or disable_head requests with the same head. It is a protocol error to omit a head in a configuration." | 25 | [INF-docs] All heads must be explicitly enabled or disabled in every configuration. |
| 4 | Test validation semantics | `zwlr_output_configuration_v1.test` description (`:483-485`) | "Test the new output configuration. The configuration won't be applied, but will only be validated." | 14 | [INF-docs] Documented test purpose is non-mutating validation; host may stub. |
| 5 | Outcome event requirement | `zwlr_output_configuration_v1.apply` description (`:476-478`) | "After this request has been sent, the compositor must respond with an succeeded, failed or cancelled event." | 16 | [INF-docs] Apply and test requests require exactly one terminal reply event. |
| 6 | Failure revert requirement | `zwlr_output_configuration_v1.failed` description (`:508-511`) | "Sent if the compositor rejects the changes or failed to apply them. The compositor should revert any changes made by the apply request that triggered this event." | 25 | [INF-docs] Failed apply transactions mandate compositor-side state rollback. |
| 7 | Hotplug cancellation | `zwlr_output_configuration_v1.cancelled` description (`:517-521`) | "Sent if the compositor cancels the configuration because the state of an output changed and the client has outdated information (e.g. after an output has been hotplugged)." | 24 | [INF-docs] Concurrent output topology mutations trigger transaction cancellation. |

---

## 5. Scope Admissions, Rejections, and Flips

### 5.1 Admission
- **Admit `[INF-docs]`**: Primary specification `zwlr_output_management_unstable_v1` (v4) at pinned revision `a5028afb` (package `wlr-protocols r112.a741f0a-1`). Establishes:
  1. The formal boundary separating read-only head discovery from transactional staging.
  2. The documented non-mutating validation nature of `test` vs. hardware/compositor mutation in `apply`.
  3. The three distinct terminal outcomes (`succeeded`, `failed` with mandatory rollback, `cancelled` with hotplug race protection).

### 5.2 Rejections & Flips
1. **Reject**: *"Compositor advertisement of `zwlr_output_manager_v1` global interface in `wl_registry` proves active monitor modesetting or working display configuration on the host."*
   - Rationale: Advertisement in `wl_registry` only establishes interface availability. It does not validate display hardware capabilities, test validity, or verify successful application.
   - **Flip**: A verified client test/apply transaction executing `create_configuration`, configuring heads, and receiving the `succeeded` event followed by updated `done` events.  
     *Safety & Governance Note*: Executing live `apply` or `disable_head` requests against a host session is an active compositor mutation that alters physical display state (and in Hyprland 0.56.2 triggers eager monitor reloads before transaction completion). Any such probe requires an isolated headless testing compositor, never an uncontained desktop session.
2. **Reject**: *"A client can reconfigure an individual output without specifying the state of other connected outputs."*
   - Rationale: Protocol line 431 explicitly dictates: *"It is a protocol error to omit a head in a configuration."*
   - **Flip**: None under `wlr_output_management_unstable_v1`; would require a revised or alternate protocol interface.
3. **Reject**: *"A successful `test` request guarantees that a subsequent `apply` request will succeed."*
   - Rationale: Line 486 explicitly documents: *"Even if the compositor succeeds to test a configuration, applying it may fail."* DRM/KMS hardware resource limits, timing differences, or concurrent hotplug events can fail at apply time. Furthermore, on compositors where `test` is stubbed (such as Hyprland 0.56.2), `test` succeeding provides zero assurance of hardware configuration support.
   - **Flip**: None; runtime modeset application remains fallible even after successful validation.

---

## 6. Tooling Directive Record

In accordance with `/home/vgpnk/.omp/agent/RULES.md` (Operator tooling directive, 2026-10-19):

| Tool | Version | Channel | Reason |
|---|---|---|---|
| `wlr-protocols` | `r112.a741f0a-1` | `sudo pacman -S --needed --noconfirm wlr-protocols` (official Arch Linux `extra`) | Provide local version-pinned primary protocol XML at `/usr/share/wlr-protocols/unstable/wlr-output-management-unstable-v1.xml` per assignment precedence. |
