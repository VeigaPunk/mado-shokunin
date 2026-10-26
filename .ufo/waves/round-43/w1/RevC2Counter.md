# RevC2Counter — attack PRED-C2-r43: forgeries that are admitted

Target: `quality/counters/c2-r43-gkeep-entry.py` (PRED-C2-r43), reviewed against its docstring
clause by clause and attacked with 16 fixture repos built from the frozen control runner's own
helpers (`base_files`/`admitted`/`set_receipt`/`rep`/`score`), each scored by the UNMODIFIED
frozen counter (`kind="real"`), fixture repos under `/fast/scratch/hyaku/mado-r43/RevC2Counter`
(removed after the runs; `git -C` everywhere; run-6 rules honored). Harness sanity: the
runner's control P admits under the same driver, consistent with `receipts/ctl-c2.txt` (74/74).
The counter was only read, never edited.

Result: 9 admitted forgeries in 8 findings + 5 verified negatives. Full detail, counter line
citations, and per-fixture counter output in
`.ufo/waves/round-43/w1/RevC2Counter/findings.md`.

## Findings (severity, counter line, fixture → observed)

- **F1 MEDIUM** — held-id receipt unpinned (`:416-419`): a held id (S050) admits a fully
  fabricated receipt (bytes + quote + claim invented, e.g. "engine matches classes with Python
  re unanchored") at a true locator. Fixture R1 → `admitted=1/1`. Declared residual, but it is
  the only channel admitting invented evidence. Fix: pin held ids to their BASE-tree sha.
- **F2 MEDIUM** — clause d's "no GATE S### line outside that section" bypassed twice
  (`:403-406`, `unfenced`): (a) a byte-identical GATE line duplicated under a later `## Notes`
  is never counted (`in_gate` set bypass); (b) a fenced decoy GATE line with a wrong sha and
  invented quote is invisible to every check. Fixtures R2, R2b → `admitted=1/1`, `d:1`.
- **F3 LOW-MED** — locator `file:42x` (garbage after the line number) passes: `:490-493`
  lookahead blocks only digits; `loc_ok` at `:488-489` is dead code. Fixture R3 → `admitted=1/1`.
- **F4 LOW-MED** — junction-space line mapping off-by-one (`:245-246`): a quote whose first
  char is the collapsed newline-space maps to the line BEFORE its words; entry cites `:2`,
  words are on line 3, admitted. Fixture R6b → `admitted=1/1`, `g:1`.
- **F5 LOW** — `recheck:` prefix-matched (`:110`, `:211-218`, `:364`, `:378`): entry
  `recheck: 90d whatever junk` (R10) and registry cell `90d and-never-recheck` (R9) both →
  `admitted=1/1`. Fix: `re.fullmatch` the stripped token.
- **F6 LOW** — entry claim line may carry the gate quote mid-word (`:490`, `q in l`
  substring, no boundary rule on the entry side). Fixture R5 (`Xm_box = box;Y garbled claim`)
  → `admitted=1/1`.
- **F7 LOW** — locator inside a longer path (`archive/deep/Hyprland-Target.cpp:42`) passes
  (`:493` lookbehind allows `/`). Fixture R4 → `admitted=1/1`.
- **F8 LOW** — own-work row location points elsewhere (`elsewhere/host-gkeep.conf.bak`
  passes clause c (`:388`) and clause e containment+uniqueness). Fixture R7 → `admitted=1/1`.
  Census unaffected (clause h reads gated receipts, not locations).

## Verified negatives

Duplicate `recheck:` in window → rejected; pinned-receipt byte edit → rejected (`d:0 h:0`);
`..` path traversal in a Gate receipt path → git refuses to resolve `..` in `rev:path`,
rejected; `recheck: on-2027-01-01` → rejected; census "trivial total" hint → no forgery
available (values recomputed from pinned bytes and matched verbatim); `rxc.fullmatch` ≡
RE2::FullMatch for the pinned RX `^(org.omarchy.gkeep)$`.

## Residual risk / gaps

Quote-to-claim binding stays out of the counter's reach (declared; F1 is its maximal form).
HTML-receipt locators unchecked (declared; not re-tested). Only the named edge families were
fuzzed. No tools installed. The counter, runner, registration, controls and fetch receipts
were not modified.

Report: .ufo/waves/round-43/w1/RevC2Counter.md
