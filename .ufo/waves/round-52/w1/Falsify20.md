# Falsify20 — C1 counter isolation/scratch behavior

Round 52, seat Falsify20. Source-only attack on the frozen C1 claim; no tracked
lane edits, no claim/predicate edits, no installs. Base `85d57a818c3707397e21c840b6498b105ba798aa`.

## Attacked clause

- **Item/predicate attacked:** C1 frozen predicate — *"a new counter for the tracked
  instrument ledger runs at a requested pinned revision, and validates population row
  uniqueness, resolvable evidence pointer, non-self pointer, and a description containing
  instrument-specific functional context"* — in the dimension of **counter
  isolation/scratch behavior**, plus the round scratch contract it must operate under
  (*"All scratch/clone/work under /fast/scratch/hyaku/mado-r52/<SeatName>/ (mkdir, explicit
  TMPDIR/--work); never /tmp for evidence"*).
- **Named control attacked:** the volatile-root refusal control in the predecessor
  counter, `REFUSED_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")`
  (`quality/counters/c1-r51-ledger.py:68`).

The new r52 counter is absent at base by design, so the demonstration runs against the
predecessor's committed bytes (the pattern the new counter is built from) plus seat-local
fixtures in scratch. This is not a generic review; it is one concrete failure mode,
reproduced.

## Finding: the scratch-location half of isolation is uncontrolled; the named refusal control is dead

**Reproduced: YES.**

### Evidence 1 — the counter's own refusal control never refuses

`grep -n REFUSED_ROOTS quality/counters/c1-r51-ledger.py`:

```
68:REFUSED_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
405:                    tuple(os.path.realpath(r) for r in REFUSED_ROOTS)):
407:                      % ", ".join(REFUSED_ROOTS))
```

Lines 405–407 sit inside the branch that prints a *hint after the delegated checker's
selftest has already failed*. `resolve_work()` (lines ~343–358) performs no location
check: with `TMPDIR` unset it calls `tempfile.mkdtemp(prefix="c1-r51-", dir=None)`
→ `/tmp`; an explicit `--work` under `/tmp` is accepted verbatim.

Deterministic demonstration by importing the committed module and calling its own
function (driver was seat-local scratch, now removed; output in
`receipt-d1-resolve-work.txt`):

```
resolve_work(None) TMPDIR-unset -> /tmp/c1-r51-7nyoto7y created= True
make_clone would place clone at: /tmp/c1-r51-7nyoto7y/clone-403811
work resolves under /tmp: True
explicit --work /tmp/c1falsify20-explicit accepted -> /tmp/c1falsify20-explicit created= False
```

(`make_clone` then does `clone = os.path.join(work, "clone-%d" % os.getpid())`, line 143.)

### Evidence 2 — live run transits the full measurement through /tmp

Command (cwd = seat scratch; all state written by the counter itself, cleaned by it):

```
env -u TMPDIR python3 quality/counters/c1-r51-ledger.py \
  --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
  --rev 85d57a818c3707397e21c840b6498b105ba798aa
```

Mid-run snapshot caught the clone in the prohibited location:

```
OBSERVED work=/tmp/c1-r51-s7o284gk
drwx------ 3 vgpnk vgpnk  26 ... clone-371340
```

Final result (`receipt-d2-tmp-unset.log`):

```
detail: checker selftest failed (exit=2 form=with-work)
detail: hint: the gate refuses --selftest work under /tmp, /var/tmp, /dev/shm
detail: checker ledger ok (rev=85d57a818c3707397e21c840b6498b105ba798aa)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=failed verdict=TARGET_MISSED ...
```

Synchronous rerun: `exit=1`. The counter cloned, measured all 82 rows, and ran the
ledger cross-check *from /tmp*; the failure came only from the **delegated**
`quality/check-tool-ledger.py`, whose own `resolve_work` (lines 414–421,
`REFUSED_WORK_PREFIXES` + home-dir refusal, `GateError` → exit 2) refused the selftest
sandbox. The counter's `REFUSED_ROOTS` contributed nothing but the hint line.

### Evidence 3 — compliant scratch gives green (failure is location, not content)

```
TMPDIR=/fast/scratch/hyaku/mado-r52/Falsify20 python3 quality/counters/c1-r51-ledger.py \
  --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 85d57a818c3707397e21c840b6498b105ba798aa
```

→ `selftest ok (ratio=50/50)`, `checker ledger ok`, `verdict=TARGET_MET`, exit 0
(`receipt-d3-tmpdir-green.log`; matches the committed base receipt
`.ufo/waves/round-52/receipts/c1-base.txt`).

