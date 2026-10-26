# ScrQualityCriteria — QUALITY criteria 82+ draft (round 44, w1)

Behavior: drafted five new `corpus/QUALITY.md` criteria (82–86) from the routed round-43 closure defects, each with a
runnable checker that I built and ran in both directions; refused six of the nine §6 items with reasons. Nothing in the
lane was edited: the deliverable and its instruments live in this seat's directory, and `corpus/QUALITY.md` is untouched
for the L1 to integrate.

## Deliverable

- `.ufo/waves/round-44/w1/ScrQualityCriteria/criteria.md` — criteria 82–86 in the file's own style (rule, mistake class,
  `Check:`, `Shown able to fail:`, `(lesson: …)`), a Grounds table, the refusal section, and notes for the L1.
- Instruments beside it: `check82.py` … `check86.py`, `verify-quotes.py`, `run-checks.sh`, `receipts.txt` (180 lines:
  command, output and `exit=` for every run below; first block is the sha256 of each instrument).

| # | rule (one line) | mistake class | routed defect |
|---|---|---|---|
| 82 | a tool's verdict vocabulary is audited against the state fields the pinned producer's serializer carries; a field it never reads is declared ignored, and a field it consumes has a selftest case | state-space shortfall | D3 (prose half) + round-44 C1 |
| 83 | a citation resolves at the revision the citing document is judged at; a path added later is `LATE` | early citation | D4 |
| 84 | a round's axis verdict is read from a receipt committed at the closing revision whose bytes name it | untipped receipt | D7 |
| 85 | a registration's seat count is a plan; the executed count is the wave's results file, reconciled in one line | plan read as result | D5 |
| 86 | a locator's source is resolved from the repository (not only `fetch/`) and the range carries every code-shaped identifier the line names | range slop | D4, second sentence |

## Gates (all run; transcript `receipts.txt`)

| gate | red | green |
|---|---|---|
| `check82.py` (L1 source / L2 mention / L3 selftest case) | round-43 tool at `6a1a905`: `mention=0 declare=0 case=0`, `L2-unmentioned-undeclared`, exit 1; L3-only red on the reference with its 13 field cases removed; L1 red at `Hyprland-HyprCtl.cpp:400` | frozen reference `ctl-ref-tool.py.txt`: `mention=31 declare=0 case=10 ok`, exit 0; a declared-ignore copy passes L2 by declaration (the check audits, it does not prescribe) |
| `check83.py` | entry `hyprland-gkeep-geometry-r43.md` at data commit `1959770`: `LATE …/20-observation.txt (added 2a3707c after 1959770)`, `citations=3 violations=2`, exit 1 | the same document at tip `5846662`: `citations=6 violations=0`, exit 0 |
| `check84.py` | round-43 tip `5846662` and round-44 freeze `e2289516`: only `axis-base.txt`, `rev=` the base → `no receipt names the closing revision`, exit 1 | synthetic tip receipt: `verdict=PASS`; its `mismatched=1` twin: exit 1 |
| `check85.py` | round-43 `.ufo/waves/round-43/registration.md:5` + `w1-results.json`: `VIOLATION WAVE w1 plan=37 results_seats=38`, `VIOLATION TOTAL plan=69 results_rows=70`, exit 1 | round-44 registration (bound form, `bound=1`): `verdict=PASS`; synthetic `w1 38 / w2 32 / total 70` with 38+32 rows: `verdict=PASS` |
| `check86.py` | `20-observation.txt:24` as committed: `OUTSIDE gkeep-shm.c:156-164 ids_inside=0 ids_outside=app_id@34`, exit 1 | the same receipt with `150-159`: `ids_inside=app_id`, `verdict=PASS` |
| `verify-quotes.py` on my own draft | — | `VERIFY_QUOTES: verdict=PASS` (16 prose quotes, each located by a `file:line` on its own or the wrapped line, or by `receipts.txt` for quoted checker output) |
| criterion 69 vs 84 (informational) | lane-only invocation on the round-43 report returns `MISSING-REPORT`, exit 2 (the report is committed in the fleet repo at `906cfe70`); `--text` returns `FAIL 1/1 cited revisions lack a committed receipt`, exit 1 | — |

## Findings

1. **D4's citation is `LATE`, not `NOWHERE`** — the entry's oracle transcript entered the tree at `2a3707c`, after the
   data commit `1959770` that admitted the entry (`check83` rows above; `git cat-file -e 1959770:…/20-observation.txt`
   absent). The same defect class covers D7's log pointer: `tip-2a3707c-axis.log` is committed only from `5846662`, so a
   lesson that cites it as committed is right at the closure revision and wrong for the revision it describes.
2. **D7's proximate cause is a cross-repository check that returns setup error, not a verdict.** Criterion 69 already
   catches D7's token form when it is given the report's actual bytes (`FAIL 1/1`, exit 1) but returns
   `MISSING-REPORT`/exit 2 when invoked lane-only, because the report is committed in the fleet repo. An exit-2 is not a
   pass, and 84 exists so the axis reading can be checked in the lane alone.
