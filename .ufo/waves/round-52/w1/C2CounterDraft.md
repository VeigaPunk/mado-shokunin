# C2CounterDraft — draft C2 counter `PRED-C2-r52` (round 52 w1, mado)

status: complete. A runnable structural counter for the C2 claim, its selftest, its mutation
suite, and its measurement receipts are below. Everything written by this seat lives in
`.ufo/waves/round-52/w1/C2CounterDraft/` and this report; no tracked lane file was touched
(`git status --short` in the lane shows only `?? .ufo/waves/round-52/`, the wave's own
untracked directory, which was already there when I started). No install, no service, no
compositor or process read, no package query, no fetch — the round's source-only boundary was
respected end to end.

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Frozen base
`85d57a818c3707397e21c840b6498b105ba798aa` (also the lane tip: the lane has not moved since
round 51). Counter bytes: sha256 `55452a3d6eab7cca2b20095f8678fbe936c8c65f241a561611a675defd8379fb`,
965 lines, stdlib only.

## Deliverables

- `.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py` — the draft counter
- `.ufo/waves/round-52/w1/C2CounterDraft/make-fixture.py` — synthetic staged fixture (own grammar)
- `.ufo/waves/round-52/w1/C2CounterDraft/mutants.py` — 18-mutant discrimination suite
- `.ufo/waves/round-52/w1/C2CounterDraft/blockform-check.py` — block-form grammar + setup errors
- `.ufo/waves/round-52/w1/C2CounterDraft/make-draft-fixture.py` — stages the *real* C2EntryDraft
  draft into a scratch clone (`--fix` applies the two markdown corrections as a satisfiability
  control)
- `.ufo/waves/round-52/w1/C2CounterDraft/recycled-check.sh` — the round-51 body at the target path
- `.ufo/waves/round-52/w1/C2CounterDraft/run-receipts.sh` — regenerates every receipt below
- `.ufo/waves/round-52/w1/C2CounterDraft/receipts/r-base.txt`
- `.ufo/waves/round-52/w1/C2CounterDraft/receipts/r-tip.txt`
- `.ufo/waves/round-52/w1/C2CounterDraft/receipts/r-green.txt`
- `.ufo/waves/round-52/w1/C2CounterDraft/receipts/r-mutants.txt`
- `.ufo/waves/round-52/w1/C2CounterDraft/receipts/r-blockform.txt`
- `.ufo/waves/round-52/w1/C2CounterDraft/receipts/r-draft-as-is.txt`
- `.ufo/waves/round-52/w1/C2CounterDraft/receipts/r-draft-fixed.txt`
- `.ufo/waves/round-52/w1/C2CounterDraft/receipts/r-recycled.txt`
- `.ufo/waves/round-52/w1/C2CounterDraft/receipts/r-fixture-build.txt`

**Integration for the L1**: copy `c2-r52-proposition-entry.py` byte-identically to
`quality/counters/c2-r52-proposition-entry.py`. The module holds no path to its own location:
every path it reads is relative to `--repo` (`ENTRY`, `REGISTRY`, `README`, `FETCH_ROOT`) or a
git object of the frozen `BASE`, so the copy needs no edit. `ENTRY_DEFAULT` is set to
`corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md`, the path seat `C2EntryDraft` says it
will land; if the landed path differs, change that one constant (or pass `--entry`).

## What the counter checks

`python3 -I c2-r52-proposition-entry.py --repo <lane> --rev <rev> [--entry <path>]
[--fetch-root .ufo/waves/round-52] [--work <scratch>]`. One diagnostic line per clause, then:

```
C2_R52: entailment=not-checked (outside non-author review)
C2_R52: clauses=abcde clauses_met=<n> admitted=<0|1>/1 verdict=TARGET_MET|TARGET_MISSED rev=<sha>
```

- **(a)** the target entry exists at `<rev>` and an unfenced row of `corpus/README.md` indexes it.
- **(b)** the entry declares ≥4 propositions (table form or block form), each with a claim, a
  source row, a pin locator, a quote and a written support rationale; ids and claims distinct.
