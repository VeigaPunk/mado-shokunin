# Survivors — w2 attack on the delivered `tools/mado-globals.py` selftest and v2 fixtures

Seat `ExecMutDelivered`, mado round 41 (w2), lane `mado-shokunin`.
Tool under attack: `tools/mado-globals.py` at DATA commit
`07f2641696b5ac73de1404ea737a9f27e9819aa1` (sha256
`286c051f648f24b23475a893d386f5366b91df00b7e87924bc212c8bf797f55e`, byte-identical to
`.ufo/waves/round-41/c1/ctl-ref-tool-v2.py.txt`).
Predicate: `quality/counters/c1-r41-globals-v2.py` (PRED-C1-r41-v2, 39 fixtures, clauses
a,b,b2,b3,g), rev `07f2641…`, nonce `c1w2mut0001` (identical lattice across all runs).

Baseline: `fixtures=39/39 verdict=TARGET_MET`, selftest `63/63`, clause b2 `sites=18
killed=6/6 forced_dead=1`, b3 both variants ok (`logs/_baseline.log`).

## Result

**64 new single-edit mutants** (one contiguous textual replacement each; zero
(old,new) overlap with the 55 frozen control pairs of `ctl/run-c1-v2-controls.py`
and the 42 w1 `gen_mutants.py` pairs; all outside the matrix.md operator set):

- **28 killed** (each fails ≥1 frozen fixture).
- **33 TARGET_MET survivors** (fixtures=39/39, all clauses) — listed below.
- **3 fixtures=39/39 but clause-failed** (TARGET_MISSED): M113, M115, M154 — the
  selftest/clause machinery catches the *tally* corruption even though all 39
  fixtures pass.

Every survivor is either a **missing fixture class** (a verified kill fixture
exists: the counter's own model diverges from the mutant, so a one-line fixture
addition would score it) or an **equivalent/self-test-integrity** finding
(proved by code argument + corpus equality, see `verify_kill_fixtures.py`
receipt `logs/_killfix.log`).

## Survivor table

| mutant (single edit) | kind | kill fixture / proof |
|---|---|---|
| M100-ver-zero-rejected | missing value domain | `(ver 0)` advert → model: session ver=0, rc0; mutant: line ignored → UNRECOGNIZED_FORMAT |
| M101-ts-minus-only | missing value domain | `+02:00` timestamp → model accepts; mutant ignores line |
| M102-year-locked-2026 | missing value domain | `2027-…` timestamp → model accepts; mutant ignores line (all fixtures use 2026) |
| M103-host-spaces-allowed | missing value domain | host `a b` (space) → model: ignored line, rc4; mutant parses advert |
| M104-level-warning-accepted | missing value domain | `[WARNING]` advert → model: ignored line, rc4; mutant parses advert (fixtures only have `[LOG]`/`[ERR]`/`[log]`/`[Log]`) |
| M105-boot-33hex | missing value domain | 33-hex `-- Boot` line → model: boot stays `-`; mutant adopts boot id |
| M106-diff-added-empty-X | missing value domain | two sessions with identical name sets (`--diff`) → model renders `added=-`; mutant renders `added=X` (every frozen diff has a non-empty added side) |
| M111-live-too-large-ge | live boundary | live stub emitting exactly 8 MiB then EOF → ref: NO_SESSIONS rc3; mutant: journalctl_too_large rc5 |
| M116-ts-fractional-seconds | missing value domain | `T13:00:00.250-03:00` → model: ignored line; mutant parses advert |
| M117-name-dot-allowed | missing value domain | name `wl.seat` → model: ignored line; mutant parses advert |
| M135-month-validator | missing value domain | month `13` → model accepts; mutant ignores line |
| M145-host-length-cap128 | missing value domain | 129-char host → model accepts (\S+); mutant ignores line |
| M146-pid-length-cap7 | missing value domain | pid `12345678` (8 digits) → model accepts; mutant ignores line |
| M112-read-chunk-2MiB | equivalent | `os.read(fd,n)` returns min(n, available); loop/EOF identical for every input |
| M114-selftest-return-flat | selftest integrity | `return 0 if ok == n else 1` → `return 0`: only differs when an internal check fails; no external input can reach that state today; clause b2 still kills flipped product comparisons (it observes k≠n) |
| M125-usage-exit-3 | equivalent | edit lands in unreachable `except SystemExit` branch (ap.error overridden, add_help=False) |
| M131-stderr-pipe | equivalent (theoretical) | journalctl stubs write nothing to stderr; divergence would need a stub filling stderr before stdout EOF |
| M132-expect-dups-not-deduped | equivalent | `report()` re-applies `set()` to expects; dedup in `run()` is redundant |
| M137-selftest-timeout-reset-drop | equivalent | LIVE_TIMEOUT reset occurs after its last use in the selftest |
| M143-selftest-ts-literal-change | equivalent | selftest literal ts is consumed only by the ADVERT regex, which accepts both ± offsets |
| M138…M163 (13 probe deletions) | selftest integrity | each removes one `check(...)` statement; selftest still reports k==n≥50; no product behaviour changes (probe deletions are undetectable by the predicate) |

## The 3 clause-failed 39/39 mutants (TARGET_MISSED)

