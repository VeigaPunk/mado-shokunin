# RevLesson — w2 review of `corpus/lessons/round-43.md` (data commit `1959770657f1f8665097c1aed4be6c1cbb07139f`)

Verdict: the lesson's core Gate is sound — all ten GATE sha256s recompute exactly and all ten quotes pass the v2
counter's own functions (`quote_at`/`occurrences`/`quote_in_code`: one word-bounded occurrence each, outside
comments, absent from the other receipts, 3-11 words); every checked Mistakes line pointer resolves at its cited
rev; M43-1's and M43-3's shown-able-to-fail re-run as claimed. Eight defects found, none of them flips a claim
verdict; three are major (one leaves the registered tip condition without any receipt).

## Findings (full evidence and fix text in `.ufo/waves/round-43/w2/RevLesson/findings.md`)

- **F1 (major)** — Census section cites `receipts/c1-after-tip.txt` and `receipts/c2-after-tip.txt`; neither exists
  at any ref or on disk. The kill rule scores "at the data commit and at the tip", so the tip half of both claims
  has no receipt (criterion 79 / the M43-3 class). Fix: run and land them, or drop the "at the tip" clauses.
- **F2 (major)** — the Gate paragraph's "Locators the entry carries (computed)" lists start lines `:70`, `:428`,
  `:50`, `:33` for four ids whose landed entry locators are the ranges `:70-71`, `:428-429`, `:50-51`, `:33-34`
  (M43-7's own fix); M43-1's fix text repeats the stale `<receipt>:<line>` form. Fix: the four range forms.
- **F3 (major)** — Gate anecdote "the clients JSON [draft quote] occurred twice … (two 1720x1414 objects)" is
  wrong twice over: the scribe drafts' clients-JSON quotes occurred once (ScrLessonSkeleton) and four times
  (ScrEntryB, lines 6/21/36/51) — never twice — and the receipt holds four 1720x1414 objects (S296's own row says
  so). The HyprCtl half (occurred twice, 427 and 447-448) verifies.
- **F4 (moderate)** — M43-4's "Shown able to fail" cites `receipts/c2-after-data.txt`, which records the PASS
  (`gates=1 bound=1`, `d:1`, `admitted=1/1`); the fail was never run. This seat demonstrated it on a scratch
  fixture (Gate section removed from the data tree): `gates=0 bound=0` per id, `clauses=… d:0 … admitted=0`,
  `admitted=0/1 verdict=TARGET_MISSED`, exit 1 — receipt `w2/RevLesson/receipt-nogate-demo.txt`.
- **F5 (moderate)** — `receipts/census-after.txt` never exists under that name; the receipt is
  `receipts/census-after-data.txt` (bytes match the expected W04 ×7 + W01 S277 set, exit 0).
- **F6 (moderate)** — four present-tense claims that only became true at `2a3707c`: LOG.md Round 43
  (correction first bullet, 38-seat record) absent at the data commit; the after-data counter receipts absent there;
  M43-6's w1 `.md` count was 0 at the data commit (38 at 2a3707c); `.ufo/reports/round-43/mado.md` (SHONEN box 2
  holder) exists nowhere yet. Fix: date them to the w1-evidence commit / closure.
- **F7 (minor)** — M43-3's six-file `NO_MATCHING_CLIENT` enumeration at `a62f2e0` omits
  `.ufo/waves/round-42/w1-dispatch.json` (7 files, "never in a run receipt" still holds).
- **F8 (minor)** — M43-2's fix pointer `registration.md:59` carries the count but not the definition (lines 60-61);
  should be `:59-61` by the round's own criterion 77.

## Verified clean (highlights)

Ten GATE hashes+quotes (counter's own functions, re-run); M43-1 line pointers (`LOG.md:2483`, r42
`registration.md:61`, grep lines 426-428/447-448, 394-395/412-413 template fields, `da384db4` non-resolution,
closure `:83-84`) and its shown-able-to-fail re-run (base-LOG MISS, exit 1; landed `quality/check-locators.py`
byte-identical to the ExecLocatorGate deliverable, sha c1ea52ad…; entry run `locators=10 miss=0`); M43-2 numbers
(46/47/45, 48 ok, 38 M*, runner `:139`); M43-3 (LOG no-hit re-run, live receipt 11 lines, in the data commit);
M43-5 (488-line file, `44d43` blank line, r43 header/45 lines/empty diff, both sha256s); M43-6 (watchdog line,
29 files/0 reports, spec 38); M43-8 (17-line entry, 1/1 v1, 0/1 v2 receipts); the assimilation ledger's package
claims (r11 S302-S305+S310, r8 S275/round8-path, r10 §1, r30 comment, r9/r12/r13/r15/r31); registry 226→234,
entries 59→60, SOURCES diff = 8 appends + S155/S158 one-item used-by appends, census receipts, axis receipt,
QUALITY 77-81 landed.

## Residual gaps

M43-8's "prompt §6 item 9" quote is not a repo artifact (substance corroborated by the v1/v2 diff and the X3
receipts); M43-7's draft-MISS run (`miss=4`) has no committed receipt; axis and live-host receipt bytes accepted as
pinned (no re-derivation, no compositor read). No tools installed; no pacman; scratch deleted.
