# ExecIndepV2 — an independent implementation of PRED-C1-r44-v2 from the counter docstrings

Seat: `ExecIndepV2`, wave `w2`, round 44 (hyaku run 9, 2026-10-26).
Target: implement the v2 tool contract from the docstring only, score it, and report every contract
sentence that was ambiguous.

**Result: the contract is implementable from its docstring alone — `fixtures=26/26 … verdict=TARGET_MET`,
exit 0, all seven clauses, on the first scoring run.** No open predicate defect was found; the notes in §4
are docstring-precision findings, not holes.

## 1. Deliverable

| item | value |
|---|---|
| file | `.ufo/waves/round-44/w2/ExecIndepV2/mado-geometry-indep.py` (557 lines) |
| sha256 | `88e17eb8f9d994c34a000e8a376eeb3c9b1e01c9e0ddad1f420e1fbb0798c6af` |
| starting point | `git show 6a1a90528fe533cadee506a9fa3e9d13d15cc41f:tools/mado-geometry.py`, sha256 `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99` (matches the round-43 hash registration-v2 names) |
| change size | `+168 / -35` vs that base → `w2/ExecIndepV2/diff-vs-base.diff` |
| selftest | `MADO_GEOMETRY_SELFTEST: 129/129 passed` (k == n, n = 129 ≥ 80); 56 of the cases are new round-44 state assertions |
| scoring receipt | `w2/ExecIndepV2/receipt-score.txt` |
| ambiguity demos | `w2/ExecIndepV2/receipt-ambiguity.txt` |

Scored with exactly the counting command plus `--tool` (full stdout in the receipt):

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r44-geometry-states-v2.py \
  --repo . --rev e46789213830597348fe96a351ae004d10587385 \
  --work /fast/scratch/hyaku/mado-r44/ExecIndepV2 \
  --tool .ufo/waves/round-44/w2/ExecIndepV2/mado-geometry-indep.py
