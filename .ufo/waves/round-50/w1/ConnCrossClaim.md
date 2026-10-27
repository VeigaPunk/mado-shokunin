# ConnCrossClaim — causal separability at round-50 freeze

## Verdict
**The claimed separability is not established; there is a concrete read coupling.** C1 writes corpus entry/registry/lesson/pins/receipt artifacts, while C2's v3 gate scans every tracked path by default (`--scope all`). Thus C2 reads the C1 surface as scanned input, even when its own executable is the only C2 change. This is an overlap in read/write surfaces, not evidence of a harmful finding in the C1 artifacts. The requested four frozen-counter final lines cannot be produced in w1: neither round-50 counter is frozen or present yet, and the r49 counter tests a different claim/path contract.

## Evidence
- Claims: `claims.md:33` asserts disjoint reads, while `claims.md:14-31` defines C1 corpus additions and C2 gate replacement. C2's stated default-scope-all behavior is explicit at `claims.md:27-30`.
- C1 counter source `quality/counters/c2-r49-bind-entry.py:155-161, 205-216` names entry, registry, README, lesson, fetch and receipts paths; its round-50 port is not available in the seat at this time. The r49 counter consumes committed revision content, including repository tree/object data, not only the entry file.
- C2 gate source `.ufo/waves/round-49/w1/ExecSessionShapes/check-session-material.py:9-18, 2091-2145` reads tracked files from the repo revision; default scope is all. The identical v3 draft is present at `.ufo/waves/round-50/w1/ExecGateV3/check-session-material.py` (sha256 `ffdc9d62c387050e016cf9d0eaacbf87f37d6647021cbd2c492eb6328dddbb61`). Installed v2 at `quality/check-session-material.py` is different (sha256 `82c9053ae2e8b7db2fb8c0e195c32b8b151a593cf9412dcae3589427ac2dfa6f`).
- Executed: `python3 -I <v3 draft> --selftest` → `SELFTEST: passed=94/94 failed=0`; v2 selftest → `SELFTEST: passed=69/69 failed=0`. The base v2 full-tree run at revision `8ae47b957034ae21012bbf09173cca2c48be345e` exited 1 with `SESSION_MATERIAL: files=22998 findings=113`; this is baseline behavior, not a C1-vs-C2 isolation run.
- The round-50 `ScrEntryR50/hyprland-bind-key-match-r50.md` exists as a seat artifact and states its rows/pins/receipt are under round-50 paths, but the entry's own locator alias table still says round-49 paths / its header says Round 49 (`:20, :22-36`). It is not a frozen/integrated C1 payload and was not used to claim counter success.
- The r49 counter's constants target `hyprland-bind-key-match-r49.md`, round-49 lesson/fetch/receipt paths and base `03e4ae76...` (`quality/counters/c2-r49-bind-entry.py:155-163`). Therefore running it against round-50 candidates would not be a valid PRED-C1-r50 run, and this seat did not invent a modified/frozen counter.

## Affected axes and proposed move
- **Coverage:** no direct change measured here. C1's coverage contribution remains independent in intent.
- **Operability:** gate's whole-tree scope creates a second-order dependency on all tracked C1 additions; it can change C2 finding counts/verdicts as C1 content lands. This is the only observed potential axis interaction; no actual C1-induced finding was measured.
- **Bounded move:** freeze C2 counter fixtures as two matched committed trees differing only by C1 payload (gate unchanged), and record gate results on each. Keep default all-tree gate semantics; treat any C1-induced detection as an explicit cross-claim effect rather than claiming strict independence. This tests the real policy without weakening privacy coverage.

## Files read / coupling
- C1 counter (r49 template): fixed entry, `corpus/SOURCES.md`, `corpus/README.md`, lesson, current/held fetch-pin trees, receipts; base/revision Git objects for novelty/presence and row/quote validation; live hyprctl replay is only reached by its replay clause. The port should retain analogous round-50 inputs.
- C2 v3 gate: `git ls-tree -r` tracked paths in its selected scope, then file blobs via `git cat-file --batch`; default is whole tree. For the r50 counter, its spec additionally reads the gate source bytes from the tested revision and creates nonce fixture repos; the gate selftest itself uses Python standard library and generated scratch repos.
- **Coupling:** C1 writes the corpus files/pins/receipt, and C2 default scope reads them. C2 also reads the C1 counter and other tracked sources as ordinary tracked files. C1 does not appear to read the gate path from its named inputs. No other shared mutable input was demonstrated.

## Verification and limitation
- Verified the two selftest outputs and v2 base-run summary above.
- Could not produce four final counter lines: at the inspected round-50 tree, `ExecCounterC1R50` and `ExecCounterC2R50` contain no counter source (C2 seat only has `receipts/`), and no round-50 counter freeze exists yet per claims. The requested r49 counter does not match the round-50 claim paths. No scratch trees or counter verdicts are represented as run.
