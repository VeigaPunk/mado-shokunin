# AssimilationScan — mado round 52 (W1)

Scope: read-only assimilation of the latest `considerthese` proposal 2 against frozen
claim C1; merge/mado presence check; absent-register path inspection. No claim or
predicate edits; no tracked lane writes.

## Axes named

- coverage: does C1 close proposal 2's tracking-table gap, wholly or partially?
- operability: is the evidence C1 demands actually producible/absent as registered?
- operability (merge hygiene): is any merge state present that could perturb the
  frozen base `85d57a818c3707397e21c840b6498b105ba798aa`?

## Source evidence (read-only)

- `considerthese/2026-10-26.md` (latest reflection; 2026-10-23 → 2026-10-26 window,
  75 commits, tip `6a1a905`). Its "Self-improvement suggestions" list numbers six
  proposals; **proposal 2** (line ~48): "Keep a running ledger of live-state tools.
  Four tools now read the running desktop. A small table (tool, question it answers,
  last live run, verdict) in each reflection would let João see at a glance which
  ones he could run himself, and whether any has gone stale."
- The four live-state tools named by the reflection: `tools/mado-eventq.py`,
  `tools/mado-options.py` (+ `--live`), `tools/mado-globals.py`,
  `tools/mado-geometry.py` (considerthese/2026-10-26.md, "Top 3 lessons / gains" #1).
- `quality/tool-ledger.md` (119 lines): rows for all four live tools exist with
  functional descriptions and accountability pointers — e.g.
  `tools/mado-eventq.py` → `SCORECARD.md:2370`, `tools/mado-globals.py` →
  `PROVINCE.md:31`, `tools/mado-geometry.py` → `PROVINCE.md:32`,
  `tools/mado-options.py` → `SCORECARD.md:2436`.
- `.ufo/waves/round-52/claims-frozen.md` and `.ufo/waves/round-52/registration.md`:
  C1 target is a *new committed counter* distinguishing the production ledger from
  `controls/c1-do-nothing.md` via unique population, non-self resolvable evidence
  targets, and instrument-specific context checks; "New counter absent" at base;
  selftest must include explicit red/green receipts.
- `quality/counters/c1-r51-ledger.py` (+ `quality/check-tool-ledger.py`,
  SELFTEST_CHECKS = 50): the existing counter/checker enforce row grammar,
  pointer resolution, basename-in-bytes — i.e. exactly the weakness the freeze
  names (any referenced file containing the instrument basename passes).
- `.ufo/waves/round-52/controls/c1-do-nothing.md` (4 lines): 2 rows, both
  `tools/mado-verify.sh`, both pointing at `quality/tool-ledger.md` with the
  generic description "generic accountability pointer to this ledger itself".
- `.ufo/waves/round-52/receipts/c1-base.txt`: existing counter at base reports
  `population=82 ledger_rows=82 ... verdict=TARGET_MET` (does not measure context).

## Findings

### 1. Does C1 cover considerthese proposal 2? — Partially; mostly no.

Overlap (what C1 *does* supply toward proposal 2):

- C1's enforced ledger already contains one accountable row per live-state tool,
  with a description read from the tool's own header (ledger preamble: "cell 2 is
  what the instrument does, read from its own header, never inferred from its
  name"). That is the "tool + question it answers" column of proposal 2's table,
  at higher integrity than the proposal's ask, because the new counter adds
  uniqueness + non-self pointer + instrument-specific context checks. The four
  live tools are in the 82-row population (`grep` hits shown above), so a C1 pass
  at base *is* evidence that the running-ledger population is real and non-vacuous.

Not covered (what remains absent even if C1 lands TARGET_MET):

- **No "last live run" evidence.** C1 checks static ledger bytes at a pinned
  revision; nothing records when each live tool last ran against the host, nor
  that the run was reproduced by a non-author. The reflection explicitly
  complains this is relayed, not owned (proposal 4: "All live runs I report are
  relayed from closures"). A C1 pass leaves this gap exactly as wide.
- **No "verdict" column / staleness signal.** C1 measures ledger row well-formedness,
  not whether each tool's most recent verdict still holds. Proposal 2's "whether
  any has gone stale" is unmeasured by C1.
- **No per-reflection update requirement.** C1 is a round-scoped counter; it does
  not create the recurring table in each `considerthese` file.
- Proposal 2 is also only a "proposals only; not acted on" item in the reflection —
  it has no frozen registration, so C1 was never obligated to cover it.

Net: C1 is a *prerequisite integrity layer* for proposal 2 (it makes the tool
ledger trustworthy enough to serve as the table's data source) but covers at
most the population/description half of the proposal. The operability half
(last live run, verdict freshness, per-reflection cadence) has no evidence path
in round 52 and would need a separate frozen claim (e.g. a live-run ledger
counter with recency fields) to be scored.

### 2. Evidence absent for C1 at base (what workers still owe)

- The new counter itself: `quality/counters/` at base contains `c1-r51-ledger.py`
  and per-round counters through `c1-r51`; no r52 ledger-accountability counter
  exists. Confirmed consistent with registration ("New counter absent").
- Red/green selftest receipts demonstrating production pass at
  `85d57a81` *and* control fail on `controls/c1-do-nothing.md` specifically for
  the self-pointer/context defects. `receipts/c1-base.txt` covers only the old
  counter (82/82, context-blind).
- Demonstration that the old weakness is actually closed: a fixture where a row
  points at a *resolvable, non-self* file that merely contains the basename but
  whose description is generic — the r51 counter passes this today; the new
  counter must be shown to fail it (context check), not only the shipped
  do-nothing control.

### 3. Merge / mado presence (read-only)

- No `merge/` directory exists in the lane repo or fleet root (`find -maxdepth 3
  -iname '*merge*'` returns only `.git/hooks/pre-merge-commit.sample`).
- No in-progress merge: `.git/MERGE_HEAD`, `MERGE_MSG`, `REBASE_HEAD`,
  `CHERRY_PICK_HEAD` all absent. A stale `.git/AUTO_MERGE` file exists
  containing tree `d997261c911ccc752a08e4510c245fd2be0666fc` (unreachable tree
  object; an `ort` merge leftover, not an active operation). No action needed;
  noted as hygiene only.
- Repo state: `HEAD = 85d57a81` (the frozen base), working tree clean except
  untracked `.ufo/waves/round-52/` (this round's own files). Nothing observed
  perturbs the frozen revision.

### 4. Absent-register path

- No dedicated absent-register file/path exists in the lane (searched `.ufo/**`
  for `*absent*`, grepped `quality/` and `corpus/` for `absent-register` /
  `absent_register`: no hits).
- Absence checks are claim-local and inline in `registration.md`: for C2 the
  *new counter itself* must "name a separate target slug and prove absent at
  base" (`receipts/c2-base.txt` is untrusted for C2 because the r51 dispatcher
  entry already exists — confirmed by that receipt showing
  `index_row=knowledge/hyprland-dispatcher-dispatch-r51.md ... TARGET_MET`).
  For C1, absence of the new counter is asserted in the registration text, not
  registered in any machine-readable structure. If the lane wants an
  absent-register as standing infrastructure, that would be a proposal-level
  change, out of scope for this round.

## Commands run (all read-only; lane repo source reads only)

- `ls`/`find` over `.ufo/waves/round-52/`, lane root, `.git/` merge-state files
- `read considerthese/2026-10-26.md` (full; line 30 re-read raw for the
  truncated freeze-discipline sentence)
- `git log --oneline -3`, `git status --short`, `git rev-parse HEAD`,
  `git cat-file -t d997261c...`
- `cat` of `.ufo/waves/round-52/controls/c1-do-nothing.md`,
  `receipts/c1-base.txt`, `receipts/c2-base.txt`
- `grep` of `quality/tool-ledger.md` for the four live-state tool rows;
  `grep` of `quality/check-tool-ledger.py` for selftest structure
- `df -h /fast` (26% used; no ENOSPC risk); scratch
  `/fast/scratch/hyaku/mado-r52/AssimilationScan/` created, never used for
  evidence, removed on exit.

## Limitations

- Reflection content (live-run reproduction counts, relay provenance) is taken
  as authored prose; this seat ran no tools against any host state per the
  source-only safety boundary.
- I did not execute the r51 counter or the checker; the 82/82 TARGET_MET figure
  is from the committed receipt `receipts/c1-base.txt`, not re-measured.
- Judgment of whether a C1-context check would accept/reject each live-tool row's
  description is deferred to the C1 workers' counter and the non-author closure;
  this seat makes no TARGET_MET prediction.
- No installs this seat; tooling authorization (`/home/vgpnk/.omp/agent/RULES.md`)
  not exercised.

## Deliverables

- `.ufo/waves/round-52/w1/AssimilationScan.md` (this report)

Report: .ufo/waves/round-52/w1/AssimilationScan.md
