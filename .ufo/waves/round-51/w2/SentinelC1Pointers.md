# SentinelC1Pointers — round 51, w2: pointer audit of `quality/tool-ledger.md`

Lane `mado-shokunin`; freeze revision `56026fcb9800370ae04bc65952a6567181c398d0`; round base
`6ca8c559a4a3d6d361101592116eea2bc7452437`. Surface audited: the accountability-pointer clause of the frozen
PRED-C1-r51 sentence only. Advisory findings; no lane file edited, no frozen predicate or lane file changed.

## Verdict under the frozen sentence

> "…each such file appears exactly once in `quality/tool-ledger.md` with a non-empty description and an
> accountability pointer naming an existing repo file that contains the file's basename"

**PASS.** At the freeze revision all 82 ledger rows dereference and name their instrument: 82 rows for 82
population files, `bad_pointer=0`, 0 rows missing, 0 rows outside the population, 0 pointer tokens failing to
exist at the revision, 0 rows whose pointer file lacks the basename (checker semantics), and 0 rows where only
the counter's weaker substring test would have passed. The 79 rows that carry a `:<line>` suffix all name the
basename on the cited line — no stale annotations. Nothing here falsifies C1; the claim's pointer clause holds
as literally written.

Frozen command reproduced at the freeze revision (scratch clone, no lane writes):

```
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=56026fcb9800370ae04bc65952a6567181c398d0
exit=0
```

Pointer census: 12 distinct pointer files, 69 distinct tokens; 10 tokens reused (max `PROVINCE.md:20`, 4 rows).
Classes measured: `SCORECARD.md` 42, `PROVINCE.md` 20, `corpus/lessons/*` 9, `.ufo/waves/round-N/registration.md`
8, `corpus/QUALITY.md` 3. 62/82 rows (75.6 %) resolve into the two mutable aggregate documents. The header
declares a `corpus/knowledge/*.md` class that no row uses.

## Findings (advisory)

**1. 3/82 rows resolve only because of round-51 registration prose, and that is the scored claim itself.**
The checker and both C1/C2 counters (ledger lines 117–119) point at `.ufo/waves/round-51/registration.md`. The
mentions are the predicate sentence (line 9, the counter's obligation) and "Frozen implementation" (lines 11,
17). `quality/tool-ledger.md`, the checker, both counters and that registration are all first added by the
**same commit** `56026fcb`; the three pointers cannot resolve at any earlier revision. Outside `.ufo/`, only the
instruments' own files and the ledger name them — no `PROVINCE.md`, `SCORECARD.md`, knowledge or criterion text
does. So the document-level cycle is: registration declares the predicate → instruments implement/score it →
ledger certifies the instruments → the ledger's witness for the instruments is the registration. Literally
compliant, but self-certifying; this is the class the seat was asked to isolate.

**2. No file-level circular pointer exists.** No pointer target is a population instrument, so the
instrument→witness graph is a star into documents. The available cycle (counter names the checker as
`DEFAULT_CHECKER`; the checker reads the ledger) is broken only because the ledger points outside the
population.

**3. The pointer clause is vacuous under self-reference (medium).** `quality/tool-ledger.md` is itself a blob
whose bytes contain every row's basename. Repointing **all 82 rows** at it yields, on the freeze code, checker
`bad_pointer=0 verdict=TARGET_MET` exit 0 and the frozen counter `bad_pointer=0 verdict=TARGET_MET` exit 0. The
delivered ledger does not do this, but the clause can never distinguish a genuine witness from the ledger's own
text.

**4. Three implementation defects in the pointer test (low, reproduced).** (i) The checker's negative lookahead
`(?![A-Za-z0-9_-])` omits `.`, so a target containing only `check-tool-ledger.py.orig` counts as naming the
instrument — contradicting its "as a name, not as a fragment of a longer filename" docstring. (ii) `:<line>` is
stripped by both implementations, so `SCORECARD.md:999999` passes; anchors are unenforced (they are, today, all
accurate). (iii) The counter's own measurement is `base.encode() in bytes` (substring) while the checker is
name-bounded: for a target containing only `xcheck-tool-ledger.py` the counter prints `bad_pointer=0` and the
checker `bad_pointer=1`; the final MISS comes only from the `max` agreement clause, so the counter's
"independent" pointer metric is weaker than the checker's and is saved only by that clause.

