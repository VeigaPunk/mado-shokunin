# mado round 64 — verifier spot-check

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

Date 2026-11-01. Lane repo `C:/Users/jpvei/.zcode/workspace/95b1ba4d-5089-47a4-9fd8-54adebbce2ae/fleet/mado-shokunin`
(branch `master`), base `7fe65562c15d20e5cfdc1da536f774149ab52b7e`, head
`66b8994b6397e27904779a26264c0196d2bd0368`. I did not author this round; every check below
was run by me at closure time with index-free git only (`rev-parse`, `cat-file`, `ls-tree`,
`diff-tree`, `merge-base --is-ancestor`, `show`, `log`, `ls-remote`) — no `git status`, no
mutating command, no sibling gate executed. The r56-era security boundary was observed: no
r56-era blob was opened, diffed, or surfaced; the citecheck runs below scan only the r63/r64
receipt trees; file-identity checks on larger records were byte-prefix comparisons (cmp /
head -c), with no record content dumped. Tools were run from committed bytes extracted into a
closure scratch dir (`scratch/mado-r64-closure`), invoked `python -I`.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by lane identity | `git -C <fleet> log --format='%an <%ae> %H %ad' -1 -- .ufo/reports/round-64/mado.md` | `mado-shokunin <mado@shokunin.local> 68783cbbf5f034693161e1602c153eee237741ac Sun Nov 1 08:12:31 2026 -0800` | PASS |
| Report content committed == filed | `git show HEAD:.ufo/reports/round-64/mado.md` vs worktree file, `cmp` | identical | PASS |
| `SHONEN` heading | read report | `## SHONEN` with 4 `[~]` lines, each with an evidence pointer | PASS |
| Cited lane commits exist + ancestral | `cat-file -e <h>^{commit}`; `merge-base --is-ancestor <h> refs/heads/master` for `688144573a26`, `8c5af6ad`, `ecfcea41`, `66b8994b` | all exist, all ancestral | PASS |
| Base is ancestor | `merge-base --is-ancestor 7fe65562c15d refs/heads/master` | yes | PASS |
| Tip pushed | `ls-remote origin refs/heads/master` vs `rev-parse refs/heads/master` | both `66b8994b6397…` | PASS |
| Cited work reachable in round range | `git log 7fe65562c15d..66b8994b…` | exactly the four cited commits | PASS |
| Timing vs watchdog digest | report commit 08:12:31 -08:00 vs `complete mado round=64 … 08:12:30-08:00` | report lands last, one second after the complete line; lane commits 15:39–16:04 UTC sit inside launch 06:23:52 → complete 08:12:30 -08:00 | PASS |
| Dispatched prompt fidelity | read `.ufo/prompts/mado-round-64.md` | full round contract embedded (mission/axes binding, L2 minimum, commit-then-push, push scope, L0 channel, report path, commit-before-report, SHONEN heading rule, hash-citation rule, write scope); prompt committed at fleet HEAD | PASS |

Conformance defects: none. Two status-neutral number drifts in report prose are recorded in
§8 below.

## 2. Claims re-check

### C1 — calibration (the r63 carry-in repair) — TARGET_MET, re-measured

- Fixture presence: `git ls-tree <rev> --name-only -- .ufo/waves/round-63/receipts/broken-fixture.json | wc -l`
  → **0** at base `7fe65562`; **1** at landing `688144573a26`. Re-derived exactly as reported.
