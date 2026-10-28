# R55W2MutTool3 — round 55 wave w2 (falsify): mutation test of the C2 tool

Seat: R55W2MutTool3 (leaf member, no subagents). Deliverable: `.ufo/waves/round-55/w2/R55W2MutTool3/mutants.md` with receipts under `.ufo/waves/round-55/w2/R55W2MutTool3/mutants/`.
Target: `tools/mado-kbdopts.py`, scored revision 57584ed67716340b3d466fa04333ac0bab3fb79e (blob sha256 `9c69dd62…c2`, equal to the lane worktree before and after).
Focus: the structural parser (stack push/pop, `}` underflow, current-device lifetime, name-line handling, key-before-name, nested blocks, `device[` bracket forms, per-file reset, ignored `$` and `source` LHS).

## What ran

- Export (read-only): `git -C <lane> archive 57584ed… tools/mado-kbdopts.py .ufo/waves/round-55/fixtures .ufo/waves/round-55/fetch` into scratch; also `quality .ufo/waves/round-55 tools` for the frozen harness.
- Baseline: unmodified tool, 26 fixtures via `python3 -I` with cwd = scratch root and `args.json` argv, stdout bytes and rc compared to `expected.out`/`expected.rc`: **26/26**; `--selftest`: **83/83**, rc 0.
- 21 one-edit mutants generated in scratch copies (`receipts/gen.py`, each substring asserted to occur exactly once). The lane was never written; no lane file was modified, staged, committed or restored.
- Per mutant: 26 fixtures + own `--selftest` (`receipts/drive.py`). Table in `mutants.md`.
- Differential fuzz original-vs-mutant, in-process, 200 000 random configs (`receipts/fuzz.py`, seed 5521), to check the equivalence claims and find extra kills.
- Hand-derived kill configs for the 13 non-equivalent fixture survivors (`receipts/kills.py`), each run against original and mutant (`receipts/repro.py`: 13/13 killed, original matches the hand-derived contract output in 13/13).
- Frozen harness run on each mutant: `python3 -I quality/check-r55-controls.py --claim c2 --repo <D> --rev <commit> --work <W>` on a scratch repo `<D>` (`git init`, `rev-parse --show-toplevel` asserted equal to `<D>`, lane tree at 57584ed archived in, one commit per mutant with `-c user.name=ctl -c user.email=ctl@ctl`). Verified that each harness `--rev` carries the intended mutant blob (`git show <rev>:tools/mado-kbdopts.py | sha256sum`).
- Host: no hyprctl, no config reads, no network reads (not needed for a source-level parser probe).
- Tooling: no tool installed or upgraded. Only `python3` stdlib (`-I`), `git`, `tar`, `sha256sum`, `diff`. Read `/home/vgpnk/.omp/agent/RULES.md` (tooling directive). No pacman use.

## What did not run

- No real Hyprland check of any mutated clause; the contract text (registration.md §C2 v1 and registration-v2.md E7) is the only oracle. Hyprland source was not re-opened for these clauses this round.
- No subagent, no background job.
- I did not run the lane's own `quality/check-r55-controls.py` against the lane revision itself as part of this seat (that is the L1's job); I ran it only on the scratch commits to score mutants. The pristine scratch run reproduces `TARGET_MET` (18/18, 8/8, holdout ok, controls 3/3) on a commit whose tool blob equals the lane's.

## Results

Verdicts per target:

