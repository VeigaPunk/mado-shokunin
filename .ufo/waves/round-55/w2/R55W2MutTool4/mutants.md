# R55W2MutTool4 — mutation test of `tools/mado-kbdopts.py` (C2), focus: argv, setup reasons and exit codes, getoption join, output/order/repeat

Subject: `tools/mado-kbdopts.py` at lane revision `57584ed67716340b3d466fa04333ac0bab3fb79e`, sha256 `9c69dd62c1737d4842a4a0e73db3f8317eda71ee103e71ad3cda11a19c837c2e` (`results/orig.sha256`).
Frozen text: `.ufo/waves/round-55/registration.md` §C2 (v1), `registration-v2.md` E7 (C2 wording is unchanged by v2 except E7).

## Method (what ran)

- Export: `git archive 57584ed… tools/mado-kbdopts.py .ufo/waves/round-55/fixtures .ufo/waves/round-55/fetch` into scratch. Read-only; no lane or fleet mutation.
- Harness `bin/harness.sh <ID> <tool>`: copies the fixtures and `fetch/` into a private run dir, places the tool there as `tool.py`, runs `python3 -I tool.py <args from args.json>` with cwd = that run dir for all 26 fixtures (18 committed `c2/F01..F18`, 8 hold-out `c2-holdout/H01..H08`), and compares stdout bytes and exit status with `expected.out` / `expected.rc`. Then runs `python3 -I tool.py --selftest`; a mutant is selftest-killed when rc≠0 or the line is not `N/N`.
- Unmodified tool: 26/26 fixtures pass; selftest `MADO_KBDOPT_SELFTEST: 83/83 assertions passed` (`results/ORIG.txt`). Note: registration-v2 prose says "82 selftest assertions"; the shipped selftest has 83. Prose drift only.
- 25 mutants, each exactly one changed line (`diffs/Mxx.diff`, full sources `src/Mxx.py`). Each was made with the `edit` tool on a COPY in scratch. The lane was never opened for write; nothing in the lane was modified or restored. Python 3.14.8, `python3 -I`.
- Survivor repros: `bin/repro.sh <orig> <mutant-dir> <workdir>` runs the minimal input under the original and the mutant (`python3 -I`, cwd = workdir). Output: `results/repro.txt`. Each survivor has an `attack` row and a `control` row (a parser-compatible, in-grammar input that must print identically on both sides; it does).

## Result

- 9 of 25 mutants fail at least one fixture (M03, M07, M08, M15, M19, M22, M23, M24, M25).
- 16 of 25 pass all 26 fixtures: **M01, M02, M04, M05, M06, M09, M10, M11, M12, M13, M14, M16, M17, M18, M20, M21**.
- Of those 16, selftest kills 12. Four pass both fixtures and selftest: **M04, M06, M17, M18**.
- Under PRED-C2-r55 selftest is not counted ("`--selftest` alone is informational and is not part of PRED-C2-r55", registration.md §C2). So for the gate, 16 defective variants of the focus behaviour are indistinguishable from the shipped tool.

## Mutant table

Fixture column: IDs of the fixtures whose stdout or rc differs from `expected.out`/`expected.rc`. Selftest column: the selftest verdict on the mutant (KILLED = rc≠0 or N≠M, with the failing assertion name where the tool prints one). Survivor = passes all 26 fixtures.

