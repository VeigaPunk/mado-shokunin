author: mado (round 26 L1, `MadoR26`)

# Round 26 — registration (written and landed before any control or data seat scores a counter)

Base: lane tip `96101be5` (round-25 closure: admitted). Paths below are relative to
`.ufo/waves/round-26/` unless they start with the lane root (`tools/`, `corpus/`, `SCORECARD.md`).

## Host safety first: the oracle no longer touches the live session

Round 25's oracle started nested Hyprland instances with the wayland backend on the operator's live session
(windows on the desktop) and those instances left ~1330 SIGABRT coredump records (`coredumpctl`: 1330
`/usr/bin/Hyprland` entries in the 12 h before this round). From this round on every nested Hyprland runs
through `harness/oracle.py` only:

- Hyprland 0.56.2 cannot run headless-only: with no DRM card and no parent compositor, aquamarine has no
  allocator and Hyprland aborts with `CBackend::create() failed!` (pilot runs 1–2). Each nested Hyprland
  therefore gets its own private parent: tinywl from wlroots 0.20.2 (`d7835334`), built in
  `/fast/scratch/hyaku/mado-r26/wlroots` with `-Dbackends= -Dsession=disabled -Dxwayland=disabled
  -Drenderers=gles2 -Dallocators=gbm -Dexamples=true`, patched to offer wl_compositor v6 and xdg_wm_base v6
  (`harness/tinywl-global-versions.patch`; without it aquamarine's bind is a protocol error, pilot run 4),
  run with `WLR_BACKENDS=headless`. Binary pins: tinywl `227a74af…0cda`, libwlroots `1f3d7036…7967`.
- Both run in one bubblewrap sandbox: `--unshare-all --clearenv` (no WAYLAND_DISPLAY, no
  HYPRLAND_INSTANCE_SIGNATURE, no D-Bus address), `--tmpfs /run`, a private XDG_RUNTIME_DIR under `/tmp`,
  `/dev` with only `/dev/dri/renderD129` (amdgpu render node; no DRM card node, no input device),
  `LIBSEAT_BACKEND=noop`, `prlimit --core=0 --as=8000000000`. The counter reaches the instance with the host's
  `hyprctl` under `env -i XDG_RUNTIME_DIR=<private>` and stops it with `dispatch exit`.
- Pilot (`harness/pilot-receipt.txt`): the final method answered `binds -j` and `animations -j`, exited on
  `dispatch exit`, and the Hyprland coredump count stayed 1335 → 1335. The four failed pilot runs before it
  (backend creation and the protocol-version error) each aborted and added one record (1330 → 1335); they are
  this round's only coredumps and are named here, not hidden. Every counter receipt prints
  `HOST_SAFETY hyprland_coredumps_before=… after=… delta=…`.

## C1 — coverage (sourced): the animation directive → entry expansion, from `[INF]` to a tool

Surface moved: `corpus/knowledge/hyprctl-verification-layer.md:158` holds the animations row as "agreement at
count level; directive→entry expansion `[INF]`"; no lane tool or entry computes the `hyprctl animations -j`
table (34 animation nodes + internal node, bezier list) from config bytes. C1 adds that operation:
`python3 -I tools/mado-anims.py --home DIR` prints `[nodes, beziers]` in the shape of `hyprctl animations -j`.
The command that would show it unmoved is the counter at base (`tool=MISSING_TOOL`, 0/41).

**PRED-C1-r26** (same sentence in `c1/count.py`'s docstring and the receipt label): At REV, the committed
bytes of tools/mado-anims.py, run in the tool sandbox (no network, no /run, cleared environment, the case tree
read-only at /snap/home from a randomly named directory), print for the unperturbed snapshot of the four
Hyprland config roots and for each of 40 generated cases the same animation-node set (name, overridden,
bezier, enabled, speed, style) and the same bezier set (name, X0, Y0, X1, Y1) that Hyprland v0.56.2 itself
reports with `hyprctl animations -j` for the same tree (a nested, headless, session-isolated instance run by
the counter on a copy with exec lines removed); target: cases_pass=41/41.

Counter `c1/count.py` (sha256 in the landing commit; `harness/oracle.py` pinned inside it). Cases apply 2–4
operations from ROOT, SOURCED, NEWSRC, UNSOURCED, BEZIER, REBEZ, VARIABLE, COMMENT, CATEGORY, DISABLE,
INVALID, ORDER, SPACING to a copy of the snapshot; expected values come only from Hyprland.

## C2 — operability: the bind resolver works on trees that use hyprlang `{{…}}` expressions

Surface moved: `tools/mado-binds.py` (round 25) leaves `{{…}}` literal (round-25 scope limit,
`a3res/ResC1Remeasure.md`; spot-check routed defect 6), so on a tree whose binds or variables use hyprlang
arithmetic its table is wrong. C2 makes the existing capability work on such trees without losing the round-25
behaviour.

**PRED-C2-r26** (same sentence in `c2/count.py`'s docstring and the receipt label): At REV, the committed
bytes of tools/mado-binds.py, run in the tool sandbox (no network, no /run, cleared environment, the case tree
read-only at /snap/home from a randomly named directory), reproduce exactly over all 18 `hyprctl binds -j`
fields the bind multiset that Hyprland v0.56.2 itself reports for the same tree (a nested, headless,
session-isolated instance run by the counter on a copy with exec lines removed), for the unperturbed snapshot
of the four Hyprland config roots, for 30 ARITH cases (added binds and variables whose values use hyprlang
`{{...}}` expressions) and for 20 V3 cases (round 25's count-v3.py generator, two of each of its ten types,
fed the oracle's table of the unperturbed snapshot), and the tool bytes contain none of that table's arg or
description strings of 12 or more characters; target: cases_pass=51/51 and embed_hits=0.

Counter `c2/count.py` (pins `harness/oracle.py` and `round-25/c1/count-v3.py`). The 20 V3 cases are the
no-harm half: a change that breaks round-25 behaviour misses the target.

## Kill rule, measurement and order (both claims)

1. This file, `harness/`, `c1/count.py`, `c2/count.py` land in one commit before any control seat runs.
2. Control wave (w1) scores the controls below under the frozen counters; receipts land in one commit before
   the data wave (w2) registry exists. A control that meets a target sends that claim back to redesign before
   data, or the claim is declared exploratory; this file then gets an appended note, never an edit above.
3. Data seats build in scratch; the L1 lands the first tool file a data seat returns that it has not
   modified, by that rule fixed here.
4. One measurement run per claim at the landing commit: `python3 -I .ufo/waves/round-26/cN/count.py REV`.
   Its verdict is the claim's verdict; a non-`TARGET_MET` exit 1 is a miss, reported, never re-scaled. A run
   that exits 2 (guard: ORACLE_FAIL, ORACLE_UNSTABLE, pin mismatch) measured nothing; it is kept and re-run.
5. Before receipts: each counter at base `96101be5` (C1 `MISSING_TOOL`; C2 the round-25 tool).

## Controls (w1, before data; each scored with the frozen counter, two fresh seeds)

C1: do-nothing (absent / empty output), all-empty `[[],[]]`, junk, static default table (Hyprland's tree with
no config read), snapshot-cached table (the operator's current table embedded, config ignored), root-only
reader (no `source`), naive grep (every `animation =`/`bezier =` line in every file under DIR, no source graph,
no variables, no validation), no-validation reader (source graph and variables, accepts every line),
label/position-keyed (tries to learn the case from paths, mountinfo, mtimes or file names).
C2: do-nothing, base tool (round-25 `tools/mado-binds.py` at `96101be5`), brace-stripper (base tool, `{{`/`}}`
deleted), python-eval shortcut (base tool + `eval` of the brace contents with no hyprlang rules), V3-only
reader, label/position-keyed, embed (base table cached and replayed).

## Repairs routed by the round-25 spot-check (not claims)

R1 M25-2 label-free case paths: `harness/oracle.py` `run_tool` (random mkdtemp case directories, shuffled run
order). R2 counter mutants: drift-fault witness and embed fixture in a counter self-test. R3 M25-4 population
equality encoded in QUALITY 36 (successor criterion 37) and its check. R4 M25-3 fixtures for the surviving
`check-control-receipts.py` mutants plus a `--counter-sha` filter. R5 `round-25/registration.md:85` correction
(appended). R6 round-25 before receipt without `exit=` (appended note; the receipt itself is not rewritten).
R7 bind-tool scope limits: `{{…}}` is C2; reads outside `--home` stay a stated limit.

## Separability and harm watch

C1 needs only `tools/mado-anims.py`; C2 only `tools/mado-binds.py`; neither counter reads the other's tool.
Harm watch at the measured commits: other `tools/` files byte-identical to base; census exit 0; no line removed
from LOG, SCORECARD, QUALITY, README, SOURCES except logged in-place `used-by` changes.

## Pins at landing

`c1/count.py` sha256 `f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd`; `c2/count.py` sha256
`b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8`; `harness/oracle.py` sha256
`680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441`. Development runs before landing scored only
an empty-output tool and a snapshot-cache tool written by the L1 (C1 0/41 and 2/41, C2 0/51; scratch, not
receipts): they tested the plumbing and led to one generator change before landing (every C1 case carries at
least one table-changing operation). No control or data seat has run.

## Errata (appended after landing; the rule above is unchanged)

- Host-safety paragraph: "The four failed pilot runs" should read "The five failed pilot runs" (the unpatched-tinywl
  run was executed twice, the second time with debug logs); the count 1330 → 1335 was right
  (`harness/pilot-receipt.txt` errata; flagged by w1 ScribeMistakes).

## C1 redesign before data: counter v2 (appended 08:59Z; no data seat exists yet)

w1 `CritC1Design` (`w1/reports/CritC1Design.md` B, C, E1) found, before any data seat: (1) every v1 case appends to
the same snapshot, so a tool that caches the snapshot's own directives and parses only appended lines could meet v1
without reading the original config bytes (an untested cache-plus-delta shortcut); (2) v1 does not check which
Hyprland answered; (3) the sentence above "every C1 case carries at least one table-changing operation" is false —
v1 guarantees only an operation from the EFFECTIVE list (the K1SnapshotCache receipts pass 1–2 unchanged cases).
v1 (`c1/count.py`) and its w1 control receipts stay as they are. **C1 is now judged by counter v2**
(`c1/count-v2.py`, sha256 `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428`), frozen here, before any data seat:

**PRED-C1-r26-v2** (same sentence in `c1/count-v2.py`'s docstring and the receipt label): At REV, the committed
bytes of tools/mado-anims.py, run in the tool sandbox (no network, no /run, cleared environment, the case tree
read-only at /snap/home from a randomly named directory), print for the unperturbed snapshot of the four Hyprland
config roots and for each of 40 generated cases (20 that append directives to the snapshot, 10 that edit or
delete the snapshot's own directives, 10 independent trees that contain none of the snapshot's files) the same
animation-node set (name, overridden, bezier, enabled, speed, style) and the same bezier set (name, X0, Y0, X1, Y1)
that Hyprland v0.56.2 itself reports with `hyprctl animations -j` for the same tree (a nested, headless,
session-isolated instance run by the counter on a copy with exec lines removed); target: cases_pass=41/41.

New guard: `ORACLE_VERSION` (exit 2) unless the nested instance's `hyprctl version -j` commit is
`efb50993780079460b0cbed1363e2166a2de1d9f`. Per-case `changed=yes|no` is printed as a diagnostic only. The
cache-plus-delta shape is bounded by construction under v2: the 10 SYNTH trees contain none of the snapshot's
files and the 10 EDIT cases change the snapshot's own lines, so a cache of the snapshot's events applies to at most
BASE + 20 APPEND = 21 of 41 cases. Every committed C1 control program is re-scored under v2 before the data wave
(receipts `controls/v2/`); the kill rule and landing rule above apply to v2 unchanged. C2 and its counter are
unchanged.

C2 notes from w1 `CritC2Design` (no rule change): the ARITH cases cover hyprlang's one-operator expressions,
decimals, `$var` substitution, one escape form and unclosed braces, not every expression rule (bare-name
variables, backslash parity, nested braces are not generated); the V3 half re-checks round-25 behaviour on 20
sampled cases, it is not an exhaustive no-harm proof — "the no-harm half" above means exactly that sample.
