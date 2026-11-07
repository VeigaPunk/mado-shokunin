# R97MReviewC2 -- attack report on C2 (counter self-invocation) -- round 97 w1

Base revision `e6152b589c2c6a28426c28263c4bcc3c46398be4` (branch `master`). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Scratch `$HYAKU_SCRATCH/mado-r97/R97MReviewC2`.
All probes read-only; nothing installed or upgraded. The only repositories I created are throwaway
scratch repositories under my scratch dir (each `git -C "$D" rev-parse --show-toplevel` = `$D`,
asserted); the lane repo was never mutated. `[MEASURED]` = command + output in
`receipts/review-c2-r97.txt`; `[INFERENCE]` = reading only.

The C2 drafts were rewritten at least seven times during this seat. Numbers below are tied to the
hash of the bytes measured. Snapshot at 14:28 local (the executor's 14:31 revision is measured in
the Delta section immediately after this table and supersedes these hashes):

| artifact | sha256 | measured |
|---|---|---|
| `build/c1-r96-magictext-selftest.py` | `cc39301e67845723058cc478b7eb90d35be5c094d804a64dc1a13783509528aa` | strip/diff, selftest, panel, scenes |
| `build/c2-r96-selftest-kills-selftest.py` | `c5aadb87b1edbe6ca7be09c1b6dec7dfcb2a383bd0165296a1923e1a5eba4109` | strip/diff, selftest, panel, scenes |
| `build/c2-r97-counter-selftest.v2.py` | `97783bf8bf0038c14b4573f1b7cc5461279f4069b0e6440fa8cbb17b197bc1fa` (superseded by `05fa7910c71ac001a32ad0a0c7ced3c8bdacf628e7275e2b09c7077e4dd59652` at 14:31; the findings below were re-checked on that revision: same `counter` requirement, same `uncovered_ok`, same `reg_rev == 3`, same anchor-gated stub, and the real-panel run still prints `SETUP_ERROR ... broken row 'missing-input' malformed`, rc 2) | end-to-end runs |
| `controls/counter-selftest-panel-r97.json` | `a672c9fcce52de9edf966a5bb5f6aede1134bcdec35424dc4d5c8b5dc08221ec` | anchors, duplicates, instrument run |

---

## Delta after the executor's 14:31 revision (re-measured, supersedes where they conflict)

The executor reported three fixes at 14:31; the bytes on disk are now
c1 `377a34fe822bb567717f28a51d48db3fdcd3978714bafa5c6dd100c4cc15aeb9` and
c2 `861883b3a823106377fb76f9dd1e8a5b184c1843361de244c4730b29c3dcb9ae` (instrument `abb17a01...`).

Closed, verified `[MEASURED]`:

- **F1 (self-containment) is fixed.** A bare scene holding only the counter and the fixtures
  (`sc/quality/counters/c{1,2}.py` + `sc/.ufo/waves/round-97/selftest-fixtures/`) now prints
  `MADO_COUNTER_SELFTEST: checks=7 failed=0` rc 0 for both counters. The repo reads are gone.
- **Env precedence is fixed.** `MADO_SELFTEST_FIXTURE_DIR=<empty dir>` plus
  `--fixture-dir <good fixtures>` runs green, i.e. the explicit flag wins.
- **The empty-fixture vacuity is fixed.** With `c1-mutants.json` / `c2-kills.json` emptied,
  the counters print `FAIL C1-mutant-mismatch` / `FAIL C2-mutant-mismatch`, rc 1.
- Byte identity holds: c1 `added=175 removed=0 hunks=4`, c2 `added=177 removed=0 hunks=4`,
  both `stripped_equal_base=True`.
- With a **re-anchored** panel (7 entries per counter, 6 broken rows carrying
  `counter`/`path`/`expect_line`/`expect_exit`; my file sha `96335f5c...`) the current v2 instrument
  reaches `TARGET_MET` rc 0 on a scratch layout: `selftest_green=2/2 checks=7,7
  negative_ids=14/14 broken_modes=6/6 broken_c1=3/3 broken_c2=3/3 base_refuse=ok
  registry=1->3 ledger_members=2/2`.

Still open:

- **The landed panel is stale against the new bytes.** 10 of its 16 `find` anchors now occur
  **0** times (`C1/C2-green-target-met`, `-mutant-mismatch`, `-result-format`, `-no-scratch-left`,
  `-fixture-parses`), because the check bodies were rewritten. With it the instrument would report
  `find occurs 0 times` for 10 entries and `negative_ids=6/16`. It must be re-anchored (and the
  duplicate ids, F7, resolved at the same time).
- **F2 still stands.** The newest instrument (`abb17a01...`) still requires a `counter` field, and the
  real panel still yields `MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR ... broken row 'missing-input'
  malformed`, rc 2 `[MEASURED at 14:34]`.
- **F6 still stands.** In the re-anchored TARGET_MET run the ledger leg again printed
  `ledger rc=1 uncovered_ok=True` (the scratch checker reports `bad_pointer>0`), and the verdict
  stayed TARGET_MET: rc and verdict are still ignored.
- **F4 was narrowed here and is closed by the third pass below.** At this revision `*-result-format` was still `bool(re.compile(...).pattern)`
  (always true) in both counters, and `*-green-target-met` is a fixture-shape assertion; the
  neutralisation clause still cannot tell those from a check that bites, even though
  `*-mutant-mismatch`, `*-no-scratch-left` and `*-fixture-parses` now do bite.



### Third pass (executor's F4 fix: c1 `3cb53f2c`, c2 `5bb32d0a`) -- [MEASURED]

- strip/diff: c1 `added=176 removed=0 hunks=4`, c2 `added=178 removed=0 hunks=4`,
  `stripped_equal_base=True` for both.
- lane and bare counter+fixtures scene: both green (`checks=7 failed=0`, rc 0).
- `*-result-format` now asserts `src.count(<emit line>) == 2` and bites: neutralising `== 2` to
  `== 3` prints `MADO_COUNTER_SELFTEST_FAIL: C1-result-format` / `C2-result-format` at rc 1.
  F4 is closed for the counters' scope; `*-green-target-met` remains a documented shape check.
- F8 recommendation given to the executor: drop the absolute committed fallback; keep
  `--fixture-dir` > `--repo` > walk-ups > `__file__` sibling.
- The panel is stale against these bytes: 10 of 16 anchors occur 0 times (both
  `green-target-met`, `mutant-mismatch`, `result-format`, `no-scratch-left`, `fixture-parses`).
  The counters must be frozen before the panel is re-anchored, or every further edit re-stales it.

### Frozen bytes (c1 `dd9b5a0b`, c2 `d4689f5a`) -- verdict for the counters' scope

Executor froze these bytes and asked for a verdict. Verified independently `[MEASURED]`:

- strip/diff vs base: c1 `added=173 removed=0 hunks=4`, c2 `added=175 removed=0 hunks=4`,
  `stripped_equal_base=True` for both;
- zero `/home/vgpnk` literals in either file; resolver order `--fixture-dir` > env > `--repo` >
  walk-up `__file__` > walk-up cwd > sibling;
- lane green (`checks=7 failed=0`, rc 0) and bare counter+fixtures scene green with
  `--fixture-dir`; a lone copy with no nearby fixtures and no env prints
  `MADO_COUNTER_SELFTEST_FAIL: C1|C2-fixture-could-not-evaluate` + `checks=0 failed=1`, rc 2;
- bites: neutralising `return src.count(needle) == 2` to `== 3` prints `C1|C2-result-format` at
  rc 1; emptying `c1-mutants.json` / `c2-kills.json` prints `C1|C2-mutant-mismatch` at rc 1.

**Recommendation: accept for landing, for the counters' scope only.** Standing conditions outside
the counters: the panel must be re-anchored to exactly these two shas (10 of 16 anchors are stale),
and the c2-r97 instrument must accept the panel shape it is handed. Documented limit: the
`*-green-target-met` check is a fixture-shape check, so the mode proves fixture and check wiring,
not production green.

### F1 -- BLOCKER: the instrument's green leg cannot see the c2 counter green in the layout the instrument builds

`[MEASURED]` The v2 instrument materialises only the two counters and the fixture tree into its
layout root, then runs each `--selftest` with `--fixture-dir <root>/.ufo/waves/round-97/selftest-fixtures`.
The c2 counter's selftest derives `REPO = normpath(FIX/../../../..)` (line 460) and then **reads the
repository** in four of its seven checks:

- `C2-green-target-met` reads `<REPO>/quality/check-selftest-strength.py` (line 492);
- `C2-missing-panel` and `C2-wrong-rev-pin` compute `_sha(<REPO>/quality/check-selftest-strength.py)`
  to build their argv (the exception is caught as a failed check);
- `C2-mutant-mismatch` reads `<REPO>/quality/check-receipt-presence.py` (line 508).

A layout with the counter and the fixtures and nothing else -- exactly the instrument's layout -- makes
those four checks fail:

```
scene: sc2/quality/counters/c2.py + sc2/.ufo/waves/round-97/selftest-fixtures/ (lane fixtures)
$ (cd sc2 && python3 -I quality/counters/c2.py --selftest --fixture-dir .ufo/waves/round-97/selftest-fixtures)
MADO_COUNTER_SELFTEST_FAIL: C2-green-target-met
MADO_COUNTER_SELFTEST_FAIL: C2-missing-panel
MADO_COUNTER_SELFTEST_FAIL: C2-wrong-rev-pin
MADO_COUNTER_SELFTEST_FAIL: C2-mutant-mismatch
MADO_COUNTER_SELFTEST: checks=7 failed=4
rc=1
```

and the instrument run against the current pair, with the panel and fixture tree copied at their
real relative paths, prints

```
selftest quality/counters/c1-r96-magictext.py rc=0 checks=7 failed=0 green=True
selftest quality/counters/c2-r96-selftest-kills.py rc=1 checks=7 failed=4 green=False
MADO_COUNTER_SELFTEST_COUNT: TARGET_MISSED ... selftest_green=1/2 ... negative_ids=10/14 ... rc=1
```

So clause (i) (`selftest_green=2/2`) is unreachable with the current drafts. The c2 counter is green
only when run *in the lane* (where the walk-up finds the real `quality/` tree): `checks=7 failed=0`
rc 0 `[MEASURED]`. Contract 3 asks the `--selftest` to run "over committed fixtures"; reading
`quality/*.py` of the containing repository makes it a repo test, not a fixture test.

This also invalidates the earlier TARGET_MET observation: that run used an older c2 revision whose
selftest still hardcoded the lane root and therefore read the lane from inside the layout.

### F2 -- BLOCKER: the landed panel cannot be consumed by the landed instrument

`[MEASURED]` Instrument run with the real panel:

```
$ python3 -I build/c2-r97-counter-selftest.v2.py --repo R --rev 7145377 --base-rev bcbdc37 \
    --panel controls/counter-selftest-panel-r97.json --expect-panel-sha256 a672c9fc...
MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR pred=PRED-C2-r97-v1 broken row 'missing-input' malformed
rc=2
```

Three independent mismatches in the frozen inputs:

1. `broken` rows carry no `counter` field (`{'id': 'missing-input', 'counter': None, ...}`) and no
   `path`; `validate_panel` requires a string `counter` and rejects the panel before any leg;
2. there are **3** rows total, not ">=3 per counter" (6) -- the validator would also refuse on
   `counter ... has N broken rows < 3`;
3. `expect_line` is `MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR` -- the **runner's** verdict prefix.
   The counters print `MADO_MAGICTEXT_COUNT: SETUP_ERROR` (c1) and `MADO_SELFTEST_KILLS: SETUP_ERROR`
   (c2); neither ever prints `MADO_COUNTER_SELFTEST_COUNT` `[MEASURED]`. `expect_exit: 2` is also
   wrong for two of the three modes: measured `wrong-rev` -> rc 1, `mutated-tool` -> rc 1, only
   `missing-input` -> rc 2.

### F3 -- BLOCKER (claim arithmetic): the registry before-state is 1, not 0; the instrument enforces 1 -> 3 while the declaration says 0 -> 4; the published command cannot measure either

`[MEASURED]` Table rows (`lines starting with '|'`) of `git show e6152b58:SKILL.md` (469 rows):

```
tools/mado-mimetext.py                              1   (line 887; added by 5dd921b3, round 96)
quality/counters/c1-r96-magictext.py                0
quality/counters/c2-r96-selftest-kills.py           0
quality/selftest-kills/check-receipt-presence.json  0
covered artifacts at base = 1
```