### Evidence 4 — the pinned-revision half of isolation works (sharpens the attack)

Seat-local fixture repo (scratch, since removed): commit A = ledger with dangling
`tools/ghost.py` row (`6f4cc310…`), commit B = fixed (`8b68a5fa…`), then the working
tree dirtied with an uncommitted row. Counter scored the *requested revision* in both
cases and the delegated checker agreed (`receipt-d4-pinned-rev.txt`):

- `--rev A` (dirty tree) → `dangling=1 … verdict=TARGET_MISSED`
- `--rev B` (dirty tree) → `population=1 ledger_rows=1 … verdict=TARGET_MET`

So "runs at a requested pinned revision" is satisfiable and is isolated from HEAD and
from working-tree dirt. The uncontrolled surface is exactly the scratch-location half.

## Why this defeats the claim as scoped

The frozen C1 predicate constrains uniqueness, pointer resolution, non-self pointers,
and description context — and requires "Selftest includes explicit red/green receipts" —
but it does **not** require the new counter to delegate to `check-tool-ledger.py`, nor
any refusal of volatile roots, nor any placement of clone/work state. The only effective
/tmp protection in the entire r51 stack lives in the delegated checker's selftest path;
it is an accident of delegation, not a property of the counter or the predicate (a
fragile/duplicate-authority defect: the protection's existence depends on an
instrument the predicate never names). A new counter that self-tests with its own
fixtures and honors `TMPDIR` (unset in a fresh shell → `/tmp`) satisfies **every frozen
C1 predicate** — including green-on-production and red-on-`controls/c1-do-nothing.md` —
while placing all clone/evidence-transit state in `/tmp`, in direct violation of the
round's scratch/evidence contract. Predicate pass therefore does not imply the
instrument is operable within the round's own rules: an axis-1 (operability) gap.

## Smallest safe correction

Construction requirement on the new counter (no predicate amendment after data):
hard-fail (`exit 2`, `setup=error`) when the resolved work dir realpaths under `/tmp`,
`/var/tmp`, or `/dev/shm`, applying the check to **both** explicit `--work` and default
resolution, with default resolution failing closed when `TMPDIR` is unset instead of
silently using `/tmp`; and the committed selftest receipts must include an explicit
**red** receipt showing the `/tmp` refusal beside the green production receipt. At
scoring time, a counter lacking that red/green scratch-location pair should not be
admitted as meeting the operability claim even if all ledger predicates pass.

## Commands (key)

```
grep -n REFUSED_ROOTS quality/counters/c1-r51-ledger.py
env -u TMPDIR python3 quality/counters/c1-r51-ledger.py --repo <lane> --rev 85d57a81…   # → TARGET_MISSED exit 1, clone observed under /tmp
TMPDIR=/fast/scratch/hyaku/mado-r52/Falsify20 python3 quality/counters/c1-r51-ledger.py --repo <lane> --rev 85d57a81…   # → TARGET_MET exit 0
```

## Limitations

- The r52 counter is absent at base by design; the demonstration uses the predecessor's
  committed bytes and seat-local fixtures, per the seat's "source bytes/seat-local
  fixtures" remit. The conclusion is about the frozen predicate's coverage of scratch
  behavior, not about unaudited r52 code.
- `/var/tmp` and `/dev/shm` were not exercised live; they flow through the identical
  untested code path (no check at all in the counter).
- The delegated checker was not probed with a hostile checker script (out of scope for
  this seat).
- No installs. Scratch dir removed after receipts were copied; `/tmp` verified clean of
  counter leftovers. Disk guard checked (598G avail on /fast).

## Deliverables

- `.ufo/waves/round-52/w1/Falsify20.md` — this report
- `.ufo/waves/round-52/w1/Falsify20/receipt-d1-resolve-work.txt` — resolve_work() /tmp placement + REFUSED_ROOTS use-sites
- `.ufo/waves/round-52/w1/Falsify20/receipt-d2-tmp-unset.log` — TMPDIR-unset run: clone under /tmp, TARGET_MISSED via delegated checker only
- `.ufo/waves/round-52/w1/Falsify20/receipt-d3-tmpdir-green.log` — compliant scratch run: TARGET_MET
- `.ufo/waves/round-52/w1/Falsify20/receipt-d4-pinned-rev.txt` — pinned-rev isolation fixture runs (dirty tree, revs A/B)

Report: .ufo/waves/round-52/w1/Falsify20.md
