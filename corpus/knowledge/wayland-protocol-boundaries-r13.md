source: S005 (wayland-protocols README, https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/3dac056d83ad8947eed6eb621f346e91da736efd/README.md §Protocol phases); S040 (GOVERNANCE §2, upstream 35d9638cf0c3f0bbf0c42996580a284f3d8ce564); S041 (.ufo/waves/round-13/w1/globals.json); S042 (https://wayland.freedesktop.org/extras.html §Compositor features, source revision 8923a19916635c21a3577b616f650a7e45d70fa9); S043 (installed Wayland core wayland.xml, wl_registry, Wayland 1.26.0); S046 (https://gitlab.freedesktop.org/wayland/wayland-utils/-/raw/1.3.0/wayland-info/wayland-info.c, global_handler and colour/output queries)
verified-at: 2026-10-20; host capture 2026-10-20T04:10:03Z; revision-bound round measurements in .ufo/waves/round-13/
recheck: On compositor, wayland-utils or protocol-source release; re-open pinned documents and repeat sanitized registry capture before reusing a host observation.
covers: U4

# Protocol phase is not a compositor capability verdict

This entry closes the **documented protocol-phase and advertised-global diagnostic route** of U4. It does not close protocol request behavior, output management/colour (U5), the kernel-input ladder (U6), or Waybar module text (U7). Labels: `[INF-docs]` upstream documented semantics; `[OBS]` sanitized host observation; `[UNK]` not exercised.

## The three questions to separate

| Question | Evidence route | What it does not establish |
|---|---|---|
| Which upstream development/compatibility phase applies to this exact protocol? | `[INF-docs]` Read its owning repository's XML, README and pinned release; S005/S040 define wayland-protocols phases. | An interface-name prefix alone does not classify every compositor-specific protocol. |
| Which interface/version does this compositor advertise to this client now? | `[OBS]` Sanitized `wayland-info` registry header capture, S041; S042 documents the discovery tool. | Successful feature requests, client negotiation, permissions, rendering or end-to-end behavior. |
| Does the intended feature actually work? | `[UNK]` Requires a separately authorized, feature-specific behavioral observation. | Neither upstream phase nor registry presence substitutes for that observation. |

## Phase and version decision table

`[INF-docs]` S005, README §Protocol phases / §Backward compatible protocol changes / §The staging phase / §The stable phase:

| Upstream category | Supported reading | Rejected shortcut |
|---|---|---|
| experimental | Actively iterated; no expectation of avoiding incompatible changes; implementations need active tracking. | "Merged upstream, therefore safe to treat as a frozen API." |
| staging | Ready for wider adoption; minimize incompatible changes. Backward-compatible additions bump the interface version; incompatible changes require a new protocol major version. | "Staging means stable and unchanged forever." |
| stable | Proven adequate; avoid incompatible changes. Promotion preserves major version, interface versions and names. | "Stable proves this host implements or correctly executes it." |
| deprecated | No more changes; replacement or undesirability is the documented reason to investigate. | "Old protocol disappears from every compositor immediately." |
| legacy unstable | The old categorization used the `z` prefix; upstream keeps an `unstable/` directory. | "Every `z*` interface is a current experimental wayland-protocols protocol." |
| outside wayland-protocols | Core and compositor/vendor-specific interfaces require their own owning-repository authority. | "Every advertised name must fit experimental/staging/stable." |

Keep **protocol major version**, **interface version**, and **package release** separate. A name ending `_v1` can advertise interface version 3; that is not protocol major version 3. S005's backward-compatible-change mechanism uses XML `version` and `since`. The host capture's `wp_color_manager_v1` / version 3 is an advertisement example, not a colour-management test.

`[INF-docs]` S040 documents namespace-specific governance and implementation/acknowledgment requirements. Governance controls admission and promotion of protocols, not runtime success on this desktop. Its rules are scoped to wayland-protocols; wlroots, Hyprland-specific and other repositories require their own authority. Do not infer Hyprland runtime support from a project's governance membership.

## Advertisement, binding and behavior

`[INF-docs]` S043, `wl_display.get_registry`, `wl_registry` description and `global`/`bind`/`global_remove`:

1. A registry object announces globals available to the client, with an interface and interface version. Globals may appear or disappear through hotplug or reconfiguration.
2. `wl_registry.bind` creates a handle to a named global. Advertisement and binding are different protocol events.
3. Feature behavior requires the applicable object's requests/events and compositor policy. A registry inventory does not exercise that contract.

S046's **upstream 1.3.0 diagnostic-client implementation binds advertised interfaces** through its global handlers and issues detail queries, including `get_xdg_output`, linux-dmabuf `get_default_feedback`, and colour-manager `get_output` / `get_image_description` / `get_information`. The `-i` option filters printing, not binding. This is source-grounded implementation behavior, not a claim of binary-source equivalence. The retained S041 data is only registry interface/version headers: output identity, device paths, human-readable seat names, geometry, colourimetry and numeric registry names were discarded. Do not describe the entire diagnostic execution as advertisement-only or as zero protocol requests. No input injection, output reconfiguration, lock request, screenshot, portal consent or compositor reload was requested.

## Host point sample

`[OBS]` S041 records Hyprland **0.56.2**, commit `efb50993780079460b0cbed1363e2166a2de1d9f`, read by `hyprctl -j version`; `wayland-info` returned 0 with no stderr. Installed diagnostic package: `wayland-utils 1.3.0-1`; installed Wayland package: `1.26.0-1` (link-time version unverified). These are distinct package/compositor pins. A later, non-atomic correlation at 04:18:27Z matched the unique signature-selected instance's `wl_socket` to `WAYLAND_DISPLAY`; only the matching socket and booleans were retained in `session_binding`, never the signature.

Selected observed pairs, directly from `.ufo/waves/round-13/w1/globals.json`:

| Interface | Advertised interface version | Retained in S041 |
|---|---|---|
| `wl_compositor` | 6 | Registry header only. |
| `xdg_wm_base` | 7 | Registry header only; no test window. |
| `zwlr_output_manager_v1` | 4 | Registry header only; no output changes. |
| `wp_color_manager_v1` | 3 | Registry header only; diagnostic detail queries were not retained; no HDR, renderer or display-path verdict. |

The duplicated `wp_drm_lease_device_v1` entries are retained in the raw sanitized list. Their multiplicity does not authorize an inference about monitor count or hardware topology. `global_count`, `unique_interface_count` and `set_sha256` are separately recorded by the capture; do not replace the object list with a deduplicated set when counting objects.

## Safe recheck checklist

- Name the target compositor/session without printing instance signatures or raw environment.
- Read the installed diagnostic tool's version/package; compare to the capture's pins.
- Run `wayland-info` through an allowlist projection retaining only interface/version header records. Never persist its unfiltered output: device/output details exceed this entry's boundary.
- Preserve the probe exit status independently of parser success. Failure leaves advertisement `[UNK]`, not "no protocols".
- Compare observed interfaces by name/version; keep multiplicity and identify the revision of any protocol XML used to classify phase.
- Keep the retained claim at advertisement. The diagnostic's detail queries above do not authorize an output-configuration, virtual-input, screen-capture or session-locking feature test.

Safe inventory recheck (raw output exists only in process memory; the
digest preserves duplicate advertisements):

```bash
python3 - <<'PY'
import hashlib, re, subprocess
p = subprocess.run(["wayland-info"], capture_output=True, text=True)
if p.returncode or p.stderr:
    raise SystemExit(f"advertisement UNKNOWN: exit={p.returncode} stderr_bytes={len(p.stderr.encode())}")
pairs = re.findall(r"^interface: '([A-Za-z0-9_]+)',\s+version:\s+([0-9]+),", p.stdout, re.M)
if not any(name == "wl_compositor" for name, _ in pairs):
    raise SystemExit("advertisement UNKNOWN: no wl_compositor header")
lines = sorted(f"{name}@{version}" for name, version in pairs)
digest = hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()
print(f"globals={len(lines)} interfaces={len(set(name for name, _ in pairs))} sha256={digest} exit={p.returncode}")
PY
```

The installed XML, not the unversioned HTML rendering, is S043's
versioned authority: SHA-256
`cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`
(rederive with `sha256sum /usr/share/wayland/wayland.xml`).
S042's website revision is from branch **main**, not the older master
branch. GOVERNANCE at the selected main revision differs from release
1.49 only in a spelling correction; no governance threshold is inferred
from the installed package alone.

## Rejected

- **Staging means stable ABI forever.** Rejected by S005's distinct staging and stable policy. Flip: an exact protocol's newer pinned authority explicitly supplies the stronger guarantee.
- **An advertised output/color manager proves working monitor reconfiguration or HDR.** Rejected: S041 observes discovery, not the action or rendering path. Flip: a separately authorized end-to-end measurement of that exact feature.
- **A global's name/version encodes its development phase.** Rejected: S005 categories are repository policy, not the registry wire fields in S043. Flip: an exact owning-repository mapping at the cited revision, not a prefix guess.

## Limits

The capture is time-bound and client/session-specific; a future absence is not a historical falsification. No source XML inventory of every advertised extension was performed. Phase-classification coverage is the decision method, not a per-interface stable/staging assignment. No desktop configuration was written. Kernel/libinput diagnosis, device permission changes and full output/colour validation remain outside this admitted entry.
