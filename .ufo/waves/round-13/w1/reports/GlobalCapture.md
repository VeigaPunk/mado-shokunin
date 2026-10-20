# GlobalCapture report — round 13, w1

## Files changed

| path | role |
|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/globals.json` | new sanitized machine-readable host globals capture (assigned artifact) |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/GlobalCapture.md` | new draft: probe record, exact census, crosswalk, S041 candidate |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/reports/GlobalCapture.md` | this scoped report |

No shared source, gate, fixture, corpus or config file was modified. No commit or push.

## Behavior / result

- `wayland-info` was absent; `wayland-utils 1.3.0-1` was installed via
  `sudo pacman -S --needed --noconfirm wayland-utils` (pacman `extra`), after reading
  `/home/vgpnk/.omp/agent/RULES.md`. No partial upgrade was run. Tool record: wayland-utils
  1.3.0-1, pacman extra, reason = assigned read-only globals probe.
- Probe: `wayland-info`, rc 0, empty stderr, socket `wayland-1`; 72 global advertisements,
  71 distinct interfaces. A second run produced the identical set digest.
- Sanitized capture keeps only interface names/versions. All indented detail (output identity,
  colorimetry, device paths, dmabuf modifiers, seat name/capabilities, registry ids) is dropped;
  an identity-token grep over the artifact returns no matches.
- Compositor pin: Hyprland 0.56.2, tag `v0.56.2`, commit
  `efb50993780079460b0cbed1363e2166a2de1d9f`, dirty false (`hyprctl -j version`, rc 0) — the same
  tag commit S018 already covers for U1.
- Session binding (read-only, in memory): `hyprctl -j instances` rc 0 returned 1 instance; the
  current `HYPRLAND_INSTANCE_SIGNATURE` matched exactly one record and its `wl_socket` equals
  `WAYLAND_DISPLAY=wayland-1` (2026-10-20T04:18:27Z). Signature, pid and instance time were not
  printed or persisted; `globals.json.session_binding` holds `correlated: true`,
  `unique_signature_match: true`, `instance_count: 1`, `wl_socket: "wayland-1"`. The compositor
  association is therefore `[OBS]`, not `[INF]`.
- Upstream crosswalk against wayland-protocols pinned at `35d9638c…` (2026-10-12):
  5 stable, 28 staging advertisements (27 distinct), 12 unstable, 27 names absent from that tree.
  Three advertised versions lag pinned upstream (linux-dmabuf 5/6, tablet manager 1/2,
  text-input manager v3 1/2); none exceed it.
- Candidate S041 own-work row proposed with status `queued`; provisional file sha
  `ced47240…`, set sha `9569d02f…`; flip requires the w1 commit binding plus a U4 knowledge
  citation (QUALITY 7).

## Evidence retained

- Artifact: `.ufo/waves/round-13/w1/globals.json`, 72 advertisements; set sha256
  `9569d02fe2b04bf62079258b1d74f5d2ad8510c26ef0710a1a64c95f1a9becaa`; multiplicity
  `wp_drm_lease_device_v1@1 × 2`. Session binding fields in the same file:
  `correlated: true`, `unique_signature_match: true`, `instance_count: 1`, `wl_socket: "wayland-1"`,
  captured `2026-10-20T04:18:27Z`, `hyprctl -j instances` rc 0.
- Reproducible commands: `wayland-info` rc 0 twice; `sed` projection pipeline and
  `jq -r '.globals[] | "\(.interface)@\(.version)"' | sort | sha256sum` both returned the set
  digest at authoring time.
- Source open: wayland-protocols README at archive commit `35d9638c…`, README last-touch
  `3dac056d…`; 24-word quote at `README.md:69-71` (directory placement decides phase) and
  24-word quote at `README.md:61-62` (`z` is a legacy prefix). Tier A. Admitted only to fence
  `[INF-docs]` phase labels; rejected as host behavior; S005 row untouched.
- Raw stdout was ephemeral scratch only and was deleted after projection; no raw dump is retained
  (identity-bearing session material stays outside the lane). The set digest replays from
  `globals.json` alone.

## Risks

- Single host, single socket, one capture instant; the census is not a claim about other sessions.
- `wayland-info` 1.3.0 lists registry-driven globals but annotates only known extras; listing is
  complete, annotation depth is not.
- Naive set equality loses the duplicate DRM-lease global; compare as a multiset or consume the
  artifact's `multiplicity` field.
- Phase labels are upstream directory-placement inference; a global name with `z` prefix is not
  itself unstable (2 stable, 10 outside in this census).

## Blockers

None.

## Checks L1 should run once

```sh
jq -e '.global_count == 72 and .unique_interface_count == 71' .ufo/waves/round-13/w1/globals.json
jq -e '.session_binding.correlated == true and .session_binding.instance_count == 1 and .session_binding.wl_socket == "wayland-1"' .ufo/waves/round-13/w1/globals.json
jq -r '.globals[] | "\(.interface)@\(.version)"' .ufo/waves/round-13/w1/globals.json | sort | sha256sum
wayland-info | sed -n "s/^interface: '\([^']*\)', *version: *\([0-9]*\),.*/\1@\2/p" | sort | sha256sum
hyprctl -j instances | jq 'length'
git show <wave-commit>:.ufo/waves/round-13/w1/globals.json | sha256sum
```

Expected: both `jq -e` checks are `true`; both digests equal
`9569d02fe2b04bf62079258b1d74f5d2ad8510c26ef0710a1a64c95f1a9becaa`; `hyprctl -j instances` length
is `1`; the `git show` digest binds the work-window hash
`ced47240c2a1941bbbf1f125d9a1e41624cfeeb8218ab2a3a425eb335a08a949` only if the file is committed
byte-identical.
