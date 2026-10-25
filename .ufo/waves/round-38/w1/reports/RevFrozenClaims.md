# RevFrozenClaims — round 38 wave 1: frozen claims vs delivered bytes

Reviewer: L1Mado38.RevFrozenClaims (leaf, no subagents). Date: 2026-10-25.
Scope: verify the registration's three frozen claim specs and kill rules
(`.ufo/waves/round-38/registration.md`, frozen at `58e55ec9e905c85fb5a794f9a51dc06cc16166ba`)
against the delivered work, clause by clause: run each counter's before/after pair
verbatim (before at base `f6e3247f73152a39afb86066af48f3cedf95fb0a`, after at the lane
tip), confirm verdict letters, check the do-nothing controls, report over/under-delivery.

Revs named below (full shas): base `f6e3247f…`, freeze `58e55ec9e905…`, data `245065c58a0c…`,
data-fix `efb0ec234b61…`, counter-patch `859d0cf2911a…`, manifest-patch `b6c1d3124555…`
(tip when review started), records `23a0e0f91e03…` (tip when review ended — the lane moved
mid-review; every number below is pinned to a named rev).

No tool installs were needed (none performed). Scratch: `/tmp/mado38-RevFrozenClaims/`
(frozen counter/manifest blobs extracted with `git show <rev>:<path>`). The lane working
tree was never mutated; all runs are `git show`/sandbox-clone readers.

---

## Verdict summary

| Claim | Frozen promise | Delivered (measured) | Verdict letters | Finding |
|---|---|---|---|---|
| C1 calibration (discrimination) | before: v2 counters `correct<19 TARGET_MISSED exit 1`; target: v3 `correct=19/19 TARGET_MET exit 0` | before **13/19 TARGET_MISSED exit 1**; after **19/19 TARGET_MET exit 0** | match | **FAIL AS DECLARED** — F1/F2: the instrument and the frozen manifest were patched post-freeze; the frozen bytes never scored 19/19 at any rev |
| C1 ground counter (standalone) | "0→2/2" (ticket framing) | before **admitted=1/2 TARGET_MISSED exit 1**; after **2/2 TARGET_MET exit 0** | letters match, count does not | F4: before is 1/2, not 0/2 — the r26 entry already passed every v3 clause at base |
| C2 operability (eventq) | "0→14/14+triplet" | before `fixtures=14/14 readonly=1 live=0 artifacts-missing → TARGET_MISSED exit 1`; after `14/14 readonly=1 live=1 → TARGET_MET exit 0` | match | F5 nuance: fixtures already 14/14 at base; before-MISSED rides solely on the missing live triplet |
| Domain coverage (request-ground) | before `admitted=0/3 TARGET_MISSED exit 1`; target `3/3 TARGET_MET exit 0` | exactly that, at `b6c1d31` **and** at tip `23a0e0f` | match | **CLEAN** — no over- or under-delivery found |
| Do-nothing controls | reject | `c1-donothing` MISSED, `c2-donothing` MISSED (all 5 gate runs); domain do-nothing = base run 0/3 MISSED | match | PASS |

---

## Findings by severity

### F1 — HIGH — C1's claim fails as declared under the registration's own freeze rule

The registration freezes: *"This file, the three counters, the discrimination gate and its
frozen manifest, the fetch receipts, the live triplet and the assimilation scratch land in
one freeze commit; **any later change to a counter is a new predicate and the claim it
belongs to then fails as declared**."*

Delivered history contradicts this for three freeze-listed files, all AFTER the freeze
commit `58e55ec9` and AFTER the data commits `245065c`/`efb0ec2`:

- `859d0cf` — `quality/counters/c1-r38-event-ground.py`, +5/−2: clause c gains
  `len(rows.get(i, [])) == 1` uniqueness (`c1-r38-event-ground.py:201-206` at HEAD).
  Commit message: *"c1-duprow crib was passing"* — an admission that the frozen instrument
  did not meet the frozen target.
- `b6c1d31` — `.ufo/waves/round-38/controls/manifest.json`, 353 lines rewritten
  (wholesale reformat + one substantive change: `c1-duprow` write op `append` at EOF →
  `py` insert inside the `## Registry` table). The manifest still carries
  `"frozen_at": "2026-10-25"` and the note *"Frozen before the round-38 data commit"* —
  false for the delivered bytes (the rewrite is post-data).
- `23a0e0f` — `quality/check-r38-discrimination.py`, 45 lines (sandbox-confinement
  hardening: `_confine()`, env pruning, clone flags). Scoring logic unchanged
  (19/19 before and after — see evidence), but the gate is also a freeze-listed file.

By the frozen kill rule, C1's claim is a **new predicate at HEAD** and *"fails as
declared"*. The lane discloses this honestly (`corpus/lessons/round-38.md:76-82`:
*"Freeze-discipline failure (RevCommitChain F1-F3): the C1 counter (859d0cf) and the
discrimination manifest (b6c1d31) were patched after the freeze"*), and a "re-registration
ruling" is cited as covering it — but the frozen registration text contains no such
carve-out, so the as-frozen verdict stands: **C1 = miss, as declared.**

