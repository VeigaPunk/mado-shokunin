# Q37 — population equality: predicate population = counter population (R3 / M25-4)

Status: repaired and exercised red/green against round 26's frozen registration and receipts. QUALITY
criterion 37 is drafted below for the L1 to register; `corpus/QUALITY.md` was not edited by this seat.

## What the assignment was

Round-25 spot-check routed defect 3 (M25-4, `corpus/lessons/round-25-verifier-spotcheck.md:198-205`
§7 item 3; round-26 `registration.md` § "Repairs routed by the round-25 spot-check" R3): encode that a
predicate's population equals its counter's population. Concretely: given the registration and a
counter receipt, the registration sentence's stated total (`cases_pass=N/T`), the receipt's printed
denominator and the receipt's count of `CASE ` lines must be one number.

## Files changed (all new; nothing edited outside these paths)

| path | purpose | provisional sha256 |
|---|---|---|
| `.ufo/waves/round-26/quality/check-population.py` | the check (stdlib only, reads text, writes nothing) | `803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64` |
| `.ufo/waves/round-26/quality/q37-population-red-green.txt` | red/green transcript, every run verbatim with `rc=` | `bac76c5927716b7b30574fb08b4260eec2e532b973b953856c423decfc2ae9f1` |
| `.ufo/waves/round-26/quality/population-fixtures/receipt-c1-green.txt` | synthetic 41-CASE C1 receipt (green) | `45c04c00aea88e1ab71f8eb7c002748fd043bb7e1b7558e883b469ccf111e58f` |
| `.ufo/waves/round-26/quality/population-fixtures/receipt-red-case-removed.txt` | green minus `CASE C39` (40 CASE lines, denominator 41) | `bbbeda734e73bdf3d6f98ac6a56a98335de91614bda143f2740a8af60c62bf8d` |
| `.ufo/waves/round-26/quality/population-fixtures/receipt-red-denominator.txt` | 41 CASE lines, printed `41/42` | `21e47a997ca2e2d8797e518566cd644388a2956481b63ae1f70452e31fff8041` |
| `.ufo/waves/round-26/quality/population-fixtures/registration-red-total.md` | byte-copy of `registration.md` with only `target: cases_pass=41/41.` → `41/42.` | `3cc95b6d37f003aeea6927686cc6de13dcda0cb9646a15ce25fc0a7233527d07` |
| `.ufo/waves/round-26/quality/population-fixtures/receipt-red-selfconsistent-40.txt` | internally consistent shrink: 40 CASE lines, `40/40` | `89043adaa73bde06d09a35b0d69e07b8b7ca915c48078eac33d371cad2625512` |

The hashes are work-window values (QUALITY criterion 7): they bind these bytes before landing and must be
re-cut from `git show <commit>:<path>` at the landing commit.

## Checker behavior

CLI: `python3 -I .ufo/waves/round-26/quality/check-population.py --registration PATH RECEIPT [RECEIPT ...]`.

- Registration parse: blank-line-delimited paragraphs carrying a `**PRED-<id>**` marker; the stated
  total is the denominator of the paragraph's unique `cases_pass=N/T` occurrence. A paragraph naming
  several predicates beside one total, one predicate beside several distinct totals, or a predicate
  stated twice with different totals is exit 2 (cannot attribute the number).
- Receipt parse: lines starting with `PRED-<id>` that contain `cases_pass=N/T` are population
  summaries; `CASE `-prefixed lines are the counter's case lines (round-26 counters print one per built
  case, `c1/count.py:283`, `c2/count.py:219`).
- Agreement: for every summary, `denominator == count(CASE lines) == registered total` for that same
  `PRED-<id>`. A receipt naming a predicate with no registered total is exit 1; a receipt with no
  summary line, a missing file or a registration with no `PRED` total is exit 2. Exit 1 for a
  disagreement, 0 for full agreement; final line is `exit=<n>`.
- It prints one `POPULATION ...` line per leg examined, naming the mismatched legs
  (`legs=case_lines`, `legs=denominator`, `legs=registration_total`), so a receipt is not rejected
  anonymously.

## Evidence (full verbatim transcript: `.ufo/waves/round-26/quality/q37-population-red-green.txt`)

