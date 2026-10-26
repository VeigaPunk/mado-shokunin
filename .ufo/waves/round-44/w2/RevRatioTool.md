# RevRatioTool — w2 review of `quality/ratio-domain-meta.py` (mado round 44, 2026-10-26)

Target: `quality/ratio-domain-meta.py` at data commit `e46789213830597348fe96a351ae004d10587385`.
Identity: blob `c97cdb9` identical at data commit, tip (`290cddea`) and worktree; worktree sha256
`131c5c84993e4838d56ccfa5613e6a4d11592206149abb120fc76a352d46cfb0`, equal to w1's frozen
`w1/ExecDomainMetaRatio/receipts/tool-sha256.txt`; `cmp` proves `.ufo/waves/round-44/w1/ExecDomainMetaRatio/ratio.py`
byte-identical to the landed tool. Frozen rule: criterion 82 (`corpus/QUALITY.md:411` at the data
commit, seat copy `corpus-QUALITY-at-datacommit.md`), the tool docstring, and `--rule` output.

## Verdict

The tool does what criterion 82 records for its registered use: the published number reproduces
byte-for-byte at both revs I ran, my hand-classification agrees with the tool on **all 19 rows**
of rounds 34-44 (class and clause; 17/17 on the published 34-43 window), both criterion-82
mutants reproduce exactly, and the lesson carries the verbatim line plus one hand-labelled
disagreement. Five findings follow: one MEDIUM contract break on pre-round-34 windows, two
latent parser defects, one robustness gap, one registration-integrity note.

## What I ran (receipts in this seat dir; scratch under `/fast/scratch/hyaku/mado-r44/RevRatioTool/`, removed)

- `tool-34-44-why.txt` — `--from 34 --to 44 --why` at `e467892`: 19 rows, `DOMAIN_META: domain=14 meta=5 window=34-44 default=1`, exit 0.
- `tool-34-43.txt` — `--from 34 --to 43` at `e467892`: `domain=12 meta=5 window=34-43 default=1` = `SCORECARD.md:2583`'s published line.
- Lesson's exact command (`--rev 03fa5c6…` freeze, 34-43): same `domain=12 meta=5 window=34-43 default=1` = `corpus/lessons/round-44.md:255`.
- `legacy-13-33.txt` — `--from 13 --to 33` at `e467892`: exit 0, 53 rows scored, `domain=6 meta=47 default=31`.
- `abort-12-44.txt` — `--from 12 --to 44`: exit 3, zero rows (one round-12 row aborts the window).
- `synth-50.txt`, `synth-60.txt` — two synthetic fixture repos (built per the git-fixture protocol: `mktemp -d` under the scratch dir, `git init -q`, `rev-parse --show-toplevel` check, throwaway identity inside `$D` only).
- Edge probes at `e467892`: empty window 100-200 → exit 0 zeros; round 38 alone → exit 0 zeros; bad rev → exit 2 with stderr; `--from 44 --to 34` → exit 2; `python3` vs `python3 -I` diff → IDENTICAL.
- Mutants: `ratio-mutant-axis-token.py` on 34-43 → `domain=13 meta=4 default=0`; `ratio-draft1-no-clause2.py` → `40 | C1 | operability | meta`, `domain=11 meta=6`.

## Hand-classification (independent reading under the frozen rule)

Rule applied by hand over each row's bytes at `e467892` (flags parsed separately in `rows-parsed.json`):
clause 1 axis calibration; 2 operability + row carries `fixtures=`/`tool=absent|present`; 3 claim cell names
`tools/*.py|sh`; 4 claim cell names `corpus/knowledge/*.md`; 5 coverage + `admitted=` in row or entry-word in
claim cell; 6 claim cell names `SKILL.md`; 7 fail-closed meta.

