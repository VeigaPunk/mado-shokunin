# AtkLesson23Fix — routed defect 1, appended correction in `corpus/lessons/round-23.md`

Attacked: the correction appended at the end of `corpus/lessons/round-23.md` (:230-237 of 237), landed in
`d9fec1d3` ("round-24: C1 counter lane-path override …; routed r23 defects 1-2 (append-only)", 2026-10-23
00:12:30 −03, ancestor of tip `39c59630`; the only commit touching the lesson in `8e5d9369..39c5963`).
Checks re-run from source, not taken from the correction's own text.

## 1. Is it true? — YES, every checkable claim verified

- **"first added in lane commit `c8cb3930` (2026-10-22 08:49:46 −03)"** — `git log --format='%h %ci' --
  corpus/knowledge/terminal-trees-r23.md` returns, oldest-first tail: `c8cb393 2026-10-22 08:49:46 -0300`
  (same commit as `c8cb3930`; resolves unambiguously). `git cat-file -e c8cb3930^:<note>` fails (ABSENT),
  `c8cb3930:<note>` EXISTS → first add confirmed at exactly that commit and timestamp.
- **"amended append-only in `3732c7a7`"** — `git diff --numstat c8cb3930 3732c7a7 -- <note>` = `13 0`
  (additions only); the commit subject itself says "(append-only)".
- **"the closure re-measured the ghostty route at 3/3"** — committed receipt
  `.ufo/waves/round-23/evidence/c2-after-2f1134f3.json`: `"note_present": true`, ghostty ids
  `S134,S135,S136,S137,S138,S139,S150,S151`, `"count": "3/3"`. Independent w2 critic
  `w2/reports/CritC2Gaming.md`: "Result: 3/3, exit 0 … ghostty has 8". ✓
- **"copied scribe draft"** — the paragraph exists verbatim at
  `3df1062:.ufo/waves/round-23/w1/reports/SrcGhostty.md:160`, including the same bolded
  "**The note file does not yet exist**" opener and the same "until the integrator creates the note" tail.
- **"false at the round-23 tip"** — `<note>` EXISTS at `3df1062`, `fa819d56` (r23 tip), `8e5d9369`
  (r23 closure / r24 base) and `39c59630`, while :197-199 asserts non-existence.

Residual (non-defect) nuance: the note's history did not end at `3732c7a7` — the closure commit `3df1062`
appended a further 9-line Errata block (numstat `9 0`, also additions-only), recorded in the lesson at :59
("the note's Errata"). The correction never claims `3732c7a7` is the last change, so this is an omission of
a benign later append, not a misstatement.

## 2. Is it append-only? — YES

`git diff 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122 39c596307333b8ca0a1e42b3f3b9a748bb8b208b --
corpus/lessons/round-23.md`: single hunk `@@ -227,3 +227,11 @@`, 8 `+` lines, zero `-` lines;
`--numstat` = `8 0`. The correction sits at the file end (:231-237 of 237). Working tree matches the tip
(`git diff --quiet 39c59630 -- <lesson>` clean). No commit between base and tip other than `d9fec1d3`
touched the lesson, so the net diff is the landed correction itself.

## 3. Does it fully correct :197-199? — YES

- Line pointer is exact: the stale paragraph is precisely :197-199 in the current file (numbered re-read).
- Both false assertions are overturned with verification affordances: existence (note added `c8cb3930`,
  embeds the exact `git log --format='%h %ci' …` command a reader can run) and counter ("still 0/3" →
  closure re-measured 3/3, backed by the committed receipt above).
- The one true fragment inside the stale paragraph ("`corpus/knowledge/terminal-trees-r23.md` is absent at
  the base revision") is left uncontradicted and is true at the r23 base (`c8cb3930^` ABSENT); the
  correction's framing "read that paragraph as the pre-integration draft it was" preserves it.
- "Corrections sweep every mention" (the standard cited by spotcheck §7 defect 1): corpus-wide sweep of
  `does not yet exist|0/3 for ghostty|until the integrator creates` finds no other live false mention —
  hits are only the stale span itself (:197), the correction's quotation of it (:233), the spotcheck
  defect ledger (round-23-verifier-spotcheck.md:140-141, legitimate defect record), and lesson-24's
  repair entry (round-24.md:71, which correctly attributes the fix to `d9fec1d3`). Other "0/3" occurrences
  (round-23.md:8, :25) are true historical before-values, not stale claims.
- The routed instruction — "Append a correction" — is exactly what landed.

## VERDICT: holds

No finding against the round on this item. Residual risk: none identified beyond the noted benign
omission (the `3df1062` errata append is not enumerated in the correction's one-sentence history; it is
append-only itself and separately recorded). No tools were installed for this check.