| # | input | result | observed |
|---|---|---|---|
| 1 | round-26 `registration.md` + `receipt-c1-green.txt` (synthetic, 41 CASE lines) | exit 0 | `pred=PRED-C1-r26 cases_pass=41/41 case_lines=41 registered=41 agree=ok` |
| 2 | + `receipt-red-case-removed.txt` | exit 1 | `case_lines=40 registered=41 agree=MISMATCH legs=case_lines` |
| 3 | + `receipt-red-denominator.txt` | exit 1 | `cases_pass=41/42 case_lines=41 registered=41 agree=MISMATCH legs=denominator` |
| 4 | `registration-red-total.md` + green receipt | exit 1 | `case_lines=41 registered=42 agree=MISMATCH legs=case_lines,denominator` (registration leg) |
| 5 | + `receipt-red-selfconsistent-40.txt` | exit 1 | `cases_pass=40/40 case_lines=40 registered=41 agree=MISMATCH legs=case_lines,denominator` — the receipt is internally consistent; the registration total is what catches the shrink |
| 6 | round-26 `registration.md` + committed base C1 receipt `.ufo/waves/round-26/evidence/c1-before-96101be5.txt` | exit 0 | `cases_pass=0/41 case_lines=41 registered=41 agree=ok` |
| 7 | round-26 `registration.md` + committed base C2 receipt `.ufo/waves/round-26/evidence/c2-before-96101be5.txt` | exit 0 | `cases_pass=22/51 case_lines=51 registered=51 agree=ok` |
| 8 | + nonexistent receipt | exit 2 | `verdict=UNREADABLE error=FileNotFoundError` |

Rows 6–7 are the out-of-fixture evidence: both frozen base receipts already carry the population the
registration states (41 and 51), while their pass counts are 0/41 and 22/51 — the check binds population,
not success, exactly the distinction M25-4 was about. Row 4 (`registration-red-total.md`) differs from the
real `registration.md` in exactly one value; the fixture was made by copy and a single field edit.

## Draft QUALITY criterion 37 (not written to `corpus/QUALITY.md`; L1 to register)

```text
37. A predicate's population and its counter's population are one number: for every
    `PRED-<id> ... cases_pass=N/T` summary a receipt prints, the receipt's denominator T,
    its count of `CASE ` lines and the total T stated for the same `PRED-<id>` sentence
    in the registration must be equal, and a receipt naming a predicate with no registered
    total never counts as measuring that population. Check: `python3 -I
    .ufo/waves/round-26/quality/check-population.py --registration
    .ufo/waves/round-26/registration.md RECEIPT` exits 1 on any disagreement and 2 when
    the registration or a receipt cannot be read; green on both committed round-26 base
    receipts (C1 41 `CASE` lines at `cases_pass=0/41`, C2 51 at `cases_pass=22/51`) and on
    a synthetic 41-case receipt, red on fixtures dropping one `CASE` line, changing the
    printed denominator, changing the registration total and shrinking to a self-consistent
    `40/40` (`.ufo/waves/round-26/quality/q37-population-red-green.txt`).
    (lesson: lessons/round-25-verifier-spotcheck.md#7-routed-defects-lane-fixes-next-round item 3)
```

## Limits and risks

- It reads three printed numbers, not execution: it cannot detect a counter that prints one `CASE `
  line per case but duplicates labels (e.g. 41 lines over 40 distinct cases), nor that `cases_pass=N`
  counts the PASSes the tool actually observed. Those remain proposed counter self-tests (R2) and
  receipt checks, not this criterion.
- A registration whose PRED sentence is split across paragraphs (marker and total in different
  paragraphs) reads exit 2, not a pass: fail-closed by design.
- The synthetic green receipt is labelled `seed=synthetic-fixture-not-a-run` and is a fixture; it is
  credited only for the shape, with rows 6–7 supplying real-receipt evidence.
- No counter, harness, `tools/`, `corpus/QUALITY.md` or other lane file was edited; the check runs no
  oracle/Hyprland and reads only text. Nothing was installed or upgraded (no package transaction).
- Sibling artifacts (`check-control-receipts.py`, `q36-fixtures/`) appeared under
  `.ufo/waves/round-26/quality/` during this seat; they are not mine and were not touched.

## Commands run (all from `/home/vgpnk/Projects/shokunin/mado-shokunin`)

```text
python3 -I .ufo/waves/round-26/quality/check-population.py --registration .ufo/waves/round-26/registration.md <receipt>   # 8 runs, transcript above
sha256sum .ufo/waves/round-26/quality/check-population.py .ufo/waves/round-26/quality/q37-population-red-green.txt .ufo/waves/round-26/quality/population-fixtures/*
```

No git/jj write command was issued; no host compositor, `/dev/dri` node, `/run` or oracle was touched.
