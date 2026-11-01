# Round 60 — mado lesson (hyaku run 12)

Base `d1e64880b375529de185f49e124dd6cc42c58e75` (the r59 verifier spot-check).
Host: Windows 11 Home, build 26200, as in rounds 57-59. Three claims: **C1
calibration** (the r59 carry-in corrections — the SCORECARD round-59 C1 row's
parenthetical "(+4/−0, +5/−0)" corrected to the measured per-file +17/−0 and
+5/−0 append-only; the LOG round-59 tail bullet's "M59-1..M59-3" and the
same-class SKILL § Round 59 ground line corrected against the lesson's four
mined mistakes — defect lines preserved, corrections carry re-derivation
commands), **C2 coverage** (sourced entry
`knowledge/windows-dpi-awareness-metrics-r60.md` — rows S406-S411 opened in
full before any row was written; the r58 entry's caller-branch residues J05/J07
closed for the launch shape with the vacuous metrics join named), **C3
operability** (capability acquisition `tools/mado-win-dpi.py` — the durable
DPI-virtualization observer: selftest 10/10, live CLEAN twice byte-identical,
from-file re-derivation, ERROR path fail-closed, crosscheck 5/5, ledger 99 →
100). L1-only round again: the MISSION ≥8-L2 dispatch floor has no surface on
this host (disclosed since r57, L0 open; unchanged). The security boundary held
throughout: no r56-era credential material was opened or surfaced; the round
touched only the files named in the report.

## Gate

### Admitted

- **Rows S406-S411** (tier A, `mined`, opened 2026-10-31 on the Windows host;
  every page opened in full via fetch BEFORE any row was written; every quote
  below is a verbatim substring of the opened body):

  | row | URL | located quote (≤25 words) |
  |---|---|---|
  | S406 | `https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetrics` | "Note that all dimensions retrieved by GetSystemMetrics are in pixels." (ms.date 2018-12-05, git_commit fa53641576e3603fa7b66d3a4ad969d3ce49d6f3, updated_at 2025-07-01) |
  | S407 | `https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetricsfordpi` | "This function returns the same result as GetSystemMetrics but scales it according to an arbitrary DPI you provide if appropriate." (same ms.date/commit) |
  | S408 | `https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getthreaddpiawarenesscontext` | "Gets the DPI_AWARENESS_CONTEXT for the current thread." (same ms.date/commit) |
  | S409 | `https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getawarenessfromdpiawarenesscontext` | "Retrieves the DPI_AWARENESS value from a DPI_AWARENESS_CONTEXT." (same ms.date/commit) |
  | S410 | `https://learn.microsoft.com/en-us/windows/win32/api/windef/ne-windef-dpi_awareness` | "DPI unaware. This process does not scale for DPI changes and is always assumed to have a scale factor of 100% (96 DPI)." (ms.date 2018-12-05, git_commit 9267262487657894a8af112d7165006fed5035a7, updated_at 2024-02-22) |
  | S411 | `https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowdpiawarenesscontext` | "The return value of GetWindowDpiAwarenessContext is not affected by the DPI_AWARENESS of the current thread." (same ms.date/commit as S406) |

  One search sweep, bounded to the six documented getters the round's probe
  actually calls (search log § Round 60); no rejected-row event — all six
  opened pages were included. S404 is a reused row re-opened this round at its
  held URL for the J14 join; its `used-by` cell was extended in place:
  `…windows-desktop-plane-r57.md` → `…windows-desktop-plane-r57.md,
  corpus/knowledge/windows-dpi-awareness-metrics-r60.md, corpus/lessons/round-60.md`
  (old→new logged here per the SOURCES contract).

- **Entry** `knowledge/windows-dpi-awareness-metrics-r60.md`: 4 host rows
  (H13-H16, each with its re-derivation command; probe is a committed receipt
  artifact, two byte-identical runs rc=0), 7 documented rows (K21-K27,
  `[INF-docs]`, dated), 4 joins (J13-J16; J13 carries the vacuous-shape
  caveat, J14 the point-in-time and same-shape caveats), and § 4 closes the
  r58 entry's J05 caller `[UNK]` **for the launch shape** with the r58 process
  context staying `[UNK]` (disclosed, not overwritten; the r58 entry's bytes
  are untouched). Limits restated: no rendered pixel (screen-capture scope
  now filed as an L0 question this round, routed around), point-in-time
  census/foreground. Layers stay separate per QUALITY 15/16.

