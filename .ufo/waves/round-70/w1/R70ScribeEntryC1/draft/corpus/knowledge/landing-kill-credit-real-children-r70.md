source: S441 — CPython 3.14 documentation (rendered): `subprocess`, `CompletedProcess.returncode` — https://docs.python.org/3.14/library/subprocess.html (page title "Python 3.14.10 documentation"; fetched 2026-11-04 UTC, three byte-identical fetches, sha256 c8a66b3abf91790cea34128c5636c2e27a4b26ade459f7d4f797400da706079f, 207155 bytes, subprocess.html:360-366) — "Exit status of the child process. Typically, an exit status of 0 indicates that it ran successfully." and "A negative value -N indicates that the child was terminated by signal N (POSIX only)." — the ground for reading a nonzero status as a process outcome, not an assertion verdict; with held S435 (GNU Bash 5.3 §3.7.5 Exit Status, bashref.texi:3905-3916) for the multi-cause vocabulary
verified-at: 2026-11-04
recheck: 90d — re-fetch and re-hash the rendered page and the bash-5.3 release tarball; also when the harness's kill-credit line, the fixture-lane template or the frozen three-scenario set changes, when the `MADO_LANDING_COUNTERS_SELFTEST` summary grammar moves, or when docs.python.org re-renders the 3.14 line

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
--scratch-root …` (`:445-447`). The file is byte-frozen: sha256
`9461a059466e723ba0ae88c86dea2fc97eb5f4fdfb15ef6c6646acce69649a73` at the measured content.

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
`b3a6f131abf371ecf64273b65a143478c4b23eaa7acf974ec80e5efebf6e6a7b`) builds a scratch git repo
and runs both harnesses against three real `bash` children — no scripted stand-in. The children
are extracted at `--rev` from the lane itself (`c3-r56-used-by.py`, `check-tool-ledger.py`,
`mado-receipt-citecheck.py`), so the fixture holds copies of real lane files:

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

Measured at content `6a25e865` (`.ufo/waves/round-70/measurement-r70.txt` § C1; the same values
were measured at `5adba5a9`), the candidate harness and the held one run against the same
fixture:

| mode | child rc | summary | r70 `mz=` (candidate) | r69 `mz=` (base) | correct | base correct |
|---|---|---|---|---|---|---|
| genuine | 1 | `1/2` | `pass` | `pass` | yes | yes |
| crash | 2 | none | `fail` | `pass` | yes | no |
| garbage | 1 | `??? assertions passed` | `fail` | `pass` | yes | no |

Last line, exit 0:

    MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=1 verdict=TARGET_MET rev=6a25e865...

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
- The credit is still presence-based: a summary that parses with `p < n` is credited even if
  the failing assertion is unrelated to the frozen clause. The harness's M-Z recipe and the
  child's own summary are the only join.
- The selftest is hermetic and spawns nothing (`:41-44`): it drives the decision functions and
  the template's structural invariants, and does not claim a real `bash` child behaves as the
  fixture says. The measurement is what runs the children.
- The `base_correct=1` leg says the held harness is wrong on these inputs; it does not
  characterize the held harness elsewhere.

## 5. The sourced ground (`[INF-docs]`, S441 rendered + held S435)

`CompletedProcess.returncode`, rendered page (S441, fetched 2026-11-04 UTC; sha256
`c8a66b3abf91790cea34128c5636c2e27a4b26ade459f7d4f797400da706079f`, 207155 bytes, 2032 lines;
three fetches byte-identical):

> "Exit status of the child process. Typically, an exit status of 0 indicates that it ran
> successfully." (S441:362-363)

> "A negative value ``-N`` indicates that the child was terminated by signal ``N`` (POSIX
> only)." (S441:364-365)

The same page states the rule again for `Popen.returncode`, adding the shell mapping
(subprocess.html:1176-1181: a negative value is a signal death; under `shell=True` the code is
the shell's, which "may map signals to codes such as `128+N`"), and its `getstatusoutput`
examples show two ordinary nonzero causes that are not assertion outcomes —
`(127, 'sh: /bin/junk: not found')` at subprocess.html:1751 and `(-15, '')` at
subprocess.html:1753.

Held S435 supplies the multi-cause vocabulary from the Bash manual (fetched from the bash-5.3
release tarball, sha256 `0d5cd869…` as the registry records; `doc/bashref.texi` sha256
`f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5`, 415804 bytes):

> "So while an exit status of zero indicates success, a non-zero exit status indicates failure.
> This seemingly counter-intuitive scheme is used so there is one well-defined way to indicate
> success and a variety of ways to indicate various failure modes." (S435:3905-3909)

> "When a command terminates on a fatal signal whose number is N, Bash uses the value 128+N as
> the exit status." (S435:3911-3912)

> "If a command is not found, the child process created to execute it returns a status of 127.
> If a command is found but is not executable, the return status is 126." (S435:3914-3916)

The documentary point is narrow and sufficient: a nonzero status records *that the child did
not exit 0*, not *why*. Both pages name causes unrelated to an assertion verdict — a signal
death, a missing program, a non-executable program, the shell's own `128+N` mapping. "Nonzero"
therefore cannot mean "the mutant's assertions failed"; only the child's own summary carries
that. This is why the repaired decision reads the summary and keeps the status as the necessary
second witness.

The raw `Doc/library/subprocess.rst` carries the same `returncode` sentences at :136-142, but
that URL is already `S108` (the `args` claim) and the L1 rejected a second row for it (lesson
`round-70.md` § Gate); `S441` is the rendered page the L1 adopted. Locators in this entry are
therefore `subprocess.html:36x`, not `subprocess.rst:13x` — a table pin at `subprocess.rst:136`
resolves to `subprocess.html` and reports MISS.

## Evidence rows

| id | claim the row grounds | source | locator |
|---|---|---|---|
| K01 | `returncode` is the child's exit status; `0` typically means success. | S441 | subprocess.html:362 |
| K02 | A negative `-N` is a signal death, not an assertion verdict. | S441 | subprocess.html:364 |

S435 is cited in prose with its `bashref.texi` locators (§5), not as a pinned row: the registry
anchor resolves its name as `Exit-Status.html` from the row's URL, while the anchor cell carries
`bashref.texi:` locators, so a table pin to S435 reports `name=Exit-Status.html locators=none
verdict=MISS reason=no-cover` (measured). The propositions it grounds are in §5; the two pinned
rows above carry the sentences the rule actually joins on.

## 6. Recheck and provenance

- Fetch (2026-11-04 UTC, 2026-11-03 local): `curl -sSfL -o subprocess.html
  https://docs.python.org/3.14/library/subprocess.html`, three times, all sha256
  `c8a66b3abf91790cea34128c5636c2e27a4b26ade459f7d4f797400da706079f`, 207155 bytes, 2032
  lines; `<title>` is `subprocess — Subprocess management — Python 3.14.10 documentation`.