- **(c)** each proposition's `S###` row exists in the `corpus/SOURCES.md` registry at `<rev>`, is
  `mined`, carries this round's access date (`2026-10-27`), is **absent from the registry at the
  frozen base** (so it was opened this round, not reused), its `anchor` cell names the pin under
  the round's fetch path and a 40-hex revision, and its `used-by` cell names this entry.
- **(d)** each proposition's pin resolves to a file present at `<rev>` under the round's fetch
  root, and the quote (3–25 words) appears **verbatim, whitespace-collapsed, inside the pin's
  cited line span**. When the entry carries a pin manifest, the manifest must declare the pin
  and, if it names rows, the cited row must be among them. The clause reports the frozen
  comparison policy and the two counts a reader needs to see whether the verdict depends on it:
  `quotes_bound=18/18 quotes_raw=6/18 pins=4 policy=whitespace-collapsed`, plus
  `pins_prior_equal=N/M` — how many of the bound pins are byte-identical to a pin staged in an
  earlier round.
- **(e)** the mapping is complete: every registry row *this entry opened* is mapped by a
  proposition, every proposition's row is cited by the entry, every proposition id is drawn on
  outside the map, no two propositions share a quote or a claim, and the propositions stand on at
  least two distinct rows.

Exit codes: `0` only on 5/5; `1` on any missed clause; `2` on setup errors (bad `--repo`/`--rev`,
the base commit absent, the base already holding the target entry, the round-51 slug offered as
the target, unusable scratch, a `--work` inside the scored repository). Scratch is `--work`, else
a `mkdtemp` under `$TMPDIR`; nothing outside the scratch dir is written; the scratch dir receives
`c2-r52-probe.json`.

**What it does not check, and cannot.** It does not decide whether a quote entails the
proposition it is attached to — the final line says so on every run. Entailment and source
truth are an outside non-author reviewer's job (this round's `C2PinAudit`, `C2EntryQuality`,
`C2SourceCritic`, `C2Novelty` seats). It also does not score novelty, wording reuse, or held-fact
omission; those are attack seats' business. The claim's "cannot claim automated entailment" is
honoured by construction, not by assertion.

## The grammar it accepts (documented so an entry can be written against it)

A markdown table whose header names six roles, in any order; a trailing parenthetical is ignored
(`quote (<=25 words)` is the quote column), whitespace and case are ignored, and no header cell
may serve two roles. Roles: `id` (`id`/`prop`/`proposition id`, optional), `claim`
(`claim`/`proposition`/`statement`/`fact`), `row` (`row`/`source row`/`s-row`/`registry row`),
`pin` (`pin`/`pin path`/`locator`/`source pin`/`pin:anchor`), `quote` (`quote`/`quoted`/
`quoted text`), `support` — a rationale column (`why`, `why it supports`, `rationale`,
`justification`, `reason`) outranks a support-class column (`support`, `support class`), because
a one-word class label is not a written rationale. The block form (`P1` on its own line, then
`claim:`/`row:`/`pin:`/`quote:`/`support:` lines) is accepted too.

Pin cells: `<pin>:<first>[-<last>]`, optionally `@ <revision>`. A path binds by basename; a
shortened name (`legacy-DispatcherTranslator.cpp`) resolves to the staged file when exactly one
file under the fetch root ends with it; a bare `:123` continues the previous proposition's pin.
Quote cells: backticks/quotes stripped, compared whitespace-collapsed against the cited line
span. **A `|` inside a cell must be written `\|`**, or the row splits — see the defect found below.

Thresholds not named by the frozen sentence, and why: `MIN_PROPS=4` is the sentence's "at least
four"; `MAX_QUOTE_WORDS=25` is the sentence's quote cap (whitespace words); `MIN_QUOTE_WORDS=3`
(counted as identifier tokens) keeps a bare token from "binding" a pin line;
`MIN_DISTINCT_ROWS=2` keeps four propositions from resting on one row; `ACCESS_DATE` and the
frozen base are the round's own.

## Receipts (exact text retained)

