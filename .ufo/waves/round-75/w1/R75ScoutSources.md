# R75ScoutSources — round-75 w1 scout report

**Question.** Open the two sources the round's C2 claim rests on, three fetches each, and ground
`del env[KEY]` and `dict(env, KEY="1")` in the language/library reference at the same pin the
registry already uses — naming any existing `corpus/SOURCES.md` row for those URLs before the L1
appends.

**Answer, in one line.** Both branches are grounded at CPython tag `v3.14.8`, both documents
re-derive byte-identically three times, and both URLs are *already held at other scopes*
(`simple_stmts.rst` by S440/S447/S451; `stdtypes` by S446) — so the two new rows are
different-scope repetitions, i.e. **non-failing W04 warnings**, and must not carry `supersedes`.

## Findings

| | Source A — `del` statement | Source B — `dict(mapping, **kwargs)` |
|---|---|---|
| URL fetched | `…/v3.14.8/Doc/reference/simple_stmts.rst` | `…/v3.14.8/Doc/builtins/stdtypes.rst` (**not** `Doc/library/stdtypes.rst`, which 404s) |
| fetches | 3 × `curl -sS -f -L`, `cmp` 0 for 1-2 and 1-3 | 3 × `curl -sS -f -L`, `cmp` 0 for 1-2 and 1-3 |
| bytes | **41,375** | **248,201** |
| sha256 | **`d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`** | **`5a6951b72ecc630a87f45a650fc11c186cfeb4251bedd1ea28f45bcb3116e8e1`** |
| located span | `simple_stmts.rst:468-469` (§ The ``del`` statement, head at `:439-442`) | `builtins_stdtypes.rst:5350-5352` (signatures at `:5325-5327`) |
| quote (markup stripped — span has no RST markup) | "Deletion of attribute references and subscriptions is passed to the primary object involved" | "If keyword arguments are given, the keyword arguments and their values are added to the dictionary created from the positional argument" |
| word count | **13** | **21** |
| grounds | `del env[KEY]` deletes *into the mapping*, not the name ⇒ a literal-key delete between guard construction and launch removes the key the child would receive ⇒ C2 cancellation | `dict(env, KEY="1")` adds the keyword pair to a dict built from `env` ⇒ the copy carries `KEY` in key position regardless of the bound name ⇒ C2 guarded |

Pin re-derived read-only this run: `v3.14.8` → tag object `992560c2cc62d47b308cec662feb485456847931`,
peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12` (matches S105–S122, S440–S452).

**Requested path is absent, and that is itself already on the record.** All three attempts at
`…/Doc/library/stdtypes.rst` returned **rc=22, HTTP 404**. `corpus/SOURCES.md:396` (S446) records
the identical result for the round-71 citation and `:865` restates it; the 3.14 tree carries the
document at `Doc/builtins/stdtypes.rst`. Substituting that path is not a workaround — it is the
repair S446 already made, and my fetch reproduces S446's digest and length exactly (248,201 B,
`5a6951b7…`), as well as round-74's `.ufo/waves/round-74/fetch/stdtypes.rst.1`. Source A likewise
reproduces round-74's `simple_stmts.rst.1` digest byte-for-byte.

**Existing rows named (nothing displaced):**

- `simple_stmts.rst` — S440 (assignment statements `:190-194`), S447 (`global` `:972-973`), S451
  (attribute-reference targets `:160-165`). My span `:468-469` is unclaimed and disjoint.
- `Doc/builtins/stdtypes.rst` — S446 (mapping **methods** `update(**kwargs)`/`setdefault`,
  `:5299,5523,5529`, status `rejected`). My span is the **constructor** argument paragraph; S446's
  rejection reason (method behaviour, not call-site/result-object semantics) is not overturned.
- `Doc/library/stdtypes.rst` — held by no row as a fetched source; it appears only as the 404
  record inside S446 and the search-log prose at `:865`.

Per `corpus/SOURCES.md:502-509`, a same-URL collision is a merge-review trigger and a non-failing
W04 warning unless the row says `supersedes S###`. Drafts **S453** and **S454** therefore carry no
`supersedes`, and neither anchor cell uses a `pin <path>` token (criterion 107 would try to
resolve the external path inside the repo and fail — held external rows omit it for the same
reason).

## Confidence

- **High / observed:** digests, lengths, triple byte-identity, the 404s (`rc=22`), the tag pin, the
  line spans, the exact quote text and the 13/21 word counts, the existing rows and their scopes,
  the W04 rule text.
- **Inference:** that these two spans licence the round-75 C2 *rule shapes* — the documents ground
  runtime semantics, not the detector's syntactic approximation. No detector behaviour is claimed
  here; the C2 counting command is the only authority on that.
- **Gaps / not claimed:** no CPython code was executed; nothing about host posture was probed; the
  `dict` copy's aliasing beyond "the keyword pair is added to the new dictionary" is not claimed;
  `del` is modelled for a literal key in the same scope only, matching the claim's declared limit.

## Artifacts (all inside this seat dir)

- `sources.md` — full findings, quotes, line spans, word counts, registry overlap.
- `fetch-digests.txt` — three-fetch digest/length/`cmp` receipt for both documents.
- `fetch-404.txt` — the `Doc/library/stdtypes.rst` absence receipt (rc=22 ×3).
- `quote-locations.txt` — exact spans, raw lines, quote text, word-count commands, markup scan.
- `rows-draft.txt` — draft **S453**/**S454** rows ready for the L1 to append, with the W04 and
  criterion-107 mechanics spelled out.

Scratch `/fast/scratch/hyaku/mado-r75/R75ScoutSources/` held only the raw fetched bytes and was
deleted on exit (every cited digest is re-derivable from the pinned tag, proven byte-identical
three times). No lane file, no registry row, no git/jj write, and no PATH directory was touched;
no packages were installed.