- Verdict re-derivation: I extracted the tool and fixture at the landing rev
  (`tools/mado-win-displayconfig.py` unchanged across the range — `diff-tree` empty) and ran
  `python -I mado-win-displayconfig.py --from-file <fixture>` → **rc=2**, stdout
  `MADO_WINDISPLAYCONFIG: ERROR (stage=parse detail=JSONDecodeError in snapshot <path>)` —
  the same whitelisted detail shape; the committed receipt
  `.ufo/waves/round-64/receipts/windisplayconfig-errorpath-r64.txt` is byte-identical to the
  r63 receipt's line `MADO_WINDISPLAYCONFIG: ERROR (stage=parse detail=JSONDecodeError in
  snapshot .ufo/waves/round-63/receipts/broken-fixture.json)`.
- Disclosure: the re-creation (r63 original bytes ephemeral/unrecoverable) is stated at every
  claim site (entry Update `## Update (round 64) — the r63 receipt's fixture citation
  repaired (carry-in)`, lesson Gate, LOG, SCORECARD). The routed item exists: r63 spot-check
  names it (`round-63-verifier-spotcheck.md` line 178).
- Verdict: **improved** on calibration; the honest-unknown discipline kept (raw bytes never
  echoed; the r63 receipt remains the record of the r63 run).

### C2 — coverage, sourced (the D05 flip-condition probe) — TARGET_MET, re-measured

- Entry row sites: `git show <rev>:corpus/knowledge/windows-displayconfig-r63.md | grep -cE '^\| [HJK][0-9]{2} '`
  → **19** at base, **23** at landing and head. `grep -c '^## Update (round 64)'` → **0 → 2**
  (two Update sections: the probe and the carry-in repair). Base entry is 105 lines and a
  verified byte-prefix of head (§3).
- Probe determinism: extracted committed `qdc-matrix-run1.json` / `run2.json`, `cmp` →
  **identical, rc=0** (twice-byte-identical claim verified from committed bytes).
- Crosscheck re-run: extracted committed `qdc-matrix-crosscheck.py` plus its two named inputs
  (r63 snapshot + run1) into a scratch repo shape; `python -I crosscheck.py <scratch>` →
  **19/19 stable fields AGREE, exit 0** — reproduced exactly.
- Probe safety: committed `qdc-flagmatrix-probe.ps1` greps clean of `Set-` verbs, `Out-File`,
  `New-Item`, `Remove-Item`; P/Invoke surface is `GetDisplayConfigBufferSizes` +
  `QueryDisplayConfig` only (getters). Receipt JSON carries aggregate/structural fields only —
  no ids, no LUID halves, no names.
- H29 from the committed run bytes: leg `qdc_flags=0x42` is **identical to the 0x02 baseline
  leg modulo the `qdc_flags` field** (verified programmatically: deep-compare after popping
  the flags key → True), including `mode_info_types [2, 1]`, `path_flags 0x1`, target idx 0,
  refresh 64/1, and pixelRate/hSync/vSync all **4294967294 (0xFFFFFFFE)** — the sentinel
  included.
- H30 from the committed run bytes: legs `0x12`/`0x52` show buffer 1 path / **3 modes**,
  `mode_info_types [2, 1, 3]` (the third entry infoType 3, the documented DESKTOP_IMAGE
  vocabulary), `path_flags 0x1 → 0x9` (bit 0x8, the documented SUPPORT_VIRTUAL_MODE), and
  `target.mode_info_idx 0 → 2` with the decode guard emitting `target_mode = null` (fields
  absent/null at that non-TARGET index). The two virtual-mode legs are identical to each
  other modulo flags (True).
- H31 / the honest-unknown: entry line 58 keeps D05's cause **`[UNK]`** byte-untouched
  (append-only Update); H31 states **narrowed, not flipped** — D05's flip ("a query shape
  that returns decoded frequencies") did not fire under any documented shape; remaining
  residue (driver-class / second-host) is named operator-scoped. The narrowing rests on the
  committed two-run probe receipts, which I verified as above.
- Sourced: the claim rests on S424, re-opened this round (see §6).
- Verdict: **improved** on coverage.

### C3 — operability, capability acquisition (`tools/mado-receipt-citecheck.py`) — TARGET_MET, re-run

- Tool presence: `git ls-tree <rev> --name-only -- tools/ | grep -c citecheck` → **0** at
  base, **1** at landing.
- Selftest re-run (from committed bytes at head): `python -I mado-receipt-citecheck.py
  --selftest --scratch-root <closure-scratch>/st` → `MADO_CITECHECK_SELFTEST: 12/12
  assertions passed`, **rc=0**.
- Red re-run at the base rev: `--repo <lane> --rev 7fe65562… --paths <lane>/.ufo/waves/round-63/receipts`
  → `files=26 citations=9 resolved=8 missing=1 … verdict=TARGET_MISSED`, **rc=1**; the single
  MISSING is exactly `.ufo/waves/round-63/receipts/broken-fixture.json` cited from
  `windisplayconfig-error-path.txt` — the routed citation. Byte-substance match with the
  committed receipt `citecheck-red-base-rev.txt` (path-separator styling only differs:
  relative vs absolute scan paths).
- Green re-run: **TARGET_MET, missing=0, rc=0 at every scope I ran** — full round-64 dir
  (19/19), receipts dirs of the current worktree (18/18), and the exact 45-file committed
  tree at the repair rev extracted to scratch (14/14).
- Reconciliation of the receipt's recorded `16/16` (files=46): at `8c5af6ad` the two receipt
  dirs commit **45** files; the recorded run also scanned the then-in-progress
  `landing-counters-r64.txt` draft (46th file), whose mid-draft bytes carried 2 unique
  citations → 14+2=**16**. The final committed counters receipt carries exactly **4**
  citations unique to it (`tools/mado-receipt-citecheck.py`, `tools/mado-win-displayconfig.py`,
  `corpus/knowledge/windows-displayconfig-r63.md`, `quality/tool-ledger.md` — computed with
  the tool's own extraction function), so today's worktree scan reads 18. Arithmetic bracket
  exact (14 ≤ 16 ≤ 18); the load-bearing verdict (all citations resolve, rc=0) reproduces at
  every scope. No defect.
- Ledger 103 → 104: **evidence-verified, gate not executed** (lane-owned gate). Base state
  receipted in `before-state-r64.txt` (`population=103 ledger_rows=103 uncovered=0 dangling=0
  TARGET_MET`, rc=0). Both landing states receipted in `landing-counters-r64.txt` named
  sections: red at the landing (`population=104 ledger_rows=102 uncovered=2 dangling=1
  TARGET_MISSED rev=68814457…`) and green at the repair (`population=104 ledger_rows=104
  uncovered=0 dangling=0 TARGET_MET rev=8c5af6ad…`); the red leg's true rc=1 is in
  `ledger-red-leg-rc.txt` (the receipt discloses that its in-receipt `LEDGER_LANDING_RC=0`
  is tail's rc, an in-round receipt defect caught and disclosed — QUALITY 26).
- Verdict: **improved** on operability; capability row entered the SCORECARD table the same
  round with the red+green demonstration.

### Re-measured vs evidence-verified

- Re-measured by me: every git-count claim in the report (fixture 0→1, rows 19→23, Update
  0→2, tool 0→1, SOURCES 371→371, range numstat), the C3 selftest/red/green runs, the
  crosscheck re-run, run1/run2 `cmp`, the C1 verdict re-derivation, the five byte-prefix
  checks, leg-level JSON facts.
- Evidence-verified (committed receipts read, gate not executed): the ledger counter's three
  states (base/landing/repair), navigation 78/78 and used-by TARGET_MET at the repair,
  harmwatch selftests (55/55, 63/63), the mado-verify sha prefix `050efc720599345a`, census
  start/after receipts.

## 3. Disclosed in-round defects — restorations verified

- **M64-1 (backtick echo in the before-state script).** The committed
  `before-state-r64.txt` is the re-run's output and is complete (runs every base counter
  with per-producer rc; ends `== before-state end ==`). Disclosed in the lesson `## Mistakes`
  with class (`measurement`), evidence, captured-by, and fix. Status-neutral.
