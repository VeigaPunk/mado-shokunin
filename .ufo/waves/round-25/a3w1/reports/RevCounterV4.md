# RevCounterV4 — review of `.ufo/waves/round-25/c1/count.py` (v4)

Scope: does `count.py` v4 compute exactly the PRED-C1 (v4) sentence in `registration.md` "Attempt 3"
and its own docstring; are the guards fail-closed; can a missing/failed oracle ever count as a pass or
the tool be scored against a non-oracle truth; is the predicate meetable by a correct resolver.
Read-only review; counter run once at base `41cc04c8`.

**REVIEW v4: defects: 1 minor, fail-closed — uncaught oracle-side exceptions exit 1 instead of the
documented exit 2 (count.py:260; oracle() pre-`try` block), so a transient environment failure is
recorded as TARGET_MISSED rather than a re-runnable setup error; the predicate itself computes
exactly the sentence, and no path exists to a forged TARGET_MET.**

Pins verified: `count.py` sha256 `323a3849…342e2`, `count-v3.py` `8532d3e9…8375` (both match the
registration). Host Hyprland `0.56.2 @ efb50993` (matches pin).

## Sentence → code mapping

| Sentence element | Code | Verdict |
|---|---|---|
| Population 41 = BASE + 40 generated (10 types × 4) | `cases = [("BASE", None)] + [(t,i) for t in TYPES for i in range(PER_TYPE)]`, count.py:242; `TYPES` has ADD, UNBIND, VARIABLE, SOURCE, GLOB, UNSOURCED, COMMENT, SYNTH, REWRITE, HARD; `PER_TYPE = 4`, count-v3.py:64-65 | exact |
| All 18 hyprctl JSON fields | `FIELDS` count-v3.py:59-61 lists 18; verified live `hyprctl binds -j` emits exactly that key set (n_binds=192, live_only=[], v3_only=[]) | exact |
| Exact multiset | `key_of` = tuple of `json.dumps(e.get(f))` over FIELDS; `compare` = `collections.Counter` difference, missing/extra counts, count-v3.py:84-85,746-751 | exact |
| "bind multiset that Hyprland v0.56.2 itself builds from the same case tree" | `oracle()` starts nested `Hyprland -c root` on a copy (`copytree` → `strip_exec` → append `ORACLE_EXTRA`), waits for `hyprctl instances -j` to show its pid, reads `hyprctl -i <sig> binds -j` until 3 identical reads, kills the process group, count.py:120-166 | exact |
| "exec lines removed" | `EXEC_RE = ^\s*exec(?:r)?(?:-once|-shutdown)?\s*=` covers the 5 documented keywords (and the nonexistent `execr-shutdown`, harmless superset), count.py:57 | exact |
| "run in a bubblewrap sandbox (no network, no /run, cleared environment, HOME = a fresh case directory)" | `run_tool`: `timeout 60 bwrap --ro-bind /usr … --tmpfs /tmp --ro-bind home /snap/home --ro-bind tool /snap/tool.py --unshare-all --die-with-parent --clearenv --setenv PATH /usr/bin --setenv HOME /snap/home python3 -I /snap/tool.py --home /snap/home`; `/run` is never bound, network unshared, env cleared, HOME set, case tree read-only, count-v3.py:730-736 | exact |
| "none of the live capture's arg or description strings of 12 or more characters" | `strs` = every live arg/description with `len ≥ 12`; substring test on tool bytes decoded `errors="replace"`; `embed_hits` must be 0, count.py:233-240,295 | exact |
| "target: cases_pass=41/41 and embed_hits=0" | `met = npass == len(built) and embed_hits == 0`; exit 0 only then, count.py:295-298 | exact |

## Guards — all fail-closed before any CASE line is scored

