# ExecAssimFetches — round-39 w1 receipt fetch report (2026-10-25)

Task: fetch receipt bytes for admitted rows S218/S219/S220; one receipt line per row
(path, sha256, quote, anchor, access date). Access date for all rows: 2026-10-25.
All receipts saved under the seat dir `.ufo/waves/round-39/w1/ExecAssimFetches/`.

## S218 — Hyprland configuration/option-syntax documentation (Variables page, 0.56.0)

- Receipt path: `.ufo/waves/round-39/w1/ExecAssimFetches/S218.bin` (full:
  `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-39/w1/ExecAssimFetches/S218.bin`)
- URL: `https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/`
  (`curl -L -sS` → HTTP 200, final URL unchanged, 364905 bytes)
- sha256: `400d18195020316c25e1874e567d868458b69e342a019b3ec8da6211d7222801`
  (re-fetch byte-identical to first fetch; deterministic)
- Quote (16 words): "You are allowed multiple hl.config() invocations, each one will
  update just what you pass into it."
- Anchor: Variables page, §Syntax (heading `Syntax`, in-page anchor `#syntax` present in
  HTML), first prose paragraph after the `hl.config ({ category = { value = ... } })`
  syntax example; page revision footer "Last updated on July 17, 2026".
- Grounding: the page is the 0.56.0 option-syntax documentation; the sentence grounds
  the last-declarer/option-syntax claim — options are declared via `hl.config()`
  invocations and repeated invocations merge, each updating only what is passed (the
  last declarer's values take effect). Supporting syntax line (verbatim):
  `hl.config ({ category = { value = ... }, category2 = { value2 = ... } })`.

## S220 — Dispatchers page (0.56.0)

- Receipt path: `.ufo/waves/round-39/w1/ExecAssimFetches/S220.bin` (full:
  `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-39/w1/ExecAssimFetches/S220.bin`)
- URL: `https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/`
  (`curl -L -sS` → HTTP 200, final URL unchanged, 297863 bytes)
- sha256: `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2`
- Quote (10 words): "Their purpose is to be fed into hl.bind() or hl.dispatch()."
- Anchor: Dispatchers page, opening section ("Dispatchers return tables that describe an
  action you want to make. They do not invoke any action immediately, and their contents
  are not guaranteed to be stable at all." — immediately preceding the quote); page
  revision footer "Last updated on July 15, 2026".
- Grounding: states how dispatcher registry entries resolve to actions through the Lua
  API surface (`hl.bind()` / `hl.dispatch()`), the dispatcher-surface/request-grammar
  amendment theme.

## S219 — own-work receipt (mado-options.py at data tip): UNVERIFIABLE at fetch time

- Requirement: sha256 of `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-options.py`
  committed at the data tip.
- Evidence at fetch time (2026-10-25, during w1 execution):
  - `git rev-parse HEAD` → `457d1b125932c1e0d797061a2156b917bcd7edaa` (freeze commit
    "round-39: freeze registration + base receipts + inherited r38 seat reports"; HEAD of
    `master`, no data commit has landed yet).
  - `git log --oneline master -5` → tip remains `457d1b1`; no round-39 data commit.
  - `ls -la tools/mado-options.py` → exit 2, "No such file or directory" (tool not
    present in worktree).
  - `git log --all --oneline -- tools/mado-options.py` → empty (no ref/commit contains
    the file; checked all refs incl. `refs/jj/keep/*`).
- Status: S219 marked unverifiable (receipt pending) — the tool bytes are not committed at
  any tip during this fetch window. No sha256 fabricated. Re-run after the round-39 data
  commit lands: `git show <data-tip>:tools/mado-options.py | sha256sum`.
- No other files written besides S218.bin/S220.bin and this report.

## Environment / tooling

- No tools installed; `curl` and python3 (stdlib) were already available. No pacman/npx/
  uv action taken.
- Candidate URL probes (all returned HTTP 404, 924 B, unless noted):
  - `https://wiki.hypr.land/Configuring/Variables/` → 404
  - `https://wiki.hypr.land/Configuring/Hyprlang/` → 404
  - `https://wiki.hypr.land/0.56.0/Configuring/Hyprlang/` → 404
  - `https://wiki.hypr.land/0.56.0/Configuring/Variables/` → 404
  - `https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/` → 200 (used, S218)
  - `https://wiki.hypr.land/hypr-ecosystem/dev/hyprlang/` → 200 (candidate; contains only
    `$VAR = value` variable-definition syntax, no last-declarer/option-syntax sentence —
    not used)
  - `https://wiki.hypr.land/0.56.0/Configuring/Basics/` → 200 (nav-only page, not used)
  - `https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/` → 200 (used, S220)

## Final answer (≤6 lines)

1. S218 receipt saved: S218.bin, sha256 400d1819…2801, HTTP 200 @ 0.56.0 Variables page.
2. S218 quote: "You are allowed multiple hl.config() invocations, each one will update
   just what you pass into it." — anchor §Syntax, rev 2026-07-17.
3. S220 receipt saved: S220.bin, sha256 f9b51362…6e2, HTTP 200 @ 0.56.0 Dispatchers.
4. S220 quote: "Their purpose is to be fed into hl.bind() or hl.dispatch()." — opening
   section, rev 2026-07-15.
5. S219 UNVERIFIABLE: no data commit yet (HEAD=457d1b1, freeze), tool absent from worktree
   and every ref (ls exit 2; git log --all empty); no hash fabricated; re-run after data tip.
6. No tools installed; only S218.bin/S220.bin + this report written.
