author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

# mado round 60 — verifier spot-check (non-author closure)

Closed against lane tip `252bf383a224974e3b06b06f41755bcd1226d828` (branch `master`, pushed),
landing `edc2d378ba38ec760e8f964dc31be1f1e421f134`, base `d1e64880b375529de185f49e124dd6cc42c58e75`.
Every command below was run by this verifier on 2026-11-01 UTC against committed bytes
(`git show <rev>:<path>` / `git diff-tree` / `git ls-tree` / `git merge-base --is-ancestor`).
Security boundary held on the verifier side too: no r56-era credential material was opened or
surfaced; only counts/shapes recorded.

## 1. Step-1 conformance — PASS

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git -C <fleet root> log --format='%an <%ae> %H' -1 -- .ufo/reports/round-60/mado.md` | `mado-shokunin <mado@shokunin.local> 909ebb99970f719d2d432ce2813689168f84f132` |
| committed report bytes = filed bytes | `diff <(git show 909ebb99:.ufo/reports/round-60/mado.md) .ufo/reports/round-60/mado.md` | identical |
| `SHONEN` heading | read of report | `## SHONEN` present, one `[~]` line per box with pointers |
| cited commits exist + ancestor | `git merge-base --is-ancestor <h> refs/heads/master` for 252bf383a224, edc2d378, 6f2e4115, 25294ab3, 3eb5f5ee, d1e64880b375 | all ANCESTOR |
| branch tip pushed | `git ls-remote origin refs/heads/master` vs local `rev-parse refs/heads/master` | both `252bf383a224974e3b06b06f41755bcd1226d828` |
| round work in range | `git log --format='%H %an' d1e64880b375..252bf383a224` | exactly 2 commits, both authored `mado-shokunin` |
| dispatch digest | grep `.ufo/watchdog.log` | lines 87/106 match the contract digest verbatim (launch 22:59:04-07:00, complete 23:55:45-07:00 head=252bf383a224 pushed=True) |
| L0 line durable | `git show HEAD:.ufo/l0-questions.md \| grep -c 'mado \| round-60'` | 1 (committed in 909ebb99 with the report) |

## 2. Claim re-checks