- Pin: `load_v3()` exits 2 on sha mismatch before `main()` is imported, count.py:61-65. Verified by hashing.
- `UNSTABLE`: two `hyprctl binds -j` captures bracket the snapshot copy; difference → `die(…, 2)`, count.py:226-229.
- `ORACLE_FAIL`: any case whose oracle returned `(None, err)` → `die(…, 2)`, count.py:261-263 — checked for all 41 labels before `ORACLE_CHECK`.
- `ORACLE_DRIFT`: BASE oracle vs live capture nonzero diff → `die(…, 2)`, count.py:264-271.
- Bad REV → `die` default code 2 (count.py:200-201, count-v3.py:75-77); `hyprctl` capture failure → `die` default 2 (count-v3.py:88-94); argparse → exit 2.
- Tool absent → `tb is None` → every CASE prints FAIL, `npass=0`, TARGET_MISSED exit 1 (count.py:278-279).
- `run_tool` nonzero exit or non-JSON-array stdout → `(None, err)` → CASE FAIL (count-v3.py:737-744). A missing `bwrap` yields `timeout` exit 127 → CASE FAIL, not a crash.

## Truth-source audit (no non-oracle comparator, no pass-on-failure path)

- `exp = truth[label][0]` for every label including BASE (count.py:275); the tool is compared only via
  `compare(got, exp)` (count.py:285). The v3 model expectation is used solely for `V3_MODEL_AGREE`
  (count.py:276-277,294) — printed and labeled "diagnostic, not the predicate", matching the docstring.
- BASE's exp is the nested instance's table, not the live capture; `ORACLE_CHECK` pins it equal to
  live before scoring, so the sentence's "the same case tree" ground truth is literally enforced.
- The `data is None` test at count.py:262 means an empty but valid `[]` table is a legitimate oracle
  answer (correct for zero-bind trees), and any oracle error exits 2 before scoring — no CASE can be
  scored against a failed oracle.
- `--tool-file` only changes which bytes are measured (receipt prints path+sha256, count.py:209-210);
  truth generation is unchanged.
- The tool runs *after* all oracles complete, on the raw case tree bound read-only at `/snap/home`;
  it cannot mutate a case tree or reach any oracle socket.

## Meetable by a correct resolver

Every expected table is a pure function of case-tree bytes plus pinned Hyprland v0.56.2 semantics —
the oracle's two tree transforms (exec-line strip, `ecosystem` block append) are bind-neutral and are
disclosed inside the sentence itself. Nothing in any case type (including HARD's rejected lines,
keycodes, mouse binds, variables, comma args) depends on runtime state invisible to a static reader.
Empirically `V3_MODEL_AGREE 41/41` on the fresh seed below shows every case table consistent with the
documented v0.56.2 line model — no impossible case observed.

## Finding (minor, fail-closed)

**Uncaught oracle-side exceptions exit 1, not 2.** `truth = {label: f.result() for …}` (count.py:260)
has no `try`/`except`; any exception raised inside `oracle()` *before* its `try/finally` — `copytree`
(:124), `strip_exec` (:125), `open(root,"a")` (:129-131), `subprocess.Popen` (:137-140), `Slot` —
propagates as a traceback and Python exits 1. The docstring and registration promise exit 2 for
setup/`ORACLE_FAIL`; under the kill rule an exit-1 is a permanent miss rather than a re-runnable
failure. Direction is fail-closed (it can only mis-record a miss, never fabricate a pass). Same class:
`json.loads(raw1)` (count.py:230) if `hyprctl` returned rc 0 with malformed bytes; a raised exception
from `run_tool` (e.g., `subprocess.run` OSError). Instances inside `try` are fine: `KeyError` on
`inst["instance"]`, `ValueError` on JSON, poll timeouts — all funnel to `(None, err)` → `ORACLE_FAIL` 2.

## Residual risk (not a code defect)

- Oracle truth = the instance's answer when three consecutive `binds -j` polls (0.3 s apart) are
  identical within 30 s. A nested instance that answered before finishing its config parse would be
  frozen as a wrong truth — a false FAIL for an honest tool, or a false per-case PASS only for a
  degenerate `[]`-output tool (the whole predicate still can't be forged: `ORACLE_CHECK` pins BASE to
  the 192-bind live capture). Low probability; BASE and all 41 cases agreed with the model on this run.
- `ORACLE_DRIFT` correctly forces exit 2 if the host's live table contains binds not derivable from
  the snapshot tree (e.g., runtime-added binds) — per design, disclosed.

## Verification run (the one permitted run, REV `41cc04c8`, fresh seed, 38.89 s)