| mutant | edit (orig line → mutant) | fixtures killed (of 26) | selftest killed? | survivor? |
|---|---|---|---|---|
| M01 | :114 `if i + 1 >= len(argv):` → `if i + 1 > len(argv):` (dangling flag off-by-one) | none | KILLED (IndexError traceback, rc 1) | **SURVIVOR** (fixtures) |
| M02 | :123 `elif flag == "--getoption" and not getoption:` → `elif flag == "--getoption":` (repeat accepted) | none | KILLED (`usage: two --getoption`) | **SURVIVOR** (fixtures) |
| M03 | :129 `if not any(kind == "config" …):` → `… and False:` (no `--config` accepted) | F17 | KILLED (`usage: no args`, `usage: no --config`) | killed by fixtures |
| M04 | :120 `ord(c) < 32 or ord(c) == 127` → `ord(c) < 32` (DEL allowed in NAME) | none | survived (83/83) | **SURVIVOR** (both) |
| M05 | :74 `MAXIMA` repeat_rate 200 → 201 | none | KILLED (`rate 201 out of range`) | **SURVIVOR** (fixtures) |
| M06 | :70 `WS` drops `\v` | none | survived (83/83) | **SURVIVOR** (both) |
| M07 | :136 true-prefix drops `on` | F08 | KILLED (`on prefix`) | killed by fixtures |
| M08 | :138 false-prefix drops `no` | F07 | KILLED (`no prefix is zero`) | killed by fixtures |
| M09 | :164 `cur = None` → `pass` (device not forgotten when stack empties) | none | KILLED (`device forgotten after block`) | **SURVIVOR** (fixtures) |
| M10 | :262 DONE precedence: UNKNOWN checked before DIFFER | none | KILLED (`live overall DIFFER beats UNKNOWN`) | **SURVIVOR** (fixtures) |
| M11 | :234 drop the integer-type check on `int` (keep boolean rejection) | none | KILLED (`live float int ignored`) | **SURVIVOR** (fixtures) |
| M12 | :234 drop the boolean rejection on `int` | none | KILLED (`live boolean int ignored`) | **SURVIVOR** (fixtures) |
| M13 | :234 accept float `int` (`(int, float)`) | none | KILLED (`live float int ignored`) | **SURVIVOR** (fixtures; contract-ambiguous, see O2) |
| M14 | :228 `json.loads(line, parse_constant=reject)` → `json.loads(line)` (NaN/Infinity accepted) | none | KILLED (`bad_json on NaN constant`) | **SURVIVOR** (fixtures) |
| M15 | :221 blank `--getoption` line not skipped | F02, F13, F14, H06 | KILLED (`SETUP bad_json`, rc 2) | killed by fixtures |
| M16 | :232 non-object JSON line → `continue` instead of `bad_json` | none | KILLED (`bad_json on JSON array`) | **SURVIVOR** (fixtures) |
| M17 | :103 `len(data) > MAX_BYTES` → `>=` (exactly 1048576 bytes → too_large) | none | survived (83/83) | **SURVIVOR** (both) |
| M18 | :104 too_large reason → `unreadable` | none | survived (83/83) | **SURVIVOR** (both) |
| M19 | :409 setup exit code 2 → 1 | F15, F16, F17 | survived (selftest does not check the CLI rc) | killed by fixtures |
| M20 | :174 device name line: no `#`-comment cut | none | KILLED (`device name cut at comment`) | **SURVIVOR** (fixtures) |
| M21 | :252 `--getoption` comparison uses the first `--keyboard`'s device value instead of the global | none | KILLED (`live compares the global, not a device`) | **SURVIVOR** (fixtures) |
| M22 | :244 keyboard list deduplicated (`dict.fromkeys`) | H04 | KILLED (`repeated --keyboard prints per argument`) | killed by fixtures |
| M23 | :180 `lhs in NAMES` → `lhs in NAMES[:2]` (device numlock key not relevant) | F05, H03 | survived (83/83) | killed by fixtures |
| M24 | :235 `live[opt] = val` → `live.setdefault(opt, val)` (first getoption line wins) | H06 | KILLED (`live later line wins`) | killed by fixtures |
| M25 | :205 `if n in dev:` → `if n in dev and n not in st.glob:` (global beats device) | F04, F05, F09, H03, H04 | KILLED (`device beats global`) | killed by fixtures |

Totals: fixtures kill 9; survive all 26 fixtures: 16 (M01, M02, M04, M05, M06, M09, M10, M11, M12, M13, M14, M16, M17, M18, M20, M21); survive selftest too: 4 (M04, M06, M17, M18).

## Survivors: minimal input, contract text, output under original vs mutant

Repro rows: `results/repro.txt`, labels `M01 attack` / `M01 control` etc. The "orig" column is the unchanged tool, i.e. the output the frozen text requires (or, where noted, the docstring requires). "Mutant" is the mutant. Every control row is byte-identical on both sides.

**M01** — contract: "anything else … is usage" (§C2 argv), exit 2 on setup failure. Input argv `--config r30.conf --keyboard` (or `--config` alone).
- orig: `MADO_KBDOPT: SETUP usage`, rc 2.
- mutant: empty stdout, `IndexError: list index out of range` on stderr, rc 1.

**M02** — contract: "`--getoption PATH` at most once; anything else … is usage". Input argv `--config empty.conf --getoption g40.json --getoption g41.json`.
- orig: `MADO_KBDOPT: SETUP usage`, rc 2.
- mutant: rc 0; `MADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=41 verdict=DIFFER`, `…DONE keyboards=1 unsupported=0 live=DIFFER`.

**M04** — contract: §C2 is silent on NAME control bytes. The tool's docstring (and a code comment, "the contract is silent, this is an extension") says a NAME with a byte below 0x20 or equal to 0x7f is usage. Input argv `--config empty.conf --keyboard $'kbd\x7fx'`.
- orig: `MADO_KBDOPT: SETUP usage`, rc 2.
- mutant: `MADO_KBDOPT: keyboard=kbd<DEL>x repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0` then `DONE keyboards=1 unsupported=0 live=NONE`, rc 0.
- Both suites pass the mutant. This is a gap in the docstring-level rule, not in the frozen text (see O1).

