# SourceSafety — U5 protocol request boundaries (round 14, w1)

Seat: `MadoR14.SourceSafety` (sentinel, leaf). Opened: 2026-10-20. Axes: **coverage** (C1, U5 boundary ground) and
**operability** (a recheck recipe that is safe to run).

Labels: `[SRC]` read in pinned implementation source; `[INF-docs]` protocol XML text; `[OBS]` read-only package or source
observation made in this seat; `[INFERENCE]` derived, not observed; `[UNK]` not exercised.

I issued no Wayland requests, ran no Wayland client, made no compositor mutations, and read no session logs or output
identities. My only observations were package queries, protocol XML digests, and fetches of public upstream source.

## Pins

| Artifact | Canonical URL / path | Revision | SHA-256 (this run) |
|---|---|---|---|
| Hyprland v0.56.2 (S041 compositor pin) | https://github.com/hyprwm/Hyprland | tag `v0.56.2` = `efb50993780079460b0cbed1363e2166a2de1d9f` (`git ls-remote`) | see per-file below |
| `src/protocols/OutputManagement.cpp` | `…/Hyprland/efb5099…/src/protocols/OutputManagement.cpp` | efb5099 | `148f12d73ced4e045bc864ebc3cc5022e3681b82bbec9936f2cd8b32d0bbd588` |
| `src/managers/ProtocolManager.cpp` | same tree | efb5099 | `b4a91b2647f3bb80dd28b41377465916c00ba84da9f3494370bd90302b9e8622` |
| `src/Compositor.cpp` | same tree | efb5099 | `74833ecbf0e2b6f8ad84345ac0716a3295a0e347420a188be0ab4f6a684af7c0` |
| `src/config/shared/monitor/MonitorRuleManager.cpp` | same tree | efb5099 | `17d46685c2623657f52e71b22a033c0a798cf3903f7bbeb64ceebce87527f016` |
| `src/protocols/CTMControl.cpp` | same tree | efb5099 | `c7c56ba6c38b2f32054a86bb46bd567cde81e4bfe54eb3cffae582d19207896c` |
| `src/protocols/GammaControl.cpp` | same tree | efb5099 | `aa00dfdcdfdda875bef25e5cdbfe1ddca110812a8d2034fccd9986822cfde7b0` |
| `src/protocols/OutputPower.cpp` | same tree | efb5099 | `b6a1fcdbadc5b1b91beeba92bd078b4d8cd17868d2b47ef828dc12d4ff6b9109` |
| `src/protocols/ColorManagement.cpp` | same tree | efb5099 | `38599f2888953c34d4b67ffd20ac4ff5d20589375c8c571859aa0b8c0e96ad7b` |
| `src/managers/permissions/DynamicPermissionManager.hpp` | same tree | efb5099 | `8dcf116e4261f33aeaad5d8b028b90e22e7ab0445135f08e00ce78432c76005a` |
| `src/config/values/ConfigValues.cpp` | same tree | efb5099 | `a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754` |
| Vendored `protocols/wlr-output-management-unstable-v1.xml` | same tree | efb5099 | `890594ae68d47a441d47f34497e8e515f88de452b04615487ce97683c03ea9e1` |
| Upstream wlr-output-management XML | https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/bf4fc79abc359eea5a0edec0ac6d4a2b2955f82a/unstable/wlr-output-management-unstable-v1.xml | `bf4fc79a` (main HEAD, `git ls-remote` 2026-10-20) | `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7`; equals installed `/usr/share/wlr-protocols/…` (`cmp` true) |
| colour-management-v1 XML | https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/staging/color-management/color-management-v1.xml | tag `1.49` (peeled `ee78491a237eaff9389a0ccf8680521d074407d3`) | `18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9`; equals installed `wayland-protocols 1.49-1` |
| wlr-randr `main.c` (client reference; **not installed**) | https://gitlab.freedesktop.org/emersion/wlr-randr/-/raw/v0.5.0/main.c | tag `v0.5.0` = `4e239ef2317235d35b2693a55efadc23153a037a` | `b63a7c156cfbec73e3d6b3c6cd41a63862073eb0e3a12b093e694702a3c4df30` |
| wayland-info `wayland-info.c` (S046) | https://gitlab.freedesktop.org/wayland/wayland-utils/-/raw/1.3.0/wayland-info/wayland-info.c | tag 1.3.0 (S046: `d01edd68`) | `fcdc6c09d8111c8bcec407299be9ef582105c8ff954ebf9b57fa25b5e86c46a6` |

