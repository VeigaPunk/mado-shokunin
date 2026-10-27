ExecLedgerCounter — PRED-C1-r51 counter: the tracked lane-level tool ledger, measured

status: COMPLETE (draft + receipts, re-measured against the final gate and ledger bytes; nothing
tracked was edited, integration is the L1's call)

## Deliverables

- `.ufo/waves/round-51/w1/ExecLedgerCounter/c1-r51-ledger.py`
- `.ufo/waves/round-51/w1/ExecLedgerCounter/fixtures/build-fixtures.py`
- `.ufo/waves/round-51/w1/ExecLedgerCounter/fixtures/rehearse-integration.py`
- `.ufo/waves/round-51/w1/ExecLedgerCounter/receipts/base-and-setup.txt`
- `.ufo/waves/round-51/w1/ExecLedgerCounter/receipts/fixtures.txt`
- `.ufo/waves/round-51/w1/ExecLedgerCounter/receipts/rehearsal.txt`
- `.ufo/waves/round-51/w1/ExecLedgerCounter/receipts/scratch-and-defaults.txt`

Draft target path for integration: `quality/counters/c1-r51-ledger.py`
(sha256 `d5c2447d098681251fd41c04414d4e8823b41b78f150a5fc6bedd526a4a35b56`, 445 lines).
Measured against `ExecLedgerPopulation/tool-ledger.md` sha256 `c0a89805f4e5b7362d74763c3ef2aad0def8adb9664dc3c7845b6c381f382e25`
(79 rows) and `ExecLedgerGate/check-tool-ledger.py` sha256 `6dd4061c1d8a82d5a9efa8ae954ff1c4559e43abefbb69210fa831bd758a98d4`
(`--selftest` `50/50 passed`).

## What it does

`python3 -I c1-r51-ledger.py --repo <lane> --rev <rev> --work <scratch> [--checker PATH]`

1. Resolves `--rev` to a full commit in `--repo`, makes `git clone --shared --no-checkout` inside
   `--work` and `checkout --detach <rev>`; asserts clone HEAD and toplevel. The clone is removed on
   exit, together with `--work` when the counter created it (`--work` defaults to a fresh directory
   under `TMPDIR`; no temporary path is hard-coded — the only `/tmp`-family literal in the file is
   the `REFUSED_ROOTS` list used to print a diagnostic hint).
2. Derives the population itself from one `git ls-tree -r --name-only <rev>`: every file under
   `tools/` + direct children `quality/*.py` + direct children `quality/counters/*.py`
   (`__pycache__`/`.pyc`/`.pyo` excluded). Base `6ca8c559` → **P=79** (tools 17, quality/*.py 18,
   quality/counters/*.py 44, independently reproduced); the data rev with the gate and this counter
   → **P=81**. Field order on the line is the frozen order.
3. Parses `quality/tool-ledger.md` at `<rev>`: three-cell pipe rows, path in cell 1, description in
   cell 2, pointer(s) in cell 3; header/separator rows and rows whose first cell carries no `/` are
   not rows, and fenced code blocks are documentation — as in the gate. Measures `uncovered`,
   `dangling`, `bad_pointer`, `empty_desc`, plus a `dup` printed only when non-zero. `bad_pointer` =
   no pointer token names a file that exists at `<rev>` whose bytes contain the row file's basename
   (`:N`/`:N-M` suffixes stripped, never content-validated).
4. Runs the gate — the lane's `quality/check-tool-ledger.py` (or `--checker`) **from the clone at
   the same revision** — as `python3 -I <clone>/<checker> --repo <clone> --rev <rev>` in a sandbox
   whose `HOME`, `TMPDIR` and `XDG_*` live under `<work>/sandbox-<pid>`, and requires its `LEDGER:`
   line to be `TARGET_MET` **and** its six numbers to equal this counter's own independent
   measurement. Then `--selftest --work <sandbox>/selftest` must exit 0 with `n/n passed`
   (n == total); the bare `--selftest` fallback is used only on an argparse "unrecognized arguments"
   exit 2, and the receipt records which form ran (`form=with-work` in every receipt here).

Exit 0 only when every field is clean, the ledger has one row per population file, the gate line
agrees and the gate selftest passes; 1 for any ledger defect or an absent ledger; 2 for setup
errors (bad repo/rev/work/checker, clone failure, gate timeout).

The docstring carries the frozen predicate sentence byte-for-byte from `claims.md` — verified: the
eight `> PRED-C1-r51:` lines compare equal to the counter's docstring lines.

## Receipted evidence

- `receipts/base-and-setup.txt` — lane at base `6ca8c559`:
  `C1_R51: verdict=TARGET_MISSED ledger=absent population=79 rev=6ca8c559…`, exit 1. Same at the
  claims tip `d2740281` (ledger not integrated yet), exit 1. Short rev `6ca8c55` resolves and the
  line prints the full commit. Setup errors (nonexistent repo, unknown rev, `--checker ../x.py`)
  → exit 2 with `C1_R51: setup=error detail=…`.
- `receipts/fixtures.txt` — synthetic repository (population 5, complete ledger, stand-in gate),
  built by `fixtures/build-fixtures.py` under `--scratch`, 13 recorded runs:

  | case | counter line (tail) | exit |
  |---|---|---|
  | complete ledger | `population=5 ledger_rows=5 … selftest=ok verdict=TARGET_MET` | 0 |
  | omit `tools/beta.sh` | `ledger_rows=4 uncovered=1 …` | 1 |
  | pointer `docs/missing.md` | `bad_pointer=1 …` | 1 |
  | description `-` | `empty_desc=1 …` | 1 |
  | row for `tools/ghost.py` | `dangling=1 …` | 1 |
  | duplicate row | `dup=1 …` (also `ledger_rows=6`) | 1 |
  | gate selftest fails | `selftest=failed …` | 1 |
  | parroting gate over a ledger missing a row | `uncovered=1 … checker=failed` | 1 |
  | gate advertises population=6 | `checker=failed (disagree population checker=6 counter=5)` | 1 |
  | fenced example naming `tools/ghost.py` | `ledger_rows=5 dangling=0 … TARGET_MET` | 0 |
  | ledger file removed | `verdict=TARGET_MISSED ledger=absent` | 1 |
  | bogus rev | `setup=error` | 2 |

  The fenced row is the parity case: a fenced grammar example never becomes a ledger row, so both
  instruments stay MET.
- `receipts/rehearsal.txt` — integration rehearsal (`fixtures/rehearse-integration.py`): scratch
  clone of the lane at `d2740281`, the real drafts committed at their tracked paths.
  stage-a (drafts only, 79 rows vs population 81):
  `C1_R51: population=81 ledger_rows=79 uncovered=2 … checker=failed verdict=TARGET_MISSED` exit 1,
  gate line `LEDGER: population=81 ledger_rows=79 uncovered=2 …`. stage-b (the two owed rows added,
  seat reports committed beside them): gate `LEDGER: population=81 ledger_rows=81 uncovered=0
  dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET` exit 0, and
  `C1_R51: population=81 ledger_rows=81 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0
  selftest=ok verdict=TARGET_MET` exit 0, with the gate's `--selftest` reporting `50/50 passed`.
  stage-c (the two rows instead point at `.ufo/waves/round-51/claims.md:20` and `:21`, and the
  seat reports are removed): gate and counter both `population=81 ledger_rows=81 uncovered=0
  dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET`, exit 0 — so the freeze does not depend
  on any round-51 seat report being committed.
- `receipts/scratch-and-defaults.txt` — default `--work` honours `TMPDIR` and the directory it
  creates is gone afterwards (0 entries); an absent `--checker` at the rev yields
  `selftest=absent checker=absent … verdict=TARGET_MISSED`; `--work` holds no clone or sandbox
  residue after any run.

Honest limitation of the receipted green: the fixture and rehearsal gate is the lane's own gate in
a scratch clone. A parroting gate is caught only numerically (the counter compares the six fields
against its own parse); the counter cannot certify that a numerically matching gate reached those
numbers the same way.

## Findings for the freeze / integration (read before the w2 freeze)

1. **Two rows are owed at the data rev.** The ledger draft covers the 79 base instruments; at the
   integrated tip the population is 81 (gate + this counter). Stage-a of the rehearsal is exactly
   that MISS (`uncovered=2`), and the ledger draft itself names the debt. Integration must add a row
   for each. Two pointer targets were measured: the seat reports
   (`.ufo/waves/round-51/w1/ExecLedgerGate.md` / `.ufo/waves/round-51/w1/ExecLedgerCounter.md`,
   stage-b) and `.ufo/waves/round-51/claims.md:20` / `:21`, which is committed at `d2740281` and
   already names both basenames (stage-c, no round-51 seat report present) — both give
   `population=81 ledger_rows=81 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0` from the gate
   and from this counter. `claims.md` is the more durable target; the seat reports are the fallback.
2. **Pointer durability is the fragile part of the predicate.** Any row pointed at a seat report or
   a round-51 receipt that is later deleted, moved or squashed becomes `bad_pointer` at the tip it
   is measured from. The 79 existing rows are durable (SCORECARD.md, PROVINCE.md, corpus/lessons,
   corpus/QUALITY.md, round registrations) and produced `bad_pointer=0` at stage-a with no seat
   report committed; the two owed rows are the only seat-report pointers, and only because those
   two instruments have no other naming file at the data rev.
3. **Gate `--selftest` work root.** The gate refuses `--work` under `/tmp`, `/var/tmp`, `/dev/shm`
   and `$HOME`. Pass a `--work`/`TMPDIR` on `/fast/scratch/…`; the counter prints a hint when a
   selftest fails while the work root is in a refused tree.
4. **Divergences from the gate, all bounded.** (a) The gate counts duplicate and malformed rows as
   `dangling`; this counter reports repeats as `dup` and skips rows whose first cell is not a path
   (those surface as `uncovered`). (b) The gate's pointer containment is name-bounded
   (`not-alpha-tool.py` does not cover `alpha-tool.py`); this counter uses the literal substring
   containment the frozen sentence states. Because the gate's line must agree with the counter's
   numbers, the gate stays binding in every case: the counter cannot pass a ledger the gate rejects,
   and a ledger this counter rejects cannot pass on the gate's word alone.

## Risks

- A ledger row whose description contains a literal `|` splits into four cells; the gate calls it
  `dangling`, the counter reads the tail as part of the pointer. Both MISS, but the counter's
  `dangling` field then under-reports and the gate field is the authoritative one (the ledger draft
  is pipe-free by construction, confirmed by its seat).
- The counter's `checker=` requirement couples the freeze to the gate's `LEDGER:` field names and
  its 0/1/2 exit map. Confirmed against the final gate build and agreed by message with
  `ExecLedgerGate`; a frozen gate that renames a field or changes the absent-ledger wording would
  turn the counter's verdict into `TARGET_MISSED` without a ledger defect.

## Scratch and hygiene

- Scratch: `/fast/scratch/hyaku/mado-r51/ExecLedgerCounter/` (fixture repository, rehearsal clone,
  `--work` trees, transcripts) — **deleted** at the end of this seat; the receipts above are the
  retained evidence.
- Disk guard checked before the heavy passes: `/fast/scratch/hyaku` 66% used, 279.4 G free.
- No tool installed or upgraded; no pacman transaction; no compositor socket, no host service, no
  config plane touched. Lane worktree: `git diff --name-only` empty — every write is under this
  seat directory (plus its own scratch, now gone).

Report: .ufo/waves/round-51/w1/ExecLedgerCounter.md