- **M64-2 (truncated heredoc; SCORECARD restored byte-exact).** Verified: base SCORECARD
  (`375162` bytes measured via `wc -c` on `git show base:SCORECARD.md`) is a **byte-prefix**
  of head SCORECARD (`cmp` of the first 375162 bytes: PREFIX_OK); the base..head SCORECARD
  diff is a pure append (numstat 99/0; zero removed lines) with exactly the four r64 headers
  (`## Round 64 …`, `### Capabilities (round 64)`, `### Planned (round 65; intent only)`,
  `### Corrections (round 64)`). Disclosed in lesson Mistakes + Addendum, LOG amendment, and
  the SCORECARD Corrections block.
- **Ledger-append glue (red→green).** Landing `688144573a26` numstat on
  `quality/tool-ledger.md` = 1/1 (the glue); repair `8c5af6ad` = 2/1 (the split); range
  −1 comes solely from this file. Verified the r63 row restored byte-exact: base ledger is
  exactly **32955 bytes** (matching the lesson's head-prefix cmp figure) and its final byte
  is not a newline (the glue precondition); those 32955 base bytes are a **byte-prefix** of
  the repair commit's ledger (cmp PREFIX_OK). Both counter states receipted (§2 C3).
  Disclosed in the repair commit message, lesson Addendum, SCORECARD Corrections, LOG
  amendment.
- Prefix preservation re-verified for all five records named in the landing counters receipt:
  entry (14402 bytes), PROVINCE.md (42090), LOG.md (283115), SCORECARD.md (375162) as
  byte-prefixes of head; `quality/tool-ledger.md` (32955) as a byte-prefix of the repair.

## 4. No owned axis harmed

`git diff-tree -r -p 7fe65562c15d 66b8994b… -- SCORECARD.md` is a pure append (99/0); spot
reads confirm the prior tables stand and the round only appends the Round 64 section,
capabilities row, Planned, and Corrections. Base posture re-measured in the committed
before-state receipt (navigation 78/78 = 10.0000, used-by TARGET_MET, ledger 103 TARGET_MET,
registry 371; carried tables unchanged). Harm watch receipts: census exit 0 both ends
(re-run by me at closure — §6), both observers re-measured unchanged (`windisplayconfig-recheck-r64.txt`
CLEAN 64/1 vsync=unavailable(0xfffffffe); `dwm-recheck-r64.txt` timing=unavailable
hr=0x88980090 — D04 and the D05 baseline stand), prior tools' bytes untouched (only the new
tool file added under tools/), SOURCES.md absent from the range diff (no registry cell
edited). No axis regressed.

