# Round 18 — final tripwire review (non-author, W3)

Seat: `MadoR18.W3TripwireFinal`. Target commit
`a210241b5429fb3c3f9ad23f42863d6e6d9e5845` (branch master), scope
`git diff abfbf35 a210241 -- tools/mado-tripwire.py .ufo/waves/round-18/tripwire/`.
Read-only review in a `/tmp` clone; no lane write except this report; no jj,
no package/service/compositor command, no gate live run. No tool installs.

Clone identity:

```
$ git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/w3tf-final
$ cd /tmp/w3tf-final && git checkout -q a210241b5429fb3c3f9ad23f42863d6e6d9e5845
$ git rev-parse HEAD
a210241b5429fb3c3f9ad23f42863d6e6d9e5845
$ git status --porcelain | wc -l
0
```

Fence disclosure: in my first tool batch, concurrently with reading the
round-18 lesson's M5 entry, I ran one `git status --porcelain` **in the lane**
to check for a dirty worktree. It printed no entries. Like the M5 seat, this
verb is outside the read-only allowlist (`show/log/diff/ls-tree/rev-parse/
merge-base/cat-file`) and may refresh the index stat cache; no tracked
worktree byte changed. Every other lane git read was `log`, `rev-parse`,
`diff` or `show`; all suite and probe executions ran in the `/tmp/w3tf-final`
clone and `/tmp` fixtures, and this report is the only lane write.

Tool digests (sha256 of the tool file at each rev):

