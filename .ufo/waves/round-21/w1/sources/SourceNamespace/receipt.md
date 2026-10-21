# Public source receipt — CPython execution model

- URL: https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst
- Access date: 2026-10-21
- Version locator: CPython v3.14.8 (URL tag); S111 records tag object `992560c2cc62d47b308cec662feb485456847931` and peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12`.
- Saved body: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceNamespace/cpython-v3.14.8-executionmodel.rst`
- Content type observed: `text/plain`
- Byte size: 24,445
- SHA-256: `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89`
- Located quote (`Doc/reference/executionmodel.rst:147-148`, section “Binding of names”): “If the nearest enclosing scope for a free variable contains a global statement, the free variable is treated as a global.” (21 words)
- Context: lines 89-93 define a name bound in a block as local unless `nonlocal`/`global`, module-level bound names as global, and a used-but-undefined-in-block name as a free variable.

The saved body digest and size match the existing S111 metadata in `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`. This receipt is a located public-documentation citation, not an execution or runtime-behavior measurement.