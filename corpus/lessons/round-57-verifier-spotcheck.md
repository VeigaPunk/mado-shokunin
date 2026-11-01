author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

# mado round 57 — verifier spot-check (closure, non-author)

Lane repo: `C:/Users/jpvei/.zcode/workspace/95b1ba4d-5089-47a4-9fd8-54adebbce2ae/fleet/mado-shokunin`
base `5337d2509f5c91c6f200b6637cf77bd0ad1cd67f` → tip `f71c0f98e0b38e56f811bdc6018498f6413ed9be`.
I did not author this round; everything below is my own re-derivation over committed bytes
(index-free git only), live read-only probes, and source re-opens. Security boundary held in
this verification: no r56-era credential material was opened or surfaced; only round-57
receipts were read.

## 1. Conformance results

| check | command (abbreviated; run 2026-10-31/11-01 UTC) | observed | result |
|---|---|---|---|
| report landed by lane identity | `git -C <fleet> log --format='%an %H' -1 -- .ufo/reports/round-57/mado.md` | `mado-shokunin e4236d608c9588dfbee719b01187daecbaf6685c` | PASS |
| `SHONEN` heading | read of the report | `## SHONEN` with one `[~]` line per box (4 boxes, each with a pointer) | PASS |
| cited commits exist + are ancestors | `git merge-base --is-ancestor 13b00d5c… / f71c0f98… refs/heads/master` | both: yes | PASS |
| branch tip pushed | `git rev-parse refs/heads/master` vs `git ls-remote origin refs/heads/master` | both `f71c0f98e0b38e56f811bdc6018498f6413ed9be` | PASS |
| round work in range | `git log 5337d2509f5c..f71c0f98e0b38e56f811bdc6018498f6413ed9be` | exactly the two cited commits (13b00d5c work, f71c0f98 receipts) | PASS |
| marker rule | report content | real report: work performed, evidence pointers, landed changes tied to LOG, measurements, Sources & frontier, trends, SHONEN — not a marker | PASS |
| landed-changes match report table | `git diff-tree -r --name-status 5337d25 f71c0f98` | exactly the 20 paths the report's table names (10 receipts, tools/mado-win-desk.py, knowledge entry, lesson, plus M-logs) | PASS |
| no existing registry row cell rewritten | `diff-tree -p … -- corpus/SOURCES.md` deletions count | 0 deleted lines (additions only: S398-S401 + search log) | PASS |
| gate bytes untouched | `git rev-parse 5337d25:tools/mado-verify.sh` vs `f71c0f98:…` | identical blob `9113c7c05e58…` (stronger than the reported sha256 equality) | PASS |
| census exit 0 at closure | `bash scripts/sources-census.sh validate --root <fleet> mado` | `mado ok`, exit 0; 36 W04 + 1 W01, all pre-existing (matches committed census receipts, which diff empty) | PASS |
| L0 line appended | `grep '^mado \| round-57' .ufo/l0-questions.md` | fleet working-tree line 228 (rubric disposal + L2 floor question); integrator/orchestrator commits it with the integration commit | PASS (durability pending, normal) |
| LOG entry | `git show f71c0f98:LOG.md` | `## Round 57 (2026-10-31, hyaku run 12)` block at :2678 | PASS |

Conformance notes (status-neutral, none bars admission):

1. The dispatched prompt does not state the MISSION ≥8-L2 batched-dispatch floor (round-level
   embed item). The lane disclosed the shortfall itself in SCORECARD/LOG/report and filed the
   L0 question — the defect is in the dispatch artifact, not the lane's work.
2. The C2 sub-claim "malformed snapshot → `MADO_WINDESK: ERROR` exit 2 with raw bytes never
   echoed" has no committed receipt (the ERROR path exists at `tools/mado-win-desk.py:119`; the
   selftest receipt covers 9 assertions but no observed ERROR run is committed). Evidence gap,
   not a claim-defeater; route below.
