# R66RevRegister — C1 register-counter attack report (round 66, wave w1)

Seat: R66RevRegister · Lane: mado-shokunin · Lane HEAD at attack time: `ed980316e330703030d0c17b2a7098e058295b99` (claims freeze) · Base under claims: `eafd500fa7be76dca59e729435e231a5032cc037` · Date: 2026-11-03.
Under attack: frozen baseline `quality/counters/c1-r65-register.py` (committed, `git status --porcelain quality/counters/` empty → untouched) and candidate draft `.ufo/waves/round-66/w1/R66ExecRegister/c1-r66-register.py` — initially sha256 `4e1b94ff94309e3bd728b50bb83991c5ca71f5a46602eb96afb06313c5bbf829`, superseded during review by `8ca15c66e953b093913559b7eda7f390c111a79062ef22f75caa498a4a04ec31` (authorized defect fix: `GIT_NO_REPLACE_OBJECTS=1` added to the counter's git env; predicate strings and 15 selftest cases untouched — both versions fully re-run, see F-8; read-only; no peer-draft mutation).
Tool installs: **none** (RULES.md respected; no pacman; no uv/npx needed). Scratch git only, under `/fast/scratch/hyaku/mado-r66/R66RevRegister/`, `git rev-parse --show-toplevel` asserted before every fixture's first commit; scratch removed before yield (reproducible via `.ufo/waves/round-66/w1/R66RevRegister/attack-r65-register.sh`).

## Verdicts

| Attack | Baseline c1-r65 | Candidate c1-r66 |
| --- | --- | --- |
| genuine (real HEAD PROVINCE.md + 4 named receipts) | rc=0 MET | rc=0 MET |
| A1 duplicate heading, genuine block first | rc=0 MET (defect) | rc=1 MISSED `heading-count=2` |
| A2 duplicate heading, broken decoy first | rc=1 MISSED | rc=1 MISSED `heading-count=2` |
| B one row without receipt (em-dash cell) | rc=0 MET (defect) | rc=1 MISSED `row-receipt-missing='windows desktop plane'` |
| C1 file-plane CLEAN only, **tree intact** | rc=0 MET (defect) | **rc=0 MET — see F-1** |
| C2 file-plane CLEAN only, LIVE popped from tree (executor construction) | rc=0 MET (defect) | rc=1 MISSED `exact-live-line-missing` |
| C2b tampered live line (file-plane wording inside gate-live) | rc=0 MET (defect) | rc=1 MISSED `exact-live-line-missing` |
| F1 forged state cells + valid receipts + exact live line | rc=0 MET | rc=0 MET (declared truth limit) |

Baseline score on claim fixtures (A/B/C + genuine) = **1/4** ("before at most 1/4" confirmed independently); candidate = 4/4 on its committed construction (their `controls.json` numbers reproduce: baseline 1, candidate 4). Selftest: `python3 …/c1-r66-register.py --selftest` → 15/15 PASS rc=0, also from a foreign cwd (hermetic).

## Findings

**F-1 (MEDIUM — control-construction dependence, not a draft defect; RESOLVED by L1 decision 2026-11-03, option (a)).** The candidate's gate leg is tree-level per the frozen sentence ("the exact live CLEAN line in `.ufo/waves/round-65/receipts/gate-live-r65.txt`"): when `gate-live-r65.txt` remains committed at rev, a register whose receipt cells cite **only** the file-plane receipt is ACCEPTED — `fixture-c1-fileplane-clean-only`: `MADO_R66_REGISTER: headings=1 rows=8 groups=8/8 receipts=4 resolved=4 gate=ok verdict=TARGET_MET`, rc=0, zero reasons on stderr. This matches the draft's own selftest case `unreferenced-live-receipt` (expected accepted) and the r65 reviewer's clause (c), which was written tree-level (`.ufo/waves/round-65/w1/R65RevRegister.md`). Consequence: the declared control "only a file-plane CLEAN receipt rather than the exact live receipt" is rejected **only** under the executor's construction (`objects.pop(LIVE)`; their `candidate-file-plane-only.txt`: rc=1 `gate=missing`), while r65's own documented accepted forge (R65RevRegister A3) kept the receipts tree intact — under that construction the candidate accepts. **L1 resolution (binding for the harness): option (a)** — the candidate's frozen tree-level gate requirement is preserved; the harness `file-plane-only` control MUST omit the live receipt object from the fixture tree (not merely its citation); the acceptance of an unreferenced-but-committed live receipt at rev is disclosed as a **bounded citation gap**, a truth limit distinct from the state-cell-truth limit (F-2). No target tightening after scoring.

**F-2 (LOW — declared truth limit).** State-cell truth is not measured, as declared: `fixture-f1-forged-state-cells` (all eight state cells forged false, receipts and exact live line untouched) → rc=0 MET on both counters. Same conclusion as r65 A3; the r66 predicate does not change it. Do not call fixed.

**F-3 (LOW — baseline historical; candidate strictly stronger than declared here).** The frozen r65 counter inherits `GIT_*` (`env = dict(os.environ)` in its `git()`): `GIT_DIR=<evil>/.git` redirects reads (genuine fixture → rc=1 MISSED reading evil-empty's PROVINCE); `GIT_DIR=<evil-perfect>/.git --rev <evil-rev>` through a clean victim repo that does **not** contain that rev → rc=0 TARGET_MET; `GIT_ALTERNATE_OBJECT_DIRECTORIES=<evil-perfect>/.git/objects` alone → rc=0 TARGET_MET. The r66 draft scrubs every `GIT_*` var and fails closed on all three vectors (rc=2 `setup=error`), with scrub proven active (`GIT_DIR=/nonexistent` → rc=0 MET). C1-r66's declaration names no env hardening; keep the scrub at integration. [Disclosure: my first G2/G3 pass was confounded — the victim was a directory-copy of the genuine fixture and already contained the evil rev; superseded by the clean-victim runs above.]

**F-4 (INFO — baseline asymmetry closed).** r65 reads only the FIRST heading block: duplicate-heading with genuine block first → rc=0; decoy first → rc=1. The candidate counts headings whole-file and rejects both (rc=1 `heading-count=2 expected=1`). Declared leg satisfied in both orderings.

**F-5 (INFO — row-shape edges, all within the declared letter).** Inserted cell (receipt shifts out of the 4th cell) → rc=1; appended 5th cell (receipt stays 4th) → rc=0 (cell-count exactness not enforced; predicate names the receipt cell, not cell count); uppercase `.TXT` pointer is dropped from the receipt set by the frozen case-sensitive pattern (row still passes on its other pointer, rc=0 — identical semantics to r65); traversal-shaped token `.ufo/waves/round-65/receipts/../../../etc/passwd.txt` matches the frozen pattern but never resolves → rc=1 (inert, fail-closed); sentinel right after the heading → rc=1; duplicate group row → rc=1 (`rows=9 expected=8`, `rows=2 expected=1`).

**F-6 (INFO — exact-line strictness).** Trailing space appended to the live CLEAN line → rc=1; prefix-substring variant → rejected (selftest `live-line-substring`). The gate compares whole `splitlines()` elements, so byte-exact. A symlink blob at LIVE_PATH fails closed (blob content is the target path string, code-derived).

**F-7 (INFO — setup/contract).** `--repo /nonexistent-dir` → rc=2; unknown rev → rc=2; missing `--rev` → rc=2 (argparse); option-like `--rev --exec=virus` → rc=2 (`--end-of-options` holds, no injection). Exactly one `MADO_R66_REGISTER:` line on stdout, `C1_R66: detail=…` diagnostics on stderr, rc∈{0,1,2}. Counter reads git objects only (`git -C … show/rev-parse`; no worktree opens, no scratch, no network). Candidate on real lane: base `eafd500` rc=0 (their `genuine-base.txt`), HEAD `ed980316` rc=0 — no false positive on the latest committed register (heading occurs exactly once in PROVINCE.md at HEAD).

**F-8 (INFO — superseding replace-ref hardening independently checked).** New draft sha256 `8ca15c66e953b093913559b7eda7f390c111a79062ef22f75caa498a4a04ec31` sets `GIT_NO_REPLACE_OBJECTS=1` after scrubbing inherited `GIT_*`. Selftest remains 15/15 PASS. The independent structural matrix re-run gave the same results as above, including the two deliberately accepted truth limits. Replace-ref probes: R1 planted genuine-rev → broken-commit replacement; raw `git show REV:PROVINCE.md` demonstrably returned broken content, while the candidate accepted the actual genuine revision (rc=0). R2 planted broken-rev → genuine-commit replacement; candidate rejected the actual broken revision (rc=1). Replace refs were removed after probing. This establishes resistance in both substitution directions. The second steering pass's clean-victim directory was absent, so its G2/G3 rc=2 results are setup failures, not additional steering evidence; the earlier existing-clean-victim results remain the valid G2/G3 evidence. No old draft bytes were retained for an independent textual diff.

## Commands (committed-path-ready)

```
python3 quality/counters/c1-r65-register.py --repo <fixture> --rev <rev>   # baseline, rc per table
python3 .ufo/waves/round-66/w1/R66ExecRegister/c1-r66-register.py --repo <fixture> --rev <rev>
python3 .ufo/waves/round-66/w1/R66ExecRegister/c1-r66-register.py --selftest   # rc=0, 15/15
bash .ufo/waves/round-66/w1/R66RevRegister/attack-r65-register.sh  # requires genuine fixture setup below; baseline driver only
```

Fixture setup prerequisite: initialize `/fast/scratch/hyaku/mado-r66/R66RevRegister/fixture-genuine` as a Git repository; assert its toplevel before committing. Populate `PROVINCE.md` and the four named receipts from `git show eafd500fa7be76dca59e729435e231a5032cc037:PATH`, preserving their paths. Then run the driver, which creates variant fixtures and prints the baseline matrix. It does not reproduce the separately executed candidate/replace-ref probes. Fixture commit IDs depend on timestamps. The driver's original G2/G3 cases use a copied victim containing the genuine objects and are confounded; use the separately described fresh clean-victim construction for semantic steering evidence.

## Limitations and scope

- Review-only seat: no draft changes, no lane mutations, no commits outside scratch (scratch removed before yield).
- State-cell truth (F-2) and the bounded citation gap (F-1, option (a) chosen by L1) remain distinct limitations — recorded, not fixed.
- Candidate hardening beyond the declaration (GIT_* scrub) was verified empirically, not formally: `HOME`/system-gitconfig injection was not probed (no plausible read-path effect found for `show`/`rev-parse`; residual risk noted, parity with baseline).
- Baseline steering (F-3) is recorded for the frozen instrument only; r65 stays frozen per claims.

## Changed drafts

No production edits by this reviewer. Executor independently superseded its draft with the replace-ref fix identified above; latest reviewed sha256 is `8ca15c66e953b093913559b7eda7f390c111a79062ef22f75caa498a4a04ec31`. The popped-tree control outputs were inspected in executor receipts; the retained-tree variant and other structural probes were independently executed here. LSP was not available among mounted tools, so analysis used source inspection and targeted runtime probes, not semantic references/diagnostics.
