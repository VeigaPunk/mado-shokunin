# R86ScoutSources — re-grounding S491 and S492 at their committed bytes

Seat: `R86ScoutSources` (leaf scout, no dispatch). Owned file: this report only.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Freeze revision `237ecf4e69a4986108f719f3beeafe111adaa033`
("round-86: repair the frozen instruments pre-verdict and freeze the measurement", 2026-11-05 00:00:51 -0300).
Base revision `a722c60493f24f83429112e9123058835b2cdd82`.
Scratch: `/fast/scratch/hyaku/mado-r86/R86ScoutSources/` (created with `mkdir -p`, removed before yield).

Nothing under the lane was edited except this report. No instrument, control set, declaration,
registry row, lesson or knowledge entry was touched. No mutating git command was run; `git` was
used read-only (`log`, `ls-tree`, `show`, `cat-file`, `hash-object`, `status`, `rev-parse`).

---

## 1. Verdict summary

| # | question | verdict | confidence |
|---|---|---|---|
| S491 | does it pin a **MUST** (not a SHOULD) for duplicate member names? | **Yes — for I-JSON messages only.** RFC 7493 §2.3 is a normative `MUST NOT`, RFC 2119 boilerplate at lines 108–110. It is *not* a general-JSON MUST, and it reaches only **one** of the ten C1 refusal tokens. | high |
| S492 | does it pin **whole-string** match semantics as opposed to `search`? | **Yes — and it pins the `search` contrast twice** (the `search` directive at line 925 and the `search() vs. match()` comparison at lines 1702–1714). | high |
| — | are the committed bytes the upstream bytes? | **Yes.** Both endpoints re-fetched today (2026-11-05), HTTP 200, byte-identical (`cmp` clean) to the committed pins. | high |

Two findings below (F1, F2) are defects in *frozen lane prose*, not in the sources; they are
reported, not fixed. F3 is a grounding-precision finding about how the counter implements the
predicate S492 pins.

---

## 2. S491 — RFC 7493 (I-JSON) §2.3

### 2.1 Identity at the committed bytes

```
$ sha256sum .ufo/waves/round-86/fetch/S491.bin
a44ccf1451a7bf4f4bbb78b39e10ed0e9a27ff2ee5b639c6458042b5a7197062  .ufo/waves/round-86/fetch/S491.bin
$ wc -c .ufo/waves/round-86/fetch/S491.bin
12849 .ufo/waves/round-86/fetch/S491.bin
```

* Declaration (`claims-declaration-r86.md:125`) prints `a44ccf14…`, 12,849 B — **prefix and size match**.
* `corpus/lessons/round-86.md:76` prints the full digest `a44ccf1451a7bf4f4bbb78b39e10ed0e9a27ff2ee5b639c6458042b5a7197062`
  — **exact match**.
* `corpus/knowledge/refusal-records-clause-observations-r86.md:1` prints the same full digest — **exact match**.
* `corpus/SOURCES.md:443` (row S491) prints **no** digest — nothing to check there.

### 2.2 The quote, its line, and its byte offsets

Quote (11 whitespace-separated words; ≤ 25 as required):

> Objects in I-JSON messages MUST NOT have members with duplicate names.

It is **wrapped across two lines in the file**, so the sentence opens at line 159 and closes on
line 160:

```
$ sed -n '157,161p' .ufo/waves/round-86/fetch/S491.bin
2.3.  Object Constraints

   Objects in I-JSON messages MUST NOT have members with duplicate
   names.  In this context, "duplicate" means that the names, after
   processing any escaped characters, are identical sequences of Unicode
```

| locator | value |
|---|---|
| §2.3 heading | line **157**, byte offset **6335** (0-based) |
| **quote opens** | line **159**, byte offset **6361** (0-based) — quote text starts at **6364** (0-based) / **6365** (1-based) |
| quote's second line | line **160**, byte offset **6428** (0-based) |
| full sentence span (with the embedded newline + 3-space indent) | bytes **6364 … 6436** inclusive (73 B) |
| normative-keyword boilerplate | lines **108–110** (§1.2 Requirements Language → RFC 2119) |
| document status | `Standards Track`, `March 2015`, T. Bray, Ed. (lines 4–9); "This is an Internet Standards Track document." (line 22) |

