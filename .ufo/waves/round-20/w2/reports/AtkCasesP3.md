# AtkCasesP3 — partly falsified: all 19 AdoptW2 P wants are numerically right, but 4 of them certify constructs whose five spawning twins are rows at `1f7f995` and clean at `28c6837`, 4 are exact-shape duplicates of other scored P cases, and 2 cannot fail on the body their `why` names

Seat: P-family expectations from `CaseAdoptW2` (19 of the 66 P cases) in
`.ufo/waves/round-20/precision/expected.json`. Lane `a4046a8`; every tool byte read with
`git show`, all scans in `/tmp/mado-r20w2-AtkCasesP3` (clone, `origin` removed) and
`/tmp/r20p3`. Fixture JSONL was only fed to `--scan`; no fixture code was executed. The two
executed snippets are pure-stdlib semantics probes (below).

## Measurement (commands and results)

From the clone, the committed counter copied in (removed afterwards; no lane write):

```
git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado-r20w2-AtkCasesP3
git -C /tmp/mado-r20w2-AtkCasesP3 remote remove origin
git show a4046a8:.ufo/waves/round-20/tw-precision.py > /tmp/r20p3/tw-precision-clone.py
cp /tmp/r20p3/tw-precision-clone.py /tmp/mado-r20w2-AtkCasesP3/.ufo/waves/round-20/tw-precision-copy.py
python3 -I .ufo/waves/round-20/tw-precision-copy.py {1f7f995,9c54c56,28c6837}
```

| rev | `tools/mado-tripwire.py` sha256 | score | total | P | families |
|---|---|---|---|---|---|
| `1f7f995` | `367be947…` | 1.6571 | 29/175 | 7/66 | H 15/52, L 1/18, S 2/17, W 4/22 |
| `9c54c56` | `c1ae45a7…` | 6.2857 | 110/175 | 66/66 | H 35/52, L 1/18, S 7/17, W 1/22 |
| `28c6837` | `9613f510…` | 9.8286 | 172/175 | 66/66 | H 51/52, L 17/18, S 17/17, W 21/22 |

These reproduce `SCORECARD.md:1329` exactly, including the 3 remaining failures
(`W-CaseWrapperForms-class-method-instance`, `L-AdoptW2-AdvHelperFn-b14`,
`H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help`). The suite bytes at the pin equal the tip:
`git log f3da504..a4046a8 -- .ufo/waves/round-20/precision` is empty, `expected.json`
sha256 `1039c4fa…` at both, and all 175 file digests match. The 19 in scope: **19/19 pass at
`28c6837`, 19/19 fail at `1f7f995`, 19/19 pass at `9c54c56`**; every `before` value matches.
All 66 P `before` values match my scans (0 mismatches).

`--scan` was run on every case with copied tool bytes (`git show REV:tools/mado-tripwire.py`),
cwd = a temp dir per case, `python3 -I`, exactly the counter's rule (exit code + multiset of
`(class, rule, line, evidence)`; a missing `evidence` key counts as `observed`). `1f7f995`
rows carry no `evidence` key, as the contract's normalize rule expects.

### Per-case verdict (want = exit 0, `findings: []`, for all 19)

