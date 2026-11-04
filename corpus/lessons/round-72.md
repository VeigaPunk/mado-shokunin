# mado round 72 — lesson

author: mado L1 (the scored instruments are the L1's own; the one w1 wave's seats attack them).
date: 2026-11-04 (America/Sao_Paulo)
base: `976684a27e99c2508037a60eec415f550f53d70e`
frozen declaration: `.ufo/waves/round-72/claims-declaration-r72.md`, `5601e5269bdc365213507604357375a74fe61fe1`
control sets: `.ufo/waves/round-72/controls/c1-modes-r72.json` sha256
`18144745d65a00e1d812c663dbace402a5714fde74506f54d9adabe858268c13` and
`.ufo/waves/round-72/controls/c2-controls-r72.json` sha256
`640fb44fdb1f31b4706b381c905fde4b5dae769bfd3e5b656bdb374bad58a793`
pre-freeze baselines: `.ufo/waves/round-72/control-baseline-c1-r72.txt` (held 6/8) and
`.ufo/waves/round-72/control-baseline-c2-r72.txt` (held 4/8)
measured content: `9bcb4fd5b598844f168230dc05e441721d95b272` (both instruments; measurement
`.ufo/waves/round-72/measurement-c1-r72.txt` and `measurement-c2-r72.txt`)

## Outcome and boundaries

Two bounded claims, both frozen before any candidate data; both `TARGET_MET` at the measured
content with the do-nothing controls at their declared scores.

- **C1 calibration — the kill credit requires the run's own failure detail.** `credit(out)` in
  `quality/counters/c1-r72-landing-controls.py` credits the M-Z kill only when the last parsed
  `MADO_LANDING_COUNTERS_SELFTEST: p/n` summary reports `n > 0` and `p < n` **and** the run's own
  `SELFTEST FAIL` lines number exactly `n − p`. Measured by
  `quality/counters/c1-r72-summary-credit.py`: eight real `bash` fixture modes, `correct=8
  base_correct=6 verdict=TARGET_MET` rc 0; the held round-71 harness credits two shapes it must
  not (`bare-failing`, `mismatch-detail`).
- **C2 operability — the outcome reads the gate's summary, not its exit status.**
  `summary_green(out)`/`outcome_verdict(selftest_out, killed)` green a run only when the last
  parsed summary has `n > 0` and `p == n` and the kill count is 2/2. Measured by
  `quality/counters/c2-r72-outcome.py`: eight frozen `(gate_out, gate_rc, killed)` cases,
  `correct=8 base_correct=4 verdict=TARGET_MET` rc 0; the held rule is wrong on four cases, in
  both directions.

**Not claimed.** That the arithmetic check authenticates a summary (a captured summary replayed
with its own matching detail lines stays byte-indistinguishable); that eight modes or eight cases
exhaust the summary grammar; that the fixture lane is the lane's real landing instrument; that
the counters execute a whole harness end to end (C2's scores the committed functions); any
desktop, compositor, session or service behaviour (none was probed); any `[x]`, promotion or axis
retirement. The r71 guard-census widening (r71 plan item 2) is deferred, not claimed.

## Mistakes

| mistake | class | evidence | captured-by | fix and the failure it can now show |
|---|---|---|---|---|
| M72-1: the round-71 reject (`stdtypes.rst`) existed only as Gate prose, not as a `rejected` registry row, so the taste it evidences was not durable (routed by the r71 spot-check, item 4). | landing | `corpus/lessons/round-71-verifier-spotcheck.md` § Discernment, row `Reject curation`; `grep -n stdtypes corpus/SOURCES.md` was 0 rows. | `none` — CORPUS § Shape says a rejection stays as a row with reason and flip; no lane criterion checked that the Gate's rejects are mirrored into the registry. | S446 lands as a `rejected` row with the reason and flip. The failure it can show: a Gate reject whose URL has no `rejected` row is now visible as a diff between the lesson's Gate block and the registry; round 72's own Gate mirrors all three verdicts. |
| M72-2: the r71 lesson claimed an "11 words" quote for a sentence that is 10 words. | number-drift | `corpus/lessons/round-71.md` § Gate quote A vs the fetched `subprocess.rst:53` sentence; the spot-check counted 10. | r71's own Gate block, which the spot-check re-opened; no criterion required a word count to be machine-derived. | This round's Gate quotes are ≤25 words and counted by `awk '{print NF}'` on the quoted span (receipts under `.ufo/waves/round-72/fetch/`); a wrong count is now a visible mismatch against that command. |
| M72-3: the r71 reject cited `Doc/library/stdtypes.rst`, which 404s at tag v3.14.8 (3.14 moved the file to `Doc/builtins/`). | reference-drift | `curl -fsSL …/Doc/library/stdtypes.rst` rc 22 ×3 this round; the real path returns 248,201 bytes. | `none` — the r71 Gate recorded its access date but the URL was never re-resolved after the tag-pinned path moved; the anchor rule names a path, not a resolution check. | S446 anchors at the real 3.14 path and records the 404. The failure it can show: any future row whose cited URL does not resolve at its pinned tag is now a `curl` rc 22 against the fetch receipt, not a prose claim. |
| M72-4: r71's harm-watch recorded `rc=0` for a leg that died as a setup error (the frozen round-70 counter's `--round 70` default), and the report still asserted `TARGET_MET` at the tip. | landing | `corpus/lessons/round-71-verifier-spotcheck.md` § Conformance defects; `.ufo/waves/round-71/harm-watch-r71.txt`. | QUALITY criterion needed: a receipt line's rc must be the command's rc, and a setup error must not be readable as a pass. No criterion said so before this round. | QUALITY 116(b) makes a receipt's rc the measured value; this round's harm watch records each command's own rc and prints the failing text instead of a verdict word. |

