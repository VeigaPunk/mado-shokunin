# Round-35 scorecard draft — NOT committed; apply-ready text

ScribeScorecard draft, measured 2026-10-24 against lane tip
`19e4ab3171c1540c40d6b12097745af98053b07d` (the freeze commit; an ancestor of
HEAD). `⟨…⟩` marks cells the integrator fills when the C1 data commit lands;
every printed value below was re-measured at write time. Nothing here was
copied from an earlier session's plan.

## Proposed section text

```markdown
## Round 35 — the clause ledger admits a ledger audit; the idle-lock offer surface waits for its data commit (2026-10-24, attempt 1)

Registration `.ufo/waves/round-35/registration.md` was frozen before any data
at `19e4ab3171c1540c40d6b12097745af98053b07d` — the same commit carries both
frozen predicates, both counters, the clause ledger, the eleven committed
control receipts and the re-issued frozen-blob ledger. One wave, 64 seats
(13 executor, 12 scout, 11 reviewer, 8 critic, 3 mutation-tester, 2 each
simplifier/sentinel/revenger, 7 scribe, 4 connector). The round-34 counters are
NOT amended — their blob ids are unchanged at the round-34 freeze, the
round-34 tip `dff394109f3cc3d851309ad7c67dd3b35b46adf2` and this tip
(`RevFrozenBlobs-r35.md` §3 re-verifies all seven at the real tip).

| Claim / axis | Before → after | Counting command | Author verdict |
|---|---|---|---|
| C1 coverage — the idle-lock control surface theme (frontier → core): three admitted entries (`idle-lock-never-asked-r12.md`, `idle-lock-chain-armed-r14.md`, `idle-lock-offered-in-the-bar-r15.md`) + eight registry rows S203–S210, adopted from the shokuknow merge package with ids re-pointed by document (package ids S309/S310/S321/S329/S330/S331/S334/S336 recorded in the round lesson) | pre-data freeze `19e4ab3`: `PRED-C1-r35-v1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED` exit 1 → data commit ⟨fill commit hash⟩: `closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET` exit 0 ⟨re-run at that commit and paste actual⟩; registry 192 → 200 rows; navigation 47/47 → ⟨50/50⟩ | `python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json` | ⟨pending data commit — expected: target met on the frozen counter⟩. Kill rule discharged by the eleven committed pre-data receipts: every defect control prints `TARGET_MISSED` exit 1, `controls/golden` prints `closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET` exit 0; all eleven receipts reproduced byte-for-byte on re-run (w1 RevReceipts). In-round scratch additions (not part of the committed kill set): entry `nlink=2` → MISSED; receipt-side `S_ISLNK` → MISSED (w1 ExecSymlink). |
| C2 calibration (tied for lowest; all three scored sub-axes at 1.0 and a capability entered in round 34, so the stagnation nudge does not waive) — the lane's self-description of its own evidence: retire the r34 dead word-bound clause, split the S_ISLNK/O_NOFOLLOW pair into load-bearing vs declared-TOCTOU, re-issue the frozen-blob ledger at the real r34 tip | before @ r34 tip `dff394109f3cc3d851309ad7c67dd3b35b46adf2` (tree extracted to scratch): `PRED-C2-r35-v1 error=clause-ledger-missing` exit 2 — no clause ledger, no re-issued blob ledger existed → after @ `19e4ab3171c1540c40d6b12097745af98053b07d`: `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET` exit 0 | `python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json` | target met at the freeze commit; the committed do-nothing receipt (`controls/c2-donothing.txt`: scratch one-clause ledger with neither control nor declaration) prints `uncovered=1 … verdict=TARGET_MISSED` exit 1. Caveat carried, not waived: the ledger's membership is unauthenticated worktree bytes — w1 RevDoNothing showed a scratch ledger truncated to the TOCTOU clause (V1) or repointing all eight receipts to one committed MISSED receipt (V3) also prints TARGET_MET. The counter scores the shape of the committed ledger; nothing pins the ledger itself. |

Axis table re-derived at ⟨data commit⟩: navigation ⟨50/50⟩ = 1.0;
calibration resolved-active ⟨N/N⟩ = 1.0; operability selftest 12/12 = 1.0.
(At `19e4ab3` the gate already reads `MADO_AXIS: checked=3 mismatched=0`,
navigation 47/47.)

### Capabilities (round 35)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| clause-ledger audit of an admission counter | Verify a committed clause ledger's shape: every live clause names a control whose committed receipt records `TARGET_MISSED`, or carries a `not-load-bearing` declaration with a reason; retired ids are absent from `live`; exactly the named TOCTOU clause may carry such a declaration; frozen blob ids re-verify by `git rev-parse` at the named tip | `python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json` → `TARGET_MET` exit 0; the `controls/c2-donothing` scratch ledger → `uncovered=1 … TARGET_MISSED` exit 1 | 35 |

Proposed-row caveat: this capability is a *shape* audit. w1 RevDoNothing
demonstrated reachable do-nothing TARGET_MET paths against a substituted
ledger (V1 truncation, V3 receipt-aliasing) because ledger contents and
receipts are trusted worktree bytes, not blob-pinned. If the integrator
judges the demonstrated thing "audit of whatever ledger the caller points
at", the row is defensible; if the capability claim is "the lane's evidence
ledger is verified", it is not yet supported. Stated here so the row is
admitted with its limit named.

### Sources, saturation, planned

Sources 192 → ⟨200⟩ rows (S203–S210 added; adopted from the merge package and
re-pointed by document; no row touched old→new; no frontier row advanced —
the named U items stay open, this theme is the idle-lock control surface).
Saturation 9.0 / N=3 unchanged; retired: none.
Planned (round 36; intent only): the binding gap w1 RevDoNothing found —
clause ledger and receipts are unauthenticated worktree bytes; a pinned
ledger hash or per-clause receipt binding would close the V1/V3 reachables;
w1 ExecSymlink's two scratch controls (entry `nlink=2`, receipt-side
`S_ISLNK`) live only under `scratch/` — commit-or-drop decision; w1 ExecRows'
observation that `on-change`/`on-request` recheck tokens are cadence-shaped
but unenumerated in the SOURCES v1 contract; ScoutReg's staged-append census —
the package's 140 contiguous ids S197–S336 collide with lane-allocated
S201/S202, reconciliation is campaign-side and stays operator-owned.

### Harm watch

⟨fill after data commit⟩ — expected unchanged: index gate `MADO_INDEX`
50/50 exit 0; axis gate `MADO_AXIS: checked=3 mismatched=0`; operability
selftest `MADO_SELFTEST` N/N; `--regression` `MADO_REGRESSION: PASS`; no
config tree, compositor state or sibling repo written.
```

## Measured values backing the ⟨fill⟩-free cells (re-run at write time)

- `python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json`
  at tip `19e4ab3` → `closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED`, exit 1.
- `python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json`
  at tip `19e4ab3` → `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET`, exit 0.
- Same C2 command against a scratch extraction of r34 tip `dff3941` →
  `PRED-C2-r35-v1 error=clause-ledger-missing`, exit 2.
- `git show 6d754bd:corpus/SOURCES.md | grep -cE '^\| S[0-9]'` → 192;
  `git ls-tree --name-only 6d754bd corpus/knowledge/` → 47 files, 0 matching `idle-lock-r1`.
- `git ls-tree --name-only HEAD .ufo/waves/round-35/fetch/` → 8 committed receipts S203–S210.
- `python3 -I quality/check-axis-scores.py --rev HEAD --repo .` → `checked=3 mismatched=0` exit 0.
