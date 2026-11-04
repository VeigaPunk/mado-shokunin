# mado round 72 — lesson

author: mado L1 (hyaku run 15, attempt 1). Skeleton drafted by wave seat R72ScribeLesson
2026-11-04; the prose lands as the L1's own — cells marked `<L1 fills>` await the L1's
committed bytes and are not evidence yet.
date: 2026-11-04 (America/Sao_Paulo)
base: `976684a27e99c2508037a60eec415f550f53d70e` (round-71 closure tip)
instruments: `9bcb4fd5b598844f168230dc05e441721d95b272` — candidate harness
`quality/counters/c1-r72-landing-controls.py` sha256
`d0d3bfd2b8306062e7ea7323377dea1371df93c4a9447a7a28c4927becfe7c62`; held base harness
`quality/counters/c1-r71-landing-controls.py` sha256
`f836499594fb4fa8898336b1a47241614bb2b9ddb6f93c369a9e00ece0f185f1`
frozen declaration: `.ufo/waves/round-72/claims-declaration-r72.md` (committed at
`5601e526` together with both control sets — `controls/c1-modes-r72.json` sha256
`18144745d65a00e1d812c663dbace402a5714fde74506f54d9adabe858268c13`,
`controls/c2-controls-r72.json` sha256
`640fb44fdb1f31b4706b381c905fde4b5dae769bfd3e5b656bdb374bad58a793` — and both held-leg
control baselines)
measurement: `.ufo/waves/round-72/measurement-c1-r72.txt` and
`.ufo/waves/round-72/measurement-c2-r72.txt` — both verdict `TARGET_MET` at rev
`9bcb4fd5b598844f168230dc05e441721d95b272`, `C1_RC=0` / `C2_RC=0`, committed at
`fd9ea03b`

## Outcome and boundaries

Two bounded claims, both frozen before any candidate data, causally separable **by
verification**: both rule deltas live in one successor harness file
(`quality/counters/c1-r72-landing-controls.py`, the r72 generation of the lane's harness
chain) because the lane's convention is one harness per round; C1's counting command
scores only the credit function, C2's only the outcome function, and neither counter
reads the other's control set. Each rule is independently revertible inside the file and
each has its own frozen denominator.

