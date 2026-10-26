# SimpContract — C1 contract dead weight before data (round 43 w1)

Status: **complete**. Deliverable `.ufo/waves/round-43/w1/SimpContract/dead-weight.md`; receipts in
`.ufo/waves/round-43/w1/SimpContract/evidence/` (quote gate 31/31, hashes in `SHA256SUMS`). Scratch
`/fast/scratch/hyaku/mado-r43/SimpContract/` deleted. No tool installed (stdlib, `/usr/bin/python3` 3.14.8);
no pacman, no compositor verb, no network, no lane edit.

## What was run

The frozen counter was not scoreable in the sandbox here (no bwrap needed): the reference
`.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (sha256 `e3c2e4715059…`) was imported and driven through the
same `run(argv, stdin)` path, and all 37 fixtures were replayed in-process by patching only the counter's
`execute`: **37/37 pass**, i.e. the harness is the oracle the counter scores against. Three instruments:

- **65 input pairs** over 62 atomic claims of the 22 tool-contract sentences: 65/65 as expected (58 pairs
  differ, 7 constraint pairs are byte-identical; two compare verdicts only).
- **11 violating variants** of the reference over a 647-case corpus (107 fixture replays + path-kind/boundary
  battery + regex alphabet + 500 seeded lattice cases; histogram reaches every rc and all four SETUP
  reasons): **4 equivalent variants at 0/647**, **7 positive controls at 2–277 diffs**.
- **Fixture scan**: every argv/stdin/file byte of all 107 fixture runs, scanned for eight dimensions.

## Findings

**Deletable (6 items, no behaviour change; exact text in `dead-weight.md` §2):**

1. **DEL-1** the `1` in "REGEX fully matches **1-200** characters" — implied by `match:class[ \t]+(.+)` and
   by the field strip; V2 (`{0,200}`) is 0/647; P2 (relaxing the bound *and* the field grammar) differs
   63/647, so the field grammar must stay. The frozen controls already exclude `M38-regex-empty` for this
   reason — the same class of dead clause as round 43's `M20` `#` clause. Contract `:34`, reference `:34`,
   model `:129`, reference code `:69`.
2. **DEL-2** the cap number "at most **1048577** bytes" (V1 with `MAX_BYTES + 2` is 0/647); the *bound* is
   live and `M05-stdin-short` already kills a cap of `MAX_BYTES`. Contract `:20-21`, reference `:21-22`; no
   model edit.
3. **DEL-3** "tested in that order" for the last two verdict links (V3, V4 are 0/647; P5, which moves
   `NO_MATCHING_CLIENT` in front of `NO_SIZE_RULES`, differs 277/647). Contract `:55-56`, reference `:55-57`;
   no model edit (the `elif`s may be permuted).
4. **DEL-4** "not floats" — no JSON token is both an integer and a float; "not booleans" stays (Python
   `True` is an `int`). Both docstrings; no model edit, and adding a float test to the model would be dead code.
5. **DEL-5** two reference-docstring sentences no input can answer ("It reads files and standard input
   only; …", "DIFFER is a report, not a fault: …"); the counter's contract already omits both, which is the
   only reason its "restated here, the same sentence" claim is defensible.
6. **DEL-6** cosmetic: `first`/`first` duplicated across counter docstring lines 29–30.

**Live but unexercised by the 37 fixtures — free passes for a cheat (9, `dead-weight.md` §4):** flag order
(`--rules` before `--clients` in an expected-success run), non-UTF-8 rule files, rules-file argument order on
setup failure, a non-"," field separator, a duplicated `address` key, permission-denied paths, the
`unreadable ≺ too_large` link, the `too_large ≺ bad_json` link, and a zero-argument `size`.

**Deletions refused after checking (`dead-weight.md` §3):** the C14 order parenthetical is *mostly live* — a
mode-000 1048577-byte file and `/proc/kcore` are both unreadable and oversized (P6 differs), and a
1048577-byte invalid-JSON input is both too_large and bad_json (P7 differs); only `unreadable` vs `bad_json`
is vacuous, and that single link is not worth deleting a sentence for. Also rejected: "not booleans",
"BADSIZE ≻ TILED" (covered by `client0`'s `{}` client, which the fixture scan found), the 200 upper bound,
the first verdict link, and an alleged "takes precedence over the size rule" sentence that **does not exist**
in either docstring (hypothesis from the brief, refuted by grep; `evidence/grep-precedence.txt`).

## What the L1 should do

- Nothing is blocking data. None of the six deletions changes any score: the four that touch an expression
  are equivalent under the frozen controls (`M38`) or unobservable (`MAX_BYTES + 2`, `elif` order).
- If a **v2 re-freeze** happens before the data commit (registration §Residuals allows it), apply DEL-1…DEL-4
  to the counter docstring, DEL-1/DEL-2/DEL-3/DEL-4/DEL-5 to the reference docstring, DEL-1 to the counter
  model (`SAFE_RE`), DEL-1/DEL-2/DEL-3 to the reference code, and DEL-6 to the counter docstring.
  `M38-regex-empty` would then have to be **retired**, not just delisted: its patch target `{1,200}` disappears,
  and `run-c1-controls.py` aborts on a pattern that does not match exactly once (`controls` 46 → 45, and the
  `equivalent_mutants_excluded` header line changes).
- The nine free passes are a counter gap, not a contract gap: one fixture input each would close them, but
  that changes `TOTAL` and the controls, so it is a v2 decision, not a w1 edit.

## Residuals

- The reference is the only oracle: a sentence the reference and the model both ignore is invisible here.
  I checked the model against the reference for every deletion target and found them identical in the
  affected region (`SAFE_RE`/`SAFE`, `type(v) is int`, the verdict chain), so no divergence was introduced.
- The equivalence corpus reaches every rc and setup reason, but "equivalent on 647 cases" is not a proof;
  for DEL-1/DEL-2/DEL-3 the *argument* (unreachable regex, cap ≥ MAX+1, mutually exclusive conditions) is the
  proof and the corpus is the check. DEL-4 rests on JSON's number grammar, not on a corpus.
- No live sentence was found whose behaviour the model implements differently from the reference.
