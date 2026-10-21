# ConnIndependence — C1/C2 causal separability (round 22, w1, connector)

Author-lane advice only. It is not admission or closure. No measurements, scanner runs or production edits were made. Machine-readable note: `.ufo/waves/round-22/w1/notes/ConnIndependence.json`.

## Outcome

Source inspection identifies one high-severity conditional coupling route and four medium verification gaps. These do **not** demonstrate actual C1/C2 dependence; no intervention was executed. The historical representation contradictions below are separate from runtime independence.

The high-severity route is the historical-C3 target. It cannot be met from the r19 receipt alone, so whoever builds it has to supply evidence labels, command strings and file counters from somewhere. If they come from re-scanning with the current or candidate tripwire, C2's red/green outcome becomes a function of C1's bytes. The r21-style swap of classifier bytes cannot detect this, because by then the fixture already carries C1's output.

A no-run, C1-invariant construction exists. Committed pre-base blobs already contain everything needed, so I propose that construction plus a stronger runtime intervention. Neither changes any tool.

Main subsequently clarified that the raw original C3 stays code 2, projections are explicitly derived from old committed blobs only, and no candidate classifier supplies historical fields. This addresses R1 by construction, subject to provenance review; it grants no retroactive admission. Main separately authorized authoring `audit/independence.py` for future bounded interventions, without executing it.

## Evidence (observed)

| Fact | Source (sha256 or blob) |
|---|---|
| The r19 C3 receipt has only `{file,line,detected}` rows: detected 6, score 10.0, tool `367be947…` | `round-19/evidence/final/tw-recall-after.txt` `8ff13d23…`, blob `4e436b40` |
| The actual r19 raw scan (same tool, 7b4839d) has 11 findings with class, rule and command, and 5 files with every counter 0. **No finding has an `evidence` key.** | `round-19/evidence/final/tripwire-frozen-scan-classes.txt` `64648cca…`, blob `10f5a706`; JSON line 3 `97c6fc99…` (with newline) |
| The r19 tool gives 11 unmarked findings | `round-20/evidence/recall-split-1f7f995.txt` `7928e3fa…` |
| The 5 observed + 1 lead **line** split, which is 10 + 1 **rows**, first appears with the r20 tool `9613f510…` and again with `a57d4fe9…` (the r21 C1base). The only lead is `r13-root.jsonl:4 pacman:-Q`. | `recall-split-final.txt` `5165b728…`; `a2/…recall-split-a8960de….txt` `016975df…`, blob `34bb3ee3` |
| The current C1 base is tripwire `46c82902…` (a6cef89 = 741122d = HEAD). No committed split exists for it. | `git show REV:tools/mado-tripwire.py \| sha256sum` |
| Source grounding for that lead: the query runs through local helper `run_record`, whose `def` (line 437) is outside the pinned snapshot pairs | `round-18/frozen/expected.json` `4f3534ae…` known_misses; `round-19/w1/reports/CriticC3.md` §2 |
| The r21 intervention stages only gate, classifier and fixtures; runs only `--selftest`; compares stdout only | `round-21/assessment-independence.py` `4e289793…` |
| Both pre-base receipt commits (d642ce5 and 94b6925) are ancestors of 741122d | `git merge-base --is-ancestor` |

## Contradictions (stated, not smoothed)

- **K1, the faithful receipt is unmarked.**
  - Under the contract, a missing marker is invalid, so a faithful r19 snapshot can only give code `2`.
  - The registration asks for red on the faithful receipt "without changing rows" and also green "scoped to five observed plus one lead". Neither is reachable unless evidence keys are added to all 11 rows.
- **K2, the units differ.**
  - "observed5/6 plus lead1/6" counts incident **lines**; the contract counts finding **rows**. The faithful population is 11 rows: 10 observed and 1 lead.
  - The SCORECARD-literal claim `{6,5,1,0,false}` on that snapshot is **red** (`finding_count_mismatch`, `observed_count_mismatch`).
  - The green claim in contract units is `{11,10,1,0,false}`. Collapsing to six rows would delete five real findings.
