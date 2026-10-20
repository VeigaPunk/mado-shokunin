# AttackSeparability — replay separability of C1/C2/C3, falsification attempt

Scope: whether each round-17 claim moves **only** with its own commit. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, lane HEAD
`988b858bd6049bc709807534fd725c05264f7e60`. Method: fresh `--no-hardlinks` clones under
`/tmp`, single-commit reverts of `3722ba4` (C1), `a9998d1` (C2), `988b858` (C3), reversed
in both directions (revert-from-HEAD and cherry-pick-onto-base), re-measured with
`.ufo/waves/round-17/measure.py` and the tripwire selftests. Read-only w.r.t. the lane; no
git mutation in the lane, no installs (**install: none**), no host probes, no
`pacman`/`systemctl`/`hyprctl` execution.

## Verdict

**The attack failed.** In every construction the three measured quantities form a clean
diagonal: reverting C1 moves only `c1`, reverting C2 moves only `c2`, reverting C3 moves
only `c3`. The forward direction agrees (C1 alone on the pre-C1 base reaches 15/23; the C3
tool alone on the pre-C3 base sets `c3` present). No cross-claim contamination, no
offsetting pair, no hidden second mover was found. Two structural caveats follow
(one Low, one Info) that concern commit independence and artifact placement, not the
measured claims.

## 1. Single-commit reverts from HEAD (the requested test)

Each revert was a real `git revert` commit in its own clone. C1 reverts with one
modify/delete conflict (finding A1); the state used here is the resolved revert, and its
tree is byte-identical to the resolved probe tree (`51e3d748…`, §4).

| state | clone HEAD | c1 `lesson_cited/criteria` | c2 provinces | c3 tool |
|---|---|---|---|---|
| HEAD (`988b858`) | — | **15/23** = 6.5217 | **4/6** = 6.6667 (P1,P2,P4,P6) | present `4ced68d3…` |
| HEAD − C1 | `345f54d6` | **14/22** = 6.3636 | 4/6 (P1,P2,P4,P6) | present `4ced68d3…` |
| HEAD − C2 | `770fa700` | 15/23 = 6.5217 | **2/6** = 3.3333 (P1,P2) | present `4ced68d3…` |
| HEAD − C3 | `792c56c1` | 15/23 = 6.5217 | 4/6 (P1,P2,P4,P6) | **absent** (`tool_present:false`) |

Each revert removes exactly its own claim and leaves the other two at HEAD values. The
`−C2` state credits P1/P2 via the pinned legacy rows (`U1`,`U2`→P1; `U7`→P2) and nothing
else; the `−C1` state's P4/P6 credit is still carried by `terminal-route-r17.md`
(S056–S060) and `idle-lock-route-r17.md` (S063–S069).

## 2. Cumulative chain — no third mover

`python3 .ufo/waves/round-17/measure.py REV` over the whole round-17 chain. Moves occur
exactly at the owning commits and nowhere else:

| REV | commit subject | c1 | c2 | c3 |
|---|---|---|---|---|
| `0175f13` | pre-register claims | 14/22 | 2/6 | absent |
| `f52f43f` | bind measure instrument | 14/22 | 2/6 | absent |
| `ab0bc9b` | tighten instrument | 14/22 | 2/6 | absent |
| `a9998d1` | **C2** | 14/22 | **4/6** | absent |
| `fc6f960` | wave-1 evidence | 14/22 | 4/6 | absent |
| `245fd11` | label fixture | 14/22 | 4/6 | absent |
| `3722ba4` | **C1** | **15/23** | 4/6 | absent |
| `3e9848a` | corrections | 15/23 | 4/6 | absent |
| `988b858` | **C3** | 15/23 | 4/6 | **present** |

The evidence commit `fc6f960` and the correction commit `3e9848a` move nothing, so the
receipts do not smuggle claim movement in either direction. `u_routes` = 7
(`U1..U7`) and `rejected` = 0 in **all twelve** measured states (9 chain + 3 reverts) —
the harm watch does not budge under any revert.

## 3. Forward direction — each commit alone on the pre-claim base

Complementary to the reverts, so the diagonal is not an artifact of undo order:

- `ab0bc9b` + cherry-pick `3722ba4` (C1 alone, C2 absent): c1 **15/23**, c2 2/6, c3 absent.
- `ab0bc9b` + only `tools/mado-tripwire.py` from `988b858` (C3 capability alone, C1 and C2
  absent): c1 14/22, c2 2/6, c3 **present**, sha `4ced68d33ad4…`.

C2 needs no such test: its parent is `ab0bc9b`, i.e. `a9998d1` *is* base+C2, measured in §2.

## 4. Instrument fidelity (so the diagonal is not an instrument illusion)

- `measure.py` bytes are identical, sha256 `4023124f…`, at `ab0bc9b`, `a9998d1`,
  `fc6f960`, `3722ba4`, `3e9848a`, `988b858` — every before/after pair above is read by
  one instrument.
- The pre-tightening instrument (`f52f43f`, sha256 `a280b3ab…`) independently reports
  14/22, 2/6 at `ab0bc9b` and 14/22, **4/6** at `a9998d1`: C2's movement exists under both
  instrument versions, so it is not a tightening artifact.
- The counter is revision-bound: appending a fabricated `99. … lessons/` line to the
  clone's working-tree `corpus/QUALITY.md` changed nothing (`c1` stayed 15/23); only
  `git show REV:` bytes are read.
