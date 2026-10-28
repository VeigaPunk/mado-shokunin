# R55W2MutTool3 — mutation probe of `tools/mado-kbdopts.py` (structural parser)

Subject: `tools/mado-kbdopts.py` at 57584ed67716340b3d466fa04333ac0bab3fb79e (blob sha256 `9c69dd62…c2`, equal to the lane worktree).
Method: 21 one-edit mutants (each a single exact-once substring replacement on a copy in scratch; the lane was never written).
Each mutant was run against the 26 fixtures (18 committed `c2/F01..F18`, 8 hold-out `c2-holdout/H01..H08`; argv from `args.json`,
cwd = export root, stdout bytes and exit status compared with `expected.out` / `expected.rc`) and against its own `--selftest`.
Baseline: the unmodified tool passes 26/26 and `MADO_KBDOPT_SELFTEST: 83/83 assertions passed` (rc 0).

## Score table

"fixtures killed" lists the fixtures whose stdout bytes or rc differ. "selftest killed" = rc ≠ 0 or output ≠ `83/83`.
Survivor = passes all 26 fixtures. Per-mutant files: `mutants/<ID>/mado-kbdopts.py`, `mutants/<ID>/edit.diff`.

| mutant | edit (original → mutant) | fixtures killed (ids) | selftest killed? | survivor |
|---|---|---|---|---|
| M01 | `if stack:` / `stack.pop()` → `stack.pop()` (stray `}` at empty stack) | none | yes (IndexError, rc 1, no stdout) | **SURVIVOR** (fixtures); kill K-M01 |
| M02 | `if not stack:` (device forget) → `if False:` | none | yes (82/83) | **SURVIVOR**; kill K-M02 |
| M03 | `if not stack:` (device forget) → `if True:` (forget on every pop) | none | yes (82/83) | **SURVIVOR**; kill K-M03 |
| M04 | `stack.pop()` → `stack.clear()` | H02 | yes (82/83) | killed (hold-out only) |
| M05 | `stack, cur = [], None` → `stack, cur = st.__dict__.setdefault('stack', []), None` (stack survives file start) | none | yes (82/83) | **SURVIVOR**; kill K-M05 |
| M06 | `cur = rhs.split("#", 1)[0].strip(WS)` → `cur = rhs.strip(WS)` (name keeps comment) | none | yes (82/83) | **SURVIVOR**; kill K-M06 |
| M07 | device key before name: `st.unsupported += 1` → `+= 0` | H01 | yes (80/83) | killed (hold-out only) |
| M08 | `if in_device and lhs == "name":` → `if stack and lhs == "name":` (nested `name =` renames device) | none | **no** (83/83) | **SURVIVOR** (both); kill K-M08 |
| M09 | `in_device = stack == ["device"]` → `bool(stack) and stack[0] == "device"` | H02 | yes (82/83) | killed (hold-out only) |
| M10 | `stack.append(line[:-1].strip(WS))` → `stack.append(line[:-1])` | F02–F14, F18, H01–H08 (22) | yes (70/83) | killed |
| M11 | `if not line or line[0] == "#":` → `if not line:` (full-line `#` not skipped) | none | **no** (83/83) | **SURVIVOR** (both); kill K-M11 |
| M12 | `line.split("=", 1)` → `line.rsplit("=", 1)` (split on last `=`) | none | **no** (83/83) | **SURVIVOR** (both); kill K-M12 |
| M13 | `if line == "}":` → `if line.startswith("}"):` | none | **no** (83/83) | **SURVIVOR** (both); kill K-M13 |
| M14 | `key = ":".join(stack + [lhs])` → `":".join(stack[-1:] + [lhs])` | none | **no** (83/83) | **SURVIVOR** (both); kill K-M14 |
| M15 | `if bracket or "$" in line or` → `if bracket or` (RHS `$` not unsupported) | none | yes (82/83) | **SURVIVOR** (fixtures); kill K-M15 |
| M16 | `WS = " \t\r\n\v\f"` → `WS = " \t\r\n"` (VT/FF not stripped) | none | **no** (83/83) | **SURVIVOR** (both); kill K-M16 |
| M17 | `if lhs.startswith("$") or lhs == "source":` → `if lhs.startswith("$"):` | none | no | **EQUIVALENT** (no kill exists; see below) |
| M18 | `if lhs.startswith("$") or lhs == "source":` → `if lhs == "source":` (`$` LHS not ignored) | none | **no** (83/83) | **SURVIVOR** (both) — *not* equivalent; kill K-M18 |
| M19 | `if bracket or "$" in line` → `if "$" in line` (bracket check dropped from unsupported test) | none | no | **EQUIVALENT** (no kill exists; see below) |
| M20 | control: `or (bracket and key.rsplit(":", 1)[-1] in NAMES)` → `or False` | F10 | yes (81/83) | killed (committed) |
| M21 | control: `st.devices.setdefault(cur, {})` → `st.devices[cur] = {}` (merge → overwrite) | F09 | yes (82/83) | killed (committed) |

