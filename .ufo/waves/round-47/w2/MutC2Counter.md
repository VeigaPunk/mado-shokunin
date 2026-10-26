# MutC2Counter-6 — mutation test of PRED-C2-r47 (w2, round 47, 2026-10-26)

Seat: `MutC2Counter-6` (leaf; no subagents). Scratch: `/fast/scratch/hyaku/mado-r47/MutC2Counter-6` (removed at the end). Findings land in `.ufo/waves/round-47/w2/MutC2Counter-6/`; this report is `.ufo/waves/round-47/w2/MutC2Counter.md`.

## Method

Counter under test: `quality/counters/c2-r47-terminal-entry.py` (sha256 `cdd4c8460c7289cedab3f8c7426cf80065516d7d51df3ea56272e614bc6e9be5`; the lane file is byte-identical to the pristine scratch copy — untouched, hash verified). Harness: `.ufo/waves/round-47/ctl/c2/build-control.py` + `run-controls.py` in a scratch clone. Per the C2 harness, “Every mutation is a commit in the scratch clone $S/ctl (POS tree + one defect); the clone's toplevel is asserted before the first commit.” (ctl/c2/run-controls.py:4-5). I ran a scratch copy of the runner with `C2R47_COUNTER`/`C2R47_SEAT` pointing at my scratch counter copies and scratch receipt dirs — the shared `receipts/ctl-c2/` was never written. POS tree built at commit `6e83dee58ffed8b3de38a3d8a3d518834e72d59a` (on base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`), from the pinned tag tarball `xdg-terminal-exec-v0.14.3.tar.gz` (sha256 `82ac2dfdb357361d15f5163cdeb3cfd457bbb30bf5d2e14436393f493bd32afe`, fetched from `https://codeload.github.com/Vladimir-csp/xdg-terminal-exec/tar.gz/refs/tags/v0.14.3`, kept in this seat dir).

Baseline (pristine counter): POS `admitted=1/1 TARGET_MET` exit 0; all 10 negatives (BASE, QUOTE, BRANCH, HELD, RECEIPT, NOSTEPS, OBS, NOSHA, RANGE, PIN) `TARGET_MISSED` exit 1, each reporting its intended clause token. `harness/pristine.log` / `harness/pristine-summary.txt` in this seat dir.

Each mutant = one minimal behavior-bearing edit of the pristine counter, then the full 11-control matrix re-run (15 runs × 11 scores = 165 counter invocations; ~1.5 s each, sequential — no parallel runs share the ctl clone). Verdict: **KILLED** iff POS fails or any negative is falsely admitted (exit 0); **SURVIVED** otherwise.

## Results (per-mutant control verdicts)

| mutant | defect | POS | negatives | verdict |
|---|---|---|---|---|
| drop-a | `cl["a"]=1`, early return removed | MET | all MISSED (BASE token `clause=a entry_absent` gone) | **SURVIVED** (equivalent) |
| drop-b | `cl["b"]=1` | MET | all MISSED | **SURVIVED** |
| drop-c | `cl["c"]=1` | MET | BRANCH, PIN falsely admitted | KILLED |
| drop-d | `cl["d"]=1` | MET | QUOTE, RANGE falsely admitted | KILLED |
| drop-e | `cl["e"]=1` | MET | NOSTEPS falsely admitted | KILLED |
| drop-f | `cl["f"]=1` | MET | RECEIPT, OBS, NOSHA falsely admitted | KILLED |
| drop-g | `cl["g"]=1` | MET | all MISSED | **SURVIVED** |
| drop-h | `cl["h"]=1` | MET | HELD falsely admitted | KILLED |
| drop-i | `cl["i"]=1` | MET | all MISSED | **SURVIVED** |
| refpin-any | branch-ref list check removed | MET | all MISSED (BRANCH token gone) | **SURVIVED** (equivalent) |
| refpin-any2 | all ref-pin checks removed | MET | BRANCH falsely admitted | KILLED |
| recheck-any | `recheck_ok` always true | MET | all MISSED | **SURVIVED** |
| held-skip | `clause_h` always true | MET | HELD falsely admitted | KILLED |
| nosha-skip | `resolver_sha256` check removed | MET | NOSHA falsely admitted | KILLED |

Evidence: `diffs/<mutant>.diff` (all 14), `harness/<mutant>.log` + `-summary.txt`, `results.json`.

## Reproduction recipe (all probe/control commits are in the scratch ctl clone; the scores below used)

