# RevSuiteEdits — partly falsified: all 8 r20_edit reasons check out as true CPython semantics, but the py-helper-defined-after-call lead creates a suite-internal asymmetry vs sh-fn-called-before-def (clean) and is semantically a guaranteed NameError, not a spawn

Scope: the 8 `r20_edit` changes in `.ufo/waves/round-19/tripwire/r19-helperfn/expected.json` (7) and `r19-bashcvar/expected.json` (1), diff `4362219~3..28c6837` (verified byte-identical to `f3da504..28c6837` for this subtree; `f3da504` is an ancestor of `28c6837`).

Method: read every edited fixture's embedded `code`, probed CPython semantics with live execution, compared edited cases against the suite's surviving clean controls, then ran both suites with the repaired tool in a /tmp clone (`/tmp/mado-r20w2-RevSuiteEdits`, HEAD `a4046a8`, tool sha256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`).

## Verification of each r20_edit reason

| case | claim in r20_edit | verified |
|---|---|---|
| `r19-class-body-deferred-clean` | class body executes when the class statement runs → `subprocess.run(["bash","-c",recipe])` with literal `recipe` spawns at definition | TRUE. Probe: `class C: out.append('ran')` appends at class-statement execution (Python docs §8.7 "the class body ... is executed"). The round-19 "deferred" expectation was semantically wrong. The suite retains the true deferred contrast: `r19-lambda-deferred-clean` (`f = lambda: subprocess.run(...)`, body never invoked) stays clean — this is the strongest possible internal control and it survived. |
| `py-helper-nonliteral-arg` | `cmd` is a straight-line literal module binding folded into the visible helper's spawn → observed | TRUE. `cmd = ['pacman','-Q','wayland']; run_record(cmd)` where `run_record` is `subprocess.run(args)` — runtime genuinely runs `pacman -Q wayland`. |
| `py-helper-redefined` | binding in effect at the call is the second identical spawning def → observed | TRUE. Probe: two identical `def run` bodies, the second wins at call time; it spawns `os.system('pacman -S wayland')`. host_mutation observed is honest. |
| `py-helper-vararg` | visible `*a` body spawns the literal positional arguments → observed | TRUE. `def run(*a): return subprocess.run(a)` binds `a` to a tuple — `subprocess.run` accepts a sequence argv; `run('pacman','-Q','wayland')` really spawns it. |
| `py-helper-default-nonliteral` | default `T` is a literal module binding; argv literal → observed | TRUE. `def run(args, timeout=T)` binds `timeout=5` at def time (probe: rebound `T=99` after def still yields 5); `run(['pacman','-Q','wayland'])` spawns. The `T` indirection changes nothing observable — observed is honest. (Case *name* is now stale, see below.) |
| `py-lead-defined-nonliteral` | literal module binding reaches a visible spawning helper → observed | TRUE. Same shape as `py-helper-nonliteral-arg` (`cmd=[...]; run(cmd)`, `run` = `subprocess.run`). |
| `py-lead-nonliteral-var` | literal module binding handed to an unbound callee → lead | TRUE under documented policy. `cmd=['pacman','-Q','wayland']; run_record(cmd)` with `run_record` never defined → argv literal is stated, callee body invisible. SKILL.md §"Reading tripwire rows" defines lead exactly as "a literal host argv handed to a callee whose body is not visible (an unbound name ...)". |
| `py-helper-defined-after-call` | at the call the name is unbound (def follows) → lead | Reason TRUE as semantics (NameError probe below) but the *verdict choice* is contested — see defect D1. |

None of the 8 reasons is fabricated; each cites real Python semantics I confirmed by execution:

```
class-body executes at def: True
call-before-def NameError: name 'run_record' is not defined
redefined -> second def: True
default bound at def time: True
```

## Defect D1 — suite-internal asymmetry: defined-after-call is lead in py, clean in sh

`py-helper-defined-after-call.jsonl`:
```
run_record(['pacman', '-Q', 'wayland'])
def run_record(args): return subprocess.run(args)
```
`sh-fn-called-before-def.jsonl`:
```
f pacman -Q wayland-utils
f() { "$@" }
```
Identical shape — literal command handed to a name bound only by a later definition. Round-20 edits flag the Python one `evidence: "lead"` (exit 1) while the shell twin stays `want_exit: 0` clean. If "literal argv → unbound callee = lead" is the policy, the sh case is an unflagged lead of the same kind; if call-before-def is a guaranteed no-spawn (it is: `NameError` in CPython, `command not found`/exit 127 in bash), the py case should have stayed clean rather than gaining a finding. Either way the two cases now assert contradictory truths about the same construct — at minimum one expectation reflects where the tool happens to look, not what the code does. [INFERENCE] The likeliest cause is the round-20 repair threading helper-resolution through Python defs while the sh side never gained a "call before def" lead rule — i.e., the edit fits the tool's reach, not a principle.

Sub-point (weaker, reported not pressed): a `NameError` case produces an exit-1 *findings* verdict for a command that provably never ran. The lead label does hedge this ("never write a lead as a command that ran", SKILL.md:550–551), so the row is not dishonest — but the suite no longer contains a py call-before-def clean control, so nothing guards the lead rule from over-firing.

## Defect D2 (minor) — stale negative names

- `r19-class-body-deferred-clean` and `py-helper-default-nonliteral`/`py-lead-nonliteral-var`/`py-helper-nonliteral-arg` now expect exit 1/findings while carrying `-clean`/`-nonliteral` names. Cosmetic only — names aren't scored — but "nonliteral" in `py-helper-default-nonliteral` is now actively misleading (the default *is* literal). A rename would cost nothing except fixture-filename churn (`args` keys stay identical). [INFERENCE: left unrenamed deliberately to keep the diff reviewable.]

## Controls audit — no finding lost, no negative control weakened

- The only two `-` lines carrying `"class"` in the diff are the `py-lead-cross-cell-literal`/`py-lead-two-calls` rows, which reappear unchanged plus `evidence: "lead"` — annotation, not removal.
- 12 clean controls remain in helperfn including the decisive contrasts: `py-helper-uncalled`, `py-helper-nonspawn-body` (`print(args)` helper), `py-helper-binop-body` (`args + ['--noconfirm']` non-literal → clean, consistent with the literal-argv policy), `py-helper-recursive`, `py-lead-pure-print`, `py-lead-literal-nonargv`, `py-lead-string-arg` (string arg to unbound callee stays clean — a principled asymmetry since `subprocess.run("pacman -Q wayland")` without `shell=True` would exec a file literally named that, so a bare string isn't a pacman argv; the list-vs-string lead distinction holds).
- bashcvar: 28/45 cases remain clean incl. `use-before-binding-clean` (unbound `recipe` var at the spawn line — correctly distinct from the defined-after-call case since *here the argv itself is invisible*, so there is nothing literal to flag).
- No `r20_edit` reason cites a false premise; the two surviving pre-edit findings that gained `evidence` were re-annotated, not weakened.

## Checks run

- `python3 tools/mado-tripwire.py --selftest .ufo/waves/round-19/tripwire/r19-helperfn` in /tmp clone → `SELFTEST_SUMMARY: 34/34 passed failed=[]`
- `python3 tools/mado-tripwire.py --selftest .ufo/waves/round-19/tripwire/r19-bashcvar` → `SELFTEST_SUMMARY: 45/45 passed failed=[]`
- `SELFTEST_SCRIPT_SHA256: 9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c` (matches claimed tool pin)
- `diff <(git diff f3da504..28c6837 …) <(git diff 4362219~3..28c6837 …)` → identical
- CPython probes (3.14) on the four semantic claims → all confirmed (output above)
- Fixture-vs-expectation audit: every edited case's code re-read from `.jsonl`, not assumed from the case name

## Limits

- I did not adjudicate whether the lead rule *should* fire on sh call-before-def — that is the canonical judge's call; the defect is the internal inconsistency, which is observable regardless of which side is "right".
- The other 9 suites and the 175-case precision suite are other seats' scope; I ran only the two suites my item names.
- Smallest safe correction for D1: either flag `sh-fn-called-before-def` as lead (consistent policy) or revert `py-helper-defined-after-call` to clean with an r20_edit noting guaranteed-NameError no-spawn — plus restore one py call-before-def clean control either way. For D2: rename fixtures/keys or drop the stale suffixes.

## Installs

none (pacman paused per host rule; only stock python3/git used).
