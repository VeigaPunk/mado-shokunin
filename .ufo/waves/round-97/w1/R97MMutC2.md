# R97MMutC2 - C2 control panel for the two selftest-enabled counters

Seat: R97MMutC2 (mutation-tester), round 97, wave w1. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, base revision
`e6152b589c2c6a28426c28263c4bcc3c46398be4` (branch master). Scratch
`/fast/scratch/hyaku/mado-r97/R97MMutC2` (removed before yield).

Owned artifact (draft, for the L1 to land):
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-97/controls/counter-selftest-panel-r97.json`
sha256 `f380e7efb7e654ca63b97cbcaaaf02a432f8543b220ad7f1b2899a456301d9f5`, 16 neutralisation rows
(8 per counter) + 3 broken-mode rows, exactly the shared-contract-3 shape
`{"counters":[{"path","checks":[{"id","find","replace"}]}],"broken":[{"id","mode","expect_exit","expect_line"}]}`.

Bytes the panel was verified against (the C2 selftest-enabled counter drafts owned by R97MExecC2):

| target path | build file | sha256 | lines |
|---|---|---|---|
| `quality/counters/c1-r96-magictext.py` | `.ufo/waves/round-97/build/c1-r96-magictext-selftest.py` | `dd9b5a0ba09dc490e286522e9d4d55d60f04dec4274bf456c0a891fa630f61d6` | 1501 |
| `quality/counters/c2-r96-selftest-kills.py` | `.ufo/waves/round-97/build/c2-r96-selftest-kills-selftest.py` | `d4689f5a43b3bc38ef45a1eca354169cf5de4b91846bed336b8d15c0ae79f7a3` | 568 |

The counters changed several times during the wave; the panel's check-body anchors were re-derived
from these bytes and every row was re-run against them. The C2 counter draft (`build/c2-r97-counter-selftest.py`)
is sha256 `bf5352dc23c0aa57c69b3239d30affcf3ecd375150be3e051526dd477fb62521` (the preceding
revision `7370491c...` had the unsatisfiable always-OK control recorded in F4; the fix is described
in Controls 2).

The two `--selftest` modes report `MADO_COUNTER_SELFTEST: checks=7 failed=0`, exit 0, when the
committed fixture tree is reachable. Fixture resolution is `--fixture-dir > MADO_SELFTEST_FIXTURE_DIR
> --repo > walk-up from __file__/cwd > __file__/../selftest-fixtures`; the current draft's
`run_counter()` sets `MADO_SELFTEST_FIXTURE_DIR`, which is what the rehearsal uses. Without that env
var a lone copy in a flat temp dir returns `...-fixture-could-not-evaluate`, `checks=0 failed=1`,
rc 2 (measured on the same bytes). Check ids are the seven each prints, in order:
`C1-green-target-met, C1-missing-cases, C1-wrong-rev-pin, C1-mutant-mismatch, C1-result-format,
C1-no-scratch-left, C1-fixture-parses` (and the `C2-` equivalents with `C2-missing-panel` in place of
`C1-missing-cases`).

## Method

1. The panel's `find` strings were taken from the build bytes and each asserted to occur exactly
   once before use (the C2 counter re-checks this and prints `find occurs N times` otherwise).
2. Every row was rehearsed by applying `find -> replace` to a byte copy of the counter and running
   `python3 -I counter.py --selftest` from a fresh flat temp dir, exactly like the C2 counter's
   `run_counter` (including its `MADO_SELFTEST_FIXTURE_DIR` child env). The verdict rule is the C2
   counter's own: `rc == 1` and the declared id appears in the combined output.
3. The C2 counter draft's panel rules are unchanged from the revision that was dry-runnable
   in-wave: counters must be exactly the two declared paths, `path` unique, `>=6` checks each,
   check rows carry `id/find/replace`, broken rows carry `id/mode/expect_line` plus an int
   `expect_exit` and a mode in `missing-input|wrong-rev|mutated-tool` (read at lines 186-230 of the
   draft). The current draft cannot be dry-run at the base revision any more because it materialises
   the round-97 fixture tree at `--rev` and the base revision has none: it exits 2 with
   `no .ufo/waves/round-97/selftest-fixtures* tree at --rev`. The previous draft revision
   (`5bb9a8b625481972bf4e0c6ed0ac331ce9a8e4be061acbd8304ba02eb18aa5b8`) accepted the same panel
   shape at the base revision and reported `broken_modes=3/3`, `base_refuse=ok`.
4. The `.v2.py` sibling (`97783bf8...`) is a different instrument and was not run: it requires
   `counter`/`path` keys on broken rows (see F5) and the fixture tree at `--rev`.

## Panel totals

- counters: 2; neutralisation rows: 16 (8 + 8; contract minimum is 6 + 6 and 12 total).
- rows killed: **16/16**. survivors: **0**.
- broken rows: 3 (one per declared mode).
- baseline (untouched build bytes): both green, `rc=0`, `checks=7 failed=0`.
- do-nothing control (base counter bytes): both rc 2 (measured).

## Per-row verdicts

Each row states the kind of text it neutralises: `prod` = production-path text the check exercises
through `main()`; `check` = the check's own body inside the selftest block (no production text is
observable for that check). "FAIL ids" is the complete list of failing checks the selftest printed,
so coupling is visible.

| # | counter | id (declared FAIL token) | kind | rc | FAIL ids printed | verdict |
|---|---|---|---|---|---|---|
| 1 | c1-r96-magictext | `C1-missing-cases` | check body | 1 | C1-missing-cases | killed |
| 2 | c1-r96-magictext | `C1-wrong-rev-pin` | prod (`setup()` returns 1) | 1 | C1-missing-cases, C1-wrong-rev-pin | killed (coupled) |
| 3 | c1-r96-magictext | `C1-mutant-mismatch` | check body | 1 | C1-mutant-mismatch | killed |
| 4 | c1-r96-magictext | `C1-result-format` | check body | 1 | C1-result-format | killed |
| 5 | c1-r96-magictext | `C1-no-scratch-left` | check body | 1 | C1-no-scratch-left | killed |
| 6 | c1-r96-magictext | `C1-fixture-parses` | check body | 1 | C1-fixture-parses | killed |
| 7 | c1-r96-magictext | `C1-green-target-met` | check body (`line_ok`) | 1 | C1-green-target-met | killed |
| 8 | c1-r96-magictext | `C1-green-target-met` | check body (`find_ok`) | 1 | C1-green-target-met | killed |
| 9 | c2-r96-selftest-kills | `C2-missing-panel` | prod (`cannot read --panel`) | 1 | C2-missing-panel | killed |
| 10 | c2-r96-selftest-kills | `C2-wrong-rev-pin` | prod (panel pin mismatch) | 1 | C2-wrong-rev-pin | killed |
| 11 | c2-r96-selftest-kills | `C2-mutant-mismatch` | check body | 1 | C2-mutant-mismatch | killed |
| 12 | c2-r96-selftest-kills | `C2-result-format` | check body | 1 | C2-result-format | killed |
| 13 | c2-r96-selftest-kills | `C2-no-scratch-left` | check body | 1 | C2-no-scratch-left | killed |
| 14 | c2-r96-selftest-kills | `C2-fixture-parses` | check body | 1 | C2-fixture-parses | killed |
| 15 | c2-r96-selftest-kills | `C2-green-target-met` | check body | 1 | C2-green-target-met | killed |
| 16 | c2-r96-selftest-kills | `C2-missing-panel` | prod (`setup()` returns 1) | 1 | C2-missing-panel, C2-wrong-rev-pin | killed (coupled) |

Coupling notes: row 2 makes every `SETUP_ERROR` path return 1, so `C1-missing-cases` also fails;
row 16 does the same on the other counter, so `C2-wrong-rev-pin` also fails. In both cases the
declared id is present and rc is 1, so the C2 counter's rule is met; neither row is a clean
single-check kill. No row produced a green selftest (the "not independent -> whole selftest green"
fallback of the seat item was not needed).

## Broken modes (declared by the panel, executed by the C2 counter)

| id | mode | expect_exit | expect_line | observed |
|---|---|---|---|---|
| `missing-input` | missing-input | 2 | `MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR` | rc 2, line present (previous draft revision) |
| `wrong-rev` | wrong-rev | 2 | `MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR` | rc 2, line present (previous draft revision) |
| `mutated-tool` | mutated-tool | 2 | `MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR` | rc 2, line present (previous draft revision) |

Result line of the dry run at the base revision with draft `5bb9a8b6`:
`MADO_COUNTER_SELFTEST_COUNT: TARGET_MISSED ... counter_pin=ok,ok selftest_green=0/2 checks=0,0
negative_ids=0/16 broken_modes=3/3 base_refuse=ok always_ok_flagged=5 ...`.
The three broken rows are the runner's own constructions (missing panel file, nonexistent 40-hex
rev, pinned counter bytes with a trailing `# mutated`), so the expected exit and line are the
runner's setup-error paths, not the counters' behaviour. The current draft (7370491c) keeps the
same mode construction and validator rules for the panel and additionally materialises fixtures at
`--rev`; that is why it cannot be dry-run at the base revision.

