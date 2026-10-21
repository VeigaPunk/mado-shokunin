# CaptureStarUnknown — C1 static-truth proposal (expected_kind: uncertain)

Seat: `MadoR22.CaptureStarUnknown` · Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`
Wave: round-22 w1 (authorized recovery, NOT admission). Artifacts only; nothing executed, nothing measured.

## Delivered artifact

| Item | Value |
|---|---|
| Proposal | `.ufo/waves/round-22/w1/proposals/CaptureStarUnknown.json` |
| Proposal file sha256 | `459af4c81ec067ad685032f72b661030ae291ccb8ce1437bc11c381a8930ee62` |
| Cell[0] sha256 | `6aff041ae7b9637889e99a2a4f7307ae6703b35077735738f23716c2a3d7c784` |
| `expected_kind` | `uncertain` |
| `want` | `[]` (no statically determined spawn argv exists) |
| `forbid_observed_commands` | `pacman -Q r22-starunk-decoy`, `pacman -S r22-starunk-decoy` |
| `forbid_commands_any_tier` | `pacman -Q r22-starunk-decoy`, `pacman -S r22-starunk-decoy` (parent-directed stricter tier) |
| `require_signal` | `true` (zero rows AND zero unparsed is a miss, not a pass) |

## Cell (inert transcript source; never executed)

```python
import subprocess


def make(unknown):
    def run():
        subprocess.run(unknown)
    return run


unknown = ["pacman", "-Q", "r22-starunk-decoy"]
parts = list(input())
runner = make(*parts)
runner()
```

## Static semantic argument (Python 3.14.8)

1. `parts = list(input())` binds `parts` to a non-literal call result. `input()` is
   opaque to static analysis: the starred expression's runtime element count and
   values are statically unknowable.
2. `make(*parts)` is the r21 F2 "starred non-literal argument" trigger (FinalBindingReview
   lines 78-83, bind_literal 1972-1976). Runtime has two disjoint branches:
   `*parts` unpacking to anything other than one element raises TypeError before
   `runner` binds (`runner()` then raises NameError); unpacking to exactly one
   element binds make's parameter `unknown` to that element's value.
3. Either way, `run`'s use of `unknown` is a free variable resolved via the
   nearest enclosing scope — make's parameter closure cell — never the module
   namespace (executionmodel.rst lines 89-93, 113-115). The module global
   `unknown = ["pacman", "-Q", "r22-starunk-decoy"]` is unreachable from `run`.
4. The decoy exists only to catch the F2 fabrication: any row at ANY evidence
   tier naming `pacman -Q r22-starunk-decoy` (or the `-S` sibling) is a
   same-named-module-global borrow, not a value reachable from this transcript.
5. The only spawn site has an unresolvable argv, so no command string is
   statically determined. `want` is empty by construction — a lead row requires
   a serializable command and inventing one would itself be fabrication.
6. Honest outcome contract: zero observed rows AND at least one uncertainty
   signal (lead row and/or nonzero unparsed-spawn count; the documented sweep
   contract marks swept parameters unknown and every found row lead). Silence is
   a miss → `require_signal: true`.

## Independence vs. the r21 F2 fixture

Not a copy of `capture-unbound-global.jsonl`: that fixture left the starred
source `parts` unbound (NameError at the call; closure never invoked) and used
`argv` as both parameter and decoy global. Mine binds `parts` to an opaque
non-literal (`list(input())`), so the call is well-formed source and the closure
invocation genuinely happens with an unknowable bound value, and the decoy
global carries the parameter's name (`unknown`), which exercises the parameter→
global fallthrough directly rather than coincidentally.

## Uncertainty-contract mapping

- "no observed invented argv": enforced by empty `want` plus both forbid lists
  covering the only command literal present in the cell.
- "at least lead or explicit unparsed": the swept-body spawn cannot produce an
  exact row; `require_signal: true` demands a lead row and/or unparsed count,
  matching "The sound output is unparsed or lead" (FinalBindingReview line 81).

## Sources

- `round-21/residual/FinalBindingReview.md` F2 (lines 78-83), sweep contract
  (lines 2179-2186), W2 NamespaceBinding #1 remedy (line 82).
- `tools/mado-tripwire.py` docstring lines 38-46, 47-56, 75-81 (read as source
  text/data; contract wording for observed/lead/sweep — no detector execution).
- Fetched official refs: `w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-
  executionmodel.rst` (89-93, 113-115) and `...-compound_stmts.rst` (1326-1336);
  `expressions.rst` call-unpacking via https://docs.python.org/3.14/reference/
  expressions.html#calls (not vendored this wave).

## Status / unknowns / hygiene

- **Parent addendum (any-tier forbids):** incorporated inline before delivery —
  `forbid_commands_any_tier` and `require_signal` are in the proposal body; no
  separate addendum file was needed since nothing was frozen yet. OracleHarness
  notified.
- **Open semantic unknown:** whether a sound implementation reports the swept
  unknown-argv spawn as a lead row (command-bearing) or as an unparsed-spawn
  count is implementation-defined by the tool's documented contract; the spec
  accepts either, hence `expected_kind: "uncertain"` with `require_signal`.
- **No execution:** the cell was verified parse-only via `ast.parse` (syntax
  well-formedness as data); no subprocess, scanner, or fixture run.
- **Tools installed:** none.
- **Git:** read-only; no lane state, index, or sibling file touched.
- **No detector measurement** performed or consulted for expectations.
