# ClaimsSeparable — round 16 (mado-r16-w1)

Seat: `MadoR16.ClaimsSeparable` (connector, leaf). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Baseline: `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
Scope: causal separability of C1 (U7 Waybar coverage) and C2 (static action-plan safety gate), and whether the declared "C1 coverage = lowest active rubric" selection holds under the lane's own pre-registered counting commands.

Status: read-only source analysis. Nothing edited, committed, installed or executed beyond the read-only counts listed in §7. No `measure.py`, `mado-verify.sh`, selftest, pacman, service or live probe was run. Tool rules were read (`~/.omp/agent/RULES.md`); nothing was installed.

## 1. Verdict

1. **C1 and C2 are separable at the measured-object and gate level.** C1 is measured by a revision-bound counter over `corpus/SOURCES.md`, `corpus/README.md` and `corpus/knowledge/`. C2 is measured by `tools/mado-action-plan.py` over declared JSON. `tools/mado-verify.sh` has zero non-comment references to `README`, `SOURCES` or `QUALITY` at baseline, so neither claim can move the gate verdict through corpus indexes.
2. **They are not separable on one axis: calibration.** `corpus/QUALITY.md` is C2's edit site (criterion 21) and also the measured object of the calibration rubric. The calibration verdict for C2 flips sign depending on how a multi-line criterion is counted (§3.2).
3. **The declared lowest-axis selection is not supported by the lane's own rubric.** At baseline, calibration scores **6.0000** under the pre-registered literal command and **7.5000** under the block reading. Both are below coverage 8.5714 (6/7), which the round-16 claim names as "lowest active finite rubric". The claim does not mention calibration. This is the central finding (§4).
4. **C2 does not contend for the lowest-axis slot on any scored axis.** Its operability effect is a binary capability row (absent 0 → demonstrated 1), which the SCORECARD keeps outside the 10-point axis rubrics (`SCORECARD.md` "Capabilities": "— none yet —"). Its scored operability rubrics (selftest 372/372) are unchanged by design.

## 2. Evidence — causal separability

### 2.1 Write sets (declared, from the spec and LOG round-16 entry)

| Claim | Measured object | New or edited artifacts | Shared with the other claim |
|---|---|---|---|
| C1 U7 | `git show REV:corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/*.md`, `.ufo/waves/round-16/measure.py` | `corpus/knowledge/<U7 note>.md`; SOURCES rows S053 (Waybar man `waybar-custom.5.scd`) and S054 (`src/modules/custom.cpp`); README row; `measure.py` U7 extension | SCORECARD, LOG (L1 only) |
| C2 gate | `tools/mado-action-plan.py` `--selftest`, `--plan`, `--policy`, `--frozen DIR` over declared JSON | `tools/mado-action-plan.py`, persisted paused policy, frozen digest dir, SKILL standing instruction, QUALITY criterion 21 | SCORECARD, LOG, SKILL.md (L1 only); QUALITY.md (calibration object) |

Working-tree state at this read (uncommitted, not yet authored by this seat): `git diff --stat 32c4fda` over `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/README.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `tools/mado-verify.sh` shows 4 files changed, +86 lines (SCORECARD +29, SKILL +16, QUALITY +22, SOURCES +19). `tools/mado-verify.sh` is unchanged. `corpus/QUALITY.md` now carries criterion 21 (line 82, round-16 section) and `corpus/lessons/round-16.md` exists with rows M1 and M2. S053 and S055 are absent at baseline.

### 2.2 Measurement coupling

- **Gate**: `tools/mado-verify.sh` at baseline has no non-comment reference to `README`, `SOURCES` or `QUALITY` (`grep -nE 'README|SOURCES|QUALITY'` minus `#` lines → 0 hits). `corpus/knowledge/` and `corpus/lessons/` appear only in comments. Gate sha at baseline: `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207`, the same digest recorded at round 15. C1 cannot change the gate verdict; C2 does not touch the gate. **Separable.**
- **Navigation** (intra-C1): the round-15 counter requires every `corpus/knowledge/*.md` to appear exactly once in `corpus/README.md`. A U7 note landing without its README row fails navigation. This is an intra-claim duty, not a cross-claim coupling.
- **Calibration**: C2's criterion 21 changes the calibration object. See §3.2.
- **Shared write surfaces** (SCORECARD, LOG, SKILL.md): integration-sequencing only. No measurement reads a number from another claim's artifact. L1 integrates once.

### 2.3 Content coupling (discernment, not separability)

U7 overlaps existing treatment. `corpus/knowledge/gate-standing-use.md` §6 already lists "waybar module text" as UNKNOWN by constraint, and `SKILL.md` routing states module text is config-only with no IPC verb in waybar 0.15.0 (`SKILL.md` plane map, bar row). The U7 note must add source-level producer-contract and renderer-boundary facts, not restate that UNK. A marker-only `covers: U7` count can admit a near-duplicate. Discernment risk, not a separability failure.

## 3. Evidence — calibration axis (the coupling point)

### 3.1 Counts at baseline `32c4fda` (read-only `git show` + grep/awk; this seat)

The pre-registered command (`corpus/SCORECARD.md` round-12 table, line 234) is `grep -cE '^[0-9]+\. .*lessons/' corpus/QUALITY.md` over `grep -cE '^[0-9]+\. '`. It is line-based. Criteria 18, 19 and 20 cite their lessons on continuation lines (`QUALITY.md` baseline lines 49, 55, 77), so the literal command does not see them.

| Reading | Command or rule | Count | Score (÷ criteria × 10) |
|---|---|---|---|
| Literal (pre-registered) | same-line `^N. .*lessons/` | 12 / 20 | **6.0000** |
| Block | criterion block (number to next number or heading) contains `lessons/` | 15 / 20 | 7.5000 |
| Strict literal (excl. 15–16 external traps, QUALITY provenance note) | same-line minus 15, 16 | 10 / 20 | 5.0000 |
| Strict block | block minus 15, 16 | 13 / 20 | 6.5000 |

Calibration was last scored at round 12 as 11/16 → 6.8750 (`SCORECARD.md` round-12 results). Rounds 13–15 added criteria 17–20 and did not re-score calibration; round-15 verdict says "calibration unchanged, no scored move" (`SCORECARD.md` round-15 table). Retired: none (`SCORECARD.md` Retired sections). Calibration therefore remains an active finite rubric.

### 3.2 Effect of the in-progress criterion 21 (working tree, not committed)

| Reading | Baseline (20) | Working tree, criterion 21 with citation on line 2 (as now) | Working tree, citation moved to line 1 (proposal) |
|---|---|---|---|
| Literal | 12/20 = 6.0000 | 12/21 = **5.7143** (−0.2857, harm) | 13/21 = **6.1905** (+0.1905) |
| Block | 15/20 = 7.5000 | 16/21 = 7.6190 (+0.1190) | 16/21 = 7.6190 (+0.1190) |

Criterion 21 (QUALITY.md line 82) carries its lesson citation at line 95 (`lessons/round-16.md#mistakes M1/M2`). The resolver requirement from round 12 ("counting only criteria whose cited paths resolve") is met: `corpus/lessons/round-16.md` now exists with rows M1 and M2. So the cited path is not the problem; the line placement is. The C2 edit therefore lowers the literal calibration score while raising the block score. Whether C2 harms calibration depends on a counter reading the lane has not pinned.

## 4. Evidence — lowest-axis selection

Active finite rubrics at baseline (scores from last measured rounds; baseline values were not re-measured for every rubric):

| Rubric | Last measured | Score | Source |
|---|---|---|---|
| coverage / admitted-note reachability | 29/29 (round 15 measured content) | 10.0000 | `LOG.md` round-15 entry; navigation counter |
| coverage / sourced current-art ground | U1–U6 = 6/7 (round 15) | **8.5714** | `SCORECARD.md` round-15 table |
| calibration / lesson-grounded criteria | 12/20 literal at baseline (this seat) | **6.0000** (block 7.5000) | §3.1 |
| freshness / file-plane gate agreement | 29 PASS / 0 FAIL / 0 UNKNOWN (round 15) | 10.0000 | round-15 `gate-file-plane` evidence |
| operability / hermetic selftest | 372/372 (round 15) | 10.0000 | round-15 `gate-selftest` |
| operability / finite diagnostic subsets (rounds 13–14) | 10/10 on their subsets | 10.0000 | `SCORECARD.md` rounds 13–14 |
| operability / capability acquisition (C2) | absent → demonstrated | binary 0 → 1 (not on the 10-point scale) | round-16 claim; `SCORECARD.md` "Capabilities" |
| depth, adjacency | unscored (no bounded rubric) | — | `SCORECARD.md` round-12 baseline |

Under the lane's own rule ("lowest … rubric", `SCORECARD.md` round-12 lowest-axis statements), the lowest active scored rubric at baseline is **calibration**, not coverage. Under every reading in §3.1 calibration is below 8.5714. The round-16 declaration ("C1 coverage, lowest active finite rubric 6/7 → 7/7") does not address calibration. The declaration is therefore not supported by the lane's pre-registered counting commands.

C2's capability row is binary and sits outside the 10-point comparison. Comparing 0 with 8.5714 is not a valid ordering; it is a separate capability track.

After C1 lands, coverage moves to 10.0000 and calibration becomes the lowest scored axis regardless of C2.

## 5. Affected axes

- **Coverage** (C1): improved if U7 admitted with reciprocal S053/S054 joins and README row. Rubric would reach 10.0000 on the finite denominator.
- **Calibration**: the separability-relevant axis. C2's criterion 21 moves it by sign depending on the reading (§3.2). Also the actual lowest scored axis (§4).
- **Operability** (C2): capability row only; scored selftest unchanged; gate sha unchanged. No scored improvement claimed by the SCORECARD mechanism.
- **Freshness, depth, adjacency**: no interaction found. Freshness is the gate file plane, which neither claim touches.
- **Quality** (host-safety harm, round 15): C2's classifier and criterion 21 are the remediation for the round-15 M2 harm. No C1 interaction.

## 6. Proposed move (one bounded change)

**Place criterion 21's lesson citation on its first line and state the calibration reading in SCORECARD.**

1. Edit `corpus/QUALITY.md` criterion 21 so `(lesson: lessons/round-16.md#mistakes M1/M2)` sits on the line starting `21. ` (line 82). Text unchanged otherwise. Expected literal reading 12/20 → 13/21 = 6.1905 (vs baseline 6.0000); block reading 7.6190 (vs 7.5000). Predictions, not measurements. L1 measures them.
2. In the round-16 SCORECARD entry, record the calibration rubric's reading explicitly: literal (pre-registered) and block, both at `32c4fda` and at the candidate, with the lowest-axis finding from §4. Do not re-score silently.
3. Do not change C1's declared claim. Record that under the pre-registered rule calibration is the lowest scored axis (6.0000 literal / 7.5000 block) and that C1's coverage move is therefore not the lowest-axis move. L1 chooses between explicit re-declaration by operator ruling and selecting calibration for this round. This seat does not make that choice.

Why this move and not another: it is the smallest edit that makes C2 non-harmful on calibration under the literal reading while keeping the block reading non-harmful, and it changes no gate, navigation, source or knowledge file. It also uses a path that now resolves (`corpus/lessons/round-16.md` M1/M2).

## 7. Risks and limits

- **Counter ambiguity**: the pre-registered calibration command is line-based and blind to continuation-line citations. The fix in §6 makes the literal reading agree with the block reading for criterion 21, but criteria 18–20 remain literal-blind at baseline. A complete fix needs a pinned counter revision, disclosed as a rubric change, not a silent swap.
- **Uncommitted tree**: criterion 21 and `corpus/lessons/round-16.md` are uncommitted working-tree content. The resolver rule ("paths resolve at the named commit", QUALITY criterion 8) binds only after commit. L1 confirms at commit time.
- **Lowest-axis selection**: §4 is an observation under the lane's stated rule. The lane may legitimately re-declare the rule, but only with an explicit disclosed ruling in the SCORECARD. Silent re-selection would be an own-goal under QUALITY criterion 5 ("a rejection is kept").
- **Baseline freshness of scores**: navigation, freshness and selftest values are last-measured round-15 numbers, not re-measured at `32c4fda`. The calibration numbers in §3.1 were measured at `32c4fda` by this seat.
- **U7 duplication risk**: see §2.3.
- **C2 scope**: the classifier grades declared JSON actions. Its self-invocation tests cannot falsify the fixture shape. It neither intercepts tools nor repairs the host, as stated in the round-16 claim.

## 8. Verification for L1 (run once after integration; not run by this seat)

- `git -C mado-shokunin show 32c4fda873c9cb47a84c549b24b80ead2bcaa1ea:tools/mado-verify.sh | sha256sum` → expect `fba82a66…c207` (this seat read the same digest).
- After criterion 21 edit: `grep -cE '^[0-9]+\. .*lessons/' corpus/QUALITY.md` / `grep -cE '^[0-9]+\. ' corpus/QUALITY.md` → expect 13/21 literal.
- Block reading: awk block count over `corpus/QUALITY.md` → expect 16/21.
- `python3 .ufo/waves/round-16/measure.py 32c4fda873c9cb47a84c549b24b80ead2bcaa1ea` and the candidate revision: coverage 6/7 → 7/7 only if U7 lands with reciprocal S053/S054 and README row; navigation 29/29 → N/N complete.
- `bash tools/mado-verify.sh --selftest` must remain 372/372 (C1 and C2 do not touch the gate; any delta is an error).
- `python3 tools/mado-action-plan.py --selftest` for C2 (separate tool, separate count).

## 9. Commands run by this seat (all read-only)

- Read: `.ufo/waves/round-16/w1/spec.json` (context and items), `dispatch.json` (ClaimsSeparable entry), `corpus/lessons/round-15-verifier-spotcheck.md`, `corpus/lessons/round-15.md`, `corpus/lessons/round-16.md` (mistake rows), `corpus/QUALITY.md`, `corpus/knowledge/gate-standing-use.md`, `SCORECARD.md`, `SKILL.md`, `LOG.md` (round-12 to round-16 entries), `corpus/SOURCES.md` (grep), `tools/mado-verify.sh` (grep), `.ufo/waves/round-15/measure.py` (structure), `~/.omp/agent/RULES.md` (per contract).
- Read-only git: `git -C mado-shokunin show 32c4fda…:{corpus/QUALITY.md,corpus/SOURCES.md,SCORECARD.md,tools/mado-verify.sh}` piped to grep/awk/sha256sum; `git -C mado-shokunin diff --stat 32c4fda… -- <files>`.
- Not run: `measure.py`, `mado-verify.sh` (any mode), any selftest, `pacman`, `apt`/package query, services, `hyprctl`, screenshot, input or compositor probe, `omp` CLI, anything under `~/.omp/agent/agent.db*`.
- Installs/updates: none.
