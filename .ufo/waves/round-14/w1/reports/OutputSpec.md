# OutputSpec — rendered report (mado-r14-w1)

Full findings: `.ufo/waves/round-14/w1/OutputSpec.md`. Seat: `OutputSpec` (scout). Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Reserved source row: `S047`. No protocol clients executed; read-only XML analysis.

---

## 1. Source Open & Precedence

1. **Installed protocol XML `[OBS]`**:
   - Package: `wlr-protocols r112.a741f0a-1` installed via `sudo pacman -S --needed --noconfirm wlr-protocols` (official Arch Linux `extra`).
   - Path: `/usr/share/wlr-protocols/unstable/wlr-output-management-unstable-v1.xml` (611 lines).
   - Package commit: `a741f0ac5d655338a5100fc34bc8cec87d237346` (tagged `r112`, 2025-08-16).
   - Digest: `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7`.

2. **Upstream Git Repositories `[OBS]`**:
   - Standalone repository: `https://gitlab.freedesktop.org/wlroots/wlr-protocols`
   - Exact commit touching XML: `a5028afbe4a1cf0daf020c4104c1565a09d6e58a` (2025-07-02, author Simon Ser).
   - Canonical raw URL: `https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/a5028afbe4a1cf0daf020c4104c1565a09d6e58a/unstable/wlr-output-management-unstable-v1.xml`
   - Sibling wlroots commit: `cdd2c7e0064efee7fd398b2935923508b2fa9842` (2025-09-10).
   - Byte equality: Both local package file and raw git URLs yield identical SHA-256 `65b0f82a...`.

---

## 2. Key Findings: Protocol Semantics

1. **Read-Only vs. Mutation Separation**:
   - `zwlr_output_manager_v1` (v4), `zwlr_output_head_v1` (v4), `zwlr_output_mode_v1` (v3) form the read-only plane.
   - Output devices (heads) are advertised even when disabled/turned off.
   - Head metadata (`name`, `description`, `physical_size`, `make`, `model`, `serial_number`, modes) is read-only.
   - Reconfiguration cannot be executed directly on head objects; it requires an explicit `zwlr_output_configuration_v1` object.

2. **Exhaustive Configuration Invariant**:
   - Every head known to the client must be explicitly configured via `enable_head` or `disable_head`.
   - Omitting any head is a fatal protocol error (`unconfigured_head = 2`).
   - Duplicate head configuration is a fatal protocol error (`already_configured_head = 1`).

3. **Validation (`test`) vs. Application (`apply`)**:
   - `test`: Non-mutating validation dry-run in specification (`[INF-docs]`). Evaluates whether the requested configuration is supported without altering display state. Test success does not guarantee apply success. Host compositors may stub this behavior: e.g. pinned Hyprland v0.56.2 (`src/protocols/OutputManagement.cpp:343-346`) stubs `applyTestConfiguration` to unconditionally return true, and `disable_head` (`:298-324`) eagerly saves `enabled=false` and reloads before `apply` or `test` is called.
   - `apply`: Mutating transaction. Commits configuration to compositor and display hardware.
   - Both requests consume the configuration object; subsequent requests other than `destroy` trigger `already_used = 3`.

4. **Terminal Outcomes**:
   - `succeeded`: Configuration accepted/tested. Client destroys configuration object. If applied, compositor sends change events followed by `wlr_output_manager.done`.
   - `failed`: Configuration rejected or modeset failed. Mandatory rollback: compositor must revert changes made by the apply request (`[INF-docs]`). Client destroys object.
   - `cancelled`: Output topology changed concurrently (e.g. monitor hotplug/unplug). Outdated serial. Client destroys object, waits for updated heads and new `done(serial)`, and retries (`[INF-docs]`). Hyprland v0.56.2 does not implement `sendCancelled()` or enforce serial checks.

5. **Serial Concurrency Guard**:
   - `zwlr_output_manager_v1.done(serial)` provides an atomic generation counter.
   - `create_configuration(serial)` binds the staging transaction to that generation.
   - Prevents stale configuration application during hotplug races in protocol specification (`[INF-docs]`). Note that in Hyprland 0.56.2, serial is unused in `create_configuration`.

---