Installed package observations `[OBS]` (`pacman -Q`): `hyprland 0.56.2-2`, `wayland-protocols 1.49-1`,
`wayland-utils 1.3.0-1`, `hyprsunset 0.4.0-3`. Not installed: `wlr-randr`, `kanshi`, `wlsunset`, `gammastep`, `shikane`.
At 02:42 local `wlr-protocols` was absent. Seat OutputSpec later recorded installing `wlr-protocols r112.a741f0a-1`.
The installed file now matches upstream `bf4fc79a` byte for byte.

Line numbers below are the raw fetched files at the revisions above.

## Findings

### F1 — HIGH: on Hyprland v0.56.2, a "dry-run" output configuration can still disable a monitor

- **Evidence `[SRC]`, `OutputManagement.cpp`:**
  - `:298-324` `setDisableHead`: copies the manager's saved state and sets `newState.enabled = false`, calls
    `Config::monitorRuleMgr()->scheduleReload()` (`:321`), then stores the state in `m_owner->m_monitorStates[...]`.
    This happens as soon as the request arrives, not on `apply`. The `enable_head` handler is different: it logs
    "For now, doing nothing. Waiting for apply()".
  - `MonitorRuleManager.cpp:44-54` overrides `rule.m_disabled = !CONFIG->enabled`, using
    `PROTO::outputManagement->getOutputStateFor(PMONITOR)`.
  - `:25-29` handles the scheduled reload on the next render pre-check: `ensureMonitorStatus()` calls `onDisconnect()`
    on any monitor whose rule is now disabled.
- **Client sequence `[SRC]`, `wlr-randr main.c@v0.5.0`:**
  - `:371-381` creates a configuration and sends `disable_head` for every head whose state is not enabled.
  - `:416-417` sends `test` instead of `apply` when `--dryrun` is set.
- **Exploit path:** `wlr-randr --output <head> --off --dryrun` sends `disable_head(head)` and then `test`. The head is
  disconnected on the next frame, and the client receives `succeeded` (see F2).
  - A sequence without `--off` and with no disabled heads does not trigger this path: `enable_head` is deferred.
- **Persistence `[INFERENCE]`:** the saved state lives in the manager object. `destroyResource(COutputManager*)` only
  erases the manager and does not schedule a reload. The monitor can therefore stay off until some later trigger
  re-evaluates rules, such as a hotplug, a config reload or another manager's apply. I did not observe this.
- **Impact:** loss of a display from a request the user believed was read-only. It is also a contract violation
  ("No compositor mutations").
- **Smallest remediation:** the U5 entry and every recipe must classify **any** `zwlr_output_configuration_v1` creation
  as mutation class, whatever terminal request follows. `--dryrun` is not a safe probe on this pin.
  Flip: a later pinned Hyprland revision whose `disable_head` handler defers state until `apply`.

### F2 — MEDIUM: at this pin, `test` succeeding proves nothing

- **Evidence `[SRC]`:** `OutputManagement.cpp:326-333` replies `succeeded` when `applyTestConfiguration(true)` returns
  true. `:351-355` returns true without validating:
  `"TODO: STUB: applyTestConfiguration for test not implemented, returning true."`
- **Spec `[INF-docs]`:** the vendored XML at `:471-481` says test "won't be applied, but will only be validated."
- **Impact:** a claim that a configuration was "validated by test" is fabricated readiness on Hyprland 0.56.2. The test
  request also writes a WARN line to the compositor session log, which is a side effect on a log this lane must not read.
- **Remediation:** the U5 entry should state that a `test` result at efb5099 carries no validation evidence. It should
  reject "test succeeded ⇒ apply would work". Flip: a later pin where `applyTestConfiguration(true)` performs a real
  validation.

### F3 — MEDIUM: the protocol XML describes a contract; the compositor source shows how this host behaves

- **Evidence `[OBS]` (recipe below):**
  - Over all of `OutputManagement.cpp`: `cancelled_ever_sent=false` and `unconfigured_head_enforced=false`.
  - The `serial` argument of `create_configuration` (`:22`) is never used.
- **Contrast with the XML:**
  - It makes omitting a head a protocol error (`:421`).
  - It sends `cancelled` on outdated serials.
  - It makes requests after test/apply `already_used` errors.
- **Text divergence:** the vendored copy (`890594ae…`) differs from upstream wlr-protocols (`65b0f82a…`). The
  differences are description-only (wl_output vs xdg-output naming, and once-per-object wording). Interface versions are
  the same (manager/head/configuration 4, mode 3).
