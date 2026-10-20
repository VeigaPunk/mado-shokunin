# AtkCasesS — partly falsified: 15/17 S expectations hold; `del-run` and `del-run-cross-cell` pin a guaranteed NameError as a lead, and the S family cannot detect a resolver that prefers any pure def.

Target root `/home/vgpnk/Projects/shokunin/mado-shokunin` at `a4046a8`; suite pin
`f3da504` (no drift: `git diff --stat f3da504 a4046a8 -- .ufo/waves/round-20/precision*`
is empty, expected.json sha256 `1039c4fa…` at both). Tool bytes read with
`git show REV:tools/mado-tripwire.py` at `28c6837` (sha256
`9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`), `1f7f995`
(`367be947…`) and `9c54c56` (`c1ae45a7…`). All scans run from the /tmp clone
`/tmp/mado-r20w2-AtkCasesS` (origin removed). The fixture cells were executed only under a
recorder harness with `subprocess` and `lanehelpers` replaced by fakes, so no pacman or
host command could run; the recorder established what each fixture would call. The tripwire
itself only parses text.

## Method and instrument check

- Per-case comparison uses the counter's rule (`.ufo/waves/round-20/tw-precision.py:87`
  and `:195`): exit code equal AND multiset of (class, rule, line, evidence) equal; a row
  without `evidence` counts as `observed`.
- Counter at the three revisions, run from the clone so the suite pin and the tool bytes are
  both the committed ones:

```
28c6837 9613f510… passed 172 / 175 score 9.8286 {"H":{51,52},"L":{17,18},"P":{66,66},"S":{17,17},"W":{21,22}}
1f7f995 367be947… passed  29 / 175 score 1.6571 {"H":{15,52},"L":{1,18},"P":{7,66},"S":{2,17},"W":{4,22}}
9c54c56 c1ae45a7… passed 110 / 175 score 6.2857 {"H":{35,52},"L":{1,18},"P":{66,66},"S":{7,17},"W":{1,22}}
```

The three declared numbers reproduce exactly, and all 34 `before` claims for the S family
(17 cases x 2 revisions) match an independent re-scan. Receipts:
`.ufo/waves/round-20/w2/AtkCasesS/counter-summary.txt`, `scan-table.txt`, `semcheck.txt`.

## Per-case verdict

`py` is what CPython 3.14.8 would do with the fixture cells (recorder harness, not
execution of pacman); `tip`/`1f7f995`/`9c54c56` show pass/fail by the counter's rule with
the rows the tool emitted.

| # | case | want | py semantics | tip 28c6837 | 1f7f995 | 9c54c56 | verdict |
|---|---|---|---|---|---|---|---|
| 1 | print-lambda-spawn | 1 observed L1 | lambda body spawns argv | pass | fail clean | fail clean | holds |
| 2 | print-imported | 1 lead L1 | imported from non-stdlib; body invisible | pass | fail clean | fail clean | holds (declared lead) |
| 3 | list-bound-to-spawn | 1 observed L1 | `list = subprocess.run`; spawn | pass | fail clean | fail clean | holds |
| 4 | frozenset-def-spawn | 1 observed L1 | def rebinds builtin; spawn | pass | pass | fail clean | holds; control load-bearing |
| 5 | run-redef-pure | 0 | latest def is pure | pass | fail observed L1 | pass | holds; one-sided (V1) |
| 6 | run-call-before-spawn-redef | 0 | pure def in effect at call | pass | fail observed L1 | pass | holds; one-sided (V1) |
| 7 | run-import-rebound-print | 0 | `run = print` → builtin | pass | fail observed L1 | fail observed L1 | holds |
| 8 | run-redef-cross-cell | 0 | cell 2 pure def in effect | pass | fail observed L3 | pass | holds; one-sided (V1) |
| 9 | print-def-cross-cell | 1 observed L2 | cell 1 spawner def | pass | fail clean | fail clean | holds |
| 10 | del-run | 1 lead L1 | **NameError; no callee, no call** | pass | fail observed L1 | fail clean | **falsified vs Python** (W1) |
| 11 | del-run-cross-cell | 1 lead L3 | **NameError at cell 3** | pass | fail observed L3 | fail clean | **falsified vs Python** (W1) |
| 12 | del-print-restores-builtin | 0 | del restores builtin print | pass | fail observed L1 | pass | holds; contradicts E3's literal text (D2) |
| 13 | param-shadows-helper | 1 lead L1 | param bound to opaque `show` | pass | fail observed L1 | fail clean | holds; under-determined (V2) |
| 14 | param-shadows-spawn-alias | 1 lead L1 | param bound to opaque `show` | pass | fail observed L1 | fail observed L1 | holds; under-determined (V2) |
| 15 | shlex-join-as-run | 0 | `shlex.join` returns a string | pass | fail observed L1 | pass | holds |
| 16 | run-as-frozenset-control | 1 observed L1 | alias to subprocess.run; spawn | pass | pass | pass | holds; control load-bearing |
| 17 | S-AdoptW2-AdvHelperFn-b09 | 0 | `record = None` → TypeError | pass | fail observed L1 | pass | holds |

