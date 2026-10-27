# ExecDiskHygiene — scratch-rule-4 verification of the round-51 w1 drafted tools

Seat: executor (leaf), wave `round-51/w1`, lane `mado-shokunin`, 2026-10-27.
Status: **DONE**. Verdicts, per-file table and selftest transcripts: `w1/ExecDiskHygiene/disk-hygiene.md`.

## What was measured

1. **Static sweep** of every `.py` drafted under `w1/` (20 files at the 07:05 snapshot) for
   hardcoded `/tmp`, `/var/tmp`, `/dev/shm` **write targets** (`mkdtemp(dir="/tmp…")`,
   `open("/tmp…")`, `mkdir`, `dump`), for `mkdtemp` / `TemporaryDirectory` /
   `NamedTemporaryFile` / `TemporaryFile` **without `dir=`**, and for `gettempdir()` used as a
   write target. Every literal found is classified as write target / sandbox argv (`--tmpfs /tmp`
   in a bwrap argv) / refusal-list entry / comment.
2. **Runtime cases** for the tools that have an `--selftest` or a real invocation, each run as
   `python3 -I <tool> …` under `env -i`-style environment with `TMPDIR` inside seat scratch, and
   each `isolate_tmp` case inside `unshare -Urm` with fresh tmpfs mounts over `/tmp` and
   `/var/tmp` — so what a tool writes to `/tmp` is *listed afterwards*, not assumed.
3. **Refusal probes**: an existing `--work /tmp/...` and `TMPDIR=/tmp` must exit 2 (scratch rule 4:
   `corpus/lessons/round-48.md:372`, `SCORECARD.md:2728`).

## Verdicts

| object | verdict |
|---|---|
| hardcoded `/tmp` write target in any drafted `.py` | **none** — 0 DEFECT across 20 files, 13 CLEAN, 7 REVIEW (no hardcoded write in the REVIEW rows either) |
| `python3 -I` | **PASS** on every tool this seat executed (all invocations used `-I`; no site, `PYTHONPATH` or cwd dependence) |
| `ExecLedgerGate/check-tool-ledger.py` (C1 checker) | **rule-4 PASS**; `--selftest` green `LEDGER_SELFTEST: 50/50 passed`, exit 0, `/tmp` residue 0; refuses `--work /tmp` (exit 2), `TMPDIR=/tmp` (exit 2), missing `TMPDIR` (exit 2) |
| `ExecLedgerCounter/c1-r51-ledger.py` (C1 counter) | base case green (`TARGET_MISSED ledger=absent population=79`, exit 1, no `/tmp` residue); fixture `TARGET_MET … selftest=ok` reached through the real checker; **rule-4 MISS** — accepts `--work /tmp/...` and `TMPDIR=/tmp` |
| `ExecCounterC2/c2-r51-dispatch-entry.py` (C2 counter) | base case green (`admitted=0/1 verdict=TARGET_MISSED`, exit 1, no `/tmp` residue); **rule-4 MISS** — accepts `--work /tmp/...` and `TMPDIR=/tmp`, writes `c2-r51-probe.json` there, and leaves an auto-created `/tmp` work dir behind |

`c1`'s `REFUSED_ROOTS` constant exists but is only used to print a *hint* when the checker selftest
fails; it does not gate `--work`/`TMPDIR`. `c2`'s root cause is `os.environ.get("TMPDIR") or
tempfile.gettempdir()` — a silent `/tmp` substitution.

## Routed (advisory; the L1 owns the freeze, this seat edited no sibling file)

- **R-C1-rule4** — `c1-r51-ledger.py` must refuse a `/tmp` `--work`/`TMPDIR` (copy
  `REFUSED_WORK_PREFIXES` from the same wave's checker, exit 2).
- **R-C2-rule4** — `c2-r51-dispatch-entry.py` same, plus: remove its auto-created work dir, and the
  `--work` must-exist vs auto-create disagreement with `c1` picked one way for the freeze.
- These are exactly the round-48 `SentScratch` route; a w2 sentinel will re-open them if the
  frozen predicate receipts do not address them.

## Evidence (exact, retained in seat dir)

- `receipts/static-scan.json` — per-file findings, class and line, for all 20 drafts.
- `receipts/checker-selftest.txt` — `LEDGER_SELFTEST: 50/50 passed`, `EXIT=0`, namespace `/tmp`
  and `/var/tmp` empty afterwards.
- `receipts/checker-work-slash-tmp.txt` — `refusing work dir under /tmp …`, `EXIT=2`, residue empty.
- `receipts/checker-probe.json`, `receipts/checker2-probe.json` — refusal matrix incl. `TMPDIR` unset.
- `receipts/c1-base.txt` — `C1_R51: verdict=TARGET_MISSED ledger=absent population=79 …`, `EXIT=1`.
- `receipts/c1-work-slash-tmp.txt` — accepted `/tmp/dh-probe-c1`, `EXIT=1`, residue `/tmp/dh-probe-c1`.
- `receipts/c1-r51-probe.json` — four-case matrix (base, `--work /tmp`, `TMPDIR=/tmp`, TMPDIR-only).
- `receipts/c2-base.txt`, `receipts/c2-work-slash-tmp.txt`, `receipts/c2-tmpdir-slash-tmp.txt`,
  `receipts/c2-probe.json` — base MISS with empty residue; `/tmp` acceptance with
  `c2-r51-probe.json` and a leaked `/tmp/c2-r51-*` dir.
- `receipts/anchors-probe.json` (`verify-anchors.py` selftest 6/6, residue 0),
  `receipts/build-fixtures.txt` (fixture builder, `selftest=ok verdict=TARGET_MET`, residue 0),
  `receipts/probeclauses-probe.json` (control probe, residue 0).

## Churn note

The authoring seats were still editing while this seat ran: `c1-r51-ledger.py` was measured on four
successive hashes with an identical rule-4 result, `c2-r51-dispatch-entry.py` on five, and
`check-tool-ledger.py` moved from `34/46` (failing) to `42/42` to `50/50` (green). The two commands
in `disk-hygiene.md` (§Method) reproduce every verdict on frozen bytes; re-run them before the
freeze, since the verdict rows name the hashes actually judged.

## Scratch

All clones, fixtures and probe work lived under `/fast/scratch/hyaku/mado-r51/ExecDiskHygiene/` and
nothing in `/tmp` outside the private namespaces; the scratch dir was removed at seat end after
the receipts above were copied into this seat directory.

## Deliverables

- `.ufo/waves/round-51/w1/ExecDiskHygiene.md`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/disk-hygiene.md`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/hygiene-scan.py`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/selftest-probe.py`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/recheck.sh`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/specs/c1-r51.json`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/specs/c2.json`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/specs/checker2.json`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/receipts/static-scan.json`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/receipts/checker-selftest.txt`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/receipts/checker-work-slash-tmp.txt`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/receipts/checker-probe.json`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/receipts/checker2-probe.json`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/receipts/c1-base.txt`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/receipts/c1-work-slash-tmp.txt`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/receipts/c1-r51-probe.json`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/receipts/c2-base.txt`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/receipts/c2-work-slash-tmp.txt`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/receipts/c2-tmpdir-slash-tmp.txt`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/receipts/c2-probe.json`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/receipts/anchors-probe.json`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/receipts/build-fixtures.txt`
- `.ufo/waves/round-51/w1/ExecDiskHygiene/receipts/probeclauses-probe.json`

Report: .ufo/waves/round-51/w1/ExecDiskHygiene.md