| rev | tool sha256 |
|---|---|
| `d9a5a18` (pre-C3) | `962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072` |
| `4c103b5` / `abfbf35` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` |
| `a210241` (final) | `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd` |

`git diff --stat abfbf35 a210241 -- tools/mado-tripwire.py .ufo/waves/round-18/tripwire/`
= 35 files, +727 −84. `git diff --stat be886a3 a210241 -- <same paths>` = empty
(the final commit changes only receipts/docs/SCORECARD/LOG for this scope), so
the tool and suite at `a210241` are the wave-2 bytes.

## 1. Behaviour changes in the diff

`tools/mado-tripwire.py` has 19 hunks. Enumerated:

### Scan

1. **`classify_pacman` unknown-operator default** (`:414-418`). Previously
   `op is None` returned `package_query` for `pacman` (and `host_mutation` only
   for `yay`/`paru`); now it returns `host_mutation` for every argv0. The rule
   string is still the argv0 (`pacman`, `yay`, `paru`). This is the stated
   failsafe: an operator the parser cannot read (variable op, `$'...'`-quoted
   op, typo, bare invocation) can no longer land in a permitted class.
2. **`scan(paths)`** drops the `permit` parameter (the unpermitted count moved
   out); a new **`verdict_of(findings, permit)`** (`:832`) is the one authority
   for the scan verdict, used by both `run_scan` and `run_frozen`. The formula
   is unchanged (`exit 1` iff an unpermitted finding; `clean` iff no findings,
   else `findings` iff unpermitted, else `permitted_only`), so `--scan` output
   is unchanged except for (1).

### Frozen validation (`--frozen`)

3. **Symlinked frozen directory** (`:1101-1104`): `--frozen DIR` with `DIR` a
   symlink is rejected up front as `snapshot_tampered` ("frozen directory is a
   symlink").
4. **Duplicate JSON keys** (`:907-915`, used at `:1113`): `expected.json` is
   parsed with `object_pairs_hook=unique_pairs`; any repeated key at any object
   depth raises `ValueError` → `frozen_error` exit 2 (no last-wins).
5. **Unknown top-level keys**: `set(spec) - FROZEN_KEYS` → `frozen_error`
   (e.g. `unknown expected.json key(s): known_mises`).
6. **Input shape**: `inputs` must now be a non-empty list; every path must
   `fullmatch` `inputs/[A-Za-z0-9._-]+\.jsonl` (`:866`) — absolutes and
   traversals become `frozen_error`; duplicate input paths (normpath) are a
   baseline error. `git diff` note: the old code reported absolute/traversal
   paths as `snapshot_tampered`; they are now rejected earlier as
   `frozen_error` (exit 2 both ways). The suite's `absolute-input` and
   `path-traversal` cases were re-pinned from `want_label snapshot_tampered` to
   `frozen_error`, and the red-before receipt shows the `abfbf35` tool's old
   `snapshot_tampered` label on both.
7. **Pinned-line shape** (`validate_frozen`, `:917-1000`): unknown class in
   `expected_findings`; `expected_findings`/`known_misses` must name a listed
   input; the exit/label pair must be reachable (`FROZEN_PAIRS`:
   `(0,clean)`, `(0,permitted_only)`, `(1,findings)`); label/finding
   consistency (`clean` cannot list findings; `permitted_only` must list only
   permit classes; `findings` must list at least one non-permit class); a
   `known_misses`/`expected_findings` overlap on the same `(file,line)` is a
   baseline error.
8. **Containment** (`frozen_snapshot`, `:1024-1100`): the old lexical
   absolute/`..` test is replaced by `realpath` containment inside
   `realpath(DIR)` plus an `lstat` non-symlink regular-file requirement; a
   symlinked `DIR/inputs` sets every listed path bad and returns
   `snapshot_tampered`; unlisted `*.jsonl` still returns `snapshot_tampered`.
9. **Per-line stats**: verified inputs yield per-line non-blank flags from the
   same bytes that matched the pin; `frozen_snapshot` now returns
   `(outcome, report, stats)`.
10. **`validate_reachable`** (new, `:1002-1021`): `expected_findings` line must
    be within the file's line count; `known_misses` line must be within range
    **and non-blank**. Called after digest verification and before replay, so
    an unreachable pin is reported as `frozen_error`.
11. **Known-miss handling**: the old loop that forced a finding on a
    `known_misses` line into `extra_findings` is removed. With overlap now
    rejected in shape validation, a violated known-miss line is naturally an
    `extra` (key includes file+line), so counters are unchanged for valid
    pins (verified by `known-miss-violated`, `swapped-missing-extra`).
12. **Selftest harness, frozen mode** (`:1182-1235`): a `mode: "frozen"` case
    must have a string `want_label` and integer `want_missing`/`want_extra`
    (default 0); the harness now parses the verdict JSON and pins the schema
    `mado-tripwire-frozen-verdict-v1`, `outcome == want_label`,
    `exit == want_exit`, and the exact `len(missing_findings)` /
    `len(extra_findings)`. Previously only exit status and line 1 were checked.
13. Docstring updated to state the above; no other logic change in the file.

### Suite `.ufo/waves/round-18/tripwire/`

- Frozen suite 17 → 31 cases; all 17 pre-existing case names are retained
  (`git show abfbf35:…/expected.json` names ⊆ new names; names removed: none).
  New cases: `contradictory-exit-label`, `duplicate-input-path`,
  `duplicate-json-key`, `expected-unlisted-file`, `known-miss-blank`,
  `known-miss-unreachable`, `label-clean-with-findings`,
  `swapped-missing-extra`, `symlinked-frozen-dir` (+ `-target`),
  `symlinked-inputs-dir`, `unknown-class`, `unknown-key`, `unreachable-line`.
  `known-miss-violated` was re-cut because the old fixture put a
  `known_misses` entry on a line that also appeared in `expected_findings` —
  the exact overlap the new validator rejects as a baseline error. It now
  expects two line-1 findings and pins a *different* line-2 finding as the
  known miss, so a violation is a natural `extra` (`want_extra 1`).
  `verdict-exit-label`'s inner spec changed from a contradictory pin
  (`clean` + two findings, which is now the separate `label-clean-with-findings`
  case → `frozen_error`) to a valid clean pin with no findings over an input
  that produces two, so it is a verdict mismatch with `want_missing 0` /
  `want_extra 2`. `verdict-missing-finding`, `verdict-extra-finding` and
  `known-miss-violated` gained `want_missing`/`want_extra` assertions.
   
  The r18 failsafe case is the only new scan-suite assertion beyond the frozen
  suite.
- New `r18-failsafe/`: one case, `pacman -$o wlroots`, `--permit
  package_query`, `want_exit 1`, `want_findings` `host_mutation/pacman` line 1
  (the stated failsafe).

## 2. Required runs (exact commands, outputs)

All in `/tmp/w3tf-final`, tool `c1ae45a7…` at `a210241`:

```
python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/core
SELFTEST_SUMMARY: 9/9 passed failed=[]                                    rc=0
python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/compound
SELFTEST_SUMMARY: 16/16 passed failed=[]                                  rc=0
python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/hardening
SELFTEST_SUMMARY: 33/33 passed failed=[]                                  rc=0
python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/w2-regressions
SELFTEST_SUMMARY: 30/30 passed failed=[]                                  rc=0
python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-18/tripwire/frozen
SELFTEST_SUMMARY: 31/31 passed failed=[]                                  rc=0
python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-18/tripwire/r18-failsafe
SELFTEST_SUMMARY: 1/1 passed failed=[]                                    rc=0
python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen
MADO_TRIPWIRE_FROZEN: frozen_match                                        rc=0
```

`--frozen` verdict body: `expected_sha256 4f3534ae33d8daba…` (independently
`sha256sum .ufo/waves/round-18/frozen/expected.json` = same), five inputs all
`ok: true`, `missing_findings []`, `extra_findings []`, `tool_sha256
c1ae45a7…`.

Independence check of the 31/31 claim: I re-implemented the suite assertions
in an external script (run each case dir through `--frozen`, compare
`(exit, line-1 label, outcome, exit field, len(missing), len(extra))` against
the case's `want_*`): **31 ok, 0 fail**.

Provenance (supports C3's "provenance match"):

```
python3 -I .ufo/waves/round-18/frozen-provenance-check.py
MADO_FROZEN_PROVENANCE: match                                             rc=0
```
(228 indexed sources; all 5 input pairs byte-equal to their transcript lines.)

Exact final receipts reproduced (not just compared):

```
python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen
# lines 2-3 == .ufo/waves/round-18/evidence/final/tripwire-frozen-match.txt lines 2-3 (True/True)
# tamper copy + append one byte to inputs/r15-libinput-events.jsonl
python3 -I tools/mado-tripwire.py --frozen <copy>
# MADO_TRIPWIRE_FROZEN: snapshot_tampered, rc=2
# lines 2-3 == .../tripwire-frozen-tampered.txt lines 2-3 (True/True)
```

Pre-state receipt `evidence/tripwire-frozen-before.txt` also reproduces with
the `d9a5a18` tool (`sha256 962919ce…`): usage line, `could_not_evaluate`,
exit 2.

## 3. Red-before receipt vs the `abfbf35` tool on the `a210241` suite

```
git show abfbf35:tools/mado-tripwire.py > /tmp/w3tf-abfbf35-tool.py
sha256sum /tmp/w3tf-abfbf35-tool.py
c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb
python3 -I /tmp/w3tf-abfbf35-tool.py --selftest .ufo/waves/round-18/tripwire/frozen
SELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb
SELFTEST_SUMMARY: 17/31 passed failed=['symlinked-inputs-dir', 'path-traversal',
 'absolute-input', 'unreachable-line', 'contradictory-exit-label',
 'label-clean-with-findings', 'unknown-class', 'known-miss-blank',
 'known-miss-unreachable', 'expected-unlisted-file', 'duplicate-input-path',
 'unknown-key', 'duplicate-json-key', 'symlinked-frozen-dir']
