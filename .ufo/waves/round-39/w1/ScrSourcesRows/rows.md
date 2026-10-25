# SOURCES row drafts — round-39 w1 (ScrSourcesRows)

Draft rows for the round-39 registry addition: S218/S219/S220 (new, opened
2026-10-25, status mined) plus the S018 used-by old→new change line. Format
mirrors `corpus/SOURCES.md` § Registry (11 columns, pipe-delimited, no pipe
inside any cell). Receipts and quotes come from ExecAssimFetches
(`.ufo/waves/round-39/w1/ExecAssimFetches.md` + `.bin` files); both quotes were
independently verified against the receipt bytes.

## New rows

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S218 | Hyprland wiki — Variables (0.56.0) — https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/ | docs | A | The documented option-declaration syntax on the host's release line: hl.config() invocations merge per-category instead of replacing the whole configuration, so later declarers override only the options they pass | rendered text §Syntax (`#syntax`), first prose paragraph after the `hl.config ({ category = { value = ... } })` example: "You are allowed multiple hl.config() invocations, each one will update just what you pass into it." @ page revision "Last updated on July 17, 2026", 364905 B, sha256 `400d18195020316c25e1874e567d868458b69e342a019b3ec8da6211d7222801`; receipt .ufo/waves/round-39/w1/ExecAssimFetches/S218.bin | options are declared via hl.config() calls and repeated calls merge, each updating only what is passed — the last declarer's values take effect (the last-declarer/option-syntax ground) | mined | 2026-10-25 | on-release | corpus/knowledge/config-option-table-r39.md |
| S219 | mado options tool — tools/mado-options.py | own-work | A | The static resolver of the config-tree option table (all non-bind/non-animation/non-workspace/non-rule `key = value` settings) through the Hyprland source graph, with last-declarer ownership resolution and an optional `--getoption` live-value merge | committed bytes at data tip — INCOMPLETE: receipt missing at fetch time (no data commit; HEAD 457d1b125932c1e0d797061a2156b917bcd7edaa freeze; tool absent from worktree and every ref, `ls tools/mado-options.py` exit 2, `git log --all -- tools/mado-options.py` empty); no sha256 fabricated | the tool delivers the option-ownership table C2 claims, resolving each key to its last declarer with the divergence vocabulary (agreement/agreement*/live-default/mismatch/config-only) | mined | 2026-10-25 | on-change | corpus/knowledge/config-option-table-r39.md |
| S220 | Hyprland wiki — Dispatchers (0.56.0) — https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/ | docs | A | The Lua dispatcher surface as published for the host's own release line (0.56.0 docs) — how dispatcher registry entries resolve to actions through hl.bind()/hl.dispatch(), grounding the dispatcher-surface/request-grammar amendment | rendered text opening section: "Their purpose is to be fed into hl.bind() or hl.dispatch()." (immediately preceded by "Dispatchers return tables that describe an action you want to make. They do not invoke any action immediately, and their contents are not guaranteed to be stable at all.") @ page revision "Last updated on July 15, 2026", 297863 B, sha256 `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2`; receipt .ufo/waves/round-39/w1/ExecAssimFetches/S220.bin | dispatcher entries are inert tables fed into hl.bind() or hl.dispatch(); they do not invoke any action immediately — the resolution surface the amendment's request-grammar section rests on | mined | 2026-10-25 | on-compositor-release | corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md |

## S018 used-by change line (old→new)

| S018 | used-by | corpus/knowledge/window-rule-effects-getprop.md | corpus/knowledge/window-rule-effects-getprop.md, corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md | the admitted dispatcher amendment re-reads HyprCtl.cpp (S018) for the dispatcher-name-resolution quotes (`:1149` DISPATCHER lookup, `:1151` "Invalid dispatcher", `:1309` batch split, `:2096` flag strip, `:1132` Lua wrap) — a second citation on the held row, not a new row |

## Notes

- S219 is the only row missing its receipt (sha256 of the committed tool bytes).
  ExecAssimFetches marked it unverifiable: no round-39 data commit had landed and
  `tools/mado-options.py` exists in no ref. The row stays structurally complete
  but is flagged INCOMPLETE in its anchor cell; it must be completed by hashing
  `git show <data-tip>:tools/mado-options.py` once the data commit lands.
- Conflict reported verbatim: S196 already covers the same 0.56.0 Dispatchers
  page (same URL, same sha256 prefix `f9b51362f2440e02`, opened 2026-10-24,
  used-by `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md`).
  Registration assigns "the 0.56.0 Dispatchers page → row S220"; drafting S220 as
  a fresh row with this round's receipt as instructed creates a duplicate-URL row
  (census W04 risk). Left for the judge to resolve; S220 drafted per instruction.
