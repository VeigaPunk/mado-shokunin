# C1 control fixtures — SPEC (mado round 51, w1, seat ExecControlsC1)

Contract: `.ufo/waves/round-51/claims.md` C1 (`PRED-C1-r51`), frozen 2026-10-27.
Round base: `6ca8c559a4a3d6d361101592116eea2bc7452437` (lane `mado-shokunin`).
Sibling spec consulted: `.ufo/waves/round-51/w1/CritLedgerControls/controls-c1.md`.

The fixture **trees are not committed** — they lived under
`/fast/scratch/hyaku/mado-r51/ExecControlsC1/` and were deleted after the receipts
were copied here. This file plus `expected.txt`, the receipts in `actual-run/`, and
the three drivers (`make-fixture.py`, `run-all.sh`, `verify-controls.py`) are the
frozen SPEC.

## 1. Instruments under test

At this seat's first read, `w1/ExecLedgerGate/` was empty; it was populated minutes
later (draft mtime 07:01, this seat re-read 07:0x). Every control was therefore run
against **both** instruments, and both agree on every count:

| file | sha256 | role |
|---|---|---|
| `w1/ExecLedgerGate/check-tool-ledger.py` | `6dd4061c1d8a82d5a9efa8ae954ff1c4559e43abefbb69210fa831bd758a98d4` | the tracked-instrument draft (primary) |
| `controls-c1/check-tool-ledger.py` | `8317cbcca4b9006833177221b394c891391994bb991a8c9a2f100e17ce7296c7` | faithful seat build of the frozen predicate (independent cross-check) |
| `controls-c1/make-fixture.py` | `3b6ab25803901b12b8248c370d2de08f896ada388fc6993251d75ab7bf51f06c` | fixture builder |
| `controls-c1/verify-controls.py` | `ca33f7eb7479370d7ac7cb1689a76d7038a91f40befed36e8c4fa333464a8057` | grades the seat build's receipts |
| `controls-c1/verify-gate.py` | `83afcdce48895a0a2c534da9720d98f6512782eaf929f1cd22f1c8f324d66925` | grades the gate draft's receipts in the gate's own schema |
| `controls-c1/run-all.sh` | `c484dd77678af29fe2bdb6fe97d2ceffd25cd8b4f15e61ef5581cc23c9bbc4d4` | re-runs every seat-build receipt |

The seat build is **not** the tracked `quality/check-tool-ledger.py` and must not be
copied to that path; the ledger builder owns the tracked instrument. Its reading of
the predicate:

