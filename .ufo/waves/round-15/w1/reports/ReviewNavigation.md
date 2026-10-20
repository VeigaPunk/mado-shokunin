# ReviewNavigation — U6 README inventory join and no predeclared missing file

Scope: C1 coverage, U6 input-debugging layer route. Navigation join only: `corpus/README.md` coverage-map rows against `corpus/knowledge/*.md` at a resolved revision. Semantic note quality, source tiers and gate behaviour are other seats' scope.

Baseline observed (static reads only, no probe run): HEAD `ea0446fcb4840089f0e541d96350144506fb5d1d`. Working tree has `SCORECARD.md` modified and round-15 wave files staged. `corpus/knowledge/` holds 28 `.md` notes (`git ls-tree -r --name-only HEAD corpus/knowledge | wc -l` → 28). `corpus/README.md` has 28 coverage-map rows at lines 12–39. No U6 note exists. `corpus/SOURCES.md` ends at S050; S051/S052 are absent. `.ufo/waves/round-15/measure.py` does not exist yet.

## Findings (by severity)

1. **High — a complete navigation count does not prove U6 integration.** At HEAD the join is trivially 28/28 with no U6 note. A probe run at any revision before the note commit returns `missing=[] extra=[] duplicates=[]` while `covers: U6` is 0. Navigation completeness must be reported alongside coverage at the same resolved SHA, and the U6 row must be counted there. Evidence: `.ufo/waves/round-14/measure.py:147-212` (expected set derived from `ls-tree`, index from `git show <sha>:corpus/README.md`); `.ufo/waves/round-14/evidence/after.txt:143-149` (navigation block for 28/28).

2. **High — exit code is not a navigation verdict.** The probe exits 0 by design (`.ufo/waves/round-14/measure.py:579-582`; spec says "exit 0 non-admission"). Any "navigation complete" claim must come from the arrays being empty, not from `exit=0`. Evidence: `.ufo/waves/round-14/evidence/after.txt:295`.

3. **Medium — basename join can silently collapse.** `expected = {Path(p).name ...}` (`measure.py:205`) turns two notes with the same basename in different subdirectories into one expected member. The current tree is flat, so this is latent. Fail-closed for README rows that include a subdirectory, but not for same-name files. Acceptance requires either path-level join (`knowledge/<relpath>`) or an explicit assertion that basenames are unique under `corpus/knowledge`.

4. **Medium — reciprocity check is U5-only in the round-14 counter.** The `inverse` check (`measure.py:180-192`) lives in the `item[1] == 'U5'` branch. The round-15 spec requires reciprocal mined S051/S052 joins for U6 (`SCORECARD.md:606`; spec item MeasureBuild). If MeasureBuild copies only the U5 branch, the U6 reciprocity is never computed and U6 passes without it. This is a README→measurement chain risk, not a README row check, but it breaks the same join.

5. **Medium — stale frontier and route text is not measured.** `corpus/README.md:91-95` still lists "the input debugging ladder" as open. `corpus/SOURCES.md:79-82` says "U5–U7 remain frontier ground." The counter reads neither. After U6 is admitted, both lines contradict the index unless updated. Round-14 had the same pattern as G6 (`.ufo/waves/round-14/w1/reports/ScribeClaims.md`, gap ledger entry G6/G8).

6. **Low — fail-closed behaviour is correct; keep it.** The regex `^\| \`knowledge/([^\`]+\.md)\`` (`measure.py:204`) requires a column-0 coverage-map row. A route-table link (`| Hyprland config…` rows, `corpus/README.md:55-61`) or a Frontier bullet does not count. A U6 entry present only in those places produces `missing=[<name>]`. Do not loosen the regex to match links.

7. **Low, out of scope — top-level `README.md` is not joined.** Its "What's here" lists only `SKILL.md` and `PROVINCE.md` (`README.md:12-14`). No measurement reads it. Do not expand scope to it for this claim.

## Acceptance conditions

