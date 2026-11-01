author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

# Round 58 — mado verifier spot-check (closure, non-author)

Round: mado lane-round 58, 2026-10-31, hyaku run 12. Base
`5e483f0d1fcabbbe21cb9ade04a93c24e8224b35` → landing
`92c4b741f717f59db678f2f052c3901b28eaaf85` (branch tip, pushed). This file is
written by the closure judge, who did not author the round. Index-free git
only (`rev-parse`, `cat-file`, `ls-tree`, `diff-tree`, `merge-base
--is-ancestor`, `show`, `log`, `ls-remote`); sibling gates were NOT executed —
their committed evidence was verified per the gate standard. Security boundary
held: no r56-era credential material was opened or surfaced (counts and shapes
only).

## 1. Step-1 conformance — all checks pass

| check | command (abbreviated) | observed |
|---|---|---|
| report committed by lane identity | `git -C <fleet> log --format='%an %ae %H' -1 -- .ufo/reports/round-58/mado.md` | `mado-shokunin mado@shokunin.local 7076f18544448bebb6a3c1cb5420025ed712789c` |
| SHONEN heading + box lines | `git show 7076f185:…mado.md \| grep -c '^\- \[~\]'` | heading `## SHONEN` at line 148, 4 `[~]` lines (one per box; no `[x]` written by the lane) |
| cited hashes exist + are ancestors | `cat-file -t` + `merge-base --is-ancestor <hash> refs/heads/master` | `92c4b741f717…` and `5e483f0d1fca…` both commits, both ancestors |
| other hash citations in report | report's hash-like strings | only the three above plus blob `9113c7c05e58` (verified: `tools/mado-verify.sh` blob identical base↔landing) |
| branch tip pushed | `rev-parse refs/heads/master` vs `ls-remote origin refs/heads/master` | both `92c4b741f717f59db678f2f052c3901b28eaaf85` |
| round work reachable | `diff-tree -r --stat 5e483f0d 92c4b741` | 27 files, +914/−37 — exactly the report's claim; one lane commit `92c4b741` authored `mado-shokunin <mado@shokunin.local>` |
| dispatch/complete digest | `grep 'mado round=58' .ufo/watchdog.log` | `20:10:47 launch … base=5e483f0d1fca (zcode run14)`; `21:11:44 complete … head=92c4b741f717 pushed=True` — matches the closure digest |
| marker rule | report content | real work, evidence pointers, LOG ties, resolvable commit — a real report, not a marker |
| L0 line (r58) | `grep 'mado \| round-58' .ufo/l0-questions.md` | present (line 237, `<lane> \| round-58 \| …` shape, routed-around-not-answered); in the fleet working tree for the orchestrator to commit, as the report states |

## 2. Claims — re-derivation

Re-measured = the closure ran its own counting command over committed bytes;
evidence-verified = the lane's committed receipts and code were verified, per
the gate standard, without executing the sibling's gate.

### C1 operability — improved (evidence-verified)

- Code read at the landing (`git show 92c4b741:quality/check-tool-ledger.py`,
  same policy in `quality/check-wave-done.py`): `resolve_work(explicit,
  declared_tree)` refuses the shared-scratch prefixes FIRST, in every mode,
  comparing both the literal prefix and `os.path.realpath(bad)`; the
  `--scratch-root` waiver then skips ONLY the home refusal, and only for a
  candidate inside the declared tree; `--work` + `--scratch-root` is an
  argparse usage error in both checkers; pinned counts `SELFTEST_CHECKS` 50 →
  54 and 58 → 62 with 4 new assertions each (declared-root-accepts-home +
  3 declared-root-refuse-<prefix>).