Totals: 21 mutants. 6 killed by fixtures (M04, M07, M09, M10, M20, M21). Of the 19 non-equivalent mutants, 13 survive all 26
fixtures (M01, M02, M03, M05, M06, M08, M11, M12, M13, M14, M15, M16, M18); 7 of those also survive their own selftest (M08, M11, M12, M13, M14, M16, M18).
The 18 committed fixtures alone kill only 3 of 21 (M10, M20, M21); the 8 hold-out fixtures add M04, M07, M09.

## Survivor kills (13 non-equivalent) — minimal config, expected output, original-vs-mutant

Each kill is a plain config text inside the contract grammar of `registration.md` §C2 (v1) and `registration-v2.md` E7, which
the errata does not change. The "expected" column is derived by hand from the contract text, then checked: the ORIGINAL tool
matches it byte-for-byte for all 13 (`receipts/repro-output.txt`). Files: `mutants/<ID>/kill/`.

| id | minimal config (exact bytes; `\n` = newline) | argv | expected per contract (original) | mutant output | contract clause |
|---|---|---|---|---|---|
| K-M01 | `}\ninput:repeat_rate = 30\n` | `--config k.conf` | `keyboard=* repeat_rate=30 … from=G/-/- unsupported=0`; DONE `unsupported=0 live=NONE`; rc 0 | rc 1, `IndexError: pop from empty list`, empty stdout | **contract silent** on a `}` with an empty stack; expected = no-op, completed run |
| K-M02 | `device {\nname = a\n}\ndevice {\nrepeat_rate = 50\n}\n` | `--config k.conf --keyboard a` | `keyboard=a repeat_rate=25 … from=-/-/- unsupported=1`; DONE `unsupported=1` | `repeat_rate=50 … from=D/-/- unsupported=0` | v1 §C2: "when the stack empties the current device is forgotten"; device key with no current device → unsupported +1 |
| K-M03 | `device {\nname = a\ntouchpad {\n}\nrepeat_rate = 50\n}\n` | `--config k.conf --keyboard a` | `repeat_rate=50 … from=D/-/- unsupported=0` | `repeat_rate=25 … from=-/-/- unsupported=1` | v1 §C2: device forgotten only when the stack empties (nested close keeps it) |
| K-M05 | file `k1.conf`=`input {\n`; file `k2.conf`=`repeat_rate = 30\n` | `--config k1.conf --config k2.conf --keyboard kbd-a` | `repeat_rate=25 … from=-/-/- unsupported=0` | `repeat_rate=30 … from=G/-/- unsupported=0` | v1 §C2: "the category stack and the current device reset at each file's start" |
| K-M06 | `device {\nname = kbd-a # kbd\nrepeat_rate = 50\n}\n` | `--config k.conf --keyboard kbd-a` | `repeat_rate=50 … from=D/-/- unsupported=0` | `repeat_rate=25 … from=-/-/- unsupported=0` | v1 §C2: device name "with a trailing `#`-comment cut" |
| K-M08 | `device {\nname = a\nfoo {\nname = b\n}\nrepeat_rate = 50\n}\n` | `--config k.conf --keyboard a --keyboard b` | `a: repeat_rate=50 … from=D/-/-`; `b: repeat_rate=25 … from=-/-/-`; both `unsupported=0` | `a: 25 -/-/-`; `b: 50 D/-/-` | v1 §C2: name line recognised only "With stack exactly [\"device\"]" |
| K-M11 | `#note {\ninput {\nrepeat_rate = 30\n}\n` | `--config k.conf` | `repeat_rate=30 … from=G/-/- unsupported=0` | `repeat_rate=25 … from=-/-/- unsupported=0` | v1 §C2: "a line whose first character is `#` is skipped" |
| K-M12 | `input:repeat_rate = 30=1\n` | `--config k.conf` | `repeat_rate=25 … from=-/-/- unsupported=1` (RHS `30=1` not an int) | `unsupported=0` | v1 §C2: "LHS and RHS are … before/after the FIRST `=`" |
| K-M13 | `input {\n}x\nrepeat_rate = 30\n}\n` | `--config k.conf` | `repeat_rate=30 … from=G/-/- unsupported=0` (`}x` is ignored, not a pop) | `repeat_rate=25 … from=-/-/- unsupported=0` | v1 §C2: "exactly `}` pops the stack" |
| K-M14 | `device[a] {\nfoo {\nrepeat_rate = 3\n}\n}\n` | `--config k.conf` | `repeat_rate=25 … from=-/-/- unsupported=1` (KEY `device[a]:foo:repeat_rate` starts `device[`) | `unsupported=0` | v1 §C2: "KEY is the stack joined with `:` then `:` then LHS"; bracket rule |
| K-M15 | `input {\n numlock_by_default = true$x\n}\n` | `--config k.conf` | `numlock=0 … from=-/-/- unsupported=1` (line contains `$`) | `numlock=1 … from=-/-/G unsupported=0` | v1 §C2: "a line containing `$`, `{{` or a backslash adds one to `unsupported`" |
| K-M16 | `input {\nrepeat_rate = 30\x0c\n}\n` (`\x0c` = FF) | `--config k.conf` | `repeat_rate=30 … from=G/-/- unsupported=0` | `repeat_rate=25 … from=-/-/- unsupported=1` | v1 §C2: "stripped of space, tab, CR, LF, VT, FF" |
| K-M18 | `device[a] {\n$x:repeat_rate = 3\n}\n` | `--config k.conf` | `repeat_rate=25 … from=-/-/- unsupported=0` (LHS starting `$` is ignored) | `unsupported=1` | v1 §C2: "an LHS starting with `$` … ignored"; the LHS may contain `:` so its KEY matches the bracket rule |

