# SimplifyV3 — deletable dead weight in the round-38 v3 counters and the discrimination gate

**Seat:** `L1Mado38.SimplifyV3` (leaf, no dispatch). **Scope:** `quality/counters/c1-r38-event-ground.py`,
`quality/counters/c2-r38-eventq.py`, `quality/counters/c2-r38-request-ground.py`,
`quality/check-r38-discrimination.py`.

**Bottom line.** Nine deletion candidates were found and each was **measured**: the frozen 19-control
gate still scores **19/19 `TARGET_MET`** with the file patched in a `/dev/shm` sandbox. One further
candidate (`C7`) was **measured and rejected** — it breaks the counter. Three more candidates
(`C9` pin-derivation, the `srv_inodes` item named in the task, and clause-`j`/`b` removal as a
*semantic* change) were **measured and rejected** with evidence. One **pre-existing crash** was found
and is reported, not fixed.

**No lane file was edited.** `git status --short quality/` is empty and the four files' md5s are
unchanged from the round-38 landing:

```
f128d128142f1d7372bfa6da02ad515e  quality/counters/c1-r38-event-ground.py
358edfe39e144487137ec6debdbdf087  quality/counters/c2-r38-eventq.py
160c3271ee174932d73fa42a39d3c4d6  quality/counters/c2-r38-request-ground.py
d5748ee2f25682888f326aa754651095  quality/check-r38-discrimination.py
```

---

## Method

The lane moved under this seat twice during the wave (gate file rewritten by peer `SentManifestScope`
in `b8400aa`; tip advanced `b6c1d31 → e072af6`). All measurements below were re-taken against the
**current** file contents, snapshotted to `/dev/shm/mado38-SimplifyV3/base/`.

The gate command (frozen per `.ufo/waves/round-38/registration.md:42`):

```
python3 -I <gate> --c1 <c1> --c2 <c2> \
  --manifest .ufo/waves/round-38/controls/manifest.json --rev <rev> --sandbox-root /dev/shm
```

Baseline before any patch — **19/19**, twice (`--rev HEAD` and `--rev b6c1d31`):

```
control=c1-live instrument=c1 expected=TARGET_MET observed=TARGET_MET ok=1
...
MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET
```

