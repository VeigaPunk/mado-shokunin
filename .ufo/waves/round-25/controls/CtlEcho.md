# CtlEcho — round 25 C1 control receipt (shape: SERVER ECHO)

Seat: `MadoR25.CtlEcho`. Lane base REV `04051723562b8a6ac1f3a9ae05e861aa6f544aff`. Frozen counter read but not edited:
`sha256:70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895`. Registration not edited. No installs, no
package transactions, no writes outside this receipt, its `.py` twin, and `/fast/scratch/hyaku/mado-r25/controls/MadoR25.CtlEcho9/`.

## Shape

Skip the real work — a static Hyprland bind-table resolver — entirely; instead ask the running compositor for its own
table and return that. Cheapest possible program of that shape: no config parsing, no source/graph walk, no variable
expansion, no unbind semantics, no `--home` use.

## What the stub does (and skips)

1. `hyprctl binds -j` (read verb) via `subprocess`; if exit 0 and the stdout parses as a JSON list, print it and exit 0.
2. Else glob `$XDG_RUNTIME_DIR/hypr/*/.socket.sock` and `/run/user/*/hypr/*/.socket.sock`, AF_UNIX-connect to the first
   that accepts, send `j/binds`, read to EOF; if that parses as a JSON list, print it and exit 0.
3. Else print `[]` and exit 0 (so the counter records per-case mismatches rather than a hard error).

Skipped: everything the claim is about. The stub never opens `DIR/.config/hypr/hyprland.conf`; `--home` is accepted and
discarded. It follows no `source =`, expands no globs, resolves no `$variable`, applies no `unbind`, ignores comments and
never reads the four Hyprland config roots.

Stub bytes: `sha256:e9ef07b8aca630a30fb8c013c86124bd3479baf81f57948d4c73312d1ea7c1d3` (2123 bytes). Byte-exact twin at
`.ufo/waves/round-25/controls/CtlEcho.py`. It contains no live arg/description string of any length, so it cannot trip
`embed_hits` — the miss below is not an embedding artifact.

