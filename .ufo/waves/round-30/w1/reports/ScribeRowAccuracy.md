# ScribeRowAccuracy — audit of the two round-30 index rows

Seat: scribe (leaf, no dispatch). Round 30, wave 1, `mado-shokunin`.
Scope: the two rows added to `corpus/README.md` in the data commit — for
`knowledge/workspace-rules-r27.md` and `knowledge/mutation-testing-r28.md` —
audited against the notes they name. Read-only audit; no lane file edited, no
counter, gate or verifier re-executed, no tool installed.

Revisions: base `8f51071b5bc44c815eeb5da76bb7f1947994ffb8`, data
`446dc3966193c81e64896f4880a19a4bd249255b`, lane HEAD `92d3c867`. The two README
rows are byte-identical at data and HEAD (`git diff 446dc396 HEAD -- corpus/README.md`
empty), and both notes are byte-identical base→data→HEAD
(`git diff 8f51071b 446dc396` and `446dc396 HEAD` over the two note paths, empty).

## Verdict

- **Form/countability:** both rows are well-formed index rows. Each matches the
  gate's row regex once; at `446dc396` the static row-set is **43 rows / 43 unique /
  43 notes / 0 missing / 0 dangling / 0 duplicate**. This is a static replication
  (see Method), not a gate run. The committed receipt
  `evidence/c1-after-446dc396.txt` reads
  `revision=446dc396… indexed=43/43 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`
  / `EXIT=0`; it is quoted as context, not reproduced here.
- **Row A** (`workspace-rules-r27`): every named referent resolves. PASS with
  low-severity wording/omission notes (F4–F7).
- **Row B** (`mutation-testing-r28`): every named referent resolves (note, S183
  mined/title-level, registration, six legs, limits section), but the Holds cell
  carries **one semantic overclaim (F1)** — exactly the defect class this seat was
  sent to find: a row that promises more than the note holds, and that the
  completeness fence cannot see because the row still counts.

## Row A — `knowledge/workspace-rules-r27.md` (surface P1)

Committed text (Holds cell, verbatim):

> How Hyprland v0.56.2 parses `workspace =` rules into the `hyprctl workspacerules -j`
> table (selector/property semantics, gaps shorthand, merge-in-place,
> on-created-empty), the round-27 tool `tools/mado-wsrules.py` and the frozen v4
> counter that scores it against Hyprland's own table.

| # | Row claim | Evidence found | Verdict |
|---|---|---|---|
| A1 | note exists and is the indexed bytes | present at `8f51071b`, `446dc396`, HEAD; bytes unchanged across those revs | holds |
| A2 | subject is Hyprland v0.56.2 | note title; §Scope pins v0.56.2 / `efb50993…`; §Measurement status line 22 | holds |
| A3 | "parses `workspace =` rules into the `hyprctl workspacerules -j` table (selector/property semantics, gaps shorthand, merge-in-place, on-created-empty)" | note line 22: measurement at `20022a65` "reproduces Hyprland v0.56.2's `hyprctl workspacerules -j` byte-for-byte, entry-by-entry" and "establishes the emitted schema … merge-in-place with first-seen order, and the `on-created-empty` `[workspace X] cmd` prefix"; selectors §Selector grammar (line 30); merge line 48; gaps §Rule keys | holds (bounded by F7) |
| A4 | tool name `tools/mado-wsrules.py`, "round-27 tool" | file present at base/data/HEAD (30,664 B at HEAD); added in `48b9434` "round-27: C1 data — tools/mado-wsrules.py"; the counter's `TOOL_PATH` is exactly this path | holds |
| A5 | "frozen v4 counter" | `.ufo/waves/round-27/c1/count-v4.py` present at base and data; **one** history entry (`2fdca5c`, round-27 freeze), never modified; self-labels `counter c1-r27-v4`; PRED name `PRED-C1-r27-v4` | holds |
| A6 | "scores it against Hyprland's own table" | counter docstring: compares the tool's JSON array to `hyprctl workspacerules -j` from "a nested, headless, session-isolated instance run by the counter", pinned to `HYPR_COMMIT=efb50993…`, type-strict canonical-JSON equality | holds |
| A7 | recheck command exists and is quoted correctly | note frontmatter `recheck:` and the README backticked command are **string-equal**: ``python3 -I .ufo/waves/round-27/c1/count-v4.py REV``; script accepts positional `rev` (`argparse`); path exists at base, data and HEAD | holds (preconditions in F4) |
| A8 | `source:` S178–S182, S158, S162 | exactly the note's 7-id frontmatter set; all seven SOURCES rows exist, tier A, status `mined`, and each `used-by` names `corpus/knowledge/workspace-rules-r27.md` | holds |
| A9 | "index row added round 30" | `git log -S'workspace-rules-r27.md' -- corpus/README.md` returns only `446dc39` (round-30 data); base→data README diff is exactly `+2` lines | holds |
| A10 | "surface P1 Hyprland workspace rules" | SCORECARD.md:848 defines P1 as the Hyprland config tree (including rules); sibling rows use the same label form. The note itself carries no `surface:` declaration, so the label is navigation, not rubric-V credit | holds as label (F6) |

