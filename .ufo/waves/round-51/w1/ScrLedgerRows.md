# ScrLedgerRows — C1 tool-ledger row prose and pointer provenance (round 51 w1)

Leaf seat (`ScrLedgerRows`). Lane `mado-shokunin`. Measured revision: lane tip
`3ac316426497e8649bffedc88d28241d9bc71c52`; round base `6ca8c559a4a3d6d361101592116eea2bc7452437`.
Nothing outside this seat's directory and this report was written; no tracked file was edited; all git
use was read-only. No tool was installed (nothing was needed).

## Verdict / behaviour

The seat produced the full row set the C1 ledger needs: **79 rows, one per population file**, each with a
≤17-word factual description taken from the file's own docstring/header, an accountability class, and a
pointer to an existing tracked file plus a line number **verified to contain the file's basename**. This
is prose and provenance only — it is **not** `quality/tool-ledger.md`, not the C1 checker, and not a C1
verdict. Nothing here asserts that PRED-C1-r51 passes.

Population, measured at the tip (`git ls-tree -r --name-only <rev> tools/ quality/` filtered to
`tools/**`, immediate `quality/*.py`, immediate `quality/counters/*.py`, de-duplicated): **79** files —
17 under `tools/` (incl. `tools/mado-verify.sh`), 18 top-level `quality/*.py`, 44 `quality/counters/*.py`.
`PROVINCE.md`, `SCORECARD.md`, `LOG.md` and `corpus/**` are byte-identical between base and tip
(`git diff --stat 6ca8c559..3ac31642 -- PROVINCE.md SCORECARD.md corpus/ LOG.md` → empty), so every
pointer line number holds at both revisions.

Class distribution (primary class per row, first match in the priority order
`province-table` → `scorecard-capability` → `knowledge-named` → `lesson-named` → `quality-named` →
`successor-named` → `scorecard-row` → `wave-artifact`):

| class | rows | pointer surface |
|---|---|---|
| `lesson-named` | 27 | 17 distinct `corpus/lessons/*.md` files |
| `scorecard-capability` | 20 | `SCORECARD.md` capability tables |
| `province-table` | 20 | `PROVINCE.md` (11 tools, 6 counters, 3 top-level checks) |
| `successor-named` | 5 | the v2 counter's docstring naming its frozen v1 |
| `scorecard-row` | 4 | `SCORECARD.md` move-log/claim rows |
| `quality-named` | 3 | `corpus/QUALITY.md` criterion bodies |
| `wave-artifact` | 0 | — |
| `GAP` (no tracked file names it) | 0 | — |

59 of 79 rows have no `province-table` naming. The two files the round-50 wave-seat ledger missed,
`tools/mado-hostguard.py` and `tools/mado-keysym.py`, are covered here through `SCORECARD.md` capability
rows (`:2762`, `:2743`) — neither has a PROVINCE row.

## Gates and checks actually run

- Builder `build-ledger-rows.py` ran to completion (`rc=0`) against the lane at the tip: it re-reads
  **every** pointer line at `--rev` and exits non-zero if the line is out of range or the basename is
  absent. 79/79 passed.
- First pass (scratch script) additionally verified all 79 pointer lines at **both** the tip and the base:
  0 failures (`VERIFIED_ROWS 79 BAD []`).
- The builder refuses a description over 20 words and refuses a description keyed to a file outside the
  population (both assertions active; descriptions actually range 6–17 words).
- `python3 -I` compiles the builder; it writes nothing but `--out` and uses no temporary path (no
  `/tmp`, no TMPDIR — the only `/tmp` string is in its docstring stating that).
- Not run, by design: no compositor socket, no `hyprctl`, no config-plane read, no service probe. Row
  descriptions were written from headers, not from execution.

## Findings routed to the L1 freeze

- **F1 — the population sentence admits two different `P`.** `quality/*.py` as a *git pathspec* recurses
  into `counters/` (62 paths = 18 + 44); as a *filesystem glob* it returns 18. A summing implementation
  therefore counts 123 entries for 79 distinct files. "each such file appears exactly once" already
  implies a set: freeze "files under `tools/`, immediate children `quality/*.py`, immediate children
  `quality/counters/*.py`, de-duplicated" (`P = 79` at the tip; **`P = 81`** once this round's two new
  files land).
