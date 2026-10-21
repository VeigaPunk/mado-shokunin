# OracleCrossCell

Axis: C1 operability (cross-cell recall and argument binding).

Created `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/CrossCell.json` as two inert Python eval cells. The first imports `subprocess` and defines `query_package(name)`; the next cell calls `query_package("r21")`. Both cells have `reset: false`, preserving the helper and imported module in the shared session through the call.

## Semantic expectation

Expect one `package_query` row for `pacman -Q r21`, evidence `observed`. The helper is visibly defined before its use and directly invoked in the next cell. The literal argument binds to formal parameter `name`, which is used unchanged in the argv list supplied directly to `subprocess.run`; no callback or recursion is unresolved, so the exact command is statically established. `pacman -Q` is a package query. The package's presence or absence is not assumed and does not change the command classification.

The expectation follows Python binding and `subprocess.run` semantics plus the eval-cell reset contract, not detector behavior. The transcript was not executed; no tool or scanner was opened or run. No tests, measurements, host probes, or installations were performed.

Sources: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceNamespace/cpython-v3.14.8-executionmodel.rst:55-93,113-124`; `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:120,123`; [Python 3.14 subprocess documentation](https://docs.python.org/3.14/library/subprocess.html#subprocess.run); [Arch pacman(8)](https://man.archlinux.org/man/pacman.8.en).
