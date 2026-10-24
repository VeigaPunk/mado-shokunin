# RevRecordsChain — round-30 landed-chain review (records + claim machinery)

Seat: reviewer, records chain. Lane `mado-shokunin`, base `8f51071b`, tip `master`
`92d3c86`. Read-only: this seat wrote nothing except this report (all `git` calls
read-only; counters/gate re-run against committed bytes, no lane state changed).

Tooling note: **no LSP device is mounted in this session** (`write xd://lsp` →
`No such tool: xd://lsp. Mounted devices: ast_edit, debug`). Caller/definition
checks were therefore done by reading both changed Python artifacts in full plus
live re-runs; `grep` appears below only for literal-string/quote verification, never
as semantic proof of a caller relation.

## Verdict

The landed chain is **exactly the declared write set, append-only, three linear
commits by `mado-shokunin`**, and every cited hash and measured fraction reproduces
from committed bytes. **No unrelated change.** Two **High** record defects: one
committed receipt that is a tail rather than the full freeze-smoke output the round
claims, and one "verbatim" superseding criterion that silently drops a normative
anti-credit clause. Neither moves a measured predicate — all claim numbers were
independently reproduced (see §4). Findings are recommendations; nothing here is an
admission or a verdict.

## 1. Chain shape, authorship, scope — verified

`git log --oneline 8f51071b..master`:

```
92d3c86 round-30 records: receipts, wave spec, LOG, SCORECARD
446dc39 round-30 data: index rows, criterion grounding, S185, lesson
451e8b3 round-30: freeze registration, counters, index gate, controls
```

- **Linearity**: `451e8b3c` parent `8f51071b`; `446dc396` parent `451e8b3c`;
  `92d3c86` parent `446dc396`. No merge, no side branch.
- **Ancestry of the cited hashes**: `git merge-base --is-ancestor` true for both
  `451e8b3c` (freeze) and `446dc396` (data).
- **Authorship**: author *and* committer of both are
  `mado-shokunin <mado@shokunin.local>`; base `8f51071b` is
  `protocol-shokunin` (round-29 verifier spot-check), as expected.
- **Scope**: cumulative `git diff --name-only 8f51071b master` is 22 paths, all
  under `.ufo/waves/round-30/`, `corpus/`, `quality/check-index.py`, `LOG.md`,
  `SCORECARD.md`. The filtered command that prints everything *outside* those
  prefixes printed nothing.
- **`.ufo/waves/round-29/**` and `tools/` byte-untouched**:
  `git diff --stat 8f51071b master -- .ufo/waves/round-29/ tools/` is empty.
  Same empty result for `corpus/knowledge/ SKILL.md PROVINCE.md` (the registered
  harm-watch pathspec, `LOG.md:1818-1819`, `SCORECARD.md:1924-1927`).
- **Append-only**: every edited corpus/record file is an insertion-only hunk —
  `corpus/QUALITY.md @@ -334,3 +334,25 @@`, `corpus/README.md @@ -50,6 +50,8 @@`,
  `corpus/SOURCES.md @@ -194,6 +194,7 @@`, `LOG.md @@ -1774,3 +1774,56 @@`,
  `SCORECARD.md @@ -1898,3 +1898,41 @@`; cumulative diffstat says
  `1388 insertions(+)`, 0 deletions. `corpus/lessons/round-30.md` is a new file.
  Criterion 4 (errata append-only) holds.
- **Freeze integrity**: the three frozen artifacts are byte-identical to their
  freeze commit (same blob ids at `451e8b3c` and `master`):
  `quality/check-index.py` `df01b20f…`, `.ufo/waves/round-30/c2/count.py`
  `74a4859d…`, `registration.md` (110 lines; `git diff --stat 451e8b3c master --
  <those three>` empty). Individual sizes equal the freeze-commit insertions
  (219/195/110), i.e. no post-freeze edit.