- **K3, r19 never claimed "observed".** It claimed *detected* 6/6 (any class, any evidence). The "observed 6/6" assertion is a translation; in row units it is `{11,11,0,0,false}`.
- **K4, the lead label comes from a classifier.**
  - It comes from the same detector lineage that C1 modifies. Whether base `46c82902` or the candidate still labels that row lead is unknown (not measured, by contract).
  - Source authority supports the label independently of any classifier (see the evidence table).

## Coupling routes

| ID | Route | Severity |
|---|---|---|
| R1 | Data generation: historical fields filled by a HEAD or candidate re-scan make C2's outcome depend on C1's bytes. A post-freeze swap cannot see this. | high |
| R2 | Staged-tree blindness: any lane path not staged (`round-22/oracle/`, other `tools/`, git) is absent in every state, so equality holds vacuously | medium |
| R3 | Clause mismatch: output equality does not test "never imports/runs/reads C1" | medium |
| R4 | No positive control: equality is unfalsifiable without one | medium |
| R5 | Argv coverage: only `--selftest` was intervened, but the historical target is a `--check` verdict | medium |
| R6 | Shared harness and reverse direction: audit/measure reusing oracle code; C1 credited through C2 `--check` | low–medium |
| R7 | Schema drift: the contract sums only `eval_unparsed` and `unparsed_spawns` and does not refuse unknown keys. A new C1 uncertainty channel would be undercounted on future receipts. | low (scope only) |

## Proposed move: a two-channel separability protocol (no tool bytes change)

### Channel A: freeze provenance from pre-base blobs

1. Build the historical snapshot from two blobs, both read with `git show 741122d:<path>`:
   - findings and files from blob `10f5a706`;
   - evidence from blob `34bb3ee3`, joined on `(file, line, class, rule)`.
2. Refuse unless the join is exactly 1:1 over 11 rows. Keep every other key verbatim. The translator never opens `tools/`.
3. Freeze four variants, with expected results in contract row units:

| Variant | Claim | Expected |
|---|---|---|
| Raw r19, unmarked | any | `2` `[evidence_audit_input_invalid]` (discloses K1) |
| Joined | `{11,11,0,0,false}` | `1` `[observed_count_mismatch, lead_count_mismatch]` |
| Joined | `{11,10,1,0,false}` | `0` `[evidence_audit_clean]` |
| Joined | SCORECARD literal `{6,5,1,0,false}` | `1` `[finding_count_mismatch, observed_count_mismatch]` (surfaces K2 for Main) |

4. **Temporal pin:** the commit that freezes these digests must be an ancestor of the first post-741122d commit that touches `tools/mado-tripwire.py`.

### Channel B: full-tree runtime intervention

1. Extract the candidate commit with `git archive <commit> | tar -x` into a temp dir. This avoids a worktree and any Git index or jj mutation.
2. Run these states, sequentially, one child at a time, with the 384 MiB / 15 s cap:
   - base (`46c82902`);
   - changed (candidate);
   - absent;
   - **read-detector**: a FIFO at the C1 path, so any read times out;
   - **exec-detector**: inert bytes that only drop a marker file inside the temp dir;
   - **harness-hostile**: the same FIFO/marker pair replacing `round-22/oracle/`.
3. Use the exact admission argv in every state: `--selftest FIXTURE_ROOT` plus `--check BUNDLE --root ROOT` for every bundle, including the four historical variants.
4. Pass criteria:
   - (exit, stdout, stderr) are byte-equal across base, changed and absent;
   - no timeout and no marker appears;
   - the fixture-tree sha256 is unchanged before and after each state.
5. **Positive control:** a staged copy of the gate with one appended line that hashes the C1 path into stdout. It must diverge between base and changed and time out on the FIFO. Discard it afterwards; it never enters `tools/`.
6. **Reverse check:** the C1 oracle verdict bytes must be invariant to the C2 tool being present, absent or replaced by a FIFO. C1 admission must not consume any C2 `--check` verdict.
7. **R7 disclosure:** C2's capability statement covers only receipts whose uncertainty sits in the two contract counters.

