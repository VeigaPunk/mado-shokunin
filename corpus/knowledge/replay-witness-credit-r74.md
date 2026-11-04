---
source: S450 (CPython 3.14.8 library reference, `secrets.token_hex`); own-work — `.ufo/waves/round-74/{claims-declaration-r74.md,controls/c1-replay-cases-r74.json,control-baseline-r74.txt,measurement-c1-r74.txt}`; held S441 (the exit-status vocabulary) and S444 (the result object's pass/fail read) stand behind the round-72 arithmetic the successor keeps
verified-at: `b73db773aaf67c9b26c8cf1a4cd567dec3af11f4` (round-74 rule and counter; measurement in `.ufo/waves/round-74/measurement-c1-r74.txt`)
recheck: `python3 -I quality/counters/c1-r74-replay-witness.py --repo . --rev <rev> --base-rev bd5a971532f37df85a78f6f566dd1e649b79de11 --controls .ufo/waves/round-74/controls/c1-replay-cases-r74.json --scratch-root DIR` — `cases=12 correct=12 base_correct=8 verdict=TARGET_MET`
---

# The credit rule's replay limit, closed on the rule: a challenge the run must echo (round 74, C1)

## 1. The gap this round closes

Rounds 71–73 state the landing kill credit's limit in their own words: the rule bounds the
summary to the run's own `SELFTEST FAIL` lines, "it does not authenticate them — a captured
summary replayed with its own matching detail lines remains byte-indistinguishable from a genuine
run." The consequence was measured this round: the held round-72 `credit(out)` on the frozen
twelve-case set scores **8/12** and credits all four replay modes
(`.ufo/waves/round-74/control-baseline-r74.txt`).

The successor closes that limit on the rule, not on the fixture: the caller generates a per-run
challenge and hands it to the child; the child echoes it in a `MADO_LANDING_WITNESS: <16 hex>`
line; the credit requires the last parsed witness to equal the challenge. A block captured from
an earlier run carries an earlier challenge, so it cannot pass.

The witness's shape is sourced: CPython 3.14.8 `secrets.token_hex` returns "a random text string,
in hexadecimal. The string has *nbytes* random bytes, each byte converted to two hex digits."
(`Doc/library/secrets.rst:80-81`, row S450) — 8 bytes give the 16 hex characters the grammar
matches, and a captured block cannot contain the current challenge.

## 2. The rule, frozen

`quality/counters/c1-r74-witness-rule.py:credit(out, nonce)` is true iff **both** hold:

1. the round-72 arithmetic: the last parsed
   `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed` line reports `n > 0` and `p < n`,
   and the run's own `SELFTEST FAIL <i>: ` lines number exactly `n - p`;
2. the witness: the last parsed `MADO_LANDING_WITNESS: <16 lowercase hex>` line equals `nonce`.

Both captured streams are read (the round-71 rule, unchanged); a malformed trailing summary or
witness line neither wins nor hides the last parsed one.

## 3. The twelve-case set and what separates what

`.ufo/waves/round-74/controls/c1-replay-cases-r74.json` (sha256 `17c95774…`), one real `bash`
child per case, each a copy of the landing-counter fixture with the frozen zero-citation clause
deleted once (the harness's own M-Z mutation). The eight round-72 modes are carried by name and
expectation; the four replay modes are new.

| case | class | expect | held round-72 rule | successor | what refuses it |
|---|---|---|---|---|---|
| liar-success | carried | pass | pass | pass | arithmetic holds (1/2, one fail line) and witness present |
| stderr-genuine | carried | pass | pass | pass | both streams read; witness on stderr |
| liar-kill | carried | fail | fail | fail | `p == n` on the last summary |
| crash-stderr | carried | fail | fail | fail | no summary at all |
| bare-failing | carried | fail | fail | fail | summary shortfall 2, zero fail lines |
| mismatch-detail | carried | fail | fail | fail | summary shortfall 2, three fail lines |
| last-wins-pass | carried | fail | fail | fail | last summary is `2/2` |
| last-wins-fail | carried | pass | pass | pass | last summary `1/2` with one fail line; witness present |
| replay-captured | replay | fail | **pass** | fail | witness is the stale nonce `0123456789abcdef` |
| replay-no-witness | replay | fail | **pass** | fail | no witness line |
| witness-mismatch | replay | fail | **pass** | fail | witness `deadbeefdeadbeef` is not the challenge |
| witness-last-wins | replay | fail | **pass** | fail | the last witness is the wrong one |

Measured at `b73db773…`: `cases=12 correct=12 base_correct=8 verdict=TARGET_MET` rc 0
(`.ufo/waves/round-74/measurement-c1-r74.txt`). The do-nothing control (the round-72 harness's
`credit` at `bd5a9715…`) credits exactly the four replay cases — the 8/12 in the same receipt.

## 4. What this does and does not claim

- **It claims** the rule can now refuse a captured block replayed with its own matching detail
  lines, proven on twelve real children with a challenge generated per run
  (`secrets.token_hex(8)`, never the frozen stale value).
- **It does not claim** the challenge authenticates the assertions: a child that echoes the
  challenge and reports arithmetic it did not perform still passes the arithmetic check. The
  witness authenticates the run's echo, not the truth of the report.
- **It does not claim** fault coverage: twelve fixture modes are a bounded set, and the counter's
  own selftest does not claim a real child behaves as the fixture says — the measurement runs the
  children.
- **Wiring is open**: the successor ships as a standalone instrument; the frozen round-72 harness
  is not edited this round, so the live landing chain still uses the round-72 rule. A later round
  that wires it must carry its own red-before receipt (QUALITY 116).
- **Replay of a live challenge** is out of scope: the rule compares tokens; it does not prove the
  token was not observed in transit.
