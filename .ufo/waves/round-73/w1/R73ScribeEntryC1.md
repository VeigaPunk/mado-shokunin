# R73ScribeEntryC1 — C1 knowledge entry report

## Deliverable and behavior

Draft: `.ufo/waves/round-73/w1/R73ScribeEntryC1/draft/corpus/knowledge/control-set-mutant-kill-r73.md`.

158-line table-led entry opens with `source:`, `verified-at:`, `recheck:`; names calibration, preservation, and provenance axes. It links the round-72 M3/GAP-1 survivor and parser erratum to the new finite ten-case denominator, records all four mutants' held/new answers, and bounds the result to four named mutations of one outcome-rule family. It does not change a committed corpus entry.

## Evidence and gates

| Item | Outcome | Evidence class |
|---|---|---|
| Historical M3 | Eight outcome cases still returned `TARGET_MET`; missing positive-denominator guard survived | Committed M72 battery, read at base `d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce` |
| Historical parser defect | Trailing malformed marker suppressed a valid summary; repaired at `4f598cfd142e1bfcf4d63341e0b5ea11348c5c4c` | Read-only commit diff and declaration erratum |
| C1 measurement | `cases=10 mutants=4 killed=4 base_killed=2 verdict=TARGET_MET rev=1459cca11fb5d3956a6e9a128217852dd0c28cb9` | Existing on-disk receipt, not this seat's execution |
| Do-nothing comparison | `new_set=4/4 held_set=2/4` | Baseline read from freeze `87e4c61ac90e9ac587c9f65ac7844ded268d9046` |
| C2 context | `population=20 readers=13 guarded=13 unguarded=0 controls=28/28 base_controls=25/28 verdict=TARGET_MET` | Existing on-disk receipt, context only |
| Measurement rc | Assignment says rc 0; bare measurement text does not independently encode rc | Reported, not independently executed |
| Builds/tests/checkers | Not run | Scribe restriction; no reruns for report decoration |

## Findings and resolved conflicts

1. Assignment source path `.ufo/waves/round-72/w1/R72MutBattery.md` omitted the seat directory. Actual committed source is `.ufo/waves/round-72/w1/R72MutBattery/R72MutBattery.md`; located with read-only tree listing and read at base. L1 confirmed the correction.
2. Assignment wording: “each separates exactly one of the four named mutations (N1..N4)”. Literal per-case exclusivity conflicts with receipt N4's `zero-denominator` miss. Correct marginal statement, approved by L1: each of N1/N2 is separated by exactly one case and that case is new; zero-denominator also separates N4, but N4 was already killed by held controls.
3. Assignment labels measurement receipts “Committed receipts (re-read, do not rewrite)”. At observation, HEAD was `1459cca11fb5d3956a6e9a128217852dd0c28cb9`; `git show HEAD:.ufo/waves/round-73/measurement-c1-r73.txt` returned `fatal: path '.ufo/waves/round-73/measurement-c1-r73.txt' exists on disk, but not in 'HEAD'`, rc 128. L1 confirmed these receipts await its wave-evidence commit. Draft explicitly calls R73 an inspected on-disk receipt, not committed evidence at the time of reading.
4. Repair involved product parser changes and selftest regressions, not a frozen-control expansion. The repair also tightened failure-line grammar; the entry marks that separate change outside C1's specific target.

## Exact shell commands and outcomes

All git commands ran with cwd `/home/vgpnk/Projects/shokunin/mado-shokunin`; none writes git state.