No individual scored S case is degenerate: 16 of 17 were red at one of the two baselines
(only control 16 is green at both, by design); the two controls (4, 16) are red under a
plausible wrong repair (see "controls" below). The wrongness is in two expectations and in
the family's coverage directions.

## W1 — wrong expectations: `S-CaseShadowing-del-run`, `S-CaseShadowing-del-run-cross-cell`

Fixture (case 10): `def run(argv): return subprocess.run(argv, check=True)`, then
`del run`, then `run(['pacman','-Q','hyprland'])`. Case 11 is the same across cells 1→3.

- CPython: the callee expression is evaluated before the argument list, so the call raises
  `NameError: name 'run' is not defined` and never reaches a callee or builds/executes an
  argv. Probe (safe; no subprocess import):
  `python3 -I -c 'def run(argv): return argv; del run; run(["pacman","-Q","hyprland"])'`
  → `NameError: name 'run' is not defined`. The recorder harness reproduces this for both
  fixtures: `outcome=NameError ... spawn_calls=[]` (`semcheck.txt`).
- The expectation is a **row with `evidence: lead`, exit 1** for that NameError. It is
  contract-conformant only because the wave-1 spec's E3 says "`del name` or a `reset` cell
  unbinds it (then a literal-argv call to it is a lead)" (`.ufo/waves/round-20/w1/spec.json`
  field `context`, "Target semantics" E1–E4), and E1 lists "an unbound bare name" as a lead.
  The SCORECARD's own C1 sentence states the general shape and names no unbound-name case:
  "`lead` (a literal argv handed to a callee whose body is not visible)" (`SCORECARD.md:1248`),
  so the case rests on the wave spec's broader parenthetical rather than on the declared
  claim's own wording.
