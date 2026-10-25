# MutC2Tool — mutation probe: `tools/mado-options.py` fixture coverage (round-39 w1)

Claim context: C2 operability (`PRED-C3-r39-v1`). Question probed: do the tool's own
fixtures (its `--selftest`, 69 assertions) catch broken resolution? Method: single-point
mutations in an isolated sandbox copy (`/tmp/mutc2-tool/mado-options.py`, copied from the
lane tip bytes), same bounded detector on pristine → mutated → restored bytes.

Lane file `tools/mado-options.py` was never modified: final `diff -q` vs sandbox →
`IDENTICAL`; sandbox restored hash equals pristine hash after every mutant.

## Detector and baseline

- Detector: `python3 -I /tmp/mutc2-tool/mado-options.py --selftest` (the counter's clause-b
  detector: hermetic fixtures, child runs a copy of the script itself).
- Pristine baseline: `MADO_OPTIONS_SELFTEST: 69/69 passed`, exit 0 — detector conclusive
  (not inconclusive), so every red below is a genuine kill.
- Pristine sha256: `cee78d99de2e3420572aa028f439240ac12e5eb6d595de75e2fc62e5ea9ce61e`
  (identical for lane file and sandbox copy before/after each cycle).

## Mutants

| # | Single-point mutation (site) | Defect class | Result | Verdict |
|---|---|---|---|---|
| M1 | `State.declare`: `layer_of(path, home)` → `layer_of(os.path.dirname(path), home)` (line 262) | owner resolution picks wrong layer | `64/69`, RC=1; FAILs: gaps_out layer toggles, kb_layout layer user, rounding layer ai-usage, root option layer root, theme layer | **killed** |
| M2 | `layer_of` toggles branch: `return "toggles"` → `return "defaults"` (line 229) | toggle layer ignored | `68/69`, RC=1; FAIL: gaps_out layer toggles | **killed** |
| M3 | `parse_line` comment loop: `else: line = line[:pos]; break` → `else: break` (line 349) | comment tokens parsed as settings | `68/69`, RC=1; FAIL: trailing comment dropped (`col.inactive_border` value gained ` # trailing comment dropped`) | **killed** |
| M4 | `parse_line`: escape test → `if False and pos + 1 < len(line) and line[pos+1] == "#":` (line 344) | `##` escapes mishandled | `68/69`, RC=1; FAIL: `## escape: value #000000` (`decoration:shadow:color` declared empty) | **killed** |

Survived: none. Coverage finding: none — each targeted resolution defect (ownership layer,
toggle labeling, comment-token bleed, `##` escape pass) is caught by ≥1 named assertion,
and each kill is precisely the targeted behavior (M1 kills 5 layer assertions; M2–M4 kill
exactly one each), i.e. the fixtures are not passing for incidental reasons.

## Red receipts and restoration evidence

- Receipts: `.ufo/waves/round-39/w1/MutC2Tool/m{1,2,3,4}-red.txt` (command, output, exit
  code, mutant sha256, verdict).
- Mutant sha256s: M1 `dc6bf92e611fdf01f4b51b2323b4250bcdc5b0ec93b8875182b41ff68697e311`;
  M2 `03714474f4b286e8cf674d5f3f24c186c369ef5d7d9d67eab95fa4989c481dc5`;
  M3 `f3d2c4bf4c6a18fae19da0831f1fcd0bc8179ec780803e15c789e3e553c82e1a`;
  M4 `4c915273f1497438e30ae3d3f6c1ab00f29d736abad3716a3e44e03a8f95f7a3`.
- After each revert: selftest `69/69 passed` RC=0 and sandbox sha256 back to
  `cee78d99de2e3420572aa028f439240ac12e5eb6d595de75e2fc62e5ea9ce61e`; final
  `diff -q` lane↔sandbox: identical.

## Scope and safety

- Writes: this report + 4 receipts under `.ufo/waves/round-39/w1/MutC2Tool/` only; sandbox
  and receipts also staged under `/tmp/mutc2-tool/`. No tracked lane file touched; no
  git/jj mutation; no installs (stdlib python3 only); no pacman, sockets, or host config
  writes. No subagents/background jobs.