## Row B — `knowledge/mutation-testing-r28.md` (lane tooling, no surface)

Committed text (Holds cell, verbatim):

> What a finite mutation score claims and cannot claim: the score is conditional on
> the selected mutants, oracle, harness and frozen rule; a survivor is a suite
> limitation, not a real-fault verdict; equivalent mutants bound the denominator.
> Covers the round-28 C1 six-leg gate's challenge surface and its declared limits.

| # | Row claim | Evidence found | Verdict |
|---|---|---|---|
| B1 | note exists and is the indexed bytes | present at base/data/HEAD; byte-identical across all three | holds |
| B2 | "what a finite mutation score claims and cannot claim" | note title "Finite mutation suites: evidence and limits"; §Scope lines 11–14 | holds |
| B3 | conditionality list | note line 12: "conditional on the chosen mutants, **subject/input population**, oracle, harness, and frozen scoring rule" — row drops "subject/input population" and the note's "score **or pass verdict**" | holds with omission (F3) |
| B4 | "a survivor is a suite limitation, not a real-fault verdict" | note line 20 says a survivor is "evidence that the tested suite did not distinguish that mutant under the gate's observations; it is not, by itself, proof of a real defect", and that **equivalent mutants "can appear as survivors"** | **does not hold — F1 (semantic overclaim)** |
| B5 | "equivalent mutants bound the denominator" | note line 20: "if they are excluded, equivalence classification affects the denominator"; if included, they appear as survivors | holds loosely (F2) |
| B6 | "round-28 C1 six-leg gate's challenge surface and its declared limits" | note line 18 names "six registered legs" and "that enumerated challenge surface"; `.ufo/waves/round-28/registration.md:17-55` lists legs 1–6; note §"Limits inherited by C1" lines 22–27 declares four limits | holds |
| B7 | `source:` S183, "(title-level; no article result attributed)" | SOURCES.md:195 — tier A, status `mined`, `used-by: corpus/knowledge/mutation-testing-r28.md`, teaches "the title does not establish that a mutation score predicts fault detection"; note lines 12, 14, 27 match the parenthetical | holds |
| B8 | registration `.ufo/waves/round-28/registration.md` | present at `446dc396` and HEAD (9,238 B, 136 lines); note cites `:17-55` and `:31-55,94-107` | holds |
| B9 | "(round 28; lane tooling, no surface)" | round-28 registration C1 lists "Surface moved: the committed suite `quality/counter-selftest.py` …"; the note has no `surface:` line; same convention as the r20–r22 lane-tooling rows | holds |
| B10 | "index row added round 30" | `git log -S'mutation-testing-r28.md' -- corpus/README.md` returns only `446dc39` | holds |

## Findings

### F1 — semantic overclaim (defect; the class this seat was sent to find)

Row B asserts, categorically, that "a survivor is a suite limitation".
The note it indexes refuses that categorical step. Verbatim from
`corpus/knowledge/mutation-testing-r28.md:20`:

