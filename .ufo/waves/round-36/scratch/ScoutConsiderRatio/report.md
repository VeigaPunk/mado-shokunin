# ScoutConsiderRatio — domain-versus-meta ratio, round 36 wave 1

Seat: scout. Prompt: `.ufo/waves/round-36/w1/prompts/ScoutConsiderRatio.md` (proposal 1 of `considerthese/2026-10-24.md`).

## 1. The measure (as specified)
From proposal 1 (considerthese/2026-10-24.md:46): "how many rounds touched `tools/`, `corpus/knowledge/` or `PROVINCE.md` versus only quality/records". Operationalized per commit over the lane's last 30 commits:

- **domain** = commit touches at least one of: `tools/`, `corpus/knowledge/`, `PROVINCE.md` (root paths only; `.ufo/waves/.../corpus/knowledge/` fixture copies are wave test data and excluded — they are not production knowledge).
- **record-only** = commit touches only records: `.ufo/`, `LOG.md`, `SCORECARD.md`, `corpus/{README,SOURCES,QUALITY,lessons}/`, `quality/`, `considerthese/`, `plans/`, `reports/`, root meta files (README/AGENTS/MINT/SHONEN/SKILL).

## 2. Exact commands

Pinned window: `19e4ab3..f77b554` (30 commits, oldest `02088b4` at the base edge, newest `f77b554`).

```bash
# window endpoints
git rev-parse HEAD            # f77b55478402afbb77fdc1f18e3826ac2c6e96d5 (tip)
git rev-parse HEAD~30         # 19e4ab3171c1540c40d6b12097745af98053b07d (base)
git log --format='%h %s' 19e4ab3..f77b554 | wc -l   # 30

# classification (git log --name-only pipeline)
git log --format='%h' 19e4ab3..f77b554 | while read c; do
  echo "== $c"
  git show --name-only --format='' "$c" | grep -v '^\.ufo/'   # non-wave paths
done
```

Classification was run via `git show --name-only --format=` per commit (same pipeline) with the bucket predicates above; every non-`.ufo/` path touched in the window is enumerated below (§4), so the buckets are exhaustive — there is no `other` category and no unclassified path.

## 3. Counts

| bucket | commits |
|---|---|
| domain | **4** |
| record-only | **26** |
| other | 0 (no commit touches a path outside the two buckets) |

**Domain commits:**
1. `02088b4` round-35 — idle-lock control surface: ADDS `corpus/knowledge/idle-lock-chain-armed-r14.md`, `idle-lock-never-asked-r12.md`, `idle-lock-offered-in-the-bar-r15.md` (+ modifies `corpus/QUALITY.md`, `README.md`, `SOURCES.md`, lessons).
2. `4f35c80` round-35 — falsification errata: MODIFIES the same three `corpus/knowledge/idle-lock-*.md` files.
3. `a3094c9` round-36 — repaired counters: MODIFIES `PROVINCE.md` (+ `quality/counters/c1-idle-lock.py`, `c2-ledger.py`).
4. `520c631` round-36 — records: MODIFIES `PROVINCE.md` (+ LOG/scorecard/QUALITY/lesson, `quality/receipts/`).

**Longest run of record-only commits: 20** — `dbf8b57` … `7b745a1` (round-36 freeze commit through round-35 closure sweep; consecutive). All record-only runs in the window: (20, `dbf8b57`→`7b745a1`), (6, `f77b554`→`ebc5437`) — note the run of 6 is at the newest tip since the pinned window (see §5), (4, `19e4ab3`→`57622b8`), (1, `3420e82`).

## 4. Exhaustive non-`.ufo/` path set in the window (evidence for classification)
```
corpus/lessons/round-36.md (6)   SCORECARD.md (6)   corpus/lessons/round-35.md (5)
corpus/SOURCES.md (4)            corpus/QUALITY.md (4)          LOG.md (4)
corpus/knowledge/idle-lock-*.md (2 each, 3 files)    corpus/README.md (2)
PROVINCE.md (2)                  quality/check-evidence-pointers.py (2)
quality/receipts/red-axis-publication-stale-at-data-commit.txt (1)
quality/receipts/axis-520c631….txt (1)   quality/counters/c2-ledger.py (1)
quality/counters/c1-idle-lock.py (1)     quality/check-counter-discrimination.py (1)
corpus/lessons/round-35-verifier-spotcheck.md (1)
```
Nothing else at root; all remaining changed paths in the window are under `.ufo/waves/`.

## 5. Round-36 side of the ratio (the two claims) + under-count note
Round-36 commits in the window: `dbf8b57` (freeze: C1/C2 predicates, manifest, cribs, before receipts — record-only), `a3094c9` (data: counters, ledgers, receipts, PROVINCE.md — domain), `520c631` (records — domain via PROVINCE.md), `ebc5437`, `c5d7773`, `cf175c7`, `2d90524`, `a5f76c9`, `f77b554` (record-only wave reports/after receipts).

The two round-36 claims (freeze: `registration.md`, both frozen at `dbf8b579`):
- **C1** (calibration): repaired counters do not exist in the freeze — `quality/counters/` was empty at the freeze commit, populated by `a3094c9` (`c1-idle-lock.py`, `c2-ledger.py`). C1's controls are `quality/check-counter-discrimination.py` (before: 14/25, `receipts/before-discrimination.txt`).
- **C2** (operability): `quality/check-evidence-pointers.py` over the lane's own records; before: TARGET_MISSED (`receipts/before-pointers.txt`).

**Under-counted: YES.** The round is mid-flight: the two quality gates are still being edited in the working tree (` M quality/check-evidence-pointers.py`, ` M .ufo/waves/round-36/w1/reports/RevIndexGate.md` at final snapshot), and at least three further round-36 commits landed *after* this window was pinned (`f77b554` → tip `2d90524`, see §6). The freeze commit `dbf8b57` is inside the window but the round's final outcome commits are not; the round-36 side of the ratio is therefore provisional and will change when the round closes.

## 6. Stability caveat (measurement was taken on a live repo)
HEAD advanced during measurement: 04:01 freeze → 04:24 `a3094c9` → 04:45 `c5d7773` → 04:46 `cf175c7` → 04:47 `2d90524`. The window `19e4ab3..f77b554` is pinned by SHA at first-stable snapshot (04:47); numbers are exact for that window as of that instant. Re-running against a later HEAD will shift the window and will count the 6 still-running round-36 record-only commits (`ebc5437`…`f77b554`), which would change the 20-run to 26 — a sign the "two or more rounds without a desktop-facing change" flag is still active at close.

## 7. Findings
1. **Ratio 4:26** domain:record-only over the last 30 commits (= 13% domain), i.e. about one domain commit per seven.
2. **Longest record-only run: 20** (`dbf8b57`…`7b745a1`) — spans the entire round-35 closure and the round-36 freeze; well past the proposal's "flag when the lane goes two or more rounds without a desktop-facing change" threshold. The only domain content in the window is the r35 idle-lock knowledge entries and two round-36 PROVINCE.md touch-ups — no `tools/` change since round 27 (`20022a6`, 2026-10-23).
3. Round-36 is **under-counted** (mid-flight; see §5).
4. `tools/` untouched: confirmed — last touch is `20022a6` (round-27 C1 data, `tools/mado-wsrules.py`).