### F2 — HIGH — the frozen bytes never met the frozen target at any revision

The claim as frozen promises *"the v3 counters score `correct=19/19 verdict=TARGET_MET`"*.
Replays of the frozen pair (manifest+counter blobs extracted from `58e55ec`, run under the
current gate, which the diff shows changed only confinement):

```
# REPLAY A — frozen manifest × frozen c1 counter, data rev efb0ec2
control=c1-duprow instrument=c1 expected=TARGET_MISSED observed=TARGET_MET ok=0
MADO_R38_DISCRIMINATION: controls=19 correct=18/19 verdict=TARGET_MISSED   (exit 1)

# REPLAY B — frozen manifest × c1 counter at b6c1d31 (post-859d0cf), same data rev
control=c1-duprow instrument=c1 expected=TARGET_MISSED observed=TARGET_MET ok=0
MADO_R38_DISCRIMINATION: controls=19 correct=18/19 verdict=TARGET_MISSED   (exit 1)

# REPLAY C — frozen manifest × frozen c1 counter, AT the freeze rev 58e55ec9…
control=c1-duprow instrument=c1 expected=TARGET_MISSED observed=TARGET_MET ok=0
MADO_R38_DISCRIMINATION: controls=19 correct=18/19 verdict=TARGET_MISSED
```

Replay B proves the counter fix alone was insufficient; only the joint counter+control
retune reaches 19/19. This is a two-file post-freeze co-edit against a discovered failure —
exactly what the freeze rule declares a miss.

### F3 — HIGH — the lane's freeze-coherence record is factually wrong

`LOG.md` (tail, RevCensusBefore entry) and `corpus/lessons/round-38.md:78-82` record:
*"direct replay at the freeze rev `58e55ec9` shows frozen instruments × frozen manifest =
**19/19**: the claim as frozen was internally coherent (its `c1-duprow` append landed
outside `## Registry`)."*

My direct replay at that rev (Replay C) gives **18/19** with `c1-duprow … observed=TARGET_MET
ok=0`. The recorded number is impossible as described, and the record's own parenthetical
explains why: the frozen control appends the duplicate S189 row at EOF of
`corpus/SOURCES.md`, which is *after* `## Paths` (`:221` at `58e55ec`, `:225` at `efb0ec2`)
— outside the `## Registry` section that `registry_rows()` parses — so the frozen counter
can never see the crib, and the crib control necessarily fails. The only pairing that
yields 19/19 with the frozen counter is frozen-counter × **repaired** control (clause j's
uniqueness bites once the row is inside the section) — `[INFERENCE]` the recorded 19/19
came from that mixed pairing (repaired worktree manifest passed as "frozen"). The
"re-registration ruling" said to cover the manifest rewrite rests on this incorrect record
and should be re-derived.

### F4 — MEDIUM — C1's before side is 1/2, not 0/2 (over-stated repair delta)

```
# python3 -I quality/counters/c1-r38-event-ground.py --repo . --rev f6e3247…
PRED-C1-r38-v3 entry=corpus/knowledge/event-delivery-limits-r26.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 h=1 j=1 k=1 l=1 ids=S189,S201,S212 lineage=6/4 ok=1
PRED-C1-r38-v3 entry=corpus/knowledge/event-queue-observability-r37.md a=1 b=1 c=1 d=0 e=1 f=1 g=0 h=0 j=1 k=1 l=1 ids=S189,…,S217 lineage=2/2 ok=0
PRED-C1-r38-v3 admitted=1/2 verdict=TARGET_MISSED   (exit 1)
```

At the named base, the r26 entry passes **every** v3 clause — pin binding (h), quote floor
(i via d/g), unique rows (j), parsed headers (k), lineage 6/4 (l). The event entries are
untouched since base (`git log f6e3247..HEAD -- <both entries>` is empty), so the v3
repairs' real-corpus delta is confined to the r37 observability entry (whose base Gate
lines failed pin binding, h=0; repaired by the freeze commit's own `round-37.md` Gate
edit). Verdict letters (MISSED→MET) are correct; the "0" of "0→2/2" is not what the
instrument delivers under its only self-consistent base (default `--base b4e47e9…`;
`--base f6e3247` would make even the after-run 0/2 via clause a).

### F5 — LOW — C2 before-state nuance: 14/14 fixtures already pass at base

`git log` shows `tools/mado-eventq.py` unchanged since round-37 (`3f42425`). The before run
at `f6e3247` prints `fixtures=14/14 readonly=1 live=0` with `live-detail
artifacts-missing` — the four "new discriminating cases" exercise the tool's parser, which
already had those properties; v2's holes were in the v2 counter's fixture set. The
before-MISSED rides solely on the missing committed triplet. Verdict letters match the
frozen promise; no promise broken.

---

## What passed, with evidence (all commands run verbatim from the lane root)

