# RerunControlsV2 — re-run of the C2 v2 controls and the CritC2Cheat forgery harness

Seat: w2, round 43 (hyaku run 8). Leaf re-run seat; no subagents, no background jobs, no compositor or host state touched.
Attacked claim: `receipts/ctl-c2-v2.txt` and `ctl/v2-forgeries/{forge-v2.log,more-v2.log}` as registered in
`registration-v2.md` (v2 freeze `496340dd53fabd800be42e8fb19090f35e2c235c`) and as measured at the data commit
`1959770657f1f8665097c1aed4be6c1cbb07139f`.

**Verdict: NOT FALSIFIED.** All three artifacts reproduce byte-for-byte, with one mechanical difference: the committed
logs end with an `exit=0` line that the invoking shell appended; a direct redirect does not emit it (my runs returned
rc 0, printed separately). Every control line, every forgery line and all 60 dumped fixture files are identical.

## Method (nothing frozen was rewritten)

Three copies in this seat, hashed before patching:

| file | seat copy sha256 | original sha256 |
|---|---|---|
| `run-c2-controls-v2.local.py` | `30ccdf57…` → patched, see `copy-patch.diff` | `30ccdf57…` |
| `forge.local.py` | `87506e60…` → patched | `87506e60…` |
| `more.local.py` | `3828ab68…` → patched | `3828ab68…` |

`copy-patch.diff` is the whole delta: 12 lines, all path lines — the runner's `LANE` pinned absolute (its copy no longer
sits four levels under the lane), `WORK` moved to `/fast/scratch/hyaku/mado-r43/RerunControlsV2/forge`, `SEAT` for the
forge fixture dumps moved to this seat, and `CTL` re-pointed at the seat's runner copy. `TMPDIR` was passed explicitly on
every invocation. Nothing under `ctl/`, `quality/counters/`, `receipts/` or `fetch/` was written: `find .ufo/waves/round-43/ctl quality/counters -newermt '2026-10-26 05:20'`
lists only another seat's `c1-r42-geometry` pyc, and the ctl tree still carries its 04:45/04:46 mtimes.

Commands (all outputs in this seat, `verify.out` re-derives every number below):

```
TMPDIR=/fast/scratch/hyaku/mado-r43/RerunControlsV2 python3 -I .ufo/waves/round-43/w2/RerunControlsV2/run-c2-controls-v2.local.py
TMPDIR=… python3 -I .ufo/waves/round-43/w2/RerunControlsV2/forge.local.py
TMPDIR=… python3 -I .ufo/waves/round-43/w2/RerunControlsV2/more.local.py
```

## Tallies

**Controls** — `ctl-c2-v2.rerun.txt` vs `receipts/ctl-c2-v2.txt`: identical after dropping the `exit=` line.
74 control lines, all distinct names: 2 sanity (`P-real`, `P-patched`, both must be 1/1) and 72 mutants (each must be
0/1). `ok=1` on all 74; final line `CTL_C2: controls=74 correct=74/74`; rc 0.

**Forge** — `forge-v2.rerun.log` vs `forge-v2.log`: identical after dropping `exit=`.
`=== forged fixtures admitted by the frozen counter: 6/15` (`forge-v2.log:17`). Admitted by name:
`P-genuine`, `A1-unsupported-claim`, `A2-census-contradiction`, `D1-census-irrelevant`,
`E2-anonymous-contradiction`, `H1-theme-contradiction`. Rejected by name: `B1-second-occurrence`,
`B2-second-locator-negative`, `C1-comment-quote`, `C2-comment-quote-dup`, `E1-id-contradiction`,
`F1-fake-package-dir`, `F2-refuse-no-flip`, `G1-fake-url`, `G2-relative-path`.
Counting `P-genuine` as the sanity fixture, five forgeries survive in this harness.

**More** — `more-v2.rerun.log` vs `more-v2.log`: identical after dropping `exit=`.
`X1-index-row-lie` admitted (1/1); `X3-own-work-only` rejected (i:0); `X2-localized-in-entry` rejected (i:0).
The three probe counters behave as logged: `P-genuine` is 1/1 under `refuse-flip-marker`, `bad-loc-in-entry` and
`all-pins-cited` (each probe is P-safe), and each probe kills its target (`F2`, `X2`, `X3` respectively, all i:0).

So the registration's admitted set — `registration-v2.md:29`, "still admitted: A1, A2, D1, E2, H1, X1" — is exactly
what the frozen counter does at HEAD: five from the forge harness plus `X1` from `more.py`. No name moved.