- The case author had the contradicting evidence and fixed only the builtin half: the
  CaseShadowing report's F1 probe prints "`after_del_run: NameError: name 'run' is not
  defined` for a non-builtin" and uses it to correct case 12 (`.ufo/waves/round-20/w1/reports/CaseShadowing.md:175-179`);
  the same report's source-row draft says "a later call raises NameError, so a literal-argv
  call to it is a lead" — the "so" does not follow: a NameError cannot spawn. Cases 10/11
  therefore pin the un-fixed half of the clause the spec says is "fixed by evidence, not by
  this paragraph".
- Tool and contract disagrees one level down too: the tip tool already distinguishes the
  two halves of `del` — `update_bindings` pops a `PURE_ARG_CALLS` name (builtin restored;
  `tool-28c6837.py:1588-1594`) and marks any other name `deleted`; `spawn_scan` then routes
  the tuple `("unresolved", "external", "deleted", "unknown", "parameter")` to
  `helper_argv_leads` (`:1874-1877`, `:1799-1808`), so a deleted non-builtin emits exit 1,
  `observed_findings: 0, lead_findings: 1` — a blocking row for a command Python cannot run.
  The precise complement is one branch: `deleted` with no builtin fallback is a NameError,
  not a lead.
- Impact: a tool that treats a name deleted in the scanned text, with no builtin fallback,
  as a guaranteed NameError (no row) fails exactly these 2 cases: S would read 15/17 and
  the total 173/175 = 9.8857 instead of the declared N/N. The cases therefore reward the
  over-approximation and block a precision gain, which is the opposite of criterion 30′'s
  purpose.
- Suggested disposition (L1 decides): either (a) change both wants to `exit 0`/no rows and
  make the `deleted`+no-builtin case clean (a small extension of the `del print` handling
  the tool already has; expectations and tool then stay consistent, 172/175 still possible
  with the 3 known misses), or (b) keep the lead but write it up as a declared
  over-approximation (not precision evidence) in E3 and the knowledge note. Option (a) is
  the consistent completion of the author's own F1 correction.

## D1 — the suite's `before` mechanism claim is false (values are right)

`expected.json:3` says "`before` is the author's reading, re-measured by the counter."
`grep -n before .ufo/waves/round-20/tw-precision.py` → no match, rc 1: the counter never
reads `before`; `assemble-suite.py:30,60` copies it verbatim from each author's
`cases.json`. All 34 S `before` values independently re-derived here are correct, so no
number in the S family is wrong, but the "re-measured" claim is not true of the instrument
and should be dropped (or the counter should actually re-measure it) before the sentence is
cited under criterion 10.

## D2 — E3's `del` clause is inconsistent across the three documents of record

- E3 (wave spec): any `del name` → a literal-argv call is a lead.
- Case 12 wants clean after `del print` and is right (CPython restores the builtin; E2
  applies). The case's `why` says it is "evidence-fixed against E3's literal 'then a lead'".
- The knowledge note states only the builtin half: "`del` of a name that shadowed a builtin
  falls back to the builtin (no row)" (`corpus/knowledge/tripwire-precision-r20.md:31`); its
  lead table lists "an unbound name" (`:19`), which is the broad half cases 10/11 use.
- No committed correction amends E3: the SCORECARD "Round-20 pre-measurement corrections"
  amend E4 only, and the lesson's Decisions record E4 as amended by measurement.
Consequence: the suite, the wave spec and the SCORECARD disagree about a deleted non-builtin;
the suite follows the broadest text and pins the over-approximation. Append a correction to
E3 with the four cases (`del` builtin → builtin; `del` non-builtin with no re-binding →
NameError/no row; never-bound name → lead; re-bound after `del` → judged by the new binding).

## V1 — one-sided: the S clean trio cannot detect a "prefer any pure def" resolver

Cases 5, 6 and 8 all want clean; no S case has a **spawner** binding in effect at a call
after a pure def of the same name. Mutant R (`AtkCasesS/mutant-R.py`, sha256
`3cd527c0…`) implements "a name with a pure def anywhere is pure" (`PURE_DEF_NAMES` consulted
before the binding) and:

- passes **all 17** S cases (same rows as tip);
- emits `clean` for the positive shapes that Python says are observed and that the tip tool
  reports: `probes/positive-redef-cross.jsonl` (pure cell 1, spawner cell 2, call cell 3 →
  tip `observed L3`, mutant `clean`), `probes/spawn-call-pure.jsonl` (spawner, call, then
  pure → tip `observed L1`, mutant `clean`), `probes/del-then-redef.jsonl` (pure, `del`,
  spawner, call → tip `observed L1`, mutant `clean`).
- scores 166/175 on the whole suite (tip 172/175): six new failures on top of the tip's
  own three — `L-CasePureCrossCell-reset-clears-helper`, `W-WrapperCrossCell-two-hop`,
  `W-CaseWrapperForms-async-def-exec-param`, `-starred`, `L-AdoptW2-…-b12`,
  `W-AdoptW2-…-a25` — so the *overall* C1 score is not blind. But the S family's own 17/17
  is not evidence for the positive half of E3's "latest preceding binding" rule, and the
  mutant is a real false negative on all three probes.
Add at least `positive-redef-cross` (and ideally `spawn-call-pure`) to S; the tip tool
already passes them.

## V2 — one-sided: the parameter cases pin only the opaque-argument direction

Cases 13/14 want `lead` and pass `show` (non-stdlib import) as the only argument. The tip
tool is parameter-**blind**: it emits the same `lead` for `preview(subprocess.run)` (the
callee is an alias bound in the text; a call-site-aware reading gives `observed`) and for
`preview(' '.join)` (pure; a call-site-aware reading gives clean). Probes (scan-only):
`probes/trace-param-spawn.jsonl` → tip `lead`; `probes/trace-param-pure.jsonl` → tip `lead`;
`probes/param-pure-arg.jsonl` → tip `lead`. So a parameter-blind tool and a call-site-aware
tool both pass 13/14; the S family does not pin the parameter rule in either direction.
E1/E3 do not state parameter scoping (the author's F2 says the same), so this is a contract
gap to close rather than a wrong row: either declare parameters opaque in E3 (and record
the resulting limits), or add the traceable case and judge it.

## Holds, and the controls are load-bearing

- All 10 row-wanting cases and all 7 clean-wanting cases reproduce Python's binding
  behaviour as recorded in the table; the `why` lines match the fixture text and the
  E-clauses, except cases 10/11's "whose body is not visible" (there is no callee — W1)
  and b09's citation of E3 for a no-row conclusion E3 alone does not state (E2's "provably
  pure" covers it only by principle, since its enumerated forms do not name constant
  bindings) — a wording nit; the expectation itself is right.
- Control 16 (`run-as-frozenset-control`) and control 4 (`frozenset-def-spawn`) are not
  vacuous: mutant `mutant-namefirst.py` (sha256 `a4245e1b…`, builtin name checked before
  the binding) turns both **clean** (they fail) while the P `frozenset-closure` case stays
  clean (it passes). That is the over-suppression the controls are for.
- Untested-but-correct tool directions that the S family does not cover: `del frozenset`
  with a prior def → tip clean (correct); cross-cell `del print` → tip clean (correct);
  `del` then re-def spawner → tip observed (correct). These are coverage gaps, not wrong
  expectations; the first two would make useful cheap additions beside case 12.

## Held-out S cases (reported, not scored)

`precision-heldout/expected.json` carries 3 S cases (`a01`, `a02`, `a15`), all EDGE
bash-function shadowing (`pacman() { echo shadowed; }` / `sudo() { echo no; }`), wants
`exit 0`. The tip tool reports `host_mutation`/`package_query` at line 1 for each, so the
held-out reading is 0/12 as declared; these are outside E1–E4 and are not part of the
17-case judgment above.

## Limits

- Fixtures are synthetic transcripts; the tool parses text and never executes. My semantics
  harness substitutes `subprocess` and `lanehelpers` with recorders and does not run pacman,
  git, jj or any host probe (host pause binding). The `print-imported` and
  `param-shadows-*` fixtures would raise `ModuleNotFoundError` on `lanehelpers` if executed;
  their `lead` is the contract's honest "body not visible" label, not an execution claim.
- I did not judge the other 158 scored cases' expectations or run the held-out counter; the
  full-suite numbers cited come from the committed counter and from my own scan loop over
  all scored files (used only for the mutant comparison).
- Mutants R and name-first are scratch demonstrations under /tmp and in the seat dir; they
  are not proposed patches. Mutant R's 166/175 shows the full suite, not the S family,
  catches it.
- The parameter/lead versus observed question in V2 is contract-ambiguous; the "would be
  observed/clean" labels there are [INFERENCE] from E1's alias clause, not a committed rule.

## Installs

none.
