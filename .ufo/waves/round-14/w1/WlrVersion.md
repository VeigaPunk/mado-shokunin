# WlrVersion — Official wlr-protocols Revision/Tag and Transaction Semantics (mado-r14-w1)

**Seat:** `MadoR14.WlrVersion` (scout, leaf; no subagent dispatch, no background jobs).  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`.  
**Milestone:** U5 boundaries and regular-source targets.  
**Judged on:** coverage, operability.  
**Draft path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/WlrVersion.md`  
**Report path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/reports/WlrVersion.md`  
**Date:** 2026-10-20.  
**Status:** complete findings; no shared repo files edited; no tests/builds/selftests run.

---

## 1. Executive Summary & Bottom Line

1. **Tag Status (Untagged Upstream):**  
   The official `wlr-protocols` upstream repository (`https://gitlab.freedesktop.org/wlroots/wlr-protocols`) contains **zero git tags** (`git tag -l` and `git ls-remote --tags` yield empty). Upstream has never tagged releases. Downstream distributions track commit snapshots (e.g. Arch Linux official repository package `extra/wlr-protocols` version `r112.a741f0a-1`, which packages commit `a741f0ac5d655338a5100fc34bc8cec87d237346`).
2. **Branch & Commit Pinned Revisions:**  
   - Default branch: `master`.
   - `master` branch HEAD commit: `bf4fc79abc359eea5a0edec0ac6d4a2b2955f82a` (committed 2026-03-09T11:15:36-03:00, "wlr-export-dmabuf-unstable-v1: fix typo").
   - Last commit modifying `unstable/wlr-output-management-unstable-v1.xml`: `a5028afbe4a1cf0daf020c4104c1565a09d6e58a` (committed 2025-07-02T07:20:08Z / authored 2025-06-05T17:32:03+02:00, "output-management: refer to wl_output instead of xdg-output").
   - Blob SHA-256: `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7` (611 lines, 26,355 bytes). The file is byte-identical across `a5028af`, Arch package `a741f0a`, and `master` HEAD `bf4fc79`.
3. **Repository Disambiguation (`wlr-protocols` vs `wlroots`):**  
   Round 13 (`ReviewPhases.md` / `ScribeFrontier.md`) referenced `wlroots` commit `cdd2c7e0064efee7fd398b2935923508b2fa9842` under `https://gitlab.freedesktop.org/wlroots/wlroots`. Commit `cdd2c7e0` belongs to the `wlroots/wlroots` compositor library repository and does **not** exist in the `wlroots/wlr-protocols` repository. While the XML payload blob hash is identical (`65b0f82a…`), any canonical citation of `wlr-protocols` must cite the `wlr-protocols` repository commit (`a5028af` or `bf4fc79`), not `cdd2c7e0`.
4. **Transaction Semantics (`test` vs `apply`):**  
   - `test` (lines 481–494): Strictly non-mutating validation. "Test the new output configuration. The configuration won't be applied, but will only be validated." (15 words). Crucial caveat: "Even if the compositor succeeds to test a configuration, applying it may fail." (13 words).
   - `apply` (lines 466–479): Mutates compositor state. "Apply the new output configuration." (5 words). With caveat: "In case the configuration is successfully applied, there is no guarantee that the new output state matches completely the requested configuration." (20 words).
   - Both share a locked transaction lifecycle and the same three mutually exclusive outcome events: `succeeded` (lines 496–505), `failed` (lines 507–515), or `cancelled` (lines 517–528), terminated by `destroy` (lines 530–538).

---

## 2. Official Source Verification

### 2.1 Repository & Upstream Metadata

- **Canonical Repository URL:** `https://gitlab.freedesktop.org/wlroots/wlr-protocols`
- **Git Clone URL:** `https://gitlab.freedesktop.org/wlroots/wlr-protocols.git`
- **File in Tree:** `unstable/wlr-output-management-unstable-v1.xml`
- **Canonical Raw URL (last modifying commit):**  
  `https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/a5028afbe4a1cf0daf020c4104c1565a09d6e58a/unstable/wlr-output-management-unstable-v1.xml`
- **Canonical Raw URL (master HEAD):**  
  `https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/bf4fc79abc359eea5a0edec0ac6d4a2b2955f82a/unstable/wlr-output-management-unstable-v1.xml`
- **Canonical Blob URL (master HEAD):**  
  `https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/blob/bf4fc79abc359eea5a0edec0ac6d4a2b2955f82a/unstable/wlr-output-management-unstable-v1.xml`

### 2.2 Independent Revision & Tag Findings