**Fixture dumps** — `diff -r ctl/v2-forgeries/fixtures w2/RerunControlsV2/fixtures` is empty; 60 files on both sides
(15 tags × the 4 dumped files). The forgery *inputs* reproduce, not just their verdicts.

## Inputs the rerun measured are the frozen ones

- Counter `quality/counters/c2-r43-gkeep-entry-v2.py` is `9a83407062d165661d211a714ce06b381391c7c4574c91c71eb54689dde1d028`
  at the data commit and at HEAD (HEAD `2a3707c`, data `1959770` is an ancestor); the forge log's own header prints the
  same digest.
- `git log 496340d..HEAD -- .ufo/waves/round-43/ctl quality/counters/c2-r43-gkeep-entry-v2.py .ufo/waves/round-43/fetch`
  is empty, and `git diff --stat 496340d HEAD` over the same paths is empty: the scripts, the counter and the ten pinned
  receipts have not moved since the v2 freeze, so running at HEAD is running the frozen experiment.
- `python3 --version` = 3.14.8, matching the `cpython-314` tag of the committed `ctl/__pycache__`.
- The suite was executed twice in this seat (`ctl-c2-v2.rerun.txt`, `teeth-v2.txt`); the two outputs are identical, so
  the result is deterministic and not run-order dependent.

## Teeth probe — is the 74/74 tally load-bearing?

Three extra runs through a thin driver (`teeth.py`) that loads the seat's runner copy and swaps only the scorer:

| mode | result | reading |
|---|---|---|
| `v2` | `controls=74 correct=74/74`, rc 0 | reproduces the receipt |
| `always-admit` (score forced to 1/1) | `controls=74 correct=2/74`, rc 1 | the tally is not a tautology: only the two `P-*` lines survive; all 72 mutants go `ok=0` |
| `v1` counter (`c2-r43-gkeep-entry.py`) over the same fixtures | `controls=74 correct=74/74`, rc 0 | see below |

The `v1` row is a limitation of the receipt, not a divergence: the *ok* column of the 74 controls does not discriminate
v1 from v2. What discriminates is the clause column — comparing the two committed receipts, 23 of the 74 control lines
differ (46 `diff` lines), and a pairwise check proves every one of them changes **only** `i:1` → `i:0` with the `ok`
column unchanged (`verify.sh`, last section: `controls=74 differing=23 only-i-changed=True ok-unchanged=True`).
So `ctl-c2-v2.txt` evidences "re-run under v2" exactly as registered,
and it evidences the added `i+` clause only through those 23 clause flips — not through a control that a v1-style counter
would fail. Anyone quoting the 74/74 as proof of the v2 clauses specifically would be over-reading it.

## Residuals and risks (declared, not new findings)

- The six admitted forgeries are the residual the registration already declares (`registration-v2.md:29`): a real quote
  at a true locator under a claim it does not support (A1, A2), a census contradiction in prose (D1, H1), an anonymous
  contradiction (E2), an index-row lie (X1). My rerun confirms these are live at HEAD, so an entry could pass
  `PRED-C2-r43-v2` while misdescribing its own census. Non-author closure, not a control defect.
- The harness is synthetic by construction: `base_files()` and `admitted()` build the fixture, and only the receipts come
  from `fetch/`. A pass says nothing about the real entry's prose; entry-level attacks belong to the seat that reads the
  entry (`w2/CritEntryOverreach`, `w1/CritC2Cheat`).
- Everything here is reproducible from this seat: `verify.sh` recomputes each number and greps the quoted lines at their
  cited locations.

## Files in this seat

`report.md` (this file), `run-c2-controls-v2.local.py`, `forge.local.py`, `more.local.py` (patched copies),
`copy-patch.diff` (their whole delta from the frozen originals), `ctl-c2-v2.rerun.txt`, `forge-v2.rerun.log`,
`more-v2.rerun.log` (+ `.err`, all empty), `fixtures/` (60 files), `teeth.py`, `teeth-v2.txt`, `teeth-v1.txt`,
`teeth-always-admit.txt`, `verify.sh`, `verify.out`.

Tooling: nothing installed or upgraded; `python3` 3.14.8 and the host `git` were sufficient. Scratch
(`/fast/scratch/hyaku/mado-r43/RerunControlsV2`, git fixtures included) deleted after the receipts were copied here;
host compositor untouched, no `hyprctl` call was made by this seat.
