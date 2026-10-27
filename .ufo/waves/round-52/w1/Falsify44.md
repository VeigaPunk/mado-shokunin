# Falsify44 — C1 counter isolation/scratch behavior

Seat: Falsify44 (critic, leaf). Round 52, wave w1.
Target claim: C1 (operability) — new tool-ledger counter vs no-work control.
Primary attacked clause: the C1 counter's **isolation/scratch behavior** — the frozen
predicate (registration.md) names only uniqueness / resolvable pointer / non-self
pointer / instrument-specific context, and the committed "before" counter
(`quality/counters/c1-r51-ledger.py`) carries no enforced scratch gate of its own.
Supporting attacked clause: the "resolvable evidence pointer + non-self pointer"
pair as naively read does not exclude self-pointers into the ledger itself.

No tracked lane files touched. All fixtures and the mutable lane fork live under
`/fast/scratch/hyaku/mado-r52/Falsify44/`; receipts copied to this seat dir.
Source-only round respected: bytes read from the pinned base
`85d57a818c3707397e21c840b6498b105ba798aa`, no live probes, no package queries,
no installs.

## Findings

### F1 (primary, reproduced): the r51 counter has no scratch gate — refused roots are advisory, and the default work location is `/tmp`

Attacked: counter-level isolation. `c1-r51-ledger.py` defines
`REFUSED_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")` (line 68) but uses it only to
print a hint after a checker selftest failure (lines 405–407). Work resolution
(line 335: `tempfile.mkdtemp(prefix="c1-r51-", dir=TMPDIR-or-None)`) defaults to the
system tempdir, which is `/tmp` when `TMPDIR` is unset (verified:
`python3 -c 'import tempfile; print(tempfile.gettempdir())'` → `/tmp`).

Commands and actual results (full logs in `receipts/`):

1. Explicit refused root, production rev:
   `env -u TMPDIR python3 quality/counters/c1-r51-ledger.py --repo <lane> --rev 85d57a8… --work /tmp/f44-r51-explicit-work`
   → exit=1, `verdict=TARGET_MISSED`, `detail: checker selftest failed (exit=2 form=with-work)`,
   `detail: hint: the gate refuses --selftest work under /tmp, /var/tmp, /dev/shm`,
   while `checker ledger ok` ran fine from the `/tmp` clone. The counter accepted the
   refused root, cloned the repo there, and only the *checker's* selftest gate stopped
   the run. (`receipts/r51-work-tmp.log`; empty `/tmp/f44-r51-explicit-work` left
   behind — counter only refuses to create, never to use.)
2. Default location, production rev, no `--work`, `TMPDIR` unset:
   → same outcome (`receipts/r51-default-tmpdir.log`): the default evidence/clone
   location is `/tmp`.
3. Green baseline, identical command with `TMPDIR=/fast/scratch/hyaku/mado-r52/Falsify44`:
   → exit=0, `population=82 ledger_rows=82 … selftest=ok verdict=TARGET_MET`,
   matching the frozen base receipt `.ufo/waves/round-52/receipts/c1-base.txt`.
   (`receipts/r51-green-baseline.log`)
4. Where today's protection actually lives: in a scratch fork
   (`lane-fork`, rev `1bbc42af…`) I neutered *only* the checker's
   `REFUSED_WORK_PREFIXES` refusals (kept everything else byte-identical). The
   checker's own selftest then fails `47/50` with
   `FAIL refuse-work-tmp accepted`, `FAIL refuse-work-var-tmp accepted`,
   `FAIL refuse-work-dev-shm accepted`. Conclusion: scratch safety in the current
   instrument is enforced exclusively by the checker's selftest contract
   (`check-tool-ledger.py` cases refuse-work-*), which the frozen C1 predicate does
   not require. A new counter+checker written exactly to the frozen predicate can
   legally pass the production ledger with the full clone and selftest evidence
   under `/tmp`, exit 0 — the predicate has no scratch clause to fail it.
   (`receipts/r51-tmp-bypass.log`; fork left in scratch for inspection.)

Reproduced: **yes** (runs 1–4 above).

