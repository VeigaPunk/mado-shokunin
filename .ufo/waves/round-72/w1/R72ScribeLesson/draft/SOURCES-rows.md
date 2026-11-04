# SOURCES rows — draft (wave seat R72ScribeLesson, 2026-11-04)

Three ready rows in the CORPUS.md 11-column schema (id, source, kind, tier, scope,
anchor, teaches, status, opened, recheck, used-by); no `|` inside any cell. Every digest,
byte count, line anchor and quote below was seat-verified over
`.ufo/waves/round-72/fetch/*.1-3` (byte-identical within each triple) before drafting.

- Ids S444–S446 were observed taken in the SOURCES.md **working tree** (rows at
  :394-396, uncommitted at read time); these drafts are numbered to match. If the L1's
  landing assigns different free ids, renumber; the row content does not depend on the id.
- Before any append the L1 runs the duplicate-id and duplicate-URL checks and the
  registry census (must exit 0 at round end). Seat pre-check over the committed r71 tip:
  no `unittest` row exists and none of the three URLs is held, so no new census W04
  warning is expected. S446 is a new `rejected` row at a **new** real path — a rejection
  curation, not a supersede (no `supersedes S###` marker, no W04 family entry).
- S444/S445 `used-by` name the round's knowledge entry `corpus/knowledge/
  outcome-verdict-gate-summary-r72.md` (untracked at read time — lands with the round).

```markdown
| S444 | CPython v3.14.8 unittest reference — TestResult.wasSuccessful — https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/unittest.rst | docs | A | mado lane tooling: the result object's pass/fail read is `wasSuccessful()`, the fact the round-72 outcome rule parses from the subject's own last summary instead of the process status (round-72 C2) | § TestResult, `wasSuccessful()`, unittest.rst:2127-2130 @ tag v3.14.8 (fetched 2026-11-04 three times, byte-identical: sha256 d6522f68c29c8ced8d2d81c91cb41ac739f855e6c0b9831f4a0e5a81f7ae5b86, 107372 bytes) | "Return ``True`` if all tests run so far have passed, otherwise returns ``False``." — the pass/fail fact lives in the result object, not in a runner's status | mined | 2026-11-04 | on-release | corpus/knowledge/outcome-verdict-gate-summary-r72.md |
| S445 | CPython v3.14.8 unittest runner — the exit derivation — https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/unittest/main.py | code | A | mado lane tooling: the official runner derives its process exit from `result.wasSuccessful()`, so a child's exit status is a projection of the result object and carries no independent assertion result (round-72 C2; also grounds C1's summary-first kill credit) | Lib/unittest/main.py:271-275 @ tag v3.14.8 (fetched 2026-11-04 three times, byte-identical: sha256 12de7da0fea92dbff8713ebe9904ada6dbd1e0a334d58861c6287ccfc0a261d2, 11660 bytes) | "if not self.result.wasSuccessful(): sys.exit(1)" — one status bit derived from the result, so the status cannot be read back as the assertion record | mined | 2026-11-04 | on-release | corpus/knowledge/outcome-verdict-gate-summary-r72.md |
| S446 | CPython 3.14.8 library reference — stdtypes mapping methods (round-71 reject, re-opened at its real 3.14 path) — https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/stdtypes.rst | docs | A | mapping-method behaviour (`dict.update`, `setdefault`) under `Mapping Types --- dict`; curated to keep the round-71 reject as a registry row, not admitted for call-site or result-object semantics | § Mapping Types --- dict :5299, `setdefault` :5523, `update(**kwargs)` :5529 @ tag v3.14.8 (fetched 2026-11-04 three times, byte-identical: sha256 5a6951b72ecc630a87f45a650fc11c186cfeb4251bedd1ea28f45bcb3116e8e1, 248201 bytes; the round-71 citation `Doc/library/stdtypes.rst` returns HTTP 404 at the pinned tag) | REJECTED: documents method behaviour (argument forms and defaults), not call-site or result-object semantics, and no admitted entry needs it; flip: a claim whose subject is mapping-method behaviour re-opens it | rejected | 2026-11-04 | 180d | — |
```