| target | verdict | evidence |
|---|---|---|
| T1. `tools/mado-kbdopts.py` @57584ed, structural parser vs the contract text | **SURVIVES** | The 13 hand-derived contract probes (K-M01..K-M18) all match the original byte-for-byte: `receipts/repro-output.txt`, `repro-results.json` (`status=ORIG_MATCHES_HAND_EXPECTED`). Original 26/26 fixtures and selftest 83/83. No contract clause was violated by the original in any probe. |
| T2. PRED-C2-r55 as a discriminator of the structural clauses (fixture gate) | **BROKEN** as a discriminator (does not falsify the frozen sentence) | Frozen harness prints `TARGET_MET` for 13 mutants that violate v1 §C2 text: M01, M02, M03, M05, M06, M08, M11, M12, M13, M14, M15, M16, M18 (`receipts/harness/M*.out`, `commit-map.txt`). The committed 18 fixtures kill only M10, M20, M21 of 21. |
| T3. Hold-out sufficiency for the structural clauses | **SURVIVES** (hold-out carries weight) | H01 kills M07 (key-before-name), H02 kills M04 (`}` clears stack) and M09 (nested device keys). Without the hold-out these three pass the gate. |
| T4. Equivalence of M17 (`source` LHS) and M19 (bracket check in unsupported test) | **NOT-REPRODUCED as kills**; equivalent by argument, fuzz 0/200 000 | No config can kill them; proof in `mutants.md` "Equivalent mutants"; `receipts/fuzz-results.json`. |
| T5. M18 (`$` LHS not ignored) — the equivalence I first assumed | **BROKEN** (non-equivalent) | LHS may contain `:`, so `device[a] {` + `$x:repeat_rate = 3` yields a bracket KEY. Original `unsupported=0`, mutant `unsupported=1`; fuzz 1820/200 000. Harness `TARGET_MET`. |
| T6. M01 stray `}` on empty stack (crash) | **UNVERIFIED** against the contract | Mutant crashes (`IndexError`, rc 1). The contract is silent on `}` with an empty stack; the original's no-op is the tool's documented choice, not a contract clause. Recorded as a crash-robustness probe, not a contract violation. |

Survivors of the fixture gate (passes all 26), with kill configs in `mutants.md` and `mutants/<ID>/kill/`:
M01, M02, M03, M05, M06, M08, M11, M12, M13, M14, M15, M16, M18 (non-equivalent, 13) and M17, M19 (equivalent, no kill). Seven of the 13 also pass their own selftest: M08, M11, M12, M13, M14, M16, M18.

Decisive outputs (exact):
- Original, K-M02 (`device {\nname = a\n}\ndevice {\nrepeat_rate = 50\n}\n`, `--keyboard a`): `MADO_KBDOPT: keyboard=a repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=1`; mutant (`if False:`): `… repeat_rate=50 … from=D/-/- unsupported=0`.
- Original, K-M18 (`device[a] {\n$x:repeat_rate = 3\n}\n`): `… from=-/-/- unsupported=0`; mutant: `… unsupported=1`.
- Harness on the M02 commit (`1e75918e…`): `MADO_R55_C2: rev=1e75918e… fixtures=18/18 holdout=8/8 holdout_commit=ok controls=3/3 verdict=TARGET_MET`.

## Recommendation (for the L1; not applied)

Add committed or hold-out fixtures pinning the 13 survivor clauses (the kill texts in `mutants.md` are the candidates: per-file stack/device reset, nested-name ignore, comment-line skip, `rsplit` vs first `=`, `}x` non-pop, bracket depth-2 KEY, `$` in RHS, FF strip, and `$`-LHS with `:`). Decide the stray-`}`-at-empty-stack behaviour explicitly in the contract (M01) rather than by tool choice. No lane file was changed by this seat; the L1 decides.

## Hand-off notes

- Receipts in the deliverable: `mutants/receipts/` holds the generator, driver, kill specs, repro, fuzz, harness outputs, commit map and score JSON. `drive.py` and `gen.py` hard-code the scratch root; `repro.py` and `fuzz.py` take the mutants directory as an argument.
- Scratch `/fast/scratch/hyaku/mado-r55/R55W2MutTool3/` (exports, mutant copies, scratch repo) is removed before yield.
- Lane integrity: `sha256sum` of the lane worktree `tools/mado-kbdopts.py` = blob at 57584ed = `9c69dd62…c2`, before and after.
