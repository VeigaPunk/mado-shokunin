# w2/LabNotCompared — the landed tool equals the v2 counter's model on 20031 dumps; one OPEN predicate defect in C1

Seat: `LabNotCompared` (leaf executor, w2 wave, mado round 44). Lane: `mado-shokunin`.
Data commit `e46789213830597348fe96a351ae004d10587385`, lane HEAD at run time
`290cddea92a18e2202456db89cb2bb60d9aaacff`.

Objects under test (digests in `receipt-digests.txt`):

| object | sha256 |
|---|---|
| `tools/mado-geometry.py` (working tree = data commit) | `1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4` |
| `quality/counters/c1-r44-geometry-states-v2.py` (PRED-C1-r44-v2) | `0d872405bb41dd88a9265bb46bfd39c7a92d7738d01f9d91927c9a49a0e9977b` |
| `quality/counters/c1-r42-geometry.py` (imported by the counter) | `ed78d6930545aedc1b529f06dd3f9bce0d1ead88832ae3f53a125263a316ff99` |

## 1. Hypothesis and verdict

**Hypothesis.** The landed `tools/mado-geometry.py` equals the v2 counter's model
(`c1-r44-geometry-states-v2.py:96 model_out_states`) in stdout and exit code on ≥ 20000 random
(clients, rules) dumps.

**Verdict: held. 20031 cases, 0 divergences** — `receipt-fuzz-20031.txt`,
`receipt-fuzz-summary.json`. No minimisation was needed because nothing diverged; the honest
negative is the count and the seed (`LabNotCompared-r44-w2`), both recorded in the receipt's
`CASES … seed=` line.

This wave therefore finds **no defect in the landed tool and none in the model's contract
encoding**. It does find a defect in the predicate's *fixture coverage* (§5), reported as an OPEN
predicate defect.

## 2. Method

- The counter is imported with `importlib.util.spec_from_file_location`; `main()` is never run, so
  no sandbox, no git read, nothing in the lane is touched. `model_out_states` is the oracle and
  `old.gen_texts` / `gen_state_clients` (`:197`) supply the counter's own lattice.
- Case mix, 20031 total:
  - 15000 `sgen<i>`: `old.gen_texts` + `c1-r44:197 gen_state_clients`, half of them via
    `--clients -` (stdin), half via a file — the same split the counter's own fixtures use;
  - 5000 `state<i>`: this seat's state-heavy generator, 10 variants cycling — all-state dumps,
    state+tiled, state+agree, state+badsize, duplicate JSON keys (`"fullscreen": 2, "fullscreen": 0`,
    both orders, duplicate `size`/`class`), huge ints (`10**18`, `2**63`, `10**40` sizes;
    `10**30`, `2**64+2` states), every JSON state value type (`true`, `1.0`, `"2"`, `[2]`,
    `{"internal": 2}`, `null`, `0`, `3`, `-1`), unmapped/missing/control-char class states,
    float-rules-only dumps, multi-file last-wins rules, want `0 0`;
  - 31 fixed/analytic cases: the precedence edges (BADSIZE before state, state before TILED,
    AGREE vs NOT_COMPARED, DIFFER with a state), 5-digit vs 6-digit rule arguments, `-0`/`1e0`
    states, a 300-client dump, and the seven bad-JSON shapes.
