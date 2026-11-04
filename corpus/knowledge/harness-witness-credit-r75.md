---
source: own-work — `.ufo/waves/round-75/{claims-declaration-r75.md,controls/c1-harness-cases-r75.json,control-baseline-r75.txt,measurement-c1-r75-final.txt}`; `quality/counters/{c1-r75-landing-controls.py,c1-r75-harness-witness.py,c1-r72-landing-controls.py}`; external witness ground S450 (`secrets.token_hex`)
verified-at: `4527fcae6a8619e890172ca0a616ae8a3e20fd87` (the final measured content; freeze body `def73656c94f0e88bd671cfb4a65124338261722`)
recheck: `python3 -I quality/counters/c1-r75-harness-witness.py --repo . --rev <rev> --base-rev b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6 --controls .ufo/waves/round-75/controls/c1-harness-cases-r75.json --scratch-root DIR` — `cases=11 correct=11 base_correct=6 verdict=TARGET_MET`
---

# Witness credit wired into the landing harness (round 75, C1)

## 1. The gap this closes

The round-74 rule left its own wiring open: "the rule ships as a standalone instrument and is
not yet wired into the frozen round-72 harness" (`corpus/lessons/round-74.md` § C1). The held
round-72 harness (`quality/counters/c1-r72-landing-controls.py`, sha256 `b6108c86…`) credits the
M-Z zero-citation mutant on arithmetic alone: the last parsed
`MADO_LANDING_COUNTERS_SELFTEST: p/n` has `n > 0` and `p < n`, and the run's own `SELFTEST FAIL`
lines number exactly `n - p`. A captured report with matching detail lines therefore earns the
same credit as a current run.

## 2. The successor harness

`quality/counters/c1-r75-landing-controls.py` is a generation, not a rewrite. It loads the
frozen round-72 bytes from the measured repository at `--rev`, refuses any bytes whose sha256 is
not the pin, writes them into a private unpredictable directory under the validated scratch root
with `O_NOFOLLOW`, and installs the round-75 rule into that generation's own globals. The
extraction list, the extracted instrument's selftest, the M-Z clause deletion and the M-R
replacement-ref leg are the round-72 code unchanged.

One `secrets.token_hex(8)` challenge is drawn per run and handed to the child in
`MADO_LANDING_NONCE` (the round-74 ground, S450). The M-Z kill is credited only when the held
arithmetic holds **and** the child's last parsed `MADO_LANDING_WITNESS: <16 hex>` line equals the
challenge byte-exactly (either hex case is accepted as a value; equality does not normalise it).
The contract outcome is green only under the same echo, with both mutants killed. The standing
instrument `quality/landing-counters.sh` echoes a well-formed challenge after its summary; with no
challenge in the environment it prints nothing and every held caller keeps its output (verified
62/62 on the amended instrument, critic receipt).

## 3. The eleven frozen fixture modes

Each mode is a real `bash` fixture lane committed into its own scratch git fixture, measured
through the actual harness pipeline; the scored value is the **M-Z credit decision**.

| mode | expected credit | held r72 | successor | what separates it |
|---|---|---|---|---|
| `right` | pass | pass | pass | failing summary, matching detail, exact echo |
| `liar-success` | pass | pass | pass | exit 0 does not override failing arithmetic (same rule-visible path as `right`) |
| `uppercase-echo` | fail | pass | fail | uppercased echo is not byte-exact |
| `stale-witness` | fail | pass | fail | captured old witness |
| `absent-witness` | fail | pass | fail | no parsed witness |
| `wrong-witness` | fail | pass | fail | wrong token |
| `last-wins-wrong` | fail | pass | fail | last parsed witness overrides an earlier exact echo |
| `crash` | fail | fail | fail | no summary |
| `zero-denominator` | fail | fail | fail | `0/0` is not a kill |
| `mismatch-detail` | fail | fail | fail | detail count ≠ summary shortfall |
| `green-mutant` | fail | fail | fail | `2/2` reports no failed assertion |

Measured at `4527fcae`: `cases=11 correct=11 base_correct=6`. The held leg misses exactly the
five witness separators. The pre-freeze do-nothing receipt (`control-baseline-r75.txt`) records
the same 6/11 from the frozen harness alone.

## 4. What the challenge does not authenticate

- It authenticates the **run's echo**, not the truth of the assertions: a child can echo the
  current challenge and invent matching detail lines, and the arithmetic still accepts them.
- A fixed captured witness collides with a fresh 64-bit challenge with probability `2^-64`; the
  separation is probabilistic in that sense, not logical impossibility.
- The frozen modes are separators, not fault coverage. `right` and `liar-success` have the same
  rule-visible behaviour (they differ only in exit status, which the rule does not read), so
  eleven modes carry ten distinct behaviours.
- The `uppercase-echo` separator is probabilistic as an oracle: `token_hex(8)` can draw sixteen
  decimal digits (probability `(10/16)^16 ≈ 5.4e-4` per draw), uppercasing which is a no-op; a
  later denominator should force a case-changing challenge. The frozen label was not re-cut.
- The counter scores the M-Z decision only. The outcome clause is implemented and inspected
  (`green_with_witness`), but the frozen eleven-case denominator does not certify it; a successor
  predicate must score the outcome field itself.
