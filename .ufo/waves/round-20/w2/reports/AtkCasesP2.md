# AtkCasesP2 — partly falsified: all 34 numeric wants are right, but 2 dataclass P cases and 1 decorator P case cannot discriminate the repaired rule (their clean is a blanket skip, and spawn twins of the identical shape are missed), and 2 CrossCell fixtures do not do what their `why` says

Seat: P/L-case expectations from `CasePureFormatters` (13), `CasePureCallables` (14) and
`CasePureCrossCell` (7) in `.ufo/waves/round-20/precision/expected.json` (33 P + 1 L = 34
cases; the other 141 of 175 suite slots are out of scope). Lane tip `a4046a8`; tool bytes read
with `git show`; every scan in `/tmp/mado-r20w2-AtkCasesP2` (clone, origin removed) or
`/tmp/AtkCasesP2`. Fixture JSONL was only ever fed to `--scan`; no fixture code was executed.

## Measurement (commands and results)

From the clone:

```
python3 -I .ufo/waves/round-20/tw-precision.py {28c6837,1f7f995,9c54c56}
```

| rev | tool sha256 | score | total | P | families |
|---|---|---|---|---|---|
| `28c6837` | `9613f510…` | 9.8286 | 172/175 | 66/66 | H 51/52, L 17/18, S 17/17, W 21/22 |
| `1f7f995` | `367be947…` | 1.6571 | 29/175 | 7/66 | H 15/52, L 1/18, S 2/17, W 4/22 |
| `9c54c56` | `c1ae45a7…` | 6.2857 | 110/175 | 66/66 | H 35/52, L 1/18, S 7/17, W 1/22 |

These reproduce `SCORECARD.md:1329` and the pre-harm line `SCORECARD.md:1330` exactly. For the
34 cases in scope: **34/34 pass at `28c6837`; 30 fail + 4 pass at `1f7f995`; 33 pass + 1 fail
(the L case) at `9c54c56`.** Every `expected.json` `before` value matches the independent
re-measurement (0 mismatches across 34 × 2 revisions). Direct scans at `28c6837` report
`eval_unparsed: 0` and `unparsed_spawns: 0` for all 34, so no clean verdict is a parse failure.

Each of the 30 non-control P cases fails at `1f7f995` with exactly the false-positive rows its
`why` names (`host_mutation/sudo` + `host_mutation/pacman:-S|systemctl:restart`,
`package_query/pacman:-Q`, or `vcs_write/git:commit`), all unmarked (no `evidence` key). So
each is a real negative of the round-19 harm; none is a case where the old tool already passed.

## What holds

- **No `want_exit`, `want_findings` or `evidence` value in these 34 is wrong** against Python
  semantics or E1–E4 (`gen_w1.py:36-39`). Every fixture's argv is data:
  `shlex.join/quote`, `json.dumps`, `pprint.pformat`, `textwrap.indent`, `' '.join`,
  f-string/`str.format`, `functools.partial(dumps)`, dataclass/plain-class/NamedTuple/
  namedtuple/lambda/def/async def bodies, and visible same- or earlier-cell helpers. No
  fixture has a reachable `subprocess`/`os.system`/`asyncio` call; the only two `subprocess.run`
  tokens sit in defs that are rebound or defined after the call (`duplicate-def-*-spawner`), and
  the only file write (`write-case`) is not a command. The test that would have shown the
  opposite is a row at `28c6837`: none (34/34 clean, exit 0).
- **The L case is exactly E3.** `reset` unbinds `format_command`, so a literal-argv call is a
  `lead`: the tool emits `package_query/pacman:-Q/L3/lead` and the want matches. The case
  discriminates the marker: at `1f7f995` the same fixture emitted the same class/rule/line
  with **no** `evidence` key (counts as `observed` → fail); at `9c54c56` it was clean (fail).
- The admission guard "every P case passes at `9c54c56`" holds for these 33 P cases (P 66/66).
- Author per-seat claims are accurate: formatters 11 red + 2 controls (report says 2/13 at
  `1f7f995`), callables 12 red + 2 controls, cross-cell 6 red + 1 L (`fail/fail`).

## Findings

### F1 (pins a blind spot) `P-CasePureCallables-dataclass-ctor` — want right, but the tool never reads the class body