**Locator check against the routed defect.** r85's routed defect R6 ("declaration source locators
off by one") is dispositioned in `corpus/lessons/round-86.md:50` as applied for r86: "S491/S492
locators are line numbers of the committed pins and are re-derived by the round's scout seat".
Re-derived independently here: **line 159 is correct** — the sentence *opens* at 159 and wraps to
160, exactly as `corpus/lessons/round-86.md:76` states ("the sentence opens line 159"), and the
§2.3 heading is at 157 as that row claims. The r86 locator fix holds.

### 2.3 Does it pin a MUST, not a SHOULD?

**Yes, and the contrast with the row the lane already held is real and in-format.**

* S491 §2.3 (line 159): `Objects in I-JSON messages MUST NOT have members with duplicate names.`
  — "MUST NOT", with RFC 2119 semantics fixed by §1.2 (lines 108–110).
* The lane's weaker row S486 (`corpus/SOURCES.md:438`) carries RFC 8259 §4:
  `The names within an object SHOULD be unique.` — verified in the lane's own r84 pin at
  `.ufo/waves/round-84/fetch/rfc8259.txt:322` (digest `61a5378f…cd2d7`, matching S486's row).
* So the SHOULD→MUST upgrade is genuine: *forbidden* under I-JSON, *tolerated-but-unpredictable*
  under plain JSON.

**Permission to refuse** is also in the same pin, at §3 Software Behavior (lines 180–186):
"receivers can avoid ambiguous semantics in the JSON messages they receive. This allows receivers
to reject or otherwise disregard messages that do not conform…" — that is the "may refuse" half
C1's duplicate-name refusal leans on.

### 2.4 Scope limits that must travel with the citation (observation, not a defect)

1. **The MUST binds I-JSON messages, not JSON.** RFC 7493 §1 defines "the unit of definition"
   as "the I-JSON message", a *restricted profile*. The lane's `--allocation` declaration is not
   established anywhere as an I-JSON surface — `grep -rn "application/[a-z+]*json\|+json"` over the
   lane's `*.md`/`*.py`/`*.sh` (excluding waves/lessons/knowledge) returns **nothing**, and no
   document in the lane claims the I-JSON profile for any surface. `corpus/lessons/round-86.md:81-85`
   states the flip honestly ("an I-JSON-mandated surface (`application/…+json` with the I-JSON
   profile) where the SHOULD becomes a MUST — S491 is exactly that"), but that surface is not
   implemented in the lane, so today S491 licenses a refusal *by analogy to a profile the lane does
   not adopt*, not by requirement. This is the same caveat r85's scout already raised
   (`.ufo/waves/round-85/w1/R85ScoutSources.md:198`), so it is a carried, known scope limit rather
   than a new defect.
2. **It reaches one of C1's ten refusal tokens, not the class.** I-JSON speaks to JSON *member
   names* in an object. C1's vocabulary (`quality/counters/c1-r86-refusal-records.py:41-52`) is ten
   tokens; four of them — `namespace-duplicate-bar`, `namespace-duplicate-surface`,
   `namespace-duplicate-cross-level`, `live-duplicate-surface` — are layer-shell **surface/level
   identity** defects that I-JSON does not mention at all. Only `alloc-duplicate-key` (2 of the 75
   control cases bind that cause; measured from `.ufo/waves/round-86/controls/c1-cases-r86.json`) is
   a JSON-member-name defect. The declaration's phrase "grounds C1's duplicate-identity refusal
   class" (`:122-124`) therefore overstates S491's reach over the *class*; the honest statement is
   that it grounds the *allocation-object* duplicate refusal, not the namespace/level ones.

Neither point changes either claim's instrument (neither counter reads S491 or S492 — verified:
`grep -n "S491\|S492\|7493\|SOURCES\|re\.rst" quality/counters/c1-r86-refusal-records.py
quality/counters/c2-r86-clause-observations.py` → no matches). They are citations about the
*meaning* of the rules, not inputs to the measurements.