3. M57-1 (lane-mined): the r55/r56 checkers' `--selftest` modes are unrunnable on this host
   (fail-closed scratch policy). Disclosed by the lane; not a red gate this round (the ledger
   checker's non-selftest mode ran green).

## 2. Per-claim re-check

Re-measured = I ran the plain measurement myself. Evidence-verified = I checked the committed
receipt/tally and did not re-execute a lane-owned gate or selftest.

### C1 freshness — re-measured → improved

- `git show 5337d2509f5c…:PROVINCE.md | grep -cE '^\| .* \| (absent|observed) \(2026-10-31\) \|'` → **0**
- `git show f71c0f98e0b3…:PROVINCE.md | grep -cE '^\| .* \| (absent|observed) \(2026-10-31\) \|'` → **8**
- Register spot-read at tip: 8 groups (7 `absent` + 1 `observed`), each row dated 2026-10-31
  with its re-derivation probe; the register's group set covers the omarchy-era `**Owns
  (surfaces)**` paragraph (7 groups) plus the new Windows desktop plane.
- Supporting probes re-run live by me (read-only): 0/11 binaries present, 0/10 trees present —
  agrees with the register and the committed `gate-nolive-windows.txt`
  (`MADO_VERIFY: DIVERGED (17 fail, 7 unknown, 2 pass)`, first fail `hypr.file.root`,
  `gate.boundary.readonly PASS`).
- Rubric re-baseline is declared with reason in SCORECARD (new "surface-state audit currency"
  0→10; old "file-plane gate agreement" 9.6552 recorded **dormant, host-absent**, disposal
  routed to L0) — a disclosed re-baseline, not a silent rewrite. No freshness harm.

### C2 operability (capability acquisition) — evidence-verified → improved

- Tool absent at base, present at tip (`git ls-tree`); committed blob sha256 recomputed by me:
  `92a51aec1cf1bd579256d2c00e00d538e339f3551b427bc1a7224005b3eee712` — equals `PINS.txt` and
  the report's value.
- Committed receipts match the report exactly: `selftest.txt` (9/9, OK), `windesk-live1.txt`
  (`MADO_WINDESK: CLEAN (screens=1 dpi=96 dwm=on windows=6)`), `xprobe-indep.txt` +
  `crosscheck.txt` (5/5 stable fields AGREE, window census bound-only), `fromfile-rerun.txt`
  (snapshot re-derivation CLEAN), `snapshot-live1.json`.
- Tool ledger population re-counted by me over committed bytes (rows matching the row grammar,
  excluding the header's grammar example): **98 → 99**; the `tools/mado-win-desk.py` row is
  present with a `PROVINCE.md` pointer; no duplicate paths.
- Boundary spot-reads of the committed tool: no `os.environ`/environment-value reads (the only
  "environ"/"clipboard" hits are the never-prints boundary text and the selftest assertion that
  bans `MainWindowTitle`, `Get-Clipboard`, `$env:`, `ConvertTo-SecureString` from the fixed
  script); no `GetWindowText` anywhere. M56-17 criterion applied as claimed.
- I did not execute the tool or its selftest (lane-owned gate discipline); the verdict rests on
  the committed tallies plus the byte-level checks above.
- Gap noted above: the malformed-snapshot ERROR run has no committed receipt.

### C3 coverage (sourced) — re-measured + sources re-opened → improved

- Knowledge files `git ls-tree … corpus/knowledge/ | grep -c '\.md$'`: **71 → 72**.
- README index rows (`grep -cE '^\| `knowledge/[^`]+\.md`'`): **71 → 72** (new entry indexed).
- SOURCES registry rows (`grep -cE '^[[:space:]]*\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`):
  **334 → 338** (S398-S401, tier A docs, `mined`, opened 2026-10-31, used-by names the entry
  and the lesson).
- All four newly written rows re-opened 2026-10-31/11-01; every ≤25-word quote verified as a
  verbatim substring at the named anchor, and every recorded ms.date/git_commit matched the
  live page front matter (table below, incl. D01).
- Entry `corpus/knowledge/windows-desktop-plane-r57.md` spot-read: layers kept separate
  (H rows host/probe-backed, K rows dated `[INF-docs]`, J01 marked a vacuous agreement, J02
  carries S400's own manifest caveat — which I confirmed on the live page).

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | improved | C3 re-measured (71→72 indexed entries, 334→338 sourced rows); first sourced record of the new live plane; index reachability intact |
| operability | improved | C2 capability landed with committed able-to-fail receipts (selftest red twice before green — M57-2/M57-4); ledger row entered same round (98→99) |
| freshness | improved | C1 re-measured (register 0→8 dated, probe-backed; probes re-run live by me); old rubric frozen dormant with disclosure, nothing silently rewritten |
| depth | unchanged | no depth claim this round; SKILL § Round 57 is additive host-scoping of existing claims (spot-read), no existing claim text rewritten |
| calibration | improved | every self-assessment I checked matches observed state (L2 shortfall disclosed, dormant-not-retired, J01 marked vacuous, M57-3 counting-command honesty); the outside admit/reject sample agrees (below) — the outside check prior rounds lacked |
| adjacency | unchanged | no cross-domain absorption; secret-shaped values stay kagi's (restated in PROVINCE/SKILL); contested ground untouched |

No axis harmed. All three declared claims verify → **admitted**.

## 4. Spot-check table (gate decisions, sample)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S398 High-DPI page (admit) | admit, tier A docs | fetched learn.microsoft.com/…/high-dpi-desktop-application-development-on-windows | agree | quote "By default, the system considers desktop applications DPI unaware and bitmap-stretches their windows." verbatim at § DPI Awareness Mode; ms.date 2026-09-10, git 55e845e9… match the row; 13 words |
| S399 DWM overview (admit + D01) | admit, tier A docs | fetched learn.microsoft.com/…/dwm/dwm-overview | agree | "Desktop composition is performed by the Desktop Window Manager (DWM)." verbatim (intro); ms.date 2018-05-31, git 26465e18… match; the Vista/7-era sentence "The Desktop Window Manager runs as a Windows service. It can be enabled and disabled…" is really on the page, so divergence D01 vs S400's "As of Windows 8, DWM composition is always enabled." + observed TRUE is a genuine, correctly-classed era drift |
| S400 DwmIsCompositionEnabled (admit) | admit, tier A docs | fetched learn.microsoft.com/…/nf-dwmapi-dwmiscompositionenabled | agree | "As of Windows 8, DWM composition is always enabled." verbatim at § Parameters Note; ms.date 2018-12-05, git 92672624… match; the manifest caveat J02 relies on is on the page ("If no such manifest entry is found … receives a value of FALSE") |
| S401 Screen class (admit) | admit, tier A docs | fetched learn.microsoft.com/…/system.windows.forms.screen | agree | "Represents a display device or multiple display devices on a single system." verbatim at § Definition; AllScreens = "Gets an array of all displays on the system." verbatim in § Properties; ms.date 2025-07-01, git e2eb860a… match |
| Re-point `mado-verify.sh` at Windows substitutes (reject) | rejected | `git rev-parse` blob identity base↔tip + gate receipt | agree | the gate stayed byte-untouched and honestly reports the absent plane; corrupting a frozen instrument's EXPECT list to manufacture a pass would be worse than DIVERGED |
| Retire the omarchy-host freshness rubric (reject) | rejected (kept dormant, host-absent) | SCORECARD round-57 section + L0 line 228 | agree | the 9.6552 stays on record as a real measurement of a real host; disposal is routed to the operator instead of being self-executed |
| Per-monitor DPI row from registry alone (reject) | rejected | entry J-row region + S398/S400 page text | agree | AppliedDPI/LogPixels are system-level values; a per-monitor table needs `GetDpiForMonitor`/`GetDpiForWindow` — declining the overreach is correct calibration |

Sample size: 4 admits (all four new rows) + 3 rejects — exceeds the ≥1 admit / ≥1 reject bar;
all agree, so per LEARNING.md the discernment trend may be scored `improved` (the outside
judgment the round deferred to closure is now on record, here).

## 5. Trend verdicts (closure's ruling)

- **expansion: improved** — one new declared surface observed and sourced: knowledge entry
  71→72 (indexed, reachable), registry 334→338 with four `mined` tier-A rows whose `used-by`
  cites the entry; the abandoned plane's absence is registered, not dropped. Re-measured.
- **quality: improved** — the host-swap drift every present-tense claim carried is now named,
  dated and probe-backed; no existing artifact byte was rewritten to fake continuity (SOURCES
  additions-only, gate blob identical, ledger grammar intact); the instrument landed red-first
  (M57-2, M57-4) with committed receipts. Evidence-verified + re-measured.
- **discernment: improved** — the lane self-graded `unchanged` pending outside judgment; this
  spot-check supplies it: 4 admits + 3 rejects re-opened, all agree, no disagreement left
  unlearned; layers discipline (docs vs host facts) verified in the entry. Per LEARNING.md's
  table (spot-check agrees on admits and rejects), improved.

## 6. Routed defects / items for the lane's next round

1. Commit a malformed-snapshot receipt (`MADO_WINDESK: ERROR` exit 2, raw bytes not echoed) or
   fold that assertion into the selftest tally, so the C2 ERROR-path claim carries committed
   evidence (from closure note 2).
2. M57-1 (lane-routed, stands): host-portable scratch policy for the fail-closed checkers so
   the r55/r56 `--selftest` modes run on this host.
3. Operator items (not lane debt): rule on the L0 questions (omarchy freshness-rubric disposal;
   L2 floor on this host); the dispatched round prompt omits the MISSION ≥8-L2 floor from its
   embedded contract (orchestrator-side template gap — the lane self-disclosed regardless).
4. SHONEN: all four boxes are `[~]` author-asserted. In this verifier's judgment all four are
   checkable by a non-author reviewer from committed evidence (box 2 on this round's
   sweep→register→observer→sourced-entry chain alone; boxes 1/3/4 on the repo's SKILL/corpus/
   PROVINCE state). Per duty I wrote no `[x]`; the operator may commission the promotion review.

Closure: status ok, admitted true. Spot-check file authored by the non-author closure judge;
the orchestrator commits it.
