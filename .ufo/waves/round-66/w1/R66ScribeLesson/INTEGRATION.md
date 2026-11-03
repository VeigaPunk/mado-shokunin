# R66ScribeLesson — integration map

All snippets below are drafts for L1 integration. This seat wrote no lane file outside
`.ufo/waves/round-66/w1/R66ScribeLesson/` (plus the seat-spec report copy at
`.ufo/waves/round-66/w1/R66ScribeLesson.md`).

| draft | destination | insertion point | notes |
|---|---|---|---|
| `round-66.md` | `corpus/lessons/round-66.md` | new file | The lesson references `corpus/lessons/round-66.md` from S435's `used-by`; land the lesson before or with the source row or the census E11 fires. |
| `quality-append-108.md` | `corpus/QUALITY.md` | append after criterion 107 (EOF) | Numbering continues at 108; contains one criterion plus declared limits. |
| `skill-registry-additions.md` | `SKILL.md` | `## Gate registry` table (header `:692`), or a dated `## Round 66` append | Three rows: C1 counter, C2 driver, hardened landing instrument with the a–d verdict map. |
| `tool-ledger-additions.md` | `quality/tool-ledger.md` | append after the current last row (`:144`) | Two rows. Expected integrated population 108/108 only after both files are installed under `quality/counters/`. |
| `province-instrument-addendum.md` | `PROVINCE.md` | immediately after the round-65 refinement paragraph (`:276`) | Append-only instrument accounting; no new write surface. |
| `scribe-evidence.txt` | retained in this seat dir | n/a | Every command with its own captured rc; `evidence.sh` reproduces it. |

## Integration order that keeps the evidence honest

1. Install the committed candidates at their production paths:
   `quality/counters/c1-r66-register.py`,
   `quality/counters/c2-r66-landing-instrument.py`, `quality/landing-counters.sh`.
2. Re-pin the draft hashes and assertion counts at the integration revision. At this seat's final
   read the values were: C1 `4e1b94ff…`, 15/15; landing `1671cebc…`, 58/58 (the wave moved it
   `f72e579d…`/46 -> `f0c8d74f…`/56 -> `1671cebc…`/58; no final count is pinned).
3. Append the two ledger rows, then run
   `python3 quality/check-tool-ledger.py --repo . --rev <integrated-rev>` and require
   `population=108 ledger_rows=108 … verdict=TARGET_MET`. That is a prediction, not an observation.
4. Append the SKILL rows, the PROVINCE paragraph and QUALITY 108.
5. Land the lesson and the S435 row together, then run the census end. S435's `used-by` names
   `corpus/lessons/round-66.md`; a row landing first is an E11.
6. Run the frozen controls (`check-controls.py --claim c1` and `--claim c2`) and the committed
   four-leg landing. The C2 count must also run the candidate selftest and a real four-leg landing;
   its a-d `correct=4/4` alone over-credits the claim (`.ufo/waves/round-66/w1/R66CriticLanding.md`
   F1). Their results, not this seat's copies, are the C1/C2 gate evidence.

## Frozen and out of scope

- `quality/counters/c1-r65-register.py` and `quality/counters/c2-r65-landing-instrument.py` keep
  their frozen bytes; r66 adds successors and never edits them. The C1 baseline control runs the
  r65 counter at the same revision.
- No admission, promotion, census-end, or committed-landing claim is made by this seat.
- Marker checking is structural, not truth binding: register state cells stay unmeasured.