**1. Base — the no-work control, MISS, exit 1** (`receipts/r-base.txt`):

```
C2_R52: meta rev=85d57a818c3707397e21c840b6498b105ba798aa base=85d57a818c37 entry=corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md work=…
C2_R52: a ok=0 entry=absent
C2_R52: b ok=0 skipped=entry-absent
C2_R52: c ok=0 skipped=entry-absent
C2_R52: d ok=0 skipped=entry-absent
C2_R52: e ok=0 skipped=entry-absent
C2_R52: work=… probe=written
C2_R52: entailment=not-checked (outside non-author review)
C2_R52: clauses=abcde clauses_met=0 admitted=0/1 verdict=TARGET_MISSED rev=85d57a818c3707397e21c840b6498b105ba798aa
exit=1
```

**2. Lane tip** (`receipts/r-tip.txt`) — identical, exit 1: the lane tip *is* the frozen base.

**3. Green staged fixture** (`receipts/r-green.txt`, fixture `bfad9e67…`) — my own six-column
grammar, five propositions over three registry rows and one pinned file:

```
C2_R52: a ok=1 index_row=`knowledge/hyprland-dispatcher-action-effects-r52.md` (MA...
C2_R52: b ok=1 propositions=5 ids=5 forms=table
C2_R52: c ok=1 rows_bound=3/5 distinct_rows=3
C2_R52: d ok=1 quotes_bound=5/5 quotes_raw=5/5 pins=1 policy=whitespace-collapsed pins_prior_equal=1/5
C2_R52: e ok=1 prose_rows=3 prop_rows=3 manifest_rows=3
C2_R52: clauses=abcde clauses_met=5 admitted=1/1 verdict=TARGET_MET rev=bfad9e67224d9a0d6c901cd656906fba009bc02c
exit=0
```

**4. Mutation suite — 18/18 caught, green holds** (`receipts/r-mutants.txt`, driver `mutants.py`).
One change per mutant, each committed on top of the green fixture in one scratch clone that is
reset between mutants (`git reset --hard` + `git clean -qfdx`); an earlier version cloned the
lane 18 times and died on a transient `git clone` object-copy error, so the driver now clones
once:

| mutant | clause | reported reason |
|---|---|---|
| index_row_removed | a | `index_row=absent` |
| only_three_propositions | b | `propositions=3<4` |
| support_empty | b | `P2:empty(support)` |
| row_not_mined | c | `P1:status(queued)` |
| row_opened_earlier | c | `P3:opened(2026-10-26)` |
| row_reused_from_base | c | `P1:row_not_new(S364)` |
| used_by_other_entry | c | `P1:used_by(corpus/knowledge/hyprland-dispatcher-dispatch-r51.md)` |
| anchor_no_fetch_root | c | `P3:anchor_no_fetch_root` |
| anchor_no_revision | c | `P5:anchor_no_revision` |
| quote_not_at_pin | d | `P1:quote_not_at_pin(Hyprland-legacy-DispatcherTranslator.cpp:45)` |
| quote_too_long | d | `P3:quote_too_long(28)` |
| pin_not_manifested | d | `P3:pin_not_manifested(Hyprland-Other-File.cpp)` |
| pin_file_absent | d | `P3:pin_not_manifested(Hyprland-Absent.cpp)` |
| pin_line_out_of_range | d | `P4:pin_line_out_of_range(…:99999)` |
| manifest_row_mismatch | d | `P1:manifest_row_mismatch(S370!=S372)` |
| unmapped_body_row | e | `row_unmapped:S373` |
| orphan_proposition | e | `row_uncited:S373` |
| duplicate_quote | e | `duplicate_quote:if arg empty arg active` |

Summary `MUTANTS: mutants=18 escaped=0 green_ok=True`, exit 0.

**5. Block form and setup errors** (`receipts/r-blockform.txt`) — the block-form fixture passes
5/5, and four setup paths each exit 2 with a setup-error line: unresolved `--rev`, non-git
`--repo`, `--work` inside the scored repository (`scratch dir inside the scored repository`), and
the round-51 slug offered as the target (`must differ from the round-51 entry`).

