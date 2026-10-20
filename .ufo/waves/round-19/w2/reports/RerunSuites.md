# MadoR19.RerunSuites — holds

Item: run every assigned tripwire suite on the committed tool at
`01b80946d92b26370d3012a7da655d00dd135154`, plus both `--frozen` replays, after proving the
worktree tool bytes are that commit's. I tried to make this false by (a) checking the harness can
actually fail, (b) mutation-testing the six merged patch areas plus permit/frozen logic, (c) running
from a foreign cwd with an empty environment on a copied suite, (d) checking every positive
expectation against its fixture line, and (e) proving the documented r18 extras are *exactly* the
three former misses and nothing else. All attempts failed; the item holds with the tallies below.

## 1. Byte identity (prerequisite, not assumed)

```
$ git -C <lane> rev-parse HEAD
01b80946d92b26370d3012a7da655d00dd135154
$ sha256sum tools/mado-tripwire.py
367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d  tools/mado-tripwire.py
$ git show 01b80946…:tools/mado-tripwire.py | sha256sum
367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d  -
$ git diff --stat 01b80946… -- .ufo/waves/round-{17,18,19}/tripwire .ufo/waves/round-{18,19}/frozen
(empty)
$ git status --porcelain .ufo/waves/round-17/tripwire .ufo/waves/round-18/tripwire \
    .ufo/waves/round-19/tripwire .ufo/waves/round-18/frozen .ufo/waves/round-19/frozen
(empty)
```

Worktree tool = tip tool; every suite/frozen file is tip's byte set; no untracked file inside a
suite can alter a result. Every tally below prints `SELFTEST_SCRIPT_SHA256: 367be947…`, i.e. the
bytes that ran are the bytes I hashed.

## 2. Verbatim tallies (first and second run byte-identical)

Command form: `python3 -I tools/mado-tripwire.py --selftest <DIR>` (cwd = lane; `rc` captured from
python, not from a pipe).

| suite | tally | rc |
|---|---|---|
| `.ufo/waves/round-17/tripwire/core` | `SELFTEST_SUMMARY: 9/9 passed failed=[]` | 0 |
| `.ufo/waves/round-17/tripwire/compound` | `SELFTEST_SUMMARY: 16/16 passed failed=[]` | 0 |
| `.ufo/waves/round-17/tripwire/hardening` | `SELFTEST_SUMMARY: 33/33 passed failed=[]` | 0 |
| `.ufo/waves/round-17/tripwire/w2-regressions` | `SELFTEST_SUMMARY: 30/30 passed failed=[]` | 0 |
| `.ufo/waves/round-18/tripwire/frozen` | `SELFTEST_SUMMARY: 31/31 passed failed=[]` | 0 |
| `.ufo/waves/round-18/tripwire/r18-failsafe` | `SELFTEST_SUMMARY: 1/1 passed failed=[]` | 0 |
| `.ufo/waves/round-19/tripwire/r19-bashcvar` | `SELFTEST_SUMMARY: 45/45 passed failed=[]` | 0 |
| `.ufo/waves/round-19/tripwire/r19-helperfn` | `SELFTEST_SUMMARY: 34/34 passed failed=[]` | 0 |
| `.ufo/waves/round-19/tripwire/r19-installers` | `SELFTEST_SUMMARY: 18/18 passed failed=[]` | 0 |
| `.ufo/waves/round-19/tripwire/r19-vcs` | `SELFTEST_SUMMARY: 17/17 passed failed=[]` | 0 |
| `.ufo/waves/round-19/tripwire/r19-frozen-f1f2` | `SELFTEST_SUMMARY: 13/13 passed failed=[]` | 0 |

Sum: **247/247 cases, 11/11 suites rc=0, zero `CASE … FAIL` lines** (per-suite `CASE … ok` line
counts equal each numerator: 9,16,33,30,31,1,45,34,18,17,13). Second run diffed against first:
identical including the `SELFTEST_SCRIPT_SHA256` line.

Frozen replays (rc from python; JSON is an excerpt with keys reordered and `inputs[]` abridged as `…`):

```
$ python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen
MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch
{"exit": 1, "expected_sha256": "4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9",
 "outcome": "frozen_verdict_mismatch", "scan_exit": 1, "scan_label": "findings",
 "tool_sha256": "367be947…", "missing_findings": [],
 "extra_findings": [{"class":"package_query","file":"inputs/r13-root.jsonl","line":4,"rule":"pacman:-Q"},
                    {"class":"package_query","file":"inputs/r14-source-safety.jsonl","line":2,"rule":"pacman:-Q"},
                    {"class":"package_query","file":"inputs/r14-source-safety.jsonl","line":3,"rule":"pacman:-Q"}]}
rc=1

$ python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-19/frozen
MADO_TRIPWIRE_FROZEN: frozen_match
{"exit": 0, "expected_sha256": "50d2a45e2602cb430b94043f6c658204b0b1802e8c1931cb2a3eda167af02435", …}
rc=0
```

