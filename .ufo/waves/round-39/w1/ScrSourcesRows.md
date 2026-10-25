# ScrSourcesRows — round-39 w1 report (2026-10-25)

## Task

Draft the SOURCES registry rows S218/S219/S220 (+ S018 used-by old→new change
line) as the exact 11-column rows in
`.ufo/waves/round-39/w1/ScrSourcesRows/rows.md`, using fetch receipts from
ExecAssimFetches; mark incomplete rows if a receipt/quote is missing.

## Deliverable

- `rows.md` written at `.ufo/waves/round-39/w1/ScrSourcesRows/rows.md`
  (5,074 bytes), containing:
  - 3 new rows S218/S219/S220 (status mined, opened 2026-10-25, recheck
    on-release / on-change / on-compositor-release), no pipe inside any cell,
    used-by exactly the admitted entries (config-option-table-r39.md /
    dispatcher-surface-and-request-grammar-r26.md).
  - 1 change line `| S018 | used-by | old | new | reason |`.
- No other file written. No tools installed (none needed; python3/curl already
  present — no pacman/npx/uv action).

## Evidence used

- ExecAssimFetches report: `.ufo/waves/round-39/w1/ExecAssimFetches.md`
  (S218 sha256 `400d18195020316c25e1874e567d868458b69e342a019b3ec8da6211d7222801`,
  S220 sha256 `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2`).
- Receipt bytes verified by me:
  - `sha256sum S218.bin` → `400d1819...2801`, 364905 B; quote "You are allowed
    multiple hl.config() invocations, each one will update just what you pass
    into it." found verbatim in extracted text line 282 (16 words ≤ 25).
  - `sha256sum S220.bin` → `f9b51362...6e2`, 297863 B; quote "Their purpose is
    to be fed into hl.bind() or hl.dispatch()." found verbatim in extracted text
    line 260 (10 words ≤ 25).

## Findings

1. **S218** complete: receipt + quote present, both independently verified.
2. **S219 INCOMPLETE**: own-work receipt (sha256 of committed
   `tools/mado-options.py` at data tip) is missing. At fetch time HEAD was
   `457d1b125932c1e0d797061a2156b917bcd7edaa` (freeze commit); no round-39 data
   commit had landed; `tools/mado-options.py` absent from worktree
   (`ls` exit 2) and from every ref (`git log --all -- tools/mado-options.py`
   empty). No sha256 fabricated; the row is flagged INCOMPLETE in its anchor
   cell and must be completed by hashing `git show <data-tip>:tools/mado-options.py`.
3. **Conflict reported verbatim (for the judge)**: S196 already covers the same
   0.56.0 Dispatchers page (same URL, same sha256 prefix `f9b51362f2440e02`,
   opened 2026-10-24, used-by `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md`).
   Registration says "the 0.56.0 Dispatchers page → row S220"; S220 was drafted
   per instruction with this round's receipt, which creates a duplicate-URL row
   (census W04 risk). Not resolved by me — scribe only.
4. S018 change line: used-by `corpus/knowledge/window-rule-effects-getprop.md`
   → `corpus/knowledge/window-rule-effects-getprop.md, corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md`,
   reason names the five amendment quotes (`:1149`, `:1151`, `:1309`, `:2096`,
   `:1132`).

## Scope safety

- Only wrote to my seat dir (`w1/ScrSourcesRows/rows.md`) and the named report
  path (`w1/ScrSourcesRows.md`). No tracked file edited; no git/jj mutation; no
  host action; no installs.
