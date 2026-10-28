# R55W2MutTool4 — wave w2 (falsify), C2 mutation test

Seat: R55W2MutTool4 (mutation tester, leaf, no subagents). Scope: `tools/mado-kbdopts.py` at `57584ed67716340b3d466fa04333ac0bab3fb79e`, focus = argument parsing, setup reasons and exit codes, the `--getoption` join (AGREE/DIFFER/UNKNOWN, DONE summary, last-line-wins, boolean/float `int` rejection, NaN and invalid JSON, blank lines), output formatting, keyboard order and repeat. Full table, survivor inputs and outputs: `w2/R55W2MutTool4/mutants.md`.

## What ran

- Exported the tool and `fixtures/` + `fetch/` with `git archive` into scratch. No lane, fleet, sibling or shokuknow write.
- Unmodified tool: 26/26 fixtures match `expected.out`/`expected.rc` (18 committed, 8 hold-out) and `--selftest` gives `83/83` (`results/ORIG.txt`).
- 25 one-line mutants, each made with the `edit` tool on a COPY in scratch (`diffs/`, `src/`). The lane was not touched; nothing was restored in the lane because nothing was changed in it.
- Harness `bin/harness.sh`: per mutant, a private run dir with copies of the fixtures and the tool, `python3 -I tool.py <args.json argv>` with cwd = that dir, stdout bytes and rc compared; then `--selftest`. Output `results/mutants.txt`.
- Survivor repro `bin/repro.sh`: each survivor's minimal input under the original and the mutant, plus a parser-compatible control per survivor (must match). Output `results/repro.txt`.
- Python 3.14.8, `python3 -I`. No hyprctl, no network, no subagents.

## Results

- 9 of 25 mutants fail a fixture (M03, M07, M08, M15, M19, M22, M23, M24, M25).
- 16 of 25 pass all 26 fixtures: M01, M02, M04, M05, M06, M09, M10, M11, M12, M13, M14, M16, M17, M18, M20, M21.
- Of those 16, 12 are caught by the tool's own selftest. 4 pass both: M04 (DEL in NAME), M06 (VT in the stripped set), M17 (`too_large` at exactly 1048576 bytes), M18 (`too_large` reported as `unreadable`).
- PRED-C2-r55 does not count selftest (registration.md §C2: "`--selftest` alone is informational"). So the gate would accept the 16 survivors.

## Verdicts

| target | verdict | evidence |
|---|---|---|
| Unmodified tool passes the 26 committed and hold-out fixtures and its selftest | SURVIVES (reproduced: 26/26; selftest 83/83, not the "82" in registration-v2 prose) | `results/ORIG.txt`, `results/mutants.txt` |
| Shipped tool departs from the frozen C2 text on any survivor input | NOT-REPRODUCED. On all 16 survivor inputs the unchanged tool prints what the frozen text requires; where the text is silent or ambiguous (M04, M13, M14) the note is recorded, not counted as a departure | `results/repro.txt`, `orig` rows |
| The 26 fixtures distinguish a contract-conformant tool from the 16 focus defects (evidence relied on by PRED-C2-r55) | BROKEN as evidence: 16/25 defective variants pass all 26 fixtures; 4 pass selftest too | `mutants.md` table, `results/mutants.txt` |

Survivor inputs, one line each (full output in `mutants.md`):
- M01 argv `--config r30.conf --keyboard` → orig `SETUP usage` rc 2; mutant `IndexError`, rc 1.
- M02 argv with two `--getoption` → orig `SETUP usage` rc 2; mutant rc 0, live DIFFER.
- M04 argv `--keyboard $'kbd\x7fx'` → orig `SETUP usage` rc 2; mutant prints the DEL in keyboard NAME, rc 0.
- M05 `input:repeat_rate = 201` → orig rate 25, unsupported 1; mutant rate 201, unsupported 0.
- M06 VT byte before `input:repeat_rate = 30` → orig rate 30; mutant rate 25 (line not recognised).
- M09 device block, then a second `device {` with `repeat_rate = 50` → orig 25 unsupported 1; mutant 50 from D.
- M10 config rate 40, live 41 plus unknowns → orig DONE live DIFFER; mutant DONE live UNKNOWN.
- M11 getoption `"int":"x"` → orig UNKNOWN; mutant DIFFER with live=x.
- M12 getoption numlock `"int":true` → orig UNKNOWN; mutant DIFFER with live=True.
- M13 getoption `"int":40.0` → orig UNKNOWN; mutant AGREE with live=40.0 (contract-ambiguous).
- M14 getoption `{"nothing": NaN}` → orig `SETUP bad_json` rc 2; mutant rc 0.
- M16 getoption `[1]` → orig `SETUP bad_json` rc 2; mutant rc 0.
- M17 config of exactly 1048576 bytes → orig rc 0; mutant `SETUP too_large` rc 2.
- M18 config of 1048577 bytes → orig `SETUP too_large`; mutant `SETUP unreadable`, both rc 2.
- M20 device `name = kbd-a # my kbd` → orig rate 50 from D; mutant rate 25 from -.
- M21 global rate 30, device rate 50, live 50 → orig config=30 DIFFER; mutant config=50 AGREE.

## Observations on the frozen text (not counted as falsifications)

- O1: the NAME control-byte usage rule (below 0x20 or 0x7f) is in the tool's docstring and code comment only; registration.md §C2 and registration-v2 E7 do not state it. Its 0x7f branch has no test (M04).
- O2: "an integer (not boolean)" does not define JSON `40.0` (M13).
- O3: the frozen text says "non-empty `--getoption` line"; the tool treats whitespace-only lines as blank.
- O4: the frozen text does not say whether NaN/Infinity are JSON; the tool rejects them (M14).
- O5: registration-v2 prose says 82 selftest assertions; shipped selftest has 83.

## Not verified / limits

- Not run: the L1 harness `MADO_R55_C2`, `freeze-verify*.py`, the hold-out commitment hash, and any Hyprland/hyprctl read. These were outside the focus.
- Mutant set is 25 one-line edits in the focus list, not an exhaustive operator set. 16 survivors is a lower bound.
- Fixture expected outputs were taken as given; they match the unmodified tool.
- Only Python 3.14.8 was used.

## Tooling and lane discipline

- No tools installed or upgraded; no pacman, no `~/.local/bin` writes, no host changes.
- No git/jj mutations, no commits, no fleet or sibling writes. Only `.ufo/waves/round-55/w2/R55W2MutTool4.md` and `.ufo/waves/round-55/w2/R55W2MutTool4/` were written in the lane.
- Scratch `/fast/scratch/hyaku/mado-r55/R55W2MutTool4/` was removed before yield after copying receipts.

## Receipts (under `w2/R55W2MutTool4/mutants/`)

- `mutants/diffs/M01..M25.diff`, `mutants/src/M01..M25.py`
- `mutants/bin/harness.sh`, `mutants/bin/repro.sh` (paths inside point at the scratch tree; the scripts are self-contained otherwise)
- `mutants/results/mutants.txt`, `ORIG.txt`, `repro.txt`, `selftest-fails.txt`, `orig.sha256` (tool sha256 `9c69dd62…c837c2e`), `fixtures.sha256`