Runnable repro (original vs mutant, plus hand-expected check; prints 13/13 killed):
`python3 -I mutants/receipts/repro.py /abs/path/to/mutants` (the original is `mutants/original/mado-kbdopts.py`, a byte copy of the lane tool).
Output: `receipts/repro-output.txt`; machine results: `repro-results.json` (all 13 `status=ORIG_MATCHES_HAND_EXPECTED`, `killed=True`).

Controls for the kills: every kill config is parsed by the original as a normal run (rc 0, never `SETUP`). K-M14 and K-M15 print `unsupported=1` on the original, as the contract requires for those lines. The original passes all 26 fixtures, so the kills are not syntactic rejections of the instrument.

## Equivalent mutants (no config can kill them)

- **M17** (`source` LHS not ignored). The `source` branch has no effect on state: `source` is never in OPTIONS, never an in-device
  name (not in NAMES), never a bracket key's last component (not in NAMES). Only the `name` branch could be affected, and it requires
  LHS = `name`. Fuzz: 0 / 200 000 disagreements (`receipts/fuzz-results.json`).
- **M19** (bracket check dropped from the unsupported test). For a bracket key, the original adds one and ignores the line. The mutant
  reaches the value parse, which also adds one on an invalid value; on a valid value it reaches `elif cur is None` and adds one,
  because `cur` is provably `None` on every bracket key. Invariants: stack empty ⇒ `cur is None` (reset on the emptying pop and at file
  start); stack non-empty with `stack[0]` starting `device[` ⇒ `cur` was `None` when that frame opened and only `stack == ["device"]`
  can assign it. Fuzz: 0 / 200 000.