---

## 3. S492 — CPython v3.14.8 `Doc/library/re.rst`

### 3.1 Identity at the committed bytes

```
$ sha256sum .ufo/waves/round-86/fetch/S492.bin
d252cc185dfc1014e1b4a8087b2515b71c76527f0f2f6dfddba9a880537e6a48  .ufo/waves/round-86/fetch/S492.bin
$ wc -c .ufo/waves/round-86/fetch/S492.bin
78262 .ufo/waves/round-86/fetch/S492.bin
```

* Declaration (`:128-129`) prints `d252cc18…`, 78,262 B — **prefix and size match**.
* `corpus/lessons/round-86.md:77` and the knowledge entry `:1` both print the full digest
  `d252cc185dfc1014e1b4a8087b2515b71c76527f0f2f6dfddba9a880537e6a48` — **exact match**.
* `corpus/SOURCES.md:444` (row S492) prints no digest.

### 3.2 The quote, its line, and its byte offsets

Quote (13 whitespace-separated words; ≤ 25 as required), as rendered in the lesson/knowledge
entries with the RST role markup stripped:

> If the whole *string* matches the regular expression *pattern*, return a corresponding Match.

In the file the sentence is **wrapped across two lines** and carries RST role markup:

```
$ sed -n '955,959p' .ufo/waves/round-86/fetch/S492.bin
.. function:: fullmatch(pattern, string, flags=0)

   If the whole *string* matches the regular expression *pattern*, return a
   corresponding :class:`~re.Match`.  Return ``None`` if the string does not match
   the pattern; note that this is different from a zero-length match.
```

| locator | value |
|---|---|
| `fullmatch` directive | line **955**, byte offset **39738** (0-based) |
| **quote opens** | line **957**, byte offset **39789** (0-based) — quote text starts at **39792** (0-based) / **39793** (1-based) |
| quote's second line | line **958**, byte offset **39865** (0-based) |
| quote block span (both lines, raw bytes with markup) | bytes **39792 … 39900** inclusive (109 B) |
| `search` directive (the contrast) | line **925** |
| `match` directive | line **937** |
| `search() vs. match()` comparison section | lines **1702–1714** (`.. _search-vs-match:` at 1702) |

**Locator check.** Line 957 is where the sentence opens and 955 is the `fullmatch` directive —
exactly what `corpus/lessons/round-86.md:77` claims ("**line 957** (the `fullmatch` directive at
line 955)"). The r86 locator fix holds here too.

### 3.3 Does it pin whole-string semantics rather than `search`?

**Yes, twice, in the same file.**

1. The `fullmatch` entry itself (955–958): "If the whole *string* matches the regular expression
   *pattern*, return a corresponding :class:`~re.Match`. Return ``None`` if the string does not
   match the pattern".
2. The comparison section (1709–1714) states the three-way distinction explicitly:

   > + :func:`re.match` checks for a match only at the beginning of the string
   > + :func:`re.search` checks for a match anywhere in the string
   > + :func:`re.fullmatch` checks for entire string to be a match

   and the `search` entry (925–931) says "Scan through *string* looking for the **first location**
   where the regular expression *pattern* produces a match" — i.e. `search` is explicitly *not*
   whole-string.

So the ground C2 needs — "a whole-line rule is `fullmatch` semantics, a substring/search rule is
not" — is present, unambiguous, and pinned. Note also that `re.match` is a **third** predicate
(prefix-anchored, line 937), so the file distinguishes all three; the counter's `regex-anchor-dropped`
mutant (search instead of whole-line) is exactly the `search`/`fullmatch` distinction this file draws.

---

## 4. Re-fetch: are the committed bytes the upstream bytes?

Both endpoints were re-fetched today from the URLs the lane prints (see F2 for where those URLs
live), and compared byte-for-byte with the committed pins:

