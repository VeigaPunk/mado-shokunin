# R55W2MutTool2 — C2 mutation test: value parsing, ranges, comments, detection

Target: `tools/mado-kbdopts.py` at lane rev `57584ed67716340b3d466fa04333ac0bab3fb79e`.
Original sha256 `9c69dd62c1737d4842a4a0e73db3f8317eda71ee103e71ad3cda11a19c837c2e`, identical to the rev blob (`git show <rev>:tools/mado-kbdopts.py | sha256sum`).

## Setup (what ran)

- Export: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive 57584ed67716340b3d466fa04333ac0bab3fb79e tools/mado-kbdopts.py .ufo/waves/round-55/fixtures .ufo/waves/round-55/fetch | tar -x -C /fast/scratch/hyaku/mado-r55/R55W2MutTool2`. No git command was run against the lane after this. The scratch export was removed after the receipts were copied here.
- Interpreter: system `python3 -I`, Python 3.14.8, `sys.get_int_max_str_digits()` = 4300. No tools were installed.
- Fixtures: 26 = `fixtures/c2/F01..F18` (committed) + `fixtures/c2-holdout/H01..H08`. Each runs as `python3 -I <tool> <args from args.json>` with cwd = the scratch root. Stdout bytes and rc are compared to `expected.out` / `expected.rc`.
- Hold-out integrity (read-only check): sha256 over `<relpath>\0<sha256 bytes>\n` for the 33 regular files under `fixtures/c2-holdout` (sorted UTF-8 relpath) = `1275d7f804c887c1109e3c9e0c4cc590c162399660301da5fa4196c05a92c549`. This equals `c2.holdout_commit_sha256` in `frozen-tables-v2.json`, so the hold-out commitment is intact.
- Selftest: each mutant runs `--selftest`. A mutant is "selftest-killed" if the line is not `X/X assertions passed` with rc 0. The original passes `MADO_KBDOPT_SELFTEST: 83/83` (the v2 preamble cites 82; the tool at this rev has 83 cases, recorded here as a minor discrepancy, not a contract item).
- Mutants: 26 one-edit copies made by `mkmut.py`. Each replaces one exact span that must occur exactly once in the source, and writes a copy under `mutants/`. **The lane was not touched. Mutants are copies in the seat deliverable directory only.** The control `M00-original.py` is the unmodified tool.
- Receipts: `mutants/scores.json` (per-mutant fixture kills, selftest output, mutant sha256), `mutants/repro-results.json` (per kill input: contract stdout, original stdout, every mutant's rc and stdout head), `mutants/equiv.py` output.

## 1. Mutant table

"Fixtures killed" is the set of fixture ids whose stdout or rc differs from expected. "Survivor" means the mutant passes all 26 fixtures.

| mutant | edit | fixtures killed (ids) | selftest killed? | survivor (of 26)? | kill input(s) |
|---|---|---|---|---|---|
| M01 | drop `yes` from `startswith(("true","on","yes"))` | - | yes (`yes prefix (word start)`) | **yes** | K01 |
| M02 | case-fold the true/on/yes test (`rhs.lower()`) | - | no | **yes** | K02 |
| M03 | digit class `[0-9]+` -> `\d+` (Unicode Nd digits) | - | no | **yes** | K03 |
| M04 | `[0-9]+` -> `[0-9]*` (empty value accepted as 0) | - | yes (`empty value unsupported`) | **yes** | K04 |
| M05 | `fullmatch` -> `match` (prefix digits accepted) | H07 (rc 1 traceback on `0x10`) | yes | no | - |
| M06 | leading zeros not stripped before the 6-digit test (`digits = rhs`) | - | no | **yes** | K05 |
| M07 | `int(digits or "0")` -> `int(digits)` (`0` crashes) | - | yes (`digit one`/`rate bounds`) | **yes** | K06 |
| M08 | over-cap digit run returns `0` instead of `10**6` | - | yes (`huge digit run`) | **yes** | K07 |
| M09 | cap `len(digits) <= 6` -> `<= 4` | - | no | **yes, EQUIVALENT** | none exists (see §4) |
| M10 | `repeat_rate` maximum 200 -> 201 | - | yes (`rate 201 out of range`) | **yes** | K18 |
| M11 | `repeat_delay` maximum 2000 -> 2001 | - | yes (`delay 2001 out of range`) | **yes** | K19 |
| M12 | `numlock_by_default` maximum 1 -> 2 | F18 | yes | no | - |
| M13 | range test `>` -> `>=` | F02,F05,F08,F11,F18,H03 | yes | no | - |
| M14 | drop the `##` rule | F12 | yes (`## unsupported`) | no | - |
| M15 | value comment cut at LAST `#` (`rsplit`) | - | no | **yes** | K08 |
| M16 | `$` detection narrowed to `${` | - | yes (`$ in a trailing comment`) | **yes** | K09 |
| M17 | drop the backslash check | - | no | **yes** | K10 |
| M18 | drop the `{{` check | - | no | **yes** | K11 |
| M19 | drop the full-line `#` skip | - | no | **yes** | K12 |
| M20 | device name not comment-cut | - | yes (`device name cut at comment`) | **yes** | K13 |
| M21 | form feed removed from `WS` (not stripped) | - | no | **yes** | K14 |
| M22 | value strip narrowed to spaces (`strip(" ")`) | - | no | **yes** | K15 |
| M23 | JSON bool accepted as integer live value | - | yes (`live boolean int ignored`) | **yes** | K16 |
| M24 | remove `sys.set_int_max_str_digits(0)` | - | yes (`huge live int prints without crash`) | **yes** | K17 |
| M25 | `repeat_rate` maximum 200 -> 199 | F18 | yes | no | - |
| M26 | `repeat_delay` maximum 2000 -> 1999 | F18 | no | no | - |

