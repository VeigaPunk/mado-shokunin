# K4ShellOut — oracle shell-out control, counter v4

## Verdict
CONTROL K4ShellOut v4 best: cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED — not met

Both measured runs returned 0/41, embed_hits=0, exit=1, on fresh seeds `7fd5162ee689e505` and `954a5d8ce17a972b`. Both printed `ORACLE_CHECK base_vs_live missing=0 extra=0` and `V3_MODEL_AGREE 41/41`. This is a control receipt, not an admission judgment or a claim that all possible shell-out implementations have been excluded.

## Scope and axes

Read registration.md first, including Attempt 3 and PRED-C1 (v4), then the frozen counter and its imported sandbox runner. Wrote only the assigned single-file control `.ufo/waves/round-25/controls/v4/K4ShellOut.py` and this report in the lane. No `tools/mado-binds.py`, full resolver, counter amendment, corpus edit, git/jj write, or package change was made.

Axes: C1 operability and exact 18-field table fidelity; independence of the oracle and shortcut rejection; host safety and isolation; factual calibration/provenance. The control delegates all bind parsing to the installed Hyprland; its only config processing is copying bytes, removing exec keyword lines for safety, and appending non-bind ecosystem/debug options. It neither follows the source graph itself nor interprets variables, binds, flags, unbinds, or case labels. A complete JSON table must actually come from the child compositor's private command socket, hyprctl, or its log; otherwise stdout is `[]`.

Final control hash, printed identically in both scored receipts: `sha256:d41e395c1f5db6207ee006e2e5df4d8d431c35b40869ca418b4ae60016848d53`. Frozen counter receipt hash: `323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2`. Generator hash: `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375`.

## Counterexample and exact failure boundary

The smallest diagnostic input was an exec-keyword-free home whose `.config/hypr/hyprland.conf` contained exactly:

```ini
bind = SUPER, A, exec, true
```

Here `exec` is a bind dispatcher, not an executable startup keyword. Both diagnostic probes used the counter's exact bubblewrap mounts, namespaces, and cleared environment, with a 4 GB address-space cap and timeout. No local Hyprland was started outside bubblewrap by these probes. The final probe took 0.836 s, emitted `[]`, and exited 0.

| Final mode | Compositor natural exit | Queried instances | Observed result |
|---|---:|---:|---|
| cleared environment, no runtime | -6 (SIGABRT) | 0 | `XDG_RUNTIME_DIR is not set!` |
| writable private runtime, no display | -6 | 0 | seat unavailable, Wayland connect failed, no allocator |
| AQ headless plus WLR headless/pixman | -6 | 0 | same backend failure |
| headless plus llvmpipe/surfaceless | -6 | 0 | same backend failure |
| headless plus softpipe | -6 | 0 | same backend failure |
| AQ null plus software settings | -6 | 0 | same backend failure |
| AQ wayland, private `WAYLAND_DISPLAY=wayland-0` | -6 | 0 | same backend failure |
| AQ/WLR X11, `DISPLAY=:0` | -6 | 0 | same backend failure |
| `--verify-config` | 0 | 0 | `config ok`, no bind table |
| `--verify-config` plus trace/software settings | 0 | 0 | `config ok`, no bind table |

With the first runtime error fixed, the final diagnostic logged this actual failure sequence:

```text
DEBUG from aquamarine ]: [libseat] [libseat/backend/seatd.c:64] Could not connect to socket /run/seatd.sock: No such file or directory
ERR from aquamarine ]: [libseat] [libseat/backend/logind.c:638] Could not get primary session for user: No data available
ERR from aquamarine ]: [libseat] [libseat/libseat.c:79] No backend was able to open a seat
ERR from aquamarine ]: libseat: failed to open a seat
ERR from aquamarine ]: Failed to open a session
ERR from aquamarine ]: DRM Backend failed
ERR from aquamarine ]: Wayland backend cannot start: wl_display_connect failed (is a wayland compositor running?)
ERR from aquamarine ]: Requested backend (wayland) could not start, enabling fallbacks
ERR from aquamarine ]: Implementation wayland failed, erasing.
CRIT from aquamarine ]: Cannot open backend: no allocator available
CRIT ]: Critical error thrown: CBackend::create() failed!
```

`/run` and `/dev/dri` were absent. No child command socket was created, so the control's explicit-instance hyprctl and direct `j/binds` readers had no target to query; it did not contact another compositor. This is a startup/allocator failure, not a failure to decode a returned table. Software-rendering environment settings did not supply the missing Aquamarine allocator. `--verify-config` is a stronger counterexample to the simplistic claim that Hyprland cannot run at all in the sandbox: it parses this config and exits successfully, but exposes only validation text, not the 18-field bind table or IPC server.

The tested environment knobs are recorded in the control itself: `AQ_BACKEND` (headless/null/wayland/x11), `AQ_NO_DRM=1`, empty `AQ_DRM_DEVICES`, `AQ_TRACE=1`, `WLR_BACKENDS` (headless/x11), `WLR_HEADLESS_OUTPUTS=1`, `WLR_RENDERER=pixman`, `WLR_LIBINPUT_NO_DEVICES=1`, `WLR_NO_HARDWARE_CURSORS=1`, `LIBGL_ALWAYS_SOFTWARE=1`, `GALLIUM_DRIVER` (llvmpipe/softpipe), `MESA_LOADER_DRIVER_OVERRIDE=llvmpipe`, `EGL_PLATFORM=surfaceless`, and `HYPRLAND_TRACE=1`. These are experiments, not a claim that every knob is recognized by these versions.

### Source corroboration, with authority separated from observation

Opened the pinned startup implementation using:

```sh
timeout 30 curl -fsSL --max-filesize 2000000 https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/Compositor.cpp
```

[Hyprland v0.56.2 Compositor.cpp](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/Compositor.cpp), `CCompositor::initServer`, has a separate verification branch: it constructs the keybind manager, initializes the config manager, prints `Config::mgr()->verify()`, and returns before display/backend initialization. Normal initialization hard-codes mandatory HEADLESS, optional DRM, and fallback WAYLAND backend options; NULL is not selected at this site. It then requires `m_aqBackend->start()` before proceeding to `initManagers(STAGE_LATE)`, where CHyprCtl is created. The source literally retains `// TODO: headless only`. This source explains why an AQ_BACKEND environment guess alone does not change that selection; the runtime diagnostic, rather than source alone, establishes the actual failure on this host. The installed `/usr/include/aquamarine/backend/Backend.hpp:26-30` also enumerates HEADLESS and NULL separately.