| # | case (suffix) | `1f7f995` rows (all line 1) | `9c54c56` | `28c6837` | Is the want what Python + the contract demand? |
|---|---|---|---|---|---|
| 1 | CriticC3W2-dc-dataclass | `sudo` + `pacman:-S` | pass | pass | Yes — `@dataclass` ctor only stores; `print(len(cases))` runs. **But see F1.** |
| 2 | CriticC3W2-dc-namedtuple | `sudo` + `pacman:-Syu` | pass | pass | Yes — `collections.namedtuple` instance only holds the argv. |
| 3 | CriticC3W2-dc-shlex-join | `sudo` + `pacman:-S` | pass | pass | Yes — `shlex.join` renders text. Exact-shape twin of `P-CasePureFormatters-shlex-join` (F2). |
| 4 | CriticC3W2-dc-lambda | `sudo` + `systemctl:restart` | pass | pass | Yes — lambda body joins; exact-shape twin of two other P cases (F2). |
| 5 | CriticC3W2-dc-decorated-def | `sudo` + `pacman:-S` | pass | pass | Yes for `@functools.cache`; **but see F1** (decorator application is never evaluated). |
| 6 | CriticC3W2-dc-frozenset | `package_query pacman:-Q` | pass | pass | Yes — the closure's exact harm artifact plus `print(BLOCK)`; frozenset of literals is data. |
| 7 | CriticC3W2-dc-deque | `systemctl:restart` | pass | pass | Yes — `deque` stores; near-duplicate of b18b (F2). |
| 8 | CriticC3W2-dc-async-def | `sudo` + `pacman:-S` | pass | pass | Yes — top-level `await` runs a print-only body; `PyCF_ALLOW_TOP_LEVEL_AWAIT` (`tools/mado-tripwire.py@28c6837:1785-1787`) parses it. |
| 9 | CriticC3W2-dc-type-hint-shape | `sudo` + `pacman:-S` | pass | pass | Yes — duplicate `check`; the later binding prints. Name is wrong (no type hint), family questionable (F4/F5). |
| 10 | AdvHelperFn-b06 | `package_query pacman:-Q` | pass | pass | Yes — `format(list)` is `str(list)`; exact-shape twin of `format-list` (F2). |
| 11 | AdvHelperFn-b07 | `package_query pacman:-Q` | pass | pass | Yes — `__init__` only assigns. |
| 12 | AdvHelperFn-b08 | `package_query pacman:-Q` | pass | pass | Yes — lambda only prints. |
| 13 | AdvHelperFn-b15 | `package_query pacman:-Q` | pass | pass | Yes (nothing runs: `outer()` is never called), **but the case cannot fail on `log`'s body** (F3). |
| 14 | AdvHelperFn-b16b | `package_query pacman:-Q` | pass | pass | Yes — frozenset of literals; exact-shape twin of `frozenset-direct` (F2). `why` is factually wrong (F4). |
| 15 | AdvHelperFn-b17 | `package_query pacman:-Q` | pass | pass | Yes — `@dataclass` bare ctor stores. **But see F1.** |
| 16 | AdvHelperFn-b18b | `package_query pacman:-Q` | pass | pass | Yes — `deque` of literals; near-duplicate of dc-deque. |
| 17 | AdvHelperFn-b20 | `package_query pacman:-Q` | pass | pass | Yes — the coroutine is never awaited, so nothing runs; **cannot fail on the body** (F3). |
| 18 | AdvHelperFn-b21 | `package_query pacman:-Q` | pass | pass | Yes — `@functools.lru_cache` body joins. At runtime the call raises `TypeError` before the body (F3 note); **see F1** for the decorator. |
| 19 | AdvHelperFn-b22 | `package_query pacman:-Q` | pass | pass | Yes — later duplicate def prints. Duplicate-def shape is S's subject (F5). |

**No case has a wrong `want_exit`, `want_findings` or `evidence` value.** Every fixture's argv
is data: a static scan for `subprocess|os.system|Popen|check_(output|call)|os.exec|
create_subprocess|tool.bash|system(|popen(` finds **none** in all 19 payloads. What would have
shown the opposite: any row at `28c6837` (none) or at `9c54c56` (none), any `1f7f995` pass
(none), or a spawn token in a fixture (none).

## Findings

### F1 (pins a blind spot, 4 cases) — the dataclass and decorator constructs are exempted wholesale; all five spawning twins are rows at `1f7f995` and clean at `28c6837`

Four of the 19 exercise a construct whose executed body the repaired tool never reads. Twins
that keep the case's shape and put a real spawn in the executed path:

```
# dataclass-postinit-literal  (based on dc-dataclass / b17)
from dataclasses import dataclass
import subprocess
@dataclass
class Case:
    argv: list
    def __post_init__(self):
        subprocess.run(['sudo','pacman','-S','x'])
Case(['pacman','-Q','y'])
```

| twin (case it shadows) | `1f7f995` | `28c6837` |
|---|---|---|
| dataclass-postinit-literal (dc-dataclass, b17) | rc=1 `[package_query pacman:-Q, host_mutation sudo, host_mutation pacman:-S]` | **rc=0 `[]`** |
| dc-dataclass + `__post_init__: subprocess.run(self.argv)` | rc=1 `[sudo, pacman:-S]` | **rc=0 `[]`** |
| b17 + `__post_init__: subprocess.run(self.argv)` | rc=1 `[sudo, pacman:-S]` | **rc=0 `[]`** |
| dc-decorated-def with a `cache` decorator whose body spawns | rc=1 `[sudo, pacman:-S]` | **rc=0 `[]`** |
| b21 with an `lru_cache` decorator whose body spawns | rc=1 `[pacman:-Q]` | **rc=0 `[]`** |

Controls isolate the mechanism:

- `@dataclass` with an **explicit** `__init__` that spawns the parameter → rc=1 at `28c6837`
  (the class handler works; the generated `__init__`/`__post_init__` is the gap). Anchor:
  `tools/mado-tripwire.py@28c6837:1848-1852` (`init = next(... "__init__" ...)`; none →
  `continue`), so `__post_init__` is never read.
- `f = deco(f)` **explicit application** of the same spawning decorator → rc=1 at `28c6837`
  (decorator **syntax** is the gap: `@deco` is not an `ast.Call`, so the implicit
  `deco(f)` at definition time is never scanned).
