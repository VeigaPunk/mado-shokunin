# MeasureBuild — round-15 C1 structural counter

Status: **implemented, not executed**. The lane forbids tests, smoke runs and
live probes, so this report is a static review of the delivered probe and the
inputs it will read. No gate, libinput tool, hyprctl call, device read, event
observation or compositor action was performed.

## Files changed

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/measure.py`
  (new, 295 lines, sha256
  `dc42a7942f73e630378c1809f89bd94f9c7417f31ad16abc4a305c406728311b`).
- This report only. No source registry, corpus note, README, SCORECARD, LOG,
  gate, fixture or configuration file was written.

## Behavior

- Revision binding matches round-14: argv revision -> `git rev-parse --verify
  <rev>^{commit}`, then every input (`tools/mado-verify.sh`,
  `corpus/SOURCES.md`, `corpus/README.md`, each `corpus/knowledge/*.md`) is
  read with `git show <resolved-sha>:<path>`. The working tree is not an input.
- C1 join semantics are preserved from
  `.ufo/waves/round-14/measure.py:104-215`: provenance trio (`source:`,
  `verified-at:`, `recheck:` in the head 15 lines), exactly one
  `covers: U[1-7]` line, cited ids joined to `mined` registry rows whose
  `used-by` names the note, and at least one tier A/B mined row.
- U4 has its three unchanged facets (phase/S005, advertisement/S041,
  unexercised behavior/S043). U5 retains `body_facets()` unchanged plus
  S047/S048 reciprocal joins and the inverse rule covering every mined row
  that names the note.
- U6 adds exact level-2 headings `## Layer ladder`, `## Safe boundary`,
  `## Unexercised delivery`, and `[UNK]` inside the delivery section body.
  Level-3 headings remain part of their enclosing level-2 body. The pair is
  `S051`/`S052`; both must be present, `mined`, tier A/B, named in `used-by`,
  cited on the source line, and pass the same inverse rule. `S007` is not a
  required id and gets no credit.
- Output is JSON on stdout with `coverage.count`, `/7` score
  (`10 * count / 7`), per-item joins, `u4_facets`, `u5_candidates`,
  `u6_present`, `u6_facets`, `u6_candidates`, `navigation` (notes, indexed,
  missing, extra, duplicates), `source_registry` (row count, tier counts,
  status counts, `round15_required` for S051/S052) and
  `measure_inputs.gate_sha256` with `gate_executed: false`. The only process
  invoked is git; no gate or fixture command is executed.
- A zero/low coverage or absent U6 join is reported and the process exits 0.
  Only usage error exits 2.

## Source-id reconciliation retained

- Final pair after source review: **S051/S052**. S051 is the tagged libinput
  1.32.0 `tools.rst` replacement for the mutable latest-docs page; S052 is the
  core Wayland 1.26.0 XML input scope. Both must be mined reciprocal.
- The initial S007/S051 interim reconciliation is not implemented. S007 stays
  queued and receives no U6 credit because its composite `teaches` cell groups
  debug-events with kernel replay and mutable docs wording. The code docstring
  records this rejection/supersession rationale; the registry lesson remains
  L1's source correction.
- The current candidate draft
  `.ufo/waves/round-15/input-draft.txt:1-4` cites S007 and S051, and the
  current SOURCES registry has S007 `queued` and no S051/S052 rows. As-is that
  draft cannot admit U6. L1 must land the final note with `source:` citing
  S051/S052 plus reciprocal mined registry rows before the count can be 6/7.

## Retained evidence

- Round-14 join semantics read at
  `.ufo/waves/round-14/measure.py:1-163`, `:149-333`, `:319-473`, `:474-582`.
- Round-15 pre-registration read at `SCORECARD.md:580-610` (U6 headings,
  provenance trio, exactly `covers: U6`, reciprocal mined A/B joins, `/7`
  denominator, no gate execution).
- Candidate U6 body headings observed at
  `.ufo/waves/round-15/input-draft.txt:14` (`## Layer ladder`), `:66`
  (`## Safe boundary`), `:88` (`## Unexercised delivery`, `[UNK]` in body).
- Current registry state observed at `corpus/SOURCES.md:19` (S007 queued);
  read-only, not modified.
- L1 reconciliation directives: final required ids are S051/S052, not
  S007/S051 and not S051/S052-with-S007-credit.

## Risks and limits

- **Not executed.** Static review only. L1 should run
  `python3 .ufo/waves/round-15/measure.py <REV>` at the measured revision.
- The probe measures structure, not source or body truth; L1's semantic review
  still owns admission. `[UNK]` is tested in the delivery section body, not by
  the section's absolute position in the note.
- `S051`/`S052` must be `mined` and reciprocal; a queued row, missing
  `used-by`, or uncited mined row suppresses U6 admission while leaving the
  exit code 0.
- Complete navigation requires the new note's README row exactly once;
  missing/extra/duplicates are reported, not repaired.
- The gate SHA-256 is computed from the revision-bound bytes with the
  round-14 text-decode convention and is reported for the harm watch. The gate
  is never run, so no selftest, file-plane or regression verdict is claimed.
- No tooling was installed or updated.