## Risks

- The joined labels come from detectors of rejected rounds. They are used as frozen data only and admit nothing. If HistoricalC3 finds a source disagreement on any row, drop the joined variants rather than relabel them.
- K1 makes the registration wording unattainable literally. Main must pick between the translated artifact and the faithful-invalid outcome and disclose the choice. This proposal does not silently shrink scope.
- The FIFO state can cost up to 15 s per argv on misbehavior.
- The exec-detector must stay inert. If the sentinels object, drop that state and disclose R3 as unverified.
- `git archive` omits untracked w1 files. Seal the fixtures into the commit first, or copy them in with recorded digests.

## Verification for Main (after seal; none run here)

1. Recompute the Channel A snapshot from blobs `10f5a706` and `34bb3ee3`, assert an 11-row 1:1 join, and pin its sha256 before any C1 tool commit.
2. Check freeze-commit ancestry with `git merge-base --is-ancestor`.
3. Run all Channel B states and assert equality and the positive-control divergence.
4. Check that C1 oracle bytes are invariant to the C2 tool.
5. Statically grep `audit/measure.py` for any reference to `round-22/oracle/` or `tools/mado-tripwire.py`.

## Unknowns

- How base `46c82902` and the candidate label `r13-root.jsonl:4`.
- Source grounding of the 10 observed rows against the raw input bytes (HistoricalC3 owns this; it is [INFERENCE] here).
- Harness code did not exist when I wrote this, so R6 is a prescription, not an observed defect.
- Main's decision on K1 and K2.

## Tooling

No installs or updates. Commands used were read-only: `git show`, `git log`, `git rev-parse`, `git merge-base --is-ancestor`, `git status`, `sha256sum` and `sed` for hashing committed bytes. No detector, scanner, harness or payload was run.

## Additional Main-authorized deliverable: future independence driver

Authored `.ufo/waves/round-22/audit/independence.py` only; `assemble.py` and `measure.py` remain AuditHarness-owned. Coordinated its exact schema with `MadoR22.AuditHarness`: `mado-r22-audit-fixtures-v1`, complete `cases[]` with `bundle`, `bundle_sha256`, `root`, `expected.code`, and exact `input_entries` inventory plus `expected.sha256`. No guessed field names, shape-discovery population, or empty-list fallback remains.

Future invocation after a sealed fixture population and the first implementation commit:

```sh
python3 -I .ufo/waves/round-22/audit/independence.py \
  --revision CANDIDATE_COMMIT --baseline 741122d177ae8ff68a73768777f20484d5bdcbe4 \
  --fixtures LANE_RELATIVE_SEALED_AUDIT_ROOT
```

The driver stages only tracked candidate bytes using `git archive` into a temporary directory outside the source root. It validates the manifest seal and exact input inventory, then runs `--selftest` and every sealed `--check` with its per-case root across baseline/changed/absent/FIFO/import-execution-marker states. Candidate and baseline must differ. Children are sequential, 384 MiB, 15 seconds, 1 MiB per output stream, with owned process-group cleanup. Original executable permission bits are preserved on classifier replacements. Candidate gate and fixture bytes are checked for stability.

Receipts retain argv, exits, stdout/stderr and hashes. Equality compares exit and raw-stream hashes, expected exits must match, and selftests must return 0. A separate classifier-hash positive control must distinguish baseline/changed and time out on the FIFO; intentional execution of the inert marker replacement must create its marker and exit 83. This is finite intervention evidence, not semantic correctness, universal noninterference, or admission. Exact finding-ID correctness remains `measure.py`'s responsibility. The reverse-direction and oracle-directory interventions remain recommendations; this driver does not claim them.

**Not run:** syntax checks, assembly, tests, scanners, driver, positive controls, or any measurements. Main must review and exercise the script after seal. No installations.
