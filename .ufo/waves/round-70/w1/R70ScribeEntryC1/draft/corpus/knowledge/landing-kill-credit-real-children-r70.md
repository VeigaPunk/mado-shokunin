source: S441 — CPython v3.14.8 `Doc/library/subprocess.rst` (tag v3.14.8, fetched 2026-11-03, sha256 05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd, 61603 bytes) — the return-code vocabulary the kill decision turns on: `returncode` is the child's own exit status, a negative value is a signal death reported as `-N`, and the documented shell examples put a missing program at 127 and a signal death at -15, so a nonzero status names a family rather than an assertion verdict
verified-at: 2026-11-03
recheck: 90d — re-fetch the tag's `Doc/library/subprocess.rst` and re-hash it; also when the landing harness's decision line, the fixture-lane template or the frozen three-scenario set changes, when the `MADO_LANDING_COUNTERS_SELFTEST` summary grammar moves, or when the host python leaves 3.14.8

# Landing kill credit: a parsed failed assertion, not a child exit status (MADO-R70-1)

## Scope

Lane-tooling scope only. This entry explains the decision behind round-70 claim C1
(`claims-declaration-r70.md`, C1 §): when the landing control harness may mark a mutant child
`mz=pass` (a kill), why the round-69 rule `mz_rc != 0` had to be replaced, how three real
`bash` children exercise the decision, and what the resulting `correct=3 base_correct=1` line
does not establish. It is not a desktop claim, not a fault-coverage claim, and not a claim about
the real landing lane's four legs; the fixture lane is the counter's own instrument. Criterion
111(a) (`corpus/QUALITY.md:678-683`) is the shape it has to satisfy: a frozen recipe must change
a printed observable, and here the observable is the `mz=` field of the frozen sentence.

## 1. What round 69 credited (`[OBS]`)

The round-69 harness decided a kill with one expression:

    mz_killed = mz_rc != 0          # quality/counters/c1-r69-landing-controls.py:452

`mz_rc` is `r.returncode` (`:448`) of the child the harness spawns, `bash <mutant> --selftest
--scratch-root …` (`:445-447`). The file is byte-identical at the scored commit `5144a6b5` and
at the measured content `5adba5a9`: sha256
`9461a059466e723ba0ae88c86dea2fc97eb5f4fdfb15ef6c6646acce69649a73`.

Under that line "kill" means only "the child exited nonzero". The pre-freeze receipt shows what
that conflates. All three real `bash` children exit nonzero when the harness deletes the frozen
clause, so all three print `mz=pass`:

| scenario | child rc | summary the child printed | evidence fields | held `mz=` | receipt verdict |
|---|---|---|---|---|---|
| genuine | 1 | `MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed` | `failed_assertions=1 assertions=1/2` | `pass` | correct |
| crash | 2 | none | `failed_assertions=0 assertions=none` | `pass` | INCORRECT |
| garbage | 1 | `MADO_LANDING_COUNTERS_SELFTEST: ??? assertions passed` | `failed_assertions=0 assertions=none` | `pass` | INCORRECT |

`.ufo/waves/round-70/control-baseline-r70.txt:40-51` — `base_correct=1/3`.

The harness was already printing the discriminator and not reading it: its M-Z evidence line
carries the parsed `assertions=<p>/<n>` beside `killed=`, and on the crash scenario that same
line reads `failed_assertions=0 assertions=none killed=yes`. A child that never reached its
assertions, and a child whose summary cannot be parsed, both received the credit that belongs
to a child which ran its assertions and reported one failed.

## 2. The repaired rule (`[OBS]`)

`quality/counters/c1-r70-landing-controls.py` (sha256
`71a7b6c45b904a734f194be9a8de6cc2eeb5f5ea1922760f908f5637f1d4db58`) replaces the single test
with a conjunction at `:478`:

    mz_killed = bool(mz_rc != 0 and summary_shows_failure(mz_out))

`summary_shows_failure` (`:315-330`) is:

```python
line = last_summary(out)
m = re.fullmatch(r"MADO_LANDING_COUNTERS_SELFTEST: (\d+)/(\d+) assertions passed", line)
if not m:
    return False
passed, total = int(m.group(1)), int(m.group(2))
return total > 0 and passed < total
```

with the docstring: "True only when the child's own summary parses AND reports fewer passes than
assertions. `MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed` -> True; `... 2/2 ...` ->
False; a crash (no summary) and a garbled summary -> False. A kill is credited on a failed
assertion, never on a broken child."

The five decision cases the harness's own selftest pins (`:719-727`): `1/2` → failure; `2/2`,
`??? assertions passed`, an absent summary and `0/0` → no failure. The zero-total guard matters:
a vacuous `0/0` is an empty instrument, not a failed assertion. The two new scripted cases go
through the real measurement body (`_measure_case`, `:634`): `mz-crash` (rc 2, no summary,
`:701-708`) and `mz-allpass` (rc 1, `62/62`, `:710-717`) must both print `mz=fail … killed=0/2`.

