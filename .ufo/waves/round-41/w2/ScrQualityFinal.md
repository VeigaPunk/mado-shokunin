# ScrQualityFinal — report (mado round 41, w2)

Seat `ScrQualityFinal` (scribe, leaf). Target: final text for QUALITY.md criteria 69+,
`corpus/QUALITY.md` append candidate. Final deliverable: `.ufo/waves/round-41/w2/ScrQualityFinal/criteria.md`.

## What this seat produced

- **criteria.md** — final text for criteria **69–75**, numbered continuously, same shape as 60–68
  (rule, `Check:`, `Shown able to fail:`, `(lesson: lessons/round-41.md#mistakes M41-n)`):
  - 69–72: the four w1 drafts of seat `ScrQualityCriteria`, finalized; lesson pointers set to the
    round-41 ids the lesson's `### QUALITY.md criteria` section requires (69→M41-4, 70→M41-3,
    71→M41-8, 72→M41-1). 72 additionally names the round-41 two-site row `M09-expect-not-deduped`.
  - 73: sandbox hides the stub payload (compiled execute-only live stub, no plaintext copy) —
    CH1/CH2 + controls `K01`/`K02` (verified killed at `ctl-c1-v2.txt:49-50`, 33/39).
  - 74: teeth clause b2 paired with neutrality clause b3 and exact-name exclusion —
    CH6/CH9/CH10 + controls `K05`/`K07` (verified killed at `ctl-c1-v2.txt:53,55`).
  - 75: parser contract states digit classes, numeric-vs-string comparison, format scope; silent
    `NO_SESSIONS` on unrecognized input is a defect — ExecDiffFuzz F1-F3, ExecJournalFormat, fixtures
    `vernum0`/`pidzeros0`/`asciidigits0`/`unicodename0`/`unrec0`/`mixed0`; controls `W1-N12`,
    `W1-N23`, `K03` (verified killed at `ctl-c1-v2.txt:83,64,51`).
- **verify-quotes.py** + **quotes-check.txt** — every quoted fragment in criteria.md (19/19) is
  verified against committed bytes read at `07f264…` (`git show`), each ≤ 25 words and located.

## Evidence grounding (read-only; all bytes committed at 07f264)

- v2 counter docstring/clauses: `quality/counters/c1-r41-globals-v2.py` (a/b/b2/b3/g, stub build
  `build_stub` chmod 0o111/0o131, `prepare` live branch writes no journal, teeth `function_sites`
  exact-name exclusion + forced summary-site, neutrality `neutrality` comment/unparse variants).
- Tool contract: `tools/mado-globals.py:13-16` ("The grammar is `journalctl -o short-iso` only",
  "UNRECOGNIZED_FORMAT (exit 4), never a silent NO_SESSIONS").
- Wave-1 findings: `w1/CritC1Cheat.md` (CH1 24/24, CH2 21/24, CH6/CH9/CH10 24/24),
  `w1/ExecDiffFuzz.md` (F1/F2/F3 variants scored 24/24; `accepted_versions=[1..9]…`),
  `w1/ExecJournalFormat.md` (five of six `-o` formats silent `NO_SESSIONS` rc 3 stderr 0).
- Control receipts: `.ufo/waves/round-41/receipts/ctl-c1-v2.txt` (K01 :49, K02 :50, K05 :53,
  K07 :55, K03 :51, W1-N12 :83, W1-N23 :64; overall 95/95 correct, 4 skipped absent-pattern
  controls) and `c1-v2-after-data.txt` (clauses line :50; `unrec0` :48).
- Verification commands run: `git show 07f264…:<path>` for every cited file;
  `python3 verify-quotes.py` (output in `quotes-check.txt`, 19/19 OK).

## Findings

- **No defect found** in the sources used for the draft: every cited control, clause line, fixture
  and score exists in committed bytes and matches the numbers quoted. No DATA defect to route.
- **Assumption flagged for the L1**: the committed lesson carries M41-1..8 only; the findings
  criteria 73–75 close are the `M41-9..` rows seat `ScrMistakesV2` drafts. This draft cites
  M41-10 (73), M41-9 (74), M41-9 + M41-11 (75) per the w2-spec enumeration order. If that seat
  lands different ids, renumber only the parentheticals; the bodies name committed evidence
  independent of the ids.

## Safety / limits

- Wrote only inside `.ufo/waves/round-41/w2/ScrQualityFinal/` and the report file
  `.ufo/waves/round-41/w2/ScrQualityFinal.md`. No tracked file edited; no git/jj mutation;
  no pacman/host-service/compositor contact; no journal verb beyond read-only `journalctl` (none
  even needed); no subagent dispatch, no background jobs.
- Tooling: **nothing installed** (system `python3` 3.14 only; no package transaction).
- Not verified: the check commands in criteria 69–72 were executed by w1 seat `ScrQualityCriteria`
  (its receipts are committed); this seat did not re-run them (they are integration-time checks
  against future rounds' inputs).

Report: `.ufo/waves/round-41/w2/ScrQualityFinal.md`
