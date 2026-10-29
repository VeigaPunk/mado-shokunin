# R56W2MutC2ToolB — mutation test of `tools/mado-watchplan.py`

Rev `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` (tool blob sha256 `ed6ee9f200cdc0646fb2f31898f37a2570318a7609d91c7cd730c501c1aa9379`).
Mutants are edited in COPIES inside `/fast/scratch/hyaku/mado-r56/R56W2MutC2ToolB/`; the lane was read with `git show`/`git archive` only.

## 1. Result

| | count |
|---|---|
| one-line mutants generated (every anchor unique, every mutant changes exactly one line) | 117 |
| KILLED by the unchanged oracle (tool `--selftest` 82 assertions, and/or C2 harness `TARGET_MET` on 18+8 fixtures) | 82 (70.1%) |
| SURVIVED | 35 |
| &nbsp;&nbsp;EQUIVALENT (argued, §3.1) | 10 |
| &nbsp;&nbsp;non-equivalent, killed by a proposed staged fixture verified through the harness path (§4) | 23 |
| &nbsp;&nbsp;non-equivalent, killed only with a root-level config path, which the staged layout cannot express (§4.2, bwrap probe) | 2 |
| non-equivalent survivors with no kill found | 0 |

Kill rate on non-equivalent mutants (107 = 117 − 10): **82/107 = 76.6%** with the wave-1 oracle; **107/107** with the proposed additions (23 staged, 2 root-level).

Which oracle kills the 82: the tool's `--selftest` kills 73, the 26 fixtures kill 62; both 53; selftest only 20; fixtures only 9.

Survivor rate in the same order as round 55 (11/24, 8/38, 4/17); the per-counter numbers are not comparable, so no claim is made from the comparison.

## 2. Oracle and method

- **Oracle, unchanged.** (a) `python3 -I <mutant> --selftest`, exit 0 required. (b) The C2 harness functions from the lane at rev, `quality/r56_ctl_c2.py` (`score` and `staged_run`), which run the tool STAGED (tree only, empty cwd, bwrap sandbox, registration-v2 E6) on the 18 committed fixtures and the 8 revealed hold-out fixtures, comparing stdout bytes and exit status. A mutant is KILLED if the selftest fails or the harness line is not `TARGET_MET`.
- **Baseline.** Pristine: selftest `MADO_WATCH_SELFTEST: 82/82 assertions passed`, rc 0; harness `MADO_R56_C2: rev=28fc86ac… fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET`. Both captured in `receipts/`.
- **Mutant table.** `driver/mutate.py` holds the 117 `(id, area, anchor, replacement, note)` rows. Each run asserts the anchor is present exactly once and that the mutant differs from pristine on exactly one line; anything else is INVALID. Four first-run anchors were wrong (m82, m87, m101, m107); they were corrected and re-run (`receipts/sweep-rerun4-results.json`). Final: 117 valid, 0 invalid.
- **Parallelism.** 8 spawn workers; each worker has its own scratch copy of the lane paths the harness reads (`git archive` of 350 entries, not the 584 MB lane).
- **Per-fixture breakdown.** Each mutant is also scored per fixture with the harness's own `score`, so `fixtures_failed` names the fixture that catches it (in `receipts/merged-results.json`).
- Tool versions: python3 3.14.8 (`/usr/bin/python3`), bubblewrap 0.13.1 (pre-installed). **No tool was installed or upgraded by this seat.**

Commands (absolute paths; scratch `S=/fast/scratch/hyaku/mado-r56/R56W2MutC2ToolB`):

```
D=$(mktemp -d -p $S) && git -C "$D" init -q && git -C "$D" rev-parse --show-toplevel   # equals $D
git -C <lane> archive 28fc86ac2359ec27406d8a2c63bef82ea6e947ed | tar -x -C "$D"  (fresh repo, one base commit)
python3 -I driver/mutate.py --repo <lane> --rev 28fc86ac2359ec27406d8a2c63bef82ea6e947ed --work $S/wk --out $S/out --jobs 8
   -> sweep run 1: TOTAL killed=80 survived=33 invalid=4 of 117
   -> 4 corrected anchors re-run (--only m82,m87,m101,m107): m82 SURVIVED, m87 KILLED, m101 SURVIVED, m107 KILLED
python3 -I driver/verify.py --repo <lane> --rev <rev> --work $S/vwF --mutants all-tools.json --cands driver/cands.py --out $S/voutF
   -> CANDIDATES killed=24 of 24 pairs
```

## 3. Survivors

Every survivor, with the mutated line and its status, is in §6. The arguments:

### 3.1 EQUIVALENT (10): no fixture can kill these