> A surviving mutant is evidence that the tested suite did not distinguish that mutant
> under the gate's observations; it is not, by itself, proof of a real defect. A
> behaviorally equivalent mutant cannot be distinguished by any test that observes the
> same behavior. If equivalent mutants remain in the counted population, they can appear
> as survivors; if they are excluded, equivalence classification affects the denominator.

A survivor that is a behaviourally equivalent mutant is **not** a suite limitation —
the note says no test observing the same behaviour can distinguish it. The row's own
third clause ("equivalent mutants bound the denominator") shows the source distinction
is present but flattened into a categorical claim. The completeness fence counts the
row as indexed either way, so this defect is invisible to C1/C3.

- Affected file: `corpus/README.md` (row B Holds cell only). This seat does not edit.
- Report-only repair, within the note's wording: replace "a survivor is a suite
  limitation, not a real-fault verdict" with "a survivor is evidence the suite did not
  distinguish that mutant under the gate's observations, not a real-fault verdict".
- Severity: medium — it mis-describes the note's central equivalence caveat, the
  lesson's stated purpose; it makes no false measurement claim and does not affect any
  predicate value.

### F2 — low: "bound the denominator"

The note says equivalence classification **affects** the denominator (and equivalent
mutants can appear as survivors); "bound the denominator" is a stronger, less faithful
compression. Report-only; fold into any F1 repair as "equivalence classification
affects the denominator".

### F3 — low: conditionality list omits a named conditioner

Row B lists "selected mutants, oracle, harness and frozen rule"; the note (line 12)
also conditions on **subject/input population** and on a **pass verdict**, and its first
limit (line 24) is explicitly "conclusions stay within the mutants, subjects, and input
cases actually named by the frozen legs". Omission, not overclaim. Restoring
"subject/input population" in the same repair as F1 would remove the gap.

### F4 — low: recheck preconditions not stated

The Row A recheck command is byte-identical to the note's and the script exists, but it
is not hermetic: the counter derives `LANE` from its own path (four levels up), reads
`tools/mado-wsrules.py` at `REV` via `git show`, needs the lane git history, launches a
nested headless Hyprland at `efb50993…`, and exits 2 on oracle-pin mismatch
(`ORACLE_SHA=0da5b855…`), `ORACLE_FAIL`, `ORACLE_UNSTABLE` or `ORACLE_VERSION`. The
sibling `bind-table-r25` row states "through a nested instance"; this row does not.
The row repeats the note's own command, so this is an omission shared with the note, not
a row-only overclaim.

### F5 — informational: note-side receipt provenance (not a row defect)