## 5. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 verified: the routed ephemeral-fixture citation now resolves to committed bytes with the verdict re-derived (rc=2, identical whitelisted line) and the re-creation disclosed at every site |
| coverage | improved | C2 verified: the D05 flip-condition dimension measured with committed two-run receipts; entry 19→23 row sites; sourced on the re-opened S424 |
| operability | improved | C3 verified: capability runs (selftest 12/12 re-run; red TARGET_MISSED at base re-run; green reproduced at every scope); ledger 103→104; PROVINCE refined append-only |
| depth | unchanged | no depth-axis move claimed; prior tables stand (SCORECARD pure append) |
| freshness | unchanged | both prior observers re-verified unchanged with committed receipts; no freshness move claimed |
| adjacency | unchanged | no cross-domain evidence absorbed; PROVINCE change is a same-domain tool refinement, append-only |

## 6. Discernment spot-check (non-author)

SOURCES.md rows **371 → 371** measured at base and head (`grep -cE '^[[:space:]]*\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`);
SOURCES.md is absent from the range diff — the round's claim of no new row and no cell edit
is true, so there is no newly written row to re-open; the round's opened source is the S424
**re-open**, quoted in the lesson Gate, which I re-opened.

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S424 re-open (lesson Gate admit) | admit | Live page `https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-querydisplayconfig` fetched 2026-11-01 | **agree** | Quote verbatim on the page (§ Parameters flags OR-table, QDC_VIRTUAL_REFRESH_RATE_AWARE row): "This flag should be bitwise OR'ed with other flags to indicate that the caller is aware of virtual refresh rate support." (21 words ≤ 25); QDC_VIRTUAL_MODE_AWARE 0x00000010 "Supported starting in Windows 10", QDC_VIRTUAL_REFRESH_RATE_AWARE 0x00000040 "Supported starting in Windows 11"; example declares `UINT32 flags = QDC_ONLY_ACTIVE_PATHS | QDC_VIRTUAL_MODE_AWARE;`; metadata ms.date 2018-12-05, updated_at 2026-05-15, git_commit `39f250c30f4e46de1ef92f2ef07161753ba36e35` — all exactly as the lesson records |
| Entry Update rows H29/H30/H31/J29 (admit) | admit | Committed run JSONs `qdc-matrix-run1/2.json` (byte-identical) + crosscheck re-run | **agree** | Every row's measured facts re-derived from the committed bytes (§2 C2); the narrowing honestly stops at [UNK] where the flip did not fire |
| Reject: evolving `tools/mado-win-displayconfig.py` with a virtual-flags option | reject | `diff-tree` (tool absent from range) + `windisplayconfig-recheck-r64.txt` | **agree** | Tool bytes genuinely unchanged and the r63-v1 verdict shape re-measured unchanged, so the stated reason (committed receipts pin r63-v1 bytes; a tool change would invalidate the crosscheck byte-match) holds; flip condition is coherent |
| Reject: decoding the DESKTOP_IMAGE union member | reject | H30 row + entry Limits section | **agree** | No claim this round needs the member's storage; the class is named from the documented vocabulary; flip (a claim joining the fields with the page opened) is coherent — judgment, not re-measurement |

