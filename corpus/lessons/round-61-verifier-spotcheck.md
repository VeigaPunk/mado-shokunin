author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

# mado round 61 — non-author verifier spot-check

Closed 2026-11-01T08:27Z against lane tip `0c77f7266879a569f4b3097db4a8878406f6412b`
(base `cccda4dacc1009f767799ce62fe112fd53d2d47a`). This file is written by the
closure judge, not committed by the lane. Security boundary held on the closure
side too: no r56-era credential material was opened or surfaced; only counts
and topic names were recorded.

## 1. Step-1 conformance — PASS

| check | command | observed |
|---|---|---|
| report landed by lane identity | `git -C <fleet> log --format='%an %ae %H' -1 -- .ufo/reports/round-61/mado.md` | `mado-shokunin mado@shokunin.local 53a47d01d2ccf4367df33126b628c561b8892cb9` |
| `SHONEN` heading in committed report bytes | `git show 53a47d01:.ufo/reports/round-61/mado.md \| grep -nE '^(## SHONEN\|SHONEN:)'` | line 179 `## SHONEN`; line 200 `SHONEN: no box reached [x] …` |
| cited lane commits exist + ancestry | `git -C <lane> cat-file -t <h>`; `merge-base --is-ancestor <h> refs/heads/master` | `ad4e8403`, `0c77f726`, base `cccda4da` all commits, all ancestors of master |
| branch tip pushed | `ls-remote origin refs/heads/master` vs `rev-parse refs/heads/master` | both `0c77f7266879a569f4b3097db4a8878406f6412b` |
| cited work inside `cccda4da..0c77f726` | `git log --format='%h %an %s' cccda4da..0c77f726` | 2 commits, both authored `mado-shokunin`, subjects match the report |
| landing shape | `diff-tree -r --numstat --no-commit-id ad4e8403` | 28 files, +1416/−0, **zero deleted lines in every file** (matches the report) |

## 2. Per-claim re-check

### C1 calibration (corrections) — VERIFIED (re-measured)

- `grep -c '^## Corrections (round 61)'` on committed bytes: round-59.md **0 → 1**, round-60.md **0 → 1**; `grep -c 'landing-counters-r60'` round-60.md **0 → 3**. All as reported.
- Preservation (append-only, filed bytes intact): `git show <base>:<lesson>` diffed against the tip's first N lines — round-59.md base 217 lines and round-60.md base 181 lines are **byte-exact prefixes** of the tip versions. Combined with 0 deleted lines in the whole landing, both correction blocks are pure appends and the defect lines keep their original bytes (r59 line 74 re-read at the tip: unchanged).
- The correction's own numbers re-derive: `git diff-tree -r --numstat 6f2e4115 25294ab3 -- corpus/knowledge/windows-desktop-plane-r57.md corpus/knowledge/windows-permonitor-dpi-r58.md` → `17 0` / `5 0` exactly.
- The r60 correction's supersedings resolve: the three ghost receipt names (`navigation-landing-r60.txt`, `usedby-after-r60.txt`, `ledger-landing-r60.txt`) exist nowhere in the tree (`ls-tree -r \| grep` → nothing), and `.ufo/waves/round-60/receipts/landing-counters-r60.txt` at base carries the three named sections the correction points at (`-- navigation counter (SCORECARD fence, python for python3) --`, `-- used-by counter --`, `-- tool ledger production --`).

### C2 coverage (sourced) — VERIFIED (re-measured; lane-owned counter evidence-checked)

