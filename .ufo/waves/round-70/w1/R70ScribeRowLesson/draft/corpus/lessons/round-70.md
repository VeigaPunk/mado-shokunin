# mado round 70 — lesson

author: R70ScribeRowLesson (w1 scribe seat)
date: 2026-11-04 (America/Sao_Paulo)
round: mado lane counter 70 (hyaku run 15), base `b37a5aec4ea03f2223d8e09dd5d386d055c24179`
frozen inputs: `.ufo/waves/round-70/claims-declaration-r70.md` @ `bc18399b409a6390a6c6e8831bf9ad2dacbbf189`
receipts read: `.ufo/waves/round-70/measurement-r70.txt` (tracked, measured content `5adba5a9`),
`.ufo/waves/round-70/harm-watch-r70.txt` (rev `71caa8b7`), `.ufo/waves/round-70/control-baseline-r70.txt`
lane head at scribe time: `3aea1e10aad3365ca1b648ddfba7e6b1818970fc` (moved three times while this seat ran; see § Findings in the seat report)
scope of this file: the round lesson only. No measurement here was produced by executing either scored counter.

## Outcome and boundaries

**C1 — calibration: the landing harness credits a kill only on a parsed failed assertion.** The frozen
predicate is declaration § C1: at `REV`, `quality/counters/c1-r70-real-children.py --repo . --rev REV
--base-rev b37a5aec… --scratch-root DIR` prints, as its last line,
`MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=1 verdict=TARGET_MET rev=<sha>` and exits 0;
a scenario is correct iff the harness's own `mz=` field equals the pre-frozen expectation, and
TARGET_MET additionally requires `base_correct == 1`. The round's receipt
(`.ufo/waves/round-70/measurement-r70.txt`, `# measured content: 5adba5a92a8d58eb76533b39a9216d8e85d48fbc`)
prints that line at `5adba5a92a8d58eb76533b39a9216d8e85d48fbc`, `rc=0`, over three real `bash`
fixtures: `genuine` (candidate `pass`, base `pass`), `crash` (candidate `fail`, base `pass`),
`garbage` (candidate `fail`, base `pass`) — so the held round-69 harness still credits the crashed and
the garbled child, `base_correct=1`. Bounded score `10 × 3/3 = 10.0000` against the base leg `3.3333`.
**This seat did not execute the counter**: the numbers above are read from the receipt, not measured
here. The fixture revisions (`1fc2ee07`, `aa96ca80`, `8346d41c`) are scratch fixtures built by the
counter, not lane commits.

**C2 — operability: the guard census counts four more carrier shapes.** The frozen predicate is
declaration § C2: at `REV`, `quality/counters/c2-r70-carriers.py --repo . --rev REV --base-rev
b37a5aec… --controls .ufo/waves/round-70/controls/c2-controls-r70.json --scratch-root DIR` prints
`MADO_R70_GUARD_CARRIERS: population=20 readers=13 guarded=13 unguarded=0 controls=17/17
base_controls=13/17 verdict=TARGET_MET rev=<sha>` and exits 0, with the frozen control file's sha256
asserted (`29947b4c…`). The same receipt prints that line at `5adba5a9`, `rc=0`: all 17 candidate
control rows `correct=yes`; the base leg is `13/17` with `alias-carried`, `attribute-carried`,
`splat-carried` and `constant-key` each `correct=no` (`guard=no`, `expect_guard=yes`). Bounded
`10 × 17/17 = 10.0000` against `7.6471`. The population is re-derived at the measured rev
(`population=20 readers=13 guarded=13 unguarded=0`), so the stricter rule did not reclassify a real
gate file. **This seat did not execute the counter**; the line is the receipt's.

