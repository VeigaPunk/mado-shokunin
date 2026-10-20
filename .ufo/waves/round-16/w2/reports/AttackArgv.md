# AttackArgv — finite basename screen: path, trailing slash, control characters

Seat: `MadoR16.AttackArgv` (leaf reviewer, read-only, no subagent dispatch).
Baseline: `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`. Target root:
`/home/vgpnk/Projects/shokunin/mado-shokunin`.

Scope: attack the argv[0] basename screen of `tools/mado-action-plan.py` (`_basename`,
its call in `_classify`, the argv checks in `_validate_plan`) on trailing slash, path
prefixes, whitespace, NUL/control characters, and shell-shaped names. Confirm that no
command is resolved or executed.

Execution: **none.** No gate, selftest, measure, frozen run, shell probe, package, service,
compositor, input or host operation. Every counterexample below is derived by reading the
source and the Python semantics it relies on; each is tagged `[INFERENCE from source; not
executed]`. L1 owns verification.

Tooling: nothing installed or updated. Pacman transactions remain paused; no pacman query.

Snapshot note: `tools/mado-action-plan.py` changed while this review ran (tags `#8440` →
`#FD91` → `#D3C7`; the file now reads each input once and uses `O_NOFOLLOW`). The argv screen
did not change: `_basename` (lines 319-324 at `#FD91` and `#D3C7`), its call site (349-355) and
`_validate_plan` argv checks (313-315 at `#FD91`) read the same. Line numbers below are
`#FD91`/`#D3C7`. Findings after this note are about that snapshot.

## 1. Mechanism under attack (source, verified by reading)

```
# tools/mado-action-plan.py:319-324
def _basename(arg0):
    stripped = arg0.strip()
    if not stripped:
        return ""
    return stripped.rstrip("/").rsplit("/", 1)[-1]
```

```
# tools/mado-action-plan.py:349-355 (in _classify, allowed kinds only)
exe = _basename(argv[0]) if argv else ""
if not exe: -> empty_argv (1)
if exe in deny_exec: -> denied_executable:<exe> (1)
```

Order of operations is: whole-string `strip()` (Unicode whitespace), then strip trailing `/`
characters, then take text after the last `/`. Only exact equality with the 12 names in
`PINNED_DENY_EXECUTABLES` (`tools/mado-action-plan.py:109-112`) refuses.

What the screen does **not** do:

- `_validate_plan` (`:292-316`) accepts any list of strings for `argv`. Argv elements are
  not checked for NUL, control characters, interior whitespace, or shell metacharacters.
- No argv[0] shape check exists: no regex, no "must be a plain name", no "reject trailing
  slash as malformed". Malformed-argv handling is limited to `argv` being a list of strings
  and to empty-after-normalization (`empty_argv`).
- `strip()` is applied before `rstrip("/")`, so the trailing-slash rule depends on whether
  a space sits in front of the slash.

Python semantics relied on `[INFERENCE from Python docs; not executed]`: `str.strip()` with
no argument removes characters for which `str.isspace()` is true (includes ASCII whitespace,
`\x1c`-`\x1f`, `\x85`, `\xa0`, and other Unicode spaces). `\x00`, `\u200b` and other
non-space code points are not removed. JSON `\u0000`, `\t`, `\n` in strings decode to those
code points with the standard `json` module; raw control bytes are rejected by strict mode.

## 2. Counterexamples (argv[0] under `read-source`, committed paused policy)

Expected outcome is the one the code path yields by source trace `[INFERENCE from source;
not executed]`. "Consumer bypass" means: `plan_safe` is reported while the shape would run a
denied program if the downstream consumer renders argv[0] into a shell line or splits it on
whitespace. Under an execve-style consumer the shape names no real file and is inert.