Summary: 26 mutants (M01–M26). 6 are killed by fixtures (M05, M12, M13, M14, M25, M26). 20 survive all 26 fixtures: 19 are killable and each has a kill input K01–K19 (one per mutant, §2); M09 is EQUIVALENT (§4), so no input can kill it. The control M00 passes all 26 fixtures and 83/83 selftest. Of the 20 fixture survivors, the selftest also passes on M02, M03, M06, M09, M15, M17, M18, M19, M21, M22 (selftest gap; shown in the `selftest killed?` column), and M26 is fixture-killed but passes its selftest.

Coverage gap for the frozen fixture set: none of the 26 fixtures contains `yes`, a case-folded token (`True`), a non-ASCII digit, a leading-zero value longer than 6 characters, a zero value, an empty value, a value of 199, 201, 1999 or 2001 (only 200 and 2000 appear, in F18), a comment containing `$`, `{{` or a backslash, a tab before `#`, a comment after a device name, a JSON boolean `int`, or an integer over 4300 digits in `--getoption`.

## 2. Kill inputs for survivors (contract expectation, original, mutant)

Each kill input is run by `mutants/repro.py`, which writes the file under `mutants/kill/<K>/`, runs the original and each mutant, and records `orig_matches_contract` per case in `repro-results.json` (all 19 are `true`). The contract expectation is written by hand from the §C2 / E7 sentences in `registration.md` (§C2, lines 60–112) and `registration-v2.md` (E7); the tool's output is never used to write it. Each row below is verified by `repro-results.json`.

Run: `cd .../R55W2MutTool2/mutants && python3 -I repro.py`