| id | mutated line | why no input distinguishes |
|---|---|---|
| m06 | `return home + raw[1:]` → `... if home is not None else raw` | `absolute_path` gets `home=None` only from `source()` for a raw starting `~`, which is rejected earlier (`unsupported`); matched paths are absolute, so `~` never reaches it |
| m15 | `except (OSError, ValueError)` → `except OSError` | `os.stat(target)`: `target` is a `glob` result (absolute, from the filesystem); `glob` returns `[]` for any NUL-bearing pattern (probed), so no NUL reaches `stat` |
| m19 | `except (OSError, ValueError, RuntimeError)` → drop `RuntimeError` | on CPython ≥3.13 `realpath(strict=True)` raises OSError (ELOOP) on a symlink loop, not RuntimeError (probed on 3.14.8: `OSError [Errno 40]`). Interpreter-dependent: the pristine keeps the RuntimeError catch for older Pythons |
| m77 | `glob.glob(pattern)` → `glob.glob(pattern, recursive=False)` | the default |
| m82 | `target = absolute_path(match, cur, self.home) if match else match` → `target = match` | `match` is a glob result of an absolute pattern, so it starts with `/`; `absolute_path` is the identity on it |
| m97 | `if gdata is not None` → `if gdata` (in `live = ...`) | `live_value(b"")` is `None`, as the `None` branch gives |
| m102 | `off = ... bool(value.strip("0"))` → `... .strip("0").strip(" ")` | `value` comes from `config_int`, digits only: no space |
| m104 | `rhs.strip(WS)` → `rhs` (LHS/RHS split) | the RHS is read only by `"##" in rhs` (strip-invariant) and by two later `.strip(WS)` calls |
| m108 | `"$" in line or "{" in line or "\\" in line` → same tests on `rhs` | the test runs only for key `== misc:disable_autoreload` (after the key test); that LHS, and the stack name `misc`, contain none of `$ { \` |
| m116 | `self.value.strip("0")` → `self.value.strip("0") != ""` | identical truthiness for a string |

### 3.2 Non-equivalent survivors (25)

Each row is a concrete behaviour change, with the fixture that shows it (§4). The pristine and mutant output lines are in `receipts/candidate-verify.json`.

| id | what the mutant changes | the input that shows it | fixture |
|---|---|---|---|
| m01 | `~x.conf` no longer expands via `--home` | `source = ~x.conf`, `--home …/tree/home`, file `tree/homex.conf` | K01 |
| m07 | `glob(recursive=True)`: `**` matches zero dirs | `source = conf.d/**/*.conf`, files `conf.d/a.conf`, `conf.d/sub/b.conf` | K02 |
| m08 | `sorted(found)` (code points) instead of bytewise | `conf.d/\x80.conf` (raw byte) and `conf.d/Ā.conf` (`C4 80`); bytewise puts `\x80` first | K03 |
| m09 | `expand` no longer catches `RecursionError` | `source = */`×1100 `x`: pristine `reason=nomatch` rc 0; mutant traceback rc 1 (the 1000-level recursion limit makes glob raise) | K20 |
| m14 | `inaccessible` → `continue` (not `return`) | `conf.d/a.conf` dangling symlink sorts first, `conf.d/b.conf` regular: pristine stops (`paths=1`), mutant adds `b.conf` (`paths=2`). F10 has the dangling entry last, where return and continue agree | K04 |
| m18 | `realpath(strict=True)` → non-strict | dangling MAIN config symlink: pristine prints no canonical watch, mutant prints one at the missing target | K05 |
| m21 | `lexists` → `exists` | the same dangling main config: pristine `type=file`, mutant `type=missing` | K05 |
| m25 | symlink-to-directory typed as file | MAIN config symlink to a directory: pristine `type=dir` and a canonical watch, mutant `type=file` | K06 |
| m30 | trailing slash of `--display-root` kept | display root `…/lnk/` where `lnk` → `real`, config via `lnk/` | K08 |
| m31 | the given display-root text not a prefix (realpath only) | display root `…/lnk`, config via `lnk/hyprland.conf` | K07 |
| m36 | `root[:-1]` for the given text | same as K07 | K07 |
| m94 | display root equal to a printed path does not match | `--display-root` = the config file itself | K10 |
| m95 | `root[1:]` for the given text | same as K07 | K07 |
| m49 | a backslash no longer makes a value unsupported | `misc:disable_autoreload = true\` (pristine `unsupported=1`, mutant `disable_autoreload=1`) | K11 |
| m51 | key `sourcex` treated as `source` | `sourcex = a.conf` with `a.conf` present (mutant `paths=2`) | K12 |
| m55 | comment lines are not skipped | `# x {` then `misc:disable_autoreload = 1` (a comment opens a category in the mutant) | K13 |
| m56 | `strip()` (wider set) instead of `WS` | a leading U+00A0 on the option line (pristine ignores it, mutant applies it) | K14 |
| m105 | `rpartition('=')` instead of the first `=` | `misc:disable_autoreload = 1 # a=b` | K15 |
| m101 | non-string option key with an int value stored | `go.json`: `{"option": [1], "int": 0}` (mutant: TypeError, unhashable, rc 1) | K16 |
| m109 | entry cap halved (131072) | 262143 entries (K18): pristine OK, mutant `SETUP too_large` | K18 |
| m64 | entry cap 1024 | same K18 | K18 |
| m65 | entry cap `>` instead of `>=` | exactly 262145 add attempts (K19): pristine `SETUP too_large` (rc 2), mutant OK | K19 |
| m114 | argv values stripped | `--config '…/hyprland.conf '` (trailing space): pristine `type=missing`, mutant finds the file | K17 |
| m75 | `curdir` bound off by one (`pos > 0`) | ROOT-LEVEL cur only: config `/hyprland.conf` with `source = sub/x.conf`. Pristine `/sub/x.conf` found, mutant `nomatch` (receipts/root-level-probe.txt) | probe |
| m76 | `../` parent bound off by one (`pos > 0`) | ROOT-LEVEL cur only: `/sub/x.conf` with `source = ../a.conf`. Pristine `/a.conf` found, mutant `nomatch` | probe |

m75 and m76 need a `cur` whose directory has a single `/` (a file directly under `/`). The staged layout places every file under `{FX}/…`, so no committed fixture can present that path; they are killed only by the bwrap probe (`driver/root-level-probe.sh`), which mounts a tmpfs root with `/hyprland.conf`, `/sub/x.conf` and `/a.conf`.

## 4. Proposed killing fixtures

Each proposed fixture is a directory with `args.json`, `tree/`, `expected.out`, `expected.rc`, in the frozen format. `expected.*` are the PRISTINE tool's bytes, produced by the harness's own staged bwrap runner. `driver/verify.py` runs both tools through the harness's own `score` (staged): pristine must score 1, the mutant 0. Result: **24 of 24 pairs KILLED** (`receipts/candidate-verify.log`). The fixture directories are in `fixtures/<mutant>/<K##>/`.

