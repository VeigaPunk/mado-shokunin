# R55RevC2Spec — §C2 ambiguity review (`tools/mado-kbdopts.py`)

Contract read: `registration.md` §C2 at freeze commit `54dacbd8` (working-tree copies are byte-identical to it: `git diff --stat` empty).
Fixtures read: `fixtures/c2/F01..F18` (73 committed files, all read; `fixtures/c2-holdout` is absent at the freeze commit and was not looked for).
Tool: `tools/mado-kbdopts.py` is **absent** from the lane tree, so nothing here is a test of an implementation. It is a reading analysis.

Method. A scratch reference model (`receipts/ref.py`, `python3 -I`) implements §C2 with one switch per ambiguity. `LIT` is the reading the 18 committed fixtures pin: it reproduces 18/18 (`receipts/fixture-pinning.txt`). Each alternative is run on a concrete input (`receipts/cases.txt`, 43 cases). "Pinned" means at least one committed fixture fails under the alternative. "Unpinned" means no committed fixture distinguishes the readings, so the frozen claims cannot catch a wrong choice.

Severity. **H**: silent wrong value, wrong `from=` letter, or wrong exit on a plausible config. **M**: divergence on a plausible input, or a contract sentence that contradicts itself or its source. **L**: edge case or operability.

---

## 0. What the committed fixtures decide

| Reading | Evidence |
|---|---|
| Top-level `input:repeat_rate = 30` (no block) has KEY `input:repeat_rate` (join), not `:input:repeat_rate` (literal text) | **F10**: literal text gives `unsupported=3`; expected `4` (A12) |
| `##` is tested on the RHS **before** the `#` cut | **F12**: `repeat_delay = 4##0` → unsupported=1; the after-cut alternative gives unsupported=0 (A7) |
| Booleans are prefix matches (`nope`→0, `online`→1) | F07, F08 |
| Device value overrides global when the global line comes first in a file | F04, F05, F09. Device-before-global order is **unpinned** (A20) |
| Same-name device blocks merge (F09); a later write of the **same** key winning is **unpinned** | F09 (merge only) |
| Global later file overrides global earlier file | F11 (`repeat_rate` 30 then 45 → 45) |
| Range is inclusive (200, 2000); numlock `2` is out of range | F18 |
| getoption verdicts, `bad_json`, `unreadable`, empty-argv `usage`, host path | F13, F14, F16, F15, F17, F02 |

Everything in A1–A36 below is **unpinned** unless marked otherwise.

---

## 1. Line grammar

### A1 — `}` followed by text (M, unpinned)
Sentence: "exactly `}` pops the stack". Input (`cases/C01`):
```
input {\n  repeat_rate = 30\n} # end\nrepeat_delay = 300\n
```
- exact (`line == "}"`): `keyboard=* repeat_rate=30 repeat_delay=300 numlock=0 from=G/G/- unsupported=0`
- lead (`line.startswith("}")`): `keyboard=* repeat_rate=30 repeat_delay=600 numlock=0 from=G/-/- unsupported=0`

### A2 — `{` followed by a comment (H, unpinned)
Sentence: "a line ending in `{` pushes its text". `#` cut is only specified for values and names. Input (`cases/C02`):
```
input { # main\n  repeat_rate = 30\n}\n
```
- line must literally end in `{` (no push): `keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0`
- cut `#` first, then test for `{`: `keyboard=* repeat_rate=30 repeat_delay=600 numlock=0 from=G/-/- unsupported=0`

Note: under the first reading the `}` then pops an empty stack, silently. A real config with a trailing comment on a block opener loses its values with no `unsupported` count.

### A3 — indented comment that ends in `{` (M, unpinned)
Sentence: "a line whose first character is `#` is skipped" — is "line" raw or stripped? Input (`cases/C03`):
```
input {\n  # section {\n  repeat_rate = 30\n}\n
```
- strip first, then `#`-test (comment skipped): `repeat_rate=30 ... from=G/-/- unsupported=0`
- raw first character (`  # section {` is not skipped, pushes `# section`): `repeat_rate=25 ... from=-/-/- unsupported=0`

