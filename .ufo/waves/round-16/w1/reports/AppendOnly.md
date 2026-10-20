# Round 16 — LOG / SOURCES / QUALITY / lesson immutability review (AppendOnly)

Seat: `MadoR16.AppendOnly` (reviewer, leaf). Scope: read-only source and git-history
review of the immutability rules for `LOG.md`, `corpus/SOURCES.md`,
`corpus/QUALITY.md` and `corpus/lessons/*.md` for the round-16 cutover.
Baseline `HEAD` = `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
Snapshot of the live worktree: **2026-10-20T05:41:09-03:00**. Peers were writing
in-round during this review; the verdicts below bind to that snapshot only.
No build, lint, test, sources-census, measure, frozen replay, package, service,
or live desktop/compositor probe was run. No `jj` command was run. No installs
or updates (record: none).

## Verdict

**No immutability violation found in committed history or in the uncommitted
round-16 worktree at the snapshot.** Every protected file is append-only or has
its in-place changes logged in a lesson. Two low-severity documentation items
and one optional pointer remain for L1 integration (F1–F2 below). Nothing is
blocking.

## Requirements reviewed (where each rule is stated)

| File | Immutability rule | Stated at |
|---|---|---|
| `LOG.md` | Every change appends an entry with motivating evidence; corrections are appended errata, not edits | `AGENTS.md`; `LOG.md` errata wording (e.g. `LOG.md` round-12/13/14 "append-only" notes) |
| `corpus/SOURCES.md` | Rows are append-only; only `status`, `recheck`, `used-by` change in place, each logged old→new in that round's lesson; rejected rows kept; a supersession is a new row with a resolvable prior id | `SOURCES.md:3-7` header (current); QUALITY criterion 17 (`QUALITY.md:34`) |
| `corpus/QUALITY.md` | Criteria 1–5 incl. "Errata are append-only blocks" (4) and "A rejection is kept" (5); new criteria are appended with a lesson citation | `QUALITY.md:1-8`; criteria 6–21 are appended sections |
| `corpus/lessons/*.md` | Filed lessons are not rewritten; corrections go in a successor/append block; closure entries appended via the serialized helper | `lessons/round-15-verifier-spotcheck.md` §Routed defects ("do not rewrite filed history"); `LOG.md` round-15 entry |

The round-15 closure lesson `corpus/lessons/round-15-verifier-spotcheck.md`
is read and honored: its routed defects R15-V1 (host, operator-owned),
R15-V2 (procedural, carried into QUALITY 21) and R14-V1 are not rewritten here.

## Evidence

### E1. Committed history — `LOG.md` (append-only, one benign EOF artifact)

`git --no-pager log --numstat -- LOG.md` over every LOG-touching commit: each is
insertion-only except `7cd7f33` (`1 deletion`) and merge `7dcb785`.

- `7cd7f33` "deletion" is a **trailing-newline completion, not a content edit**.
  Parent's last line `  the promotion decision; \`.ufo/\` not inspected this round.`
  had no terminating `\n`; the new file is `parent + "\n" + appended block`
  (`python: new.startswith(old+b"\n")` → True). Byte-prefix holds modulo the EOF
  newline. Classified benign, no lost text.
- Merge `7dcb785` (`Integrate remote documentation; preserve local round log`):
  `LOG.md` 760 lines in parent 1 → 767 in merge (+7, 0 deletions); parent 2 661 → 767
  (+106 relative to that side, 0 deletions). `git diff 7dcb785^1 7dcb785 -- LOG.md`
  and `7dcb785^2` both contain no `-` content lines. No loss from either side.
- Harness note (not a repo defect): the sentence `Ran in a temporary shell while
  the session shell is busy…` appeared at the end of some bash outputs. It is
  **not in any LOG.md revision**: `git log --all -G 'Ran in a temporary shell'`
  returns nothing; `grep -c` on the worktree and on `HEAD:LOG.md` is 0. Do not
  "clean" LOG.md for it.

### E2. Committed history — lessons (append-only)

`numstat` across all lesson commits (`round-1.md` … `round-15.md`,
`round-*-verifier-spotcheck.md`): **0 deletions in every commit**. The lesson
fix commits (`bed2b90` +5/0, `a6df2f5` +9/0, `6e3b75f` +5/0, etc.) are pure
appends. Worktree vs `HEAD` at the snapshot: 0 deletions for every lesson file;
`corpus/lessons/round-15.md` and `round-15-verifier-spotcheck.md` are
byte-identical to `HEAD` (`git diff --quiet`).

New in-round: `corpus/lessons/round-16.md` (untracked, 71 L) — exists; Mistakes
table M1/M2 present (`## Mistakes` line 10, `## Gate` 21, `## Boundaries and
handoff` 62). Not deleted anything from earlier files.

### E3. Committed + uncommitted — `corpus/SOURCES.md` (cell-level audit)

Cell-by-cell diff over the 5 SOURCES-touching commits (`5174e15`, `8dbfc93`, `95cbc41`, `32118fc`, `5f13870`), comparing
each row id's 11 cells between consecutive commits:

| commit | in-place changes | logged old→new in lesson? |
|---|---|---|
| `8dbfc93` (round-12 post-review) | S017 `used-by`; S030 `status` mined→rejected, `used-by` | yes — `lessons/round-12.md` §Post-review registry changes (table, lines 118–124) |
| `95cbc41` (round-13) | S005 `status` queued→mined, `used-by`; S017 `used-by` | yes — `lessons/round-13.md` §Registry mutations (lines 42–50) |
| `32118fc` (round-14) | S041 `used-by` only | yes — `lessons/round-14.md` §Registry mutations (line 88) |
| `5f13870` (round-15), `9ebd737` and `32c4fda` (no SOURCES change) | none | n/a — `rows 52` at `5f13870`; no row cell changed |

No row was ever removed (row count 39 → 46 → 50 → 52). Protected cells (`id`,
`source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `opened`) never changed.

Uncommitted round-16 worktree at snapshot: `corpus/SOURCES.md` **19 insertions,
0 deletions**. New rows S053 (line 65), S054 (line 66), S055 (line 67) are
appended after S052 — each id appears exactly once; no pre-existing id existed
repo-wide before this round (grep `S05[3-5]` found only round-16 references).
The S053–S055 search-log block is appended at the end of the file.

### E4. Uncommitted round-16 worktree — `QUALITY.md`, `SCORECARD.md`, `SKILL.md`

At snapshot: `corpus/QUALITY.md` **+22/−0** (criterion 21 + `## Round 16` heading,
appended after criterion 20, `QUALITY.md:79-100`); `SCORECARD.md` **+29/−0**;
`SKILL.md` **+16/−0**. Criteria 1–20 are byte-unchanged (`git diff HEAD` shows
only `+` lines). Criterion 20 text (`QUALITY.md:72-78`) is preserved verbatim.

Live check of the whole protected set at 05:41:09: deletions = 0 for `LOG.md`,
`corpus/SOURCES.md`, `corpus/QUALITY.md`, every lesson file, `SCORECARD.md`,
`SKILL.md`.

### E5. Reserved ids and cited anchors

- S053/S054/S055 reserved by the spec; now present exactly once each. S055
  cites `corpus/lessons/round-15-verifier-spotcheck.md` — exists.
- QUALITY 21 cites `lessons/round-16.md#mistakes M1/M2` — **exists now** (it did
  not at the first snapshot; the citation was dangling then and resolved by
  05:41). Per QUALITY 8 the path is landed only after existence was confirmed
  here; it stays a recheck target if the lesson is later renamed.
- Fleet-root `CORPUS.md:64-67` contains the `## SOURCES.md` section and points to
  `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` (exists). The SOURCES header's
  "canonical `CORPUS.md` § SOURCES.md" pointer resolves.
- Reflog `HEAD@{0..14}` shows only commits (no reset, amend, rebase or
  filter-branch entries in the top 15). Recorded anchors `ea0446f`, `5f13870`,
  `9ebd737`, `32c4fda` are all ancestors of `HEAD`.

## Findings (severity order)

**F1 — Low (documentation, optional):** `QUALITY 21` supersedes criterion 20's
prospective install route "while the operator's host-wide pause holds", but
criterion 20 itself carries no pointer that it is partly superseded. A reader
who lands on 20 alone would apply the install route as active. Criterion 20 is
correctly **not** edited in place (QUALITY 4). Recommended fix (append-only, no
edit to 20): add a dated errata block directly under criterion 20, before the
`## Round 16` heading, saying "partly superseded by 21 (2026-10-20) while the
pause holds; criterion 20's real-plan comparison still applies after lift".
Owner: L1 (QUALITY.md).

**F2 — Low (unlogged in-place prose rewrite, historical):** commit `95cbc41`
(round 13) rewrote the **SOURCES.md header prose** in place: it removed the
sentence "Rows are append-only: … each change logged in that round's lesson", removed
the round-12 pointer "Every row below was opened … its ≤25-word grounding quote
is in `lessons/round-12.md` ## Gate", and repointed the contract reference from
`.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` to "canonical `CORPUS.md` § SOURCES.md".
Row cells were not changed, and the new pointer resolves (E5), so no row
information is lost. However, this header rewrite is **not logged**: round-13
lesson §Registry mutations covers row cells only, and the round-13 LOG entry has
no matching line. Do not revert the header. Recommended remediation: L1 records
the rewrite as an append-only note in the round-16 LOG entry (old and new header
text quoted, `95cbc41` named), so the historical registry-contract change is
auditable.

**F3 — Info (benign, do not act):** `7cd7f33` shows 1 LOG deletion. It is an
EOF-newline completion; the text of the old line is preserved byte-for-byte.
Record in the audit trail only.

**F4 — Info (benign, do not act):** merge `7dcb785` shows a large combined-diff
hunk (`@@@ -656,105 -656,6 +656,112 @@@`). Against either parent LOG has 0
deletions; the hunk is a merge artifact of the two-parent diff.

**F5 — Info (scope note, outside the four named files):** `corpus/README.md`
was edited in place in `32118fc` (2 deletions: the "Still open" prose) and
`95cbc41` (5 deletions: index rows and "Still open" prose), and `7dcb785`
appended 14 lines. README has no stated immutability rule (grep for
append/immutable/in-place finds none), so these are not violations. L1 should
decide whether the README index is "current-state" (edit in place, as now) or
append-only, and state it in the round-16 LOG so the rule is explicit.

## Integration guardrails (for L1; not run by this seat)

1. Re-run the protected-set deletion check **after the last writer finishes**
   (the worktree moved between 05:39 and 05:41 during this review):
   `git --no-pager diff HEAD --numstat -- LOG.md corpus/SOURCES.md corpus/QUALITY.md corpus/lessons SCORECARD.md SKILL.md`
   Expect deletions 0 everywhere, except any registry `status`/`used-by` cell
   change, which must have an old→new row in `lessons/round-16.md` §Registry
   mutations (currently none).
2. Confirm `git --no-pager diff HEAD -- corpus/SOURCES.md | grep -c '^-[^-]'`
   is `0` and each of `S053`, `S054`, `S055` appears exactly once in the
   registry (`grep -c '^| S05[345] |' corpus/SOURCES.md`).
3. Confirm the round-15 closure files are unchanged:
   `git --no-pager show 32c4fda:corpus/lessons/round-15-verifier-spotcheck.md | cmp - corpus/lessons/round-15-verifier-spotcheck.md`.
4. Append the round-16 LOG entry at the end; do **not** edit the round-15 entry
   ("No round 16." stays as history). A supersession belongs in a new block.
5. Land F1 (optional pointer under criterion 20) and F2 (LOG note for `95cbc41`)
   as append-only additions.

## Verification gaps and limits

- Contents of the S053/S054 tagged upstream files and the round-16 claims about
  them were **not** verified here (source-content review belongs to the source
  reviewers). This seat checked only immutability and identity.
- SCORECARD.md and SKILL.md were checked for deletions/insertions only, not for
  content correctness.
- The round-15 closure states the lesson/LOG appends went through a "serialized
  helper". Not located or executed; the immutability conclusion here does not
  depend on it, because the history itself is append-only.
- The worktree is a moving target. Every "0 deletions" statement is valid only
  for the snapshot `2026-10-20T05:41:09-03:00`; guardrail 1 must be re-run.
- No check was executed (per assignment). All evidence is git read-only history
  plus file reads.

## Tooling record

No installs or updates by this seat. Tools used: `git --no-pager` (read-only
log/show/diff/reflog/numstat), `grep`, `python3` stdlib (read-only parsing of
`git show` output), `read`. No `pacman`, `uv`, `npm`, `cargo`, or
`sudo` was invoked.