- Plain counts at base → tip: knowledge files `ls-tree … \| grep -c '\.md$'` **75 → 76**; README index rows `grep -cE '^\| `+backtick+`knowledge/[^`]+\.md'` **75 → 76**; SOURCES rows **348 → 354**; entry rows `grep -cE '^\| [HJKD][0-9]{2} '` on the new entry **19** (4 H + 10 K + 4 J + D03). All as reported.
- Navigation counter (lane-owned gate — committed evidence verified, not executed by the closure): receipt `.ufo/waves/round-61/receipts/landing-counters-r61.txt` at rev-pinned `ad4e8403` reads `indexed=76/76 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, `NAV_EXIT=0`; used-by `missing=0 extra=0 … verdict=TARGET_MET`. Matches the report.
- **D03 divergence and the honest unknown**: the work-area band owner is recorded `[UNK]` in three places (H19 "which appbar surface occupies the subtracted band is `[UNK]` (the taskbar is never read)"; J17 "*which* surface owns the subtracted 48 px band is `[UNK]`"; §6 Limits "The subtracted work-area band's owner … is `[UNK]` — neither artifact reads the taskbar"). The honest unknown is recorded, not papered over; PROVINCE's planned-r62 item 3 keeps the join behind an operator ruling. Verified.
- The entry opens with its provenance trio (`source: S412…S417`, `verified-at: 2026-11-01`, `recheck: on-release`).

### C3 operability (capability acquisition) — VERIFIED (re-measured; selftest + live re-run by the closure)

- **Getter-only byte check** (closure-read of the 576 committed lines): the only Win32 surface is `EnumDisplayMonitors` + `GetMonitorInfoW` + `EnumDisplaySettingsW` over `MONITORINFOEXW`/`DEVMODEW`/`RECT` — all getters. No `ChangeDisplaySettings`/`Set*` verb anywhere; the tool's own selftest asserts this (`test_fixed_script_only_getters_never_titles_handles_or_changes`). The `subprocess` call spawns exactly one read-only PowerShell child running a fixed embedded script (stdin `DEVNULL`, output parsed as JSON, raw bytes never echoed — ERROR paths print a sha256 prefix + length only). The only file writes are selftest fixtures inside a private temp dir, removed in `finally`. Working-tree file is byte-identical to the committed blob (`git hash-object` = `6418bf8027c3e9af7ce60a40d864291e9808ffaa`; sha256 `42be0205…` both).
- **Closure re-runs** (`python -I tools/mado-win-display.py`): `--selftest` → `MADO_WINDISPLAY_SELFTEST: 10/10 assertions passed`, rc=0; live → `MADO_WINDISPLAY: CLEAN (monitors=1 primary=\\.\DISPLAY1 mode=1920x1080@64 work=1920x1032)`, rc=0 — byte-for-byte the verdict lines in the committed receipts (`windisplay-selftest.txt`, `windisplay-live-run1/2.txt`, which diff byte-identical to each other, as do `display-probe-run1/2.txt`).
- Receipts read: `--from-file` CLEAN rc=0; malformed snapshot `MADO_WINDISPLAY: ERROR (stage=parse …)` rc=2; crosscheck `MADO_DISPLAY_CROSSCHECK: 5/5 stable fields AGREE`; harmwatch `LEDGER_SELFTEST: 55/55` + `MADO_WAVE_DONE_SELFTEST: 63/63`, both rc=0.
- **Ledger 100 → 101 by plain measurement**: rows starting with a backticked path in `quality/tool-ledger.md` are 101 at base and 102 at tip — each count includes the one literal placeholder header row `<repo-relative path>`, so real rows are **100 → 101**; the +1 is the new `tools/mado-win-display.py` row. Actual population (`ls-tree -r tools/ quality/` filtered per the ledger's definition) is 100 at base → **101** at tip. Landing receipt `population=101 ledger_rows=101 uncovered=0 … verdict=TARGET_MET` agrees.

## 3. Harm check — no axis harmed

`git diff-tree -r -p cccda4da 0c77f726 -- SCORECARD.md` is a pure **+61-line append** (one new Round-61 section); zero deleted lines anywhere in the landing means every published axis row is byte-identical to base. No score was lowered or rewritten in place. Spot reads of the claims table confirm the three declared claims target three distinct axes (calibration, coverage, operability), declared before the formal receipt runs (declaration quoted in the report appendix; predicates carried unchanged into SCORECARD).

## 4. Per-axis verdicts (closure ruling)

| axis | verdict | basis |
|---|---|---|
| calibration | **improved** | C1 verified above (append-only corrections, preservation, re-derivations) |
| coverage | **improved** | C2 verified above (all four count pairs; navigation receipt green; D03 honest) |
| operability | **improved** | C3 verified above (capability runs on my own invocation; ledger row landed same round) |
| depth | unchanged | no claim; no harm (history tables untouched) |
| freshness | unchanged | dormant rubrics stay behind open L0 questions, routed around, never answered lane-side |
| adjacency | unchanged | nothing absorbed; Shell-plane widening explicitly rejected |

## 5. Discernment spot-check (non-author)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S412 EnumDisplayMonitors (admit, tier A) | admit | live `learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaymonitors` | **agree** | all three recorded quotes are verbatim substrings of the live page (description, NULL/NULL behavior row, SM_CMONITORS note); ms.date 2018-12-05, git_commit `9267262…`, updated_at 2024-02-22 all match the row |
| S414 MONITORINFO (admit, tier A) | admit | live `learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-monitorinfo` | **agree** | rcWork sentence and `MONITORINFOF_PRIMARY: This is the primary display monitor.` verbatim on the live page; ms.date/git_commit match the row (same commit as S412, as recorded) |
| Entry `windows-display-topology-r61.md` + capability (admit) | admit | my own re-runs of the tool + receipt reads (§2 C2/C3) | **agree** | host rows re-verified by my own invocation; documented rows dated `[INF-docs]` and quote-located; capability demonstrated, not pre-claimed |
| Building a screen-capture probe (reject) | reject | `.ufo/l0-questions.md` — the r60 mado scope question is still open and unanswered; no ruling exists | **agree** | routing around an open operator question is correct; flip (operator rules the scope) is named |
| Reading the taskbar to close H19's `[UNK]` (reject) | reject | repo sweep for `Shell_TrayWnd`/`ABM_GETTASKBARPOS`/`SHAppBarMessage` | **agree** | the only hits in the lane repo are the lesson naming the surfaces out-of-scope; no lane instrument touches a Shell surface, so the widening reject is real; flip named |
| New SOURCES row quote check (S412, also S414) | — | live pages (above) | **agree** | quotes are ≤25 words, located (§ Description / § Members / behavior row), and verbatim |
| census validate | — | `bash <fleet>/scripts/sources-census.sh validate --root <fleet> mado` | rc=0, `mado ok`, 36 W04 + 1 W01 — identical warning set both ends (`census-start-r61.txt` / `census-after-r61.txt`, both committed; the r59/r60 un-tee'd disclosure is closed this round) | no new W04 — none of the six URLs was previously held, as claimed |

## 6. Trend verdicts (closure ruling)

- **expansion: improved** — new sourced entry on ground no committed entry held (knowledge 75→76, index 75→76, SOURCES 348→354, all re-measured), plus a capability row entered through a demonstrated run (ledger 100→101, re-measured).
- **quality: improved** — red/green evidence both ways (ERROR rc=2 path; crosscheck 5/5; three red selftest runs disclosed as M61-1 instead of smoothed); both carry-in defects corrected beside preserved bytes with re-derivations that I re-ran; all landing counters green at the landing (committed receipts).
- **discernment: improved** — the band owner stays `[UNK]` rather than guessed; mode-layer `[UNK]` correctly not imported (J20 pins S416's no-DPI-virtualization remark); two Shell-plane widenings rejected with named flips; four L0 questions routed around, never treated as answered; the closure's spot-check agrees with every sampled gate decision (admits and rejects).

## 7. Routed defects for the lane (next round; status-neutral)

1. **Report "Landed changes" per-file count drift (number-drift, report-only).** Actual landing numstat: `LOG.md` **+64** (reported +52), `PROVINCE.md` **+19** (reported +13), `SKILL.md` **+55** (reported +50). The totals (28 files, +1416/−0) are correct and the underlying files are correct; the drift is in the report's table only. Ironic given C1 corrects a member of this very class — correct append-only (an erratum in the round-62 report or a correction block naming the superseded table rows).
2. **Nit (no action required):** the r60 correction block names the section `-- navigation counter --` while the actual header is `-- navigation counter (SCORECARD fence, python for python3) --`. The pointer still resolves (prefix of the real header); noting for precision only.
3. **Standing (unchanged, operator-side):** the MISSION L2 dispatch floor has no surface on this host — disclosed since r57, L0 open, routed around again; never treated as answered. Correctly handled.

## 8. SHONEN observation (for the operator)

All four boxes are `[~]` self-asserted and no `[x]` was written by the lane — correct discipline (only a named non-author may write `[x]`). Boxes 2 and 3 now have non-author-executed evidence on record from this closure (the end-to-end observation chain re-run; the entry's § Verify commands executed by the closure judge), which a promotion review may cite — the write remains the promoter's act, not this file's.

## 9. Re-measured vs evidence-verified

- **Re-measured by the closure:** every C1/C2 count pair, both preservation diffs, the r59 numstat re-derivation, the ghost-name sweep, the ledger 100→101 count, census validate, and the C3 tool selftest + one live run (re-executed on this host, matching the committed receipts byte-for-byte at the verdict line).
- **Evidence-verified (lane-owned gates; committed evidence read, not executed by the closure):** the navigation counter, the used-by counter, `check-tool-ledger.py`, the display probe and crosscheck runs, and the harmwatch checker selftests — their receipts at rev-pinned `ad4e8403` / the tip were read and cross-checked against the report's numbers.
