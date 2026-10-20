# AtkCasesL — partly falsified: 12 of 18 L expectations rest on a `lead` definition written after the measurement, `dc-pytest-param` pins a known miss, and three cases cannot discriminate what they name

Scope: every `family: "L"` case in `.ufo/waves/round-20/precision/expected.json` (18 cases,
lines 664, 2124, 2145, 2172, 2199, 2226, 2247, 2344, 2385, 2432, 2481, 2502, 2579, 2600,
2621, 2698, 2761, 2782), re-scanned with the 28c6837 (sha256 `9613f510…`) and 1f7f995
(sha256 `367be947…`) tools, plus 1f7f995's pre-harm predecessor 9c54c56 (`c1ae45a7…`).
Leaf seat: no delegation. All work ran in `/tmp/mado-r20w2-AtkCasesL`; the lane was
read-only (`git show`/`log`/`cat-file` only), no `jj`, no host operation, fixture code
was parsed as data and never executed.

## Axis

One axis only: **does each L case's `want_exit`/`want_findings` (class, rule, line,
evidence) follow from CPython semantics and from the round-20 contract?** Not the tool's
quality in general, not the W/H/S/P families.

## Reproduction (what would have shown the opposite)

Counter from my clone, committed bytes only:

```text
cd /tmp/mado-r20w2-AtkCasesL
python3 -I .ufo/waves/round-20/tw-precision.py 28c6837   # L 17/18, P 66/66, S 17/17, W 21/22, H 51/52; 172/175, score 9.8286
python3 -I .ufo/waves/round-20/tw-precision.py 1f7f995   # L 1/18; 29/175, score 1.6571
python3 -I .ufo/waves/round-20/tw-precision.py 9c54c56   # L 1/18; 110/175, score 6.2857
```

`28c6837`'s only L red is `L-AdoptW2-AdvHelperFn-b14` (`got exit 0, []`). At both 1f7f995
and 9c54c56 the only L green is `L-AdoptW2-AdvHelperFn-c01`. All 18 case digests match
`expected.json` at the suite pin f3da504 (verified with `hashlib.sha256` over the case
bytes), and all 18 `before` fields re-measured exactly as written (fail/fail, except c01
pass/pass). Full counter JSON and per-case scans are saved beside this report for L1 to
commit (wave-2 output is uncommitted by contract):
`.ufo/waves/round-20/w2/AtkCasesL/precision-{28c6837,1f7f995,9c54c56}.json` and
`.ufo/waves/round-20/w2/AtkCasesL/scans.txt` (sha256 `912add75…`); lab fixtures and their
digests under `.ufo/waves/round-20/w2/AtkCasesL/lab/`.

Confirmation by counterexample: for the three shapes where the wanted answer is right, the
tool output that would have shown the opposite is on record — `reset-lead` and
`reset-cleared-helper` give `observed` at 1f7f995 and `lead` at 28c6837 (reset-blind
following of the visible spawning body would keep `observed`); `c03` gives one collapsed
`observed` row at 1f7f995 and `observed`+`lead` at 28c6837 (dedup on class+rule alone would
lose the second row). Those three cases hold.

## Findings

### F1 — (high) The pre-registered `lead` definition does not cover 12 of the 18 L cases; the definition that does was written after the measurement

The pre-registration (read at `e629f73`, unchanged at the tip) defines the term in one
sentence:

- `SCORECARD.md:1246-1250`: "`evidence` is `observed` (…) or `lead` (**a literal argv
  handed to a callee whose body is not visible**)."

The enumerating version that the L cases actually use appears only later:

- `SKILL.md:548-549`: "`lead`: a literal host argv handed to a callee whose body is not
  visible (**an unbound name, a non-stdlib import, a parameter**)."

`git log -S "an unbound name, a non-stdlib import, a parameter" -- SKILL.md` gives exactly
`4362219` (the prose commit after the 28c6837 measurement); the phrase is absent at
`e629f73`, `f3da504` and `28c6837`. So the L family was scored at 28c6837 against a
definition that the pre-registration does not contain and that did not exist in any
committed file at measurement time.

Which cases depend on the broad reading (a call target that has **no body at all** or no
binding at the call site):