**M05** — contract: "`repeat_rate` 0..200 … out-of-range → `unsupported` +1, line ignored." Input config `input:repeat_rate = 201`.
- orig: `MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=1`, `DONE … unsupported=1 live=NONE`.
- mutant: `repeat_rate=201 … from=G/-/- unsupported=0`, `DONE … unsupported=0`.
- Control `input:repeat_rate = 200`: identical (`repeat_rate=200 … from=G/-/-`).

**M06** — contract: "A raw line is stripped of space, tab, CR, LF, **VT**, FF." Input config: the bytes `0x0b` `input:repeat_rate = 30` `\n` (VT first on the raw line).
- orig: `repeat_rate=30 … from=G/-/- unsupported=0`.
- mutant: `repeat_rate=25 … from=-/-/- unsupported=0` (the line is no longer recognised as `input:repeat_rate`).
- Both suites pass the mutant.

**M09** — contract: "when the stack empties the current device is forgotten." Input config `device {\n  name = kbd-a\n}\ndevice {\n  repeat_rate = 50\n}\n`, argv `--config dev9.conf --keyboard kbd-a`.
- orig: `keyboard=kbd-a repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=1`.
- mutant: `keyboard=kbd-a repeat_rate=50 repeat_delay=600 numlock=0 from=D/-/- unsupported=0`.

**M10** — contract: "`DIFFER` if any DIFFER, else `UNKNOWN` if any UNKNOWN, else `AGREE`." Input config `input:repeat_rate = 40\n`, getoption `{"option":"input:repeat_rate","int":41}`.
- orig: lines identical to the mutant (`live=41 verdict=DIFFER`, `…verdict=UNKNOWN` ×2), final `MADO_KBDOPT: DONE keyboards=1 unsupported=0 live=DIFFER`.
- mutant: final line `… live=UNKNOWN`.

**M11** — contract: "an object with a string `option` and an integer (not boolean) `int` records that option's live value … other objects are ignored; no record → `live=?` `UNKNOWN`." Input getoption `{"option":"input:repeat_rate","int":"x"}`.
- orig: `MADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN`, `DONE … live=UNKNOWN`.
- mutant: `config=25 live=x verdict=DIFFER`, `DONE … live=DIFFER`.

**M12** — contract: "(not boolean)". Input getoption `{"option":"input:numlock_by_default","int":true}`.
- orig: numlock line `config=0 live=? verdict=UNKNOWN`.
- mutant: numlock line `config=0 live=True verdict=DIFFER`; `DONE … live=DIFFER`.

**M13** — contract: "an integer (not boolean) `int`". Input config `input:repeat_rate = 40`, getoption `{"option":"input:repeat_rate","int":40.0}`.
- orig: `config=40 live=? verdict=UNKNOWN`.
- mutant: `config=40 live=40.0 verdict=AGREE`.
- Contract-ambiguous: the frozen text does not say whether JSON `40.0` is an integer. Listed as a survivor because the tool's own selftest rejects it.

**M14** — contract: "`bad_json` (a non-empty `--getoption` line that is not a JSON object)". Input getoption `{"nothing": NaN}`.
- orig: `MADO_KBDOPT: SETUP bad_json`, rc 2.
- mutant: rc 0; three `MADO_KBDOPT_LIVE … live=? verdict=UNKNOWN` lines, `DONE … live=UNKNOWN`.
- Reading "JSON object" strictly (RFC 8259 has no NaN), the mutant is wrong. The tool's selftest pins the strict reading.

**M16** — contract: "`bad_json` (a non-empty `--getoption` line that is not a JSON object)". Input getoption `[1]`.
- orig: `MADO_KBDOPT: SETUP bad_json`, rc 2.
- mutant: rc 0; `DONE … live=UNKNOWN`.

**M17** — contract: "`too_large` (a file over 1048576 bytes)". Input config of exactly 1048576 bytes (`#` + 1048574 × `x` + `\n`; `repro/exact.conf` in the run).
- orig: `MADO_KBDOPT: keyboard=* repeat_rate=25 …`, `DONE … live=NONE`, rc 0.
- mutant: `MADO_KBDOPT: SETUP too_large`, rc 2.
- Both suites pass the mutant; no fixture or selftest case sits at the boundary.

**M18** — contract: `too_large` reason for a file over 1048576 bytes. Input config of 1048577 bytes (`repro/over.conf`).
- orig: `MADO_KBDOPT: SETUP too_large`, rc 2.
- mutant: `MADO_KBDOPT: SETUP unreadable`, rc 2.
- Both suites pass the mutant; `too_large` is not exercised by any fixture or selftest case.