| # | argv[0] (JSON form) | trace | predicted verdict | note |
|---|---|---|---|---|
| C1 | `"sudo/"` | strip → `sudo/` → rstrip → `sudo` | exit 1 `denied_executable:sudo` | held |
| C2 | `"sudo /"` | strip → `sudo /` → rstrip → `sudo ` → basename `sudo ` | **exit 0 `plan_safe`** | trailing-slash rule defeated by a preceding space; shell render runs `sudo` with operand `/` |
| C3 | `"sudo\u0000"` | NUL not stripped → basename `sudo\x00` | **exit 0 `plan_safe`** | a C-string consumer truncates to `sudo`; Python `os.execv`/`subprocess` raise on NUL rather than exec, so a Python-native consumer is not bypassed |
| C4 | `"\u0000sudo"` | NUL not stripped | **exit 0 `plan_safe`** | same class as C3 |
| C5 | `"sudo -S"` | interior space kept → basename `sudo -S` | **exit 0 `plan_safe`** | shell-joined consumer runs sudo |
| C6 | `"x\nsudo"` (escaped `\n`) | interior newline kept → basename `x\nsudo` | **exit 0 `plan_safe`** | line-oriented consumer sees a second command |
| C7 | `"sudo\tcat"` | interior tab kept | **exit 0 `plan_safe`** | whitespace-splitting consumer sees `sudo` |
| C8 | `"true;sudo"` / `"sudo;id"` | no `/`, no whitespace; basename is whole string | **exit 0 `plan_safe`** | shell metacharacters: any string-rendering consumer runs the second command |
| C9 | `"sudo/."` and `"sudo/./"` | rstrip removes `/` only at the end; basename `.` | **exit 0 `plan_safe`** | lexical divergence from POSIX `basename`. Not an execve path: `sudo/.` names a directory component, so no exec. Low |
| C10 | `"/usr/bin/sudo /"` | basename `sudo ` | **exit 0 `plan_safe`** | path-qualified form of C2 |
| C11 | `"\u200bsudo"` (zero-width space) | not whitespace to `strip()` → basename `\u200bsudo` | **exit 0 `plan_safe`** | no exec path for execve. Low. A Unicode-normalizing consumer could fold it, which is not checked |
| C12 | `"sudo\u00a0"` | NBSP is whitespace to `strip()` → `sudo` | exit 1 `denied_executable:sudo` | held (over-denial) |
| C13 | `"  sudo"` / `"sudo\n"` | stripped → `sudo` | exit 1 `denied_executable:sudo` | held (over-denial) |
| C14 | `"sudo/ "` | strip → `sudo/` → rstrip → `sudo` | exit 1 `denied_executable:sudo` | asymmetry with C2: `sudo/ ` denied, `sudo /` allowed |
| C15 | `"libinput-debug-events"` under `read-source` | basename not in list | **exit 0 `plan_safe`** | sibling binary. Its class is raw-input capture, which is blocked only by the `input-capture` label. Declared limit; see F3 |
| C16 | `"libinput-record"`, `"evtest-qt"`, `"pacman-key"`, `"systemd-run"`, `"paccache"`, `"busctl"` under `read-source` | exact-name list | **exit 0 `plan_safe`** | same family limit. Binary names come from the lane's corpus (S051) and other seats' reports, not from host inspection |
| C17 | `"sudo"` with `kind: "net-fetch"` / any non-pinned kind | unknown kind first | exit 1 `unknown_action_kind` | held |
| C18 | `"sudo"` under `package-install` | label precedence | exit 1 `blocked_action_kind:package-install` | held (the label decides first; this is the label-trust limit in F4) |

Blank and whitespace-only argv[0] (`"  "`, `""`, `"/"`) yield `empty_argv` (exit 1). Held.

## 3. Findings (severity ordered)

### F1 — High (conditional on consumer): argv[0] normalization is inconsistent, so the denied-executable finding is false for some shapes

Shapes C2, C3/C4, C5–C8, C10 produce `plan_safe` (exit 0) even though the program a shell
or C-string consumer would run is a denied name. The finding is the gate's only content
check on argv, and it reports "no listed basename" for these shapes. The gate's own
docstring (`tools/mado-action-plan.py:5-13`) and SKILL (`SKILL.md:533-539`) describe
`plan_safe` as "no listed argv[0] basename". For C2 the basename the screen actually
inspects is `sudo ` (with a trailing space), not `sudo`; the claim is therefore not what
the code tests.

Severity is High only if a consumer renders argv[0] into a shell string or uses a C-string
API. The gate states it never executes argv, and the consumer is not in the repo
(`[INFERENCE]`: no caller of this gate exists in-tree beyond SKILL and the selftest). Under
a strict execve consumer these shapes are inert, and C3/C4 are rejected by Python's
`subprocess` before any exec. The defect is still real: the finding names one program and
the screen examined a different string.