Both witnesses are necessary. A child that prints a failed summary but exits 0 is not credited
(the status must agree), and a child that exits nonzero without a parseable failed summary is
not credited (the summary must exist). That is the change the frozen sentence prints: under the
held harness crash and garbage print `mz=pass`; under the repaired one they print `mz=fail`, and
`mz=` is the frozen contract's decision token.

## 3. The real-children leg (`[OBS]`)

The counting command `quality/counters/c1-r70-real-children.py` (sha256
`b3a6f131abf371ecf64273b65a143478c4b23eaa7acf974ec80e5efebf6e6a7b` at the measured content)
builds a scratch git repo and runs both harnesses against three real `bash` children — no
scripted stand-in. The children are extracted at `--rev` from the lane itself
(`c3-r56-used-by.py`, `check-tool-ledger.py`, `mado-receipt-citecheck.py`), so the fixture holds
copies of real lane files:

- `build_fixture` (`:213`): `git init -q .`, asserts `rev-parse --show-toplevel` is the fixture
  dir, writes the children and the lane, then makes one commit per mode with an explicit
  identity (`-c user.name=r70-c1 -c user.email=r70-c1@example.invalid -c
  commit.gpgsign=false`) and `-C` on every git call.
- the fixture lane is `LANE_TEMPLATE` (`:79`); it is the frozen
  `.ufo/waves/round-70/proto/fixture-lane.tmpl` text (sha256
  `9e31681dd95976af4b107566b1710a50d962b9af36d3e5db6b73078393c91b6f`) with the mode token
  respelled (`__MODE__` in the proto, `@MODE@` in the template). Its `verify()` carries the
  frozen clause at `:85`:

      [ "$citations" -gt 0 ] && [ "$citations" -eq "$((resolved+missing))" ] || return 1

  The shipped lane carries the same clause at `quality/landing-counters.sh:73`.
- the three modes are driven by that clause's own effect, not by branches keyed to the mode
  name. With the clause present, `verify 0 0 0` returns 1 at `[ "$citations" -gt 0 ]`, so
  `zero=1` and the lane takes the passing branch (`2/2`, rc 0). When the harness deletes the
  clause, `verify 0 0 0` falls through the equalities and returns 0, so `zero=0` and the mode's
  branch decides the child's behavior: `genuine` scores the zero-citation assertion `1` against
  `0` (`1/2`, exit 1); `crash` exits 2 before printing any summary; `garbage` prints
  `MADO_LANDING_COUNTERS_SELFTEST: ??? assertions passed` and exits 1.

Measured at content `5adba5a9` (`.ufo/waves/round-70/measurement-r70.txt` § C1), the candidate
harness and the held one run against the same fixture:

| mode | child rc | summary | r70 `mz=` (candidate) | r69 `mz=` (base) | correct | base correct |
|---|---|---|---|---|---|---|
| genuine | 1 | `1/2` | `pass` | `pass` | yes | yes |
| crash | 2 | none | `fail` | `pass` | yes | no |
| garbage | 1 | `??? assertions passed` | `fail` | `pass` | yes | no |

Last line, exit 0:

    MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=1 verdict=TARGET_MET rev=5adba5a9...

`base_correct=1` is the fixture-health assertion: the held harness must be wrong on exactly the
two broken-child inputs, which is what makes the candidate's two flips a repair rather than a
re-spelling of the same decision.

## 4. Limits — what the counter cannot do (`[INF]` unless cited)

Quoting the counter's own declared limits (`:46-50`): "the scenarios are three fixture lanes,
not a fault-coverage claim; the fixture is the counter's own instrument and is not the lane's
real landing instrument; a harness that always printed `mz=fail` fails the `genuine` case, and
one that always printed `mz=pass` fails `crash` and `garbage`, but the counter cannot tell a
correct decision from a decision that happens to agree on these three inputs."

- The three texts are the counter's instrument. The real lane has four legs and a
  marker-validity rule (`quality/landing-counters.sh:64-75`); the fixture is one function with
  two assertions. A green line here is a statement about the decision under these three
  children, not about the lane's landing behavior.
- Nothing wider than the three cases is proven. A rule that credits a kill whenever the child
  printed any `SELFTEST FAIL` line also scores 3/3 on these texts — genuine prints one, crash
  and garbage print none — so the set does not separate the parsed-fraction rule from a
  line-count heuristic (derived from the frozen template; not measured).
- The selftest is hermetic and spawns nothing (`:41-44`): it drives the decision functions and
  the template's structural invariants, and does not claim a real `bash` child behaves as the
  fixture says. The measurement is what runs the children.
- The `base_correct=1` leg says the held harness is wrong on these inputs; it does not
  characterize the held harness elsewhere.

## 5. The sourced ground (`[INF-docs]`, tag `v3.14.8`)

`Doc/library/subprocess.rst` @ `v3.14.8` (fetched 2026-11-03; sha256
`05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd`, 61603 bytes, 1622 lines;
three fetches byte-identical):

