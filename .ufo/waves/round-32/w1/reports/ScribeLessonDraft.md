# ScribeLessonDraft — round-32 lesson draft (scratch)

Seat: scribe (leaf; no subagent dispatch). Date: 2026-10-24.

## Deliverable

Draft written to `.ufo/waves/round-32/scratch/ScribeLessonDraft/round-32.md`
(260 lines). **Nothing under `corpus/` was written by this seat** — per the
prompt, the draft lives in scratch only; landing it at
`corpus/lessons/round-32.md` is the L1's closure action.

## Coverage vs. the mandated contract

- `## Gate` — candidates table (3 staged entries + the 5 registry rows they
  cite: S186/S187/S189, S188, S196); ADMITS table with URL, access date
  2026-10-24, and a ≤25-word located quote per source; REJECTS (S196
  `teaches` erratum → M32-3 flip condition; `compositor-focus-manipulation-
  literature-r26.md` province reject with flip; claim-level `exec` reject →
  M32-2); review-layer line (used-by closure both directions; IPC draft
  FAIL→corrected; dispatchers entry unreviewed); quarantine verdicts from
  `w1/reports/ExecQuarantineSlice.md` (landed — 6 `payload-absent` + 7
  never-checked = 13 mado data rows; named `## By lane` defects); search-log
  note (pre-staged package; all-negative own searches; considerthese audit +
  one executed proposal).
- `## Mistakes` — 14 rows (M32-1…M32-14). Classes observed: scope ×3,
  attribution ×3, number-drift ×2, reference-drift ×1, vacuous ×2, survivor
  ×1, landing ×3. `stale-premise` and `provider` recorded as **no observed
  instance** (with the `stale-premise` adjudication noted — resolved *for*
  C2's premise by `SimplifierEvidence` + `CriticC2Predicate` attack 1).
  Every fix names a fails-before/passes-after command or fixture.
- `## Frontier` — moved/not-moved, ending with the explicit note that
  `round-31.md` was never filed and this draft must not repeat that defect.

## Evidence discipline

- 31/32 seat reports landed at write time; **one pending:
  `ReviewEntryDispatch`** — the dispatchers entry is unreviewed. Flagged
  UNBACKED in the draft rather than invented.
- Late-landing seats were folded in while drafting: `ExecQuarantineSlice`,
  `ReviewEntryIPC`, `ReviewUsedByClosure`, `CriticC2Predicate`,
  `RevengerPriorDefects` (each added rows M32-10…M32-14 or verdict text).
- Self-checks run against live bytes: `git status` (r30 report leftovers,
  three untracked landing entries, `M corpus/README.md`), `git ls-files
  quality/check-axis-scores.py` → untracked (M32-9), `grep -cE
  'S(186|196)' corpus/SOURCES.md` → 0 (append not landed), wave-pointer
  residue grep on the landing copy → clean (M32-12 fix verified).
- `ReviewUsedByClosure`'s "the L1's drafts do not exist" is recorded as
  accurate-but-stale (written while scribe drafts were scratch-only); its
  verdicts run on the staged package alone.

## Known soft spots for the L1

- M32-12's "*landing copy fixed*" is verified by grep-absence, not by a
  line-level diff — the fix claims only that no `wave-` pointer remains.
- The ADMITS quotes for S187/S189/S196 carry render-text line numbers from
  the L1's own scratch normalizations; the byte-level pins are the
  `fetch/S*.bin` shas.
- If `ReviewEntryDispatch` lands before closure, its findings fold into the
  Gate review-layer line and (if it FAILs) possibly new Mistakes rows — the
  draft's pending note marks exactly where.