These two are reported as equivalent, not as SURVIVORS of the contract; they are not counterexamples to the fixture suite.

## Fuzz (differential, in-process, `receipts/fuzz.py`, seed 5521, 200 000 random 1–2-file configs over a 70-token vocabulary)

Non-equivalent mutants disagree with the original on 1–35 925 of the 200 000 cases (M08 1, M02 1, M03 2, up to M10 35 925); the equivalents on 0 (M17, M19). M02 and M03 disagree on
only 1 and 2 of 200 000 random configs: the fuzz is too weak to find them (device-forget needs a specific 5-line sequence), so their
kill comes from the hand-derived config, not from the fuzz. Fuzz numbers are per-mutant counts only; the table above and the kill
configs are the evidence.

## Frozen harness on each mutant (`quality/check-r55-controls.py --claim c2`, 2026-10-28)

Scratch repo (not the lane): `git -C <D> init`, `rev-parse --show-toplevel` asserted equal to `<D>`, the lane tree at 57584ed exported
by `git archive` into `<D>`, then one commit per mutant with `-c user.name=ctl -c user.email=ctl@ctl`, and the frozen harness run
with `--repo <D> --rev <commit> --work <W>` (the harness reads tool, fixtures and controls from git objects at `--rev`). Receipts:
`receipts/harness/M*.out`, `commit-map.txt`, `repo-log.txt`. The `--rev` of each line is the scratch commit that carries the mutant
blob (verified with `git show <rev>:tools/mado-kbdopts.py | sha256sum`).

| mutant | harness verdict | fixtures / holdout | note |
|---|---|---|---|
| pristine | TARGET_MET | 18/18, 8/8, holdout_commit=ok, controls 3/3 | baseline |
| M01, M02, M03, M05, M06, M08, M11, M12, M13, M14, M15, M16, M18 | **TARGET_MET** | 18/18, 8/8 | the frozen C2 predicate passes 13 mutants that violate v1 §C2 text |
| M17, M19 | TARGET_MET | 18/18, 8/8 | equivalent |
| M04, M07, M09, M10, M20, M21 | TARGET_MISSED | — | killed by fixtures (as in the table) |

## Limits

- The 13 survivors are violations of the contract text, not of Hyprland itself: the contract is the oracle here. Whether real Hyprland 0.56.2
  behaves as the contract says on these inputs was NOT checked (no source re-open this round for these clauses; no hyprctl run).
- K-M01 rests on a clause the contract does not state (stray `}` at empty stack). The original's answer (no-op) is the tool's documented
  choice; the contract is silent. Treat M01 as a crash-robustness probe, not a contract violation.
- Mutants were generated by a script over exact-once substrings in scratch copies (`receipts/gen.py`); the script and edit diffs are
  the record. No lane file was written; the lane blob hash was checked before and after (`9c69dd62…c2`, unchanged).
- `receipts/drive.py` and `receipts/gen.py` hard-code the scratch root `/fast/scratch/hyaku/mado-r55/R55W2MutTool3`; `repro.py`
  and `fuzz.py` take the mutants directory as an argument and are the runnable receipts.