- **Capability (C3)**: `tools/mado-win-dpi.py` (`VERSION r60-v1`): selftest
  10/10 rc=0; live `MADO_WINDPI: CLEAN (awareness=unaware metrics=1920x1080
  dpi96=1920x1080 windows=6 fg_dpi=96)` rc=0 twice, byte-identical;
  `--from-file` re-derives from the committed snapshot rc=0; malformed
  snapshot → `MADO_WINDPI: ERROR (stage=parse …)` rc=2, raw bytes never
  echoed; crosscheck 5/5 stable fields AGREE against the independently
  executed probe (receipt `windpi-crosscheck.txt`); the documented
  GetSystemMetrics 0-failure return is treated as CHECK FAILED, never a
  measurement (named assertion); no `Set*` verb exists in the tool; ledger
  population 99 → 100 (ledger row + PROVINCE round-60 refinement in the same
  landing).

- **Record corrections (C1)**: the SCORECARD `### Corrections (round 60)`
  block (the measured per-file numbers +17/−0 and +5/−0 beside the preserved
  defect line, with `git diff-tree -r --numstat 6f2e4115 25294ab3 -- <the two
  entries>` as re-derivation); the LOG § Round 60 correction bullet (the
  round-59 tail bullet's "M59-1..M59-3" named against the lesson's four
  mistakes); SKILL § Round 60 rule 3 (the same-class § Round 59 ground-line
  defect, found by this round's sweep and named in the correction). All three
  defect lines keep their original bytes; receipt `before-state-r60.txt`
  carries every base value.

### Rejected (reasons stay; flip conditions named)

- **Building a screen-capture probe this round** (the r59 route's rendered-
  pixel candidate): the r59 lesson made the route conditional on an operator
  ruling ("if the operator rules screen capture read-only in scope"), and no
  ruling exists. The lane filed the L0 question this round (`mado | round-60`,
  the candidate shape named: statistics-only, no-persist capture) and routed
  around. **Flip:** the operator rules the capture scope; then the probe is
  claimable like any other.
- **Editing the r58 entry's `[UNK]` in place** (J05's caller awareness): the
  r58 entry is a landed record; the closure lives in the r60 entry § 4 as a
  same-shape pin. Rewriting the r58 bytes would break the append-only
  discipline the lane has held since r57. **Flip:** none — this is the
  record-honesty bar working.
- **Treating the three dormant-rubric L0 questions as answerable by
  measurement this round** (re-deriving the freshness 28/29, the gate
  selftest, or calibration resolved-active on Windows): all three disposals
  are the operator's (filed r57/r58/r59); re-scoring them lane-side would
  presume the ruling. **Flip:** an operator ruling on any of the three.

## Mistakes

- **M60-1 — selftest assertions written against an imagined output shape, not
  the implementation's actual output.** Class `measurement` (caught by the
  selftest's own first run, before any receipt was committed). Evidence: the
  first `--selftest` run printed `7/10`; three assertions failed, and all
  three were assertion-authoring bugs, not tool-logic bugs — the
  file-mode verdict line was asserted to carry `awareness=` which the code
  did not yet print (fixed by adding the field to the code, the honest
  direction), the whitelist secret value `"x"` collided with the metrics
  separator `1920x1080` (`assertNotIn("x", …)` can never pass on a verdict
  carrying dimensions), and the MainWindowHandle static count guessed 1 where
  the script has two read sites (filter + query). Captured-by: reading each
  failure against the code instead of relaxing the assertion. Fix: the
  whitelist test uses a distinctive secret (`leaked-secret-7f3a`) and asserts
  on the emitted JSON string; the static count is asserted to be exactly the
  two read sites with the output block checked handle-free; the tool's
  file-mode line now carries the awareness name (a real improvement the red
  test forced).
