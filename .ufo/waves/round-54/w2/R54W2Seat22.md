# R54W2Seat22 — item 22: C2 S377 quote/teaches comparison

Axes: coverage, operability. Attack: whether frozen S377 quote matches the exact source pin and whether S377's `teaches` cell faithfully/appropriately characterizes the source evidence. No predicate/registration edits.

## Finding

The frozen source quote is present at the cited exact pin span, but the current registry S377 `teaches` cell explicitly rejects the content rather than teaching the frozen proposition. The live lane has not landed the round-54 C2 entry or counter, so there is no scored implementation to run. This is an observable C2 contract/data conflict, not a mutant kill result: the frozen registration requires the S377 row to be `mined` and used by the entry, whereas the current lane row is `rejected` and used-by is `—`.

Frozen predicate lines 60–63 require each S375–S377 row to be `mined`, opened 2026-10-27, commit-pinned, and its located quote to occur verbatim in the named pin. Registration lines 65–69 freeze S377's quote and anchor, and require the row shape `code`, tier A, `mined`, `on-release`, used-by the entry.

Exact pin evidence: `.ufo/waves/round-54/fetch/uwsm-0.27.1-main.py:3714` is exactly `unit_name = f"app-{desktop_unit_substring}-{cmd_unit_substring}-{random_hex(8)}.{app_unit_type}"`, verbatim identical to the frozen registration quote. The nearby branches at 3715–3718 distinguish service naming and invalid type; this anchor's quoted line is source text, not evidence by itself of app-environment behavior. The pin hash matches frozen registration's SHA256 `7dd6363244c101c7a0e7641684e29b6a13905e98f9fc3a4c81421e536a976c72`, as recorded in `.ufo/waves/round-54/fetch/SHA256SUMS.txt:2`.

Exact current source row: `corpus/SOURCES.md:327` (S377) has scope `generated app unit-name construction (adjacent system-session ground)` but its teaches cell reads `REJECTED: systemd application-unit naming is outside mado's province; flip: an explicit province ruling or a lane-owned claim limited to static launch declarations`; status is `rejected`, used-by `—`. This is a direct conflict with the frozen required row state and frozen C2 predicate. The teaches cell does not paraphrase the construction quote; it rejects its admission. Even a paraphrase like “constructs a randomized app unit name from desktop/cmd substrings and app unit type” would fit the exact line more faithfully, but whether that source belongs to scope is a governance decision; the frozen contract already settles the tested row requirement for this round and must remain unchanged.

Relevant W1 report: `.ufo/waves/round-54/w1/R54Seat22.md` lines 5–19 attacked repeated host citations under clause (c), noted the absent counter, and recommended distinct locations. That report is a separate clause-(c) ambiguity, not evidence about S377. This attack is item 22's specific quote/teaches comparison.

## Detector / status

Pinned command per claims-frozen.md: `python3 -I quality/counters/c2-r54-uwsm-entry.py --repo . --rev <rev>` — NOT RUN: counter absent. Entry `corpus/knowledge/uwsm-app-environment-r54.md` also absent. Thus the frozen predicate currently cannot be scored; the source/pin mismatch is directly evidenced from committed lane bytes, while counter behavior is unknown. No mutant was applied because the counter and target entry are absent; no claim of killed/survived mutant.

Exact commands and outputs (lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`):

- `test -e quality/counters/c2-r54-uwsm-entry.py` → no output; exit 1 (absent).
- `test -e corpus/knowledge/uwsm-app-environment-r54.md` → no output; exit 1 (absent).
- `git rev-parse HEAD` → `350d30e4ec5531f65ce99a57efeb8216f38e678a`; exit 0. This differs from specified base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`; no git mutation performed.

Pinned command output/exit: NOT RUN / absent.

## Scratch and restoration

No mutation performed; no restore required. Scratch was explicitly created at `/fast/scratch/hyaku/mado-r54/R54W2Seat22` and removed before report completion. No installs, host reads, or producer execution.

---
Report path (relative to lane root): `.ufo/waves/round-54/w2/R54W2Seat22.md`
