# RevCommitChain — round-38 commit-chain audit (wave 1)

Auditor: L1Mado38.RevCommitChain (leaf; no subagents dispatched). Date: 2026-10-25.
Scope: the commit chain of the landed round-38 at lane `master` HEAD `f0c9432a`. Read-only on
production files; no git mutations in LANE (only `log`/`show`/`ls-tree`/`diff`/`status`/`grep`).
Scratch: /tmp/mado38-RevCommitChain/.

## What I attacked

1. Freeze ordering: does `58e55ec9` precede all data commits?
2. Freeze completeness: registration.md + counters + manifest + fetch receipts + live triplet at the freeze?
3. Are the fetch receipts and live triplet committed at the freeze (counters need them), and unmodified after?
4. Is registration.md's frozen_at honest?
5. Any file under `.ufo/waves/round-38` modified after the data commit that the counters depend on?

## Commands and evidence

### Chain (git log -8 master)

```
f0c9432a84662478ae2215c783be16c8f4d208cd 2026-10-25 11:15:57 -0300 round-38 wave-1 dispatch + scorecard/log records
b6c1d3124555d7d4c38bc467d85d5efa4a65c053 2026-10-25 11:12:28 -0300 round-38 manifest fix: c1-duprow inserts inside Registry table, c2-docconn updates receipt sha; discrimination 19/19 TARGET_MET
859d0cf2911ae9679fbb5cd150c8aff4c96ee643 2026-10-25 11:10:19 -0300 round-38 c1 v3 repair: clause c enforces unique registry rows per id (c1-duprow crib was passing)
efb0ec234b6120a2d5051682f2d079b23118472b 2026-10-25 11:09:01 -0300 round-38 data fix: drop legacy S-ids from r8 entry body (counter counts them as cited)
245065c58a0c34dff9890d2a5bb798a5f2681b6c 2026-10-25 11:08:33 -0300 round-38 data: three request-socket package entries re-grounded ...
58e55ec9e905c85fb5a794f9a51dc06cc16166ba 2026-10-25 09:40:37 -0300 round-38: freeze — v3 counters (M37-5 repairs), request-ground counter, discrimination manifest, opened-source receipts, live triplet, assimilation scratch
32c3ea3aa31ec33b30bdabc954cb193a3625a8dc 2026-10-25 09:57:41 -0300 considerthese: 2026-10-25 daily reflection
f6e3247f73152a39afb86066af48f3cedf95fb0a 2026-10-25 09:40:37 -0300 round-37 verifier spot-check (integrator, hyaku): non-author admit/reject
```

Author vs committer dates (`git show -s --format='%h | author %ad | commit %cd'`):

```
58e55ec | author 2026-10-25 09:40:37 -0300 | commit 2026-10-25 11:06:33 -0300 | round-38: freeze ...
32c3ea3 | author 2026-10-25 09:57:41 -0300 | commit 2026-10-25 09:57:41 -0300 | considerthese: 2026-10-25 daily reflection
f6e3247 | author 2026-10-25 09:40:37 -0300 | commit 2026-10-25 09:40:37 -0300 | round-37 verifier spot-check ...
```

### Freeze tree (git ls-tree -r --name-only 58e55ec9 -- .ufo/waves/round-38)

```
.ufo/waves/round-38/assimilation/{collisions,quarantine-slice,reg-ids,staged-ids}
.ufo/waves/round-38/controls/manifest.json
.ufo/waves/round-38/fetch/{S158,S187,S221,S253,S277}.bin, fetch/stat-sockets.txt
.ufo/waves/round-38/receipts/{axis-base,before-c2,before-discrimination-v2,census-before,eventq-live-proc,eventq-live-ss,eventq-live}.txt
.ufo/waves/round-38/registration.md
```

Counters at the freeze (`git ls-tree 58e55ec9 -- quality/`): `quality/check-r38-discrimination.py`,
`quality/counters/c1-r38-event-ground.py`, `quality/counters/c2-r38-eventq.py`,
`quality/counters/c2-r38-request-ground.py` — all present.

Counter input paths pinned in the freeze blobs match the committed files:
`c2-r38-eventq.py:59-61` → `receipts/eventq-live.txt`, `eventq-live-ss.txt`, `eventq-live-proc.txt`;
`c2-r38-request-ground.py:64-74` → `fetch/S158.bin … S277.bin, stat-sockets.txt`.

### Per-file history under .ufo/waves/round-38 (git log -- <file>)

