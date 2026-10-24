# ScoutIndexHistory — how the 41/43 gap formed

Read-only reconnaissance; all git state untouched. Revs abbreviated; full hashes in commit titles.

## 1. Formation timeline (observed)

| Rev | Date | Notes `corpus/knowledge/*.md` | Index `corpus/README.md` | Event |
|---|---|---|---|---|
| `ca135237` | 10-23 | 41 | 41/41 | r26 data: `animation-table-r26.md` added **with** README index row (commit msg: "README index + route") — last green index |
| `86f7355` | 10-23 | 42 | 41/42 | r27: added `workspace-rules-r27.md`; touched `SCORECARD.md`, `SKILL.md`, `corpus/SOURCES.md` — **no `corpus/README.md`** |
| `43fdd7e` | 10-23 | 42 | 41/42 | r27 follow-up: same note only (`verified-at` update) |
| `317ff19` | 10-23 | 43 | 41/43 | r28: added `mutation-testing-r28.md`; corpus touches = note, `SOURCES.md`, `lessons/round-27.md`, `lessons/round-28.md` — **no `corpus/README.md`** |
| `cb4e1c0`–`8f51071b` | 10-24 | 43 | 41/43 | r29: no knowledge notes added; README again untouched; gap discovered |
| `446dc396` | 10-24 | 43 | 43/43 | r30 data commit: +2 rows, first `corpus/README.md` touch since `ca135237` |

Decisive: `git log ca135237..HEAD -- corpus/README.md` = exactly one commit, `446dc396`.

Commits that added the notes — **confirmed neither touched `corpus/README.md`**:
- `workspace-rules-r27.md` → **`86f7355`** ("round-27: SOURCES S178-S182 … knowledge note workspace-rules-r27, SKILL gate registry rows"). Staged draft lived in `5c1d495` under `.ufo/waves/round-27/drafts/` (not corpus).
- `mutation-testing-r28.md` → **`317ff19`** ("round-28 integration: three suite-A blind-spot probes…"). Its only `corpus/` writes: the note, `SOURCES.md`, two lesson files.

## 2. Did any round 27–30 run the navigation fence and record 41/43? (observed)

- **Rounds 27, 28 — no.** `lessons/round-27*.md` and `lessons/round-28*.md` contain zero occurrences of `indexed`, `index row`, or `README`; registrations carry no flat-index axis (r27 C1 = 41-case tool counter `PRED-C1-r27-v4`; r28 explicitly "not a coverage claim"). The many `41/41` strings in r27–29 records are *case-counter* results (coincidentally matching the 41-row index) — not fence output.
- **Round 29 — yes, twice, no committed receipt.** `corpus/lessons/round-29.md` `M29-sweep` (committed `cb4e1c0`): a sweep line asserting the navigation counter stays exit-0 was found FALSE post-commit and corrected in place — "the navigation counter … reads 41/43 at base and tip alike, an inherited round-27/28 index gap … routed to round 30 intent, not silently repaired". `corpus/lessons/round-29-verifier-spotcheck.md` (committed `8f51071b`): coverage verdict "unchanged — The inherited index gap remains: `mutation-testing-r28.md` and `workspace-rules-r27.md` exist under `corpus/knowledge/` but have no rows in `corpus/README.md`", routing "the 41/43 gap as unchanged" forward.
- **Round 30 — yes, receipts committed.** `.ufo/waves/round-30/evidence/c1-before-8f51071b.txt` (`indexed=41/43 missing=2` exit 1), `controls/C3K1-base-red.txt`, `freeze-smoke-451e8b3c.txt`, `c3-after-446dc396.txt`; registration rows lines 26/44/72.
- `.ufo/reports/`: only `round-1/mado.md` contains `indexed=` — **no committed fence receipt exists for rounds 27–29 anywhere in `.ufo/`**.

## 3. Inference

The fence is the embedded "Counting command" Python block at `SCORECARD.md:77-84` (now S185; `check-index.py` re-implements it). It survived as a *recorded* rubric but stopped being a *registered scored axis*: rounds 27–29 measured per-round counters instead. Rounds 27 and 28 each added a note without an index row — a two-commit omission pattern (r26's `ca135237` shows the paired commit style was established: note + "README index + route" in one commit). With no fence run at either closure, the gap went undetected for two rounds; the 41/41 case-counter overlap likely further masked it. Round 29's closure sweep ran the fence, found 41/43, recorded it in lesson/spotcheck (no receipt file), and routed it rather than repairing out-of-band — consistent with the claim discipline quoted in M29-sweep.

## Remaining unknowns

- Whether the r29 sweep's 41/43 run was ever captured to a file before the lesson was corrected (the committed correction says it was found FALSE *after commit*; the earlier claim text was rewritten, so only the corrected text survives).
- `git log --follow` shows `43fdd7e` also modified the r27 note — noted for completeness, index-neutral.
- ~~Fence semantics: `check-index.py` vs the embedded SCORECARD snippet not diffed~~ — RESOLVED by peer `RevC1Fence` (`w1/reports/RevC1Fence.md`): gate ROW_RE `^\|\s*` is a strict superset of the fence's `^\| `, plus `--root`/`--rev` divergence on empty trees, non-ASCII path quoting, `split()` vs `splitlines()`, and a pinned-baseline-vs-`master` default divergence — all latent on committed bytes.

Confidence: high on all stated facts (commit name-lists and byte counts directly queried); medium on the masking hypothesis (marked inference).
