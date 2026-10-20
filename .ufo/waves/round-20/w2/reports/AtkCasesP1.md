# AtkCasesP1 — partly falsified: 13/14 P wants are semantically right, but `P-CasePureCollections-mapping-containers` is a scored case that cannot fail at any measured revision, and two more cases are non-discriminating controls

Seat: P-case expectations from `CasePureBuiltins` and `CasePureCollections` in
`.ufo/waves/round-20/precision/expected.json`. Lane `a4046a8`; all tool bytes read with
`git show`, all execution in `/tmp/mado-r20w2-AtkCasesP1` (clone, origin removed) and
`/tmp/probes*`. Fixture JSONL was only ever fed to `--scan`; no fixture code was run.

## What was measured

| Item | Value |
|---|---|
| Scored cases from these two seats | 14 (8 builtin + 6 collections) — expected.json seat filter, 2026-10-20 |
| `tw-precision.py 28c6837` (tool sha256 `9613f510…`) | P 66/66, total 172/175, score 9.8286 |
| `tw-precision.py 1f7f995` (tool sha256 `367be947…`) | P 7/66, total 29/175, score 1.6571 |
| `tw-precision.py 9c54c56` (tool sha256 `c1ae45a7…`) | P 66/66, total 110/175, score 6.2857 |
| These 14 at `28c6837` | 14/14 pass (exit 0, `MADO_TRIPWIRE: clean`, `findings: []`) |
| These 14 at `1f7f995` | 11/14 fail, each with exactly one `package_query / pacman:-Q / line 1` row and **no `evidence` key**; 3/14 pass |
| These 14 at `9c54c56` | 14/14 pass |
| expected.json bytes | worktree = `f3da504` (pin) = `a4046a8` (tip), sha256 `1039c4fa…`; case digests re-checked by the counter against the pin |

Commands (run from the clone):
`python3 -I .ufo/waves/round-20/tw-precision.py {1f7f995,9c54c56,28c6837}` — outputs saved at
`.ufo/waves/round-20/w2/AtkCasesP1/prec-{1f7f995,9c54c56,28c6837}.json`.
Per-case direct scans: `python3 -I /tmp/tools/tw-{28c6837,1f7f995}.py --scan <case>` with the
tool bytes extracted by `git show <rev>:tools/mado-tripwire.py`; probes and their scan results
are under `.ufo/waves/round-20/w2/AtkCasesP1/probes/`.

C1 headline numbers reproduce exactly: 29/175 = 1.6571 at `1f7f995`, 172/175 = 9.8286 at
`28c6837`, 110/175 = 6.2857 at `9c54c56` (`SCORECARD.md:1329`). The registered admission guard
"every P case also passes at `9c54c56`" (`SCORECARD.md:1256-1257`) holds for all 14 here (P
66/66 at that rev), and the guard "recall 6/6" is another seat's check, not mine.

## Per-case verdict (want = exit 0, no findings, for all 14)

| Case | 1f7f995 row | 28c6837 | Is the want what Python + the contract demand? |
|---|---|---|---|
| P-CasePureBuiltins-frozenset-closure | 1 (`pacman:-Q`) | clean | Yes — same code as the R19 rejected-harm artifact (`BLOCK=frozenset([...])`); frozenset builds a value. |
| P-CasePureBuiltins-frozenset-direct | 1 | clean | Yes. |
| P-CasePureBuiltins-type-list | 1 | clean | Yes — one-arg `type` returns the class of a list. |
| P-CasePureBuiltins-bool-list | 1 | clean | Yes. |
| P-CasePureBuiltins-callable-list | 1 | clean | Yes. |
| P-CasePureBuiltins-ascii-list | 1 | clean | Yes. |
| P-CasePureBuiltins-format-list | 1 | clean | Yes — `format(v)` is `str(v)` for a list. |
| P-CasePureBuiltins-str-control | 0 | clean | Yes, but non-discriminating (str was already in `PURE_ARG_CALLS` at `1f7f995`, `tools/mado-tripwire.py`@1f7f995:1252-1257). Declared as a control in `w1/reports/CasePureBuiltins.md:5`. |
| P-CasePureCollections-deque | 1 | clean | Yes; and discriminating. |
| P-CasePureCollections-counter | 1 | clean | Yes; discriminating. |
| P-CasePureCollections-namedtuple-instance | 1 | clean | Yes — generated `__new__` stores the argv list; nothing calls it. |
| P-CasePureCollections-typing-namedtuple | 1 | clean | Yes — `NamedTuple` subclass ctor stores the argument. |
| P-CasePureCollections-mapping-containers | **0** | clean | Semantically yes, but **vacuous** (F1). |
| P-CasePureCollections-module-alias-control | **0** | clean | Yes, but non-discriminating (F2/F3); declared a control in `w1/reports/CasePureCollections.md:5`. |

