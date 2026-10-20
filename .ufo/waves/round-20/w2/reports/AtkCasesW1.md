# AtkCasesW1 — partly falsified: 16/17 W wants are exactly what Python/git semantics and the contract demand and match the tip tool; `W-CaseWrapperForms-class-method-instance` is a wrong want that fails at 28c6837 on a true detection, and `W-WrapperCrossCell-r13-verbatim`'s `observed` is not derivable from its own bytes

## Scope and method

Item: attack the precision-suite expectations for the 17 W cases of `CaseWrapperCrossCell`
(8) and `CaseWrapperForms` (9) in `.ufo/waves/round-20/precision/expected.json`; re-scan each
with the 28c6837 and 1f7f995 tools; list every wrong or vacuous expectation.

Lab (all reads/code under /tmp, lane read-only):

```
git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado-r20w2-AtkCasesW1
git -C /tmp/mado-r20w2-AtkCasesW1 remote remove origin      # HEAD a4046a8
git -C <lane> show <rev>:tools/mado-tripwire.py > /tmp/.../tools/tool-<rev>.py
```
| rev | tool sha256 |
|---|---|
| `28c6837` (= `a4046a8`) | `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c` |
| `1f7f995` | `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d` |
| `9c54c56` | `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd` |

Counter: byte copy of `.ufo/waves/round-20/tw-precision.py` at `a4046a8`
(sha256 `bd3bdc23747a6d8f195e69528f532988202db4ab3476d141a8ff46871e42a8e7`) placed at
`/tmp/mado-r20w2-AtkCasesW1/.ufo/waves/round-20/` so its `LANE` resolves to the clone. Case
bytes copied from the lane tree; `git diff --stat f3da504 a4046a8 -- .ufo/waves/round-20/precision/`
is empty, so the tree equals the scored pin. The counter's diff `f3da504..28c6837` is one hunk:
`SUITE_PIN = None` → `"f3da504…"`. No scoring-rule change.

Scans: one `--scan` per case at each rev, plus the counter at three revs.

## Counter measurements (reproduce the ticket's numbers)

| rev | score | passed | P | S | W | H | L |
|---|---|---|---|---|---|---|---|
| `1f7f995` | 1.6571 | 29/175 | 7/66 | 2/17 | **4/22** | 15/52 | 1/18 |
| `28c6837` | 9.8286 | **172/175** | 66/66 | 17/17 | **21/22** | 51/52 | 17/18 |
| `9c54c56` | 6.2857 | 110/175 | 66/66 | 7/17 | 1/22 | 35/52 | 1/18 |

The three failures at 28c6837: `W-CaseWrapperForms-class-method-instance` (W, this report),
`L-AdoptW2-AdvHelperFn-b14`, `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help` (both outside this item).

W passers at `1f7f995` (4): `r13-shape`, `r13-verbatim`, `class-method-instance`,
`async-def-exec-starred`. At `9c54c56` (1): `class-method-instance` only.

## Case-by-case: derived command vs want vs scans

"derived" is the command the fixture's own Python/git semantics produce (static derivation;
no fixture was executed). Rows are `(class, rule, line, evidence)`.

