# Proposal — a re-runnable domain-versus-meta count (QUALITY criterion 82 draft)

Source: `considerthese/2026-10-25.md:46` proposal 1 — "Track the domain-versus-meta
ratio as a running number. This window went 4 domain rounds to 2 calibration
rounds, against 1 to 4 in yesterday's window." (17 words, locator from
`grep -n 'domain-versus-meta ratio' considerthese/2026-10-25.md`, receipt
`receipts/quote-locators.txt`).

The reflection asks for the *number*; it reports the *prose*. This seat turns the
prose into a command: `ratio.py` (same directory) reads `SCORECARD.md` at a
revision, classifies every `^| C<digit>` claim row of a round window under a rule
stated in its docstring before the first run, and prints
`DOMAIN_META: domain=<d> meta=<m> window=<a>-<b> default=<n>`.

## Why the unit is the claim row, not the round

The reflection counts rounds ("4 domain rounds to 2 calibration rounds"). The
committed record does not support a round-level label for the window it would
next be applied to:

| Round | claim rows | classes under the rule |
|---|---|---|
| 34 | 2 | domain, meta (mixed) |
| 35 | 2 | domain, meta (mixed) |
| 36 | 2 | meta, meta |
| 37 | 2 | domain, domain |
| 38 | 0 | — no `## Round 38` heading in SCORECARD.md |
| 39 | 3 | meta, domain, domain (mixed) |
| 40 | 2 | domain, domain |
| 41 | 2 | domain, domain |
| 42 | 0 | — no `## Round 42` heading in SCORECARD.md |
| 43 | 2 | domain, domain |

Three of the eight rounds that carry rows spend one row on the lane's own
instruments (34, 35, 39), so no single word describes them; and two rounds carry
no claim row at all, so a round-based tally silently shrinks its denominator. The
row count is the finer, reproducible unit, and it is already written down in a
form a command can read: `.ufo/waves/round-38/` and `.ufo/waves/round-42/` exist,
yet neither round has a SCORECARD heading or a claim row, which a round-level
ratio cannot represent.

Measured windows (freeze `e2289516a9a857f55cda7be635933e89b931c3da`,
`ratio.py` sha256 `131c5c84993e4838d56ccfa5613e6a4d11592206149abb120fc76a352d46cfb0`):

```
34-43: DOMAIN_META: domain=12 meta=5 window=34-43 default=1
39-43: DOMAIN_META: domain=8  meta=1 window=39-43 default=0
```

## Criterion draft (next free number)

Numbering check: `corpus/QUALITY.md` holds 81 numbered criteria, the last at
`corpus/QUALITY.md:409` (`grep -n '^81\. '`), and `grep -c '^82\. '` prints `0`
(receipt `receipts/quote-locators.txt`).  So the next free number is **82**.

The criterion belongs to the round that **adopts** it, not to round 44:
`corpus/lessons/round-44.md` does not exist at `HEAD`
(`git cat-file -e HEAD:corpus/lessons/round-44.md` exits `128`), and a lesson
written at a closure cannot carry a criterion registered after it.  The draft
below therefore names the path that lesson will occupy, `corpus/lessons/round-<n>.md`,
and is checkable from round 45 on.

> **82.** A round's balance between desktop ground and the lane's own
> self-measurement is a re-runnable count, not prose:
> `python3 -I .ufo/waves/round-44/w1/ExecDomainMetaRatio/ratio.py --repo . --rev
> <closure tip> --from <first round> --to <last round>` classifies every
> `| C<digit>` claim row of those SCORECARD round sections under a rule frozen
> before the run — a claim whose deliverable is a desktop-facing artifact (a
> `tools/` tool, a `corpus/knowledge/` entry, a `SKILL.md` table) is **domain**;
> calibration, counters, manifests, ledgers, admission gates and record repairs
> are **meta**, and a row no clause matches is meta by fail-closed default
> (reported as `default=`) — prints one `round | claim | axis | class` line per
> row and `DOMAIN_META: domain=<d> meta=<m> window=<a>-<b> default=<n>`, and the
> round's lesson (`corpus/lessons/round-<n>.md`) carries that line verbatim
> beside the reflection sentence it answers, plus one hand-labelled row where the
> reader's own reading disagrees with the rule and the disposition (the rule was
> changed, or it was retained and why). A round-level tally — "4 domain rounds
> to 2 calibration rounds", `considerthese/2026-10-25.md:46` — is not the count:
> rounds 34, 35 and 39 are mixed under the rule, and rounds 38 and 42 carry no
> claim row at all, so a per-round label cannot express the window. Check: run
> the command at the closure tip and at the window base — a window whose rows
> did not change must print identical counts; an empty window must print
> `domain=0 meta=0` exit 0, not crash; a calibration row that names a tool must
> class meta (clause 1 outranks the named tool); and the axis-word mutant
> (`ratio-mutant-axis-token.py`, which classes `coverage`/`operability` rows
> domain) must print a different `domain=` on the same window (`13` against the
> rule's `12`, the one differing row being round-36 C2, whose object is the
> lane's own records) — a count the rule cannot move measures the labels, not
> the lane. Shown able to fail: draft 1 of the rule, kept as
> `ratio-draft1-no-clause2.py`, scored round-40 C1 `meta` although that row's
> deliverable is `mado-options.py` behind `fixtures=0/19`, printing
> `domain=11 meta=6 default=2`; the fixtures clause was added and the row now
> classes domain.

## Re-running it (the command a closure runs)

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I .ufo/waves/round-44/w1/ExecDomainMetaRatio/ratio.py \
  --repo . --rev <closure tip> --from <first round> --to <last round>
```

Read-only: one `git -C <repo> show <rev>:SCORECARD.md`, no writes, no network,
stdlib only.  Exit codes: `0` counted (an empty window prints
`domain=0 meta=0`), `2` bad arguments or unreadable revision, `3` a claim row in
the pre-round-34 split shape — the rule is stated and validated for the merged
shape used from round 34 on, and refuses the old shape loudly instead of scoring
it meta (`receipts/out-of-scope-12-33.txt`, exit 3).

## Deployment note for the L1

The tool sits in this seat directory because that is the only path a wave seat
may write.  If the L1 adopts criterion 82, promote the file to
`quality/ratio-domain-meta.py`, add the frozen rule as the criterion's own text,
and re-point the criterion's check at the promoted path; the wave path is cited
here because criterion 78 already cites
`.ufo/waves/round-43/w1/ScrQualityCriteria/check78.py` and wave directories are
committed.  Two mutants travel with the tool on purpose: they are the
discrimination evidence, not spares.

## What the number does not measure

- Only `^| C<digit>` rows under a `## Round` heading.  The early axis-score
  table (`SCORECARD.md:16-26`), `LOG.md`, SHONEN boxes, lessons and wave
  manifests are outside the denominator, so the count is of *claims*, not of
  rounds of work.
- The rule is lexical over the row's own bytes.  A calibration row that is, in
  content, a desktop fact (round-34 C2, the queue-cap line number) counts meta;
  that disagreement is recorded in the seat report, not hidden.
- No claim about whether either class is *good*.  A high domain share in rounds
  39-43 is a fact about attention, not evidence that the entries are true.