> "Exit status of the child process. Typically, an exit status of 0 indicates that it ran
> successfully." (S441:138-139)

> "A negative value ``-N`` indicates that the child was terminated by signal ``N`` (POSIX
> only)." (S441:141-142)

> "The exit code for the command can be interpreted as the return code of subprocess."
> (S441:1500-1501)

and the two examples that name ordinary nonzero causes:

> `(127, 'sh: /bin/junk: not found')` (S441:1508)
>
> `(-15, '')` (S441:1510)

The documentary point is narrow and sufficient: a nonzero status records *that the child did
not exit 0*, not *why*. The page itself shows two unrelated causes — a missing program (`127`)
and a signal death (`-15`) — the `Popen.returncode` paragraph repeats the signal rule and adds
that under `shell=True` the code is the shell's, which may map signals to `128+N`
(S441:961-963). "Nonzero" therefore cannot mean "the mutant's assertions failed"; only the
child's own summary carries that. This is why the repaired decision reads the summary and keeps
the status as the necessary second witness.

## Evidence rows

| id | claim the row grounds | source | locator |
|---|---|---|---|
| K01 | `returncode` is the child's exit status; `0` typically means success. | S441 | subprocess.rst:138 |
| K02 | A negative `-N` is a signal death, not an assertion verdict. | S441 | subprocess.rst:141 |
| K03 | A shell command's exit code is interpretable as the subprocess return code — the status records the child, not the harness's reading of it. | S441 | subprocess.rst:1500 |
| K04 | A missing program is reported as `127` — an ordinary nonzero cause that is not a failed assertion. | S441 | subprocess.rst:1508 |
| K05 | A signal death is reported as a negative code (`-15`) — a second nonzero cause beside the assertion outcome. | S441 | subprocess.rst:1510 |
| K06 | Under `shell=True` the code is the shell's and may map signals to `128+N`. | S441 | subprocess.rst:961 |

## 6. Recheck and provenance

- Fetch (2026-11-03): `curl -sSfL -o subprocess.rst
  https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst`, three
  times, all sha256 `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd`, 61603
  bytes, 1622 lines; tag `v3.14.8`.
- Line pins checked against those bytes: the `CompletedProcess.returncode` block L136-142, the
  `Popen.returncode` block L949-963, the `getstatusoutput` examples L1500-1510.
- Instrument pins: r69 harness sha256
  `9461a059466e723ba0ae88c86dea2fc97eb5f4fdfb15ef6c6646acce69649a73`, `mz_killed` at `:452`;
  r70 harness sha256 `71a7b6c45b904a734f194be9a8de6cc2eeb5f5ea1922760f908f5637f1d4db58`,
  `summary_shows_failure` at `:315-330`, the decision at `:478`; counting command sha256
  `b3a6f131abf371ecf64273b65a143478c4b23eaa7acf974ec80e5efebf6e6a7b`, fixture builder at
  `:213`, lane template at `:79`, declared limits at `:46-50`.
- Receipts: `.ufo/waves/round-70/control-baseline-r70.txt:40-51` (§ C1, pre-freeze control);
  `.ufo/waves/round-70/measurement-r70.txt` § C1 (measured content `5adba5a9`, rc 0).
- The only change to the counting command after the scored commit is `9508e878`
  (`os.makedirs(scratch, exist_ok=True)` in `run_harness`); it creates the per-scenario
  directory and leaves `EXPECT`, the fixture text and the scoring untouched. [INFERENCE] from
  the commit diff, not a re-measured statement.
- Row id: the entry cites `S441`, the round's new tier-A registry row for the return-code
  paragraph. The URL already has `S108` (scope: the `args` command parameter,
  `corpus/SOURCES.md:120`), but that row cannot carry these pins: `check-anchor-cover.py`
  derives the file name from the *last* URL in a row — for S108 that is `Lib/subprocess.py`, so
  `name=subprocess.py` — and S108's anchor carries no `subprocess.py:` occurrence. A probe row
  pinned to S108 against a scratch copy of the registry reports
  `name=subprocess.py locators=none verdict=MISS reason=no-cover` (measured, `rows=1
  covered=0 miss=1 verdict=FAIL`). `S441`'s anchor is
  `subprocess.rst:136-142,949-963,1500-1510`; the same scratch run with that row reports
  `rows=6 covered=6 miss=0 verdict=OK`. The row draft and the duplicate-URL (W04) decision sit
  in `.ufo/waves/round-70/w1/R70ScribeRowLesson/draft/corpus/SOURCES-row-subprocess-CONFLICT.txt`.
  The L1's adoption row
  in `corpus/lessons/round-70.md` § Gate fixes the id; if a different id is adopted, every
  `S441` here and in the Evidence rows table moves with it. Without that row the six evidence
  rows have nothing to resolve against, and `check-anchor-cover.py` cannot pass.
- Cadence: 90d, plus the on-change triggers named above.