### A4 — line splitting (M, unpinned)
Sentence: "split on `\n`". `str.splitlines()` also splits on CR, VT, FF, U+2028 and others. Input (`cases/C24`, CR-only file):
```
input {\r  repeat_rate = 30\r}\r
```
- split on `\n`: one line, `LHS` = `input {\rrepeat_rate`; `repeat_rate=25 ... from=-/-/- unsupported=0`
- `splitlines()`: `repeat_rate=30 ... from=G/-/- unsupported=0`

### A5 — strip character set (M, unpinned)
Sentence: "stripped of space, tab, CR, LF, VT, FF". Python `str.strip()` also strips `\x1c`–`\x1f`, U+00A0 and other Unicode spaces. Inputs (`cases/C25`, `cases/C26`): `  repeat_rate = 30\x1c` and `  repeat_rate = 30` followed by U+00A0.
- exact set: `repeat_rate=25 ... from=-/-/- unsupported=1`
- `str.strip()`: `repeat_rate=30 ... from=G/-/- unsupported=0`

### A6 — UTF-8 BOM (M, unpinned)
Sentence: "decoded as UTF-8". Python `utf-8` keeps U+FEFF; `utf-8-sig` drops it. Input (`cases/C23`): `EF BB BF` + `input {\n  repeat_rate = 30\n}\n`.
- `utf-8`: `repeat_rate=25 ... from=-/-/- unsupported=0` (the `input` block is never recognised, silently)
- `utf-8-sig`: `repeat_rate=30 ... from=G/-/- unsupported=0`

### A7 — where the check scope ends (M, partly pinned)
Sentence: "a line containing `$`, `{{` or a backslash" (whole line) vs "a RHS containing `##`" (RHS).
Inputs (`cases/C20`, `cases/C21`): `  repeat_rate = 30 # 50$`, `  repeat_rate = 40 # C:\dir`.
- whole line, comment included (literal): `repeat_rate=25 ... unsupported=1` and `repeat_rate=25 ... unsupported=1`
- value after the `#` cut: `repeat_rate=30 ... from=G/-/- unsupported=0` and `repeat_rate=40 ... from=G/-/- unsupported=0`

