# SctRound38Report — round-39 w1: refuted addendum-5 extraction (mado lane)

Seat: `SctRound38Report` (scout, leaf — no subagents dispatched, no background jobs).
Date: 2026-10-25. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Lane HEAD at read time: `457d1b125932c1e0d797061a2156b917bcd7edaa` (round-39 freeze commit).
Deliverable file: `.ufo/waves/round-39/w1/SctRound38Report/refuted.txt` (only file written besides this report).
Tool installs: **none** (nothing needed; all evidence was in-repo git bytes).
Host safety: no pacman, no service/compositor mutation, no socket connects, no input injection. Fleet repo read-only (git log/show/hash-object only). No mutating git/jj in the lane.

## Assignment

Round-39 registration `.ufo/waves/round-39/registration.md:23-25` (routed defect #2) requires:
"Correct the fleet round-38 report's refuted addendum-5 refinement (the 'frozen pair 19/19 at
freeze rev' sentence, refuted by the lane's own errata c46f868/f551b70) in this round's report
as an erratum naming the superseded text."

My scope: extract the exact superseded text and the exact refuting records, with line/commit
pointers, so the report's erratum can quote them verbatim. The filed bytes are never rewritten.

## Findings (all verified from committed bytes)

### 1. The superseded text (fleet repo, read-only)

- File: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-38/mado.md`, **line 166**, section
  `## Addendum — wave-1 seat findings folded in` (heading at :135).
- Blob `728d9d80ddf5ba494643a9e0786b89aeabbfef45` (11770 bytes, 166 lines).
- Fleet commit `9386c91f24665faeed8d5ae5c0c503466c5cdd8c` — "round-38: mado report addendum 5 —
  RevCensusBefore refinement", commit date 2026-10-25T11:26:06-03:00, author `mado-shokunin
  <mado@shokunin.local>`. File commit range `8a1cbcd3..9386c91f` (7 commits, same identity).
- Refuted clause (verbatim): *"Refines the errata: frozen instruments × frozen manifest **at the
  freeze rev** = 19/19 — the claim as frozen was internally coherent (the `c1-duprow` append
  landed outside `## Registry`); HEAD instruments × frozen manifest = 18/19."*
- **Pointer defect in the same bullet:** it cites "(LOG @ `22f600f1`)", but `22f600f1` is the
  *RevC1v3 residual refinement* erratum. The record actually carrying the RevCensusBefore
  freeze-verdict refinement is lane commit `3674cf28` at `LOG.md:2337-2343`.

### 2. The lane's own source record of the claim