The `mado-mimetext` row is named by `git log -S'mado-mimetext' -- SKILL.md` -> `5dd921b3`. The one
`check-receipt-presence` hit elsewhere is the gate row `mado-receipt-presence` (line 870), which
names `check-receipt-presence.py`, not the kill-set JSON.

- the declaration's "registry holds **0** rows for the four round-96 artifacts" and its `0 -> 4` are
  false at base; the honest move is `1 -> 4`, or `1 -> 3` if the kill-set is ruled out;
- the instrument has been revised to three artifacts and enforces `reg_base == 1 and reg_rev == 3`
  (`c2-r97-counter-selftest.v2.py:607`), with a docstring ruling that the kill-set "is in the
  mado-selftest-strength row's population, not a registry row of its own (R97MCritic C2-2, L1
  ruling)". That ruling holds only while the `mado-selftest-strength` row's entry command does not
  name `quality/selftest-kills/check-receipt-presence.json`; once the round-96 pair is added there,
  a four-artifact count scores the artifact too (base 0 -> 1 on that row alone);
- the published counting command has no `--base-rev` (`has --base-rev: False`), while the v2 CLI
  requires `--base-rev` and `--expect-base-registry-sha256`
  (`error: the following arguments are required: ...`, rc 2 `[MEASURED]`). The declaration's command,
  the predicate sentence and the instrument must be made to say the same thing before the freeze.

### F4 -- MAJOR: clause (ii) cannot distinguish a check that bites from a decorative check

`[MEASURED]` All 16 panel entries are credited on the final bytes (rc 1 + declared id), but most of
the checks they neutralise are decorative:

| check | what it actually asserts |
|---|---|
| `C1-green-target-met` | fixture JSON `version == 2` and 2 cases, and a dummy file lacks a string |
| `C1-mutant-mismatch` | `broken.count(mut["find"]) == 0` after its own `str.replace` -- no counter run |
| `C1-result-format` | `bool(re.compile(...).pattern)` -- always true |
| `C1-no-scratch-left` | `isdir(FIX) and len(listdir(FIX)) > 0` -- the opposite of its name |
| `C1-fixture-parses` | `json.loads` of one fixture |
| `C2-green-target-met` | panel has `hand`/`neutral` and the gate source contains a word (F1) |
| `C2-mutant-mismatch` | a string replacement changed the string |
| `C2-result-format` | `bool(pat.pattern)` -- always true |
| `C2-no-scratch-left` | no leftover dirs beside the fixtures |

The strongest bite in the whole set is the fixture-break test (2 of 14 checks). A counter whose
checks are `return True` placeholders passes clause (ii) as soon as each placeholder is text-editable
to fail. The clause needs a companion: each id must also be observed failing on a *broken input*,
not only on a corrupted assertion.

### F5 -- MAJOR: `always_ok_flagged == 0` is guaranteed by construction, so the stub control cannot fail

