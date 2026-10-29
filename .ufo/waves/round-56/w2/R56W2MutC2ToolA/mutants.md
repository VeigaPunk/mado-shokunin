# Round 56 w2 - mutation test of `tools/mado-watchplan.py` (seat R56W2MutC2ToolA)

Target: `tools/mado-watchplan.py` at lane revision `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` (lane tip `9c3ca28a59de0dd23ee9950d22349333fc168a11` adds wave-1 evidence only, not the tool).

## Verdict

The committed oracle (the unchanged C2 harness on 18 committed + 8 revealed hold-out fixtures, plus the tool's own
`--selftest`) does **not** pin the tool's config model. 105 one-line mutants were run; 62 are killed by the frozen claim predicate and 43 survive it. Of those survivors, 9 are provably equivalent and **34 are real model defects the frozen predicate accepts**. Each real survivor has a verified killing fixture (below). The predicate is therefore satisfiable by a tool that is wrong in the model registration-v2 §C2 writes down. The defect is in the fixture set, not in the tool at the frozen revision: the pristine tool passes every check.

| measure | count | rate |
|---|---|---|
| mutants generated and run (0 skipped) | 105 | |
| killed by the frozen claim predicate (`MADO_R56_C2 ... TARGET_MET` not printed) | 62 | 59.0% of all |
| killed by the full oracle (claim predicate + `--selftest`) | 77 | 73.3% of all |
| provably equivalent (no observable difference) | 9 | |
| claim-predicate kill rate, equivalents excluded | 62/96 | 64.6% |
| full-oracle kill rate, equivalents excluded | 77/96 | 80.2% |
| claim survivors, non-equivalent (each has a verified killing fixture) | 34 | |
| full-oracle survivors, non-equivalent (undetected by the committed oracle) | 19 | |

Baseline (unmutated tool, same scratch repo): `MADO_R56_C2: rev=4b456d26d02d0f40e19b8303423657b746ee37a0 fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET`; selftest `MADO_WATCH_SELFTEST: 82/82 assertions passed`.

Equivalents: M104, M73, M77, M78, M79, M81, M83, M85, M99.

## Method

- The lane was read at `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` and exported with `git archive | tar -x` into a fresh
  scratch repo `/fast/scratch/hyaku/mado-r56/R56W2MutC2ToolA/repo` (`git -C` asserted to be that dir before the first
  commit; identity `-c user.name=ctl -c user.email=ctl@ctl`). The scratch baseline commit is `d997f00`, so the
  `rev=` field in the harness line differs from the lane revision; the verdicts are what matter. The lane was never
  mutated: each mutant is a one-line change written to a COPY of `tools/mado-watchplan.py` in the scratch repo and
  committed there (`mutate.py`). The pristine bytes were restored and re-checked after the run (`cmp` identical).
- Oracle, unchanged: `python3 -I quality/check-r56-controls.py --claim c2 --repo <scratch> --rev <mutant> --work <scratch>/w`.
  It stages each fixture under `<work>/stage-N/<id>/tree`, runs the tool from an empty cwd inside bwrap, and compares
  stdout bytes and exit status against `expected.out` / `expected.rc` (18 committed, 8 hold-out). The full oracle adds
  the tool's `--selftest`.
- Mutant design: 105 one-line changes in the tool's config model (argument parsing, size/depth bounds, comment and
  brace stack, `=` split, `$`/`{`/backslash/`##` rules, value parsing, source handling, watch list, display root,
  getoption join, counters). Each mutant changes one operator, constant, bound, guard, argument or output field.
- Survivor handling: every claim survivor was attacked with the smallest fixture that separates it from the pristine
  tool. Each proposal was run through the same staged bwrap path (`kill4.py`) and its pristine and mutant outputs
  compared. Killer sets come from the full cross-matrix (`cross.py`: every proposal against every claim survivor), so
  a fixture is credited only when it separates that mutant.
- Equivalence was argued from the code and checked by differential testing (`equiv.py`, in-process differential over a 3,851-case corpus (config bodies x getoption dumps x --home forms x argument shapes)).

## The 9 equivalent mutants (proved, not killed)

