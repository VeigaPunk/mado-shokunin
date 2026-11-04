# R70ScribeEntryC1 — claim C1 knowledge entry

Seat scope: draft `corpus/knowledge/landing-kill-credit-real-children-r70.md` only. No production
path, lane git state, declaration, control JSON or baseline receipt was written or re-scoped.

## Artifact

| path | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-70/w1/R70ScribeEntryC1/draft/corpus/knowledge/landing-kill-credit-real-children-r70.md` | 227 | 14401 | `86afc55536769a08275e2c0b4f76b0d47aae755ad0e000894177c5b43280f612` |

Grammar copied from `corpus/knowledge/gate-guard-dominance-r69.md`: `source:` / `verified-at:` /
`recheck:` header, `# … (MADO-R70-1)`, `## Scope`, sections 1–5, `## Evidence rows`, section 6
`## 6. Recheck and provenance`. `## 4. Limits — what the counter cannot do` is the Limits section.

## Findings (evidence only from committed bytes and receipts)

1. Held rule: `mz_killed = mz_rc != 0` at `quality/counters/c1-r69-landing-controls.py:452`
   (sha256 `9461a059466e723ba0ae88c86dea2fc97eb5f4fdfb15ef6c6646acce69649a73`; byte-identical
   at `5144a6b5` and at measured content `5adba5a9`). The child rc is `r.returncode` at `:448`;
   the spawn is `bash <mutant> --selftest --scratch-root …` at `:445-447`.
2. Pre-freeze receipt: `.ufo/waves/round-70/control-baseline-r70.txt:40-51` credits `mz=pass`
   for genuine, crash and garbage → `base_correct=1/3`; the r69 evidence line itself printed
   `failed_assertions=0 assertions=none killed=yes` on the crash and garbage scenarios.
3. Repaired rule: `summary_shows_failure` at
   `quality/counters/c1-r70-landing-controls.py:315-330` (sha256
   `71a7b6c45b904a734f194be9a8de6cc2eeb5f5ea1922760f908f5637f1d4db58`), decision
   `mz_killed = bool(mz_rc != 0 and summary_shows_failure(mz_out))` at `:478`; five summary
   cases pinned at `:719-727`; `mz-crash` / `mz-allpass` non-kill cases at `:701-717`.
4. Real-children leg: counter `quality/counters/c1-r70-real-children.py` (sha256
   `b3a6f131abf371ecf64273b65a143478c4b23eaa7acf974ec80e5efebf6e6a7b` at `5adba5a9`),
   `build_fixture` at `:213`, `LANE_TEMPLATE` at `:79`, declared limits at `:46-50`. Measured
   receipt `.ufo/waves/round-70/measurement-r70.txt` § C1: candidate `mz=pass/fail/fail`,
   base `mz=pass/pass/pass`, `MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=1
   verdict=TARGET_MET rev=5adba5a9…`, rc=0. The entry cites that receipt; no value invented.
5. The counter's `LANE_TEMPLATE` with the mode token substituted is byte-identical to the frozen
   `.ufo/waves/round-70/proto/fixture-lane.tmpl` (sha256 `9e31681d…`) with `__MODE__`
   substituted — checked by importing the counter and diffing (`identical: True`).
