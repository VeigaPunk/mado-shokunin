# RevCensusBefore — round-38 before-state census (mado 38, wave 1)

Reviewer: `L1Mado38.RevCensusBefore` (leaf; no subagents). Bounds honored: READ-ONLY on every
lane production file; only this report (and scratch under `/tmp/mado38-RevCensusBefore/`)
written. No git writes in LANE; no socket connects; no `model` value; no agents spawned.
No tools installed (nothing beyond the repo's own python3/git was needed).

## Verbatim before-state re-run (item 1) — PASS / identical

Command re-run verbatim as assigned:

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r38-request-ground.py --repo . --rev f6e3247f73152a39afb86066af48f3cedf95fb0a
```

rc=1; stdout (4 lines, stderr empty):

```
PRED-C2-r38-v1 entry=corpus/knowledge/hyprctl-flags-r28.md a=0 b=0 c=0 d=0 e=0 f=0 g=0 l=0 ids=- lineage=0/3 ok=0
PRED-C2-r38-v1 entry=corpus/knowledge/request-socket-live-bound-r8.md a=0 b=0 c=0 d=0 e=0 f=0 g=0 l=0 ids=- lineage=0/3 ok=0
PRED-C2-r38-v1 entry=corpus/knowledge/request-limits-upstream-r31.md a=0 b=0 c=0 d=0 e=0 f=0 g=0 l=0 ids=- lineage=0/3 ok=0
PRED-C2-r38-v1 admitted=0/3 verdict=TARGET_MISSED rev=f6e3247f73152a39afb86066af48f3cedf95fb0a base=f6e3247f73152a39afb86066af48f3cedf95fb0a
```

`diff <(sed -n '1,4p' <rerun stdout>) <(sed -n '1,4p' .ufo/waves/round-38/receipts/before-c2.txt)` → **IDENTICAL lines1-4**. The receipt's 5th line is `exit=1`, matching the run's rc=1 (the receipt capture appended the exit code). PASS.

## Counter verdicts at the two base revs (item 2) — all honest TARGET_MISSED

Notation: `--base` default is `b4e47e98…` for the c1/c2 counters, `f6e3247…` for the
request-ground counter (see `BASE_DEFAULT` in each file).

### `c1-r38-event-ground.py` (PRED-C1-r38-v3)

At `b4e47e980bfb0cbc8a4e788f59a41db858751fd8` (round-36 base; default base = same rev),
rc=1:

```
PRED-C1-r38-v3 entry=corpus/knowledge/event-delivery-limits-r26.md a=0 b=0 c=0 d=0 e=0 f=0 g=0 h=0 j=0 k=0 l=0 ids=- lineage=0/4 ok=0
PRED-C1-r38-v3 entry=corpus/knowledge/event-queue-observability-r37.md a=0 b=0 c=0 d=0 e=0 f=0 g=0 h=0 j=0 k=0 l=0 ids=- lineage=0/2 ok=0
PRED-C1-r38-v3 admitted=0/2 verdict=TARGET_MISSED rev=b4e47e980bfb0cbc8a4e788f59a41db858751fd8 base=b4e47e980bfb0cbc8a4e788f59a41db858751fd8
```

At `f6e3247…` (round-38 base; default base still `b4e47e98…`), rc=1:

```
PRED-C1-r38-v3 entry=corpus/knowledge/event-delivery-limits-r26.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 h=1 j=1 k=1 l=1 ids=S189,S201,S212 lineage=6/4 ok=1
PRED-C1-r38-v3 entry=corpus/knowledge/event-queue-observability-r37.md a=1 b=1 c=1 d=0 e=1 f=1 g=0 h=0 j=1 k=1 l=1 ids=S189,S213,S214,S215,S216,S217 lineage=2/2 ok=0
PRED-C1-r38-v3 admitted=1/2 verdict=TARGET_MISSED rev=f6e3247f73152a39afb86066af48f3cedf95fb0a base=b4e47e980bfb0cbc8a4e788f59a41db858751fd8
```

The overall verdict is an honest miss (report summary is `admitted=1/2 verdict=TARGET_MISSED`,
rc=1). Note: the counter itself (not just the summary) is honest — the r26 entry legitimately
passes at the round-38 base because its ground (entry + registry rows S189/S201/S212 with
gate pins) already existed at `f6e3247` (round-37-era ground), which is expected for a
calibration/regression instrument; the r37 entry fails exactly where the round-38 pin table
(`.ufo/waves/round-38/fetch/`) is absent at base (d=0, g=0, h=0).
With `--base` pinned to itself (`f6e3247`), the counter reports the honest SETUP refusal
`ground_held_at_base` (rc=2): the counter refuses to run when the base rev already holds any
target token — the same guard that trips when `--rev` is a data rev with a non-data base.

### `c2-r38-eventq.py` (PRED-C2-r38-v3)

At `b4e47e98…`, rc=1: `fixtures=0/14 readonly=0 live=0 tool=absent verdict=TARGET_MISSED`
(14/14 cases `rc=None`, tool absent from that rev — `tools/mado-eventq.py` entered later).
At `f6e3247…`, rc=1: `fixtures=14/14 readonly=1 live=0 tool=present verdict=TARGET_MISSED`
with `live-detail artifacts-missing` (the live triplet receipts do not exist at base;
fixtures pass only because they exercise the tool's behavior, not the round's data). Honest
misses in both.

### `c2-r38-request-ground.py` (PRED-C2-r38-v1)

At `b4e47e98…`, rc=1: `admitted=0/3 verdict=TARGET_MISSED` (all entries absent at that rev).
At `f6e3247…` — the receipt run reproduced above (0/3). Both honest.

## Freeze order (item 3) — PASS, with one errata-visible nuance

`git log -5 --format='%H %ad %s' --date=iso` (current HEAD):

```
3f14bd2d7c3aa067091bc52e63fb8abdd944c3b8 2026-10-25 11:18:41 -0300 round-38 errata: RevCommitChain F1-F3 — post-freeze counter/manifest patches mean the frozen claim fails as declared (18/19); 19/19 is a new predicate routed to closure
bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5 2026-10-25 11:16:06 -0300 round-38 scorecard: move-log rows + capabilities section (round-38 table, not the rollout snapshot)
f0c9432a84662478ae2215c783be16c8f4d208cd 2026-10-25 11:15:57 -0300 round-38 wave-1 dispatch + scorecard/log records
b6c1d3124555d7d4c38bc467d85d5efa4a65c053 2026-10-25 11:12:28 -0300 round-38 manifest fix: c1-duprow inserts inside Registry table, c2-docconn updates receipt sha; discrimination 19/19 TARGET_MET
859d0cf2911ae9679fbb5cd150c8aff4c96ee643 2026-10-25 11:10:19 -0300 round-38 c1 v3 repair: clause c enforces unique registry rows per id (c1-duprow crib was passing)
```

Freeze commit is `58e55ec9e905c85fb5a794f9a51dc06cc16166ba` (2026-10-25 09:40:37 -0300):
`round-38: freeze — v3 counters (M37-5 repairs), request-ground counter, discrimination manifest, opened-source receipts, live triplet, assimilation scratch`.
Its parent chain: `58e55ec9` ← `32c3ea3` (considerthese daily reflection, 09:57) ←
`f6e3247` (the round-38 base). `git merge-base --is-ancestor f6e3247… 58e55ec9…` → yes.
All three data entries are **absent at the freeze commit**:

```
git ls-tree 58e55ec9 -r --name-only | grep -E 'hyprctl-flags-r28|request-socket-live-bound-r8|request-limits-upstream-r31'   →  (no match; grep exit 1)
git ls-tree f6e3247 -r --name-only | grep -E '…'   →  (no match)
```

and are present at HEAD (`corpus/knowledge/{hyprctl-flags-r28,request-socket-live-bound-r8,request-limits-upstream-r31}.md`). Their add-commit is `245065c` (11:08:33, "round-38 data: three request-socket package entries re-grounded…"), i.e. the freeze predates every round-38 data file. PASS.

Errata-visible nuance (the freeze is *not* the current snapshot): the errata commit
`3f14bd2` (11:18:41) states plainly that **post-freeze counter/manifest patches mean the
frozen claim fails as declared (18/19); 19/19 is a new predicate routed to closure** — i.e.
at HEAD the 19/19 discrimination/TARGET_MET runs against *patched* instruments, not the
frozen ones. This is confirmed by direct measurement (below). The errata itself does not
modify the instruments; it only records that finding (git show `3f14bd2` touches only
`w1/reports/RevCommitChain.md`, `RevLiveTriplet.md`, `swarm-registry.json`, `LOG.md`).

## Additional evidence gathered (finding)

- **Frozen-instrument discrimination at the freeze rev, using the manifest as committed at the freeze, scores 19/19** (`controls=19 correct=19/19 verdict=TARGET_MET`, rc=0). So the *claim as frozen at 58e55ec9* was internally coherent: the frozen instruments accepted the frozen manifest's 19 controls against the freeze's own (data-less) rev.
- **HEAD instruments against the frozen manifest score 18/19** (rc=1), failing `c1-duprow` (`expected=TARGET_MISSED observed=TARGET_MET`) — the frozen crib writes a second S189 row via `append`; the current c1's tightened clause c (unique `len(rows.get(i,[]))==1`) finds exactly two S189 rows and admits, leaving the crib un-discriminated.
- **The manifest itself is frozen-identity only:** `id: MANIFEST-r38-v1`, `frozen_at: 2026-10-25`, 19 controls at both the freeze and HEAD, but the control bodies were rewritten (freeze→HEAD diff: manifest +353 lines; `c1-duprow` moved from `append` to a `py` write inserting before the S217 row; `c2` control writes gained `path` fields). The C1 counter differs freeze→HEAD (+7/-2: clause c, `r[10]` used-by, `len(...)==1`); `check-r38-discrimination.py` differs (+45: sandbox confinement, py-control writes per the build); `c2-r38-eventq.py` and `c2-r38-request-ground.py` are byte-identical freeze→HEAD. Hence the manifest the current 19/19 runs against is a different control set than the frozen manifest — consistent with the errata, and an   of the (falsification) rule in registration.md: *"any later change to a counter is a new predicate and the claim it belongs to then fails as declared"* — the frozen claim did fail as declared (18/19), and 19/19 is a later predicate.
- The acceptance/negative outputs quoted above are all direct console bytes; no output was inferred. LANE remained untouched by these runs: `git status --porcelain` at the end shows only pre-existing wave-1 workspace entries (`M quality/check-r38-discrimination.py` — working-tree modification present before this census, from the wave-1 sandbox confinement fix; `?? .ufo/waves/round-38/w1/…`), and no new files under any other path.

## Summary

| Item | Result |
|---|---|
| Verbatim before-state re-run vs `receipts/before-c2.txt` | PASS (identical lines 1-4; rc=1 = receipt's `exit=1`) |
| c1-r38 at `b4e47e98` / `f6e3247` | TARGET_MISSED (0/2, 1/2) — honest |
| c2-r38-eventq at `b4e47e98` / `f6e3247` | TARGET_MISSED (0/14, 14/14 live=0) — honest |
| request-ground at `b4e47e98` / `f6e3247` | TARGET_MISSED (0/3, 0/3) — honest |
| Freeze `58e55ec9` predates the three data entries | PASS (absent at freeze and at base; added in `245065c`; freeze's parent is the round-38 base `f6e3247`) |
| Frozen instruments × frozen manifest at freeze rev | 19/19 TARGET_MET (the frozen claim as frozen) |
| HEAD instruments × frozen manifest | 18/19, fails `c1-duprow` — matching the errata (frozen claim fails as declared) |

Residual risk / verification gaps: (1) freeze vs HEAD definitions of `c1-duprow` and the
two other rewritten controls could be diffed mechanically if any later reviewer needs proof
that the current manifest's control bodies are exactly the patched ones; (2) the live
triplet receipts (C3) were not re-verified here — they are `RevLiveTriplet`'s scope (the
HEAD full run passed `live=1` with `proc=3/3`); (3) I did not run the counters against any
post-freeze data rev other than HEAD/`6c1d31`-style canonical calls — earlier `b6c1d31`
vs `f6e3247` request-ground runs (3/3, rc=0) are recorded in `/tmp` scratch.

## Privacy

No raw journal lines or window titles were captured or quoted; only counter verdict lines and
commit metadata appear in this report.