**Boundaries.** (1) Both scores are the round's, not this seat's; neither counter was run here and no
scenario was re-created. (2) The measured rev's instrument bytes are not the bytes the declaration
names: `c1-r70-real-children.py` is `b1785f38…` at `5144a6b5` and `b3a6f131…` at `5adba5a9`;
`c2-r70-carriers.py` is `87ca4664…` at `5144a6b5` and `d868ae33…` at `5adba5a9`;
`c1-r70-landing-controls.py` is `71a7b6c4…` at both (re-derived with `git show REV:path | sha256sum`).
The declaration's sentence "The scored instruments are committed at 5144a6b5" and the receipt's
measured content therefore describe different bytes for two of the three instruments; the receipt
measures the later bytes. Reported, not reconciled — that sentence is frozen and the L1 owns it.
(3) The declaration's Not-claimed list stands verbatim and is not widened: no universal fault
coverage; three scenarios do not exhaust the kill-credit hazards; the fixture lane is not the lane's
real landing instrument; four carrier shapes are not all remaining Python shapes; the dominance rule is
a bounded syntactic approximation; runtime behaviour of the extracted instruments is not measured; no
desktop, compositor, session, service or package state was probed; no `[x]`, promotion or axis
retirement is claimed. (4) Freeze-order evidence for this lane is not `quality/check-freeze-order.py`
(M70-3): the lane's own evidence is the declaration commit preceding the instrument commit and the
measurement commit — `bc18399b` 23:27:05 < `5144a6b5` 23:29:46 < `5adba5a9` 23:33:01 (committer
timestamps, `git log --format='%h %cI'`). (5) A production lesson for this round already exists on disk
when this draft was written — `corpus/lessons/round-70.md`, authored by the L1, untracked — and it fixes
the register ids this file follows (S439 expressions, S440 simple_stmts, subprocess and ast refused).
This file is the seat-level lesson: it keeps the measurements, the four assigned mistakes and the
byte-level checks of that Gate that the production file does not carry.

## Mistakes

