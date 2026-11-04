# R73ScribeEntryC2 — C2 knowledge draft

## Behavior and artifact

Draft: `.ufo/waves/round-73/w1/R73ScribeEntryC2/draft/corpus/knowledge/guard-carrier-global-environ-r73.md`.
159 lines, tables preferred, opening `source` / `verified-at` / `recheck` trio.
Axes: operability (this claim), calibration (companion claim, not independently scored here).
No production entry adopted by this seat.

## Findings

| item | evidence and qualification |
|---|---|
| Global mapping carrier | Instrument `quality/counters/c2-r73-shapes.py:895-946`, committed at `1459cca11fb5d3956a6e9a128217852dd0c28cb9`; frozen fixture `c2-cases-r73.json:143-147`. |
| Mutated environment transport | Instrument `:949-989`; frozen fixtures `:149-159`; exact copies `{**os.environ}` and `dict(os.environ)`. |
| Candidate versus held | Disk `measurement-c2-r73.txt:46-50,75-81`: 28/28 versus 25/28; exactly three missed positives. |
| Population | Disk measurement `:3-22,81`: 20 files, 13 readers, 13 guarded, 0 unguarded. |
| Baseline | `control-baseline-r73.txt:8`: held SHA and same three misses. |
| Limits | One global declaration, cross-function source-line order even if execution is later, one direct environ store, two copies, no environ alias, no value interpretation. |
| Sources | Fetched CPython v3.14.8 simple_stmts:972-980, os:184-198, subprocess:88-91. L1 assigned S447/S448/S449; placeholders replaced on explicit L1 direction. No source fetch or registry append by this seat. |

## Commands and outcomes

Commands ran in `/home/vgpnk/Projects/shokunin/mado-shokunin` unless stated otherwise.

| exact command | observed result |
|---|---|
| `mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-73/w1/R73ScribeEntryC2/draft/corpus/knowledge /fast/scratch/hyaku/mado-r73/R73ScribeEntryC2 && echo OK` | `OK`; cwd fleet root. |
| `git show 1459cca11fb5d3956a6e9a128217852dd0c28cb9:quality/counters/c2-r73-shapes.py` | Committed instrument bytes read successfully. |
| `git show 1459cca11fb5d3956a6e9a128217852dd0c28cb9:.ufo/waves/round-73/controls/c2-cases-r73.json` | Committed frozen control bytes read successfully. |
| `git show HEAD:.ufo/waves/round-73/measurement-c2-r73.txt && git show HEAD:.ufo/waves/round-73/control-baseline-r73.txt` | rc 128 on first command; second command did not execute. |
| `git log -1 --format='%H %s' -- .ufo/waves/round-73/measurement-c2-r73.txt .ufo/waves/round-73/control-baseline-r73.txt` | `87e4c61ac90e9ac587c9f65ac7844ded268d9046 round-73: freeze the two claims, their control sets and the do-nothing baseline`. Combined-path log does not establish measurement commit availability. |
| `rmdir /fast/scratch/hyaku/mado-r73/R73ScribeEntryC2` | Succeeded with no output; empty scratch removed. |

Static reads used specialized read/glob/grep tools: frozen declaration, candidate and held counters, frozen controls, measurement/baseline receipts, r71 knowledge precedent, and source fetch snapshots.
One invalid `read` selector `:-0` returned `Tail selector -0 is invalid; use :-N with N >= 1 to read the last N lines.`; retried with explicit control ranges. No bytes changed by that failed read.

## Conflicts and resolution provenance

Assignment calls measurement receipts “Committed receipts (re-read, do not rewrite)”. Observed verbatim:
`fatal: path '.ufo/waves/round-73/measurement-c2-r73.txt' exists on disk, but not in 'HEAD'`.
L1 subsequently confirmed: “the two measurement receipts were written after the instruments commit `1459cca1` and are on disk, uncommitted at HEAD until I commit the wave evidence before the report.”
Draft therefore names the on-disk receipt's `rev=1459cca11fb5d3956a6e9a128217852dd0c28cb9`, not committed receipt availability at read time.
No later evidence commit is claimed observed.

Write-bound wording says “Your ONLY write directory is .../w1/R73ScribeEntryC2/”, while the explicit seat report target is `.ufo/waves/round-73/w1/R73ScribeEntryC2.md`.
This report uses that expressly named report target; draft stays inside seat directory.

Original source instruction says “leave the S-ids as `<S447>/<S448>/<S449>` placeholders”; L1 later explicitly said “S-ids are now fixed” and “Replace the placeholders with those ids”. Draft follows that update.

## Gates, touched surfaces and exclusions

- Only draft and this expressly named report written; empty seat scratch created and removed.
- No judge, counter, selftest, lint, build or fixture execution; recorded rc 0 is assignment evidence, not observed process status here.
- Counter recheck command is in the draft for L1 use; frozen gate requirements remain requirements, not new execution evidence.
- No product edits, git/jj mutations, commit, push, publish, deploy, runtime invocation, host probes, tool install/update, or credential access.
- No scratch receipts exist or are cited; existing lane receipts remain in their original locations.

## Self-evaluation

| axis | score | evidence / improvement |
|---|---|---|
| Accuracy | 4 | Receipt availability conflict disclosed; L1 must finalize its evidence commit. |
| Completeness | 4 | Requested carriers, limits, negatives and provenance covered; adoption remains L1-owned. |
| Clarity | 4 | Tables separate semantic sources, syntax and measurement; long provenance caveat could shorten after commit. |
| Actionability | 4 | Draft path and exact recheck command supplied; source IDs assigned but registry not independently audited. |
| Conciseness | 4 | 159-line draft within requested 120–220; report repeats anchors for auditability. |

Overall 4.0. Ranked improvements: L1 record final receipt commit; shorten historical caveat only when that provenance is secured. User agreement expected because no recorded measurement was upgraded into scribe execution evidence.