- Baseline receipt reproduces: `measure.py 27cd06f` output is byte-identical to committed
  `evidence/measure-before.json` (14/22 = 6.3636, 2/6 = 3.3333, `tool_present:false`).
- Independent c1 oracle: `git show HEAD:corpus/QUALITY.md | grep -cE '^[0-9]+\. '` → 23,
  `| grep -cE '^[0-9]+\. .*lessons/'` → 15. Criterion 23 is the only numbered line C1 adds
  and it carries `lessons/round-17.md#mistakes M1` on its own line.

## 5. C3 capability and receipts under the other reverts

- Tripwire selftests run in the `−C1` and `−C2` clones: `tripwire/core` **9/9**,
  `tripwire/compound` **16/16**, `tripwire/hardening` **33/33**, all exit 0,
  `SELFTEST_SCRIPT_SHA256: 4ced68d3…` — identical to HEAD. C3's capability does not depend
  on C1's QUALITY/label work or C2's routes.
- `−C3` state: `tools/mado-tripwire.py` absent and `evidence/tripwire-*` absent (0 C3 files
  in the tree); `c3.tool_present:false`, sha `null`. Nothing else in the tree supplies a
  tripwire.
- Anchor re-derived at HEAD (`--scan` of
  `…/2026-10-20T01-48-55-258Z_01a156ff…/MadoR15/MadoR15.LibinputEvents.jsonl`): exit **1**,
  counts `{host_mutation: 2, live_probe: 1, package_query: 5}` — exactly the committed
  `evidence/tripwire-anchor-r15.txt`. The line-54 findings are `sudo` and `pacman:-S` on
  `pacman -S --needed --noconfirm libinput libinput-tools`, and line 54 of that transcript
  contains `call_38165`.
- `pacman.log:2429` reads
  `[2026-10-20T04:25:16-0300] [PACMAN] Running 'pacman -S --needed --noconfirm libinput libinput-tools'`
  (= 07:25:16Z, matching the transcript timestamp); 2410/2422/2423 carry the other three
  joined transactions.
- C1's label check is stable across the other reverts: at HEAD, `−C2`, and `−C3` the output
  is byte-identical — `LABEL_SUMMARY: 4/7`, `EXPECT_SUMMARY: 7/7`, exit 1.

## Findings

### A1 — Low: C1 is not revert-clean; C3 edits a file C1 created

`git revert 3722ba4` fails deterministically:
`CONFLICT (modify/delete): corpus/lessons/round-17.md deleted in parent of 3722ba4 … and
modified in HEAD`. Everything else C1 touched reverts cleanly (probe status: staged `D`
for `label-check.py`, `label-claims.json`, `evidence/label-check.txt`, staged `M` for
`QUALITY.md` and `lessons/round-16.md`). The conflict exists because `988b858` (C3) adds
its M2 row and capability section into `corpus/lessons/round-17.md`, which only exists
because C1 created it. The resolved tree (`git add` keeping HEAD's file) is
`51e3d748dd8504b8a6146e5097643d94b0695de6`, identical to the hand-built `−C1` state.
Consequence: `SCORECARD.md:862` — "Separable: C1 counts QUALITY text only; C2 needs no
tool or criterion; C3 needs no note or criterion" — is true for the **counters** (proved
above) but overstates **commit-level** independence: C3 cannot be applied before C1, and a
naive LIFO unwind of the wave fails. This is a documentation/replay-order property, not a
claim movement; severity Low.

### A2 — Info: C3's commit ships a C1 receipt

`evidence/measure-c1.json` is added by `988b858`, not by `3722ba4`. Reverting C3 deletes
that receipt while `c1` remains 15/23. Receipt placement only — the measure never reads
`evidence/` — but a reader auditing C1's claim from "files added in C1" will not see its
own receipt.

### A3 — Info: label-check's exit 1 is expected-red, not failure

At HEAD the C1 checker prints `LABEL_SUMMARY: 4/7` (three declared-red rows) and
`EXPECT_SUMMARY: 7/7`, then exits **1**; the final line of `label-check.py` is
`return 1 if mismatch else 0`. `corpus/lessons/round-17.md` M1 documents "exit 1", and the
criterion text only requires `EXPECT_SUMMARY` 7/7. No defect — flagged only because
"runnable check" invites a green-exit reading that the receipt does not give.

## Residual risk and verification gaps

- The instrument is the lane's own `measure.py`. I cross-checked `c1` with an independent
  grep and `c2` with the pre-tightening instrument, but did not write a third-party c2
  implementation; the structural rules (surface token, pinned legacy net, upstream-https
  keyword) are taken as read. Content accuracy of S056–S070 and the two entries is out of
  scope (Reopen seats).
- `c2` counts provinces, so separability is proved at province granularity; whether one
  entry alone carries a province is a property of the instrument, not attacked here.
- The 4/4 pacman join: I verified the pacman.log side (all four cited lines) and re-derived
  the r15 anchor; the r13/r14 transcript endpoints were not independently re-scanned in
  this item (AnchorRerun peer's scope).
- Selftest totals are the tool's own `expected.json` verdicts; the outer oracle
  (expected.json correctness) is not audited here (SelftestRerun peer's scope).
- Revert orders other than LIFO were not exercised beyond the cherry-pick forward tests in
  §3; C2-before-C1 is the lane's actual order, so the remaining permutation (revert C1
  then C3) reduces to A1's resolved tree.