`timeout 10 Hyprland --help` describes `--verify-config` as “Do not run Hyprland, only print if the config has any errors.” `timeout 10 ... Hyprland --version` reported 0.56.2, commit efb50993780079460b0cbed1363e2166a2de1d9f, Aquamarine 0.15.1, hyprlang 0.6.8, and hyprutils 0.14.2. The counter receipts independently name its own pinned bytes; no binary/source-equivalence claim is needed for the observed diagnostic.

### Fixable control defects corrected before scoring

The first sandbox diagnostic exposed an overlong private runtime socket path and disabled logs. The final control uses short runtime paths and explicitly enables stdout/file logging before any scored run. The first diagnostic's `--safe-mode` attempt ignored the supplied legacy config and selected/generated a Lua config; it was removed, rather than misrepresented as a case-tree oracle. The retained full final diagnostic below has no overlong-socket-path error. These are local control improvements, not counter changes. Both scored runs used identical final bytes.

## Smallest safe correction and remaining limit

No frozen-counter correction is supported by this shell-out result. Keep the display/DRM/socket isolation intact. Granting the tool the live runtime, display socket, or host GPU devices would change the trust boundary rather than repair static capability acquisition. The claimed solution must remain a static resolver, which this seat deliberately did not build. A hypothetical extra Hyprland bind-export interface is not present in the tested CLI; implementing or injecting one was not part of this control.

The failures establish that these normal startup, headless/software/backend, and verification-output routes do not meet v4. They do not prove every imaginable use of the executable is impossible, and the two seeds do not establish oracle determinism on other seeds. No numeric C1 gain or saturation claim is inferred.

## Commands, setup failures, and retry rule

The initial Python tool kernel lacked `HYPRLAND_INSTANCE_SIGNATURE` and `WAYLAND_DISPLAY`; the shell tool had both. Therefore the two initial runs failed at the counter's live capture, before any case was measured. Both exit-2 receipts are retained verbatim. `timeout 10 hyprctl instances -j` identified live PID 1614 with socket `wayland-1`; `timeout 5 printenv HYPRLAND_INSTANCE_SIGNATURE WAYLAND_DISPLAY XDG_RUNTIME_DIR HOME` provided the shell's actual session environment. Each failed run was retried exactly once, restoring those two environment values only for the host-side counter. Bubblewrap still clears the tool's environment; neither the counter nor sandbox rule changed. No exit-1 run was repeated.

All four counter invocations used the lane as cwd. The 1200-second counting command is the prescribed command, with an outer 4 GB address-space cap and disabled core dumps. The two independent score invocations ran concurrently; the counter's shared six-slot lock remained authoritative for nested host oracles.

### Initial run 1 — full stdout/stderr and exit

```sh
prlimit --as=4000000000 --core=0 timeout 1200 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4ShellOut.py
```

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4ShellOut.py sha256:d41e395c1f5db6207ee006e2e5df4d8d431c35b40869ca418b4ae60016848d53
seed=f9a8e10a69158d54
SETUP_ERROR hyprctl binds -j failed: CalledProcessError(1, ['timeout', '20', 'hyprctl', 'binds', '-j'])
exit=2
```

### Initial run 2 — full stdout/stderr and exit

```sh
prlimit --as=4000000000 --core=0 timeout 1200 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4ShellOut.py
```

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4ShellOut.py sha256:d41e395c1f5db6207ee006e2e5df4d8d431c35b40869ca418b4ae60016848d53
seed=ba3ddf2b0d6e2474
SETUP_ERROR hyprctl binds -j failed: CalledProcessError(1, ['timeout', '20', 'hyprctl', 'binds', '-j'])
exit=2
```

### Measured run 1 — one retry, full stdout/stderr and exit

Elapsed: 68.910 s.

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 WAYLAND_DISPLAY=wayland-1 prlimit --as=4000000000 --core=0 timeout 1200 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4ShellOut.py
```

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4ShellOut.py sha256:d41e395c1f5db6207ee006e2e5df4d8d431c35b40869ca418b4ae60016848d53
seed=7fd5162ee689e505
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=192 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=73 key='A' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=73 key='M' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=72 key='RIGHT' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=73 key='' keycode=13) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vaqcqitw) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-1   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vnyshroi) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-2   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vrzojlox) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-3   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vojdxmvx) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-0     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 16) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-1     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 17) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 29) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-3     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 7) v3_model=agree
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
CASE COMMENT-0    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-1    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=16 extra=0 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=2) v3_model=agree
    missing mask=65 key="F5" code=0 disp="exec" arg="logger 0blcel4c6d"
    missing mask=77 key="EQUAL" code=0 disp="exec" arg="ujpqvw8we ksmg"
CASE SYNTH-1      FAIL missing=12 extra=0 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
    missing mask=13 key="KP_5" code=0 disp="exec" arg="true y5i7jki81w"
    missing mask=64 key="KP_9" code=0 disp="exec" arg="5jrgqfh7s qx24"
CASE SYNTH-2      FAIL missing=15 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=3) v3_model=agree
    missing mask=13 key="ESCAPE" code=0 disp="exec" arg="true r6prk58lew"
    missing mask=77 key="F1" code=0 disp="exec" arg="notify-send 47pdsbql9u"
CASE SYNTH-3      FAIL missing=13 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
    missing mask=13 key="0" code=0 disp="exec" arg="logger wtn7d4uab9"
    missing mask=1 key="F19" code=0 disp="exec" arg="uarlc3xus lmht"
CASE REWRITE-0    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='' code=10; unbind mask=68 key='SPACE' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-1    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='LEFT' code=0; unbind mask=73 key='' code=11; add changegroupactive) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-2    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=0 key='switch:off:Lid Switch' code=0; unbind mask=64 key='G' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-3    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='M' code=0; unbind mask=65 key='' code=14; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE HARD-0       FAIL missing=17 extra=0 oracle_binds=17 (HARD tree lines=27 binds=17 unbinds=2 vars=4) v3_model=agree
    missing mask=72 key="" code=129 disp="movetoworkspace" arg="9"
    missing mask=4 key="F" code=0 disp="sendshortcut" arg="CONTROL_shift, 7, activewindow"
CASE HARD-1       FAIL missing=21 extra=0 oracle_binds=21 (HARD tree lines=32 binds=21 unbinds=3 vars=4) v3_model=agree
    missing mask=8 key="" code=189 disp="focusmonitor" arg="u"
    missing mask=65 key="" code=98 disp="layoutmsg" arg="5ol3"
CASE HARD-2       FAIL missing=23 extra=0 oracle_binds=23 (HARD tree lines=29 binds=23 unbinds=3 vars=4) v3_model=agree
    missing mask=1 key="P" code=0 disp="togglespecialworkspace" arg=""
    missing mask=64 key="F10" code=0 disp="movefocus" arg="l"
CASE HARD-3       FAIL missing=26 extra=0 oracle_binds=26 (HARD tree lines=31 binds=26 unbinds=2 vars=4) v3_model=agree
    missing mask=76 key="" code=51 disp="sendshortcut" arg="Shift, D, activewindow"
    missing mask=65 key="mouse:272" code=0 disp="mouse" arg="movewindow"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

### Measured run 2 — one retry, full stdout/stderr and exit

Elapsed: 65.897 s.

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 WAYLAND_DISPLAY=wayland-1 prlimit --as=4000000000 --core=0 timeout 1200 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4ShellOut.py
```

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4ShellOut.py sha256:d41e395c1f5db6207ee006e2e5df4d8d431c35b40869ca418b4ae60016848d53
seed=954a5d8ce17a972b
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=192 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=65 key='RETURN' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=68 key='COMMA' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=68 key='W' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=65 key='C' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $viqblnjm) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-1   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vcwiuaau) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-2   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vmhbrilf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-3   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vlzojuqs) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-0     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 29) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-1     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 18) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 4) v3_model=agree
    missing mask=8 key="KP_1" code=0 disp="exec" arg="logger 8w03tu018t"
    missing mask=72 key="END" code=0 disp="exec" arg="notify-send cp6cx5k45g"
