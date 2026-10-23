# AtkNoteProse — round 24 wave 2: prose attack on `corpus/knowledge/rule-attribution-r24.md`

Seat: `MadoR24.AtkNoteProse` (leaf reviewer, no spawns). Attack surface: the note's prose only —
decision table, negative sweeps, host join, limits — against (a) row-reference fidelity for every
A1–A26 citation, (b) overreach, (c) observation/inference labelling, (d) provenance-header
completeness. All line numbers below are `corpus/knowledge/rule-attribution-r24.md` unless a path
is given. Review is text-level; no lsp server answers a markdown note, so no semantic-server
results are cited. No lane file besides this report was touched; no counter refetch was run.

## Verdict

VERDICT: partial — the note's substance holds under attack (no row reference is content-unsupported,
no hard overreach, header complete), but four citation-precision defects exist (D1–D4).

## Defects

### D1 (minor) — L31, L39, L41–42, header L1: three claim rows fail the frozen predicate; the note never says so
The wave-1 counted receipt `.ufo/waves/round-24/evidence/c1-after-cf86f9e0.txt` (refetch mode at
cf86f9e0) records `FAIL_ROW quote-off-topic` for **A5 (S155), A7 (S156), A8 (S156)**;
`PASS_ROW=23/26, distinct_sources=14`. The failure is mechanical: the quotes' only `rule` tokens
(`PRIORITY_WINDOW_RULE`, `RULE_PROP_NONE`, `eRuleProperty`) are underscore/letter-joined and yield no
`\brule\b` word-boundary match. I re-verified locally that the three quotes **are** verbatim in the
committed bytes (`grep -cF`: A5 → S155.bin:1; A7, A8 → S156.bin:1), so L31's "each quote re-opens
verbatim in its pinned bytes" is true. What is missing: L31's "counted by …count.py" framing presents
26 predicate-valid rows with no disclosure that 3 are not PASS_ROWs, and header L1 lists **S156 — the
only source with zero passing rows** (its rows A7/A8 both fail). Impact on TARGET_MET: none. Fix: one
disclosure clause at L31 (e.g. "A5/A7/A8 fail the counter's topic-word clause; quotes are verbatim").

### D2 (minor) — L27: A25 does not support the sentence it is cited for
Sentence: "Ordering still decides which value wins: named rules first, then anonymous, top to bottom,
last match wins (A21, A25, A26)." A21 (S165.bin:318, cross-rule last-wins — context S165.bin:300–320
shows two `hl.window_rule` lines "match both; last wins" and the kitty 0.8/0.5 example) and A26
(S168.bin:14, named-first) support it. **A25** (S168.bin:16 "_All_ props must match for a rule to be
applied") is a matching precondition, not ordering; it supports no clause of this sentence. Fix: drop
the A25 citation or add a clause about which rules participate.

### D3 (minor) — L25: "the workspace-rule path" mislabels A18's log path
The logs row says "the one matched-by log line is the workspace-rule path (A18)". A18's quote
("Rule workspace matched by {}, {} applied.") sits at S164.bin:2187 **inside `CWindow::mapWindow`**
(function head S164.bin:2052) and prints `m_ruleApplicator->static_.workspace` — i.e. the window-rule
`workspace` **effect** path. "workspace-rule path" collides with the note's own L21 usage of
"workspace rules" for the `workspacerules` feature (A24) — a different subsystem. Fix: "the window-rule
`workspace`-effect path".

### D4 (nit) — L82–83, L91: "only the key list was read" / "no tag value was read" understates the census
ScoutHostRules §5 ran jq presence/type/non-empty checks over all 4 clients (`has("tags")`,
`tags|type`, `(.tags|length>0)`): the tags field of every client was evaluated, though no tag string
was printed or recorded. The parenthetical's discipline claim is honest in spirit but imprecise; the
accurate form is "no tag string was read or recorded".

## Attacked and verified clean
- **Header L1–3**: `source:`/`verified-at:`/`recheck:` all present and substantive (plus `covers:`/
  `author:`). All 15 listed S### have status `mined`, opened `2026-10-23`, used-by this note
  (corpus/SOURCES.md:165–180); S161 (`queued`, used-by `—`) is correctly excluded from both header and
  claim rows. L1's pin identity confirmed: host `hyprctl version` first line names `efb50993…` (run
  read-only this seat), wiki clone HEAD = `c66e8de2` 2026-10-22.
