# AdvHelperFn — breaks

Adversarial test of the two helper rules shipped at tip `01b80946d92b26370d3012a7da655d00dd135154`
(`tools/mado-tripwire.py`, file sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`):
(A) same-text helper def + literal call substitution, (B) "call to a name this text resolves neither to a
same-text helper nor to a spawn function", handed a literal argv list, is a *lead*.

The pinned suite reproduces (**34/34**), and C3's 6/6 reproduces. But the rules **as stated in the shipped
docstring** do not hold on several ordinary test-harness shapes: rule B emits `host_mutation` from pure data
(`frozenset([...])`, `format([...])`), and from same-text helpers the text *does* define but the resolver does
not index (decorated, async, duplicate, class, lambda, parameter/local). Rule A loses two-hop `$@` forwarding
entirely: a wrapper that runs `sudo pacman -S` scans **clean**. Lead findings are byte-identical in schema to
real spawn findings, so nothing downstream can tell them apart. Shadowing/def-line false positives are
**pre-existing at the baseline** (verified), not introduced here, but rule A has `funcs` in hand and does not
use it.

Verdict is on the *rules' claims*; the integration of the file itself is not attacked here.

## Attack setup

```
$ git -C <lane> show 01b80946…:tools/mado-tripwire.py > /tmp/tw-tip.py   # sha256 367be947… (== worktree file)
$ git -C <lane> show 9c54c56…:tools/mado-tripwire.py > /tmp/tw-base.py # sha256 c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd
$ python3 -I /tmp/tw-tip.py --selftest .ufo/waves/round-19/tripwire/r19-helperfn | tail -2
SELFTEST_SCRIPT_SHA256: 367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d
SELFTEST_SUMMARY: 34/34 passed failed=[]
```

Probes are my own synthetic one-line OMP-shaped JSONL files under `/tmp/advhelperfn/` (no real transcript bytes
copied). Each was scanned individually:

```
python3 -I /tmp/tw-tip.py --scan /tmp/advhelperfn/<probe>.jsonl
```

Proposed regressions are in `/tmp/advhelperfn/suite-proposed/` (`expected.json` + 14 fixtures) and were run with
`--selftest`; they score **0/14 today**, which is the red-before for every delta below.

## Case matrix (synthetic payloads)

| probe | payload (synthetic) | expected (real execution / doc) | got | class |
|---|---|---|---|---|
| b01 | `run_case('q', ['pacman','-Q','wayland-utils'])`, callee undefined | lead per doc | exit 1, package_query `pacman:-Q` | doc-consistent |
| b02 | same call under `if False:` | argv stated but never executed | exit 1, package_query | lead is not an execution claim; precision cost |
| b10 | imported `log_argv(['pacman','-Q',…])` | doc: imported helper is a lead | exit 1, package_query | doc-consistent |
| b11 | same-text `def note(args): print(args)` | no body spawns | clean | ok |
| b14 | `def run_all(run_case): run_case('q',['pacman','-Q',…])` | name bound as a parameter | exit 1 | **FP (B overclaim)** |
| b15 | nested `def log(args): print(args)` + call | text defines it | exit 1 | **FP** |
| b20 | `async def note(argv): return print(argv)` + call | body only prints; unawaited coroutine never runs | exit 1 | **FP** |
| b21 | `@functools.lru_cache def note(argv): return ' '.join(argv)` + call | body only formats | exit 1 | **FP** |
| b22 | two `def note(...)` (dup), last only prints | last def wins, only prints | exit 1 | **FP** |
| b07 | same-text `class Case` ctor `Case(['pacman','-Q',…])` | text defines `Case` | exit 1 | **FP** |
| b17 | same with `@dataclass` | text defines `Case` | exit 1 | **FP** |
| b08 | `r = lambda a: print(a); r(['pacman','-Q',…])` | text defines `r` | exit 1 | **FP** |
| b09 | `record = None; record(['pacman','-Q',…])` | text binds `record` to `None` | exit 1 | **FP** |
| b04 / b05 | `print([...])` / `json.dumps([...])` | pure | clean | ok |
| b06 | `format(['pacman','-Q','wayland-utils'])` | pure formatter | exit 1, package_query | **FP** |
| b16b | `frozenset(['pacman','-Q','wayland-utils'])` | pure container | exit 1, package_query | **FP** |
| b23 | `frozenset(['pacman','-S','wayland-utils'])` | pure container | exit 1, **host_mutation `pacman:-S`** | **FP, top severity class** |
| b24 | `format(['sudo','pacman','-Syu','wayland-utils'])` | pure formatter | exit 1, **host_mutation `sudo` + host_mutation `pacman:-Syu`** | **FP, top severity class** |
| b18b / b19b | `deque([...])` / `expect([...])` flat argv | pure container / undefined lead | exit 1 | FP (B overclaim) / lead-by-design |
| b12 | call then `def` (module level) | NameError at call | clean | ok |
| b13 | keyword-only `log_argv(argv=[...])` | documented miss | clean | ok (stated) |
| a03 | `f() { f "$@"; }; f pacman -Q wayland-utils` | runtime loops, no host command | clean, terminates | ok |
| a04 | mutual recursion `f`↔`g` | loops | clean, terminates | ok |
| a05 | `f() { sudo "$@"; }; f pacman -S wayland-utils` | sudo + pacman -S | both findings | ok |
| a09 | `f() { bash -c "$1"; }; f 'pacman -Q wayland-utils'` | package_query | found | ok |
| a10 | `f() { "$1" -S wayland-utils; }; f pacman` | host_mutation | found | ok |
| a08 | call before def, top level | bash: not found at that line | clean | ok |
| a18 | `f() { g "$@"; }; g() { "$@"; }; f pacman -Q wayland-utils` | runtime runs `pacman -Q` | **clean** | **FN (A)** |
| a22 | same two hops, `f sudo pacman -S wayland-utils` | runtime runs `sudo pacman -S` | **clean** | **FN, host_mutation missed** |
| a20 | `run(){"$@"}; b(){ run sudo pacman -S "$@"; }; b wayland-utils` | sudo + pacman -S | **clean** | **FN** |
| a24 | `main(){ run pacman -Q …; }` + `run(){ "$@"; }` + `main` | pacman -Q | clean | FN (textual-order limit) |
| a25 | py: `def build(): return go([...])` then `def go(argv): subprocess.run(argv)` then `build()` | subprocess.run literal | clean | FN (textual-order limit) |
| a13 / a14 | `f pacman -Q 'wayland-*'` / `f pacman -Q ~/.config` | pacman -Q stated | clean | conservative miss (guard) |
| a01 | `pacman() { echo shadowed; }; pacman -Q wayland-utils` | bash runs `echo` | **host_mutation `pacman` + package_query `pacman:-Q`** | **FP (baseline-inherited)** |
| a02 | `sudo() { echo no; }; sudo pacman -S wayland-utils` | bash runs `echo` | sudo + pacman:-S | **FP (baseline-inherited)** |
| a15/a16 | definition alone: `pacman() { echo shadowed; }`, `sudo() { echo no; }` | issues nothing | host_mutation `pacman` / `sudo` | **FP (baseline-inherited)** |
| a17 | `git() { echo no; }` alone | issues nothing | clean | ok |

## Findings

**F1 — B's definition test is narrower than the docstring says (FP on same-text helpers).**
Docstring: "a call to a name this text resolves neither to a same-text helper nor to a spawn function"
(`tools/mado-tripwire.py:41-43`). The index that decides "resolves" is built at `:1368-1372` from
`tree.body` only, `isinstance(node, ast.FunctionDef)` only, and `not node.decorator_list` only. So
`AsyncFunctionDef`, decorated defs, `ClassDef`, nested defs, duplicate names, lambdas and assigned locals are
all "unresolved", even when every one of them has a body visible in the same text that cannot spawn. The lead
site `:1431-1433` then classifies the argv. Evidence: b20 (`async def`, body print), b21 (`@lru_cache`,
`' '.join`), b22 (dup def, last prints), b07/b17 (`class`/`@dataclass` ctor), b08 (lambda), b09
(`record = None`), b14 (parameter), b15 (nested def) all exit 1 with package_query `pacman:-Q`. The wave-1
report discloses "top-level `def`s (no decorators) are indexed" in its rule text; the shipped docstring does
not, and its "resolves" sentence reads as if it would.

**F2 — the pure-data exemption is a closed list, so data literals become host_mutation.**
`PURE_ARG_CALLS` (`:1252-1256`) omits `format`, `frozenset`, `deque`, `bool`, `int`, `hash`, …; the docstring
says "Pure data calls (`print`, `json.dumps`, ...) are exempt" (`:46-49`), which reads as a category, not an
enumeration. Worst observed, from pure formatting/containers:

```
$ python3 -I /tmp/tw-tip.py --scan /tmp/advhelperfn/b24-format-sudo.jsonl
MADO_TRIPWIRE: findings
  host_mutation sudo           | sudo pacman -Syu wayland-utils
  host_mutation pacman:-Syu    | pacman -Syu wayland-utils
$ python3 -I /tmp/tw-tip.py --scan /tmp/advhelperfn/b23-frozenset-mutation.jsonl
MADO_TRIPWIRE: findings
  host_mutation pacman:-S      | pacman -S wayland-utils
```

Also note `json.dumps` is exempt only because dotted callees never reach the lead branch at all
(`:1431` requires `ast.Name`), so the example in the docstring does not exercise `PURE_ARG_CALLS`.

**F3 — "reported as a lead" is not observable in the verdict.**
The finding record (`:1596-1602`) carries `file,line,tool_call_id,timestamp,tool,class,rule,argv0,command` and
nothing marking provenance. A direct `subprocess.run(['pacman','-Q','wayland-utils'])` and the rule-B lead for
the same rule produce identical objects apart from `file`, and `--permit package_query` silences both:

```
spawn keys: ['argv0','class','command','file','line','rule','timestamp','tool','tool_call_id']
lead  keys: ['argv0','class','command','file','line','rule','timestamp','tool','tool_call_id']
difference: {'file': ('…/c01-direct-spawn.jsonl', '…/b01-table-direct.jsonl')}
c01 --permit package_query -> MADO_TRIPWIRE: permitted_only  (permitted: ['package_query'])
b01 --permit package_query -> MADO_TRIPWIRE: permitted_only  (permitted: ['package_query'])
```

The per-call dedup key is `(class, rule)` (`:1590-1595`), so a lead and a real spawn of the same rule in one
tool call collapse to one record (c03: `go()` spawn + `log_argv` lead → one finding). Downstream precision
work (e.g. "how many leads are data-only?") cannot be measured from the verdict as shipped.

**F4 — rule A resolves exactly one hop, so two-hop `$@` forwarding is invisible (FN).**
`:870-875` expands a same-text helper body and re-enters `classify_shell(expanded, depth+1)`; that call
recomputes `funcs = shell_functions(pairs)` (`:855`) from the *expanded text*, which contains no defs. Every
definition is therefore lost after the first hop:

```
$ python3 -I /tmp/tw-tip.py --scan /tmp/advhelperfn/a22-twohop-sudo.jsonl
MADO_TRIPWIRE: clean                       # f() { g "$@"; }; g() { "$@"; }; f sudo pacman -S wayland-utils
$ python3 -I /tmp/tw-tip.py --scan /tmp/advhelperfn/a20-wrapper-realfn.jsonl
MADO_TRIPWIRE: clean                       # run(){"$@"}; b(){ run sudo pacman -S "$@"; }; b wayland-utils
```

Bash executes both — the second is a complete `sudo pacman -S` host mutation. The python side has the opposite
design (`depth < 4` with `funcs` threaded through, `:1411-1419`) and the suite pins `py-helper-two-hop` as a
positive; the shell docstring (`:36-39`) states no one-hop limit and the report's rule text says only
"(A) Same-text helper … substitutes … and re-classifies the expanded body" — it does not say the callee
definitions vanish. The same textual-order condition (`idx > defn[0]` `:871`; `node.lineno > helper[0]`
`:1411`) also misses a deferred call to a helper defined later in the file (a24 shell, a25 python:
`build()` → `go([...])` → `subprocess.run(argv)` scans clean).

**F5 — shadowing and definition lines are classified as invocations (FP; baseline-inherited, not fixed).**
`classify_shell` calls `classify_segment` on every segment of every line *before* consulting `funcs`
(`:866-875`), so the definition line `pacman() { … }` (the `()` token splits the line, leaving segment
`['pacman']`) is read as `pacman` with no args → `host_mutation`; and a later call to a name that a same-text
function shadows is classified as the host binary although bash runs the function:

```
$ python3 -I /tmp/tw-tip.py --scan /tmp/advhelperfn/a01-shadow-pacman.jsonl
  host_mutation pacman            | pacman
  package_query pacman:-Q         | pacman -Q wayland-utils
```

`/tmp/tw-base.py --scan` gives the same two findings at `9c54c56`, so this is pre-existing base behavior; rule A
now has `funcs` at the call site and could gate on it, but does not. `pacman() { echo shadowed; }` alone yields
`host_mutation pacman` (a15) at both revisions.

**F6 — recursion is safe (pass).** a03 (self) and a04 (mutual) terminate clean, and a 3-hop chain (a23) also
terminates; `classify_shell` re-enters with a definition-free text so recursion decays after one expansion and
the `depth > 8` guard (`:852`) is not reached. No hang, no stack blow-up.

**F7 — forwarding positives work (pass).** `sudo "$@"` (a05), `bash -c "$1"` (a09) and `"$1"` as argv0 (a10)
all produce the expected classes; `"$@"` inside a double-quoted string that is not a command (logging
`echo "issuing: $@"`) does not create a finding.

**F8 — conservative guard (not counted as defect).** Any metacharacter in the call's arguments (`$`, backtick,
`*`, `?`, `[`, `{`, `~`, newline; `SHELL_EXPANSION` `:579`, guard `:871-872`) skips substitution, so
`f pacman -Q 'wayland-*'` (a13) and `f pacman -Q ~/.config` (a14) scan clean even though the body is `"$@"`
and the command is stated. Documented only as "nothing is substituted unless the call text states it
literally"; this is conservative, but worth a limit line.

## C3 cross-check (independent)

`python3 -I .ufo/waves/round-19/tw-recall.py 01b80946…` → `incident_lines: 6, detected: 6, score: 10.0`, rc 0.
Attribution: instrumenting `helper_argv_leads` on the frozen inputs shows `r13-root.jsonl:4` is detected
**only** by rule B — with leads disabled that line yields zero findings — one of the six is rule-B-carried and
none is rule-A-carried. So C3's numerator is honest, but it measures recall only: B's false-positive surface
(F1/F2) and A's two-hop miss (F4) are outside what the 6/6 number can see.

## Proposed regression cases

Suite format as in `.ufo/waves/round-19/tripwire/r19-helperfn/expected.json` (one fixture per case in the same
directory). `want_*` encode the behavior I argue is correct, so every case currently fails — that is the
red-before. Fixture payloads are below the JSON; all are synthetic.

```json
{
  "schema": "mado-tripwire-selftest-v1",
  "note": "AdvHelperFn round-19 w2 proposed regressions. B-resolution hardening, B pure-data, A two-hop. Every case fails on tip 367be947.",
  "cases": [
    {"name": "py-async-def-format-only",   "args": ["py-async-def-format-only.jsonl"],   "want_exit": 0, "want_label": "clean", "want_findings": []},
    {"name": "py-decorated-def-format-only","args": ["py-decorated-def-format-only.jsonl"],"want_exit": 0, "want_label": "clean", "want_findings": []},
    {"name": "py-dup-def-format-only",     "args": ["py-dup-def-format-only.jsonl"],     "want_exit": 0, "want_label": "clean", "want_findings": []},
    {"name": "py-class-ctor-argv",         "args": ["py-class-ctor-argv.jsonl"],         "want_exit": 0, "want_label": "clean", "want_findings": []},
    {"name": "py-lambda-bound-argv",       "args": ["py-lambda-bound-argv.jsonl"],       "want_exit": 0, "want_label": "clean", "want_findings": []},
    {"name": "py-local-none-argv",         "args": ["py-local-none-argv.jsonl"],         "want_exit": 0, "want_label": "clean", "want_findings": []},
    {"name": "py-format-builtin-argv",     "args": ["py-format-builtin-argv.jsonl"],     "want_exit": 0, "want_label": "clean", "want_findings": []},
    {"name": "py-frozenset-flat-argv",     "args": ["py-frozenset-flat-argv.jsonl"],     "want_exit": 0, "want_label": "clean", "want_findings": []},
    {"name": "py-expect-flat-argv",        "args": ["py-expect-flat-argv.jsonl"],        "want_exit": 0, "want_label": "clean", "want_findings": []},
    {"name": "py-param-runner-table",      "args": ["py-param-runner-table.jsonl"],      "want_exit": 0, "want_label": "clean", "want_findings": []},
    {"name": "sh-twohop-at-forward",       "args": ["sh-twohop-at-forward.jsonl"],       "want_exit": 1, "want_label": "findings", "want_findings": [{"class": "package_query", "rule": "pacman:-Q", "line": 1}]},
    {"name": "sh-wrapper-sudo-twohop",     "args": ["sh-wrapper-sudo-twohop.jsonl"],     "want_exit": 1, "want_label": "findings", "want_findings": [{"class": "host_mutation", "rule": "sudo", "line": 1}, {"class": "host_mutation", "rule": "pacman:-S", "line": 1}]},
    {"name": "sh-shadow-def-only",         "args": ["sh-shadow-def-only.jsonl"],         "want_exit": 0, "want_label": "clean", "want_findings": []},
    {"name": "sh-shadow-call",             "args": ["sh-shadow-call.jsonl"],             "want_exit": 0, "want_label": "clean", "want_findings": []}
  ]
}
```

Fixture payloads (`eval` → `arguments: {"language":"py","code":…}`; `bash` → `{"command":…}`, OMP JSONL shape as
in the existing suite):

```json
{
  "py-async-def-format-only":    {"tool": "eval", "payload": "async def note(argv):\n    return print(argv)\nnote(['pacman','-Q','wayland-utils'])\n"},
  "py-decorated-def-format-only":{"tool": "eval", "payload": "import functools\n@functools.lru_cache\ndef note(argv):\n    return ' '.join(argv)\nnote(['pacman','-Q','wayland-utils'])\n"},
  "py-dup-def-format-only":      {"tool": "eval", "payload": "def note(argv):\n    return print('a')\ndef note(argv):\n    return print('b')\nnote(['pacman','-Q','wayland-utils'])\n"},
  "py-class-ctor-argv":          {"tool": "eval", "payload": "class Case:\n    def __init__(self, argv):\n        self.argv = argv\nCase(['pacman','-Q','wayland-utils'])\n"},
  "py-lambda-bound-argv":        {"tool": "eval", "payload": "r = lambda a: print(a)\nr(['pacman','-Q','wayland-utils'])\n"},
  "py-local-none-argv":          {"tool": "eval", "payload": "record = None\nrecord(['pacman','-Q','wayland-utils'])\n"},
  "py-format-builtin-argv":      {"tool": "eval", "payload": "format(['pacman','-Q','wayland-utils'])\n"},
  "py-frozenset-flat-argv":      {"tool": "eval", "payload": "frozenset(['pacman','-Q','wayland-utils'])\n"},
  "py-expect-flat-argv":         {"tool": "eval", "payload": "expect(['pacman','-Q','wayland-utils'])\n"},
  "py-param-runner-table":       {"tool": "eval", "payload": "def run_all(run_case):\n    return run_case('q', ['pacman','-Q','wayland-utils'])\n"},
  "sh-twohop-at-forward":        {"tool": "bash", "payload": "f() { g \"$@\"; }\ng() { \"$@\"; }\nf pacman -Q wayland-utils\n"},
  "sh-wrapper-sudo-twohop":      {"tool": "bash", "payload": "run() { \"$@\"; }\nb() { run sudo pacman -S \"$@\"; }\nb wayland-utils\n"},
  "sh-shadow-def-only":          {"tool": "bash", "payload": "pacman() { echo shadowed; }\n"},
  "sh-shadow-call":              {"tool": "bash", "payload": "pacman() { echo shadowed; }\npacman -Q wayland-utils\n"}
}
```

Notes on the proposed split: the first ten pin rule B's resolution/exemption claims; `sh-twohop-at-forward` and
`sh-wrapper-sudo-twohop` pin rule A's dual behavior (one-hop must keep working, ≥2 hops must not silently
drop); `sh-shadow-*` are **baseline-inherited** pins (failing at `9c54c56` too) and are optional for the
helper-fn suite — if included, they change base classification of every transcript with a shadowed host-command
name, so L1 should decide scope before landing. If the F1 shapes are judged acceptable leads, the fix is at
minimum a docstring limit line naming the excluded def shapes, and a `lead: true` field (F3) so downstream
work can count them; neither changes a suite pin. b02/b10/b14 are doc-consistent leads — precision cost only,
not proposed as regressions.

## Limits

- Synthetic probes only; corpus frequency of the B false positives is not measured here. CriticC3W2 reported
  independently (message, not re-verified by me) that rule B adds exactly 2 lines over 4805 stable transcripts,
  both real — so the defect is a specification/precision overclaim with apparently small corpus cost [INFERENCE
  from their note; my evidence is the shape, not the frequency].
- I did not run the gate, the round-18 frozen replay, or the other suites; I ran `--selftest` on the
  `r19-helperfn` suite (34/34), `--scan` on my probes, and `tw-recall.py` for C3. The tool's own guarantee that
  `ast` bodies are never executed was relied on: no probe code was executed.
- `async def` non-execution and decorator/lambda semantics are CPython behavior asserted from the language, not
  observed by running the probes [INFERENCE].
- Whether a lead should ever carry `host_mutation` (F2 severity) is a policy call for L1, not measured here.
- Rule A's >=2-hop and later-def misses sit at the edge of the docstring's "defined earlier in the SAME text"
  wording; I classify them as unstated limits (the python side does resolve hops, and the shell text is fully
  present), not as plain contradictions.

## Installs

none.
