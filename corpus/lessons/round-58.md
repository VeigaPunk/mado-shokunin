# Round 58 — mado lesson (hyaku run 12)

Base `5e483f0d1fcabbbe21cb9ade04a93c24e8224b35` (the r57 verifier spot-check).
Host: Windows 11 Home, build 26200, as in round 57. Three claims: **C1
operability** (the M57-1 routed fix — a caller-declared scratch tree for the
two fail-closed checkers, making their selftests runnable and green on this
host with the fail-closed defaults preserved), **C2 coverage** (sourced entry
`knowledge/windows-permonitor-dpi-r58.md`, rows S402-S404, closing the r57
entry's named "per-monitor DPI joins are future ground"), **C3 calibration**
(the r57 closure's routed receipt gap — the malformed-snapshot ERROR sub-claim
now runs inside the observer's selftest tally, 9/9 → 10/10, with a committed
ERROR receipt). L1-only round again: the MISSION ≥8-L2 dispatch floor has no
surface on this host (disclosed in r57 and routed to L0; unchanged). The
security boundary held throughout: no r56-era credential material was opened
or surfaced; this round's git-object work touched only the committed files
named in the report.

## Gate

### Admitted

- **Rows S402-S404**, tier A, `mined`, opened 2026-10-31 on the Windows host.
  URLs, access date 2026-10-31, and located quotes (verbatim, ≤25 words; page
  ms.date / git_commit recorded in the registry cells):

  | row | URL | located quote |
  |---|---|---|
  | S402 | `https://learn.microsoft.com/en-us/windows/win32/api/shellscalingapi/ne-shellscalingapi-monitor_dpi_type` | `This value is the linear DPI of the screen as measured on the screen itself.` (§ Constants, MDT_RAW_DPI; ms.date 2018-12-05, git 92672624) |
  | S403 | `https://learn.microsoft.com/en-us/previous-versions/dn302058(v=vs.85)` (archived previous-versions page; status carried in the row) | `Queries the specified monitor for the dots per inch (dpi) horizontal and vertical values.` (§ Description; ms.date 2014-01-13, git f20b8056) |
  | S404 | `https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getdpiforwindow` | `Returns the dots per inch (dpi) value for the specified window.` (§ Description; ms.date 2022-05-25, git fa536415) |

  Each page was opened in full this round (fetch with the page body returned);
  each quote is a verbatim substring of the opened body. No rejected-row
  event: the sweep was bounded to the three documentation surfaces the
  round's probe rests on (search log § Round 58).

- **Entry** `knowledge/windows-permonitor-dpi-r58.md`: 3 host rows (H06-H08,
  each with its re-derivation command; the probe is a committed receipt
  artifact), 7 documented rows (K08-K14, all `[INF-docs]`, dated), 4
  claim-to-host joins (J05 `agreement*` — effective 96 at 100% scaling is the
  same vacuous shape as the r57 entry's J01, with the caller's
  PROCESS_DPI_AWARENESS `[UNK]`; J07 names the awareness-branch ambiguity),
  and divergence finding D02 (the three documented modes do not collapse:
  effective 96 vs angular 91 vs raw 92 — the per-monitor table is real
  ground, not a copy of the system value; raw/angular must never feed UI
  scale factors). Layers stay separate per QUALITY 15/16.

- **Checker scratch policy (C1)**: `quality/check-tool-ledger.py` and
  `quality/check-wave-done.py` accept `--scratch-root <dir>` — a
  caller-declared scratch tree that waives only the home-directory refusal;
  shared-scratch prefixes stay refused in every mode, and the prefix compare
  now also resolves the prefix (`os.path.realpath(bad)`), closing a Windows
  bypass where `--work C:/tmp/...` slipped past the literal `/tmp` rule at
  base. Selftests pin the policy (4 new assertions each; the pinned counts
  moved 50 → 54 and 58 → 62): both suites green via the flag on this host;
  default `--work` under home still refuses, rc=2.

- **Observer selftest fold (C3)**: `tools/mado-win-desk.py` (`VERSION
  r58-v1`) gains a 10th assertion that runs `--from-file` against a
  malformed snapshot and pins rc=2, the `ERROR (stage=parse …)` line, and
  that the raw payload bytes are never echoed. The r57 closure's routed
  receipt gap is closed by both halves it offered: the tally now covers the
  ERROR path AND a committed ERROR run exists
  (`.ufo/waves/round-58/receipts/windesk-error-path.txt`). Live mode
  re-verified CLEAN after the change.

- **Record changes**: SKILL.md § Round 58 (four rules: the DPI join; the
  checker policy; the gate-selftest host gap measured and routed —
  superseding the r57 sentence "the `--selftest` modes of the pure-Python
  record instruments run unchanged" insofar as it covered the bash gate and
  the two checkers; the observer fold); `corpus/README.md` (index row +
  frontier bullet); `quality/tool-ledger.md` (the observer row's assertion
  count 9 → 10, version noted); the r57 entry gains an `## Errata (round 58)`
  block (tally history vs current count; the § 6 per-monitor limit closed).

### Rejected (reasons stay; flip conditions named)

- **Modifying `tools/mado-verify.sh` to make its selftest runnable on
  Windows** (rewriting the POSIX symlink fixtures, or pointing EXPECT at
  invented substitutes): the gate is the frozen instrument at
  `93e43f8f…`; its selftest failure here is a host fact, not a gate
  defect, and rewriting a frozen instrument to manufacture a pass is the
  exact move r57 rejected. The failure is measured, disclosed in SKILL, and
  routed to L0. **Flip:** an operator ruling that a Windows-side gate or
  fixture layer should exist creates a new tool, not an edit to this one.
- **Re-baselining the operability sub-axis "existing hermetic suite pass
  fraction" (10.0000) unilaterally**: unlike the r57 freshness case (where
  the re-baseline was the claimed freshness move itself), no r58 claim
  needed that rubric to move; the score stands as the omarchy-host value
  with this round's receipt attached, and disposal goes to L0. **Flip:**
  the operator rules the rubric closed or Windows-scoped.
