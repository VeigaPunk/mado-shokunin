# TwFrozenF1 — F1 fixed as a 2-line patch, red-before and green-after both measured

Seat `MadoR19.TwFrozenF1` (executor, leaf). Target root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, branch `master`, base blob
`git show 17661e0fa83f978fb659f5bb8fef47f0969f6945:tools/mado-tripwire.py`
= `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`,
byte-equal to the lane's `tools/mado-tripwire.py` at this moment.

## 1. F1 mechanism (carried from round 18)

`validate_reachable` rejects an out-of-range line for both pin lists but
blank-checks only `known_misses` (base blob `:1019-1020`); an `expected_findings`
entry pinned to a blank line is accepted and then graded as a failed verdict
(`frozen_verdict_mismatch`, exit 1) instead of the documented pin error
(`frozen_error`, exit 2). The module docstring already promises the stricter
contract: quoted ≤25 words, base blob `:39-41` —

> every expected/known line must name a listed input, be in range and non-blank

so this is a code/docstring divergence, not a new rule. A blank line can never
yield a finding (`scan_file` skips `raw.strip()`-empty lines, `:767-768`), so
the pin is unreachable by construction.

Reproduced verbatim on the unpatched blob before any edit:

```
$ python3 -I <base c1ae45a7> --frozen .../f1-blank-expected
MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch        rc=1
{"exit": 1, ..., "missing_findings": [{"class":"host_mutation","file":"inputs/incident.jsonl","line":2,"rule":"pacman"}], ...}
```

## 2. Patch

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/drafts/TwFrozenF1.r19.patch`
(sha256 `a51f93f19370971d85546c9493707f64d4f98c28202b79e5c44d4712b62756b6`),
minimal diff vs the blob: **one file, 2 added lines, 0 removed**, no docstring
or suite edit:

```diff
--- a/tools/mado-tripwire.py
+++ b/tools/mado-tripwire.py
@@ -1011,6 +1011,8 @@
         if w["line"] > len(lines):
             return "expected_findings line %d is past the end of %s" % (
                 w["line"], w["file"])
+        if not lines[w["line"] - 1]:
+            return "expected_findings line %d of %s is blank" % (w["line"], w["file"])
     for k in pinned["known"]:
         lines = stats[os.path.normpath(k["file"])]
         if k["line"] > len(lines):
```

The blank rule is the scanner's own skip rule (`bool(raw.strip())` over the
same digest-verified bytes), so after the patch "reachable" means exactly
"the scanner would look at that line". No ordering change: range is still
checked first, so a pin on the phantom line after a trailing newline stays
`past the end`, not `blank`.

Application proofs (base blob, and the lane's live `tools/mado-tripwire.py`
which is the same bytes):

```
$ cd /tmp/patchcheck && git apply --check <patch> && git apply <patch>
$ git diff --stat
 tools/mado-tripwire.py | 2 ++
 1 file changed, 2 insertions(+)