- **Rule for the U5 entry:**

  | Evidence | Label | What it licenses |
  |---|---|---|
  | Reading the XML | `[INF-docs]` | The upstream contract. |
  | Reading the compositor implementation at its pin | `[SRC]` | What the host would do. |
  | Neither of the above | `[UNK]` | Runtime behavior; that needs a separately authorized feature test, which this lane does not run. |

- **Peer impact:** `OutputSpec.md` §2.2, quote #4 "Teaches", §2.4 and flip #1 read the XML as host behavior. I messaged
  the seat.

### F4 — MEDIUM: keeping metadata is not the same as receiving raw identity; binding alone delivers identity

- **Evidence `[SRC]`:**
  - `OutputManagement.cpp`: the manager constructor sends every head right after bind.
  - `sendAllData` sends name, description, physical size, enabled state, position, transform and scale. It also sends
    make and model, plus serial number (`:145`, version ≥ 2), adaptive sync, and the full mode list.
  - The compositor DEBUG-logs `" | sending output head for {}"` with the monitor name.
- **Spec `[INF-docs]`:** the XML says serial and make "allow clients to recognize heads from previous sessions". It also
  says the protocol "is not designed to be a generic output property advertisement protocol for regular clients".
- **Consequence:** a "list only, no requests" client still receives raw identity. That includes `wlr-randr` with no
  arguments, which prints it, and `--json`. "Zero requests" must never be written as "zero identity".
- **Proposed retention boundary for the U5 entry:**

  | Retain (metadata) | Never retain (raw identity) |
  |---|---|
  | Interface name and advertised version; request/event names and `since` from pinned XML; file digests; package versions; booleans from static source checks; counts the capture actually measured | Head/connector name, description, make, model, serial, physical size, mode list, position, scale, transform, adaptive-sync state |
  | Sanitized probe/tool/compositor/session-binding fields already in S041 (R13-V1 wording: "global records contain interface/version only; sanitized probe/session metadata is also retained") | Colourimetry from image-description info (primaries, luminances, target volume), ICC fds/bytes, EDID-derived values `[INFERENCE: derivation not traced]` |

### F5 — MEDIUM: privilege scope — no prompt for output or colour mutators; filtering applies only to sandboxed clients

- **Evidence `[SRC]`:**
  - `Compositor.cpp:262-267,283`: the global filter returns true unless `isClientSandboxed(client)`. Only
    security-context clients are filtered.
  - `ProtocolManager.cpp:348-391`: `ALLOWED_WHITELIST` includes `PROTO::colorManagement` but not output management,
    gamma, CTM or output power. `om_whitelisted_for_sandbox=false` and `cm_whitelisted_for_sandbox=true`.
  - `DynamicPermissionManager.hpp:16-23`: the permission types are screencopy, plugin, keyboard, cursor_pos and
    input_capture. None covers outputs or colour.
  - `ConfigValues.cpp:620`: `ecosystem:enforce_permissions` defaults to false.
- **Impact:**
  1. Any unsandboxed local client can reconfigure outputs (F1), set gamma or CTM, or switch DPMS without a prompt.
  2. A capture from a sandboxed client would omit `zwlr_output_manager_v1` and the other mutators. That gap comes from
     privilege scope, not missing support. S041 shows `zwlr_output_manager_v1@4`, so its client was not sandboxed
     `[INFERENCE]`.
- **Remediation:** the recheck records the client sandbox context. It treats absence as `[UNK]`, never as unsupported.

### F6 — MEDIUM/LOW: colour mutators — binding alone has effects on two of them

- **CTM `[SRC]`, `CTMControl.cpp`:**
  - `:91-103`: the first unblocked binder becomes the active manager; later binders are `block()`ed.
  - `:50-63`: a `commit` resets every monitor without a pending matrix to identity.
  - `:74-80`: destroying an unblocked resource resets **all** monitors to identity.
  - Exploit path: a "bind every advertised global" probe that starts before `hyprsunset` (installed 0.4.0-3) holds the
    manager takes the manager. Night-light is blocked for the probe's lifetime, and the probe's exit resets the CTM.
- **Gamma `[SRC]`, `GammaControl.cpp`:**
  - `:29-33`: one control per monitor, so holding one blocks other gamma tools.
  - `:49-121`: `set_gamma` changes the LUT.
  - `:129-135`: the destructor resets the LUT.
