# Attack21 — W2 attack #21: C1 TMPDIR and workdir boundary

Seat: Attack21 (mutation-tester, leaf). Date: 2026-10-27. Fleet root: `/home/vgpnk/Projects/shokunin`.
Base/frozen revision: `85d57a818c3707397e21c840b6498b105ba798aa` (verified `git rev-parse HEAD` at seat start; unchanged — still HEAD at report time).
Target artifact: `quality/counters/c1-r52-ledger.py` — **untracked** in the lane tree (`git status --porcelain` → `?? quality/counters/c1-r52-ledger.py`, 78 lines), sha256 `923faf02cd0c2db374f7757d38ef24fc8381c2882cb3d853882f0fadce1c17d7`. No committed C1-r52 counter exists at HEAD (`git show HEAD:quality/counters/c1-r52-ledger.py` → `fatal: … not in 'HEAD'`; `git log -- quality/counters/c1-r52-ledger.py` → empty). All findings below are about this working-tree candidate — the only r52 C1 counter present anywhere in the tree.

Scratch: `/fast/scratch/hyaku/mado-r52/Attack21/` — removed at end of seat (see Scratch). Disk guard at start: `/fast` 28% used, 581G free; no ENOSPC.

## Attacked clauses

- **A1 (claims-frozen.md, C1):** "a new committed counter distinguishes the production ledger from a no-work control … Demonstrate production pass and control fail at the frozen revision."
- **A2 (registration.md, C1):** "must pass on the existing production ledger at the base revision and fail on `controls/c1-do-nothing.md` specifically for self-pointer/context defects."
- **A3 (registration.md, C1):** "Selftest includes explicit red/green receipts."
- **A4 (registration.md, C1 + wave dispatch safety rule):** workdir boundary — "runs at a requested pinned revision" with scratch discipline "explicit TMPDIR/--work; never /tmp"; the W1-specified control is the draft's `resolve_work`/`REFUSED_WORK_PREFIXES` behavior (refuse `/tmp`, `/var/tmp`, `/dev/shm` via realpath before any creation; require `--work` or a non-refused `TMPDIR`).

## W1 evidence read before judging

`claims-frozen.md`, `registration.md`, `w1/C1CounterDesign.md` (+ `receipts/receipts.txt`), `w1/C1Simplify.md`, `w1/C1Mutation.md`, `w1/Falsify20` and `Falsify25` entries in `w1-results.json`. W1 receipts for the boundary (refusal of `--work /tmp/refused` exit 2; `--work`-or-TMPDIR-required exit 2; selftest `53/53 passed`; green `82/82 TARGET_MET`; red control `ledger_rows=2 … self_pointer=1 generic_desc=1`) were all generated from the 847-line W1 draft at `.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py` (`REFUSED_WORK_PREFIXES` at :76, `rows_of` unfenced+path guard at :185–202, `tempfile.mkdtemp(dir=work)` at :645, `shutil.rmtree` at :764, `resolve_work` at :768). None was generated from the candidate now sitting at the integration path.

## Method

Bounded detector `receipts/detector.sh` (copy retained in seat dir). Every probe runs under `bwrap --ro-bind / / --tmpfs /tmp --tmpfs /var/tmp --tmpfs /dev/shm --bind <scratch> <scratch>`: fleet root read-only, system temp roots private tmpfs, so **no probe can write the host in any outcome branch** (pristine, mutant, restored). Probes: G (production green at pinned rev), R (frozen do-nothing control), B1 (`--work /tmp/...`), B2 (no `--work`, `TMPDIR` unset), B3 (`TMPDIR=/tmp/...`), B4 (valid scratch `TMPDIR`, residue check), S1/S2 (selftest reachability), P (pin boundary: committed green fixture repo in scratch, dirty worktree row appended uncommitted, same `--rev`), F3 (counterfeit-context control from C1Simplify, secondary). Run on pristine, on two single-point mutants, and on restored bytes; residue and host-leak checks after every run.

## Findings

### F1 — Workdir boundary absent in the candidate (A4) — **REPRODUCED**

Locator: the string `work` occurs in the candidate **only** at `quality/counters/c1-r52-ledger.py:68` (argparse declaration `a.add_argument('--work')`); `x.work`, `TMPDIR`, `tempfile`, `mkdtemp`, `realpath`, and any refusal list occur nowhere (grep receipts). `--selftest` likewise appears only at :68.