| case | derived command / rule | want | @1f7f995 | @28c6837 |
|---|---|---|---|---|
| W-WrapperCrossCell-r13-shape | `subprocess.run(['pacman','-Q','hyprland'])` → pacman:-Q @2 | exit 1; pacman:-Q@2 observed | rc 1, pacman:-Q@2 **unmarked** | rc 1, pacman:-Q@2 observed |
| W-WrapperCrossCell-r13-verbatim | `run_record('packages',['pacman','-Q','wayland-utils','wayland','wayland-protocols','hyprland'],0)` → pacman:-Q @2 | exit 1; pacman:-Q@2 observed | rc 1, pacman:-Q@2 **unmarked** | rc 1, pacman:-Q@2 observed |
| W-WrapperCrossCell-kw-argv | `argv=['pacman','-Q','hyprland']` → pacman:-Q @2 | exit 1; pacman:-Q@2 observed | rc 0, none | rc 1, pacman:-Q@2 observed |
| W-WrapperCrossCell-check-true | `argv=['sudo','pacman','-S','--needed','hyprland']` → sudo + pacman:-S @2 | exit 1; both @2 observed | rc 0, none | rc 1, both @2 observed |
| W-WrapperCrossCell-two-hop | `pkg_version('hyprland')` → `pacman -Q hyprland` @3 | exit 1; pacman:-Q@3 observed | rc 0, none | rc 1, pacman:-Q@3 observed |
| W-WrapperCrossCell-format-then-run | `sh('pacman','-Qi','hyprland')` → `pacman -Qi hyprland` shell @2 | exit 1; pacman:-Qi@2 observed | rc 0, none | rc 1, pacman:-Qi@2 observed |
| W-WrapperCrossCell-gap-cell | `pkg_files('hyprland')` → `pacman -Ql hyprland` @3 | exit 1; pacman:-Ql@3 observed | rc 0, none | rc 1, pacman:-Ql@3 observed |
| W-WrapperCrossCell-git-commit | `git -C … add -A`; `git -C … commit -m …` @2 | exit 1; git:add + git:commit @2 observed | rc 0, none | rc 1, both @2 observed |
| W-CaseWrapperForms-spawn-kwarg-args | `subprocess.run(args=['pacman','-Q','hyprland'])` → pacman:-Q @1 | exit 1; pacman:-Q@1 observed | rc 0, none (unparsed 1) | rc 1, pacman:-Q@1 observed |
| W-CaseWrapperForms-alias-assign-shell | `run('pacman -Qi hyprland', shell=True)` → pacman:-Qi @1 | exit 1; pacman:-Qi@1 observed | rc 0, none (unparsed **0**) | rc 1, pacman:-Qi@1 observed |
| W-CaseWrapperForms-partial-shell-sudo | `sh('sudo pacman -S --needed --noconfirm wayland-utils')` → sudo + pacman:-S @1 | exit 1; both @1 observed | rc 0, none (unparsed **0**) | rc 1, both @1 observed |
| W-CaseWrapperForms-decorated-cache-param | `pkg_version('hyprland')` → `pacman -Q hyprland` @1 | exit 1; pacman:-Q@1 observed | rc 0, none | rc 1, pacman:-Q@1 observed |
| W-CaseWrapperForms-decorated-lrucache-call | `pkg_info('hyprland')` → `pacman -Qi hyprland` @1 | exit 1; pacman:-Qi@1 observed | rc 0, none | rc 1, pacman:-Qi@1 observed |
| W-CaseWrapperForms-async-def-exec-param | `await pkg_version('hyprland')` → `create_subprocess_exec('pacman','-Q','hyprland')` @1 | exit 1; pacman:-Q@1 observed | rc 0, none | rc 1, pacman:-Q@1 observed |
| W-CaseWrapperForms-lambda-param-argv | `pkg('hyprland')` → `pacman -Q hyprland` @1 | exit 1; pacman:-Q@1 observed | rc 0, none | rc 1, pacman:-Q@1 observed |
| **W-CaseWrapperForms-class-method-instance** | `Runner().run(['pacman','-Q','hyprland'])` → `subprocess.run(argv…)` → **pacman -Q hyprland** @1 | **exit 0; no rows** | rc 0, none (unparsed 1) | **rc 1, pacman:-Q@1 observed — FAIL** |
| W-CaseWrapperForms-async-def-exec-starred | `await run_argv(['pacman','-Q','hyprland'])` → `create_subprocess_exec(*argv)` @1 | exit 1; pacman:-Q@1 observed | rc 1, pacman:-Q@1 **unmarked** | rc 1, pacman:-Q@1 observed |

All 17 `before` fields in expected.json match this measurement (17/17; the counter never reads
`before`, so this is an independent check).

## Findings

### F1 (high) — `W-CaseWrapperForms-class-method-instance` is a wrong expectation that penalises a true detection