- **Output power `[SRC]`, `OutputPower.cpp:13`:** `set_mode` changes DPMS.
- **Colour manager `[SRC]`, `ColorManagement.cpp`:**
  - `get_output` → `get_image_description` → `get_information` is read-only, but it returns colourimetry (F4).
  - `get_surface` / `set_image_description` affects only the client's own surface, which is still a feature exercise.
- **Note:** `wayland-info` 1.3.0 binds none of these (no `zwlr_output_manager`, `zwlr_gamma`, `hyprland_ctm` or
  `zwlr_output_power` bind in its source). Its colour path is limited to the request chain above.

### F7 — LOW: advertised colour version depends on config; R13 wording is imprecise

- **Version source `[SRC]`:**
  - `ProtocolManager.cpp:235` advertises `*PCMV1_2 ? 3 : 1`.
  - The global exists only when `render:cm_enabled` is set (`ConfigValues.cpp:567`, default true).
  - `experimental:wp_cm_1_2` defaults to true (`:717`).
  - So S041's `wp_color_manager_v1@3` reflects compositor configuration, not just the protocol revision.
- **What wayland-info used `[SRC]`:** it binds the colour manager at **version 1** (`wayland-info.c:2919-2920`). The
  `get_image_description` it sends is `wp_color_management_output_v1`'s v1 request (`:2750`), not the manager's
  `since="2"` request (XML `:587`).
- **Correction to R13 `wayland-protocol-boundaries-r13.md:43`:** it reads "colour-manager `get_output` /
  `get_image_description` / `get_information`". It should name each object.
- **Correction to OutputHost:** its version table is wrong against the XML.
  - `set_custom_mode` has no `since`, so it is v1. Output manager v4 adds only adaptive sync.
  - Colour v2 adds `get_image_description`, `ready2` and `preferred_changed2`. v3 adds `create_windows_bt2100`. The
    parametric creator is v1.
  - I messaged the seat.

### F8 — INFO: what this seat wrote

- **Temporary source copies:** public upstream sources went to `/tmp/srcsafety-r14/`, which I deleted before finishing.
  The recipe's own `mktemp` directory cleaned itself up (`glob('/tmp/mado-u5-static.*')` → `[]`).
- **Retained data:** none.
- **Other writes:** none outside this file and `reports/SourceSafety.md`.
- **Installs:** none.

## Source opens (all 2026-10-20)

| # | Source (URL @ revision) | Tier / scope | Located quote (≤25 words) | Verdict + flip |
|---|---|---|---|---|
| 1 | Hyprland `src/protocols/OutputManagement.cpp` @ efb5099, `:353` | A code; host-pin output-management semantics | "TODO: STUB: applyTestConfiguration for test not implemented, returning true." | **Admit** for F1/F2 `[SRC]`. Flip: later pin implements test or defers disable. |
| 2 | Same file, `:298-324` | A code; eager disable state | "Config::monitorRuleMgr()->scheduleReload();" (inside `setDisableHead`, `:321`) | **Admit** (F1). Flip: same as #1. |
| 3 | Hyprland `src/config/shared/monitor/MonitorRuleManager.cpp` @ efb5099, `:46,54` | A code; wlr state overrides rules | "const auto CONFIG = PROTO::outputManagement->getOutputStateFor(PMONITOR);" | **Admit** (F1). Flip: consumer removed. |
| 4 | Hyprland `src/managers/ProtocolManager.cpp` @ efb5099, `:235,348-391` | A code; sandbox visibility and colour version gate | "this is a static whitelist of allowed protocols," | **Admit** (F5/F7). Flip: whitelist changes. |
| 5 | Hyprland `src/Compositor.cpp` @ efb5099, `:263` | A code; filter applies to sandboxed clients only | "if (!PROTO::securityContext->isClientSandboxed(client))" | **Admit** (F5). |
| 6 | Hyprland `DynamicPermissionManager.hpp` @ efb5099, `:16-23` | A code; permission types | "PERMISSION_TYPE_SCREENCOPY, PERMISSION_TYPE_PLUGIN, PERMISSION_TYPE_KEYBOARD," | **Admit** (F5): no output/colour permission. Flip: an output-config permission type appears. |
| 7 | Hyprland `src/protocols/CTMControl.cpp` @ efb5099, `:74-80` | A code; CTM bind/destroy side effects | "PROTO::ctm->setCTM(m, Mat3x3::identity());" (destructor of an unblocked resource) | **Admit** (F6). |
| 8 | Hyprland `src/protocols/GammaControl.cpp` @ efb5099, `:133` | A code; gamma reset/exclusivity | "reset the LUT if the client dies for whatever reason and doesn't unset the gamma" | **Admit** (F6). |
| 9 | Hyprland vendored `protocols/wlr-output-management-unstable-v1.xml` @ efb5099, `:471-475` | A spec; contract text only | "Test the new output configuration. The configuration won't be applied, but will only be validated." | **Admit** `[INF-docs]`. **Reject** as proof of host behavior (F2/F3). Flip: implementation evidence at the same pin. |
| 10 | wlr-protocols upstream XML @ bf4fc79a | A spec; upstream text | "This protocol is not designed to be a generic output property advertisement protocol for regular clients." | **Admit** (F4). Note the vendored copy differs in descriptions. |
| 11 | wlr-randr `main.c` @ v0.5.0 (4e239ef2), `:376-381,416-419` | A code; client request sequence (not installed on host) | "if (dry_run) { zwlr_output_configuration_v1_test(config); } else { zwlr_output_configuration_v1_apply(config); }" | **Admit** (F1 exploit path). **Reject** as a safe probe. Flip: none at this compositor pin. |
| 12 | wayland-info.c @ 1.3.0, `:2919-2920,:2750` | A code; diagnostic bind version | "color->manager = wl_registry_bind(info->registry, id, &wp_color_manager_v1_interface, 1);" | **Admit** (F7). |
| 13 | Hyprland `src/config/values/ConfigValues.cpp` @ efb5099, `:717` | A code; default config | "\"experimental:wp_cm_1_2\", \"Allow wp-cm-v1 version 2\", true" | **Admit** (F7). Flip: default changes or host config differs (host config not read). |
| 14 | wayland-protocols color-management-v1.xml @ 1.49, `:601` | A spec; version additions | "<request name=\"create_windows_bt2100\" since=\"3\">" | **Admit** (F7). |

