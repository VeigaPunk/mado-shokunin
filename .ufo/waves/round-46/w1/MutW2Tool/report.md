# MutW2Tool — report (summary)

Round-45 w2 falsification executed: 100 single-site mutants of `tools/mado-monitors.py` @ 4d22eeb66c2835af8aaa3fac6ad838fa616aa663
(sha256 2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609, = current lane file) scored against the frozen
PRED-C1-r45-v2 battery, detector = the counter's own code replayed in-process (`run_fixture` 81 fixtures x 3 variants,
`--selftest`, clause-r marker, `run_generated` 150 @ --nonce 45 for fixture-survivors).

**Result: 68 KILLED, 32 fixture-survivors — 31 of them survive the ENTIRE counter battery (fixtures + generated 150/150 +
selftest + readonly), i.e. the real counter prints `verdict=TARGET_MET` for those mutated tools.** Proven end-to-end with the
real counter on a scratch clone: mutant M01 (`MAX_BYTES = 1048575`) → `PRED-C1-r45-v2: ... verdict=TARGET_MET rev=b2a8acc05b9a375fae87f8b5171f96ba4976e827`.
M39 (rate tolerance `<`→`<=`) → TARGET_MISSED (fixtures 80/81), confirming kill fidelity. Baseline pristine → TARGET_MET (81/81, 150/150).

- 6 survivors are true equivalents (dead/masked code): M02, M03 (read-ahead masks loop bounds), M09 (INT_RE bound immaterial
  for transform 0-7), M15 (match == fullmatch for `monitor[ \t]*=(.*)`), M32 (lower() immaterial), M90 (`new_rule` rate write-only).
- 26 are genuine coverage gaps — untested input classes: size boundary at exactly 1048576 bytes (M01/M04), 5-digit dims (M07),
  6-digit coords (M08), 10-digit stoi/transform values (M10/M11), `monitorv2{`/`monitorv2=` (M12), `monitor=` no-space (M14),
  \v\f-padded line ends (M16), `##`/backslash bodies (M19/M20), addreserved 5th field (M27), `0xH`/`Wx0` modes (M34), float
  width/height (M41), exact 0.0001 scale boundary (M43), half-up k boundary (M45), search steps 88-89 (M46), absent mirror
  target → mutant crashes where pristine DIFFERs (M48), bare `desc` selector (M51), zero dims (M60), bool transform equal to
  rule value (M61), odd-length argv (M78), double `--monitors` (M79), non-UTF-8 config (M82), trailing empty fields (M96).
  M44 survives all fixtures but is killed by the generated battery (146/150).

A surviving mutant is a coverage finding, not a tool defect: the landed tool matches its contract at these sites; the
counter's battery leaves them unobserved. Supports closure D1 (the round-45 w2 never ran; the counter has substantial
survivor surface).

Full table (per-mutant site with computed `grep -n` locators, killing fixture, survivor notes): `MutW2Tool-full.md` in this
directory. Receipts: `mutants.json`, `results.json`, `baseline.json`, `summary.json`, `real/{pristine,M01-survivor,M39-killed}.txt`.

Safety: writes confined to this seat dir + /fast/scratch/hyaku/mado-r46/MutW2Tool (deleted after receipt copy); lane
`tools/mado-monitors.py` re-verified sha256 2f007417… after the campaign; no pacman transaction, no tool installs, no
host-service/compositor mutation, no subagent dispatch.
