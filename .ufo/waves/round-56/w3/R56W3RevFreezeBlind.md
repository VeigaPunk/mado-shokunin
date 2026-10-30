# R56W3RevFreezeBlind — report (round 56, wave w3, attempt 2)

Scored at lane tip `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`. Lane not written; scratch removed.
Full evidence: `.ufo/waves/round-56/w3/R56W3RevFreezeBlind/receipts/freeze-blind.md`.
Deliverable diff (never applied): `.ufo/waves/round-56/w3/R56W3RevFreezeBlind/freeze-blind.diff`.

## Item attacked
D4 blindness of `quality/check-freeze-order.py` (blob `ada2cf72`) to `claims-frozen-v2.md`,
`registration-v2.md`, `frozen-tables-v2.json`; and whether the w3 launch is order-safe anyway.

## Blindness lines (check-freeze-order.py @0f3a5436)
- 36-37: `REQUIRED = ("claims-frozen.md","registration.md")`, `OPTIONAL = ("frozen-tables.json",)`: no v2 names.
- 112 and 116: `blobs_at` and `fset` read only `REQUIRED + OPTIONAL`, so v2 blobs are never read at REV.
- 120: `git log --first-parent -- <fset>` never enumerates v2-only changer commits.
- 133: `edited` is computed over `fset` only, so a v2 edit is never `freeze_edited`.
- 140-142: `freeze=` / `freeze_time=` is the v1 commit `3423ae28` even though v2 entered later.
- 146-158: LAUNCH is the self-declared `createdAt` in the registry blob at REV.
- 10-12: docstring declares the three-name set.

## Patch (deliverable, not applied)
Two lines: the docstring FREEZE list and `OPTIONAL` (line 37) gain the three v2 names. Every use of
`REQUIRED + OPTIONAL` picks them up. The original selftest (11 cases) and the patched one both print OK.

## Red / green
- Synthetic scratch repo (v2 edited after launch): current prints `verdict=OK reason=ok` (RED);
  patched prints `reason=freeze_edited:claims-frozen-v2.md` (GREEN). Control before the edit: both OK.
- Real-history replay (clone of the lane + simulated w3 registry commit + post-launch v2 append):
  current prints `w3 ... verdict=OK` (RED); patched prints `verdict=FAIL reason=freeze_edited:claims-frozen-v2.md` (GREEN).

## Why w3 is order-safe despite the blindness
The checker does not establish it; the facts do:
- v2 blobs at tip equal their blobs at `323a69c9` (`f9b76148`, `4689de72`, `e97271bc`).
- The only commit touching the three v2 freeze files, in the whole history, is `323a69c9`.
- `323a69c9` is committed 2026-10-29T00:44:35Z. The w3 launch `createdAt` is 2026-10-30T05:01:50.708Z,
  and the w3 dispatch marker is 05:05:19Z.

The current checker's OK for w3 comes from v1 alone and would still read OK after a post-launch v2 edit (RED above).

## Defects
1. **Weakens (round 56 v2 claims):** the checker is blind to v2 at the lines above. Input: lane tip, `--wave w1`
   prints `freeze=3423ae285676 ... verdict=OK` though the v2 files did not exist in that commit. Replay: post-launch
   v2 append still reads `w3 ... verdict=OK`.
2. **Weakens (premise):** "v2 entered before any wave" is false. `323a69c9` (00:44:35Z) is after the w1 launch
   (`createdAt` 00:22:47.615Z) and after w1 results (`w1-results.json` 00:39:43Z). `registration-v2.md` lines 1-3 say
   it was "Written ... after wave 1 settled". w1 ran against the v1 freeze (`3423ae28`, 00:19:17Z), which does precede it.
   The patched checker reports w1 as `freeze_after_launch`, which is correct for v2.
3. **Weakens; blocks the patch as a "harm none" move (decision for the orchestrator):** the minimal patch flips two
   recorded OK verdicts: R56 w1 (`freeze=3423ae28`, OK → `323a69c9`, FAIL freeze_after_launch) and R55 w1
   (`round-55/receipts/at-final.txt:44`, `54dacbd8` OK → `5a43d67f`, FAIL, because round-55's v2 `5a43d67f`
   was committed 23:11Z, after the R55 w1 launch 21:50:15Z). Sweep r17-r56 × w1-w3: 12 pairs compared, 6 differ
   (R55 w1, w2 freeze field, w3 freeze field; R56 w1, w2 freeze field, w3 freeze field). Only R55 w1 and R56 w1 change
   verdict. These flips are the honest reading, but they change receipts. Options for round 57: accept the correction
   and record it, or use variant B (anchor on v1; compare only edits to v2 files). Variant B was not implemented or run.
