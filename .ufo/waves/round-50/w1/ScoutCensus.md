# ScoutCensus — source census

## Verdict

**Candidate rows fail the required scratch-mirror validation as tested.** All 12 candidate lines have 11 table fields (13 pipe-separated fields including outer delimiters); none creates E03 or E04. However the appended rows are outside the `## Registry` section because `candidate/rows.md` rows were concatenated after the complete registry file, and validator emits E12 for every S352–S363. Therefore this is not an acceptable clean candidate validation; the test must put these rows within Registry to assess the intended rows. No new W01/W04 warning attributable to the candidate was observed. The candidate's 12 cited `used-by` values refer to corpus/knowledge paths not present in this scratch mirror context, which produces many E11 findings for existing registry entries; the `--file` mode resolves used-by paths relative to the mirror's parent, not the lane root. E11 output is therefore not evidence of candidate row defects.

## Commands and observations

- Required lane census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` returned the 18 baseline warnings and `mado ok` (exit 0). It matches `.ufo/waves/round-50/receipts/census-before.txt` exactly except that receipt line 20 records `exit=0`.
- Scratch `--file` mirror made under `/fast/scratch/hyaku/mado-r50/ScoutCensus/`, using a copy of `corpus/SOURCES.md` with candidate rows appended; validation output included E12 for S352 through S363 and E11 for absent used-by targets; exit 1. Scratch was removed after the run.
- Width check: `awk -F'|' '{print $2, NF}' candidate/rows.md` reported S352–S363 each with `NF=13`, i.e. 11 cells. E03/E04 were absent in the candidate output.
- The 18 baseline warnings are unchanged: W04 cross-scope duplicate URLs on S030, S042, S045, S097, S119, S120, S121, S303, S307, S317, S318, S320, S321, S324, S326, S327, S332; W01 tier-C mined row S277 with a used-by path. The baseline receipt records precisely these warnings. They predate and are independent of candidate rows.

## Interpretation / remaining gap

The check does not establish the desired registry-context result because the `--file` candidate rows were appended outside the Registry section. Validator source `scripts/sources-census.sh:618-624` explicitly classifies row-shaped sources there as E12. A proper follow-up mirror must insert the candidate lines before the next top-level section after `## Registry`, and provide the lane tree context needed for E11 used-by checks (or report those separately). The requested candidate `--file` result cannot be called clean from this run.
