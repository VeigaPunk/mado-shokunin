# w1/ExecDomainMetaRatio — the domain-versus-meta ratio as a re-runnable count

Seat: ExecDomainMetaRatio (leaf, round 44 w1). Status: **complete**.
Target: `considerthese/2026-10-25.md:46` proposal 1. Nothing frozen was edited; no
`git`/`jj` mutation, no package transaction, no host-service read beyond none, no
subagent (no labrat was needed).

## Files written (all inside the seat directory)

| Path | What |
|---|---|
| `.ufo/waves/round-44/w1/ExecDomainMetaRatio/ratio.py` | stdlib, read-only classifier; `--repo --rev --from --to`, `--why`, `--rule`. sha256 `131c5c84993e4838d56ccfa5613e6a4d11592206149abb120fc76a352d46cfb0` |
| `…/ratio-mutant-axis-token.py` | teeth: the naive axis-word rule (`coverage`/`operability` → domain). NOT the rule |
| `…/ratio-draft1-no-clause2.py` | teeth: draft 1 of the rule, before the fixtures clause existed |
| `…/proposal.md` | QUALITY criterion **82** draft + re-run command + limits |
| `…/receipts/*.txt` | 12 receipts, each `$ <cmd>` / output / `exit=<n>` |
| `.ufo/waves/round-44/w1/ExecDomainMetaRatio.md` | this report |

## The rule (frozen in `ratio.py`'s docstring before the first run; `--rule` prints it)

A **claim row** is a `| C<digit>` line under a `## Round <N>` heading. First
matching clause over the row's own bytes at `--rev`:

1. axis `calibration` → **meta**
2. axis `operability` AND (`fixtures=` | `tool=absent|present`) → **domain** (a tool)
3. claim cell names `tools/<name>.py|.sh` → **domain** (a tool)
4. claim cell names `corpus/knowledge/<name>.md` → **domain** (an entry)
5. axis `coverage` AND (`admitted=` | `entry`/`entries` in the claim) → **domain** (an entry)
6. claim cell names `SKILL.md` → **domain** (a table)
7. otherwise → **meta**, fail-closed, reported as `default=` so it is visible

Rationale stated before classifying: the *immediate object* decides, not the axis
word — a tool or entry held against the desktop outlives the lane; counters,
manifests, ledgers, admission gates and record repairs do not. Clause 1 outranks
a named tool because a calibration row's deliverable is the record.

## Runs (freeze `e2289516a9a857f55cda7be635933e89b931c3da`; identical at `HEAD` `ae996fcf5e50d2d882dcf543a4ab2df5604dada2`)

```
$ python3 -I .ufo/waves/round-44/w1/ExecDomainMetaRatio/ratio.py --repo . --rev e2289516a9a857f55cda7be635933e89b931c3da --from 34 --to 43
34 | C1 | coverage | domain
34 | C2 | calibration | meta
35 | C1 | coverage | domain
35 | C2 | calibration | meta
36 | C1 | calibration | meta
36 | C2 | operability | meta
37 | C1 | coverage | domain
37 | C2 | operability | domain
39 | C1 | calibration | meta
39 | C2 | operability | domain
39 | C3 | coverage | domain
40 | C1 | operability | domain
40 | C2 | coverage | domain
41 | C1 | operability | domain
41 | C2 | coverage | domain
43 | C1 | operability | domain
43 | C2 | coverage | domain
DOMAIN_META: domain=12 meta=5 window=34-43 default=1
exit=0
```

```
$ python3 -I .ufo/waves/round-44/w1/ExecDomainMetaRatio/ratio.py --repo . --rev e2289516a9a857f55cda7be635933e89b931c3da --from 39 --to 43
39 | C1 | calibration | meta
39 | C2 | operability | domain
39 | C3 | coverage | domain
40 | C1 | operability | domain
40 | C2 | coverage | domain
41 | C1 | operability | domain
41 | C2 | coverage | domain
43 | C1 | operability | domain
43 | C2 | coverage | domain
DOMAIN_META: domain=8 meta=1 window=39-43 default=0
exit=0
```

Denominator check: `grep -n '^| C[0-9]' SCORECARD.md | awk -F: '$1>=2122' | wc -l`
prints `17` — the 17 rows above (receipt `receipts/quote-locators.txt`).

Per-round shape (why the unit is the row, not the round): rounds 34, 35 and 39
are **mixed**; 36 is pure meta; 37, 40, 41, 43 are pure domain; **38 and 42 carry
no claim row at all** — `.ufo/waves/round-38/` and `.ufo/waves/round-42/` exist but
`SCORECARD.md` has no `## Round 38` and no `## Round 42` heading, so a round-level
tally silently shrinks its denominator and cannot express a mixed round. This is
the concrete reason the reflection's prose form ("4 domain rounds to 2 calibration
rounds") is not re-runnable as-is.

## The classifier can fail — three receipts

**(a) Changed (a real miss, fixed).** Draft 1 of the rule had no fixtures clause
and scored **round-40 C1 `meta`** — a row whose deliverable is `mado-options.py`
behind `fixtures=0/19`, but whose claim cell only says `--live`:

```
$ sed -n 2480p SCORECARD.md
| C1 **operability** (capability) `--live` | v2 `fixtures=0/19` exit 1 at base -> see report for the data-tip receipt | `python3 -I quality/counters/c1-r40-live-v2.py --repo . --rev <rev>` | reported in the fleet report; v1 and v2 both scored |
```

Draft 1 on 34-43: `DOMAIN_META: domain=11 meta=6 window=34-43 default=2`
(`receipts/draft1-no-clause2-34-43.txt`; `40 | C1 | operability | meta | C7:fail-closed`).
**What I changed:** added clause 2 — axis `operability` with `fixtures=` or
`tool=absent|present` in any cell is a tool claim. It is principled, not a
special case: every fixture/tool-presence measurement in the window is a tool
claim, and no meta row in the window carries those tokens (round-36 C2, the only
default row left, measures `scratch_disposition_ok` / `tip_axis_transcript`, not a
tool).

**(b) Retained (rule vs my own reading, not fixed).** **Round-34 C2**, hand
label **domain**, rule **meta** (`receipts/hand-labels.txt`):

```
| C2 calibration (lowest scored axis, tied) — the published S189 queue-cap line number must match a re-read of the pinned fetch | before: …
```

My reading: the claim's content is a fact about the desktop — which line of the
pinned Hyprland `EventManager.cpp` carries the queue-cap constant (published 169,
measured 169). The rule says meta because the axis word is `calibration` and the
row's deliverable is a publication record, not a tool or an entry.
**Why not changed:** admitting "a calibration row that happens to be about
desktop source" would move every calibration-of-a-fact row into domain and
dissolve the distinction the ratio exists to expose — the row checks the lane's
record against a pinned fetch, and the fetch is the lane's own artefact. The
disagreement is reported, and `proposal.md` names it as a known limit of the
lexical rule.

**(c) The number is not tautological.** The axis-word mutant, which classes a row
by its label, prints `DOMAIN_META: domain=13 meta=4 window=34-43 default=0` on the
same rev and window, differing from the rule's `12/5` in exactly one row —
`36 | C2 | operability | domain` vs `meta` (round-36 C2 measures the lane's own
records durability gate). Receipt: `receipts/mutant-axis-token-34-43.txt`; row
diff reproduced with `diff <(grep '^[0-9]' receipts/run-34-43.txt) <(grep '^[0-9]' receipts/mutant-axis-token-34-43.txt)`.

Also exercised: empty window `--from 44 --to 44` prints
`DOMAIN_META: domain=0 meta=0 window=44-44 default=0` exit 0
(`receipts/empty-window-44-44.txt`); the pre-round-34 split row shape is refused
loudly with exit 3 rather than scored meta (`receipts/out-of-scope-12-33.txt`,
`SCORECARD.md:296`).

## Proposal (`…/ExecDomainMetaRatio/proposal.md`)

QUALITY criterion **82** (next free: `corpus/QUALITY.md` holds 81, last at
`corpus/QUALITY.md:409`, `grep -c '^82\. '` prints `0`), citing
`considerthese/2026-10-25.md:46` proposal 1, with the re-run command, the
discrimination check (mutant must move the count; calibration-about-a-tool must
class meta; empty window must not crash) and the shown-able-to-fail draft-1 case.
`corpus/lessons/round-44.md` **does not exist** at `HEAD`
(`git cat-file -e HEAD:corpus/lessons/round-44.md` exits 128), so the draft names
`corpus/lessons/round-<n>.md` for the round that adopts it (45), not 44 — a lesson
written at a closure cannot carry a criterion registered after it.

## Retained evidence

`receipts/`: `rule.txt`, `run-34-43.txt`, `run-34-43-why.txt`, `run-39-43.txt`,
`mutant-axis-token-34-43.txt`, `draft1-no-clause2-34-43.txt`,
`empty-window-44-44.txt`, `out-of-scope-12-33.txt`, `head-vs-freeze.txt`,
`hand-labels.txt`, `quote-locators.txt`, `tool-sha256.txt`. Every pasted number
above is a line of one of those files; the two quoted sources are located by
`grep -n` inside `quote-locators.txt`, not typed.

## Risks, limits, blockers

- **Lexical rule.** Only `| C<digit>` rows under a `## Round` heading: the early
  axis-score table (`SCORECARD.md:16-26`), `LOG.md`, SHONEN boxes and wave
  manifests are outside the denominator. The count is of *claims*, not of rounds
  of work; a high domain share in 39-43 is attention, not truth.
- **Clause 7 is a residual.** One row (36 C2) falls through to the fail-closed
  default. Reported, not hidden; a future round could add a "records durability"
  clause, but doing so now would be a rule written after seeing the answer.
- **Deployment.** The tool lives in the seat directory because that is the only
  path a wave seat may write. If the L1 adopts criterion 82, promote it to
  `quality/ratio-domain-meta.py` and re-point the criterion; the wave path is
  cited here on criterion 78's precedent.
- **Not run** (per wave policy, the L1 owns the gate): no build, lint, formatter
  or test suite. The runs above are the deliverable's own measurements, not a
  verification pass.
- **Tooling:** no tool installed or updated. Scratch
  `/fast/scratch/hyaku/mado-r44/ExecDomainMetaRatio/` used only for `TMPDIR` and
  removed at the end; nothing citable lives there.
- **Blockers:** none.