```
$ cd /fast/scratch/hyaku/mado-r86/R86ScoutSources
$ curl -sS -L --max-time 50 -o refetch-S491.bin -w 'S491 http=%{http_code} size=%{size_download} url=%{url_effective}\n' \
    https://www.rfc-editor.org/rfc/rfc7493.txt
S491 http=200 size=12849 url=https://www.rfc-editor.org/rfc/rfc7493.txt
$ curl -sS -L --max-time 50 -o refetch-S492.rst -w 'S492 http=%{http_code} size=%{size_download} url=%{url_effective}\n' \
    https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/re.rst
S492 http=200 size=78262 url=https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/re.rst
$ sha256sum refetch-S491.bin refetch-S492.rst
a44ccf1451a7bf4f4bbb78b39e10ed0e9a27ff2ee5b639c6458042b5a7197062 refetch-S491.bin
d252cc185dfc1014e1b4a8087b2515b71c76527f0f2f6dfddba9a880537e6a48 refetch-S492.rst
$ cmp refetch-S491.bin .../round-86/fetch/S491.bin && echo "S491 IDENTICAL"
S491 IDENTICAL
$ cmp refetch-S492.rst .../round-86/fetch/S492.bin && echo "S492 IDENTICAL"
S492 IDENTICAL
```

**Both endpoints were reachable (HTTP 200); neither is `unreachable`.** The pins are
byte-identical to upstream as of 2026-11-05, and byte-identical to the blobs recorded at the
freeze and at the pre-freeze commit:

```
$ git ls-tree 237ecf4e .ufo/waves/round-86/fetch/
100644 blob 7630aa4b8f57c225237af77e6787d98443c4b1ee   .ufo/waves/round-86/fetch/S491.bin
100644 blob 456d74292ef4a7eef2f086d488b6d93a270ecae1   .ufo/waves/round-86/fetch/S492.bin
$ git hash-object .ufo/waves/round-86/fetch/S491.bin .ufo/waves/round-86/fetch/S492.bin
7630aa4b8f57c225237af77e6787d98443c4b1ee
456d74292ef4a7eef2f086d488b6d93a270ecae1
$ git ls-tree f72bba01 .ufo/waves/round-86/fetch/     # same two blobs
```

The worktree files are byte-equal to the freeze blobs (`git show 237ecf4e:<path> | cmp - <path>`
clean), so the pins that back these claims are the committed ones.

Fetch dates: file mtimes are `2026-11-04 22:31:03 / 22:31:04 -0300`; the pins were first
committed in `f72bba01` ("mado r86: preserve in-flight work at hyaku run-15 wrap-up",
2026-11-04 17:49:58 -0300) and carried unchanged into the freeze. The registry rows and the lesson
Gate block record access date `2026-11-04` — consistent.

---

## 5. Findings

### F1 — The lesson Gate block does not carry the byte offsets the declaration promises it does

`claims-declaration-r86.md:132` states:

> "The Gate block in `corpus/lessons/round-86.md` carries the access date, URL, **byte offsets** and
> ≤25-word quotes, plus at least one reject."

Measured on the frozen lesson:

```
$ grep -in "offset" corpus/lessons/round-86.md | head
(no output)
$ grep -in "byte" corpus/lessons/round-86.md | head
53:**M86-5 — inherited bytes are not inherited verdicts.** …
```

The Gate block carries the access date (2026-11-04), the URLs (lines 76–77), the sha256 digests,
the byte **sizes** (12,849 B / 78,262 B), the line numbers, and the quotes — but **no byte
offsets**, and no byte offset appears anywhere else in the lane for these two pins
(`grep -rin "offset" corpus/knowledge/refusal-records-clause-observations-r86.md` → none).

This is the same species of defect as r85's routed R6 ("declaration source locators were off by
one … Future declarations must cite the section numbers of the bytes actually opened"): a locator
promise the artifact does not keep. The offsets are supplied for the first time in §2.2 and §3.2
of this report. **Not fixed here** — `corpus/lessons/round-86.md` is L1's file.