Re-measured = this verifier ran the measurement; evidence-verified = lane-owned
gate/selftest verified through its committed rc-owned, revision-pinned evidence (per the gate
standard, a sibling's gate is not executed).

### C1 calibration (carry-in corrections) — re-measured, VERIFIES

- Anchored counts, base → landing:
  `git show d1e64880b375:SCORECARD.md | grep -c '^### Corrections (round 60)'` → **0**;
  at `edc2d378` → **1**. `LOG.md` `^## Round 60` → **0 → 1**. `SKILL.md` `^## Round 60` → **0 → 1**.
- Preservation: `git diff-tree -r --numstat d1e64880b375 edc2d378 -- SCORECARD.md LOG.md SKILL.md`
  → `82 0` / `67 0` / `50 0` — **0 deleted lines in each** (matches the report's +82/+67/+50, insertions only).
- Measured numbers re-derived:
  `git diff-tree -r --numstat 6f2e4115 25294ab3 -- corpus/knowledge/windows-desktop-plane-r57.md corpus/knowledge/windows-permonitor-dpi-r58.md`
  → `17 0` and `5 0` — exactly the corrected per-file figures.
- Mistake count: `grep -c '^- \*\*M59-' corpus/lessons/round-59.md` → **4** (the LOG/SKILL "M59-1..M59-3" lines are wrong as written; corrections appended, original bytes preserved — original defect lines still present at LOG line 2702 and in SKILL § 59; unanchored counts at landing include the corrections' own quotations, exactly as the report disclosed).

### C2 coverage, sourced — re-measured, VERIFIES

- Denominators: knowledge files `git ls-tree` count **74 → 75**; README index rows
  `grep -cE '^\| `+backtick+`knowledge/[^`]+\.md`'` **74 → 75**; SOURCES rows
  `grep -cE '^[[:space:]]*\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` **342 → 348**;
  entry rows `grep -cE '^\| [HJK][0-9]{2} '` → **15** (H=4, K=7, J=4).
- Navigation counter (SCORECARD § Counting command fence, `python` for `python3` as disclosed)
  re-run at `REV=edc2d378`: `indexed=75/75 missing=0 dangling=0 duplicates=0
  coverage=10.0000/10`, exit 0. Reproduced the receipt.
- Probe re-run by this verifier:
  `powershell.exe -NoProfile -NonInteractive -NoLogo -ExecutionPolicy Bypass -File
  .ufo/waves/round-60/receipts/dpi-awareness-probe.ps1` → rc=0, output **byte-identical** to
  committed `dpi-awareness-run1.txt`; committed run1 and run2 are byte-identical. H13-H16
  observed first-hand (`thread.awareness=0`, 1920x1080 = ForDpi-96, 6 × PER_MONITOR_AWARE,
  fg dpi 96 / awareness 2).
- **S404-table join (J14)**: the S404 row's `used-by` cell was extended in place — the whole
  26-file landing diff has exactly **1 deleted line**, and it is this cell move (old ending
  `…windows-desktop-plane-r57.md |`, new appending
  `, corpus/knowledge/windows-dpi-awareness-metrics-r60.md, corpus/lessons/round-60.md |`);
  old→new logged in the lesson per the SOURCES contract. H16 (fg dpi 96, window awareness 2)
  read against S404's return table (PER_MONITOR_AWARE → "The DPI of the monitor where the
  window is located") is an agreement, and the r58 process context stays `[UNK]` (same-shape
  pin disclosed in J14; the r58 entry is not in the changed-file set — bytes untouched).
- **Named vacuous join (J13)**: the entry states the metrics equality at effective 96 "cannot
  identify the branch; the branch is identified by the measured awareness value (H13), never
  by the metrics equality" — the r58 J05/J07 residues close for the launch shape with the
  vacuous shape named rather than read as identification. Correct.
- Sources: S406, S407, S410 quotes re-opened at their URLs — all three verbatim substrings of
  the page bodies (S406 "Note that all dimensions retrieved by GetSystemMetrics are in
  pixels.", § Description; S407 "This function returns the same result as GetSystemMetrics
  but scales it according to an arbitrary DPI you provide if appropriate.", § Remarks; S410
  "DPI unaware. This process does not scale for DPI changes and is always assumed to have a
  scale factor of 100% (96 DPI).", § Constants) with ms.date 2018-12-05 and git_commit
  `fa53641576e3603fa7b66d3a4ad969d3ce49d6f3` (S410: `9267262487657894a8af112d7165006fed5035a7`,
  updated_at 2024-02-22) matching the rows and the lesson's Gate table. All ≤25 words.
- Used-by counter: evidence-verified — `usedby-before-r60.txt` (base: entries=74 rows=342
  missing=0 TARGET_MET, `USEDBY_BASE_RC=0`) and the landing run inside
  `landing-counters-r60.txt` (entries=75 rows=348 missing=0 TARGET_MET, `USEDBY_LANDING_RC=0`,
  rev-pinned).

### C3 operability, capability acquisition — re-measured, VERIFIES

- `git ls-tree d1e64880b375 --name-only tools/ | grep -c win-dpi` → **0**; at `edc2d378` → **1**.
- Safety review of the tool's committed bytes before running: every P/Invoke is a getter
  (no `Set*` verb, no Shcore), live mode spawns exactly one PowerShell child with a fixed
  embedded script, stdin DEVNULL, stdout parsed as JSON and re-printed through a whitelist,
  parse failure prints byte length + sha256 prefix never the bytes, no file writes, no
  sockets. Read-only observer — safe to run.
- Offline selftest re-run by this verifier: `python tools/mado-win-dpi.py --selftest` →
  `MADO_WINDPI_SELFTEST: 10/10 assertions passed`, **rc=0**.
- Live receipt re-run once by this verifier: `MADO_WINDPI: CLEAN (awareness=unaware
  metrics=1920x1080 dpi96=1920x1080 windows=6 fg_dpi=96)`, **rc=0**, output **byte-identical**
  to both committed receipts (`windpi-live-run1.txt` = `windpi-live-run2.txt` = my run).
- `--from-file .ufo/waves/round-60/receipts/windpi-snapshot.json` → rc=0, re-derives.
- Malformed snapshot (fresh fixture in verifier scratch) → `MADO_WINDPI: ERROR (stage=parse …)`,
  **rc=2**, raw bytes never echoed.
- Crosscheck receipt `windpi-crosscheck.txt`: 5/5 stable fields AGREE (read).
- Tool ledger: evidence-verified — `landing-counters-r60.txt`
  (`LEDGER: population=100 ledger_rows=100 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0
  verdict=TARGET_MET`, `LEDGER_LANDING_RC=0`, rev-pinned) + base receipt population=99/99
  TARGET_MET + checker selftest tally in `harmwatch-selftests-r60.txt`
  (`LEDGER_SELFTEST: 55/55`, rc 0). Plain corroboration: the ledger table gained exactly
  **+1 row** in the diff, and the new row describes `tools/mado-win-dpi.py`.
- PROVINCE round-60 refinement (+18/−0, append-only) read against the tool's actual bytes —
  accurate (one fixed child, whitelisted output, no Set* verb, operator-owned awareness
  changes stay outside).

### M60-3 (heredoc truncation caught and restored byte-exact) — re-measured, VERIFIES

- Restoration: `git show edc2d378:SCORECARD.md | head -3057 | diff - <(git show
  d1e64880b375:SCORECARD.md)` → **empty; ORIGINAL_PRESERVED reproduced** (base is 3057 lines;
  landing 3139 = +82, all appended).
- Anchored-count catch: all four anchored greps the lesson names count exactly **1** at the
  landing (`^### Corrections (round 60)`, `^### Capabilities (round 60)`, `^### Planned
  (round 61`, `^## Round 60`) — a mid-file truncation would zero at least the last three.
  The lesson's fix (large appends via written files; anchored section-count greps after every
  append) is recorded.

## 3. Per-axis verdicts (this verifier's ruling)

| axis | verdict | basis |
|---|---|---|
| coverage | **improved** | C2 re-measured: 74→75 sourced entries on previously-uncovered ground (the DPI-awareness layer), index 74→75 at 75/75 reachable exit 0, registry 342→348, S406-S411 quotes verified |
| operability | **improved** | C3 re-measured: new durable read-only tool, selftest 10/10, live byte-identical, fail-closed ERROR rc=2, from-file roundtrip; PROVINCE/ledger/row landed in the same round |
| calibration | **improved** | C1 re-measured: drift corrected with measured numbers + re-derivation commands beside preserved defect lines; 0 deleted lines in SCORECARD/LOG/SKILL |
| freshness | unchanged | no claim; harm watch green (navigation/used-by/ledger/census at landing) |
| depth | unchanged | unscored, no bounded rubric; nothing harmed |
| adjacency | unchanged | nothing absorbed; third-party content untouched; cross-domain evidence reported, not absorbed |

No owned axis harmed: SCORECARD diff is append-only (82/0), every existing row's bytes
untouched; `tools/mado-verify.sh` not in the changed set (grep count 0); both fail-closed
checkers' selftests receipted green (55/55, 63/63); census validate re-run by this verifier →
exit 0, warning set 36 W04 + 1 W01 (same as receipt).

## 4. Discernment spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S406/S407/S410 admitted as tier-A `mined` rows | admit | the three live URLs (fetch 2026-11-01) | **agree** | quotes verbatim ≤25 words; ms.date/git_commit metadata in the rows matches the pages exactly; opened-before-written discipline recorded in the lesson's Gate table |
| Entry `windows-dpi-awareness-metrics-r60.md` + J13/J14 admitted | admit | entry bytes + my probe/tool re-runs | **agree** | every H row re-derived rc=0; the vacuous join is named instead of read as identification; the `[UNK]` is preserved, not overwritten |
| Screen-capture probe rejected this round | reject (decision upheld) | `corpus/lessons/round-59.md` route lines 211-215 + `.ufo/l0-questions.md` line 240 | **agree** | the r59 route is explicitly conditional ("if the operator rules screen capture read-only in scope"); no ruling exists; the L0 question was filed and committed (909ebb99) instead of self-authorizing — flip condition named |
| Editing the r58 entry's `[UNK]` in place rejected | reject (decision upheld) | `git diff-tree --name-only d1e64880b375 edc2d378` | **agree** | the r58 entry is not in the changed set; closure lives in the r60 entry § 4 as a same-shape pin — append-only discipline held |
| Treating the three dormant-rubric L0 questions as answerable rejected | reject (decision upheld) | `.ufo/l0-questions.md` r58/r59 mado lines | **agree** | all three disposals remain the operator's; SCORECARD posture names them as routed-around, never answered |
| `sources-census.sh validate --root <fleet root> mado` | (duty run) | script re-run | exit **0**; 36 W04 + 1 W01, final `mado ok` — matches `census-after-r60.txt` | warning set unchanged; no new W04 for S406-S411 |

## 5. Trend verdicts (this verifier's ruling)

- **expansion: improved** — new sourced entry on uncovered ground (knowledge 74→75, index
  74→75 at 75/75 reachable exit 0, registry 342→348), plus a capability row entered through a
  demonstrated run. All re-measured.
- **quality: improved** — the capability lands with named red/green assertions and evidence
  both ways (ERROR path rc=2, crosscheck 5/5); records corrected to observed state with defect
  lines preserved; no admitted entry failed a re-check (navigation re-run green; used-by,
  ledger, census evidence-verified green at the landing).
- **discernment: improved** — corrections carry re-derivations beside preserved defect lines;
  the vacuous join named (J13) and the `[UNK]` kept (J14); screen-capture scope went to L0
  instead of self-authorization; three mistakes mined including a recurrence of M58-4 (M60-2)
  caught by its own self-contradicting receipt and a landing defect (M60-3) caught by anchored
  counts. This verifier's spot-check agrees with the gate on the sampled admits and rejects.

## 6. Routed defects for round 61 (status-neutral; fix append-only)

1. **Pointer-resolution defect (lesson Census).** `corpus/lessons/round-60.md` § Census names
   three receipt files — `navigation-landing-r60.txt`, `usedby-after-r60.txt`,
   `ledger-landing-r60.txt` — that do not exist under those names anywhere in the repo. The
   landing runs they describe live inside `.ufo/waves/round-60/receipts/landing-counters-r60.txt`
   (sections `-- navigation counter --`, `-- used-by counter --`, `-- tool ledger production --`);
   the base used-by run is `usedby-before-r60.txt`. The evidence standard requires pointers to
   resolve at closure. Fix next round: append a correction line (lesson or LOG) naming the
   three supersedings; do not rewrite the filed bytes.
2. **Same-class sweep incompleteness (the C1 class, one mention left standing).**
   `corpus/lessons/round-59.md` line 74 still reads "(diff shape +4/−0 each, checked at commit
   time in the report)" — the same number-shape drift C1 corrected in SCORECARD/LOG/SKILL (the
   r58 entry's landing was +5/−0, its trio is 5 lines; the r57 entry's landing was +17/−0
   including the errata append). The round's own `before-state-r60.txt` counted this
   occurrence (1) but no correction or named disposition landed for it. Fix next round: append
   a correction to the r59 lesson (the corrections-block precedent exists — r59 appended one to
   the r58 lesson), citing the same `git diff-tree -r --numstat 6f2e4115 25294ab3` re-derivation.