These fixtures are NOT added to the frozen `fixtures/c2` tree: adding any file changes `c2.fixture_commit_sha256` and the registration would then need a new versioned freeze (v3), as v2 requires. Each one is a candidate for that freeze.

### 4.1 Staged fixtures

| id | tree / args (summary) | pristine (key) | mutant (key) | kills |
|---|---|---|---|---|
| K01 | `source = ~x.conf`, `--home {FX}/tree/home`, `tree/homex.conf` | `paths=2 errors=0` | `paths=1 errors=1` | m01 |
| K02 | `source = conf.d/**/*.conf`; `conf.d/a.conf`, `conf.d/sub/b.conf` | `paths=2` | `paths=3` | m07 |
| K03 | `source = conf.d/*.conf`; `conf.d/\x80.conf` (raw byte), `conf.d/Ā.conf` | first `n=2` is `\x80.conf` | first `n=2` is `Ā.conf` | m08 |
| K04 | `source = conf.d/*.conf`; `conf.d/a.conf` dangling symlink, `conf.d/b.conf` | `paths=1 errors=1` | `paths=2 errors=1` | m14 |
| K05 | MAIN config is a dangling symlink | `n=1 type=file`, no canonical | canonical watch, or `type=missing` | m18, m21 |
| K06 | MAIN config is a symlink to a directory `realdir/` | `type=dir` + canonical `type=file` | `type=file` | m25 |
| K07 | `--config {FX}/tree/lnk/hyprland.conf --display-root {FX}/tree/lnk` (`lnk` → `real`) | `config=$ROOT/hyprland.conf` | raw absolute path | m31, m36, m95 |
| K08 | as K07 with `--display-root {FX}/tree/lnk/` | `config=$ROOT/hyprland.conf` | raw absolute path | m30 |
| K09 | `--config {FX}/tree/real/hyprland.conf --display-root {FX}/tree/lnk` | `config=$ROOT/hyprland.conf` | raw absolute path | m96 |
| K10 | `--display-root {FX}/tree/hyprland.conf` (= the config file) | `config=$ROOT` | raw absolute path | m94 |
| K11 | `misc:disable_autoreload = true\` | `autoreload=on … unsupported=1` | `autoreload=off disable_autoreload=1` | m49 |
| K12 | `sourcex = a.conf`, `a.conf` present | `paths=1` | `paths=2` | m51 |
| K13 | `# x {` then `misc:disable_autoreload = 1` | `autoreload=off` | `autoreload=on` | m55 |
| K14 | U+00A0 before `misc:disable_autoreload = 1` | `autoreload=on` | `autoreload=off` | m56 |
| K15 | `misc:disable_autoreload = 1 # a=b` | `autoreload=off` | `autoreload=on` | m105 |
| K16 | `--getoption go.json`, `{"option": [1], "int": 0}` | `live=? verdict=UNKNOWN`, rc 0 | rc 1 (TypeError) | m101 |
| K17 | `--config '{FX}/tree/hyprland.conf '` (trailing space) | `type=missing` | `type=file` | m114 |
| K18 | `source = hyprland.conf` ×2 (self-sourcing), `misc:disable_autoreload = 1` (262143 entries) | `paths=262143` rc 0 | `SETUP too_large` rc 2 | m64, m109 |
| K19 | `main`: `source = self.conf` ×2, `source = leaf.conf` ×2, disable=1; `self.conf`: `source = self.conf` ×2 (262145 add attempts) | `SETUP too_large` rc 2 | `paths=262145` rc 0 | m65 |
| K20 | `source = */` ×1100 `x` | `ERROR … reason=nomatch` rc 0 | traceback rc 1 (RecursionError) | m09 |

Runtime: K18 and K19 take about 5–9 s per tool run on this host, against the harness's 30 s `TIMEOUT`.

### 4.2 Root-level probe (m75, m76)

`driver/root-level-probe.sh PRISTINE MUTANT…` (bwrap, tmpfs root, `/hyprland.conf`, `/sub/x.conf`, `/a.conf`). Output in `receipts/root-level-probe.txt`:

```
== pristine-tool.py
MADO_WATCH: config=/hyprland.conf ... paths=3 unsupported=0 errors=0
MADO_WATCH: n=2 role=primary path=/sub/x.conf ...      n=3 role=primary path=/a.conf ...
== m75.py
MADO_WATCH: config=/hyprland.conf ... paths=1 unsupported=0 errors=1
MADO_WATCH: ERROR via=/hyprland.conf:1 source=sub/x.conf reason=nomatch
== m76.py
MADO_WATCH: config=/hyprland.conf ... paths=2 unsupported=0 errors=1
MADO_WATCH: ERROR via=/sub/x.conf:1 source=../a.conf reason=nomatch
```

## 5. Limits and what was not verified

- **Equivalence is argued, not proven by machine.** The 10 EQUIVALENT rows rest on the argument in §3.1 and on the probes named there. The random differential probe (`driver/difftest.py`) was stopped after 11 of 35 survivors (`receipts/difftest-PARTIAL-not-evidence.log`). It is NOT evidence: it reported `distinguishable=False` for m07 and m105, which K02 and K15 kill with one fixture each (its input vocabulary has no `**` and no `=` in comments). Its output is kept only to show that.
- **Interpreter dependence.** m19's equivalence needs CPython ≥3.13 (`realpath` strict raises OSError). K20 needs the default recursion limit of 1000 (`sys.getrecursionlimit()`); K20 uses 1100 components so that it crosses that limit on 3.14.8, not on a higher limit.
- **Oracle is the wave-1 oracle, not a stronger one.** I did not add mutants outside the 117 rows; coverage is the 117 one-line edits the seat was given, not an exhaustive set.
- **Not checked against Hyprland or glibc.** The pristine's choice to report a Python `RecursionError` as `reason=nomatch` (K20) is not a documented divergence. Whether glibc `glob(3)` gives the same no-match on that pattern is not verified (glibc was not run). Not verified.
- **Hold-out disclosure.** The revealed hold-out (`fixtures/c2-holdout`, H01–H08) and the committed F01–F18 were read in this seat. The candidates were written from the tool source and the pristine's behaviour, not from hold-out content.
- The sweep and verify runs were executed on this host once each; no repeat runs were made to measure flakiness (none was observed: the verify run reproduced the 24/24 KILLED pattern on a second pass for m65/m64).

