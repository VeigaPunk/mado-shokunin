# R69ExecDominance — C2 counting command (production draft)

seat: `R69ExecDominance` · axis: operability (C2) · claim: `quality/counters/c2-r69-guard-dominance.py`
frozen declaration: `.ufo/waves/round-69/claims-declaration-r69.md` (frozen at `789a87f1a667b43dd759222a2f048bf8f75b43ce`)
lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` · base rev: `04093b83f73a841117d3b31dbb2a6063f4f2a454`

## Candidate

- draft: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-69/w1/R69ExecDominance/draft/quality/counters/c2-r69-guard-dominance.py`
- sha256: `782b95aa0da0dd263baa2953944478dcce8e90d53c78a98ab887ffb48a7a333c`
- integration target: `quality/counters/c2-r69-guard-dominance.py` (L1 action; this seat wrote no production path)
- tooling installed: none (no pacman transaction, no uv/npx/binary install)

**Provenance note.** `quality/counters/c2-r69-guard-dominance.py` already exists untracked in the lane
worktree; it is **not** this seat's artifact and was never written or modified here. Its sha256 moved while
this seat worked (`b6bcec07…` at R69RevC2's first attack, `85f9e60a…` when checked at 22:56), so running
the frozen command from the lane root executes a foreign file, not this draft.

## Contract result at the frozen base rev

```
MADO_R69_GUARD_DOMINANCE: population=20 readers=13 guarded=13 unguarded=0 controls=11/11 base_controls=7/11 verdict=TARGET_MET rev=04093b83f73a841117d3b31dbb2a6063f4f2a454
```

rc 0 — population/readers/guarded/unguarded/controls/base_controls all at the frozen target.

## Commands, exit codes, observed output

All commands ran with `env -i PATH=/usr/bin:/bin HOME="$HOME" LC_ALL=C`; scratch under
`/fast/scratch/hyaku/mado-r69/R69ExecDominance/` (removed; see end).

a) selftest — rc 0

```
python3 <draft> --selftest --scratch-root <scratch>/st
MADO_R69_GUARD_DOMINANCE_SELFTEST: 60/60 assertions passed
# rc 0
```

The same file copied to a fixture's `quality/counters/c2-r69-guard-dominance.py` and run from there gave
`60/60 assertions passed`, rc 0.

b) before state at the base rev — the counter does not exist

```
git -C <lane> cat-file -e 04093b83f73a841117d3b31dbb2a6063f4f2a454:quality/counters/c2-r69-guard-dominance.py
fatal: path 'quality/counters/c2-r69-guard-dominance.py' exists on disk, but not in '04093b83...'
# rc 128

# faithful base checkout for that path: git archive 04093b83 -- quality/counters (0 c2-r69 files), then
python3 quality/counters/c2-r69-guard-dominance.py --repo . --rev HEAD --base-rev 04093b83... \
  --controls <frozen> --scratch-root <scratch>/bt
python3: can't open file '.../basetree/quality/counters/c2-r69-guard-dominance.py':
[Errno 2] No such file or directory
# rc 2
```

The draft itself reads the frozen base correctly: `--repo <lane> --rev 04093b83 --base-rev 04093b83`
prints the target line and rc 0 (the counter is external to the measured tree; only the file's absence at
base is the before state).

c) scratch fixture (git init in scratch, `git rev-parse --show-toplevel` asserted equal to the fixture,
explicit `-c user.name=R69ExecDominance -c user.email=r69@example.invalid` on every commit)

- base commit `2813cfe498b11812e1cba289128a885a6caf7158`: the 20 `quality/check-*.py` blobs at base,
  `quality/counters/c2-r68-reader-guard.py` at base, and the frozen control JSON.
- tip commit `20597873feae576b5d5fed99663ea9f6a428ee87`: adds the draft counter.
- `git fetch <lane> HEAD` brought the real base commit object into the fixture (rc 0;
  `cat-file -e 04093b83^{commit}` rc 0), so `--base-rev` stayed **literal**.

```
cd <fixture> && python3 quality/counters/c2-r69-guard-dominance.py \
  --repo . --rev HEAD --base-rev 04093b83f73a841117d3b31dbb2a6063f4f2a454 \
  --controls .ufo/waves/round-69/controls/c2-controls-r69.json --scratch-root <scratch>/run2
# 20 MADO_R69_GUARD rows
MADO_R69_GUARD_DOMINANCE: population=20 readers=13 guarded=13 unguarded=0 controls=11/11 base_controls=7/11 verdict=TARGET_MET rev=20597873feae576b5d5fed99663ea9f6a428ee87
# rc 0
```

Negative denominators (same draft bytes):

- fixture with 19 check files (dropped `quality/check-wave-done.py`), tip `2fad9d01…`:
  `population=19 readers=12 guarded=12 unguarded=0 controls=11/11 base_controls=7/11 verdict=TARGET_MISSED`,
  rc 1.
- truncated control file (`head -c 200`): `setup error: controls file sha256 c442bae8... does not match
  the frozen digest`, rc 2.
- `--scratch-root /tmp/x`: `unsafe scratch root (tmp-family): /tmp/x`, rc 2.

d) census at the base rev (every one of the 20 files; the L1 can commit this table as the receipt)

