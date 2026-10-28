# R55W2CritToolDiff — differential test of tools/mado-kbdopts.py against an independent oracle

Seat: R55W2CritToolDiff (leaf, no subagents). Round 55 wave w2, falsify. Scope: the C2 instrument
(`tools/mado-kbdopts.py`) under `registration.md` §C2 as amended by `registration-v2.md` E7.
Deliverable: `.ufo/waves/round-55/w2/R55W2CritToolDiff/diff.md` (divergence list, classification, appendices with the
generator, oracle and directed battery) plus receipts in the same directory.

## What I did

1. Wrote an oracle (`oracle.py`) from the contract text alone, before opening the tool. I never opened
   `tools/mado-kbdopts.py` in this seat. Every verdict below is black-box against the tool's stdout and exit code.
   I read `.ufo/waves/round-46/fetch/hyprlang-config.cpp` (lines 185–271) only to confirm that the bool prefixes are
   case-sensitive and that the decimal rule is a full-match; the contract is the authority, the pin confirmed it.
2. Wrote a seeded generator (`gen_diff.py`) covering: nested blocks, device blocks with and without names, bracket
   forms, repeated and merged blocks, comments, `##`, `$`, `{{`, backslashes, signs, hex, huge digit runs (up to 9000
   digits), CRLF and lone CR, blank and brace-only lines, BOM, NBSP, 0x1C, invalid UTF-8 bytes, getoption files with
   duplicate keys, odd JSON, NaN/Infinity, empty and whitespace-only lines, and usage/setup argv shapes.
3. Ran oracle and tool on every input in a private per-case directory (`python3 -I`, cwd = that directory, identical
   relative argv), comparing stdout bytes and exit code exactly. Each divergence was minimised (argv tokens, then
   lines, then bytes) while it persisted.
4. Probed the divergences, the contract's ambiguous points, and the JSON and usage edges directly.
5. Checked that the comparator is not blind: eight deliberately mutated oracles (copies in scratch) all diverge.

## Commands (exact, from the seat)

```
python3 -I gen_diff.py --seed 55 --n 3400 --workers 8 --mode clean --profile adv   --out <scratch>/final-clean-adv
python3 -I gen_diff.py --seed 56 --n 1200 --workers 8 --mode clean --profile valid --out <scratch>/final-clean-valid
python3 -I gen_diff.py --seed 57 --n 1000 --workers 8 --mode ambig --profile adv   --out <scratch>/final-ambig-adv
python3 -I directed_battery.py            # 70/71 agree, output in directed-battery-output.txt
ORACLE_MOD=oracle_m<k> python3 -I gen_diff.py --seed 55 --n 3400 --mode clean --profile adv --no-min --out <scratch>/mut-<k>
python3 -I build_diff_md.py
```
Tool under test: `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-kbdopts.py ...`. Python 3.14.8.

## Decisive output

```
final-clean-adv    STATS total=3443 edge=43 random=3400 oracle_setup=563 divergent=29 tool_timeouts=0
final-clean-valid  STATS total=1243 edge=43 random=1200 oracle_setup=199 divergent=11 tool_timeouts=0
final-ambig-adv    STATS total=1043 edge=43 random=1000 oracle_setup=270 divergent=145 tool_timeouts=0
  classes: final-clean-adv {GO-WS-ONLY 3, CTL-NAME 2, GO-FF-STRIP 24}; final-clean-valid {GO-WS-ONLY 3, CTL-NAME 2, GO-FF-STRIP 6};
           final-ambig-adv {GO-WS-ONLY 74, CTL-NAME 56, GO-FF-STRIP 15}; OTHER = 0 in all three runs
directed_battery.py: DIRECTED agree=70 diverge=1   (the one: J17, VT after a JSON object — GO-FF-STRIP class)
```
Coverage (oracle side) shows the grammar was reached, not only defaults: clean-valid has 122 device-scoped outputs
(`from=D`), 329 global (`from=G`), 840 with `unsupported>0`, 122 numlock=1, and 153/400/20 live DIFFER/UNKNOWN/AGREE.
Clean-adv has 12 device-scoped outputs, which is low; the valid profile is the one that exercises device semantics.

