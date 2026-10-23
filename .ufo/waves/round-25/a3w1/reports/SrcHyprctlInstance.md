# SrcHyprctlInstance — pinned hyprctl client source

## Findings

Opened Hyprland `hyprctl/src/main.cpp` at commit `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2). The pinned repository tree lists `hyprctl/src/main.cpp`; the raw source was fetched and retained at the artifact path below.

- `-i` and `--instance` consume the next argument. If it contains `_`, the client treats it as an instance signature directly. Otherwise it must pass the numeric check and is used as a zero-based index into the instance list; a negative or out-of-range index returns `no such instance`. The list is sorted by instance timestamp ascending before indexing. With no override, selection falls back to `HYPRLAND_INSTANCE_SIGNATURE` (lines 427-435, 493-520; sorting at 159).
- `instances` is handled before instance selection and is explicitly marked independent of `HYPRLAND_INSTANCE_SIGNATURE` (482-486). The listing scans the runtime `hypr` directory for directories with a parseable `hyprland.lock`: its first line is the PID and second line is the Wayland socket. It rejects malformed records, removes entries whose PID is gone (`ESRCH`), and sorts by timestamp. Text and JSON outputs include the instance ID/signature, timestamp, PID, and Wayland socket (100-161, 351-379).
- The runtime directory is `$XDG_RUNTIME_DIR/hypr`; when `XDG_RUNTIME_DIR` is absent it falls back to `/run/user/<uid>/hypr` (75-90). For the ordinary IPC request path, `request()` constructs `<runtime-dir>/<instance-signature>/.socket.sock` and connects to that Unix socket (222-235). Unhandled ordinary requests, including the normal command route, call `request()` (577-579).
- Thus the pinned client source grounds how `hyprctl -i <instance> binds -j` selects a target and derives its IPC socket. This is source evidence only: no hyprctl command, counter oracle, nested compositor, or compositor behavior was executed here.

## Located quotes

Each quote below was checked against the fetched bytes by Python after collapsing whitespace; all four checks returned `True`.

- `hyprctl/src/main.cpp:89` — “`return std::string{XDG} + "/hypr";`” This makes the XDG runtime directory the parent of the compositor-instance directories.
- `hyprctl/src/main.cpp:157` — “`std::erase_if(result, [](const auto& el) { return kill(el.pid, 0) != 0 && errno == ESRCH; });`” This removes dead-process entries from the instance list used for numeric selection.
- `hyprctl/src/main.cpp:510` — “`instanceSignature = INSTANCES[INSTANCENO].id;`” This maps a numeric `-i` selector to the selected instance directory ID/signature.
- `hyprctl/src/main.cpp:230` — “`std::string socketPath = getRuntimeDir() + "/" + instanceSignature + "/.socket.sock";`” This identifies the Unix IPC endpoint used after instance selection.

## SOURCES draft row

| S? | Hyprland v0.56.2 hyprctl client — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/hyprctl/src/main.cpp | code | A | CLI instance selection, instance inventory, and IPC socket path for the C1 oracle readback | hyprctl/src/main.cpp:81-90,100-161,222-235,351-379,427-520,577-579 @ efb50993780079460b0cbed1363e2166a2de1d9f; sha256:f6b0d1fcfc6695194c70964250591a35ffe90274309303d8f5fd0ac6f8c1c93f; 17168 B | Shows instance discovery and PID filtering, signature or numeric `-i` selection, environment fallback, and runtime-directory/signature socket construction | mined | 2026-10-23 | on-release | corpus/knowledge/bind-table-r25.md |

Duplicate review: searched the complete `corpus/SOURCES.md` for this exact raw URL; no match. The reviewed S153–S168 rows are other Hyprland rule-engine/client sources and do not duplicate this URL.

## Gates, touched surfaces, and limits

- Gate/evidence: no C1 counter was run and no verdict was scored. This source opening supplies a source anchor for the v4 oracle readback only.
- Fetch command: `mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1 && timeout 60 curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/hyprctl/src/main.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcHyprctlInstance.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcHyprctlInstance.bin && wc -c -l /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcHyprctlInstance.bin`
- Fetch outcome: `f6b0d1fcfc6695194c70964250591a35ffe90274309303d8f5fd0ac6f8c1c93f  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcHyprctlInstance.bin`; `583 17168 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcHyprctlInstance.bin` (`wc -c -l`: 583 lines, 17168 bytes).
- Touched surfaces: the fetched source artifact and this report only. No corpus file was edited; the SOURCES entry above is a draft for the report.
- Out of scope: no tool installation, product/counter changes, host configuration or service changes, live compositor verbs, runtime oracle execution, or build/test run.

## Artifact paths

- `.ufo/waves/round-25/fetch/a3w1/SrcHyprctlInstance.bin`
- `.ufo/waves/round-25/a3w1/reports/SrcHyprctlInstance.md`
