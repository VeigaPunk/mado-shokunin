# Seat ExecDoNothingV2 — do-nothing controls against PRED-C2-r43-v2 (round 43, w2)

**Assignment.** Build cheap controls that skip the claimed work but keep the shape, score them under
`PRED-C2-r43-v2` at the data commit, and say for each admitted one whether the landed entry's actual prose is
distinguishable from it by any mechanical rule. Lane `mado-shokunin`, data commit
`1959770657f1f8665097c1aed4be6c1cbb07139f` (base `a35cfdf…`), judged revision for every number below.

**Identity.** Counter `quality/counters/c2-r43-gkeep-entry-v2.py` sha256
`9a83407062d165661d211a714ce06b381391c7c4574c91c71eb54689dde1d028`; v2 controls runner
`.ufo/waves/round-43/ctl/run-c2-controls-v2.py` sha256
`30ccdf571b291510391d1aa1a222b284cfb130610774556a6fc12c69897224bd` (helpers imported by `importlib`,
`main()` never called); CPython 3.14.8; no tool was installed this seat. No tracked file was edited; nothing was
written outside this seat directory; no pacman, no compositor verb, no input injection.

## Verdict

**21 fixture repos scored: 16 admitted, 5 rejected, every one as designed (`unexpected=-`).**
14 are cheap do-nothing controls that keep the landed shape; all 14 are `admitted=1/1`. The landed entry
transcribed verbatim (L0) and the runner's registered control P are also `1/1`, so the fixture harness is
faithful; the 5 rejected fixtures (D06, the literal ten-quote file, and four shape-breakers built to confirm the
clauses bite) die on the clause designed for them, so the harness is not blind.

The claim under attack is the v2 residual, and it is confirmed at the data commit: **C2 certifies quotation
bookkeeping, not coverage.** The landed entry's own prose is not distinguishable from **four** admitted
do-nothing controls by any of the thirteen cheap mechanical rules I measured (D11, D12, D13, D15); two of those
(D11, D12) have an entry **byte-identical** to the landed one. Every other admitted control is separated from
the landed entry only by rules that also **reject the registered control P** (D02, D03, D04, D07), or by a
single-token marker whose addition is the second control (D01/D09/D10 vs D02).

## Method