Anchors: `tools/mado-action-plan.py:321-324` (strip, then rstrip), `:292-316` (no argv
element shape check), `:349-355` (decision point).

### F2 — Medium: no fixture pins any argv[0] shape the screen mishandles, and the seat design rules were not adopted or recorded as accepted

- `tools/mado-action-plan.py` selftest argv[0] cases (`:514-565` at `#D3C7`): `/usr/bin/pacman`
  (`read-disguised-pacman`), `sudo`, `bash`, `env`, empty `[]`, and blank `"  "`. None
  covers NUL, interior whitespace or newline, a trailing slash (`sudo/`, `sudo /`), a
  trailing `/.`, or shell metacharacters.
- `.ufo/waves/round-16/safety-cases.json` (450 lines) has no case with such argv[0]. Its
  `scope_limit` (line 17) says the screen is a "finite 12-basename screen" and names
  `omarchy-pkg-add`, `python3 -c` as residuals. It does not name the shapes in §2.
- The seat designs ExitMap H-table row (`.ufo/waves/round-16/w1/reports/ExitMap.md:48`,
  "empty/whitespace/control-char/trailing-slash argv0 → exit 2 `action_malformed`") and
  FindingStability rows 2.7 and 2.9 (`.ufo/waves/round-16/w1/reports/FindingStability.md:98-100`,
  NUL → malformed, `argv_program`) recommended malformed exit 2 for these. The landed code
  does neither. The dispatch spec (`w1/spec.json`, SafetyGate) does not require these rules,
  so this is a design gap against the lane's own review, not a spec violation. Nothing in
  `adjudication.json` (`bounded_not_expanded` lists wrapper holes only) records it as
  accepted.

Result: the fail-closed claim for argv[0] is untested for the shapes most likely to break
it. The round-15 incident was a literal `sudo` argv, which the screen does catch.

### F3 — Medium (declared limit, but the boundary is under-described for the incident family)

The exact-name list does not cover hyphenated siblings of denied names. The counterexample
that matters is C15: `libinput-debug-events` under `read-source` is `plan_safe`. That binary
is the raw-input-capture tool the `input-capture` kind exists to block (S051 `tools.rst`
names it, per `corpus/knowledge` and the round-15 lesson). The screen passes it because the
basename `libinput-debug-events` is not `libinput`. The only protection is the plan's own
`kind` label, which the plan author declares.

Fixtures do not pin this boundary. `read_source_libinput_debug_events_help`
(`safety-cases.json:319-330`) uses the parent path `/usr/bin/libinput debug-events --help`,
which is caught by `libinput`. The `residual_control` cases pin `omarchy-pkg-add` (`:411-422`)
and `python3 -c` (`:424-436`) only. The round-16 `scope_limit` names those two but not
`libinput-*`, `pacman-key`, `systemd-run` or the other C16 names. The boundary for the exact
incident family is therefore unrecorded.

Declared-limit status: the SKILL wording ("no listed argv[0] basename") is accurate for C15.
It is still a gap a reader would not expect from the round-15 incident.

### F4 — Low: kind label is self-declared; the basename screen is the only content check

Stated plainly for claim honesty. `{"kind":"read-source","argv":["rm","-rf","x"]}` and
`{"kind":"read-source","argv":["tee","/etc/x"]}` pass as `plan_safe` `[INFERENCE from source;
not executed]`. The kinds `package-install`, `service-mutate`, `compositor-mutate`,
`input-capture` are blocked only when the author labels the action with them. This is the
design (declared plan), and SKILL says so. It is listed because F3 depends on it.

### F5 — Low: basename is non-POSIX; a reader will assume `os.path.basename` semantics

`_basename` (`:319-324`) does `strip()` then `rstrip("/")` then `rsplit`. `os.path.basename`
and `posixpath.basename` do neither. Behaviour differs on C2, C9, C14. The docstring says
"Pure-string basename" and the SKILL row says "basename of argv[0]" without specifying the
normalization. A reader comparing with POSIX will get C2 and C14 wrong. Recommended: say so
in the docstring and SKILL row, or change the normalization (see §5).

## 4. Held controls (verified by reading source)