| SCORECARD line | rnd | id | axis | tool (clause) | mine | agree |
|---|---|---|---|---|---|---|
| 2140 | 34 | C1 | coverage | domain (4, names waybar-module-text-route-r25.md) | domain (4) | yes |
| 2141 | 34 | C2 | calibration | meta (1) | meta (1) | yes |
| 2186 | 35 | C1 | coverage | domain (5, entry word; no `admitted=`) | domain (5) | yes |
| 2187 | 35 | C2 | calibration | meta (1) | meta (1) | yes |
| 2257 | 36 | C1 | calibration | meta (1) | meta (1) | yes |
| 2258 | 36 | C2 | operability | meta (7, no fixtures=/tool= token) | meta (7) | yes |
| 2369 | 37 | C1 | coverage | domain (5, `admitted=` in row) | domain (5) | yes |
| 2370 | 37 | C2 | operability | domain (2, fixtures=) | domain (2) | yes |
| 2435 | 39 | C1 | calibration | meta (1) | meta (1) | yes |
| 2436 | 39 | C2 | operability | domain (2) | domain (2) | yes |
| 2437 | 39 | C3 | coverage | domain (4, config-option-table-r39.md) | domain (4) | yes |
| 2480 | 40 | C1 | operability | domain (2) | domain (2) | yes |
| 2481 | 40 | C2 | coverage | domain (5) | domain (5) | yes |
| 2502 | 41 | C1 | operability | domain (2) | domain (2) | yes |
| 2503 | 41 | C2 | coverage | domain (4, hyprland-focus-grab-r41.md) | domain (4) | yes |
| 2535 | 43 | C1 | operability | domain (2) | domain (2) | yes |
| 2536 | 43 | C2 | coverage | domain (4, hyprland-gkeep-geometry-r43.md) | domain (4) | yes |
| 2570 | 44 | C1 | operability | domain (2) | domain (2) | yes |
| 2571 | 44 | C2 | coverage | domain (4, hyprland-gkeep-size-request-r44.md) | domain (4) | yes |

Zero disagreements. The lesson's hand-labelled row (`corpus/lessons/round-44.md:257-258`, round-36 C2:
axis-word reading would say domain, rule says meta, rule retained) is consistent with my reading; w1's
`receipts/hand-labels.txt` additionally hand-labelled 34 C2 (reader: domain) — also a non-rule reading,
correctly not carried as a second lesson row, since criterion 82 requires exactly one.

## Findings

### F1 — MEDIUM: pre-round-34 rows are silently scored, and the refusal contract is factually wrong

`quality/ratio-domain-meta.py:52-53` promises exit 3 for "the pre-round-34 split shape, which the rule
does not score", and `:112-115` states rounds 12-33 write `| C1 | calibration / ... |`, a shape "refused
loudly instead of being silently scored meta". At `e467892` only round 12 has that empty-first-cell shape
(`SCORECARD.md:296`); rounds 13-33 write a third shape — bare axis and claim sharing the first cell, no
bold (`SCORECARD.md:770`: `C1 coverage, documented custom-module observation route`). `split_row` refuses
only when the post-id remainder is empty (`:121 if not rest:`), so every 13-33 row is parsed and scored:

- `--from 16 --to 16` → exit 0, three rows classified, two fail-closed meta.
- `--from 13 --to 33` → exit 0, 53 rows, `domain=6 meta=47 default=31` (`legacy-13-33.txt`): six legacy
  rows land domain under clauses never validated on their shape (24 C1, 25 C1, 26 C1, 26 C2, 27 C1 via
  clause 3; 32 C1 via clause 5).
- Any window touching round 12 exits 3 with the whole count lost (`abort-12-44.txt`), so the same tool
  refuses 12-33 but scores 13-33 — refusal depends on whether one round is included.

Reproduction: `python3 -I quality/ratio-domain-meta.py --repo . --rev e46789213830597348fe96a351ae004d10587385 --from 13 --to 33 --why`.
w1's scope receipt tested only 12-33 (`out-of-scope-12-33.txt`), which aborts and masked this hole.
Rounds 34-44, the criterion's registered surface, are unaffected.