| dependency | cases |
|---|---|
| unbound name at the call (CPython `NameError`, measured below) | `L-CasePureCrossCell-reset-clears-helper`, `L-CaseLeadsInvisible-run-record`, `L-CaseLeadsInvisible-opaque-runner`, `L-CaseLeadsInvisible-reset-cleared-helper`, `L-AdoptW2-CriticC3W2-dc-cross-cell-fixture`, `L-AdoptW2-CriticC3W2-dc-pytest-param` (`expect` row), `L-AdoptW2-AdvHelperFn-b01`, `-b02`, `-b12`, `-b19b` |
| unbound name in a mixed cell | `L-AdoptW2-AdvHelperFn-c03` (`log_argv` row) |
| parameter, never called (no callee exists) | `L-AdoptW2-AdvHelperFn-b14` |

CPython check, run with harmless payloads (`python3 -I`, my own snippets, no fixture code):

```text
call-before-def -> NameError name 'run_case' is not defined
undefined       -> NameError name 'run_case' is not defined
del-then-call   -> NameError name 'f' is not defined
if-false        -> NO EXCEPTION (body not executed)
opaque-assign   -> NameError name 'make_runner' is not defined
```

A `lead` is honest in the narrow sense ("argv text stated, body not visible"), and the
final SKILL makes it deliberate policy; but the pre-registered sentence requires a
*callee*, and these 12 have none. Only 6 L cases are derivable from the pre-registration
alone: the five non-stdlib-import cases (whose imported callee may exist) and the `c01`
`observed` control. [INFERENCE] If the narrow sentence had governed at measurement time and
the affected wants were rewritten to clean, L would read 6/18 and C1 161/175, not L 17/18
and 172/175. I did not re-score that counterfactual; it is arithmetic from the table.

Consequence for the claim: the C1 row's L number is a *broad-definition* result, and the
definition was completed after the number. It is not a tool defect; it is a claim-scope
defect that L1 must either accept explicitly (adopt the SKILL wording retroactively as
the contract) or restate the L result under the pre-registered sentence.

Corroborating and independent: `.ufo/waves/round-19/w2/reports/AdvHelperFn.md:62` (the
seat that first built the b12/b14 payloads) records `b12` as "NameError at call | clean |
ok" — i.e. the payload's author, before round 20, read the same code as *clean*, not lead.

### F2 — (high; rule reading [INFERENCE]) `L-AdoptW2-CriticC3W2-dc-pytest-param` is wrong: it omits two rows the declared rule demands and thereby pins a known miss

Case (`expected.json:2432`): `CASES=[pytest.param(['sudo','pacman','-S','x'],'host_mutation')]`
then `expect(['pacman','-Qi','walker'],'package_query')`; want = one `pacman:-Qi` lead.
Its own `why` says "E2: pytest.param(...) is an attribute call (stays unflagged)".

`pytest.param` is a callee whose body is not visible (non-stdlib import, body outside the
transcript). The declared rule (`SKILL.md:548-549`; also the tool's own docstring at
`tools/mado-tripwire.py:42-44`, "unresolved bare name **or imported external callable**")
makes a literal `['sudo','pacman','-S','x']` handed to it a `lead`. The case instead wants
that argv silent, and the tool agrees — but only because of an undeclared carve-out:

```text
lab/attr_pytest_param.jsonl   import pytest;   pytest.param(['sudo','pacman','-S','x'],'host_mutation')
  tool-28: exit 0 []                                   # no row
lab/bare_pytest_param.jsonl   from pytest import param; param(['sudo','pacman','-S','x'],...)
  tool-28: exit 1 [sudo lead, pacman:-S lead]           # same callable, bare import
lab/attr_mod_sudo.jsonl       import labtools; labtools.run(['sudo','pacman','-S','x'])
  tool-28: exit 0 []                                   # any imported-module attribute call
lab/bare_mod_sudo.jsonl       from labtools import run; run(['sudo','pacman','-S','x'])
  tool-28: exit 1 [sudo lead, pacman:-S lead]
```

