# RevSourceS211 — re-opening PMC3053408 and re-hashing its receipt

Seat: `L1Mado36.RevSourceS211`. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Date: 2026-10-25. Read-only on every production file; evidence under
`.ufo/waves/round-36/scratch/RevSourceS211/` (`fresh.html`, `fresh2.html`,
`fresh3.html`, `plain.txt`, `hashes.txt`).

Environment: `curl 8.23.0`, `python3 3.14.8` (stdlib only). **No install or update was
performed**; no pacman transaction was issued.

Extraction method (stated so the numbers below are reproducible): `<script|style|noscript>`
elements removed, remaining tags replaced by a space, HTML entities unescaped, all
whitespace collapsed to single spaces (`plain.txt`, 38,661 chars).

---

## 1. Quote (a) — verbatim, contiguous, ≤25 words

Command:

```
cd /tmp/revsrc211 && python3 - <<'EOF'
import re,html
raw=open('fresh.html',encoding='utf-8',errors='replace').read()
s=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>',' ',raw)
s=re.sub(r'(?s)<[^>]+>',' ',s); s=html.unescape(s)
s=re.sub(r'\s+',' ',s)
q="the protective effect was observed even in circumstances where the vaccine could not have caused the protection"
print("quoteA present:",q in s, "words:",len(q.split()))
EOF
```

Output:

```
quoteA present: True words: 17
```

Further, the sentence occurs **exactly once** in the article text
(`s.count(A) == 1`), so the anchor is unambiguous. Count check by hand: the / protective /
effect / was / observed / even / in / circumstances / where / the / vaccine / could / not /
have / caused / the / protection = 17 words, inside the 25-word bound.

Receipt block re-derived from the fresh fetch (tag-strip + normalise) is contiguous:

```
receipt block contiguous in fresh plain: True | words 79
receipt block startswith: 6 – 8 To test this hypothesis, Jackson et al 7 reproduced ea
```

**Verdict: CONFIRMED.** The quote is verbatim, contiguous after tag-stripping and
whitespace normalisation, 17 words, and the receipt's recorded extraction block is what the
live page still yields.

## 2. Quote (a) — location "the Introduction's Jackson et al. paragraph"

### 2a. The claim as landed

```
$ git show master:corpus/SOURCES.md | grep -n "S211" | cut -c1-400
213:| S211 | … | paper | A | … | Introduction, the Jackson et al. negative-control-outcome example; PMC3…
$ git show master:corpus/lessons/round-36.md | grep -n "Introduction"
74:Location: Introduction, the Jackson et al. negative-control-outcome example. It
```

### 2b. What the page actually says

Command (paragraph ids mapped to their enclosing `<section>` id and the nearest preceding
`<h2>`):

```
cd /tmp/revsrc211 && python3 - <<'EOF'
import re,html
raw=open('fresh.html',encoding='utf-8',errors='replace').read()
def norm(x): return re.sub(r'\s+',' ',html.unescape(re.sub(r'(?s)<[^>]+>',' ',x))).strip()
secs=[(m.start(), m.group(1)) for m in re.finditer(r'(?i)<section[^>]*\bid="([^"]+)"',raw)]
paras=[(m.start(), m.group(1)) for m in re.finditer(r'(?i)<p\b[^>]*\bid="(P\d+)"',raw)]
heads=[(m.start(), norm(m.group(1))) for m in re.finditer(r'(?i)<h2[^>]*>(.*?)</h2>',raw)]
q="the protective effect was observed even in circumstances where the vaccine could not have caused the protection"
astart=raw.find('id="abstract1"'); send=raw.find('id="S3"')
for o,pid in paras:
    if not (astart<o<send): continue
    cur=[s for s in secs if s[0]<o][-1][1]
    hd=[h for h in heads if h[0]<o][-1][1][:55]
    pt=norm(re.match(r'(?is)<p\b[^>]*>.*?</p>',raw[o:]).group(0))
    print(f"{pid:4} | section {cur:4} | heading {hd:57} | hasQ_A={q in pt}")
EOF
```

Output (abridged to the body rows that matter):