- `__post_init__` really runs on construction: `Case(['/bin/echo','post-init-ran'])` printed
  `post-init-ran` (rc 0). `functools.lru_cache`'s list argument really fails before the body:
  `TypeError: unhashable type: 'list'`.

`@functools.cache`/`lru_cache` are pure, so the two wants are *semantically* right; the defect
is that the case cannot distinguish "the decorator is pure" from "decorators are ignored", and
that the tool's class exemption is unconditional on the class body's content. The two dataclass
cases cannot distinguish "stores argv" from "class body never inspected". This is the same
mechanism independently reported by `AtkCasesP2` F1/F3 for `P-CasePureCallables-dataclass-ctor`,
`P-CasePureCrossCell-dataclass-case` and `P-CasePureCallables-same-text-decorator`; these four
are the `CaseAdoptW2` instances. No scored case covers the spawning variant (`grep -rn
"__post_init__" .ufo/waves/round-19 .ufo/waves/round-20 --include=*.jsonl` → no match;
`grep -n post_init tools/mado-tripwire.py` → no match), so the suite cannot see it.

Consequence for C1's whole-corpus no-harm guard (`SCORECARD.md:1258-1260`, pending wave 2):
the guard counts rows, and the dataclass-postinit twin loses 3 rows and the decorator twins lose
1–2 each versus `1f7f995`. [UNK] whether the scanned corpus contains these shapes. The old rows
on the dataclass twin come partly from the old over-broad rule (a literal handed to a ctor),
so they are not proof the old tool reasoned about `__post_init__`; the repaired tool's miss is
real regardless of the old mechanism. Recommend the corpus/no-harm seat grep the corpus for
`__post_init__` and `@<name>` definitions with spawn bodies before reading "loses zero
findings" as complete.

### F2 (non-independent scored shapes; 4 of 19) — exact AST-shape duplicates of other P cases

AST dump with every string constant normalized to `STR` (command under Limits). The 19 sit in
four duplicate groups; the other member(s) are scored P cases from other seats:

- `dc-shlex-join` = `P-CasePureFormatters-shlex-join`
- `dc-lambda` = `P-CasePureFormatters-lambda-join` = `P-CasePureCallables-lambda-same-cell`
- `b06` = `P-CasePureBuiltins-format-list`
- `b16b` = `P-CasePureBuiltins-frozenset-direct`

Plus three internal near-duplicate pairs on the same construct with only binding/print
differences: `dc-dataclass`/`b17` (dataclass store), `dc-deque`/`b18b` (deque of literals),
`dc-frozenset`/`b16b` (frozenset of `pacman -Q`).

These are **not vacuous** under the measured-revision test (each fails at `1f7f995`), but they
cannot fail independently of their twin under any rule that does not key on the argv strings.
Effect on the score: removing the 4 duplicate `CaseAdoptW2` members gives P 62/62 and
**168/171 = 9.8246** (instead of 172/175 = 9.8286); removing all 8 duplicate Python-shape
members suite-wide gives N 167 and 164/167 = 9.8204. The C1 claim is not falsified; the
denominator is 4 slots larger than the number of independent shapes it claims to measure.

### F3 (cannot fail on the body its `why` names) — b15 and b20

- **b15** (`def outer(): def log(args): print(args); log([...])`): `outer()` is never called, so
  the tool never enters the body and never sees `log([...])`. Measured: the same fixture with
  `log` changed to `subprocess.run(args)` is **rc=0 clean** at `28c6837`; adding `outer()` and
  the same spawn is rc=1. The case therefore tests "a literal inside an uncalled def is not
  flagged", not "the nested def's body is pure". Its `why` states the latter.
- **b20** (`async def note(argv): return print(argv)`; `note([...])` not awaited): measured, the
  same async body with `subprocess.run(argv)` and no `await` is rc=0; with `await` it is rc=1.
  Clean is semantically right (nothing runs), but the case cannot fail on body content.
- Note on **b21**: at runtime the call raises `TypeError` before the body (measured), so no
  dynamic path reaches `' '.join`; the *detector* still scans the body (list + spawn twin is
  rc=1), so b21 is content-sensitive and not vacuous for the tool. Only the `why`'s implicit
  runtime reading is off.

### F4 (wrong or incomplete `why` statements)