CASE SOURCE-3     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 32) v3_model=agree
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
CASE COMMENT-0    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-1    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=14 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
    missing mask=9 key="HOME" code=0 disp="exec" arg="printf 2u3xhwtfm8"
    missing mask=5 key="F1" code=0 disp="exec" arg="true okasvt4pbk"
CASE SYNTH-1      FAIL missing=11 extra=0 oracle_binds=11 (SYNTH tree binds=11 unbound=1 vars=2) v3_model=agree
    missing mask=4 key="X" code=0 disp="exec" arg="logger we9s94trsg"
    missing mask=69 key="U" code=0 disp="exec" arg="true 1p5zniap1n"
CASE SYNTH-2      FAIL missing=17 extra=0 oracle_binds=17 (SYNTH tree binds=17 unbound=1 vars=2) v3_model=agree
    missing mask=9 key="E" code=0 disp="exec" arg="2f4rfvpvb z8wz"
    missing mask=65 key="9" code=0 disp="exec" arg="2f4rfvpvb 5pbv"
CASE SYNTH-3      FAIL missing=13 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
    missing mask=64 key="F5" code=0 disp="exec" arg="true rppu7hbhrr"
    missing mask=72 key="F21" code=0 disp="exec" arg="true zvmpu0padz"
CASE REWRITE-0    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='' code=13; unbind mask=65 key='P' code=0; add focusmonitor) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-1    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=0 key='XF86TouchpadOff' code=0; unbind mask=0 key='XF86AudioMicMute' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-2    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=72 key='' code=10; unbind mask=64 key='W' code=0; add fullscreenstate) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-3    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='RIGHT' code=0; unbind mask=76 key='B' code=0; add swapwindow) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE HARD-0       FAIL missing=26 extra=0 oracle_binds=26 (HARD tree lines=36 binds=26 unbinds=3 vars=4) v3_model=agree
    missing mask=1 key="" code=220 disp="movefocus" arg="d"
    missing mask=65 key="mouse:274" code=0 disp="mouse" arg="resizewindow"
CASE HARD-1       FAIL missing=18 extra=0 oracle_binds=18 (HARD tree lines=29 binds=18 unbinds=2 vars=4) v3_model=agree
    missing mask=68 key="" code=241 disp="togglegroup" arg="w03e"
    missing mask=73 key="8" code=0 disp="movefocus" arg="d"
CASE HARD-2       FAIL missing=20 extra=0 oracle_binds=20 (HARD tree lines=26 binds=20 unbinds=2 vars=4) v3_model=agree
    missing mask=64 key="B" code=0 disp="layoutmsg" arg=""
    missing mask=65 key="mouse:272" code=0 disp="mouse" arg="movewindow"
CASE HARD-3       FAIL missing=19 extra=0 oracle_binds=19 (HARD tree lines=32 binds=19 unbinds=3 vars=4) v3_model=agree
    missing mask=64 key="9" code=0 disp="sendshortcut" arg="SHIFT, BACKSPACE, activewindow"
    missing mask=65 key="I" code=0 disp="killactive" arg="kq5g"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

## Final exact-sandbox diagnostic — complete output

The temporary input home held only the one-line legacy config shown above and was deleted after the command.

```sh
timeout 60 prlimit --as=4000000000 --core=0 bwrap --ro-bind /usr /usr --symlink usr/lib /lib --symlink usr/lib64 /lib64 --symlink usr/bin /bin --proc /proc --dev /dev --tmpfs /tmp --ro-bind /tmp/k4shellout-probe-p0rmn1z0 /snap/home --ro-bind /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4ShellOut.py /snap/tool.py --unshare-all --die-with-parent --clearenv --setenv PATH /usr/bin --setenv HOME /snap/home python3 -I /snap/tool.py --home /snap/home
```

Stdout:

```text
[]
```

Stderr:

```text
SANDBOX exec_lines_removed=0 run_exists=False dri_exists=False
ATTEMPT cleared-no-runtime natural_exit=-6 final_exit=-6 queried_instances=0 table=none
LOG cleared-no-runtime begin
[1;35mCRIT [0m]: Critical error thrown: XDG_RUNTIME_DIR is not set!
terminate called after throwing an instance of 'std::runtime_error'
  what():  XDG_RUNTIME_DIR is not set!

LOG cleared-no-runtime end
ATTEMPT runtime-no-display natural_exit=-6 final_exit=-6 queried_instances=0 table=none
LOG runtime-no-display begin
[1;32mDEBUG [0m]: User-specified config location: '/tmp/kf7bx0608/home/.config/hypr/hyprland.conf'
Welcome to Hyprland!

                                                  
                     YY    UJ                     
                    YYY    UUJ                    
                   XXXY    UUUU                   
                  zXXXX    UUUUU                  
                zzzzX        UUUUJ                
               cczzz          UUUUJ               
             vccccz            UUUUUJ             
            vvcccc              UUUUUJ            
           vvvvv                  UUUUJ           
          uuuvv                    UUUUJ          
         uuuuu                      UUUUU         
        nnnuu                        UUUUU        
       nnnnn                          YUUUU       
       xxnn                            YUUU       
       xxxn                            YYUU       
      xxxx                              YYUU      
      rxxx                              YYYY      
      rrrx                              YYYY      
       rrrx                            XXXY       
       rrrr                            XXXX       
        rrrr                          zzXX        
         rrrr                        zzzz         
          rrrrr                    ccczz          
           rrrrrx                vccccc           
             rrrrxxxx        uuvvvvvc             
                rrxxxxxxnnnnuuuuuv                
                    xxxxxnnnnu                    



[!!WARNING!!] XDG_RUNTIME_DIR looks non-standard. Proceeding anyways...
DEBUG ]: Old rlimit: soft -> 524288, hard -> 524288
DEBUG ]: New rlimit: soft -> 524288, hard -> 524288
WARN ]: WARNING: Hyprland is being launched without start-hyprland. This is highly advised against.
DEBUG ]: Creating the EventLoopManager!
DEBUG ]: Creating the KeybindManager!
DEBUG ]: Creating the AnimationManager!
DEBUG ]: Creating the DynamicPermissionManager!
DEBUG ]: Creating the MonitorState!
DEBUG ]: Creating the WorkspaceState!
DEBUG ]: Creating the ConfigManager!
DEBUG ]: [cfg] Config is either explicit or special.
DEBUG ]: [cfg] Config is NOT lua, loading regular mgr
DEBUG ]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
DEBUG ]: !!!!HEY YOU, YES YOU!!!!: further logs to stdout / logfile are disabled by default. BEFORE SENDING THIS LOG, ENABLE THEM. Use debug:disable_logs = false to do so: https://wiki.hypr.land/Configuring/Basics/Variables/#debug
DEBUG ]: Creating the Error Overlay!
DEBUG ]: Creating the LayoutManager!
DEBUG ]: Creating the TokenManager!
DEBUG ]: Creating the EventManager!
DEBUG ]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
DEBUG ]: Creating the PointerManager!
DEBUG ]: Creating the AsyncResourceGatherer!
[1;32mDEBUG [0mfrom aquamarine ]: Creating an Aquamarine backend!
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/backend/seatd.c:64] Could not connect to socket /run/seatd.sock: No such file or directory
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:76] Backend 'seatd' failed to open seat, skipping
[1;31mERR [0mfrom aquamarine ]: [libseat] [libseat/backend/logind.c:638] Could not get primary session for user: No data available
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:76] Backend 'logind' failed to open seat, skipping
[1;31mERR [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:79] No backend was able to open a seat
[1;31mERR [0mfrom aquamarine ]: libseat: failed to open a seat
[1;31mERR [0mfrom aquamarine ]: Failed to open a session
[1;31mERR [0mfrom aquamarine ]: DRM Backend failed
[1;32mDEBUG [0mfrom aquamarine ]: Starting the Aquamarine backend!
[1;32mDEBUG [0mfrom aquamarine ]: Starting the Wayland backend!
[1;31mERR [0mfrom aquamarine ]: Wayland backend cannot start: wl_display_connect failed (is a wayland compositor running?)
[1;31mERR [0mfrom aquamarine ]: Requested backend (wayland) could not start, enabling fallbacks
[1;31mERR [0mfrom aquamarine ]: Implementation wayland failed, erasing.
[1;35mCRIT [0mfrom aquamarine ]: Cannot open backend: no allocator available
[1;35mCRIT [0m]: m_pAqBackend couldn't start! This usually means aquamarine could not find a GPU or encountered some issues. Make sure you're running either on a tty or on a Wayland session, NOT an X11 one.
[1;35mCRIT [0m]: Critical error thrown: CBackend::create() failed!
terminate called after throwing an instance of 'std::runtime_error'
  what():  CBackend::create() failed!


LOG runtime-no-display end
ATTEMPT aq-headless natural_exit=-6 final_exit=-6 queried_instances=0 table=none
LOG aq-headless begin
[1;32mDEBUG [0m]: User-specified config location: '/tmp/kf7bx0608/home/.config/hypr/hyprland.conf'
Welcome to Hyprland!

                                                  
                     YY    UJ                     
                    YYY    UUJ                    
                   XXXY    UUUU                   
                  zXXXX    UUUUU                  
                zzzzX        UUUUJ                
               cczzz          UUUUJ               
             vccccz            UUUUUJ             
            vvcccc              UUUUUJ            
           vvvvv                  UUUUJ           
          uuuvv                    UUUUJ          
         uuuuu                      UUUUU         
        nnnuu                        UUUUU        
       nnnnn                          YUUUU       
       xxnn                            YUUU       
       xxxn                            YYUU       
      xxxx                              YYUU      
      rxxx                              YYYY      
      rrrx                              YYYY      
       rrrx                            XXXY       
       rrrr                            XXXX       
        rrrr                          zzXX        
         rrrr                        zzzz         
          rrrrr                    ccczz          
           rrrrrx                vccccc           
             rrrrxxxx        uuvvvvvc             
                rrxxxxxxnnnnuuuuuv                
                    xxxxxnnnnu                    



[!!WARNING!!] XDG_RUNTIME_DIR looks non-standard. Proceeding anyways...
DEBUG ]: Old rlimit: soft -> 524288, hard -> 524288
DEBUG ]: New rlimit: soft -> 524288, hard -> 524288
WARN ]: WARNING: Hyprland is being launched without start-hyprland. This is highly advised against.
DEBUG ]: Creating the EventLoopManager!
DEBUG ]: Creating the KeybindManager!
DEBUG ]: Creating the AnimationManager!
DEBUG ]: Creating the DynamicPermissionManager!
DEBUG ]: Creating the MonitorState!
DEBUG ]: Creating the WorkspaceState!
DEBUG ]: Creating the ConfigManager!
DEBUG ]: [cfg] Config is either explicit or special.
DEBUG ]: [cfg] Config is NOT lua, loading regular mgr
DEBUG ]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
DEBUG ]: !!!!HEY YOU, YES YOU!!!!: further logs to stdout / logfile are disabled by default. BEFORE SENDING THIS LOG, ENABLE THEM. Use debug:disable_logs = false to do so: https://wiki.hypr.land/Configuring/Basics/Variables/#debug
DEBUG ]: Creating the Error Overlay!
DEBUG ]: Creating the LayoutManager!
DEBUG ]: Creating the TokenManager!
DEBUG ]: Creating the EventManager!
DEBUG ]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
DEBUG ]: Creating the PointerManager!
DEBUG ]: Creating the AsyncResourceGatherer!
[1;32mDEBUG [0mfrom aquamarine ]: Creating an Aquamarine backend!
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/backend/seatd.c:64] Could not connect to socket /run/seatd.sock: No such file or directory
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:76] Backend 'seatd' failed to open seat, skipping
[1;31mERR [0mfrom aquamarine ]: [libseat] [libseat/backend/logind.c:638] Could not get primary session for user: No data available
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:76] Backend 'logind' failed to open seat, skipping
[1;31mERR [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:79] No backend was able to open a seat
[1;31mERR [0mfrom aquamarine ]: libseat: failed to open a seat
[1;31mERR [0mfrom aquamarine ]: Failed to open a session
[1;31mERR [0mfrom aquamarine ]: DRM Backend failed
[1;32mDEBUG [0mfrom aquamarine ]: Starting the Aquamarine backend!
[1;32mDEBUG [0mfrom aquamarine ]: Starting the Wayland backend!
[1;31mERR [0mfrom aquamarine ]: Wayland backend cannot start: wl_display_connect failed (is a wayland compositor running?)
[1;31mERR [0mfrom aquamarine ]: Requested backend (wayland) could not start, enabling fallbacks
[1;31mERR [0mfrom aquamarine ]: Implementation wayland failed, erasing.
[1;35mCRIT [0mfrom aquamarine ]: Cannot open backend: no allocator available
[1;35mCRIT [0m]: m_pAqBackend couldn't start! This usually means aquamarine could not find a GPU or encountered some issues. Make sure you're running either on a tty or on a Wayland session, NOT an X11 one.
[1;35mCRIT [0m]: Critical error thrown: CBackend::create() failed!
terminate called after throwing an instance of 'std::runtime_error'
  what():  CBackend::create() failed!


LOG aq-headless end
ATTEMPT headless-llvmpipe natural_exit=-6 final_exit=-6 queried_instances=0 table=none
LOG headless-llvmpipe begin
[1;32mDEBUG [0m]: User-specified config location: '/tmp/kf7bx0608/home/.config/hypr/hyprland.conf'
Welcome to Hyprland!

                                                  
                     YY    UJ                     
                    YYY    UUJ                    
                   XXXY    UUUU                   
                  zXXXX    UUUUU                  
                zzzzX        UUUUJ                
               cczzz          UUUUJ               
             vccccz            UUUUUJ             
            vvcccc              UUUUUJ            
           vvvvv                  UUUUJ           
          uuuvv                    UUUUJ          
         uuuuu                      UUUUU         
        nnnuu                        UUUUU        
       nnnnn                          YUUUU       
       xxnn                            YUUU       
       xxxn                            YYUU       
      xxxx                              YYUU      
      rxxx                              YYYY      
      rrrx                              YYYY      
       rrrx                            XXXY       
       rrrr                            XXXX       
        rrrr                          zzXX        
         rrrr                        zzzz         
          rrrrr                    ccczz          
           rrrrrx                vccccc           
             rrrrxxxx        uuvvvvvc             
                rrxxxxxxnnnnuuuuuv                
                    xxxxxnnnnu                    



[!!WARNING!!] XDG_RUNTIME_DIR looks non-standard. Proceeding anyways...
DEBUG ]: Old rlimit: soft -> 524288, hard -> 524288
DEBUG ]: New rlimit: soft -> 524288, hard -> 524288
WARN ]: WARNING: Hyprland is being launched without start-hyprland. This is highly advised against.
DEBUG ]: Creating the EventLoopManager!
DEBUG ]: Creating the KeybindManager!
DEBUG ]: Creating the AnimationManager!
DEBUG ]: Creating the DynamicPermissionManager!
DEBUG ]: Creating the MonitorState!
DEBUG ]: Creating the WorkspaceState!
DEBUG ]: Creating the ConfigManager!
DEBUG ]: [cfg] Config is either explicit or special.
DEBUG ]: [cfg] Config is NOT lua, loading regular mgr
DEBUG ]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
DEBUG ]: !!!!HEY YOU, YES YOU!!!!: further logs to stdout / logfile are disabled by default. BEFORE SENDING THIS LOG, ENABLE THEM. Use debug:disable_logs = false to do so: https://wiki.hypr.land/Configuring/Basics/Variables/#debug
DEBUG ]: Creating the Error Overlay!
DEBUG ]: Creating the LayoutManager!
DEBUG ]: Creating the TokenManager!
DEBUG ]: Creating the EventManager!
DEBUG ]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
DEBUG ]: Creating the PointerManager!
DEBUG ]: Creating the AsyncResourceGatherer!
[1;32mDEBUG [0mfrom aquamarine ]: Creating an Aquamarine backend!
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/backend/seatd.c:64] Could not connect to socket /run/seatd.sock: No such file or directory
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:76] Backend 'seatd' failed to open seat, skipping
[1;31mERR [0mfrom aquamarine ]: [libseat] [libseat/backend/logind.c:638] Could not get primary session for user: No data available
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:76] Backend 'logind' failed to open seat, skipping
[1;31mERR [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:79] No backend was able to open a seat
[1;31mERR [0mfrom aquamarine ]: libseat: failed to open a seat
[1;31mERR [0mfrom aquamarine ]: Failed to open a session
[1;31mERR [0mfrom aquamarine ]: DRM Backend failed
[1;32mDEBUG [0mfrom aquamarine ]: Starting the Aquamarine backend!
[1;32mDEBUG [0mfrom aquamarine ]: Starting the Wayland backend!
[1;31mERR [0mfrom aquamarine ]: Wayland backend cannot start: wl_display_connect failed (is a wayland compositor running?)
[1;31mERR [0mfrom aquamarine ]: Requested backend (wayland) could not start, enabling fallbacks
[1;31mERR [0mfrom aquamarine ]: Implementation wayland failed, erasing.
[1;35mCRIT [0mfrom aquamarine ]: Cannot open backend: no allocator available
[1;35mCRIT [0m]: m_pAqBackend couldn't start! This usually means aquamarine could not find a GPU or encountered some issues. Make sure you're running either on a tty or on a Wayland session, NOT an X11 one.
[1;35mCRIT [0m]: Critical error thrown: CBackend::create() failed!
terminate called after throwing an instance of 'std::runtime_error'
  what():  CBackend::create() failed!


LOG headless-llvmpipe end
ATTEMPT headless-softpipe natural_exit=-6 final_exit=-6 queried_instances=0 table=none
LOG headless-softpipe begin
[1;32mDEBUG [0m]: User-specified config location: '/tmp/kf7bx0608/home/.config/hypr/hyprland.conf'
Welcome to Hyprland!

                                                  
                     YY    UJ                     
                    YYY    UUJ                    
                   XXXY    UUUU                   
                  zXXXX    UUUUU                  
                zzzzX        UUUUJ                
               cczzz          UUUUJ               
             vccccz            UUUUUJ             
            vvcccc              UUUUUJ            
           vvvvv                  UUUUJ           
          uuuvv                    UUUUJ          
         uuuuu                      UUUUU         
        nnnuu                        UUUUU        
       nnnnn                          YUUUU       
       xxnn                            YUUU       
       xxxn                            YYUU       
      xxxx                              YYUU      
      rxxx                              YYYY      
      rrrx                              YYYY      
       rrrx                            XXXY       
       rrrr                            XXXX       
        rrrr                          zzXX        
         rrrr                        zzzz         
          rrrrr                    ccczz          
           rrrrrx                vccccc           
             rrrrxxxx        uuvvvvvc             
                rrxxxxxxnnnnuuuuuv                
                    xxxxxnnnnu                    



[!!WARNING!!] XDG_RUNTIME_DIR looks non-standard. Proceeding anyways...
DEBUG ]: Old rlimit: soft -> 524288, hard -> 524288
DEBUG ]: New rlimit: soft -> 524288, hard -> 524288
WARN ]: WARNING: Hyprland is being launched without start-hyprland. This is highly advised against.
DEBUG ]: Creating the EventLoopManager!
DEBUG ]: Creating the KeybindManager!
DEBUG ]: Creating the AnimationManager!
DEBUG ]: Creating the DynamicPermissionManager!
DEBUG ]: Creating the MonitorState!
DEBUG ]: Creating the WorkspaceState!
DEBUG ]: Creating the ConfigManager!
DEBUG ]: [cfg] Config is either explicit or special.
DEBUG ]: [cfg] Config is NOT lua, loading regular mgr
DEBUG ]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
DEBUG ]: !!!!HEY YOU, YES YOU!!!!: further logs to stdout / logfile are disabled by default. BEFORE SENDING THIS LOG, ENABLE THEM. Use debug:disable_logs = false to do so: https://wiki.hypr.land/Configuring/Basics/Variables/#debug
DEBUG ]: Creating the Error Overlay!
DEBUG ]: Creating the LayoutManager!
DEBUG ]: Creating the TokenManager!
DEBUG ]: Creating the EventManager!
DEBUG ]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
DEBUG ]: Creating the PointerManager!
DEBUG ]: Creating the AsyncResourceGatherer!
[1;32mDEBUG [0mfrom aquamarine ]: Creating an Aquamarine backend!
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/backend/seatd.c:64] Could not connect to socket /run/seatd.sock: No such file or directory
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:76] Backend 'seatd' failed to open seat, skipping
[1;31mERR [0mfrom aquamarine ]: [libseat] [libseat/backend/logind.c:638] Could not get primary session for user: No data available
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:76] Backend 'logind' failed to open seat, skipping
[1;31mERR [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:79] No backend was able to open a seat
[1;31mERR [0mfrom aquamarine ]: libseat: failed to open a seat
[1;31mERR [0mfrom aquamarine ]: Failed to open a session
[1;31mERR [0mfrom aquamarine ]: DRM Backend failed
[1;32mDEBUG [0mfrom aquamarine ]: Starting the Aquamarine backend!
[1;32mDEBUG [0mfrom aquamarine ]: Starting the Wayland backend!
[1;31mERR [0mfrom aquamarine ]: Wayland backend cannot start: wl_display_connect failed (is a wayland compositor running?)
[1;31mERR [0mfrom aquamarine ]: Requested backend (wayland) could not start, enabling fallbacks
[1;31mERR [0mfrom aquamarine ]: Implementation wayland failed, erasing.
[1;35mCRIT [0mfrom aquamarine ]: Cannot open backend: no allocator available
[1;35mCRIT [0m]: m_pAqBackend couldn't start! This usually means aquamarine could not find a GPU or encountered some issues. Make sure you're running either on a tty or on a Wayland session, NOT an X11 one.
[1;35mCRIT [0m]: Critical error thrown: CBackend::create() failed!
terminate called after throwing an instance of 'std::runtime_error'
  what():  CBackend::create() failed!


LOG headless-softpipe end
ATTEMPT aq-null natural_exit=-6 final_exit=-6 queried_instances=0 table=none
LOG aq-null begin
[1;32mDEBUG [0m]: User-specified config location: '/tmp/kf7bx0608/home/.config/hypr/hyprland.conf'
Welcome to Hyprland!

                                                  
                     YY    UJ                     
                    YYY    UUJ                    
                   XXXY    UUUU                   
                  zXXXX    UUUUU                  
                zzzzX        UUUUJ                
               cczzz          UUUUJ               
             vccccz            UUUUUJ             
            vvcccc              UUUUUJ            
           vvvvv                  UUUUJ           
          uuuvv                    UUUUJ          
         uuuuu                      UUUUU         
        nnnuu                        UUUUU        
       nnnnn                          YUUUU       
       xxnn                            YUUU       
       xxxn                            YYUU       
      xxxx                              YYUU      
      rxxx                              YYYY      
      rrrx                              YYYY      
       rrrx                            XXXY       
       rrrr                            XXXX       
        rrrr                          zzXX        
         rrrr                        zzzz         
          rrrrr                    ccczz          
           rrrrrx                vccccc           
             rrrrxxxx        uuvvvvvc             
                rrxxxxxxnnnnuuuuuv                
                    xxxxxnnnnu                    



[!!WARNING!!] XDG_RUNTIME_DIR looks non-standard. Proceeding anyways...
DEBUG ]: Old rlimit: soft -> 524288, hard -> 524288
DEBUG ]: New rlimit: soft -> 524288, hard -> 524288
WARN ]: WARNING: Hyprland is being launched without start-hyprland. This is highly advised against.
DEBUG ]: Creating the EventLoopManager!
DEBUG ]: Creating the KeybindManager!
DEBUG ]: Creating the AnimationManager!
DEBUG ]: Creating the DynamicPermissionManager!
DEBUG ]: Creating the MonitorState!
DEBUG ]: Creating the WorkspaceState!
DEBUG ]: Creating the ConfigManager!
DEBUG ]: [cfg] Config is either explicit or special.
DEBUG ]: [cfg] Config is NOT lua, loading regular mgr
DEBUG ]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
DEBUG ]: !!!!HEY YOU, YES YOU!!!!: further logs to stdout / logfile are disabled by default. BEFORE SENDING THIS LOG, ENABLE THEM. Use debug:disable_logs = false to do so: https://wiki.hypr.land/Configuring/Basics/Variables/#debug
DEBUG ]: Creating the Error Overlay!
DEBUG ]: Creating the LayoutManager!
DEBUG ]: Creating the TokenManager!
DEBUG ]: Creating the EventManager!
DEBUG ]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
DEBUG ]: Creating the PointerManager!
DEBUG ]: Creating the AsyncResourceGatherer!
[1;32mDEBUG [0mfrom aquamarine ]: Creating an Aquamarine backend!
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/backend/seatd.c:64] Could not connect to socket /run/seatd.sock: No such file or directory
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:76] Backend 'seatd' failed to open seat, skipping
[1;31mERR [0mfrom aquamarine ]: [libseat] [libseat/backend/logind.c:638] Could not get primary session for user: No data available
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:76] Backend 'logind' failed to open seat, skipping
[1;31mERR [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:79] No backend was able to open a seat
[1;31mERR [0mfrom aquamarine ]: libseat: failed to open a seat
[1;31mERR [0mfrom aquamarine ]: Failed to open a session
[1;31mERR [0mfrom aquamarine ]: DRM Backend failed
[1;32mDEBUG [0mfrom aquamarine ]: Starting the Aquamarine backend!
[1;32mDEBUG [0mfrom aquamarine ]: Starting the Wayland backend!
[1;31mERR [0mfrom aquamarine ]: Wayland backend cannot start: wl_display_connect failed (is a wayland compositor running?)
[1;31mERR [0mfrom aquamarine ]: Requested backend (wayland) could not start, enabling fallbacks
[1;31mERR [0mfrom aquamarine ]: Implementation wayland failed, erasing.
[1;35mCRIT [0mfrom aquamarine ]: Cannot open backend: no allocator available
[1;35mCRIT [0m]: m_pAqBackend couldn't start! This usually means aquamarine could not find a GPU or encountered some issues. Make sure you're running either on a tty or on a Wayland session, NOT an X11 one.
[1;35mCRIT [0m]: Critical error thrown: CBackend::create() failed!
terminate called after throwing an instance of 'std::runtime_error'
  what():  CBackend::create() failed!


LOG aq-null end
ATTEMPT wayland-fallback natural_exit=-6 final_exit=-6 queried_instances=0 table=none
LOG wayland-fallback begin
[1;32mDEBUG [0m]: User-specified config location: '/tmp/kf7bx0608/home/.config/hypr/hyprland.conf'
Welcome to Hyprland!

                                                  
                     YY    UJ                     
                    YYY    UUJ                    
                   XXXY    UUUU                   
                  zXXXX    UUUUU                  
                zzzzX        UUUUJ                
               cczzz          UUUUJ               
             vccccz            UUUUUJ             
            vvcccc              UUUUUJ            
           vvvvv                  UUUUJ           
          uuuvv                    UUUUJ          
         uuuuu                      UUUUU         
        nnnuu                        UUUUU        
       nnnnn                          YUUUU       
       xxnn                            YUUU       
       xxxn                            YYUU       
      xxxx                              YYUU      
      rxxx                              YYYY      
      rrrx                              YYYY      
       rrrx                            XXXY       
       rrrr                            XXXX       
        rrrr                          zzXX        
         rrrr                        zzzz         
          rrrrr                    ccczz          
           rrrrrx                vccccc           
             rrrrxxxx        uuvvvvvc             
                rrxxxxxxnnnnuuuuuv                
                    xxxxxnnnnu                    



[!!WARNING!!] XDG_RUNTIME_DIR looks non-standard. Proceeding anyways...
DEBUG ]: Old rlimit: soft -> 524288, hard -> 524288
DEBUG ]: New rlimit: soft -> 524288, hard -> 524288
WARN ]: WARNING: Hyprland is being launched without start-hyprland. This is highly advised against.
DEBUG ]: Creating the EventLoopManager!
DEBUG ]: Creating the KeybindManager!
DEBUG ]: Creating the AnimationManager!
DEBUG ]: Creating the DynamicPermissionManager!
DEBUG ]: Creating the MonitorState!
DEBUG ]: Creating the WorkspaceState!
DEBUG ]: Creating the ConfigManager!
DEBUG ]: [cfg] Config is either explicit or special.
DEBUG ]: [cfg] Config is NOT lua, loading regular mgr
DEBUG ]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
DEBUG ]: !!!!HEY YOU, YES YOU!!!!: further logs to stdout / logfile are disabled by default. BEFORE SENDING THIS LOG, ENABLE THEM. Use debug:disable_logs = false to do so: https://wiki.hypr.land/Configuring/Basics/Variables/#debug
DEBUG ]: Creating the Error Overlay!
DEBUG ]: Creating the LayoutManager!
DEBUG ]: Creating the TokenManager!
DEBUG ]: Creating the EventManager!
DEBUG ]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
DEBUG ]: Creating the PointerManager!
DEBUG ]: Creating the AsyncResourceGatherer!
[1;32mDEBUG [0mfrom aquamarine ]: Creating an Aquamarine backend!
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/backend/seatd.c:64] Could not connect to socket /run/seatd.sock: No such file or directory
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:76] Backend 'seatd' failed to open seat, skipping
[1;31mERR [0mfrom aquamarine ]: [libseat] [libseat/backend/logind.c:638] Could not get primary session for user: No data available
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:76] Backend 'logind' failed to open seat, skipping
[1;31mERR [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:79] No backend was able to open a seat
[1;31mERR [0mfrom aquamarine ]: libseat: failed to open a seat
[1;31mERR [0mfrom aquamarine ]: Failed to open a session
[1;31mERR [0mfrom aquamarine ]: DRM Backend failed
[1;32mDEBUG [0mfrom aquamarine ]: Starting the Aquamarine backend!
[1;32mDEBUG [0mfrom aquamarine ]: Starting the Wayland backend!
[1;31mERR [0mfrom aquamarine ]: Wayland backend cannot start: wl_display_connect failed (is a wayland compositor running?)
[1;31mERR [0mfrom aquamarine ]: Requested backend (wayland) could not start, enabling fallbacks
[1;31mERR [0mfrom aquamarine ]: Implementation wayland failed, erasing.
[1;35mCRIT [0mfrom aquamarine ]: Cannot open backend: no allocator available
[1;35mCRIT [0m]: m_pAqBackend couldn't start! This usually means aquamarine could not find a GPU or encountered some issues. Make sure you're running either on a tty or on a Wayland session, NOT an X11 one.
[1;35mCRIT [0m]: Critical error thrown: CBackend::create() failed!
terminate called after throwing an instance of 'std::runtime_error'
  what():  CBackend::create() failed!


LOG wayland-fallback end
ATTEMPT x11-fallback natural_exit=-6 final_exit=-6 queried_instances=0 table=none
LOG x11-fallback begin
[1;32mDEBUG [0m]: User-specified config location: '/tmp/kf7bx0608/home/.config/hypr/hyprland.conf'
Welcome to Hyprland!

                                                  
                     YY    UJ                     
                    YYY    UUJ                    
                   XXXY    UUUU                   
                  zXXXX    UUUUU                  
                zzzzX        UUUUJ                
               cczzz          UUUUJ               
             vccccz            UUUUUJ             
            vvcccc              UUUUUJ            
           vvvvv                  UUUUJ           
          uuuvv                    UUUUJ          
         uuuuu                      UUUUU         
        nnnuu                        UUUUU        
       nnnnn                          YUUUU       
       xxnn                            YUUU       
       xxxn                            YYUU       
      xxxx                              YYUU      
      rxxx                              YYYY      
      rrrx                              YYYY      
       rrrx                            XXXY       
       rrrr                            XXXX       
        rrrr                          zzXX        
         rrrr                        zzzz         
          rrrrr                    ccczz          
           rrrrrx                vccccc           
             rrrrxxxx        uuvvvvvc             
                rrxxxxxxnnnnuuuuuv                
                    xxxxxnnnnu                    



[!!WARNING!!] XDG_RUNTIME_DIR looks non-standard. Proceeding anyways...
DEBUG ]: Old rlimit: soft -> 524288, hard -> 524288
DEBUG ]: New rlimit: soft -> 524288, hard -> 524288
WARN ]: WARNING: Hyprland is being launched without start-hyprland. This is highly advised against.
DEBUG ]: Creating the EventLoopManager!
DEBUG ]: Creating the KeybindManager!
DEBUG ]: Creating the AnimationManager!
DEBUG ]: Creating the DynamicPermissionManager!
DEBUG ]: Creating the MonitorState!
DEBUG ]: Creating the WorkspaceState!
DEBUG ]: Creating the ConfigManager!
DEBUG ]: [cfg] Config is either explicit or special.
DEBUG ]: [cfg] Config is NOT lua, loading regular mgr
DEBUG ]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
DEBUG ]: !!!!HEY YOU, YES YOU!!!!: further logs to stdout / logfile are disabled by default. BEFORE SENDING THIS LOG, ENABLE THEM. Use debug:disable_logs = false to do so: https://wiki.hypr.land/Configuring/Basics/Variables/#debug
DEBUG ]: Creating the Error Overlay!
DEBUG ]: Creating the LayoutManager!
DEBUG ]: Creating the TokenManager!
DEBUG ]: Creating the EventManager!
DEBUG ]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
DEBUG ]: Creating the PointerManager!
DEBUG ]: Creating the AsyncResourceGatherer!
[1;32mDEBUG [0mfrom aquamarine ]: Creating an Aquamarine backend!
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/backend/seatd.c:64] Could not connect to socket /run/seatd.sock: No such file or directory
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:76] Backend 'seatd' failed to open seat, skipping
[1;31mERR [0mfrom aquamarine ]: [libseat] [libseat/backend/logind.c:638] Could not get primary session for user: No data available
[1;32mDEBUG [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:76] Backend 'logind' failed to open seat, skipping
[1;31mERR [0mfrom aquamarine ]: [libseat] [libseat/libseat.c:79] No backend was able to open a seat
[1;31mERR [0mfrom aquamarine ]: libseat: failed to open a seat
[1;31mERR [0mfrom aquamarine ]: Failed to open a session
[1;31mERR [0mfrom aquamarine ]: DRM Backend failed
[1;32mDEBUG [0mfrom aquamarine ]: Starting the Aquamarine backend!
[1;32mDEBUG [0mfrom aquamarine ]: Starting the Wayland backend!
[1;31mERR [0mfrom aquamarine ]: Wayland backend cannot start: wl_display_connect failed (is a wayland compositor running?)
[1;31mERR [0mfrom aquamarine ]: Requested backend (wayland) could not start, enabling fallbacks
[1;31mERR [0mfrom aquamarine ]: Implementation wayland failed, erasing.
[1;35mCRIT [0mfrom aquamarine ]: Cannot open backend: no allocator available
[1;35mCRIT [0m]: m_pAqBackend couldn't start! This usually means aquamarine could not find a GPU or encountered some issues. Make sure you're running either on a tty or on a Wayland session, NOT an X11 one.
[1;35mCRIT [0m]: Critical error thrown: CBackend::create() failed!
terminate called after throwing an instance of 'std::runtime_error'
  what():  CBackend::create() failed!


LOG x11-fallback end
ATTEMPT verify-config natural_exit=0 final_exit=0 queried_instances=0 table=none
LOG verify-config begin
[1;32mDEBUG [0m]: User-specified config location: '/tmp/kf7bx0608/home/.config/hypr/hyprland.conf'
[1;32mDEBUG [0m]: [cfg] Config is either explicit or special.
[1;32mDEBUG [0m]: [cfg] Config is NOT lua, loading regular mgr
[1;32mDEBUG [0m]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
[1;32mDEBUG [0m]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
[1;32mDEBUG [0m]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf


======== Config parsing result:

config ok

LOG verify-config end
ATTEMPT verify-config-trace natural_exit=0 final_exit=0 queried_instances=0 table=none
LOG verify-config-trace begin
[1;32mDEBUG [0m]: User-specified config location: '/tmp/kf7bx0608/home/.config/hypr/hyprland.conf'
[1;32mDEBUG [0m]: [cfg] Config is either explicit or special.
[1;32mDEBUG [0m]: [cfg] Config is NOT lua, loading regular mgr
[1;32mDEBUG [0m]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
[1;32mDEBUG [0m]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf
[1;32mDEBUG [0m]: Using config: /tmp/kf7bx0608/home/.config/hypr/hyprland.conf


======== Config parsing result:

config ok

LOG verify-config-trace end
```

exit=0

## Safety and tooling

The program refuses host execution outside `/snap/home` with no `/run`; it only starts Hyprland after copying and stripping exec keyword lines. Its children have 4 GB address-space, 2 MiB file-size and zero-core limits, private process groups, per-attempt time bounds, a global deadline below the counter's 60-second tool limit, and unconditional TERM/KILL/wait cleanup. Probes' child processes all naturally exited and the finally cleanup still ran. Counter-owned oracle processes use the frozen counter's existing group cleanup. Temporary probe homes were removed. No standalone host compositor was started for this item; only the frozen counter started the host nested oracle instances authorized by the control contract. No live compositor write verb, service/package/config change, tool installation/update, or unrelated repository change was performed.