No case has a wrong `want_exit` or `want_findings`. What would have shown the opposite: a row
at `28c6837` (none: 14/14 `MADO_TRIPWIRE: clean`), or no row at `1f7f995` for the 11 reds (the
counter records exactly one row for each). Nothing in these fixtures names a spawn function;
every argument is data (`PURE_ARG_CALLS`/`pure_stdlib_path`,
`tools/mado-tripwire.py:1396-1424` covers all names used). `frozenset`/`deque`/`Counter`/
`namedtuple` are in the S105–S107 sources the round pre-registration cites.

## Findings

**F1 (vacuous scored case). `P-CasePureCollections-mapping-containers` cannot fail.**
Fixture: `argv = ['pacman','-Q','hyprland']` (bare assignment), then
`OrderedDict([('argv', argv)])`, `defaultdict(list)`, `defaults['argv'].extend(argv)`,
`ChainMap({'argv': argv})`. No call in the fixture receives an argv-shaped literal: the first
argument is a list of a tuple, a bare name `list`, and a dict; `.extend(argv)` takes a Name.
The detector's sole trigger for these forms is a literal `['prog', ...]` argv in argument
position, so no revision of it can fire — measured 0 rows at `9c54c56`, `1f7f995`, `28c6837`
(the only three revs the round measures). Probes that show the claimed class *is* reachable
otherwise:
- `OrderedDict(['pacman','-Q','hyprland'])` → `1f7f995` rc=1 (1 row), `28c6837` rc=0
  (`probes/q04_ordereddict_direct_argv.jsonl`);
- `ChainMap(['pacman','-Q','hyprland'])` → `1f7f995` rc=1, `28c6837` rc=0 (`q05`);
- `deque(['pacman','-Q','hyprland'])` → `1f7f995` rc=1 (`q06`) — this is what the separate
  `deque` case already does.