A fix counts only on its named red/green evidence: M72-1's green is S446's registry row (red was
`grep -n 'stdtypes' corpus/SOURCES.md` → nothing); M72-2's green is the word-count command on the
Gate quotes (red was the r71 text); M72-3's green is the real-path fetch (red was rc 22 ×3);
M72-4's green is this round's harm-watch receipt with per-command rc (red is the r71 line whose
rc does not match its own error text).

## Gate

Admitted, **S444** — CPython v3.14.8 `Doc/library/unittest.rst`, § `TestResult`, `wasSuccessful()`.

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/unittest.rst`
- Access date: 2026-11-04, fetched three times, byte-identical (sha256
  `d6522f68c29c8ced8d2d81c91cb41ac739f855e6c0b9831f4a0e5a81f7ae5b86`, 107,372 bytes; receipts
  `.ufo/waves/round-72/fetch/Doc_library_unittest.rst.{1,2,3}`).
- Located quote, 14 words, unittest.rst:2129-2130: "Return ``True`` if all tests run so far have
  passed, otherwise returns ``False``."
- Why it grounds C2: the pass/fail fact is a read of the result object — exactly the summary the
  successor parses — and not the runner's status.

Admitted, **S445** — CPython v3.14.8 `Lib/unittest/main.py`, the runner's exit derivation.

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/unittest/main.py`
- Access date: 2026-11-04, three times byte-identical (sha256
  `12de7da0fea92dbff8713ebe9904ada6dbd1e0a334d58861c6287ccfc0a261d2`, 11,660 bytes).
- Located quote, main.py:272-273 (inside `if self.exit:` at :271):
  `if not self.result.wasSuccessful(): sys.exit(1)` — 9 words of code, quoted as a statement.
- Why it grounds C2: the official runner's process status is *derived* from `wasSuccessful()`,
  so a status carries no assertion result beyond the result object it was computed from.

Rejected and curated, **S446** — CPython 3.14.8 `Doc/builtins/stdtypes.rst` (Mapping Types —
`dict`, `update(**kwargs)` at :5529, `setdefault` at :5523).

- URL opened at its real 3.14 path on 2026-11-04, three times byte-identical (sha256
  `5a6951b72ecc630a87f45a650fc11c186cfeb4251bedd1ea28f45bcb3116e8e1`, 248,201 bytes); the
  round-71 citation `Doc/library/stdtypes.rst` returned HTTP 404 on all three attempts (rc 22).
- Reason: it documents method behaviour (argument forms, defaults), not call-site or
  result-object semantics; no admitted entry needs it. Flip condition: a claim whose subject is
  mapping-method behaviour re-opens it.
- This row is the repair of the round-71 routed defect: the r71 rejection now exists as a
  registry row with reason and flip, not only as Gate prose.

Registry cell changes (old → new, logged per CORPUS rule 2; only `used-by` changed):

- **S442** `used-by` `corpus/knowledge/kill-credit-exit-disagreement-r71.md,corpus/lessons/round-71.md`
  → `…,corpus/knowledge/summary-credit-own-detail-r72.md`;
- S444 and S445 enter `mined` with `used-by corpus/knowledge/outcome-verdict-gate-summary-r72.md`;
  S446 enters `rejected` with `used-by —`.

No `status` or `recheck` cell changed on any held row. Registry 380 → 383 rows; census
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` exit 0 both at
round start (380) and at round end (383), with the held W04 superseding-URL warnings only.

**Spot-check duty.** The in-round wave seats are the lane's own; the non-author spot-check of
this round's gate decisions (at least one admit and one reject) is the closure's, per LEARNING.md.
The two admits and the one reject are handed over with their URLs, dates and quotes above.

## Addendum — wave review findings and the repair (append-only)

The wave's `R72RevC1` (F1 P2, F2 P3) and `R72CriticClaims` (Counterexample B) found the
implementation wider/narrower than the frozen sentence: the first successor selected the last
prefix-matching line and then rejected it, so a malformed trailing marker suppressed a valid
summary; and `count_fails` counted `SELFTEST FAILURE:` as a fail line. Repaired at `4f598cfd`:
`last_parsed_summary()` scans for the last full match, `count_fails()` matches the production
grammar `SELFTEST FAIL <i>: `, both repros are selftest regressions, and the red-before/green-
after pair is `.ufo/waves/round-72/receipts/c1-r72-repair.txt`. The frozen eight-case sets
score identically at the repair (`.ufo/waves/round-72/receipts/re-measure-r72.txt`).

`R72RevC2`'s Medium finding stands as a **declared limit**: the harness reads `stdout + stderr`
in the r71 capture order, so "last" is last in the captured concatenation, not interleaved
chronological last; separate pipes cannot be interleaved after the fact. `CriticClaims`
Counterexample A stands as a **finite-set statement**: the C2 eight cases carry no
zero-denominator case (the successor's `total > 0` guard is selftest-covered, not frozen-set
covered), and a later round adds those controls under a new denominator.
