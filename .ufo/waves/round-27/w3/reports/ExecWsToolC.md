# ExecWsToolC — second, independent implementation of `tools/mado-wsrules.py`

Seat: `MadoR27.ExecWsToolC` (round 27, hyaku run-5, attempt 2, residual wave w3).
Role per the frozen data rule: two executor seats build `tools/mado-wsrules.py`
independently.  ExecWsToolA's file returned and landed unmodified; this seat is the
independent second implementation.

**This file stays a second implementation.**  It is *not* measured for the C1 claim
and it does *not* replace the landed tool (`tools/mado-wsrules.py` at rev
`48b9434a0b0619b3896c9d80e8288ec2226c9ed8`, sha256
`722c7ae47eaee57eda4c6a223f4dad6fc585018453c2f7a2fd26c52d1e006008`).  Nothing in
the fleet repo was modified by this seat; the only file written there is this report.

## 1. The artifact

| item | value |
|---|---|
| path | `/fast/scratch/hyaku/mado-r27/data/ExecWsToolC/mado-wsrules.py` |
| sha256 | `dcf5c8c05b2d5b68ef967df339f7539a762e56c8a3811d7fbef33db9936ca389` |
| size | 30664 bytes, 851 lines |
| mode | executable (`-rwxr-xr-x`), shebang `#!/usr/bin/env python3` |
| dependencies | Python 3 standard library only (`argparse`, `glob`, `json`, `os`, `re`, `struct`, `sys`) |
| interface | `--home DIR` → on stdout the JSON array `hyprctl workspacerules -j` prints for the tree rooted at `DIR/.config/hypr/hyprland.conf`, derived from bytes only |

Helpers written by this seat (all under the same scratch directory, not part of the
deliverable): `selftest.py` (13 recorded probe trees + the report's merge/sameline/bools
cases), `probe_oracle.py`, `rawbytes.py` (raw-byte comparison against the pinned
Hyprland), `difftest.py` (differential against the landed tool *and* the oracle),
`fuzz.py` (randomized differential), `laneclone/` (sandbox clone of the lane used to
run the frozen counter against this file), `evidence/` (transcripts).

## 2. Method and ground truth

Read before writing the first draft (independence first, the landed file was only
opened afterwards, for the diff in §5):

* `.ufo/waves/round-27/w2/reports/ScoutOracleWsSemantics.md` — the measured
  semantics of the pinned Hyprland (row keying, merge, bool spellings, error
  handling, the `enabled`/`layoutopt` facts).
* Hyprland **v0.56.2** (commit `efb50993780079460b0cbed1363e2166a2de1d9f`), source
  in `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2/`:
  `src/config/legacy/ConfigManager.cpp` (`handleWorkspaceRules`, `handleSource`),
  `src/helpers/MiscFunctions.cpp` (`getWorkspaceIDNameFromString`,
  `cleanCmdForWorkspace`), `src/debug/HyprCtl.cpp` (`getWorkspaceRuleData`).
* **hyprlang v0.6.8** (commit `3a1c1b25b059dae2c6bbc46991562ba1158d125c`), source in
  `/fast/scratch/hyaku/mado-r26/hyprlang-0.6.8/`: `src/config.cpp` (`getNextLine`,
  `parseComment`, `parseVariable`, `parseExpression`, `parseLine`, `clearState`,
  `recheckEnv`), `include/hyprlang.hpp`.
* **hyprutils v0.14.2**, source in `/fast/scratch/hyaku/mado-r26/hyprutils-0.14.2/`:
  `src/string/VarList2.cpp` (`CVarList2`, the escape/empty-argument rules),
  `src/string/String.cpp` (`trim`, `replaceInString`), `include/hyprutils/string/Numeric.hpp`
  (`isNumber2`).