$ sha256sum tools/mado-tripwire.py
7ee8bdb7ffba30d37340fd7ba3f4f3355985f616ee0fb328eb79723883e859b2
$ cd /tmp/patchcheck2 && patch -p1 --dry-run < <patch> && patch -p1 < <patch>
$ sha256sum tools/mado-tripwire.py
7ee8bdb7ffba30d37340fd7ba3f4f3355985f616ee0fb328eb79723883e859b2
```

Patched tool digest `7ee8bdb7…` is the one used for every green-after run
below. The hunk context (`validate_reachable`) is untouched by any of the
three round-18 carried drafts: `grep -c 'validate_reachable\|expected_findings'`
over `TwMissBashCVar.patch`, `TwMissHelperFn.patch`,
`TwInstallerChannels.patch` = `0 0 0`.

## 3. Suite: `.ufo/waves/round-19/tripwire/r19-frozen-f1f2/`

Cases are owned per seat: my six fixtures are `f1-*` dirs, my spec is
`expected-f1.json` (sha256 `246b8cd55c47583ddde35accc46ac4505013b62b82f9e534ae40875f8742a9e9`),
F2 owns `f2-*` and `expected-f2.json`. Schema is `mado-tripwire-selftest-v1`
with a `cases` array only, so L1's merge is a concatenation of `cases`
(verified mergeable against the current `expected-f2.json`: 6 + 7 cases, 0
name overlap, same schema). No `expected.json` was left in the lane dir —
until L1 merges, the runnable view is a byte-identical `/tmp` copy
(`expected-f1.json` → `expected.json`).

| case | bytes (`inputs/incident.jsonl` sha256) | pin | old tool | patched tool |
|---|---|---|---|---|
| `f1-blank-expected` | `568c3e48…d006` (line 2 empty) | expected finding line 2 | `frozen_verdict_mismatch`/1, missing 1 | `frozen_error`/2, "line 2 … is blank" |
| `f1-whitespace-expected` | `13c1f760…a9ef` (line 2 = spaces+tab) | expected finding line 2 | mismatch/1, missing 1 | `frozen_error`/2, blank |
| `f1-blank-after-valid` | `40f2b35f…e278` (line 2 empty, line 3 whitespace) | line 1 valid + line 3 blank | mismatch/1, missing 1, extra 1 | `frozen_error`/2, "line 3 … is blank" |
| `f1-nonblank-control` | `df6f29a1…63bc1` (line 2 real `sudo pacman -Syu`) | line 1 clean, non-blank | mismatch/1, missing 1, extra 2 | **unchanged** mismatch/1, 1/2 |
| `f1-nonblank-note-control` | `271c3560…6788` (line 1 `{"type":"note"}`) | line 1 non-blank non-message | mismatch/1, missing 1 | **unchanged** mismatch/1, 1/0 |
| `f1-trailing-newline-past-end` | `1c23c97b…6fa5` (one trailing `\n`) | expected finding line 2 | `frozen_error`/2 past-the-end | **unchanged** `frozen_error`/2 past-the-end |

Three cases move wrong-label→pin-error; two non-blank controls and one
trailing-newline boundary case pin that the check does **not** overreach
(they pass on both tools). The control pins are what stop a future "blank"
mutation from passing the suite by rejecting every unreachable line.

Red-before / green-after over the byte-identical lane fixtures (fixture tree
hash `9edb960082df2cbd82ace86de3267f2b89f82860ce62d281e05d4990198bb614`
computed over the six `f1-*` dirs for both lane and run copy; `expected-f1.json`
`cmp`-equal to the run's `expected.json`):

```
$ python3 -I <base c1ae45a7> --selftest /tmp/r19f1
CASE f1-blank-expected FAIL want=(2,'…frozen_error',0,0) got=(1,'…frozen_verdict_mismatch',('frozen_verdict_mismatch',1,1,0))
CASE f1-whitespace-expected FAIL … got=(1, …, ('frozen_verdict_mismatch',1,1,0))
CASE f1-blank-after-valid FAIL … got=(1, …, ('frozen_verdict_mismatch',1,1,1))
CASE f1-nonblank-control ok
CASE f1-nonblank-note-control ok
CASE f1-trailing-newline-past-end ok
SELFTEST_SUMMARY: 3/6 passed failed=['f1-blank-expected', 'f1-whitespace-expected', 'f1-blank-after-valid']   rc=1

