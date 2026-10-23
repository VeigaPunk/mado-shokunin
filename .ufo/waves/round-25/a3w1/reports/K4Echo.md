# K4Echo — SERVER ECHO control against frozen C1 counter v4

## Verdict

CONTROL K4Echo v4 best: cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED — not met

The server-echo shortcut was rejected in both completed measurements (exit 1). Each had `ORACLE_CHECK base_vs_live missing=0 extra=0`, 41 failing cases, and no embedded-string hit. The first two attempts exited 2 before any case ran because this seat's Python orchestration environment lacked the live compositor signature; those attempts are **inconclusive**, not kills. Each received exactly one retry, with the host-only session context recovered through the allowed `hyprctl instances -j` read verb. No rule, counter, generator, or control byte changed between attempts.

## Scope and axes

- Axes: strength of the server-echo shortcut, bounded/repeatable evidence, and host/sibling safety.

- Assigned control/mutant: replace static bind resolution entirely with asking an existing compositor for its own bind array. No claimed `tools/mado-binds.py` was built, read as an implementation, or changed. This is a pre-data control, not a feature-ablation mutation of a landed resolver.

- Expected detector: the unchanged frozen v4 counter should reject this shape because the sandbox exposes no compositor IPC or host compositor process. Target remained 41/41 with embed_hits=0.

- Only lane writes: `.ufo/waves/round-25/controls/v4/K4Echo.py` and this requested report. No git/jj writes, package installs, services/config edits, live-compositor write verbs, runtime changes, or peer-source edits.

## Control behavior and bounds

`K4Echo.py` is a single Python stdlib program accepting `--home DIR`. It never opens or parses the Hyprland config tree. It first executes `hyprctl binds -j`, then `hyprctl instances -j`; discovers filesystem IPC under `/run`, `/tmp`, and any visible XDG runtime; inspects visible `/proc` process names/argv and, only for Hyprland processes, the two IPC-related environment fields; inspects `/proc/net/unix`, `/proc/self/net/unix`, and any visible compositor network tables; queries discovered signatures with `hyprctl -i SIGNATURE binds -j`; and tries discovered Hyprland command sockets plus four conventional abstract names. Direct socket requests send only `j/binds`. Event sockets are excluded. It returns the first JSON array of objects, otherwise `[]`; structured avenue diagnostics go to stderr.

Discovery is capped at 20 seconds, 10,000 entries per root/socket table, 2,048 visible PIDs, 256 candidate addresses, 8 MiB per socket reply, 2 seconds per hyprctl child, and 250 ms per socket operation. No namespace-escape technique, socket write verb, or nested compositor launch exists in the control. The official counter alone launches its bounded oracle instances, removes exec lines, applies its six-slot host-wide cap, and cleans each process group in `oracle()`'s finally block. Both completed counter processes returned normally through their cleanup paths.

## Which avenues were blocked

| Avenue | Actual observation | Isolation mechanism / limit of conclusion |
|---|---|---|

| `hyprctl binds -j` | exit 1; `HYPRLAND_INSTANCE_SIGNATURE not set! (is hyprland running?)` | `--clearenv` retains only PATH and HOME. Binary availability alone does not expose a table. |

| `hyprctl instances -j` | exit 0, raw stdout `\n]\n\n`, not a JSON array | No instance directory is visible. Exit 0 is not treated as evidence of a usable table. |

| `/run` filesystem sockets | `FileNotFoundError`, errno 2 | The sandbox does not mount `/run`; this also removes `/run/user/1000/hypr`. |

| `/tmp` filesystem sockets | 0 entries; no command sockets; scan not truncated | A private `--tmpfs /tmp` hides the host's temporary sockets and counter/oracle work trees. |

| `$XDG_RUNTIME_DIR` | unset, as is the instance signature | Cleared environment supplies no runtime or signature hints; no such root can be scanned from the variable. |

| Abstract Unix sockets | Both Unix tables have 0 entries; four conventional-address connects all fail `ECONNREFUSED` (111) | `--unshare-all` includes a private network namespace, isolating the Linux abstract Unix namespace. This is not a claim that guessed names exhaust every possible name; the empty namespace tables are the discovery evidence. |