| Facet | Finding | Evidence / Command |
|---|---|---|
| Git Tags | **None (0 tags)** | `git tag -l` → empty; `git ls-remote --tags https://gitlab.freedesktop.org/wlroots/wlr-protocols.git` → empty. |
| Downstream Packaging | `r112.a741f0a-1` | `pacman -Si wlr-protocols`: version `r112.a741f0a-1`, build date 2025-10-04, commit `a741f0ac5d655338a5100fc34bc8cec87d237346`. |
| Default Branch | `master` | `git remote show origin` / `refs/heads/master`. |
| Master Branch HEAD SHA | `bf4fc79abc359eea5a0edec0ac6d4a2b2955f82a` | Commit date 2026-03-09T11:15:36-03:00; author Diego Viola. |
| Last Modifying Commit SHA | `a5028afbe4a1cf0daf020c4104c1565a09d6e58a` | Commit date 2025-07-02T07:20:08Z; author Simon Ser; subject "output-management: refer to wl_output instead of xdg-output". |
| File Diff (`a5028af` vs `bf4fc79`) | **Zero difference (identical)** | `git diff a5028af..bf4fc79 -- unstable/wlr-output-management-unstable-v1.xml` → empty. |
| File Blob SHA-256 | `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7` | `sha256sum unstable/wlr-output-management-unstable-v1.xml` (26,355 bytes, 611 lines). |
| `wlroots/wlroots` contrast | Commit `cdd2c7e0` is in `wlroots`, NOT `wlr-protocols` | `git cat-file -e cdd2c7e0064efee7fd398b2935923508b2fa9842` fails in `wlr-protocols`. |

---

## 3. Transaction Semantics: `test` versus `apply` Purpose

All line numbers are indexed to `unstable/wlr-output-management-unstable-v1.xml` (611 lines, sha256 `65b0f82a…`).

### 3.1 Overview of Transaction Object (`zwlr_output_configuration_v1`)

Interface `zwlr_output_configuration_v1` (version 4, lines 425–539) defines a staged transaction created via `zwlr_output_manager_v1.create_configuration(id, serial)` (lines 99–106).

- **Lifecycle summary (lines 433–436):**
  > "Then, the client can apply or test the configuration. The compositor will then reply with a succeeded, failed or cancelled event. Finally the client should destroy the configuration object." (27 words; located excerpt below)
- **Located quote (21 words, lines 433–435):**
  > "Then, the client can apply or test the configuration. The compositor will then reply with a succeeded, failed or cancelled event."
- **Pre-execution constraints:**
  - Client must configure every head: each head is either enabled via `enable_head` (lines 447–456) or disabled via `disable_head` (lines 458–464).
  - Protocol error `already_configured_head` (value 1): sent two enable or disable requests for the same head.
  - Protocol error `unconfigured_head` (value 2): omitted any head from the configuration.
  - Protocol error `already_used` (value 3): sending any request after `apply` or `test` has already been sent (except the `destroy` destructor).

### 3.2 Request: `apply` (Lines 466–479)

```xml
    <request name="apply">
      <description summary="apply the configuration">
        Apply the new output configuration.

        In case the configuration is successfully applied, there is no guarantee
        that the new output state matches completely the requested
        configuration. For instance, a compositor might round the scale if it
        doesn't support fractional scaling.

        After this request has been sent, the compositor must respond with an
        succeeded, failed or cancelled event. Sending a request that isn't the
        destructor is a protocol error.
      </description>
    </request>
```

- **Primary Purpose Quote (5 words, lines 467–468):**
  > "Apply the new output configuration."
- **State Non-Guarantee Quote (20 words, lines 470–473):**
  > "In case the configuration is successfully applied, there is no guarantee that the new output state matches completely the requested configuration."
- **Semantic Classification:** **Mutation**. Directly commands the compositor to commit changes to the active display pipeline (modesetting, output resolution, scale, position, transform, adaptive sync, enabling/disabling physical heads).

### 3.3 Request: `test` (Lines 481–494)

```xml
    <request name="test">
      <description summary="test the configuration">
        Test the new output configuration. The configuration won't be applied,
        but will only be validated.

        Even if the compositor succeeds to test a configuration, applying it may
        fail.

        After this request has been sent, the compositor must respond with an
        succeeded, failed or cancelled event. Sending a request that isn't the
        destructor is a protocol error.
      </description>
    </request>
```

- **Primary Purpose Quote (15 words, lines 482–484):**
  > "Test the new output configuration. The configuration won't be applied, but will only be validated."
- **Caveat Quote (13 words, lines 486–487):**
  > "Even if the compositor succeeds to test a configuration, applying it may fail."
- **Semantic Classification:** **Read-only atomic validation**. Evaluates whether the requested configuration would be valid and acceptable to the compositor/KMS driver without changing the current display state. Crucially, a positive test result is advisory: subsequent `apply` may still fail due to dynamic hardware state, race conditions, or unmodeled resource contention.

