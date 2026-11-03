# R66ConnSiblings — sibling-overlap scan (read-only)

Round 66 / w1 / connector. Lane root `mado-shokunin`. Frozen base
`eafd500fa7be76dca59e729435e231a5032cc037`; lane HEAD at scan time
`ed980316e330703030d0c17b2a7098e058295b99` (freeze-only: declaration, spec,
dispatch, ready, registry — 5 files, no instrument changes). `git diff
--name-only eafd500f..ed980316 -- quality/landing-counters.sh
quality/check-tool-ledger.py quality/counters/c3-r56-used-by.py
tools/mado-receipt-citecheck.py quality/check-index.py quality/tool-ledger.md
corpus/README.md` → empty, rc 0, so the mado line numbers below hold at both
revisions. Sibling worktree tips read for binding: kumitate `3c369336`,
tsukuroi `acce353b`, tameshi `f20ba482`.

Read-only. No sibling instrument was executed, no scratch was created
(`/fast/scratch/hyaku/mado-r66/R66ConnSiblings` absent), no git/jj mutation, no
host probe, no credentials/session/env dump, no r56-era material, no
`agent://all`. No production or adoption edits.

## 1. Axes named

- **calibration** — C1 (`PRED-C1-r66`): a register counter must reject three
  r65-accepted controls (duplicate returned-host heading; a row without a
  receipt while other rows resolve; a file-plane CLEAN receipt instead of the
  exact live line) and accept the genuine register. Lock file:
  `quality/counters/c1-r66-register.py` (absent at base/HEAD).
- **operability** — C2 (`PRED-C2-r66`): the landing instrument must distinguish
  genuine red (rc=1 + contract marker), child crash (rc=2), skipped/forced-zero
  child with no marker, and missing used-by sibling; `--round N` selects the
  default receipts tree and dirty guard; child markers bind; scratch and
  inherited `GIT_*` cannot redirect reads. Lock files:
  `quality/landing-counters.sh` (extended) and
  `quality/counters/c2-r66-landing-instrument.py` (absent at base/HEAD).

**Causal separability: mechanically separate, not landing-independent.**
Neither claim's lock file is a code dependency of the other: C1's counter is
not one of C2's four legs, and C2's driver does not invoke C1's counter. But
two shared surfaces couple their measurements (§5.1, §5.6): the tool-ledger
population includes `quality/counters/*.py`, so each new counter changes
`population` for C2's ledger leg; and both claims write receipts under the
round-66 receipts tree that C2's default citecheck leg scans. The predicates
themselves are disjoint sentences, but a landing order that ignores those
surfaces can make C2's real GREEN false because of C1's file.

## 2. Prior art — crashed/never-ran vs red

Bounded scan: `kumitate-shokunin/scripts/`, `tsukuroi-shokunin/tools/`,
`tameshi-shokunin/tools/`. The distinction C2 claims to add is already a
standing convention in all three lanes.