**6. The real `C2EntryDraft` draft, staged unmodified** (`receipts/r-draft-as-is.txt`) — the
sibling's `entry-draft.md` bytes copied into a scratch clone at
`corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md`, with the four proposed registry rows
S370–S373 appended, its four pinned files staged under
`.ufo/waves/round-52/w1/C2EntryDraft/fetch/`, and one README index row:

```
C2_R52: a ok=1 index_row=`knowledge/hyprland-synthetic-key-dispatch-r52.md` (MADO-R5...
C2_R52: b ok=1 propositions=18 ids=18 forms=table
C2_R52: c ok=1 rows_bound=4/18 distinct_rows=4
C2_R52: d ok=1 quotes_bound=18/18 quotes_raw=6/18 pins=4 policy=whitespace-collapsed pins_prior_equal=4/18
C2_R52: e ok=1 prose_rows=6 prop_rows=4 manifest_rows=0
C2_R52: clauses=abcde clauses_met=5 admitted=1/1 verdict=TARGET_MET rev=…
exit=0
```

All 18 quotes verify verbatim at their cited pin line spans across 4 pins. This is the
interoperability evidence: the counter reads an entry written by a different seat, in that seat's
table shape (`id | proposition | row | pin:anchor | quote (<=25 words) | support class | why it
supports`), without being taught the draft's exact header strings. The `quotes_raw=6/18` and
`pins_prior_equal=4/18` figures are printed on the same line — see the feedback section below.

**7. Recycled round-51 body at the target path — MISS, exit 1** (`receipts/r-recycled.txt`):

```
C2_R52: a ok=1 index_row=`knowledge/hyprland-dispatcher-action-effects-r52.md` (MA...
C2_R52: b ok=0 propositions=0<4
C2_R52: c ok=0 rows_bound=0/0 distinct_rows=0
C2_R52: d ok=0 quotes_bound=0/0 quotes_raw=0/0 pins=0 policy=whitespace-collapsed
C2_R52: e ok=0 prose_rows=8 prop_rows=0 manifest_rows=6 miss=rows_too_few:0
C2_R52: clauses=abcde clauses_met=1 admitted=0/1 verdict=TARGET_MISSED rev=…
exit=1
```

A recycled body passes the index clause and fails everywhere else. This is the C2 analogue of
the round-50 falsification the round-51 counter carried in clause (c).

**8. Satisfiability control** (`receipts/r-draft-fixed.txt`) — the same draft with the two
markdown corrections applied (see below), 5/5, exit 0. The predicate is reachable by the lane's
own entry content, not only by my synthetic fixture.

## Three corrections in the sibling's draft (fixed by the sibling, verified by me)

Running the counter against `C2EntryDraft/entry-draft.md` surfaced two real defects in its
**markdown** proposition-map table. The sibling's own `proposition-map.tsv` was correct in both
respects; the markdown table had diverged from it.

1. **Unescaped `|` in P07's quote cell.** The cell holds
   `… modMask |= HL_MODIFIER_SHIFT;`. In a markdown table an unescaped `|` ends the cell, so
   the row split into eight cells: P07's quote truncated to its first half and its support cell
   shifted onto the support-class value `direct`. The counter reported `P07:support_thin` and
   `P07:quote_not_at_pin`. Fix: escape it as `\|=`.
2. **A bare `:NNN` pin cell across a file switch.** P07 is
   `KeybindManager.cpp:223-225`; P08–P12 then read `:540-543`, `:544-547`, `:565-566`, `:557`,
   `:582-586`, which the house shorthand resolves to *KeybindManager.cpp*. Their rows are S370/S371
   — the legacy dispatcher translator — and the draft's own TSV gives the real anchor. Verified on
   the bytes: `Hyprland-legacy-DispatcherTranslator.cpp:540-543` holds P08's quote, while
   `Hyprland-KeybindManager.cpp:540-543` holds `void CKeybindManager::onSwitchOnEvent(...)` —
   unrelated code. The same applies to P15 (`:612`) and P17 (`:574`), which the TSV places in the
   translator, not in the preceding `ConfigActions.hpp`. The counter reported
   `P08..P12:anchor_no_pin(KeybindManager.cpp)` and `quote_not_at_pin` on the same rows.

