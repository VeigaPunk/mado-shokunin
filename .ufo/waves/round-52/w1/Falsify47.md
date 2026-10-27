# Falsify47 — C2 held-ground novelty

## Attacked clause

Frozen C2, the distinctness qualifier only: `claims-frozen.md:11` — “Target: **a distinct new
indexed knowledge entry** is grounded in sources opened this round”; `registration.md:9` — “one
new indexed entry on a **distinct** Hyprland dispatcher-execution mechanism … A counter checks
proposition count, row/pin/quote bindings and index”.

Two defects, both measured against committed bytes, no predicate or claim edit:

- **D1 — the enumerated counter checks contain no novelty clause.** `registration.md:9` enumerates
  the round-52 counter's checks as “proposition count, row/pin/quote bindings and index”. The word
  *distinct* has no clause. A clone of `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` with
  fresh `S###` rows and a fresh slug satisfies every enumerated check while adding no mechanism.
  (Named without reproduction by `w1/Falsify15.md:5,19`; this seat reproduces the same gap against
  the only committed implementation — see below.)
- **D2 — the lane's only committed novelty implementation is bypassable.** The r51 counter's
  `clause_c` (`quality/counters/c2-r51-dispatch-entry.py:456-486`) is a per-file **containment**
  ratio: `hits / len(body)`, where `body` is the *candidate's own* 8-gram shingle set
  (`:479`), computed over `body_text()` (`:434-446`) — a projection that **drops every line
  starting with `|`**, every fenced block, and lines beginning
  `source|ground|held|verified-at|recheck|lane|pin` (`:441-444`). Consequences: padding the
  candidate lowers its score with no penalty for copied ground; and the proposition→source table
  that C2 *mandates* is invisible to the only novelty measurement.

## Reproducible setup and command

Read-only. No git/jj mutation, no tracked write, no package query, no live read, no producer,
no source fetch, no install.

```
TMPDIR=/fast/scratch/hyaku/mado-r52/Falsify47 \
  python3 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/Falsify47/probe.py
```

`probe.py` (seat copy) loads the committed counter by path
(`quality/counters/c2-r51-dispatch-entry.py`) with `importlib`, reuses its own
`body_text`, `shingles`, `MAX_OVERLAP`, `MIN_BODY_SHINGLES`, `KNOW_RE`, `ls_files`, `show`, and
then (a) replays the `clause_c` scoring loop at base
`85d57a818c3707397e21c840b6498b105ba798aa` (67 files under `corpus/knowledge`), and (b) calls the
committed `clause_c(repo, BASE, BASE, <fixture>)` directly with each fixture as `entry_text`.
Constants are the counter's: `NGRAM=8`, `MAX_OVERLAP=0.30`, `MIN_BODY_SHINGLES=300`
(`c2-r51-dispatch-entry.py:68-73`).

Fixtures (seat copies, all in `.ufo/waves/round-52/w1/Falsify47/`):

| fixture | content |
|---|---|
| `f1_verbatim.md` | byte-identical copy of the r51 entry under a new slug |
| `f2_diluted.md` | `f1` verbatim + 9 000 words of unrelated vocabulary prose |
| `f3_tabled.md` | every r51 table row verbatim + 400 synthetic unique tokens |
| `f4_props_in_table.md` | all nine r51 chain paragraphs verbatim inside table cells + 420-word novel abstract |
| `f5_paraphrase.md` | r51 chain with a mechanical synonym swap and sentence reversal |

## Actual result

Entry ground measured at base: r51 entry = 31 514 B, 265 body lines, **3 364 body shingles**;
its **40 table rows contribute 0 shingles** to `body_text`; the nine-step chain is 1 757 shingles
(52.2 % of the body).

Replayed loop and direct `clause_c` call agree:

```
FIXTURE f1_verbatim.md       body= 3364 worst=99.05% verdict=FAIL   CLAUSE_C ok=0 max=99.0%
FIXTURE f2_diluted.md        body=12365 worst=26.95% verdict=PASS   CLAUSE_C ok=1 max=26.9%
FIXTURE f3_tabled.md         body=  399 worst= 0.00% verdict=PASS   CLAUSE_C ok=1 max=0.0%
FIXTURE f4_props_in_table.md body=  420 worst= 0.00% verdict=PASS   CLAUSE_C ok=1 max=0.0%
FIXTURE f5_paraphrase.md     body= 1849 worst= 9.95% verdict=PASS   CLAUSE_C ok=1 max=10.0%
```