- Want: `expected.json:1312` — `want_exit: 0`, `want_findings: []`; `why`: "Control, stated miss: Runner().run([...]) is a method call through an instance; E1 lists def/async def/lambda helpers only and E2 keeps attribute/method calls unflagged".
- Fixture `.ufo/waves/round-20/precision/CaseWrapperForms--class-method-instance.jsonl:1`:
  `class Runner: def run(self, argv): return subprocess.run(argv, capture_output=True, text=True)` /
  `print(Runner().run(['pacman', '-Q', 'hyprland']).stdout)`.
  Python semantics: this **is** a literal spawn of `pacman -Q hyprland`. The row is not a false positive.
- Tip scan (rc 1):
  ```
  cd /tmp/mado-r20w2-AtkCasesW1/cases
  python3 -I ../tools/tool-28c6837.py --scan CaseWrapperForms--class-method-instance.jsonl
  → MADO_TRIPWIRE: findings
    {"counts": {… "package_query": 1 …}, "exit": 1, … "findings": [{"argv0": "pacman",
     "class": "package_query", "command": "pacman -Q hyprland", "evidence": "observed",
     "line": 1, "rule": "pacman:-Q", …}], "lead_findings": 0, "observed_findings": 1,
     "unpermitted": 1}            # unparsed_spawns: 0
  ```
  At `1f7f995` the same file is `MADO_TRIPWIRE: clean`, rc 0, `unparsed_spawns: 1`.
- Counter: this is the **only** W failure at 28c6837 → W 21/22, total 172/175. The ticket's
  "172/175 at 28c6837" holds; the one W point lost is this case.
- The contract is self-contradictory on exactly this shape:
  - E1 (`w1/spec.json` `/context`, also summarised at `SCORECARD.md:1246-1249`): `observed` = a
    call with literal argv to a helper **whose body is visible** "where the argv reaches a
    spawn in that body". `Runner.run`'s body is visible and does reach `subprocess.run`.
  - E2 (`w1/spec.json` `/context`): "attribute/method calls like `' '.join(argv)` stay
    unflagged as before." Read categorically, `Runner().run(...)` must stay clean.
  - The repaired tool's own docstring (`tool-28c6837.py:39`): "an explicit `__init__` and a
    **directly resolved visible class method are followed**." The implementer brief
    (`w1/spec.json` item TwRuleB) required carrying "def/async def/lambda/**class**/import/
    assignment bindings forward". So the tool is doing what its brief asked; the case is
    enforcing the other side of an unresolved E2/E1 conflict.
- The author's own condition for editing was met and not applied. `CaseWrapperForms.md:35`
  records "stated miss"; its §5 says "If a later tool resolves it, this case must be edited,
  with the reason recorded." `TwRuleB.md:70` then says the case was left unchanged and
  *predicted* `pacman:-Q @1 observed`. The prediction was correct (above), no edit was made,
  and the counter hard-pins the suite at `f3da504`, so no edit could change the score.
- `SCORECARD.md:1329` discloses the failure as "case wants a stated miss; the tool now
  resolves the visible method body that spawns — a true detection". *Disclosure is correct*,
  but the accounting still treats it as a missed target rather than as a defective expected
  value: W's registered definition is "real wrapper misses (**want observed**)"
  (`SCORECARD.md:1251`), and this want-clean control is not a W case under that
  definition. Resolution for L1: either (a) record the case as a known-wrong want and report
  172/174 with the exclusion stated, or (b) apply the edit the author pre-authorised
  ("must be edited, with the reason recorded") under a second, disclosed suite pin, recomputing
  the before readings at 1f7f995/9c54c56 as well and keeping the f3da504 reading as the
  historical record, or (c) revert the class-method follow and amend the tool docstring, E1
  and E2 consistently. Leaving the contradiction and counting the case as a precision miss
  is the one option that misstates the evidence.
- Breadth of the behaviour (probes, all rc 1, `observed`, at 28c6837): spawning method reached
  as `Fmt.show([...])` with `@staticmethod`, as `Fmt.show([...])` with `@classmethod`, as
  `Runner().run([...])`, as `r = Runner(); r.run([...])`, and with an explicit `__init__`.
  An inherited method (`class Runner(Base)`) stays clean. So the behaviour is deliberate and
  broad, not an accident of this fixture.

