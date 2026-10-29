source: [ref] (https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/a741f0ac5d655338a5100fc34bc8cec87d237346/unstable/wlr-output-management-unstable-v1.xml, manager/head/configuration descriptions and test/apply/events); [ref] (https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/staging/color-management/color-management-v1.xml, manager supported_* events, output/surface image descriptions, target_luminance); [ref] (.ufo/waves/round-13/w1/globals.json, historical interface/version advertisements); [ref] (https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/OutputManagement.cpp, COutputConfiguration setDisableHead/setTest and applyTestConfiguration)
verified-at: 2026-10-20; source-byte bindings .ufo/waves/round-14/evidence/{output,colour}-source-binding.txt; historical advertisement captured 2026-10-20T04:10:03Z, not refreshed this round
recheck: On owning protocol/compositor release, reopen the pinned XML and source digests; repeat only the sanitized inventory recipe in wayland-protocol-boundaries-r13.md if a fresh advertisement is needed. Feature execution requires separate operator authorization.
covers: U5

# Output-management transactions and colour descriptions are not display validation

This entry adds U5's **documented output-management/colour boundary route**, not complete output feature coverage. `[INF-docs]` means exact upstream semantics; `[OBS-history]` means the committed earlier point sample; `[UNK]` means behavior not exercised. Source rows are scoped authorities, not host certification.

## Decision table

| Question | Evidence that answers it | What remains unproved |
|---|---|---|
| Output management: what does a configuration test or apply reply mean? | `[INF-docs]` [ref] distinguishes the current-state serial, a proposed full head configuration, validation-only `test`, state-changing `apply`, and `succeeded`/`failed`/`cancelled`. | `[UNK]` This host's acceptance, requested-versus-actual state, hotplug race handling, rendering and persistence. |
| Colour management: which colour properties does the protocol describe? | `[INF-docs]` [ref] separates manager support events, an output's immutable image-description snapshot, a surface's preferred description and a client-set surface description. | `[UNK]` Actual supported feature events, ICC processing, tone mapping, HDR signal path, panel luminance and colour accuracy. |
| Does the intended feature actually work? | `[UNK]` Requires an authorized feature-specific observation, including the exact request, reply and resulting state or physical measurement as appropriate. | Upstream XML, matching interface versions and retained registry records alone cannot answer this. |

## Output management

[ref] is **wlroots/wlr-protocols**, not wayland-protocols. Its header calls this protocol experimental; do not apply [ref]'s wayland-protocols governance as its authority. At the pinned revision the manager interface is `zwlr_output_manager_v1`, interface version 4. The `_v1` name and interface version 4 are different version dimensions.

The manager describes heads, including disabled heads; head objects advertise properties and cannot directly change them. A head name must not be assumed to encode a DRM connector. The manager's `done(serial)` groups the current head/mode changes into a coherent state. `create_configuration(serial)` starts a proposed configuration tied to that state. Every head must be enabled/configured or disabled exactly once; omission and duplicate configuration are protocol errors.

| Operation or event | Documented meaning at [ref] | Verification boundary |
|---|---|---|
| `test` | Validates the proposed configuration without applying it. The XML explicitly says a later apply may still fail. | Not permission to run the request as a lane probe; not evidence of a display change. |
| `apply` | Attempts a new output configuration; the compositor may round unsupported fractional scale, so successful application need not exactly match the request. | State-changing and operator-owned. Read resulting state before claiming exact agreement. |
| `succeeded` | The compositor successfully **applied or tested**, depending on the request that preceded it. | The event name alone does not distinguish validation from application. |
| `failed` | The compositor rejected or could not apply the proposal; it should revert changes made by the corresponding apply request. | A documented rollback obligation is not observed rollback behavior. |
| `cancelled` | Output state changed and the client used outdated information; a newer serial can ground a new proposal. | Not equivalent to unsupported mode or a successful retry; no retry was attempted here. |

The manager description expressly limits this protocol's information to **output configuration purposes**, not generic regular-client output advertisement. This is not a replacement for every core/xdg-output information route. No output-management client was run in round 14.

### Tagged implementation safety caveat — not a runtime test

`[SRC]` [ref] is Hyprland source at `efb50993780079460b0cbed1363e2166a2de1d9f`,
not proof of binary/source equivalence or an observed live display change.
Its `COutputConfiguration::applyTestConfiguration(true)` logs that the
test is a stub and returns true; `setTest` then sends `succeeded`.
Its `setDisableHead` callback saves `enabled = false` and calls
`scheduleReload()` **before any later test/apply request**. The XML's
validation contract above must therefore not be read as assurance that
this tagged implementation validates a proposal or keeps transaction
construction free of state-changing work.

Treat the entire configuration-object/transaction path as mutation-class:
do not run a dry-run client or build a transaction on the assumption that
only `apply` can have side effects. The static discrepancy is a safety
reason to stop, not a claimed executed exploit or measured host failure.
The more extensive implementation walk in
`.ufo/waves/round-14/w1/SourceSafety.md` is advisory; only the specifically
opened [ref] callback/stub facts are admitted here.

[ref] is the owning protocol contract, not a claim about the exact XML
copy compiled into Hyprland. Matching advertised interface versions
cannot establish XML-text equality or implementation conformity.

[ref] also says binding the output manager advertises current heads.
Head events can contain identity and modes: “no explicit configuration
requests” does not mean “no identity received.” Never retain raw head
metadata merely because an observer made no state-changing request.