| id | mutated line | why no input distinguishes it |
|---|---|---|
| M73 | `if line == "}": ⏎                     if stack: ⏎                         stack.pop()` -> `if line == "}": ⏎                     if len(stack) > 0: ⏎                         stack.pop()` | `if len(stack) > 0` is `if stack` (a list): identical truth value. |
| M77 | `if lhs == "source": ⏎                 if stack:` -> `if lhs == "source": ⏎                 if len(stack) > 0:` | same as M73: `if len(stack) > 0` is `if stack`. |
| M78 | `if "$" in line or "{" in line or "\\" in line or "##" in rhs:` -> `if "$" in line or "{" in line or "\\" in line or "##" in line:` | the mutant tests `##` in `line`, the pristine in `rhs`. A line reaches the OPTION branch only when its key is exactly `misc:disable_autoreload` (empty stack, lhs = OPTION) or `misc:disable_autoreload` with stack `[misc]` (lhs = `disable_autoreload`). Neither lhs contains `#`, and the stack text `misc` contains no `#`, so `##` in `line` holds iff it holds in `rhs`. |
| M79 | `if "$" in line or "{" in line or "\\" in line or "##" in rhs:` -> `if "$" in rhs or "{" in line or "\\" in line or "##" in rhs:` | same argument for `$`: the OPTION branch's lhs and stack contain no `$`, so `$` in `line` iff `$` in `rhs`. |
| M81 | `if lhs.startswith("$"): ⏎                 continue` -> `if lhs.startswith("$") and len(lhs) > 1: ⏎                 continue` | the mutant does not skip an lhs equal to `$` alone. That line's key is `$` or `<stack>:$`, never OPTION, so the mutant's fall-through to `if key != OPTION: continue` discards it with no side effect. The pristine `continue` discards it too. |
| M83 | `if not matches: ⏎             self.event_error(via, raw, "nomatch") ⏎             return` -> `if not matches: ⏎             self.event_error(via, raw, "nomatch")` | the mutant drops `return` after `nomatch`. `matches` is then empty and the following `for` loop has no body. |
| M85 | `target = absolute_path(match, cur, self.home) if match else match` -> `target = absolute_path(match, cur, self.home)` | the mutant drops `if match else match`. `glob` never yields the empty string, and `VALUE` is absolute (the `--config` path is absolute), so every match is absolute and `absolute_path(match)` is the identity. |
| M99 | `return live.get(OPTION)` -> `return live.get(OPTION, None)` | `dict.get(k)` and `dict.get(k, None)` return the same value. |
| M104 | `verdict = "UNKNOWN" if live is None else ("AGREE" if live == config_flag else "DIFFER")` -> `verdict = "UNKNOWN" if live is None else ("AGREE" if live == int(config_flag) else "DIFFER")` | `config_flag` is already an int, so `int(config_flag)` is the same int. |

Corpus check for the same nine (`equiv-results.json`): zero differences over 3,851 cases for each of M73, M77, M78, M79, M81, M83, M85, M99, M104. The corpus check did not run on M80 or M96 as equivalent: M80 is a real defect (`on$x` is accepted as 1) and M96 is killed by K57 (see below), so neither is in this set.

## Real survivors of the frozen claim predicate (34)

These mutants print `MADO_R56_C2: ... verdict=TARGET_MET` on the unchanged oracle, so the frozen predicate does not
falsify them. Each is separated from the pristine tool by a fixture listed in the last column (verified in
`receipts/kill-<K>.txt`).

