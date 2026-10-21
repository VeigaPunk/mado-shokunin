# FalsifyC152 — C1 case `OriginalF2CaptureUnboundGlobal`

Seat: FalsifyC152 (leaf, author-lane advisory). Rev `71228fd582d6d9338d7916cc64e69bd4c2e928b5` target. One authorized bounded measurement; no other scanner runs. No production/fixture edits. Receipt: `.ufo/waves/round-22/w2/receipts/FalsifyC152/result.json` (+ `stdout.raw`, `stderr.raw`, `exit_code.txt`, `argv.txt`).

## Verdict: AGREE (green is semantically correct for this case)

## Independently derived expected truth (pre-measurement, from sealed bytes only)

Fixture `inputs/OriginalF2CaptureUnboundGlobal.jsonl`, sha256 `9ab845d4a8886714cfea0b16203328b67335013f00b21b18ba23e9b7175e1d9d`, byte-identical to r21 source authority `.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/capture-unbound-global.jsonl` (both hashed locally). One eval cell, `reset=false`:

```python
import subprocess
def make(argv):
    def run():
        subprocess.run(argv)
    return run
argv = ["pacman", "-Q", "r21-global"]
runner = make(*parts)
runner()
```

Reasoning: `parts` is never bound, so `make(*parts)` raises `NameError` before the factory body executes; `runner` never binds and `run` never invokes `subprocess.run`. The closure parameter `argv` cannot borrow the same-named module global literal — supported-forms.md: "Its lexical parameter can NEVER borrow a same-named module literal at any evidence tier." Correct static outcome: zero findings, the borrowed `pacman -Q r21-global` absent at ALL tiers (it can never execute), no observed rows, and an explicit uncertainty signal (positive `eval_unparsed`/`unparsed_spawns`) because the spawn argv is statically unresolvable. Sealed grading agrees: `expected_kind=uncertain`, `want=[]`, `accept_exact_want=null`, `forbid_commands_any_tier=["pacman -Q r21-global"]`, `forbid_observed_commands=["pacman -Q r21-global"]`, `require_signal=true`.

## Actual observed evidence (authorized run)

`python3 -I .ufo/waves/round-22/oracle/measure.py --tool tools/mado-tripwire.py --case OriginalF2CaptureUnboundGlobal` → runner exit 0, status `complete`, totals `{"pass": 1, "total": 1}`, no integrity errors (before == after).

Scanner child (one spawn, WRAPPER, 384MiB/15s caps enforced by runner) exit 0, stdout payload:

```json
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0},
 "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1,
            "path": ".../oracle/inputs/OriginalF2CaptureUnboundGlobal.jsonl",
            "sha256": "9ab845d4a8886714cfea0b16203328b67335013f00b21b18ba23e9b7175e1d9d",
            "unparsed_spawns": 1}],
 "findings": [], "lead_findings": 0, "observed_findings": 0, "permitted": [],
 "schema": "mado-tripwire-verdict-v1", "unpermitted": 0, "exit": 0}
```

Row-level grading check against the sealed case: no rows at all → no forbidden command at any tier, no observed row (mandatory for uncertain with null `accept_exact_want`), zero required leads missing; `unparsed = eval_unparsed(0) + unparsed_spawns(1) = 1 > 0` satisfies `require_signal`; file digest/path/shape/exit all clean. Pass is genuine under the exact rules, not subset containment.

## Semantic rationale (green ≠ taken as proof; shape audited)

- The tool's signal attribution is semantically precise for this input: exactly one unresolvable spawn (`unparsed_spawns: 1`) — the `subprocess.run(argv)` inside the closure whose factory call is unbindable. It did not resolve the closure parameter to the same-named module global; the F2 defect mechanism (r21 line-2335 `captured is not None` env leak per FinalBindingReview.md) is absent in this instance.
- The r21 red (fabricated observed `package_query pacman -Q r21-global`, table row F2) resolved by removing a false finding — the only true runtime behavior in the cell is a `NameError`; nothing host-mutating ever executes. This is not a prior-true-finding loss; the r21 output additionally lacked any signal (`eval_unparsed: 0, unparsed_spawns: 0`), so the repair added an honest uncertainty counter where r21 claimed a false observed row.
- `accept_exact_want` vs true uncertainty: this case has no accepted alternate exact multiset. The observed shape (no rows + `unparsed_spawns: 1`) is the true-uncertainty outcome. There is no parsed-clean ambiguity: the tool did not print "clean" as semantics-free; it produced a positive uncertainty signal while `MADO_TRIPWIRE: clean` correctly describes zero findings.
- Lifetime: correct — the closure is recognized as never-invoked/unbindable rather than lifetime-assuming the factory executed.

## Uncertainty boundaries (what this green does NOT establish)

1. Only this frozen input is measured. Variants (e.g. starred argument bound to a resolvable list, keyword-collision without star, bound `parts` later) are untested here; F2 family closure is not implied.
2. A blanket-unparse tool could produce the same shape without understanding NameError semantics; the single-case green proves the borrowed command is absent at all tiers and a signal exists — exactly the sealed oracle's authority, nothing more.
3. `eval_unparsed: 0` vs `unparsed_spawns: 1` split is a defensible attribution (cell parses; spawn argv unresolvable), but whether the tool would account a NameError-aborted cell differently in other shapes is unknown.

## Scope vs current target

This is one of 7 supplemental-original cases in the frozen 57-case C1 population. A green here is bounded static-source-shape agreement for the named tested form only; it does not close the full C1 target (all 57 eligible frozen expectations), does not close defect family F2 broadly, and is not non-author admission. Prior r19/r20/r21 rejected-harmed streak and receipts remain untouched; no admission grant is made or implied. Main owns closure and streak disposition.

## Integrity / hashes

- Tool `tools/mado-tripwire.py` sha256 before == after: `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` (no drift, matches fixed identity).
- Oracle expected.json `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357`; pin file `7cc4aae9…`; runner measure.py `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7`; producer assemble.py `0270c10b90828a895ae3f0a5dec8b2c5610f960a2c1d994aa9409cad702c5600`; truth seal `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4` (106 sealed sources verified before and after); population digest `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad` unchanged; 52 proposal files and 57 inputs verified.
- r21 originals were read only; never executed with the old tool. No extra scanner probes. No installs performed (none needed).
