# Seat CritC1Contract — w2 FALSIFY report (round 47, wave w2)

Goal: break the C1 contract docstring (`.ufo/waves/round-47/l1-draft/mado-terminal.py`
lines 2-88) against the pinned real script `.ufo/waves/round-47/fetch/xdg-terminal-exec`
(sha256 `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`, verified). Full detail,
evidence and the reproducible driver: `.ufo/waves/round-47/w2/CritC1Contract/findings.md`
(+ transcripts `results2.log`/`results3.log`/`results4.log`, `pin.sha256` in the same dir).

Method: hermetic per-case scratch trees (all XDG_* and HOME inside scratch; XDG_CONFIG_DIRS /
XDG_DATA_DIRS isolated to empty dirs so the host cannot leak in; cold cache; only
`--print-*`/`--test`; no empty argv elements; `timeout 25`; XTE_DEBUG=true to observe reads).
~60 pin runs. No tool installs, no package transactions, no host writes.

## Findings

- **No hard FALSE sentence found** among the resolver-testable claims: every tested sentence
  matched the pinned script (see the verdict table in findings.md).
- **MISLEADING (fixture-parity consequence), docstring line 65-66**: "tokenized by the
  shell-quoting rules … its field codes stripped … reject otherwise". `de_tokenize_exec` /
  `de_strip_fields` failures are **ignored** by `check_entry_key`; malformed Exec strings are
  accepted with the partial/raw `$XTE__EXEC_USEP`. Proven with real fixture lines:
  `Exec=alacritty %z` → accepted, prints `alacritty\n%z` (results2.log p19_unknownfield);
  `Exec=foot )` → accepted, prints `foot` (results4.log p45_tokerr);
  `Exec=alacritty "unclosed` → accepted, prints `alacritty\nunclosed` (results4.log p46_unclosed).
  A strict implementation (rejecting on tokenizer/strip failure) diverges from the oracle on
  existing C1 fixtures.
- **MISLEADING wording, line 47**: "Plain lines are kept verbatim" — there are no plain lines;
  only validated entry-id lines survive; everything else is ignored (the next sentence says so).
- **Incomplete environment list, lines 28-29**: resolver also reads `XTE_DEBUG`/`DEBUG` and
  `LC_ALL`/`LANG` (stderr volume and self-re-call).
- **UNTESTABLE (tool absent — no data commit yet)**: lines 4, 13-16 (tool half), 17-24
  (explain), 25-26 (selftest), 83-84 (tool half). Their resolver halves are supported
  (no-print-option reaches `exec "$@"`, pin x:1499).

## Verified-true highlights (full evidence in findings.md)

Lowercasing/split-empty semantics; list-file order incl. XDG_DATA_DIRS subdirs and trailing-slash
removal; non-regular/unreadable list behavior (exit 1 errexit); NUL drop-and-merge; unterminated
last line ignored; directives first-of-pair and env-wins both directions; `/execarg_default`
compat-only; +/- exclusion/inclusion first-word-wins with explicit-listing unaffected; find/id
mapping/last-path-wins (DATA_HOME beats DIRS); `CategoriesX=` whole-text matching; OnlyShowIn/
NotShowIn case-sensitive fallback-only; escape expansion; TryExec/Hidden; command -v
aliases/functions/builtins/reserved words/abspath/empty-PATH=cwd; while-loop-status rejection;
cross-entry inheritance without reset; execarg default `-e` vs strict skip; no-candidate message
rc 1; print order (words, app-id, title, dir, hold, execarg, command), `/./` fold, action suffix,
delimiters via `printf %b` without trailing newline, `--test` shape, `--print-content` dropping
unterminated last lines; cache only rewritten on `--print-cmd` (not id/path alone) and invalidated
on change.

## Hygiene

All writes inside the seat dir and `/fast/scratch/hyaku/mado-r47/CritC1Contract/` (scratch
deleted after evidence copy; logs kept in seat dir). No mutation of the lane, fleet, or host
state; no terminal launched; no empty argv elements; cache always redirected into scratch.
