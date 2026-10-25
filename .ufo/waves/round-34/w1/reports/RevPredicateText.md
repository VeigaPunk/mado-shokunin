# RevPredicateText — round 34 predicate-string parity review

Reviewer: w1 leaf (mado-shokunin). Date: 2026-10-24.
Method: `ast.get_docstring` + `ast.walk` on each `count.py` (PREDICATE constant and
module docstring line), `json.load` on each `frozen.json` (`predicate` value), and
the predicate line inside the `## C1 coverage` / `## C2 calibration` sections of
`.ufo/waves/round-34/registration.md` (markdown-fence-free, stripped line).
Compared byte-for-byte by sha256 over the extracted strings.

Note on paths: `registration.md` is one shared file at
`.ufo/waves/round-34/registration.md`; there are no per-case `c1/registration.md`
or `c2/registration.md` files. C2's coverage section is titled `## C2 calibration`.

## PRED-C1-r34-v1

All four sources carry byte-identical text (len=535, sha256 `5f6d9026a330ae60…`
for each of: `c1/count.py` PREDICATE, `c1/count.py` docstring, `c1/frozen.json`
`predicate`, `registration.md` `## C1 coverage`):

```
PRED-C1-r34-v1: TARGET_MET iff closed_entries=1 AND closed_rows=2 AND open_cites=0, where a frozen cite is closed only when the entry path and the fetch path are both regular files (not symlinks, nlink=1) whose every path component stays inside the scored root, the fetch bytes read with O_NOFOLLOW have sha256 equal to the digest in c1/frozen.json, the entry contains a 1-25 word gate-quote line for that id that is a contiguous substring of those bytes, and the registry row for that id lists the entry path as a whole used-by token.
```

Same sentence everywhere: **yes.** Same target triple: **yes** —
`closed_entries=1, closed_rows=2, open_cites=0`, matching
`EXPECTED_TARGET = {"closed_entries": 1, "closed_rows": 2, "open_cites": 0}` in
`c1/count.py` and `"target": {"closed_entries": 1, "closed_rows": 2, "open_cites": 0}`
in `c1/frozen.json`.

## PRED-C2-r34-v1

All four sources carry byte-identical text (len=405, sha256 `7b4a0f5864dea66c…`
for each of: `c2/count.py` PREDICATE, `c2/count.py` docstring, `c2/frozen.json`
`predicate`, `registration.md` `## C2 calibration`):

```
PRED-C2-r34-v1: TARGET_MET iff mismatch=0, where mismatch is 0 only when the last SCORECARD line matching r34-s189-line: publishes line=169 and line 169 of the regular-file fetch .ufo/waves/round-32/fetch/S189.bin opened with O_NOFOLLOW (nlink=1, sha256 eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d) strip-equals const size_t MAX_QUEUED_EVENTS = 64; and line 128 of that file does not.
```

Same sentence everywhere: **yes.** C2's predicate does not carry a
closed_entries/closed_rows/open_cites triple — its target is `mismatch=0`, and
`c2/frozen.json` holds scalar fields (`"published_line": 169`,
`"false_line": 128`, `"sha256": "eea605…40d"`) rather than a `target` object.
All embedded literals agree across sources: `line=169` / line 169 true,
line 128 false, `O_NOFOLLOW`, `nlink=1`,
sha256 `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d`,
quote `const size_t MAX_QUEUED_EVENTS = 64;`.

## Verdict

Both predicates are verbatim-identical across every surface (PREDICATE constant,
module docstring, frozen.json, registration.md). No drift found.