Reproduction (inside bwrap, private `/tmp`):
- `python3 -I <candidate> --repo <lane> --rev 85d57a8… --work /tmp/c1r52-attack21-refused` → exit **1**, full measurement executed (`C1_R52: population=82 ledger_rows=83 … verdict=TARGET_MISSED`); no refusal, `/tmp` work path accepted and then ignored. (W1-specified: exit 2 `refusing work dir under /tmp`, receipt `C1CounterDesign/receipts/receipts.txt`.)
- no `--work`, `TMPDIR` unset → exit **1**, measurement executed. (W1-specified: exit 2 `--work <dir> or a TMPDIR outside /tmp, /var/tmp, /dev/shm is required`.)
- `TMPDIR=/tmp/c1r52-attack21-tmp`, no `--work` → exit **1**, measurement executed. (W1-specified: exit 2.)

Mitigation measured, not assumed: the candidate performs **zero filesystem writes** (only read-only `git ls-tree/show/rev-parse` subprocesses and stdout; residue checks: 0 entries in every passed `--work`/`TMPDIR` dir; host `/tmp` leak check: absent). So the missing boundary is currently harmless in effect — but the specified control does not exist in the artifact, and `--work`/`--selftest` are accepted-and-ignored interface lies. Verdict against the W1-specified boundary control: **not carried into the candidate; control missing** (mutant-verified below).

### F2 — Frozen green case fails on the candidate (A1, A2) — **REPRODUCED**

