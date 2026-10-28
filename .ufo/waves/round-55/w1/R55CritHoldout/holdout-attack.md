# R55CritHoldout — attack on the C2 hold-out and its commitment (round 55, wave w1)

Seat: R55CritHoldout (critic, leaf). Lane base 3b55b6e91e40f455dd56b2985e4ffc087ada92d5; freeze commit 54dacbd8 (18:46:52 -0300).
Read-only: claims-frozen.md (C2 + Causal separability + Harm watch), registration.md §C2, frozen-tables.json `c2` (field names and
values), ctl/*.py, fixtures/c2/F01–F18 (all committed), fetch/host-input.conf, fetch/host-getoption.json, fetch/SHA256SUMS.txt,
freeze-verify.py, quality/check-r55-controls.py (dispatcher, untracked). Demonstrations in
`attack/` next to this file; raw output in `receipts.txt`.

Hold-out disclosure: `frozen-tables.json` field `c2.holdout_dir` names the sealed directory path, and every seat can read that
file. I did not open that path, did not list it, and did not use it. Reported under Defect D6.

## Summary (ranked)

| # | Finding | Severity | Evidence |
|---|---|---|---|
| D1 | A grammar-free tool passes 17/18 committed fixtures by reading the `expected.out` that sits beside `--config`. No frozen control catches it. | High | `attack/sibling_tool.py`, receipts R1 |
| D2 | The same tool passes 1/18 once the export carries only the argv-named inputs. The harness does not do that export, so the hole is open. | High (fix is cheap) | receipts R2 |
| D3 | The harness that computes the hold-out commitment and runs the controls is not frozen: `quality/check-r55-controls.py` is untracked, `r55_ctl_c2.py` does not exist yet, and neither is in freeze commit 54dacbd8. | High | `git ls-files` / freeze file list |
| D4 | The commitment has no frozen root convention and no frozen test vector. A root mismatch at reveal reads as `holdout_commit=bad` and blames a correct tool. | Medium-high | registration §C2 wording |
| D5 | Hold-out expected outputs come from the author's reference, not from the prose. The prose has at least ten points where a literal reading differs from the likely reference, and the class list names them. The hold-out measures agreement with the reference. | Medium | Table A (A1–A10) |
| D6 | The sealed directory path is in committed `frozen-tables.json` (`c2.holdout_dir`), although the seat spec says seats are not told the path. | Low-medium | frozen-tables.json field |
| D7 | Selection among candidates by hold-out score is not governed. The L1 authors the hold-out, owns the reference, and integrates, so the selection is not independent. | Medium | registration "L1 holds the hold-out" |
| D8 | `ctl/lookup-committed.py` demands 0/8 hold-out. Any hold-out fixture whose argv equals a committed argv (for example `[]`, which is F17) gives it a hit and trips the control on a correct tool. | Low | ctl/lookup-committed.py; F17 args |

## Q1. Can a tool pass 18/18 + 8/8 without implementing the grammar?

**Memorisation keyed on argv: no, blocked.** `ctl/lookup-committed.py` is the control. It passes 18/18 committed by construction.
Its hold-out result is 0/8 only because hold-out argv paths point into the sealed directory. That holds as long as no hold-out
argv equals a committed argv. D8 is the exception.

**Memorisation keyed on the filesystem: yes, not blocked.** The C2 fixture exporter copies each fixture directory whole.
`expected.out` and `expected.rc` sit beside each `c*.conf` and `getoption.json`. A tool that prints the sibling
`expected.out` and exits with the sibling `expected.rc` never parses a line of the grammar.

Measured, `attack/sibling_tool.py` (about 15 lines, no grammar; the only logic is "find expected.* beside argv --config"), run by
`attack/run_fixtures.py` in the harness layout (cwd = exported tree, argv from `args.json`, byte compare of stdout, rc compare):

    F01:ok F02:FAIL F03:ok F04:ok F05:ok F06:ok F07:ok F08:ok F09:ok F10:ok F11:ok F12:ok F13:ok F14:ok F15:ok F16:ok F17:ok F18:ok
    fixtures=17/18

F02 fails only because its config is `fetch/host-input.conf`, which has no sibling. F15 passes because `F15/expected.out` is
next to a missing config path, and F17 passes on a usage fallback. A second grammar-free rule ("argv equals a committed argv,
print that expected") closes F02 and takes the tool to 18/18. That rule is a lookup and the control catches it, but the rule
combined with the sibling read is a lookup on argv plus a sibling read, and the controls only test the first half.

Against the hold-out: sibling reading gives 8/8 whenever each hold-out config sits in the same directory as its `expected.out`.
The registration says the hold-out is "revealed into `fixtures/c2-holdout/`" and does not state the layout. If the layout
matches the committed one (likely) and no hold-out reads a file under `fetch/` (the committed F02 is the only one that does),
the sibling tool gets 8/8 too. **So 18/18 + 8/8 without a grammar is reachable.** No frozen control detects it:
`const-host` passes at most 1 of 26 (F02's output, fixed), `empty` passes 0, and `lookup` is argv-keyed only.

Sandboxed export (R2 in receipts): copy only the argv-named input files into a clean tree, with no `expected.*`, `args.json`
or sibling fixtures present. The same sibling tool scores `fixtures=1/18` (F17 only). A grammar tool with correct path handling
is unaffected, since its inputs are the same bytes. So the fix is in the export, not in the grammar.

**Other routes checked, closed or weak:**
- Reading `frozen-tables.json` for fixture hashes: gives hashes, not outputs. Not a route.
- Calling `hyprctl` at run time to fill `live=` for F02/F13/F14/F16: the spec says the tool starts no process. The harness does not check that.
  A tool calling `hyprctl getoption` would disagree with the file-supplied values on F13 and on every hold-out with a `--getoption` file,
  so this route fails the hold-out. It is a rule the harness should enforce (for example, empty `PATH` in the child), not a live hole.
- Constant printing by argv: `const-host` is the control. Passes 1 of 26.

## Q2. Does the commitment bind args.json and the expected files, or only part?

Formula (registration §C2): sha256 over the lines `<relpath>\0<sha256(file bytes)>\n` for each file in sorted relative-path order.

- **Binds (if the walk covers every regular file in each hold-out directory):** `args.json`, `expected.out`, `expected.rc`, every
  `c*.conf`, every `getoption.json`, the set of file names, and the directory names through `relpath`. Changing one byte of any of
  these changes `holdout_commit`. So for the bytes, the answer is "all of them", on the assumption that the walk is over the
  directory and not over a list named in code.
- **Does not bind (unless the harness adds it):**
  1. **The relpath root.** The text does not say whether `relpath` is relative to `fixtures/c2-holdout/` or to the lane root. The
     two give different hashes. The sealed hash was computed once, with some root. If the harness uses the other root, the result is
     `holdout_commit=bad` for correct content. See D4.
  2. **Symlinks, modes, empty directories.** sha256 follows symlinks, so a link to a committed file hashes as that file. Empty
     hold-out directories are invisible to the hash. The harness must enumerate the directory and reject non-regular entries.
  3. **Correctness of `expected.*`.** The hash proves the bytes were not changed after sealing. It does not prove they are what
     the grammar says. Their producer is not recorded in any committed file. See D5.
  4. **The execution contract**: cwd, path resolution, environment, whether the tool may read siblings. The sibling attack (Q1)
     lives entirely in this gap.
  5. **The count of fixtures.** Implied by the file set; not stated separately.
- **Not verifiable before reveal.** `freeze-verify.py` checks committed fixtures and pins only. Nothing before reveal checks the
  hold-out against `holdout_commit_sha256`, and nothing committed records the sealed manifest (names and per-file hashes, no content).

Proposals (all require only a new committed file, not an edit of the frozen text):
- P1: commit a **manifest** of the sealed hold-out (relpath and sha256 lines, no content) in the freeze commit or a commit before the
  reveal. The manifest makes the commitment auditable and fixes the root.
- P2: commit a **self-test vector** for the commitment function: a dummy directory with known bytes and its expected
  `holdout_commit`, frozen in the same commit. The harness must reproduce it. A root or sort-order mismatch then shows up on the
  dummy, not on the hold-out.

## Q3. What can a seat who reads the registration infer about the hold-out classes, and how much does that help?

The registration names eight classes: key-before-name, nested touchpad blocks, boolean prefixes, duplicate keyboards,
CRLF/tabs, getoption anomalies, hex/sign tokens, variables and backslashes. Each class maps to a spec clause. Some of those
clauses are explicit, and some are ambiguous. The ambiguous ones are where the names help:

- Explicit, no help needed: key-before-name (no current device, unsupported +1), duplicate keyboards (merge, later key wins),
  nested `touchpad` (stack is not exactly `["device"]`, so ignored), hex/sign (anything not `[0-9]+` is unsupported), variables and
  backslashes (whole-line check, ends the line).
- Ambiguous, where the class name points at a choice (Table A): boolean prefixes (case, and `nope`/`onion`), CRLF/tabs (strip set,
  line split), getoption anomalies (blank line, NaN, `int` vs `bool`), hex/sign (fullmatch vs prefix, Unicode digits).

Assessment: the class list shows a seat where the reference is likely to differ from a naive reading. It does not reveal expected
output. A seat that implements the literal text gets each class right where the text is explicit. A seat that guesses the
reference's reading on ambiguous points gets some of them right by chance. The list therefore helps a dishonest seat only to
**choose between readings**, and only at the points in Table A. It does not let a seat fit fixtures it has not seen. Rating: **low
to moderate**. The larger problem is D5 (the reference is not the prose).

## Q4. Does selecting among independent candidates by hold-out score bias the claim?

Yes. Each candidate passes or fails each fixture as a byte comparison. Once the hold-out score is used to pick a candidate, or to
decide which one to repair, the 8 hold-out fixtures act as a training signal, and "8/8" is no longer a held-out result. With N
candidates that each pass the hold-out with probability p (for illustration: p = 0.05, N = 5 gives about 1-(0.95)^5 = 0.23),
the chance that at least one passes by luck is large. Candidates share a spec, so they are correlated, and the real number is
lower, but the claim should count the candidates that reached reveal.

**Proposed rule (R1–R5), to freeze before any candidate is revealed:**
- **R1 Candidate freeze.** Each candidate's tree is committed, and its sha256 manifest (file names and hashes) is committed, in a commit
  before the reveal. No candidate changes after that commit.
- **R2 One reveal.** The eight hold-out fixtures are revealed once, for the whole frozen set, in one integration step. A failing
  candidate is recorded as failed. It is not repaired and resubmitted against the same hold-out.
- **R3 Pre-declared selector.** The selector is fixed before reveal, for example "manifest order, first candidate that passes all
  committed fixtures". It is not "highest hold-out score". The report states N (candidates revealed) and lists every candidate's
  committed and hold-out result.
- **R4 No max-over-N claim.** The claim is TARGET_MET only for the selected candidate, and the report gives N. If N > 1, the
  claim is reported with N and the all-candidates table, not as a single 8/8.
- **R5 Post-reveal use.** After reveal the hold-out is public. The next round needs a new sealed set. The reveal commit is recorded
  in the receipt.

Plus a derivability gate (new, reported with the result, not a fourth claim): before reveal, a second implementer who did not write the
reference derives each hold-out expected output from the frozen prose only. If the second implementer's output disagrees with an H
fixture, that fixture is labelled **prose-ambiguous** and is reported, not counted as a tool failure.

## Defects and ambiguities (with inputs)

**D1 sibling read (High).** Input: `fixtures/c2/F01/args.json` = `["--config", ".../F01/c1.conf"]`. The tool finds `F01/expected.out`
beside `c1.conf` and prints it. Output: `fixtures=17/18` (receipts R1). The frozen controls do not catch it. Fix: export only
argv-named inputs, with no `expected.*`, `args.json` or sibling fixtures (receipts R2 shows 1/18). Add control
`C2-CTL-4 sibling-read`: a tool that reads `expected.*` beside `--config` must score ≤1 of 26 under the sandboxed export.
Add a `strace`/`openat` check or an empty-tree run so that "reads only the files named" is enforced, since the spec states the rule
and the harness does not check it.

**D2 sandbox.** Same as D1; receipts R2 is the evidence that the sandbox closes it.

**D3 harness not frozen.** `git ls-files quality/check-r55-controls.py` reports it is not tracked. The freeze commit (54dacbd8) file list
does not include `quality/`. `r55_ctl_c2.py`, which the dispatcher imports and which holds the commitment check and the three controls,
does not exist yet. Claims-frozen says "No predicate ... changes after any seat has scored". The predicate code is not in the
freeze. Fix: commit the harness modules, or their sha256, in a commit before `.ready`, and have `freeze-verify.py` check them.

**D4 commitment root and sort (Medium-high).** Input: registration §C2 "sha256 over, for each file in sorted relative-path order, the
line `<relpath>\0<sha256 of file bytes>\n`". Relative to what is not stated; sort is not stated as bytewise. A correct hold-out
can fail the commitment only because of the root convention, and nothing before reveal can show which convention was used.
Fix: P1 and P2 above.

**D5 reference is not the prose (Medium). Input: committed F10.** `F10/c1.conf` line 5 is `device[kbd-a]:repeat_rate = 70` at top level, with the
stack empty. The registration says KEY is "the stack joined with `:` then `:` then LHS". Read literally, the empty stack gives the
KEY `:device[kbd-a]:repeat_rate`, which is not relevant and not counted. Hand trace: the literal reading gives unsupported=3, and
the committed `F10/expected.out` says unsupported=4. The committed fixture follows the bare-LHS reading. So the prose, read
literally, disagrees with a committed fixture. The hold-out will follow the same reference, and so the prose cannot be the sole
source for it. This was hand-traced; the seat did not run a literal implementation.

**D6 hold-out path disclosed (Low-medium).** `frozen-tables.json` `c2.holdout_dir` = `.ufo/waves/round-55/fixtures/c2-holdout`. The
seat spec says "seats are not told its path". The string is in a committed file every seat reads. Harmless while the directory is
absent. After reveal it is public. Fix: keep the path out of committed files, or keep the sealed directory outside the lane until
reveal (the registration already says so; the frozen table does not follow it).

**D7 selection independence (Medium).** Registration says the L1 holds the hold-out, the L1 is the canonical planner, and the L1
integrates. The author, the reference, the selector and the integrator are one seat. Fix: R1–R5 and the derivability gate.

**D8 lookup control brittle (Low).** `ctl/lookup-committed.py` requires 0/8 on the hold-out. A hold-out argv identical to a committed
argv, with the same expected output, gives the lookup a hit, and the control fails on a correct tool. F17's argv is `[]`, so a hold-out
usage fixture with `[]` would trip it. Fix: state the control as "passes 0 hold-out fixtures whose argv is not in the committed set",
or assert the hold-out argv set is disjoint from the committed one at reveal.

### Table A — prose ambiguities a hold-out can hinge on

Each row: the input, the literal reading, the trap reading, and what Python does with the trap (`python3 -I`, measured).

| id | input | literal (prose) | trap | measured |
|---|---|---|---|---|
| A1 | top-level `device[kbd-a]:repeat_rate = 70` | empty stack: KEY `:…` → ignored | bare LHS, as F10 expects | committed F10 requires the bare-LHS reading (D5) |
| A2 | `repeat_rate = 0x1F`, `repeat_rate = 40abc` | `[0-9]+` full match: unsupported | `re.match('[0-9]+', …)` prefix: `0x1F`→0, `40abc`→40 | `re.match` on `40abc` → match; `fullmatch` → no. The prose names hex as unsupported, which requires fullmatch |
| A3 | `repeat_rate = 30 # $note` | whole-line check: `$` in the comment → unsupported +1, line ends, rate not set | RHS-only check: rate 30 | prose says "a line containing"; the check runs before the `#` cut |
| A4 | `repeat_rate = \xa030` (NBSP) | not in strip set: unsupported | `str.strip()` strips U+00A0 and `\x1c`–`\x1f`: `'\xa030'.strip()` → `'30'` | measured |
| A5 | `repeat_rate = 30\rrepeat_delay = 5` (lone CR) | split on `\n` only: one line, unsupported | `str.splitlines()` splits on `\r`: `'a\rb'.splitlines()` → 2 items | measured |
| A6 | file begins with U+FEFF then `input {` | UTF-8 decode keeps BOM: stack `["\ufeffinput"]`, keys ignored | `utf-8-sig` decode: block recognised | `'\ufeffinput'.strip()` keeps BOM |
| A7 | `repeat_rate = ٣٠` (Arabic-Indic digits) | `[0-9]` is ASCII: unsupported | `int()` accepts it: 30; `'²'.isdigit()` is True | measured `int('٣٠')` → 30 |
| A8 | getoption line `   ` (spaces only) | "non-empty" by raw bytes: `json` error → bad_json | "empty after strip" → skipped | spec does not say which |
| A9 | getoption line `{"option":"input:repeat_rate","int":NaN}` | RFC JSON: invalid → bad_json | Python `json` accepts NaN: float, so ignored, rc 0 | `json.loads` accepts NaN (measured) |
| A10 | getoption `"int": true` | not an integer: ignored | Python `bool` is an `int` subclass | `isinstance(True, int)` is True (measured) |

Other unspecified points, lower risk: getoption decoding (the config decode rule is in the config paragraph); precedence when several
setup errors apply (`--config missing` with a bad `--getoption`); `--keyboard` followed by `--config`; `name = kbd#1` (first or last `#`;
VALUE rule implies first, prose says "trailing"); `{` alone (pushes the empty string).

Each of A2–A10 is a defect if the hold-out uses it. Each reading in the trap column is one a careful implementer could pick, so
the reference's choice cannot be recovered from the prose. The fix is to make the derivability gate (Q4) decide, not the
implementer.

## Proposed control additions (for the L1; not edits to the frozen text)

- `C2-CTL-4 sibling-read`: tool reads `expected.*` beside `--config` → must score ≤1/26 under the sandboxed export.
- `C2-CTL-5 export-isolation`: the harness runs each fixture in a tree that holds only argv-named inputs (no `expected.*`, no
  `args.json`, no other fixture directories). Every fixture's expected output must still be producible from the inputs, which
  a control tool that reads only argv-named files demonstrates.
- `C2-CTL-6 no-process`: run the tool with an empty `PATH` and no network; a tool that calls `hyprctl` fails the fixture
  that needs `live=` (F13, F14, F16 and the hold-out getoption cases).
- Commitment self-test vector (P2) run before the hold-out check.

## What I could not verify

- The hold-out's contents, layout and expected outputs. Sealed, not opened. The commitment's root and the hold-out's layout are
  therefore unverified; Q1's "8/8 by sibling read" depends on the layout, which I did not see.
- `quality/r55_ctl_c2.py` (not present in the lane at time of reading) and the full check-r55-controls run. The sibling demonstration
  reproduces the fixture loop (argv from `args.json`, cwd = exported tree, byte compare), not the harness itself.
- Whether the reference implementation exists and what it does on Table A. Not in the lane.
- The literal-prose trace in D5 is by hand, not by a run of a literal implementation.
- Nothing was run against `tools/mado-kbdopts.py` (not yet in the tree).

## Tooling
None installed. Python 3 (`python3 -I`) only, for the demonstrations. No pacman or package actions.