A1. `measure.py` derives `notes` only from `git ls-tree -r --name-only <resolved_sha> -- corpus/knowledge` filtered to `.md`. No literal filenames, no expected-count constants, no allowlist of permitted missing names. Grep the file for `input`, `U6`, `expected_missing`, `allow`, `28`, `29` — none should be a membership or count constant.
A2. Index rows come only from `git show <resolved_sha>:corpus/README.md`. No working-tree reads.
A3. Output prints `notes`, `indexed`, `missing`, `extra`, `duplicates` as arrays, keyed by the resolved SHA. The report's navigation verdict cites those arrays.
A4. The U6 note file and its coverage-map row (`| \`knowledge/<slug>.md\` …`) land in the **same committed content revision**. Measure that SHA. Expect `notes = indexed = 29`, `missing = extra = duplicates = []`.
A5. The U6 coverage-map row names `covers: U6` and cites S051/S052 in its Source column, matching the note's head-15 `source:` line.
A6. `corpus/README.md` Frontier text (lines 91–95) removes the input debugging ladder from the open list and keeps delivery, IME and kernel limits open. `corpus/SOURCES.md:79-82` is updated to match.
A7. U6 reciprocity (`inverse`) is computed by the same rule for U6 as for U5 (every mined row whose `used-by` names the note is cited on that note's source line). It is not hard-coded.
A8. Measured content SHA and delivered SHA are byte-equal for `corpus/README.md`, the U6 note and `corpus/SOURCES.md` (`git show <sha>:path | sha256sum`), as in the round-14 closure.

## Rejection conditions

R1. Any navigation claim taken from `exit=0` alone, or any "28/28" or "29/29" text not backed by empty arrays at the cited SHA.
R2. Any hard-coded U6 filename, count, or missing-file allowance in `measure.py`, SCORECARD, spec, or report. "No predeclared missing file" fails if one exists.
R3. A README row that names a file absent at the measured SHA (`extra != []`), or a note present in the worktree but not in the content commit (measured `notes` 28, U6 coverage 0).
R4. A U6 route recorded only in the route table or Frontier bullets, with no coverage-map row (`missing != []`).
R5. `inverse` for U6 computed by copying the U5 branch, or hard-coded true.
R6. A navigation claim measured at a parent or pre-commit SHA, or at `HEAD` when HEAD is not the content commit.
R7. Frontier text still lists the input debugging ladder as open after U6 is admitted (contradicts the index).
R8. Any new `.md` under `corpus/knowledge` at the measured SHA without a matching README row (draft or scratch notes count as missing).

## Structural versus semantic checks

Structural (counter-checkable): name-set equality, duplicates, header `covers:` count, reserved-row presence, `inverse`. Semantic (not counted): whether the Holds text describes the U6 note, whether the Frontier wording is accurate, whether S051/S052 pins match the cited quotes. Those need the reviewer seat's read, not the counter.

## Evidence pointers

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/measure.py:147-212` (navigation join; reciprocity U5 branch at 180-192)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/measure.py:579-582` (exit 0 observation)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/evidence/after.txt:143-149,295` (28/28 empty arrays; exit 0)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/README.md:12-39` (28 rows), `:55-61` (route table), `:91-95` (stale open frontier)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:62` (S050, registry end), `:79-82` (stale U5–U7 frontier text)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md:598-621` (round-15 declared claim; `:606-612` U6 requirements; counter command)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-14-verifier-spotcheck.md:90` (independent navigation re-measure precedent, 27→28)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/reports/ScribeClaims.md` (G5, G6, G8 gap ledger: unpinned filename, frontier text, README row required)

## Residual risk and verification gaps

- The probe was not executed (contract: no measurement or live probe). All conclusions come from reading the code and committed bytes; the join's output for a U6 candidate is unobserved.
- The round-14 counter has not been re-run here; its after.txt is recorded evidence, not a fresh observation.
- Duplicate-basename and nested-path cases are latent; no current file triggers them.
- Frontier wording and source-row text are not checked by any counter.

## Tooling

No installs or updates were performed by this seat. No `agent.db`, credential files, omp CLI, tests, gates, builds, linters, formatters, or input probes were touched.
