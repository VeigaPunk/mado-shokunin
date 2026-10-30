# R56W3RevFreezeBlind — receipts: D4 freeze-order blindness

Scored at lane tip `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`. Checker blob
`quality/check-freeze-order.py` = `ada2cf72fd73a2f2d65885a45b406a0f5b032ed0`. All times are committer
times unless marked; UTC shown with Z. Local offset is -03:00 (so local 21:22:47 = 00:22:47Z next day).
Every git call was read-only (`rev-parse`, `show`, `log`, `ls-tree`, `cat-file`, `clone --shared` of the lane
into scratch). Nothing in the lane was written.

## 1. Blindness map — `quality/check-freeze-order.py` at 0f3a5436

| line | code | effect on the v2 files |
|---|---|---|
| 10-12 | docstring: `FREEZE set: .ufo/waves/round-N/{claims-frozen.md,registration.md,frozen-tables.json}` | the set is declared as three names; v2 is not in it |
| 36 | `REQUIRED = ("claims-frozen.md", "registration.md")` | no v2 name |
| 37 | `OPTIONAL = ("frozen-tables.json",)` | `frozen-tables-v2.json` absent |
| 112 | `at_rev = blobs_at(repo, tip, [base + "/" + n for n in REQUIRED + OPTIONAL], work)` | v2 blobs are never read at REV |
| 116 | `fset = [p for p in ... if p in at_rev]` | v2 never enters the freeze set |
| 120 | `git log --first-parent --full-history --format=%H tip -- <fset>` | commits that touch only v2 are never enumerated as changers |
| 128-131 | `all(have.get(x) == at_rev[x] for x in fset)` | freeze commit chosen by v1 equality only |
| 133 | `edited = [x for x in fset if first_seen.get(x) != at_rev[x]]` | an edit to a v2 file is never `freeze_edited` |
| 140-142 | `ct = ... show -s --format=%cI anchor`; `f["freeze"] = anchor[:12]` | the reported `freeze=` / `freeze_time=` is the v1 commit even when v2 entered later |
| 146-158 | `cat-file blob tip:<base>/<wave>/swarm-registry.json` → `createdAt` | LAUNCH is the self-declared `createdAt` in the registry blob at REV, not the git time of the commit that added it |
| 164-168 | `parse_iso(ct) < launch_dt` → OK / `freeze_after_launch` | verdict only sees the v1-derived anchor |

Byte-level consequence: the set is computed from REV, so a v2 file that is absent from the v1 freeze commit
and enters later moves nothing; a v2 file edited after launch moves nothing.

## 2. Chronology of round 56 (committer times; `Z` = UTC)

| event | UTC | source |
|---|---|---|
| v1 freeze `3423ae28` | 2026-10-29T00:19:17Z | `git show -s --format=%cI 3423ae28` = 21:19:17-03:00 |
| w1 spec/registry `2aa347b1` | 2026-10-29T00:22:53Z | committer 21:22:53-03:00 |
| w1 launch `createdAt` | 2026-10-29T00:22:47.615Z | `w1/swarm-registry.json` at 2aa347b1 |
| w1 dispatch marker | 2026-10-29T00:27:02Z | `w1.ready.dispatched` mtime 21:27:02 -03 |
| w1 results file | 2026-10-29T00:39:43Z | `w1-results.json` mtime 21:39:43 -03 |
| **v2 entry `323a69c9`** | **2026-10-29T00:44:35Z** | committer 21:44:35-03:00 (author 21:44:34) |
| v2 files mtime | 00:43:46Z / 00:44:16Z | `registration-v2.md` / `claims-frozen-v2.md` mtime |
| w1 results commit `9c3ca28a` | 2026-10-29T01:01:22Z | committer 22:01:22-03:00 |
| errata `15015e77` (`registration-v2-errata.md`) | 2026-10-29T01:04:18Z | committer 22:04:18-03:00 |
| w2 launch `createdAt` | 2026-10-29T01:04:27.541Z | `w2/swarm-registry.json` at 19be88b6 |
| w3 launch `createdAt` (uncommitted, working tree) | 2026-10-30T05:01:50.708Z | `w3/swarm-registry.json`, sha256 `6d2591c69c94f98d...` |
| w3 dispatch marker | 2026-10-30T05:05:19Z | `w3.ready.dispatched` mtime 02:05:19 -03 |