`fetch/` (all six files), `receipts/eventq-live.txt`, `eventq-live-ss.txt`, `eventq-live-proc.txt`,
`registration.md`: touched **only** by `58e55ec` (freeze). Never modified after.
`controls/manifest.json`: `58e55ec` then **`b6c1d31` (11:12:28, after the data commit 11:08:33)**.

`git diff --stat 58e55ec9 HEAD -- .ufo/waves/round-38`:

```
 .ufo/waves/round-38/controls/manifest.json         | 353 ++++++++++++-----
 .../round-38/receipts/after-discrimination-v3.txt  |  20 +
 .ufo/waves/round-38/w1-dispatch.json               | 428 +++++++++++++++++
 .ufo/waves/round-38/w1-spec.json                   | 182 ++++++++++
```

`registration.md` diff freeze→HEAD: empty (unchanged). Working tree: `?? .ufo/waves/round-38/w1/` only.

### The two post-freeze instrument changes

`859d0cf` diff (quality/counters/c1-r38-event-ground.py, @@ -199,8 +199,11 @@):

```
-            any(len(r) == 11 and r[7] == "mined" and path in [u.strip() for u in r[10].split(",")]
-                for r in rows.get(i, []))
+            # registry rows are unique per id and must bind the entry in used-by
+            len(rows.get(i, [])) == 1 and (
+                lambda r: len(r) == 11 and r[7] == "mined"
+                          and path in [u.strip() for u in r[10].split(",")]
+            )(rows[i][0])
```

`b6c1d31` manifest diff (JSON-parsed control comparison, 19 controls both revisions): only
`c1-duprow` changed — write op `append` (duplicate S189 row appended at end of SOURCES.md,
outside the Registry table) → `py` insert immediately after the `| S217 |` row (inside the
table). `c2-docconn` is byte-identical freeze→HEAD (its "updates receipt sha" in the commit
message describes the control's own runtime write op, not a manifest edit).

### Registration freeze contract (58e55ec9:.ufo/waves/round-38/registration.md, lines 4-7)

> This file, the three counters, the discrimination gate and its frozen manifest, the fetch
> receipts, the live triplet and the assimilation scratch land in one freeze commit; any later
> change to a counter is a new predicate and the claim it belongs to then fails as declared.

### Receipts

`before-discrimination-v2.txt` (at freeze) ends: `MADO_R38_DISCRIMINATION: controls=19 correct=13/19 verdict=TARGET_MISSED`.
`after-discrimination-v3.txt` (added in `b6c1d31`, i.e. after both patches) ends:
`MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET`. Neither receipt records
a rev, manifest sha, or counter sha.

### Digest spot-checks (both match)

- Added GATE line at freeze (`corpus/lessons/round-37.md`): `GATE S217 receipt=.ufo/waves/round-37/fetch/S217.bin sha256=aeb07ba1…78fe` — `git show 58e55ec9:.ufo/waves/round-37/fetch/S217.bin | sha256sum` → `aeb07ba1ba1fd5cfdb75aaf7434910c887096c24952f1a6788f71a4d7dbe78fe`.
- `c2-r38-request-ground.py` S253 pin `3ba8e461…d6cf` — `git show 58e55ec9:.ufo/waves/round-38/fetch/S253.bin | sha256sum` → `3ba8e461bd466a8a716a7a29a2a917d94a4d9af6fb87904a2c76978f4833d6cf`.

## Findings

### PASS

- **P1 — freeze precedes all data commits (DAG).** Committer dates: freeze `11:06:33` < data
  `11:08:33` (`245065c`) < `efb0ec2` < `859d0cf` < `b6c1d31` < `f0c9432`. `git log -3 -- .ufo/waves/round-38`
  = `f0c9432, b6c1d31, 58e55ec` — no other commit touched the wave dir.
- **P2 — freeze completeness.** registration.md, all three counters, the discrimination checker,
  the 19-control manifest, six fetch receipts, the live triplet (3 files) and assimilation scratch
  are all in `58e55ec9` (24 files, +12556). Counter path constants reference exactly those paths.
- **P3 — fetch receipts + live triplet committed at the freeze and never modified after.** Per-file
  history: only `58e55ec`. The counters' needs are satisfied at the freeze.
- **P4 — registration.md unchanged since freeze; working tree clean** (only untracked `w1/`).
- **P5 — digest bindings spot-checked honest** (S217 GATE line, S253 pin).

### FAIL / findings

- **F1 (major) — post-freeze counter change breaches the registration's own freeze contract, and
  the failure was never declared.** registration.md lines 6-7: "any later change to a counter is a
  new predicate and the claim it belongs to then fails as declared." `859d0cf` (11:10:19, after the
  freeze and after the data commit) changed `quality/counters/c1-r38-event-ground.py` clause c
  (unique-registry-row requirement, diff above). Per the frozen contract the C1 claim then **fails
  as declared**; instead the round re-scored with the patched counter and claims TARGET_MET
  (SCORECARD row 38 calibration). No record declares the C1 miss: `git grep '859d0cf\|c1 v3 repair\|clause c' HEAD -- LOG.md SCORECARD.md` → no hits.