6. Source: CPython `Doc/library/subprocess.rst` @ `v3.14.8`, fetched three times 2026-11-03,
   byte-identical sha256 `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd`,
   61603 bytes, 1622 lines. Located quotes: L138-139 (`returncode` is the child's exit status),
   L141-142 (`-N` is a signal death), L1500-1501 (exit code interpreted as return code),
   L1508 (`127` missing program), L1510 (`-15` signal death), L961-963 (`shell=True` maps
   signals to `128+N`).
7. **Row id conflict (measured).** The URL already has `S108` (`corpus/SOURCES.md:120`, scope:
   the `args` command parameter). A row pinned to S108 cannot pass `quality/check-anchor-cover.py`:
   the check derives the file name from the *last* URL in the row (`Lib/subprocess.py` for S108,
   so `name=subprocess.py`) and S108's anchor has no `subprocess.py:` occurrence. Measured on a
   scratch registry copy: `ANCHOR_COVER: row=P01 sid=S108 line=138 name=subprocess.py
   locators=none eof=unchecked verdict=MISS reason=no-cover`, `rows=1 covered=0 miss=1
   verdict=FAIL`, rc=1. The entry therefore cites `S441` — the lesson seat's third new row, anchor
   `subprocess.rst:136-142,949-963,1500-1510` — and states the W04 duplicate-URL decision in §6.
   With a synthetic S441 row carrying that anchor, the draft scores `rows=6 covered=6 miss=0
   verdict=OK`, rc=0. The lesson seat confirms by message that S441 is its drafted id, its anchor
   cell is exactly `subprocess.rst:136-142,949-963,1500-1510` (line 143 is blank, so 136-142 is
   the correct range), the row is 11 cells, and the row is held in its CONFLICT file pending the
   L1's W04 decision. If the L1 keeps S108 only, the six evidence rows must be dropped and the
   source cited in prose; the entry says so.

## Commands run and exit codes

| command | result |
|---|---|
| `curl -sSfL -o subprocess.{1,2,3}.rst https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst` (in scratch) | rc 0; all three sha256 `05cd782c…`; `wc -c` 61603; `wc -l` 1622 |
| template identity check (python import of `LANE_TEMPLATE`, substitute `@MODE@`/`__MODE__`, diff against the proto file) | `identical: True` |
| `git -C <lane> cat-file -p 5144a6b5:quality/counters/{c1-r69-landing-controls,c1-r70-real-children}.py \| sha256sum` (read-only) | r69 `9461a059…` (equal to HEAD file); real-children `b1785f38…` at `5144a6b5` vs `b3a6f131…` at HEAD, difference is `9508e878`'s one-line `os.makedirs(scratch, exist_ok=True)` in `run_harness`, outside `EXPECT`/fixture/scoring |
| `python3 -I quality/check-anchor-cover.py --repo <scratch> --rev HEAD --entry corpus/knowledge/probe.md` with a synthetic S108-pinned probe | rc 1; `name=subprocess.py locators=none verdict=MISS reason=no-cover`; `rows=1 covered=0 miss=1 verdict=FAIL` |
| same check, scratch registry copy + synthetic 11-cell S441 row (anchor `subprocess.rst:136-142,949-963,1500-1510`) + this draft | rc 0; all six rows `verdict=OK`; `CHECK107: rows=6 covered=6 miss=0 verdict=OK` |
| `wc -l -c` + `sha256sum` on the draft | 227 lines, 14401 bytes, `86afc555…` |
| `test -e /fast/scratch/hyaku/mado-r70/R70ScribeEntryC1` | `ABSENT` (scratch removed) |

All fixture git repos were created only under the scratch dir, `git init` toplevel asserted equal
to the fixture dir, commits made with explicit `-c user.name/-c user.email/-c commit.gpgsign=false`,
and every git call `-C`-named. No tool installs or upgrades were needed. No desktop, compositor,
service, socket or package manager was touched. No credentials in any artifact.

## Out of scope / not claimed

- No production write, no lane commit/stage/reset/checkout, no fleet-repo write, no sibling-lane
  write. The only git objects created anywhere were inside
  `/fast/scratch/hyaku/mado-r70/R70ScribeEntryC1/` and were deleted with it.
- No measurement was rerun: the entry cites `.ufo/waves/round-70/measurement-r70.txt` and
  `control-baseline-r70.txt` as found. `base_correct=1` and `correct=3` are receipt values, not
  this seat's runs.
- The entry does not claim fault coverage, that three scenarios exhaust the kill-credit hazards,
  that the fixture is the real landing instrument, or anything about desktop/session/package
  state. The "line-count heuristic also scores 3/3" sentence in §4 is marked as derived from the
  frozen template, not measured.
- Row id adoption, the S108-vs-S441 decision and the final `corpus/lessons/round-70.md` Gate
  block remain the L1's.

Report path: `.ufo/waves/round-70/w1/R70ScribeEntryC1.md`.
