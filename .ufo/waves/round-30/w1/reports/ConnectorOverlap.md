# ConnectorOverlap — sibling index gates and criterion-grounding

Read-only scan of `*-shokunin` lanes other than mado. No lane bytes were edited. No tool installed.

## Axes

- **coverage / admitted-note reachability** — frozen fence: uniquely-once `corpus/knowledge/*.md` rows (`indexed=covered/notes`, missing, dangling, duplicates).
- **calibration / lesson-grounded criteria** — literal `^[0-9]+\. .*lessons/` plus resolved-active (file, anchor, M-id, supersession).
- **operability** — `quality/check-index.py` claims the fence's row set as a re-runnable gate. Harm watch: do not retarget that gate at a sibling counter.

## Mado row set (the thing siblings are compared to)

Owner: **mado**.

| Surface | Line | What a row is |
|---|---|---|
| `SCORECARD.md` counting command | 76–88 | `git ls-tree REV:corpus/knowledge` names ending `.md` vs `^\| `knowledge/([^`]+\.md)`` over the whole README. `covered` counts a note only when its row count is exactly 1. Exit 1 if missing, dangling, or duplicates. |
| `quality/check-index.py` | 4–8, 29, 76–81, 118 | Same partition. Regex is `^\|\s*`knowledge/([^`]+\.md)`` (zero-or-more spaces, not exactly one). `--rev` uses `ls-tree`; `--root` refuses symlinks. Selftest rows are `\| `knowledge/{n}` \| holds \| source \|` (118) — column 1, no trailing cell prose. |
| Live rows | `corpus/README.md:12–54` | Column 1, and the cell is **not** only the path: `` `knowledge/<file>.md` (MADO-…) ``. Trailing label is outside the backtick span, so both regexes still capture the filename. |

`check-index.py:6–8` says the gate is the fence. On the landed rows they agree. The regexes are not the same: a line `|`knowledge/x.md`` (no space) or `|  `knowledge/x.md`` (two spaces) is invisible to `SCORECARD.md:78` and visible to `check-index.py:29`. No selftest case exercises that.

## Overlaps that share the three-way partition

### kengaku — closest false friend (contradicts the numerator and the cell grammar)

Owner: **kengaku**.

Worktree census, same three names, different row:

- `plans/round26_census.sh:111–147` and `plans/round27_census.sh:111–147`. Comment at `round26_census.sh:111–112`: bidirectional knowledge parity, unindexed / dangling / duplicates.
- Extractor `round26_census.sh:124` and `round27_census.sh:123`: awk field `$2` (first cell) must be the **entire** cell, `/^`knowledge\/[^`|]+\.md`$/`.
- Files: shell glob + `[ -f ]` (`round27_census.sh:127–130`) — follows a symlink to a regular file, skips a dangling symlink, not revision-bound. Dangling is `[ -f corpus/$rel ]` failing (`:136–138`).
- Receipts that print `knowledge_readme_parity=match`: `.ufo/waves/round-26/build/ExecRound26Census.md:31–34`, `.ufo/waves/round-27/build/ExecCensus27.md:36–38`.

Revision-bound cousin, still not the fence:

- `corpus/evidence/round13-coverage/coverage_census.py:133–171`. First cell must be exactly one backtick span (`:142–145`). `indexed` is `len(discovered & found)` — a file listed twice **stays indexed** and is also listed in `duplicate_rows` (`:168–171`). Mado's numerator drops that file (`SCORECARD.md:83`, `counts[p] == 1`). Lessons and evidence directories are in this census; mado's denominator is `knowledge/*.md` only.

Cell contradiction on mado's own rows: `` `knowledge/foo.md` (MADO-1) `` does not end with a backtick, so both kengaku extractors drop it. Run on mado's README they report every note unindexed while the fence reports `indexed=43/43`. The reverse is also sharp: kengaku's coverage-map table puts the path in column 3 (`corpus/README.md:333–335` and `:360–362`), which neither kengaku's `$2` rule nor mado's line-anchored regex sees. Kengaku Q7 (`corpus/QUALITY.md:56–60`) requires the entry file, a README index row, **and** a coverage-map row as three lands. Mado's fence treats the README row as the coverage map. Q7 applied to mado would demand a second table the predicate does not score.

### kotoba — same words, different column, different denominator (contradicts)

Owner: **kotoba**.

- `verifiers/verify_corpus_integrity.py:6–15` — `unindexed` / `stale_patterns` / `missing_paths`. There is no duplicate counter.
- Heading gate `verify_corpus_integrity.py:152–153`: only a section `## Coverage map`. Harvest is column 2 (`cells[2]`, `:406–417`), not column 1.
- `index_findings` `:438–467`: set union of brace-expanded FILE tokens; fenced rows are excluded (`:431–436`); `unindexed` is every tracked `corpus/` path except `README.md` with no hit. A `lessons/` or `QUALITY.md` file with no FILE-cell token is unindexed. Mado ignores those files.
- `stale_patterns` is "pattern matched no tracked file". `missing_paths` is "token does not exist on disk". `verifiers/fault_injection_corpus.sh:209–212` and `:450–452`: an on-disk untracked file is `stale_patterns`, not `missing_paths`. Mado `--rev` would call a row whose blob is absent from `ls-tree` **dangling**, and would call a note with no row **missing**. Kotoba's `missing=0` is not mado's `missing=0`.
- Independent witness repeats the set, not the multiset: `verifiers/verify_corpus_independent.py:377–388` and `:545–548`.

A mado row is green for the fence and invisible to kotoba (path is in cell 1; the description cell is what kotoba reads). Moving the path to cell 2 to satisfy kotoba makes it invisible to the fence and to kengaku. One cell cannot be a row for all three.

Kotoba `corpus/QUALITY.md:60` states its own admission bar is indexed in that column-2 map. That is kotoba's index, not a second implementation of S185.

## Criterion-grounding prior art (requirement text, not mado's resolver)

Owner of the resolver: **mado**, `.ufo/waves/round-30/c2/count.py:6–25`. Literal fraction is the r12 grep at `SCORECARD.md:234` and `:845–846`. No sibling implements that resolver (file exists at REV, anchor word, M-id / range / `lesson round<NN>` spelling, `Supersedes criterion N` dropped from both sides).

| Lane | Path:line | What it actually is | Relation |
|---|---|---|---|
| kotoba | `corpus/QUALITY.md:3–10` | Table `\| Qnn \|` with a `grounded in` column and a `supersedes` column. "No criterion exists without a lesson behind it." | Same intent. Line grammar is not `^[0-9]+\. `. `count.py` would see zero criterion lines. |
| mori | `corpus/QUALITY.md:9–11` | Numbered `N. … ← lessons/<file>#M` — the syntactic cousin of mado's literal grep. | Citation shape differs (`←`, `#M` on the lesson file, no `Supersedes criterion N` parser). `tools/mori-census.sh:941–942` cites QUALITY #15 inside a journal counter; it does not resolve criterion citations. |
| kengaku | `corpus/QUALITY.md:56–60`, `:111–120` | Bullet `**Qn —**` plus `Lesson: `corpus/lessons/...``. Q14 prose says it supersedes Q13. | Not `^[0-9]+\. `. Supersession is not `Supersedes criterion N`. |
| revenger | `corpus/QUALITY.md:3–6`, `:23–25` | Q-table; each row cites a mistake class. Q12's cell contains `` M21 (`lessons/round-61.md`) ``. | Requirement, not a resolver. |
| kotodama | `corpus/QUALITY.md:29` (and the same `Grounded in` pattern on later numbered items) | `Grounded in … `corpus/lessons/round-N.md#anchor``. | Anchor is a heading slug, not mado's M-id check. |
| kotodama | `reports/round-34/cross/X03-protocol.md:336–338` | "lesson-citation coverage" of a reissue table (18 instances / 10 targets). | A different denominator. |
| mori | `.ufo/waves/round-35/w2/ReviewQ98Corr.md:12–13` | Names a "lesson-citation defect" already fixed at `QUALITY.md:763`. | Narrative, not a counter. |
| revenger | `.ufo/waves/kaika-r1/scribe-pointer-audit.md:123–124` | "not a lesson-citation defect" while auditing Q↔M pointers. | Audit note, not a gate. |

## Name collisions (not prior art)

| Lane | Path:line | Why it is not this gate |
|---|---|---|
| souji | `tools/cand-d1-verify.sh:602` (same comment in `cand-d1-quarantine.sh:778`, `cand-d1-vault.sh:781`) | Parameter "check-index" means "look at the git index flag", not a corpus coverage map. |
| chousa | `.ufo/reports/round-10/goal-wave/report-draft.md:131` and finding id `REF_UNRESOLVED` | Dangling cross-section ids inside a research record. Not `knowledge/*.md` vs README rows, and not QUALITY lesson resolution. |
| audio | `reports/round-101/r101-planner.md:70` | Prints `indexed=all` as a file count. No missing/dangling/duplicate partition. |
| kaidoku | `.ufo/waves/round-19/w2/CorpusIndex.md:71` | One-off set diff of knowledge files vs backtick ids in a wave note. Not a standing gate. Other kaidoku "unindexed" hits are lesson-table bookkeeping or AppImage overlay prose. |

## Proposed move (one)

Do not reconcile mado's row grammar with either sibling, and do not cite a sibling receipt as a control for `PRED-C1-r30` or `PRED-C3-r30`.

The three instruments want incompatible cells:

1. Fence / gate: line-anchored column 1, path is the first backtick span, trailing cell prose allowed, denominator is revision-bound `knowledge/*.md`, numerator requires count == 1.
2. Kengaku census: column 1 must be exactly `` `knowledge/<file>.md` `` and nothing else; worktree `[ -f ]`; `coverage_census.py` still counts a duplicated file as indexed.
3. Kotoba: column 2 under a heading `## Coverage map`, any corpus file, set union, fences ignored, `missing` means on-disk absence.

Live mado rows (`corpus/README.md:12`) satisfy (1) and fail (2) and (3). Stripping the `(MADO-N)` label to satisfy (2) still fails (3) and rewrites the row text C1 said would quote the note header. Moving the path to column 2 to satisfy (3) turns the fence red and undoes C1.

C2 stays on `count.py`'s three citation shapes. Kotoba's `grounded in` column, mori's `← lessons/…#M`, kengaku's `Lesson:` bullets, revenger's Q-table, and kotodama's `Grounded in` slug are not substitutes and are not unresolved-criterion bugs in mado.

## Affected axes

- **Coverage — not harmed**, only if the fence stays the witness. Substituting kengaku `parity=match` or kotoba `unindexed=0 stale=0 missing=0` can report green on a tree the fence scores red, and the reverse.
- **Calibration — improved** by refusing those substitutions, including for C2. No sibling resolver is promoted into the predicate.
- **Operability — not harmed**. The gate's selftest fixtures (`check-index.py:118`) are the column-1 subset. Retargeting the harvest to kotoba's `cells[2]` would make those fixtures fail and would make the base-red / tip-green pair stop measuring C1.

## Risks

- Intra-lane, confirmed from the sources (not a sibling): the counting algebra matches; the input contract does not. `check-index.py:29` `^\|\s*` is a superset of `SCORECARD.md:78` `^\| ` (`\s` includes tab and newline under `re.M`). `check-index.py:45` tokenizes `ls-tree` with `split()`; the fence uses `splitlines()` (`SCORECARD.md:76`). `check-index.py:88` turns an empty note set into `indexed=0/0` exit 0; the fence divides by `len(notes)`. `check-index.py:211-213` defaults `--rev` to `rev-parse master`; the fence defaults `REV` to `bb08dd57` (`SCORECARD.md:70`). RevC1Fence measured the grammar split on ephemeral repos (two spaces, zero spaces, tab, newline, and a fabricated duplicate) and recorded it in `.ufo/waves/round-30/w1/reports/RevC1Fence.md`. On committed rows both still print 41/43 and 43/43. Do not "fix" this by adopting kengaku's exact-cell rule or kotoba's column 2.
- `coverage_census.py:168` uses the word `indexed` for a set intersection. Quoting that number next to `indexed=43/43` launders a duplicate into the numerator.
- Kengaku Q7's three-artifact landing rule, applied here, would invent a second coverage-map table the registration does not score.
- Observed, not touched: worktree `quality/q36-successor-receipts.txt` is modified (4 lines). Outside this seat's write path; not restored.

## Verification (not run by this seat)

On one scratch README, three rows, scored only by reading the cited predicates:

1. `` | `knowledge/a.md` (MADO-1) | holds | `` — fence hit, kengaku exact-cell miss, kotoba column-2 miss.
2. `` | `knowledge/a.md` | holds | `` twice — fence `duplicates=1` and `indexed` excludes it; `coverage_census.py` still counts it in `indexed` and in `duplicate_rows`.
3. A `## Coverage map` row whose **second** cell is `` `knowledge/a.md` `` — kotoba hit, fence miss, kengaku miss.

Do not point `plans/round27_census.sh` or `verifiers/verify_corpus_integrity.py` at the mado repo and read the exit code as K1/K3.
