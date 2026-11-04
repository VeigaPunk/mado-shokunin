# R73ScoutSources — fetch receipts for the three sources claim C2 cites

seat: R73ScoutSources (round 73, wave 1)
date: 2026-11-04 02:06 -03 (America/Sao_Paulo)
fetched with: `curl -sS -f --max-time 60` (no mirror substitution, no redirect to another host)
raw bodies: `.ufo/waves/round-73/w1/R73ScoutSources/fetch/<name>.<1|2|3>` (9 files, 3 per URL)
quote extracts: `.ufo/waves/round-73/w1/R73ScoutSources/fetch/quotes/q1.txt`, `q2.txt`, `q3.txt`, `q3-anchor.txt`

## Result in one line

Three URLs, three fetches each, all nine HTTP 200, each triple byte-identical (`cmp`),
and byte-identical to the round-73 working-tree `.ufo/waves/round-73/fetch/` bodies (untracked
at HEAD `1459cca11fb5d3956a6e9a128217852dd0c28cb9`). The three sentences C2 needs exist at the
cited places. One provenance defect found in an uncommitted working-tree registry row
(S448 digest, § Findings F2), and one scope mismatch against this seat's
brief (S449 cites `run`, not `Popen`, § Findings F3).

## Fetch integrity

| source | bytes | sha256 | 1v2 | 1v3 | distinct digests |
|---|---|---|---|---|---|
| `Doc/reference/simple_stmts.rst` | 41375 | `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc` | identical | identical | 1 |
| `Doc/library/os.rst` | 208655 | `2d0f2892676e1cf9547be2bd94cfe2a6221dddea82d52cb2475d4a3d819b2ae5` | identical | identical | 1 |
| `Doc/library/subprocess.rst` | 61603 | `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd` | identical | identical | 1 |

Cross-check against the round-73 working-tree bodies (read-only `cmp`, 9/9 identical; that
directory is untracked, `git ls-files` count 0):

```
.ufo/waves/round-73/fetch/Doc_reference_simple_stmts.rst.{1,2,3}  == fetch/simple_stmts.{1,2,3}
.ufo/waves/round-73/fetch/Doc_library_os.rst.{1,2,3}             == fetch/os.{1,2,3}
.ufo/waves/round-73/fetch/Doc_library_subprocess.rst.{1,2,3}     == fetch/subprocess.{1,2,3}
```

All three digests equal the values already recorded for these documents at S440
(`d4320642…`), S113 (`2d0f2892…`) and S108/S442 (`05cd782c…`).

## 1. `global` statement — simple_stmts.rst

- URL: https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst
- sha256 `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`, 41375 bytes, 3/3 identical.
- Section heading `The :keyword:`!global` statement` at lines 961-962; anchor `.. _global:` at 959.
- Sentence line range: **972-973** (first sentence of the section body).
- Quote, exact bytes (91 bytes, sha256 `f05d9ed482a6e37e60da46a6dac2e062fbeb5af236b0447be574511809fd55db`):

```
The :keyword:`global` statement causes the listed identifiers to be interpreted
as globals.
```

- Word count, `awk '{print NF}'` over the two lines: **12** (`paste -sd+` sum: 12).
- Rendered reading: "The global statement causes the listed identifiers to be interpreted as globals."
- Occurrences of this exact byte span in the file: **1**.
- Context (line 974-975, not part of the quote): the sentence continues the same paragraph —
  "It would be impossible to assign to a global variable without :keyword:`!global`…".

## 2. `os.environ` — os.rst

- URL: https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/os.rst
- sha256 `2d0f2892676e1cf9547be2bd94cfe2a6221dddea82d52cb2475d4a3d819b2ae5`, 208655 bytes, 3/3 identical.
- Directive `.. data:: environ` at line 184.
- Sentence line range: **186-187** (the sentence that describes `os.environ` as the environment mapping).
- Quote, exact bytes (104 bytes, sha256 `82a4ad9916a453c9320a67e17031015416a9a0a0e560602b660a557ed46dd6b3`):

```
   A :term:`mapping` object where keys and values are strings that represent
   the process environment.
```

- Word count, `awk '{print NF}'` over the two lines: **14** (sum: 14).
- Rendered reading: "A mapping object where keys and values are strings that represent the process environment."
- Occurrences of this exact byte span in the file: **1**.
- Adjacent clause that the working-tree row S448 actually quotes — lines **192-194** (sentence begins mid-line 192):
  `Changes to the environment made after this time are not reflected in :data:`os.environ`, except for changes made by modifying :data:`os.environ` directly.`
  (160 bytes, sha256 `ffe6ff2db3e72d91f6a817d3c1ab03b83feb530d0f530e27e60ea5516e2727f6`, 21 words raw and 21 words rendered, 1 occurrence.)

## 3. `env` parameter of `Popen` — subprocess.rst

- URL: https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst
- sha256 `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd`, 61603 bytes, 3/3 identical.
- Enclosing directive `.. class:: Popen(...)` at line 359; no intervening class/function directive between 359 and 648.
- Full sentence line range: **648-650** (sentence ends at "environment." inside line 650).
- Quote, exact bytes, 19 words (108 bytes, sha256 `9a7182645ecb41166c87a322f263295a6e863fb4fbc77f6636cb8c3b059b0c21`) — a leading exact substring of that sentence, cut at the semicolon to stay under the 25-word limit:

```
If *env* is not ``None``, it must be a mapping that defines the environment
   variables for the new process
```

- Word count, `awk '{print NF}'`: **19** (sum: 19).
- Rendered reading: "If env is not None, it must be a mapping that defines the environment variables for the new process"
- Occurrences of this exact byte span in the file: **2** — line 88-89 (`.. function:: run`, declared at line 38) and line 648-649 (`.. class:: Popen`). Verified `L88-89 == L648-649` byte-for-byte; the paragraphs diverge only at line 90 ("It is passed") vs line 650 ("This mapping can be").
- Popen-unique disambiguating anchor, lines **650-652**, 22 words, 1 occurrence in the file (142 bytes, sha256 `572fe0a47f34df4d503f98efeb33551fb8f074a1224d02a6b4832f0c82b877e0`):

```
This mapping can be
   str to str on any platform or bytes to bytes on POSIX platforms much like
   :data:`os.environ` or :data:`os.environb`.
```

## Findings

**F1 — all three URLs are already registered; no append is needed.** The claims declaration's
§ Sources plan says "up to three new rows opened this round"; the working-tree registry already
carries them (uncommitted: `git show HEAD:corpus/SOURCES.md` contains none of S447-S449), all
opened 2026-11-04 and all used by `corpus/knowledge/guard-carrier-global-environ-r73.md`:

| row | URL | anchor recorded | my check |
|---|---|---|---|
| S447 | simple_stmts.rst | `:972-973` | exact; quote exact (12 words raw, markup-stripped 12 words) |
| S448 | os.rst | `:184-196` | quote exact at `:192-194`, 21 words |
| S449 | subprocess.rst | `:88-90` (`run` *env* paragraph) | quote exact, 11 words, 2 occurrences (run + Popen) |

Earlier rows for the same documents: S440 (simple_stmts), S113 (os), S108 and S442 (subprocess).
A duplicate-URL check would therefore flag every one of the three URLs — correctly, because the
rows exist. This seat did not edit `corpus/SOURCES.md`.

**F2 — S448 records a digest that the bytes do not produce.** The row states
`sha256 2d0f2892676e1cf9f0d8e61c63a2e70a86f0e0a5cdb6b06dd7b7d2c9b8b88a4e, 208655 bytes`.
The bytes (three identical fetches, and the round-73 working-tree body) hash to
`2d0f2892676e1cf9547be2bd94cfe2a6221dddea82d52cb2475d4a3d819b2ae5` — the value S113 already
records for the same document. The recorded string shares only the first 16 hex characters with
the true digest and diverges after them. Tested transformations, none of which reproduce it:
raw, CRLF, CR, per-line trailing-whitespace strip, trailing-newline removal, UTF-8 BOM prefix,
UTF-8→latin-1 roundtrip. Byte count and quote are correct; only the digest is wrong. This is a
provenance defect in an uncommitted working-tree registry row, not in the source.

**F3 — scope mismatch on the subprocess anchor.** This seat was asked for the `env` parameter of
`Popen` (line 648-650); S449 scopes the `run` paragraph (line 88-90). Both paragraphs are the
same sentence bytes for their first two lines, and `run`'s paragraph says the mapping "is passed
directly to :class:`Popen`" (line 90-91), so S449's ground is not false — but a direct git launch
is a `Popen`/spawn call, and only the Popen paragraph carries the Popen-specific continuation
(lines 650-652). If the row is to anchor the `Popen` claim, `:648-650` (or the unique
`:650-652` anchor above) is the tighter reference.

**F4 — quote uniqueness.** q1 1×, q2 1×, q3 2× (run and Popen), Popen anchor 1×. The 2×
occurrence of q3 is the only ambiguity; the cited line range 648-649 plus the unique anchor
resolves it.

## Remaining unknowns / gaps

- No fetch failed and no mirror was substituted, so there is no fallback provenance gap.
- This receipt proves the documented sentences and the byte identity of the documents. It does
  not evaluate whether the C2 classifier implements the `global` / `os.environ` carriers
  correctly, nor whether the `global` line-order approximation (declared limit) is sound — those
  belong to the C2 instrument seats.
- The registry census's own treatment of the S448 digest (F2) was not run by this seat; the
  census was not executed and its verdict is not claimed here.

## Reproduction

```sh
D=.ufo/waves/round-73/w1/R73ScoutSources/fetch
for i in 1 2 3; do
  curl -sS -f -o "$D/simple_stmts.$i" https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst
  curl -sS -f -o "$D/os.$i"          https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/os.rst
  curl -sS -f -o "$D/subprocess.$i"  https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst
done
sha256sum "$D"/*.1
# the quote extracts shipped beside the bodies are the exact byte spans; count those
for q in q1 q2 q3 q3-anchor; do
  printf '%s words=' "$q"; awk '{print NF}' "$D/quotes/$q.txt" | awk '{s+=$1} END{print s}'
done
# and prove each extract is a literal substring of its body
python3 - "$D" <<'PY'
import sys
D=sys.argv[1]
for src,q in (("simple_stmts.1","q1"),("os.1","q2"),("subprocess.1","q3"),("subprocess.1","q3-anchor")):
    body=open(f"{D}/{src}","rb").read(); sub=open(f"{D}/quotes/{q}.txt","rb").read()
    print(q, src, "occurrences=", body.count(sub))
PY
```
