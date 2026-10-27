# disk-hygiene — scratch-rule-4 verification of the round-51 w1 drafted tools

Seat: `ExecDiskHygiene` (executor, leaf). Lane: `mado-shokunin`. Wave: `round-51/w1`, 2026-10-27.
Scratch used: `/fast/scratch/hyaku/mado-r51/ExecDiskHygiene/` (removed at seat end; receipts copied here first).

Rule under test — scratch rule 4 (as amended round 49; `corpus/lessons/round-48.md:372`,
`SCORECARD.md:2728`): a counter / probe / gate MUST honour `TMPDIR`, MUST accept an explicit
scratch argument, and MUST refuse a `--work` or `TMPDIR` under `/tmp`, `/var/tmp` or `/dev/shm`
(a hardcoded `/tmp` is a routed defect).

## Verdict summary

| object | verdict |
|---|---|
| hardcoded `/tmp` / `/var/tmp` write targets in any drafted `.py` | **0** across 20 files |
| `python3 -I` compatibility of every drafted `.py` run this seat performed | **PASS** (every invocation used `-I`; no `PYTHONPATH`, no user site, no cwd on `sys.path`) |
| `quality/check-tool-ledger.py` (C1 checker) scratch rule 4 | **PASS** — refuses `--work /tmp`, `TMPDIR=/tmp`, and a missing `TMPDIR`; selftest 50/50 |
| `quality/counters/c1-r51-ledger.py` (C1 counter) scratch rule 4 | **MISS (routed)** — accepts `--work /tmp/...` and `TMPDIR=/tmp`; never refuses, only prints a hint |
| `quality/counters/c2-r51-dispatch-entry.py` (C2 counter) scratch rule 4 | **MISS (routed)** — accepts `--work /tmp/...` and `TMPDIR=/tmp`, writes a probe file there, and leaves its auto-created work dir behind |
| other 17 drafted `.py` | no hardcoded tmp write; 5 write only to caller-supplied explicit paths, 4 are read-only, the rest use `TMPDIR`/`--work`/`--scratch` |

None of the three primary drafts writes any host `/tmp` path unconditionally: there is no
`mkdtemp(dir="/tmp")`, no `open("/tmp/...")`, no `NamedTemporaryFile`/`TemporaryDirectory`
without `dir=`, and no `tempfile.gettempdir()` used as a write target in the primary drafts.
The defect class actually present is *acceptance* of a `/tmp` scratch root, not a hardcoded one.

## Method

Two instruments, both written this seat (seat-local, not deliverables for tracked paths):

1. `hygiene-scan.py` — static. Per line: a `/tmp`,`/var/tmp`,`/dev/shm` literal is classified
   `hardcoded-tmp-write` (used as a write target → DEFECT), `sandbox-argv` (bwrap argv such as
   `--tmpfs /tmp`: the `/tmp` is private to the sandbox), `refusal-list` (an entry of a refusal
   check), or `mention`; every `mkdtemp|TemporaryDirectory|NamedTemporaryFile|TemporaryFile`
   call without `dir=` is `implicit-tempdir-*`; a file with no `TMPDIR`, no `--work`/`--scratch`
   and no sandbox is `ambient-no-contract`. It creates no temporary directory itself.