- **Decision table L20–25**: every other citation supports its sentence — A11 (getprop opacity branch
  → applicator alpha; matches HyprCtl.cpp:1548-1553 in ScoutAttributionSweep), A24 (workspacerules
  lists workspace rules), A10+A22 (tags in clients; `*` suffix), A9+A10 (tag keeper is the matching
  state and the clients source), A12–A14+A23 (Lua handle set_enabled/is_enabled), A5–A8 (value+mask+
  priority content-true even though A5/A7/A8 fail the counter's topic clause — D1), A18 (log text
  existence). Negative cells ("does not show") trace to the sweeps, which are labelled L76.
- **Negative sweeps L64–74**: every anchor and count matches the cited reports — HyprCtl.cpp:1548-1553
  and `:2005`, LuaWindowRule.cpp:58-70, 35 socket2 event names with 0 rule-bearing, OverridableVar.hpp:153
  one optional per priority, `getPriority()` unexported, `updateRules` carries the window only,
  "15 log calls … none prints a rule name; five TRACE-gated" verbatim matches SrcRuleLogSweep,
  `IRule::name()` consumers, unnamed inline rules at legacy/ConfigManager.cpp:2019, block rules keyed by
  `name` (A15/A16).
- **Host join L80–85**: all figures match ScoutHostRules exactly (82 = 77 inline + 3 block + 2 layerrule
  sourced; 3 named omarchy block rules `geforce`/`jetbrains-focus`/`moonlight`; 21 tag-effect lines;
  4/4 clients with `tags`; "which rule produced a given tag is still not observed" matches the report's
  §7).
- **Limits L89–93**: "latest-git" wiki supported (clone HEAD c66e8de2; ScoutWikiEra title/context);
  `configProvider: hyprlang` is a cited round-12 `[OBS]` (hyprland-config-era-r12.md:82, via
  `hyprctl systeminfo`) — not re-observed 10-23, but header L2 honestly scopes the 2026-10-23 host
  re-verification to `hyprctl version` + clients key list. `[INF-docs]` (L90), `[UNK]` (L91),
  `[INFERENCE]`/not-checked (L92–93) labels present and correctly placed; L28–29 labels the replay
  attribution an inference.
- **Provenance L97–122**: all 12 cited wave-1 reports exist; drafting attribution spot-checked
  (SrcRuleEngine.md ↔ registerRule; SrcHyprCtl.md ↔ alphaToString/m_tagKeeper.getTags, 11 hits).
- **Covers L4**: the round-12 bullet "Still open: rule *attribution*" exists verbatim at
  corpus/README.md:105; the move is announced at README:201–204.

## Residual risk and gaps
- L69 "Verdict NEGATIVE on every channel" carries none of ScoutAttributionSweep's own depth caveat (no
  field-by-field LuaLayerSurface sweep; the layer conclusion rests on the shared applicator/priority
  model plus the 0-hit socket2/Lua-query sweeps). Faithful to the report's verdict table, but the caveat
  lives only in the report.
- README:105 still lists attribution as "Still open" inside the historical round-12 bullet while
  README:201–204 announces the move — README-side reviewers' lane (AtkReadmeFrontier), not a note defect.
- Did not re-run the counted C1 counter (no refetch from this seat; receipt cf86f9e0 + sibling
  ReRunC1Tip cover it). A5/A7/A8 verbatim checks were local `grep -cF` against committed
  `.ufo/waves/round-24/fetch/S15{5,6}.bin`.
- Did not open all 12 provenance reports end-to-end to confirm each drafted its exact rows (existence +
  two spot-checks only).
- No tool was installed or updated; no git/jj command ran in the lane; hyprctl use was the read verb
  `version` only.
