# Control CtlGrepAll — GREP-ALL SHORTCUT

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` (branch master, rev `04051723562b8a6ac1f3a9ae05e861aa6f544aff`)
Counter: `.ufo/waves/round-25/c1/count.py`, sha256 `70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895` (unmodified, frozen before data)
Stub: `/fast/scratch/hyaku/mado-r25/controls/CtlGrepAll/stub.py`, sha256 `2d6fe9f96e2b4f38be1f38efdf10d1b04edc9b572c20d14caa65a3dca8b9534d`
Copied byte-exact to `.ufo/waves/round-25/controls/CtlGrepAll.py` (same sha256).

## Shape

GREP-ALL SHORTCUT. The stub answers "what would this config tree bind" with a recursive grep
instead of a resolver:

- walks every file under the four config roots (`~/.config/hypr`,
  `~/.config/omarchy/current/theme`, `~/.local/share/omarchy/default/hypr`,
  `~/.local/state/omarchy/toggles/hypr`) — no source graph, no glob evaluation, no `~` logic;
- regex-matches every `bind*=` line, **commented-out ones included**
  (`^\s*(?:#+\s*)?bind([a-z]*)\s*=(.*)$`);
- splits the value on commas and stuffs the pieces into the 18 `hyprctl binds -j` fields;
- computes `modmask` from the mod names present in field 0 (substring test, Hyprland's own
  `stringToModMask` used as a lookup only);
- fills the flag booleans straight off the bind keyword's letter suffix (`l r e m n a o d u x c g`),
  handles `code:N` / numeric keys / `catchall`, lowercases the dispatcher, sets `submap=""`,
  `submap_universal` from `u`.

Deliberately skipped (the shortcut): source following, globbing, `unbind`, `$variable` expansion,
comment stripping (neither full-line nor trailing), quoting/device/submap handling, dispatcher
validation, duplicate-key arbitration. It is a grep, not a Hyprland v0.56.2 resolver.

## Exact command

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && timeout 900 python3 -I .ufo/waves/round-25/c1/count.py 04051723562b8a6ac1f3a9ae05e861aa6f544aff --tool-file /fast/scratch/hyaku/mado-r25/controls/CtlGrepAll/stub.py
```

Fresh seed (not replayed): `seed=4e548edf8e3c1ab5`. Live capture taken live during the run
(`live=hyprctl binds -j`, read verb only, sha256 shown below). Exit code: **1**.

## Counter stdout (complete, verbatim)

```
counter sha256:70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895 rev=04051723562b8a6ac1f3a9ae05e861aa6f544aff
tool=override:/fast/scratch/hyaku/mado-r25/controls/CtlGrepAll/stub.py sha256:2d6fe9f96e2b4f38be1f38efdf10d1b04edc9b572c20d14caa65a3dca8b9534d
seed=4e548edf8e3c1ab5
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
CASE BASE         FAIL missing=6 extra=81 (unperturbed)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-0        FAIL missing=6 extra=81 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-1        FAIL missing=6 extra=81 (ADD into .config/hypr/bindings.conf)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-2        FAIL missing=6 extra=81 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-3        FAIL missing=6 extra=81 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-0     FAIL missing=6 extra=82 (UNBIND mask=65 key='BACKSPACE' keycode=0)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-1     FAIL missing=6 extra=82 (UNBIND mask=68 key='SPACE' keycode=0)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-2     FAIL missing=6 extra=82 (UNBIND mask=68 key='BACKSPACE' keycode=0)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-3     FAIL missing=6 extra=82 (UNBIND mask=68 key='O' keycode=0)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-0   FAIL missing=7 extra=82 (VARIABLE $vinopxcb)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-1   FAIL missing=7 extra=82 (VARIABLE $vhxzknum)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-2   FAIL missing=7 extra=82 (VARIABLE $vuuvedzg)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-3   FAIL missing=7 extra=82 (VARIABLE $vvsyegvm)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-0     FAIL missing=6 extra=81 (SOURCE new file at root line 16)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-1     FAIL missing=6 extra=81 (SOURCE new file at root line 10)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-2     FAIL missing=6 extra=81 (SOURCE new file at root line 12)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-3     FAIL missing=6 extra=81 (SOURCE new file at root line 6)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE GLOB-0       FAIL missing=6 extra=81 (GLOB new toggles file)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE GLOB-1       FAIL missing=6 extra=81 (GLOB new toggles file)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE GLOB-2       FAIL missing=6 extra=81 (GLOB new toggles file)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE GLOB-3       FAIL missing=6 extra=81 (GLOB new toggles file)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNSOURCED-0  FAIL missing=6 extra=83 (UNSOURCED new bindings file)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNSOURCED-1  FAIL missing=6 extra=83 (UNSOURCED new bindings file)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNSOURCED-2  FAIL missing=6 extra=83 (UNSOURCED new bindings file)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNSOURCED-3  FAIL missing=6 extra=83 (UNSOURCED new bindings file)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE COMMENT-0    FAIL missing=7 extra=83 (COMMENT into .config/hypr/bindings.conf)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE COMMENT-1    FAIL missing=7 extra=83 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE COMMENT-2    FAIL missing=7 extra=83 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE COMMENT-3    FAIL missing=7 extra=83 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=64 key="C" code=0 disp="sendshortcut" arg="CTRL, Insert, activewindow"
    missing mask=64 key="V" code=0 disp="sendshortcut" arg="SHIFT, Insert, activewindow"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SYNTH-0      FAIL missing=12 extra=16 (SYNTH tree binds=13 unbound=1 vars=2)
    missing mask=65 key="F1" code=0 disp="exec" arg="epqktls74 krqz"
    missing mask=77 key="Z" code=0 disp="exec" arg="epqktls74 uzme"
    extra   mask=64 key="U" code=0 disp="exec" arg="true pnjt6q7e5g # 0krzu"
    extra   mask=73 key="HOME" code=0 disp="exec" arg="$sqaeijmj vwmw"
CASE SYNTH-1      FAIL missing=5 extra=9 (SYNTH tree binds=11 unbound=1 vars=3)
    missing mask=8 key="Q" code=0 disp="exec" arg="printf ey2o67a80q"
    missing mask=12 key="1" code=0 disp="exec" arg="z6pcvpo1e dgd3"
    extra   mask=72 key="R" code=0 disp="exec" arg="$smlvypbc bhp6"
    extra   mask=9 key="F20" code=0 disp="exec" arg="printf sc1cccs1hu"
CASE SYNTH-2      FAIL missing=10 extra=14 (SYNTH tree binds=13 unbound=1 vars=2)
    missing mask=65 key="F22" code=0 disp="exec" arg="true tc4cu2h55m"
    missing mask=77 key="EQUAL" code=0 disp="exec" arg="igz6leduv 8kap"
    extra   mask=69 key="F13" code=0 disp="exec" arg="$sftvsabp 4l6t"
    extra   mask=69 key="INSERT" code=0 disp="exec" arg="notify-send opkvm7rmnl # 7sbr7"
CASE SYNTH-3      FAIL missing=5 extra=9 (SYNTH tree binds=13 unbound=1 vars=2)
    missing mask=9 key="L" code=0 disp="exec" arg="dpvavloi0 qst4"
    missing mask=1 key="DELETE" code=0 disp="exec" arg="true w3jyuv6t5e"
    extra   mask=13 key="F21" code=0 disp="exec" arg="$ssewxhiw stuo"
    extra   mask=9 key="8" code=0 disp="exec" arg="$ssewxhiw t9pe"
PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED
```

Final line: `PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED`

## What the measurement says

The shortcut emits 267 entries where the live table has 192: **missing=6, extra=81** on the
unperturbed snapshot, so it fails BASE before any perturbation is applied.

- 70 of the 81 extras are grep hits in files that exist under the roots but are never sourced:
  `.local/share/omarchy/default/hypr/bindings/tiling.conf` (50),
  `.local/share/omarchy/default/hypr/bindings.conf` (10),
  `.local/share/omarchy/default/hypr/plain-bindings.conf` (10).
- The remaining 11 extras / 6 missing come from the two parse shortcuts on *sourced* files:
  trailing comments are not stripped (`bindd = SUPER, P, Pseudo window, pseudo, # dwindle`,
  `..., resizeactive, -100 0    # - key`), and args containing commas are re-joined without the
  original spacing (`sendshortcut, CTRL, Insert, activewindow` becomes `CTRL,Insert,activewindow`).