## Safe recheck recipe (static only; no Wayland connection)

This recipe makes no Wayland connection and no compositor requests, reads no logs, and creates no identity-bearing
output. It fetches pinned public sources into a self-cleaning temporary directory and prints digests and booleans.

I ran it once in this seat as a read-only source observation. The exit status was 0. The observed values are reproduced
below the script.

```bash
set -euo pipefail
HYPR=efb50993780079460b0cbed1363e2166a2de1d9f   # v0.56.2 (S041 pin)
WLRP=bf4fc79abc359eea5a0edec0ac6d4a2b2955f82a   # wlr-protocols main, opened 2026-10-20
WPT=1.49                                        # wayland-protocols tag (peeled ee78491a)
T=$(mktemp -d /tmp/mado-u5-static.XXXXXX); trap 'rm -rf -- "$T"' EXIT
gh=https://raw.githubusercontent.com/hyprwm/Hyprland/$HYPR
fetch(){ curl -fsSL --max-time 30 "$1" -o "$T/$2"; }
fetch "$gh/src/protocols/OutputManagement.cpp" om.cpp
fetch "$gh/src/managers/ProtocolManager.cpp" pm.cpp
fetch "$gh/src/Compositor.cpp" comp.cpp
fetch "$gh/src/config/shared/monitor/MonitorRuleManager.cpp" mrm.cpp
fetch "$gh/src/protocols/CTMControl.cpp" ctm.cpp
fetch "$gh/protocols/wlr-output-management-unstable-v1.xml" om-vendored.xml
fetch "https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/$WLRP/unstable/wlr-output-management-unstable-v1.xml" om-upstream.xml
fetch "https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/$WPT/staging/color-management/color-management-v1.xml" cm.xml
( cd "$T" && sha256sum om.cpp pm.cpp comp.cpp mrm.cpp ctm.cpp om-vendored.xml om-upstream.xml cm.xml )
b(){ if "$@" >/dev/null 2>&1; then echo true; else echo false; fi; }
echo "test_is_stub=$(b grep -q 'TODO: STUB: applyTestConfiguration for test not implemented, returning true' "$T/om.cpp")"
echo "disable_head_schedules_reload=$(b awk '/setDisableHead/{f=1} f&&/scheduleReload/{found=1; exit} f&&/setTest/{exit} END{exit !found}' "$T/om.cpp")"
echo "cancelled_ever_sent=$(b grep -q 'sendCancelled' "$T/om.cpp")"
echo "unconfigured_head_enforced=$(b grep -q 'UNCONFIGURED_HEAD' "$T/om.cpp")"
echo "rule_manager_consumes_wlr_state=$(b grep -q 'getOutputStateFor' "$T/mrm.cpp")"
echo "global_filter_sandbox_only=$(b grep -q 'isClientSandboxed(client)' "$T/comp.cpp")"
echo "cm_whitelisted_for_sandbox=$(b grep -q 'PROTO::colorManagement ? PROTO::colorManagement->getGlobal()' "$T/pm.cpp")"
echo "om_whitelisted_for_sandbox=$(b grep -q 'PROTO::outputManagement->getGlobal()' <(sed -n '/ALLOWED_WHITELIST/,/};/p' "$T/pm.cpp"))"
echo "ctm_unblocked_destroy_resets_identity=$(b grep -q 'setCTM(m, Mat3x3::identity())' "$T/ctm.cpp")"
echo "cm_version_gate=$(grep -o 'PCMV1_2 ? 3 : 1' "$T/pm.cpp" || echo absent)"
echo "vendored_equals_upstream_xml=$(b cmp -s "$T/om-vendored.xml" "$T/om-upstream.xml")"
echo "installed_cm_equals_tag=$(b cmp -s "$T/cm.xml" /usr/share/wayland-protocols/staging/color-management/color-management-v1.xml)"
x=/usr/share/wlr-protocols/unstable/wlr-output-management-unstable-v1.xml
[ -r "$x" ] && echo "installed_wlr_om_equals_upstream=$(b cmp -s "$T/om-upstream.xml" "$x")" || echo installed_wlr_om=absent
pacman -Q hyprland wayland-protocols wayland-utils 2>&1 || true
```