* **population P** = files at `<rev>` matching `tools/*`, `quality/*.py` (no
  subdirectory), `quality/counters/*.py`; base = **79** files
  (tools 17 + quality/*.py 18 + quality/counters/*.py 44; `controls-c1/population-base.txt`).
* **ledger** = `quality/tool-ledger.md` bytes at `<rev>` (`git show <rev>:…`, never
  the worktree).
* **row syntax** = markdown table row `| `path` | description | `pointer` |`;
  header/separator skipped; a path cell without `/` is ignored.
* **pointer** = backticked path, optional `:LINE` / `#LLINE`; valid iff that path
  exists at `<rev>` **and** its bytes at `<rev>` contain `basename(row path)`.
* **counters**: `uncovered` = population files with no row; `dangling` = rows whose
  path is not a fresh population member (unknown path **or** a duplicate occurrence
  of an already-covered path); `bad_pointer` / `empty_desc` evaluated **only** on
  rows that bind a fresh population file, so the four defect counters are
  orthogonal (a dangling row is reported once, as `dangling`).
* **absent ledger** (claims.md wins over the common line):
  `C1_R51: population=P ledger=absent verdict=TARGET_MISSED rev=<rev>`, exit 1.
* **common line**:
  `C1_R51: population=<P> ledger_rows=<R> uncovered=<u> dangling=<d> bad_pointer=<bp> empty_desc=<e> selftest=<ok|FAIL> verdict=<TARGET_MET|TARGET_MISSED> rev=<rev>`,
  exit 0 / 1. `--selftest` runs 9 hermetic cases (`SELFTEST cases=9 failed=0`);
  a normal run executes the same suite silently, so `selftest=ok` is measured on
  every invocation, not asserted.
* setup errors → exit 2 (bad repo/rev, `--work` under `/tmp`, `/var/tmp`,
  `/dev/shm`, or inside `HOME`; `--work` defaults to `TMPDIR` when omitted).

## 2. Fixture construction (`make-fixture.py --lane … --base 6ca8c55… --fixture …`)

A **fresh** `git init` sandbox (never a clone of the lane; the lane is read with
`git show` only). Every commit asserts
`git rev-parse --show-toplevel` equals the fixture dir first
(receipt `actual-run/fixture-toplevel-and-log.txt`).

1. Materialize the 79 base-population files byte-for-byte from the lane base rev.
2. Add `ACCOUNT.md` (one `- <basename>` line per file — the accountability target),
   `DECOY.md` (prose that contains no basename), `EXTRA-DECOY.md` (names the three
   rejected fixture paths).
3. Commit → `rev_fixture_base` **e5943b7032fd9b73d02f7e9a71efa6848cec22a8** (no ledger).
4. Write `quality/tool-ledger.md` with 79 rows: path, `does <basename>`,
   pointer `ACCOUNT.md:<line of that basename>`; commit, tag **`r51-control`**
   → **aef0acf4ea4be1598771a210b8d41771517ff4be** (green baseline). Population
   stays 79 (no new `.py` files).
5. One branch per mutant, each a single commit on top of `r51-control`:

| control | mutation | rev |
|---|---|---|
| (a) | delete only the `tools/mado-keysym.py` row (78 rows) | `c02eeab908ae9da8d2413ef6dfbbfe81a089467a` |
| (b) | the five newest tools' pointers → `DECOY.md:1` (file exists, bytes lack the basenames) | `a03b9fdcf63122cb3cf35fa1870b77fcb45e6f4b` |
| (c) | description cell emptied on all 44 `quality/counters/*.py` rows | `70d323611187101f67a5c5afa08f34bbbb382899` |
| (d) | append 3 rows `quality/not-a-tool-{1,2,3}.txt` → `EXTRA-DECOY.md:{1,2,3}` (82 rows) | `f6bbf864f4ec034a5fe2c009548a625ceb695a3d` |
| (e) | the lane's own base revision `6ca8c55…` (ledger absent) | lane |

The five newest tools are derived from **base history**, not lexicographic order
(`git log --follow --diff-filter=A --format=%ct -1 <base> -- tools/<f>`, receipt
`actual-run/newest-five-tools-derivation.txt`):
`mado-hostguard.py`, `mado-keysym.py`, `mado-terminal.py`, `mado-devices.py`,
`mado-monitors.py`.

Fixture commit hashes are **not reproducible** (timestamps/identity differ on a
rebuild); the receipt hashes above are the ones measured at this seat run. What is
reproducible is the shape: P=79, C=44, the mutation semantics and the verdicts.

## 3. Expected vs actual

Reproduce with
`bash controls-c1/run-all.sh <scratch> <this-seat-dir> /home/vgpnk/Projects/shokunin/mado-shokunin`
after regenerating the fixture with `make-fixture.py` at the same base rev.

| control | expected final line | exit | actual |
|---|---|---|---|
| green | `C1_R51: population=79 ledger_rows=79 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=r51-control` | 0 | match |
| (a) | `… ledger_rows=78 uncovered=1 … verdict=TARGET_MISSED rev=mut-a` | 1 | match |
| (b) | `… bad_pointer=5 … verdict=TARGET_MISSED rev=mut-b` | 1 | match |
| (c) | `… empty_desc=44 … verdict=TARGET_MISSED rev=mut-c` | 1 | match |
| (d) | `… ledger_rows=82 … dangling=3 … verdict=TARGET_MISSED rev=mut-d` | 1 | match |
| (e) | `C1_R51: population=79 ledger=absent verdict=TARGET_MISSED rev=6ca8c559a4a3d6d361101592116eea2bc7452437` | 1 | match |
| fixture base | `C1_R51: population=79 ledger=absent verdict=TARGET_MISSED rev=e5943b70…` | 1 | match |
| `--selftest` | `SELFTEST cases=9 failed=0` | 0 | match |

The exact strings, including the full-hash replays, are in `expected.txt`; the
graded table is `actual-run/compare.txt` (`controls=8 mismatched=0`, exit 0).
Every field value is exact: no approximations, no inferred counts.

### 3b. Same controls against the ExecLedgerGate draft

The draft appeared after the first read; it was re-run on every fixture rev and on
the lane base. Its own schema (`LEDGER:` prefix, no `selftest=` field) was graded by
`verify-gate.py` → `actual-run/compare-gate.txt`
(`controls=8 mismatched=0`, exit 0):

| control | gate line (counts) | exit | actual |
|---|---|---|---|
| green | `population=79 ledger_rows=79 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET` | 0 | match |
| (a) | `ledger_rows=78 uncovered=1 dangling=0 bad_pointer=0 empty_desc=0` | 1 | match |
| (b) | `ledger_rows=79 bad_pointer=5` | 1 | match |
| (c) | `empty_desc=44` | 1 | match |
| (d) | `ledger_rows=82 dangling=3` | 1 | match |
| (e) | `population=79 verdict=TARGET_MISSED ledger=absent` | 1 | match |
| fixture base | `population=79 verdict=TARGET_MISSED ledger=absent` | 1 | match |
| `--selftest` | `LEDGER_SELFTEST: 50/50 passed` (42/42 on the 07:01 draft bytes) | 0 | match |

The draft also emits one `LEDGER-ROW reason=… path=… detail=…` finding line per
defect before the summary (e.g. `reason=bad_pointer path=tools/mado-terminal.py
detail=pointer-lacks-basename:DECOY.md`), so attribution is per-row, not only counted.

### 3c. Schema delta the freeze must resolve

`actual-run/frozen-line-vs-gate-schema.txt`:

1. **Prefix.** The frozen predicate line starts `C1_R51:`; the draft prints `LEDGER:`.
   The counter `quality/counters/c1-r51-ledger.py` must emit the frozen prefix
   (either by wrapping the draft or by the draft adopting it).
2. **`selftest=ok`.** The frozen line carries it; the draft's normal run has no
   selftest field (it has a 50-case `--selftest`, receipt `gate-selftest.txt`).
3. **`--work`.** The frozen command passes `--work <scratch>`; the draft rejects
   `--work` outside `--selftest` with exit 2 (`actual-run/gate-work-flag.txt`).
   The wrapper must accept `--work` itself and not forward it.
4. **Absent-ledger order.** The draft matches claims (`verdict=TARGET_MISSED
   ledger=absent`); the seat build printed the two fields in the other order (both
   present). Freeze the draft's order.

Additional receipts:

* `actual-run/population-per-rev.txt` — P=79 at every fixture rev and at the lane base.
* `actual-run/rev-scope-worktree-green-rev-mut-a.txt` — worktree ledger is the green
  one (`85410244…`), `mut-a` ledger is `7cb03d7e…`; `--rev mut-a` reports
  `uncovered=1 ledger_rows=78`, proving the counter reads the revision, not the tree.
* `actual-run/work-guard.txt` — `--work /tmp/…` refused (exit 2), `TMPDIR` honoured,
  unknown rev is a setup error (exit 2), `$HOME` work dir refused.
* `actual-run/selftest.txt` — 9/9 hermetic cases, exit 0.

## 4. What the freeze must pin, and what stays implementation-dependent

1. **Absent-ledger line.** claims.md freezes `verdict=TARGET_MISSED ledger=absent`
   for the base; a counter that only emits the common line cannot satisfy (e).
   The tracked instrument must emit that exact form (field order as above) or the
   claim and the instrument disagree.
2. **Row syntax.** The expected numbers assume the table row form above. If the
   tracked ledger uses a different row grammar, controls (a)–(d) must be rebuilt
   with it; the *values* (P−1, 5, 44, P+3) are grammar-independent, the parse is not.
3. **Duplicate rows.** The frozen sentence says "exactly once" but the frozen line
   has no duplicate field. This build charges duplicates to `dangling`; if the
   tracked instrument instead rejects via a separate field, the claim's line schema
   must be extended before the freeze (no control in (a)–(d) is affected).
4. **Dangling-row pointer/description checks.** This build reports dangling rows only
   as `dangling`; in control (d) their pointers resolve to a file that does contain
   the basenames, so a build that *also* checks pointers on dangling rows still
   yields `bad_pointer=0` — (d) is robust either way.
5. **Pointer content scope.** "contains the file's basename" is checked against the
   whole file at `<rev>` (a `path:line` pointer is resolved to its file). A stricter
   line-scoped reading would still MISS (b), because `DECOY.md:1` lacks every one of
   the five basenames and the file itself names none of them.
6. **Green baseline is deliberately synthetic** (`ACCOUNT.md` index). It certifies
   machine-checkability of the predicate, not that a real ledger's pointers are
   *meaningful*; a mechanically complete ledger with one reused description and an
   index pointer still passes, exactly as `CritLedgerControls` predicted.
7. **Draft is in flight.** The graded bytes are sha256
   `6dd4061c1d8a82d5a9efa8ae954ff1c4559e43abefbb69210fa831bd758a98d4`; if
   ExecLedgerGate revises the draft before the freeze, re-run
   `controls-c1/verify-gate.py` against `actual-run/gate-*.txt` regenerated with the
   final bytes. The counts above are invariant to the row grammar (both instruments
   parse the same table form).
8. **Description placeholder rule.** The draft additionally treats `-`, `?`, `TBD`,
   `TODO`, `N/A`, `none` as empty (beyond the frozen "non-empty" wording). No control
   depends on that rule — (c) uses truly empty cells — but a ledger that fills the
   44 counter rows with `TODO` would MISS under the draft and could pass a literal
   reading of the claim. The freeze should state which rule it intends.

## 5. Hygiene

* Writes: only this seat dir and `/fast/scratch/hyaku/mado-r51/ExecControlsC1/`
  (deleted); `mkdir -p` + fresh `git init` sandbox; no clone of the lane, no
  mutating git in the lane or fleet. All lane reads via `git -C … show/ls-tree`.
* No harness/lane file edited; no pacman, no service action, no PATH writes.