I sent both to the sibling seat; it regenerated the markdown table from the TSV (pipe escaped,
full pin filename in every `pin:anchor` cell) and re-verified with its own checkers
(`md-table-check.txt`: `rows_md=18 rows_tsv=18 ids_match=True failures=0`; `quotes-check.txt`:
`props=18 rows=4 pins=4 quote_max_words=25 failures=0 verdict=OK`). I then re-ran my counter
against the corrected draft: 5/5, exit 0 (receipt 6). The defects and the fix are in the
sibling's report under "Counter-seat feedback applied".

**A third correction, from a factual error rather than a table defect.** `C2Novelty` flagged
that P16's claim rested on a quote that did not support it. The sibling confirmed and fixed it
as a wrong sentence: `Actions::pass(modMask, key, w)` calls `xtract(w)` first, and `xtract` is
`return window.value_or(Desktop::focusState()->window());`
(`Hyprland-ConfigActions.cpp:47-49`) — so an empty selector resolves to the **focused** window and
the focus-switch block does run, contradicting the old "delivers without moving focus" wording.
Step 6 was rewritten, P12 narrowed to the translator-side ternary, P16 now carries the `xtract`
quote at anchor 47–49, P17 became the surviving-null case, and the key-not-found proposition
moved to P18: the map is now 18 propositions over the same 4 rows.

I re-read the corrected draft: **5/5, `propositions=18 ids=18`, `quotes_bound=18/18`** (receipt 6
as it now stands). `quotes_raw` stayed at 6 — only the denominator moved from 17 to 18 — which
confirms the sibling's prediction that the multi-line `xtract` quote is reflowed rather than
byte-exact. The important part for the report is *why* my counter never saw this defect: the
old P16 quote sat correctly at the line the draft cited, so the error was in the claim the quote
was attached to, not in the quote's location. A structural counter binds quotes; it cannot tell
that the claim is false. That is the honest boundary of this seat's work, and the reason the
claim's "an independent non-author samples actual source truth" is not optional.

## Feedback from the attack seats, and what I changed

`C2Novelty` (critic) sent three points against this counter after it had read it. Two were
right and are now in; one was already handled.

1. **Freshness: require each cited row id to be absent from the base registry.** Already
   implemented, and it is the reason the counter is not fooled by the date check. `C2Novelty`
   is right that the date check alone is bypassable — S364–S369 are also dated `2026-10-27` —
   and clause (c) therefore compares the registry at the frozen base with the registry at
   `<rev>` and reports `row_not_new(S364)` for a row that already existed. The mutation
   `row_reused_from_base` drives exactly that (receipt 4).
2. **Freeze one quote-comparison policy and print it.** Right, and now done. The counter
   prints `quote_policy=whitespace-collapsed` in its meta line and `policy=whitespace-collapsed`
   in clause (d), and it reports the byte-exact count next to the binding count:
   `quotes_bound=18/18 quotes_raw=6/18`. On the sibling's draft only 6 of 18 quotes are
   byte-exact — 12 are reflowed across source lines — so the verdict genuinely does depend on
   the policy, and a reader can now see that instead of having to guess. Whitespace-collapsed
   is frozen as the binding policy because a quote reflowed by markdown is still the same
   quote; the stricter number is reported rather than hidden.
3. **Print how many bound pins are byte-equal to a prior round's pin.** Now printed as
   `pins_prior_equal=4/18` on the sibling's draft — all four bound pins are byte-identical to
   the round-51 copies, which is what the sibling's own `fetch/verify.txt` says. This is a
   **diagnostic, not a gate**, deliberately: a new row may legitimately reopen a pinned file
   under a new scope (the row's own freshness is clause (c)'s job), so gating on byte-equality
   would fail the lane's own entry for a fact that is not a defect. It is printed so a reviewer
   sees it.
