# RevShonen — SHONEN boxes and the vacuity criterion (round 35, wave 2, falsification)

Seat: `L1Mado35.RevShonen` (reviewer, leaf — no dispatch). Read-only attack; writes only this
report plus `.ufo/waves/round-35/scratch/RevShonen/QUALITY-HEAD.md` (a HEAD snapshot for the diff).
No installs, no pacman, no lane corpus edit, no jj command, no `git diff`/`git status` (index untouched;
blob identity checked with `git hash-object` / `git rev-parse`).

Axes named: (1) SHONEN mark integrity, (2) evidence-pointer resolvability, (3) promotion-gate
independence, (4) QUALITY-bar coverage of instrument vacuity, (5) ledger supersession consistency.

Revisions (criterion 9 binding). The lane **committed during this review**, so every verdict below names
its revision:

| revision | time (-03) | state |
|---|---|---|
| `19e4ab3` | 2026-10-24T23:24:06 | round-35 freeze: C1/C2 predicates, clause ledger, control receipts, blob ledger |
| working tree | 2026-10-25T03:31:22 | `corpus/QUALITY.md` gains criteria 55-56 (working blob `c08d7f14…`) |
| `02088b4` | 2026-10-25T03:34:26 | "round-35: the idle-lock control surface lands — three entries, eight rows S203-S210, errata, and the wave-1 evidence" |

All counter runs and `git` reads below are post-`02088b4` (≈06:35Z). SHONEN.md and QUALITY.md were
byte-compared at both revisions.

## 1. SHONEN.md — per-box state, pointer, and round-35 change

File: `SHONEN.md`, 12 lines, sha256 `c723b7413170aa9952bd071941a3e6376527f1e2cc6ab48fa2a85c489b3b3e99`,
git blob `20c91c61b10b3f53ebaa21cfcd35d455a6565c89`.

Round-35 change: **none.** `git rev-parse HEAD:SHONEN.md` = `git hash-object SHONEN.md` =
`20c91c61…` at `02088b4`; the same at `19e4ab3`; last commit touching the file is
`7cd7f33` (2026-10-15T02:12:36-03:00); `git show --name-only --format='' 02088b4 | grep -c '^SHONEN.md$'`
→ `0`, exit 1. `grep -c '\[x\]' SHONEN.md` → `0`, exit 1: **no `[x]` exists, no box was
self-promoted, no named non-author verifier was added this round.** Round 35 also has no LOG closure
entry yet (LOG tail is wave-1 seat scratch notes, LOG.md:2014-2033), and `02088b4` touched neither
LOG.md nor SCORECARD.md.

| Box | Mark | Stated pointer | Resolves? | Fits the box's own condition? | Round-35 change |
|---|---|---|---|---|---|
| 1 SKILL.md contains real decision tables, error patterns, checklists, cited sources | `[~]` | `corpus/knowledge/executor-test-sufficiency.md` (MADO-R3-4) | YES — 16,002 B, present | **NO** — the note is a sufficiency transcript, not an artifact inventory. `grep -c "decision table"` → 0 (exit 1); `grep -c "error pattern"` → 0 (exit 1). Its verdict is `## Sufficiency verdict` (`:139`) "Sufficient, end-to-end, against the version read" (`:141`), i.e. box 3's subject. SKILL.md does carry `## Scoped verification — executable checklist` (`SKILL.md:266`) and `## Error patterns & traps` (`:353`), but the SHONEN line's stated pointer does not attest them. | none |
| 2 ≥1 end-to-end domain task executed and logged in LOG.md | `[~]` | `corpus/knowledge/config-health-report-r3.md` + "LOG.md round 3 (VER-M3)" | HALF — the report is present (64,102 B); the round-3 block is LOG.md:159-293 and contains **no** `VER-M3` (`sed -n '159,293p' LOG.md \| grep -c VER-M3` → `0`, exit 1). VER-M3 appears only at LOG.md:294 (the **round-4** entry) and LOG.md:417. | Partly. LOG.md:294 labels the VER-M3 closure "box-3 … config-health report reproduces" — under current SHONEN that content is box **2** (box 3 is the no-oral-context criterion). LOG's box number and SHONEN's box number are not the same surface. | none |
| 3 Instructions executable by an agent without oral context | `[~]` | `corpus/knowledge/executor-test-sufficiency.md` (MADO-R3-4) | YES | YES — the note's own assignment (`:3-7`) is a no-oral-context executor lane reading SKILL.md only, and its verdict is "Sufficient, end-to-end". Only independence bars `[x]`: MADO-R3-4 was lane-dispatched, and `PROTOCOL.md:65` says "a subagent the lane dispatched is still the lane". | none |
| 4 No cross-domain bleed (PROVINCE.md still accurate) | `[~]` | `corpus/knowledge/province-accuracy-selfaudit.md` round-5 receipt (VER-M4B); `PROVINCE.md` | PARTIAL — the addendum is present (`:267` "Round-5 addendum — §8 re-run receipt (M5-1, box-4 close evidence)"); `PROVINCE.md` present. But `grep -c M4B corpus/knowledge/province-accuracy-selfaudit.md` → `0`, exit 1: the receipt the box cites **does not name VER-M4B**. The verifier verdict lived only at `/tmp/w5-ver-m4b-work/VERDICT.md` (sha `f70fc3c70a11e91e…`, quoted at `plans/round-5-record-draft.md:201`) — ephemeral under criterion 13. | none |

