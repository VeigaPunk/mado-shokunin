# ReopenExecModel — partly falsified: S111's bytes, tag pin and quote hold; the Gate line miscounts the quote (20 vs 19 words) and misstates its span (`:141-142` drops the leading "The" on `:140`), and the row's quoted anchor omits the `del`-unbinding premise the note/SKILL lean on

Target: `corpus/SOURCES.md:123` (S111), `corpus/lessons/round-20.md:48` (GATE S111), consumers
`corpus/knowledge/tripwire-precision-r20.md:30-33` and `SKILL.md:553-554`. Fetched bytes and
receipts: `.ufo/waves/round-20/w2/ReopenExecModel/fetch/`. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.

## Findings

### F1 — pinned URL, digest and size: row and existing receipt both hold
`curl -sSL --max-time 60 -o cpython-3.14.8-Doc-reference-executionmodel.rst -w '%{http_code} %{url_effective}' https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst`
→ `200 https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst`;
`sha256sum` → `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89`, size `24445`.
Row `SOURCES.md:123` says `24,445 B sha256 11f99f83…` — exact. Seat receipt
`.ufo/waves/round-20/fetch/CaseShadowing/receipts.jsonl:1` (fetched `2026-10-20T19:51:49Z`)
carries the same `11f99f83…` / `24445`; its body file hashes to the same digest.
The peeled-commit URL `.../8e6e75d9102e39bed2a2b279203a396741180f12/Doc/reference/executionmodel.rst`
also returned `200`, `24445 B`, `11f99f83…`, and `cmp` against the tag copy printed `IDENTICAL`.

### F2 — tag→commit pin: holds
`git ls-remote https://github.com/python/cpython refs/tags/v3.14.8 'refs/tags/v3.14.8^{}'`
```
992560c2cc62d47b308cec662feb485456847931	refs/tags/v3.14.8
8e6e75d9102e39bed2a2b279203a396741180f12	refs/tags/v3.14.8^{}
```
Row says annotated tag object `992560c2…` peeled to commit `8e6e75d9…` — exact. The seat
receipt `fetch/CaseShadowing/git-ls-remote-v3.14.8.txt` holds the same two lines.

### F3 — quote verbatim and ≤ 25 words: the row is right, the Gate line is wrong twice
File lines 140-142 (fetch copy):
```
140: ...module :mod:`builtins`.  The
141: global namespace is searched first.  If the names are not found there, the
142: builtins namespace is searched next. If the names are also not found in the
```
Programmatic check over the fetched bytes:
```
words_row_quote= 19
quote_in_140_142= True
quote_in_141_142= False
```
- Row `SOURCES.md:123`: `:140-142`, "19 words, whitespace normalized; in the `global`-statement paragraph `:136-144`" — correct on both line span and count (19 ≤ 25), and it carries the paragraph qualifier.
- Gate line `round-20.md:48`: `:141-142` "(20 words)" — **both wrong**. The quoted sentence starts with `The`, which is the last token of line 140, so `:141-142` alone does not contain the quote; the whitespace-delimited count is 19, not 20. The Gate line also drops the row's `global`-statement-paragraph qualifier.
Consequence: any consumer that trusts the Gate line gets a locator that fails containment and a wrong tally — the kind of numeric claim round 20's M3 (stale tally) and criterion 10 exist to catch (whether the criterion formally reaches gate-line word counts is [UNK]). The row itself is not at fault for these two fields.

### F4 — does the row support the knowledge note and SKILL?
`tripwire-precision-r20.md:30-33` claims (a) "the binding in effect at the call wins", (b) "a call before its `def` is a lead", (c) "`del` of a name that shadowed a builtin falls back to the builtin (no row)", (d) "a builtin rebound to a spawner … is judged by its binding". `SKILL.md:553-554` repeats (c): "`del` of a shadowing name restores the builtin (S111)".