3. **No round in 35–44 has a tip-named axis receipt.** 13 `MADO_AXIS` rows across those rounds, each `match=0` against
   the commit that carries it (the scan is in `receipts.txt`); `round-38`…`round-44` commit only `axis-base.txt`. Adopting
   84 is prospective and the LOG must say so (the same disclosure criterion 79 needed).
4. **Criterion 77 does not reach D4's second sentence.** The wrong locator `(gkeep-shm.c:156-164)` is not backticked and
   `gkeep-shm.c` is not in `fetch/`, so the locator gate never resolved it; `check86` resolves any committed lane file and
   reports `app_id` sitting at `34,58,116,118,150` (only `150` inside the true span).
5. **The frozen reference itself would fail 82 read as "every field"**: 15 scalar keys of the client block are
   unmentioned and undeclared (`AUDIT` line). The criterion is therefore scoped to the claim's subject (`--must`), which
   is what its command takes; the widening is left to a later round.
6. **Round 44's registration already fixes D5's form** (`bound=1`: counts are to be read from each wave's
   `*-results.json`), so 85's green case is this round's own freeze, not a synthetic one.

## Touched surfaces

- Written (new, untracked): `.ufo/waves/round-44/w1/ScrQualityCriteria/` (criteria.md, check82–86.py,
  verify-quotes.py, run-checks.sh, receipts.txt) and this report.
- Read only: `corpus/QUALITY.md`, `corpus/lessons/round-43-verifier-spotcheck.md`, `corpus/lessons/round-43.md`,
  `SKILL.md`, `.ufo/waves/round-44/{registration.md,receipts/,c1/,fetch-c1/}`,
  `.ufo/waves/round-43/{registration.md,receipts/,w1-results.json,w2-results.json,w1/ExecOracleGkeep/}`,
  `corpus/knowledge/hyprland-gkeep-geometry-r43.md`, `.ufo/waves/round-41/w1/ScrQualityCriteria/check69.py`,
  `.ufo/waves/round-41/…`, fleet-repo report `.ufo/reports/round-43/mado.md` at `906cfe70` (read-only input, copied to
  scratch and deleted).
- No tracked file edited; no mutating `git`/`jj`; no `pacman`; no compositor command; no tool installed; no lane counter
  or `quality/` gate executed (only the five new seat-local checkers and `check69.py` read-only).
- Scratch `/fast/scratch/hyaku/mado-r44/ScrQualityCriteria/` deleted at the end; every synthetic control is regenerated by
  `run-checks.sh`.

## Out of scope / refused (deliberate)

- Not integrated into `corpus/QUALITY.md`, `LOG.md`, or a lesson — the L1 is the only integrator; numbering assumes the
  file ends at 81.
- **D1** refused: already numbered (42, 77; M43-1/M43-7 record the repeats).
- **D2** refused: no mechanical observable; the registry's append-only supersession owns it.
- **D3** refused as a new number: assigned to 82's class applied to prose (`SKILL.md:276`), with M43-9 covering the
  inference half.
- **D6** refused: declared predicate weakness, bound by criteria 36/56; repair is re-registration.
- **D8** refused: driver duplicate, not a lane fact; criterion 81 already counts attempts from digest lines.
- **D9** refused: still-open round-41 items, not a round-43 mistake.

## Limits

- 82's block parser includes the nested `workspace` keys (`id`, `name`) and stops at `stableId`; 83 judges backticked
  tokens only; 85 reads a same-line `N seats` form (a table-shaped plan needs the pattern extended); 86 scores snake_case
  identifiers only, so `gkeep-shm.c:152-155` (no code-shaped identifier on its line) is unchecked.
- The five checkers are seat-local; if they should outlive the round they need a committed home under `quality/`, and the
  five `Check:` commands move with them.

Report: .ufo/waves/round-44/w1/ScrQualityCriteria.md

## Artifacts (sha256, seat dir `.ufo/waves/round-44/w1/ScrQualityCriteria/`)

```
bc373ca12eb2a8f9e658449623ed0d1be967e8889c500817751951d98bd60819  check82.py
2be1d523282861e83ac4310541624698d943cbeb8da8a99489dcfb8ad51ad7fb  check83.py
a18c4cb369e96a6935b77ba2a5262c68aae3e673ca755cbf28bf38a515c6903c  check84.py
04c1845748a2531721997bc4d3c7510a148be2bbafc9a966910df61172c2f07f  check85.py
514404f2b44fbcacd75fa7f0b55b9170c1826964837c5ea37e55ff0c168f1541  check86.py
85cc43ed8c49f76a1e3b35c95b538a39618b8d7a8c373af33cb4defcfa375560  verify-quotes.py
13e3dd187659cfbdc4942e6914d1950132088210476943fb9a2439e79ad1a6b6  criteria.md
3b2f48cf106dffab31abc92cf789ca71363f03e5596465fa6fb438bbe70ac104  receipts.txt
```
