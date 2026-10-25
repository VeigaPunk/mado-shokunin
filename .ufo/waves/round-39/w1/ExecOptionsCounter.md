# ExecOptionsCounter — C2 counter

Implemented only `quality/counters/c3-r39-options.py` as assigned.

- Predicate/docstring is `PRED-C3-r39-v1`; supports `--repo`, `--rev`, and optional `--base` (frozen default `08be4eb7fd13358ed29b096e8924005d46ac409c`).
- Git access is read-only and every subprocess environment excludes ambient `GIT_*`; unresolved revs and a tool already present at base produce setup exit 2.
- Scores committed tool presence, isolated `--selftest`, committed fixture checker, required JSON row fields, and named refusal of a FIFO config path; standard-library imports are checked from the committed AST.
- Final line emitted as `PRED-C3-r39-v1: fixtures=N/N tool=present verdict=TARGET_MET|TARGET_MISSED rev=<resolved>`; miss exit 1.

Evidence gathered (no counter execution per parent-owned verification policy):
- `git rev-parse HEAD` → `457d1b125932c1e0d797061a2156b917bcd7edaa`.
- `git cat-file -t 08be4eb7fd13358ed29b096e8924005d46ac409c` → `commit` (exit 0).
- `git ls-tree -r --name-only 08be4eb7fd13358ed29b096e8924005d46ac409c -- tools/ | grep -c mado-options` → `0` (base precondition evidence).
- Round-39 registration specifies `fixtures=N/N tool=present verdict=TARGET_MET`, exit 0; fixture deliverable path is `.ufo/waves/round-39/w1/ExecOptionsFixtures/run-fixtures.sh`.
- Not run: selftest, fixtures, counter, build/lint/test. Expected to run after integration: `python3 -I quality/counters/c3-r39-options.py --repo . --rev <data-revision>`.

Risk: counter expects the fixture checker to accept `--tool`, `--repo` arguments, emit `fixtures=N/N`, and a `MADO_OPTIONS_ROWS:` JSON marker for row-shape scoring. Confirm the fixture seat's interface at integration; a mismatch produces TARGET_MISSED. No tools installed.