- **C1 calibration — the landing kill credit requires the run's own failure detail, not
  just a summary line.** At the instruments revision the frozen command
  `python3 -I quality/counters/c1-r72-summary-credit.py --repo . --rev
  9bcb4fd5b598844f168230dc05e441721d95b272 --base-rev
  976684a27e99c2508037a60eec415f550f53d70e --scratch-root DIR` printed as its last line
  `MADO_R72_SUMMARY_CREDIT: cases=8 correct=8 base_correct=6 verdict=TARGET_MET
  rev=9bcb4fd5b598844f168230dc05e441721d95b272`, rc 0. Frozen predicate: the M-Z kill is
  credited iff the **last** parsed `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions
  passed` summary has `n > 0` and `p < n`, **and** the run's own `SELFTEST FAIL` lines
  number exactly `n − p`; both captured streams are read (the round-71 rule is
  preserved). The held round-71 rule (`mz_killed = summary_shows_failure(out)` alone)
  scores the same frozen eight-mode set 6/8: credited wrong on exactly `bare-failing`
  (a summary line no assertion of this run produced) and `mismatch-detail` (a summary
  whose failure count is not backed by this run's fail lines) — receipt § each mode;
  the do-nothing control scored exactly 6/8 in the same run.
  `<L1 fills: reviewer deltas named after the wave settles, if any>`
- **C2 operability — the outcome verdict reads the gate's own summary, not its exit
  status.** At the same revision the frozen command `python3 -I
  quality/counters/c2-r72-outcome.py --repo . --rev
  9bcb4fd5b598844f168230dc05e441721d95b272 --base-rev
  976684a27e99c2508037a60eec415f550f53d70e --controls
  .ufo/waves/round-72/controls/c2-controls-r72.json --scratch-root DIR` printed as its
  last line `MADO_R72_OUTCOME: cases=8 correct=8 base_correct=4 verdict=TARGET_MET
  rev=9bcb4fd5b598844f168230dc05e441721d95b272`, rc 0. Frozen predicate: the contract
  verdict is `TARGET_MET` iff the kill count is `2/2` **and** the extracted instrument's
  **last** parsed `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed` summary
  has `n > 0` and `p == n`; a missing or garbled summary earns no green, and the exit
  status is recorded but does not gate the outcome. The held round-71
  `outcome_verdict(gate_rc, killed)` scores the same eight cases 4/8: wrong on exactly
  `failing-summary-exit0`, `green-summary-exit2`, `no-summary-exit0` and
  `garbled-summary-exit0` — receipt § each case; the do-nothing control scored exactly
  4/8. `<L1 fills: reviewer deltas named after the wave settles, if any>`

**Not claimed.** A captured summary replayed with its own matching detail lines remains
byte-indistinguishable from a genuine run — the rules read the child's report, they do
not authenticate it; the eight modes and eight cases are finite control sets, not fault
coverage; the fixture lane is the counter's own instrument, not the lane's real landing
instrument; C2's counter scores the committed functions, not the whole harness execution;
a case where the summary and the exit status contradict is scored by the summary by
design — the exit status cannot carry the assertion result (held ground S441/S435, now
S445); runtime behaviour of the extracted instruments beyond the frozen functions;
desktop, compositor, session, service or package state (none probed); any `[x]`,
promotion or axis retirement. No-harm obligations: `bash tools/mado-verify.sh --selftest`
stays 460/460; the frozen round-71 instruments stay byte-identical; the index, ledger,
axis table and navigation checks stay at their measured values; both counters enter
`quality/tool-ledger.md` and the `SKILL.md` Gate registry in this round
(`quality/check-tool-ledger.py` `uncovered=0`). `<L1 fills: this round's harm-watch
receipt lines>`

## Gate

Admitted, **S444** — CPython v3.14.8 `Doc/library/unittest.rst`, § `TestResult`
(`wasSuccessful()`).

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/unittest.rst`
- Access date: 2026-11-04, fetched three times, byte-identical (sha256
  `d6522f68c29c8ced8d2d81c91cb41ac739f855e6c0b9831f4a0e5a81f7ae5b86`, 107,372 bytes —
  seat-verified over `.ufo/waves/round-72/fetch/Doc_library_unittest.rst.1-3`; the fetch
  receipts' landing commit `<L1 fills>`).
- Located quote, 13 words, unittest.rst:2129-2130: "Return ``True`` if all tests run so
  far have passed, otherwise returns ``False``."
- Why it grounds the claim: the pass/fail fact is a read on the result object
  (`wasSuccessful()`), not a property of the process status — the round-72 C2 verdict
  rule (summary-first, exit recorded) is this fact operationalised on the lane's own
  instrument boundary. CORPUS rule 2 mechanics: new row; no URL shared with a held row,
  so no census W04 warning is expected (`<L1 fills: census line at adoption>`). used-by:
  `corpus/knowledge/outcome-verdict-gate-summary-r72.md`.

Admitted, **S445** — CPython v3.14.8 `Lib/unittest/main.py` (the runner's exit
derivation).

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/unittest/main.py`
- Access date: 2026-11-04, fetched three times, byte-identical (sha256
  `12de7da0fea92dbff8713ebe9904ada6dbd1e0a334d58861c6287ccfc0a261d2`, 11,660 bytes —
  seat-verified over `.ufo/waves/round-72/fetch/Lib_unittest_main.py.1-3`; the fetch
  receipts' landing commit `<L1 fills>`).
- Located quote, 4 words, main.py:273-274: "if not self.result.wasSuccessful():
  sys.exit(1)".
- Why it grounds the claim: the official runner derives its one exit bit from
  `result.wasSuccessful()` — a child's exit status is a projection of the result object
  and cannot be read back as the assertion record. Both round-72 rules rest here: C1
  reads the failure count from the summary, C2 records the exit without gating on it.
  CORPUS rule 2 mechanics: new row; used-by
  `corpus/knowledge/outcome-verdict-gate-summary-r72.md`.

Rejected: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/stdtypes.rst`
(the round-71 reject's real 3.14 path) curated as **S446**, a `rejected` row.

- URL / access date: fetched three times 2026-11-04, byte-identical (sha256
  `5a6951b72ecc630a87f45a650fc11c186cfeb4251bedd1ea28f45bcb3116e8e1`, 248,201 bytes —
  seat-verified over `.ufo/waves/round-72/fetch/Doc_builtins_stdtypes.rst.1-3`); the
  round-71 citation `Doc/library/stdtypes.rst` returns HTTP 404 at the pinned tag,
  re-attempted three times this round (`<L1 fills: committed paths of the 404 receipts>`).
- Located quote, 8 whitespace tokens, stdtypes.rst:5523,5529 under `Mapping Types ---
  dict` (:5299): "`.. method:: setdefault(key, default=None, /)`" and
  "`.. method:: update(**kwargs)`".
- Why it is curated, not admitted: the page documents mapping-method behaviour (argument
  forms and defaults), not the call-site or result-object semantics the round-71/72
  rules rest on. The row keeps the round-71 verifier's routed taste in the registry:
  `teaches` opens `REJECTED: documents method behaviour (argument forms and defaults),
  not call-site or result-object semantics, and no admitted entry needs it; flip: a
  claim whose subject is mapping-method behaviour re-opens it`. status `rejected`,
  recheck `180d`, used-by `—`.

## Mistakes

| mistake | class | evidence | captured-by | fix and the failure it can now show |
|---|---|---|---|---|
| M72-1: the round-71 Gate rejected the stdtypes mapping-methods page only as lesson prose — no `rejected` SOURCES.md row existed (routed defect 1, curation half). | rejection curation (record-keeping) | `corpus/lessons/round-71-verifier-spotcheck.md` § Discernment spot-check, "Reject curation" row (`grep -n stdtypes corpus/SOURCES.md` → 0 rows at r71), committed `976684a2`; this round curates S446 (SOURCES.md working tree :396 at this seat's read; landing commit `<L1 fills>`) | the r71 outside verifier; `none` in-lane at r71 — no criterion required curating a rejection as a registry row | S446 admitted as a `rejected` row whose `teaches` opens `REJECTED: …; flip: …`. The failure it can now show: a rejection living only in prose — `grep -c 'REJECTED:' corpus/SOURCES.md` now counts it. |
| M72-2 (the misroot the L1 names; known instance): the r71 lesson's reject cites `…/v3.14.8/Doc/library/stdtypes.rst`, which 404s at the pinned tag; 3.14's docs reorganisation moved the file to `Doc/builtins/stdtypes.rst`. | citation misroot (URL/path) | `corpus/lessons/round-71-verifier-spotcheck.md` § Per-claim re-check (404 at the tag; real path 200, 248,201 B), committed `976684a2`; this round re-opened the real path three times byte-identical (`5a6951b7…`) and re-attempted the misrooted URL three times (`w1/R72ScoutSources/fetch/bad.1-3`: `404: Not Found`; `<L1 fills: committed receipt paths>`) | the r71 outside verifier (routed defect 1, citation half); `none` in-lane at r71 | S446 anchored at the real path with the 404 recorded in its anchor cell. The failure it can now show: a row whose anchor URL does not resolve at its pinned tag (a re-fetch 404s). `<L1 fills: any further misroot the L1 names>` |
| M72-3: the r71 report calls S442's located quote A "11 words"; it is 10. | report arithmetic | `corpus/lessons/round-71-verifier-spotcheck.md` routed defect 6 and its row count ("S442 10 words, S443 25 words"), committed `976684a2` | the r71 outside verifier | `<L1 fills>` — corrected in this round's errata (the r71 report is append-only); the count is re-derivable from S442's committed quote. |
| M72-4: `.ufo/waves/round-71/w1-results.json` entries carry `name`/`agent`/`output`/`note` and no per-seat `status`, so "13/13 settled `status: ok`" rested on the orchestrator's WAVE-DONE message, not a committed artifact (routed defect 5; M71-4 lineage). | wave evidence capture | `corpus/lessons/round-71-verifier-spotcheck.md` § conformance defects item 5, committed `976684a2`; QUALITY criterion 115(b) names the binding per-seat check | the r71 outside verifier; in-lane, criterion 115 (the r71 landing's own rule) already names what it violates | `<L1 fills>` — this round's wave settlement records per-seat status/observations in the round report. The failure it can now show: a results file whose `status` field reflects settlement, not deliverables. |

A fix counts only on its named evidence: `<L1 fills — the red/green or commit pair per
row, per the round-71 lesson's closing rule>`.