Sensitivity (comparator is not blind, `--no-min`, clean-adv 3400 inputs): m1 prefix-digits `30abc`→30: 236 divergent;
m2 case-insensitive bools: 58; m3 Python `str.strip()`: 98; m4 numlock 0..2: 30; m5 bracket key silently ignored: 964;
m6 bool accepted as getoption int: 104; m7 `splitlines()`: 1088; m8 device value without current device: 78.
Unmutated: 29. These mutant copies were built before the big-int fix described below; the fix only touches
getoption integers with more than 4300 digits, which those inputs do not contain.

## Verdicts per target

**T1. C2 config grammar** (line classification, stack and KEY rule incl. E7, device blocks and merges, `name` cut at `#`,
value parse incl. bool prefixes and full-match decimal, ranges, `unsupported` counting order, `from` letters, output
and DONE grammar): **SURVIVES** against this oracle. Zero config-grammar divergences in the 4,600 random clean-mode inputs (adv and valid
profiles; the 40 divergences in those 4,600 are all getoption-strip or CTL-NAME, none is config-grammar) and 53 of 53 directed config points agree. Evidence: `run-stats.json`,
`directed-battery-output.txt`. The verdict is against the one oracle written here, not against the frozen fixtures.
Points where two readings are defensible and both agree are listed in `diff.md` under "Directed battery"
(e.g. `$`/`##` inside a comment, `*` device name vs wildcard, BOM/NBSP before a key). Those are the places the contract
itself must be settled by the L1; no differential test can settle them.

