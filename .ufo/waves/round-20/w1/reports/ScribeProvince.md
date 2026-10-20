# ScribeProvince — no PROVINCE.md line changes; two corpus/README.md additions drafted for the new tripwire note

Scope: draft only. Output is `.ufo/waves/round-20/w1/drafts/ScribeProvince.md`; no tracked file was edited.

## Findings

1. **PROVINCE.md: no line must change.** The tripwire (`tools/mado-tripwire.py`), its precision suite, the isolation check and QUALITY criteria 29–30 are lane tooling or corpus text, not province surfaces. `PROVINCE.md` `Owns`/`Refuses` name config trees, secrets, endpoints and quality only. Evidence: `git show e629f73:PROVINCE.md | grep -ci tripwire` = 0; PROVINCE.md sha256 prefix `1b25bb1e980925b3` (e629f73).
2. **corpus/README.md existing lines: none must change.**
   - `## Quality bar` (lines 47–50) cites `QUALITY.md` with no criterion count; criteria 29–30 don't alter that statement.
   - Lines 69–76 (`tools/mado-verify.sh --no-live`): the gate does not reference the tripwire (`git show e629f73:tools/mado-verify.sh | grep -ci tripwire` = 0), and round 20 does not change the gate.
   - Coverage-map and Frontier rows for rounds 1–19 remain true.
3. **New note row (drafted):** the new note is `corpus/knowledge/tripwire-precision-r20.md` (ScribeKnowledge's spec). Drafted two additions:
   - Coverage-map row to insert after line 45 (after `theme-route-r18.md`). Precedent: gate/tooling notes already appear in the index (`gate-standing-use.md`, `gate-mutation-proof.md`, `snapshot-diff-receipt-r9.md`).
   - Frontier bullet to append after line 150 (end of the round-19 bullet). It states round 20 moves no province surface, names the observed/lead boundary, keeps the still-open list unchanged, and says a clean scan is not evidence that no command ran.
   The bullet is worded as pre-registered and pending L1 verification; it claims no landed repair.
4. **Dependency:** the row and bullet cite the note's path and `S1xx-pending` ids. If ScribeKnowledge retitles the note, both lines must follow. No SOURCES rows are assigned here (reserved S099–S110 are L1's).

## Evidence pointers

- Draft: `.ufo/waves/round-20/w1/drafts/ScribeProvince.md` (sha256 not recorded; written by `write`).
- Province reads: `PROVINCE.md` (full, incl. round-19 refinement at line 18); `corpus/README.md` lines 1–150 (`## Frontier` at line 78; round-19 bullet at lines 136–150).
- Pre-registration read: `SCORECARD.md` `## Round 20 — declared claims` (line 1228 onward) and `corpus/lessons/round-19-verifier-spotcheck.md` §"Routed defects" (R19-V1–V6).
- Spec: `.ufo/waves/round-20/w1/spec.json` ScribeProvince entry; ScribeKnowledge entry names `corpus/knowledge/tripwire-precision-r20.md`.
- Hashes at e629f73 (sha256 prefixes): PROVINCE.md `1b25bb1e980925b3`, corpus/README.md `c38227ff7339f974`, corpus/QUALITY.md `461bcde2f5e75ace` (28 numbered criteria at e629f73).

## Limits

- Did not read any sibling draft (ScribeKnowledge's note, ScribeQuality's criteria, ScribeSkill's tripwire text); the row and bullet are drafted from the spec's description and need a check against the final note header.
- Did not verify the round-20 tool or suites; the bullet's "pre-registered" wording is from SCORECARD, not measured.
- Did not run the tripwire, counter, or any gate; no host command was run. Read-only git and file reads only.
- The coverage-map row placement assumes the index is chronological (it is, by round); L1 may prefer a different slot.
- Frontier bullet length: the README has long bullet lines already; I kept the bullet shorter than round 19's but did not check rendered width.

## Installs

none