- **The C:/tmp prefix-bypass closure verifies.** Base logic compared only the
  literal `/tmp` prefix, which a drive-letter candidate can never match on
  Windows. The fix resolves the prefix. Verifier's own platform measurement
  (not gate execution): `python -I -c "import os;
  r=os.path.realpath('/tmp'); c=os.path.realpath('C:/tmp/some/scratch');
  print(repr(r), repr(c), r==c or c.startswith(r+os.sep))"` →
  `'C:\\tmp' 'C:\\tmp\\some\\scratch' True`. Red receipt committed:
  `failclosed-after.txt` shows `--work C:/tmp/mado-r58-probe` → rc=2
  `refusing work dir under /tmp (got C:\tmp\mado-r58-probe)`, plus default
  `--work` under home refusing rc=2 for both checkers, the mutual-exclusion
  usage error rc=2, and production `LEDGER: population=99 ledger_rows=99 …
  verdict=TARGET_MET` rc=0.
- Red-before receipts committed (`ledger-selftest-before-refusal.txt`,
  `wavedone-selftest-before-refusal.txt`): base bytes refuse the home
  scratch with rc=2 — consistent with base code (home check, no USERPROFILE
  fallback, no prefix resolution). Green receipts: `LEDGER_SELFTEST: 54/54
  passed`, `MADO_WAVE_DONE_SELFTEST: 62/62 passed`.
- Residual hardening (routed, see § 5): on Windows `os.path.realpath` does
  not case-fold a NON-EXISTENT path, so `--work C:/TMP/…` (uppercase, absent)
  still slips past the resolved-prefix compare; likewise a candidate on a
  different drive than the process cwd. The claimed closure (the literal
  `C:/tmp` case) is real and receipted.

### C2 coverage — improved (re-measured + sources re-opened)

Verifier's own counts over committed bytes:

| command (at base `5e483f0d` / landing `92c4b741`) | base | landing |
|---|---|---|
| `git ls-tree -r --name-only <rev> corpus/knowledge \| grep -c '\.md$'` | 72 | 73 |
| `git show <rev>:corpus/README.md \| grep -cE '^\| ` + '`knowledge/[^`]+\.md`' | 72 | 73 |
| `git show <rev>:corpus/SOURCES.md \| grep -cE '^[[:space:]]*\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | 338 | 341 |
| `git show 92c4b741:corpus/knowledge/windows-permonitor-dpi-r58.md \| grep -cE '^\| [HJK][0-9]{2} '` | — | 14 (3 H + 7 K + 4 J) |

Matches the report exactly. SOURCES diff is append-only: new rows S402-S404
inside `## Registry`, plus a new search-log paragraph (question, where,
date, 3 identified / 3 screened / 3 included / 0 excluded, stop rationale).

Sources re-opened by the closure (WebFetch, 2026-11-01):

- **S402** `…/ne-shellscalingapi-monitor_dpi_type`: quote "This value is the
  linear DPI of the screen as measured on the screen itself." present VERBATIM
  in § Constants under `MDT_RAW_DPI`; enum `MDT_EFFECTIVE_DPI = 0,
  MDT_ANGULAR_DPI = 1, MDT_RAW_DPI = 2` confirmed; ms.date 2018-12-05,
  git_commit `92672624…` — matches the row's anchor cells.
