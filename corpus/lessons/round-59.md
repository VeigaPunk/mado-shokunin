# Round 59 — mado lesson (hyaku run 12)

Base `6f2e4115dc1ebeb87c4d1aba9803c04c82dc4c80` (the r58 verifier spot-check).
Host: Windows 11 Home, build 26200, as in rounds 57-58. Three claims: **C1
calibration** (the r58 non-author closure's carry-in corrections — the stale
`93e43f8f…` gate identity in the r58 lesson corrected append-only with the
measured current blob; the provenance trios the r57/r58 entries lacked added
as pure insertions), **C2 operability** (the carry-in's case-variation
residual in the checker prefix rule hardened: the shared-scratch refusal folds
letter case, because `realpath` cannot case-fold an absent prefix; named pin
assertions; fail-closed behavior preserved both directions), **C3 coverage**
(sourced entry `knowledge/windows-dwm-service-model-r59.md` — row S405 plus
re-used S399/S400 — closing the r57 entry's finding D01 with the named
residue). L1-only round again: the MISSION ≥8-L2 dispatch floor has no
surface on this host (disclosed since r57, L0 open; unchanged). The security
boundary held throughout: no r56-era credential material was opened or
surfaced; the round touched only the files named in the report.

## Gate

### Admitted

- **Rows S405** (tier A, `mined`, opened 2026-10-31 on the Windows host):

  | row | URL | located quote |
  |---|---|---|
  | S405 | `https://learn.microsoft.com/en-us/windows/compatibility/desktop-window-manager-is-always-on` | `In Windows 8, Desktop Window Manager (DWM) is always ON and cannot be disabled by end users and apps.` (§ Description; ms.date 2018-07-11, git_commit 40f2250e0d45a6cdf02bd22408933c9ee4c10d78, updated_at 2021-11-17, Platforms "Clients – Windows 8" carried verbatim) |

  The page was opened in full this round (fetch with the page body returned);
  the quote is a verbatim substring of the opened body. Re-used rows S399 and
  S400 were re-opened this round (K20 re-quotes S400's note from its page).
  One search sweep, bounded to the flip's surface (search log § Round 59);
  no rejected-row event: the one candidate that surfaced was opened and
  included, and the sweep honestly reports that a Win11-labeled model
  sentence did not surface.

- **Entry** `knowledge/windows-dwm-service-model-r59.md`: 4 host rows (H09-H12,
  each with its re-derivation command; probe is a committed receipt artifact,
  two byte-identical runs), 6 documented rows (K15-K20, `[INF-docs]`, dated),
  4 joins (J09-J12; J10/J11 carry the vacuous-shape and point-in-time
  caveats), and § 4 closes D01 as **closed (flip met)** with the residue
  named (no Win11-labeled model sentence in the bounded sweep; the
  build-26200 pin is the host join). The r57 entry gains an
  `## Errata (round 59)` pointer; layers stay separate per QUALITY 15/16.

- **Checker case-fold hardening (C2)**: `quality/check-tool-ledger.py` and
  `quality/check-wave-done.py` fold letter case in the shared-scratch prefix
  compare (`os.path.normcase`, identity on POSIX) — before this round a
  case-variant spelling of an ABSENT shared-scratch prefix (`C:/DEV/shm/…`
  for `/dev/shm`) matched nothing after `realpath` resolution and was
  accepted, the exact residual the r58 closure named (its `C:/TMP` spelling
  is real as a code defect but is masked on this host today: `C:\tmp` exists
  with third-party content, and `realpath` true-cases an existing prefix on
  both sides — measured, receipt `casefold-before.txt`, per-prefix table).
  Red-before at base bytes: both checkers ACCEPTED the `C:/DEV/shm` variant
  (rc=1, bypasses=2). After: refused in every mode and through the CLI
  (rc=2 ×4 receipt), both selftests green at the new pins 55/55 and 63/63
  (`SELFTEST_CHECKS` now host-derived: +1 on Windows only), the named
  assertion `refuse-work-casefold` present in both suites, fail-closed
  behavior preserved (default `--work` under home still refuses, rc=2;
  `--work C:/tmp/…` still refuses), production mode still `TARGET_MET`
  (population 99/99). Host left clean (the probe removes every directory it
  created; `C:/DEV` verified absent after).

- **Record corrections (C1)**: the r58 lesson's stale gate identity corrected
  append-only (`## Corrections (round 59)`: the frozen-instrument pin
  `93e43f8f…` is the round-9-11 arc freeze at 3,231 L; the gate this round
  declines to rewrite is blob `9113c7c05e586328f44ed6822a3d12ff34c47a36`,
  sha256 `050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1`,
  4,194 L, byte-unchanged since round 19 / `7b4839d3`; receipt
  `.ufo/waves/round-59/receipts/gate-identity-r59.txt`). The r57 and r58
  entries gained the provenance trio the corpus contract requires (CORPUS.md:
  `source:`, `verified-at:`, `recheck:` first) — pure insertions above the
  title, zero existing lines modified (diff shape +4/−0 each, checked at
  commit time in the report).

- **Record changes**: SKILL.md § Round 59 (three rules + ground);
  `corpus/README.md` (index row + frontier bullet); `corpus/SOURCES.md`
  (row S405; used-by cells of S399/S400 extended with the r59 entry and
  lesson — the exact consistency move the used-by contract wants; search-log
  § Round 59); the r57 entry errata append; the two trios; the r58 lesson
  corrections block.

### Rejected (reasons stay; flip conditions named)

- **Rewriting `tools/mado-verify.sh`** (still, and again): its selftest
  remains non-runnable on this host (r58 receipt stands); the gate bytes are
  untouched this round — blob identity re-measured in the C1 receipt, and
  byte-equality at base was checked before work started (`git show HEAD:` |
  `sha256sum` = working bytes for both checkers too). **Flip:** unchanged
  from r58 (an operator ruling creates a new tool, not an edit).
- **Extending the DWM probe to mutate anything** (starting/stopping a
  service, `DwmEnableComposition` calls): the lane's Windows boundary is
  read-only observation; mutating verbs stay operator-owned (SKILL § Round 57
  rule 4). The probe answers the service model with four read-only queries.
  **Flip:** an operator ruling that a throwaway mutation probe of
  composition state is in scope.
- **Declaring D01 closed on the host probes alone** (without a sourced model
  row): D01's flip demands a sourced row; host facts alone would re-class
  the finding, not close it. S405 was required, and the residue (no
  Win11-labeled sentence) is carried rather than smoothed over. **Flip:**
  none needed — this is the record-honesty bar working.

### Outside spot-check (pending; not obtainable this round)

No non-author reviewer was reachable (no dispatch surface; L1-only round),
so every verdict in the round report is the author's. Ready for an outside
spot-check: (a) the S405 quote against the named page (ms.date/git_commit in
the row; Platforms metadata carried verbatim); (b) the probe receipts against
the committed script (re-run command in the entry § 5); (c) the checker
red/green pair (run `python .ufo/waves/round-59/receipts/casefold-probe.py`
against the base revision and the landing revision — rc 1 then 0), both
selftests (55/55, 63/63), and the CLI refusals receipt; (d) the C1 receipts
(`gate-identity-r59.txt`; the trio insertions against `git diff --stat`);
(e) the D01 closure reasoning in the entry § 4 against S399/S400/S405.

## Mistakes

- **M59-1 — the first probe draft equated "rc=1" with "bypass demonstrated",
  and a crashed run earned the same code.** Class `measurement` (caught
  before any receipt was committed). Evidence: the first `casefold-probe.py`
  draft computed its repo root one directory short and died on
  `FileNotFoundError` at import time — exit code 1, indistinguishable from
  the bypass verdict it was designed to report; the transcript that first
  landed in `casefold-before.txt` was a traceback, not a measurement, and it
  was overwritten by the corrected run. Captured-by: reading the run's own
  output against the printed code (the M58-4 lesson re-arming one level up:
  owning `$?` is not enough — the exit-code vocabulary itself must be
  crash-safe). Fix: the probe returns 1 only when `bypasses > 0`; any crash
  propagates as an exception (traceback + non-1 rc); the committed receipt
  carries the probe's self-describing verdict line
  (`CASEFOLD_PROBE: BYPASS/NO-BYPASS (bypasses=n)`) next to the rc, so
  neither can be read alone.
- **M59-2 — the host's own state masks the residual the carry-in named, and
  the first probe design would have missed that.** Class `stale-premise`.
  Evidence: the carry-in spelled the residual as "C:/TMP case-variation", but
  on this host `C:\tmp` exists (with third-party content — `kake-r16`,
  `openclaw`, `pi-github-repos`; not the lane's, left untouched), and
  `realpath` true-cases an EXISTING prefix on both sides, so the `C:/TMP/…`
  candidate was already refused at base bytes (`casefold-before.txt` prints
  the per-prefix table: /tmp and /var/tmp REFUSED at base, only the absent
  `/dev/shm` prefix ACCEPTED). The first design also cleaned up only the
  mkdtemp and candidate directory, which would have left created ancestors
  (`C:\VAR\tmp`) on the host. Captured-by: probing all three refused
  prefixes with per-prefix pre-existence recorded instead of assuming the
  named spelling demonstrates the defect. Fix: the probe (and the pin
  assertion in both selftests) selects the first ABSENT prefix, records
  pre-existence for every directory it might create, and removes exactly
  those; the masking itself is recorded in the entry and the receipts as a
  named host fact.
- **M59-3 — `git status` noise nearly misread as working-tree drift.** Class
  `host-assumption` (the known host defect, recorded since r57). Evidence:
  `git status --porcelain` on the two checkers printed `MM` although
  `git show HEAD:<path> | sha256sum` equals the working-tree sha256 for both
  (byte-identical to the tip). Captured-by: the round prompt's standing rule
  (never `git status` on this host) plus the byte-compare cross-check. Fix:
  tree state on this host is only ever asserted by comparing bytes against
  `git show <rev>:<path>`; the status output is ignored as garbage.
- **M59-4 — round 58's errata append inside the r57 entry named rows S402-S404
  without extending their used-by cells; the standing counter reads those
  tokens as citations and reported missing=2 at the r58 tip.** Class
  `landing` (a consistency cell missed at the r58 landing; caught this round
  by the frozen r56 instrument working as designed). Evidence:
  `python -I quality/counters/c3-r56-used-by.py --repo . --rev 6f2e4115…`
  → `entries=73 rows=341 missing=2 … verdict=TARGET_MISSED`, detail naming
  `S402` and `S404` × `corpus/knowledge/windows-desktop-plane-r57.md`
  (receipt `usedby-before-r59.txt`); the source of the phantom citations is
  the r57 entry's `## Errata (round 58)` block ("rows S402-S404; finding D02
  there"). Captured-by: the round-59 harm watch running the counter at base
  before touching anything. Fix: the two used-by cells extended with
  `corpus/knowledge/windows-desktop-plane-r57.md` this round — counter at
  the landing revision: missing=0 (receipt `usedby-after-r59.txt`). The
  general rule: an append that names rows inside an existing entry extends
  those rows' used-by cells in the same landing.

## Census

Start (round start, before any edit; output quoted in the round report — the
run was not tee'd to a file, disclosed): `mado ok`, exit 0, warning set 36
W04 + 1 W01 (identical to r57/r58), 341 rows by the SCORECARD grep. End:
`.ufo/waves/round-59/receipts/census-after.txt` → same warning set, exit 0,
342 rows by the grep (S405; the S399/S400 used-by extensions add no warning —
the W01 class is tier-C used-by, untouched). Used-by counter: base receipt
`usedby-before-r59.txt` (`missing=2 … TARGET_MISSED` — the M59-4 defect),
landing receipt `usedby-after-r59.txt` (`missing=0 … TARGET_MET`). Tool
receipts committed beside them: casefold-probe.py, casefold-before.txt
(rc=1 BYPASS at base bytes), casefold-after.txt (rc=0),
ledger-selftest-after.txt (55/55), wavedone-selftest-after.txt (63/63),
casefold-cli-refusals.txt (4 × rc=2), failclosed-after-r59.txt (home refusal
rc=2), ledger-production-r59.txt (TARGET_MET), gate-identity-r59.txt,
dwm-service-probe.ps1 + dwm-service-run1/run2.txt.

## Considerthese and assimilation

- Mined all nine `considerthese/` files again this round (2026-10-19 through
  2026-10-28; nothing new since the r58 mining): no adoptable proposal. The
  dispositions of r57/r58 stand (capability-demonstration list absorbed by
  the fleet-1 table; daily-reproduction proposals need a dispatch/permission
  surface this host does not offer; the metrics-trend-line proposal is an
  aggregator surface; the rest dispositioned in r57).
- Assimilation: none — shokuknow unreachable.

## Route to round 60 (intent only; no commitment)

1. The two L0 rubric rulings (omarchy freshness disposal; gate-selftest host
   gap) remain the operator's; whichever way they land, the SCORECARD tables
   follow, not before.
2. The rendered-pixel observation (both plane entries' limits) stays the
   largest open Windows-plane ground — needs the right read-only surface
   (candidate: DXGI/Magnification read-only capture APIs, if the operator
   rules screen capture read-only in scope).
3. A Win11-labeled DWM model sentence, if one surfaces, strengthens the D01
   closure pin (the residue is named in the r59 entry).