| mutant | why clause fails |
|---|---|
| M113-selftest-ok-always (`ok += bool(cond)` → `ok += 1`) | selftest tally is corrupted, so every clause-b2 flipped product comparison "passes" its selftest (killed=1/6 < 4) |
| M115-selftest-n-twice (`n += 1` → `n += 2`) | clause b: k(63) ≠ n(126) |
| M154-selftest-check-cond-negate | clause b: the negated check fails → k < n |

## Killed mutants (28) and the fixture that kills each (first failing fixture)

| mutant | kills |
|---|---|
| M107-diff-removed-empty-X | vernum0 (frozen fixture has an empty removed side — asymmetry with M106) |
| M108-ignored-counts-twice | gen3, nosess0, vernum0, levelcase0, … |
| M109-ver-min-not-max | gen0…gen5 |
| M110-name-count-adds-two | gen0…gen5 |
| M118-open-nonblock-drop | fifo0 |
| M119-loop-lt-maxbytes | toolarge0 |
| M120/M121-diff-added/removed-unsorted | gen1, gen2, gen6, diff0, live0, live1 |
| M122-unit-loosened-plus | gen3, nosess0 |
| M123-verdict-unrec-overrides | gen3, vernum0, levelcase0, … |
| M124-maxbytes-9MiB | toolarge0, livelarge0 |
| M126-session-init-adverts-one | gen0…gen5 |
| M127-guard-raw-compare | usage0 |
| M128-unit-flag-longform | live0, live1, liveenv0, livelarge0 |
| M129-global-line-column-swap | gen0…gen5 |
| M130-ignoree-short-iso | live0, live1, liveenv0, livelarge0 |
| M133-diff-none-line-text | diff1, nosess1 |
| M134-last-first-column-swap | gen0…gen5 |
| M136-summary-ignore-position | gen0…gen5 |
| M144-live-timeout-zero | live0, live1, liveenv0, livelarge0, livehang0 |
| M147-os-exit | gen0…gen5 (stdout lost) |
| M148-toolarge-exit-3 | toolarge0 |
| M149-live-failed-reason-text | livehang0 |
| M150-live-too-large-reason | livelarge0 |
| M151-badexpect-exit-3 | badexpect0, expectlatest0 |
| M152-unrec-verdict-exit-3 | nosess0, unrec0 |
| M153-ok-verdict-exit-1 | gen0, gen2, gen4, gen6, diff0, diff1 |
| M160-argv-order-reversed | live0, live1, liveenv0, livelarge0 |

## Findings the survivors make (attack conclusions)

1. **Value domains the v2 lattice still cannot see** (12 distinct missing fixture
   classes): ver=0; `+` zone offsets; non-2026 years; space-containing hosts;
   `[WARNING]` (any third level) adverts; 33-hex boot ids; fractional seconds;
   dotted interface names; calendar-invalid months; >128-char hosts; >7-digit
   pids; and an **empty added-side `--diff`** (M106) — while the removed side
   is covered by vernum0 (M107 is killed). All twelve are single-journal
   additions.
2. **Live boundary**: exactly-8-MiB output is not exercised (`livelarge0`
   overruns 9 MiB); the `>` vs `>=` size check is indistinguishable on it.
3. **Selftest integrity is not load-bearing for the predicate**: 13 of the 63
   selftest probes can be deleted one at a time with the whole predicate still
   green; `return 0` flatlining also passes clause b (k==n stays intact). Clause
   b only checks the *tally* (k==n), not that any probe asserts anything — a
   probe-deletion or a flat `ok`/`return` cannot be detected by the counter.
   Only *tally-corrupting* edits (M113/M115/M154) are caught.

- generation: `python3 gen_mutants.py` → `MUTANTS total=64 bad=0` (each old
  occurs exactly once; mutants/64 files).
- novelty: pairwise (old,new) comparison vs `ctl/run-c1-v2-controls.py`
  (55 pairs) and `w1/ExecC1ExtraMutants/gen_mutants.py` (42 pairs) →
  `pair-overlap: []`, `source-overlap: []` (script in seat dir).
- scoring: `python3 -I quality/counters/c1-r41-globals-v2.py --repo LANE
  --rev 07f2641… --tool mutants/<name>.py --nonce c1w2mut0001` —
  6-way parallel; `logs/<name>.log`, `logs/_summary.tsv`.
- kill fixtures: `python3 verify_kill_fixtures.py` → `logs/_killfix.log`
  → `KILLFIX fails=0`: every non-equivalent survivor has a verified kill
  fixture (reference reproduces the model, mutant diverges); every equivalent
  survivor passes a 12-journal corpus equality run; the 13 probe deletions pass
  the corpus and differ from the reference only in the selftest tally
  (63→62), as intended.
- safety: no pacman (host-wide pause respected), no new tools installed
  (host python3 3.14.8), no git/jj mutation, read-only git `show` only.

## Limits

- Kill fixtures are mine, not the counter's; adding them is the L1's decision.
- Survivor verdicts are for nonce `c1w2mut0001`; the missing classes are
  structural (value domains), so other nonces cannot close them.
- M114/M113 show the predicate cannot tell a *truthful* selftest from a
  flatlined one; whether that matters is a contract question for the L1.