## Colour management

[ref] is `wayland-protocols` tag **1.49**, file `staging/color-management/color-management-v1.xml`; the XML itself says “currently in the testing phase.” We retain both the repository directory and that exact wording, without inventing an additional phase or treating it as stable. Its manager interface is `wp_color_manager_v1`, interface version 3. Neither the [ref] README's earlier commit nor the later [ref] governance commit is substituted for this file revision.

The tag's raw XML and installed `wayland-protocols 1.49-1` XML have the same measured SHA-256, `18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9`. This is source-file equality, not equivalence of the installed compositor binary to upstream source. Commands and observed results are in `.ufo/waves/round-14/evidence/colour-source-binding.txt`.
Tag 1.49 peels to commit `ee78491a237eaff9389a0ccf8680521d074407d3`;
`a8d65d7f121497ddd0d10f620f4284896ab80aff` is its tag object, not the
commit. The exact `git ls-remote` result is retained in
`.ufo/waves/round-14/evidence/colour-release-binding.txt`.

- Binding the manager yields separate `supported_intent`, `supported_feature`, `supported_tf_named`, `supported_primaries_named` events and a final `done`. A registry version is **not** that feature list. These events were not retained in [ref].
  In particular, `supported_tf_named` lists transfer functions supported
  with the parametric image-description creator; presence of PQ/HLG
  there would not by itself establish display-HDR capability.
- `get_output` creates a colour-management object associated with a `wl_output`; `get_image_description` captures its current image description. A later `image_description_changed` requires another description request if the client wants updated information; image descriptions are immutable. Removal of the output makes the output-colour object inert; the XML defines `no_output` and inadequate-version `low_version` failure cases.
- A surface's preferred image description is compositor feedback, not a physical display calibration certificate. `set_image_description` supplies the client's content encoding and rendering intent as double-buffered surface state applied with `wl_surface.commit`; it is **not** a monitor-mode or panel-HDR toggle. The client must provide content matching its declared description. No such request or test surface was created here.
- Crucially, `wp_image_description_info_v1.target_luminance` says its luminance range is theoretical and may not correspond to light emitted by an actual display. A metadata number cannot replace physical luminance/colour measurement.

[ref] raw XML SHA-256 is `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7`; the full revision and raw-byte counting command are in `.ufo/waves/round-14/evidence/output-source-binding.txt`. Element names above are exact XML anchors; transformed reader offsets are not substituted for raw-source locations.

## Historical advertisement and retained data

[ref]'s earlier capture advertises `zwlr_output_manager_v1` interface version 4 and `wp_color_manager_v1` interface version 3 for the recorded Hyprland 0.56.2 client/session. These match the **interface identities** discussed above. They are not fresh round-14 host measurements and do not prove either protocol's implementation conforms.

**Global records contain interface/version only; sanitized probe/session metadata is also retained.** The top-level capture also includes package/probe/compositor pins, a socket name and later non-atomic session-correlation metadata. Output identities, raw device paths, geometry and colourimetry detail blocks were excluded. The diagnostic used for [ref] did bind/query some interfaces ([ref] in the U4 note); “retained registry headers” never means “the diagnostic sent zero protocol requests.”

## Unexercised feature behavior

`[UNK]` Output test/apply, resulting monitor state, persistence across restart, hotplug race behavior, HDR rendering, display colour accuracy, gamma LUTs, Hyprland CTM, monitor-rule HDR/ICC settings and output-power behavior remain unexercised. No `wlr-randr`, output-management test/apply, surface colour request, screenshot, compositor reload or host-config write was run for this entry. This negative statement is scoped to round-14 executed work, recorded in the round lesson and evidence directory; it is not a claim that no other process used these features.

Safe use of this entry:

1. Pick the exact question in the decision table; identify the owning XML/revision before inferring semantics from a name.
2. For a historical advertisement claim, read [ref] directly, keeping its timestamp and client scope. For a current inventory, follow the U4 safe projection and preserve the diagnostic exit separately; do not persist raw output.
3. For transaction or colour semantics, reopen the exact [ref]/[ref] elements. Re-bind package/source digests if the installed source changes.
4. Stop at the documented/advertised boundary. Hand off any actual feature experiment to the operator with proposed action, expected reply, resulting-state/measurement criterion and rollback plan; the plan is not executed evidence.
5. Kernel, DRM/KMS and device diagnosis remain sibling-owned; report that boundary instead of expanding this compositor-craft note into hardware repair.

## Rejected candidates

- **A successful output test guarantees apply succeeds.** Reject: [ref] `test` explicitly denies that implication. Flip requires a stronger exact-scope guarantee, not the same successful-test event.
- **Output apply succeeded means every requested property matches exactly.** Reject: [ref] `apply` explicitly allows scale rounding. Flip requires actual property-by-property observed agreement for the named request.
- **An advertised colour manager proves working HDR or measured panel luminance.** Reject: [ref] lacks feature/colorimetry results and [ref]'s target luminance can be theoretical. Flip requires separately authorized end-to-end and, for physical claims, physical measurement.
- **[ref] governance makes wlr-output-management stable.** Reject: different owning project and [ref]'s experimental warning. Flip requires the owning protocol's exact revised authority.

These are explicit rejected inferences, not newly discovered failed host features. U6 input debugging and U7 Waybar module text remain outside this entry.
