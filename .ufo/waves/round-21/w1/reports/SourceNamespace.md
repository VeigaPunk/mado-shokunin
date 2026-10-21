# SourceNamespace — CPython global/free-variable boundary

## Axes

- **C1 operability:** this source supports an independently stated name-binding/shadowing oracle boundary; it is specification evidence only, not a measurement of the tool.
- **C2 calibration:** this public-source receipt does not validate an artifact-integrity gate or its judgments.

## Located source evidence

- **Observed:** CPython 3.14.8 language reference, `Doc/reference/executionmodel.rst`, fetched from https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst on 2026-10-21.
- **Quote (21 words):** “If the nearest enclosing scope for a free variable contains a global statement, the free variable is treated as a global.”
- **Exact source lines:** 147-148, under “Binding of names”. Lines 89-93 provide the surrounding definitions: block-bound names are local except `nonlocal`/`global`, module-level bound names are global, and used-but-undefined names are free variables.
- **Saved source body:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceNamespace/cpython-v3.14.8-executionmodel.rst`
- **SHA-256:** `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89` (24,445 bytes). It matches the digest and byte size already recorded by S111.
- **Receipt:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceNamespace/receipt.md`

## Existing S-row coverage

**S111** in `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` is the same versioned URL and broad name-binding/resolution subject. Its recorded anchors are `:59-61` (formal parameters) and `:140-142` (global namespace searched before builtins); its row describes module-level globals and binding/shadowing. However, those recorded anchors do **not** cite `:89-93` or `:146-148`, and the row does not explicitly record the free-variable-to-global rule. Thus S111 covers the document and adjacent binding scope, but explicit locator coverage of this exact boundary was not established in the existing row. No new SOURCES row was added; L1 reserves S116 onward.

## Limits and remaining unknowns

This is a documentation claim about Python name resolution, not runtime evidence about a particular tripwire, interpreter execution, wrapper, or dynamic-code path. The quote establishes the stated free-variable/global treatment only; it does not by itself settle behavior outside that scope. Source identity, digest, and quote location are high-confidence; no runtime behavior was exercised.