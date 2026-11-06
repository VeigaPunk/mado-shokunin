# R91MReviewC2 — C2 candidate review + D1 selftest design (round 91, w1)

Status: **DRAFT** — every run below is a draft run at base `cc0381db585cc44c3dfc13ced807409c32c45bb0`
(= lane HEAD when reviewed; `git rev-parse HEAD` verified). No measurement is claimed; no file under
`.ufo/waves/round-91/receipts/` was written.

Reviewed bytes: `.ufo/waves/round-91/build/check-seat-reports.c2.py`
sha256 `2e0f082e36caee7090339665e3a7fb3c1c7954692cc66e67aa9df0510a3d916c`, 259 lines,
mtime 2026-11-06 21:11:36 -0300. **The candidate changed mid-review**: my first read saw an earlier
revision (ls-tree pathspec `-- .ufo/waves`, cat-file fallback in `size()`, no mode-120000 filter).
Everything below is re-run against the pinned current bytes; if it changes again before the freeze,
re-run (`--all`, `--selftest`) and re-pin.

Lane `PROTOCOL.md` does not exist; the governing standard read is the fleet
`/home/vgpnk/Projects/shokunin/PROTOCOL.md` §Gate standard (lines 375-413).

## 1. Protocol / gate-standard review (item 1)

Verified conformance (each item exercised, command and rc listed in §2/§5):

| Standard point | Result |
|---|---|
| Verdict codes 0=OK, 1=failed, 2=setup, all declared in docstring | PASS — all three observed (0, 1, 2×5 distinct setup messages) |
| Finding ids stable (SR01-SR04) + fixed summary format | PASS — ids are literal prefixes; `--round`+`--all` exclusivity rc2; no-selector rc2 |
| `--selftest` asserts rc AND finding ids | PASS — `case()` asserts `rc == want_rc and ids == want_ids` and that the last line is the summary; 10/10 green, rc0 (run with TMPDIR in scratch) |
| Read-only in `--rev` mode | PASS — fixture: report deleted from worktree still found at `--rev HEAD` (reads committed tree); `git status --porcelain` byte-identical before/after in both modes; no write path outside selftest tempdirs |
| Symlinks | PASS (current bytes) — mode 120000 excluded in `--rev` (`ls-tree` filter, candidate line 69), `os.path.islink` excluded in `--worktree`; consistent both modes. Dangling and live symlinks both → SR01 in both modes (fixtures `fx-sym-dangling`, `fx-sym-live`). Lane census: 64 symlinks at cc0381db, all under `.ufo/waves/`, **all** fixture/tripwire trees (rounds 17-56), zero are trailer targets → no lane verdict affected |
| Huge dispatches | PASS — synthetic 20000-seat dispatch: 0.1 s in both modes, `seats=20000` correct; 500-missing rev scan <0.1 s (full-tree size cache, no per-miss subprocess since the mid-review change); lane `--all` (35582 blobs) 0.25 s |
| Non-UTF-8 | PASS — invalid bytes in a dispatch → rc2 `SETUP_ERROR … not a dispatch (taskCall.tasks)` in both modes; non-UTF-8 bytes in a report file → present (content never decoded) |
| Trailer path with spaces | See F4 (info) — never parses as a trailer; seat reads `SR04 untrailed`, rc stays 0 |

### Findings by severity

**F1 (medium) — SR01 conflates "no report anywhere" with "report written off-trailer".**
Of the 133 SR01s at cc0381db, **71** have a same-basename file elsewhere in the tree and **32 of
those have the report exactly at `<wave>/<seat>/<seat>.md`**: round-49 ×1, round-65 ×3, round-72 ×8,
round-73 ×9, round-74 ×11 (e.g. trailer `.ufo/waves/round-65/w1/R65ExecC1Counter.md` missing while
`.ufo/waves/round-65/w1/R65ExecC1Counter/R65ExecC1Counter.md` exists — 10997 bytes, real report;
same for R72ExecC1 12461 B, R74Sentinel 9534 B, ExecSessionTriage 19236 B). The remaining 39
near-misses are same-basename files belonging to *other* rounds (not false positives; e.g. round-42's
36 seats have their stems in rounds 43-45 — different rounds' reports; round 42's own wave dir holds
none of its 36 reports — wholesale loss, correctly flagged).
**Is the gate's rule the right one? Yes.** The trailer names the canonical resolver path; a report at
`<seat>/<seat>.md` violates the contract and, unchecked, teaches seats that any nearby path counts.
Verdicts (rc, counts) are correct as-is. Recommendation: keep SR01 fatal and strict, and optionally add
a non-fatal `SR05 offtrailer <round>/<wave> <seat> <found-at>` (checked only when `dir/name/name.md`
exists) so M90-4-style total loss (round 90: truly nothing anywhere) stays distinguishable from
misplaced-but-retained in triage. L1 note: the frozen expectation set must expect SR01 for rounds
72-74's subdir cases (they are missing *as written*, which is the contract the counter freezes).