| K | kills | config text (literal bytes) | argv | §C2 clause that fixes the output | contract stdout (original) | mutant stdout (rc) |
|---|---|---|---|---|---|---|
| K01 | M01 (+M13) | `input {` / `  numlock_by_default = yes` / `}` | `--config kill/K01/c.conf` | "starts with `true`, `on` or `yes` → 1" | `keyboard=* repeat_rate=25 repeat_delay=600 numlock=1 from=-/-/G unsupported=0` | `numlock=0 ... from=-/-/- unsupported=1` (rc 0) |
| K02 | M02 | `input {` / `  numlock_by_default = True` / `}` | `--config kill/K02/c.conf` | "starts with `true`" is literal, lowercase; hyprlang pin `starts_with("true")` at round-46 hyprlang-config.cpp:259 | `numlock=0 from=-/-/- unsupported=1` | `numlock=1 from=-/-/G unsupported=0` |
| K03 | M03 | `input:repeat_rate = ٣٠` (U+0663 U+0660, UTF-8) | `--config kill/K03/c.conf` | "matches `[0-9]+`" — ASCII only; otherwise unsupported | `repeat_rate=25 ... unsupported=1` | `repeat_rate=30 from=G/-/- unsupported=0` |
| K04 | M04 | `input:repeat_rate =` (empty RHS) | `--config kill/K04/c.conf` | "anything else (... empty ...) → unsupported" | `repeat_rate=25 ... unsupported=1` | `repeat_rate=0 from=G/-/- unsupported=0` |
| K05 | M06 | `input:repeat_rate = 00000030` | `--config kill/K05/c.conf` | "matches `[0-9]+` → that decimal integer" (leading zeros are decimal) | `repeat_rate=30 from=G/-/- unsupported=0` | `repeat_rate=25 from=-/-/- unsupported=1` |
| K06 | M07 | `input:repeat_rate = 0` | `--config kill/K06/c.conf` | "matches `[0-9]+` → that decimal integer"; 0 in range 0..200 | `repeat_rate=0 from=G/-/- unsupported=0` | Python traceback, rc 1, empty stdout |
| K07 | M08 | `input:repeat_rate = 99999999` | `--config kill/K07/c.conf` | decimal 99999999 is out of range 0..200 → unsupported, line ignored | `repeat_rate=25 ... unsupported=1` | `repeat_rate=0 from=G/-/- unsupported=0` |
| K08 | M15 | `input:repeat_rate = 30 # note # more` | `--config kill/K08/c.conf` | "RHS is cut at its FIRST `#`" → `30` | `repeat_rate=30 from=G/-/- unsupported=0` | `repeat_rate=25 ... unsupported=1` |
| K09 | M16 | `input:repeat_rate = 30 # $x` | `--config kill/K09/c.conf` | "a line containing `$` adds one to unsupported" (whole line) | `repeat_rate=25 ... unsupported=1` | `repeat_rate=30 from=G/-/- unsupported=0` |
| K10 | M17 | `input:numlock_by_default = yes\` | `--config kill/K10/c.conf` | "a line containing a backslash adds one to unsupported" | `numlock=0 from=-/-/- unsupported=1` | `numlock=1 from=-/-/G unsupported=0` |
| K11 | M18 | `input:repeat_rate = 30 # {{x}}` | `--config kill/K11/c.conf` | "a line containing `{{` adds one to unsupported" | `repeat_rate=25 ... unsupported=1` | `repeat_rate=30 from=G/-/- unsupported=0` |
| K12 | M19 | `input {` / `# group {` / `  repeat_rate = 30` / `}` | `--config kill/K12/c.conf` | "an empty line or a line whose first character is `#` is skipped" | `repeat_rate=30 from=G/-/- unsupported=0` | `repeat_rate=25 from=-/-/- unsupported=0` |
| K13 | M20 | `device {` / `  name = kbd-a # main board` / `  repeat_rate = 50` / `}` | `--config kill/K13/c.conf --keyboard kbd-a` | "current device becomes RHS with a trailing `#`-comment cut" | `keyboard=kbd-a repeat_rate=50 ... from=D/-/- unsupported=0` | `keyboard=kbd-a repeat_rate=25 ... from=-/-/-` |
| K14 | M21 | `input:repeat_rate = 30` + FF (0x0C) + LF | `--config kill/K14/c.conf` | "A raw line is stripped of space, tab, CR, LF, VT, FF" | `repeat_rate=30 from=G/-/- unsupported=0` | `repeat_rate=25 ... unsupported=1` |
| K15 | M22 | `input:repeat_rate = 33` + TAB + `# fast` | `--config kill/K15/c.conf` | "RHS is cut at its first `#` and stripped to VALUE" (stripped = same WS set) | `repeat_rate=33 from=G/-/- unsupported=0` | `repeat_rate=25 ... unsupported=1` |
| K16 | M23 | config `input:numlock_by_default = 1`; getoption `{"option": "input:numlock_by_default", "int": true, "set": true}` | `--config kill/K16/c.conf --getoption kill/K16/opt.json` | "an integer (not boolean) `int` records that option's live value" | `numlock=1 ...` / `input:numlock_by_default config=1 live=? verdict=UNKNOWN` / `DONE ... live=UNKNOWN` | `numlock_by_default config=1 live=True verdict=AGREE`, `DONE ... live=UNKNOWN` (the boolean is recorded as an integer) |
| K17 | M24 | config `input:repeat_rate = 40`; getoption line `{"option": "input:repeat_rate", "int": <5000 nines>}` | `--config kill/K17/c.conf --getoption kill/K17/opt.json` | a JSON object with an integer `int` is a valid record (bad_json is only for non-object lines) → `live=<digits> verdict=DIFFER`, DONE `live=DIFFER`, rc 0 | `repeat_rate=40 ... unsupported=0`; `live=99…9 verdict=DIFFER`; `DONE ... live=DIFFER` | `MADO_KBDOPT: SETUP bad_json`, rc 2 |
| K18 | M10 | `input:repeat_rate = 201` | `--config kill/K18/c.conf` | out of range 0..200 → unsupported, line ignored | `repeat_rate=25 ... unsupported=1` | `repeat_rate=201 from=G/-/- unsupported=0` |
| K19 | M11 | `input:repeat_delay = 2001` | `--config kill/K19/c.conf` | out of range 0..2000 → unsupported, line ignored | `repeat_delay=600 ... unsupported=1` | `repeat_delay=2001 from=-/G/- unsupported=0` |

