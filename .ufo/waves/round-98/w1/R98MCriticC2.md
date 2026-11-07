# R98MCriticC2 - C2 falsification (round 98, w1)

Seat: critic, C2 (SOURCES read-back gate + its counter). Base revision
`35f3ce808788b11c063309b1b5ad0192754795ea`. Every number below is measured on a
`git archive 35f3ce80` extraction (`$S/base`), not on the working tree: the working tree already
carries an **uncommitted** repair of `corpus/SOURCES.md` (18 rows, `git status` = ` M`), so a
measurement taken there would score the repair as if it were the base.

Instruments (all in scratch, none committed): `myreadback.py` (my own parser, written from the
11-column row shape and the `source:` lines, independent of any counter), `refgate.py` (a literal
implementation of the declared R1-R6, used only to expose what the sentences do), `fixtures.py`,
`discrimination.py`, `donothing.py`. The candidate is never run; I judge the declaration.

Verdict in one line: the 23-pair count is arithmetically right, but the declared rule set cannot
report `findings=0` at `--rev` (R2 fires 21 times on pre-existing cells) and the counter's
`repaired` leg is vacuous under three cheap no-work shapes. Two sentences must change before the
freeze; four more should.

## 1. The 23 pairs, re-derived (item 1)

My parser reproduces **exactly 23** (row, entry) pairs at base, and the set is **equal** to the
repair map's 23 distinct pairs (`only mine = []`, `only theirs = []`). The count is stable under
both readings of "frontmatter": all `source:` lines anywhere (23 pairs) and the frontmatter block
only (23 pairs; 3 further body `source:` matches are the same three pairs).

| # | row | status | entry | verdict |
|---|---|---|---|---|
| 1 | S030 | rejected | hyprland-config-era-r12.md | **rule should not require** (entry disowns it, see below) |
| 2 | S132 | queued | terminal-trees-r23.md | **rule should not require** (entry says it supports nothing) |
| 3 | S457 | mined | bar-footprint-composition-r80.md | genuine |
| 4 | S459 | mined | bar-footprint-composition-r80.md | genuine |
| 5 | S460 | mined | bar-footprint-allocation-r82.md | genuine |
| 6 | S460 | mined | bar-footprint-rounding-auto-r81.md | genuine |
| 7 | S464 | mined | bar-footprint-allocation-r82.md | genuine |
| 8 | S464 | mined | bar-footprint-rounding-auto-r81.md | genuine |
| 9 | S464 | mined | bar-footprint-surface-band-r83.md | genuine |
| 10 | S465 | mined | bar-footprint-composition-r80.md | genuine |
| 11 | S466 | mined | bar-footprint-composition-r80.md | genuine |
| 12 | S470 | mined | bar-footprint-allocation-r82.md | genuine |
| 13 | S470 | mined | bar-footprint-rounding-auto-r81.md | genuine |
| 14 | S470 | mined | bar-footprint-surface-band-r83.md | genuine |
| 15 | S481 | mined | bar-footprint-surface-band-r83.md | genuine |
| 16 | S484 | mined | bar-footprint-surface-band-r83.md | genuine |
| 17 | S485 | mined | bar-footprint-surface-band-r83.md | genuine |
| 18 | S493 | mined | mako-fields-containment-r88.md | genuine |
| 19 | S501 | mined | portal-keyfile-bytes-r93.md | genuine |
| 20 | S502 | mined | portal-keyfile-bytes-r93.md | genuine |
| 21 | S511 | mined | mime-magic-sniff-r95.md | genuine |
| 22 | S512 | mined | mime-magic-sniff-r95.md | genuine |
| 23 | S517 | mined | mime-magic-sniff-r95.md | genuine citation of the row's locator status (support is S523) |

So: **21 genuine, 2 the rule should not require**. The two are not hypothetical:

- **S132**: the entry's `source:` line ends `... S132 stays queued and supports nothing.` The row
  is `queued`, used-by `U+2014`. Adding `corpus/knowledge/terminal-trees-r23.md` to S132's used-by
  (what the repair map does) makes the registry assert a use the entry's own sentence denies, and
  makes a `queued` row carry a used-by path - a shape the contract's status gloss ("mined (cited by
  >=1 path in used-by)") reads as mined while the status says queued. No E-code catches it.