| mistake | class | evidence | captured-by | fix and the failure it can now show |
|---|---|---|---|---|
| **M70-1** the round-69 LOG bullets were inserted into two filed entries | record order: an append-only insertion not anchored to its own round | The 10-line block (`Critic closures (R69CriticClaims, B1-B11) …`, `Final measurement at 759c9d7b …`, `Wave settlement: 12 seats dispatched …`) appears at `LOG.md:3257-3266` (inside `### Round 67`, which starts at `LOG.md:3220`), at `LOG.md:3314-3323` (inside `## Round 68 (2026-11-03)`, which starts at `LOG.md:3273`) and at `LOG.md:3396-3405` (`### Round 69`, `LOG.md:3339`). All three copies from `139f4801` (`git log -S 'Wave settlement: 12 seats dispatched' -- LOG.md` returns only that commit). No prior byte was deleted; two filed entries were altered and r69 facts misattributed to r67/r68. Re-derived here with one command: `awk '/^#+ Round/{r=$0} /Wave settlement: 12 seats dispatched/{printf "%d \| %s\n", NR, r}' LOG.md` prints `3266 \| ### Round 67 …`, `3323 \| ## Round 68 …`, `3405 \| ### Round 69 …` | none — no rule said an append-only edit must be anchored to its own round heading | Rule: an append-only insertion is anchored to the round whose heading encloses it; a block found under another round's heading is misattributed even when no prior byte was deleted, and is repaired append-only (name the misplaced copies, delete nothing). One-command sweep: the `awk` above; any hit whose printed heading is not the block's own round is a defect, and the fix is an erratum in the *current* round's entry. Failure it can now show: a round-70 LOG entry pasted into the r68 section prints `## Round 68 …` for its own bullet — the same command catches it before the commit lands |
| **M70-2** a round commit was left unenumerated | enumeration completeness: the landed table and the revision range disagree | `git rev-list --count 04093b83f73a841117d3b31dbb2a6063f4f2a454..9d91f7f6f5c603bdc19cf455ce6f413c5990d744` = 19, while the report's Landed-changes table (`.ufo/reports/round-69/mado.md:69-86`) enumerates 18 rows (re-counted here: `awk 'NR>=69 && NR<=86 && /^\|/' … \| wc -l` = 18). The missing revision is `b9b70a09` ("round-69: final measured content and the mutation-battery closure in the records", committer `2026-11-03T23:01:21-03:00`, 8 files: `cross-set-r69.txt`, `final-gates-r69.txt`, `landing-counters-r69.txt`, `measurement-final-r69.txt`, `report-draft.md`, `LOG.md`, `SCORECARD.md`, `corpus/lessons/round-69.md`). `grep -c b9b70a09 LOG.md` = 0 and `grep -c b9b70a09 SCORECARD.md` = 0 at the lane head. | none — the report's Landed-changes table was never checked against the revision range | Rule: the table is complete iff its enumerated revisions are co-extensive with `git rev-list <base>..<tip>` — count equality is necessary, set equality is the check. Commands: `git rev-list --count BASE..TIP` must equal the table's data-row count, and `comm -3 <(git rev-list BASE..TIP \| cut -c1-12 \| sort) <(grep -oE '[0-9a-f]{12}' REPORT \| sort -u)` must print nothing. Failure it can now show: a commit like `b9b70a09` leaves a non-empty `comm` line and a one-count surplus, even when every enumerated row is correct |
| **M70-3** the round-69 freeze-order evidence was misdescribed | evidence misdescription: the named check cannot see this lane's freeze file | `quality/check-freeze-order.py:36` hardcodes `REQUIRED = ("claims-frozen.md", "registration.md")`; the lane submits `.ufo/waves/round-N/claims-declaration-rN.md`. The committed r69 receipt reads `MADO_FREEZE_ORDER: SETUP work_not_a_directory` (`.ufo/waves/round-69/final-gates-r69.txt:17`), not `reason=no_freeze`, and the report's r68 line was reused for r69. | none — the report named a check it had not matched to the lane's file names | Rule: report the lane's own freeze-order evidence, which is the declaration commit preceding the first instrument commit and the measurement: `git log --format='%h %cI' -1 -- .ufo/waves/round-70/claims-declaration-r70.md` (`bc18399b`, `2026-11-03T23:27:05-03:00`) < `git log --format='%h %cI' -1 5144a6b5` (`23:29:46`) < `git log --format='%h %cI' -1 5adba5a9` (`23:33:01`). Round 70 satisfies it. Failure it can now show: an instruments commit that precedes the declaration commit inverts the comparison; and a `SETUP work_not_a_directory` line is never again printed as this lane's freeze result. The `check-freeze-order.py` repair itself (make the required set a parameter and extend its own selftest fixtures, which construct `claims-frozen.md`/`registration.md`) is a production-code change and is routed, not made, by this seat |
| **M70-4** the round-69 `w1-results.json` carried no settlement status | missing field: a settled/dead claim inferred from non-empty output | `.ufo/waves/round-69/w1-results.json` `results[]` rows carry exactly `["agent","name","note","output"]` (`jq -c '[.results[] \| keys] \| unique'` returns one shape) over 12 rows; "12 settled, no dead seats" was inferred from 12 non-empty `output` values. | none — no schema field was required, so the inference was invisible | Rule: the wave's own results file states `status: settled` or `status: dead` on every `results[]` row, and a report that reasons from non-empty output must say "inferred". Round 70: `.ufo/waves/round-70/w1-results.json` does not exist at scribe time (`ls` → `No such file or directory`), so this is reported only; the fix lands when the L1 writes that file, and a file without the field keeps the claim inferred |

**Fixed this round versus reported only.** None of M70-1..M70-4 is repaired by bytes this seat may
write: `LOG.md` and `SCORECARD.md` are fleet-root tracked files, and the round report and
`w1-results.json` are the L1's at integration. What this round adds is a re-derivation command per
mistake (`awk` sweep for M70-1, `rev-list`/`comm` for M70-2, the commit-time comparison for M70-3, the
`status` field for M70-4) and QUALITY 112/113 so the first two are checkable by a non-author. M70-3's
check repair is routed as a production change, not drafted here.