`why`: "its generated __init__ cannot spawn." The repaired tool cannot know that: at
`28c6837:1848-1871` a class callee is handled by finding a member named `__init__` in the class
body; a `@dataclass` with no explicit `__init__` has none, so the handler `continue`s without
scanning anything. A dataclass's generated `__init__` does call `__post_init__`
(print-only probe: `post_init sees ['pacman','-Q','hyprland']`), and the argv field is set
before it runs.

Twin (same shape, body executes; envelope = one assistant `eval` toolCall, `{language:"py",code}`):

```python
import subprocess
from dataclasses import dataclass

@dataclass
class Case:
    name: str
    argv: list
    def __post_init__(self):
        subprocess.run(['pacman', '-Q', 'hyprland'])

c = Case('x', ['git', 'commit', '-m', 'wip'])
```

```
python3 -I /tmp/AtkCasesP2/tool-28c6837.py --scan probes/p19-dataclass-postinit-literal.jsonl
MADO_TRIPWIRE: clean
{... "counts": {"package_query": 0, ...}, "exit": 0, "findings": [], "lead_findings": 0,
 "observed_findings": 0, ...}
```

That is a real `pacman -Q hyprland` executing and going unreported. The skip is specific to
"no `__init__` in the body", not to dataclasses: p14 (same dataclass with an explicit
`def __init__(self, name, argv)` that calls `subprocess.run(argv)`) is detected
(`package_query/pacman:-Q/L1/observed`, rc=1). So `dataclass-ctor`'s green is produced by the
blanket skip: a repair that exempts every constructor without proof would pass this case and
still miss F1's twin. The same shape in `P-CasePureCrossCell-dataclass-case` (F2) gives the same
result (`dataclass-case` twin rc=0).

Effect on C1/30′: the case is a valid negative of the historical harm, but it is not evidence
for the E2 body clause. Recommend a W-family positive for a `__post_init__` spawn (or record
the case as a form control, not a body-purity test).

### F2 (same, cross-cell) `P-CasePureCrossCell-dataclass-case` — want right, body never read

Identical mechanism across cells: the binding is a `ClassDef`, the class handler finds no
`__init__`, no scan. Twin (cell 1 defines the dataclass with `__post_init__` spawning; cell 2
constructs it with `('pacman','-Q','hyprland')`) → `rc=0`, `findings: []`. The case's `why`
("stores command-looking argv as tuple data") is true of the fixture, but a tool that never
looks at `__post_init__` passes it for the wrong reason.

### F3 (pins a blind spot) `P-CasePureCallables-same-text-decorator` — want right, wrapper body never modelled

`why`: "wrapper and body only print and join the git argv." The tool binds a decorated def to
the **raw FunctionDef node** (`update_bindings`: `bindings[stmt.name] = {"kind": "helper",
"node": stmt}`); the decorator is only visited as an eager call at decoration time, and the
wrapper it returns is never the analysed body. So the claim about the wrapper is never checked.