| `/proc` compositor processes | Only `bwrap` and `python3`; 2 PIDs, no Hyprland, no read errors, not truncated | The PID namespace plus its `/proc` mount hides host and oracle compositor processes, preventing environment/signature recovery. No compositor-specific environment or network table could be read because no compositor PID was visible. |

| Discovered-signature `-i` / direct filesystem IPC | No signatures or filesystem socket candidates discovered | These conditional routes had no endpoint to query, rather than an observed per-endpoint permission denial. |

| Result | stdout `[]`, exit 0, `fallback_empty=true` | No compositor table was obtained in the diagnostic sandbox; both real counter runs likewise produced no extra binds in all 41 cases. |

Isolation source anchors: `c1/count-v3.py:729-743` supplies the actual bwrap argv; `c1/count.py:72-74` reuses it, `:124-189` owns/cleans oracle process groups, and `:272-298` scores arrays against Hyprland. Paths in this paragraph are relative to `.ufo/waves/round-25/`. Successful tool stderr is suppressed by `run_tool`, so a separate bounded invocation of the same sandbox argv captured the detailed avenue receipt below. Its temporary home was empty; the echo control never uses config bytes, so this changes no discovery behavior. No claim is made that the detailed stderr was captured for each of the 82 official cases.

## Commands and setup recovery

Capacity check: `timeout 10 df -h /fast` observed 222G available (804G total, 583G used). All command processes had explicit time bounds; scored/diagnostic runs used `prlimit --as=4000000000`. No tools were installed or updated.

The two initial commands, started concurrently, were exactly:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && timeout 1200 prlimit --as=4000000000 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4Echo.py
```

Both failed at `v3.live_capture()` before the sandbox tool or any nested oracle was run. The orchestration environment had HOME=/home/vgpnk and XDG_RUNTIME_DIR=/run/user/1000, but HYPRLAND_INSTANCE_SIGNATURE and WAYLAND_DISPLAY were unset. The recovery command was:

```sh
timeout 15 prlimit --as=4000000000 hyprctl instances -j
```

The oldest listed instance was the live one (PID 1614, socket `wayland-1`, signature `efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120`). Its discovered context was set only on the two counter retry subprocesses. The counter still clears the sandbox environment. The exact retry command, used once per exit-2 attempt with a fresh seed, was:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 WAYLAND_DISPLAY=wayland-1 timeout 1200 prlimit --as=4000000000 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4Echo.py
```

Recovery instance-list stdout (verbatim; it may include other seats' oracle instances, none modified by this seat):

```text
[
{
    "instance": "efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120",
    "time": 1792655744,
    "pid": 1614,
    "wl_socket": "wayland-1"
},
{
    "instance": "efb50993780079460b0cbed1363e2166a2de1d9f_1792740061_2125718214",
    "time": 1792740061,
    "pid": 1814466,
    "wl_socket": "wayland-4"
},
{
    "instance": "efb50993780079460b0cbed1363e2166a2de1d9f_1792740061_769419201",
    "time": 1792740061,
    "pid": 1810525,
    "wl_socket": "wayland-7"
},
{
    "instance": "efb50993780079460b0cbed1363e2166a2de1d9f_1792740062_2067556557",
    "time": 1792740062,
    "pid": 1816094,
    "wl_socket": "wayland-6"
},
{
    "instance": "efb50993780079460b0cbed1363e2166a2de1d9f_1792740062_1858092577",
    "time": 1792740062,
    "pid": 1815073,
    "wl_socket": "wayland-5"
},
{
    "instance": "efb50993780079460b0cbed1363e2166a2de1d9f_1792740062_85142587",
    "time": 1792740062,
    "pid": 1814566,
    "wl_socket": "wayland-2"
}
]

exit=0
```

## All counter receipts, verbatim

### Attempt 1 — initial; inconclusive setup failure

Elapsed 0.053 s. stdout:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4Echo.py sha256:a0458dfeea7254092ccc9b26960b37242a6496ec56441c96f24ebcc8a1168ef0
seed=43772f15443394c0
SETUP_ERROR hyprctl binds -j failed: CalledProcessError(1, ['timeout', '20', 'hyprctl', 'binds', '-j'])
exit=2
```

stderr: empty.

### Attempt 2 — initial; inconclusive setup failure

Elapsed 0.051 s. stdout:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4Echo.py sha256:a0458dfeea7254092ccc9b26960b37242a6496ec56441c96f24ebcc8a1168ef0
seed=69531f3220e52c28
SETUP_ERROR hyprctl binds -j failed: CalledProcessError(1, ['timeout', '20', 'hyprctl', 'binds', '-j'])
exit=2
```

stderr: empty.

### Attempt 3 — one retry of attempt 1

Elapsed 45.469 s. stdout:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4Echo.py sha256:a0458dfeea7254092ccc9b26960b37242a6496ec56441c96f24ebcc8a1168ef0
seed=adbedcf5ce9f4250
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=192 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=0 key='XF86TouchpadOn' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=0 key='XF86MonBrightnessDown' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=72 key='COMMA' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=69 key='SPACE' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vepvmygk) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-1   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vkfuxhgy) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-2   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vekxzkif) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-3   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vtrrjqla) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-0     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 8) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-1     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 29) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-3     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 9) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-0       FAIL missing=193 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-1       FAIL missing=193 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-2       FAIL missing=193 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-3       FAIL missing=193 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-0  FAIL missing=192 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-1  FAIL missing=192 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-2  FAIL missing=192 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-3  FAIL missing=192 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-0    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-1    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=4 key="INSERT" code=0 disp="exec" arg="notify-send vdjoxutgd1"
CASE SYNTH-0      FAIL missing=13 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
    missing mask=69 key="END" code=0 disp="exec" arg="ouel3o4e6 qrq8"
    missing mask=13 key="INSERT" code=0 disp="exec" arg="notify-send 2pqgzo1ob3"