`corpus/knowledge/workspace-rules-r27.md` frontmatter names
`evidence/c1-after-20022a65.txt` beside `verified-at: 20022a65…`. That path is **absent
from tree `20022a65`**; it first lands in `98ebd5b` ("round-27: C1 official
measurement"), an ancestor of base. The note exists at `20022a65`; the note bytes change
`20022a65 → 8f51071b` (7 insertions, 3 deletions), i.e. the indexed note is not
byte-identical to the note at the pinned revision. The README row does not repeat this
path, so the row makes no false claim; recorded so the canonical judge does not read the
row as pinning a receipt at `20022a65`.

### F6 — informational: surface labels

Row A's "surface P1 Hyprland workspace rules" agrees with SCORECARD.md:848
("PROVINCE.md owned surfaces P1 Hyprland config tree, P2 Waybar, P3 Walker, P4
terminal-emulator configs, P5 themes/wallpapers, P6 screen/idle") and with the r25/r26
row convention. Neither note carries a `surface:`/`covers:` declaration in its first 15
lines, so neither row can be read as rubric-V surface credit — only as navigation.

### F7 — low: Row A drops the note's declared limits

The note keeps three open items the row does not signal: dynamic selectors are `[INF]`
beside the static-selector path (line 30, open item line 68); runtime
`hyprctl keyword workspace` is `[INF]` (line 67); `mergeLeft` per-field conflict
precedence is not established (line 48). The row's parenthetical enumerates only
measured features (schema, gaps shorthand, merge-in-place, on-created-empty), so it does
not contradict the note, and the README preamble ("A new index row does not close a
behavioral gap"; notes' unknowns still govern) routes the reader to the limits. Omission
only.

## Cross-row checks

- Both first cells match the gate's pattern `^\|\s*`knowledge/([^`]+\.md)``: regex over
  `446dc396:corpus/README.md` yields 43 matches, 43 unique; `git ls-tree 446dc396
  corpus/knowledge/` yields 43 `*.md`; missing/dangling/duplicate sets empty; each new
  note matches exactly once. The two rows sit in the Coverage map table, before
  `## Quality bar`.
- Both notes existed at base (`8f51071b`) already, so the base gap was rows-only —
  consistent with the registration's `indexed=41/43` at base (receipt read, not rerun).
- No other README row names either note at base (the base→data diff is two insertions
  and nothing else).
- "index row added round 30" is accurate for both: earliest (and only) appearance is
  `446dc39`; the round-30 commit lineage is `451e8b3` freeze → `446dc39` data →
  `92d3c86` records.

## Behavior / gates / touched surfaces

- Behavior: read-only inspection. Commands run: `git rev-parse`, `git log`
  (`--oneline`, `-S`, per-path history, `--diff-filter=A`), `git diff`,
  `git cat-file -e`, `git ls-tree`, `git merge-base --is-ancestor`, `stat -c`,
  `wc -l`, and one Python cell replicating the gate's row regex and parsing the
  SOURCES table / note frontmatter. No `python3 -I` counter or gate was executed.
- Gates: none exercised by this seat. The receipts `.ufo/waves/round-30/evidence/`
  (`c1-after`, `c2-after`, `c3-after`, freeze-smoke, census before/end) belong to other
  seats; only `c1-after-446dc396.txt` was read, as count context.
- Touched surfaces: exactly one file written — this report. No README, note, counter,
  gate, registration, lane git/jj state or sibling repo touched. No tool installed.

## Out of scope / not claimed

- Did not verify `PRED-C1-r30`, `PRED-C2-r30` or `PRED-C3-r30`; did not run
  `quality/check-index.py`, `count-v4.py`, the C2 counter, or any selftest.
- Did not audit the QUALITY.md rows, SOURCES S185 row, lesson, SCORECARD or wave spec.
- Did not change any row; F1–F3 are repair recommendations to the canonical judge /
  L1, not applied edits.

## Artifact paths

- Report: `.ufo/waves/round-30/w1/reports/ScribeRowAccuracy.md`
- Indexed rows: `corpus/README.md:53-54` (at `446dc396`; unchanged at HEAD)
- Notes: `corpus/knowledge/workspace-rules-r27.md`, `corpus/knowledge/mutation-testing-r28.md`
- Counter/tool: `.ufo/waves/round-27/c1/count-v4.py`, `tools/mado-wsrules.py`
- Source rows: `corpus/SOURCES.md:170` (S158), `:174` (S162), `:190–194` (S178–S182),
  `:195` (S183)
- Receipt read for context: `.ufo/waves/round-30/evidence/c1-after-446dc396.txt`

## Addendum — peer-reported worktree write (outside this seat's scope)

Received after the audit from `RevC1Fence`; re-checked read-only by this seat
(`git status --porcelain`, `git diff --stat/--numstat/-U0`), not restored, not edited.

- Worktree state: `M quality/q36-successor-receipts.txt`; diff is 4 insertions /
  4 deletions. The four changed lines differ **only** in ephemeral run paths
  (`/tmp/mado-r28-q36-ge5zx30t` → `/tmp/mado-r28-q36-g3nfq53x`;
  `/fast/scratch/hyaku/mado-r28/ExecQ36Runner/run.gR7SQoLa` →
  `…/run.Kv8n49Ha`). Every `rc=`, `expected=` and `PASS` field is unchanged.
- This is a committed round-28 evidence file, not a round-30 data-rule path, and the
  write is outside the registered write scope. No verdict moves on the shown bytes; the
  file is reported, not restored, because restoring is not this seat's write scope.
- This observation is not evidence about the two index rows audited above and does not
  change any verdict in this report. Attribution: `RevC1Fence` reported the write; this
  seat re-read the diff only.