**Discrimination before (frozen v2 counters, current manifest, `--rev b6c1d31…`):**
`python3 -I quality/check-r38-discrimination.py --c1 quality/counters/c1-r37-event-ground.py --c2 quality/counters/c2-r37-eventq.py --manifest .ufo/waves/round-38/controls/manifest.json --rev b6c1d3124555d7d4c38bc467d85d5efa4a65c053`
→ `controls=19 correct=13/19 verdict=TARGET_MISSED`, exit 1. Inaccurate controls:
`c1-duprow`, `c1-nolineage`, `c1-r28-verbatim` (observed MET), `c2-forged`, `c2-docconn`
(observed MISSED), `c2-proc-mismatch` (observed MET) — 13/19 matches the context claim and
matches `.ufo/waves/round-38/receipts/before-discrimination-v2.txt` line-for-line.

**Discrimination after (v3 counters, same command with v3 paths):** `controls=19
correct=19/19 verdict=TARGET_MET`, exit 0 — matches
`receipts/after-discrimination-v3.txt`. Re-confirmed at tip `23a0e0f` (`--rev 23a0e0f`):
19/19 again, now under the hardened gate.

**C1 counter:** before (above, F4) → after `--rev b6c1d31…`: `admitted=2/2
verdict=TARGET_MET`, exit 0; at tip `23a0e0f`: `admitted=2/2 verdict=TARGET_MET`, exit 0.

**C2 counter:** before `--rev f6e3247…`: `fixtures=14/14 readonly=1 live=0 tool=present
verdict=TARGET_MISSED`, exit 1 → after `--rev b6c1d31…`: `fixtures=14/14 readonly=1 live=1
tool=present verdict=TARGET_MET`, exit 0, `live-detail replay=1 sha=1 full_table=1 proc=3/3
sha_in=1 agree=1`; at tip `23a0e0f`: MET again.

**Domain counter:** before `--rev f6e3247…`: all three entries `a=0 … ok=0`,
`admitted=0/3 verdict=TARGET_MISSED`, exit 1 — byte-equivalent to the delivered
`receipts/before-c2.txt`. After `--rev b6c1d31…`: `admitted=3/3 verdict=TARGET_MET`, exit
0 (`hyprctl-flags-r28.md` ids=S221 lineage 3/3; `request-socket-live-bound-r8.md`
ids=S158,S187,S277 lineage 5/3; `request-limits-upstream-r31.md` ids=S253 lineage 5/3); at
tip `23a0e0f`: `admitted=3/3 verdict=TARGET_MET`, exit 0 (the tip's entry edits — S258
source line, reworded amends — keep every clause green). **This claim delivers exactly its
frozen wording.**

**Do-nothing controls:** `c1-donothing` (rev `b4e47e9…`, expect MISSED) and `c2-donothing`
(same) observed MISSED in all five gate runs (before, after, tip, Replays A/C); the domain
do-nothing control is the base run itself (0/3 MISSED, above). All correct.

**Other frozen wordings spot-checked:** v2 counters untouched since the round-37 re-freeze
`893a8aa` (*"v2 stays frozen beside it, never edited"* holds); `receipts/axis-base.txt`
matches the registration's quoted axis line (`navigation 52/52`, `calibration 50/50`,
`operability 12/12`, `MADO_AXIS: checked=3 mismatched=0 rev=f6e3247…`); manifest has 19
controls, same ids, at freeze and HEAD (only `c1-duprow` substantively changed — F1).

---

## Residual risk and verification gaps

- The declared fabrication residuals stand as written (consistent forged triplet; invented
  lineage phrases) — I did not attack them; that is MutC1/MutC2's seat. MutC2's LOG entry
  (six surviving clause mutants) further weakens the 19-control manifest's strength; the
  frozen "discriminates" claim is thinner than the letter `19/19` suggests.
- My discrimination runs all used the gate bytes present in the worktree during the run
  (post-`23a0e0f` hardening; the `b6c1d31`→`23a0e0f` gate diff shows confinement/env
  changes only, and the 19/19 result is version-invariant across my runs). I did not
  re-run the suite under the literal `b6c1d31` gate bytes.
- Replay C's process exit code was consumed by a `| grep` pipe; the quoted verdict line is
  the evidence (MISSED ⇒ exit 1 by construction). Replays A/B and the six counter runs
  captured exits directly.
- The lane is live: `23a0e0f` landed mid-review. All findings are rev-pinned; the tip
  re-checks (three counters + discrimination) all held.
- I did not re-derive the fetch receipts' digests against live sources (S221/S253/S277/
  S158/S187) — sourcing truth is other seats' scope; I verified only that the frozen pin
  table and committed receipts satisfy the counters.

**Bottom line:** domain claim CLEAN; C2 (eventq) letters clean with a nuance; C1's numbers
reproduce at HEAD but its claim fails as declared under the registration's own freeze rule
(F1), the frozen target was unreachable with the frozen bytes (F2), and the lane's record
of frozen-pair coherence at the freeze rev is falsified by direct replay (F3).
