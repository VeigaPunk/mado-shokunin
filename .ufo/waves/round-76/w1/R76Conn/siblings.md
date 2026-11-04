# Round 76 sibling overlap — read-only sweep

## Sweep and boundary

2026-11-04, specialized `grep`, case-insensitive, gitignore disabled:

- Paths: `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge/**/*.md` and `/home/vgpnk/Projects/shokunin/*-shokunin/quality/counters/**/*`, excluding `/home/vgpnk/Projects/shokunin/mado-shokunin/**`.
- First pattern: `outcome field|witness|GIT_NO_REPLACE_OBJECTS|del env\[|interprocedural`.
- Direct-shape follow-up: `outcome field|GIT_NO_REPLACE_OBJECTS|del env\[|interprocedural`.
- Witness-only follow-up: `witness`, paginated with skip 0,20,40,…,260; pages list many generic historical/documentary witnesses. Selected relevant corpus entries were then read at explicit ranges.
- Directory discovery used `glob` on sibling `corpus/knowledge/` and `quality/counters/`. Only mado supplied a `quality/counters/` directory in that discovered set. No sibling counter implementation is inferred from prose about tools elsewhere.

An initial directory-glob grep returned no matches; that empty result was discarded and repeated using file globs, which found the records below. Absence statements below concern these literal searches and these surfaces, not semantic novelty across all tools or the fleet.

## Existing sibling ground

| Sibling / exact local path | Ground already held | Relation to r76 / non-equivalence |
|---|---|---|
| `kaidoku-shokunin/corpus/knowledge/2026-11-04-r72-checker-env-capsule.md:43-49` | A10 reads checker-emitted `clauses.run_nonce` / `clauses.run_binding`; `checker_met()` requires checker `met` and `clauses.met` agreement. Its `binding_ok=True` mutation is killed by `a10-binding-from-checker`. | Closest C1 overlap: instrument-owned emitted verdicts, not a probe's reconstructed success, are the acceptance surface. Does not hold mado's outcome conjunction, sixteen modes or four mutations. A11/A8 also distinguish raw child-environment observations from summaries, but they do not classify mado's syntactic guard deletions. |
| `kake-shokunin/corpus/knowledge/receipt-integrity.md:20-39,48-85` | Counter-error, absent-tool and stale-planted receipts must not earn witness/not-met credit. v2 binds a receipt to invocation using exit/note/counter hash/run window; shared row builders prevent an unwired gate. | Existing freshness/receipt-authority ground adjacent to C1. It is not mado's challenge echo mechanism. Explicit tension: kake must gate counter exit, while mado's subject assertion summary deliberately does not trust child rc as assertion truth. Different contract layers; neither universally overrides the other. |
| `chousa-shokunin/corpus/knowledge/keyed-engine-output-equivalence-r35.md:54-101` and `chousa-shokunin/corpus/knowledge/per-record-argv-attribution-r36.md:19-35,38-70` | Distinguishes routing witness, per-record query receipt and output correctness; trace entry alone does not establish computation, and a query-for-show can survive attribution. | The “echo is not truth” limit is already held in compatible form. mado's nonce is not a mechanism/computation certificate; neither sibling supplies r76 outcome or guard-control results. |
| `tameshi-shokunin/corpus/knowledge/witness-scoped-kill-verdict.md:8-23,46-54` | A red suite can be accidental rather than killed-on-witness; capture declared failing labels and keep attribution separate from aggregate rates. | Supports retaining each r76 mutant's named separator/score rather than only 4/4. Historical predeclaration contamination is explicitly disclosed; do not turn this into a universal independent witness implementation. |
| `tameshi-shokunin/corpus/knowledge/r41-variable-destination-writes.md:105-107` | Explicitly declares no dataflow, taint tracking or interprocedural analysis. | Literal `interprocedural` hit is a **limit**, not existing D3 support. |
| `lore-shokunin/corpus/knowledge/r103-canon-status-and-supersession.md:18` | Notes that a fiction contradiction record lacks a status/outcome field. | Literal `outcome field` hit is unrelated; exclude as C1 overlap. |

The direct-shape follow-up returned only the tameshi limit and lore unrelated hit. It found no sibling `GIT_NO_REPLACE_OBJECTS` or `del env[` literal on the searched surfaces, and no sibling positive interprocedural deletion implementation. This does not prove absence of equivalent implementations using different names or paths.

## Compatible synthesis — same single proposal as crosswalk.md

Use one typed provenance crosswalk to keep **emitted decision**, **run binding**, **assertion truth**, and **static carrier classification** separate. Cite the sibling entries as compatibility context, not as new source registrations or proof of mado's counts. In particular, pair mado's observable `verdict=` field with kaidoku's emitted-clause discipline, while carrying chousa's and kake's authentication/contract-layer limits verbatim in substance. Preserve tameshi-style named separators without changing mado's frozen kill rule.

Axes: calibration benefits from separating authority surfaces; operability is not harmed because no runtime, population, mutation family or gate is modified. Risk: treating generic witness language as duplicated end-to-end capability, or importing kake's exit rule into the assertion-summary layer. Verification belongs to L1: retain exact sibling paths, confirm claims stay within their local scopes, and check final mado receipts against the crosswalk. No sibling code, corpus, config, services or runtime were changed or invoked.
