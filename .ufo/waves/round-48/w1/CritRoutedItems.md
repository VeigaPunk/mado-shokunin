# CritRoutedItems — round-48 w1: routed round-47 closure items, open/stale check

Seat: `CritRoutedItems` (leaf). Reviewed rev: `579f694b45c797a9c39761fdb4f9e0a1b71b3585` (lane tip at round start).
Method: read-only `git log`/`git ls-tree`/`git grep`/`git show` at 579f694b; one fresh read-only run of the tracked
session-material gate; quote verification script. Nothing was written outside this seat dir; no tools installed; no
scratch used (no generated files). Post-base commit `5ff16742` touched only `.ufo/waves/round-48/*`; no referenced
draft changed after base.

**Status: all nine routed items (D1-D4, R3, R4b, M47-10, `w2/CritC1Explain.md`, `w2/SentC1Sandbox.md` F1-F4)
are still open at base, and none of the round-47 drafts they point at is stale** (each draft was created in one wave
commit and never modified; their targets — counters, fixtures, entries, registration — are byte-unchanged at base).

Per-item evidence: `.ufo/waves/round-48/w1/CritRoutedItems/findings.md` (table with one line per item + receipts).

Receipts:
- `git log` per referenced file at base: w2 drafts all created in `d40189c9` (single commit each);
  `w1/ExecSessionMarker/check-session-material.py` in `9bddd6ac`; selection entry in `0c699605`; frozen counter/
  fixtures/registration/l1-draft in `d7527d60`; r45 entry + tracked gate in `ee6659b9`; `terminal-route-r17.md` in
  `f71ccbe5` — none modified since.
- `git grep 'findings=128' 579f694b` → NO-MATCH (D2 unreceipted number).
- Live gate: `python3 -I quality/check-session-material.py --repo . --rev 579f694b...` → `SESSION_MATERIAL:
  files=19969 findings=128 rev=579f694b...` exit 1 (R3 still red; D2's number reproduced, still unreceipted).
- `git status --porcelain` after the gate run: no tracked change.
- `verify-quotes.sh` (seat dir): 10/10 quoted fragments verified by grep at computed locators.