**One further provenance fact, reported not learned as a new mistake.** `9508e878` ("create the
per-scenario scratch dir in the C1 counter; predicate unchanged", 23:32:33) and `5adba5a9` ("label the
candidate and base control-leg lines … observability only", 23:33:01) both edit scored instruments
after the freeze commit `bc18399b`. Both are declared predicate-preserving and both precede the
measurement; this seat did not audit the diffs, and records only that the measured bytes differ from
the freeze-time instrument commit (see § Outcome and boundaries (2)).

## Gate

Access date for all three URLs: **2026-11-04** (local `2026-11-03T23:32:49-03:00`; UTC
`2026-11-04T02:32:49Z`). Each URL was fetched three times with `curl -fsSL`, each retry independent;
the three downloads per URL are byte-identical (one distinct sha256 per URL). Line numbers are from
the fetched bytes (`wc -l`: 1622 / 2407 / 2698).

**ADMIT — S439, CPython `Doc/reference/expressions.rst` @ `v3.14.8`.**
URL `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/expressions.rst`;
92,034 bytes; 2,407 lines; sha256 `e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a`;
tag object `992560c2cc62d47b308cec662feb485456847931` peeled to commit
`8e6e75d9102e39bed2a2b279203a396741180f12` (`git ls-remote https://github.com/python/cpython 'refs/tags/v3.14.8*'`).
Located quote, 8 words, at `expressions.rst:514`: "A double asterisk ``**`` denotes
:dfn:`dictionary unpacking`." Second locator, 13 words, at `:1161-1162`: "Subscriptions may also be
used as targets in assignment or deletion statements." Reason to admit: it is the grammar the C2
classifier reads — a `**` operand is unpacked into the mapping and a subscript store writes under the
key expression's value, which is what makes a splat-carried guard and a literal-name-key guard real
carriers rather than mentions. It does not establish that any file is guarded.

**REJECT — S441, CPython `Doc/library/ast.rst` @ `v3.14.8` (this seat's third row; rejected by the
L1's round-70 Gate on discipline, not bytes).**
URL `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/ast.rst`; 92,619 bytes;
2,698 lines; sha256 `9908f4f029c3258bdfb9ffa6af69d2bca5bd17ff2f175f92a71303d43699ab85`; same tag
object/peeled commit as above. Located quote, 10 words, at `ast.rst:449-450`: "with a ``None`` at the
corresponding position in ``keys``". Second locator, 14 words, at `:761-763`: "``ctx`` is
:class:`Load`, :class:`Store` or :class:`Del` according to the action performed with the subscript".
Reason this seat drafted it: it is the node-shape ground for the classifier that replaces text matching — a dict
unpack keeps `None` in `keys` and a subscript store is the same node class as a load, so the
classification must read fields, not spelling. I opened it for a distinct fact (not a second quote of
expressions): the `None`-key marker and the `ctx` discriminant are what the counter's `isinstance`
branches actually test (`quality/counters/c2-r70-carriers.py:167-176,279-330`).

The L1's reason for refusing it is discipline, not bytes: the page documents the node vocabulary the
classifier reads, not the runtime carrier semantics the claim rests on, and the named flip is a future
claim whose subject is the classifier's own grammar. This seat keeps the fetched row as **S441** with
`status: rejected` in `draft/corpus/SOURCES-rows.txt` so a later round does not re-fetch it.

**REJECT — a new registry row for CPython `Doc/library/subprocess.rst` @ `v3.14.8` (this seat's rule;
the L1's Gate also refuses it and substitutes held S435, GNU Bash 5.3 § Exit Status, as the C1 ground).**
The URL already has a row: `corpus/SOURCES.md:120` **S108**, tier A, status `mined`, scope "the command
parameter … is `args`", anchor `subprocess.rst` 61,603 B sha256 `05cd782c…`, `run` :38-43, `Popen`
:359-366, `Popen.args` :898-900. A second row for the same URL in a different scope is the census's
W04 "duplicate url … across scopes" (`scripts/sources-census.sh:33,645`) — warning-only, but a new
warning on a lane whose census is otherwise clean (`validate` exit 0 with the pre-existing W04 set
unchanged). Measured byte facts, recorded for the register but not appended: 61,603 B, 1,622 lines,
sha256 `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd` (identical to S108's
recorded digest, so the tag has not moved), three byte-identical fetches; located quote, 15 words, at
`subprocess.rst:141-142`: "A negative value ``-N`` indicates that the child was terminated by signal
``N`` (POSIX only)."; the `getstatusoutput` examples at `:1503-1510` report `1` (ordinary failure),
`127` (missing program) and `-15` (killed child). **Flip condition:** the rejection flips when either
(a) the L1 or operator allows the registry's in-place cell set to include `anchor`, so S108's anchor
can be re-anchored to the return-code lines, or (b) the round accepts one W04 to give the C1 entry a
pinnable row. (b) is not academic: `quality/check-anchor-cover.py:136-155` derives the row's file name
from the **last** URL in the source cell (for S108 that is `Lib/subprocess.py`, so the name is
`subprocess.py`) and then requires `subprocess.py:NNN` inside the anchor cell; S108's anchor carries
bare `:38-43` locators and no `subprocess.py:` occurrence, so a pin citing S108 reports
`locators=none verdict=MISS reason=no-cover` (replica of the check's own `occurrences()` run on S108's
cells: `name=subprocess.py occurrences=[]`). The ready-to-adopt row for case (b) is
`draft/corpus/SOURCES-row-subprocess-CONFLICT.txt` (S442, 11 cells verified; its teaches cell carries
`supersedes S108` so the row is E04-clean if a later round takes the flip); it is deliberately not in
`SOURCES-rows.txt`.

**Register state at integration (measured by this seat, 2026-11-04).** The L1's production lesson
`corpus/lessons/round-70.md` (§ Gate) assigns **S439 = expressions.rst** and **S440 = simple_stmts.rst**,
and refuses both `subprocess.rst` and `ast.rst`. This seat checked that Gate against the fetched bytes:
- S440 is byte-correct and its quote location is exact: 41,375 bytes, 1,079 lines, sha256
  `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`, three byte-identical fetches;
  "If the target is a subscription: The primary expression in the reference is evaluated. Next, the
  subscript expression is evaluated." sits at `simple_stmts.rst:190-192` exactly as cited.
- S439's quote is mislocated in that Gate: it cites `expressions.rst:509-512`, but 509-513 are a blank
  line plus `.. index::` with two index entries; the quoted sentence begins at `:514` and ends at
  `:517` (numbering re-derived with `awk 'NR>=505 && NR<=520'`). Reported, not edited — the production
  file is the L1's. The row drafted here anchors `:514`, so the register bytes will be right even
  though the lesson's locator is not.
- The L1's S439 anchor must cover the subscription ranges (`1096-1140`, `1161-1166`) or the C2 entry's
  pins at `expressions.rst:1137` and `:1161` miss check-107; this seat's row provides that coverage, and
  `R70ScribeEntryC2` independently re-ran the check's logic against it (`CHECK107_SIM rows=5
  covered=5`).

**Register bookkeeping: nothing applied, and this round needs nothing.** The L1 substituted the held
S435 (GNU Bash 5.3 § Exit Status) for C1, so S108 keeps its cells and no `used-by` change is logged. If
a later round takes the S442 flip, S108's `used-by` still stays unchanged and that lesson cites S442.
No row id is written into the declaration by this seat; `corpus/SOURCES.md` is untouched.
