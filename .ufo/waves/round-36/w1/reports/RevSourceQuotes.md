# RevSourceQuotes — reviewer report, mado round 36 wave 1

Seat: `L1Mado36.RevSourceQuotes`
Role: reviewer
Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Run date: 2026-10-25

## 1. Scout reports availability

I opened `LANE/.ufo/waves/round-36/w1/reports/` at run time. It contains **only**
`swarm-registry.json` (8,117 bytes). No `ScoutPriorArt` or `ScoutPriorArt2`
report file exists there, and no output from either scout exists anywhere under
the lane (find across all rounds for `*PriorArt*` / prior-art files returned only
the two prompt files; the round-36 `scratch/` tree is empty). The registry file
confirms the scouts' slots never acquired an agent:
`swarm-registry.json:135,141` (`"ScoutPriorArt"` and `"ScoutPriorArt2"` members)
both have `"agentId": null`.

Per the assignment ("If a report is absent when you run, say so and verify
whatever candidate you can open yourself"), I opened the two candidates myself
and verified quotes from them.

## 2. Sources opened (2026-10-25)

### ScoutPriorArt candidate — negative-controls methodology (primary literature)

- **Canonical URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/
  (PubMed Central, open access), DOI 10.1097/EDE.0b013e3181d61eeb,
  PMID 20335814.
- Source: Lipsitch M, Tchetgen Tchetgen E, Cohen T. "Negative Controls: A Tool
  for Detecting Confounding and Bias in Observational Studies." *Epidemiology*
  2010;21(3):383–388. Accessed 2026-10-25 (fetched HTML, sha256
  cf5a8eb3ae4ff67ec0fc33579b44136cae14a27985ce17cc4f091a707bda49b3).
- Text extracted from the PMC HTML (tag-stripped). Anchor: the section headed
  `Experimental biology: threats to causal inference and the use of negative
  controls` (article text line 90), body line 95.

The LWW pages (journals.lww.com) are Cloudflare-gated ("Just a moment...");
the PMC copy is the open-access version of the same article.

### ScoutPriorArt2 candidate — mutation testing / seeded-fault methodology (open access)

- **Canonical URL**: https://mutationtesting.uni.lu/survey.pdf
  (author-hosted preprint of the published chapter).
- Source: Papadakis M, Kintis M, Zhang J, Jia Y, Le Traon Y, Harman M.
  "Mutation Testing Advances: An Analysis and Survey." *Advances in Computers*
  112:275–378, 2019 (DOI 10.1016/bs.adcom.2018.03.015); the PDF opened is the
  2017-12-14 preprint ("Preprint submitted to Journal of LATEX Templates,
  December 14, 2017", survey.txt line 44). Accessed 2026-10-25 (fetched PDF,
  sha256 63b7bfca877cd4661cb24e93fbfe1757a2740b39fb65ee3a79eb17e36215f023).
- Text extracted with `pdftotext -layout`. Anchor: Section 1 "Introduction",
  page 1 (page marker at survey.txt:78), lines 30–32.

## 3. Verified quotes

### Q1 (ScoutPriorArt candidate — Lipsitch et al. 2010)

> "The second general approach is to perform negative controls: to repeat the
> experiment under conditions in which it is expected to produce a null result"

- **Contiguous substring**: verified programmatically; the full sentence
  occupies one line of the extracted text (lipsitch.txt:95) and the quote is a
  contiguous substring of it (`True`). Verbatim line:
  `The second general approach is to perform negative controls: to repeat the experiment under conditions in which it is expected to produce a null result and verify that it does indeed produce a null result. Several strategies are employed to design negative controls, 2 such as:`
- **≤25 words**: 25 whitespace-delimited tokens (python `len(s.split())`).
- **Supports the rule** (an instrument must be shown able to fail on a
  do-nothing or fabricated input): yes — the quote says negative controls
  require *repeating the experiment under conditions expected to produce a null
  result*; the next sentence of the same section makes the failure property
  explicit ("and verify that it does indeed produce a null result"). A control
  that produced a non-null result on a null-input experiment would mark the
  instrument as biased/uninformative. This is exactly the do-nothing-control
  logic of C1's kill rule (a degenerate instrument must not reach
  `TARGET_MET`).