### F2 — The declaration prints no URL for either source; the URLs live in the lesson Gate and the registry rows

My seat brief said "the URL of each source is printed in the declaration". It is not:

```
$ grep -c "http" .ufo/waves/round-86/claims-declaration-r86.md
0
```

The only URL-ish tokens in the declaration are the phrase "duplicate-URL warnings" (`:141`) and the
declaration's own reference to the Gate block (`:132`). The URLs are printed in
`corpus/lessons/round-86.md:76-77` and `corpus/SOURCES.md:443-444`:

* S491 — `https://www.rfc-editor.org/rfc/rfc7493.txt`
* S492 — `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/re.rst`

I re-fetched **exactly** these two URLs (no URL was invented), and both are the upstream endpoints
named in the registry rows. Reporting the location discrepancy so a reader does not hunt for a URL
in the declaration.

### F3 — The counter implements whole-**line** semantics by search+span, not `re.fullmatch`; the knowledge entry names the wrong function

`corpus/knowledge/refusal-records-clause-observations-r86.md:122` reads:

> "`re.fullmatch` is that predicate; `re.search` is not."

The counter does not call `re.fullmatch` on the anchor branch. It implements
`quality/counters/c2-r86-clause-observations.py:387-394`:

```python
def line_anchored(pattern, text):
    """True when the pattern matches one complete line of the output, never a prefix of one."""
    rx = re.compile(pattern)
    for line in text.splitlines():
        found = rx.search(line)
        if found is not None and found.group(0) == line:
            return True
    return False
```

i.e. `re.search` per line plus a span-equality test — a **whole-line** predicate over the output's
lines, not `re.fullmatch`'s whole-**string** predicate. Two measurable differences from
`re.fullmatch`:

```
$ python3 - <<'EOF'
import re
def line_anchored(pattern, text):
    rx = re.compile(pattern)
    for line in text.splitlines():
        f = rx.search(line)
        if f is not None and f.group(0) == line: return True
    return False
for pat, txt in [("[0-9]+","0"), ("[0-9]+","0 extra"), ("[0-9]+","-1"),
                 ("b|bc","bc"), ("[0-9]+","0\njunk")]:
    la = line_anchored(pat, txt); fm = re.fullmatch(pat, txt) is not None
    print(f"pat={pat!r:9} text={txt!r:12} line_anchored={la!s:5} re.fullmatch={fm!s:5} "
          f"{'DIVERGES' if la!=fm else ''}")
EOF
pat='[0-9]+'   text='0'        line_anchored=True  re.fullmatch=True
pat='[0-9]+'   text='0 extra'  line_anchored=False re.fullmatch=False
pat='[0-9]+'   text='-1'       line_anchored=False re.fullmatch=False
pat='b|bc'     text='bc'       line_anchored=False re.fullmatch=True   DIVERGES
pat='[0-9]+'   text='0\njunk'  line_anchored=True  re.fullmatch=False  DIVERGES
```

* Under alternation, `search` returns the leftmost-first alternative (`"b"`), whose span ≠ the
  line, so `line_anchored` refuses where `fullmatch` (which backtracks to `"bc"`) would accept.
* Over multi-line output, `line_anchored` accepts if **any** line matches whole, while
  `re.fullmatch` over the whole stdout fails.

**Impact on the claim: none measured.** Over the entire committed regex population
(`.ufo/waves/round-86/controls/c2-cases-r86.json`, all `kind == "regex"` cases, both samples and
negatives — 36 outputs) the two predicates agree exactly:

```
committed regex sample/negative outputs checked: 36  divergences line_anchored vs re.fullmatch: 0
```

The three `anchor: line` cases are `version` (`^…\.$`), `omarchy-version` (`^…$`) and
`border-size-int` (`[0-9]+`); their committed outputs are single-line and contain no alternation,
and the witness that distinguishes the rules — the negative `0 extra` — is refused by both
predicates and accepted by plain `re.search` (`re.search("[0-9]+", "0 extra")` matches), which is
precisely the discrimination the row needs. So C2's measured behaviour stands on S492's ground.

