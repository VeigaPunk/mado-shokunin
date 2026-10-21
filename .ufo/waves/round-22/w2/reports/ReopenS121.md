# Reopen S121 — tagged CPython v3.14.8 executionmodel.rst

Seat: `ReopenS121` (scout, leaf — no dispatch). Date: 2026-10-21.
Authority: author-lane source verification only. This report cannot grant admission, retire the r19/r20/r21 red receipts or streak, or certify any instrument.

## Reopen action (only the assigned source)

- URL reopened: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst`
- One GET via `curl 8.23.0 -sS -fL`; HTTP **200**, no redirect, `text/plain; charset=utf-8`.
- `access_utc` 2026-10-21T15:37:59Z; server `date` header `Wed, 21 Oct 2026 15:37:59 GMT`.
- Bytes **24445** (`content-length` matches body); ETag `"e8fc9ff60a7eb0022c96e7d9591c769a703112860e0ab2e06012f4d7b6f4e922"`; 591 lines, LF only, no CR/NUL.
- Fresh body SHA-256: `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89`.
- Byte-identical to the retained raw `w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-executionmodel.rst` (`cmp` exit 0); matches the S121 row digest and the retained `receipts.jsonl` body claim.
- Tag identity re-derived independently with `git ls-remote` (exit 0): `refs/tags/v3.14.8` tag object `992560c2cc62d47b308cec662feb485456847931`, peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12`. Output SHA-256 `6549cb7c…d0ac` is identical to the retained `git-ls-remote-v3.14.8.txt`, so the row's peel claim reproduces.
- No second URL fetched: the peeled-commit-URL cross-check remains the retained W1 receipt's, not re-run here.

No source-registry edit, no tool/gate edit, no scanner or gate run, no fixture code executed.

## Verification results

| item | observed | verdict |
|---|---|---|
| Row anchor file path | `Doc/reference/executionmodel.rst` at tag v3.14.8 | agrees |
| Row tag/peel | tag object `992560c2` → commit `8e6e75d9` | agrees (fresh `git ls-remote`) |
| Row digest | `11f99f83d785ac1…a2eb89` | agrees, fresh body identical |
| Row cited range `89-114` | 89–93 free-variable definition; 105–109 scope extension into contained blocks; 113–114 nearest-enclosing sentence complete | agrees |
| Row cited range `322-329` | 322 runtime sentence; 323–329 canonical `i = 10 / def f(): print(i) / i = 42 / f()` example documented to print 42 | agrees |
| Lesson quote location `:322` | exact line 322, unique occurrence in file | agrees |
| Lesson quote word count `12` | 73 chars, `len(quote.split()) == 12`, ≤25 | agrees |
| Lesson "enclosing-scope rule at 113–114" | sentence complete at 113–114 (17 words) | agrees |
| S120 duplicate-URL warning | S120 cites same file/digest at 240–256; disjoint from S121's 89–114/322–329 | agrees (duplicate URL is real, lines disjoint) |

Exact quote, verified byte-for-byte against the reopened body:

> `Name resolution of free variables occurs at runtime, not at compile time.`
> Doc/reference/executionmodel.rst:322 · 73 chars · 12 whitespace words · SHA-256 `7b11083b248bde8963cd48c4ba433dd9ed07b6e7e233f8467cb5b0aec449d383` (without newline)

Section placement: heading `Interaction with dynamic features` (lines 319–320, `-` underline), a subsection of `Naming and binding` (line 39, `=` underline), inside top-level `Execution model` (line 5, `*` underline); the next section is `Exceptions` (line 346, `=` underline). The quoted line is ordinary paragraph text, not a directive or literal block.

Nearest-enclosing scope, verified: line 113 `When a name is used in a code block, it is resolved using the nearest enclosing` + line 114 `scope.` forms the complete sentence; line 114 then begins the environment definition, so the row range 89–114 is complete for the cited claim though it truncates the following sentence at line 115.

## Scope analysis

Literal support in the row's cited ranges:

1. **Factory locals belong to their enclosing scope** — 105–109: a function-block local's scope extends into contained blocks “unless a contained block introduces a different binding for the name”; 89–93 defines a free variable as a use not defined in the block.
2. **Free names resolve at runtime** — 322, exact and unique.
3. **Late module-global lookup** — 322–329; the documented example binds module `i = 10`, defines `f`, rebinds `i = 42`, calls `f()`, prints 42. Note this exemplar is module-level: it demonstrates a global free variable, not an enclosing-function local.

