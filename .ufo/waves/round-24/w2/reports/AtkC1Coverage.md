# AtkC1Coverage — C1 axis attack after landing (round 24, wave 2)

Seat: MadoR24.AtkC1Coverage. Lane `mado-shokunin` at `39c596307333b8ca0a1e42b3f3b9a748bb8b208b` (base
`8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122`). Read-only: no lane write outside this report; no git/jj write in
the lane or fleet; the only git writes are in the scratch clone `/fast/scratch/hyaku/mado-r24/w2/c1mut`.

**What I attack.** The registration sentence (`.ufo/waves/round-24/registration.md` C1): "the `corpus/README.md`
`## Frontier` item 'Still open: rule *attribution*' (round-12 bullet) moves to documentary sourced ground in a new
entry `corpus/knowledge/rule-attribution-r24.md`". Two precise questions:

1. Did the frontier item actually move, and does the frozen predicate test that move?
2. Do the counted rows add attribution ground, or do they re-score rule semantics already in
   `keybind-rule-semantics.md` / `window-rule-effects-getprop.md`? How many of the 23 PASS rows are
   attribution-relevant (reviewer RevRegistration H1)?

## Commands run

- `python3 -I .ufo/waves/round-24/c1/count.py 39c596307333b8ca0a1e42b3f3b9a748bb8b208b` (counted/refetch mode,
  one run): 26 rows, `PASS_ROW=23`, `distinct_sources=14`, `readme_indexed=True`, `verdict=TARGET_MET`,
  `counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66` (label sha256:).
  FAIL rows: A5 (`quote-off-topic`), A7 (`quote-off-topic`), A8 (`quote-off-topic`).
- Falsifier: sandbox clone of the lane at the tip under `/fast/scratch/hyaku/mado-r24/w2/c1mut`, note replaced by
  the nine counted rows that carry **no attribution content** (A1, A2, A3, A4, A17, A20, A21, A25, A26), committed
  as `25e91210f21e05d019681d09668a4e2b97cac45e`, scored with
  `MADO_LANE=/fast/scratch/hyaku/mado-r24/w2/c1mut python3 -I .ufo/waves/round-24/c1/count.py 25e91210`:
  9 rows, `PASS_ROW=9`, `distinct_sources=6`, `readme_indexed=True`, `verdict=TARGET_MET`.
- Spot check of the note's headline negative ("no attribution channel"), read-only in
  `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`:
  `grep -n registerCommand src/debug/HyprCtl.cpp` → the only rule-listing verb is `workspacerules` at `:2005`
  (`clients` `:2007`, `getprop` `:2032`); `grep -n rule src/managers/EventManager.cpp` → no match (no socket2
  rule event); `grep -rn "Rule workspace matched by" src/` → only `src/desktop/view/Window.cpp:2187`
  `... static_.workspace`, i.e. the workspace-rule path as A18 says.

## 1. Did the frontier item move? No — the README now says both things

`git diff --numstat 8e5d9369 39c59630 -- corpus/README.md` is `15 0`: fifteen insertions, **zero** removals. The
round-12 frontier bullet (`corpus/README.md:99-103`) is byte-identical, including `:102`:

> Still open: rule *attribution*, output-management behavior, the input debugging ladder and Waybar module text

The wave-1 edit only appended a coverage-map row (`:47`) and a Frontier subsection (`:198-205`) that claims
"Round 24 moves the round-12 frontier item ... onto documentary sourced ground". So the `## Frontier` section now
asserts the item open (round-12 bullet) and moved (round-24 bullet) in the same section.

The counter cannot see this: its only README test is `re.search(r"^\| \`knowledge/rule-attribution-r24\.md\`")`
over the coverage map (`c1/count.py:150`). It does not read the frontier bullet, so `readme_indexed=True` is
compatible with the frontier item being untouched. The registration's "the same counter shows it unmoved" test is
therefore not implemented for the frontier item it names; it tests note-existence-plus-index, which is a different
surface.

Note the no-removal guard does not cover README (it names SCORECARD, SOURCES, LOG, PROVINCE), so annotating the
round-12 bullet is inside this round's allowed repairs.

## 2. Restatement versus new attribution ground

Prior corpus already holds most of these facts, with these lines:

| prior fact | prior line |
|---|---|
| `getprop` returns the applicator value, no rule identity; attribution claim explicitly rejected | `window-rule-effects-getprop.md:33, :76, :146` |
| `hyprctl --help` lists `workspacerules`; `workspacerules -j` measured | `window-rule-effects-getprop.md:12, :24, :31, :140` |
| wiki: all props must match, top-to-bottom effects | `window-rule-effects-getprop.md:35`; `keybind-rule-semantics.md:177` |
| named rules first, then anonymous | `keybind-rule-semantics.md:207` |
| last match takes precedence | `keybind-rule-semantics.md:208` |
| dynamic effects re-evaluated on property change | `keybind-rule-semantics.md:210` |
| dynamic tags carry `*`; only named rules live-toggleable | `keybind-rule-semantics.md:212, :213, :285` |
| `clients -j` exposes per-window tags (starred) as an observed read | `keybind-rule-semantics.md:253, :263, :280` |

