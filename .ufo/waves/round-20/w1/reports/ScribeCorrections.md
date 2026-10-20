# ScribeCorrections — drafted six append-only correction items; two counts corrected, one dead-seat count not reproduced

Scope: draft correction blocks for `SCORECARD.md` (new round-20 "corrections to round 19" section) and the round-20 lesson, written only to `.ufo/waves/round-20/w1/drafts/ScribeCorrections.md`. No lane file, SCORECARD, round-19 lesson, closure file, tool, or gate was edited. No checks were executed beyond read-only reads of committed bytes and receipts.

Draft: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/drafts/ScribeCorrections.md` (sha256 `b59e3209…d08e4`).

## Findings

| ID | Round-19 statement | Measured now | Disposition in draft |
|---|---|---|---|
| R19-V1 | C1 target ≥21/29 "missed by decision" via criterion-24 reframing | Closure census 18/26 → 20/28 (`corpus/lessons/round-19-verifier-spotcheck.md:47`); reframing is not a hit | Miss stands; no redefinition |
| R19-V2 | "5/13 name S096 on the crediting line" (`SCORECARD.md:1167`, from `w2/reports/RerunC2.md:71` at `01b8094`) | At `b435568` (= `7b4839d`, = `e629f73` for these files): **8/13 any-line**, **6/13 first-line**; five files cite only S090: `arc-synthesis.md:392`, `closeout-r11.md:299`, `config-health-report-r3.md:1009`, `waybar-walker-plane.md:479`, `waybar-walker-semantics.md:467` | Corrected; "all files cite S096" unmet; S096 = provenance pin, not behaviour |
| R19-V4 | "155 round-19 transcripts" (`corpus/lessons/round-19.md:124`) | Receipt `evidence/final/tripwire-seat-scan.txt` JSON `files` length **154** (`json.load`); fail-open `inns.sh` chain at `w2/reports/SentinelGatePath.md:77-79`; scan blind to script-wrapped probe (`round-19.md:127-129`) | Corrected to 154; fail-open recorded; captured-by = self-report only |
| R19-V5 | "ten old OM10 assertions" (`SCORECARD.md:1225-1226`) | `git show 9c54c56:tools/mado-verify.sh` labeled OM10 occurrences at lines 839–848: **9 occurrences, 8 distinct**; `b435568` has OM10A six (900–906) + OM10B eight (913–922) | Corrected to nine (eight distinct) |
| R19-V6 | QualityDraft misroot; "25 dead seats" | Misroot files present in lane (`drafts/QualityDraft.md`, `w1/reports/QualityDraft.md`); registry 86 members, 62 `.md` reports; `item`/`agentId` join keys null | Misroot recorded; 25 **not reproduced** (86−62=24 one-to-one) → [UNK] |
| R19-V3 | (not in closure list) — not drafted | — | out of this seat's item |

## Verification performed (read-only)

- `python3` over `git show` of committed bytes at `9c54c56`, `b435568`, `7b4839d`, `e629f73`: fixed set of 13 files at baseline (matches closure); tally above, identical at all three revisions. Script: `/tmp/scribe-cc/s096.py` (scratch; `/tmp`, not in lane).
- `git grep`/`git show` for the OM10 labels at `9c54c56` and `b435568`; `git merge-base --is-ancestor b435568 refs/heads/master` → ancestor (master `e629f73`).
- `json.load` on `.ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt` (one JSON line; `files` = 154).
- Registry `.ufo/waves/round-19/w1/reports/swarm-registry.json`: `members` dict, 86 entries.
- Tool hash confirmed: `tools/mado-tripwire.py` = `367be947…`. Not the tool under test here; cited only as the receipt's binding.

## Limits

- Did not re-run `measure.py`, `tw-recall.py`, the gate, or any tripwire suite; C1/C2/C3 figures are cited from the closure and the committed receipts.
- The `5/13` figure is correct for `01b8094` under RerunC2's own definition; I did not re-measure at `01b8094`, so the statement "5/13 was the snapshot value" is from the report text [UNK as independent measurement].
- The exact first command that ran in the R19-V4 incident is taken from the closure transcript and the lane report; `SentinelGatePath.md` cites two harness forms (`--map-current-user` at :77 vs `--map-root-user` at :32). Which was first is [UNK] beyond the report text.
- No host-state check was made; host state change after the probe is unmeasured (closure line 124).
- The round-20 lesson file does not exist at this tip, so block (B) is staged text for L1 to place.
- The dead-seat count depends on a join key the registry does not store; 25 vs 24 is unresolved.
- R19-V3 (rule-B precision) is not in this seat's item and was not drafted.

## Installs

none (no tool installed or updated; only `python3` standard library and `git` read-only, `/tmp` scratch)