- Lane commit `3674cf281e8c434d673d38e80ab902716bf87ce1` ("round-38 errata: RevCensusBefore
  freeze-verdict refinement (frozen pair 19/19 at freeze rev)", 11:26:04-03:00) →
  `LOG.md:2337-2343`.
- Origin seat report `.ufo/waves/round-38/w1/reports/RevCensusBefore.md:110` and summary
  table `:124`.

### 3. The refutation — two lane errata plus a third independent one

- **`c46f868f40dec89a68a1d2a97bc5027504f32388`** ("record dispute between RevFrozenClaims and
  RevCensusBefore on the frozen pair — closure adjudicates", commit date 11:35:43-03:00) →
  `LOG.md:2385-2391`: *"RevFrozenClaims's direct replay of the frozen `58e55ec` counter+manifest
  gives 18/19 at BOTH the data rev and the freeze rev … falsifying the recorded 'frozen pair
  19/19 at freeze rev' (added from RevCensusBefore at `3674cf28`)."*
  The falsifying seat report `.ufo/waves/round-38/w1/reports/RevFrozenClaims.md:89-106`
  ("### F3 — HIGH — the lane's freeze-coherence record is factually wrong") quotes the lane's
  own record and refutes it; Replay C output at `:80-82` →
  `MADO_R38_DISCRIMINATION: controls=19 correct=18/19 verdict=TARGET_MISSED`.
- **`f551b70569d08fe82c04d7c3d61a87c2912ad80f`** ("freeze-pair resolution", commit date
  12:25:59-03:00) → `LOG.md:2414-2423` + `SCORECARD.md` round-38 calibration move-row
  wording fix. Cross-pair matrix in `.ufo/waves/round-38/w1/reports/ScoutConsiderThese.md:77-82`:
  frozen×frozen **18/19**; frozen×landed 19/19; landed×frozen **18/19**; landed×landed 19/19.
  Console bytes at `:85-93`.
- **Third, independent refutation already landed BEFORE addendum-5**:
  `.ufo/waves/round-38/w1/reports/RevM37Routing.md:227-233` ("neither of us can reproduce …
  the distinguishing variable is manifest version, not rev"), corroborated by
  `.ufo/waves/round-38/w1/scratch/RevCommitChain/revm37routing-verification.md:31-39`.

### 4. Propagation map of the superseded claim (named so the erratum can name it)

1. `LOG.md:2337-2343` (commit 3674cf2) — the original record; superseded by `LOG.md:2385-2391`
   (c46f868) and adjudicated by `LOG.md:2414-2423` (f551b70).
2. `corpus/lessons/round-38.md:87-89` — the **same false sentence still live** in the Mistakes
   section: *"frozen instruments x frozen manifest = 19/19 at the freeze rev …"*.
3. `SCORECARD.md` round-38 calibration row — already corrected by f551b70 (now reads
   "repaired manifest+counters discriminate v2 13/19 → 19/19 (the frozen pair replays 18/19;
   see LOG errata)").
4. Fleet `.ufo/reports/round-38/mado.md:166` — the refuted bullet itself; never rewritten.

### 5. Ruling basis for the erratum

Frozen pair = frozen counter × frozen manifest = **18/19 at every rev**: the frozen `c1-duprow`
control appends the duplicate S189 row at EOF of `corpus/SOURCES.md` (after `## Paths`),
outside the `## Registry` section the counter's `registry_rows()` parses — so the crib never
bites and the control necessarily fails. The 19/19 belongs to the post-data manifest rewrite
`b6c1d31` (`c1-duprow` moved inside `## Registry`); the `859d0cf` counter patch is a verdict
no-op. The distinguishing variable is the **manifest version, not the rev** — exactly what the
superseded sentence mis-attributed. Consequence (unchanged): round-38's C1 fails as declared;
the landed 19/19 is a new predicate, re-registered by round-39 §C1, whose red-before receipt
`.ufo/waves/round-39/receipts/c1-redbefore.txt` shows `controls=19 correct=18/19
verdict=TARGET_MISSED` (exit 1), sole failure `c1-duprow`.

## Confidence

- **High** for every quotation and pointer above: each was read from committed bytes
  (`git show`, `git log`, `git hash-object`, `grep -n`), not from memory.
- **Unresolved (not needed for the erratum):** the exact command RevCensusBefore ran to obtain
  19/19. RevFrozenClaims marks it `[INFERENCE]` (mixed pairing: repaired manifest passed as
  "frozen"); RevM37Routing says "I cannot reconstruct their exact command." The lane's own
  records agree the number is unreachable for the frozen pair.

## Commands run (all read-only)

```
git -C /home/vgpnk/Projects/shokunin log --format='%h %cI %s' 8a1cbcd3..9386c91f -- .ufo/reports/round-38/mado.md
git -C /home/vgpnk/Projects/shokunin show 9386c91f -- .ufo/reports/round-38/mado.md
git -C /home/vgpnk/Projects/shokunin hash-object .ufo/reports/round-38/mado.md     # 728d9d80…
git -C …/mado-shokunin show 3674cf28 -- LOG.md
git -C …/mado-shokunin show c46f868 -- LOG.md ; git -C …/mado-shokunin show f551b70 -- LOG.md SCORECARD.md
git -C …/mado-shokunin show c46f868:LOG.md | sed -n '2375,2395p'
git -C …/mado-shokunin show f551b70:LOG.md | sed -n '2400,2430p'
grep -n over .ufo/waves/round-38/w1/reports/{RevCensusBefore,RevFrozenClaims,ScoutConsiderThese,RevM37Routing}.md, corpus/lessons/round-38.md, LOG.md
```
No mutating git/jj command was run. No file outside this seat directory and this report was written.

## Handoff to the report author

The round-39 report's erratum should (a) quote the superseded fragment verbatim as above,
(b) name the three refuting records with commit + LOG line pointers, (c) state the correct
number (frozen pair = 18/19; distinguishing variable = manifest version), and (d) note that
`corpus/lessons/round-38.md:87-89` carries the same false sentence and is routed to round-39's
lesson correction (the round-39 lesson file already records this at
`.ufo/waves/round-39/w1/ScrLesson/round-39.md:102`).