Impacted axis: **operability** (C1's own axis). Evidence integrity/availability of
the verification instrument depends on a gate that is (a) absent at the counter
layer and (b) not named in the frozen predicate, so it can regress without any
predicate violation. No effect on coverage.

Smallest safe correction: the new counter must hard-refuse work roots under
`/tmp`, `/var/tmp`, `/dev/shm` for both explicit `--work` and the TMPDIR-default
path (mirror `check-tool-ledger.py:resolve_work`), or default its work to a
non-refused scratch root; and the replacement checker must keep the
`refuse-work-tmp/var-tmp/dev-shm` selftest cases so the gate is receipt-visible.
This is additive to the frozen predicate (no predicate edit proposed — a build
requirement on the counter).

### F2 (supporting, reproduced): the before-design evidence rule passes a pure self-pointer; "non-self" must be defined against the ledger file

Attacked: "resolvable evidence pointer, non-self pointer" as naively implementable.
The committed `pointer_resolves` returns True whenever any tracked file *contains
the instrument basename*. A row for `tools/mado-verify.sh` whose pointer cell names
`quality/tool-ledger.md` therefore resolves — the ledger bytes contain
"mado-verify.sh" because the row names it.

Fixture (scratch, rev `849931ac…`): `tools/mado-verify.sh` + `quality/tool-ledger.md`
holding the verbatim frozen control `.ufo/waves/round-52/controls/c1-do-nothing.md`.
Harness imports the committed counter by path and reuses its own functions
(`receipts/harness-control-eval.py`, `.log`):

- Against the real control bytes: `pointer_tokens(pointer cell) = []` (the pointer
  cell is prose "nothing | generic accountability pointer to this ledger itself"),
  so the committed rule reports `pointer_resolves -> False`; the row's only
  path-like token sits in the **desc** cell and points at the ledger itself, with
  basename-in-bytes = True.
- Pathological variant (self-pointer in the pointer cell, the shape a slightly
  less lazy no-work ledger would use): `committed pointer_resolves -> True`,
  `non-self clause PASS under naive def (pointer != row-path) -> True`,
  `non-self clause PASS under ledger def (pointer != LEDGER_REL) -> False`.

Reproduced: **yes**.

Consequence for C1: if the new counter implements "non-self" as pointer-path ≠
row instrument path, the do-nothing class of control passes the resolvable+non-self
clauses outright. The smallest correction: non-self means no evidence pointer of
the row resolves to the ledger file itself (`quality/tool-ledger.md`), evaluated
over path-like tokens in the whole row (desc + pointer cells) — which also makes
the real frozen control fail **specifically for the self-pointer/context defects**
as registration requires, instead of misattributing to "pointer unresolvable"
(the control's pointer cell contains no path at all).

## Dissent / failed controls / limitations

- The r52 counter was **not yet committed** at review time (counters dir stops at
  `c1-r51-ledger.py`), so F1/F2 attack the committed before-design and the frozen
  predicate text — the template any r52 implementation is copied from — not a
  sibling's draft. No peer draft was readable.
- F1's end-to-end "pass under /tmp" was demonstrated by gate-neutering simulation
  (run 4); the unmodified instrument fails safe today via the *checker's* gate.
  The report claim is precisely that this safety is unpredicate-bound and
  therefore regressable, not that the base instrument currently passes under /tmp.
- The fork simulation mutates only the scratch clone; the lane checkout was not
  touched (read-only) and no git/jj mutation occurred outside the scratch fork,
  whose toplevel was asserted before committing (host guard).
- F2's "pathological variant" is a seat-local mutation of the control's *fixture
  copy*, not the frozen control file, which is unchanged.
- Round respected as source-only: no package queries, no live reads, no process/
  compositor probes, no screenshots, no host mutation. No installs needed.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify44.md` — this report.
- `.ufo/waves/round-52/w1/Falsify44/receipts/r51-work-tmp.log` — refused-root run (exit 1, hint-only gate).
- `.ufo/waves/round-52/w1/Falsify44/receipts/r51-default-tmpdir.log` — default `/tmp` work location run.
- `.ufo/waves/round-52/w1/Falsify44/receipts/r51-green-baseline.log` — scratch-TMPDIR green baseline (TARGET_MET, matches frozen receipt).
- `.ufo/waves/round-52/w1/Falsify44/receipts/r51-tmp-bypass.log` — fork run with checker scratch gate neutered (selftest 47/50, refuse-work-* fail).
- `.ufo/waves/round-52/w1/Falsify44/receipts/harness-control-eval.py` — self-pointer bypass harness (imports committed counter, fixture-based).
- `.ufo/waves/round-52/w1/Falsify44/receipts/harness-control-eval.log` — its output (F2 evidence).
- Scratch (pre-clean): `/fast/scratch/hyaku/mado-r52/Falsify44/` held `fixture/` (rev 849931ac…), `lane-fork/` (rev 1bbc42af…), harness, logs; `/tmp` leftovers removed. Scratch removed on exit.

Report: .ufo/waves/round-52/w1/Falsify44.md
