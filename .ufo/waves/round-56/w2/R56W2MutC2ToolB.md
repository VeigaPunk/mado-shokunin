# R56W2MutC2ToolB — wave 2 (falsify), C2 tool mutation test

Attacked: the wave-1 claim that the C2 oracle (the tool's own `--selftest` plus the 18 committed and 8 revealed hold-out fixtures) is the only kill evidence for `tools/mado-watchplan.py` (rev `28fc86ac2359ec27406d8a2c63bef82ea6e947ed`, blob sha256 `ed6ee9f200cdc0646fb2f31898f37a2570318a7609d91c7cd730c501c1aa9379`). Item: source handling and watch list (absolute_path branches, glob, stat errors, symlink canonical watch, dir/file/missing typing, duplicates, `--display-root`, getoption parsing and verdicts, entry and size caps, argv).

Full write-up, the 117-row table and the proposed fixtures: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w2/R56W2MutC2ToolB/mutants.md`.

## 1. Verdict

- The wave-1 oracle kills **82 of 117** one-line mutants (70.1%); **82 of 107** non-equivalent mutants (76.6%).
- **25 non-equivalent behaviour changes survive** it. Each one has a verified killing input (23 as staged fixtures through the unchanged harness path; 2 — m75, m76 — only with a root-level config path the staged layout cannot express).
- 10 survivors are equivalent on Python 3.14.8, each with an argument (mutants.md §3.1).
- No pristine-tool defect was found by the mutation exercise. What it found is a coverage gap in the C2 predicate and one undeclared divergence (D2 below).
- Claim effect: the C2 predicate `TARGET_MET` shows the tool is operable on the 26 inputs; it does not show the watch list is right on the inputs listed in §3.2. The claim should be worded as an operability predicate, not as a discrimination test.

## 2. What I did

1. Read `claims-frozen-v2.md`, `registration-v2.md` (C2 E6–E8), `registration.md` §C2, the tool at rev, the harness `quality/r56_ctl_c2.py` at rev, the 18 committed and 8 revealed hold-out fixtures (both read in full).
2. Fresh git repo in scratch from `git archive 28fc86ac…` (checked `git -C "$D" rev-parse --show-toplevel` = `$D`). Lane not touched; no git mutation.
3. Baseline: pristine `--selftest` → `MADO_WATCH_SELFTEST: 82/82 assertions passed`, rc 0. Harness → `MADO_R56_C2: rev=28fc86ac… fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET`.
4. 117 one-line mutants (`driver/mutate.py`), each with a unique anchor and a one-line diff asserted; oracle = selftest + harness functions (staged, bwrap) on 26 fixtures + per-fixture breakdown. Run in 8 parallel workers. Result: 80 killed / 33 survived / 4 invalid in the first run; the 4 bad anchors corrected and re-run: final 82 killed / 35 survived / 0 invalid.
5. Classification of the 35 survivors: 10 equivalent (argued), 25 non-equivalent.
6. For each non-equivalent survivor, a candidate fixture (`driver/cands.py`, K01–K20) verified by `driver/verify.py` through the harness's own `score`/`staged_run`: pristine 1, mutant 0. **24/24 pairs KILLED** (`receipts/candidate-verify.log`). m75/m76 verified with `driver/root-level-probe.sh` (bwrap, root-level config).
7. Tried a random differential probe (`driver/difftest.py`); it was too weak (false negatives on m07 and m105) and was stopped at 11/35. Not used as evidence.

Commands (trimmed):

```
$ python3 -I driver/mutate.py --repo <lane> --rev 28fc86ac… --work $S/wk --out $S/out --jobs 8
TOTAL killed=80 survived=33 invalid=4 of 117
$ python3 -I driver/mutate.py … --only m82,m87,m101,m107
m82 SURVIVED  m87 KILLED  m101 SURVIVED  m107 KILLED
$ python3 -I driver/verify.py … --mutants all-tools.json --cands driver/cands.py --out $S/voutF
m01 K01 KILLED pristine=1 mutant=0 rc=0/0      …  m65 K19 KILLED pristine=1 mutant=0 rc=2/0
CANDIDATES killed=24 of 24 pairs
$ driver/root-level-probe.sh pristine-tool.py m75.py m76.py
m75: ERROR via=/hyprland.conf:1 source=sub/x.conf reason=nomatch     (pristine: n=2 path=/sub/x.conf found)
m76: ERROR via=/sub/x.conf:1 source=../a.conf reason=nomatch         (pristine: n=3 path=/a.conf found)
```

Killed by which oracle (of 82): selftest 73, fixtures 62, both 53, selftest only 20, fixtures only 9.

## 3. Defects, with input and severity

**D1 — weakens the C2 claim: coverage gap, 25 non-equivalent behaviour changes survive the wave-1 oracle.**
Inputs that the 26 fixtures and the selftest do not separate from the mutant:

- dangling symlink sorted first in a `source` glob (`inaccessible` must stop the line): F10 has it last. K04 (m14).
- dangling MAIN config symlink (canonical watch and `type=file` vs `type=missing`): K05 (m18, m21).
- MAIN config symlink to a directory: K06 (m25).
- display root given through a symlink (given-text prefix, trailing slash, `[:-1]`, `[1:]`): K07–K09 (m30, m31, m36, m95, m96).
- display root equal to a printed path (exact-equality branch of the spec): K10 (m94).
- backslash in an option value (`true\`): K11 (m49).
- `sourcex = …` treated as `source`: K12 (m51).
- a comment line `# x {` opening a category: K13 (m55).
- NBSP before the option key (WS strip set): K14 (m56).
- `=` inside a trailing comment (first-`=` split): K15 (m105).
- non-string option key with an integer value (crash in the mutant): K16 (m101).
- argv value with a trailing space (argv fidelity): K17 (m114).
- entry-cap boundary (1024, 131072, `>` vs `>=`): K18, K19 (m64, m109, m65).
- glob `**`, non-UTF-8 name ordering: K02, K03 (m07, m08).
- glob `RecursionError` (pristine maps it to `nomatch`): K20 (m09).
- root-level config path (`cur` one level deep): m75, m76 (bwrap probe only).

Severity: **weakens**. Not blocking as an operability predicate, but the 26-fixture predicate does not verify the watch list on these inputs, so a `TARGET_MET` does not say the tool is correct on them. Round-55 survivor rates were 46%, 21%, 24%; this seat's non-equivalent survivor rate is 23%.

Reproduction gap, stated: `driver/verify.py --mutants` takes a JSON map `{mutant id: path to mutant tool}`. `mutate.py` writes each mutant to `<work>/w*/mut/<id>/mado-watchplan.py` during the sweep, and that map was not kept as a receipt. The mutant files regenerate from the 117-row table in `driver/mutate.py`; sha256 of the 35 survivors' files are in `receipts/mutant-tools-survivors.sha256`.

**D2 — weakens: undeclared divergence (silent exception mapping).**
Input: a `source` line `source = ` + `*/`×1100 + `x` (or any pattern with ~1000 wildcard components). Pristine output: `MADO_WATCH: ERROR via=… source=… reason=nomatch`, rc 0. The `RecursionError` from `glob` is swallowed in `expand()` and reported as an ordinary no-match. The E8 declared-divergence list does not mention it. Whether glibc `glob(3)` (Hyprland's call) returns a no-match for such a pattern is NOT verified here: I did not run glibc. Severity: **weakens**; add the divergence or report the exception differently.

**D3 — weakens: fixture commitment blocks the cheap fix.** The 20 candidate fixtures cannot be added to `fixtures/c2` without changing `c2.fixture_commit_sha256` (and the holdout commitment), which needs a new versioned freeze (v3) before scoring. Severity: **weakens** (process).

**D4 — weakens: the random differential probe does not support equivalence claims.** `difftest.py` reported `distinguishable=False` for m07 and m105, both killed by one fixture (K02, K15). The vocabulary lacks `**` and `=` in comments. Severity: **weakens** (any "no difference found by fuzzing" wording would be wrong). Not used as evidence.

**D5 — cosmetic / risk: runtime.** K18 and K19 (262k entries) take ~5–9 s per tool run here; the harness `TIMEOUT` is 30 s. On a loaded host a timeout reads as rc None, which would score the pristine as failing. Severity: **cosmetic** at present.

**D6 — cosmetic: interpreter dependence.** m19 is equivalent only on CPython ≥3.13 (`realpath(strict=True)` raises OSError). K20 relies on the default recursion limit of 1000. Recorded in mutants.md §5.

## 4. Deliverables

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w2/R56W2MutC2ToolB/mutants.md`: method, classification, proposed fixtures, limits, full 117-row table.
- `…/R56W2MutC2ToolB/driver/`: `mutate.py` (117 mutants, oracle, parallel sweep), `cands.py` (K01–K20), `verify.py` (candidate verification through the harness path), `make-table.py`, `root-level-probe.sh`, `difftest.py` (PARTIAL, not evidence), `driver.sha256`.
- `…/R56W2MutC2ToolB/receipts/`: `pristine-selftest.txt`, `c2-baseline-stdout.txt`, `sweep-run1-results.json` / `.tsv` / `.log`, `sweep-rerun4-results.json`, `merged-results.json`, `candidate-verify.json` / `.log`, `root-level-probe.txt`, `table.md`, `mutant-tools-survivors.sha256`, `difftest-PARTIAL-not-evidence.log`.
- `…/R56W2MutC2ToolB/fixtures/<mutant>/<K##>/`: `args.json`, `tree/` (symlinks and raw-byte names preserved), `expected.out`, `expected.rc` for each candidate (24 pairs). No fixture for the 10 equivalent survivors (none can kill them) and none for m75/m76 (not stageable).

## 5. Unverified, and checks that did not run

- EQUIVALENT (10) is argued, not machine-proven (mutants.md §3.1). Probes run: glob NUL/`[z-a]` patterns, `realpath` loop, `RecursionError` threshold.
- The random differential probe ran for 11 of 35 survivors and was stopped; no result from it is used.
- Not run: real Hyprland, glibc `glob(3)`, other Python versions.
- m75/m76 killed only by the bwrap probe, not by the frozen harness.
- No repeat runs to measure flakiness (the candidate run was executed twice for m64/m65 with the same result).
- I read the revealed hold-out fixtures in this seat; the candidates were not derived from them.

## 6. Hosts, tools, scratch

- No tool installed or upgraded. Used the existing python3 3.14.8 and bubblewrap 0.13.1.
- Nothing written to the lane except the deliverable directory above. No git/jj mutation of the lane or fleet. No ~/.config, ~/.local, hyprctl, or fleet/sibling/shokuknow writes.
- Scratch `/fast/scratch/hyaku/mado-r56/R56W2MutC2ToolB/` removed before yield (after copying receipts). Probe temp dirs I created under /tmp removed.