Observed `[OBS]` (exit 0; digests as in § Pins):

```text
test_is_stub=true
disable_head_schedules_reload=true
cancelled_ever_sent=false
unconfigured_head_enforced=false
rule_manager_consumes_wlr_state=true
global_filter_sandbox_only=true
cm_whitelisted_for_sandbox=true
om_whitelisted_for_sandbox=false
ctm_unblocked_destroy_resets_identity=true
cm_version_gate=PCMV1_2 ? 3 : 1
vendored_equals_upstream_xml=false
installed_cm_equals_tag=true
installed_wlr_om_equals_upstream=true
hyprland 0.56.2-2
wayland-protocols 1.49-1
wayland-utils 1.3.0-1
```

**Limits of these checks:**
- Each boolean is a string-presence test against pinned source, a measurement within this run. It is not a semantic
  proof or a claim that the outputs are equal across revisions (R13-V2).
- Network fetch failure makes the script exit non-zero under `set -e`. Treat that as `[UNK]`, never as false.
- The sandbox/whitelist grep depends on source layout. Re-anchor on any Hyprland upgrade before reusing it.

**Advertisement step (optional; only if separately authorized for this round).** Reuse the R13 `wayland-info` recipe
(`wayland-protocol-boundaries-r13.md:69-85`) unchanged:
- It binds `wl_output`, `xdg_output` and the colour manager at v1, and runs the output colour read chain (F6/F7).
- It retains only `interface@version` headers.
- Also record whether the client was sandboxed (F5).

**Never run as part of a U5 recheck** (each one either mutates or delivers raw identity):
- `wlr-randr` in any form, including no-args, `--json` and `--dryrun` (F1/F4).
- `kanshi`, `shikane`, `nwg-displays`, `wdisplays`.
- `hyprctl monitors` (make/model/serial), `hyprctl keyword monitor`, `hyprctl reload`.
- Any client that creates a `zwlr_output_configuration_v1`, a `zwlr_gamma_control_v1`, or a `zwlr_output_power_v1`
  object, or that binds `hyprland_ctm_control_manager_v1` (F6).
- `hyprsunset` start/stop.
- Reading `$XDG_RUNTIME_DIR/hypr/*/hyprland.log`. Binding and test requests write monitor names into it (F2/F4).

## Proposed U5 entry wording (for the knowledge seat; not written by me)

- "At Hyprland v0.56.2 (efb5099), `zwlr_output_configuration_v1.test` always replies `succeeded` without validation.
  `disable_head` takes effect before test or apply. A dry-run is therefore neither validation nor mutation-free.
  `[SRC]`; runtime `[UNK]`."
- "Binding `zwlr_output_manager_v1` delivers head name, description, make, model, serial and the mode list with no
  client request. Only interface/version records and sanitized probe metadata are retained."
- "Advertised `wp_color_manager_v1@3` reflects default config (`render:cm_enabled`, `experimental:wp_cm_1_2`), not
  exercised v2/v3 requests. HDR and colourimetry correctness stay `[UNK]`."