- **No resolution, no execution of supplied argv.** `subprocess` appears only in
  `_self_invoke` (`:489-492`, `shell=False`, `-I`, fixed `[sys.executable, script, ...]`).
  `shutil.which`, `os.path.exists/isfile/realpath/abspath` on argv, `os.stat`, `os.access`,
  `os.exec*`, `os.spawn*` and `shell=True` do not appear in the file (grep at `#D3C7`).
  `os.path.realpath(__file__)` (`:497`) is the script, not argv. Basename is pure string.
- **Output injection via `denied_executable` is closed.** The rendered `<exe>` can only be
  one of the 12 pinned names, because the finding is emitted only when `exe in deny_exec`.
  `blocked_action_kind:<kind>` renders only pinned kinds. `unknown_action_kind` detail is
  `json.dumps`-encoded in the verdict line, and `plan_malformed` detail is JSON-encoded too.
- **Policy/code drift fails closed.** `_validate_policy` requires
  `set(deny_executables) == PINNED_DENY_EXECUTABLES` (`_validate_policy`, `:232-289` at `#FD91`). Removing a
  name from either the code set or the policy list yields `policy_malformed` (exit 2) rather
  than a silent weakening.
- **Blank argv[0] and `/` alone are refused.** `"  "`, `""`, `"/"` → `empty_argv` (exit 1).
- **Over-denial on whitespace around a name.** `"  sudo"`, `"sudo\n"`, `"sudo\u00a0"` are
  denied, because the strip runs before the comparison.

## 5. Proposed fix (L1 decision; not applied)

1. Replace the normalization with a shape check on argv[0], applied before classification,
   and refuse non-matching shapes as `plan_malformed` (exit 2):
   argv[0] must match `^[A-Za-z0-9._+@/-]+$` (no whitespace, no control characters, no NUL,
   no shell metacharacters), must not end in `/`, and its basename after the last `/` must be
   non-empty. This refuses C2, C3–C8, C10, C14, C9 (`sudo/.`: `.` is the final component, so
   reject a final component of `.` or `..`) and C11 (non-ASCII). It keeps C1, C12 and C13 as
   they are or moves them to malformed.
2. Compute the basename with `rsplit("/", 1)[-1]` on the validated string. Drop `strip()` and
   `rstrip("/")`.
3. Pin each of §2 C1–C15 as a selftest case and a `safety-cases.json` row, with the exit and
   finding stated by the fixed rule. Pin C15 as a `residual_control` so the sibling boundary
   is recorded, not implied.
4. Add a `scope_limit` sentence naming the sibling family and the self-declared kind.

## 6. Predicted verdicts for L1 verification (not run)

Under the current code (`#D3C7`), by source trace `[INFERENCE from source; not executed]`:
C1 exit 1, C2 exit 0, C3 exit 0, C5 exit 0, C8 exit 0, C9 exit 0, C12 exit 1, C14 exit 1,
C15 exit 0. Under the §5 fix: C2, C3, C5, C8, C9 exit 2 `plan_malformed`; C1 exit 2 or 1
(decide with L1); C12, C14 exit 2; C15 unchanged (exit 0) and pinned as a residual.

Commands for L1 (each as a one-plan JSON file, `read-source` kind, against
`.ufo/waves/round-16/safety-policy.json`): `python3 -I tools/mado-action-plan.py --plan <f>
--policy .ufo/waves/round-16/safety-policy.json`. Each argv[0] in §2 is one case; no plan
should be run with a live argv.

## 7. Verification gaps and limits

- Nothing was executed. Every verdict in §2 and §6 is a source-trace prediction.
- Python `str.strip()`, `str.isspace()`, JSON escape decoding and `subprocess`/`os.execv`
  NUL behaviour are cited from documented semantics, not observed here.
- No downstream consumer of `plan_safe` exists in the lane. Severity in F1 depends on that
  consumer, which is not in this repo.
- The file changed during review (three tags). Re-check §1 anchors against the final
  snapshot before L1 adjudicates.
- Out of this seat's scope: the frozen-mode digest/parse ordering and symlink handling
  (`run_frozen`, `_read_regular`) are assigned to other attack seats. Not reviewed here.
- Interpreter-level wrappers (`timeout`, `nice`, `env` with an unlisted name, `python3 -c`)
  and argv[1..] content are owned by ExecBasename / SafetyService. Not re-attacked here.