```

Final two lines of `receipt-score.txt` (exit 0):

```
PRED-C1-r44-v2 clauses=a:1 b:1 b4:1 b5:1 e:1 g:1 r:1
PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET rev=e46789213830597348fe96a351ae004d10587385 nonce=b9ded6207e2e5df8
```

Clause detail from the same receipt:

- `b rc=0 selftest=129/129`;
- `b4 sites=18 killed=18 need=14` (my own two state functions `fsmode_of`, `verdict_of` plus the state
  branches in `evaluate`/`report`; every flipped comparison fails the selftest — no surviving mutant);
- `b5 state_blind_selftest rc=1 selftest=111/129 failed=1` — with `json.loads` renaming `fullscreen`, 18
  state assertions fail, so the teeth bind the JSON path and not a helper dictionary;
- `e` — all five fixtures `sandbox_rc=… plain_rc=… same=1` (fs0 5/5, fsagree0 5/5, max0 5/5, fsmix0 1/1,
  fsclient0 1/1);
- `r rc=0 PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET` — the round-42 contract (and its
  TILED behaviour) is unharmed, i.e. the non-state output is byte-identical to round 43;
- all 12 `sgen*` and all 14 fixed fixtures `ok=1`.

Implementation shape (from the docstring, not from the landed tool): `fsmode_of` returns the `fullscreen`
integer only when `type(f) is int` and it is 1 or 2; `verdict_of` tests
`BADSIZE → FULLSCREEN → MAXIMIZED → TILED → AGREE → DIFFER`; `report` computes
`states = maximized + fullscreen` from the *tally* and inserts ` maximized=<n> fullscreen=<n>` between
`badsize=<n>` and ` verdict=` only when `states > 0`, and adds `NOT_COMPARED` (exit 5) when
`agree == 0 and states > 0` after the NO_SIZE_RULES/DIFFER/NO_MATCHING_CLIENT tests.

## 2. What the exercise establishes

- The predicate is satisfiable by a second, independently written implementation: the docstring plus the
  round-42 docstring determine the output byte-exactly (26/26), so the fixtures are not keyed to the
  reference's internals (they are keyed to the model, which is what the docstring restates).
- The clause **b4** minimum (`>= 6` sites) is reachable organically: two small state functions with a
  `fullscreen` string constant give 18 flippable comparisons, all killed by state assertions. A tool does
  not need the reference's layout to pass b4.
- **b5** discriminates on content, not on name: renaming the JSON key killed 18/129 of my cases, which is
  exactly the state surface, so the clause is load-bearing for a tool built this way.

## 3. Ambient facts recorded

- Lane `HEAD` is `290cddea92a18e2202456db89cb2bb60d9aaacff` at the time of this seat, i.e. above the data
  commit; every score above used `--rev e46789213830597348fe96a351ae004d10587385` as assigned, so the
  result does not depend on the tip.
- No install, no `pacman`, no package transaction, no git write (only `git show` / `git rev-parse`), no
  compositor call, no Wayland connection.
- Written only under `w2/ExecIndepV2/`. Scratch `/fast/scratch/hyaku/mado-r44/ExecIndepV2` was used for the
  counter's `--work` and the base extraction, and removed at the end of the seat.

## 4. Contract sentences that were ambiguous (or silent)

Each item: the sentence (≤ 25 words, locator computed with `grep -n`), the competing readings, what I
implemented, and what settles it. Severity is what a *second implementer* would risk, not a defect in the
counter.

### A1 — are `maximized`/`fullscreen` client attributes or verdict counts? (HIGH)

> "the summary line carries ` maximized=<n> fullscreen=<n>` … exactly when maximized + fullscreen > 0"
> — `quality/counters/c1-r44-geometry-states-v2.py:17-18`

Competing readings: (i) count clients whose `fullscreen` key is 1/2; (ii) count the two *verdict classes*.
Reading (i) makes a fullscreen client with `"size": [420.0, 500]` produce `fullscreen=1 verdict=NOT_COMPARED`;
reading (ii) makes it `badsize=1` with no state field and **`verdict=OK` exit 0**. The docstring fixes the
verdict order (BADSIZE first, `:15-16`) but never says the summary counters are verdict counts. I implemented
(ii); `receipt-ambiguity.txt` shows both cases, and fixture `fsbad0` pins it: a dump whose only client is
fullscreen but has an unusable size is `OK`. This is the single sentence I would re-word, e.g. "maximized and
fullscreen count the MAXIMIZED and FULLSCREEN verdicts, so a state client with no usable size counts as
BADSIZE only".

### A2 — a fullscreen client whose size equals the rule's `want` is `NOT_COMPARED`, not `OK` (HIGH)

> "verdict is tested in the order NO_SIZE_RULES … | NOT_COMPARED (agree=0 and maximized + fullscreen > 0; exit 5)"
> — `quality/counters/c1-r44-geometry-states-v2.py:19-20` (the sentence starts on `:18`, after "the top")

Nothing states the consequence: because `FULLSCREEN` is tested before `AGREE` (`:15-16`), a maximized or
fullscreen client never increments `agree`, so a dump of one fullscreen client at exactly 420x500 is
`NOT_COMPARED` (exit 5), not `OK`. A reader who keeps the rule's size comparable for state clients gets
`agree=1 … verdict=OK` and fails `fsagree0`. I implemented the literal order; my selftest pins it as
`fs-matching-size-not-compared` and the fixture `fsagree0` agrees. (Related, and stated only in
`registration-v2.md`, not in the predicate: a TILED-only dump stays `OK`; my `tiled-only-ok` case covers it.)

### A3 — clause b4's sentence is grammatically ambiguous about scope and about what a "site" is (MEDIUM)

> "the comparison sites of every function … whose body holds a string constant containing `fullscreen` (any case) number >= 6"
> — `quality/counters/c1-r44-geometry-states-v2.py:31-32`

Three readings: (i) each qualifying function must hold ≥ 6 sites; (ii) the total across qualifying functions
must be ≥ 6; (iii) the numbers 6 count something other than comparisons. The sentence also never defines
"comparison site". **Disclosure:** because of this I read the clause's implementation, `state_sites`
(`:290-315`), which shows (ii) — summed — and a site is any `ast.Compare` with exactly one op in the
flippable set (`old.FLIP`). A docstring-only implementer who reads (i) and concentrates the state logic in one
function would still pass (my `verdict_of` alone has 4, so the split matters); one who reads "site" as "any
expression mentioning fullscreen" would not know how to count. Suggested re-wording: "across all such
functions there are at least 6 single-operator comparisons, and flipping ≥ 75 % of them (rounded up) makes the
copy's selftest fail".

### A4 — `rules=0` in the round-42 verdict line means *size* rules (MEDIUM)

> "V = NO_SIZE_RULES (rules=0; exit 4)" — `quality/counters/c1-r42-geometry.py:55`

The summary prints `rules=<size rules> float_rules=<n>`, so `rules=0` is a statement about size rules only: a
config with one supported `float` rule is `NO_SIZE_RULES`, exit 4, printed as `rules=0 float_rules=1`. The
sentence alone can be read as "no supported rules at all". I implemented size-rules-only (base semantics);
`fsnorules0` and my `no-size-rule-rc` case pin it.

### A5 — `fullscreenClient` is never defined, yet must be ignored (MEDIUM, silence)

> "…and sometimes a `fullscreenClient` value" — `quality/counters/c1-r44-geometry-states-v2.py:28`

The contract defines the state as "the `fullscreen` value" (`:13-15`) and says nothing about
`fullscreenClient`, but the generator injects it and `fsclient0` (and `maxfloat0`-adjacent cases) require it
to have no effect. A tool that accepted either key fails. I ignored it (`fsclient-ignored-maximized`,
`fsclient-alone-ignored`; demo B in `receipt-ambiguity.txt`). Worth one clause sentence: "no other key,
`fullscreenClient` included, carries a state".

### A6 — the state field's position is stated unconditionally, but three verdicts can print it (LOW)

> "the summary line carries ` maximized=<n> fullscreen=<n>` between `badsize=<n>` and ` verdict=`"
> — `quality/counters/c1-r44-geometry-states-v2.py:17-18`

The sentence does not scope the field to a verdict. It is unreachable under `NO_SIZE_RULES` and
`NO_MATCHING_CLIENT` (a client is matched only through a size rule), but it *is* printed under `DIFFER`
(fsmix0: `… badsize=0 maximized=1 fullscreen=1 verdict=DIFFER`) and under `OK` (a fullscreen client beside an
agreeing one — my `fs-plus-agree-summary`). I computed the field from the tally after the loop, independent of
the verdict; both fixtures agree.

### A7 — "the client line is unchanged except for the two new words" (LOW)

> "the client line is unchanged except for the two new words" — `quality/counters/c1-r44-geometry-states-v2.py:16`

Ambiguous whether a state client still reports `want=<WxH>` (the rule's size) and its own `size=`, or gets
`size=-`/no `want`. "Unchanged" settles it: full line, only `verdict=` changes to `FULLSCREEN`/`MAXIMIZED`.
Implemented that way; my `fs-client-line` and `max-client-line` cases pin the whole line.

### A8 — clause b/b5 do not say *which* state assertions the selftest needs (LOW)

> "`--selftest` exits 0 printing `MADO_GEOMETRY_SELFTEST: k/n passed`, k == n, n >= 80"
> — `quality/counters/c1-r44-geometry-states-v2.py:30`

and

> "the selftest asserts state verdicts through the JSON path" — `quality/counters/c1-r44-geometry-states-v2.py:36`

There is no minimum number of state cases and no list of states. b5 makes "some state assertion through
`json.loads`" necessary, not "each of the six verdict words". I chose to assert all of: both state words, both
state counts, the state-absent line, `NOT_COMPARED` and `OK`, the BADSIZE-beats-state precedence, the ten
non-state `fullscreen` values, duplicate-key resolution, `fullscreenClient`, and the summary byte position.
A minimal tool with one `MAXIMIZED` assertion would pass b5 — that is a declared-residual-shaped gap, not a
hole in what is scored (b4 still needs the comparisons killed).

### A9 — clause e fixes stdout and exit but not stderr (LOW)

> "stdout and exit code must equal the sandboxed run" — `quality/counters/c1-r44-geometry-states-v2.py:39`

Clause f already requires empty stderr on rc 0/1/3/4/5 (`:29`), so nothing is scored on stderr under e; a tool
that wrote a warning only in the unsandboxed environment would not be caught by e. My tool writes no stderr
at all.

### A10 — "absent, null, 0, 3, -1, true, 2.0, \"2\", lists and objects are 0" is a closed list (LOW)

> "else 0 (absent, null, 0, 3, -1, true, 2.0, \"2\", lists and objects are 0)"
> — `quality/counters/c1-r44-geometry-states-v2.py:13-15`

The list is illustrative of a rule that is already complete ("a JSON integer … equal to 1 or 2"), so I
implemented the rule (`type(f) is int` and `f in (1, 2)`), not the list. Consequence worth knowing: a *bool*
falls out by type, so `true` is 0 and not 1 — the list says so, and the pool draws `true`. No conflict; noted
because "lists and objects" in a value list reads oddly for a JSON member.

## 5. Independence and disclosures

Not read, deliberately and verifiably (no `read`/`grep` call in this seat names them):

- `tools/mado-geometry.py` at `e46789213830597348fe96a351ae004d10587385` or at lane `HEAD`;
- `.ufo/waves/round-44/c1/ctl-ref-tool-v2.py.txt` (the reference) and the `receipts/c1-v1-to-v2.diff`;
- the w1 reports.

Read, in this order: `registration-v2.md`; the docstrings of
`quality/counters/c1-r44-geometry-states-v2.py` and `quality/counters/c1-r42-geometry.py`; the base tool at
`6a1a905`; then — **disclosed** — the v2 counter's implementation (`model_out_states`, `state_sites`,
`state_blind`, `invariance`, `main`) and, from the round-42 counter, `execute`/`case_files`/`function_sites`/
`mutate_source`. The reason for reading implementations on top of the docstrings was A3 (b4's sentence is
grammatically ambiguous) and the need to know the sandbox/judge shape; §4 records that disclosure at the point
where it changes an answer.

## 6. Findings for the L1

1. **No open predicate defect.** Every clause of `PRED-C1-r44-v2` is met by an implementation that shares no
   code with the landed tool, so the predicate is not satisfiable only by the reference's shape.
2. **Content-error candidates in the predicate docstring (his call, no re-registration):** A1 and A2 are
   precision gaps that a careful implementer can read wrong without any fixture hint in the docstring text;
   A3 is a genuine grammar defect ("every function … number >= 6"); A5 is a missing sentence about an input
   the counter itself generates. Exact replacement sentences are proposed in place at A1, A3 and A5.
3. **Not evidence about C1's operability claim**: this seat only shows the contract is implementable; it says
   nothing about whether the landed `tools/mado-geometry.py` is correct.
4. Deliverable is a seat artifact, not a lane file: if it is to be integrated, the L1 owns the integration and
   the post-integration gate run (I ran only my own selftest and the assigned scoring command).

## 7. Reproduction

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
git show 6a1a90528fe533cadee506a9fa3e9d13d15cc41f:tools/mado-geometry.py   # sha256 e3c2e471…
python3 -I .ufo/waves/round-44/w2/ExecIndepV2/mado-geometry-indep.py --selftest
python3 -I quality/counters/c1-r44-geometry-states-v2.py --repo . --rev e46789213830597348fe96a351ae004d10587385 \
  --work /fast/scratch/hyaku/mado-r44/ExecIndepV2 --tool .ufo/waves/round-44/w2/ExecIndepV2/mado-geometry-indep.py
```

Artefacts in this seat: `mado-geometry-indep.py`, `diff-vs-base.diff`, `receipt-score.txt`,
`receipt-ambiguity.txt`, `verify-quotes.sh`, `receipt-quotes-verified.txt` (every §4 quote, grepped
verbatim at the cited line — 17/17 `OK`, exit 0).
