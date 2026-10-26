# SimpEntryLesson — w2 dead weight in the landed entry, lesson and SKILL subsection

Target `1959770657f1f8665097c1aed4be6c1cbb07139f` (data); lane tip `2a3707c` for pointer re-checks. Attacks
`corpus/knowledge/hyprland-gkeep-geometry-r43.md`, `corpus/lessons/round-43.md`, `SKILL.md:246-288`
(`### Rule size versus reported size`). Nothing tracked in the lane was edited; every deletion was applied to a scratch
clone and the gate re-run there.

Deliverable: `.ufo/waves/round-43/w2/SimpEntryLesson/dead-weight.md` (exact before/after text per finding,
SAFE/UNSAFE against `PRED-C2-r43-v2`, tradeoffs, receipts).

## Findings

Dead (path resolves at neither the data commit, the tip, nor disk):

- **D1** lesson `:93` — `receipts/census-after.txt` does not exist; the receipt is `receipts/census-after-data.txt`
  (`cat-file -e` MISS at `1959770657f1` and at `2a3707c`; `ls .ufo/waves/round-43/receipts/ | grep census`). The same
  line is framed "expected: … exit 0" for a census that was run; replacement states the measured `mado ok`, exit 0.
- **D2** lesson `:205-208` — `receipts/c1-after-tip.txt` and `receipts/c2-after-tip.txt` exist in no commit and on no
  disk; the receipts dir holds 17 files, none a tip receipt. Replacement points at the spot-check counting command that
  already exists (`:198-199`). Consequence worth naming: the registration's target is "at the data commit and the tip",
  so the tip run is still owed — the deletion removes a false delivered-measurement claim, it does not supply the run.
- **D2b** same lines — the C2 v2 base was cited as `receipts/c2-before-base.txt`, whose first line is `PRED-C2-r43 …` (the
  v1 counter); the registered v2 base is `receipts/c2-v2-before-base.txt` (`PRED-C2-r43-v2 …`). Both say `admitted=0/1`,
  so the number was right and the pointer wrong.

Unverifiable as written (checked, not lifted from a w1 report):

- **U1** lesson `:124` — `receipt.txt:60` covers the `LOC … verdict=MISS` line (`:60`) but the quoted
  `CHECK_LOCATORS: locators=1 miss=1` is at `:61`; the M43-1 class inside M43-1's own record. → `:60-61`.
- **U2** lesson `:170` — `ls .ufo/waves/round-43/w1/*.md | wc -l` prints 38, not "36 or more" (the lesson states 38 at
  `:20`); a lower bound where the measurement is exact.
- **U3** lesson `:74` — with `-E`, `\|` is a literal pipe, so the cited
  `git grep -ciE 'set_default_size\|GEOMETRIC_GOAL\|…'` cannot match anything and cannot discriminate. The fact it is
  cited for holds: the corrected alternation also prints nothing at base (rc=1). Same escaped string sits in the frozen
  `registration.md:34`; the lesson should not carry the defect forward.

Redundant (each reads as a duplicate of a named sibling line):

- **R1** entry `:78` — "…; the GOAL is what every read verb reports" repeats table row `:27` and §3 `:56` (the only place
  with the `popin 87%` ground). Kept: the rest of the bullet.
- **R2** lesson `:29-30` — the held-row sentence repeats `:89-90` (exact old→new cells) and `:91`.
- **R3** `SKILL.md:278-279` — the prose restates the block under it (rule `size 420 500`, `clients=4`, `matched=0`); only
  the run conditions (date, no gkeep window open) are not in the block.
- **R4** `SKILL.md:286` — the first sentence restates the `NO_MATCHING_CLIENT` licence-table row `:272`; the
  operator-act/`[UNK]` part stays.
- **R5 (optional)** `SKILL.md:254` — `, command registered at ':2007'` is accurate (`:2007` is the `clients`
  registration) but not part of "what the reported size is"; the formatter is already located at `:395`/`:427-428`.

## Preserved contract (SAFE/UNSAFE)

- SAFE: R1 (no id on the line, so clause `g+` cannot bind it; not a census line), R2/R3/R4/R5 (no gate reads `SKILL.md`
  — `grep -rln SKILL quality/ scripts/` → nothing), D1/D2/U1/U2/U3 (lesson prose outside `## Gate` and outside the
  ADMIT/REFUSE lines; `score()` reads the lesson only at counter `:468`, `:477-479`, `:580-581`).
- UNSAFE and retained: entry `source:`/`verified-at`/`recheck` lines (clause b, i); the ten id-bearing claim lines
  `:32,34,40,42,44,46,52,54,60,66` (clause g + `all_body_lines_bound`, counter `:329-347`); the three census lines
  `:70-74` (clause h); lesson `GATE` lines `:34-43` (clause d); lesson `ADMIT`/`REFUSE` `:45-49` (clause i).

## Evidence

- `dead-weight.md`, `pointer-audit.tsv` (40 pointers × data commit / tip / disk: 25 at data, 11 late-landed, 4 dead),
  `receipt-dead-pointers.txt`, `receipt-c2-v2-after-deletions.txt`, `receipt-locators-after-deletions.txt`,
  `receipt-c1-after-deletions.txt`, `scratch-diff.txt` — all in `.ufo/waves/round-43/w2/SimpEntryLesson/`.
- Proof of retained behavior on scratch commit `c8c3769472f8f7c27302d9640fe328950dc7728b` (scratch clone of the lane at
  the data commit, all findings except R5 applied; `3 files changed, 13 insertions(+), 15 deletions(-)`):
  `PRED-C2-r43-v2: admitted=1/1 verdict=TARGET_MET` exit 0; `CHECK_LOCATORS: locators=10 miss=0` exit 0;
  `PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET` exit 0 (C1 untouched).
- Checked and retained, with the proof: `merge/mado/…` package ids are a document mapping (r11 `:11-14` = the four
  documents of S291-S294) and the package exists under the root `registration.md:77` names; the own-work pins match
  their originals (`sha256sum ~/.config/hypr/gkeep.conf` = `3726e488…`; gkeep HEAD `133b867`); the oracle controls in the
  entry (`floatonly` 200x200, `size300` 300x300, `nofloat` tiled) match `w1/ExecOracleGkeep/20-observation.txt` §5.
- No gate reads `SKILL.md`; no check was re-run to confirm a user/peer observation.

## Tool state

No tool installed or updated (`python3`, `git` from the system). Scratch clone under
`/fast/scratch/hyaku/mado-r43/SimpEntryLesson/` deleted at seat end; nothing of it is cited as evidence.