rc=1
```

Receipt match: comparing the receipt body (all lines except the `RECEIPT`
header and the final `exit=1`) to this run gives **33 body lines, 0
mismatches**; the embedded `SELFTEST_SCRIPT_SHA256` is the `abfbf35` tool
digest. Suite identity: `git diff --stat be886a3 a210241 --
.ufo/waves/round-18/tripwire/frozen` is empty, so the suite bytes named in the
receipt ("suite bytes at `be886a3`") are exactly the `a210241` bytes; a
content tree hash over the sorted per-file sha256 values plus symlink targets
is `d1ca00c2bcf3313e7b0421793b7a40c8fbdd9d030104a50ddb2fa8a6fdb0f05b`. The
receipt was added at `a210241` with `measured_commit=abfbf35…` and
`tool_sha256=c87a31ef…`, both independently verified.

Caveat on reading the number: the `abfbf35` harness checked only exit status
and line 1, not `want_missing`/`want_extra`, so `17/31` is a label/exit
measure. The 14 failures are the 12 new validation/symlink cases plus the two
re-pinned path cases (`absolute-input`, `path-traversal`, whose expected label
changed from `snapshot_tampered` to `frozen_error`). That matches the
scorecard's wording ("the abfbf35 tool fails 14/31").

## 4. Scan-classification differential

Method: extract the `abfbf35` tool to `/tmp`; render the same JSONL through
both tools; compare the full `findings` multiset `(file, line, class, rule)`.
Two corpora: (a) 56 hand-built pacman/yay/paru invocations, one per file;
(b) every committed `*.jsonl` (242 files) scanned per-file. Per-file exit
distribution is identical between the tools with no `--permit`:
`{(1,1): 94, (0,0): 95, (2,2): 53}` — zero return-code differences. The 53
exit-2 files are deliberate refusals present under both tools
(`core/malformed.jsonl`, `hardening/agent.db.jsonl` by name,
`hardening/symlink-target.jsonl` and `frozen/symlink-input/inputs/link.jsonl`
by symlink, and the `fetch/*/receipts.jsonl` files whose records are not
transcripts: "unknown record shape"); both tools report the same refusal with
zero findings, so every real transcript fixture was compared. With `--permit
package_query`, exactly 3 committed files flip exit `0 → 1` — the failsafe
working as intended: `drafts/.../sh-fn-positional-n`,
`drafts/.../sh-fn-single-quoted`, `r18-failsafe/unparsed-operator` (the other
two class-changed files already carried a `sudo` host_mutation, so their exit
was 1 before and after). The failsafe suite is genuinely red-before: the
`abfbf35` tool scores `0/1` on `.ufo/waves/round-18/tripwire/r18-failsafe`
(`want 1`, got `0`) while it still scores the four round-17 suites identically
(`9/9`, `16/16`, `33/33`, `30/30`), so the new suite isolates the change.

- (a) 61 findings on each side; **9 files differ**, every one
  `package_query → host_mutation`, rule `pacman`:
  bare `pacman`; `pacman --help`; `pacman -h`; `pacman --typo`;
  `pacman -$o wlroots`; `pacman -z foo`; `pacman -y`;
  `sudo pacman`; `sudo pacman --typo`.
- (b) **5 files differ**, every one `package_query → host_mutation`, rule
  `pacman`:
  `.ufo/waves/round-17/w2/adversarial/{dollar-quote-op,var-op-install}.jsonl`
  (`sudo pacman $'-S' wlroots`; `o=S; sudo pacman -$o wlroots`),
  `.ufo/waves/round-18/drafts/tripwire/r18-helperfn/{sh-fn-positional-n,
  sh-fn-single-quoted}.jsonl` (`pacman "$1" wayland`; `sh -c 'pacman $1'`),
  `.ufo/waves/round-18/tripwire/r18-failsafe/unparsed-operator.jsonl`.
- Minimal exact repro of the one class flip (any changed fixture works):

```
$ printf '%s\n' '{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","name":"bash","arguments":{"command":"pacman -$o wlroots"}}]}}' > /tmp/one.jsonl
$ python3 -I /tmp/w3tf-abfbf35-tool.py --scan /tmp/one.jsonl | sed -n 2p \
    | python3 -c 'import json,sys; v=json.load(sys.stdin); print("counts", {k:v["counts"][k] for k in ("host_mutation","package_query")}, "findings", [(f["class"],f["rule"]) for f in v["findings"]])'
counts {'host_mutation': 0, 'package_query': 1} findings [('package_query', 'pacman')]
$ python3 -I tools/mado-tripwire.py --scan /tmp/one.jsonl | sed -n 2p \
    | python3 -c 'import json,sys; v=json.load(sys.stdin); print("counts", {k:v["counts"][k] for k in ("host_mutation","package_query")}, "findings", [(f["class"],f["rule"]) for f in v["findings"]])'
counts {'host_mutation': 1, 'package_query': 0} findings [('host_mutation', 'pacman')]
```

- No flip in the other direction; no other class or rule changed anywhere in
  either corpus. Genuine query forms stay `package_query`:
  `-Q`, `-Qq`, `-Qi`, `-Qdtq`, `-Qo`, `-Qs`, `-Si`, `-Ss`, `-Sl`, `-Sp`,
  `-Ssq`, `-Fl`, `-F`, `-T`, `-V`, `--query`, `--version`; mutations stay
  `host_mutation`: `-S`, `-Syu`, `-Syyu`, `-Sy`, `-Sw`, `-Sc`, `-U`, `-R`,
  `-D`, `-Fy`, `-S --needed`. `yay`/`paru` are unchanged (they already
  returned `host_mutation` on an unreadable operator).
- Frozen baseline unaffected: the `abfbf35` tool also returns `frozen_match`
  on `.ufo/waves/round-18/frozen`, and `--scan` over its 5 inputs is
  byte-identical between the two tools (`cmp`). `recut-summary.json` at
  `be886a3` reports `all_counts_identical: true`, `all_receipts_identical:
  true`, consistent with this.

**Flag:** no scan-classification change was found outside the stated failsafe.
The one scope nuance is that the flip is broader than "an operator the parser
could not read": it also reclasses operator-absent invocations that are not
mutations (`pacman --help`, `pacman -h`, `pacman -y`) from `package_query` to
`host_mutation`. That direction is fail-safe (over-report, never a query
downgrade) and is exactly what the new comment says ("must never land in a
permitted class"), so I record it as scope, not as an unstated change.

## 5. Findings (severity order)

### F1 — Low: reachability validation does not blank-check `expected_findings`

`validate_reachable` (`:1002-1021`) rejects an out-of-range line for both
lists, but tests `if not lines[k["line"] - 1]` **only** for `known_misses`
(`:1019`); an `expected_findings` entry pinned to a blank line is accepted as
a valid baseline. A blank line cannot yield a finding, so such a pin is
unreachable by construction.

Repro (copy-free, `/tmp`):

```
# /tmp/w3tf-probe-frozen/blank-expected/inputs/x.jsonl:
#   line 1 = one clean bash toolCall, line 2 = blank
# expected.json: permit [host_mutation], expected_exit 0,
#   expected_label permitted_only,
#   expected_findings [{file inputs/x.jsonl, line 2, class host_mutation, rule pacman}]
$ python3 -I tools/mado-tripwire.py --frozen /tmp/w3tf-probe-frozen/blank-expected
MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch
{"exit": 1, "outcome": "frozen_verdict_mismatch",
 "missing_findings": [{"file":"inputs/x.jsonl","line":2,...}], ...}
rc=1
```

This contradicts the module docstring added by this commit ("every
expected/known line must ... be in range and non-blank ... an unreachable pin
is `frozen_error`, never a failed verdict") and the SCORECARD phrase
"unreachable pin is frozen_error". Impact is bounded: the case cannot produce
a false `frozen_match` (it fails as 1), so it is a baseline-error
misclassification (exit 1 instead of 2). The suite exercises
`known-miss-blank` but has no expected-finding-on-blank case. Fix: apply the
same blank test to `pinned["findings"]` and add a suite case that fails
before the fix.

### F2 — Low: symlinked-DIR rejection is bypassed by `DIR/.`

`run_frozen` uses `os.path.islink(directory.rstrip("/") or directory)`
(`:1102`) — a lexical test. Path spellings that reach the final component
through `.` defeat it; the target's own `expected.json` and pinned inputs are
self-consistent, so the run reports a match:

```
$ ln -s "<copy of .ufo/waves/round-18/frozen>" /tmp/w3tf-probe-frozen/link
$ for p in .../link .../link/ .../link/. .../link/./; do
    python3 -I tools/mado-tripwire.py --frozen "$p" | head -1; done
MADO_TRIPWIRE_FROZEN: snapshot_tampered   # .../link
MADO_TRIPWIRE_FROZEN: snapshot_tampered   # .../link/
MADO_TRIPWIRE_FROZEN: frozen_match        # .../link/.     rc=0
MADO_TRIPWIRE_FROZEN: frozen_match        # .../link/./    rc=0
```

This defeats the check the suite calls `symlinked-frozen-dir` for a plausible
spelling. The committed gate command uses the canonical path, so current
receipts are unaffected; the inputs are still digest-verified against the
target's `expected.json`, so this is not a false verdict on tampered bytes —
it is a bypass of "the frozen directory itself must not be a symlink".
Fix: normalize the path (`os.path.normpath` before `islink`, or compare
`realpath` with the lexical path) and add the `/.` spelling to the suite.

### F3 — Info: docstring overstates the escaping-path outcome

The docstring groups "a symlinked DIR/inputs, an escaping path, a leaf symlink
or an unlisted `*.jsonl`" as `snapshot_tampered`. Escaping/absolute paths are
rejected earlier by `FROZEN_PATH` (`:866`) and report `frozen_error` — the
`abfbf35` tool reported `snapshot_tampered` for them, and the suite's
`path-traversal`/`absolute-input` expectations were deliberately re-pinned to
`frozen_error`. Exits are both 2, so only the docstring's classification is
stale; the code and suite agree.

### F4 — Info: unknown-key rejection is top-level only

`FROZEN_KEYS` is applied to the spec object only. A nested unknown key in an
inputs entry is silently ignored (probe: `{"path": ..., "sha256": ...,
"extra_field": 1}` → `frozen_match` exit 0); a repeated key at any depth is
rejected (object_pairs_hook). Low risk (required fields are still checked),
but "unknown keys are baseline errors" is true only at the top level.

### F5 — Info: duplicate-key diagnostic loses the key name

`unique_pairs` raises `ValueError("duplicate key %r")`, but `run_frozen`
formats only `type(exc).__name__`, so the user sees
`expected.json not JSON (ValueError)` — indistinguishable from a syntax error
(the `duplicate-json-key` case asserts only label/exit). If diagnostics
matter, catch the duplicate-key case separately or include `str(exc)`.

### F6 — Info (non-gated draft drift)

`.ufo/waves/round-18/drafts/tripwire/r18-helperfn`: 14/24 with the `abfbf35`
tool, **13/24** with the landed tool. `sh-fn-single-quoted` (cmd
`f() { sh -c 'pacman $1'; }\nf -Q`) is pinned to
`package_query/pacman`; the failsafe now yields `host_mutation/pacman`.
Drafts are round-19 work and are outside the harm-watch glob (which enumerates
`round-17/tripwire/*` and `round-18/tripwire/*`; `harm-watch.sh` lists exactly
the six suites run above), so no gate regressed. When the drafts are
applied/rejected, that pin must be re-cut. The round-17
`w2/adversarial` expected.json also still says `package_query` for the two
variable-op fixtures, but both tools score that corpus 4/26 (it expects
`pacman:-S` rules neither tool produces), so there is no pass/fail regression
there — only stale prose (`w2/reports/AdversarialFixtures.md`).

## 6. Residual risk and verification gaps

- I did not re-run `.ufo/waves/round-18/recut-receipts.sh` (not required by the
  ticket, and it needs the real transcripts outside the assigned scope). The
  direct local facts that matter were checked: both tools return
  `frozen_match` on the committed baseline and produce byte-identical
  `--scan` output over its 5 inputs, and `recut-summary.json` records
  `all_counts_identical`/`all_receipts_identical` true.
- Frozen replay hashes inputs, then `scan_file` re-reads them; the post-read
  digest check ("snapshot changed during scan" → `snapshot_tampered`) closes
  the obvious TOCTOU for the scanned bytes. Verified by reading `run_frozen`,
  not by racing a writer.
- `--frozen` still proves only "a pinned snapshot reproduces a pinned
  verdict"; provenance remains the separate read-only checker (it reports
  `match` here).
- I did not audit the r18 seat-scan receipt (`tripwire-r18-seats.txt`) or the
  5-file change-detector receipts beyond the frozen baseline; out of scope for
  this diff.
- No scan-classification difference was found outside the stated failsafe;
  the differential covers every committed `.jsonl` (242 files, including all
  transcript fixtures) and a 56-command operator matrix, not arbitrary future
  inputs.

## 7. Verdict

The landed `be886a3` tripwire change matches its declared scope. The only
observable scan-classification change is `package_query → host_mutation` for
`pacman` invocations with no readable operator, in the safe direction, with no
other class/rule change across the whole committed corpus; the four round-17
suites, the 31-case frozen suite, the failsafe suite and the frozen baseline
all pass exactly as claimed; the red-before receipt reproduces byte-for-byte
from the `abfbf35` tool on the `a210241` suite bytes (17/31, same 14 names).

Two small, contained validation gaps should be closed before the frozen gate
is treated as fully hardened: **F1** (`expected_findings` blank-line
reachability) and **F2** (`DIR/.` symlink bypass). F3-F6 are wording,
diagnostic, or non-gated draft-drift items; none changes a current receipt.
C3's headline evidence (frozen_match / one-byte tamper / 31/31 / provenance)
is verified.