4. `C2Novelty`'s sample defect — P16 needs `xtract` at `ConfigActions.cpp:47-49`, unquoted —
   was a **factual error in the draft, not only a quoting gap**, and the entry seat has fixed it
   (see below). My counter could not have caught it: it binds P16's old quote correctly at the
   line the draft cited, because the error was in the *claim* the quote was attached to, not in
   the quote's location. That is exactly the class of defect the counter refuses to certify.

## Risks and notes for the freeze

- **Clause (c) is shape-sensitive on the registry rows.** It requires each cited row's `anchor`
  to carry the round's fetch path and a 40-hex revision, and its `used-by` to name the entry.
  When the data seat appends S370–S373 the anchor must name
  `.ufo/waves/round-52/…/fetch/…` and revision `efb50993780079460b0cbed1363e2166a2de1d9f`, or
  the clause reports `anchor_no_fetch_root` / `anchor_no_revision`. This is deliberate, not
  incidental: it is what stops a row opened in an earlier round from being passed off as opened
  this round. The sibling has been told the exact requirement.
- **`row_not_new` is the strongest single check** and depends on the frozen base being present in
  the scored repository. It compares the registry at `BASE` with the registry at `<rev>`.
- **Clause (e) scopes "unmapped row" to the rows this entry opened.** A prose mention of a
  held row (`S364`–`S369`) is not a proposition this entry has to map, so the unmapped-row check
  is scoped to rows that are new this round; a prose row that names no registry row at all is a
  defect of any kind (`row_not_in_registry`). The `held`/`ground`/`lane`/`recheck`/`verified-at`
  marker lines are excluded from the prose scan for the same reason.
- **The counter certifies structure, not truth.** A quote that verifies at a cited line can
  still be cherry-picked, and a claim can be wrong while its quote is correctly located. Only
  an outside non-author reviewer can judge entailment; this counter's own final line refuses to
  claim it.
- **The header grammar is deliberately loose** (whitespace/case/parenthetical-insensitive, two
  support tiers, optional id column, optional pin manifest, path-or-basename pin names). That
  looseness is what let the counter read the sibling's draft unchanged, and it is also its main
  sharp edge: a table whose columns are named in a way the role lists do not cover is not read
  as a proposition map at all, and clause (b) reports `propositions=0<4`. That is a legible
  failure, not a silent pass.
- The `id` column is optional and synthesized `P1..Pn` when absent; with the id absent, the
  per-proposition reference check of clause (e) cannot run, and the id is then not a stable
  handle. An entry that wants the completeness check to bite should carry an id column.

## Scratch and host discipline

All clones, fixtures, probe dirs and receipts lived under
`/fast/scratch/hyaku/mado-r52/C2CounterDraft/` (explicit `TMPDIR` for every counter run), and
were removed on finish; the receipts were copied into the seat dir first. Disk guard checked
before the first heavy pass and again at the end: `/fast/scratch` 26% used / 598G free at the
start, 27% used / 593G free at the end; `/` 35% used / 589G free. No ENOSPC.

Every git mutation was inside a scratch clone, each preceded by `git rev-parse --show-toplevel`
asserting the clone root (`recycled-check.sh` prints the assertion). No git or jj operation
touched the lane: no commit, no push, no branch, no checkout in
`/home/vgpnk/Projects/shokunin/mado-shokunin`. **No package install, no pacman transaction, no
tooling change of any kind** — the counter and every driver use only the Python 3.14 standard
library already present, so the install channel in `/home/vgpnk/.omp/agent/RULES.md` was never
reached. No host, config, service, compositor, process or package state was read or written; no
screenshot; no producer executed; no URL fetched. The only source bytes I read were the
round-51 and round-52 fetch pins already on disk in the lane, and the sibling's draft bytes.

Sources read (locally available, no network):

- `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` — the round-51 entry, to see the house
  grammar, the pin manifest, the `source:`/`held:`/`ground:` marker lines and the chain style.
- `corpus/SOURCES.md` — the registry table's 11-column shape (`id|source|kind|tier|scope|anchor|
  teaches|status|opened|recheck|used-by`) and rows S364–S369, and the `## Paths` / `## Search
  log` / `## Leads` sections.