## 7. Notes for the operator

- SHONEN boxes all remain `[~]` (self-asserted). From this round's observations, **box 1**
  (SKILL decision tables/rules; § Round 60 verified against the tool's actual bytes) and
  **box 4** (PROVINCE round-60 refinement verified accurate; the diff absorbs nothing from
  other lanes) look checkable by a competent non-author reviewer. **Boxes 2–3** rest on
  historical assertions (`config-health-report-r3.md`/VER-M3,
  `executor-test-sufficiency.md`/MADO-R3-4) that a reviewing session must re-open, and the
  outside-lane verifier-independence gap the lane names is real. This verifier wrote no `[x]`
  (closure contract forbids it).
- The census start run was not tee'd (disclosed in the lesson, same as r59) — disclosed
  continuation, not a new defect.
- The report's landing-diff claims (26 files, +1200/−1; receipts 16 files at `edc2d378`;
  insertions-only in SCORECARD/LOG/SKILL/PROVINCE) all re-derived exactly.

## 8. Closure ruling

All three declared claims verify (C1/C2/C3 re-measured; used-by and ledger checkers
evidence-verified per the gate standard). No axis is harmed. Conformance defects found
(§ 6) are status-neutral and routed. **mado round 60: admitted** (`lanes.mado = ok`).