Pinned: F12 pins "checked before the cut" for `##` (after-cut gives unsupported=0 on F12 and fails it). By analogy the same holds for `$` and `\`, but no fixture contains those characters in a comment. Recommend the contract state it explicitly.

---

## 2. Values

### A8 — "matches `[0-9]+`": fullmatch or prefix? (H, unpinned, settled by source)
Sentence: "matches `[0-9]+`". The contract's own examples ("hex, sign, float, empty, words → unsupported") require fullmatch. A prefix reading would make `0x1F` → 0 and `1.5` → 1. The pinned hyprutils body (`round-45/fetch/hyprutils-String.cpp:50-84`, `isNumber2`) requires every character to be a digit (a leading `-`, or `.` only when `allowfloat`), so the real parser also rejects spaces.

| input (`cases/`) | fullmatch (LIT) | prefix |
|---|---|---|
| `repeat_rate = 30 = 4` (C04) | `repeat_rate=25 ... unsupported=1` | `repeat_rate=30 ... from=G/-/- unsupported=0` |
| `repeat_rate = 3 3` (C05) | `repeat_rate=25 ... unsupported=1` | `repeat_rate=3 ... from=G/-/- unsupported=0` |
| `repeat_rate = 1.5` (C06) | `repeat_rate=25 ... unsupported=1` | `repeat_rate=1 ... from=G/-/- unsupported=0` |
| `repeat_rate = 0x1F` (C07) | `repeat_rate=25 ... unsupported=1` | `repeat_rate=0 ... from=G/-/- unsupported=0` |
| `numlock_by_default = 1abc` (C08) | `numlock=0 ... from=-/-/- unsupported=1` | `numlock=1 ... from=-/-/G unsupported=0` |

Recommendation: write "fullmatch `[0-9]+`" in the contract.

### A9 — leading minus: contract vs source (H, unpinned, **contract contradicts source**)
Sentence: "anything else (hex, sign, float, empty, words) → `unsupported`", and "parses as `configStringToInt`". Input (`cases/C43`): `numlock_by_default = -0` and `repeat_rate = -0`.
- contract as written (sign → unsupported): `repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=2`
- source (`isNumber2` accepts a leading `-` and needs the last character to be a digit; `-0` → `stoll` → 0): `repeat_rate=0 repeat_delay=600 numlock=0 from=G/-/G unsupported=0`

Evidence: `round-45/fetch/hyprutils-String.cpp:50-84`; `nm -D --undefined-only /usr/lib/libhyprlang.so.0.6.8` shows an import of `Hyprutils::String::isNumber(const std::string&, bool)`, so the installed hyprlang calls the hyprutils function. The lone `-` is rejected by the same function (`isdigit(str.back())`), so the divergence is limited to `-` followed by digits, and only `-0…` survives the range checks.
Recommendation: either model `-digits` as the source does or state the sign rule as an explicit divergence the tool reports.

### A10 — booleans are case-sensitive (resolved, pinned by source)
`numlock_by_default = True` → `unsupported=1`, numlock 0. `round-46/fetch/hyprlang-config.cpp` line 259 uses `VALUE.starts_with("true")`, which is case-sensitive. Prefix behaviour is pinned by F07/F08.

### A11 — boolean words on integer keys (resolved by text, unpinned)
`repeat_rate = yes` (C28) → `repeat_rate=1 ... from=G/-/-`. The text runs every VALUE through `configStringToInt`, which is generic. A reader who restricts booleans to `numlock_by_default` contradicts the text. Low risk; the contract should say "any key" if that is intended.

---

## 3. Keys and blocks

### A12 — top-level colon-form key (H, **pinned by F10 against the literal sentence**)
Sentence: "KEY is the stack joined with `:` then `:` then LHS". With an empty stack the literal string is `":" + LHS`, so `:input:repeat_rate`, which is never relevant. Input (`cases/C29`): `input:repeat_rate = 30\n`.
- literal text (leading colon): `repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0`
- join (LHS when stack is empty): `repeat_rate=30 repeat_delay=600 numlock=0 from=G/-/- unsupported=0`

F10 (`device[kbd-a]:repeat_rate = 70` at top level) expects `unsupported=4`. The literal sentence gives 3. The fixture pins the join reading. The contract text is wrong as written and should say so.

### A13 — `device {` opened inside `input {` (H, unpinned)
Sentence: "the stack is exactly `["device"]`". Input (`cases/C09`, `--keyboard kbd-a`):
```
input {\n  device {\n    name = kbd-a\n    repeat_rate = 50\n  }\n}\n
```
- exact stack (literal): `keyboard=kbd-a repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0`
- innermost block is `device` (a reader who thinks "device block" means "any device block"): `keyboard=kbd-a repeat_rate=50 repeat_delay=600 numlock=0 from=D/-/- unsupported=0`

The text supports the literal reading. A parser author who reads it as "innermost" gets a device value that Hyprland's own parser would not give for this layout. Say which in the contract.

### A14 — RELEVANT key nested in a `touchpad` inside a device (M, unpinned, asymmetric)
Sentence: "KEY starts with `device[` and its last component is one of those three names". Two layouts with the same nested key, `--keyboard kbd-a`:
- plain `device {` (C10): `keyboard=kbd-a repeat_rate=25 ... unsupported=0` (the KEY is `device:touchpad:repeat_rate`, not relevant)
- `device[kbd-a] {` (C11): `keyboard=kbd-a repeat_rate=25 ... unsupported=1` (the KEY starts with `device[`, so it is counted)

The text produces this asymmetry but does not say that is intended. Decide whether nested bracket keys count.

### A15 — device name containing `$` (H, unpinned)
Sentence: "the current device becomes RHS" with a comment cut; `$` is not mentioned for name lines, and the contract says "never guessed". Input (`cases/C19`): `$kbd = kbd-a` then `device {\n  name = $kbd\n  repeat_rate = 50\n}`.
- literal (device NAME is the string `$kbd`): `--keyboard kbd-a` → `keyboard=kbd-a repeat_rate=25 ... from=-/-/- unsupported=0`; `--keyboard '$kbd'` (C19b) → `keyboard=$kbd repeat_rate=50 ... from=D/-/- unsupported=0`
- `$` in a name is unsupported (never guessed): `--keyboard kbd-a` → `repeat_rate=25 ... from=-/-/- unsupported=2`; `--keyboard '$kbd'` → `repeat_rate=25 ... from=-/-/- unsupported=2`

A real Hyprland config expands `$kbd` to `kbd-a`, so the literal reading silently reports the wrong device.

### A16 — empty device NAME (M, unpinned)
Input (`cases/C18`): `device {\n  name = # none\n  repeat_rate = 50\n}\n` with `--keyboard ""`.
- empty name is a device with NAME `""`: `keyboard= repeat_rate=50 repeat_delay=600 numlock=0 from=D/-/- unsupported=0`
- empty name means no current device: `keyboard= repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=1`

### A17 — device named `*` collides with the default NAME (H, unpinned)
Sentence: "`*` when no `--keyboard`". Input (`cases/C15`, no `--keyboard`): `device {\n  name = *\n  repeat_rate = 50\n}\n`.
- `*` is an ordinary device name (the default line consults it): `keyboard=* repeat_rate=50 repeat_delay=600 numlock=0 from=D/-/- unsupported=0`
- `*` is reserved for the default line: `keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0`

The same divergence appears with `--keyboard '*'` (C16). Recommend the contract reserve `*` or define the default line as not consulting devices.

### A18 — stray `{` line pushes empty text (M, unpinned)
Input (`cases/C31`): `input {\n{\n  repeat_rate = 30\n}\n}\n`.
- push `""` (literal): `repeat_rate=25 ... from=-/-/- unsupported=0`
- reject empty push: `repeat_rate=30 ... from=G/-/- unsupported=0`

The brace count then differs by one, so the second `}` pops or does not pop `input`.

### A19 — `source = …` (M, unpinned)
Sentence: "an LHS equal to `source` [is] ignored"; but the same contract says "everything outside it is `unsupported`, never guessed". Input (`cases/C30`): `source = ~/.config/hypr/extra.conf\n`, whose sourced file sets `repeat_rate`.
- ignored (literal): `repeat_rate=25 ... from=-/-/- unsupported=0`. The output claims a complete answer when the sourced file was never read.
- counted: `repeat_rate=25 ... from=-/-/- unsupported=1`

Recommend counting it.

### A20 — `from` letters and device/global ordering across files (resolved by text, unpinned)
Input (`cases/C17`): file 1 `device {\n  name = kbd-a\n  repeat_rate = 50\n}\n`; file 2 `input {\n  repeat_rate = 30\n}\n`; `--keyboard kbd-a --keyboard kbd-b`.
- literal: `keyboard=kbd-a repeat_rate=50 ... from=D/-/- unsupported=0` and `keyboard=kbd-b repeat_rate=30 ... from=G/-/- unsupported=0`
I could not derive a defensible alternative from the text: the global write does not clear a device value, and "device value if set for NAME" is a statement about the stored value. Listed because the brief asked. Only global-before-device within one file is pinned (F04, F05, F09); device-before-global, within one file or across files, is not.

Related, resolved by text: two `name` lines in one block switch the current device (C38: `kbd-a` → `50 D`; `kbd-b` → `delay=100 -/D/-`). A device key before its block's `name` is unsupported and ignored (C39: `unsupported=1`, value `25 -/-/-`).

---

## 4. Argv

### A21 — empty `--keyboard ""` (M, unpinned)
- accept (NAME is the empty string): `keyboard= repeat_rate=30 repeat_delay=600 numlock=0 from=G/-/- unsupported=0`
- usage: `MADO_KBDOPT: SETUP usage` (rc 2)

### A22 — value starts with `--` (L, unpinned)
Input (`cases/C13`): `--config c.conf --keyboard --getoption`.
- next token is the NAME (two-token form, taken literally): `keyboard=--getoption repeat_rate=30 ... from=G/-/- unsupported=0`
- values may not start with `--`: `MADO_KBDOPT: SETUP usage` (rc 2)

### A23 — `--getoption` twice (M, unpinned)
Sentence: "`--getoption PATH` at most once"; "anything else … is usage". Input (`cases/C14`): `--config c --getoption g1.json --getoption g2.json`.
- at most once → usage: `MADO_KBDOPT: SETUP usage` (rc 2)
- last wins (argparse's default): `keyboard=* repeat_rate=40 ... from=G/-/- unsupported=0`, then `MADO_KBDOPT_LIVE: option=input:repeat_rate config=40 live=41 verdict=DIFFER`, `… repeat_delay … live=? verdict=UNKNOWN`, `… numlock … live=? verdict=UNKNOWN`, `MADO_KBDOPT: DONE keyboards=1 unsupported=0 live=DIFFER` (rc 0)

### A24 — `--selftest` (L, unpinned)
Stdout, rc, and what happens with other arguments are unspecified. The predicate excludes it, so it only matters for operability. Output observed in the model: none defined.

### A25 — usage stdout (M, implementation trap, measured)
The contract requires stdout to be exactly `MADO_KBDOPT: SETUP usage`. An argparse-based implementation writes its usage message to **stderr** and exits 2 with empty stdout (measured: `argparse rc 2 stdout bytes 0`). The contract does not say what stderr may contain. Either forbid stderr or specify it.

---

## 5. Setup and files

### A26 — which setup failure wins (M, unpinned)
Sentence lists four reasons without an order. Input (`cases/C34`): `--config /nonexistent/none.conf --getoption g.json` where `g.json` is `{not json`.
- configs first: `MADO_KBDOPT: SETUP unreadable` (rc 2)
- getoption first: `MADO_KBDOPT: SETUP bad_json` (rc 2)

### A27 — symlinks (M, unpinned)
Sentence: "missing/unreadable/directory/FIFO/non-regular path". Input (`cases/C35`): `--config link.conf`, where `link.conf` → a regular file with `repeat_rate = 30`.
- `stat` (follow): `repeat_rate=30 ... from=G/-/- unsupported=0`
- `lstat`: `MADO_KBDOPT: SETUP unreadable` (rc 2)

### A28 — `too_large` for `--getoption` (M, unpinned)
Sentence: "`too_large` (a file over 1048576 bytes)"; "a file" is generic. Input (`cases/C42`): a 1048577-byte `--getoption` file of newlines.
- applies to every file: `MADO_KBDOPT: SETUP too_large` (rc 2)
- config only: `keyboard=* repeat_rate=40 ... from=G/-/- unsupported=0` plus three `live=?` lines and `DONE … live=UNKNOWN` (rc 0)

### A29 — FIFO and open-before-classify (M, measured, unpinned)
"non-regular path → unreadable" needs classification before opening. A reader that calls `open()` first blocks on a FIFO with no writer. Measured on a scratch FIFO: `stat`-first returns `SETUP unreadable` at once; `open`-first ran to the 5 s `timeout` (rc 124).

### A30 — deep JSON on a `--getoption` line (M, measured, unpinned)
Sentence: "`bad_json` (a non-empty `--getoption` line that is not a JSON object)". Input (`cases/C36`): one line of 200 000 `[` characters.
- Python `json.loads` raises `RecursionError`, not `ValueError`. A parser that catches only `ValueError` dies with an uncaught exception: rc 1, empty stdout, traceback on stderr. Contract requires `SETUP bad_json` with rc 2.
Recommend the contract say "any parse failure, including resource limits".

### A31 — whitespace-only `--getoption` line (L, unpinned)
Sentence: "non-empty". Input (`cases/C33`): `{"option": "input:repeat_rate", "int": 40, "set": true}\n   \n`.
- non-empty = non-zero length: `MADO_KBDOPT: SETUP bad_json` (rc 2)
- non-empty after stripping: `keyboard=* repeat_rate=40 ...`, `live=40 verdict=AGREE`, `DONE … live=UNKNOWN` (rc 0)

### A32 — JSON integers (M, unpinned)
Sentence: "an integer (not boolean) `int`". JSON `40.0` is integer-valued. Input (`cases/C32`): `"int": 40.0`.
- JSON ints only: `MADO_KBDOPT_LIVE: option=input:repeat_rate config=40 live=? verdict=UNKNOWN`
- integer-valued numbers: `live=40 verdict=AGREE`

### A33 — how `--getoption` is decoded (L, unpinned)
The contract specifies UTF-8 with replacement for `--config` and nothing for `--getoption`. A UTF-16 getoption line: `replace`-decoded UTF-8 gives `bad_json` in the model, while `json.loads(bytes)` auto-detects UTF-16 and accepts `{"option": "input:repeat_rate", "int": 30}`. Specify the decoding.

### A34 — the same config passed twice (L, unpinned)
Input (`cases/C41`): `--config c.conf --config c.conf`, where `c.conf` has `numlock_by_default = 2`.
- summed per read: `unsupported=2`
- distinct paths: `unsupported=1`

---

## 6. Resolved or non-divergent (no action beyond stating them)

- **R1 — live compare uses the global value only.** Text: `config=<global effective value>`. Probe: `input {repeat_rate=30}` + `device {name=kbd-a; repeat_rate=50}`, `--keyboard kbd-a --getoption g.json` (`int 30`) gives `keyboard=kbd-a repeat_rate=50 … from=D/-/- unsupported=0`, then `config=30 live=30 verdict=AGREE`. A reader will think the per-keyboard value was verified. It was not. Worth one line in the operator docs.
- **R2 — `"int": true` is excluded.** Explicit in the text.
- **R3 — repeated `--keyboard`** prints one line per argument, `keyboards=` counts arguments. Explicit.
- **R4 — the no-current-device check and the `$`/`##` checks can both fire on one line.** At most one is counted per line and the value is ignored either way, so the output is identical whichever runs first. [INFERENCE from the one-per-line rule; the model order is bracket, no-device, `$`, `##`, value.]
- **R5 — names containing spaces or `=`** print unquoted (`keyboard=a=b c repeat_rate=30 …`, C40). Parseable only by a consumer that knows the NAME set. Operability, not a parse ambiguity.
- **R6 — `unsupported` is run-wide** (text explicit): a line for a device nobody asked about still counts.
- **R7 — `name = X # c` and `#` inside names.** Text: the device NAME is "the RHS with a trailing `#`-comment cut and stripped", so `name = kbd-a # c` gives `kbd-a` and `name = kbd#1` gives `kbd`. Unambiguous as written; unpinned (no fixture names a device with `#`). Consequence: a device whose real name is `kbd#1` can only be requested as `--keyboard kbd`, and the output gives no warning that the name was cut.

---

## 7. Summary for the L1

| ID | Sev | Pinned by fixture? | One-line |
|---|---|---|---|
| A9 | H | no | `-0` accepted by hyprutils `isNumber2`; contract says sign → unsupported (contract ≠ source) |
| A12 | H | **F10** | literal "stack joined with `:`" text is wrong; fixture pins join |
| A2 | H | no | `input { # c` is not a block opener under the literal rule |
| A8 | H | no | "matches" must read fullmatch; source and examples agree |
| A15 | H | no | `name = $kbd` taken verbatim; "never guessed" says unsupported |
| A17 | H | no | device named `*` collides with the default line |
| A13 | H | no | `device {` inside `input {`: exact stack vs innermost |
| A1 | M | no | `} # end` |
| A3 | M | no | indented comment ending in `{`: stripped vs raw |
| A4 | M | no | CR-only files |
| A5 | M | no | `str.strip()` vs the listed set (`\x1c`, NBSP) |
| A6 | M | no | UTF-8 BOM |
| A7 | M | F12 (`##` only) | `$`, `{{`, `\` in comments |
| A14 | M | no | nested bracket vs plain device keys count differently |
| A16 | M | no | empty device name |
| A18 | M | no | stray `{` pushes `""` |
| A19 | M | no | `source = …` silently ignored vs counted |
| A21 | M | no | `--keyboard ""` |
| A23 | M | no | repeated `--getoption` |
| A25 | M | no | argparse writes usage to stderr, stdout empty |
| A26 | M | no | setup-failure precedence |
| A27 | M | no | symlinks |
| A28 | M | no | `too_large` for getoption |
| A29 | M | no | FIFO hangs if opened before classified (measured) |
| A30 | M | no | deep JSON → RecursionError (measured) |
| A32 | M | no | `40.0` is an integer value |
| A11 | L | no | boolean words on integer keys |
| A20 | L | no | device-then-global across files (`from` letter) |
| A22 | L | no | `--keyboard --getoption` |
| A24 | L | no | `--selftest` unspecified |
| A31 | L | no | whitespace-only getoption line |
| A33 | L | no | getoption decoding |
| A34 | L | no | duplicate `--config` count |

Pinned-reading check: all 18 committed fixtures pass under LIT, so no committed fixture contradicts LIT. Only **A12** and the `##` part of **A7** are pinned by a committed fixture. Every other item is unpinned, meaning a parser built to the wrong reading still passes all 18 committed fixtures and the 8 hold-out fixtures can only catch it if they happen to exercise the same input.

Receipts (in `receipts/`): `ref.py` (scratch model), `fixtures_run.py` (fixture pinning), `cases.py` (43 cases, the source of `cases.txt`), `cases.txt` (full stdout for every case and alternative, with committed-fixture failure counts), `cases-stdout.txt` (same, captured run), `fixture-pinning.txt` (LIT 18/18 and every single-switch alternative vs the committed fixtures).