`registration-v2.md` lines 1-3 say the v2 file was "Written 2026-10-28 by the L1 after wave 1 settled (43 seats,
0 dead)". The seat premise "v2 entered before any wave" is therefore false for wave 1.

## 3. Blob equality: v2 content at tip vs at entry

```
$ git -C LANE log --first-parent --format='%h %cI %s' 0f3a5436 -- claims-frozen-v2.md registration-v2.md frozen-tables-v2.json
323a69c9 2026-10-28T21:44:35-03:00 round-56: registration v2 (pre-data), frozen tables v2, ...
$ git -C LANE log --format='%h %cI %s' 0f3a5436 -- <same three>        # no-first-parent, whole history
323a69c9 2026-10-28T21:44:35-03:00 ...
claims-frozen-v2.md equal f9b76148d871f8d356bfc6356c8d9a8d6bdce78f
registration-v2.md  equal 4689de72e0f33c7b5561131fb93954784b8f4192
frozen-tables-v2.json equal e97271bc98a96ed49226380e7fbe0b2e06edd495
sha256(frozen-tables-v2.json @tip) = 9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2   (matches the registration pin)
```

Companion v2 artifacts: `c3-name-only.tsv`, `ctl/sibling-reader.py`, `freeze-verify-v2.py` last touched `323a69c9`;
`registration-v2-errata.md` last touched `15015e77`. None of the four is in the checker's set.

## 4. Verdicts at tip, original vs patched checker

```
$ python3 -I check-orig.py --repo LANE --rev 0f3a5436 --round 56 --wave w1 --work SCRATCH
MADO_FREEZE_ORDER: round=56 wave=w1 freeze=3423ae285676 freeze_time=2026-10-28T21:19:17-03:00 launch=2026-10-29T00:22:47.615Z verdict=OK reason=ok        rc=0
$ python3 -I patched/check-freeze-order.py --repo LANE --rev 0f3a5436 --round 56 --wave w1 --work SCRATCH
MADO_FREEZE_ORDER: round=56 wave=w1 freeze=323a69c9014d freeze_time=2026-10-28T21:44:35-03:00 launch=2026-10-29T00:22:47.615Z verdict=FAIL reason=freeze_after_launch   rc=1
$ ... check-orig.py ... --wave w2
MADO_FREEZE_ORDER: round=56 wave=w2 freeze=3423ae285676 freeze_time=2026-10-28T21:19:17-03:00 launch=2026-10-29T01:04:27.541Z verdict=OK reason=ok        rc=0
$ ... patched ... --wave w2
MADO_FREEZE_ORDER: round=56 wave=w2 freeze=323a69c9014d freeze_time=2026-10-28T21:44:35-03:00 launch=2026-10-29T01:04:27.541Z verdict=OK reason=ok        rc=0
$ ... check-orig.py ... --wave w3   (registry not yet committed at tip)
MADO_FREEZE_ORDER: round=56 wave=w3 freeze=3423ae285676 freeze_time=2026-10-28T21:19:17-03:00 launch=none verdict=FAIL reason=no_registry   rc=1
```

Selftests: `python3 -I check-orig.py --selftest --work S` → `MADO_FREEZE_ORDER_SELFTEST: OK`;
`python3 -I patched/check-freeze-order.py --selftest --work S` → `MADO_FREEZE_ORDER_SELFTEST: OK` (both 11 cases, unchanged).

## 5. RED / GREEN — synthetic scratch repo

Repo built with `git -C D init`; `git -C D rev-parse --show-toplevel` = D checked before the first commit.
Freeze commit 2026-10-27T10:00-03 holds all six round-9 files (three v1, three v2); launch registry
`createdAt 2026-10-27T14:00:00.000Z` committed 11:30-03; then `claims-frozen-v2.md` appended and committed 12:00-03.