## 3. Candidate Full Registry Row (S047)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S047 | wlr-output-management protocol — /usr/share/wlr-protocols/unstable/wlr-output-management-unstable-v1.xml; https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/a5028afbe4a1cf0daf020c4104c1565a09d6e58a/unstable/wlr-output-management-unstable-v1.xml | spec | A | wlr-output-management v1 transaction model: read-only head advertisement, serial-guarded atomic test/apply, terminal outcome events | wlr-protocols r112.a741f0a-1 XML @ a5028afb (2025-07-02); zwlr_output_manager_v1:43-125, zwlr_output_head_v1:129-143, zwlr_output_configuration_v1:423-539 | Documented protocol semantics [INF-docs]: heads are read-only; configuration staging is explicit and must account for all heads; test validates without mutation; apply mutates; failure requires compositor revert; outdated serial causes cancellation. Does not assert host compositor implementation fidelity | mined | 2026-10-20 | on-release | corpus/knowledge/wayland-output-management-r14.md |

---

## 4. Located Quotations (≤ 25 Words Each)

All quotations opened 2026-10-20 from `/usr/share/wlr-protocols/unstable/wlr-output-management-unstable-v1.xml` (SHA-256 `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7`):

1. **Read-only head** (`zwlr_output_head_v1`, `:132-135`):
   > "A head object only advertises properties and cannot be used directly to change them. A head has some read-only properties: modes, name, description and physical_size." (24 words)
2. **Serial binding** (`zwlr_output_manager_v1.done`, `:94-95`):
   > "A serial is sent to be used in a future create_configuration request." (12 words)
3. **Exhaustive configuration rule** (`zwlr_output_configuration_v1`, `:429-432`):
   > "It is a protocol error to send two enable_head or disable_head requests with the same head. It is a protocol error to omit a head in a configuration." (25 words)
4. **Test semantics** (`zwlr_output_configuration_v1.test`, `:483-485`):
   > "Test the new output configuration. The configuration won't be applied, but will only be validated." (14 words)
5. **Terminal response obligation** (`zwlr_output_configuration_v1.apply`, `:476-478`):
   > "After this request has been sent, the compositor must respond with an succeeded, failed or cancelled event." (16 words)
6. **Failure revert requirement** (`zwlr_output_configuration_v1.failed`, `:508-511`):
   > "Sent if the compositor rejects the changes or failed to apply them. The compositor should revert any changes made by the apply request that triggered this event." (25 words)
7. **Hotplug race cancellation** (`zwlr_output_configuration_v1.cancelled`, `:517-521`):
   > "Sent if the compositor cancels the configuration because the state of an output changed and the client has outdated information (e.g. after an output has been hotplugged)." (24 words)

---

## 5. Scope Admission, Rejections & Flips

- **Admit `[INF-docs]`**: Pinned upstream specification `wlr-output-management-unstable-v1.xml` at commit `a5028afb` / package `r112.a741f0a-1` for U5 output-management boundaries.
- **Reject 1**: *"Global advertisement of `zwlr_output_manager_v1` in `wl_registry` proves active display management or working modesetting."*
  - **Flip**: Verified client transaction issuing `create_configuration`, configuring heads, and receiving `succeeded` followed by updated `wlr_output_manager.done`. (Executing live `apply` or `disable_head` requests against a host session is an active compositor mutation altering display hardware state; prohibited in uncontained desktop sessions).
- **Reject 2**: *"A client can reconfigure an individual output without specifying the state of other connected outputs."*
  - **Flip**: None under `zwlr_output_management_unstable_v1` (protocol error `unconfigured_head`).
- **Reject 3**: *"A successful `test` request guarantees that a subsequent `apply` request will succeed."*
  - **Flip**: None (runtime hardware resources, DRM/KMS allocation, and hotplug events can fail at apply time; compositors stubbing `test` provide no hardware validation).

---

## 6. Tooling Directive Record

- **Tool**: `wlr-protocols`
- **Version**: `r112.a741f0a-1`
- **Channel**: `sudo pacman -S --needed --noconfirm wlr-protocols` (official Arch Linux `extra`)
- **Reason**: Installed official version-pinned protocol XML locally at `/usr/share/wlr-protocols/unstable/wlr-output-management-unstable-v1.xml` per assignment precedence.