Locator: committed base blob `85d57a8…:quality/tool-ledger.md` lines 11–13 (blob sha256 `df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b`; extract at `receipts/ledger-at-base-extract.md`): a fenced block (``` at lines 11 and 13) containing the template row `` | `<repo-relative path>` | <one-line description> | `<pointer path>` or `<pointer path>:<line>` | ``.

Reproduction: `python3 -I <candidate> --repo <lane> --rev 85d57a8…` (default ledger = pinned blob) →
`C1_R52: population=82 ledger_rows=83 uncovered=0 dup=0 dangling=1 bad_pointer=1 self_pointer=0 generic_desc=0 verdict=TARGET_MISSED` exit 1.

Cause: candidate `parse_ledger` (:60–66) has no fence handling and no path-shape guard — it admits the fenced template row (`dangling=1`, and `bad_pointer=1` because basename `<repo-relative path>` is not in the pointer). The W1 draft excludes it two ways (`rows_of` :190–197: `unfenced(text)` + "non-path first cell" skip), hence W1 receipts `ledger_rows=82 … TARGET_MET` at the same rev. The candidate therefore **does not pass the production ledger at the frozen revision** — A1/A2's green half fails on the integration-path artifact.

### F3 — Frozen red case fires, but vacuously (A1, A2) — **REPRODUCED (degenerate)**

Reproduction: same command with `--ledger .ufo/waves/round-52/controls/c1-do-nothing.md` →
`C1_R52: population=82 ledger_rows=0 uncovered=82 … verdict=TARGET_MISSED` exit 1.

The control's rows are wider than three cells; the candidate's strict `len(c)==3` grammar parses **zero** rows, so the red verdict comes from an empty ledger, not from the claimed `self_pointer`/`generic_desc` signals (W1 draft on the same control: `ledger_rows=2 … self_pointer=1 generic_desc=1`). Combined with F2: the candidate scores **MISSED for both production and control** — it does not distinguish them, so A1's distinguishing requirement fails outright on this artifact.

### F4 — Selftest absent from the candidate (A3) — **REPRODUCED**

Reproduction: `--selftest --repo <lane> --rev 85d57a8… --work <scratch>` → exit 1, output is the ordinary measurement line (`C1_R52: population=82 ledger_rows=83 …`); no `C1_R52_SELFTEST` line exists in the candidate (grep: no `SELFTEST` outside :68). `--selftest --work <scratch>` alone → argparse exit 2 (`--repo` required). Registration A3's "Selftest includes explicit red/green receipts" is **not reproducible from the candidate**; the 53/53 receipt belongs to the W1 draft only.

### F5 — Pin boundary holds (A4, "runs at a requested pinned revision") — **NOT REPRODUCED (control verified)**

Fixture (scratch throwaway repo, rev `2c4c99f7…`, 2 instruments + green committed ledger): append a parseable self-pointer row to the **working tree** without committing, run `--repo <fixture> --rev 2c4c99f7…` → exit **0** `population=2 ledger_rows=2 … verdict=TARGET_MET`. The dirty worktree is ignored; the default ledger read is `blob(repo, rev, LEDGER)` at :73. Pinned-revision predicate verified on the candidate.

### F6 — Secondary: counterfeit-context control passes the candidate (adjacent to the F3 W1 signal)

`--ledger w1/C1Simplify/control-F3-forged.md` → exit **0** `generic_desc=0 verdict=TARGET_MET`. The candidate's generic check (:65) is bare bigram overlap with the instrument bytes — the pre-filter draft semantics that W1 already holed. On this artifact the forged-context control is not rejected. (Main ownership: the context-clause seats; recorded here because it changes what "control fail" means for the same artifact.)

## Mutation table (same detector on pristine / mutated / restored)

Detector output summaries in `receipts/*-v3.txt.summary`; full transcripts in `receipts/*-v3.txt`.

| variant | sha256 (prefix) | G green | R red | B1 | B2 | B3 | S1 | P pin | F3 | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| pristine (tree bytes) | `923faf02` | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | boundary+green+selftest defects present |
| mut_restore — insert draft's `resolve_work` gate (refuse `/tmp`,`/var/tmp`,`/dev/shm` via realpath; require `--work`/TMPDIR) after `parse_args()` | `3744a435` | 1 | 1 | **2** | **2** | **2** | 1 | 0 | 0 | **killed** — B1/B2/B3 flip to the specified refusals, proving the probes measure exactly the missing control |
| mut_worktree — replace default ledger read `blob(repo,rev,LEDGER)` with `open(os.path.join(repo,LEDGER))` | `6e581c24` | 1 | 1 | 1 | 1 | 1 | 1 | **1** (`TARGET_MISSED`, `self_pointer=1 dup=1` from the uncommitted row) | 0 | **killed** — pin probe discriminates; F5's control is real |
| restored — re-copy of tree bytes | `923faf02` | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | identical to pristine |

Restoration evidence: `sha256sum bytes/pristine.py bytes/restored.py quality/counters/c1-r52-ledger.py` → all three `923faf02cd0c2db374f7757d38ef24fc8381c2882cb3d853882f0fadce1c17d7` (receipts/variant-hashes.txt). No lane byte was modified at any point; mutants lived only in scratch.

## Limitations

1. The claim binds a **committed** counter; none exists at HEAD. F1–F4, F6 are verdicts on the untracked working-tree candidate; if a different/superset artifact is committed before integration, these verdicts must be re-run against those bytes (detector is retained and self-contained).
2. R-red (F3) still exits 1, so a driver checking only exit codes would score the red case green; the vacuity is visible only in the parsed-field breakdown.
3. The wave is live: `git status` showed ` M quality/tool-ledger.md` during the seat (sibling integration edits to the worktree). All evidence reads are pinned-blob (`git show 85d57a8…`) or scratch-only; the re-hash at report time confirms the tested candidate bytes are unchanged.
4. The boundary probes cannot distinguish "refusal missing" from "refusal present but ignoring `--work`" by exit code alone — that gap is closed by the grep locator (F1) and the mut_restore kill.
5. No draft selftest re-run: the 53/53 receipt is cited from W1, not re-executed (out of my boundary scope; the candidate has no selftest to compare).

## Deliverables

- `.ufo/waves/round-52/w2/Attack21.md` — this report.
- `.ufo/waves/round-52/w2/Attack21/receipts/detector.sh` — exact bounded detector (bwrap-sandboxed).
- `.ufo/waves/round-52/w2/Attack21/receipts/{pristine,mut_restore,mut_worktree,restored}-v3.txt` (+ `.summary`) — per-variant transcripts.
- `.ufo/waves/round-52/w2/Attack21/receipts/variant-hashes.txt` — before/after byte hashes.
- `.ufo/waves/round-52/w2/Attack21/receipts/ledger-at-base-extract.md` — pinned blob extract showing the fenced template row.

## Scratch

`/fast/scratch/hyaku/mado-r52/Attack21/` — removed after receipts were copied into the seat dir; removal verified. No tracked tree edits, no git/jj mutation, no installs, no pacman, no live/process/compositor probes, no host mutation (all probes bwrap-confined; host `/tmp` leak checks negative).

Report: `.ufo/waves/round-52/w2/Attack21.md`