Content-error correction (exact replacement, locator `quality/ratio-domain-meta.py:112-115`, worktree
bytes = data-commit bytes): replace
"`Rounds 12-33 write `| C1 | calibration / ... | ... |`, where the axis and claim sit in a second cell;
that shape is outside the rule's validation and is refused loudly instead of being silently scored meta.`"
with: "`Round 12 writes `| C1 | calibration / ... | ... |` (axis and claim in a second cell); that
empty-first-cell shape is refused with exit 3. Rounds 13-33 write `| C1 coverage, <claim> | ... |` (bare
axis and claim sharing the first cell): this tool parses and scores that shape with the same clauses,
although the rule was validated only on the round-34+ merged shape; start windows at 34 to exclude legacy
rows.`" and at `:52-53` replace "3 a claim row in the pre-round-34 split shape, which the rule does not
score." with "3 a claim row whose first cell holds only the claim id (round 12's split shape)." The L1
decides whether to land the doc fix or tighten the code.

### F2 — LOW-MED, latent: the axis token is the first `**bold**` anywhere, not the first token

Docstring: "Its axis is the token after the claim id" — the first token. Code takes the first
`AXIS_BOLD_RE` match anywhere in the post-id text (`:128`), else a bare leading word (`:63-64`).

- Bold axis containing a character outside `[A-Za-z0-9 /_-]` (`**coverage (sourced)**`) matches no bold,
  and the bare regex cannot match a leading `*`, so axis becomes empty and a clause-5 coverage row falls
  to clause-7 meta. Synthetic: `synth-50.txt` row C1 (`admitted=1/1`, entry word present) printed
  `50 | C1 | - | meta | C7`.
- A later bold token hijacks a bare axis: `| C2 coverage - verdict **TARGET_MET**, admits the entry |`
  printed axis `target_met`, clause 7 meta (`synth-50.txt` row C2), where the rule's clause 5 says domain.

No real row in 34-44 is affected (18 clean bold axes, 2 bare; `rows-parsed.json`), so this is latent, but
both cases misclassify a natural markdown form the rule's prose covers.

### F3 — LOW-MED, latent: escaped pipe truncates the claim cell

`split_row` splits on every `|` (`:117`), so a markdown-escaped `\|` cuts the first cell; anything after
it is invisible to clauses 3-6. Synthetic (`synth-50.txt` row C3): a claim cell naming
`tools/mado-geometry.py` after a `\|` printed meta C7 instead of domain C3. Real instance with no effect:
`SCORECARD.md:2257` (round-36 C1) contains one `\|` and still classifies meta — via clause 1, which fires
before the path clauses.

### F4 — LOW: rounds with no claim sections are indistinguishable from an empty window

Rounds 38 and 42 have no `## Round` claim sections at `e467892` (38: `### Planned (round 38; intent
only)` + `### Capabilities (round 38)` at `SCORECARD.md:2402,2412` and an axis-table row at `:200`; 42:
claims re-registered into round 43, `SCORECARD.md:2531`), so `--from 38 --to 38` prints
`domain=0 meta=0` exit 0. The `window=` field echoes the inputs, never which rounds contributed; a
consumer cannot tell "no claims by design" from a typo'd window. Also, a row before the first `## Round`
heading is dropped and a row under a trailing non-Round heading inherits the last round number
(`synth-60.txt`); neither occurs in the real file (0 `| C` rows before `SCORECARD.md:231`; none after the
round-44 section). Note only — criterion 82 does not require round-coverage reporting.

### F5 — LOW, registration integrity: "a rule frozen in the tool's docstring before its first run" has no tree-order witness