Per-row classification of the 26 claim rows (A5, A7, A8 fail the counter; count column is `PASS_ROW`):

| row | S### | counted | attribution-relevant | restates a prior line | verdict |
|---|---|---|---|---|---|
| A1 | S153 | PASS | no — engine storage | no | generic rule-engine internals |
| A2 | S154 | PASS | no — accessor/header | no | generic |
| A3 | S155 | PASS | no — apply flow | partly (keybind §4.3 rows 4–5 semantics) | generic |
| A4 | S155 | PASS | no — traversal | no | generic |
| A5 | S155 | FAIL | yes — priority class | no | real quote, rejected only by the topic word filter |
| A6 | S155 | PASS | yes — rule-property mask companion slot | no | **new attribution ground (origin metadata)** |
| A7 | S156 | FAIL | yes — value+mask pair | no | real quote, rejected only by the topic word filter |
| A8 | S156 | FAIL | yes — dynamic-tag mask | no | real quote, rejected only by the topic word filter |
| A9 | S157 | PASS | no — match test on tag keeper | no | generic matching |
| A10 | S158 | PASS | yes — tags emitted in `clients` from tag keeper | live fact known (:253, :280); source anchor new | **new source anchor, known route** |
| A11 | S158 | PASS | yes — getprop opacity value only | :33, :76, :146 | restatement |
| A12 | S159 | PASS | yes — Lua name→rule registry | no | **new attribution ground (identity)** |
| A13 | S160 | PASS | yes — enable setter handle | :213, :285 (semantics) | restatement (Lua form new) |
| A14 | S160 | PASS | yes — isEnabled readback | :213, :285 | restatement |
| A15 | S162 | PASS | yes — named special category | named blocks known (:172-177); source plumbing new | **new, plumbing** |
| A16 | S162 | PASS | yes — named-key traversal | same | **new, plumbing** |
| A17 | S163 | PASS | no — layer apply gate | no | generic |
| A18 | S164 | PASS | yes — matched-by log is workspace path | no | **new attribution ground (negative channel)** |
| A19 | S165 | PASS | no — Lua rule syntax | :172-177; r12 wiki syntax | restatement |
| A20 | S165 | PASS | no — dynamic re-eval | :210 | restatement |
| A21 | S165 | PASS | no — order/last wins | :207, :208, :35 | restatement |
| A22 | S165 | PASS | yes — tag `*` suffix, check `clients` | :212, :253, :263 | restatement |
| A23 | S166 | PASS | yes — layer rule handle | :213 (same handle pattern); layer API new | partial restatement |
| A24 | S167 | PASS | yes — `workspacerules` listing (workspace rules only) | :12, :24, :31, :140 | restatement |
| A25 | S168 | PASS | no — all props must match | :177, :35 | restatement |
| A26 | S168 | PASS | no — named first then anonymous | :207 | restatement |

Counts over the 23 PASS rows:

- **Attribution-relevant: 12** (A6, A10, A11, A12, A13, A14, A15, A16, A18, A22, A23, A24). The other **11**
  (A1, A2, A3, A4, A9, A17, A19, A20, A21, A25, A26) are generic rule-engine, matching, syntax or ordering
  semantics that carry no information about which rule produced an effect.
- **Strict restatements of prior notes: 10** (A11, A13, A14, A19, A20, A21, A22, A24, A25, A26), plus A23 partial.
- **New attribution ground: 6** (A6, A10, A12, A15, A16, A18), from S155, S158, S159, S162, S164 — five sources.
  Of those, A10 is a source-level anchor for a live fact the keybind note already measured (clients tags), and
  A15/A16 are config plumbing for a named-rule mechanism the keybind note already relied on. The facts that are
  new to the corpus at all: A6 (property-mask bookkeeping), A12 (Lua name registry), A18 (the matched-by log line
  is the workspace path), plus the Lua handle API form in A13/A14.

So the note is **majority re-scoring**: 10 strict restatements + 11 generic rows = 21 of 23 PASS rows either
repeat a prior note or do not concern attribution. The six new attribution rows clear the frozen target floor of
six, but only just; without A10/A15/A16 the note would fall to three new attribution rows (A6, A12, A18), below
the floor.

### The proposed route was already assembled in the prior notes

