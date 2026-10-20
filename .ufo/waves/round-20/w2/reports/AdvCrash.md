# AdvCrash — falsified: 28c6837 crashes (exit 2, `internal RecursionError`) on well-formed transcripts at roughly half the AST depth 1f7f995 survives, and any expression depth inside a *called* helper/lambda/class-method body; the crash fails closed but flips a `findings`/`clean` verdict to `could_not_evaluate`.

## Scope
Crash fuzz of `tools/mado-tripwire.py` at 28c6837 (sha256 9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c, confirmed) vs 1f7f995 (sha256 367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d). Method: 172 well-formed `.jsonl` transcripts (fixtures generated, `--scan` only, nothing executed) covering every named shape — JS cells, reset cells, non-dict `arguments`, huge cells, 50–200-deep helper chains, self/mutual recursion, syntax errors, async comprehensions, walrus, match statements, lambdas in defaults — plus a grammar fuzzer (10 000 random cells, in-process dual-revision diff) and a 104-snippet deep-structure sweep run at the stock recursion limit (1000). Full per-fixture results: `w2/AdvCrash/results/scan-per-file.json`, `w2/AdvCrash/results/scan2-per-file.json`.

## Finding 1 (regression, confirmed): exit-2 `internal RecursionError` on transcripts 1f7f995 scans clean

Minimal reproducer (committed bytes also at `w2/AdvCrash/fixtures2/min_repro_deep_helper_attr.jsonl`):

```python
def f():
    x = a.b.b.…        # 550 attribute levels
f()
subprocess.run(['ls'])
```

`python3 -I /tmp/tw-28c6837.py --scan min_repro_deep_helper_attr.jsonl` →
`MADO_TRIPWIRE: could_not_evaluate`, `"error": "internal RecursionError"`, exit 2.
Same file at 1f7f995 → `MADO_TRIPWIRE: clean`, exit 0.

Two distinct new recursion surfaces:

1. **Module level** — `x = a` + `.b`×500 crashes 28c6837 (`eager_calls` NodeVisitor, `generic_visit` at ast.py:510 — ~2 C-frames per AST level); 1f7f995 survives to ~1000+ (its crash is `module_unsafe_names.scan`, ~1 frame/level). Bisected: new trips between d=480 and d=500; old between d=900 and d=1000. Fluent chains `a.m().m()…` trip new at ~150–200 links vs old ~400. Traceback head: `classify_eval → prepare_eval_calls → eager_calls → ast.visit/generic_visit` (tw:1792→1758→1670). `eager_calls` is new code (tw:1646–1673); the old revision has no per-statement NodeVisitor.
2. **Deferred bodies** — any expression deeper than ~500 inside a *called* `def`/`async def`/lambda/`__init__`/method body crashes new via `spawn_scan → prepare_eval_calls(helper.body) → module_unsafe_names.scan` (tw:1840→1735→1356, traceback captured). 1f7f995 never recursively scanned helper bodies (`ast.walk` is iterative), so helper-body depth is unbounded there. 11 fixture files reproduce this end-to-end: `deep_attrchain_in_helper`, `deep_callsuffix_in_helper/init/method/lambda`, `deep_attr_in_lambda/staticmethod`, `deep_binop_in_helper`, `deep_body_via_chain`, `deep_helper_cross_cell`, `deep_in_inner_def_called` — all new=2 (`internal RecursionError`), old=0. Depth ~490–550 suffices; threshold scales down inside nested helper calls (each followed helper adds frames).

**Verdict-masking consequence (strongest counterexample):** `x = a` + `.b`×550 + `\nsubprocess.run(['pacman','-S','z'])` → new `could_not_evaluate`/exit 2, old `findings`/exit 1. A crash in one cell discards that cell's findings entirely and flips the file verdict; inside a directory scan it aborts the whole run (confirmed: `--scan fixtures2/` exits 2 under both revisions for their own crash files). Exit 2 *wins over* 1, so this fails closed — a judge may weigh it as robustness-only — but a generated transcript containing a long fluent chain or a helper with a deep expression turns a real hit into "could not evaluate" rather than a finding.

