# K4ShellOut independent re-measure and receipt attack

REMEASURE K4ShellOut: 0/41 (receipt said 0/41); strengthened: 0/41 — not met

## Scope, identity, and axes

Read the round-25 registration's Attempt 3 / PRED-C1 (v4), the committed control and receipt, the frozen v4 counter, and the imported sandbox runner. The only lane write for this review is this report. The only control write is `/fast/scratch/hyaku/mado-r25a3/rm/K4ShellOut-strong.py`. No lane tool, counter, registration, receipt, host config, package, service, or git/jj state was changed. No subagent or other judgment runtime was invoked; these are the requested counter measurements, not an admission decision.

Axes: C1 operability / exact 18-field fidelity; oracle independence and shortcut rejection; calibration / output provenance; host safety / isolation.

Command (lane cwd):

```sh
timeout 15 sha256sum .ufo/waves/round-25/controls/v4/K4ShellOut.py .ufo/waves/round-25/c1/count.py .ufo/waves/round-25/c1/count-v3.py
```

Observed:

```text
d41e395c1f5db6207ee006e2e5df4d8d431c35b40869ca418b4ae60016848d53  .ufo/waves/round-25/controls/v4/K4ShellOut.py
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  .ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  .ufo/waves/round-25/c1/count-v3.py
```

The control hash exactly matches `controls/v4/K4ShellOut.md:14` and both original scored receipt identities. The counter and generator also match their frozen pins. The original receipt says 0/41, embed_hits=0, exit=1 on two fresh seeds. This review performed one new scored run of those unchanged control bytes at `459dd17f8fd60df85b25f15e69376a9765e267d3`, without `--seed`.

## Independent committed-control receipt

Exact executed command, lane cwd:

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 prlimit --as=4000000000 --core=0 timeout 1200 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4ShellOut.py
```

`-B` only prevents lane bytecode writes; the environment prefix repairs host-side live capture, and bubblewrap still clears the tool environment. A prior asynchronous dispatch was refused by the tool's background-job cap before execution; it produced no seed or counter receipt and is not a second score. The actual run completed in 117.65 s. Full tool receipt: `artifact://8195` (includes the tool wrapper's elapsed-time/exit footer). Counter stdout, verbatim, with the observed exit appended:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4ShellOut.py sha256:d41e395c1f5db6207ee006e2e5df4d8d431c35b40869ca418b4ae60016848d53
seed=bc2e9d3f88f242d2
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=192 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=190 extra=0 oracle_binds=190 (UNBIND mask=0 key='F9' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=65 key='' keycode=10) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=69 key='R' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=68 key='A' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vqfehgqk) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-1   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vutgwjme) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-2   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vvnurmfo) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-3   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vemvmjql) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-0     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 19) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-1     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 29) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 20) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-3     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 17) v3_model=agree
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
CASE COMMENT-0    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-1    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=13 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
    missing mask=1 key="KP_9" code=0 disp="exec" arg="true l1d91ox8ej"
    missing mask=73 key="F19" code=0 disp="exec" arg="printf gha92usumg"
CASE SYNTH-1      FAIL missing=16 extra=0 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=2) v3_model=agree
    missing mask=77 key="F24" code=0 disp="exec" arg="notify-send x3010knof8"
    missing mask=77 key="DELETE" code=0 disp="exec" arg="printf ir8z0ylh5l"
CASE SYNTH-2      FAIL missing=13 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
    missing mask=1 key="F6" code=0 disp="exec" arg="true omp1gs3f2t"
    missing mask=65 key="F19" code=0 disp="exec" arg="printf ybclc5kdz4"
CASE SYNTH-3      FAIL missing=13 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
    missing mask=77 key="COMMA" code=0 disp="exec" arg="printf zvo5x79104"
    missing mask=12 key="END" code=0 disp="exec" arg="notify-send irnpl48zgq"