- **b16b** — `why` says "b23 frozenset(['pacman','-S',...]) merged: same shape, **host_mutation
  at 1f7f995**". The adopted file's measured `1f7f995` output is one `package_query /
  pacman:-Q / line 1` row; there is no `host_mutation` row. The parenthetical describes the
  pre-merge b23, but as written it states a row class this case does not produce.
- **b06** — `why` cites `format(['sudo','pacman','-Syu',...])`; the adopted payload is
  `format(['pacman','-Q','wayland-utils'])`. "Same shape" is true; the argv provenance is stale.
- **b15** — omits that `outer()` is never called (see F3).
- **b21** — omits the runtime `TypeError` (see F3).
- **dc-type-hint-shape** — the name says type-hint shape; the payload is two duplicate `check`
  defs with no annotations. Cosmetic, but the name is the only index a reader has.

### F5 (family assignment, lower severity, `[INFERENCE]`)

`dc-type-hint-shape` and `b22` are duplicate-def/binding cases (their `why` cites E3); the
registered family split says **S** is binding/shadowing and **P** is "pure containers/formatters
(want clean)" (`SCORECARD.md:1250-1253`). Reclassifying the two gives P 64, S 19; both minima
unaffected, total unchanged. [INFERENCE] because the two definitions overlap (P is stated as a
shape+want, S as a mechanism).

### F6 (the P family is one-sided: all 19 pass with the Python analyzer deleted)

Mutant of `28c6837` with the Python AST path removed (`return hits, 0, 0` immediately before
`compile(...)`, line 1785; `!`/`%%bash` handling retained):

| tool | P | 19-set | total | score |
|---|---|---|---|---|
| mutant, no Python AST analysis | 66/66 | **19/19** | 120/175 | 6.8571 |
| stub, always clean exit 0 | 66/66 | **19/19** | 109/175 | 6.2286 |
| `28c6837` | 66/66 | 19/19 | 172/175 | 9.8286 |

So no P case — and none of the 19 — can fail on under-detection; "P 66/66" certifies that these
shapes are not over-reported, not that the tool resolved them. This is consistent with the
declared family design, but it means 30′'s detector-precision green is one-sided, and the only
family that requires a row is L. A reader must not cite P 66/66 as evidence that the repair
classifies `@dataclass`, decorator, lambda, etc.; F1 shows exactly where that inference breaks.

### F7 (`evidence` untested; `before` inert)

All 19 want `findings: []`, so no `evidence` value is pinned by these cases; the P family
cannot detect an observed/lead marking regression. `grep -n "before" .ufo/waves/round-20/
tw-precision.py` → no match (rc 1), so the counter never reads `expected.json`'s `before`; a
wrong `before` would not be caught. Here all 19 (and all 66 P) match my independent
re-measurement, so nothing surfaced.

## What would have refuted the confirmations

- Any of the 19 emitting a row at `28c6837` or `9c54c56`: would have made the want wrong or
  shown over-firing — measured none (19/19 clean at both).
- Any of the 19 passing at `1f7f995`: would have made it a non-discriminating control —
  measured 19/19 fail, each with the rows in the table.
- Any `before` mismatch: 0 across 66 P × 2 revisions.
- A spawn token in a fixture: none in 19 (regex above).
- A dataclass/decorator twin that was also clean at `1f7f995`: would have made F1 a pre-existing
  gap rather than a row-losing change — measured rows at `1f7f995`, none at `28c6837`.
- A dataclass with an explicit spawning `__init__` or an explicit `f = deco(f)` that was *also*
  clean at `28c6837`: would have shown the whole construct is blind — both are rc=1, so the
  gap is specifically generated `__init__`/`__post_init__` and decorator syntax.

## Limits

- Scope is the 19 scored `CaseAdoptW2` P cases. `AtkCasesP1` covers Builtins/Collections;
  `AtkCasesP2` covers Formatters/Callables/CrossCell. I did not run the isolation check,
  `tally-check.py`, the recall suites, the 11 existing suites, the frozen replay, or the
  whole-corpus diff — other wave-2 items own those.
- `9c54c56` was measured through the suite pin `f3da504` (only P matters here); its own suite is
  not used. `1f7f995` rows have no `evidence` key; the counter normalizes them to `observed`.
- Twins are `--scan`-only JSONL under `/tmp`; no fixture code was executed. The only executed
  code was `/bin/echo` through a dataclass `__post_init__` and the `lru_cache` `TypeError`
  probe. Host pause honoured: no pacman/yay/jj/hyprctl/systemctl/service/compositor call; host
  files read as bytes.
- Decorator-application and dataclass `__post_init__` execution are CPython semantics
  `[INFERENCE]` plus the two probes; the twins' spawns were not executed.
- F1's corpus implication is `[UNK]`: I did not run the corpus diff. My one corpus grep found
  `__post_init__` only in an unrelated project's logs and in this round's own seat transcripts,
  not in a lane transcript with a spawn.
- AST-shape duplicates are computed with string constants normalized; a tool keyed on argv
  strings could still separate a duplicate pair, so F2 is about independent failure under a
  content-general rule.

## Installs

none.