Behaviour implemented from those bytes: hyprlang line handling (`#` comments with `##`
escapes, `\` continuation, `$name = value` variables in one shared table, redefinition
taking effect from that line on, `{{ expr }}` single-operator float expressions),
`source =` followed depth-first in line order (`~` expansion, paths relative to the
sourcing file, glob-sorted matches, non-regular files skipped, a file sourced twice
parsed twice, cycles skipped), and the legacy `workspace = SELECTOR, RULES` grammar
(selector = first comma field trimmed; later fields split, empty dropped, trimmed;
first key found in a field wins; a value that fails to parse drops the whole line;
rows keyed by the exact trimmed selector, merged in place in first-seen order,
overwriting only the fields a line sets).

## 3. Acceptance evidence

### 3.1 Self-test without Hyprland — 16/16

`python3 -I selftest.py` (trees under `trees/`, expected arrays read from the probe's
`results.json`):

```
probe/empty                        PASS
probe/merge                        PASS
probe/sameline                     PASS
probe/norules                      PASS
probe/unknown                      PASS
probe/substr                       PASS
probe/gaps                         PASS
probe/mergeerr                     PASS
probe/enabled                      PASS
probe/layoutopt                    PASS
probe/whitespace                   PASS
probe/namevsid                     PASS
probe/bools                        PASS
report/merge                       PASS
report/sameline                    PASS
report/bools                       PASS
stdout parses as JSON array: PASS
stdout is exactly one JSON array: PASS
SELFTEST pass=16 fail=0
```

* the 13 probe trees of `/fast/scratch/hyaku/mado-r27/probe/ScoutOracleWsSemantics/<case>/tree`
  against the expected arrays in that probe's `results.json`: **13 matched, 0 mismatched**;
* fresh trees under `trees/` reproducing the report's `merge`, `sameline` and `bools`
  cases, diffed against the JSON recorded in the report (canonical, key-order
  independent, type strict): **3 matched, 0 mismatched**.

### 3.2 Byte-identical to the compositor's own output

`rawbytes.py` captures the raw bytes Hyprland v0.56.2 prints for
`hyprctl workspacerules -j` and compares them with this tool's stdout for the same
tree:

```
--- hyprland raw (421 bytes) ---
'[{\n    "workspaceString": "3",\n    "enabled": true,\n    "gapsIn": [1, 1, 1, 1],\n ...
--- mine (421 bytes) ---
'[{\n    "workspaceString": "3",\n    "enabled": true,\n    "gapsIn": [1, 1, 1, 1],\n ...
BYTE_IDENTICAL: True
JSON_IDENTICAL: True
```

The output is byte-identical to `hyprctl workspacerules -j`, including the indentation,
the field order and the trailing newline — not merely equal after parsing.

### 3.3 The frozen counter `PRED-C1-r27-v4`

Run in a sandbox clone of the lane (`laneclone/`, clone of
`/home/vgpnk/Projects/shokunin/mado-shokunin`), with this file committed as
`tools/mado-wsrules.py` at clone rev `71388a7bcc0f02e59e037c6dabb625ea0d4ddd5d`
(sha256 `dcf5c8c05b2d5b68ef967df339f7539a762e56c8a3811d7fbef33db9936ca389`):

```
$ python3 -I .ufo/waves/round-27/c1/count-v4.py 71388a7bcc0f02e59e037c6dabb625ea0d4ddd5d --seed <seed> --jobs 4
PRED-C1-r27-v4 cases_pass=41/41 verdict=TARGET_MET
```

Four independent seeds, all `41/41` (`a1b2c3d4e5f60718`, `7f3e91c05a6b2d84`,
`00ff11aa22bb33cc`, `5c6d7e8f90a1b2c3`); transcripts in `evidence/c1-seed-*.txt`.
`HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0` on every run.

### 3.4 Differential against the landed tool and the real Hyprland

`difftest.py` builds adversarial trees, runs **this tool**, the **landed tool** and
the **pinned Hyprland** (through the round-27 harness oracle) on the same tree with
the same environment, and compares all three (74 cases: comments, continuations,
variables, redefinition, embedded variables, expressions, gap shorthands 1–5 values,
bad gaps, negative and large gaps, border sizes, bool spellings incl. hex/sign/overflow,
substring key matches, unknown keys, `enabled`, `layoutopt`/`layout`/`animation`,
on-created-empty, trailing/empty fields, escaped commas, duplicate keys, space before
colon, `default`/`defaultName`, empty monitor, `name:` selectors, row merging, and the
`source` variants: glob, nested, twice, variable path, missing, directory, relative,
mid-line, variables across files, redefinition in a sourced file).

Result (transcript in `evidence/diff-suite.txt`):

* this tool equals the oracle's array in **73 of 74** cases;
* the one remaining case is `env_home` (`monitor: $HOME`), where the value is the
  *sandbox's* `HOME` path: the oracle's `HOME` is its own copy of the tree
  (`…/m27diff-…/env_home-o/home`) and the tool's is the tree it was given, so the two
  paths cannot be equal by construction — the value is right for each environment;
* the landed tool equals the oracle in **57 of 74** cases; the 17 disagreements are
  15 `on-created-empty` cases (§5.1), 1 environment-variable case (`env_path`, §5.2)
  and 1 `env_home` case in which both tools differ from the oracle for
  environment reasons.

`fuzz.py` compares the two tools on 1500 randomly generated trees (random selectors
from the counter's selector space, random rule items, sources, variables, comments):

```
FUZZ cases=1500 diffs=570 new_class_diffs=0
```

570 raw differences, **0** of a difference class other than the `onCreatedEmpty`
artifact of §5.1.

## 4. Behaviour notes (measured, not assumed)

* **Row identity.** One row per exact trimmed selector, first-seen order kept; a later
  line with the same selector merges into the existing row in place and overwrites only
  the fields it sets.  `1`, `01` and `name:1` are three rows; `defaultName` is a field
  of a row, not a second selector.
* **`enabled`** is always `true` and is not a rule key; a field `enabled:false` is an
  unknown key and is ignored.
* **Bools** follow `ParserUtils::parseInt` prefix semantics: `true|on|yes` → true,
  `false|off|no` → false, anything else is parsed as an integer and `!= 0` decides.
* **Gaps** are the CSS 1–4 value shorthand; a gap value that does not parse drops the
  whole line, and the error text Hyprland prints is only the bad value.
* **`on-created-empty`** prints as `[workspace NAME] <cmd>`, where NAME is what
  Hyprland's `getWorkspaceIDNameFromString` resolves at config-parse time: the
  selector's id text for a numeric selector, the part after `name:`, `special:special`
  / `special:<x>`, `-1` for a plain name that no workspace carries, and the **empty**
  name for every selector that needs live state (`empty`, `prev`, `next`, `r±`, `m±`,
  `e±`, `+`, `-`) — while the config is being parsed there is no monitor yet, so
  Hyprland returns `{WORKSPACE_INVALID}`, whose name is empty.  Measured against the
  oracle (`evidence/diff-suite.txt`, cases `oce_*`).
* **Environment variables are part of the variable table**, as in hyprlang v0.6.8
  (`clearState()`: `impl->variables = impl->envVariables`), so `$PATH` expands.
* **`layoutopt` / `layout` / `animation`** are accepted and stored, but are not fields
  of `getWorkspaceRuleData` and are therefore not printed.
* A **source cycle** is skipped (the pinned Hyprland would recurse; the round-27
  counter feeds no cycles).

## 5. Semantic diff against the landed implementation

Landed file: `mado-shokunin/tools/mado-wsrules.py`, sha256
`722c7ae47eaee57eda4c6a223f4dad6fc585018453c2f7a2fd26c52d1e006008` (rev
`48b9434a0b0619b3896c9d80e8288ec2226c9ed8`).

### 5.1 The landed tool mis-parses every `on-created-empty` value (defect)

The landed tool takes the value with `field[delimiter + 16:]`, but the key
`"on-created-empty:"` is **17** characters long, so the value keeps its leading
colon:

```
landed, tools/mado-wsrules.py:574
    command = clean_cmd_for_workspace(name, field[delimiter + 16:])
```

Measured, same tree, same environment:

| config line | this tool | landed tool | Hyprland v0.56.2 |
|---|---|---|---|
| `workspace = 1, on-created-empty: kitty` | `[workspace 1] kitty` | `[workspace 1] : kitty` | `[workspace 1] kitty` |
| `workspace = 2, on-created-empty:echo hi` | `[workspace 2] echo hi` | `[workspace 2] :echo hi` | `[workspace 2] echo hi` |
| `workspace = 3, on-created-empty: kitty --class x` | `[workspace 3] kitty --class x` | `[workspace 3] : kitty --class x` | `[workspace 3] kitty --class x` |

This is the same defect the frozen counter sees: **every** case of the landed tool's
own C1 run that carries the `ONEMPTY` feature fails, which is exactly what the
already-landed receipt shows — `.ufo/waves/round-27/evidence/c1-after-48b9434a.txt`
(landed tool sha256 `722c7ae4…`) ends with

```
PRED-C1-r27-v4 cases_pass=19/41 verdict=TARGET_MISSED
```

and all 22 failing cases carry `ONEMPTY` in their feature list (the 19 passing ones
do not).  The same run with this seat's file is `41/41 verdict=TARGET_MET` (§3.3).
The fix is one character (`+ 17`), but it is in the fleet repo, which this seat may
not touch — reported, not changed.

### 5.2 Environment variables in the variable table

This tool seeds the variable table from the process environment, as hyprlang v0.6.8
does (`clearState()` → `impl->variables = impl->envVariables`).  The landed tool keeps
environment variables literal (its docstring calls this the round-27 note M26-10
"environment limit", shared with `tools/mado-binds.py`).

Measured (`env_path`, case `monitor: $PATH`, tool sandbox `PATH=/usr/bin`):

| | value |
|---|---|
| this tool | `/usr/bin` |
| Hyprland v0.56.2 | `/usr/bin` |
| landed tool | `$PATH` (literal) |

So for a config that references an environment variable, the landed tool's output
diverges from the compositor's; this tool's does not.  (`$HOME` cannot be compared
across the two sandboxes — each has its own `HOME` — so that case is not a
divergence in kind, only in path.)

### 5.3 Runtime-dependent selector names — now agreeing

This seat's first draft resolved `prev`, `next`, `+`/`-` and the relative forms to
`-1`; the landed tool resolved them to the empty name.  Measuring the pinned
Hyprland (cases `oce_prev`, `oce_next`, `oce_empty`, `oce_plus`, `oce_minus`,
`oce_rel`, `oce_relmon`) showed the **empty** name to be what Hyprland prints at
config-parse time, so this seat's draft was corrected to the empty name (the landed
tool was right) and the correction was verified against the oracle
(`evidence/diff-suite.txt`: all `oce_*` cases are `MINE=OK`).  The two tools now
agree on these selectors; the only remaining difference on those cases is §5.1.

### 5.4 Variable ordering (tie-break)

hyprlang keeps the variable list sorted by name length, longest first, with an
unstable sort for equal lengths, and leaves the environment variables in `environ`
order until a config variable is added.  This tool sorts by name length descending
with a lexicographic tie-break, and always sorts.  The difference is observable only
with prefix-overlapping variable names (e.g. `$FOO` and `$FOOBAR`), where the
replacement order decides the result; no case in the probe trees, the 74-case
differential, the 1500-case fuzz or the counter's 164 cases reaches it.

### 5.5 Output formatting

This tool's stdout is byte-identical to `hyprctl workspacerules -j` (§3.2).  The
landed tool prints the same array in a compact single-line form.  Both parse to the
same JSON, so the counter (which compares parsed JSON) does not see the difference.

### 5.6 Internal-only differences

Error signalling (exceptions vs `None` returns), helper names and file layout
differ; the observable behaviour does not, apart from §5.1–§5.5.

## 6. Files changed by this seat

* `/fast/scratch/hyaku/mado-r27/data/ExecWsToolC/mado-wsrules.py` — the deliverable
  (second implementation; sha256 `dcf5c8c05b2d5b68ef967df339f7539a762e56c8a3811d7fbef33db9936ca389`).
* `/fast/scratch/hyaku/mado-r27/data/ExecWsToolC/{selftest.py,probe_oracle.py,rawbytes.py,difftest.py,fuzz.py,trees/,probe/,evidence/,laneclone/}`
  — test scaffolding and transcripts (scratch).
* this report.

No file of the fleet repo was modified: no git/jj mutation in the lane repo, no
touch of `tools/`, `corpus/SOURCES.md`, `SCORECARD.md`, `LOG.md`, `quality/` or
`.ufo/state|watchdog.log`.  The only write into the lane repo is this report at
`.ufo/waves/round-27/w3/reports/ExecWsToolC.md`.  The `laneclone/` directory is a
separate clone under this seat's scratch, used only to run the frozen counter against
this seat's file.

## 7. Tools installed or updated

None.  No package was installed, upgraded or removed by this seat (no `pacman`, no
`uv tool`, no release binary); everything used was already present on the host
(python3, git, bubblewrap, the pinned Hyprland build and the round-27 harness).

## 8. Risks and blockers

* **The landed tool fails the frozen C1 predicate** (§5.1, receipt
  `c1-after-48b9434a.txt`: 19/41 `TARGET_MISSED`).  This seat cannot fix it: the
  write scope for this wave excludes `tools/`.  The one-character fix
  (`field[delimiter + 16:]` → `field[delimiter + 17:]` at `tools/mado-wsrules.py:574`)
  is handed to the L1.  Note that this seat's file is *not* a drop-in replacement by
  policy, so the L1's options are (a) fix the landed file in place, or (b) keep the
  claim unmeasured for C1.
* The `$HOME`-style case (§3.4) cannot be adjudicated across the two sandboxes; it is
  reported as measured, not as a pass.
* The environment-variable difference (§5.2) means the two tools would disagree on a
  config that references an environment variable; whether the landed tool's "no
  environment variables" limit is the accepted round-27 rule is the L1's call — the
  pinned Hyprland expands them.
* The variable-order tie-break (§5.4) is unverified for prefix-overlapping names; no
  available case exercises it.