- **Extending the probe to `SetProcessDpiAwareness` to read the
  awareness-true effective DPI**: the r57 rejected list drew the line at
  registry-only inference; a call that mutates the calling process's own
  DPI awareness crosses the lane's "process operations stay operator-owned"
  reading, and the RAW_DPI mode already yields a real per-monitor value
  without it. The caller-awareness question stays `[UNK]` in J05, named.
  **Flip:** an operator ruling that a process-local awareness set inside a
  throwaway probe child is in scope.

### Outside spot-check (pending; not obtainable this round)

No non-author reviewer was reachable (no dispatch surface; L1-only round),
so every verdict in the round report is the author's. Ready for an outside
spot-check: (a) the S402-S404 quotes against the named pages (ms.date/
git_commit in the registry cells; S403's archived status); (b) the probe
receipts against the committed script (re-run command in the entry § 5);
(c) the checker selftests both ways (refusal at base bytes, green via
`--scratch-root`, fail-closed preserved — receipts committed); (d) the
observer tally fold (run `python tools/mado-win-desk.py --selftest` → 10/10;
`--from-file` on any non-JSON file → ERROR rc=2); (e) the gate host-gap
receipt (`bash tools/mado-verify.sh --selftest` → 360/100 rc=2).

## Registry changes old→new

- Rows `338 → 341` (`grep -cE '^[[:space:]]*\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`):
  new ids S402-S404, inserted inside `## Registry` immediately after S401. No
  existing row touched; no `status`/`recheck` change on existing rows. Each
  new row's `used-by` names the entry and this lesson.
- Knowledge files `72 → 73`; README index rows `72 → 73` (counting commands
  in the SCORECARD table); census exit 0 both ends.

## Mistakes

- **M58-1 — the omarchy gate's `--selftest` does not run on this host, and
  the r57 SKILL sentence covering it was wrong.** Class `host-assumption`.
  Evidence: `bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: FAILED —
  360 passed, 100 failed`, rc=2 (`ln: failed to create symbolic link …
  Permission denied`, `rm: cannot remove … Is a directory`, stub binaries
  failing to load); receipt `.ufo/waves/round-58/receipts/gate-selftest-windows.txt`.
  Captured-by: this round's harm-watch probe of the operability rubric's
  command before writing the SCORECARD axis posture. Fix: none in the gate
  (byte-frozen by choice — see the round's rejected list); SKILL § Round 58
  corrects the r57 sentence's scope, the failure is disclosed, and disposal
  is routed to L0. The kept fixture dir `/tmp/w5-mado-m52-selftest.DPf2Ro`
  was swept after the run.
- **M58-2 — the DPI probe's first draft ordered `MONITOR_DPI_TYPE` from an
  unopened search snippet (raw=1, angular=2) — backwards.** Class
  `sourcing-discipline` (captured by the discipline working as designed).
  Evidence: the opened pages S402 (§ Syntax) and S403 (its dpiType table)
  both state `MDT_ANGULAR_DPI = 1`, `MDT_RAW_DPI = 2`; the first probe run's
  labels were swapped, so its "raw=91/angular=92" reading was wrong (true:
  angular 91, raw 92). Captured-by: the sourced-claim order — pages opened
  and quoted before any entry row was written. Fix: probe corrected and
  re-run (receipts `dpi-probe-run1.txt`/`run2.txt` carry the corrected
  labels); lesson: a search snippet is not a source; the quote comes from
  the opened page or the row does not exist.
- **M58-3 — the first `--scratch-root` design keyed the home-refusal waiver
  on the candidate source, and the ledger selftest's own P-rule broke.**
  Class `landing` (red before landing, by design). Evidence: first run of
  `check-tool-ledger.py --selftest --scratch-root <scratch>` crashed in the
  P-rule (`resolve_work(None)` → TMPDIR under home → `GateError: refusing
  work dir inside the home directory`) because the waiver did not apply to a
  candidate that came from TMPDIR inside the declared tree. Captured-by: the
  selftest itself. Fix: the parameter became a waiver *scope* (`declared_tree`):
  the declaration waives the home refusal for everything inside the declared
  tree (including TMPDIR-derived candidates there) but never supplies a
  license outside it; the shared-scratch refusal is checked before the
  waiver. Selftest re-run: 54/54.
- **M58-4 — the first failing run's exit code was read from the wrong
  place.** Class `measurement` (a receipt-discipline slip, caught before any
  receipt was committed). Evidence: the first exploratory run piped the
  selftest through `tail` and printed `$?` — which reported `tail`'s rc=0
  for a crashed run; the traceback on screen contradicted the printed RC.
  Captured-by: reading the run's own output against the printed code. Fix:
  every committed receipt runs the command with direct redirection and
  records `$?` immediately (`before-refusal`, `after`, `failclosed-after`
  receipts all do); the lesson generalizes — in a pipeline, `$?` is the last
  command's, and a receipt that quotes an exit code must own the process it
  measured.

## Census

Start: `.ufo/waves/round-58/receipts/census-before.txt` → `mado ok`, exit 0
(338 rows by the SCORECARD grep; the emit is 36 W04 + 1 W01, unchanged from
round 57). End: `.ufo/waves/round-58/receipts/census-after.txt` → same
warning set, exit 0 (341 rows by the grep); the S402-S404 warning check is
the diff of the two emits (empty). Tool receipts committed beside them:
before-refusal ×2, selftest-after ×2, failclosed-after, gate host-gap,
windesk selftest-10/ERROR/live, dpi-probe.ps1 + run1/run2, PINS.txt.

## Considerthese and assimilation

- Mined all nine `considerthese/` files again this round (2026-10-19 through
  2026-10-28): no adoptable proposal. The capability-demonstration list
  proposal (2026-10-19 #1) was already absorbed by the fleet-1 capabilities
  table; the daily-reproduction proposals need a dispatch/permission surface
  this host does not offer; the metrics-trend-line proposal (2026-10-21 #4)
  is an aggregator-surface suggestion; the remainder were dispositioned in
  r57's mining and nothing new landed in the directory since.
- Assimilation: none — shokuknow unreachable.

## Route to round 59 (intent only; no commitment)

1. The D01 flip (a sourced Win11 DWM service-model row) — the oldest open
   Windows-plane finding; needs the right operator-doc surface or a
   service-control read-only probe.
2. Operator rulings decide ground: the two L0 rubric questions (r57
   freshness disposal; r58 gate-selftest host gap). Whichever way they rule,
   the SCORECARD tables follow the ruling, not before.
3. Multi-display or caller-awareness DPI ground is available only if the
   host changes or the operator rules the process-local awareness probe in
   scope (the r58 rejected list names the flip).
