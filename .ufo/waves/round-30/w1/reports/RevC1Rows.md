# RevC1Rows — C1 index-row attack (round 30, w1)

Seat: leaf reviewer. Item: ATTACK C1 (report only). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Nothing outside this report and the
`quality/q36-successor-receipts.txt` worktree change (not mine, see I3) was written.

Read scope: the two new rows at `corpus/README.md:53-54` at `446dc396`; both named notes
(`corpus/knowledge/workspace-rules-r27.md`, `corpus/knowledge/mutation-testing-r28.md`);
the frozen fence (`SCORECARD.md`, S185); the round-28/27 registrations; `corpus/SOURCES.md`
S178–S185; the after/before receipts; `quality/check-index.py`.

## What reproduces (claim's numeric core holds)

- Frozen fence (S185 block, extracted verbatim) re-run read-only:

  | REV | line | exit |
  |---|---|---|
  | `8f51071b` (base) | `indexed=41/43 missing=2 dangling=0 duplicates=0 coverage=9.5349/10`, missing = `mutation-testing-r28.md`, `workspace-rules-r27.md` | 1 |
  | `451e8b3c` (freeze) | `indexed=41/43 missing=2 …` | 1 |
  | `446dc396` (data) | `indexed=43/43 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | 0 |
  | `92d3c86` (records) | `indexed=43/43 …` | 0 |

  Matches `evidence/c1-before-8f51071b.txt` / `evidence/c1-after-446dc396.txt` exactly,
  including the full-sha receipt lines. K1 (do-nothing never reaches 43/43) holds.
- Fence identity: the `bash` block's sha256 (`body+\n`) is
  `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88` at all four
  revisions — identical to the hash recorded in `corpus/SOURCES.md:197` (S185). The
  instrument is frozen, not re-cut under the data.
- Row set: 43 index rows vs 43 `corpus/knowledge/*.md`; the data-commit README diff is
  exactly `+2` lines and nothing else. No duplicate/dangling.
- Provenance of the rows: row 53's source list `S178–S182, S158, S162` equals the note's
  front-matter list; the note's `verified-at 20022a65` receipt
  `.ufo/waves/round-27/evidence/c1-after-20022a65.txt` is committed and records
  `41/41`, seed `4cfdf858277ad362`, `ORACLE_VERSION commit=efb5099… tag=v0.56.2`;
  `tools/mado-wsrules.py` is byte-identical at `20022a65` and `446dc396`
  (blob `93b6484…`). Row 54's `registration .ufo/waves/round-28/registration.md` exists
  at the data commit; that registration has exactly six numbered legs (`h1-rotation`,
  `h2-rotate`, `refpub-kills`, `boolword-v5`, `q36-witness`, `q37-open-ended`), so
  "six-leg gate" is accurate.
- Harm-watch adjacency: `git diff 8f51071b 446dc396 -- corpus/knowledge tools/ SKILL.md
  PROVINCE.md` is empty; the worktree registration copy is identical to `451e8b3c`.

## Findings

### MEDIUM

**M1 — C1's "target met" proves path completeness only; the claim's fidelity half is
outside the predicate.** Registration C1 requires "each row quoting the note's own
header/scope (no new domain claim admitted)", but `PRED-C1-r30` and its kill rule read only
row *paths*. The fence's matcher is
`re.findall(r"^\| `knowledge/([^`]+\.md)`", …)` (`SCORECARD.md:78`), and the only emitted
fields are counts of that capture group (`:84-88`); the Holds/Sources cells are never
parsed. Any text after the path — including a false Holds — scores 43/43. So the claim's
second sentence is unfalsifiable by the instrument that certifies it. The author does
declare the gap in SCORECARD's *Planned* sweep ("semantic index-row accuracy … the fence
counts rows, not truth"), but that declaration lives in the records commit, not in the
registration's C1 text, and no kill rule covers it.
Mitigation actually observed: I read both rows against both notes (below) — the rows do
quote note content, contain no new domain entity, and the README preamble ("A new index
row does not close a behavioral gap") carries the global hedge. The fix is scope hygiene:
either drop the fidelity clause from the claim or add a content predicate
(row-id ↔ note front-matter/title check) to a future gate.

### LOW

**L2 — row 53 drops the note's evidence class for selector semantics.**
Row 53: "How Hyprland v0.56.2 parses `workspace =` rules into the `hyprctl workspacerules
-j` table (selector/property semantics, gaps shorthand, merge-in-place, on-created-empty)
…". The note's Scope says: "The selector-property descriptions are from the pinned
hyprlang-era wiki, and are **documentation rather than a runtime measurement**"
(`workspace-rules-r27.md:18`), and its Open items keep "dynamic selector forms or update
semantics" `[INF]` (`:68`). The row's unqualified parenthetical presents the wiki-derived
selector material under "How Hyprland parses". Everything else in the parenthetical is
measurement-backed (`:22`: gaps shorthand, merge-in-place/first-seen order,
`on-created-empty` prefix). No new domain claim; a qualifier was compressed away. Contrast
row 51 (`bind-table-r25`) which does state its out-of-scope runtime path.

**L3 — row 53 names the superseded scoring instrument.** Row 53: "the **frozen v4
counter** that scores it against Hyprland's own table", recheck
`python3 -I .ufo/waves/round-27/c1/count-v4.py REV`. At the same data commit,
`.ufo/waves/round-28/c1/count-v5.py` exists, self-described as "successor to the frozen
round-27 v4", adding two fixed RNG-independent `BOOLWORD` cases (`truex`, `nope`). Row 53
mirrors the note's own stale `recheck:` field, so this is inherited staleness, not a new
claim — but navigation sends a reader to the weaker instrument. Same remediation class as
the note's front matter.

**L4 — row 54 converts two hedged note sentences into categorical summaries and drops one
scope condition.** Row 54: "the score is conditional on the selected mutants, oracle,
harness and frozen rule; a survivor is a suite limitation, not a real-fault verdict;
equivalent mutants bound the denominator."
- The note lists **five** conditions: "chosen mutants, **subject/input population**, oracle,
  harness, and frozen scoring rule" (`mutation-testing-r28.md:12`); row 54 drops the
  population and the "pass verdict" half.
- "a survivor is a suite limitation" — the note says a survivor is "evidence that the
  tested suite did not distinguish that mutant **under the gate's observations**; it is
  not, **by itself**, proof of a real defect" and, two sentences later, that equivalent
  mutants "can appear as survivors" and that no test observing the same behavior can
  distinguish them (`:20`). The row's universal is contradicted by its own next clause.
- "bound the denominator" is not the note's claim: "if they are excluded, equivalence
  classification **affects** the denominator" (`:20`).
No new domain claim; the compressions weaken caveats, which is the failure direction that
matters for a navigation map.

### INFO / adjacent (not introduced by this diff)

**I1 — pre-existing malformed row 52.** `corpus/README.md:52`
(`animation-table-r26.md`) has two cells (`pipes=3`) in a three-column table; its sources
are prose ("Sources S175–S177, S158, S162."). Identical at `8f51071b` and `446dc396`;
the fence and `quality/check-index.py` are cell-count-blind, so it survives both. Repair
should ride a round that touches the table.

**I2 — gate/fence matcher divergence (cross-ref `RevC1Fence`).** Confirmed independently:
fence `^\| `knowledge/…` vs gate `^\|\s*`knowledge/…` (`quality/check-index.py:ROW_RE`) —
strict superset. Latent on committed bytes (all 43 rows use the canonical single space).
Reported in `RevC1Fence.md`; not duplicated as a C1 finding.

**I3 — worktree write outside w1 scope.** `quality/q36-successor-receipts.txt` shows
`M` (4 lines changed: `/tmp` + `/fast/scratch` run-dir names only; `rc=`, `expected=`,
`PASS` unchanged, so no verdict moved). First observed by `RevC1Fence`; I did not touch or
restore it. Not a C1 finding — flagged for the integrator's write-scope ruling.

## Answers to the three assigned attacks

1. **Does a row's Holds overclaim vs the note's own scope?** Not by adding domain claims —
   both rows are composed from each note's title/scope/measurement-status text, and no new
   entity, capability or source is introduced. But two qualifier drops are real: row 53
   promotes wiki-documented selector grammar into "how Hyprland parses" (L2), and row 54
   detaches survivors and equivalence from the note's "under the gate's observations /
   not, by itself" hedges and drops the subject/input-population condition (L4). Row 53's
   v4 pointer is stale against the committed v5 successor (L3). None of these is a
   kill-rule event; all are repaired by adding the note's own qualifier words.
2. **Is the S183 citation honest (title-level only)?** Yes. `corpus/SOURCES.md:195` records
   S183 status `A`, disposition `mined`, evidence "DOI metadata `title` field"; the note's
   Scope and Gate block restrict it to paper identity/title and explicitly attribute "no
   empirical result, method detail, or conclusion"; row 54's parenthetical
   "(title-level; no article result attributed)" matches that scope and does not source the
   mutation-score propositions to S183. The note's prior-gate anchors also resolve at the
   data commit (`corpus/lessons/round-26.md:32` = M26-8, `corpus/lessons/round-27.md:15` =
   M27-3). Notable: the round-28 registration's own C1 text says the note "cites S183 for
   the finite mutation-suite method and its limits" — broader than the note's title-only
   scope; row 54 correctly follows the note, not the registration.
3. **Could a row exist without the note (dangling-then-note ordering)?** No window exists in
   this round or in README history. Both notes are present at `8f51071b` (r27/r28) and are
   first indexed at `446dc396`; a scan of all 29 commits that touch `corpus/README.md`
   finds **zero** commits with a dangling row, and the fence reports `dangling=0` at all
   four round-30 revisions. The `dangling`/`duplicates` terms are therefore vacuous at both
   C1 endpoints (no note was renamed/deleted), so they carry no signal this round; the row
   set is one contiguous table with 43 rows for 43 notes. The ordering hazard the fence
   *would* catch (row committed ahead of its note) is structurally absent here because the
   notes predate the rows by two rounds.

## Residual risk

- Only the two new rows were semantically read; the other 41 rows' Holds text is unmeasured
  by fence and gate (M1's general case; the round's *Planned* sweep owns it).
- Row 53's recheck command does not reproduce the note's recorded run: `count-v4.py`
  defaults `seed = os.urandom(8).hex()`, so `… count-v4.py REV` samples a fresh case
  population (and needs a nested Hyprland v0.56.2 + harness pins) unless
  `--seed 4cfdf858277ad362` is supplied. The row faithfully copies the note's `recheck:`
  field, but a future reader cannot replay the recorded 41/41 from the printed command.
- Row 52's malformed cell split (I1) is unguarded by both index instruments.
- No saturation claim rides C1; the round's claims are bounded and I found no
  same-identity rerouting: one fence, frozen hash, one base and one data revision.

## Verification gaps

- No `lsp` device is exposed on this seat and no language server answers Markdown corpus
  prose; all checks here are git-object and text-level. No semantic-reference proof is
  claimed beyond the git-level identity comparisons.
- I did not execute `count-v4.py`/`count-v5.py` (they spin a nested headless Hyprland
  instance; outside a row-text review, and the r27 capability is cited from its committed
  receipt plus blob identity instead).
- I did not re-run `tools/mado-verify.sh --selftest` or the census (harm watch, not my
  item; already re-run by the freeze smoke and the records commit).