`window-rule-effects-getprop.md:146` already rejected "`getprop` proves which window rule matched" and set the
flip condition "a version-pinned read surface that returns a rule name or matched-condition record"; the keybind
note already recorded named-rule toggles (`:213, :285`), dynamic-tag `*` (`:212`) and per-window tags in
`clients -j` (`:253`). The new note's usable answer — "give the rule a unique `tag`, read `tags` in `hyprctl
clients`" — is a composition of those two prior notes plus the wiki sentences A21/A22, not a newly observed
channel. What r24 genuinely adds is the systematic negative sweep and the Lua handle/mask detail; the note itself
labels the sweep "lane observations ... not counted rows".

## 3. H1 confirmed, in the strongest form: the predicate is insensitive to attribution

RevRegistration H1 reported a sandbox control meeting the counter with generic wiki rule sentences. I tested the
real predicate with the real note's own generic rows: a note containing only A1, A2, A3, A4, A17, A20, A21, A25,
A26 — no attribution table, no tag route, no sweeps — scores `PASS_ROW=9` from 6 sources and `TARGET_MET`
(sandbox rev `25e91210`, refetch mode). The 23-row note does not merely tolerate generic rows; the frozen target
is met in full by generic rows alone. H1 is not a hypothetical: **11 of the 23 PASS rows in the landed note are
exactly such rows**, and the answer table's most attribution-specific line ("per-property origin", A5–A8) rests
on three rows (A5, A7, A8) the counter rejects.

That rejection is lexical, not substantive: `TOPIC_RE` uses `\b(?:...|rules?)\b` and `_` is a word character, so
`PRIORITY_WINDOW_RULE`, `eRuleProperty` and `RULE_PROP_NONE` do not match; A5/A7/A8 are real, quoted, sha-matched
lines. The counter's topic test therefore fails in both directions: it rejects three attribution-bearing rows and
accepts eleven non-attribution ones.

Note the round already records the residual at `corpus/lessons/round-24.md:16` (M24-2: "v2 is still met by true
but non-attribution rule lines", citing H1 and CritC1Predicate, "Not fixed this round"). My finding is not that
the residual is hidden; it is that the landed C1 prose and README movement claim are still written as if the
count established attribution, and M24-2's own number should be updated from the sandbox's 6 to the landed
note's 11 generic PASS rows.

## 4. Headline answer is uncounted (not false on my spot check)

The note's answer — "no upstream channel maps an applied property back to the rule that set it" — is carried by
the "Negative sweeps" section, which the note explicitly excludes from counting. My read-only spot check of the
pinned clone agrees: `workspacerules` is the only rule-listing hyprctl verb, `EventManager.cpp` has no rule event,
and the sole matched-by log line is `Window.cpp:2187 static_.workspace`. The claim holds on the checked channels;
it just has zero counted-row support, so the predicate would report `TARGET_MET` even if every sweep sentence
were deleted.

## Verdict

- Frontier item moved: **fails as written** — README `:102` still lists `rule *attribution*` as still open, the
  diff removes nothing, and the counter's indexed check never reads that bullet. The README contradicts itself.
- Re-scoring: **fails** — 10 of 23 PASS rows strictly restate prior lines and 11 more are generic non-attribution
  semantics; only 6 add attribution ground, three of them marginally.
- Attribution relevance / H1: **holds against the round** — 12 of 23 PASS rows are attribution-relevant (11 are
  not), and a generic-only note scores `TARGET_MET` (9/9, 6 sources), confirming H1 on the landed bytes.
- Predicate validity (secondary): the topic filter rejects three genuinely attribution-bearing rows (A5, A7, A8)
  and accepts eleven non-attribution rows.

`VERDICT: partial` — the note lands, is indexed and quotes re-fetch, and adds a real (if small) increment of
attribution ground; but the frontier surface it claims to move is untouched, the answer rests on uncounted
sweeps, and the counted target is met by generic rule semantics, as the round's own M24-2 already admits.

## Impacted axes

- **Coverage (C1)**: surface-move claim and its measurement. The target is met, the surface is not moved in the
  named artifact.
- **Registration / QUALITY (bookkeeping)**: README frontier bullet versus appended round-24 bullet; the
  `readme_indexed` clause measures a different surface than the claim names.
- **Provenance (predicate sensitivity)**: H1 confirmed on landed bytes; the round-24 lesson's H1 number (6, from
  the sandbox) understates the landed note (11 generic PASS rows).
- Not calibration (C2), not operability, no `tools/` contact.

## Smallest safe correction

1. README (inside the round's allowed repairs): change the round-12 frontier bullet `:102` from
   `Still open: rule *attribution*, ...` to a pointer — e.g. "rule *attribution* is documentary ground as of
   round 24 ([r24](knowledge/rule-attribution-r24.md)); observed attribution on this host, output management,
   ..." — so the Frontier section states one position. No predicate change.
2. Note intro: add one sentence that the counted rows establish documentary rule semantics and that the
   "no attribution channel" answer rests on the uncounted sweeps (`ScoutAttributionSweep`), not on PASS rows.
   This keeps the claim honest without touching frozen predicates or targets.
3. Lesson 24 M24-2: replace/annotate the sandbox figure with the landed partition (23 PASS = 12
   attribution-relevant + 11 generic; 10 strict restatements; 6 new attribution rows), so the next counter's
   rule-context term and sha256-per-document requirement are justified by measured numbers.
4. Next counter only (predicate is frozen this round): make the topic test identifier-aware
   (`PRIORITY_WINDOW_RULE`, `eRuleProperty`, `RULE_PROP_*`) so real attribution rows are not rejected lexically,
   and require a rule-context term rather than bare `rule`/`match`, per M24-2.