### 3.4 Terminal Outcome Events (Lines 496–528)

Once either `apply` or `test` is sent, the compositor MUST respond with exactly one of three mutually exclusive events:

1. **`succeeded` (lines 496–505):**
   - Quote (12 words, lines 497–499):
     > "Sent after the compositor has successfully applied the changes or tested them."
   - Follow-up: If the current configuration was changed (i.e. under `apply`), updated head/mode events are emitted followed by `zwlr_output_manager_v1.done`.
2. **`failed` (lines 507–515):**
   - Quote (12 words, lines 508–510):
     > "Sent if the compositor rejects the changes or failed to apply them."
   - Revert guarantee (15 words, lines 510–512):
     > "The compositor should revert any changes made by the apply request that triggered this event."
3. **`cancelled` (lines 517–528):**
   - Quote (19 words, lines 518–521):
     > "Sent if the compositor cancels the configuration because the state of an output changed and the client has outdated information"
   - Recovery (13 words, lines 523–524):
     > "The client can create a new configuration with a newer serial and try again."

In all three terminal events, the specification dictates:
> "Upon receiving this event, the client should destroy this object." (lines 501, 513, 526; 9 words).

The client sends `destroy` (lines 530–538), which discards any unapplied state and frees child head configuration objects.

---

## 4. Upstream Scope and Non-Goals Boundaries

The XML preamble establishes strict boundary fences directly relevant to milestone U5:

1. **Experimental Status (lines 32–33, 15 words):**
   > "The protocol described in this file is experimental and backward incompatible changes may be made."
2. **Configuration Purpose Fence (lines 66–67, 16 words):**
   > "The information obtained from this protocol should only be used for output configuration purposes."
3. **Non-Advertisement Fence (lines 68–70, 16 words):**
   > "This protocol is not designed to be a generic output property advertisement protocol for regular clients."
   *(Compositor clients desiring output information for window placement or UI scaling should use `wl_output` / `xdg-output` instead).*

---

## 5. Candidate SOURCES.md Registry Entry (for S047)

Proposed candidate row conforming to the 11-column `corpus/SOURCES.md` schema:

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S047 | wlr-protocols `unstable/wlr-output-management-unstable-v1.xml` — https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/bf4fc79abc359eea5a0edec0ac6d4a2b2955f82a/unstable/wlr-output-management-unstable-v1.xml | spec | A | Upstream protocol specification for `zwlr_output_manager_v1` and `zwlr_output_configuration_v1` (v4); experimental status, transaction test vs apply semantics | `zwlr_output_configuration_v1` :425-538 @ `master` bf4fc79 / a5028af (sha256 `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7`) | `test` validates without applying; `apply` mutates active configuration; both share succeeded/failed/cancelled terminal events; protocol is configuration-only, not generic property advertisement | queued | 2026-10-20 | on-release | corpus/knowledge/output-colour-boundaries-r14.md |

### Source Open Summary Table

- **Canonical URL:** `https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/bf4fc79abc359eea5a0edec0ac6d4a2b2955f82a/unstable/wlr-output-management-unstable-v1.xml`
- **Pinned Revisions:**
  - Pinned `master` HEAD commit: `bf4fc79abc359eea5a0edec0ac6d4a2b2955f82a` (committed 2026-03-09)
  - Pinned file-modifying commit: `a5028afbe4a1cf0daf020c4104c1565a09d6e58a` (committed 2025-07-02)
  - Blob SHA-256: `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7`
- **Access Date:** 2026-10-20
- **Tier Scope:** Tier A (Official upstream protocol XML specification).
- **Admission / Rejection:** Admit as candidate S047 for U5 protocol boundary knowledge.
- **Flip:** Was unopened lead / untracked frontier; now grounded to verified upstream `wlr-protocols` commits and exact quotes.

---

## 6. Judgement & Verification Status

- **Coverage (C1):** Sourced documentation boundary established for U5 output-management configuration transactions (`test` vs `apply`, shared terminal events). Upstream lack of release tags is documented.
- **Operability (C2):** Exact durable URLs, SHAs, line numbers, and quotes verified directly against official Git repository and verified package data.
- **Harm Watch:** No compositor modifications, no protocol client executions, no tests run, no test/apply feature behavior attributed to host.
- **Remaining Unknowns (`[UNK]`):** Host driver response to `test` requests; whether compositor fractional-scale rounding occurs on this hardware; physical multi-monitor KMS atomic modesetting execution.
- **Tooling Statement:** No tools installed or upgraded. Read-only git observation and package query only.