Twin (wrapper passes the call's own argv to a spawn):

```python
import subprocess

def traced(fn):
    def inner(*args):
        return subprocess.run(args[0])
    return inner

@traced
def show(argv):
    return ' '.join(argv)

print(show(['pacman', '-Q', 'hyprland']))
```

```
python3 -I /tmp/AtkCasesP2/tool-28c6837.py --scan probes/p10-decorator-inner-spawns-argv.jsonl
MADO_TRIPWIRE: clean   (rc=0, findings [], observed_findings 0)
```

Isolation: p17 (`@traced def show(argv): return subprocess.run(argv)`) **is** detected
(`package_query/pacman:-Q/L1/observed`, rc=1) — the decorated function's own body is scanned;
the wrapper is not. A literal spawn inside `inner` is also missed (`p4`, `p20`). So the case's
green is independent of whether the wrapper is pure.

### F4 (partial, lower severity) `P-CasePureCallables-plain-class-init` — `__repr__` runs but is never scanned

The class handler scans only `init.body` (`28c6837:1864-1868`). The fixture executes
`__repr__` via `print(step)`; a spawn there is unreported:

```python
class Step:
    def __init__(self, label, argv): ...
    def __repr__(self):
        subprocess.run(['pacman', '-Q', 'hyprland'])
        return '%s: %s' % (self.label, ' '.join(self.argv))
```

`p18-repr-spawn.jsonl` → rc=0, `findings: []` (runtime probe shows `__repr__` runs). The direct
parameter path *is* analysed: p7 (`__init__(self, argv): subprocess.run(argv)`) → rc=1. So the
case is discriminating for `__init__`, but its clean also covers an unanalysed `__repr__`. The
`self.argv` flow (`subprocess.run(self.argv)` in `__init__`, the exact field the fixture stores)
is likewise missed (twin `plain-class-init` rc=0).

### F5 (fixture defects) two CrossCell fixtures do not perform the operation their `why` states

(a) `P-CasePureCrossCell-write-case`. Cell 1 is
`def write_case(name, argv): (base / name).write_text(json.dumps(argv))`; neither cell imports
`json` or binds `base`. The call in cell 2 therefore raises `NameError` on `base` before any
serialisation. The `why` ("serializes literal command-looking argv as data") is not what the
transcript does. The want (clean) is still correct — nothing spawns either way — but the case
does not test "data serialisation"; it tests a helper whose body references unbound globals.

(b) `P-CasePureCrossCell-lambda-format-case`. Cell 1 is `render = lambda argv: json.dumps(argv)`
with no `json` import in either cell; at call time this is `NameError` under standard Python
[INFERENCE: the transcript never binds `json`; `base` in (a) is unbound outright]. The want
(clean) is still correct — `json.dumps` is a known-pure exact path and attribute calls are
unflagged — but the `why` ("passes literal argv only to json.dumps") is not established by the
bytes.

Both cases still discriminate against `1f7f995` (each emitted one `package_query/pacman:-Q`
row at line 2), so this is a fixture-honesty defect, not a wrong want.

### F6 (counting) declared controls and the P denominator

4 of these 34 pass at `1f7f995` **and** `9c54c56`: `fstring-def-control`, `dotted-control`,
`staticmethod-classmethod-control`, `two-hop-plain-control`. All four are honestly labelled
`Control:` in their `why` and in the wave-1 reports. Suite-wide, 7/66 P cases pass at
`1f7f995` (`str-control`, the 4 here, `mapping-containers`, `module-alias-control`), so P's
marginal discrimination is **59/66**, not 66/66. The C1 score is not falsified (it counts what
it says), but "P 7/66 → 66/66" should not be read as 66 repaired negatives. (The other three
are AtkCasesP1's F1/F2 scope.)

Within these 34, only the L case pins `evidence`; the 33 P cases cannot detect an
`observed`/`lead` regression by design (P = want clean). This is consistent with the family
design and with 30′ resting the `lead` marker on L.

### F7 (hazard, values correct here) `before` is inert

`tw-precision.py` never reads `expected.json`'s `before` (no match for `before` in the counter);
`assemble-suite.py` copies it verbatim. For these 34 the values are nonetheless correct
(independently re-measured: 30 fail / 4 pass at `1f7f995`; all P pass at `9c54c56`). Same
hazard as AtkCasesP1 F5; recorded here because it applies to my seats too.

## Per-case verdict

Want = exit 0 / no findings unless noted. `before` columns are the counter at that revision.

| Case | want_exit | 1f7f995 | 9c54c56 | 28c6837 | Verdict |
|---|---|---|---|---|---|
| `P-CasePureFormatters-shlex-join` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureFormatters-json-dumps` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureFormatters-pprint-pformat` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureFormatters-textwrap-indent-chain` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureFormatters-lambda-join` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureFormatters-fstring-def` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureFormatters-str-format-bound` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureFormatters-quote-cross-cell` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureFormatters-dumps-alias` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureFormatters-join-cross-cell-import` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureFormatters-partial-dumps` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureFormatters-fstring-def-control` | 0 | pass | pass | pass | want right; declared control (passes at both baselines) |
| `P-CasePureFormatters-dotted-control` | 0 | pass | pass | pass | want right; declared control (passes at both baselines) |
| `P-CasePureCallables-dataclass-ctor` | 0 | fail | pass | pass | want right; non-discriminating (class with no `__init__` skipped; F1) |
| `P-CasePureCallables-plain-class-init` | 0 | fail | pass | pass | want right; partial (only `__init__` scanned, `__repr__` runs unanalysed; F4) |
| `P-CasePureCallables-functools-cache-def` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureCallables-async-def-await` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureCallables-duplicate-def` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureCallables-duplicate-def-later-spawner` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureCallables-duplicate-def-earlier-spawner` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureCallables-nested-def` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureCallables-nested-def-param` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureCallables-lambda-same-cell` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureCallables-transitive-class` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureCallables-same-text-decorator` | 0 | fail | pass | pass | want right; non-discriminating (wrapper body not modelled; F3) |
| `P-CasePureCallables-staticmethod-classmethod-control` | 0 | pass | pass | pass | want right; declared control (attribute calls exempt by E2) |
| `P-CasePureCallables-two-hop-plain-control` | 0 | pass | pass | pass | want right; declared control (passes at both baselines) |
| `P-CasePureCrossCell-write-case` | 0 | fail | pass | pass | want right; fixture defect (`base`/`json` unbound; F5a) |
| `P-CasePureCrossCell-expect-case` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureCrossCell-dataclass-case` | 0 | fail | pass | pass | want right; non-discriminating (same skip, cross-cell; F2) |
| `P-CasePureCrossCell-namedtuple-class-case` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureCrossCell-namedtuple-factory-case` | 0 | fail | pass | pass | want right; discriminating |
| `P-CasePureCrossCell-lambda-format-case` | 0 | fail | pass | pass | want right; fixture defect (`json` unbound; F5b) |
| `L-CasePureCrossCell-reset-clears-helper` | 1 | fail | fail | pass | want right (one `package_query/pacman:-Q/L3/lead`); discriminating |

## Twin test method (why F1–F4 are not merely "the fixture is pure")

For each P case I built a structurally identical twin in which the same literal (or the same
call argv) reaches `subprocess.run`, then scanned it with the `28c6837` tool. A detected twin
means the case's clean requires the tool to have seen the literal and chosen not to fire; an
undetected twin means the case's clean is produced by not looking. 35 twins were scanned; 30
were detected (`observed`). Undetected: `dataclass-ctor`, `dataclass-case`,
`same-text-decorator-body`, `namedtuple-class` (a `.run()` attribute call — out of contract by
E2's attribute-call clause, not counted as a defect), and `plain-class-init` (`self.argv` flow).
Commands: `python3 -I /tmp/AtkCasesP2/tool-28c6837.py --scan /tmp/AtkCasesP2/twins/<name>.jsonl`.
The findings above (F1–F4) are exactly the undetected cases whose *own* fixture shape the suite
counts as clean; the positive controls (p1, p2, p3, p5, p7, p14, p17) show the same tool
detecting the same sink through a plain def, an explicit `__init__` parameter, a decorated
function's body and a lambda — so the misses are specific to the class-without-`__init__`,
decorator-wrapper and `self.attr`/`__repr__` paths. (p13, an uncalled literal-spawning def, is
correctly clean; it is not a positive control.)

## Limits

- Scope is the 34 cases of these three seats. I did not run the recall counter/split, the 11
  existing suites, the frozen replay, the whole-corpus diff, `isolation-check.sh`,
  `tally-check.py`, criterion 10/29/30 checks, or the gate — other wave-2 items own those.
- F1–F4 are evidentiary findings, not wrong wants. Under the narrow reading "a P case only has
  to forbid a false positive", each is acceptable as written; they are not evidence that
  the repaired rule resolves the construct. L1 should choose which reading the closure adopts.
- Runtime semantics of `__post_init__`, decorator wrappers and `__repr__` were confirmed with a
  print-only probe (no subprocess, no host effect); the lane fixtures themselves were never
  executed (only fed to `--scan`).
- `base` is certainly unbound in `write-case` (no binding in either cell); `json` in
  `lambda-format-case`/`write-case` is unbound by the transcript, and I did not verify whether
  the eval kernel happens to pre-import `json` [UNK]. Either way the wants stay clean.
- The namedtuple twins cannot be made to spawn at construction (generated `__new__`), so those
  two cases cannot discriminate execution either; they are valid false-positive guards. Not
  listed as defects.
- No LSP server was applicable (no code repository query in scope); sources were read as text
  plus `--scan` results.

## Installs

none