So one `sudo pacman -S` literal is a lead when the callee is imported by name and silent
when the same callable is reached through the module object. The case therefore adds the
`expect` lead (unbound name) while recording an unflagged `sudo`/`pacman:-S` as correct:
it asks the detector to be *more* sensitive for one imported callee and *less* sensitive
for the other, and the corpus carries no note that the difference is intended. Criterion 30′ asks for "committed
negatives of the shapes the new rule could misread"; this is the opposite — the shape is
committed as a *clean* case inside the lead family, so the negatives set has a hole where
the tool's implementation deviates from the prose. Either the attribute-call carve-out must
be declared in the contract (and its recall cost accepted), or the case must want the two
`sudo`/`pacman:-S` leads.

### F3 — (high) `b14` is a contract contradiction, not a clean tool miss; C1's "3 misses" includes a case no document resolves

`sources`: `expected.json:2621`; `SCORECARD.md:1329` ("a lead for a parameter callee inside
a never-called def; not implemented").

- Wanted: `package_query pacman:-Q @1 lead`. `SKILL.md:549` lists "a parameter" as a lead.
- Tool: nothing, citing `tools/mado-tripwire.py:40-41` "Uncalled helpers do not establish
  an execution path."
- Measured, tool-28:

```text
lab/b14.jsonl                    def run_all(run_case): return run_case('q',[...])        exit 0 []
lab/b14_called_pure.jsonl        ... + run_all(print)                                    exit 1 [lead]
lab/b14_called_spawner.jsonl     ... + run_all(spawn)  (spawn = subprocess.run wrapper) exit 1 [lead]
lab/b14_called_real_spawner.jsonl ... + run_all(subprocess.run)                          exit 1 [lead]
lab/c_uncalled_direct.jsonl      def go(): subprocess.run(['pacman','-Q','a'])  (uncalled) exit 0 []
   (the same file at tool-1f: exit 1 [observed])
```

Two things follow. (a) The parameter rule is emitted *unconditionally once the helper is
called*, even when the caller passes `print`/`len` (provably no spawn): `lab/param_pure_caller`
(`run_all(len)`) → lead. So the wanted row would carry no information about the callee.
(b) The same uncalled-body suppression that silences b14 is what fixed a real old false
positive: an uncalled def containing a direct literal spawn read `observed` at 1f7f995 and
`clean` at 28c6837. b14 asks for the lead inside that suppressed region; that is implementable
("no `observed` claim from an uncalled body, but a `lead` is not an execution path"), but
neither the pre-registration nor the tool docstring states it, and the tool's sentence reads
the other way. The assembler knew: `CaseAdoptW2.md:147` (F4) records the flip from the case
author's "clean", and `AdvHelperFn.md:47` rates the lead an **FP**. L1 must rule on the
sentence, not "fix" b14; a fix must not re-open the uncalled-direct-spawn false positive.

### F4 — (high) `b02` is a non-discriminating duplicate of `b01`; the dead-code shape it names is untested and the tool mislabels it `observed`

`L-AdoptW2-AdvHelperFn-b02` (`expected.json:2502`) differs from `b01` only by the
`if False:` wrapper; both want exactly `package_query pacman:-Q @1 lead`, and both get it:

```text
lab/...-b01.jsonl  run_case('q',['pacman','-Q','wayland-utils'])          tool-28: [pacman:-Q@1 lead]
lab/...-b02.jsonl  if False: run_case('q',['pacman','-Q','wayland-utils']) tool-28: [pacman:-Q@1 lead]
```

The wanted multiset is invariant to the dead branch, so the case cannot test "dead code
stays a lead" beyond the generic unbound-name row; its only discriminating power is to
*reject* a reachability-aware repair. Worse, the tool has no dead-code model where it
matters — a dead branch with a **visible** spawn is labelled an execution:

```text
lab/dead_direct.jsonl  import subprocess; if False:     subprocess.run(['pacman','-Q','a'])
lab/dead_if0.jsonl     import subprocess; if 0:         subprocess.run(['pacman','-Q','a'])
lab/dead_while.jsonl   import subprocess; while False:  subprocess.run(['pacman','-Q','a'])
  tool-28: exit 1 [package_query pacman:-Q @1 observed]     (all three)
```

`observed` for unreachable code is an execution claim and is a worse error than a `lead`;
no case in P/S/W/H/L pins that shape. `b02` therefore provides false comfort: it scores a
dead-code claim as green without ever exercising dead code.

### F5 — (high) `import-alias` and `dc-import-classifier` do not discriminate what they name

- `L-CaseLeadsInvisible-import-alias` (`expected.json:2247`) wants `sudo`+`pacman:-S @1 lead` —
  byte-identical to `import-run-cmd`'s wanted multiset. A tool that never resolves an import
  alias (treats `launch` as an ordinary unresolved bare name) emits exactly those rows, so
  the case cannot distinguish alias resolution from no import handling at all. To test the
  alias, the wanted row would have to differ (e.g. an alias of a known-pure stdlib callable
  wanted clean).
- `L-AdoptW2-CriticC3W2-dc-import-classifier` (`expected.json:2344`) is the assembler's own
  admitted near-duplicate of `import-classify-argv` (`CaseAdoptW2.md:44`: "mine adds
  `import sys; sys.path.insert(0,'tools')`"). The added line is inert; both want the same
  two rows. N is inflated by 1 (0.57 % of C1, 1/18 of L).

Six L cases share the identical wanted multiset `package_query pacman:-Q @1 lead`
(`b01`, `b02`, `b12`, `b14`, `b19b`, `run-record`) and five share
`host_mutation sudo @1 lead` + `host_mutation pacman:-S @1 lead` (`import-run-cmd`,
`import-classify-argv`, `import-alias`, `dc-import-classifier`, `opaque-runner`). Distinct
source shapes still justify most of those, but the two above do not add discrimination.

### F6 — (high; disclosed, still load-bearing) `b12` and the round-19 pin edit turn a CPython-correct negative into a `lead`

`L-AdoptW2-AdvHelperFn-b12` (`expected.json:2600`) wants `lead` for a call that precedes its
`def`. The same shape is `.ufo/waves/round-19/tripwire/r19-helperfn/py-helper-defined-after-call.jsonl`;
that pin was **exit 0 / clean at 1f7f995** and was edited at 28c6837 to exit 1 / `lead`
(`.ufo/waves/round-19/tripwire/r19-helperfn/expected.json:114-121`, `r20_edit` at :121):

```text
r19-helperfn/py-helper-defined-after-call.jsonl  (call then def)
  tool-28: exit 1 [package_query pacman:-Q @1 lead]
  tool-1f: exit 0 []
```

CPython raises `NameError` at the call, so nothing is handed to any callee (demo above);
`AdvHelperFn.md:62` documented the shape as "clean, ok". The edit is disclosed and is
consistent with the final SKILL's "unbound name" wording, but it means the C1 guard
"every existing tripwire suite all-pass (a case edit only with its reason)" was met partly
by flipping a committed precision *negative*, not by preserving it. That guard cannot be
cited as evidence that the repair lost no precision on this shape; the contract itself was
redefined. Same class as F1.

### F7 — What holds (confirmations with the output that would have shown the opposite)

- `reset-lead`, `reset-cleared-helper`: genuine reset tests — 1f7f995 `observed` →
  28c6837 `lead`. A reset-blind tool that followed the visible body would emit nothing for
  `reset-lead` (its body is the pure `' '.join`) and `observed` for `reset-cleared-helper`
  (its body is `subprocess.run`); both would fail the wanted `lead`, so reset handling is
  actually exercised.
- `c03`: genuine per-call dedup test — 1f7f995 one `observed` row, 28c6837 `observed` +
  `lead` on the same (class, rule, line), separated only by `evidence`; the counter's
  multiset (`tw-precision.py:87,195`) preserves both.
- `c01`: an `observed` control that passes at both historical tools; it cannot evidence the
  repair (declared control in `AdvHelperFn.md`), but it would catch an observed→lead
  regression.
- The five non-stdlib-import cases are the only L cases whose wanted `lead` is derivable
  from the pre-registered sentence as written.

## Per-case verdict

| # | case (`expected.json` line) | want | got@28c6837 | CPython semantics of the fixture | verdict |
|---|---|---|---|---|---|
| 1 | `L-CasePureCrossCell-reset-clears-helper` (:664) | `pacman:-Q@3 lead` | same | `NameError` (reset cleared the only def) | holds under SKILL; broad-reading only |
| 2 | `L-CaseLeadsInvisible-run-record` (:2124) | `pacman:-Q@1 lead` | same | `NameError` | holds under SKILL; broad-reading only |
| 3 | `L-CaseLeadsInvisible-import-run-cmd` (:2145) | `sudo`, `pacman:-S` lead | same | body outside transcript (import may exist) | holds |
| 4 | `L-CaseLeadsInvisible-import-classify-argv` (:2172) | `sudo`, `pacman:-S` lead | same | body outside; truth is a classifier (author admits data) | holds; fail-closed policy |
| 5 | `L-CaseLeadsInvisible-opaque-runner` (:2199) | `sudo`, `pacman:-S` lead | same | `NameError` at `make_runner()`; `run` never bound | broad-reading only |
| 6 | `L-CaseLeadsInvisible-reset-cleared-helper` (:2226) | `pacman:-Q@2 lead` | same | `NameError` | holds under SKILL; broad-reading only |
| 7 | `L-CaseLeadsInvisible-import-alias` (:2247) | `sudo`, `pacman:-S` lead | same | body outside | holds, but **non-discriminating** (F5) |
| 8 | `L-AdoptW2-CriticC3W2-dc-import-classifier` (:2344) | `sudo`, `pacman:-S` lead | same | body outside; data in truth | holds, **author-admitted duplicate** (F5) |
| 9 | `L-AdoptW2-CriticC3W2-dc-cross-cell-fixture` (:2385) | 3 leads incl. `hyprctl:reload` | same | `write_case` unbound → `NameError` | broad-reading only |
| 10 | `L-AdoptW2-CriticC3W2-dc-pytest-param` (:2432) | `pacman:-Qi@1 lead` only | same | `expect` `NameError`; `pytest.param` literal is data, but its callee body is invisible | **wrong: omits `sudo`+`pacman:-S`** (F2) |
| 11 | `L-AdoptW2-AdvHelperFn-b01` (:2481) | `pacman:-Q@1 lead` | same | `NameError` | broad-reading only |
| 12 | `L-AdoptW2-AdvHelperFn-b02` (:2502) | `pacman:-Q@1 lead` | same | dead branch + `NameError` | **vacuous duplicate of b01** (F4) |
| 13 | `L-AdoptW2-AdvHelperFn-b10` (:2579) | `pacman:-Q@1 lead` | same | body outside transcript | holds |
| 14 | `L-AdoptW2-AdvHelperFn-b12` (:2600) | `pacman:-Q@1 lead` | same | `NameError` (call before def) | broad-reading only; pin flipped (F6) |
| 15 | `L-AdoptW2-AdvHelperFn-b14` (:2621) | `pacman:-Q@1 lead` | **exit 0, []** (red) | uncalled def: nothing executes | **contract contradiction** (F3) |
| 16 | `L-AdoptW2-AdvHelperFn-b19b` (:2698) | `pacman:-Q@1 lead` | same | `expect` unbound → `NameError` | broad-reading only |
| 17 | `L-AdoptW2-AdvHelperFn-c01` (:2761) | `pacman:-Q@1 observed` | same | literal `subprocess.run` | holds (control, passes at both) |
| 18 | `L-AdoptW2-AdvHelperFn-c03` (:2782) | `observed` + `lead` same rule/line | same | `go()` runs; `log_argv` unbound → `NameError` | holds; lead broad-reading only |

## Limits

- I did not run the gate, `--selftest` suites, recall counters, the isolation check, or the
  whole-corpus diff; other wave-2 seats own those. I read only committed bytes in my /tmp
  clone and ran only the committed precision counter plus my own scan fixtures.
- Fixture code was never executed. The CPython `NameError`/dead-branch facts were
  reproduced with harmless self-written snippets (`['true']`, no fixture payload).
- No `pacman`/`hyprctl`/service call of any kind; the dangerous strings appear only as
  fixture text parsed by `--scan`.
- The F2 rule reading (does "imported external callable" cover `module.attr`?) is marked
  [INFERENCE]; the measured asymmetry is not.
- The F1 counterfactual (L 6/18, C1 161/175 under the narrow pre-registered definition) is
  arithmetic, not a measurement.
- `expected.json` was read at the suite pin f3da504; the toolchain (python 3.14.8) and the
  counter are unchanged from the author's report. Unicode/line endings of the case files
  were not altered.

## Installs

none.