- S435 fetch: `https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz`, sha256
  `0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba` (matches the registry
  anchor's recorded tarball digest); `doc/bashref.texi` sha256
  `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5`, 415804 bytes, 11553 lines.
  The registry anchor cites :3902-3906,3911-3916,3925-3928; the zero/nonzero sentence begins
  at :3905 and its trailing clause at :3907-3909, so this entry quotes 3905-3909 (the registry
  range covers the sentence's first two lines, not its last clause).
- Line pins checked against those bytes: `returncode` block subprocess.html:359-366 (sentences
  at 362-363 and 364-365), `Popen.returncode` block 1169-1181, `getstatusoutput` examples
  1743-1753.
- Anchor-cover measurement on a scratch registry copy carrying S441's landed row: the two pins
  above score `rows=2 covered=2 miss=0 verdict=OK`, rc 0. A pin at `subprocess.rst:136` scores
  MISS (`locators=360-366` but the pin line is outside them); a pin to S435 scores MISS as
  described in `## Evidence rows`.
- Instrument pins: r69 harness sha256
  `9461a059466e723ba0ae88c86dea2fc97eb5f4fdfb15ef6c6646acce69649a73`, `mz_killed` at `:452`;
  r70 harness sha256 `71a7b6c45b904a734f194be9a8de6cc2eeb5f5ea1922760f908f5637f1d4db58`,
  `summary_shows_failure` at `:315-330`, the decision at `:478`; counting command sha256
  `b3a6f131abf371ecf64273b65a143478c4b23eaa7acf974ec80e5efebf6e6a7b`, fixture builder at
  `:213`, lane template at `:79`, declared limits at `:46-50`.
- Receipts: `.ufo/waves/round-70/control-baseline-r70.txt:40-51` (§ C1, pre-freeze control);
  `.ufo/waves/round-70/measurement-r70.txt` § C1 at rev `6a25e865` (candidate `mz=pass|fail|fail`,
  base `mz=pass|pass|pass`, `cases=3 correct=3 base_correct=1`, rc 0).
- Row adoption: `S441` is the L1's admitted rendered-page row (`corpus/lessons/round-70.md`
  § Gate). If the L1 renames or re-anchors it, every `S441` and every `subprocess.html:36x`
  locator here moves with it; the anchor must keep the range 360-366 for these two pins.
- Cadence: 90d, plus the on-change triggers named above.