- **What it licenses / what it does not**: it licenses requiring a demonstrable
  null result under null conditions for any instrument claim (the C1 `r35`
  do-nothing control before-score). It does not license treating a non-null
  negative-control finding as identifying the specific bias (the paper's eAppendix
  3 caveat: "the 'failure' of a negative control ... does not identify what form
  of bias is operating").

### Q2 (ScoutPriorArt2 candidate — Papadakis et al. 2019/2017 preprint)

> "Mutation analysis answers these questions by checking the ability of our tests
> to reveal some artificial defects"

- **Contiguous substring**: verified programmatically against the full
  normalized extracted text (`True`). The sentence straddles the PDF page-1
  line wrap, so in the raw `pdftotext -layout` output the quote appears as:
  `our test suite? Mutation analysis answers these questions by checking the ability` (line 31) `of our tests to reveal some artificial defects.` (line 32);
  the quote itself contains no page-break-adjacent tokens and reads as a
  contiguous sentence of the source (no footnote or running head intervenes
  between lines 31 and 32 in the layout output; the footnote marker `∗
  Corresponding author` comes *after* the quoted sentence).
- **≤25 words**: 17 tokens.
- **Supports the rule**: yes — mutation analysis is defined as checking the
  ability of tests to reveal *artificial defects* (seeded faults = fabricated
  inputs). Tests that fail to reveal them are judged not to be trusted ("we
  should not be confident on our testing and should improve our test suites",
  line 32-33). An instrument that cannot fail on a fabricated input is exactly
  what the rule forbids. This is the same kill-rule logic: a test suite that
  cannot fail on a mutant proves nothing about adequacy.
- **What it licenses / what it does not**: it licenses requiring a
  seeded-fault/fabricated-input case (a mutant fixture) to exist for any
  adequacy claim. It does not license equating mutant-kill counts with real-fault
  counts (the survey later discusses the relation between mutants and fault
  revelation as a distinct research question).

## 4. Verdicts

- ScoutPriorArt report: **ABSENT** (no file; `swarm-registry.json:135` has
  `agentId: null`). Candidate reopened by me; quote Q1 **verifies** (contiguous,
  25 words, supports the rule). Agree-with-scout verdict cannot be given — no
  scout claim exists.
- ScoutPriorArt2 report: **ABSENT** (no file; `swarm-registry.json:141` has
  `agentId: null`). Candidate reopened by me; quote Q2 **verifies** (contiguous,
  17 words, supports the rule). Agree-with-scout verdict cannot be given — no
  scout claim exists.

## 5. Method notes / blockers

- LWW Cloudflare gate blocked the publisher-URL copy of Lipsitch et al.; the
  PMC open-access copy was used instead (same article, PMID 20335814, DOI
  10.1097/EDE.0b013e3181d61eeb).
- The second candidate I attempted for ScoutPriorArt2's "oracle problem"
  preference — Barr, Harman, McMinn, Yoo et al., "The oracle problem in software
  testing" (UCL CREST preprint, https://crest.cs.ucl.ac.uk/fileadmin/crest/sebasepaper/BarrHMY14.pdf)
  — failed to download twice (`error: failed to redirect to /tmp/.../oracle.pdf: No such file or directory`),
  including from a background job. Per ScoutPriorArt2's own fallback clause
  ("If the best candidate is paywalled, say so and give the open-access
  alternative you actually opened"), I used the open-access mutation-testing
  preprint instead; the oracle survey could not be verified and is **not**
  cited.
- No tools were installed or upgraded this run (curl, python3, pdftotext all
  pre-existing).
- Verification commands (exact, quoted key output):
  - `python3` substring/word-count checks: `LIP-final: words=25 contiguous=True`,
    `SURV-final: words=17 contiguous=True`, `SURV-alt: words=18 contiguous=False`.
  - `pdftotext -layout survey.pdf survey.txt` → 5,750 lines; quote lines 30–32.
  - HTML text extraction of `lipsitch_pmc.html` → 208 lines; quote line 95,
    section heading line 90.