Verdict on the gate rule: all four boxes correctly remain `[~]`. No `[x]` is present, and no evidence
in round 35 could have supported one: the round's own outputs are (a) a coverage claim whose counter is
shape-satisfiable (see §2) and (b) lane-dispatched seats, which `PROTOCOL.md:65` and
`corpus/QUALITY.md` criterion 12 both keep at `[~]`.

## 2. Findings by severity

### F1 — Medium — LOG.md still states present-tense "Probation 4/4 `[x]`" with no supersession pointer

`LOG.md:417`: "Probation 4/4 `[x]` since round 5 (VER-M3 | VER-M4B; `SHONEN.md`);" and `LOG.md:295`:
"SHONEN box 4 CLOSED by VER-M4B — PROBATION COMPLETE 4/4." The file they cite, `SHONEN.md`, carries
**zero** `[x]` since `7cd7f33` (2026-10-15). `SKILL.md:733-737` ("Round-16 current-status correction:
… four `[~]` assertions and zero approved boxes") and `SCORECARD.md:40,687,1621` carry the correction;
LOG.md does not. Under criterion 28 the superseded present-tense value needs an in-file pointer in every
owned file in the same round — LOG.md:417 is the surviving un-pointed site, and `LOG.md:295` predates the
downgrade. Inherited defect, unchanged by round 35; it is the one place a reader greps and concludes 4/4
approved.

### F2 — Medium — Box 2's VER-M3 attribution points at the wrong LOG entry and the wrong box number

Verified above: `VER-M3` has 0 occurrences inside LOG.md:159-293 (round 3) and is recorded only under the
round-4 entry (`:294`). The round-3 entry's own verifier ids are MADO-R3-2/MADO-R3-4 (`:159-175`).
Compounding it, `:294` labels the closure "box-3" while the config-health-report reproduction it names is
box 2's subject. The SHONEN line inherits the mislabel verbatim (`SHONEN.md:8`).

### F3 — Medium — Box 4's cited receipt does not name the verifier it credits

`SHONEN.md:12` names "round-5 receipt (VER-M4B)". The cited file's round-5 addendum (`:267-…)` is
explicitly the **evidence** half ("M5-1, box-4 close evidence"); `grep -c M4B` over the file → `0`,
exit 1. The verifier half is recoverable only from `plans/round-5-record-draft.md:195-205` and `LOG.md:295`,
i.e. a plan draft narrating an ephemeral `/tmp` verdict (criterion 13; the producer-naming intent of
criterion 24).

### F4 — Low — Box 1's pointer evidences box 3, not box 1

The bar's own minimum text (gate text `PROTOCOL.md:69-71`; seed template `PROTOCOL.md:455-464` with the marks rule at `:466-467`) requires box 1 to show
"at least one `SKILL.md` decision table, error-pattern list, and checklist, each citing a resolvable
source". `executor-test-sufficiency.md` contains neither term (`0`/`0`, exits 1). The claim may be true
on SKILL.md itself (`:266`, `:353`), but the pointer supplied for it does not attest it — a
pointer/condition mismatch that survives until an outside reviewer reads SKILL.md directly.

### F5 — Low — Boxes 1 and 3 cite the same note for different conditions

One transcript cannot simultaneously attest "real decision tables, error patterns, checklists, cited
sources" (box 1) and "executable without oral context" (box 3); it attests the latter. This is the root
of F4 and is worth naming so a future reviewer does not read two hits as two independent attestations.

### F6 — Low — SKILL.md's seed anchor does not resolve at the current fleet revision

`SKILL.md:716` says the gate is "the canonical four boxes … seed PROTOCOL.md:419-431". At the current
fleet `PROTOCOL.md` (544 lines) that range is the **Scope / Closure consequence / Delivery** passage;
the canonical seed template is `PROTOCOL.md:455-464`, with the canonical-form rule at `:446` and the
marks rule at `:466-467` ("`[x]` only with a named non-author verifier per **Promotion gates**"). The
four boxes and SHONEN.md's box order do match the template, so this is an anchor defect, not a
content defect — but criterion 8 (a path is a recheck target only after confirming it at the named
revision) and criterion 54 (an anchor resolves in the named file at the named location) both bite on it.
The fleet file is out-of-lane and was read only; the repair belongs to the lane's SKILL.md, not here.

## 3. QUALITY.md — is the vacuity / shape-only admission criterion there?

**Yes — criterion 55, with criterion 56 — but it is round-35 output that landed mid-review, and its own
application sentence does not reproduce.**

Observed sequence:

- At `19e4ab3` (freeze) `corpus/QUALITY.md` was **360 lines**, ending at criterion 54; no round-35
  section, no vacuity criterion (`git show 19e4ab3:corpus/QUALITY.md | grep -c '^55\.'` → 0).
- At 2026-10-25T03:31:22-03 the working tree gained two lines (362 lines; working blob `c08d7f14…`).
- At `02088b4` they are committed: `git show HEAD:corpus/QUALITY.md | grep -n '^55\.\|^56\.'` → `:361`,
  `:362`; HEAD blob = working blob = `c08d7f14…`.

Content, checked against the round's findings:

- **Criterion 55** (`QUALITY.md:361`) names exactly the shape-only/fabricated-payload families:
  indirection cribs (symlink at the claimed path, symlinked parent, hardlinked file, fetch/overlay path)
  and content cribs ("a shape-only tree whose rows and gate-quote lines are present while the prose is
  absent, and a fabricated-payload tree whose receipt files carry the right names and lengths but not the
  frozen bytes"), each requiring a `TARGET_MISSED` receipt, and says "A counter that pins a receipt digest
  but never binds it to the bytes it read has a dead clause, not a defence." That is the CritVacuous /
  RevTarget finding, and it extends (does not restate) criterion 36.
- **Criterion 56** (`:362`) requires per-clause accounting (controlled or declared) — the clause-ledger
  half (the dead `digest-match`/`o-nofollow-open` problem).
- Grounding resolves: `lessons/round-35.md` exists at HEAD (blob `2af3479…`), `## Mistakes` `:165`,
  `### M35-2 — instrument vacuity` `:195`. Round-30's grounding rule is satisfied for criterion 55. For
  criterion 56 the second citation `lessons/round-34.md#mistakes instrument` is a class label inside
  `## Mistakes` (`round-34.md:109`, "class: instrument" `:111`), not a heading — weaker than criterion 54's
  heading-anchor convention, though inside the named file.

Three defects in the new criterion's own evidence, which a closure must fix or record:

1. **Wrong crib root (reproduced).** Criterion 55 says "`scratch/CritVacuous/` and `scratch/RevTarget/`
   both reach `TARGET_MET`". Observed, at `02088b4`:

   ```
   python3 -I .ufo/waves/round-35/c1/count.py --root .ufo/waves/round-35/scratch/RevTarget --frozen .ufo/waves/round-35/c1/frozen.json
   PRED-C1-r35-v1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED   rc=1
   python3 -I .ufo/waves/round-35/c1/count.py --root .ufo/waves/round-35/scratch/RevTarget/quote-only ...  → TARGET_MET rc=0
   python3 -I .ufo/waves/round-35/c1/count.py --root .ufo/waves/round-35/scratch/RevTarget/fake-all  ...  → TARGET_MET rc=0
   python3 -I .ufo/waves/round-35/c1/count.py --root .ufo/waves/round-35/scratch/RevTarget/empty      ...  → TARGET_MISSED rc=1
   python3 -I .ufo/waves/round-35/c1/count.py --root .ufo/waves/round-35/scratch/CritVacuous        ...  → TARGET_MET rc=0
   ```

   The named `RevTarget/` root reproduces `TARGET_MISSED`; the MET trees are its subdirectories. By
   criterion 54 (an anchor resolves against the named location only) the criterion's own application
   sentence is wrong by one path level — a criterion that demands exact receipt naming must itself name
   the reproducing path.
2. **The crib evidence is not committed.** Criterion 55 requires a *committed* `TARGET_MISSED` receipt per
   crib, but `git ls-tree -r --name-only HEAD -- .ufo/waves/round-35/scratch | wc -l` → `0`: both
   `scratch/CritVacuous/` and `scratch/RevTarget/` are uncommitted working-tree bytes at `02088b4`.
   Criterion 13's durable-path condition is unmet for the very evidence criterion 55 cites (criterion 50
   names the same decision: commit the bytes or name the committed basis receipt).
3. **The bar does not clean the round it came from.** The counter still prints `TARGET_MET` on a
   shape-only tree at the same revision it prints `TARGET_MET` on the real lane root:

   ```
   --root <lane root>                              → closed_entries=3 closed_rows=8 open_cites=0 TARGET_MET rc=0
   --root <lane root>/controls/golden              → closed_entries=3 closed_rows=8 open_cites=0 TARGET_MET rc=0
   --root <lane root>/controls/c1-donothing        → closed_entries=0 closed_rows=0 open_cites=8 TARGET_MISSED rc=1
   C2: --repo <lane root>                          → uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 TARGET_MET rc=0
   ```

   That is the correct state under the round's own rule (predicate frozen at `19e4ab3`, repair is a
   round-36 claim), and `lessons/round-35.md:253-266` says so. Criterion 55 does not, and must not, be
   read as clearing C1 — C1's `TARGET_MET` remains evidence of presence and internal consistency only,
   never that the eight receipts are the bytes their digests name.