## Controls

1. Do-nothing control (base counter bytes, no `--selftest`): measured on the current tree.
   `python3 -I quality/counters/c1-r96-magictext.py --selftest` -> rc 2 (argparse refuses);
   `python3 -I quality/counters/c2-r96-selftest-kills.py --selftest` -> rc 2. 0/2 green, as the
   predicate requires.
2. Always-OK stub: the plain stub prints `MADO_COUNTER_SELFTEST: checks=6 failed=0` and exits 0
   without running a check (measured rc 0, parsed `(6,0)`). Declared expected count: the stub must
   be credited with **0** of the 16 neutralisations (`always_ok_flagged == 0`, and with the current
   draft also `stub_uncredited == 16/16`).
   History: in the preceding draft revision (`7370491c`) this control was unsatisfiable
   (`stub_flagged = st_rc == 1 or (st_st and st_st[1] != 0) or chk["id"] in st_out`;
   `if not stub_flagged: always_ok_flagged += 1`; `met` required `always_ok_flagged == 0`), so a
   well-formed stub was never flagged and the counter reached 16/16. The current draft
   (`bf5352dc`, lines 336-341 and 460-461) replaces this with the v2 echo stub plus an anchored
   credit rule: the stub prints the result line and the panel ids at exit 1, and a row credits the
   stub only when the stub's own bytes carry that row's `find` anchor exactly once. The stub bytes
   carry no anchor, so `always_ok_flagged` stays 0 and `stub_uncredited` counts every row; `met`
   requires both. Measured on the old logic: `stub_flagged(C1-missing-cases)=False`,
   `stub_flagged(C2-missing-panel)=False`. The `.v2.py` sibling has the equivalent inverted rule.
