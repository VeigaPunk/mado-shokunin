# RevShonen — SHONEN boxes and the round-36 report draft (round 36, wave 1, reviewer)

Seat: `L1Mado36.RevShonen` (reviewer, leaf — no dispatch). Read-only over the lane and fleet files;
this report is the only write. No installs, no pacman, no compositor/service/package touch, no
`model` parameter, no peer message.

Axes named: (1) SHONEN mark integrity, (2) evidence-pointer resolvability at `master`,
(3) promotion-gate independence, (4) report-draft conformance to the canonical seed + marks rule.

Revisions: lane `master` = `a3094c99ab85bec35534de2447552c47dd2b647f` at read time (the freeze commit
`dbf8b57` plus wave-1 report commits; `git status` not run — blob identity via `git rev-parse` /
`git cat-file`). Fleet `PROTOCOL.md` = `/home/vgpnk/Projects/shokunin/PROTOCOL.md` at HEAD (fleet tip
not re-pinned here; cited line numbers verified on the working file).

## 1. SHONEN.md — box count and current markers

File: `LANE/SHONEN.md`, 12 lines. `git rev-parse master:SHONEN.md` →
`20c91c61b10b3f53ebaa21cfcd35d455a6565c89` = `git hash-object SHONEN.md` (working tree = `master` blob).
Last touching commit: `git log -1 --format='%h %cI %s' -- SHONEN.md` →
`7cd7f33 2026-10-15T02:12:36-03:00 mado: retain fleet round 1 navigation candidate; record routing block`.

- **Box count: 4** — matching the canonical seed verbatim (fleet `PROTOCOL.md:441-448`):
  1. `SHONEN.md:5` `[~]` SKILL.md contains real decision tables, error patterns, checklists, cited sources
  2. `SHONEN.md:7` `[~]` At least one end-to-end domain task executed and logged in LOG.md
  3. `SHONEN.md:9` `[~]` Instructions executable by an agent without oral context
  4. `SHONEN.md:11` `[~]` No cross-domain bleed (PROVINCE.md still accurate)

  All four carry **marker `[~]`** (author-asserted with evidence pointer). **Zero `[x]`, zero `[ ]`.**

- **`[x]` with named non-author verifier: none — PASS.**
  `grep -n '\[x\]' SHONEN.md` → no output, exit 1. The round-35 requirement ("it must not") is met
  by construction: no `[x]` exists to check. Historical context, confirmed by `git show c03c249:SHONEN.md`:
  boxes 1–4 once carried `[x]` marks naming MADO-R3-4 / VER-M3 / VER-M4B; commit `7cd7f33` downgraded
  all four to `[~]` because "a subagent the lane dispatched is still the lane" (PROTOCOL.md:65) voided
  the claimed independence. That state is unchanged in round 36.

- **Gate rule conformance (PROTOCOL.md:63-73).** Each box has exactly one indented evidence line,
  all four begin "Historical assertion: …"; the seed prose and box order diff clean modulo marks.
  `[~]` = asserted-by-author (PROTOCOL.md:165), which is the only correct mark here: round 36 has no
  outside-lane verifier for these boxes, and the lane itself wrote this round's changes.

## 2. Pointer resolvability of the *stated* evidence at `master`

| Box | Stated pointer | Resolves at `master`? | Notes |
|---|---|---|---|
| 1 | `corpus/knowledge/executor-test-sufficiency.md` | YES (`git cat-file -e` rc 0) | F4/F5 stand: the note attests box 3's condition (sufficiency transcript, verdict at `:139-141`), not box 1's — `grep -c "decision table"` → 0, `grep -c "error pattern"` → 0. SKILL.md itself carries `## Scoped verification — executable checklist` (`SKILL.md:266`) and `## Error patterns & traps` (`SKILL.md:353`); the stated pointer just doesn't prove them. |
| 2 | `corpus/knowledge/config-health-report-r3.md` + "LOG.md round 3 (VER-M3)" | HALF — report resolves; `VER-M3` does not occur in the round-3 block (`LOG.md:159-293`); `grep -n VER-M3 LOG.md` → `:294` (the **round-4** entry) and `:417` only | The cited mislabel survives: `LOG.md:294` calls it "box-3 CLOSED" while naming box 2's subject. |
| 3 | `corpus/knowledge/executor-test-sufficiency.md` | YES | Content fits the box (`:141` "Sufficient, end-to-end, against the version read"); only the independence bar keeps it `[~]` (PROTOCOL.md:65: dispatched subagent = the lane). |
| 4 | `corpus/knowledge/province-accuracy-selfaudit.md` round-5 receipt (VER-M4B); PROVINCE.md | PARTIAL — file resolves; the round-5 addendum is at `:267` ("§8 re-run receipt (M5-1, box-4 close evidence)"); `grep -c M4B` on the file → 0: the receipt **does not name VER-M4B** | The verifier half survives only in `plans/round-5-record-draft.md:195-205` + `LOG.md:295`; the `/tmp` verdict bytes are ephemeral (F3, criterion 13). |

