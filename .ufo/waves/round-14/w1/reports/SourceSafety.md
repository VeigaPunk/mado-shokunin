# SourceSafety — scoped report (round 14, w1)

Full findings, pins, source opens and the recipe script are in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/SourceSafety.md`.

Pins:
- **Compositor:** Hyprland `v0.56.2` = `efb50993780079460b0cbed1363e2166a2de1d9f`.
- **wlr-output-management XML:** two copies.
  - Vendored in Hyprland: `890594ae…`.
  - Upstream wlr-protocols `bf4fc79a`: `65b0f82a…`, which equals the installed `/usr/share/wlr-protocols` copy.
- **colour-management XML:** `wayland-protocols 1.49`, `18a2678e…`, which equals the installed copy.
- **Client reference:** `wlr-randr v0.5.0` (`4e239ef2`), not installed.

All line anchors refer to these raw files.

## Findings

- **F1 HIGH: a "dry-run" can still disable a monitor.**
  - `OutputManagement.cpp:298-324` applies `disable_head` as soon as it arrives: it saves `enabled=false` and calls
    `scheduleReload()`. It does not wait for test or apply.
  - `MonitorRuleManager.cpp:46,54` then overrides the rule, and the monitor is disconnected on the next frame.
  - `wlr-randr --output X --off --dryrun` sends `disable_head` + `test` (`main.c:376-381,416-417`), so it turns off X and
    still gets `succeeded`.
  - It may persist after the client exits, because manager destroy schedules no reload `[INFERENCE]`.
  - Fix: treat any creation of a `zwlr_output_configuration_v1` object as a mutation.
- **F2 MED: `test` is a stub.** `OutputManagement.cpp:353` reads "TODO: STUB: applyTestConfiguration for test not
  implemented, returning true."
  - A `succeeded` reply therefore validates nothing.
  - It also writes a WARN line to the session log.
- **F3 MED: the XML is the contract, not the host's behavior.** This Hyprland never sends `cancelled`, never enforces
  `unconfigured_head`, and ignores the `serial` argument (`:22`).
  - The vendored XML differs from upstream in descriptions only; interface versions match.
  - Label the XML `[INF-docs]`, the pinned source `[SRC]`, and runtime behavior `[UNK]`.
  - OutputSpec reads the XML as host behavior; I messaged them.
- **F4 MED: binding the output manager alone delivers raw identity.** Binding `zwlr_output_manager_v1` sends name,
  description, make, model, serial (`:145`), physical size and the mode list, with no client request.
  - The proposed boundary between retained metadata and raw identity is tabulated in full.
  - That includes the R13-V1 wording: "global records contain interface/version only; sanitized probe/session metadata
    is also retained".
- **F5 MED: privilege scope.**
  - Globals are filtered only for sandboxed clients (`Compositor.cpp:263`). The output-management, gamma, CTM and power
    globals are not whitelisted for them; colour management is (`ProtocolManager.cpp:348-391`).
  - No permission type covers outputs or colour, and `enforce_permissions` defaults to false.
  - So any unsandboxed client can reconfigure outputs without a prompt.
  - If a sandboxed client's capture lacks a global, that is `[UNK]`, not proof the compositor doesn't support it.
- **F6 MED/LOW: binding some colour mutators has side effects.**
  - CTM: the first binder takes the manager and blocks `hyprsunset` (installed 0.4.0-3). When it is destroyed, every
    monitor resets to identity (`CTMControl.cpp:74-80,91-103`).
  - Gamma: each monitor has one exclusive control.
  - wayland-info 1.3.0 binds none of these.
- **F7 LOW: colour version claims.**
  - `wp_color_manager_v1@3` is gated by config: `ProtocolManager.cpp:235` advertises `PCMV1_2 ? 3 : 1`, and
    `experimental:wp_cm_1_2` defaults to true.
  - wayland-info binds it at v1 (`:2919-2920`). The `get_image_description` it sends is the output object's v1 request.
  - R13 note `:43` needs per-object wording.
  - OutputHost's version table was wrong (`set_custom_mode` is v1; the parametric creator is v1). OutputHost
    acknowledged and corrected both of its files.
- **F8 INFO: this seat's writes.**
  - Temporary source copies in `/tmp/srcsafety-r14/` are deleted, and the recipe's tempdir cleaned itself up. Both are
    confirmed absent.
  - Nothing was installed, and no Wayland client was run.

## Safe recheck recipe

The recipe is static only: it fetches the pinned sources into a `mktemp` directory that is removed on exit.

- **Output:** digests plus 13 boolean or value checks.
- **Run:** I ran it once as a read-only source observation. It exited 0 with `test_is_stub=true`,
  `disable_head_schedules_reload=true`, `cancelled_ever_sent=false`, `unconfigured_head_enforced=false`,
  `om_whitelisted_for_sandbox=false`, `cm_whitelisted_for_sandbox=true`, `vendored_equals_upstream_xml=false`,
  `installed_cm_equals_tag=true` and `installed_wlr_om_equals_upstream=true`.
- **Scope:** these values are presence checks from this one run, not semantic proof or cross-revision equality (R13-V2).
- **Failure:** a failed fetch exits non-zero and leaves the result `[UNK]`.

**Optional advertisement step:** reuse the R13 wayland-info header-only recipe unchanged, and also record the client's
sandbox context.

**Never run** as part of the recheck:
- `wlr-randr` in any form;
- kanshi or shikane;
- `hyprctl monitors`, `keyword monitor` or `reload`;
- any client that creates a configuration, gamma or power object, or binds the CTM manager;
- reading the session log.

## Tooling

Nothing was installed or upgraded. These read-only package queries were made: `pacman -Q`, and `pacman -Qi
wayland-utils`.