Supported by S111:
- (a)(b): `:95-96` (each occurrence refers to the binding established by the resolution rules), `:113-115` (nearest enclosing scope), `:121-124` (`NameError` when not found; `UnboundLocalError` for an unbound local), `:127-132` (bindings are determined by scanning the whole block). Host probe on Python 3.14.8: `call_before_def: NameError name 'run' is not defined`; `del_nonbuiltin_then_call: NameError` — so treating a pre-def call as a lead, not an observed run, is grounded. Caveat: the rule is static per block, so "binding in effect at the call" is true for the module-level cells the tripwire reads, not inside a function (probe: `UnboundLocalError` for a name bound later in the same function body).
- (d): `:59-73` lists the constructs that bind names, `:95-96` makes the occurrence refer to that binding; the tool follows the binding — scanning `.ufo/waves/round-20/precision/CaseShadowing--print-lambda-spawn.jsonl` at the tip returns exit 1 with one `package_query` row marked `"evidence": "observed"`.
- (c): the file supports it, but only through two premises: `:81-82` "A target occurring in a `del` statement is also considered bound for this purpose (though the actual semantics are to unbind the name)." and the search order at `:140-142`; `:90-92` supplies "If a name is bound at the module level, it is a global variable". Probe: `module_level: shadowed_before_del=False builtin_after_del=True`. **The row's anchor cites `:140-142` (with `:136-144` as paragraph context) and `:59-61` — it does not cite `:81-82` or `:90-92`**, so the shipped quote alone does not demonstrate (c); w1 `CaseShadowing.md:177` itself marks applying the `:140-142` sentence to plain module code `[INFERENCE]` backed by that probe. The gate line attributes (c) to the case, not to a quoted source line.
- The SKILL sentence is true only at module scope: the probe's function-local case `local_shadow_then_del` printed `UnboundLocalError: cannot access local variable 'print' where it is not associated with a value`, and S111 `:122-124` documents that outcome. SKILL.md carries no "module-level" qualifier; in its cell-level context the use is correct, but the sentence as written overgeneralises.
- Implementation at the tip matches the note for module-level `del`: `tools/mado-tripwire.py:1588-1595` pops a `PURE_ARG_CALLS` name on `ast.Delete` (builtin restored) and otherwise stores `{"kind": "deleted"}`; `:1874-1877` routes `deleted` to the lead path. Scan of the committed case: `python3 -I tools/mado-tripwire.py --scan .ufo/waves/round-20/precision/CaseShadowing--del-print-restores-builtin.jsonl` → `MADO_TRIPWIRE: clean`, `rc=0`; `precision/expected.json:888-899` wants exit 0. Tool sha256 at the clone (`a4046a8`) is `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`, equal to the note's pin.

Net: the row supports (a)(b)(d) directly from its file and (c) only as a two-premise inference whose `del` premise is not in the row's anchor. The row is a fair source row; the consumer wording and the anchor's line selection are what need tightening.

### F5 — used-by omission (minor)
Row's `used-by` names only `corpus/knowledge/tripwire-precision-r20.md`. `SKILL.md:553-554` cites `(S111)` and `.ufo/waves/round-20/precision/expected.json:895` names "CPython executionmodel"; neither is listed. `[INFERENCE]` that `used-by` is meant to be exhaustive — `SOURCES.md` states only that the field changes in place and is logged.

## Verdict
Partly falsified. Hard checks on the row pass: URL 200, `11f99f83…` / 24,445 B equal to row and receipt, tag `992560c2…` → commit `8e6e75d9…`, quote verbatim and 19 words inside `:140-142`. The falsified parts are bookkeeping and anchor scope: the Gate line's `:141-142` locator excludes the quote's first word and its "(20 words)" is wrong (actual 19); the Gate line also drops the row's `global`-statement-paragraph qualifier; and the row's anchor does not cite the `:81-82`/`:90-92` premises that the note's and SKILL's `del` claim depends on, while SKILL's sentence is module-scope-only.

## Limits
- Only S111 (this seat's assigned row). I did not run `tw-precision.py` / `tw-recall.py` end-to-end (other wave-2 seats own C1/C2); I read `precision/expected.json` and ran the two named fixtures (`del-print-restores-builtin`, `print-lambda-spawn`) through the tip tool.
- The probe ran host `python3` 3.14.8 (matches the pinned tag) and only bound names/deleted them; it touched no service or host state. `[UNK]` whether L1 applies criterion 10 to gate-line word counts; the discrepancy is reported regardless.
- `[UNK]` whether any other round-20 artifact repeats the Gate line's "20 words" for S111; a lane grep for "20 words" hit `round-14-verifier-spotcheck.md:142` (S048), `round-20.md:47` (S110, genuinely 20 words) and `round-20.md:48` (S111, actually 19). Only the last is wrong.

## Installs
none.