## 3. Findings

- **F1 — Low (stale anchor, worth one line in the report):** `LOG.md:417` still reads
  "Probation 4/4 `[x]` since round 5" — zero `[x]` exist in `SHONEN.md` since `7cd7f33`. Known
  inherited defect (r35 RevShonen F1); unchanged by this round; a reader grepping LOG still sees
  4/4 approved.
- **F2 — Low:** Box 2's SHONEN line cites "LOG.md round 3 (VER-M3)" but VER-M3 is only at
  `LOG.md:294` (round-4 entry) — pointer resolves, attribution mislabeled. Known (r35 F2).
- **F3 — Low:** Box 4's "(VER-M4B)" is not inside the cited receipt (`grep -c M4B` → 0). Known (r35 F3).
- **F4 — Info:** No new defect introduced this round to the SHONEN surface; file untouched since
  `7cd7f33`. The defects are pointer-quality, not mark-integrity, failures.

## 4. Draft `## SHONEN` lines for the round-36 report

Contract (fleet prompt `mado-round-36.md:118-119` and `PROTOCOL.md:163-168`): one line per box,
`[x]` only with a named non-author verifier (none exists — forbidden), `[~]` with a resolvable
pointer, `[ ]` if untouched. The round-35 report's honest form (`[INFERENCE]` none — observed at
`.ufo/reports/round-35/mado.md:169-181`) is kept: marker `[~]`, stated pointer carried verbatim
where it resolves, mislabeled anchors named rather than silently fixed.

Draft (drop-in):

```markdown
## SHONEN

- `[~]` SKILL.md contains real decision tables, error patterns, checklists, cited sources — unchanged
  (`SHONEN.md` blob `20c91c61…` at `master` `a3094c99`); stated pointer
  `corpus/knowledge/executor-test-sufficiency.md` resolves but attests box 3's condition; SKILL.md's
  own `## Scoped verification` (`SKILL.md:266`) and `## Error patterns & traps` (`SKILL.md:353`) carry
  the substance. No named non-author verifier — `[x]` would violate PROTOCOL.md:65.
- `[~]` At least one end-to-end domain task executed and logged in LOG.md — unchanged; pointer
  `corpus/knowledge/config-health-report-r3.md` + `LOG.md:294` (VER-M3 lives in the round-4 entry,
  not the round-3 block the box cites; LOG.md:294's "box-3" label is box 2's subject).
- `[~]` Instructions executable by an agent without oral context — unchanged;
  `corpus/knowledge/executor-test-sufficiency.md:141` ("Sufficient, end-to-end, against the version
  read") fits the box; lane-dispatched verifier keeps it author-asserted only.
- `[~]` No cross-domain bleed (PROVINCE.md still accurate) — unchanged;
  `corpus/knowledge/province-accuracy-selfaudit.md:267` (round-5 addendum) + `PROVINCE.md`; the
  receipt does not name VER-M4B (grep → 0); verifier attribution survives at `LOG.md:295` /
  `plans/round-5-record-draft.md:195-205`. Round 36 touched no PROVINCE surface.

No box moved, nothing was self-promoted (`grep -c '\[x\]' SHONEN.md` → 0 at `a3094c99`).
```

**Pointer-resolution check at `master` `a3094c99` — every path above resolves:**

```
git cat-file -e master:corpus/knowledge/executor-test-sufficiency.md     → rc 0
git cat-file -e master:corpus/knowledge/config-health-report-r3.md        → rc 0
git cat-file -e master:corpus/knowledge/province-accuracy-selfaudit.md    → rc 0
git cat-file -e master:LOG.md                                           → rc 0
git cat-file -e master:PROVINCE.md                                      → rc 0
git cat-file -e master:SKILL.md                                         → rc 0
git rev-parse master:SHONEN.md                                          → 20c91c61b10b3f53ebaa21cfcd35d455a6565c89
```

Line anchors verified on the `master` blobs: `SHONEN.md` boxes at `:5,:7,:9,:11`; `SKILL.md:266` /
`:353` section heads confirmed by `grep -n`; `LOG.md:294` (round-4 VER-M3) and `:417` (stale 4/4)
confirmed; `province-accuracy-selfaudit.md:267` round-5 addendum confirmed; `M4B` absent from that
file (`grep -c` → 0, rc 1).

## 5. Residual risk and gaps

- Lane tip moved during this review (`dbf8b57` → `a3094c99`); all resolvability claims name `master`
  = `a3094c99`. A later lane commit cannot invalidate the SHONEN.md blob claim (file untouched since
  `7cd7f33`) but can shift cited line anchors.
- Fleet `PROTOCOL.md` was read from the working tree; cited lines (`:63-73`, `:163-168`, `:441-451`)
  verified on those bytes. It is out-of-lane and can change under this report.
- The draft's negative claims (`grep -c` → 0) are exit-1 results on committed blobs — durable.
- Tool record: no installs, no upgrades (host pacman pause respected); this report is the only write.
