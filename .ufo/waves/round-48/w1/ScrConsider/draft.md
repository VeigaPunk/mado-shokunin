# Draft — landing `considerthese/2026-10-26.md` proposal 6 (2026-10-26)

Seat `ScrConsider`, round 48 `w1`, lane `mado-shokunin`. Base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`.
Chosen proposal: **proposal 6, "Lead with round-level outcomes, not counter internals"** (`considerthese/2026-10-26.md:52`,
dateline 2026-10-26). Landing form: **a QUALITY criterion** (provisional number 96; the L1 freezes the final number, the
final file path and the frozen token list). A lesson-paragraph fallback is in §9, for the case the L1 declines a criterion.

Everything below is a draft. No tracked file was edited by this seat; the criterion text, the checker and the receipts all
live in this seat directory.

---

## 1. The proposal, as written

`considerthese/2026-10-26.md:52` (2026-10-26):

> "Lead with round-level outcomes, not counter internals."

and, on the same line:

> "the useful signal for João is what his desktop tooling can now do"

Both quotes are verified against the base blob by `.ufo/waves/round-48/w1/ScrConsider/verify-quotes.py`
(receipt `receipts/quotes.txt`: `claimed=52 found=52 words=7` and `words=13`, `QUOTE_SUMMARY: quotes=7 pass=7 fail=0`).

The proposal's subject is a *receiver*: João reads the day's output at 75 commits a day and needs the capability change,
not the counter mechanics. Its author states the rule for its own file ("I should keep counter mechanics to one
paragraph"), but the same defect sits in the artifact the lane writes for João — the round's closure section.

## 2. Why this one, and not the others

Disposition at base, each by the lane's own bytes (all greps reproduced in `receipts/unimplemented-base.txt`):

| Proposal | State at base `579f694b` | Evidence |
|---|---|---|
| 1 privacy check on new receipts | **implemented** | `corpus/lessons/round-45.md:81` — proposal 1 → `quality/check-session-material.py` + QUALITY 85 |
| 2 running ledger of live-state tools | **refused round 47** (as the assignment states) | `corpus/lessons/round-47.md:227` — drafted, attacked, refused with a flip condition |
| 3 track routed defects until they close | **implemented** | `corpus/QUALITY.md:454-459` — criterion 90, citing proposal 3 |
| 4 re-run one tool myself, read-only | **not landable now** — see below | `considerthese/2026-10-26.md:50`; `corpus/QUALITY.md:399` |
| 5 domain-to-meta ratio as a number | **implemented** | `corpus/lessons/round-44.md:248` — proposal 1 of 2026-10-25 → `quality/ratio-domain-meta.py` + criterion 82 |
| 6 lead with round-level outcomes | **unimplemented** | §3 |

Proposal 4 was opened and set aside on its own text: "All live runs I report are relayed from closures" and "they need
João's host, so this would need his OK and a machine connection" (`considerthese/2026-10-26.md:50`). Its lane-side half —
a relayed number must be marked `relayed:` rather than trusted — is already carried by QUALITY 76
(`corpus/QUALITY.md:399`: "the reflection is a pointer, not evidence"), and its remaining half is an operator decision with
no lane-side bytes to bind, so it cannot become a check that fails on a committed revision. Proposal 6 has no lane-side
coverage at all and does.

## 3. Evidence that proposal 6 is unimplemented at base

From `receipts/unimplemented-base.txt`, all run at `579f694b`:

- **No criterion.** `git show BASE:corpus/QUALITY.md | grep -cE '^[0-9]+\. '` → `95` criteria, and the `considerthese/`
  citations inside them sit at `:367` (criterion 60), `:399` (76), `:409` (81), `:411` (82) and `:459` (inside criterion
  90) — none of them proposal 6.
- **No rule anywhere else.** `git grep -niE "proposal 6|outcome-first|round-level outcome" BASE -- . ':!considerthese/'`
  → `rc=1` (no match outside the reflection file itself; the only hit in the whole tree is the reflection line that
  states the proposal).
- **Governance files counted.** `outcome-first|round-level outcome|leads with the outcome` in `corpus/QUALITY.md`,
  `SKILL.md`, `AGENTS.md`, `PROVINCE.md` at base → `0`, `0`, `0`, `0`.
- **No gate.** `git ls-tree -r --name-only BASE quality/ | grep -ciE 'outcome'` → `0`.
- **Nothing refused it either.** `git grep -n 'proposal 6' BASE -- corpus/` → `rc=1`: no lesson has disposed of it, so
  it is open, not declined.

## 4. What it points at in the lane's bytes

The lane's own closure section is the artifact João reads, and it opens with process, not capability. Round 47's section
starts like this (`SCORECARD.md:2656` at base):

> "Claims declared at `c24adef2` (`.ufo/waves/round-47/claims.md`) before wave `w1` (41 build seats)"

— a freeze hash, a seat count and a wave name before any statement of what SUPER+RETURN can now do. Rounds 44-46 open the
same way (`registration … frozen at`, with 9, 10 and 14 process tokens in the opening sentence).

Census with the draft checker at base (`receipts/check96.txt`, `--rounds 1-47`): **`rounds=47 pass=0 fail=34 skip=13`** —
all 34 round sections that exist in `SCORECARD.md` at base fail, the 13 skipped rounds never landed a section. The defect
is therefore not a one-round slip; it is how the lane has written every closure since round 12.

## 5. The landing — proposed QUALITY criterion 96

Transposition, labelled: the proposal is addressed to the reflection's author, and the reflection file is
operator-authored and not the lane's to edit (`corpus/lessons/round-32.md:120`: "operator-authored, read-only — not
edited"). **[INFERENCE]** The lane can bind the same principle where it *does* write and where João looks first — its own
`SCORECARD.md` round section — which is why the criterion below governs the closure's leading sentence rather than the
reflection's prose. It is the same receiver and the same complaint, moved to bytes the lane controls.

Proposed text (house form; paste-ready, provisionally 96):

> 96. A round's closure section in `SCORECARD.md` leads with the round-level outcome before its own bookkeeping: the
> section's first sentence names the desktop surface the round moved — `tools/mado-<name>.py`, `tools/mado-<name>.sh`,
> `corpus/knowledge/<name>.md`, `SKILL.md` or `PROVINCE.md` (the criterion-60 definition of domain-facing), and that path
> exists in the revision being scored — and carries no process token: `registration`, `frozen`/`freeze`, `Claims
> declared`, `PRED-`, `TARGET_MET`/`TARGET_MISSED`, `fixtures=`, `seat`/`seats`, `wave`, `attempt=`, `receipts/`,
> `counter`. The freeze hash, seat counts, counter ids and receipts follow in the same section, unfettered. A round that
> never landed a section is out of scope. Check: `python3 -I quality/check-round-outcome-first.py --repo . --rev
> <closure tip> --rounds <a>-<b>` prints one `OUTCOME_FIRST: round=<N> verdict=PASS|FAIL|SKIP line=<n> surface=<path|none>
> process_tokens=<k> reasons=<no-surface|surface-absent|process-first|no-paragraph>` line per round and the summary
> `OUTCOME_FIRST_SUMMARY: rounds=<n> pass=<p> fail=<f> skip=<s>`; a `fail=0` is the requirement. Shown able to fail: at
> base `579f694b` the same tool prints `OUTCOME_FIRST_SUMMARY: rounds=47 pass=0 fail=34 skip=13`, and round 47's opening
> is the freeze-hash sentence quoted above; it passes once the opening paragraph leads with the capability (positive
> control in §6). (proposal: `considerthese/2026-10-26.md` proposal 6, 2026-10-26 — "Lead with round-level outcomes, not
> counter internals"; lesson: `lessons/round-48.md`, to be written by the round's lesson seat.)

Why this form and not a new axis or a new counter: it sits beside criteria 60 and 82, which already govern *what* a round
report counts (its ratio, and that ratio as a re-runnable number), and it adds only *what the section says first*. It
creates no new instrument, no scoring path and no axis movement; it constrains prose the lane already writes.

## 6. The check, and the proof that it can fail

Prototype: `.ufo/waves/round-48/w1/ScrConsider/check96.py` (Python 3 stdlib only, no network, no process beyond the two
`git` read verbs `show`/`cat-file -e`, reads `SCORECARD.md` from the object database via `git show <rev>:SCORECARD.md`;
its scoring path writes nothing — only `--selftest` writes, into a `tempfile` directory under `$TMPDIR`, which it removes).
Rule frozen in its docstring before the first run. The L1 would move it to `quality/check-round-outcome-first.py` (the
criterion names the landed path); a byte-identical scratch copy under that name produces the same verdicts
(`receipts/check96.txt` §9).

Receipt `receipts/check96.txt` (tool sha256 `21d6be5c7afae9231d6de8ec2db25deed0e32ade8263ebb4a71a63e56254c488`):

- **Selftest, 5 cases, `SELFTEST: ok cases=5`** — positive control that leads with the outcome (`PASS`), process-first
  negative (`FAIL`, `process-first`), surface-only-in-second-sentence negative (`FAIL`, `no-surface`), no-prose negative
  (`FAIL`, `no-paragraph`), and a sentence naming `tools/mado-ghost.py`, absent from the tree (`FAIL`, `surface-absent`).
  Fixture git repo built under `$TMPDIR=/fast/scratch/hyaku/mado-r48/ScrConsider`, toplevel asserted equal to the fixture
  dir before its single commit.
- **Red at base**, 4 most recent rounds: `round=44/45/46/47 verdict=FAIL surface=none process_tokens=9/10/14/11
  reasons=no-surface,process-first`, `fail=4`, `rc=1`.
- **Red at base**, whole history: `rounds=47 pass=0 fail=34 skip=13`, `rc=1`.
- **Green control on real bytes**: a scratch `--shared` clone of the lane at base, one edit to `SCORECARD.md` (round 47's
  opening paragraph replaced with an outcome-first sentence naming `tools/mado-terminal.py`), committed in the clone only
  (`f73436ed5408f3745d86cecc29d989fbb6f50afc`), prints `round=47 verdict=PASS surface=tools/mado-terminal.py
  process_tokens=0 reasons=none` while 44-46 stay `FAIL`. The check is satisfiable by editing the lane's own prose; the
  lane repo was not modified.

Self-application: landed as written, criterion 96 scores round 48's own closure section at its data commit — the round
that lands it must satisfy it (`fail=0`), which is the cheapest falsification the L1 has.

## 7. What the L1 must decide at freeze

1. **Number and path.** Provisional `96` and `quality/check-round-outcome-first.py`; other w1 seats may add criteria 96+
   before the freeze, and the file name must match the criterion text (the round-39 defect the reflection records at
   `considerthese/2026-10-26.md:30` — a registration naming a counter file absent from the freeze commit — is now guarded
   by QUALITY 64, `corpus/QUALITY.md:375`: every counter or checker path a registration names must exist at the freeze
   commit).
2. **Frozen token list.** §5's list is the draft's; adding a token later is a re-registration under the round's own rules.
3. **`SKIP` policy.** A round with no `SCORECARD.md` section is `SKIP`, not `FAIL` (rounds 38 and 42 at base). If the L1
   prefers strictness, the criterion must say so and the two skips become violations.
4. **Scope of the sentence test.** Draft: the first sentence of the first paragraph only. Widening it to the whole
   paragraph would fail round 47 twice over and changes what the criterion demands.

## 8. Known limits (declared, not hidden)

- **Ordering only, not content.** A round with a content-free but capability-shaped opening sentence passes; the check
  does not test whether the named surface actually changed. Criterion 83 (citation resolves at the revision) and the
  round's own claim counters carry content. The leading sentence is a reading-order requirement, nothing more.
- **The proposal's second half is not scored.** "Keep counter mechanics to one paragraph" is not measured: paragraph
  counting is fragile and the lane's closure sections legitimately carry several process paragraphs. Only the opening
  order is bound.
- **Heading shape.** The checker finds a section by `^## Round <N>`; a renamed heading turns a round into `SKIP` silently —
  the summary's `skip=` counts it, which is why the criterion requires `fail=0` *and* a skip count a reader can compare
  with the rounds that landed.