Impacted axes: the L1 repair's correctness delta (new exit-2 class created where none existed), criterion-30 style precision evidence (any scored corpus entry containing a deep expression in a helper body would be silently unscoreable), and "guards unchanged" framing (new crashes sit outside all named guards).

**Smallest safe correction:** catch `RecursionError` in `classify_eval` around `prepare_eval_calls`/`spawn_scan` and degrade to `eval_unparsed += 1` (matching the existing never-executed semantics for unparseable cells) — one `try` in `classify_eval` fixes both surfaces and every deferred-body variant. A strictly better fix iterates `eager_calls`/`update_bindings`/`module_unsafe_names`, but the parity set (deep class-body/module expressions, `sudo` chains, deep JSON-adjacent shapes below) remains crashable on both revisions either way.

## Finding 2 (parity, not a regression): pre-existing exit-2 surfaces both revisions share

- Module-level deep expressions ~≥1000 (`deep_attr_chain_5k`, `deep_binop_2k/50k`, `deep_call_suffix_2k`, `huge_string_concat_2k/20k`): `internal RecursionError` on both.
- `sudo ×1500` chain: `classify_segment` recurses per `sudo` (tw:1072), crashes both at ~1500 (`depth>8` cap only bounds `classify_shell`, not `classify_segment` re-entry).
- Non-dict line / dict without `"type"` (`deep_json_line` = a 3000-deep JSON list): `unknown record shape`, exit 2 both — `could_not_evaluate` by design for malformed records.
- `1e400` timestamp field: `invalid line (ValueError)` both [UNK: this json.loads accepted `1e400` in a plain interpreter but the tool reports ValueError; identical in both revisions, parity regardless].
- 2 MiB single-token bash command: ~88 s in pure-Python `shlex.read_token` (9 calls × 9.8 s, 6 000 021 `StringIO.read` calls — `tokenize` re-reads the whole token per punctuation_chars access; cProfile attached in evidence). **Symmetric** — both revisions identical time; not a regression, but a head-of-line DoS worth noting for any harness with a wall-clock gate.

## Confirmed safe (no new crash surface)

- All malformed-record shapes (`arguments` list/string/null/number, `content` string/null/dict/mixed items, `name` non-string, non-string `code`/`command`, weird `timestamp`/`id`, surrogate escapes): handled, exit 0, zero exceptions — 10 000-cell grammar fuzz found **zero** anomalies in either revision on well-formed-ish eval/bash text.
- Semantic exit diffs all match the intended repair: `frozenset_block` (old 1 → new 0), `helper_lambda_default`/`shadow_subprocess_var`/`namedtuple_field` (old 1 → new 0), `partial_spawn`/`rebind_pure_name`/`posonly_kwonly`/`method_via_instance_var`/`class_callable_instance` (old 0 → new 1). `helpers_50/200_deep` new=0 vs old=1 is the documented execution-path/depth-4 discipline, not a crash.
- Zero uncaught crashes (exit ∉ {0,1,2}) in 172 fixtures × 2 revisions; zero new-only timeouts.
- `reset`/`language`/JS cells, import-star/exec/globals rebinding, `from . import`, kwargs/vararg/posonly binding shapes, match/NamedExpr/ExceptHandler binding tracking: no exceptions either revision (104-snippet sweep).

## Limits

- Crash verdict is `error: "internal RecursionError"` — an honest fail-closed signal, not a false `clean`; the regression is a verdict flip (findings/clean → could_not_evaluate), not a missed finding silently labeled clean.
- Depth thresholds measured under CPython 3.14 stock limit 1000; exact numbers shift with `sys.setrecursionlimit` but the ~2× new-vs-old gap and the unbounded-helper-body delta are structural.
- Only `--scan` exercised (mandate). `--selftest`/`--frozen` not fuzzed.
- 6 000 eval + 4 000 shell grammar cells; exotic generators (deep `cond_expr`, `lambda_nest`, match-class patterns) sampled, not exhaustive.

## Installs

none. (Python 3.14 stdlib only; tools were `git show` extracted into /tmp — no repo mutation.)