- **S030**: the entry's round-13 erratum says, verbatim: `read every S030 citation in this entry
  (header and line 67) as **S017** ... This mapping preserves the old bytes and their rejection.`
  S030 is `rejected`; S017's used-by already names the entry. Adding S030 to the entry's used-by
  makes the registry claim the entry uses both S017 and S030 for the same claim, while the entry
  says every S030 occurrence resolves to S017 and not to an admitted S030. That is false
  provenance written by a read-back gate.

S517 is a third, weaker case: the entry cites it only to record that `the spec's registered S517
locator now answers 301 and the ... body is the redirect stub`; its content support is S523. The
used-by addition is defensible (the entry does cite the row), but it records a locator status, not
a use.

Not defects, checked: a row cited in an entry's **body** but not its `source:` line is not counted
by a frontmatter rule (fixture P5 passes; the 3 body `source:` matches are the same 3 pairs, so a
body scan changes the pair count by 0 but the **finding** count by +3 if the gate emits per
occurrence). A lesson-only used-by path, a `rejected` row with used-by `U+2014`, an ASCII-hyphen used-by, and a
row cited by a lesson all pass (fixtures P1-P4, P1b). A `source:` line **after** the frontmatter
block is the scope test: the frontmatter reading passes it (P5b `front`), the all-`source:`-lines
reading fires R4 on it (P5b `all`) - so the declaration's word "frontmatter" must be pinned, and
the 3 committed body `source:` lines are the reason.

## 2. Attacking the rules (item 2)

Fixtures: 14 pass-shaped, 18 fail-shaped, each run under both scopes (`front` = frontmatter block,
`all` = every `source:` line). Of the 64 runs (32 fixtures x 2 scopes), 14 mismatch: 11 on six
fail-shaped fixtures (F8, F9, F10, F11, F13, F15) and 3 on two pass-shaped fixtures (P5b under
`all`, P12 under both). Each mismatch below is a rule defect, with its real-registry case count:

**F1 - R2 contradicts the predicate's own `findings=0` (blocking).** R2 ("a `used-by` path not
under `corpus/`") fires **21 times** on the committed registry, on 19 `mined` rows, all paths that
exist: S096 (2), S173, S174, S178-S182, S184, S185 (2), S332-S339, S482. The literal gate on the
repaired tree prints `rows=462 entries=118 findings=21` (R4=0, R2=21). The predicate's (ii) says
"at `--rev` the gate reports `findings=0` over the committed registry" - unreachable. The contract
does say used-by names "knowledge entries or lessons", so R2 is *right* and the registry has 21
pre-existing violations; but the round declares a 23-cell repair, not 44. Fixture
`F10-real-outside-cell` reproduces it with one cell.

**F2 - R4 counts disowned citations.** Fixtures `F8-negative-cite` (the S132 shape) and
`F9-rejected-cite` (the S030 shape) fire R4 on citations the entry's own text disowns. The rule has
no status test: it fires on a `rejected` and a `queued` row exactly as on a `mined` one.

**F3 - the frontmatter scope loses citations (false negative).** `F11-yaml-list-unack`: an entry
whose frontmatter is `source:` followed by indented `  - S001` items. A frontmatter-only parser that
does not join continuation items reads `source:` as empty and reports 0; the literal gate does
exactly that (`front` scope: 0 findings, expected 1 R4). Three committed entries use this form
(`animation-table-r26.md`, `mutation-testing-r28.md`, `workspace-rules-r27.md`), all currently
acknowledged, so the defect is latent - strip S175 from S175's used-by and the gate stays silent.
`F13-wrapped-id`: an id on a wrapped continuation line is missed in both scopes (0 findings,
expected 1). Three committed entries wrap their `source:` line (`windows-display-topology-r61.md`,
`windows-dpi-awareness-metrics-r60.md`, `windows-permonitor-dpi-r58.md`).

**F4 - an id-looking token inside a path counts as a citation (false positive).**
`F15-path-token`: `source: own-work receipt .ufo/waves/round-37/fetch/S213.receipt.txt` produces
`R4 S213`. The committed registry has 16 such path-context tokens; 12 are acknowledged and the 4
unacknowledged are already in the 23 from other lines, so today it adds 0 findings - a future
receipt path would add one.

**F5 - path spelling (false positive).** `P12-dot-path`: used-by `./corpus/knowledge/a.md` (a legal
repo-relative spelling, the path exists) produces `R2` (not `corpus/`-prefixed) *and* `R4` (string
compare fails). No committed cell uses this spelling today. Related: `P11-dash-token` shows the
`U+2014` token beside a real path must be skipped, not treated as a path (the literal gate handles
it; a naive split does not).

**F6 - R2, R5, R6 are never exercised by the predicate.** The predicate plants R4, R1 and R3 only.
A gate implementing R1+R3+R4 and omitting R2/R5/R6 passes every leg - and R2 is the rule that
fires on the real registry, so the only gate that can pass (ii) is one that omits R2. See section 3.

Rules that are clean at base: R1 (no recheck cell contains `/` or ends `.md`), R3 (all used-by paths
exist; census E11 clean), R6 (no duplicate id). `rows=462`, `entries=118` (files; 192 `source:`
lines - the two counts must be pinned, see section 4).

## 3. Counter discrimination (item 3)

Planted copies built from the **repaired** tree, one defect each; gates: the literal gate, an
always-clean stub, a count-only decoy (prints one `R1 S001` finding for any input), an R1-only
gate. Verdicts are per rule (the real registry always carries the 21 R2 findings, so "exactly one
finding total" is impossible; the counter must count per rule).

| plant | expect | literal gate | clean stub | count-only decoy | R1-only gate |
|---|---|---|---|---|---|
| C-R1 recheck path | R1 S464 | exact | missed | **count-only, wrong id S001** | exact |
| C-R2 used-by tool | R2 S464 | count=22 | missed | missed | missed |
| C-R3 dangling used-by | R3 S464 | exact | missed | missed | missed |
| C-R4 strip one path | R4 S464 | exact | missed | missed | **missed** |
| C-R5 missing row | R5 S999 | exact | missed | missed | missed |
| C-R6 duplicate id | R6 S464 | exact | missed | missed | missed |

Answers to the three questions:

- **Does the always-clean stub get caught?** Yes, by any per-rule check - but only if the check is
  exact. The count-only decoy **passes the C-R1 leg under a count-only check** (one R1 finding, id
  S001): the counter must compare rule **and** id **and** that the detail names the planted entry,
  not just `len(findings) == 1`. It must also check the exit code (1 on a planted copy, 0 on the
  clean registry); a gate that prints the right line and exits 0 passes a stdout-only check.
- **Does an R1-only gate pass the planted R4?** No: it prints 0 on C-R4 and is caught. It does pass
  (ii) and (iii) (the repaired registry has no R1 defect, and (iii) is the counter's own pass), so
  the planted R4 leg is the only thing that catches it - load-bearing, keep it. But the same
  argument shows R2/R5/R6 are unguarded: plant them too (cheap), or a gate that omits them is
  TARGET_MET.
- **Is `repaired == base_mismatches` vacuous at 0?** Yes. With `--base-rev` equal to the repaired
  tip, `base_mismatches=0` and `repaired=0`, and `0 == 0` passes (measured, M5). Worse, the
  sentence's direction is ambiguous: "every base mismatch's **entry** now names the **row** back"
  is already true at base (that is why the pair exists). The repair is the **row** naming the
  **entry**. Under the pair-disappeared reading, three no-work shapes pass (section 4).

## 4. The do-nothing control (item 4)

Measured on the base extraction (23 pairs), gate = literal frontmatter rule, `rep_row` = "row's
used-by now contains the entry", `rep_pair` = "the pair is no longer an R4 finding", `added` =
used-by paths added versus base:

| tree | gate R4 | rep_row | rep_pair | added | rows | entries |
|---|---|---|---|---|---|---|
| M0 base | 23 | 0 | 0 | 0 | 462 | 118 |
| M1 delete every `source:` line in the 23 entries | **0** | 0 | **23** | 0 | 462 | 118 |
| M2 shotgun: every row acknowledges every mismatch entry | **0** | **23** | **23** | **4095** | 462 | 118 |
| M3 reword S464 -> S481 in one entry | 22 | 0 | **1** | 0 | 462 | 118 |
| M4 the real repair (working tree) | 0 | 23 | 23 | 23 | 462 | 118 |
| M6 delete the 5 entries that carry the 23 pairs | **0** | 0 | **23** | 0 | 462 | **109** |

Loopholes, each with the sentence that closes it:

- **L1 delete the citations.** `findings=0`, `rep_pair=23`. Closed by: "a pair whose entry's
  `source:` line no longer names the row scores **unrepaired**; a deleted citation is not a repair,
  and the per-entry citation set at `--rev` is a superset of the base set."
- **L2 delete the entries.** `entries` drops 118 -> 109; the counter's (ii) compares the gate's
  count to its own parse, so both read 109 and it passes. Closed by: "the set of entry paths at
  `--rev` equals the set at `--base-rev`."
- **L3 reword to an already-acknowledged row.** The pair disappears, `rep_pair=1`. Closed by the
  row->entry definition (L1's sentence covers it).
- **L4 shotgun.** Both definitions pass; only the added-path count catches it (4095 vs 23). Closed
  by: "the number of used-by paths added at `--rev` equals `repaired`, and each added path is
  exactly the mismatch entry."
- **L5 `base_mismatches = 0`.** Closed by: "`--expect-base-mismatches 23` (or 21, see section 5) is
  pinned; the counter refuses when `base_mismatches != expect` or when `--base-rev == --rev`."
- **L6 dirty tree.** The repair is currently uncommitted; a counter that runs the gate on the
  working tree reports TARGET_MET before the repair lands. Closed by: "the gate runs on an
  extracted `--rev` tree whose `corpus/SOURCES.md` sha256 equals `git show <rev>:corpus/SOURCES.md`."

The do-nothing control as declared ("a gate that prints findings=0 for every input passes (ii) but
is caught by (iv)") is true but incomplete: it only covers a *stub gate*, not a *no-work repair*.
The four no-work shapes above are the ones the control must name.

## 5. The before-number (item 5)

My count is **23**, exactly the declaration's, and the pair set equals the repair map's. So the
number is right **as a count of unacknowledged citations**. It is not right as a count of defects:
2 of the 23 (S030, S132) are citations the entry's own bytes disown, and the repair map writes
used-by acknowledgements for them. The honest numbers are:

- 23 unacknowledged citations (the rule's firing set, and what `base_mismatches` will print);
- 21 genuine read-back defects (20 support citations + S517's locator-status citation);
- 2 citations the rule should not require (S030, S132) - a status-aware R4 (`status == mined`)
  drops them without losing a genuine pair, because S030's support is already acknowledged by S017
  and S132 supports nothing.

Two further count corrections:

- **The gate's total at base is 44, not 23** (23 R4 + 21 R2). The declaration's "the 23 defects it
  finds" describes one rule's output, not the gate's.
- **"the 23-cell repair" is 18 cells / 23 paths.** The working-tree diff touches 18 rows
  (18 insertions, 18 deletions) and adds 23 paths.

The repair map is not an old->new log and must not be logged verbatim: 3 of its 26 items are
grouped items whose `old` does not match the base cell; 8 of its 26 `new` values do not match the
final cell; applied sequentially, 18 apply and 8 fail (5 old-mismatch, 3 grouped). The contract
(rule 2) requires an old->new entry per cell in the round lesson; derive it from base -> final (18
cells), not from the map.

## Smallest safe corrections, ranked

1. **R2 must not be a finding.** Either emit it as `SOURCES_READBACK: WARN R2 ...` (not counted in
   `findings`) or repair the 21 cells too (then the before-number is 44 and the log covers 39
   cells). Without this, (ii) is unreachable and TARGET_MET is impossible by construction.
2. **R4 must be status-aware or the declaration must say used-by records citations including
   disowned ones.** Recommended: `R4` fires only for rows with `status: mined`; the before-number
   becomes 21; S030/S132 are recorded in the lesson with their disowning sentences quoted and no
   used-by is written. If 23 is kept, the declaration must add: "a used-by path records that the
   entry cites the row, including a citation the entry's erratum maps elsewhere; it is not a claim
   of support."
3. **Pin the frontmatter scope and the counts**: "the `source:` entries of the frontmatter block,
   including indented `  - Sxxx` continuation items and wrapped lines, and no `source:` line after
   the block; `rows` = 11-column rows (462), `entries` = `corpus/knowledge/*.md` files (118), one
   finding per (row, entry) pair, not per occurrence."
3b. **The gate's `--selftest` must cover the six rules and the three parser shapes** (YAML list,
   wrapped line, id-in-path); `N >= 10` is satisfiable by ten trivial checks that leave F3-F5
   unguarded.
4. **Id-token context and path normalization**: an id counts only when not preceded by `/` and not
   followed by `.`/`-`/`_`; used-by paths are compared after `posixpath.normpath`, and `-` and
   `U+2014` are empty.
5. **Counter sentences** (add before the freeze): pin `--expect-base-mismatches`; require
   `--base-rev != --rev`; define `repaired` as **row -> entry**; pin the entry-path set and the
   per-entry citation set (superset of base); require `added_paths == repaired`; plant R2, R5, R6
   as well as R1/R3/R4; each planted copy must yield exactly one finding of the planted rule with
   the planted id and a detail naming the planted entry, and exit 1; run a committed stub and
   require `stub_flagged=1`; run the gate on an extracted `--rev` tree pinned to
   `git show <rev>:corpus/SOURCES.md`.
6. **Repair log**: derive old->new from base -> final (18 cells, 23 paths); do not log the map.

## Impacted axes

C2 (operability) only: the gate's rule set (R2, R4), the counter's (ii)/(iii)/(iv) legs, the
before-number (23 -> 21 if R4 becomes status-aware), and the do-nothing control's scope. C1 is
untouched. No lane artifact outside this report and its receipt was written; no git/jj mutation was
run; no host application was started.

## What survives

The 23-pair set is correct and reproducible; the base gate is absent (`git cat-file -e` rc 128);
the census still validates the repaired registry (exit 0; W01 S277 and the W04 set only); the
literal gate is exact on R1/R3/R4/R5/R6 and on 12 of 14 pass-shaped fixtures (P12 is the exception,
P5b only under `all`); the planted-copy leg catches an R1-only gate. The defects are in the rule set's reachability (R2), its semantics
(R4), its parser scope (F3/F4/F5), and the counter's vacuity and discrimination (sections 3-4).