```
file reader=yes guard=yes   quality/check-anchor-cover.py
file reader=yes guard=yes   quality/check-axis-scores.py
file reader=yes guard=yes   quality/check-control-receipts.py
file reader=no  guard=no    quality/check-counter-discrimination.py
file reader=yes guard=yes   quality/check-deliverables.py
file reader=yes guard=yes   quality/check-evidence-pointers.py
file reader=yes guard=yes   quality/check-freeze-order.py
file reader=yes guard=yes   quality/check-index-rows.py
file reader=yes guard=yes   quality/check-index.py
file reader=yes guard=yes   quality/check-landed-contract.py
file reader=no  guard=no    quality/check-locators.py
file reader=no  guard=no    quality/check-population.py
file reader=no  guard=no    quality/check-r38-discrimination.py
file reader=no  guard=no    quality/check-r55-controls.py
file reader=no  guard=no    quality/check-r56-controls.py
file reader=yes guard=yes   quality/check-round-outcome-first.py
file reader=yes guard=yes   quality/check-session-material.py
file reader=no  guard=no    quality/check-state-cite.py
file reader=yes guard=yes   quality/check-tool-ledger.py
file reader=yes guard=yes   quality/check-wave-done.py
```

(verbatim machine rows: `MADO_R69_GUARD file=<path> reader=<yes|no> guard=<yes|no>`)

## What the counter implements

- Population: tracked `quality/check-[^/]+\.py` at `--rev`, read from git objects through a scrubbed
  `GIT_*` env; reader = r68 rule (git token + frozen object-read verb), unchanged.
- Key position: dict-literal key, `**` spread of a mapping literal (`{**{KEY:"1"}}`, `dict(**{KEY:"1"})`),
  `env[KEY] = ...`, `update`/`setdefault(KEY=...)`, `dict(KEY=...)`. Value-position strings don't count.
  Multi-target assignments (`env = other = {KEY: "1"}`) credit every env-named target.
- Dominance, one module: (a) inline `env=<guarded mapping|producer call>` at a git call; (b) env-named
  name bound to a guarded mapping or producer, used as `env=` with no intervening plain rebinding to a
  mapping without the key (subscript mutations don't rebind; a multi-target rebinding does); (c) guarded
  name passed at the parameter position of a local function whose env-named parameter reaches `env=` at a
  git call — and that parameter must not be rebound to an unguarded mapping before the call.
- Literal-false `if`/`while` bodies are dead; the `else` arm is live. Nested scopes are separate: a
  sibling function's binding cannot dominate, while a free-variable (closure) use still does; a use is
  shadowed by a local binding/parameter on the path from the guard scope.
- Producer validity is path-conservative: **every** non-dead `return` of the function must hand back a
  key-carrying mapping, and the last plain rebinding before each such return must itself carry the key or
  a guarded construction must follow it. Direct `return {KEY: "1"}` is a producer; an unguarded return
  before (or after) a guarded one is not.
- Controls: exact sha256 `975ca3ba...f90b9`, exactly 11 cases, strict types, validated before any scan;
  a case scores only when reader and guard both match. Base leg extracts
  `quality/counters/c2-r68-reader-guard.py` at `--base-rev` into scratch, imports it, and scores the same
  cases (7/11 observed).
- Exits: 0 on the full frozen target, 1 otherwise, 2 on usage/setup (repo, revs, controls digest/count/
  shape, base counter absent/unimportable, scratch refusals, contract self-check).

## Reviewer attacks (R69RevC2 shapes) against these bytes

```
dead-inline (True,False)          producer-overwrite (True,False)     producer-late (True,False)
sibling-scope (True,False)        nested-key-value (True,False)       onehop-wrong-parameter (True,False)
multitarget-rebind (True,False)   param-rebind (True,False)           unreachable-return (True,False)
dead-else-valid (True,True)       producer-direct (True,True)         closure-env (True,True)
splat-env literal (True,True)     filtered-conditional (True,True)
attribute-env / alias-env / late-guard / except-other-env / cross-module (True,False)
name-keyed subscript (True,False)
```

The prototype's six false positives (dead inline, producer overwrite, producer return ordering, sibling
scope, nested mapping value, wrong one-hop parameter) and its `dead-else-valid` false negative are closed;
the three follow-up false positives (multi-target rebinding, callee-parameter rebinding, unreachable
guarded return) are closed as well. `closure-env`, literal `splat-env` and non-literal conditional guards
stay accepted — they are not excluded by the frozen sentence.

## Bounds and risks (declared, not defects)

- `env[KEY_NAME]` where a constant name holds the string, `self.env[i]`, aliases and container flows stay
  false negatives: the freeze's "Not claimed" excludes alias/attribute/container flow.
- A guard under a non-literal condition (`if enabled:`) is accepted: the freeze excludes only literal-false
  branches; no further path sensitivity is claimed.
- The base leg requires the `--base-rev` commit to be present in `--repo`. The freeze's command hard-codes
  `04093b83...`; the lane has it, a scratch fixture only with an explicit fetch (proved above).
- Importing the extracted r68 counter leaves a `__pycache__` inside the caller-declared scratch root; all
  writes stay under it.

## Scratch

`/fast/scratch/hyaku/mado-r69/R69ExecDominance/` was created, used for every fixture/run above, and removed
(`SCRATCH_PRESENT=no`). Seat-local `__pycache__` created by `py_compile` was removed; the draft sha256 is
unchanged after cleanup.
