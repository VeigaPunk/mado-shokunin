# ConnHistorical — r19/r20/r21 red receipts vs r22 registration

Seat `MadoR22.ConnHistorical`, connector, leaf. Read-only: I took SHA-256 hashes of existing artifacts only. I ran no scanner or detector, executed no payload, edited no production code and installed no tools. Machine-readable form: `.ufo/waves/round-22/w1/notes/ConnHistorical.json`.

## Outcome

The registration does not grant any re-admission. However, the C2 green target as worded ("green only when correctly scoped to five observed plus one lead", `registration.md:9`, `SCORECARD.md:1482`) **cannot be reached on faithful r19 bytes**. Every route to it rewrites old history. Three smaller record and guard gaps follow (H2–H4).

## Authoritative reds (unchanged)

| Round | MANIFEST | Verdict | Harmed |
|---|---|---|---|
| 19 | rounds[367] | rejected-harmed | operability (rule-B pure-data finding with no lead marker); C1 ≥21/29 missed |
| 20 | rounds[387] | rejected-harmed | operability; expansion/quality trends; calibration unprovable; 172/175 |
| 21 | rounds[400] | rejected-harmed | operability (F1–F5); quality trend; C2 bounded, no credit |

## H1 (high): the C2 r19 target is a rewrite path

- **The faithful r19 finding rows** are line 3 of `.ufo/waves/round-19/evidence/final/tripwire-frozen-scan-classes.txt`, committed at `d642ce5`. The file's SHA-256 is `64648cca…f857`; line 3 alone is `0ffc3e81…cc1e` (4431 B). They come from tool `367be947…` at `7b4839d`.
  - There are **11 rows** over the 6 incident lines: host_mutation 6, live_probe 1, package_query 4.
  - **0 of the 11 rows have an `evidence` key.** All rows carry class and command.
  - The 5 files all report error counters of 0.
- **The r19 counter receipt** (`tw-recall-after.txt`) has only `{file,line,detected}` rows. It has neither a findings list nor a files list, so it does not fit the audit contract.
- **The "5 observed + 1 lead" split exists only in r20 receipts from later tools**: `recall-split-final.txt` (tool `9613f510`) and `a2/recall-split-{3610e3e,a8960de}.txt`. It counts incident *lines*. At row level the same receipts give observed 10 + lead 1. Those rows also have no command strings.
- **The audit contract counts finding rows** and requires an explicit `observed|lead` marker on each.

So on faithful r19 rows, no claim of observed 5 / lead 1 can be consistent. Getting a green requires one of these, and each one rewrites r19 C3 so it looks correctly scoped after the fact:

1. adding markers to the r19 rows;
2. presenting an r20 rejected-round receipt as r19;
3. converting line counts into row counts;
4. a fresh scan with a marker-capable tool, which is a detector measurement and, with the C1 tool, breaks C2 independence.

**The rules for markerless rows also contradict each other:**

- The r20 counter treats an unmarked row as observed (`SCORECARD.md:1248`).
- The r22 contract says a missing marker is "uncertainty, never silently observed".
- The contract schema ("each explicit evidence") together with verdict 2 lets markerless r19 rows be read as invalid input. On that reading the registered "red" never arrives as code 1.

## H2 (medium): verdict labels softened

`registration.md:3` and the r21 MANIFEST notes call r19 and r20 "rejected". The MANIFEST verdict for both is **rejected-harmed**, and the r21 registration (`SCORECARD.md:1437`) says so.

## H3 (medium): a carried guard was dropped

The r20 closure (defect 1) requires keeping the 175-case population. r21 delivered **166/175** with the wants unchanged. The r22 guard list does not mention 175 or 166 at all, so C1 could lower 166/175 without any registered harm signal.

## H4 (low): no incident-split baseline at the r21 tool

r21 recorded only "six incident lines still detected". No split receipt exists at `a6cef89`, so the before value is UNKNOWN until it is measured after seal.

## Proposed move (one, bounded)

**Two-tier historical pin, frozen before any audit code exists.**

1. Freeze H19 as the verbatim line 3. Bind both digests and the extraction rule. Do not edit any row.
2. Choose now how markerless rows are read:
   - **Reading U:** they are uncertain. They count toward total but are neither observed nor lead.
   - **Reading I:** they are invalid input (code 2).
3. Freeze these H19 rows. Reading I gives code 2 for all four.

   | Claim | Reading U |
   |---|---|
   | total 6, observed 6 | 1: finding_count_mismatch + observed_count_mismatch |
   | total 6, observed 5, lead 1 | 1: finding_count_mismatch + observed_count_mismatch + lead_count_mismatch |
   | total 11, observed 0, lead 0, clean false | 0 |
   | total 11, observed 0, lead 0, clean true | 1: findings_claimed_clean |

4. Append a dated pre-seal correction. "Correctly scoped" on r19 bytes means 11/0/0. The 5+1 split is r20-tool line evidence and gives r19 no credit. Keep the original wording beside the correction.
5. If an r20 receipt is used at all, label it H20 with its own tool digest. Because its rows lack command strings, it reads code 2.
6. Quote every prior verdict as rejected-harmed (fixes H2).
7. Add 166/175 (P66 S17 W21 H47 L15) as a disclosed no-worse guard (fixes H3). Mark the r21 split UNKNOWN (H4).

**Axes:** calibration improves, because a rewrite path closes before seal. Operability and the other axes are unchanged; the 166/175 guard is disclosure only.

## Risks

- A pre-seal correction can look like a target-preserving swap, the r20 30′/M13 pattern. To avoid that, land it before any audit code, keep the original words, and leave the judgment to the closure.
- Choosing reading U or I after seeing results would be post-hoc. Freeze the choice now.
- Under reading U, a green on r19 means "no evidence tier proven". It is not a precision repair and not an admission.

## Verification (for implementers after seal; not run here)

- The two digests above, plus 11 rows of which 0 have an `evidence` key.
- The r20 split receipts show finding totals 10+1 and line totals 5+1.
- MANIFEST rounds[367], [387] and [400] all read rejected-harmed.
- `grep -nE '175|166' registration.md` returns no hits before the correction.
- The audit selftest on H19 rows 1–4 returns the frozen codes.

## Already sound (no rewrite found)

- The r19 ≥21/29 miss is kept as a miss.
- The r20 175/175 miss is kept, with 172/175 recorded as history and 166/175 as delivered.
- No capabilities were added in rounds 19–21. The r21 C2 row is marked as not admitted.
- The audit tool is absent at both the base and HEAD (exit 128).
- All six r21 FinalBindingReview fixtures still match their review digests.
- The r22 LOG append (not yet committed) already says the 5/1 translation is not a new execution receipt for the old markerless tool.
- An outside-lane falsification is required before any re-admission proposal.

## Unknowns

- The incident split at the r21 delivered tool.
- Which reading (U or I) L1 adopts.
- `w1/proposals/` was empty when I read it, so I could not check other seats' H19 representations.