**5. The ledger header overstates its own evidence (low).** "Five superseded v1 counters have no lane-level
document naming them; their registration is the only tracked file that does" is false for all five: each v2
successor names its v1 predecessor with the supersession reason (e.g. `quality/counters/c1-r40-live-v2.py:4`,
`c1-r44-geometry-states-v2.py:5`, `c2-r45-monitor-entry-v2.py:5`, and the same for `c2-r40-forms-entry.py`,
`c1-r45-monitors.py`). Choosing the registration avoided instrument→instrument edges; the wording presents a
choice as a necessity.

**Severity:** medium (3); low–medium (1); low (4, 5). All are limits of the frozen rule or of supporting prose;
none makes the frozen pointer sentence false.

## Smallest remediations (future amendment, not applied)

Reject the ledger itself and the row's own file as pointer tokens (closes 3); require a non-`.ufo` target for
`quality/` instruments (closes 1 for future rows); guard `.` in the lookahead (4i); validate a present `:<line>`
suffix (4ii); reuse the checker's `names_basename` in the counter or drop the independence claim (4iii); point
the five superseded rows at their v2 successors or reword the header (5).

## Evidence / reproduction

- Audit: `audit.py` (read-only `git ls-tree`/`git show`), raw `pointer-audit.json`, per-row `pointer-census.md`.
- Freeze: `receipts/freeze-c1-command.txt`, `receipts/freeze-checker.txt`.
- Witness provenance: `receipts/witness-grep.txt` (non-`.ufo` greps, same-commit landing, registration lines 9/11/15/17).
- Fixtures: `receipts/fixture-allself.txt`, `receipts/fixture-allself-counter.txt`,
  `receipts/fixture-dotted.txt`, `receipts/fixture-anchor.txt`, `receipts/fixture-fragprefix.txt`,
  `receipts/fixture-fragprefix-counter.txt` — each a `git clone --shared` of the lane at `56026fcb`, toplevel
  asserted against the fixture path, one ledger pointer cell rewritten, committed under a fixture identity.
- All scratch was under `/fast/scratch/hyaku/mado-r51/SentinelC1Pointers/` and is deleted; no tracked lane file,
  fleet file, `MANIFEST.json`, `.ufo/state`, git/jj mutation or install was performed.

## Deliverables

- `.ufo/waves/round-51/w2/SentinelC1Pointers.md`
- `.ufo/waves/round-51/w2/SentinelC1Pointers/pointer-audit.md`
- `.ufo/waves/round-51/w2/SentinelC1Pointers/pointer-census.md`
- `.ufo/waves/round-51/w2/SentinelC1Pointers/pointer-audit.json`
- `.ufo/waves/round-51/w2/SentinelC1Pointers/audit.py`
- `.ufo/waves/round-51/w2/SentinelC1Pointers/receipts/freeze-c1-command.txt`
- `.ufo/waves/round-51/w2/SentinelC1Pointers/receipts/freeze-checker.txt`
- `.ufo/waves/round-51/w2/SentinelC1Pointers/receipts/pointer-audit-summary.txt`
- `.ufo/waves/round-51/w2/SentinelC1Pointers/receipts/witness-grep.txt`
- `.ufo/waves/round-51/w2/SentinelC1Pointers/receipts/fixture-allself.txt`
- `.ufo/waves/round-51/w2/SentinelC1Pointers/receipts/fixture-allself-counter.txt`
- `.ufo/waves/round-51/w2/SentinelC1Pointers/receipts/fixture-dotted.txt`
- `.ufo/waves/round-51/w2/SentinelC1Pointers/receipts/fixture-anchor.txt`
- `.ufo/waves/round-51/w2/SentinelC1Pointers/receipts/fixture-fragprefix.txt`
- `.ufo/waves/round-51/w2/SentinelC1Pointers/receipts/fixture-fragprefix-counter.txt`

Report: .ufo/waves/round-51/w2/SentinelC1Pointers.md