| id | mutated line | full-oracle | killing fixtures (verified) |
|---|---|---|---|
| M04 | `if not value.startswith("/"): ⏎             raise Setup("usage")` -> `if not value.startswith("/") and False: ⏎             raise Setup("usage")` | selftest catches | K04 |
| M06 | `MAX_BYTES = 1048576` -> `MAX_BYTES = 1048575` | selftest catches | K06 |
| M07 | `MAX_BYTES = 1048576` -> `MAX_BYTES = 1048577` | selftest catches | K07 |
| M100 | `if not line: ⏎             continue ⏎         try:` -> `if not line: ⏎             continue ⏎         if line.startswith("#"): ⏎             continue ⏎         try:` | undetected | K100 |
| M101 | `if isinstance(option, str) and type(value) is int: ⏎             live[option] = value` -> `if isinstance(option, str) and type(value) is int and value >= 0: ⏎             live[option] = value` | undetected | K101 |
| M11 | `if len(data) > MAX_BYTES: ⏎         raise Setup("too_large")` -> `if len(data) >= MAX_BYTES: ⏎         raise Setup("too_large")` | selftest catches | K11 |
| M12 | `data = fh.read(MAX_BYTES + 1)` -> `data = fh.read(MAX_BYTES)` | selftest catches | K12 |
| M16 | `if not line or line[0] == "#": ⏎                 continue` -> `if not line or line[0] == ";": ⏎                 continue` | undetected | K16, K17, K71 |
| M17 | `if not line or line[0] == "#": ⏎                 continue` -> `if not line: ⏎                 continue` | undetected | K16, K17 |
| M18 | `if line == "}": ⏎                     if stack: ⏎                         stack.pop()` -> `if line == "}": ⏎                     if stack is not None: ⏎                         stack.pop()` | selftest catches | K18 |
| M26 | `ok, number_text = config_int(rhs.split("#", 1)[0].strip(WS))` -> `ok, number_text = config_int(rhs.split("#", 1)[0])` | selftest catches | K26 |
| M27 | `if "$" in line or "{" in line or "\\" in line or "##" in rhs:` -> `if "{" in line or "\\" in line or "##" in rhs:` | undetected | K27 |
| M28 | `if "$" in line or "{" in line or "\\" in line or "##" in rhs:` -> `if "$" in line or "\\" in line or "##" in rhs:` | undetected | K28 |
| M29 | `if "$" in line or "{" in line or "\\" in line or "##" in rhs:` -> `if "$" in line or "{" in line or "##" in rhs:` | undetected | K29 |
| M33 | `if DIGITS.fullmatch(value):` -> `if DIGITS.match(value):` | selftest catches | K33 |
| M44 | `self.event_error(via, raw, "inaccessible") ⏎                 return` -> `self.event_error(via, raw, "inaccessible") ⏎                 continue` | undetected | K44 |
| M50 | `elif os.path.lexists(path): ⏎                 kind, mask = "file", MASK_FILE` -> `elif os.path.exists(path): ⏎                 kind, mask = "file", MASK_FILE` | undetected | K50, K89, K90 |
| M54 | `out.append(("primary", path, kind, mask, via))` -> `out.append(("primary", path, kind, MASK_FILE, via))` | selftest catches | K54 |
| M55 | `if path == prefix or path.startswith(prefix + "/"):` -> `if path.startswith(prefix):` | selftest catches | K55 |
| M56 | `given = root[:-1] if root.endswith("/") else root` -> `given = root` | undetected | K56 |
| M57 | `self.prefixes.append(os.path.realpath(root))` -> `self.prefixes.append(root)` | selftest catches | K57 |
| M60 | `if isinstance(option, str) and type(value) is int: ⏎             live[option] = value` -> `if isinstance(option, str) and isinstance(value, int): ⏎             live[option] = value` | selftest catches | K60 |
| M62 | `return live.get(OPTION)` -> `return live.get(OPTION, 0)` | selftest catches | K62 |
| M63 | `if not stat.S_ISREG(os.stat(path).st_mode): ⏎             raise Setup("unreadable")` -> `if False: ⏎             raise Setup("unreadable")` | undetected | K63, K97 |
| M71 | `if not line or line[0] == "#": ⏎                 continue` -> `if not line or line[0] == "#" or line[0] == ";": ⏎                 continue` | undetected | K71 |
| M76 | `lhs, rhs = lhs.strip(WS), rhs.strip(WS)` -> `lhs, rhs = lhs.strip(WS), rhs.strip(WS + "!")` | undetected | K76 |
| M80 | `if "$" in line or "{" in line or "\\" in line or "##" in rhs:` -> `if "$" in line[0:1] or "{" in line or "\\" in line or "##" in rhs:` | undetected | K27 |
| M89 | `elif os.path.lexists(path): ⏎                 kind, mask = "file", MASK_FILE` -> `elif os.path.isfile(path): ⏎                 kind, mask = "file", MASK_FILE` | undetected | K50, K89, K90 |
| M90 | `if os.path.islink(path): ⏎                 try: ⏎                     canonical = os.path.realpath(path, strict=True)` -> `if os.path.islink(path): ⏎                 try: ⏎                     canonical = os.path.realpath(path)` | undetected | K50, K89, K90 |
| M93 | `if os.path.isdir(path): ⏎                 kind, mask = "dir", MASK_DIR` -> `if os.path.isdir(path): ⏎                 kind, mask = "dir", MASK_DIR if False else MASK_FILE` | selftest catches | K93 |
| M94 | `given = root[:-1] if root.endswith("/") else root` -> `given = root[:-1] if root.endswith("/") else root + "/"` | undetected | K94, K96 |
| M96 | `self.prefixes.append(os.path.realpath(root))` -> `self.prefixes.append(os.path.realpath(root) + "/")` | selftest catches | K57 |
| M97 | `if not stat.S_ISREG(os.stat(path).st_mode): ⏎             raise Setup("unreadable")` -> `if not stat.S_ISREG(os.stat(path).st_mode) and stat.S_ISDIR(os.stat(path).st_mode): ⏎             raise Setup("unreadable")` | undetected | K63, K97 |
| M98 | `option, value = obj.get("option"), obj.get("int")` -> `option, value = obj.get("option"), obj.get("int", obj.get("value"))` | undetected | K98 |