Not registered: `registration.md` (frozen at `19e4ab3`) contains no criterion claim for 55/56 and no
round-35 counter measures them, so they may not be counted as a criterion-count axis move for round 35.
They are a bar addition, landed in the data commit, after the falsification that motivated them — the
append-only shape the lane uses, but it should be stated as such at closure.

## 4. Residual risk and verification gaps

- **Concurrent commit.** The lane moved from the freeze `19e4ab3` to `02088b4` while this review ran.
  Every verdict here is read at/after `02088b4`; a later commit can change the state without changing
  this report's claims about the two revisions it names.
- **Unobservable revert.** SHONEN.md's working blob equals its HEAD blob at both revisions; a mid-round
  write-and-revert of SHONEN.md cannot be excluded from committed bytes, only from the two states
  observed.
- **VER-M4B's verdict bytes are not durable.** I did not search outside the lane for
  `/tmp/w5-ver-m4b-work/VERDICT.md` (gone); the sha quoted in `plans/round-5-record-draft.md:201` is the
  only trace, and I did not find a committed copy.
- **Out-of-lane citation only.** `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md`
  was read, never written; it can change underneath this report's F6 anchor without a lane commit.
- **No new crib controls.** `.ufo/waves/round-35/controls/` still holds the freeze set (11 C1 trees + the
  C2 receipt); no shape-only or fabricated-payload control tree exists there, so criterion 55's required
  cribs are not yet exercised as controls — as recorded in finding 1/3 above.