2. `selftest-probe.py` — runtime. Each case runs `python3 -I <tool> …` with a minimal explicit
   environment (`env -i`-equivalent: `PATH`, `HOME`, `LANG`, `TZ`, plus the case's `TMPDIR`).
   `isolate_tmp` cases run inside `unshare -Urm` after `mount -t tmpfs tmpfs /tmp` and
   `mount -t tmpfs tmpfs /var/tmp`, so **what the tool writes to `/tmp` is listed afterwards** —
   measured, not inferred. A refused `/tmp` scratch is asserted as `exit 2`.

Commands (verbatim, seat scratch `$S=/fast/scratch/hyaku/mado-r51/ExecDiskHygiene`):

```
python3 -I <seat>/hygiene-scan.py --root <lane>/.ufo/waves/round-51/w1 \
        --json .../ExecDiskHygiene/receipts/static-scan.json
python3 -I <seat>/selftest-probe.py --spec $S/spec/checker2.json  --scratch $S/run
python3 -I <seat>/selftest-probe.py --spec $S/spec/c1-r51.json    --scratch $S/run
python3 -I <seat>/selftest-probe.py --spec $S/spec/c2.json        --scratch $S/run
python3 -I <seat>/selftest-probe.py --spec $S/spec/helpers.json   --scratch $S/run
python3 -I <seat>/selftest-probe.py --spec $S/spec/buildfix2.json --scratch $S/run
```

One-shot re-run on frozen bytes (specs persisted in the seat dir, scratch argument required):

```
sh <seat>/recheck.sh /fast/scratch/hyaku/mado-r51/ExecDiskHygiene/recheck
```

runs the static scan plus the `c1-r51`, `c2` and `checker2` probe matrices and leaves four JSON
receipts in that scratch dir. Verified working at 07:07 on the then-current bytes: checker
`50/50`, `c1` and `c2` rule-4 MISS as tabulated.

## Per-file verdicts (static, `receipts/static-scan.json`)

`SCAN files=20 clean=13 review=7 defect=0` (snapshot 2026-10-27 07:05; the wave was still being
written — the two commands in "Method" reproduce this on any later byte set).

| file (under `w1/`) | static | hardcoded tmp write | TMPDIR | scratch arg | selftest | note |
|---|---|---|---|---|---|---|
| `ExecLedgerGate/check-tool-ledger.py` | CLEAN | 0 | yes | `--work` | yes | `REFUSED_WORK_PREFIXES = ("/tmp","/var/tmp","/dev/shm")` L69 |
| `ExecLedgerCounter/c1-r51-ledger.py` | CLEAN | 0 | yes | `--work` | no (checker's) | `REFUSED_ROOTS` L67 is a *hint* only, not a check |
| `ExecCounterC2/c2-r51-dispatch-entry.py` | CLEAN | 0 | yes | `--work` | no | `TMPDIR or tempfile.gettempdir()` L525 → silent `/tmp` fallback; no refusal |
| `SentScope51/check-scope.py` | CLEAN | 0 | yes | `--scratch` | yes | literal L499 is the embedded fixture source, not a write |
| `ExecFetchDispatch/verify-anchors.py` | REVIEW | 0 | yes | `--scratch` | yes | L100 `mkdtemp(prefix=…)` with no `dir=`: honours `TMPDIR`, does not refuse `/tmp` |
| `ExecLedgerCounter/fixtures/build-fixtures.py` | REVIEW | 0 | yes | `--scratch` | none (`--selftest` exists only in its embedded fixture source) | L183 `… or tempfile.mkdtemp()`; measured: writes only under `--scratch`/`TMPDIR` |
| `ExecLedgerCounter/fixtures/rehearse-integration.py` | CLEAN | 0 | yes | `--work` | no | static only |
| `ExecControlsC2/controls-c2/drive-controls-c2.py` | CLEAN | 0 | yes | `--work` | no | exports `TMPDIR=work` to the counter (L118) |
| `ExecControlsC2/controls-c2/probe-clauses.py` | CLEAN | 0 | yes | none | no | measured: TMPDIR-only run left `/tmp` empty |
| `ExecCounterC2/mutants.py` | CLEAN | 0 | yes | `--work` | no | static only |
| `ExecControlsC1/controls-c1/check-tool-ledger.py` | CLEAN | 0 | yes | `--work` | yes | mutant copy of the checker; `for bad in ("/tmp",…)` L322 |
| `ExecControlsC1/controls-c1/make-fixture.py` | REVIEW | 0 | no | required `--fixture` | no | writes only to the caller-supplied `--fixture` path; creates no temp dir |
| `ExecControlsC1/controls-c1/verify-controls.py` | REVIEW | 0 | no | none | no | read-only (opens receipt files for read only) |
| `ExecCounterC2/make-fixture.py` | REVIEW | 0 | no | required `--fixture` | no | writes only to the caller-supplied `--fixture` path |
| `ScrLedgerRows/build-ledger-rows.py` | CLEAN | 0 | yes | none | no | static only |
| `ScrRowsDispatch/verify-quotes.py` | REVIEW | 0 | no | none | no | read-only: no write calls at all |
| `ExecControlsC1/controls-c1/verify-gate.py` | REVIEW | 0 | no | none | no | read-only: no write calls |
| `SimplifierLedger/ref-minimal-c1.py` | CLEAN | 0 | no | `--work` | flag present | measured at base: exit 1 `ledger=absent`, `/tmp` residue 0 |
| `ExecDiskHygiene/hygiene-scan.py` | CLEAN | 0 | yes | — | no | the scanner itself; literal L64 is a comment |
| `ExecDiskHygiene/selftest-probe.py` | CLEAN | 0 | yes | `--scratch` | — | the probe; `TMPISH` L36 is a refusal list |

The seven REVIEW rows are "no scratch contract" or "implicit `mkdtemp`": none of them writes a
host `/tmp` path deliberately, and the two measured ones (`verify-anchors.py`,
`build-fixtures.py`) left `/tmp` empty under the isolated namespace.

## Selftest receipts (primary C1/C2 drafts)

All runs: `python3 -I`, `env -i`-equivalent, `TMPDIR` inside seat scratch, private tmpfs `/tmp`
and `/var/tmp`.

### `check-tool-ledger.py` — GREEN

`receipts/checker-selftest.txt`:

```
LEDGER_SELFTEST: 50/50 passed
EXIT=0
--- host /tmp residue in this namespace:
```

(empty residue). Refusal cases, `receipts/checker-work-slash-tmp.txt`:

```
check-tool-ledger.py: refusing work dir under /tmp (got /tmp/dh-selftest): use a scratch filesystem
EXIT=2
--- namespace /tmp residue:
```

`TMPDIR=/tmp` → same refusal, exit 2. `TMPDIR` unset and no `--work` → exit 2:
`--selftest needs --work <dir> or a TMPDIR outside /tmp, /var/tmp, /dev/shm and the home directory`
(`receipts/checker2-probe.json`). This is the rule-4 shape the other two counters should copy.

Note: earlier snapshots of the same file failed their own suite (`34/46 passed`, self-reporting
`expected=36 got=45` at 07:00) and then passed `42/42` at 07:01; the last measured bytes pass
`50/50`. The suite keeps growing with every author edit, so the verdict applies to the hash named
at the end of this file — re-run `--selftest` once the bytes are frozen.

### `c1-r51-ledger.py` — frozen base case GREEN, scratch rule 4 MISS

`receipts/c1-base.txt`:

```
detail: quality/tool-ledger.md absent at 6ca8c559a4a3
C1_R51: verdict=TARGET_MISSED ledger=absent population=79 rev=6ca8c559a4a3d6d361101592116eea2bc7452437
EXIT=1
--- namespace /tmp residue:
```

(empty residue; the clone it makes in `--work` is removed on exit — the `--work` dir was empty
afterwards.) `--work` inside scratch and `TMPDIR`-only default both stay in scratch.

`receipts/c1-work-slash-tmp.txt` — an **existing** `--work /tmp/dh-probe-c1` is accepted:

```
C1_R51: verdict=TARGET_MISSED ledger=absent population=79 rev=6ca8c559a4a3d6d361101592116eea2bc7452437
EXIT=1
--- namespace /tmp residue:
/tmp/dh-probe-c1
```

The counter's own frozen-TARGET_MET path is green through the real checker, measured by the
seat's fixture builder under the same isolated `/tmp` (`receipts/build-fixtures.txt`):

```
== fixture complete ledger -> exit 0
detail: checker selftest ok (ratio=6/6 form=with-work)
detail: checker ledger ok (rev=d4dd0c697ef3afbe879c85089e28e70829ddea03)
C1_R51: population=5 ledger_rows=5 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=d4dd0c697ef3afbe879c85089e28e70829ddea03
```

i.e. `selftest=ok` in the final line is produced by the checker's own `--selftest`, and the run
left `/tmp` and `/var/tmp` empty.

`TMPDIR=/tmp` with no `--work` is accepted too (exit 1, the auto-created dir is removed after the
run, so the `/tmp` write is transient rather than persistent — still an accepted `/tmp` scratch).
`TMPDIR` unset falls back to `tempfile.mkdtemp(dir=None)` → `/tmp`, same class.
Re-measured on three successive byte versions of the file with identical results.

### `c2-r51-dispatch-entry.py` — frozen base case GREEN, scratch rule 4 MISS + leak

`receipts/c2-base.txt`:

```
C2_R51: clauses=abcd clauses_met=0 admitted=0/1 verdict=TARGET_MISSED rev=6ca8c559a4a3d6d361101592116eea2bc7452437
EXIT=1
--- namespace /tmp residue:
```

(empty residue). `receipts/c2-work-slash-tmp.txt` — an existing `--work /tmp/dh-probe-c2` is
accepted and written:

```
C2_R51: work=/tmp/dh-probe-c2 probe=written
EXIT=1
--- namespace /tmp residue:
/tmp/dh-probe-c2
/tmp/dh-probe-c2/c2-r51-probe.json
```

`receipts/c2-tmpdir-slash-tmp.txt` — `TMPDIR=/tmp` is accepted, and the auto-created work dir is
**not** removed (persistent leak, unlike c1):

```
C2_R51: meta rev=… work=/tmp/c2-r51-pwfijuoq
C2_R51: work=/tmp/c2-r51-pwfijuoq probe=written
EXIT=1
--- namespace /tmp residue:
/tmp/c2-r51-pwfijuoq
/tmp/c2-r51-pwfijuoq/c2-r51-probe.json
```

`--work` also must already exist here: a non-existent `--work` is exit 2
`setup error: --work is not a directory`, where `c1-r51-ledger.py` creates it. Inconsistent
CLI contract between the two counters.

## Other runtime checks

| tool | case | result |
|---|---|---|
| `ExecFetchDispatch/verify-anchors.py` | `--selftest`, TMPDIR in scratch | exit 0, `selftest: cases=6 wrong=0`, `/tmp` residue 0 (`receipts/anchors-probe.json`) |
| `ExecLedgerCounter/fixtures/build-fixtures.py` | `--scratch <scratch>` | exit 0, residue 0; fixture ledger run prints `TARGET_MET … selftest=ok` then `checker=failed` per mutant, as designed (`receipts/build-fixtures.txt`) |
| same | no `--scratch`, `TMPDIR` only | exit 0, residue 0, fixture tree under `TMPDIR` (`receipts/c1-r51-probe.json` case set) |
| `ExecControlsC2/controls-c2/probe-clauses.py` | base rev, TMPDIR only | exit 1, `PROBE_C2_R51: clauses=abcd clauses_met=1 admitted=0/1`, residue 0 (`receipts/probeclauses-probe.json`) |
| `SentScope51/check-scope.py` | wave sweep, `--scratch` and TMPDIR-only | exit 1 (in-flight defects, expected), residue 0 both modes; its own scratch check reported `tmp_defects=0` (`receipts/checker-probe.json`) |

## Routing (advisory — the L1 owns the freeze; this seat edits no sibling file)

1. **R-C1-rule4**: `quality/counters/c1-r51-ledger.py` accepts a `/tmp` `--work` and `TMPDIR=/tmp`.
   Fix shape already present in the same wave: `ExecLedgerGate/check-tool-ledger.py`
   `REFUSED_WORK_PREFIXES` + exit 2. `c1`'s `REFUSED_ROOTS` exists but only prints a hint.
2. **R-C2-rule4**: `quality/counters/c2-r51-dispatch-entry.py` accepts both; additionally
   `TMPDIR`-default work dirs are never removed (`/tmp/c2-r51-*` leaks), and `--work` must
   pre-exist. `TMPDIR or tempfile.gettempdir()` (L525) is the root: it silently substitutes `/tmp`.
3. **R-CLI**: the two counters disagree on whether `--work` must exist; pick one for the freeze.
4. **R-hint**: if the freeze keeps any `/tmp` acceptance, the predicate receipts must state it, or
   a w2 sentinel will re-open it as scratch rule 4 (this is exactly the round-48 `SentScratch` route).

## Judged bytes

Static scan judged 20 `.py` under `w1/`; the primary drafts at the time of the green receipts:

| file | sha256 (first 12) |
|---|---|
| `ExecLedgerGate/check-tool-ledger.py` | `6dd4061c1d8a` (50/50, `/tmp` residue 0) |
| `ExecLedgerCounter/c1-r51-ledger.py` | `11fc2ca77047` (four successive hashes measured, identical rule-4 result) |
| `ExecCounterC2/c2-r51-dispatch-entry.py` | churned on every observation — `065625cea90f`, `1d3984f95001`, `b19059d2dcda`, `abf41d4b84f8`, `909e254d9f9d`, `b2515d65a5cc` — identical rule-4 MISS on each |

The authoring seats were still editing when this report was written; the rule-4 result was
stable across every hash this seat measured, so the verdict is not an artifact of a half-written
file. Re-run `hygiene-scan.py` + the three specs before the freeze to re-confirm on frozen bytes.

## Limitations

- The `/tmp` evidence is a private tmpfs inside a user+mount namespace (`unshare -Urm`); it
  observes host-path writes, not writes through an fd to another path.
- "Refusal" is asserted as `exit 2` (the setup-error code the frozen predicates use); a tool that
  refused a `/tmp` scratch with exit 1 would be scored MISS here even if it refused.
- Only the tools present when the scan ran are covered; `--selftest` was run where the tool has an
  actual `--selftest` entry point (the checker, `verify-anchors.py`, `check-scope.py`,
  `ExecControlsC1/.../check-tool-ledger.py`); helpers without one were verified by their real
  invocation instead.
