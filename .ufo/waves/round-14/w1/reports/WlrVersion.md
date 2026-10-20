# WlrVersion — rendered report (mado-r14-w1)

Full findings: `.ufo/waves/round-14/w1/WlrVersion.md`. Read-only upstream repository discovery and package observation; no tests executed; no client connections to compositor.

## Findings

1. **Upstream wlr-protocols Tag Status — Zero Git Tags:**  
   The official `wlr-protocols` upstream Git repository (`https://gitlab.freedesktop.org/wlroots/wlr-protocols`) maintains **no git tags** (`git tag -l` and `git ls-remote --tags` yield empty). Downstream distributions track commit revisions (e.g. Arch Linux official `extra/wlr-protocols` package version `r112.a741f0a-1`, packaging commit `a741f0ac5d655338a5100fc34bc8cec87d237346`).

2. **Branch & Commit Pinned Revisions:**  
   - Default branch: `master`.
   - `master` HEAD SHA: `bf4fc79abc359eea5a0edec0ac6d4a2b2955f82a` (committed 2026-03-09T11:15:36-03:00).
   - Last commit touching `unstable/wlr-output-management-unstable-v1.xml`: `a5028afbe4a1cf0daf020c4104c1565a09d6e58a` (committed 2025-07-02T07:20:08Z / authored 2025-06-05T17:32:03+02:00, "output-management: refer to wl_output instead of xdg-output").
   - Blob SHA-256: `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7` (611 lines, 26,355 bytes). Byte-identical across `a5028af`, Arch package `a741f0a`, and `master` HEAD `bf4fc79`.

3. **Repository Disambiguation (`wlr-protocols` vs `wlroots`):**  
   Round 13 (`ReviewPhases.md` / `ScribeFrontier.md`) cited `cdd2c7e0064efee7fd398b2935923508b2fa9842` under repository `wlroots/wlroots`. That commit does not exist in `wlroots/wlr-protocols`. While the XML file contents are identical (`65b0f82a…`), the canonical source rows for `wlr-protocols` must cite `wlr-protocols` commits (`a5028af` or `bf4fc79`).

4. **Transaction Semantics: `test` versus `apply` Purpose:**  
   In `zwlr_output_configuration_v1` (lines 425–539):
   - **`apply` (lines 466–479, mutation):**  
     - Primary purpose quote (lines 467–468, 5 words): `"Apply the new output configuration."`
     - Caveat quote (lines 470–473, 20 words): `"In case the configuration is successfully applied, there is no guarantee that the new output state matches completely the requested configuration."`
   - **`test` (lines 481–494, read-only atomic validation):**  
     - Primary purpose quote (lines 482–484, 15 words): `"Test the new output configuration. The configuration won't be applied, but will only be validated."`
     - Caveat quote (lines 486–487, 13 words): `"Even if the compositor succeeds to test a configuration, applying it may fail."`
   - **Terminal events & atomic lifecycle (lines 496–538):**  
     - Both requests lock the configuration (`already_used` error for subsequent requests).
     - Compositor emits exactly one terminal event: `succeeded` (lines 497–499: `"Sent after the compositor has successfully applied the changes or tested them."`), `failed` (lines 508–510: `"Sent if the compositor rejects the changes or failed to apply them."`), or `cancelled` (lines 518–521: `"Sent if the compositor cancels the configuration because the state of an output changed and the client has outdated information"`).
     - Client must then destroy the object via `destroy` request (lines 530–538).

5. **Preamble Boundary Fences (Milestone U5):**  
   - Experimental: `"The protocol described in this file is experimental and backward incompatible changes may be made."` (lines 32–33, 15 words).
   - Configuration purpose only: `"The information obtained from this protocol should only be used for output configuration purposes."` (lines 66–67, 16 words).
   - Non-advertisement: `"This protocol is not designed to be a generic output property advertisement protocol for regular clients."` (lines 68–70, 16 words).

## Judgement

- **Coverage (C1):** Establishes the official upstream `wlr-protocols` source anchor, untagged revision reality, and transactional validation/mutation boundary for U5.
- **Operability (C2):** Provides exact reproducible URLs, git commit SHAs, line numbers, and located verbatim quotes for S047 admission without running tests.

## Gaps & Unknowns

- No live test or apply requests were executed against the compositor (`[UNK]`).
- Host driver KMS modesetting behavior upon `test` vs `apply` remains unexercised.

## Tooling

None installed or upgraded.