```
P13  | section S2   | heading Examples of the use of negative controls in epidemiolog | hasQ_A=False
P14  | section S2   | heading Examples of the use of negative controls in epidemiolog | hasQ_A=False
P15  | section S2   | heading Examples of the use of negative controls in epidemiolog | hasQ_A=True
P16  | section S2   | heading Examples of the use of negative controls in epidemiolog | hasQ_A=False
```

The document's `h2` sequence in reading order is: `Abstract`, `FIG 1.`,
`Experimental biology: threats to causal inference and the use of negative controls`,
`Examples of the use of negative controls in epidemiology`,
`Choice of negative controls to detect confounding in epidemiology`, …, `Discussion`.
There is **no `Introduction` heading anywhere in the article** (`grep -c Introduction`
on the raw HTML = 1, and that single hit is a *reference title*, "Introduction to
Regression Modeling"). Every one of the four `Jackson` mentions in the body is inside
`section id="S2"` (`P15`, `P15`, `P16`); the remaining hits are the reference list.

Command:

```
$ python3 -c "print('Introduction count:', len(__import__('re').findall(r'Introduction', open('/tmp/revsrc211/fresh.html').read())))"
Introduction count: 1   # sole hit: "Greenland S. Introduction to Regression Modeling", References
```

**Verdict: FALSIFIED.** The quote is real, but it is not in the Introduction. It is
`<p id="P15">` under `§"Examples of the use of negative controls in epidemiology"`
(`<section id="S2">`), twelve body paragraphs after the unheaded lead text.

### 2c. Current repair state (concurrent, uncommitted)

```
$ grep -n "S211" corpus/SOURCES.md   # working tree
213:| S211 | … | #S2 section Examples of the use of negative controls in epidemiology, paragraph #P15 (the Jackson et al. negative-control-outcome example); PMC3053408 author manuscript, …

$ git status --porcelain corpus/SOURCES.md corpus/lessons/round-36.md
 M corpus/SOURCES.md
 M corpus/lessons/round-36.md
```

So the registry row is **already corrected in the working tree** (and the corrected anchor
`#S2` / `#P15` matches the fresh fetch exactly, including heading capitalisation). The
lesson, however, was **not** repaired at the location sentence — `corpus/lessons/round-36.md:74`
still reads `Location: Introduction, the Jackson et al. negative-control-outcome example.`
— while the same lesson's appended repair block at `:315-325` says the cell "was corrected
in place" because the paragraph is in `§S2`, not the Introduction. The lesson therefore now
contradicts itself: `:74` still asserts the retracted location, and `:317` retracts it.

**Finding — MEDIUM (record accuracy, documentation-only):** `corpus/lessons/round-36.md:74`
carries a location that the same file's `## Gate — S211 anchor correction` block declares
wrong; the uncommitted `SOURCES.md` fix does not reach it. A re-opener following `:74`
lands in the Introduction and finds no Jackson paragraph.
Impact bound (verified, so the severity is not overstated): **no instrument consumes the
anchor cell** — `grep -rn "S211" quality/` = 0 hits, `grep -rn "Introduction" quality/*.py`
= 0 hits — so C1/C2 are unaffected. Fix: make `:74` read `#S2 §"Examples …", paragraph
#P15` (or strike the sentence and point at the Gate block).

## 3. Quote (b) — the Gate corroboration sentence at `#P8`, section `#S1`

Command:

```
cd /tmp/revsrc211 && python3 - <<'EOF'
import re,html
raw=open('fresh.html',encoding='utf-8',errors='replace').read()
p8=re.search(r'(?is)<p[^>]*id="P8"[^>]*>.*?</p>',raw)
t=re.sub(r'\s+',' ',html.unescape(re.sub(r'(?s)<[^>]+>',' ',p8.group(0)))).strip()
q="under conditions in which it is expected to produce a null result and verify that it does indeed produce a null result"
print("P8 words",len(t.split()),"quote in P8:",q in t)
print("P8 full:",t)
EOF
```

Output:

```
P8 words 46 quote in P8: True
P8 full: The second general approach is to perform negative controls: to repeat the experiment under conditions in which it is expected to produce a null result and verify that it does indeed produce a null result. Several strategies are employed to design negative controls, 2 such as:
```

Enclosing section, from the map in §2b: `<h2>` = `Experimental biology: threats to causal
inference and the use of negative controls`, `<section id="S1">`; the paragraph is
`<p id="P8">`. Word count of the quoted clause: under / conditions / in / which / it / is /
expected / to / produce / a / null / result / and / verify / that / it / does / indeed /
produce / a / null / result = **22**. Single occurrence in the article text
(`s.count(B) == 1`).

**Verdict: CONFIRMED.** Exactly the paragraph (`#P8`) and section (`#S1`) the lesson names,
contiguous, 22 words.

## 4. Receipt sha256 vs a fresh fetch

```
$ curl -sS -L --max-time 90 -A "Mozilla/5.0 (X11; Linux x86_64)" -o fresh.html \
    -w "http:%{http_code} bytes:%{size_download}\n" "https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/"
http:200 bytes:150283
$ sha256sum fresh.html
06a4f88dca7eaf4e383c831920ae13f45a2f6bd109d42cbacef1617e64f7060c  fresh.html
```

Receipt header: `fetched_sha256: 2c160aa0eb9d7fcd92906ceb34de66bcace8c5042ceed5737bcd8be3679f8bc8`,
`fetched_bytes: 150283`.

**Drift: yes — every fresh fetch differs, including from each other.**

```
$ for n in 2 3; do curl -sS -L --max-time 90 -A "Mozilla/5.0 (X11; Linux x86_64)" -o fresh$n.html "$URL"; done
$ sha256sum fresh.html fresh2.html fresh3.html
06a4f88dca7eaf4e383c831920ae13f45a2f6bd109d42cbacef1617e64f7060c  fresh.html
f05cb19f946f00ef4d5dde16d33775cfbfd549d3c5abd0c10d490f6a4d3c72ff  fresh2.html
3b51215b6ce22d7590261829782f9d91c3d41d25568c6ef99ff99dd4fb92c27f  fresh3.html
```

Three distinct hashes, **all 150,283 bytes** — the same size the receipt records.

Cause, isolated by diff:

```
$ diff <(tr '>' '\n' < fresh.html) <(tr '>' '\n' < fresh2.html)
107c107
< <meta name="ncbi_phid" content="96393EABADDB3803113EAB000C93311F.m_1" />
---
> <meta name="ncbi_phid" content="C1ED3D8EADDB1083113D8E00368448F5.m_1" />
3219c3219
<     <input type="hidden" name="csrfmiddlewaretoken" value="MMCMcKVAUJjslFB9qP24yusWK37wNDE97unID4oKfc4DLrHy9WeQLwSxoGlaLNpf" />
---
>     <input type="hidden" name="csrfmiddlewaretoken" value="AjJMQwgzrtSBfwkrMYeTS6SeaDE7hxxVGkqXNxoDM3NnvdPA5YWzZY18Xz294Rt0" />
```

Both rotating values are **fixed length** (phid 36 chars, csrf 64 chars on all three
fetches), which is exactly why the byte count is invariant at 150,283 while the hash is not.

**Does the drift change the quotes? No.**

```
plain texts identical across 3 fetches: True
fresh.html  plain sha256 75e35b4a4005ea73f457ee9b2c185887... len 38661
fresh2.html plain sha256 75e35b4a4005ea73f457ee9b2c185887... len 38661
fresh3.html plain sha256 75e35b4a4005ea73f457ee9b2c185887... len 38661
```

Token-normalised raw HTML is likewise stable across all three
(`47ff7d9ee240666f9970c928f6f7f912ae1387f8365417cdfdf6491af6f01210` for all three). No
normalisation I tried reproduces the receipt's recorded value:

```
raw                 06a4f88d…  match=False
tokens-emptied      fb677470…  match=False
crlf                589b15bd…  match=False
stripped            db23eacc…  match=False
plain-norm          75e35b4a…  match=False
plain-raw-strip     688943e6…  match=False
plain-collapse-strip 3b2f9bde… match=False
```

**Finding — LOW (receipt identity, instrument-plane):** `S211.receipt.txt`'s
`fetched_sha256` is a hash of per-request-mutated HTML, so it can never be re-verified — a
receipt whose digest is unfalsifiable is a receipt, not an identity. Content is provably
unchanged (byte count identical; plain text identical across three draws; both quotes
present and contiguous), so nothing in this round's claims turns on it. Suggested repair for
future fetch receipts, in this lane's own idiom: record the **extraction** digest
(`plain.txt` = `75e35b4a4005ea73f457ee9b2c1858872928823c9d5fe59c34da1151b2d14e98`) or the
token-normalised raw digest, next to the byte count — never the bare raw-HTML hash.

## 5. Receipt header identity claims

```
TITLE: Negative Controls: A Tool for Detecting Confounding and Bias in Observational Studies - PMC
PMCID in page: True
journal: Epidemiology (Cambridge, Mass.)
citation_volume : 21
citation_issue : 3
citation_firstpage : 383
citation_author : Marc Lipsitch
citation_author : Eric Tchetgen Tchetgen
citation_author : Ted Cohen
```

**Verdict: CONFIRMED** — title, `PMC3053408`, journal, `2010;21(3):383-…` and the three
authors all match the receipt header; `http: 200` matches; `fetched_bytes: 150283` matches
all four fetches.

## 6. Incidental number drift in the lesson

```
$ stat -c '%s %n' .ufo/waves/round-36/fetch/S211.receipt.txt
1037 .ufo/waves/round-36/fetch/S211.receipt.txt
$ git cat-file -s $(git rev-parse master:.ufo/waves/round-36/fetch/S211.receipt.txt)
1037
$ grep -n "1,033" corpus/lessons/round-36.md
68:receipt `.ufo/waves/round-36/fetch/S211.receipt.txt` (1,033 B; the fetched HTML's
```

**Finding — LOW (number drift, same class as M36-2):** the lesson states the receipt is
1,033 B; on disk and at `master` it is 1,037 B. The receipt is unmodified
(`git status --porcelain` shows only `SOURCES.md`, `lessons/round-36.md`,
`quality/check-evidence-pointers.py`), so the lesson's byte count was wrong when written,
not overtaken by an edit.

---

## Severity roll-up

| # | Finding | Severity | Evidence |
|---|---|---|---|
| 1 | `corpus/lessons/round-36.md:74` attributes the S211 quote to the Introduction; it is `§S2` / `<p id="P15">`, and the same lesson's `## Gate — S211 anchor correction` block (`:315-325`) says so. Working-tree `SOURCES.md` is fixed; the lesson is not. No instrument reads the anchor cell. | MEDIUM (record accuracy) | §2b, §2c |
| 2 | `S211.receipt.txt` records a raw-HTML sha256 that is unreproducible by construction (rotating `ncbi_phid` + `csrfmiddlewaretoken`); content drift is nil. | LOW (receipt identity) | §4 |
| 3 | Lesson says receipt is 1,033 B; actual and committed size is 1,037 B. | LOW (number drift) | §6 |

Confirmed items: quote (a) verbatim/contiguous/17 words; quote (b) contiguous at `#S1`/`#P8`,
22 words; receipt header identity (title, PMCID, journal, volume/issue/pages, authors, HTTP
200, 150,283 bytes); the receipt's 79-word extraction block still reproduces from the live
page.

## Residual risk and verification gaps

- The page is mutation-prone at the token level; content is identical across three draws
  taken within ~80 s. Longer-horizon content drift (PMC re-rendering, errata) is not
  excluded by this pass — only that today's rendering carries both quotes.
- Verified against the PMC HTML rendering only. The print/PDF rendering and the publisher
  copy (Epidemiology 21(3):383-388) were not opened, so section *labels* are PMC's anchors,
  not the journal's; `#S2`/`#P15` are correct for the article's machine anchor space and
  should be cited as such.
- Quote accuracy was checked against one extraction recipe. Other strippers (e.g. keeping
  `<figcaption>`) can shift offsets but cannot remove an occurrence; contiguity of the
  sentence itself was verified in the paragraph node, so the check is not recipe-dependent.
- Not in this seat's scope, left for other seats: whether `SOURCES.md`'s uncommitted fix is
  the one that lands, and whether `LOG.md`'s "five mistakes (M36-1…M36-5)" / "criteria
  57–60" match the lesson's six mistakes and criteria 57–61.
