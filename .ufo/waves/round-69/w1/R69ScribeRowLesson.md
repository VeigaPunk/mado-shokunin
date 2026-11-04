# R69ScribeRowLesson — seat report

role: scribe (leaf; no subagent dispatch)
round: mado 69, wave w1
seat: `.ufo/waves/round-69/w1/R69ScribeRowLesson/`
lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`
scratch: `/fast/scratch/hyaku/mado-r69/R69ScribeRowLesson/` (removed before yield)

## Deliverables

| path (lane-relative) | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-69/w1/R69ScribeRowLesson/draft/corpus/SOURCES-row.txt` | 1114 | `eb0ccce85c1f28e6bff04946f379f1172b62bdf20f8972411f9a6290793033c8` |
| `.ufo/waves/round-69/w1/R69ScribeRowLesson/draft/corpus/lessons/round-69.md` | 13002 | `0d1258b9f59a07f173dd1e625f0623f46acccc48f0d9a1d2580f407d3692f37d` |
| `.ufo/waves/round-69/w1/R69ScribeRowLesson/draft/corpus/QUALITY-addendum.md` | 3909 | `3e54b1aebda4fc043711eaf3751d335390a29993df483e5dd94c9c63d9ae69f5` |

No production path was created, edited or deleted. No git/jj mutation, no pacman transaction, no
service/compositor/socket touch, no tool install (nothing needed installing this seat).

## Behavior

- **A. Registry row S438** (one physical line, 11 cells): `git v2.56.0 Documentation — git.adoc`,
  URL `https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc`, anchors
  `git.adoc:14` (SYNOPSIS), `:178-182` (OPTIONS `--no-replace-objects`), `:927-929` (ENVIRONMENT
  `GIT_NO_REPLACE_OBJECTS`); located quote (18 words) is the ENVIRONMENT sentence; status `mined`,
  opened 2026-11-03, recheck `on-release`, used-by the round's entry and lesson. Fetch measured
  this seat: three fetches, byte-identical, sha256
  `050c5330f1a231be22bee3db27c7ef90d8ba22bb7bd6c72c8bab462f6f0a1f79`, 47005 bytes.