**F2 (low) — `--selftest` never exercises `--rev`/GitTree mode.** Every selftest case calls
`run(d, None, True, rounds)` (worktree hard-wired). The rev-mode path — full-tree ls-tree parse, the
120000 exclusion, the size cache — has zero selftest coverage; a regression there (e.g. re-adding the
old pathspec + fallback, or dropping the symlink filter so rev/worktree diverge again) passes selftest.
Fix: two rev cases in `selftest()` — `git init` a temp repo (throwaway identity), commit a fixture
dispatch+report, assert rc+ids (my `fx-sym-*` / `fx-outside-waves` fixtures are the recipes).

**F3 (low) — worktree/`--all` on a directory with no `.ufo/waves` returns OK rc0** (`rounds=0 …
verdict=OK`, verified on an empty scratch dir), while any named `--round` on the same dir is rc2. A
run against a wrong/empty directory reads as a clean pass. Mitigated because PRED-C2 pins exact
expectation sets, but the bare gate could require ≥1 dispatch in worktree mode, or the counter should
pin `rounds=` for its worktree cases.

**F4 (info) — trailer paths with spaces are unrepresentable.** TRAILER/PLAIN both require a single
`\S+` token, so an assigned path containing a space yields `SR04 untrailed` (non-fatal) even when the
seat wrote the file (fixture: `A B.md`/`C D.md` existing → `SR04 untrailed round-7/w1 A`, `… B`, rc0).
Fleet dispatch convention uses single-token paths, so no lane impact today; document the constraint
(or support quoted paths) before any wave context ever names a spaced path.

**F5 (info) — mid-review candidate change.** The earlier bytes' per-miss `cat-file` fallback and
`-- .ufo/waves` pathspec are gone; symlink policy is now consistent across modes. Net effect on my
findings: the old asymmetry I initially observed (rev counted a symlink blob's target-string length as
a present report) is fixed in the current bytes. Whoever last edits the candidate before the freeze
must re-pin sha256 in the frozen evidence; the counter should verify the target digest it measures.

**F6 (info) — misc verified behaviours, no action.** Directory as trailer path → SR01 both modes;
report outside `.ufo/waves` → found (full-tree cache); rendered trailer wins over a later plain
`Report:` line and last rendered line wins (matches docstring); nested `w1/w1-dispatch.json` is not a
dispatch (named round → rc2); `taskCall.tasks` not a list → rc2; non-string task body → `SR04`; empty
tasks list → OK `seats=0`.

## 2. DRAFT runs (item 2)

All at `--repo <lane> --rev cc0381db`, DRAFT-labelled, exit codes observed:

- `--all` → `rounds=46 waves=61 seats=1732 trailered=1732 present=1599 missing=133 empty=0 unsafe=0
  verdict=MISSING`, rc=1, wall 0.25 s. **Reproduces the declaration's draft numbers exactly.**
- Per round (rc after each): 39 → 4 SR01, rc1; 42 → 36 SR01 (present=0), rc1; 71 → 11 SR01, rc1;
  83 → 3 SR01, rc1; 86/87/88/89 → OK rc0 (14/12/16/16 seats); 90 → 2 SR01
  (R90MScoutSources, R90MScoutCases — exactly the M90-4 seats), rc1.
- `--selftest` → `SEAT_REPORTS_SELFTEST: checks=10 failed=0`, rc0.
- Setup errors: `--round 91` (no dispatch) rc2; `--rev deadbeef` rc2 `not a commit`; no selector rc2;
  `--round`+`--all` rc2; rev mode on non-repo rc2; worktree on empty dir `--all` rc0 / `--round 7` rc2.

**Spot-check (10 SR01s, `git cat-file -e cc0381db:<path>`):** all 10 ABSENT, rc=128 each —
round-39 ExecAssimAppendBlock, round-42 ExecIndepA, round-48/a4r1 MadoA4RevGate, round-55
R55ScoutCallers, round-65 R65ExecC1Counter, round-71 R71ScoutSources, round-74 R74Sentinel, round-81
R81Sentinel, round-83 R83ScoutSource, round-90 R90MScoutSources. False positives among the ten: only
the round-65/round-74 off-trailer class (see F1); round-39/55 neighbours found are different seats;
round 90 has no same-basename file anywhere (genuine M90-4 loss). See F1 for the full-population
71/133 near-miss quantification.