Both match the expected outcome in the assignment: r18 `frozen_verdict_mismatch` with extras only
at the three former misses; r19 `frozen_match`. All 5 pinned inputs `ok:true` in both replays.

**Exactness of the "three former misses" clause** (the part most likely to overclaim):

```
r18 pin: 8 expected findings {host_mutation:6, live_probe:1, package_query:1}; known_misses 3
extras(file,line) == known_misses(file,line): True
extra classes: {'package_query'}  extra rules: {'pacman:-Q'}
r19 pin: expected findings 11 {host_mutation:6, live_probe:1, package_query:4}; known_misses []
r19 pin contains all three former misses: True
```

The extras are a set-equal match to `known_misses` in
`.ufo/waves/round-18/frozen/expected.json` (r14-source-safety:2, :3, r13-root:4 — the three notes
there name the R17-V4 misses and the TwMissBashCVar/TwMissHelperFn targets), the class/rule is
`package_query/pacman:-Q` for all three, nothing else is extra, and `missing_findings` is empty
(8+3=11 = the r19 pin's 11 findings). No hidden loss is masked by the mismatch.

## 3. Attack: can these suites fail at all?

The pass criterion is exact, not count-based:
`tools/mado-tripwire.py:2062` compares sorted `(class, rule, line[, basename])` tuples for equality;
`:2063-2068` additionally pins label, `want_error_contains`, `want_ids`; frozen-mode cases pin
`(outcome, exit, len(missing), len(extra))` at `:2036-2042`; a failing case returns 1 (`:2077`).

Harness failure modes (scratch copies in /tmp, lane untouched):

```
--selftest /tmp/rs/empty            -> SELFTEST_SUMMARY: 0/0 malformed expected.json (FileNotFoundError)   rc=2
--selftest /tmp/rs/nonexistent-dir  -> SELFTEST_SUMMARY: 0/0 malformed expected.json (FileNotFoundError)   rc=2
--selftest DIR with case want_findings=99 and no schema -> 0/0 malformed (AssertionError)                  rc=2
mutant M8 suite (2 real failures)   -> SELFTEST_SUMMARY: 29/31 passed failed=['verdict-extra-finding','known-miss-violated']  rc=1
```

So green cannot come from an empty/skipped case list; and red really propagates rc=1.

## 4. Attack: do the suites bind to the six merged patches?

One surgical single-line mutant per merged behaviour, run against all 11 suites + both frozen
replays (mutant copies in `/tmp/rs/mut/*/mado-tripwire.py`; rule-injection asserted to match
exactly once in the source before running):

| mutant | patch area | suites red | frozen r18 / r19 |
|---|---|---|---|
| M1 `if False:` at pacman dispatch (`:979`) | pacman class | 9 (core, compound, hardening, w2-regressions, frozen, r18-failsafe, r19-bashcvar, r19-helperfn, r19-frozen-f1f2) | mismatch / mismatch |
| M2 `if False:` at jj dispatch (`:969`) | jj write class | 1 (r19-vcs) | mismatch / match |
| M3 `if False:` at git dispatch (`:974`) | git write class | 2 (hardening, r19-vcs) | mismatch / match |
| M4 `found = None` (`:995`) | installer channels | 1 (r19-installers) | mismatch / match |
| M5 helper branch `if False:` (`:1412`) | same-text helper argv | 1 (r19-helperfn) | mismatch / match |
| M6 `expanded = None` (`:873`) | shell function positional expand | 1 (r19-helperfn) | mismatch / match |
| M7 permit ignored (`:1619`) | permit semantics | 7 (core, compound, w2-regressions, frozen, r19-bashcvar, r19-installers, r19-vcs) | mismatch / match |
| M8 drop `bool(extra)` (`:1973-1974`) | frozen extra detection | 1 (frozen) | **match** / match |
| M9 `missing = Counter()` (`:1965`) | frozen missing detection | 2 (frozen, r19-frozen-f1f2) | mismatch / match |

**9/9 mutants killed by at least one suite**, and the kill lands in the area's own suite for every
patch claimed by wave 1 (M2→r19-vcs, M4→r19-installers, M5/M6→r19-helperfn). M8 additionally proves
the documented r18 `frozen_verdict_mismatch` is produced *solely* by the extra-detection path: with
that path disabled the r18 replay flips to `frozen_match`.

## 5. Attack: fabricated expectations / wrong line attribution

Resolved every `want_findings` entry (367 findings, 88 distinct `(class, rule)` pairs) to its
fixture file and line and checked the rule token appears in that line. 367/367 resolve; 1 flagged
and explained, 0 defects:

- `r19-bashcvar` / `r19-reset-false-keeps-carry` wants `package_query pacman:-Q` at
  `reset-false-keeps-carry.jsonl:3`, whose text is
  `subprocess.run(["bash","-c",recipe])` with no literal `pacman`. That is correct by construction:
  line 1 binds `recipe = "pacman -Q hyprland"`, line 2 is `reset: false`, so the carry survives to
  the line that executes it — exactly what the case name asserts.
- (2 paths my first pass "unresolved" were my own `args[0]=="."` path join, not the tool's.)

Negative cases are real too: no fixture across the 11 suites is smaller than 2 bytes, and every
suite's `CASE … ok` numerator equals its `expected.json` case count (45/34/18/17/13 for r19).

## 6. Attack: host/cwd dependence

Copied `tools/mado-tripwire.py` + `r19-bashcvar` + `r19-vcs` to `/tmp/rs/herm`, then

```
env -i /usr/bin/python3 -I /tmp/rs/herm/mado-tripwire.py --selftest /tmp/rs/herm/r19-bashcvar
SELFTEST_SUMMARY: 45/45 passed failed=[]   rc=0
env -i /usr/bin/python3 -I /tmp/rs/herm/mado-tripwire.py --selftest /tmp/rs/herm/r19-vcs
SELFTEST_SUMMARY: 17/17 passed failed=[]   rc=0
cd /tmp && python3 -I <lane>/tools/mado-tripwire.py --selftest <lane>/.ufo/waves/round-19/tripwire/r19-installers
SELFTEST_SUMMARY: 18/18 passed failed=[]   rc=0
cd /tmp && python3 -I <lane>/tools/mado-tripwire.py --frozen <lane>/.ufo/waves/round-19/frozen
MADO_TRIPWIRE_FROZEN: frozen_match        rc=0
```

Suites are hermetic and cwd-independent; the assignment's exact invocation reproduces.

## 7. Cross-check against declared numbers (no overclaim found)

Wave-1 reports declare exactly these tallies — `TwFrozenF1.md:140-144` (9/9, 16/16, 33/33, 30/30,
31/31), `CriticInstallerClass.md:33-35` (1/1, 31/31; legacy unchanged), `TwBashCVar.md:15` (45
cases), `TwInstallers.md:18` (18 cases), `TwMerge.md:161-167` ("nothing extra outside the three
former known-miss lines"). My measurements match all of them, including the r18 extras set.

The "selftest 443/443" figure in the wave context is the **gate** (`bash tools/mado-verify.sh
--selftest`), not a tripwire number; nothing I measured contradicts it and nothing I measured
supports it — I did not run the gate (out of this item; it has its own coverage).

## 8. Trap worth flagging to L1 (not a defect)

Three superseded draft suites carry `expected.json` under `.ufo/waves/round-18/drafts/tripwire/`:

```
r18-bashcvar   15/15  rc=0
r18-installers 13/13  rc=0
r18-helperfn   22/24  rc=1  failed=['sh-fn-positional-n','sh-fn-single-quoted']
```

The two draft failures are declared, intentional re-cuts: both expect `package_query pacman` for a
bare `pacman` that the round-18 fail-safe reclassifies as `host_mutation pacman`
(`.ufo/waves/round-19/w1/reports/TwHelperFn.md:71-73,131`; merged
`r19-helperfn/expected.json` pins the re-cut values and passes). Anyone who globs "all dirs with
expected.json under tripwire" will see a spurious red; the gate list is the 11 suites §2 names.

## Limits

- The r19 frozen baseline is self-generated: its `expected_findings` is the tool's own output on
  those bytes at the same `tool_sha256=367be947…`, as `.ufo/waves/round-19/frozen/README.md:9-16`
  states. `frozen_match` therefore witnesses byte/pin stability and the refusal rule (no source
  finding lost, no finding on an unhinted line), *not* independent correctness of the classifier.
  The r18 replay is the only cross-version witness, and it is contradictory-by-design (3 extras).
- Mutation testing shows the suites bind to behaviour; it cannot show the 247 expectations are all
  semantically *right* (e.g. `pacman` bare → `host_mutation`, or `journalctl` → `live_probe`). I
  spot-checked line attribution and the three r18 extras' provenance, not every verdict's policy.
- M8 kills only the r18 `frozen` suite for the extras path; `r19-frozen-f1f2` stays green because
  its `want_extra` cases also carry `want_missing` and thus remain mismatched. Coverage exists,
  redundancy does not. [INFERENCE] that a future extras-only regression would be caught once, by
  `round-18/tripwire/frozen`.
- Interpreter: `/usr/bin/python3` 3.14; tallies are for that interpreter with `-I`. Not measured on
  3.12/3.13.
- I did not run the gate, any gate copy, `frozen-repin.py`, `tw-recall.py`, `fresh-pins.py` or
  `landed-check.sh`; C1/C2/C3 and the non-claim repairs are other seats' items.
- Sibling seats wrote during my run: untracked `evidence/harm/`, `fetch/RETENTION.json`,
  `w1/reports/RevDraftInstallers.md` appeared, and tracked `SCORECARD.md` (+38) and
  `.ufo/waves/round-19/fetch/.gitignore` (+6) were modified. Neither is mine. None touches a suite
  directory, `tools/mado-tripwire.py` (sha still `367be947…`) or a frozen dir, so §1's byte
  identity and every tally remain valid against tip's committed bytes; the worktree as a whole is
  no longer globally equal to `01b80946` for that reason alone.

## Installs

None. No package manager, no sudo, no network fetch, no jj. Scratch only under `/tmp/rs/`.