CASE SYNTH-1      FAIL missing=13 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
    missing mask=5 key="S" code=0 disp="exec" arg="printf 96binkfdtz"
    missing mask=72 key="F16" code=0 disp="exec" arg="logger 6qxl6g9kba"
CASE SYNTH-2      FAIL missing=13 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
    missing mask=65 key="F19" code=0 disp="exec" arg="printf 4prke630xm"
    missing mask=9 key="F9" code=0 disp="exec" arg="printf r6qj4yb4fg"
CASE SYNTH-3      FAIL missing=14 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
    missing mask=13 key="F18" code=0 disp="exec" arg="wf51ubic7 czjf"
    missing mask=64 key="F1" code=0 disp="exec" arg="qbdbbz1yo iqfs"
CASE REWRITE-0    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=72 key='S' code=0; unbind mask=64 key='DOWN' code=0; add changegroupactive) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-1    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='' code=20; unbind mask=65 key='SLASH' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-2    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=72 key='COMMA' code=0; unbind mask=68 key='C' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-3    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=68 key='F' code=0; unbind mask=65 key='' code=13; add movetoworkspace) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE HARD-0       FAIL missing=25 extra=0 oracle_binds=25 (HARD tree lines=32 binds=25 unbinds=2 vars=4) v3_model=agree
    missing mask=68 key="" code=186 disp="layoutmsg" arg=""
    missing mask=64 key="END" code=0 disp="moveoutofgroup" arg="wo31"
CASE HARD-1       FAIL missing=17 extra=0 oracle_binds=17 (HARD tree lines=28 binds=17 unbinds=3 vars=4) v3_model=agree
    missing mask=72 key="mouse_up" code=0 disp="cyclenext" arg="ihn1"
    missing mask=0 key="" code=51 disp="togglegroup" arg="libu"
CASE HARD-2       FAIL missing=17 extra=0 oracle_binds=17 (HARD tree lines=27 binds=17 unbinds=1 vars=4) v3_model=agree
    missing mask=72 key="F11" code=0 disp="sendshortcut" arg="CTRL_Shift, F24, activewindow"
    missing mask=64 key="" code=181 disp="swapwindow" arg="l"
CASE HARD-3       FAIL missing=25 extra=0 oracle_binds=25 (HARD tree lines=34 binds=25 unbinds=2 vars=4) v3_model=agree
    missing mask=4 key="mouse:274" code=0 disp="mouse" arg="MoveWindow"
    missing mask=76 key="" code=58 disp="changegroupactive" arg=""
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

stderr: empty.

### Attempt 4 — one retry of attempt 2