Census validate re-run at closure:
`bash <fleet>/scripts/sources-census.sh validate --root <fleet> mado` → **exit 0**, `mado ok`,
warning set **36 W04 + 1 W01** — identical to the committed `census-start-r64.txt` /
`census-after-r64.txt` warning set.

## 7. Trend verdicts (with evidence)

- **expansion: improved** — a capability entered the repertoire table with a demonstrated
  red+green (C3), and coverage gained measured ground the map did not hold (H29–H31, entry
  19→23 row sites), sourced on the re-opened S424.
- **quality: improved** — the routed citation now resolves to committed bytes with the
  verdict re-derived; a durable read-only instrument replaces the manual find; both prior
  observers re-verified unchanged; the three in-round write defects were each caught by a
  gate or read-back, disclosed in four places, and repaired byte-exact (§3) — no defect
  smoothed.
- **discernment: improved** — D05 recorded "narrowed, not flipped" against a result that
  would have tolerated a flipped headline; the decode guard emitted null rather than decoding
  an undocumented union member; the landing's red ledger state is disclosed rather than
  silently repaired; rejected rows kept with flip conditions; this outside spot-check agrees
  with the gate on the sampled admits and rejects (§6).

## 8. Routed defects and notes for round 65 (status-neutral; none bars admission)

1. **Report numstat drift**: report says "Range numstat `7fe65562..66b8994b`: 30 files,
   +1192/−1"; measured at closure: **31 files, +1193/−1** (`git diff-tree -r --numstat`).
   One 1-line file and its line are uncounted in the report prose. Status-neutral number
   drift; the −1 attribution to the ledger split is correct.
2. **Receipt-count prose drift**: report's Landed changes says "18 round-64 receipt files";
   the landing commit carries **19** files under `.ufo/waves/round-64/receipts/` (plus the
   claims declaration at `round-64/` top). Immaterial counting-convention drift.
3. **In-receipt rc quirk (self-disclosed)**: `landing-counters-r64.txt` prints
   `LEDGER_LANDING_RC=0` for the red landing state (tail's rc); the true rc=1 lives in
   `ledger-red-leg-rc.txt` and the receipt names this. Already disclosed in-round; no action
   beyond the QUALITY 26 rule the lane already cites.
4. Carried from the round (unchanged, operator-owned): the five L0 questions (omarchy
   freshness disposal; gate-selftest host gap; calibration resolved-active re-derivability;
   screen-capture scope; the L2 floor) remain open and were routed around, never treated as
   answered; D05's remaining residue is operator-scoped; the citecheck's standing use in the
   landing counters is the lane's stated round-65 intent.
5. SHONEN note for the operator: all four boxes are `[~]` with resolvable historical
   pointers, and each line accurately states that non-author verifier independence is not
   yet established. Box 4 (no cross-domain bleed — PROVINCE append-only refinement, no
   boundary change) and box 3 (Verify blocks/receipt commands re-runnable from committed
   bytes — this spot-check re-ran several) now look fully checkable by a commissioned
   non-author review; per protocol I did not write `[x]`.

## 9. Closure judgment

All three declared claims verify (two re-measured end-to-end, one re-run from committed
bytes; lane-owned gate states evidence-verified, never executed); no owned axis is harmed;
conformance is clean; the disclosed in-round defects are repaired byte-exactly with both
ledger states receipted. The round is **admitted**.