Notes on the contract column: the §C2 range sentence in `registration.md` gives the three maxima (`repeat_rate` 0..200, `repeat_delay` 0..2000, `numlock_by_default` 0..1). The pinned source (`round-55/fetch/Hyprland-ConfigValues.cpp:277-280`) confirms `.min/.max` = 0/200 and 0/2000 and `Bool` with default false for numlock. Whether Hyprland rejects or clamps an out-of-range value is not pinned (the tool's own docstring says so). K18/K19 therefore pin the lane's rule, not the compositor's behaviour.

Repro for one row (K04, original vs mutant):
```
cd .../R55W2MutTool2/mutants
python3 -I M00-original.py --config kill/K04/c.conf   # MADO_KBDOPT: ... repeat_rate=25 ... unsupported=1
python3 -I M04.py          --config kill/K04/c.conf   # MADO_KBDOPT: ... repeat_rate=0 ... unsupported=0
```

## 3. Model-level findings (not mutants; the frozen text vs the pinned source)

These were found by checking the tool's comment, brace and backslash rules against the round-46 hyprlang pin (`round-46/fetch/hyprlang-config.cpp`). The tool conforms to the frozen text in each case. The frozen text diverges from the pinned source. Each one is reproduced by running the original tool on the input below (no mutant involved). Files: `mutants/model/`.

**A. Backslash line continuation: next line is applied as a separate line (BROKEN, silent-value, against "never guessed").**
- Input `model/A-backslash-continuation.conf`:
  ```
  input {
    repeat_rate = 30 \
    repeat_delay = 300
  }
  ```
- Tool (original): `MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=300 numlock=0 from=-/G/- unsupported=1`
- Pinned hyprlang: `getNextLine` (hyprlang-config.cpp:44-65) joins a line ending in `\` with the next line: `  repeat_rate = 30  repeat_delay = 300`. `parseLine` then sets `repeat_rate` to `30  repeat_delay = 300`, which fails `configStringToInt`, so `repeat_delay` is never set. Source-level expectation: `repeat_rate=25 repeat_delay=600 ... from=-/-/-`.
- The tool flags the backslash (unsupported=1) but still prints `repeat_delay=300` from `G` as a definite value. The frozen §C2 model ("split on `\n`") does not model continuation. Fixture H08 has a backslash line followed by `}`, where both outputs happen to agree (25/600) and only the unsupported count differs, so the frozen fixtures do not discriminate this.

**B. A block opener with a trailing `#` comment is silently ignored (BROKEN vs pinned source; silent, unsupported=0).**
- Input `model/B-block-open-comment.conf`:
  ```
  input { # c
    repeat_rate = 30
  }
  ```
- Tool (original): `MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0`
- Pinned hyprlang: `parseLine` cuts the comment first (hyprlang-config.cpp:674-704, a single `#` truncates the line), then trims to `input {`, which ends in `{`, so the category opens (hyprlang-config.cpp:713, 899-908). Source-level expectation: `repeat_rate=30 from=G/-/-`.
- The frozen text says only a line ending in `{` pushes a category, and that any other line is ignored. The raw line `input { # c` does not end in `{`, so the frozen text sends it to "anything else is ignored". The tool's own selftest asserts this (`"\`{\` with trailing comment not a push"`, expects 25). The pinned source cuts the comment before the `{` test, so the block opens. This is a silent wrong value with no flag, the sharpest model finding. It is a frozen-text defect, not a tool bug, and no frozen predicate catches it.

**C. Hex is parsed by hyprlang but reported unsupported (conservative; not a wrong value).**
- Input `model/C-hex-value.conf`: `input:repeat_rate = 0x10`
- Tool: `repeat_rate=25 ... unsupported=1`. Pinned `configStringToInt` (hyprlang-config.cpp:195-197) returns 16 for `0x…`. The frozen text says "(hex ...) → unsupported", which is the tool's behaviour and is safe (it is flagged, never guessed). The frozen claim that the model "parses as configStringToInt" is inaccurate for hex; this does not change any output that a fixture pins.