### F2 (medium) — `W-WrapperCrossCell-r13-verbatim`'s `observed` is not supported by the case's own bytes

- Want `observed` @2. The command derivation is fine; the *evidence label* is the problem.
- The fixture's line 1 is a 12-line verbatim prefix of `MadoR13.jsonl:437` (verified: prefix
  True; line 2 is a 4-line prefix of `:470`, True). But that prefix begins:
  ```
  import subprocess, os, shlex, hashlib, time
  proof=root/'.ufo/waves/round-13/evidence'
  ```
  `root` is bound **only** at `MadoR13.jsonl:82` (`root=Path('/home/vgpnk/Projects/shokunin/
  mado-shokunin')`), which the case does not carry; `json` (used later in the def body) is
  also not imported. In the case file's own kernel the cell raises `NameError` at its second
  statement, **before** `def run_record` binds, so the line-2 call cannot run.
- In the real transcript the cell did run (its output is at `MadoR13.jsonl:439`), so the
  real-world claim is sound; the defect is the de-contextualised fixture.
- E1 requires `observed` to mean "the scanned transcript states the command **and the path
  that runs it**". The path is broken in the scanned file. Under the narrower textual clause
  ("a helper whose body is visible in the scanned transcript") the label is defensible.
  [INFERENCE] L1 must decide which reading governs; if execution reachability governs, this
  want is wrong and the case needs its binding (or a `lead` want, matching the frozen
  `r13-root.jsonl:4`, which the tip correctly reports as `lead` — see Confirmations).
- Compounding: this is a control whose `before: pass` at 1f7f995 came from an **unmarked**
  rule-B row, so its pre-repair pass does not demonstrate the body-visible resolution the
  `why` claims.

### F3 (low, vacuity) — three observed-case "controls" cannot fail at 1f7f995 for the property they name

At `1f7f995` these three print rows with **no `evidence` key**, and the counter maps unmarked
to `observed` by the registered rule (`SCORECARD.md:1248-1249`):

| case | @1f7f995 row | why this is vacuous pre-repair |
|---|---|---|
| r13-shape | `pacman:-Q@2` unmarked | passes identically to a resolved `observed` row; cannot distinguish rule B from helper resolution |
| r13-verbatim | `pacman:-Q@2` unmarked | same |
| async-def-exec-starred | `pacman:-Q@1` unmarked | same; its report label "control" understates that its pre-pass is the round-19 defect being repaired |

They are still useful as **provenance guards** (they fail if the tip demotes to `lead`), and
their post-repair rows are genuinely `observed`. But their `before: pass` must not be read as
"this shape already worked", and they cannot contribute evidence for the repair.

### F4 (low, correlation) — case count overstates independent evidence

- `r13-shape`, `kw-argv`, `two-hop` have **byte-identical** line-1 cells
  (sha256 `fe650434f354c526…` of the code string: `import subprocess\ndef run_record(name,
  argv, rc, **kw): …`); `two-hop` differs only in its later cells. `check-true` is the same
  binder shape with an added `check=True` and an all-keyword call (different bytes,
  `9423958aa8f8a4ef…`). So 4 of the 8 CrossCell cases rest on one helper binder.
- `decorated-cache-param` and `decorated-lrucache-call` are the same body and mechanism; only
  the decorator AST node differs (`Name` vs `Call`) and the rule (`-Q` vs `-Qi`). A tool that
  simply ignores `decorator_list` passes both.
- Distinct mechanisms remain ≥ 4 in both seats (CrossCell: cross-cell positional, keyword
  argv, keyword call + `**kw`, shell-string assembly, gap cell, git argv = 6; Forms: keyword
  `args=`, alias, partial, decorated, async def, lambda = 6 plus 2 controls), so the
  admissibility rule is met; only the "6 reds / 7 reds" headlines overstate independence.

### F5 (note) — `r13-shape` is not the real round-13 shape, despite the name and `why`