CASE REWRITE-0    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='E' code=0; unbind mask=65 key='' code=19; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-1    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=68 key='A' code=0; unbind mask=68 key='F' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-2    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=0 key='XF86AudioPlay' code=0; unbind mask=64 key='' code=15; add movecurrentworkspacetomonitor) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-3    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='X' code=0; unbind mask=68 key='LEFT' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE HARD-0       FAIL missing=20 extra=0 oracle_binds=20 (HARD tree lines=30 binds=20 unbinds=1 vars=4) v3_model=agree
    missing mask=1 key="F8" code=0 disp="resizeactive" arg="-60 -4"
    missing mask=73 key="F8" code=0 disp="pseudo" arg=""
CASE HARD-1       FAIL missing=25 extra=0 oracle_binds=25 (HARD tree lines=33 binds=25 unbinds=3 vars=4) v3_model=agree
    missing mask=68 key="mouse_down" code=0 disp="pseudo" arg=""
    missing mask=72 key="" code=158 disp="togglespecialworkspace" arg="sgln"
CASE HARD-2       FAIL missing=23 extra=0 oracle_binds=23 (HARD tree lines=30 binds=23 unbinds=1 vars=4) v3_model=agree
    missing mask=68 key="" code=42 disp="cyclenext" arg="67r2"
    missing mask=64 key="mouse:273" code=0 disp="mouse" arg="resizewindow"
CASE HARD-3       FAIL missing=19 extra=0 oracle_binds=19 (HARD tree lines=28 binds=19 unbinds=1 vars=4) v3_model=agree
    missing mask=69 key="" code=224 disp="moveoutofgroup" arg=""
    missing mask=72 key="F17" code=0 disp="swapwindow" arg="l"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

## Receipt attack: genuine shape, but one fixable provenance defect

The committed file genuinely implements the named shell-out shape rather than the claimed static work. Its only config transformation is copying bytes and removing startup exec-keyword lines; it appends non-bind ecosystem/debug settings and leaves source traversal, variables, bind grammar, rejected lines, and unbind semantics to Hyprland. Its ten modes cover missing/private runtime, headless/software/backend environment guesses, and `--verify-config`. It tries both explicit-instance hyprctl and direct `j/binds` on sockets under a newly private runtime. It contains no static resolver, embedded table, or fixture/label lookup. This is not a do-nothing control merely renamed shell-out.

**Counterexample actually tested:** `from_log()` does not require a table export. It can manufacture a one-row table from a JSON-shaped object embedded in unrelated diagnostic prose. Its field-name test cannot distinguish an echoed config value from a bind-export record. The original receipt's statement that a complete table must actually come from the child's log is therefore too weak to establish the provenance of individual recovered rows.

Exact import-only probe (no compositor started):

```sh
prlimit --as=1000000000 --core=0 timeout 10 python3 -I -B -c 'import importlib.util,json
p="/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4ShellOut.py"
s=importlib.util.spec_from_file_location("k4_probe",p)
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)
row={k:False for k in m.FIELDS}
row.update(modmask=0,key="A",keycode=0,submap="",description="",dispatcher="exec",arg="true")
text="Config error: echoed value, not a table export: "+json.dumps(row)
value=m.from_log(text)
print("FORGED_LOG_ACCEPTED="+str(value==[row]))
print("parsed_rows="+str(len(value or [])))
'
```

Observed:

```text
FORGED_LOG_ACCEPTED=True
parsed_rows=1
exit=0
```

This was an artificial log-string probe, not a real Hyprland log and not a demonstrated generated-case or scorer exploit. [INFERENCE] A diagnostic echo of a suitably shaped input could trigger the same helper behavior; that actual echo route was not exercised. The independent 0/41 result offers no evidence that the flaw affected the original score. Fresh-case exact comparison would still reject the fabricated row unless it matched the entire expected multiset.