`python3 -I quality/counters/c2-r47-terminal-entry.py --repo <scratch>/ctl --rev <defect-sha>` — first `git -C <scratch>/ctl rev-parse --show-toplevel` must equal `<scratch>/ctl`; each defect is one commit on the POS tree. Per-probe log (defect + commit + pristine/mutant verdict lines) in `probes/`.

## Findings

### Coverage holes (mutants no control kills — the counter can be weakened without any control noticing)

1. **Clause b (provenance head) is unchecked by any control.** `drop-b` survives the whole 11-control suite. Clause b (“provenance head, unfenced lines inside the first 20 raw lines”, counter:26-29) is the only clause with no dedicated negative. Reproducible defect: remove the `verified-at: 2026-10-26` head line from the POS entry and commit — pristine scores `clauses=a:1 b:0 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=0` exit 1; the mutant admits (`admitted=1/1`, exit 0). Second defect: cite ghost id `S999` — same flip (probe logs `probes/probe-b-verifiedat.log`, `probes/probe-b-ghost.log`; defect commits `4bb74f40346d3fec6aa2e5d197a105b3cea1b601`, `4315a7931f5a4152a83c083e5e57cd2fd0c4644c`). A corrupted source count, `verified-at`, ghost id, tier/status/opened/used-by cell, `MIN_ID` breach, or head-window violation would all pass the current suite.
2. **Clause g (README index row) is unchecked.** `drop-g` survives; removing the `corpus/README.md` index row for the entry flips pristine (exit 1) to the mutant (exit 0) — `probes/probe-g-readme-row.log`. The `g` clause has no negative control.
3. **Clause i (ground-term census) is unchecked.** `drop-i` survives; swapping `-`/`_` in all four `GROUND` terms in the entry (census present=0) flips pristine (exit 1, `clauses=… i:0 …`) to the mutant (exit 0) — `probes/probe-i-terms.log`. A ground-present-at-BASE violation is also untested (only the `>= 2 present at REV` side is reachable, and no control exercises it).
4. **The recheck-cell validation (clause b) is unchecked.** `recheck-any` survives; changing the S327 row's recheck cell `on-release` → `whenever` flips pristine (exit 1) to the mutant (exit 0) — `probes/probe-recheck-cell.log`. No control corrupts a row's recheck cell or the head `recheck:` line.

These are honest misses in the control set, not defects in the counter: pristine rejects every one of the five probe defects (exit 1, correct clause flag), and the mutant admits them — so the *controls* would not catch a counter that dropped those checks. The v2 control set should add negatives for each: a verified-at/source-count/ghost-id head defect (b), a recheck-cell defect (b), a README-row removal (g), and a ground-term removal (i).

### Redundant / defense-in-depth checks (equivalents — not holes)

5. **`drop-a` is equivalent on the suite and nearly equivalent in general**: the entry-absent-at-BASE precondition is doubly enforced — `main()` raises `Setup` exit 2 when the entry exists at BASE (counter:766-768), and an entry-absent-at-REV revision is still rejected by the `fetch_pins=0` early return (counter:737-741) or by clause e (`steps=0 <6`). Removing score()-level clause a changes no observable verdict.
6. **The `BRANCH_REFS` list check (`counter:383-384`) is dead weight**: every name it refuses (`main`, `master`, `HEAD`, `head`, `latest`, `dev`, `trunk`, `develop`, `Main`, `Master`) is refused anyway by the general pinned-ref rule `ref != TAG and not re.fullmatch(r"[0-9a-f]{7,40}", ref)` (counter:385-386) — `refpin-any` survives because N-BRANCH is still rejected by the second rule. The ref-pin check *as a whole* is load-bearing: `refpin-any2` (both rules removed) is killed by N-BRANCH (false admit). The list is kept only for the error-message token `url_branch_ref`; the v2 controls should pin the *general* rule (any non-tag non-hex ref) rather than the list.

### Mutation-killed checks (control coverage confirmed)

drop-c (pin-bound + ref-pin: BRANCH, PIN), drop-d (quotes: QUOTE, RANGE), drop-e (chain steps: NOSTEPS), drop-f (capture: RECEIPT, OBS, NOSHA), drop-h / held-skip (held rows: HELD), nosha-skip (resolver digest: NOSHA).

## Host/tool notes

Tooling: no new tools installed; only `curl` for the pinned tarball fetch (official source URL, sha256 verified, recorded above). No pacman transaction attempted (host pause respected). Nothing outside the lane was written; the lane counter was never modified; the shared `receipts/ctl-c2/` was not touched. All fixture reads/writes happened in the seat scratch and seat dir. Quote verification: `verify-quotes.sh` (in this seat dir) greps every source quote and receipt token cited above against its named file/line — ran clean.
