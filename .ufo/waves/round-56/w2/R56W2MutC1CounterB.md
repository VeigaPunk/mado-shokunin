# R56W2MutC1CounterB — mutation test of the C1 counter's parsing helpers

REV measured: `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` (counter `quality/counters/c1-r56-autoreload-entry.py`, sha256 `2b2ef41b3329edde…`). Lane tip `9c3ca28a` not used. Lane read through git objects only (`git show`, `git archive`, `rev-parse`, `ls-tree`, `cat-file`, and the counter/harness's own git calls). No lane tracked file, index or ref was written.

Axes named: (1) oracle kill rate on helper-level mutants, (2) whether each surviving non-equivalent mutant has a verified kill fixture, (3) defect severity of anything the survivors expose.

## Attacked item

Wave-1 seats wrote each artifact once; their own selftests were the only kill evidence. This seat mutates the PARSING helpers of the C1 counter (strict_row, lenient_row, registry_cells, registry_id, fence/comment handling, live_lines, first_cell, scope_covers, to_int, the four token regexes, git object access in `Repo`) and the helper-level thresholds. The `evaluate()` legs were left alone (two thresholds read inside evaluate are disclosed in `mutants.md`).

## Deliverables

Directory: `.ufo/waves/round-56/w2/R56W2MutC1CounterB/`

- `mutants.md` — full table of 71 mutants, the classification of every survivor, the 28 proposed fixtures with baseline and mutant outputs, exact mutated lines.
- `mutate.py` — the driver. Generates 71 one-line mutants of the pinned counter, runs both oracles on each, writes `results.json`.
- `diffhelpers2.py` — helper-level differential, baseline vs each survivor (`diffs2.json`).
- `fuzz_equiv.py` — random differential for the equivalence claims (200000 inputs each).
- `fixtures.py` — the 28 proposed kill fixtures plus the M69 CLI check. Each is one edit of a minimal export of the pinned tree.
- `receipts/` — `baseline-selftest.txt`, `baseline-harness.txt`, `fuzz-equiv.txt`, `mutants-results.json`, `helper-diffs.json`, `fixtures-results.json`, `frozen-quote-lengths.json`, `mutant-sha256.txt`.

Scripts reference scratch paths (`/fast/scratch/hyaku/mado-r56/R56W2MutC1CounterB/`). To reproduce, export the pinned tree first: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive 28fc86ac2359ec27406d8a2c63bef82ea6e947ed -- corpus/knowledge/hyprland-config-autoreload-r56.md corpus/SOURCES.md corpus/README.md .ufo/waves/round-56/frozen-tables-v2.json .ufo/waves/round-56/fetch | tar -x -C <scratch>/base`, then `python3 -I mutate.py <scratch>` and `python3 -I fixtures.py`.

## What I did and the commands run

1. Baseline oracles on the pinned counter (`receipts/baseline-*.txt`):

```
python3 -I baseline.py --selftest --repo <lane> --rev 28fc86ac… --work <scratch>/work/st2
  -> 242/242 assertions passed            (rc 0)
python3 -I quality/check-r56-controls.py --claim c1 --repo <lane> --rev 28fc86ac… --work <scratch>/work/ht2 --counter baseline.py
  -> MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK   (rc 0)
```

2. Mutation sweep: `python3 -I mutate.py <scratch>` — 71 one-line `str.replace` mutants (each old text asserted to occur exactly once, line count asserted unchanged, all compile). Each mutant runs `--selftest` and the unchanged harness with `--counter <mutant>`. Result:
   `TOTAL=71 KILLED=35 SURVIVED=36 ERROR=0`.

3. Helper-level differential (`diffhelpers2.py`) on each survivor, and random differential (`fuzz_equiv.py 200000`): M14 0/200000 disagreements, M44 0/200000, M26 disagrees only on the 3-character line `| |` at function level (argued unreachable; output check below), M57 quote-length check.

4. Output-level check for M26, E26: inserting `| |` and `|  |` lines in the entry and a `| |` line in the registry, baseline vs M26: `identical output: True`.

5. Fixtures (`fixtures.py`): 28 single-edit fixtures plus the M69 CLI case, each run through the baseline and the mutant with `--rev HEAD`. Result: `FIXTURES KILLED 28 / 28` (all 28 non-equivalent survivors).

## Results

| measure | value |
|---|---|
| mutants | 71 |
| KILLED by the existing oracle | 35 (49.3% of all; 55.6% of the 63 non-equivalent) |
| SURVIVED the existing oracle | 36 |
| EQUIVALENT (argued; 3 with fuzz or output checks) | 8: M14, M26, M44, M57, M63, M64, M66, M70 |
| non-equivalent survivors | 28, each killed by a verified proposed fixture (28/28) |
| non-equivalent mutants killed with existing oracle + proposed fixtures | 63/63 |

Selftest vs harness on the 35 killed: 21 killed by both, 14 by the selftest alone, **0 by the harness alone**. On helper-level mutants the independent harness adds no kill beyond the selftest.

Survivor counts for round 55 (11/24, 8/38, 4/17) are quoted from the wave brief and were not re-measured here.

### Survivors, by cause (non-equivalent; proposed fixture in brackets)

- Thresholds in the row grammar: K_MIN 39/41 [F59, F60]; ECHO_MIN 31 [F58] (harness control 11 accepts any echo leg).
- Fence and comment scanner: 4-space opener [F04]; backtick info string [F06]; 4-space closer [F08]; VT closer [F10]; `<!DOCTYPE` opens a comment [F11]; `<!-->` closed at once [F13].
- Row parse: leading tab drops the candidate [F19]; no space before final pipe [F25]; trailing space [F29].
- Registry parse: double space before a separator [F33]; tab after the id pipe [F37]; URL token swallows trailing text [F56]; `S3999` not seen by prov [F55].
- Locator scan (E3 and digit classes): `33-,` crash [F42]; covering range plus past-EOF locator [F45]; reversed past-EOF range [F46]; superscript digits crash the mutant [F48, F49]; 18-digit locator [F50, pin absent only].
- Digit runs: zero-padded 18-digit run [F51]; digit followed by a letter [F54].
- Executable blob mode [F62]; `--rev <tree oid>` [F69].

## Defects found (severity)

All findings are against the pinned counter or the harness as committed at 28fc86ac; none change the real verdict (`TARGET_MET`, 30/3/30/30/33/8) because the real entry and registry do not exercise them, checked below.

1. **Harness coverage gap: mixed past-EOF anchor (weakens the claim).** Input: S383 anchor `ConfigWatcher.cpp:33-34,46,…,105,9999` (F45). Baseline: `scope=20/30 … missed=scope:K03…K12`, verdict TARGET_MISSED. Mutant M45 (`return covered and not over` → `return covered`): `scope=30/30 TARGET_MET`. Harness control 12 uses only the lone range `1-9999`; the counter classifies a past-EOF locator as `over` (its `elif` never sets coverage: `scope_covers(…, 33, 4046)` is False for `ConfigWatcher.cpp:1-9999`), so control 12 cannot tell `covered and not over` from `covered`. The E3 "past EOF fails every row of the pin" rule is therefore untested in its mixed form. Severity: weakens the claim (the test does not guard the rule it names).
2. **Harness coverage gap: reversed past-EOF locator (weakens the claim).** Input: `…,5000-5` beside `33-34` (F46). Baseline TARGET_MISSED; mutant TARGET_MET. Same root cause as 1. Severity: weakens.
3. **Selftest coverage gap: rev is a tree oid (cosmetic).** `--rev <tree>`: baseline rc 2 `setup error: rev does not resolve to a commit`; mutant rc 0 `TARGET_MET`. Only commit revs are tested. Severity: cosmetic (the baseline is correct; no test pins it).
4. **Digit-run boundary inconsistency (cosmetic).** A proposition with the 18-digit run `000000000000000003` passes `num` (value 3 is accepted); the 19-digit form is rejected because `to_int` returns None at 19 digits. The boundary is inconsistent. Input F51. Severity: cosmetic.
5. **Digit runs glued to letters are ignored (cosmetic, latent).** `12x` in a proposition passes `num` in the baseline (lookahead `(?![A-Za-z0-9_])`), while `config7` is ignored by both versions. Input F54. Severity: cosmetic.
6. **Four-digit S-id invisible to prov (weakens prov in principle).** `source:` line with `S3999` passes prov in the baseline, because `SID_RE` requires exactly three digits and then a non-digit. The mutant reads `S399` and fails prov (F55). Real source lines contain only S383–S391. Severity: weakens prov (latent).
7. **`<!-->` opens a comment in the baseline (cosmetic for this entry).** Input F13: baseline hides K05 (`rows=29/30`); the mutant (closing at once) gives TARGET_MET. [INFERENCE, not verified against a renderer: CommonMark HTML-block type 2 ends at a line containing `-->`, which would include the opener line.] The real entry contains no `<!--` (count 0), checked. Severity: cosmetic.
8. **Invalid UTF-8 is replaced, not rejected (cosmetic, conservative).** Input F02: `33\xff-34` in the S383 anchor leaves line 34 uncovered (baseline `scope=21/30`). Fails closed. The real files decode as UTF-8 (checked). Severity: cosmetic.
9. **CRLF entries fail every row (cosmetic, conservative).** Input F03: `rows=0/30`. Per the grammar (no trailing byte) this is the intended result. Severity: cosmetic.

No defect was found that changes the real `TARGET_MET` verdict. The baseline did not crash on any input in the fixture set; crashes appear only in mutants.

## What could not be verified / limits

- Equivalence is argued and fuzzed, not proven. Fuzz covered M14, M44 and M26 (function level) and M57 (quote-length table check). M63, M64, M66, M70 rest on git object-format and path-constant arguments (checked against the frozen pin names and paths), not on fuzzing.
- The 71 mutants are one-line helper edits, not the full mutation space. `ECHO_MIN`, `K_MIN` and `NEW_ROWS_DENOM` are read inside `evaluate()`; M57–M61 touch those legs (disclosed in `mutants.md`).
- The fixtures are proposed additions, not edits to `quality/r56_ctl_c1.py` (not in scope). Each was verified by running the mutant and the baseline on the fixture; none was run through the harness as a control. F50 deletes a pin file and is therefore the least minimal fixture (it is the only way to make `nlines` None).
- The CommonMark/HTML5 comparison in defect 7 was not checked against a renderer.
- The round-55 survivor counts were not re-measured.
- Lane mtime observation (not attributed): a `find -newer` scan after the run listed `corpus/knowledge/hyprland-config-autoreload-r56.md`, `corpus/SOURCES.md`, `.git` and several sibling `w2/` directories as newer than this seat's first scratch file. This seat issued no write to any of them: all lane access was git plumbing (`show`, `archive`, `rev-parse`, `ls-tree`, `cat-file`), and the counter and harness write only under `--work` (scratch). I did not run `git status`, which can refresh the index.

## Tooling

No tool installed or upgraded. Python 3.14 stdlib and git (already present) only. No pacman transaction, no network, no `~/.local/bin` write.

## Scratch and cleanup

Scratch `/fast/scratch/hyaku/mado-r56/R56W2MutC1CounterB/` (mutants, fixtures, work dirs, baseline copy) is removed after the receipts were copied into the deliverable directory. The deliverable carries `receipts/mutant-sha256.txt` for every mutant file, so the mutants can be regenerated and checked.

VERDICT: 71 mutants, 35 killed by the existing oracle (49.3%); 8 equivalent; 28 non-equivalent survivors, each killed by a verified proposed fixture (28/28). Two harness coverage gaps (defects 1 and 2) weaken the C1 test suite; no defect changes the real verdict.