The real def at `MadoR13.jsonl:437` is `run_record(name,args,expected=None,stdin=None,
extra_env=None,timeout=300)` with no `**kw`; the case `why` says "round-13
run_record(name, argv, rc, **kw)". The wave-1 brief (`w1/spec.json` item
CaseWrapperCrossCell) asserted the `**kw` form *was* the real shape; `CaseWrapperCrossCell.md`
§Findings 2 corrects this and keeps both forms. The verbatim case covers the real one, so this
is a naming/`why` inaccuracy, not a wrong expectation.

## Confirmations (each with the check that would have shown the opposite)

- **Numbers.** `python3 -I .ufo/waves/round-20/tw-precision.py 1f7f995` → 29/175 (1.6571);
  `… 28c6837` → 172/175 (9.8286); `… 9c54c56` → 110/175 (6.2857). P is 66/66 at both the tip
  and the pre-harm baseline. These match the ticket's C1 claims exactly.
- **`before` fields.** Script over the three result JSONs vs `expected.json`: 0 mismatches of
  17. At 1f7f995 the 13 reds fail and the 4 controls pass; at 9c54c56 only
  `class-method-instance` passes. Both authors' `before` tables are accurate.
- **Wants vs semantics.** 16 of 17 wants equal the row multiset the derived command requires
  *and* the tip tool emits (table above). The exception is F1.
- **Observed/lead split.** `python3 -I tools/tool-28c6837.py --scan probes/r13-root.jsonl`
  (frozen `round-19/frozen/inputs/r13-root.jsonl`) → `[('package_query','pacman:-Q',4,'lead')]`,
  while `r13-verbatim` (def present) → `observed`. The distinction the control pins is real;
  at 1f7f995 the frozen line is an unmarked row and at 9c54c56 it is clean, as expected.
- **E2 purity is not broken by the W repairs.** Probes at 28c6837: `def f(argv): return argv`
  called with `['pacman','-Q','hyprland']` → clean; `len(argv)` → clean; `@functools.cache`
  pure body → clean; pure `async def` → clean; `class S: def run(...): return ' '.join(argv)`
  → clean.
- **Alias/partial/keyword/starred.** All resolve at 28c6837 and none do at 1f7f995 except via
  rule B, which is what the W cases claim.
- **Pre-measurement corrections do not touch W.** The corrections amend E4 only (jj
  `--dry-run` snapshotting, git/jj help placement, `git commit --short|--long|-z`, `add -N`,
  `commit -n`). No W fixture invokes help or a dry run: `git add -A` and `git commit -m` stay
  writes, and `pacman -Q*`/`-S`/`sudo` are unaffected. So none of the 17 wants changes under
  the corrections.
- **Pin integrity.** Suite bytes at `f3da504` and `a4046a8` are identical (empty
  `git diff --stat`), and the counter's only `f3da504..28c6837` change is the `SUITE_PIN`
  literal.

## Limits

- No fixture was executed (they spawn pacman/sudo/git); Python/git semantics were derived
  statically from the call shapes and CPython/git signatures already measured in the wave-1
  reports. Nothing here is a runtime observation of the fixtures.
- I ran the precision counter only; no recall, no 20-control-lines run, no existing 11
  suites, no corpus diff, no held-out set, no isolation/tally checks (other seats/items).
  Consequently I confirm 172/175 but not C1's guard list.
- The F1 breadth probes (staticmethod/classmethod/instance-variable/explicit `__init__`/
  inherited) are synthetic shapes I wrote, not corpus occurrences.
- [UNK] whether L1 intends E2's "attribute/method calls … stay unflagged" as categorical or
  only as the pure-callee example; both readings are quoted and they lead to opposite
  verdicts for F1.
- [UNK] whether the *frozen* replay of `r13-root.jsonl` is rescored for round 20 (the ticket
  says the round-19 frozen replay is recorded); the `lead` row above is the whole-file scan.
- The class-method fixture has no `reset` marker and its row is `observed` at `line 1`; the
  counter's file renaming (`case.jsonl`) does not affect the comparison.

## Installs

none