- `corpus/README.md` — the coverage-map index row shape.
- `quality/counters/c2-r51-dispatch-entry.py` — the round-51 counter, for the counter's own
  conventions (clause-per-line output, probe JSON, scratch refusal, exit codes) and for the
  citation grammar it documents.
- `quality/counter-selftest.py`, `quality/check-index.py` — the lane's selftest and index-gate
  conventions.
- `.ufo/waves/round-51/fetch/Hyprland-legacy-DispatcherTranslator.cpp` — the pinned upstream
  file, read as the fixture's source of quotes (lines 45–48, 51–62, 248–256).
- `.ufo/waves/round-52/w1/C2EntryDraft/entry-draft.md` and `proposition-map.tsv` — the sibling's
  in-flight entry, read to check interoperability; the two defects above were found there.
- `.ufo/waves/round-52/w1/C2EntryDraft/fetch/Hyprland-*.cpp|hpp` — the sibling's staged pins,
  read to verify the quote/anchor claims above.

Upstream provenance of the pinned bytes (for the report's own citations, not fetched by me):
Hyprland 0.56.2 at commit `efb50993780079460b0cbed1363e2166a2de1d9f`, from
`https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp`
and the sibling's two companion paths, read from disk on 2026-10-27 (the sibling's
`pins.txt` records the digests and that no URL was fetched by it either).

## Honest limits

- The counter is a **draft**: it is not committed, it is not in `quality/counters/`, and no
  tracked lane file was touched. Integration is the L1's copy-one-file step.
- Clause (b)'s "substantive" is measured structurally — five fields present, a distinct id and
  a distinct claim, a rationale of at least four identifier tokens. Whether a proposition is
  *materially* substantive is a reviewer's judgement, not a mechanical one.
- Clause (e)'s completeness is measured at row granularity (every row this entry opened is
  mapped; every mapped row is cited; every proposition id is drawn on). A factual proposition
  asserted in prose but bound to no registry row at all is not detectable from the entry alone;
  the `row_not_in_registry` check catches the *opposite* case (a cited row that does not exist).
- The quote binding is exact-text, whitespace-collapsed, within the cited line span. A quote
  that is correct in the source but paraphrased in the entry will not bind — that is the
  intended behaviour, but it means the entry must quote verbatim.
- Nothing here measures entailment, novelty, held-fact omission or wording reuse. Those are
  this round's attack seats, and the counter's own output says so on every run.

Report: .ufo/waves/round-52/w1/C2CounterDraft.md
Report: .ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py
Report: .ufo/waves/round-52/w1/C2CounterDraft/make-fixture.py
Report: .ufo/waves/round-52/w1/C2CounterDraft/mutants.py
Report: .ufo/waves/round-52/w1/C2CounterDraft/blockform-check.py
Report: .ufo/waves/round-52/w1/C2CounterDraft/make-draft-fixture.py
Report: .ufo/waves/round-52/w1/C2CounterDraft/recycled-check.sh
Report: .ufo/waves/round-52/w1/C2CounterDraft/run-receipts.sh
Report: .ufo/waves/round-52/w1/C2CounterDraft/receipts/r-base.txt
Report: .ufo/waves/round-52/w1/C2CounterDraft/receipts/r-tip.txt
Report: .ufo/waves/round-52/w1/C2CounterDraft/receipts/r-green.txt
Report: .ufo/waves/round-52/w1/C2CounterDraft/receipts/r-mutants.txt
Report: .ufo/waves/round-52/w1/C2CounterDraft/receipts/r-blockform.txt
Report: .ufo/waves/round-52/w1/C2CounterDraft/receipts/r-draft-as-is.txt
Report: .ufo/waves/round-52/w1/C2CounterDraft/receipts/r-draft-fixed.txt
Report: .ufo/waves/round-52/w1/C2CounterDraft/receipts/r-recycled.txt
Report: .ufo/waves/round-52/w1/C2CounterDraft/receipts/r-fixture-build.txt