**M20** — contract: "the current device becomes RHS with a trailing `#`-comment cut and stripped." Input config `device {\n  name = kbd-a # my kbd\n  repeat_rate = 50\n}\n`, argv `--keyboard kbd-a`.
- orig: `keyboard=kbd-a repeat_rate=50 … from=D/-/- unsupported=0`.
- mutant: `keyboard=kbd-a repeat_rate=25 … from=-/-/- unsupported=0`.
- Control: a device line without a comment is identical on both sides.

**M21** — contract: "`config=<global effective value, default if unset>`". Input config `input {\n  repeat_rate = 30\n}\ndevice {\n  name = kbd-a\n  repeat_rate = 50\n}\n`, argv `--keyboard kbd-a --getoption g50.json` (g50 = `{"option":"input:repeat_rate","int":50}`).
- orig: `MADO_KBDOPT_LIVE: option=input:repeat_rate config=30 live=50 verdict=DIFFER`, `DONE … live=DIFFER`.
- mutant: `config=50 live=50 verdict=AGREE`, `DONE … live=UNKNOWN`.

## Coverage gaps the table reveals (fixtures and selftest)

- `too_large` (M17, M18): no fixture, no selftest case, at or over the 1048576-byte boundary.
- Setup exit code and reasons: fixtures cover rc 2 for `unreadable`, `bad_json`, `usage`. No fixture or selftest asserts the CLI rc of a successful run with a non-zero DONE live value (the selftest never checks rc).
- `DONE` precedence when DIFFER and UNKNOWN co-occur (M10): no fixture mixes them.
- Non-integer `int` values (`"x"`, `true`, `40.0`; M11–M13): no fixture; selftest-only.
- Device-block details: name comment cut (M20), device forgotten when the stack empties (M09), numlock as a device key (M23, killed only by F05/H03), and live compared to the device value (M21): no fixture.
- VT in the stripped set (M06) and DEL in the NAME control-byte rule (M04): neither in any fixture nor selftest.
- Keyboard list dedup (M22), getoption last-line-wins (M24), global-beats-device (M25) are killed, but each by a single or hold-out fixture only.

## Observations on the frozen text (not mutants)

- **O1 — NAME control-byte rule is outside the frozen C2 text.** registration.md §C2 and registration-v2 E7 do not mention `--keyboard` control bytes. The rule (below 0x20 or 0x7f → usage) exists only in the tool's docstring and code comment, which says "the contract is silent, this is an extension". M04 exposes that the rule has no test.
- **O2 — "an integer (not boolean)" is undefined for JSON numbers with a fraction.** M13 is a survivor only under a reading of "integer" that accepts `40.0`. The tool rejects it; its selftest pins the rejection.
- **O3 — "non-empty `--getoption` line" vs whitespace-only lines.** The tool strips WS (including the 0x0b/0x0c characters) and skips a line that becomes empty, so `"  "` is a blank line. The frozen text says "non-empty". The selftest pins the tool's reading (`live blank lines skipped`).
- **O4 — NaN/Infinity.** The frozen "not a JSON object" is the basis for rejecting `{"nothing": NaN}` (M14). The text does not say NaN is in or out; the tool rejects it and its selftest pins that.
- **O5 — selftest count.** registration-v2 prose says 82 selftest assertions; the shipped selftest has 83, all passing on the unmodified tool.

## Limits

- Mutation sample: 25 one-line edits in the focus list, not an exhaustive operator set. 16 survivors is a lower bound on the gap in the focus behaviours, not a count of all gaps.
- Mutants are judged only by stdout bytes, rc, and selftest exit. Each survivor has a repro input on which its stdout or rc differs from the original (`results/repro.txt`), so none is an equivalent mutant on those inputs.
- `--selftest` is informational under the frozen predicate; its kill column is evidence about the tool's own assertions, not about PRED-C2-r55.
- Nothing here runs a Hyprland process, `hyprctl`, or the L1 harness (`MADO_R55_C2`).

## Files

- `diffs/Mxx.diff` — the one-line diff of each mutant against `tools/mado-kbdopts.py` (paths relative to the scratch export).
- `src/Mxx.py` — full mutant sources (the original is `tools/mado-kbdopts.py`, sha above).
- `bin/harness.sh` — 26-fixture + selftest harness used for the table (`results/mutants.txt`, `results/ORIG.txt`).
- `bin/repro.sh` — survivor repro (`results/repro.txt`); run as `bash bin/repro.sh <orig-tool> <src-dir> <workdir>`. The `<src-dir>` is the mutant directory (`src/`), and the script expects `Mxx.py` files there.
- `results/selftest-fails.txt` — the selftest stderr/stdout for each mutant.
- `results/fixtures.sha256` — sha256 of every file under the fixture tree at the export.
- Hold-out commitment was not verified by this seat.