## 6. Full table (117 rows)

Status column: `killed by …` (original oracle); `SURVIVED - EQUIVALENT` (§3.1); `SURVIVED - non-equivalent: KILLED-BY K##` (§4); `SURVIVED - non-equivalent, ROOT-LEVEL` (§4.2). The `oracle (orig)` column names what killed the mutant first, and the fixture count where the harness ran.

| id | area | oracle (orig) | mutated line: old -> new | note | final status |
|---|---|---|---|---|---|
| m01 | absolute_path | survived (selftest ok, 26/26) | `if raw[0] == "~":` -> `if raw[0] == "~" and raw[1:2] == "/":` | tilde only expands when a slash follows | SURVIVED - non-equivalent: KILLED-BY K01 (verified via harness path) |
| m02 | absolute_path | selftest; fixtures 24/26 | `return parent + raw[2:]` -> `return parent + raw[3:]` | off-by-one in the ../ branch | killed by selftest + fixtures 24/26 |
| m03 | absolute_path | selftest; fixtures 24/26 | `if raw.startswith("./"):` -> `if raw.startswith(".//"):` | ./ branch never taken | killed by selftest + fixtures 24/26 |
| m04 | absolute_path | selftest | `return curdir + "/" + raw` -> `return curdir + raw` | bare/dot path loses its separator | killed by selftest |
| m05 | absolute_path | selftest; fixtures 24/26 | `pos = curdir.rfind("/")` -> `pos = curdir.rfind("/") + 1` | off-by-one on the parent directory bound | killed by selftest + fixtures 24/26 |
| m06 | absolute_path | survived (selftest ok, 26/26) | `return home + raw[1:]` -> `return home + raw[1:] if home is not None else raw` | tilde with home=None falls through | SURVIVED - EQUIVALENT: `absolute_path` is only reached with `home=None` for a non-`~` raw; `source()` rejects `~` without --home first, and matched paths are absolute |
| m07 | glob | survived (selftest ok, 26/26) | `found = glob.glob(pattern)` -> `found = glob.glob(pattern, recursive=True)` | recursive glob enables ** semantics | SURVIVED - non-equivalent: KILLED-BY K02 (verified via harness path) |
| m08 | glob | survived (selftest ok, 26/26) | `return sorted(found, key=bytewise)` -> `return sorted(found)` | bytewise order replaced by code-point order | SURVIVED - non-equivalent: KILLED-BY K03 (verified via harness path) |
| m09 | glob | survived (selftest ok, 26/26) | `except (OSError, ValueError, RecursionError, re.error):` -> `except (OSError, ValueError):` | re.error/RecursionError no longer swallowed | SURVIVED - non-equivalent: KILLED-BY K20 (verified via harness path) |
| m10 | glob | selftest; fixtures 22/26 | `self.event_error(via, raw, "nomatch")` -> `self.event_error(via, raw, "no-match")` | nomatch reason renamed | killed by selftest + fixtures 22/26 |
| m100 | getoption | selftest; fixtures 24/26 | `live[option] = value` -> `live.setdefault(option, value)` | the first record of an option wins | killed by selftest + fixtures 24/26 |
| m101 | getoption | survived (selftest ok, 26/26) | `if isinstance(option, str) and type(value) is int:` -> `if not isinstance(option, str) or type(value) is int:` | the record filter inverted | SURVIVED - non-equivalent: KILLED-BY K16 (verified via harness path) |
| m102 | getoption | survived (selftest ok, 26/26) | `off = value is not None and bool(value.strip("0"))` -> `off = value is not None and bool(value.strip("0").strip(" "))` | a space-padded zero is not off | SURVIVED - EQUIVALENT: `value` is produced by `config_int` and is only digits, so it never contains a space |
| m103 | grammar | selftest; fixtures 21/26 | `if lhs.startswith("$"):` -> `if not lhs.startswith("$"):` | the variable rule inverted | killed by selftest + fixtures 21/26 |
| m104 | grammar | survived (selftest ok, 26/26) | `lhs, rhs = lhs.strip(WS), rhs.strip(WS)` -> `lhs, rhs = lhs.strip(WS), rhs` | the right-hand side is not stripped | SURVIVED - EQUIVALENT: the unstripped RHS is only read by a `"##" in rhs` test (strip-invariant) and by two later `.strip(WS)` calls |
| m105 | grammar | survived (selftest ok, 26/26) | `lhs, _, rhs = line.partition("=")` -> `lhs, _, rhs = line.rpartition("=")` | the last '=' splits instead of the first | SURVIVED - non-equivalent: KILLED-BY K15 (verified via harness path) |
| m106 | grammar | selftest; fixtures 18/26 | `if key != OPTION:` -> `if key == OPTION:` | the option-key test inverted | killed by selftest + fixtures 18/26 |
| m107 | grammar | selftest; fixtures 21/26 | `if ok:` -> `if not ok:` | the value-accept test inverted | killed by selftest + fixtures 21/26 |
| m108 | grammar | survived (selftest ok, 26/26) | `if "$" in line or "{" in line or "\\" in line or "##" in rhs:` -> `if "$" in rhs or "{" in rhs or "\\" in rhs or "##" in rhs:` | the unsupported-value test moved from the line to the RHS | SURVIVED - EQUIVALENT: a line that holds `$`, `{` or a backslash only in its LHS fails the key test first: the only key that matters is `misc:disable_autoreload` (or `disable_autoreload` under `misc {`), which has none of those characters |
| m109 | limits | survived (selftest ok, 26/26) | `if len(self.entries) >= MAX_ENTRIES:` -> `if len(self.entries) >= MAX_ENTRIES // 2:` | entry cap halved | SURVIVED - non-equivalent: KILLED-BY K18 (verified via harness path) |
| m11 | glob | selftest; fixtures 12/26 | `matches = expand(absolute_path(raw, cur, self.home))` -> `matches = expand(raw)` | glob pattern not made absolute | killed by selftest + fixtures 12/26 |
| m110 | limits | selftest; fixtures 25/26 | `if depth + 1 > MAX_DEPTH:` -> `if depth + 1 > MAX_DEPTH + 1:` | depth cap raised | killed by selftest + fixtures 25/26 |
| m111 | limits | selftest | `MAX_BYTES = 1048576` -> `MAX_BYTES = 2097152` | size limit doubled | killed by selftest |
| m112 | limits | selftest; fixtures 3/26 | `if len(data) > MAX_BYTES:` -> `if len(data) > 0:` | the size limit is never applied | killed by selftest + fixtures 3/26 |
| m113 | usage | selftest; fixtures 2/26 | `if len(argv) % 2:` -> `if len(argv) % 2 != 2:` | the argument count test changed | killed by selftest + fixtures 2/26 |
| m114 | usage | survived (selftest ok, 26/26) | `opts[flag] = value` -> `opts[flag] = value.strip()` | the argument value is stripped | SURVIVED - non-equivalent: KILLED-BY K17 (verified via harness path) |
| m115 | watchlist | selftest; fixtures 21/26 | `out = [] /         if self.value is not None and self.value.strip("0"):` -> `out = [] /         if self.value is not None and self.value.strip("1"):` | a value of 1 does not empty the watch list | killed by selftest + fixtures 21/26 |
| m116 | watchlist | survived (selftest ok, 26/26) | `if self.value is not None and self.value.strip("0"):` -> `if self.value is not None and self.value.strip("0") != "":` | the watch-list gate always fires | SURVIVED - EQUIVALENT: `value.strip("0") != ""` is exactly the truthiness of that string |
| m117 | watchlist | selftest; fixtures 22/26 | `out.append(("primary", path, kind, mask, via))` -> `out.append(("primary", os.path.realpath(path), kind, mask, via))` | the primary watch prints the realpath | killed by selftest + fixtures 22/26 |
| m12 | stat | selftest; fixtures 25/26 | `self.event_error(via, raw, "inaccessible")` -> `self.event_error(via, raw, "nomatch")` | inaccessible downgraded to nomatch | killed by selftest + fixtures 25/26 |
| m13 | stat | selftest; fixtures 23/26 | `mode = os.stat(target).st_mode` -> `mode = os.lstat(target).st_mode` | stat replaced by lstat (symlink not followed) | killed by selftest + fixtures 23/26 |
| m14 | stat | survived (selftest ok, 26/26) | `self.event_error(via, raw, "inaccessible") /                 return` -> `self.event_error(via, raw, "inaccessible") /                 continue` | the rest of the line's matches is no longer skipped | SURVIVED - non-equivalent: KILLED-BY K04 (verified via harness path) |
| m15 | stat | survived (selftest ok, 26/26) | `except (OSError, ValueError): /                 self.event_error(via, raw, "inaccessible")` -> `except OSError: /                 self.event_error(via, raw, "inaccessible")` | ValueError no longer caught | SURVIVED - EQUIVALENT: `os.stat(target)` never sees a NUL: targets are `glob` results, and `glob` returns [] for any NUL-bearing pattern (probed) |
| m16 | canonical | selftest; fixtures 23/26 | `if os.path.islink(path):` -> `if False:` | canonical watch never emitted | killed by selftest + fixtures 23/26 |
| m17 | canonical | selftest; fixtures 23/26 | `out.append(("canonical", canonical, "file", MASK_CANON, via))` -> `out.append(("canonical", canonical, "file", MASK_FILE, via))` | canonical watch carries the primary mask | killed by selftest + fixtures 23/26 |
| m18 | canonical | survived (selftest ok, 26/26) | `canonical = os.path.realpath(path, strict=True)` -> `canonical = os.path.realpath(path)` | realpath no longer strict | SURVIVED - non-equivalent: KILLED-BY K05 (verified via harness path) |
| m19 | canonical | survived (selftest ok, 26/26) | `except (OSError, ValueError, RuntimeError):` -> `except (OSError, ValueError):` | RuntimeError no longer caught | SURVIVED - EQUIVALENT: CPython 3.13+ `realpath(strict=True)` raises OSError (ELOOP) on a loop, never RuntimeError (probed on 3.14.8) |
| m20 | canonical | selftest; fixtures 24/26 | `out.append(("canonical", canonical, "file", MASK_CANON, via))` -> `out.append(("canonical", canonical, "file", MASK_CANON, "main"))` | canonical watch loses its via | killed by selftest + fixtures 24/26 |
| m21 | typing | survived (selftest ok, 26/26) | `elif os.path.lexists(path):` -> `elif os.path.exists(path):` | lexists replaced by exists (dangling symlink becomes missing) | SURVIVED - non-equivalent: KILLED-BY K05 (verified via harness path) |
| m22 | typing | selftest; fixtures 25/26 | `kind, mask = "missing", MASK_FILE` -> `kind, mask = "missing", MASK_DIR` | missing watch carries the directory mask | killed by selftest + fixtures 25/26 |
| m23 | typing | selftest; fixtures 25/26 | `kind, mask = "missing", MASK_FILE` -> `kind, mask = "file", MASK_FILE` | missing watch typed as file | killed by selftest + fixtures 25/26 |
| m24 | typing | selftest | `kind, mask = "dir", MASK_DIR` -> `kind, mask = "dir", MASK_FILE` | directory watch carries the file mask | killed by selftest |
| m25 | typing | survived (selftest ok, 26/26) | `if os.path.isdir(path):` -> `if os.path.isdir(path) and not os.path.islink(path):` | symlink to a directory typed as file | SURVIVED - non-equivalent: KILLED-BY K06 (verified via harness path) |
| m26 | duplicates | selftest; fixtures 24/26 | `len(plan.entries), plan.unsupported, plan.errors)]` -> `len(set(p for p, _ in plan.entries)), plan.unsupported, plan.errors)]` | paths= counts distinct paths | killed by selftest + fixtures 24/26 |
| m27 | duplicates | selftest; fixtures 4/26 | `len(plan.entries), plan.unsupported, plan.errors)]` -> `len(plan.entries) + 1, plan.unsupported, plan.errors)]` | paths= count off by one | killed by selftest + fixtures 4/26 |
| m28 | duplicates | selftest; fixtures 7/26 | `for path, via in self.entries:` -> `for path, via in self.entries[:-1]:` | last entry dropped | killed by selftest + fixtures 7/26 |
| m29 | duplicates | fixtures 14/26 | `out.append(("primary", path, kind, mask, via))` -> `out.append(("primary", path, kind, mask, "main"))` | primary watch loses its via | killed by fixtures 14/26 |
| m30 | display-root | survived (selftest ok, 26/26) | `given = root[:-1] if root.endswith("/") else root` -> `given = root` | trailing slash of display-root kept | SURVIVED - non-equivalent: KILLED-BY K08 (verified via harness path) |
| m31 | display-root | survived (selftest ok, 26/26) | `self.prefixes.append(given)` -> `pass` | the given text of display-root is not a prefix | SURVIVED - non-equivalent: KILLED-BY K07 (verified via harness path) |
| m32 | display-root | selftest | `self.prefixes.append(os.path.realpath(root))` -> `self.prefixes.append(root)` | display-root realpath not used as prefix | killed by selftest |
| m33 | display-root | selftest | `if path == prefix or path.startswith(prefix + "/"):` -> `if path.startswith(prefix):` | prefix match without a path-separator boundary | killed by selftest |
| m34 | display-root | selftest; fixtures 4/26 | `return "$ROOT" + path[len(prefix):]` -> `return "$ROOT" + path[len(prefix) + 1:]` | $ROOT suffix drops a character | killed by selftest + fixtures 4/26 |
| m35 | display-root | selftest; fixtures 4/26 | `return "$ROOT" + path[len(prefix):]` -> `return "$ROOT/" + path[len(prefix):]` | $ROOT gains a separator | killed by selftest + fixtures 4/26 |
| m36 | display-root | survived (selftest ok, 26/26) | `given = root[:-1] if root.endswith("/") else root` -> `given = root[:-1]` | display-root always loses its last character | SURVIVED - non-equivalent: KILLED-BY K07 (verified via harness path) |
| m37 | getoption | selftest; fixtures 7/26 | `gdata = read_getoption(opts["--getoption"]) if "--getoption" in opts else None` -> `gdata = read_getoption(opts["--getoption"]) if "--getoption" in opts else b""` | no --getoption behaves like an empty dump | killed by selftest + fixtures 7/26 |
| m38 | getoption | selftest | `if isinstance(option, str) and type(value) is int:` -> `if isinstance(option, str) and isinstance(value, int):` | bool accepted as an int value | killed by selftest |
| m39 | getoption | selftest; fixtures 25/26 | `if not isinstance(obj, dict):` -> `if not isinstance(obj, (dict, list)):` | JSON arrays accepted as records | killed by selftest + fixtures 25/26 |
| m40 | getoption | selftest | `except (ValueError, RecursionError):` -> `except ValueError:` | RecursionError no longer caught | killed by selftest |
| m41 | getoption | selftest | `obj = json.loads(line, parse_constant=_no_constant)` -> `obj = json.loads(line)` | NaN/Infinity accepted | killed by selftest |
| m42 | getoption | fixtures 25/26 | `if not line: /             continue` -> `if not line: /             break` | a blank line ends the dump scan | killed by fixtures 25/26 |
| m43 | getoption | selftest | `return live.get(OPTION)` -> `return live.get(OPTION, 0)` | an absent option reads as 0 | killed by selftest |
| m44 | getoption | selftest; fixtures 23/26 | `verdict = "UNKNOWN" if live is None else ("AGREE" if live == config_flag else "DIFFER")` -> `verdict = "UNKNOWN" if live is None else ("AGREE" if live != config_flag else "DIFFER")` | AGREE and DIFFER swapped | killed by selftest + fixtures 23/26 |
| m45 | getoption | selftest; fixtures 23/26 | `config_flag = 1 if off else 0` -> `config_flag = 0 if off else 1` | config flag inverted | killed by selftest + fixtures 23/26 |
| m46 | getoption | selftest; fixtures 24/26 | `off = value is not None and bool(value.strip("0"))` -> `off = value is not None` | any set value counts as off | killed by selftest + fixtures 24/26 |
| m47 | getoption | fixtures 24/26 | `if self.value is not None and self.value.strip("0"):` -> `if self.value is not None:` | a zero value empties the watch list | killed by fixtures 24/26 |
| m48 | getoption | selftest | `ok, number_text = config_int(rhs.split("#", 1)[0].strip(WS))` -> `ok, number_text = config_int(rhs)` | comment not cut from an option value | killed by selftest |
| m49 | getoption | survived (selftest ok, 26/26) | `if "$" in line or "{" in line or "\\" in line or "##" in rhs:` -> `if "$" in line or "{" in line or "##" in rhs:` | backslash no longer unsupported | SURVIVED - non-equivalent: KILLED-BY K11 (verified via harness path) |
| m50 | grammar | fixtures 25/26 | `if stack: /                     self.unsupported += 1` -> `if False: /                     self.unsupported += 1` | source inside a category no longer unsupported | killed by fixtures 25/26 |
| m51 | grammar | survived (selftest ok, 26/26) | `if lhs == "source":` -> `if lhs.startswith("source"):` | a key merely starting with source is a source | SURVIVED - non-equivalent: KILLED-BY K12 (verified via harness path) |
| m52 | grammar | selftest; fixtures 22/26 | `key = ":".join(stack) + ":" + lhs if stack else lhs` -> `key = lhs` | category stack ignored in the key | killed by selftest + fixtures 22/26 |
| m53 | grammar | selftest | `if stack: /                         stack.pop()` -> `if stack or True: /                         stack.pop()` | pop without an emptiness guard | killed by selftest |
| m54 | grammar | selftest; fixtures 22/26 | `stack.append(line[:-1].strip(WS))` -> `stack.append(line)` | category name keeps its brace | killed by selftest + fixtures 22/26 |
| m55 | grammar | survived (selftest ok, 26/26) | `if not line or line[0] == "#":` -> `if not line:` | comment lines are parsed | SURVIVED - non-equivalent: KILLED-BY K13 (verified via harness path) |
| m56 | grammar | survived (selftest ok, 26/26) | `line = raw_line.strip(WS)` -> `line = raw_line.strip()` | strip uses the wider default set | SURVIVED - non-equivalent: KILLED-BY K14 (verified via harness path) |
| m57 | grammar | selftest; fixtures 12/26 | `for number, raw_line in enumerate(data.decode("utf-8", errors="replace").split("\n"), 1):` -> `for number, raw_line in enumerate(data.decode("utf-8", errors="replace").split("\n"), 0):` | line numbers start at 0 | killed by selftest + fixtures 12/26 |
| m58 | grammar | fixtures 25/26 | `self.source(rhs.split("#", 1)[0].strip(WS), path, number, depth)` -> `self.source(rhs.split("#", 1)[0], path, number, depth)` | source path not stripped | killed by fixtures 25/26 |
| m59 | limits | selftest; fixtures 25/26 | `if depth + 1 > MAX_DEPTH:` -> `if depth + 1 >= MAX_DEPTH:` | depth cap off by one | killed by selftest + fixtures 25/26 |
| m60 | limits | selftest; fixtures 25/26 | `MAX_DEPTH = 16` -> `MAX_DEPTH = 15` | depth cap lowered | killed by selftest + fixtures 25/26 |
| m61 | limits | selftest | `MAX_BYTES = 1048576` -> `MAX_BYTES = 1048575` | size limit lowered | killed by selftest |
| m62 | limits | selftest | `data = fh.read(MAX_BYTES + 1)` -> `data = fh.read(MAX_BYTES)` | one byte too few is read to detect oversize | killed by selftest |
| m63 | limits | selftest | `if len(data) > MAX_BYTES:` -> `if len(data) >= MAX_BYTES:` | size comparison off by one | killed by selftest |
| m64 | limits | survived (selftest ok, 26/26) | `MAX_ENTRIES = 262144` -> `MAX_ENTRIES = 1024` | entry cap lowered | SURVIVED - non-equivalent: KILLED-BY K18 (verified via harness path) |
| m65 | limits | survived (selftest ok, 26/26) | `if len(self.entries) >= MAX_ENTRIES:` -> `if len(self.entries) > MAX_ENTRIES:` | entry cap comparison off by one | SURVIVED - non-equivalent: KILLED-BY K19 (verified via harness path) |
| m66 | usage | selftest; fixtures 2/26 | `if len(argv) % 2:` -> `if len(argv) % 2 == 0:` | argument parity inverted | killed by selftest + fixtures 2/26 |
| m67 | usage | selftest; fixtures 25/26 | `if flag not in ("--config", "--home", "--display-root", "--getoption") or flag in opts:` -> `if flag not in ("--config", "--home", "--display-root", "--getoption") and flag in opts:` | a repeated flag is accepted | killed by selftest + fixtures 25/26 |
| m68 | usage | selftest | `if not value.startswith("/"):` -> `if not value.startswith("/") and False:` | a relative argument value is accepted | killed by selftest |
| m69 | usage | selftest; fixtures 1/26 | `if "--config" not in opts:` -> `if "--config" in opts:` | config requirement inverted | killed by selftest + fixtures 1/26 |
| m70 | absolute_path | selftest; fixtures 12/26 | `if raw[0] == "/":` -> `if raw[0] != "/":` | absolute-path test inverted | killed by selftest + fixtures 12/26 |
| m71 | absolute_path | selftest | `if raw.startswith("../"):` -> `if raw.startswith(".."):` | ../ prefix widened to any two dots | killed by selftest |
| m72 | absolute_path | selftest | `if raw.startswith("./"):` -> `if raw.startswith("."):` | ./ prefix widened to any dot | killed by selftest |
| m73 | absolute_path | selftest; fixtures 14/26 | `pos = cur.rfind("/")` -> `pos = cur.rfind("/") - 1` | directory bound off by one | killed by selftest + fixtures 14/26 |
| m74 | absolute_path | selftest; fixtures 24/26 | `return home + raw[1:]` -> `return home + raw[1:].lstrip("/")` | tilde home joined without a separator | killed by selftest + fixtures 24/26 |
| m75 | absolute_path | survived (selftest ok, 26/26) | `curdir = cur[:pos] if pos >= 0 else cur` -> `curdir = cur[:pos] if pos > 0 else cur` | directory bound off by one | SURVIVED - non-equivalent, ROOT-LEVEL: `curdir` bound for a root-level cur (`/hyprland.conf`): pristine gives `/a.conf`, mutant `/hyprland.conf/a.conf` (killed by bwrap probe, root-level-probe.sh) |
| m76 | absolute_path | survived (selftest ok, 26/26) | `parent = curdir[:pos] if pos >= 0 else curdir` -> `parent = curdir[:pos] if pos > 0 else curdir` | parent bound off by one | SURVIVED - non-equivalent, ROOT-LEVEL: `../` bound for a cur whose directory is one level deep (`/sub/x.conf`): pristine gives `/a.conf`, mutant `/sub/a.conf` (killed by bwrap probe, root-level-probe.sh) |
| m77 | glob | survived (selftest ok, 26/26) | `found = glob.glob(pattern)` -> `found = glob.glob(pattern, recursive=False)` | explicitly non-recursive glob | SURVIVED - EQUIVALENT: `glob.glob(pattern, recursive=False)` is the default; the mutant is the same call |
| m78 | glob | fixtures 22/26 | `return sorted(found, key=bytewise)` -> `return sorted(found, key=bytewise, reverse=True)` | bytewise order reversed | killed by fixtures 22/26 |
| m79 | glob | fixtures 25/26 | `found = glob.glob(pattern)` -> `found = glob.glob(pattern, include_hidden=True)` | hidden files included in the glob | killed by fixtures 25/26 |
| m80 | stat | selftest; fixtures 12/26 | `if stat.S_ISREG(mode):` -> `if not stat.S_ISREG(mode):` | regular-file test inverted | killed by selftest + fixtures 12/26 |
| m81 | stat | selftest; fixtures 23/26 | `elif stat.S_ISDIR(mode):` -> `elif not stat.S_ISDIR(mode):` | directory test inverted | killed by selftest + fixtures 23/26 |
| m82 | stat | survived (selftest ok, 26/26) | `target = absolute_path(match, cur, self.home) if match else match` -> `target = match` | match not made absolute | SURVIVED - EQUIVALENT: `glob` results start with `/` (the pattern is absolute), so `absolute_path(match)` is the identity |
| m83 | stat | selftest; fixtures 24/26 | `if len(raw) < 2:` -> `if len(raw) < 1:` | bogus threshold lowered | killed by selftest + fixtures 24/26 |
| m84 | stat | fixtures 25/26 | `if len(raw) < 2:` -> `if len(raw) < 3:` | bogus threshold raised | killed by fixtures 25/26 |
| m85 | canonical | selftest; fixtures 23/26 | `out.append(("canonical", canonical, "file", MASK_CANON, via))` -> `out.append(("canonical", canonical, "file", MASK_CANON, path))` | canonical via replaced by the path | killed by selftest + fixtures 23/26 |
| m86 | canonical | selftest; fixtures 8/26 | `if os.path.islink(path):` -> `if not os.path.islink(path):` | symlink test inverted | killed by selftest + fixtures 8/26 |
| m87 | canonical | selftest; fixtures 7/26 | `out.append(("primary", path, kind, mask, via))` -> `out.append(("primary", path, kind, mask, canonical))` | primary watch via replaced by a canonical name | killed by selftest + fixtures 7/26 |
| m88 | typing | selftest; fixtures 8/26 | `if os.path.isdir(path):` -> `if os.path.isfile(path):` | directory test replaced by file test | killed by selftest + fixtures 8/26 |
| m89 | typing | fixtures 9/26 | `elif os.path.lexists(path):` -> `elif os.path.islink(path):` | existence test replaced by a symlink test | killed by fixtures 9/26 |
| m90 | typing | selftest | `kind, mask = "dir", MASK_DIR` -> `kind, mask = "missing", MASK_DIR` | directory watch typed as missing | killed by selftest |
| m91 | duplicates | selftest; fixtures 14/26 | `for path, via in self.entries:` -> `for path, via in reversed(self.entries):` | entry order reversed | killed by selftest + fixtures 14/26 |
| m92 | duplicates | selftest; fixtures 7/26 | `for path, via in self.entries:` -> `for path, via in self.entries[1:]:` | first entry dropped | killed by selftest + fixtures 7/26 |
| m93 | duplicates | selftest; fixtures 7/26 | `self.entries.append((path, via))` -> `self.entries.append((via, path))` | entry tuple order swapped | killed by selftest + fixtures 7/26 |
| m94 | display-root | survived (selftest ok, 26/26) | `if path == prefix or path.startswith(prefix + "/"):` -> `if path.startswith(prefix + "/"):` | the prefix itself no longer matches | SURVIVED - non-equivalent: KILLED-BY K10 (verified via harness path) |
| m95 | display-root | survived (selftest ok, 26/26) | `given = root[:-1] if root.endswith("/") else root` -> `given = root[1:]` | display-root loses its first character | SURVIVED - non-equivalent: KILLED-BY K07 (verified via harness path) |
| m96 | display-root | selftest | `self.prefixes.append(os.path.realpath(root))` -> `self.prefixes.append(os.path.realpath(root) + "/")` | realpath prefix gains a separator | killed by selftest |
| m97 | getoption | survived (selftest ok, 26/26) | `live = live_value(gdata) if gdata is not None else None` -> `live = live_value(gdata) if gdata else None` | an empty dump is treated as no dump | SURVIVED - EQUIVALENT: `live_value(b"")` returns None, the same value the `None` branch gives |
| m98 | getoption | selftest | `if gdata is not None:` -> `if gdata:` | the LIVE line is emitted for an empty dump | killed by selftest |
| m99 | getoption | selftest; fixtures 23/26 | `option, value = obj.get("option"), obj.get("int")` -> `option, value = obj.get("option"), obj.get("value")` | the dump's key is renamed | killed by selftest + fixtures 23/26 |