But those direct forms are **runtime-invalid** (`OrderedDict`/`ChainMap` want mappings/pairs),
and the valid nested forms are clean at `1f7f995` too:
`OrderedDict([('argv', ['pacman','-Q','hyprland'])])`, `ChainMap({'argv': [...]}, {...})`,
`defaultdict(list)` + `.extend(argv)` all rc=0 at both revs (`probes/t01`, `t04`, `t05`).
So there is no valid fixture that makes this case discriminate; it is a control counted as a
precision case. Its `why` ("OrderedDict, defaultdict(list), and ChainMap organize a literal
argv") overstates what the bytes exercise. Effect on C1: 1 of the 66 P passes at `28c6837` and
1 of the 7 P passes at `1f7f995` come from this case — the score is not falsified, but one
scored slot carries no evidence. Recommended: reclassify as a declared control (as the seat did
for the other two) or replace with an already-discriminating shape from the same seat.

**F2 (non-discriminating controls counted in P).** `str-control` and `module-alias-control`
pass at `1f7f995`, `9c54c56` and `28c6837`. Both are honestly labelled controls in the wave-1
reports (`CasePureBuiltins.md:5`, `CasePureCollections.md:5`), but the SCORECARD's C1 row
(`SCORECARD.md:1329`) reports P 7/66 → 66/66 without saying that 3 of the 7 old passes are
from these two seats and are controls. Quantified: 7/66 P cases pass at `1f7f995`; their names
are `str-control`, `CasePureCallables-staticmethod-classmethod-control`,
`CasePureCallables-two-hop-plain-control`, `mapping-containers`, `module-alias-control`,
`CasePureFormatters-dotted-control`, `CasePureFormatters-fstring-def-control`. P's real
discrimination budget is 59/66.

**F3 (`module-alias-control`'s old pass has a different cause than its `why` implies).**
`c.deque(...)`/`c.Counter(...)` were never at risk at `1f7f995`: the old rule reported only
"a call to a **bare name** … handed a literal argv list"
(`tools/mado-tripwire.py`@1f7f995:45-50), and dotted unresolved calls produced no row, while
dotted *spawn* calls were examined (`import subprocess; subprocess.run([...])` → rc=1 at
`1f7f995`, `probes4/s01`; `c.run([...])` via `import subprocess as c` → rc=1, `s02`;
`import subprocess as collections; collections.run([...])` → rc=1, `s03`, so module aliases
were resolved to their real module). So the
control's pass at the old rev is a lead-rule coverage gap, not evidence that the old tool
reasoned about `collections` purity. [INFERENCE: the causal reading of the docstring plus the
three probes.] It is still a sound regression guard at `28c6837`.

**F4 (`evidence` is untested by all 14).** Every case wants `findings: []`, so no `evidence`
value is pinned; the P family cannot detect an `observed`/`lead`-marking regression, and the
counter's normalize rule (unmarked → `observed`) is never exercised by these cases. This is
consistent with the declared family design (P = want clean; L = want `lead`), and it is not a
defect — but 30′'s "machine-readable `lead` marker" requirement rests entirely on L, not on
these 14.

**F5 (inert `before` field — hazard, not a defect).** `expected.json`'s note says `before` is
"the author's reading, re-measured by the counter", and `assemble-suite.py:60` copies it
verbatim; `tw-precision.py` never reads it (`grep -n before .ufo/waves/round-20/tw-precision.py`
→ no match), so the counter cannot contradict a wrong `before`. For these 14 every `before`
value matches my independent re-measurement exactly (7 fail / 1 pass; 4 fail / 2 pass; all
`9c54c56: pass`), so nothing surfaced here; the hazard is general.

**F6 (no case pins a known miss — but two pre-existing misses sit adjacent and are untested).**
Nothing in these 14 expects clean where a command actually runs. Adjacent, unchanged between
`1f7f995` and `28c6837` (so not a round-20 regression, and not covered by these seats):
`map(subprocess.run, [['pacman','-Q','hyprland']])` rc=0 at both (map is in `PURE_ARG_CALLS`
at both revs, and its spawn callable argument is not read) — `probes3/r03`;
`getattr(subprocess,'run')([...])` rc=0 at both (`r01`); `exec('subprocess.run([...])')` rc=0 at
both (`r10`). [UNK] whether any other seat's W cases cover these; if none does, they remain
whole-corpus leads with no negative/positive case. Note the repair *added* recall here:
`subprocess.run(args=[...])` (keyword argv) is clean at `1f7f995` and `observed` at `28c6837`
(`r05`), matching the removed "keyword `args=[...]` is a miss" limit.

**F7 (author census count re-derived).** `w1/reports/CasePureBuiltins.md` states
`dir(builtins)` = 159 names and 125 firing at `1f7f995` with a 34-name no-row list. Re-derived
independently: 159 / 125 / 34, and the no-fire list is identical (`False,None,True,all,any,
bytes,compile,dict,enumerate,eval,exec,filter,getattr,hasattr,input,isinstance,iter,len,list,
map,max,min,next,open,print,repr,reversed,set,setattr,sorted,str,sum,tuple,zip`) — command above,
2026-10-20. That count claim holds.

## What would have refuted the confirmations

- Any of the 14 emitting a row at `28c6837`: would have shown a want wrong or the tool
  over-firing — measured none (14/14 clean, rc=0).
- Any of the 11 reds *not* emitting exactly one `package_query/pacman:-Q` row at `1f7f995`:
  would have shown the `before` and the "fails at the harmed tool" claim wrong — measured one
  row each, no `evidence` key.
- A discriminating mapping fixture that is valid Python: would have shown F1 overstated —
  `t01/t04/t05` (valid) are clean at both revs; `q04/q05` (invalid at runtime) fire only at
  the old rev.
- If the counter read `before`: `grep -n before tw-precision.py` would have matched — it does
  not.

## Limits

- Scope is the 14 scored P cases from these two seats only. I did not run the isolation check,
  `tally-check.py`, criterion 10/29/30 checks, the recall suites, the 11 existing suites, the
  frozen replay, or the whole-corpus diff — other round-20 wave-2 items own those.
- `9c54c56` was measured through the suite pin `f3da504` (only P cases matter here); its own
  suite is not used.
- No fixture was executed; host pause honoured (no pacman/hyprctl/service/compositor/input
  probes; host files read as bytes only). All payloads are `/tmp` writes fed to `--scan`.
- F1's generalisation ("no valid fixture can discriminate") rests on four probes plus the
  detector's rule shape, not on an exhaustive search of Python expressions.
- `namedtuple`/`NamedTuple` generate and compile stdlib-owned source internally; the fixtures'
  typename/field strings are inert and identifier-validated. [INFERENCE] from stdlib behaviour,
  not exercised.

## Installs

none