- Each case: `python3 -I tools/mado-geometry.py --clients … --rules …` in the scratch dir, run
  8-wide with one case directory per thread; comparison is byte equality of stdout plus equality
  of the exit code, and for rc 0/1/3/4/5 an empty stderr (the counter's clause f rule).
- Coverage actually reached (the equality result is only meaningful over this distribution):

| rc | verdict | state segment in the summary | cases |
|---|---|---|---|
| 0 | OK | absent | 3402 |
| 0 | OK | present (state+TILED, state+AGREE) | 676 |
| 1 | DIFFER | present | 2758 |
| 1 | DIFFER | absent | 2043 |
| 2 | SETUP bad_json | absent | 7 |
| 3 | NO_MATCHING_CLIENT | absent | 4734 |
| 4 | NO_SIZE_RULES | absent | 2500 |
| 5 | NOT_COMPARED | present | 3911 |

  7345 cases carry ` maximized=<n> fullscreen=<n>`; 12686 are state-free; every exit code the
  contract defines (0,1,2,3,4,5) is exercised.

## 3. Why equality is expected (static reading, then measured)

- `c1-r44:89 fsmode_of` is `type(f) is int and f in (1, 2)`; `tools/mado-geometry.py:200
  client_fsmode` is `isinstance(f, int) and not isinstance(f, bool) and f in (1, 2)`. `json.loads`
  produces only exact `int`/`bool`, so the two predicates are extensionally equal on the model's
  input domain. Measured over 29 JSON state values plus the absent key: 0 mismatches
  (`receipt-predicate-crosscheck.txt`), and the same cross-check for the size predicate
  (`tools/mado-geometry.py:192 client_size` vs the model's inline test) over 21 values: 0
  mismatches.
- The state segment is built at `c1-r44:166` and `tools/mado-geometry.py:277` with the same
  format string, the same `> 0` guard, and the same position between `badsize=` and ` verdict=`;
  the verdict chains (`c1-r44:156-161`, `tools/mado-geometry.py:264-274`) list the same five
  verdicts in the same order and give the same exit codes.
- On state-free dumps the v2 model reduces to the round-42 model: 3000 fresh round-42-generated
  dumps, `receipt-stateless-identity.txt` → `mismatches=0 cases_with_state_segment=0`. The
  12686 state-free cases above therefore also confirm the "round-43 output unchanged otherwise"
  arm against the landed tool's bytes.

## 4. Declared domain boundaries (not divergences)

- A clients dump larger than `MAX_BYTES = 1048576` (`tools/mado-geometry.py:86`) makes the tool
  print `MADO_GEOMETRY: SETUP too_large` and exit 2; the model has no file-size notion. Measured:
  a 1400000-byte dump → `SETUP too_large`, rc 2. Dumps are kept under 1 MiB everywhere here, so the
  comparison stays inside the model's domain (largest generated dump ≈ 40 KB).
- `argv`/usage errors and unreadable or non-regular paths are outside `model_out_states` as well
  (the counter scores them through its own `judge`-based fixtures); bad JSON *is* inside the
  domain and agrees (7/7).

## 5. OPEN predicate defect — the top-verdict precedence is not pinned by any fixture

**What it attacks.** The registered contract order at
`quality/counters/c1-r44-geometry-states-v2.py:19-20`:

> verdict is tested in the order NO_SIZE_RULES (rules=0; exit 4) | DIFFER (differ>0; exit 1) | NO_MATCHING_CLIENT

against the counter's fixture set (`:250 FIXED`, plus the `sgen` lattice) and its controls
(`receipts/ctl-c1-v2.txt`).

**Finding.** A tool that tests `NOT_COMPARED` *before* `DIFFER` — the reverse of the registered
order — reaches `TARGET_MET`, every clause 1, 26/26 fixtures, at nonce `2064187c49e2b5f5` on rev
`e467892` (`receipt-mut-blind.txt`, last two lines: `clauses=a:1 b:1 b4:1 b5:1 e:1 g:1 r:1` and
`fixtures=26/26 … verdict=TARGET_MET … nonce=2064187c49e2b5f5`).

The mutant is `mut-not-compared-first.py`: the landed tool with the two branches swapped (landed
`tools/mado-geometry.py:267`/`:271` become mutant `:269`/`:267`) and its own selftest case at
`:464` updated to the mutant's expectation (selftest still 94/94). It is wrong per the contract on
exactly this dump (`receipt-mut-repro.txt`):

```
clients: [{"class":"org.omarchy.gkeep","size":[421,500],"floating":true},
          {"class":"org.omarchy.gkeep","size":[2560,1440],"floating":true,"fullscreen":2}]
rules:   GKCONF (float on + size 420 500)
landed:  … agree=0 differ=1 tiled=0 badsize=0 maximized=0 fullscreen=1 verdict=DIFFER  rc=1
mutant:  … agree=0 differ=1 tiled=0 badsize=0 maximized=0 fullscreen=1 verdict=NOT_COMPARED rc=5
```

**Why a nonce decides it.** A fixture separates the two orders only when it has
`differ>0`, `agree==0` and `maximized+fullscreen>0` at once. The fixed fixtures cannot do it by
construction: every one that carries a state has `differ=0` (`fs0`, `max0`, `maxfloat0`,
`fsagree0`, `fsstdin0`, `fsdup0-0`), and every one with `differ>0` either also has `agree>0`
(`fsmix0` `:259`, `fsmany0`) or carries no state (`fsvals0` `:257`, `fsclient0` `:270`,
`fsdup0-1`). Whether one of the 12 `sgen` fixtures or `fsmany0` — both nonce-derived — lands in
that pattern is therefore a property of the nonce. Measured over 200 deterministic 16-hex probe
nonces per revision (`receipt-nonce-survey-data.txt`, `receipt-nonce-survey-tip.txt`):

| rev | nonces | blinded lattices (no fixture separates the orders) | rate |
|---|---|---|---|
| `e467892` (data commit) | 200 | 53 | 0.2650 |
| `290cddea` (lane tip) | 200 | 41 | 0.2050 |

The same mutant is caught as soon as the lattice samples the pattern: at nonce
`4c2b0c1d0f0e0a0b` it misses on `sgen2`, `sgen7` and `sgen10` (`rc=5 want=1`),
`fixtures=23/26 verdict=TARGET_MISSED`, with every other clause still 1
(`receipt-mut-sensitive-nonce.txt`). Nothing about the mutant changes between the two runs — only
the nonce, which is why this is a coverage hole and not a scoring bug.

So this defect class passes the counter with probability ≈ 0.265 at the data commit and ≈ 0.205 at
the tip, instead of 0. The control set does not cover it: none of the 18 variants in
`receipts/ctl-c1-v2.txt` reorders the top verdicts, and `K01`–`K16` also fail clause **b** (`b:0`),
i.e. their selftests were never updated, so their fixture misses are not what made them miss; the
two ported cheats `X1`/`X2` keep the contract order and are caught by `e`/`b5` only.

**Not an attack on the landed data.** The landed tool takes the registered order
(`tools/mado-geometry.py:267` before `:271`), and `receipts/c1-after-data.txt` ends
`fixtures=26/26 … verdict=TARGET_MET … nonce=65b72cf3b24db2b4`. Nothing here asks for
re-registration after data; the defect is that the predicate's discrimination against a
*contract-violating* tool is nonce-dependent.

**Closure the L1 could land (candidate, its call).** One fixed fixture of the shape the tool's own
selftest already uses at `tools/mado-geometry.py:463-464` — a state client plus a `DIFFER` client
and no `AGREE` client:

```
("fsdiffer0", one("fsdiffer0", [G([421, 500]), G([2560, 1440], 2)])),
```

With it, the model's output (`differ=1 … fullscreen=1 verdict=DIFFER`, rc 1) differs from the
mutant's on every nonce, so the precedence stops riding on the lattice. (Counted, not landed: a
fixture count change would move `TOTAL`, which only the L1 integrates.)

## 6. Reproduction

```
S=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/w2/LabNotCompared
# 20031-case differential fuzz (≈70 s at 8 workers)
python3 -I $S/fuzz-c1.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
  --work /fast/scratch/hyaku/mado-r44/LabNotCompared/fullwork \
  --n-base 15000 --n-state 5000 --workers 8 --dump $S/receipt-fuzz-summary.json
# predicate cross-check and state-free reduction
python3 -I $S/predicate-crosscheck.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I $S/stateless-identity.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin
# the defect: score the mutant at a blinded nonce (expect TARGET_MET)
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r44-geometry-states-v2.py \
  --repo . --rev e46789213830597348fe96a351ae004d10587385 --tool $S/mut-not-compared-first.py \
  --nonce 2064187c49e2b5f5 --work /fast/scratch/hyaku/mado-r44/LabNotCompared/c1work
# blink rate of the lattice (blind = no fixture separates DIFFER from NOT_COMPARED)
python3 -I $S/nonce-survey.py --repo . --rev e46789213830597348fe96a351ae004d10587385 --nonces 200
```

## 7. Receipts (all in this seat directory)

| file | proves |
|---|---|
| `receipt-fuzz-20031.txt`, `receipt-fuzz-summary.json` | 20031 cases, 0 divergences, seed, coverage table |
| `receipt-predicate-crosscheck.txt` | fsmode 29 values + absent and size 21 values: 0 mismatches |
| `receipt-stateless-identity.txt` | v2 model == round-42 model on 3000 state-free dumps |
| `receipt-mut-blind.txt` | the reordered mutant scores TARGET_MET, all clauses 1, 26/26, at nonce `2064187c49e2b5f5` |
| `receipt-mut-sensitive-nonce.txt` | the same mutant misses 23/26 at nonce `4c2b0c1d0f0e0a0b` — the nonce, not the tool, decides |
| `receipt-mut-repro.txt` | the 5-line dump where landed and mutant disagree (DIFFER/1 vs NOT_COMPARED/5) |
| `receipt-nonce-survey-data.txt`, `receipt-nonce-survey-tip.txt` | 53/200 and 41/200 blinded lattices |
| `receipt-digests.txt` | sha256 of tool and counters, at HEAD and at the data commit |
| `receipt-quote-check.txt` | computed locators for the quoted contract sentence and the tool lines |
| `fuzz-c1.py`, `nonce-survey.py`, `predicate-crosscheck.py`, `stateless-identity.py` | harnesses (read-only; write only into `--work`) |
| `mut-not-compared-first.py` | the mutant scored in `receipt-mut-blind.txt` |

## 8. Safety, tools, scratch

- No file outside this seat directory was written; no mutating git/jj command was run (only
  `rev-parse`, `status --porcelain`, `show`), no lane file edited, no compositor/pacman action.
- Tools installed or updated: none.
- Scratch `/fast/scratch/hyaku/mado-r44/LabNotCompared/` is deleted at the end of this seat; the
  files cited above live in this seat directory, not in scratch.