- Per-type deltas over BASE: UNBIND +1 extra (the `unbind` is ignored, the old bind survives),
  VARIABLE 7 missing / 82 extra (`$name` not expanded), COMMENT 7 missing / 83 extra (the
  commented twin becomes a bind, the trailing comment enters `arg`), UNSOURCED +2 extras
  (the unsourced file is walked anyway), SYNTH 5–12 missing / 9–16 extra (unsourced file,
  commented bind, unexpanded variables, ignored `unbind` all at once).
- SOURCE and GLOB show the same 81 extras as BASE: walking every file happens to find binds in
  newly written files whether or not they are sourced, so those two types are absorbed — that is
  exactly the ambiguity UNSOURCED exists to catch.

## Verdict

`CONTROL CtlGrepAll: not met`

## Critique (not part of the score)

The control does what it was assigned, and the registration's kill list survives, but two things
about the framing are worth attacking. First, the registration says "a grep of every bind line
under the roots fails UNSOURCED, UNBIND and COMMENT"; on this host it also fails BASE, by 81/6,
because 70 grep hits sit in three unsourced files. That is stronger than the registration claims,
and it means a 0/33 receipt alone carries almost no information: the case-level verdicts are
dominated by base-file noise, and the designed failure modes only become visible in the deltas
(+1 for UNBIND, +2 for UNSOURCED, +2 for COMMENT). If a future control of a *smarter* shape
(source following but no comment stripping) is scored, the receipt should quote the deltas, not
just the pass count, or a near-miss and a hopeless stub will read alike. Second, BASE grades the
candidate resolver against a second implementation (`hyprctl` on the running compositor), so a
BASE mismatch is indistinguishable from a tool defect; a TARGET_MET would only show that the
resolver and this particular compositor agree on these 192 binds, not that the resolver is
correct. That is acceptable for "surface unmoved", but the receipt should not be read as a
semantic proof, and no perturbed case can repair a BASE disagreement. Neither point requires
touching the counter or the registration; the smallest safe correction is a wording note in the
data round that grep-all dies at BASE on this host, plus the per-type deltas above in the
control-receipt record.