- **First-sentence cut is textual.** A period followed by whitespace ends the sentence; a path or version period does not.
  A sentence ending at a period followed by a newline (as in a wrapped paragraph) is joined before cutting; other markdown
  shapes (a list item, an em dash) are treated as ordinary text.
- **Not yet a gate.** `check96.py` is a seat draft. It has not been registered under `PROVINCE.md`, has no clean-state
  receipt at a landed revision, and by criterion 93 could not be one before it lands.

## 9. Alternative form, if the L1 declines a criterion — a lesson paragraph

> **M48-x — the closure's first sentence is the only part João reliably reads.** Class: receiver-signal. Evidence:
> `considerthese/2026-10-26.md:52` proposal 6 (2026-10-26) asks for round-level outcomes before counter internals; at
> base `579f694b` all 34 `SCORECARD.md` round sections open with registration/freeze bookkeeping
> (`receipts/check96.txt`, `pass=0 fail=34 skip=13`), round 47 included (`SCORECARD.md:2656`, claims/wave/seat counts
> first). Fix: criterion 96 (§5), or this line; the flip is the same `pass=34` census. Captured-by: none before this
> round; the proposal is the reflection's, the receiving artifact is the lane's.

## 10. Provenance

- Base: `579f694b45c797a9c39761fdb4f9e0a1b71b3585`; every count re-derived at that revision, no number relayed from the
  reflection or from a spot-check.
- Receipts in `receipts/`: `unimplemented-base.txt` (greps and the 1-47 census), `check96.txt` (selftest, red, green),
  `quotes.txt` (locators computed from the base blob).
- Scratch: `/fast/scratch/hyaku/mado-r48/ScrConsider` (fixture repo, `--shared` clone); deleted before the seat closed.
  No `/tmp` path is cited.
- Tooling: no install, no upgrade, no package transaction. `git` read verbs only in the lane; the only commit made this
  seat is inside the scratch clone, after asserting its toplevel.