Elapsed 37.254 s. stdout:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4Echo.py sha256:a0458dfeea7254092ccc9b26960b37242a6496ec56441c96f24ebcc8a1168ef0
seed=07cc364b51a15fa5
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=192 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=72 key='UP' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=190 extra=0 oracle_binds=190 (UNBIND mask=9 key='TAB' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=68 key='RIGHT' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=0 key='XF86AudioLowerVolume' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioMute" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume mute-toggl
CASE VARIABLE-0   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vfyegrsq) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-1   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vyucqwkp) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-2   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vpkklxox) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-3   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vbmtmvcm) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-0     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 12) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-1     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 16) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 4) v3_model=agree
    missing mask=13 key="H" code=0 disp="exec" arg="logger c3l5njo7gi"
    missing mask=5 key="F14" code=0 disp="exec" arg="true 7t727c0hth"
CASE SOURCE-3     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-0       FAIL missing=193 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-1       FAIL missing=193 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-2       FAIL missing=193 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-3       FAIL missing=193 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-0  FAIL missing=192 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-1  FAIL missing=192 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-2  FAIL missing=192 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-3  FAIL missing=192 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-0    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-1    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=13 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
    missing mask=9 key="F2" code=0 disp="exec" arg="logger aouiscfcoz"
    missing mask=13 key="COMMA" code=0 disp="exec" arg="printf yd5a069jue"
CASE SYNTH-1      FAIL missing=15 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=3) v3_model=agree
    missing mask=72 key="7" code=0 disp="exec" arg="logger ihthohkpl5"
    missing mask=4 key="F9" code=0 disp="exec" arg="nhujdqu0p mt34"
CASE SYNTH-2      FAIL missing=14 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
    missing mask=5 key="F6" code=0 disp="exec" arg="ldn1fx57y xpe3"
    missing mask=1 key="F8" code=0 disp="exec" arg="true lkn5uzs4lp"
CASE SYNTH-3      FAIL missing=14 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
    missing mask=76 key="KP_1" code=0 disp="exec" arg="notify-send 4bkuhari79"
    missing mask=68 key="F8" code=0 disp="exec" arg="wdkb0907j mn03"
CASE REWRITE-0    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='C' code=0; unbind mask=1 key='XF86MonBrightnessUp' code=0; add movecurrentworkspacetomonitor) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-1    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='' code=201; unbind mask=68 key='S' code=0; add movetoworkspacesilent) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-2    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='' code=13; unbind mask=65 key='' code=20; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-3    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=0 key='XF86AudioMute' code=0; unbind mask=72 key='LEFT' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE HARD-0       FAIL missing=20 extra=0 oracle_binds=20 (HARD tree lines=29 binds=20 unbinds=3 vars=4) v3_model=agree
    missing mask=13 key="" code=105 disp="focusmonitor" arg="u"
    missing mask=72 key="" code=172 disp="movecurrentworkspacetomonitor" arg="u"
CASE HARD-1       FAIL missing=22 extra=0 oracle_binds=22 (HARD tree lines=33 binds=22 unbinds=3 vars=4) v3_model=agree
    missing mask=13 key="B" code=0 disp="focusmonitor" arg="u"
    missing mask=73 key="1" code=0 disp="movetoworkspacesilent" arg="20"
CASE HARD-2       FAIL missing=17 extra=0 oracle_binds=17 (HARD tree lines=29 binds=17 unbinds=3 vars=4) v3_model=agree
    missing mask=1 key="SLASH" code=0 disp="killactive" arg=""
    missing mask=76 key="SLASH" code=0 disp="exec" arg="uwsm-app -- eqcol7 \"9wn 4isku\""
CASE HARD-3       FAIL missing=22 extra=0 oracle_binds=22 (HARD tree lines=31 binds=22 unbinds=3 vars=4) v3_model=agree
    missing mask=64 key="L" code=0 disp="movefocus" arg="u"
    missing mask=0 key="" code=248 disp="killactive" arg=""
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

stderr: empty.

## Bounded sandbox avenue probe

The same bwrap options as the frozen `run_tool` were used once, with an empty disposable temporary home. The home was removed by `TemporaryDirectory`; its absence was observed as `True`. Exact executed argv:

```sh
timeout 60 prlimit --as=4000000000 bwrap --ro-bind /usr /usr --symlink usr/lib /lib --symlink usr/lib64 /lib64 --symlink usr/bin /bin --proc /proc --dev /dev --tmpfs /tmp --ro-bind /tmp/mado-K4Echo-llhldhbe/home /snap/home --ro-bind /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4Echo.py /snap/tool.py --unshare-all --die-with-parent --clearenv --setenv PATH /usr/bin --setenv HOME /snap/home python3 -I /snap/tool.py --home /snap/home
```

stdout and exit, verbatim:

```text
[]
exit=0
```

stderr, verbatim (one JSON line):

```text
{"environment": {"HOME": "/snap/home", "HYPRLAND_INSTANCE_SIGNATURE": null, "XDG_RUNTIME_DIR": null}, "fallback_empty": true, "hyprctl": [{"argv": ["hyprctl", "binds", "-j"], "exit": 1, "extra_env": {}, "stderr": "", "stdout": "HYPRLAND_INSTANCE_SIGNATURE not set! (is hyprland running?)\n\n"}, {"argv": ["hyprctl", "instances", "-j"], "exit": 0, "extra_env": {}, "stderr": "", "stdout": "\n]\n\n"}], "proc": {"comms": {"bwrap": 1, "python3": 1}, "compositor_pids": [], "errors": [], "pid_count": 2, "truncated": false}, "result_binds": 0, "roots": [{"command_sockets": 0, "entries": 0, "error": "FileNotFoundError: [Errno 2] No such file or directory: '/run'", "errors": [], "path": "/run"}, {"command_sockets": 0, "entries": 0, "errors": [], "path": "/tmp", "truncated": false}], "selected": null, "socket_attempts": [{"address": "@hyprland", "errno": 111, "error": "ECONNREFUSED: [Errno 111] Connection refused", "origin": "abstract-conventional-name"}, {"address": "@hypr", "errno": 111, "error": "ECONNREFUSED: [Errno 111] Connection refused", "origin": "abstract-conventional-name"}, {"address": "@.socket.sock", "errno": 111, "error": "ECONNREFUSED: [Errno 111] Connection refused", "origin": "abstract-conventional-name"}, {"address": "@hyprland/.socket.sock", "errno": 111, "error": "ECONNREFUSED: [Errno 111] Connection refused", "origin": "abstract-conventional-name"}], "unix_tables": [{"abstract": 0, "entries": 0, "hyprland": 0, "named": 0, "path": "/proc/net/unix"}, {"abstract": 0, "entries": 0, "hyprland": 0, "named": 0, "path": "/proc/self/net/unix"}]}

```

## Before/after bytes and restoration evidence

No existing lane byte was mutated, so restoration of an existing resolver/counter was unnecessary. Before means immediately after writing the new control but before any detector ran; after means after both initial runs and both required retries. Every protected hash remained identical. The new control is intentionally retained as the requested control artifact, not substituted into the claimed tool path.

| Path (relative to lane) | Before sha256 | After sha256 |
|---|---|---|

| `.ufo/waves/round-25/c1/count.py` | `323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2` | `323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2` |

| `.ufo/waves/round-25/c1/count-v3.py` | `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375` | `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375` |

| `.ufo/waves/round-25/registration.md` | `aa86facc7b725a385c628f71d678b2f1d6da1c23d20988f0dee40365b64f99d3` | `aa86facc7b725a385c628f71d678b2f1d6da1c23d20988f0dee40365b64f99d3` |

| `.ufo/waves/round-25/controls/v4/K4Echo.py` | `a0458dfeea7254092ccc9b26960b37242a6496ec56441c96f24ebcc8a1168ef0` | `a0458dfeea7254092ccc9b26960b37242a6496ec56441c96f24ebcc8a1168ef0` |


Control size: 10318 bytes. The counter receipts independently print the same control and frozen counter/generator hashes. Initial setup failures are kept rather than silently discarded, and no completed measurement was rerun to improve a score.


Restoration verdict: protected original bytes unchanged; disposable diagnostic home removed; both bounded detector retries completed with normal counter cleanup; no manual live-compositor action or external runtime was invoked by this control beyond the explicitly requested `hyprctl` read-only client.
