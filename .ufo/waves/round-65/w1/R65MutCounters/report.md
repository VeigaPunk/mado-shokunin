# R65MutCounters — seat report (mado round-65, w1)

Mutation-tester, leaf. Attacked the two new round-65 instruments on copies in
`/fast/scratch/hyaku/mado-r65/w1/R65MutCounters/`; the drafts were read-only. Full evidence and the
per-mutant table: `mutations.md` (this dir) and `evidence/`.

## Tested bytes (final, re-checked at write time)

| target | sha256 | detector |
|---|---|---|
| `c1-r65-register.py` (C1 counter) | `2ccedc6852a35a8cfbaaf8a92b1ad473c1464499cc892fa8753dc199eaaa1871` | 11-fixture git matrix + base control |
| `landing-counters.sh` (C2 instrument) | `c12b72e20cfaeb92e7ff242b26f2a26eecd6184610e78287fb7b326a30fd5e9a` | its own `--selftest` (baseline 19/19, rc=0) |

Both drafts were mid-iteration when first picked up: an earlier instrument revision (`55d39b6f…`)
failed its own selftest **18/19** (`a15 selftest scratch removed on exit`; `SW: unbound variable`
in the EXIT trap). The executor replaced it; the full battery was re-run on the final bytes above,
and both draft shas matched at write time. The early-revision failure is recorded as an in-wave
defect, not charged against the final bytes.

## Verdict — do the new instruments fail loudly under mutation?

- **C1 counter: yes.** 9/10 mutants killed; the one survivor (M2, `rows >= 8` → `>= 7`) is
  provably equivalent because 7 rows can never carry 8 distinct group cells — the `rows` leg is
  redundant with `groups == 8`. Every frozen clause is independently discriminating: exact group
  equality (M6), required-group set (M10), gate substring (M4), receipt resolution (M5),
  rev-only read (M7), exit code (M8), sentinel boundary (M9), row threshold (M1). Important
  qualifier: the claim's single base-rev control kills **none** of the ten mutants (all return at
  the pre-predicate `block is None` branch). Discrimination came entirely from fixtures built for
  this seat, which do not exist in the lane.
- **C2 instrument: only partly.** 5/9 mutants killed (`I2` rc-via-tail, `I3` `&&`→`||`, `I4`
  exit 0, `I5` /tmp guard, `I6` symlink guard). Four survivors, two of them fatal:

  | survivor | what it does | evidence |
  |---|---|---|
  | `I1` leg skipped with `rc=0` | selftest 19/19 rc=0; at rev `cb63ab13…` pristine is **RED rc=1** (citecheck=1) while the mutant prints **GREEN rc=0** claiming `citecheck=0` without running it | `evidence/probe-I1.log` |
  | `I7` default citecheck tree redirected to round-64 | selftest 19/19 rc=0; at `cb63ab13…` mutant citecheck is green over `files=21/citations=18/missing=0` (r64) whereas the correct r65 tree is `files=6/citations=10/missing=1` → **GREEN instead of RED** | `evidence/probe-I7.log` |
  | `I8` `--citecheck-paths` with no value accepted | selftest 19/19; pristine refuses rc=2, mutant runs and exits 1 | `evidence/probe-I8-*.log` |
  | `I9` used-by sibling path broken | selftest 19/19; landing at `cb63ab13…` gives usedby rc=2 RED — and the unmutated bytes are equally blind: copying the script where its `../quality/…` siblings do not exist still passes 19/19 | `evidence/probe-I9.log`, `evidence/probe-location-blind.log` |

  Root cause of `I1`/`I9`: `a7` asserts that a `LANDING_LEG <leg> rc=<digits>` line is printed,
  not that the leg's child ran; and a fixture landing is allowed to be red, so a missing child and
  a legitimately failing child look identical. Root cause of `I7`: nothing pins the default
  receipt tree. So for C2, `--selftest` is necessary but not sufficient evidence for the landing
  claim; a landing run at the real rev is still required (the executor's simulated landing covers
  that, but the claim's own counting command runs the selftest first and only then the landing —
  the survivors bite only if the landing run itself is skipped or its default path drifts).

## Defects seen

1. Instrument revision `55d39b6f…` selftest fails 18/19 on pristine bytes (EXIT trap reads a
   function-local `SW` under `set -u`). Fixed at `42f620f1…`/`c12b72e2…`.
2. `landing-counters.sh` selftest is location-blind: 19/19 with all three sibling instruments
   absent. It also cannot see a skipped leg (`I1`) or the wrong default receipt tree (`I7`).
3. C1 counter's `rows>=8` leg is non-discriminating given `groups==8`; a duplicated group row is
   accepted as long as 8 rows exist (`neg-dupgroup` → MET). That matches the frozen predicate but
   means the `rows=` cell alone can hide a duplicate.
4. The base-rev control does not exercise any C1 predicate; a one-command control cannot
   distinguish these mutants.

## Bounds / hygiene

Installs: none. pacman: not invoked. No git mutation in the lane; the two fixture repos/clones
under `/fast/scratch/…` were the only git writes (toplevel asserted before commit). No r56
material opened, no credential-shaped capture, no compositor/session change. Seat writes:
`mutations.md`, `report.md`, `evidence/**` (tested bytes + hashes, both harnesses, all logs).
Scratch `/fast/scratch/hyaku/mado-r65/w1/R65MutCounters/` removed after the evidence copy; the one
`/tmp/mado-r65-selftest-*` directory created by the I5 mutant during its run was removed.