| Lane | Path:lines | Signature | Maps to C2 leg |
|---|---|---|---|
| kumitate | `scripts/bind-oracle.mjs:17-29,108-109,128,171,194` | exit map `0 held · 1 a real defect · 2 fail-closed · 64 usage`; a child with no report or an absent runner is `NO_CHILD reason=... exit=2`, never a scored zero | (b) crash / (c) no marker / (d) missing sibling |
| kumitate | `scripts/round-gate.mjs:63-64,113-128,168-170,195,341-406` | same 0/1/2/64 map; fail-closed tokens `REPORTS_DIR_MISSING`, `NOT_A_GIT_WORKTREE`, `UPSTREAM_MISSING`, `INTERNAL_ERROR`; an absent tree "keeps the unverifiable arm, never a scored zero"; `COMMIT_CITED_UNRESOLVED`/`NOT_ANCESTOR` are errors | (b) crash / (c) skipped / (d) missing input |
| kumitate | `scripts/counter-rerun.mjs:48-52,255-256` | "an evaluation failure must never be recorded as a measured disagreement"; a child exit 2 is propagated as exit 2, "the round-48 rule is that an exit-2 reading is never a score" | (b) crash |
| kumitate | `scripts/inline-dispatch-evidence.mjs:8-10,29-33` | "A dead seat (transcript present, no `yield` or no clean `session_exit`) is named, never credited as done" | (c) skipped/never-ran |
| kumitate | `scripts/make-dispatch-actual.mjs:37-39,594-607` | exit 2 fail-closed for an input "that makes the record untrustworthy"; an unplanned settled seat is `UNPLANNED_SEAT` exit 2, not silently added | (c)/(d) |
| kumitate | `scripts/harm-matrix.mjs:31-35` | `unmeasured=` rows are reported separately; `ALL_UNMEASURED` is fail-closed | (c) never measured |
| tsukuroi | `tools/_revision.py:11-12`; `tools/check-report-receipts.py:8-10` | a revision failure is exactly one finding with "exit class 2 = could-not-evaluate"; an unreadable report or lane revision exits 2, never pass/fail | (b) crash / (d) unreadable input |
| tsukuroi | `tools/check-fd-band-r49.py:26-29` | the fixture work dir is caller-declared and the counter "never writes under /tmp"; exhausted setup is a named failure class, not a silent pass | (c) skipped/setup |
| tameshi | `tools/golden-verdict.py:4-15,27-33,38-41` | three outcomes, not two: diff rc 0 match, 1 differ, **>1 error**; absent golden file is `error`; the write path is flagged | (b) crash |
| tameshi | `tools/arm-liveness.py:17-21,36-41,50-53,67-75,105-107,133-166` | `ARM_LIVE` only when the pinned instrument's exit matches and the tally strictly moves; a declared red arm whose input cannot move it is `ARM_DEAD`; exit 0 all live / 1 any dead / 2 usage or an empty manifest ("an empty manifest proves nothing") | (b)/(c) — a red arm that never fired is dead, not red |
| tameshi | `tools/receipt-exists.py:2-11,23-38` | committed-bytes resolution; exit 0 all resolve / 1 any missing / 2 usage or setup; an `EXTRA` filesystem hit is "a worktree check, not a git-object check" | (a) red vs (c) unlanded |
| tameshi | `tools/registry-check.py:36-45` | every active/superseded row runs; a row holds only when exit equals `expect.exit` and every `stdout_contains` needle appears; every inherited `GIT_*` is removed | (a) red-with-marker binding |

Consequences for C2:

