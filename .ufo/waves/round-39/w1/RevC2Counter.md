# RevC2Counter — C2 counter review (`quality/counters/c3-r39-options.py`)

Reviewed the C2 counter as delivered. Counter/tool/fixtures are currently UNCOMMITTED in the lane
(HEAD = `457d1b1` freeze commit; `git cat-file -e HEAD:tools/mado-options.py` → 128, same for the
counter and the fixture script). No data commit exists yet; the "tip" behavior below was verified on a
faithful scratch replica in `/tmp/c3scratch` (same bytes, two commits: base-no-tool → data-tool-fixtures).

## Verdict-line format (confirmed)
Final line: `PRED-C3-r39-v1: fixtures=N/N tool=present|absent verdict=TARGET_MET|TARGET_MISSED rev=<full-hash>`,
exit 0 on MET / 1 on MISS; setup failures print `PRED-C3-r39-v1 SETUP <msg>` and exit 2 (no verdict line).
Matches registration `fixtures=N/N tool=present verdict=TARGET_MET` syntax. Clause lines prefixed `PRED-C3-r39-v1 clause=…`.

## Checks
1. **Self-contained stdlib** — imports: `argparse, ast, json, os, re, shutil, subprocess, sys, tempfile` (all stdlib). Runs under `python3 -I`. No external deps.
2. **GIT_\* scrubbed** — module-level `ENV` and per-subprocess `env` drop `GIT_*`. Verified: with `GIT_DIR=GIT_WORK_TREE=GIT_CONFIG_GLOBAL=GIT_OBJECT_DIRECTORY=/nonexistent` the counter still resolves revs and prints the verdict cleanly (exit 1). Git access is read-only (`git -C <repo> rev-parse/--`).
3. **Exit 2 on base-precondition failure** — `--base` = rev containing the tool → `SETUP precondition_failed tool_present_at_base`, exit 2 (scratch: `--rev ec371c4 --base ec371c4`). Unresolvable revs also exit 2. ✓
4. **Base run (real lane)** — `python3 -I quality/counters/c3-r39-options.py --repo . --rev 08be4eb…` →
   `clauses=b:0 c:0 a:0 d:0 e:0 f:1 g:0` → `fixtures=0/1 tool=absent verdict=TARGET_MISSED`, exit 1 (matches registration "Before").

## Clause-bite matrix (scratch replica at data rev `ec371c4` vs base `e4c9f39`)
- a (tool at rev): bites — drop-tool commit → `tool=absent` MISSED exit 1; data rev → a=1.
- b (selftest assertions > 40): **CANNOT BITE POSITIVELY**. Tool `--selftest` prints exactly one line
  `MADO_OPTIONS_SELFTEST: 69/69 passed` (rc=0). Counter regex `(\d+)\s*/\s*(\d+)\s+assertions?` requires the
  literal word `assertions`; `passed` never matches → `assertions=0` → b=0 at the data rev. b is stuck at 0.
- c (fixture checker passes): **CANNOT BITE POSITIVELY as integrated**. The counter extracts ONLY `run-fixtures.sh`
  into an empty temp sandbox. The fixture script requires sibling artifacts: `$HERE/expected.json` and
  `$HERE/trees/{main-home,fifo-home,dangling-home}/…` (it computes `HERE` from its own location). In-place from the
  real seat dir the fixture passes `fixtures=4/4` rc=0; through the counter's sandbox it yields `fixtures=0/4` rc=1
  → c=0 at the data rev.
- d (row-shape `MADO_OPTIONS_ROWS:` marker): **CANNOT BITE POSITIVELY**. `grep -n MADO_OPTIONS_ROWS run-fixtures.sh`
  → nothing; the fixture never emits the marker the counter requires (clause d is nested under `fixture_ok` too).
- e (FIFO refusal, named): bites — manual: `mado-options.py: /tmp/fifo-ev/.config/hypr/hyprland.conf: not a regular file`,
  rc=3; data-rev run e=1.
- f (base lacks tool): bites — f=1 at base runs; base-with-tool → exit 2.
- g (stdlib-only imports): bites — tool imports `{argparse, glob, json, os, shutil, stat, subprocess, sys, tempfile}`
  ⊆ allowlist → g=1; absent tool → g=0.

## Result at data state (expected MET, observed MISSED)
```
PRED-C3-r39-v1 clause=b selftest_rc=0 assertions=0 ok=0
PRED-C3-r39-v1 clause=c fixtures=0/4 rc=1 ok=0
PRED-C3-r39-v1 clause=d row_shape=0
PRED-C3-r39-v1 clause=e strict_named_refusal=1
PRED-C3-r39-v1 clauses=b:0 c:0 a:1 d:0 e:1 f:0 g:1
PRED-C3-r39-v1: fixtures=0/4 tool=present verdict=TARGET_MISSED rev=ec371c4…   (exit 1)
```
Break-fixture commit → c=0 MISSED exit 1 (bites); drop-tool commit → a=0 MISSED exit 1 (bites). All expected
miss paths exit 1 cleanly with the verdict line; no crashes (base-run `ep` short-circuit prevents NameError).

## Findings / blockers to MET
1. **Clause b never bites**: selftest output format `69/69 passed` ≠ regex `N/N assertions` → assertions=0 → b=0 always. Tool must print `N/N assertions` (or counter regex widened).
2. **Clause c never bites**: counter stages only the one script file; fixture needs `expected.json` + `trees/` siblings. Counter must extract the whole fixture dir (or the fixture must be rewritten self-contained).
3. **Clause d never bites**: fixture never emits `MADO_OPTIONS_ROWS:` JSON marker.

Net: as delivered, the counter can only emit `TARGET_MISSED` at the data tip; `TARGET_MET` is unreachable.
Other clauses (a, e, f, g), exit codes (0/1/2), GIT_* scrub, stdlib self-containment, and verdict-line format all verified correct.

No tools installed (none needed). All evidence gathered read-only; no lane files modified. Scratch artifacts in `/tmp/c3scratch` (base `e4c9f39`, data `ec371c4`, drop `fc6bafa`, broken `fde13f1`).