- **B. Round lesson** with the three required sections. `## Outcome and boundaries` carries both
  claims, the frozen rolls and the **measured** contract lines from the committed receipts at
  `5fc29ae72e66b9347d576c796ee656aea2fdd04c` (`killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET`,
  `population=20 readers=13 guarded=13 unguarded=0 controls=11/11 base_controls=7/11
  verdict=TARGET_MET`), plus an `**Open harm item.**` paragraph for `landing_rc=2`.
  `## Mistakes` is a 5-column table with M69-1 (equivalent-mutant misclassification) and M69-2
  (value-position key accepted), each with class, evidence pointer, `captured-by: none` and the
  fix with the failure it can already show. `## Gate` carries the ADMIT (S438, URL, access date,
  quote), one REJECT (a second row on the same file's OPTIONS sentence) with reason and flip
  condition, and the E11 ordering note.
- **C. QUALITY criterion 111** in the 108-110 grammar: numbered bold statement, (a) printed-
  observable clause and (b) key-position clause, `Shown able to fail` with the L-probe red state
  and the r68 `7/11` red state, a `Recheck` command pair, `Ground`, and `Limits`.

## Gates run (exact commands, exit codes)

| check | command | result |
|---|---|---|
| fetch identity | `curl -sSL -o git2560.N https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc` ×3 | rc 0 each; `sha256sum` identical ×3 (`050c5330…f79`), 47005 B each; `cmp` → IDENTICAL |
| cell count | python split with `check-anchor-cover.py`'s own `cells()` semantics | 11 cells, awk `NF=13`, no pipe inside any cell |
| row validity (mine) | `bash scripts/sources-census.sh validate --file <scratch>/min-mine-stubs/corpus/SOURCES.md --today 2026-11-03` | rc 0, `file ok` |
| E11 counter-check (mine, used-by absent) | same file, stubs removed | rc 1, `E11 S438 missing used-by corpus/knowledge/gate-guard-dominance-r69.md` + `…/lessons/round-69.md` |
| row validity (already in the working tree) | minimal fixture with that row + stubs | rc 0, `file ok`; 11 cells, `NF=13` |
| lesson table shape | pipe-count per table row | 4 rows × 6 pipes → 5 columns |
| frozen blobs | `git rev-parse 789a87f1:<path>` vs `git hash-object <path>` | declaration `94bd1346…`, baseline `fd98cfb8…`, control set `726771c5…` — freeze equals worktree for all three |

The full-registry census was **not** run against the lane (it would read sibling lanes and the
working tree is mid-integration); the minimal fixtures isolate row shape, enums, URL scope and
E11 without that noise.

## Findings

1. **The working tree already carries an S438 row that is not mine.** `corpus/SOURCES.md:388` is
   uncommitted (` M corpus/SOURCES.md`, HEAD `6a5cefd2`) and holds a row with the same id, URL,
   anchors (`git.adoc:14,178-182,927-929`), sha256 and byte count as my draft. It parses as 11
   cells (`NF=13`) and validates rc 0 in a minimal fixture. Differences from my draft: cell 5
   wording (`mado lane tooling: the documented identity of --no-replace-objects …` vs my
   "the documented ground for round 69's C2 dominance rule …"), cell 7 (two quotes vs my
   quote + teaching clause) and used-by order. I did not touch it; the L1 decides which version
   lands.
2. **Production lesson and entry already exist untracked**: `corpus/lessons/round-69.md`,
   `corpus/knowledge/gate-guard-dominance-r69.md` (both `??` in `git status`). My lesson draft is a
   parallel version of the first; its measured values agree with mine because both cite the same
   receipts.
3. **Evidence mismatch in the untracked production lesson's M69-3 (verbatim conflict).** That row
   says the first harm-watch run exited 2 with `citecheck path missing` and a second run with
   explicit paths printed `MADO_LANDING_COUNTERS: RED (… ledger=1 …)`. The committed receipt
   `.ufo/waves/round-69/harm-watch-r69.txt` (HEAD `6a5cefd2`, same bytes in the worktree) contains
   neither string: it records `landing-counters.sh: citecheck path has uncommitted changes:
   .ufo/waves/round-69/measurement-c1-r69.txt` and `landing_rc=2`, and has no
   `MADO_LANDING_COUNTERS` line at all. As written, M69-3's evidence pointer does not support its
   claim; the harm item is real but its recorded cause is the uncommitted measurement file.
4. **Harm watch is not green at the measured snapshot.** `harm-watch-r69.txt`: gate
   `MADO_SELFTEST: 460/460` rc 0, axis `checked=3 mismatched=0` rc 0, five instrument selftests
   rc 0, but `landing_rc=2` — the declaration's `MADO_LANDING_COUNTERS: GREEN` is not established
   at `5fc29ae7`. My lesson records this as an open item instead of reading the refusal as green.
5. **Minor: word counts in the untracked lesson's Gate.** It states 14 words for the
   `--no-replace-objects` quote and 17 for the ENVIRONMENT quote; whitespace-token counts are 12
   and 18 (both within the `<=25` bound, so no gate failure — a count correction only).
6. **Row admission ordering.** Census `E11` reads every `mined` row's used-by path on disk
   (`scripts/sources-census.sh` `usedby_findings`); S438's two used-by paths are round-69
   deliverables, so the row is clean only when the row, the entry and the lesson are validated
   together (proved rc 0 vs rc 1 above). The row is a draft, not an admission: the declaration
   requires the scout to open it independently and the Gate to admit it.

## Out of scope / not done

- No counter run, no measurement, no mutation, no falsification — those are the executor,
  reviewer, critic and mutation-tester seats; this seat read the committed receipts only.
- No edit to the declaration, control JSON, baseline receipt, `corpus/SOURCES.md`, the knowledge
  entry or the production lesson; no claim re-scope; no desktop/compositor probe.
- No credential material, screenshots or `op://` refs in any artifact.

Report: .ufo/waves/round-69/w1/R69ScribeRowLesson.md
