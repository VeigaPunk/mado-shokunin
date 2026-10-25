# ScoutPriorArt — report, mado round 36 wave 1

Seat: `L1Mado36.ScoutPriorArt` (scout). Date: 2026-10-25.
Task: find and OPEN a primary external source grounding the round's core rule —
an instrument must be shown able to fail on a do-nothing or fabricated input —
and deliver one row (canonical URL, access date, exact anchor, ≤25-word quote at
that anchor).

## What I opened

- `https://pmc.ncbi.nlm.nih.gov/articles/PMC2833407/` — probed first by guess;
  it is a proteomics paper (Con A-induced hepatitis), NOT the negative-controls
  paper. Rejected; not cited further.
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/` — Lipsitch M, Tchetgen
  Tchetgen E, Cohen T, "Negative Controls: A Tool for Detecting Confounding and
  Bias in Observational Studies," *Epidemiology* 2010 May;21(3):383–388
  (author manuscript, NIHMS272869; PMID 20335814; DOI
  10.1097/EDE.0b013e3181d61eeb). Full article body read via the reader and via
  `curl` + `grep` against the raw HTML to pin element ids.
- Discovery command for the correct PMCID:
  `web_search("Lipsitch Tchetgen Tchetgen Cohen Negative Controls ... PMC full text")`
  which returned PMCID PMC3053408 (the earlier PMC2833407 guess was wrong by
  memory).

## Row (SOURCES.md 11-column shape)

| field | value |
|---|---|
| id | next free after S211 (registry tail checked 2026-10-25; S211 already names this paper — see note below) |
| source | Negative controls: a tool for detecting confounding and bias in observational studies — Lipsitch, Tchetgen Tchetgen, Cohen — https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/ |
| kind | paper |
| tier | A (primary methodological literature; peer-reviewed, DOI 10.1097/EDE.0b013e3181d61eeb) |
| scope | negative-control doctrine: run the procedure under conditions expected to produce a null result and verify the null; an apparent positive there is instrument/procedure failure, not evidence |
| anchor | section `#S1` "Experimental biology: threats to causal inference and the use of negative controls", paragraph `#P8` (first sentence, "The second general approach is to perform negative controls: …"); PMC3053408 author manuscript, Epidemiology 2010;21(3):383–388; opened 2026-10-25 |
| teaches | the negative control is a falsification run of the instrument itself: repeat under expected-null conditions and confirm null; licenses the r36 do-nothing control and kill rule (a TARGET_MET the do-nothing input could reach is invalid); says nothing about which specific controls a lane must pick |
| status | mined |
| opened | 2026-10-25 |
| recheck | on-release |
| used-by | candidate for `.ufo/waves/round-36/registration.md` claims C1/C2 kill-rule grounding and any round-36 lesson |

## Located quote (verbatim, 22 words ≤ 25)

Anchor: `#S1` §"Experimental biology: threats to causal inference and the use
of negative controls", paragraph `#P8`.

> "under conditions in which it is expected to produce a null result and verify that it does indeed produce a null result"

Word count verified: `len(quote.split())` → 22 (the full sentence including the
prefatory "…to perform negative controls:" is 26 words, over budget, so the
quote is the contiguous operative clause). Exact HTML at that anchor
(`curl -s …/PMC3053408/ | grep -n "second general approach"`, line 1448):

`<p id="P8">The second general approach is to perform negative controls: to repeat the experiment under conditions in which it is expected to produce a null result and verify that it does indeed produce a null result. …</p>`

## What it licenses and what it does not

Licenses: requiring that every admission instrument be run on an expected-null
(do-nothing or fabricated) input and *demonstrated* to return null/fail there —
i.e. the round-36 kill rule that a degenerate counter cannot reach `TARGET_MET`.
Does not license: any claim that passing negative controls makes an instrument
correct (the paper itself notes controls are "sensitive, but blunt" and only
*detect* bias), nor any particular choice of controls, nor software-domain
claims — it is epidemiology/experimental-method precedent, and the analogy to
code counters is the lane's own.

## Corroborating anchor (same source, second quote if integrator wants two)

- `#S2` §"Examples of the use of negative controls in epidemiology",
  paragraph `#P15` (Jackson et al. discussion): "the protective effect was
  observed even in circumstances where the vaccine could not have caused the
  protection" — 17 words; the "effect where cause is impossible = instrument
  failure" formulation. S211's existing row points loosely at "Introduction,
  the Jackson et al. example"; the Jackson material is actually in section
  `#S2`, not the introduction — anchor tightening recorded for whoever owns
  SOURCES.md.

## Overlap note

`corpus/SOURCES.md` row S211 (opened 2026-10-25, `mined`, used-by
`corpus/lessons/round-36.md`) already cites this same paper/URL but with a
loose anchor ("Introduction, the Jackson et al. negative-control-outcome
example") and no verbatim quote. This report supplies the tighter anchor and a
located quote; if admission is taken, update S211 in place rather than adding a
duplicate row.

## Verdict

PASS — primary source opened and read this round; row fields complete;
verbatim quote located at the stated anchor and within the 25-word bound.

## Tooling / installs

None. `read` (URL fetch) + `curl`/`grep`/`python3` already present; no pacman,
uv, npx, or cargo transactions were run.