`harness.py` transcribes the landed entry into a committed-shape fixture from the data commit's own bytes
(`git show 1959770:<path>` for the entry, `corpus/SOURCES.md` rows, the lesson's ten `GATE` lines, the real
`ADMIT`/`REFUSE` lines, the README index row, the ten pinned receipts from `fetch/`), with the two HELD ids
(S155, S158) carried in the **base** registry exactly as the lane carries them. Fixtures are
`git init`-ed under `/fast/scratch/hyaku/mado-r43/ExecDoNothingV2`, every git call names `-C "$D"`, the
toplevel is asserted equal to `$D` before the first commit, and each fixture is removed after scoring. The
counter is read, never edited.

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w2/ExecDoNothingV2
TMPDIR=/fast/scratch/hyaku/mado-r43/ExecDoNothingV2 python3 harness.py     # ~5 min, 21 fixtures
python3 entries.py                                                        # rule matrices, no scoring
```
`harness.py` sets `TMPDIR` itself; `entries.py` dumps each fixture's entry text and evaluates the rule matrices.
`harness.py`'s `alt_quote` was re-run after the fact and reproduces all ten rows of `d15-swaps.txt` exactly, so
the D15 entry can be rebuilt from the landed entry plus that table (which `entries.py` does).

## Controls (all `admitted=1/1` unless stated)

| # | control | what it skips | observed clauses |
|---|---|---|---|
| L0 | landed verbatim | — (reference: the transcription admits) | a–i all 1 |
| P | registered control P (runner's `admitted()`) | — (reference) | a–i all 1 |
| D01 | quotes-only wallpaper: neutral header, the ten correct quotes, the three census lines | every claim about gkeep | a–i all 1 |
| D02 | same, with `**OBS**` markers and the landed `source:` descriptions | every claim **outside** the unbound header descriptions | a–i all 1 |
| D03 | landed with all claim prose replaced by wallpaper prose (quotes and census intact) | the entire argument | a–i all 1 |
| D04 | landed with every `**INF**`/`**UNK**` line and UNK table row deleted | the whole licensing argument | a–i all 1 |
| D05 | landed with every claim negated (`False: …`, `… does not hold`, opposite closing section), quotes intact | the argument's direction | a–i all 1 |
| D06 | the ten quotes **literally only** (no header, no census) | shape itself | **b,c,d,e,g,h,i = 0** → rejected |
| D07 | decision table that contradicts the census ("gkeep open now: yes, 420x500", "host has no gkeep rule") | the census reading | a–i all 1 |
| D08 | landed + verdict section asserting the opposite conclusion | the conclusion | a–i all 1 |
| D09 | D01 with the ten quotes in reverse order | ordering of the argument | a–i all 1 |
| D10 | D01 + a cited oracle run recorded at a path that does not exist | that the evidence exists | a–i all 1 |
| D11 | landed, with the lesson `REFUSE` reason = `superseded zebra ladder quokka` | the assimilation reading | a–i all 1 |
| D12 | landed, registry `teaches` cell of the eight new rows = "nothing here teaches anything about window sizes or geometry" | the registry's own claim | a–i all 1 |
| D13 | landed, `source:` descriptions misdescribe their receipt ("the wallpaper daemon's config file") | the header's provenance prose | a–i all 1 |
| D14 | landed + "The census lines above were not taken on this host; they are illustrative" | the census's standing | a–i all 1 |
| D15 | landed with **all ten quotes swapped for other genuine quotes** of the same ten receipts (prose untouched) | the reading of the sources | a–i all 1 |
| R01 | D01 with the S158 link dropped (nine pins) | — | **i = 0** → rejected |
| R02 | D01 without the three census lines | — | **h = 0** → rejected |
| R03 | D01 + `**INF** S290 also proves the wallpaper is unrelated.` | — | **g = 0** → rejected |
| R04 | D01 + `See https://amgsk.dev/posts/hyprland-rules/ …` | — | **i = 0** → rejected |

`D06` is the shape break the task's own phrasing invites ("a wallpaper entry made of the ten quotes only"): the
literal ten-quote file cannot satisfy clause `b` (four `source:` lines in the first 20 raw lines, one
`verified-at:`, one `recheck:`), `h`, `g` or `i`. Adding exactly the header and three census lines is `D01`,
which is admitted. The distance between the rejected and the admitted wallpaper is one header block and three
lines the counter itself recomputes.

## Is the landed prose distinguishable from each admitted control?

Thirteen cheap rules were measured on every fixture's entry text (`rules-matrix.txt`,
`rules-matrix-extended.txt`, `distinguish.txt`): M1 `**INF**` line, M2 `**UNK**` line, M3 license table,
M4 `ground:` line, M5 table row with UNK, M6 ≥120 prose words outside id lines, M7 ≥5 `## §` headings,
M8 prose mentions 420; E1 `**OBS**` marker, E2 quote-line order = source-line order (source lines excluded —
a first implementation that did not exclude them was vacuous and was fixed before the numbers below), E3 ≥1 prose line inside a `## §`
section, E4 `FullMatch` outside a quote line, E5 any negation marker ("False:", "does not hold", "nothing else",
"not taken on this host").

| control | rules separating it from landed | of those, rules the registered control P also satisfies | entry identical to landed |
|---|---|---|---|
| D01 | M1–M8, E1, E3, E4 | **E1 only** | no |
| D09 | M1–M8, E1, E2, E3, E4 | **E1, E2** | no |
| D10 | M1–M8, E1, E4 | **E1 only** | no |
| D02 | M1–M8, E3 | **none** | no |
| D03 | M2, M8 | none | no |
| D04 | M1, M2, M5, M6, M8 | none | no |
| D05 / D08 / D14 | E5 | E5 | no |
| D07 | M5 | none | no |
| **D11** | **none** | — | **yes** |
| **D12** | **none** | — | **yes** |
| **D13** | **none** | — | no (1 line added, 10 rewritten) |
| **D15** | **none** | — | no (10 quote lines rewritten) |

Answers, case by case:

- **D11, D12 — no mechanical rule can distinguish them.** Their entry bytes are the landed entry's bytes
  (`distance.txt`: `identical_to_landed yes`); the do-nothing edit lives in the lesson and in the registry, and
  every clause that reads those files scores only shape (a flip word plus four words; `mined`, `opened`,
  `used-by`, `recheck`). A rule that separated them would have to read the REFUSE reason or the `teaches` cell
  for meaning.
- **D13, D15 — no rule among the thirteen separates them, and none of the cheap ones could be made to without
  reading.** D15 keeps every sentence of the argument and swaps only which genuine line is quoted. The result is
  self-contradictory prose — "the class test is anchored on the whole string" now sits beside
  `CRegexMatchEngine::CRegexMatchEngine(const std::string& regex) {` (RegexMatchEngine.cpp:6) — and the quotes
  stand 10, 410, 210, 140, 353, 38, **1917**, 23 and 48 lines away from the claim they are offered for
  (`d15-swaps.txt`, reproduced from the run log by `alt_quote` in this seat's harness). This is the declared
  residual ("a real receipt can be cited for a claim it does not support, at a true locator, with a word-bounded
  quote") demonstrated on the entry's **real prose**, not on a synthetic wallpaper.
- **D02, D03, D04, D07 — distinguishable only by rules that reject control P.** The separating rules are exactly
  the claim-vocabulary ones (`**INF**`/`**UNK**` lines, the license table, its UNK row, prose volume). The
  registered control P has none of them (`P-registered M=00000000`), so any of those rules converts P from
  `admitted=1/1` to `admitted=0/1` — that is a re-registration decision, not a falsification, and registration.md
  forbids re-registration after data.
- **D01, D09, D10 — distinguishable by E1 (the `**OBS**` marker), which is P-safe, and evaded by adding the
  token.** D02 is exactly that evasion and becomes indistinguishable under all P-safe rules. D09 adds E2 (quote
  order = source order), also P-safe, and also free to evade: a do-nothing entry that keeps the source order is
  D01.
- **D05, D08, D14 — distinguishable only by E5, a negation vocabulary, and trivially reworded.** E5 is P-safe
  because the landed entry and P share the vocabulary; a do-nothing entry stating the opposite conclusion in its
  own words carries no marker (D15's `E5=0`).

**The general shape of the answer.** Any control that is the landed entry plus or minus prose is admitted, so a
rule can only separate it by objecting to *what the prose says*; the only cheap proxies for that are vocabulary
lists, which the author of the do-nothing entry controls. The rules that would actually bite — a fixed-form
conclusion line bound to the census values, "≥1 `**INF**` per `**OBS**`", "the quoted line must be the one the
sentence is about" — either reject the registered control P (first two) or are the non-author closure's reading
(the third). None can be added now without a re-registration, which registration.md:72 forecloses.

## Findings, ranked

1. **F1 (widest, confirms the declared residual).** A 31-line wallpaper (D01: header + the ten correct quotes +
   the three census lines) is `admitted=1/1`; so is the same with the landed source descriptions (D02), and so is
   the landed entry with every claim deleted (D04) or replaced by wallpaper prose (D03). The `w1` statement this
   confirms under v2 at the data commit is `CritC2Cheat/findings.md` finding 1 ("control P is itself a wallpaper
   entry") — and this seat shows the landed entry shares the property, not only the synthetic P.
   `CritClaimSizing` F2 ("a 17-line entry citing three own-work receipts and one upstream file is admitted") is
   **closed** by v2's clause i+: all ten pins must be cited, which R01 demonstrates by failing only on `i` when
   the S158 link is dropped.
2. **F2 (claim binding, at scale).** D15: all ten quotes replaced by other genuine unique non-comment lines of the
   same receipts, up to 1917 lines away, prose untouched, `admitted=1/1` with `clauses=a:1 … i:1`. The declared
   residual is therefore not an edge case of the counter's grammar; it is the only thing standing between a
   written entry and an admitted one.
3. **F3 (contradiction is uncosted).** D07 (decision table asserting `gkeep` present at 420x500 and no host rule,
   next to census lines the counter computes as `total=4 floating=0 gkeep=0` and `size=420x500`), D08 (opposite
   verdict appended) and D14 ("the census was not taken") are all admitted. Clause `h` recomputes the census
   from the receipts but never binds the entry's prose to it. (Same root as `CritC2Cheat` A2 for v1; still holds.)
4. **F4 (evidence pointers are unbound).** D10: an oracle run "recorded at
   `.ufo/waves/round-43/w2/ExecDoNothingV2/oracle-absent.txt`" — a file that does not exist — is admitted because
   it names no cited id. Only lines naming a cited id are bound (clause `g`+).
5. **F5 (assimilation is vocabulary).** D11: `REFUSE … reason=superseded zebra ladder quokka` is admitted; `i`+
   needs four distinct words and a flip word, which is what it got. (v1 equivalent closed as `CritC2Cheat` F2.)
6. **F6 (registry and header prose unbound).** D12: all eight new rows may say their receipt teaches "nothing
   about window sizes or geometry"; D13: `source:` descriptions may misdescribe their receipt. Both admitted.
7. **F7 (positive: what v2 does enforce).** The four shape-breakers die on exactly their clause — `b` (D06),
   `h` (R02), `g` (R03), `i` (R04) — and R01 shows the ten-pin clause is what enforces the chain: with nine pins
   every other clause passes (`a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:0`). Coverage is enforced as *citation
   presence*, which is exactly what a wallpaper supplies.

## Reproduction caveat (fixture grammar, reported not judged)

Two of the first three harness runs rejected **every** fixture at clause `c`. Cause: the fixture carried the two
held ids (S155, S158) as new rows, whose lane `opened` dates are not `2026-10-26`; clause `c` tests `opened` only
for ids absent from the base registry. Carrying the lane's **BASE** rows for S155/S158 in the fixture's base
commit — where the lane also carries them — fixes it, and all 21 fixtures then behave. Not a counter defect; a
fixture-grammar fact worth writing down: an entry citing a held id can only be scored by a fixture whose base
registry already holds it.

## Evidence inventory (relative to the lane root)

| receipt | what it holds |
|---|---|
| `.ufo/waves/round-43/w2/ExecDoNothingV2/harness.py` | the 21 fixtures, their builders, the scorer |
| `…/summary.txt` | every control's expected/observed/clauses/rc, `CTL_DONOTHING: fixtures=21 admitted=16 rejected=5` |
| `…/runs/*.txt` (21) | the frozen counter's full stdout per fixture (clause lines, `admitted=`, rev) |
| `…/entries/*.md` (21) | the entry text of each fixture (D15's reconstructed from `d15-swaps.txt` and checked against the run's clause-`g` locators) |
| `…/rules-matrix.txt`, `…/rules-matrix-extended.txt` | the M-rule and E-rule matrices |
| `…/distinguish.txt` | the per-control separating-rules / P-safety table quoted above |
| `…/distance.txt` | line delta vs the landed entry; `identical_to_landed yes` for D11 and D12 |
| `…/d15-swaps.txt` | the ten swap rows (id, receipt, original line, chosen line, distance, quote) |
| `…/run-harness.log` | the run's own stdout, including the swap table `d15-swaps.txt` was recovered from |
| `…/entries.py` | the no-scoring script that produced the two matrices and `distance.txt` |

## Notes for the integrator

- The tip is now `8750016` ("round-43: w2 corrections …"), which rewrites two of the landed entry's prose
  clauses (S290's `negative:` prefix sentence, S297's window class/line) and leaves all ten quotes and their
  locators unchanged. Everything above was scored at the data commit `1959770` as assigned; the controls are
  transformations of the entry text and do not depend on those two clauses, so they transfer unchanged.
- Scratch `/fast/scratch/hyaku/mado-r43/ExecDoNothingV2` is deleted at seat close; the only artefacts kept are
  the seat files above. Frozen artefacts (`quality/counters/`, `.ufo/waves/round-43/ctl/`, `fetch/`,
  `registration*.md`, `corpus/SOURCES.md`) were confirmed unmodified at seat close (`git status --porcelain` on
  those paths is empty).
- Nothing here is a re-registration proposal: F1–F6 are open defects of `PRED-C2-r43-v2` to be recorded, and the
  mechanical rules that would close them are named with their P-safety so the next round can decide.