Criterion 82 (`corpus/QUALITY.md:411`) asserts the rule was "frozen in the tool's docstring before its
first run". The tool's entire history is the data commit itself (`git log e467892 --
quality/ratio-domain-meta.py` → single entry `e4678921`), and w1's evidence landed after data
(`290cddea`), so commit order cannot witness the freeze — unlike C1/C2, whose registration-v2 freeze
`03fa5c6` predates the data commit. Mitigations that do reproduce today: w1's `ratio.py` is
byte-identical (same sha256 `131c5c84…`), and the lesson's command against the pre-data rev `03fa5c6`
reproduces the published number exactly, on a SCORECARD whose 34-43 sections the data commit did not
touch (freeze..data diff appends only the Round-44 section). Residual: the freeze claim stays
process-verifiable only, same class as the registration's declared residuals; reporting so the L1 can
rule it covered or add a witness.

## Criterion-82 cross-check (all reproduce)

- Published number: `SCORECARD.md:2583` `DOMAIN_META: domain=12 meta=5 window=34-43 default=1` = my run
  at `e467892` = lesson `corpus/lessons/round-44.md:255` at freeze `03fa5c6`.
- Verbatim carriage + one hand-labelled disagreement with disposition: `corpus/lessons/round-44.md:257-259`.
- "Shown able to fail" mutants: axis-token mutant `domain=13` against 12 on 34-43; draft-1 classes 40 C1
  meta — both exactly as recorded in criterion 82.
- "rounds 34, 35 and 39 are mixed": hand-checked exact — every other round in 34-43 is single-class
  (36 all-meta; 37, 40, 41, 43 all-domain); round 44 (outside the published window) is all-domain.
- Round-level-tally caveat in criterion 82 matches the considerthese proposal's grain
  (`considerthese/2026-10-25.md:46`); the row-grain implementation is what criterion 82 registers.
- Numbering note: w1 draft checks `check82.py`/`check84.py` (state-field audit / MADO_AXIS receipts) do
  not correspond to landed criteria 82 (this tool) and 84 (FORGED-PIN); landed criterion 82's check is
  the tool invocation itself, so nothing independent pins it.

## Robustness probes (all at `e467892` unless stated)

| Probe | Result |
|---|---|
| empty window 100-200 | exit 0, `domain=0 meta=0 default=0` (documented) |
| bad rev | exit 2, clear stderr (documented) |
| `--from 44 --to 34` | exit 2 (documented) |
| `python3` vs `python3 -I` | byte-identical output |
| `|C5 **coverage**|admitted=1/1|…` (no padding) | parsed, domain C5 |
| lowercase `| c6` | silently skipped (rule-conformant: rule says `C<digit>`) |
| duplicate ids (round 12 has two C2 rows) | both counted (row-grain, by design) |
| clause-2 tokens in the evidence cell (40 C1) | fires on the whole row — rule-conformant ("the row carries") |
| clause-5 `admitted=` in the evidence cell (37 C1) | fires on the whole row — rule-conformant |

## Residual risk and verification gaps

- I did not fuzz beyond the cases above (no CRLF/UTF-8/NUL probes; `splitlines` + `decode(replace)`
  read suggests they are safe, unverified).
- Pre-34 windows were spot-checked (12, 13-33, 16), not enumerated round by round.
- I did not re-derive w1's own run receipts beyond the mutants and the two 34-43 reproductions; w1
  receipt provenance (timestamps) was not audited.
- Tooling: none installed (python3 + system git only). Scratch dir created under
  `/fast/scratch/hyaku/mado-r44/RevRatioTool/` and removed; all cited receipts live in this seat dir.

## Quote verification (script: `verify-quotes.py`, receipt: `quotes-check.txt`)

```
QUOTE src=quality/ratio-domain-meta.py:52 :: `domain=0 meta=0`), 2 bad arguments or unreadable revision, 3 a claim row in
QUOTE src=quality/ratio-domain-meta.py:53 :: the pre-round-34 split shape, which the rule does not score.
QUOTE src=quality/ratio-domain-meta.py:112 :: claim id, axis word and claim text share the first cell.  Rounds 12-33
QUOTE src=quality/ratio-domain-meta.py:113 :: write `| C1 | calibration / ... | ... |`, where the axis and claim sit in a
QUOTE src=quality/ratio-domain-meta.py:114 :: second cell; that shape is outside the rule's validation and is refused
QUOTE src=quality/ratio-domain-meta.py:115 :: loudly instead of being silently scored meta.
QUOTE src=quality/ratio-domain-meta.py:117 ::     cells = line.strip().strip("|").split("|")
QUOTE src=quality/ratio-domain-meta.py:121 ::     if not rest:
QUOTE src=quality/ratio-domain-meta.py:128 ::     bold = AXIS_BOLD_RE.search(rest)
QUOTE src=SCORECARD.md:2583 :: DOMAIN_META: domain=12 meta=5 window=34-43 default=1
QUOTE src=SCORECARD.md:770 :: C1 coverage, documented custom-module observation route
QUOTE src=SCORECARD.md:2257 :: C1 **calibration** — the two round-35 admission counters are repaired
QUOTE src=corpus/lessons/round-44.md:255 :: DOMAIN_META: domain=12 meta=5 window=34-43 default=1
QUOTE src=corpus/lessons/round-44.md:257 :: Hand-labelled disagreement: round-36 C2 (operability) is classed meta by the rule
QUOTE src=corpus-QUALITY-at-datacommit.md:411 :: under a rule frozen in the tool's docstring before its first run
QUOTE src=corpus-QUALITY-at-datacommit.md:411 :: one hand-labelled row where the reader's reading disagrees with the rule
QUOTE src=corpus-QUALITY-at-datacommit.md:411 :: rounds 34, 35 and 39 are mixed
QUOTE src=.ufo/waves/round-44/w1/ExecDomainMetaRatio/receipts/tool-sha256.txt:1 :: 131c5c84993e4838d56ccfa5613e6a4d11592206149abb120fc76a352d46cfb0
```
