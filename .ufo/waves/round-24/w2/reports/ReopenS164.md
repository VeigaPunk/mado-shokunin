# Wave 2 — reopen SOURCES S164 and claim row A18

Seat: `MadoR24.ReopenS164` (reviewer, leaf). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, master at
`39c596307333b8ca0a1e42b3f3b9a748bb8b208b`, round base `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122`.
Attacked: SOURCES row S164 (`corpus/SOURCES.md:176`) and its single citing claim row A18
(`corpus/knowledge/rule-attribution-r24.md:52`). No file edited except this report. No tool installed or updated.
All commands wrapped in `timeout`; work done in `/fast/scratch/hyaku/mado-r24/w2/ReopenS164/` and the read-only
clone `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`.

## 1. Pin and bytes — re-fetched by this seat

Row URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp`

| Check | Row says | Observed by this seat |
|---|---|---|
| fetch | — | `http=200 bytes=124226` (curl `-sS -L`, no auth, no challenge) |
| sha256 | `sha256:d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded` | `d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded` — match |
| byte count | 124226 B | 124226 B — match |
| committed fetch `.ufo/waves/round-24/fetch/S164.bin` | — | sha256 `d735d454…`, 124226 B; `cmp` vs my refetch: **byte-identical** |
| local clone copy `src/desktop/view/Window.cpp` | — | sha256 `d735d454…`, 124226 B |

Pin resolution, both ways:
- local clone: `git rev-parse v0.56.2` = `git rev-parse 'v0.56.2^{commit}'` = `efb50993780079460b0cbed1363e2166a2de1d9f`;
  `git cat-file -t efb5099…` = `commit`; `git describe --tags --exact-match efb5099…` = `v0.56.2`.
- network: `git ls-remote https://github.com/hyprwm/Hyprland refs/tags/v0.56.2` →
  `efb50993780079460b0cbed1363e2166a2de1d9f	refs/tags/v0.56.2`.

The URL pins a 40-hex commit (not a branch), matches the tag object, and the bytes are reproducible.

## 2. Row-field audit against the frozen PASS_ROW predicate

`corpus/SOURCES.md:176` cells, printed in full by this seat:

- id `S164`; status `mined`; opened `2026-10-23`; recheck `on-release`; used-by
  `corpus/knowledge/rule-attribution-r24.md` — all required by the predicate.
- anchor `src/desktop/view/Window.cpp:103-108,141-146,1484-1486,1791-1795,2143-2281,2497 @ commit efb5099…,
  sha256:d735d454…, 124226 B` — sha256 carries the `sha256:` label (repair 4), byte count matches.
- Anchor ranges re-read in the pinned bytes: `103-108` / `141-146` construct
  `m_ruleApplicator = makeUnique<Desktop::Rule::CWindowRuleApplicator>(…)` in both `CWindow::create`
  overloads; `1484-1486` calls `m_ruleApplicator->propertiesChanged(RULE_PROP_TITLE | RULE_PROP_CLASS)`;
  `2497` calls `propertiesChanged(RULE_PROP_ALL)`; `2143-2281` is the `setStaticProps` lambda inside
  `void CWindow::mapWindow()` (`:2052`) applying `m_ruleApplicator->static_.*` to window state.
- Evidence cell claim "the source does not identify a particular originating config rule" — verified against
  the whole file: zero occurrences of `IRule`, `CRuleEngine`, `ruleEngine` or `->name()`; the only two
  rule-word log calls are `:2167 "Rule monitor, applying to {:mw}"` and `:2187` (the A18 quote), neither
  printing a rule identity.
- Citation-hygiene note (not a defect of A18): range `1791-1795` is `CWindow::xdgTag()` (reads
  `m_xdgSurface->m_toplevel->m_toplevelTag`); the evidence cell does not mention tags, so that range is
  unaccounted for in the row's own summary.

## 3. A18 — per-criterion verdict

Claim cell (`rule-attribution-r24.md:52`): "CWindow log text says `Rule workspace matched by` and contains
two `{}` placeholders before `applied`."  Quote: "Rule workspace matched by {}, {} applied." (7 words).

**(a) Quote verbatim — HOLDS.** `grep -nF 'Rule workspace matched by {}, {} applied.'` on my refetched bytes
returns exactly one hit, `:2187`:
`Log::logger->log(Log::DEBUG, "Rule workspace matched by {}, {} applied.", m_self.lock(), m_ruleApplicator->static_.workspace);`
The literal is inside the cited anchor range `2143-2281`; no other occurrence exists in the tree
(`grep -rn 'Rule workspace matched by' src/` → only `src/desktop/view/Window.cpp:2187`).

**(b) Claim true of the bytes, no overreach — HOLDS.** The log call sits inside the `setStaticProps` lambda of
`void CWindow::mapWindow()` (`:2052`, lambda opens `:2143`), so "CWindow log text" is accurate. The format
string begins with `Rule workspace matched by`; it contains exactly two `{}` and both precede `applied`. The
claim asserts nothing about the placeholders' values, log level, or that the message names a rule — no
overreach to falsify.

**(c) Attribution content — DOES NOT HOLD as worded.** The row asserts only the existence and shape of a log
format string. It does not state what the message exposes (per the bytes, the two arguments are the window
handle `m_self.lock()` and the matched workspace value `m_ruleApplicator->static_.workspace`) and does not
state the attribution-relevant negative (no rule handle/name is printed). That negative is what the note's
answer table actually uses — "logs: none name a rule; the one matched-by log line is the workspace-rule path
(A18)" (`rule-attribution-r24.md:24`) — and it is true of the bytes (only occurrence of `matched by` in the
file sits inside `if (!m_ruleApplicator->static_.workspace.empty())`), but it is established by the separate
`SrcRuleLogSweep` over `src/desktop/rule/` and by the SOURCES evidence cell, not by A18's own sentence. As
written, A18 is log-formatting trivia: it names no rule-produced effect and states nothing about what exposes
rule identity. An attribution-wording would be, e.g., "the only CWindow rule log, emitted on the
workspace-rule path, prints the window and the matched workspace value and no rule name."

## Verdict

- S164 pin, sha256, byte count, committed fetch copy: **hold** (re-fetched, byte-identical, tag `v0.56.2`
  resolves to the pinned commit locally and over the network).
- A18 (a) verbatim and (b) truth/no-overreach: **hold**.
- A18 (c) rule-attribution content: **fails as worded** (formatting claim; the attribution point lives in the
  answer table and the SOURCES evidence cell, not in the claim row).

VERDICT: partial
