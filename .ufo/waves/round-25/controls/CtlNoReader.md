# CtlNoReader — round-25 C1 pre-data control (NO-READER shape)

Control seat: `MadoR25.CtlNoReader`. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`
(jj-colocated, branch `master`, registration landed at `04051723562b8a6ac1f3a9ae05e861aa6f544aff`).
Claim under control: **C1**, predicate **PRED-C1** (see `.ufo/waves/round-25/registration.md`).
Counter: `.ufo/waves/round-25/c1/count.py`, frozen sha256 `70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895`.

## Shape

**NO-READER.** The stub never opens anything under `HOME` — or anywhere else that could carry
config bytes. It accepts `--home DIR`, discards the value, and prints a fixed, plausible
omarchy-style bind table written out longhand from **public omarchy defaults** (omarchy's
`default/hypr/bindings/*.conf`: `media.conf`, `tiling-v2.conf`, `utilities.conf`,
`clipboard.conf`). No live capture was copied into the file. The table is emitted in the
exact 18-field shape of `hyprctl binds -j` (HyprCtl `bindsRequest`, Hyprland v0.56.2), with
the correct field names, boolean types, integer `modmask` (SHIFT=1, CTRL=4, ALT=8, SUPER=64
per `src/devices/IKeyboard.hpp`), and the string-typed `submap_universal`.

The stub is 40 hand-written entries, each built as a literal tuple in the source. It has no
config parser, no `source =` following, no glob expansion, no `$var` expansion, no `unbind =`
handling, and no comment stripping. Every entry is emitted unconditionally, identically, on
every invocation — including for the SYNTH cases, where the config tree is a wholly different
synthetic forest.

## What the stub does and skips

**Does:** parse `--home` and throw it away; print a constant 40-entry JSON array of bind
objects in `hyprctl binds -j` field shape; exit 0.

**Skips — the entire real work of the C1 surface:**

- reading `DIR/.config/hypr/hyprland.conf` and following `source =` (glob-aware) into
  `~/.local/share/omarchy/default/hypr/**`, `~/.config/omarchy/current/theme/**`,
  `~/.local/state/omarchy/toggles/hypr/*.conf` and the user's `~/.config/hypr/**`;
- hyprlang v0.6.8 comment handling (leading `#` line, trailing `#` comment, `##` escape);
- hyprlang v0.6.8 `$var` expansion (the VARIABLE and SYNTH families both hinge on it);
- Hyprland v0.56.2 `ConfigManager::handleBind` / `handleUnbind` / `parseKey`
  (`code:NN` → keycode, `catchall`, numeric keys > 9) and `KeybindManager::stringToModMask`
  (uppercase-then-substring modifier matching, so `SUPER`+`SHIFT` → 65);
- `KeybindManager::removeKeybind` unbind semantics (erase on exact modmask+key+keycode);
- the per-run perturbation deltas the counter writes (random keys, random flags, random
  `$var` names, random file names, random arg tokens).

**Proof of the NO-READER property.** The stub was traced under `strace -f -e
trace=openat,open,stat,statx,getdents64` inside the counter's own bubblewrap invocation
shape (`--ro-bind home /snap/home --ro-bind tool /snap/tool.py --unshare-all --clearenv
--setenv HOME /snap/home python3 -I /snap/tool.py --home /snap/home`). Result: **0**
`open`/`openat`/`stat`/`statx`/`getdents64` calls naming `/snap/home` — the counter's case
directory is never touched. The only paths opened are the interpreter's own
(`/usr/lib/libpython3.14.so.1.0`, `/usr/bin/pyvenv.cfg`, `/etc/localtime`, `/proc/self/maps`).
Traced under `python3 -I` (as the counter invokes it) the stub also makes **0** calls under
`/home/vgpnk`; traced without `-I` it touches `/home/vgpnk/.local/lib/python3.14/site-packages`
twice, which is CPython's own user-site probe, not the stub, and does not occur under the
counter's `-I` invocation.

**Host safety.** Read-only throughout. No package, display, compositor, service or
`~/.config` change. `hyprctl` was used only with read verbs (`binds -j`, `version`,
`getoption`) — by this seat and by the counter itself. No `dispatch`, `keyword`, `reload`,
`setprop`, `reload` or any other write verb. Every subprocess was bounded by `timeout`.
No git or jj write command was run in the lane repo or the fleet repo; the only git calls
were read-only (`rev-parse`, `show`, `status`, `diff`, `sha256sum` of blobs).

## Counter provenance and a mid-round counter mutation

The scored run below is against the **frozen v1 counter**, sha256 `70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895`, which is
the sha256 named in `registration.md`. The counter self-reports its own sha256 on the first
line of stdout, and the scored run's stdout carries exactly that value, so the bytes that
produced this receipt are provably the frozen ones. This seat did not edit, re-version or
otherwise touch the counter.

**Fact recorded for the wave, not caused by this seat:** while this seat was running, the
counter file in the lane was **mutated in place** by another actor, from frozen v1
(`70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895`) to a v2 (`b251ddecb3a99993bbb8a7e9cb2363896da7f69ac58bf63e6b8deb2e0ccf81a8`) that adds a `REWRITE` case type (33 → 37 cases); the
frozen v1 was preserved alongside as `.ufo/waves/round-25/c1/count-v1.py` (sha256
`70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895`), and `registration.md` was also edited. File mtimes: frozen v1 in the working
tree 02:11:02, `count-v1.py` 02:11:24, `registration.md` 02:11:40 — all **after** this
seat's scored run completed at 02:08:53. The scored run therefore ran against the frozen
counter, and the v1 bytes remain available verbatim at `.ufo/waves/round-25/c1/count-v1.py`.
Because a control must be scored against the counter it was assigned, this receipt reports
the **frozen v1** run as the scored result and adds a clearly-labelled **supplementary v2
run** so the wave can see the control is not sensitive to the counter revision. The v2 run
was made after the mutation, using the same stub file and the same command form.

## Scored run — frozen v1 counter

Exact command:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && timeout 900 python3 -I .ufo/waves/round-25/c1/count.py 04051723562b8a6ac1f3a9ae05e861aa6f544aff --tool-file /fast/scratch/hyaku/mado-r25/controls/CtlNoReader/stub.py
```

Exit code: **1**

Complete counter stdout, verbatim:

```text
counter sha256:70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895 rev=04051723562b8a6ac1f3a9ae05e861aa6f544aff
tool=override:/fast/scratch/hyaku/mado-r25/controls/CtlNoReader/stub.py sha256:aa8f0986d3ddfb25daaf33dddf786566a4f21d1c75fdd0f6c457a50e83504665
seed=571c72202734aaf3
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
EMBED_HIT 'Brightness down'
EMBED_HIT 'Brightness maximum'
EMBED_HIT 'Brightness minimum'
EMBED_HIT 'Brightness up'
EMBED_HIT 'Clipboard manager'
CASE BASE         FAIL missing=171 extra=19 (unperturbed)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE ADD-0        FAIL missing=172 extra=19 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE ADD-1        FAIL missing=172 extra=19 (ADD into .config/hypr/bindings.conf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE ADD-2        FAIL missing=172 extra=19 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE ADD-3        FAIL missing=172 extra=19 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE UNBIND-0     FAIL missing=170 extra=19 (UNBIND mask=68 key='SPACE' keycode=0)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE UNBIND-1     FAIL missing=170 extra=19 (UNBIND mask=73 key='B' keycode=0)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE UNBIND-2     FAIL missing=171 extra=20 (UNBIND mask=64 key='' keycode=14)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="" code=14 disp="workspace" arg="5"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
CASE UNBIND-3     FAIL missing=170 extra=19 (UNBIND mask=65 key='DOWN' keycode=0)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE VARIABLE-0   FAIL missing=172 extra=19 (VARIABLE $vfyykjln)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE VARIABLE-1   FAIL missing=172 extra=19 (VARIABLE $vkfsfszo)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE VARIABLE-2   FAIL missing=172 extra=19 (VARIABLE $vmmtongn)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE VARIABLE-3   FAIL missing=172 extra=19 (VARIABLE $vlcvhhxf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE SOURCE-0     FAIL missing=173 extra=19 (SOURCE new file at root line 9)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE SOURCE-1     FAIL missing=173 extra=19 (SOURCE new file at root line 29)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE SOURCE-2     FAIL missing=173 extra=19 (SOURCE new file at root line 10)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE SOURCE-3     FAIL missing=173 extra=19 (SOURCE new file at root line 17)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE GLOB-0       FAIL missing=172 extra=19 (GLOB new toggles file)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE GLOB-1       FAIL missing=172 extra=19 (GLOB new toggles file)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE GLOB-2       FAIL missing=172 extra=19 (GLOB new toggles file)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE GLOB-3       FAIL missing=172 extra=19 (GLOB new toggles file)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE UNSOURCED-0  FAIL missing=171 extra=19 (UNSOURCED new bindings file)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE UNSOURCED-1  FAIL missing=171 extra=19 (UNSOURCED new bindings file)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE UNSOURCED-2  FAIL missing=171 extra=19 (UNSOURCED new bindings file)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE UNSOURCED-3  FAIL missing=171 extra=19 (UNSOURCED new bindings file)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE COMMENT-0    FAIL missing=172 extra=19 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE COMMENT-1    FAIL missing=172 extra=19 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE COMMENT-2    FAIL missing=172 extra=19 (COMMENT into .config/hypr/bindings.conf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE COMMENT-3    FAIL missing=172 extra=19 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE SYNTH-0      FAIL missing=15 extra=40 (SYNTH tree binds=15 unbound=1 vars=2)
    missing mask=5 key="8" code=0 disp="exec" arg="true vg6qbupddd"
    missing mask=13 key="9" code=0 disp="exec" arg="nj9p48uq2 0swh"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-1      FAIL missing=14 extra=40 (SYNTH tree binds=14 unbound=1 vars=2)
    missing mask=72 key="F17" code=0 disp="exec" arg="logger c1n6dmlwbi"
    missing mask=5 key="T" code=0 disp="exec" arg="4lwmrwp02 tsci"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-2      FAIL missing=10 extra=40 (SYNTH tree binds=10 unbound=1 vars=2)
    missing mask=1 key="D" code=0 disp="exec" arg="printf zircsgqamt"
    missing mask=69 key="J" code=0 disp="exec" arg="true 85hvsr9rw0"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-3      FAIL missing=12 extra=40 (SYNTH tree binds=12 unbound=1 vars=2)
    missing mask=72 key="F9" code=0 disp="exec" arg="notify-send 612g8dinnl"
    missing mask=9 key="T" code=0 disp="exec" arg="notify-send qr1v6bqici"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
PRED-C1 cases_pass=0/33 embed_hits=43 verdict=TARGET_MISSED
```

Final predicate line:

```text
PRED-C1 cases_pass=0/33 embed_hits=43 verdict=TARGET_MISSED
```

## Supplementary run — counter v2 (post-mutation), same stub, same command form

Exact command:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && timeout 900 python3 -I .ufo/waves/round-25/c1/count.py 04051723562b8a6ac1f3a9ae05e861aa6f544aff --tool-file /fast/scratch/hyaku/mado-r25/controls/CtlNoReader/stub.py
```

Exit code: **1**

Complete counter stdout, verbatim:

```text
counter sha256:b251ddecb3a99993bbb8a7e9cb2363896da7f69ac58bf63e6b8deb2e0ccf81a8 rev=04051723562b8a6ac1f3a9ae05e861aa6f544aff
tool=override:/fast/scratch/hyaku/mado-r25/controls/CtlNoReader/stub.py sha256:aa8f0986d3ddfb25daaf33dddf786566a4f21d1c75fdd0f6c457a50e83504665
seed=561f5a3395cd6ad0
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
EMBED_HIT 'Brightness down'
EMBED_HIT 'Brightness maximum'
EMBED_HIT 'Brightness minimum'
EMBED_HIT 'Brightness up'
EMBED_HIT 'Clipboard manager'
CASE BASE         FAIL missing=171 extra=19 (unperturbed)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE ADD-0        FAIL missing=172 extra=19 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE ADD-1        FAIL missing=172 extra=19 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE ADD-2        FAIL missing=172 extra=19 (ADD into .config/hypr/bindings.conf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE ADD-3        FAIL missing=172 extra=19 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE UNBIND-0     FAIL missing=170 extra=19 (UNBIND mask=65 key='G' keycode=0)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE UNBIND-1     FAIL missing=170 extra=19 (UNBIND mask=8 key='XF86AudioRaiseVolume' keycode=0)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE UNBIND-2     FAIL missing=170 extra=19 (UNBIND mask=69 key='R' keycode=0)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE UNBIND-3     FAIL missing=171 extra=20 (UNBIND mask=0 key='XF86AudioMicMute' keycode=0)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=0 key="XF86AudioMicMute" code=0 disp="exec" arg="omarchy-audio-input-mute"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
CASE VARIABLE-0   FAIL missing=172 extra=19 (VARIABLE $vkdgxrvs)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE VARIABLE-1   FAIL missing=172 extra=19 (VARIABLE $vhayfbqo)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE VARIABLE-2   FAIL missing=172 extra=19 (VARIABLE $vwdylota)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE VARIABLE-3   FAIL missing=172 extra=19 (VARIABLE $veogaqsn)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE SOURCE-0     FAIL missing=173 extra=19 (SOURCE new file at root line 16)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE SOURCE-1     FAIL missing=173 extra=19 (SOURCE new file at root line 20)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE SOURCE-2     FAIL missing=173 extra=19 (SOURCE new file at root line 8)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE SOURCE-3     FAIL missing=173 extra=19 (SOURCE new file at root line 7)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE GLOB-0       FAIL missing=172 extra=19 (GLOB new toggles file)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE GLOB-1       FAIL missing=172 extra=19 (GLOB new toggles file)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE GLOB-2       FAIL missing=172 extra=19 (GLOB new toggles file)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE GLOB-3       FAIL missing=172 extra=19 (GLOB new toggles file)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE UNSOURCED-0  FAIL missing=171 extra=19 (UNSOURCED new bindings file)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE UNSOURCED-1  FAIL missing=171 extra=19 (UNSOURCED new bindings file)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE UNSOURCED-2  FAIL missing=171 extra=19 (UNSOURCED new bindings file)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE UNSOURCED-3  FAIL missing=171 extra=19 (UNSOURCED new bindings file)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE COMMENT-0    FAIL missing=172 extra=19 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE COMMENT-1    FAIL missing=172 extra=19 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE COMMENT-2    FAIL missing=172 extra=19 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE COMMENT-3    FAIL missing=172 extra=19 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE SYNTH-0      FAIL missing=12 extra=40 (SYNTH tree binds=12 unbound=1 vars=3)
    missing mask=69 key="U" code=0 disp="exec" arg="notify-send tjlalez148"
    missing mask=8 key="INSERT" code=0 disp="exec" arg="ijcnvaa2u ujwb"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-1      FAIL missing=13 extra=40 (SYNTH tree binds=13 unbound=1 vars=2)
    missing mask=72 key="O" code=0 disp="exec" arg="logger gapxuenmoc"
    missing mask=73 key="9" code=0 disp="exec" arg="notify-send vz301wma0d"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-2      FAIL missing=12 extra=40 (SYNTH tree binds=12 unbound=1 vars=3)
    missing mask=69 key="PRINT" code=0 disp="exec" arg="ugyur7ier tunx"
    missing mask=8 key="F6" code=0 disp="exec" arg="true dq0xhai1na"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-3      FAIL missing=17 extra=40 (SYNTH tree binds=17 unbound=1 vars=2)
    missing mask=76 key="ESCAPE" code=0 disp="exec" arg="true l0lps053r1"
    missing mask=5 key="3" code=0 disp="exec" arg="true ypqv0ophff"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-0    FAIL missing=172 extra=20 (REWRITE argswap mask=65 key='' code=15; unbind mask=1 key='XF86MonBrightnessUp' code=0; add exec)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
CASE REWRITE-1    FAIL missing=171 extra=19 (REWRITE argswap mask=72 key='RIGHT' code=0; unbind mask=73 key='DOWN' code=0; add exec)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE REWRITE-2    FAIL missing=171 extra=19 (REWRITE argswap mask=69 key='SPACE' code=0; unbind mask=65 key='' code=15; add exec)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
CASE REWRITE-3    FAIL missing=171 extra=19 (REWRITE argswap mask=68 key='BACKSPACE' code=0; unbind mask=64 key='DOWN' code=0; add exec)
    missing mask=0 key="XF86KbdBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-keyboard up"
    missing mask=0 key="XF86KbdBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-keyboard down"
    extra   mask=64 key="Q" code=0 disp="exec" arg="omarchy-menu-keybindings"
    extra   mask=64 key="D" code=0 disp="exec" arg="omarchy-launch-walker"
PRED-C1 cases_pass=0/37 embed_hits=43 verdict=TARGET_MISSED
```

Final predicate line:

```text
PRED-C1 cases_pass=0/37 embed_hits=43 verdict=TARGET_MISSED
```

## Hashes

```text
aa8f0986d3ddfb25daaf33dddf786566a4f21d1c75fdd0f6c457a50e83504665  /fast/scratch/hyaku/mado-r25/controls/CtlNoReader/stub.py
aa8f0986d3ddfb25daaf33dddf786566a4f21d1c75fdd0f6c457a50e83504665  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/CtlNoReader.py
70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895  .ufo/waves/round-25/c1/count-v1.py   (frozen v1 counter, preserved by the mutating seat)
b251ddecb3a99993bbb8a7e9cb2363896da7f69ac58bf63e6b8deb2e0ccf81a8  .ufo/waves/round-25/c1/count.py   (counter v2, mutated in place mid-round)
9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779  live `hyprctl binds -j` capture used by both runs (stable across both)
```

The live capture sha256 is identical in both runs and equals the sha256 observed before the
scored run began, so the compositor's bind table did not move during the wave.


## Reading of the result

The NO-READER shape misses on **both** halves of PRED-C1, and the two failures have
different causes, which matters for how much the wave should read into the counter.

**Behavioural half — `cases_pass=0/33`.** Not one case passes, and the mechanism is
structural rather than a near miss. The counter's BASE case expects the *live* 192-entry
multiset, while the stub emits a fixed 40-entry table; the gap is 171 missing / 19 extra
before any perturbation. Because the stub's output does not depend on the case directory at
all, every perturbed case inherits the same base mismatch plus its own delta: ADD and
VARIABLE add one random bind (missing 172), SOURCE adds two (missing 173), UNBIND removes
one live bind (missing 170), UNSOURCED adds two binds the tool is expected *not* to see
(missing 171), and the four SYNTH cases replace the whole tree with 10–15 unknown binds
(missing 10–15, extra 40). The SYNTH rows are the sharpest: the counter deletes the snapshot
and writes a fresh synthetic forest with random keys and random arg tokens, so a constant
table is guaranteed to miss. This is the registration's own argument — "keys, mods, flags,
descriptions and args of generated binds are random per run, so no fixture id or label
exists to key on" — confirmed with a measurement.

**Embed half — `embed_hits=43`.** The counter scans the tool bytes for the live capture's
`arg`/`description` strings of ≥12 characters. The stub trips it 43 times. Worth recording
precisely *why*, because the reason is a fact about the counter's discriminator rather than
about this stub's diligence: **all 43 hits are strings that also occur verbatim in the
public omarchy default tree** (`~/.local/share/omarchy/default/hypr/**`), and **zero** of
them are user-specific. This was checked by walking the public default tree and intersecting
the hit set: 43 of 43 present in the public defaults, 0 of 43 absent from them. In other
words a stub that never read the live capture and wrote only public omarchy defaults still
trips the embed check — because on this host the public omarchy defaults *are* the live
table's vocabulary. The embed check is therefore not a "did you copy the live capture"
detector on an omarchy host; it is a "did you write any ≥12-character string that the live
capture contains" detector, and public defaults are indistinguishable from a live copy
under it.

**Verdict.** The NO-READER shortcut does not meet PRED-C1, and cannot be made to meet it by
any amount of tuning of a fixed table, because the counter's expected multiset is a
function of the case directory that the stub by construction never reads.

## Critique (not part of the score)

This paragraph is outside the scored result above and proposes no change to the frozen
counter or to the registration.

The strongest counterexample to the *round's framing* of PRED-C1 is not about this seat's
stub at all; it is that the counter's embed check is a **literal substring scan of the tool
bytes** (`s in text` over the raw file, frozen v1 `count.py` lines 386–392), and a literal substring
scan cannot distinguish "embedded the live capture" from "wrote the same bytes in two
pieces". I verified this against the counter's own logic: a tool file containing
`"omarchy-swayosd-client --output-volume " + "raise"` yields **0** embed hits for the
string `omarchy-swayosd-client --output-volume raise`, while the same bytes written as one
literal yield **1**. The check is defeated by any transformation that is trivial to apply —
string concatenation, `repr()`-style escaping, base64, or byte reversal — and none of those
transformations makes a tool *behave* correctly. The consequence for the round is that
`embed_hits=0` is not evidence of the property the registration wants it to witness
("the tool bytes contain none of the live capture's arg or description strings"); it is
evidence only that the tool did not embed those strings *verbatim*. The v2 counter's
docstring records that the CtlLabelKeyed critique led to the REWRITE family being added for
a closely related reason, so the wave is already moving on this axis; the smallest safe
correction, if the canonical judge wants one, is to define the embed criterion
**behaviourally** — score the tool's *stdout* against the live capture's strings, which is
what actually matters and cannot be defeated by re-spelling — rather than by scanning the
tool's source bytes.

Second, and independent of the embed axis: `cases_pass=0/33` is reported here, but the
registration's own "why a shortcut control cannot meet it" paragraph is not the only
possible reading of a fixed table. The SYNTH family is generated by the counter's own
`Gen.bind()`/`entry()` helpers, which share the counter's field template and its
`mods_str` ordering rule. A tool that reimplements *the counter's model* of Hyprland
rather than Hyprland would be rewarded on SYNTH for resembling the generator. My stub does
not benefit from this — it scores 0 on SYNTH too, because the SYNTH keys and arg tokens are
random per run — but a reader should not treat the SYNTH sub-score as independent
corroboration of Hyprland fidelity. The smallest safe correction is that the after-run
receipt report the SYNTH sub-score and the 28 non-SYNTH sub-score separately, so that
agreement carried by the perturbation families can be distinguished from agreement carried
by the synthetic families alone.

Third, a factual point about the counter's own stability, which the wave should know
regardless of what any control concludes: the counter anchors the BASE case to the **live**
`hyprctl binds -j` capture, while the tool under test reads **only** config bytes. Those
two agree only if the compositor's in-memory bind table is exactly what the config tree
would produce. On this host they do agree right now — I counted 192 `bind` lines in the
40-file source closure of the four roots, matching the live table's 192 binds, and every
live `arg` and `description` string is present verbatim in the roots (0 of 192 missing) —
but the compositor was started on 2026-10-22 04:55 and the newest config mtime is
2026-10-17 17:05, so the agreement is currently a consequence of the operator not having
edited a config since the last compositor start, not of anything the counter checks. If a
bind is edited without a compositor reload, the live capture keeps the old table and the
snapshot keeps the new bytes, and the BASE case becomes unsatisfiable by *any* correct
tool. The counter's `UNSTABLE` guard only detects the capture changing *during* the
snapshot copy (two captures seconds apart), not the capture being stale relative to the
files. The smallest safe correction, if the canonical judge wants one, is for the
after-run receipt to record a staleness check — the newest mtime across the four roots
versus the compositor's start time — so that a future BASE failure can be attributed
between "the tool is wrong" and "the live capture was already stale".

Fourth, a note on the sequencing, recorded because it bears on the receipt's evidential
weight rather than on the score: the counter was **mutated in place mid-round** (frozen v1
→ v2, adding the REWRITE family) while this control wave was in flight, and
`registration.md` was edited in the same window. This seat's scored run predates the
mutation by roughly two minutes and used the frozen v1 bytes, which the counter's own
self-reported sha256 on stdout proves; the frozen bytes were also preserved as
`count-v1.py` by the mutating seat, so the scored run remains reproducible. What the wave
should take from this is narrower than it may first appear: the *frozen* counter named in
`registration.md` is not the counter that will exist when the data seat is measured, so a
`TARGET_MET` measured against v2 is not the same claim as a `TARGET_MET` measured against
the frozen sha256 the registration cites, and the registration should say which sha256 the
after-run is measured against. If v2 is the intended frozen counter, the registration's
`PRED-C1` sentence needs its case count and target updated to match (37 and 37/37), and
this receipt's frozen-v1 result should be read as the control result *against the counter
as first frozen*, with the v2 supplementary run as the result against the counter as
presently frozen.

Finally, the smallest correction for this seat's own artefacts, if the canonical judge
wants one: the receipt's NO-READER proof rests on a `strace` invocation whose shape mirrors
the counter's `bwrap` command line but is not literally the counter's command line (the
counter's `run_tool` does not include `strace`). That is adequate for the property being
witnessed — that the stub performs no filesystem access under the case HOME — because the
sandbox's `--ro-bind home /snap/home` and `--clearenv --setenv HOME /snap/home` are what
make the case tree reachable at all, and the traced run reproduced those exactly. But a
reader who wants the strongest form should re-run the counter with `strace` interposed
around the tool and read the trace of the *counter's own* invocation, rather than
trusting a mirror of it.

CONTROL CtlNoReader: not met