`/tmp` was at 100% (peers' sandboxes, not mine); all scratch was moved to `/dev/shm`.

---

## Deletion list — each measured 19/19

| # | File | Deletion | Evidence |
|---|---|---|---|
| **C1** | `c1-r38-event-ground.py` | **Clause `j`** (`:216`, `:226`, `:228`) — the "unique registry row" clause | 19/19 |
| **C2** | `c1-r38-event-ground.py` | **Clause `b`** (`:198-200`) — header-line presence | 19/19 |
| **C3** | `c1-r38-event-ground.py` | **Both `b` and `j`** | 19/19 |
| **C4** | `c2-r38-eventq.py` | **Double-format of `sha_in`/`agree`** in the `why` string (`:245-247`) | 19/19 |
| **C5** | `c2-r38-eventq.py` | **Dead `"unscored"` literal** (`:266`) | 19/19 |
| **C6** | `c2-r38-request-ground.py` | **`pin[1] is not None` always-true guard** (`:213`) | 19/19 (not a gate instrument — own check below) |
| **C8** | `check-r38-discrimination.py` | **Unused `BASE` constant** (`:38`), **dead `ctx["scratch"]=None`** (`:154`), **dead store `p =`** (`:182`) | 19/19 |
| **C10** | `check-r38-discrimination.py` | **Unreachable `env` keys** `sb`, `append`, `delete`, `json`, `hashlib` (`:59-70`) | 19/19 |
| **C11** | `c2-r38-eventq.py` | **Second `git show` of the tool** (`:221-222`) — re-derives a blob already on disk | 19/19 |
| **SHARED** | `c1-r38-event-ground.py` + `c2-r38-request-ground.py` | **48-line duplicated helper block** → one shared module | 19/19 |

Full result set (`/dev/shm/mado38-SimplifyV3/out/*/summary.txt`):

```
BASE        :: controls=19 correct=19/19 verdict=TARGET_MET
C1          :: controls=19 correct=19/19 verdict=TARGET_MET
C2          :: controls=19 correct=19/19 verdict=TARGET_MET
C3          :: controls=19 correct=19/19 verdict=TARGET_MET
C4          :: controls=19 correct=19/19 verdict=TARGET_MET
C5          :: controls=19 correct=19/19 verdict=TARGET_MET
C6          :: controls=19 correct=19/19 verdict=TARGET_MET
C8          :: controls=19 correct=19/19 verdict=TARGET_MET
C10         :: controls=19 correct=19/19 verdict=TARGET_MET
C11         :: controls=19 correct=19/19 verdict=TARGET_MET
SHARED_HEAD :: controls=19 correct=19/19 verdict=TARGET_MET
```

### C1/C2/C3 — clause `j` and clause `b` in c1 are subsumed

Clause `j` (`:216`, `:226`, `:228`) requires `len(rows.get(i, [])) == 1` for every cited id. Clause
`c` (`:201-207`) requires **the same** `len(rows.get(i, [])) == 1` **plus** the mined/used-by
binding. `j` is therefore implied by `c`: `c=1 ⟹ j=1`, and `c=0 ⟹ ok=0` regardless of `j`. Clause `j`
was added by `859d0cf` ("clause c enforces unique registry rows per id") — that commit put the
uniqueness test **into `c`**, leaving `j` as a second, weaker copy of the same fact.

Clause `b` (`:198-200`) requires a `verified-at:` line and a `recheck:` line to be **present**.
Clause `k` (`:209-213`) requires those same two lines to be **present and parse**
(`bool(ver) and bool(rec)` over lists built from those exact `head` lines). `b` is implied by `k`;
and `k` is implied by nothing else, so `b` adds no discriminating power.

Measured on the `c1-duprow` crib (duplicate `S189` registry row inserted inside `## Registry`),
which is the manifest's `clause=j` control:

```
BASE (j present):  ... c=0 d=1 e=1 f=1 g=1 h=1 j=0 k=1 l=1 ... ok=0   admitted=0/2 TARGET_MISSED
C1  (j deleted):   ... c=0 d=1 e=1 f=1 g=1 h=1     k=1 l=1 ... ok=0   admitted=0/2 TARGET_MISSED
```

Same verdict, same `ok=0`, **and the crib is still caught** — because `c` (not `j`) is what now
carries the uniqueness test. The `c1-duprow` control therefore still scores `TARGET_MISSED`
(confirmed in the C1/C3 gate runs: `control=c1-duprow ... observed=TARGET_MISSED ok=1`).

**Caveat (stated, not hidden):** `j` and `b` are *named clauses* of the frozen predicate — the
manifest's `clause` field says `"j"` for `c1-duprow` and `"b"` for `c1-clause-b`, and the c1 docstring
enumerates `h`–`l` as the v3 additions. Deleting `j` removes the clause the manifest *names* for
that control even though the control still discriminates on `c`. The gate proves behaviour is
preserved; the *nomenclature* would need the manifest's `clause` field re-pointed at `c`. Recommend
C1/C3 land **with** the manifest `clause` field updated in the same change.

### C4 — the `why` string double-formats two predicates the gate already computed

`c2-r38-eventq.py:245-247`:

```python
proc_ok = (f"ss_sha256={snap_sha}" in ptext
           and srv and named == len(srv)
           and re.search(r"OVERALL:\s*AGREE", ptext) is not None)
why = (f"replay={int(replay_ok)} sha={int(sha_ok)} full_table={int(full_table)} "
       f"proc={named}/{len(srv)} sha_in={int('ss_sha256=' + snap_sha in ptext)} "
       f"agree={int(bool(re.search('OVERALL:.AGREE', ptext)))}")
```

`why` re-derives `sha_in` and `agree` **independently** of `proc_ok`. Two problems:

1. `sha_in` uses `int('ss_sha256=' + snap_sha in ptext)` — the same fact as `f"ss_sha256={snap_sha}" in ptext`,
   written a second time.
2. **`agree` uses a different regex than the gate.** The gate uses `OVERALL:\s*AGREE`; the detail
   line uses `OVERALL:.AGREE` (`.` = any char, exactly one). These disagree:

```
'OVERALL: AGREE'      gate=True  why=True   DIVERGE=False
'OVERALL:AGREE'       gate=True  why=False  DIVERGE=True
'OVERALL:XAGREE'      gate=False why=True   DIVERGE=True
'OVERALL:  AGREE'     gate=True  why=False  DIVERGE=True
```

Measured, committed proc receipt with `OVERALL: AGREE` → `OVERALL:XAGREE`:

```
BASE : live-detail replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1   fixtures=14/14 ... live=0 TARGET_MISSED
C4   : live-detail replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=0   fixtures=14/14 ... live=0 TARGET_MISSED
```

**BASE prints `agree=1` while the counter scores `live=0`** — the detail line contradicts the verdict
it is meant to explain. C4 hoists both into single booleans (`sha_in`, `agree`) used by *both*
`proc_ok` and `why`, so the detail line can no longer disagree. Gate: **19/19**.

### C5 — dead `"unscored"` literal

`:266` `live, why = 0, "unscored"` — `why` is unconditionally overwritten by `live_check` at `:278`
whenever `blob is not None`, and `live` is the only value read at `:286`/`:288`. The `"unscored"`
string is never observable. Gate: **19/19**.

### C6 — always-true guard in the request-ground counter

`:213` `if pin is None or rpath != pin[0] or (pin[1] is not None and digest != pin[1]):`

`pin` comes from `PINS` (`:63-76`), where every value is a 2-tuple `(path, sha256)` — `pin[1]` is
**never** `None`. The guard is always true, so it is dead. C6 rewrites it to
`if pin is None or (rpath, digest) != pin:` — the same form c1 already uses at `:222`.

`c2-r38-request-ground.py` is **not** a gate instrument (the manifest's `c2` is
`c2-r38-eventq.py`), so its own check was used:

```
C6 @b6c1d31 : admitted=3/3 verdict=TARGET_MET   exit=0
C6 @f6e3247 : admitted=0/3 verdict=TARGET_MISSED exit=1
```

(identical to BASE). The gate itself is unaffected: **19/19**.

### C8 — dead weight in the gate

* `BASE = "f6e3247f73152a39afb86066af48f3cedf95fb0a"` (`:38`) — **defined and never read**; the
  gate takes the base revision from `ctl["base"]`/the counter's own `--base` default. An AST scan of
  all four files reports `BASE` as the only top-level name with **zero references**.
* `ctx["scratch"] = None` (`:154`) — overwritten by `ctx["scratch"] = root` (`:156`) before any
  reader sees it.
* `p = sh(["git", *IDENT, "commit", ...])` (`:182`) — `p` is reassigned at `:185` without ever
  being read; the `git commit` call itself must stay.

Gate: **19/19**.

### C10 — unreachable `env` keys in the gate

`apply_writes` (`:59-70`) builds the `exec` namespace for manifest `py` writes. Scanning every `py`
op in the frozen manifest for identifier use:

```
{'sb': 0, 'write': 12, 'append': 0, 'delete': 0, 'read': 8, 'digest': 2, 'ctx': 0,
 're': 4, 'os': 0, 'json': 0, 'subprocess': 0, 'sys': 0, 'hashlib': 0, 'counters': 0}
```

`sb`, `append`, `delete`, `json`, `hashlib` are **never referenced** by any frozen control. (A peer
already removed `os`, `sys`, `subprocess`, `ctx`, `counters` in `b8400aa` — the same reasoning, and
the same residual names remain.) Gate: **19/19**.

### C11 — the tool blob is fetched twice

`c2-r38-eventq.py:221-222`:

```python
sha_ok = any("tool_sha256=" + hashlib.sha256(
    git(repo, "show", f"{rev}:{TOOL}") or b"").hexdigest() in l for l in text)
```

`main()` already wrote that exact blob to disk at `:270-272` (`tool = os.path.join(work,
"mado-eventq.py")`), and `live_check` receives `tool` as a parameter. The second `git show` re-derives
bytes already on disk. C11 reads the file instead. Gate: **19/19**; counter at HEAD unchanged
(`fixtures=14/14 readonly=1 live=1 verdict=TARGET_MET`) and at the tool-absent base unchanged
(`fixtures=0/14 readonly=0 live=0 tool=absent`).

### SHARED — the 48-line duplicated helper block

`c1-r38-event-ground.py` and `c2-r38-request-ground.py` carry **byte-identical** helper blocks —
verified by diffing the `class Setup` … `def main()` span:

```
c1 helper block lines: 48
request-ground helper block lines: 48
IDENTICAL: True
```

The shared span is `Setup`, `git`, `show`, `section`, `registry_rows`, `norm`, `quote_floor_ok`, plus
the module constants `ROW_RE`, `GATE_RE`, `ENV`, `DATE_RE`, `RECHECK_RE`.

**Constraint found:** `python3 -I` (isolated mode) **removes the script's directory from `sys.path`**,
so a plain `import mado_ground_common` fails under `-I` — which is exactly how the counters are
invoked (`registration.md:42`, and the gate's own `subprocess.run([sys.executable, "-I", script, …])`
at `check-r38-discrimination.py:185`). Measured:

```
--- python3 -I main.py ---
sys.path[0..2]: ['/usr/lib/python314.zip', '/usr/lib/python3.14', '/usr/lib/python3.14/lib-dynload']
IMPORT FAILED: No module named 'helper'
```

So the extraction needs an explicit `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))`.
With that, the extracted counters run identically and the gate scores **19/19**
(`SHARED_HEAD`, at the current tip `e072af6`):

```
PRED-C1-r38-v3 admitted=2/2 verdict=TARGET_MET rev=73412d29… exit=0
PRED-C2-r38-v1 admitted=3/3 verdict=TARGET_MET rev=73412d29… exit=0
SHARED_HEAD :: controls=19 correct=19/19 verdict=TARGET_MET
```

**Caveat:** the `sys.path` insertion is a new mechanism in two frozen instruments, and
`check-r38-discrimination.py` loads counters via `importlib.util.spec_from_file_location`
(`:48-51`), so the module must sit beside the counters on disk. The 19/19 is measured, but this is
a **structural** change to two frozen predicate files, not a local trim — recommend it only with
explicit sign-off, and note the gate's `load_counter` path is the one that must keep working.

---

## Measured and REJECTED — do not delete

### C7 — deriving `SURFACE_TOKENS` from `TARGETS` breaks the counter (**REJECTED**)

`c2-r38-request-ground.py:102-103` `SURFACE_TOKENS` and the `TARGETS` token tuples overlap but are
**not** the same set: `SURFACE_TOKENS` omits `1023`, which `TARGETS` carries for
`request-socket-live-bound-r8.md`. `1023` **is held at base**:

```
f6e3247:corpus/knowledge/event-delivery-limits-r26.md   (token "1023")
```

So `SURFACE_TOKENS` is the base-clean subset, deliberately narrower than `TARGETS`. C7 derives it
from `TARGETS` and the precondition fires:

```
C7 @b6c1d31 : PRED-C2-r38-v1 SETUP ground_held_at_base corpus/knowledge/event-delivery-limits-r26.md:1023   exit=2
C7 @f6e3247 : PRED-C2-r38-v1 SETUP ground_held_at_base corpus/knowledge/event-delivery-limits-r26.md:1023   exit=2
```

The counter stops scoring entirely (`exit 2`, `Setup`). **Not deletable.** (Independently reported
as F3 in `RevDomCounter.md:85-93`.)

### C9 — deriving `PINS` from the `## Gate` block removes the pin binding (**REJECTED**)

`PINS` (`c1-r38-event-ground.py:67-84`) duplicates the `## Gate` block's `(receipt, sha256)` pairs
in `corpus/lessons/round-37.md` — the task named this as a duplication candidate. It is **not**
redundant: `PINS` is the *anchor*, the Gate block is the *untrusted* side.

Measured probe — fabricate `S999` with a real receipt file, a matching `## Gate` line carrying a
valid quote, and a valid `## Registry` row; the only thing wrong is that `S999` is not in `PINS`:

```
BASE (frozen PINS)     : ... c=1 d=0 f=0 g=0 h=0 j=1 k=1 l=1 ids=S999 lineage=7/4 ok=0   admitted=1/2 TARGET_MISSED
C9   (PINS from Gate)  : ... c=1 d=1 f=1 g=1 h=1 j=1 k=1 l=1 ids=S999 lineage=7/4 ok=1   admitted=2/2 TARGET_MET
```

**C9 admits a fully fabricated source.** The pin table is what stops a self-consistent forgery
passing; deleting it (or deriving it from the same file it is supposed to police) removes the whole
`h`/`d` binding. **Not deletable.**

### `srv_inodes` — the named leftover does not exist (**NOT FOUND**)

The task named `c2-r38-eventq.py`'s `srv_inodes` leftovers. There is **no `srv_inodes` identifier**
in the lane:

```
$ grep -rn "srv_inodes" . | grep -v '^\./\.git/'
./.ufo/waves/round-38/w1-spec.json:149:   "prompt": "Find deletable dead weight … srv_inodes leftovers …"
./.ufo/waves/round-38/w1-dispatch.json:392: … (same prompt text)
```

Only the task text itself matches. The live code is `srv` (a set of socket2 server inodes, `:235-240`),
`named` (`:241`), `srv`/`named` are both **read** by `proc_ok` (`:242-244`) and by the `why` string
(`:246`). An AST scan of the four files reports **no unreferenced top-level name other than the
gate's `BASE`** and **no unused local variable in any function**. The `srv`/`named` pair is live and
load-bearing; there is nothing to delete.

### Clause `j` / clause `b` as *semantic* removals — the manifest names them (**CAVEAT, not a veto**)

See the C1/C2 caveat above: the gate proves the discriminative behaviour is preserved, but the
frozen manifest's `clause` field (`"j"` for `c1-duprow`, `"b"` for `c1-clause-b`) would point at a
clause that no longer exists. The `c1-clause-b` control in particular exists to exercise `b`;
after C2 it exercises `k` instead. Behaviour is preserved (the control still yields
`TARGET_MISSED`, because `k` fails when the `verified-at:` line is removed) but the control's
*stated target* moves. Recommend landing with the manifest `clause` field re-pointed.

---

## Pre-existing defect found (reported, not fixed — outside the deletion remit)

`c2-r38-request-ground.py:198-200` **crashes** with `TypeError` when an entry's first 15 lines have a
`source:` line but **no `verified-at:` line**:

```
c["b"] = int(bool(ids) and ver and rec
             and all(DATE_RE.match(v.split()[0] if v.split() else "") for v in ver)
             and all(RECHECK_RE.match(r.split()[0] if r.split() else "") for r in rec))
TypeError: int() argument must be a string, a bytes-like object or a real number, not 'list'
```

`ver`/`rec` are **lists**; `and` returns the list, and `int(list)` raises. Reproduced on a sandbox
clone with the `verified-at:` line removed from `hyprctl-flags-r28.md`:

```
PRED-C2-r38-v1 … (traceback)  TypeError: int() argument must be … not 'list'   exit=1
```

This is **pre-existing in HEAD** (`git show HEAD:quality/counters/c2-r38-request-ground.py` carries the
identical three lines) and is **not** introduced by any candidate above. c1 does not have it —
`c1-r38-event-ground.py:198-200` uses `any(re.match(...))` (a bool) rather than a list. The
one-token fix is `bool(ver) and bool(rec)`, matching c1's style. **Reported for routing; this seat
does not edit lane files.**

---

## Tools

No package installs were needed; `pyflakes` was run via `uv tool run --from pyflakes` (ephemeral, no
install). No compositor, config, service, package, or socket was touched; `hyprctl` was never invoked;
no Hyprland socket was contacted. `git` writes were confined to `/dev/shm` sandbox clones
(`git clone -q --no-local`, `git -c user.name=s -c user.email=s@i commit`); the lane's own jj/git
state was never modified (`git status --short quality/` is empty).

## Recommendation order

1. **C4, C5, C8, C10, C11** — pure local trims, no clause-set change, no new mechanism. Lowest risk.
2. **C6** — one always-true guard; `c2-r38-request-ground.py` is not a gate instrument.
3. **C1/C2/C3** — land only together with the manifest `clause` field re-pointed (`j`→`c`, `b`→`k`).
4. **SHARED** — structural; needs sign-off because it adds a `sys.path` insertion to two frozen
   instruments and constrains where the shared module may live.
5. **C7, C9, `srv_inodes`** — rejected; do not delete.