3. Empty panel: rejected by the C2 counter at setup (`<6` checks per counter, `panel_total < 12`),
   which is the correct refusal.

## Findings (for the L1; none is a reason to change the frozen contract)

**F1 - 12/16 neutralisations are check-body edits, not production-path neutralisations.** The
selftest's checks mostly assert source literals or fixture shape, so no production edit can make
them fail: `C1/C2-result-format` counts a needle in its own source; `C1/C2-no-scratch-left` lists
the fixture dir for a prefix the selftest never creates; `C1/C2-fixture-parses` is a parse-only
function returning True; `C1/C2-green-target-met` asserts fixture dict shape and a dummy-tool text
count. These rows prove the check body can fail, not that the counter can. Only 4 rows (2, 9, 10,
16) exercise the counters' production paths.
**F2 - check names overstate what is exercised, and one check no longer tests its own subject.**
`C1-missing-cases` invokes `main()` with `--repo "."` from the temp cwd, so the counter's rev
verification fails first; the check passes on that refusal and the missing-cases guard is never
reached - neutralising the guard changes nothing (measured: the row survives as a production edit),
which is why row 1 is a check-body edit. `C1-wrong-rev-pin` now uses `HEAD~999999` (a genuine
refusal), but `C1-green-target-met` still never runs a green production path, and
`C2-no-scratch-left` cannot observe scratch removal because the selftest never creates a `c2r96-`
or `c2-selftest-` dir in the fixture tree.
**F3 - `selftest` fixtures are cwd/repo coupled.** Checks pass `--repo "."` and `--rev HEAD`, so
they depend on where the counter is run; they are not hermetic fixtures.
**F4 - the named C2 counter's always-OK control was unsatisfiable (resolved in the current draft).**
In revision `7370491c` the predicate conjunct `always_ok_flagged == 0` and the implementation could
not both hold (see Controls 2). The current draft `bf5352dc` replaces it with the anchored echo-stub
rule, so the declared 0 is reachable; the old behaviour and the old sha are kept here as the
correction record. The `.v2` sibling carries the equivalent rule.
**F5 - schema divergence in `.v2.py`.** It requires `counter` on every broken row, a relative
fixture `path` on `mutated-tool` rows, and >=3 broken rows per counter, and its CLI adds
`--base-rev` / `--expect-base-registry-sha256` / `--min-checks`. A panel built to shared contract 3
is rejected by it. If the L1 freezes `.v2.py`, the panel must be extended with per-counter rows
(`c1-`/`c2-` ids, `counter` = the declared path, `path` = a fixture name such as `c1-mutants.json`)
and its `expect_line` must match whatever line v2's scenes produce; v2 cannot be rehearsed in-wave
because it needs the fixture tree at `--rev`.
**F6 - fixture discovery is the load-bearing runner/counter coupling.** On an intermediate revision
(`c1 66b4979c... / c2 dafb7a8b...`) the counters had no fallback and the runner's flat temp layout
saw `...-fixture-could-not-evaluate`, rc 2 for both, which turns the whole panel into survivors.
The current draft sets `MADO_SELFTEST_FIXTURE_DIR` and the current counter bytes resolve the tree
under it, so the panel verdicts above are measured on the runner's actual invocation. A later edit
that drops the env hook or moves resolution back to `__file__`-only will silently un-measure the
whole panel.

