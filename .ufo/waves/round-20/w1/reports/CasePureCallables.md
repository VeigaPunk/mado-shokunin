# CasePureCallables — 14 P cases delivered (12 red at 1f7f995, 14/14 pass at 9c54c56, 2 controls); every same-text pure callable outside rule A's index reproduces the rule-B harm

All paths are absolute or relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`. Seat dir:
`.ufo/waves/round-20/w1/cases/CasePureCallables/` (14 `.jsonl` + `cases.json`). Fixture code was never
executed: the only programs run against it were the two pinned tools' `--scan` (a text parser). No lane file outside
the seat dir, this report and `.ufo/waves/round-20/fetch/CasePureCallables/` was written; no git/jj write; no host probe.

## Method (commands as run)

```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 1f7f995:tools/mado-tripwire.py > /tmp/CasePureCallables/tool-1f7f995.py
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 9c54c56:tools/mado-tripwire.py > /tmp/CasePureCallables/tool-9c54c56.py
sha256sum → 367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d  tool-1f7f995.py
            c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd  tool-9c54c56.py
(e629f73:tools/mado-tripwire.py is also 367be947…; refs/heads/master = e629f731172b8238caffe50f152217ce56535fb4)
python3 -I /tmp/CasePureCallables/gen.py   <seat dir>                 # writes the jsonl + cases.json (text only)
python3 -I /tmp/CasePureCallables/before.py <seat dir> /tmp/CasePureCallables/scan before.json raw.txt
```

`before.py` copies the seat dir to `/tmp/CasePureCallables/scan`, then per case and revision runs
`python3 -I /tmp/CasePureCallables/tool-REV.py --scan FILE` with cwd = the copy, and applies the counter rule: pass iff
exit equals `want_exit` AND the multiset of (class, rule, line, evidence) equals `want_findings`, a row without an
`evidence` key counting as `observed`. A second independent copy/run (`scan2`) gave a byte-identical before map
(`cmp before.json before2.json` → `BEFORE-STABLE`). Every scan at both revisions reports `eval_unparsed: 0`, so each
cell parsed (including the top-level `await`). Scratch scripts stay in `/tmp/CasePureCallables/` (not lane files).

Envelope: the one-line shape of `.ufo/waves/round-19/tripwire/r19-helperfn/py-lead-cross-cell-literal.jsonl`
(`type` message, `message.role` assistant, one `toolCall` `eval` `{language:"py",code}`), compact JSON. Every case is a
single jsonl line, so a row would be `line: 1`; every case wants `want_exit: 0`, `want_findings: []`.

## Cases and before (counter rule)

| # | name | file | 1f7f995 | 9c54c56 | 1f7f995 rows (class / rule) |
|---|---|---|---|---|---|
| 1 | P-CasePureCallables-dataclass-ctor | dataclass-ctor.jsonl | fail | pass | host_mutation/sudo, host_mutation/pacman:-S |
| 2 | P-CasePureCallables-plain-class-init | plain-class-init.jsonl | fail | pass | package_query/pacman:-Q |
| 3 | P-CasePureCallables-functools-cache-def | functools-cache-def.jsonl | fail | pass | host_mutation/sudo, host_mutation/pacman:-S |
| 4 | P-CasePureCallables-async-def-await | async-def-await.jsonl | fail | pass | package_query/pacman:-Q |
| 5 | P-CasePureCallables-duplicate-def | duplicate-def.jsonl | fail | pass | host_mutation/sudo, host_mutation/pacman:-S |
| 6 | P-CasePureCallables-duplicate-def-later-spawner | duplicate-def-later-spawner.jsonl | fail | pass | package_query/pacman:-Q |
| 7 | P-CasePureCallables-duplicate-def-earlier-spawner | duplicate-def-earlier-spawner.jsonl | fail | pass | package_query/pacman:-Q |
| 8 | P-CasePureCallables-nested-def | nested-def.jsonl | fail | pass | package_query/pacman:-Q |
| 9 | P-CasePureCallables-nested-def-param | nested-def-param.jsonl | fail | pass | package_query/pacman:-Q |
| 10 | P-CasePureCallables-lambda-same-cell | lambda-same-cell.jsonl | fail | pass | host_mutation/sudo, host_mutation/systemctl:restart |
| 11 | P-CasePureCallables-transitive-class | transitive-class.jsonl | fail | pass | package_query/pacman:-Q |
| 12 | P-CasePureCallables-same-text-decorator | same-text-decorator.jsonl | fail | pass | vcs_write/git:commit |
| 13 | P-CasePureCallables-staticmethod-classmethod-control | staticmethod-classmethod-control.jsonl | pass | pass | — (control) |
| 14 | P-CasePureCallables-two-hop-plain-control | two-hop-plain-control.jsonl | pass | pass | — (control) |

Contract check: 14 cases ≥ 6; 12 red at 1f7f995 ≥ 4; 2 controls ≤ 2; names unique, prefixed `P-CasePureCallables-`;
every P case passes at 9c54c56 (the admission guard). `cases.json` keys are exactly name/family/file/want_exit/
want_findings/why/before (validated by script); controls are marked by the `-control` slug and a `Control:` why, not by
an extra key. No fixture string contains a `/` or a ≥ 32-char token (checked by regex); file names do not collide with
the CasePureBuiltins / CasePureCrossCell / CasePureCollections / CaseLeadsInvisible dirs present when I listed them.

Shapes (code abridged; exact bytes in the files):
1. `@dataclass class Case: name: str; argv: list` → `cases = [Case('mut1', ['sudo','pacman','-S','--noconfirm','foo'])]`, print loop.
2. `class Step:` `__init__` assigns `label`, `argv = list(argv)`; `__repr__` joins → `Step('query', ['pacman','-Q','hyprland'])`.
3. `@functools.cache def show(argv): return ' '.join(argv)` → `print(show(('sudo','pacman','-S','--noconfirm','foo')))` (tuple: cache arguments must be hashable, S1xx-pending row C).
4. `async def show(argv): print(argv)` → `await show(['pacman','-Q','hyprland'])`.
5. two printing `def check(name, argv)` → `check('x', ['sudo','pacman','-S','--noconfirm','foo'])`.
6. pure `def show` → call `show([... 'hyprland'])` → later `def show(argv): return subprocess.run(argv)` (binding in effect = first, pure).
7. `def show(argv): return subprocess.run(argv)` → pure redefinition → call (latest preceding binding = pure).
8. `def report():` nested `def show(argv): print(' '.join(argv))`; `show(['pacman','-Q','hyprland'])`; `report()`.
9. `def report(pkg):` nested formatting `show`; `print(show(['pacman','-Q', pkg]))`; `report('hyprland')`.
10. `fmt = lambda argv: ' '.join(argv)` → `print(fmt(['sudo','systemctl','restart','elephant']))`.
11. `class Row:` `__init__` joins; `def render(argv): return Row(argv).text` → `print(render(['pacman','-Q','hyprland']))`.
12. same-cell logging decorator `traced(fn)` → `inner(*args)` prints, returns `fn(*args)`; `@traced def show(argv)` joins → `print(show(['git','commit','-m','wip']))`.
13. control: `class Fmt` with `@staticmethod show` / `@classmethod label` → `Fmt.show([...pacman -Q...])`, `Fmt.label([...sudo pacman -S...])`.
14. control: plain `def quote(argv)` + `def note(label, argv): print(label, quote(argv))` → `note('query', ['pacman','-Q','hyprland'])`.

Provenance of the assigned shapes: `.ufo/waves/round-19/w2/reports/CriticC3W2.md:129` (dataclass `Case('mut1',…)`),
`:132` (lambda + systemctl restart elephant), `:133` (`@functools.cache def show`), `:139` (async def + await), `:140`
(duplicate printing def); `.ufo/waves/round-19/w2/reports/AdvHelperFn.md:48-54` (b15 nested def, b20 async, b21
lru_cache, b22 dup def, b07/b17 class/dataclass, b08 lambda).

File digests (`sha256sum`, seat dir):

```
ff264cfd71853b051e6211d9f89ae388fe7be993b0b1b757d950a2b00d0311e8  dataclass-ctor.jsonl
2ac2a413e6407b2d6b65e353eacfdc430252ec3f17e12601f664c21598fccf8e  plain-class-init.jsonl
0e248bbf45cdd3eae5d829210b4860f048610441f6a30c106edf7d75b434ee38  functools-cache-def.jsonl
60bfadc99a80bd69126b149ec4a508c30d04343fb778b66400b565391f535dde  async-def-await.jsonl
46be903e7e942928f5e2ce7b728b13286062c2187e36f65fdeceed9a593b85ba  duplicate-def.jsonl
91a23000843a3c09931a92b5254ede033212ca3b94decb591a02846a0c542173  duplicate-def-later-spawner.jsonl
001daa61173e82718e2d982c29125363a4171220e67eb955df371c28073c67b3  duplicate-def-earlier-spawner.jsonl
919e19cb34304446586c4bce0146f771e196b8b262a5f57411cdf7cb3bc40223  nested-def.jsonl
c55c6dfadb9e5cd054fd9443e50d0e67ab5155589ea8fc10234dc30dd420294d  nested-def-param.jsonl
973f541927115dab133a7f7400359ba107c1ccbb13be9b7e0ca80738be815a05  lambda-same-cell.jsonl
881c999a8e34ab605295666b4e4477ffe79911e39edbfbd72fdbdf5add7d1f98  transitive-class.jsonl
aff322d3e271a0d6c134a5aa4f5440c6fa31f275745bfa0f0e5577f0e777755f  same-text-decorator.jsonl
0967a92d8259edcbb52c6f846d41b9f3f78dba9e0c8f3322cac5812eba9f2f21  staticmethod-classmethod-control.jsonl
c906eb8d339b1a3ed146f17636879c076839ce82426529f55ff25864e71494b6  two-hop-plain-control.jsonl
249c8aef350156f84dc9bda9e86f80c9c7617e271a257452f9495d2e58deb1a0  cases.json
```

## Exact scan output for each red (1f7f995)

Each red printed line 1 `MADO_TRIPWIRE: findings` and a JSON line with `"exit": 1`. Below: the verbatim `findings`
fragment of that JSON line (checked to be an exact substring and to re-parse to the verdict's list), and the sha256 of
the full two-line stdout. No row carries an `evidence` key, so the counter reads each as an observed execution claim.

1. dataclass-ctor (stdout sha256 `2882865a3cf28cd5953ecbd4956e3ea2d480feea6405b951b192cf5ee3edd11b`)
   `"findings": [{"argv0": "sudo", "class": "host_mutation", "command": "sudo pacman -S --noconfirm foo", "file": "dataclass-ctor.jsonl", "line": 1, "rule": "sudo", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}, {"argv0": "pacman", "class": "host_mutation", "command": "pacman -S --noconfirm foo", "file": "dataclass-ctor.jsonl", "line": 1, "rule": "pacman:-S", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
2. plain-class-init (`236a91b11f1491a84b594524e8ca35a35beac5171aa5fa5486934469df3e4700`)
   `"findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "plain-class-init.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
3. functools-cache-def (`b03afcff2ce605eaebc7e1205c75c9ec06a02d3c92191e39a0e43063c45a45d5`)
   `"findings": [{"argv0": "sudo", "class": "host_mutation", "command": "sudo pacman -S --noconfirm foo", "file": "functools-cache-def.jsonl", "line": 1, "rule": "sudo", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}, {"argv0": "pacman", "class": "host_mutation", "command": "pacman -S --noconfirm foo", "file": "functools-cache-def.jsonl", "line": 1, "rule": "pacman:-S", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
4. async-def-await (`e02fc5dad91e14a1b4c811223bdc5844515803be88c594ed210391a6c30f5ccd`)
   `"findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "async-def-await.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
5. duplicate-def (`3286b9508d7370a071e3a74c247ccaefe29e5697121b97d2c6c866d959df0485`)
   `"findings": [{"argv0": "sudo", "class": "host_mutation", "command": "sudo pacman -S --noconfirm foo", "file": "duplicate-def.jsonl", "line": 1, "rule": "sudo", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}, {"argv0": "pacman", "class": "host_mutation", "command": "pacman -S --noconfirm foo", "file": "duplicate-def.jsonl", "line": 1, "rule": "pacman:-S", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
6. duplicate-def-later-spawner (`8e650dce13f2f005eb30f9a27f4eb75484193fd39979be6a99955d8d786d6ec5`; `unparsed_spawns: 1`)
   `"findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "duplicate-def-later-spawner.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
7. duplicate-def-earlier-spawner (`caf156cb8fb73eb4145d4f7d2c7c58f2f0e7fcc240f88cdfd3e0bab182d336c4`; `unparsed_spawns: 1`)
   `"findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "duplicate-def-earlier-spawner.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
8. nested-def (`2bb27c54ea8157da535b0e768395cff2c749b9f9395c0f0c12cb2c51763cfc9a`)
   `"findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "nested-def.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
9. nested-def-param (`fc6f59a8329369cf53641641bfd80377cef32682dd16cbf2bd805df8101d9520`)
   `"findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "nested-def-param.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
10. lambda-same-cell (`efd9fae3772d15d10b5019eef11d80d56f9db931322fc8d67b41090abb52e07f`)
   `"findings": [{"argv0": "sudo", "class": "host_mutation", "command": "sudo systemctl restart elephant", "file": "lambda-same-cell.jsonl", "line": 1, "rule": "sudo", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}, {"argv0": "systemctl", "class": "host_mutation", "command": "systemctl restart elephant", "file": "lambda-same-cell.jsonl", "line": 1, "rule": "systemctl:restart", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
11. transitive-class (`c1b388c901c092751acccf7aa65d25491318ca396ace405d320d3ce1e9753024`)
   `"findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "transitive-class.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`
12. same-text-decorator (`46c49394c2044644f45ffbc4503123c39c172e8f661e0cdb9afc08e8ab1ad89e`)
   `"findings": [{"argv0": "git", "class": "vcs_write", "command": "git commit -m wip", "file": "same-text-decorator.jsonl", "line": 1, "rule": "git:commit", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}]`

At 9c54c56 all 14 printed `MADO_TRIPWIRE: clean` with `"exit": 0`, `"findings": []` (cases 6 and 7 also report
`unparsed_spawns: 1` for the never-called `subprocess.run(argv)` body). Both controls printed `MADO_TRIPWIRE: clean` at
1f7f995 too (stdout sha256 `c8ac1410…323c` staticmethod, `bd707c5c…5a36` two-hop).

## Findings

**F1. Why each red fires at 1f7f995 (read from `/tmp/CasePureCallables/tool-1f7f995.py`).** Rule A's helper index
is `funcs`, built at `:1368-1372` from `tree.body` (module level only), `ast.FunctionDef` only, `not
node.decorator_list`, and a name seen twice is dropped (`:1371-1372`). Any bare-name call not in that index and not in
`PURE_ARG_CALLS` (`:1252-1257`) takes the lead branch `:1431-1433` and classifies every literal positional argv list via
`helper_argv_leads` (`:1379-1390`). The 12 reds cover seven distinct escape paths: ClassDef (1, 2), decorated def (3,
12), AsyncFunctionDef (4), dropped duplicate (5, 6, 7), nested def (8), assignment-bound lambda (10), and a lead raised
inside a rule-A expansion with bound parameters (`:1412-1417` → `:1431-1433`; cases 9 and 11). A partial fix that only
widens `funcs` to decorated/async module-level defs leaves 1, 2, 5-11 red. At 9c54c56 `classify_eval`
(`tool-9c54c56.py:646-692`) only inspects spawn functions (`:660-661` `continue`s every other call), so no case can
fire there.

**F2. The three duplicate-def cases separate binding orders [INFERENCE for the hypothetical resolvers].** With two
printing defs (case 5) any choice of def is clean. Case 6 is clean only if the call does not resolve to the later
spawning def (a resolver mapping a name to its last def in the cell regardless of call position would substitute the
argv into `subprocess.run(argv)` and read observed `pacman:-Q`); case 7 is clean only if the later def replaces the
earlier one (a "first def wins" resolver reads observed). E3's latest-preceding binding passes both, as does leaving
duplicates unresolved without a lead. Documentary basis: S1xx-pending row A (`compound_stmts.rst:1247-1248`,
`:1253-1254`).

**F3. Contract interaction for TwRuleB / L1 — `r19-helperfn/py-helper-redefined` [INFERENCE].** That existing suite
case wants exit 0 / clean (`.ufo/waves/round-19/tripwire/r19-helperfn/expected.json`). It is a minimal pair with
`py-helper-shell-string`, which wants `package_query/pacman:-Qi`: code
`"import os\ndef run(cmd):\n    return os.system(cmd)\nrun('pacman -Qi wayland')\n"` versus
`"import os\ndef run(cmd):\n    return os.system(cmd)\ndef run(cmd):\n    return os.system(cmd)\nrun('pacman -S wayland')\n"`
(read from both fixtures). The only difference is the duplicate def. Under E1 as the existing rule-A suites apply it
(a literal argument, here a string, substituted into a visible spawning body is observed) plus E3 (latest preceding
binding), the redefined call reads observed `host_mutation/pacman:-S`. A contract-faithful resolver therefore breaks
that case unless it is edited with its reason. My cases do not force this (leaving duplicates unresolved keeps both
clean), but the contract text does. Not measured: the round-20 tool does not exist yet.

**F4. Contract gaps deliberately not authored [UNK].** (a) A visible class whose `__init__` is pure but another
method spawns `self.argv` and is never called: E2 ("body has no spawn") withholds the exemption, yet E1 has no row type
(body visible → not lead; argv reaches no executed spawn → not observed). (b) A call to an instance of a visible class
with a pure `__call__` (`echo = Echo(); echo([...])`): E3 "judged by its binding" does not say whether instance types
are tracked. (c) A pure def decorated by a callable outside the E2 known-pure list (e.g. `contextlib.contextmanager`):
E1 "decorated or not" vs. the decorator being an unseen callable that could replace the function. L1 should rule before
anyone writes cases for these. Cases 3 and 12 avoid (c): `functools` is E2-listed, `traced` is visible and pure.
(d) A pure chain deeper than the depth-4 cap. E2 proves purity only to depth 4, and E1's lead needs a body that is not
visible, so the contract gives no row for a visible body that was never analysed. 1f7f995 stays silent there
(`tool-1f7f995.py:1412`: past `depth < 4` a known helper takes no lead). TwRuleB reports it keeps the cap at four. My
cases reach depth 2 at most (same-text-decorator, transitive-class, nested-def-param, two-hop control).

**F5. Severity at 1f7f995.** These pure-data rows are emitted at full class — `host_mutation` `sudo`,
`systemctl:restart`, `vcs_write` `git:commit` — with no lead marker, identical in shape to the rejected-harm
`BLOCK=frozenset([...])` row (`corpus/lessons/round-19-verifier-spotcheck.md` §C3).

**F6. Recall risk in a purely textual latest-preceding resolver (measured on a /tmp probe; not a seat case).**
TwRuleB replied that it will keep latest-preceding semantics, with any frozen-R19 conflict reported as a
contract-updated case and suite edits left to L1. The caveat I sent back: a call inside a def body binds when that
body runs, not at the call's own line (row A `:1253-1254`). Probe `/tmp/CasePureCallables/probe-deferred/deferred-rebind.jsonl`
(sha256 `b9d081e5a0cf558a8616e99ccc302c7d1c41fb367f6f5e9452a52151efd315bf`, text only, never executed) has code
`def show: print` / `def outer(): show(['pacman', '-Q', 'hyprland'])` / `def show(argv): return subprocess.run(argv)` /
`outer()`. When `outer()` runs, `show` is the spawning redefinition. Scanned: 1f7f995 → exit 1, `MADO_TRIPWIRE: findings`,
`(package_query, pacman:-Q, 1)` with no evidence key; 9c54c56 → exit 0, `clean`, `unparsed_spawns: 1`. A resolver that
uses the call's textual position would read it clean. That loses a 1f7f995 finding which the 9c54c56-baseline corpus
guard cannot see, because 9c54c56 misses it too. It is a W/S shape (want observed), so I did not author it here. L1 may
route it to CaseShadowing or CaseWrapperCrossCell.
TwRuleB then said (its own report of its code; I have not measured it) that its recursion prepares each helper body
with bindings captured at the enclosing call site, so the probe's later redefinition is in effect when `outer()` runs.
I pointed it at cases 8, 9 and 11 (locals inside an expanded body must shadow module names and count as visible).

## Source drafts (S1xx-pending; L1 assigns ids)

Fetch receipts: `.ufo/waves/round-20/fetch/CasePureCallables/receipts.jsonl` (3 lines, sha256
`7c0b5c26fa9e5e2a83c8ae69095c49b9132afbc46f80401bdf4522e83ab0225d`), all `http_status` 200, `final_url` = `url`,
fetched 2026-10-20T19:54:35Z with `curl 8.23.0`. Tag pin: `git ls-remote https://github.com/python/cpython
refs/tags/v3.14.8 'refs/tags/v3.14.8^{}'` → `992560c2cc62d47b308cec662feb485456847931 refs/tags/v3.14.8`,
`8e6e75d9102e39bed2a2b279203a396741180f12 refs/tags/v3.14.8^{}` (saved as `git-ls-remote-v3.14.8.txt`, sha256
`6549cb7c…0ac`, byte-identical to SrcPyBuiltins' copy). Host `python3 --version` → `Python 3.14.8`. Doc text is data.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S1xx-pending (A) | CPython 3.14.8 language reference, compound statements — https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/compound_stmts.rst | docs | A | when a `def` binds its name, when a function body runs, and what name a decorated `def` is bound to, for CPython 3.14.8 | tag v3.14.8 → annotated tag `992560c2cc62d47b308cec662feb485456847931`, peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12`; 70,054 B sha256 `35e6dfbf2794d367774253655d95b6d5ef91ba63084685624144f2b3945e3e2f`; `:1247-1248` "A function definition is an executable statement.  Its execution binds the function name in the current local namespace to a function object"; `:1253-1254` "The function definition does not execute the function body; this gets executed only when the function is called."; `:1262-1263` "The returned value is bound to the function name instead of the function object." | a call sees the latest `def` executed before it (P cases 5-7); an uncalled body runs nothing; a decorated name is the decorator's return, so a visible pure decorator keeps the call pure (case 12) | mined | 2026-10-20 | on-release | round-20 precision suite, P-CasePureCallables-* (L1 binds path) |
| S1xx-pending (B) | CPython 3.14.8 dataclasses reference — https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/dataclasses.rst | docs | A | what `@dataclass` adds to a class constructor, for CPython 3.14.8 | same tag/commit; 34,310 B sha256 `190ca836908da62ad54422b901eb4ec164545a0136594e2e2445680d67e34de4`; `:34` "will add, among other things, a :meth:`!__init__` that looks like::"; `:37` "self.name = name" | a dataclass constructor with a literal argv only assigns fields: `Case('mut1', [...])` is data (case 1) | mined | 2026-10-20 | on-release | same |
| S1xx-pending (C) | CPython 3.14.8 functools reference — https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/functools.rst | docs | A | `functools.cache` wrapper semantics and argument constraint, for CPython 3.14.8 | same tag/commit; 32,022 B sha256 `e938fb679d763ffc02472865a1ffbd816d0f4665068d1419b2d3ac6d1a9fbc31`; `:31` "Simple lightweight unbounded function cache."; `:34-35` "Returns the same as ``lru_cache(maxsize=None)``, creating a thin wrapper around a dictionary lookup for the function arguments."; `:166-167` (lru_cache) "the positional and keyword arguments to the function must be :term:`hashable`." | `@functools.cache` adds a dictionary lookup, not a spawn; arguments must be hashable, hence the tuple argv in case 3 | mined | 2026-10-20 | on-release | same |

Rows B and C are optional; L1 may fold them or drop them to save reserved ids.

## Limits

- The round-20 tool, `tw-precision.py` on the real suite, `tw-recall.py`, the 11 existing suites, the gate and the
  whole-corpus diff were not run; F3 is derived from the E1/E3 text, not measured.
- Runtime claims (dataclass `__init__`, decorator binding, `functools.cache` hashability, coroutine bodies) are
  documentary (rows A-C) or [INFERENCE]; fixture code was never executed.
- Single-cell cases only; cross-cell and reset variants are CasePureCrossCell's. Not checked against seats whose case
  dirs did not exist when I listed (CaseShadowing, CaseWrapper*, CaseHelp*, CaseDryRunBash).
- Reading the tool lines was enough, so I did not use LSP. No labrat was spawned. No /tmp clone (I used a /tmp scratch
  dir with `git show` copies, as the case-format contract describes).

## Installs

none
