# Seat MutC2Controls — C2 counter mutation probe (PRED-C2-r40-v1)

Target: `quality/counters/c2-r40-forms-entry.py` (sha256 `b34dd357bbf31472a271fc849909e74bec98f0da265a26ed5ddbfa8df7a843db`),
detector: `.ufo/waves/round-40/ctl/run-c2-controls.py` (sha256 `14ab2f2fe9dab59a2a1ee62c23b13333e41ddbdc83ae2a31507d6afc79ad7aa9`).
Method: pristine counter + 7 single-rule mutants copied to `/tmp/mutc2/` (lane bytes never touched);
each mutant gets a `/tmp` harness copy (`H0`–`H7`) whose `COUNTER` constant is retargeted to it.
One mutation per counter; detector identical in all runs. Scratch disposable, removed after the probe.

## Baseline (pristine)

`H0` (pristine counter, retargeted harness copy): **`CTL_C2: controls=21 correct=21/21`, exit 0** —
P admits 1/1, N01–N20 all reject 0/1. Baseline valid, so every mutant verdict below is conclusive
(a baseline failure would have been inconclusive, not a kill).

## Results: 5 killed, 2 survived (control gaps)

| # | Mutation (one site each, lane line numbers) | Diff | Detector result | Verdict | Killing control |
|---|---|---|---|---|---|
| M1 | drop clause g (`:194`) | `int(d_ok), int(g_ok)` → `int(d_ok), 1` | `correct=20/21`, N10 observed `admitted=1/1` (g:1) | **KILLED** | `N10-entry-line-lacks-quote` |
| M2 | quote word cap 25→40 (`:177`) | `<= 25` → `<= 40` | `correct=20/21`, N05 observed `admitted=1/1` (d:1) | **KILLED** | `N05-quote-26-words` |
| M3 | accept `candidate` status (`:147`) | `cells[7] == "mined"` → `cells[7] in ("mined", "candidate")` | `correct=20/21`, N13 observed `admitted=1/1` | **KILLED** | `N13-status-candidate` |
| M4 | accept opened != 2026-10-25 (`:154`) | `good &= cells[8] == OPENED` → `good &= bool(cells[8])` | **`correct=21/21`, exit 0** | **SURVIVED — control gap** | none (see below) |
| M5 | skip held-row byte-equality (`:150-151`) | drop `and old[0][:10] == cells[:10]` | `correct=20/21`, N08 observed `admitted=1/1` (c:1) | **KILLED** | `N08-held-row-rewritten` |
| M6 | skip gate sha256 compare (`:174-175`) | `if blob is None or … != digest` → `if blob is None` | `correct=20/21`, N03 observed `admitted=1/1` (d:1) | **KILLED** | `N03-gate-sha-wrong` |
| M7 | ignore lesson receipt path prefix (`:171-172`) | remove `if not path.startswith(FETCH): continue` | **`correct=21/21`, exit 0** | **SURVIVED — control gap** | `N14` is the intended control but cannot see it (see below) |

Mutant sha256s (all differ from pristine `b34dd357…`):
M1 `eb6e9310f6ef5b72d10fa82ed63aa5405961d42886ed12cb6bc8b9d2ac19d693`,
M2 `0899fbb2950868d3295646de9daeaeec1148acdd384de9207022af88dd04dfb7`,
M3 `94676f7ddd88764b8fd2f0f1cd0db270d3f678c7573a2ebf7e553dda6d69e4b5`,
M4 `f144531f79be5967081c64ef16d06ee4aa725289a3866eeeaa476146025a2a26`,
M5 `d774f128bc64c145511c3e60ac87980f89e24b50f5eca3b24a8e4a4ae070c75c`,
M6 `d5b56fde220da42691c0cfe3ddf26f9c3910e5a93a2dd51d9eb727a539f8a381`,
M7 `a604da22e4697925c3ea1046967eced0525148bc03590f15f32692d165c77e84`.
`diff` of each mutant vs pristine shows exactly the one site above (verified, nothing else changed).
P passed (admitted=1/1) under every mutant — no mutant broke the positive control.

## Control gap 1 — M4 (clause c new-row `opened` date)

No shipped control ever varies the registry `opened` cell of a new-id row: the harness `row()`
helper pins `opened="2026-10-25"` for every row it emits, `N13` varies only the **status** cell of
that same new-row family, and `N11` varies the entry's `verified-at` (clause b), not clause c's
`opened` cell. So relaxing clause c's date equality is invisible to all 21.

Discriminating probe (fixture = admitted state with S301's row `opened` 2026-10-25 → 2026-10-24,
one-cell change):

```
probeM4  counter=pristine  observed=admitted=0/1  clauses=a:1 b:1 c:0 d:1 e:1 f:1 g:1 h:1  exit=1
probeM4  counter=M4        observed=admitted=1/1  clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1  exit=0
```

Pristine rejects on c, M4 admits — the mutation is behavior-bearing and the shipped set is blind.
The control that should have caught it: a one-cell sibling of N13, e.g.
`N-new-row-opened-stale` = `row(...)` with `opened="2026-10-24"` on one new id (must reject 0/1).

## Control gap 2 — M7 (clause d receipt-path policy) and why N14 misses it

`N14-receipt-outside-fetch` only renames the gate's receipt path to
`.ufo/waves/round-39/fetch/S301.html` **without committing any bytes there**, so the counter
rejects via `blob is None` (existence), not via the FETCH-prefix policy. Replay of shipped N14:

```
N14  counter=pristine  observed=admitted=0/1  clauses=a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1  exit=1
N14  counter=M7        observed=admitted=0/1  clauses=a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1  exit=1
```

Identical signature — N14 cannot distinguish a path-enforcing counter from a path-blind one.
Discriminating probe (gate receipt bytes + sha committed intact at `corpus/receipts/S301.html`,
i.e. outside `.ufo/waves/round-40/fetch/`):

```
probeM7  counter=pristine  observed=admitted=0/1  clauses=a:1 b:1 c:1 d:0 e:1 f:1 g:1 h:1  exit=1
probeM7  counter=M7        observed=admitted=1/1  clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1  exit=0
```

The shipped control that should have caught it and does not: **N14** — its fixture should also
commit the receipt bytes at the outside-fetch path (sha/quote consistent) so rejection is forced
by the path policy; the current bytes-absent variant can stay as a separate existence case.

## Restoration evidence

- Lane counter `quality/counters/c2-r40-forms-entry.py`: sha256 `b34dd357…843db` before == after.
- Lane harness `.ufo/waves/round-40/ctl/run-c2-controls.py`: sha256 `14ab2f2f…d7aa9` before == after.
- `git -C <lane> status --porcelain` on both paths: empty (no modification, no index touch).
- All mutations lived in `/tmp/mutc2/` (H0–H7, M1–M7, probe.py); lane writes were limited to this
  report file. Scratch removed after the probe.

## Tooling

No installs: stock `python3` and system `git` only (no pacman, no downloads).

## Notes for the L1 integrator

Surviving mutants are coverage findings, not contract changes — the C2 counter and its controls
were not modified. If the two gaps are closed (N-new-row-opened-stale; N14 variant with bytes
committed outside fetch/), the control count grows past 21 and the two clause-c/d relaxations
become detectable.