## Exact command

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && timeout 900 python3 -I .ufo/waves/round-25/c1/count.py 04051723562b8a6ac1f3a9ae05e861aa6f544aff --tool-file /fast/scratch/hyaku/mado-r25/controls/MadoR25.CtlEcho9/stub.py
```

First (measurement) run used the fresh seed `67b3543765193809` that the counter printed. The block below is that run
replayed with `--seed 67b3543765193809` and captured verbatim to
`/fast/scratch/hyaku/mado-r25/controls/MadoR25.CtlEcho9/counter-stdout.txt`
(`sha256:774d32d9af06ea3b9aaae59d49be54b24f0cfe5e1e877338d004b287fd194681`, 105 lines, 33 `CASE` lines); header lines
(`live=` sha, `snapshot files=79` digest, `live_binds=192`) are identical to the measurement run, i.e. the replay
reproduced it, and both runs exited 1 with the same verdict.

## Counter provenance (unchanged; read, never edited)

```
$ sha256sum .ufo/waves/round-25/c1/count.py .ufo/waves/round-25/registration.md
70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895  .ufo/waves/round-25/c1/count.py
a0afab65428112e7ef1b118bed3889491ed0de6729eeb2ae955c1f485f5695e5  .ufo/waves/round-25/registration.md
```

The counter's own first line prints the same `count.py` hash, so the bytes scored are the bytes registered.

## Complete counter stdout

```
counter sha256:70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895 rev=04051723562b8a6ac1f3a9ae05e861aa6f544aff
tool=override:/fast/scratch/hyaku/mado-r25/controls/MadoR25.CtlEcho9/stub.py sha256:e9ef07b8aca630a30fb8c013c86124bd3479baf81f57948d4c73312d1ea7c1d3
seed=67b3543765193809
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
CASE BASE         FAIL missing=192 extra=0 (unperturbed)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 (UNBIND mask=64 key='' keycode=11)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=191 extra=0 (UNBIND mask=0 key='XF86KbdBrightnessDown' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 (UNBIND mask=64 key='TAB' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 (UNBIND mask=0 key='XF86Calculator' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=0 (VARIABLE $vvpnbwlu)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-1   FAIL missing=193 extra=0 (VARIABLE $vbvyvyud)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-2   FAIL missing=193 extra=0 (VARIABLE $vnttrhrl)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-3   FAIL missing=193 extra=0 (VARIABLE $vziuvzmv)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-0     FAIL missing=194 extra=0 (SOURCE new file at root line 4)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-1     FAIL missing=194 extra=0 (SOURCE new file at root line 5)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 (SOURCE new file at root line 4)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-3     FAIL missing=194 extra=0 (SOURCE new file at root line 19)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-0       FAIL missing=193 extra=0 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-1       FAIL missing=193 extra=0 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-2       FAIL missing=193 extra=0 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-3       FAIL missing=193 extra=0 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-0  FAIL missing=192 extra=0 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-1  FAIL missing=192 extra=0 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-2  FAIL missing=192 extra=0 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-3  FAIL missing=192 extra=0 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-0    FAIL missing=193 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-1    FAIL missing=193 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=15 extra=0 (SYNTH tree binds=15 unbound=1 vars=3)
    missing mask=77 key="L" code=0 disp="exec" arg="wjxt1nkod uel4"
    missing mask=65 key="F6" code=0 disp="exec" arg="wjxt1nkod meo9"
CASE SYNTH-1      FAIL missing=13 extra=0 (SYNTH tree binds=13 unbound=1 vars=2)
    missing mask=68 key="EQUAL" code=0 disp="exec" arg="notify-send iegtha3hlz"
    missing mask=5 key="F8" code=0 disp="exec" arg="mvk0tjc33 95l1"
CASE SYNTH-2      FAIL missing=14 extra=0 (SYNTH tree binds=14 unbound=1 vars=2)
    missing mask=64 key="F3" code=0 disp="exec" arg="printf aptj3i9hqa"
    missing mask=13 key="F4" code=0 disp="exec" arg="true p21lu2egnk"
CASE SYNTH-3      FAIL missing=15 extra=0 (SYNTH tree binds=15 unbound=1 vars=2)
    missing mask=8 key="F9" code=0 disp="exec" arg="rat9w1n6q gjfz"
    missing mask=1 key="S" code=0 disp="exec" arg="my2n88lly 0kaw"
PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED
```

Exit code: **1**.

Final line: `PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED`

CONTROL CtlEcho: not met

## Why it returns nothing in the sandbox (diagnosed, not assumed)

The counter's `run_tool` uses `bwrap … --unshare-all --clearenv --setenv PATH /usr/bin --setenv HOME /snap/home`, binds
`/usr` read-only plus a tmpfs `/tmp` and a fresh `/dev` and `/proc`, and **nothing under `/run`**. Running the same bwrap
argument list on a read-only probe:

```
rc 1
stdout_head b'HYPRLAND_INSTANCE_SIGNATURE not set! (is hyprland running?)\n\n'
stderr
XDG_RUNTIME_DIR None
HYPRLAND_INSTANCE_SIGNATURE None
run_user []
sockets []
```

So step 1 fails (`hyprctl` exits 1: no `HYPRLAND_INSTANCE_SIGNATURE`, and no socket to find even with one), and step 2's
globs see an empty `/run/user/*` and an unset `XDG_RUNTIME_DIR`; the stub therefore emits `[]` for every case. Every case
then shows `missing=<size of expected multiset>` and `extra=0`, i.e. the empty answer, not a wrong table. The
`--unshare-all` network namespace additionally blocks any TCP route to the compositor.

## Host run, outside the counter (echo works when the sandbox does not block it)

```
cd /fast/scratch/hyaku/mado-r25/controls/MadoR25.CtlEcho9 && timeout 60 python3 -I stub.py --home "$HOME"
```

exit 0, stdout 76203 bytes = a JSON array of **192** entries (saved at `host-out.json` in that scratch dir). Compared
against a fresh `hyprctl binds -j`:

```
host_stub_entries 192 hyprctl_entries 192 identical_json True
```

So the echo shape is sound on the live host and dies exactly at the sandbox boundary: the table it returns is
byte-for-byte the compositor's own, and that table carries none of the per-run perturbations the counter writes into the
`--home` snapshot.

## Verdict

The cheapest SERVER ECHO program does not come close: 0/33 cases, exit 1, `TARGET_MISSED`. Two independent reasons, both
structural rather than fixable-in-the-stub: (a) the sandbox has no compositor socket, so the echo is empty; (b) even with
a socket the answer is the live table, which is wrong for all 32 perturbed cases (in SYNTH the snapshot is deleted
outright, so the live table is irrelevant by construction). A stub that also read `/snap/home` would no longer be an
echo; that is the real resolver the claim asks for.

---

## Critique (not part of the score)

1. **The echo route is closed by accident, not by an assertion.** `embed_hits` plus the perturbation deltas are what the
   registration cites against an echo, but the binding constraint here is `--unshare-all` and the absence of a `/run`
   bind. If a later counter revision binds `/run/user/$UID` (a plausible convenience for a "no network" sandbox), an
   echo stub would still score 1/33 (BASE only). The claim's blocking power survives, but for a different reason than
   the registration says; the registration sentence "cannot reach a socket inside the sandbox" should be read as
   sandbox-policy-dependent, and it is worth recording that BASE alone being passable by an echo is harmless.
2. **`embed_hits` is a substring filter over literals ≥12 characters, not an anti-embedding check.** A tool that embeds
   the live table with each `arg`/`description` split across adjacent string literals (`"omarchy-swayosd-" "client …"`)
   scores `embed_hits=0`. That path is still killed by the 32 perturbed cases (random keys/mods/args per run, and SYNTH
   has no live binds at all), so the miss is over-determined — but the number `embed_hits=0` in a receipt must not be
   read as "no table was copied in". The safe correction (if this counter is ever reused) is to compare a normalised
   token stream or to score embedding as part of the case set rather than as a separate scalar; no change is needed for
   this round's claim, whose kill surface is the perturbation cases.
3. **`UNSOURCED` and `BASE` are the same expectation.** The control prints `UNSOURCED-*` with `missing=192`, identical to
   `BASE`, so 4 of 33 cases carry no discrimination against any stub that gets BASE right — by design (they test that
   the resolver doesn't over-read), but it means the effective discrimination budget is 29 cases, not 33. Not a defect;
   worth stating when 33/33 is cited as the bar.
4. **Nothing else to attack from this seat.** My stub never parses config, so I have no evidence for or against the
   resolver's own hazard surface (variable expansion order, `unbind` of a keycode target, glob ordering, comment
   stripping), which round 24's lessons already flagged as the hard parts. The counter's expected multisets for those
   cases are asserted, not independently derived here; a data seat still has to earn them.