Of these, 19 are also undetected by `--selftest` (the tool's own selftest passes on them), so no test in the lane catches them: M100, M101, M16, M17, M27, M28, M29, M44, M50, M56, M63, M71, M76, M80, M89, M90, M94, M97, M98.

## Proposed additions: greedy cover of the real survivors (not proven minimum)

Greedy set cover over the killer sets above. Each chosen fixture kills every mutant listed against it. The fixtures
are in `receipts/kill-<K>.txt`. Adding any of them changes the C2 harness counts (18 to 19, etc.), so they are a
pre-data re-registration (new versioned file, as registration-v2 requires), not a silent edit of the committed set.

| fixture | kills | what it puts in the tree / args |
|---|---|---|
| K50 | M50, M89, M90 | a dangling symlink --config lexists -> type=file, not type=missing |
| K16 | M16, M17 | a full-line comment is skipped and must not push the category stack |
| K27 | M27, M80 | a `$` in the value line is unsupported: `on$x` must not parse as 1 |
| K57 | M57, M96 | the canonical watch path is printed through the display root's realpath |
| K63 | M63, M97 | --getoption on a non-regular but readable file is `unreadable` |
| K04 | M04 | a relative --config path is a usage error |
| K06 | M06 | a file of exactly 1048576 bytes is read (MAX_BYTES is inclusive) |
| K07 | M07 | a file of 1048577 bytes is too_large (MAX_BYTES is inclusive) |
| K11 | M11 | a file of exactly 1048576 bytes is read (the bound is `>` not `>=`) |
| K12 | M12 | a file of 1048577 bytes is too_large (the read takes MAX_BYTES+1) |
| K18 | M18 | a stray `}` on an empty stack is ignored (no crash) |
| K26 | M26 | the value is stripped of spaces before parsing (`1 # x` -> 1) |
| K28 | M28 | a `{` in the value line is unsupported: `on{` must not parse as 1 |
| K29 | M29 | a backslash in the value line is unsupported: `off\` must not parse as 0 |
| K33 | M33 | a value that only STARTS with digits is not an int |
| K44 | M44 | an inaccessible match aborts the REST of that line's matches (dangling symlink first) |
| K54 | M54 | a directory watch carries the directory mask |
| K55 | M55 | --display-root is a PATH prefix, not a string prefix |
| K56 | M56 | --display-root that is a symlink path with a trailing slash (the given text loses its `/`) |
| K60 | M60 | a bool `int` in the getoption dump is ignored (UNKNOWN, not AGREE) |
| K62 | M62 | no record for the option in the dump is UNKNOWN, not AGREE |
| K71 | M71 | a `;`-first line is NOT a comment: it is an ordinary line |
| K76 | M76 | the value side of `=` is not stripped of `!` |
| K93 | M93 | a directory watch carries the directory mask |
| K94 | M94 | --display-root without a trailing slash is used as given |
| K98 | M98 | the live value comes from the `int` key only |
| K100 | M100 | a `#`-first line in the --getoption dump is NOT skipped: it is bad_json |
| K101 | M101 | a negative live int is still a record (the option is present) |

28 fixtures cover all 34 real claim survivors.

## Full mutant table (all 105)

`kill` column: the claim harness (`C2`) or `--selftest` (`st`) flags the mutant; `-` = neither. `class`: `E` =
equivalent, `K` = killable by a new fixture (listed), `-` = already killed.

| id | area | mutated line (old -> new) | claim | selftest | kill | class | killers |
|---|---|---|---|---|---|---|---|
| M01 | args | `if len(argv) % 2: ⏎         raise Setup("usage")` -> `if len(argv) % 2 == 0: ⏎         raise Setup("usage")` | miss | FAIL | C2 | - | NONE |
| M02 | args | `if flag not in ("--config", "--home", "--display-root", "--getoption") or flag in opts:` -> `if flag not in ("--config", "--home", "--display-root", "--getoption"):` | miss | FAIL | C2 | - | NONE |
| M03 | args | `if "--config" not in opts: ⏎         raise Setup("usage")` -> `if "--config" in opts: ⏎         raise Setup("usage")` | miss | FAIL | C2 | - | NONE |
| M04 | args | `if not value.startswith("/"): ⏎             raise Setup("usage")` -> `if not value.startswith("/") and False: ⏎             raise Setup("usage")` | TARGET_MET | FAIL | st | K | K04 |
| M05 | args | `if flag not in ("--config", "--home", "--display-root", "--getoption") or flag in opts:` -> `if flag not in ("--config", "--home", "--display-root", "--getoption") or opts:` | miss | FAIL | C2 | - | NONE |
| M06 | bounds | `MAX_BYTES = 1048576` -> `MAX_BYTES = 1048575` | TARGET_MET | FAIL | st | K | K06 |
| M07 | bounds | `MAX_BYTES = 1048576` -> `MAX_BYTES = 1048577` | TARGET_MET | FAIL | st | K | K07 |
| M08 | bounds | `MAX_DEPTH = 16` -> `MAX_DEPTH = 15` | miss | FAIL | C2 | - | NONE |
| M09 | bounds | `MAX_DEPTH = 16` -> `MAX_DEPTH = 17` | miss | FAIL | C2 | - | NONE |
| M10 | bounds | `MAX_ENTRIES = 262144` -> `MAX_ENTRIES = 16` | miss | FAIL | C2 | - | NONE |
| M11 | bounds | `if len(data) > MAX_BYTES: ⏎         raise Setup("too_large")` -> `if len(data) >= MAX_BYTES: ⏎         raise Setup("too_large")` | TARGET_MET | FAIL | st | K | K11 |
| M12 | bounds | `data = fh.read(MAX_BYTES + 1)` -> `data = fh.read(MAX_BYTES)` | TARGET_MET | FAIL | st | K | K12 |
| M13 | bounds | `if depth + 1 > MAX_DEPTH:` -> `if depth + 1 >= MAX_DEPTH:` | miss | FAIL | C2 | - | NONE |
| M14 | bounds | `if depth + 1 > MAX_DEPTH:` -> `if depth + 1 > MAX_DEPTH + 1:` | miss | FAIL | C2 | - | NONE |
| M15 | bounds | `self.parse_file(target, depth + 1)` -> `self.parse_file(target, depth)` | miss | FAIL | C2 | - | NONE |
| M16 | stack | `if not line or line[0] == "#": ⏎                 continue` -> `if not line or line[0] == ";": ⏎                 continue` | TARGET_MET | pass | - | K | K16, K17, K71 |
| M17 | stack | `if not line or line[0] == "#": ⏎                 continue` -> `if not line: ⏎                 continue` | TARGET_MET | pass | - | K | K16, K17 |
| M18 | stack | `if line == "}": ⏎                     if stack: ⏎                         stack.pop()` -> `if line == "}": ⏎                     if stack is not None: ⏎                         stack.pop()` | TARGET_MET | FAIL | st | K | K18 |
| M19 | stack | `elif line.endswith("{"): ⏎                     stack.append(line[:-1].strip(WS))` -> `elif line.endswith("{"): ⏎                     stack.append(line[:-1])` | miss | FAIL | C2 | - | NONE |
| M20 | stack | `elif line.endswith("{"): ⏎                     stack.append(line[:-1].strip(WS))` -> `elif line.startswith("{"): ⏎                     stack.append(line[:-1].strip(WS))` | miss | FAIL | C2 | - | NONE |
| M21 | stack | `key = ":".join(stack) + ":" + lhs if stack else lhs` -> `key = ":".join(stack) + ":" + lhs` | miss | FAIL | C2 | - | NONE |
| M22 | stack | `if lhs == "source": ⏎                 if stack:` -> `if lhs == "source": ⏎                 if not stack:` | miss | FAIL | C2 | - | NONE |
| M23 | eqsplit | `lhs, _, rhs = line.partition("=") ⏎             lhs, rhs = lhs.strip(WS), rhs.strip(WS)` -> `rhs, _, lhs = line.partition("=") ⏎             lhs, rhs = lhs.strip(WS), rhs.strip(WS)` | miss | FAIL | C2 | - | NONE |
| M24 | eqsplit | `lhs, _, rhs = line.partition("=") ⏎             lhs, rhs = lhs.strip(WS), rhs.strip(WS)` -> `lhs, _, rhs = line.partition("=") ⏎             lhs, rhs = rhs.strip(WS), lhs.strip(WS)` | miss | FAIL | C2 | - | NONE |
| M25 | eqsplit | `self.source(rhs.split("#", 1)[0].strip(WS), path, number, depth)` -> `self.source(rhs.split("#", 1)[0], path, number, depth)` | miss | pass | C2 | - | - |
| M26 | eqsplit | `ok, number_text = config_int(rhs.split("#", 1)[0].strip(WS))` -> `ok, number_text = config_int(rhs.split("#", 1)[0])` | TARGET_MET | FAIL | st | K | K26 |
| M27 | unsupported | `if "$" in line or "{" in line or "\\" in line or "##" in rhs:` -> `if "{" in line or "\\" in line or "##" in rhs:` | TARGET_MET | pass | - | K | K27 |
| M28 | unsupported | `if "$" in line or "{" in line or "\\" in line or "##" in rhs:` -> `if "$" in line or "\\" in line or "##" in rhs:` | TARGET_MET | pass | - | K | K28 |
| M29 | unsupported | `if "$" in line or "{" in line or "\\" in line or "##" in rhs:` -> `if "$" in line or "{" in line or "##" in rhs:` | TARGET_MET | pass | - | K | K29 |
| M30 | unsupported | `if "$" in line or "{" in line or "\\" in line or "##" in rhs:` -> `if "$" in line or "{" in line or "\\" in line:` | miss | pass | C2 | - | - |
| M31 | value | `if value.startswith(("true", "on", "yes")):` -> `if value.startswith(("true", "on")):` | miss | FAIL | C2 | - | NONE |
| M32 | value | `if value.startswith(("false", "off", "no")):` -> `if value.startswith(("false", "off")):` | miss | FAIL | C2 | - | NONE |
| M33 | value | `if DIGITS.fullmatch(value):` -> `if DIGITS.match(value):` | TARGET_MET | FAIL | st | K | K33 |
| M34 | value | `return True, value.lstrip("0") or "0"` -> `return True, value.lstrip("0")` | miss | FAIL | C2 | - | NONE |
| M35 | value | `return False, ""` -> `return True, "0"` | miss | FAIL | C2 | - | NONE |
| M36 | value | `off = value is not None and bool(value.strip("0"))` -> `off = value is not None and bool(value)` | miss | FAIL | C2 | - | NONE |
| M37 | value | `if self.value is not None and self.value.strip("0"):` -> `if self.value is not None:` | miss | pass | C2 | - | - |
| M38 | value | `if ok: ⏎                 self.value = number_text` -> `if ok and number_text != "0": ⏎                 self.value = number_text` | miss | FAIL | C2 | - | NONE |
| M39 | source | `if len(raw) < 2: ⏎             self.event_error(via, raw, "bogus")` -> `if len(raw) < 1: ⏎             self.event_error(via, raw, "bogus")` | miss | FAIL | C2 | - | NONE |
| M40 | source | `if len(raw) < 2: ⏎             self.event_error(via, raw, "bogus")` -> `if len(raw) < 3: ⏎             self.event_error(via, raw, "bogus")` | miss | pass | C2 | - | - |
| M41 | source | `if (raw[0] == "~" and self.home is None) or "\\" in raw:` -> `if (raw[0] == "~" and self.home is None):` | miss | FAIL | C2 | - | NONE |
| M42 | source | `matches = expand(absolute_path(raw, cur, self.home))` -> `matches = expand(raw)` | miss | FAIL | C2 | - | NONE |
| M43 | source | `if not matches: ⏎             self.event_error(via, raw, "nomatch")` -> `if matches is None: ⏎             self.event_error(via, raw, "nomatch")` | miss | FAIL | C2 | - | NONE |
| M44 | source | `self.event_error(via, raw, "inaccessible") ⏎                 return` -> `self.event_error(via, raw, "inaccessible") ⏎                 continue` | TARGET_MET | pass | - | K | K44 |
| M45 | source | `self.event_error(via, raw, "inaccessible") ⏎                 return` -> `self.event_error(via, raw, "nomatch") ⏎                 return` | miss | FAIL | C2 | - | NONE |
| M46 | source | `elif stat.S_ISDIR(mode):` -> `elif stat.S_ISREG(mode):` | miss | FAIL | C2 | - | NONE |
| M47 | source | `self.events.append("MADO_WATCH: SKIP via=%s path=%s reason=directory" % (via, self.show(target)))` -> `self.events.append("MADO_WATCH: SKIP via=%s path=%s reason=nonregular" % (via, self.show(target)))` | miss | FAIL | C2 | - | NONE |
| M48 | source | `via = "%s:%d" % (self.show(cur), number)` -> `via = "%s:%d" % (cur, number)` | miss | FAIL | C2 | - | NONE |
| M49 | watch | `if os.path.isdir(path): ⏎                 kind, mask = "dir", MASK_DIR` -> `if os.path.isfile(path): ⏎                 kind, mask = "dir", MASK_DIR` | miss | FAIL | C2 | - | NONE |
| M50 | watch | `elif os.path.lexists(path): ⏎                 kind, mask = "file", MASK_FILE` -> `elif os.path.exists(path): ⏎                 kind, mask = "file", MASK_FILE` | TARGET_MET | pass | - | K | K50, K89, K90 |
| M51 | watch | `kind, mask = "missing", MASK_FILE` -> `kind, mask = "missing", MASK_DIR` | miss | FAIL | C2 | - | NONE |
| M52 | watch | `if os.path.islink(path): ⏎                 try:` -> `if not os.path.islink(path): ⏎                 try:` | miss | FAIL | C2 | - | NONE |
| M53 | watch | `out.append(("canonical", canonical, "file", MASK_CANON, via))` -> `out.append(("primary", canonical, "file", MASK_CANON, via))` | miss | FAIL | C2 | - | NONE |
| M54 | watch | `out.append(("primary", path, kind, mask, via))` -> `out.append(("primary", path, kind, MASK_FILE, via))` | TARGET_MET | FAIL | st | K | K54 |
| M55 | display | `if path == prefix or path.startswith(prefix + "/"):` -> `if path.startswith(prefix):` | TARGET_MET | FAIL | st | K | K55 |
| M56 | display | `given = root[:-1] if root.endswith("/") else root` -> `given = root` | TARGET_MET | pass | - | K | K56 |
| M57 | display | `self.prefixes.append(os.path.realpath(root))` -> `self.prefixes.append(root)` | TARGET_MET | FAIL | st | K | K57 |
| M58 | display | `plan.show(plan.config), "off" if off else "on",` -> `plan.config, "off" if off else "on",` | miss | FAIL | C2 | - | NONE |
| M59 | live | `if not isinstance(obj, dict): ⏎             raise Setup("bad_json")` -> `if not isinstance(obj, (dict, list)): ⏎             raise Setup("bad_json")` | miss | FAIL | C2 | - | NONE |
| M60 | live | `if isinstance(option, str) and type(value) is int: ⏎             live[option] = value` -> `if isinstance(option, str) and isinstance(value, int): ⏎             live[option] = value` | TARGET_MET | FAIL | st | K | K60 |
| M61 | live | `live[option] = value` -> `live.setdefault(option, value)` | miss | FAIL | C2 | - | NONE |
| M62 | live | `return live.get(OPTION)` -> `return live.get(OPTION, 0)` | TARGET_MET | FAIL | st | K | K62 |
| M63 | live | `if not stat.S_ISREG(os.stat(path).st_mode): ⏎             raise Setup("unreadable")` -> `if False: ⏎             raise Setup("unreadable")` | TARGET_MET | pass | - | K | K63, K97 |
| M64 | counters | `len(plan.entries), plan.unsupported, plan.errors)]` -> `len(plan.entries) + 1, plan.unsupported, plan.errors)]` | miss | FAIL | C2 | - | NONE |
| M65 | counters | `len(plan.entries), plan.unsupported, plan.errors)]` -> `len(plan.entries), plan.errors, plan.errors)]` | miss | FAIL | C2 | - | NONE |
| M66 | counters | `len(plan.entries), plan.unsupported, plan.errors)]` -> `len(plan.entries), plan.unsupported, plan.unsupported)]` | miss | FAIL | C2 | - | NONE |
| M67 | counters | `len(watches), plan.unsupported, plan.errors, verdict))` -> `len(plan.entries), plan.unsupported, plan.errors, verdict))` | miss | FAIL | C2 | - | NONE |
| M68 | counters | `len(watches), plan.unsupported, plan.errors, verdict))` -> `len(watches), plan.errors, plan.errors, verdict))` | miss | FAIL | C2 | - | NONE |
| M69 | counters | `verdict = "UNKNOWN" if live is None else ("AGREE" if live == config_flag else "DIFFER")` -> `verdict = "UNKNOWN" if live is None else ("AGREE" if live != config_flag else "DIFFER")` | miss | FAIL | C2 | - | NONE |
| M70 | counters | `config_flag = 1 if off else 0` -> `config_flag = 0 if off else 1` | miss | FAIL | C2 | - | NONE |
| M71 | stack | `if not line or line[0] == "#": ⏎                 continue` -> `if not line or line[0] == "#" or line[0] == ";": ⏎                 continue` | TARGET_MET | pass | - | K | K71 |
| M72 | stack | `if not line or line[0] == "#": ⏎                 continue` -> `if not line or line[0] == "#" or len(line) == 1: ⏎                 continue` | miss | FAIL | C2 | - | NONE |
| M73 | stack | `if line == "}": ⏎                     if stack: ⏎                         stack.pop()` -> `if line == "}": ⏎                     if len(stack) > 0: ⏎                         stack.pop()` | TARGET_MET | pass | - | E | NONE |
| M74 | stack | `elif line.endswith("{"): ⏎                     stack.append(line[:-1].strip(WS))` -> `elif line.endswith("{"): ⏎                     stack.append(line[:-1].strip(WS)) ⏎                     stack.append("")` | miss | FAIL | C2 | - | NONE |
| M75 | stack | `key = ":".join(stack) + ":" + lhs if stack else lhs` -> `key = ":".join(stack) + ":" + lhs if stack else ":" + lhs` | miss | FAIL | C2 | - | NONE |
| M76 | stack | `lhs, rhs = lhs.strip(WS), rhs.strip(WS)` -> `lhs, rhs = lhs.strip(WS), rhs.strip(WS + "!")` | TARGET_MET | pass | - | K | K76 |
| M77 | stack | `if lhs == "source": ⏎                 if stack:` -> `if lhs == "source": ⏎                 if len(stack) > 0:` | TARGET_MET | pass | - | E | NONE |
| M78 | unsupported | `if "$" in line or "{" in line or "\\" in line or "##" in rhs:` -> `if "$" in line or "{" in line or "\\" in line or "##" in line:` | TARGET_MET | pass | - | E | NONE |
| M79 | unsupported | `if "$" in line or "{" in line or "\\" in line or "##" in rhs:` -> `if "$" in rhs or "{" in line or "\\" in line or "##" in rhs:` | TARGET_MET | pass | - | E | NONE |
| M80 | unsupported | `if "$" in line or "{" in line or "\\" in line or "##" in rhs:` -> `if "$" in line[0:1] or "{" in line or "\\" in line or "##" in rhs:` | TARGET_MET | pass | - | K | K27 |
| M81 | unsupported | `if lhs.startswith("$"): ⏎                 continue` -> `if lhs.startswith("$") and len(lhs) > 1: ⏎                 continue` | TARGET_MET | pass | - | E | NONE |
| M82 | unsupported | `if lhs.startswith("$"): ⏎                 continue` -> `if lhs.startswith("$"): ⏎                 self.unsupported += 1 ⏎                 continue` | miss | pass | C2 | - | - |
| M83 | source | `if not matches: ⏎             self.event_error(via, raw, "nomatch") ⏎             return` -> `if not matches: ⏎             self.event_error(via, raw, "nomatch")` | TARGET_MET | pass | - | E | NONE |
| M84 | source | `matches = expand(absolute_path(raw, cur, self.home)) ⏎         if not matches:` -> `matches = expand(absolute_path(raw, cur, self.home)) ⏎         matches = list(reversed(matches)) ⏎         if not matches:` | miss | pass | C2 | - | - |
| M85 | source | `target = absolute_path(match, cur, self.home) if match else match` -> `target = absolute_path(match, cur, self.home)` | TARGET_MET | pass | - | E | NONE |
| M86 | source | `mode = os.stat(target).st_mode` -> `mode = os.lstat(target).st_mode` | miss | FAIL | C2 | K | K44, K57, K86 |
| M87 | source | `if stat.S_ISREG(mode): ⏎                 self.add_entry(target, via)` -> `if stat.S_ISREG(mode): ⏎                 self.add_entry(target, via) ⏎                 self.events.append("MADO_WATCH: SKIP via=%s path=%s reason=nonregular" % (via, self.show(target)))` | miss | FAIL | C2 | - | NONE |
| M88 | source | `if (raw[0] == "~" and self.home is None) or "\\" in raw:` -> `if (raw[0] == "~" and self.home is None) or "\\" in raw or "/" in raw:` | miss | FAIL | C2 | - | NONE |
| M89 | watch | `elif os.path.lexists(path): ⏎                 kind, mask = "file", MASK_FILE` -> `elif os.path.isfile(path): ⏎                 kind, mask = "file", MASK_FILE` | TARGET_MET | pass | - | K | K50, K89, K90 |
| M90 | watch | `if os.path.islink(path): ⏎                 try: ⏎                     canonical = os.path.realpath(path, strict=True)` -> `if os.path.islink(path): ⏎                 try: ⏎                     canonical = os.path.realpath(path)` | TARGET_MET | pass | - | K | K50, K89, K90 |
| M91 | watch | `out.append(("canonical", canonical, "file", MASK_CANON, via))` -> `out.append(("canonical", canonical, "file", MASK_CANON, "main")` | miss | FAIL | C2 | - | NONE |
| M92 | watch | `out.append(("primary", path, kind, mask, via))` -> `out.append(("primary", path, kind, mask, via)) ⏎             if os.path.islink(path): ⏎                 out.append(("canonical", path, "file", MASK_CANON, via))` | miss | FAIL | C2 | - | NONE |
| M93 | watch | `if os.path.isdir(path): ⏎                 kind, mask = "dir", MASK_DIR` -> `if os.path.isdir(path): ⏎                 kind, mask = "dir", MASK_DIR if False else MASK_FILE` | TARGET_MET | FAIL | st | K | K93 |
| M94 | display | `given = root[:-1] if root.endswith("/") else root` -> `given = root[:-1] if root.endswith("/") else root + "/"` | TARGET_MET | pass | - | K | K94, K96 |
| M95 | display | `if path == prefix or path.startswith(prefix + "/"): ⏎                 return "$ROOT" + path[len(prefix):]` -> `if path == prefix or path.startswith(prefix + "/"): ⏎                 return "$ROOT" + path[len(prefix) + 1:]` | miss | FAIL | C2 | - | NONE |
| M96 | display | `self.prefixes.append(os.path.realpath(root))` -> `self.prefixes.append(os.path.realpath(root) + "/")` | TARGET_MET | FAIL | st | K | K57 |
| M97 | live | `if not stat.S_ISREG(os.stat(path).st_mode): ⏎             raise Setup("unreadable")` -> `if not stat.S_ISREG(os.stat(path).st_mode) and stat.S_ISDIR(os.stat(path).st_mode): ⏎             raise Setup("unreadable")` | TARGET_MET | pass | - | K | K63, K97 |
| M98 | live | `option, value = obj.get("option"), obj.get("int")` -> `option, value = obj.get("option"), obj.get("int", obj.get("value"))` | TARGET_MET | pass | - | K | K98 |
| M99 | live | `return live.get(OPTION)` -> `return live.get(OPTION, None)` | TARGET_MET | pass | - | E | NONE |
| M100 | live | `if not line: ⏎             continue ⏎         try:` -> `if not line: ⏎             continue ⏎         if line.startswith("#"): ⏎             continue ⏎         try:` | TARGET_MET | pass | - | K | K100 |
| M101 | live | `if isinstance(option, str) and type(value) is int: ⏎             live[option] = value` -> `if isinstance(option, str) and type(value) is int and value >= 0: ⏎             live[option] = value` | TARGET_MET | pass | - | K | K101 |
| M102 | counters | `len(plan.entries), plan.unsupported, plan.errors)]` -> `len(plan.entries), plan.unsupported, plan.errors + 1)]` | miss | FAIL | C2 | - | NONE |
| M103 | counters | `len(watches), plan.unsupported, plan.errors, verdict))` -> `len(watches), plan.unsupported + 1, plan.errors, verdict))` | miss | FAIL | C2 | - | NONE |
| M104 | counters | `verdict = "UNKNOWN" if live is None else ("AGREE" if live == config_flag else "DIFFER")` -> `verdict = "UNKNOWN" if live is None else ("AGREE" if live == int(config_flag) else "DIFFER")` | TARGET_MET | pass | - | E | NONE |
| M105 | counters | `for k, (role, path, kind, mask, via) in enumerate(watches, 1):` -> `for k, (role, path, kind, mask, via) in enumerate(watches, 0):` | miss | FAIL | C2 | - | NONE |

## Notes on the proposals that did not kill (kept for the record)

`receipts/kill-<K>.txt` also holds the first proposals I wrote, which missed: K73, K77, K78, K79, K81, K83, K85, K99,
K104 (their mutants are provably equivalent) and K80 and K96 (mis-targeted: K80 used an LHS `$` the mutant never
reads; K96 used a display root whose realpath prefix was not reached). M80 is killed by K27 and M96 by K57, both in
the cross-matrix. K60 was first written with a typo in its config line (`misc:disable_autoridl`); it was corrected to
`misc:disable_autoreload = 0` and re-verified (it kills M60).

## Restoration and what did not run

- Restoration: after the 105-mutant run `tools/mado-watchplan.py` in the scratch repo was rewritten from the pristine
  bytes and committed; `cmp` against the `git show HEAD:` blob succeeds (see `receipts/run.log`). The lane was not touched.
- Not verified: the harness's bwrap staging was reproduced by copying its `staged_run` command line; the harness run
  itself was used for every oracle verdict. The fixtures in 'Proposed additions' were run through my own copy of the
  staging, not through the harness's `score()` (the harness counts are fixed at 18/8 and would reject additions).
- Not run: no `pacman`/install; the tools used (`python3` 3.14, `git`, `tar`, `bwrap`) were already present.

## Deliverables (this directory)

- `mutants.md` (this file), generated by `report.py` from the receipts below.
- driver: `mutate.py` (105-entry mutant list and the oracle loop), `kill4.py` (killing-fixture transcripts),
  `kill2.py` (fixture definitions), `extra.py` (two later fixtures), `cross.py` (cross-kill matrix), `equiv.py`
  (equivalence corpus), `report.py` (this table).
- receipts: `receipts/<M##>.txt` (one per mutant: the mutated bytes' sha256, the blob, the oracle line, selftest rc),
  `receipts/kill-<K##>.txt` (one per killing fixture: both outputs), `results.json`, `results.tsv`,
  `cross-matrix.json`, `kill-results.json`, `equiv-results.json`, `baseline.txt`, `run.log`.