```
-- control (rev = launch commit, before the v2 edit), current:
MADO_FREEZE_ORDER: round=9 wave=w1 freeze=626539b71d36 freeze_time=2026-10-27T10:00:00-03:00 launch=2026-10-27T14:00:00.000Z verdict=OK reason=ok   rc=0
-- control, patched:
MADO_FREEZE_ORDER: round=9 wave=w1 freeze=626539b71d36 ... verdict=OK reason=ok   rc=0
-- RED  (HEAD, v2 edited after launch), CURRENT checker:
MADO_FREEZE_ORDER: round=9 wave=w1 freeze=626539b71d36 freeze_time=2026-10-27T10:00:00-03:00 launch=2026-10-27T14:00:00.000Z verdict=OK reason=ok   rc=0
-- GREEN (HEAD), PATCHED checker:
MADO_FREEZE_ORDER: round=9 wave=w1 freeze=66e8c72e785c freeze_time=2026-10-27T12:00:00-03:00 launch=2026-10-27T14:00:00.000Z verdict=FAIL reason=freeze_edited:claims-frozen-v2.md   rc=1
```

RED = `OK` on the post-launch v2 edit (blind). GREEN = `freeze_edited:claims-frozen-v2.md`.

## 6. Replay on the real lane history (scratch `git clone --shared`, toplevel asserted)

Clone HEAD = `0f3a5436`. C1 = tip + the uncommitted w3 registry copied as `w3/swarm-registry.json`, committer
2026-10-30T05:02Z (a simulation of the commit the lane will make). C2 = C1 + one appended line in
`claims-frozen-v2.md`, committer 2026-10-30T06:00Z (post-launch).
C1 = `cd9303654eb5`, C2 = `1affd847bb0e`.

```
-- w3 @C1 (no mutation), current : verdict=OK  freeze=3423ae285676 launch=2026-10-30T05:01:50.708Z
-- w3 @C1, patched               : verdict=OK  freeze=323a69c9014d launch=2026-10-30T05:01:50.708Z
-- w3 @C2 (v2 edited after w3 launch), current  [RED]  : verdict=OK  freeze=3423ae285676   rc=0
-- w3 @C2, patched                              [GREEN]: verdict=FAIL reason=freeze_edited:claims-frozen-v2.md freeze=1affd847bb0e   rc=1
-- w2 @C2, current : verdict=OK  freeze=3423ae285676
-- w2 @C2, patched : verdict=FAIL reason=freeze_edited:claims-frozen-v2.md freeze=1affd847bb0e
```

`git show --stat C2` = `claims-frozen-v2.md | 1 +` (only file changed).

## 7. Regression sweep of the patch over every round 17-56, waves w1-w3

Loop: for each round R and wave W, run both checkers at the lane tip, skip pairs where the current checker says
`no_freeze`/`SETUP` (the patch cannot change those: `claims-frozen.md` is required). 12 pairs compared:

```
DIFF r55 w1  cur: freeze=54dacbd843d6 freeze_time=2026-10-28T18:46:52-03:00 launch=2026-10-28T21:50:15.231Z verdict=OK rc=0
             pat: freeze=5a43d67f99e4 freeze_time=2026-10-28T20:11:17-03:00 launch=2026-10-28T21:50:15.231Z verdict=FAIL reason=freeze_after_launch rc=1
DIFF r55 w2  cur: ... verdict=OK rc=0 (freeze 54dacbd843d6)
             pat: ... freeze=5a43d67f99e4 ... verdict=OK rc=0
DIFF r55 w3  cur: freeze=54dacbd843d6 ... launch=none verdict=FAIL reason=no_registry
             pat: freeze=5a43d67f99e4 ... launch=none verdict=FAIL reason=no_registry
DIFF r56 w1  cur: freeze=3423ae285676 ... verdict=OK rc=0
             pat: freeze=323a69c9014d ... verdict=FAIL reason=freeze_after_launch rc=1
DIFF r56 w2  cur: freeze=3423ae285676 ... verdict=OK rc=0
             pat: freeze=323a69c9014d ... verdict=OK rc=0
DIFF r56 w3  cur: freeze=3423ae285676 ... launch=none verdict=FAIL reason=no_registry
             pat: freeze=323a69c9014d ... launch=none verdict=FAIL reason=no_registry
compared=12 differing=6   (the other 6 pairs identical)
```

