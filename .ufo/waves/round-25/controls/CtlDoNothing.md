# CtlDoNothing — round-25 C1 pre-data control (DO-NOTHING shape)

Control seat: `MadoR25.CtlDoNothing`. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`
(jj-colocated, branch `master`, tip `04051723562b8a6ac1f3a9ae05e861aa6f544aff`).
Base revision: `41cc04c8d593837a0d5078bffaacdaa163d12897`.

## Shape

DO-NOTHING. No resolver was written. The counter was run exactly as frozen, without
`--tool-file`, so it measured the committed bytes of `tools/mado-binds.py` at each
revision — which do not exist at either revision — and therefore reported
`tool=MISSING_TOOL` and failed every case with `tool absent`.

## What the stub does and skips

There is no stub file for this seat, by assignment. The "stub" for a do-nothing control
is the empty program: no `--tool-file` was passed, so the counter took the `git show
REV:tools/mado-binds.py` path, the path lookup failed at both revisions, and the counter
short-circuited every case with `FAIL tool absent`.

Skipped, exactly as the registration's "why a do-nothing or shortcut control cannot meet
it" paragraph claims for the absent-tool case:

- the faithful Hyprland bind-table resolver (config-bytes parse of `~/.config/hypr/**`
  plus sourced files, `source =` glob following, `$var` expansion, `unbind =` handling,
  comment stripping per hyprlang v0.6.8, and emission of the 18 `hyprctl binds -j`
  fields with `modmask`/`keycode`/`catch_all` semantics per Hyprland v0.56.2) — none of
  it exists at these revisions;
- the sandbox execution of any tool inside bubblewrap (the counter never reached
  `run_tool`, so `bwrap` was never invoked for this seat);
- the `embed_hits` check on tool bytes (reported as `embed_hits=0` because there are no
  tool bytes to scan — a vacuous zero, not a demonstrated property).

Nothing on the host was modified: no config file, no compositor state, no service. The
only host reads were `hyprctl binds -j` (read verb, invoked by the counter itself) and
read-only reads of the four config roots under `$HOME`. No `hyprctl dispatch`, `keyword`,
`reload`, or any other write verb was used.

## Counter provenance (unchanged before and after both runs)

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && sha256sum .ufo/waves/round-25/c1/count.py
```

Exit 0, before both runs and again after both runs:

```text
70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895  .ufo/waves/round-25/c1/count.py
```

This equals the sha256 named in `registration.md` for the frozen counter. The counter
was neither edited nor re-versioned by this seat.

## Run 1 — registration revision, do-nothing

Exact command:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && timeout 900 env -u MADO_LANE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 -I .ufo/waves/round-25/c1/count.py 04051723562b8a6ac1f3a9ae05e861aa6f544aff
```

Complete counter stdout, verbatim:

```text
counter sha256:70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895 rev=04051723562b8a6ac1f3a9ae05e861aa6f544aff
tool=MISSING_TOOL at 04051723562b8a6ac1f3a9ae05e861aa6f544aff
seed=0c2e7eea218318f5
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
CASE BASE         FAIL tool absent (unperturbed)
CASE ADD-0        FAIL tool absent (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
CASE ADD-1        FAIL tool absent (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
CASE ADD-2        FAIL tool absent (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf)
CASE ADD-3        FAIL tool absent (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf)
CASE UNBIND-0     FAIL tool absent (UNBIND mask=64 key='' keycode=20)
CASE UNBIND-1     FAIL tool absent (UNBIND mask=65 key='' keycode=12)
CASE UNBIND-2     FAIL tool absent (UNBIND mask=73 key='' keycode=16)
CASE UNBIND-3     FAIL tool absent (UNBIND mask=8 key='PRINT' keycode=0)
CASE VARIABLE-0   FAIL tool absent (VARIABLE $vvdbaxeg)
CASE VARIABLE-1   FAIL tool absent (VARIABLE $vbkaopzz)
CASE VARIABLE-2   FAIL tool absent (VARIABLE $vrnyefbs)
CASE VARIABLE-3   FAIL tool absent (VARIABLE $vdupthdh)
CASE SOURCE-0     FAIL tool absent (SOURCE new file at root line 16)
CASE SOURCE-1     FAIL tool absent (SOURCE new file at root line 11)
CASE SOURCE-2     FAIL tool absent (SOURCE new file at root line 9)
CASE SOURCE-3     FAIL tool absent (SOURCE new file at root line 12)
CASE GLOB-0       FAIL tool absent (GLOB new toggles file)
CASE GLOB-1       FAIL tool absent (GLOB new toggles file)
CASE GLOB-2       FAIL tool absent (GLOB new toggles file)
CASE GLOB-3       FAIL tool absent (GLOB new toggles file)
CASE UNSOURCED-0  FAIL tool absent (UNSOURCED new bindings file)
CASE UNSOURCED-1  FAIL tool absent (UNSOURCED new bindings file)
CASE UNSOURCED-2  FAIL tool absent (UNSOURCED new bindings file)
CASE UNSOURCED-3  FAIL tool absent (UNSOURCED new bindings file)
CASE COMMENT-0    FAIL tool absent (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
CASE COMMENT-1    FAIL tool absent (COMMENT into .config/hypr/bindings.conf)
CASE COMMENT-2    FAIL tool absent (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf)
CASE COMMENT-3    FAIL tool absent (COMMENT into .config/hypr/bindings.conf)
CASE SYNTH-0      FAIL tool absent (SYNTH tree binds=15 unbound=1 vars=2)
CASE SYNTH-1      FAIL tool absent (SYNTH tree binds=12 unbound=1 vars=2)
CASE SYNTH-2      FAIL tool absent (SYNTH tree binds=16 unbound=1 vars=3)
CASE SYNTH-3      FAIL tool absent (SYNTH tree binds=10 unbound=1 vars=3)
PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED
```

stderr: empty. Exit code: **1**.

Final `PRED-C1` line:

```text
PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED
```

## Run 2 — base revision, do-nothing

Exact command:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && timeout 900 env -u MADO_LANE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 -I .ufo/waves/round-25/c1/count.py 41cc04c8d593837a0d5078bffaacdaa163d12897
```

Complete counter stdout, verbatim:

```text
counter sha256:70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895 rev=41cc04c8d593837a0d5078bffaacdaa163d12897
tool=MISSING_TOOL at 41cc04c8d593837a0d5078bffaacdaa163d12897
seed=f8b149d72606879d
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
CASE BASE         FAIL tool absent (unperturbed)
CASE ADD-0        FAIL tool absent (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
CASE ADD-1        FAIL tool absent (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
CASE ADD-2        FAIL tool absent (ADD into .config/hypr/bindings.conf)
CASE ADD-3        FAIL tool absent (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
CASE UNBIND-0     FAIL tool absent (UNBIND mask=64 key='' keycode=14)
CASE UNBIND-1     FAIL tool absent (UNBIND mask=64 key='K' keycode=0)
CASE UNBIND-2     FAIL tool absent (UNBIND mask=73 key='G' keycode=0)
CASE UNBIND-3     FAIL tool absent (UNBIND mask=68 key='BACKSPACE' keycode=0)
CASE VARIABLE-0   FAIL tool absent (VARIABLE $vvxikmim)
CASE VARIABLE-1   FAIL tool absent (VARIABLE $vtpsxgnz)
CASE VARIABLE-2   FAIL tool absent (VARIABLE $vjuldooo)
CASE VARIABLE-3   FAIL tool absent (VARIABLE $vkwsgujw)
CASE SOURCE-0     FAIL tool absent (SOURCE new file at root line 5)
CASE SOURCE-1     FAIL tool absent (SOURCE new file at root line 9)
CASE SOURCE-2     FAIL tool absent (SOURCE new file at root line 29)
CASE SOURCE-3     FAIL tool absent (SOURCE new file at root line 32)
CASE GLOB-0       FAIL tool absent (GLOB new toggles file)
CASE GLOB-1       FAIL tool absent (GLOB new toggles file)
CASE GLOB-2       FAIL tool absent (GLOB new toggles file)
CASE GLOB-3       FAIL tool absent (GLOB new toggles file)
CASE UNSOURCED-0  FAIL tool absent (UNSOURCED new bindings file)
CASE UNSOURCED-1  FAIL tool absent (UNSOURCED new bindings file)
CASE UNSOURCED-2  FAIL tool absent (UNSOURCED new bindings file)
CASE UNSOURCED-3  FAIL tool absent (UNSOURCED new bindings file)
CASE COMMENT-0    FAIL tool absent (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
CASE COMMENT-1    FAIL tool absent (COMMENT into .config/hypr/bindings.conf)
CASE COMMENT-2    FAIL tool absent (COMMENT into .config/hypr/bindings.conf)
CASE COMMENT-3    FAIL tool absent (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
CASE SYNTH-0      FAIL tool absent (SYNTH tree binds=15 unbound=1 vars=2)
CASE SYNTH-1      FAIL tool absent (SYNTH tree binds=16 unbound=1 vars=2)
CASE SYNTH-2      FAIL tool absent (SYNTH tree binds=10 unbound=1 vars=2)
CASE SYNTH-3      FAIL tool absent (SYNTH tree binds=14 unbound=1 vars=3)
PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED
```

stderr: empty. Exit code: **1**.

Final `PRED-C1` line:

```text
PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED
```

## Observations

- Both runs read the same live capture (`sha256:9a47199e…`) and the same snapshot
  (`79` files, digest `sha256:fe1b2d8b…`), and both saw `live_binds=192`. The live
  capture was stable across the two runs' own double-capture check (neither run exited
  2 / `UNSTABLE`), so the miss is not a stability artifact.
- The two runs differ only in the random perturbation seed, so the per-case failure
  descriptions differ (different random keys, masks, variables, source insertion points).
  The scored quantities are identical: `cases_pass=0/33`, `embed_hits=0`, exit 1.
- `embed_hits=0` here is vacuous: the counter only scans tool bytes, and there are none.
  It is not evidence that an embed-free implementation is hard.
- Cross-check, read-only, on the host config tree: the source graph of
  `~/.config/hypr/hyprland.conf` reaches 40 files across the four roots and contains
  exactly 192 `bind`-family lines, matching `live_binds=192`. So the BASE case is in
  principle satisfiable from config bytes alone, and a real resolver has a reachable
  target to hit.
- No `git`/`jj` write command was run in the lane repo or the fleet repo; the only git
  invocations were read-only `rev-parse`, `show`, `log`, `status` in the lane and
  `sha256sum`/`python3` elsewhere. No scratch clone was needed because this seat
  produced no stub and no mutation.
- Tools installed or updated: none.

## Verdict

The do-nothing control does not meet the target. I did not meet it, and I do not claim
to have: `cases_pass=0/33`, `embed_hits=0`, `verdict=TARGET_MISSED`, exit 1, at both the
registration revision and the base. The absent-tool case is therefore detected by the
frozen counter as the registration states, and no hole was demonstrated by this seat.

CONTROL CtlDoNothing: not met

## Critique (not part of the score)

The counter is sound for the shape it was built to catch, but two properties of the
scoring loop deserve the canonical judge's attention, because they bound what the
after-run can prove.

First, `embed_hits` is only meaningful when a tool file exists. With `tb is None` the
counter skips the scan entirely and prints `embed_hits=0`, so the do-nothing run's
`embed_hits=0` is a vacuous zero that reads identically to a genuine clean
implementation's zero. A receipt that quotes `embed_hits=0` without also quoting
`tool=MISSING_TOOL` would be misleading; the do-nothing receipt quotes both.

Second, the perturbation families are keyed to random per-run material — random key
names, random variable names, random mask combinations, random file names — so a
shortcut implementation has no stable fixture id to key on, which is the registration's
own argument. That argument is sound, and this seat's evidence is consistent with it,
but it is also weaker than the registration implies in one respect: the SYNTH family is
generated from the counter's own `Gen.bind()` helper, which uses the same flag set
string, the same `mods_str` ordering rule, and the same `entry()` field template that
the counter uses to build the expected entries. A candidate tool that happens to
reimplement the counter's `entry()` template and `mods_str` ordering would be
*rewarded* on SYNTH for resembling the counter's generator rather than for
reproducing Hyprland v0.56.2. The SYNTH cases therefore test "does the tool agree with
the counter's model of Hyprland", which is the intent, but they cannot separate
"reproduces Hyprland" from "reproduces the counter". This is a property of the frozen
counter, not a defect in the do-nothing control, and it is not a counter change
proposal — it is a caution about how much weight the SYNTH sub-score can carry on its
own. The smallest safe correction, if the canonical judge wants it, is that the after-run
receipt should report the SYNTH sub-score and the 28 non-SYNTH sub-score separately, so
that a reviewer can see whether agreement is carried by the perturbation families or by
the synthetic families alone.

Finally, a factual note about `registration.md`: it states the before-run evidence is
`evidence/c1-before-41cc04c8.txt` with seed `0123456789abcdef`, and that file does
exist and does show `cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED` at exit 1.
This seat's independent re-run of the same base revision with a fresh seed reproduced
that result exactly, which is the expected outcome and does not contradict the filed
evidence.
