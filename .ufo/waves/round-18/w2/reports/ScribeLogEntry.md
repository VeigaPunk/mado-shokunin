# ScribeLogEntry — round-18 LOG entry draft (wave 2, scribe)

Behavior: drafted the round-18 LOG.md entry in the round-17 entry's structure
(trigger, C1-C3 with measured before→after, gate fix, routed fixes, harm watch,
waves, not-applied drafts, capabilities table, planned). Every number was read
from committed evidence or from `git show` of committed bytes; none was
invented. The entry is not appended to LOG.md (per assignment).

Touched surfaces: only `.ufo/waves/round-18/drafts/ScribeLogEntry.md` (new) and
this report. No git or jj write, no package-manager, service, compositor, input,
screenshot or REA/browser command, no selftest/regression/tripwire run, no
fetch, no tool installed or updated (none needed).

## Commands run (read-only)

- `tail`/`grep` of `LOG.md` (round-17 entry at lines 1255-1285), `SCORECARD.md`
  tail, `corpus/lessons/round-18.md`, `corpus/SOURCES.md` rows S072-S095,
  `corpus/QUALITY.md` criteria 24, `SKILL.md` line 566 (registry row),
  `.gitignore` at `4c103b5`.
- `git log`/`git show --stat` of `d3a0000`, `4c103b5`, `abfbf35` (read only).
- `git show <rev>:tools/mado-verify.sh | sha256sum` at `d9a5a18`, `4c103b5`,
  `abfbf35`: `fba82a66…`, `c9fb0cef…`, `c9fb0cef…`.
- `git ls-tree -r --name-only abfbf35 -- .ufo/waves/round-18/fetch` and
  `git show` of each `receipts.jsonl` at `abfbf35`: 21 files, 301
  `mado-fetch-receipt-v1` lines; status set {200, 404}.
- Python (read-only) exact-URL match of the committed receipts against each
  S072-S095 row: 21 URL rows each have ≥1 receipt with status 200; S090, S091,
  S095 have no URL and no receipt; five 404 receipts are for URLs that are not
  any S072-S095 row's URL.
- Python (read-only) read of `evidence/measure-mutants.json`,
  `evidence/recut-summary.json`, `w1/dispatch.json`, `w2/dispatch.json`.
- `grep`/`cat` of `evidence/*.txt` headers and summary lines (listed in the entry).

## Findings

1. **Provenance gap on the regression receipt (QUALITY 24 would fail on it).**
   `evidence/regression-recut.txt` prints `REGRESSION_TOOL:
   tools/mado-verify.sh sha256=2bdf5e8a…` and has no `RECEIPT … tool_sha256=…
   measured_commit=…` line. The committed gate at `4c103b5` and `abfbf35` is
   `c9fb0cef…` (`git show | sha256sum`), the same sha as `gate-selftest.txt` and
   the harm-watch pin. `gate-rc-redbefore.txt` also records `2bdf5e8a…` as the
   "working tree at the time of this run". The derived target hash
   (`20714096…`) matches the pin in both states, but no committed receipt binds
   the 10/10 regression to the committed bytes. The draft discloses this rather
   than claiming it closed. Suggested fix for L1: re-run the regression against
   `c9fb0cef…` (only if L1 authorises it), or cite the caveat verbatim.
   Not run by this scribe.

2. **Live fetch tree is drifting; committed counts differ.** The working tree
   now holds 26 `receipts.jsonl` files / 309 lines, including
   `ReviewWalkerUpstream`, `ReviewThemeUpstream`, `ReopenS077` and `ReopenS088`,
   written by live wave-2 seats and not committed. The draft cites only the
   committed `abfbf35` counts (21 files / 301 lines). The live
   `ReopenS077`/`ReopenS088` directories hold body and `.commit` files but no
   `receipts.jsonl`; the committed receipts covering their URLs are 200
   (`theme/mod.rs` via `MadoR18.SrcWalkerThemes`; `omarchy-refresh-walker` via
   `NoteWalker`).

3. **Rubric V credits host rows as documentary coverage.** S090 and S091
   (pacman.log, walker host bytes) and S095 (P5 host theme state) carry no fetch
   receipt and are counted in `sources_ok` for P3/P5. The draft states this
   explicitly; a non-author reader should weigh P3/P5 as partly host-byte
   evidence.

4. **Wave-2 outcome is not in the evidence.** `w2/reports/` contains only the
   registry at drafting time; `w2/dispatch.json` records 73 spawn items. The
   draft carries one `[PENDING: L1 wave-2 integration outcome …]` marker that
   L1 must replace before appending to LOG.md. No wave-2 count is asserted.

5. **Stale placeholder draft.** `drafts/ScoreResultsDraft.md` is a skeleton with
   `[PENDING: …]` values and points at `.ufo/waves/round-18/frozen-tripwire`,
   which does not exist (the frozen snapshot is `.ufo/waves/round-18/frozen`).
   Not copied into the LOG entry; L1 should not reuse it as-is.

6. **Pacman join is a file read, not a re-derivation.** `tripwire-pacmanlog-join.txt`
   records the awk command and 4/5 joins; the entry cites it as evidence of
   that join only. R15-V1 stays `[UNK]`.

7. **Freshness not claimed.** No round-18 receipt re-anchors the pins moved by
   the 2026-10-20 `-Syu`; the entry states this.

## Output checks (for L1)

- Entry numbers traceable: C1 15/23 → 18/26 (`measure-before/after.json.txt`);
  C2 4/6 → 6/6 (same, `c2`); C3 frozen 17/17, match exit 0, tamper exit 2, d9a5a18
  usage exit 2; mutants 6/6 bite; harm watch PASS (10 commands); census exit 0;
  nav 34/34; U 7/7; selftest 389/389; action-plan 52/52.
- Not applied to any file: the draft is not LOG.md. L1 owns the append and the
  wave-2 placeholder.

## Checks the main agent should run

- `python3 .ufo/waves/round-17/measure.py 4c103b55b1ea5c3c555884afe3eb69b5189701b7`
  (expect c1 18/26, c2 6/6) before appending the entry.
- `python3 -I .ufo/waves/round-18/receipt-check.py` (expected red on finding 1
  if the regression receipt is cited).