## 3. D1 — minimal selftest for `quality/check-receipt-presence.py` (item 3)

Routed defect reproduced today (DRAFT): `--selftest` → argparse rc2,
`check-receipt-presence.py: error: unrecognized arguments: --selftest`.

Minimal fixture set (three throwaway `git init` repos, throwaway identity; all DRAFT-verified by
running the real checker on them — outputs below are its actual bytes):

- **FX-OK**: base commit `round-88: base` with `LOG.md` = `# LOG\n- round 88: base.\n`; then
  `LOG.md` → `# LOG\n- round 88: base.\n- round 89: cites receipts/ghost-r89.txt.\n` plus
  `.ufo/waves/round-89/receipts/ghost-r89.txt` = `seat report copy\n`; commit `round-89: lands ghost
  receipt`. Run `--rev HEAD`. Assert rc **0** and exactly one stdout line matching
  `RECEIPT_PRESENCE: mode=rev rev=<40-hex> records=1 cited=1 present=1 missing=0 verdict=OK`
  (assert prefix + suffix; sha is fixture-dependent).
- **FX-MISSING**: FX-OK without the receipt file. Run `--rev HEAD`. Assert rc **1** and exactly:
  `missing receipts/ghost-r89.txt -> .ufo/waves/round-89/receipts/ghost-r89.txt LOG.md:3`
  `RECEIPT_PRESENCE: mode=rev rev=<40-hex> records=1 cited=1 present=0 missing=1 verdict=MISSING`
  (the finding line doubles as the stable "finding id": cite, resolved path, file:line all pinned).
- **FX-RC2** (two cheap cases): plain non-git dir `--rev HEAD` → rc2 +
  `RECEIPT_PRESENCE: SETUP_ERROR not a git repository: <path>`; repo at base with `--rev deadbeef`
  → rc2 + `RECEIPT_PRESENCE: SETUP_ERROR bad --rev deadbeef`.
- Optional 4th (worktree mode, since the registry row will advertise both): FX-OK with the `LOG.md`
  edit left **uncommitted**, run `--worktree --base <base-sha> --commit-path LOG.md` → same OK
  summary with `mode=worktree rev=<base-sha>`. Pitfall found while probing: with the change already
  committed and `--base HEAD`, cited=0 and the case vacuously passes — the worktree fixture must keep
  the edit uncommitted for `cited=1` to be asserted.

## 4. Residual risk / verification gaps

- JSON parser fuzzed only with the shapes listed in F6 (no giant single strings, no duplicate keys,
  no deep nesting).
- The frozen expectation set (`controls/seat-reports-set-r91.json`) is another seat's work; not
  cross-checked here. If it labels rounds 72-74, it must expect the subdir cases as SR01 (F1).
- I did not audit whether any of the 39 "same-basename elsewhere" files is a round's report renamed
  across rounds (they name other rounds' dispatches; treated as other rounds' reports).
- Candidate bytes may change again during w1; results are pinned to sha256 `2e0f082e…` (mtime
  2026-11-06 21:11:36 -0300). Re-run `--all` + `--selftest` on the final bytes before the freeze.

## 5. Evidence index (commands, all DRAFT)

- `python3 …/check-seat-reports.c2.py --selftest` → rc0 (also rc0 with TMPDIR in scratch).
- `python3 …/check-seat-reports.c2.py --repo <lane> --rev cc0381db --all` → rc1 (twice: pre-change
  bytes and pinned bytes; identical summary).
- `… --round {39,42,71,83,86,87,88,89,90}` → rc per §2.
- `git -C <lane> cat-file -e cc0381db:<path>` ×10 → rc128 ×10.
- `git -C <lane> ls-tree -r cc0381db` → 35582 blobs, 64 mode-120000 (all under .ufo/waves, none a
  trailer target).
- Edge fixtures (scratch `/fast/scratch/hyaku/mado-r91/R91MReviewC2`, deleted after this report):
  24 checks, 0 failed — symlinks (dangling/live × rev/worktree), non-UTF-8 dispatch/report, spaced
  trailers, 20000-seat dispatch, 500-missing scan, dir-trailer, outside-waves report, nested dispatch,
  tasks-not-list, body-not-str, plain-vs-rendered precedence, two waves, empty tasks, rev-reads-tree +
  read-only proof.
- D1 probe (scratch, deleted): FX-OK rc0, FX-MISSING rc1 (exact lines above), FX-RC2 ×2 rc2,
  worktree bonus, `--selftest` rc2 argparse.

Installs: none (python3 3.14 + system git sufficient).