Derived, not literal: the row's teaches clause “distinguish caller rebinding from changes to the captured cell and late globals” is a compound inference from 105–109 + 113–114 + 322 + 323–329. The cited ranges contain neither `caller` nor `cell` in normative prose: `caller` occurs only in the exec/eval exception at line 335, and `cell` only in the non-rendered RST comment `.. XXX(ncoghlan)` at line 341. The distinction is defensible from the two normative passages, but the row should not be cited as if the documentation literally states cell identity.

Qualifications the same document states **outside** the row's cited ranges — these bound, but do not contradict, the cited sentences:

- 127–134: if a name binding operation occurs anywhere in a block, all uses in the block are references to the current block (so a read-before-assignment is `UnboundLocalError`, not a late free lookup). A case whose inner block assigns the name is governed here, not by 113–114.
- 136–148: `global` statement resolution via global then builtins namespaces; a `global` statement in the nearest enclosing scope makes a free variable global.
- 152–156: `nonlocal` refers to previously bound variables in the nearest enclosing function scope; compile-time `SyntaxError` if absent.
- 163–173: class definition blocks are special; class scope is limited to the class block and does not extend to methods. Method bodies inside classes are not covered by nearest-enclosing reasoning from the class block.
- **333–338: literal exception** — for `eval`/`exec`, “Free variables are not resolved in the nearest enclosing namespace, but in the global namespace.” A universal reading of 113–114 would be false there.
- 340–342: editorial `.. XXX` comment (non-normative) says the above is “only accurate for string execution” and that closure cells may be passed explicitly when executing code objects. This is a comment, not documentation text, but it is the file's own completeness caveat.

No contradiction of the exact quote, line, digest, tag, or cited ranges was found. Citation precision notes: row range 89–114 truncates the environment sentence at 115 if read as prose, and 322–329 ends exactly at the example's last line (blank line 330).

## Author-lane advisory (not clearance)

- **Admit-sample agreement: AGREE.** The file, tag peel, raw digest, exact line-322 quote, 12-word count, section placement, and 113–114 nearest-enclosing sentence all verify against the reopened official tag. The row's first two taught clauses are literally supported by its cited ranges.
- **Reject-sample agreement: AGREE.** Keeping S121 out of threading, detector hygiene, complete semantic detection, and complete Python semantics remains necessary; the qualifications above sit outside the cited ranges.
- **Keep rejected**: (a) S121 as proof that every free name in every construct resolves in the nearest enclosing scope (false for exec/eval string execution at 333–338 and for class blocks at 163–173); (b) S121 as proof of instrument/detector completeness; (c) citing the row as if the doc literally states “captured cell” or “caller rebinding”.
- **Derived flag**: label the captured-cell/caller-rebinding clause as a compound inference, not a verbatim source statement.

Source documents describe Python language behavior; they cannot establish that the C1 instrument detects it completely, that fixtures are correct, or that anything is admissible. This seat grants nothing.

## Unknowns / not established

- Whether any C1 eval-cell path depends on `exec`/`eval` string-execution semantics (which would require the 333–338 exception rather than 113–114 alone) — not inspected; outside this seat's assigned question.
- Whether the row's derived captured-cell clause was intended as inference or as paraphrase — the row text does not label it.
- Complete Python semantics: the file's own non-normative XXX note at 340–342 flags code-object/closure-cell coverage.
- Instrument completeness for any C1 form: not established and not establishable from source text.

## Receipts

Directory `.ufo/waves/round-22/w2/receipts/ReopenS121/`:

| file | sha256 / size |
|---|---|
| `source.json` | `0669117de28229cb6c6ef0127abbe819d283f5359c5c84a471ef0e92fc2cc7dc` · 18381 B |
| `executionmodel.rst` | `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89` · 24445 B |
| `executionmodel.headers` | `6135ad024c764ec40eff94494655cca8a3f190944a2bc745cdefaa5dc393cd45` · 895 B |
| `git-ls-remote-v3.14.8.txt` | `6549cb7c3492366c3440e8b774e38c2642d153ce3e3f660ac6d8e94b5447d0ac` · 121 B |
| `quote-line322.txt` | `7b11083b248bde8963cd48c4ba433dd9ed07b6e7e233f8467cb5b0aec449d383` · 73 B |
| `access-utc.txt` | `2026-10-21T15:37:59Z` |

`source.json` contains the full verification record, including exact normalized text for every cited and qualifying span; each `exact_text` was machine-checked against the reopened body, and the two-span global-statement text and the nearest-enclosing quote are labeled separately from full-span text.
