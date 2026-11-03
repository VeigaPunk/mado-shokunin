# R66ExecRegister — C1 register counter

Axes: calibration (register discrimination), operability (hermetic CLI and useful miss reasons). Frozen scope: PRED-C1-r66 only. No production files changed.

## Changed drafts

- `.ufo/waves/round-66/w1/R66ExecRegister/c1-r66-register.py` → proposed production destination `quality/counters/c1-r66-register.py`.
- SHA256: `8ca15c66e953b093913559b7eda7f390c111a79062ef22f75caa498a4a04ec31` (supersedes `4e1b94ff94309e3bd728b50bb83991c5ca71f5a46602eb96afb06313c5bbf829`; sole change after R66SentFrontier's refs/replace steering demonstration: `git()` sets `GIT_NO_REPLACE_OBJECTS=1` after the inherited-env scrub, so `--rev` reads exactly the committed bytes; predicate clauses, selftest cases and verdict semantics unchanged).
- `.ufo/waves/round-66/w1/R66ExecRegister/demonstrate.py` is the retained reproducer for the committed minimal-fixture comparisons; not a proposed production dependency.

Counter requires exactly one returned-host heading, exactly eight rows covering the eight existing groups once, a resolving receipt in each fourth receipt cell, resolution of every extracted register receipt, and the exact frozen live CLEAN line in the dedicated live receipt. It reads repository content through git objects pinned to a resolved commit, never worktree files. Inherited GIT_* variables are removed from subprocess environments. Missing structural conditions produce individual `C1_R66: detail=...` diagnostics.

CLI: `python3 quality/counters/c1-r66-register.py --repo REPO --rev REV`; rc 0 met, 1 missed, 2 setup/usage error. Stdout marker `MADO_R66_REGISTER:` includes headings, rows, groups, receipts, resolved, gate, verdict, revision. `--selftest` uses strings only and does not invoke git or write fixtures. Interface and final SHA sent to R66ExecHarness, R66MutHardening, and R66RevRegister.

## Commands and retained evidence

All paths below are lane-relative. Full argv, stdout/stderr and child rc are retained in the individual comparison receipts.

1. `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show eafd500fa7be76dca59e729435e231a5032cc037:.ufo/waves/round-65/receipts/gate-live-r65.txt` — rc 0. Exact copied line and source command in `.ufo/waves/round-66/w1/R66ExecRegister/live-line-source.txt`:

   `MADO_VERIFY: CLEAN (52 pass, 8 notes; file + live planes verified read-only)`

2. `python3 .ufo/waves/round-66/w1/R66ExecRegister/c1-r66-register.py --selftest` — rc 0, 15/15 PASS. Receipt `.ufo/waves/round-66/w1/R66ExecRegister/selftest.txt`.
3. `python3 .ufo/waves/round-66/w1/R66ExecRegister/demonstrate.py` — rc 0, baseline correct=1/4, candidate correct=4/4. JSON evidence `.ufo/waves/round-66/w1/R66ExecRegister/controls.json`.
4. Candidate against actual base commit `eafd500fa7be76dca59e729435e231a5032cc037` — rc 0; `.ufo/waves/round-66/w1/R66ExecRegister/genuine-base.txt`.
5. `python3 .ufo/waves/round-66/w1/R66ExecRegister/replace-refs-check.py` — rc 0. Reproduces R66SentFrontier's finding and verifies the fix: a planted `refs/replace` redirecting an invalid register commit to genuine bytes no longer steers `--rev` reads; candidate reads the exact invalid committed bytes and reports `TARGET_MISSED` rc=1. Receipt `.ufo/waves/round-66/w1/R66ExecRegister/replace-refs.txt`.

| Fixture | r65 baseline rc | r66 candidate rc |
|---|---:|---:|
| Genuine committed register | 0 | 0 |
| Duplicate returned-host heading | 0 | 1 |
| One row without receipt; others resolve | 0 | 1 |
| Only file-plane CLEAN receipt | 0 | 1 |

Each cell has its own `.ufo/waves/round-66/w1/R66ExecRegister/{baseline,candidate}-{genuine,duplicate-heading,row-without-receipt,file-plane-only}.txt` receipt. The demonstrator extracts baseline source and genuine PROVINCE/receipt bytes from committed base objects. It creates one isolated git repository, verifies its exact toplevel before commit operations, then commits four minimal fixtures. No lane/fleet git mutations occurred. Scratch `/fast/scratch/hyaku/mado-r66/R66ExecRegister` was removed in `finally`; retained proof `.ufo/waves/round-66/w1/R66ExecRegister/scratch-cleanup.txt`. Removed fixture commit hashes remain in receipts for attribution; reproduction uses the retained driver, not availability of those deleted objects.

## Limits, risks, blockers

- State-cell truth is NOT measured. Invented state prose with valid per-row pointers intentionally passes selftest. Historical live receipt presence does not prove present host state or prevent forged committed receipt content.
- Fourth cell is the existing register's receipt column; this is not a general Markdown parser. Existing r65 receipt path shape and token wrappers are preserved.
- Selftest and these targeted demonstrations were explicitly assigned and run; no whole-repository build, lint, formatter, or landing check was run. L1 owns integrated harness/landing gates.
- No LSP interface was mounted in this seat; new-file work reused directly read reference functions and did not refactor existing symbols.
- No tools installed or updated. No host/service/configuration changes. No blocker.

Self-evaluation: accuracy 4/5 (targeted evidence, not integrated landing); completeness 4/5 (all assigned drafting and targeted controls done, production integration deliberately L1-owned); clarity 4/5 (explicit frozen limits, receipt names verbose); actionability 4/5 (exact draft/hash/interface and reproducer, integration still required); conciseness 4/5 (compact production source, verbose retained evidence). Overall 4.0/5. Next parent action: integrate the sole production draft, then run the frozen shared control harness and post-integration gate.

## Post-review scope ruling

R66RevRegister independently reproduced the selftest and comparison results, and identified a citation-gap variant: a register citing only file-plane receipts still passes if the exact live receipt remains committed but unreferenced. This is intentionally accepted by the existing `unreferenced-live-receipt` selftest. Our file-plane-only control removes the live object; it does NOT demonstrate rejection of that stronger retained-tree forge.

L1 MadoR66 explicitly ruled after review: keep candidate and selftest unchanged; the declared live-receipt check is tree-level, and disclose the citation gap rather than tighten after scoring. Thus 4/4 applies only to the exact controls retained by this seat and the agreed harness construction. Candidate SHA remains unchanged.