- **Worktree (not part of this chain)**: `git status --porcelain` shows
  `M quality/q36-successor-receipts.txt` (uncommitted, written after the records
  commit; first flagged by RevC1Fence) and untracked `.ufo/waves/round-30/w1/`
  (this wave's seat reports). The chain under review is clean; the q36 drift is
  out-of-chain and I did not restore it (write-scope).

## 2. Classification of every change

| Path | Commit | Class | Note |
|---|---|---|---|
| `.ufo/waves/round-30/registration.md` | freeze | claim-machinery | frozen spec; unchanged after freeze |
| `.ufo/waves/round-30/c2/count.py` | freeze | claim-machinery | C2 counter; reads `git show REV:…`, writes nothing |
| `quality/check-index.py` | freeze | claim-machinery **+ shipped capability** | the C3 deliverable itself |
| `.ufo/waves/round-30/controls/C2K1-donothing.txt` | freeze | claim-machinery (control) | `cmp` byte-identical to `evidence/c2-before-8f51071b.txt` |
| `.ufo/waves/round-30/controls/C3K1-base-red.txt` | freeze | control | equals the live gate run at base (§4) |
| `.ufo/waves/round-30/controls/C3K2-selftest.txt` | freeze | control | `6/6`, equals live `--selftest` |
| `evidence/c1-before-8f51071b.txt`, `c2-before-8f51071b.txt`, `census-before.txt` | freeze | record | pre-data receipts |
| `corpus/README.md` | data | record / measured substrate | 2 index rows — the object the C1 fence counts |
| `corpus/QUALITY.md` | data | record / rubric substrate | rows 41–52 + preamble — the object the C2 counter parses |
| `corpus/SOURCES.md` | data | record | +S185 registry row |
| `corpus/lessons/round-30.md` | data | record | M30-1, M30-2, Gate (S185) |
| `evidence/{c1,c2,c3}-after-446dc396.txt`, `census-end.txt`, `freeze-smoke-451e8b3c.txt` | records | record | post-data receipts |
| `.ufo/waves/round-30/w1-{plan,spec}.json` | records | claim-machinery (wave) | 33 items; plan `counts {spawn:33, resume:0}` |
| `LOG.md`, `SCORECARD.md` | records | record | append-only round entry + results/scorecard |
| **unrelated** | — | **none** | 0 paths outside the declared set |

## 3. Findings (severity order)

### F1 — High. The freeze-smoke receipt's C2 leg is a tail, not "full output"

`.ufo/waves/round-30/evidence/freeze-smoke-451e8b3c.txt:5-9` contains, for C2,
only five lines:

```
--- C2 at freeze ---
UNRESOLVED criterion 39: no citation
UNRESOLVED criterion 40: no citation
LINE 20 superseded excluded
PRED-C2-r30 verdict=TARGET_MISSED
```

Live re-run at the same revision prints **14** lines: the `counter=` header, three
`METRIC` lines (`literal lines=28/40`, `superseded=[20]`, `active=39
resolved_active=31`), **eight** `UNRESOLVED` criteria (1–5, 38, 39, 40), `LINE 20
superseded excluded`, verdict, and `EXIT=1`. So the receipt hides 6 of the 8
unresolved criteria and *all* the tallies, and unlike the C1/C3 legs it carries no
`EXIT` line (C1 `:4`, C3 `:14`). The missing lines do not contradict the committed
pre-data receipt (`c2-before-8f51071b.txt`, which is complete); the defect is
evidence completeness, not measurement.

Why it is a defect, not a nit: the round invokes its own criterion 49 for exactly
this artifact — `LOG.md:1810-1811` "all three counters run at the freeze commit
`451e8b3c` and print real tallies", `registration.md:86-88` "the composite smoke
rule (criterion 49) is satisfied by running all three at their freeze commit";
criterion 49 (`QUALITY.md:355` at tip, superseding 38) requires "its **full
output** is committed". As committed, the C2 leg does not show the tallies the LOG
says it printed. Fix: replace the C2 section with the full 14-line output (and the
`EXIT=1`), keeping the current receipt as an erratum.

### F2 — High. Row 48 is not a "verbatim" restatement: it drops a normative clause

`corpus/QUALITY.md:338-346` (new preamble) asserts: "Each superseding row below
restates its rule **verbatim** and supplies the canonical citation."

Base criterion 32 is a single 861-byte line (`8f51071b:corpus/QUALITY.md`) whose
final sentence is:

> Ground: lesson round21 M13, `residual/FinalBindingReview.md` F1–F5 and its six
> inert fixtures. **This criterion is added after final falsification, supplies no
> retroactive pass and no numeric C2/criterion-count credit; delivered C1 fails it
> and remains harmed.**

Tip row 48 (`QUALITY.md:354`, complete at 793 bytes, balanced parentheses) keeps
the *rule* sentences verbatim and folds the "Ground" pointer into its citation —
but the second sentence above is **absent**. That sentence is an accounting
constraint ("no numeric C2/criterion-count credit"), i.e. precisely the kind of
anti-inflation clause that should stay in force when a round changes the criterion
population (39 → 40 active, 40 → 52 lines) and claims C2 credit for it.

Rows 46–47 and 49–51 are different in kind and acceptable under the same claim:
row 46 is normalized-identical to base 18 (checked programmatically), row 47 keeps
19's numbered rule and only turns the "outside R13-V1" tag into a resolvable path,
and rows 49–51 drop only the parenthetical *evidence instances* (`count.py:100`
pin, H1 receipt, `ref-chk-*` survivors) while preserving every rule and check
sentence. Row 48 is the sole case where normative text leaves the active rubric.
Fix: append the dropped sentence to row 48 (append-only correction; no rewrite).

### F3 — Medium. The seed-five "grounding" cites the defect row about itself

Rows 41–45 (`QUALITY.md:347-351`) cite `lessons/round-30.md#mistakes M30-1`, whose
only content (`lessons/round-30.md:13`) is the finding that criteria 1–5 had no
lesson citation, plus `MINT.md`. `MINT.md` is real and does support row 41's
description (two numbered demand instances; "No province absorbs the compositor
config plane", `MINT.md:3-16`) — I checked it, it is not fabricated. But 5 of the
40 active criteria now "resolve" through the audit row that records their own
defect, not through a lesson that derives the rule. The preamble discloses this
("its grounds are `MINT.md` … and … M30-1"), so it is not concealment; the defect
is the metric's name. C2's predicate measures **citation resolvability**, not
lesson derivation. The round report should state that limit rather than let
"lesson-grounded admission criteria" imply otherwise.

### F4 — Medium. S185's "verbatim" located quote is a paraphrase, and its sha256 is serialization-specific

`corpus/lessons/round-30.md:24` presents as a "located quote (≤25 words, verbatim)":

```
revision=$rev indexed=$covered/$total missing=$missing dangling=$dangling duplicates=$duplicates coverage=$score/10
```

That string occurs **nowhere in `SCORECARD.md`** (grep over all `*.md`: only the
lesson itself contains it). The actual source line, `SCORECARD.md:84`, is a Python
f-string: `print(f"revision={rev} indexed={covered}/{len(notes)}
missing={len(missing)} … coverage={10*covered/len(notes):.4f}/10")`. The Gate
protocol in this lane requires a verbatim located quote; this is a normalized
template. The pinned block digest `8b59b503805396b5…` **does** resolve, but only
under one of five plausible serializations I tested — the fence *inner* bytes
including the trailing newline (the other four: fences included, inner without
trailing newline, fences without newline, lang line included). The S185 row is
therefore checkable only by guessing the serialization; name it in the row (e.g.
"sha256 of the bytes between the fences, trailing newline included") so the anchor
is re-derivable. `SOURCES.md`'s own S185 anchor cell (`prints
indexed=covered/N missing=… coverage=…/10`) is honest description and not affected.

### F5 — Low. Registration arithmetic wording is off by one (frozen doc; note only)

`registration.md:60-62`: "Target: resolved-active 40/40 (12 lines superseded by
rows 41–51, +1 new criterion 52 …)". Rows 41–51 supersede **11** lines
(1–5, 18, 19, 32, 38–40); the twelfth superseded line is 20 (by criterion 21, as
the same registration says two paragraphs earlier). The landed arithmetic is
correct — 52 lines − 12 superseded = 40 active — and the counter's own
`METRIC superseded=[1, 2, 3, 4, 5, 18, 19, 20, 32, 38, 39, 40]` matches
`SCORECARD.md:1915`'s set exactly. The registration is frozen, so this is a note
for the round report, not an edit.

### F6 — Low. The gate selftest's "symlink-refused" case does not exercise member refusal

`quality/check-index.py:203-213` (case 5) symlinks the *knowledge directory* to
`/nonexistent` and asserts `REFUSED`. The member-level branch at
`check-index.py:66-68` (`os.path.islink(fpath)` per directory entry) is never
exercised, so the capability rows' "refuses non-regular members"
(`SCORECARD.md:1922`) and the lesson's "symlink-refused" (`lessons/round-30.md`,
C3 note) rest on code inspection plus a directory-level probe. Also note the gate
is stricter than criterion 46's source-target policy (which *follows* file
symlinks): that is a different subject and the gate's own contract says "symlinks
refused" (`registration.md:52-54`), so no contradiction — just scope. Adding one
member-symlink case would make 7/7 and close the gap.

### F7 — Low. "misroot sweep clean" has no committed receipt

`LOG.md:1820` and `SCORECARD.md:1924-1928` finish the harm watch with "no
compositor/config mutation; misroot sweep clean". Every other harm-watch item names
a re-runnable command or a receipt; this one names neither, and no misroot receipt
is in `evidence/`. The chain diff corroborates the *lane* half (0 paths outside the
write set, `tools/`+`corpus/knowledge/` empty), but the fleet-root sweep is
unverifiable from the chain. Criterion 42 (measured anchor) applies; either commit
the sweep output or drop it from the harm watch.

### F8 — Low. Round-report pointer is dangling at the records commit (closure pending)

`LOG.md:1828`: "The round report `.ufo/reports/round-30/mado.md` cites the pushed
lane hash at write time." `.ufo/reports/round-30/` does not exist at `master`. The
sentence is forward-looking and the round is not closed (wave 1 is being
dispatched), so this is a pending closure pointer, not a false claim — recorded
because S003's closure-time pointer rule is satisfied only when the report lands.

### F9 — Out-of-chain, low. Committed q36 receipt is dirty in the worktree

`M quality/q36-successor-receipts.txt` (uncommitted, after the records commit).
Per RevC1Fence the change is ephemeral `/tmp` + `/fast/scratch` run dirs with all
rc/expected/PASS lines unchanged, so no verdict moved. If it is committed, a
prior-round evidence blob changes outside this round's registered write set. Not
restored (write-scope).

### F10 — Low. Counter block attribution: trailing section prose binds to the last criterion

`c2/count.py`'s criterion block runs from a numbered line to the next numbered line
with no heading awareness, so the new `## Grounding repair` heading and preamble
(`QUALITY.md:338-346`) are part of **criterion 40's** text. Harmless this round only
because 40 is superseded and excluded from both fractions. The future vector: any
concrete `lessons/<file>.md` path appended after the last *active* criterion makes
that criterion "resolve" without a citation on its own line (literal stays red,
resolved flips green). Also note the deliberate asymmetry — literal is per numbered
line (`c["lit"]`), resolved is per block — which is why 18/19/32 resolved at base;
that is the frozen rubric and is fine, but heading-aware blocking would remove the
free-text vector.

## 4. Claim numbers reproduced (so the record defects cannot hide a measurement defect)

All run by this seat against committed bytes; outputs match the receipts byte-for-byte
except where noted in F1.

| Measurement | Command | Result |
|---|---|---|
| C2 at base | `python3 -I .ufo/waves/round-30/c2/count.py 8f51071b` | `literal 28/40`, `superseded=[20]`, `active=39 resolved_active=31`, UNRESOLVED {1–5,38,39,40}, `TARGET_MISSED`, exit 1 |
| C2 at data commit | `… count.py 446dc396` | `literal 40/52`, `superseded=[1..5,18,19,20,32,38,39,40]`, `active=40 resolved_active=40`, `TARGET_MET`, exit 0 |
| C3 gate at base | `python3 -I quality/check-index.py --rev 8f51071b --repo .` | `indexed=41/43 missing=2` (both named), exit 1 |
| C3 gate at tip | `… --rev 446dc396 --repo .` | `indexed=43/43 missing=0 dangling=0 duplicates=0`, exit 0 |
| C3 selftest | `… --selftest` | `MADO_INDEX_SELFTEST: 6/6`, exit 0 |
| Harm watch | `bash tools/mado-verify.sh --selftest` | `MADO_SELFTEST: 460/460`, exit 0 (18 s) |
| Sources counts | row/tier/status recount at both revs | 184→185 rows; A 177→178; mined 165→166; queued 10; rejected 9; no duplicate ids; max id 185 — exactly `SCORECARD.md:1932-1934` |
| Freeze smoke C2 | `… count.py 451e8b3c` | 14 lines incl. METRIC tallies and `EXIT=1` — receipt has 5 (F1) |
| Supersede restatement | normalized text diff, base criteria → rows 41–51 | 46 identical; 47/49/50/51 rule-preserving; **48 drops one normative sentence** (F2) |
| Controls | `cmp` | `C2K1 == c2-before`; `C3K1` == gate base run; `C3K2` == `--selftest` |

Grounds for the record claims I could check end-to-end: `MINT.md` supports row 41;
`corpus/lessons/round-29.md` M29-sweep **does** record "41/43 at base and tip alike"
as M30-2 (`lessons/round-30.md:14`) states; the routed-gap pointer
`corpus/lessons/round-29-verifier-spotcheck.md:56,85-87` exists and names the two
notes; the two new README rows point at real notes and real artifacts
(`tools/mado-wsrules.py`, `.ufo/waves/round-27/c1/count-v4.py`,
`.ufo/waves/round-28/registration.md`; S178–S183 present); S185's `used-by` paths
exist; census `185 / malformed 0 / dup ids none / mined used-by missing none`.

No code caller consumes the changed artifacts other than the committed receipts:
`quality/counter-selftest.py` is a round-26-counter harness and does not enumerate
`c2/count.py` or `check-index.py`; neither new script imports the other; both are
invoked only as `python3 -I <path>`.

## 5. Residual risk and verification gaps

- **Resume lanes: not applicable.** `w1-plan.json` `counts {spawn: 33, resume: 0}`,
  33 unique task names, no `resume` token anywhere in the plan, and the spec has 33
  items — so `resume_continuity_v1` is not exercised by this chain; there is no
  resume path to preflight, by construction.
- **One canonical runtime: holds for the two claim instruments.** Both read
  committed bytes only (`count.py` `git show REV:…`; `check-index.py`
  `git -C repo show`/`ls-tree` in `--rev` mode). Neither writes to the lane
  (`count.py` has no write path; `check-index.py` writes only inside
  `tempfile.TemporaryDirectory` in `selftest()`). The receipts use `--rev`, not the
  other (`--root`) mode; the `--root`/`--rev` divergences RevC1Fence found are
  latent on committed bytes and are their item, not a record defect here.
- **Not verified by me** (no artifact in the chain): saturation "9.0 / N=3
  unchanged"; the fleet misroot sweep (F7); the round report that would close F8;
  the forensic provenance of the dirty q36 receipt (F9, RevC1Fence's observation).
- **Claim-scope limit worth carrying into closure**: C2's 40/40 measures citation
  resolvability under a counter that accepts a defect row as ground (F3), and its
  freeze-smoke evidence is incomplete as committed (F1). Both should be named in
  the round report rather than implied away; neither changes the measured numbers,
  which I reproduced independently.