4. **Weakens (residual, not v2-specific):** the checker's set covers none of the directories `claims-frozen.md`
   lines 3-5 say are frozen in ONE freeze commit (`fixtures/c2/`, `ctl/`, `fetch/`, `freeze-verify.py`, `receipts/`).
   Post-freeze additions: `ctl/sibling-reader.py` (`323a69c9`, 00:44:35Z, after w1 launch) and
   `fetch/Hyprland-PropRefresher.hpp` (`0ff41272`, 00:59:02Z, after w1 launch; unpinned — the pinned file is the `.cpp`).
5. **Weakens (residual):** `registration-v2-errata.md` (`15015e77`, 01:04:18Z) entered 9 s before the w2 launch
   `createdAt` 01:04:27.541Z. It is outside the checker's set, as are `c3-name-only.tsv`, `ctl/sibling-reader.py`,
   `freeze-verify-v2.py`. The patch covers only the three named files.
6. **Cosmetic:** LAUNCH is the registry's self-declared `createdAt` (line 146-158), 3 min 29 s before the w3 dispatch
   marker. Already declared in the docstring (lines 24-28).

## Commands and decisive output (trimmed; full text in receipts)
```
$ python3 -I check-orig.py --repo LANE --rev 0f3a5436 --round 56 --wave w1 --work S
MADO_FREEZE_ORDER: round=56 wave=w1 freeze=3423ae285676 freeze_time=2026-10-28T21:19:17-03:00 launch=2026-10-29T00:22:47.615Z verdict=OK reason=ok        rc=0
$ python3 -I patched/check-freeze-order.py --repo LANE --rev 0f3a5436 --round 56 --wave w1 --work S
MADO_FREEZE_ORDER: round=56 wave=w1 freeze=323a69c9014d freeze_time=2026-10-28T21:44:35-03:00 launch=2026-10-29T00:22:47.615Z verdict=FAIL reason=freeze_after_launch   rc=1
$ python3 -I check-orig.py --repo SYN --rev HEAD ...      # v2 edited after launch (synthetic)
MADO_FREEZE_ORDER: round=9 wave=w1 ... verdict=OK reason=ok                                        rc=0   [RED]
$ python3 -I patched/check-freeze-order.py --repo SYN --rev HEAD ...
MADO_FREEZE_ORDER: round=9 wave=w1 freeze=66e8c72e785c ... verdict=FAIL reason=freeze_edited:claims-frozen-v2.md  rc=1   [GREEN]
$ python3 -I check-orig.py --repo CLONE --rev C2 --round 56 --wave w3 --work S   # real history + post-launch v2 append
MADO_FREEZE_ORDER: round=56 wave=w3 freeze=3423ae285676 ... verdict=OK reason=ok                   rc=0   [RED]
$ python3 -I patched/check-freeze-order.py --repo CLONE --rev C2 --round 56 --wave w3 --work S
MADO_FREEZE_ORDER: round=56 wave=w3 freeze=1affd847bb0e ... verdict=FAIL reason=freeze_edited:claims-frozen-v2.md  rc=1   [GREEN]
$ git -C LANE log --first-parent --format='%h %cI %s' 0f3a5436 -- claims-frozen-v2.md registration-v2.md frozen-tables-v2.json
323a69c9 2026-10-28T21:44:35-03:00 round-56: registration v2 (pre-data), frozen tables v2, ...
$ sha256sum frozen-tables-v2.json @tip -> 9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2 (matches pin)
$ python3 -I check-orig.py --selftest --work S      -> MADO_FREEZE_ORDER_SELFTEST: OK
$ python3 -I patched/check-freeze-order.py --selftest --work S -> MADO_FREEZE_ORDER_SELFTEST: OK
```

## Not verified
- The w3 registry is uncommitted at tip; its launch time comes from the working-tree file (sha256 `6d2591c6…`).
  The replay used a simulated commit.
- Variant B: not implemented or run.
- Rounds 40-48 have `registration-v2.md` but no `claims-frozen.md`; they are `no_freeze` under both checkers, so the
  patch cannot change them. Not checked further.
- No hyprctl, /proc, journal or host reads (not needed for this item).

## Tooling
No tool was installed, upgraded or added to PATH. No pacman transaction. Git was read-only against the lane (`rev-parse`,
`show`, `log`, `ls-tree`, `cat-file`, `grep`, `clone --shared` into scratch). The lane's working tree was not touched.