**D. `source = …` is ignored silently (contract-explicit; pinned by H08).**
- Input `model/D-source-line.conf`: `source = ~/kb.conf`
- Tool: `repeat_rate=25 ... unsupported=0`. The frozen text says `source` LHS "ignored". Included files are never read, and no flag is raised. Fixture H08 pins this behaviour. Recorded as a contract-level limit, not counted as a mutant.

**`##` rule (checked, conservative).** The pin (hyprlang-config.cpp:686-704) treats `##` as an escape for a literal `#`, not as a comment. The tool marks any RHS containing `##` unsupported. For `30 ## x` the pinned source yields an error, so the tool is consistent. For `30 # c ## d` the pinned source yields 30 and the tool yields unsupported. That is over-flagging, never a wrong value, and it is the frozen rule.

**Numlock range 0..1 (flagged, not pinned).** E7 states this is the lane's modelling rule. `numlock_by_default = 2` yields unsupported=1 (F18), which is safe. `Bool` in the pin has no min/max (ConfigValues.cpp:277).

## 4. M09 is equivalent (proof and check)

M09 changes the digit cap from 6 to 4 characters. For the cap to matter, the value must have more than 4 significant digits after `lstrip("0")`. Then its integer is at least 10000. Every maximum is at most 2000, so `value > MAXIMA` holds and the line is unsupported in both versions (the original uses `10**6`, which also exceeds every maximum). For 4 or fewer significant digits the code path is identical.

Check: `python3 -I equiv.py` (in-process `report()` comparison, original vs `M09.py`, over `input:<key> = <token>` for each of the 3 keys):
- `checked=1440147 tokens_per_key=480049 differing=0`, rc 0.
- Tokens: all integers 0..100000; the same with 1..40 leading zeros (0..2000); 300000 seeded random digit strings of length 5..30 with random leading zeros; boundary tokens (`2000`, `02000`, `00002001`, `9`×5000, …).

## 5. What survived, what was not verified

- **Tool, value parsing and ranges (this focus):** every non-equivalent mutant is killed by a fixture (6 mutants) or by a kill input K01–K19 (19 mutants). The original tool matches the frozen §C2 text on all 26 fixtures, on all 19 kill inputs, and on `equiv.py`. No implementation defect against its own frozen text was found. The §3 items are defects of the frozen text relative to the pinned source (and A/B are silent or over-stated values); they are reported as model findings, not as implementation mutants.
- **Fixture coverage gap (not a tool bug):** 19 of the 20 fixture-survivor mutants are killable only by inputs outside the frozen fixture set (K01–K19). The frozen C2 harness (PRED-C2-r55) does not discriminate them. M09 is the 20th, equivalent.
- **BROKEN (model vs pinned source):** A (backslash continuation), B (block opener with comment). Both are silent or carry a value that hyprlang does not set. Not measured by the frozen predicate.
- **UNVERIFIED:** whether Hyprland rejects or clamps out-of-range values (the pin shows `.min/.max` on `MS<Int>`, not the enforcing site); `isNumber(VALUE,false)` (used at hyprlang-config.cpp:265 but defined outside the pin, so the sign rule is not pinned); hyprlang's read of `numlock_by_default = 2` (Bool).
- **Not run:** no hyprctl call (host reads not needed for this focus); no network reads; no hyprlang library execution (the model findings rest on reading the pinned source, not on running hyprlang).

## 6. Reproduction

From `.ufo/waves/round-55/w2/R55W2MutTool2/mutants/`:
- `python3 -I M00-original.py --selftest` → `MADO_KBDOPT_SELFTEST: 83/83 assertions passed`
- `python3 -I repro.py` → writes `kill/K01..K19`, asserts the original matches the contract text for all 19, prints each mutant kill list, writes `repro-results.json`
- `python3 -I equiv.py` → `differing=0` for M09
- `python3 -I M00-original.py --config model/A-backslash-continuation.conf` (and B, C, D) → the model-finding outputs in §3
- `mkmut.py` regenerates the 26 mutant copies and the fixture scores; it expects the export at `/fast/scratch/hyaku/mado-r55/R55W2MutTool2`, which was removed after this run, so re-run the `git archive` command in §Setup first.

Files in this directory: `mutants/M00-original.py` (control), `mutants/M01.py`..`M26.py` (copies), `mutants/scores.json`, `mutants/repro.py`, `mutants/repro-results.json`, `mutants/kill/K01..K19/`, `mutants/equiv.py`, `mutants/mkmut.py`, `mutants/model/A..D`.