**Smallest safe correction:** do not infer a bind table from arbitrary log substrings/individual objects. Use only the private child IPC response for the installed CLI, and keep diagnostic logs diagnostic. This improves provenance without implementing any static grammar or granting access to a host compositor. The scratch strengthened version makes this correction, requires exactly the 18 fields, and waits for three identical private-IPC replies rather than accepting the first response. The stability change is defensive; no startup-race failure was demonstrated here. All ten original startup modes, isolation guards, exec stripping, resource limits, deadlines, and group cleanup remain. This is provenance-strengthening, not a claim of a newly working backend route.

## Strongest contrary route and unavoidable boundary

The receipt already correctly disclaims exclusion of every conceivable executable use. I checked the installed CLI with:

```sh
prlimit --as=1000000000 --core=0 timeout 10 Hyprland --help
```

It advertises `--verify-config` as “Do not run Hyprland, only print if the config has any errors”; no bind-export option is advertised. I also opened the pinned sources, separately from the runtime measurement:

- [Hyprland v0.56.2 Compositor.cpp](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/Compositor.cpp): `initServer()`'s verification branch creates the keybind/config managers, prints `Config::mgr()->verify()`, and returns before backend / late IPC initialization. Normal startup explicitly requests HEADLESS, optional DRM, and fallback WAYLAND, and requires the backend before `STAGE_LATE` creates CHyprCtl. The source does not select a NULL/X11 backend merely because those guessed environment variables are present.
- [Legacy ConfigManager.cpp](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp): `verify()` returns the parsing error or `config ok`; `handleBind()` calls `addKeybind()` but does not emit the table.
- [KeybindManager.cpp](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp): `addKeybind()` stores the entry and returns it without a complete JSON/table log. Thus ordinary verbose-log decoding is not an evidenced missing exporter.

`--verify-config` is the strongest counterexample to saying the sandbox prevents all Hyprland parsing: it can parse without the renderer. It is not an evidenced route to all 18 output fields. The prior receipt's allocator/backend failure explains why the normal socket routes never answer; that diagnostic was not rerun separately here. The new counter run independently measured all 41 cases as missing every oracle bind with zero extras.

No score-strengthening backend/export route was found within the installed single-file shell-out shape. Giving it `/run`, the host display socket or GPU devices would change the predicate and host-safety boundary; adding a static bind parser would perform the very work this control must skip. Those are not safe corrections to this control. Neither two prior seeds nor these fresh measurements prove universal shell-out impossibility or justify saturation.

## Strengthened-control receipt