`[MEASURED, code] `c2-r97-counter-selftest.v2.py:485-488` credits the echo stub only when
`stub_src.count(chk["find"]) == 1`; `ECHO_STUB` is six lines and contains none of the anchors, so
`stub_flagged` is False for every entry before any other conjunct is evaluated. The run prints
`always_ok_flagged=0 stub_uncredited=14/14` regardless of what the stub does. A control that cannot
fail is not evidence.

That said, the instrument *does* reject a stub counter fed through the normal path: with `c1`
replaced by a stub that prints `MADO_COUNTER_SELFTEST: checks=7 failed=0` and exits 0, the run
prints `TARGET_MISSED ... negative_ids=3/14 broken_c1=0/3` because every `find` anchor occurs 0 times
in the stub `[MEASURED]`. So the predicate's answer to "stub vs real counter" is carried by the
anchor conjunct, not by the always-OK control.

### F6 -- MAJOR: the ledger leg accepts a ledger run that failed

`[MEASURED]` `uncovered_ok = "uncovered=0" in out` -- no rc and no verdict. In my instrument run
the ledger checker printed `LEDGER: ... uncovered=0 ... bad_pointer=182 empty_desc=0 verdict=TARGET_MISSED`
and exited 1, and the runner still counted `ledger_uncovered_ok=True`. Clause (v) says the ledger
"reports uncovered 0"; a run whose verdict is TARGET_MISSED is not that report. Require rc 0 and
`verdict=TARGET_MET` (the lane's ledger prints exactly that at base, rc 0).

### F7 -- MAJOR: panel content -- duplicate ids and two non-single-check neutralisations

`[MEASURED]` The panel has 8 entries per counter for 7 checks: `C1-green-target-met` twice and
`C2-missing-panel` twice (`distinct 7`). A FAIL line carries only the id, so two entries for one
check are indistinguishable and inflate `negative_ids`. Two entries are not single-check either:
neutralising `C1-wrong-rev-pin` prints `['C1-missing-cases', 'C1-wrong-rev-pin']`, and the second
`C2-missing-panel` entry prints `['C2-missing-panel', 'C2-wrong-rev-pin']`.

Positive: all 16 anchors occur exactly once in the final bytes (`stale anchors: 0`), and the ids
they name are ids the counters really print (16/16 credited).

### F8 -- MAJOR: fixture resolution -- ambient env outranks the explicit flag; the machine-local path is back

`[MEASURED, code]` Resolution order (c1:1344, c2:408) is
`MADO_SELFTEST_FIXTURE_DIR` env > `--fixture-dir` > `--repo` > walk-up from `__file__` > walk-up
from cwd > `__file__` sibling. An ambient variable overrides the explicit command-line flag, so a
run under a shell that exports it reads a tree the caller did not ask for; the runner passes only
`--fixture-dir`, so it cannot detect the substitution. `--fixture-dir` must win.

The machine-local fallback is still present in both current drafts:
`grep -c '/home/vgpnk/Projects/shokunin/mado-shokunin'` = **1** in each (the `_committed` path). A
committed gate must not carry this lane's absolute path; the walk-up already covers the in-lane case.

### F9 -- MINOR: fixture rename classification and exception-as-failure

`[MEASURED]` Renaming a guarded input (`c1-cases.json`) -> rc 2, no FAIL id (the early guard fires).
Renaming an unguarded input (`host-list.txt`; `c2-kills.json`) -> rc 1 with ids `C1-missing-cases` +
`C1-wrong-rev-pin` / `C2-mutant-mismatch`, but the cause is an exception (`_sha(HOST)`,
`open(CKILLS2)`) reported as a check failure, indistinguishable from an assertion. Ids are hardcoded
strings and do not change under relocation: a moved fixture dir with `cwd=/tmp` gives the identical
`MADO_COUNTER_SELFTEST: checks=7 failed=0` `[MEASURED]`.

The absent-`--fixture-dir` spelling was fixed during the wave: `MADO_COUNTER_SELFTEST_FAIL:
<C1|C2>-fixture-could-not-evaluate` + `MADO_COUNTER_SELFTEST: checks=0 failed=1`, rc 2 `[MEASURED]`.

### F10 -- MINOR: one c1 revision broke the production path and the selftest stayed green

`[MEASURED]` c1 `4b8ba55d` (14:15) had `added=186 removed=1`, stripped != base: `draft =
bool(a.draft_tool)` was deleted while 1316/1318/1335 still read `draft`; `symtable` showed
`main().draft = {local: False, global_: True, assigned: False}` -- `NameError` on every production
run that reaches the verdict -- and its `--selftest` was green (`checks=7 failed=0`). The line was
restored at 14:21. The bytes are overwritten (transcript-only); the method is reproducible:

```
python3 - "$P" <<'EOF'
import symtable, sys
p = sys.argv[1]
st = symtable.symtable(open(p, encoding="utf-8").read(), p, "exec")
for s in st.get_children():
    if s.get_name() == "main":
        d = {x.get_name(): x for x in s.get_symbols()}.get("draft")
        print(dict(local=d.is_local(), global_=d.is_global(),
                   assigned=d.is_assigned(), referenced=d.is_referenced()))
