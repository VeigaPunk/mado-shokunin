# RevEntryR14 — errata to this seat's own record (post-measurement)

Written 2026-10-25 03:52. Corrections to what this seat recorded or reported earlier. The
as-measured probe log (`probe-log.md`, 8446 B, sha256 `2bde25ab…36da`) is deliberately
**unmodified**: it is evidence of what was measured and printed, errors included. This file is
a correction record, not host evidence.

## E-A. Wrong exit code recorded for the coredump query (my error)

The as-measured log says `coredumpctl list hypridle --no-pager -> "No coredumps found." rc=0`.
The `rc=0` is **wrong**: the command was run as `coredumpctl list hypridle --no-pager 2>&1 | head -10 ;
echo "rc=$?"`, so `$?` was `head`'s status, not coredumpctl's. Re-run without a pipeline:

```
$ coredumpctl list hypridle --no-pager   ; echo filtered_rc=$?
No coredumps found.
filtered_rc=1
$ coredumpctl list --no-pager >/dev/null ; echo all_rc=$?
all_rc=0
$ coredumpctl list hyprlock --no-pager   ; echo hyprlock_rc=$?
No coredumps found.
hyprlock_rc=1
```

So: filtered "no match" is **rc=1**; only the unfiltered listing returns 0. The substantive
finding (no hypridle/hyprlock dumps exist, one continuous run since 2026-10-23 22:14:10) is
unchanged; only the exit code this seat attributed to the query was wrong. Correct usage in the
report is now rc=1, and the pipeline-status trap is the reason.

## E-B. The registry row S205 was rewritten mid-round; C1 never reads it

`corpus/SOURCES.md` mtime `2026-10-25 03:40:12`. Row S205's `teaches` cell (index 6):

```
02088b4 (wave-1 landing, 03:23:36): "… the journal holds two start lines on 2026-10-23, while the unit probe reads inactive only because the daemon ru…"
4f35c80 (03:34:26):                 "… the journal holds one start line in the current boot (two across two boots) on 2026-10-23, while the unit probe reads inactive only because the daemon runs inside a transient scope, so the process probe is the true reading; the declared chain is a screensaver at 150 s and a lock at 152 s"
```

Verified by `git show 02088b4:corpus/SOURCES.md` vs `git show 4f35c80:corpus/SOURCES.md`; worktree
matches HEAD (`a80f8cb`). The commit that rewrote it — `4f35c80`, "wave-2 falsifications as
errata — the shape-scored counter, the falsified ledger claim, the census gaps and the misroot" —
is also the commit that appended E1 to the entry.

Consequences:
- C1 stayed `TARGET_MET` rc=0 across the rewrite, because it reads only cells 0/5/7/9/10 and row
  shape, never cell 6. `closed_rows=8` therefore certifies well-formedness and receipt anchoring,
  not row truth or row/entry agreement.
- The row now says "one start line in the current boot" while entry line 17 still says
  "a restart, not a first start" — the artifact set contradicts itself and the predicate is green.
- The row's new `teaches` also asserts the transient-scope mechanism as fact. That is true (see
  report §4) but S205 does not license it, so an unlicensed claim now sits in a cell no clause reads.

## E-C. C1 reproduces TARGET_MET on the lane's own shape-only and fabricated mutants

Read-only runs against the committed controls (they are fixtures, not census data):

```
$ python3 -I .ufo/waves/round-35/c1/count.py --root $PWD/.ufo/waves/round-35/controls-content/c1-shape-only --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET      rc=0
$ python3 -I .ufo/waves/round-35/c1/count.py --root $PWD/.ufo/waves/round-35/controls-content/c1-fabricated-payload --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET      rc=0
```

Payloads:
- `c1-shape-only/corpus/knowledge/idle-lock-chain-armed-r14.md` is **one line**:
  `gate-quote: S205 snarfg plugh`; its S205 receipt is
  `111111111111 snarfg plugh 999999999999 lorem ipsum void`.
- `c1-fabricated-payload/…/idle-lock-chain-armed-r14.md` is **one line**:
  `gate-quote: S205 fabricated attestation for S205`; its S205 receipt is 78 B and reads
  `THIS IS NOT A FETCHED RECEIPT / fabricated attestation for S205 / ZERO REAL BYTES`.

The lane also ships negative controls (`controls/c1-digest`, `c1-donothing`, `c1-entry-symlink`,
`c1-quote-absent`, `c1-quote-long`) which the predicate rejects. So the predicate's failure mode is
precisely what a substring test can and cannot do: it rejects malformed shape, and it accepts any
well-shaped payload, including a one-line entry and a receipt that announces its own fabrication.
This seat did not discover that; it is committed at `4f35c80` and named in that commit's subject
("the shape-scored counter"). What remains open is the interpretive step the frozen claim takes —
reporting `TARGET_MET` as coverage — and the concrete instance in E-B, which the mutants do not model.