Round 55: `5a43d67f` (registration-v2.md + frozen-tables-v2.json) committed 2026-10-28T20:11:17-03:00, after the
round-55 w1 launch (21:50:15Z). The recorded verdict `round=55 wave=w1 ... verdict=OK` is at
`.ufo/waves/round-55/receipts/at-final.txt:44`. The patch flips that recorded OK to FAIL.

## 8. Residual blind spots (outside the three named files; not in the patch)

- `claims-frozen.md` lines 3-5 (and `registration.md` line 4) say `frozen-tables.json`, `fixtures/c2/`, `ctl/`,
  `fetch/`, `freeze-verify.py` and `receipts/{before,census-before,selftest-before,scope-replay-r55,pins}.*`
  "are committed in ONE freeze commit BEFORE any wave .ready". The checker's set covers none of the directories.
- Commits touching those directories after the v1 freeze `3423ae28`, first-parent:
  ```
  ctl                323a69c9 2026-10-28T21:44:35-03:00   (adds ctl/sibling-reader.py, 15 lines)
  fetch              0ff41272 2026-10-28T21:59:02-03:00   (adds fetch/Hyprland-PropRefresher.hpp, 40 lines)
  fixtures/c2        (none)
  freeze-verify.py   (none)
  frozen-tables.json (none; blob 7fca8087 at 3423ae28 and tip)
  ```
- `fetch/Hyprland-PropRefresher.hpp` is not in any frozen pin: the pinned file is `Hyprland-PropRefresher.cpp`
  (`frozen-tables.json` c1.pin_sha256 `65f01a1a…2817b`). `git cat-file -e 3423ae28:…/Hyprland-PropRefresher.hpp` = no;
  `git cat-file -e 2aa347b1:…` = no. Its first commit is `0ff41272` at 00:59:02Z, after the w1 launch (00:22:47.615Z).
- `registration-v2-errata.md` entered at `15015e77` 01:04:18Z, nine seconds before the w2 launch `createdAt`
  01:04:27.541Z, after the w1 results commit `9c3ca28a` 01:01:22Z.
- `LAUNCH` is `createdAt` (self-declared plan time): the w3 `createdAt` 05:01:50.708Z is 3 min 29 s before the
  dispatch marker 05:05:19Z. Declared in the docstring at lines 24-28; not v2-specific.

## 9. Why the wave-3 launch is still order-safe (fact chain, not checker verdict)

1. v2 content at launch = v2 content at `323a69c9` (blob equality at tip, section 3).
2. No first-parent or full-history commit touches the three v2 freeze files after `323a69c9` (section 3).
3. `323a69c9` committer 2026-10-29T00:44:35Z precedes the w3 launch `createdAt` 2026-10-30T05:01:50.708Z by 28 h 17 min
   and the w3 dispatch marker 05:05:19Z.
4. The v1 freeze `3423ae28` (00:19:17Z) precedes the w3 launch too.

So order-safety for w3 holds on the facts. The checker's OK for w3 (section 5 and 6, current variant) comes from
v1 alone and would still read OK after a post-launch v2 edit (section 6, RED). The checker does not establish the
w3 order; the blob and commit facts do.

Round-56 w1 is NOT order-safe for v2: v2 entered 00:44:35Z after the w1 launch 00:22:47.615Z. w1 ran against
v1, which entered `3423ae28` at 00:19:17Z before the launch. The patched checker reports that correctly as
`freeze_after_launch`.

## 10. Not verified / limits

- The w3 registry is not committed at tip; its launch time (05:01:50.708Z) is read from the working-tree file.
  Section 6 uses a simulated commit for it.
- Variant B (anchor on v1 only; compare v2 edits only; no v2 creation timestamp) was reasoned about and not
  implemented or run.
- Section 7 compares only the 12 pairs the current checker can score. Rounds 40-48 have `registration-v2.md` but
  no `claims-frozen.md`; they are `no_freeze` under both checkers.
- No hyprctl, /proc, journal or host reads were used (not needed for this seat).
- No package was installed; no pacman transaction; no tool added to PATH.