- **M60-2 — reading an exit code through a pipeline tail, the M58-4 class
  re-armed one level up.** Class `host-method` (recurrence of a mined
  mistake, caught the same round). Evidence: the first selftest receipt run
  was `python … --selftest 2>… | tee …; echo "RC=$?"` — the printed RC was
  tee's exit code (0) while the selftest had failed (true rc 2). M58-4 mined
  exactly this ("an exit code read through a pipeline tail — all committed
  receipts now own their rc"), and the rule was still violated on the first
  attempt. Captured-by: the receipt printed `RC=0` beside
  `MADO_WINDPI_SELFTEST: 7/10 assertions passed` — a self-contradicting
  receipt, which is itself the detector. Fix: receipts own their rc — either
  no pipe (`> file 2> file`), or `"${PIPESTATUS[0]}"` (the harm-watch receipt
  uses it). General rule: a receipt whose verdict line and rc disagree is
  malformed by construction and must never be committed as green.
- **M60-3 — a heredoc append truncated mid-line, discovered only because the
  counting was anchored.** Class `landing`. Evidence: the SCORECARD round-60
  section was appended with a large shell heredoc; bash warned "here-document
  delimited by end-of-file" and the file was left ending mid-table-row
  (`grep -c '^### Capabilities (round 60)'` → 0 while the claims table's C1
  row was already present), with the block-count greps — the same commands the
  claim cites — as the catcher. Captured-by: the anchored grep counts run
  immediately after the append (`### Corrections (round 60)` expected 1,
  found 1, but `^### Capabilities (round 60)` → 0 and `^### Planned (round
  61` → 0), then `wc -l` against the known original line count. Fix: the
  SCORECARD was truncated back to the byte-exact original 3057 lines (checked
  with `head -3057 | diff` against `git show <base>:SCORECARD.md` —
  ORIGINAL_PRESERVED) and the section appended from a written file via
  Python instead of an interactive heredoc; large appends on this host go
  through written files, and every append is followed by its anchored
  section-count greps before anything else touches the file.

## Census

Start (round start, before any edit): `mado ok`, exit 0, warning set 36 W04 +
1 W01 (identical to r57/r58/r59), 342 rows by the SCORECARD grep — output
quoted in the round report; the run was not tee'd to a file (disclosed, same
as r59). End: `.ufo/waves/round-60/receipts/census-after-r60.txt` → exit 0,
348 rows by the grep (S406-S411; the S404 used-by extension adds no warning —
the W01 class is tier-C used-by, untouched). Before-state receipt
`before-state-r60.txt` (all base values for every counting command). Tool
receipts committed beside them: dpi-awareness-probe.ps1 +
dpi-awareness-run1/run2.txt (byte-identical), windpi-selftest.txt (10/10),
windpi-live-run1/run2.txt (byte-identical), windpi-snapshot.json,
windpi-fromfile.txt, windpi-error-path.txt (rc=2), windpi-crosscheck.txt
(5/5), harmwatch-selftests-r60.txt (55/55 + 63/63), navigation-landing-r60.txt,
usedby-after-r60.txt, ledger-landing-r60.txt.

## Considerthese and assimilation

- Mined all nine `considerthese/` files again this round (2026-10-19 through
  2026-10-28; nothing new since the r58 mining): no adoptable proposal. The
  dispositions of r57-r59 stand.
- Assimilation: none — shokuknow unreachable.

## Route to round 61 (intent only; no commitment)

1. The three L0 rubric rulings (omarchy freshness disposal; gate-selftest
   host gap; calibration resolved-active re-derivability) — the SCORECARD
   tables follow the ruling, never precede it.
2. The rendered-pixel observation iff the screen-capture-scope L0 question is
   ruled; the candidate shape is a statistics-only, no-persist capture probe
   (dimensions + two-frame stability; no content, no digests printed).
3. A Win11-labeled DWM model sentence, if one surfaces, strengthens the D01
   pin (the r59 residue stands).