- **f2 is a verbatim clone** — 3 332 of the r51 entry's 3 364 body shingles (99.05 %) are present
  — and the committed `clause_c` returns `ok=1`. Only 7 850 shingles of padding were needed; the
  arithmetic is `hits/|body|`, so the cap admits `0.30 × 3 364 = 1 009` verbatim shingles in an
  r51-sized entry: steps 1-5 of the chain (945 shingles) fit under the cap untouched.
- **f4 preserves every proposition of the r51 mechanism verbatim** (paragraphs copied into table
  cells, `|`→`/` only) and still scores 0.0 %: `body_text` never sees table rows. The 300-shingle
  floor is met by 420 words of arbitrary prose.
- **f5** is a proxy for a human rewrite: 8-gram lexical overlap dies (10.0 %), propositions do not.
  A real paraphrase is strictly freer, so 10.0 % is an upper bound `[INF]`.
- **f1 fails correctly** (`ok=0`, 99.0 %): the check has a working red for byte-identical copies.
  The finding is not “no novelty check”, it is “the novelty check measures the wrong projection and
  normalises in the wrong direction”.

## Reproduced

- **Yes** for D2: the committed `clause_c` returns `ok=1` on a fixture containing 99.05 % of the
  prior entry's body shingles (f2) and on a fixture carrying all nine prior propositions (f4).
  `probe-output.txt` is the run receipt; exit 0.
- **Not reproducible yet** for D1: no round-52 counter exists at base (no `quality/counters/c2-r52*`;
  `w1/C2CounterDraft/` absent), so D1 is a predicate gap read from `registration.md:9`, not a
  measured acceptance.
- `clause_c` was called with `rev = BASE`, so the candidate-file branch (`:467-474`) contributes
  only the 3 pre-existing `.ufo/waves/*/candidate/` files; the round-52 candidate path is untested.

## Proposed bounded move (recommendation only — no amendment after data)

For the round-52 counter as built, or the next round: score the **whole** entry (prose + table
cells + fenced spans), normalise by the **reference** mass (`Jaccard`, or `hits/max(|cand|,|ref|)`)
rather than the candidate's own, and run the mandated proposition table through the same check.
Add three red fixtures — padded clone, table clone, paraphrase — that must each return `ok=0`.
Keep outside source-truth review as the only semantic judge; none of this is entailment proof.
Replacing containment with Jaccard alone fixes f2 but not f3/f4/f5.

## Axes and harm

Coverage only: a clone of r51 adds no new dispatcher-execution coverage, so a counter that accepts
it inflates the coverage axis. No operability effect and no axis harm claimed.

## Limitations

- The measured object is the r51 clause, not an unseen r52 clause; D2 transfers only if the r52
  counter reuses `body_text`/`clause_c` (its design is absent at base).
- Fixtures are seat-local synthetic bytes; the filler is generated vocabulary prose. They test
  predicate acceptance, not author intent.
- `MIN_BODY_SHINGLES=300` is satisfiable with 420 words of content-free prose (measured), so the
  size floor is not a substance floor.
- No fresh external source was opened; this seat stayed inside held-ground material and local
  source bytes. No live/runtime/package action.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify47.md`
- `.ufo/waves/round-52/w1/Falsify47/probe.py`
- `.ufo/waves/round-52/w1/Falsify47/probe-output.txt`
- `.ufo/waves/round-52/w1/Falsify47/f1_verbatim.md`
- `.ufo/waves/round-52/w1/Falsify47/f2_diluted.md`
- `.ufo/waves/round-52/w1/Falsify47/f3_tabled.md`
- `.ufo/waves/round-52/w1/Falsify47/f4_props_in_table.md`
- `.ufo/waves/round-52/w1/Falsify47/f5_paraphrase.md`

No installs. Scratch `/fast/scratch/hyaku/mado-r52/Falsify47/` used for the run and removed after
the seat copies were made.

Report: `.ufo/waves/round-52/w1/Falsify47.md`