- **F2 — self-pointer loophole: 26 of 79 files contain their own basename** (usage/header text). A row
  pointing at **itself** satisfies "pointer names an existing repo file that contains the file's
  basename" and leaves `bad_pointer=0`. The freeze needs `pointer_file != row.file` plus a control that a
  self-pointer MISSes, or control (b) is defeatable without touching the ledger.
- **F3 — ledger-self loophole.** `quality/tool-ledger.md` will contain every basename and is **not** in
  the population (`quality/*.py` covers Python only), so any row could point at the ledger itself and
  pass. Add `pointer_file != quality/tool-ledger.md` and the same MISS control.
- **F4 — no durable instrument register for the `quality/` instruments.** 27 rows are accountable only
  through lesson/spot-check prose (mostly a sentence recording a *defect* in the counter), 5 only through
  the successor that superseded them, 4 only through a move-log row, 3 only through a QUALITY criterion
  body. Coverage is obtainable (0 strict gaps) but accountability for two-thirds of the instruments is
  incidental prose — the round-50 `RevLedgerR50` finding reproduced at lane level.
- **F5 — `:line` suffixes are rev-stable only while `PROVINCE.md`/`SCORECARD.md`/`corpus/**` do not
  move.** True today (base ≡ tip). A later insertion drifts the numbers while the basename test still
  passes, and a checker that only tests "contains the basename" will not notice. Either drop the `:line`
  suffix from the frozen row format, or freeze it as provenance only.
- **F6 — 7 pointer lines are shared by more than one row** (`corpus/lessons/round-48.md:153` ×5;
  `PROVINCE.md:100`, `PROVINCE.md:109`, `SCORECARD.md:2385`, `:2454`, `:2669`, `:2743` ×2 each).
  Legitimate (one capability row can name both a tool and its counter), but per-file accountability for
  those rows cannot be argued from the ledger alone.
- **Pending rows (not in the 79).** `quality/check-tool-ledger.py` and `quality/counters/c1-r51-ledger.py`
  are absent at the tip; both are named at `.ufo/waves/round-51/claims.md:20` and `:21` (verified, line
  contains the basename). At the revision where PRED-C1-r51 is scored, both exist, so the ledger must
  carry those two rows or `uncovered=2`.

## Touched surfaces

- Written: `.ufo/waves/round-51/w1/ScrLedgerRows/ledger-rows.md` (the row set),
  `.ufo/waves/round-51/w1/ScrLedgerRows/build-ledger-rows.py` (re-runnable, read-only builder), and this
  report.
- Read only: git objects of the lane (`ls-tree`, `show`, `grep`), `PROVINCE.md`, `SCORECARD.md`,
  `corpus/**`, `.ufo/waves/round-51/claims.md`. No config plane, no compositor, no network, no
  `shokuknow`.
- Scratch `/fast/scratch/hyaku/mado-r51/ScrLedgerRows/` removed after copying nothing out of it (the
  builder regenerates the deliverable).

## Out of scope (untouched)

- `quality/tool-ledger.md`, `quality/check-tool-ledger.py`, `quality/counters/c1-r51-ledger.py` — the
  ledger builder and the freeze belong to other seats/the L1.
- Round-50 bytes, including `.ufo/waves/round-50/fetch/SHA256SUMS` (D4/M50-9) — not edited, not
  normalised.
- D1 (final WAVE-DONE receipt), the 13-row absent-defect register slice, `merge/mado` theme scan.

## Limits

- Class boundaries are defined by *which file names the instrument*, not by intent: `ACCOUNTABILITY`
  here means "a tracked file names it", exactly the frozen `bad_pointer` test's notion. A conservative
  reading — "names it in an accountability context" — would shrink `province-table`/`scorecard-capability`
  slightly and push more rows into `lesson-named`.
- Lesson-named pointers are the **first** naming line in the chosen file, not a curated one; several read
  as defect sentences (`corpus/lessons/round-38.md:8`, `round-43.md:150`, `round-47.md:200`).
- Descriptions are header-derived prose, deliberately free of behavioural claims this seat did not run.
  Counters described as "superseded by v2"/"re-registered" rest on their successor's docstring or the
  PROVINCE refinement paragraph, both cited in the pointer column.

## Deliverables

- `.ufo/waves/round-51/w1/ScrLedgerRows/ledger-rows.md`
- `.ufo/waves/round-51/w1/ScrLedgerRows/build-ledger-rows.py`

Report: `.ufo/waves/round-51/w1/ScrLedgerRows.md`