EOF
```

Current c1 prints `{'local': True, 'global_': False, 'assigned': True, 'referenced': True}`.

---

## Seat items, answered

1. **Strip and diff.** c1 final `added=220 removed=0 hunks=4`, `stripped_equal_base=True`
   (stripped sha = base `9d3e1e76...`); c2 final `added=174 removed=0 hunks=4`,
   `stripped_equal_base=True` (stripped sha = base `2bd9e562...`). The added lines are the pre-parse
   `--selftest` dispatch, the two argparse flags, and one insert before `if __name__` (the marker
   block). The executor's "14 added lines" is the main()-part count only.
2. **Run `--selftest`.** Both green in the lane: `MADO_COUNTER_SELFTEST: checks=7 failed=0`, rc 0,
   >= 6 checks each; result line on stdout. Fixture break: c1 -> `C1-green-target-met`; c2 ->
   `C2-fixture-parses`; ids are strings, not line numbers. But F1: in the instrument's own layout
   c2 is red (4 checks) because its selftest reads the repository.
3. **Id stability.** Relocated fixture dir and different cwd: identical green line for both. Rename:
   F9. Ids never change because they are hardcoded.
4. **Registry and ledger, independently.** Base registry coverage **1** (only
   `tools/mado-mimetext.py`), not 0; `quality/selftest-kills/check-receipt-presence.json` has 0 rows
   at base. Ledger: `population=188 ledger_rows=188 uncovered=0 dangling=0 bad_pointer=0
   verdict=TARGET_MET` rc 0 at base, with both counters present as rows 225-226 of
   `quality/tool-ledger.md` -- clause (v) is already true at base and does not move.
5. **Predicate attack.** Stub vs real: a stub counter is rejected (`negative_ids=3/14`,
   `broken_c1=0/3`) because it carries no `find` anchor, but the declared always-OK control is
   vacuous (F5). Panel ids: all 16 name ids the counters print, with two duplicate ids and two
   non-single-check edits (F7). Broken modes: distinct at the rc/id level once the panel is
   corrected (F2 last paragraph), but the runner's `wrong-rev`/`mutated-tool` are fixture
   truncation/appending, not a wrong revision or a mutated tool, and their id sets overlap heavily.

## Predicate clause-by-clause (final bytes)

| clause | state |
|---|---|
| (i) green, rc 0, failed=0, checks >= 6 | HOLDS on the 14:31 bytes: both green in the lane AND in a bare counter+fixtures scene (Delta); the 14:28 c2 revision failed it (F1) |
| (ii) every neutralisation fails with its declared id | HOLDS mechanically (16/16 credited) but non-discriminating (F4) |
| (iii) broken modes, >=3 per counter | FAILS as landed (panel shape, F2); distinguishable with a corrected panel |
| (iv) base bytes refuse (rc 2, 0/2 green) | HOLDS: `base-control rc=2 green=False` for both `[MEASURED]` |
| (iv) always-OK stub flags none | HOLDS trivially; cannot fail (F5) |
| (iv) registry 0 -> 4 | FAILS: base is 1; instrument enforces 1 -> 3; published command cannot measure the base (F3) |
| (v) ledger uncovered 0, both counters present | HOLDS at base already; instrument ignores the ledger's verdict (F6) |

## Residual risk

- Every number is bound to the hashes in the table; the drafts changed seven times during the seat
  and may change again before the freeze. Re-run `stripdiff.py`, the 16 neutralisations and the
  instrument after the L1 freezes the bytes.
- F4 is a property of the predicate, not of these drafts: fixing the checks without adding a
  broken-input clause will pass again with decorative checks.
- `MADO_SELFTEST_FIXTURE_DIR` is an interface element not in Contract 3; if it stays, the contract
  and the registry row must name it and its precedence must be below `--fixture-dir`.

## Verification gaps

- No measurement at a landed revision: the drafts are untracked, so the instrument's `--rev` legs ran
  only against scratch repositories I built (`bcbdc37` base; `c30a1a6`, `7145377`, `3776035`,
  `2925bce` revs). They validate the instrument's logic, not the lane's post-landing state.
- The real panel could only be validated for anchors and ids; the instrument stops at F2's
  SETUP_ERROR, so its per-mode verdicts are not observable as landed.
- No full production invocation of either counter (C1 compiles an oracle and scores hundreds of
  cases): the production-path identity rests on stripping/diffing and, for the broken revision, on
  `symtable`, not on a full run.