## Evidence and restoration

- The build files were never written by this seat. The panel rehearsal applied every edit to
  temporary copies under the scratch root; the build-file sha256 values before and after the
  rehearsal are identical to the table above.
- The panel file is the only lane artifact written; its sha256 is `f380e7ef...` and it parses as
  `{"counters":[2 x {"path","checks":[8]}], "broken":[3]}` with only the contract-3 keys.
- Fixture inventory used by the rehearsal (sha256, under `.ufo/waves/round-97/selftest-fixtures/`):
  `c1-cases.json f090273e...`, `c1-mutants.json e5f9d381...`, `c2-kills.json 3ef502bf...`,
  `control-kills.json 305d735f...`, `dummy-tool.py 384055f9...`, `host-list.txt 0c7ebb4a...`,
  `panel.json 2659cb3e...`, `r90-argv.json 5941534b...`.
- No tool installs or upgrades were needed; no host state, network, git index or jj state was
  touched.

## Verdict

Panel complete and rehearsed: 16/16 neutralisations killed with the declared ids, 0 survivors,
both baselines green, both do-nothing controls behind, 3 broken rows declared against the
contract-3 runner construction. Coverage is limited by the counters' selftest design (F1-F3):
12 of 16 rows can only attack the check bodies, so the C2 counter's `negative_ids == panel` result
over this set proves the selftest block is sensitive to its own text, not that the two counters'
production verdict logic is exercised end-to-end. The one instrument-level defect found in-wave (the
named draft's always-OK control) was fixed by the draft owner in `bf5352dc`; the old value is kept
in Controls 2 and F4.