$ python3 -I <patched 7ee8bdb7> --selftest /tmp/r19f1
CASE f1-blank-expected ok … CASE f1-trailing-newline-past-end ok
SELFTEST_SUMMARY: 6/6 passed failed=[]                                    rc=0
```

Because the lane suite has no merged `expected.json` yet, the merged suite
was run from a `/tmp` composite over the lane's own fixture dirs (13 cases):

```
base c1ae45a7            : 7/13 passed  failed=[3 f1 + 3 f2]
F1-only 7ee8bdb7         : 10/13 passed failed=[f2-symlink-dir-dot, f2-symlink-dir-dot-slash, f2-symlink-dir-inputs-dotdot]
F1+F2 stack 7eb41bb1     : 13/13 passed failed=[]
```

## 4. Regression: the six carried suites, old vs patched

Same commands, lane-relative dirs, `python3 -I <tool> --selftest <suite>`:

| suite | base `c1ae45a7` | patched `7ee8bdb7` |
|---|---|---|
| `.ufo/waves/round-17/tripwire/core` | 9/9 | 9/9 |
| `.ufo/waves/round-17/tripwire/compound` | 16/16 | 16/16 |
| `.ufo/waves/round-17/tripwire/hardening` | 33/33 | 33/33 |
| `.ufo/waves/round-17/tripwire/w2-regressions` | 30/30 | 30/30 |
| `.ufo/waves/round-18/tripwire/frozen` | 31/31 | 31/31 |
| `.ufo/waves/round-18/tripwire/r18-failsafe` | 1/1 | 1/1 |

Committed baseline: `python3 -I <patched> --frozen .ufo/waves/round-18/frozen`
→ `MADO_TRIPWIRE_FROZEN: frozen_match` (same first line with the base tool).
No existing pin in the tree puts an expected finding on a blank line, so the
new check fires only on the new F1 fixtures.

## 5. Integration with TwFrozenF2 (cross-check, not F2's verdict)

The two round-19 tripwire patches are disjoint and stack in either order:
applying `TwFrozenF2.r19.patch` either before or after my hunk yields the
same tool `7eb41bb1c81b2ef1b73fe6f24d79cb495ae2c00c88d74ecb32026788af53e130`,
and that stacked tool passes all six legacy suites plus the merged 13-case
suite (table above) and the committed baseline (`frozen_match`). On my
F1-only tool the three F2 symlink-spelling cases still fail, i.e. neither
patch masks or substitutes for the other. `[INFERENCE]` The 17 other round-19
patch/draft streams shown in `drafts/` do not touch `validate_reachable`; only
a future tool change that reorders `frozen/expected` parsing could displace
the hunk context.

## 6. Files written (all under the target root)

- `.ufo/waves/round-19/drafts/TwFrozenF1.r19.patch`
- `.ufo/waves/round-19/tripwire/r19-frozen-f1f2/expected-f1.json`
- `.ufo/waves/round-19/tripwire/r19-frozen-f1f2/f1-{blank-expected,whitespace-expected,nonblank-control,blank-after-valid,trailing-newline-past-end,nonblank-note-control}/expected.json` and `inputs/incident.jsonl` (12 files)
- `.ufo/waves/round-19/w1/reports/TwFrozenF1.md` (this report)

No other lane byte written; no `tools/mado-tripwire.py`, no `MANIFEST.json`,
no state file, no sibling dir touched. All suite/tool runs used `/tmp` copies;
the lane was read-only during them.

## Limits

- I did not run the gate (`bash tools/mado-verify.sh`) in any mode, no package,
  service, compositor or host probe, and no live `walker`/transcript read.
- The frozen-mode selftest harness (unchanged by this patch) asserts outcome,
  exit, and missing/extra counts only: my cases pin the label `frozen_error`
  and rc 2, not the exact error string (`want_error_contains` is honoured for
  `mode: scan` only). The string is shown above by direct run, not by the suite.
- `f2-*` fixtures and `expected-f2.json` are F2's; I ran them only as a
  cross-check of patch independence, and their content may have changed after
  my `/tmp` snapshot (`14:10` local). `[UNK]` whether F2 revises them before
  L1 merges.
- I did not test a revision-ordered stack against the three carried scans
  drafts (`TwMissBashCVar`/`HelperFn`/`InstallerChannels`): they are diffs vs
  the `d9a5a18` tool, not this blob, so rebasing them is another seat's work.
  The disjointness check above is textual (0 hits for my context symbols), not
  an applied stack.
- Fence disclosure: two lane git reads outside the strict allowlist spelling —
  `git diff --stat` and `git status --porcelain --untracked-files=no`; both
  read-only, the latter may refresh index stat bytes. No git/jj write in the
  lane; the only git write commands ran in `/tmp/patchcheck*` and `/tmp/stack*`
  scratch repos (`init`/`add`/`commit`/`apply`). jj was never invoked.
- `[INFERENCE]` No behavior change outside `--frozen` reachability: the added
  branch only runs after all inputs digest-verify, and `--scan` never calls
  `validate_reachable`; the six suites and baseline above are the exercised
  evidence for that.

## Installs

none