Exact executed command, lane cwd:

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 prlimit --as=4000000000 --core=0 timeout 1200 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /fast/scratch/hyaku/mado-r25a3/rm/K4ShellOut-strong.py
```

One fresh seed, no replay or miss-until-pass loop. Counter stdout, verbatim, with observed exit appended:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r25a3/rm/K4ShellOut-strong.py sha256:02eb41a4de09414b3ac50ed41dffc4788d6b3500d89a362bf18b5972056c1a52
seed=44fed51a4562b253
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=192 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=64 key='TAB' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=64 key='' keycode=18) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=65 key='Y' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=72 key='' keycode=13) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vxqtxhsr) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-1   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vxenyrzc) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-2   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vhlcjeph) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-3   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vufxfhur) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-0     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-1     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 10) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 29) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-3     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 23) v3_model=agree
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
CASE COMMENT-2    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=14 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
    missing mask=5 key="LEFT" code=0 disp="exec" arg="notify-send w7ph75abkc"
    missing mask=69 key="F1" code=0 disp="exec" arg="x8qwjbw9n 0gyk"
CASE SYNTH-1      FAIL missing=15 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=3) v3_model=agree
    missing mask=5 key="J" code=0 disp="exec" arg="notify-send av8jfkzvd6"
    missing mask=68 key="END" code=0 disp="exec" arg="notify-send nmfpoxwaof"
CASE SYNTH-2      FAIL missing=14 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
    missing mask=69 key="F18" code=0 disp="exec" arg="true 9vohw2qtjp"
    missing mask=4 key="F5" code=0 disp="exec" arg="logger d69bt0sub1"
CASE SYNTH-3      FAIL missing=15 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=3) v3_model=agree
    missing mask=9 key="2" code=0 disp="exec" arg="true un3m66gori"
    missing mask=13 key="PRINT" code=0 disp="exec" arg="true aqeqmpdhr2"
CASE REWRITE-0    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='F' code=0; unbind mask=64 key='RETURN' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-1    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='' code=18; unbind mask=65 key='SLASH' code=0; add workspace) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-2    FAIL missing=191 extra=0 oracle_binds=191 (REWRITE argswap mask=65 key='' code=16; unbind mask=8 key='TAB' code=0; add fullscreenstate) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-3    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='XF86AudioMute' code=0; unbind mask=65 key='N' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE HARD-0       FAIL missing=18 extra=0 oracle_binds=18 (HARD tree lines=27 binds=18 unbinds=2 vars=4) v3_model=agree
    missing mask=64 key="" code=60 disp="focusmonitor" arg="d"
    missing mask=0 key="3" code=0 disp="layoutmsg" arg="q9e2"
CASE HARD-1       FAIL missing=20 extra=0 oracle_binds=20 (HARD tree lines=27 binds=20 unbinds=3 vars=4) v3_model=agree
    missing mask=64 key="" code=75 disp="movefocus" arg="l"
    missing mask=65 key="9" code=0 disp="sendshortcut" arg="Shift, U, activewindow"
CASE HARD-2       FAIL missing=19 extra=0 oracle_binds=19 (HARD tree lines=29 binds=19 unbinds=3 vars=4) v3_model=agree
    missing mask=76 key="M" code=0 disp="togglespecialworkspace" arg=""
    missing mask=65 key="DOWN" code=0 disp="movefocus" arg="d"
CASE HARD-3       FAIL missing=23 extra=0 oracle_binds=23 (HARD tree lines=31 binds=23 unbinds=2 vars=4) v3_model=agree
    missing mask=73 key="" code=236 disp="changegroupactive" arg=""
    missing mask=4 key="mouse:272" code=0 disp="mouse" arg="resizewindow"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

The strengthened run completed in 140.35 s; full tool receipt `artifact://8894`. Its measured sha256 is `02eb41a4de09414b3ac50ed41dffc4788d6b3500d89a362bf18b5972056c1a52`. Both runs had `ORACLE_CHECK base_vs_live missing=0 extra=0`, `embed_hits=0`, and `V3_MODEL_AGREE 41/41` (diagnostic only). Neither met the predicate. No score gain is claimed for the provenance correction.

## Impact and scoped disposition

- C1 operability / fidelity: unchanged at 0/41 for both measured controls. The requested static capability is not supplied by these shell-out routes.
- Oracle independence / shortcut rejection: no measured escape of the isolation boundary and no successful shortcut. Do not turn this into a universal impossibility claim.
- Calibration / provenance: the log helper's synthetic-object acceptance is a demonstrated local defect, not an observed source of a false passing receipt. The scratch version removes it without adding the forbidden resolver work.
- Safety: all commands were bounded; score commands inherited a 4 GB address-space cap and zero-core limit. Hyprland was not launched separately from the prescribed counter invocations (the separate CLI call was `--help`). The counter owns nested process-group cleanup; no independent process-inventory verification is claimed. No live compositor write verb or host config/service/package change was used.

Read the operator tooling rules. Installs/updates: none. Checks exercised: hash comparison, one fresh committed-control measurement, one import-only provenance probe, installed CLI help, pinned-source inspection, and one fresh strengthened-control measurement. No unrun check is represented as passed.

REMEASURE K4ShellOut: 0/41 (receipt said 0/41); strengthened: 0/41 — not met