- **Not my scope, not run:** C1/C2 quote, receipt-byte, row and census attacks (sibling seats), corpus
  renders, fleet repo, sibling lanes. No tool installation or update was performed (host pause respected);
  tool record: none.

## 5. Command ledger (every verdict above)

Run from `/home/vgpnk/Projects/shokunin/mado-shokunin`, post-`02088b4`.

| # | command | observed | rc |
|---|---|---|---|
| 1 | `git rev-parse HEAD:SHONEN.md; git hash-object SHONEN.md` | `20c91c61b10b3f53ebaa21cfcd35d455a6565c89` / same | 0 |
| 2 | `grep -c '\[x\]' SHONEN.md` | `0` | 1 |
| 3 | `git show --name-only --format='' 02088b4 \| grep -c '^SHONEN.md$'` | `0` | 1 |
| 4 | `git log -1 --format='%h %cI %s' -- SHONEN.md` | `7cd7f33 2026-10-15T02:12:36-03:00 …` | 0 |
| 5 | `grep -c "decision table" corpus/knowledge/executor-test-sufficiency.md` | `0` | 1 |
| 6 | `grep -c "error pattern" corpus/knowledge/executor-test-sufficiency.md` | `0` | 1 |
| 7 | `sed -n '159,293p' LOG.md \| grep -c VER-M3` | `0` | 1 |
| 8 | `grep -n "VER-M3" LOG.md` | `294`, `417` only | 0 |
| 9 | `grep -c M4B corpus/knowledge/province-accuracy-selfaudit.md` | `0` | 1 |
| 10 | `grep -n "Round-5 addendum" corpus/knowledge/province-accuracy-selfaudit.md` | `:267` | 0 |
| 11 | `grep -n "Probation 4/4" LOG.md` | `:417` | 0 |
| 12 | `grep -n "four \`\[~\]\`\|zero approved" SCORECARD.md` | `40, 687, 1621` | 0 |
| 13 | `grep -n "Round-16 current-status correction" SKILL.md` | `:733` | 0 |
| 14 | `git show 19e4ab3:corpus/QUALITY.md \| wc -l` ; `… \| grep -c '^55\.'` | `360` ; `0` | 0 / 1 |
| 15 | `git show 02088b4:corpus/QUALITY.md \| wc -l` ; `… \| grep -n '^55\.\|^56\.'` | `362` ; `:361`,`:362` | 0 |
| 16 | `git hash-object corpus/QUALITY.md; git rev-parse HEAD:corpus/QUALITY.md` | both `c08d7f149d906ec08b48c19ba0b180f90998832b` | 0 |
| 17 | `git ls-tree -r --name-only HEAD -- .ufo/waves/round-35/scratch \| wc -l` | `0` | 0 |
| 18 | `python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json` | `closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET` | 0 |
| 19 | same, `--root .ufo/waves/round-35/scratch/CritVacuous` | `TARGET_MET` | 0 |
| 20 | same, `--root .ufo/waves/round-35/scratch/RevTarget` | `closed_entries=0 closed_rows=0 open_cites=8 TARGET_MISSED` | 1 |
| 21 | same, `--root …/RevTarget/quote-only` ; `…/fake-all` ; `…/empty` | `TARGET_MET` ; `TARGET_MET` ; `TARGET_MISSED` | 0 / 0 / 1 |
| 22 | same, `--root .ufo/waves/round-35/controls/golden` | `TARGET_MET` | 0 |
| 23 | same, `--root .ufo/waves/round-35/controls/c1-donothing` | `TARGET_MISSED` | 1 |
| 24 | `python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json` | `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 TARGET_MET` | 0 |
| 25 | `git rev-parse HEAD:corpus/lessons/round-35.md` | `2af347903a2364491cc2616070357815da5e8ae2` | 0 |
| 26 | `grep -n "^## \|^### M35-2" corpus/lessons/round-35.md` | `## Mistakes` `:165`, `### M35-2 — instrument vacuity` `:195` | 0 |
| 27 | `grep -n "still the lane" PROTOCOL.md` (fleet) ; `grep -n "Box 1 needs at least one" PROTOCOL.md` | `:65` ; `:69` | 0 |
| 28 | `sed -n '455,464p' PROTOCOL.md` (fleet) | canonical seed template, four boxes | 0 |


## 6. Axes and trend (scoped to this seat)

`discernment` and `calibration` are the only axes this seat can speak to, and only negatively: the round's
own bar gained the criterion its falsification produced (55), which is a quality move, but the criterion's
cited evidence is uncommitted and mis-rooted, and the SHONEN surface is unchanged, so no promotion
inference is available. `coverage` is untouched by this report beyond observing that C1's `TARGET_MET`
is shape-satisfiable at the data revision.