```
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=41cc04c8d593837a0d5078bffaacdaa163d12897 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=MISSING_TOOL at 41cc04c8d593837a0d5078bffaacdaa163d12897
seed=690a5d8bb8e0bd25
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL tool absent (unperturbed) v3_model=agree
CASE ADD-0        FAIL tool absent (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE ADD-1        FAIL tool absent (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-2        FAIL tool absent (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE ADD-3        FAIL tool absent (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE UNBIND-0     FAIL tool absent (UNBIND mask=65 key='M' keycode=0) v3_model=agree
CASE UNBIND-1     FAIL tool absent (UNBIND mask=0 key='XF86AudioMute' keycode=0) v3_model=agree
CASE UNBIND-2     FAIL tool absent (UNBIND mask=0 key='XF86KbdLightOnOff' keycode=0) v3_model=agree
CASE UNBIND-3     FAIL tool absent (UNBIND mask=76 key='R' keycode=0) v3_model=agree
CASE VARIABLE-0   FAIL tool absent (VARIABLE $vfhloyzr) v3_model=agree
CASE VARIABLE-1   FAIL tool absent (VARIABLE $vxzyoonf) v3_model=agree
CASE VARIABLE-2   FAIL tool absent (VARIABLE $vdlmycje) v3_model=agree
CASE VARIABLE-3   FAIL tool absent (VARIABLE $vblrjrpl) v3_model=agree
CASE SOURCE-0     FAIL tool absent (SOURCE new file at root line 17) v3_model=agree
CASE SOURCE-1     FAIL tool absent (SOURCE new file at root line 20) v3_model=agree
CASE SOURCE-2     FAIL tool absent (SOURCE new file at root line 32) v3_model=agree
CASE SOURCE-3     FAIL tool absent (SOURCE new file at root line 7) v3_model=agree
CASE GLOB-0       FAIL tool absent (GLOB new toggles file) v3_model=agree
CASE GLOB-1       FAIL tool absent (GLOB new toggles file) v3_model=agree
CASE GLOB-2       FAIL tool absent (GLOB new toggles file) v3_model=agree
CASE GLOB-3       FAIL tool absent (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  FAIL tool absent (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  FAIL tool absent (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  FAIL tool absent (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  FAIL tool absent (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    FAIL tool absent (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE COMMENT-1    FAIL tool absent (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE COMMENT-2    FAIL tool absent (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE COMMENT-3    FAIL tool absent (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE SYNTH-0      FAIL tool absent (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
CASE SYNTH-1      FAIL tool absent (SYNTH tree binds=12 unbound=1 vars=2) v3_model=agree
CASE SYNTH-2      FAIL tool absent (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      FAIL tool absent (SYNTH tree binds=10 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    FAIL tool absent (REWRITE argswap mask=65 key='UP' code=0; unbind mask=12 key='DELETE' code=0; add moveintogroup) v3_model=agree
CASE REWRITE-1    FAIL tool absent (REWRITE argswap mask=64 key='C' code=0; unbind mask=73 key='X' code=0; add exec) v3_model=agree
CASE REWRITE-2    FAIL tool absent (REWRITE argswap mask=64 key='BACKSPACE' code=0; unbind mask=64 key='' code=15; add changegroupactive) v3_model=agree
CASE REWRITE-3    FAIL tool absent (REWRITE argswap mask=65 key='B' code=0; unbind mask=76 key='R' code=0; add exec) v3_model=agree
CASE HARD-0       FAIL tool absent (HARD tree lines=32 binds=24 unbinds=2 vars=4) v3_model=agree
CASE HARD-1       FAIL tool absent (HARD tree lines=32 binds=22 unbinds=2 vars=4) v3_model=agree
CASE HARD-2       FAIL tool absent (HARD tree lines=31 binds=22 unbinds=2 vars=4) v3_model=agree
CASE HARD-3       FAIL tool absent (HARD tree lines=25 binds=15 unbinds=1 vars=4) v3_model=agree
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Matches the registered before-receipt shape (`ORACLE_CHECK` clean, MISSING_TOOL → 0/41, exit 1).
The stray nested instance and `/tmp/mado-r25-c1v4-*` dirs visible post-run belong to an in-flight
peer run in its own clone (`MadoR25A3.MutCounterV4`), not to this run; my run's tmpdir was removed
by its `finally` and it left no instances.

No tools installed (pacman transactions paused host-wide; nothing needed).

Report: .ufo/waves/round-25/a3w1/reports/RevCounterV4.md