**T2. `--keyboard NAME` containing ASCII control characters** (TAB, LF, VT, FF, CR, 0x01, 0x1C, 0x7F): **BROKEN**
(TOOL BUG). Contract: `--keyboard NAME` is one argv token after the flag; “anything else is usage” constrains argument
shape, not NAME's characters. The tool answers `SETUP usage`, rc 2. Config side, with real bytes
(`ctlname-probe.txt`): a device `name = a<TAB>b` with `repeat_rate = 7` is answered by the oracle
(`keyboard=a\tb repeat_rate=7 ... from=D/-/-`, rc 0) and rejected by the tool (`SETUP usage`, rc 2), so such a device
cannot be queried. A VT name is rejected the same way. NBSP (U+00A0) and U+2028 are accepted. Occurrences: 2 + 2 + 56
argv-side in the three runs (the ambiguity run's 56 are the same class), minimised in `diff.md` D-entries.
Defensible alternative reading (the only one that makes the tool right): NAME must be printable. The contract does
not say that. I could not find text that supports it.

**T3. getoption line handling** (form feed/VT after a JSON object; whitespace-only lines): **UNVERIFIED as a defect;
CONTRACT AMBIGUITY.** Reading A (oracle): the raw line is the unit; “non-empty” means zero bytes; the JSON is strict
RFC 8259 (FF and VT are not whitespace), so `{...}\x0c` and a line of spaces are `bad_json`. Reading B (tool): the
contract's strip set (space, tab, CR, LF, VT, FF) applies to every getoption line before the empty test and the JSON
parse, so `{...}\x0b` parses and whitespace-only lines are skipped. The strip rule is stated only for config lines,
and “non-empty `--getoption` line” is undefined. Occurrences: GO-FF-STRIP 45, GO-WS-ONLY 80 across the three runs.
Consistent with reading B: `\x1c` (outside the strip set) is rejected by the tool (directed J18 agrees with the
oracle). The L1 must decide which reading is the contract. Until then the tool is not falsified.

**T4. Usage, setup and file classes** (usage shapes incl. `--config=PATH`, missing value, repeated `--getoption`,
unknown flags; `unreadable` for missing, directory, FIFO, symlink-to-dir; `too_large` at 1048577 bytes; exact 1048576
readable; `bad_json` for non-object lines; empty and missing getoption; setup precedence): **SURVIVES.** No divergence
in E01–E27, E30, E32–E40 (E28, E29, E31 are the T3 class; E41, E43 are the T2 argv cases). FIFO returns `unreadable` without blocking (no timeout in 3 runs). The
`--config --keyboard` shape reads a file named `--keyboard` (two-token form taken literally), agreeing with the oracle.

**T5. Robustness** (5000–20000-digit values, 200000-deep JSON nesting, 9×5000-digit config value, lone-CR file):
**SURVIVES.** No crashes, no tracebacks, no timeouts in any run. 200000-deep nesting gives `SETUP bad_json` rc 2 in both
(implementation limit; the contract does not cover valid deep objects). Lone CR splits nothing (A17 agrees).

**Not a tool verdict: ORACLE BUG (mine, fixed).** The first oracle called `json.loads` under Python 3.11+'s 4300-digit
int↔str cap, so a 4301+-digit getoption integer became `bad_json`. The tool printed the full integer and verdict
DIFFER/AGREE correctly. Fixed with `sys.set_int_max_str_digits(0)`; the 4301, 5000 and 20000-digit cases then agree
byte-for-byte. No effect on the three final runs (none has such an integer) except the directed battery.

## Seat-internal construction error (corrected)

My deterministic edge cases E41 and E43 were meant to put a real TAB and VT into a device name. The heredoc wrote them as
literal backslash text, so they tested the argv side only. The real-byte config probe above is the correct test and is
the basis for T2. The argv-side CTL-NAME divergences in the random runs are real, and they are unaffected.

## Could not verify / out of scope

- The fixtures `fixtures/c2` (18) and `fixtures/c2-holdout` (8) were not run by this seat. Their names were visible in a
  directory listing of `fixtures/c2-holdout/` (H01–H08). I did not open their contents and did not use them as inputs.
- `--selftest` is informational under the contract and not part of PRED-C2; not tested.
- Symlink semantics beyond "follows to a regular file" (E17) and "to a directory" (E18) are not tested.
- The contract's ambiguous readings (T3, and the directed-battery list) cannot be settled from the contract text; I
  report both readings and the tool's observed reading, and I do not pick a winner.
- The oracle is a second reading by one author. Agreement shows the tool implements that reading, not that the reading
  is the frozen contract. Two readings coincide in the oracle and the tool on several points, and I list them.

## Tooling and host

- No tool installed or upgraded. Python 3.14.8 was already present; `python3 -I` used throughout. No pacman, no `uv`, no
  network fetch. (Per RULES.md the install record is "none".)
- Host: no `hyprctl` call and no host read in this seat (not needed for C2 differential testing).
- Lane: writes only inside `.ufo/waves/round-55/w2/` (this report and `R55W2CritToolDiff/`). No tracked-file edit, no
  git/jj mutation, no commit. Mutation tests ran on copies in scratch; the lane was never touched by them.
- Scratch `/fast/scratch/hyaku/mado-r55/R55W2CritToolDiff/` (case directories, mutant oracles, runs) removed before
  yielding; every receipt needed to reproduce the results is in the deliverable directory.

## Receipts (`.ufo/waves/round-55/w2/R55W2CritToolDiff/`)

`diff.md` (divergence list, classification, directed battery, coverage, sensitivity, appendices A–C with the full
source), `gen_diff.py`, `oracle.py`, `directed_battery.py`, `directed-battery-output.txt`, `ctlname-probe.txt`,
`run-stats.json`, `final-clean-adv-minimised.json`, `final-clean-valid-minimised.json`, `final-ambig-adv-minimised.json`.

## Summary for L1

- T1 C2 config grammar: SURVIVES (no config-grammar divergence in 4,600 random clean inputs and 53 directed config points
  against an independent oracle; comparator shown sensitive by 8/8 mutants).
- T2 keyboard NAME with control characters: BROKEN, TOOL BUG (a device named with an internal TAB or VT in config can
  never be queried; tool prints `SETUP usage`).
- T3 getoption FF/VT and whitespace-only lines: CONTRACT AMBIGUITY, verdict UNVERIFIED as a defect. Settle the strip rule
  for getoption lines in the contract, then re-run `gen_diff.py --mode ambig`.
- T4 usage, setup and file classes: SURVIVES.
- T5 robustness: SURVIVES.
