# Round 57 — mado lesson (hyaku run 12)

Base `5337d2509f5c91c6f200b6637cf77bd0ad1cd67f`. The lane's live host changed:
this round runs on Windows 11 Home, build 26200 (`HOME=/c/Users/jpvei`,
MINGW64_NT-10.0-26200; Python 3.13.15 as `python`, no `python3`). Three claims:
**C1 freshness** (host-change drift detected and recorded; PROVINCE/SKILL dated
corrections; freshness rubric re-baselined), **C2 operability** (capability
`tools/mado-win-desk.py`), **C3 coverage** (sourced entry
`knowledge/windows-desktop-plane-r57.md`, rows S398-S401). No wave was
dispatched: the MISSION L2 floor (≥8 seats, one batched AgentSwarm call) is
**absent on this host** — no dispatch surface is reachable from this lane
session; the round is L1-only work, disclosed in SCORECARD, the report and an
L0 line. The security boundary from the round contract was in force throughout:
no r56-era credential material was printed, copied, excerpted or surfaced; the
r56 wave receipt that carried it was never opened; the new tool reads no
environment values and no window titles (M56-17's routed criterion, applied).

## Gate

### Admitted

- **Rows S398-S401**, tier A, `mined`, opened 2026-10-31 on the Windows host.
  URLs, access date 2026-10-31, and located quotes (verbatim, ≤25 words; page
  ms.date / git_commit recorded in the registry cells):

  | row | URL | located quote |
  |---|---|---|
  | S398 | `https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows` | `By default, the system considers desktop applications DPI unaware and bitmap-stretches their windows.` (§ DPI Awareness Mode; ms.date 2026-09-10, git 55e845e9) |
  | S399 | `https://learn.microsoft.com/en-us/windows/win32/dwm/dwm-overview` | `Desktop composition is performed by the Desktop Window Manager (DWM).` (intro; ms.date 2018-05-31, git 26465e18) |
  | S400 | `https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/nf-dwmapi-dwmiscompositionenabled` | `As of Windows 8, DWM composition is always enabled.` (§ Parameters Note; ms.date 2018-12-05, git 92672624) |
  | S401 | `https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.screen` | `Represents a display device or multiple display devices on a single system.` (§ Definition; ms.date 2025-07-01, git e2eb860a) |

  Each page was opened in full this round (fetch with the page body returned);
  each quote is a verbatim substring of the opened body. No rejected-row event:
  the sweep was bounded to the four documentation surfaces the round's probes
  and instrument rest on (search log § Round 57).

- **Entry** `knowledge/windows-desktop-plane-r57.md`: 5 host rows (H01-H05,
  each carrying its own re-derivation command and observed value), 7 documented
  rows (K01-K07, all `[INF-docs]`, dated), 4 claim-to-host joins (J01-J04;
  J01 is `agreement*` — at 96 DPI the bitmap-stretch path K02 describes is
  never exercised, so the agreement is vacuous; J02 carries S400's own
  manifest caveat — which compatibility clause applied for the querying
  process is `[UNK]`), and one divergence finding D01 (S399's Vista/7-era
  service sentence against S400's always-enabled note and the observed TRUE).
  Layers stay separate per QUALITY 15/16: no K row is a host fact, no H row
  cites a page.

- **PROVINCE.md round-57 host-change record + surface state register** (8
  groups: 7 absent, 1 observed, each row dated 2026-10-31 with a re-derivation
  probe), the `tools/mado-win-desk.py` tool row, and **SKILL.md § Round 57**
  (omarchy-host claims frozen as host-scoped; the six carried rules). These are
  §6 absent-surface corrections — protocol work, recorded as such.

- **Capability** `tools/mado-win-desk.py` (selftest 9/9; live
  `MADO_WINDESK: CLEAN (screens=1 dpi=96 dwm=on windows=6)`; cross-check 5/5
  stable fields AGREE against independently executed probes; `--from-file`
  re-derivation; malformed input rejected without echoing bytes). Tool ledger
  population 98 → 99 (`LEDGER: population=99 ledger_rows=99 uncovered=0
  dangling=0 … verdict=TARGET_MET` at landing).

### Rejected (reasons stay; flip conditions named)

- **Re-pointing `tools/mado-verify.sh` or any omarchy-era instrument at
  substitute Windows paths**: the gate's value is that its EXPECT list is the
  omarchy plane; pointing it at invented Windows equivalents would corrupt a
  frozen instrument to manufacture a pass. The gate stays byte-untouched; on
  this host it honestly reports the plane absent (`--no-live` → DIVERGED
  17/7/2). **Flip:** an operator ruling that a Windows file-plane instrument
  should exist would create a new tool, not edit this one.
- **Marking the omarchy-host freshness rubric "retired"**: the 9.6552 is the
  last measured value of a real rubric on a real host; retirement would discard
  it. It is recorded **dormant, host-absent**, with the disposal routed to L0.
  **Flip:** the operator rules the rubric closed (then it moves to SCORECARD's
  retired table with that reason).
- **A per-monitor DPI row from registry values alone**: `AppliedDPI` is a
  system-level value; the observed 96 with two agreeing read layers is a
  system-DPI fact, not a per-monitor table. **Flip:** a future round joining
  `GetDpiForMonitor`/`GetDpiForWindow` captures per display.

### Outside spot-check (pending; not obtainable this round)

No non-author reviewer was reachable (no dispatch surface; L1-only round), so
every verdict in the round report is the author's. Ready for an outside
spot-check: (a) the S398-S401 quotes against the named pages (ms.date/git_commit
in the registry cells); (b) the register's absence probes (each row names its
command); (c) the tool's selftest/live/cross-check receipts (commands in the
entry § Verify); (d) D01 (read the two pages' sentences side by side); (e) the
claim that the register covers every declared surface group (count the groups
in PROVINCE's omarchy-era "Owns" paragraph against the register).

## Registry changes old→new

- Rows `334 → 338` (`grep -cE '^[[:space:]]*\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`):
  new ids S398-S401, inserted inside `## Registry` immediately after S397. No
  existing row touched; no `status`/`recheck` change on existing rows. Each new
  row's `used-by` names the entry and this lesson.
- Knowledge files `71 → 72`; README index rows `71 → 72` (both counting
  commands in the SCORECARD table); census exit 0 both ends.

## Mistakes

- **M57-1 — the round-56-era checkers' scratch policy refuses this host's
  canonical scratch.** Class `host-assumption`. Evidence:
  `python quality/check-tool-ledger.py --selftest --work …/scratch/mado-r57/work`
  → `refusing work dir inside the home directory`; its contract also excludes
  `/tmp`, `/var/tmp`, `/dev/shm`, and on this host `$TMP` is the user's temp
  under the home — so every fail-closed scratch refusal fires for the
  contract-mandated scratch path `…/workspace/…/scratch/mado-r57`. Captured-by:
  the checker itself (fails closed, correctly). Fix this round: none needed for
  landing (the ledger check's non-selftest mode reads git objects and writes
  nothing; it ran green). Routed: a host-portable scratch policy (a caller-
  declared scratch root accepted by flag) is a round-58 candidate; until then
  the affected `--selftest` modes are **unrunnable on this host**, which the
  report states rather than papers over.
- **M57-2 — the new tool's first selftest failed on Windows: an open
  `mkstemp` file descriptor locked the fixture against cleanup.** Class
  `host-portability` (POSIX habit). Evidence: first selftest run → 8/9 with
  `PermissionError: [WinError 32] … cannot access the file because it is being
  used by another process` raised from `TemporaryDirectory.__exit__`; the
  descriptor returned by `tempfile.mkstemp` was never closed, and Windows locks
  a file with an open handle where POSIX would unlink it. Captured-by: the
  tool's own selftest (red before landing, by design). Fix: `os.close(fd)`
  immediately after `mkstemp`, plus the read handle closed before asserts; the
  lesson generalizes — on this host, close every descriptor you create before
  any directory cleanup, and expect lane code written for POSIX to need exactly
  this class of pass. Selftest re-run: 9/9, exit 0.
- **M57-3 — the first draft of C1's counting command counted 1 of 8 register
  rows.** Class `landing` (a wrong counting command nearly frozen). Evidence:
  draft `grep -cE '^\| [a-z][a-z /-]*[a-z] \| (absent|observed) \(2026-10-31\)'
  PROVINCE.md` → 1, because the register rows' first cells contain backticks
  and parentheses the character class rejects. Captured-by: the round's own
  pre-freeze verification of its counting commands against the worktree and
  `git show <base>` (the contract's step 4). Fix: the frozen command keys on
  the state cell — `grep -cE '^\| .* \| (absent|observed) \(2026-10-31\) \|'`
  → 8 (worktree) / 0 (base) — and both values were re-derived before the
  SCORECARD text was written. Lesson: a counting command is itself an artifact
  under test; run it red and green before it enters a claim row.
- **M57-4 — a fixed-import slip shipped and was caught by the lane's own run:
  `import os` was dropped from the tool's top-level imports while cleaning up
  the selftest runner, so the fixed `os.close(fd)` raised `NameError` on the
  next selftest run (8/9 again, with the temp dir orphaned).** Class
  `landing`. Evidence: second selftest run traceback (`NameError: name 'os' is
  not defined` at the `os.close(fd)` line), then a stray `tmp…` fixture dir in
  `$TMP` from the aborted cleanup. Captured-by: the selftest (third run) and
  the explicit leftover sweep that found and removed the orphaned dir. Fix:
  `import os` restored to the module imports; selftest 9/9; leftover sweep
  clean. Lesson: each fix run must end in a full green run **and** a
  side-effect sweep — a fix that fails partway can leave host state behind.

## Census

Start: `.ufo/waves/round-57/receipts/census-before.txt` → `mado ok`, exit 0
(334 rows by the SCORECARD grep; the validate emit lists warnings plus the ok
line only, so the before/after emits are byte-identical — 36 W04 + 1 W01,
unchanged from round 56 — and the row totals come from the grep commands).
End: `.ufo/waves/round-57/receipts/census-after.txt` → same warning set, exit 0
(338 rows by the grep); the S398-S401 warning check is the diff of the two
emits (empty). Tool receipts committed beside them: `selftest.txt`
(9/9, exit 0), `windesk-live1.txt` (CLEAN), `xprobe-indep.txt` +
`crosscheck.txt` (5/5 AGREE), `fromfile-rerun.txt` (snapshot re-derivation),
`gate-nolive-windows.txt` (the absence receipt), `snapshot-live1.json`,
`PINS.txt` (tool and gate sha256 at the landing commit).

## Considerthese and assimilation

- Mined all nine `considerthese/` files; none adoptable this round: 2026-10-28
  proposal 2 was already addressed (r56 attempt-2 receipt), the 2026-10-19
  "refresh the live plane" proposal is void (its object host is gone — the
  proposal itself predates the swap and is now answered by C1's absence
  register), and the remainder are operator-process suggestions outside the
  lane's write surface.
- Assimilation: none — shokuknow unreachable.

## Route to round 58 (intent only; no commitment)

1. Host-portable scratch policy for the fail-closed checkers (M57-1), so the
   r55/r56 control harnesses become runnable here again.
2. A Windows-side criterion-107-class anchor check is unnecessary (no pin
   blobs this round), but the r56-routed kill-power items stand; they are
   git-object work and run on this host.
3. Per-monitor DPI join and the D01 flip (a Win11 DWM service-model row), if
   the operator wants the Windows plane deepened; otherwise the omarchy-plane
   disposal ruling (L0) decides whether the lane keeps two live planes.
