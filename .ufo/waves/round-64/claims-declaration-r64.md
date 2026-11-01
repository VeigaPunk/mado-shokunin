# mado round-64 claims declaration (filed before the formal receipt runs; no predicate changes after scoring)

Base `7fe65562c15d20e5cfdc1da536f774149ab52b7e` (the r63 closure tip, pushed).
Axis posture at base, measured in `receipts/before-state-r64.txt`: navigation 78/78
= 10.0000, registry 371 rows, ledger 103 TARGET_MET, used-by missing=0 TARGET_MET;
carried published tables unchanged (freshness 8/8 = 10.0000; calibration resolved-active
86/86 published r56-era, not re-derivable on this host; the two omarchy-host rubrics
dormant with receipts). So no axis is distinctly lowest — the same posture as rounds 56
and 58-63; the four disposals plus the L2 floor stay the open L0 questions
(r57/r58/r59/r60 + the standing L2 line), routed around again this round, never treated
as answered. L1-only round (no dispatch surface on this host; disclosed since r57).

## C1 — calibration: the r63 carry-in repair (the closure's routed item 1)

The r63 verifier spot-check (§6.1) routed: the error-path receipt
`.ufo/waves/round-63/receipts/windisplayconfig-error-path.txt` cites its input fixture
`…receipts/broken-fixture.json`, which never landed (ephemeral). Repair, two parts:
(a) commit the fixture at the cited path — disclosed as the round-64 re-creation, not
the unknowable r63 original bytes; (b) append-only record notes (lesson Corrections +
entry) stating exactly that, and re-derive the error verdict against the committed
bytes in a new r64 receipt.

- Before: `git ls-tree <base> --name-only -- .ufo/waves/round-63/receipts/broken-fixture.json | wc -l` → **0**;
  the r63 receipt's citation names the path; no committed fixture backs it.
- After (landing): the same command → **1**; `python tools/mado-win-displayconfig.py --from-file .ufo/waves/round-63/receipts/broken-fixture.json` → `MADO_WINDISPLAYCONFIG: ERROR (stage=parse …)` rc=2 (receipt `windisplayconfig-errorpath-r64.txt`); the citation resolves to committed bytes, with the re-creation disclosure on record.

## C2 — coverage (sourced): the D05 flip-condition probe (the QDC flag matrix)

D05's named flip condition (entry Finding D05): "whether a `QDC_VIRTUAL_MODE_AWARE`
query fills the fields differently". S424 was re-opened this round (2026-11-01, page
unchanged: git_commit `39f250c3…`, updated_at 2026-05-15) and its flag table confirms
the OR-able flags QDC_VIRTUAL_MODE_AWARE 0x10 (Windows 10+) and
QDC_VIRTUAL_REFRESH_RATE_AWARE 0x40 (Windows 11+); the page's own example code is the
`QDC_ONLY_ACTIVE_PATHS | QDC_VIRTUAL_MODE_AWARE` shape. One bounded read-only probe
runs the four-shape flag matrix 0x02 / 0x12 / 0x42 / 0x52 (baseline + both virtual
flags, each alone and together), twice, byte-compared, whitelist unchanged (counts,
rationals, flags; no ids, no LUID halves, no names); the entry gains an append-only
`## Update (round 64)` with the measured rows and D05's disposition — narrowed (the
sentinel persists in every shape → residue: not query-shape-specific on this host) or
flipped (a shape returns decoded frequencies → D05 moves to measured, per its own Flip
sentence). The claim rests on S424, opened this round.

- Before: entry rows `grep -cE '^\| [HJK][0-9]{2} '` → **19**; `grep -c '^## Update (round 64)'` → **0**; probe script absent (`git ls-tree <base> -- …qdc-flagmatrix-probe.ps1 | wc -l` → 0).
- After (landing): entry rows → **19 + N** (N = the Update section's row count, pinned in the SCORECARD cell); update section **1**; probe + both run receipts + crosscheck receipt committed.

## C3 — operability (capability acquisition): `tools/mado-receipt-citecheck.py`

The r63 closure routed the ephemeral-fixture citation as a manual find; this
generalizes the class into a durable instrument: a read-only checker that extracts
repo-relative path citations from named receipt/text artifacts and verifies each
resolves in the git tree at `--rev` (one `git ls-tree -r --name-only` child per run;
strict path grammar; unresolved paths named, never silently skipped; `--selftest`
hermetic on private temp fixtures, spawns nothing). Scan scope is caller-named paths —
the checker never walks r56-era material (the security boundary's affected blobs stay
untouched).

- Before: `git ls-tree <base> --name-only tools/ | grep -c citecheck` → **0**; `python quality/check-tool-ledger.py --repo . --rev <base>` → **population=103**.
- After (landing): citecheck present; `--selftest` → `MADO_CITECHECK_SELFTEST: N/N assertions passed` rc=0; a run over the r63+r64 receipt trees → `MADO_CITECHECK: … verdict=TARGET_MET` after C1's fixture lands (the red state before C1 is recorded in the work-window receipt as the demonstration that the checker catches the routed class); ledger → **population=104**; the capability row enters the SCORECARD table this round.

## Causally separable

C1 verifies alone (fixture + re-derived receipt). C2 verifies alone (probe + entry
rows; rests on S424's re-open, not on C1/C3). C3 verifies alone (selftest + its own
work-window red/green demonstration on a synthetic tree; the joint r63-receipts scan
is a bonus, not its evidence base).