- **F2 (major) — the "frozen" manifest was rewritten after the data commit while keeping its
  frozen identity.** `b6c1d31` (11:12:28 > data 11:08:33) modified `.ufo/waves/round-38/controls/manifest.json`
  (c1-duprow crib: out-of-table append → in-table insert). HEAD manifest still carries
  `"id": "MANIFEST-r38-v1"`, `"frozen_at": "2026-10-25"`, note "Frozen before the round-38 data
  commit." — false for the HEAD content. The manifest is a named part of the C1 predicate
  (registration line 39-40), so the predicate was altered on both sides post-freeze.
- **F3 (moderate) — the landed 19/19 is unreachable with the frozen pair; the scorecard attributes
  it to the frozen manifest.** With the frozen counter the c1-duprow crib passed (859d0cf message:
  "(c1-duprow crib was passing)") → 18/19 → the C1 kill rule ("anything other than correct=19/19 …
  is a miss, reported as an honest stop") fired at the freeze. With the frozen crib the patched
  counter also still passes it (out-of-table row is not parsed as a registry row). Only the
  post-freeze counter patch **and** crib fix together yield 19/19. SCORECARD row 38 says "frozen
  19-control manifest discriminates v2 13/19 → v3 19/19" — the manifest that produced 19/19 is the
  patched one, not the frozen one.
- **F4 (moderate) — LOG.md omits the counter-repair commit.** The round-38 LOG section records
  freeze `58e55ec`, data `245065c`/`efb0ec2`, "Manifest/receipts fix `b6c1d31`", wave 1 — but not
  `859d0cf` (the c1 counter patch). The chain record is incomplete for the exact change F1 turns on.
- **F5 (minor) — predicate id unchanged across a code change.** `PRED-C1-r38-v3` (c1 counter line 51)
  is identical at freeze and HEAD although the clause-c code differs — a changed predicate kept
  under the same id, which the registration itself calls "a new predicate".
- **F6 (minor) — the freeze commit contains an undeclared corpus edit.** `58e55ec9` adds one line to
  `corpus/lessons/round-37.md` (`GATE S217 … sha256=aeb07ba1…`, needed by c1's pin-binding; digest
  verifies). The registration's freeze contents list (lines 4-6) does not declare a round-37 lesson
  edit. Content is honest; the freeze manifest-of-contents is incomplete.
- **F7 (observation) — freeze timestamps are rebased, not wall-clock.** Freeze author date
  `09:40:37` is identical to the second with base `f6e3247`'s author date and *earlier* than its own
  parent's author date (`32c3ea3`, `09:57:41`); committer date `11:06:33`. The freeze was
  cherry-picked/rebased and landed 2m56s before the first data commit. DAG-order claims hold;
  any "frozen at 09:40" wall-clock reading does not.
- **F8 (minor) — discrimination receipts carry no provenance.** `before/after-discrimination-*.txt`
  record only control lines + verdict; no rev, manifest sha, or counter sha. The 19/19 receipt
  cannot itself prove which instrument revisions produced it (commit adjacency implies the patched
  pair).

### On "is registration.md's frozen_at honest?"

registration.md contains **no `frozen_at` field**; its honesty claim is structural ("frozen before
any round-38 data", base `f6e3247f`). That structural claim holds in DAG terms: the freeze commit
precedes the data commits and contains no round-38 corpus data (its only corpus touch is the
round-37 GATE S217 line, F6). The only `frozen_at` in the round is the manifest's (`2026-10-25`,
date-only) — honest at the freeze, **false at HEAD** after the post-data rewrite (F2).

## Residual risk and verification gaps

- I did not re-run the counters or the discrimination replay (other seats own those); F3's
  18/19-at-freeze inference rests on the 859d0cf commit message plus the crib/counter mechanics,
  not on a replay of the frozen pair. A sandbox replay of frozen-counter × frozen-manifest would
  close it.
- Whether the post-freeze repairs were sanctioned by a re-registration I could not find; if one
  exists outside LOG.md/SCORECARD.md/git history, F1/F2 soften to "undeclared", not "breached".
- Live-triplet content truthfulness (ss/proc consistency) is another seat's assignment; I verified
  presence, paths, and immutability only.