- **S403** `…/previous-versions/dn302058(v=vs.85)`: quote "Queries the
  specified monitor for the dots per inch (dpi) horizontal and vertical
  values." present VERBATIM as the page's description line; `is_archived:
  true` (status correctly carried in the row); ms.date 2014-01-13, git_commit
  `f20b8056…`; the page's own dpiType table maps 0/1/2 identically.
- **S404** `…/nf-winuser-getdpiforwindow`: quote "Returns the dots per inch
  (dpi) value for the specified window." present VERBATIM; ms.date 2022-05-25,
  git_commit `fa536415…`; the Remarks table grounds J07's awareness-branch
  ambiguity (UNAWARE → 96, SYSTEM_AWARE → system DPI, PER_MONITOR_AWARE →
  monitor DPI).

All three quotes are ≤25 words, located, and match their `teaches` claims.

### C3 calibration — improved (re-measured greps + static assertion read)

- `grep -c 'MADO_WINDESK: ERROR'` over all 10 committed
  `.ufo/waves/round-57/receipts/` files at the landing → 0 matches in every
  file (negative claim carries its sweep). The same grep over
  `.ufo/waves/round-58/receipts/windesk-error-path.txt` → 1. The r57 base
  receipt `round-57/receipts/selftest.txt` records `9/9`; the r58 receipt
  `windesk-selftest-10.txt` records `10/10`.
- Static read of the landing tool (`VERSION = "r58-v1"`): the 10th test
  `test_malformed_snapshot_is_error_and_bytes_never_echoed` writes a malformed
  snapshot, runs `--from-file`, and asserts `rc == 2`, output starts with
  `MADO_WINDESK: ERROR (stage=parse`, and the payload markers are never
  echoed. The committed ERROR receipt carries the bounded single-line ERROR
  output with a truncated path — no raw payload bytes echoed. Live
  re-verified CLEAN (`windesk-live-r58.txt`).
- Minor note: the standalone ERROR receipt does not print a literal `rc=2`
  token; rc=2 is pinned by the tally's 10th assertion (committed) — accepted.

## 3. No axis harmed

`git diff-tree -r -p 5e483f0d 92c4b741 -- SCORECARD.md` is append-only: one
new Round 58 section (no scored value changed; claims declared before the
receipt runs; measured before→afters), one new capabilities row
(`--scratch-root`). The r57 knowledge entry gained an append-only
`## Errata (round 58)` block — no entry body rewritten; PROVINCE.md and
SHONEN.md untouched (absent from the diff). The gate-selftest failure is a
measured host fact (`gate-selftest-windows.txt`: POSIX symlink creation
denied), disclosed and routed to L0, gate bytes untouched. The README index
r57 row still reads "selftest 9/9" — reviewed and accepted: it describes the
r57 round state, and the errata block + tool-ledger row (9 → 10) carry the
current count under the lane's errata convention.

## 4. Discernment spot-check table

Sample: 2 admits (the sourced rows + the checker policy) and 2 rejects (gate
rewrite; awareness-mutating probe). Re-opened sources: S402, S403, S404
(all three new rows) + committed receipts for the non-URL items.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| Rows S402-S404 admitted tier A `mined` | admit | the three live Microsoft Learn pages (fetched) | agree | all quotes verbatim and located; ms.date/git_commit match the registry cells; S403's archived status is carried, not hidden; enum mapping 0/1/2 confirmed against both pages (the M58-2 correction is real) |
| Checker `--scratch-root` policy admitted (C1) | admit | checker diffs at the landing + all six committed receipts + verifier's own realpath measurement | agree | waiver is home-refusal-only and tree-scoped; shared-scratch prefixes refused first in every mode; red-before AND fail-closed-after receipts committed; the C:/tmp bypass closure is genuine |
| Observer tally fold admitted (C3) | admit | tool code at landing, r57 selftest receipt (9/9), r58 receipts (10/10, ERROR line) | agree | the routed r57 gap is closed both ways the closure asked for (tally covers the path AND a committed run exists) |
| Modifying `tools/mado-verify.sh` fixtures to pass on Windows | reject | `gate-selftest-windows.txt` + gate blob identity base↔landing | agree | the failure is a measured host fact (symlink denial), not a gate defect; rewriting a frozen instrument to manufacture a pass would violate the red-before discipline; L0 routing is the correct disposal |
| Re-baselining the operability rubric unilaterally | reject | SCORECARD r58 section + L0 line 237 | agree | no r58 claim needed the rubric to move; keeping the omarchy-host value with the receipt attached and routing disposal to the operator is the honest-stop shape |
| Extending the probe to `SetProcessDpiAwareness` | reject | probe receipts + the rejected list's reasoning | agree | the probe would mutate its own process's DPI awareness — outside the lane's read-only/process-operations reading; RAW_DPI already yields real per-monitor ground; J07 keeps the ambiguity named `[UNK]` |

Census validate run by the closure: `bash <fleet>/scripts/sources-census.sh
validate --root <fleet> mado` → exit 0, `mado ok`, 36 W04 + 1 W01 (all
pre-existing, matching the committed census receipts); the fleet-root mirror
the census reads is at the landing commit (`92c4b741`, 341 rows).

## 5. Per-axis verdicts and trends (closure rulings)

| axis | verdict | evidence |
|---|---|---|
| operability | improved | C1 evidence-verified: selftests runnable on this host again (54/54, 62/62 receipts), fail-closed side receipted, capability row entered with a passing demonstration |
| coverage | improved | C2 re-measured 72→73 files / 72→73 index rows / 338→341 registry rows; new entry on uncovered ground citing mined rows opened this round; indexed and reachable |
| calibration | improved | C3 re-measured: routed receipt gap closed both ways; errata keeps the historical 9/9 from being confused with the current 10/10; host gap measured and routed instead of papered over |
| freshness | unchanged | dormant omarchy-host rubric untouched (L0 open); re-verification receipts added (live CLEAN, probe run2) without score movement |
| depth | unchanged | new entry adds sourced detail but no depth claim was declared or scored this round |
| adjacency | unchanged | no contested scope; considertese/ re-mined, nothing adoptable; shokuknow unreachable (disclosed) |

Trends: **expansion improved** (net new admitted entry on uncovered ground,
each claim citing its coverage-map row); **quality improved** (checkers
re-verified green on this host with no admitted entry failing a re-check; no
frozen byte changed); **discernment improved** (the round's gate decisions
AGREE with this outside spot-check on the sampled admits and rejects, and the
one live defect — M58-2 — was caught by the lane's own sourced-row discipline
and mined). All three of the lane's self-graded trend verdicts are confirmed.

## 6. Routed defects for round 59 (status-neutral; none bars admission)

1. **Lesson reference-drift (M58-adjacent).** The Gate § Rejected first item
   calls the gate "the frozen instrument at `93e43f8f…`". That value is the
   FLEET-ROUND-1-era sha256 (recorded in `.ufo/evidence/round-12/gate-shas.txt`
   and `.ufo/continuations/fleet-round-1.json`); the current gate bytes are
   blob `9113c7c05e586328f44ed6822a3d12ff34c47a36`, sha256
   `050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1` at the
   landing (PINS.txt pins the blob identity correctly, as does the report).
   Fix: append a one-line correction in the r59 lesson naming the current pin.
2. **Provenance trio absent from the new knowledge entry.**
   `corpus/knowledge/windows-permonitor-dpi-r58.md` sources via prose (Scope +
   Sources paragraphs and S-row ids) and the README index row carries
   `source:` S402-S404, but the entry does not OPEN with the literal
   `source:` / `verified-at:` / `recheck:` lines the CORPUS trio rule and the
   lane's own r47/r55/r56 entries use; a freshness sweep keyed on
   `recheck:` will not find it. (The r57 entry has the same shape — recurring
   miss.) Fix: r59 appends the trio block to the r58 entry (append-only) and
   backfills r57 the same way.
3. **C:/tmp hardening residual.** The claimed bypass closure is genuine, but
   on Windows `os.path.realpath` does not case-fold a non-existent path, so
   `--work C:/TMP/…` (uppercase, absent) still slips past the resolved-prefix
   compare, as would a candidate on a different drive than the process cwd.
   Fix (optional, next checker-touching round): case-insensitive prefix
   compare on Windows and/or drive-absolute prefix parsing, with a red-before
   receipt per the fix rule.
4. **Note only (no fix owed):** the standalone ERROR receipt carries the
   ERROR line but not a literal `rc=2` token (rc=2 is pinned by the committed
   10th assertion); the README r57 index row's historical "selftest 9/9" stands
   under the errata convention.

## 7. Closure

Step-1 conformance: PASS (no defects). All three claims verify; no axis
harmed; no exploratory claim was declared, so no `unprovable-but-better`
ruling was needed. Lane-round 58 is **admitted** (`ok`). SHONEN boxes remain
`[~]` author-asserted — correctly not self-checked `[x]`; the promotion
review stays open for a non-author verifier (all four boxes are checkable
from committed artifacts when the operator schedules it).