The finding is about **citation precision**: S492 pins `re.fullmatch`'s whole-*string* semantics;
the counter's rule is whole-*line* semantics implemented differently, and the knowledge entry names
`re.fullmatch` as "that predicate". A reader checking the code against the sentence would not find
`re.fullmatch` on that branch. The sentence that is literally true of the code is: "the whole-line
rule is `search` plus a whole-line span test — it accepts a line that *starts with* the value only
when the match spans the entire line; `re.search` alone is not it."

**Not fixed here** — the knowledge entry is L1's file, and the counter is frozen. Reported for the
record.

### F4 (bookkeeping, low) — the lesson's word counts for the two quotes are one higher than the text

`corpus/lessons/round-86.md:76-77` labels the S491 quote "(12 words)" and the S492 quote
"(14 words)". Whitespace tokenisation of the quoted strings gives 11 and 13 respectively
(`"Objects in I-JSON messages MUST NOT have members with duplicate names."` → 11; the S492 string
→ 13). The ≤25-word requirement holds either way, so nothing is out of bounds; the parenthetical
counts are simply off by one relative to plain whitespace counting. (r85's report
`R85ScoutSources.md:184` gives the same 12.) No action needed beyond noting it.

---

## 6. What I did not run, and what remains open

* I did **not** execute either counter (`c1-r86-refusal-records.py`, `c2-r86-clause-observations.py`).
  That is another seat's assignment; my seat is source re-grounding, and the instruments are frozen.
  Nothing in this report depends on a counter run.
* I did not re-derive the RFC 7493 §3 permission sentence's line range beyond reading it
  (lines 180–186); it is quoted in §2.3 above and is corroborated by r85's independent read.
* Open: whether the lane will ever adopt an I-JSON surface (the flip `corpus/lessons/round-86.md:84`
  names). Until then S491's MUST is a profile rule the lane borrows by analogy, not a requirement
  the lane satisfies. This is a lane-design decision, not a source defect, and it is already recorded
  in the lesson's Rejects block.
* Open (L1-owned, reported not fixed): F1 (missing byte offsets in the Gate block), F2 (URLs absent
  from the declaration), F3 (knowledge entry names `re.fullmatch` where the counter implements
  `search`+span over lines). F4 is cosmetic.
* The round-86 fetch directory holds only the two `.bin` pins — unlike `.ufo/waves/round-84/fetch/`
  and `.ufo/waves/round-85/fetch/`, it carries no `source-pins-r86.json` manifest recording the
  fetch attempts (URL, http status, per-fetch digests, byte offsets). r85's manifest is exactly the
  place where the "unreachable endpoint recorded as unreachable" discipline lives. Both endpoints
  were reachable today, so nothing is lost factually, but the r86 fetch directory does not follow
  the lane's own provenance convention.

---

## 7. Commands run (read-only, plus scratch)

```
sha256sum / wc -c  .ufo/waves/round-86/fetch/S491.bin .ufo/waves/round-86/fetch/S492.bin
sed -n '157,161p' / '955,959p' / '925,945p' / '1702,1714p'  (the two pins)
grep -n "MUST NOT have members" / "If the whole \*string\* matches" / "function:: fullmatch" / "function:: search"
python3 (byte offsets, word counts, line-anchored vs re.fullmatch over the c2 control set)
curl -sS -L --max-time 50 -o refetch-* <the two printed URLs>; sha256sum; cmp
git -C <lane> log / ls-tree / show / cat-file / hash-object / status --porcelain   (read-only)
grep -rn "S491|S492|7493|SOURCES|re\.rst" quality/counters/c1-r86-refusal-records.py quality/counters/c2-r86-clause-observations.py
grep -rn "application/[a-z+]*json|+json" over the lane's *.md/*.py/*.sh
```

Scratch (`/fast/scratch/hyaku/mado-r86/R86ScoutSources/`, containing the two re-fetched copies) was
removed before this report was written. No file outside this report was written in the lane.