| Command | Outcome |
|---|---|
| `git show d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce:.ufo/waves/round-72/w1/R72MutBattery.md` | rc 128; requested short path absent |
| `git show 4f598cfd --` | rc 0; full repair diff and repair receipt |
| `git ls-tree -r --name-only d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce .ufo/waves/round-72/w1` | rc 0; resolved actual battery path |
| `git log --all --format='%H %s' -- .ufo/waves/round-72/w1/R72MutBattery.md` | rc 0; no history for incorrect path |
| `git show HEAD:.ufo/waves/round-73/measurement-c1-r73.txt` | rc 128; receipt exists on disk but not at HEAD |
| `git log -1 --format='%H %s' -- .ufo/waves/round-73/measurement-c1-r73.txt .ufo/waves/round-73/measurement-c2-r73.txt .ufo/waves/round-73/control-baseline-r73.txt` | rc 0; freeze commit `87e4c61ac90e9ac587c9f65ac7844ded268d9046` |
| `git show d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce:.ufo/waves/round-72/w1/R72MutBattery/R72MutBattery.md` | rc 0; committed battery and GAP-1 |
| `git show 87e4c61ac90e9ac587c9f65ac7844ded268d9046:.ufo/waves/round-73/control-baseline-r73.txt` | rc 0; pre-freeze baseline |
| `git show 1459cca11fb5d3956a6e9a128217852dd0c28cb9:.ufo/waves/round-73/controls/c1-outcomes-r73.json` | rc 0; ten frozen cases |
| `git rev-parse HEAD` | rc 0; `1459cca11fb5d3956a6e9a128217852dd0c28cb9` |
| `mkdir -p /fast/scratch/hyaku/mado-r73/R73ScribeEntryC1/` | rc 0; explicitly assigned scratch created |
| `rmdir /fast/scratch/hyaku/mado-r73/R73ScribeEntryC1/` | rc 0; unused empty scratch deleted |

Specialized read tools additionally inspected D73 first, the three round-73 receipts, D72 erratum, actual M72 battery, frozen JSON, godspeed skill, and self-evaluation skill. Specialized write/edit tools authored the draft and this report; one locator correction changed `Lines 1–12` to `Lines 1–11`.

## Touched surfaces and cleanup disclosure

Permanent artifacts are only the draft and this requested report path (the report path is explicitly named by the seat assignment, despite being outside the seat's nested directory).

One accidental empty-file write used the doubled path `/home/vgpnk/Projects/shokunin/mado-shokunin/mado-shokunin/.ufo/waves/round-73/w1/R73ScribeEntryC1/draft/corpus/knowledge/control-set-mutant-kill-r73.md`. It contained zero bytes. The owned file was deleted immediately with specialized edit `REM`; no product content was changed. Exact cleanup command: `rmdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/mado-shokunin/.ufo/waves/round-73/w1/R73ScribeEntryC1/draft/corpus/knowledge`; it removed the accidentally created empty directory chain and stopped at the existing nonempty actual repo root with rc 1, `Directory not empty`. This transient write exceeded the intended write surface and is disclosed rather than represented as perfect boundary compliance.

No tool install/update; no product edit, git mutation, dispatch, host probe, runtime invocation, credential access, or publication.

## Limits and handoff

No full-harness execution or no-harm gate is claimed. Source digests are quoted from existing receipts, not recomputed. The entry is a draft for L1 adoption only. L1 should retain the actual receipt-containing commit in its final evidence provenance and run whatever final checks its main assignment authorizes; none were delegated to this scribe.

## Self-evaluation

| Axis | Score | Evidence / improvement |
|---|---:|---|
| Accuracy | 4/5 | Distinguishes marginal versus total kills and receipt versus commit provenance; rc remains assignment-reported. |
| Completeness | 4/5 | Requested entry length, tables, trio, historical repair and limits present; transient write-bound incident is disclosed. |
| Clarity | 4/5 | Tables resolve N4 overlap; long digest/source tables trade brevity for auditability. |
| Actionability | 4/5 | Exact draft path and reference command supplied; adoption intentionally reserved to L1. |
| Conciseness | 4/5 | 158-line entry fits 120–220 bound; provenance tables are deliberately detailed. |

Overall 4.0/5. Highest-impact improvements: retain receipt commit after L1 records it; avoid path-prefix duplication in artifact writes. Would the user agree? Likely with the provenance caveat and transient boundary incident made explicit.

Report: .ufo/waves/round-73/w1/R73ScribeEntryC1.md
Drafted the 158-line C1 knowledge entry with provenance and mutation tables.
Resolved source-path, marginal-kill, and receipt-commit discrepancies without changing evidence.
No measurements rerun; scratch removed; transient erroneous empty write cleaned and disclosed.