- The vocabulary C2 uses ("crash", "skipped", "missing sibling", "never a
  scored zero") is not new fleet-wide; kumitate's `NO_CHILD` and tameshi's
  `ARM_DEAD` are the closest direct analogues. C2 is a **local repair of the
  mado instrument**, not a fleet-first discrimination.
- The same-round convergence is explicit: tameshi `tools/arm-liveness.py:43-53`
  and `tools/receipt-commit-bind.py:1-30` both describe round-66 changes for
  the "vacuous pass / dead arm" class, and the fleet L0 register already names
  the crash-vs-red indistinguishability as an open ruling
  (`.ufo/l0-questions.md:160`, revenger round-69). C2 lands in a worked
  neighbourhood; it cannot claim novelty from the absence of a hit, and the
  scan does find hits.

## 3. Prior art — receipt binding

| Lane | Path:lines | Mechanism | Maps to C1/C2 |
|---|---|---|---|
| tameshi | `tools/receipt-revision-gate.py:11-32,45-56,102-126,319-323` | binds receipt `rev=` tokens to the certified revision (exactly one for positive/verdict; ancestry for controls); named refusals `RECEIPT_MISSING/EMPTY/NOT_BLOB/REV_ABSENT/REV_AMBIGUOUS/REV_UNRESOLVABLE/REV_MISMATCH/CONTENT_DRIFT/CONTROL_NOT_ANCESTOR/DIGEST_MISMATCH/REQUIRED_LINE_MISSING`, exit 3; `lane_env()` strips every inherited `GIT_*`; `REQUIRE_REGEX` is the "exact required line in this receipt" arm | C1's exact live CLEAN line (stronger prior art: line + revision + ancestry + digest) and C2's marker binding |
| tsukuroi | `tools/check-cited-receipts-r62.py:3-6,18-21,40-45,71-88` | a receipt cited as landed evidence must exist at the committed revision; worktree-only receipts are false on committed bytes; per-path findings, exit 0/1/2; GIT child environment allow-list with `GIT_CEILING_DIRECTORIES` | C1's per-row receipt cell and the file-plane vs committed-plane distinction |
| tsukuroi | `tools/check-report-receipts.py:2-11` | every revision-cited gate in a report must have a committed receipt; exit 0/1/2 | C1's "one row without a receipt while other rows resolve" |
| tsukuroi | `tools/check-scorecard-unique-sections.py:12-19,22-28,62-63` | duplicate level-2 headings are a finding unless a supersession line is declared; `SCORECARD-DUPLICATE-UNMARKED`; exit 0/1/2 | C1's duplicate returned-host heading control |
| tsukuroi | `tools/check-adjacency-table-r51.py:52-53,187-191` | `REDIRECT_ENV` names 16 variables (`GIT_DIR`, `GIT_WORK_TREE`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_INDEX_FILE`, `GIT_REPLACE_REF_BASE`, `GIT_COMMON_DIR`, `GIT_NAMESPACE`, `GIT_CONFIG`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`, `GIT_CONFIG_COUNT`, `GIT_CEILING_DIRECTORIES`, `GIT_EXEC_PATH`, `PYTHONPATH`, `PYTHONSTARTUP`); an override is "never a measurement" | C2's inherited-`GIT_*` requirement |
| tameshi | `tools/receipt-commit-bind.py:1-30` | a commit message that names receipt content must carry those bytes at that commit; round-66 arm 2 makes every message path span a candidate so an absent-at-commit path cannot read `named=0 findings=0` | C1's no-receipt row and C2's no-marker child — the same vacuous-pass class |
| kumitate | `scripts/receipt-attest.mjs:20-21,36,98-104,183-198` | digest-bound semantic fields (argv, exit, nonce, stdout/stderr hashes, wall/mono times); `VALID 0`, `REPLAY/TAMPERED 1`, `UNREADABLE 2`; spawn failures recorded as 127 | receipt binding + crash/never-ran witness |
| kumitate | `scripts/report-receipt-diff.mjs:30-35` | declared limit: "a receipt written by the lane itself is trusted as written — nothing in the tree binds a receipt to a counter run" | the exact gap C2's marker/citecheck binding narrows (and a named bound: syntactic binding is not run binding) |

Consequences:

- C1's third control ("only a file-plane CLEAN receipt rather than the exact
  live receipt") is a narrower instance of a binding already mechanized by
  tameshi `receipt-revision-gate.py` (revision + required line + digest). The
  mado predicate's added value is that the exact live line is required in a
  named committed receipt while a merely CLEAN file-plane twin is rejected;
  this is a local acceptance test, not a new class.
- C2's "marker binds the child" is weaker than tameshi's `registry-check`
  (exit + stdout needles) and than `receipt-attest` (digest-bound fields). The
  declaration's own bound ("bounded structural guarantees, not proof against
  malicious child forgery") is consistent with that prior art.

## 4. Duplicate-claim check

- **C1 vs C2:** distinct. Different lock files (`quality/counters/c1-r66-register.py`
  vs `quality/landing-counters.sh` + `quality/counters/c2-r66-landing-instrument.py`),
  different predicates (register parse/reject vs child outcome classification),
  different axes (calibration vs operability), different observable targets
  (4/4 including genuine register vs 4/4 a–d plus selftest and real landing
  GREEN). No predicate sentence is repeated. They share the new
  `.ufo/waves/round-66/check-controls.py` harness and the scratch root
  `/fast/scratch/hyaku/mado-r66/measure`; that is scaffolding sharing, not
  claim duplication. The harness draft selects by `--claim` (`choices=("c1",
  "c2")`, `R66ExecHarness/check-controls.py:428`) and isolates extraction under
  `<scratch-root>/r66harness/<claim>/` (`:32,450`); integration must preserve
  that, or a harness defect becomes common-mode evidence for both claims.
- **vs r65:** successors, not duplicates. r65 C1 was the surface-state register
  re-derivation on the returned host; r65 C2 was the landing-counters
  capability acquisition. r66 C1 keeps `c1-r65-register.py` frozen and adds a
  discrimination counter; r66 C2 keeps the r65 driver frozen and extends the
  instrument with red/crash/skipped/missing discrimination and `--round N`.
  The baseline instrument's hardcoded round-65 path is the before-state the
  successor exists for (§5.2).
- **Same-round sibling convergence (not a duplicate claim):** tameshi r66
  `arm-liveness` and `receipt-commit-bind` arm 2 target the same
  vacuous-pass/dead-arm class in another lane. Cross-lane adoption is closed
  by the contract and I made no adoption edit; the convergence only forbids a
  novelty claim.

## 5. Second-order effects found (grounded; no edits made)

### 5.1 Ledger-population coupling can make C2's real GREEN false because of C1

`quality/check-tool-ledger.py:10-15` defines the population as files under
`tools/` plus `quality/*.py` plus `quality/counters/*.py` (direct children);
the ledger leg is C2's third leg (`quality/landing-counters.sh:59-61`). Both new
counters land in that population:

- `quality/counters/c1-r66-register.py` (C1's candidate),
- `quality/counters/c2-r66-landing-instrument.py` (C2's driver).

The ledger requires `ledger_rows == population` with a non-empty description
and a pointer whose bytes name the row file (`check-tool-ledger.py:16-44`).
Neither wave draft adds a `quality/tool-ledger.md` row (grep over
`R66ExecRegister/`, `R66ExecDriver/`, `R66ExecLanding/`, `R66ExecHarness/`
returns only a dependency path, not ledger rows). Therefore, at any landing
revision that contains either new counter without its ledger row, the ledger
leg reads `uncovered>=1 verdict=TARGET_MISSED` exit 1, and C2's real four-leg
landing is RED. C1's own landing introduces one of those files, so a C1-first
landing without the row silently changes C2's measured result. This is an
ordering/integration requirement, not a predicate contradiction: the final
landing commit must add both rows before C2's real GREEN is measured.

### 5.2 The baseline instrument is hardcoded to round 65 (confirms C2's predicate)

`quality/landing-counters.sh:62-66` defaults the citecheck paths to
`.ufo/waves/round-65/receipts`; `:218-222` dirty-guards only
`.ufo/waves/round-65/receipts`; `:114,120` build the selftest fixture under
`round-65`. C2's `--round N` requirement is therefore grounded in committed
bytes. The wave draft (`R66ExecLanding/landing-counters.sh:13,15,40,81,100,123,145,156,199,211`)
already carries `--round`, scopes the dirty guard to the selected round and
adds a round-66 dirty/decoy self-test. Two bounded cautions for integration:
the default must come from `--round`, not a constant, and the selftest fixture
must not keep a round-65 literal that makes the default-scope decoy test pass
vacuously.

### 5.3 The shell instrument's inherited-GIT guard is incomplete if run directly

`quality/landing-counters.sh:7-8` unsets six variables (`GIT_DIR`,
`GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_COMMON_DIR`, `GIT_OBJECT_DIRECTORY`,
`GIT_ALTERNATE_OBJECT_DIRECTORIES`). It does not unset `GIT_CONFIG*`,
`GIT_CEILING_DIRECTORIES`, `GIT_NAMESPACE`, `GIT_REPLACE_REF_BASE`,
`GIT_EXEC_PATH`, `PYTHONPATH`, or `PYTHONSTARTUP`; sibling prior art names the
complete set (tsukuroi `check-adjacency-table-r51.py:187-191`; tameshi
`registry-check.py:36-45` removes every inherited `GIT_*`). The C2 driver
draft reports stripping all inherited `GIT_*` before git and leg children
(`R66ExecDriver/report.md`, "Changed draft"), so the requirement may hold at
the driver boundary; the predicate names the standing instrument, so the
instrument must also be safe when invoked directly. I did not execute either
form.

### 5.4 Marker literals are not child-unique as written for used-by

The C2 declaration names "used-by `TARGET_MET`/`TARGET_MISSED`" and "ledger
`MADO_TOOL_LEDGER`". The committed children emit:

- navigation leg (inline in the landing instrument, not `check-index.py`):
  `revision=<rev> indexed=A/B ...` (`quality/landing-counters.sh:42-53`;
  `check-index.py:137` emits a different `MADO_INDEX:` line and is not this
  leg),
- used-by: `MADO_USED_BY: ... verdict=TARGET_MET|TARGET_MISSED ...`
  (`quality/counters/c3-r56-used-by.py:13,300`),
- ledger: `LEDGER: population=... verdict=TARGET_MET|TARGET_MISSED rev=...`
  (`quality/check-tool-ledger.py:38-44,368-371`) — the declaration's
  `MADO_TOOL_LEDGER` literal is already corrected by
  `.ufo/waves/round-66/marker-premise-erratum.md:1-4`,
- citecheck: `MADO_CITECHECK: rev=... verdict=TARGET_MET|TARGET_MISSED`
  (`tools/mado-receipt-citecheck.py:23-24,136`).

A bare `TARGET_MET` appears in three children, so a structural acceptance that
looks for only that substring does not bind it to used-by. The landing draft
already prefixes by leg (`R66ExecLanding/landing-counters.sh:47`:
`MADO_USED_BY:`, `LEDGER:`, `MADO_CITECHECK:`, and `revision=` for nav), which
removes the cross-child substitution. The residual risk is integration
reverting to the declaration's field-name-only form; full prefixes plus rc (as
tameshi `registry-check.py:36-45` does with `stdout_contains`) cost no
predicate change.

### 5.5 Both claims share one scratch root (draft already isolates per claim)

The declared count command uses `--scratch-root
/fast/scratch/hyaku/mado-r66/measure` for both `--claim c1` and `--claim c2`.
The harness draft already scopes extraction and fixtures under
`<scratch-root>/r66harness/<claim>/` (`R66ExecHarness/check-controls.py:32,450`),
refuses symlink roots (`:443`) and `/tmp`, `/var/tmp`, `/dev/shm` (`:445-447`).
The residual integration risk is only that the frozen count command passes the
same root for both claims; if the per-claim subdirectory is preserved, the
claims cannot read each other's trees. This is an operability check, not a
claim change.

### 5.6 The round-66 receipts tree is a shared measurement surface

C2's default citecheck leg scans `.ufo/waves/round-66/receipts` once
`--round 66` is selected. C1's controls and before/after receipts also land
there. A citecheck run before all cited receipts are committed (or after a C1
receipt cites an unlanded path) turns C2's GREEN red for reasons outside C2's
four conditions. The declaration gives the lever: `--citecheck-paths` is
caller-supplied, and the driver draft passes the real round-66 receipts path
explicitly. The integration requirement is to measure C2's real landing at a
revision where the cited receipts are committed, or scope the leg to C2's own
receipt subtree.

## 6. merge/mado package and latest considerthese — Assimilation: none

Inspected read-only: `/home/vgpnk/Projects/shokuknow/merge/mado/` and
`considerthese/2026-10-28.md` (latest; no 2026-10-29+ file exists).

**Package:** `MERGE-REPORT.md`, `MERGE-REPORT.json`, `SOURCES.append.md`,
`amendments/` (4 files), `knowledge/` (65 files; 69 proposed entries per
report). Theme is desktop/IPC knowledge: Hyprland socket contract, dispatchers,
Waybar producers, gkeep geometry, two-literature coverage (examples
`MERGE-REPORT.md:32-38,50,75,78`; `SOURCES.append.md:30,34,46-47,50,55-57`).
Only one title contains "instruments" (`MERGE-REPORT.md:78`,
`japanese-input-observation-methods-r14.md`) and it is input-observation
methods, not counter/receipt instrumentation. No entry title or staged
source row supports calibration or operability instrument discrimination
(searched `MERGE-REPORT.md` and `SOURCES.append.md` for counter, instrument,
receipt, exit, calibration, verdict, gate, measurement; only the title above
matched "instruments").

**Adoption mechanics are stale:** the package was built when the lane registry
held 192 rows with first staged id `S203` (`MERGE-REPORT.md:9`). At this scan
the lane holds 371 rows through `S434`; the staged range is `S203-S349`.
Measured intersection: **94 of 147 staged ids collide** with current lane ids
(53 staged ids are free but interleaved). The package also has no
`ID-REMAP.md` on disk now, although the L0 register records its remap as stale
and URL-duplicating (`.ufo/l0-questions.md:149`). Adoption would require
scratch renumbering plus per-entry re-grounding (CORPUS rule 1/2/4), and it
would still be off-axis. `Assimilation: none` on theme, not on reachability.

**considerthese 2026-10-28:** six proposals at lines 52-57 — missing-day
placeholder, privacy recheck, lane-state streak, live-tool table,
relayed-vs-re-measured labelling, adoption flagging. Proposal 5 is the only
one adjacent to this round's evidence honesty (it asks numbers to be marked
"relayed" or "re-measured"), but it is a report-prose convention, not a
source-grounded knowledge entry, and adopting it would impose a writing rule
outside the two frozen claims. Proposal 3/4 are lane bookkeeping, 1/2/6 are
process hygiene. None carries a source row or a knowledge entry that could
enter the corpus under the assimilation contract, and the declaration forbids
an additional claim.

**Sibling-lane considerthese screen (latest per lane, read-only):** the
nearest-fit themes exist outside mado, and none is a source-grounded entry:

- tameshi `considerthese/2026-10-28.md:73-75` proposes a receipt-existence
  linter and `:77-78` a counter-arm liveness check. Both are already landed in
  tameshi as tools: `tools/receipt-exists.py:4-5` says it is the cited-receipt
  half of that proposal 1 (landed round 64), and
  `tools/arm-liveness.py:3-6,43-53` says it adopts proposal 2 in round 66.
- kumitate `considerthese/2026-10-26.md:64-65` ("every number has a
  transcript"), `:69-70` ("new tools get registered"), and `:76-77` ("plot
  noisy counters") are the closest process themes to C2's marker receipts and
  to the ledger coupling in §5.1.
- tsukuroi `considerthese/2026-10-26.md:9` records the counter-as-attack-surface
  lesson ("a PASS is only as strong as the counter's resistance to being
  gamed"), which is the C1/C2 calibration theme.

These are reflections and process proposals, not corpus entries with source
rows; two are already implemented in the proposing lane, and the third is what
mado's own ledger/receipt gates already mechanize. Adopting one would either
duplicate the round's own C1/C2 mechanism or add an ungrounded prose theme,
both outside the assimilation interface (`merge/mado/` entries + rows).

**Assimilation: none** across mado 2026-10-28 and the sibling latest screens;
grounded in theme mismatch for the packaged entries, the absence of a
source-grounded entry in every nearest-fit proposal, and the stale staged id
space as an independent adoption blocker.

## 7. Bounded move (recommendation only; not a claim, no edits)

**Move:** make C2's real GREEN unreachable-by-accident: bind each leg witness
to its full verdict-line prefix and add both r66 counters
(`quality/counters/c1-r66-register.py`,
`quality/counters/c2-r66-landing-instrument.py`) to `quality/tool-ledger.md`
in the same landing revision at which C2's four-leg landing is measured.

- **Why it improves an axis without harming another:** it removes the
  ledger-population coupling (§5.1) that can turn C2's operability GREEN red
  when C1 lands, and it closes the cross-child `TARGET_MET` substitution
  (§5.4). C1's predicate and lock file are untouched; calibration is unharmed.
- **Risks:** the ledger gate is structural (non-empty description + a
  self-naming pointer), so the rows do not prove accountability; they only
  prevent a false RED. If L1 instead measures C2 at a revision before C1
  lands, the coupling disappears but C2 would no longer be measured on the
  final tree — that trade should be explicit, not incidental.
- **Verification (for the main agent, not run here):** at the chosen landing
  rev run `python3 -I quality/check-tool-ledger.py --repo . --rev <rev>`
  (expect `LEDGER: ... uncovered=0 ... verdict=TARGET_MET` rc 0), then
  `bash quality/landing-counters.sh --repo . --rev <rev> --round 66
  --scratch-root /fast/scratch/hyaku/mado-r66/measure/w1/conn` (expect
  `MADO_LANDING_COUNTERS: GREEN` rc 0), and confirm each leg's marker is the
  full `revision=`/`MADO_USED_BY:`/`LEDGER:`/`MADO_CITECHECK:` prefix.

## 8. Commands and rc (read-only evidence)

| Command | rc | Result |
|---|---|---|
| `git -C mado-shokunin rev-parse HEAD` | 0 | `ed980316...` |
| `git -C mado-shokunin cat-file -t eafd500f...` | 0 | `commit` |
| `git -C mado-shokunin diff --name-only eafd500f..HEAD -- <7 cited files>` | 0 | empty (no drift on cited mado instruments) |
| `git -C kumitate/tsukuroi/tameshi rev-parse HEAD` | 0 | `3c369336`, `acce353b`, `f20ba482` |
| `ls quality/counters/c1-r66-register.py quality/counters/c2-r66-landing-instrument.py .ufo/waves/round-66/check-controls.py` | 2 (ENOENT) | all three absent at HEAD (candidate-only files) |
| python id-collision computation over `corpus/SOURCES.md` and `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md` | 0 | lane 371 rows S001-S434; staged 147 S203-S349; intersection 94; staged-not-in-lane 53 |
| `grep`/`read` scans over the three sibling `scripts/`/`tools/` trees, mado `quality/`, `.ufo/waves/round-66/`, `considerthese/2026-10-28.md`, `merge/mado/`, `.ufo/l0-questions.md` | n/a (tool results) | the paths/lines cited above |
| `ls /fast/scratch/hyaku/mado-r66/R66ConnSiblings` | 2 | absent; no scratch created |

## 9. Limitations

- Bounded k: only the three sibling lanes' `scripts/` and `tools/` trees, the
  named mado instruments/drafts, the merge package, the latest considerthese,
  and the relevant L0 line. Sibling report prose and full `.ufo` trees were not
  swept; a wider scan could find more prior art.
- The prior-art claims are from committed source/docstrings, not observed
  executions. I read one committed tameshi demonstration receipt
  (`tameshi-shokunin/.ufo/evidence/round-66/win-host/live-demo-dead.txt:1`,
  `ARM_DEAD bind-candidates-red tally=findings=0`) but did not replay it.
- Sibling worktrees were read at their current tips; I did not inspect their
  uncommitted state, so a line number in a dirty worktree could move. The
  mado citations are pinned at base/HEAD equality.
- No-hit is not novelty: this scan found hits, and the report claims no
  novelty anywhere. C1/C2 are local instrument repairs; their value is in the
  frozen predicates, not in fleet-first status.
- I did not run any selftest, counter, landing leg, or whole-repo gate; the
  seat is read-only. The C2 real-GREEN question remains the parent's to
  measure.
- The merge package is outside the lane; it was read only and not adopted.

## 10. Changed drafts

None. No production file, seat draft, ledger row, or adoption edit was
created. The only file written is this report.

Report: `.ufo/waves/round-66/w1/R66ConnSiblings.md` (paths relative to
`/home/vgpnk/Projects/shokunin/mado-shokunin`).
