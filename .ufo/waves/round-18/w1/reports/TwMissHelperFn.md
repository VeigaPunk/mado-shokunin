# TwMissHelperFn — same-text helper resolution (round 18, wave 1)

Seat: MadoR18.TwMissHelperFn. Item: real tripwire miss at MadoR13.jsonl:470 (helper
`run_record` wrapping a package query); design the **narrowest sound** rule for a function
defined in the same command text and then invoked, body classified with the call's
arguments substituted **only when literal**. Deliverable: one patch, one fixture suite
with negative controls, this report. No git/jj writes in the lane; all work on /tmp copies.

## Files written

| Path | What | SHA-256 |
|---|---|---|
| `.ufo/waves/round-18/drafts/TwMissHelperFn.patch` | unified diff vs `git show d9a5a18:tools/mado-tripwire.py` (7 hunks, 298 lines) | `6cf9ca69ffd192732d98af3bf548766241ac4ea7c471d1c76268f46384bc1bcf` |
| `.ufo/waves/round-18/tripwire/r18-helperfn/expected.json` | 24-case suite (10 positives, 14 negatives/guards) | `fc56ea24e99ea0d9a790623c66a361e384a49d97e565bd3c66081e66260518d7` |
| `.ufo/waves/round-18/tripwire/r18-helperfn/*.jsonl` | 24 synthetic fixtures | — |
| `.ufo/waves/round-18/w1/reports/TwMissHelperFn.md` | this report | — |

The patch applied with `patch -p1` to a fresh `d9a5a18:tools/mado-tripwire.py` reproduces the
tested tool byte-for-byte: `sha256 1a70bf235583f0ccaa83fa180191fb01b15e2b42852cc0f61a253b341f96a1fd`.

## The rule (as implemented)

One principle, two definition forms, both restricted to a **single command text**:

1. **Python `def` (the incident's shape).** In `classify_eval`, top-level `FunctionDef`s of the
   same cell are indexed by name; a def name seen twice in the cell is dropped (ambiguous). A
   call to that name **after** its `def` line is dispatched when every positional and keyword
   argument is literal (`str`/`int`/`float`/`bool`/`None`, or a `list`/`tuple` of those) and every
   parameter the call leaves out has a literal default. No varargs, no `*`/`**` at the call, no
   starred arguments. Bound names are then resolved inside the body (depth ≤ 4, ≤ 8 name hops) so
   `subprocess.run(args)`, `os.system(cmd)` and `subprocess.run(cmd, shell=sh)` classify with the
   literal value the call states. A call with any non-literal argument resolves to nothing.
2. **Shell functions.** `name() { ... }` and `function name { ... }` are collected per
   `classify_shell` text; the closing `}` must be in the same text (otherwise the def is dropped),
   a name defined twice is dropped, and a call must occur on a later logical line. A call whose
   arguments contain no expansion metacharacters (`$`, backtick, `*`, `?`, `[`, `{`, `~`, newline)
   substitutes `$1..$9`, `$@`/`$*`, `${...}` **outside single quotes** (bash does not expand there;
   `"$@"` is emitted as one quoted word per argument, which is bash's special case) and classifies
   the expanded body. A positional the call does not supply yields no substitution, never a guess.

Additive only: the old module-level body walk is unchanged, so a literal command inside a never-
called body is still reported exactly as before; findings dedupe per `(class, rule)` per toolCall.
`unparsed_spawns` semantics are unchanged (a helper body's non-literal spawn site is counted where
the body is defined, not re-counted per call).

Docstring limits updated: "helpers defined in one text and called from another" is now an
explicit stated limit, alongside a new paragraph describing the same-text substitution.

## Evidence

Existing suites, patched copy (`9+16+33+30 = 88/88`):

| Suite | Round 17 baseline (`962919ce…`) | Patched (`1a70bf23…`) |
|---|---|---|
| core | 9/9 | **9/9** |
| compound | 16/16 | **16/16** |
| hardening | 33/33 | **33/33** |
| w2-regressions | 30/30 | **30/30** |
| r18-helperfn (new) | 14/24 | **24/24** |

The new suite is shown able to fail: against the base tool exactly the **10 positive cases** fail
(`py-helper-literal-list`, `py-helper-shell-string`, `py-helper-shell-kw`, `py-helper-two-hop`,
`py-helper-keyword`, `py-helper-literal-twice`, `sh-fn-positional-at`, `sh-fn-positional-n`,
`sh-fn-function-keyword`, `sh-fn-oneline`); all 14 negatives pass on both tools, as controls should.

Incident measurements on the real transcript
(`…/2026-10-20T01-48-55-258Z_01a156ff-…/MadoR13.jsonl`, read-only):

| Scan | verdict | findings | unparsed_spawns |
|---|---|---|---|
| base | clean | 0 | 5 |
| patched | clean | 0 | 5 |

So the patch changes nothing on that transcript — deliberately, and the reason is the scope:

- line 470 (2121-byte eval cell) calls `run_record('packages',['pacman','-Q',…],0)` but defines
  nothing; the definition lives at **line 437** (1803-byte eval cell):
  `def run_record(name,args,expected=None,stdin=None,extra_env=None,timeout=300):` with
  `cp=subprocess.run(args,cwd=root,input=stdin,…)`. A **same-text** rule cannot see across cells,
  and the base tool already counts that one body site among the 5 `unparsed_spawns`.
- **Proof the rule covers the shape when the text is whole:** I joined exactly those two cell
  texts into one synthetic cell in /tmp. Base: `clean`, no findings, unparsed 2. Patched:
  `findings`, `package_query pacman:-Q`, unparsed 2. The same command, with def and call in one
  text, is resolved; split across cells it is not.

This is the honest boundary of the item as written ("defined in the same command text and then
invoked"). Catching line 470 as it actually exists would require modelling kernel state across
cells (def seen in an earlier assistant cell, not rebound, same session, no `%reset`) — a
different, much larger rule than was assigned, and one whose soundness depends on cell ordering
and execution success that a single toolCall does not expose. Flagged for L1 as a round-19
candidate, **not implemented here**.

## Negative controls (all 14 verified clean or exact-set)

| Fixture | Property it pins |
|---|---|
| `py-helper-uncalled` | def only, body spawn stays unparsed, no finding |
| `py-helper-nonliteral-arg` | call argument is a variable → no substitution |
| `py-helper-defined-after-call` | call precedes the `def` → no substitution |
| `py-helper-redefined` | two defs of one name → ambiguous, dropped |
| `py-helper-vararg` | `def f(*a)` → never bound |
| `py-helper-recursive` | self-recursive helper terminates (depth cap), no finding |
| `py-helper-nonspawn-body` | literal list passed to a non-spawn `print` → no finding |
| `py-helper-binop-body` | body does `args + [...]` → not literal after binding |
| `py-helper-default-nonliteral` | missing param default is a `Name` → no substitution |
| `sh-fn-uncalled` | `f() { "$@"; }` never called → clean |
| `sh-fn-nonliteral-arg` | call arg `"$cmd"` contains `$` → no substitution |
| `sh-fn-called-before-def` | shell call precedes the definition → no substitution |
| `sh-fn-unterminated` | definition without its `}` in the text → dropped |
| `sh-fn-single-quoted` | `sh -c 'pacman $1'` + `f -Q` → **only** `package_query pacman`; no `pacman:-Q` (single quotes never expand) |

## Risks / integration notes

- Patch base is `d9a5a18:tools/mado-tripwire.py` (`962919ce…`). A sibling seat is adding
  `--frozen DIR` to the same file; the two patch sets touch disjoint regions (`classify_shell`
  head/loop, `classify_eval` tail, docstring limits) but L1 should apply them in one order and
  re-run all five suites — the frozen selftest cases run `--frozen`, not `classify_*`, so a clean
  merge should keep 88/88.
- Shell parsing is deliberately shallow: brace-on-next-line (`function f` newline `{`), nested
  functions, and `}`-terminated one-liners with trailing commands are accepted only in the forms
  described; anything else yields no substitution (a miss, never a fabricated hit).
- Name shadowing: if a cell both `from subprocess import run` and `def run(...)`, the same-text
  helper wins for calls after the def; documented, not resolved.
- `/tmp/tw18` (first lab) was wiped by another process at 12:48; rebuilt as
  `/tmp/mado-r18-helperfn-lab` and re-validated. No lane artifact was affected.

## Reproduction

```sh
# base → patched
git -C <lane> show d9a5a18:tools/mado-tripwire.py > /tmp/base.py
mkdir -p /tmp/v/tools && cp /tmp/base.py /tmp/v/tools/mado-tripwire.py
cd /tmp/v && patch -p1 < <lane>/.ufo/waves/round-18/drafts/TwMissHelperFn.patch

# existing suites + new suite
for d in core compound hardening w2-regressions; do
  python3 -I /tmp/v/tools/mado-tripwire.py --selftest <lane>/.ufo/waves/round-17/tripwire/$d | tail -1
done
python3 -I /tmp/v/tools/mado-tripwire.py --selftest <lane>/.ufo/waves/round-18/tripwire/r18-helperfn | tail -1
```

Tooling installed/upgraded: **none** (stdlib-only work; no pacman/uv/npx used, host pause respected).
